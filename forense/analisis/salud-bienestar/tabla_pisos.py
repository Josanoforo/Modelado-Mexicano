#!/usr/bin/env python3
"""Deriva tabla-pisos-v1_0.tsv (conducta × segmento × ola, con el id de cada RESULT) desde los
resultados.json sellados de los tres CALC de ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1. Sólo lee
los sellados; ninguna cifra se teclea. Uso: python3 forense/analisis/salud-bienestar/tabla_pisos.py"""
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CALCS = {"CALC-ENSANUT-PISOS-SALUD-0001": "RESULT-ENSANUT-PISOS-SALUD",
         "CALC-ENCODAT-PISOS-SUSTANCIAS-0001": "RESULT-ENCODAT-PISOS-SUSTANCIAS",
         "CALC-ENBIARE-PISOS-BIENESTAR-0001": "RESULT-ENBIARE-PISOS-BIENESTAR"}
DOMINIO = {
    "DEPRESION-CESD7": "SALUD_MENTAL", "IDEACION-SUICIDA-ADULTOS": "SALUD_MENTAL",
    "IDEACION-SUICIDA-ADOLESCENTES": "SALUD_MENTAL", "ANSIEDAD-GAD2": "SALUD_MENTAL",
    "SATISFACCION-VIDA": "SALUD_MENTAL", "ESCALERA-CANTRIL": "SALUD_MENTAL",
    "CONFIANZA-MAYORIA-GENTE": "CONFIANZA", "CONFIANZA-GENTE-CONOCIDA": "CONFIANZA",
    "CONFIANZA-POLICIA-MUNICIPAL": "CONFIANZA", "CONFIANZA-PARTIDOS": "CONFIANZA",
    "CUENTA-APOYO-FAMILIA": "CAPITAL_SOCIAL", "CUENTA-APOYO-AMISTADES": "CAPITAL_SOCIAL",
    "TIENE-RELIGION": "RELIGIOSIDAD", "ASISTE-SERVICIO-RELIGIOSO": "RELIGIOSIDAD",
}
PAT = re.compile(r"^(?P<c>.+?)-(?P<ola>20\d\d)-(?P<eje>TOTAL|SEXO|EDAD|ESTRATO|ESCOLARIDAD|TLOC)-(?P<cat>.+)-P$")


def _v(r, k):
    x = r.get(k)
    return "" if x is None else (f"{x:.6f}" if isinstance(x, float) else str(x))


def filas():
    for calc, pref in CALCS.items():
        doc = json.load(open(os.path.join(RAIZ, "data", "corrida0", calc, "resultados.json")))
        r = doc.get("resultados", doc)
        r = {x["id"]: x["valor"] for x in r} if isinstance(r, list) else r
        for k in r:
            m = PAT.match(k[len(pref) + 1:]) if k.startswith(pref + "-") else None
            if not m:
                continue
            b = k[:-2]
            yield [calc, m["c"], DOMINIO.get(m["c"], "SALUD"), m["ola"], m["eje"], m["cat"],
                   _v(r, b + "-P"), _v(r, b + "-IC-LO"), _v(r, b + "-IC-HI"),
                   _v(r, b + "-ICC-LO"), _v(r, b + "-ICC-HI"), _v(r, b + "-N"), k]


def main():
    cab = ["calc", "conducta", "dominio", "ola", "eje", "categoria", "p", "ic_lo", "ic_hi",
           "icc_lo", "icc_hi", "n", "result_id_p"]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tabla-pisos-v1_0.tsv")
    fs = sorted(filas(), key=lambda f: (f[2], f[0], f[1], f[4], f[5], f[3]))
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
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
