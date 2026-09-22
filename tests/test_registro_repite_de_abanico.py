#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_registro_repite_de_abanico.py -- prueba de
tools/corrida0.py::_sucesor_de (ACTO GEN2-PENDIENTES-CAJA-1, 22/sep/2026).

Defecto que atrapa (ocurrido, no supuesto): las 9 specs ENIGH 2016/2018/2020
selladas en d1a27b7d declaran `repite_de: CALC-ENIGH2022-*` con sentido
«misma receta, otra ola». registro() leía todo `repite_de` como sucesión y,
con tres hijos por padre, ganaba el último: la vista habría publicado las
tres corridas ENIGH 2022 como SUPERADO->CALC-ENIGH2020-*.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0 as C  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def _o(calc, repite=""):
    return {"calc_id": calc, "repite_de": repite}


def _regla_vieja(oferta):
    return {o["repite_de"]: o["calc_id"] for o in oferta if o["repite_de"]}


def prueba_sintetica():
    oferta = [_o("A"), _o("A-v2", "A"), _o("P"),
              _o("P-2016", "P"), _o("P-2018", "P"), _o("P-2020", "P")]
    s = C._sucesor_de(oferta)
    afirma(s.get("A") == "A-v2", "una cadena de un solo hijo sigue siendo sucesion")
    afirma("P" not in s, "un abanico de tres hijos no es sucesion")
    afirma(_regla_vieja(oferta).get("P") == "P-2020",
           "control: la regla vieja SI marcaba P superado por el ultimo hijo")


def prueba_vista_real():
    ruta = os.path.join(ROOT, "data", "corrida0", "corridas.tsv")
    lineas = [l for l in open(ruta, encoding="utf-8").read().split("\n")
              if l and not l.startswith("#")]
    cab = lineas[0].split("\t")
    filas = [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]
    for padre in ("CALC-ENIGH2022-INTENSIDAD-REMESAS-0001",
                  "CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003",
                  "CALC-ENIGH2022-REMESAS-CONTEXTO-0001"):
        est = [f["estado"] for f in filas if f["spec_id"] == padre]
        afirma(est == ["SELLADA"], f"{padre}: estado en la vista {est}, se espera ['SELLADA']")


def main():
    prueba_sintetica()
    prueba_vista_real()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_registro_repite_de_abanico.py: 2 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
