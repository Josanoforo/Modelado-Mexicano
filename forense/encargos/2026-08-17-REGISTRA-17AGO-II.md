# ENCARGO `REGISTRA-17AGO-II` · tres firmas más, la reformulación de FP-29 y el texto que desbloquea FP-33

- **SHA de redacción:** `1282ae3` (`origin/main`, merge #247) · **Fecha:** 17/ago/2026 · **Estado:** `VIVO`
- **Entorno: NUBE**, repo-only, sin red, sin corpus. **NO en la caja** — ahí corre BARRIDO-2.
- **Modelo: Sonnet 4.6.** Registro y pegado, no adjudicación.
- **Archívese en `forense/encargos/`** con su lanzamiento (A.3).

## ⛔ GATE — este acto NO arranca hasta que **PR #248 esté fusionado**

Escribe los mismos dos archivos que #248 (`forense/firmas-pendientes.tsv` y `canon/gobernanza-v1_15.md`). Correr en paralelo garantiza conflicto en las dos.

```sh
git fetch origin && git merge-base --is-ancestor <sha-de-#248> origin/main && echo OK || echo "PARA: #248 sin fusionar"
```
**Si da PARA, para.** No ramifiques desde la rama de #248: espera el merge.

---

════════ ARRANQUE ════════
1 · **REPO.** Clon existente; si clonas, dilo. Ruta absoluta · `git log -1 --format="%h %s"` · `git status`. **No arranques desde el home.** `git rev-parse --is-shallow-repository`; si `true`, `git fetch --unshallow` **antes** de cualquier veredicto.
2 · **SHA.** Base: el `main` **posterior** al merge de #248. Si main avanzó más, no es PARO — clasifica la deriva (¿tocó `firmas-pendientes.tsv` o `gobernanza`?) y repórtala antes de editar.
3 · **data/raw.** No toca microdato — dilo y salta.
4 · **ENTORNO.** Reporta la variable cruda y la sonda a `https://github.com/`. No toca red de datos.
5 · **ESPEJO.** Prohibido para cifras.
══════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección contra `1282ae3` ═══

**1 · ESTRUCTURA.** Gobiernan `forense/firmas-pendientes.tsv` (7 columnas, A.12/ADR-85) y `canon/gobernanza-v1_15.md` §4. Dominio 7 del índice. **Nada de `data/` se escribe.**

**2 · CONTENIDO.** Las tres filas a firmar están `ABIERTA` con `firmada_en` vacío contra `1282ae3`: **`FP-24`, `FP-30`, `FP-31`** → `EXISTE-NO-SATISFACE`. `FP-29` y `FP-33` existen y su descripción es la que hay que corregir → `EXISTE-NO-SATISFACE`.

**3 · COBERTURA RETROACTIVA.** Las cinco nacieron con el tablero (14/ago) o con `ADR-91` (17/ago). Sin brecha.

**⚠️ Y la corrección al bloque de existencia del encargo anterior, que es el hallazgo más útil de #248.** `REGISTRA-17AGO` declaró, con el comando pegado como prueba, que BARRIDO-2 **no** tocaba `firmas-pendientes.tsv`. Al ejecutarse, el mismo comando dijo que **sí** — BARRIDO-2 había apilado su propio `FP-38` entre una corrida y la otra. **La verificación no estaba mal corrida: estaba caducada.** Contra una rama viva, una verificación de concurrencia tiene vida de minutos.

Por eso este bloque lleva **estampa de universo (A.10)**: lo de arriba se verificó contra `origin/main = 1282ae3` y contra `origin/codex/barrido-2` con **12 commits**, el 17/ago. **Re-córrelo al arrancar y reporta la diferencia** — si el universo creció, este bloque queda `VENCIDO EN ALCANCE` y manda el tuyo.

═══════════════════════════════════════════════════════════════════

**PERÍMETRO.** Escribe **exactamente**: `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` (UN ADR) · `forense/notas/2026-08-17-registra-2.md` · `forense/hallazgos.md` (una entrada, `merge=union`) · `forense/encargos/2026-08-17-REGISTRA-17AGO-II.md` (este texto, A.3).
**NO escribe:** `data/**` · `tools/**` · `canon/estado-programa-v1_10.md` · `canon/glosario-v5_6.md` · `canon/integrador-*` · `corpus/**` · `tests/**` · `instrucciones-*` · `propuesta-motor-adaptativo-celda-v0_4.md`.

**⚠️ Nombra tu nota `registra-2`, no `registra-17ago-ii`.** T02 colisiona por nombre normalizado y ya mordió en #248: `forense/notas/2026-08-17-registra-17ago.md` y `forense/encargos/2026-08-17-REGISTRA-17AGO.md` normalizan igual y T02 falló. No repitas el patrón.

**⚠️ No cites archivos inexistentes con backticks.** `PLAN-MULTIFASE-F0-F6-2026-08-13.md` y los transfers **no están en el árbol** y T03 dispara sobre ellos — falló en #248 por eso. Precedente de cómo hacerlo, verbatim de `forense/notas/2026-08-14-enlace2-clase-limbo.md:3`: *"citado sin backticks a propósito: vive fuera del repo y T03 no dispara"*. **Cítalos sin backticks.**

**Numeración.** Este acto **no crea filas nuevas** — solo firma y corrige existentes. Con eso evita del todo la colisión de ids que #248 y BARRIDO-2 tienen abierta (los dos reclaman `FP-38`). Si aun así necesitaras una fila nueva, **derívala al sellar**, no la heredes: tras fusionar #248 y BARRIDO-2 el máximo será `FP-43`, no `FP-42`.

---

## COMMIT 1 · Las tres firmas

Formato de `firmada_en` idéntico al de `ADR-91`/`ADR-92`. **Citas exactamente como están; no las corrijas ni las puntúes.**

**`FP-31` → `FIRMADA`.** Cita: *"1- hay que firmarla y sellarla."* Texto adoptado:
> "`propuesta-motor-adaptativo-celda-v0_4.md` queda sellada **por referencia**, sin acto de contenido: sus preguntas de mesa ya estaban resueltas y el documento no lo decía. `ADR-71(d)` adjudicó la única que esa versión abría —la partición del enum, sin cajón de sastre— y `ADR-68` ya había adoptado el contrato celda-D v0.3 como formato del registro de comparación de estimadores. Las diez preguntas de v0.3 §8 siguen resueltas como estaban; ninguna se reabre."

**Deriva la premisa, no la heredes:** `propuesta-motor-adaptativo-celda-v0_4.md:122` debe decir literal *"Preguntas para mesa — resueltas, 12/ago/2026"*. **Si no lo dice, PARA.** Y **no edites la propuesta**: está fuera de perímetro; el sello vive en el ADR y en la fila.

**`FP-24` → `FIRMADA`.** Cita: *"2: entonces vamos a cerrarla indicando de donde viene."* Texto adoptado:
> "Se adopta como política de pares el texto ya citado inline en `forense/notas/2026-08-14-enlace2-clase-limbo.md` §4, que pasa a ser **el canónico**: *'cada `objeto_evidencia` conserva su fila; la gemela `NO_DETERMINADO` se enlaza SOLO si su objeto es evidenciable con una entrada distinta del manifiesto'*. **Procedencia, declarada por instrucción de mesa:** el texto se propuso en PLAN-MULTIFASE-F0-F6-2026-08-13.md §94, documento de dirección que vive fuera del repo; la nota de ENLACE-2 lo transcribió inline y **esa transcripción es la que rige** — el original deja de ser necesario, que es exactamente el remedio que A.3 prescribe. Las 20 filas con par (ENSAFI 9 · ENFIH 8 · ENBIARE 3) se adjudican con esta regla en acto propio; **este acto no las escribe.**"

**Deriva y reporta:** el conteo 48/20 y el reparto por fuente, contra `data/relaciones.tsv` con la definición de par de la §4 (misma `necesidad_id` + misma `fuente_canonica_normalizada`, una fila `SI` y su gemela `SI_O_REFERENCIADO`). **Si no reproduce 20, PARA** — la regla se firmó sobre un alcance que ya no existe.

**`FP-30` → `FIRMADA`.** Cita: *"FP30: ii: Solo equivalencias."* Texto adoptado:
> "El Bloque A **no se amplía**. Los siete vocabularios que T07 reporta como ajenos no son siete niveles: son **cuatro conceptos escritos con siete grafías**, y se resuelven con tabla de equivalencia, no con bandas nuevas. Mapeo adoptado: `SÓLIDO`→fuerte · `MEDIO`, `Moderada`, `MODERADA`→media · `HIPÓTESIS RAZONABLE`→hipótesis razonable · `Narrativa exagerada`→narrativa popular · `MODERADA-FUERTE`→media-fuerte. **No hay v2.11 de instrucciones y no hay pegado nuevo.** La ejecución del mapeo sobre el corpus va en acto propio."

**⚠️ Y el inciso que este ADR debe traer, porque sin él la firma queda a medias.** `tests/check.py:286` define `CANONICO = {"FUERTE", "MEDIA", "MEDIA-FUERTE", "HIPÓTESIS"}` — **no coincide con el Bloque A**, que dice *fuerte · media · hipótesis razonable · narrativa popular*: el test **añadió `MEDIA-FUERTE` y borró `narrativa popular`** por su cuenta, sin ADR. Y su contador compara con `.upper()` pero cuenta con `tok.strip()`, por lo que `Moderada` y `MODERADA` se reportan como dos vocabularios cuando el propio test los trata como uno — **el "7" está inflado por esa razón**. `FP-41` (creada por #248) ya lo registra. El ADR **declara que la firma de FP-30 no alinea el test** y que eso es el acto sucesor. **No toques `tests/`.**

**El ADR.** Registra las tres firmas verbatim, más los dos incisos de abajo. Número **derivado al sellar** con la receta de T15 (`^\*\*ADR-(\d+)`), contra el `main` real, sin dejar hueco. Tras #248 el máximo será `92`; **si te da otra cosa, ése es tu número.**

**Cascada del conteo de ADR:** ⚠️ `canon/estado-programa-v1_10.md` está **fuera de perímetro** (BARRIDO-2). **No lo edites.** Deja la línea redactada en tu nota bajo `CASCADA NO ESCRITA — colisión de perímetro con BARRIDO-2` y repórtalo en el PR. Es el mismo movimiento que #248 ya hizo, y es la causa de sus entradas T15/T16 — **espéralas y decláralas, no recongeles.**

## COMMIT 2 · Las dos filas que cambian de forma, no de estado

Ninguna se firma. Las dos siguen `ABIERTA`; lo que cambia es que pasan de indecidibles a ejecutables.

**`FP-29` — reformulada.** Instrucción de mesa, verbatim: *"Necesitamos ver qué obtuvimos, como por qué hay esas diferencias? son de diferente año? diferente tipo de cuestionario? etc. No podemos tomar una decisión así de facil."*

Reescribe `qué_se_firma` y `gatea` para que la fila diga lo que realmente falta:

> **`qué_se_firma`:** "Antes de adjudicar magnitud de confianza radial hay que resolver **la procedencia del 22%** y **alinear escalas**. Las tres cifras no son comparables tal como están: ENCUCI usa escala 0-10 con corte declarado (≥8/10); WVS, Pew y Latinobarómetro usan ítem binario. Y el 22% **no es una cifra: son tres atribuciones distintas de la misma cifra en cuatro documentos** — WVS 2018 · ENAFI/WVS · Latinobarómetro+ENAFI+LAPOP · Latinobarómetro/LAPOP (`forense/notas/2026-08-04-c06a-cinco-cifras-conf06-localizadas.md` §3.1). No se puede elegir entre tres cifras cuando una no sabe de dónde viene."
> **`gatea`:** "acto de reconciliación de instrumentos externos, especificación ya escrita en §5 y §6 de esa nota: exige series temporales de WVS/Pew/Latinobarómetro, **no** una re-corrida sobre ENCUCI — esas tres no son recalculables desde el microdato en disco. Mantiene el vínculo con `R8.3` (D-06), **con la reserva de §7 de la misma nota: reconciliar `conf.06` no le da falsador automático a `R8.3`** — el dato ENCUCI candidato tiene marca C3 contra la regla que sostiene R8.3, por circularidad."

**`FP-33` — desbloqueada.** Su texto ya no falta. **Pégalo inline en la fila** (A.3), con su procedencia declarada como **tipo (3) — recuperado de la conversación de proyecto "003 - Maestra 25 (Fable)", 12/ago/2026, no del repo**:

> **Las cuatro preguntas de U3/DOC-BACKFILL:** (1) **ficha RNM abierta** — url + fecha + qué campos `NO_DETERMINADO`/inferidos quedaron resueltos, con atención a `periodo_levantamiento`, `periodo_referencia_por_variable` y los nombres exactos de ponderador/estrato/conglomerado; (2) **indicadores de calidad** — existen o no en su catálogo, con URL, y si aparecen nuevos se suman a la cola de EV-1; (3) **diseño muestral oficial vs inferido**, por producción que la use; (4) **`NO-ENCONTRADO` en su cadena cuyo universo no incluyera el nivel documental** — *"solo si gatea algo vivo se reabre; si no, una línea y se queda"*.
> **Población — cerrada por criterio, no por lista:** las fuentes que sostienen (a) las producciones vigentes, (b) las celdas-D registradas, (c) las fichas de Hito D con acto en cola.

**⚠️ Y el aviso que la fila debe llevar escrito:** la enumeración original decía *"las 11 producciones… hoy eso es ENBIARE, ENASIC, ENIGH (2018/2022), ENCUCI, ENVIPE, ENCIG, ENFIH, ENSAFI — ocho fichas, no 958"*. **Eso es una foto del 12/ago.** Derivado hoy contra `1282ae3`: **12 producciones y 3 celdas-D**, no 11. **La población se re-deriva al ejecutar; copiar las ocho es heredar una foto vencida.** Escríbelo así en la fila.

## Lo que este acto NO hace

- **No adjudica `FP-29`.** Solo la vuelve ejecutable.
- **No ejecuta `FP-33`.** Solo le pega su texto.
- **No adjudica las 20 filas con par de `FP-24`.** Acto propio.
- **No ejecuta el mapeo de equivalencias de `FP-30`** sobre el corpus, ni alinea `CANONICO`. Actos propios.
- **No ejecuta la cascada al corpus** de `conf.02` ni `conf.05` — sigue pendiente desde #248.
- **No toca `tests/`, `estado-programa`, la propuesta del motor adaptativo, ni ningún archivo de BARRIDO-2.**

## Cierre

`python3 tests/check.py --baseline` **antes y después**, cifra en ambas. **Espera ROJO** y decláralo: T22 imprimirá los cambios de fila (señal, no defecto) y T15/T16 seguirán rojos por la cascada de ADR que no puedes escribir. **No recongeles** — `--freeze` exige ADR de mesa (ADR-76(f)) y este acto no lo trae firmado.

**Reporta el conteo de entradas nuevas por test, no agregado.** #248 reportó 8 y la corrida real dio 11: dos de las suyas —`T02` por colisión de nombre y `T03` por citar un archivo inexistente— eran **suyas y arreglables dentro de su perímetro**, y se le pasaron por reportar el total en bloque.

Nota en `forense/notas/2026-08-17-registra-2.md` con cada comando y su salida cruda · una entrada en `hallazgos.md` · este encargo `CONSUMIDO` con su PR · **merge local**, editor web de conflictos prohibido · `git diff --check` · **jamás te auto-fusionas**.

**Contadores del programa: 0.** Mueve el tablero a 19 `FIRMADA` y vuelve ejecutables dos filas. Ningún contador de medición sobre México. **Dilo así, sin justificarlo.**
