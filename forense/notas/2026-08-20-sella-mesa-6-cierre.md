# Nota · ACTO SELLA-MESA-6

**Fecha:** 2026-08-20 · **Entorno:** UBUNTU · **Encargo:** `forense/encargos/2026-08-20-SELLA-MESA-6.md`. **Base:** `origin/main = c6fe9852c29d2ab0a1ff5cfa5d063fedd0695447`, verificado por `git log -1 --format=%H` al arrancar y re-verificado sin cambio al escribir.

## 0. Verificación previa (regla v2.1 — nada de memoria)

- Máximo ADR verificado: `grep -oE 'ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -5` → único máximo `134`, sin huecos. El ADR de este acto se candidatea `ADR-135`.
- Máximo FP verificado: `grep -oE 'FP-[0-9]+' forense/firmas-pendientes.tsv | sort -t- -k2 -n -u | tail -5` → único máximo `91`. Las filas nuevas de este acto se numeran `FP-92`..`FP-95`.
- `FP-79`..`FP-84`: leídas con `csv.DictReader` (no `grep` de conteo) — las seis en `estado=ABIERTA`, `firmada_en`/`ejecutada_en` vacías, todas del encargo `2026-08-20-ACT-PIL-2.md`. Confirmado.
- `data/indice-descarga-masiva-2026-08-05.tsv`: **7 930** filas de datos (`wc -l` menos cabecera). Por columna `carpeta`: `7 633` `microdatos`, `296` `doc`, `1` `otro`. Por columna `formato`: `7 578` `zip`, `222` `pdf`, `92` `xlsx`, `34` `xls`, `4` `csv`.
- `data/indice-canastas-2026-08-08.tsv`: **17 163** filas de datos. Por columna `canasta`: `15 563` `tabulados`, `970` `denue`, `557` `indicadores`, `70` `sala_de_prensa`, `3` `inv`.
- Ficha RNM 922: localizada en `forense/notas/2026-08-19-lote-ubuntu-adq-1-cierre.md:89` (sección (c)), cita verbatim de los rangos de interpretación del CV, ENASIC 2022.
- `data/censo-explotacion-2026-08-17.tsv`: **627** filas de datos (`wc -l` menos cabecera).
- Cita "adoptarlos en vez de inventarlos": localizada verbatim en `forense/adv-duelo/ADV-1_demolicion_duelo_L_vs_M.md:142`.
- Cita "infraestructura completa en CODEX … no para desperdiciarla": **no preexistía en el árbol** — es la decisión de mesa que este mismo acto sella en `FP-82`/`ADR-135(d)`, no una cita histórica a verificar contra el corpus.

## 1. Ejecución

Un solo ADR nuevo, `ADR-135`, en `canon/gobernanza-v1_15.md`, que sella las seis filas `FP-79`..`FP-84`:

- `FP-79` → `FIRMADA`: escala CV de INEGI adoptada, corte en «baja precisión», dos bandas por tipo de unidad (hogares / unidades económicas), citando verbatim `ADV1-M1` y la ficha RNM 922. Abre `FP-92` sin re-etiquetar la θ ya sellada que el hallazgo del 19/ago encontró con dos celdas en «baja».
- `FP-80` → `FIRMADA`: sin piso de `n` ex ante, razón escrita.
- `FP-81` → `CERRADA POR PREMISA REFUTADA`: el filtro (i) sí es ejecutable desde una caja sin navegador vía los dos índices de descarga masiva ya en el árbol; diseño en dos pasos abierto en `FP-93`, asignado a Ubuntu.
- `FP-82` → `FIRMADA`: marco a saturación antes de sortear, semilla `867948c` anulada, cita de mesa verbatim sobre CODEX.
- `FP-83` → `FIRMADA`: árbitros sin error muestral llevan banda propia pre-registrada; regla sellada aquí, banda por celda diferida a `FP-94`.
- `FP-84` → `FIRMADA`: cruce contra censo nuevo (627 filas), re-censo acotado a las 14 fuentes que cambiaron de estado, diferido a `FP-95`, asignado a Ubuntu.

`forense/firmas-pendientes.tsv`: las seis filas cambian de estado en el mismo commit; cuatro filas nuevas `ABIERTA` (`FP-92`..`FP-95`), numeradas correlativamente tras el máximo real (`91`), escritas por script Python línea por línea (no con `csv.writer`, para no arriesgar el TSV — se verificó después con `csv.DictReader` que el resultado parsea limpio).

`forense/hallazgos.md`: tres líneas nuevas — el patrón "negativo derivado de conteo sin inspección" (con las dos ocurrencias que sí se pudieron verificar en el árbol, `LOTE-RETRIAGE` y `FP-81`/`ACT-PIL-2`; **"los pobres no pagan" se buscó y no encaja en el patrón — se dice así en vez de forzar la cita**, ver §2); que el índice de canastas resuelve una prueba declarada inejecutable; y que los tres números del encargo (ADR máximo, FP máximo, estado de las seis filas) se re-verificaron por comando y coincidían con lo afirmado, sin heredarlos.

## 2. Lo que no se pudo verificar, y por tanto se omitió o se marcó así

- **"El acto ya había medido 0/14 sobre ENFIH/ENSAFI antes de que fueran anunciadas como 'mayor palanca' en alguna apertura v1.2 §3"**: se buscó `"mayor palanca"` en todo el árbol (`grep -rn`) y no aparece en ningún archivo. `ADR-134`/`APERTURA-ENFIH-ENSAFI` sí midió `0 de 8` celdas en `EXISTE-SATISFACE` (no `0/14`; la tasa base `0 de 14` es de `ABRIR-4`, 8/ago, sobre los mismos dos instrumentos) y sí hay un episodio real sobre `APERTURA v1.2 §3` como premisa mal fundada al principio y sostenida después por una fusión concurrente (`forense/notas/2026-08-20-apertura-enfih-ensafi-cierre.md §0/§6`) — pero ninguno de los dos hechos usa la frase "mayor palanca". **No se escribió esta línea en `hallazgos.md`**, para no fabricar una cita.
- **"los pobres no pagan" como ocurrencia del patrón "negativo derivado de conteo sin inspección"**: localizada en el árbol (`ADR-117`/`ADR-123`/`ADR-125`, `forense/hallazgos.md:429-432`) pero es un veredicto de deep-research sobre 11 casos auditados (CNBV/BMV/SEC), no un negativo derivado de un conteo mecánico sin inspeccionar el instrumento real. Se omitió de la línea de hallazgo por no encajar en el patrón, y se dice explícitamente en la línea misma.
- **"dos actos previos habían declarado inejecutable" el filtro (i)**: en el árbol, la declaración de inejecutabilidad aparece dos veces (`ADR-130(e)` y `forense/hallazgos.md:454`) pero ambas provienen del **mismo** acto (`ACT-PIL-2`, T2), no de dos actos distintos. Se citó así en `ADR-135(c)` — "el acto que escribió `FP-81`" — sin inflar a "dos actos".

## 3. Línea base

Mecanismo real localizado: `python3 tests/check.py --baseline` (ver `tests/check.py:1442` y `tests/bitacora.py:83`). Corrido antes de commitear. Salida relevante:

```
24 FAIL · 137 WARN
LÍNEA BASE: ROJO — 2 entradas nuevas frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
· T15: canon/estado-programa-v1_10.md: cita 134 ADR; gobernanza tiene 135 únicos
· T16: canon/estado-programa-v1_10.md: declara 21 FAIL · 137 WARN vigente; la corrida real da 23 FAIL · 135 WARN
(3 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

**El ROJO es esperado y no se corrige aquí**: `T15`/`T16` disparan porque `canon/estado-programa-v1_10.md` sigue citando `134 ADR` — ese archivo está **fuera del perímetro estricto** que este acto se impuso (no está en la lista de archivos permitidos: `canon/gobernanza-v1_15.md`, `forense/firmas-pendientes.tsv`, `forense/hallazgos.md`, `forense/encargos/`, `forense/notas/`). Mismo patrón que `ADR-134`/`ADR-133`/`ADR-131` ya dejaron medido esta jornada: sellar un ADR nuevo sin poder tocar `estado-programa` deja el conteo desincronizado hasta que un acto con permiso sobre ese archivo lo recifre. Se declara aquí en vez de forzar el perímetro para pintar el semáforo en verde.

## 4. Perímetro respetado

No se tocó `milpa/`, `data/` (salvo lectura), `tests/` (salvo ejecución de `check.py --baseline`, sin escritura), `corpus/`, `canon/modelo-decision-v4_0.md`, ni ningún `resultado.tsv`. `data/diseno-muestral.yaml` se cita, no se edita (fuera de perímetro, declarado también en la propia fila `FP-84`/`FP-95`).
