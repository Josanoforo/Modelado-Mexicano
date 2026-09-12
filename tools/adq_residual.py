#!/usr/bin/env python3
"""Alta/actualización atómica de un objeto residual de adquisición.

No crea otra cola: escribe la fila en el registro canónico con
``tsv_crudo.upsert_fila`` y regenera su vista. La metadata estructurada vive
en ``nota`` para que selector, cierre y operador hablen del objeto exacto, no
del padre documental o parcialmente obtenido.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
REGISTRO = RAIZ / "data" / "curacion-registro" / "cola-adquisicion-registro.tsv"
VISTA = RAIZ / "data" / "cola-adquisicion-v1_0.tsv"
MARCADOR = "RESIDUAL-ADQ-V1="
ESTADOS = {
    "PENDIENTE",
    "SIN-FETCH",
    "SOLICITUD-PREPARADA",
    "NO-ACCESIBLE",
    "NO-ENCONTRADO",
    "NO-OBTENIDO-POR-ESTE-AGENTE",
    "OBTENIDO",
}
_ID = re.compile(r"^[A-Z0-9][A-Z0-9_.-]*$")
_AUTORIZADA = re.compile(
    r"^AUTORIZADA:(?P<quien>[^/\s]+)/(?P<fecha>\d{4}-\d{2}-\d{2})/(?P<objeto>[^/\s]+)$"
)


def metadata_de_nota(nota: str) -> dict | None:
    """Extrae la metadata residual sin interpretar la prosa histórica."""
    for parte in (nota or "").split(" || "):
        if parte.startswith(MARCADOR):
            try:
                dato = json.loads(parte[len(MARCADOR):])
            except json.JSONDecodeError:
                return None
            return dato if isinstance(dato, dict) else None
    return None


def _nota(meta: dict, historia: str = "") -> str:
    bloque = MARCADOR + json.dumps(meta, ensure_ascii=False, separators=(",", ":"))
    return bloque + (" || " + historia.strip() if historia.strip() else "")


def construye_fila(*, objeto_id: str, padre: str, consumidor: str,
                   objeto: str, cobertura: str, residual: str, via: str,
                   autoridad: str, siguiente_accion: str, estado: str,
                   prioridad: str, origen: str, url: str = "",
                   nota: str = "", existente: dict | None = None) -> dict[str, str]:
    if not _ID.fullmatch(objeto_id):
        raise ValueError("objeto_id debe ser un identificador estable A-Z/0-9/_.-")
    if estado.split("(")[0] not in ESTADOS:
        raise ValueError(f"estado residual no permitido: {estado}")
    obligatorios = {
        "padre": padre, "consumidor": consumidor, "objeto": objeto,
        "cobertura": cobertura, "residual": residual, "via": via,
        "autoridad": autoridad, "siguiente_accion": siguiente_accion,
        # En una actualización, el origen histórico de la fila no se
        # reemplaza por el acto que sólo añadió estructura al residual.
        "origen": previa.get("origen") or origen,
    }
    vacios = [k for k, v in obligatorios.items() if not str(v).strip()]
    if vacios:
        raise ValueError("campos residuales vacíos: " + ", ".join(vacios))
    if estado.split("(")[0] == "PENDIENTE":
        m = _AUTORIZADA.fullmatch(autoridad)
        if not m or m.group("objeto") != objeto_id:
            raise ValueError("PENDIENTE exige AUTORIZADA:<quien>/<fecha>/<objeto_id>")
        if not url:
            raise ValueError("PENDIENTE exige una URL ejecutable")
    meta = {"padre": padre, "consumidor": consumidor, "objeto": objeto,
            "cobertura": cobertura, "residual": residual, "via": via,
            "autoridad": autoridad, "siguiente_accion": siguiente_accion}
    previa = existente or {}
    return {
        "fila_origen": previa.get("fila_origen") or f"residual:{objeto_id}",
        "fuente_canonica": objeto_id,
        "fuente_canonica_normalizada": objeto_id,
        "discordancia_alias": previa.get("discordancia_alias") or "SIN_ALIAS",
        "estado_A4A5": estado,
        "prioridad": prioridad,
        "url_conocida": url,
        "ids_manifiesto": previa.get("ids_manifiesto", ""),
        "origen": origen,
        "nota": _nota(meta, nota or previa.get("nota", "")),
    }


def upsert_residual(fila: dict[str, str], registro: Path = REGISTRO,
                    vista: Path = VISTA) -> None:
    sys.path.insert(0, str(RAIZ / "tools" / "curador_registro"))
    import tsv_crudo
    import vista_cola_adquisicion

    lineas = tsv_crudo.leer_lineas(registro)
    campos = lineas[0].split("\t")
    tsv_crudo.upsert_fila(registro, fila, campos, clave="fuente_canonica")
    contenido = vista_cola_adquisicion.render(tsv_crudo.leer_dicts(registro))
    vista.write_text(contenido, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--objeto-id", required=True)
    ap.add_argument("--padre", required=True)
    ap.add_argument("--consumidor", required=True)
    ap.add_argument("--objeto", required=True)
    ap.add_argument("--cobertura", required=True)
    ap.add_argument("--residual", required=True)
    ap.add_argument("--via", required=True)
    ap.add_argument("--autoridad", required=True)
    ap.add_argument("--siguiente-accion", required=True)
    ap.add_argument("--estado", required=True)
    ap.add_argument("--prioridad", default="sin-prioridad-asignada")
    ap.add_argument("--origen", required=True)
    ap.add_argument("--url", default="")
    ap.add_argument("--nota", default="")
    a = ap.parse_args()

    sys.path.insert(0, str(RAIZ / "tools" / "curador_registro"))
    import tsv_crudo
    existentes = {r["fuente_canonica"]: r for r in tsv_crudo.leer_dicts(REGISTRO)}
    fila = construye_fila(
        objeto_id=a.objeto_id, padre=a.padre, consumidor=a.consumidor,
        objeto=a.objeto, cobertura=a.cobertura, residual=a.residual,
        via=a.via, autoridad=a.autoridad, siguiente_accion=a.siguiente_accion,
        estado=a.estado, prioridad=a.prioridad, origen=a.origen, url=a.url,
        nota=a.nota, existente=existentes.get(a.objeto_id),
    )
    upsert_residual(fila)
    print(json.dumps({"ok": True, "objeto_id": a.objeto_id,
                      "estado": a.estado, "registro": str(REGISTRO),
                      "vista": str(VISTA)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
