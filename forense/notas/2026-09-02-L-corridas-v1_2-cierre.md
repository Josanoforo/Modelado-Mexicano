# `ACTO L-CORRIDAS-v1_2` — cierre

`ACTO L-CORRIDAS-v1_2`, 2/sep/2026, entorno **UBUNTU** (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`
= `sin_variable`, caja del usuario en `/home/pc0/Modelado-Mexicano`, `data/raw`
presente con 368 entradas — no se abre microdato en este acto). Rama
`L/corridas-v1_2`, nacida de `origin/main` = `6330ea3` (`Merge pull request #462`),
árbol limpio al arrancar. Firma de mesa **`DL-(1)`**, 2/sep/2026.

Este es el acto que **mesa corre** de `PAQUETE-L-v1_2` (`FP-228`), con una
enmienda al runner autorizada por la misma firma antes de lanzar.

## §0 · Firma de mesa, verbatim

> *"firmo (1) Enmendar el runner para que escriba `sha256_prompt` y `params`
> (restaurar el esquema de 9 claves que `carga_l_v1_1.py:130` ya valida),
> re-sellar sha, correr solo las 128 nuevas; los 96 quedan intactos con la
> re-derivación anexada como enmienda fechada y los 12 sha de hoy en la nota.
> La nomenclatura sin versión queda como fila FP aparte."*

## §1 · Compuerta de hashes

`sha256sum forense/prereg-duelo-v2/L-spec-v1_2.json` →
`bb49023ba71b5d04b4f8330ac6eed673eba0a7b7cb10c6c93df96c0311934885`, **idéntico**
al declarado en `L-spec-v1_2.sha256`. Sin discordancia.

## §2 · El defecto que motiva la enmienda — medido, no supuesto

El encargo de mesa pedía comparar, para cada una de las 96 rutas ya existentes
de las 6 celdas que v1.2 comparte con v1.1, el `sha256_prompt` del archivo
contra el sha256 del prompt que `construir_prompt()` genera hoy. **La
comparación no es ejecutable sobre esos artefactos.** Veredicto:

```
96 examinados · coinciden 0 · difieren 0 · sin campo sha256_prompt 96  (A.13)
```

Ninguno de los 96 trae `sha256_prompt`, y ninguno trae el texto del prompt ni
campo equivalente, así que no hay segunda vía de comparación. Los 96 comparten
un único esquema de **8 claves**, sin variación:
`fuente_citada · id_celda · indice · modelo_real · texto_crudo · timestamp ·
valor_extraido · variante` — faltan `sha256_prompt` y `params`.

**Universo declarado y control positivo (`A.13`).** `corridas-L/` tiene **296**
`.json`: **176** con el patrón `L-*-M__` (las 11 celdas de v1.1 × 2 variantes ×
k=8, commit `ba7bfa7`) y **120** del marco piloto. **Los 176 carecen de
`sha256_prompt`, no sólo los 96.** El mismo lector, sobre las **8** capturas del
piloto `CIV-08__L-solo__*.json`, encuentra la clave en **8 de 8** — el cero no
es de un lector roto ni de un comando que no examinó archivos.

**Causa, en dos piezas.** (i) `ejecutar_corrida()` escribía 8 claves y no esas
dos. (ii) La referencia de esquema de `dry_run()` en `runner_l_cli.py` se había
reducido a 7 claves, frente a las 9 que `carga_l_v1_1.py:130` valida — de modo
que **el runner daba verde sobre el esquema que él mismo había degradado**. Sin
la enmienda, las 128 capturas nuevas habrían nacido con el mismo hueco: el
problema no quedaba atrás, se duplicaba.

## §3 · Re-derivación de los 96 — evidencia sobre los insumos, no sobre los archivos

Los 176 archivos de v1.1 **no se tocan** (insumo sellado del agregado-b). Lo que
sigue es la re-derivación que la firma manda anexar. Es una cadena sobre los
**insumos**; **no** es una verificación de los archivos, que siguen sin llevar
prueba propia de con qué prompt nacieron.

1. **Las 6 entradas de spec compartidas son byte-idénticas** entre
   `L-spec-v1_1.json` y `L-spec-v1_2.json` (`json.dumps` con claves ordenadas):
   `CIV-M-01`, `CIV-M-12`, `CIV-M-13`, `FAM-M-01`, `TRA-M-03`, `TRA-M-07`,
   las 6 de 6.
2. **Los 12 prompts (6 celdas × 2 variantes) construidos hoy bajo v1.1 y bajo
   v1.2 dan el mismo `sha256`, 12 de 12**, con **control negativo**: dos pares
   distintos no colisionan. La versión de spec no toca estos prompts.
3. **La cadena que construye el prompt no se ha tocado desde la corrida.**
   `pipeline-L-adv1-m2.py` (`construir_prompt`) en `ac731cc`, 20/ago;
   `carga_l_v1_1.py` (`celda_a_spec`, `construir_params`) en `3839e1d`,
   1/sep 04:39 UTC; ventana de captura de los 176, leída de los propios
   `timestamp`: **2026-09-01T20:30:40Z – 21:51:23Z**. El único cambio posterior
   al runner (`967d067`, 2/sep 04:35 UTC) toca **sólo** contadores y aserciones
   de `dry_run()`/`correr()` — quita los literales `11`/`176` — y no roza la
   construcción del prompt.

**Alcance honesto de lo anterior:** hoy la equivalencia se sostiene porque el
árbol de código no cambió; deja de ser verificable en cuanto alguien toque el
pipeline, y nunca fue una propiedad del archivo. Por eso la conclusión de este
acto sobre los 96 es `K=96`, no `coinciden 96`.

### Los 12 `sha256` de los prompts construidos hoy

| celda | variante | `sha256` del prompt construido el 2/sep/2026 |
| --- | --- | --- |
| `CIV-M-01` | `L+corpus` | `ccc560d8ee804c8a70fa39ecf418d1dc4aaea8ffa9f567fe12680f56cfcb2f92` |
| `CIV-M-01` | `L-solo` | `a3742903eb175c351deef91ca54308c2541a05214fecef4c4dfbb638d505d4dd` |
| `CIV-M-12` | `L+corpus` | `593b716f031eb3dcbbda8b6ffa1ee555e71a14b973373091416505164020eb16` |
| `CIV-M-12` | `L-solo` | `16d03b55b5f0367c4a3f616f408c62b0a8b34c15ec25133e695da55788f214b2` |
| `CIV-M-13` | `L+corpus` | `5b6e68d4f2fd83bfad8f919017a92ee3521f968230d8151701bacf41cedda074` |
| `CIV-M-13` | `L-solo` | `2a234d666fd452b123ac6236ca86ac87da0194273a46b2559f505dcd9dcb7ec2` |
| `FAM-M-01` | `L+corpus` | `abbd2b50a1841fb80eb0ab9d798d64a9791ada1b815476b9c7ab88d64abc8aa7` |
| `FAM-M-01` | `L-solo` | `2abf2dbb064411640e9fa6fb744e10cee70d658576ea052ca97c968d8ffa984d` |
| `TRA-M-03` | `L+corpus` | `f47790ede06e781a94a9cb477ccda181b04229eb873d452f32ae150f19c3d51a` |
| `TRA-M-03` | `L-solo` | `ce81dcb2e7ddb08f43fbc504f591085ed7576d76d9c327dde745162c45289a7d` |
| `TRA-M-07` | `L+corpus` | `bfcd28974bd03047df23af73a9af4e6a6419a8b725fe60477abd41748fe86c06` |
| `TRA-M-07` | `L-solo` | `b0d23660e7212426a9a426e085853953463a9ef32a241d0a292f71cec4786c43` |

## §4 · La enmienda al runner (P1 de la firma)

`forense/prereg-duelo-v2/runner_l_cli.py`, cinco cambios y nada más:

1. `ejecutar_corrida()` recibe los `params` y escribe **`sha256_prompt`**
   (sha256 utf-8 del prompt **exacto que se envía** — el último argumento de
   `construir_comando_cli`) y **`params`** (`dataclasses.asdict` de lo que
   `construir_params` devuelve).
2. `_iter_plan()` cede los `params` en vez de descartarlos, para no
   re-derivarlos en el sitio de escritura (la variable deja de llamarse
   `params_dummy`: ya no lo es).
3. La referencia de esquema de `dry_run()` vuelve a **las 9 claves de
   `carga_l_v1_1.py:130`**.
4. Dos importaciones (`hashlib`, `dataclasses.asdict`).
5. Los tres desempaques de `_iter_plan()`.

**La construcción del prompt no se toca.** Nada más cambia.

**Regresión obligatoria, verde en las dos:** `--dry-run` con
`L-spec-v1_1.json` → **176** rutas; con `L-spec-v1_2.json` → **224**. En ambos
casos la verificación de esquema de 9 claves pasa contra
`CIV-08__L-solo__01.json`.

**Re-sellado:** `sha256sum runner_l_cli.py` →
`7ac9852e22201bc61218d2ccfb501e97efc76b51d55261abf213388257e04e4b`. El de
`MAESTRA34-N4`, `0c10e9ab95350ce2b3596216eeda0c23e270bce492177bd14c5657c6e28598e2`,
queda como historia — verificado antes de sobreescribir: el `sha256` del
archivo **pre-parche** (`git show HEAD:...`) es exactamente ese `0c10e9ab…`, así
que el que se retira es el que la firma nombra y no otro. Enmienda fechada en
`PAQUETE-L-v1_2/PAQUETE-L-v1_2.md` §6, como **ENMIENDA 2**, citando `DL-(1)`.

## §5 · La corrida (P2 de la firma)

`--correr` con la spec v1.2 **por override en runtime** — import por ruta y
`r._CARGA.L_SPEC_JSON = D / "L-spec-v1_2.json"`; **ningún `.py` se editó para
apuntar la spec**. Cliente `claude` **2.1.258**, sesión de `claude.ai`
(`authMethod: claude.ai`, `apiProvider: firstParty`), **sin
`ANTHROPIC_API_KEY`**, conforme a la firma `MAESTRA33-E17`.

Reanudación: de las 224 rutas de v1.2, **96 ya existían** (las de v1.1) y se
saltaron sin tocarse; **128** se invocaron.

**Conteo de la corrida, con la interrupción declarada.** El primer lanzamiento
se hizo con `nohup` desde una llamada de shell que terminó antes que el
proceso: el sandbox se llevó el árbol de procesos y el runner **murió tras
escribir 1 captura** (`L-CIV-M-02-M__L-solo__01.json`), con log vacío y sin
traza. Se relanzó bajo el gestor de tareas del entorno, y por ser reanudable
retomó en la 2 sin repetir ninguna: la segunda invocación reporta
`127 corridas nuevas, 97 ya existentes (reanudación), total 224` — las 97 son
las 96 de v1.1 más la única que el intento abortado alcanzó a dejar escrita.
**Total real de capturas nuevas de este acto: 1 + 127 = 128.**

### Verificación de las 128 (`A.13`)

Universo: las **224** rutas que `_iter_plan()` deriva de `L-spec-v1_2.json`,
clasificadas contra `git status --porcelain` (128 sin versionar = nuevas de
este acto; 96 ya versionadas = reanudadas de v1.1).

```
con sha256_prompt                          : 128/128
con params                                 : 128/128
sha256_prompt == sha256(prompt construido) : 128/128
sin campo: ninguna | discrepantes: ninguna
control negativo (cotejo contra el prompt de otro par): 0/128
```

El **control negativo** importa tanto como el positivo: cotejar cada archivo
contra el prompt de *otro* par `(celda, variante)` da **0** coincidencias, de
modo que el `128/128` de arriba no es el resultado de un comparador que
siempre dice que sí.

**Los 176 de v1.1, intactos:** `git status --porcelain` sobre `corridas-L/`
devuelve **0** archivos modificados o borrados; los 128 aparecen todos como
`??`. Nada se movió ni se renombró.

**Salud de las respuestas:** 0 de 128 con `texto_crudo` vacío; longitudes
mín/mediana/máx = 1020 / 1857 / 2543 caracteres.

**Hueco medido, no reparado (`modelo_real`):** las 128 capturas traen
`modelo_real = None`, las 128. El cliente `claude` 2.1.258 no emite la clave
`model` en el JSON de `--output-format json`, y el runner declara `None` en vez
de inventar (comportamiento previo, `runner_l_cli.py:113-123`). Consecuencia:
**el registro sellado no guarda qué modelo respondió**, sólo el alias `opus`
del comando y el `modelo_id` sellado en `params`
(`claude-opus-4-6`, valor precargado por mesa en el paquete — `F2(a)` del
pre-registro — y no una lectura del proveedor). La firma `DL-(1)` dice «nada más cambia», así que **no se tocó**;
queda declarado aquí para que mesa decida si merece fila propia.

## §6 · Lo que este acto NO cierra — la nomenclatura

`corridas-L/L-<id>-M__<variante>__<indice>.json` no codifica la versión de
spec, así que la reanudación de `correr()` decide **por nombre** y no puede
comprobar que un archivo existente corresponda al prompt vigente. Desde este
acto las capturas nuevas sí llevan `sha256_prompt`, lo que cierra el
diagnóstico a futuro — pero **no** la reanudación: un archivo viejo sigue
ganando por nombre antes de que nadie mire su contenido.

**Segundo sitio ya afectado, medido.** La COMPUERTA de la ENMIENDA 1 de
`MAESTRA34-N3` verifica el producto con
`git show origin/main:forense/prereg-duelo-v2/corridas-L/ | grep -c "__v1_2"`
= 224, y ese sufijo no existe en la nomenclatura: el comando devuelve **0**
(control positivo `A.13`: el mismo comando con `L-CIV-M-01-M` devuelve **16**;
el árbol lista **296** `.json`). **`MAESTRA34-N3` no podía abrir su compuerta.**
Se anexó **ENMIENDA 2** al pie de su encargo — con la procedencia del texto
declarada y la ratificación de dirección del 2/sep — sustituyendo esa compuerta
por una que deriva las 224 rutas de la spec y las intersecta con `origin/main`.
Probada antes de escribirla: contra `L-spec-v1_1.json` da **176 / 176**
(control positivo) y contra `L-spec-v1_2.json` da **224 / 96** hoy, que pasa a
`224 / 224` al fusionar este PR.

Tablero: fila nueva **`FP-235`** (`ABIERTA`, vence 2026-09-15) por la
nomenclatura sin versión; **`FP-228`** pasa a `EJECUTADA`.

## §7 · Suite

`python3 tests/check.py --baseline`, sobre el árbol **ya fusionado con
`origin/main` = `4de5b1e`** (que trae `tests/check.py` modificado por los PR
#463/#464, así que una cifra pre-merge no serviría).

**Núcleo citado, en los dos entornos, porque no dan lo mismo y la diferencia es
del entorno, no del acto:**

| dónde | núcleo | línea base |
| --- | --- | --- |
| CI (clon limpio, autoritativo) | `19 FAIL · 165 WARN` | **VERDE — nada nuevo** |
| caja UBUNTU de la corrida | `21 FAIL · 165 WARN` | 2 entradas `T27`, ajenas |

La diferencia **cuadra exactamente**: 19 + las 2 `T27` de la caja = 21. No hay
un tercer `FAIL` sin explicar.

El `FAIL` de más en UBUNTU y las 2 entradas de línea base son **`T27`** sobre
`data/raices.local.yaml` y `data/secretos.local.yaml`: gitignorados
(`.gitignore:7-8`), no versionados (`git ls-files --error-unmatch` falla en
ambos) y del **31/jul** y **6/ago**, anteriores a esta sesión. `T27` barre el
árbol de trabajo incluyendo ignorados, así que salen en la caja y no en el CI.
Ninguno entra al commit. **La cifra que manda es la del CI.**

**Dos FAIL fueron de este acto, y los dos eran el mismo lazo.** `T22` marca un
archivo cuando trae un marcador de ranura nuevo que ninguna fila del tablero
cita; su detector es una expresión regular sobre esa palabra **en mayúsculas**,
de modo que **no distingue mención de uso**. (1) La primera pasada con las 128
capturas dentro dio `22 FAIL`: `§5` explicaba de dónde sale `modelo_id`
escribiendo esa palabra en mayúsculas — la frase que *explicaba* el valor
precargado creaba el marcador. Se reformuló. (2) El párrafo que narraba esa
corrección **volvió a crear el defecto**, porque citaba la expresión regular y
el nombre de su constante, y los dos contienen el token; el CI lo atrapó
después de que este acto lo diera por cerrado. Se reformuló también, sin
nombrar ninguno de los dos. Se corrige aquí sin tocar `tests/check.py` y sin
pedir exención — el archivo del acto se adapta al test, no al revés.

**Autocrítica del método, no sólo del texto.** El (2) no lo cazó la suite local
sino el CI, y la causa es de procedimiento: la cifra que esta sección citaba se
midió **antes** de escribir esta sección, y el commit salió sin volver a
correrla. Un número de suite sólo vale para el árbol que lo produjo. Precedente
ya registrado en la casa (`CAJA-RESIDUOS`, `FP63-CIERRA`, la ranura citada
dentro de su propia compuerta): **el bloque que narra la corrección de un
marcador es el sitio más probable donde el marcador reaparece.**

**Control tras la corrección**, con el detector real importado de
`tests/check.py` y control positivo sobre una cadena de prueba: **0** aciertos
del marcador de ranura y **0** del patrón de pendiente-de-mesa en los cuatro
archivos que este acto escribe. Los aciertos que quedan en
`forense/firmas-pendientes.tsv` son las filas preexistentes del tablero, que es
justamente la fuente que `T22` usa para dar por citado un marcador.

**Integridad tras el merge** (un merge sin `CONFLICT` puede romper en
silencio): tablero con **226** filas, **cero** ids duplicados, **cero** filas
con distinto de 9 columnas, y las ediciones que `main` traía sobrevivieron
(`FP-231`/`FP-232` siguen `EJECUTADA`). `canon/gobernanza-v1_15.md` queda
**byte-idéntica** a `origin/main` (`git diff` = 0 líneas): este acto no escribe
`ADR`, y la lista de números de `ADR` repetidos es **idéntica** en las dos
ramas, es decir preexistente y no inducida por este merge.

**Compuerta de `MAESTRA34-N3`, ya contra el commit de este acto:** el bloque de
la ENMIENDA 2 da `224 / 224` para `L-spec-v1_2.json` y `176 / 176` para
`L-spec-v1_1.json` (control positivo). La compuerta abre.

## §8 · Lo que este acto NO hace

No edita `pipeline-L-adv1-m2.py` ni `carga_l_v1_1.py`; no toca la construcción
del prompt; no edita ni renombra ninguno de los 176 archivos de v1.1 (insumo
sellado del agregado-b); no corre el extractor ni el agregado ni el scoring; no
abre microdato; no adjudica ninguna celda; no activa el corredor E; no repara
la nomenclatura (queda en `FP-235`).

**CONTADOR:** capturas L del marco v1.2: 96 → **224** (128 nuevas de este
acto). Celdas puntuadas: **cero** — este acto captura, no interpreta.
