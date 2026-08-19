# NOTA · DOC-BACKFILL — las cuatro preguntas del transfer sobre las fuentes que sostienen celdas vivas

**Acto:** `ACTO DOC-BACKFILL`, 19/ago/2026, sobre `forense/encargos/2026-08-19-DOC-BACKFILL.md`.
**SHA de arranque:** `62e60e9` (`origin/main`, `HEAD` verificado por `git rev-parse HEAD`).

## 1 · Gate y firma que autorizan este acto (no relitigados, citados)

El encargo cita `FP-33` de `forense/firmas-pendientes.tsv` (verbatim, `awk -F'\t' '$1=="FP-33"'`): gate `post-BARRIDO-2`, firma D-6 de `MESA-19AGO` (`ADR-111(f)`): *"Escribir gateado — Se escribe DOC-BACKFILL ahora... gateado a B2-SEMÁNTICO fusionado y con la población re-derivable, no copiada. No se lanza aquí."* El gate («`B2-SEMANTICO` fusionado») ya estaba confirmado antes de abrir este acto (`forense/notas/2026-08-18-mesa-19ago-seis-firmas.md` punto 4; `forense/notas/2026-08-19-fp10-precedencia.md` §1, `PR #268` fusionado). No se re-verifica el gate aquí; se ejecuta lo que el gate deja vivo.

**Corrección de referencia obsoleta que el encargo hereda:** el texto de `FP-33` no menciona `FP-58`/`FP-60`, así que no hay nada que corregir de esa fila — la instrucción de la tarea sobre "texto stale citando FP-58/FP-60" no aplica a este encargo concreto; se deja constancia de que se buscó (`grep -n "FP-58\|FP-60" forense/encargos/2026-08-19-DOC-BACKFILL.md` → sin resultados) y de que ambas filas están, de todos modos, `CERRADA` en el tablero vigente (verificado: `awk -F'\t' '$1=="FP-58"{print $(NF-4)}'` y lo mismo para `FP-60` dan `CERRADA`).

## 2 · Población re-derivada por comando (no copiada de ninguna foto)

```
$ awk -F'\t' 'NR>1{print $4}' data/curacion-registro/produccion-modelo.tsv | sort | uniq -c
      2 G5.familismo_apoyo
      2 G5.familismo_obligacion
      8 G5.radio_confianza
$ awk -F'\t' 'NR>1{print $1}' data/curacion-registro/produccion-modelo.tsv | wc -l
12
$ ls data/curacion-registro/celdas-d/
G5.familismo_obligacion.actitud.yaml
G5.obligacion_medida.conducta.yaml
G5.radio_confianza.encuci_vs_enbiare.yaml
```

**12 producciones, 3 celdas-D, 3 constructos-fuente** — confirma el aviso del propio encargo (§3): no son "las 11 producciones / ocho fichas" de la foto del 12/ago.

**Bucket (c) — fichas de Hito D con acto en cola:** verificado que ningún archivo `forense/hitoD-*.md` trae un acto en cola sobre estos tres constructos:

```
$ grep -iln "radio_confianza\|familismo" forense/hitoD-*.md
forense/hitoD-preregistro-v2_0.md
$ grep -in "radio_confianza\|familismo" forense/hitoD-preregistro-v2_0.md
1022:...G1·radio_confianza pasa de ASIGNADO a ASIGNADO · SIGNO BAJO PRUEBA...
```
La única mención es la reserva de signo de `radio_confianza` bajo `ADR-60`, ya resuelta como reserva de canon (no una ficha con acto en cola sobre la *fuente*). Ningún `FP-*` que cite `hitoD` (`FP-43`, `FP-48`, `FP-53`, `FP-54`) toca `radio_confianza`/`familismo_apoyo`/`familismo_obligacion`. **Bucket (c) no aporta fuentes nuevas** — la población se cierra en las tres celdas-D de (b), que a su vez sostienen (junto con `familismo_apoyo`) las 12 producciones de (a).

## 3 · Las tres fuentes que sostienen la población, y quién las sostiene

Derivado de `data/curacion-registro/celdas-d/*.yaml` y de `produccion-modelo.tsv` (columna `input_path`, agrupada por `objeto_modelo_origen`):

```
$ python3 -c "
import csv
rows=list(csv.DictReader(open('data/curacion-registro/produccion-modelo.tsv'), delimiter='\t'))
from collections import defaultdict
d=defaultdict(set)
for r in rows: d[r['objeto_modelo_origen']].add(r['input_path'])
for k,v in d.items(): print(k,'->',v)"
G5.radio_confianza -> {enbiare_2021_base_de_datos_csv.zip}
G5.familismo_apoyo -> {enbiare_2021_base_de_datos_csv.zip}
G5.familismo_obligacion -> {enasic_2022_bd_csv.zip}
```

- `G5.radio_confianza.encuci_vs_enbiare.yaml`: BASELINE=**ENCUCI 2020** (no pasa por `tools/curador_registro/`, no tiene fila en `produccion-modelo.tsv` — celda-D líneas 42-56, 81-82), CHALLENGER=**ENBIARE 2021** (las 8 filas de `produccion-modelo.tsv`, `ESP-OPACA-C-9ecb5c61`).
- `G5.familismo_obligacion.actitud.yaml` + `G5.obligacion_medida.conducta.yaml`: ambas **ENASIC 2022** (`ESP-OPACA-B-d13ec4fe`, `ESP-OPACA-D-d800e103`).
- `G5.familismo_apoyo` (2 filas de producción, sin celda-D propia todavía — `PB2_1`/`PB2_2` en la misma tabla `TENBIARE`): **ENBIARE 2021**.

Tres fuentes distintas: **ENCUCI 2020, ENBIARE 2021, ENASIC 2022.**

## 4 · Las cuatro preguntas, por fuente

### 4.1 · ENBIARE 2021 (radio_confianza-CHALLENGER, familismo_apoyo) — **ABSORBIDO por BARRIDO-2 + VERIFICA-PUERTAS**, con un residuo declarado

1. **Ficha RNM abierta:** `https://www.inegi.org.mx/rnm/index.php/catalog/730` — verificada alcanzable (`200`) por `ACTO VERIFICA-PUERTAS` (13/ago/2026), fila `RNM_ENBIARE_2021_ficha730`, `data/acceso-puertas-2026-08-13.tsv:31`. La misma URL vive citada en la columna `evidencia_ref` de las 10 filas de producción ENBIARE de `produccion-modelo.tsv` (ej. `PROD-1e9ced27f928f0c8628b8b76`), junto a la metodología oficial `https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/nueva_estruc/889463903628.pdf`.
   - `periodo_levantamiento`: **2021-06-03/2021-07-23** — resuelto, campo no vacío en las 10 filas de producción (verificado: `awk -F'\t' 'NR>1 && $4~/radio_confianza|familismo_apoyo/{print $15}' produccion-modelo.tsv` da un único valor repetido).
   - `periodo_referencia_por_variable`: resuelto por reactivo, no genérico — `PF1_*`/radio_confianza: "últimos 12 meses"; `PB2_1`/`PB2_2`/familismo_apoyo y `PB1_01`/`PB1_02`: "momento de la entrevista (reactivo sin ventana retrospectiva explícita)" (columna `periodo_referencia` de cada fila, verbatim).
   - ponderador/estrato/conglomerado: **`FAC_ELE`** / **`EST_DIS`** / **`UPM_DIS`** — nombres exactos, confirmados dos veces: en `data/curacion-registro/expedientes-produccion/evidencia-neutral-produccion.json#/fuentes/ENBIARE_2021/diseno` (`{"ponderador":"FAC_ELE","estrato":"EST_DIS","conglomerado":"UPM_DIS"}`) y en la celda-D (`G5.radio_confianza.encuci_vs_enbiare.yaml:97`, "suma_pesos=84,449,936"). Ningún `NO_DETERMINADO` pendiente en este bloque.
2. **Indicadores de calidad:** no verificados en el catálogo propio del programa ENBIARE (RNM no expone una pestaña de indicadores de calidad por ficha en lo que este árbol registró; el catálogo genérico de indicadores de calidad de INEGI está *declarado pero no adquirido* — `data/curacion-universo/estado-activos.tsv:25658`, `DECLARADO_NO_ADQUIRIDO`, `https://www.inegi.org.mx/contenidos/masiva/indicadores/temas/calidad/calidad_00_xlsx.zip`). **`NO_DETERMINADO`** si existen indicadores de calidad específicos de ENBIARE — nadie en el árbol abrió ese catálogo. No se fabrica una URL de indicador específico. Si se abre en el futuro y aparecen indicadores nuevos, la cola donde se declaran es el propio encargo hermano `U2/EV-1` (`forense/encargos/2026-08-19-U2-EV1.md`, gateado igual que este, todavía sin lanzar) — no existe hoy una infraestructura de "cola EV-1" distinta de ese encargo para escribir en ella, así que aquí solo se deja la nota, no se crea artefacto.
3. **Diseño muestral oficial vs. inferido, por producción:** oficial, no inferido — las 10 filas de producción llevan `tipo_inferencia=DESCRIPTIVA_CON_DISENO` y `ponderacion_diseno` citando el tipo declarado por INEGI verbatim: *"probabilístico, estratificado, trietápico y por conglomerados"* (columna `ponderacion_diseno`, todas las filas ENBIARE).
4. **`NO-ENCONTRADO` con universo sin nivel documental:** no se encontró ningún `NO-ENCONTRADO` de ENBIARE en `forense/hallazgos.md` cuyo universo excluyera el nivel documental (ficha RNM) — el único `NO-ENCONTRADO` de esta familia de fuentes en el árbol es el de ENASIC (ver 4.2). No se reabre nada para ENBIARE.

### 4.2 · ENASIC 2022 (familismo_obligacion·actitud, obligación_medida·conducta) — **respondido por acto previo (ENCARGO C/ADR-69), citado aquí, no repetido**

1. **Ficha RNM abierta:** `https://www.inegi.org.mx/rnm/index.php/catalog/922` — verificada alcanzable (`200`), `data/acceso-puertas-2026-08-13.tsv:30`. La ficha **sí se abrió de contenido**, no solo se sondeó el HTTP: `forense/hallazgos.md:187` (entrada `2026-08-12`, `ENCARGO C`) documenta que el `NO-ENCONTRADO` original de `periodo_levantamiento` (11/ago, E4b SELLO-B — el descriptor de 6 hojas + el PDF de 26 páginas no lo traían) fue reabierto **porque su universo de búsqueda no incluía la ficha RNM** — exactamente el caso que la pregunta 4 pide reabrir cuando gatea algo vivo (gateaba `CRES-7cb78abf`, el cálculo de `familismo_obligacion.actitud`). Sección *Recolección de Datos* de la ficha 922 dio **`periodo_levantamiento = 2022-10-24/2022-12-16`** — valor que hoy vive en `produccion-modelo.tsv` fila `PROD-cca3ea0bccd54d70083728b2` y sus pares (`periodo_levantamiento` columna 15). **Discrepancia interna de la propia ficha, declarada y no resuelta por aquel acto:** la sección *Supervisión* de la misma ficha dice "10 de diciembre" (seis días antes del cierre de *Recolección*) — se deja igual de sin resolver aquí; no gatea nada vivo adicional (el valor usado en producción es el de *Recolección*, consistente con el uso).
   - `periodo_referencia_por_variable`: P7_12_7 (actitud) y P6_38 (obligación_medida) — "momento de la entrevista, sin ventana retrospectiva" para P7_12_7; "la semana anterior a la fecha de referencia" para P6_38 (`G5.obligacion_medida.conducta.yaml:123` — límite de escala declarado explícitamente entre las dos, no se restan).
   - ponderador/estrato/conglomerado: **`FAC_ELE`** (tabla `TPER_ELE`, actitud) / **`FAC_CUI`** (tabla `TPOB_CUI`, obligación_medida) — **no `FAC_SEL`**: discrepancia entre la prosa metodológica (que llama `FAC_SEL` al factor) y el descriptor/CSV real (`FAC_ELE`/`FAC_CUI`), ya registrada antes de este acto en `evidencia-neutral-produccion.json#ENASIC_2022.ambiguedad_material` y en `ponderacion_diseno` de la fila de producción (columna `reserva`, verbatim: *"El documento metodológico llama FAC_SEL a este factor en prosa... la columna real es FAC_ELE"*). Estrato=`EST_DIS`, conglomerado=`UPM_DIS` en ambas tablas.
2. **Indicadores de calidad:** mismo estado que ENBIARE — **`NO_DETERMINADO`**, catálogo genérico de INEGI declarado pero no adquirido en el árbol (`data/curacion-universo/estado-activos.tsv:1382`). Ningún acto abrió la sección de indicadores de calidad propia de la ficha 922. No se fabrica.
3. **Diseño muestral oficial vs. inferido:** oficial — *"probabilístico, estratificado, unietápico y por conglomerados; método de Conglomerados Últimos y Series de Taylor"* (`evidencia-neutral-produccion.json#/fuentes/ENASIC_2022/diseno_observado`, y replicado en `ponderacion_diseno` de las 2 filas de producción).
4. **`NO-ENCONTRADO` con universo sin nivel documental:** el único caso de la población, y **ya reabierto y cerrado** por `ENCARGO C`/`ADR-69` (12/ago/2026) antes de que este acto existiera — ver punto 1. No hay nada vivo que reabrir aquí; se cita, no se repite (mismo criterio que la pregunta 4 exige: *"solo si gatea algo vivo se reabre"* — ya gateó, ya se resolvió).

### 4.3 · ENCUCI 2020 (radio_confianza-BASELINE) — **parcialmente absorbido; residuo genuino `NO_DETERMINADO`**

1. **Ficha RNM abierta:** `https://www.inegi.org.mx/rnm/index.php/catalog/647` — verificada alcanzable (`200`), `data/acceso-puertas-2026-08-13.tsv:32` (`ACTO VERIFICA-PUERTAS`, 13/ago/2026). **A diferencia de ENASIC, ningún acto del árbol abrió el *contenido* de esta ficha** (ni la sección *Recolección de Datos* ni *Diseño Muestral*) — solo se sondeó su HTTP. `periodo_levantamiento` de ENCUCI **no aparece en ningún archivo del árbol más allá de "edición 2020"**: `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` (la nota que originó la celda-D) da fecha de edición pero no rango de levantamiento, y `G5.radio_confianza.encuci_vs_enbiare.yaml:60` solo declara `edicion_periodo: "2020"`. **`NO_DETERMINADO`** — se declara así en vez de fabricar una fecha; no gatea nada nuevo porque ninguna producción de `produccion-modelo.tsv` usa ENCUCI directamente (el BASELINE de radio_confianza corre fuera de `tools/curador_registro/`, per la celda-D, línea 81-82), así que el residuo no bloquea ningún cálculo vigente.
   - `periodo_referencia_por_variable`: sí resuelto — `AP5_1_1/2/3` sin ventana retrospectiva explícita, per la nota de origen (§1.1).
   - ponderador/estrato/conglomerado: **`FAC_SEL`** / **`EST_DIS`** / **`UPM_DIS`** — nombres exactos, confirmados en la nota de origen (`forense/notas/2026-08-03-...md:113-114,155,161`) y en la celda-D (línea 70: "Ponderador `FAC_SEL`, suma verificada 96,427,583"). **Aquí `FAC_SEL` sí es el nombre real** (no hay discrepancia como en ENASIC — verificado por comando, no heredado por analogía).
2. **Indicadores de calidad:** `NO_DETERMINADO`, mismo motivo que las otras dos fuentes.
3. **Diseño muestral oficial vs. inferido:** el diseño (`FAC_SEL`/`EST_DIS`/`UPM_DIS`, conglomerado último) se toma del propio microdato/documento fuente citado en la nota de origen — tratado como oficial (mismo patrón declarativo que ENBIARE/ENASIC), no inferido por el ejecutor.
4. **`NO-ENCONTRADO` con universo sin nivel documental:** no se encontró ningún `NO-ENCONTRADO` de ENCUCI en `forense/hallazgos.md` con ese patrón. Nada que reabrir.

## 5 · La decisión del gate (§5 del encargo): ¿lanzado, absorbido, o mixto?

Ni un "sí" limpio ni un "no" limpio. **ENASIC** está genuinamente absorbido: las cuatro preguntas ya tenían respuesta citable en el árbol antes de este acto (`ENCARGO C`/`ADR-69` para la pregunta 1/4, `evidencia-neutral-produccion.json` para ponderador/diseño). **ENBIARE** está absorbido salvo el residuo declarado de indicadores de calidad. **ENCUCI** queda con un residuo real: nadie abrió el contenido de su ficha RNM 647 para extraer `periodo_levantamiento`. Ese residuo **no gatea nada vivo** (el BASELINE de `radio_confianza` no pasa por el pipeline de producción y su `champion_actual` no depende de esa fecha — `champion_actual: "BASELINE.ENCUCI"`, celda-D línea 139, fijo desde `ADR-82`), así que per la propia regla de la pregunta 4 (*"solo si gatea algo vivo se reabre; si no, una línea y se queda"*) **se declara y se queda**, no se reabre un acto de descarga.

**Conclusión:** este acto se ejecuta como **backfill documental parcial + declaración de absorción parcial** — no un cierre limpio "absorbido por BARRIDO-2" para las tres fuentes por igual, y no un acto que descubre nada nuevo: cita lo que ya existía, dispersos en `BARRIDO-2` (`data/curacion-universo/`), `VERIFICA-PUERTAS` (`data/acceso-puertas-2026-08-13.tsv`), `evidencia-neutral-produccion.json` y `ENCARGO C` (`forense/hallazgos.md:187`), y deja un único residuo honesto (`periodo_levantamiento` de ENCUCI) sin fabricar.

## 6 · Indicadores de calidad — estado de la cola `EV-1`

Las tres fuentes dan el mismo resultado: **`NO_DETERMINADO`** si existen indicadores de calidad específicos por ficha — el catálogo genérico de indicadores de INEGI (`.../indicadores/temas/calidad/calidad_00_xlsx.zip`) está declarado en `data/curacion-universo/` pero **`DECLARADO_NO_ADQUIRIDO`**, nunca abierto por ningún acto. No se añade nada a una "cola EV-1": esa cola no existe hoy como artefacto propio, es el propio encargo hermano `forense/encargos/2026-08-19-U2-EV1.md` (`FP-32`, mismo gate, todavía sin lanzar) — este acto no lo lanza (fuera de perímetro) y deja escrito que, si `U2-EV1` corre y abre ese catálogo, ahí es donde correspondería registrar indicadores nuevos.

## 7 · Corrección de referencias obsoletas (FP-58/FP-60)

Verificado que ni `forense/encargos/2026-08-19-DOC-BACKFILL.md` ni la fila `FP-33` citan `FP-58`/`FP-60` — no había texto obsoleto que corregir en el material de este encargo específico. Se deja constancia, por instrucción explícita recibida, de que ambas filas están cerradas en el tablero vigente:

```
$ awk -F'\t' '$1=="FP-58"{print $1"\t"$6}' forense/firmas-pendientes.tsv
FP-58	CERRADA
$ awk -F'\t' '$1=="FP-60"{print $1"\t"$6}' forense/firmas-pendientes.tsv
FP-60	CERRADA
```
(Columna 6 = `estado`, confirmado contra la cabecera: `head -1 forense/firmas-pendientes.tsv | tr '\t' '\n' | cat -n`.)

## 8 · Suite

```
$ python3 tests/check.py --baseline
...
21 FAIL · 121 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
```
Sin `--freeze`. Cifra idéntica a la vigente en `62e60e9` antes de este acto — este acto no toca `tests/`, `milpa/`, `canon/` (salvo la fila de `firmas-pendientes.tsv`) ni `data/`.

## 9 · Cierre

- `FP-33` → **CERRADA** (mismo vocabulario de `estado` que `FP-58`/`FP-60`; ver `firmas-pendientes.tsv`, misma fila, columna `ejecutada_en` actualizada).
- Tres fuentes cubiertas: **ENBIARE 2021** (absorbido, residuo: indicadores de calidad `NO_DETERMINADO`), **ENASIC 2022** (absorbido, cita `ENCARGO C`/`ADR-69`), **ENCUCI 2020** (parcial: `periodo_levantamiento` exacto `NO_DETERMINADO`, no gatea nada vivo).
- Cero fabricación: toda URL citada en esta nota (`catalog/730`, `catalog/922`, `catalog/647`, la metodología ENBIARE, el catálogo genérico de calidad) existe ya en el árbol, verificada por comando, ninguna tecleada de memoria.
- `tests/check.py --baseline`: **VERDE**, `21 FAIL · 121 WARN`, sin cambio.
- Encargo `forense/encargos/2026-08-19-DOC-BACKFILL.md` → `CONSUMIDO`.
