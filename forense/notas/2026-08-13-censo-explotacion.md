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
