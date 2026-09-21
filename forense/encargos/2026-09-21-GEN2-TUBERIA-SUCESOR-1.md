# ENCARGO · ACTO GEN2-TUBERIA-SUCESOR-1 · T15 ASEVERA TRES COSAS Y ACEPTA HUECOS · LA GUARDA DE SALTO DE LÍNEA QUE `union` NECESITA · Y EL PRIMER ACTO QUE ACUÑA CON RAÍZ DE ACTO, CON SUS CONSUMIDORES YA ENSANCHADOS

**CABECERA** · redactado contra `d5825063` (re-deriva al abrir; si `main` se movió **no es PARO**: refresca, fusiona hacia la rama, re-deriva y reporta) · **ENTORNO: NUBE — Claude en la nube**, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, **con credenciales de Git y publicación de PR funcionando**; cero microdato, `data/raw` no hace falta · una sola sesión, rama propia (D-17) · **MODO: ABIERTO** (D-18) · **MODELO SUGERIDO: Opus** (se puede subir, nunca bajar) · **COMPUERTA: ninguna** — no abre dato, no congela spec, no adopta, no borra (D-20) · **CONTADOR: `cuenta_gen2 = NO`** — este acto no mide ninguna celda del programa · vehículo: `/acto`.

**EL PR NO SE FUSIONA EN ESTE ACTO.** Se publica y se deja **propuesto; mesa central lo revisa y fusiona.** El acto termina con `## CONSUMIDO` citando el número real de PR verificado contra el HEAD remoto, no con el merge.

**Ramas vivas al redactar: siete** (`acto/gen2-din-credito-comparabilidad-texto-1`, `acto/gen2-limpieza-ramas-locales-4-cierre-fp402`, `acto/gen2-limpieza-ramas-locales-5`, `claude/ecstatic-edison-y1t005`, `claude/new-session-lvyz4s`, `claude/trusting-allen-0y61rq`, `claude/trusting-allen-0y61rq-bis`). Re-deriva el conteo al abrir y decláralo (A.13). **La concurrencia es alta y es normal: este acto no necesita ventana** — no migra nada.

**Máximos del espacio viejo, derivados hoy y sólo para no pisar citas, nunca para acuñar:** `ADR-571` · `NC-0432` · `FP-403`. **El `ADR` de este acto sigue siendo numérico** (`ADR-572` candidato, deriva al cierre; renumera quien fusiona segundo): la firma 1 pone `NC` y `FP` primero, `ADR` después con careo propio.

---

## RAÍZ CONGELADA — pegar este encargo es el sello de esta congelación

```
<PREFIJO>-<AAMMDD>-<RÓTULO>-<hhhh>-<NN>
```

- `<PREFIJO>` · `NC` o `FP`, según el espacio.
- `<AAMMDD>` · fecha del 0-bis, seis dígitos. Ordena cronológicamente por prefijo.
- `<RÓTULO>` · el rótulo del acto **completo, con su prefijo de generación**. `GEN2-` **se conserva**: separa 355 rótulos de generación 2 de los 933 anteriores del canon, y E.1 no admite que la generación se dé por supuesta.
- `<hhhh>` · los **cuatro primeros hex del commit de 0-bis** de esta sesión. Es lo que hace único el id bajo despacho duplicado: dos sesiones del mismo encargo comparten fecha y rótulo, nunca el commit.
- `<NN>` · secuencia **local del acto**, dos dígitos desde `01`, derivada de los ids que este acto ya acuñó — **nunca del máximo global, nunca reiniciada al fusionar `main`**.

Ejemplo de este acto: `NC-260921-GEN2-TUBERIA-SUCESOR-1-7c2d-01` · `FP-260921-GEN2-TUBERIA-SUCESOR-1-7c2d-02`.

**Orden obligatorio:** el commit de 0-bis existe **antes** de que se escriba el primer `NC` o `FP`. No se acuña contra un hash futuro ni se rellena después.

**Prohibido en este acto:** derivar cualquier `NC` o `FP` de `max+1`. Ése es el defecto que el acto cierra.

---

## 1 · OBJETIVO

Que al terminar: (a) `T15` asevere tres cosas y acepte huecos, probado por mutación; (b) exista una guarda que falle cuando un archivo con `merge=union` no termina en salto de línea; (c) los consumidores que parsean `FP-` acepten las dos épocas de id; (d) el careo `GEN2-TUBERIA-CAREO-1` esté archivado en el repo con sus reservas, **acuñadas con la raíz nueva**.

**Criterio de «hecho»:** `python3 tests/check.py --baseline` en **LÍNEA BASE VERDE**, PR publicado y propuesto a mesa, `## CONSUMIDO` con el PR real verificado contra el HEAD remoto, y **cero ids de este acto derivados de `max+1`**.

## 2 · FIRMAS DE MESA, verbatim

> **D-1** — «El veredicto de registro del careo es el del expediente: B′.»

> **D-2** — «Las acuñaciones nuevas de NC y FP adoptan un esquema de raíz de acto, prospectivo. El espacio NC-####/FP-### se CIERRA, no se migra: ningún id viejo cambia de dueño y todas sus citas siguen resolviendo.»

> **D-3** — «T15 asevera TRES cosas: sin duplicados · el conteo citado igual al número de únicos · toda cita resoluble. Acepta huecos. Sustituye a la firma 2, cuyo texto afirmaba que dos aserciones bastaban; dirección lo escribió sin ejecutarlo y tu prueba de mutación lo refuta. El ADR del sucesor no afirma que la enmienda proteja contra la renumeración.»

> **D-4** — «El parche del careo lo aplica un acto sucesor, DESPUÉS de congelar la raíz, y es el primero que acuña con el esquema nuevo. Corre en nube o caja, por /acto, con credenciales.»

> **D-7** — «No se mide bloque con devolución.»

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo

- `LEÍDO` · `tests/check.py:820` (`def t15_adr_count`) y `:833-835`: el bloque que hoy falla por huecos es `huecos = sorted(set(range(1, max(nums)+1)) - set(nums))`. **El resto de la función se conserva**: duplicados, y el cotejo del conteo citado contra `len(set(nums))` con su exención `MARCA_HISTORICA`.
- `EJECUTADO` (dirección, prototipo contra el árbol real, cinco mutaciones): la enmienda de **tres** aserciones sale verde hoy; verde con un id acuñado con salto y el conteo reconciliado; **falla** con `ADR` duplicado; **falla** con el conteo mal citado (defecto del 29/jul, 32 contra 37); **falla** con cita a un `ADR` inexistente. Y medido: con **dos** aserciones —sin el cotejo de conteo— el defecto del 29/jul **sale verde**. Por eso la firma dice tres.
- `EJECUTADO` (dirección): la enmienda **no protege contra la renumeración**. Una renumeración internamente consistente deja el registro sin duplicados, sin huecos y sin citas colgantes mientras la prosa sellada re-apunta en silencio a otro `ADR`; `T15` verde antes y después. **El ADR de este acto no afirma lo contrario.**
- `EJECUTADO` (dirección, reproducción propia del 21/sep): un archivo con `merge=union` que **no** termina en salto de línea, fusionado desde dos ramas que apendican, no produce conflicto y **no duplica una fila limpia**: pega la última fila compartida a la primera fila de cada rama y deja **dos filas deformadas**, mientras la fila compartida desaparece como fila propia. Receta mínima para que el ejecutor escriba su propio caso: archivo base de tres líneas **sin** `\n` final · `merge=union` en `.gitattributes` · ramas X e Y, cada una apendica una línea · `main` fusiona X y luego Y · resultado medido `- ULTIMA COMPARTIDA- entrada de X` y `- ULTIMA COMPARTIDA- entrada de Y`, cero conflictos. Con el archivo bien terminado, la misma fusión sale limpia.
- `LEÍDO` · `.gitattributes`: hoy `merge=union` está en **dos** archivos, `forense/hallazgos.md` y `forense/bitacora.md`; `hitoD-preregistro-v2_0.md` está excluido **a propósito** y esa exclusión **no se toca**. `EJECUTADO`: los dos terminan hoy en salto de línea, así que la guarda nace verde — es preventiva, y el defecto que atrapa es el reproducido arriba más la nota del 5/ago que ya lo documentaba.
- `EJECUTADO` (dirección, censo de quién parsea ids `NC-`/`FP-` en `tools/`, `tests/`, `.claude/`): **los contadores son inmunes** — `no_corrido_abiertas` cuenta por la columna `estado` (`tools/corrida0.py:4334`) y `tests/check.py:7051` usa `startswith("NC-")`. **Se rompen en silencio**: `tools/nc_por_clase.py:103` (`re.fullmatch(r"FP-\d+", fid)`) y `:143` (`re.findall(r"FP-\d+", texto)`), y `tools/digesto_tramite.py:2324` (`RE_FP_ID = re.compile(r"\bFP-\d+\b")`). **Quedan obsoletas pero ruidosas**: las recetas de máximo en `tools/tablero_programa.py:517` y `.claude/commands/revisa.md:432,435`.
- `EJECUTADO` (dirección): **el parche del careo no aplica** sobre `main` de hoy — fallan `forense/firmas-pendientes.tsv`, `forense/hallazgos.md` y `forense/no-corrido.tsv`. **No se usa el parche.** El contenido viaja en los cinco archivos del expediente.
- `EJECUTADO` (dirección): los ids del parche ya están tomados: `FP-402` lo tiene otro acto y el máximo `NC` va en `NC-0432`.
- `LEÍDO` (evidencia cruda del careo): su corrida en rojo son **4 FAIL**, ninguno de sustancia — `T02` por basename compartido entre su encargo y su nota, `T25` por un rótulo pelado `E1` sin prefijo de espacio, y `T16` ×2 como consecuencia aritmética de esos dos. Este acto los previene, no los hereda.
- `EJECUTADO` (dirección): las sesiones **no escriben en `main`** — 351 de 351 commits del primer padre en 14 días son «Merge pull request», cero push directo. Por eso el esquema de bloque reservado quedó descartado: exigiría un merge de mesa **para arrancar** cada acto.

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO

- `EJECUTADO`, A.8(2): **no existe guarda de salto de línea final**. Universo declarado: **303 archivos** `tests/*.py` y `tools/*.py`, patrones `endswith('\n')`, `newline`, `final_newline`, `salto de l`; los 8 aciertos son parseo de CSV o *trailers* de git. Vocabulario A.4: **NO-ENCONTRADO**.
- `EJECUTADO`, A.8(3), cobertura retroactiva: `merge=union` entró el 5/ago/2026 y la nota que documenta la trampa es de ese día; ningún test posterior la cubrió. El hueco lleva siete semanas abierto.
- **La adjudicación del esquema ya está firmada.** El expediente del careo deja su `FP` en PENDIENTE pidiendo a mesa decidir; **mesa ya decidió** con D-1 y D-2. La fila que este acto asiente **nace FIRMADA** con ese verbatim. **No se vuelve a preguntar a mesa lo que mesa ya firmó.**
- `EJECUTADO`: `tools/nc_por_clase.py` nació **el 21/sep** por `GEN2-SENAL-1`, que ya fusionó y no tiene rama viva; 249 líneas, un consumidor. Entra al perímetro de este acto. `tools/digesto_tramite.py` nació el 31/ago, 2 854 líneas, 32 menciones en gobernanza, y lo consumen `.claude/commands/revisa.md` y `tramite.md`, `cierre_acto.py`, `estado_comun.py`, `check.py` y tres tests: **queda fuera del perímetro**, es de dirección por superficie de consumo.

## 5 · PIEZAS — resultado esperado, no receta

**P0 · 0-bis (A.3) y chequeo de duplicado por CONTENIDO.** Este encargo verbatim a `forense/encargos/`, en el commit que además fija el `<hhhh>` de la raíz. El 0.c estándar busca el rótulo en nombres de rama, worktrees y PR; **el 40 % de las ramas llevan nombre autogenerado sin rótulo**, así que ese `grep` es ciego por construcción: mira también si alguna rama viva **archiva ya este encargo**. Declara cuántas ramas examinaste (A.13). Si encuentras un duplicado, PARA con cero commits y repórtalo.

**P1 · `T15` con tres aserciones.** Se retira el bloque de huecos; se conservan duplicados y el cotejo de conteo con su exención `MARCA_HISTORICA`; se añade la comprobación de cita a `ADR` inexistente. Entregable: la función enmendada **y** un test que la ejerza **por mutación** —una guarda que no se puede disparar no es guarda—, con al menos los cinco casos de §3: las que deben fallar fallan y el original pasa. La cabecera declara qué defecto atrapa cada aserción y su falsador a tres meses (§9). **El ADR no afirma que la enmienda proteja contra la renumeración.**

**P2 · Guarda de salto de línea final.** Test que falle si cualquier archivo declarado `merge=union` en `.gitattributes` no termina en `\n`. **El universo se deriva de `.gitattributes`**, no se teclea: un tercer archivo que entre a `union` mañana queda cubierto solo. Verificada por mutación contra el caso de §3. Si algún archivo ya está mal terminado, arréglalo y decláralo (defecto adyacente de menos de diez líneas, D-21).

**P3 · Los consumidores, ensanchados.** `tools/nc_por_clase.py:103` y `:143` aceptan las **dos épocas** de id `FP`. El patrón lo elige el ejecutor; lo que no es negociable es el test: **pina un id de cada época en el mismo caso** —un `FP-###` viejo y un `FP-<AAMMDD>-GEN2-…-<hhhh>-<NN>` nuevo—, porque un patrón ensanchado probado sólo contra ids viejos no prueba nada. Añade la misma cobertura a la forma del id: un test de **gramática** que acepte las dos épocas y rechace una tercera inventada. **`tools/digesto_tramite.py:2324` NO se toca**: se redacta el diff de una línea y se asienta como `NC` `FUERA-DE-PERÍMETRO` dirigida a dirección, con el diff dentro de la fila para que no haya que reconstruirlo.

**P4 · El careo, archivado y re-acuñado.** El contenido viaja en cinco archivos del expediente, con sha256 verificado al abrir: `01-VEREDICTO.md` `6bdb7758…` · `02-ENCARGO-verbatim.md` `817f7cd2…` · `03-hallazgos-de-este-acto.md` `b882985e…` · `04-asientos-NC.tsv` `69ed1ed6…` · `04-asiento-FP-402.tsv` `ed2676e6…`. **El parche no se usa** (no aplica, verificado). Entran: el encargo del careo verbatim, su veredicto como nota, sus tres líneas de `hallazgos.md`, sus cuatro reservas y su fila de firma. Con estas correcciones obligatorias:

- **Ids re-acuñados con la raíz nueva.** Los del parche están tomados.
- **La fila `FP` nace FIRMADA** con el verbatim de D-1/D-2, no PENDIENTE.
- **La reserva de la guarda de salto de línea nace CERRADA**, citando el PR de este acto: la cierra P2.
- Las otras tres reservas nacen abiertas: evaluar el tercer esquema `C`; el censo de consumidores de **orden** por id (el careo censó formato, no orden); y la diferencia de 2 en el conteo de filas `FP`, que es **error de dirección** y se declara como tal.
- **La nota lleva basename distinto del encargo** (`T02`), y todo rótulo nuevo se registra con su prefijo de espacio (`T25`). Los dos son los FAIL que el careo topó.

**P5 · Cierre.** Cascada de `/acto` completa, `check.py --baseline` VERDE o PARO, `## NO-CORRIDO / RESERVAS` («Ninguno.» es obligatorio) y `## CONSUMIDO` con el PR real verificado contra el HEAD remoto. **El PR queda propuesto; mesa central revisa y fusiona.**

## 6 · LATITUD

El cómo es tuyo: cómo escribes los tests, qué patrón eliges, cómo integras el contenido del careo, qué vehículo usas para asentar la decisión ya firmada. Un obstáculo reversible y barato se resuelve y se declara (D-19). Si `main` se mueve durante el acto —con siete ramas vivas, se moverá—, fusiona hacia la rama y re-deriva; no es PARO. Si un `ADR`/`NC`/`FP` **viejo** colisiona al fusionar, renumera quien fusiona segundo, como siempre: este acto cambia la regla hacia adelante, no hacia atrás.

## 7 · PAROS — lista cerrada

Entorno sin credenciales de publicación · encontrar que otra rama viva ya archiva este encargo · perder una fila ajena al integrar el contenido del careo · adoptar o mover un contador vedado · borrar, forzar o reescribir algo sellado · objetivo inalcanzable. **Fuera de esta lista no se para**: se resuelve, o se pregunta a mesa con opciones y recomendación y se sigue con lo demás.

## 8 · PERÍMETRO Y CONCURRENCIA

Escribes en: `tests/check.py` (sólo `T15` y lo que la guarda nueva necesite allí) · el archivo del test de la guarda y el de gramática, si van aparte · `tools/nc_por_clase.py` · `forense/encargos/` (este encargo y el del careo) · `forense/notas/` · `forense/hallazgos.md` · `forense/no-corrido.tsv` · `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` y la cascada mecánica que `cierre_acto.py --aplica` reconcilia · `canon/registro-rotulos.tsv`. Más el perímetro de cierre permanente (D-21). **Si te encuentras escribiendo fuera de esta lista, PARA.**

**No tocas:** `milpa/` · ningún `CALC` · `tools/corrida0.py` · `tools/digesto_tramite.py` · `data/corrida0/demanda-resultados.tsv` ni `demanda-corridas.tsv` · el asignador `tools/cierre_acto.py:132-133`, que sigue siendo `max+1` para `ADR` **a propósito** · `.claude/commands/acto.md`. **No migras ningún id viejo**: el espacio `NC-####`/`FP-###` se cierra, no se reasigna (D-2), y ninguna cita existente se reescribe.

## 9 · LO QUE NO HACE · SUCESORES

No evalúa el tercer esquema `C` · no censa consumidores de orden · no arregla el chequeo 0.c de `acto.md` ni `digesto_tramite.py` (los dos quedan en `NC` para dirección) · no toca `RES`/`CORR` · no fracciona ningún archivo de gobierno · no escribe la taxonomía de PR · no fusiona su propio PR.

Sucesores, en el orden que mesa fijó: (3) `RES`/`CORR` con llave lógica sin ruta ni versión, contra el informe de `GEN2-RELEVO-RECONCILIA-1`; (4) un archivo por entrada; (5) taxonomía de PR y regla de enrutamiento. Y, fuera de esa fila, lo que este acto deja asentado para dirección: el diff de `digesto_tramite.py` y el chequeo 0.c por contenido.

## 10 · FALSADOR (§9)

Si en tres meses ni la tercera aserción de `T15`, ni la guarda de salto de línea, ni el test de gramática de id han fallado una sola vez en CI, se anota y se revisa si valían el aparato. La guarda de `union` deja de tener sentido el día que ningún archivo lleve `merge=union`: su falsador se revisa entonces, no a los tres meses.

---

## NO-CORRIDO / RESERVAS

**`P4 · El careo, archivado y re-acuñado`** — *verbatim del encargo: «El contenido viaja en
cinco archivos del expediente, con sha256 verificado al abrir: `01-VEREDICTO.md` `6bdb7758…` ·
`02-ENCARGO-verbatim.md` `817f7cd2…` · `03-hallazgos-de-este-acto.md` `b882985e…` ·
`04-asientos-NC.tsv` `69ed1ed6…` · `04-asiento-FP-402.tsv` `ed2676e6…`»*
· **por qué:** `PARO-PREMISA` — la premisa `EJECUTADO` no se sostiene: **ninguno de los cinco
archivos llegó**. El directorio de adjuntos de esta sesión contiene **1 archivo**, el encargo
mismo; `GEN2-TUBERIA-CAREO-1` no aparece en **ninguna de las 7 refs vivas** del remoto
(`git grep -l "TUBERIA-CAREO" origin/main` → 0 aciertos; los 7 aciertos de `careo` en el árbol
son de `CELDA-D-CAREO-1`, `ADV-DUELO`, `benchmarks-4RT` y `PILOTO-3`, otro objeto). A.4:
**NO-ACCESIBLE** (los adjuntos) · **NO-ENCONTRADO** (el acto en el repo). §2: es «no pude
alcanzar la fuente», **no** «la fuente no tiene el dato». La premisa toca **logística**, no
estimando ni firma de mesa, y los objetivos (a), (b) y (c) seguían alcanzables → por §4/D-19
**no es PARO del acto**: se replanteó, se siguió con P1/P2/P3/P5 y se declara aquí.
· **impacto:** objetivo (d) de §1 no entregado. Quedan sin asentar el encargo del careo
verbatim, su veredicto como nota, sus tres líneas de `hallazgos.md` y **tres** de sus cuatro
reservas (el tercer esquema `C`; el censo de consumidores de **orden** por id; la diferencia de
2 en el conteo de filas `FP`, que el encargo declara error de dirección). **La cuarta reserva no
queda huérfana:** la guarda de salto de línea la cierra `P2` de este acto, por producto. **La
firma tampoco queda huérfana:** `D-1`/`D-2`/`D-3`/`D-4`/`D-7` viajan verbatim en §2 del encargo
y se asientan **FIRMADAS** en `FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01`. Ningún contador del
programa depende de esto (`cuenta_gen2 = NO`).
· **sucesor:** `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-03` — acto de dirección, re-lanzable con
los cinco archivos adjuntos; **cuesta un encargo, no rehacer el careo**.

**`P3 · tools/digesto_tramite.py:2324 NO se toca: se redacta el diff de una línea y se asienta
como NC FUERA-DE-PERÍMETRO dirigida a dirección, con el diff dentro de la fila`**
· **por qué:** `FUERA-DE-PERÍMETRO` — **es de dirección**, y el propio encargo lo excluye por
nombre y por superficie de consumo (2 854 líneas, 32 menciones en gobernanza, consumido por
`.claude/commands/revisa.md` y `tramite.md`, `cierre_acto.py`, `estado_comun.py`, `check.py` y
tres tests). **Ejecutado tal como se pidió**: el diff de una línea está **dentro** de la fila.
· **impacto:** el digesto de trámite deja de ver en silencio cualquier `FP` de la época nueva.
Hoy: 1 fila. Crece con cada acto que acuñe.
· **sucesor:** `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01`.

**`§9 · no arregla el chequeo 0.c de acto.md`**
· **por qué:** `FUERA-DE-PERÍMETRO` — **es de dirección**: `.claude/commands/acto.md` está en la
lista «No tocas» de §8. El encargo lo manda dejar en `NC`, y eso se hizo, **con la medición que
lo justifica**: 4 de las 6 ramas vivas llevan nombre autogenerado sin rótulo, así que el `grep`
de rótulo es ciego en el 67 % del universo.
· **impacto:** todo acto futuro corre un 0.c que no detecta un despacho duplicado en una rama de
nombre autogenerado — el caso mayoritario hoy. Dos sesiones sobre el mismo rótulo producen dos
`ADR` con el mismo número.
· **sucesor:** `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-02`.

**`§3 · recetas de máximo «obsoletas pero ruidosas» (tools/tablero_programa.py:517 y
.claude/commands/revisa.md:432,435)`**
· **por qué:** `FUERA-DE-PERÍMETRO` — **es de dirección**, misma bandeja: §8 enumera
`tools/nc_por_clase.py` como el único consumidor dentro del perímetro.
· **impacto:** ruidoso, no silencioso — el tablero y el revisor reportan un máximo que, cerrado
el espacio viejo (D-2), ya describe medio universo. Nadie pierde una fila.
· **sucesor:** `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-04`.

**`§9 · el PR no se fusiona en este acto`**
· **por qué:** `DECISIÓN-DE-MESA-PENDIENTE` — no es deuda: es la instrucción explícita del
encargo («**EL PR NO SE FUSIONA EN ESTE ACTO.** Se publica y se deja propuesto; mesa central lo
revisa y fusiona»). Se declara para que la ausencia de merge no se lea como acto sin cerrar.
· **impacto:** ninguno sobre contadores; la **política de cero ramas** (A.14) se satisface con
el merge o el borrado que mesa decida.
· **sucesor:** mesa central.

**Todo lo demás del encargo se corrió:** P0 (0-bis y chequeo de duplicado por contenido), P1
(`T15` con tres aserciones, probado por mutación), P2 (guarda de salto de línea con universo
derivado y el defecto reproducido con git), P3 (`tools/nc_por_clase.py` ensanchado, con un id de
cada época pinado en el mismo caso y el test de gramática) y P5 (cascada completa, `check.py
--baseline` VERDE).

---

## CONSUMIDO

**PR #939** — <https://github.com/Josanoforo/Modelado-Mexicano/pull/939>, rama
`claude/new-session-ccjtu7`, **propuesto a mesa, no fusionado desde el acto** (instrucción
verbatim del encargo: «EL PR NO SE FUSIONA EN ESTE ACTO»). Número real verificado contra el
HEAD remoto, no inferido.

**Orden de fusión fijado por mesa durante el acto:** este PR va **después de `#937`**. `#937`
reclama hoy `ADR-573`, así que **es previsible una renumeración más al fusionar**; le toca a
quien fusione segundo, como siempre. Este acto ya renumeró **cuatro veces** en una sola sesión
(572 → 573 → 574 → 575 → 576, por `#932`, `#935` y otros dos), y las dos primeras colisiones las
atrapó **la aserción (1) de su propia enmienda de `T15`** — esa aserción cobró su falsador el día
en que se selló, sin esperar tres meses. Los ids propios de raíz de acto (`…-6e60-NN`) **no se
renumeran** con el `ADR`: son inmunes a esta clase de colisión por construcción, y ésa es
exactamente la propiedad por la que D-2 existe.

`ADR-576` · `cuenta_gen2 = NO`, cero contadores del programa movidos ·
`NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01`–`-04` ABIERTAS con sucesor nombrado ·
`FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01` **FIRMADA** ·
nota: `forense/notas/2026-09-21-GEN2-TUBERIA-SUCESOR-1-cierre.md` ·
suite `--baseline` en **LÍNEA BASE VERDE**.
