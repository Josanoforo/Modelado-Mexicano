# ACTO MAESTRA38-A6 · P0 · Reconciliación notas → cola

**Pieza D del encargo**, corrida ANTES del COMMIT-1.
Universo (A.10): árbol del worktree `acto/maestra38-a6-resondeo-negativos` a
`ef9ba36` (= `origin/main`, distancia 0 commits), 6/sep/2026.

## 0 · Comandos y conteos (A.13)

```
$ command grep -rl "NO-OBTENIDO-POR-ESTE-AGENTE" forense/ data/ | wc -l
43
$ command grep -rn "NO-OBTENIDO-POR-ESTE-AGENTE" forense/ data/ | wc -l
138
$ command find forense/ data/ -type f | wc -l
2788
```

**Discrepancia con la premisa del encargo, declarada.** El encargo dice
«43 archivos hoy (1 294 examinados)». Los 43 archivos se reproducen
exactos. El denominador **no**: este acto mide **2 788** archivos bajo
`forense/` + `data/` (`data/raw` es symlink y `-r` no lo sigue, así que
el corpus no entra en la cuenta). El `1 294` del encargo no se reproduce
con ningún comando de este acto; se declara la diferencia en vez de
heredarla. La conclusión de P0 no depende del denominador — depende de
los 43 archivos y las 138 líneas, que sí se reproducen.

**Trampa de la caja, pagada.** `grep` en esta máquina es una función que
envuelve `ugrep -I`: descarta en silencio cualquier archivo con un byte
no-UTF8. Todo conteo de arriba usa `command grep`. Igual `command find`
(`find` aquí es `bfs`).

## 1 · Método — diferencia de conjuntos, no léxico

1. Universo de la cola = columnas 2 y 3 (`fuente_canonica`,
   `fuente_canonica_normalizada`) de
   `data/curacion-registro/cola-adquisicion-registro.tsv` → **132** nombres
   distintos.
2. Menciones fuera de los dos TSV de cola (ahí el objeto es la columna 2
   por construcción, no hay nada que inferir) → **117** líneas.
3. Candidatos = tokens `UPPER_SNAKE` (40 distintos) **más** tokens
   `ALLCAPS` de una palabra, sobre esas 117 líneas.
4. `comm -23 candidatos cola` y revisión línea por línea de las 117.

El paso 4 se hizo a mano sobre las 117 líneas completas, no solo sobre el
`comm`: un objeto puede nombrarse en prosa sin token en mayúsculas, y una
diferencia léxica no es una diferencia de conjuntos.

## 2 · Salida — las tres clases que el encargo pide

### 2.1 · YA-EN-COLA con estado aún abierto (7) — entran a P1 por la cola, no por aquí

| objeto | estado hoy |
| --- | --- |
| `BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO` | `NO-OBTENIDO-POR-ESTE-AGENTE(31 intentos)` |
| `SICEE` | `NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)` |
| `PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND` | `OBTENIDO-PARCIAL` |
| `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` | `OBTENIDO-PARCIAL` |
| `ENJUVE` | `OBTENIDO-PARCIAL` |
| `REUTERS_DNR` | `OBTENIDO-PARCIAL` |
| `ENAFIN` | `OBTENIDO-PARCIAL` |

### 2.2 · YA-OBTENIDO — la nota quedó vieja (14). Una línea en `hallazgos.md`, NO se catalogan

Regla del encargo: «YA-OBTENIDO (la nota quedó vieja) → se anota en
hallazgos.md, una línea por caso, no se cataloga».

| objeto | estado real en la cola | mención vieja (archivo:línea) |
| --- | --- | --- |
| `EXT_OF_11_REUNE_REDECO` | OBTENIDO | `forense/notas/2026-09-03-MAESTRA37-A2-PAQUETE-RECETAS-3.md:15` |
| `TEPJF_ELECCIONES_CONCURRENTES_1991_2018` | OBTENIDO | `forense/notas/2026-09-03-MAESTRA37-A2-PAQUETE-RECETAS-3.md:17` |
| `IETAM_TAMAULIPAS_SERIE_MUNICIPAL` | OBTENIDO | `forense/notas/2026-09-03-MAESTRA37-A2-PAQUETE-RECETAS-3.md:18` |
| `IEEPCO_OAXACA_SERIE_MUNICIPAL` | OBTENIDO | `forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md:56` |
| `MEXICO_PANEL_STUDY_2012` | OBTENIDO | `forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md:50` |
| `CNGMD` | OBTENIDO | `forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md:75` |
| `CERO_DESABASTO` | OBTENIDO | `forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md:134` |
| `OBSERVATORIO_DE_CUIDADOS_INDICADORES_TERRITORIALES` | OBTENIDO | `forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md:149` |
| `EXT_OF_03_PARTICIPACION_LOCAL_2024` | OBTENIDO | `forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md:190` |
| `EXT_OF_12_PREP_2024` | OBTENIDO | `forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md:221` |
| `WVS` | OBTENIDO | `forense/notas/2026-08-31-agente-adquisicion-1-cierre.md:75` |
| `IEE_AGUASCALIENTES_SERIE_MUNICIPAL` | OBTENIDO | `forense/encargos/2026-09-02-MAESTRA35-L3-CIVICA-TIPO-DE-BOLETA.md:23` |
| `PDN_SESNA_S1_S2_S3_S6` | OBTENIDO | `forense/encargos/2026-09-06-ADENDA-A4-rutas-PDN.md:13` |
| `EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI` | OBTENIDO **bajo otro nombre** | `forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md:174` |

**El caso 14 es de otra clase y se separa.** `EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI`
no tiene fila con ese nombre: la fila existe como
`DGIS_URGENCIAS_CUBO_IMSS_INEGI` (OBTENIDO). Es un **alias caduco**, no
una fila faltante — buscarlo por su rótulo viejo da un falso
`SIN-FILA`. Identificar el contenido por su identidad y no por su
rótulo es lo que evita darlo de alta dos veces.

### 2.3 · SIN-FILA (2) — alta en la cola, entran a P1

| objeto | qué es | origen (archivo:línea) | lo que la nota origen midió |
| --- | --- | --- | --- |
| `RUPC` | Registro Único de Proveedores y Contratistas (reporte `norah` de CompraNet) | `forense/notas/2026-09-03-MAESTRA36-A2-P1-P3-compranet-llaves.md:96` | «el endpoint `norah` del reporte RUPC **existe y rechaza** (403 de aplicación, no 404): necesita sesión» |
| `DD_*` (los tres diccionarios de datos de CompraNet) | `DD_*.xlsx` bajo `upcp-compranet.funcionpublica.gob.mx/publicas/` | `forense/notas/2026-09-03-MAESTRA36-A2-P1-P3-compranet-llaves.md:258` | «`DD_*` del encargo: no se obtuvieron» |

Los dos son piezas del mismo hueco que la fila
`EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6` ya nombra («persona + sanción»),
pero **ninguno tiene fila propia** y por eso ningún proceso los vuelve a
tocar. Se dan de alta con `NO-OBTENIDO-POR-ESTE-AGENTE` heredado y nota
`alta por reconciliación A6, origen <archivo>:<línea>`, como el encargo fija.

## 3 · Contra la premisa del encargo — clase A6, medida

El encargo pide «corregir las 6 etiquetas caducas: UNAM, ECOPRED, Cultura
Constitucional (ya OBTENIDO por A4), CNGMD (646 entradas en corpus), y las
2 que P0 identifique», y lista `INE` y
`FINTECH_LENDING_TO_BORROWERS_WITH_NO_CREDIT_HISTORY` como `SIN-FETCH` a
abrir byte a byte.

**Medido contra el árbol, los seis ya están corregidos.** Los seis
objetos que el encargo nombra tienen hoy `estado_A4A5 = OBTENIDO` en el
registro:

```
$ awk -F'\t' 'NR>1 && ($2 ~ /UNAM|ECOPRED|CULTURA|CNGMD|^INE$|FINTECH/){print $2" -> "$5}' \
    data/curacion-registro/cola-adquisicion-registro.tsv
CNGMD -> OBTENIDO
FINTECH_LENDING_TO_BORROWERS_WITH_NO_CREDIT_HISTORY -> OBTENIDO
INE -> OBTENIDO
LOS_MEXICANOS_VISTOS_POR_SI_MISMOS_UNAM_IIJ_2015 -> OBTENIDO
ECOPRED_2014_INEGI -> OBTENIDO
CULTURA_CONSTITUCIONAL_UNAM_IIJ -> OBTENIDO
```

`SIN-FETCH` sobrevive **sólo en la columna `nota`**, que es historia
fechada y no estado. Ninguno de los seis es una etiqueta caduca en
`estado_A4A5`; corregirlos sería reescribir el registro de qué se sabía
cuándo. **Etiquetas caducas en `estado_A4A5`: 0.**

Y las «2 que P0 identifique» no son etiquetas caducas: son **filas que
faltan** (§2.3). La clase A6 del encargo, tal como está escrita, no tiene
objeto en el árbol de hoy; lo que P0 sí encontró es otra cosa y se
entrega como tal.

## 4 · Contador de P0

- archivos con la mención: **43** (premisa del encargo reproducida)
- líneas con la mención: **138**
- líneas fuera de los dos TSV de cola, revisadas una por una: **117**
- objetos distintos nombrados: **23** (más las menciones genéricas de vocabulario)
- **YA-EN-COLA con estado abierto: 7**
- **YA-OBTENIDO (nota vieja): 14** — una línea cada uno en `hallazgos.md`, no se catalogan
- **SIN-FILA: 2** (`RUPC`, `DD_*`) — alta en la cola, entran a P1
- **etiquetas caducas en `estado_A4A5`: 0** (la premisa A6 del encargo ya estaba saldada)
