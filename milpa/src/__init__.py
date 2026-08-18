"""`milpa.src` — la rebanada mínima del motor de matriz.

ACTO LANE-A-E0-E5, COMMIT C2. Fase CON SELLO del encargo
`forense/encargos/2026-08-14-MOTOR-3-E0-autocontenido.md`, habilitada por
`ADR-100` (sello de `ADR-MOTOR-2`, M1-M6 firmadas).

LEY DE MESA VIGENTE, cableada aquí porque es lo que gobierna qué puede hacer
este paquete: **E0 compila y reproduce lo YA adjudicado — prohibido producir
cifra nueva al canon.** Toda calibración E1+ espera el cierre de BARRIDO-2.

Principio de diseño: un módulo que pudiera producir una cifra nueva nace
CERRADO CON LLAVE, no ausente. Existe, tiene contrato, y falla ruidosamente si
se le invoca antes de su sello (ver `pi.py`).
"""

__all__ = [
    "clases",
    "procedencia",
    "celdas",
    "pi",
    "theta",
    "matriz",
    "momentos",
    "motor",
    "salida",
]

VERSION = "0.1.0"
