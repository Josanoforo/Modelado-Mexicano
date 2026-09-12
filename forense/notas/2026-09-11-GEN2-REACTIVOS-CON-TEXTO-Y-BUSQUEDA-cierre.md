# Cierre · GEN2-REACTIVOS-CON-TEXTO-Y-BUSQUEDA

Fecha: 11/sep/2026. PR: **#737**. Entorno: **CAJA Ubuntu/WSL2**. Worktree: `/home/pc0/mm-gen2-reactivos-contexto-busqueda`; rama: `acto/gen2-reactivos-contexto-busqueda`. Arranque efectivo: `origin/main=9472223f6b463c31b6c9f3129bd26e95bf992b00`; sincronización antes del cierre: `origin/main=7a59c0eb84923e50dcb1a373a9c7d6fd34a34f04`. El corpus compartido quedó montado y `numpy`, `pandas`, `pyreadstat`, `dbfread`, `openpyxl`, `pyreadr` y `xlrd` estuvieron disponibles.

## Resultado

Se publica `data/inventario-reactivos-contexto-v1_0.tsv`, overlay sucesor de 22,367 filas (22,350 identidades lógicas) con texto acreditado. No modifica ni reordena `inventario-reactivos-v1_2.tsv` o `inventario-reactivos-ext-v1_0.tsv`: cada fila conserva la identidad histórica mediante `id_origen` (`v1_2:<fila>` o `ext:<fila>`). El campo `contexto_busqueda` contiene vocabulario editorial de recuperación claramente separado; no se atribuye como texto literal del instrumento. SHA-256 publicado: `b45813d4f63856f83486f4658c2eb65f9195bb7e2f6f894dad3aceb5947f2342`.

El extractor `tools/actualiza_reactivos_contexto.py`:

- lee sólo metadatos nativos y documentación pública conocida, nunca valores de microdatos;
- distingue `ETIQUETA_VARIABLE`, `PREGUNTA_DICCIONARIO` y `PREGUNTA_COMPLETA`;
- conserva instrumento, ola, payload, tabla/miembro, variable, SHA de la fuente y localizador;
- acepta `--objeto` repetible, publica mediante archivo temporal + `os.replace` y cachea por SHA-256 completo de la fuente + formato + versión `reactivos-contexto-1.0.0`;
- conecta la operación incremental al cierre manual compatible de `.claude/commands/adquiere.md`, sin añadir scheduler ni tocar cron.

Primera ejecución real: 21 fuentes procesadas, 0 hits / 21 misses, 22,367 publicadas y 33,528 residuales dentro del perímetro prioritario. Segunda ejecución idéntica: 21 hits / 0 misses y el mismo SHA de salida.

`tools/busca_reactivos.py` usa ahora `--fuente vigente` por defecto: overlay primero y las dos tablas históricas después, deduplicadas por `payload_id + archivo_miembro + variable_id`. La salida sigue mostrando el `id_origen` histórico y añade tipo, contexto y referencia acreditada. `--fuente ambas` y `--tablas hoy` conservan la vista anterior.

## Cobertura medida

| Familia | Filas históricas del perímetro | Con texto en overlay | Residual |
|---|---:|---:|---:|
| ENVIPE | 31,140 | 1,248 | 29,892 |
| ENNViH | 17,181 | 17,176 | 5 |
| ENCUCI | 458 | 2 | 456 |
| ENIF | 6,747 | 3,572 | 3,175 |
| ENSAFI | 369 | 369 | 0 |
| **Total** | **55,895** | **22,367** | **33,528** |

Tipos publicados: 17,177 etiquetas nativas, 5,179 preguntas de diccionario y 11 preguntas completas revisadas. De los 102 grupos históricamente ciegos de NC-0136, 21 ganan al menos una fila con texto. Esto no equivale a terminar los 116 instrumentos.

## Antes / después del buscador

La vista histórica contiene 241,591 filas físicas; tras eliminar sus 1,519 identidades duplicadas revisa 240,072 identidades lógicas y 24,138 textos. Antes, los seis comandos siguientes daban 0 candidatos. La vista vigente revisa las mismas 240,072 identidades lógicas, ahora 29,311 con texto, y declara 23,886 filas históricas sombreadas por el overlay.

| Necesidad | Antes | Después | Ejemplo exacto y fuente |
|---|---:|---:|---|
| denuncia ENVIPE | 0 | 28 | `envipe2025/BP1_23`: “1.23 ¿Cuál fue la razón principal por la que no denunció o no denunciaron el delito ante el Ministerio Público o Fiscalía Estatal?” — `fd_envipe2025.pdf`, SHA `83fe02467b66`, p. 73 |
| tandas ENNViH | 0 | 52 | `ennvih2002/crh01_1e`: “TANDA GUARDA AHORROS MH” — etiqueta nativa de `ennvih/ehh02dta_all.zip`, SHA `8b9b51904ca8`, miembro `ehh02dta_all/ehh02dta_b2/ii_crh.dta` |
| ahorro ENIF | 0 | 280 | `enif2024/P5_1_5`: “5.1 En los últimos 12 meses, de junio de 2023 a la fecha, ¿usted participó en una tanda?” — `enif_2024_fd.xlsx`, SHA `17e2ad86ce9e`, hoja `TMODULO`, fila 342 |
| corrupción ENCUCI | 0 | 2 | `encuci2020/AP5_17`: pregunta 5.17 sobre solicitud de dádiva, favor o dinero extra — `FD_ENCUCI2020.pdf`, SHA `6cd6f7475a0b`, p. 35, sección 5 |
| atraso ENSAFI | 0 | 3 | `ensafi2023/P6_7`: “6.7 ¿Usted se ha atrasado en el pago de uno de estos préstamos o créditos?” — `ensafi2023/ensafi_2023_fd_xlsx.zip`, SHA `37bd0cb6dd54`, `TMODULO`, fila 350 |
| afrontamiento ENSAFI | 0 | 1 | `ensafi2023/P6_10_2`: “6.10 Durante el último mes, para cubrir sus gastos, ¿usted utilizó el dinero que tenía ahorrado?” — misma fuente, `TMODULO`, fila 365 |

Los conteos son candidatos del índice, no afirmaciones de cobertura del universo científico completo.

## Residuales y estado de NC

`NC-0100` queda **ABIERTA**. En las tres olas señaladas se cubren `212/400` (ENVIPE 2012), `245/419` (2013) y `24/485` (2015): 481/1,304, con 823 identidades DBF pendientes de correspondencia exacta tabla-variable.

`NC-0136` queda **ABIERTA**. El paro de entorno está resuelto, pero el lote prioritario conserva 33,528 identidades sin texto y quedan 81 de los 102 grupos históricamente ciegos sin una fila nueva acreditada. No se extrapola el lote de cinco familias al alcance entero.

## Verificación

- `python3 -m unittest -v tests.test_reactivos_contexto`: 6/6 OK, incluida la resolución de las 22,367 filas contra identidad/hash histórico.
- ejecución real repetida del actualizador: 21/21 cache hits, 0 misses, salida byte-estable.
- búsquedas vigentes de denuncia, tanda, ahorro, corrupción, atraso y afrontamiento: 28/52/280/2/3/1 candidatos.
- `python3 tests/check.py --baseline`: línea base VERDE, cero fallos nuevos; conserva 3 fallos y 3,115 avisos heredados.
- cero llamadas LLM, cero OCR, cero lectura de valores personales, cero cambios en microdatos, motor, CALC, resultados F5 o cron.

Decisión administrativa: `ADR-485`, renumerada desde 484 al sincronizar con `origin/main=7a59c0e`; actualización L0 y rótulo GEN2 en las vistas canónicas. No mueve contador científico ni adopta parámetros.
