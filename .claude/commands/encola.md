---
description: Copia/appenda piezas de dirección a forense/encargos/ (o cola/) y a canon/, censa rótulos, corre la suite y abre PR [COLA] — solo si cada ruta listada aparece en el diff.
argument-hint: <lista destino←origen, una por línea>
---

# `/encola` — lleva piezas de dirección al árbol, con verificación de completitud

Instaurada por `ACTO MAESTRA34-N7 · SKILLS-COLA-Y-ADQ`
(`forense/encargos/2026-09-01-MAESTRA34-N7-SKILLS-COLA-Y-ADQ.md`). Defecto
medido que la crea: `PR #454` omitió 1 de 3 piezas de la instrucción
`[COLA]` (la enmienda a `N3`) y requirió perdón `T25` manual; `PR #455` lo
corrigió a mano. Esta skill existe para que "encolar N piezas" deje de
depender de que quien redacta el PR las cuente bien de memoria.

Entrada: una lista de rutas **destino ← origen**, cada una de dos formas:

- **ARCHIVO NUEVO**: destino es una ruta que no existe hoy en el árbol —
  típicamente bajo `forense/encargos/` o `forense/encargos/cola/`. Origen es
  el texto completo a escribir ahí, verbatim.
- **ENMIENDA**: destino es un archivo que **ya existe**. Origen es el texto
  a **appendear al pie**, verbatim — nunca se edita nada por encima de la
  línea de append.

No decide **qué** se encola — eso es de dirección, y llega ya redactado en
`$ARGUMENTS` o en los archivos que la sesión cite. Esta skill es el
mecanismo de aterrizaje, no el redactor.

---

## 0 · Lo que esta skill NO hace

1. **No redacta.** El texto de cada pieza es el que dirección trae; se
   copia o se appenda tal cual, sin resumir, sin corregir, sin mejorar
   prosa.
2. **No inventa perdones de test.** Si `tests/check.py --baseline` da un
   `FAIL` nuevo por `T25` (rótulo pelado) en el texto que se está
   encolando, **PARA y reporta el rótulo pelado exacto** — la corrección es
   de **dirección** (citar con serie `MAESTRA<nn>-`), no de esta skill. No
   se añade la ruta a `_T25_ARCHIVOS_CONOCIDOS` para pasar por alto un
   rótulo que dirección todavía no corrigió.
3. **No abre el PR si la completitud falla.** Ver paso 4.

---

## 1 · `git fetch`

```
git fetch origin main
```

Trabaja sobre una rama nueva desde `origin/main` (`claude/encola-<fecha>` o
similar), nunca sobre `main`.

## 2 · Copia / append, en orden

Para cada entrada de la lista, en el orden en que se recibió:

- **ARCHIVO NUEVO** → `Write` del contenido completo en la ruta destino.
  Si la ruta ya existe, esto es un error de clasificación (debió ser
  ENMIENDA) — PARA y repórtalo, no sobrescribas.
- **ENMIENDA** → append al final del archivo destino, precedido de un
  separador claro (p.ej. `---` o el encabezado de sección que la propia
  pieza traiga) para que quede visualmente distinguible del contenido
  anterior. Nunca reescribe ni reordena lo que ya estaba.

## 3 · Censo de rótulos nuevos — `canon/registro-rotulos.tsv`

Solo los rótulos que el texto **recién encolado** trae **con serie
completa** `MAESTRA<nn>-<letra><n>` (p.ej. `MAESTRA34-N7`, `MAESTRA34-E1`)
se censan aquí, siguiendo el formato TSV existente (`espacio`, `rótulo`,
`que_significa`, `donde_vive`) — lee `canon/registro-rotulos.tsv` primero
para calzar columnas y estilo de prosa.

**Rótulos pelados** (`M<n>`, `E<n>` sin la serie `MAESTRA<nn>-`) **no se
censan aquí** — no son un habitante nuevo del espacio de rótulos, son
exactamente el patrón que `tests/check.py::T25` existe para atrapar. Si el
texto trae uno, eso se resuelve en el paso 5, no en este.

## 4 · `tests/check.py --baseline`

```
python3 tests/check.py --baseline
```

- **VERDE** → sigue al paso 5.
- **`FAIL` nuevo por `T25` (rótulo pelado)** → **PARA.** Reporta el rótulo
  pelado exacto, el archivo y la línea que la salida de `check.py` señala.
  No lo añadas a `_T25_ARCHIVOS_CONOCIDOS`, no lo edites tú mismo dentro
  del texto de dirección (violaría A.3 si la pieza es un encargo
  archivado) — repórtalo para que dirección lo corrija con la serie
  correcta y vuelva a encolar.
- **Cualquier otro `FAIL` nuevo** → PARA y repórtalo con la salida cruda;
  no es responsabilidad de esta skill decidir si es tolerable.

## 5 · Verificación de completitud (A.13) — antes de abrir nada

```
git diff --stat
```

**Cada ruta destino de la lista tiene que aparecer en ese diff.** Cuenta
las dos cifras:

- `n` = número de rutas destino en la lista de entrada.
- `m` = número de esas rutas que aparecen en `git diff --stat`.

Si `m < n`: **no abras el PR.** Reporta con la forma exacta `A.13: n
listadas / m en diff`, y nombra **cuál(es)** falta(n) — esto es exactamente
el defecto que `PR #454` cometió (una de tres piezas omitida sin que nadie
lo notara hasta que `T25` reventó por perdón manual). Un `n == m` que no se
verificó mecánicamente no cuenta como verificado.

Si `m == n`: sigue al paso 6.

## 6 · Abre el PR

Título: `[COLA] <lo que se encola, en pocas palabras>` (p.ej.
`[COLA] encola MAESTRA34-N7 y MAESTRA34-E1`).

Cuerpo, en este orden:

1. Qué piezas se encolaron (lista destino ← origen).
2. Censo de rótulos hecho en el paso 3 (o "ninguno con serie" si no
   aplicaba).
3. Veredicto de `tests/check.py --baseline` (VERDE, con conteo).
4. La verificación de completitud del paso 5, con sus dos cifras (`n
   listadas / m en diff`) y el `git diff --stat` completo.

No lo fusiones. `CONTADOR`: piezas encoladas, declarado — esta skill no
mide nada del programa, solo aterriza texto.

---

## Prueba en seco — contra los tres archivos de `PR #455`

`PR #455` (`[COLA] encola MAESTRA34-N7 y MAESTRA34-E1`) tocó exactamente
tres archivos:

```
git show --stat 399e1f0 2>/dev/null || git log --all --format='%H %s' --grep='encola MAESTRA34-N7'
```

Verificado contra este árbol: el commit `399e1f0` (`[COLA] encola
MAESTRA34-N7 y MAESTRA34-E1`) toca
`forense/encargos/2026-09-01-MAESTRA34-N7-SKILLS-COLA-Y-ADQ.md`,
`forense/encargos/cola/2026-09-08-MAESTRA34-E1-REVISION-FALSADORES.md` y
`canon/registro-rotulos.tsv` (los dos rótulos `MAESTRA34-N7` y
`MAESTRA34-E1` censados en la misma pieza).

Correr esta skill en seco contra esas tres rutas como lista de entrada
(los dos primeros como ARCHIVO NUEVO, el tercero como ENMIENDA sobre
`canon/registro-rotulos.tsv`) produce, en el paso 5, `n = 3` rutas
listadas y `m = 3` en `git diff --stat` — completo, PR se abre.

**Y la comprobación de que esta skill habría detectado la omisión de `PR
#454`**: si la misma lista de tres se hubiera encolado con solo dos de las
tres piezas realmente escritas (el caso de `#454` — la enmienda a `N3`
faltante), el paso 5 habría dado `n = 3 / m = 2`, nombrado la ruta que
falta, y **no habría abierto el PR** — exactamente el resultado que
`#454` necesitaba y no tuvo, porque nadie corrió esa cuenta antes de
fusionar. Esta skill no requiere un PR real para probarse: el mecanismo
del paso 5 es determinista y se verifica con el `git diff --stat` de
cualquier commit ya fusionado, incluido éste.
