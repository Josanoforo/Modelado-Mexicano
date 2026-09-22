# ACTO GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1 · nota de cierre

22/sep/2026 · CAJA (Ubuntu/WSL2, `ENTORNO-DERIVADO = CAJA`, `sin_variable`, corpus montado
`archivos_examinados=436`, red 200) · Opus · MODO RÍGIDO desde COMMIT-1 · encargo
`forense/encargos/2026-09-22-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1.md` (0-bis `286889ee`,
sello de cuerpo `8b46cbab…`) · ADR `ADR-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-01`.

**Contadores:** +1 corrida sellada y registrada (`CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001`,
1125 RESULT, `cuenta_gen2 = SI` por etiqueta de la spec, `verify` REPRODUCE/IDENTICO,
asiento en `replay-evidencia.tsv`); `N_corridas_selladas = 155` tras el registro. No adopta;
`celdas_validadas` no se mueve (RETROSPECTIVA-MECÁNICA).

## 1 · Qué se midió

Un intervalo de persistencia por celda para las 32 celdas ENIF que el árbitro evaluó
(`FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02`: el IC95 muestral del piso 2021 cubre R 2024 en
6/32 = 0.19 [0.09, 0.35]). La regla, congelada en COMMIT-1 (`e1310d86`, spec
`forense/prereg-caja/ENIF-PERSISTENCIA-IC-CALIBRADO-spec-v1_0.md` §4) antes de abrir 2015/2018:
IC = expit(logit p2021 ± 1.959964·√(ee_muestral² + τ²_g)), con τ²_g la media **sin centrar**
de (logit h2021 − logit h2018)² sobre las celdas del grupo desenlace × eje, en el universo
18-70 y con el constructo armonizado (D9 medido como D8: sin la vía formal «Internet o
aplicación», que 2018 no pregunta).

**Todo lo de abajo es RETROSPECTIVA-MECÁNICA** (R 2024 ya vista; una sola regla, sin variante).
No se mezcla con la cobertura PROSPECTIVA de ningún piloto.

## 2 · Resultado (sellado)

| agregado | N | dentro | cobertura | Wilson por celda | Wilson por conglomerado (n=12) |
|---|---|---|---|---|---|
| GLOBAL ENIF | 32 | 32 | **1.00** | [0.893, 1.000] | [0.758, 1.000] |
| D9 (ahorra sólo informal) | 16 | 16 | 1.00 | [0.806, 1.000] | — |
| informal cualquiera | 16 | 16 | 1.00 | [0.806, 1.000] | — |

- Control: el mismo cotejo con el IC muestral sellado da **6/32 — COINCIDE** con el árbitro.
- ORO: el conducto 2021 18+ nueve vías reproduce los 32 pisos sellados a |Δ| = 0 (P, IC, N).
- `REGLA-X-LECTURA-MECANICA = CUMPLE` (cobertura ≥ 0.80 y Wilson por conglomerado ≥ 0.50).
- `verify` aislado: REPRODUCE / IDENTICO, 1125/1125 (8 nulos declarados: el τ² descriptivo
  «con 2015» de los 8 grupos donde 2015 no es comparable).

## 3 · Hallazgo — por qué cubre, y cuánto cuesta

**El intervalo cubre porque es ancho.** Ancho mediano **35 pp** (29.1–39.7), **8.9 veces** el
IC muestral (6.6–12.0). El error que tenía que cubrir, |R2024 − piso2021|, es de 2.7 pp de
mediana y 5.2 pp de máximo. τ ≈ 0.37–0.43 logit en los 12 grupos, y es casi idéntica a |Δ
medio| (ruido muestral ≈ 0.003 logit): el cambio 2018→2021 fue **un solo choque común** —
entre −0.21 y −0.50 logit, **negativo en las 32 celdas** (el ahorro informal cayó en todos los
segmentos). Doce grupos no son doce observaciones independientes del cambio: son la misma
observación vista doce veces. El cambio 2015→2018 (descriptivo, 12 celdas de informal) fue
chico y de otro signo: −0.01 a +0.15 logit; el τ² «con 2015» baja a la mitad (0.08–0.09 vs
0.15–0.18). El 2021→2024 fue de −0.23 a +0.22 logit.

Lectura: con dos olas de cambio y una de ellas atípica, el τ² empírico calibra al peor
trienio observado. Cumple la regla fijada antes del dato (y esa regla no se toca), pero su
precio es un intervalo de ~35 pp alrededor de cada piso. Eso va con la FP, no se esconde.

## 4 · Premisas del encargo que cayeron (logística; declaradas, no PARO)

1. `[EXISTE] enif2015_csv` — el manifiesto no tiene ese id; 2015 es `enif_2015_enif_2015_bd_dbf`.
2. «Lee los marginales 2024 sellados del yaml» — R se leyó del CALC GEN2
   `CALC-ARBITRO-MARGINALES-ENIF2024-0001` (el árbitro midió que el yaml no discrepa a 4.95e-7;
   leer `milpa/` volvería la corrida legacy). ENIF 2024 no se abrió.
3. `[SUPUESTO]` comparabilidad por texto 2015/2018/2021 — falsa en parte, y la tabla sellada
   `data/ahorro-comparabilidad-texto-v1_0.tsv` ya lo decía: D9 no existe en 2015 y en 2018 sólo
   como D8; formalidad y cuenta 2015 son cambio de instrumento. 2015 comparable en 12/32.
4. `[SUPUESTO]` «dos cambios por celda» — sólo hay uno usable (2018→2021) en la rama elegida.
5. Compuerta §8 «no hay otro acto de caja en vuelo» — **falsa al abrir**:
   `GEN2-PENDIENTES-CAJA-1` (rama `claude/gen2-pendientes-caja-1`, 0-bis 19:38 UTC) y
   `GEN2-MARGINALES-ADOPCION-1` (cerrando) estaban vivos. Protege **borrar** (D-20): este acto
   no borró nada; se siguió y se declara.

## 5 · Pregunta a mesa (encargo §6), respondida provisionalmente con la recomendación

«2015 no es comparable por texto en 20 de 32 celdas. ¿Calibrar sólo con 2018→2021
(recomendado) o esperar?» — COMMIT-1 congeló la recomendada. Sin respuesta de mesa al cerrar:
fila NC `DECISIÓN-DE-MESA-PENDIENTE`. Mezclar 2015 donde es comparable sería una segunda
variante con R vista; no se evaluó (su τ² queda sólo como descriptivo).

## 6 · Vistas derivadas: qué más cambió al registrar (medido, no supuesto)

`registro --verifica --escribe --lote CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001`, comparado
contra `origin/main` (31da26e0) excluyendo las filas propias: `usos.tsv` IDÉNTICO.
`corridas.tsv`: +21 corridas ajenas **ya selladas en main sin fila** (ARBITRO-MARGINALES-2 ×3,
DIN-CREDITO-PREDICCION-2024 ×2, DIN-CREDITO-PISOS-ENIF2021-RECORTE1870, DIN-CREDITO-K2-BANCARIA-
HISTORIA, DIN-LOTE-ENIF2024 ×2, ENIGH-DUELO ×3, ENIGH2016/2018/2020 ×9); las 3 filas
`SPEC-FIJADA` de K2-BANCARIA y DIN-LOTE-ENIF2024 pasan a sus corridas selladas;
`motivo_cuenta_gen2` en 17 filas (lee filas de mesa ya en `decisiones.tsv`); `fuente_replay`
en 4 (asientos aislados ya en main); 3 filas ENIGH2022 pasan a `SUPERADO→…2020` (regla ajena
del registro). **Ningún `resultado_replay`/`contexto_replay` previo cambió.** `resultados.tsv`:
las filas de esas mismas corridas. Es proyección pendiente de otros actos, no decisión de éste;
de las 21 nuevas, 4 entran `REPRODUCE` (tienen asiento) y 17 `NO-VERIFICADO` (su E.7 es de
sus actos / `GEN2-PENDIENTES-CAJA-1`).

## 7 · Reservas

- `envuelto_legacy` y `origen_numerico` salen `INDETERMINADO` en la fila propia (inputs repo
  METADATO que citan CALC por id). `cuenta_gen2 = SI` por etiqueta. Spec congelada: no se edita.
- El test `tests/test_enif_persistencia_ic_calibrado.py` necesita numpy/pandas/yaml: en CI se
  censa como huérfano con dependencia pendiente (misma clase que sus hermanos).

Auditoría de rigor: no aplica (calibra el aparato; las cifras sobre México ya estaban selladas).

## 8 · Enmienda de cierre (CI de #1009, mismo día)

El commit de registro (`7fc4e115`) llevó `data/corrida0/corridas.tsv` y `resultados.tsv` al PR.
CI lo rechazó: `enrutamiento-pr` («Ningún PR toca un archivo DERIVADO — NO EDITAR», firma de
mesa 21/sep §2(2): los derivados los re-deriva y commitea el job del push a `main`) y, por
arrastre, `guardas-res` G5 (las filas ENIGH2016/2018/2020 ajenas que la re-derivación proyectó
citan RES sin fila en la tabla de citas). Corrección: las dos vistas se restauran a
`origin/main`; el asiento de replay (`forense/replay-evidencia.tsv`) sí viaja. Lo de §6 queda
como medición de lo que el job de `main` proyectará, no como cambio de este PR;
`NC-…-2868-04` se cierra por eso.
