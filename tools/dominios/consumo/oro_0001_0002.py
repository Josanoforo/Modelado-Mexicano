#!/usr/bin/env python3
"""Oro interno declarado en CONSUMO-ENIGH-PISOS-spec-v1_1.md §0-bis: toda RESULT de
CALC-ENIGH-CONSUMO-PISOS-0002 que no dependa de `gastoshogar` 2016/2018 es idéntica a la de
CALC-ENIGH-CONSUMO-PISOS-0001. Sólo lee los dos resultados.json sellados.

Dependen de gastoshogar 2016/2018 (y por eso se EXCLUYEN de la igualdad): P/EE/IC/N de esas olas
de las conductas desde gastoshogar, y su τ², N-DELTAS e ICC 2022 (heredan los Δ 2016→2018→2020).
Uso: python3 tools/dominios/consumo/oro_0001_0002.py  (sale 0 si COINCIDE, 1 si no)."""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
P = "RESULT-ENIGH-CONSUMO-PISOS-"
DESDE_GASTOS = ("PART-EFECTIVO-EN-GASTO-DIRECTO", "PART-CANAL-", "HOG-COMPRA-FIADO", "HOG-COMPRA-TARJETA-CREDITO",
                "HOG-COMPRA-INTERNET")


def _carga(calc):
    d = json.load(open(os.path.join(RAIZ, "data", "corrida0", calc, "resultados.json"), encoding="utf-8"))
    r = d.get("resultados", d)
    return {x["id"]: x["valor"] for x in r} if isinstance(r, list) else r


def depende(k):
    s = k[len(P):]
    if not s.startswith(DESDE_GASTOS):
        return s.startswith("G-2016-FILAS-GASTO") or s.startswith("G-2018-FILAS-GASTO")
    return ("-2016-" in s or "-2018-" in s or s.endswith("-TAU2") or s.endswith("-N-DELTAS")
            or s.endswith("-ICC-LO") or s.endswith("-ICC-HI"))


def main():
    a, b = _carga("CALC-ENIGH-CONSUMO-PISOS-0001"), _carga("CALC-ENIGH-CONSUMO-PISOS-0002")
    comunes = sorted(set(a) & set(b))
    comparadas = [k for k in comunes if not depende(k)]
    difieren = [k for k in comparadas if a[k] != b[k]]
    print(f"ids_0001={len(a)} ids_0002={len(b)} comunes={len(comunes)} comparadas={len(comparadas)} "
          f"excluidas_por_gastoshogar_2016_2018={len(comunes) - len(comparadas)} difieren={len(difieren)}")
    for k in difieren[:20]:
        print(f"  DIFIERE {k}: {a[k]!r} -> {b[k]!r}")
    print("ORO:", "COINCIDE" if not difieren else "NO-COINCIDE")
    return 0 if not difieren else 1


if __name__ == "__main__":
    sys.exit(main())
