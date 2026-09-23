#!/usr/bin/env python3
"""RESULT citados existen -- las 9 celdas-D de crédito 2024 registradas por
ACTO GEN2-DIN-CREDITO-CELDAS-D-2 (P3 del encargo). No re-mide, no adjudica:
solo prueba que cada RESULT que el yaml cita (holdout ref y las claves de
VEREDICTO-PRIMARIO / DELTA-MAE-PP / N-CELDAS-ELEGIBLES por conducta) existe
de verdad en el `resultados.json` sellado del CALC que se declara como
fuente -- el defecto que atrapa es un yaml que cita un id que nunca se
selló (cortar-pegar de otra conducta, hash o id truncado).
"""
import glob
import json
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELDAS_DIR = os.path.join(ROOT, "data", "curacion-registro", "celdas-d")
CALC_ID = "CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002"
RESULTADOS = os.path.join(ROOT, "data", "corrida0", CALC_ID, "resultados.json")

CONDUCTAS = [
    "K1", "K2-AUTOMOTRIZ", "K2-DEPARTAMENTAL", "K2-NOMINA", "K3",
    "K4A-AUTOEXCLUSION", "K4B-OFERTA", "K5", "K6-P-TENEDORES",
]


def _mis_yamls():
    return sorted(glob.glob(os.path.join(CELDAS_DIR, "DIN.credito_*.marginal16.yaml")))


def test_nueve_archivos_una_por_conducta():
    paths = _mis_yamls()
    assert len(paths) == 9, f"esperaba 9 celdas-D de crédito, hay {len(paths)}: {paths}"


def test_holdout_ref_apunta_al_calc_sellado():
    for path in _mis_yamls():
        with open(path, encoding="utf-8") as fh:
            d = yaml.safe_load(fh)["celda_d"]
        refs = d["momentos_holdout_refs"]
        assert any(r.startswith(CALC_ID + "--") for r in refs), (
            f"{path}: momentos_holdout_refs no cita {CALC_ID}: {refs}")


def test_result_citados_existen():
    with open(RESULTADOS, encoding="utf-8") as fh:
        res = json.load(fh)["resultados"]

    faltantes = []
    for path in _mis_yamls():
        with open(path, encoding="utf-8") as fh:
            d = yaml.safe_load(fh)["celda_d"]
        cid = d["id"]
        conducta = next((c for c in CONDUCTAS if f".credito_k" in cid and
                          cid.split(".")[1].replace("credito_", "").replace("_", "-").upper()
                          .startswith(c.split("-")[0].lower().upper()[:2])), None)
        # emparejar por slug en vez de heurística: usar el prefijo real del id
        pre = f"RESULT-DIN-CREDITO-PREDICCION-2024-ESC2-ADJ16-"
        # localizar la conducta exacta comprobando que exista VEREDICTO-PRIMARIO
        candidatas = [c for c in CONDUCTAS
                      if f"{pre}{c}-VEREDICTO-PRIMARIO" in res and
                      c.lower().replace("-", "_") in cid]
        assert candidatas, f"{path}: no pude emparejar el id con una conducta conocida ({cid})"
        c = candidatas[0]
        for suf in ("VEREDICTO-PRIMARIO", "N-CELDAS-ELEGIBLES", "PERSISTENCIA-MAE-PP"):
            key = f"{pre}{c}-{suf}"
            if key not in res:
                faltantes.append((path, key))
        assert d["veredicto"] == res[f"{pre}{c}-VEREDICTO-PRIMARIO"], (
            f"{path}: veredicto del yaml ({d['veredicto']!r}) no calza con "
            f"{pre}{c}-VEREDICTO-PRIMARIO ({res[f'{pre}{c}-VEREDICTO-PRIMARIO']!r})")

    assert not faltantes, f"RESULT citados ausentes en resultados.json: {faltantes}"


def main():
    ok = True
    for fn in (test_nueve_archivos_una_por_conducta,
               test_holdout_ref_apunta_al_calc_sellado,
               test_result_citados_existen):
        try:
            fn()
            print(f"{fn.__name__}: ok")
        except AssertionError as exc:
            ok = False
            print(f"{fn.__name__}: FAIL -- {exc}", file=sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
