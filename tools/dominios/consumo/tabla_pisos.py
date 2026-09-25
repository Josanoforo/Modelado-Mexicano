#!/usr/bin/env python3
"""Deriva forense/analisis/consumo-gasto/tabla-pisos-v1_0.tsv (conducta × segmento × ola, con el
id de cada RESULT) desde los resultados.json sellados de los dos CALC de ACTO
GEN2-CONSUMO-Y-GASTO-PISOS-1, e imprime «N conductas con piso GEN2 por dominio». Sólo lee
los sellados; ninguna cifra se teclea. Uso: python3 tools/dominios/consumo/tabla_pisos.py"""
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CALCS = {"CALC-ENIGH-CONSUMO-PISOS-0001": "RESULT-ENIGH-CONSUMO-PISOS",
         "CALC-ENGASTO-CONSUMO-PISOS-0001": "RESULT-ENGASTO-CONSUMO-PISOS"}
# dominio del mapa (canon/mapa-dominios-v1_0.tsv col. 26): crédito, deuda, préstamo, medio de pago
# e ingreso-gasto son DINERO; estructura, canal y conectividad del gasto son CONSUMO.
DINERO = {"PART-EFECTIVO-EN-GASTO-DIRECTO", "HOG-TIENE-TARJETA-CREDITO", "HOG-USA-TARJETA-ALIMENTOS-SI-TIENE",
          "HOG-PAGO-TARJETA-CREDITO", "HOG-PAGO-DEUDAS", "HOG-RECIBE-PRESTAMO", "HOG-GASTO-MAYOR-INGRESO",
          "HOG-COMPRA-FIADO", "HOG-COMPRA-TARJETA-CREDITO"}
PAT = re.compile(r"^(?P<c>.+?)-(?P<ola>20\d\d)-(?P<eje>TOTAL|SEXO-JEFE|EDAD-JEFE|ESCOLARIDAD-JEFE|TLOC|DECIL|ENTIDAD)"
                 r"-(?P<cat>.+)-P$")
SALIDA = os.path.join(RAIZ, "forense", "analisis", "consumo-gasto", "tabla-pisos-v1_0.tsv")


def _v(r, k):
    x = r.get(k)
    return "" if x is None else (f"{x:.6f}" if isinstance(x, float) else str(x))


def filas():
    for calc, pref in CALCS.items():
        doc = json.load(open(os.path.join(RAIZ, "data", "corrida0", calc, "resultados.json"), encoding="utf-8"))
        r = doc.get("resultados", doc)
        r = {x["id"]: x["valor"] for x in r} if isinstance(r, list) else r
        for k in r:
            m = PAT.match(k[len(pref) + 1:]) if k.startswith(pref + "-") else None
            if not m:
                continue
            b = k[:-2]
            yield [calc, m["c"], "DINERO" if m["c"] in DINERO else "CONSUMO", m["ola"], m["eje"], m["cat"],
                   _v(r, b + "-P"), _v(r, b + "-IC-LO"), _v(r, b + "-IC-HI"),
                   _v(r, b + "-ICC-LO"), _v(r, b + "-ICC-HI"), _v(r, b + "-N"), k]


def main():
    cab = ["calc", "conducta", "dominio", "ola", "eje", "categoria", "p", "ic_lo", "ic_hi",
           "icc_lo", "icc_hi", "n", "result_id_p"]
    fs = sorted(filas(), key=lambda f: (f[2], f[0], f[1], f[4], f[5], f[3]))
    with open(SALIDA, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\t".join(cab) + "\n")
        for f in fs:
            fh.write("\t".join(f) + "\n")
    conductas = {}
    for f in fs:
        if f[4] == "TOTAL" and f[6] != "":
            conductas.setdefault(f[2], set()).add((f[0], f[1]))
    print(f"filas={len(fs)}")
    for d in sorted(conductas):
        print(f"{d}\t{len(conductas[d])}")


if __name__ == "__main__":
    main()
