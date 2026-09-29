#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENOE · prueba sintética del COMMIT-1.

Fabrica dos zips con la forma de ENOE_SDEMT (CSV con fin de línea \\r\\n y cabecera en
minúsculas), corre `medir()` y exige `corrida0._valida_outputs(spec, out) == []`,
respuestas conocidas (participación, brecha de ingreso 1 − M/H, estado conyugal),
el filtro de universo (r_def/c_res/edad) y el camino degenerado (sin jóvenes -> None).
Uso: python3 tests/test_mc2_enoe.py [--emite-ids]
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-MC2-ENOE-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_mc2_enoe", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _csv(cols, rows):
    out = [",".join(cols)] + [",".join(str(r.get(c, "")) for c in cols) for r in rows]
    return ("\r\n".join(out) + "\r\n").encode("latin-1")


def _fabrica(tmp, med, n=800, sin_jovenes=False):
    cols = ["cd_a", "ent"] + med.COLS
    r25, r23 = [], []
    for i in range(n):
        sexo = 1 + i % 2
        base = {"r_def": "00" if i % 97 else "15", "c_res": "1", "sex": sexo, "fac_tri": 100,
                "est_d_tri": f"{1 + i % 8:04d}", "upm": f"{1 + i % 40:07d}"}
        eda = (30 + i % 40) if sin_jovenes else (15 + i % 60)
        # hombres: PEA 3/4; mujeres: PEA 1/2; ingreso H 10 000, M 8 000 -> brecha 0.2
        pea = (i // 2) % 4 < (3 if sexo == 1 else 2)
        r25.append({**base, "eda": eda, "e_con": 6, "clase1": 1 if pea else 2, "clase2": 1 if pea else 4,
                    "ingocup": (10000 if sexo == 1 else 8000) if pea else 0, "emp_ppal": 1})
        r23.append({**base, "eda": eda, "e_con": (1, 5, 6, 3)[i % 4] if i % 50 else 9, "clase1": 1,
                    "clase2": 1, "ingocup": 1, "emp_ppal": 1})
    z25, z23 = tmp / "e25.zip", tmp / "e23.zip"
    with zipfile.ZipFile(z25, "w") as z:
        z.writestr("ENOE_SDEMT425.csv", _csv(cols, r25))
        z.writestr("ENOE_COE1T425.csv", b"x\r\n")
    with zipfile.ZipFile(z23, "w") as z:
        z.writestr("ENOE_SDEMT323.csv", _csv(cols, r23))
    return z25, z23


def corre(sin_jovenes=False, reps=60):
    med = _load()
    with tempfile.TemporaryDirectory() as t:
        z25, z23 = _fabrica(Path(t), med, sin_jovenes=sin_jovenes)
        return med.medir({med.P25: {"ruta_absoluta": str(z25)}, med.P23: {"ruta_absoluta": str(z23)}},
                         {"parametros": {"bootstrap_replicas": reps}, "seed": {"valor": 42}})


def test_conducto():
    import corrida0
    med = _load()
    spec = yaml.safe_load((CALC / "spec.yaml").read_text())
    out = corre()
    assert corrida0._valida_outputs(spec, out) == [], corrida0._valida_outputs(spec, out)[:5]
    P = med.PFX
    assert abs(out[f"{P}-2025T4-PARTICIPA-HOMBRE-P"] - 0.75) < 0.02
    assert abs(out[f"{P}-2025T4-PARTICIPA-MUJER-P"] - 0.50) < 0.02
    assert abs(out[f"{P}-2025T4-INGRESO-BRECHA-MUJER-HOMBRE-P"] - 0.20) < 1e-9
    assert out[f"{P}-DIAG-2025T4-UNIVERSO-15-98"] == 800 - len(range(0, 800, 97))
    assert abs(out[f"{P}-2023T3-ECON-UNION-LIBRE-15MAS-P"] - 0.25) < 0.02
    out2 = corre(sin_jovenes=True)
    assert out2[f"{P}-2023T3-ECON-CASADO-15-29-P"] is None
    assert corrida0._valida_outputs(spec, out2) == []


if __name__ == "__main__":
    if "--emite-ids" in sys.argv:
        out = corre()
        for k in out:
            print(k, "entero" if isinstance(out[k], int) else "flotante")
    else:
        test_conducto()
        print("OK test_mc2_enoe")
