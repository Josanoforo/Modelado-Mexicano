# RECIBO · GEN2-RECIBO-ASTRA-1 · seis CALC de Astra (PR #1030 ENCIG, PR #1031 ENVIPE)

SHA base al abrir el acto: `619748f5` (origin/main, coincide con lo declarado). Ramas fijadas: `codex/astra-encig-1` @ `ccebbf74` (PR #1030), `codex/astra-interaccion-dinamica-1` @ `159dc874` (PR #1031). Ninguna de las dos toca `data/corrida0/marcador-segmento.tsv`, `canon/`, `forense/decisiones.tsv` ni celdas-D (`git diff --stat origin/main...<rama> -- forense/decisiones.tsv canon data/corrida0/celdas-D` → vacío en ambas).

## Hallazgo que gobierna el recibo (P2/(b), pregunta (i) de la cabecera)

`git log --oneline origin/acto/gen2-celda-d-piloto-4-encogida-1` muestra que el piloto 4 **ya corrió su COMMIT-1** (`5939e9d COMMIT-1: codigo y D-22 congelados, PILOTO-4-ENCOGIDA-1`), y `git merge-base --is-ancestor 5939e9d origin/main` → NO — ese COMMIT-1 vive solo en la rama del piloto, no en `origin/main`; tampoco lo está PR #1031. La ADENDA-1 (`forense/encargos/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-ADENDA-1.md`, sellada 20:08) dice verbatim: «Se admite un candidato adicional `C-ASTRA` en COMMIT-1 **si al abrir el acto existe en `origin/main`** un CALC … sellado». Al momento en que el piloto 4 abrió y congeló su COMMIT-1, ni `CALC-ASTRA-ENVIPE-*` ni `CALC-ASTRA-ENCIG-*` estaban en `origin/main` (siguen sin estarlo). El propio PR #1031 lo admite en su cuerpo: «Esta rama aún no está en main… Permanece EN-RAMA hasta observar una fusión a main anterior al COMMIT-2 … La sesión autora no fusionará el PR» — y el "mandato posterior" que citaba un plazo distinto («antes de COMMIT-2») es `[REPORTADO]` por Astra, no la firma sellada; **manda la adenda** (recomendación de dirección, §35 del encargo, adoptada aquí).

**Conclusión de (b) para ENVIPE: NO-ENTRA por timing — la ventana de admisión ya cerró.** No es un juicio sobre la calidad del candidato: aunque los cuatro CALC de PR #1031 cumplieran (a) y (c) letra por letra, la condición temporal de la ADENDA-1 ya no puede satisfacerse porque el COMMIT-1 del piloto 4 ya está sellado sin ellos. Responde también la pregunta (i) de la cabecera sin necesidad de que mesa elija entre las dos fechas: bajo cualquiera de las dos («al abrir» o «antes de COMMIT-2»), hoy PR #1031 no está en `main`, así que el resultado práctico es el mismo NO-ENTRA mientras mesa no lo funda ANTES de que el piloto llegue a su COMMIT-2.

## P1 · Etiquetas y asiento (los seis)

| CALC | cuenta_gen2 | adopta | origen_numerico | sello.json/.sha256 | replay-evidencia |
|---|---|---|---|---|---|
| CALC-ASTRA-ENCIG-EDADXSEXO-0001 | SI | 'NO' | MICRODATO | presentes | REPRODUCE / IDENTICO (40/40 RESULT, 3/3 inputs) |
| CALC-ASTRA-ENCIG-ESCOLARIDADXSEXO-0001 | SI | 'NO' | MICRODATO | presentes | REPRODUCE / IDENTICO (40/40 RESULT, 3/3 inputs) |
| CALC-ASTRA-ENVIPE-EDADXSEXO-0001 | SI | 'NO' | MICRODATO | presentes | REPRODUCE / IDENTICO (34/34 RESULT, 3/3 inputs) |
| CALC-ASTRA-ENVIPE-ESCOLARIDADPROXYXSEXO-0001 | SI | 'NO' | MICRODATO | presentes | REPRODUCE / IDENTICO (34/34 RESULT, 3/3 inputs) |
| CALC-ASTRA-ENVIPE-DOMINIOXSEXO-0001 | SI | 'NO' | MICRODATO | presentes | REPRODUCE / IDENTICO (26/26 RESULT, 3/3 inputs) |
| CALC-ASTRA-ENVIPE-EDADXESCOLARIDADPROXY-0001 | SI | 'NO' | MICRODATO | presentes | REPRODUCE / IDENTICO (66/66 RESULT, 3/3 inputs) |

Los seis traen las tres etiquetas coherentes con «candidato externo, no adopta» y fila en `forense/replay-evidencia.tsv` (E.7) con `resultado_replay=REPRODUCE`, `contexto_replay=IDENTICO`. **P1 satisfecho por forma en los seis.**

## P2 · Orden spec→dato y olas (criterio b)

- **ENCIG (PR #1030).** `spec.yaml` de ambos CALC declara `exposicion_historica: CIEGO-A-ENCIG2025-CRUCE-NO-ABIERTO` y `inputs` con `origen: repo` — no microdato: `historico_2021`/`historico_2023` apuntan a `resultados.json` de CALC ya sellados (`CALC-ENCIG2021/2023-CRUCES-HISTORICOS-000x`), y `marginales_publicos_2025` apunta a `milpa/tramite-ola5-propuesta-v0.yaml`, un archivo de **propuesta** que el motor no carga (según su propia cabecera) y que ya vive en `origin/main` con el mismo sha256 declarado (`93dfa3f9…` verificado con `git show origin/main:milpa/tramite-ola5-propuesta-v0.yaml | sha256sum`). Ningún input es un tabulado o comunicado de una ola reservada — no aplica el PARO (a) de §7. `ejecucion.json` confirma `input_ids` idénticos a los del `spec.yaml`, congelados en `044c3f32` (mismo commit citado por PR #1030 como freeze) antes de correr.
- **ENVIPE (PR #1031).** `input_ids` = `envipe2023_csv`, `envipe2024_csv`, `MARGINALES-PUBLICOS`; los dos primeros SÍ están en `data/manifiesto.yaml` por id (líneas 309 y 323) — **no** verificables por sha aquí porque el acto es NUBE sin corpus montado (`ls data/raw` vacío); el propio PR declara `envipe2023_csv=0dcc00a7…`, `envipe2024_csv=90776b2f…`. `MARGINALES-PUBLICOS` no resuelve por id exacto contra `manifiesto.yaml` desde este acto — **NO-VERIFICABLE-AQUÍ** (NC, abajo). El PR se autodeclara `RETROSPECTIVA-MECÁNICA`/prospectiva condicional y dice explícitamente «no se abrió ningún cruce 2025 ni R»; no hay contradicción visible en el diff (`git diff --stat` no toca ninguna ruta de microdato 2025/2026).
- El punto que decide el veredicto de ENVIPE no es (b)-contenido sino (b)-ventana: ver hallazgo que gobierna, arriba.

## P3 · Celdas (criterio a) y forma (criterio c)

- **ENCIG.** `data/corrida0/marcador-segmento.tsv` trae, para ENCIG 2025, exactamente los dos ejes que emite Astra: `CRUCE-GRUPO::tramite.gobierno_digital.util_sin_coercion_ejes_encig2025::edadxsexo` y `::escolaridadxsexo`, ambas `RESERVADA` / `EMITIDA-SIN-EVALUAR` / `EMITIDA-SIN-R` (líneas 209-210). El dominio sustantivo coincide: la fila registra `adopta_encig2025_luz` (canal internet/cajero para trámite de luz) y el `estimando` de `CALC-ASTRA-ENCIG-EDADXSEXO-0001` es «Proporción de trámites de pago ordinario de luz con canal internet o cajero/kiosco inteligente» — mismo objeto. **El piloto 5 (`GEN2-CELDA-D-PILOTO-5-ENCOGIDA-ENCIG-1`) no está lanzado** (no existe rama ni encargo con ese rótulo: `git ls-remote --heads origin | grep -i piloto-5` → vacío), así que el veredicto es condicional: **ENTRARÍA si el piloto 5 pide estas celdas**, tal como exige el encargo. Unidad declarada en el marcador: trámite (no persona) — el CALC de Astra reporta "proporción" sobre trámites, consistente; no se detecta promedio cruzado de unidades (§4).
- **ENVIPE.** No aplica: el veredicto ya es NO-ENTRA por (b)-ventana, así que (a)/(c) quedan sin adjudicar contra la spec del piloto 4 — el cotejo detallado celda-por-celda contra `TRA-evade-norma-cruces-encogida-spec-v1_0.md` no se hizo (ver NC). Astra mismo declara en el PR #1031 «edad × dominio (NC-0328) y escolaridad × dominio quedan excluidas» — es decir, ni siquiera Astra afirma cobertura completa de la lista del piloto.
- Los seis `spec.yaml` declaran punto, IC (límite inferior/superior 95%), nivel y tipo de intervalo por celda (`unidad: proporción` / `límite inferior 95%` / `límite superior 95%` / `nivel` / `tipo de intervalo` en cada bloque de variable) — **(c) satisfecho por forma en los seis**.

## P4 · Veredicto y recomendación

| CALC | (a) | (b) | (c) | etiquetas | asiento | veredicto |
|---|---|---|---|---|---|---|
| CALC-ASTRA-ENCIG-EDADXSEXO-0001 | coincide (condicional a piloto 5) | sin ola reservada abierta | declarado | completas | REPRODUCE | **ENTRARÍA-CONDICIONAL** (piloto 5 aún no existe) |
| CALC-ASTRA-ENCIG-ESCOLARIDADXSEXO-0001 | coincide (condicional a piloto 5) | sin ola reservada abierta | declarado | completas | REPRODUCE | **ENTRARÍA-CONDICIONAL** |
| CALC-ASTRA-ENVIPE-EDADXSEXO-0001 | no adjudicado | **ventana cerrada** | declarado | completas | REPRODUCE | **NO-ENTRA** (piloto 4) |
| CALC-ASTRA-ENVIPE-ESCOLARIDADPROXYXSEXO-0001 | no adjudicado | **ventana cerrada** | declarado | completas | REPRODUCE | **NO-ENTRA** |
| CALC-ASTRA-ENVIPE-DOMINIOXSEXO-0001 | no adjudicado | **ventana cerrada** | declarado | completas | REPRODUCE | **NO-ENTRA** |
| CALC-ASTRA-ENVIPE-EDADXESCOLARIDADPROXY-0001 | no adjudicado | **ventana cerrada** | declarado | completas | REPRODUCE | **NO-ENTRA** |

**Recomendación de fusión por PR:**
- **PR #1030 (ENCIG) → FUSIONAR-CON-NC.** Forma completa, sin ola reservada abierta, candidato condicional legítimo para un piloto 5 que aún no existe; el NC es que este recibo no corrió el cotejo celda-por-celda contra una spec de piloto 5 que no existe todavía (no puede existir).
- **PR #1031 (ENVIPE) → NO-FUSIONAR por ahora**, no por defecto de Astra sino porque el candidato ya no tiene ventana de admisión al piloto 4 (COMMIT-1 sellado sin él) y el piloto 5 de ENVIPE no es el que este encargo evalúa. Mesa puede fusionar el PR como documentación histórica (`C-ASTRA-2026` para un duelo posterior, tal como el propio PR se autodescribe) sin que eso adopte ni mida nada — decisión de mesa, no de este acto.

Pregunta (ii) de la cabecera (etiqueta faltante → ¿FUSIONAR-CON-NC o devolver?) no aplicó: los seis traen las tres etiquetas completas.

## NO-CORRIDO / RESERVAS

Ver `## NO-CORRIDO / RESERVAS` en el propio encargo archivado (añadida por /acto) y filas `NC-*` en `forense/no-corrido.tsv`.
