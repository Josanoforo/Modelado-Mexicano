# ACTO GEN2-CORRIDA0-CASCADA-POST-682 · cierre de NC-0145

**Base:** `origin/main = 09149bc` (merge de PR #682).  
**Entorno:** CAJA, `data/raw` montada.  
**Encargo:** `forense/encargos/2026-09-10-GEN2-CORRIDA0-CASCADA-POST-682.md`.

## VEREDICTO NC-0145

`PARO`. Las discrepancias son transiciones reales y legítimas de tres fuentes
vivas, no mutaciones de una pieza histórica que pueda restaurarse sin degradar
otra corrida o retirar estado vigente. No se recalculó ni re-selló ningún
`CALC`; no cambió ningún valor sellado y no se tocó `milpa/`.

| CALC | estado publicado | estado proyectado | input discrepante | hash sellado | hash actual | commit que lo cambió | clase | acción |
|---|---|---|---|---|---|---|:---:|---|
| `CALC-C0D-MARCADOR` | `REPRODUCE / IDENTICO` | `NO-REPRODUCE · CONTEXTO-DISTINTO / DISTINTO` | `IN-MANIFIESTO` (`data/manifiesto.yaml`) | `fadabe668e7af8897cca691ed8c1a688ee2c07c8fc996170d7041ccbf7df28a1` | `6c68e5afab94e81051bc202b86e0e5f39b3a16054f01f01ebb3e1f4e5f69b6a4` | `a2c6ca6` (`[ADQ] 2026-09-10`) | B | adjudicar la transición; conservar corrida y sello intactos |
| `CALC-C0D-MARCADOR-v2` | `REPRODUCE / IDENTICO` | `NO-REPRODUCE · CONTEXTO-DISTINTO / DISTINTO` | `IN-MANIFIESTO` (`data/manifiesto.yaml`) | `fadabe668e7af8897cca691ed8c1a688ee2c07c8fc996170d7041ccbf7df28a1` | `6c68e5afab94e81051bc202b86e0e5f39b3a16054f01f01ebb3e1f4e5f69b6a4` | `a2c6ca6` (`[ADQ] 2026-09-10`) | B | adjudicar la transición; conservar corrida y sello intactos |
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
esa transición ni toca una cuarta corrida.

Restaurar cualquiera de las tres rutas activas habría sido incorrecto:
`tools/emite_m.py` posterior está sellado por
`CALC-M-marco-M-sorteado-v1_3-ola-v2`; `milpa/tramite.yaml` contiene adopciones
firmadas posteriores; `data/manifiesto.yaml` es el registro vivo de
adquisiciones. La supuesta reparación degradaría otras identidades o retiraría
estado sustantivo vigente. Se adjudica B con la evidencia anterior.

## Compuerta de publicación y conteos

Comando intentado, sin `--force`:

```text
python3 tools/corrida0.py registro --verifica --escribe \
  --lote CALC-C0D-MARCADOR,CALC-C0D-MARCADOR-v2,CALC-M-marco-M-sorteado-v1_3,CALC-TRIADA-0001
```

La compuerta paró antes de escribir: además de las dos transiciones C0D y la
incorporación nueva de TRIADA detectó una cuarta corrida fuera del lote,
`CALC-ENCIG-0001`, cuyo estado publicado es
`REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` y cuyo estado proyectado,
después de la reparación de identidad de PR #682, es
`REPRODUCE / IDENTICO`. Es una mejora, no una degradación, pero el encargo
ordenó parar ante **cualquier** cuarta corrida. El registrador terminó con
`REPLAY-PISADO`, exit `1`, y confirmó `no se escribio ninguna vista`.

La derivación seca sigue dando `139` corridas y `2889` `RESULT`; las vistas
publicadas permanecen en `138` y `2630`, sin TRIADA, hasta que mesa decida si
autoriza añadir `CALC-ENCIG-0001` al lote explícito.

## NO-CORRIDO / RESERVAS

`DECISION-DE-MESA-PENDIENTE`: autorizar o rechazar que la cascada de
`NC-0145` incluya la transición positiva de `CALC-ENCIG-0001` ya causada por
PR #682, además de las tres corridas nominales y TRIADA. No hay otra
investigación pendiente. Este acto no repara `NC-0141`, `NC-0146`, `NC-0147`,
`NC-0148` ni ninguna otra NC.

## Verificación

- `CALC-ENCIG-0001`: `REPRODUCE / CONTEXTO=IDENTICO` al verificar, pero su
  vista sigue en el estado anterior por el PARO;
- `CALC-TRIADA-0001`: `REPRODUCE / CONTEXTO=IDENTICO`.
- las dos C0D: transición B explícita a
  `NO-REPRODUCE · CONTEXTO-DISTINTO / DISTINTO`;
- corrida M: conserva `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO`;
- TRIADA todavía no está en las vistas porque la compuerta no escribió;
- ningún `data/corrida0/CALC-*/resultados.json` cambió;
- `tests/check.py --baseline` se ejecutó aislando/restaurando los dos TSV de
  demanda que `NC-0141` reconoce como efecto lateral.
