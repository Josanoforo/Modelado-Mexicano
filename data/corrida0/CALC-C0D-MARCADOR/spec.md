# `CALC-C0D-MARCADOR` — el marcador GEN2: la pareada `L_SOLO ↔ L_CORPUS`

Cara **local** de la spec sellada `forense/prereg-caja/C0D-MARCADOR-spec-v1_0.md`
(`prereg-caja-C0D-MARCADOR`, sha256 `c249e3b2ad8efd64326dc4b65ca770ca20e0e7fdac78dc2696e84a9838c56bd9`).
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

- `L_SOLO` / `L_CORPUS` — media de `valor_extraido` sobre las réplicas no nulas de
  las 8 del brazo (`corridas-L/L-<id>-M__{L-solo,L+corpus}__NN.json`); `None` si
  las 8 son nulas. Regla verbatim de `agregado_v1_1._leer_l_variante`.
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

## 5 · Veredictos

`RESULT-C0D-VEREDICTO-PAREADA` ∈ {`NO-ESTIMABLE-POR-COBERTURA`, `CORPUS-ESTORBA`,
`CORPUS-AYUDA`, `NO-DISCRIMINA`} por la precedencia de §4 de la sellada.

`RESULT-C0D-ADJUDICACION-HALLAZGO` ∈ {`NO-ADJUDICA-POR-CONTROL`,
`EXPLICADO-POR-UNIVERSO`, `EXPLICADO-POR-METRICA`, `CONFIRMADO-CON-ALCANCE`,
`NO-ESTIMABLE-POR-COBERTURA`} por la precedencia de §5 de la sellada.

**Ninguna cifra de este CALC entra a un veredicto de regla (`T9`).**

**Frase de sello:** *el primer resultado que produzca este procedimiento es el que
se reporta.*
