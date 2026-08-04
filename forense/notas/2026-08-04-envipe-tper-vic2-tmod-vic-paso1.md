# ENVIPE, agotar la fuente — `TPer_Vic2` y `TMod_Vic`: ¿traen reactivo de `exposicion_violencia`?

Contadores movidos: 0

Sin módulo de auditoría — no afirma nada sobre México (v2.3)

*4 de agosto de 2026.*

**Resultado de este acto, dicho antes que nada: CANDIDATO VÁLIDO.**
`TPer_Vic2`, Sección VII (Victimización personal), trae seis variables —
`AP7_3_09` a `AP7_3_14` — que preguntan directamente a la persona
seleccionada si sufrió, durante 2024, un hecho específico de violencia
(amenaza, agresión física con lesión, secuestro, agresión sexual,
violación), **sobre el universo completo de la tabla** (persona
seleccionada 18+, sin condicionar a `RESUL_H`, sin blanco en ninguna
fila). `TMod_Vic` — la otra tabla de este acto — se recorrió completa y
**no sirve**: es la subpoblación de víctimas por construcción, el mismo
defecto de denominador que `PR #57` encontró en `BP1_20`/`BP1_23`/`BP1_28`.
Este acto no mide nada, no adjudica, no decide CP-1: enumera candidatas,
resuelve C3 variable por variable, y deja C2 acotado con lo verificado.

---

## 0 · Verificación de entorno (protocolo §0, antes del diseño)

```
$ python3 tests/bitacora.py --abre
HEAD:  53bdd3a34dcec24ad4f396df88823a70945fba4e  ==  origin/main  (sin divergencia)
check.py --baseline:        exit=0 · LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
validador_registro_ids.py:  exit=0 · OK — 49 reglas, 27 en perímetro, 49 IDs verificados
Versión de instrucciones vigente: v2.3

$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable

$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200

$ ls data/raw | wc -l
0   -- AUSENTE, no PARO (checkout nuevo, data/raw es symlink local no versionado)
```

`data/raw` reportó ausente en el primer chequeo: este es un checkout
**nuevo** (worktree creado para este acto, distinto del de `PR #74` y
distinto del que corre el Encargo F en paralelo), y `data/raw` es un
symlink local (`.gitignore: data/raw/`) que cada checkout arma por
separado — la trampa que el protocolo §0 anticipa. Se enlazó a la raíz
externa ya integrada al resto de la organización de trabajo (ruta real no
citada aquí, por disciplina de §0):

```
$ ln -s <raíz externa> data/raw
$ ls data/raw | wc -l
133
```

Sin `cloud_default` en la variable de entorno; INEGI responde `200`.
**Entorno correcto para este acto, confirmado antes de leer nada.**

Rama nueva desde `origin/main` (`git fetch` + verificación):
`sesion/cal-conf-faseb-pos4-envipe-tpervic2-tmodvic-paso1`, worktree
separado del checkout de `PR #74` y del checkout del Encargo F —
`53bdd3a`, exactamente el merge de `PR #74` a `main`, el base que el
encargo pide ("`main` = `53bdd3a` o posterior"; verificado
`git merge-base --is-ancestor 53bdd3a origin/main` → sí, y
`origin/main` == `53bdd3a`, sin commits posteriores al momento de abrir
este acto).

## 1 · Premisas (§1 del encargo), verificadas contra HEAD

| # | Verificación | Resultado |
|---|---|---|
| PG-1 | `forense/notas/2026-08-04-cal-conf-faseb-pos4-envipe-paso1.md` §4 y §12 | Confirmado: el FD localiza **seis** tablas (`grep -n "Tabla T" fd.txt` → `TVivienda:314`, `THogar:549`, `TSDem:659`, `TPer_Vic1:858`, `TPer_Vic2:2885`, `TMod_Vic:4417`); `TPer_Vic2` (149 variables, columnas del CSV verificadas = 149) y `TMod_Vic` (137 variables, columnas del CSV verificadas = 137) no se abrieron en `PR #74` — su propio §11 lo declara: *"No se leyeron `TMod_Vic`, `TPer_Vic2` ni las Secciones VI/VII"* |
| PG-2 | misma nota, §10 | Confirmado: *"LA FUENTE NO TIENE EL DATO. Descriptor recorrido completo de `TPer_Vic1`... no se adjudicó nada"* — el veredicto es sobre `TPer_Vic1`, nombrado explícitamente en el título de la nota y en cada sección |
| PG-3 | `forense/hallazgos.md` (entrada 04/ago/2026, línea 72) + `hitoE §15` | Confirmado en ambos: *"`TMod_Vic` es la subpoblación de víctimas (`RESUL_H='A'` en el 100% de 40 280 filas)"*. Re-verificado independientemente contra el CSV de esta sesión: `conjunto_de_datos_tmod_vic_envipe2025.csv` → **40 280 filas, `RESUL_H` = 'A' en el 100%** (conteo exacto, sin excepción) |
| PG-4 | `PR #74` §6; re-derivado con `grep -in envipe forense/notas/2026-07-31-inventario-segmentacion.md` | Confirmado: ENVIPE es una de las 8 fuentes de Tabla B (línea 4); usada en varias filas, incluida la explícita `civico.denuncia.sin_seguro`/`con_seguro` ← `BP1_20`+`BP1_23`+`BP2_1`+`BP1_28` (línea 353) |
| PG-5 | `data/manifiesto.yaml`, parseado | Confirmado: `grep -c "^- id: envipe" data/manifiesto.yaml` → **32** ids, series 2018-2025 (fd/cuest_principal/cuest_modulo/csv × 8 años = 32) |
| PG-6 | `canon/gobernanza-v1_15.md`, ADR-52 A (línea 634, y línea 525 ss.) | Confirmado: ADR-52 A cuenta `PR #61` + su reemisión como **un** acto hacia la caducidad de tres; `PR #74` (el de `TPer_Vic1`) es el segundo acto examinado con argumento. La caducidad de tres actos "queda intacta" como criterio — decisión de mesa, no de este acto (línea 561, mismo lenguaje reusado en ADR-54) |

Las seis premisas (1) se sostienen. Se procede.

## 2 · El criterio, heredado literal de `PR #74`

*Exposición a violencia sufrida por la persona (antecedente), en cualquier
periodo de referencia, condicionada al vector de atributos observables de
`canon` §1.1.A — distinta de percepción o actitud sobre inseguridad, y
distinta de conducta posterior a la victimización (denuncia, búsqueda de
ayuda, medidas defensivas).*

Mismas tres distinciones que `PR #74` §2, sin reescribir:

1. **Exposición a violencia** (lo que se busca) → **SIRVE si aparece**.
2. **Denuncia o conducta posterior a la victimización** → **NO SIRVE si aparece**.
3. **Percepción/actitud de inseguridad** → **NO SIRVE si aparece**.

Distinción adicional que este acto necesita y `PR #74` no (porque
`TPer_Vic1` no tenía delito patrimonial): **(4) delito patrimonial/fraude
sin componente de violencia** (robo simple, fraude bancario, fraude al
consumidor) → tampoco es exposición a violencia, no por percepción ni por
conducta posterior, sino porque el hecho mismo no es un acto de
violencia. Se declara antes de mirar el descriptor, para no forzarla
después.

## 3 · Insumos y verificación de payload

```
$ sha256sum data/raw/fd_envipe2025.pdf
83fe02467b661d64e8638d882b242b0e534b8383e683a3fcbeadd66ead777fad  -- COINCIDE con data/manifiesto.yaml:1756

$ sha256sum data/raw/cuest_principal_envipe2025.pdf
a3e08bd496cefd75b17265828a4a9edade0ddbac467a4d71363488d13a8f7228  -- COINCIDE con data/manifiesto.yaml:1769

$ sha256sum data/raw/cuest_modulo_envipe2025.pdf
21df38610b21c481382dfb05cf8061e87216d97557c665b2e6e50aacaa216d27  -- COINCIDE con data/manifiesto.yaml:1782
```

Los tres ya estaban registrados en `data/manifiesto.yaml` (`:1750`,
`:1763`, `:1776`) y en disco; los tres sha256 coinciden — ninguna
condición de PARO por hash se activó. `cuest_modulo_envipe2025.pdf`
**se abre en este acto** — es el insumo que `PR #74` dejó explícitamente
sin abrir (su §11), y aquí entra porque `TMod_Vic` es la tabla del
módulo.

`pdftotext -layout` sobre los tres (herramienta del sistema): `fd.txt` →
7 207 líneas (idéntico a lo que reportó `PR #74`, mismo archivo, mismo
hash); `cuest_principal.txt` → 987 líneas (idéntico); `cuest_modulo.txt`
→ 597 líneas (nuevo para este acto).

**Además**, este acto abrió `envipe2025_csv.zip` (registrado en
manifiesto, no descargado de nuevo) — no para medir, sino para el
chequeo de denominador que el encargo pide en §2.1 (filas totales, filas
con valor válido): eso es estructura de la tabla, no una estimación
poblacional. Se declara en la sección de contaminación (§9) igual que si
fuera lectura de estructura, conservador.

## 4 · Localización de las tablas dentro del FD

```
$ grep -n "Tabla T" fd.txt
314   Tabla TVivienda
549   Tabla THogar
659   Tabla TSDem
858   Tabla TPer_Vic1
2885  Tabla TPer_Vic2      <- 149 variables, llave UPM+VIV_SEL+HOGAR+R_SEL (fd.txt:279) -- MISMA llave que TPer_Vic1
4417  Tabla TMod_Vic       <- 137 variables, llave UPM+VIV_SEL+HOGAR+R_SEL+BPCOD+ND_TIPO (fd.txt:295) -- llave por delito, no por persona
```

`TPer_Vic2` (`fd.txt:2885-4416`) se divide en dos secciones:
**Sección VI. Victimización en el hogar** (`fd.txt:3002-4110`, variables
`AP6_*`, unidad de análisis el hogar — *"algún(a) integrante de este
hogar incluido(a) usted"*, `cuest_principal.txt:715-928`, tarjeta
"grupo A"/"grupo B") y **Sección VII. Victimización personal**
(`fd.txt:4111-4416`, variables `AP7_*`, unidad de análisis la persona
seleccionada directamente — *"identificaremos si usted ha sufrido en su
persona"*, `cuest_principal.txt:930`, CC8).

`TMod_Vic` (`fd.txt:4417-7207`) no tiene encabezados de "Sección": es el
Instrumento B (`cuest_modulo.txt:28`), aplicado condicionalmente —
*"SI HAY REGISTRO DE ALGÚN DELITO EN LAS PREGUNTAS 6.6 o 7.4, APLIQUE EL
MÓDULO SOBRE VICTIMIZACIÓN (INSTRUMENTO B)"* (`cuest_principal.txt:973`).
Gran parte de sus 2 790 líneas de FD son catálogos geográficos (entidad/
municipio/localidad de ocurrencia) sin relación con el criterio; el
contenido sustantivo (variables `BP1_*` a `BP7_*`, catálogo de delito
`BPCOD:01-15`) se localizó por `grep` dirigido sobre el archivo completo
y se leyó íntegro el bloque `BP1_1`-`BP1_28` (`fd.txt:4437-5152`), que es
donde vive tanto el reactivo ya retirado (`BP1_20`/`23`/`28`,
`fd.txt:5049-5152`, confirmando la cita de `PR #74`) como el único otro
contenido de violencia de la tabla (`BP1_15`-`BP1_19`, armas y lesión
física, ver §6).

## 5 · Candidatas por descriptor literal

### 5.1 · `TPer_Vic2`, Sección VII (universo: persona seleccionada, sin condicionar — ver §7)

| Variable | Pregunta (wording literal) | Catálogo | Distinción |
|---|---|---|---|
| `AP7_1` (`fd.txt:4118`) | *"Antes de 2024, ¿usted sufrió directamente alguna de las situaciones del grupo B?"* | 1 Sí / 2 No / 9 NS-NR | **Agregado impuro** — "grupo B" mezcla 11 códigos, de los cuales 5 son delito patrimonial/fraude sin violencia (distinción 4) y 6 son violencia (distinción 1). Un solo ítem no puede aislar el constructo. **NO SIRVE tal cual** — la variable existe, pero no separa lo que el criterio exige separado |
| `AP7_2` (`fd.txt:4125`) | *"En lo que va del 2025, ¿usted ha sufrido directamente alguna de las situaciones del grupo B?"* | 1 Sí / 2 No / 9 NS-NR | Mismo defecto que `AP7_1`, otro periodo de referencia. **NO SIRVE tal cual** |
| `AP7_3_05` (`fd.txt:4136`) | *"Robo o asalto en la calle o en el transporte público (incluye robo en banco o cajero automático)"* | 1 Sí / 2 No / 9 NS-NR | **(4) Delito patrimonial** — robo, sin verbo de violencia en el wording (el robo puede o no involucrar confrontación; el ítem no lo distingue). **NO SIRVE** |
| `AP7_3_06` (`fd.txt:4152`) | *"Robo en forma distinta a la anterior"* (especifique) | 1 Sí / 2 No | **(4) Delito patrimonial**, catch-all de robo. **NO SIRVE** |
| `AP7_3_07` (`fd.txt:4164`) | *"Alguien usó su chequera, número de tarjeta o cuenta bancaria sin su permiso... (fraude bancario) o le dio dinero falso"* | 1 Sí / 2 No / 9 NS-NR | **(4) Fraude**, sin contacto ni violencia. **NO SIRVE** |
| `AP7_3_08` (`fd.txt:4189`) | *"Entregó dinero por un producto o servicio que no recibió... (fraude al consumidor)"* | 1 Sí / 2 No / 9 NS-NR | **(4) Fraude**. **NO SIRVE** |
| `AP7_3_09` (`fd.txt:4212`) | *"Amenazas, presiones o engaños para exigirle dinero o bienes; o para que hiciera algo o dejara de hacerlo (extorsión)"* | 1 Sí / 2 No / 9 NS-NR | **(1) Exposición a violencia — coerción por amenaza**, hecho consumado (le extorsionaron), no expectativa (compárese con `AP4_6` de `TPer_Vic1`, *"¿cree que le pueda ocurrir?"*, que sí es distinción 3). Mixto con motivo patrimonial (el fin es dinero/bienes), declarado, no resuelto por este acto cuál pesa más. **SIRVE, con matiz declarado** |
| `AP7_3_10` (`fd.txt:4229`) | *"Amenazas verbales o por escrito hacia su persona diciendo que le va a causar un daño a usted, a su familia, a sus bienes o su trabajo"* | 1 Sí / 2 No / 9 NS-NR | **(1) Exposición a violencia — amenaza directa**, hecho consumado (recibió la amenaza), no percepción de riesgo futuro. **SIRVE** |
| `AP7_3_11` (`fd.txt:4246`) | *"Alguien sólo por actitud abusiva o por una discusión lo (la) golpeó, empujó o atacó generándole una lesión física (moretones, fracturas, cortadas, etcétera)"* | 1 Sí / 2 No / 9 NS-NR | **(1) Exposición a violencia — agresión física consumada con lesión**. El más limpio de los seis: verbo de violencia física directa, resultado verificable (lesión). **SIRVE** |
| `AP7_3_12` (`fd.txt:4269`) | *"Lo (la) secuestraron para exigir dinero o bienes"* | 1 Sí / 2 No / 9 NS-NR | **(1) Exposición a violencia — secuestro personal consumado**. **SIRVE** |
| `AP7_3_13` (`fd.txt:4281`) | *"Alguien en contra de su voluntad lo (la) agredió mediante hostigamiento o intimidación sexual, manoseo, exhibicionismo o intento de violación"* | 1 Sí / 2 No / 9 NS-NR | **(1) Exposición a violencia — agresión sexual consumada**. **SIRVE** |
| `AP7_3_14` (`fd.txt:4306`) | *"Fue obligado(a) mediante violencia física o amenaza por alguien conocido o desconocido a tener una actividad sexual no deseada (violación sexual)"* | 1 Sí / 2 No / 9 NS-NR | **(1) Exposición a violencia — violación consumada**. **SIRVE** |
| `AP7_3_15` (`fd.txt:4326`) | *"Otros delitos distintos a los anteriores"* (especifique) | 1 Sí / 2 No | Catch-all sin wording propio — no clasificable sin ver la especificación textual (no capturada en el CSV estructurado). **NO SIRVE tal cual, sin verificar** |
| `AP7_4_09`…`AP7_4_14` (`fd.txt:4212-4326`, siguiendo a cada `AP7_3_XX`) | *"¿Me podría decir cuántas veces sufrió...?"* | 01-99 / blanco si `AP7_3_XX`≠1 | Frecuencia del mismo hecho — no agrega distinción nueva, hereda la de su `AP7_3_XX`. Útil para intensidad, no para el binario de exposición. Declarado, no evaluado variable por variable |

**Búsqueda dirigida adicional** (`grep -i` sobre las 1 533 líneas de
`TPer_Vic2`): `presenci|testig|escuch|conoce a alguien|algún familiar`
— sin resultados nuevos fuera de lo ya catalogado. Sección VI
(household, `AP6_*`, ~107 variables: robo de vehículo, secuestro,
desaparición, homicidio de integrantes del hogar) **no se itemiza
variable por variable** — se descarta en bloque por construcción: su
propio wording (*"algún(a) integrante de este hogar incluido(a)
usted"*, `cuest_principal.txt:718-724`) mezcla al respondente con otros
integrantes del hogar sin distinguir cuál de los dos sufrió el hecho, lo
que rompe el vínculo evento↔atributos-de-la-persona que el criterio exige
(`canon` §1.1.A es un vector de atributos de la persona, no del hogar).
**NO SIRVE, por construcción, sin candidata individual**.

### 5.2 · `TMod_Vic` (universo: subpoblación de víctimas — ver §7, denominador ya viciado)

| Variable | Pregunta (wording literal) | Catálogo | Distinción |
|---|---|---|---|
| `BP1_15` (`fd.txt:4956`) | *"¿Llevaba(n) arma(s) el (los) delincuente(s)?"* | 1 Sí / 2 No / 9 NS-NR / blanco | Describiría exposición a arma, pero el denominador ya es "ya víctima de un delito confrontacional" (ver §7). **NO SIRVE para `exposicion_violencia` poblacional** — podría servir para severidad condicional, no adjudicado aquí |
| `BP1_16_1`-`BP1_16_4`/`_9` (`fd.txt:4959-4980`) | *"¿Qué tipo de arma(s) llevaba(n)?"* (fuego/blanca/contundente/otro) | 0/1/blanco | Mismo defecto de denominador que `BP1_15`. **NO SIRVE** |
| `BP1_17` (`fd.txt:4991`) | *"¿Le causaron alguna lesión física con el arma (heridas)?"* | 1 Sí / 2 No / 9 NS-NR / blanco | Mismo defecto — condicionado además a `BP1_15`=1 (portaba arma). **NO SIRVE** |
| `BP1_18` (`fd.txt:4997`) | *"¿Utilizaron otro tipo de violencia física?"* | 1 Sí / 2 No / 9 NS-NR / blanco | Wording más cercano al criterio de toda la tabla, pero mismo defecto de denominador (ver §7, n disponible = 15 399 de 40 280, ya condicionado). **NO SIRVE poblacionalmente** |
| `BP1_19_1`-`_8` (`fd.txt:5010-5043`) | *"¿Qué tipo de lesión física sufrió?"* (moretones/cortadas/dislocaciones/fracturas/quemaduras/pérdida de conocimiento/bala/otro) | 0/1/blanco | Detalle de severidad, mismo defecto. **NO SIRVE poblacionalmente** — el catálogo más rico de tipo de lesión de todo ENVIPE, útil si algún día se mide severidad condicional a victimización, no exposición |
| `BP1_20`-`BP1_28` (`fd.txt:5049-5152`) | Ya cubiertas por `PR #57`/hitoE §15 | — | **(2) Conducta posterior a la victimización** — mismo veredicto ya sellado, no se reabre aquí |

**Búsqueda dirigida** (`grep -i` sobre las 2 790 líneas de `TMod_Vic`):
`violenci|arma de fuego|golpe|lesion|agres|amenaz` — únicos resultados:
el catálogo `BPCOD` (códigos 09-14, ya cubiertos vía `TPer_Vic2` porque
son la misma tipología de delito, ver §7), el bloque `BP1_15`-`BP1_19`
de la tabla de arriba, y `"agresor(a)"` dentro de `BP1_23` (ya cerrado).
**No hay contenido de violencia en `TMod_Vic` fuera de lo catalogado.**
Resto del archivo (`BP2_*` a `BP7_*`, no leídos variable por variable):
por nombre en el catálogo de microdato (`envipe2025_csv.zip`), cubren
valor del bien robado/asegurado, efectos económicos, seguimiento del
proceso de denuncia y percepción de la autoridad que atendió — ninguno
sugiere contenido de violencia distinto por su nombre; no se abrieron sus
wordings en el FD (fuera del perímetro de la búsqueda dirigida, que sí
cubrió el archivo completo por patrón de texto).

## 6 · Chequeo de denominador (§2.1 del encargo — el que decide)

| Tabla | Filas totales | `RESUL_H` | ¿Universo poblacional? |
|---|---|---|---|
| `TPer_Vic1` (referencia, `PR #74`) | 91 182 | A: — / B: — (no re-derivado aquí, mismo archivo de personas) | Sí — persona seleccionada, ya establecido por `PR #74` |
| `TPer_Vic2` | **91 182** | **A (con victimización): 22 295 · B (sin victimización): 68 887** — ambos códigos presentes, en la misma proporción que el universo general de personas seleccionadas | **Sí.** Mismo `n` que `TPer_Vic1` (verificado: ambos CSV tienen exactamente 91 182 filas, misma llave `UPM+VIV_SEL+HOGAR+R_SEL`) — es la tabla de **toda** persona seleccionada de 18+, no la de víctimas |
| `TMod_Vic` | **40 280** | **A (con victimización): 40 280 — 100%** | **No.** Confirma `PG-3`: el denominador ya excluyó a quien no fue víctima. Llave `UPM+VIV_SEL+HOGAR+R_SEL+BPCOD+ND_TIPO` — **filas ≠ personas**: una persona con dos delitos distintos aporta dos filas. El propio disparador del instrumento (`cuest_principal.txt:973`, *"SI HAY REGISTRO DE ALGÚN DELITO... APLIQUE EL MÓDULO"*) es la definición operativa de "ya víctima" |

**`n` válido por candidata de `TPer_Vic2` (Sección VII), sobre el universo completo de 91 182 filas, sin excepción de blanco:**

| Variable | 1 (Sí) | 2 (No) | 9 (NS-NR) | Blanco | Total |
|---|---|---|---|---|---|
| `AP7_1` | 19 494 | 71 639 | 49 | 0 | 91 182 |
| `AP7_2` | 6 096 | 85 020 | 66 | 0 | 91 182 |
| `AP7_3_09` | 4 292 | 86 879 | 11 | 0 | 91 182 |
| `AP7_3_10` | 3 099 | 88 073 | 10 | 0 | 91 182 |
| `AP7_3_11` | 1 092 | 90 080 | 10 | 0 | 91 182 |
| `AP7_3_12` | 72 | 91 101 | 9 | 0 | 91 182 |
| `AP7_3_13` | 1 112 | 90 056 | 14 | 0 | 91 182 |
| `AP7_3_14` | 108 | 91 056 | 18 | 0 | 91 182 |

Cero blancos en las ocho variables — cada una de las 91 182 filas tiene
respuesta válida (1/2/9). Esto es lo que el §2.1 del encargo exige
verificar antes de nada más: **el universo permite reconstruir la
población completa**, no solo el subgrupo de víctimas. Esta cifra se
obtuvo abriendo `envipe2025_csv.zip` (ya registrado en manifiesto) y
contando filas/valores — verificación estructural, no una estimación
poblacional; **este acto no mide** `exposicion_violencia` (eso es
protocolo §4.1, sesión de medición aparte).

**`n` disponible en `TMod_Vic`, mismas variables candidatas (contraste,
para que quede escrito por qué NO SIRVE):**

| Variable | 1 (Sí) | 2 (No) | 9 (NS-NR) | Blanco | Total |
|---|---|---|---|---|---|
| `BP1_15` | 4 414 | 8 446 | 2 915 | 24 505 | 40 280 |
| `BP1_17` | 376 | 4 034 | 4 | 35 866 | 40 280 |
| `BP1_18` | 2 479 | 12 614 | 306 | 24 881 | 40 280 |

Doble condicionamiento: primero a ser víctima (denominador de la tabla,
40 280 de 91 182 personas), después a que el delito fuera de un subtipo
confrontacional (`BP1_15` ya trae 24 505 blancos sobre ese denominador
reducido). Exactamente el patrón que el encargo anticipa en §2.1: *"una
variable que solo exista dentro del subgrupo de víctimas se reporta como
NO SIRVE... por buena que se vea su wording."* `BP1_18` es, por wording,
la más cercana al criterio de toda la tabla — y es la que mejor ilustra
el defecto: no sirve por lo que dice, sirve por a quién se le pregunta.

## 7 · Chequeo C3 (circularidad contra Tabla B), variable por variable

```
$ grep -in "AP7_1\b\|AP7_2\b\|AP7_3_09\|AP7_3_10\|AP7_3_11\|AP7_3_12\|AP7_3_13\|AP7_3_14\|BP1_15\|BP1_17\|BP1_18\|BP1_19" forense/notas/2026-07-31-inventario-segmentacion.md
(sin resultados)
```

Ninguna de las ocho candidatas de §6 aparece en las 41 filas de Tabla B.
Los únicos hits de ENVIPE en ese archivo son (ya conocidos, ninguno
nuevo): `AP3_8`/`AP3_10` (línea 47, eje 1), `EDAD` (línea 60), `DOMINIO`
(línea 73), `ESTRATO` (línea 86), `AP4_9_1..6` (línea 246),
`AP5_2_1..4` (línea 262), `BP1_23` (línea 299, ya retirado como reactivo
de `exposicion_violencia`, cerrado por `PR #57`) y el bloque
`BP1_20`+`BP1_23`+`BP2_1`+`BP1_28` (línea 353, reactivo de
`civico.denuncia.sin_seguro`/`con_seguro`, también ya retirado).
**C3 pasa limpio para las ocho candidatas de este acto — ninguna
alimenta Tabla B, resuelto variable por variable, no en bloque.**

Nota de higiene, no de circularidad: `inventario-segmentacion.md:357`
cita `AP7_3_5/6`/`AP7_4_5/6` como candidato de `civico.protesta.
agravio_urbano` — son variables de **ENCUCI**, no de ENVIPE; coinciden en
mnemónico por azar de numeración de sección entre encuestas distintas.
Verificado para que una lectura futura no las confunda con las
`AP7_3_XX` de este acto.

## 8 · Chequeo C2 (mismo instrumento observa desenlaces de `G4`)

Los tres desenlaces de `G4` (`canon/modelo-decision-v4_0.md`):
`civico.protesta.agravio_urbano` (`:490`),
`civico.autodefensa.agravio_rural` (`:491`),
`comunicacion.inseguridad.ver_oir_callar` (`:517`).

```
$ grep -in "protesta|autodefensa|linchamiento|justicia por propia mano|ronda|guardia comunitaria|manifestaci|marcha|bloqueo" fd.txt[2885:4417] fd.txt[4417:7207] cuest_modulo.txt
(sin resultados en ninguno de los tres)
```

**Extiende el hallazgo de `PR #74`** (que solo cubrió `TPer_Vic1`): ningún
wording literal de los tres desenlaces vive tampoco en `TPer_Vic2` ni en
`TMod_Vic`, ni en el cuestionario de módulo. Con esto, las tres tablas
sustantivas de ENVIPE 2025 abiertas hasta ahora (`TPer_Vic1` por
`PR #74`, `TPer_Vic2`/`TMod_Vic` por este acto) están libres de wording
literal para `G4`.

**No cierra C2 — declarado ABIERTO Y ACOTADO, con un riesgo concreto que
`PR #74` §7 anticipó y que este acto confirma que se materializa:**
`BP1_23` (*"¿Cuál fue la razón principal por la que no denunció...?"*,
`TMod_Vic`) sigue señalado en `hitoE §15` como candidato **Parcial** para
`comunicacion.inseguridad.ver_oir_callar` (el tercer desenlace de `G4`).
`BP1_23` solo se pregunta a quien ya contestó `BP1_20`=No (no denunció),
que a su vez solo se pregunta a quien ya disparó el Instrumento B
(`cuest_principal.txt:973`) — es decir, a quien ya contestó `AP7_3_XX`=1
o `AP6_6`=1 en `TPer_Vic2`. **Si `exposicion_violencia` se terminara
midiendo con `AP7_3_09`-`_14` (este acto) y `comunicacion.inseguridad.
ver_oir_callar` se terminara operacionalizando con `BP1_23` (`hitoE
§15`), las dos variables no serían independientes por diseño del
instrumento: la segunda solo existe para la subpoblación que ya
respondió afirmativamente a una de las primeras.** No es coincidencia de
contenido (C3, que pasó limpio) — es dependencia estructural de
aplicación dentro del mismo cuestionario. Se declara para que la sesión
que adjudique cualquiera de las dos variables lo resuelva explícitamente;
este acto no lo resuelve ni lo puede resolver sin adjudicar, que tiene
prohibido.

`AP4_10`/`AP4_11` (`TPer_Vic1`, conducta defensiva/evitación, el riesgo
original que `PR #74` señaló) siguen sin wording de los tres desenlaces
— mismo hallazgo que antes, no cambia con este acto.

## 9 · Ejes de atributos disponibles (`canon` §1.1.A)

`TPer_Vic2` comparte llave (`UPM+VIV_SEL+HOGAR+R_SEL`) y `n` (91 182)
exactos con `TPer_Vic1` — verificado, no asumido (§6). Trae copia propia
de `SEXO` (cons. 9) y `EDAD` (cons. 10) dentro de la tabla, y
`DOMINIO`/`ESTRATO` en el bloque de diseño muestral (cons. 146-147,
`fd.txt:1504-1518`) — los mismos ejes que `PR #74` derivó para
`TPer_Vic1`, disponibles sin `join` adicional salvo `AP3_8`/`AP3_10`
(formalidad laboral), que vive en `TSDem` y requiere unir por la llave
compartida, igual que en `TPer_Vic1`. **No re-derivado desde cero —
heredado por identidad de llave y de `n`, verificado, no citado a
ciegas:**

| Eje (canon §1.1.A) | ¿Disponible en `TPer_Vic2`? |
|---|---|
| 1. Formalidad laboral | Parcial — vía `join` a `TSDem` (`AP3_8`/`AP3_10`), mismo límite que `TPer_Vic1` |
| 2. Edad | Sí — `EDAD` nativa en la tabla |
| 3. Urbanización | Sí — `DOMINIO` nativa en el bloque de diseño |
| 4. Ingreso | Parcial — `ESTRATO` de área, no ingreso declarado, mismo límite que `TPer_Vic1` |
| 5. Acceso digital | No — mismo límite que `TPer_Vic1` (no re-verificado variable por variable en `TPer_Vic2`, heredado) |
| 6. Condición migratoria | No — mismo límite que `TPer_Vic1` (heredado, no re-verificado) |

`TMod_Vic` no aplica (candidatas de esa tabla ya descartadas por
denominador, §6) — sus ejes de atributos serían los mismos de
`TPer_Vic2` vía la llave compartida, pero sobre el subconjunto de 40 280
filas, irrelevante dado el veredicto de §6.

## 10 · Declaración de contaminación (ADR-46)

**Este acto abrió:** `fd_envipe2025.pdf` completo vía `pdftotext`
(lectura íntegra de `TPer_Vic2` — Secciones VI y VII — y lectura dirigida
más lectura íntegra del bloque `BP1_1`-`BP1_28` de `TMod_Vic`, más
búsqueda dirigida por patrón sobre el texto completo de ambas tablas);
`cuest_principal_envipe2025.pdf` (relectura de las secciones VI-VII, ya
abierto antes por `PR #74` para Sección IV-V); `cuest_modulo_envipe2025.
pdf` completo, **primera apertura registrada de este insumo**. También se
abrió `envipe2025_csv.zip` (estructura: conteo de filas y de valores por
variable en `TPer_Vic2` y `TMod_Vic` — no estimación poblacional).

**Esta sesión y esta máquina, mientras retengan este contexto, quedan
inhabilitadas para pre-registrar contra ENVIPE** (ADR-46, unidad =
sesión) — la misma inhabilitación que `PR #74` ya declaró para sí misma,
ahora también cubriendo estructura/contenido de `TPer_Vic2`, `TMod_Vic`
y microdato estructural (no sustantivo) de ambas. Sigue pudiendo medir y
seguir el descriptor — la restricción es sobre pre-registro, no sobre
trabajo con la fuente.

## 11 · Veredicto (vocabulario §3 del encargo)

**CANDIDATO VÁLIDO.**

Seis variables de `TPer_Vic2` — `AP7_3_09`, `AP7_3_10`, `AP7_3_11`,
`AP7_3_12`, `AP7_3_13`, `AP7_3_14` — cumplen el criterio de §2 con
universo poblacional completo (persona seleccionada 18+, `n`=91 182, sin
condicionar a `RESUL_H`, cero blancos), C3 limpio variable por variable
(§7), y C2 declarado abierto y acotado con un riesgo estructural concreto
identificado, no solo señalado (§8). `AP7_3_11` (agresión física con
lesión) y `AP7_3_14` (violación sexual mediante violencia o amenaza) son
las más limpias contra el criterio — verbo de violencia directa, hecho
consumado, sin mezcla patrimonial; `AP7_3_09` y `AP7_3_10` cargan un
componente de coerción/amenaza con fin económico parcial, declarado, no
resuelto por este acto. `TMod_Vic`, la otra tabla del acto, se recorrió
completa y **no sirve**: mismo defecto de denominador que retiró
`BP1_20`/`23`/`28` (§6). `AP7_1`/`AP7_2` (agregados) y `AP7_3_05`-`_08`/
`_15` (patrimonial/fraude) tampoco sirven, con argumento por cada uno
(§5.1).

**Consecuencia, dicha con las palabras del encargo, sin adjudicarla:**
ENVIPE recupera la vía poblacional para `exposicion_violencia`; con esto
manda sobre ENDIREH (que en su paso 1, `PR #67`, encontró candidato
parcial en universo mujeres 15+, más estrecho que el universo aquí
verificado); CP-1 se re-plantea en mesa. No se mide, no se adjudica, no
se decide aquí — es exactamente lo que el protocolo §4.1 reserva a otra
sesión.

**Con este acto, las seis tablas del FD de ENVIPE 2025 quedan cubiertas**
entre `PR #74` (`TPer_Vic1`) y este (`TPer_Vic2`, `TMod_Vic`) — `TVivienda`,
`THogar`, `TSDem` no se abrieron en ninguno de los dos actos porque
ninguna premisa (1) de ninguno de los dos las señaló como candidatas de
victimización; quedan fuera del perímetro declarado de la búsqueda de
`exposicion_violencia`, no del catálogo general de ENVIPE.

## 12 · Nota para mesa, declarada y no decidida por este acto

ENVIPE 2025 es la octava ola de una serie 2018-2025, cada año con FD y
cuestionarios propios ya registrados en el manifiesto (32 ids, PG-5). Si
mesa adjudica alguna de las seis candidatas de §11 como reactivo de
`exposicion_violencia`, eso abre la puerta a una **serie repetida de
corte transversal de ocho olas**, no un dato de un solo año — y el
programa tiene 15 coeficientes de ritmo en cero, sin vía viva desde que
se retiró `unico_calibrable_hoy` y desde que el Encargo E encontró que la
premisa del pseudo-panel vía ENOE/ENNViH no se sostiene contra la cita
que la respaldaba. No se explora aquí y no se pre-registra nada contra
esa posibilidad — se anota una línea, para que mesa la tenga presente al
decidir sobre §11. Un candidato con ocho olas vale distinto que uno con
una.

## 13 · Qué NO se hizo

- No se midió nada — ni proporciones, ni el coeficiente `G4`.
- No se adjudicó CP-1.
- No se decidió si este acto cuenta hacia la caducidad de ADR-52 A (es
  mesa quien decide si un CANDIDATO VÁLIDO cuenta igual que un NO SIRVE
  argumentado para ese conteo — ni siquiera está claro que aplique,
  dado que la caducidad de tres está pensada para búsquedas que
  terminan en NO SIRVE, no en candidato).
- No se editó el cuerpo de `hitoE` — la adenda de esta nota vive en
  `hitoE §21` (append-only; renumerada desde `§20` al fusionar `main`
  por colisión de numeración concurrente con el Encargo F —
  `forense/hallazgos.md`, entrada de cierre de este acto), no en el
  cuerpo ni en `§14.3`/`§15`.
- No se tocó `canon/` ni `milpa/`.
- No se resolvió C2 — declarado abierto y acotado (§8), con el riesgo de
  `BP1_23` nombrado explícitamente, no fabricado ni cerrado.
- No se itemizaron las ~107 variables de Sección VI (`AP6_*`) ni el resto
  de `TMod_Vic` fuera del bloque `BP1_1`-`BP1_28` — descartadas en bloque
  con argumento de construcción (§5.1) o cubiertas por búsqueda dirigida
  sin contenido nuevo (§5.2), no leídas variable por variable.
- No se registró ninguna entrada nueva en `data/manifiesto.yaml` — los
  tres PDF de ENVIPE 2025 ya estaban registrados y verificados; el CSV
  (`envipe2025_csv.zip`) tampoco es entrada nueva, ya registrado.
- No se fusionó el PR de este acto.

## 14 · Límite de lectura declarado

Leído completo (`pdftotext -layout`): `data/raw/fd_envipe2025.pdf`,
`TPer_Vic2` íntegra (`fd.txt:2885-4416`, Secciones VI y VII); de
`TMod_Vic` (`fd.txt:4417-7207`) se leyó íntegro el bloque de
identificación/llave/`BPCOD`/`RESUL_H` (`fd.txt:4417-4560`) y el bloque
`BP1_1`-`BP1_28` (`fd.txt:4437-5152` aprox., confirmado contra la cita de
`PR #74`); el resto (catálogos geográficos, `BP2_*`-`BP7_*`) se cubrió
por búsqueda dirigida de patrón sobre el archivo completo, no por lectura
línea a línea. `data/raw/cuest_principal_envipe2025.pdf` completo
(987 líneas, ya había sido leído por `PR #74` para Secciones IV-V; este
acto releyó VI-VII). `data/raw/cuest_modulo_envipe2025.pdf` completo
(597 líneas) — primera apertura de este insumo en la búsqueda de
`exposicion_violencia`. `envipe2025_csv.zip`: se listó el índice completo
del zip y se contaron filas/valores de `conjunto_de_datos_tper_vic2_
envipe2025.csv` y `conjunto_de_datos_tmod_vic_envipe2025.csv` — no se
leyó ninguna otra tabla del microdato, ni se abrió el contenido de
`conjunto_de_datos_tper_vic1_envipe2025.csv` más allá de su conteo de
filas (91 182, para el contraste de §6). No se reabrió el contenido de
`TPer_Vic1` en el FD (secciones IV-V) — se citó `PR #74` sin releerlo.
Leído: `canon/modelo-decision-v4_0.md:225`, `:245`, `:251`, `:269`,
`:278`, `:394`, `:490-491`, `:517`, `:725` (mismas citas que `PR #74`,
re-verificadas contra HEAD, sin discrepancia nueva encontrada);
`canon/gobernanza-v1_15.md:525-567`, `:632-634` (ADR-52, ADR-53, ADR-54);
`forense/hitoE-campana-medicion-v2_0.md §15` completo (líneas
1203-1271); `forense/hallazgos.md` (entrada 04/ago/2026, líneas 58, 72);
`forense/notas/2026-07-31-inventario-segmentacion.md` (grep dirigido:
los ocho mnemónicos candidatos, no lectura completa de las 41 filas,
mismo criterio que `PR #74`). No abierto: `data/manifiesto-staging.yaml`,
`data/catalogo-fuentes-v1_0.md`. `python3 tests/check.py` corrido tras
la última edición de esta nota — resultado en §15.

## 15 · Suite, corrida tras la última edición

```
$ python3 tests/check.py
19 FAIL · 84 WARN
(idéntico al estado que PR #74 dejó en main — "Después: 19 FAIL · 84 WARN"
de su propio bloque de bitácora; esta nota no introdujo FAIL/WARN nuevos)

$ python3 tests/check.py --baseline
19 FAIL · 84 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
(HEAD congelado 090ee0f6b72f662d0361d205d4599d705d84dfd0)
```

VERDE. Ningún rojo nuevo que explicar.
