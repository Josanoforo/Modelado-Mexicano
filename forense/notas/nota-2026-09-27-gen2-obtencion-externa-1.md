# ACTO GEN2-OBTENCION-EXTERNA-1 · nota de cierre

Encargo: `forense/encargos/2026-09-27-GEN2-OBTENCION-EXTERNA-1.md` (A.3; sha256 del adjunto recibido `09b41e34…4b853c`; SHA de redacción `eda5bb9f`). Rama `acto/gen2-obtencion-externa-1`, 0-bis `81e18980`. ADR `ADR-260928-GEN2-OBTENCION-EXTERNA-1-81e1-01`.

**Contadores movidos: cero mediciones, cero adopciones.** Lo único que se mueve es `payloads` del manifiesto (§5).

## 1 · Arranque (salida cruda, resumida)

- `git rev-list --count HEAD..origin/main` → 0 al abrir; `git status --porcelain` vacío; duplicado: sin rama, worktree ni PR con `OBTENCION-EXTERNA` (0.c); `limpia_arbol --reporta`: base al día, `fuera_de_politica: 0`.
- `tools/entorno.py --arranque`: `ENTORNO-DERIVADO = CAJA` · `montado=SI archivos_examinados=512` · `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable` · `red: PERMITIDA (http_code=200)`. El encargo pide CAJA: coincide.
- `data/raw` enlazado a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiado del clon padre y ampliado (local, gitignorado) con `reserva_respondentes: /home/pc0/mm-corpus/reservas-respondentes`, para que `--verifica` resuelva las olas reservadas.
- Adjuntos (§3 del encargo): **no llegaron**. Ni el informe de investigación del 27/sep ni `REVISION-repo-y-fuentes-alternas-2026-09-27.md` están en `Descargas MX` ni en `Downloads` (listados con `ls -t` fuera del sandbox). El §1 del encargo es autosuficiente; sus cifras se tratan como [REPORTADO] y se re-verifican al bajar.

## 2 · Premisas re-derivadas (A.15, por id, 7 049 entradas examinadas)

| premisa del encargo | rótulo | lo que dice el manifiesto hoy | efecto |
|---|---|---|---|
| ECRIGE-CDMX 0 entradas | EJECUTADO | 0 (patrón `ecrige\|catalog/601\|regulatoria.*cdmx`) | se sostiene |
| ENVE: «hoy 2016 y 2024» | EJECUTADO | 7 entradas: **2012, 2014, 2016, 2018** (todas bases de *ejemplo* de 2.3–2.5 KB; 2018 reservada) + 2024 (datos abiertos + 2 cuestionarios) | cae (logística): las olas existen pero sólo como ejemplo; P1 completa lo público por ola |
| ENCRIGE 2016 sólo ejemplo | EJECUTADO | `cc1_inegi_encrige_2016__ejemploencrige_csv` (6 116 B, reservada) + página de programa | se sostiene |
| ENCIG 2025 FD/cuestionario «si no está» | EJECUTADO | `encig25_cuestionario_pdf` y `encig25_estructura_base_datos_pdf` **ya están** | EXISTE-SATISFACE; nada que bajar |
| `zenodo_electoral…` y `ine_conteos_censales…` «ya en corpus» | EJECUTADO | zenodo: 1 zip v1 «Static» (739 952 144 B); conteos: sólo 2024 (+ prisión preventiva y voto anticipado 2024); 2009–2021 SIN-FETCH por host `portal-pruebas.ine.mx` caído el 1/sep | P2 verifica versión y reintenta olas |
| Imai-King-Velasco 2020 por bajar | EJECUTADO | **OBTENIDO** por GEN2-ASTRA5-U5 (fila `ASTRA5-U5:IMAI-KING-VELASCO-REPLICA_2020`) | se cita; P3 sólo compara archivos |
| `python3 tools/manifiesto.py verifica <id>` | EJECUTADO | la herramienta es `tests/manifiesto.py --verifica --id <id>` | logística; se usa ésa |
| registro por `/adquiere` | EJECUTADO | en `eda5bb9f`, `tests/manifiesto.py --registra` aborta por dos entradas ajenas con `estado_reserva` fuera de vocabulario (`enoe_2026_1t_*`, FP-…-43d6-02); MAPA-INSTRUMENTOS-ALTERNOS-1 lo arregló en paralelo (#1255, 28/sep) y además `--registra` re-serializa todo el YAML | se registra por apéndice validado, mismo método que CORPUS-COMPLETO-1 (`registra_obtencion_externa.py`): no toca líneas ajenas |

Regla de reserva aplicada (fila `reserva:ola-nueva-de-encuesta-con-historia` de `data/corrida0/decisiones.tsv`, lectura operativa (a): «encuesta con historia» = el manifiesto ya trae ≥ 1 ola): ENVE 2018/2020/2022, ENCRIGE 2016 y toda ola de ECCO distinta de 2023 entran RESERVADAS; ENVE 2012/2014/2016 (olas ya abiertas), ECRIGE-CDMX 2019 (encuesta sin historia en el corpus) y todos los registros administrativos (INE, IECM, Mecanismo, QQP) entran ABIERTOS. Se declara para que mesa lo corrija si lee otra cosa.

## 3 · Instrumento

- `forense/analisis/obtencion-externa-1/baja.py`: doble descarga con UA de navegador, sha crudo y neutralizado (A.7), estructura (ZIP `testzip`, PDF `%%EOF`, JSON), detector del soft-404 de INEGI. **Control positivo** (antes de usarlo): `ejemploencrige_csv.zip` → sha `6e0dfb28…9b772`, idéntico al manifiesto; **control negativo**: ruta inventada → `FALLO-SOFT404-HTML` (2 263 B). Los dos archivos de prueba se borraron.
- `forense/analisis/obtencion-externa-1/registra_obtencion_externa.py`: deriva sha y tamaño del disco, exige bitácora A.7, deduplica por sha, anexa con validación completa.
- Ejecución: P1, P2(i–ii), P2(iii–iv) y P3 en cuatro subagentes Sonnet con perímetro propio (sólo su `lote-*.tsv`, su bitácora y su carpeta); P4, el registro y la auditoría en el hilo principal (Opus). Declarado según D-13 y la cabecera del encargo. **Incidencia:** los subagentes de P2(iii–iv) y P3 quedaron detenidos ~10 h (sin proceso vivo; probablemente en espera de un permiso) sin escribir su `lote-*.tsv`. Se detuvieron por `TaskStop` el 28/sep ~08:30; sus bitácoras A.7 estaban completas y cuadraban con el disco (P2b 88/88, P3 17/17), así que el hilo principal reconstruyó sus tablas desde las bitácoras y terminó lo que faltaba (IECM entero; JEMS, ECCO, DOI de pago, conciliación de Phillips, dos ediciones de Banxico, 6 PDF del índice del Mecanismo).

## 4 · P4 · solicitudes con identidad

Once archivos en `forense/analisis/obtencion-externa-1/solicitudes/` (índice `00-LEEME.md`). Vía verificada en la sesión: LGTAIP (DOF 20-03-2025) bajada y registrada (`oe1_p4_lgtaip_dof_2025_03_20_pdf`), arts. 3-V, 130, 134, 144 leídos; PNT viva con módulo SISAI. Estado por letra: (a) Banxico, (b) IECM, (c) Segob, (d) Félix-Brasdefer, (e) Delaney/FIU, (f) Worldpanel: PREPARADA, NO ENVIADA · (g) LM INEGI: **ARCHIVADA-NO-NECESARIA** — el 27/sep MAPA-INSTRUMENTOS-ALTERNOS-1 sólo tenía su 0-bis y la pieza quedó condicionada; el 28/sep #1255 fusionó y su mapa da ENCRIGE 2020 (empresa, todos los tamaños) y ENVE 2024 como EXISTE-SATISFACE-PARCIAL para R03 y recomienda no abrir trámite de identidad por ENAPROCE: se toma la rama «si no» del encargo (`solicitudes/g-inegi-lm-enaproce.md`) · registros con identidad: cuatro listados con URL comprobada.

## 5 · Hallazgo lateral: la NC de caja de OBTENCION-PREVIA-1

`NC-260928-GEN2-OBTENCION-PREVIA-1-8e6a-02` (ABIERTA, «DIFERIDO-A:caja -- bajados desde nube; no están en el corpus compartido»). Al verificar `P4-I1` por id, los 14 payloads que ese acto registró desde nube estaban AUSENTES en caja. Se trajeron por id y **14 de 14 COINCIDEN** (`tests/manifiesto.py --verifica`): 1 por `--descarga --id` (el ZIP de datos abiertos), 13 por curl con comparación de sha contra el manifiesto antes de colocar (`--descarga` rechaza URL sin extensión: las 8 páginas de programa y las 5 descargas del RNM). La fila NC no se edita (es ajena; PARO b): **mesa o el trámite la cierra citando esta nota**. Además, la solicitud del LM de ese acto cita el formato en una ruta que no es la registrada: el mismo sha (`5a5d041d…`) está bajo `inegi_laboratorio_microdatos_solicitud_uso`.

## 6 · Resultados por pieza (detalle: `forense/analisis/obtencion-externa-1/obtencion.tsv`, 179 filas; por lote: `lote-P{1,2a,2b,3,4}.tsv`)

| pieza | objeto | resultado |
|---|---|---|
| P1 | ECRIGE-CDMX 2019 | datos abiertos (ZIP, 370 miembros) y cuestionario OBTENIDOS; FD NO-OBTENIDO-POR-ESTE-AGENTE(10); microdato completo NO-ACCESIBLE (RNM 601, Laboratorio). Encuesta sin historia en el corpus → ABIERTA |
| P1 | ENVE 2012–2022 | datos abiertos 2016/2018/2020/2022, cuestionarios de las seis olas y FD 2012/2014 OBTENIDOS (2018/2020/2022 RESERVADAS, 6 payloads en `reserva_respondentes`, no leídos); datos abiertos 2012/2014 y bases de ejemplo 2020/2022 NO-OBTENIDO-POR-ESTE-AGENTE(4); microdato completo NO-ACCESIBLE (condición verbatim en RNM 815 y 1058) |
| P1 | ENCRIGE 2016 microdato | NO-ACCESIBLE (RNM 264: Laboratorio); en corpus sigue la base de ejemplo reservada |
| P1 | ENCIG 2025 FD y cuestionario | YA-EN-CORPUS (`encig25_cuestionario_pdf`, `encig25_estructura_base_datos_pdf`) |
| P2(i) | Zenodo electoral | YA-EN-CORPUS y **verificado**: la API da una sola versión (Static_v1, concepto 14991954), título idéntico al del artículo DOI 10.1038/s41597-025-04918-9; JSON de API y Crossref registrados como evidencia |
| P2(ii) | INE cómputos federales por casilla 2012, 2015, 2018, 2021 | OBTENIDOS (2012 vía Wayback de ife.org.mx; 2018/2021 vía Wayback: los hosts `computosAAAA.ine.mx` ya no resuelven; 2015 es RAR v4 con extensión `.tar.gz`, 3 miembros listados con `tar.exe`); 2024 YA-EN-CORPUS |
| P2(ii) | Conteos Censales de Participación 2009–2021 | OBTENIDOS las 5 olas (hoy en `ine.mx/wp-content/uploads/2022/04/`); con 2024 la serie queda completa |
| P2(iii) | IECM SEPCOPP/SERCOPP, COPACO (resultados e integración) | NO-OBTENIDO-POR-ESTE-AGENTE(11): captcha de Radware para curl y para Chrome real (no se elude); 0 paquetes de resultados en los CKAN de CDMX y federal. Catálogos de colonias/UT 2019 y 2022 del IECM OBTENIDOS por `datos.cdmx.gob.mx` (PROPUESTO-POR-EJECUTOR). Cubre el resto la solicitud (b) |
| P2(iv) | Mecanismo de Protección, informes | 94 PDF del índice OBTENIDOS: 89 mensuales (may/2018–jul/2026; dic/2024 enlazado dos veces con el mismo sha → 88 ids) y 5 anuales (PROPUESTO-POR-EJECUTOR). dic/2018 y mar–dic/2019: NO-ENCONTRADO en el índice |
| P3 | Phillips 2017 | dta, do, apéndice y artículo OBTENIDOS del sitio del autor. **Conteo conciliado**: el propio texto dice «more than 70 municipalities» (introducción) y «There are 76 municipalities coded “1” for the variable» (datos); el 76 del proyecto es exacto |
| P3 | De La O 2013 AJPS | paquete de replicación (dta + do) y SI OBTENIDOS; el `adq15_jpal_…24ft7wz` del corpus es otro paquete |
| P3 | Imai, King & Velasco Rivera 2020 | YA-EN-CORPUS (ASTRA5-U5) + 3 tar que faltaban OBTENIDOS |
| P3 | JEMS 47(6) | los dos artículos pertinentes identificados por Crossref; réplica NO-ENCONTRADA (Dataverse, texto abierto de LSE); 3×1 de acceso cerrado → SIN-FETCH |
| P3 | Banxico «estudios cuantitativos y cualitativos sobre efectivo» | 2014, 2015, 2017, 2018, 2023 + estudio CIESAS de la nueva serie OBTENIDOS; otras ediciones NO-OBTENIDO-POR-ESTE-AGENTE(2) |
| P3 | Profeco QQP | diccionario, metadatos y años 2024–2026 OBTENIDOS (RAR v5 verificados con `tar.exe`, 25 miembros c/u); años anteriores SIN-FETCH (frontera para el sucesor) |
| §3 | ECCO | NO-OBTENIDO-POR-ESTE-AGENTE(13): NO-ENCONTRADO en el CKAN de datos.gob.mx (sfp 11 + sabg 22 paquetes, con control positivo de búsqueda) |
| P3 | Sandoval 2026; Pellegrini & Scandura 2008 | SIN-FETCH con DOI (10.1111/lamp.70057 — identidad con la cita por confirmar; 10.1177/0149206308316063). De pago; no se pirateó |
| P4 | (a)–(g), registros con identidad | §4 de esta nota |

## 7 · Conteo de payloads (manifiesto, lector YAML)

- Al abrir (`eda5bb9f`): **7 049 entradas, 7 044 con sha256**.
- Tras registrar (antes de fusionar #1255): 7 194 / 7 189. Tras fusionar `origin/main` (MAPA añadió 3 DDI) y registrar la evidencia del RNM 1058: **7 198 entradas, 7 193 con sha256**; de ellas **146 son de este acto** (`oe1_*`: 140 en `data_raw`, 6 RESERVADAS en `reserva_respondentes`).
- Verificación por id: `tests/manifiesto.py --verifica` sobre los 140 de `data_raw` → **140 COINCIDE**, 0 ausentes; las 6 reservadas (fuera del perímetro físico del verificador) comprobadas por sha256 a mano → 6 COINCIDE. Anti-PR#77: todos viven en `/home/pc0/mm-corpus/{raw,reservas-respondentes}`, no en el worktree.
- Cola: 29 filas nuevas en `data/curacion-registro/cola-adquisicion-registro.tsv` (prefijo `forense/encargos/2026-09-27-GEN2-OBTENCION-EXTERNA-1.md#`), ninguna fila ajena editada; vista regenerada (952 filas).

## 8 · Hallazgos

1. **MAPA-INSTRUMENTOS-ALTERNOS-1 lee como «vía abierta PROBABLE» el microdato de ENVE 2024** (`acceso-rnm.tsv`, por la plantilla `open_terms_*` de `get_microdata`) y su mapa propone «OBTENER(microdato ENVE 2024 por RNM 1058)». La ficha del mismo catálogo dice «Los microdatos de proyectos estadísticos en establecimientos no están abiertos al público en general […] acceso indirecto mediante el Laboratorio de microdatos/Procesamiento remoto» (página registrada: `oe1_enve_2024_rnm_1058_catalogo_html`). El mapa es ajeno y no se edita: lo corrige su sucesor `mapa-instrumentos-alternos-v1_1`.
2. **ENCRIGE 2016 y la preservación F5 R08** («la ola 2016 no se toca ni en documentación hasta la fase confirmatoria», citada por MAPA). Este acto, por encargo de §1, tocó de ENCRIGE 2016 sólo la página de acceso del RNM 264 y la lista de enlaces de la pestaña «Microdatos» (nombre del FD, no bajado); ningún cuestionario, FD ni tabulado de la ola se bajó ni se leyó. Se declara de más para que mesa juzgue si consume algo.
3. **NC de caja de OBTENCION-PREVIA-1** (§5): 14/14 payloads traídos por id y COINCIDEN; la fila `NC-260928-GEN2-OBTENCION-PREVIA-1-8e6a-02` se deja para que la cierre mesa o el trámite.
4. **Error propio atrapado por el registrador**: escribí que los dos adjuntos de dic/2024 del Mecanismo tenían sha distinto; la deduplicación por sha mostró que son idénticos. Corregido antes de escribir el manifiesto (se registran una vez).
5. **Generalización de un subagente corregida**: P1 extendió la condición de acceso del RNM 815 a «las siete ediciones»; la nota de la fila dice ahora en cuáles se leyó (815 y 1058) y en cuáles se infiere por la estructura del portal.

Módulo de auditoría: no aplica (acto de obtención; no afirma nada sobre México).
