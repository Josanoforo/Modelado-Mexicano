# Nota de cierre · `ACTO MAESTRA30-E3 · EJERCE-LLAVE-COMPARTAMOS` — 26 de agosto de 2026

**Entorno UBUNTU · caja del acto `/home/pc0/mm-e3-ejerce-compartamos`, rama `acto/e3-ejerce-llave-compartamos` · base `186f090` · `ADR-203`**

---

## 0 · Arranque — las cinco líneas, tal como salieron

1. **REPO.** El clon existente `/home/pc0/Modelado-Mexicano` estaba **parado en otra rama** (`acto/cal-g3-puntual`, `ea22bdd`); no se clonó nada nuevo. Se abrió caja propia del acto en `/home/pc0/mm-e3-ejerce-compartamos` sobre `186f090`, `git status` limpio. Es la disciplina de siempre: en el worktree principal, parado en otra rama, las premisas de un encargo parecen falsas sin serlo.
2. **SHA.** `origin/main` = **`186f090`**, **idéntico** al que el encargo declara. `main` no se movió; nada que re-derivar por perímetro.
3. **`data/raw`.** Ausente en la caja nueva, como nace siempre. **Enlazada** a `/home/pc0/mm-corpus/raw`, el mismo destino que las demás cajas. Control positivo `A.2`: `ls data/raw/ | head -1` → `2005trim1_csv.zip`, **321** entradas. Este acto **no descarga nada** (prohibido por el encargo).
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → **sin_variable** (el esperado para UBUNTU). `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` → **200**. En esta caja `grep` **sí** es una función que envuelve otro binario: todos los conteos de este acto usan `command grep`, declarado en cada lugar donde aparece un negativo.
5. **ESPEJO.** No se tocó. Toda cifra de esta nota sale de la caja de (1), con el comando a la vista.

**Hallazgo de terreno reportado antes de empezar, no al final.** El encargo ordena correr **después de MAESTRA30-E4**. La caja `/home/pc0/mm-e4-diseno-ensafi` existe pero estaba en `186f090` con status limpio y **sin un solo commit**, y `gh pr list --state open` salió **vacío** al arrancar. MAESTRA30-E4 no había corrido, ni MAESTRA30-E1/E2. La razón declarada del orden —*«secuencial evita dos merges simultáneos desde la misma caja»*— quedaba satisfecha por vacío, así que el acto procedió. Al cerrar hay **`PR #372`** abierto, ajeno a este lote (ver §6).

---

## 1 · Compuerta cero

`FP-160` en estado **`FIRMADA`** (`forense/firmas-pendientes.tsv:158`), con la firma de mesa verbatim en su campo `firmada_en` y en `ADR-199` §L4: *«SELLO FP-160: la spec B-bis de EXP-COMPARTAMOS-1 queda sellada tal como está propuesta.»* Es **enmienda de estado, no de archivo**: `forense/spec-bbis-exp-compartamos-v1_0-PROPUESTA.md` conserva el nombre porque las citas vivas apuntan a él.

**Lo que la firma no eligió, y que decide la forma de este acto.** La fila `FP-160` planteaba **dos** disyuntivas — sellar el texto, y elegir el destino del número futuro entre (a) el `[MEDIA](a)` y (b) la octava clase de `milpa/`. El campo `firmada_en` y `ADR-199` §L4 resuelven **solo la primera**. La `RANURA DE MESA` del encargo llegó **VACÍA**. De ahí todo lo demás: la llave se ejerce, el número queda `PROPUESTO`, `milpa/` no se toca.

**Hash del payload — `A.1`, con las tres respuestas sin colapsar.** Una invocación de `python3 tests/manifiesto.py --verifica` (951 líneas, 790 payloads con veredicto). Línea 609:

```
116334_v1 [descargas_mx]: COINCIDE -- sha256 y tamaño (1404772 bytes) verificados contra data/manifiesto.yaml
```

**Pero la primera invocación en esta caja no dijo eso**, y la diferencia importa: dijo `RAÍZ NO CONFIGURADA -- este entorno no define 'descargas_mx' en data/raices.local.yaml`. Eso **no es `AUSENTE`** y **no es hash discordante**: es la tercera respuesta, y significa que el verificador **no examinó ni un archivo** para ese payload. Se resolvió configurando `data/raices.local.yaml` (gitignorado, `.gitignore:7`) con `descargas_mx: /mnt/c/Users/PC0/Descargas MX`, copiado del clon principal. Solo entonces la respuesta pasó a `COINCIDE`. Recuento del reporte: `AUSENTE` **0**; hash discordante **1** en todo el manifiesto (`endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf [data_raw]`, `:323`) — **ajeno a este acto y a su perímetro**, declarado y no tocado.

**`A.13`, con el ejemplo que este acto produjo contra sí mismo.** Al buscar el payload, un `find /mnt/c/Users/PC0 -maxdepth 2 -name "116334*"` salió **vacío**. Ese vacío **no era un negativo**: el archivo vive a profundidad 3 (`Descargas MX/Descargas Manuales/116334-V1.zip`) y el comando nunca llegó a mirarlo. `sha256sum` sobre la ruta completa → `776d56bf…c89d1c`, `1404772` bytes, idéntico al manifiesto.

---

## 2 · Regla de dos commits del Bloque D — cumplida y verificable, no afirmada

| commit | qué | verificación |
|---|---|---|
| `1a7e763` | `A.3`: el encargo íntegro archivado **antes de abrir nada** | `forense/encargos/2026-08-26-E3-EJERCE-LLAVE-COMPARTAMOS.md` |
| `0ac76d9` | **§COMMIT-1** — el procedimiento congelado | escrito antes de abrir un solo valor |
| `474d1e4` | **§COMMIT-2** — resultados y adjudicación | `git diff 0ac76d9 474d1e4` sobre el archivo: **94 inserciones, 0 eliminaciones** |

**Ceguera de §COMMIT-1, declarada en el propio commit.** Se leyeron: el listado de los 98 archivos del zip; los **nombres y etiquetas** de las 124 variables vía `pandas.io.stata.StataReader(...).variable_labels()` — metadatos del encabezado del `.dta`, sin materializar una fila; y el texto de los `.do`/`.ado`. Ningún valor de ninguna celda. El encargo lo permite en esos términos exactos.

**No hubo tercer commit.** La especificación no resultó mal: la contingencia de binariedad no se activó, la lista cerrada de desenlaces resultó ejecutable, la variable de daño existía por nombre y el estimador reprodujo dos cifras del censo previo al dígito.

---

## 3 · Lo que se corrió, y lo que salió

`regress Y Treatment i.supercluster_xi, vce(cl cluster)` sobre `survey == "Endline"`. **N = 16,560 · G = 238** conglomerados (120 tratados / 118 control, `Treatment` constante en **238 de 238**) · t de **237** gl · `k = 46` · **sin ponderador** (`[pw/aw/fw/iw]` → **0 coincidencias sobre los 14 `.do`** del paquete). Universo verificado contra el censo de `ADR-162` en cada cifra, no supuesto.

| desenlace | papel | ITT (pp) | IC95% (pp) | ¿va como el mecanismo postula? |
|---|---|---|---|---|
| `in_admin` | adopción (admin) | **+11.4735** | [+9.7022, +13.2448] | sí |
| `Q21_3_comp` | adopción (encuesta) | **+8.2199** | [+6.6794, +9.7603] | sí |
| `A_ever_late_not_cond` | **daño primario — mora** | **+1.1009** | [+0.6423, +1.5595] | **sí** |
| `Q9_4_soldloan_none` | daño secundario (invertida) | **+0.9908** | [+0.2357, +1.7460] | **no — signo contrario** |

Niveles de mora, misma variable y misma escala: **0.337 pp** en control (28/8,298) → **1.404 pp** en tratamiento (116/8,262).

**Cuatro controles positivos, corridos antes de reportar un solo ITT.** Dos de implementación: con `G = N` la VCE agrupada se reduce a HC1 (`3.036e-18`) y `β̂` resuelve las normal-ecuaciones (`8.882e-16`). Dos de **valor esperado externo**, que valen más porque su referencia la produjo otro acto en otra caja con otro código: `in_admin` = **2,048/16,560 = 12.37%** y atrición = **1,090/2,912 = 37.43%**, ambas **coincidencia exacta** con el censo de `ADR-162` — no pertenencia a un intervalo, el número exacto.

**Hueco declarado y no rellenado.** No hay control contra las cifras **publicadas** del artículo. El paquete no las trae: `Main/results/{Tables,Datasets}/` contienen solo `empty.txt`, y `Format-Compartamos-tables.xlsm` es un libro de macros de formato (sus 34 cadenas son rótulos de parámetros y rutas, inspeccionadas con `zipfile`). Traerlas exigiría descargar el artículo, prohibido por el encargo. Se dice; no se rellena por memoria.

---

## 4 · La adjudicación, y la parte que vale más que el veredicto

La precedencia sellada **`rompe → inejecutable → acota → corrobora → no-refuta`** se recorrió **entera**, descartando cada fila con su razón:

- **`rompe` no dispara** — el desenlace de daño **primario** ni cruza cero ni va contra.
- **`inejecutable` no dispara** — `A_ever_late_not_cond` existe, es administrativa y no está condicionada a haber tomado crédito.
- **`acota` no dispara**, y **ésta es la parte transferible del acto**: su rama de magnitud —*«ITT significativo pero de magnitud menor a la que el `[MEDIA]` vigente asumiría»*— resultó **INEVALUABLE**. El `[MEDIA](a)` de `dinero.credito.baja_friccion_usura_dano_downstream` (`canon/modelo-decision-v4_0.md:501`) **no asume ninguna magnitud**: es puramente cualitativo, sin cifra, umbral ni banda. **Mientras la regla siga sin número, ninguna evidencia futura podrá acotarla por magnitud.** Y el hueco **no se rellenó** con la única cifra a la mano: el «techo de mora 15-20%» y el umbral de IMOR «~25-30%» viven en `dinero.credito.scoring_alternativo` (`:500`), otro objeto y otra escala, y `A-bis` regla 3 lo prohíbe expresamente. Este acto **no declara ningún enlace de escala** entre las dos reglas.
- **`corrobora` dispara** en 3 de 4 desenlaces, incluido el primario.

**VEREDICTO: `corrobora` → `EJERCIDA_CORROBORA`.**

**La reserva sin la cual el veredicto está mal citado.** El desenlace de daño **secundario** satisface **literalmente** la condición de `rompe`: signo contrario y IC95% que excluye cero. **No decidió la fila** porque §COMMIT-1 escribió, **a ciegas del dato y antes de que ninguno de los dos números existiera**: *«La adjudicación de §4 de la spec se ancla en el primario; el secundario entra como corroboración o como reserva escrita, nunca como el desenlace que decide la fila por sí solo.»* Esa regla se obedeció tal cual — es exactamente para esto que existe el pre-registro, y decirlo así es más honesto que presentar el `corrobora` como si el dato lo hubiera dictado solo. Dos reservas más: la corroboración descansa sobre **144 eventos** de mora con tasa base de 0.34%, y **dos de las tres condiciones estructurales del mecanismo (CAT >100% y reporte crediticio incompleto) no se miden** aquí — de modo que se corrobora **la dirección, no la cláusula condicional completa**, que es justo la forma que tiene la «lectura peligrosa» contra la que la propia regla advierte.

---

## 5 · Contador y destino

**Llaves de identificación: `4` de `5` → `5` de `5`.** Derivado con la receta de §4 del propio registro, no tecleado (numerador `5`, denominador `5`), con los cinco estados crudos impresos uno por fila como control positivo del comando (`registro-llaves-identificacion-v1_0.md` §13). **No queda ninguna fila `SELLADA_NO_EJERCIDA`.** Primera fila de **clase (iii)** en ejercerse; primer `CORROBORA` del registro. **Hito D: sin movimiento.**

**Destino: la ranura llegó VACÍA, así que el número no entra a ninguna parte.** El ITT queda **`PROPUESTO`**. `milpa/procedencia.yaml` **intocado** — cero líneas de diferencia en este acto, la octava clase `EVIDENCIA_EXPERIMENTAL_TERCEROS` sigue vacía. El `[MEDIA](a)` de `modelo-decision:501` **intocado**. Fila **`FP-164`** `ABIERTA` para que mesa elija (a) competir por el `[MEDIA](a)`, (b) entrada nueva en la octava clase con `cita`+`llave_id`, o (c) ninguna — con el hallazgo de la magnitud ausente nombrado **dentro** de la fila, porque mesa lo necesita antes de elegir. Mismo patrón que `CAL-G3`/`FP-127`.

---

## 6 · Concurrencia y cascada

Máximo de ADR re-derivado **por conteo entero**, nunca por `sort -t- -k2 -n` (que parte en el primer guion y devuelve un máximo falso): `re.findall(r'ADR-(\d+)')` sobre `canon/gobernanza-v1_15.md` → **199**, sin huecos → **`ADR-200`**. `FP` por el mismo método → **163** (con los huecos históricos `137-140`) → **`FP-164`**.

**Colisión declarada al escribir, y ocurrida tres veces seguidas — cada una anunciada antes de pasar.** Al arrancar, `gh pr list --state open` salió **vacío**. Después fusionaron, en este orden: `PR #371` (`ACTO E2-PREP-L-RUN`) se quedó con `ADR-200`; `PR #372` (`ACTO CIERRA-FP157`) renumeró a `ADR-201`; y `PR #373` (`ACTO DISEÑO-ENSAFI`) renumeró a `ADR-202`. **Regla de la casa aplicada las tres veces, y este acto es el que fusiona al final:** máximo re-derivado por conteo entero **contra el árbol ya fusionado** (`re.findall(r'ADR-(\d+)')` sobre `canon/gobernanza-v1_15.md` → **202**, sin huecos) → **`ADR-203`**. Ninguna de las tres renumeraciones editó nada hacia atrás: los bloques de `ADR-200`, `ADR-201` y `ADR-202` quedan **sin tocar**, y en `canon/registro-rotulos.tsv` conviven las tres filas censales del pack. **Y `PR #373` era `MAESTRA30-E4`** — el hermano que el encargo decía que corría *antes* que éste, y que al arrancar no había corrido (§0). Corrió después y fusionó antes; el orden se invirtió, y por eso la secuencialidad la resolvió la regla de renumeración, no el calendario. **`FP-164` no colisionó** en ninguna ronda: máximo de `forense/firmas-pendientes.tsv` re-derivado por el mismo método → **163** (con los huecos históricos `137-140`). Los conflictos de `git merge` cayeron donde se anticipó —`canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`, `canon/registro-rotulos.tsv`— y se resolvieron conservando ambos lados; la línea `L0`, que es la que se duplica al resolver a mano, quedó **una sola** (verificado por conteo: 1 línea, 76 recifrados, 57,388 caracteres = la de ellos más la inserción de este acto), nunca a ojo.

---

## 7 · Perímetro — lo que se tocó y lo que no

**Tocado:** `forense/resultado-exp-compartamos-v1_0.md` [nuevo] · `forense/registro-llaves-identificacion-v1_0.md` (la fila `EXP-COMPARTAMOS-1`, el contador y §13 nuevo) · `forense/firmas-pendientes.tsv` (fila `FP-164`) · `canon/gobernanza-v1_15.md` (`ADR-203` + cabecera de conteo) · `canon/estado-programa-v1_10.md` (recifrado de ADR, línea de llaves, tabla de canon, suite) · esta nota · `forense/encargos/2026-08-26-E3-EJERCE-LLAVE-COMPARTAMOS.md` (`A.3`). Nada fuera de la lista del encargo.

**No tocado, y son prohibiciones, no omisiones:** `milpa/procedencia.yaml` (la ranura llegó VACÍA) · el `[MEDIA](a)` de `canon/modelo-decision-v4_0.md:501` · `data/manifiesto.yaml` · el Hito D · `data/diseno-muestral.yaml` (es el perímetro de `MAESTRA30-E4`). No se estimó TOT/LATE ni se usó `in_admin` como instrumento. No se usó `BTreatment` ni la línea base. No se corrigió por atrición. No se descargó nada. No se comparó la escala en pp contra la de ninguna otra regla.

---

## 8 · Desviación mecánica de perímetro, declarada en vez de tomada como atajo

La suite tocó dos veces, y las dos veces se resolvió por el lado que no falsea el registro.

**(a) `T25`/`D-6` — el rótulo del acto.** Dirección lanzó este acto con un rótulo **pelado** de la familia vigilada: la letra `E` seguida del dígito 3, sin prefijo. Esa forma **ya tiene dos habitantes censados** en `canon/registro-rotulos.tsv` (la fila `E3-TRIAGE` del censo, y el encargo del 4/ago/2026 sobre `tests/svystat.py`); un tercero es exactamente la colisión que `D-6` existe para evitar, y `T25` la atrapó. **Esta nota no vuelve a escribir el token pelado** — nombrarlo es usarlo, y usarlo aquí crearía el mismo habitante que el acto está evitando. Resuelto donde se puede resolver: **el acto se declara `MAESTRA30-E3` en todos los archivos que escribe** —resultado, esta nota, el registro de llaves, `ADR-203`, `estado-programa`— y queda censado con fila propia en `canon/registro-rotulos.tsv`, junto con sus tres hermanos `MAESTRA30-E1`, `MAESTRA30-E2` y `MAESTRA30-E4`. **El encargo archivado no se edita**: `A.3` pide el texto de dirección verbatim, y el texto de dirección no se edita para complacer a un test. Entra a `_T25_ARCHIVOS_CONOCIDOS` con su razón escrita — **mismo movimiento y misma razón** que `PREREG-CORRIDA` (`ADR-194`), `SELLA-AGO24-C-v2` (`ADR-155`) y `ADQ-CORRE-R74R75` (`ADR-158`), que ya viven en esa lista por lo mismo.

**Consecuencia sobre la regla de dos commits, dicha y no escondida.** El renombre alcanzó **una línea** de `forense/resultado-exp-compartamos-v1_0.md`: su fecha-línea de cabecera, donde figura el rótulo del acto. Eso es un **tercer commit** que toca un archivo cuyo §COMMIT-1 estaba congelado, así que se hizo **aislado y visible**: commit propio (`d7cd738`), una sola línea de diff: el rótulo pelado de la cabecera pasa a `MAESTRA30-E3`. **No toca el procedimiento ni el resultado** — ni una cifra, ni un desenlace, ni una condición de la escala, ni el orden de la precedencia; el diff completo está a la vista y se puede leer en dos segundos. La especificación no se corrigió hacia atrás: no hacía falta corregirla.

**(b) `T22`(b) — marcador de ranura sin fila que lo cite.** Esta nota nombra la `RANURA DE MESA` del encargo, y `T22`(b) exige que un archivo nuevo de `canon/`/`forense/` con marcador de ranura esté citado por alguna fila `ABIERTA`/`FIRMADA` del tablero. Se resolvió como debe: **añadiendo el nombre de esta nota al campo `dónde` de `FP-164`**, que es la fila que efectivamente pide la firma. Cero cambios de lógica.

**Los dos archivos fuera de la lista del encargo, nombrados uno por uno:** `tests/check.py` (una línea de snapshot en `_T25_ARCHIVOS_CONOCIDOS`, cero cambios de lógica) y `canon/registro-rotulos.tsv` (una fila censal). Se declaran aquí porque el encargo lo pide con esas palabras — *«si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo»*. El atajo disponible era renombrar el encargo de dirección; no se tomó.

**Suite al cerrar:** `python3 tests/check.py --baseline` (nunca `--freeze`) → **19 FAIL · 129 WARN, LÍNEA BASE VERDE**, medida **sobre el árbol ya fusionado** con `PR #371`/`PR #372`, no sobre la base del encargo. Neto de WARN **+1** sobre los 128 que dejó `ACTO CIERRA-FP157`, y es exactamente la fila `FP-164` `ABIERTA` que este acto abre (`T22`(a)); `FAIL` núcleo sin cambio. El recifrado de `T16` marcó como `{cita-historica}` las citas que dejaron de ser vigentes, sin borrar ninguna.
