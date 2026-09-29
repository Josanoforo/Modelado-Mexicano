#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENIF 2024 · prueba sintética del COMMIT-1.

Fabrica un zip con la forma de enif_2024_bd_csv.zip (TMODULO.csv con cabecera
entrecomillada, CRLF, códigos con cero a la izquierda y columnas P7_* que el
medidor NO debe leer), corre `medir()` y exige
`corrida0._valida_outputs(spec, out) == []`, ids exactos, una respuesta
conocida, la guardia del módulo 7 y el camino degenerado (celda vacía -> None).
Uso: python3 tests/test_mc2_enif2024.py [--emite-ids]
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-MC2-ENIF2024-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_mc2_enif2024", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _csv(cols, rows):
    lines = [",".join(f'"{c}"' for c in cols)]
    for r in rows:
        lines.append(",".join(str(r.get(c, "")) for c in cols))
    return ("\r\n".join(lines) + "\r\n").encode("utf-8")


def _fabrica(tmp: Path, med, n=720, sin_region6=False):
    cols = ["LLAVEMOD"] + med.COLS + ["P7_1_1", "P7_3_1"]
    rows = []
    for i in range(n):
        sexo = str(1 + i % 2)
        r = {"LLAVEMOD": f"{i:08d}", "EDAD_V": str(18 + i % 80), "NIV": f"{i % 12:02d}" if i % 41 else "99",
             "SEXO": sexo, "TLOC": str(1 + i % 4),
             "REGION": ("1" if sin_region6 and i % 6 == 5 else str(1 + i % 6)),
             "EST_DIS": f"{1 + i % 8:03d}", "UPM_DIS": f"{1 + i % 40:05d}", "FAC_PER": str(100 + i % 5),
             "P3_13": ("7" if i % 3 == 0 else ("b" if i % 3 == 1 else "1")),
             "P4_6_4": str(1 + i % 3) if i % 29 else "9", "P4_10": str(1 + i % 5) if i % 31 else "8",
             "P5_1_5": "1" if i % 4 == 0 else "2", "P5_13": str(1 + i % 7) if i % 2 else "b",
             "P6_14": str(1 + i % 9) if i % 3 == 0 else "b",
             "P6_17_4": ("1" if i % 10 == 0 else "0") if i % 5 == 0 else "b",
             "P8_1": "1" if i % 5 == 0 else ("9" if i % 37 == 0 else "2"),
             "P9_2": str(1 + i % 9) if i % 4 == 1 else "b",
             "P9_9_1": "1" if i % 3 else "2", "P9_9_5": "1" if i % 2 else "2",
             "P7_1_1": "1", "P7_3_1": "1"}
        # AFORE: mujeres 1 de cada 4, hombres 1 de cada 2 (respuesta conocida)
        r["P9_1"] = "1" if (i // 2) % (4 if sexo == "2" else 2) == 0 else "2"
        r["P9_3"] = ("1" if i % 7 == 0 else "2") if r["P9_1"] == "1" else "b"
        for k in range(1, 10):
            r[f"P5_4_{k}"] = "1" if (k == 4 and i % 3 == 0) else "2"
            r[f"P6_2_{k}"] = "1" if (k == 1 and i % 6 == 0) else "2"
        rows.append(r)
    z = tmp / "enif2024.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("TMODULO.csv", _csv(cols, rows))
        zf.writestr("TSDEM.csv", _csv(["LLAVEHOG"], []))
    return z


def corre(sin_region6=False, reps=60):
    med = _load()
    with tempfile.TemporaryDirectory() as t:
        z = _fabrica(Path(t), med, sin_region6=sin_region6)
        inputs = {med.PAYLOAD: {"ruta_absoluta": str(z)}}
        contrato = {"parametros": {"bootstrap_replicas": reps}, "seed": {"valor": 42}}
        return med.medir(inputs, contrato)


def test_conducto():
    import corrida0
    med = _load()
    spec = yaml.safe_load((CALC / "spec.yaml").read_text())
    out = corre()
    assert corrida0._valida_outputs(spec, out) == [], corrida0._valida_outputs(spec, out)[:5]
    assert not any(isinstance(v, str) for v in out.values())
    P = med.PFX
    # respuesta conocida: AFORE mujer = 1/4, hombre = 1/2 (pesos iguales por paridad)
    assert abs(out[f"{P}-AFORE-MUJER-P"] - 0.25) < 0.02, out[f"{P}-AFORE-MUJER-P"]
    assert abs(out[f"{P}-AFORE-HOMBRE-P"] - 0.50) < 0.02, out[f"{P}-AFORE-HOMBRE-P"]
    assert out[f"{P}-AFORE-BRECHA-MUJER-HOMBRE-P"] < 0
    # 'b' y '9' fuera del denominador; la cuenta de ahorro sale 1/3
    assert abs(out[f"{P}-CTA-AHORRO-NAC-P"] - 1 / 3) < 0.02
    assert out[f"{P}-DIAG-SEGURO-NO-SABE"] == sum(1 for i in range(720) if i % 5 and i % 37 == 0)
    # guardia del módulo 7: pedir una P7_* revienta
    try:
        med._lee("no-importa.zip", ["P7_1_1"])
        raise AssertionError("la guardia del módulo 7 no se disparó")
    except med.ReservaRota:
        pass
    # degenerado: sin región 6 -> celda None y el conducto la acepta
    out2 = corre(sin_region6=True)
    assert out2[f"{P}-CUENTA-REGION-6-P"] is None
    assert corrida0._valida_outputs(spec, out2) == []


if __name__ == "__main__":
    if "--emite-ids" in sys.argv:
        out = corre()
        for k in out:
            print(k, "entero" if isinstance(out[k], int) else "flotante")
    else:
        test_conducto()
        print("OK test_mc2_enif2024")
