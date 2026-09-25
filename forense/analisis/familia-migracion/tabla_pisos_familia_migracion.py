#!/usr/bin/env python3
"""Deriva tabla-pisos-familia-migracion-v1_0.tsv (conducta × segmento × ola, con el id de cada RESULT) desde los
resultados.json sellados de los tres CALC de ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1.
Sólo lee los sellados; ninguna cifra se teclea. Imprime «N conductas con piso GEN2 por
dominio» (conducta con al menos un P de TOTAL no nulo).
Uso: python3 forense/analisis/familia-migracion/tabla_pisos_familia_migracion.py"""
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CALCS = {"CALC-ENADID-FAMILIA-HOGARES-0001": "RESULT-ENADID-FAMILIA-HOGARES",
         "CALC-ENASIC-CUIDADOS-VEJEZ-0001": "RESULT-ENASIC-CUIDADOS-VEJEZ",
         "CALC-PEW-MIGRACION-MEX-0001": "RESULT-PEW-MIGRACION-MEX"}
# dominios del encargo §1 (VEJEZ no es dominio del mapa; sus filas viven en FAMILIA_CUIDADOS)
DOMINIO = {
    "HOGAR-UNIPERSONAL": "FAMILIA_CUIDADOS", "HOGAR-NUCLEAR": "FAMILIA_CUIDADOS",
    "HOGAR-AMPLIADO": "FAMILIA_CUIDADOS", "HOGAR-JEFATURA-FEMENINA": "FAMILIA_CUIDADOS",
    "JOVEN-25-34-HIJO-DEL-JEFE": "FAMILIA_CUIDADOS", "HOGAR-NECESITA-CUIDADOS": "FAMILIA_CUIDADOS",
    "PERSONA-60MAS": "VEJEZ", "AM60-VIVE-SOLO": "VEJEZ", "AM60-EN-HOGAR-AMPLIADO": "VEJEZ",
    "HOGAR-CON-60MAS-QUE-NECESITA-CUIDADOS": "VEJEZ", "AM60-CUIDADO-POR-ALGUIEN-DEL-HOGAR": "VEJEZ",
    "AM60-CUIDADOR-PRINCIPAL-MUJER": "VEJEZ", "AM60-CUIDADOR-PRINCIPAL-HIJA": "VEJEZ",
    "AM60-CUIDADOR-PRINCIPAL-CONYUGE": "VEJEZ", "AM60-CUIDADO-POR-PERSONA-DE-OTRO-HOGAR": "VEJEZ",
    "PERSONA-15MAS-UNIDA": "PAREJA", "UNIDO-15MAS-EN-UNION-LIBRE": "PAREJA",
}
EJES = ("TOTAL", "SEXO-JEFE", "EDAD-JEFE", "ESCOLARIDAD-JEFE", "TAMANO-HOGAR", "CONDICION-PAREJA",
        "SEXO", "EDAD", "ESCOLARIDAD", "TLOC")
PAT = re.compile(r"^(?P<c>.+?)-(?P<ola>20\d\d)-(?P<eje>" + "|".join(EJES) + r")-(?P<cat>.+)-P$")


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
            yield [calc, m["c"], DOMINIO.get(m["c"], "MIGRACION"), m["ola"], m["eje"], m["cat"],
                   _v(r, b + "-P"), _v(r, b + "-IC-LO"), _v(r, b + "-IC-HI"),
                   _v(r, b + "-ICC-LO"), _v(r, b + "-ICC-HI"), _v(r, b + "-N"), k]


def main():
    cab = ["calc", "conducta", "dominio", "ola", "eje", "categoria", "p", "ic_lo", "ic_hi",
           "icc_lo", "icc_hi", "n", "result_id_p"]
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tabla-pisos-familia-migracion-v1_0.tsv")
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
