ADENDA · ACTO GEN2-RELEVO-USOS-1 · REGLA DE ADOPCIÓN EN BLOQUE

CABECERA DE ARCHIVO (A.3 / `forense/encargos/convencion.md`) — la escribe el acto que archiva, **no** es texto de dirección. El texto de dirección va íntegro abajo, verbatim, bajo la línea `PIEZA DE DIRECCIÓN`.

- **SHA de redacción** — archivado contra `582d4e9` (`origin/main`, merge de `PR #779`, `ACTO GEN2-MEDICION-DEMANDA-1`), 0 commits detrás en el momento del archivo.
- **Entorno asignado** — no lo fija esta pieza: hereda el del `ACTO GEN2-RELEVO-USOS-1`, cuyo encargo **todavía no existe en el árbol** (ver A.8 (2) abajo). Esta adenda **no** es un encargo despachable por sí sola y por eso **no** va a `forense/encargos/cola/`: gobierna el `P4` de otro acto.
- **Estado** — `VIVO`.
- **Compuerta que la propia pieza declara** — «aplica en cuanto abra tu compuerta de `P4`, el merge de `FIRMAS-MESA-1`». Ninguno de los dos rótulos existe hoy en el árbol; la pieza llega **antes** que el acto que gobierna.
- **Procedencia del texto** — archivo entregado por mesa en la sesión de la nube del 15/sep/2026, `sha256 = 23ad347ecaffb2bc9dde008837c478cc7e939549676ce487a366f3fb774b31aa` (4 898 bytes, 31 líneas). Se copia **verbatim**: sin resumir, sin corregir, sin reordenar.
- **Rótulos censados en `canon/registro-rotulos.tsv` por este archivo** — ninguno. `GEN2-RELEVO-USOS-1`, `FIRMAS-MESA-1` y `SELLA-3` no son de la serie `MAESTRA<nn>-<letra><n>` que `/encola` §3 censa, y la casa censa el rótulo de un acto **al cerrarlo**, con su ADR y su PR — no al encolar su instrucción. Censarlo aquí declararía un habitante que todavía no vive.

VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2 — contestada por quien archiva, contra `582d4e9`, con comando):

**(1) ¿Existe ya la estructura?** SÍ, completa, y la pieza no inventa ninguna pieza de maquinaria:

```
$ ls data/corrida0/demanda-resultados.tsv data/corrida0/decisiones.tsv milpa/procedencia.yaml forense/hallazgos.md
data/corrida0/decisiones.tsv   data/corrida0/demanda-resultados.tsv
forense/hallazgos.md           milpa/procedencia.yaml
$ python3 tools/corrida0.py delta --help | head -2
usage: corrida0 delta [-h] --entrada PARES.yaml [--formato {humano,json,tsv}]
                      [--salida-dir DIRECTORIO]
```

`corrida0 delta` **está implementado** y ya pide exactamente el contrato que la regla exige («contrato `GEN2-DELTA-1` con ambos objetos, uso y comparabilidad» = «hashes, uso y contrato explícitos — nunca a mano»). Discrepancia **no material** declarada, no corregida aquí (fuera de perímetro): la cabecera de `tools/corrida0.py` sigue listando `delta` y `vigencia` como declarados y vacíos, a la espera del `ACTO GEN2-E7`, texto que el propio árbol contradice. `demanda-resultados.tsv` trae hoy **207 slots** (209 líneas − cabecera `# DERIVADO — NO EDITAR` − fila de columnas), con `consumidor`, `valor_legacy`, `escala_legacy`, `clase_legacy`, `corrida_natural`, `estado`, `vigencia` y `validacion_independiente` ya como columnas. `decisiones.tsv` tiene las cuatro columnas (`objeto`, `decision`, `fuente`, `fecha`) que el paso 1 de PROPAGACIÓN usa.

**(2) ¿Existe ya el contenido?** NO, en las dos direcciones que importan, y por eso esto se archiva en vez de ejecutarse:

```
$ grep -rl "RELEVO-USOS" --include=*.md --include=*.tsv --include=*.py .   # 0 líneas
$ grep -rl "FIRMAS-MESA-1" . | grep -v '^\./\.git'                        # 0 líneas
$ grep -n "PARA-v2.14" forense/hallazgos.md                               # 0 líneas
```

Ni `ACTO GEN2-RELEVO-USOS-1` ni `FIRMAS-MESA-1` existen en el árbol: no hay `P4` que propagar ni compuerta que pueda abrirse hoy. `PARA-v2.14` tampoco existe todavía — `instrucciones_vigentes` es v2.13, entregada íntegra el 8/sep/2026 (`ACTO GEN2-V213`), y la última serie acumulada, `PARA-v2.13`, quedó absorbida por esa entrega. La entrada `PARA-v2.14` que pide el paso 2 de PROPAGACIÓN sería la **primera** de su serie.

**(3) Cobertura retroactiva.** No hay nada retroactivo que cubrir: la pieza **precisa** `E.2`, no la sustituye. `E.2` vive en `instrucciones-proyecto-v2_13.md:446` y ya fija las tres preguntas que no se colapsan, con la tercera verbatim: *«¿se adopta? (humana, por merge de mesa)»* — que es el gozne sobre el que la regla apoya «el merge de mesa del PR que trae un bloque ES la adopción de ese bloque». Ningún slot de `demanda-resultados.tsv` se reclasifica por archivar esto, y ninguna adopción pasada se revisa: la regla gobierna relevos futuros.

LO QUE ESTE ARCHIVO NO HACE. No ejecuta el `P4` (no hay acto que lo tenga). No abre fila en `data/corrida0/decisiones.tsv`, no deriva ADR, no escribe `PARA-v2.14`, no clasifica ningún slot en bin 1/2/3, no toca `demanda-resultados.tsv` ni `usos.tsv` ni `milpa/`. No redacta el encargo de `ACTO GEN2-RELEVO-USOS-1` ni el de `FIRMAS-MESA-1` — eso es de dirección. Sólo fija el texto por `A.3`, para que cuando el acto se lance su `P4` encuentre la regla en el árbol y no en una conversación.

---

PIEZA DE DIRECCIÓN — verbatim, tal como llegó:

════ ADENDA · ACTO GEN2-RELEVO-USOS-1 · REGLA DE ADOPCIÓN EN BLOQUE (gobierna tu P4) ════
(dirección, 15/sep/2026 · la firma viaja adentro, verbatim; el ejecutor PROPAGA, no decide — SELLA-3 · aplica en cuanto abra tu compuerta de P4, el merge de FIRMAS-MESA-1)

FIRMA DE MESA, mesa, 15 de septiembre de 2026 — verbatim: «Pues si, la regla de adopción en bloque es lo que nos permitirá dejar de enfocarnos en transacción y movernos a esta otra fase más estratégica y de cálculo.»
OBJETO: se adopta la REGLA DE ADOPCIÓN EN BLOQUE de abajo para los relevos GEN1→GEN2 de slots demandados; el merge de mesa del PR que trae un bloque ES la adopción de ese bloque (E.2: «¿se adopta? — humana, por merge»). Resuelve el gobierno de adopción para `demanda-resultados.tsv`; no toca E.2/E.3/E.4, las precisa.

── LA REGLA ──────────────────────────────────────────────────────────────────

Ámbito. Todo slot de `demanda-resultados.tsv` (consumidor + resultado legacy) para el que existe un RESULT GEN2 SELLADO en su corrida natural y un delta legacy→GEN2 calculado por `corrida0 delta` (hashes, uso y contrato explícitos — nunca a mano). Sin delta por script no hay relevo, en ningún bin.

Tres bins, y ningún relevo queda fuera de ellos:

1 · NO-MATERIAL — entra al PR en bloque; el merge lo adopta. Las tres condiciones a la vez: (i) mismo signo; (ii) el punto GEN2 no dispara la cláusula del consumidor: si el consumidor declara `se_mueve_si`, ésa manda; si no, el punto GEN2 cae dentro del IC declarado del legacy; (iii) el slot no es un coeficiente del generador (`procedencia.yaml`), ni una regla con p medida, ni insumo del marcador (M/R/L/agregado) — ésos son siempre bin 2.

2 · MATERIAL — un renglón por slot en la lista a mesa, con el delta a la vista; firma individual. Cae aquí lo que cambia signo, tier, clasificación o dispara `se_mueve_si`, y todo lo del inciso (iii), aunque el delta sea cero: para el generador y el marcador, la adopción se firma aunque no cambie nada, porque cambia quién manda.

3 · SIN-CRITERIO — el consumidor no declara `se_mueve_si` y el legacy no trae IC: no hay con qué decir "no material". Se agrupan en un bloque aparte con la tabla de deltas (valor legacy, valor GEN2, delta, escala, universo) y mesa firma ese bloque de una vez o lo devuelve. No se cuelan al bin 1 por defecto ni se degradan al bin 2 uno por uno: eso es el modo de falla de transacción que esta regla existe para cerrar.

Invariantes, sin excepción:
- Escala y universo declarados por pareja (A-bis 3 y 4): un delta entre escalas distintas o entre universos distintos (poblacional vs. subpoblación) no es un delta — va a bin 3 con la razón escrita. Nunca "difiere en Z%" entre escalas.
- Cada slot adoptado deja: fila de uso en el registro derivado (escritor canónico), cita `corrida0_*` en el consumidor, delta citado. Adoptar no es validar (E.2, tres preguntas): la validación independiente sigue reservada a lo que puede cambiar signo, tier, clasificación, marcador o coeficiente — es decir, al bin 2.
- Los replays de GEN1 no relevan nada (`cuenta_gen2 = NO`). Un bloque nunca reescribe un sello: si el legacy queda SUPERADO, es estado del registro derivado, no edición de su archivo.
- El PR del bloque lista todos los slots que adopta, uno por línea, con su bin: es lo que mesa firma al fusionar, y lo que un auditor puede leer sin reconstruir nada.

Falsador y caducidad (mismo criterio que A.3/A.8/A.9/A.10/A.12/A.13). Si en tres meses un slot adoptado por bin 1 resulta haber cambiado tier, signo o clasificación sin que la regla lo atrapara, la regla se estrecha (no se retira) y el caso se cita. Si en tres meses ningún bloque se ha fusionado, la regla no sirvió y se anota.

── PROPAGACIÓN (P4, tras tu compuerta) ────────────────────────────────────────
1 · Fila en `decisiones.tsv` con la firma verbatim de arriba y esta regla como OBJETO.
2 · ADR derivado por el comando de la casa en tu cascada, y una entrada `PARA-v2.14` en `forense/hallazgos.md` con el texto de la regla: las instrucciones se entregan por versión íntegra (firma de mesa del 2/sep), no se pegan enmiendas.
3 · Tus tres listas al cierre, con conteos derivados y no tecleados: bin 1 (adoptados por este merge), bin 2 (a mesa, uno por uno), bin 3 (bloque a mesa con tabla). `## NO-CORRIDO / RESERVAS` declara todo slot que no cupo en ningún bin y por qué.
════════════════════════════════════════════════════════════════════════════════

---

ENMIENDA FECHADA (15/sep/2026, mismo día, tras el merge de `PR #785`) — **la compuerta abrió**. Append puro: nada por encima de esta línea se edita, y el texto de dirección de arriba queda íntegro en su sitio. Verificación del bloque verbatim, ahora que ya no es el pie del archivo: `sed -n '45,75p' <este archivo> | sha256sum` debe dar `23ad347ecaffb2bc9dde008837c478cc7e939549676ce487a366f3fb774b31aa`.

Re-verificado contra `5973f12` (`origin/main`, merge de `PR #785`). De las tres inexistencias que el bloque A.8 contestó contra `582d4e9`, **una cayó y dos siguen en pie**:

- **`FIRMAS-MESA-1` YA EXISTE y YA FUSIONÓ.** `PR #785` **es** el `ACTO GEN2-FIRMAS-MESA-1` (`forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-1.md`, cierre en `forense/notas/2026-09-15-GEN2-FIRMAS-MESA-1-cierre.md`, `ADR-513`). Es exactamente la compuerta que esta adenda nombra: «aplica en cuanto abra tu compuerta de `P4`, el merge de `FIRMAS-MESA-1`». **La regla de adopción en bloque está vigente desde este merge.** El «NO» de A.8 (2) era cierto contra `582d4e9` y se conserva ahí por su valor de auditoría — no se reescribe, se fecha.
- **`ACTO GEN2-RELEVO-USOS-1` sigue sin existir** (`git grep -l "RELEVO-USOS" 5973f12` → 0 líneas). La compuerta abrió sobre un `P4` que todavía no tiene encargo: la regla está vigente y **no hay quién la propague**. Éste es hoy el único bloqueo real; lo levanta dirección lanzando el acto.
- **`PARA-v2.14` sigue sin existir** (0 líneas en `forense/hallazgos.md`): seguiría siendo la primera entrada de su serie.

Lo que `PR #785` movió y que la regla tendrá que leer cuando su `P4` corra:

- **`corrida0 delta` intacto y sigue implementado.** Los `+30` de `tools/corrida0.py` tocan `cmd_demanda` y `status`, no `delta`; el contrato `--entrada PARES.yaml` es el mismo.
- **El universo no cambió de tamaño: siguen 207 slots, los 207 en `estado = PENDIENTE`**, y siguen 58 con `escala_legacy = NO-DECLARADO-EN-EL-REGISTRO`. La cuenta de «legacy sin IC propio» subió de **14 a 18**.
- **Los 7 coeficientes del generador ya vienen rotulados.** `OBJETO 5` (D3 de `NC-0197`) hace que `cmd_demanda` anteponga `SIN-PROCEDENCIA-VERIFICABLE·` al `clase_legacy` de los 7 `milpa/procedencia.yaml:coeficientes_generador_sellados:*` que `decisiones.tsv` marca. Son bin 2 por el inciso (iii) de la regla, y ahora se pueden seleccionar por rótulo en vez de a ojo.
- **Aparece un estado que los tres bins no cubren.** `OBJETO 2` (`NC-0168`) autoriza `adopcion=VETADA-POR-DECISION` en `decisiones.tsv`, hoy sobre `RESULT-C1-POSEL-AMENAZA-VEREDICTO` y `RESULT-C1-POSEL-OFERTA-VEREDICTO`, y `corrida0 status` los cuenta aparte precisamente para que dejen de leerse como cola de adopción. Un slot vetado no es bin 1 (lo adoptaría el merge), ni bin 2 (no se firma uno por uno lo que mesa ya prohibió adoptar), ni bin 3 (no es falta de criterio: es criterio en contra). La regla dice «ningún relevo queda fuera de ellos»; con el veto vigente eso ya no se sostiene sin una cuarta salida. Mientras dirección no la escriba, el `P4` los declara en `## NO-CORRIDO / RESERVAS`, que es lo que el propio paso 3 de PROPAGACIÓN manda para «todo slot que no cupo en ningún bin y por qué». **Decisión de dirección, no del ejecutor.**

---

CORRECCIÓN FECHADA (15/sep/2026, mismo día) — **la cifra «sin IC propio: 14 → 18» de la enmienda de arriba es FALSA y queda retirada.** Append puro, como la anterior: nada por encima se edita, y el bloque verbatim de mesa sigue siendo `sed -n '45,75p'` → `23ad347ecaffb2bc9dde008837c478cc7e939549676ce487a366f3fb774b31aa`.

La levanta la RESERVA de la revisión adversarial de `PR #786` (`VEREDICTO: FUSIONABLE-CON-RESERVA`, 0 BLOQUEA · 1 RESERVA, punto 2.5): la cifra no era re-derivable con un comando. Al buscarle el comando resultó que además **no era cierta**.

**No hubo alza. La cuenta es 18 en las tres bases**, y el comando que la re-deriva es:

```
$ for SHA in 582d4e9 5973f12 15423d0; do \
    git show $SHA:data/corrida0/demanda-resultados.tsv \
    | awk -F'\t' 'NR>2{print $6}' | grep -c "sin IC propio"; done
18
18
18
```

**De dónde salió el «14».** De un `awk … | sort | uniq -c | sort -rn | head -6` sobre `clase_legacy`: ese `14` es el conteo de **un solo** valor, `DERIVADO de R, M y L -- sin IC propio`. Hay un **segundo** valor que también dice `sin IC propio` — `DERIVADO de A, B y A∪B de MAESTRA34-L5 P4 -- sin IC propio; no es MEDIDO`, 4 slots — que el `head -6` dejó fuera del cuadro. Se comparó un conteo por valor contra un total y se leyó como movimiento lo que era un artefacto del truncamiento. El defecto es de quien archiva, no del texto de mesa, que no cita ninguna cifra.

**Qué cambia para la regla.** La dirección del hallazgo: la carga del bin 3 **no creció con `PR #785`**. Sigue siendo la misma de antes — 58 slots con `escala_legacy = NO-DECLARADO-EN-EL-REGISTRO` más 18 sin IC propio, sobre 207. Lo que la enmienda decía sobre el tamaño del problema se sostiene; lo que decía sobre su *movimiento*, no.

**Las demás cifras se re-verificaron contra `15423d0`** (`origin/main` tras `PR #787` y `PR #782`, que no tocan `demanda-resultados.tsv`, `decisiones.tsv` ni `tools/corrida0.py`) y **todas siguen exactas**: 207 slots, los 207 en `estado = PENDIENTE`, 58 con `escala_legacy = NO-DECLARADO-EN-EL-REGISTRO`, 7 con `SIN-PROCEDENCIA-VERIFICABLE` en `clase_legacy`. `ACTO GEN2-RELEVO-USOS-1` y `PARA-v2.14` siguen sin existir en `15423d0` (0 líneas cada uno).

---

SEGUNDA CORRECCIÓN FECHADA (15/sep/2026) — **el `ACTO GEN2-RELEVO-USOS-1` existe, fusionó, y su `P4` YA CORRIÓ — sin esta regla.** Append puro; el bloque verbatim de mesa sigue siendo `sed -n '45,75p'` → `23ad347ecaffb2bc9dde008837c478cc7e939549676ce487a366f3fb774b31aa`.

Queda retirado lo que la enmienda anterior daba por cierto: «`ACTO GEN2-RELEVO-USOS-1` sigue sin existir … la compuerta abrió sobre un `P4` que todavía no tiene encargo … éste es hoy el único bloqueo real». Era cierto contra `15423d0` y dejó de serlo con el merge de `PR #788` (`eba9fd2`): `forense/encargos/2026-09-15-GEN2-RELEVO-USOS-1.md`, `forense/notas/2026-09-15-GEN2-RELEVO-USOS-1-cierre.md`, `ADR-514`, `forense/relevo-usos/`.

**Por qué corrió sin la regla.** Esta adenda nunca estuvo en el árbol: vive en `PR #786`, sin fusionar. El acto no podía leerla. Ejecutó la regla **inline de su propio encargo** (línea 13): «los NO-MATERIALES entran en bloque al PR; los MATERIALES se sirven a mesa como lista, uno por uno, con su delta» — dos bins, no tres. No es defecto del ejecutor.

**Lo que el acto SÍ cumplió de esta regla, sin conocerla.** El delta salió por script con el contrato que la regla exige: `forense/relevo-usos/relevo-usos-pares-v1_0.yaml` declara `version: GEN2-DELTA-1` y dice, verbatim, «ni los pares ni los hashes ni las citas se teclean» (`tools/relevo_usos.py --contrato`) — la invariante «nunca a mano» se respetó. Y el inciso (iii) del bin 2 también: «coeficiente central — entra a mesa aunque el delta sea cero».

**Los tres pasos de PROPAGACIÓN, verificados contra `origin/main`:**

| paso | qué pedía | estado |
|---|---|---|
| 1 | fila en `decisiones.tsv` con la firma verbatim y esta regla como OBJETO | **NO HECHO** — `git diff --stat 15423d0 origin/main -- data/corrida0/decisiones.tsv` vacío; la firma da 0 líneas en todo el árbol |
| 2 | ADR derivado **y** entrada `PARA-v2.14` en `forense/hallazgos.md` con el texto de la regla | **PARCIAL** — `ADR-514` existe, pero por el acto, no con esta regla como OBJETO; `PARA-v2.14` da 0 líneas |
| 3 | tres listas al cierre, con conteos derivados | **HECHO EN FORMA, NO EN DEFINICIÓN** — la nota cierra con «4 MATERIAL · 20 NO-MATERIAL · 3 NO-DETERMINABLE» (27 slots, 2 adoptados) |

**`NO-DETERMINABLE` no es el bin 3.** El bin 3 (`SIN-CRITERIO`) es «el consumidor no declara `se_mueve_si` y el legacy no trae IC: no hay con qué decir *no material*», y se firma **en bloque, de una vez, o se devuelve**. El `NO-DETERMINABLE` del acto es otra cosa: el delta no se puede calcular por falta de identidad de universo o por veredictos en conflicto (`RES-0005`, `RES-0028`, `RES-0035`). Hay solape —`RES-0028` compara `U1` contra `U4`, que por la invariante de escala/universo de esta regla iría a bin 3 con la razón escrita— pero los tres acabaron en filas `NC` individuales (`NC-0214`, `NC-0216`, `NC-0217`), es decir **degradados uno por uno**: exactamente el «modo de falla de transacción que esta regla existe para cerrar».

**Y el acto refuta el bin 1 tal como está escrito.** Su `P4` dice, verbatim: «De los 7 NO-MATERIAL pendientes, 5 tienen un sellado o una firma que prohíbe la cita … Adoptarlos por ser inmateriales habría violado `E.3` y una decisión firmada: **la materialidad no es la única compuerta.**» El bin 1 de esta regla presenta sus tres condiciones como suficientes para que el merge adopte. No lo son: un veredicto sellado (`COMPLEMENTO-CON-DENOMINADOR-RECORTADO`, `SIN CITA` de D1/`NC-0108`) prohíbe la cita con independencia de la materialidad. De 7 NO-MATERIAL pendientes se adoptaron **2**. Esto es un falsador cumplido antes de los tres meses, y por la propia cláusula de caducidad de la regla corresponde **estrecharla, no retirarla**: el bin 1 necesita una cuarta condición — que ningún sellado ni firma vigente prohíba la cita. **Decisión de dirección; aquí sólo se deja escrito.**

---

ENMIENDA FECHADA (17/sep/2026, `ACTO GEN2-TRAMITE-4`) — **paso 1 de PROPAGACIÓN (línea 72) queda HECHO por este acto.** Append puro; nada por encima se edita, y el bloque verbatim de mesa sigue siendo `sed -n '45,75p'` → `23ad347ecaffb2bc9dde008837c478cc7e939549676ce487a366f3fb774b31aa`.

De la tabla de PROPAGACIÓN que `PR #809`/`ACTO GEN2-PINS-REPRODUCE-1` dejó en `NO HECHO`/`PARCIAL` (ver la SEGUNDA CORRECCIÓN FECHADA arriba): **paso 1 — fila en `decisiones.tsv` con la firma verbatim y esta regla como OBJETO — HECHO hoy** (`data/corrida0/decisiones.tsv`, objeto `adopcion-en-bloque-v1`, 2026-09-17). **Paso 2 — ADR derivado y entrada `PARA-v2.14` en `forense/hallazgos.md`** se cierra en la misma cascada de `ACTO GEN2-TRAMITE-4`. `FP-381` (`FIRMADA`) registra la firma de mesa del 15/sep/2026 y cita `ADR-524` (`PR #809`) como su primer uso real, sin que el ejecutor de ese acto conociera el texto (esta adenda no estaba fusionada cuando corrió). **Paso 3 sigue sin tocarse**: las tres listas al cierre de `PR #809` quedan «HECHO EN FORMA, NO EN DEFINICIÓN» tal como la SEGUNDA CORRECCIÓN ya lo dejó escrito, y el falsador cumplido sobre el bin 1 (2 de 7 NO-MATERIAL adoptados, no los 7) sigue siendo decisión de dirección, no de este acto: se cita, no se resuelve aquí.
