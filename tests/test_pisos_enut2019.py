#!/usr/bin/env python3
"""Falsadores de la tabla de identidad ENUT 2019 (ACTO GEN2-PISOS-ENUT2019-EJES-1).

La rejilla que este acto EMITE (`forense/prereg-caja/PISOS-ENUT2019-ejes-
metadatos-v1_0.tsv`) debe coincidir uno a uno con la rejilla del ÁRBITRO
(`milpa/tramite-ola5-propuesta-v0.yaml`, entrada
`familia.cuidado.reparto_mujeres40_ejes_enut2024`): mismos ejes, mismas
categorías leídas del yaml (no tecleadas), una fila por celda, ni una más.
Como el dictamen P0 fue NO-CONSTRUIBLE, además se prueba que ninguna fila
trae un piso y que el marcador transporta la causa de la tabla tal cual.

No abre microdatos. Corre standalone (`python3 tests/test_pisos_enut2019.py`)
y expone `corre()` con el mismo arnés que `tests/test_pisos_rejilla.py`.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TABLA = ROOT / "forense/prereg-caja/PISOS-ENUT2019-ejes-metadatos-v1_0.tsv"
SIDECAR = Path(str(TABLA) + ".sha256")
YAML_ARBITRO = ROOT / "milpa/tramite-ola5-propuesta-v0.yaml"
CONSUMER = "familia.cuidado.reparto_mujeres40_ejes_enut2024"
UNIDAD_POR_EJE = {"sexo_edad": "PERSONA", "reparto_hogar": "HOGAR"}


def _tabla() -> list[dict]:
    with TABLA.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader((l for l in fh if not l.startswith("#")),
                                   delimiter="\t"))


def _celdas_arbitro() -> list[tuple[str, str]]:
    d = yaml.safe_load(YAML_ARBITRO.read_text(encoding="utf-8"))
    regla = next(r for r in d["reglas_propuestas"] if r.get("id") == CONSUMER)
    return [(e["eje"], c["celda"]) for e in regla["ejes"] for c in e["celdas"]]


def corre() -> list[str]:
    errores: list[str] = []
    if not TABLA.exists():
        return [f"no existe `{TABLA.relative_to(ROOT)}`"]
    filas = _tabla()
    arbitro = _celdas_arbitro()

    # 1 · rejilla emitida == rejilla del árbitro (ejes y categorías del yaml)
    emitida = [(f["axis"], f["category"]) for f in filas]
    if sorted(emitida) != sorted(arbitro):
        errores.append(f"rejilla emitida {sorted(emitida)} != árbitro {sorted(arbitro)}")
    if len(set(f["cell_id"] for f in filas)) != len(filas):
        errores.append("cell_id duplicado en la tabla")
    if len(filas) != 11:
        errores.append(f"{len(filas)} filas, esperaba 11 (10 sexo_edad + 1 reparto_hogar)")

    # 2 · dictamen NO-CONSTRUIBLE: una sola causa, unidad por eje del árbitro,
    #     consumer exacto, ningún RESULT que el marcador pudiera leer como piso
    causas = {f["reason"] for f in filas}
    if {f["status"] for f in filas} != {"NO-CONSTRUIBLE"}:
        errores.append("toda fila debe ser NO-CONSTRUIBLE (dictamen P0 por texto)")
    if len(causas) != 1 or not next(iter(causas)).startswith("ENUT 2019 sin tvar_crea"):
        errores.append(f"causa única esperada, se leyó {causas}")
    for f in filas:
        if f["consumer"] != CONSUMER:
            errores.append(f"{f['cell_id']}: consumer {f['consumer']!r}")
        if f["unit"] != UNIDAD_POR_EJE.get(f["axis"]):
            errores.append(f"{f['cell_id']}: unit {f['unit']!r} para eje {f['axis']}")
        if f["outcome"] != "horas_cuidado":
            errores.append(f"{f['cell_id']}: outcome {f['outcome']!r}")
        if not f["cell_id"].startswith("EXCLUSION-PISOS-ENUT2019-"):
            errores.append(f"{f['cell_id']}: una fila NO-CONSTRUIBLE no lleva id de RESULT")
        if (f["source_instrument"], f["source_edition"], f["target_edition"]) != ("ENUT", "2019", "2024"):
            errores.append(f"{f['cell_id']}: olas {f['source_edition']}->{f['target_edition']}")
    if (ROOT / "data/corrida0/CALC-PISOS-ENUT2019-EJES-0001").exists():
        errores.append("existe data/corrida0/CALC-PISOS-ENUT2019-EJES-0001 y el dictamen es NO-CONSTRUIBLE")

    # 3 · sidecar y fuente del dictamen, byte a byte
    if not SIDECAR.exists():
        errores.append("falta el sidecar .sha256")
    else:
        esperado = SIDECAR.read_text(encoding="utf-8").split()[0]
        real = hashlib.sha256(TABLA.read_bytes()).hexdigest()
        if esperado != real:
            errores.append(f"sidecar {esperado[:12]} != tabla {real[:12]}")
    fuentes = {(f["metadata_source"], f["metadata_source_sha256"]) for f in filas}
    for ruta, sha in fuentes:
        p = ROOT / ruta
        if not p.exists():
            errores.append(f"metadata_source ausente: {ruta}")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != sha:
            errores.append(f"metadata_source_sha256 no coincide con {ruta}")

    # 4 · el marcador transporta la causa: las 11 celdas salen SIN-PISO con
    #     `NO-CONSTRUIBLE:<causa de la tabla>`, ni una con piso.
    spec = importlib.util.spec_from_file_location(
        "marcador_para_enut2019", ROOT / "tools" / "marcador_segmento.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    marg = [f for f in mod.deriva()["filas"]
            if f["tipo"] == "MARGINAL" and f["regla_o_eje_origen"] == CONSUMER]
    if len(marg) != 11:
        errores.append(f"el marcador trae {len(marg)} filas para {CONSUMER}, esperaba 11")
    causa = next(iter(causas)) if causas else ""
    for f in marg:
        if f["estado"] != "SIN-PISO" or f["piso_fuente"] != f"NO-CONSTRUIBLE:{causa}":
            errores.append(f"{f['celda_id']}: estado={f['estado']} piso_fuente={f['piso_fuente'][:50]!r}")
        if f["piso"] not in ("", None):
            errores.append(f"{f['celda_id']}: trae piso={f['piso']!r} con dictamen NO-CONSTRUIBLE")
    return errores


def main() -> int:
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print("PASA -- tests/test_pisos_enut2019.py (rejilla emitida == rejilla del árbitro; 11 NO-CONSTRUIBLE)")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
