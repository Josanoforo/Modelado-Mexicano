#!/usr/bin/env python3
"""Falsadores de la tabla de identidad ENIF 2021 × formalidad
(ACTO GEN2-PISOS-ENIF2021-FORMALIDAD-1).

La rejilla que este acto EMITE (`forense/prereg-caja/PISOS-ENIF2021-
formalidad-metadatos-v1_0.tsv`) debe coincidir uno a uno con la rejilla del
ÁRBITRO (`milpa/tramite-ola5-propuesta-v0.yaml`): eje `formalidad` de los
dos desenlaces de `dinero.ahorro.via_informal_ejes_enif2024` y de
`dinero.ahorro.horizonte_corto_ejes_enif2024`, categorías leídas del yaml
(no tecleadas), una fila por celda, ni una más. Como el dictamen P0 fue
CONSTRUIBLE, además se prueba que cada `cell_id` es un RESULT sellado en
`CALC-PISOS-ENIF2021-FORMALIDAD-0001` con punto, IC y n.

No abre microdatos. Corre standalone
(`python3 tests/test_pisos_enif2021_formalidad.py`) y expone `corre()` con
el mismo arnés que `tests/test_pisos_enut2019.py`.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TABLA = ROOT / "forense/prereg-caja/PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv"
SIDECAR = Path(str(TABLA) + ".sha256")
YAML_ARBITRO = ROOT / "milpa/tramite-ola5-propuesta-v0.yaml"
CALC = ROOT / "data/corrida0/CALC-PISOS-ENIF2021-FORMALIDAD-0001"
# (outcome de la tabla) -> (id de regla del árbitro, bloque `desenlaces` o None)
REGLAS = {
    "ahorra_solo_informal": ("dinero.ahorro.via_informal_ejes_enif2024", "ahorra_solo_informal"),
    "informal_cualquiera": ("dinero.ahorro.via_informal_ejes_enif2024", "informal_cualquiera"),
    "horizonte_corto": ("dinero.ahorro.horizonte_corto_ejes_enif2024", None),
}


def _tabla() -> list[dict]:
    with TABLA.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader((l for l in fh if not l.startswith("#")),
                                   delimiter="\t"))


def _celdas_arbitro() -> list[tuple[str, str, str]]:
    d = yaml.safe_load(YAML_ARBITRO.read_text(encoding="utf-8"))
    reglas = {r["id"]: r for r in d["reglas_propuestas"]}
    out = []
    for outcome, (rid, bloque) in REGLAS.items():
        r = reglas[rid]
        ejes = r["ejes"] if bloque is None else next(
            v["ejes"] for v in r["desenlaces"].values() if v.get("nombre") == bloque)
        eje = next(e for e in ejes if e["eje"] == "formalidad")
        out += [(outcome, "formalidad", c["celda"]) for c in eje["celdas"]]
    return out


def corre() -> list[str]:
    errores: list[str] = []
    if not TABLA.exists():
        return [f"no existe `{TABLA.relative_to(ROOT)}`"]
    filas = _tabla()
    arbitro = _celdas_arbitro()

    # 1 · rejilla emitida == rejilla del árbitro (desenlace, eje, categoría)
    emitida = [(f["outcome"], f["axis"], f["category"]) for f in filas]
    if sorted(emitida) != sorted(arbitro):
        errores.append(f"rejilla emitida {sorted(emitida)} != árbitro {sorted(arbitro)}")
    if len(set(f["cell_id"] for f in filas)) != len(filas):
        errores.append("cell_id duplicado en la tabla")
    if len(filas) != 6:
        errores.append(f"{len(filas)} filas, esperaba 6 (3 desenlaces × 2 categorías)")

    # 2 · dictamen CONSTRUIBLE: cada cell_id es un RESULT -P sellado con IC y n
    res = {}
    rj = CALC / "resultados.json"
    if rj.exists():
        res = json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
    else:
        errores.append(f"falta {rj.relative_to(ROOT)}")
    for f in filas:
        if f["status"] != "CONSTRUIBLE" or f["reason"]:
            errores.append(f"{f['cell_id']}: status={f['status']!r} reason={f['reason']!r}")
        if not f["cell_id"].endswith("-P"):
            errores.append(f"{f['cell_id']}: una fila CONSTRUIBLE lleva el id del RESULT -P")
        base = f["cell_id"][:-2]
        for s in ("P", "IC-LO", "IC-HI", "N", "DEN-W"):
            if f"{base}-{s}" not in res:
                errores.append(f"{base}-{s}: no está sellado en el CALC")
        if f["unit"] != "PERSONA ELEGIDA 18+":
            errores.append(f"{f['cell_id']}: unit {f['unit']!r}")
        if (f["source_instrument"], f["source_edition"], f["target_edition"]) != ("ENIF", "2021", "2024"):
            errores.append(f"{f['cell_id']}: olas {f['source_edition']}->{f['target_edition']}")

    # 3 · sidecar y fuente del dictamen, byte a byte
    if not SIDECAR.exists():
        errores.append("falta el sidecar .sha256")
    else:
        esperado = SIDECAR.read_text(encoding="utf-8").split()[0]
        real = hashlib.sha256(TABLA.read_bytes()).hexdigest()
        if esperado != real:
            errores.append(f"sidecar {esperado[:12]} != tabla {real[:12]}")
    for ruta, sha in {(f["metadata_source"], f["metadata_source_sha256"]) for f in filas}:
        p = ROOT / ruta
        if not p.exists():
            errores.append(f"metadata_source ausente: {ruta}")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != sha:
            errores.append(f"metadata_source_sha256 no coincide con {ruta}")
    return errores


def main() -> int:
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print("PASA -- tests/test_pisos_enif2021_formalidad.py (rejilla emitida == rejilla del árbitro; 6 CONSTRUIBLE selladas)")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
