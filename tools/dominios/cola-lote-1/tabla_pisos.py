#!/usr/bin/env python3
"""Deriva forense/analisis/cola-lote-1/tabla-pisos-cola-lote-1-v1_0.tsv (conducta × segmento × ola, con el
id de cada RESULT) desde los resultados.json sellados de los cuatro CALC de ACTO GEN2-COLA-LOTE-1, e
imprime «N conductas con piso GEN2 por dominio». Sólo lee los sellados; ninguna cifra se teclea.
Registros (EMAT, EDR): sin IC de diseño; P exacta, N y CONTEO. Uso:
python3 tools/dominios/cola-lote-1/tabla_pisos.py [--verifica]"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# CALC -> (prefijo de RESULT, dominio del mapa según canon/mapa-dominios-v1_1.tsv / cola-medicion-v1_0.tsv)
CALCS = {"CALC-CCPV-FAM-PISOS-0001": ("RESULT-CCPV-FAM-PISOS", "FAMILIA_CUIDADOS"),
         "CALC-EMAT-PAREJA-PISOS-0001": ("RESULT-EMAT-PAREJA-PISOS", "PAREJA"),
         "CALC-ENPECYT-CONOC-PISOS-0001": ("RESULT-ENPECYT-CONOC-PISOS", "CONOCIMIENTO"),
         "CALC-EDR-SUICIDIO-PISOS-0001": ("RESULT-EDR-SUICIDIO-PISOS", "SALUD_MENTAL")}
EJES = "TOTAL|SEXO-JEFE|EDAD-JEFE|ESCOLARIDAD-JEFE|SEXO|EDAD|ESCOLARIDAD|TLOC|ENT"
PAT = re.compile(rf"^(?P<c>.+?)-(?P<ola>(?:19|20)\d\d)-(?P<eje>{EJES})(?:-(?P<cat>.+))?-P$")
CAB = ["calc_id", "conducta", "dominio", "ola", "eje", "categoria", "p", "ic_lo", "ic_hi", "icc_lo", "icc_hi",
       "tau2", "n", "conteo", "result_id_p"]
SALIDA = os.path.join(RAIZ, "forense", "analisis", "cola-lote-1", "tabla-pisos-cola-lote-1-v1_0.tsv")


def _v(r, k):
    x = r.get(k)
    return "" if x is None else (f"{x:.6f}" if isinstance(x, float) else str(x))


def filas():
    for calc, (pref, dom) in CALCS.items():
        r = json.load(open(os.path.join(RAIZ, "data", "corrida0", calc, "resultados.json"),
                           encoding="utf-8"))["resultados"]
        ms = [(k, m) for k in sorted(r) if k.startswith(pref + "-")
              for m in [PAT.match(k[len(pref) + 1:])] if m and not m["c"].startswith("G-")]
        ultima = max(m["ola"] for _, m in ms)
        for k, m in ms:
            b = k[:-2]
            # τ² e IC calibrado de persistencia: ids sin ola, sobre el piso de la última ola abierta
            s = f"{pref}-{m['c']}-{m['eje']}" + (f"-{m['cat']}" if m["cat"] else "")
            u = m["ola"] == ultima
            yield [calc, m["c"], dom, m["ola"], m["eje"], m["cat"] or "", _v(r, b + "-P"), _v(r, b + "-IC-LO"),
                   _v(r, b + "-IC-HI"), _v(r, s + "-ICC-LO") if u else "", _v(r, s + "-ICC-HI") if u else "",
                   _v(r, s + "-TAU2") if u else "", _v(r, b + "-N"), _v(r, b + "-CONTEO"), k]


def main():
    fs = list(filas())
    texto = "\t".join(CAB) + "\n" + "".join("\t".join(f) + "\n" for f in fs)
    if "--verifica" in sys.argv:
        igual = open(SALIDA, encoding="utf-8").read() == texto
        print("TABLA", "IDENTICA" if igual else "DIFIERE")
        return 0 if igual else 1
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    open(SALIDA, "w", encoding="utf-8", newline="\n").write(texto)
    por = {}
    for f in fs:
        por.setdefault(f[2], set()).add(f[1])
    print(f"filas={len(fs)}")
    print("N conductas con piso GEN2 por dominio: " + " · ".join(f"{d} {len(c)}" for d, c in sorted(por.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
