# `ADV1-M5 v2` · escala de cinco casillas del piloto — capa de cómputo — 20/ago/2026

**Acto:** `SELLA-M5-V2` (nube, Opus). Sella `ADV1-M5 v2` como capa de cómputo sobre la escala original, y cumple `D-ii`. Nombre estable de este mecanismo: **`ADV1-M5 v2`** — nunca el rótulo pelado a secas: colisiona con cuatro habitantes vivos de ese mismo rótulo pelado en este corpus (`ADR-100(5)` · el defecto homónimo de `RONDA-M:61`, cableado en `milpa/src/matriz.py:21` · el homónimo histórico de `forense/hallazgos.md:65` · y este mecanismo, `ADV1-M5`, careo §B, y ahora su v2).

**Relación con `v1_0`:** `v1_0` (`forense/escala-cinco-casillas-piloto-v1_0.md`) queda íntegro, sin editar, y gana un banner de una línea apuntando aquí — mismo patrón que `v0.4` sobre `v0.3` del contrato celda-D. Corolario 1 de `A.10`: *«un sello vencido se reactiva por re-sello contra el universo nuevo, nunca por edición del viejo»*. `v1_0` no queda refutado por este acto: sigue siendo la fuente para el §1 de abajo.

**Firma de mesa que sella esta capa, verbatim (20/ago/2026):** «Vamos con 1» — sobre la opción (1) del benchmark de `forense/adv-duelo/ADV1-M5-v2-propuesta-2026-08-20.md`: eje unificado, márgenes declarados antes, veredictos por posición del intervalo, todos los corredores como filas de la misma tabla, y secuencia fija declarada al sellar. Y «Venga!!!!» autorizando el sello.

**Firma que ancla la obligación (`D-ii`, `TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md` §4 y `CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §C, texto idéntico en ambos, FIRMADA 19/ago/2026):**

> **D-ii** · "Firma la tabla de cinco casillas de `ADV1-M5` antes de la primera celda — 'incluso un piloto imperfecto es seguro si su peor resultado deja de ser pivote estratégico y pasa a ser dato'." — FIRMADA 19/ago.

Con este sello, **`D-ii` queda CUMPLIDA** y la primera celda puntuada del piloto deja de estar bloqueada por esta compuerta.

---

## 1 · El párrafo original, verbatim, y sigue siendo la fuente

Copiado verbatim de `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:42` (§B, párrafo `ADV1-M5` — nota: el archivo vive en `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md`, no bajo `forense/adv-duelo/`; no fue movido cuando los cuatro informes `compass-5`/`ADV-1`/`ADV-2` sí lo fueron, ver `forense/firmas-pendientes.tsv` fila de cascada de `ADR-128(e)`). No se toca una palabra:

> **ADV1-M5 · Tabla de consecuencias, cinco casillas, firmada antes de la primera celda.** (1) L más cerca → "en estos momentos el canal LLM quedó más cerca del dato"; NO licencia "el motor sobra" (procedencia, contrafactuales e interpretabilidad no se puntuaron). (2) M más cerca → "el motor transportó mejor que la memoria del LLM"; NO licencia "M es bueno" salvo skill material sobre B. (3) Empate-TOST dentro de banda pre-declarada. (4) **Ninguno supera a B** → ninguno utilizable v1; re-tierización dirigida sin coronación. (5) **Ambos fuera del IC de R en la mayoría** → el fenómeno no es predecible con estas herramientas hoy; consecuencia propia, y es la casilla que el FFC dice esperar. Cláusula de alcance: ningún resultado autoriza abandonar L ni M para usos no muestreados — el duelo mide estimación de cantidades encuestables y nada más.

---

## 2 · La capa de cómputo — eje, márgenes, secuencia, veredictos

Tomada íntegra de `forense/adv-duelo/ADV1-M5-v2-propuesta-2026-08-20.md`, sellada por la firma de mesa de la cabecera. Remito a esa propuesta para el detalle completo; aquí queda la capa operativa:

**Eje único (§2 de la propuesta).** Ya implementado en `forense/prereg-duelo-v2/scoring-adv1-m3.py:359` (`def skill`, línea corregida — el archivo citaba `:74`, desactualizada desde `PR #330`; verificado por `grep -n "^def skill" forense/prereg-duelo-v2/scoring-adv1-m3.py`): `s = 1 − error_corredor / error_baseline`, contra `B` como baseline, uno por corredor (`s_L-solo`, `s_L+corpus`, `s_M`, `s_E`). `Δs = s_A − s_B` entre corredores. El intervalo del agregado sale de remuestreo pareado entre celdas, no del `EE` del árbitro por celda.

**Enmienda `PROPAGA-330-337`, 25/ago/2026 — scope del agregado adjudicante.** `PR #330` (`ACTO scoring-adv1-m3`) dejó este agregado sin scope declarado: `scoring-adv1-m3.py` implementa `comparacion_principal_id` (`:85`, `:102`, `:205-322`) con universos propios por comparación (`_construir_universo`, `:581`; `construir_universo_marginal`/`construir_universo_pareado`, `:618`/`:624`), no un solo universo compartido. Se declara: el agregado que adjudica es **{L predeclarada, M}** vía `comparacion_principal_id`, cada comparación con su propio universo, más el corredor **E** y la **L auxiliar no-gating** (no adjudica por sí sola, informativa). **La reserva de cuál `L` se predeclara (L-solo vs. L+corpus) sigue viva/abierta** — este acto no la cierra, solo declara el scope que `PR #330` implementó sin anunciarlo aquí.

**Márgenes (§3 de la propuesta).** Línea del mínimo `s = 0`, no negociable. Banda de indiferencia `±Δ`: **no se fija aquí** — `D-iv` (FIRMADA 19/ago) ordena que el acto de pre-registro la derive de los `EE` reales del set y traiga el número con su justificación; mesa la firma aparte. El estimado puntual nunca adjudica: solo la posición del intervalo.

**Secuencia fija (§4 de la propuesta) — fijada al sellar y no después:**

```
PASO 0 (siempre, en paralelo, nunca gatea) — cobertura contra R,
        alimenta la LECTURA (5) y la calibración al 80%.
PASO 1 · ¿Algún corredor supera a B? (IC de s contra la línea 0)
  ├─ ninguno despeja 0 por arriba ──► LECTURA (4). TERMINA.
  └─ al menos uno lo despeja ───────► sigue al PASO 2.
PASO 2 · Entre los que superan a B: ¿equivalentes o distintos?
  (IC de Δs contra ±Δ)
  ├─ IC entero dentro de ±Δ ────────► (3a) EQUIVALENTES
  ├─ IC fuera por el lado de L ─────► (1)
  ├─ IC fuera por el lado de M ─────► (2)
  └─ IC ni dentro ni excluye 0 ─────► (3b) INDETERMINADO
PASO 3 · E se reporta siempre, fila de la misma tabla, nunca gatea.
```

**Tabla de veredictos por posición del intervalo (§5 de la propuesta):**

| # | Posición | Lectura publicable |
|---|---|---|
| **(4)** | Ningún IC de `s` despeja 0 | Ninguno utilizable v1 |
| **(1)** | `IC(Δs)` entero fuera de `+Δ` | El canal LLM quedó más cerca del dato |
| **(2)** | `IC(Δs)` entero fuera de `−Δ` | El motor transportó mejor que la memoria del LLM |
| **(3a)** | `IC(Δs)` entero dentro de `±Δ` | Equivalentes dentro de la banda pre-declarada |
| **(3b)** | `IC(Δs)` ni dentro ni excluyendo 0 | Indeterminado — el piloto no tuvo potencia para distinguirlos |
| **(5)** | Cobertura contra `R` baja en la mayoría | El fenómeno no es predecible con estas herramientas hoy — se reporta siempre |

---

## 3 · Las cinco cláusulas anti-sobrelectura del original, verbatim, atadas a su posición

Son lo que `D-ii` firmó. No se tocan:

| # | Cláusula anti-sobrelectura (verbatim del original) |
|---|---|
| **(1)** | *«NO licencia "el motor sobra" (procedencia, contrafactuales e interpretabilidad no se puntuaron)»* |
| **(2)** | *«NO licencia "M es bueno" salvo skill material sobre B»* |
| **(4)** | *«ninguno utilizable v1; re-tierización dirigida sin coronación»* |
| **(5)** | *«el fenómeno no es predecible con estas herramientas hoy; consecuencia propia, y es la casilla que el FFC dice esperar»* |

**Cláusula de alcance — gobierna sobre las seis, verbatim del original:**

> «ningún resultado autoriza abandonar L ni M para usos no muestreados — el duelo mide estimación de cantidades encuestables y nada más.»

---

## 4 · Declaración B-bis — qué significa que el falsador no refute

Bloque B-bis (`instrucciones-proyecto-v2_10.md:113`): *«La ficha declara, antes de correr, qué significa que el falsador no refute: si la regla queda corroborada, si queda acotada, o si el falsador era demasiado débil para decir nada.»* Esta declaración es la que abre la compuerta B-bis que `v1_0` dejó activada.

Bajo la escala de §2, cuando el falsador (el intento de mostrar que `Δs` cae fuera de la banda de indiferencia) no refuta, caen exactamente dos lecturas de la tabla, y esta capa las mantiene **separadas y no fundidas**:

- **`(3a) EQUIVALENTES`** — el falsador intentó y no encontró diferencia dentro de una banda pre-declarada con potencia suficiente: **corroboración, hallazgo positivo.** La regla (equivalencia entre corredores dentro de `±Δ`) queda corroborada.
- **`(3b) INDETERMINADO`** — el intervalo no cae ni dentro de `±Δ` ni excluye 0: **el falsador fue demasiado débil** para decir nada. No se reporta como empate; si el piloto estaba subpotenciado, la diferencia real puede seguir siendo sustancial.

Esta separación es exactamente la que el original fundía en su casilla (3) «Empate-TOST», y es la traducción declarada en el §1 de `forense/adv-duelo/ADV1-M5-v2-propuesta-2026-08-20.md`.

**Nota de alcance sobre `mesa-pendientes.md` §1:** este acto responde a B-bis dentro del vocabulario propio de la escala v2 (posición del intervalo, corroboración vs. falsador débil). No elige entre las cuatro lecturas candidatas de `mesa-pendientes.md` §1 sobre el origen del término «falsador» en la cabecera del encargo original — esa pregunta, sobre procedencia del término, sigue abierta a mesa y no la cierra este acto.

---

## 5 · Regla de precedencia — fijada al sellar y no después

Es la secuencia de §2 arriba (PASO 0 → PASO 1 → PASO 2 → PASO 3). La secuencia no la inventa este acto: la implementa. La casilla (2) del original ya condicionaba su lectura a «skill material sobre B» — eso es el PASO 1 leído como compuerta, no como advertencia. Regla del Bloque B-bis (`instrucciones-proyecto-v2_10.md:113`): *«Si dos filas de una escala pueden satisfacerse a la vez, se declara cuál manda, al sellar y no después.»* Esta secuencia es esa declaración, y gobierna sobre cualquier lectura genérica de las cinco casillas.

Responde también a `mesa-pendientes.md` §2 (Opción C, la que el propio texto de `ADV1-M3`/`ADV1-M4` ya sugería): se adopta Opción C — precedencia por orden de evaluación (PASO 1 primero contra `B`; PASO 2 solo si alguien lo superó; PASO 0/PASO 3 en paralelo, sin gatear) — vía la firma de mesa «Vamos con 1» sobre el benchmark que la deriva.

---

## Cierre

Este documento es la capa de cómputo vigente de `ADV1-M5`, sellada por `ADR` correspondiente en `canon/gobernanza-v1_15.md`. `v1_0` sigue siendo la fuente para el texto original (§1 arriba lo cita, no lo reemplaza). Lo que este documento NO fija: `Δ` (pre-registro, `D-iv`) · la adjudicación de `FP-91` (los siete umbrales) · qué emite el corredor `M` (sesión `EMISOR-M`) · el marco de candidatas ni el sorteo.
