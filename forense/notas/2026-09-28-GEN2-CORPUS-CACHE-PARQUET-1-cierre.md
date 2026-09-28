# ACTO GEN2-CORPUS-CACHE-PARQUET-1 · caché Parquet del corpus, cargador único y medida de memoria · nota de cierre

28/sep/2026 · CAJA (Ubuntu/WSL2, 24 GB + 16 GB swap, 24 CPU) · MODO ABIERTO (cláusula v1.0) · rama `acto/gen2-corpus-cache-parquet-1` · 0-bis `01aac006` · ADR `ADR-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-01`.
Encargo archivado: `forense/encargos/2026-09-28-GEN2-CORPUS-CACHE-PARQUET-1.md` (SHA de redacción `16ba3d02`, sello de cuerpo `ab988056…`).

**Contadores movidos: cero.** No mide, no adopta, no toca sellos ni medidores sellados, no convierte olas reservadas, no cambia el tope de sesiones (eso es de mesa, §4).

## 0 · Arranque y premisas

```
ENTORNO-DERIVADO = CAJA
senal-corpus: montado=SI archivos_examinados=515
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable
red: PERMITIDA (http_code=200, http_connect=200, x_deny_reason=ausente, via_proxy=SI)
head-vs-origin/main: detras=0 adelante=0
```
Base `16ba3d02` = `origin/main` al arrancar (0 commits detrás). Duplicado (0.c): rama remota, worktree y PR abiertos con `CACHE|PARQUET` → 0 / 0 / 0. `data/raw` enlazado a `/home/pc0/mm-corpus/raw` y `data/raices.local.yaml` copiado del clon padre. Al cierre se fusionó `origin/main` (+37 commits, sin conflictos); P1 re-derivado tras la fusión sale idéntico.

| premisa (rótulo del encargo) | verificación | qué hice |
|---|---|---|
| `demanda-corridas.tsv` (105 corridas) [§1] | EJECUTADO: 87 filas de datos (lector TSV) | logística: el universo se deriva de las tres fuentes que el encargo nombra, no del conteo |
| sin «parquet»/«cache» en el árbol [EJECUTADO] | se sostiene (0) | — |
| `tools/manifiesto.py` (sha por id) [EXISTE] | falsa en la ruta: vive en `tests/manifiesto.py` | se reusa desde ahí (`resolver_raiz_declarada`, `resolver_raiz`) |
| pyarrow instalable en caja [SUPUESTO] | no estaba; `pip` sólo con `--user --break-system-packages` (PEP 668, python3.14 del sistema) | instalados `pyarrow 25.0.1` y `zipfile-deflate64 0.2.0` en el site de usuario (CCPV 2010 y ENNViH usan deflate64). Receta: `pip install --user --break-system-packages pyarrow zipfile-deflate64` |
| filtro de reserva = campo del manifiesto + hoja «reserva sin decidir» | incompleto: ENVIPE 2026 (`envipe2026_csv`) y ENIGH 2024 (`enigh2024_nc_csv`), reservadas por el régimen vigente (`canon/MEMORIA-OPERATIVA.md` §1; E.6, firma #964), **no** llevan `estado_reserva`, y sellados las citan | unión conservadora (§1). Excluir de más no abre nada; convertir de menos sí lo haría |
| payloads que miden: zips CSV/DBF de 50–250 MB | además DTA (CCPV 2010 muestra censal: 32 zips DTA en deflate64, citados por un CALC sellado) | entran por la regla de P1 |
| preflight compara el payload, no la caché | la caché vive fuera del manifiesto y fuera de `data/raw`; ningún sellado la lee | — |

## 1 · P1 · qué entra (`data/cache/universo-p1.tsv`, DERIVADO)

Comando: `python3 tools/corpus_loader.py universo` (fuera del sandbox: 28 payloads viven en `descargas_mx`, `/mnt/c`).
Universo = ids que citan (a) `inputs` con `origen: manifiesto` de los 371 `data/corrida0/*/spec.yaml` (sellados o no; los de familias 2027 aparte), (b) `payload_ids` de `demanda-corridas.tsv`, (c) ids del manifiesto citados literalmente en `forense/analisis/familias-2027/`.

```
53	NO-SE-CONVIERTE FORMATO-NO-TABULAR
10	NO-SE-CONVIERTE RESERVADA
72	NO-SE-CONVIERTE YA-PEQUEÑO
144	SE-CONVIERTE
UNIVERSO · 279 ids -> data/cache/universo-p1.tsv
```

- **RESERVADA** (se decide antes de abrir el zip; ni su directorio central): unión de `estado_reserva: RESERVADA*` del manifiesto (0 en el universo), la hoja `forense/analisis/mapa-instrumentos-alternos/hoja-para-mesa-mapa-instrumentos-alternos.md:22-31` (ENCRIGE 2020, ENVE 2024, CSES Módulo 5, ENDUTIH 2025, ENIF 2024 por su módulo 7) y el régimen de MEMORIA-OPERATIVA §1 (ENVIPE 2026, ENIGH 2024, ENCO). Diez ids: `conjunto_de_datos_encrige_2020_csv`, `encrige2020_cuestionario`, `gen2_encrige2020_diseno_muestral`, `endutih_2025_endutih2025_bd_dbf`, `endutih_2025_fd_endutih2025`, `enif2024_csv`, `enif2024_fd_xlsx`, `enif_2024_enif_2024_bd_csv`, `enigh2024_nc_csv`, `envipe2026_csv`. Constante `RESERVA_FUERA_DEL_MANIFIESTO` en el tool.
- **FORMATO-NO-TABULAR**: sin miembro `.csv/.dbf/.dta/.sav` (PDF, XLSX de FD, JSON, HTML, XML).
- **YA-PEQUEÑO**: < 100 MB tabulares descomprimidos. Con el patrón de carga medido en P4 (≈10× el tamaño del miembro en RSS), eso es ≲ 1 GB por CALC: no es lo que satura la caja.
- **SE-CONVIERTE**: 144 ids · 4.49 GB en zip · 60.48 GB tabulares descomprimidos.

## 2 · P2 · conversión y constancia

Comando: `python3 tools/corpus_loader.py convierte --todos` (fuera del sandbox). 30 min 08 s de pared, pico 2.85 GB. Un DTA (ENCODAT 2016-17 individual) falló por codificación y se reconvirtió tras el arreglo (reintento en latin-1, biyectiva sobre bytes; queda `mm.encoding = latin1-forzado`).

Por miembro: extracción en streaming del zip, **dos sha256 del miembro** en dos lecturas independientes (A.7; en microdato tabular no hay tokens volátiles que neutralizar, así que las dos huellas son la cruda leída dos veces), tipos **declarados, nunca inferidos** — diccionario de datos del propio zip (CSV de datos abiertos INEGI), descriptor de campo (DBF: `N/F` → numérico), metadato del archivo (DTA/SAV) — y Parquet zstd por tabla en `<raíz de caché>/<id>/<tabla>.parquet`. Una columna sin tipo declarado, o declarada numérica cuyo soporte no cabe sin pérdida (`NA`, `b`, `1\r`…), queda **TEXTO crudo** y se cuenta (rama prevista del encargo §5). La caché física vive junto al corpus (`/home/pc0/mm-corpus/cache`, 2.74 GB, compartida entre worktrees; nunca en git: `data/cache/.gitignore`); en el árbol quedan sólo `constancias.tsv`, `verificacion.tsv` y `universo-p1.tsv`.

Igualdad verificable, por miembro, con salida cruda en `data/cache/verificacion.tsv`: filas, columnas y nombres; y por columna, huella del texto (bytes + longitudes) o, en numéricas, suma entera exacta y no-nulos (enteros) o huella de los float64 y de la máscara de nulos, calculadas del original y del Parquet releído. La constancia sólo se escribe si todo casa.

```
$ python3 tools/corpus_loader.py verifica
VERIFICA · 1324 constancias examinadas · 0 discordantes
verificacion.tsv: 1324 filas · IGUAL 1324 · sha256_origen_1 == sha256_origen_2: 1324
columnas 85 921 · con valor igual 85 921 · numéricas 25 928 · texto por tipo no declarado 40 034 · texto por soporte no numérico 4 503
filas 180 925 429 · constancias 1324 · ids 144
```

Reproducibilidad: reconvertidos con el código final 5 payloads en otra raíz (CCPV DTA, ENNViH DTA ×137 miembros, ENCIG 2023 CSV, ENVIPE 2020 CSV latin-1, ENVIPE 2016 DBF): **155/155 sha256 de Parquet idénticos** a sus constancias.

Tipos por miembro: DTA 523 (tipos del archivo) · DBF 224 (descriptor) · CSV con diccionario legible 134 · CSV **sin** diccionario en el zip 443 → todo texto (ENCIG 2023/2025, ENOE, ENDIREH, EIC, ENADID…; su FD es PDF). 96 miembros tienen columnas declaradas numéricas con soporte no numérico.

Defectos que la verificación atrapó en esta sesión (y por eso la verificación existe):
1. La huella de texto dependía del corte en lotes (hasheaba longitudes y bytes intercalados por lote): 3 miembros de ENVIPE 2020 salieron DISCORDANTE en la prueba y no se registraron; corregido a dos flujos de hash concatenados; lo mismo para floats (una `fsum` por lote no es invariante al corte).
2. El nombre de tabla era sólo el tallo del archivo: en `edr2015_2019_bd_dbf_zip` (cinco carpetas por año con los mismos `CAPGPO.dbf`…) y `enut2019_bd_csv` los Parquet se pisaron. `verifica` dio 28 discordantes; la tabla lleva ahora la carpeta inmediata (salvo `conjunto_de_datos/`), `convierte` se niega si dos miembros colisionan, los 18 ids cuyo nombre cambió se reconvirtieron y `verifica` volvió a 0.

Hechos del dato que la caché conserva a propósito (no los corrige): ENVIPE 2020 trae valores entrecomillados con `\r` final (`"1\r"`) y fin de línea `\r` solo; ENCIG 2023 escribe el blanco como `NA`; `gastoshogar` de `enigh2016_nc_csv`/`enigh2018_nc_csv` está truncado a **1 048 575 filas** (la constancia lo muestra; la versión por tabla `cc1_inegi_enigh_{2016,2018}__…gastoshogar_csv` está completa y también está en la caché).

## 3 · P3 · cargador único (`tools/corpus_loader.py`)

`cargar(id, tabla, columnas=[...], como="pandas"|"arrow")`: localiza `<raíz>/<id>/<tabla>.parquet`, **verifica su sha256 contra `constancias.tsv` antes de leer** (discordancia → `ValueError CACHE-DISCORDANTE`), lee con proyección y devuelve texto como `string[pyarrow]` y enteros como `Int64`; `df.attrs["fuente"]` = `PARQUET:<id>/<tabla>.parquet:<sha>`. Sin caché con constancia en esta máquina: lee el miembro original del payload como **texto crudo**, avisa por stderr y `attrs["fuente"] = ORIGINAL-TEXTO-CRUDO:…`. Nunca escribe. Raíz de caché: `MM_CACHE_RAIZ`, o `cache:` en `data/raices.local.yaml`, o junto al `data/raw` real. `tabla_de(miembro)` da el nombre (p. ej. `encig2023_04_sec_7`, `conjunto_de_datos_TSDem_ENVIPE_2020`, `defunciones_base_datos_2015__CAPGPO`).

Los medidores sellados no se tocaron (E.3): `git diff --stat origin/main -- data/corrida0/` → vacío.

Test: `tests/test_corpus_loader.py` (huérfano censado en `forense/analisis/ci-guardias/censo-tests.tsv`): 6 sintéticos (diccionario, tipos declarados, `NA` → texto, ceros a la izquierda intactos, DBF, proyección, Parquet adulterado → error, mutación de la huella → DISCORDANTE sin constancia), 1 de colisión de nombres, y 2 reales que comparan filas/columnas/nombres de cada Parquet de `enasem2021_bd_csv_zip` y `enut2019_bd_csv` contra `pandas.read_csv(dtype=str)` del original. En CAJA: `9 passed`. En CI se salta (sin pyarrow; §NO-CORRIDO).

## 4 · P4 · medida y pregunta a mesa

CALC representativo: `CALC-PISOS-ENCIG2023-EJES-0002` (ENCIG 2023, pisos por eje). Su carga es `_csv(path, suffix, cols)`: lee el miembro entero, lo decodifica y hace `pd.read_csv(dtype=str)` de todas las columnas antes de proyectar. La medida importa **esa función del medidor sellado, sin modificarlo** (sha256 `29be74a2…`, igual al de su `sello.json`), y la compara con `cargar()` con proyección. S1 = exactamente lo que carga `medir()` (sec_7 × 6 columnas + residentes × 4). S2 = el mismo patrón sobre el miembro más grande del payload (sec_8, 1 207 946 filas, 2 columnas). Un proceso por medida, tres repeticiones (el bootstrap de este CALC es réplicas × celdas, del orden de 10⁴ × 10¹: la carga fija el pico).

```
$ /usr/bin/time -f "%e s wall · %M KB maxRSS" python3 tools/corpus_loader.py mide-carga --modo {csv|parquet} --escenario {S1|S2}
S1 csv     [123186, 122588] 1.170 s 512.6 MB   1.31 s wall · 524904 KB maxRSS
S1 csv     [123186, 122588] 1.149 s 512.6 MB   1.27 s wall · 524896 KB maxRSS
S1 csv     [123186, 122588] 1.176 s 512.2 MB   1.29 s wall · 524532 KB maxRSS
S1 parquet [123186, 122588] 0.205 s 231.5 MB   0.30 s wall · 241000 KB maxRSS
S1 parquet [123186, 122588] 0.204 s 229.9 MB   0.29 s wall · 238956 KB maxRSS
S1 parquet [123186, 122588] 0.195 s 225.5 MB   0.28 s wall · 234592 KB maxRSS
S2 csv     [1207946]        3.358 s 2243.9 MB  3.49 s wall · 2297800 KB maxRSS
S2 csv     [1207946]        2.845 s 2243.8 MB  2.97 s wall · 2297688 KB maxRSS
S2 csv     [1207946]        2.916 s 2243.8 MB  3.04 s wall · 2297688 KB maxRSS
S2 parquet [1207946]        0.209 s 284.7 MB   0.29 s wall · 294856 KB maxRSS
S2 parquet [1207946]        0.202 s 288.7 MB   0.29 s wall · 299540 KB maxRSS
S2 parquet [1207946]        0.198 s 288.8 MB   0.29 s wall · 299052 KB maxRSS
base (import pandas+numpy+pyarrow): 112.7 MB
```

Contexto medido en la misma caja: `free -m` total 24 029 MB; 8 procesos `claude` sumando 2 663 MB (máximo 417 MB); durante la medida otra sesión tenía un `python3` de 3.0 GB (el pico es por proceso: no altera los RSS de arriba; los tiempos sí pueden variar). El pico del propio conversor fue 2.85 GB.

**Cálculo.** Presupuesto = 24 GB − 4 GB de reserva (kernel, caché de páginas mínima, sesiones no pesadas) = **20 GB**. Sesión pesada = proceso de Claude (0.42 GB, máximo medido) + CALC.
- Patrón CSV, medido (S2, un miembro grande): 2.30 + 0.42 = 2.72 GB → ⌊20 / 2.72⌋ = **7**.
- Patrón CSV, un CALC que cargue dos miembros grandes (p. ej. ENCIG 2025 sec_6 + sec_8, 226 y 231 MB): **estimado, no medido** = 2 × 2.30 + 0.42 = 5.02 GB → ⌊20 / 5.02⌋ = **3**.
- Con el cargador (S2 Parquet): 0.30 + 0.42 = 0.72 GB → ⌊20 / 0.72⌋ = 27; ahí manda la CPU (24), no la memoria.

**Pregunta a mesa** (fila `FP-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-01`; el tope lo declara mesa, no este acto — PARO c):
- **(a) Recomendada: tope de 3 sesiones pesadas de caja con el patrón CSV (el de todo medidor sellado y de todo lote que aún no adopte el cargador), y hasta 6 en total cuando las sesiones adicionales declaren en su spec `tools/corpus_loader.cargar`.** Razón: 3 aguanta el peor caso estimado de CSV; cada sesión con cargador cuesta ~0.7 GB, y 3×5.0 + 3×0.7 = 17.1 GB < 20 GB.
- (b) 4 sesiones sin distinguir patrón: cabe con el patrón medido (4 × 2.72 = 10.9 GB), pero no con el estimado de dos miembros grandes (4 × 5.02 = 20.1 GB); el swap de 16 GB lo absorbería lento.
- (c) Mantener 2 hasta que un lote selle un CALC que use el cargador.

## 5 · «Hecho», por comando sobre el commit final con `origin/main` fusionado

| criterio | comando | salida |
|---|---|---|
| constancia por miembro convertido; sha256 reproducible | `python3 tools/corpus_loader.py verifica` | `1324 constancias examinadas · 0 discordantes` |
| 0 olas reservadas en la caché | cruce ids de `constancias.tsv` y directorios de la raíz contra `estado_reserva` del manifiesto y contra `motivo_reserva` | 144 ids / 144 directorios · RESERVADA por manifiesto 0 · por la unión 0 |
| test huérfano filas/columnas Parquet vs CSV en dos payloads pequeños | `python3 -m pytest -q tests/test_corpus_loader.py` | `9 passed` |
| P4 con cifras | §4 | — |
| ningún sello ni medidor cambió | `git diff --stat origin/main -- data/corrida0/` | vacío |
| suite | `python3 tests/check.py --baseline` | ver §6 |

## 6 · Suite

Ver el cuerpo del PR: salida cruda de `tests/check.py --baseline` sobre el commit final.
