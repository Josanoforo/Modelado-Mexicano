# ENCARGO P2 · Cierre documental — mesa #20, 5/ago/2026

**Rama:** `claude/cierre-documental-p2-l9gxgn` · **HEAD inicial (origin/main):** `3de5a2853ad9b6f04ceace00f668848c62ae4e12` (idéntico a `origin/main`, ninguna rebase necesaria) · **Entorno:** nube (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, ADR-59(b)) · **`data/raw`:** ausente, no usada por este acto.

Premisa verificada antes de arrancar: el encargo declaraba `origin/main = a7f807e` (PR #125); al fusionarse `origin/main` ya traía dos commits más allá, incluyendo el merge de PR #124 (`ENCARGO M-5: sella conf.06 con ADR-64`). Confirmado contra el archivo: `canon/gobernanza-v1_15.md` cabecera ya declaraba **64 ADR** antes de este acto — M-5 estaba en `main`, condición de arranque satisfecha. No fue PARO: se re-derivó el ADR máximo (64) con la receta de T15 en vez de asumir el 63 declarado por el encargo.

Concurrencia viva derivada: `git branch -r` solo listaba `origin/main` y `origin/claude/cierre-documental-p2-l9gxgn` — ningún otro acto (`A5` incluido) tenía rama remota visible en el momento del arranque.

## Tarea 1 · Sella `[MESA-X]` — ADR-65

Citas verbatim de `forense/notas/2026-08-04-x-condicionamiento-y-forma.md`, con línea, usadas para el ADR:

- **W1, líneas 460-465:** *"ninguno de los tres ítems traza una curva monótona. `AP5_1_1` sube de 0 a un pico en 4 (18.01%) y luego baja de forma irregular hasta 9 (5.70%); `AP5_1_2` tiene un mínimo aislado en 2 (5.56%, `n`=219)... luego se aplana 11-15% en 5-10; `AP5_1_3` sube de 0 a un pico en 1-2 (≈18.5%) y baja de forma más regular después"*.
- **W1, líneas 466-467:** *"El corte `≥6` de W no coincide con un salto visible en ninguno de los tres — no hay escalón entre el nivel 5 y el 6 en ninguna de las tres columnas."*
- **§6, líneas 541-542:** *"W1: pendiente descendente débil, ruidosa, no monótona en ninguno de los tres ítems — ni recta, ni S, ni escalón visible en el corte `≥6` (§5.1)."*
- **W2, §4.2, líneas 387-391:** *"las cuatro celdas del único eje estricto disponible tienen signo positivo y distinguible de cero al 95% — signo opuesto al marginal (−0.0645), en las cuatro celdas, sin una sola excepción. No es un debilitamiento del marginal: es una reversión completa de signo, consistente en las cuatro celdas de edad."*
- **W2, §5.2, línea 486:** *"la curva más limpia de todo el acto"*.
- **W2, §5.2, líneas 489-494:** *"esta curva agrega sobre todas las edades sin condicionar, y §4.2 ya mostró que, dentro de cada tramo de edad, el signo de la relación... se invierte... La limpieza de esta curva marginal es compatible con ser, ella también, un artefacto de composición por edad — no lo contradice, lo redondea"*.
- **W3, §5.3, línea 500:** *"No aplica — `p9_9_4` es binario. Declarado en §2, no forzado aquí."*
- **§6, líneas 548-550:** *"Ninguna forma se declara ganadora — no le corresponde a este acto (§2.1). La mesa lee las tablas de §5 con la advertencia explícita de §5.2 sobre W2."*

ADR-65 escrito en `canon/gobernanza-v1_15.md` (tras ADR-64, sección §4), con las cuatro cláusulas del encargo: W1 sin forma, W2 casi recta pero compatible con artefacto de composición, W3 no aplica, y la conclusión de que leer la forma NO destraba los 15 β. **No** declara ninguna forma por descarte — cita `canon/modelo-decision-v4_0.md:149` (*"La forma funcional NO se inventa en este acto... Donde no hay evidencia, la condicional queda declarada con forma PENDIENTE"*). **No** cierra `D-ABC` — cita `milpa/procedencia.yaml:780` (*"ningún ADR de D-ABC ha sellado función de enlace a la fecha de este commit"*), decisión de mesa pendiente y distinta.

Cascada (receta T15, escanea `canon/*.md`): conteo de ADR 64→65 en `gobernanza-v1_15.md:2` (cabecera) y `estado-programa-v1_10.md:27,99`. Ningún contador de Hito D, condicionales o coeficientes se mueve.

## Tarea 2 · `instrucciones-proyecto-v2_5.md`

`sha256` de `instrucciones-proyecto-v2_4.md` sin tocar: `d71a2351afc270b25563cd8fa7d30a9c7302c57bcc63299c1a67db800f5bcf65` (idéntico antes y después de crear v2.5 — el archivo no se editó). `diff` entre v2.4 y v2.5 acotado a exactamente dos cambios: (1) el número de versión de la cabecera (`v2.4`→`v2.5`, necesario, el archivo se llama distinto) y (2) un bloque nuevo apendizado al final, "Bloque D-bis · Delta v2.5", con los tres deltas del encargo (A.1 verificación de payloads uno por `--id`, A.2 firma de entorno de tres partes, A.3 encargos vivos viven en el repo). Ninguna línea existente de v2.4 se modificó ni se borró — verificado con `diff` línea por línea, no solo por hash.

## Tarea 3 · Cierre parcial de `I-07`

Sitios `T20:HITO-D` derivados con `grep -rc "T20:HITO-D" README.md canon/*.md`: `README.md:1` · `estado-programa-v1_10.md:2` · `gobernanza-v1_15.md:2` · `modelo-decision-v4_0.md:3` — **total 8**, igual al valor que el encargo citaba (sin cambio). `I-07` (`gobernanza:362`) se cierra con la redacción parcial que la evidencia admite: `T20` vigila los ocho sitios marcados; un contador escrito sin marca sigue siendo invisible, límite declarado del propio test, no una falla del test. Entrada añadida al final de `forense/bitacora.md` (append-only, `merge=union`), sin reordenar ni tocar entradas previas.

## Tarea 4 · `forense/encargos/`

Directorio creado con `forense/encargos/convencion.md` (documenta cabecera obligatoria — SHA de redacción, entorno asignado, estado `VIVO`/`CONSUMIDO` — y el ciclo de vida de A.3). **Nombrado `convencion.md` y no `README.md`**: un primer intento con `README.md` chocó con `T02` (nombre normalizado colisiona con el `README.md` de la raíz — `norm()` de T02 ignora el directorio, solo compara el nombre base) y se corrigió antes de commitear, verificado con `check.py` en VERDE después. No se pobló con encargos concretos — mesa los añade después.

## Cierre — `check.py --baseline`

Antes (origin/main, sin mis cambios, corrida real sin `--baseline`): **18 FAIL · 95 WARN**. Después (con las cuatro tareas aplicadas): **18 FAIL · 95 WARN**, idéntico. `--baseline` da **VERDE** — nada nuevo frente a `tests/baseline.json` (HEAD congelado `837d5fe`). `T13` (cabecera de versión): 1 warning pre-existente (`canon/integrador-psicologia-mexicano.md`, ya en baseline, no tocado por este acto) — se verificó holgura antes de escribir en `gobernanza`: los marcadores `**ARCHIVO**`/`**NOMBRE ESTABLE**` caen en los caracteres 155 y 631 del archivo, muy por debajo del corte de 2500 que `T13` lee, y toda la prosa nueva de ADR-65 se escribió en el cuerpo (§4) y en `§0.1`/cabecera solo como referencia de una línea, no como prosa de ADR. `T15` (T-ADR-COUNT): ok, 65 únicos, sin huecos, sin duplicados. `T20` (T-CASCADA-MARCADA): ok.

No impidió medir. Contadores movidos: 0.
