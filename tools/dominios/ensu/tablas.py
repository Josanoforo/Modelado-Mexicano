#!/usr/bin/env python3
"""Tablas del acto GEN2-SEGURIDAD-ENSU-SERIE-1, sólo ids de RESULT sellados (ninguna cifra).

  tabla-serie-v1_0.tsv     conducta × eje × categoría × ola -> RESULT P/IC/N (CALC-ENSU-SERIE-0001
                           y, para ENT y CIUDAD de C02-C15, CALC-ENSU-PISOS-0001)
  tabla-dictamen-ensu-v1_0.tsv  una fila por serie -> RESULT del dictamen DONDE-CAMBIO

    python3 tools/dominios/ensu/tablas.py
"""
from __future__ import annotations

import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
OUT = RAIZ / "forense/analisis/seguridad-ensu"
EJES = ("TOTAL", "SEXO", "EDAD", "ENT", "CIUDAD")


def ids(calc):
    return json.loads((RAIZ / "data/corrida0" / calc / "resultados.json").read_text())["resultados"]


def partes(s):
    """'C01-INSEG-CIUDAD-2025T3-CIUDAD-40' -> (conducta, ola, eje, cat)."""
    i = next(k for k, t in enumerate(s.split("-")) if len(t) == 6 and t[4] == "T" and t[:4].isdigit())
    t = s.split("-")
    return "-".join(t[:i]), t[i], t[i + 1], "-".join(t[i + 2:])


def main():
    filas = {}
    for calc, pref in (("CALC-ENSU-SERIE-0001", "RESULT-ENSU-SERIE-"), ("CALC-ENSU-PISOS-0001", "RESULT-ENSU-PISOS-")):
        for k in ids(calc):
            if not k.endswith("-P") or "-G-" in k:
                continue
            c, o, e, cat = partes(k[len(pref):-2])
            filas.setdefault((c, e, cat, o), (calc, k[:-2]))
    lin = ["# GENERADO por tools/dominios/ensu/tablas.py -- sólo ids; el valor vive en el resultados.json sellado",
           "conducta\teje\tcategoria\tola\tcalc\tresult_p\tresult_ic_lo\tresult_ic_hi\tresult_n"]
    for (c, e, cat, o), (calc, b) in sorted(filas.items(), key=lambda x: (x[0][0], EJES.index(x[0][1]), x[0][2], x[0][3])):
        lin.append("\t".join([c, e, cat, o, calc, b + "-P", b + "-IC-LO", b + "-IC-HI", b + "-N"]))
    (OUT / "tabla-serie-v1_0.tsv").write_text("\n".join(lin) + "\n", encoding="utf-8")
    D = "RESULT-ENSU-DICTAMEN-"
    r = ids("CALC-ENSU-SERIE-0001")
    lin2 = ["# GENERADO por tools/dominios/ensu/tablas.py -- sólo ids (CALC-ENSU-SERIE-0001)",
            "conducta\teje\tcategoria\tresult_dictamen\tresult_direccion\tresult_k\tresult_n_fuera\t"
            "result_delta_pp\tresult_ola_ini\tresult_ola_fin\tresult_n_cambio_documentado"]
    for k in sorted(r):
        if not (k.startswith(D) and k.endswith("-DICTAMEN")):
            continue
        s = k[len(D):-len("-DICTAMEN")]
        t = s.split("-")
        j = max(i for i, x in enumerate(t) if x in ("TOTAL", "SEXO", "EDAD", "CIUDAD") and i >= 3)
        c, e, cat = "-".join(t[:j]), t[j], "-".join(t[j + 1:])
        b = D + s
        lin2.append("\t".join([c, e, cat] + [b + x for x in ("-DICTAMEN", "-DIRECCION", "-K", "-N-FUERA", "-DELTA-PP",
                                                             "-OLA-INI", "-OLA-FIN", "-N-CAMBIO-DOCUMENTADO")]))
    (OUT / "tabla-dictamen-ensu-v1_0.tsv").write_text("\n".join(lin2) + "\n", encoding="utf-8")
    print("serie", len(lin) - 2, "dictamen", len(lin2) - 2)


if __name__ == "__main__":
    main()
