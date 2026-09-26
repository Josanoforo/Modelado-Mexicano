**Contador: 42 conductas con piso GEN2 por dominio — FAMILIA_CUIDADOS 14 · PAREJA 12 · CONOCIMIENTO 10 · SALUD_MENTAL 6** (`python3 tools/dominios/cola-lote-1/tabla_pisos.py`, sobre los sellados). No se adopta nada; no se evalúa prospectivamente.

# GEN2-COLA-LOTE-1 · cierre

25–26/sep/2026 · CAJA · Opus 5.5 · rama `acto/gen2-cola-lote-1` · base `aa36232a` = SHA de redacción · 0-bis `3a49c186` · encargo `forense/encargos/2026-09-25-GEN2-COLA-LOTE-1.md` · MODO AUTÓNOMO. La sesión se cortó después del COMMIT-2 de ENPECYT; otra sesión retomó el 26/sep sobre `0330d753` sin rehacer nada sellado: verify aislado, asientos, tabla, mapa, nota, FP y cascada.

## 1 · Qué se midió

| pieza | CALC | olas abiertas (reservada) | conductas | RESULT | verify aislado | COMMIT-1 → COMMIT-2 |
|---|---|---|---|---|---|---|
| P-CCPV | `CALC-CCPV-FAM-PISOS-0001` | 2010 muestra censal (2020 RESERVADA) | 14 | 3 216 | REPRODUCE / IDENTICO, 3 216/3 216, max\|Δ\| = 0 | `ac1cae42` (+1b `b2fd5e47`) → `0e691812` |
| P-EMAT | `CALC-EMAT-PAREJA-PISOS-0001` | 2010–2023, 14 olas (2024 RESERVADA) | 12 | 10 506 | REPRODUCE / IDENTICO, 10 506/10 506, max\|Δ\| = 0 | `21dfec0b` → `b0a1386e` |
| P-EDR | `CALC-EDR-SUICIDIO-PISOS-0001` | 2015–2023, 9 olas (2024 RESERVADA) | 6 | 8 724 | REPRODUCE / IDENTICO, 8 724/8 724, max\|Δ\| = 0 | `30fb560d` → `4192e078` |
| P-ENPECYT | `CALC-ENPECYT-CONOC-PISOS-0001` | 2011, 2013, 2015 (2017 RESERVADA) | 10 | 1 698 | REPRODUCE / IDENTICO, 1 698/1 698, max\|Δ\| = 0 | `3d31a11f` → `0330d753` |

Specs humanas: `forense/prereg-caja/{CCPV-FAM,EMAT-PAREJA,EDR-SUICIDIO,ENPECYT-CONOC}-PISOS-spec-v1_0.md` (con sidecar), congeladas antes de abrir registros ni microdatos; `spec.yaml` generados por `tools/dominios/cola-lote-1/genera_spec_yaml.py`; test sintético `tests/test_cola_lote_1_pisos.py`. Tabla conducta × segmento × ola con el id de cada RESULT: `forense/analisis/cola-lote-1/tabla-pisos-cola-lote-1-v1_0.tsv` (6 816 filas; `--verifica` IDENTICA). Asientos E.7: cuatro filas en `forense/replay-evidencia.tsv`, evidencia en `forense/analisis/cola-lote-1/evidencia-replay-cola-lote-1-*-2026-09-26.json`.

**IC calibrado de persistencia** (receta común `tools/dominios/salud/pisos_diseno.py`, por sha256): τ² por conducta × eje × categoría en EMAT (14 olas), EDR (9) y ENPECYT (3), columnas `icc_lo/icc_hi/tau2` de la tabla sobre la última ola abierta (ids `-TAU2`, `-ICC-LO/-HI`). En los registros el ee de diseño es nulo y el ICC es solo persistencia. CCPV, con una sola ola, no tiene.

**Ejecuciones previas declaradas (D-24, «Commits»).** CCPV: la primera corrida falló al leer (`NotImplementedError`: `MC2010_15`/`_20` usan Deflate64) sin producir resultado. El COMMIT-1b (`b2fd5e47`) añade el lector Deflate64, con largo y CRC comprobados, y limita el marco persona a 60+ (el único universo de persona que la spec usa). Se hizo antes de cualquier resultado; la spec humana no cambió. Un intento salió `NO-EJECUTADO` (preflight con árbol sucio) y dos murieron con la sesión sin escribir. Ninguno es un primer resultado distinto.

### 1.1 · Premisas del encargo que cayeron (cláusula de autonomía, puntos 1-2)

- **«Censo 2020 muestra ampliada».** La muestra 2020 (VIVIENDAS/PERSONAS con factor) no está en el corpus: los ids `Censo2020_*` son CAAS y CEU. Además, 2020 es la ola más reciente, así que queda RESERVADA por E.6. Se mide la muestra 2010 (32 ZIP `MC2010_<ee>_dta`). INTERPRETACIÓN-DECLARADA.
- **«¿Encuesta de Matrimonio?».** EMAT es la *Estadística de Matrimonios*: registro administrativo de los matrimonios civiles inscritos. No observa unión libre ni disolución (los divorcios son otro registro). La lista «edad a la unión, unión libre vs matrimonio, disolución» se sustituye por lo que las cinco afirmaciones piden y el registro sostiene.
- **«ENPECYT 2017, una ola → descriptivo».** En el corpus están 2005–2017. 2017 queda RESERVADA; se miden 2011/2013/2015, la misma familia de cuestionario. 2011 no trae `EST_DIS`/`UPM_DIS`: ahí hay P ponderada sin IC.
- **«EDR: catálogo 1990/1995/2000 vs cola 2022;2024».** No hay discrepancia de programa: es la *Estadística de Defunciones Registradas*. En el corpus hay 2015–2024 por id; 2024 queda RESERVADA. Unidad: defunción registrada, nunca persona encuestada.
- **Sin población en el corpus**: no hay denominador para tasas por habitante (EMAT, EDR). Se publican conteos y composición; ninguna tasa.

## 2 · Verificación de texto y mapa (P1, NC `…MAPA-DOMINIOS-V1-1-1-3cf7-01`)

`ASTRA5-U0-FAM-005` va a `forense/analisis/dominios/no-construibles-v1_1.tsv`. Se recorrieron las 108 etiquetas `label variable` de `Personas.do` (MC2010) y ningún reactivo pregunta la edad de salida del hogar parental; `IDMADRE`/`IDPADRE` dan corresidencia actual, que es un proxy de estado, no de edad. Mapa re-derivado: `python3 forense/analisis/dominios/redictamina_v1_1.py`, y `--verifica` sale limpio. NO-CONSTRUIBLE-EN-CORPUS pasa de 0 a 1.

Las otras 15 afirmaciones **no suben a MEDIBLE-EN-CORPUS**. La compuerta A.15 del derivador exige que `texto_pregunta` case byte a byte con una fila de los seis inventarios de reactivos del repo, y ninguno trae EMAT, ENPECYT ni la muestra censal 2010. Solo aparece `edr2024` (ola reservada) y el diccionario ampliado 2020 (reservada). El texto de cada reactivo está citado de los descriptores y cuestionarios en las specs humanas (§0), pero extender un inventario queda fuera del §9. Se asienta como NC (§6 del encargo, `## NO-CORRIDO / RESERVAS`).

## 3 · Bloque C por report

Evidencia: **(a)** en todo. EMAT y EDR son registros administrativos completos (P exacta, sin muestreo). CCPV 2010 es una muestra censal con IC de diseño (bootstrap de UPM). ENPECYT es una encuesta urbana de 100 000+ habitantes con IC de diseño. Cada cifra es un RESULT sellado de la tabla.

### *Elegir, cortejar y amar* (PAREJA, EMAT)

- **PAREJA-001 (edad media al matrimonio 34.1 H / 31.3 M en 2022, desde 29.8 / 26.9 en 2013; 507 052 matrimonios)** — **CONFIRMA.** Edad media del contrayente: 2022 H 34.12, M 31.20; 2013 H 29.78, M 26.92. El total 2022 es 507 052, exacto. La mujer 2022 difiere en 0.1 (31.2 frente a 31.3): puede ser redondeo o cierre de edición y no se ajusta. Mide todas las nupcias, no solo las primeras.
- **PAREJA-012 (6 606 matrimonios del mismo sexo en 2023)** — **CONFIRMA** exacto: CONTEO 6 606, 0.0131 de 501 529 (ICC [0.0059, 0.0286]); 5 829 en 2022.
- **PAREJA-021 (52 % ambos trabajan; 53 % misma escolaridad, 2022)** — **MATIZA.** 0.5625 ambos trabajan (265 415 / 471 832) y 0.5837 misma escolaridad (269 107 / 461 002). El universo excluye los «no especificado» y la escolaridad «otra»; eso sube la proporción frente a una base con todos los matrimonios. Dirección confirmada, nivel de 4–5 pp arriba por la definición del denominador. En 2013 eran 0.4389 y 0.5716: ambos-trabajan subió 12 pp.
- **PAREJA-030 (25–29 concentra la mayoría; suben 30–34 y 35–39; matrimonios con menores 48 275 en 2013 → 32 en 2022)** — **MATIZA / CONFIRMA.** 25–29 es el quinquenio más frecuente (0.2533 de contrayentes en 2022), pero no «la mayoría». 30–34 sube de 0.1352 a 0.1770 y 35–39 de 0.0705 a 0.1019: **CONFIRMA**. Matrimonios con al menos un contrayente de 12–17: 32 en 2022, exacto (20 en 2023); en 2013 son 43 183, no 48 275. La definición del report no se conoce (¿contrayentes, no matrimonios?) y no se ajusta.
- **PAREJA-002 (tasa de nupcialidad por mil de 18+)** — **NO-COMPARABLE aquí**: falta el denominador de población en el corpus (NC).

### *La familia mexicana como sistema* y *Vejez y cuidado intergeneracional* (FAMILIA_CUIDADOS, CCPV 2010)

Todo es 2010 contra cifras 2020: **dirección y orden, nunca reproducción** (spec §5).
- **FAM-025 (24.4 % ampliados, 12.4 % unipersonales)** — **MATIZA.** En 2010: ampliados 0.2389 [0.2382, 0.2395], unipersonales 0.0944 [0.0940, 0.0948], nucleares 0.6386. El orden coincide; el 12.4 % de 2020 implica unos tres puntos más de unipersonales en diez años, y aquí no se puede verificar. Los unipersonales son más urbanos: 0.1040 en 100 000+ frente a 0.0800–0.0875 en el resto.
- **VEJEZ-005 (82 % de hogares con 60+ nucleares o ampliados; tamaño medio 3.4; hasta 28 % multigeneracionales)** — **CONFIRMA el 82 %, MATIZA el resto.** 0.8170 [0.8163, 0.8179] en 2010. El tamaño medio medido es el de todos los hogares (3.90), no el de los que tienen 60+: universos distintos, no se comparan. Tres generaciones por parentesco con la jefa(e): 0.1677; con 60+ y menor de 18 corresidiendo: 0.0975. «Hasta 28 %» es una cota del report con otra definición.
- **VEJEZ-006 (16.8 % unipersonales entre hogares con 60+ = 1.8 millones de personas 60+ solas)** — **CONFIRMA en orden.** 0.1556 en 2010 (0.2649 con jefa mujer, 0.0991 con jefe hombre). Personas 60+ que viven solas: 0.1143, y su total expandido es 1.20 millones en 2010 (hogar ≠ persona, ids distintos). Crece con la edad: 0.0892 en 60–69 y 0.1553 en 80+.
- **FAM-005 (edad de independización 28.9)** — **NO-CONSTRUIBLE** en el censo (§2).

### *Salud mental*, *Juventud* y *Familia* (SALUD_MENTAL, EDR)

Unidad: defunción registrada. **Sin tasas**: un conteo no es una tasa.
- **SALMEN-016 (los hombres mueren ~4 veces más por suicidio; más en varones de 15–44)** — **CONFIRMA en conteo, sin afirmar la razón de tasas.** 0.8059 de los suicidios CIE de 2023 son hombres (7 310 de 9 070; ICC [0.7939, 0.8174]; 0.8006 en 2015): 4.2 hombres por mujer en conteos. Con poblaciones de hombres y mujeres parecidas, esto va en la dirección de «~4 veces», pero no es la razón de tasas. 0.7287 de los suicidios con edad válida son de 15–44.
- **JUV-011 (11.4 vs 2.5 por 100 mil en 2023)** — **CONFIRMA en dirección (H > M); nivel no verificable** sin población.
- **SALMEN-015 (9 051 suicidios en 2024; 7.0/100k, desde 5.3 en 2015)** — **NO-COMPARABLE**: 2024 está RESERVADA. En la serie abierta, los suicidios CIE registrados pasan de 6 425 (2015) a 9 072 (2023), +41 % en conteo. Su peso en todas las defunciones es 0.0097 → 0.0113, con un valle de 0.0072 en 2020 porque el COVID infla el denominador. CIE X60–X84 y «presunto suicidio» concuerdan casi a la unidad (máximo 2 de diferencia por ola).
- **FAM-023 (tasa de suicidio 15–19 +114 % entre 2017 y 2022)** — **MATIZA con fuerza.** Suicidios CIE de 15–19 registrados: 795 (2017) → 861 (2022), **+8.3 %** en conteo. Un +114 % en tasa exigiría que la población de 15–19 cayera a la mitad en cinco años. El denominador no está en el corpus, así que la ruptura no se certifica aquí; con conteo creciente de un dígito, la cifra del report no se sostiene como tasa sin una fuente que la explique.

### *Report 26 · Knowledge* (CONOCIMIENTO, ENPECYT)

Piso 2015 contra las cifras 2017 del report: dirección y orden (2017 RESERVADA).
- **CONOC-004 (75.0 % interés al menos moderado, 2017)** — **CONFIRMA.** 0.7542 [0.7159, 0.7949] en 2015, con la misma redacción que 2017; ICC [0.678, 0.817]. Gradiente fuerte por escolaridad: básica 0.60, media 0.85, superior 0.91.
- **CONOC-005 (~92 % de acuerdo con invertir más en investigación)** — **CONFIRMA.** 0.9212 [0.9047, 0.9356] en 2015 («no sabe» en el denominador); 0.9376 sin él. Subió desde 0.8536 (2011) y 0.8674 (2013).
- **CONOC-025 (10/10: bomberos 59.5 %, inventores 48.4 %, enfermeras 41.5 %, investigadores 34.6 %; ~72 % «fe sobre ciencia»)** — **CONFIRMA el orden, MATIZA el nivel.** En 2015: bombero 0.5666, inventor 0.3778, enfermera 0.3535, investigador 0.2663. Es el mismo orden. Inventor (IC [0.318, 0.439]) e investigador (ICC [0.204, 0.340]) quedan por debajo de las cifras 2017. «Fe sobre ciencia»: 0.7012 [0.661, 0.741], estable desde 0.7258 (2011).

## 4 · Módulo de auditoría

- **Contadores:** mueve «N conductas con piso GEN2 por dominio» (+42: FAMILIA_CUIDADOS 14, PAREJA 12, CONOCIMIENTO 10, SALUD_MENTAL 6) y NO-CONSTRUIBLE-EN-CORPUS del mapa (0 → 1). MEDIBLE-EN-CORPUS no se mueve (§2).
- **Escalas y unidades:** matrimonio, contrayente, defunción, hogar, persona 60+ y persona urbana de 18+. Cada una lleva su id y ninguna se promedia con otra. Los registros no tienen IC de diseño; su ICC es persistencia.
- **¿Qué parece psicológico y es estructura o registro?** La «caída del matrimonio» es caída del registro civil: la unión libre no está en EMAT. El «aumento del suicidio» mezcla oportunidad de registro, clasificación y población: `SUIC-OCURRIDO-EN-OLA` 2023 = 0.9888 (el registro tardío es chico, pero existe). Vivir solo en la vejez es sobre todo de mujeres (viudez y longevidad), no una preferencia.
- **¿Clase media urbana?** ENPECYT es urbana de 100 000+ por diseño: nada de ella dice del México rural. El gradiente de interés por escolaridad es de 31 pp.
- **Antigüedad:** CCPV 2010 no es 2020. Ninguna frase afirma un valor 2020 o 2024.
- **PROSPECTIVA/RETROSPECTIVA:** nada es prospectivo. Todo es descripción retrospectiva de olas abiertas.
- **Peligroso leído simplista:** «los jóvenes se suicidan el doble» (el conteo sube 8 %); «el mexicano ya no se casa» (se registra menos y más tarde; la unión libre no se mide aquí).
- **¿Qué cifra se escribió a mano?** Ninguna; todas son de la tabla derivada o de RESULT por id. Firewall genético y marcos importados: no aplican.

## 5 · Adopción por instrumento (F-ASTRA-5-4)

Cuatro filas FP en `forense/firmas-pendientes.tsv`, `FP-260926-GEN2-COLA-LOTE-1-3a49-01..04` (CCPV, EMAT, EDR, ENPECYT). Todas recomiendan CON-RESERVA-DE-ANCHO, por esta razón en cada caso:

| FP | instrumento | razón de la reserva |
|---|---|---|
| 01 | CCPV | una ola, 2010 |
| 02 | EMAT | registro, sin unión libre |
| 03 | EDR | conteos sin tasa |
| 04 | ENPECYT | urbana; 2011 sin IC |
