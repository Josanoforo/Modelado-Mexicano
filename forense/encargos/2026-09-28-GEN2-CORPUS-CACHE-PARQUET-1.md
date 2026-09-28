# ENCARGO · ACTO GEN2-CORPUS-CACHE-PARQUET-1 · Caja está limitada a dos sesiones pesadas porque cada CALC carga en memoria el CSV completo de ENCIG, ENVIPE, ENIGH, ENOE o ENDIREH (hasta 250 MB comprimidos, varios GB en pandas) en una máquina de 24 GB. Este acto construye la caché columnar (Parquet) del corpus que la demanda y los lotes usan, con sha de origen y de caché registrados como constancia, un cargador único con proyección de columnas, y la medida de memoria y tiempo antes/después que permita a mesa levantar el tope

> ENTORNO: **CAJA** — lee el corpus montado y escribe la caché junto a él. Convierte **solo olas no reservadas** (leer el contenido para convertir es abrir; una ola reservada se convierte únicamente cuando su código congelado la abra). Hook imprime ENTORNO-DERIVADO; si dice cloud_default o milpa-inegi, PARA. Es una sesión pesada mientras convierte; después, ninguna.

CABECERA · SHA de redacción `16ba3d02` (re-deriva al abrir) · una sesión, rama propia · MODELO: **Opus** para P1 y P4 (qué entra a la caché y cómo se sella), Sonnet admisible para la conversión · MODO: **ABIERTO**, cláusula v1.0 · ids con raíz de acto · D-21 aplica.
CONTADOR: **cero mediciones; no adopta**. No crea payloads: la caché es derivado del payload (mismo id + sufijo), no entrada nueva del manifiesto; su sha queda como constancia (D-22(4)).

## 1 · OBJETIVO
(P1) **Qué entra.** Universo derivado: los payloads que `demanda-corridas.tsv` (105 corridas), los CALC sellados de `data/corrida0/` y las familias 2027 citan por id, filtrados a olas sin campo de reserva en el manifiesto y no listadas en la hoja consolidada como «reserva sin decidir». Lista con id, formato, tamaño, y si se convierte o por qué no (RESERVADA · FORMATO-NO-TABULAR · YA-PEQUEÑO).
(P2) **Conversión y constancia.** Por payload: extraer del zip (A.7: dos hashes del miembro), leer con tipos declarados desde el FD (no inferidos), escribir Parquet particionado por tabla del instrumento en `data/cache/<id>/`, y registrar `data/cache/constancias.tsv` (id · miembro · sha256_origen · sha256_parquet · filas · columnas · fecha · versión del conversor). Igualdad verificable: recuento de filas y de columnas y una comprobación de valores por columna contra el CSV (suma o hash por columna), con salida cruda.
(P3) **Cargador único.** `tools/corpus_loader.py`: `cargar(id, tabla, columnas=[...])` lee Parquet con proyección; si no hay caché, lee el CSV y lo dice; verifica el sha de constancia contra el archivo antes de devolver; nunca escribe. Los medidores nuevos lo usan; los sellados **no se tocan** (E.3): lo que ya midió sigue midiendo del CSV.
(P4) **Medida.** Memoria pico y tiempo de un CALC representativo (ENCIG 2023 marginales por eje, o el que `PISOS-Y-ADENDAS-1` acabe de correr) leyendo CSV vs Parquet con proyección, con el comando y las cifras crudas; recomendación a mesa de cuántas sesiones caja caben a la vez con 24 GB, con el cálculo.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: `constancias.tsv` con una fila por miembro convertido y `sha256sum` reproducible sobre cada Parquet · 0 olas reservadas en `data/cache/` (cruce con el manifiesto) · test huérfano que compara filas/columnas Parquet vs CSV en dos payloads pequeños · P4 con las cifras en la nota · ningún sello ni medidor existente cambió (`git diff --stat` sobre `data/corrida0/` = vacío) · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
Transfer 26/sep §6 (mandato de mesa): «Máximo dos sesiones de caja pesadas a la vez hasta que la caché Parquet exista (diferida)» — este acto es esa caché. D-14: defecto real → lotes de caja en serie (PISOS-Y-ADENDAS-1 y RELEVO-TRAMITE-CAJA-1 hoy se turnan); costo → días de cola en el único entorno que mide. D-22(4), D-23, E.3, E.6 (reservadas no se abren), A.7. Mesa 28/sep: «¿por qué tenemos solo 2 sesiones trabajando en caja?». **Levantar el tope es de mesa**, con la cifra de P4.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `16ba3d02` · manifiesto: 7 193 entradas con tamaño, 41.2 GB; sin ninguna entrada ni herramienta con «parquet» o «cache» en el árbol (`git ls-tree | grep -ci` = 0). Los payloads que miden son zips CSV/DBF de 50–250 MB (ENOE 2005 dbf 246 MB, EIC 2025 762 MB, CCPV 486 MB); los mayores del corpus (PDN, réplicas de Dataverse, GDELT, CompraNet) no los usa ningún CALC: no entran.
- [LEÍDO] Transfer 26/sep §1.8: WSL de mesa a 24 GB + 16 GB swap; §6: tope de dos sesiones pesadas. [EXISTE] `tools/manifiesto.py` (sha por id), `corrida0 preflight` (payload COINCIDE en caja: la caché no debe romperlo: el preflight sigue comparando el payload, no la caché).
- [SUPUESTO] Que pyarrow está o se puede instalar en caja (uv); si no, el hallazgo y la receta.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'CACHE\|PARQUET'` → 0. Homónimos: CORPUS-INTEGRIDAD-Y-RESPALDO-1 (sha del corpus; cítalo para los sha de origen), CORPUS-COMPLETO-1. En vuelo en caja: PISOS-Y-ADENDAS-1 (no leer sus archivos de trabajo), RELEVO-TRAMITE-CAJA-1 (arranca después de PISOS: puede ya usar el cargador si este acto cierra antes; si no, lee CSV). Nube: DEMANDA-DICTAMEN-1, REGLAS-Y-RESULT-1, TUBERIA-Y-CURACION-1 (tools/: coordina `corpus_loader.py` por archivo, es tuyo).

## 5 · PIEZAS
P1 → P2 por instrumento (ENCIG, ENVIPE, ENIGH, ENIF, ENCUCI, ENSAFI, ENDIREH, ENVE, ENCRIGE, ENOE olas vistas) → P3 → P4. Rama prevista: CSV con tipos que el FD no declara → columna como texto y hallazgo; miembro con sha distinto al manifiesto → PARA esa conversión (A.1 hash-discordante) y sigue el resto.

## 6 · LATITUD
Orden de instrumentos, partición, compresión, nombres: tuyos. PREGUNTA A MESA: solo la cifra de P4 (cuántas sesiones). NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) convertir u abrir una ola reservada · b) editar un sello, un medidor sellado, el manifiesto (salvo nada), un payload · c) adoptar; declarar vigente un tope distinto de sesiones (mesa) · d) no aplica · e) NUBE · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Reservadas no se convierten» protege **abrir dato** · «Constancia con dos sha antes de que un CALC la cite» protege **congelar** (D-22(4)) · «Sellados intactos» protege **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `data/cache/` (nuevo), `data/cache/constancias.tsv` (registrado en INFRAESTRUCTURA), `tools/corpus_loader.py` + test huérfano, nota, L0, cascada. Ajeno: `data/raw/`, `data/manifiesto.yaml`, `data/corrida0/`, specs. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no toca sellados, no convierte reservadas, no cambia el tope (mesa con P4). Sucesores: los lotes de caja adoptan el cargador en sus specs nuevas; `CACHE-PARQUET-2` para olas que mesa abra. Sin módulo de auditoría. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-CORPUS-CACHE-PARQUET-1-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

- **qué:** P2 · ENIF 2024 (`enif2024_csv`, `enif_2024_enif_2024_bd_csv`) · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: la hoja consolidada (`mapa-instrumentos-alternos`:22-31) lista ENIF 2024 módulo 7 como reserva sin decidir; convertir el CSV lee el módulo 7 · **impacto:** ENIF 2024 (14 CALC sellados, 2 familias 2027) sigue cargándose del CSV; ningún contador se mueve · **sucesor:** GEN2-CORPUS-CACHE-PARQUET-2 (`NC-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-01`)
- **qué:** P2 · olas reservadas (`envipe2026_csv`, `enigh2024_nc_csv`, `conjunto_de_datos_encrige_2020_csv`, `endutih_2025_endutih2025_bd_dbf`) · **por qué:** DIFERIDO-A:GEN2-CORPUS-CACHE-PARQUET-2 -- se convierten cuando su código congelado o mesa las abra · **impacto:** sus CALC leen el original; ningún medidor abierto afectado · **sucesor:** GEN2-CORPUS-CACHE-PARQUET-2 (`NC-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-02`)
- **qué:** test en CI (`tests/test_corpus_loader.py`, job guardias) · **por qué:** DIFERIDO-A:ejecución de FP-398 (a) «librerías en CI» -- pyarrow y zipfile-deflate64 no están en `requirements.txt` (fuera del perímetro); en CI el módulo se salta, en CAJA 9 passed · **impacto:** la CI no ejerce los 7 casos sintéticos · **sucesor:** FP-398 (`NC-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-03`)

## CONSUMIDO

Ejecutado por PR #1284 (rama `acto/gen2-corpus-cache-parquet-1`), ADR `ADR-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-01`, nota `forense/notas/2026-09-28-GEN2-CORPUS-CACHE-PARQUET-1-cierre.md`. Pregunta a mesa: `FP-260928-GEN2-CORPUS-CACHE-PARQUET-1-01aa-01`. Sin adendas.
