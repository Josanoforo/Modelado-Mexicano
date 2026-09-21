# Nota de cierre · GEN2-TRAMITE-FIRMAS-5

**Acto:** GEN2-TRAMITE-FIRMAS-5 · **Fecha:** 21/sep/2026 · **Entorno:** NUBE (papeleo) · **Rama:** `claude/tramite-firmas-5`

## Contador — antes / después

`python3 tools/corrida0.py status`:

| campo | antes | después |
|---|---|---|
| `N_resultados_gen2_adoptados_activos` | 72 | 72 (sin mover — ver hallazgo P3 abajo) |
| `N_corridas_selladas` | 143 | 143 (sin mover — F2 asienta `cuenta_gen2`, no sella corridas nuevas) |
| `N_resultados_gen2_sellados` | 24025 | 24025 |
| `N_resultados_gen2_pendientes_adopcion` | 12 | 12 |
| `celdas_validadas` (tablero) | 77 (cruce_vs_R=20) | 77 (cruce_vs_R=20, sin mover) |

Ningún contador se movió por este trámite. Es lo esperado: P2 asienta firma sobre corridas ya selladas (no crea corridas nuevas) y P3 adopta un piso cuya celda-D el marcador NO cuenta hasta un mecanismo de `tools/` que este acto no toca (NC-…-3619-01, ya abierta, lo predice explícitamente).

## Filas que cambiaron de estado

**NC cerradas (`forense/no-corrido.tsv`):** NC-0185, NC-0237, NC-0344, NC-0363, NC-0366, NC-0369, NC-0372, NC-0378, NC-0434, NC-0435, NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3-5870-01, NC-260921-GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3-5870-03, NC-260921-GEN2-TUBERIA-RES-LLAVE-1-5573-02, NC-260921-GEN2-RELEVO-TANDA-3-7bf5-01, NC-260921-GEN2-RELEVO-TANDA-3-7bf5-02.

**NC NO cerradas pese a mandato aparente del encargo (premisa que no se sostuvo — ver hallazgo):** NC-0425, NC-260921-GEN2-RELEVO-TANDA-3-7bf5-03.

**FP firmadas (`forense/firmas-pendientes.tsv`):** FP-408 (INFERIDO), FP-409 (DECLARADO, admisible sin reserva), FP-405 (texto verbatim de F5).

**FP nuevas creadas:** FP-260921-GEN2-TRAMITE-FIRMAS-5-958c-01 (acto de re-sello de FP-374, sin dueño, F6) · FP-260921-GEN2-TRAMITE-FIRMAS-5-958c-02 (firma F7, vocabulario `SIN-PISO-POR-DISEÑO`, FIRMADA; la tabla EDER queda como acto sucesor).

**`data/corrida0/decisiones.tsv`:** +11 filas `cuenta_gen2=SI` (P2, las once corridas de NC-0372) · +1 fila de adopción del piso C2 (P3) · +6 filas `cuenta_gen2=SI` para CALC-ENCIG-SERIE-CANAL-{2015,2017,2019,2021,2023} y CALC-ENCIG-ORIGEN-MOVIL-0001 (P5, hallazgo A.12).

**Celda-D:** `data/curacion-registro/celdas-d/GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml` — solo `champion_actual: NINGUNO → C2`; `veredicto` y `fecha_adjudicacion` intactos.

## Hallazgos de P5 (A.12: firma dada pero no asentada por fila)

1. **ENCIG-SERIE-Y-TENDENCIA-1** (ADR-260921-GEN2-ENCIG-SERIE-Y-TENDENCIA-1-852f-01, ya en `canon/gobernanza-v1_15.md`, es decir ya fusionado): la entrada de gobernanza dice `cuenta_gen2 = SI` para las seis corridas, pero `grep` de esos seis `CALC-*` en `decisiones.tsv` daba 0 filas antes de este acto. Asentadas ahora (P5).
2. **VALIDACION-INDEPENDIENTE-PILOTOS-1**: el encargo existe (`forense/encargos/2026-09-21-GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1.md`) pero no tiene entrada en `canon/gobernanza-v1_15.md` — no está fusionado/cerrado. No hay firma de `cuenta_gen2` que asentar todavía: es un acto de validación de resultados ya sellados (columna `validacion_independiente`, no `cuenta_gen2`), y su estado es NO-VERIFICABLE-AQUÍ hasta que cierre.
3. **L-DESDE-CAPTURAS-1 (PR #973)**: la cabecera del encargo GEN2-TRAMITE-FIRMAS-5 (§2, "ya ejecutadas") y su propio §6.2 asumen que `#973` ya ejecutó y midió los 28 slots. **Verificado por objeto (mcp github, `pull_request_read`): PR #973 está `state: open`, `merged: false`.** Esta es una premisa que no se sostuvo — logística/estado del repo, no una firma de mesa ni un estimando — así que el objetivo (cerrar NC-0425 y NC-…-7bf5-03 citando #973) NO es alcanzable hoy: **no se cerraron esas dos filas**. Quedan `ABIERTA`, y se declara aquí (D-19: bifurcación que cambia el entregable; no PARO porque el resto del acto sigue).

## Premisas que no se sostuvieron y cómo se replantearon

- **Dependencias Python ausentes en NUBE** (numpy/pandas/scipy, necesarias para `corrida0.py verify`): logística, reversible y barata (D-19/latitud) — se instalaron con `pip install` en esta sesión para poder correr `verify` sobre las once corridas de F2. No se tocó ningún dato ni código congelado.
- **`data/raw` ausente en NUBE**: esperado (ARRANQUE §3); las cinco corridas cuya reejecución exige microdato dieron `NO-EJECUTABLE` por `FileNotFoundError`, lo cual es **NO-VERIFICABLE-AQUÍ**, no un `NO-REPRODUCE`. La evidencia de REPRODUCE que sostiene F2 para las once corridas viene de `forense/replay-evidencia.tsv` (fechado 2026-09-19, CAJA con corpus montado), no de un re-verify en esta sesión.
- **PR #973 no fusionado**: ver hallazgo 3 arriba. No se cerraron NC-0425 ni NC-…-7bf5-03.

## PAROS

Ninguno de la lista cerrada de §7 se activó.
