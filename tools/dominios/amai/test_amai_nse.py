"""Pruebas del conducto AMAI-NSE sobre sintético y oro (D-22 (2)); no tocan el corpus.

Correr: python3 -m pytest -q tools/dominios/amai/test_amai_nse.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

from tools import corrida0 as C0
from tools.dominios.amai import componentes as C
from tools.dominios.amai import genera_specs as G
from tools.dominios.amai import imputacion as I
from tools.dominios.amai import medidor as M
from tools.dominios.amai import regla as R
from tools.dominios.amai import sintetico as S

ROOT = Path(__file__).resolve().parents[3]


def test_cortes_del_anexo():
    p = pd.Series([0, 1, 47, 48, 94, 95, 115, 116, 140, 141, 167, 168, 201, 202, 300])
    assert list(R.nivel(p)) == ["E", "E", "E", "D", "D", "D+", "D+", "C-", "C-", "C",
                                "C", "C+", "C+", "A/B", "A/B"]


def test_puntos_del_anexo_y_topes():
    comp = pd.DataFrame({"educa_jefe": [1, 11], "banos": [0, 5], "autos": [1, 3],
                         "internet": [0, 1], "ocupados": [3, 9], "dormitorios": [2, 7]})
    p = R.puntos(comp)
    assert p.iloc[0].tolist() == [0, 0, 22, 0, 46, 16]
    assert p.iloc[1].tolist() == [85, 47, 43, 32, 61, 32]
    assert p.sum(axis=1).tolist() == [84, 300]


def test_educa_regla_enigh_y_blancos_no_son_ninguno():
    niv = pd.Series(["00", "02", "02", "03", "04", "05", "06", "07", "08", "08", "09", "", "99"])
    gra = pd.Series(["0", "5", "6", "3", "2", "3", "2", "1", "3", "4", "1", "", ""])
    e = C.educa_desde_niv(niv, gra, "enif2024-endutih")
    assert e.iloc[:11].tolist() == [1, 3, 4, 6, 6, 6, 7, 8, 9, 10, 11]
    assert e.iloc[11:].isna().all()
    e21 = C.educa_desde_niv(pd.Series(["04", "05", "09"]), pd.Series(["1", "1", "1"]), "enif2021")
    assert e21.tolist() == [6, 6, 11]
    with pytest.raises(RuntimeError):
        C.educa_desde_niv(pd.Series(["12"]), pd.Series(["1"]), "enif2024-endutih")


def test_oro_enigh_distribucion_exacta(tmp_path):
    """Seis hogares con puntaje calculado a mano: A/B, C+, C, C-, D+, E."""
    filas = [  # educa, baños, autos, internet, ocupados, dormitorios -> puntaje
        ("11", 2, 2, 1, 4, 4),   # 85+47+43+32+61+32 = 300 -> A/B
        ("10", 1, 1, 1, 2, 3),   # 59+24+22+32+31+24 = 192 -> C+
        ("08", 1, 1, 0, 2, 3),   # 27+24+22+0+31+24 = 128 -> C-
        ("08", 1, 1, 1, 2, 3),   # 27+24+22+32+31+24 = 160 -> C
        ("06", 1, 0, 0, 2, 2),   # 18+24+0+0+31+16 = 89 -> D
        ("01", 0, 0, 0, 1, 1),   # 0+0+0+0+15+8 = 23 -> E
    ]
    hog, con, viv = [], [], []
    for i, (e, b, a, it, o, dm) in enumerate(filas):
        fv = f"{i:010d}"
        viv.append({"folioviv": fv, "cuart_dorm": dm, "bano_comp": b})
        hog.append({"folioviv": fv, "foliohog": "1", "conex_inte": 1 if it else 2,
                    "num_auto": a, "num_van": 0, "num_pickup": 0})
        con.append({"folioviv": fv, "foliohog": "1", "educa_jefe": e, "ocupados": o,
                    "upm": f"{i // 2:05d}", "est_dis": "001", "factor": 100, "remesas": 0})
    base = "conjunto_de_datos_{t}_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_{t}_enigh2022_ns.csv"
    ruta = tmp_path / "oro.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr(base.format(t="hogares"), S._csv_bytes(list(hog[0]), hog))
        z.writestr(base.format(t="concentradohogar"), S._csv_bytes(list(con[0]), con))
        z.writestr(base.format(t="viviendas"), S._csv_bytes(list(viv[0]), viv))
    comp, _ = M.nse_hogares("ENIGH", "2022", str(ruta), None)
    assert comp["puntaje"].tolist() == [300, 192, 128, 160, 89, 23]
    assert comp["nivel"].tolist() == ["A/B", "C+", "C-", "C", "D", "E"]
    d = M.distribucion(comp)
    assert d["grupos"] == {"BAJO": 2 / 6, "MEDIO": 2 / 6, "ALTO": 2 / 6}


def test_imputacion_cae_de_celda_y_es_determinista(tmp_path):
    don = C.enigh2022(S.enigh2022(tmp_path / "d.zip", n=400))
    t = I.tabla_donante(don)
    comp = pd.DataFrame({"educa_jefe": [11.0, np.nan], "internet": [1.0, 1.0],
                         "ocupados": [9.0, 1.0], "autos": [1.0, 0.0],
                         "banos": np.nan, "dormitorios": np.nan})
    v1, u1 = I.imputa(comp, t)
    v2, _ = I.imputa(comp, t)
    assert v1.equals(v2)
    assert u1.iloc[1] == 2  # sin educa_jefe cae a (con_auto)


@pytest.mark.parametrize("inst,ola", list(G.CALCS))
@pytest.mark.parametrize("rama,n", [("normal", 1200), ("rara", 40), ("sin_nse", 300)])
def test_conducto_acepta_cada_rama(inst, ola, rama, n):
    spec = yaml.safe_load((ROOT / "data/corrida0" / G.calc_id(inst, ola) / "spec.yaml")
                          .read_text(encoding="utf-8"))
    out = G.corrida_sintetica(inst, ola, rama=rama, n=n, replicas=20)
    assert C0._valida_outputs(spec, out) == []


@pytest.mark.parametrize("inst,ola", list(G.CALCS))
def test_medidor_del_calc_es_el_del_modulo(inst, ola):
    a = (ROOT / "data/corrida0" / G.calc_id(inst, ola) / "medidor.py").read_bytes()
    assert a == (ROOT / "tools/dominios/amai/medidor.py").read_bytes()
