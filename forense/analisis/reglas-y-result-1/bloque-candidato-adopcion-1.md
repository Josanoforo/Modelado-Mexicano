# Bloque candidato de adopción de reglas · 1 · ACTO GEN2-REGLAS-Y-RESULT-1

28/sep/2026 · derivado de `canon/reglas-contrastadas-v1_0.tsv` (162 reglas) · **candidato, no adoptado**: si mesa lo decide, el merge del PR que traiga el bloque es la adopción (E.2). Todo RETROSPECTIVO: ninguna regla se valida prospectivamente aquí.

## 1 · Conteo por dictamen (derivado: `python3 forense/analisis/reglas-y-result-1/p4_ensambla.py`, tras revisión R2 adversarial y decisiones R3 del usuario del 28/sep)

| dictamen | filas |
|---|---|
| CONFIRMA | 3 (una sola regla: RG-afa48731c6 + dos VARIANTE-DE fundidas) |
| MATIZA | 6 |
| MATIZA-SIN-CRUCE | 8 |
| ROMPE | 0 |
| INCOMPARABLE | 0 |
| SIN-CIFRA-GEN2 | 145 |

Solo (b)/(c): 39, fuera del bloque. Firewall genético: 12 RESPETA, 0 VIOLA. Tier declarado vs evidenciado: 21 bajan, 22 igual, 8 suben (sin promoción: el tier evidenciado es columna, no cambio de estado), 111 sin tier declarado — `tier-declarado-vs-evidenciado-v1_0.tsv` lista las 21 que no aguantan.

## 2 · El bloque — **CONDICIONAL a la decisión pendiente sobre el criterio de CONFIRMA**

| regla_id (fuentes fundidas) | regla | RESULT · punto [IC95] · unidad | tier evid. | implica para motor/catálogo |
|---|---|---|---|---|
| RG-afa48731c6 (+ RG-709601ed63, RG-160683e479) | SI hogares de menor ingreso ENTONCES mayor parte del gasto a alimentos | `RESULT-ENIGH-CONSUMO-PISOS-PART-ALIMENTOS-2022-DECIL-D01-P` 0.511 [0.483, 0.539] vs D10 0.283 [0.260, 0.308] · proporción del gasto, hogar; patrón repetido 2016/2018/2020 | fuerte | Sin consumidor en `tramite.yaml`. Se confirma la conducta descriptiva (SI); el ENTONCES («probar precios/canasta») es prescriptivo sin cifra y el PORQUE (restricción, Engel) no queda identificado. |

**Decisión pendiente (DECISIÓN-DE-MESA-PENDIENTE):** si CONFIRMA cubre la conducta descriptiva (bloque = 1 regla) o exige la regla completa (pasa a MATIZA; bloque = 0). El usuario pidió antes insumo para investigar buenas prácticas; ver §5.

RG-33ece9e072 (comités × escolaridad) salió del bloque: MATIZA por IC que no despeja (R3).

## 3 · ROMPE — correcciones propuestas a reports
Ninguna.

## 4 · MATIZA (fuera del bloque)
MATIZA: RG-56f645220c, RG-97bd27956f, RG-55c7a10915, RG-6f79d79dc1, RG-33ece9e072, RG-df62e016a7. MATIZA-SIN-CRUCE: RG-a4ed0259ce, RG-3d4669ddc0, RG-1bd7c23d10, RG-cc7bc4ae1a, RG-a215c82838, RG-806ce20ffa, RG-21c3d453f6, RG-b3349eadb3.

## 5 · Insumo para investigar el criterio de CONFIRMA (prompt de búsqueda)
Ver `forense/analisis/reglas-y-result-1/prompt-criterio-confirma.md`.

---

# Hoja para mesa (lenguaje RH)

**Qué se decide.** Si dos reglas de conducta, ya respaldadas por cifras selladas, pasan de «propuesta» a «adoptada».

**Lo que hay.** De 162 reglas escritas, 1 (en tres redacciones) se sostiene con cifra sellada en su parte descriptiva; 14 se matizan; ninguna queda desmentida; 145 no tienen cifra.

**Opciones.**
1. **Adoptar la regla de alimentos como conducta descriptiva** — recomendada si mesa acepta CONFIRMA de conducta: datos nacionales (a), IC disjuntos, cuatro olas.
2. Esperar cruces y el criterio de CONFIRMA — bloque más grande con las 8 MATIZA-SIN-CRUCE medidas en caja.
3. Declarar el bloque 1 vacío si CONFIRMA exige la regla completa.

**Texto de firma listo:** «Mesa adopta el bloque candidato 1 de GEN2-REGLAS-Y-RESULT-1 (RG-afa48731c6, con variantes RG-709601ed63 y RG-160683e479) como regla descriptiva de conducta, sin adoptar su ENTONCES prescriptivo ni su PORQUE.» · Fila: `FP-260928-GEN2-REGLAS-Y-RESULT-1-a3cc-01`.
