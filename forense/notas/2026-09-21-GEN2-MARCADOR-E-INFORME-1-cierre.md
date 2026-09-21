# Nota de cierre · `ACTO GEN2-MARCADOR-E-INFORME-1`

21/sep/2026 · NUBE (`cloud_default`, corpus **NO** montado, cero microdato) · Opus 5 ·
sin sub-agentes · MODO ABIERTO · LOTE de cuatro piezas, un PR ·
`ADR-260921-GEN2-MARCADOR-E-INFORME-1-48d4-01`

Encargo archivado verbatim (A.3) con sello de cuerpo:
`forense/encargos/2026-09-21-GEN2-MARCADOR-E-INFORME-1.md`
(`d9c9fe577ea26b1284303f3ca62c2d7155cbc0b13fe109a536305482a517be0a`).
Raíz de acto `48d4` (4 hex del commit de 0-bis `48d40ba`).

---

## 1 · ARRANQUE (A.2, tres partes, salida cruda)

```
ENTORNO-DERIVADO = NUBE
senal-corpus: montado=NO archivos_examinados=0
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403, x_deny_reason=ausente, via_proxy=SI)
```

`ENTORNO-DERIVADO` = el que el encargo asigna. `data/raw` ausente y **no se
necesita**: este acto no abre microdato, todo lo que lee está en el repo.
Espejo: no se usó; toda cifra sale del clon, con el comando a la vista.

**SHA.** El encargo declara `55c8d57c`; `origin/main` al abrir era `55c8d57`
— **idéntico, re-derivado**. Al cerrar, `main` se había movido 12 commits
(`fc13cdc`) y se fusionó antes de la cascada, **sin conflicto**.

**Duplicado (0.c).** Cero coincidencias del rótulo en `git ls-remote --heads`,
`git worktree list` y los PR abiertos (uno solo, `#962`, de TUBERÍA).

**Precondición del encargo.** `PR #961` (piloto 3) **fusionado** a `main`
(`merged_at 2026-09-21T18:23:49Z`) → P1 y P4 corren. No se leyó nada de una rama
sin fusionar.

## 2 · Premisas verificadas

| premisa | rótulo | resultado |
|---|---|---|
| `_celdas_validadas()` teclea dos celdas-D y suma `n_cruce + n_persist` | `[LEÍDO]` | **CONFIRMADA** |
| 4 fallan / 10 pasan en `test_motor_gen2_explicito` | `[EJECUTADO]` | **CONFIRMADA** (4 fallan, 9 + 7 subtests pasan) |
| el mapa de olas vive en `_OLA_CALIBRACION_FIJA` | `[LEÍDO]` | **CONFIRMADA** |
| las tres fallas de transferencia son por la ola sin declarar | `[REPORTADO]` | **PARCIAL** — cierta para `test_10` y `test_11`; `test_08` tenía una **segunda** falla que la primera enmascaraba (→ `NC-…-48d4-01`) |
| pilotos 1 y 2: C2 1.47 y 1.57 pp, cobertura 18/20 | `[REPORTADO]` | **RE-DERIVADA E IDÉNTICA** (1.467 · 1.568 · 7/8 + 11/12 = 18/20) |
| piloto 3: MAE C2 3.41, encogida 1.95, ΔMAE 1.465 [0.439, 2.115], 3/15 vence | `[LEÍDO en rama]` | **RE-DERIVADA EN `main` E IDÉNTICA** |

**Premisa caída, y qué se hizo.** La de `test_08` toca **estado del repo**, no
qué se mide ni una firma de mesa: por v2.15 §2 el acto **replanteó, siguió y lo
declara**, en vez de parar. Re-sellar el snapshot habría sido PARO (b).

**«Ya hecho», repetido por objeto** sobre `forense/encargos/`, `forense/notas/`,
`canon/` y ramas remotas: la `NC` de la métrica la abrió el piloto 3, el informe
vigente era el v1.0 del 15/sep, y ningún acto hacía ninguna de las cuatro cosas.
Confirmado.

## 3 · Lo que se entregó

- **P0** — tres firmas asentadas verbatim, con verificación de existencia de
  universo declarado (414 + 185 filas, cero coincidencias).
- **P1** — `celdas_validadas` **73 → 92**. La métrica se deriva de toda celda-D
  con veredicto sellado; el veredicto **no** entra en el conteo; la escala se
  deriva contra el `margen_material` sellado y, si no se deriva, **la celda no
  cuenta**.
- **P2** — columna `prospectividad` publicada en el marcador, seis clases, orden
  desde los sellos. **20 PROSPECTIVA / 59 RETROSPECTIVA / 89 IDENTICO / 30
  SIN-EMISION / 16 EMITIDA-SIN-R / 0 ORDEN-NO-DERIVABLE**.
- **P3** — ola de `tramite.evasion_norma` = ENVIPE 2025, derivada de la spec
  sellada y cerrada por hash. `test_10` y `test_11` pasan.
- **P4** — `canon/informe-programa-v1_1.md`, con el módulo de auditoría completo
  y cada cifra con su comando o su `RESULT`.

## 4 · Lo que mesa debería mirar primero

**La cobertura del piso bajó con el tercer dominio, y eso es el hallazgo.** Con
dos pilotos era 18/20 = 0.90 y parecía una propiedad del método; con el tercero
es **26/35 = 0.743, Wilson95 [0.579, 0.858]**, porque el piloto 3 cubrió sólo
8 de 15. El intervalo nominal del piso resultó optimista en el dominio nuevo.
Un informe que sólo hubiera reportado los dos primeros habría vendido una
garantía que el tercero no sostiene.

**Y el segundo: apareció valor añadido y aun así no adjudica.** La interacción
encogida erra 1.946 pp contra 3.411 del piso, con ΔMAE sellado que no toca cero
y cobertura 14/15 — pero gana en 3 de 15 celdas contra las ≥12 que pide el
criterio. `FALSADOR-DEBIL`, `champion_actual: NINGUNO`, y el piso sigue siendo el
estimador adjudicado donde lo era. **Esto entrega la primera de las tres filas de
la regla de salida de θ** (`…-8a1f-06`): ningún retador con interacción venció al
piso. Faltan el lote ENIF 2024 y ENVIPE 2026, ninguno lanzado.

## 5 · Contador

`cuenta_gen2 = NO` — no sella corrida, no adopta, no adjudica, no re-adjudica.
Único contador movido: **`celdas_validadas` 73 → 92** (`python3
tools/tablero_programa.py`), y lo mueve contando lo que ya estaba adjudicado. El número **no se heredó**: esta rama medía 88 contra su base (`55c8d57`) y `ACTO GEN2-ARBITRO-MARGINALES-1` (`PR #971`) medía 77 contra la suya; `#971` fusionó primero y, tras traer `main`, la cifra se **re-derivó por comando** (`python3 tools/tablero_programa.py`): **35** cruce (esta rama) + **57** marginal (`#971` subió las marginales con error medido de 53 a 57). Los dos ejes se componen sin doble conteo.

## 6 · Estado de la suite

`python3 tests/check.py --baseline --parallel` → **LÍNEA BASE: VERDE**, sin
`FAIL` nuevos. **37 WARN nuevos** se listan como estado y **no adjudican**
(D-16); esta nota no asevera ningún total de WARN.
`python3 tools/verifica_sidecars.py` → **FAIL: 0 — VERDE** (el sello de cuerpo
del 0-bis sigue casando: la cascada se añadió **al final**, D-a6).

Las cuatro `NC` abiertas están en `forense/no-corrido.tsv` y, verbatim, en el
`## NO-CORRIDO / RESERVAS` del encargo archivado y en el cuerpo del PR.
