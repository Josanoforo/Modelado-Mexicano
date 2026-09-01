#!/usr/bin/env python3
"""Deriva, para cada variable_id EXISTE-SATISFACE de data/cruce-inverso-v1_1.tsv,
si ya existe una entrada `clase: MEDIDO...` propia en milpa/procedencia.yaml
(bloque acotado por línea de inicio de la SIGUIENTE clave a indentación de 2
espacios) que la cite -- es decir, si la medición diferida de FP-172 sobre esa
variable ya se ejecutó por otro acto (COND-ATRIB, CAL-CONF Fase B, Encargo X,
Encargo W1-P, Encargo E, etc.) antes de que este acto (MAESTRA33-C8) corriera.

Uso: python3 tools/deriva_diferidas_fp172.py
"""
import re
import sys

PROCEDENCIA = "milpa/procedencia.yaml"
CRUCE = "data/cruce-inverso-v1_1.tsv"


def cargar_bloques(path):
    lines = open(path, encoding="utf-8").readlines()
    starts = [
        i
        for i, l in enumerate(lines)
        if re.match(r"^  [a-zA-Z_][a-zA-Z0-9_áéíóúñ]*:\s*(\S.*)?$", l)
    ]
    starts.append(len(lines))
    bloques = []
    for k in range(len(starts) - 1):
        s, e = starts[k], starts[k + 1]
        nombre = lines[s].strip()
        texto = "".join(lines[s:e])
        m = re.search(r"clase:\s*\"?([^\"\n]*)", texto)
        clase = m.group(1) if m else ""
        bloques.append((s + 1, nombre, clase, texto))
    return bloques


def cargar_existe_satisface(path):
    filas = []
    for linea in open(path, encoding="utf-8"):
        if linea.startswith("#") or not linea.strip():
            continue
        cols = linea.rstrip("\n").split("\t")
        if cols[0] == "variable_id":
            continue
        if len(cols) >= 3 and cols[1] == "EXISTE-SATISFACE":
            filas.append({"variable_id": cols[0], "instrumentos": cols[2], "n_citas": cols[3]})
    return filas


# A.13: el detector de bloques es un PRIMER PASE, no la verificación final.
# Un bloque "clase: MEDIDO" puede citar un variable_id dentro de prosa que
# EXPLÍCITAMENTE lo excluye de esa medición (colisión de mnemónico, ruta
# bloqueada, candidato descartado). Las dos excepciones de abajo se verificaron
# leyendo el bloque completo a mano (no a ojo sobre el grep) -- ver
# forense/notas/2026-09-01-c8-medidor-fp172-cierre.md para la cita exacta:
#   - AP7_1: el hit cae en el bloque `exposicion_violencia` (procedencia.yaml
#     ~468-470), pero el propio texto dice "colisión de nombre entre encuestas
#     distintas, ya documentada, no es la AP7_1 de ENVIPE de este acto" -- el
#     AP7_1 de ENCUCI (trabajo voluntario) nunca fue medido ni usado.
#   - P4_10: el hit cae en `familismo_apoyo` solo como referencia cruzada
#     ("...vía P4_10"); la propia entrada de P4_10 en
#     rutas_estimabilidad_coeficiente.detalle (línea ~1121) la declara
#     SIN-RUTA / SUBDETERMINADA-PERSISTENTE -- bloqueada por decisión formal
#     previa (ACTO ESCALAS-COMPLETAS-P1), no promovible sin reabrir esa
#     decisión.
FALSOS_POSITIVOS_MEDIDO = {
    "AP7_1": "colision de mnemonico ENCUCI/ENVIPE, nunca medido bajo ese hit (procedencia.yaml ~468-470)",
    "P4_10": "SIN-RUTA / SUBDETERMINADA-PERSISTENTE, bloqueado por ACTO ESCALAS-COMPLETAS-P1 (procedencia.yaml ~1121)",
}


def main():
    bloques = cargar_bloques(PROCEDENCIA)
    filas = cargar_existe_satisface(CRUCE)

    medidas, diferidas = [], []
    for fila in filas:
        v = fila["variable_id"]
        hits = [b for b in bloques if re.search(r"\b" + re.escape(v) + r"\b", b[3])]
        medido_bruto = any("MEDIDO" in b[2].upper() for b in hits)
        medido = medido_bruto and v not in FALSOS_POSITIVOS_MEDIDO
        n_pares = len(set(fila["instrumentos"].split(";")))
        fila["medido"] = medido
        fila["bloques"] = [b[1] for b in hits]
        fila["n_instrumentos_declarados"] = n_pares
        fila["nota_exclusion"] = FALSOS_POSITIVOS_MEDIDO.get(v, "")
        (medidas if medido else diferidas).append(fila)

    print(f"# EXISTE-SATISFACE: {len(filas)} · ya MEDIDO (verificado, bloque real + lectura manual de excepciones): {len(medidas)} · sin medicion utilizable: {len(diferidas)}")
    print("# candidatas 'pares del motor' (>=2 instrumentos declarados por motor) sin medicion utilizable:")
    for f in diferidas:
        marca_par = "PAR" if f["n_instrumentos_declarados"] >= 2 else "solo"
        print(f"  {f['variable_id']}\t{marca_par}\tinstrumentos={f['instrumentos']}\tbloques_donde_aparece={f['bloques']}\tmotivo_exclusion={f['nota_exclusion']}")


if __name__ == "__main__":
    sys.exit(main())
