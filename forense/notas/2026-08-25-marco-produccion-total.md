# ACTO MARCO-PRODUCCIÓN-TOTAL — 253 → marco elegible → PARO en congelado

**Cierre.** 25/ago/2026 · Base `12fd435` (main, `#349` fusionado, coincide con la referencia de mesa) · Encargo: "ACTO · MARCO-PRODUCCIÓN-TOTAL · 253 → MARCO ELEGIBLE → CONGELADO → SORTEO".

## 0 · Arranque

```
git fetch origin && git switch main && git pull --ff-only
git log -1 --oneline   →  12fd435 Merge pull request #349 ...
```

`origin/main` no había avanzado más allá de la referencia de mesa (`12fd435fdb30e31428a76fb00aa2e36996874b93`). `#349` está cerrado (fusionado, no reabierto).

Estado consolidado, re-verificado contra `data/curacion-universo/diagnostico-autoridad-semantica-marco-v1_0.json`: 129,845 semillas, 128,995 procedencia exacta final, 850 no reconciliadas, 253 candidatas, 195 BINARIA/58 CATEGORICA, ENIF 2024=115, ENASIC 2022=27, ENUT 2024=85, MOCIBA 2024=26, 39 identidades conflictivas fuera. Coincide exactamente con la cifra de mesa. No se tocó `AUTORIDAD-SEMANTICA-MARCO` ni las 129,845 semillas.

## FASE 1 · Materialización de las 253 en 18 columnas

`python3 tools/curador_registro/generar_marco.py --indice-e2 .barrido2/private/e2-neutral-index.jsonl` corrido dos veces: **253 candidatas, 254 filas con cabecera, exactamente 18 columnas, TSV idéntico byte a byte** entre corridas (`sha256 2260daf0...`), y **coincide con la corrida al cierre de `#349`** (misma `sha256`). Cero autoridades huérfanas, cero specs conflictivas reentradas (el generador ya excluye las 39 vía `CONFLICTO_IDENTIDAD_CONCEPTUAL`, verificado en el diagnóstico).

Artefacto: `data/curacion-universo/marco-produccion-total-v1_0.tsv` (253 filas + cabecera, 18 columnas contractuales, sin cambio de contrato).

## FASE 2-6 · Enriquecimiento en bloque — qué resuelve regla, qué no

### `grado_dependencia` — RESUELTO para las 253, por regla determinista existente

Regla vigente, verbatim de `forense/notas/2026-08-20-act-pil-2-marco.md` §"`grado_dependencia`, derivado y no tecleado": **P0** = el par `(encuesta, ola)` aparece en `milpa/procedencia.yaml` como ruta de parametrización de M; **P1** = misma familia nombrada, otra ola o sin ola; **P2** = el resto.

Aplicada mecánicamente contra `milpa/procedencia.yaml` (no releída de memoria, `git grep` verbatim):

- `ENIF 2024` cita 4 veces como fuente de parametrización directa (`condicionales_confianza_institucional.financiera`, `familismo_apoyo`, `dinero.ahorro.volatilidad_horizonte_corto`, más `G1/RUTA-A`) → **P0**.
- `ENASIC 2022` cita 3 veces (`P7_12_7` para `norma_de_género`, `P6_38` para `obligación_medida`) → **P0**.
- `ENUT` se nombra como familia (sin "2024" exacto), y explícitamente como **proxy histórico ya no vigente** (`norma_de_género`, corregido por `ACTO PROC-11`/ADR-67(b)) → **P1** (familia nombrada sin ola exacta, la regla no exige vigencia).
- `MOCIBA` no aparece en `milpa/procedencia.yaml` bajo ningún nombre → **P2**.

Resultado: **P0 = 142** (ENIF 2024 + ENASIC 2022) · **P1 = 85** (ENUT 2024) · **P2 = 26** (MOCIBA 2024). Suma 253, verificado.

### `publicada`, `cv_arbitro`, `n_no_ponderado`, `frase_discriminacion`, `post_corte_u_ola_retenida`, `dominio`, `dificultad`, `estrato` — NO resueltos en este acto

No son PENDIENTE genérico: cada uno tiene una razón material específica, ya documentada por el propio programa al construir el único precedente comparable (el marco piloto de 60 filas, `ACT-PIL-2`/`ADR-130`, `forense/marco-candidatas-piloto-v1_0.tsv`):

1. **`publicada` (filtro (i) de `ADV1-M1`).** La receta sellada exige "prueba del bibliotecario": abrir el sitio de INEGI en **navegador**, pestaña Tabulados que arma JavaScript, y buscar el cuadro que cruce la variable con su eje de condicionamiento — un minuto por celda, verificado y citado (archivo, hoja, fila, cifra). `www.inegi.org.mx` es una SPA con soft-404 (`200` para cualquier ruta, incluso inexistente — verificado de nuevo en este acto: `curl -s -o /dev/null -w "%{http_code}" https://www.inegi.org.mx/programas/xxxxx-no-existe-jamas/9999/` → `200`), así que no es automatizable por `curl`/API. El único precedente real (`BIBLIOTECARIO-56`) tardó un acto completo dedicado para **56** filas: 922 archivos descargados y validados por contenido, 3,806 libros, 46,645 hojas leídas. Extrapolar esa misma labor a **253** filas (4.5× el precedente) es exactamente la clase de trabajo que el encargo prohíbe fabricar por atajo ("no hagas búsquedas web abiertas caso por caso salvo que el contrato vigente explícitamente lo requiera" — y aquí el contrato vigente **sí** lo requiere caso por caso, así que la única vía honesta es no simular el resultado). **No se inventó ninguna clasificación SI/NO.**
2. **`cv_arbitro` y `n_no_ponderado` (filtro (iii)).** Documentado verbatim en la nota de `ACT-PIL-2` §"El CV del árbitro no existe antes de que exista el árbitro": no existe en el repo un árbitro genérico que compute CV/n sobre una celda arbitraria del marco. El mecanismo que sí existe (`prepare_production.py`/`produce.py`, confirmado en este acto por lectura directa) exige una especificación `ESP-OPACA` autorada a mano **por θ individual**, el mismo régimen que produjo cada entrada de `milpa/procedencia.yaml` (un acto, un ADR, por variable). Aplicarlo a 253 filas no es una corrida de script: son hasta 253 actos de la misma envergadura que `ACTO COND-ATRIB` o `PROD-P638`. La fuente oficial de precisión de ENASIC 2022 (re-verificada en este acto) tiene 2 filas con dato de 337 — el filtro no lo cubre ni la fuente oficial. **No se calculó ningún CV ni n.**
3. **`frase_discriminacion`.** Exige prosa que distinga el mecanismo `M` de un rival `L` **por variable**, con juicio semántico sobre el contenido sustantivo de cada reactivo — el encargo mismo prohíbe automatizarlo por regex. Sin ese juicio por variable no hay frase honesta que escribir 253 veces.
4. **`post_corte_u_ola_retenida`.** Depende lógicamente de (i) y (iii): la regla sellada de `ACT-PIL-2` ("(ii) gana sobre (v)... post_corte pasa a NO en toda fila P0") solo resuelve el caso P0; para P1/P2 el resto de la regla nunca se completó porque dependía de si la ola se usó como fuente publicada, que es exactamente el filtro (i) sin resolver.
5. **`dominio`, `dificultad`, `estrato`.** En el único precedente, estas tres columnas se asignaron por **clasificación sustantiva de cada variable** (seis "tandas" temáticas ejecutadas por revisión humana/Sonnet supervisado, más auditoría fila por fila), no por una función determinista de `encuesta`/`ola` — la misma encuesta (p. ej. ENIF) aparece en más de un dominio del precedente según el contenido específico del reactivo. No hay regla mecánica en el repo que las derive de las columnas ya materializadas; clasificar 253 variables sustantivamente está fuera de lo que este acto puede producir sin fabricar el juicio.

**Ninguno de estos ocho campos se rellenó con un valor plausible.** Cada fila del artefacto de adjudicación lleva la razón exacta en su propia columna (`PENDIENTE-BIBLIOTECARIO`, `PENDIENTE-ARBITRO-INEXISTENTE`, `PENDIENTE-JUICIO-SEMANTICO-POR-VARIABLE`, etc.), no un `PENDIENTE` desnudo.

## FASE 7 · Tabla de adjudicación

`data/curacion-universo/adjudicacion-marco-produccion-total-v1_0.tsv` — 253 filas, una por candidata, con las 18 columnas contractuales origen, `grado_dependencia` resuelto + evidencia, y el resto de los filtros con su razón material. **Ninguna fila queda en una bolsa "pendiente de revisar" sin nombre**: las 253 llevan el mismo veredicto (ver Fase 9) porque los dos filtros que determinan elegibilidad (publicada, cv) no se resolvieron para ninguna.

## FASE 8 · Marco elegible

No se puede producir un marco elegible real (ELEGIBLE/EXCLUIDA por fila) sin resolver primero `publicada` y `cv_arbitro`: son, junto con `n_no_ponderado`, los filtros que la propia `ADV1-M1` usa para decidir elegibilidad. Reportar "elegibles por dominio/dificultad/estrato/CV" sería fabricar una distribución sobre columnas que no existen todavía. Se reporta en su lugar el conteo de entrada (253) y la razón exacta por la que ninguna puede adjudicarse todavía a ELEGIBLE o EXCLUIDA.

Comparación contra las 60 filas históricas (solo para entender qué cambió, sin forzar la cifra): la población de 60 es una **población distinta**, construida a mano bajo `ADV1-M1`/`ACT-PIL-2`/`ADR-130` para el piloto; la de 253 nace de `AUTORIDAD-SEMANTICA-MARCO` (índice-E2 privado real). No comparten identidad `(encuesta,ola,variable)` como universo de entrada — la de 60 no se deriva del generador de índice-E2. Fusionarlas o hacer que 253 quepa en 60 fabricaría una relación que no existe.

## FASE 9 · Decisión de congelado — PARO

Las reglas vigentes de suficiencia/congelado (`ADV1-M1`) exigen los cinco filtros resueltos. Dos de cinco — (i) publicada, (iii) CV/n — no lo están, por razón material documentada arriba, no por omisión. **No se congela.**

**PARO_MESA: filtros (i) y (iii) de `ADV1-M1` no resueltos para las 253 candidatas.** Falta exactamente: (i) verificación manual del bibliotecario en navegador contra `inegi.org.mx` para cada una de las 253 filas (el precedente costó un acto completo para 56); (iii) un árbitro genérico de CV/n que hoy no existe en el repo, o 253 especificaciones `ESP-OPACA` individuales por el motor formal existente. Ninguno de los dos es producible dentro de este acto sin fabricar el resultado.

## FASE 10 · Sorteo — no ejecutable en este acto, por diseño

Además de depender del congelado (Fase 9, no cumplido), el propio procedimiento de sorteo escrito en `ACT-PIL-2` (`forense/notas/2026-08-20-act-pil-2-marco.md` §6, script `sorteo.py`, no corrido) fija la semilla como **el SHA de 40 hex del commit de *merge* del PR que congela el marco** — un objeto que, por construcción, no existe hasta después de que ese PR se fusione. Este acto entrega un PR que **no se mergea** (instrucción explícita), así que la semilla no puede existir todavía aunque el marco se congelara. El sorteo no es postergable por descuido: es estructuralmente posterior a la fusión, nunca ejecutable dentro del mismo PR que la propone.

## FASE 11 · Propagación

No aplica: no hay marco congelado ni sorteo ejecutado que vuelva falso ningún estado operativo existente. No se tocó `estado-programa` ni se abrió ADR (no hay decisión normativa nueva; `grado_dependencia` aplicó una regla ya sellada, no creó una).

## Verificación

- `generar_marco.py` corrido dos veces: 253 candidatas, 254 filas, 18 columnas, TSV idéntico byte a byte, y coincide con el cierre de `#349`.
- `grado_dependencia`: 142+85+26 = 253, regla determinista citada arriba, reproducible por comando (`git grep` contra `milpa/procedencia.yaml`).
- `python3 -m unittest` de los tests dirigidos de `autoridad_semantica_productiva`/`marco`/`primary_metadata_projectors`/`marco_e2_adapter`: sin cambios de código en este acto, no hay defecto material que corregir — no se tocaron.
- `python3 tests/check.py --baseline`: VERDE, sin nuevas entradas.
- `git diff --check`: limpio.
- No hay sorteo que repetir (Fase 10 no ejecutada).

## Perímetro respetado

No se reabrió `AUTORIDAD-SEMANTICA-MARCO` ni las 129,845 semillas. No se tocaron los proyectores SAV/DTA/XLS/XLSX. No se tocó scoring, duelo, `BARRIDO-2`, privacidad. No se congeló nada por inercia de la cifra histórica de 60. No se declaró saturación.
