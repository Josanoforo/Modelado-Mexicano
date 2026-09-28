#!/usr/bin/env python3
"""GEN2-PISOS-DOMINIOS-Y-REGLAS-1 · pieza P-ENUT2024 · prueba sintética del COMMIT-1.

Fabrica zips con la forma de enut2024_bd_csv.zip (tmodulo.csv, tvar_crea.csv;
cabecera entrecomillada, CRLF, sin BOM) y enut2019_bd_csv.zip
(enut_2019/TMODULO.csv, latin-1, CRLF), corre `medir()` y exige
`corrida0._valida_outputs(spec, out) == []`, ids exactos, ningún str > 1024
bytes, una respuesta conocida y el camino degenerado (celda vacía -> None).
Uso: python3 tests/test_pdr1_enut2024.py [--emite-ids]
"""
from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-PDR1-ENUT2024-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_pdr1_enut2024", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _csv(cols, rows, enc="utf-8"):
    lines = [",".join(f'"{c}"' for c in cols)]
    for r in rows:
        lines.append(",".join(str(r.get(c, "")) for c in cols))
    return ("\r\n".join(lines) + "\r\n").encode(enc)


def _fabrica(tmp: Path, med, n=600, seed=7, sin_rural=False):
    rng = np.random.default_rng(seed)
    m_cols = med.COLS_M24 + ["NIV", "OTRA"]
    v_cols = med.COLS_V24 + ["EDAD", "SEXO"]
    mr, vr, r19 = [], [], []
    for i in range(n):
        llave = f"{i:012d}"
        sexo = str(1 + i % 2)
        tloc = "1" if sin_rural else str(1 + i % 4)
        est = f"{1 + i % 6:04d}"
        upm = f"{1 + i % 30:05d}"
        r = {"LLAVEMOD": llave, "SEXO": sexo, "EDAD_V": str(12 + i % 80), "P4_1": str(1 + (i % 5 > 0)),
             "TLOC": tloc, "EST_DIS": est, "UPM_DIS": upm, "FAC_PER": str(100 + i % 7),
             "P6_17_3": "1" if i % 3 == 0 else ("2" if i % 17 else "9")}
        for k in (1, 2, 3, 4):
            r[f"P6_17A_3_{k}"] = f"{k:02d}" if r["P6_17_3"] == "1" else ""
        for blq, items in (("21", med.CONV_ITEMS), ("22", med.MED_ITEMS)):
            for it in items:
                si = rng.random() < 0.6
                r[f"P6_{blq}_{it}"] = "1" if si else "2"
                for k in (1, 2, 3, 4):
                    r[f"P6_{blq}A_{it}_{k}"] = f"{int(rng.integers(0, 10)):02d}" if si else ""
        mr.append(r)
        tnr = "" if i % 53 == 0 else f"{(30.0 if sexo == '2' else 10.0) * (i % 4 > 0):021.17f}"
        vr.append({"LLAVEMOD": llave, "TRAB_NO_REM_VOL": tnr,
                   "TRAB_NO_REM_CON_CP": f"{float(i % 3):021.17f}",
                   "ACTIV_PROD_CON_CP": f"{float(40 + i % 20):021.17f}",
                   "MENOR10": "1" if tloc in ("3", "4") else "", "COND_IND": str(1 + i % 3 % 2) if i % 11 else "9"})
        r19.append({"UPM": str(i), "SEXO": sexo, "EDAD_V": "30", "P4_1": r["P4_1"], "P6_17_2": r["P6_17_3"],
                    "TLOC": tloc, "EST_DIS": est[1:], "UPM_DIS": f"{int(upm):07d}", "FAC_PER": "50"})
    z24, z19 = tmp / "enut2024.zip", tmp / "enut2019.zip"
    with zipfile.ZipFile(z24, "w") as z:
        z.writestr("tmodulo.csv", _csv(m_cols, mr))
        z.writestr("tvar_crea.csv", _csv(v_cols, vr))
        z.writestr("tsdem.csv", _csv(["LLAVESDE"], []))
    with zipfile.ZipFile(z19, "w") as z:
        z.writestr("enut_2019/", b"")
        z.writestr("enut_2019/TMODULO.csv", _csv(["UPM"] + med.COLS_M19, r19, "latin-1"))
        z.writestr("enut_2019_indigena/TMODULO.csv", _csv(["UPM"] + med.COLS_M19, r19[:5], "latin-1"))
    return z24, z19


def corre(sin_rural=False, reps=60):
    med = _load()
    with tempfile.TemporaryDirectory() as t:
        z24, z19 = _fabrica(Path(t), med, sin_rural=sin_rural)
        inputs = {med.P24: {"ruta_absoluta": str(z24)}, med.P19: {"ruta_absoluta": str(z19)}}
        contrato = {"parametros": {"bootstrap_replicas": reps}, "seed": {"valor": 42}}
        return med.medir(inputs, contrato)


def test_conducto():
    import corrida0
    spec = yaml.safe_load((CALC / "spec.yaml").read_text())
    out = corre()
    assert corrida0._valida_outputs(spec, out) == [], corrida0._valida_outputs(spec, out)[:5]
    assert all(len(v.encode()) <= 1024 for v in out.values() if isinstance(v, str))
    # respuesta conocida: TNR mujer = 30 entre participantes, hombre = 10 -> brecha 20
    P = "RESULT-PDR1-ENUT2024"
    assert abs(out[f"{P}-TNR-INT-MUJER-P"] - 30.0) < 1e-9
    assert abs(out[f"{P}-TNR-INT-HOMBRE-P"] - 10.0) < 1e-9
    assert abs(out[f"{P}-TNR-INT-BRECHA-SEXO-P"] - 20.0) < 1e-9
    assert out[f"{P}-DIAG-TNR-INVALIDOS"] == len(range(0, 600, 53))
    # degenerado: sin rurales -> celda rural None y válido
    out2 = corre(sin_rural=True)
    assert out2[f"{P}-COMUN-PART-RURAL-P"] is None
    assert corrida0._valida_outputs(spec, out2) == []


if __name__ == "__main__":
    if "--emite-ids" in sys.argv:
        out = corre()
        for k in out:
            tipo = "entero" if isinstance(out[k], int) else "flotante"
            print(k, tipo)
    else:
        test_conducto()
        print("OK test_pdr1_enut2024")
