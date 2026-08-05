# ACTO M — Censo de diseño muestral del corpus

**Origen.** El PARO de P-A (`PR #96`, `sesion/encup-paso2-deferencia`, mergeado en
`fbfd3dda9`) mostró que ENCUP 2012 no tiene diseño muestral resoluble sin abrir
el instrumento, y que nadie sabía de cuántas fuentes más era cierto lo mismo.
Este acto responde esa pregunta una vez, para las 17 fuentes con payload en
`data/manifiesto.yaml`, y deja nombradas (`PENDIENTE`) las 26 operables del
catálogo (`data/catalogo-fuentes-v2_0.md` / `data/catalogo_unico.json`) que
aún no tienen payload.

Producto: `data/diseno-muestral.yaml` (archivo nuevo, cero traslape con
`canon/`, `milpa/`, `tests/`, `data/manifiesto.yaml`).

## 0 · Verificación de premisas del encargo (antes de ejecutar)

El encargo se redactó "contra `origin/main` = `4b27869` (re-deriva al
lanzar)". Al lanzar, `origin/main` ya había avanzado a `fbfd3dda9` (merge de
`PR #96`, 42 minutos después de `4b27869`) — verificado que `4b27869` es
ancestro de `fbfd3dda9` (`git merge-base --is-ancestor`), consistente con "re-
deriva al lanzar": no es una premisa rota, es la premisa funcionando como se
declaró.

**Premisa que SÍ falló la verificación: la matriz `PARALELOS-tanda-2.md` {cita-ilustrativa}.**
El encargo dice "CONCURRENCIA (matriz de `PARALELOS-tanda-2.md` {cita-ilustrativa} + esta
fila)". Ese archivo **no existe** — verificado con `git log --all --oneline
-- '*PARALELOS*'` (cero resultados en todo el historial, todas las ramas),
`git show <rama>:PARALELOS-tanda-2.md` {cita-ilustrativa} contra cada rama local y remota (cero
encontrados), y un `grep -rl "PARALELOS"` acotado sobre `/home/pc0` (el único
hit fue un paste-cache del propio texto del encargo, no un archivo de
matriz). Tampoco aparece en `canon/protocolo-sesion-v1_0.md` (que sí
describe cómo se parte un traspaso, §3, pero no menciona ninguna matriz de
paralelos) ni en `canon/gobernanza-v1_15.md`.

Por la regla de premisas (ADR-39, `gobernanza:290`): una premisa que no se
sostiene contra el archivo se reporta, no se ejecuta a ciegas y no se ajusta
el texto para que cuadre. Este es exactamente ese caso — se reporta aquí y
en `forense/hallazgos.md`. **No se detuvo el acto completo**, porque la
regla de señal de v2.3 pregunta si el defecto impide medir, y este no lo
hizo: se verificó independientemente, sin la matriz, que no hay colisión —

- `gh pr list --repo Josanoforo/Modelado-Mexicano --state all` (105 PRs):
  ninguna rama abierta toca `data/diseno-muestral.yaml`, `forense/notas/`
  (con el nombre de esta nota) ni `forense/hallazgos.md` de forma
  conflictiva; la única PR abierta hasta el lanzamiento (`#96`) ya estaba
  mergeada.
- Barrido de los ~30 worktrees vivos en `/home/pc0/mm-*` (`git log
  origin/main..HEAD` + `git status --short` en cada uno): tres tenían
  commits locales no mergeados (`mm-cruce-catalogo-fichas`,
  `mm-regla-elegibilidad-preregistro`, `mm-svystat-casos-referencia`) — los
  tres tocan `canon/`, `milpa/`, `tests/check.py` o notas con nombres
  propios distintos al de este acto; ninguno toca `data/diseno-muestral.yaml`
  ni colisiona con el nombre de esta nota.

Dicho lo cual: la matriz declarada como fuente de verdad para concurrencia
**no existe**, y esta verificación sustituta es más débil que consultarla
(no ve acuerdos de "quién toca qué" que no se hayan materializado todavía en
un commit o rama). Si `PARALELOS-tanda-2.md` {cita-ilustrativa} existe en algún lugar fuera de
este entorno (documento de mesa, otra sesión, otra máquina) y declara algo
que contradiga el perímetro de este acto, ese documento manda sobre esta
nota.

## 1 · FASE A — consolidación limpia (commit `07aa541`)

**Universo del censo, derivado (no tecleado):**

- `python3 tests/catalogo.py && python3 tests/dedup.py` (RECETA: consistente,
  11 inventarios) → 131 fuentes únicas, 43 operables (microdato + acceso
  libre), cruce contra `data/manifiesto.yaml` reporta 16 registradas / 15
  "ya en disco" (heurística de `dedup.py`, ver defecto abajo) / 28 sin bajar.
- Verificación independiente contra `data/manifiesto.yaml` (202 entradas,
  parseo por prefijo de `id`, no por texto libre — el texto libre dio dos
  falsos positivos, ver más abajo): **17 fuentes con payload real** (CPV,
  ENADID, ENCIG, ENCUCI, ENCUP, ENDIREH, ENDUTIH, ENIF, ENIGH, ENNViH, ENOE,
  ENSANUT, ENUT, ENVIPE, LAPOP, LATINOBARÓMETRO, MOCIBA) — dos más que la
  heurística de `dedup.py`, que no reconoce a ENSANUT (ids con prefijo
  numérico, `1_vfinal_...`) ni a LATINOBARÓMETRO (acento en "Ó" no
  normalizado en la comparación de prefijos). **Defecto de `tests/dedup.py`,
  no de este acto** — no se corrige aquí (fuera de perímetro, `tests/` no se
  toca); una línea en `forense/hallazgos.md`.
- **26 operables del catálogo sin payload** → `PENDIENTE`, derivadas
  restando el conjunto de 17 verificado (no las 15 de la heurística) del
  conjunto de 43 operables.
- Dos entradas del manifiesto sin campos (`nota_metodologica_rotulo_pareada`,
  `hitoD_fase1_ediciones_requieren_navegador`) y cinco `descargamasiva_
  3072026_*` se excluyeron del censo por fuente: las primeras dos no son
  payload; las cinco últimas son el instalador/lanzador genérico "Descarga
  Masiva" de INEGI (mismo componente para cualquier encuesta), **no
  identificables como de una fuente específica** —
  `forense/notas/2026-07-31-enut-descarga.md` §"Parte 2" ya lo declaró así
  explícitamente ("No se identifican... el nombre no lleva ningún token de
  programa, año o idBiinegi") y esta sesión lo verificó antes de asumir que
  eran de ENUT (candidato obvio por streak temporal, descartado por la
  propia nota).

**Barrido de notas existentes** (workflow paralelo, 16 agentes de
solo-lectura, uno por fuente con payload salvo ENCUP —ya resuelta por
`PR #96`—; perímetro estricto: solo `.md`/`.yaml`, cero acceso a
`data/raw/`): **7 resueltas sin abrir nada** — ENCIG (`FAC_P18`/`EST_DIS`/
`UPM_DIS`), ENCUCI (`FAC_SEL`/`EST_DIS`/`UPM_DIS`), ENIF (`fac_per`/
`est_dis`/`upm_dis`), ENVIPE (`FAC_ELE`/`EST_DIS`/`UPM_DIS`), ENUT
(`FAC_PER`/`EST_DIS`/`UPM_DIS`), ENIGH (`factor`/`est_dis`/`upm`), ENSANUT
(`ponde_f`/`estrato`~`est_sel`/`upm`) — cada una con archivo:línea exacto en
`data/diseno-muestral.yaml`. LATINOBARÓMETRO resuelta como
`SIN_DISEÑO_PUBLICADO` vía una nota ya existente (`2026-08-03-cbis-
deferencia-externas.md:153`) que ya había leído la ficha técnica — sin abrir
nada nuevo.

Dos falsos positivos de "verificar, no heredar" que el barrido descartó
explícitamente (documentados en el propio `data/diseno-muestral.yaml`,
campo `notas` de ENCIG/ENADID): una nota de ENCUCI que mencionaba "ENCIG
2023" solo como comparación de contexto, y tres notas (`z1`/`z2`/`z3`,
Encargo Z) que citan la misma tripleta de nombres de ENSANUT y que por
convención de nombres compartida ("Nota 17") podrían haberse atribuido
erróneamente a ENADID.

## 2 · FASE B — sesión sacrificada, declarada por adelantado (commit
   siguiente a `07aa541`)

**Declaración previa al primer PDF (según lo exige el encargo):** esta
sesión abre documentos de diseño (FD/estructura/diccionario — NO
cuestionarios ni microdato) de cuatro fuentes de la lista de huecos de la
FASE A, y queda inhabilitada por ADR-46 para pre-registrar contra esas
cuatro. Es un intercambio a propósito: una elegibilidad por un mapa.

**Lista exacta de lo que se abrió, archivo por archivo:**

1. `data/raw/diccionario_cuestionario_ampliado_cpv2020.xlsx` (id manifiesto
   `cpv2020_diccionario_cuestionario_ampliado_xlsx`) — leído completo
   (4 hojas: VIVIENDAS, PERSONAS, MIGRANTES, "Modelo de datos") con un lector
   de xlsx propio (`zipfile` + `xml.etree.ElementTree`, biblioteca estándar
   — no hay `openpyxl`/`pandas` instalados en este entorno, verificado antes
   de intentar otra ruta).
2. `data/raw/fd_enadid23.xlsx` (id `enadid2023_fd_xlsx`) — leído completo
   (7 hojas: TVIVIENDA, THOGAR, TSDEM, TMIGRANTE, TFECHISEMB, TMUJER1,
   TMUJER2), mismo método.
3. `data/raw/ennvih/calculo-de-factores-de-expansion.pdf` (id
   `ennvih3_2009_factores_exp`) — leído completo con `pdftotext -layout`
   (410 líneas).
4. `data/raw/ennvih/guia_de_usuario_ennvih-3.pdf` (id `ennvih3_2009_guia`) —
   leído completo con `pdftotext -layout` (3361 líneas) — se abrió porque el
   documento anterior no traía nombres de columna; este tampoco los trae
   (es una guía de fusión de tablas/"libros", no un diccionario de diseño).
5. `"3. Metodología/Metodologías/enoe_n_diseno_muestral.pdf"` — extraído
   (sin tocar ningún otro archivo del zip) de `data/raw/enoe_n_trim3_2020-
   trim4_2022.zip` (id `enoen_trim3_2020_trim4_2022_documentacion_zip`),
   leído completo con `pdftotext -layout` (423 líneas).

**No se abrió**: ningún cuestionario, ningún microdato (CSV/DTA/DBF/SAS/SPSS
con valores reales), ni ningún otro archivo de las cinco fuentes anteriores
ni de ninguna otra. En particular, no se tocó `enoe_n_manual_critico.pdf`
(11 MB) ni `enoe_n_manual_entrevistador.pdf` (15 MB) del mismo zip de ENOE —
ambos quedan como candidato para una sesión futura si se decide perseguir el
nombre de columna de `estrato` en ENOE (que este acto no cerró, ver abajo).

**Resultado, fuente por fuente:**

- **CPV → `MAPEADO` (componente Cuestionario Ampliado).** `ESTRATO`
  (alfanumérico 17), `UPM` (alfanumérico 7), `FACTOR` (numérico, Factor de
  Expansión) — sección "DISEÑO MUESTRAL" del diccionario, confirmado igual
  en las tres hojas de microdato. El Cuestionario Básico del CPV es
  enumeración censal completa — no aplica ponderador de muestreo — es el
  Cuestionario Ampliado el que trae una muestra probabilística propia con
  estas tres variables. Cita: `data/diseno-muestral.yaml`, entrada CPV.
- **ENADID → `MAPEADO`.** `EST_DIS`/`UPM_DIS` (variables de diseño) —
  explícitamente distintas de `ESTRATO` (sustantiva, 1-4) y `UPM` (llave de
  enlace) que conviven en las mismas tablas con nombre casi igual. Ponderador
  varía por nivel: `FAC_VIV`/`FAC_HOG`/`FAC_PER`. Confirmado en TVIVIENDA,
  THOGAR y TMUJER1 con fila Excel exacta en `data/diseno-muestral.yaml`.
- **ENNViH → sigue `PENDIENTE`, no sube a `MAPEADO`.** El documento de
  cálculo de factores de expansión (ola 3) documenta el MÉTODO completo
  (región → estrato → UPM con probabilidad igual → USM con probabilidad
  proporcional al tamaño → vivienda; ajuste por no respuesta a nivel
  estrato; calibración) pero usa notación matemática genérica (subíndices
  h/i/r), nunca un nombre de columna real. La guía de usuario de la ola 3 se
  revisó completa (grep sin coincidencias de "estrato"/"upm"/"conglomerado"
  como nombre de campo) y tampoco lo trae. Dos de tres campos (`estrato`,
  `upm`) quedan sin nombre de columna citable — por diseño de este censo
  (regla dura: los tres campos necesitan nombre de columna, no solo rol
  conceptual), la entrada no sube a `MAPEADO`. Lo que sí cambió: antes solo
  había una cita de la FAMILIA de archivo del ponderador
  (`forense/hitoD-preregistro-v2_0.md:499,622`); ahora hay mecánica completa
  del diseño, citable, sin abrir el `.dta` real.
- **ENOE → sigue `PENDIENTE`, no sube a `MAPEADO`.** El documento de diseño
  muestral confirma "bietápico, estratificado y por conglomerados" y el
  procedimiento de colapsamiento de estratos (pseudo-estratos cuando un
  estrato original queda con menos de 2 UPM) — pero, igual que ENNViH, es
  puramente narrativo/matemático, cero nombres de columna en mayúsculas.
  `UPM` y `FAC`/`FAC_TRI`/`FAC_MEN` ya estaban citados como columnas reales
  por una nota previa (`2026-07-31-cal-enoe-fasea.md:126-127`); lo que falta
  es el nombre de columna de `estrato`, que solo viviría en el Descriptor de
  Archivos (`enoe_n_fd_c_bas_amp.pdf`), confirmado **ausente** en este
  entorno (no está en el zip de documentación ni en ningún otro lugar del
  corpus).

**Por qué no se intentó FASE B en ENDIREH/ENDUTIH/MOCIBA:** sus únicos
candidatos (`endireh2021_fd_pdf`, `endutih2024_bd_dbf_zip`,
`mociba2024_bd_csv_zip`) están **AUSENTES** en este entorno Ubuntu —
verificado con `tests/manifiesto.py --verifica --id <cada uno>` ANTES de
intentar abrir nada (metadata, no contaminante): los tres reportan
`AUSENTE`. No es una decisión de esta sesión, es una imposibilidad del
entorno — hallazgo distinto de "la fuente no tiene el dato" (regla de
`instrucciones` v2.2, no confundir ambos hallazgos).

**Por qué no se intentó FASE B en LAPOP:** su único archivo en el corpus es
un cuestionario (77 páginas), no un documento de diseño. Abrirlo habría
pagado el mismo costo de contaminación ADR-46 que los otros cuatro, por una
probabilidad de éxito baja (los cuestionarios de LAPOP no suelen traer el
anexo metodológico con estrato/UPM/ponderador). Se dejó la decisión de pagar
ese costo a una sesión futura o a mesa, en vez de gastarlo aquí
especulativamente — corolario de la regla de señal v2.3 ("antes de añadir
cualquiera, se declara qué defecto real atrapó").

## 3 · Verificación

```
python3 tests/check.py --baseline            → exit=0, LÍNEA BASE VERDE (no se movió nada -- este acto no toca vigilados)
python3 tests/validador_registro_ids.py       → exit=0, 49 IDs verificados
python3 -c "import yaml; d=yaml.safe_load(open('data/diseno-muestral.yaml')); print(len(d))"  → 43
```

## 4 · Lo que este acto NO hizo

No decidió qué fuente se usa para qué constructo (mesa/fichas). No
descargó nada (perímetro de P-B — los tres AUSENTE de este entorno se
quedan AUSENTE, no se persiguieron). No estimó nada. No propone test para
el yaml (si algún PARO futuro demuestra que hace falta, ese día se paga).
No tocó `data/manifiesto.yaml`, `milpa/procedencia.yaml`, `canon/` ni
`tests/`.
