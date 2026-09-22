# ENIGH2016-INTENSIDAD-REMESAS · especificación humana, generalización por ola v1.0

Generalización, parametrizada por ola, de `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`
(`spec.md` sellado, sha256 `e3e845dbc94b6834594f4aeeb4ea1e3d475ecf15ef3d47e8e3228d27a7e7195c`), congelada en
`ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, P1. Fecha de congelamiento: 21/sep/2026.

## 1. Qué cambia y qué no cambia frente a 2022

Contrato estadístico idéntico a `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001` — ver
ese `spec.md`. Verificado por comando: el medidor generalizado, corrido sobre
2022, reproduce exactos (point estimates y bootstrap IC bit a bit, mismo
`numpy.random.Generator(PCG64)` con la misma semilla) los 11 valores
principales sellados de `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001/resultados.json`
— test de regresión en `tests/test_enigh_serie_oro.py`.

**Único cambio declarado:** el control de prevalencia contra el "padre" ya no
usa `prevalencia_padre: 0.04569409956405095` (el valor 2022 de
`CALC-ENIGH-0001`), sino el valor YA SELLADO de la ola 2016 en
`CALC-B-0001/resultados.json` (`RESULT-B-ENIGH-2016-P = 0.04745859252351374`, sobre
n=70311 hogares) — la misma serie `remesas>0` que el propio encargo cita
como el único estimando de ENIGH que ya pasa la regla de entrada en ≥3 olas.
`tolerancia_prevalencia` se mantiene en `1e-10`: este control no es un
oro contra 2022 sino una prueba de consistencia interna entre dos medidores
independientes (`CALC-B-0001`, sellado antes de este acto, y este medidor) que
deben coincidir exactamente sobre la MISMA columna `remesas` del MISMO archivo.

## 2. Corte de serie

Ver `CALC-ENIGH2016-PERFIL-ESTRUCTURAL-0001/spec.md §2` (mismo hallazgo,
no se repite: ventana 2016–2022, 2012/2014 excluidos por metodología NCV).

## 3. Fuentes documentales

- `enigh2016_nc_csv`, 40,991,826 bytes, SHA-256 `95e30780dfff83305fd1293945a0a5ed04c4e4daed4b0d45b66343db09e8eca1`.
- `CALC-B-0001/resultados.json`, SHA-256 `87e20e5aa2923fcc4b206734fa13ec321d3b036d61edd48eb0efd5bd369f263d` (control de prevalencia
  padre, ola 2016).

## 4. RESULT

Mismos 45 RESULT de `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`, prefijo
`RESULT-ENIGH16-REMINT-` en vez de `RESULT-ENIGH22-REMINT-`.

## 5. Interpretación y reservas

Igual que el sellado 2022: cinco descriptores entre receptores, participación
estrictamente contable, transversal y no causal. No estudio ciego ni
confirmatorio (se conocía el valor sellado de prevalencia antes de correr).
`cuenta_gen2` queda `PENDIENTE-DE-MESA`.
