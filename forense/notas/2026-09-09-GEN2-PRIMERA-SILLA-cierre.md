# `ACTO GEN2-PRIMERA-SILLA` — nota de cierre

**9 de septiembre de 2026 · NUBE, Opus · rama `claude/tender-franklin-sh9430` · base `main = 8b9f9d4`**

Encargo archivado verbatim (0-bis A.3): `forense/encargos/2026-09-09-GEN2-PRIMERA-SILLA.md`.
Firmas que este acto porta y que el merge sella: **FIRMA 1** (contador, `cuenta_gen2 = SI` para `CALC-0003-v3` y `CALC-B-0001`) y **FIRMA 2** (adopción, condicionada a P1/P2 en verde).
Contexto medido que se hereda y NO se re-descubre: `forense/notas/2026-09-08-GEN2-C0-B-cierre.md` §5.

---

## 0 · Qué se pidió y qué salió

| pieza | pedido | entregado |
|---|---|---|
| **P1** | `tolerancia_adopcion`: la adopción compara al grano del consumidor; la reproducibilidad no se afloja | **HECHO.** `_compara_adopcion` en `tools/corrida0.py`; `_compara_result` y `verify` intactas. `NC-0069` CERRADA, `FP-365` EJECUTADA |
| **P2** | la llave correcta del WARN; adoptar 1 baja el conteo en exactamente 1 | **HECHO y falsado.** `NC-0068` CERRADA, `FP-364` EJECUTADA |
| **P3** | las dos filas del contador, registro re-derivado una vez, `status` pegado | **HECHO.** `N_corridas_selladas` 3 → **5**. La cifra de resultados sorprendió y se pega explicada (§5) |
| **P4** | la cita, con P1+P2 en verde | **HECHO.** WARN 443 → **442**, exactamente 1. `NC-0053` CERRADA |

**Las cuatro se movieron.** La silla que llevaba todo el programa vacía está ocupada, y el patrón queda probado de punta a punta para `C0-D`.

---

## 1 · P1 · Un campo servía a dos preguntas; ahora son dos

`ACTO GEN2-C0-B` §5.4 dejó el diagnóstico medido y este acto sólo lo ejecutó. `tolerancia.abs` contestaba a la vez:

1. *«¿esta corrida se reproduce a sí misma?»* — `1e-10` es correcto y aflojarlo un decimal es perder sensibilidad.
2. *«¿el consumidor materializa este RESULT?»* — el grano NO lo fija la corrida sino `milpa/`, que publica **seis decimales**.

`T35 (c)` usaba la primera para contestar la segunda. Por eso el único candidato real del programa daba `FAIL` por grano y la cita no se escribía.

`tools/corrida0.py::_compara_adopcion` separa las dos preguntas, con **tres modos y en este orden**:

| declaración de la spec | vara de adopción |
|---|---|
| `tolerancia_adopcion` numérica | esa tolerancia, tal cual |
| `tolerancia_adopcion: NO-APLICA` | la de reproducibilidad — **`NO-APLICA` es un valor**, no la ausencia del campo |
| sin declarar (**defecto**) | el RESULT **redondeado al grano del consumidor**, comparado EXACTO |

`_compara_result` no cambió una línea: `verify` compara hoy igual que ayer. La nueva columna `tolerancia_adopcion` viaja en `data/corrida0/resultados.tsv` (vacía = defecto), y `CALC-B-0001` adopta **sin tocar su spec congelada**, por la rama de defecto.

**Los dos falsadores, sobre el caso MEDIDO de C0-B (no uno inventado):**

```
_compara_result   (0.04569409956405095, 0.045694, tol.abs=1e-10)  -> False   ← el FAIL falso era real
_compara_adopcion (0.04569409956405095, 0.045694)                 -> True    delta=9.956e-08 · grano = 6 decimales
_compara_adopcion (0.04569409956405095, 0.045695)                 -> False   delta=9.004e-07 · grano = 6 decimales
```

La segunda línea es lo que desbloquea la silla; **la tercera es lo que impide que esto sea aflojar la tolerancia con otro nombre.** `T-ADOPCION-GRANO` y `T-ADOPCION-DECLARADA` en `tests/test_corrida0.py` fijan las dos, más `NO-APLICA`, más los tipos donde el grano no significa nada (`entero`, `texto` → exacto, como siempre).

## 2 · P2 · La llave del WARN, y la prueba de que muerde

`t35_repro` construía `Counter(u["resultado_id"] for u in usos)` —ids de **DEMANDA** (`RES-NNNN`)— y lo consultaba con un id de **OFERTA** (`RESULT-…`). C0-B §5.3 midió los dos espacios: **intersección 0**. Con esa llave el WARN no podía bajar ni con una adopción real y correcta.

Ahora la llave es `usos.corrida0_resultado_id`, y **sólo cuenta con la cadena completa**: uso activo + marca + `corrida0_generacion: GEN2`. Media cita no adopta — ya falla por `T35 (e)` y no debe además bajar el conteo, o el WARN volvería a mentir por el otro lado (`T-SSA-LLAVE-MEDIAS`).

**Control positivo, corrido de verdad y no razonado:** revirtiendo *sólo* la llave y dejando todo lo demás, el falsador `T-SSA-LLAVE` falla con el mensaje exacto que C0-B predijo —

```
FAIL T-SSA-LLAVE: adoptar 1 no bajo el conteo en exactamente 1: antes=2 despues=2
```

— y con la llave correcta pasa. La tabla «llave de HOY vs llave correcta» de C0-B queda reproducida en un test permanente.

## 3 · P3 · FIRMA 1, y la cifra que sorprendió

Dos filas en `data/corrida0/decisiones.tsv`, escritas por vía directa: **cero simulación**, ni siquiera en memoria (la fotocopiadora ya está desarmada por `CHECADOR-2` y aun así no se usó). Registro re-derivado **una vez**, con `--escribe`. `status` pegado sin retocar:

| contador | antes | después |
|---|---|---|
| `N_corridas_selladas` | 3 | **5** |
| `N_resultados_sellados` (renglones OFERTA que cuentan GEN2) | 211 | **443** |
| `N_resultados_gen2_sellados` (ids ÚNICOS) | 211 | **315** |
| `N_resultados_gen2_adoptados_activos` | 0 | **1** |
| `dependencias_numericas_legacy_activas` | 205 | **204** |

**El encargo esperaba 301 y la máquina dijo 315. Se pega y se explica, no se fuerza.** El desglose, derivado de `resultados.tsv`:

```
CALC-0001      SELLADA                 54
CALC-0002      SELLADA                 29
CALC-0003-v2   SUPERADO→CALC-0003-v3  128
CALC-0003-v3   SUPERADO→CALC-0003-v4  142
CALC-B-0001    SELLADA                 90
                                      ─── 443 renglones · 315 ids únicos
```

La simulación de C0-B (301) firmaba **sólo** `CALC-B-0001`: 211 + 90. FIRMA 1 firma **dos** CALC. `CALC-0003-v3` trae 142 RESULT, pero **128 de ellos son los mismos ids de `v2`** por cadena `repite_de` — la unicidad de un RESULT es por corrida, y el contador de ids únicos no los suma dos veces. Así que v3 aporta **14**, no 142: `211 + 90 + 14 = 315`. La cifra no sorprende por un defecto; sorprende porque el encargo simuló una firma y se dictaron dos.

**Reserva que no se forzó (`NC-0071`, `FP-362` → FIRMADA-PARCIAL):** FIRMA 1 nombra `CALC-0003-v3`, **no `v4`** — y `v4` es el sello **vigente**, con `v3` en `SUPERADO→CALC-0003-v4`. El contador cuenta hoy una corrida superada y no la vigente. El efecto en la cifra es de **1 id**; lo que queda raro es *cuál* corrida está contada. No se firmó `v4` desde aquí: sería inventar el objeto de una firma de mesa.

## 4 · P4 · La primera silla, ocupada

Un consumidor, un campo, en la única ranura que el registro reconoce (una conducta con `p:` dentro del `entonces` de una regla de `milpa/tramite.yaml`), tal como C0-B §5.1 la derivó:

```yaml
- {conducta: recibe_remesas, p: 0.045694, clase: "MEDIDO·p(tasa base ponderada)",
   corrida0_resultado_id: RESULT-B-ENIGH-2022-P, corrida0_generacion: GEN2}
```

**El `p` no se movió.** Vale hoy exactamente lo que valía el 8/sep: lo único que se agrega es de dónde viene. No se aflojó `tolerancia.abs`, no se redondeó ningún RESULT y no se tocó ninguna spec congelada.

La línea pedida, medida antes y después de escribir la cita y con lo demás idéntico:

```
antes:    SELLADA-SIN-ADOPTAR: 443 · más vieja: 1 días   ·   T35: 0 FAIL
después:  SELLADA-SIN-ADOPTAR: 442 · más vieja: 1 días   ·   T35: 0 FAIL
```

**443 → 442: exactamente uno, y con cero FAIL.** Los dos hechos importan por separado: el `−1` es P2 funcionando, y el `0 FAIL` es P1 funcionando — sin P1 esta misma cita habría metido el `FAIL` falso que C0-B se negó a meter.

**El número del encargo era 211→210 y el real es 443→442.** No es discrepancia de mecanismo sino de orden: P3 firma dos CALC *antes* de que P4 adopte, así que el universo del WARN sube (211 → 443 renglones) antes de bajar. La resta es la misma y es 1.

## 5 · Contadores

| contador | antes | después | por qué |
|---|---|---|---|
| `N_corridas_selladas` | 3 | **5** | FIRMA 1 |
| `N_resultados_gen2_sellados` | 211 | **315** | FIRMA 1 (§3: +90 de B, +14 de v3) |
| `N_resultados_gen2_adoptados_activos` | 0 | **1** | P4 — **la primera del programa** |
| `dependencias_numericas_legacy_activas` | 205 | **204** | ídem |
| `SELLADA-SIN-ADOPTAR` | 443 | **442** | P4, medido con P2 puesta |
| `no_corrido_abiertas` | 37 | **37** | tres cierran (`NC-0053`, `NC-0068`, `NC-0069`), tres abren (`NC-0071..0073`) |

## 6 · Registro de filas

- **`NC-0053`** (contadas ≠ adoptadas; E.2 pendiente) → **CERRADA** por P4.
- **`NC-0068`** (la llave del WARN) → **CERRADA** por P2. `FP-364` → **EJECUTADA**.
- **`NC-0069`** (`tolerancia.abs` sirve a dos preguntas) → **CERRADA** por P1. `FP-365` → **EJECUTADA**.
- **`FP-366`** (contador de `CALC-B-0001`) → **FIRMADA-EJECUTADA** por FIRMA 1.
- **`FP-362`** (contador de `CALC-0003-v3`/`v4`) → **FIRMADA-PARCIAL**: ejecutada para `v3`, abierta para `v4` (§3).
- **`NC-0071`** (nueva): `CALC-0003-v4` sin firma de contador; el contador cuenta la superada y no la vigente.
- **`NC-0072`** (nueva): una silla, no la fila entera — 442 RESULT siguen sin adoptar.
- **`NC-0073`** (nueva): ningún CALC corrió; este acto no midió nada.

## 7 · Lo que `C0-D` consume de aquí

1. **El patrón de cita, probado de punta a punta** — ya no es derivación en prosa: hay un consumidor real citando un RESULT GEN2, con los tres contadores movidos y `0 FAIL`. Copiarlo es copiar dos campos.
2. **Las dos varas, separadas y con nombre.** Al escribir una spec nueva: si el consumidor materializa con un grano distinto del de la corrida, no hay nada que declarar (el defecto lo resuelve); si se quiere una tolerancia de adopción propia, `tolerancia_adopcion` existe; si se quiere exigir la vara estricta, `NO-APLICA` lo dice.
3. **La segunda silla necesita un CALC, no otra cita** (`NC-0072`). C0-B §5.2 ya midió por qué: los demás CALC producen deltas, marginales y veredictos — ninguno es una probabilidad de conducta del motor, y ésa es la única ranura que el registro reconoce.

## 8 · A.13 — qué se examinó, y con qué

| veredicto | qué se examinó | comando |
|---|---|---|
| «el FAIL falso era real» | el caso medido de C0-B §5.4 | `_compara_result(0.04569409956405095, 0.045694, …)` → `False` |
| «adopta al grano y falla en el sexto decimal» | el mismo par, y `0.045695` | `_compara_adopcion` → `True` / `False` |
| «la llave vieja no puede bajar» | falsador con la llave revertida | `tests/test_corrida0.py` → `T-SSA-LLAVE` FALLA `antes=2 despues=2` |
| «315 y no 301» | 443 renglones de `resultados.tsv`, por `spec_id` y estado | conteo sobre la vista re-derivada |
| «WARN 443 → 442, 0 FAIL» | árbol completo, antes y después de la cita | `t35_repro()` sobre el árbol real, dos corridas |
| suite | `tests/check.py` completa | §9 |

## 9 · Suite

Línea base al arrancar (`main = 8b9f9d4`): **3 FAIL · 432 WARN**, `T35` con 212 WARN.
Al cerrar: **3 FAIL · 660 WARN**, `T35` con 443 WARN.

Los **3 FAIL son los mismos tres de la línea base** y ninguno está en el perímetro: `T06` (2, valores de Gini y confianza interpersonal divergentes en el corpus) y `T08` (1, siete reports sin mapa de evidencia). Deuda aceptada preexistente, declarada desde `MAESTRA38-N4`. **Este acto no agrega ni quita FAIL.**

El WARN se mueve 432 → 660, y el diff de agregados dice que se mueve **en dos tests y sólo dos**:

```
· T-REPRO: 212 -> 443    (+231)
· T22:      53 ->  50    (−3)
```

`T-REPRO` sube **por FIRMA 1, no por defecto**: firmar dos CALC mete 231 renglones nuevos al universo de `SELLADA-SIN-ADOPTAR` (+232 por la firma, −1 por la adopción de P4). **Es exactamente lo que «cuenta, no adopta» significa**, y es el mismo mecanismo que C0-B midió al simular la firma en memoria. `T22` baja 3 porque `FP-364`, `FP-365` y `FP-366` dejan de ser filas pendientes. Ningún otro test cambia ni una unidad.

## 10 · Higiene

- Todos los `git add` por ruta explícita, nunca `-A` ni `.`.
- `registro --escribe` corrido **una sola vez** tras las filas de firma, y una segunda tras la cita de P4 (P4 cambia la vista de `usos`); ninguna otra escritura de TSV.
- Nada se escribió fuera del perímetro que el encargo declaró.
- Ninguna spec congelada, ningún `sello.json` y ningún `resultados.json` se tocó.
- **El rótulo del acto se censó como `GEN2-PRIMERA-SILLA`, no como el que `cierre_acto.py` derivó de la rama.** La rama de esta sesión (`claude/tender-franklin-sh9430`) la impuso el arnés, no el acto, así que el rótulo que la Fase A propone (`TENDER-FRANKLIN-SH9430`) no nombra nada del programa. Se dice aquí en vez de registrar una etiqueta sin significado.
- `FP-362` se dejó en `ABIERTA -- FIRMADA-PARCIAL…` y no en `FIRMADA-PARCIAL` a secas: la mitad de `v4` sigue viva (`NC-0071`), y sólo un estado abierto mantiene la fila citando su encargo de origen — con el estado terminal, `T22` perdía la única fila que cubre el marcador de `GEN2-SPECS-SUCESORAS` y aparecía un `FAIL` nuevo. El estado abierto es además el honesto.
