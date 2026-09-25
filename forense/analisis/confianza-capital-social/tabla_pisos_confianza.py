#!/usr/bin/env python3
"""Deriva tabla-pisos-confianza-v1_0.tsv (conducta × segmento × ola, con el id de cada RESULT) desde los
resultados.json sellados de los cuatro CALC de ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1
(misma forma que forense/analisis/salud-bienestar/tabla_pisos.py de #1124). Sólo lee los sellados;
ninguna cifra se teclea. Uso: python3 forense/analisis/confianza-capital-social/tabla_pisos_confianza.py

Dominio: el del mapa (`canon/mapa-dominios-v1_0.tsv`) al que pertenece el report que cita la
conducta. La tolerancia (homosexualidad) no tiene dominio en el mapa: se rotula VALORES-FUERA-DEL-MAPA."""
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CALCS = {"CALC-WVS-PISOS-2018-0001": "RESULT-WVS-PISOS-2018",
         "CALC-LATINOBAROMETRO-PISOS-2023-0001": "RESULT-LATINOBAROMETRO-PISOS-2023",
         "CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001": "RESULT-PEW-PISOS",
         "CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001": "RESULT-LAPOP-PISOS-CS"}
CS = ("MIEMBRO-", "ASISTE-ORG-", "ASISTE-ASOC-", "ASISTE-COMITE-", "ASISTE-PARTIDO", "AYUDO-",
      "TRABAJA-POR-", "FIRMO-", "ASISTIO-")
REL = ("RELIGION-", "IMPORTANCIA-DE-DIOS", "ASISTE-SERVICIO-", "PERSONA-RELIGIOSA", "PERTENECE-",
       "CATOLICO", "SIN-RELIGION", "PRACTICANTE", "ORA-")
TOL = ("RECHAZA-VECINO-HOMOSEXUAL", "HOMOSEXUALIDAD-JUSTIFICABLE", "APRUEBA-HOMOSEXUALES-")


def dominio(c):
    if c.startswith(TOL):
        return "VALORES-FUERA-DEL-MAPA"
    if c.startswith(REL):
        return "RELIGIOSIDAD"
    if c.startswith(CS):
        return "CAPITAL_SOCIAL"
    if c.startswith(("CONFIANZA-", "CONFIA-")):
        return "CONFIANZA"
    return "AUTORIDAD"


PAT = re.compile(r"^(?P<c>.+?)-(?P<ola>20\d\d)-(?P<eje>TOTAL|SEXO|EDAD|ESCOLARIDAD|TAMLOC|INGRESO-SUBJETIVO|CLASE-SUBJETIVA|UR)-(?P<cat>.+)-P$")


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
            yield [calc, m["c"], dominio(m["c"]), m["ola"], m["eje"], m["cat"],
                   _v(r, b + "-P"), _v(r, b + "-IC-LO"), _v(r, b + "-IC-HI"),
                   _v(r, b + "-ICC-LO"), _v(r, b + "-ICC-HI"), _v(r, b + "-N"), k]


def main():
    cab = ["calc", "conducta", "dominio", "ola", "eje", "categoria", "p", "ic_lo", "ic_hi",
           "icc_lo", "icc_hi", "n", "result_id_p"]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tabla-pisos-confianza-v1_0.tsv")
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
