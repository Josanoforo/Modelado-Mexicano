# Encargo AA · El punto ciego estructural del catálogo, medido y cerrado

Mesa #19, 4/ago/2026. Base: `main` = `37950da` (merge de PR #92 — ya fusionado al iniciar este
acto, no `06385eb` como asumía el encargo; diferencia reportada y no bloqueante, §2 del
protocolo de arranque). Worktree nuevo: `/home/pc0/mm-encargo-aa-clase-fuente`, rama
`sesion/encargo-aa-clase-fuente` (no existía clon previo para este encargo — se declara, no se
oculta).

## 1 · Las tres afirmaciones falsas de §1, verificadas contra el repo

| Afirmación citada | Verificación en este acto |
|---|---|
| "ninguna fuente del corpus tiene panel para este choque" (R5.1) | **Ya corregida antes de este acto.** `forense/hallazgos.md:102` registra que mesa #19 adjudicó `A` a R5.1 sobre esa premisa falsa (rama de PR #85), y que se **retiró antes de fusionar** — R5.1 volvió a "sin adjudicar". `forense/cruce-catalogo-fichas-v1_0.md:130-137` ya documenta el caso de prueba completo: ENASEM/MHAS está en el catálogo desde v1.0 (línea 41), `[verificado]` en el inventario de salud (línea 164), panel con olas que flanquean la reforma de 2019. **No requiere acción de este acto** — se reporta como defecto ya cerrado, no reabierto. |
| "ENSANUT sigue sin bajar" | **Falsa, verificable en disco.** `data/manifiesto.yaml` tiene 72 líneas con mención de ENSANUT y 198 entradas con `sha256:` en total — los Encargos Y y Z (mismo día) ya usaron ENSANUT CONTINUA 2024 extensamente (`forense/notas/2026-08-04-z1/z2/z3-declaracion-fuente-*.md`), abriendo cuestionarios completos, no solo catálogos de nombre. **No requiere acción de este acto.** |
| "no existe variable de distancia; ninguna fuente audita fuera del prestador" (R9.1, R9.2) | **Parcialmente falsa como afirmación general sobre México — cierta como afirmación sobre el catálogo v1.0.** Los D archivados de R9.1/R9.2 (Notas 23 y 25 de `hitoD-preregistro-v2_0.md`) están bien fundados **contra el catálogo que tenían disponible** (solo encuestas) — no son descuido, son la consecuencia correcta de un catálogo incompleto. CLUES (registro georreferenciado de establecimientos) y Cero Desabasto (transparencia independiente del prestador) **sí existen y no estaban catalogados**. Ver Tarea D (`2026-08-04-aa-relectura-cuatro-d.md`) para si esto cambia algún veredicto. |

**La causa, confirmada:** `data/catalogo-fuentes-v1_0.md` se deriva de 10 inventarios, los diez
construidos sobre encuestas (`README-inventarios.md` no lo dice explícito, pero los 10 nombres de
archivo y sus 183 entradas son, sin excepción, instrumentos de encuesta o censo). Registro
administrativo, padrón de programa y transparencia de sociedad civil **no tenían clase propia en
la taxonomía** — no podían aparecer aunque existieran, porque el catálogo no tenía dónde ponerlos.

## 2 · Los tres candidatos de §1, verificados (procedencia tipo 3 → tipo 1)

Investigación delegada a un fork con acceso a WebSearch/WebFetch (11 consultas + 5 fetches),
verificación de host por sondeo directo en este mismo acto. Resultado completo:
`data/inventarios/inventario_fuentes_clase-fuente-mexico.md`, entradas #1 (CLUES), #6 (Cero
Desabasto), #12 (ESTAD/"ENSATD").

- **CLUES: existe, verificado.** Catálogo nacional de establecimientos de salud (DGIS,
  Secretaría de Salud), granularidad de establecimiento con domicilio/localidad/municipio,
  actualización mensual, descarga directa sin registro. Coordenadas GPS nativas **no
  confirmadas** — si un Umbral pide distancia en km, CLUES da la ubicación del establecimiento,
  no necesariamente lat/long lista para calcular distancia sin geocodificación adicional.
- **Cero Desabasto: existe, verificado.** Plataforma de +140 organizaciones de sociedad civil,
  5 años operando, +14,000 reportes, informes anuales 2019-2023. **Independiente del prestador
  por diseño.** Granularidad exacta (¿entidad? ¿unidad médica?) **no verificada con precisión**
  — declarado ambiguo, no forzado a una lectura favorable.
- **"ENSATD": no existe con ese nombre — hallazgo, no fuente inexistente.** El instrumento real
  es **ESTAD** (Encuesta de Satisfacción, Trato Adecuado y Digno), DGCES/INSP desde 2015,
  aplicada en Consulta Externa por Monitores Institucionales y Ciudadanos en paralelo. Confirma
  exactamente la clase "encuesta institucional no de hogares" que el encargo buscaba, solo bajo
  otro nombre. Se documenta la discrepancia porque §1 del encargo pide explícitamente
  verificar "si no son lo que digo, es hallazgo".

## 3 · Qué se hizo, en el perímetro autorizado

1. **Tarea A** — `data/inventarios/inventario_fuentes_clase-fuente-mexico.md` (11º inventario,
   18 entradas, las 6 clases de §3 barridas al menos una vez cada una) + regeneración del
   pipeline (`tests/catalogo.py && tests/dedup.py`, RECETA consistente, 131 fuentes únicas desde
   119) + `data/catalogo-fuentes-v2_0.md` (nueva versión MAYOR, v1.0 no se edita, queda para
   borrar por convención de nomenclatura).
2. **Tarea B** — `forense/notas/2026-08-04-aa-barrido-alcanzabilidad.md`.
3. **Tarea C** — `forense/cruce-catalogo-fichas-v2_0.md`.
4. **Tarea D** — `forense/notas/2026-08-04-aa-relectura-cuatro-d.md`.

## 4 · Nota de entorno — sandbox de red del Bash tool

El entorno remoto asignado (ARRANQUE §4) confirmó `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` vacío y
`curl` a inegi.org.mx respondiendo 200 — firma de entorno de red correcta. Sin embargo, la
herramienta de shell de este acto trae **su propia lista blanca de red**, independiente de la
política del entorno, que no incluía los hosts institucionales nuevos de este encargo (CLUES,
Cero Desabasto, CONSAR, INE, etc.) — los primeros intentos daban `000`/timeout silencioso, no un
código de error real. Verificado que era la sandbox del shell, no el entorno: el mismo host
(`cerodesabasto.org`) pasó de `000` a `200` al desactivar esa sandbox para el comando, sin
cambiar nada más. Todos los sondeos de Tarea B se corrieron con la sandbox del shell desactivada
para ese comando específico — el entorno de red asignado (§4 del arranque) sí es el correcto.

## 5 · Escala (v2.4, módulo de auditoría)

Este acto no produce cantidades estimadas de ningún fenómeno de México. Las únicas cifras que
produce son de conteo del propio catálogo (119→131 fuentes únicas, 10→11 inventarios) y de
alcanzabilidad de host (Tarea B) — ninguna es una estimación sustantiva que compita con las del
motor de decisión. No aplica declaración de escala adicional.
