# Nota · `ACTO ENMIENDA-CUADRO-SORTEO` — propagación de hecho, `FP-146` → `sorteo-v2`

25/ago/2026. Entorno **NUBE** (`cloud_default`). Rama `claude/pack-nube-3-actos-w4v5j8`, `ACTO 3` de `PACK
NUBE-3`, corre después de los commits de `ACTO SELLA-G` y `ACTO ESCALAS-COMPLETAS-P1`.

## 0 · Qué es esto y qué NO es

`forense/notas/2026-08-25-indice-no-inegi.md` (`ACTO INDICE-NO-INEGI`, `PR #345`, mismo día que
`SORTEO-V2-PROPUESTA` pero fusionado después) resolvió las 8 filas `PENDIENTE-FUERA-DE-INDICE` que
`forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` §1 citaba como abiertas: **5 `SI` + 3 `NO`**. Las
reglas del algoritmo (§2-§2.3: cuota dura, fallback, protocolo de semilla) **siguen correctas** — no cambian en
nada. Lo que quedó **desactualizado** son las cifras ilustrativas de §1 y la rama de exclusión, ahora satisfechas
en los hechos por `#345`. Este acto es **propagación de un hecho ya resuelto**, no una decisión nueva.

## 1 · Mapeo de las 8 resoluciones a `grado_dependencia`

```
$ awk -F'\t' 'NR==1 || $1 ~ /^(DIN-07|DIN-08|DIN-09|DIN-10|DIN-12|DOC-03|DOC-05|DOC-06)$/ {print $1"|"$9"|"$16"|"$15}' forense/marco-candidatas-piloto-v1_0.tsv
id|grado_dependencia|dificultad|dominio
DIN-07|P2|MEDIA|dinero
DIN-08|P2|MEDIA|dinero
DIN-09|P2|FACIL|dinero
DIN-10|P2|MEDIA|dinero
DIN-12|P2|MEDIA|dinero
DOC-03|P2|DIFICIL|dinero
DOC-05|P2|DIFICIL|dinero
DOC-06|P2|DIFICIL|dinero
```

Las 8 son `P2|dinero` — **todas dentro del marcador puntuable** (`P1` ∪ `P2`, §1/§4 de `SORTEO-V2-PROPUESTA`),
ninguna `P0`. Esto importa para el cuadro: las 8 pendientes que §1 restaba del denominador puntuable de 50
(dejándolo en 22/50 evaluadas-`SI`, 8 sin evaluar) ya estaban **dentro** de ese marcador, no fuera — su
resolución mueve directamente la cifra del marcador puntuable, no solo la del marco de 60.

## 2 · Cuadro post-índice, re-derivado del framework v1_0 — comando y salida

```
$ awk -F'\t' 'NR>1{split($10,a," "); print a[1]}' forense/marco-candidatas-piloto-v1_0.tsv | sort | uniq -c
     27 NO
     33 SI

$ awk -F'\t' 'NR>1 && ($9=="P1"||$9=="P2"){split($10,a," "); print a[1]}' forense/marco-candidatas-piloto-v1_0.tsv | sort | uniq -c
     23 NO
     27 SI
```

| | filas | `SI` | % `SI` | tope 20% (`floor`) | exceso |
|---|---|---|---|---|---|
| marco completo (60) | 60 | 33 | 55.0 % | 12 | +21 |
| marcador puntuable (50, `P1`∪`P2`) | 50 | 27 | 54.0 % | 10 | +17 |

**0 filas `PENDIENTE-FUERA-DE-INDICE`** — verificado, la columna `publicada` de `marco-candidatas-piloto-v1_0.tsv`
no tiene ningún valor distinto de `SI`/`NO` (mismo `awk`, sin tercera categoría en la salida).

## 3 · Discrepancia encontrada contra la nota de `FP-146`, declarada y corregida en el uso

`forense/notas/2026-08-25-indice-no-inegi.md` §5 reporta *"SI sobre el marcador 50: 33/50 = 66.0 %"* (exceso
+23). Esa cifra usa el numerador equivocado: **33** es el total de `SI` del marco **completo** de 60 (incluye
las 6 `SI` de las 10 filas `P0`, verificado: `awk -F'\t' 'NR>1 && $9=="P0"{...}'` da 6 `SI` + 4 `NO`), no el
conteo de `SI` **dentro** del marcador puntuable. Re-derivado directo del framework (§2 arriba), el marcador
puntuable tiene **27** `SI`, no 33 — la cifra correcta es **27/50 = 54.0 %**, exceso **+17**, no +23. El número
del marco completo (33/60 = 55.0 %, exceso +21) sí coincide con la nota de `FP-146` — el desacople está acotado
al recorte por `grado_dependencia`, un filtro que la nota de `#345` no aplicó porque no era su perímetro (su
perímetro era la columna `publicada`, no el marcador puntuable del sorteo). **Este acto usa el número
re-derivado directamente del framework**, no el de la nota, y deja la discrepancia escrita en la propia
enmienda del `PROPUESTA` (§1) para que quien audite vea las dos cifras y por qué difieren — no se sustituye una
por otra en silencio, y no se corrige la nota de `#345` (fuera de perímetro de este acto, y su cifra de 33/60
sigue siendo correcta para lo que ella reporta).

## 4 · Amendment aplicado a `sorteo-act-pil-3-v2-PROPUESTA.md`

Enmienda in situ fechada, insertada al final de §1 (antes de §2, sin tocar una sola línea de §2-§2.3): cuadro
vigente con comando y salida, la discrepancia de §3 declarada, lectura para el sorteo (nada de §2 necesita
cambiar) y confirmación de que la rama de exclusión queda **satisfecha en los hechos**, no cerrada por una
decisión nueva de mesa — la propia regla de elegibilidad de §1 ("si y solo si `FP-146` las resuelve") ya
prescribía este desenlace. Verificado por `git diff` antes de commitear: §2-§2.3 **byte a byte intactas**; el
único texto nuevo vive entre el párrafo de "Las 8 `PENDIENTE-FUERA-DE-INDICE`..." y el encabezado `## 2`.

## 5 · Ningún ejemplo trabajado depende de las cifras viejas

Revisados los tres casos de prueba de §5 (`n_sorteo=12/15`, cuotas y estratos ilustrativos: `dinero|P2|DIFICIL`,
`tiempo|P2|MEDIA`, etc.) — son **sintéticos**, declarados como tal en su propio encabezado ("Estratos de ejemplo
abreviados para legibilidad"), y no citan `28/60`, `22/50` ni ninguna cifra del cuadro real de §1. No requieren
enmienda. Las únicas apariciones de `28/60`/`22/50`/`46.7`/`44.0` en todo el archivo son la línea original de
§1 (histórica, correcta cuando se escribió, intacta) y las dos referencias de la propia enmienda nueva que las
citan explícitamente como estado **anterior** — verificado por `grep -n` sobre el archivo completo tras editar.

## 6 · `FP-150`

`FP-150` (`ABIERTA`) recibe una actualización en su columna `gatea`: el cuadro vigente post-`#345` y la nota
*"lista para sello de mesa sobre cifras post-#345"*. **No se marca `FIRMADA`** — eso exige una firma de mesa
futura, que este acto no trae. `forense/firmas-pendientes.tsv` es el único archivo del tablero tocado por esta
fila.

## 7 · Tests

`python3 tests/check.py --baseline` corrido antes y después de la edición: línea base **VERDE**, sin FAIL
nuevo.

## 8 · Lo que este acto NO hace

No sella `FP-150` — es fact-propagation, no una decisión de mesa. No toca §2-§2.3 del `PROPUESTA` (verificado
byte a byte). No corre ningún sorteo real. No corrige la cifra de `forense/notas/2026-08-25-indice-no-inegi.md`
§5 (fuera de perímetro; su 33/60 sigue correcto, solo el 33/50 quedó señalado como el numerador equivocado para
ese denominador). No toca `tools/curador_registro/**` ni `data/curacion-universo/**` (perímetro ajeno).
