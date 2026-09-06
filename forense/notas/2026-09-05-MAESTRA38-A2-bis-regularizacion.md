# COMMIT-2 · `MAESTRA38-A2-bis` — promoción, exclusiones y cierre de residuo

**Universo y comando.** `python3 tests/manifiesto.py --promueve --descargado-por MAESTRA38-A2-bis` sobre `data/manifiesto-staging.yaml` (35 entradas: 34 `data_raw` + 1 `descargas_mx`).

## A · Promoción (--promueve)

**34 promovidas** a `data/manifiesto.yaml` (grupo 1: `ennvih/doc/*.pdf` ×24 · grupo 2: `enaproce2018/*.zip` ×4 + `DescargaMasivaOD_582026_171540_NACIONAL_7930url.xml` ×1 · grupo 3: `ADQ15_ENAFIN_2024_RNM_INEGI/*.html.2a` ×3 + `ADQ15_JPAL_.../jpal_evaluacion_landing.html.2a` ×1 + `ADQ15_VotarEntreBalas_DataCivica/votar_entre_balas_base.zip.2a` ×1). Todas con `url_origen: "no determinada"` / `url_origen_procedencia: "no derivada -- --escanea no encontró sugerencia, NO confirmada por el autor"` / `usado_para: "sin uso asignado — registro de inventario"` (comportamiento por diseño de `--promueve`, no un dato inventado). **1 no promovida**: `descargas.php` (página guardada, `EXTENSIONES_PAGINA`, nunca se promueve por diseño) — retirada a mano de `data/manifiesto-staging.yaml` (ver `## CONSUMIDO`/hallazgo de staging), dejándolo vacío.

**No hay nada "de mesa"** que promover además de las 34: el staging no traía ninguna otra entrada.

**`--verifica` (una invocación, 34 `--id`)**: `python3 tests/manifiesto.py --verifica --id <34 ids>` → **34/34 COINCIDE** (sha256 y tamaño verificados contra `data/manifiesto.yaml`, entorno `Linux 6.18.33.2-microsoft-standard-WSL2 · Python 3.14.4`).

**Cola por writer**: de las fuentes cuyo nombre coincide con los grupos promovidos (`grep -in "ennvih\|enaproce\|enafin\|jpal\|votarentrebalas"` sobre `data/curacion-registro/cola-adquisicion-registro.tsv`), sólo `ENAFIN` (fila 50, `PENDIENTE-DE-MESA`) tiene relación directa — anotada con lo que se promovió (3 páginas de catálogo, no el microdato de empresa que `N19` pide), **estado sin cambio** (sigue `PENDIENTE-DE-MESA`, correcto: no hay microdato nuevo). `VOTAR_ENTRE_BALAS` y `EXPERIMENTO_INFORMACION_ELECTORAL_2009` ya estaban `OBTENIDO` — sin cambio, coherente con lo promovido (registro adicional del mismo objeto).

## B · Exclusiones en `tests/corpus.py` (patrón B, §3 de la spec)

`tests/corpus.py::c1_huerfanos()` gana la clasificación **`patron_b`**: un huérfano `sin_registro` cuyo `sha256` ya duplica contenido de la MISMA raíz (condición 1 de la spec) se reclasifica a `patron_b` — excluido del conteo de candidatas nuevas, jamás borrado ni ocultado del reporte — sólo si además (condición 2) su nombre trae el sufijo de copia de navegador ` (N)` antes de la extensión, o es una página guardada (`M.EXTENSIONES_PAGINA`). Implementado en `_es_patron_b()`, invocado desde `c1_huerfanos()`.

**Ejemplos reales, verificados contra el árbol:**
- `descargas.php` — página guardada; NO cae en patrón B porque su sha256 **no** duplica nada (es contenido genuinamente nuevo) — sigue `sin_registro`, categoría A real, consistente con `--escanea`.
- `icpsr35024-ds1-w2-crosstabs-derivadas (1).csv`/`(2)`/`(3)` — sha256 duplica `icpsr35024_ds1_w2_crosstabs_derivadas` (misma raíz `descargas_mx`) Y nombre trae sufijo `(N)` → **patrón B**, excluido.
- `adolescentes_ensanut2024_w.Cuestionarios.pdf` — sha256 duplica `3_vfinal_cuestionario_adolescentes_ensanut_2024_etiquetas_cuestionarios` (misma raíz) pero el nombre **no** trae sufijo de copia → sigue `sin_registro`, categoría **D** (dedup por contenido sin patrón de nombre), tal como la spec §3 exige explícitamente ("un archivo que cumple (1) pero no (2)... pertenece a la categoría D, no a B").
- `ADQ15_OMCA_conflictos_agua/omca_consulta.html.2a` (`data_raw`) — mismo caso D, sin cambio (ya documentado por la ENMIENDA 2 previa del propio archivo).

**Total `patron_b` de esta corrida: 19** (todos en `descargas_mx`), de los 33 `sin_registro` originales de esa raíz.

## Re-corrida `tests/corpus.py` antes/después, por raíz

| raíz | C1 antes (4/sep, censo) | C1 después (5/sep, este acto) | detalle del cambio |
|---|---|---|---|
| `data_raw` sin_registro | 37 | **3** | 34 promovidas (A→registrado), 3 sin cambio (categoría D, ya documentada) |
| `data_raw` presente_bajo_otra_raiz | 0 | 0 | sin cambio |
| `descargas_mx` sin_registro | 33 | **14** | 19 reclasificados a `patron_b` (excluidos del conteo), 14 quedan (13 categoría D + 1 página `descargas.php`) |
| `descargas_mx` presente_bajo_otra_raiz | 73 | 73 | sin cambio — `FP-308` firmada (iii), no se recifra `raiz` |
| `descargas_mx` patrón B (nuevo bucket) | — | 19 | reportado aparte, nunca oculto |
| `downloads` (fuera de universo) | 1 + 41 | 1 + 41 | sin cambio, fuera de universo del recenso |
| **`C1` total (warn, todas las raíces)** | **185** | **132** | 34 promovidas + 19 patrón B excluidas = 53 menos |

Comando: `python3 tests/corpus.py` (sandbox deshabilitado para alcanzar `descargas_mx` bajo `/mnt/c`).

## C · Residuo categoría C dudoso

**0 residuo nuevo.** El único residuo de categoría C de este acto son las 73 entradas `presente_bajo_otra_raiz` de `descargas_mx` — ya identificadas como coexistencia (no error de captura) en `COMMIT-1` y firmadas `FP-308 (iii)` en `P0`. Ningún otro archivo de las dos raíces cae en categoría C (raíz declarada ≠ raíz física real por error, distinto de coexistencia) — verificado: `data_raw` da `0 presente_bajo_otra_raiz`. No hay tablero de "C dudoso ≤10" que abrir: la única categoría C que existía ya tiene firma.

## Staging

`data/manifiesto-staging.yaml` queda **vacío de candidatos** (comentario explicando por qué la única entrada que no se pudo promover —`descargas.php`— se retiró a mano, con su sha256 citado para no perder el registro).

## Cierre de INFRAESTRUCTURA

Ver `data/INFRAESTRUCTURA-v1_0.md`, sección "Coexistencia física `data_raw`/`descargas_mx` regularizada" (dos líneas: coexistencia declarada + reclasificación patrón B).

**El primer resultado que produce este procedimiento es el que se reporta.**
