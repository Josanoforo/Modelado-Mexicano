#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENIGH 2022 · prueba sintética del COMMIT-1.

Fabrica un zip con la forma de enigh2022_nc_csv (concentradohogar en su ruta
`…/conjunto_de_datos/…`), corre `medir()` y exige `corrida0._valida_outputs(spec,
out) == []`, respuestas conocidas (razones regionales, Gini de dos niveles de
ingreso = 0.25 con pesos iguales, Gini de ingreso constante = 0, deciles) y el
camino degenerado (sin Nuevo León -> None).
Uso: python3 tests/test_mc2_enigh2022.py [--emite-ids]
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import zipfile
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-MC2-ENIGH2022-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_mc2_enigh2022", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fabrica(tmp, med, n=1000, sin_nl=False):
    cols = med.COLS + ["tot_integ"]
    lines = [",".join(cols)]
    for i in range(n):
        ent = ["09", "07", "07" if sin_nl else "19", "15"][i % 4]
        ing = 30000.0 if i % 2 else 10000.0          # dos niveles, mitad y mitad -> Gini 0.25
        r = {"folioviv": f"{i:010d}", "foliohog": "1", "ubica_geo": f"{ent}001", "est_dis": f"{1 + i % 8:03d}",
             "upm": f"{1 + i % 40:07d}", "factor": "100", "ing_cor": ing, "transfer": ing,   # sin transfer: 0
             "gasto_mon": 3000.0 * (2 if ent == "09" else 1), "alimentos": ing / 2, "tot_integ": 3}
        lines.append(",".join(str(r[c]) for c in cols))
    z = tmp / "enigh.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/"
                    "conjunto_de_datos_concentradohogar_enigh2022_ns.csv", ("\r\n".join(lines) + "\r\n").encode())
    return z


def corre(sin_nl=False, reps=40):
    med = _load()
    with tempfile.TemporaryDirectory() as t:
        z = _fabrica(Path(t), med, sin_nl=sin_nl)
        return med.medir({med.PAYLOAD: {"ruta_absoluta": str(z)}},
                         {"parametros": {"bootstrap_replicas": reps}, "seed": {"valor": 42}})


def test_conducto():
    import corrida0
    med = _load()
    spec = yaml.safe_load((CALC / "spec.yaml").read_text())
    out = corre()
    assert corrida0._valida_outputs(spec, out) == [], corrida0._valida_outputs(spec, out)[:5]
    P = med.PFX
    assert abs(out[f"{P}-GASTO-RAZON-CDMX-CHIAPAS-P"] - 2.0) < 1e-9
    assert abs(out[f"{P}-GINI-CON-TRANSFERENCIAS-P"] - 0.25) < 0.01
    assert abs(out[f"{P}-D1-ALIMENTOS-SOBRE-INGRESO-P"] - 0.5) < 1e-9
    assert abs(out[f"{P}-D1-TRANSFER-SOBRE-INGRESO-P"] - 1.0) < 1e-9
    assert abs(out[f"{P}-D10-PARTICIPACION-INGRESO-P"] - 0.15) < 1e-9     # 10 % de hogares con 30 000 de 20 000 medios
    assert out[f"{P}-GINI-SIN-TRANSFERENCIAS-P"] is None      # ingreso sin transferencias = 0: no estimable
    out2 = corre(sin_nl=True)
    assert out2[f"{P}-ING-COR-TRIM-NUEVO-LEON-P"] is None
    assert corrida0._valida_outputs(spec, out2) == []


if __name__ == "__main__":
    if "--emite-ids" in sys.argv:
        out = corre()
        for k in out:
            print(k, "entero" if isinstance(out[k], int) else "flotante")
    else:
        test_conducto()
        print("OK test_mc2_enigh2022")
