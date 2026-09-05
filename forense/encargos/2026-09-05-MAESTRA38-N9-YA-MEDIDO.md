ENCARGO · ACTO MAESTRA38-N9 · YA-MEDIDO — invoca /acto
SHA: 25383f35 · COMPUERTA: ninguna · ENTORNO: NUBE · NO en CAJA · MODELO: Sonnet. CARRILES: N10 (sólo notas y forense/prereg-caja/; N9 no escribe ahí).
FIRMA — verbatim (4/sep): «Revisa nuevamente los PRs mergeados y dame los siguientes encargos en nube.» Defecto real que justifica el test (impuesto v2.3): N5 clasificó 2 de 9 reglas como SIN-INSTRUMENTO teniendo medición (N6 lo corrigió); N7 recibió un encargo que llamaba «territorio virgen» a dos id con falsaciones corridas dos días antes. Ambos, 4/sep/2026.
A.8 contra 25383f35: ls tools/ | grep -c ya_medido → 0. Fuentes que hay que cruzar, todas en repo: milpa/tramite.yaml (20), milpa/tramite-ola5-propuesta-v0.yaml (entradas por id con situacion/tier/veredicto), canon/modelo-decision-v4_0.md §7 (enmiendas por regla), forense/notas/*-L*-*.md (celdas y veredictos por id), forense/prereg-caja/S*-spec-*.md (specs selladas). FP-301 ABIERTA con #537 fusionado.
SPEC (un PR, un ADR):
P1 · tools/ya_medido.py <id-de-regla|R-n>: imprime, por fuente, cada aparición con archivo:línea, situacion/tier/veredicto/p si existe, y una línea final NUNCA-MEDIDA / MEDIDA-EN: …. Sin heurística de parecido: match por id exacto y por R-n del canon; alias sólo los que ya estén en canon/registro-rotulos.tsv. Control positivo: los dos id de N7 devuelven L9/L11; control negativo: familia.cortejo.urbano_joven_apps devuelve sólo la hipótesis de N6.
P2 · .claude/commands/mapea.md y acto.md (verificación de existencia): todo acto que clasifique, pre-registre, cargue o selle una regla pega la salida de ya_medido.py en su A.8 — una línea de regla, sin compuerta nueva. T-YAMEDIDO en check.py: FAIL si un encargo bajo forense/encargos/ con fecha ≥ hoy cita un id de regla en su SPEC y no trae la salida de la herramienta (docstring con los dos defectos).
P3 · FP-301 → FIRMADA-POR-MERGE (#537); hallazgos: una línea (patrón repetido dos veces).
PERÍMETRO. Toca: tools/ya_medido.py (nuevo) · tests/check.py · .claude/commands/{mapea,acto}.md · tablero · hallazgos · INFRAESTRUCTURA · A.3 · cascada. NO toca: milpa/** · canon (salvo ADR) · data/** · forense/prereg-caja/. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR: ADR-340 · FP-302 recibo. CONTADOR: herramientas de lectura previa 0 → 1 · abiertas 4 → 3 · medición: cero.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N9 · YA-MEDIDO` (5/sep/2026, entorno NUBE, rama
`claude/ya-medido-audit-tool-lrmrh7`), SHA de redacción `25383f35` (=
`origin/main` exacto al arrancar, sin desfase).

**P1.** `tools/ya_medido.py <id-de-regla|R-n>` (nuevo). Cruza mecánicamente
`milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`,
`canon/modelo-decision-v4_0.md` §7, `forense/notas/*-L*-*.md` y
`forense/prereg-caja/S*-spec-*.md`; imprime por fuente cada aparición con
`archivo:línea` y los campos `situacion`/`tier`/`veredicto`/`p` que traiga, y
cierra con una sola línea `NUNCA-MEDIDA` o `MEDIDA-EN: <habitantes>`. Sin
heurística de parecido: el match es por `id` exacto y por `R-n` exacto — la
única equivalencia entre ambos que el script conoce sale del registro
congelado de `tests/validador_registro_ids.py` (ancla cada `R-n` a su regla
de §3 por subcadena estable, no por posición ni por parecido de texto)
cruzado con el tag `**id:**` que esa misma regla ya trae en el canon; nunca
se inventa una equivalencia. El alias adicional vía `canon/registro-
rotulos.tsv` es solo el que esa tabla ya declaraba.

**Control positivo, verificado.** `civico.voto.clientelar_si_observable` y
`civico.protesta.agravio_urbano` (los dos `id` que el encargo de `N7` trató
como territorio virgen) devuelven `MEDIDA-EN:` citando `L9`/`L11` —
resueltos vía `R7.6`/`R7.4` del canon, que sí aparecen literalmente en
`forense/notas/2026-09-02-MAESTRA35-{L9,L11}-*.md` con veredicto real
(`CONTRARIA`/`CORROBORADA-PARCIAL`), aunque el `id` punteado completo no
aparece ahí verbatim — el puente `id`↔`R-n` es justamente lo que hace falta
para que el control positivo funcione, y por diseño no es una heurística de
parecido: sale del registro congelado + el tag `**id:**` del propio canon,
ambos ya existentes en el repo. **Control negativo, verificado.**
`familia.cortejo.urbano_joven_apps` (`R5.4`) devuelve `NUNCA-MEDIDA` — su
única aparición con algún campo es la entrada `HIPÓTESIS-SIN-INSTRUMENTO` que
`MAESTRA38-N6` cargó por `FP-298` en `milpa/tramite-ola5-propuesta-v0.yaml`,
sin ningún veredicto real en ninguna de las cinco fuentes.

**Ajuste sobre la marcha, declarado (A.8/D-13).** Una primera versión del
detector de "veredicto real" buscaba el vocabulario `B-bis`
(`CONTRARIA`/`CORROBORADA`/etc.) en todo el bloque de YAML o en toda la línea
de `canon/modelo-decision-v4_0.md` §7 que contuviera el término buscado —
verificado que esto daba **falso `MEDIDA-EN`** para el propio control
negativo: un bloque de YAML vecino (`tramite.gobierno_digital.
coercitivo_tabla_de_universos`, líneas 3059-3198) trae, en un comentario de
cierre que en realidad describe las tres entradas SIGUIENTES, la cadena
literal `"R5.4"` junto con un veredicto real (`AMBIGUA-POR-UNIVERSO`) de
OTRA regla; el mismo patrón aparece en el párrafo `FP-298` de §7, que
menciona `R5.4` y, más adelante en el mismo párrafo, `CONTRARIA-REPLICADA`
de `R7.3`. Corregido acotando la búsqueda de veredicto a una ventana de
texto centrada en la aparición real del término (`_ventana_de_terminos`,
±260 caracteres) en vez del bloque/línea completos — verificado de nuevo
contra los tres controles tras el fix, sin falsos positivos.

**P2.** `.claude/commands/mapea.md` §4 (junto a la definición de
`HIPÓTESIS-SIN-INSTRUMENTO`, que ya narraba el defecto de `N5`) y
`.claude/commands/acto.md` ARRANQUE (junto a A.8 contra la raíz): todo acto
que clasifique/pre-registre/cargue/selle una regla pega la salida de
`ya_medido.py` en su A.8 — una línea de regla, sin compuerta nueva, tal como
pedía el `SPEC`. `T30`/`T-YAMEDIDO` en `tests/check.py`: `FAIL` si un
encargo archivado bajo `forense/encargos/` (no `cola/`, que todavía no se
ejecutó) con fecha de archivo ≥ hoy cita, en su cuerpo, un `id` de regla
(diez dominios registrados como tag `**id:**` en el canon) o un `R-n`, y ese
mismo archivo no trae `NUNCA-MEDIDA`/`MEDIDA-EN:` — con un allowlist
declarado (`_T_YAMEDIDO_ARCHIVOS_CONOCIDOS`, mismo patrón que
`_T25_ARCHIVOS_CONOCIDOS`) para citas ilustrativas. Este mismo encargo cita
`familia.cortejo.urbano_joven_apps` en su propio control negativo (línea 6,
arriba) — verificado que el texto del `SPEC` ya contiene, por describir el
formato de salida esperado ("una línea final `NUNCA-MEDIDA`/`MEDIDA-EN:`"),
las dos marcas que `T30` busca, así que en la práctica pasaría igual sin el
allowlist; se declara la entrada de todas formas porque la cita no es una
salida genuina de la herramienta —que no existía cuando este texto se
escribió— y la honestidad de esa distinción vale más que el ahorro de una
línea.

**P3.** `forense/firmas-pendientes.tsv`: `FP-301` (recibo de `MAESTRA38-N8`)
recifrada `ABIERTA`→`FIRMADA-POR-MERGE` — `PR #537` (que la propia fila ya
declaraba como su firma, regla 1 de maestra-34) verificado fusionado contra
`origin/main` = `25383f35` (`git log -1`). `FP-302` (recibo de este acto,
nueva). `forense/hallazgos.md`: una línea nombrando el patrón repetido dos
veces (`MAESTRA38-N5`, `MAESTRA38-N7`) que este acto instrumenta, distinta
de las dos "reglas candidatas, no instrumentadas aquí" que la preceden.

**Efecto colateral de P3, corregido en la misma cascada (A.8).** Recifrar
`FP-301` a un estado que `T22` (`tests/check.py`) no reconocía como terminal
(`("ABIERTA", "FIRMADA")` es el único filtro que esa función usa) sacó a
`canon/estado-programa-v1_12.md` y a
`forense/encargos/2026-09-04-MAESTRA38-N8-ESTADO-PROGRAMA-v1_12.md` del
conjunto de archivos "citados" por una fila `ABIERTA`/`FIRMADA` —
`python3 tests/check.py --baseline` dio **ROJO** (2 entradas nuevas de
`T22`) al medirlo antes de commitear. Corregido declarando ambos archivos en
`_T22_ARCHIVOS_CONOCIDOS`, no ampliando el filtro de estados de `T22` (que
tampoco reconoce las otras variantes `FIRMADA-*` ya en uso y no se auditaron
aquí).

**Cascada.** `canon/gobernanza-v1_15.md`: `ADR-340` (candidato derivado por
el comando de la casa contra el máximo real `339`, contiguo — coincide con
el que este mismo encargo ya citaba, sin colisión ni renumeración);
cabecera de conteo `339`→`340 ADR`. `canon/estado-programa-v1_12.md`: `L0`
gana la anotación de `ADR-340` (insertada antes de la de `ADR-339`, sin
reescribirla) y sube `339`→`340 ADR`; la cabecera de conteo de `gobernanza`
en la tabla de fuentes (línea 27) recifrada igual — verificado que dejarla
en `339` dispara `T15` (`{n} ADR; gobernanza tiene {real} únicos`) antes de
corregirlo. `canon/registro-rotulos.tsv`: fila `MAESTRA38-N9` censada, junto
a `N2`/`N3`/`N4`/`N6`/`N8` (`N5`/`N7` no tienen fila propia — gap
preexistente, fuera de perímetro de esta pieza reparar).
`data/INFRAESTRUCTURA-v1_0.md`: sección nueva para `tools/ya_medido.py`.
`forense/tablero/TABLERO-PROGRAMA.md` (nota inline) y `forense/tablero/
TABLERO-PROGRAMA-v1_1.md` (§8.8): recibo de este acto.

**Qué NO decide.** No mide nada de México (medición: cero, declarado por el
propio encargo). No toca `milpa/**`, `canon/modelo-decision-v4_0.md`,
`data/**` (salvo `INFRAESTRUCTURA-v1_0.md`, explícitamente permitido) ni
`forense/prereg-caja/` — perímetro explícito respetado. No reabre ni
adjudica ninguna de las clasificaciones ya selladas de
`MAESTRA38-N5`/`N6`/`N7`: solo instrumenta, hacia adelante, el cruce que a
esos actos les faltó.

**Verificación.** `python3 tests/check.py --baseline`: **LÍNEA BASE VERDE**,
3 FAIL / 170 WARN (171→170: `FP-301` sale del conteo de `ABIERTA` de `T22`
al recifrarse — mejora, no regresión). `T30`/`T-YAMEDIDO` y `T25`/`T-ROTULOS`
en verde. Los tres controles de `ya_medido.py` (dos positivos, uno negativo)
verificados a mano, salida citada arriba.

**Contador.** Herramientas de lectura previa `0`→`1`, cumplido. Abiertas
`4`→`3` (`FP-301` deja de estar `ABIERTA`), cumplido. Medición: cero,
cumplido — ningún commit de esta pieza abre microdato, corre censo real ni
mueve tier alguno.

PR de este acto, contra `main`.
