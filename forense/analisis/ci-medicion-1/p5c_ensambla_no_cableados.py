#!/usr/bin/env python3
"""P5 · ACTO GEN2-TUBERIA-CI-MEDICION-1. Los 44 archivos tests/test_*.py que
el censo (forense/analisis/ci-guardias/censo-tests.tsv) marca sin correr en
CI: 36 NECESITA-DEPENDENCIA, 8 FALLA-DE-VERDAD. Recomendación por categoría.
"""
import csv

filas = []
with open("../ci-guardias/censo-tests.tsv") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        v = r["veredicto"]
        if v == "FALLA-DE-VERDAD" or v.startswith("NECESITA-DEPENDENCIA"):
            filas.append(r)

with open("no-cableados-44.tsv", "w", encoding="utf-8") as f:
    f.write("archivo\tveredicto\tdependencias_faltantes\ttiempo_seg\tdetalle\trecomendacion\tjustificacion\n")
    for r in filas:
        if r["veredicto"].startswith("NECESITA-DEPENDENCIA"):
            rec = "MANTENER-SIN-CABLEAR"
            just = (
                "Ejercita derivaciones GEN2 reales (numpy/pandas/scipy/pytest/jsonschema/openpyxl), "
                "que este propio repo ya corre en CAJA con corpus montado -- no es decoración, es "
                "una prueba que necesita un entorno que CI deliberadamente no monta (requirements.txt "
                "explícito, sin el stack científico, D-14: no se construye base central). Cablearla "
                "en CI exige instalar ese stack en las ~330 corridas medidas por segundo test, cuando "
                "hoy corre de todas formas en cada sesión de CAJA que la toca. Costo a un lector si se "
                "elimina: pierde la única prueba de esa derivación GEN2; no se recomienda eliminar."
            )
        else:  # FALLA-DE-VERDAD
            rec = "DEFECTO-ABIERTO-NO-SE-TOCA-AQUI"
            just = (
                f"Falla de verdad, activa: {r['detalle']}. PARO de este acto prohíbe modificar un "
                "test (§7); D-14 del censo que lo detectó también prohíbe arreglarlo ahí. Es "
                "exactamente el caso que el encargo distingue de 'decoración': nadie lo mira. "
                "Recomendación: NO se elimina (perdería la única señal de que algo real está roto); "
                "se abre como NC con dueño para que un acto de contenido lo investigue -- no éste, "
                "que sólo mide."
            )
        f.write(f"{r['archivo']}\t{r['veredicto']}\t{r['dependencias_faltantes']}\t{r['tiempo_seg']}\t{r['detalle']}\t{rec}\t{just}\n")

print(f"Escrito no-cableados-44.tsv ({len(filas)} filas)")
