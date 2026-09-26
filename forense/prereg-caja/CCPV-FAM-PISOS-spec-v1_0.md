# Pisos de estructura del hogar por segmento, Censo 2010 (muestra) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-LOTE-1`, 25/sep/2026, CAJA, rama `acto/gen2-cola-lote-1`,
0-bis `3a49c186`. Encargo: `forense/encargos/2026-09-25-GEN2-COLA-LOTE-1.md` (pieza P-CCPV). CALC:
`CALC-CCPV-FAM-PISOS-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor de microdato
censal (sólo metadatos `.dta` —nombres de columna— y los `.do` de etiquetas del propio ZIP).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` El encargo dice «Censo 2020 muestra ampliada». La muestra 2020 (VIVIENDAS/PERSONAS
  con `FACTOR`/`ESTRATO`/`UPM`) **no está en el corpus**: `Censo2020_CAAS_eum_csv` es el censo de
  alojamientos de asistencia social y `Censo2020_CEU_eum_csv` el de entorno urbano (manifiesto,
  corrección del 3/ago y sus descriptores). En corpus: diccionario y cuestionario ampliado 2020
  (estructura) y la **muestra censal 2010** (`MC2010_<ee>_dta`, 32 ZIP, ids
  `cc1_inegi_ccpv_2010__mc2010_<ee>_dta`). Además, 2020 es la ola más reciente del programa:
  **E.6 — 2020 RESERVADA** aunque llegara a adquirirse. Se mide 2010. INTERPRETACIÓN-DECLARADA.
- `[EJECUTADO]` Cada ZIP 2010 trae `viviendas_<ee>.dta`, `personas_<ee>.dta`, `migrantes_<ee>.dta` y
  los `.do` de etiquetas. VIVIENDAS: `tipohog`, `numpers`, `factor`, `estrato`, `upm`, `tam_loc`.
  PERSONAS: `sexo`, `edad`, `parent`, `nivacad`, `factor`, `estrato`, `upm`, `tam_loc`. Llave
  `ent`+`id_viv`. Personas no trae número de hogar: el hogar censal es la vivienda particular
  habitada (una fila de VIVIENDAS), y `TIPOHOG` es la clasificación de INEGI para ella.
- `[EJECUTADO]` Códigos por texto (`.do` del ZIP): `SEXO2` 1 «Hombre» **3 «Mujer»**; `EDAD2` 999
  «No especificado»; `PARENT` «¿Qué es (NOMBRE) de la jefa(e)?» 1 Jefa(e) · 2 Esposa(o) · 3 Hija(o) ·
  4 Nieta(o) · 5 Nuera o yerno · 6 Madre o padre · 7 Suegra(o) · 8 Otro parentesco · 9 Sin parentesco
  · 99 No especificado; `TIPOHOG` «Tipo de hogar censal» 1 Nuclear · 2 Ampliado · 3 Compuesto ·
  4 Familiar no especificado · 5 No familiar unipersonal · 6 No familiar de corresidentes · 9 No
  especificado; `TAM_LOC` 1 <2 500 · 2 2 500–14 999 · 3 15 000–99 999 · 4 100 000+; `NIVACAD` 0–12,
  99 No especificado.
- `[EJECUTADO]` FAM-005 (edad de salida del hogar parental): el censo no la pregunta (diccionario
  ampliado 2020 y personas 2010 sin variable de edad de independización). Va a
  `no-construibles-v1_1.tsv`, no aquí.

## 1 · Unidad, universo, diseño

HOGAR: filas de VIVIENDAS con `factor > 0`, `estrato` y `upm` no vacíos. PERSONA (sólo PER60-*):
filas de PERSONAS con el mismo filtro y su propio `factor`. Diseño: estrato = `ent|estrato`, UPM =
`ent|estrato|upm` (llaves opacas; la entidad las hace únicas en el país). Jefe = la única persona
con `parent = 1` de la vivienda; vivienda con 0 o >1 jefes → fuera de los ejes del jefe
(diagnósticos `G-VIV-SIN-JEFE`, `G-VIV-JEFE-MULTIPLE`). Diagnósticos de catálogo: sexo fuera de
{1,3}, parentesco fuera de {1–9,99}, edad 999.

## 2 · Conductas (por texto)

Hogares (universo: `TIPOHOG` 1–6 salvo donde se dice):
HOG-NUCLEAR (1) · HOG-AMPLIADO (2) · HOG-COMPUESTO (3) · HOG-UNIPERSONAL (5) · HOG-CORRESIDENTES (6) ·
HOG-CON-60MAS (≥1 residente de 60+; universo: hay uno, o todas las edades conocidas) ·
HOG-CON-MENOR-18 (ídem con <18) · HOG-60MAS-Y-MENOR-18 (ambos; corresidencia intergeneracional por
edad) · HOG-TRES-GENERACIONES (nieta(o) de la jefa(e), o madre/padre/suegra(o) junto con hija(o);
universo: parentesco conocido de todos, o la condición se cumple) · HOG-JEFA-MUJER (sexo del jefe = 3) ·
HOG-TAMANO-MEDIO (media de `numpers`, 1–60) · AM-HOG-NUCLEAR-O-AMPLIADO y AM-HOG-UNIPERSONAL
(universo: hogares con 60+ y `TIPOHOG` 1–6).
Personas: PER60-VIVE-SOLO (persona de 60+ en hogar `TIPOHOG` = 5; universo: 60+ con `TIPOHOG`
1–6) y su total expandido (Σ factor, sin IC).

## 3 · Ejes (uno a la vez)

Hogar: TOTAL · SEXO-JEFE · EDAD-JEFE (≤29, 30–44, 45–59, 60+) · ESCOLARIDAD-JEFE (`NIVACAD`
básica o menos {0,1,2,3,5,6,7} / media superior {4,8} / superior {9–12}) · TLOC (4) · ENT (32).
Persona 60+: TOTAL · SEXO · EDAD (60–69, 70–79, 80+) · TLOC · ENT. Región, formalidad y NSE: no
(el encargo los pide «donde A4 lo autorizó»; no hay autorización A4 para el censo en este acto).

## 4 · Estimación

Razón ponderada con bootstrap de UPM dentro de estrato (certeza para UPM única,
`PCG64(20260925)`, 1 000 réplicas, percentiles 2.5/97.5, contrato conservador), receta común
`tools/dominios/salud/pisos_diseno.py` por sha256. Una ola abierta: **sin IC de persistencia**.

## 5 · Controles

Sintético en `tests/test_cola_lote_1_pisos.py`. Control post-sello, sin tocar el procedimiento:
la nota compara TIPOHOG 2010 con las cifras 2020 que citan los reports (24.4 % ampliados,
12.4 % unipersonales; 82 % / 16.8 % entre hogares con 60+) en **dirección y orden**, nunca como
reproducción: diez años de distancia.

## 6 · Auditoría (afirma sobre México)

**Unidad:** hogar ≠ persona — 16.8 % (hogares) y 1.8 millones (personas) son dos unidades; aquí
salen con ids distintos. **Antigüedad:** 2010 no es 2020; la nota no afirma el valor 2020.
**Clasificación:** `TIPOHOG` es de INEGI; «tres generaciones» es construcción propia por
parentesco con la jefa(e) y no ve generaciones no emparentadas con ella. **Cifra escrita a mano:**
ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
