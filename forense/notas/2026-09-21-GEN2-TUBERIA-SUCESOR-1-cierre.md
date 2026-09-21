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

Consecuencia: el `ADR` de este acto es **`ADR-574`**, no el `ADR-572` que el encargo proponía
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
en silencio a otro `ADR`; `T15` sale verde antes y después. `ADR-574` **no afirma lo contrario**.
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

## 5 · P4 · el careo NO se archivó — el expediente no llegó

**Éste es el hallazgo principal de este acto, y es un defecto de encargo, no de ejecución.**

El encargo declara, con rótulo `EJECUTADO`, que «el contenido viaja en cinco archivos del
expediente, con sha256 verificado al abrir»: `01-VEREDICTO.md` `6bdb7758…`,
`02-ENCARGO-verbatim.md` `817f7cd2…`, `03-hallazgos-de-este-acto.md` `b882985e…`,
`04-asientos-NC.tsv` `69ed1ed6…`, `04-asiento-FP-402.tsv` `ed2676e6…`.

**Ninguno de los cinco llegó.** Universo examinado y conteo (A.4/A.13):

- el directorio de adjuntos de esta sesión contiene **1 archivo**, el encargo mismo — cero de los cinco;
- `GEN2-TUBERIA-CAREO-1` no aparece en **ninguna** de las 7 refs del remoto
  (`git grep -l "TUBERIA-CAREO" origin/main` → 0 aciertos; los 7 aciertos de `careo` en el árbol
  son de `CELDA-D-CAREO-1`, `ADV-DUELO`, `benchmarks-4RT` y `PILOTO-3`, otro objeto).

Vocabulario A.4: **NO-ACCESIBLE** (los cinco adjuntos), **NO-ENCONTRADO** (el acto `GEN2-TUBERIA-CAREO-1`
en el repo, dónde: las 7 refs vivas; con qué términos: `TUBERIA-CAREO` y `careo` por nombre de archivo y por contenido).
Y la distinción que §2 prohíbe colapsar: esto es **«no pude alcanzar la fuente»**, no «la fuente
no tiene el dato». El expediente puede existir perfectamente del lado de dirección.

**Por qué esto NO es PARO y el acto siguió.** La lista cerrada de §7 no lo contiene, y §4/D-19
mandan: premisa caída que toca **logística**, con el objetivo **parcialmente** alcanzable →
se replantea, se sigue con lo demás y se declara. De los cuatro objetivos de §1, (a), (b) y (c)
se entregan completos; sólo (d) queda sin entregar. Y una frontera que no se cruzó: la fila `FP`
del careo «nace FIRMADA con el verbatim de D-1/D-2», pero **transcribir tres hallazgos, cuatro
reservas y un veredicto que no he leído sería teclearlos de memoria** — §2, regla de oro, lo
prohíbe, y el PARO de §7 «perder una fila ajena al integrar el contenido del careo» es
precisamente el riesgo que se evita no inventándolo.

**Lo que sí se pudo asentar sin el expediente, y se asentó:** la firma de mesa misma. `D-1`,
`D-2` y `D-3` viajan **verbatim dentro del encargo** (§2), así que no dependen del expediente.
Su fila `FP-260921-GEN2-TUBERIA-SUCESOR-1-6e60-01` **nace FIRMADA**, no PENDIENTE — mesa ya
decidió y no se le vuelve a preguntar lo que ya firmó. Y la reserva de la guarda de salto de
línea, que P2 cierra, se asienta **CERRADA** citando este PR: se cierra por su **producto**
(`T46` existe, corre en CI y está ejercida por mutación), que es la única forma de cerrar una
reserva, no por el hecho de que un PR fusione.

**Lo que queda para el sucesor** está en `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-03`: archivar
el careo (encargo verbatim + veredicto como nota con basename distinto + sus tres líneas de
`hallazgos.md`) y las tres reservas restantes que el encargo enumera — el tercer esquema `C`,
el censo de consumidores de **orden** por id (el careo censó formato, no orden) y la diferencia
de 2 en el conteo de filas `FP`, que el propio encargo declara **error de dirección**. Re-lanzar
ese sucesor **cuesta un encargo con los cinco archivos adjuntos**; no cuesta rehacer el careo.

**Los dos FAIL que el careo topó, prevenidos y no heredados,** como pedía el encargo:

- **`T02`** (basename compartido entre encargo y nota): esta nota se llama
  `2026-09-21-GEN2-TUBERIA-SUCESOR-1-cierre.md`, basename distinto del encargo. Verificado: la
  suite no reporta T02 nuevo.
- **`T25`** (rótulo pelado sin prefijo de espacio): se disparó — y no por un rótulo de este
  acto, sino porque **el encargo archivado narra el defecto ajeno**: su §3 cita, dentro de una
  línea de prosa que lo explica, el token pelado del espacio `E` (un dígito, sin prefijo
  `MAESTRA<nn>-`) por el que el careo salió en rojo. **Ese token no se reproduce en esta nota, y
  la omisión es deliberada**: escribirlo aquí volvería a disparar `T25` sobre un archivo que sí
  es editable, y exentar mi propia nota sería complacencia, no exención. Un encargo verbatim,
  en cambio, **no se edita para complacer un test** (A.3), así que la vía correcta es la
  exención documentada: el archivo entra a
  `_T25_ARCHIVOS_CONOCIDOS` con el comentario que explica de dónde sale el token, igual que los
  otros diez casos de esa lista, y el rótulo propio del acto se censa en `canon/registro-rotulos.tsv`.
  Registrado aquí porque es simpático y es real: **la cita de un defecto reproduce el defecto**.
- **`T16` ×2** era consecuencia aritmética de los dos anteriores; sin ellos, no aparece.

## 6 · Contadores

`cuenta_gen2 = NO` — este acto **no mide ninguna celda del programa**, no abre dato, no congela
spec, no adopta, no borra, y no toca ningún `CALC`. Contadores movidos: **cero**, por diseño y
declarado en la primera línea (módulo de auditoría §5, v2.4). Lo que sí mueve: tres guardas
donde había dos (una de ellas con un hueco de **siete semanas**), un consumidor que dejaba de
ver ids nuevos en silencio, y el primer acto que acuña con raíz de acto.

## 7 · Suite

`python3 tests/check.py --baseline --parallel` → **LÍNEA BASE VERDE**, cero FAIL nuevos frente
a `tests/baseline.json`. `python3 tests/test_tuberia_ids_union.py` → **TODO VERDE**, 18 casos.
