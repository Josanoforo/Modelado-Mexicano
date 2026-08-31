# MAESTRA32-E12 · EXTRACTOR-FD — cierre (COMMIT-2, corrida única)

Rama (b) de FP-175, entrada (2) de FP-179 → EJECUTADA.

## Corrida

`python3 tools/inventario_fd_ext.py` sobre el perímetro congelado en COMMIT-1 (46 payloads, `forense/notas/2026-08-30-fd-ext-spec.md`). Salida: `data/inventario-fd-ext-v1_0.tsv` (10,635 filas + cabecera comentada de 3 líneas + fila de encabezado = 10,638 líneas).

Por payload (estado, filas): 40 `OK`, 6 `SIN-CAMPOS-EXTRAIBLES` (0 filas cada uno) — `endireh2003/fd_endireh2003.pdf`, `enut2002_fd.pdf`, y los 4 HTML (`enut2009/2014/2019/2024_diccionario_variables.html`). Cero `ERROR:*`, cero `NO-EXTRAIDO:*` (todos los 46 están dentro de las extensiones despachadas por este acto). Detalle completo con conteo por payload: log de la corrida (stderr), reproducible con el mismo comando.

## Cobertura (B-bis)

1. **Payloads con ≥1 fila**: 40/46 = **87.0%** — por encima del falsador (<50% ⇒ abandonar la vía); la vía NO se abandonó.
2. **Filas con texto**: 10,635/10,635 = **100%** — el propio filtro de extracción descarta cualquier fila sin `texto_reactivo` no vacío (`if not val_id or not val_texto: continue` en las tres rutas), así que toda fila que entra a la tabla ya trae texto por construcción.

Los 4 HTML en 0 filas son el 100% del formato HTML de este perímetro: los 4 archivos `*_diccionario_variables.html` de ENUT no traen ninguna `<table>` con un encabezado que case `ID_LABELS`/`TEXT_LABELS` (verificado abriendo `enut2009_diccionario_variables.html`: el diccionario está en prosa/lista, no en tabla marcada). Hallazgo de heterogeneidad real (b-bis, rama baja): esta ficha concreta de ENUT no sigue el patrón tabular que sí siguen los PDF/XLS del mismo perímetro.

## Control positivo (pre-registrado en COMMIT-1, no ajustado tras ver el resultado)

| payload | extraídos (únicos) | referencia (únicos) | solape | % | validado (≥60%) |
|---|---|---|---|---|---|
| `fd_envipe2025.pdf` | 12 | 508 | 9 | **75.0%** | SÍ |
| `FD_ENCUCI2020.pdf` | 14 | 389 | 0 | **0.0%** | NO |

**Veredicto declarado por la regla de COMMIT-1**: como los dos controles son ambos sobre PDF y uno de los dos (`FD_ENCUCI2020.pdf`) cae por debajo de 60%, el parser de PDF se reporta **NO VALIDADO para el formato .pdf en general** — pese a que `fd_envipe2025.pdf` sí solapa al 75%. La regla congelada dice "si un control cae por debajo, el parser se reporta como NO VALIDADO para ese formato"; no distingue entre "válido en un caso, inválido en otro dentro del mismo formato" — así que el veredicto agregado es NO VALIDADO, no un promedio ni un 1-de-2. El esquema de la tabla es intocable (9 columnas fijas); esta declaración vive aquí y en el ADR, no en una columna nueva.

**Causa observada de la falla en `FD_ENCUCI2020.pdf`** (documentada, NO usada para ajustar el regex — el falsador/control ya corrieron y no se itera): el texto de esa ficha en particular trae varios mnemónicos por línea de tabla PDF (ej. `AP4_3_1 AP4_3_2 AP4_3_3 AP4_3_4` extraído como un solo `variable_id`), y algunas celdas de encabezado/leyenda (`Mnemónico`, `ENCUCI`, `(3)`) se colaron como filas — la tabla de esa ficha tiene una estructura de columnas más irregular que la de `fd_envipe2025.pdf`. Candidato de trabajo para un acto sucesor, NO resuelto aquí (regla de tope: no se generaliza el parser en esta misma corrida).

## Intocables — verificado

`git diff --stat` vacío contra: `data/inventario-reactivos-v1_0.tsv`, `data/inventario-reactivos-v1_1.tsv`, `data/inventario-reactivos-ext-v1_0.tsv`, `data/inventario-fd-v1_0.tsv`, `data/inventario-fd-v1_1.tsv`, `data/cobertura-composicion-v1_0.tsv`, `tools/inventario_reactivos.py`, `tools/inventario_reactivos_ext.py`, `tools/etiqueta_v1_2.py`. Confirmado antes de este commit.

## Cierre anti-PR#77

`git status --short --ignored` no muestra nada nuevo en `data/raw` (el corpus compartido en `/home/pc0/mm-corpus/raw` no recibió escritura de este acto — este acto NO descarga nada, solo lee payloads existentes). Nada quedó en `tmp/`. Los dos únicos archivos nuevos rastreados por git son `tools/inventario_fd_ext.py` y `data/inventario-fd-ext-v1_0.tsv`, ambos declarados en el perímetro del encargo.

## CONTADOR

- Payloads con ≥1 fila: **439 → 479 de 720** (+40, todos del perímetro no-xlsx de este acto; ninguno de los 40 estaba ya contado en el 439, porque `FORMATOS_SIN_CAMPOS` los ponía en 0 filas por diseño antes de este acto).
- Filas FD nuevas: **10,635**.
- Filas con texto: **10,635** (100% de las nuevas).
- Control positivo: 75.0% (`fd_envipe2025.pdf`, validado) / 0.0% (`FD_ENCUCI2020.pdf`, no validado) → **veredicto agregado del formato PDF: NO VALIDADO**.

## FP-179, entrada (2)

EJECUTADA por este acto (rama b). Rama (a) ya corrió (ADR-228, 123/133). Fila-grito de FP-179 se actualiza en la cascada de `forense/firmas-pendientes.tsv`.
