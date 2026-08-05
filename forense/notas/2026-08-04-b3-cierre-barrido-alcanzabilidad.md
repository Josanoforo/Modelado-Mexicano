Contadores movidos: 0.

# Encargo B-3 (mesa #20) — Cierra el barrido de alcanzabilidad y baja lo ya resuelto

Sesión Sonnet, Ubuntu con red, worktree nuevo `/home/pc0/mm-b3-cierre-barrido`,
rama `sesion/b3-cierre-barrido-alcanzabilidad` desde `origin/main` = `65302f7`
(el encargo declaraba `8cdabcb`; `8cdabcb` es ancestro de `65302f7` — main avanzó
a través de PR #93–#107, incluido #107/D-2, confirmado fusionado antes de arrancar).
`data/raw` ausente al crear el worktree (como espera Bloque D — no es PARO),
enlazada a `/home/pc0/mm-corpus/raw`.

Este acto no produce una medición (no mueve un contador de falsación ni de
coeficiente): cierra infraestructura de descarga. El contador es cero y se
declara aquí, no al final.

## 0 · Arranque (Bloque D), textual

```
$ pwd
/home/pc0/Modelado-Mexicano   (clon existente, localizado; worktree nuevo creado desde aquí)
$ git log -1 --format="%h %s"
302ac5a Merge origin/main into sesion/cal-conf-faseb-pos4-envipe-paso1   (rama ajena, no tocada)
$ git fetch
8cdabcb..65302f7  main -> origin/main
$ git merge-base --is-ancestor 8cdabcb origin/main && echo ancestro
ancestro
$ gh pr view 107 --json state,mergedAt
state=MERGED, mergedAt=2026-08-05T03:14:21Z  (= 2026-08-04 21:14 hora local UTC-6, ADR-59)
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200
```

Firma correcta (Ubuntu con red, ADR-59b). Espejo: no usado — todo lo anterior
sale del clon, comando a la vista.

**Worktree nuevo:** `git worktree add /home/pc0/mm-b3-cierre-barrido -b
sesion/b3-cierre-barrido-alcanzabilidad origin/main`. Dio dos líneas
`error: could not write config file .git/config: Device or resource busy`
(contención transitoria — probablemente otra sesión concurrente escribiendo
`.git/config` compartido en el mismo instante) pero el comando completó y
`git worktree list` registró la rama correctamente. Verificado que no dejó
`.git/config` corrupto: releído íntegro (contiene las ~70 entradas de rama de
todas las sesiones vivas, incluida la nueva), `git status`/`git fsck` desde
dos worktrees hermanos (`mm-d2-descargas`, `mm-encargo-w1-p-policial`) siguen
funcionando, `fsck` solo reporta objetos dangling (basura normal de un repo
con decenas de ramas, no corrupción). Una línea a `forense/hallazgos.md`
(§7 de esta nota) — no impidió medir, no es PARO.

**Concurrencia derivada:**
- `gh pr list --state open`: solo #108 (`claude/censo-estimabilidad-6qok9w`,
  "estimability census for 15 generator coefficients") — no toca
  `data/manifiesto.yaml` ni `data/raw`.
- W1-P: vivo en `/home/pc0/mm-encargo-w1-p-policial`, rama
  `sesion/encargo-w1-p-policial`, HEAD `4dca34c`, no empujado a remoto.
  Perímetro declarado por el encargo (`tests/(w1-p)`, `forense/notas/(w1-p)`,
  `milpa/procedencia.yaml`) sin traslape con el de este acto
  (`data/manifiesto.yaml`, `forense/notas/(b3-barrido)`, `data/raw`), salvo
  `forense/hallazgos.md` (append gemelo, sin conflicto).
- Ningún otro worktree tenía `data/manifiesto.yaml` con cambios sin commitear
  al momento de arrancar (`git status` limpio salvo `data/raw` no trackeado,
  esperado).

## 1 · Lista vigente de sin-payload, derivada (no heredada)

```
$ python3 tests/catalogo.py && python3 tests/dedup.py && python3 tests/cruce_operables.py
```

`catalogo.py`: RECETA consistente. 201 entradas, 151 fuentes únicas por
acrónimo, 54 con micro=sí+libre=sí (operables antes de dedup por título).
`dedup.py`: 131 fuentes únicas tras dedup por acrónimo+título, 43 operables.
`cruce_operables.py`: cruce contra `data/manifiesto.yaml` — resultado crudo:

```
RESUMEN: {'EN MANIFIESTO': 11, 'PARCIAL': 2, 'SIN PAYLOAD': 30}
OPERABLES SIN PAYLOAD DE VERDAD: 30 de 43
```

**Este número (30) está mal, y el porqué es un hallazgo de instrumento, no un
error de cálculo mío** — ver §7. `tests/cruce_operables.py` mantiene un mapa
cerrado `MAPA[acrónimo] -> [prefijos de id]`, mantenido a mano. Siete claves
tienen lista vacía: `ENASEM`, `ENDIREH`, `ENDUTIH`, `MOCIBA`, `ENSU`,
`ENCUESTA NACIONAL DE BIENESTAR` (ENBIARE), `ENCUESTA NACIONAL PARA EL SIST`
(ENASIC). Con lista vacía, `pertenece()` (`any()` sobre lista vacía) nunca
atribuye una entrada a esas siete claves — **sin importar qué exista en el
manifiesto**, así que el script las reporta `SIN PAYLOAD 0` incluso cuando
tienen payload real. Verificado con el propio script: las 17 entradas nuevas
de esta sesión, más las de D-2 (ENASEM/ENDUTIH/MOCIBA) y de una sesión previa
a D-2 (ENDIREH), aparecen listadas al final del reporte bajo "Entradas del
manifiesto NO atribuidas a ninguna de las 43 operables" — no son basura, son
las siete fuentes con `MAPA[...]=[]`.

**Corrección manual, derivada del propio manifiesto** (no de memoria):
removiendo las 7 claves con `MAPA[...]=[]` del recuento de 30 — porque las 7
tenían payload real ya para cuando corrí el script (4 de antes de esta
sesión: ENASEM/ENDIREH/ENDUTIH/MOCIBA; 3 de la Parte A de este mismo acto:
ENSU/ENBIARE/ENASIC, registradas antes de correr `cruce_operables.py`) —
quedan **23 operables sin payload de verdad, tras la Parte A de este acto**:

ACS · CLUES · CNGF · CNGMD · CONEVAL · CPS · ECOVID-ML · EDER · EDR · EIC ·
ELCOS · ENAPROCE · ENCUP · ENFIH · ENPOL · ENSAFI · ENTI · ESTADÍSTICA
EDUCATIVA · ESTADÍSTICAS DE NATALIDAD / NA · GLOBAL FINDEX DATABASE · INE ·
REGISTROS ADMINISTRATIVOS DE E · SAEH

### Diferencia contra la lista de julio (`2026-07-31-cola-descarga-rederivada.md:43`, 27 nombres)

Julio: ACS · CNGF · CNGMD · CPS · ECOVID-ML · EDER · EDR · EIC · ELCOS ·
ENAPROCE · **ENASEM** · **ENBIARE** · **ENASIC** · ENCUP · **ENDIREH** ·
**ENDUTIH** · ENFIH · ENPOL · ENSAFI · **ENSU** · ENTI · Estadística
educativa · Estadísticas de natalidad · Global Findex · **MOCIBA** ·
Registros administrativos · SAEH.

- **Salieron de la lista antes de que este acto arrancara** (payload real ya
  en manifiesto, invisible al cruce por el defecto de §7): ENASEM (D-2),
  ENDUTIH (D-2), MOCIBA (D-2), ENDIREH (sesión anterior a D-2, no
  identificada por esta nota — ya estaba en el manifiesto al arrancar).
- **Entradas nuevas, no estaban en julio** (catálogo v1.0 → v2.0, el encargo
  ya avisó de este cambio): CONEVAL, CLUES, INE. Las tres son operables
  (micro=sí, libre=sí) en `catalogo_unico.json` vigente.
- **27 − 4 resueltas + 3 nuevas = 26** al arrancar este acto (antes de Parte
  A). Después de Parte A (ENSU, ENBIARE, ENASIC resueltas) quedan las 23
  reportadas arriba.

## 2 · Parte A — re-sondeo y descarga de las tres ya resueltas

Las tres URLs, citadas de `forense/notas/2026-08-04-barrido-alcanzabilidad-27fuentes.md`
§3 (ENSU, línea 100-101) y §5 (ENBIARE/ENASIC, tabla líneas 152-156):

| Fuente | Content-Range citado (4/ago, nota previa) | Content-Range re-sondeado (este acto) |
|---|---|---|
| ENSU (`ensu_bd_2025_csv.zip`) | `0-0/12332522` | `0-0/12332522` — **coincide, sin drift** |
| ENBIARE 2021 (`enbiare_2021_base_de_datos_csv.zip`) | `0-0/5684658` | `0-0/5684658` — **coincide, sin drift** |
| ENASIC 2022 (`enasic_2022_bd_csv.zip`) | `0-0/2289078` | `0-0/2289078` — **coincide, sin drift** |

Diccionario/FD, resuelto vía `archivoscompaginacion` (`tipodocto=0`), no
verificado por la nota citada (lo declaraba explícitamente pendiente):

- **ENBIARE 2021**: FD real, dos formatos (pdf/xlsx) — bajado el PDF,
  `Content-Range 0-0/997663`, coincide con lo bajado.
- **ENASIC 2022**: FD real, un formato (xlsx) — `Content-Range 0-0/266488`,
  coincide con lo bajado.
- **ENSU**: el API declara FD para 14 ediciones (2013–2026, todas con
  `pathLogico` real bajo `/programas/ensu/doc/ensu_fd_{año}`). Probadas 4
  (2025, 2024, 2023, 2021): las 4 resuelven a **SOFT-404** (2263 B, "Página
  no encontrada" — la firma de `/contenidos/...`, no la de `/programas/...`).
  4/4 con la misma firma es señal suficiente sin cruzar a adivinar más
  variantes (mismo criterio que D-2 aplicó a ENASEM 2001/2003/2012). **FD de
  ENSU no publicado bajo el patrón que el propio API declara** — no es "no lo
  encontré", es una discrepancia reproducible entre lo que el catálogo de
  archivos anuncia y lo que el servidor sirve. Se baja solo la base.

**Bajado y registrado** (`tests/manifiesto.py --registra`, sha256/tamaño
derivados del archivo, no tecleados):

| id | Bytes | `--verifica` |
|---|---|---|
| `ensu2025_bd_csv_zip` | 12 332 522 | COINCIDE |
| `enbiare2021_bd_csv_zip` | 5 684 658 | COINCIDE |
| `enbiare2021_fd_pdf` | 997 663 | COINCIDE |
| `enasic2022_bd_csv_zip` | 2 289 078 | COINCIDE |
| `enasic2022_fd_xlsx` | 266 488 | COINCIDE |

## 3 · Parte B — mecanismo, y las cuatro clases (más una quinta nombrada)

**Descubrimiento de slug de portal, declarado explícitamente para no
confundirlo con "adivinar por analogía".** El encargo prohíbe construir URLs
de *archivo* por analogía de sufijo/año. Lo que sí se hizo, una vez por
fuente, fue probar `/programas/{acrónimo en minúsculas}/` como primer sondeo
de portal — **no es una variación de una URL de archivo ya conocida; es la
misma convención de nombrado de portal que este corpus ya confirmó 7/7 veces
antes de este acto** (ensu, enasem, enbiare, enasic, endutih, mociba, endireh
— los siete acrónimos ya resueltos usan literalmente `acrónimo.lower()` como
slug). Donde el primer sondeo no resolvió a una página real, **no se probó
ninguna variante** — se clasificó con lo que el servidor devolvió. Se intentó
un índice de programas de INEGI (`/programas/`) para evitar adivinar del
todo; resultó ser un SPA sin listado estático (8158 B, `compLista.min.js`) —
no se invirtió tiempo en revertir su API de listado no documentada.

Mecanismo completo por fuente resuelta: sondeo de portal (a veces vía un stub
de redirección JS que el propio servidor declara, `window.location=...` o
`vredirect(...)` — se sigue el destino que el servidor nombra, no se inventa
uno) → `idm`/`idBiinegi` → API `archivoscompaginacion` (`tipodocto=0`) →
`pathLogico`+`extensión` reales → sonda `-r 0-0` antes de bajar.

**Las cuatro clases del encargo, y una quinta nombrada donde ninguna de las
cuatro describe lo que pasó** (D-2 estrenó la escala en
`2026-08-04-d2-descargas-endutih-mociba-enasem.md` §2, este acto la aplica
al resto):

| # | Fuente | `idBiinegi`/`idm` | Vía de portal | Clase | Detalle (http_code / bytes) | Bajado |
|---|---|---|---|---|---|---|
| 1 | ENSAFI 2023 | 3364 | stub JS → `/2023/` | **ARCHIVO REAL** (BD) | 206, `Content-Range 0-0/5027338` | Sí (BD) |
| — | ENSAFI 2023 FD | 3364 | (vía API) | **SOFT-404** | 200, 2263 B, "Página no encontrada" | No |
| 2 | ENPOL 2021 | 3119 (idm sin comillas — variante no vista antes) | stub JS → `/2021/` | **ARCHIVO REAL** (BD+FD) | 206/206, `0-0/35914746` · `0-0/3945038` | Sí |
| 3 | ENFIH 2019 | 3099 | stub JS → `/2019/` | **ARCHIVO REAL** (BD+FD) | 206/206, `0-0/4404049` · `0-0/202396` | Sí |
| 4 | ENTI 2022 | 3327 | stub JS `vredirect()` → `/2022/` | **ARCHIVO REAL** (BD+FD) | 206/206, `0-0/18671874` · `0-0/1760381` | Sí |
| 5 | EDER 2025 | 3463 | stub JS → `/2025/` | **ARCHIVO REAL** (BD+doc) | 206/206, `0-0/15399361` · `0-0/4380365` | Sí |
| 6 | EDR (defunciones) | 3358 | directo, sin stub | **ARCHIVO REAL** (BD 2024; FD no publicado por separado — 43 archivos listados, ninguno titulado "Descriptor de archivos") | 206, `0-0/28238311` | Sí (BD) |
| 7 | ELCOS 2012 | 1729 | stub JS → `/2012/` | **ARCHIVO REAL** (BD+FD; ambigüedad de construcción de URL resuelta por sonda, ver nota) | 206/206, `0-0/3902958` · `0-0/293376` | Sí |
| 8 | CNGF 2025 | 3486 | stub JS → `/2025/` | **ARCHIVO REAL, estructural** — API enumera 31 archivos reales (`datosabiertos`/`tabulados`), sin patrón único "base+FD" (censo de gobierno federal, no encuesta de hogar) | no verificado byte a byte — ver §4 | No (diferido) |
| 9 | CNGMD 2025 | 3430 | stub JS → `/2025/` | **ARCHIVO REAL, estructural** — 148 archivos enumerados, mismo patrón que CNGF | no verificado | No (diferido) |
| 10 | ENAPROCE 2018 | 2923 | stub JS → `/2018/` | **QUINTA CLASE: responde, microdato real no publicado** — el API enumera 16 archivos; los únicos con "base" en el título son "Ejemplo de la base de datos **con valores alterados**, solo permite mostrar las características de ésta y probar algoritmos" (Microempresas, Pymes) — dato sintético declarado como tal por el propio portal, no un microdato real. El resto son `datosabiertos` (agregados) y `tabulados`. | 200 (portal), API responde | No |
| 11 | ECOVID-ML | — | — | **SOFT-404** | 200, 13 370 B, "Página no encontrada" | No |
| 12 | EIC 2015 | — | — | **SOFT-404** | 200, 13 370 B, "Página no encontrada" | No |
| 13 | CONEVAL | — | — | **SOFT-404** (probado pese a la nota del catálogo sobre absorción por INEGI 17/jul/2025 — el portal `/programas/coneval/` no existe bajo ese slug) | 200, 13 370 B | No |
| 14 | ENCUP (vía INEGI) | 1761 (real, portal existe) | directo | **SIN MECANISMO** (para esta vía) — portal INEGI real (idm=1761), pero `archivoscompaginacion` devuelve 0 archivos para `idBiinegi=1761` | 200 (portal) / 0 items (API) | No |
| 14b | ENCUP (vía SEGOB, ya documentada) | — | — | **RESPONDE, re-verificado, con la misma salvedad de cadena TLS ya declarada** (`2026-08-04-barrido-alcanzabilidad-27fuentes.md` §4) — `Content-Range 0-0/4814178` coincide exacto con lo ya registrado; sin `-k` el handshake falla (`unable to get local issuer certificate`, código curl 60); con `-k` (solo diagnóstico) confirma | — | **No** — bajar con `-k` entraría al corpus permanente sin verificación de cadena TLS; mismo criterio de `tests/manifiesto.py` (`no abre ningún socket ni valida TLS a ciegas`) y del propio `2026-08-04-d2-descargas-endutih-mociba-enasem.md` (`un script de este repo bajando de una URL con TLS sin verificar es exactamente el tipo de riesgo que el resto del proyecto trata con sospecha`). Se declara resuelto, se deja la decisión de forzarlo a mesa. |
| 15 | CLUES (DGIS/Salud) | — | — | institución distinta, mecanismo INEGI no aplica; ping mínimo de reachability al dominio (`dgis.salud.gob.mx`, `www.dgis.salud.gob.mx`) — mismo patrón de cadena TLS incompleta que SEGOB (`curl` sin `-k`: código 60). No se forzó `-k` — no hay vía de enumeración de archivos conocida para este portal, forzar TLS sin poder listar nada no compra nada. | curl exit=60 | No |
| 16 | SAEH (DGIS/Salud) | — | — | mismo que CLUES — mismo dominio, mismo hallazgo | curl exit=60 | No |
| 17 | ACS | — | — | institución distinta (U.S. Census Bureau), mecanismo INEGI no aplica por definición — no hay `idBiinegi` para una fuente no-INEGI. Host fuera del alcance de red de este entorno (no está en la lista de hosts permitidos del sandbox). No se intentó. | — | No |
| 18 | CPS | — | — | ídem ACS (U.S. Census Bureau / BLS) | — | No |
| 19 | GLOBAL FINDEX DATABASE | — | — | institución distinta (Banco Mundial/Gallup), mismo criterio que ACS/CPS | — | No |
| 20 | INE | — | — | institución distinta (Instituto Nacional Electoral, órgano autónomo, portal propio), mismo criterio | — | No |
| 21 | ESTADÍSTICA EDUCATIVA | — | — | institución distinta (SEP); el nombre del catálogo es una categoría temática, no un acrónimo de programa — este acto no adivina el slug real. No explorado. | — | No |
| 22 | ESTADÍSTICAS DE NATALIDAD / NA | — | — | nombre de categoría, no acrónimo — mismo criterio, no explorado (aunque la institución primaria es INEGI, a diferencia de EDUCATIVA) | — | No |
| 23 | REGISTROS ADMINISTRATIVOS DE E[stadísticas vitales y nupcialidad] | — | — | mismo criterio — nombre de categoría, no acrónimo, no explorado | — | No |

**Nota sobre ELCOS, la ambigüedad de construcción de URL:** el `pathLogico`
que el API devolvió (`/programas/elcos/microdatos/ELCOS_BD`, extensión
`dbf`) no incluye año, y la extensión del FD es `xls` (Excel legado, nunca
visto antes en este corpus — todo lo anterior era `pdf`/`xlsx`). La regla de
construcción documentada ("`pathLogico`+`_`+`extensión`+`.zip` para formatos
de dato; sin `.zip` si la extensión ya es `pdf`/`xlsx`") no decía qué hacer
con `xls`. Se sondearon **las dos construcciones posibles para cada archivo**
(con/sin `.zip`) antes de bajar cualquiera — no se adivinó, se verificó: BD
real con `_dbf.zip` (variante sin zip dio soft-404); FD real con `.xls` sin
zip (variante con `_xls.zip` dio soft-404). `xls` se comporta como
`pdf`/`xlsx`, no como formato de dato.

## 4 · Lo que queda para después, con URL ya verificada

- **ENCUP (SEGOB)**: `https://fomentocivico.segob.gob.mx/work/models/FomentoCivico/Documentos/PDF/CultDemo/BaseDatos_ENCUP_2012_Final.xlsx`
  — `Content-Range bytes 0-0/4814178`, re-verificado esta sesión, coincide
  exacto con `2026-08-04-barrido-alcanzabilidad-27fuentes.md` §4. Bloqueado
  solo por cadena TLS incompleta del servidor — decisión de forzar `-k` para
  entrar al corpus permanente queda para mesa.
- **CNGF 2025 / CNGMD 2025**: portal y API reales y enumerados (31 y 148
  archivos respectivamente, todos `datosabiertos`/`tabulados`, ninguno
  verificado byte a byte). Estructura de datos distinta a la de encuesta de
  hogar (censo de gobierno, muchos módulos temáticos) — el siguiente acto
  necesita decidir qué módulo(s) bajar, no solo ejecutar; se deja con la URL
  base y el listado completo disponible vía
  `archivoscompaginacion?idBiinegi=3486` (CNGF) / `3430` (CNGMD).
- **CLUES / SAEH**: dominio `dgis.salud.gob.mx` contactable pero con la misma
  falla de cadena TLS que SEGOB; sin mecanismo de enumeración de archivos
  conocido para ese portal. Necesitaría una sesión que investigue la
  estructura real del portal DGIS antes de intentar nada.

## 5 · Declaración ADR-46 (contaminación de estructura, declarar de más)

Estructura explorada esta sesión (parámetros de API, `pathLogico`,
`idBiinegi`/`idm`, tamaños vía `Content-Range`, títulos de archivo
publicados) para: **ENSU, ENBIARE 2021, ENASIC 2022** (Parte A) y
**ENSAFI, ENPOL, ENFIH, ENTI, EDER, EDR, ELCOS, CNGF, CNGMD, ENAPROCE,
ECOVID-ML, EIC, CONEVAL, ENCUP** (Parte B, INEGI e — para ENCUP — también
SEGOB). Además, un ping de conectividad sin enumeración a
`dgis.salud.gob.mx`/`www.dgis.salud.gob.mx` (institución de CLUES/SAEH) y una
lectura del índice general `/programas/` de INEGI (SPA sin listado, no
específico de ninguna fuente del corpus).

**Cero apertura de contenido en las 17 fuentes.** Ningún ZIP se extrajo,
ningún PDF/XLSX/XLS/DBF/CSV se abrió con ninguna librería ni se leyó como
texto. Verificación exclusivamente por `Content-Type`/`Content-Range` antes
de bajar y `sha256`/tamaño de archivo completo después — nunca por
inspección de contenido.

Por ADR-46(2)-(3), esta sesión **queda parcialmente contaminada para
pre-registrar** contra: ENSU, ENBIARE, ENASIC, ENSAFI, ENPOL, ENFIH, ENTI,
EDER, EDR, ELCOS, CNGF, CNGMD, ENAPROCE, ECOVID-ML, EIC, CONEVAL, ENCUP — no
"limpia y habilitada" sin matiz. No se tocaron ENIGH, ENVIPE, ENOE ni ningún
otro host fuera de esta lista.

## 6 · Verificación desde worktree hermano

Los 17 archivos de esta sesión (5 de Parte A + 12 de Parte B) verificados
**visibles y con sha256 recalculado independientemente** desde
`/home/pc0/mm-d2-descargas` (mismo symlink `data/raw -> /home/pc0/mm-corpus/raw`):
17/17 coinciden dígito por dígito contra lo que `--registra` escribió en
`data/manifiesto.yaml` de este worktree. El defecto de PR #77 (payloads que
se quedan solo en el worktree local) no se reprodujo.

## 7 · Hallazgos de instrumento (una línea cada uno, no impidieron medir)

1. **`tests/bitacora.py` reporta la versión de instrucciones vigente leyendo
   el archivo hardcodeado `instrucciones-proyecto-v2.md` (línea 124), que
   quedó congelado en contenido v2.3** desde que el proyecto empezó a
   versionar por nombre de archivo nuevo (`instrucciones-proyecto-v2_4.md`,
   incorporado verbatim por ADR-59, 4/ago). El script nunca sigue el cambio
   de nombre — reportará v2.3 como "vigente" indefinidamente aunque exista
   una v2.5, v2.6, etc. No bloqueó esta sesión (v2.4 ya estaba cargada y
   verificada independientemente vía ADR-59 + contenido del archivo real).
2. **`tests/cruce_operables.py` tiene siete claves de `MAPA` con lista de
   prefijos vacía** (`ENASEM`, `ENDIREH`, `ENDUTIH`, `MOCIBA`, `ENSU`,
   `ENCUESTA NACIONAL DE BIENESTAR`, `ENCUESTA NACIONAL PARA EL SIST`) —
   `pertenece()` nunca les atribuye una entrada del manifiesto sin importar
   qué exista, así que el resumen del script siempre las reporta `SIN
   PAYLOAD 0` incluso con payload real. Detallado en §1. Corregido a mano
   para este acto (no se editó `tests/`, fuera de perímetro); afecta a
   cualquier sesión futura que confíe en el resumen del script sin
   contrastar contra la lista de "no atribuidas" que el mismo script imprime
   al final.
3. **`git worktree add` dio dos errores transitorios de `.git/config` "Device
   or resource busy"** al crear el worktree de este acto — verificado que no
   corrompió nada (§0). Probable contención de escritura concurrente entre
   sesiones que comparten el mismo `.git/`; no se investigó más a fondo,
   fuera de perímetro.

## 8 · Suite

```
$ python3 tests/check.py --baseline
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

Idéntico al resultado de D-2 (misma línea base, mismo HEAD congelado) — este
acto no introdujo ningún FAIL/WARN nuevo.

## Prohibiciones respetadas

No se construyó ninguna URL de *archivo* por analogía de sufijo/año — todas
las URLs finales salen de `pathLogico`/`extensión` que el propio API
`archivoscompaginacion` declaró, o de un destino de redirección que el propio
servidor nombró (stub JS). El único elemento "adivinado" fue el slug de
*portal* (`acrónimo.lower()`), aplicando una convención ya confirmada 7/7
veces antes de este acto, con un solo intento por fuente y sin variantes
cuando no resolvió. No se usaron portales con registro ni se aceptaron
términos. No se bajó ningún archivo sin sonda `-r 0-0` previa. No se abrió
ningún ZIP/PDF/XLSX/XLS/DBF/CSV. No se tocó `milpa/`, `canon/`, `tests/` ni
`forense/hitoD-preregistro`. No se re-clasificó ninguna ficha del Hito D. No
se corrigió el defecto de `--verifica` (un `--id` por invocación, respetado
en las 17 verificaciones de este acto). No se forzó `-k` para entrar
contenido sin verificación de TLS al corpus permanente (ENCUP/SEGOB,
CLUES/SAEH) — declarado, no resuelto, queda para mesa.
