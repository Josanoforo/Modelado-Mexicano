#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENSANUT 2024 · prueba sintética del COMMIT-1.

Fabrica dos zips con un .dta cada uno (integrantes y adultos, nombres de
columna con la capitalización real: H0405A-C en mayúsculas), corre `medir()` y
exige `corrida0._valida_outputs(spec, out) == []`, respuestas conocidas (rural
busca 1/2 vs metro 3/4; acceso entre quien no buscó; suspensión por pago) y el
camino degenerado (sin necesidades de salud mental -> None).
Uso: python3 tests/test_mc2_ensanut2024.py [--emite-ids]
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[1]
CALC = RAIZ / "data/corrida0/CALC-MC2-ENSANUT2024-0001"
sys.path.insert(0, str(RAIZ / "tools"))


def _load():
    spec = importlib.util.spec_from_file_location("med_mc2_ensanut2024", CALC / "medidor.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _zip_dta(ruta: Path, nombre: str, df: pd.DataFrame):
    import pyreadstat
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / nombre
        pyreadstat.write_dta(df, str(p))
        with zipfile.ZipFile(ruta, "w") as zf:
            zf.write(p, nombre)


def _fabrica(tmp: Path, n=1200, sin_mental=False):
    i = np.arange(n)
    estrato = 1 + i % 3                                     # 1 rural, 2 urbano, 3 metro
    nec = np.where(i % 2 == 0, 1, 2)
    # búsqueda: rural 1/2, urbano y metro 3/4 (entre quienes tienen necesidad)
    k = i // 6
    busco = np.where(estrato == 1, np.where(k % 2 == 0, 1, 2), np.where(k % 4 < 3, 1, 2))
    busco = np.where(nec == 1, busco, np.nan)
    m1 = np.where((nec == 1) & (busco == 2), np.where(estrato == 1, 3, 1), np.nan)   # rural: lejos; otros: no grave
    m1 = np.where((nec == 1) & (busco == 2) & (i % 50 == 0), 99, m1)
    inte = pd.DataFrame({
        "FOLIO_I": i.astype(str), "ponde_f": 100.0 + i % 3, "est_sel": (i % 10).astype(str),
        "upm": (i % 60).astype(str), "estrato": estrato.astype(float), "h0302": 1.0 + i % 2,
        "h0303": (i % 90).astype(float), "h0401": nec.astype(float),
        "h0402": np.where(nec == 1, np.where((i % 5 == 0) & (not sin_mental), 47, 1), np.nan).astype(float),
        "h0404": busco, "H0405A": m1, "H0405B": np.nan, "H0405C": np.nan, "otra": 1.0})
    paga = np.where(i % 2 == 0, 150.0, 0.0)
    susp = np.where(paga > 0, np.where(i % 4 == 0, 1, 2), np.where(i % 8 == 1, 1, 2))
    adul = pd.DataFrame({
        "FOLIO_I": i.astype(str), "ponde_f": 50.0, "est_sel": (i % 10).astype(str), "upm": (i % 60).astype(str),
        "estrato": estrato.astype(float), "sexo": 1.0 + i % 2, "edad": 20.0 + i % 60,
        "a0301": np.where(i % 3 == 0, 3.0, 1.0), "a0307": 2.0, "a0310a": np.where(i % 97 == 0, 999999.0, paga),
        "a0313": susp.astype(float), "a0314": np.where(susp == 1, np.where(i % 3 == 0, 7.0, 1.0), np.nan)})
    z1, z2 = tmp / "inte.zip", tmp / "adul.zip"
    _zip_dta(z1, "integrantes_ensanut2024_w_icb.dta", inte)
    _zip_dta(z2, "adultos_ensanut2024_w.dta", adul)
    return z1, z2


def corre(sin_mental=False, reps=60):
    med = _load()
    with tempfile.TemporaryDirectory() as t:
        z1, z2 = _fabrica(Path(t), sin_mental=sin_mental)
        inputs = {med.P_INTE: {"ruta_absoluta": str(z1)}, med.P_ADUL: {"ruta_absoluta": str(z2)}}
        contrato = {"parametros": {"bootstrap_replicas": reps}, "seed": {"valor": 42}}
        return med.medir(inputs, contrato)


def test_conducto():
    import corrida0
    med = _load()
    spec = yaml.safe_load((CALC / "spec.yaml").read_text())
    out = corre()
    assert corrida0._valida_outputs(spec, out) == [], corrida0._valida_outputs(spec, out)[:5]
    P = med.PFX
    assert abs(out[f"{P}-BUSCO-RURAL-P"] - 0.5) < 0.03, out[f"{P}-BUSCO-RURAL-P"]
    assert abs(out[f"{P}-BUSCO-METRO-P"] - 0.75) < 0.03, out[f"{P}-BUSCO-METRO-P"]
    assert out[f"{P}-BUSCO-DIF-RURAL-METRO-P"] < 0
    # entre quienes no buscaron con motivo válido: rural = acceso (lejos), metro = no grave
    assert out[f"{P}-ACCESO-RURAL-P"] == 1.0 and out[f"{P}-ACCESO-METRO-P"] == 0.0
    assert out[f"{P}-NO-GRAVE-METRO-P"] == 1.0
    assert out[f"{P}-DIAG-INTE-NO-BUSCO-SIN-MOTIVO-VALIDO"] > 0
    # suspensión: paga 1/2, no paga 1/4 -> diferencia +1/4; causa 7 (sin dinero) = econ-acceso
    assert out[f"{P}-DM-SUSPENDE-DIF-PAGA-NOPAGA-P"] > 0.15
    assert out[f"{P}-DIAG-ADUL-MONTO-FUERA"] > 0
    out2 = corre(sin_mental=True)
    assert out2[f"{P}-BUSCO-MENTAL-NAC-P"] is None
    assert corrida0._valida_outputs(spec, out2) == []


if __name__ == "__main__":
    if "--emite-ids" in sys.argv:
        out = corre()
        for k in out:
            print(k, "entero" if isinstance(out[k], int) else "flotante")
    else:
        test_conducto()
        print("OK test_mc2_ensanut2024")
