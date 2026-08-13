# ENCARGO 9 · Invarianza ENCUCI↔ENBIARE — acto de vinculación, no rediseño

### 13/ago/2026 · redactado contra `origin/main` = `1cb6e3e` (PR #219/TRIAGE-63) · Entorno CAJA con corpus, NO nube · worktree `mm-invarianza-encuci-enbiare`

**Qué es.** El acto de vinculación-invarianza que `ADR-67(a)` exige y que `ADR-76(d)` diseñó (Propuesta 2 de `forense/benchmark-enlace-invarianza-v1_0.md`), ejecutado — no rediseñado. Adjudica si ENCUCI (`AP5_1_1`/`AP5_1_2`) y ENBIARE (`PB1_01`/`PB1_02`) son suficientemente convergentes para desbloquear las 8 producciones de `radio_confianza` hoy en `NO_LISTA_DECISION_HUMANA_PENDIENTE` (`produccion-modelo.tsv`, verificado en este acto: 8 filas, `objeto_modelo_origen=G5.radio_confianza`, `requiere_decision=SI` — cuenta exacta, no heredada).

**Qué NO es.** No rediseña el acto (`ADR-76(d)` ya lo selló). No sella nada en `canon/gobernanza-v1_15.md` (fuera de perímetro de este acto). No toca `AP5_1_3` (declarado fuera de alcance, per Propuesta 2 punto 2). No dicotomiza para el test mismo (usa 0-10 ordinal completo, per Propuesta 2 punto 3 — la dicotomización ≥8/10 es solo para comparación externa, si la hubiera).

**Estándar de éxito: `ARGUMENTO DE VINCULACIÓN DECLARADO`** (anclas de diseño OCDE 2017 + invarianza parcial hasta donde el par de dos ítems identifique + juicio experto rotulado como tal) — no invarianza clásica completa, que `ADR-76(d)` ya calificó inalcanzable hoy. Sellado como enmienda in situ sobre `ADR-76(d)`, `canon/gobernanza-v1_15.md:1122`, `ADR-80`/`ACTO FIRMAS-2` (13/ago/2026) — ver nota de procedencia abajo.

**Nota de procedencia del estándar — dos vías independientes, mismo resultado, corregida antes de push (no reescribe nada ya compartido).** Este acto congeló su Commit 1 con el estándar seleccionado en esta misma conversación (mesa, entre opciones estructuradas: "Sella ahora: argumento de vinculación declarado"), y redactó un borrador propio para sellarlo — primero citado como `ADR-79`. Al fusionar `origin/main` tras Commit 2 (dos veces, mientras este acto corría), aparecieron dos cosas: (1) `ACTO SELLA-3` ya había sellado un `ADR-79` real y **no relacionado** (ocho de nueve decisiones de mesa, `D-A`..`D-H`, ninguna fija este estándar — su inciso `D-B` solo autoriza correr el diseño, no adjudica la sub-pregunta) — el borrador se renumeró a `ADR-80` en un commit local, todavía sin push; (2) al fusionar de nuevo, `ACTO FIRMAS-2` (sesión distinta, nube, dispatch separado de mesa — "las dos firmas que desbloquean el carril de caja") ya había sellado **el mismo estándar, por el mismo razonamiento** ("si `INVARIANZA` sellara su propio estándar de éxito, sería autoadjudicación — el defecto que `ACTO RES` cometió esta mañana"), verbatim de mesa *"Benchmark web"* / *"usa lo que el benchmark ya dijo"*, como enmienda in situ real sobre `ADR-76(d)` bajo `ADR-80`. Dos sesiones, dos rutas de firma distintas, mismo desenlace — confirmación convergente, no coincidencia forzada. Este acto retira su propio borrador (nunca sellado en `canon/`, cero costo de retirarlo) y cita la enmienda real. Ninguno de los commits de este acto había sido compartido cuando se corrigió cada vez.

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

Bajo el estándar sellado (`gobernanza-v1_15.md:1122`, enmienda in situ sobre `ADR-76(d)`, `ADR-80`/`ACTO FIRMAS-2`: argumento de vinculación declarado), **NO RECHAZAR** significa:

- Las 8 producciones de `radio_confianza` (`produccion-modelo.tsv`, `objeto_modelo_origen=G5.radio_confianza`) pasan de `estado_uso_modelo=NO_LISTA_DECISION_HUMANA_PENDIENTE` / `requiere_decision=SI` a `estado_uso_modelo=LISTA_PARA_USO_MODELO` / `requiere_decision=NO`.
- La celda-D (`G5.radio_confianza.encuci_vs_enbiare.yaml`) registra `criterio_adjudicacion.escala` con el resultado (SOSTENIDA/PARCIAL y sobre qué parámetros), `candidatos[CHALLENGER].resultado` deja de ser `NO-EJECUTADO`, `fecha_adjudicacion`/`commit_adjudicacion` se llenan.
- **Lo que NO significa**: no promueve `ENBIARE` a `champion_actual` ni le da poder de sustitución sobre `ENCUCI` — `champion_actual` se mantiene `BASELINE.ENCUCI` y la clase `PROXY_PARCIAL` de `ADR-67(a)` no cambia aquí; este acto adjudica *convergencia de instrumentos para desbloquear el gate*, no superioridad de uno sobre otro. Tampoco resuelve la reserva de `AP5_1_3` (queda fuera de alcance, sin adjudicar). Tampoco mueve ningún contador de canon (`13 de 27`, `9 de 14`, `0 de 15`, etc.) — el contador que este acto instituye es, exclusivamente, el gate de las 8 producciones de `radio_confianza`.

Si el desenlace es **INVARIANZA RECHAZADA**: las 8 producciones NO se desbloquean, el gate de `ADR-67(a)` permanece exactamente como está, y este commit 1 ya declaró que ese desenlace era el menos probable — se reporta igual, sin forzarlo hacia el otro lado.

### 5. Promesa de primer resultado

El primer número que produzca el procedimiento del §2, corrido una sola vez con la semilla `20260813`, es el que se reporta en COMMIT 2. Si el script tiene un error de ejecución (no de resultado — p. ej. una columna mal referenciada, un `KeyError`), se corrige el error y se vuelve a correr; si el script corre sin error y produce un número, ese número no se descarta buscando otro.

*Cierra COMMIT 1. Los resultados viven exclusivamente en la sección "COMMIT 2" de abajo, en un commit de git separado que no edita esta sección.*

---

## COMMIT 2 · Resultados

*Corrido una sola vez, contra el procedimiento congelado en COMMIT 1 (commit `09c1fa3`), sin editar esa sección. Script efímero, fuera del repo (`tools/`/`tests/` no están en el perímetro declarado de este acto) — íntegro en el Apéndice al final de este commit para reproducibilidad completa. Autotest de la lógica de correlación/bootstrap sobre datos sintéticos (no sobre ENCUCI/ENBIARE) corrido antes de abrir microdato — ver primera línea de salida abajo.*

### Apertura de datos

- **ENCUCI 2020** `SEC_4_5.dbf` (`data/raw/BD_ENCUCI2020_dbf.zip`): `AP5_1_1`, `AP5_1_2`, `FAC_SEL`, `EST_DIS`, `UPM_DIS` — leídos con `tests/dbfmini.py` (lector ya validado del programa, reusado sin editar). n_filas=21,519; excluidas listwise (código `99` o vacío en cualquiera de los dos ítems)=121; útiles=21,398.
- **ENBIARE 2021** `TENBIARE.csv` (`data/raw/enbiare2021/enbiare_2021_base_de_datos_csv.zip`): `PB1_01`, `PB1_02`, `FAC_ELE`, `EST_DIS`, `UPM_DIS`. **Verificado contra archivo, no asumido por analogía con ENCUCI** (comprometido en COMMIT 1 §1): el ponderador de ENBIARE es `FAC_ELE`, no `FAC_SEL` — nombre distinto del de ENCUCI aunque `EST_DIS`/`UPM_DIS` sí coinciden de nombre. n_filas=31,166; excluidas=0 (los 31,166 casos tienen respuesta válida 00-10 en ambos ítems — verificado por distribución completa antes de calcular, ninguna categoría "99"/NS-NR presente en `PB1_01`/`PB1_02`).

### Salida completa del script (§2 del COMMIT 1, corrida única)

```
AUTOTEST: OK (r=1.0 exacto con x=y; r=None con var(x)=0; r=-1.0 exacto anticorrelacion; bootstrap en rango)

======================================================================
ENCUCI 2020 SEC_4_5 -- AP5_1_1 x AP5_1_2, ponderado FAC_SEL, EST_DIS/UPM_DIS
======================================================================
n_filas_totales=21519 excluidas(99/vacio, listwise)=121 utiles=21398
r_ponderado(AP5_1_1, AP5_1_2) = 0.516465  (n=21398)

======================================================================
ENBIARE 2021 TENBIARE -- PB1_01 x PB1_02, ponderado FAC_ELE, EST_DIS/UPM_DIS
======================================================================
n_filas_totales=31166 excluidas(no valido, listwise)=0 utiles=31166
r_ponderado(PB1_01, PB1_02) = 0.557538  (n=31166)

======================================================================
Bootstrap conglomerado ultimo, 2000 replicas, semilla 20260813
======================================================================
ENCUCI:  r=0.5165  IC95%=[0.4985, 0.5341]  replicas_no_definidas=0/2000
ENBIARE: r=0.5575  IC95%=[0.5446, 0.5704]  replicas_no_definidas=0/2000

CONFIGURAL ENCUCI:  SOSTENIDA
CONFIGURAL ENBIARE: SOSTENIDA

======================================================================
Metrica (tau-equivalente, lambda = sqrt(r12))
======================================================================
lambda_ENCUCI=0.7187  lambda_ENBIARE=0.7467  delta=-0.0280
IC95%(delta) = [-0.0431, -0.0132]  (replicas validas usadas: 2000/2000)
METRICA: NO SOSTENIDA

======================================================================
VEREDICTO (regla congelada en COMMIT 1)
======================================================================
INVARIANZA PARCIAL -- configural sostenida en ambos instrumentos, metrica no sostenida
```

Sin error de ejecución en la corrida — el número de arriba es el que se reporta, per la promesa de COMMIT 1 §5.

### Veredicto y regla A-bis aplicada

**INVARIANZA PARCIAL.** Se dice explícitamente sobre qué parámetro se sostiene y sobre cuál no, per la Reserva A-bis:

- **Configural: SOSTENIDA** en ambos instrumentos — `AP5_1_1`/`AP5_1_2` correlacionan 0.517 (IC95% estrictamente positivo) en ENCUCI; `PB1_01`/`PB1_02` correlacionan 0.558 (IC95% estrictamente positivo) en ENBIARE. Un solo factor explica ambos ítems, dentro de cada instrumento por separado, con margen amplio.
- **Métrica: NO SOSTENIDA** — las cargas tau-equivalentes implícitas difieren entre instrumentos (0.719 ENCUCI vs. 0.747 ENBIARE) con un intervalo de la diferencia que excluye 0. **Nota de magnitud, declarada para no sobre-leer el rechazo:** la diferencia puntual es pequeña (Δλ=0.028, ~4% relativo); con n grande en ambos lados (21,398 y 31,166), diferencias de esa magnitud alcanzan significancia estadística con facilidad — el rechazo es real bajo la regla congelada (el IC95% sí excluye 0), pero no describe una divergencia grande en términos sustantivos.

### B-bis aplicado — qué significa este NO RECHAZO

`INVARIANZA PARCIAL` cae en `NO RECHAZAR` (COMMIT 1 §4), el desenlace declarado de antemano como más probable. Bajo el estándar sellado (`gobernanza-v1_15.md:1122`, `ADR-80`/`ACTO FIRMAS-2`: argumento de vinculación declarado):

- Las **8 producciones de `radio_confianza`** en `produccion-modelo.tsv` (`objeto_modelo_origen=G5.radio_confianza`) pasan de `estado_uso_modelo=NO_LISTA_DECISION_HUMANA_PENDIENTE`/`requiere_decision=SI` a `estado_uso_modelo=LISTA_PARA_USO_MODELO`/`requiere_decision=NO`. Aplicado en este commit — diff verificado: exactamente 8 filas tocadas, 3 filas restantes sin cambio, 51 columnas por fila conservadas (`git diff --stat` + reparseo con `csv.DictReader` después de escribir, ver §"Verificación" abajo).
- **Hallazgo no silenciado, detectado en este acto:** de esas 8 filas, solo **2** son los ítems de confianza directamente probados aquí (`PB1_01`, `PB1_02`). Las otras **6** son la batería de precariedad financiera de Apartado F de ENBIARE (`PF1_1`..`PF1_6`, "pidió prestado para alimentos/renta/agua/luz-gas-teléfono/colegiaturas/medicinas") — comparten `objeto_modelo_origen=G5.radio_confianza` y `especificacion_id=ESP-OPACA-C-9ecb5c61` porque se extrajeron en el mismo lote (la celda-D ya declaraba esto: "Apartado F... mismo folio/hogar/persona seleccionada"), no porque haya evidencia de que midan el mismo constructo que `radio_confianza`. Este acto **no** prueba nada, directa ni indirectamente, sobre `PF1_1..6` — se desbloquean junto con las otras 2 solo por la regla de gate que `ADR-67(a)`/`ADR-76(d)` ya fijaron sobre el bundle de 8 filas, no por adjudicación de este acto sobre su contenido. Queda nombrado para que un acto de curación aparte revise si esa clasificación es correcta.
- La celda-D (`G5.radio_confianza.encuci_vs_enbiare.yaml`) registra el resultado en `criterio_adjudicacion.escala` y `candidatos[CHALLENGER].resultado`; `fecha_adjudicacion="2026-08-13"`; `commit_adjudicacion` se cierra en un commit siguiente (mismo mecanismo que `commit_declaracion` ya usó en este archivo — un commit no puede citar su propio SHA final).
- **`champion_actual` se mantiene `BASELINE.ENCUCI`, sin cambio.** Este acto adjudica convergencia suficiente para desbloquear el gate — no adjudica superioridad ni da a ENBIARE poder de sustitución. La clase `PROXY_PARCIAL` de `ADR-67(a)` no cambia.
- `AP5_1_3` permanece fuera de alcance, sin adjudicar (Propuesta 2 punto 2 — declarado, no forzado).
- Ningún contador de `canon/` se mueve. El único contador que este acto instituye es el gate de las 8 producciones citado arriba.

### Verificación

- `python3 tests/test_celdas_d.py` → `2 archivo(s) de celda-D validan` (sin regresión tras el edit).
- `produccion-modelo.tsv` reparseado con `csv.DictReader` después de escribir: 11 filas, 51 columnas, 0 filas malformadas; `estado_uso_modelo`/`requiere_decision` cuentan 11/11 `LISTA_PARA_USO_MODELO`/`NO` (antes: 8 `NO_LISTA_DECISION_HUMANA_PENDIENTE` + 3 `LISTA_PARA_USO_MODELO`).
- Edición del TSV hecha por índice de columna sobre texto plano, sin `csv.writer` (evita el defecto ya conocido en este programa: `csv.writer` corrompe estos TSV de tabulador plano).

### Apéndice — script completo (reproducibilidad)

```python
#!/usr/bin/env python3
"""ENCARGO 9 -- calculo del acto de vinculacion-invarianza ENCUCI<->ENBIARE.
Procedimiento congelado en forense/notas/2026-08-13-invarianza-encuci-enbiare.md
COMMIT 1 (repo mm-invarianza-encuci-enbiare, commit 09c1fa3). Script efimero,
fuera del repo (perimetro del acto no incluye tools/ ni tests/) -- documentado
linea por linea aqui y en COMMIT 2 de la nota para reproducibilidad.

Corre desde la raiz del worktree: python3 /tmp/claude-1000/invarianza_encuci_enbiare.py
"""
import csv
import io
import random
import sys
import zipfile
from collections import defaultdict

sys.path.insert(0, "tests")
import dbfmini  # noqa: E402

SEED = 20260813
N_BOOT = 2000
RAW = "data/raw"


def weighted_corr_from_sums(n, sw, swx, swy, swxy, swx2, swy2):
    """r ponderado a partir de sumas agregadas. None si no calculable."""
    if sw <= 0:
        return None
    mx = swx / sw
    my = swy / sw
    cov = swxy / sw - mx * my
    varx = swx2 / sw - mx * mx
    vary = swy2 / sw - my * my
    if varx <= 0 or vary <= 0:
        return None
    return cov / (varx * vary) ** 0.5


def aggregate_by_upm(rows):
    """rows: iterable de (est, upm, w, x, y). Devuelve dict est -> dict upm -> tupla de sumas."""
    out = defaultdict(lambda: defaultdict(lambda: [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))
    for est, upm, w, x, y in rows:
        acc = out[est][upm]
        acc[0] += 1
        acc[1] += w
        acc[2] += w * x
        acc[3] += w * y
        acc[4] += w * x * y
        acc[5] += w * x * x
        acc[6] += w * y * y
    return out


def point_estimate(agg):
    n = sw = swx = swy = swxy = swx2 = swy2 = 0
    for est, upms in agg.items():
        for upm, (cn, csw, cswx, cswy, cswxy, cswx2, cswy2) in upms.items():
            n += cn
            sw += csw
            swx += cswx
            swy += cswy
            swxy += cswxy
            swx2 += cswx2
            swy2 += cswy2
    r = weighted_corr_from_sums(n, sw, swx, swy, swxy, swx2, swy2)
    return n, r


def bootstrap_replicates(agg, rng, n_boot):
    """Bootstrap de conglomerado ultimo: resample UPM con reemplazo dentro de
    cada estrato, mismas n de UPM por estrato que el original."""
    strata = []
    for est, upms in agg.items():
        upm_list = list(upms.values())
        strata.append(upm_list)
    reps = []
    for _ in range(n_boot):
        n = sw = swx = swy = swxy = swx2 = swy2 = 0
        for upm_list in strata:
            k = len(upm_list)
            if k == 0:
                continue
            chosen = rng.choices(upm_list, k=k)
            for (cn, csw, cswx, cswy, cswxy, cswx2, cswy2) in chosen:
                n += cn
                sw += csw
                swx += cswx
                swy += cswy
                swxy += cswxy
                swx2 += cswx2
                swy2 += cswy2
        r = weighted_corr_from_sums(n, sw, swx, swy, swxy, swx2, swy2)
        reps.append(r)
    return reps


def percentile_ci(values, lo=2.5, hi=97.5):
    vals = sorted(v for v in values if v is not None)
    if not vals:
        return None
    n = len(vals)

    def pct(p):
        idx = (p / 100) * (n - 1)
        lo_i = int(idx)
        hi_i = min(lo_i + 1, n - 1)
        frac = idx - lo_i
        return vals[lo_i] * (1 - frac) + vals[hi_i] * frac

    return pct(lo), pct(hi)


def _autotest():
    rows = [("E1", "U1", 1.0, 1, 1), ("E1", "U1", 1.0, 2, 2),
            ("E1", "U2", 1.0, 3, 3), ("E1", "U2", 1.0, 4, 4)]
    agg = aggregate_by_upm(rows)
    n, r = point_estimate(agg)
    assert n == 4, n
    assert abs(r - 1.0) < 1e-9, r
    rows2 = [("E1", "U1", 1.0, 5, 1), ("E1", "U1", 1.0, 5, 2), ("E1", "U2", 1.0, 5, 3)]
    agg2 = aggregate_by_upm(rows2)
    n2, r2 = point_estimate(agg2)
    assert r2 is None, r2
    rows3 = [("E1", "U1", 1.0, 1, 10), ("E1", "U1", 1.0, 2, 9),
             ("E1", "U2", 1.0, 3, 8), ("E1", "U2", 1.0, 4, 7)]
    agg3 = aggregate_by_upm(rows3)
    n3, r3 = point_estimate(agg3)
    assert abs(r3 - (-1.0)) < 1e-9, r3
    rng = random.Random(1)
    reps = bootstrap_replicates(agg, rng, 50)
    assert all(v is None or -1.0001 <= v <= 1.0001 for v in reps), reps
    print("AUTOTEST: OK (r=1.0 exacto con x=y; r=None con var(x)=0; r=-1.0 exacto anticorrelacion; bootstrap en rango)")


_autotest()

print()
print("=" * 70)
print("ENCUCI 2020 SEC_4_5 -- AP5_1_1 x AP5_1_2, ponderado FAC_SEL, EST_DIS/UPM_DIS")
print("=" * 70)

import tempfile
TMP = tempfile.mkdtemp(prefix="invarianza_")
with zipfile.ZipFile(f"{RAW}/BD_ENCUCI2020_dbf.zip") as z:
    z.extract("ENCUCI_2020_SEC_4_5.dbf", TMP)

encuci_rows = list(dbfmini.read_dbf(
    f"{TMP}/ENCUCI_2020_SEC_4_5.dbf",
    wanted_fields=["AP5_1_1", "AP5_1_2", "FAC_SEL", "EST_DIS", "UPM_DIS"]))

n_total_encuci = len(encuci_rows)
tuples_encuci = []
no_resp_encuci = 0
for row in encuci_rows:
    a = row["AP5_1_1"].strip()
    b = row["AP5_1_2"].strip()
    if not a or not b or a == "99" or b == "99":
        no_resp_encuci += 1
        continue
    x = int(a)
    y = int(b)
    w = float(row["FAC_SEL"].strip())
    est = row["EST_DIS"].strip()
    upm = row["UPM_DIS"].strip()
    tuples_encuci.append((est, upm, w, x, y))

print(f"n_filas_totales={n_total_encuci} excluidas(99/vacio, listwise)={no_resp_encuci} utiles={len(tuples_encuci)}")

agg_encuci = aggregate_by_upm(tuples_encuci)
n_encuci, r_encuci = point_estimate(agg_encuci)
print(f"r_ponderado(AP5_1_1, AP5_1_2) = {r_encuci:.6f}  (n={n_encuci})")

print()
print("=" * 70)
print("ENBIARE 2021 TENBIARE -- PB1_01 x PB1_02, ponderado FAC_ELE, EST_DIS/UPM_DIS")
print("=" * 70)

with zipfile.ZipFile(f"{RAW}/enbiare2021/enbiare_2021_base_de_datos_csv.zip") as z:
    with z.open("TENBIARE.csv") as f:
        text = io.TextIOWrapper(f, encoding="latin-1")
        reader = csv.DictReader(text)
        enbiare_rows = list(reader)

n_total_enbiare = len(enbiare_rows)
tuples_enbiare = []
no_resp_enbiare = 0
for row in enbiare_rows:
    a = row["PB1_01"].strip()
    b = row["PB1_02"].strip()
    if not a or not b or not a.isdigit() or not b.isdigit():
        no_resp_enbiare += 1
        continue
    x = int(a)
    y = int(b)
    if not (0 <= x <= 10 and 0 <= y <= 10):
        no_resp_enbiare += 1
        continue
    w = float(row["FAC_ELE"].strip())
    est = row["EST_DIS"].strip()
    upm = row["UPM_DIS"].strip()
    tuples_enbiare.append((est, upm, w, x, y))

print(f"n_filas_totales={n_total_enbiare} excluidas(no valido, listwise)={no_resp_enbiare} utiles={len(tuples_enbiare)}")

agg_enbiare = aggregate_by_upm(tuples_enbiare)
n_enbiare, r_enbiare = point_estimate(agg_enbiare)
print(f"r_ponderado(PB1_01, PB1_02) = {r_enbiare:.6f}  (n={n_enbiare})")

print()
print("=" * 70)
print(f"Bootstrap conglomerado ultimo, {N_BOOT} replicas, semilla {SEED}")
print("=" * 70)

rng_encuci = random.Random(SEED)
rng_enbiare = random.Random(SEED)  # semilla identica, streams independientes (RNG distintos) -- documentado

reps_encuci = bootstrap_replicates(agg_encuci, rng_encuci, N_BOOT)
reps_enbiare = bootstrap_replicates(agg_enbiare, rng_enbiare, N_BOOT)

ci_encuci = percentile_ci(reps_encuci)
ci_enbiare = percentile_ci(reps_enbiare)

n_none_encuci = sum(1 for v in reps_encuci if v is None)
n_none_enbiare = sum(1 for v in reps_enbiare if v is None)

print(f"ENCUCI:  r={r_encuci:.4f}  IC95%=[{ci_encuci[0]:.4f}, {ci_encuci[1]:.4f}]  replicas_no_definidas={n_none_encuci}/{N_BOOT}")
print(f"ENBIARE: r={r_enbiare:.4f}  IC95%=[{ci_enbiare[0]:.4f}, {ci_enbiare[1]:.4f}]  replicas_no_definidas={n_none_enbiare}/{N_BOOT}")

configural_encuci = (r_encuci > 0) and (ci_encuci[0] > 0)
configural_enbiare = (r_enbiare > 0) and (ci_enbiare[0] > 0)
print()
print(f"CONFIGURAL ENCUCI:  {'SOSTENIDA' if configural_encuci else 'NO SOSTENIDA'}")
print(f"CONFIGURAL ENBIARE: {'SOSTENIDA' if configural_enbiare else 'NO SOSTENIDA'}")

print()
print("=" * 70)
print("Metrica (tau-equivalente, lambda = sqrt(r12))")
print("=" * 70)

if configural_encuci and configural_enbiare:
    lam_encuci = r_encuci ** 0.5
    lam_enbiare = r_enbiare ** 0.5
    lam_reps_encuci = [v ** 0.5 if (v is not None and v > 0) else None for v in reps_encuci]
    lam_reps_enbiare = [v ** 0.5 if (v is not None and v > 0) else None for v in reps_enbiare]
    deltas = [a - b for a, b in zip(lam_reps_encuci, lam_reps_enbiare) if a is not None and b is not None]
    n_deltas_validos = len(deltas)
    delta_ci = percentile_ci(deltas)
    delta_pe = lam_encuci - lam_enbiare
    print(f"lambda_ENCUCI={lam_encuci:.4f}  lambda_ENBIARE={lam_enbiare:.4f}  delta={delta_pe:.4f}")
    print(f"IC95%(delta) = [{delta_ci[0]:.4f}, {delta_ci[1]:.4f}]  (replicas validas usadas: {n_deltas_validos}/{N_BOOT})")
    metrica_sostenida = delta_ci[0] <= 0 <= delta_ci[1]
    print(f"METRICA: {'SOSTENIDA' if metrica_sostenida else 'NO SOSTENIDA'}")
else:
    print("METRICA: NO EVALUABLE -- configural no sostenida en al menos un instrumento")
    metrica_sostenida = None

print()
print("=" * 70)
print("VEREDICTO (regla congelada en COMMIT 1)")
print("=" * 70)
if configural_encuci and configural_enbiare and metrica_sostenida:
    veredicto = "INVARIANZA SOSTENIDA"
elif configural_encuci and configural_enbiare:
    veredicto = "INVARIANZA PARCIAL -- configural sostenida en ambos instrumentos, metrica no sostenida" if metrica_sostenida is False else "INVARIANZA PARCIAL -- configural sostenida en ambos instrumentos, metrica no evaluable"
else:
    veredicto = "INVARIANZA RECHAZADA -- configural no sostenida en al menos un instrumento"
print(veredicto)
```
