# ACTO MAESTRA33-A4 · REGISTRA-DESCARGAS-MANUALES — cierre por hallazgo

Encargo: `forense/encargos/2026-09-01-MAESTRA33-A4-REGISTRA-DESCARGAS-MANUALES.md`
(SHA de redacción `ee6a8a2`, merge PR #436, sin drift contra `origin/main` real —
verificado `git merge-base --is-ancestor ee6a8a2 origin/main` y `git log
ee6a8a2..origin/main --oneline` vacío al arrancar este acto).

Skill `/acto` de `ADR-237`. `COMPUERTA: ninguna` — declarada, no dispara
verificación, se continuó directo a 0-bis A.3. Worktree propio
`/home/pc0/mm-a4-registra-descargas`, rama `acto/maestra33-a4-registra-descargas-manuales`.

## ARRANQUE

1. REPO: `/home/pc0/mm-a4-registra-descargas`, `ee6a8a2 Merge pull request #436
   from Josanoforo/acto/maestra33-c6-arbitra-r-lote-3`, `git status` limpio al
   crear el worktree.
2. SHA: `HEAD == origin/main == ee6a8a2`, sin drift.
3. `data/raw`: ausente en el worktree fresco (no es PARO) — se enlazó a
   `/home/pc0/mm-corpus/raw` (328 entradas visibles tras el enlace). Se copió
   `data/raices.local.yaml` (gitignorado) desde `/home/pc0/Modelado-Mexicano`
   sin editar su contenido — mismo valor que documentan ~11 worktrees más:
   `descargas_mx: /mnt/c/Users/PC0/Descargas MX`.
4. ENTORNO (A.2, tres partes): `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=<sin_variable>`
   (esperado) · `curl -s -o /dev/null -w "%{http_code}" --max-time 10
   https://www.inegi.org.mx/` → `200` (red real) · `ls data/raw | head -1` →
   `2005trim1_csv.zip` (corpus compartido montado). Consistente con CAJA.
5. ESPEJO: ninguna cifra de este acto sale del espejo del proyecto — todo
   comando corrió contra este clon.

## A.8 — verificación de premisas del encargo

Las tres premisas declaradas por el encargo se verificaron **verdaderas**
contra el árbol de este worktree (no contra un worktree ajeno en otra rama —
lección de sesiones previas, un checkout en una rama WIP puede dar falsos
negativos sobre contenido que sí vive en `origin/main`):

- `PAQUETE-RECETAS-2026-09-01` EXISTE:
  `forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md` (10517 B, 15
  recetas, producido por `ACTO MAESTRA33-A3 · ADQUIERE-2-RUTAS-MULTIPLES`,
  commit `7c892e7`).
- `data/manifiesto.yaml` EXISTE (1192786 B). `data/cola-adquisicion-v1_0.tsv`
  EXISTE (65221 B, 80 filas).

## P1 — descargas manuales: CERO archivos nuevos (A.13, A.4)

**Comando y universo examinado**: `find "/mnt/c/Users/PC0/Descargas MX" -type
f` (raíz `descargas_mx` de `data/raices.local.yaml`) → **122 archivos
examinados**, en la raíz y en la subcarpeta `Descargas Manuales/`. Sin
subcarpetas adicionales (`find -maxdepth 1 -type d` solo devuelve
`Descargas Manuales`).

**Mtime máximo del árbol completo**: `2026-08-13 13:41`
(`Descargas Manuales/MEX_PILP_TB_v1.xlsx`) — anterior en más de dos semanas a
la emisión de `PAQUETE-RECETAS-2026-09-01` (2026-09-01) y a su plazo de
tablero (2026-09-04, sigue vigente, no vencido). Los 122 archivos ya estaban
en el árbol antes de que existiera el paquete de recetas que este acto
procesaría — no son un producto de las 15 recetas, son residuo de caminatas
anteriores (`REG-LOTE3`, `LOTE-UBUNTU-ADQ-1`, `ACTO ADQ-15`, corpus ENSANUT/
WVS/ISSP ya registrados), varios de ellos ya citados por nombre en
`data/cola-adquisicion-v1_0.tsv` (líneas 25, 36) como adquiridos vía
`Descargas Manuales/` en fechas de agosto.

**Cruce de identidad** (A.4 — universo declarado, no solo el rótulo
"no encontrado"): se buscaron por nombre, sobre los 122 archivos, los
patrones distintivos de los 4 archivos con nombre esperado conocible de las
15 recetas (`ICPSR*35024`, `MEX_2023_ES*`, `ayuntamientos_cngmd2023*`,
`SSRN-id2474620*`) más 7 patrones adicionales de host/tema para las recetas
sin nombre de archivo fijo (`cerodesabasto`, `mapadecuidados`, `catalogo
proveedores`, `dgis urgencias`, `prep2024`, `computos2024`, `MEX_2005_CAFR`)
— **0 coincidencias**. Control positivo del propio mecanismo de búsqueda:
`grep -ci enasem data/manifiesto.yaml` → 37 (el grep sí encuentra lo que
existe; el 0 de arriba no es un comando que no corrió, A.13).

**Conclusión P1**: no hay ningún archivo bajado que mover al corpus, hashear
(A.7) o registrar con `descargado_por: mesa-navegador`. Ninguna fila de
`data/cola-adquisicion-v1_0.tsv` cambia de estado por este acto. No se
re-sondeó ninguna receta (mandato explícito del encargo: "sin re-sondear") —
esto es un inventario de archivo local (`find`+`stat`), no una petición de
red.

**CONTADOR**: payloads `OBTENIDO` antes → después de este acto: **sin
cambio, +0**.

## P2 — las 6 necesidades de FP-190: nada que mapear contra "SOLO los payloads nuevos"

El encargo condiciona P2 a los payloads nuevos de P1. P1 produjo cero, así
que el universo que P2 debía mapear es el conjunto vacío — no corre
`/mapea` contra nada (correr una búsqueda semántica contra cero payloads
nuevos no produciría más información que la ya vigente).

Por transparencia, estado real (no tocado por este acto) de las 6 filas
`fp190-1`..`fp190-6` de `data/cola-adquisicion-v1_0.tsv` (líneas 75-80),
trabajadas el mismo día por `ACTO MAESTRA33-A3 · ADQUIERE-2-RUTAS-MULTIPLES`
a partir de `forense/notas/2026-09-01-mapeo-fp190.md` (`MAESTRA33-E7`):

| fila | necesidad | estado | por qué no es "payload nuevo" |
|---|---|---|---|
| fp190-1 | SFT-04 (ayuda para bañarse) | OBTENIDO | diccionario ENASEM ya en corpus desde 2026-08-04, encargo D-2 |
| fp190-2 | CIV-08 (inseguridad en la calle) | PENDIENTE | tarea de extracción de texto sobre ENVIPE ya obtenido, no una adquisición — fuera de perímetro de `/adquiere` |
| fp190-3 | TIC-06 (trabajo infantil todos los meses) | OBTENIDO | diccionario ENTI ya en corpus desde 2026-08-04, encargo B-3 |
| fp190-4 | DIN-07 θ (presupuesto en el hogar) | PENDIENTE | extracción de texto sobre payload Banxico ya obtenido — fuera de perímetro |
| fp190-5 | DIN-11 (conocimiento de cuentas sin comisión) | PENDIENTE | NO-ENCONTRADO, universo agotado (241591 filas, 5 formulaciones) — sin instrumento identificable, nada que un `/adquiere` persiga |
| fp190-6 | SFT-06 (acuerdo entre hermanos para el cuidado) | PENDIENTE | NO-ENCONTRADO, universo agotado — mismo caso |

Adicionalmente, verificado por lectura de ambos documentos: ninguna de las 15
recetas de `PAQUETE-RECETAS-2026-09-01` (World Bank Enterprise Survey 2023,
ICPSR Mexico Panel Study, CNGMD, microseguro cenfri/SSRN, Tanda+ ×2, World
Bank Capital Returns León, CeroDesabasto, Observatorio de Cuidados, catálogo
CompraNet, cubo de urgencias DGIS, PREP2024) corresponde temáticamente a
ninguna de las 6 necesidades de FP-190 — así que aun en un escenario
contrafactual donde mesa ya hubiera ejecutado las 15 recetas hoy, ninguna
habría sido candidata para estas 6 celdas/θ. No se redacta el lote
`C10 · REGLAS-OLA5-FASE2-B`: su gate explícito ("si alguna pasa a
EXISTE-SATISFACE") no se cumplió — no hubo ninguna candidata nueva que
evaluar.

## Recibo en el tablero de PAQUETE-RECETAS-2026-09-01

Ver `forense/notas/2026-09-01-PAQUETE-RECETAS-2026-09-01.md`, sección
"Tablero": recibo añadido ahí mismo (no se edita la fila original) —
verificado 2026-09-01, 0 de 15 recetas ejecutadas todavía, plazo 2026-09-04
sigue vigente, no vencido.

## Cierre

Encargo A.5-consistente: ningún negativo de este acto es un comando que no
corrió (A.13 declarado en cada uno); ningún negativo se sella sin universo
(A.4 declarado). No se abrió microdato para medir, no se cargaron reglas, no
se descargó por red — perímetro respetado íntegro. `PERÍMETRO` tocado:
`data/raw` (symlink, no contenido), `notas`, `tablero (recibo)`; `manifiesto`
y `cola-adquisicion` se leyeron, no se escribieron (nada que actualizar).

CONTADOR final: payloads `OBTENIDO` +0.
