# ACTO GEN2-CORRIDA0-CASCADA-POST-682 · cierre de NC-0145

**Base:** `origin/main = 09149bc` (merge de PR #682).  
**Entorno:** CAJA, `data/raw` montada.  
**Encargo:** `forense/encargos/2026-09-10-GEN2-CORRIDA0-CASCADA-POST-682.md`.

## VEREDICTO NC-0145

`CIERRE`. Las discrepancias son transiciones reales y legítimas de tres fuentes
vivas, no mutaciones de una pieza histórica que pueda restaurarse sin degradar
otra corrida o retirar estado vigente. No se recalculó ni re-selló ningún
`CALC`; no cambió ningún valor sellado y no se tocó `milpa/`.

| CALC | estado publicado antes | estado publicado final | input discrepante | hash sellado | hash actual | commit que lo cambió | clase | acción |
|---|---|---|---|---|---|---|:---:|---|
| `CALC-C0D-MARCADOR` | `REPRODUCE / IDENTICO` | `NO-REPRODUCE · CONTEXTO-DISTINTO / DISTINTO` | `IN-MANIFIESTO` (`data/manifiesto.yaml`) | `fadabe668e7af8897cca691ed8c1a688ee2c07c8fc996170d7041ccbf7df28a1` | `6c68e5afab94e81051bc202b86e0e5f39b3a16054f01f01ebb3e1f4e5f69b6a4` | `a2c6ca6` (`[ADQ] 2026-09-10`) | B | transición publicada; corrida y sello intactos |
| `CALC-C0D-MARCADOR-v2` | `REPRODUCE / IDENTICO` | `NO-REPRODUCE · CONTEXTO-DISTINTO / DISTINTO` | `IN-MANIFIESTO` (`data/manifiesto.yaml`) | `fadabe668e7af8897cca691ed8c1a688ee2c07c8fc996170d7041ccbf7df28a1` | `6c68e5afab94e81051bc202b86e0e5f39b3a16054f01f01ebb3e1f4e5f69b6a4` | `a2c6ca6` (`[ADQ] 2026-09-10`) | B | transición publicada; corrida y sello intactos |
| `CALC-M-marco-M-sorteado-v1_3` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `IN-EMITE-M`; `IN-TRAMITE` | `196c2fc30a4b892e52117bcd8d521cf4c4ff8c2fd9801c0940d1588148edbf17`; `08bdda0bb3f8a6424d495f96f25839bf5df04f6a487649a28359f04cfa69ce86` | `ce4ca087ca299b0c9f583017c97bc4e2ec67071d3c5b1ea76f5fece028b0dfd4`; `213ca2bd26a0ba9f8cac3a9b37f37c09f4afd95f3df2f7e3fe9c8db223c34041` | `c0fe63d` (adenda de ola); `5d2e1cc` y adopciones posteriores hasta `21cad68` | B | conservar el estado histórico ya publicado; cero transición en la derivación post-#682 |

## Evidencia y decisión

Los blobs esperados existen en Git bajo las identidades que los sellaron:

- `data/manifiesto.yaml` en `aca0792` y `e6fe5ce` produce `fadabe66…`;
- `tools/emite_m.py` en `8f09149` produce `196c2fc3…`;
- `milpa/tramite.yaml` en `8f09149` produce `08bdda0b…`.

El manifiesto cambió en `a2c6ca6` sólo para añadir tres adquisiciones reales.
Por ello ambas C0D pasan a contexto distinto y su resultado
`RESULT-C0D-ALCANCE-PAYLOADS-POSTERIORES` pasa de `435` a `438`: no es una
reparación de identidad ni un cambio silencioso de las demás cifras.

`tools/emite_m.py` cambió en `c0fe63d` para instalar la adenda de mesa de ola
previa estricta y `ORIGEN-ARBITRO`; el propio commit declara que no cambia el
camino vigente de `emite_celda`. `milpa/tramite.yaml` cambió después por
adopciones firmadas (`5d2e1cc` y sucesoras). El replay actual confirma los 33
`RESULT` de la corrida M: resultado idéntico con contexto distinto.

La afirmación heredada de `NC-0145` de que esa tercera corrida pasaría a
`NO-REPRODUCE` **no se reproduce sobre `main` post-#682**. Tanto `verify`
individual como la derivación completa conservan
`REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO`; por eso el acto no inventa
esa transición. La única corrida adicional publicada es ENCIG, autorizada por
mesa como propagación mecánica de la restauración ya fusionada en PR #682.

Restaurar cualquiera de las tres rutas activas habría sido incorrecto:
`tools/emite_m.py` posterior está sellado por
`CALC-M-marco-M-sorteado-v1_3-ola-v2`; `milpa/tramite.yaml` contiene adopciones
firmadas posteriores; `data/manifiesto.yaml` es el registro vivo de
adquisiciones. La supuesta reparación degradaría otras identidades o retiraría
estado sustantivo vigente. Se adjudica B con la evidencia anterior.

## Compuerta de publicación y conteos

Comando ejecutado, sin `--force`:

```text
python3 tools/corrida0.py registro --verifica --escribe \
  --lote CALC-C0D-MARCADOR,CALC-C0D-MARCADOR-v2,CALC-M-marco-M-sorteado-v1_3,CALC-ENCIG-0001,CALC-TRIADA-0001
```

Mesa autorizó incluir `CALC-ENCIG-0001`: PR #682 ya había restaurado
deliberadamente su identidad histórica y la vista sólo conservaba el estado
anterior. Con las cinco corridas explícitas, la compuerta no detectó ninguna
sexta transición fuera del lote y escribió las vistas sin `--force`.

Conteos finales reales: `139` corridas, `2889` `RESULT` y `205` usos. TRIADA
queda incorporada con sus `259` `RESULT`; ENCIG propaga mecánicamente la mejora
a `REPRODUCE / IDENTICO`.

## NO-CORRIDO / RESERVAS

Sin reservas pendientes para `NC-0145`. La decisión de mesa autorizó la
propagación positiva de ENCIG y la publicación terminó correctamente. Este
acto no repara `NC-0141`, `NC-0146`, `NC-0147`, `NC-0148` ni ninguna otra NC.

## Verificación

- `CALC-ENCIG-0001`: `REPRODUCE / CONTEXTO=IDENTICO`, también en la vista;
- `CALC-TRIADA-0001`: `REPRODUCE / CONTEXTO=IDENTICO`.
- las dos C0D: transición B explícita a
  `NO-REPRODUCE · CONTEXTO-DISTINTO / DISTINTO`;
- corrida M: conserva `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO`;
- TRIADA está en `corridas.tsv` y sus `259` `RESULT` en `resultados.tsv`;
- ningún `data/corrida0/CALC-*/resultados.json` cambió;
- `tests/check.py --baseline`: línea base verde, con `3 FAIL` y `2218 WARN`
  heredados; los dos TSV de demanda que `NC-0141` reconoce como efecto lateral
  fueron aislados y restaurados.
