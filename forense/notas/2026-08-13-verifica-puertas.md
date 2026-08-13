# ACTO VERIFICA-PUERTAS · quién puede bajar qué, con vocabulario cerrado

`ENCARGO VERIFICA-PUERTAS`, 13/ago/2026 (`forense/encargos/2026-08-13-VP-verifica-puertas.md`), archivado verbatim como parte de este primer commit (regla A.3). Worktree `/home/pc0/mm-vp-verifica-puertas`, rama `vp/verifica-puertas`.

## 0 · ARRANQUE

1. **REPO.** Clon existente `/home/pc0/Modelado-Mexicano`; worktree nuevo `/home/pc0/mm-vp-verifica-puertas` (`git worktree add -b vp/verifica-puertas /home/pc0/mm-vp-verifica-puertas refs/remotes/origin/main`). `git worktree add` emitió dos veces `error: could not write config file .git/config: Device or resource busy` — misma contención conocida de esta máquina ([[project-modelado-mexicano-git-config-contention]]). Verificado independientemente: `git log -1` → `19d885d Merge pull request #200 from Josanoforo/wt-apertura-issp-1786589980`, `git status` limpio, `git worktree list` lo lista — la creación no falló, solo la escritura de metadato de tracking.
2. **SHA.** El encargo declara base `e993752` (merge #202). `origin/main` real de esta sesión (`git fetch origin main:refs/remotes/origin/main`) es `19d885d` — **más adelante** que `e993752`: `git merge-base --is-ancestor e993752 refs/remotes/origin/main` confirma que `e993752` es ancestro de `19d885d`, no al revés. La diferencia exacta es el merge de PR #200 (APERTURA-ISSP), que se fusionó *después* de que el encargo se redactara. No es PARO (Bloque D) — se trabaja sobre `19d885d`, terreno más fresco, sin nada que re-derivar del perímetro (APERTURA-ISSP no toca `data/universo-puertas-2026-08-12.tsv` ni `data/acceso-puertas-*`).
3. **data/raw.** No aplica — este acto no descarga nada, solo sondea reachability. Declarado y saltado, tal como el encargo lo autoriza.
4. **ENTORNO.** `echo "[$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE]"` → `[]` (sin variable, firma de caja). `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`. Firma de caja-con-red confirmada, entorno correcto.
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale de este worktree o de comandos de red corridos en esta sesión, con el comando a la vista.

**4-bis · OVERRIDE — el hallazgo más grande del arranque, y cambia el resto del acto.** El encargo cita a SONDA-1 (8/ago): "solo inegi.org.mx y banxico.org.mx están en allowlist directo". Verificado de nuevo, por comando, en esta sesión — **ya no es así**. Probado sin override contra un dominio de control fuera de cualquier lista de datos mexicanos (`https://example.com/` → `200` real, vía un proxy CONNECT visible en `curl -v`) y contra dominios que SONDA-1/P·Lote-1 documentaron como bloqueados el 8-12/ago (`cses.org` → `200` sin override, antes daba timeout; `www.gesis.org` → `403` sin override pero con la respuesta *real* de Cloudflare, 5382 bytes, idéntica a la que da con override — no un bloqueo de caja): **la allowlist de esta sesión es sustancialmente más amplia que la medida por SONDA-1**, o el mecanismo de red de la caja cambió de allowlist a denylist. De 43 dominios únicos sondeados en este acto (§2), solo 5 no resolvieron (`historico.mejoredu.gob.mx`, `investigadores.cide.edu`, `www.inee.edu.mx`, `www.mejoredu.gob.mx`, `www.tandasparaelbienestar.economia.gob.mx`) — y los 5 dan el mismo resultado (timeout de DNS/conexión) **con y sin** `dangerouslyDisableSandbox`, confirmando que no son bloqueo de caja sino de red real desde esta máquina (dominios muertos o inalcanzables por DNS, no filtrados por política). Único bloqueo de caja confirmado en todo el acto: `www.google.com` (timeout sin override, no forma parte del universo de puertas de este acto, no se investiga más). **Consecuencia operativa: el override de sandbox está disponible en esta sesión (confirmado contra `www.gesis.org` y `cses.org`, con permiso del usuario), pero no fue necesario para casi ninguna de las 52 filas — el "de ello depende la mitad del universo" que el encargo hereda de SONDA-1 ya no describe el terreno.** Se declara la discrepancia explícitamente: no se ajusta el texto del encargo, se reporta que el terreno cambió (regla v2.1, "verificación de premisas antes de ejecución").

## 1 · Premisas (crudas, comando a la vista)

```
$ awk -F'\t' 'NR>1' data/universo-puertas-2026-08-12.tsv | wc -l
114
$ awk -F'\t' 'NR>1 && $4 ~ /^http/' data/universo-puertas-2026-08-12.tsv | wc -l
51
$ ls data/acceso-puertas-*.tsv 2>/dev/null && echo "YA EXISTE - PARA"
(vacío -- no existe, acto habilitado)
```

**Discrepancia con el encargo, declarada y no forzada a cuadrar.** El encargo dice "52 traen sondeo real de portal"; el filtro literal de la premisa (`$4 ~ /^http/`) da **51**, no 52. Re-derivado por un criterio distinto — filas cuyo `universo_declarado` NO es el texto genérico de MAP-B (`"buscada en el puntero 2026-08-12 y en la cola-adquisicion-2026-08-12 por nombre exacto y por URL, 2026-08-13 (MAP-B)"`) — da **52 exactas**, y **62** con el texto genérico (114 = 52+62, cuadra con el encargo). La diferencia de 1 es `ITAM_panel_household_finance`: tuvo sondeo real (una búsqueda que no encontró portal propio), pero su campo `url` quedó `(ninguna URL especifica...)`, no una URL http. **El "52" del encargo es correcto y es el criterio que se usa en este acto** (no-genérico, no "tiene URL"); la premisa cruda del propio encargo (`$4 ~ /^http/`) subcuenta por 1 fila sin URL. Ambas cifras derivadas por comando, ninguna copiada.

**Fechas, re-derivado:** de las 52, **26 son del 8/ago** (coincide exacto con lo que el encargo cita) y 26 son del 12-13/ago.

**Lecturas obligatorias, leídas íntegras antes de sondear:** `forense/notas/2026-08-12-acto-sonda1-mapa-barreras.md` (§5 barreras por fuente, §6 recetas manuales, §7 PRISMA) y `forense/notas/2026-08-12-acto-p-lote1-adquisicion.md` (§5.1-5.5, 11 intentos contra GESIS/ISSP con cabeceras crudas, §11 patrón `descargas_mx`). Ambas ya documentan, con evidencia cruda, las barreras de: GESIS/ISSP (Cloudflare `cf-mitigated: challenge`), WVS (SPA con sesión, `AJDownload.jsp` da 1 byte a `curl` anónimo con o sin cookies), World Bank NADA ×4 catálogos (login gratuito, formulario Laravel sin CAPTCHA), GPS/briq (do-files libres + formulario de dataset), CSES (sin barrera de portal, solo de caja — y ya no aplica, ver 4-bis), MassMobilization/Dataverse (AWS WAF `x-amzn-waf-action: challenge`), openICPSR/OECD/Cenfri (mismo Cloudflare que GESIS). Estas barreras NO se re-descubren en este acto — se citan y se re-verifica solo el código HTTP/cabecera fresca de esta sesión.

## 2 · Sondeo de dominio, fresco, en esta sesión (no heredado)

Extraídos los 43 dominios únicos de las 52 filas no-genéricas y sondeados uno por uno, sin override, `curl -s -D - -o /dev/null --max-time 12`, capturando código + cabeceras diagnósticas (`cf-mitigated`, `x-amzn-waf-action`, `server`, `location`). Resultado completo en el commit 2 (§4, por fila). Hallazgos de nivel dominio:

- **7 dominios con reto anti-bot confirmado, activo hoy:** `cenfri.org`, `ilostat.ilo.org` (`cf-mitigated: challenge`), `dataverse.harvard.edu` (`x-amzn-waf-action: challenge`, 202), `www.gesis.org`, `www.icpsr.umich.edu`, `www.oecd.org`, `www.openicpsr.org` (todos `cf-mitigated: challenge`, Cloudflare). Re-probados con cabeceras de navegador real (`User-Agent` Chrome/Windows + `Accept-Language`) — **sin cambio**, mismo `cf-mitigated: challenge` (spot-check en `ilostat.ilo.org` y `www.oecd.org`): confirma que es un reto JS real, no un filtro de huella que ceda con solo cambiar la cabecera.
- **2 dominios con bloqueo Cloudflare de huella (UA), NO de reto JS — hallazgo distinto del anterior y no documentado antes en este proyecto:** `www.plataformadetransparencia.org.mx` y `contralacorrupcion.mx` (MCCI) dan `403 "Attention Required! | Cloudflare"` con el `User-Agent` por defecto de `curl`, y **`200` limpio, sin ningún reto, con solo cambiar el `User-Agent` a uno de navegador real** — sin cookies, sin JS, sin sesión. Es una tercera clase de barrera que la cabecera `cf-mitigated: challenge` no marca (no aparece en estas respuestas): un filtro de huella de cliente que un `curl -A "<UA navegador>"` resuelve solo, y por tanto sigue siendo AGENTE, no USUARIO_NAVEGADOR — la definición del vocabulario (§3 del encargo) no exige un `User-Agent` de `curl`, exige "sin cookie de sesión y sin resolver JavaScript", y ninguna de las dos condiciones se viola aquí.
- **5 dominios sin resolver, con y sin override, confirmados como caída real de red/DNS y no de caja:** `historico.mejoredu.gob.mx`, `investigadores.cide.edu`, `www.inee.edu.mx`, `www.mejoredu.gob.mx`, `www.tandasparaelbienestar.economia.gob.mx` — los 5 dan `curl: (28) Resolving timed out`/`Connection timed out` idéntico con `dangerouslyDisableSandbox`. Por A.5: esto es un hallazgo sobre el agente y su entorno de red, no sobre el portal — no se traduce a NADIE ni a "el portal no existe".
- **Todos los demás dominios (29 de 43) responden hoy sin override, sin reto, con contenido real** — incluyendo tres que P·Lote-1/SONDA-1 documentaron como necesitando override el 12/ago (`cses.org`, `gps.econ.uni-bonn.de`, `www.worldvaluessurvey.org`): confirma 4-bis.

## 3 · El vocabulario cerrado (§3.1 del encargo, verbatim, no reescrito) y su aplicación

El encargo ya fija el enum de cinco valores de `quien_puede` (AGENTE / USUARIO_REGISTRO / USUARIO_NAVEGADOR / NADIE / NO_PROBADO) y la regla de no colapsar `http_sin_override` · `http_con_override` · `quien_puede` — ver `forense/encargos/2026-08-13-VP-verifica-puertas.md` §3.1. Este acto no redefine el vocabulario, lo aplica. Precisión operativa añadida por este acto, no contradicción: la definición de AGENTE ("sin cookie de sesión y sin resolver JavaScript") no prohíbe cambiar cabeceras de la petición (`User-Agent`, `Accept-Language`) — un filtro de huella de cliente que cede a una cabecera sigue siendo AGENTE (§2 arriba); un reto que exige ejecutar JavaScript real (Cloudflare Turnstile, AWS WAF challenge) no cede a ninguna cabecera y es USUARIO_NAVEGADOR.

## 3.3 · Pre-registro de falsación (B-bis), antes de clasificar fila por fila

Escrito antes de escribir la tabla de resultados (§4, commit 2), con la evidencia de dominio de arriba ya en mano (level de dominio, no de fila — el pre-registro de fila-por-fila con receta manual es el commit de resultados):

- **Se espera que al menos las 4 filas del 8/ago sin reintento (`Mejoredu_INEE_Bases_Datos`, `CIDE_Panel_Mexico_2006`, `DataCivica_Explorador_Violencia`, `Tandas_para_el_Bienestar`) cambien de cubeta**, porque el override y el vocabulario A.4/A.5 no existían cuando se sondearon. Falsado o confirmado por fila en §4.
- **Se espera que varias de las 21 filas de cubeta D (EXISTE-NO-SATISFACE) resulten AGENTE**, porque su `condicion_acceso` ya declara "libre, sin registro" en la mayoría — la re-clasificación de `quien_puede` no debería sorprender ahí; la sorpresa, si la hay, está en las minoritarias con `condicion_acceso` que sí menciona cuenta/registro.
- **Si el override resultara no necesario en casi ningún caso (confirmado en 4-bis, antes de este punto) — eso es la noticia del acto, no un resultado negativo.** El acto igual entrega el artefacto que no existía: la columna `quien_puede` derivable, mecánica, con evidencia fresca.
- Si una fila resulta con evidencia contradictoria entre esta sesión y una nota previa (p. ej. un dominio que antes daba Cloudflare y hoy no, o viceversa), se reporta la evidencia de HOY como la que manda (A.5: "si no se sondeó en esta sesión, no se sabe"), y se declara el contraste con la nota previa sin asumir cuál estaba mal.

El primer resultado que produzca este procedimiento es el que se reporta.

---

## 4 · Commit 2 — el sondeo fila por fila

Las 52 filas no-genéricas sondeadas individualmente (`curl -s -D - -o /dev/null -r 0-0`, sin y con `dangerouslyDisableSandbox` donde el resultado sin override no fue limpio), más las 62 de universo interno etiquetadas `NO_PROBADO` sin sondear (fuera de alcance declarado, §3.2 del encargo). Tabla completa en `data/acceso-puertas-2026-08-13.tsv`. Metodología por fila: código HTTP crudo primero, cabecera diagnóstica verbatim segundo, `quien_puede` derivado de ambos + el `condicion_acceso` ya documentado por sondeos previos (no re-abierto a nivel de contenido salvo donde se declara "PROMOCIÓN" o "CAMBIO DE CUBETA" abajo).

**Hallazgo cruzado con un acto concurrente, verificado por comando, no solo citado:** mientras se sondeaba `RNM_CNGMD_2023_catalogo977`, la memoria de sesión registró que P·LOTE-2 (PR #204, corriendo en paralelo, `/home/pc0/mm-p-lote2`) encontró la misma API de INEGI (`archivoscompaginacion`) caída (`204` vacío, incluso con un ID de control inválido). Re-verificado de forma independiente en este acto: `idBiinegi=977&tipodocto=4` → `204` hoy. Para descartar que la API completa esté muerta (no solo esta ficha), se re-probó también la URL directa de payload de ENCOAP ya conocida (`.../encoap/2023/microdatos/bd_encoap2023_csv.zip`, ruta de SONDA-1) — **sigue viva, `206`, `420306` bytes exactos** — así que la API de *descubrimiento* está caída pero las URLs de payload ya conocidas por otra vía siguen sirviendo. `INEGI_ENCOAP_2023` se mantiene `AGENTE` con esta evidencia; `RNM_CNGMD_2023_catalogo977` se reclasifica (detalle en la tabla).

### 4.1 · Conteo por `quien_puede` (los cinco valores, suman 114)

| valor | filas |
|---|---|
| NO_PROBADO | 63 (62 universo interno + 1 sin URL propia) |
| AGENTE | 30 |
| USUARIO_NAVEGADOR | 11 |
| USUARIO_REGISTRO | 8 |
| NADIE | 2 |
| **TOTAL** | **114** |

### 4.2 · Filas que cambiaron de cubeta — la noticia del acto

1. **`DataCivica_Explorador_Violencia`** — `NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS` (8/ago, HTTP 403 en `datacivica.org` y `/proyectos/`) → hoy **`AGENTE`**, `206` real en ambas URLs (título "Data Cívica" confirmado, 2913 bytes, sin reto ni bloqueo). Confirma la falsación pre-registrada en §3.3.
2. **`RNM_CNGMD_2023_catalogo977`** — `EXISTE-SATISFACE` (SONDA-1, 12/ago, 87 archivos verificados vía la API de descubrimiento de INEGI) → hoy **`USUARIO_NAVEGADOR`**, la API de descubrimiento murió (`204` vacío, confirmado dos veces independientes: este acto y P·LOTE-2 concurrente). Caso límite del vocabulario, declarado en la tabla: no es un reto anti-bot que ceda a JS, es una API muerta con una ruta manual sin confirmar.
3. **`Mexico_Evalua_IMCO_SignosVitales_Intersecta`** — `SIN-FETCH` (candidata de buscador, nunca abierta byte a byte) → **promovida** (A.6): ambas URLs abiertas con contenido real esta sesión (`206`/`200`). Se mantiene `AGENTE`.
4. **`CIDE_Panel_Mexico_2006`** — el host primario sigue muerto (`investigadores.cide.edu`, DNS no resuelve, con y sin override), pero el mirror `redalyc.org` que la nota del 8/ago ya había alcanzado ("PDF recuperado pero contenido binario/no legible por la herramienta") se reclasifica de facto: el problema era de la herramienta de lectura (WebFetch no parsea PDF binario), no de acceso — un agente con `curl` sí puede bajar esos 174 217 bytes hoy. Se clasifica `AGENTE`.
5. **`MCCI_Encuesta_Corrupcion_Impunidad`** y **`PNT_Plataforma_Nacional_Transparencia`** — ambas declaraban "libre" antes; hoy dan `403 "Attention Required! | Cloudflare"` con el `User-Agent` por defecto de `curl` — un bloqueo de huella de cliente que **no existía en el sondeo anterior** y que cede por completo con un `User-Agent` de navegador (sin JS, sin cookie). Se mantienen `AGENTE`, pero es un mecanismo nuevo, no documentado antes en este proyecto, y se declara como tal (§2 arriba) para que el próximo acto no lo confunda con `cf-mitigated: challenge`.
6. **`Mejoredu_INEE_Bases_Datos`, `Tandas_para_el_Bienestar`** — re-sondeadas con override disponible, tal como el pre-registro (§3.3) anticipaba que podrían cambiar. **No cambiaron**: las 3 URLs de Mejoredu y la única de Tandas siguen sin resolver DNS, idéntico con y sin `dangerouslyDisableSandbox`. La hipótesis del encargo ("la clasificación vieja es de antes del override") queda **falsada** para estas dos filas específicamente — el override no era la causa del bloqueo.
7. **Infraestructura, no clasificación:** `cses.org`, `gps.econ.uni-bonn.de`, `www.worldvaluessurvey.org`, `zenodo.org`, `osf.io` ya no necesitan override (§0/4-bis) — `quien_puede` no cambia para las filas que dependen de estos dominios (ya eran `AGENTE`/`USUARIO_REGISTRO` correctamente), pero el mecanismo de acceso a la caja sí cambió y queda documentado para que el próximo acto no reserve override donde ya no hace falta.

### 4.3 · La lista de descarga manual — el producto que no existía, ordenado por cuántas necesidades sirve cada fuente

19 fuentes requieren humano (`USUARIO_REGISTRO` + `USUARIO_NAVEGADOR`); las recetas completas (ejecutables en <1 min cada una) están en `data/acceso-puertas-2026-08-13.tsv`, columna `receta_manual`:

| # | fuente | quien_puede | necesidades | receta (resumen) |
|---|---|---|---|---|
| 1 | GESIS_ISSP | USUARIO_NAVEGADOR | 7 (N2,N3,N12,N13,N14,N28,N30) | Abrir en navegador, reto Cloudflare se resuelve solo; login con cuenta GESIS ya registrada |
| 2 | GPS_Global_Preferences_Survey | USUARIO_REGISTRO | 5 (N2,N4,N5,N6,N17) | Formulario ya enviado por el agente; revisar correo `jonieqsa@gmail.com` |
| 3 | WorldBank_MEX_EnterpriseSurvey_2023_catalogo6453 | USUARIO_REGISTRO | 3 (N22,N23,N32) | Registrarse gratis en `login.enterprisesurveys.org` |
| 4 | BID_IDB_Microdatos_Center | USUARIO_REGISTRO | 2 (N18,N19) | Portal con bug de redirect propio; buscar "IDB microdata center" si el enlace directo falla |
| 5 | WVS_World_Values_Survey | USUARIO_NAVEGADOR | 2 (N5,N15) | Clic en "Mexico 2018", login con cuenta WVS ya registrada |
| 6 | MassMobilization_Dataverse_MMdata | USUARIO_NAVEGADOR | 2 (N17,N27) | Abrir Harvard Dataverse en navegador, reto AWS WAF se resuelve solo |
| 7 | OIT_ILOSTAT | USUARIO_NAVEGADOR | 1 (N18) | Abrir en navegador, reto Cloudflare se resuelve solo |
| 8 | Tandas_para_el_Bienestar | USUARIO_NAVEGADOR | 1 (N29) | Buscar el programa para confirmar si sigue vigente bajo otro dominio |
| 9 | WorldBank_MEX_ECEPIE_2012_2014_catalogo2661 | USUARIO_REGISTRO | 1 (N13) | Login con cuenta NADA ya activa (`jonieqsa@gmail.com`) |
| 10 | RNM_CNGMD_2023_catalogo977 | USUARIO_NAVEGADOR | 1 (N28) | Navegar a pestaña "Datos abiertos" (API automática muerta) |
| 11 | WorldBank_MEX_LargeScaleFinancialEducation_2011_catalogo2049 | USUARIO_REGISTRO | 1 (N5) | Login con cuenta NADA ya activa |
| 12 | WorldBank_MEX_ParentalEmpowerment_2010_catalogo1039 | USUARIO_REGISTRO | 1 (N28) | Login con cuenta NADA ya activa |
| 13 | openICPSR_Microcredit_MexicoPlacement_proj116334 | USUARIO_NAVEGADOR | 1 (N3) | Abrir en navegador, reto Cloudflare se resuelve solo |
| 14 | OECD_TrustSurveyData | USUARIO_NAVEGADOR | 1 (N30) | Abrir en navegador, reto Cloudflare se resuelve solo |
| 15 | Cenfri_MicroinsuranceMexico | USUARIO_NAVEGADOR | 1 (N21) | Abrir en navegador, reto Cloudflare se resuelve solo |
| 16 | Mejoredu_INEE_Bases_Datos | USUARIO_NAVEGADOR | 0 (candidata) | Buscar "Mejoredu bases de datos PLANEA"; confirmar si el dominio también falla en casa |
| 17 | COLEF_EMIF_Norte_Sur | USUARIO_REGISTRO | 0 (candidata) | Registro en `colef.mx/emif` (nombre/correo/contraseña/institución/rol) |
| 18 | IPUMS_International_Mexico | USUARIO_REGISTRO | 0 (candidata) | Registro gratuito estándar IPUMS |
| 19 | Harvard_Dataverse_Mexico_panel | USUARIO_NAVEGADOR | 0 (candidata, NO-ENCONTRADO) | Abrir en navegador; buscar dataset de panel mexicano dentro (ninguno identificado aún) |

**`NADIE` (2, no accionable sin cambiar de condición — pago o acuerdo restringido, ninguna receta manual ayuda):** `ICPSR_Mexico_Panel_Study_2012` (Restricted Data Use Agreement, N26/N27) · `Gallup_World_Poll` (datasets de pago, N15 potencial).

### 4.4 · Estado de la suite

```
$ python3 tests/check.py --baseline
18 FAIL · 105 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 948ad70343320b62f000d31fd39e2b2b68336ad9)
(3 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

VERDE, sin `--freeze` (no hizo falta). T03 respetado: ninguna cita entre backticks de archivo gitignorado (`data/raw` no se tocó, no hay payloads nuevos).

### 4.5 · Contadores movidos

Cero contadores de México — este acto midió al propio programa (su capacidad de saber quién puede bajar qué), igual que SONDA-1 y P·Lote-1 antes. El artefacto que no existía (columna `quien_puede`, derivable, con evidencia fresca de hoy) ahora existe para 52 de 114 filas del puntero de puertas; las otras 62 quedan `NO_PROBADO`, declaradas y no adivinadas.

El primer resultado que produjo este procedimiento es el que se reporta.
