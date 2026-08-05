# ENCARGO M-2 (5/ago) · Cinco incógnitas y una corrección

Sesión ENCARGO M-2 "incógnitas", rama `sesion/encargo-m2-incognitas`, base `origin/main`
= `16d9dbd` (PR #130, `ENCARGO CORRIDA-IDG3`, ya fusionado). Entorno asignado: Ubuntu
pc0 (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, `curl` contra inegi.org.mx →
`200`). `data/raw` no montada — no fue necesaria: los cinco payloads de §1 viven bajo
`raiz: descargas_mx`, localizados directamente en `/mnt/c/Users/PC0/Descargas MX/` (fuera
del repo); ningún otro payload de este acto se abrió. `data/raices.local.yaml` (gitignorado)
se creó apuntando `descargas_mx` a esa ruta para poder correr `tests/manifiesto.py
--verifica`, un `--id` por invocación (v2.5 A.1).

Perímetro: `data/manifiesto.yaml`, esta nota, `forense/hallazgos.md`. No se tocó `canon/`,
no se selló ADR, no se abrió ningún microdato nuevo (los cinco ZIP de §1 son el lanzador,
no el microdato; su XML interno se leyó por ser el propio objeto del encargo).

## §1 · Los cinco `descargamasiva_3072026_*`: identificados

Premisa del encargo verificada primero: las cinco entradas (`_105543`, `_10560`,
`_105617`, `_105625`, `_10567`) sí decían, textual, `usado_para: sin uso asignado —
registro de inventario` y `url_origen: no determinada` — confirmado por lectura antes de
tocar nada.

`sha256sum` de los cinco ZIP en disco contra el manifiesto: **COINCIDE exacto en los
cinco** (`tests/manifiesto.py --verifica`, un `--id` por corrida, salida cruda abajo).
`unzip` no está instalado en este entorno (mismo límite que ya registró
`forense/notas/2026-07-31-enut-descarga.md`); se usó `zipfile` de Python, misma operación
no destructiva.

**Estructura, idéntica en los cinco:** `DescargaMasivaApp.exe` (850 432 B, instalador
genérico) + `leeme.txt` (434 B, instrucciones genéricas) + `DescargaMasivaOD.xml` (348–480
B, **el único archivo con contenido específico de la edición**). Confirma lo que
`2026-07-31-enut-descarga.md` §Parte 2 ya había anotado y dejado explícitamente **fuera de
perímetro** de esa sesión: los tres nombres internos no distinguen encuesta ni edición; solo
el XML lo hace, y abrirlo no es extraer/ejecutar el `.exe` — es leer un manifiesto de URLs de
69 B a 480 B, la misma operación de lectura que ya está hecha sobre
`descargamasiva_382026_131650_xml` (CPV 2020) en el manifiesto actual.

El XML de cada uno resultó ser una lista de 2–3 URLs `https://www.inegi.org.mx/contenidos/programas/enut/<año>/...`,
**instrumento ENUT (Encuesta Nacional sobre Uso del Tiempo) en los cinco casos**, una edición
por archivo:

| id | XML (bytes) | `totalMb` declarado | Edición ENUT | URLs internas |
|---|---|---|---|---|
| `descargamasiva_3072026_105543` | 480 | 17.47 MB | **2024** | `enut_2024_bd_csv.zip` · `enut_2024_diagrama_er.zip` · `enut_2024_fd.xlsx` |
| `descargamasiva_3072026_10560` | 479 | 9.53 MB | **2019** | `enut_2019_bd_csv.zip` · `enut_2019_diagrama_er.zip` · `enut_2019_fd.xlsx` |
| `descargamasiva_3072026_105617` | 348 | 5.19 MB | **2009** | `fd_enut09.pdf` · `enut_2009_dbf.zip` |
| `descargamasiva_3072026_105625` | 350 | 2.77 MB | **2002** | `descripcion.pdf` · `enut_2002_dbf.zip` |
| `descargamasiva_3072026_10567` | 348 | 5.68 MB | **2014** | `fd_enut14.xls` · `bd_enut14_dbf.zip` |

**Hallazgo colateral, no anticipado por el encargo: los cinco son redundantes.** Las URLs
internas de cada XML son, byte por byte, las mismas URLs que ya están catalogadas de forma
directa y correcta en el manifiesto — `enut2002_bd_dbf`/`enut2002_fd_pdf`,
`enut2009_bd_dbf`/`enut2009_fd_pdf`, `enut2014_bd_dbf`/`enut2014_fd_xls`,
`enut2019_bd_csv`/`enut2019_fd_xlsx`/`enut2019_der_zip`,
`enut2024_bd_csv`/`enut2024_fd_xlsx`/`enut2024_der_zip` — todas descargadas directamente el
2026-07-30, antes de que estos cinco ZIP se registraran. Los cinco `DescargaMasiva_*.zip` son
el paquete de escritorio que el portal ofrece como *alternativa* a la descarga directa, no un
payload adicional: no aportan ningún microdato que el manifiesto no tuviera ya. `usado_para`
de los cinco se corrigió para decir esto explícitamente (mecanismo, no payload; instrumento y
edición nombrados; redundancia declarada) en vez de dejarlos en "sin uso asignado". La URL de
descarga del ZIP lanzador en sí **sigue sin determinar** — el portal lo genera bajo demanda,
sin URL persistente, mismo patrón ya documentado para `descargamasiva_382026_131650_xml`
(CPV 2020) — así que `url_origen` no pasó de "no determinada" a una URL real, solo ganó la
explicación del mecanismo.

**Nota de premisa, tipo (1) verificado contra archivo:** el encargo cuenta "cinco (seis con
el XML)" como si los seis compartieran el mismo defecto (`usado_para` sin asignar). Falso
para el sexto: `descargamasiva_382026_131650_xml` **ya tenía** `usado_para` con contenido
real y detallado (mecanismo CPV 2020, 576 URLs, `forense/notas/2026-08-03-descarga-masiva-xml-mecanismo.md`)
desde antes de este acto — no decía "sin uso asignado" ni nada equivalente. Por
`instrucciones-proyecto-v2_5.md` ("Verificación de premisas antes de ejecución"): se reporta
la discrepancia, no se ejecuta como si la premisa fuera cierta. No se tocó esa entrada.

```
$ python3 tests/manifiesto.py --verifica --id descargamasiva_3072026_105543
descargamasiva_3072026_105543 [descargas_mx]: COINCIDE -- sha256 y tamaño (602155 bytes) verificados contra data/manifiesto.yaml
$ python3 tests/manifiesto.py --verifica --id descargamasiva_3072026_10560
descargamasiva_3072026_10560 [descargas_mx]: COINCIDE -- sha256 y tamaño (602154 bytes) verificados contra data/manifiesto.yaml
$ python3 tests/manifiesto.py --verifica --id descargamasiva_3072026_105617
descargamasiva_3072026_105617 [descargas_mx]: COINCIDE -- sha256 y tamaño (602150 bytes) verificados contra data/manifiesto.yaml
$ python3 tests/manifiesto.py --verifica --id descargamasiva_3072026_105625
descargamasiva_3072026_105625 [descargas_mx]: COINCIDE -- sha256 y tamaño (602154 bytes) verificados contra data/manifiesto.yaml
$ python3 tests/manifiesto.py --verifica --id descargamasiva_3072026_10567
descargamasiva_3072026_10567 [descargas_mx]: COINCIDE -- sha256 y tamaño (602152 bytes) verificados contra data/manifiesto.yaml
```

## §2 · ENCUCI 2020: corrección verificada

Premisa del encargo verificada primero: `encuci2020_bd_dbf` decía, textual, "aún no
explotado en ninguna ficha de falsación commiteada; bloqueado además por conf.06 (D-06,
canon/cola.yaml)". Confirmado por lectura antes de corregir.

**Ambas partes de la premisa correctora del encargo se sostienen contra archivo:**

1. **C-06b corrió contra este microdato.** `forense/notas/2026-08-05-c06b-conf06-encuci-corte.md:472`
   registra `encuci2020_bd_dbf [data_raw]: COINCIDE -- sha256 y tamaño (6913684 bytes)
   verificados contra data/manifiesto.yaml` antes de abrir el `.dbf` — mismo sha256 que este
   manifiesto declara (`0414fd59...f283`). C-06b abrió `ENCUCI_2020_SEC_4_5.dbf` (dentro de
   este mismo ZIP) y produjo `ADR-64` (`canon/gobernanza-v1_15.md:798`, ENCARGO M-5,
   5/ago/2026), que cierra `conf.06`.
2. **Encargo W estimó `AP5_1_1/2/3` sobre él**, antes que C-06b:
   `forense/notas/2026-08-04-w-coeficientes-generador-paso1.md:63,109-128,257-259` corre
   `AP5_1_1`/`AP5_1_2`/`AP5_1_3` de la misma tabla `ENCUCI_2020_SEC_4_5` como el coeficiente
   marginal `W1` de `radio_confianza` — resultado: solo `AP5_1_3` (vecinos) distinguible de
   cero al 95%.

`usado_para` de `encuci2020_bd_dbf` y `encuci2020_fd_pdf` se corrigió citando ambos actos, con
sus notas y rutas de archivo. Se corrigió también, en la misma entrada, el campo `formato`/`nota`
de `encuci2020_bd_dbf`, que seguía diciendo "no inspeccionado, solo hasheado" — cierto el
2026-07-30 (firewall de esa sesión, ADR-46: la contaminación es por sesión, no por payload) pero
nunca actualizado cuando las dos sesiones posteriores sí lo abrieron. No se tocó el veredicto
`D` de `R8.3` en sí: `ADR-64(e)` solo levanta la condición B (cifras en conflicto); la condición
A (marca C3, circularidad de `radio_confianza` contra `cooperacion.confianza.puente_personal`)
sigue vigente y `R8.3` no se adjudica aquí — eso es trabajo de mesa, no de este acto.

## §3 · Barrido de `usado_para` desactualizados, más allá de lo que trajo el encargo

El encargo pidió explícitamente buscar más campos de este tipo y reportar cuántos, sin exigir
corregirlos todos. Método: `awk` sobre el manifiesto extrayendo cada `usado_para` completo
(multi-línea), filtrado por un vocabulario de once variantes de "no usado" ("no explotado",
"sin uso asignado", "no leído", "sin ficha", "no evaluado", "aún sin", "pendiente de asignar",
"no abierto", "sin ejecutar", entre otras) — **51 entradas** de 227 declaran alguna forma de
no-uso. De esas, descontando las 5 `descargamasiva_3072026_*` y las 2 de ENCUCI (ya tratadas en
§1/§2), quedan **49 candidatas**. Cada una se cruzó por `grep -rl` contra `forense/`, `tests/`,
`canon/`, `milpa/`, excluyendo el propio manifiesto y excluyendo menciones de "candidata en cola"
(p. ej. `forense/hitoE-campana-medicion-v2_0.md`, que lista posiciones de una cola priorizada sin
que eso implique que el payload se abrió) y menciones de mera logística/verificación de hash
(`--verifica`, TLS, existencia en disco) — ninguna de esas dos clases cuenta como "usado" en el
sentido que el `usado_para` declara o niega.

**Resultado del cruce, dos clases de hallazgo:**

**(a) Falsos positivos del vocabulario — no estaban desactualizados.** `encig2015_csv`
(mención es un ejemplo de convención de nombres en un comentario de `tests/cruce_operables.py`,
no una lectura real) · `encig2015/2017/2021_estructura_base_datos_pdf` (cero referencias fuera
del manifiesto, o solo `--verifica` de hash) · el bloque de 23 ids de ENSANUT 2024 (`nse_*`,
`*_ensanut2024_w_*`, los cinco `*_vfinal_cuestionario_*`) — únicas referencias son posiciones de
cola en `hitoE-campana-medicion-v2_0.md` · los seis ids de ENCUP (`encup_2012_base_datos_xlsx`,
`encup_2001/2003/2005/2008/2012_cuestionario_pdf`) — únicas referencias son logística de
descarga/TLS y `--verifica`, con el propio `usado_para` ya declarando "No leída ni evaluada esta
sesión". Ninguno de estos se tocó.

**(b) Verdaderos positivos — desactualizados, no corregidos aquí, reportados:** **6 entradas de
ENUT** resultaron abiertas y usadas de verdad pese a decir "constructo pendiente de asignar en
el cruce de Hito E": `enut2024_bd_csv` (alimentó `run_r5_2.py`, Encargo Y, propuesta de `R5.2`
—"cuidado → mujeres 40+"—, `forense/notas/2026-08-04-y5-veredicto-r5-2.md`), `enut2024_fd_xlsx`,
`enut2024_diccionario_variables_html`, `enut2019_bd_csv` (`TMODULO.csv` inspeccionado),
`enut2019_fd_xlsx`, `enut2019_diccionario_variables_html` — las seis vía
`forense/notas/2026-08-04-enut-paso1-familismo-obligacion.md` §3.2/§3.5 y, para `enut2024_bd_csv`,
también `2026-08-04-y1-operacionalizacion-r5-2-enut.md`. **Estas seis SÍ se corrigieron** en este
acto (mismo criterio que ENCUCI: cita del acto que las explotó, sin inventar nada nuevo). Nota:
`enut2019_der_zip`/`enut2024_der_zip` **no** están en esta lista — la propia nota de origen
declara explícitamente "No se abrió" para ambos, así que su "pendiente de asignar" sigue siendo
cierto y no se tocaron. `enut2002_bd_dbf`/`enut2009_bd_dbf`/`enut2014_bd_dbf` y sus documentos
tampoco: solo aparecen enumerados en un conteo de existencia (`PN-2`), nunca abiertos.

**Total reportado: 8 campos `usado_para` desactualizados encontrados** (2 de ENCUCI, ya
corregidos por instrucción directa del encargo, más 6 de ENUT, encontrados por este barrido y
corregidos también). Los 5 `descargamasiva_3072026_*` de §1 no entran en esta cuenta — no
declaraban una falsedad sobre uso, declaraban ausencia de identificación, que es el defecto que
§1 resuelve.

## §4 · Cierre

`tests/check.py --baseline`: **VERDE**, `18 FAIL · 95 WARN`, idéntico antes y después. YAML
validado (`yaml.safe_load`, 227 entradas, sin cambio de conteo). No se tocó `canon/`, no se
selló ADR, no se abrió ningún microdato nuevo más allá de los cinco XML de lanzador (§1, 69–480
B cada uno) y la re-lectura de notas ya existentes citadas arriba. No impidió medir. Contadores
movidos: 0 — este acto es de contabilidad del manifiesto sobre sí mismo, no de medición sobre
México; no le aplica el módulo de auditoría de rigor extremo (`instrucciones-proyecto-v2_5.md`,
"Dónde va, y dónde ya no": no va en manifiestos).
