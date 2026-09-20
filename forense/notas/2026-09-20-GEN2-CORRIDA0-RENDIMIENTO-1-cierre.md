# Nota de cierre — ACTO GEN2-CORRIDA0-RENDIMIENTO-1

**Salidas byte-idénticas: SÍ.** Las seis invocaciones del arnés de oro
(`status`, `status --json`, `demanda`, `registro`, `registro --fuentes`,
`registro --escribe`) producen exactamente los mismos bytes de `stdout`,
`stderr`, el mismo código de salida, las mismas huellas sha256 de los veinte
TSV derivados de `data/corrida0/` y el mismo contenido en los dos TSV que
`demanda` reescribe. **Ningún contador se movió por el cambio de código**, y
se dice con precisión: con **sólo** `tools/corrida0.py` modificado, `status`
es byte-idéntico al arnés — los quince campos. Ya con la cascada de cierre
encima, `status` difiere en **un** campo y **uno solo**,
`no_corrido_abiertas` 132 → 133, que es `NC-0385` — la fila que este mismo
acto abre y que A.14 obliga a asentar. Los otros catorce campos siguen
idénticos. No es PARO: es el asiento del acto contándose a sí mismo, no una
derivación que se movió. El diff completo, verbatim:

```
13c13
< no_corrido_abiertas=132
---
> no_corrido_abiertas=133
```

## La tabla

Mediana de tres repeticiones cada una, mismo entorno, misma copia del árbol
en `adcfa978` fuera del árbol de trabajo (sólo se intercambia
`tools/corrida0.py`). **ENTORNO: NUBE**, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`,
`nproc = 4`, Python 3.11.15, corpus NO montado (`archivos_examinados=0`,
este acto no abre microdato). Las cifras absolutas de dirección venían de un
entorno de 1 CPU y no viajan; las razones sí.

| tarea | antes (`adcfa978`) | después | Δ |
|---|---|---|---|
| `corrida0.py status` | **70.94 s** | **22.45 s** | **−68.4 %** |
| `corrida0.py demanda` | 12.50 s | 12.57 s | +0.6 % (sin cambio, ver abajo) |
| `tests/test_corrida0.py` | **184.06 s** | **75.58 s** | **−58.9 %** |
| `tests/check.py --baseline --parallel` | **415.86 s** | **197.96 s** | **−52.4 %** |

Dentro de la suite, por test cronometrado: `T32 T-CORRIDA0` 181.99 s → 74.87 s
(−58.9 %) y `T35 T-REPRO` 76.19 s → 22.22 s (−70.8 %).

**`demanda` no mejora y eso es un hecho, no un descuido.** `demanda` no pasa
por `_lee_oferta`/`_propaga_envuelto`: deriva de los TSV de demanda, no del
universo de specs. Ninguna de las piezas de este encargo la toca. Si se
quiere barata, es otro acto con otro perfil.

**Contra el defecto que motivó el encargo.** `cierre_acto.py` corre la suite
con un límite interno de 300 s: con 415.9 s salía 124 (tiempo agotado, no
ROJO) — eso es `NC-0357` literal. Con 198.0 s cabe, con margen, dentro de ese
límite y dentro de los `timeout-minutes: 10` del CI. El acto no cambió el
límite: cambió lo que hay que caber en él.

## Lo que se midió antes de optimizar (y lo que corrigió a dirección)

La hipótesis del encargo era que `_propaga_envuelto` y `_verifica_sello`
concentran el 85 %, y que dentro del primero manda la repetición de
`_funcion_de_dependencia`. La repetición **existe y es mayor de lo dicho**,
pero **no era lo caro**. Contado en este entorno instrumentando el módulo
sin tocarlo (`_filas_registro()` completo, `adcfa978`):

| nodo | llamadas | distintos | factor de repetición |
|---|---|---|---|
| `_funcion_de_dependencia` | 273 385 | 1 653 tuplas `(funcion, origen, id, ruta)` | **165.4×** |
| `_referencias_numericas_de_intermediario` | 219 134 | 947 rutas | **231.4×** |
| `_verifica_sello` | 315 | 164 directorios | 1.9× |

`_propaga_envuelto` se llama **una** vez, y su memo por `(calc_id, resultado)`
**ya existía** desde antes de este acto (`corrida0.py:3598`): la pieza P2 tal
como estaba escrita («que cada `(calc_id, resultado)` se resuelva una vez»)
ya estaba hecha. Lo que no estaba hecho es el nivel de abajo. `cProfile` sobre
`_filas_registro` puso el dedo donde dolía: **183 s de 197 s dentro de
`_yaml_safe_load`**, 13 125 llamadas, casi todas desde
`_referencias_numericas_de_intermediario` — que **sí** tenía cache
(`lru_cache(maxsize=256)`) pero con el techo por debajo de su propio universo:
947 rutas distintas contra 256 ranuras, y un orden de recorrido que lo hace
thrashear entero. `cache_info()` al terminar: `hits=206337, misses=12797`.
**12 797 fallos donde debía haber 947**, es decir 13.5 parseos de YAML por
archivo en vez de uno.

Ese es el hallazgo: el cache no faltaba, estaba mal dimensionado, y un cache
mal dimensionado es indistinguible de ningún cache salvo que se mire el
`cache_info()`.

## Qué entró, qué se revirtió, y con qué cifra

Ablación **leave-one-out** sobre `status`, mediana de tres, mismo entorno.
La ganancia marginal es la que decide: es lo que cuesta quitar esa pieza del
artefacto final, no lo que aporta sola sobre un árbol que ya no existe.

| variante | mediana | ganancia marginal de la pieza ausente | veredicto |
|---|---|---|---|
| `adcfa978` sin tocar | 71.52 s | — | base |
| las tres piezas | 20.57 s | — | — |
| sin P1 (`_funcion_de_dependencia`) | 22.28 s | **7.7 %** | **< 10 % → REVERTIDA** |
| sin P2 (techo del cache de intermediarios) | 58.66 s | **64.9 %** | entra |
| sin P3 (`_verifica_sello` en proceso) | 31.32 s | **34.3 %** | entra |

Las cinco variantes dan `status` byte-idéntico al arnés. **P1 se revirtió**
tal como el encargo manda: 1.7 s de 22.3 s no pagan una función cacheada
extra y un dict reconstruido por llamada. La razón de que no pague es la
misma que el perfil: una vez que P2 quita el sobre-parseo de YAML, las
273 385 llamadas son baratas. La cifra y el argumento quedan escritos en el
docstring de `_funcion_de_dependencia`, para que quien vuelva a proponerlo
sepa qué tiene que mover.

**Lo que quedó en el árbol, íntegro:**

- **P2** — `_referencias_numericas_de_intermediario`: `maxsize` 256 → 4096,
  por encima de las 947 rutas del universo. No cambia la semántica (función
  pura de la ruta, ya cacheada de proceso desde antes); deja de tirar lo que
  va a volver a pedir. No es cache en disco ni índice persistente (D-14):
  vive y muere con la invocación.
- **P3** — `_verifica_sello`: `subprocess.run` → `sella_sha256.verifica()`
  importada en proceso, mismo patrón que `_PR` ya usaba en el mismo archivo.
  **`tools/sella_sha256.py` NO se tocó**: `verifica()` ya era función pura de
  sólo lectura que devuelve `(codigo, mensaje)` con los mismos tres códigos
  que su CLI (`0` COINCIDE · `2` SIDECAR_AUSENTE · `3` NO_COINCIDE), así que
  P3 resultó ser una importación, no una refactorización. La CLI queda
  intacta, byte por byte. **Los tres estados de A.1 no se colapsan:**
  `AUSENTE` lo sigue decidiendo la rama de arriba (sin `sello.sha256`), y
  raíz-no-configurada / hash-discordante siguen saliendo de los códigos de
  `verifica()`. Una excepción se reporta como el CLI la habría reportado —
  un exit distinto de cero — nunca un COINCIDE piadoso. Los otros tres
  `subprocess.run` contra `sella_sha256.py` (`:1738`, `:1962`, `:2082`) NO se
  tocaron: están fuera del perímetro.

## P0 — la red de seguridad, sellada antes de tocar nada

`tests/test_corrida0_oro.py`, primer commit del acto (`03dc7b9`), antes de
cambiar un byte de `corrida0.py`. Sella y coteja, por invocación: `stdout`,
`stderr`, código de salida, sha256 de los veinte TSV derivados tras la
corrida, y el **contenido completo** de los TSV que la invocación reescribe.

**Determinismo (el encargo exige PARO si no lo hay): no hay PARO.** Dos
repeticiones de las seis invocaciones contra una copia de `adcfa978` fuera
del árbol: idénticas en los cuatro ejes. **Control:** el árbol sin tocar,
cotejado contra el arnés sellado desde esa copia, VERDE 6/6 — el arnés
detecta lo que debe y no grita por lo que no.

El arnés **no usa `git checkout` para restaurar**: relee a memoria los bytes
de los veinte TSV antes de cada invocación y los repone después, así que un
árbol sucio termina igual de sucio. Esto importa porque **`demanda` escribe**:
reescribe `demanda-corridas.tsv` y `demanda-resultados.tsv` cada vez que
corre. En `adcfa978` esos dos archivos están desfasados respecto de lo que
`demanda` deriva hoy (un `demanda` limpio los modifica). Eso es deriva
preexistente de `main`, fuera de este perímetro, y va a `NC-0385`; este acto
lo detectó porque el arnés lo obligó a mirar, y lo restauró sin tocarlo.

El arnés **no corre en `check.py`** y no debe: su referencia pesa >15 MB de
TSV derivados que cambian con cada acto que sella una corrida. Congelarla en
el repo sería una segunda copia del registro que caduca sola. Sin
`CORRIDA0_ORO` el test sale `SALTADO-SIN-ARNES` y lo dice con la receta de
tres líneas para sellarlo — nunca VERDE por omisión.

## P5 — refutada por medición, no diferida por pereza

P5 (que `--parallel` solape también `T32`, hoy sólo `T35`) **no se
implementó, y la razón es una cifra.** El pool consume cada resultado en la
posición original del test, así que lo que `T32` puede solapar está acotado
por lo que corre **antes** que él. Medido sobre el log cronometrado de la
suite ya optimizada: los tests que preceden a `T32` suman **3.93 s** de
197.96 s. El techo de la ganancia es **2 %** — por debajo del 10 % que el
propio encargo fija, y a cambio de tocar el contrato de orden de la suite.
Además `T16` ya lanza una corrida completa de la suite como hijo, así que las
4 CPU no están ociosas durante `T32`. Se anota como `NC-0386` con la cifra,
no como deuda viva.

## Auditoría de rigor extremo

No aplica: este artefacto no afirma nada sobre México. Mide tiempos de un
CLI y compara bytes. Contadores movidos **por el cambio de código: cero, y es
el diseño** — mover uno habría sido el fallo. El único campo de `status` que
cambia en el árbol final es `no_corrido_abiertas` (132 → 133), y lo mueve la
fila `NC-0385` que A.14 obliga a asentar, no la optimización.

## NO-CORRIDO / RESERVAS

Ver `## NO-CORRIDO / RESERVAS` abajo y `forense/no-corrido.tsv`
(`NC-0384`–`NC-0386`).

## Falsador a tres meses (20/dic/2026)

Si `NC-0357` o un «suite sin veredicto» reaparece, esta mejora no resolvió el
defecto y se anota aquí. Señal de que sí sirvió: `cierre_acto.py` cierra
dentro de sus 300 s sin que nadie amplíe el límite a mano.
