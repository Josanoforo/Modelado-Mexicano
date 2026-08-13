# ACTO R · Registro de ISSP/ZA6980 — 2026-08-13

## §0 · Premisas

`grep -c "ZA6980" data/manifiesto.yaml data/manifiesto-staging.yaml` → `0`/`0`, como esperaba el encargo — sin registro previo. `grep -ci "gesis" data/universo-puertas-2026-08-12.tsv` → `0` antes de este acto. Entorno: caja local, sin red necesaria (los archivos ya estaban en disco).

**Terreno distinto del que el encargo suponía, declarado antes de proceder:** el encargo cita tres archivos del usuario. En `/mnt/c/Users/PC0/Descargas MX/` (raíz `descargas_mx` de `data/raices.local.yaml`) hay **cinco**: los tres declarados, más `ZA6980_backgroundvar_mx.pdf` (220,092 bytes, un documento real no mencionado — probablemente el codebook de variables de fondo/demográficas) y `ZA6980_q_mx (1).pdf` (247,978 bytes, duplicado byte-idéntico de `ZA6980_q_mx.pdf`, sufijo de navegador). Los tamaños de los tres archivos declarados coinciden con lo citado (243/5,155/3,071 KB declarados vs. 247,978/5,278,278/3,144,289 bytes reales — 242.2/5,154.6/3,070.6 KiB, redondeo consistente). Se registran únicamente los tres declarados por el encargo; `backgroundvar_mx.pdf` y el duplicado quedan sin registrar, declarados en §4.

## §1 · Identificación del módulo

Portada de `ZA6980_q_mx.pdf` (páginas 1-2, leídas de primera mano): *"Mexico / ISSP 2017 – Social Networks and Social Resources / Questionnaire"*; el propio instrumento en español confirma: *"CUESTIONARIO DEL MÓDULO DE 'REDES SOCIALES y RECURSOS SOCIALES'"*. Sin ambigüedad: **ZA6980 = ISSP 2017, módulo `social-networks/2017`** — no `social-inequality/2019` ni `family-and-changing-gender-roles/2012`. No hubo que parar por PASO 2.

## §2 · Corrección de premisa: qué necesidades cubre, contra el censo real

El encargo declara "las 5 fuentes en EN-ESPERA-DE-VIA" moviendo capa2 y da por sentado, de paso, que este módulo "cubre N12/N13/N30". Verificado contra `data/curacion-registro/relaciones.tsv` (`awk -F'\t' '$3=="ISSP"{print $2"\t"$5"\t"$13}' ...`): la fuente exacta **"ISSP Social Networks and Social Resources 2017 México"** ya está registrada como `CANDIDATA` (nunca `CONFIRMADA`) para **siete** necesidades, no tres: **N2, N3, N12, N13, N14, N28, N30**. Cruzando cada una contra su mejor fuente actual (`awk -F'\t' -v n="$n" '$2==n{...}'`):

- **N12, N13, N14 ya tienen fuente `CONFIRMADA`/`EXISTE-SATISFACE` distinta** (`ENBIARE` para N12/N14, `ENASIC` para N13) — ISSP es candidata redundante ahí, no la que cierra el hueco.
- **N2, N3, N28, N30 siguen sin ninguna fuente `CONFIRMADA`** en todo el corpus — ahí ISSP es una candidata real, entre varias sin confirmar (N2: GPS/ENCOAP también candidatas; N3: ENFIH/ENSAFI/dos estudios de microcrédito también candidatas, con dos filas `NEGATIVA`; N28: cuatro candidatas más, ninguna confirmada; N30: seis candidatas más — ENCOAP/LATINOBARÓMETRO/OECD/BIARE/LAPOP/ENBIARE —, ninguna confirmada).

Este número (7, no 3) ya estaba documentado en `forense/notas/2026-08-12-acto-p-lote1-adquisicion.md:35` y en `forense/notas/2026-08-12-acto-o-cola-adquisicion.md:122` — no es un hallazgo nuevo, es que el encargo lo simplificó de más al citarlo. Registrar el payload **no mueve `capa2_manifiesto` ni satisface ninguna necesidad** — eso exige mapeo semántico variable-por-variable, fuera del perímetro de este acto (y es justo el trabajo que ACTO V2 diagnostica como sin vía todavía).

## §3 · Registro en `data/manifiesto.yaml`

Mismo carril que produjo las 11 entradas WVS del commit `84f8e30` — leído ese commit de primera mano, no reconstruido de memoria: la forma real del carril **no es `--registra` puro** (ese comando exige `--formato`/`--licencia`, no acepta `raiz` distinta de `data_raw`, y por tanto no puede escribir `raiz: descargas_mx`). El propio commit WVS lo declara: escribió con `escribir_manifiesto()` importado directamente para evitar dos defectos reales de `--escanea`/`--promueve` (plegado que corrompe YAML en valores largos; `--grupo` que no acumula entre llamadas). Se replicó el mismo mecanismo — sha256/tamaño derivados por `tests/manifiesto.sha256_de`/`os.path.getsize` sobre el archivo real, nunca tecleados — para los tres archivos declarados:

| id | archivo | sha256 | bytes |
|---|---|---|---|
| `za6980_issp2017sn_cuestionario_mx_pdf` | `ZA6980_q_mx.pdf` | `61bc0c80…544f2ed` | 247,978 |
| `za6980_issp2017sn_datos_v2_0_0_sav_zip` | `ZA6980_v2-0-0.sav.zip` | `20a1420f…4ae97ca5` | 5,278,278 |
| `za6980_issp2017sn_datos_v2_0_0_dta_zip` | `ZA6980_v2-0-0.dta.zip` | `aa3bfcbc…65dc227de` | 3,144,289 |

`raiz: descargas_mx`, `descargado_por: usuario, vía navegador`, `fecha_descarga: '2026-08-12'`. `url_origen`: `https://www.gesis.org/en/issp/data-and-documentation/social-networks/2017` — la misma URL ya citada como la de este módulo en `forense/notas/2026-08-12-acto-p-lote1-adquisicion.md` (Commit 2, el intento del agente bloqueado por Cloudflare) y en `forense/notas/2026-08-12-acto-o-cola-adquisicion.md`; `url_origen_procedencia: confirmada` — no asignada a ciegas, corroborada por dos fuentes independientes (la cola de adquisición previa y la portada del propio PDF). `python3 tests/manifiesto.py --verifica --id <los 3>` → `COINCIDE` en los 3, `sin_configurar=0`. Único escritor: un solo proceso, una sola invocación, sin concurrencia declarada.

**Verificación de cierre (defecto PR #77):** los tres payloads viven en `/mnt/c/Users/PC0/Descargas MX/` — una ruta absoluta fuera de cualquier worktree, ya compartida por todos los worktrees vía `data/raices.local.yaml:descargas_mx` (mismo mecanismo que usan las 11 entradas WVS y ~40 entradas más bajo esa raíz). No hay "solo en mi worktree" que verificar aquí: la raíz nunca fue worktree-local. `--verifica` lo confirma leyendo directamente esa ruta.

## §4 · Fila de puerta GESIS

Añadida `GESIS_ISSP_SocialNetworks_2017_ZA6980` a `data/universo-puertas-2026-08-12.tsv` (append al final, sin reordenar — 99→100 líneas, 15/15 columnas verificado con `csv.reader`). Ya existía una fila `ISSP` (`gap_mapeo_map_b`, `NO-ENCONTRADO`, añadida por MAP-B el 2026-08-13 con exactamente las mismas 7 necesidades derivadas en §2) — es un placeholder genérico de mapeo, no una puerta institucional real; se declara redundante aquí y **no se toca**: retirarla o reconciliar el crosswalk (`data/crosswalk-fuente-puerta-2026-08-13.tsv`) es trabajo de un acto de reconciliación dedicado (mismo patrón que MAP-B ejecutó para otras 5 puertas en PR #189), fuera del perímetro de éste.

**`clasificacion_a4 = EXISTE-NO-SATISFACE`, no `EXISTE-SATISFACE`.** La lista de `UNIVERSO-MINIMO-FUENTE-v1_0.md` (ADR-69) es específica de fuentes INEGI (ficha RNM, biblioteca, DOF) y no traspasa limpiamente a GESIS/ISSP — no se fuerza aquí. Con evidencia real, no por defecto conservador: (1) el mapeo semántico variable-por-variable contra N2/N3/N28/N30 no se hizo, ninguna necesidad puede llamarse satisfecha; (2) `ZA6980_backgroundvar_mx.pdf` — un documento real, no registrado por quedar fuera de los 3 declarados — sugiere que el paquete GESIS de este módulo puede traer más piezas de las que este acto capturó; (3) los otros 2 módulos ISSP de la cola (`social-inequality/2019`, `family-and-changing-gender-roles/2012`) siguen sin obtener. `EXISTE-SATISFACE` prematuro es exactamente el defecto que la revisión de ACTO M-ADQ corrigió el 12/ago (`enasic`/`enfih`) — no se repite aquí.

## §5 · Precedente para el registro, en la nota

ACTO P·Lote-1 declaró ISSP **NO OBTENIDO POR ESTE AGENTE EN 11 INTENTOS** — bloqueo Cloudflare a nivel de dominio, anterior a que el registro gratuito fuera siquiera alcanzable (`forense/notas/2026-08-12-acto-p-lote1-adquisicion.md`). Correcto como estaba escrito: no es una falla de esa sesión, es el rendimiento que A.5 predice para un muro anti-bot que exige JavaScript real. El usuario completó el registro GESIS gratuito y la descarga manual en navegador donde el agente no pudo — mismo patrón exacto que WVS (commit `84f8e30`, mismo día). Se anota como precedente repetido, no como reproche al acto P.

## §6 · Cierre

1. Módulo identificado sin ambigüedad: **ISSP 2017 Social Networks and Social Resources (ZA6980)**, por cita literal de portada — no PARO.
2. Necesidades verificadas contra `relaciones.tsv`: **7** (N2,N3,N12,N13,N14,N28,N30), no 3 — de ésas, N12/N13/N14 ya tienen fuente `CONFIRMADA` distinta; **N2, N3, N28, N30 siguen sin fuente confirmada**, dichas por su nombre.
3. 3 archivos declarados registrados en `data/manifiesto.yaml` (sha256/tamaño derivados, `--verifica` → `COINCIDE` en los 3); 2 archivos reales no declarados (`ZA6980_backgroundvar_mx.pdf`, duplicado de cuestionario) quedan sin registrar, declarados en §0.
4. 1 fila de puerta añadida (`GESIS_ISSP_SocialNetworks_2017_ZA6980`, `EXISTE-NO-SATISFACE`, razón nombrada en §4); la fila `ISSP`/`gap_mapeo_map_b` preexistente queda redundante y sin tocar, declarada.
5. `capa2_manifiesto` sin mover — esa vía no existe (verificado, no es este acto).
6. `tests/check.py --baseline`: **LÍNEA BASE VERDE — 22 FAIL · 104 WARN**, sin cambio.
7. Receta manual pendiente para el usuario, mismos 2 módulos, mismo registro GESIS, menos de un minuto cada uno: `https://www.gesis.org/en/issp/data-and-documentation/social-inequality/2019` y `https://www.gesis.org/en/issp/data-and-documentation/family-and-changing-gender-roles/2012`.
