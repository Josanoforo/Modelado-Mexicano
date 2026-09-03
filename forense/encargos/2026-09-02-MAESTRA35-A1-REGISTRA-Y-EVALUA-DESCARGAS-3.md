# ENCARGO · ACTO MAESTRA35-A1 · REGISTRA-Y-EVALUA-DESCARGAS-3

Archivado verbatim por A.3 (Bloque D, paso 3 de `.claude/commands/acto.md`).
No se edita en ningún otro punto: es el registro de qué se pidió, para poder
auditar si el ejecutor hizo lo que se le dijo.

---

## Texto del encargo, verbatim (dirección/Fable, 2/sep/2026)

ENCARGO · ACTO MAESTRA35-A1 · REGISTRA-Y-EVALUA-DESCARGAS-3 — invoca /acto SHA de redacción: 792b7ef (merge PR #470). Redacta dirección (Fable), 2/sep/2026, contra v2.12. Estado: GATED a que mesa deposite — verificación POR PRODUCTO al arrancar: find "<raíz descargas_mx>" -type f -newermt 2026-09-02 | wc -l > 0 (raíz en data/raices.local.yaml, gitignorada; precedente: /mnt/c/Users/PC0/Descargas MX, 160 archivos el 1/sep). Si es 0, la skill se niega con A.13 y cero commits — mismo cierre «+0» que MAESTRA33-A4. ENTORNO ASIGNADO: UBUNTU (lee Descargas MX y el corpus compartido). NO en NUBE. MODELO SUGERIDO: Opus (P2 exige juicio A.4 contra la necesidad).

CARRILES: MAESTRA35-L3 (adquisición cívica: escribe manifiesto y cola) — este acto también: re-lee data/manifiesto.yaml y data/curacion-registro/cola-adquisicion-registro.tsv antes de cada append y registra por línea, nunca con el módulo csv; renumera/re-aplica quien fusiona segundo. L4/L5/L6: disjuntos.

FIRMAS DE MESA — verbatim. El ejecutor propaga, no decide (SELLA-3).

DB-a (mesa, 1/sep/2026): «dame las ligas y el detalle de qué descargar, las guardo en Descargas MX donde he guardado las que he bajado manualmente» — el PDF DESCARGAS-MANUALES-2026-09-02.pdf es esa lista; este acto es «correr algo para ver qué se bajó y si es lo que necesitamos y tachar de las descargas pendientes» (mandato verbatim de A1, 1/sep).
Mesa, 2/sep/2026: «solo asegura que estamos usando la infraestructura creada en CODEX para este y cualquier otro encargo que se genere» → REGISTRO por las tres capas, sin reinventar, mecanismo en .claude/commands/adquiere.md §5 y tools/curador_registro/GUIA-CURADOR-REGISTRO.md (enmienda de dirección ya en main, PR #475).

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — contestada por dirección contra 792b7ef ═══ (1) ESTRUCTURA — la de Codex (A5/PR #441), tres capas en este orden: (i) payload: bytes en el corpus compartido (data/raw/ → /home/pc0/mm-corpus/raw/<subcarpeta>) + tests/manifiesto.py --registra --id … --usado-para … --url-origen … --descargado-por "mesa-navegador" --fecha-descarga …, una invocación por --id (A.1), sha/tamaño los deriva el script; (ii) cola del registro: fila por fuente_canonica en data/curacion-registro/cola-adquisicion-registro.tsv (estado_A4A5, ids_manifiesto, nota con fecha y comando); fuente nueva = fila en aliases-fuentes.tsv + fila en la cola citando la receta; después python3 tools/vista_cola_adquisicion.py (data/cola-adquisicion-v1_0.tsv es VISTA GENERADA; T26 falla si no se regenera); (iii) relación: relaciones.tsv + necesidad-objeto-modelo.tsv; python3 tools/curador_registro/via_capa2.py --root . en lectura y --escribe sólo cuando el id resuelve a payload verificado; cierre con tools/curador_registro/baseline.py si el validador lo exige (GUIA §1). (2) CONTENIDO: las filas que el PDF nombra, con su estado hoy en data/cola-adquisicion-v1_0.tsv: IEEH_HIDALGO_SERIE_MUNICIPAL OBTENIDO-SIN-DENOMINADOR · IEE_AGUASCALIENTES_SERIE_MUNICIPAL OBTENIDO-SIN-DENOMINADOR · TEPJF_ELECCIONES_CONCURRENTES_1991_2018 NO-OBTENIDO-POR-ESTE-AGENTE(1) · MEXICO_PANEL_STUDY_2012 NO-OBTENIDO(1) · BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO NO-OBTENIDO(15) · PRICE_AND_INFORMATION_TYPE… NO-OBTENIDO(1) · EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6 NO-OBTENIDO(1) · SICEE NO-OBTENIDO(1). Lista nominal por municipio y federales 2018/2021 por casilla NO tienen fila propia → si mesa las trae, alta de fuente nueva (capa ii) con la receta del PDF como origen. A.13 del barrido anterior (1/sep): 160 archivos, 38 nuevos; control positivo urgencias 10 · wbes 12. (3) COBERTURA RETROACTIVA: manifiesto 29/jul; registro del curador 1/sep (A5); todo lo que mesa deposite es posterior; cubierto.

P1 · INVENTARIO. find "<raíz>" -type f -newermt 2026-09-02 + stat; total examinado y nuevos (A.13). Por archivo nuevo: tipo real por byte 0 (%PDF, PK, Rar!, HTML — el soft-404 de www.ieeags.mx entró al corpus como HTML bajo un 200), zipfile.testzip() para ZIP, sha256 (doble si hay token de sesión, A.7), y a qué fila del PDF corresponde (por nombre y por contenido, no por carpeta). Un archivo que no corresponde a ninguna fila se registra igual con usado_para: "sin necesidad declarada — mesa lo bajó el <fecha>". P2 · REGISTRO por las tres capas (arriba), archivo por archivo; mover/enlazar al corpus compartido y cierre anti-PR#77 (tests/manifiesto.py --verifica --id <id>, una invocación por id, salida cruda pegada: coincide / no_coincide / ausente / raíz-no-configurada, sin colapsar). El .zip del .rar de Hidalgo: id nuevo ieeh_hidalgo_2016_ayuntamientos_zip, usado_para citando ieeh_hidalgo_2016_ayuntamientos_rar como origen (A.7: hash de contenido = del set de archivos internos, además del crudo). P3 · EVALUACIÓN A.4 contra la necesidad (vocabulario obligatorio): por fila del PDF, EXISTE-SATISFACE (qué regla/celda destraba: FAM-M-*/TRA-M-02 no — esas son de L4; Hidalgo/Ags → MAESTRA35-L3; ICPSR → civico.*; etc.) / EXISTE-NO-SATISFACE (qué falta) / NO-OBTENIDO con la nota de mesa verbatim («no aparece», «pide cuenta», «no abre») y receta corregida. Fila de la cola actualizada por enmienda fechada (no se edita la nota anterior); vista regenerada; T26 en verde. P4 · forense/notas/2026-09-0X-MAESTRA35-A1-descargas-pendientes-v3.md: lo que SIGUE pendiente, derivado del registro, con la vía alterna conocida; y la línea de contador.

PERÍMETRO Y CONCURRENCIA: data/manifiesto.yaml (append por línea) · data/curacion-registro/{cola-adquisicion-registro,aliases-fuentes,relaciones}.tsv · data/cola-adquisicion-v1_0.tsv (solo regenerada) · corpus compartido (bytes nuevos) · forense/notas/ · forense/hallazgos.md · forense/firmas-pendientes.tsv (recibo) · A.3 · cascada. NO toca milpa/, corridas-*, tools/ (salvo correr los del curador), data/p0-*. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR CANDIDATOS: una fila de recibo; primer libre al arrancar.

CONTADOR: payloads registrados +N con sha · filas de la cola que cambian de estado +M · descargas pendientes v2 → v3 (número). Declara el real; «+0» también es entregable si mesa no bajó nada (precedente MAESTRA33-A4).

Lo que este acto NO hace: no descarga por red (los NO-OBTENIDO se quedan con su receta); no mide; no toca el motor; no registra a mano fuera de las tres capas.

Sucesores declarados, no lanzados: MAESTRA35-L3 consume Hidalgo/Ags/federales si llegan (o los pide en su P0); dirección relanza lo que siga pendiente sólo si una regla lo necesita.

---

## Enmienda de mesa, verbatim (2/sep/2026, firma e1)

Respuesta de mesa a ACTO MAESTRA35-A1 · REGISTRA-Y-EVALUA-DESCARGAS-3 (2/sep/2026). Firmas verbatim; el ejecutor propaga, no decide.

1. Paso 0: aceptado y agradecido. El hallazgo (bsdtar/libarchive 3.8.8 en /mnt/c/Windows/System32/tar.exe lee RAR3; dentro del sandbox falla por el socket del interop de WSL, no por la herramienta) va a forense/hallazgos.md con los dos comandos y las dos salidas crudas, y a forense/agente-adquisicion-v1_0.md como herramienta de entorno. La lista blanca del sandbox la ajusto yo.
2. Enmienda de dirección al encargo — P0-bis, firma e1: deposita y registra HOY ieeh_hidalgo_2016_ayuntamientos_zip (los tres XLSX que extrajiste, re-empaquetados en ZIP con mtimes preservados), por las tres capas de Codex: manifiesto (--usado-para «pata 2016 de Hidalgo, derivada del .rar ieeh_hidalgo_2016_ayuntamientos_rar ya registrado», --url-origen la del .rar, --descargado-por «derivado-en-caja», --fecha-descarga hoy), A.7 con dos hashes (crudo del zip + hash del set de los tres XLSX, porque un re-empaquetado cambia el crudo), capa cola (fila IEEH_HIDALGO_SERIE_MUNICIPAL: enmienda fechada, ids_manifiesto +1, estado sigue OBTENIDO-SIN-DENOMINADOR salvo lo que diga el punto 3), relación sin cambio, vista regenerada, --verifica una invocación por id. Es un producto en mano, no una descarga: perderlo al cerrar la sesión cuesta una corrida. El resto del acto sigue GATED a Descargas MX > 160.
3. Evaluación A.4 de lo extraído, sin medir nada: ¿alguna hoja de los tres XLSX trae lista nominal? grep -c -i «NOMINAL» por hoja (A.13: cuántas hojas examinaste de las 2+2+168), y pega el encabezado de la primera hoja de AYUNTAMIENTOS_CASILLAS.xlsx. Si la trae, Hidalgo 2016 pasa a EXISTE-SATISFACE por esta vía y lo dices en la fila; si no, queda como estaba y el denominador sigue siendo SICEE.
4. Cierra con un PR de un commit para (2)-(3) + cascada mínima; el CONSUMIDO declara «P0-bis ejecutado, P1-P4 gateados, +0 descargas de mesa». Cuando yo deposite lo de SICEE, se relanza con la compuerta abierta.

---

## CONSUMIDO

Ejecutado por **ACTO MAESTRA35-A1 · REGISTRA-Y-EVALUA-DESCARGAS-3**, 2/sep/2026,
entorno **CAJA/UBUNTU** (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`),
contra `origin/main = 4d7bd1e`. PR de un commit.

**P0-bis ejecutado** (firma e1 punto 2): `ieeh_hidalgo_2016_ayuntamientos_zip`
depositado en el corpus compartido y registrado por las tres capas; A.7 con los
dos hashes (crudo `1de5e344…`, set de los tres XLSX `16bf5826…`);
`--verifica` **COINCIDE** para el id nuevo y para el `.rar` de origen, una
invocación cada uno.

**Punto 3 ejecutado**: evaluación A.4 = **`EXISTE-NO-SATISFACE`**. 86 hojas
examinadas (1+1+84, no 2+2+168 — cifra propia corregida en la nota §2), **0**
aciertos de `NOMINAL`, controles positivos `CASILLA` 3 / `MUNICIPIO` 1. La fila
conserva `OBTENIDO-SIN-DENOMINADOR`.

**Desviación declarada del punto 4.** El texto dictado para este `CONSUMIDO`
era «P0-bis ejecutado, P1-P4 gateados, **+0 descargas de mesa**». Se propaga la
estructura pedida (un PR de un commit, P1-P4 al relanzamiento) pero **no** el
«+0», porque para cuando este acto cerró era **falso contra el árbol**: la
compuerta se abrió a mitad del acto. Verificado tres veces con el comando del
encargo: 16:33 → 160 archivos / 0 nuevos · 16:54 → 160 / 0 · **17:17 → 190 / 30**.
Mesa depositó **30 archivos (558.7 MB) entre 16:56 y 17:10**. El umbral que la
propia firma e1 fijó («GATED a Descargas MX > 160») está **cumplido**.

**P1 ejecutado en lectura** (inventario, sin registrar): 28 ZIP + 2 PDF, ningún
HTML, `testzip` limpio en los 28. Tres hallazgos de contenido en la nota §3:
(a) los paquetes SEE **sí traen `LISTA_NOMINAL`** y `PARTICIPACION` a nivel
municipio (84 filas para Hidalgo 2016) — el denominador que `MAESTRA35-L3`
declaró inalcanzable tras cinco rutas; (b) `ICPSR_35024-V1.zip` es
**documentación otra vez**, cero microdato; (c) los dos PDF de SSRN son de
Bauchet pero **no** son el paper pedido (`2474620`).

**P2-P4 NO ejecutados**: registro y evaluación de los 30 payloads quedan para el
relanzamiento que mesa ya declaró. La compuerta ya está abierta.

Detalle completo: `forense/notas/2026-09-02-MAESTRA35-A1-P0bis-y-evaluacion.md`.

---

## Enmienda de dirección, verbatim (2/sep/2026, firma e2 — relanzamiento)

Enmienda de dirección a ACTO MAESTRA35-A1 · REGISTRA-Y-EVALUA-DESCARGAS-3 (2/sep/2026). Firmas verbatim; el ejecutor propaga, no decide.

1. COMPUERTA: cumplida. Mesa: «Ya descargué lo más que pude. Corramos algo para registrar todo usando la infraestructura de códex.» Verifica por producto al arrancar: find "<raíz descargas_mx>" -type f -newermt 2026-09-02 | wc -l > 0, y pega el número (A.13). Si es 0, PARA y reporta: el depósito no llegó a la raíz que la caja ve.

2. P1–P4 corren íntegros como están escritos. Lo que mesa bajó viene de las filas A1–A4 y B1–B5 del PDF v2 (SICEE ayuntamientos Hidalgo/Aguascalientes/Veracruz, federales 2018/2021 por casilla, TEPJF, ICPSR, LAOMS, Bauchet); no asumas qué llegó: inventaría por byte 0 y contenido, no por nombre de carpeta. Todo archivo de SICEE es fuente NUEVA: alta en aliases-fuentes.tsv (alias sicee_ine → fuente_canonica_normalizada SICEE_INE_ESTADISTICA_ELECCIONES; la fila SICEE que ya existe en la cola queda como origen), fila en la cola por consulta (SICEE_LOCAL_AYUNTAMIENTOS_<ENTIDAD> y SICEE_FEDERAL_DIP_<AÑO>), descargado_por «mesa-navegador», url_origen https://sicee.ine.mx/home, usado_para citando la entrada civico.participacion.tipo_boleta_federal_2016_2024 (propuesta) y el encargo MAESTRA35-L3. Relación (capa iii): necesidad = denominador municipal de la cívica. Para cada archivo de SICEE, en P3: ¿trae LISTA NOMINAL por municipio (o por sección)? grep del encabezado, conteo de hojas examinadas; si la trae, la fila IEEH_HIDALGO_SERIE_MUNICIPAL (o IEE_AGUASCALIENTES_…) pasa de OBTENIDO-SIN-DENOMINADOR a OBTENIDO por enmienda fechada, citando el id de SICEE que lo cubre.

3. COMPRANET cambió de dominio. Mesa: «Compranet pasó a https://upcp-compranet.buengobierno.gob.mx/». Es identidad nueva, no descarga: (a) alias compranet_upcp → la fuente_canonica de la fila EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6 en aliases-fuentes.tsv, con evidencia_ref «mesa, 2/sep/2026»; (b) url_conocida de esa fila por enmienda fechada (la nota anterior, con los dos dominios muertos, se conserva); (c) sonda desde la caja, salida cruda: curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://upcp-compranet.buengobierno.gob.mx/ con UA por defecto y con UA de navegador (L3 midió que ieehidalgo da 403/200 según UA); (d) si responde, /adquiere-adyacente: localiza catálogo de proveedores o documentación de API (≤4 rutas, A.5, receta ≤1 min si falla), doble descarga con sha idéntico, tres capas, anti-PR#77; si no responde, la fila queda NO-OBTENIDO-POR-ESTE-AGENTE(N intentos) con el dominio nuevo anotado — eso ya es avance sobre «dominio por localizar».

4. Cierre: python3 tools/vista_cola_adquisicion.py, T26 verde, via_capa2.py --root . en lectura (recuerda FP-246: las filas con ids_manifiesto en lista caen fuera del contador; decláralo, no lo repares), baseline.py si el validador lo pide, tests/check.py --baseline VERDE. pendientes-v3 con lo que siga vivo. Un PR.

Lo que NO cambia: nada se mide; no se toca milpa/; no se registra nada fuera de las tres capas; los archivos que no correspondan a ninguna fila se registran igual con usado_para «sin necesidad declarada — mesa lo bajó el 2/sep».

---

## CONSUMIDO — relanzamiento (enmienda e2)

Ejecutado por el **relanzamiento** de **ACTO MAESTRA35-A1 · REGISTRA-Y-EVALUA-DESCARGAS-3**,
2/sep/2026, entorno **CAJA/UBUNTU** (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`,
sonda INEGI `200`), contra `origin/main = 19770f2` al arrancar (fusionado durante el
acto con `origin/main = 6024c32`, `PR #480 · ACTO MAESTRA35-L6`, sin PARO — perímetro
re-derivado, conflicto de puro-apéndice en `data/curacion-registro/cola-adquisicion-registro.tsv`
y su vista, resuelto por la convención de la casa: `origin/main` primero, lo propio después,
verbatim). `ADR-300` (renumerado de `297` a `300` en cadena por el resto de la jornada, sin
colisión propia — este acto fusiona después de `297`/`298`/`299`, ya resueltos por otros actos).

**COMPUERTA re-verificada al arrancar**, por el mismo comando que fijó la firma `e1`:
`command find "/mnt/c/Users/PC0/Descargas MX" -type f -newermt 2026-09-02 | wc -l` → **30**
(sobre **190** examinados). Sigue `CUMPLIDA`.

**P1-P4 ejecutados íntegros.** P1: 30 archivos nuevos inventariados por byte 0 y contenido
(28 ZIP `testzip()` limpio + 2 PDF). P2, tres capas: (i) 30 payloads al corpus compartido,
`tests/manifiesto.py --registra` ×30 + `--verifica` ×30 → **30/30 `COINCIDE`** (anti-PR#77);
(ii) 12 filas nuevas en la cola (`NUEVA-A1`, 3 locales + 9 federales SICEE), vista regenerada;
(iii) alta de fuente SICEE (`sicee_ine`, necesidad nueva `N37`, relación `REL-6c677146f183f594c0649a61`
`CONFIRMADA`), `baseline.py` VERDE, `via_capa2.py` lectura 0 diffs (`FP-246` declarado, no aplica).
P3: `IEEH_HIDALGO_SERIE_MUNICIPAL` e `IEE_AGUASCALIENTES_SERIE_MUNICIPAL` pasan de
`OBTENIDO-SIN-DENOMINADOR` a `OBTENIDO` (denominador municipal vía `LISTA_NOMINAL` de SICEE,
verificado 84 = municipios de Hidalgo, 11 = municipios de Aguascalientes); `MEXICO_PANEL_STUDY_2012`
y `PRICE_AND_INFORMATION_TYPE...` sin cambio de estado (contenido evaluado, no satisface).
Punto 3 (COMPRANET): dominio nuevo confirmado y sondeado (200/200), alias `compranet_upcp` dado
de alta, `/adquiere-adyacente` (4 rutas) sin catálogo accesible por `curl` (SPA), estado sube a
2 intentos con receta de navegador. P4: `forense/notas/2026-09-02-MAESTRA35-A1-descargas-pendientes-v3.md`.

**Desviación declarada, propia y autocorregida**: el bucle de registro de los 30 payloads
reusó un único `--url-origen`/`--licencia` de SICEE para las 30 invocaciones; las 3 no-SICEE
(ICPSR + 2 SSRN) quedaron con procedencia falsa (nunca `sha256`/`tamano_bytes`, que el script
deriva). Detectado antes del commit, corregido por línea con nota fechada, declarado en
`forense/hallazgos.md`.

`python3 tests/check.py --baseline` → **VERDE** (19 FAIL / 168 WARN, nada nuevo).

**CONTADOR real**: payloads registrados **+30** (con sha) · filas de la cola que cambian de
estado **+3** · filas nuevas en la cola **+12** · descargas pendientes v2→v3: 0 recetas del
paquete original de agosto pasan a cumplidas por esta vía; el avance real es el denominador
municipal/federal de la pieza cívica (`N37`).

Commits: `63358eb` (P1-P3) · `c0704f5` (hallazgos) · `c71bfa4` (merge `origin/main`) ·
`650bc52` (cascada ADR-300/L0/P4). PR abierto contra `main`, sin fusionar — el merge es de mesa.
