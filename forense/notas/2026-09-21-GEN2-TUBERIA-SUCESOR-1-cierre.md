# ACTO GEN2-TUBERIA-SUCESOR-1 · nota de cierre

**21/sep/2026 · NUBE (`cloud_default`) · Opus · MODO ABIERTO · COMPUERTA: ninguna · `cuenta_gen2 = NO`.**
Encargo archivado verbatim (A.3): `forense/encargos/2026-09-21-GEN2-TUBERIA-SUCESOR-1.md`,
sha256 `6e46662b053101076ff203fd58c60a5471a60739d07bcf19a9ee9c2272bf34b6`.
Base real: `origin/main` `8d78cf5` (el encargo se redactó contra `d5825063`; main se movió, no es PARO — refrescado y re-derivado).

## 0 · ARRANQUE, crudo

```
ENTORNO-DERIVADO = NUBE
senal-corpus: montado=NO archivos_examinados=0
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403, x_deny_reason=ausente, via_proxy=SI)
head-vs-origin/main: detras=0 adelante=0 (sin fetch)
worktrees: 1
es-worktree: NO
ramas-locales-con-commits-propios: 1/2
data-raw-en-este-worktree: NO
```

Entorno declarado por el encargo (NUBE) = ENTORNO-DERIVADO (NUBE). Cero microdato, cero red;
`data/raw` no hace falta y no se enlaza. Credenciales de publicación: verificadas por uso
(`git push` del 0-bis y apertura del PR), no supuestas.

**0.a base al día:** `git rev-list --count HEAD..origin/main` = `0` tras `git fetch --prune`.
El hook de arranque había impreso `detras=535 adelante=443` **sin fetch** — cifra de un
remoto rancio, no del terreno; ésta es la razón por la que 0.a se corre con fetch.

**0.b árbol limpio:** `git status --porcelain` vacío antes del 0-bis.

**0.c duplicado por CONTENIDO, no por rótulo (P0).** El `grep` de rótulo es ciego por
construcción: **4 de las 6 ramas vivas** al abrir llevan nombre autogenerado sin rótulo.
Universo examinado (A.13): **6 ramas remotas vivas + `main` = 7 refs**, cada una recorrida
con `git ls-tree -r --name-only origin/<rama> -- forense/encargos/` y con
`git diff --name-only origin/main...origin/<rama> -- forense/encargos/`. Los únicos encargos
que alguna rama añade sobre `main` son `2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-5.md`,
`2026-09-21-motor-linaje-1-nc0401.md` y `2026-09-20-GEN2-NUBE-PILOTO-1.md` (×3).
Más los **6 PR abiertos** (#930, #931, #934, #935, #936, #937), ninguno con este rótulo.
Vocabulario A.4: **NO-ENCONTRADO** (dónde: las 7 refs y los 6 PR abiertos; con qué términos:
el objeto «un archivo de `forense/encargos/` que archive este encargo», no la cadena del rótulo).
**Sin duplicado.**

**0.d higiene:** `tools/limpia_arbol.py --reporta` — 1 worktree, base al día,
`ramas remotas sin PR abierto` **NO-VERIFICABLE-SIN-GH** en este entorno (`gh` no existe);
se suplió con el listado de PR por el tool de GitHub, arriba.

## 1 · RAÍZ CONGELADA, y el primer acto que acuña con ella

```
<PREFIJO>-<AAMMDD>-<RÓTULO>-<hhhh>-<NN>
```

`<hhhh>` = **`6e60`**, los cuatro primeros hex del commit de 0-bis de esta sesión
(`6e60c1c34519131b9d3de5108abc149721a339cd`). El orden obligatorio se respetó: el commit de
0-bis existe **antes** de que se escribiera el primer `NC` o `FP`, y ningún id de este acto
se derivó de `max+1`. `<NN>` es secuencia **local del acto**, desde `01`.

**Máximos del espacio viejo, RE-DERIVADOS hoy y sólo para no pisar citas** (los del encargo
habían caducado en las horas entre su redacción y su ejecución, con `PR #932` fusionado en medio):

| | el encargo declaraba | derivado hoy contra `8d78cf5` |
|---|---|---|
| `ADR` | 571 | **572** (`tools/cierre_acto.py` Fase A) |
| `NC` | 0432 | **0435** |
| `FP` | 403 | **404** |

Consecuencia: el `ADR` de este acto es **`ADR-576`**, no el `ADR-572` que el encargo proponía
como candidato — `ADR-572` ya lo tomó `GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1`. Es
exactamente la clase de premisa que §0 manda verificar antes de obedecer: logística, no
estimando, así que se replanteó y se siguió (v2.15).

## 2 · P1 · `T15` asevera tres cosas y acepta huecos (firma D-3)

`tests/check.py::t15_adr_count`. Se retiró el bloque de huecos
(`set(range(1, max(nums)+1)) - set(nums)`); se conservan **sin tocar** las dos que ya estaban
(duplicados, y el cotejo del conteo citado contra `len(set(nums))` con su exención
`MARCA_HISTORICA`); se añadió la tercera, **toda cita `ADR-N` de `canon/` resuelve**.

Qué atrapa cada una y su falsador a tres meses (§9) quedan escritos en la cabecera de la
función, no sólo aquí. Resumen:

| aserción | defecto real que atrapa | estado hoy |
|---|---|---|
| sin duplicados | dos actos en vuelo que toman el mismo `max+1` y fusionan uno tras otro | 0 duplicados en 572 entradas |
| conteo citado = únicos | `censo-integridad-v1_0.md` C1-02, 29/jul/2026: **32 citado contra 37 reales** | cabecera, L0 y tabla dicen 572 |
| toda cita resoluble | la cita colgante que antes sólo se veía de rebote, cuando el hueco que la dejaba huérfana aún era ilegal | **0 citas no resolubles** en `canon/*.md` |

**Por qué tres y no dos, medido y no argumentado.** `tests/test_tuberia_ids_union.py` caso **A5**:
sobre el mismo árbol que rompe A3 (37 entradas, la prosa citando 32), las aserciones (1) y (3)
—la variante de DOS— dan `dup=[] colgantes=[]`, es decir **VERDE**. El defecto del 29/jul pasa
limpio sin el cotejo de conteo. La firma D-3 dice tres porque dos no bastan, y esto lo
corrobora la prueba, no la prosa.

**Lo que esta enmienda NO hace, y queda declarado en el código para que nadie lo herede al
revés: NO protege contra la renumeración.** Una renumeración internamente consistente deja el
registro sin duplicados, sin huecos y sin citas colgantes mientras la prosa sellada re-apunta
en silencio a otro `ADR`; `T15` sale verde antes y después. `ADR-576` **no afirma lo contrario**.
Quien quiera esa garantía necesita anclar la cita al CONTENIDO del ADR, no a su número, y no
es este test.

**Huecos aceptados, a propósito.** El bloque exigía que el espacio de `ADR` fuera dos cosas a
la vez —contiguo y estable—, y con actos en paralelo un hueco es el resultado **normal** de
renumerar al fusionar segundo. Caso **A1**: registro `[1,2,4]` con el conteo reconciliado a 3
pasa sin FAIL.

## 3 · P2 · la guarda de salto de línea que `union` necesita

`tests/check.py::t46_union_newline` (**T46 · T-UNION-NEWLINE**), cableada en `main()` y en
`.github/workflows/verify.yml`.

**El universo se DERIVA de `.gitattributes`**, no se teclea: `union_paths()` parsea las líneas
`<patrón> … merge=union`, ignorando comentarios — que es justamente donde este repo explica
por qué `hitoD-preregistro-v2_0.md` **no** entra a union. Hoy da exactamente los dos declarados
(`forense/hallazgos.md`, `forense/bitacora.md`); un tercero que entre mañana queda cubierto
**sin tocar el test** (caso B2 lo prueba). A.13 cableada: si el comando examina cero archivos,
el veredicto se declara no-negativo y falla.

**Los dos archivos terminan hoy en salto de línea, así que la guarda nace VERDE: es preventiva.**
No hubo nada que arreglar (el defecto adyacente de D-21 no se activó).

**Reproducción propia del defecto, con git de verdad** (caso B3, repo temporal, no el clon):
base de tres líneas **sin** `\n` final · `merge=union` · ramas X e Y que apendican una línea
cada una · `main` fusiona X y luego Y. Resultado medido, idéntico al que dirección reportó:

```
conflicto=False
deformadas=['- ULTIMA COMPARTIDA- entrada de X', '- ULTIMA COMPARTIDA- entrada de Y']
compartida_sola=False
```

Cero conflictos, la fila compartida desaparece como fila propia, dos filas deformadas. Con el
archivo bien terminado (B3b), la misma fusión sale limpia:
`['- PRIMERA', '- SEGUNDA', '- ULTIMA COMPARTIDA', '- entrada de X', '- entrada de Y']`.
Premisa `EJECUTADO` de dirección: **verificada de forma independiente**, no heredada. Esto es
lo que impide que la guarda vigile un fantasma.

**Falsador:** la guarda de `union` deja de tener sentido el día que ningún archivo lleve
`merge=union` — su falsador se revisa **entonces**, no a los tres meses. Ese día `T46` emite
WARN (no FAIL) diciendo que se quedó sin universo, que es la señal de revisarla.

## 4 · P3 · los consumidores, ensanchados

`tools/nc_por_clase.py`: una sola gramática, `RE_FP = (?:RE_FP_NUEVA|RE_FP_VIEJA)`, consumida
por los dos sitios censados — `estado_fps()` (antes `re.fullmatch(r"FP-\d+", fid)`) y
`clasifica()` (antes `re.findall(r"FP-\d+", texto)`).

**Qué se rompía en silencio, y por qué importaba.** Con `FP-\d+` a secas, un id de la época
nueva es **invisible**: ni revienta ni avisa, devuelve menos. Una NC bloqueada por una `FP`
nueva se clasificaría `SIN-ASIGNAR` en vez de `ESPERA-FIRMA`, y mesa vería deuda sin dueño
donde hay una firma pendiente. Caso **C4b** pina exactamente eso.

**Dos decisiones del patrón, ninguna cosmética:**

1. **La época nueva va primero en la alternancia.** `FP-260921…` lo casaría la rama vieja como
   el prefijo `FP-2609` si se le diera la primera oportunidad, partiendo el id en dos y
   produciendo una cita fantasma. Caso **C3-bis**.
2. **El ancho `{1,3}` de la rama vieja no está tecleado: se derivó**
   (`cut -f1 forense/firmas-pendientes.tsv | grep -oE '^FP-[0-9]+' | awk -F- '{print length($2)}' | sort | uniq -c`
   → 99 de ancho 2 · 291 de ancho 3 · ninguno más ancho). Como el espacio está **cerrado**
   (D-2), ese ancho ya no puede crecer, y acotarlo es lo que permite **rechazar** una tercera
   época inventada en vez de tragársela como un id viejo largo.

**El test es lo no negociable, y cumple las dos exigencias del encargo:** `C4c` pina **un id de
cada época en el mismo caso** (`FP-402` y `FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01`, ambos
vistos a la vez), y `C1`/`C2`/`C3` son el test de **gramática**: acepta las dos épocas y
rechaza ocho formas de una tercera inventada (fecha truncada, sin `GEN2-`, hex en mayúscula,
secuencia de un dígito, hex de cinco, `FP-`, `FP-abc`). `C4d` es el control negativo: una `FP`
nueva ya FIRMADA deja de bloquear.

**`tools/digesto_tramite.py:2324` NO se tocó**, como manda el encargo: el diff de una línea va
**dentro** de la fila `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01`, para que nadie tenga que
reconstruirlo.

## 5 · P4 · el careo, archivado y re-acuñado — en dos tiempos

**Primer tiempo: el expediente no llegó, y se declaró así.** Al abrir el acto, los cinco
archivos que el encargo declara `EJECUTADO` con sha256 **no estaban**. Universo examinado y
conteo (A.4/A.13): el directorio de adjuntos contenía **1 archivo**, el encargo mismo;
`GEN2-TUBERIA-CAREO-1` no aparecía en **ninguna de las 7 refs vivas**
(`git grep -l "TUBERIA-CAREO" origin/main` → 0 aciertos; los 7 aciertos de `careo` en el árbol
eran de `CELDA-D-CAREO-1`, `ADV-DUELO`, `benchmarks-4RT` y `PILOTO-3`, otro objeto).

Se clasificó **NO-ACCESIBLE** (los adjuntos) y **NO-ENCONTRADO** (el acto en el repo),
**sin colapsarlo** con «la fuente no tiene el dato» (§2, los tres hallazgos que nunca se
colapsan). No era PARO: §7 es lista cerrada y la premisa caída toca **logística**, con (a), (b)
y (c) alcanzables → §4/D-19, se siguió con lo demás y se declaró.

**Segundo tiempo: mesa mandó el expediente y P4 se ejecutó en el mismo acto.** Llegaron dos zip.
**Los cinco sha256 coincidieron 5 de 5** contra los declarados por el encargo — verificados al
abrir, no supuestos:

```
6bdb7758405c0aacd897a7133670c5ae98b42bb496f4236e5de4bbfd94fed6cb  01-VEREDICTO.md
817f7cd21b82106baa83081c21a6a719d7d38afe7266b199408cce5c94b32d1e  02-ENCARGO-verbatim.md
b882985e12fe502717042801bbb31c40e11e6b093abb10fa237ec164dae7991f  03-hallazgos-de-este-acto.md
69ed1ed678a13dd6b555dddcbc92c4c7fb605353ce49661551d20b8bae41e686  04-asientos-NC.tsv
ed2676e659d46d65af2d780bc4de82ef89179c12d1508bf365493771c1f9b042  04-asiento-FP-402.tsv
```

**La clasificación de A.4 fue lo que permitió recuperar la pieza sin rehacer el careo.** Un
`NO-ENCONTRADO` mal escrito —uno que hubiera dicho «no existe»— habría justificado re-carearlo.
**Y el error propio, asentado en `hallazgos.md`: el ejecutor declaró la ausencia y NO la pidió.**
Declarar era correcto y no era PARO, pero pedir cuesta una línea y habría entregado P4 en el
primer turno. Regla que deja: **ante un adjunto ausente, se declara Y se pide en el mismo turno**;
A.3 («el texto va inline o no se lanza») dice qué debe hacer quien redacta, no exime a quien
ejecuta de preguntar. **El parche no se usó**, como manda el encargo.

**Qué entró, verbatim y byte a byte:**

| pieza | destino | sha256 verificado |
|---|---|---|
| encargo del careo | `forense/encargos/2026-09-20-GEN2-TUBERIA-CAREO-1.md` | `817f7cd2…` |
| veredicto como nota | `forense/notas/2026-09-20-GEN2-TUBERIA-CAREO-1-cierre.md` | `6bdb7758…` |
| sus tres líneas | `forense/hallazgos.md`, verbatim, con comentario HTML que rastrea los ids re-acuñados | `b882985e…` |
| sus cuatro reservas | `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-05`…`-08` | `69ed1ed6…` |
| su fila de firma | `FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-02` | `ed2676e6…` |

**Las cinco correcciones obligatorias del encargo, cumplidas:**

1. **Ids re-acuñados con la raíz nueva.** Los del expediente estaban tomados, y no por poco:
   `NC-0423`–`NC-0426` los tomó `GEN2-RELEVO-RECONCILIA-1` y `FP-402` otro acto. **Ésa es
   exactamente la colisión que D-2 cierra**, ocurrida sobre el careo que la diagnosticó.
2. **La fila `FP` nace FIRMADA**, con D-1/D-2 verbatim y con la razón decisiva del careo dentro
   de la fila, para que nadie tenga que reconstruirla. No PENDIENTE: mesa ya decidió.
3. **La reserva de la guarda de salto de línea nace CERRADA** (`-6e60-06`), cerrada **por
   producto** —`T46` existe, corre en CI y está ejercida por mutación— y no por merge. Su
   `SUSTITUIDO-POR` enumera qué absorbe y declara que **nada queda huérfano**.
4. **Las otras tres nacen abiertas**: el tercer esquema `C` (`-05`), el censo de consumidores de
   **orden** (`-07`, el careo censó formato, no orden) y la diferencia de 2 en el conteo de filas
   `FP` (`-08`), **declarada error de dirección**, que es lo que el encargo manda.
5. **`T02` y `T25` prevenidos.** La nota del careo lleva basename distinto de su encargo
   (`…-cierre.md`, el desvío que el propio careo ya había declarado por D-19); su rótulo va
   censado en `canon/registro-rotulos.tsv`. `T25` volvió a dispararse sobre el veredicto, que
   cita sus cuatro mutaciones de P4 y un residuo de sus escenarios de P1 con tokens pelados del
   espacio `M` y del espacio `E` — **nombres internos del documento, no rótulos de acto**; **no se
   reproducen aquí, por la misma razón de siempre: reproducirlos vuelve a disparar el test**; un documento sellado y archivado verbatim no se edita para complacer un
   test (A.3), así que entra a `_T25_ARCHIVOS_CONOCIDOS` con su comentario.

**Lo que el careo dictamina y este acto confirma de forma independiente.** Su `P4`/mutación 4
—la renumeración internamente consistente deja `T15` **VERDE antes y después**, y no es
instrumentable, sólo prevenible por construcción— se corroboró **en vivo**: esta sesión renumeró
**cuatro veces** (572→573→574→575→576) y ninguna de esas renumeraciones habría sido visible para
`T15` si hubiera sido internamente consistente. Por eso el `ADR` de este acto **no afirma** que
la enmienda proteja contra la renumeración. Y su `P1`/escenario 5 —la trampa del salto de línea
es **ortogonal al esquema de id**— se reprodujo aquí por separado, con git de verdad (§3, caso
B3), **antes** de leer el expediente: dos derivaciones independientes del mismo defecto.

**Segundo defecto propio de esta sesión, y se asienta porque casi cuesta la nota.** La
renumeración a `ADR-576` se aplicó sobre esta nota con
`io.open(p,"w").write(io.open(p).read().replace(...))`: en Python el `open(...,"w")` se evalúa
**antes** que el `read()`, así que truncó el archivo a 0 bytes y escribió la cadena vacía. Se
detectó al releerla y se recuperó íntegra de `git show e1bda94:<ruta>` (15 455 bytes). Queda como
recordatorio del mismo género que el `sed` global asentado en `forense/hallazgos.md`: **un one-liner que lee y escribe el
mismo archivo no es atómico — se lee a una variable primero, o se pierde el archivo en silencio.**

## 6 · Contadores

`cuenta_gen2 = NO` — este acto **no mide ninguna celda del programa**, no abre dato, no congela
spec, no adopta, no borra, y no toca ningún `CALC`. Contadores movidos: **cero**, por diseño y
declarado en la primera línea (módulo de auditoría §5, v2.4). Lo que sí mueve: tres guardas
donde había dos (una de ellas con un hueco de **siete semanas**), un consumidor que dejaba de
ver ids nuevos en silencio, y el primer acto que acuña con raíz de acto.

## 7 · Suite

`python3 tests/check.py --baseline --parallel` → **LÍNEA BASE VERDE**, cero FAIL nuevos frente
a `tests/baseline.json`. `python3 tests/test_tuberia_ids_union.py` → **TODO VERDE**, 18 casos.
