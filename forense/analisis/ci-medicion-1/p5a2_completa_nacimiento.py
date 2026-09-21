#!/usr/bin/env python3
"""P5 (corrección, ADENDA-1 A4) · completa la columna `citas` de
nacimiento-check-tests.tsv para los 27 tests que la extracción mecánica
(p5a_nacimiento_check.py -- sólo mira comentarios INMEDIATAMENTE antes del
`def`) dejó vacía. Leído a mano contra tests/check.py: banner de sección
(`# Tnn · ...`), docstring completo y cuerpo de la función, no sólo la
línea justo anterior al `def`. Donde no hay ningún defecto citado, se
declara `SIN-DEFECTO-CITADO` -- no se inventa un motivo (regla explícita
de la adenda).
"""
import csv

# label -> citas (verificado a mano contra tests/check.py, línea citada)
COMPLETADO = {
    "T01 fuente única de verdad": "SIN-DEFECTO-CITADO (tests/check.py:101)",
    "T02 duplicados nombre/contenido": "SIN-DEFECTO-CITADO (tests/check.py:118)",
    "T03 referencias colgantes": "SIN-DEFECTO-CITADO (tests/check.py:484)",
    "T05 ADR-32.c constructos en glosario": "SIN-DEFECTO-CITADO (tests/check.py:529)",
    "T07 vocabulario de tiers": "ADR-94; FP-41 (tests/check.py:600, dentro del cuerpo)",
    "T09 marco (c) usado como causa": "A-04/05/06, C-02..C-05 (tests/check.py:630, banner de sección)",
    "T10 diáspora (b) sin marcar": "A-07..A-09, R-03..R-05, T-04 (tests/check.py:646, banner de sección)",
    "T11 afirmaciones de estado absolutas": "defecto #1, 5 de 5 comprobadas resultaron falsas (tests/check.py:663, banner de sección)",
    "T12 conteos del motor": "SIN-DEFECTO-CITADO (tests/check.py:681)",
    "T14 T-INVENTARIO": "C1-01, C1-08 (tests/check.py:736, docstring)",
    "T15 T-ADR-COUNT": "SIN-DEFECTO-CITADO (tests/check.py:855)",
    "T17 T-FICHAS-COUNT": "R3.2 (tests/check.py:1044, docstring — misma sesión que motivó T14/T15/T16)",
    "T19a cabecera cruzada estado→modelo": "SIN-DEFECTO-CITADO (tests/check.py:1253; docstring cita \"Encargo A\" sin fecha ni número)",
    "T19b contador 14 cruzado (modelo)": "SIN-DEFECTO-CITADO (tests/check.py:1316)",
    "T20 T-CASCADA-MARCADA": "SIN-DEFECTO-CITADO (tests/check.py:1508)",
    "T21 T-CAPA2-CAPA3": "SIN-DEFECTO-CITADO (tests/check.py:2608)",
    "T22 T-FIRMAS": "A.12 (instrucciones-proyecto-v2_9.md) (tests/check.py:2143)",
    "T23 T-CABLEADO": "SIN-DEFECTO-CITADO (tests/check.py:2782; referencia interna \"§22\" sin acto fechado)",
    "T25 T-ROTULOS": "D-6/ADR-128 (tests/check.py:5147)",
    "T31 T-CRON": "ACTO MAESTRA38-CRON-2 · REGISTRO-Y-HUELLA (tests/check.py:6163)",
    "T32-bis T-PISOS-REJILLA": "SIN-DEFECTO-CITADO (tests/check.py:6811; sin banner de sección, a diferencia de T32-ter inmediatamente antes)",
    "T34 T-NO-CORRIDO": "A.14; ACTO GEN2-T8, 8/sep/2026 (tests/check.py:7116)",
    "T39 T-DIGESTO-NC": "ACTO AUTO-DIGESTO-1 · CAMBIOS-DESDE-EL-ULTIMO- (tests/check.py:6864)",
    "T43 T-SUCESOR-EXISTE": "ACTO GEN2-VIGENCIA-DEUDA-1, 16/sep/2026 (tests/check.py:7203)",
    "T44 T-ENADID-PRECISION": "SIN-DEFECTO-CITADO (tests/check.py:7265; sólo nombra la carpeta enadid-union-actual-cli-1 que valida)",
    "T46 T-UNION-NEWLINE": "ACTO GEN2-TUBERIA-SUCESOR-1, 21/sep/2026, P2 (tests/check.py:7648)",
    "T47 T-IDS-UNICOS": "ACTO GEN2-TUBERIA-SUCESOR-1, 21/sep/2026 (tests/check.py:7730)",
}

filas = list(csv.DictReader(open("nacimiento-check-tests.tsv"), delimiter="\t"))
tocadas = 0
for row in filas:
    if row["citas"] == "" and row["label"] in COMPLETADO:
        row["citas"] = COMPLETADO[row["label"]]
        tocadas += 1

vacias_restantes = [r["label"] for r in filas if r["citas"] == ""]
print(f"filas completadas: {tocadas}; vacías restantes: {len(vacias_restantes)} {vacias_restantes}")

with open("nacimiento-check-tests.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["label", "funcion", "linea", "citas", "comentario"],
                        delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(filas)
print("Escrito nacimiento-check-tests.tsv")
