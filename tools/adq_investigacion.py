#!/usr/bin/env python3
"""Proyecta demanda científica activa y selecciona investigación recurrente."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import re
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


def _tsv(path: Path) -> list[dict[str, str]]:
    """Lee vistas TSV que pueden comenzar con comentarios de derivación."""
    texto = "".join(
        linea for linea in path.read_text(encoding="utf-8").splitlines(True)
        if linea.strip() and not linea.startswith("#"))
    return list(csv.DictReader(io.StringIO(texto), delimiter="\t")) if texto else []


def _texto_nc(base: dict) -> str:
    return " ".join(str(base.get(k) or "") for k in (
        "que_no_se_corrio", "razon", "impacto", "sucesor"))


def _etapa_faltante(base: dict) -> str:
    texto = _texto_nc(base).lower()
    pregunta = str(base.get("que_no_se_corrio") or "").lower()
    sucesor = str(base.get("sucesor") or "").lower()
    accion = f"{pregunta} {sucesor}"
    if re.search(r"presentar|enviar|credencial|login|compra|convenio|contacto|folio", accion):
        return "ACCESO_O_DESCARGA"
    if re.search(r"llenar texto_reactivo|indexar|codebook|diccionario|mapear|join|limpiar", accion):
        return "PREPARACION"
    if re.search(r"buscar|localizar|fuente|microdato|instrumento|reactivo|variable|dato", accion):
        return "FUENTE_O_VARIABLE"
    if re.search(r"prepar|spec", accion):
        return "PREPARACION"
    if re.search(r"calcul|medir|estimar|re-correr|ejecutar", accion):
        return "CALCULO"
    if re.search(r"valid|verific|replay|varianza|diseño", accion):
        return "VALIDACION"
    if re.search(r"adopt|cita corrida0|parametr", accion):
        return "ADOPCION"
    if "decision" in texto or "mesa decide" in texto or "elegir" in texto:
        return "DECISION_CIENTIFICA"
    return "DECISION_O_IMPLEMENTACION"


def _responsable(base: dict, etapa: str) -> str:
    texto = _texto_nc(base).lower()
    sucesor = str(base.get("sucesor") or "").strip()
    if etapa == "ACCESO_O_DESCARGA" or "titular" in texto:
        return "titular-acceso-y-receptor-tecnico"
    if etapa == "DECISION_CIENTIFICA" or "decision-de-mesa" in texto:
        return "mesa"
    if etapa == "FUENTE_O_VARIABLE":
        return "servicio-gen2-38"
    if sucesor and not sucesor.lower().startswith(("sin-asignar", "n/a", "ninguno")):
        return sucesor.split(";", 1)[0]
    return "direccion-programa"


def _siguiente_accion(base: dict, etapa: str, responsable: str) -> str:
    sucesor = str(base.get("sucesor") or "").strip()
    if sucesor and not sucesor.lower().startswith("sin-asignar"):
        return sucesor
    pregunta = str(base.get("que_no_se_corrio") or "brecha vigente").strip()
    if etapa == "FUENTE_O_VARIABLE":
        return f"{responsable}: investigar la brecha explícita: {pregunta}"
    if etapa == "DECISION_CIENTIFICA":
        return f"mesa: resolver con opciones explícitas la brecha: {pregunta}"
    return f"{responsable}: asignar y ejecutar el sucesor de: {pregunta}"


def _ruteo_automatico(base: dict, etapa: str) -> tuple[str, str]:
    """Enruta sólo búsquedas explícitas; nunca revive diferidos por heurística."""
    texto = _texto_nc(base).lower()
    bloqueos = (
        "diferido", "sustituido", "descartado", "fuera-de-perimetro",
        "decisión-de-mesa", "decision-de-mesa", "paro-premisa",
        "requiere-identidad", "vía-comercial-diferida", "via-comercial-diferida",
        "paro-entorno", "gen2-f5",
    )
    if any(x in texto for x in bloqueos):
        return "ESPERA_O_DELEGADA", "precedencia explícita impide reactivación automática"
    if etapa == "FUENTE_O_VARIABLE" and re.search(
            r"buscar|localizar|obtener|adquirir|fuente|microdato|instrumento|reactivo",
            texto):
        return "LISTA_SONDA", "brecha de datos explícita sin compuerta posterior"
    return "NO_SONDA", f"etapa vigente {etapa}; no corresponde investigación externa"


def _contrato_derivado(base: dict) -> dict:
    etapa = _etapa_faltante(base)
    responsable = _responsable(base, etapa)
    ruteo, motivo = _ruteo_automatico(base, etapa)
    identidad = "\t".join(str(base.get(k) or "") for k in (
        "id", "que_no_se_corrio", "impacto", "sucesor", "estado"))
    return {
        "id": base["id"],
        "version_pregunta": "AUTO-NC-v1-" + hashlib.sha256(
            identidad.encode("utf-8")).hexdigest()[:12],
        "consumidor": "/".join(filter(None, (base.get("acto"), base.get("pieza")))),
        "uso": "INVESTIGACION-DE-BRECHA; uso científico por decidir",
        "prioridad_consumidor": 60,
        "bloqueo_material": 1,
        "asignacion": responsable,
        "modos": ["CONSTRUCTO", "HERMANAS", "LATERAL"],
        "poblacion": "NO_ESPECIFICADA_EN_NC; verificar antes de evaluar suficiencia",
        "unidad": "NO_ESPECIFICADA_EN_NC; verificar antes de calcular",
        "periodo": "EL_DECLARADO_POR_LA_NC; no inferir vigencia",
        "variables": base.get("que_no_se_corrio") or "brecha explícita de la NC",
        "evidencia_disponible": base.get("impacto") or "sin evidencia resumida",
        "brecha": base.get("que_no_se_corrio") or "brecha vigente",
        "investigacion_previa": base.get("razon") or "no asentada",
        "frontera_previa": base.get("impacto") or "no asentada",
        "siguiente_accion": _siguiente_accion(base, etapa, responsable),
        "etapa_faltante": etapa,
        "responsable": responsable,
        "estado_ruteo": ruteo,
        "motivo_ruteo": motivo,
        "contrato_operativo": "MINIMO_DERIVADO_DE_NC",
        "opciones_decision": ([
            "MANTENER_ESTADO_VIGENTE",
            "APROBAR_SIGUIENTE_ACCION_DESCRITA",
            "DESCARTAR_O_DIFERIR_CON_CAUSA",
        ] if etapa == "DECISION_CIENTIFICA" else []),
    }


def contratos_vigentes(cfg: dict, raiz: Path = RAIZ) -> dict[str, dict]:
    canonicas = necesidades_canonicas(cfg, raiz)
    explicitos = {x["id"]: x for x in cfg.get("necesidades", [])}
    sucesoras = {
        anterior: item["id"]
        for item in cfg.get("necesidades", [])
        for anterior in item.get("sucede_necesidades", [])
    }
    contratos: dict[str, dict] = {}
    for ident, base in canonicas.items():
        if base.get("estado") != "ABIERTA":
            continue
        if ident in explicitos:
            item = dict(explicitos[ident])
            item.setdefault("etapa_faltante", _etapa_faltante(base))
            item.setdefault("responsable", item.get("asignacion") or _responsable(
                base, item["etapa_faltante"]))
            item.setdefault("estado_ruteo", "LISTA_SONDA" if item.get("lista") else
                            "NO_SONDA")
            item.setdefault("motivo_ruteo", "contrato explícito vigente")
            item.setdefault("contrato_operativo", "COMPLETO_EXPLICITO")
            item.setdefault("opciones_decision", [])
        else:
            item = _contrato_derivado(base)
        if ident in sucesoras:
            item["estado_ruteo"] = "ABSORBIDA_POR_SUCESORA_VIGENTE"
            item["motivo_ruteo"] = (
                f"la investigación continúa bajo {sucesoras[ident]}; no duplicar")
            item["responsable"] = sucesoras[ident]
            item["siguiente_accion"] = (
                f"seguir el estado y la siguiente acción de {sucesoras[ident]}")
        contratos[ident] = item
    return contratos


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
    contratos = contratos_vigentes(cfg, raiz)
    excluidos: list[dict] = []
    candidatas: list[tuple[tuple, dict]] = []

    for item in contratos.values():
        ident = item["id"]
        base = canonicas.get(ident)
        if base is None:
            excluidos.append({"id": ident, "razon": "no existe en la fuente canónica"})
            continue
        if base.get("estado") != "ABIERTA":
            excluidos.append({"id": ident, "razon": f"estado canónico {base.get('estado')}"})
            continue
        if item.get("estado_ruteo") != "LISTA_SONDA" and ident not in nombradas:
            excluidos.append({
                "id": ident,
                "razon": (
                    f"ruteo={item.get('estado_ruteo')}: "
                    f"{item.get('motivo_ruteo')}; responsable={item.get('responsable')}; "
                    f"siguiente={item.get('siguiente_accion')}")})
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

    elegidos = [x for _clave, x in sorted(candidatas, key=lambda x: x[0])[:maximo]]
    por_tope = [x for _clave, x in sorted(candidatas, key=lambda x: x[0])[maximo:]]
    excluidos.extend({"id": x["id"], "razon": f"lista, fuera del tope maximo={maximo}"}
                     for x in por_tope)
    return {
        "version": cfg["version"], "corte": corte.isoformat(), "maximo": maximo,
        "demanda_activa_total": len(abiertas), "demanda_configurada": len(configuradas),
        "demanda_con_contrato_operativo": len(contratos),
        "elegidos": elegidos, "excluidos": excluidos,
    }


def proyecta_elementos(cfg: dict, contratos: dict[str, dict],
                       raiz: Path = RAIZ) -> list[dict]:
    """Cruza cada adopción GEN2 viva con oferta, decisiones, NC y utilidad."""
    usos = _tsv(raiz / cfg["fuente_usos"])
    resultados = {x["resultado_id"]: x for x in _tsv(
        raiz / cfg["fuente_resultados"])}
    demanda = {x["resultado_id"]: x for x in _tsv(
        raiz / cfg["fuente_demanda_resultados"])}
    decisiones = _tsv(raiz / cfg["fuente_decisiones"])
    mapa_modelo = _tsv(raiz / cfg["fuente_necesidad_modelo"])
    utilidad = _tsv(raiz / cfg["fuente_utilidad_modelo"])
    n_por_objeto: dict[str, list[dict]] = {}
    for fila in mapa_modelo:
        n_por_objeto.setdefault(fila["objeto_modelo_origen"], []).append(fila)
    utilidad_por_n: dict[str, list[dict]] = {}
    for fila in utilidad:
        utilidad_por_n.setdefault(fila["necesidad_id"], []).append(fila)

    elementos = []
    for uso in usos:
        if uso.get("activo") != "SI" or uso.get("corrida0_generacion") != "GEN2":
            continue
        resultado_id = uso.get("corrida0_resultado_id") or ""
        resultado = resultados.get(resultado_id, {})
        regla = uso.get("reglas_impacto") or ""
        consumidor = uso["consumidor"]
        necesidades = []
        for ident, contrato in contratos.items():
            por_consumidor = consumidor in contrato.get("consumidores_consulta", [])
            por_regla = regla in contrato.get("reglas_motor", [])
            if por_consumidor or por_regla:
                necesidades.append(ident)
        bloqueada = any(
            any(v.get("consumidor") == consumidor
                for v in contratos[n].get("vinculos_consulta", []))
            for n in necesidades)
        faltantes = []
        if not resultado_id or not resultado:
            faltantes.append("CALCULO")
        elif resultado.get("estado") != "SELLADA":
            faltantes.append("CALCULO_O_SELLO")
        if resultado and resultado.get("validacion_independiente") != "PASA":
            faltantes.append("VALIDACION")
        for ident in necesidades:
            etapa = contratos[ident].get("etapa_faltante")
            if etapa and etapa not in faltantes:
                faltantes.append(etapa)
        modelo = n_por_objeto.get(regla, [])
        necesidades_modelo = sorted({x["necesidad_id"] for x in modelo})
        utilidad_modelo = [
            {
                "relacion_id": x["relacion_id"],
                "necesidad_id": x["necesidad_id"],
                "estado_productivo": x["estado_productivo"],
                "uso_actual": x["uso_actual"],
                "siguiente_accion": x["siguiente_accion"],
                "evidencia_ref": x["evidencia_ref"],
            }
            for n in necesidades_modelo for x in utilidad_por_n.get(n, [])
        ]
        decisiones_resultado = [
            {"objeto": x["objeto"], "decision": x["decision"],
             "fuente": x["fuente"], "fecha": x["fecha"]}
            for x in decisiones if x.get("objeto") == resultado.get("spec_id")]
        anterior = demanda.get(uso["resultado_id"], {})
        evidencias = sorted(set(filter(None, (
            f"{cfg['fuente_usos']}#{uso['resultado_id']}",
            f"{cfg['fuente_resultados']}#{resultado_id}" if resultado_id else None,
            resultado.get("validacion_ref"), uso.get("fuente_replay"),
            *[x.get("fuentes_verificacion") for x in modelo],
            *[f"{cfg['fuente_necesidades']}#{n}" for n in necesidades],
            *[x["fuente"] for x in decisiones_resultado],
        ))))
        if bloqueada:
            situacion = "ADOPTADO_EN_REGISTRO_PERO_BLOQUEADO_PARA_EMISION"
        elif necesidades:
            situacion = "ADOPTADO_PARA_USO_ACOTADO_CON_BRECHA_PROSPECTIVA"
        elif resultado.get("estado") == "SELLADA" and resultado.get(
                "validacion_independiente") == "PASA":
            situacion = "ADOPTADO_Y_VALIDADO_PARA_USO_VIGENTE"
        else:
            situacion = "ADOPTADO_CON_TRABAJO_PENDIENTE"
        siguientes = [contratos[n]["siguiente_accion"] for n in necesidades]
        if not siguientes:
            siguientes = [
                "mantener el contrato vigente; reabrir sólo ante nueva versión, "
                "evidencia contradictoria o cambio de uso"]
        elementos.append({
            "elemento_id": uso["resultado_id"],
            "consumidor": consumidor,
            "regla": regla,
            "uso_vigente": uso.get("uso_solicitado"),
            "resultado_id": resultado_id,
            "resultado_estado": resultado.get("estado") or "AUSENTE",
            "validacion_independiente": resultado.get("validacion_independiente") or
            "NO_HECHA",
            "adopcion": "ADOPTADO_EN_CONSUMIDOR_VIGENTE",
            "antecedente_gen1": {
                "valor": anterior.get("valor_legacy") or "NO_DECLARADO",
                "estado": anterior.get("estado") or "NO_DECLARADO",
                "vigencia": anterior.get("vigencia") or "NO_DECLARADA",
            },
            "situacion": situacion,
            "faltantes": faltantes,
            "necesidades_nc_abiertas": necesidades,
            "necesidades_utilidad_modelo": necesidades_modelo,
            "cruce_utilidad_modelo": (
                "RELACIONES_EXACTAS_POR_OBJETO_MODELO" if necesidades_modelo else
                "SIN_RELACION_EXACTA_POR_REGLA; no equivale a ausencia de datos"),
            "utilidad_modelo": utilidad_modelo,
            "decisiones_posteriores": decisiones_resultado,
            "dependencias": {
                "resultado": resultado.get("depende_de") or None,
                "funciones": resultado.get("funciones_dependencia") or None,
                "camino_linaje": uso.get("camino_linaje") or None,
            },
            "evidencias": evidencias,
            "siguiente_accion": siguientes,
        })
    return elementos


def proyecta_demanda(cfg: dict, corte: dt.date, raiz: Path = RAIZ) -> dict:
    """Vista total: ninguna NC ni adopción GEN2 desaparece fuera del selector."""
    canonicas = necesidades_canonicas(cfg, raiz)
    contratos = contratos_vigentes(cfg, raiz)
    filas = []
    for ident, base in sorted(canonicas.items()):
        if base.get("estado") != "ABIERTA":
            continue
        contrato = contratos[ident]
        estado = _lee_json(raiz / cfg["estado_dir"] / f"{ident}.json")
        if estado.get("version_pregunta") != contrato["version_pregunta"]:
            estado = {}
        filas.append({
            "id": ident,
            "version_pregunta": contrato["version_pregunta"],
            "pregunta": base.get("que_no_se_corrio", ""),
            "consumidor": contrato["consumidor"],
            "uso": contrato["uso"],
            "poblacion": contrato["poblacion"],
            "unidad": contrato["unidad"],
            "periodo": contrato["periodo"],
            "variables": contrato["variables"],
            "evidencia_disponible": contrato["evidencia_disponible"],
            "brecha": contrato["brecha"],
            "investigacion_previa": contrato["investigacion_previa"],
            "frontera": estado.get("frontera_no_examinada") or
            contrato["frontera_previa"],
            "cursor_continuacion": estado.get("cursor_continuacion"),
            "prioridad": contrato["prioridad_consumidor"],
            "etapa_faltante": contrato["etapa_faltante"],
            "responsable": contrato["responsable"],
            "siguiente_accion": contrato["siguiente_accion"],
            "estado_ruteo": contrato["estado_ruteo"],
            "motivo_ruteo": contrato["motivo_ruteo"],
            "opciones_decision": contrato["opciones_decision"],
            "suficiencia": estado.get("suficiencia") or
            contrato.get("suficiencia_actual"),
            "contrato_operativo": contrato["contrato_operativo"],
            "evidencias": [f"{cfg['fuente_necesidades']}#{ident}"],
        })
    elementos = proyecta_elementos(cfg, contratos, raiz)
    fuente = raiz / cfg["fuente_necesidades"]
    fuentes = [cfg[k] for k in (
        "fuente_necesidades", "fuente_usos", "fuente_resultados",
        "fuente_demanda_resultados", "fuente_decisiones",
        "fuente_necesidad_modelo", "fuente_utilidad_modelo")]
    fuentes_sha = {
        ruta: hashlib.sha256((raiz / ruta).read_bytes()).hexdigest()
        for ruta in fuentes
    }
    canon_fuentes = "".join(
        f"{ruta}\t{sha}\n" for ruta, sha in sorted(fuentes_sha.items()))
    return {
        "generado": True, "version": cfg["version"], "corte": corte.isoformat(),
        "fuente": cfg["fuente_necesidades"],
        "sha256_fuente": hashlib.sha256(fuente.read_bytes()).hexdigest(),
        "fuentes_sha256": fuentes_sha,
        "sha256_insumos_demanda": hashlib.sha256(
            canon_fuentes.encode("utf-8")).hexdigest(),
        "advertencia_suficiencia": (
            "cero tareas elegibles sólo describe el selector; nunca acredita "
            "suficiencia general ni cierra necesidades"),
        "total_activas": len(filas),
        "contrato_completo": sum(
            x["contrato_operativo"] == "COMPLETO_EXPLICITO" for x in filas),
        "contrato_minimo_derivado": sum(
            x["contrato_operativo"] == "MINIMO_DERIVADO_DE_NC" for x in filas),
        "contrato_incompleto": 0,
        "elementos_gen2_vigentes_total": len(elementos),
        "elementos_con_brecha_abierta": sum(
            bool(x["necesidades_nc_abiertas"]) for x in elementos),
        "elementos_gen2": elementos,
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
    validas = contratos_vigentes(cfg, raiz)
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
                          "contrato_minimo_derivado": dato[
                              "contrato_minimo_derivado"],
                          "contrato_incompleto": dato["contrato_incompleto"],
                          "elementos_gen2_vigentes_total": dato[
                              "elementos_gen2_vigentes_total"]},
                         ensure_ascii=False))
        return 0
    ap.error("elige --selecciona, --reserva-seleccion, --libera, "
             "--actualiza-desde-resultados o --escribe-proyeccion")


if __name__ == "__main__":
    raise SystemExit(main())
