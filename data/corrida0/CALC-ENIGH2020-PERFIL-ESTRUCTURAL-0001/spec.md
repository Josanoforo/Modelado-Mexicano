# ENIGH2020-PERFIL-ESTRUCTURAL · especificación humana, generalización por ola v1.0

Generalización, parametrizada por ola, de `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003`
(`spec.md` sellado, sha256 `c820e67a6d7740765ffdc606c550574a4a77d0e86d4ababaf7d99bf852eb625e`), congelada en
`ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, P1 ("las series de ENIGH se construyen
sobre olas abiertas"). Fecha de congelamiento: 21/sep/2026. Esta versión se
congela antes de correr `tools/corrida0.py run` sobre esta ola en esta sesión
(el generador y su oro-check corrieron en scratch, fuera del árbol, antes de
escribir este archivo; el árbol nunca abrió microdato antes de este commit).

## 1. Qué cambia y qué no cambia frente a 2022

El contrato estadístico completo (universo, exclusiones, categorías,
producto cartesiano, método de precisión, semilla, RESULT) es **idéntico** al
de `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003` — ver ese `spec.md` para la
prosa completa, no se repite aquí. Verificado por comando: el medidor
generalizado, corrido sobre 2022, reproduce byte a byte (sha256 exactos) las
tres tablas selladas de `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003/resultados.json`
(`P1-MARGINALES-SHA256`, `P2-CONJUNTA-SHA256`, `P2-MARGINALES-COMPLETOS-SHA256`)
— test de regresión en `tests/test_enigh_serie_oro.py`.

**Único cambio sustantivo, declarado (D-19: toca código de un procedimiento
que no estaba congelado, es la propia generalización que este acto pide):**
en `poblacion.csv` de la ola 2020, las columnas `factor`, `est_dis` y `upm`
**no existen** (verificado contra el header real del zip: ausentes en
2020/2018/2020, presentes en 2022 y 2024). En 2022 se comprobó — muestreando
500 hogares, 1667 personas — que `poblacion.factor` y `poblacion.(est_dis,upm)`
son **idénticos, byte a byte, cero discordancias**, a `concentradohogar.factor`
y `concentradohogar.(est_dis,upm)` de la misma llave hogar: INEGI simplemente
copió las variables de diseño del hogar a la tabla de personas desde esa ola
en adelante, sin cambiar el diseño. Para 2020, este medidor toma esas tres
columnas de `concentradohogar` por `(folioviv, foliohog)` — matemáticamente
la misma operación que 2022 ya hacía de forma nativa, no un cambio de método.

**Limitación declarada, no un supuesto silencioso:** las categorías nativas
(`segsoc`, `tam_loc`, `est_socio`, `celular`, `conex_inte`) se citan contra la
Descripción de la base de **2022**, porque el corpus no trae un descriptor
propio de la ola 2020 (`enigh2020_descripcion_base_pdf` NO EXISTE en
`data/manifiesto.yaml`; verificado por grep, universo=todo el archivo). Se
ASUME continuidad de codificación dentro de la ventana "nueva serie"
2016–2022 (mismo corte de serie que excluye 2012/2014, ver `## 2` de este
documento) — no verificada independientemente contra un codebook propio de
2020. Si un acto futuro trae el descriptor de 2020, esta asunción se
verifica o se retira.

## 2. Corte de serie 2012/2014 vs 2016+ (premisa de todo P1, no solo de esta pieza)

`data/manifiesto.yaml`: `enigh2012_nc_csv`/`enigh2014_nc_csv` tienen
`url_origen` con el patrón `enigh_ncv_<año>_csv.zip` ("NCV" = nueva
construcción de variables, metodología anterior); `enigh2016_nc_csv` en
adelante (2016/2018/2020/2022/2024) tienen el patrón
`..._nueva_serie_csv.zip` / `..._ns_csv.zip` ("NS" = nueva serie). Confirmado
también por `RESULT-BM-ENIGH-2014-METADATO-VERSION` (`CALC-B-MARCO-ENIGH-0001`,
sellado): `identifier=MEX-INEGI.40.202.03-ENIGH-2014-NCV`. La ventana de este
acto es 2016–2022 (2024 reservada por `#964`); 2012 y 2014 quedan fuera por
metodología distinta, no solo por tamaño de muestra (aunque también salta de
n=19 479 en 2014 a n=70 311 en 2016).

## 3. Fuentes documentales acreditadas de esta ola

- `enigh2020_nc_csv`, 93,711,908 bytes, SHA-256 `47417cac13da7dce3a710d86c5767564101086a51666ec674acf27740e0701d4`.
- Categorías y roles de variable: heredados de `enigh2022_descripcion_base_pdf`
  (SHA-256 `7b0c4e6bd36ceb9eae7cc852fce5a38dbcf4f2da6b133d35df6b1443fc76836c`),
  con la limitación declarada en `## 1` arriba.

## 4. RESULT

Mismos 32 RESULT de `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003`, prefijo
`RESULT-ENIGH20-PERFIL-` (2 dígitos de año, misma convención que el
sellado 2022 usa: `RESULT-ENIGH22-PERFIL-`) en vez de `RESULT-ENIGH22-PERFIL-`.
`residencia`
sigue `NO-ESTIMABLE-POR-DEFINICION-NO-ACREDITADA`, ahora con evidencia
adicional de que 2020 tampoco tiene descriptor propio en el corpus para
resolver la ambigüedad.

## 5. Interpretación y reservas

Igual que `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003 §7`: composición estructural
descriptiva de personas en hogares de México, ENIGH 2020. No identifica
psicología, cultura, conducta ni causalidad. `cuenta_gen2` queda
`PENDIENTE-DE-MESA`.
