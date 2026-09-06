# `ACTO MAESTRA38-A4 · ADQUIERE-TODO-LO-PUBLICO` — COMMIT-1 · lista congelada de objetivos

6/sep/2026 · `origin/main` en `a5350e59` · worktree `/home/pc0/Modelado-Mexicano/.claude/worktrees/agent-a4f8a030e1f577254`, rama `acto/maestra38-a4-adquiere-todo-lo-publico` · corpus compartido `/home/pc0/mm-corpus/raw` (symlink `data/raw`) · segunda raíz `descargas_mx` = `/mnt/c/Users/PC0/Descargas MX` (169 entradas).

**Frase de sello.** Esta lista queda congelada ANTES de bajar un solo byte. Ningún objetivo se añade, se quita ni se reescribe después de este commit: lo que no esté aquí no cuenta como obtenido por este acto, y lo que esté aquí y no se obtenga se va a `PAQUETE-RECETAS-10` con su razón exacta y su receta. La firma que este acto ejecuta es, verbatim (6/sep): «Lo que pueda bajar caja que lo baje caja, lo que no, dame las ligas y el detalle de qué tengo que bajar».

---

## 0 · Universo — derivado por comando, no heredado del encargo

```
python3 - <<'EOF'
import csv,re
rows=list(csv.DictReader(open('data/curacion-registro/cola-adquisicion-registro.tsv',encoding='utf-8'),delimiter='\t'))
ok=lambda e: e in ('PENDIENTE','PENDIENTE-DE-MESA','OBTENIDO-PARCIAL') or e.startswith('NO-OBTENIDO-POR-ESTE-AGENTE')
u=[r for r in rows if ok(r['estado_A4A5'])]
con=[r for r in u if r['url_conocida'].strip() or re.search(r'https?://', r['nota'] or '')]
print(len(rows), len(u), len(con))
EOF
→ 132 filas · 25 en el estado-universo · 13 con URL en la propia fila
```

**Desviación de premisa declarada (A.8).** El encargo dice «hoy son ~31». El comando da **25** filas en el estado-universo, de las cuales **13** traen URL en la fila. Las **12** restantes traen su URL dentro de la receta que su `nota` cita (`PAQUETE-RECETAS-3`, 6 recetas; `PAQUETE-RECETAS-5`, 6 recetas) o **no traen objeto adquirible en absoluto** (4 fichas de diseño de `MAESTRA38-N10`/`N12`: `salud.adherencia.desabasto_vs_cuidadora`, `cooperacion.comite.monitoreo_sancion_visible`, `cooperacion.faena.sancion_social_pueblo_mestizo`, `CULTURA_CONSTITUCIONAL_UNAM_IIJ` — son huecos de desenlace o fuentes cuya existencia misma está sin confirmar; no hay URL que bajar y no se fabrica una). El universo real de **objetos** (no de filas) que este acto persigue es **33**, contando los archivos que cada receta enumera por separado.

**Segunda desviación de premisa declarada (A.8), medida hoy.** El encargo afirma que `enfih2019_bd_csv_zip` está «registrado, físicamente ausente». **Es falso al 6/sep/2026**: el archivo existe en el corpus compartido y su `sha256` **COINCIDE** con el del manifiesto.

```
sha256sum data/raw/enfih2019/enfih_2019_base_de_datos_csv.zip
→ be372533d5043920892142e8bf792b7293a5f20ab466a6441bc89925b42ef4d5  (idéntico a manifiesto.yaml:4115)
ls -la data/raw/enfih2019/ → enfih_2019_base_de_datos_csv.zip (4 404 049 B) + enfih_2019_fd.xlsx (202 396 B)
```

Consecuencia: la rama «hash-discordante → INEGI republicó» del encargo **no se ejecuta**; se ejecuta la rama `COINCIDE`. Ver objetivo **32**.

---

## 1 · Objetivo 1 (primero, por instrucción del encargo) — `unzip -l` del paquete ICPSR

`data/raw/academico_icpsr35024/icpsr35024_mexico_panel_study_2012_paquete_v1.zip` (14 665 813 B, `id` de manifiesto `icpsr35024_mexico_panel_study_2012_paquete_v1_zip`, `manifiesto.yaml:20988`). Sin `unzip` en esta caja; equivalente exacto con `python3 -m zipfile`/`zipfile.ZipFile.infolist()`:

```
     1252847  ICPSR_35024/35024-Questionnaire-spanish.pdf
     1253437  ICPSR_35024/35024-Questionnaire-english.pdf
     2963516  ICPSR_35024/DS0001/35024-0001-Codebook-spanish.pdf
     3928432  ICPSR_35024/DS0002/35024-0002-Codebook-english.pdf
     3474974  ICPSR_35024/DS0003/35024-0003-Codebook-spanish.pdf
     4331362  ICPSR_35024/DS0004/35024-0004-Codebook-english.pdf
        1228  ICPSR_35024/35024-related_literature.txt
        4896  ICPSR_35024/35024-manifest.txt
        6180  ICPSR_35024/35024-descriptioncitation.html
        7148  ICPSR_35024/TermsOfUse.html
     (10 entradas · testzip() → None, ningún CRC malo)
```

**Veredicto congelado: el `.dta` NO está en el paquete.** Diez entradas, cero archivos de datos — sólo documentación (2 cuestionarios, 4 codebooks, 3 textos, 1 términos de uso). La afirmación «el contenido está sin inspeccionar» del encargo queda resuelta aquí, y la rama (d) que aplica es la segunda: leer la página de términos y decir cuál de las tres razones aplica. Se ejecuta en `COMMIT-2`, objetivo **33**.

---

## 2 · Tabla congelada de objetivos

Columna «sonda» = resultado de la sonda de alcanzabilidad corrida hoy **antes de pedir contenido** (`curl -r 0-0 -L -A <navegador>`, que trae `Content-Range` con el tamaño total sin bajar el cuerpo). Es el paso (a) del encargo, y va antes que cualquier byte.

| # | objeto (nombre esperado) | fuente / fila de la cola | URL congelada | pregunta que responde | criterio de éxito | sonda 6/sep |
|---:|---|---|---|---|---|---|
| 1 | `Final_dataset_Mexico_Earthquake.dta` | `EARTHQUAKE_TRUST_LAPOP_2017` (R-confianza post-sismo) | `dataverse.harvard.edu/api/access/datafile/10123574?format=original` | ¿cambia la confianza institucional tras un choque exógeno (sismo 2017)? — instrumento con tratamiento natural que ninguna ola LAPOP genérica da | Stata 14, **674 621 B** exactos, `sha256` estable entre dos descargas | `206` · `0-0/674621` · `application/x-stata-14` |
| 2 | `Final_do_file_Mex_quake.do` | idem | `dataverse.harvard.edu/api/access/datafile/10123575` | código de réplica: confirma el mapeo variable→cifra publicada | Stata syntax, **44 712 B** | `206` · `0-0/44712` |
| 3 | `SEGUIM_ACCIONES_INFRA_FISICA_OBRA_CONS_MANT_1Y2TRIM24.xlsx` | `IMSS_BIENESTAR_ACCIONES_DE_INFRAESTRUCTURA` | `imssbienestar.gob.mx/assets/doc/transparencia/05_datosabiertos/04_uinfraestructura/…1Y2TRIM24.xlsx` | oferta física de salud por unidad, 1º-2º trim 2024 (driver territorial de acceso) | XLSX, **251 823 B** | `206` · `0-0/251823` |
| 4 | `Seguimiento de Acciones de Infraestructura 1° Trimestre 2025.xlsx` | idem | `…/Seguimiento%20de%20Acciones%20de%20Infraestructura%201%C2%B0%20Trimestre%202025.xlsx` | idem, 1er trim 2025 | XLSX, **1 278 564 B** | `206` · `0-0/1278564` |
| 5 | `seguimiento_acciones_infraestructura_1er_trimestre_2025.csv` | idem (alterno CSV) | `repodatos.atdt.gob.mx/api_update/imss-bienestar/…/seguimiento_acciones_infraestructura_1er_trimestre_2025.csv` | control: ¿el CSV del repositorio central es el mismo universo que el XLSX? | CSV, **8 795 B** (mucho menor → extracto, se declara) | `206` · `0-0/8795` |
| 6 | `redeco_datosabiertos1ertrim_2026.csv` | `EXT_OF_11_REUNE_REDECO` | `repodatos.atdt.gob.mx/api_update/condusef/registro_despachos_cobranza_contratados_entidades_financieras/redeco_datosabiertos1ertrim_2026.csv` | despachos de cobranza registrados: presión de cobro sobre el deudor, por entidad | CSV, **678 710 B** | `206` · `0-0/678710` |
| 7 | `datosabiertos_310326.csv` (REUNE) | idem | `repodatos.atdt.gob.mx/api_update/condusef/unidades_especializadas/datosabiertos_310326.csv` | quejas ante UNE por institución: desenlace del conflicto usuario-banco | CSV, **4 482 648 B** | `206` · `0-0/4482648` |
| 8 | `envipe2025_rnm_ddi.xml` | `ENVIPE_EXTRACCION_TEXTO_REACTIVO` | `www.inegi.org.mx/rnm/index.php/metadata/export/1130/ddi` | texto **literal** de cada reactivo ENVIPE 2025 (`<qstnLit>`) — cierra el hueco 0%-texto-de-reactivo (FP-190/CIV-08) | XML DDI, **2 334 820 B**, con nodos `qstnLit` no vacíos | `206` · `0-2334819/2334820` |
| 9 | `ensu2025_rnm_ddi.xml` | idem (hermana ENSU) | `www.inegi.org.mx/rnm/index.php/metadata/export/1100/ddi` | idem para ENSU 2025 | XML DDI, **2 628 278 B** | `206` · `0-2628277/2628278` |
| 10 | `JEA_Elecciones_concurrentes.pdf` | `TEPJF_ELECCIONES_CONCURRENTES_1991_2018` | `www.te.gob.mx/editorial_service/media/pdf/JEA_Elecciones_concurrentes.pdf` | serie de concurrencia electoral 1991-2018 (contexto de participación) | PDF, **1 441 115 B** | `200` · `1441115` |
| 11 | `Concentrado_Ayuntamientos_2016.pdf` | `IETAM_TAMAULIPAS_SERIE_MUNICIPAL` | `ietam.org.mx/PortalN/documentos/PE2015/Resultados/Concentrado_Ayuntamientos_2016.pdf` | VOTOS por municipio Tamaulipas 2016 (pata 1/4 de la cohorte g2018) | PDF, **556 374 B** | `206` · `0-0/556374` |
| 12 | `Abasolo.xlsx` … ×43 municipios | idem | `ietam.org.mx/PortalN/documentos/Municipios_2017-2018/<Municipio>.xlsx` | VOTOS por municipio 2018 (pata 2/4) — la receta sólo verificó `Abasolo`; los otros 42 son **derivación**, no dato verificado | XLSX por municipio; `Abasolo.xlsx` = **58 881 B** | `206` · `0-0/58881` (sólo Abasolo) |
| 13 | `Ayuntamiento.xlsx` | idem | `ietam.org.mx/PortalN/documentos/PE2020/Computos_electorales/Ayuntamiento.xlsx` | VOTOS 2021, 43 municipios consolidados (pata 3/4) | XLSX, **77 251 B** | `206` · `0-0/77251` |
| 14 | `CONCENTRADO_DE_COMPUTOS_MUNICIPALES.xlsx` | idem | `ietam.org.mx/PortalN/documentos/PE2023/Computos_Finales/CONCENTRADO_DE_COMPUTOS_MUNICIPALES.xlsx` | VOTOS 2024 (pata 4/4) | XLSX, **171 703 B** | `206` · `0-0/171703` |
| 15 | `MILK-RCT--Study-of-Life-MI-Purchasing-Decisions-in-Mexico.pdf` | `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | `media.milliman.com/…/MILK-RCT--Study-of-Life-MI-Purchasing-Decisions-in-Mexico.pdf` | elasticidad-precio y framing en microseguro de vida (hermana del objeto SSRN bloqueado). **No cierra R1.4** (sin comparador de marca) — evidencia complementaria, declarado | PDF, **1 111 333 B** | `206` · `0-0/1111333` |
| 16 | `ESTADISTICA_CONCEJALES_2016_IEEPCO.xlsx` | `IEEPCO_OAXACA_SERIE_MUNICIPAL` | `www.ieepco.org.mx/archivos/elecciones-2016/ESTAD%C3%8DSTICA%20CONCEJALES%20%202016.xlsx` | resultados municipales Oaxaca 2016, 25 hojas D01..D25 (cobertura futura; R7.1 ya archivada A) | XLSX, **968 301 B** | **`000`** · `SSL certificate: unable to get local issuer certificate` → cadena TLS incompleta, no ausencia |
| 17 | `cngf_2025_m1s1.pdf` | `INEGI_CNGF` | `www.inegi.org.mx/contenidos/programas/cngf/2025/doc/cngf_2025_m1s1.pdf` | oferta institucional de trámites federales (contexto; 0 necesidades vivas lo citan hoy) | PDF, **2 014 714 B** (el soft-404 de INEGI es 200/2263 B — el tamaño es el discriminador) | `206` · `0-0/2014714` |
| 18 | `ec_cngf2025.xlsx` | idem | `…/doc/ec_cngf2025.xlsx` | marco conceptual CNGF 2025 | XLSX, **195 845 B** | `206` · `0-0/195845` |
| 19 | `cngf_2025_resultados.pdf` | idem | `…/doc/cngf_2025_resultados.pdf` | resultados CNGF 2025 | PDF, **1 075 400 B** | `206` · `0-0/1075400` |
| 20 | `compranet_historico.csv` | `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` | `www.datos.gob.mx/dataset/contratos_expedientes_sistema_historico_compranet` (página; recurso CSV dentro) | ventana temporal larga de contrato/procedimiento/proveedor. **No añade persona+sanción** — el hueco decisivo sólo lo cierra PDN S1/S2 | CSV, ~**951 619 345 B** (~951 MB) | `206` · `0-0/26314` · **`text/html`** → la URL congelada es la página, no el recurso; resolver en COMMIT-2 |
| 21 | `11_datos_abiertos_declaranet_2018.csv` | `PDN_SESNA_S1_S2_S3_S6` (nota lateral) | `repodatos.atdt.gob.mx/api_update/…/listado_declaraciones_situacion_patrimonial/11_datos_abiertos_declaranet_2018.csv` | declaraciones patrimoniales Ejecutivo Federal 2013-2018. **No sustituye PDN-S1** (subnacional 2019+) ni toca S2/S3/S6 | CSV, **45 284 941 B** | **`503`** · 592 B `text/html` |
| 22 | microdato WB Enterprise Surveys México 2023 | `ENAFIN` (hermana) | `microdata.worldbank.org/index.php/catalog/6453` | ¿motivo de rechazo de crédito = «sin historial crediticio»? (N19). Cobertura **incierta**, sin confirmar | archivo de microdato tras registro | `200` · página viva, descarga tras registro |
| 23 | `35024-0001-Data.dta` (ICPSR 35024) | `ICPSR35024` / fila 19 | `www.icpsr.umich.edu/web/ICPSR/studies/35024` | microdato Mexico Panel Study 2012 (1 555 casos × 374 vars) — hoy sólo hay tabulados derivados de 2ª mano | `.dta`, MD5 `3f717dfcd8f3ba136c5d5ac0f571990c` (del propio `35024-manifest.txt`) | **`403`** al host desde esta caja |
| 24 | 25 encuestas «Los mexicanos vistos por sí mismos» | `LOS_MEXICANOS_VISTOS_POR_SI_MISMOS_UNAM_IIJ_2015` | `losmexicanos.unam.mx/` | autopercepción; ≥24 de las 25 nunca evaluadas para Ola 6 | portal alcanzable + al menos un archivo de datos | **`000`** · `Recv failure: Connection reset by peer` (**desde UBUNTU con red real**, no desde nube) |
| 25 | microdato / documentación ECOPRED 2014 | `ECOPRED_2014_INEGI` | `www.inegi.org.mx/programas/ecopred/2014/` | cohesión social y prevención de violencia (¿existe siquiera el microdato?) | confirmar existencia del programa y, si existe, bajar BD+FD | `206` · `0-0/4016` · `text/html` → **shell SPA**, no dato (patrón `idBiinegi`) |
| 26 | lista nominal SICEE | `SICEE` | `sicee.ine.mx/` | denominador de participación por municipio | archivo por municipio/año | `206` · `0-0/6205` · `text/html` (SPA) — la fila ya trae veredicto `NO-BAJAR-PORQUE` |
| 27 | PDN S1/S2/S6 (bulk) | `PDN_SESNA_S1_S2_S3_S6` | `www.plataformadigitalnacional.org/` | persona-con-id + sanción (el hueco decisivo de contratación pública) | descarga masiva por sistema | `206` · `0-0/586` · `text/html` (SPA) |
| 28 | PDF Bauchet SSRN 2474620 | `PRICE_AND_INFORMATION_TYPE…` (objeto exacto) | `cenfri.org/research-paper/price-and-information-type-in-life-microinsurance-demand-experimental-evidence-from-mexico/` | el paper exacto de la fila (no la hermana) | PDF del paper | `200` página; el PDF vive en `papers.ssrn.com` (Cloudflare) |
| 29 | bases de datos ENJUVE 2000/2005/2010 | `ENJUVE` | `www.gob.mx/imjuve/documentos/base-de-datos-de-la-encuesta-nacional-de-juventud-2010` | microdato de juventud; hoy sólo hay 1 cuestionario PDF de 3 | `.sav`/`.dta` por edición | `206` · `0-0/480` · `text/html` (los dos hosts históricos ya dieron 5xx en A1) |
| 30 | microdato individual Reuters DNR | `REUTERS_DNR` | (on request) — topline ya obtenido vía `datawrapper.dwcdn.net/uLZ8T/12/dataset.csv` | confianza en medios a nivel persona | archivo por respondente | `206` · `0-0/1850` (el **topline**, ya en corpus; el microdato sigue *on request*) |
| 31 | encuesta «Cultura Constitucional» UNAM-IIJ | `CULTURA_CONSTITUCIONAL_UNAM_IIJ` | sin URL — existencia del portal **no confirmada** | legitimidad del orden legal | confirmar existencia antes que nada | `juridicas.unam.mx` `200` (host padre vivo) |
| 32 | `enfih_2019_base_de_datos_csv.zip` | `ENFIH 2019` (`enfih2019_bd_csv_zip`) | `www.inegi.org.mx/contenidos/programas/enfih/2019/microdatos/enfih_2019_base_de_datos_csv.zip` | **verificación**, no adquisición: ¿el payload registrado sigue en el corpus y con el sha del manifiesto? | `sha256` == `be372533…2ef4d5` | **ya presente**, `COINCIDE` (ver §0) |
| 33 | `TermsOfUse.html` del paquete ICPSR | `ICPSR35024` | dentro del zip ya en corpus | ¿cuál de las tres razones bloquea el `.dta`? | razón nombrada, **sin suponer** | leído (ver §1 y COMMIT-2) |

**Cuatro fichas sin objeto** (declaradas, no numeradas arriba porque no hay nada que bajar): `salud.adherencia.desabasto_vs_cuidadora`, `cooperacion.comite.monitoreo_sancion_visible`, `cooperacion.faena.sancion_social_pueblo_mestizo` — las tres son **huecos de desenlace** (`MAESTRA38-N10`: el driver está medido, el desenlace individual no existe administrativamente); y `CULTURA_CONSTITUCIONAL_UNAM_IIJ` (#31), cuya existencia misma está sin confirmar. Ninguna receta puede escribirse para un objeto que nadie ha visto: eso se dice, no se inventa.

---

## 3 · Protocolo de agotamiento (`/adquiere` v2.2, ≥4 **rutas distintas**) — congelado aquí

Refuerzo del operador, verbatim (6/sep): «Necesito que pruebes e intentes la descarga por todos los medios habidos y por haber, con todos los trucos que existan. Otras sesiones lo lograron al no quedarse con 1 intento y no lograrlo.»

Cuatro intentos idénticos con la misma herramienta **no** son cuatro rutas. Antes de escribir `NO-OBTENIDO-POR-ESTE-AGENTE` sobre cualquier objetivo, este acto agota y documenta con salida cruda:

1. **Transportes distintos** — `curl`, `wget`, `python3 urllib`, `python3 requests` si existe. Cada uno resuelve TLS, cookies y redirecciones distinto.
2. **Encabezados de navegador real** — `User-Agent` Chrome actual, `Referer` a la página del portal (no vacío), `Accept-Language: es-MX`, `Accept` de navegador. INEGI, CompraNet y varios portales `.gob.mx` rechazan el `User-Agent` de `curl`.
3. **Sesión completa antes que API** — para SPA (INEGI): `GET` a la página HTML para tomar cookies, leer `pestanaData.js` / el `idBiinegi`, y sólo entonces pegarle a `descargamasiva` reenviando cookies y `Referer`. Un `403`/`404` a la API **sin** haber pasado por la página no prueba `EXIGE-SESION-NAVEGADOR`.
4. **Espejos y rutas alternas** — otro subdominio/CDN del mismo organismo; `web.archive.org/web/2*/<url>`; buscar el nombre exacto del archivo en el buscador del portal; el vintage anterior si el del año exacto movió.
5. **Reintentos con espera real** — `HOST-NO-RESPONDE` sólo tras ≥3 intentos **espaciados**, no tres en el mismo segundo.
6. **Leer la página real** antes de decir `EXIGE-CUENTA`/`EXIGE-SOLICITUD-ESCRITA` — no inferirlo del nombre del organismo.
7. **ICPSR** — confirmar `public-use` vs `restricted-use` sobre el **dataset citado**, no sobre el estudio genérico.

Este protocolo aplica a los 33 objetivos; `PAQUETE-RECETAS-10` sólo admite lo que lo agotó.

---

## 4 · Contador congelado

- Objetivos con bytes reales confirmados por sonda **antes** de bajar: **19** (#1-#15, #17-#19) — de 33.
- Objetivos con obstáculo ya visible en la sonda: **14** (#16 TLS · #20 URL de página · #21 `503` · #22 registro · #23 `403` · #24 `000` · #25-#27 SPA · #28 Cloudflare · #29-#31 sin objeto público · #32 ya presente · #33 no aplica).
- Medición de modelo en este acto: **cero**. Es adquisición.
