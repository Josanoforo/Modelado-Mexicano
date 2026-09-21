# ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3 · nota de cierre · 21/sep/2026

**El piloto 3 corrió y tiene veredicto: FALSADOR DÉBIL.** Dos corridas selladas (`N_corridas_selladas` 119 → 121), `cuenta_gen2 = SI` en las dos, `adoptados_activos` 71 → 71 (no adopta), `celdas_validadas` 73 → 73 (ver §6). Universo: pagos ordinarios del servicio de luz (`N_TRA == 01`), unidad TRÁMITE/evento, ENCIG 2025; escala proporción en [0,1] y pp.

## 0 · Sesión, entorno, base

Sesión **nueva** (`953594cb`), Opus, CAJA (`ENTORNO-DERIVADO = CAJA`, corpus montado 420 archivos, `sin_variable`, red 200). No es `165ce648`, ni la de `#944`, ni `pc0-77`, ni la de `#951`; sin diseños A/B ni careo en contexto (F3 cumplida). Worktree `mm-piloto3-c23-v13` sobre `33d97e12` (= SHA del encargo); `data/raw` enlazada y `raices.local.yaml` copiada del clon padre. Guard 0: base 202 detrás → ff; 0 ramas remotas, 0 PR, 0 worktrees con el rótulo. 0-bis `3619d28b` + sidecar de cuerpo (`7d82e141…c6e4b3`, igual al archivo recibido). `main` se movió 17 commits (`#955`) durante el acto: fusionado en `ea447470`, sin conflicto, sin tocar los CALC.

**Ejecución previa declarada (§3 del encargo, E.5):** `#951` corrió el medidor sobre el payload real de 2025 en proceso (una variable) y `corrida0` descartó la salida; procedimiento y semilla no cambiaron, así que la corrida de hoy no es «un primer resultado distinto».

## 1 · P0 — antes de abrir

- Sidecar de la spec v1.1 `62d8d07d…` OK; `verifica_sidecars` FAIL 0.
- `pytest tests/test_piloto3_v11.py tests/test_piloto3_v13_conducto.py` → **14 passed**, incluida la de oro sobre 2023.
- `preflight EMISIONES-0002` → **VERDE**, `encig25_base_datos_csv` **COINCIDE** (`47daf2f7…`, 37 624 925 B). `preflight ADJUDICACION-0001` → **BLOQUEADO exactamente** por los cuatro de `emisiones_resultados` / `emisiones_sello` (ausente + no commiteado), y por nada más.
- Censo de rastros: 0 `ejecucion.json`/`resultados.json`/`sello.*` de los dos CALC en ningún checkout de `/home/pc0`; en disco (`-newermt 2026-09-21`) sólo copias versionadas en otros worktrees; `git ls-files` → sólo la celda-D. **Sin rastro de 2025 abierto por dos variables.**
- `secuencia_commits` del `spec.yaml` de ADJUDICACION y el encargo coinciden (commit_2 → 3a → 3 → cierre 60-96).

## 2 · P1 — COMMIT-2, emisiones selladas

`corrida0 run CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → SELLADO al primer intento. Corrida `CALC-GOB-DIGITAL-EXE-EMISIONES-0002--bfc2e4b840e3`, 565 RESULT, `script_blob 05d4c205…`, `spec_yaml c51cb15c…`. `verify` → REPRODUCE/IDENTICO; `verifica_aislada.py` (proceso nuevo) → REPRODUCE/IDENTICO; asiento en `forense/replay-evidencia.tsv` antes de publicar; `registro --verifica --escribe --lote` → corridas +1 (`cuenta_gen2 = SI`, `envuelto_legacy = SI` — el control `c2_compuesto_resultados` arrastra `milpa/tramite.yaml`), resultados +565. Commit `b136d764` (sellado) + `d2488a98` (vista); `git ls-remote` confirmó `d2488a98` en `origin` y `sello.json` presente en la rama remota **antes** de P3.

Universo 2025: 124 314 filas de eventos → 20 203 con diseño válido = universo (189 con `P7_3` excluida; 20 088 completos; 0 sin demografía). Residuo de edad fuera del universo: 115 trámites (masa 755 243).

**Código 97 (FP-399):** `S2-EDAD-97-N = 1` (masa 1 381), `S2-EDAD-98-N = 114`, `S2-EDAD-99-N = 0`; banda 60+ n = 4 476; fracción 97 en 60+ = **0.000223 < 1 %** → `S2-RESERVA = SIN-RESERVA`. **RESERVA-S2 no dispara.**

**Nulos emitidos, por familia de id (40, exactamente los declarados):**

| familia | n null | causa |
|---|---|---|
| `-C1A-P-IC-LO` | 16 | `C1A-IC-CAUSA = SIN-REPLICAS-SELLADAS-2023` (IC de C1a NO-DERIVABLE por diseño) |
| `-C1A-P-IC-HI` | 16 | ídem |
| `-60-96-<esc>-CONTROL-C2COMP-P` | 4 | control de la casa rotulado `-60-X-`; recuperado en §5 como aritmética |
| `-60-96-<esc>-C2-VS-CONTROL-ABS` | 4 | arrastre del anterior |

0 no finitos. Todo lo demás (marginales, C2/S½/Sλ punto e IC, C1b, deltas, soportes, S2) no nulo.

## 3 · P2 — compuerta sobre lo sellado

Los 9 `-MARGINAL-…-P` (ALL 0.6729; edad 0.7518 / 0.7747 / 0.6692 / 0.4758; escolaridad 0.3896 / 0.5652 / 0.6786 / 0.8123) y los puntos de candidato de las 16 celdas (C1A, C1B, C2, S-MEDIO, S-LAMBDA: 80 ids `-P`) son **todos no nulos**. La rama NaN de `adjudicacion.py:185,188-189` es inalcanzable: se siguió.

## 4 · P3 y P4 — COMMIT-3a y COMMIT-3

**COMMIT-3a** `704d5289`: dos líneas `sha256:` (`a97fee3e…` para `resultados.json`, `c04598b2…` para `sello.json`) bajo `emisiones_resultados` y `emisiones_sello` del `spec.yaml` de ADJUDICACION; `git diff --numstat` = `2 0`; `preflight` → **VERDE** (7/7 COINCIDE). Empujado antes de correr.

**COMMIT-3** `corrida0 run CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` → SELLADO. Corrida `--704d52894c2f`, 349 RESULT, **0 null** (los 174 `permite_no_estimable` no se usaron), `C2-REPRODUCE-MAX-ABS = 0.0`. `verify` y aislado → REPRODUCE/IDENTICO; asiento y registro (+349) en `e9c244bd`.

### 4.1 · Veredicto, con las palabras de la spec (v1.1 §4.2)

- Soporte 2025: **15/15 PUNTUADA** (`SOPORTE-FALLAN = 0`, `SOPORTE-GLOBAL = CON-SOPORTE`); 18-29 × HASTA-PRIMARIA FUERA-DE-SOPORTE ex ante (n₂₀₂₅ = 67). Ninguna PUNTUADA perdió su IC de R (`R-B-VALIDAS = 10000` en las 16).
- **Nadie vence.** Sλ vence a C2 en **3/15**, S½ en **3/15** (umbral ¾ = 12); 12 INDECIDIBLE cada uno; 0 celdas donde el retador pierde. `S-LAMBDA-GANA = NO`, `S-MEDIO-GANA = NO`.
- Lectura secundaria: MAE vs R — **C2 3.411 pp · Sλ 1.946 · S½ 2.310** · C1a 10.654 · C1b 10.519. ΔMAE = MAE(C2) − MAE(j): **Sλ 1.465 pp, IC95 [0.439, 2.115]; S½ 1.101 pp, IC95 [0.256, 1.484]**. Los dos IC admiten > 0.5 pp, así que «corroborada» no cabe.
- **→ FALSADOR DÉBIL** (`RESULT-GOB-EXE15-ADJ-2025-B-BIS = FALSADOR-DEBIL`). Sin marca RESERVA-S2. Alcance (A.10): C2 sigue adoptado en DIN y TRA; esto limita sólo a gobierno_digital/luz, edad × escolaridad, ENCIG 2025.

### 4.2 · Por celda (R con IC95; punto y |error| en pp por candidato)

| celda | n₂₀₂₅ | soporte | R (IC95) | C2 | Sλ | S½ | Sλ vs C2 | S½ vs C2 |
|---|---|---|---|---|---|---|---|---|
| 18-29 × HASTA-PRIMARIA | 67 | FUERA-DE-SOPORTE-EX-ANTE | 0.3261 [0.1860, 0.4795] | 0.4845 (15.84) | 0.5563 (23.01) | 0.5369 (21.08) | NO-PUNTUADA | NO-PUNTUADA |
| 18-29 × SECUNDARIA | 417 | PUNTUADA | 0.5988 [0.5211, 0.6729] | 0.6568 (5.80) | 0.6297 (3.09) | 0.6426 (4.38) | INDECIDIBLE | INDECIDIBLE |
| 18-29 × MEDIA-SUPERIOR | 934 | PUNTUADA | 0.7113 [0.6648, 0.7549] | 0.7566 (4.53) | 0.7295 (1.82) | 0.7388 (2.75) | VENCE | VENCE |
| 18-29 × SUPERIOR | 1388 | PUNTUADA | 0.8448 [0.8134, 0.8740] | 0.8644 (1.95) | 0.8422 (0.27) | 0.8461 (0.13) | INDECIDIBLE | INDECIDIBLE |
| 30-44 × HASTA-PRIMARIA | 286 | PUNTUADA | 0.5418 [0.4495, 0.6316] | 0.5163 (2.55) | 0.5098 (3.19) | 0.5041 (3.77) | INDECIDIBLE | INDECIDIBLE |
| 30-44 × SECUNDARIA | 1380 | PUNTUADA | 0.6311 [0.5935, 0.6684] | 0.6848 (5.37) | 0.6420 (1.08) | 0.6558 (2.47) | VENCE | VENCE |
| 30-44 × MEDIA-SUPERIOR | 1977 | PUNTUADA | 0.7490 [0.7178, 0.7794] | 0.7792 (3.02) | 0.7680 (1.90) | 0.7756 (2.66) | INDECIDIBLE | INDECIDIBLE |
| 30-44 × SUPERIOR | 3365 | PUNTUADA | 0.8759 [0.8541, 0.8953] | 0.8786 (0.26) | 0.8790 (0.30) | 0.8765 (0.06) | INDECIDIBLE | INDECIDIBLE |
| 45-59 × HASTA-PRIMARIA | 630 | PUNTUADA | 0.4142 [0.3566, 0.4736] | 0.3856 (2.86) | 0.4446 (3.04) | 0.4287 (1.45) | INDECIDIBLE | INDECIDIBLE |
| 45-59 × SECUNDARIA | 1529 | PUNTUADA | 0.6000 [0.5578, 0.6403] | 0.5610 (3.90) | 0.5785 (2.15) | 0.5717 (2.82) | INDECIDIBLE | INDECIDIBLE |
| 45-59 × MEDIA-SUPERIOR | 1646 | PUNTUADA | 0.6777 [0.6417, 0.7124] | 0.6749 (0.28) | 0.6674 (1.03) | 0.6667 (1.09) | INDECIDIBLE | INDECIDIBLE |
| 45-59 × SUPERIOR | 1994 | PUNTUADA | 0.8012 [0.7739, 0.8269] | 0.8097 (0.85) | 0.8105 (0.93) | 0.8129 (1.17) | INDECIDIBLE | INDECIDIBLE |
| 60-96 × HASTA-PRIMARIA | 1294 | PUNTUADA | 0.3426 [0.3032, 0.3826] | 0.2198 (12.28) | 0.2709 (7.17) | 0.2489 (9.37) | VENCE | VENCE |
| 60-96 × SECUNDARIA | 872 | PUNTUADA | 0.3977 [0.3457, 0.4527] | 0.3645 (3.33) | 0.4161 (1.84) | 0.4042 (0.64) | INDECIDIBLE | INDECIDIBLE |
| 60-96 × MEDIA-SUPERIOR | 1002 | PUNTUADA | 0.5074 [0.4579, 0.5582] | 0.4823 (2.51) | 0.5158 (0.84) | 0.5031 (0.44) | INDECIDIBLE | INDECIDIBLE |
| 60-96 × SUPERIOR | 1307 | PUNTUADA | 0.6398 [0.6007, 0.6778] | 0.6563 (1.65) | 0.6451 (0.53) | 0.6542 (1.44) | INDECIDIBLE | INDECIDIBLE |

Las tres celdas donde los retadores vencen son las mismas para Sλ y S½ (18-29 × MEDIA-SUPERIOR, 30-44 × SECUNDARIA, 60-96 × HASTA-PRIMARIA); Sλ y S½ no se separan (ni «cuánto encoger» queda adjudicado).

### 4.3 · EXPLORATORIO — NO ADJUDICA
La celda con mayor error del piso es 60-96 × HASTA-PRIMARIA (C2 12.28 pp por debajo de R; Sλ recorta a 7.17). Es una lectura sobre lo sellado, no pre-registrada, y no cambia el veredicto.

## 5 · P5 — cierre

**Aritmética derivada (control 60-96, `commit_3_cierre_control_60_96`):** |`RESULT-GOB-EXE15-2025-60-96-<esc>-C2-P` − `RESULT-C2COMP-ADOPTA-ENCIG2025-LUZ-EDADXESCOLARIDAD-60-X-<esc>`|, entre dos sellados, **ARITMÉTICA DERIVADA**, no RESULT: HASTA-PRIMARIA 0.2197701594 vs 0.2210710547 → **1.30e-3**; SECUNDARIA 0.3644720316 vs 0.3634622446 → **1.01e-3**; MEDIA-SUPERIOR 0.4823104908 vs 0.4817123548 → **5.98e-4**; SUPERIOR 0.6563449744 vs 0.6567614563 → **4.17e-4**. Del mismo orden que los 12 `-C2-VS-CONTROL-ABS` sellados (máximo 1.30e-3): el control no delata desvío del piso.

**Celda-D** `GOB.gobierno_digital.encig2025.edad_x_escolaridad`: `unidad_objetivo: evento` (FP-393 a), `veredicto: FALSADOR-DEBIL`, `estado_decidibilidad: PUNTUADA`, `margen_material: 3.411216`, `resultado` por candidato, `momentos_holdout_refs` a las dos corridas, estampas `2026-09-21` / `704d5289`, `champion_actual: NINGUNO` — **este acto no adopta**. `tests/test_celdas_d.py` → 6/6 validan.

**Marcador** re-derivado por comando (`marcador_segmento.py --escribe`): **sin diff**. El par `…::edadxescolaridad` sigue `RESERVADA` porque la herramienta sólo levanta la reserva cuando la celda-D trae `champion_actual: C2`; un estado `CONSUMIDA-POR-PILOTO` exige más de 10 líneas en `tools/` (incluida la aserción «emitir no consume») y una decisión de vocabulario: se ensayó, se revirtió sin commitear, y va a mesa (`NC-…-3619-01`). La premisa «el par deja de estar RESERVADA» era `[SUPUESTO]` y cayó por logística de la herramienta, no por el dato.

**Contadores:** `N_corridas_selladas` 119 → 121 · `adoptados_activos` 71 → 71 · `celdas_validadas` 73 → 73 (`cruce_vs_R` 20; la métrica cuenta desde el marcador y dos CALC nombrados, no desde celdas-D adjudicadas; `NC-…-3619-02`).

**Pisada ajena en las vistas (medida columna por columna contra HEAD, excluyendo filas propias):** el `registro --verifica --escribe` del COMMIT-2 re-derivó desde el estado de `main` cambios que ningún acto había proyectado: `cuenta_gen2` 17 corridas (`NO`/`PENDIENTE-DE-MESA` → `SI`, todas con fila en `decisiones.tsv`) y `motivo_cuenta_gen2` 18; `fuente_replay` de `CALC-DIN-CREDITO-PISOS-ENIF2021-0001` (→ su asiento aislado de `#943`); `funciones_dependencia`/`camino_linaje` de ENCRIGE-CARGA y ENVIPE-RES0028 (42 filas), `origen_numerico` ENVIPE-RES0028 (11); renumeración `RES-0175…0211`/`CORR-0087` de filas legado; `usos.tsv` gana las columnas `via_relevo`/`pin_de_mesa` (0 filas de contenido ajeno cambian). Ninguna es de esta sesión; se nombraron en la nota como pide `NC-0094`. El del COMMIT-3 sólo tocó `fuente_replay` de la fila propia de EMISIONES.

**Defecto adyacente (≤ 10 líneas, fuera de los CALC):** `tools/corrida0.py::_leer_tsv_derivado` reventaba con `field larger than field limit (131072)` por el `resultados_ids` de 209 856 B de `CALC-DIN-CREDITO-PISOS-ENIF2021-0001` (`#943` subió el tope en `relevo_usos`/`tablero`, no aquí): `csv.field_size_limit(sys.maxsize)` + comentario, 5 líneas, `d2488a98`.

**FP/NC por objeto:** `ejecutada_en` de FP-389, FP-399, FP-400 (llenas) y FP-407, FP-…-a6f5-01 (ampliadas). Cerradas 14 NC (NC-0356, 0367, 0407, 0408, 0409, 0451–0454, …-a6f5-01…05); re-apuntadas NC-0410 y NC-0432 a mesa; nuevas `NC-…-3619-01` (marcador) y `-02` (celdas_validadas).

## 6 · Para mesa — una página

**Qué se probó.** Que la interacción edad × escolaridad en «pagar la luz por canal digital», estable en ENCIG 2021 y 2023, se transporta a 2025 mejor que un piso sin interacción (C2: marginales de 2025 compuestas en logit). Dos retadores pre-registrados la transportan: S½ (media interacción de 2023) y Sλ (interacción promedio 2021-2023 encogida por λ = 0.894).

**Qué salió.** Nadie vence: cada retador gana sólo 3 de 15 celdas y en 12 el duelo es indecidible dentro del IC de R. Pero en promedio ambos están más cerca de R que el piso (ΔMAE 1.5 y 1.1 pp con IC que excluyen cero). **Veredicto pre-registrado: FALSADOR DÉBIL.** El piso C2 no fue vencido y, por A-bis 6, su adopción o veto es de mesa — este acto no lo decide.

**Con qué certeza.** 15 celdas con n de 286 a 3 365 trámites; IC por bootstrap UPM réplica por réplica (10 000); reserva respetada por el orden del diff (emisiones en `origin` antes del árbitro); reproducción aislada IDÉNTICA de las dos corridas; una sola lectura, sin relanzar.

**Qué NO significa.** Es un cruce de **un** trámite (pago de luz), no «gobierno digital» ni confianza en el Estado. El +11 pp de nivel entre olas (premisa del encargo) **no queda explicado** aquí: el piso lo absorbe por construcción. Canal responde a bancarización y cobertura antes que a preferencia; el universo es quien paga luz a su nombre (sub-representa hogares donde otro paga). Peligroso leído simplista: «los mayores con poca escuela no adoptan lo digital» como rasgo — puede ser oferta (A-bis 1). El piloto predice el patrón, no identifica su causa.

**Una línea para la regla de salida de θ:** ¿algún retador con interacción venció al piso? **NO** (3/15 < 12 para los dos; falsador débil).

**Decisión que queda en su mesa (`NC-…-3619-01`):** (a) adoptar el piso C2 no vencido — recomendada; el marcador levanta la reserva solo — · (b) vetar y encargar un estado `CONSUMIDA-POR-PILOTO` · (c) dejar RESERVADA como registro del cruce gastado.

## 7 · Perímetro tocado
Propio: `ejecucion.json`/`resultados.json`/`sello.*` de los dos CALC · 2 líneas del `spec.yaml` de ADJUDICACION · celda-D GOB · filas propias en `corridas.tsv`/`resultados.tsv`/`replay-evidencia.tsv` · `forense/analisis/gen2-celda-d-piloto-3-commit-2-3-v1_3/` · `firmas-pendientes.tsv` (ejecutada_en) · `no-corrido.tsv` · esta nota · cascada. Adyacente declarado: `tools/corrida0.py` (5 líneas). No tocado: `medidor.py`, `adjudicacion.py`, spec humana, sidecar, `tools/marcador_segmento.py` (ensayo revertido), tests, otros cruces de ENCIG 2025 (siguen RESERVADA).
