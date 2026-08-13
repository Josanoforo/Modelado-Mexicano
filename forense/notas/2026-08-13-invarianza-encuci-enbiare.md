# ENCARGO 9 · Invarianza ENCUCI↔ENBIARE — acto de vinculación, no rediseño

### 13/ago/2026 · redactado contra `origin/main` = `1cb6e3e` (PR #219/TRIAGE-63) · Entorno CAJA con corpus, NO nube · worktree `mm-invarianza-encuci-enbiare`

**Qué es.** El acto de vinculación-invarianza que `ADR-67(a)` exige y que `ADR-76(d)` diseñó (Propuesta 2 de `forense/benchmark-enlace-invarianza-v1_0.md`), ejecutado — no rediseñado. Adjudica si ENCUCI (`AP5_1_1`/`AP5_1_2`) y ENBIARE (`PB1_01`/`PB1_02`) son suficientemente convergentes para desbloquear las 8 producciones de `radio_confianza` hoy en `NO_LISTA_DECISION_HUMANA_PENDIENTE` (`produccion-modelo.tsv`, verificado en este acto: 8 filas, `objeto_modelo_origen=G5.radio_confianza`, `requiere_decision=SI` — cuenta exacta, no heredada).

**Qué NO es.** No rediseña el acto (`ADR-76(d)` ya lo selló). No sella `ADR-79` en `canon/gobernanza-v1_15.md` (fuera de perímetro de este acto — el borrador vive en la conversación de dirección de esta sesión, listo para que un acto con `canon/` en perímetro lo incorpore). No toca `AP5_1_3` (declarado fuera de alcance, per Propuesta 2 punto 2). No dicotomiza para el test mismo (usa 0-10 ordinal completo, per Propuesta 2 punto 3 — la dicotomización ≥8/10 es solo para comparación externa, si la hubiera).

**Estándar de éxito, sellado en esta conversación (`ADR-79`, borrador — ver `forense/hallazgos.md` de este mismo acto):** argumento de vinculación declarado (anclas de diseño OCDE 2017 + invarianza parcial hasta donde el par de dos ítems identifique + juicio experto rotulado como tal) — no invarianza clásica completa, que `ADR-76(d)` ya calificó inalcanzable hoy (sin muestra puente, sin ítems ancla verificados estadísticamente, ENCUCI 2020/ENBIARE 2021 sin panel compartido).

---

## COMMIT 1 · Especificación congelada, antes de abrir microdato

*Este commit fija el procedimiento completo y la regla de reporte antes de que este acto calcule un solo número sobre `AP5_1_1`, `AP5_1_2`, `PB1_01` o `PB1_02`. El primer resultado que produzca este procedimiento, corrido una sola vez, es el que se reporta en COMMIT 2 — ese commit no reescribe esta sección para que cuadre mejor con lo que salga.*

### 1. Universo y datos

- **ENCUCI 2020**: `SEC_4_5` (dentro de `BD_ENCUCI2020_dbf.zip`, `data/raw/`), ítems `AP5_1_1` (confianza en "la mayoría de las personas") / `AP5_1_2` (personas que conoce), escala 0-10. Ponderador `FAC_SEL`, diseño `EST_DIS`/`UPM_DIS` — nombres ya verificados contra archivo en actos previos citados por la celda-D (`forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md`), no re-derivados de memoria pero tampoco re-abiertos en este commit.
- **ENBIARE 2021**: `TENBIARE.csv` (dentro de `enbiare_2021_base_de_datos_csv.zip`, `data/raw/`), ítems `PB1_01`/`PB1_02`, escala 0-10. **Ponderador y variables de diseño de ENBIARE se verifican contra el diccionario/CSV real en COMMIT 2, antes de calcular — no se asumen por analogía de nombre con ENCUCI** (ENCUCI y ENBIARE son instrumentos de INEGI distintos; nada garantiza que compartan convención de nombre de columna de diseño).
- Casos sin respuesta válida en el ítem (missing / no sabe / no responde, según diccionario de cada instrumento) se excluyen listwise del par correspondiente — mismo criterio de `n` útil por ítem que el resto del programa ya aplica (ver `universo_instrumento` de la celda-D, que declara `n` distinto por ítem en ENCUCI).
- `AP5_1_3` (vecinos): fuera de alcance, no se calcula nada sobre él en este acto — declarado, no silenciado (Propuesta 2 punto 2).

### 2. Estadístico y procedimiento

Con dos ítems por instrumento y sin muestra puente, la secuencia configural→métrica→escalar clásica (AFC multigrupo) no es ejecutable (`ADR-76(d)`). Lo que sí se puede calcular, declarado aquí antes de calcularlo:

1. **Configural** (por instrumento, por separado): correlación de Pearson ponderada `r12` entre los dos ítems ancla, en la escala 0-10 completa. Punto de estimación: `r_w = Σw(x-x̄w)(y-ȳw) / sqrt(Σw(x-x̄w)² · Σw(y-ȳw)²)`, con `x̄w`/`ȳw` medias ponderadas. Intervalo: bootstrap de conglomerado último, **2000 réplicas, semilla fija `20260813`**, resample de UPM con reemplazo *dentro de cada estrato* (mismo conglomerado que valida `tests/svystat.py`, extendido aquí a una correlación en vez de una proporción — extensión declarada, no heredada de ese archivo, y no se edita ese archivo: el cálculo vive en un script efímero fuera del repo, documentado línea por línea en COMMIT 2).
   - **CONFIGURAL SOSTENIDA** en ese instrumento si `r12 > 0` y el IC95% excluye 0.
   - **CONFIGURAL NO SOSTENIDA** si el IC95% incluye 0, o `r12 ≤ 0`.
2. **Métrica** (tau-equivalente — única identificación posible con 2 indicadores sin ítems ancla externos): `λ = sqrt(r12)` por instrumento, definida solo si `r12 > 0`. Se compara `λ_ENCUCI − λ_ENBIARE` vía la misma familia de réplicas bootstrap (independientes entre instrumentos, por ser muestras independientes sin panel).
   - **MÉTRICA SOSTENIDA** si el IC95% de la diferencia incluye 0.
   - **MÉTRICA NO SOSTENIDA** si el IC95% excluye 0.
   - **MÉTRICA NO EVALUABLE** si `λ` no está definida en algún instrumento (configural ya no sostenida ahí).
3. Ninguna comparación de este paso dicotomiza. Si en algún punto se compara una cifra contra corpus/literatura externa (no contra el otro instrumento), se usa corte único `≥8/10` en ambos lados (`ADR-64`) — nunca el `≥6/10` interno del motor, y nunca mezclado con el test de arriba.

### 3. Reserva A-bis — invarianza parcial es un estado con nombre

Tres desenlaces posibles, nombrados aquí, ninguno forzado a los otros dos:

- **INVARIANZA SOSTENIDA** — configural y métrica sostenidas en ambos instrumentos.
- **INVARIANZA PARCIAL** — configural sostenida en ambos instrumentos, métrica no sostenida (o no evaluable). Se declara explícitamente sobre qué parámetro se sostiene (configural) y sobre cuál no (métrica) — no se resume como "parcial" sin decir cuál.
- **INVARIANZA RECHAZADA** — configural no sostenida en al menos un instrumento.

### 4. B-bis — qué significa NO RECHAZAR invarianza (obligatorio, declarado antes de correr)

`NO RECHAZAR` = desenlace `INVARIANZA SOSTENIDA` o `INVARIANZA PARCIAL`. Es, por diseño del acto (`ADR-76(d)` ya calificó invarianza clásica completa inalcanzable, y configural con 2 ítems es una barra baja), **el desenlace más probable** — declarado antes de correr, no después de ver el número.

Bajo el estándar sellado en esta conversación (`ADR-79`, argumento de vinculación declarado), **NO RECHAZAR** significa:

- Las 8 producciones de `radio_confianza` (`produccion-modelo.tsv`, `objeto_modelo_origen=G5.radio_confianza`) pasan de `estado_uso_modelo=NO_LISTA_DECISION_HUMANA_PENDIENTE` / `requiere_decision=SI` a `estado_uso_modelo=LISTA_PARA_USO_MODELO` / `requiere_decision=NO`.
- La celda-D (`G5.radio_confianza.encuci_vs_enbiare.yaml`) registra `criterio_adjudicacion.escala` con el resultado (SOSTENIDA/PARCIAL y sobre qué parámetros), `candidatos[CHALLENGER].resultado` deja de ser `NO-EJECUTADO`, `fecha_adjudicacion`/`commit_adjudicacion` se llenan.
- **Lo que NO significa**: no promueve `ENBIARE` a `champion_actual` ni le da poder de sustitución sobre `ENCUCI` — `champion_actual` se mantiene `BASELINE.ENCUCI` y la clase `PROXY_PARCIAL` de `ADR-67(a)` no cambia aquí; este acto adjudica *convergencia de instrumentos para desbloquear el gate*, no superioridad de uno sobre otro. Tampoco resuelve la reserva de `AP5_1_3` (queda fuera de alcance, sin adjudicar). Tampoco mueve ningún contador de canon (`13 de 27`, `9 de 14`, `0 de 15`, etc.) — el contador que este acto instituye es, exclusivamente, el gate de las 8 producciones de `radio_confianza`.

Si el desenlace es **INVARIANZA RECHAZADA**: las 8 producciones NO se desbloquean, el gate de `ADR-67(a)` permanece exactamente como está, y este commit 1 ya declaró que ese desenlace era el menos probable — se reporta igual, sin forzarlo hacia el otro lado.

### 5. Promesa de primer resultado

El primer número que produzca el procedimiento del §2, corrido una sola vez con la semilla `20260813`, es el que se reporta en COMMIT 2. Si el script tiene un error de ejecución (no de resultado — p. ej. una columna mal referenciada, un `KeyError`), se corrige el error y se vuelve a correr; si el script corre sin error y produce un número, ese número no se descarta buscando otro.

*Cierra COMMIT 1. Los resultados viven exclusivamente en la sección "COMMIT 2" de abajo, en un commit de git separado que no edita esta sección.*

---

## COMMIT 2 · Resultados

*(pendiente — se escribe después de correr el procedimiento del COMMIT 1, en un commit separado)*
