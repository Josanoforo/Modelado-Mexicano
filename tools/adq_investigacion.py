#!/usr/bin/env python3
"""Proyecta demanda científica activa y selecciona investigación recurrente."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import tempfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = RAIZ / "data" / "adq-investigacion.yaml"


def _fecha(valor: object) -> dt.date | None:
    if valor in (None, ""):
        return None
    if isinstance(valor, dt.date):
        return valor
    return dt.date.fromisoformat(str(valor))


def _ahora() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _json_atomico(path: Path, dato: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporal = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dato, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(temporal, path)
    except BaseException:
        try:
            os.unlink(temporal)
        except FileNotFoundError:
            pass
        raise


def cargar_config(path: Path = CONFIG) -> dict:
    dato = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(dato, dict) or dato.get("version") != "GEN2-ADQ-INVESTIGACION-V1":
        raise ValueError("configuración de investigación ausente o versión inválida")
    return dato


def necesidades_canonicas(cfg: dict, raiz: Path = RAIZ) -> dict[str, dict]:
    ruta = raiz / cfg["fuente_necesidades"]
    with ruta.open(encoding="utf-8", newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f, delimiter="\t")}


def _lee_json(path: Path) -> dict:
    try:
        dato = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return dato if isinstance(dato, dict) else {}


def _reserva_activa(path: Path, ahora: dt.datetime) -> dict | None:
    dato = _lee_json(path)
    try:
        vence = dt.datetime.fromisoformat(dato["vence"])
    except (KeyError, TypeError, ValueError):
        return None
    return dato if vence > ahora else None


def selecciona(cfg: dict, corte: dt.date, maximo: int = 3,
               nombradas: set[str] | None = None, raiz: Path = RAIZ,
               ahora: dt.datetime | None = None) -> dict:
    nombradas = nombradas or set()
    ahora = ahora or _ahora()
    canonicas = necesidades_canonicas(cfg, raiz)
    estado_dir = raiz / cfg["estado_dir"]
    reserva_dir = raiz / cfg["reservas_runtime_dir"]
    configuradas = {n["id"] for n in cfg.get("necesidades", [])}
    abiertas = {i for i, r in canonicas.items() if r.get("estado") == "ABIERTA"}
    excluidos: list[dict] = []
    candidatas: list[tuple[tuple, dict]] = []

    for item in cfg.get("necesidades", []):
        ident = item["id"]
        base = canonicas.get(ident)
        if base is None:
            excluidos.append({"id": ident, "razon": "no existe en la fuente canónica"})
            continue
        if base.get("estado") != "ABIERTA":
            excluidos.append({"id": ident, "razon": f"estado canónico {base.get('estado')}"})
            continue
        if not item.get("lista", False) and ident not in nombradas:
            excluidos.append({"id": ident, "razon": "contrato operativo no listo para investigación"})
            continue
        reserva_cfg = _fecha(item.get("reserva_hasta"))
        if (item.get("asignacion") not in (None, "", "servicio-gen2-38")
                and reserva_cfg and corte <= reserva_cfg):
            excluidos.append({"id": ident, "razon":
                              f"asignada a {item['asignacion']} hasta {reserva_cfg}"})
            continue
        reserva = _reserva_activa(reserva_dir / f"{ident}.json", ahora)
        if reserva:
            excluidos.append({"id": ident, "razon":
                              f"reserva runtime de {reserva.get('owner')} hasta {reserva.get('vence')}"})
            continue
        estado = _lee_json(estado_dir / f"{ident}.json")
        if estado.get("version_pregunta") not in (None, item["version_pregunta"]):
            estado = {}  # pregunta nueva: no hereda agotamiento de la versión anterior
        proxima = _fecha(estado.get("proxima_revision") or item.get("proxima_revision"))
        if proxima and corte < proxima and ident not in nombradas:
            excluidos.append({"id": ident, "razon": f"revisión no vence hasta {proxima}"})
            continue
        elegido = dict(item)
        elegido["pregunta"] = base.get("que_no_se_corrio", "")
        elegido["impacto_canonico"] = base.get("impacto", "")
        elegido["estado_previo"] = estado
        ultima = _fecha(estado.get("ultima_exploracion"))
        clave = (int(item["prioridad_consumidor"]), -int(item["bloqueo_material"]),
                 ultima.toordinal() if ultima else 0, ident)
        candidatas.append((clave, elegido))

    for ident in sorted(abiertas - configuradas):
        excluidos.append({"id": ident, "razon":
                          "necesidad activa sin contrato operativo de investigación; no se infieren uso/variables"})

    elegidos = [x for _clave, x in sorted(candidatas, key=lambda x: x[0])[:maximo]]
    por_tope = [x for _clave, x in sorted(candidatas, key=lambda x: x[0])[maximo:]]
    excluidos.extend({"id": x["id"], "razon": f"lista, fuera del tope maximo={maximo}"}
                     for x in por_tope)
    return {
        "version": cfg["version"], "corte": corte.isoformat(), "maximo": maximo,
        "demanda_activa_total": len(abiertas), "demanda_configurada": len(configuradas),
        "elegidos": elegidos, "excluidos": excluidos,
    }


def proyecta_demanda(cfg: dict, corte: dt.date, raiz: Path = RAIZ) -> dict:
    """Vista total de ABIERTAS; faltantes quedan explícitos, nunca omitidos."""
    canonicas = necesidades_canonicas(cfg, raiz)
    contratos = {x["id"]: x for x in cfg.get("necesidades", [])}
    filas = []
    for ident, base in sorted(canonicas.items()):
        if base.get("estado") != "ABIERTA":
            continue
        contrato = contratos.get(ident)
        if contrato:
            fila = {
                "id": ident, "pregunta": base.get("que_no_se_corrio", ""),
                "consumidor": contrato["consumidor"], "uso": contrato["uso"],
                "poblacion": contrato["poblacion"], "unidad": contrato["unidad"],
                "periodo": contrato["periodo"], "variables": contrato["variables"],
                "evidencia_disponible": contrato["evidencia_disponible"],
                "brecha": contrato["brecha"],
                "investigacion_previa": contrato["investigacion_previa"],
                "frontera": contrato["frontera_previa"],
                "prioridad": contrato["prioridad_consumidor"],
                "siguiente_accion": contrato["siguiente_accion"],
                "suficiencia": contrato.get("suficiencia_actual"),
                "contrato_operativo": "COMPLETO",
            }
        else:
            fila = {
                "id": ident, "pregunta": base.get("que_no_se_corrio", ""),
                "consumidor": "NO_DETERMINADO_EN_REGISTRO_CANONICO",
                "uso": "NO_DETERMINADO_EN_REGISTRO_CANONICO",
                "poblacion": "NO_DETERMINADA", "unidad": "NO_DETERMINADA",
                "periodo": "NO_DETERMINADO", "variables": "NO_DETERMINADAS",
                "evidencia_disponible": base.get("impacto", ""),
                "brecha": base.get("que_no_se_corrio", ""),
                "investigacion_previa": base.get("razon", ""),
                "frontera": "SIN_CONTRATO_OPERATIVO; no inferir desde prosa",
                "prioridad": "NO_DETERMINADA",
                "siguiente_accion": base.get("sucesor", ""),
                "suficiencia": None, "contrato_operativo": "INCOMPLETO",
            }
        filas.append(fila)
    fuente = raiz / cfg["fuente_necesidades"]
    return {
        "generado": True, "version": cfg["version"], "corte": corte.isoformat(),
        "fuente": cfg["fuente_necesidades"],
        "sha256_fuente": hashlib.sha256(fuente.read_bytes()).hexdigest(),
        "total_activas": len(filas),
        "contrato_completo": sum(x["contrato_operativo"] == "COMPLETO" for x in filas),
        "contrato_incompleto": sum(x["contrato_operativo"] == "INCOMPLETO" for x in filas),
        "necesidades": filas,
    }


def reserva_seleccion(seleccion: dict, owner: str, cfg: dict,
                      raiz: Path = RAIZ, ahora: dt.datetime | None = None) -> list[str]:
    ahora = ahora or _ahora()
    vence = ahora + dt.timedelta(minutes=int(cfg.get("reserva_minutos", 75)))
    directorio = raiz / cfg["reservas_runtime_dir"]
    directorio.mkdir(parents=True, exist_ok=True)
    creadas: list[str] = []
    try:
        for item in seleccion.get("elegidos", []):
            path = directorio / f"{item['id']}.json"
            existente = _reserva_activa(path, ahora)
            if existente and existente.get("owner") != owner:
                raise RuntimeError(f"{item['id']} ya reservado por {existente.get('owner')}")
            _json_atomico(path, {"necesidad_id": item["id"], "owner": owner,
                                "inicio": ahora.isoformat(), "vence": vence.isoformat()})
            creadas.append(item["id"])
    except BaseException:
        libera(owner, cfg, raiz)
        raise
    return creadas


def libera(owner: str, cfg: dict, raiz: Path = RAIZ) -> list[str]:
    directorio = raiz / cfg["reservas_runtime_dir"]
    borradas: list[str] = []
    if not directorio.exists():
        return borradas
    for path in directorio.glob("*.json"):
        if _lee_json(path).get("owner") == owner:
            path.unlink(missing_ok=True)
            borradas.append(path.stem)
    return borradas


def actualiza_desde_resultados(path: Path, cfg: dict, raiz: Path = RAIZ) -> list[str]:
    dato = json.loads(path.read_text(encoding="utf-8"))
    validas = {n["id"]: n for n in cfg.get("necesidades", [])}
    escritas: list[str] = []
    estado_dir = raiz / cfg["estado_dir"]
    for r in dato.get("investigaciones", []):
        ident = r["necesidad_id"]
        if ident not in validas or r["version_pregunta"] != validas[ident]["version_pregunta"]:
            raise ValueError(f"resultado de investigación no corresponde al contrato vigente: {ident}")
        estado = {
            "necesidad_id": ident, "version_pregunta": r["version_pregunta"],
            "ultima_exploracion": dato.get("seleccion_investigacion", {}).get("corte"),
            "estado": r["estado"], "proxima_revision": r["proxima_revision"],
            "cursor_continuacion": r["cursor_continuacion"],
            "frontera_no_examinada": r["frontera_no_examinada"],
            "evidencias": r["evidencias"], "suficiencia": r["suficiencia"],
        }
        _json_atomico(estado_dir / f"{ident}.json", estado)
        escritas.append(ident)
    return escritas


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, default=CONFIG)
    ap.add_argument("--selecciona", action="store_true")
    ap.add_argument("--maximo", type=int, default=3)
    ap.add_argument("--nombrada", action="append", default=[])
    ap.add_argument("--corte")
    ap.add_argument("--reserva-seleccion", type=Path)
    ap.add_argument("--owner")
    ap.add_argument("--libera")
    ap.add_argument("--actualiza-desde-resultados", type=Path)
    ap.add_argument("--escribe-proyeccion", type=Path)
    args = ap.parse_args(argv)
    cfg = cargar_config(args.config)
    if args.selecciona:
        corte = _fecha(args.corte) or dt.date.today()
        print(json.dumps(selecciona(cfg, corte, args.maximo, set(args.nombrada)),
                         ensure_ascii=False, indent=2))
        return 0
    if args.reserva_seleccion:
        if not args.owner:
            ap.error("--reserva-seleccion exige --owner")
        dato = json.loads(args.reserva_seleccion.read_text(encoding="utf-8"))
        print(json.dumps({"reservadas": reserva_seleccion(dato, args.owner, cfg)},
                         ensure_ascii=False))
        return 0
    if args.libera:
        print(json.dumps({"liberadas": libera(args.libera, cfg)}, ensure_ascii=False))
        return 0
    if args.actualiza_desde_resultados:
        print(json.dumps({"actualizadas": actualiza_desde_resultados(
            args.actualiza_desde_resultados, cfg)}, ensure_ascii=False))
        return 0
    if args.escribe_proyeccion:
        corte = _fecha(args.corte) or dt.date.today()
        dato = proyecta_demanda(cfg, corte)
        _json_atomico(args.escribe_proyeccion, dato)
        print(json.dumps({"ruta": str(args.escribe_proyeccion),
                          "total_activas": dato["total_activas"],
                          "contrato_completo": dato["contrato_completo"],
                          "contrato_incompleto": dato["contrato_incompleto"]},
                         ensure_ascii=False))
        return 0
    ap.error("elige --selecciona, --reserva-seleccion, --libera, "
             "--actualiza-desde-resultados o --escribe-proyeccion")


if __name__ == "__main__":
    raise SystemExit(main())
