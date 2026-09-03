# ENCARGO · ACTO CAL-G3-PUNTUAL — llaves 3 de 3 y el primer coeficiente propio

> | | |
> |---|---|
> | **ARCHIVO** | `2026-08-24-CAL-G3-PUNTUAL.md` |
> | **NOMBRE ESTABLE** | **`cal-g3-puntual-encargo`** |
> | **ESTADO** | **CONSUMIDO** — 24/ago/2026, rama `acto/cal-g3-puntual` |
> | **SALIDA** | `forense/notas/2026-08-24-cal-g3-puntual-cierre.md` (spec Commit 1 + corrida Commit 2) |

Redactado por dirección, 24/ago/2026. Firmas que ejecuta: respuesta 2 de mesa («…no está descargado, la descargamos y ya» — plan B solo si la búsqueda se agota) + FP-118. ENTORNO UBUNTU (microdato + red para el espejo académico). NO NUBE. Modelo: Opus.

⛔ **ORDEN:** tras fusionar `RECENSO-DISEÑO-2` (usa su fila ENNViH) — verificado al arrancar: `f154fd9` (PR #321) en `main`, `origin/main` al día.

**CONTADOR DECLARADO:** llaves ejercidas 2 → 3 (`CAL-G3` pasa de `SELLADA_NO_EJERCIDA` a `EJERCIDA_ACOTA`). El coeficiente queda **PROPUESTO**, no escrito en `milpa/procedencia.yaml`.

## Resumen de ejecución

1. **PASO 0** — AGOTADO (universos a+b+c, con conteos). Reproduce, independientemente, el hallazgo ya escrito por `RECENSO-DISEÑO-14` en `data/diseno-muestral.yaml:412-439`: ENNViH no trae UPM/estrato de diseño en ningún `.dta` ni documento; el espejo académico (RAND/ICPSR, 3 URLs) responde 403 real (AWS WAF, confirmado con sandbox de red deshabilitado).
2. **PASO 1** (Commit 1) — spec B-bis congelada: θ = `pr02` (horizonte temporal declarado, módulo `PR`, ordinal 1-7, olas 2-3), desenlace = `cr27` (tiene ahorros, binario), par intra-persona por primeras diferencias, ponderador `fac_3b`, varianza HC1/MAS + sensibilidad bootstrap-hogar (plan B firmado, PASO 0 = AGOTADO).
3. **PASO 2** (Commit 2) — corrida: N=6,305, θ=+0.0146, IC95%=[+0.0047,+0.0245] (HC1/MAS), IC95%=[+0.0056,+0.0248] (bootstrap-hogar). Signo opuesto al asignado (−0.60); escalas sin enlace. Veredicto: `EJERCIDA_ACOTA`.

## Cierre

- `forense/registro-llaves-identificacion-v1_0.md` — fila `CAL-G3`, contador `2→3`.
- `forense/firmas-pendientes.tsv` — fila añadida.
- `canon/estado-programa-v1_10.md` — línea de llaves y recifrado `154→155`.
- `canon/gobernanza-v1_15.md` — `ADR-157`.
- Suite: 19 FAIL preexistentes sin cambio; sin FAIL nuevo en T02/T15/T16 atribuible a este acto.
- Perímetro respetado; no se tocó `milpa/procedencia.yaml`, `hitoD-preregistro`, ni `diseno-muestral.yaml` (solo lectura).
- Push/PR: **no realizado** — trabajo dejado en rama local para revisión del supervisor, por instrucción explícita.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-24-CAL-G3-PUNTUAL.md" canon/gobernanza-v1_15.md` → 2: citado bajo ADR-157 en canon/gobernanza-v1_15.md, con lenguaje de ejecución (archivado/ejecutado) en el bloque correspondiente. Marca ausente en el archivo era defecto de trámite, no evidencia de no-ejecución.
