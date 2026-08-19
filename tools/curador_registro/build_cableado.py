#!/usr/bin/env python3
"""Ensambla el cableado durable de BARRIDO-2. No decide semántica.

ACTO B2-SEMANTICO, 18/ago/2026. El §21 del encargo madre autoriza esta
herramienta con un límite explícito y estrecho:

    build_cableado.py, si se crea, solo: ensambla; proyecta decisiones;
    incorpora terminales; valida; ordena determinísticamente; escribe.
    No decide correspondencias semánticas.

De modo que aquí no hay matching, ni heurística, ni lectura de N1-N33. Cada
celda de cada fila se copia de un producto que ya existe y que otro paso
firmó: la tarea (identidad material), la propuesta (juicio del curador,
supervisado), la decisión de `integrate_barrido2` (estado de integración) y el
reporte durable (grado, tipo de afirmación y texto recortado). Si una fila no
puede armarse con esas cuatro fuentes, no se inventa: se rechaza y el comando
termina en 1.

El producto es `data/cableado-universo-v1_0.tsv` con las 26 columnas del §21,
que son exactamente las que `tests/check.py` valida en T23 (`CABLEADO_CABECERA`).
El cableado es una PROYECCIÓN de decisiones y conocimiento, no una credencial
de escritura (§19): nada de lo que se escribe aquí puede mutar el registro.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "BARRIDO2-CABLEADO-1.0"

# Las 26 del §21, en su orden exacto. Se mantiene una copia literal aquí, y no
# un import desde tests/, porque `tests/check.py` es el VALIDADOR: que el
# escritor y el validador compartan la constante haría que un error en la
# cabecera se validara a sí mismo. Es el mismo defecto de escritor-y-validador
# que el eje durable ya pagó una vez en este acto (ADR-103); la prueba dirigida
# compara ambas listas y falla si divergen.
CABLEADO_CABECERA = [
    "payload_id", "representacion_id", "sha256_12", "sha256", "fuente_canonica",
    "objeto_logico_id", "necesidad_id", "reactivo_id", "texto_reactivo_recortado",
    "grado_inspeccion", "afirmacion_tipo", "veredicto_a4", "evidencia",
    "frontera_inspeccion", "reporte_neutral_ref", "propuesta_id", "relacion_id",
    "semrun_id", "requiere_decision_mesa", "decision_mesa_id", "dependencia_fp24",
    "razon_gate", "estado_integracion", "cegamiento_roto", "fecha", "razon",
]

# Las cinco columnas de texto durable con límite de 160 (§21, T23 regla 8).
TEXTO_160 = {
    "texto_reactivo_recortado", "razon_gate", "evidencia",
    "frontera_inspeccion", "razon",
}

LIMITE_DURABLE = 160
NO_APLICA = "NO-APLICA"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: Iterable[dict[str, str]]) -> None:
    """TSV plano, sin csv.writer: este repositorio guarda tabuladores sin
    comillas y el escritor estándar reescribiría las celdas con comillas."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(fields)]
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            if "\t" in value or "\n" in value or "\r" in value:
                raise ValueError(f"celda con separador crudo en {field}: {value[:60]!r}")
            cells.append(value)
        lines.append("\t".join(cells))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def durable(value: str) -> str:
    """Compacta a una línea y respeta el límite. Nunca devuelve vacío: la
    regla 7 del T23 prohíbe celda vacía en las 26 columnas, y el §21 fija el
    vocabulario de ausencia (NO-APLICA / NO-DETERMINADO / [REDACTADO-PRIVACIDAD])."""
    text = " ".join((value or "").split()) or NO_APLICA
    return text if len(text) <= LIMITE_DURABLE else text[: LIMITE_DURABLE - 1] + "…"


def ensambla(
    propuestas: list[dict[str, str]],
    tareas: list[dict[str, str]],
    decisiones: list[dict[str, str]],
    reportes: list[dict[str, str]],
    semrun_id: str,
    fecha: str,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Una fila por propuesta. Sin propuesta no hay fila: el cableado proyecta
    juicio supervisado, no material suelto."""
    tareas_por_id = {t["tarea_id"]: t for t in tareas}
    decision_por_propuesta = {d["propuesta_id"]: d for d in decisiones}
    reporte_por_id = {r["reporte_id"]: r for r in reportes}

    filas: list[dict[str, str]] = []
    rechazos: list[dict[str, str]] = []

    for propuesta in propuestas:
        pid = propuesta["propuesta_id"]

        def rechaza(motivo: str) -> None:
            rechazos.append({"propuesta_id": pid, "motivo": motivo})

        tarea = tareas_por_id.get(propuesta.get("tarea_id", ""))
        if tarea is None:
            rechaza("PROPUESTA_SIN_TAREA")
            continue
        decision = decision_por_propuesta.get(pid)
        if decision is None:
            rechaza("PROPUESTA_SIN_DECISION_DE_INTEGRACION")
            continue
        reporte = reporte_por_id.get(tarea.get("reporte_id", ""))
        if reporte is None:
            rechaza("TAREA_SIN_REPORTE_DURABLE")
            continue

        sha = tarea["sha256"]
        if not re.fullmatch(r"[0-9a-f]{64}", sha or ""):
            rechaza("SHA256_INVALIDO")
            continue

        filas.append({
            "payload_id": tarea["payload_id"],
            "representacion_id": tarea["representacion_id"],
            "sha256_12": sha[:12],
            "sha256": sha,
            "fuente_canonica": durable(tarea["fuente_canonica"]),
            "objeto_logico_id": tarea["objeto_logico_id"],
            "necesidad_id": tarea["necesidad_id"],
            "reactivo_id": tarea["reactivo_id"],
            # El texto sale del reporte DURABLE, no del índice E2 privado: el
            # cableado tiene que ser dereferenciable en un clon limpio (§24).
            "texto_reactivo_recortado": durable(reporte.get("descripcion_neutral", "")),
            "grado_inspeccion": durable(reporte.get("grado_inspeccion", "")),
            "afirmacion_tipo": durable(reporte.get("afirmacion_tipo", "")),
            "veredicto_a4": propuesta["veredicto_a4"],
            "evidencia": durable(propuesta["evidencia_ref"]),
            "frontera_inspeccion": durable(propuesta["frontera_semantica"]),
            "reporte_neutral_ref": f"{tarea['reporte_id']}:{tarea['reporte_record_sha256']}",
            "propuesta_id": pid,
            "relacion_id": propuesta["relacion_id_actual"],
            "semrun_id": semrun_id,
            "requiere_decision_mesa": propuesta["requiere_decision_mesa"],
            "decision_mesa_id": propuesta["decision_mesa_id"],
            "dependencia_fp24": propuesta["dependencia_fp24"],
            "razon_gate": durable(propuesta["razon_gate"]),
            "estado_integracion": decision["estado_integracion"],
            # Ningún curador de este acto rompió cegamiento; si alguno lo
            # rompiera, la excepción se declara aquí, no se omite.
            "cegamiento_roto": "NO",
            "fecha": fecha,
            "razon": durable(decision.get("razon_integracion", "")),
        })

    # Orden determinista y total: dos corridas sobre los mismos insumos deben
    # dar los mismos bytes (§28.16).
    filas.sort(key=lambda f: (f["payload_id"], f["representacion_id"],
                              f["objeto_logico_id"], f["propuesta_id"]))
    return filas, rechazos


def valida(filas: list[dict[str, str]]) -> list[str]:
    """Revalida lo escrito con las reglas del §21 que son del ensamblador.

    No duplica T23 entera -- T23 es el juez y corre aparte; esto evita
    entregarle un producto que ya se sabe roto."""
    errores: list[str] = []
    for n, fila in enumerate(filas, 2):
        for col in CABLEADO_CABECERA:
            if fila.get(col, "") == "":
                errores.append(f"fila {n}: celda vacía en {col}")
        for col in TEXTO_160:
            if len(fila.get(col, "")) > LIMITE_DURABLE:
                errores.append(f"fila {n}: {col} excede {LIMITE_DURABLE}")
        if fila["sha256_12"] != fila["sha256"][:12]:
            errores.append(f"fila {n}: sha256_12 no es prefijo")
        if not re.fullmatch(r"[^:\s]+:[0-9a-f]{64}", fila["reporte_neutral_ref"]):
            errores.append(f"fila {n}: reporte_neutral_ref no dereferenciable")
        fp24, requiere, decision = (
            fila["dependencia_fp24"], fila["requiere_decision_mesa"], fila["decision_mesa_id"])
        if fp24 == "SI" and (requiere != "SI" or decision != "FP-24"):
            errores.append(f"fila {n}: dependencia_fp24=SI inconsistente")
        if fp24 == "NO" and (requiere != "NO" or decision != NO_APLICA):
            errores.append(f"fila {n}: dependencia_fp24=NO inconsistente")
        if fp24 == "SI" and fila["estado_integracion"] == "INTEGRADA":
            errores.append(f"fila {n}: dependencia_fp24=SI no puede quedar INTEGRADA")
    return errores


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proposals", type=Path, required=True)
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--reports", type=Path, required=True)
    parser.add_argument("--semrun-id", required=True)
    parser.add_argument("--fecha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    filas, rechazos = ensambla(
        read_tsv(args.proposals.resolve()), read_tsv(args.tasks.resolve()),
        read_tsv(args.decisions.resolve()), read_tsv(args.reports.resolve()),
        args.semrun_id, args.fecha,
    )
    errores = valida(filas)
    if not errores:
        write_tsv(args.output.resolve(), CABLEADO_CABECERA, filas)

    resumen: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "filas": len(filas),
        "rechazos": rechazos,
        "errores_validacion": errores[:20],
        "estados": {},
        "salida_sha256": sha256_file(args.output.resolve()) if not errores else NO_APLICA,
    }
    for fila in filas:
        estado = fila["estado_integracion"]
        resumen["estados"][estado] = resumen["estados"].get(estado, 0) + 1
    print(json.dumps(resumen, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if (errores or rechazos) else 0


if __name__ == "__main__":
    raise SystemExit(main())
