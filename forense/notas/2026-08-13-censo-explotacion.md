# ACTO A · Censo de explotación — el contador que el ADR de provisionalidad instituye, medido por primera vez — 2026-08-13

## ARRANQUE (verificado antes de leer el resto del encargo)

1. **REPO.** Clon existente en `/home/user/Modelado-Mexicano` (no se clonó uno nuevo). `git log -1 --format="%h %s"` → al arrancar, `dcc4f6a Merge pull request #196 from Josanoforo/claude/new-session-s98494`. Rama `claude/censo-explotacion-adr-9rq3xo`, árbol limpio, worktree propio (no compartido con otro acto).
2. **SHA.** Base declarada por el encargo: `dcc4f6a`. Durante el arranque, `git fetch origin main` mostró que `origin/main` ya había avanzado a `5f90757` (ACTO SONDA-1, PR #197, `Josanoforo/sonda1-mapa-barreras-lote2`) — no es PARO, lo declara el propio §2. Verificado antes de tocar nada: `git diff --stat dcc4f6a origin/main -- data/manifiesto.yaml data/*variables*.tsv data/curacion-registro/relaciones.tsv` da **salida vacía** — SONDA-1 no toca ninguno de los tres artefactos que este censo mide (solo agrega `data/universo-puertas-2026-08-12.tsv` y su propia nota/encargo). Se hizo fast-forward de la rama de trabajo a `5f90757` para partir del terreno más fresco; el universo medido es idéntico al que `dcc4f6a` ya tenía. HEAD de este acto: `5f90757`.
3. **`data/raw`.** Ausente — verificado (`ls data/raw` → `No such file or directory`). No es PARO y aquí es parte del diseño: este acto mide `data/manifiesto.yaml` (procedencia) y las TSV de apertura, nunca el disco. Declarado, se salta.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — firma correcta de acto de nube (ADR-59(b)), sin sonda de red: el encargo la pide saltada explícitamente y este acto no toca microdato ni red.
5. **ESPEJO.** No se usó ningún espejo del proyecto. Toda cifra de esta nota sale del clon de (1), con el comando a la vista.

### Premisas (§2), corridas verbatim

```
$ python3 -c "import yaml,sys;t=open('data/manifiesto.yaml',encoding='utf-8').read().split(chr(10));i=0
while t[i].startswith('#') or not t[i].strip(): i+=1
m=yaml.safe_load(chr(10).join(t[i:]));print('entradas',len(m),'con payload',sum(1 for e in m if e.get('archivo') and e.get('sha256')))"
entradas 554 con payload 550

$ ls data/*variables*.tsv
data/abrir4-variables-2026-08-08.tsv
data/verif3-variables-2026-08-08.tsv

$ ls data/censo-explotacion-*.tsv 2>/dev/null && echo "YA EXISTE - PARA"
(sin salida — no existe, se procede)
```

Universo de este censo: **550 payloads** (de 554 entradas totales del manifiesto; 4 quedan fuera por no traer `archivo`+`sha256` a la vez — verificado, ninguna de las 4 trae uno sin el otro). Dos TSV de apertura existen hoy: `abrir4-variables-2026-08-08.tsv` y `verif3-variables-2026-08-08.tsv`. No existe `data/censo-explotacion-*.tsv` previo — se procede.

---

## COMMIT 1 · La definición, antes de contar

Los cuatro estados y su criterio, escritos y probados **antes** de correr el censo completo (v2.3: la receta se prueba antes de creerla).

### Los cuatro estados, operacionalizados

| estado | criterio exacto |
|---|---|
| `EXPLOTADO` | El `id_manifiesto` del payload aparece en alguna fila de un TSV de apertura con reactivo hallado. En `abrir4-variables-2026-08-08.tsv` eso es la columna `variable_encontrada` no vacía (vacía = cadena vacía o el placeholder `—` que la propia TSV usa para "nada"). Las TSV de apertura que **no** traen columna `variable_encontrada` (hoy, `verif3-variables-2026-08-08.tsv`) no tienen ese campo que leer — para ellas el criterio equivalente es `clasificacion_a4 = EXISTE-SATISFACE` (ver nota de diseño abajo). |
| `ABIERTO-SIN-HALLAZGO` | Aparece en un TSV de apertura y su fila **no** califica como `EXPLOTADO`: `clasificacion_a4` es `NO-ENCONTRADO` o `EXISTE-NO-SATISFACE`. Se abrió. Cuenta distinto de no haberlo mirado. |
| `REFERENCIADO-NO-ABIERTO` | Ningún TSV de apertura toca el payload, pero alguna fila de `relaciones.tsv` lo cita **por `id_manifiesto` exacto** (columna estructurada, igualdad de cadena completa — nunca `NO_DETERMINADO`). |
| `SIN-DEMANDA` | Ningún TSV de apertura lo toca y ninguna fila de `relaciones.tsv` lo cita por `id_manifiesto` resuelto. |

Los cuatro son mutuamente excluyentes por construcción: primero se pregunta "¿algún TSV de apertura lo toca?" (decide EXPLOTADO/ABIERTO-SIN-HALLAZGO); solo si la respuesta es no se pregunta "¿`relaciones.tsv` lo cita?" (decide REFERENCIADO-NO-ABIERTO/SIN-DEMANDA). Un payload nunca cae en dos cajas.

**Nota de diseño — por qué `clasificacion_a4` y no `variable_encontrada` para `verif3`.** `verif3-variables-2026-08-08.tsv` no tiene columna `variable_encontrada`; tiene `variables_encontradas` (plural), que documenta el **esquema real del archivo** para verificación negativa (qué columnas existen de verdad), no un reactivo localizado que responda a una necesidad — leídas sus 4 filas, las cuatro listan encabezados genéricos (`Country,Month,Year,Events`; `CVEENT,entidad,beneficiarios...`) mientras el texto declara explícitamente "NINGUNA variable de [lo buscado]". Tratar esa columna como equivalente a `variable_encontrada` sería la misma trampa de identidad que el encargo nombra en otro plano (confundir dos columnas de nombre parecido y semántica distinta). Por eso el criterio operativo para TSV sin `variable_encontrada` usa `clasificacion_a4` directamente — columna presente en ambas TSV con vocabulario controlado (`NO-ENCONTRADO` / `EXISTE-NO-SATISFACE` / `EXISTE-SATISFACE`), y verificado que donde ambas señales coexisten (`abrir4`) nunca se contradicen: toda fila `EXISTE-SATISFACE` en `abrir4` ya tiene `variable_encontrada` no vacía.

### Prueba contra tres casos conocidos (salida real, pegada sin editar)

```
=== ensafi2023_bd_csv_zip (7 filas en abrir4-variables) ===
  necesidad='3.11 sens_estatus (G2,G4)'    variable_encontrada='—'          clasificacion_a4='NO-ENCONTRADO'      -> ABIERTO-SIN-HALLAZGO
  necesidad='4.6 aversion_riesgo (G2,G3)'  variable_encontrada='IMPULSIVID' clasificacion_a4='EXISTE-NO-SATISFACE' -> EXPLOTADO
  necesidad='10 horizonte_temporal (G4)'   variable_encontrada='ORIEN_FUT'  clasificacion_a4='EXISTE-NO-SATISFACE' -> EXPLOTADO
  necesidad='12 familismo_apoyo (no-ENIF)' variable_encontrada='—'          clasificacion_a4='NO-ENCONTRADO'      -> ABIERTO-SIN-HALLAZGO
  necesidad='13 familismo_obligacion'      variable_encontrada='—'          clasificacion_a4='NO-ENCONTRADO'      -> ABIERTO-SIN-HALLAZGO
  necesidad='14 puente radio_confianza'    variable_encontrada='CONF_FINAN' clasificacion_a4='EXISTE-NO-SATISFACE' -> EXPLOTADO
  necesidad='theta subjetivos (ENBIARE-like)' variable_encontrada='OPTIMISMO' clasificacion_a4='EXISTE-NO-SATISFACE' -> EXPLOTADO
  ESTADO DEL PAYLOAD (EXPLOTADO si CUALQUIER fila lo es) = EXPLOTADO

=== enbiare2021_fd_pdf (7 filas en abrir4-variables) ===
  necesidad='3.11 sens_estatus (G2,G4)'    variable_encontrada='—'  clasificacion_a4='NO-ENCONTRADO' -> ABIERTO-SIN-HALLAZGO
  necesidad='4.6 aversion_riesgo (G2,G3)'  variable_encontrada='—'  clasificacion_a4='NO-ENCONTRADO' -> ABIERTO-SIN-HALLAZGO
  necesidad='10 horizonte_temporal (G4)'   variable_encontrada='PA6 (peldano de vida a 5 anios) + PA3_08 (...)' clasificacion_a4='EXISTE-NO-SATISFACE' -> EXPLOTADO
  necesidad='12 familismo_apoyo (no-ENIF)' variable_encontrada='PB2_1' clasificacion_a4='EXISTE-SATISFACE' -> EXPLOTADO
  necesidad='13 familismo_obligacion'      variable_encontrada='—'  clasificacion_a4='NO-ENCONTRADO' -> ABIERTO-SIN-HALLAZGO
  necesidad='14 puente radio_confianza'    variable_encontrada='PB1_01 / PB1_02 (...) + PF1_1..6 (...)' clasificacion_a4='EXISTE-SATISFACE' -> EXPLOTADO
  necesidad='theta subjetivos (ENBIARE-like)' variable_encontrada='PA1 (...) + PA3_01..17 (...) + PA4_01..10 (...)' clasificacion_a4='EXISTE-SATISFACE' -> EXPLOTADO
  ESTADO DEL PAYLOAD (EXPLOTADO si CUALQUIER fila lo es) = EXPLOTADO

=== latinobarometro2024_bd_stata ===
filas con id_manifiesto conteniendo 'latinobar' (acento normalizado, columna estructurada): 0
filas que MENCIONAN Latinobarómetro en fuente_canonica_normalizada/fuente_nombre (texto libre): 2
  REL-4360d0a91e5f8be30916c2b9 necesidad=N30 fuente_canonica_normalizada='LATINOBARÓMETRO' id_manifiesto='NO_DETERMINADO'
  REL-f09043ef09997adc0bb4a3f2 necesidad=N15 fuente_canonica_normalizada='LATINOBARÓMETRO' id_manifiesto='NO_DETERMINADO'
-> ninguna de estas dos filas tiene id_manifiesto resuelto: mencionan la fuente en texto libre, no citan el payload por id.
tocado por abrir4: False · tocado por verif3: False · citado por id_manifiesto exacto en relaciones.tsv: False
ESTADO = SIN-DEMANDA
```

Los tres casos dan el resultado que el encargo anticipaba: `ensafi2023_bd_csv_zip` → **EXPLOTADO** (ABRIR-4 localizó `IMPULSIVID`/`ORIEN_FUT`/`CONF_FINAN`/`OPTIMISMO` — ninguno satisface la necesidad que buscaba, todos quedan `EXISTE-NO-SATISFACE`, pero el criterio de `EXPLOTADO` es "reactivo hallado", no "necesidad satisfecha"; esa es una vara más baja y deliberada — ver §0, el contador del ADR mide si el payload se abrió y rindió algo, no si resolvió una necesidad). `enbiare2021_fd_pdf` → **EXPLOTADO**, como el encargo declaraba. `latinobarometro2024_bd_stata` → **SIN-DEMANDA**, como el encargo declaraba.

### La trampa de identidad, declarada

El encargo advierte que cruzar payload↔fuente por subcadena produce falsos positivos (`SE` dentro de "fal**se**ador", etc.). Este censo **no cruza por subcadena en ningún punto**: las tres uniones (payload↔`relaciones.tsv`, payload↔TSV de apertura) comparan el campo estructurado `id_manifiesto` por **igualdad exacta de cadena completa**, nunca por contención de un fragmento dentro de texto libre. Verificado que esto no pierde nada por accidente: `set(ids citados por relaciones.tsv) - set(ids del manifiesto)` → `[]`, y `set(ids tocados por TSV de apertura) - set(ids del manifiesto)` → `[]` — cero ids huérfanos en ninguna dirección, cero drift de nombres. El caso Latinobarómetro (arriba) muestra la otra cara de la misma disciplina: las columnas de texto libre (`fuente_canonica_normalizada`, `fuente_nombre`) sí llevan el acento (`LATINOBARÓMETRO`) y este censo **nunca las consulta** para decidir estado — por construcción es inmune tanto a perder una cita real por diferencia de acento como a inventar una cita falsa por coincidencia de texto libre.

### Alcance del universo, declarado (A.4)

Universo = los 550 payloads con `archivo`+`sha256` en `data/manifiesto.yaml` al HEAD de este acto (`5f90757` — idéntico a `dcc4f6a` en las cuatro tablas que importan, verificado en ARRANQUE/2) + las TSV de apertura que existían el 13/ago/2026: `abrir4-variables-2026-08-08.tsv`, `verif3-variables-2026-08-08.tsv`. `relaciones.tsv` (197 filas, 43 con `id_manifiesto` resuelto) se usa solo para decidir `REFERENCIADO-NO-ABIERTO`/`SIN-DEMANDA`, nunca se escribe. No apareció ningún `APERTURA-ISSP` ni TSV de apertura adicional durante la corrida de este acto — no hubo fusión concurrente que obligara a decidir corte; si hubiera aparecido, se declara aquí que no apareció, no se ocultó la pregunta.

**El primer resultado que produzca este procedimiento es el que se reporta.**

---

## COMMIT 2 · El censo

`data/censo-explotacion-2026-08-13.tsv` — 550 filas (+1 encabezado), una por payload, columnas `id_manifiesto · archivo · raiz · tamano_bytes · usado_para_declara_uso · necesidades_que_lo_citan · tsv_de_apertura_que_lo_toca · estado · universo_declarado`. `necesidades_que_lo_citan` sale de `relaciones.tsv` (unión por `id_manifiesto` exacto, nunca `NO_DETERMINADO`); vacía cuando ninguna fila cita ese id — no se usa `—` ahí (esa marca es convención de las TSV de apertura para "no encontrado dentro de una fila de verificación puntual"; aquí una celda vacía significa, sin ambigüedad, "cero citas"). `usado_para_declara_uso` es el campo `usado_para` del manifiesto, con saltos de línea/tabs colapsados a espacio para mantener una fila = una línea física (mismo formato que ya usan `relaciones.tsv`/`abrir4-variables`); donde el texto trae comillas internas, `csv.writer` las cita correctamente (RFC4180) — parseable con cualquier lector TSV estándar (`csv.reader`, `pandas.read_csv(sep="\t")`); un `split("\t")` ingenuo solo tropieza en las filas que ya traían comillas en el manifiesto de origen, no en las demás.

### Cifra 1 · `EXPLOTADO` / total

```
$ awk -F'\t' 'NR>1{t++; if($8=="EXPLOTADO")e++} END{printf "%d/%d = %.4f%%\n", e, t, 100*e/t}' data/censo-explotacion-2026-08-13.tsv
4/550 = 0.7273%
```

**Tensión declarada, no resuelta unilateralmente.** §4 pide literalmente "`EXPLOTADO`/total — el contador que el ADR instituye" → **4/550 = 0.73%**. Pero §0 describe ese mismo contador como "`payloads con apertura registrada / payloads en manifiesto`, hoy 8 de 550 = 1.45%" — y **8/550 = 1.4545…% ≈ 1.45%** es exactamente `(EXPLOTADO + ABIERTO-SIN-HALLAZGO)/total` en esta derivación, no `EXPLOTADO/total`:

```
$ awk -F'\t' 'NR>1{t++; if($8=="EXPLOTADO"||$8=="ABIERTO-SIN-HALLAZGO")a++} END{printf "%d/%d = %.4f%%\n", a, t, 100*a/t}' data/censo-explotacion-2026-08-13.tsv
8/550 = 1.4545%
```

Las dos lecturas del "contador del ADR" no son el mismo número (4 contra 8) y el propio encargo las trata como si lo fueran. "Apertura registrada" (§0) es, por el propio texto de §3, exactamente el conjunto `EXPLOTADO ∪ ABIERTO-SIN-HALLAZGO` — "se abrió, cuenta distinto de no haberlo mirado" —, mientras que "`EXPLOTADO`" (§4.1) es el subconjunto más estrecho que además rindió un reactivo. La coincidencia exacta de 8/550=1.45% con la cifra que §0 ya declaraba "hoy" es la evidencia de que el contador que el ADR realmente instituye es la lectura de "apertura registrada" — pero este acto no adjudica esa lectura por su cuenta: quedan las dos cifras derivadas y trazables, con su comando, para que mesa selle cuál es el contador oficial del ADR.

### Cifra 2 · `SIN-DEMANDA` / total

```
$ awk -F'\t' 'NR>1{t++; if($8=="SIN-DEMANDA")s++} END{printf "%d/%d = %.4f%%\n", s, t, 100*s/t}' data/censo-explotacion-2026-08-13.tsv
538/550 = 97.8182%
```

**538 de 550 (97.82%), no ≈321 de 550 (58%) como estimaba el encargo.** Diferencia de 217 payloads — no es ruido de redondeo. No se ajustó la regla para acercarse a la cifra esperada (v2.3: se reporta el primer resultado). Esta rederivación usa únicamente igualdad exacta de `id_manifiesto` (§ Trampa de identidad, arriba); si la cifra de ≈321/58% salió antes de cruzar payload↔necesidad por nombre/subcadena en vez de por `id_manifiesto` resuelto, sería exactamente el tipo de sobre-conteo que la trampa de identidad de este mismo encargo advierte — pero este acto no tiene a la vista cómo se produjo el ≈321 original y no lo afirma como causa, solo señala que es el mecanismo que produciría un SIN-DEMANDA artificialmente más bajo. Lo que sí está verificado: de las 550, solo 12 payloads distintos tienen algún enganche real (8 citados por `id_manifiesto` en `relaciones.tsv`, 8 tocados por una TSV de apertura, con 4 de traslape) — los 538 restantes no tienen ninguna de las dos señales.

### Cifra 3 · `REFERENCIADO-NO-ABIERTO` — la cola real de apertura

```
$ awk -F'\t' 'NR>1 && $8=="REFERENCIADO-NO-ABIERTO"{n=split($6,a,","); print n, $1, $6}' data/censo-explotacion-2026-08-13.tsv | sort -rn
6 za6980_q_mx                                          N2,N12,N13,N14,N28,N30
4 cses5_modulo5_2016_2021_cuestionario                  N17,N25,N26,N27
3 za5900_q_mx                                           N12,N13,N30
2 f00006635_wvs7_questionnaire_mexico_2018_spanish      N5,N15
```

Cuatro payloads, cero solapados con los `EXPLOTADO`/`ABIERTO-SIN-HALLAZGO`. `za6980_q_mx` (ISSP 2017 Social Networks, cuestionario) es citado por 6 necesidades distintas y ningún TSV de apertura lo ha tocado — es, por evidencia y no por intuición, el siguiente candidato a abrir. Le sigue `cses5_modulo5_2016_2021_cuestionario` (4), `za5900_q_mx` (3, ISSP 2012 Family and Changing Gender Roles) y `f00006635_wvs7_questionnaire_mexico_2018_spanish` (2). Los cuatro son cuestionarios/documentación (PDF/TXT), no bases de datos — ninguno de los cuatro tiene todavía un TSV de apertura que los procese a nivel variable.

### Cifra 4 · Bloques `SIN-DEMANDA` grandes por prefijo

```
$ awk -F'\t' 'NR>1 && $8=="SIN-DEMANDA"{id=tolower($1); match(id,/^[a-z]+/); pfx=(RSTART==1)?substr(id,RSTART,RLENGTH):id; c[pfx]++} END{for(k in c) print c[k], k}' data/censo-explotacion-2026-08-13.tsv | sort -rn
```

| n | prefijo | | n | prefijo |
|--:|---|---|--:|---|
| 76 | `envipe` | | 14 | `eder` |
| 48 | `mociba` | | 11 | `enoen` |
| 46 | `engasto` | | 10 | `f` |
| 41 | `endireh` | | 10 | `enaproce` |
| 37 | `encig` | | 8 | `cpv` |
| 27 | `ennvih` | | 7 | `wb` |
| 25 | `enoe` | | 6 | `enigh` / `endutih` / `encup` / `enasem` / `descargamasiva` / `conf` |
| 22 | `enif` | | 5 | `inegi` |
| 16 | `enut` / `banxico` | | 4 | `enadid` / `nse` |
| 15 | `enestyc` | | ≤3 | 33 prefijos más (`latinobarometro`, `elcos`, `enasic`, `encuci`, `enpol`, `enti`, …) |

Las siete que el encargo citaba (`mociba` 48 · `engasto` 46 · `endireh` 41 · `enut` 16 · `banxico` 16 · `enestyc` 15 · `eder` 14) **coinciden dígito por dígito** con esta rederivación — es la validación externa más fuerte de que la metodología (unión exacta, sin subcadena) reproduce lo mismo que ya se había visto antes. Pero el encargo no mencionaba los bloques más grandes de todos: `envipe` (76), `encig` (37), `ennvih` (27), `enoe` (25) y `enif` (22) superan a varios de los siete citados — su lista era ilustrativa, no exhaustiva, y esta nota la completa. Las cinco fichas `ensanut2024` de cuestionarios etiquetados (`1_vfinal_cuestionario_hogar_ensanut_2024…` a `5_vfinal_...utilizadores...`) no caen bajo ningún prefijo alfabético porque su id empieza con un dígito — quedan fuera de la tabla mecánica de arriba como 5 entradas de conteo 1 cada una; se nombran aquí a mano para que no se pierdan por un artefacto del regex de agrupación. Ningún bloque recibe canónico ni demanda inventada aquí — son un hecho del corpus, no un defecto, y quedan nombrados y sin tocar (§5).

### Estado de la suite — declarado en rojo, no maquillado

```
$ python3 tests/check.py --baseline
23 FAIL · 105 WARN
LÍNEA BASE: ROJO — 3 entradas nuevas frente a tests/baseline.json (HEAD congelado 948ad70343320b62f000d31fd39e2b2b68336ad9)
  · T02: nombre normalizado colisiona: forense/notas/2026-08-13-censo-explotacion.md · forense/encargos/2026-08-13-censo-explotacion.md
  · T16: canon/estado-programa-v1_10.md: declara 18 FAIL · 101 WARN vigente; la corrida real da 19 FAIL · 105 WARN
  · T16: canon/gobernanza-v1_15.md: declara 18 FAIL · 95 WARN vigente; la corrida real da 19 FAIL · 105 WARN
```

**No es VERDE, y se declara así en vez de maquillarlo.** Causa raíz única: §1 de este mismo encargo manda escribir `forense/notas/2026-08-13-censo-explotacion.md` **y** `forense/encargos/2026-08-13-censo-explotacion.md` — mismo nombre base, dos directorios distintos. `T02` (`tests/check.py`, `fail()`, no `warn()`) compara nombre normalizado sin distinguir directorio y no trae excepción para el par nota/encargo (su única lista de excepción, `EXCEPTED_PREFIXES`, cubre tres rutas de `data/curacion-registro/`, ninguna de `forense/`). Es mecánico, reproducible y consecuencia directa del perímetro tal como se declaró — no de cómo se ejecutó este acto. Precedente en el propio repo: el par equivalente más reciente (`forense/encargos/2026-08-13-A7-indice-infraestructura.md` / `forense/notas/2026-08-13-indice-infraestructura.md`) evitó la colisión dándole al encargo un nombre distinto (`A7-` de prefijo); **este encargo no lo hizo**, y este acto no tiene autoridad para renombrar fuera de lo que §1 declaró (`tests/` tampoco está en el perímetro para añadir una excepción ahí). Las dos entradas `T16` son eco mecánico de la primera: ambos documentos de `canon/` ya declaraban una cifra de FAIL/WARN desactualizada *antes* de este acto (la corrida pre-acto ya mostraba el mismo defecto de fondo, con otros números — ver ARRANQUE); al mover el total real de 18→19 FAIL, el mensaje de `T16` cambia de texto y deja de calzar con la entrada congelada en `tests/baseline.json`, aunque el defecto subyacente (esos dos canónicos desactualizados) no lo causó este acto. Ninguna de las tres entradas se corrige aquí: `canon/` y `tests/` están fuera del perímetro (§1). Se deja registrado también en `forense/hallazgos.md` para que quien numere el próximo `A.3` no repita el nombre.

**Actualización — resuelto tras confirmar con el usuario, no decidido unilateralmente.** PR #201 quedó `mergeable_state: blocked` por este único check requerido (`tests/check.py --baseline`, `conclusion: failure` — confirmado con los logs reales del job, sin otro bloqueo: 0 reviews, 0 comentarios, 0 hilos de revisión). Perímetro original (§1 de este mismo encargo) no daba autoridad para renombrar ni para tocar `tests/`; se preguntó al usuario entre dos vías (renombrar el archivo del encargo, o `--freeze` de la línea base) y eligió renombrar. Ejecutado: `forense/encargos/2026-08-13-censo-explotacion.md` → `forense/encargos/2026-08-13-A-censo-explotacion.md` (prefijo `A-`, mismo mecanismo que ya evitó la colisión en el par `A7-indice-infraestructura`/`indice-infraestructura` el mismo día). Reverificado tras el renombre:

```
$ python3 tests/check.py --baseline
22 FAIL · 105 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 948ad70343320b62f000d31fd39e2b2b68336ad9)
```

Confirma la hipótesis declarada arriba: las dos entradas `T16` eran eco puro del corrimiento de conteo que causaba `T02`, no defectos independientes — al quitar `T02`, el total real vuelve a `18 FAIL` y el mensaje de `T16` vuelve a calzar exactamente con el ya congelado en `tests/baseline.json`. Un solo mecanismo, tres síntomas, un solo commit para resolverlo. El texto arriba (el análisis en rojo) se deja intacto, sin reescribir, como registro de lo que pasó y por qué — esta es la corrección que le sigue, no un reemplazo silencioso.

## Cierre

1. Base: `origin/main` avanzó de `dcc4f6a` (declarado por el encargo) a `5f90757` durante el arranque (ACTO SONDA-1, PR #197) — no tocó ninguno de los cuatro artefactos que este censo mide, verificado con `git diff --stat`; no fue PARO.
2. Universo: 550 payloads con `archivo`+`sha256` en `data/manifiesto.yaml` (de 554 entradas totales) × 2 TSV de apertura vigentes (`abrir4-variables-2026-08-08.tsv`, `verif3-variables-2026-08-08.tsv`) × `relaciones.tsv` (197 filas, 43 con `id_manifiesto` resuelto, 8 ids distintos).
3. Cuatro estados, probados contra tres casos conocidos antes de correr el universo completo (Commit 1); receta congelada, sin ajuste posterior al ver el resultado completo (Commit 2).
4. Resultado: `EXPLOTADO` 4 · `ABIERTO-SIN-HALLAZGO` 4 · `REFERENCIADO-NO-ABIERTO` 4 · `SIN-DEMANDA` 538 — suman 550, verificado. Cuatro cifras de cierre entregadas con su comando, incluida la tensión §0/§4.1 sin resolver unilateralmente y la corrección de ≈321→538 en `SIN-DEMANDA`.
5. Suite: `python3 tests/check.py --baseline` cerró **ROJO, 23 FAIL · 105 WARN, 3 entradas nuevas** frente a `tests/baseline.json` (`948ad70`) al terminar Commit 2 — las tres, causadas mecánicamente por la colisión de nombre que el propio §1 del encargo introducía entre la nota y el encargo archivado. Bloqueaba el check requerido de PR #201. Confirmado con el usuario (no decidido unilateralmente): se renombró `forense/encargos/2026-08-13-censo-explotacion.md` → `forense/encargos/2026-08-13-A-censo-explotacion.md`, mismo mecanismo que ya evitó la colisión en `A7-indice-infraestructura` el mismo día. Reverificado tras el renombre: **VERDE, 22 FAIL · 105 WARN, nada nuevo** — las 2 entradas `T16` eran eco del mismo mecanismo, no defectos independientes, y se resolvieron con el mismo commit. T03: ninguna cita nueva de este acto apunta a un artefacto gitignorado.
6. Perímetro respetado con una desviación declarada y confirmada: solo se escribió `data/censo-explotacion-2026-08-13.tsv` (nuevo), esta nota, `forense/hallazgos.md` (append) y el encargo archivado (A.3) — bajo el nombre `forense/encargos/2026-08-13-A-censo-explotacion.md`, no el `forense/encargos/2026-08-13-censo-explotacion.md` que §1 pedía literalmente, por el renombre de (5). Cero bytes tocados en `data/manifiesto.yaml`, `data/curacion-registro/`, `data/inventarios/`, `canon/`, `milpa/`, `tools/`, `tests/`, ni en ninguna TSV preexistente.
7. Lo que este acto NO hizo (§5): no abrió ningún payload nuevo, no tocó `relaciones.tsv` ni el manifiesto, no propuso qué descargar, no clasificó ningún `SIN-DEMANDA` como sobrante. Contadores de medición sobre México movidos: **0** — este acto midió el propio programa, no midió a México.
8. **Entrada 4 de `forense/registro-recalculo-v1_0.md` cerrada por este mismo acto** (registro creado mientras este acto corría, por el sellado concurrente de ADR-72 — `origin/main` avanzó de `5f90757` a `c490a3a` durante la corrida; fusionado sin conflicto de contenido, único solape `forense/hallazgos.md`, `merge=union` como declara §1). Veredicto `RECALCULADO — SIN CAMBIO`: el contador que ADR-72 §2 instituyó (8/550=1.45%) se confirma exacto contra el universo ahora declarado completo — es la misma cifra que la Cifra 1b de este acto, no una coincidencia, es el mismo cálculo.
