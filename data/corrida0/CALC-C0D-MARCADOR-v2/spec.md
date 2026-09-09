# `CALC-C0D-MARCADOR-v2` — el marcador GEN2: la pareada `L_SOLO ↔ L_CORPUS`

**Sucede a `CALC-C0D-MARCADOR`**, que corrió contra la spec `v1.0` y **PARÓ por su
propia guardia** (`RESULT-C0D-ADJUDICACION-HALLAZGO = NO-ADJUDICA-POR-CONTROL`).
`repite_de: CALC-C0D-MARCADOR` es el campo que el código lee para derivar
`SUPERADO→` en `registro()` y lo único que autoriza repetir sus ids. Los bytes de
la corrida anterior quedan **INTACTOS**.

Cara **local** de la spec sellada `forense/prereg-caja/C0D-MARCADOR-spec-v1_1.md`
(`prereg-caja-C0D-MARCADOR`, sha256 `604008c7ae0d5f82e12bb8aacee39f73ae676c794d9c067de73b0e56ae3f40cd`).
Lo que este archivo dice, lo dice la sellada primero; si alguna vez discrepan, manda
la sellada. Congelado en el `COMMIT-1` de `ACTO GEN2-C0-D`, antes de calcular una
sola cifra.

## 1 · Qué mide

Sobre las **14 celdas** de `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv`
(todas `grado_DD = "P1 PUNTUA"`, todas `escala = binaria`), el error en puntos
porcentuales de cada corredor contra el patrón oro `R` de su celda:

```
err_pp(corredor, celda) = 100 * (punto − R)          [con signo]
```

y **la comparación pareada que el árbol no tenía**:

```
d_i = |err_pp(L_CORPUS, i)| − |err_pp(L_SOLO, i)|     [d_i > 0 = el corpus alejó]
```

media de `d_i` con IC95 por bootstrap de celdas, `seed = 42`, `replicas = 10000`,
`nivel_ic = 0.95`, con `generar_indices_bootstrap` / `derivar_seed_scope` /
`_cuantil_7` consumidos **desde los bytes verificados** de
`forense/prereg-duelo-v2/scoring-adv1-m3.py` — la misma maquinaria sellada del
duelo, no una reimplementación.

## 2 · De dónde sale cada punto

- `L_SOLO` / `L_CORPUS` — media de la columna `valor` de
  `forense/prereg-duelo-v2/L-extraido-v1_2.tsv` sobre las filas de ese
  `(id_celda, variante)` con `estado == "EXTRAIBLE"`; `None` si ninguna lo es.
  Regla verbatim de `agregado_v1_2._cargar_l_tsv_v1_2`, **que es la que corre**.
  `valor_extraido` de las capturas es `null` en las 224 por diseño; la spec `v1.0`
  citó la regla del módulo base y por eso su corrida PARÓ (`NC-0074`).
- `M` — `valor_punto` del archivo resuelto por el orden §16 de `MAESTRA38-M13`.
- `R`, `EE_R` — de `corridas-R/<id>.json` con `estado == "COMPUTADO"`.
- `B` — `RESULT-B-PERSISTENCIA-<ola>-P` y `RESULT-B-OPERATIVO-<ola>-P` de
  `CALC-B-0001`, citados por `corrida0_resultado_id`, **sólo** en `FAM-M-06`
  (ENIGH 2018) y `FAM-M-07` (ENIGH 2020) — §0.2 de la sellada.

## 3 · Las dos familias de `MAE_pp`, y por qué son dos

`agregado_v1_3.py` calcula el `MAE_pp` de cada corredor sobre **su propio**
subconjunto disponible. Este marcador emite eso (`MAE-MARGINAL-*`, que reproduce
D4) **y además** el `MAE_pp` sobre el **universo común** `U∩` —celdas con los
cuatro puntos— que es el único que A-bis 4 autoriza a comparar entre corredores
(`MAE-COMUN-*`). `RESULT-C0D-UNIVERSOS-IDENTICOS` dice si la distinción muerde.

## 4 · Guardias que PARAN o degradan, todas pre-declaradas

| guardia | condición | consecuencia |
|---|---|---|
| cobertura de la pareada | `n_LL < 10` | `NO-ESTIMABLE-POR-COBERTURA`; no adjudica |
| convergencia con el agregado | punto `L` re-derivado ≠ el de `agregado-v1_3-resultado.json` (tol `1e-9`) | `DIVERGE`; §5.4 manda y precede a todo |
| conmensurabilidad de `B` | `|P_B_observada(ola) − R| > 1.96·EE_R` | `PISO-NO-CONMENSURABLE`; `B` no entra a comparación |
| `n` de `M ↔ B` | `n = 2` | se emite el par crudo, **sin IC**; `NO-ADJUDICA-POR-N` |
| correspondencia TSV ↔ capturas | una llave `(celda, variante, indice)` en uno y no en el otro | `DISCORDA`; PARA por la misma vía que el control de convergencia |
| conteo de filas del TSV | ≠ 224 | `AssertionError`: no es el TSV que la spec congeló |

## 5 · Veredictos

`RESULT-C0D-VEREDICTO-PAREADA` ∈ {`NO-ESTIMABLE-POR-COBERTURA`, `CORPUS-ESTORBA`,
`CORPUS-AYUDA`, `NO-DISCRIMINA`} por la precedencia de §4 de la sellada.

`RESULT-C0D-ADJUDICACION-HALLAZGO` ∈ {`NO-ADJUDICA-POR-CONTROL`,
`EXPLICADO-POR-UNIVERSO`, `EXPLICADO-POR-METRICA`, `CONFIRMADO-CON-ALCANCE`,
`NO-ESTIMABLE-POR-COBERTURA`} por la precedencia de §5 de la sellada.

**Ninguna cifra de este CALC entra a un veredicto de regla (`T9`).**

**Frase de sello:** *el primer resultado que produzca este procedimiento es el que
se reporta.*
