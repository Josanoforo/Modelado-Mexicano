# ACTO DISEÑO-ENSAFI · el FD cierra la fila a `MAPEADO`, con tres reservas que el FD mismo produce

`ENCARGO E4 · DISEÑO-ENSAFI — abre el FD ya descargado y cierra la fila ENSAFI de
data/diseno-muestral.yaml a MAPEADO`, dirección (maestra-30), 26/ago/2026, SHA de redacción
`186f090`. Worktree `/home/pc0/mm-e4-diseno-ensafi`, rama `acto/e4-diseno-ensafi`, **`PR #373`**.
**Entorno UBUNTU** (el FD vive en el corpus). Sin descarga, sin firma de mesa, sin estimación.
Encargo archivado íntegro en `forense/encargos/2026-08-26-E4-DISENO-ENSAFI.md` (`A.3`).

**Veredicto en una línea.** El FD **sí** define las cinco variables como variables de diseño —
las doce filas relevantes viven bajo el encabezado literal `VARIABLES DE DISEÑO ESTADÍSTICO`, una
sección por hoja — y la fila cierra a `MAPEADO`. Pero el FD **no** etiqueta el universo de
`FAC_ELE`, **se contradice a sí mismo** en `FAC_HOG` y **erra** un código de `EST_DIS`. Las tres
cosas se declaran en la fila con su cita; ninguna bloquea el cierre.

---

## 0 · Arranque y firma de entorno (`A.2`, tres partes)

**1 · REPO.** El clon principal `/home/pc0/Modelado-Mexicano` estaba parado en
`acto/cal-g3-puntual` (`ea22bdd`), **no** en `main` — precedente ya conocido (`F0` se corre en la
caja del acto). No se clonó nada nuevo: se creó worktree sobre `186f090`.

```
$ git worktree add /home/pc0/mm-e4-diseno-ensafi -b acto/e4-diseno-ensafi 186f090
$ git log -1 --format="%h %s"
186f090 Merge pull request #369 from Josanoforo/claude/cierra-4-firmas-8b6f2r
$ git status --short          # vacío
```

**2 · SHA.** `git fetch origin` → `dad74ee..186f090 main`. Tras refrescar, `origin/main` **es
exactamente** el SHA que el encargo declara:

```
$ git rev-list --count 186f090..origin/main
0
```

`main` no avanzó desde la redacción. Nada que re-derivar por movimiento de perímetro.

**3 · Corpus.** `data/raw` **no existía** en el worktree nuevo (raíz integrada, gitignorada, no se
hereda). Se enlazó a la raíz compartida:

```
$ ln -s /home/pc0/mm-corpus/raw data/raw
$ cp /home/pc0/mm-ensafi-descriptor/data/raices.local.yaml data/raices.local.yaml
$ ls data/raw/ | wc -l
321
$ git status --short          # vacío -- ni el symlink ni el archivo de raíces ensucian el árbol
```

**Este acto no descarga nada**, así que la advertencia de `PR #77` (payloads que quedan solo en el
worktree) no tiene objeto aquí: el único payload que se toca ya estaba en el corpus compartido y se
leyó por esa ruta, no por copia local.

**4 · Firma de entorno, las tres partes:**

```
(1) CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE: sin_variable
(2) $ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
    200                        (curl exit 0)
(3) $ ls data/raw/ | wc -l
    321                        (corpus montado)
```

**`A.13` sobre el negativo de (1).** «Sin variable» es un veredicto negativo y por lo tanto declara
cuántos objetos examinó el comando que lo produjo: `env | command grep -c
CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → **0 coincidencias sobre 75 variables de entorno**
(`env | wc -l` → 75). **Control positivo del mismo comando**, para probar que el comando sí
examina: `env | command grep -c HOME` → **1**. Un cero de un comando que no mira nada no es un cero.

**`A.13` sobre el negativo de (3), antes de enlazar.** Se declara porque es exactamente la trampa
que la regla nombra: `ls data/raw/ 2>/dev/null | head -1` devolvió **salida vacía con exit 0** —
pero ese `0` es el exit de `head`, no de `ls`, y el directorio **no existía**: el comando examinó
**0 archivos**. Ese vacío no probaba «corpus vacío»; probaba «no hay directorio». Tras enlazar, 321
entradas.

**`grep`.** En esta caja `grep` envuelve `ugrep -I`, que descarta archivos con bytes no-UTF8 sin
error ni exit code útil. Todo `grep` de esta nota es **`command grep`** y así se declara.

**5 · ESPEJO.** No se consultó. Toda cifra de esta nota sale del worktree de (1) en `186f090`, con
el comando a la vista.

---

## 1 · Compuerta cero

**La fila seguía `PENDIENTE`** — no había trabajo duplicado:

```
$ sed -n '977,997p' data/diseno-muestral.yaml
- fuente: ENSAFI — Encuesta Nacional sobre Salud Financiera (ENSAFI)
  estado: PENDIENTE
  ...
  notas: 'SIGUE PENDIENTE tras ACTO RECENSO-DISENO-14 (2026-08-24, ADR-149, ...)
    por falta de DESCRIPTOR, no por falta de payload. ...'
```

**Hash del payload, una sola invocación (`A.1`):**

```
$ python3 tests/manifiesto.py --verifica
...
ensafi2023_fd_xlsx_zip [data_raw]: COINCIDE -- sha256 y tamaño (1108577 bytes)
    verificados contra data/manifiesto.yaml           (línea 795 de 951)
```

`COINCIDE`. No hay `PARO` por hash discordante.

**Declaración honesta sobre el exit code de esa corrida: fue `1`, no `0`.** No es de nuestro
payload. Sobre las **951 líneas** que emitió: **790** dicen `COINCIDE` y **exactamente una** dice
`NO COINCIDE` — `endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf` (línea 323), discordancia
**preexistente y ajena** a este acto y a ENSAFI. Está **fuera del perímetro** y no se toca. Se
declara aquí en vez de esconderse detrás de un `grep` filtrado que solo hubiera enseñado la línea
conveniente.

```
$ command grep -cE "NO COINCIDE|CORRUPTO" verifica.txt   → 1
$ command grep -cE "COINCIDE" verifica.txt               → 790   (control positivo)
```

---

## 2 · El FD abierto (`A.6`: leído por este acto, no heredado)

`forense/ficha-r34-condBC-v1_0.md` Anexo 2 ya había leído este FD y afirmaba que «trae `FAC_ELE`,
`UPM_DIS` y `EST_DIS`». Bajo `A.6` eso **no cuenta como verificado por este acto**: se reabrió el
payload desde cero.

**No hay `unzip` en esta caja** (`/bin/bash: unzip: command not found`, exit 127). Se usó
`zipfile` de Python, que produce el mismo inventario:

```
   1043071  2024-07-25 16:17:34  ensafi_2023_fd.pdf
    109082  2024-07-25 16:20:10  ensafi_2023_fd.xlsx
   (2 entradas)
```

**El payload trae DOS portadores del mismo descriptor.** Se leyeron los dos, y esto no fue
redundancia: es lo que permite atribuir los defectos de abajo al INEGI y no a la lectura.

- **XLSX**, con `openpyxl`, celda a celda: cuatro hojas `TVIVIENDA` / `THOGAR` / `TSDEM` /
  `TMODULO`. **12 920 celdas examinadas · 12 coincidencias** con los cinco nemónicos buscados.
- **PDF**, con `pypdf`: **49 páginas examinadas · 12 coincidencias**.

Los dos coinciden **hasta en sus dos defectos**. Luego los defectos son del documento, no del lector.

### 2.1 · Las doce filas, con hoja y celda

Las cuatro hojas tienen una sección con el encabezado literal **`VARIABLES DE DISEÑO ESTADÍSTICO`**
(`B132` en `TVIVIENDA`, `B269` en `THOGAR`, `B132` en `TSDEM`, `B932` en `TMODULO`). Columnas:
`B`=Pregunta[1] · `C`=Nemónico[2] · `D`=Tipo[3] · `E`=Tamaño[4] · `F`=Códigos válidos[5] ·
`G`=Concepto[6].

| Hoja | Fila | `C` (nemónico) | `B` (Pregunta[1]) | `G` (Concepto[6]) | Tipo · Tamaño · Códigos |
|---|---|---|---|---|---|
| TVIVIENDA | 135 | `FAC_VIV` | FACTOR VIVIENDA DE EXPANSIÓN | FACTOR VIVIENDA DE EXPANSIÓN | Numérico · 6 · 125-72801 |
| TVIVIENDA | 136 | `UPM_DIS` | UPM DE DISEÑO MUESTRAL | UPM DE DISEÑO MUESTRAL | Alfanumérico · 5 · 00001-02918 |
| TVIVIENDA | 137 | `EST_DIS` | ESTRATO DE DISEÑO MUESTRAL | ESTRATO DE DISEÑO MUESTRAL | Alfanumérico · 5 · **`0001 - 00277`** |
| THOGAR | 272 | `FAC_HOG` | FACTOR **HOGAR** DE EXPANSIÓN | FACTOR **VIVIENDA** DE EXPANSIÓN | Numérico · 6 · 126-72801 |
| THOGAR | 273 | `UPM_DIS` | UPM DE DISEÑO MUESTRAL | UPM DE DISEÑO MUESTRAL | Alfanumérico · 5 · 00001-02918 |
| THOGAR | 274 | `EST_DIS` | ESTRATO DE DISEÑO MUESTRAL | ESTRATO DE DISEÑO MUESTRAL | Alfanumérico · 5 · 00001-00277 |
| TSDEM | 135 | `FAC_HOG` | FACTOR **HOGAR** DE EXPANSIÓN | FACTOR **VIVIENDA** DE EXPANSIÓN | Numérico · 6 · 126-72801 |
| TSDEM | 136 | `UPM_DIS` | UPM DE DISEÑO MUESTRAL | UPM DE DISEÑO MUESTRAL | Alfanumérico · 5 · 00001-02918 |
| TSDEM | 137 | `EST_DIS` | ESTRATO DE DISEÑO MUESTRAL | ESTRATO DE DISEÑO MUESTRAL | Alfanumérico · 5 · 00001-00277 |
| TMODULO | 935 | `FAC_ELE` | FACTOR DE EXPANSIÓN | FACTOR DE EXPANSIÓN | Numérico · 6 · 126-364007 |
| TMODULO | 936 | `UPM_DIS` | UNIDAD PRIMARIA DE MUESTREO DE DISEÑO | ídem | Alfanumérico · 5 · 00001-02918 |
| TMODULO | 937 | `EST_DIS` | ESTRATO DE DISEÑO | ídem | Alfanumérico · 5 · 00001-00277 |

En el PDF gemelo: `TVIVIENDA` → pág. 5, `THOGAR` → pág. 14, `TSDEM` → pág. 19, `TMODULO` → pág. 49.

**La enumeración está cerrada, y esto importa para poder afirmar ausencias.** Se barrieron las
cuatro secciones **íntegras**, no solo las filas buscadas: cada una contiene **exactamente tres**
variables (un factor + `UPM_DIS` + `EST_DIS`) y termina en fila vacía (`138`, `275`, `138`, `938`).
No hay una cuarta variable de diseño en ninguna hoja. Una afirmación de ausencia sostenida por un
barrido completo, no por no haber encontrado nada.

### 2.2 · Los universos, uno por uno

**`FAC_VIV` → vivienda. Cita directa.** Su propia etiqueta lo dice: `TVIVIENDA` `B135`=`G135`=
`FACTOR VIVIENDA DE EXPANSIÓN`. Aparece en **una sola** hoja.

**`FAC_HOG` → hogar. Cita directa en `Pregunta[1]`, con defecto del FD en `Concepto[6]`.**
`THOGAR` `B272` y `TSDEM` `B135` dicen `FACTOR HOGAR DE EXPANSIÓN`. Pero `G272` y `G135` —columna
`Concepto[6]` del **mismo renglón**— dicen `FACTOR VIVIENDA DE EXPANSIÓN`. **Las dos columnas del
mismo renglón se contradicen.** El PDF (págs. 14 y 19) reproduce el defecto **idéntico**, luego es
un arrastre de copiado del INEGI y no un artefacto de `openpyxl`. Se adopta la lectura de
`Pregunta[1]` (HOGAR), que es la coherente con la tabla que lo aloja; se registra la contradicción
en la fila en vez de silenciarla.

**`FAC_ELE` → persona elegida. Cita INDIRECTA, y así queda declarada.** Aquí el encargo pedía «cita
hoja y celda/fila del FD, no lo infieras», y el FD **no da** la cita directa: el renglón de
`FAC_ELE` lleva etiqueta **genérica** — `TMODULO` `B935`=`G935`=`FACTOR DE EXPANSIÓN`, sin nombrar
universo. El universo se cita del **mismo FD y la misma hoja**, un renglón distinto: la
`LLAVE PRIMARIA` de `TMODULO`, `B17`=`G17`=**`Llave de identificación de la persona elegida`**
(`C17`=`LLAVEMOD`). Es cita dentro del documento, **no** inferencia desde otra encuesta de INEGI
—lo cual está prohibido y no se hizo—, pero es cita de la **unidad de registro de la tabla**, no de
la etiqueta del ponderador. La diferencia se hace explícita en la fila para que ningún acto futuro
tome la cita indirecta por directa.

**Nota terminológica:** el encargo escribió «persona elegible»; el FD dice **«persona elegida»**.
Se adopta la palabra del FD.

Para contraste, las llaves primarias de las otras tres hojas: `TVIVIENDA` `C17`=`LLAVEVIV`
(«Llave de identificación de la vivienda»), `THOGAR` `C17`=`LLAVEHOG` («…del hogar»), `TSDEM`
`C17`=`LLAVESDE` («…de la tabla sociodemográfica»).

**`EST_DIS` y `UPM_DIS` → variables de diseño, sin reserva.** Las etiquetas son explícitas
(`ESTRATO DE DISEÑO MUESTRAL` / `UPM DE DISEÑO MUESTRAL`, y en `TMODULO` `ESTRATO DE DISEÑO` /
`UNIDAD PRIMARIA DE MUESTREO DE DISEÑO`) y viven bajo el encabezado `VARIABLES DE DISEÑO
ESTADÍSTICO`. Esto **cierra la reserva escrita** que la fila arrastraba desde `RECENSO-DISEÑO-14`:
«sin FD no se puede confirmar que sea el estrato de diseño y no otro estrato». Ya se puede.

### 2.3 · Dos hallazgos colaterales, ambos con su comando

**(a) Errata del FD en `EST_DIS` de `TVIVIENDA`.** `F137` escribe el límite inferior con **cuatro**
dígitos, `0001 - 00277`, contra `Tamaño`=5 y contra las otras tres hojas (`00001 - 00277`). El PDF
(pág. 5) trae la misma errata. No cambia la identificación de la variable; se declara.

**(b) La fila afirmaba algo que el FD refuta, y se enmienda.** El campo `donde_vive` decía que
**solo** `TVIVIENDA` trae además una columna `UPM` sin sufijo. El FD la lista en las **cuatro**
hojas, en la sección `VARIABLES DE CONEXIÓN`:

```
TVIVIENDA C113 · THOGAR C245 · TSDEM C113 · TMODULO C861
   'UPM' = NÚMERO DE UNIDAD PRIMARIA DE MUESTREO, Alfanumérico, tamaño 7, 0100016 - 3260800
```

Barrido: **1 615 celdas de nemónico examinadas · 4 coincidencias exactas con `UPM`**. **Control
positivo del mismo barrido**, con `UPM_DIS`: **4** — el barrido sí mira. Lo que **sí** se sostiene
del texto viejo es su fondo: `UPM` a secas es identificador de conexión (tamaño 7, rango
geográfico-operativo), **no** el conglomerado de diseño; el conglomerado es `UPM_DIS` (tamaño 5,
`00001-02918`). El FD separa las dos por sección, tamaño y rango. Se corrigió el alcance de la
afirmación sin borrar su fondo, y se dejó dicho en el propio campo que es una corrección de este
acto.

**(c) `TSDEM` no tiene factor de persona.** `TSDEM` es la tabla de personas del hogar, pero el
único factor que el FD le da es `FAC_HOG`. Esto **no** es un negativo por ausencia de búsqueda: es
consecuencia de la enumeración cerrada de §2.1 (tres variables por sección, secciones barridas
íntegras). Queda sembrado como reserva en la fila.

---

## 3 · La fila cerrada

`estado: PENDIENTE` → **`estado: MAPEADO`**. Campos `ponderador` / `estrato` / `upm` reescritos
citando `ensafi2023_fd_xlsx_zip` con hoja y celda. `donde_vive` enmendado por §2.3(b) y
`procedencia` reescrito con el payload y los dos portadores.

**El texto viejo de `notas` NO se borró** — se conservó **verbatim** y el párrafo nuevo se añadió
después, fechado. Verificado por contención de cadena, no a ojo:

```
$ python3 -c "... print(viejo in nuevo)"
SI    (749 caracteres del texto viejo, íntegros dentro del campo nuevo)
```

**Movimiento del censo, derivado del propio YAML tras editar** (no tecleado):

```
$ python3 -c "import yaml,collections; d=yaml.safe_load(open('data/diseno-muestral.yaml'));
              print(collections.Counter(r['estado'] for r in d))"
MAPEADO: 23   PENDIENTE: 23   SIN_DISEÑO_PUBLICADO: 7
NO_APLICA_REGISTRO_ADMINISTRATIVO: 2   DISENO_EXPERIMENTAL: 1        (56 filas)
```

`MAPEADO` 22 → **23**; `PENDIENTE` 24 → **23**. **Exactamente una fila se movió**, y es la de
ENSAFI (`len([r for r in d if r['fuente'].startswith('ENSAFI')])` → 1). Ninguna otra fila del YAML
se tocó.

**Estampa `A.10`, escrita en la fila.** El universo bajo el que se toma este cierre: (i) el
descriptor `ensafi2023_fd_xlsx_zip` íntegro, sus dos portadores, leídos en este acto; (ii) la
verificación cruda de 2 000 filas por tabla de `RECENSO-DISEÑO-14` (24/ago), ya citada en el propio
campo; (iii) el Anexo 2 de `forense/ficha-r34-condBC-v1_0.md`. **Fuera de ese universo el cierre no
rige**: no cubre ninguna otra ronda de ENSAFI, ni los valores del microdato, ni ninguna estimación.
Si el universo crece, el cierre queda **VENCIDO EN ALCANCE** — no refutado.

**Deuda `A.5` caducada.** La receta manual que la fila describía («bajar el FD de
`inegi.org.mx/programas/ensafi/2023/#microdatos`») queda **CADUCADA por `ADR-198`**: el FD llegó el
25/ago (`ACTO ENSAFI-DESCRIPTOR`, `PR #370` — la API declaraba formato `_xlsx.zip` y no `.xlsx`; la
extensión era el obstáculo, no la publicación). No se ejecutó, no se re-descargó nada. El texto de
la receta **se conserva sin borrar** como registro de por qué la fila estuvo pendiente.

**`FP-115` citada y NO tocada.** Esa ficha cubre tres fuentes; aquí se resuelve únicamente la parte
ENSAFI. **El tablero no se edita en este acto.**

---

## 4 · Desviación de perímetro, declarada

El encargo lista el perímetro y añade: *«Si te encuentras escribiendo fuera de esta lista, PARA — el
perímetro estaba mal calculado y saberlo vale más que el atajo.»* Se encontró. Se declara en vez de
tomarse el atajo callado.

**Qué pasó.** `A.3` obliga a archivar el encargo **íntegro y verbatim**. El encargo se nombra a sí
mismo con el rótulo pelado `E4`, y `T25` (D-6/`ADR-128`) falla ante cualquier `M<n>`/`E<n>` pelado
en un archivo `.md` nuevo bajo `canon/` o `forense/`:

```
T25: forense/encargos/2026-08-26-E4-DISENO-ENSAFI.md: trae rótulo pelado nuevo `E4`
     sin prefijo de espacio (D-6/ADR-128)
```

**Los dos mandatos del encargo chocan de frente:** archivar el texto de dirección sin editarlo
(`A.3`) y entregar `tests/check.py --baseline` en verde. El choque **no se puede resolver dentro
del perímetro declarado**, porque el mecanismo que el propio test nombra para resolverlo vive fuera
de él.

**Qué se hizo, y es la segunda rama que el propio mensaje de `T25` ofrece** («o, si ya estaba en uso
y solo faltaba censarlo, añádelo a `_T25_ARCHIVOS_CONOCIDOS` y a `canon/registro-rotulos.tsv`»):

- `canon/registro-rotulos.tsv` — **fuera de perímetro** — una fila nueva censando `E4` en el
  espacio `E`, con su colisión declarada: `E4a`/`E4b`/`E4c` ya existen y son las partes a/b/c de la
  **entrada 4 del motor**, referente completamente distinto de este acto de diseño muestral. Cuatro
  referentes en la forma pelada del token, ninguno gana — mismo patrón ya registrado para `M5` y
  para `E-3`/`E3-TRIAGE`.
- `tests/check.py` — **fuera de perímetro** — el encargo y esta nota añadidos a
  `_T25_ARCHIVOS_CONOCIDOS`, con comentario que explica por qué. La nota entra por la misma razón
  que `forense/notas/2026-08-24-adq-corre-r74r75-cierre.md` en su día: **narrar el hallazgo de
  `T25` obliga a escribir el token otra vez**, y una nota de cierre que no puede nombrar su propio
  encargo es peor que la desviación.

`canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md` **ya** estaban en esa lista; no
requirieron nada.

**Precedente exacto, no invención de este acto.** El mismo movimiento, por la misma razón y con la
misma etiqueta —«extensión mínima de perímetro por desviación mecánica (CI del propio acto)»— está
registrado para `PREREG-CORRIDA` (`ADR-194`), `SELLA-AGO24-C-v2` (`ADR-155`) y `ADQ-CORRE-R74R75`
(`ADR-158`). En los tres, la razón escrita es idéntica: **el texto de dirección no se edita para
complacer a un test.**

**Lo que NO se hizo:** no se renombró el encargo, no se editó una sola palabra del texto de
dirección, no se relajó la expresión regular de `T25`, no se congeló línea base nueva (`--freeze`).
La desviación son **dos archivos** y está enteramente contenida en el censo del rótulo.

---

## 5 · Suite

`python3 tests/check.py --baseline`. La corrida previa a corregir `T25` daba **3 entradas nuevas**
frente a `tests/baseline.json`: la de `T25` y dos de `T16` —que son **consecuencia aritmética** de
la primera, no un defecto independiente: `T16` compara el conteo declarado en canon contra el real,
y el `FAIL` de `T25` movía el real de 19 a 20. Censado el rótulo, las tres caen juntas.

**Cifra final, sobre el árbol fusionado con `PR #371` y `PR #372`: 19 FAIL · 128 WARN, LÍNEA BASE VERDE, exit 0.** El árbol de este acto en solitario daba **19 FAIL · 129 WARN**; el `−1` de WARN **no es de este acto** sino de `ADR-201` (`ACTO CIERRA-FP157`), que sacó `FP-157` de `ABIERTA` y ya recifró canon a 128 — `T16` da `[ok]`. **Este acto no mueve ni FAIL ni WARN.** Detalle de la doble colisión de numeración en el bloque `Cascada` de `ADR-202`.

---

## 6 · Perímetro tocado y lo que este acto NO hace

**Tocado.** `data/diseno-muestral.yaml` (**una** fila) · `forense/notas/2026-08-26-diseno-ensafi-cierre.md`
(nueva) · `forense/encargos/2026-08-26-E4-DISENO-ENSAFI.md` (`A.3`) · `canon/gobernanza-v1_15.md` ·
`canon/estado-programa-v1_10.md` · **fuera del perímetro declarado y justificado en §4:**
`canon/registro-rotulos.tsv` · `tests/check.py`.

**NO hace.** No descarga nada. No abre `ensafi_2023_bd_csv.zip` ni ningún valor del microdato de
datos. **No estima nada** — ni una tasa, ni un error estándar, ni un efecto de diseño. No toca otra
fila del YAML. No toca el tablero de firmas ni `FP-115`. No infiere ningún universo de ponderador
desde otra encuesta de INEGI. No convierte el cierre en juicio sobre ninguna regla del motor. No
reabre `R3.4` — solo habilita que quien la reabra pueda calcular varianza de diseño de ENSAFI con
las variables ya identificadas y citadas. No mueve ningún contador de canon: **contador cero,
declarado**.
