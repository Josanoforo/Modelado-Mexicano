# ENCARGO · ACTO EVAL-COMPARTAMOS-LLAVE3 — el primer renglón de la clase (iii)

- **Redactado por:** dirección, 24/ago/2026.
- **Firma que ejecuta (D2, verbatim al ADR):** *«Valor propio, GO, pero asegurándonos que el motor lo soporta y que va ligado a lo que queremos construir.»*
- **Entorno asignado:** **UBUNTU** (abre el zip del corpus). No nube. Modelo Opus. Sin `--freeze`.
- **Estado:** `CONSUMIDO` — 25/ago/2026. Produce el quinto valor del censo de diseño (`DISENO_EXPERIMENTAL`, con criterio propio dentro del yaml), la apertura a nivel de columna de `analysis_data_AEJ_pub.dta`, la fila `EXP-COMPARTAMOS-1` del registro de llaves, `FP-123` `FIRMADA`+ejecutada, `FP-131`/`FP-132` nuevas, `ADR-162`, recifrado de estado y `forense/notas/2026-08-25-eval-compartamos.md`.
- **CONTADOR DECLARADO: cero directo** (v2.3) — la llave nace `SELLADA_NO_EJERCIDA`; ejercerla es acto posterior. Cumplido: el numerador de llaves ejercidas no se movió (`3`); subió el denominador (`3` → `4`).

---

## Texto completo tal como se lanzó

ENTORNO: UBUNTU (abre el zip del corpus). NO NUBE. · Modelo: Opus · 🚫 `--freeze` · `pgrep -af claude` · `iconv`

ORDEN: Cola UBUNTU, tras lo que esté corriendo (ADQ-CORRE-R74R75 / R34-CONDA-V2 si ya cargaron).

CONTADOR: Cero directo — crea el renglón de la llave clase (iii) `SELLADA_NO_EJERCIDA`; ejercerla es acto posterior. Declarado (v2.3).

ARRANQUE: 1 · REPO: clon existente. 2 · SHA: el main del momento; refresca y reporta. 3 · `data/raw`: enlaza al corpus; NO descarga. 4 · ENTORNO tres partes (A.2): sin_variable · sonda INEGI · `ls data/raw/` (vacío = PARO). ⚠️ [v2.11] A.13 en todo negativo. 5 · ESPEJO: nada.

VERIFICACIÓN DE EXISTENCIA (dirección): El paquete EXISTE en corpus: openicpsr `116334-V1.zip` (Compartamos AEJ, RCT de expansión de microcrédito), abierto por RECENSO-2 solo a nivel de archivos — `analysis_data_AEJ_pub.dta` sin abrir a columna (FP-123, textual). La clase de llave EXISTE y espera: ADR-57(c) verbatim — *"(iii) diseño experimental de terceros (evaluaciones aleatorizadas publicadas, clase Progresa/Oportunidades), usado como evidencia (a) con su cita"* — y el registro (`forense/registro-llaves-identificacion-v1_0.md`) no tiene ningún renglón de esa clase (re-derívalo con grep y pega el conteo). El vocabulario del censo tiene 4 valores, ninguno experimental (FP-123).

TAREAS:

1. **Valor propio en el censo** (`data/diseno-muestral.yaml`): añade `DISENO_EXPERIMENTAL` con criterio propio documentado en el propio yaml — campos que una fila experimental debe llenar: unidad y nivel de aleatorización, brazos (T/C), variable de asignación en los datos, cumplimiento/atrición si el paquete los reporta, y cita de la publicación. Aplícalo a la fila del paquete, llenándola desde los documentos del zip (readme/codebook del replication package), con cita archivo-dentro-del-zip por dato. FP-123 → FIRMADA+ejecutada con el verbatim D2.

2. **Abre `analysis_data_AEJ_pub.dta` a nivel de columna** (nombres + etiquetas): confirma que la variable de asignación T/C existe y nómbrala; confirma unidad de análisis y N; ningún efecto se estima aquí — es censo de identificación, no medición.

3. **El renglón de la llave (iii):** crea en el registro de llaves la fila `CAL-EXP-1` (o el id que la convención del archivo mande — derívala) · clase (iii) citando ADR-57(c) verbatim · objeto: expansión de microcrédito Compartamos · estado `SELLADA_NO_EJERCIDA` · qué falta para ejercerla: spec B-bis que declare qué θ/generador del modelo informa.

4. **El amarre al motor que mesa exigió, en dos mitades:** (a) a qué necesidad/θ liga — cruza contra `data/curacion-registro/necesidad-objeto-modelo.tsv` (terna del curador) y contra los generadores de crédito/riesgo del modelo v4.0; escribe el mapeo con archivo:línea, o NO-ENCONTRADO con universo si ninguna necesidad lo nombra (eso también es hallazgo: evidencia causal de primera sin consumidor declarado). (b) dónde la consumiría el motor — deriva si `milpa/procedencia.yaml` / el contrato de celdas / refutations tienen clase para "evidencia (a) con cita" experimental de terceros; si el hook no existe, PROPUESTA mínima escrita en la nota, sin implementar, y fila de tablero para mesa (A.12). No improvises esquema en `milpa/`.

5. **Cierre:** nota `2026-08-25-eval-compartamos.md` con párrafo a mesa (qué se puede ejercer con esto y qué falta) · filas A.12 · ADR (candidatea re-derivado; renumera si colisiona) · recifrado estándar · suite VERDE con tail · encargo CONSUMIDO.

PERÍMETRO: `data/diseno-muestral.yaml` · `forense/registro-llaves-identificacion-v1_0.md` · `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` · `forense/notas/2026-08-25-eval-compartamos.md` · `forense/encargos/2026-08-25-EVAL-COMPARTAMOS-LLAVE3.md` · scratchpad. NO toca `milpa/`. Fuera de la lista: PARA. Concurrencia: NUBE/ChatGPT en paralelo permitido; renumera quien fusiona segundo.

---

## Lo que este acto hizo, verificado contra el propio encargo

1. **Tarea 1 — cumplida.** `DISENO_EXPERIMENTAL` entra al vocabulario de `data/diseno-muestral.yaml` con su criterio de **cinco campos obligatorios** escrito dentro del propio archivo (no en la nota, no en el ADR), más la regla de que los tres campos heredados se escriben `no aplica — experimento` **con razón**, nunca vacíos. La fila del paquete pasa de `PENDIENTE` a `DISENO_EXPERIMENTAL` con los cinco campos llenos, cada dato con su cita archivo-dentro-del-zip. `FP-123` → `FIRMADA` con el verbatim D2 en `firmada_en` y `ejecutada_en` lleno el mismo día.
   - **Corrección de premisa, menor y material:** el encargo dice *"llenándola desde los documentos del zip (readme/codebook del replication package)"*. **El paquete no trae codebook** — su `Readme.pdf` remite a un *Data Appendix* que no viene dentro del zip — y **tampoco trae la cita bibliográfica** (barrido sobre los 98 archivos, cero coincidencias). Los cinco campos se llenaron igual: cuatro desde los do-files y el microdato, y el quinto (`cita_publicacion`) desde `data/mapa-ext-academico-2026-08-06.tsv:4`, declarando en el propio campo que la cita **no** sale del zip.
2. **Tarea 2 — cumplida.** 124 variables, 21,523 filas, nombres y etiquetas. Variable de asignación: **`Treatment`** (ola de seguimiento) y **`BTreatment`** (línea base), las dos constantes dentro de su conglomerado (0 de 238 y 0 de 34 con más de un valor). Unidad de análisis: **persona** (mujer 18-60), una fila por persona-encuesta. **N = 16,560** en seguimiento. Cero efectos estimados; ni siquiera la toma de tratamiento por brazo.
3. **Tarea 3 — cumplida, con el id derivado y distinto del propuesto.** El encargo autorizaba derivarlo. La convención del archivo nombra **el objeto del modelo al que la llave sirve**, y el prefijo `CAL-` es de la familia de calibración de un coeficiente nombrado — que aquí no existe (ver Tarea 4a). Id derivado: **`EXP-COMPARTAMOS-1`**. Nace `SELLADA_NO_EJERCIDA`, clase (iii) con `ADR-57(c)` verbatim, `preregistro_ref` = NINGUNO y "qué falta para ejercerla" escrito en la propia fila. Conteo previo de la clase re-derivado y pegado (§10 del registro): **`0`** — el `1` del patrón ingenuo es la mención que `R5.1-D2` hace de la (iii) para descartarla.
4. **Tarea 4 — cumplida, y las dos mitades dan negativo.** (a) **NO-ENCONTRADO** sobre el universo completo declarado (`A.13`): 0 de 37 filas de `necesidad-objeto-modelo.tsv`, con control positivo en el mismo comando; hallazgo lateral: la terna no cubre `dinero.credito.baja_friccion_usura_dano_downstream`. (b) **El conducto no existe** en ninguna de las tres piezas (7 clases de procedencia, 7 valores de `diseno_datos` del contrato de celda-D, 3 tipos de refutación), y sin embargo el motor ya cita `Progresa_RCT` dos veces sin clase que lo marque. Propuesta mínima escrita en §7.1 de la nota, **no implementada**; `milpa/` sin tocar. `FP-131` y `FP-132`, las dos `ABIERTA`.
5. **Tarea 5 — cumplida.** Nota con párrafo a mesa (§8), tres filas de tablero (`FP-123` firmada, `FP-131`/`FP-132` nuevas), `ADR-162` candidateado y renumerado tres veces por concurrencia, recifrado de `canon/estado-programa-v1_10.md` (ADR `161`→`162`; llaves `3 de 3`→`3 de 4`; WARN `145`→`146`), suite `--baseline` **19 FAIL · 146 WARN · LÍNEA BASE VERDE** con tail, y este encargo `CONSUMIDO`.

**Perímetro respetado.** No se tocó `milpa/`, ni el contrato de celda-D, ni `canon/modelo-decision-v4_0.md`, ni `data/mapa-ext-academico-2026-08-06.tsv`, ni `data/curacion-registro/necesidad-objeto-modelo.tsv`, ni `tests/`. Las dos correcciones que este acto encontró en tablas ajenas (250 vs 238 conglomerados; la regla `dinero.credito.*` sin necesidad) quedan **declaradas y no ejecutadas**, por estar fuera de la lista.

**Concurrencia — la regla del encargo se aplicó tres veces.** `origin/main` se movió tres veces mientras este acto estaba abierto: `21ab042` → `e8ce5ef` (`PR #327`, que trajo `ADR-159`), → `e70b424` (`PR #328`, `ACTO R34-CONDA-V2`, que se llevó `ADR-160` **y** las filas `FP-129`/`FP-130`) y → `a5f1bf6` (`PR #329`, `ACTO BANDAS-DOC-6`, que se llevó el `ADR-161` recién asignado). Las tres se absorbieron rebasando antes de cerrar; este acto quedó en `ADR-162`, `FP-131` y `FP-132` — *renumera quien fusiona segundo*, con el máximo re-derivado por `grep` sobre el árbol fusionado cada vez. Los archivos en colisión se resolvieron **por unión**, sin perder ni sobrescribir ninguna entrada ajena, verificado contra `origin/main`; incluye la corrección de una pasada de renumeración que tocó por error referencias ajenas dentro de líneas compartidas (detalle en §9 de la nota).
