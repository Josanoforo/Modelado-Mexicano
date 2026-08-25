# Cierre — Paso 2 de `FP-149`: elección ciega pre-registrada (`ACTO ESCALAS-P2`)

**Fecha:** 25/ago/2026. **Entorno:** NUBE. **Firma:** ninguna nueva — ejecuta el verbatim de `ADR-173`/`FP-149`.

## 0 · Blindaje

Sesión fresca; no se abrió `forense/registro-llaves-identificacion-v1_0.md`, ningún archivo `CAL-G3`, la sección de llaves de `canon/estado-programa-v1_10.md`, ni el término del β medido. Insumo de P1 tomado por extracto de comando (`awk '/^## 3 ·/{flag=1} /^## 4 ·/{flag=0} flag' forense/notas/2026-08-25-escalas-p1.md`) — solo §3, sin abrir §0 ni §4 de esa nota.

## 1 · Qué hizo este acto

Commit 1 (`forense/escalas-eleccion-ciega-v1_0.md` §1-§3): pre-registro de reglas de decisión, cerradas antes de resolver caso por caso.

Commit 2 (`forense/escalas-eleccion-ciega-v1_0.md` §4): aplicación mecánica de esas reglas a las 15 filas `SUBDETERMINADA`. Resultado — **7 `ELEGIDA-CIEGA`** (proporción ponderada `[0,1]`, enlace identidad, ancladas en la θ pareja ya fijada de cada relación) **/ 8 `SUBDETERMINADA-PERSISTENTE`** (sin base dimensional en ninguna fuente pre-medición ni convención con ancla propia — declarado, no inventado).

Propagado a `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente.detalle`, campo `escala_derivada` de las 15 filas (único cambio al archivo — `git diff --stat` toca solo esas 15 líneas, verificado). `canon/gobernanza-v1_15.md`: `ADR-180`, cabecera 179→180. `canon/estado-programa-v1_10.md`: recifrado ADR (:27) y línea de escalas nueva en el recifrado L0 (:105).

## 2 · Tablero

`FP-149` recibe `ejecutada_en` (Paso 2, este acto). `FP-152` recibe el resultado: 7/15 `ELEGIDA-CIEGA`, 8/15 `SUBDETERMINADA-PERSISTENTE`. Este encargo (`forense/encargos/2026-08-25-ESCALAS-P2.md`) queda `CONSUMIDO`.

## 3 · Tests

`python3 tests/check.py --baseline` corrido antes y después de la edición (nunca `--freeze`).

## 4 · Lo que este acto NO hace

No relee `CAL-G3` — `G3.horizonte_temporal` es una de las 8 `SUBDETERMINADA-PERSISTENTE`, así que la condición de la propia firma (`ADR-173`) no se cumple; la relectura queda para un acto futuro y aparte (Paso 3), solo si esa condición llega a cumplirse. No toca signos ni magnitudes asignadas de ningún coeficiente. No toca el duelo, el sorteo ni el pool de 253 candidatas (`CONGELA-SORTEA`, dominio disjunto). No abre ninguna firma nueva. No toca `data/`, `corpus/`, ni ningún `resultado.tsv`. **CONTADOR: cero** — escalas son metadato del modelo, no medición sobre México.
