# Bloque de adopción de reglas · 1 · ACTO GEN2-CIERRE-Y-PRODUCTO-3

Derivado de `canon/reglas-contrastadas-v1_1.tsv` (162 reglas) con `python3 forense/analisis/reglas-bloque-1/genera_bloque_reglas.py`. Cero cifras tecleadas: cada punto se re-lee de su CALC sellado. Todo RETROSPECTIVO (olas vistas); ninguna regla se valida prospectivamente aquí.

**Cómo se adopta.** El merge de mesa del PR que trae este archivo es la adopción del bloque (E.2), condicional a la decisión pendiente sobre el criterio de CONFIRMA (`FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01`, ABIERTA): si CONFIRMA cubre la conducta descriptiva, el bloque es el de abajo; si exige la regla completa (SI+ENTONCES+PORQUE), la regla pasa a MATIZA y el bloque queda vacío. Adoptar no escribe `milpa/tramite.yaml`: la regla viva la escribe el escritor de relevo tras esa decisión (NC de este acto).

## 1 · El bloque (CONFIRMA con tier evidenciado ≥ media)

| regla_id (variantes fundidas) | regla (verbatim, primer campo del texto) | RESULT · punto [IC95] · unidad | tier declarado → evidenciado | procedencia | firewall |
|---|---|---|---|---|---|
| `RG-afa48731c6` (RG-160683e479;RG-709601ed63) | SI hogares de menor ingreso reservan más gasto a alimentos, ENTONCES probar precios, presentaciones y costo total por canasta. | `RESULT-ENIGH-CONSUMO-PISOS-PART-ALIMENTOS-2022-DECIL-D01-P` · 0.511 [0.483, 0.539] · proporcion (hogar) | — → fuerte | (a) | NO-APLICA |

Se adopta la **conducta descriptiva** (SI), no el ENTONCES prescriptivo ni el PORQUE: el driver no se identifica con un marginal descriptivo (A-bis: co-observación no es identificación).

## 2 · Destino de las reglas

| destino | filas de regla |
|---|---:|
| `BLOQUE` | 3 |
| `FUERA-DEL-BLOQUE:TIER-EVIDENCIADO-BAJO-MEDIA` | 3 |
| `PROPUESTA:MATIZA-SIN-RESULT` | 1 |
| `PROPUESTA:SIN-CIFRA` | 141 |
| `REPORT-V3:MATIZ-CON-CIFRA` | 14 |

- `BLOQUE`: 3 filas = 1 regla(s) madre con sus variantes fundidas.
- `FUERA-DEL-BLOQUE:TIER-EVIDENCIADO-BAJO-MEDIA`: CONFIRMA cuya evidencia no pasa de hipótesis razonable (una ola, contraste rural−urbano sin identificar el driver). Siguen PROPUESTA.
- `REPORT-V3:MATIZ-CON-CIFRA`: la regla se reescribe en su report v3 con el matiz y la cifra (P4).
- `PROPUESTA:SIN-CIFRA`: quedan PROPUESTA con su instrumento pendiente (columna `instrumento_sugerido`).
- ROMPE: ninguna regla.

Destino por regla: `forense/analisis/reglas-bloque-1/destino-reglas-v1_0.tsv`.

## 3 · Texto de firma (listo para mesa)

«Mesa adopta el bloque 1 de reglas de GEN2-CIERRE-Y-PRODUCTO-3 como regla descriptiva de conducta (SI), sin adoptar su ENTONCES ni su PORQUE, si y solo si el criterio de CONFIRMA de FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01 cubre la conducta descriptiva.»
