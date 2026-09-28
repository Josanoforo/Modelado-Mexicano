# R23 · Protocolo inferencial de C1 como contrato DIAGNÓSTICO · expediente

`ACTO GEN2-C1-SUCESORES-Y-LOTE-3`, P2 · `FP-260926-GEN2-ASTRA6-C1-INCERTIDUMBRE-SPEC-1-157c-01` · 28/sep/2026.

## Firma de mesa, verbatim

`forense/encargos/2026-09-28-GEN2-TRAMITE-FIRMAS-21-ADENDA-1.md`, R23 **(2)** («el protocolo como contrato DIAGNÓSTICO»): «Apruebo el protocolo como contrato DIAGNÓSTICO de reproducción de IC para intentos futuros; no es estimador de IC adoptable ni recertifica IC históricos. El margen de equivalencia y el control simultáneo se fijarán por mesa antes del siguiente conjunto sin revelar.»

## Objeto firmado, por sha256

| Archivo | sha256 |
|---|---|
| `catalogo-1-incertidumbre-spec/p1/protocolo-propuesto.md` | `26746feed14b93829eaf60656a71ff87057e8f7026d647a798d825564bf6c0f0` |

La implementación de referencia y su congelación (`p1/protocolo_v2.py`, `p1/congelacion-protocolo.json`, `p1/astra6-c1-p1-congelacion-auxiliar-v2.json`) se citan desde ahí. Este acto no las reejecuta.

## Qué dice, y cómo se aplica

1. **Contrato previo** (punto 1 del protocolo): antes de ejecutar se fijan estimando, marco de pares estrato/UPM con ceros, réplicas, RNG y versión, orden, singleton, denominador cero, percentiles y publicación. Un cambio de marco o de estimando es una diferencia inferencial y ninguna tolerancia la neutraliza.
2. **Ley frente a realización** (punto 3): el mismo marco con otro orden, generador o semilla conserva la ley y cambia la realización. Para afirmar la misma ley hace falta verificar la igualdad del marco y de los totales por UPM. La igualdad del punto no basta.
3. **Sin margen no hay adjudicación** (punto 5 y la firma): no hay umbral de equivalencia numérica, y la ausencia de rechazo nunca acredita equivalencia. Mientras mesa no fije margen y control simultáneo, **un IC reimplementado se reporta y no adjudica**, ni a favor ni en contra.

## Aplicación a las 92 de ENDIREH 2016 (el diferido de C1-LOTE-3)

C1-LOTE-3 dejó el asiento de `RESULT-ENDIREH2016-PF-TABLA` como DIFERIDO-A `GEN2-METODO-COMPARACION-INFERENCIAL-1`, con IC dentro 0/92 bajo tolerancia 1e-10 y el bootstrap hecho con otro generador. R23 es ese método. Bajo él:

- **IC de las 92: `IC-DIAGNOSTICO-R23-NO-ADJUDICA`.** El generador es distinto (realización distinta, declarada por la reconstructora antes de comparar), no hay margen firmado, y la igualdad de marco y de totales por UPM no se verificó: los números de réplica no se cruzaron UPM a UPM. El dictamen de IC queda cerrado como diagnóstico. No es una DISCREPANCIA de estimando ni una equivalencia.
- **Asiento de la tabla: se sostiene el NO-PASA de C1-LOTE-3.** No depende del IC: 2 de 92 puntos (edad 60+, EDAD = 98) caen fuera de la tolerancia del paquete, y una tabla con un punto fuera no pasa. No se añade fila nueva al libro.
- Dictamen por identidad: `catalogo-1-lote3/dictamen-lote3-v1_1.tsv`, columna `dictamen_ic_r23`.

## Pendiente de mesa (no lo fija este acto)

El margen de equivalencia y el control simultáneo. La firma dice que se fijan «antes del siguiente conjunto sin revelar», y los paquetes ENBIARE/ENCODAT del lote 3 son ese conjunto. Sin margen, sus IC se comparan y se reportan como diagnóstico, igual que arriba. Queda como pregunta en la hoja de cierre, con FP propia.
