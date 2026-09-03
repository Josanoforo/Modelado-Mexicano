# ACTO MAESTRA36-A2 · COMPRANET-DICCIONARIOS-Y-LLAVES — nota de cierre (P1, P2, P3)

**Encargo:** `forense/encargos/2026-09-03-MAESTRA36-A2-COMPRANET-DICCIONARIOS-Y-LLAVES.md` (SHA de redacción `9af8407`).
**Base real de trabajo:** `ea45e01d` (`origin/main`, merge PR #500). `9af8407` es ancestro; main avanzó 30 commits entre la redacción y el arranque.
**Entorno:** CAJA UBUNTU, clon `/home/pc0/mm-adq`. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`; sonda `https://www.inegi.org.mx/` → `200`; `ls data/raw/ | head -1` → `2005trim1_csv.zip` (corpus compartido montado, 374 entradas). Corrida a las 00:26–00:5x CST del 3/sep, fuera de la ventana del cron (07:25–08:00).
**Compuerta:** cumplida. `git log --format=%s origin/main | grep -c 'MAESTRA36-A1'` → `1`; verificación **por producto**: `git show origin/main:forense/encargos/2026-09-02-MAESTRA36-A1-ESCANEA-RECURSIVO-Y-REGISTRA-DESCARGAS.md | grep -n '^## '` → `175:## CONSUMIDO`.
**Versión del encargo bajo la que se ejecutó:** la **v1** (SHA de redacción `9af8407`). La **ENMIENDA DE DIRECCIÓN del 3/sep** (archivada verbatim al pie del encargo por A.3) declara que la **v3**, que sustituía a la v1, difería solo en: cabecera/compuerta (`ea45e01`, COMPUERTA ninguna, cumplida **por producto**: `## CONSUMIDO` de A1 con `PR #500`, `ADR-310`), CARRILES (`N2` nube, `L12`/`L13` caja, disjuntos de `data/curacion-registro/**`), la firma de mesa verbatim del 2/sep, A.8 §(3) sobre el rótulo de la fila 63, y la cita de `FP-258` al editar esa fila por línea. **Nada de eso mueve `P1`–`P3` ni su resultado**, y los cinco puntos se verificaron uno por uno contra el árbol al cerrar (ver el encargo archivado). La fila 63 se editó **línea por línea, nunca con round-trip de `csv`** — que es el fondo de `FP-258`.

**Firmas que abre este acto:** `FP-262` (recibo del lote) y `FP-263` (el desvío de perímetro de `relaciones.tsv`, elevado a mesa; ver §P1). **ADR:** `ADR-313`. Numeración **renumerada al cerrar**: las candidatas eran `ADR-312`/`FP-261`/`FP-262`, y `PR #502` (`ACTO MAESTRA36-L13`) fusionó segundo llevándose `ADR-312` y `FP-261` — la regla «renumera quien fusione segundo», aplicada a este acto. Re-derivado contra `origin/main = 18fd2bd3`: máximo `ADR-312` sin duplicados, máximo `FP-261`. `L12` sigue abierto.

---

## P1 · Los cuatro archivos del encargo: NO OBTENIDOS. Dos payloads distintos sí llegaron.

### Las cuatro rutas, con salida cruda

**(i) URL directa, host que el encargo nombra.** Los cuatro archivos viven, según el encargo, en
`upcp-compranet.funcionpublica.gob.mx/publicas/` (los tres `DD_*.xlsx`) y en
`upcp-cnetservicios.funcionpublica.gob.mx/norah/documentos/recursos/lck/hc/obtener` (reporte RUPC).

```
curl: (7) CONNECT tunnel failed, response 502   ← dentro del sandbox, los 4
curl: (6) Could not resolve host: upcp-compranet.funcionpublica.gob.mx      ← FUERA del sandbox
curl: (6) Could not resolve host: upcp-cnetservicios.funcionpublica.gob.mx  ← FUERA del sandbox
getent hosts upcp-compranet.funcionpublica.gob.mx      → (vacío)
getent hosts upcp-cnetservicios.funcionpublica.gob.mx  → (vacío)
```

**A.5 — probado dentro y fuera del control de red.** El `502` del túnel CONNECT es lo que la caja
reporta; el hecho de fondo es que **ninguno de los dos hosts tiene registro A**. No es artefacto del
sandbox. Barrido de DNS sobre los seis hosts candidatos (fuera del sandbox):

| host | registro A |
|---|---|
| `upcp-compranet.funcionpublica.gob.mx` | **ninguno** |
| `upcp-cnetservicios.funcionpublica.gob.mx` | **ninguno** |
| `directoriosancionados.funcionpublica.gob.mx` | **ninguno** |
| `compranet.hacienda.gob.mx` | **ninguno** |
| `comprasmx.buengobierno.gob.mx` | `129.158.203.10` |
| `canvas-compranet.buengobierno.gob.mx` | `141.148.35.163` |
| `upcp-cnetservicios.buengobierno.gob.mx` | `129.153.147.199` |
| `directoriosancionados.buengobierno.gob.mx` | `200.34.175.7` (vía `ranchersedeprod.buengobierno.gob.mx`) |

El dominio `funcionpublica.gob.mx` dejó de resolver para estos servicios. La migración a
`buengobierno.gob.mx` que `ACTO MAESTRA35-A1` documentó el 2/sep está completa a nivel de DNS.

**(ii) Índice / descarga masiva del portal.** El índice HTML plano que dirección abrió entero el 2/sep:

```
https://canvas-compranet.buengobierno.gob.mx/informacion_ayuda/datos_abiertos.html → 502, 547 B (×3 intentos)
https://canvas-compranet.buengobierno.gob.mx/informacion_ayuda/                     → 502, 547 B
https://canvas-compranet.buengobierno.gob.mx/robots.txt                             → 502, 547 B
```

El `502` alcanza también a `/robots.txt`: **el backend del host está caído entero**, no es un
problema de ruta. Cuerpo: `<html><head><title>502 Bad Gateway</title>…` de nginx.

Segunda vía de (ii): leer el bundle Angular de `comprasmx` a ver si incrusta la lista de datos
abiertos. Bajados `main-7GRPPNPE.js` (2 647 141 B), `chunk-6GYNAYDM.js` (202 776 B),
`scripts-IOZCZ6RI.js` (376 069 B) — 3 225 983 B de JS examinados. Aciertos: `datos_abiertos` → **0**,
`DD_` → **0**, `informacion_ayuda` → **0**. El bundle **no** trae el índice; esa página la sirve el
host `canvas-*`, que está caído. Sí reveló 30 URL de `buengobierno.gob.mx`, entre ellas
`historico-compranet.buengobierno.gob.mx` y `upcp-cnetservicios.buengobierno.gob.mx/{janis/catalogos,norah/documentos,amy,legacy/hanna,legacy/jovovich}`.

**(iii) Espejo `buengobierno` para el mismo path.** El encargo autoriza probar el mismo path bajo
`comprasmx.buengobierno.gob.mx` (espejo verificado para `cnetassets/`):

```
comprasmx…/publicas/DD_PIC_CONTRATOS_2400703.xlsx            → 200, 7000 B, text/html   ← soft-200
upcp-compranet…/publicas/DD_PIC_CONTRATOS_2400703.xlsx       → 200, 7000 B, text/html   ← soft-200
comprasmx…/cnetassets/publicas/DD_PIC_CONTRATOS_2400703.xlsx → 404,  276 B, iso-8859-1  ← 404 REAL
```

⚠️ **El `200` de 7000 B no es éxito**: es el shell de la SPA Angular, el mismo patrón `soft-200` que
la propia fila 63 ya documentaba y que `MAESTRA35-L3` midió en `ieeags.mx`/`te.gob.mx`. Lo útil es que
`cnetassets/` sirve **404 reales de 276 B** (Apache, `iso-8859-1`), distinguibles del shell — eso hace
la sonda informativa bajo ese prefijo. Con esa discriminación se probaron cinco carpetas
(`datos_abiertos_contratos_expedientes/`, `…/diccionarios/`, `cnetassets/diccionarios/`,
`cnetassets/publicas/`, `cnetassets/datos_abiertos_rupc/`, `cnetassets/datos_abiertos/`): **404 real en
todas** para los `DD_*`. Los tres diccionarios no están bajo `cnetassets/`. Listado de directorio:
`403`, 279 B.

**(iv) Reporte RUPC y espejo histórico.**

```
upcp-cnetservicios.buengobierno.gob.mx/norah/documentos/recursos/lck/hc/obtener
  → 403, 143 B, application/json
  {"success":false,"error":"Acceso no permitido.","details":"Acceso no permitido. - /norah/documentos/recursos/lck/hc/obtener - None","pid":null}
upcp-cnetservicios.buengobierno.gob.mx/norah/documentos      → 403, mismo JSON
upcp-cnetservicios.buengobierno.gob.mx/janis/catalogos/      → 404, {"detail":"Not Found"}
comprasmx.buengobierno.gob.mx/norah/…/obtener                → 200, 7000 B (shell, no es éxito)
historico-compranet.buengobierno.gob.mx/  → curl (35) TLS connect error: unexpected eof while reading
   con --tlsv1.2 / --tlsv1.3 / --http1.1 / --tls-max 1.2 → los cuatro, http=000
```

El endpoint `norah` del reporte RUPC **existe y rechaza** (403 de aplicación, no 404): necesita sesión
o parámetros que esta caminata no tiene. `historico-compranet` (donde viviría la serie 2010–2022)
corta el TLS en las cuatro variantes probadas.

### Lo que SÍ se obtuvo, byte a byte

El ancla que dirección abrió desde nube el 2/sep se reprodujo en caja, y con ella un segundo archivo
de la misma carpeta:

| archivo | bytes | filas × col | sha256 (doble bajada) |
|---|---|---|---|
| `Contratos_CompraNet5.xlsx` | 4 417 249 | 13 406 × 45 | `9fcbce83…be6634` — **idéntico** en ambas bajadas |
| `Expedientes_CompraNet5.xlsx` | 1 573 365 | 7 200 × 21 | `a8ac896d…575b3c` — **idéntico** en ambas bajadas |

Ambos de `https://comprasmx.buengobierno.gob.mx/cnetassets/datos_abiertos_contratos_expedientes/`.
**A.7** cumplido: doble descarga, `sha256` idéntico. **Estructura verificada, no solo tamaño**:
`zipfile.testzip()` → `None` en las cuatro copias; hoja única legible por `openpyxl` en las cuatro.

⚠️ **Identidad por contenido, no por rótulo.** Viven en la carpeta de datos abiertos y el encargo
esperaba diccionarios ahí, pero **no son diccionarios de datos: son los datos**. Verificado leyendo
cabecera y 5 filas: `Contratos_CompraNet5.xlsx` trae 13 406 contratos reales (instituciones, RFC,
importes); `Expedientes_CompraNet5.xlsx`, 7 200 procedimientos. Los `DD_*` (los diccionarios
propiamente) siguen sin localizarse.

### Registro (P1, tres capas)

- `data/manifiesto.yaml`: **1 102 → 1 104 ids**. Altas `compranet5_contratos_2022_2023_xlsx` y
  `compranet5_expedientes_2019_2023_xlsx`, por `tests/manifiesto.py --registra` (una invocación por
  `--id`, A.1) — `sha256`/tamaño/entorno derivados por el script, ninguno tecleado.
  `licencia` = *no declarada por la fuente*, con la razón: la página que la declararía respondió 502.
  A.8 previo: `compranet|comprasmx` en `data/manifiesto.yaml` → **0** aciertos sobre 1 102 ids (el
  único acierto de `funcionpublica` es texto de una nota sobre SICS, no un payload). No se repitió nada.
- **Anti-PR#77** verificado: los dos payloads están en el **corpus compartido**
  `/home/pc0/mm-corpus/raw/`, no solo en el worktree — `ls -la` sobre la ruta absoluta, no sobre el symlink.
- `data/curacion-registro/cola-adquisicion-registro.tsv:63`:
  `NO-OBTENIDO-POR-ESTE-AGENTE(2 intentos)` → **`OBTENIDO-PARCIAL`**, con `ids_manifiesto` y la nota
  completa (4 rutas, salida cruda, receta de navegador ≤1 min). Vista regenerada con
  `python3 tools/vista_cola_adquisicion.py` → 111 filas (T26).
- `data/curacion-registro/aliases-fuentes.tsv`: **13 → 14** familias. Alta de
  `COMPRANET5_DATOS_ABIERTOS` → `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6`, **SIN FUSIONAR**: la fila
  canónica nombra el catálogo de proveedores S1-S3-S6 de la PDN, y lo obtenido es CompraNet5, otra
  plataforma que cubre solo parte de esa necesidad. La fusión exigiría firma de mesa.
- `data/curacion-registro/baseline.json` recifrado (`aliases-fuentes.tsv` `filas` y `sha256`,
  `conteos.familias_alias` 13 → 14, `procedencia.origen` anotado con qué acto recifró y por qué).
- `tools/curador_registro/via_capa2.py` en **verde**: `COINCIDE=54 NO_COINCIDE=0 AUSENTE=0
  SIN_PAYLOAD=0 RAIZ_NO_CONFIGURADA=14`, **diffs propuestos = 0**.

#### Desvío de perímetro, declarado (no ejecutado)

El encargo pide escribir `relaciones.tsv` + procedencia (`evidencias.tsv`) + `utilidad-modelo.tsv`
«contra la necesidad de EXT-OF-05». **No se escribieron.** Razón, verificada contra el árbol y no
supuesta:

```
tail -n+2 data/curacion-registro/relaciones.tsv | cut -f2 | sort -u | grep -vE '^N[0-9]+$'   → (vacío)
cut -f1 data/curacion-registro/necesidad-objeto-modelo.tsv                                    → N1 … N37
grep -n 'R3\.1\|R3\.2' data/curacion-registro/necesidad-objeto-modelo.tsv                     → 0 aciertos
```

`EXT-OF-05` es una necesidad del **mapa de aperturas externas**
(`data/mapa-ext-oficial-2026-08-06.tsv:6`, `data/cola-ext-oficial-2026-08-06.tsv:4`), cuya fuente
declarada es la **Plataforma Digital Nacional de SESNA** (`plataformadigitalnacional.org`, sistemas
S1-S2-S3-S6) y cuyo destino son las reglas `R3.1`/`R3.2`. El catálogo de necesidades del curador es
`N1…N37` y la columna `necesidad_id` de `relaciones.tsv` no tiene **ni una** excepción a ese dominio.
Escribir `EXT-OF-05` ahí estrenaría un valor ajeno al esquema del curador — un cambio estructural que
este acto no está autorizado a hacer. Se eleva a firma de mesa
(`forense/firmas-pendientes.tsv`, `FP-263`) en vez de resolverse por inferencia.

Corolario que el encargo no anticipaba: **CompraNet no es la fuente de `EXT-OF-05`.** La necesidad
pide S1 (declaraciones), S2 (intereses), S3 (sancionados) y S6 (contrataciones) de la PDN. CompraNet
cubre el eslabón de contrataciones y proveedores; S1/S2/S3 viven en otra plataforma. Esto acota lo
que este acto puede contestar, y se refleja en el veredicto de P2.

### Corrección de rótulo (cobertura retroactiva, punto 3 del encargo)

La fila dice `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` pero su contenido es la necesidad
**`EXT-OF-05`** (`EXT-OF-07` es IFT). Corregido **en la nota de la fila**, no en `fuente_canonica`
— como el encargo instruye. Nota adicional: la fila se cita como
`cola-adquisicion-v1_0.tsv:63`, pero en la **vista** vigente es la línea **64** (la vista lleva una
línea de cabecera `# GENERADO`); en el **registro**, que es la fuente, es la línea 63. La identidad
se confirmó por `fuente_canonica`, no por número de línea.

---

## P2 · Las llaves, contestadas con lo que hay — y medidas, no supuestas

Sin los tres `DD_*`, el universo de evidencia disponible es el **inventario de campos real** de los dos
payloads obtenidos (que es lo que un diccionario describiría) más lo que las sondas dijeron del RUPC y
del directorio de sancionados. Se declara así, y el veredicto se emite sobre ese universo, no sobre el
que el encargo esperaba.

### Tabla de llaves

| eslabón | `Contratos_CompraNet5.xlsx` | `Expedientes_CompraNet5.xlsx` | RUPC | sanciones |
|---|---|---|---|---|
| **persona** (servidor público) | `Responsable de la UC` — **nombre libre**, 690 distintos, sin id | `Operador`, `Correo electrónico` — **nombre libre**, 877 distintos | sin evidencia | sin evidencia |
| **proveedor** | `RFC` (col 38) · `Folio en el RUPC` (37) · `Proveedor o contratista` (39) · `Estratificación` (40) · `Clave del país` (41) | — (no trae proveedor) | **no obtenido** (403/DNS) | sin evidencia |
| **procedimiento** | `Código del expediente` (7) · `Número del procedimiento` (13) · `Referencia del expediente` (8) | `Código del expediente` (1) · `Número del procedimiento` (2) · `Referencia` (6) | n/a | n/a |
| **contrato** | `Código del contrato` (21) · `Núm. de control del contrato` (22) | — | n/a | n/a |
| **sanción / inhabilitación** | **NINGÚN CAMPO** | **NINGÚN CAMPO** | no obtenido | `directoriosancionados` no abrió |

Búsqueda de campo de sanción, con control positivo: el filtro
`'sanc' in h.lower() or 'inhabil' in h.lower()` sobre los 45 + 21 encabezados devuelve **0** en ambos
archivos; el mismo filtro sobre `'contrato'` devuelve 8 en contratos, así que el filtro discrimina.

### Medición del cruce (que la columna exista no es que la llave cruce)

**Llenado y unicidad en contratos (n = 13 406 filas):**

| campo | no vacíos | distintos |
|---|---|---|
| `Código del contrato` | 13 406 (**100 %**) | **13 406 → único por fila** |
| `Núm. de control del contrato` | 13 406 (100 %) | 12 727 (no único) |
| `Código del expediente` | 13 406 (100 %) | 5 759 |
| `Número del procedimiento` | 13 406 (100 %) | 5 751 |
| `RFC` | 11 590 (**86,5 %**) | 2 102 |
| `Folio en el RUPC` | 9 730 (**72,6 %**) | 1 249 |
| `RFC verificado en el SAT` | 13 406 (100 %) | 2 valores: `UC`, `PoC` |

**Identidad de proveedor — limpia donde está poblada.** `RFC` con más de un `Folio en el RUPC`
distinto: **0** de 2 102. Es decir, la correspondencia RFC ↔ folio RUPC no colisiona. Pero **980 de
los 2 102 RFC no traen ningún folio RUPC**, y 1 816 filas no traen RFC.

**Cruce contratos ↔ expedientes por `Código del expediente`:**

```
distintos en contratos 5 759 · en expedientes 7 200
intersección                                  1 961
contratos cuyo expediente no aparece          3 798
expedientes sin contrato                      5 239
```

**No es artefacto de ventana temporal** — se verificó antes de concluir. Contratos: publicación
2021 (8) / 2022 (6 839) / 2023 (6 035). Expedientes: creación 2019 (14) / 2020 (88) / 2021 (134) /
2022 (2 184) / 2023 (4 780). Restringiendo **ambos** a la ventana compartida 2022–2023:

```
contratos 5 531 · expedientes 6 964 · intersección 1 961
contratos cuyo expediente NO aparece: 3 570 (64,5 %)
```

El corte persiste dentro de la ventana común. Y es **selectivo**, no aleatorio — desglose por
`Plantilla del expediente`:

| plantilla | sin expediente | con expediente |
|---|---|---|
| `01. Licitación Pública LAASSP` | **2 829** | 202 |
| `08. Reporte de otras contrataciones…` | 1 855 | **5 094** |
| `05. Adjudicación Directa LAASSP` | 1 577 | 397 |
| `02. Licitación Pública LOPSRM` | 421 | — |

Lo que cruza es sobre todo `08. Reporte de otras contrataciones`; **la licitación pública, que es
justo el procedimiento que R3.1/R3.2 querrían trazar, es la que más se cae** (2 829 de 3 031 sin
expediente correspondiente). Los dos archivos son poblaciones distintas, no dos vistas de la misma.

### Veredicto A.4 sobre la necesidad `EXT-OF-05`

> **`EXISTE-NO-SATISFACE`**

**Universo examinado:** los 45 encabezados de `Contratos_CompraNet5.xlsx` y los 21 de
`Expedientes_CompraNet5.xlsx` (verificados contra los payloads en disco, no contra un diccionario), más
4 sondas de red sobre el RUPC y 2 sobre el directorio de sancionados. **No** se examinaron los tres
`DD_*` del encargo: no se obtuvieron. **No** se abrió ningún CSV de la serie de contratos.

**Qué sí satisface:**
- **Contrato:** `Código del contrato`, 100 % lleno y único por fila. Llave estable, sin reservas.
- **Procedimiento:** `Código del expediente` y `Número del procedimiento`, 100 % llenos en ambos archivos.
- **Proveedor:** `RFC` + `Folio en el RUPC`, sin colisión medida (0 de 2 102) — llave estable **donde está poblada**.

**Qué falta, y por eso no satisface:**
1. **El eslabón de sanción no existe en estos datos.** Cero campos de sanción o inhabilitación en los
   66 encabezados. El directorio de sancionados no se pudo abrir: el host `funcionpublica` no resuelve,
   el host `buengobierno` corta el TLS. **La cadena proveedor → sanción no cruza con lo que hay hoy en la caja.**
2. **El eslabón de persona no tiene llave.** `Responsable de la UC` y `Operador` son nombres libres
   (690 y 877 valores distintos). No hay identificador de servidor público, que es precisamente lo que
   S1/S2 de la PDN aportarían — y esos no son CompraNet.
3. **La cobertura de proveedor no alcanza para panel.** 72,6 % con folio RUPC, 86,5 % con RFC.
4. **El join procedimiento ↔ contrato pierde el 64,5 %** dentro de la ventana común, y pierde
   selectivamente la licitación pública. Un panel construido sobre este join estaría sesgado hacia
   `Reporte de otras contrataciones`.

El criterio de promoción que la propia necesidad declara — *«promover si las llaves y cobertura
permiten panel/evento reproducible sin identificación sensible»* — **no se cumple**: hay llaves, no hay
cobertura ni el eslabón de sanción.

---

## P3 · Rama «no EXISTE-SATISFACE»

Como P2 no dio `EXISTE-SATISFACE`, **no se propone la serie 2010–2025** y **no se divide la fila 63 en
sub-filas por año**. Por lo mismo no se estimaron bytes de la serie: habría sido trabajo sobre una
premisa que el veredicto no sostiene.

La fila queda en `OBTENIDO-PARCIAL` con el veredicto en su nota, y el hallazgo se anota en
`forense/hallazgos.md`: **la trazabilidad administrativa que `R3.1`/`R3.2` necesitarían no cruza** con
lo que CompraNet publica hoy y esta caja puede abrir.

Nota para quien retome: `historico-compranet.buengobierno.gob.mx` es la pista de la serie histórica y
`upcp-cnetservicios.buengobierno.gob.mx/norah/documentos` la del RUPC. Ninguna se declara inexistente
— las dos respondieron algo (TLS cortado y `403` de aplicación respectivamente), y ninguno de los dos
hechos autoriza una conclusión de A.5/A.6 sobre la fuente.

---

## CONTADOR

- **Payloads `OBTENIDO`: 83 → 83.** El encargo proyectaba **+4**; el resultado real es **+0 en ese
  estado y +1 fila en `OBTENIDO-PARCIAL`** (token de estado **nuevo** en el vocabulario de
  `estado_A4A5`, introducido por la instrucción literal del encargo «cola fila 63 → OBTENIDO parcial»;
  verificado que ningún script de `tools/`/`tests/` cuenta `estado_A4A5 == OBTENIDO`, así que no voltea
  ningún contador en silencio).
- **`data/manifiesto.yaml`: 1 102 → 1 104 ids.** Dos payloads nuevos, ambos con A.7 y estructura verificada.
- **`aliases-fuentes.tsv`: 13 → 14 familias.**
- **Necesidad `EXT-OF-05` con veredicto A.4 por primera vez:** `EXISTE-NO-SATISFACE`.
- **Los 4 archivos que el encargo nombra: 0 de 4 obtenidos**, con las 4 rutas declaradas y receta de navegador.
- **Medición de modelo: cero directo.** Este acto no corrió el motor, no tocó reglas y no archivó
  ningún veredicto del Hito D. No altera ningún falsador.

## Lo que este acto NO hizo

No bajó la serie de contratos. No tocó `milpa/**`, `tests/manifiesto.py` ni `tools/adquiere_cron.sh`.
No escribió `relaciones.tsv`/`evidencias.tsv`/`utilidad-modelo.tsv` (desvío declarado arriba, elevado a
firma). No respondió nada sobre `R3.1`/`R3.2` más allá de si las llaves cruzan — y la respuesta es que
no cruzan en el eslabón de sanción.
