# GEN2-ASTRA5-U5-ADQUISICION-1 · nota de cierre (24/sep/2026)

**Contadores.** Cero mediciones; no adopta. Mueve el manifiesto: **782 payloads nuevos** (4.09 GB): 712 en `data_raw` y 70 en `reserva_respondentes`. De esos 70, 27 son bases con `RESERVADA-NO-ABIERTA-NO-INDEXAR-L` y 43 son documentos con `DOCUMENTACION-ESTRUCTURAL-NO-RESPUESTAS`. También mueve el contador de existencia del mapa: `NO-ACCESIBLE-DESDE-SANDBOX` baja de 130 a **0**. No se abrió microdato. Bajar y hashear no es abrir: sólo sha256, tamaño, directorio central del zip, lista de miembros de un tar, `%%EOF` o la dimensión OOXML de una hoja.

- ADR `ADR-260924-GEN2-ASTRA5-U5-ADQUISICION-1-43d6-01`. La raíz `43d6` viene del 0-bis `43d6f41f`.
- Encargo: `forense/encargos/2026-09-24-GEN2-ASTRA5-U5-ADQUISICION-1.md`. Sello de cuerpo `97dc4444…cc6fd`. SHA de redacción `3423b498`; base del 0-bis `3252aaec`.
- Rama `acto/gen2-astra5-u5-adquisicion-1`, en CAJA. La sesión corrió entera en Claude Opus 5.5 (1M); el encargo pedía Opus. Hubo ejecutores Sonnet (cinco lotes de P4, dos de constancias, cuatro de localización y vías alternas, uno de `/sonda`), auditados por el supervisor: validación mecánica, re-descarga de una muestra al azar y reclasificación explícita.

## 1 · Arranque y premisas

`[EJECUTADO]` Base al día (`0.a` = 0) y árbol limpio. Duplicado: el worktree viejo `mm-adq-astra5-u5-20260923` es de otro rótulo, con PR #1094 **fusionado** (registro documental, 0 filas de cola). El encargo decía que esa rama se borró sin fusionar. Entorno: `red=200`, corpus montado (490 archivos examinados), `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` ausente → CAJA.

Premisas que cayeron. Todas son de logística; el objetivo siguió alcanzable y se declara qué se hizo en su lugar:

| premisa del encargo | lo medido | qué se hizo |
|---|---|---|
| «manifiesto: 0 payloads de ensanut, encodat, enbiare…» `[EJECUTADO]` | 146 entradas ENSANUT (2024 completa, cuestionario 2018), ENBIARE 2021 (bd + fd), ENADIS 2022 ×4, ECOPRED 2014 | A.8: ENSANUT 2024 y ENBIARE 2021 entran a la cola como OBTENIDO con sus ids, sin volver a bajarse |
| rama `codex/adq-astra5-u5-20260923` «se borró sin fusionar» | fusionada por PR #1094 | se cita; no dejó filas de cola |
| `estado: VERIFICADO` / `estado_reserva: RESERVADA` en el manifiesto | el esquema no tiene `estado`; `ESTADOS_RESERVA` sólo acepta dos valores y exige `raiz: reserva_respondentes` (`tests/manifiesto.py:244-310`) | se usó el vocabulario vigente (precedente ENCO, 16/sep); la verificación queda en `--verifica` COINCIDE |
| `grep -c 'id: ensanut_\|…'` > 0 | con los ids como nacieron (`ensanut2018__…`) daba 0; ningún id del manifiesto tenía esa forma | los 721 ids propios se renombraron a `ensanut_<ola>__`/`encodat_<ola>__` antes de fusionar; el comando da 721 |
| «ENCODAT 2016–17 primero» | el INSP publica también **ENCODAT 2025**, y ENSANUT tiene Continua **2025** (2026 responde 302 sin bases) | E.6 y F-ASTRA-5-3: 2025 es la ola más reciente de ambas y nace RESERVADA; el histórico entra abierto |
| prioridad 1: 111 · 2: 49 | cierto sobre la hoja entera; las 163 ADQUIRIR son **todas** prioridad 3 | la firma F-ASTRA-5-2 lleva prioridad 0 |

## 2 · P1 · de la hoja a la cola

`tools/dominios/hoja_a_cola.py` clasifica las 163 filas ADQUIRIR con la tabla de reglas `tools/dominios/hoja_a_cola_reglas.tsv` (regex ordenadas, regla 999 por defecto DOCUMENTO): **64 MICRODATO**, 49 TABULADO y 50 DOCUMENTO. Salen 39 (instrumento, ola) de microdato. Dos grupos ya tenían fila en la cola y no se duplican: `BANXICO_IMOR_CONSUMO_POR_PRODUCTO_MENSUAL` y `LATINOBARÓMETRO` 2024. La firma F-ASTRA-5-2 aporta 14 (instrumento, ola), de los cuales 6 se solapan con los de la hoja. Total: **47 filas nuevas** de registro con clave `ASTRA5-U5:<INSTRUMENTO>_<OLA>`, escritas con `upsert_fila`. La vista se regenera por comando. `--verifica` sale 0.

Los 78 DOCUMENTO/TABULADO no entran a la cola; van a `forense/analisis/dominios/constancias-v1_0.tsv`. El test es `tests/test_hoja_a_cola.py`: vista byte a byte, `--verifica`, cobertura de clases y un caso sintético de orden de reglas. Hay control positivo: la vista mutada sale ROJO.

**Constancias** (cuatro pasadas; bitácora por URL en `constancias-bitacora-2026-09-24.tsv`). Resultado: **40 EXISTE-SATISFACE, 21 EXISTE-NO-SATISFACE, 16 NO-ENCONTRADO, 1 NO-ACCESIBLE**. La única NO-ACCESIBLE es ENIGH 2024, que es ola reservada. El estado se fija por evidencia de fetch: sha256, código 2xx, estructura válida y una URL que no sea localizador. No se guardan copias en el repo, que es público y los documentos son de terceros: la identidad queda por sha256 + URL. Hay obras académicas tras Cloudflare que quedaron **identificadas por metadatos** en OpenAlex, sin copia.

## 3 · P2 · reconciliación con F-ASTRA-5-2

`tools/dominios/firma_astra5_2.tsv` declara las 14 (instrumento, ola) de la firma:
- **ENSANUT**: 2006, 2012, 2016, 2018, 100k 2018, 2020, 2021, 2022, 2023, 2024 y 2025.
- **ENCODAT**: 2016–2017 y 2025.
- **ENBIARE**: 2021.

Todas llevan prioridad 0. Las afirmaciones del mapa que las requieren se derivan por patrón (`patron_mapa`), no se teclean. Ejemplos:
- ENSANUT 2022: SALUD-009/014/024/025, JUV-009, CONOC-010/011, SALMEN-013.
- ENCODAT 2025: SALUD-007/008/017/018/019/034/039, JUV-010.
- ENBIARE: CLASE-005/018/019/020/040, EMOC-028, SALMEN-018/019/024.

Cinco olas no tienen afirmación en el mapa que las nombre: ENSANUT 2006, 2016, 100k 2018, 2020 y 2025. Se adquieren igual por firma, y la fila lo dice.

## 4 · P3 · `/adquiere` en caja

Por payload: doble descarga A.7 idéntica (o miembros idénticos), estructura verificada, registro por **apéndice** al manifiesto y `--verifica` al cerrar. El registro reutiliza las funciones de `tests/manifiesto.py`: sha y tamaño derivados del archivo, deduplicación por sha y validación. Se escribe por apéndice porque el volcado canónico re-envuelve unas 90 líneas escritas a mano por otros actos. Verificación final: **651 COINCIDE** en `data_raw` bajo los prefijos `ensanut_`/`encodat_` más el resto por tanda, y las 70 entradas de `reserva_respondentes` coinciden por sha directo. `--verifica` las reporta como `FUERA_DE_PERIMETRO` por diseño.

| instrumento | payloads | ruta y nota |
|---|---:|---|
| ENSANUT 2006, 2012, 2016, 2018, 100k 2018, 2020, 2021, 2022, 2023 | 643 | POST `ArchId` (INSP); stata + catálogo + cuestionarios; abiertas |
| ENSANUT Continua 2025 | 62 | **RESERVADA** (24 bases + 38 documentos estructurales) |
| ENCODAT 2016–2017 / 2025 | 8 / 8 | `encuestas.insp.mx`; 2025 **RESERVADA** |
| ENPECYT 2017, ENDISEG 2021, ENADID 2018, MMSI 2016, ENSU 2024 (trae T1), EDR 2015–2019 (trae 2017) y 2022 | 12 | INEGI (API de descarga masiva, vía el agente) |
| EMAT 2010–2014, 2015–2019, 2020, 2021, 2022, 2023 | 6 | 2013–2019 sólo existen en paquetes quinquenales; enlaces por render de la SPA |
| Latinobarómetro 2023 · Wellcome Global Monitor 2018 · PISA 2022 (SPSS estudiantes, 440 MB) | 3 | Wellcome: el XLSX público trae la hoja «Full dataset» 149 015 × 60 (hallazgo de `/sonda`); PISA por rangos en paralelo |
| ENCOVID-19 2020: 7 rondas nacionales | 26 | Zenodo CC-BY, registros verificados por API |
| INE cómputos 2024 | 1 | captura Wayback del archivo oficial (el origen responde 403) |
| Réplicas: Cantú 2019 · Imai-King-Velasco 2020 (2.4 GB) | 2 + 3 | Harvard Dataverse |
| Banxico SIE CE81 (remesas) · CF297 (financiamiento a hogares) | 2 | POST del cuadro completo; A.7 excluye la línea «Fecha de consulta» |
| SESNSP víctimas del fuero común 2015–2025 · CONDUSEF REDECO (2 cortes) | 1 + 2 | **datastore CKAN** de `www.datos.gob.mx`: `repodatos.atdt.gob.mx` niega por IP (Akamai) a Linux, a Windows y a Chrome; misma fuente, otra ruta, re-serializada; filas = total declarado |
| Índice SHF de Precios de la Vivienda | 3 | XLSX al 2T-2026 bajado con el **navegador real** (`--descarga`), CSV 2005–2017 de Wayback y nota metodológica |

Cola ASTRA5-U5 (47 filas): **36 OBTENIDO**, 1 OBTENIDO-PARCIAL (REDECO: CKAN sólo publica dos cortes), 6 NO-ACCESIBLE (solicitud, términos o comité), 3 NO-OBTENIDO-POR-ESTE-AGENTE y 1 NO-ENCONTRADO. Cada fila no obtenida trae en `nota` sus rutas agotadas y la receta de un minuto (§8).

## 5 · P4 · las 130 fuentes

Primera pasada: cinco ejecutores con la receta, 340 intentos. Siguieron tres pasadas del supervisor desde CAJA fuera del sandbox:
1. **Red real y `curl.exe` de Windows**. Varios `curl: (7)` de los ejecutores eran el proxy del sandbox con un host no declarado, no el sitio (A.13).
2. **Navegador real**.
3. **Vías alternas**: Europe PMC, `locations` de OpenAlex, Unpaywall, DSpace de CEPAL, CKAN, SIDOF y SIL, CESOP.

`forense/analisis/dominios/ensambla_mapa.py` lee `bitacora-existencia-*.tsv` y deriva `existencia_documento` en vocabulario A.4 con sufijo `-DESDE-CAJA`. Un EXISTE sólo cuenta con evidencia de fetch; un reintento de la misma URL sustituye al anterior. Resultado: **61 EXISTE-SATISFACE, 14 EXISTE-NO-SATISFACE, 41 NO-ENCONTRADO, 14 NO-ACCESIBLE**. Sólo cambia esa columna de la hoja (130 celdas). `canon/mapa-dominios-v1_0.tsv` y todos los dictámenes quedan intactos (`--verifica` 0).

Muestra auditada al azar: 15 filas EXISTE re-descargadas por el supervisor; 15 de 15 responden 200 con la misma identidad (8 con sha idéntico, el resto páginas dinámicas con el mismo título).

Caso con universo declarado (A.13), APUEST-038: el índice completo de sanciones de COFEPRIS 2012–2026 son 52 PDF examinados por texto; ninguno nombra a Laboratorios Imperiales ni la BCG. La única coincidencia con «Imperial» es un hotel, 2014.

## 6 · Herramienta nueva, por instrucción del titular

Mensajes del titular en la sesión, verbatim:
- «Necesito que asegures que estamos obteniendo toda la información y data suficiente y necesaria, si es tema de accesos lo resolvemos, pero no por un permiso que no se ha aceptado. Tenemos toda una maquinaria disponible de obtención y catalogación de activos como para no usarla.»
- «Revisa si no hay nada que instalar, pandas o cualquier otra especie de skill o procesador que nos ayude a este y otros procesos de adquisición.»
- «resuelvelo aquí, se que cae fuera del acto pero si no lo asentamos ahorita se nos pierde y esto es replicable y reutilizable para cualquier descarga»
- «Para todo aquello que nop haya sido accesible por los métodos identificados o estandar, necesito que pienses fuera de la caja, eres opus 5.5 revisa otras formas de acceder a esos registros.»

`tools/renderiza_pagina.py` usa el Chrome/Edge de Windows en headless, por interop y fuera del sandbox. Clasifica sobre el DOM: `RENDERIZADO`, `RETO`, `ERROR-RED:<ERR_*>` o `VACIO`. Extrae enlaces, y en modo `--descarga` usa un perfil nuevo por llamada, detecta el archivo en Descargas de Windows y lo mueve.

Tiene cinco defectos reales medidos y fijados en su test (`tests/test_renderiza_pagina.py`, 17 casos):
- el reto «Challenge Validation» de gob.mx (200, 1 881 B);
- el Cloudflare en español («Un momento…»);
- las páginas de error de red de Chrome, cuyo título es sólo el host;
- el DOM que es sólo scripts (DOF);
- que un perfil que ya pasó el reto no dispara la descarga.

Está cableada en `/adquiere` §3 como ruta (v). Los dos tests nuevos entran al censo de guardias como `CORRE-EN-CI`: `--ejecuta-huerfanos` corrió 113 y ninguno falló.

Qué no hace: no pasa Cloudflare ni bloqueos por IP (quedan `RETO`), no llena formularios y no inicia sesión.

Recomendación de instalación, que no se aplicó: `aria2`, `p7zip-full`/`unar` y `jq` requieren `sudo` del titular. Para PISA y las réplicas bastó la descarga por rangos con `curl -r`.

## 7 · Respuestas de mesa en la sesión, verbatim

- Tanda 3 fuera del sandbox, que el clasificador del modo automático había negado: «aprobado».
- Catalogación: «Solo documentación (Recomendado)». **No se ejecutó.** El catálogo vigente (`data/inventario-reactivos-v1_2.tsv`, `inventario-fd-v1_1`/`-ext`) es un producto versionado por acto con COMMIT-1/2. Ni ENSANUT 2024, que entró el 3/sep, tiene filas. Correr `tools/inventario_fd.py` escribió la versión obsoleta `v1_0` (+635 líneas) y se revirtió. Queda como NC con sucesor.
- Fuentes con registro: «Prueba otras formas y métodos de obtener la información ya habíamos tenido un problema similar y un agente creó una especie de protocolo para probar otras rutas, si tienes duda le pido a mesa que la busque y te comparto el detalle si tu la puedes encotnrar adelante.» Se aplicó `/sonda` LATERAL + HERMANAS (el protocolo). Recuperó Wellcome 2018, identificó la vía de ICPSR para EMOVI 2006 y confirmó los canales de acceso de IFPS y MCPS.

## 8 · Recetas de un minuto (titular)

| objeto | receta |
|---|---|
| EMOVI 2023 / 2011 | https://ceey.org.mx/contenido/que-hacemos/emovi/ → Bases de datos → formulario de solicitud (nombre, institución, uso) → enlace por correo. 2006: ICPSR 35333 con cuenta gratuita |
| WVS ola 7 EE.UU. y Japón | https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp → país → Data files → aceptar condiciones → `WVS_Wave7_<país>_Stata.zip` a Descargas MX |
| WVS longitudinal 1981–2022 | https://www.worldvaluessurvey.org/WVSEVStrend.jsp → Time-Series 1981-2022 → Stata |
| IFPS México 2020–2021 | https://foodpolicystudy.com/contact/ → solicitud al equipo (Dra. Christine White) |
| MCPS | https://www.ctsu.ox.ac.uk/research/mexico-city-prospective-study/data-access → formularios de registro y de solicitud (institucional) |
| INEGI pobreza multidimensional 2024 | https://www.inegi.org.mx/desarrollosocial/pm/ en navegador → pestaña Programas de cálculo / Datos abiertos → zip |
| EQD 2018 | https://www.openicpsr.org/openicpsr/search/studies?q=Mexico%202018%20panel en navegador, o solicitud a Greene/Simpser |
| ENEM 2024 | siguiente release de CSES Module 6 (el de dic-2025 no incluye México) o solicitud al CIDE |
| REDECO histórico | cortes anteriores a 30/09/2025: `repodatos.atdt.gob.mx` sólo responde desde otra red (bloqueo por IP) |

## 9 · Defectos heredados (fuera del perímetro, declarados)

1. **Id duplicado en el manifiesto de `main`**: `enoe_n_diseno_muestral_pdf`, escrito por `4ed8176b` (ASTRA5-U1) y `0e671c1a` (ASTRA5-DOCS), mismo sha y mismo archivo. Desde el 23/sep hacía fallar **toda** escritura por `tests/manifiesto.py` (`id duplicado`), incluida la de `/adquiere` del cron. Se corrigió en `96790872` (D-21, ≤10 líneas): se conserva la primera entrada, cuyo `usado_para` absorbe la procedencia de la segunda; ningún sha cambia.
2. **`estado_reserva` fuera del vocabulario**: `RESERVADA-ASTRA5-U1-ULTIMA-OLA-CORPUS-NO-ABRIR` en `enoe_2026_1t_csv` y `enoe_2026_1t_microdatos` (ASTRA5-U1, `4ed8176b`), con `raiz: data_raw`. El validador rechaza el manifiesto completo, así que `--registra` sigue roto para todos. Esa etiqueta la lee la guardia E.6 de `tools/dominios/enoe/pisos.py`, y cambiarla o relajar el validador es tocar la guardia de otro acto. Este acto la exime **por nombre** en su propio registrador y lo lleva a mesa (FP-…-02).

## 10 · Exposición declarada (E.6: categoría, no contenido)

- ENSANUT 2025 y ENCODAT 2025, olas RESERVADAS: se leyeron sólo sus páginas de descarga (nombres de archivo e identificadores `ArchId`). No se leyó ningún informe, tabulado ni comunicado.
- Un ejecutor Sonnet de la cuarta pasada, cuya instrucción no repitió la regla de reserva (omisión del supervisor), pidió la página de programa de **ENIGH 2024** (`https://www.inegi.org.mx/programas/enigh/nc/2024/`). Respuesta: una carcasa SPA de 3 918 B sin cifras. Los bytes se borraron y la fila se excluyó de la bitácora. Ningún número de ENIGH 2024 entró a la sesión.
- Wellcome 2018: la dimensión de la hoja «Full dataset» se leyó del XML OOXML (`<dimension ref>`), sin leer celdas. Wellcome no es ola reservada.
