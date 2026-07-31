# Cola de descarga re-derivada + campaña priorizada (Encargo D)

Sesión Sonnet, Ubuntu, rama `sesion/descarga-dirigida`. Base: `origin/main` al fast-forward
(`ba44c25`), 47 commits por delante de donde arrancaba esta rama — se sincronizó antes de
derivar cualquier cifra, porque varias de esas 47 (`sesion/enut`, `sesion/p1-enigh-semilla`,
`infra/data-raw-externa`, `adr/motor-abm-ajuste`, entre otras) cambian directamente los números
que este encargo pide verificar.

## 0 · Procedencia de las premisas, verificadas

| Premisa del encargo | Resultado de verificarla |
|---|---|
| 119 únicas / 38 operables / 32 sin bajar al 30/jul | `catalogo.py`+`dedup.py` (regenerados en esta sesión, §1): **RECETA consistente**, 119 y 38 confirmados. El "32 sin bajar" era el corte del 30/jul (`data/catalogo-fuentes-v1_0.md`, estático, no se edita aquí); al 31/jul, tras sincronizar, son **27 sin payload + 2 parcial** (§2) — la cifra bajó porque `sesion/enut` bajó ENUT en el ínterin, no porque este cruce sea distinto del suyo. |
| Cruce parcial del chat: 9 familias en manifiesto; CPV/ENADID/ENASEM/ENDIREH/ENSU sin payload | **Parcialmente refutado.** Antes de sincronizar con `origin/main`, el cruce completo daba 8 familias (sin ENUT) y 6 sin payload de esa lista (con ENUT sumado a la lista de faltantes que el parcial no vio). Después de sincronizar, coincide en 9 y en los 5 nombrados — pero por una razón que el parcial no podía saber (ENUT se bajó *durante* la ventana de este encargo, en otra rama). El cruce completo de §2 es el que hay que citar, no el parcial. |
| Cola de Hito E existe y está vencida (criterio caído con ADR-49; 3 posiciones ya en disco) | **Confirmado, con la cifra exacta verificada.** Existe en `forense/hitoE-campana-medicion-v2_0.md` §"Cola priorizada" (10 posiciones). De esas 10, **3 ya están en disco** tras la sincronización: `ENOE` (puesto 1), `ENUT` (puesto 7), `ENSANUT` (puesto 8) — verificado contra el cruce de §2, no contra la nota. El criterio que ponía a `ENOE` en el puesto 1 pese a desbloquear menos filas que otras cuatro (`unico_calibrable_hoy`, "única elasticidad calibrable con dato público") fue retirado por **ADR-49, D1** (`canon/gobernanza-v1_15.md:433`) el mismo 31/jul, sobre evidencia de reactivo (`forense/notas/2026-07-31-cal-enoe-fasea.md`: ningún cuestionario ENOE/ENOEN trae ahorro/crédito/deuda). La cola vieja se referencia, no se edita ni se hereda — ver §3 para el criterio nuevo. |
| Red a INEGI alcanzable desde Ubuntu | **RESPONDE**, confirmado por `curl -sI` esta sesión contra `www.inegi.org.mx` (raíz, `/programas/ccpv/2020/`, `/programas/enadid/{2018,2023}/`, `/programas/{endireh/2021,enasem/2021,ensu/2025}/datosabiertos/`, catálogo `/rnm/`). Ningún caso de NO ALCANZABLE (sin 403 de egreso, sin CONNECT rechazado, sin error de cadena TLS). Detalle del mecanismo real en §4. |

## 1 · Regeneración de receta (obligatoria antes de cualquier cifra)

```
$ python3 tests/catalogo.py   → RECETA: consistente (10/10 archivos, crudo==parseado)
$ python3 tests/dedup.py      → ENTRADAS: 183  ·  FUENTES ÚNICAS: 119  ·  OPERABLES: 38
                                 MICRODATOS: sí=52 no=32 ?=35
```

`tests/dedup.py` traía un bug que hacía crashear su propio cruce contra el manifiesto
(`re.match(r'^[a-z]+', i).group(0)` sobre ids que empiezan con dígito — los cinco de
ENSANUT con prefijo numérico, `1_vfinal_...`). Corregido en esta sesión (`m := re.match(...)`,
salta el id si no matchea) para que el script complete y no se pierda el resto de su salida;
no cambia ninguna cifra de las que ya imprimía antes del crash. Sigue siendo un cruce por
prefijo (grueso); el cruce real de este encargo es `tests/cruce_operables.py`, nuevo (§2).

## 2 · Cruce completo, 38 operables (parser declarado, no greps)

`tests/cruce_operables.py` (nuevo). Mapa explícito acrónimo→prefijos de `id` en
`data/manifiesto.yaml` (los ids no siguen una convención mecánica única — no hay forma de
derivarlo sin declarar el mapa a mano una vez). Resultado, corrido en esta sesión:

| Estado | Cuenta | Acrónimos |
|---|---|---|
| **EN MANIFIESTO** (microdato con payload) | **9** | ENCIG (15) · ENCUCI (2) · ENIF (9) · ENIGH (6) · ENNVIH (27) · ENOE (36) · ENSANUT (24) · ENUT (16) · ENVIPE (32) |
| **PARCIAL** (solo instrumento/cuestionario, sin base de microdatos) | **2** | CPV (1 — bajado esta sesión, §5) · ENADID (2 — bajados esta sesión, §5) |
| **SIN PAYLOAD** | **27** | ACS · CNGF · CNGMD · CPS · ECOVID-ML · EDER · EDR · EIC · ELCOS · ENAPROCE · ENASEM · Encuesta Nacional de Bienestar (ENBIARE) · Encuesta Nacional para el Sistema de Cuidados (ENASIC) · ENCUP · ENDIREH · ENDUTIH · ENFIH · ENPOL · ENSAFI · ENSU · ENTI · Estadística educativa · Estadísticas de natalidad · Global Findex · MOCIBA · Registros administrativos de estadísticas vitales · SAEH |

**Cifra para el "al volver": 27 de 38 operables sin payload de verdad**, contando CPV/ENADID
como PARCIAL (instrumento sí, microdatos no) en vez de SIN PAYLOAD. Antes de que esta sesión
bajara nada (justo después de sincronizar con `origin/main`, antes de §5) eran **29 de 38**
SIN PAYLOAD y 9 EN MANIFIESTO — la sesión movió dos posiciones de SIN PAYLOAD a PARCIAL, no a
EN MANIFIESTO: la base de microdatos de ninguna de las dos se bajó (§5). El cruce completo
también separa, sin colapsar, las **35 fuentes con microdatos indeterminado** al
corte del catálogo (listadas en `data/catalogo-fuentes-v1_0.md` §"Las 35 indeterminadas";
regeneradas aquí como el mismo 35 vía `dedup.py`) — no entran a la cola (su estatus operable no
está decidido), y su verificación pendiente es trabajo de catálogo (consulta de página), no de
descarga.

7 entradas del manifiesto no se atribuyen a ninguna de las 38 (los 5 `DescargaMasiva_*.zip` sin
identificar — contienen solo el instalador genérico de escritorio de INEGI, no un payload de
encuesta, per `forense/notas/2026-07-31-enut-descarga.md` Parte 2 — y 2 entradas de nota sin
payload). No se abrieron para identificarlos: es exactamente la lectura que ADR-46 prohíbe a
esta sesión.

`data/catalogo-fuentes-v1_0.md` (§"Operables ya en manifiesto: 6", "NO bajadas: 32") queda
desactualizado por esta sesión — describe el corte del 30/jul, antes de que `ENOE`/`ENUT`/
`ENSANUT` se bajaran. No se edita (no es mandato de este encargo, y no es canon ni manifiesto);
queda declarado aquí como hallazgo para quien lo lea después.

## 3 · Cola priorizada, criterio declarado

**El orden no es completar el catálogo.** Es lo que el programa post-sello (medición, no
canon — `forense/hitoE-campana-medicion-v2_0.md`) necesita, en orden de uso:

| # | Fuente | Para-qué (post-sello) |
|---|---|---|
| **(a)** | **CPV** — cuestionario ampliado | Candidata obvia para marginales de los 6 ejes de perfil. Verificado (`data/inventarios/*`, 4 menciones independientes): el producto que las trae es la **muestra del cuestionario ampliado** (≈4M viviendas, 103 preguntas, CSV/DBF/SAS/SPSS/Stata con diccionarios), no el cuestionario básico (enumeración exhaustiva, sin muestra). Instrumento bajado esta sesión (§5); microdatos siguen pendientes. |
| **(b)** | **ENADID** — migración con referencia temporal explícita | ENIGH (semilla IPF, P1) queda **EN CONJUNTA con límite declarado** en el eje de condición migratoria: `forense/notas/2026-07-31-p1-enigh-semilla.md:61` — ni el diccionario ni los metadatos de ENIGH traen el texto literal de la pregunta de residencia, así que no se puede confirmar si la referencia temporal es "hace 5 años" o "al nacer" sin el cuestionario, que no viene en el ZIP de ENIGH. ENADID es la fuente del catálogo dedicada a dinámica demográfica/migración con cuestionario propio — cierra ese hueco. Los dos cuestionarios (hogar + módulo mujer) bajados esta sesión (§5); base de microdatos pendiente. |
| **(c)** | *(vacío, declarado)* | Se buscó un veredicto de Encargo C que nombrara fuentes no bajadas (`grep` de CPV/ENADID/ENASEM/ENDIREH/ENSU contra `forense/*.md`): solo aparecen en `hitoE-campana-medicion-v2_0.md` (ya cubierto en (a)/(b)/resto) y en `meta-auditoria-comunicacion.md` (auditoría de proceso, no nombra fuentes a bajar). Ningún veredicto de falsación (`hitoD-R1_1`/`hitoD-R3_2-veredicto`) nombra una fuente sin bajar — son veredictos sobre reglas del motor, no sobre datos. No se fabrica una posición aquí. |
| **(d)** | *(resuelto antes de que esta sesión llegara)* | CAL-CONF Fase A (`forense/notas/2026-07-31-cal-conf-fasea.md` §"Límite declarado") citó `encig23_estructura_base_datos.pdf` como registrado en el manifiesto pero ausente de los tres worktrees vivos. Verificado con `tests/manifiesto.py --verifica --id encig23_estructura_base_datos_pdf` en esta sesión: **COINCIDE** — sha256 y tamaño (3 100 802 bytes) verificados contra disco. Ya fue recuperado por otra sesión (`infra/data-raw-externa`, merge `c87a146`, hallazgo "RECUPERADO" en `forense/hallazgos.md`) antes de que esta sesión sincronizara. Nada que bajar aquí. |
| **(e)** | El resto de operables (27, listadas en §2) | Sin urgencia fabricada: sin para-qué post-sello declarado en ningún artefacto leído esta sesión. Se listan en §2, sin posición. |

## 4 · Mecanismo de red, verificado esta sesión (extiende `2026-07-31-perimetro-descarga.md`)

`www.inegi.org.mx` RESPONDE en todos los casos sondeados. Pero **cada portal `/programas/
{prog}/{año}/` (incluidos `ccpv/2020`, `enadid/{2018,2023}`, `endireh/2021`, `enasem/2021`,
`ensu/2025`) es la misma SPA** ya documentada para ENOE/ENIF/ENVIPE/ENCIG: cualquier subruta
bajo ese path devuelve el mismo shell de 13 370 bytes (mismo `ETag`), sin `href` real en el
HTML crudo — RESPONDE, pero solo un navegador (o el mecanismo de abajo) le saca el enlace.

**Corrección a mi propio intento inicial de concluir "hace falta navegador":** `forense/
hallazgos.md` (dos entradas del 31/jul, líneas ~33/35) ya documenta que la SPA sí es navegable
sin navegador, vía dos endpoints JSON internos:
- `.../data/arbol/arbolData.js` — árbol completo de la pestaña Documentación, con URLs reales
  (`/programas/{prog}/{año}/doc/...` o `/contenidos/programas/{prog}/{año}/doc/...` según el
  programa). **Usado esta sesión** para CPV y ENADID (§5).
- `/app/api/descarga/componente/descargamasiva/lista/archivoscompaginacion?idBiinegi=...` —
  pestaña Microdatos (la base de datos real). **Intentado esta sesión, sin éxito.** El
  componente que sirve CPV/ENADID (`descargaMasivaV2.min.js`) exige además `tema`, `subtema`,
  `areaGeografica`, `proyecto`, `anio` y `agrupacion` (base64 de "Todas"); ninguno de `proyecto`/
  `anio` aparece como atributo `data-*` en `pestanadata.js` de estos dos portales (a diferencia
  de `idBiinegi`/`tipoinformacion`, que sí). Probadas ocho combinaciones (`proyecto`∈{0,"pob",""}
  × `anio`∈{0,2020,""}, más `tipodocto` vs. `tipoinformacion`): las que incluyen `tipodocto=4`
  con `proyecto=0` devuelven `HTTP 200 {"success":false,"error":true}` (el endpoint procesa la
  petición pero la rechaza); el resto, `HTTP 204` silencioso. No se encontró la combinación que
  sirve contenido. La nota de ENUT (`forense/notas/2026-07-31-enut-descarga.md` §"Mecanismo de
  descubrimiento") ya advertía justo esto: sin `pestanadata.js` de esa página específica **con
  los atributos completos**, no hay forma de derivar esos parámetros sin ejecutar el JS de
  verdad. Para CPV/ENADID, `pestanadata.js` no trae `data-proyecto`/`data-anio` — un paso más
  atrás que ENUT. **No se corrigió por fuerza bruta de parámetros** (habría sido exactamente el
  tipo de exploración sin límite que este encargo pide evitar); queda declarado como el bloqueo
  concreto para la próxima sesión, no como "hace falta navegador" (eso ya está refutado).
- `catalog/{id}/download/{n}` del RNM (`/rnm/index.php/catalog/`) **para ENDIREH (801), ENADID
  (981), ENASEM (861), ENSU (1100)** verificados esta sesión: son navegables por curl y sirven
  archivos reales (`Content-Type: application/octet-stream`, `Content-Disposition: attachment`),
  pero el nombre (`IPE_CV-EE-IC_*`) y el propio catálogo los declaran "Diccionario de datos de
  las tablas de indicadores" — **el mismo producto-señuelo ya documentado para ENOE/catálogo
  1121** (tablas de indicadores agregados con su margen de error, no microdatos). No se
  registraron: registrarlos como si fueran microdato de la encuesta habría sido exactamente el
  error que la nota original de ENOE ya advirtió.

Ningún host externo a `inegi.org.mx` se tocó (Global Findex/World Bank, LAPOP/Vanderbilt,
Latinobarómetro, ACS/CPS del Census Bureau, MHAS): fuera del alcance de red de esta sesión
(sandbox restringido a `*.inegi.org.mx` y unos pocos hosts no relacionados con datos MX) y fuera
de lo que la premisa 4 pidió verificar (solo INEGI). `inventario-fuentes-migracion-mexico.md`
y otros sí registran `https://www.mhasweb.org/` como espejo de ENASEM, no INEGI — queda anotado
para una sesión con ese host en su perímetro de red, no se persiguió aquí.

## 5 · Descarga y registro (payload → `--registra` → `--verifica`)

| id | Archivo | Origen | sha256 (primeros 12) | Bytes | `--verifica` |
|---|---|---|---|---|---|
| `cpv2020_cuestionario_ampliado_pdf` | `Censo2020_cuest_ampliado.pdf` | `.../contenidos/programas/ccpv/2020/doc/Censo2020_cuest_ampliado.pdf` | `4a88b9b7a3e8` | 986 778 | COINCIDE |
| `enadid2023_hogar_cuestionario_pdf` | `hogar_enadid23.pdf` | `.../contenidos/programas/enadid/2023/doc/hogar_enadid23.pdf` | `8b046a68dc19` | 997 178 | COINCIDE |
| `enadid2023_mujer_modulo_cuestionario_pdf` | `mujer_enadid23.pdf` | `.../contenidos/programas/enadid/2023/doc/mujer_enadid23.pdf` | `005a9e83fff2` | 943 319 | COINCIDE |

Las tres URLs se localizaron en `data/arbol/arbolData.js` de cada portal (árbol real de la
pestaña Documentación, no adivinado) y se verificaron con `curl -sI` (`Content-Type:
application/pdf`, tamaño exacto) antes de bajar. Las tres `--registra`n limpio (sin colisión de
id ni de sha256) y las tres `--verifica` dan COINCIDE contra `data_raw`.

**Lo que NO se bajó, y por qué, con palabras distintas:**
- **CPV — base de microdatos (muestra del cuestionario ampliado, CSV/DBF/SAS/SPSS/Stata).**
  RESPONDE PERO EL ENDPOINT DE MICRODATOS RECHAZA LA PETICIÓN (§4) — no NO ALCANZABLE, no SIN
  RECURSO: el recurso existe (es el mismo que otra sesión bajó para ENOE/ENIF/ENVIPE/ENCIG por
  este mecanismo), pero esta sesión no derivó los parámetros `proyecto`/`anio` que ese portal
  específico exige.
- **ENADID — base de microdatos (mismo mecanismo, mismo bloqueo).**
- **ENDIREH, ENASEM, ENSU — nada bajado.** No estaban en (a)/(b); el RNM sí expone algo con su
  nombre pero es el producto-señuelo de tablas de indicadores (§4), no microdato; no se
  registró nada bajo esos acrónimos.
- **Ningún fallo de red (host inalcanzable, TLS, 403, timeout) ocurrió esta sesión.** Todo lo
  no bajado fue RESPONDE-pero-mecanismo-sin-resolver, nunca NO ALCANZABLE.

Ningún payload de microdato se abrió más allá de lo necesario para confirmar
`Content-Type`/tamaño por HEAD (ADR-46). Los dos cuestionarios/instrumento sí se hojearon lo
mínimo para nombrarlos correctamente en `usado_para` (título de sección, no contenido de
reactivo) — no se leyó ninguna pregunta de fondo más allá de lo que la §3(b) ya cita del
inventario.

## Prohibiciones respetadas

`canon/` no se tocó. La cola de Hito E (`forense/hitoE-campana-medicion-v2_0.md`) se referencia
en §0/§3, no se edita. Ninguna cifra de este documento se tecleó sin regenerar
`catalogo.py`/`dedup.py`/`cruce_operables.py` en esta sesión (§1/§2). Esta sesión descargó y
registró; no abrió microdato ni analizó contenido de encuesta más allá de identificar qué
payload es cada archivo.
