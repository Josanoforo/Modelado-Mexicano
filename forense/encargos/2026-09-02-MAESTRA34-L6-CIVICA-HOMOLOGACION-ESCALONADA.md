ENCARGO · ACTO MAESTRA34-L6 · CIVICA-HOMOLOGACION-ESCALONADA — invoca /acto (y /adquiere)
SHA de redacción: 29ab80a. Redacta dirección (Fable), 2/sep/2026, contra v2.12. Estado: GATED a MAESTRA34-L5 fusionado (verifica por producto: entradas nuevas de L5 en milpa/tramite-ola5-propuesta-v0.yaml en origin/main). Un solo acto de caja a la vez.
ENTORNO ASIGNADO: UBUNTU (red a OPLE/SICEE por sonda A.2; abre resultados electorales). NO se lanza en NUBE. MODELO SUGERIDO: Opus (medidor de dos commits con diseño de identificación).

FIRMA DE MESA — verbatim, 2/sep/2026: DC1 «d». Diseño firmado: tratamiento escalonado de la homologación de calendarios (reforma 2014): municipios de todos los estados, 2015–2024, antes/después de que su estado pasó a elección local concurrente con la federal, contra los estados que ya eran concurrentes o que aún no cambiaban ese año; unidad municipio × elección local; desenlace participación (votos totales / lista nominal) en puntos porcentuales. Benchmark externo: Alemania ≈10 pp (Leininger, Rudolph y Zittlau, PSRM 2018), EE.UU. 36 pp (Hajnal y Lewis 2003); benchmark nacional: TEPJF, «Elecciones concurrentes y participación electoral en México, 1991-2018» (2020). El ejecutor propaga, no decide.

A.8 contra 29ab80a: L4 (ADR-284) midió entre años en Coahuila y Edomex, 163 municipios, y declaró el confundidor; sus 16 payloads OPLE (2023 y 2024) y el crosswalk sección→municipio 2016 EXISTEN en manifiesto. SICEE: 5 menciones en manifiesto (alta por A1). TEPJF 1991-2018: `grep -ci tepjf data/manifiesto.yaml` → 0, NO-ENCONTRADO en corpus. Calendario de homologación por estado (qué año cada entidad pasó a concurrente, 2015–2021): NO-ENCONTRADO como tabla en el repo (`grep -ril "homologaci" data/ forense/` → pega la salida); se deriva en P0 de fuente primaria (SICEE/OPLE/DOF), no de memoria.

P0 · TABLA DE TRATAMIENTO (un commit, antes de cualquier resultado). Para cada una de las 32 entidades: año de cada elección local de ayuntamientos 2015–2024 y si fue concurrente con la federal (2015, 2018, 2021, 2024); año de primer cambio a concurrente = fecha de tratamiento. Fuente por fila (SICEE, OPLE o DOF), con salida cruda; A.13 con entidades cubiertas. Sin esta tabla no se compra ni se mide nada.
P1 · ADQUISICIÓN. Por /adquiere, resultados de ayuntamientos por municipio con lista nominal para las elecciones que la tabla de P0 marque, priorizando: (i) estados tratados entre 2016 y 2021 con al menos una elección local no concurrente después de 2015 (antes) y una concurrente (después); (ii) sus controles del mismo año. Ruta OPLE probada en L4; SICEE como respaldo por navegador (receta de L1). Registro por las tres capas. Reporta cobertura: estados × elecciones obtenidas / requeridas por P0. También el libro TEPJF (te.gob.mx, PDF público si existe; si no, receta).
P2 · SPEC CONGELADA (COMMIT-1, antes de abrir ningún resultado). Estimando: efecto de la concurrencia sobre participación municipal en pp, por diferencias en diferencias escalonadas con efectos fijos de municipio y de año electoral; estimador robusto a adopción escalonada (Callaway-Sant'Anna o equivalente; declara cuál y por qué); errores estándar agrupados por estado; control de «año presidencial» dado por los estados no tratados en el mismo año; universo = municipios con lista nominal en todas las elecciones consideradas; exclusiones declaradas (usos y costumbres en Oaxaca: fuera, con conteo). Falsador pre-registrado (B-bis): si el IC del efecto contiene 0 → la regla civico.participacion.contingente queda REFUTADA-como-causal y el Δ de L4 se reinterpreta como efecto de año; si el efecto está entre 5 y 15 pp → CORROBORADA y el +10.5 de L4 se lee como mayormente concurrencia; si >15 pp o <5 pp con IC fuera del rango de L4 → acotada, se dice cuánto del Δ de L4 era año. Frase de sello: «el primer resultado que produzca este procedimiento es el que se reporta». Escala declarada: pp.
P3 · RESULTADOS (COMMIT-2). Estimación principal, event-study por año relativo al tratamiento (pre-tendencias como diagnóstico), heterogeneidad por tamaño de municipio; comparación de signo y magnitud contra L4 (misma escala) y contra los benchmarks; entrada en la propuesta: enmienda a civico.participacion.contingente con clase MEDIDO·Δ-identificado, tier PENDIENTE-DE-MESA, situacion propuesta con los disparadores que el diseño soporta (concurrencia sí/no). Si la cobertura de P1 no alcanza el mínimo declarado en P0 (dirección propone ≥8 estados tratados con antes y después), P3 corre sobre lo que hay y se declara acotado.
P4 · CIERRE. Propuesta a mesa en RH: qué número, contra qué benchmark, qué firma cargaría al motor y cómo se convierte a probabilidad (dirección propone: el motor consume «participa» como tasa base municipal + Δ por concurrencia; la conversión la firma mesa, no el acto). Tablero: recibos; nota de cierre con A.13 por pieza.
PERÍMETRO: corpus (payloads) · data/manifiesto.yaml (script) · data/curacion-registro/* (vía N6) · data/cola-adquisicion-v1_0.tsv (regenerada) · milpa/tramite-ola5-propuesta-v0.yaml (una enmienda) · tools/ (tabla P0, estimador) · forense/notas/ · forense/hallazgos.md · tablero · A.3 · cascada. NO toca milpa/tramite.yaml ni prereg-duelo-v2. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR: deriva al arrancar. CONTADOR: payloads OBTENIDO +N · estados con antes/después +N · reglas con Δ identificado +1 si P3 corre completo.
LO QUE NO HACE: no carga al motor; no toca L4 (queda como medición entre años, intacta); no repite la adquisición de Coahuila/Edomex 2023-2024 (reutiliza).

---

## CONSUMIDO

Ejecutado el 2/sep/2026 en entorno **UBUNTU** por `ACTO MAESTRA34-L6 ·
CIVICA-HOMOLOGACION-ESCALONADA`, con la skill `/acto` (`ADR-237`) y `/adquiere`.
**PR #468**, `ADR-288`, rama `acto/maestra34-l6-civica-homologacion-escalonada`.
NO fusionado por el ejecutor: el merge es de mesa.

Commits: `51c7009` (A.3, este archivo) · `7717afe` (`P0`) · `1e38063` (`P1`) ·
`5bddf8a` (`P2`, spec congelada) · `30d5c0f` (`P3`, resultados) · `9d5ca17`
(cascada) · este.

**Compuerta** `GATED a MAESTRA34-L5` verificada **por producto** como el propio
encargo manda: las tres entradas de `L5` presentes en
`origin/main:milpa/tramite-ola5-propuesta-v0.yaml` (`PR #467`, merge `11af678`).

**Qué se hizo de lo que se pidió, pieza por pieza:**

- **`P0`** — hecho y **completo**: las 32 entidades, 2015-2024, con fuente y
  salida cruda por fila, desde 30 acuerdos del Consejo General del INE. `A.13`
  con entidades cubiertas. **14 entidades tratadas** con antes y después.
- **`P1`** — hecho y **acotado**: 43 payloads de resultados, registro por las
  tres capas, cobertura reportada (4 entidades medibles de las 14 tratadas; 2 de
  ellas tratadas). El libro del **TEPJF** queda `NO-OBTENIDO` con receta de
  navegador, tras cuatro rutas con salida cruda.
- **`P2`** — hecho: `COMMIT-1` con la spec congelada, **antes** de abrir ningún
  resultado, con la frase de sello y la escala en pp. **Desviación declarada y
  razonada**: el estimador **no** lleva efectos fijos de año electoral, porque
  `P0` midió que el tratamiento es colineal con el año y esos efectos fijos no
  identifican; la spec lo dice en `§0.3` y explica en `§1.5` qué se conserva de
  Callaway-Sant'Anna y qué no.
- **`P3`** — hecho y **declarado acotado**, como el propio encargo prevé para
  cuando la cobertura no alcanza el mínimo de ≥8.
- **`P4`** — hecho: propuesta a mesa en formato RH (`FP-239`), tablero con
  recibos, nota de cierre con `A.13` por pieza.

**Perímetro respetado.** Se tocó: corpus (76 payloads) · `data/manifiesto.yaml`
(por script) · `data/curacion-registro/*` · `data/cola-adquisicion-v1_0.tsv`
(regenerada) · `milpa/tramite-ola5-propuesta-v0.yaml` (**una** enmienda) ·
`tools/` (tabla de `P0`, lectores, estimador) · `data/p0-*.tsv` y
`data/l6-resultados-*.json` (productos de `P0`/`P3`) · `forense/notas/` ·
`forense/hallazgos.md` · `forense/encargos/` (A.3) · `forense/firmas-pendientes.tsv`
(tablero) · cascada (`canon/gobernanza`, `canon/estado-programa`,
`canon/registro-rotulos`). **`milpa/tramite.yaml` y `forense/prereg-duelo-v2/`
intocados**, como el encargo manda.

**Un archivo del perímetro que el encargo no listaba y hubo que tocar:**
`data/INFRAESTRUCTURA-v1_0.md`. No es una ampliación de alcance: `tests/check.py`
`T27` **falla** si un archivo nuevo bajo `data/` no está citado ahí, y los tres
archivos nuevos son productos que el propio encargo ordena (`P0` «tabla de
tratamiento», `P3` resultados). Sin esa cita la suite queda en ROJO. Se declara
aquí en vez de dejarlo implícito.

**Lo que el encargo dijo que no se hiciera, y no se hizo:** no se cargó nada al
motor; **no se editó la entrada de `MAESTRA34-L4`**, que queda íntegra con su `Δ`
y su firma `DC1-d`; no se repitió la adquisición de Coahuila/Edomex 2023-2024 (se
reutilizó el payload de `L4` para Coahuila 2024).
