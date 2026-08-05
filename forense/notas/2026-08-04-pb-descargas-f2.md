# P-B · Descargas F2-restante + alta de fuentes de clase nueva

Mesa, 4/ago/2026. Worktree nuevo: `/home/pc0/mm-pb-descargas-f2`, rama
`sesion/pb-descargas-f2`, base `origin/main` = `32d9321` (merge de PR #100 —
censo de diseño muestral, **fusionado durante esta misma sesión**,
`2026-08-05T00:28:20Z` UTC — verificado con
`gh pr view 100 --json state,mergedAt,mergeCommit`). Apertura vía
`python3 tests/bitacora.py --abre`: HEAD == `origin/main`, línea base VERDE
(`tests/baseline.json`, HEAD congelado `837d5fe`), `validador_registro_ids.py`
OK (49 IDs, 27 en perímetro), `instrucciones` v2.3 confirmada contra el propio
archivo (`instrucciones-proyecto-v2.md:1`, sin desvío frente a lo reportado
por el script).

## 0 · La matriz de concurrencia citada por el encargo no existe — verificado, no fabricada

El encargo original citaba "la matriz de concurrencia de arriba" en un
archivo `PARALELO-PA-deferencia-y-PB-descargas.md` {cita-ilustrativa}. Ese archivo **no existe**
en ningún lugar: cero resultados en `git log --all` sobre todas las ramas,
cero menciones en `canon/protocolo-sesion-v1_0.md` o `canon/gobernanza-v1_15.md`,
cero archivo físico en los ~30 worktrees vivos de `/home/pc0/mm-*` al momento
de verificar. Mismo patrón, segunda ocurrencia el mismo día: ACTO M ya había
verificado horas antes que `PARALELOS-tanda-2.md` {cita-ilustrativa} tampoco existe
(`forense/hallazgos.md:108`; detalle en
`forense/notas/2026-08-04-censo-diseno-muestral.md:23-60`). Tercera
ocurrencia del mismo patrón, ver §2 (ESTAD citada como "ENSATD" en el
encargo de Encargo AA). Por ADR-39 (regla de premisas,
`canon/gobernanza-v1_15.md:294`): se reporta, no se ejecuta a ciegas, no se
fabrica una matriz para que el encargo cuadre.

**Derivada en su lugar, tipo (1), cruda** (`2026-08-05T00:37:23Z` UTC):

```
$ git branch -r
  origin/HEAD -> origin/main
  origin/main

$ gh pr list --repo Josanoforo/Modelado-Mexicano --state open
(vacío — cero PRs abiertos)
```

Y, del `git fetch --all --prune` corrido al abrir este acto (`2026-08-04
18:35 local`, antes de crear este worktree):

```
 - [deleted]  (none) -> origin/sesion/cal-conf-faseb-pos8-encig-battxi
 - [deleted]  (none) -> origin/sesion/censo-diseno-muestral
 - [deleted]  (none) -> origin/sesion/cruce-catalogo-fichas
 - [deleted]  (none) -> origin/sesion/descarga-dirigida
 - [deleted]  (none) -> origin/sesion/enasem-paso1-descriptor
 - [deleted]  (none) -> origin/sesion/encargo-aa-clase-fuente
 - [deleted]  (none) -> origin/sesion/encargo-w-coeficientes-generador
 - [deleted]  (none) -> origin/sesion/encargo-x-condicionamiento-forma
 - [deleted]  (none) -> origin/sesion/encargo-y-tres-falsaciones-hitod
 - [deleted]  (none) -> origin/sesion/encargo-z-cuatro-fichas-sin-fuente
 - [deleted]  (none) -> origin/sesion/encup-certificado-fijado
 - [deleted]  (none) -> origin/sesion/encup-paso1-deferencia
 - [deleted]  (none) -> origin/sesion/encup-paso2-deferencia
 - [deleted]  (none) -> origin/sesion/enut-paso1-familismo-obligacion
 - [deleted]  (none) -> origin/sesion/hitoD-r5-1-pension-bienestar
 - [deleted]  (none) -> origin/sesion/hitoD-r7-2-delito-sin-seguro
 - [deleted]  (none) -> origin/sesion/p3-lca-segmentacion
 - [deleted]  (none) -> origin/sesion/sens-estatus-examen-descriptor
 - [deleted]  (none) -> origin/sesion/svystat-casos-referencia
   9729894..32d9321  main -> origin/main
```

**Lectura** (no re-derivada, solo interpretación de lo de arriba): todas las
ramas `sesion/*` de PRs fusionados el 4/ago fueron borradas de `origin` tras
su merge; único ref remoto vivo hoy es `origin/main`. No hay ninguna otra
rama/PR viva que pueda colisionar con el perímetro de este acto
(`data/manifiesto.yaml`, `data/raw/`, este archivo de nota). P-A
(`sesion/encup-paso2-deferencia`) ya cerró como PR #96 ("PARO: ENCUP paso 2
(deferencia)", fusionado `2026-08-04T22:40:35Z`) más de una hora **antes**
de que PR #100 (que trae la lista de compras de este acto) se abriera
siquiera (`2026-08-04T23:41:06Z`) — no hay concurrencia real que coordinar
con P-A, solo con lo que aparezca de aquí en adelante. Local worktrees vivos
en `/home/pc0/mm-*` en este momento no se re-barrieron uno por uno en este
acto (a diferencia de ACTO M) porque el barrido de PRs/ramas remotas arriba
ya cierra la pregunta relevante para este perímetro: nada vivo toca
`data/manifiesto.yaml` ni `data/raw/`.

## 1 · Procedencia de la lista de compras

`data/diseno-muestral.yaml` **no vivía en `main`** al momento en que el
encargo fue escrito — vivía solo en `sesion/censo-diseno-muestral` (PR #100,
sin fusionar en ese momento). PR #100 se fusionó **durante esta misma
sesión** (`32d9321`, `2026-08-05T00:28:20Z` UTC) — verificado con
`gh pr view 100 --json state,mergedAt,mergeCommit`. La cifra de 32
`PENDIENTE` se deriva de `data/diseno-muestral.yaml` **tal como quedó en el
commit de merge `32d9321`**, que es el HEAD de este worktree sin cambios
posteriores:

```
$ python3 -c "import yaml,collections; print(collections.Counter(e['estado'] for e in yaml.safe_load(open('data/diseno-muestral.yaml'))))"
Counter({'PENDIENTE': 32, 'MAPEADO': 9, 'SIN_DISEÑO_PUBLICADO': 2})
```

De los 32: 6 (ENNViH, ENOE, ENDIREH, ENDUTIH, MOCIBA, LAPOP) traen nota de
diseño parcial con hueco nombrado (nombre de columna no confirmado, o
payload ausente en este entorno mismo). Los 26 restantes traen la nota
genérica "operable según catálogo pero SIN payload en `data/manifiesto.yaml`
... No se descarga aquí (perímetro de P-B)" — nombrando explícitamente a
este acto como su dueño corriente.

## 2 · CLUES / Cero Desabasto / ESTAD — citadas desde el entregable de Encargo AA

Fuente: `data/inventarios/inventario_fuentes_clase-fuente-mexico.md`
(escrito en el worktree `mm-encargo-aa-clase-fuente`, mismo contenido en
`main` vía PR #94, verificado presente en `main` en este acto).

- **CLUES** — entrada #1 (línea 33), URL en línea 43: `http://www.dgis.salud.gob.mx/`
  (HTTP, no HTTPS — verificado por sondeo directo en Tarea B de Encargo AA;
  réplicas `datos.gob.mx` / `gobi.salud.gob.mx` no alcanzables en ese sondeo).
  **Está entre las 32 `PENDIENTE`** de este acto (no es muestra
  probabilística — es registro administrativo georreferenciado — pero la
  entrada de censo la incluyó igual, "sin payload").
- **Cero Desabasto** — entrada #6 (línea 110), URL en línea 120:
  `https://cerodesabasto.org` (alcanzable, verificado en Tarea B). **No
  aparece en `data/diseno-muestral.yaml`** — no es muestra probabilística,
  el censo de diseño muestral no la cubre por diseño.
- **"TratoDigno" no es un nombre real.** Es **ESTAD** (Encuesta de
  Satisfacción, Trato Adecuado y Digno; DGCES/INSP desde 2015) — entrada #12
  (línea 200: *"Encuesta de Satisfacción, Trato Adecuado y Digno (ESTAD) —
  buscada como 'ENSATD'"*). El propio encargo de Encargo AA ya documentó
  que el nombre con el que llegó a esa sesión ("ENSATD") no correspondía a
  ningún instrumento real — tercera ocurrencia del mismo patrón de citación
  rota que §0 de esta nota. URL en línea 210: `https://calidad.salud.gob.mx`
  (alcanzable, verificado; variante estatal `sesa.qroo.gob.mx/sestad/` no
  alcanzable en ese sondeo). **Tampoco aparece en `data/diseno-muestral.yaml`.**
  Precaución de mesa aplicada al derivar esto: no confundir con la clave
  `estado:` del YAML (presente en las 43 entradas) ni con "ESTADÍSTICA
  EDUCATIVA" / "ESTADÍSTICAS DE NATALIDAD", que son otras fuentes con el
  mismo substring "ESTAD".

## 3 · Alcance de este acto (perímetro declarado)

Descarga ciega únicamente — estructura (listado top-level de archivo, sin
extraer ni leer contenido interno) + `sha256` + registro en manifiesto.
Cero apertura de contenido: no se abre ningún documento de diseño
descargado, no se lee ninguna estructura interna de zip/PDF más allá de un
listado de nombres cuando el formato lo expone sin necesidad de extraer
bytes. Nivel de contaminación declarado por ADR-46
(`canon/gobernanza-v1_15.md:367`): descarga ciega, no contamina — salvo que
una fuente puntual requiera declarar explícitamente lo contrario, en cuyo
caso se anota aquí por fuente, no en bloque.

**No se tocó** `mm-censo-diseno-muestral` en ningún momento de este acto
(instrucción de mesa) — su estado de merge, si seguía a medias al momento de
escribir esto, es responsabilidad de la sesión que lo está cerrando, no de
esta.

## 4 · Cruce re-derivado SIN PAYLOAD contra el manifiesto de hoy

`data/catalogo_unico.json` trae un campo `en_disco` por fuente, pero **hereda
el mismo defecto de `tests/dedup.py`** que ACTO M ya documentó (no reconoce
ENSANUT por prefijo numérico de id, ni LATINOBARÓMETRO por el acento no
normalizado) — verificado aquí de nuevo: `en_disco=False` para ENSANUT y
LATINOBARÓMETRO pese a tener payload real. Re-derivado con normalización de
acento+minúsculas y coincidencia de substring (no solo prefijo) contra los
202 ids de `data/manifiesto.yaml`:

```
Operables (micro=sí, libre=sí): 43
EN DISCO (re-derivado): 17 — CPV, ENADID, ENCIG, ENCUCI, ENCUP, ENDIREH,
  ENDUTIH, ENIF, ENIGH, ENNVIH, ENOE, ENSANUT, ENUT, ENVIPE, LAPOP,
  LATINOBARÓMETRO, MOCIBA
SIN BAJAR (re-derivado): 26 — ACS, CLUES, CNGF, CNGMD, CONEVAL, CPS,
  ECOVID-ML, EDER, EDR, EIC, ELCOS, ENAPROCE, ENASEM, ENCUESTA NACIONAL DE
  BIENESTAR, ENCUESTA NACIONAL PARA EL SIST[EMA DE CUIDADOS], ENFIH, ENPOL,
  ENSAFI, ENSU, ENTI, ESTADÍSTICA EDUCATIVA, ESTADÍSTICAS DE NATALIDAD / NA,
  GLOBAL FINDEX DATABASE, INE, REGISTROS ADMINISTRATIVOS DE E[STADÍSTICAS
  VITALES], SAEH
```

**Coincide exactamente, cifra y nombres, con los 17/26 que ACTO M ya había
verificado a mano** — buena señal cruzada, dos métodos independientes
(anotación manual por FASE B vs. re-derivación por substring normalizado)
convergen. **Hallazgo:** el tier "SIN PAYLOAD del cruce re-derivado" que el
encargo pide añadir "solo después" del censo de 32 PENDIENTE **no aporta
nada nuevo** — sus 26 son un subconjunto exacto de los 26 genéricos ya
dentro de los 32 PENDIENTE (los otros 6 de los 32 — ENNViH, ENOE, ENDIREH,
ENDUTIH, MOCIBA, LAPOP — traen payload parcial o tienen huecos de diseño no
resueltos por payload). No hay una lista "aparte" que agregar.

## 5 · Descargas ejecutadas — solo lo resoluble desde metadato ya catalogado

**Regla aplicada:** URL debía estar ya registrada en `data/manifiesto.yaml`
(entrada existente marcada AUSENTE) o citada con archivo:línea en un
inventario/catálogo ya escrito — cero descubrimiento nuevo, cero navegación
de páginas para inferir un enlace.

Barrido sistemático de las 32 acrónimos + CLUES/Cero Desabasto/ESTAD contra
**todos** los `id` de `data/manifiesto.yaml` (no solo lo que ya está en
disco) encontró 4 coincidencias registradas-pero-ausentes, todas en
`inegi.org.mx` (dentro de la lista blanca de red de este entorno):

| id | tamaño registrado | sha256 verificado tras descarga |
|---|---|---|
| `endireh2021_fd_pdf` | 10 369 637 B | `5c30a3f7f88123ca672f1042ec3b5c37cc1d7989f07fd23ecbf088cca6dda180` — COINCIDE |
| `endireh2021_bd_csv_zip` | 78 902 567 B | `e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e` — COINCIDE |
| `endutih2024_bd_dbf_zip` | 8 823 853 B | `ef723ed125c81c4a9036b74fab67f520de007a2d52c5e0b03d4ebec509e1ae87` — COINCIDE |
| `mociba2024_bd_csv_zip` | 1 500 882 B | `105e2e266134be538d33b5685e24bd41247eec5156f27b11ada7a3bb50f0a7ab` — COINCIDE |

Las 4 verificadas con `tests/manifiesto.py --verifica --id <id>`, **una por
invocación** — la instrumentación tiene un defecto ya registrado
(`forense/hallazgos.md`: múltiples `--id` en la misma invocación solo
verifica el último, sin aviso; reproducido aquí antes de descubrir que ya
estaba documentado, corregido al verificar cada id por separado). Tamaño
confirmado por sondeo HTTP (`curl -sI`) contra `tamano_bytes` del manifiesto
**antes** de descargar el cuerpo completo, mismo método que la entrada
original de `endireh2021_fd_pdf` ya documentaba. Cero contenido abierto:
ningún zip se extrajo, ningún PDF se leyó.

**Efecto colateral útil, no ejecutado aquí:** con `endireh2021_fd_pdf` y
`endireh2021_bd_csv_zip` ahora ambos presentes, ENDIREH queda con todo el
payload que su nota de `PENDIENTE` pedía — una sesión futura con
declaración de contaminación propia podría intentar cerrar sus columnas de
diseño (`estrato`/`upm`/`ponderador`). No se abrió nada de eso aquí.

**Casi-coincidencias descartadas, para que no se repitan como si fueran
resueltas:**
- `indice_de_bienestar_cuestionarios` (registrado, AUSENTE, host
  `ensanut.insp.mx`) **no es** "Encuesta Nacional de Bienestar
  Autorreportado" (ENBIARE) — son dos instrumentos distintos con nombre
  parecido; ENBIARE vive en `https://www.inegi.org.mx/programas/enbiare/2021/`
  (página, no archivo). Tampoco se intentó: `ensanut.insp.mx` no está en la
  lista blanca de red de este entorno.
- "Encuesta para la Medición del Impacto COVID-19 en la Educación
  (ECOVID-ED)" (`inventario-fuentes-tecnologia-digital-mexico.md`) **no es**
  el ECOVID-ML de la lista de compras (Encuesta Telefónica sobre COVID-19 y
  Mercado Laboral) — mismo prefijo "ECOVID", instrumento distinto.

**Las 26 `SIN BAJAR` restantes (§4) no se descargaron.** Cada una tiene, a
lo más, una URL de página de programa (`inegi.org.mx/programas/X/YYYY/`) o
de portal (`coneval.org.mx`, `worldbank.org`), no un enlace de archivo
directo — y una (`Estadísticas de Natalidad`) trae su propia advertencia de
origen: *"no verificado — URL construida por analogía, confirmar"*. Resolver
cualquiera de estas exige abrir/parsear una página para encontrar el enlace
real — reconstrucción, no ejecución del alcance ya dado. Instrucción de
mesa aplicada: nombrado aquí, no reconstruido. Nota de entorno conocida
(Encargo AA §4): varias páginas de `inegi.org.mx/programas/` son SPA que no
exponen el enlace a herramientas headless — ni siquiera intentar un fetch
simple garantizaría encontrar el archivo real.

## 6 · Verificación de corpus compartido (defecto PR #77)

`data/raw` **no existía** en este worktree al crearlo — ni directorio ni
symlink, no versionado por git (`git ls-files data/raw` vacío). Creado
explícitamente como symlink a `/home/pc0/mm-corpus/raw` (idéntico al de
`mm-encargo-aa-clase-fuente` y `mm-censo-diseno-muestral`, verificado con
`readlink`) **antes** de la primera descarga. Las 4 descargas se escribieron
directamente en `/home/pc0/mm-corpus/raw/.../` (ruta real, no a través del
symlink relativo del worktree, para eliminar cualquier duda). Confirmado
visible desde otro worktree hermano tras la descarga:

```
$ ls /home/pc0/mm-encargo-aa-clase-fuente/data/raw/endireh2021/
bd_endireh_2021_csv.zip  endireh2021_fd.pdf
```

Sin este paso, las 4 descargas habrían quedado locales a este worktree
únicamente — exactamente el defecto de PR #77 que la mesa citó.
