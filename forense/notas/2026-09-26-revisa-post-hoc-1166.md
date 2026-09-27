# /revisa --post-hoc · PR 1166 · ASTRA6 C1: universo completo y paquetes para iniciar validación independiente

VEREDICTO: FUSIONABLE-CON-RESERVA
0 BLOQUEA · 4 RESERVA · 0 NO-VERIFICADO · 2 NO-APLICA

El PR ya estaba fusionado cuando se pidió la revisión (26/sep/2026 19:40:20Z, por mesa). Modo `--post-hoc` (bloque 1.4): la vista previa es el merge que ya ocurrió; nada se comenta en GitHub. Esta nota no aprueba, no fusiona y no empuja nada sobre la rama revisada. Fusionar es firmar, y firmar es de mesa.

Entorno de esta revisión: NUBE (hook: `ENTORNO-DERIVADO = NUBE`, corpus no montado, 0 archivos de corpus examinados). El encargo revisado declaraba CAJA para *preparar*; revisar no abre microdato, así que no hay choque. Cero microdato abierto: los paquetes son `.tar.gz` del repo con metadatos, método y listas de insumos, no datos crudos.

## Identidades

| | sha |
|---|---|
| merge | `2c646cba93eebc9189a8135a5369bb45e8d29b89` (= tip de `origin/main` al revisar) |
| BASE (`merge^1`) | `8c4163365c23a35edc4669fe0968b8f3302984d4` |
| HEAD del PR (`merge^2`) | `f43efadf52c1079412e0d545f403630a51bc6168` |
| `git merge-base merge^1 merge^2` | `8c4163365c23a35edc4669fe0968b8f3302984d4` (= BASE: main no se movió bajo el PR) |

Diff `merge^1 merge`: 110 archivos, 52 497 inserciones, **0 líneas borradas** (`git diff --numstat` sumado). Commits: `6c304584` (0-bis) → `43cfbdf7` → `a1447a28` → `6007e495` (merge de main) → `2b655cfc` → `ef61768a` → `f43efadf` (merge de main).

Encargo gobernante: `forense/encargos/2026-09-26-ASTRA6-C1-PAQUETES-1.md` (CONTADOR: «paquetes completos y estimadores cubiertos; cero recálculos y cero adopciones»).

## Hallazgos (por peso)

**R1 · RESERVA · 2.8/enmienda 5 · referencia colgante en el registro de rótulos.**
Esperado: la fila nueva de `canon/registro-rotulos.tsv` cita documentos que existen. Encontrado: la fila 565 cita `forense/validacion-independiente/catalogo-1/README.md`, que no existe en el árbol fusionado.
```
$ ls forense/validacion-independiente/catalogo-1/README.md
ls: cannot access '…/catalogo-1/README.md': No such file or directory
$ git log --oneline -1 -- forense/validacion-independiente/catalogo-1/README.md
(sin salida)
```
Causa localizada, no toca identidad, universo, estimación, consumo ni decisión → RESERVA. Propuesta: que el ejecutor del siguiente acto C1 cambie esa cita a `…/catalogo-1/astra6-c1-paquetes-guia.md` (el documento que sí cita el ADR).

**R2 · RESERVA · 2.3 (ceguera de C1) · la separación del lanzamiento es de archivos, no de red; el repo es público.**
`tools/validacion/astra6_catalogo/astra6_lanza_catalogo.sh --ejecuta` monta `/etc/resolv.conf` y `/etc/ssl` para llegar a la API. Su guarda solo comprueba el sistema de archivos (`test ! -e /home … test ! -e /work/.git`). El repo tiene `visibility: public` (GitHub, `search_repositories repo:Josanoforo/Modelado-Mexicano`), y en él están `canon/catalogo-del-mexicano-v1_1.tsv` (con `punto`/IC) y `…/catalogo-1/preparacion/catalogo-al-corte.tsv.gz`. En `--ejecuta`, la ceguera descansa en la instrucción, no en la separación. **Está declarado** (`lanzamientos.md:80`: «La red de API permanece disponible; el encargo prohíbe obtener esperados…»), y el `recibo-entrada.json` materializado nace con la reserva NO-CIEGA. `SEPARACION-EFECTIVA` de `--prueba` es cierta solo en su alcance de archivos. Esto no bloquea esta preparación, pero condiciona el rótulo del sucesor. Propuesta: salida de red limitada al host de la API en `--ejecuta`, o conservar `REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA` como rótulo por omisión hasta que exista esa restricción.

**R3 · RESERVA · 2.3 · escritura fuera del §9 propio, declarada.**
Fuera de `catalogo-1/`, `tools/validacion/…` y la prueba propia, el PR toca `canon/L0/ADR-…-6c30-01.md`, `canon/gobernanza-v1_15.md` (+2), `canon/registro-rotulos.tsv` (+1), `data/INFRAESTRUCTURA-v1_0.md` (+2), `forense/analisis/ci-guardias/censo-tests.tsv` (+1), `forense/no-corrido.tsv` (+2) y la nota con su sidecar: todo es perímetro de cierre (D-21), y todo solo añade líneas (0 borradas). Además archiva los otros cinco encargos ASTRA6 (C2 ENCIG, ENIF, ENVIPE; C3 SOCIAL, CONSUMO-FAMILIA) con `fuentes/ASTRA6-lanzamiento-20260926/`. Eso está fuera del perímetro de C1, pero declarado con razón en `LEEME-ARCHIVO.md` («solicitado por mesa durante la sesión C1; no se ejecutaron sus instrucciones») y en el cuerpo del PR → RESERVA, no BLOQUEA.

**R4 · RESERVA · 2.9/A.3 · 24 WARN T03 nuevos: los encargos citan archivos que no están en el árbol.**
`check.py --baseline` lista, para cada uno de los seis encargos ASTRA6 archivados, tres citas sin archivo: `MISION-ASTRA-6-ADENDA-1.md` (×6), `MISION-ASTRA-6-integridad-y-frontera.md` (×6) y `PROPUESTA-ASTRA-6-PARA-CLAUDE-2026-09-26.md` (×6). A eso se suman 6 citas de `00-LEEME-LANZAMIENTO.md` a los nombres con prefijo `01-…06-`, que `rutas-archivadas.json` resuelve.
- Las dos MISION están **embebidas** entre marcadores con sha dentro de cada encargo (`…C1-PAQUETES-1.md:109-196`), así que su texto sí está en el repo, aunque no como archivo propio.
- `PROPUESTA-ASTRA-6-PARA-CLAUDE-2026-09-26.md` la cita la ADENDA-1 como «Base» (`…C1-PAQUETES-1.md:178`), pero **no está embebida ni archivada**:
```
$ git ls-tree -r --name-only origin/main | grep -c PROPUESTA-ASTRA-6
0
```
Es un WARN: no adjudica (D-16) y no cambia nada de C1 (la precedencia la dan la firma y la ADENDA-1, que sí están). Es texto de dirección, no de Astra. Propuesta: que dirección archive la PROPUESTA y las dos MISION como archivos propios con su `.sha256` en un trámite. Eso además despeja las mismas premisas del encargo GEN2-RECIBO-ASTRA6-N.

## Tabla de los once puntos

| # | punto | estado | comando · salida (recortada) |
|---|---|---|---|
| 2.1 | Encargo verbatim, 0-bis primero, cuerpo intacto, coherencia | PASA | `git log --reverse merge^1..merge^2 \| head -1` → `6c304584 0-bis ASTRA6-C1`. El encargo sale en 2 commits; `git diff 6c304584 ef61768a -- <encargo>` → único hunk `@@ -208,3 +208,13 @@`, que añade `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` después del cuerpo. `python3 tools/verifica_sidecars.py` → `[cuerpo] CASA …ASTRA6-C1-PAQUETES-1.md.cuerpo.sha256 · candidato=prefijo-antes-de-linea-211`; `FAIL: 0 — VERDE`. sha256 del prefijo = `58e3b474…35ba` = línea `01-…C1-PAQUETES-1.md` de `SHA256SUMS.txt` de la entrega. Coherencia P1–P4: ver 2.11. |
| 2.2 | Spec congelada antes de resultados | NO-APLICA | Preparación NO CIEGA sin resultados: CONTADOR «cero recálculos»; `universo.tsv` col. `estado` → `NO-EVALUADO` 36 143/36 143. La compuerta propia (hash de paquete antes de entregar) se cubre en 2.5. |
| 2.3 | Perímetro | RESERVA (R2, R3) | `git diff --name-only merge^1 merge` agrupado: 82 en `catalogo-1/`, 3 en `tools/validacion/`, 1 test, 16 encargos+sidecars, 4 `fuentes/`, 2 nota, 6 gobierno/cierre. Rutas vedadas (`replay-evidencia`, `.github/`, `data/corrida0`, `milpa/`, `manifiesto`, `catalogo-del-mexicano`, `firmas-pendientes`) → 0; la única coincidencia léxica fue `…/endireh-pisos-2021-decisiones-0001/…tar.gz`, un nombre de paquete, falso positivo de `decisiones`. |
| 2.4 | Negativos con conteo | PASA | «cero validaciones declaradas»: `astra6_paquetes.py --verifica` recorre 36 143 filas. «0 filtraciones»: re-derivado aquí sobre **476 miembros de 68 contenedores** (ver 2.5). |
| 2.5 | Cifras re-derivadas | PASA | 9 de 9 re-derivadas, ninguna contradicha. `universo.tsv` (csv.DictReader) → 36 143 filas, 68 paquetes. `lotes.json` → DISPONIBLE 9 / 3 371; INCOMPLETO 59 / 32 772; lote 1 `endireh-pisos-2021-comunitaria-0001` = 100. Catálogo en `4f125e70` → sha256 `11e35bfc…b6b7` (= `corte.json`), 36 143 filas, 68 CALC, 1 210 RESULT; `git diff --stat 4f125e70 2c646cba -- canon/catalogo-del-mexicano-v1_1.tsv` → vacío. sha256 de los 68 contenedores vs `sha256_contenedor` → 68 ok / 0 mal. `corrida0.py status` → `celdas_validadas=219` (la nota dice 219 → 219). |
| 2.6 | Originales intactos | PASA | `git diff --numstat merge^1 merge` → columna de borradas = 0 en los 110 archivos. |
| 2.7 | Escala y universo | PASA | Toda cantidad nueva es un conteo de estimadores, paquetes, CALC o RESULT, con universo = catálogo v1.1 al corte `4f125e70` (sha en `corte.json`). Ninguna cifra sobre México entra al canon. |
| 2.8 | Ids con raíz | RESERVA (R1) | `ADR-260926-GEN2-ASTRA6-C1-PAQUETES-1-6c30-01`, `NC-…-6c30-01/02`: `6c30` = 0-bis `6c304584`; la gramática casa. Gobernanza: solo +2 líneas al final, cabecera de conteo sin tocar. Referencia colgante → R1. |
| 2.9 | `check.py --baseline` | PASA (WARN → R4) | `pip install -r requirements.txt pytest`; `python3 tests/check.py --baseline` sobre el árbol fusionado (`2c646cba`) → `LÍNEA BASE: VERDE — sin FAIL nuevos frente a tests/baseline.json (HEAD congelado 7100cd03…)`, `exit=0`. FAIL presentes: T06 (2) y T08 (1), ya en la línea base. `WARN NUEVOS (estado, no adjudican): 145`, de los cuales 24 vienen de este PR (T03, ver R4). `git diff --stat merge^1 merge -- tests/baseline.json` → vacío. `pytest -q tests/test_astra6_paquetes.py` → `6 passed`. `astra6_paquetes.py --verifica` → `VERDE: cobertura exacta de 36143 filas; hashes y allowlists de paquetes; cero validaciones declaradas.` |
| 2.10 | Lo que NO hace | PASA | «no fusionar»: el merge lo hizo `Josanoforo` (mesa). «no tocar replay-evidencia / productores / sellos / decisiones / catálogo / CI / manifiesto» → 0 archivos (2.3). «no simular COINCIDE»: `estado` = `NO-EVALUADO` en 36 143/36 143; `--ejecuta` y el comparador no se corrieron (`prueba-primer-lanzamiento.json`: `sesion_validadora: NO-LANZADA, recalculos: 0`). «no copiar microdatos»: miembros de los 68 contenedores por extensión → `.md` 136, `.tsv` 68, `.json` 272; ningún raw. |
| 2.11 | NO-CORRIDO vs encargo | PASA | P1 universo → `universo.tsv` + `corte.json`. P2 → 9 DISPONIBLE; los 59 restantes con fila `NC-…-6c30-01` (DIFERIDO-A:SIN-ASIGNAR) en el encargo, en la nota y en `forense/no-corrido.tsv`. P3 → `lanzamientos.md` con 68 filas numeradas (una por paquete), lanzador y comparador (no ejecutado). P4 → `NO-EVALUADO` total, orden de lotes, orden de revelación. Recibo → `NC-…-6c30-02`. |

### Filtración de valores esperados (compuerta «paquete sin resultados ni código productor»)

Re-derivado aquí, no heredado del verificador de Astra:
- Nombres de miembro con `medidor|resultados.json|sello|ejecucion|.py|report|catalogo|esperad` → **0 de 476**.
- Valores del catálogo al corte con ≥ 4 decimales (`punto`, `ic95_inf`, `ic95_sup`; 107 854 valores distintos) que aparecen dentro de algún miembro → **0 de 476**.
- `estimandos.tsv` del lote 1 trae `llave … unidad naturaleza_ic`, sin columnas de punto ni IC.
- Tolerancias: `tolerancia.json` del lote 1 (`flotante, abs 1e-10`) = `data/corrida0/CALC-ENDIREH-PISOS-2021-COMUNITARIA-0001/spec.yaml:156-159`. Es preexistente, no inventada. Distribución en los 68 paquetes: 1e-10 ×50, 1e-06 ×4, texto ×8, determinista ×3, 1e-15 ×3.
- `metodo.md` del lote 1 es una «extracción fiel de especificación humana» con procedencia en `preparacion/procedencia-metodos.json`, que no se entrega.

## 2-bis · REVISA-CALC

NO-APLICA: el diff no toca `data/corrida0/CALC-*/`, `forense/prereg-caja/`, vistas de corrida ni citas `corrida0_*` (2.3). Las «referencias de adopción» (36) se leen, no se escriben.

## Contra la ADENDA-1 §C1 (criterios del recibo GEN2-RECIBO-ASTRA6-N)

Solo lo que esta preparación puede cumplir. La validación ciega es del sucesor.
- Paquete archivado antes de entregarse: sí, 68 contenedores con sha en `lotes.json` y un `manifiesto.json` interno. **No hay `.sha256` junto al paquete**: el hash vive en `lotes.json`, lo que es equivalente en función. Ninguna sesión ciega se lanzó todavía, así que el orden paquete → sesión ciega queda por verificar en el PR del sucesor.
- Contenido: sin `medidor.py`, sin `resultados.json`, sin valores (arriba). Rótulo del sucesor condicionado por R2.
- Estados: los 36 143 en `NO-EVALUADO`, y el PR **no** lo presenta como validación. Correcto.
- Sellos y adopciones: 0 archivos tocados; `replay-evidencia.tsv` sin asiento (correcto: no hay validación real).
- Sesión de diseño ≠ sesión ciega: declarado en `metodo.md`/`encargo.md` del paquete («El preparador conoce resultados; no ejecuta esta reconstrucción»).

CONTADOR: cero mediciones, declarado (infraestructura).

## Qué NO revisó este pase

- La fidelidad de las 68 extracciones de método contra sus specs humanas, más allá del lote 1 y de la búsqueda de valores. Leerlas una por una es trabajo del recibo por lote.
- La causa exacta de cada `faltantes.json` de los 59 INCOMPLETO. Se re-derivó el conteo, no su mérito.
- `astra6_compara_catalogo.py`: se leyó el contrato en `lanzamientos.md:86-90`, no se ejercitó (no existe ninguna reconstrucción contra la cual correrlo).
- La prueba `--prueba` del lote 1 corrió en `/home/pc0/…` (caja). Aquí es `REPORTADO` (`prueba-primer-lanzamiento.json`), no re-ejecutada.

Este informe no aprueba, no fusiona y no empuja nada. Fusionar es firmar, y firmar es de mesa.
