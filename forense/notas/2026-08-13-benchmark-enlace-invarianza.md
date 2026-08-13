# ACTO BENCHMARK-ENLACE — colapsabilidad e invarianza, con literatura

*13 de agosto de 2026. Entorno NUBE con búsqueda web, declarado por el propio encargo. Perímetro: `forense/benchmark-enlace-invarianza-v1_0.md` (nuevo) · esta nota · el encargo archivado (A.3) · `forense/hallazgos.md` (append). NO toca `canon/**`, `milpa/procedencia.yaml`, ningún dato.*

---

## 0 · Arranque (Bloque D) — verificado antes de escribir

1. **Repo.** Clon existente en `/home/user/Modelado-Mexicano`, no se clonó uno nuevo. `git log -1` inicial: `19d885d Merge pull request #200...`. `git status` limpio.
2. **SHA.** `git fetch origin main` → `origin/main` había avanzado a `b7aa67c` (PR #205), la rama de este acto seguía en `19d885d` (PR #200, el estado al crearla). **Main sí se movió — no es PARO.** `git diff --stat 19d885d..b7aa67c` acotado a `canon/`, `forense/`, `milpa/`, `data/curacion-registro/celdas-d/`: siete archivos, todos de dos actos ajenos — `ENCARGO B · ALIAS-P + MOTOR-DIAG` (`ADR-73`, mantenimiento de `tools/curador_registro/via_capa2.py`) y `ENCARGO VERIFICA-PUERTAS`. Ninguno de los dos toca `canon/modelo-decision-v4_0.md`, `milpa/procedencia.yaml`, `forense/BENCHMARKS-metodologicos-D-ABC.md` ni la celda-D de `radio_confianza` — grep dirigido de `colaps|invarian|D-ABC|radio_confianza` sobre el diff, cero coincidencias sustantivas (solo el cambio mecánico de conteo de ADR, 72→73, en las cabeceras de `gobernanza`/`estado-programa`). Se fusionó (`git merge origin/main`, fast-forward limpio) antes de escribir ningún archivo de este acto. Este documento y el resto del acto se redactan contra **`b7aa67c`**.
3. **data/raw.** Ausente (`ls data/raw` → no existe). Este acto no abre microdato — no PARO, previsto por PERÍMETRO ("ningún dato").
4. **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → `cloud_default`. Sonda `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` → `000`, `curl` exit 56 (conexión rechazada). Firma coherente con acto de nube sin ruta a datos públicos mexicanos, ya documentada en este repo (`instrucciones-proyecto-v2_6.md` Bloque D-bis A.2; ADR-59(b)) — no hace falta ejecutarla porque este acto no toca microdato ni red de datos, se corrió de todos modos por completitud y el resultado es el esperado, no un hallazgo.
5. **Espejo.** No se usó. Toda cifra de esta nota y del benchmark sale del clon de este worktree (archivo:línea citado) o de `WebSearch` con su URL a la vista.
6. **Concurrencia.** `git branch -r`: `origin/main`, `origin/claude/benchmark-enlace-invarianza-mojhke` (esta rama). Ningún otro worktree/rama tocando `forense/BENCHMARKS-metodologicos-D-ABC.md`, `canon/gobernanza-v1_15.md`, `milpa/procedencia.yaml` o la celda-D de `radio_confianza` — verificado por el diffstat de §2, no hay PR abierto que los edite.

---

## 1 · Qué se leyó del repo antes de escribir las preguntas (procedencia tipo 1)

Lista de archivos leídos completos o por sección dirigida, cada uno con lo que aportó:

- `forense/BENCHMARKS-metodologicos-D-ABC.md` — el documento que la Pregunta 1 pide verificar. Cabecera propia: recuperado del espejo el 11/ago/2026 (commit `2cf3e28`, "RECUPERACION M0: cinco archivos del espejo del proyecto sobre D-ABC"), procedencia tipo (2), contenido no editable. Se auto-declara tipo (3) en su bibliografía ("ninguna cita se ha leído en su fuente original").
- `canon/gobernanza-v1_15.md` — texto completo de `ADR-64` (línea ~ver nota m5) y `ADR-67` (a)-(d) (líneas 862-872), más la cita de `ADR-65` sobre `D-ABC` sin sellar (línea 832).
- `milpa/procedencia.yaml` — cabecera de `coeficientes_generador_medidos` (líneas 648-658, la nota de escala que resume el problema de `D-ABC` en una frase) y las entradas `G1_radio_confianza` (660-708, incluida `eje_condicionante` con el recuento corregido por ADR-61) y `G1_confianza_institucional` (709-722+); líneas 780/812 (la cita "ningún ADR de D-ABC ha sellado función de enlace").
- `canon/modelo-decision-v4_0.md` §2.2 (líneas 382-398) — tabla de los quince coeficientes `ASIGNADO` y el tratamiento de `G1a`.
- `data/curacion-registro/celdas-d/G5.radio_confianza.encuci_vs_enbiare.yaml` — completo. Trae el estado operativo de las 8 producciones de ENBIARE, la cita literal de `ADR-67(a)` sobre invarianza parcial, y el desacople de universos ENCUCI/ENBIARE (`poblacion_objetivo`, líneas 31-39).
- `forense/notas/2026-08-05-m5-adr64-conf06.md` — completo. Las cinco cláusulas de `ADR-64`, verificadas contra `README.md:91` y `C-06b`.
- `forense/notas/2026-08-04-x-condicionamiento-y-forma.md` — completo, incluida la sección §11 (un *rider* del mismo día que **corrige el titular de §6** sin editarlo: para `radio_confianza` específicamente, "todavía no se puede decir" si la inversión de signo es real o efecto de cobertura parcial del universo por eje — detalle en Commit 2, Pregunta 2).
- `forense/auditoria_adversarial_benchmarks.md` (RT-A) y `forense/CAREO-benchmarks-4RT-archivo-proyecto.md` — la auditoría adversarial que ya corrió sobre §2 de `BENCHMARKS-metodologicos-D-ABC.md` (no la pidió este encargo, se encontró explorando el perímetro; ignorarla habría violado la propia regla de oro). Veredicto resumido en Commit 2.
- `canon/estado-programa-v1_10.md` §S5 (líneas 136-143) — confirma que ni `D-ABC` ni "D4"/"D10" en el sentido de este acto tienen casillero ahí.
- `canon/glosario-v5_6.md` — grep de "colapsable", "invarianza de medición", "ítems ancla", "función de enlace", "D-ABC": cero entradas en las cinco. Se anota como hallazgo menor en Commit 2, no se corrige (fuera de perímetro, es `canon/`).
- `instrucciones-proyecto-v2_6.md` — Bloque A-bis regla 3 (escalas no se comparan sin enlace) y regla 2 (condicionar puede acercar o alejar del estimando — "nada más"), ambas centrales para la Pregunta 2.

Un hallazgo de contexto adicional, leído completo y citado en Commit 2 porque responde directamente a la Pregunta 4/5 con más profundidad que cualquier búsqueda nueva de esta sesión: `forense/EDGE-CASES-y-literatura-reciente.md` §E5 (recuperado del espejo el mismo commit `2cf3e28`) ya investigó, el 5/ago/2026, si la invarianza de medición clásica es requisito para comparar ENCUCI contra ENCIG (un par análogo, no idéntico, al de esta pregunta) y encontró literatura de 2023-2025 que disputa activamente si la invarianza es necesaria o suficiente. Se verificó independientemente contra fuente en esta sesión (Commit 2, Pregunta 4) — no se heredó tal cual.

---

## 2 · Metodología de la búsqueda web (Commit 2)

`WebFetch` se intentó contra ocho hosts académicos (`stat.ubc.ca`, `pubmed.ncbi.nlm.nih.gov`, `projecteuclid.org`, `ajconline.org`, `ehsanx.github.io`, `ncbi.nlm.nih.gov`, `semanticscholar.org`, `en.wikipedia.org`) para leer directamente el texto de Greenland-Robins-Pearl (1999) y de las fuentes secundarias que lo discuten. Los ocho devolvieron `EGRESS_BLOCKED` — límite del entorno de esta sesión (proxy de egreso), no ausencia de la fuente; por la regla A.5 de `instrucciones-proyecto-v2_6.md` ("el fallo de un agente es un hecho sobre el agente, no sobre la fuente"), se declara así y no se escribe ninguna variante de "no existe" o "no disponible" sobre esas fuentes.

Toda la literatura de este benchmark se verificó, en cambio, con `WebSearch` — que sí completó, devolviendo extractos con URL real de cada resultado (journals, PubMed, ResearchGate, arXiv, sitios de editorial). Cada claim de literatura en Commit 2 se corroboró contra ≥2 resultados de búsqueda independientes donde fue posible, marcados **(3+)** cuando ≥2 fuentes que citan o discuten directamente el artículo primario convergen (mejor que una sola cadena de cita, corto de haber abierto el PDF). Consultas ejecutadas (lista completa, sin omitir las que no aportaron): Greenland-Robins-Pearl 1999 localización y resumen; colapsabilidad RD/RR/OR/HR definición; noncollapsibility sin confusión; condiciones de colapsabilidad de la diferencia de riesgos; Meredith 1993; Vandenberg-Lance 2000; Putnick-Bornstein 2016; Byrne-Shavelson-Muthén 1989; ítems ancla y DIF; invarianza sin ítems/muestra común; anchoring vignettes King-Wand; armonización ex-post Fortier/Maelstrom; ENCUCI/ENBIARE/INEGI confianza interpersonal y comparabilidad metodológica; OECD Guidelines on Measuring Trust; Robitzsch-Lüdtke 2023; Raykov 2024; Kusano-Napier-Jost 2025; alignment method Asparouhov-Muthén 2014.

---

## 3 · Correcciones mecánicas encontradas al cerrar (declaradas, no escondidas)

`python3 tests/check.py --baseline` corrido después de escribir Commit 1 dio **ROJO, 5 entradas nuevas**: `T02` (el nombre normalizado de `forense/encargos/2026-08-13-benchmark-enlace-invarianza.md` colisionaba con el de esta nota — mismo defecto de construcción que `convencion.md` ya documenta, "un encargo y una nota con el mismo tema y sin prefijo colisionan por construcción"), `T03` (dos citas a `` `x-condicionamiento-y-forma.md` `` en el benchmark sin el prefijo de fecha, que `T03` no resuelve contra el archivo real) y tres mensajes de `T16` derivados de esos dos (el conteo real de FAIL/WARN se movió, así que las cifras que `canon/estado-programa-v1_10.md`/`canon/gobernanza-v1_15.md` declaran como vigentes dejaron de coincidir mientras las dos fallas de arriba estuvieran presentes). Corregido antes de Commit 2: el encargo se renombró con prefijo de código (`2026-08-13-BE-benchmark-enlace-invarianza.md`, mismo mecanismo que ya usó `ACTO APERTURA-ISSP` el mismo día para el mismo defecto de clase) y las dos citas ganaron su prefijo de fecha completo. Re-corrido: **`18 FAIL · 105 WARN`, LÍNEA BASE: VERDE** — nada nuevo frente a `tests/baseline.json` (`948ad70`), sin necesidad de tocar `canon/`.

## 4 · Cierre

**Contadores movidos: 0.** Este acto no mide ninguna condicional ni coeficiente del motor, no toca `canon/**` ni `milpa/procedencia.yaml` — produce literatura verificada e insumo para que mesa selle `D-ABC` y diseñe el acto de vinculación ENCUCI↔ENBIARE, ninguno de los dos sellado aquí. `git status --short` antes de Commit 2: solo `forense/benchmark-enlace-invarianza-v1_0.md` (extendido con la sección "COMMIT 2"), esta nota (extendida con §3-§4) y `forense/hallazgos.md` (append) — verificado, nada fuera del perímetro declarado.

*Esta nota no se edita hacia atrás; lo que cambió entre commits se agregó como sección nueva (§2-§4), §0-§1 quedan como se escribieron en Commit 1.*
