"""Casos materiales del IC de persistencia, sin abrir RESULT históricos."""
import json
import math
from pathlib import Path

import yaml

from tools.astra.encig.ic_calibrado import medidor as m


def test_train_no_usa_2023_y_final_si():
    cells = [(a, c) for a in m.AXES for c in m.CATS[a]]
    d = {}
    for year, p in ((2017, .2), (2019, .3), (2021, .4)):
        d[year] = {}
        for axis, cat in cells:
            stem = f"RESULT-ENCIG-SERIE-{year}-DIGITAL-{axis}-{cat}"
            d[year].update({stem + "-P": p, stem + "-IC-LO": p - .02,
                            stem + "-IC-HI": p + .02})
    train, count = m._tau(d, cells, m.TRAIN_PAIRS)
    assert count == {"SEXO": 4, "EDAD": 8, "ESCOLARIDAD": 8}
    assert all(v > 0 for v in train.values())
    frozen = m._interval(d[2021], "RESULT-ENCIG-SERIE-2021-DIGITAL-SEXO-1", train["SEXO"])
    d[2023] = {f"RESULT-PISOS-ENCIG2023-V2-DIGITAL-{a}-{c}-P": .9 for a, c in cells}
    final, _ = m._tau(d, cells, m.FINAL_PAIRS)
    assert all(final[a] > train[a] for a in m.AXES)
    assert frozen == m._interval(d[2021], "RESULT-ENCIG-SERIE-2021-DIGITAL-SEXO-1", train["SEXO"])


def test_frontera_es_no_calibrable():
    source = {"x-P": 0, "x-IC-LO": .01, "x-IC-HI": .1}
    assert m._interval(source, "x", .2) is None
    assert m._wilson(0, 0) == (None, None)


def test_media_transiciones_igual_peso_con_celdas_faltantes():
    cells = [("SEXO", "1"), ("SEXO", "2")]
    d = {y: {} for y in (2017, 2019, 2021)}
    vals = {2017: (.2, .2), 2019: (.3, .3), 2021: (.4, 1.0)}
    for year, pair in vals.items():
        for cat, p in zip(("1", "2"), pair):
            d[year][f"RESULT-ENCIG-SERIE-{year}-DIGITAL-SEXO-{cat}-P"] = p
    tau, n = m._tau(d, cells, m.TRAIN_PAIRS)
    a = (m._logit(.3) - m._logit(.2)) ** 2
    b = (m._logit(.4) - m._logit(.3)) ** 2
    assert math.isclose(tau["SEXO"], (a + b) / 2)
    assert n["SEXO"] == 3


def test_salida_completa_coincide_con_spec():
    cells = [(a, c) for a in m.AXES for c in m.CATS[a]]
    identity = "source_instrument\tstatus\taxis\tcell_id\n" + "".join(
        f"ENCIG\tCONSTRUIBLE\t{a.lower()}\tRESULT-PISOS-ENCIG2023-V2-DIGITAL-{a}-{c}-P\n"
        for a, c in cells)
    comp = "conducta\tola\tveredicto\n" + "".join(
        f"C-LUZ-DIGITAL\t{y}\t{v}\n" for y, v in
        ((2017, "MISMO-INSTRUMENTO"), (2019, "MISMO-INSTRUMENTO"),
         (2021, "MISMO-INSTRUMENTO"), (2023, "CAMBIO-MENOR")))
    inputs = {"PISOS-REJILLA-METADATOS": {"bytes": identity.encode()},
              "ENCIG-COMPARABILIDAD-TEXTO": {"bytes": comp.encode()}}
    for year, p in ((2017, .2), (2019, .3), (2021, .4), (2023, .5)):
        out = {}
        for axis, cat in cells:
            stem = (f"RESULT-PISOS-ENCIG2023-V2-DIGITAL-{axis}-{cat}" if year == 2023 else
                    f"RESULT-ENCIG-SERIE-{year}-DIGITAL-{axis}-{cat}")
            out.update({stem + "-P": p, stem + "-IC-LO": p - .02,
                        stem + "-IC-HI": p + .02})
        key = "RESULT-ENCIG-2023-PISO" if year == 2023 else f"RESULT-ENCIG-{year}"
        inputs[key] = {"bytes": json.dumps({"resultados": out}).encode()}
    actual = m.medir(inputs, {})
    spec = yaml.safe_load(Path("data/corrida0/CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001/spec.yaml").read_text())
    assert set(actual) == {r["id"] for r in spec["resultados"]}
    assert actual[m.PREF + "-N-ELEGIBLES"] == 10
