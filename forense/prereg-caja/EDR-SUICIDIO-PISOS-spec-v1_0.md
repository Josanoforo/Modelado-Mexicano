# Pisos de mortalidad por suicidio registrada, EDR 2015–2023 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-LOTE-1`, 25/sep/2026, CAJA, rama `acto/gen2-cola-lote-1`,
0-bis `3a49c186`. Encargo: `forense/encargos/2026-09-25-GEN2-COLA-LOTE-1.md` (pieza P-EDR). CALC:
`CALC-EDR-SUICIDIO-PISOS-0001`. Congelada en el COMMIT-1 de EDR, **antes** de leer un solo registro
de `DEFUNyy.dbf` (sólo descriptores PDF de cada ZIP y cabeceras DBF: nombre/largo de campo).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas (discrepancia del encargo resuelta primero)

- `[EJECUTADO]` «¿Qué programa es EDR?»: *Estadística de Defunciones Registradas* de INEGI
  (manifiesto `edr2024_bd_dbf_zip`, url `/programas/edr/microdatos/defunciones/`; descriptores
  «Descripción de la base de datos nacional» dentro de cada ZIP). **Registro administrativo; unidad
  defunción registrada, nunca persona-encuesta** (encargo §1 y §2: «defunciones ≠ personas
  encuestadas»). Se trata como serie.
- `[EJECUTADO]` «Catálogo EDR 1990/1995/2000 vs cola 2022;2024»: no hay discrepancia de programa.
  La cola casó las olas que las afirmaciones citan (2022, 2024). En corpus, por id del manifiesto:
  `edr2015_2019_bd_dbf_zip` (DEFUN15–19), `cc1_inegi_mortalidad_2020__defunciones_base_datos_2020_dbf`,
  `cc1_inegi_edr_2021__…`, `edr2022_bd_dbf_zip`, `cc1_inegi_edr_2023__…`, y los quinquenios
  1990–2014 del catálogo. 2024 es la ola más reciente: **E.6 — RESERVADA**, no es input (guardia).
  Se abren 2015–2023 (nueve olas; 1990–2014 queda para un sucesor).
- `[EJECUTADO]` Códigos por texto de los descriptores 2019 y 2023: `SEXO` 1 Hombre 2 Mujer 9 No
  especificado; `EDAD` N(4): 1001–1023 horas, 2001–2029 días, 3001–3011 meses, 4001–4120 años, x098 y
  4998 no especificados; `CAUSA_DEF` «Causa de la defunción (lista detallada)», CIE-10;
  `PRESUNTO` (2015–2021) «Tipo de defunción (presunto)» y `TIPO_DEFUN` (2022–2023) «Tipo de
  defunción», «equivalente a la captada como presunto»: 3 = Suicidio (Lesión autoinfligida) en los
  dos; `ESCOLARIDA` 1 Sin escolaridad … 10 Posgrado, 88 no aplica, 99 no especificado; `TLOC_RESID`
  17 rangos + 99; `ANIO_OCUR`, `ANIO_REGIS`.
- `[EJECUTADO]` No hay población en corpus para denominador (manifiesto sin proyecciones CONAPO de
  población por edad y sexo). **Sin tasas por habitante**: FAM-023, JUV-011, SALMEN-015 y la razón de
  tasas de SALMEN-016 piden tasas; aquí se miden conteos y composición. La razón hombre/mujer de
  CONTEOS no es la razón de tasas y la nota no las iguala.

## 1 · Naturaleza, unidad, universo

Registro completo: **sin diseño, sin EE ni IC de diseño**; cada celda es P exacta, N y CONTEO.
Unidad: defunción registrada en el año del archivo (ola = año de registro). Universo base: todas
las filas vivas del DBF de la ola.

## 2 · Conductas (por texto)

SUICIDIO-CIE (causa CIE-10 X60–X84, «lesiones autoinfligidas intencionalmente»; universo causa no
vacía) · SUICIDIO-PRESUNTO (`PRESUNTO`/`TIPO_DEFUN` = 3; universo todas) — dos definiciones, se
publican las dos con su concordancia en diagnósticos. Entre suicidios CIE: SUIC-HOMBRE (sexo 1;
universo sexo 1–2) · SUIC-15-44 y SUIC-15-29 (edad en años; universo edad válida) ·
SUIC-OCURRIDO-EN-OLA (`ANIO_OCUR` = año de la ola: mide el registro tardío).

## 3 · Ejes (uno a la vez; ninguno consigo mismo)

TOTAL · SEXO · EDAD (0–9, 10–14, 15–19, 20–24, 25–29, 30–44, 45–59, 60+) · ENT de residencia (32) ·
TLOC de residencia (<2 500 = 1–3; 2 500–14 999 = 4–6; 15 000–99 999 = 7–12; 100 000+ = 13–17) ·
ESCOLARIDAD (primaria o menos 1–4 / secundaria 5–6 / media superior 7–8 / superior 9–10).
SUIC-HOMBRE no va por SEXO; SUIC-15-* no van por EDAD.

## 4 · Persistencia

Nueve olas: τ² por conducta × eje × categoría = media de Δ² en logit entre olas consecutivas
(`tau2` de la receta común); IC calibrado del piso 2023: expit(logit p ± 1.959964·√τ²), ee nulo.

## 5 · Controles

Sintético en `tests/test_cola_lote_1_pisos.py`. Post-sello, sin tocar el procedimiento: CONTEO
SUICIDIO-CIE 2023 por sexo frente a lo que citan JUV-011 y SALMEN-016 sólo en dirección (H > M).

## 6 · Auditoría (afirma sobre México)

**Unidad:** defunción, nunca persona encuestada; no se promedia con ninguna cifra de encuesta.
**Registro ≠ ocurrencia:** ola = año de registro; SUIC-OCURRIDO-EN-OLA dice cuánto difiere.
**Subregistro y clasificación:** un suicidio clasificado como accidente o causa mal definida no
entra; CIE y presunto pueden discrepar (diagnóstico). **Sin tasas:** un conteo creciente no es una
tasa creciente. **Cifra escrita a mano:** ninguna.

El primer resultado que produzca este procedimiento es el que se reporta.
