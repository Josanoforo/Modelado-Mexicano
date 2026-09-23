# Nota de cierre · ACTO GEN2-TUBERIA-LOTE-ESTRICTO-1

Encargo: `forense/encargos/2026-09-22-GEN2-TUBERIA-LOTE-ESTRICTO-1.md`.
Opción (a) de FP `…CANAL-PUBLICACION-1-7d98-01`, firmada.

## P1 · Medición previa (el drift real, sin escribir nada)

Con el `corrida0.py` de `main` (sin tocar), sobre el repo real, sin
`--verifica` y sin `--escribe` (lectura pura):

```
vistas = _filas_registro(verifica=False, verifica_ids=None)
_transiciones_replay(vistas["corridas"])   -> 26 campos, 13 corridas
```

Las 13 corridas: `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0001/-0002`,
`CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001`,
`CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001/-0002`,
`CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001`, `CALC-L-DESDE-CAPTURAS-v1_0`,
`CALC-PISO-PERSISTENCIA-ERROR-0001`, `CALC-PISOS-ENCIG2023-EJES-0001` (y
`-v1_1`), `CALC-PISOS-ENIF2021-EJES-0001`, `CALC-PISOS-ENVIPE2024-EJES-0001`,
`CALC-WBES2023-PRECISION-INTERACCIONES-0001`. Coincide en número (13) con lo
que `ADR-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01` ya midió con push
sintético — corroboración independiente, no una remedición nueva.

Con `_para_si_pisa_replay(vistas["corridas"], {"CALC-QUE-NO-EXISTE-AUN"})`
(nombrar la corrida NUEVA que traería un push real): el guardia SÍ dispara
citando las 13 — confirma el hallazgo del `[SUPUESTO]` §3 del encargo: la
causa no es un `--verifica` que reevalúa; es la vigencia del asiento
(`_evidencia_vigente`), que se re-chequea siempre, lote o no lote.

## P4 · Push sintético en rama (antes/después del fix)

Reproducido en un clon desechable (`/tmp/repro-lote-estricto`, nunca
publicado, borrado al cerrar), con un `CALC-LOTE-ESTRICTO-REPRO-0001`
sellado de verdad (`sella_sha256.py`) + una fila nueva en
`replay-evidencia.tsv`, exactamente como lo haría un push real. Se corrieron
las MISMAS líneas que el job del canal (`.github/workflows/verify.yml`):

```
LOTE="$(python3 tools/lote_desde_asientos.py "$ANTES" HEAD --csv)"
python3 tools/corrida0.py registro --verifica --escribe --lote "$LOTE"
```

**Antes del fix (P2)** — `corrida0.py` de `main`, sin tocar:

```
lote derivado: CALC-LOTE-ESTRICTO-REPRO-0001
PARO · REPLAY-PISADO (NC-0094): ... 13 corrida(s) AJENA(s) ... (26 campo(s))
no se escribio ninguna vista
EXIT=1
```
(idénticas a las 13 de P1 — log completo en la sesión, no se pega íntegro
aquí por tamaño).

**Después del fix (P2)** — mismo lote, mismo `ANTES`/`HEAD`:

```
lote derivado: CALC-LOTE-ESTRICTO-REPRO-0001
[avisos no bloqueantes, sin PARO]
EXIT=0
```

Verificado línea por línea: las 13 corridas de P1 quedan **BYTE A BYTE**
idénticas en `corridas.tsv` antes/después de este `--escribe --lote`
(comparación `grep` por `corrida_id`, las 13 `IGUAL`). `corridas.tsv` pasa
de 285 a 308 filas: 1 es la del lote (`CALC-LOTE-ESTRICTO-REPRO-0001`), las
27 restantes son corridas que YA estaban selladas en el árbol pero que
`corridas.tsv` de `main` nunca había publicado (backlog anterior a este
canal, no algo que este acto cause ni que le toque resolver: la doctrina
del lote es «una fila nunca antes publicada entra sola», y aquí entraron
27 de una vez porque el `corridas.tsv` publicado estaba desactualizado
frente al árbol de `data/corrida0/CALC-*/`). `resultados.tsv` estaba
publicado pero muy por detrás del árbol real (pasó de un puñado de filas a
~24 900): mismo fenómeno, mismo backlog. Ninguna de las dos cosas mueve un
veredicto ya publicado de una corrida ajena — que es lo único que
`REPLAY-PISADO`/este acto protegen.

Clon desechable borrado tras la medición (`rm -rf`); nunca se empujó ni se
mezcló con el árbol real.

## P2 · La bandera (implementación)

`tools/corrida0.py`: dos funciones nuevas (`_en_lote`, `_acota_vistas_al_lote`)
+ cuatro líneas de cableado dentro de `registro()`. **42 líneas netas**, no
≤ 30 (el número real, como autoriza el encargo): `_acota_vistas_al_lote`
tiene que congelar TRES vistas (`corridas`, `resultados`, `usos`) porque
`resultados.tsv`/`usos.tsv` cargan `fuente_replay` derivado del mismo
veredicto que `corridas.tsv` — congelar solo `corridas.tsv` habría dejado
`resultados.tsv`/`usos.tsv` de una corrida ajena con una `fuente_replay`
que no coincide con la fila congelada de `corridas.tsv`.

Sin bandera nueva: se cambió la semántica de `--escribe` cuando se da
`--lote` (recomendado en el encargo). No hay consumidor que dependiera del
comportamiento viejo (`--lote` nunca se usó junto con `--escribe` fuera del
job del canal, que es precisamente lo que esto arregla — cero llamadas a
`registro(..., lote=...)` en la suite antes de este acto).

## P3 · Tests

`tests/test_registro_lote_estricto.py` (4 casos, VERDE):
- A: `_acota_vistas_al_lote` directo — 3 corridas publicadas, una con
  drift; `--lote` con 1 corrida nueva → cambia exactamente 1 fila; el
  guardia no dispara.
- B: el mismo drift, SIN pasar por el acotamiento, SÍ dispara el guardia
  (contraprueba: A prueba la protección, no que el drift no exista).
- C: extremo a extremo con `registro(escribe=True, lote=...)` sobre un
  árbol demanda+oferta real (vía fixtures de `tests/test_corrida0.py`) —
  una corrida ajena editada a mano para simular drift queda preservada
  byte a byte; la corrida del lote entra.
- D: el acotamiento NO se pasa de largo — nombrar una corrida YA
  publicada en `--lote` sigue escribiendo su valor FRESCO (lo que el lote
  autoriza), no el publicado.

No se cableó un paso nuevo en `verify.yml` (la premisa del encargo de
"cablear en verify.yml como bloqueante" quedó SUPERADA por D-21, ya vigente
en v2.16: "su test nuevo entra a CI como huérfano (`ci_guardias
--ejecuta-huerfanos`) sin editar `verify.yml` ni `check.py`" — es logística,
no una firma de mesa, así que se replanteó y se declara aquí). Lo que sí se
hizo: `python3 tools/ci_guardias.py --censo` para registrar el archivo
nuevo en `forense/analisis/ci-guardias/censo-tests.tsv` (veredicto
`CORRE-EN-CI`, `cableado_hoy=NO`) — sin eso, `--ejecuta-huerfanos` habría
fallado con `NC-HUÉRFANA`/`tests sin fila en el censo`. El resto del diff
de ese TSV es reclasificación mecánica de los demás archivos (ruido de
`tiempo_seg` y un `test_consulta_gen2.py` que esta vez sí terminó a tiempo
y reveló un `AssertionError` preexistente y ajeno a este acto) — el archivo
está declarado `merge=union` (`ADR-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01`),
así que el ruido de una re-derivación concurrente no choca.

## Pregunta de mesa ya resuelta

`ADR-260922-GEN2-TUBERIA-CANAL-PUBLICACION-1-7d98-01` dejaba abierta:
"¿lote estricto en `corrida0.py` o un catch-up explícito primero?". Este
acto implementa la opción (a) (lote estricto), ya firmada en FP 7d98-01.
El catch-up del backlog observado en P4 (27 corridas + ~24 900 resultados
nunca publicados) NO es parte de este acto (fuera de perímetro): con lote
estricto, ese backlog se va publicando solo, un push a la vez, según cada
push traiga asientos nuevos — exactamente el diseño que opción (a) preveía.
