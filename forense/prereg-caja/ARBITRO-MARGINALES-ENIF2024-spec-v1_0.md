# ÁRBITRO GEN2 · marginales por eje · ENIF 2024 · dos desenlaces de ahorro · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

ACTO GEN2-ARBITRO-MARGINALES-1 · pieza P-ENIF (21/sep/2026, CAJA). CALC:
`CALC-ARBITRO-MARGINALES-ENIF2024-0001`. Encargo archivado por A.3 en
`forense/encargos/2026-09-21-GEN2-ARBITRO-MARGINALES-1.md` (sello de cuerpo
`b6d73b3f…`). Compuerta interna del encargo (§8): este COMMIT-1 en `origin`
con su oro en verde protege **abrir dato**; ENIF 2024 no se abre antes.

## 1 · Qué estima (primera línea: universo, unidad, escala)

**Universo:** personas elegidas de 18 años y más de `TMODULO.csv` de ENIF 2024
(`enif_2024_enif_2024_bd_csv`) con ponderador `FAC_PER` positivo y diseño
`EST_DIS × UPM_DIS` no vacío, con desenlace definido; cada eje conserva su
denominador válido (código inválido o blanco → fuera sólo de ese eje).
**Unidad:** PERSONA elegida 18+. **Escala:** proporción ponderada en [0, 1],
con IC95 por bootstrap de UPM estratificado (10 000 réplicas, `numpy.PCG64(42)`,
percentiles 2.5/97.5, un solo plan de réplicas compartido por todas las celdas).

**Estimando:** para cada uno de los dos desenlaces del árbitro
(`ahorra_solo_informal` = D9: informal sí y formal no; `informal_cualquiera`:
informal sí) y cada celda marginal de la rejilla del piso — sexo (1/2), edad
(18-29 / 30-44 / 45-59 / 60-96), escolaridad (hasta primaria / secundaria /
media superior / superior), localidad (menor de 15 000 / 15 000 y más),
formalidad (sin / con seguridad social por el trabajo; **universo restringido
a quien llega a 3.13**, A-bis 4, rotulado así) y cuenta (sin / con cuenta) —
la proporción ponderada de la conducta en ENIF 2024, más el total por
desenlace. Es la **realidad R** contra la que se califica el piso de
persistencia t-1 (`CALC-PISOS-ENIF2021-EJES-0003`, `…-FORMALIDAD-0001`).

## 0 · Exposición declarada (ADR-46)

- Leídos antes de congelar: los medidores y specs sellados de los pisos
  (`PISOS-ENIF2021-ejes-spec-v2_1.md`, `PISOS-ENIF2021-formalidad-spec-v1_0.md`),
  `tools/medidor_ahorro_enif24.py` y `tools/ejes_maestra35_l1.py` (nemónicos
  2024 del árbitro GEN1), `forense/notas/2026-09-02-MAESTRA35-L1-P0-censo.md`
  §4.1/§4.4 (catálogo `NIV` 2024, `EDAD_V`, `TLOC`, `P3_13`), el yaml del
  árbitro `milpa/tramite-ola5-propuesta-v0.yaml` con sus `p` GEN1 de 2024 a la
  vista, y los 28 marginales por eje de ENIF 2024 ya sellados en
  `CALC-C2-COMPUESTO-IC-ENIF2024-0001` (`RESULT-C2IC-ENIF2024-G-MARG-*`).
- NO abierto: ningún microdato de ENIF 2024 (ni `TMODULO.csv` ni la sección
  de crédito, RESERVADA). Sí abierto ENIF 2021 (ola anterior, no reservada)
  para la prueba de oro.
- Cifra esperada: las GEN1 y las de C2IC existen y se citan en la
  adjudicación; **no** gobiernan este procedimiento (que es el del piso) y no
  se ajusta nada para cuadrar con ellas. Discrepar con ellas es un hallazgo
  sobre GEN1/el método del piloto, no un defecto de esta corrida.

## 2 · Procedimiento: el del piso, apuntado a la ola nueva

`medidor.py` IMPORTA por ruta (input `MEDIDOR-PISO-EJES-0003`, sha256
`d069f38b…`) las funciones selladas del piso — `_csv`, `_code`, `_age`,
`_school`, `_slug`, `_cells`, `_estimate`, `_known_any`, `_formal` — y sólo
añade el mapa de nemónicos por ola y la guardia. Con
`parametros.ola = "2021"` sobre `enif2021_csv` el mismo punto de entrada
reproduce los 192 RESULT de los dos pisos sellados con Δ = 0 (prueba de oro,
`tests/test_arbitro_marginales_enif2024.py`); con `ola = "2024"` mide R.

**Mapa 2021 → 2024 (A.15, por texto de pregunta):**

| rol | 2021 (piso) | 2024 (esta corrida) | fuente del texto |
|---|---|---|---|
| miembro | `conjunto_de_datos_tmodulo_enif_2021.csv` | `TMODULO.csv` | `tools/medidor_ahorro_enif24.py:31` |
| ponderador | `FAC_ELE` | `FAC_PER` | yaml `:1415` `ponderador: FAC_PER` |
| edad | `EDAD` | `EDAD_V` (18-98; 97-98 fuera por el corte 18-96 del piso, contados) | censo P0 §4.4 |
| escolaridad | `P3_1_1` (0-9) | `NIV` (00-11): 00-02 hasta primaria · 03 secundaria · 04-07 media superior · 08 licenciatura, 09 especialidad, 10 maestría, 11 doctorado → superior | censo P0 §4.1 (FD xlsx) |
| localidad | `TLOC` 1-2 / 3-4 | `TLOC` 1-2 / 3-4 (1 = 100 000+, 2 = 15 000-99 999, 3 = 2 500-14 999, 4 = < 2 500) | censo P0 §4.4 |
| formalidad | `P3_10` 1-5 con / 6 sin | `P3_13` 1-6 con / 7 sin; 9 y blanco fuera, contados | formalidad-spec §1 (cuestionario 2024 p. 7) |
| ahorro informal | `P5_1_1..6` | `P5_1_1..6` | idem |
| tenencia de cuenta | `P5_4_1..9` | `P5_4_1..9` | idem |
| ahorro formal («ahorró en esa cuenta») | `P5_7_1..9` | `P5_6_1..9`, pares por posición con `P5_4_i` | `tools/medidor_ahorro_enif24.py:34` |
| diseño | `EST_DIS`, `UPM_DIS` | `EST_DIS`, `UPM_DIS` | yaml `:1415` |

Conductas exactamente como la spec v2.1 del piso: informal = cualquiera de
`P5_1_i = 1`, no si todas = 2, indefinido en otro caso; formal = sí si
cualquier `P5_6_i = 1`, no si para cada i `P5_4_i = 2` o `P5_6_i = 2`;
D9 = informal sí y formal no (cero si informal no o formal sí).

## 3 · Celdas del marcador que cubre (por id)

Las 32 filas `SOLO-PISO` de ENIF 2024 en `data/corrida0/marcador-segmento.tsv`
(`55c8d57c`), enlazadas en `forense/prereg-caja/ARBITRO-MARGINALES-metadatos-v1_0.tsv`
(`cell_id_piso` → `cell_id_R`): el id de R es el del piso con el prefijo
`RESULT-PISOS-ENIF2021-V2-` / `RESULT-PISOS-ENIF2021-FORMALIDAD-` sustituido por
`RESULT-ARBITRO-ENIF2024-`. Además emite el total por desenlace
(`…-TOTAL-TODOS-*`) como control de coherencia y para el nacional, y los
diagnósticos `G-*` (universo, fuera de eje, códigos 9/blanco de formalidad,
n con NIV 10/11).

## 4 · Guardia de una sola variable (firma 3D, 21/sep/2026)

Misma semántica que el guardián de `tools/celda_d/marginales_reproduccion.py`:
`marginal()` recibe UN eje `str` de la lista blanca; no existe `cruce()`;
`auditoria_ast()` corre dentro de `medir()` antes de abrir el zip (imports en
lista blanca; sin `groupby`/`crosstab`/`pivot`/`merge`; toda llamada a
`marginal(` con eje literal de `EJES`; `_cells` sólo dentro de `marginal`;
ningún `_eje_*` combina dos comparaciones; ninguna constante nombra otro
instrumento ni archivo fuera de la lista) y está probada por mutación (una
mutación por regla) en el test. Reserva: con `ola ≠ 2024` ningún input que
nombre 2024 entra; ninguna variable de la sección de crédito se carga.

## 5 · Nulos y ramas terminales (D-22 ampliada)

`_estimate` del piso devuelve `None` en `-P/-IC-LO/-IC-HI` cuando una
categoría queda sin masa (denominador ponderado 0) o sin réplica definida;
esos tres ids llevan `permite_no_estimable: true` en `spec.yaml`. `-N`,
`-DEN-W`, `-B-VALIDAS` y los `G-*` nunca son nulos. El test ejercita, sobre
sintético, la rama de categoría vacía y la de eje entero vacío, y pasa la
salida por `corrida0._valida_outputs` (cero problemas) además del oro.

## 6 · Lo que NO hace

No agrupa por dos variables · no abre la sección de crédito · no adopta ·
no corrige el yaml GEN1 · no compara aquí contra el piso (eso es
`CALC-ARBITRO-PERSISTENCIA-ERROR-0001`, aritmética entre sellados).
