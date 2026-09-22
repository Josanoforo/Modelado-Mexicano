# ENIGH2016-REMESAS-CONTEXTO · especificación humana, generalización por ola v1.0

Generalización, parametrizada por ola, de `CALC-ENIGH2022-REMESAS-CONTEXTO-0001`
(`spec.md` sellado, sha256 `12e8312359ccde2185c3d80244bdecea41cdda556e3bcf526952ba7fea69b8ff`), congelada en
`ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, P1. Fecha de congelamiento: 21/sep/2026.

## 1. Qué cambia y qué no cambia frente a 2022

Contrato estadístico idéntico a `CALC-ENIGH2022-REMESAS-CONTEXTO-0001` — ver
ese `spec.md`. Verificado por comando: el medidor generalizado, corrido sobre
2022, reproduce exacta (JSON canónica idéntica) la tabla por perfil y los
contrastes sellados de `CALC-ENIGH2022-REMESAS-CONTEXTO-0001/resultados.json`
— test de regresión en `tests/test_enigh_serie_oro.py`.

**Único cambio declarado:** `controles_nacionales.prevalencia` ya no es el
valor 2022 (`0.04569409956405095`), sino el valor YA SELLADO de la ola 2016
en `CALC-B-0001/resultados.json` (`RESULT-B-ENIGH-2016-P = 0.04745859252351374`). Las
categorías `tam_loc`/`est_socio` y sus contrastes (`tam_loc=4 menos
tam_loc=1`; `est_socio=1 menos est_socio=4`) se heredan de 2022 con la misma
limitación de codebook declarada en
`CALC-ENIGH2016-PERFIL-ESTRUCTURAL-0001/spec.md §1`.

## 2. Corte de serie

Ver `CALC-ENIGH2016-PERFIL-ESTRUCTURAL-0001/spec.md §2`.

## 3. Fuentes documentales

- `enigh2016_nc_csv`, 40,991,826 bytes, SHA-256 `95e30780dfff83305fd1293945a0a5ed04c4e4daed4b0d45b66343db09e8eca1`.
- `CALC-B-0001/resultados.json`, SHA-256 `87e20e5aa2923fcc4b206734fa13ec321d3b036d61edd48eb0efd5bd369f263d` (control nacional,
  ola 2016).

## 4. RESULT

Mismos 11 RESULT de `CALC-ENIGH2022-REMESAS-CONTEXTO-0001`, prefijo
`RESULT-ENIGH16-REMCTX-` en vez de `RESULT-ENIGH22-REMCTX-`.

## 5. Interpretación y reservas

Igual que el sellado 2022: incidencia en hogares y monto/intensidad contable
condicional entre receptores; transversal, descriptivo y no causal.
`cuenta_gen2` queda `PENDIENTE-DE-MESA`.
