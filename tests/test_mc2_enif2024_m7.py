#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENIF 2024 m7 (cuatro columnas abiertas) · prueba sintética del COMMIT-1.

Fabrica un zip con la forma de enif_2024_bd_csv.zip (TMODULO.csv con cabecera
entrecomillada, CRLF, códigos con cero a la izquierda y columnas P7_* que el
medidor NO debe leer), corre `medir()` y exige
`corrida0._valida_outputs(spec, out) == []`, ids exactos, una respuesta
conocida, la guardia del módulo 7 y el camino degenerado (celda vacía -> None).
Uso: python3 tests/test_mc2_enif2024_m7.py [--emite-ids]
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-MC2-ENIF2024-M7-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_mc2_enif2024_m7", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _csv(cols, rows):
    lines = [",".join(f'"{c}"' for c in cols)]
    for r in rows:
        lines.append(",".join(str(r.get(c, "")) for c in cols))
    return ("\r\n".join(lines) + "\r\n").encode("utf-8")


def _fabrica(tmp: Path, med, n=720, sin_region6=False):
    cols = ["LLAVEMOD"] + med.COLS + ["P7_4_1", "P7_9_1_3"]
    rows = []
    for i in range(n):
        conoce = "1" if i % 2 == 0 else "2"
        rows.append({"LLAVEMOD": f"{i:08d}", "EDAD_V": str(18 + i % 80), "NIV": f"{i % 12:02d}",
                     "SEXO": str(1 + i % 2), "TLOC": str(1 + i % 4),
                     "REGION": ("1" if sin_region6 and i % 6 == 5 else str(1 + i % 6)),
                     "EST_DIS": f"{1 + i % 8:03d}", "UPM_DIS": f"{1 + i % 40:05d}", "FAC_PER": "100",
                     "P7_1_1": "3" if i % 4 else "1", "P7_1_2": "2" if i % 3 else "9",
                     "P7_2_1": conoce, "P7_3_1": ("1" if i % 4 == 0 else "2") if conoce == "1" else "b",
                     "P7_4_1": "1", "P7_9_1_3": "1"})
    z = tmp / "enif2024.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("TMODULO.csv", _csv(cols, rows))
    return z


def corre(sin_region6=False, reps=60):
    med = _load()
    with tempfile.TemporaryDirectory() as t:
        z = _fabrica(Path(t), med, sin_region6=sin_region6)
        return med.medir({med.PAYLOAD: {"ruta_absoluta": str(z)}},
                         {"parametros": {"bootstrap_replicas": reps}, "seed": {"valor": 42}})


def test_conducto():
    import corrida0
    med = _load()
    spec = yaml.safe_load((CALC / "spec.yaml").read_text())
    out = corre()
    assert corrida0._valida_outputs(spec, out) == [], corrida0._valida_outputs(spec, out)[:5]
    P = med.PFX
    assert abs(out[f"{P}-EFECTIVO-500-O-MENOS-NAC-P"] - 0.75) < 1e-9
    assert abs(out[f"{P}-CODI-CONOCE-NAC-P"] - 0.5) < 1e-9
    assert abs(out[f"{P}-CODI-USA-SI-CONOCE-NAC-P"] - 0.5) < 1e-9
    assert abs(out[f"{P}-CODI-USA-POBLACION-NAC-P"] - 0.25) < 1e-9
    assert out[f"{P}-DIAG-P7_1_2-FUERA-1-3"] == 240
    for mala in (["P7_4_1"], ["P7_9_1_3"]):
        try:
            med._lee("no-importa.zip", mala)
            raise AssertionError("guardia m7 no se disparó")
        except med.ReservaRota:
            pass
    out2 = corre(sin_region6=True)
    assert out2[f"{P}-CODI-CONOCE-REGION-6-P"] is None
    assert corrida0._valida_outputs(spec, out2) == []

if __name__ == "__main__":
    if "--emite-ids" in sys.argv:
        out = corre()
        for k in out:
            print(k, "entero" if isinstance(out[k], int) else "flotante")
    else:
        test_conducto()
        print("OK test_mc2_enif2024_m7")
