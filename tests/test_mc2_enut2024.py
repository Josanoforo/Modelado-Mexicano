#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENUT 2024 · prueba sintética del COMMIT-1.

Fabrica un zip con la forma de enut2024_bd_csv (tmodulo.csv y tvar_crea.csv unidos por LLAVEMOD), corre
`medir()` y exige `corrida0._valida_outputs(spec, out) == []`, respuestas conocidas (proporción de mujeres
entre cuidadores de dependientes, proporción de horas TNR de mujeres, diferencia de trabajo comunitario) y
el camino degenerado (sin rurales -> None).
Uso: python3 tests/test_mc2_enut2024.py [--emite-ids]
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-MC2-ENUT2024-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_mc2_enut2024", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _csv(cols, rows):
    return ("\r\n".join([",".join(f'"{c}"' for c in cols)] + [",".join(str(r.get(c, "")) for c in cols) for r in rows])
            + "\r\n").encode()


def _fabrica(tmp, med, n=800, sin_rural=False):
    M, V = [], []
    for i in range(n):
        sexo = 1 + i % 2
        k = f"{i:010d}"
        M.append({"LLAVEMOD": k, "SEXO": sexo, "EDAD_V": 12 + i % 80, "TLOC": 1 if sin_rural else 1 + i % 4,
                  "EST_DIS": f"{1 + i % 8:03d}", "UPM_DIS": f"{1 + i % 40:05d}", "FAC_PER": 100,
                  "P6_17_3": ("1" if (sexo == 2 or i % 4 == 0) else "2")})
        # dependientes: 3 de cada 4 cuidadores son mujeres; TNR: mujeres 30 h, hombres 10 h -> 0.75
        dep = 5.0 if (sexo == 2 and i % 4 != 1) or (sexo == 1 and i % 12 == 0) else 0.0
        V.append({"LLAVEMOD": k, "TRAB_NO_REM_VOL": 30.0 if sexo == 2 else 10.0, "TRAB_NO_REM_CON_CP": 2.0 * (i % 3),
                  "CUID_ESP_INT_HOG_CON_CP": dep, "CUID_INT_60MAS_CON_CP": 0.0, "ESCOLARIDAD": 1 + i % 5})
    z = tmp / "enut.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("tmodulo.csv", _csv(med.COLS_M + ["OTRA"], M))
        zf.writestr("tvar_crea.csv", _csv(med.COLS_V, V))
    return z


def corre(sin_rural=False, reps=40):
    med = _load()
    with tempfile.TemporaryDirectory() as t:
        z = _fabrica(Path(t), med, sin_rural=sin_rural)
        return med.medir({med.PAYLOAD: {"ruta_absoluta": str(z)}},
                         {"parametros": {"bootstrap_replicas": reps}, "seed": {"valor": 42}})


def test_conducto():
    import corrida0
    med = _load()
    spec = yaml.safe_load((CALC / "spec.yaml").read_text())
    out = corre()
    assert corrida0._valida_outputs(spec, out) == [], corrida0._valida_outputs(spec, out)[:5]
    P = med.PFX
    assert abs(out[f"{P}-TNR-PROPORCION-HORAS-MUJERES-P"] - 0.75) < 1e-9
    assert abs(out[f"{P}-CUIDADOR-DEP-MUJER-PROP-P"] - 200 / 267) < 1e-9     # 200 mujeres, 67 hombres
    assert abs(out[f"{P}-COMUN-PART-DIF-MUJER-HOMBRE-P"] - 0.5) < 0.03
    out2 = corre(sin_rural=True)
    assert out2[f"{P}-HOMBRES-CUID-PART-RURAL-P"] is None
    assert corrida0._valida_outputs(spec, out2) == []


if __name__ == "__main__":
    if "--emite-ids" in sys.argv:
        out = corre()
        for k in out:
            print(k, "entero" if isinstance(out[k], int) else "flotante")
    else:
        test_conducto()
        print("OK test_mc2_enut2024")
