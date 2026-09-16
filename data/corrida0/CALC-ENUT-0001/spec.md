# `CALC-ENUT-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/ENUT-CUIDADO-spec-v1_0.md`
(**`prereg-caja-ENUT-CUIDADO`**, `sha256 6ee6cb62d5e7da6bf1fb750ec44fb25474cca7c8d37869d7faeab9ac6f6177bb`).
Este archivo no la sustituye: la resume en la forma que `spec.yaml` cablea.
Donde los dos digan cosas distintas, **manda la sellada**.

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1`, 15/sep/2026, **NUBE**, sobre `f5a5227`.
**Releva:** `CORR-0014` (ENUT2024) → **1** `RESULT`: `RES-0045`.
Consumidor: `milpa/tramite.yaml:familia.cuidado.recae_mujeres_40mas` (`R5.2`).

**CONGELADO en el COMMIT-1, en NUBE, antes de abrir un solo byte de microdato.**

---

## Qué mide

**Estimador de RAZÓN**, no proporción de un binario:

`A-R = Σ_h w_h·(horas de cuidado de mujeres 40+ del hogar) / Σ_h w_h·(horas de cuidado totales del hogar)`

| | |
|---|---|
| unidad | **HOGAR** (`LLAVEHOG`) |
| horas | `CUID_ESP_INT_HOG_CON_CP + CUID_INT_0A5_CON_CP + CUID_INT_6A14_CON_CP + CUID_INT_60MAS_CON_CP`, en `tvar_crea.csv` |
| mujer 40+ | `SEXO == '2'` ∧ `EDAD >= 40` |
| ponderador | `FAC_HOG` **de `tsdem.csv`**, unido por `LLAVEHOG` |
| diseño | `EST_DIS`/`UPM_DIS` de `tvar_crea.csv`, verificados constantes dentro del hogar |

## `FAC_HOG` no está donde la regla dice que está

`milpa/tramite.yaml:1036` declara el ponderador `FAC_HOG` y `:1038` sitúa el
universo en *«los 29 181 hogares de `tvar_crea.csv`»*. **`tvar_crea.csv` no
tiene `FAC_HOG`** — tiene `FAC_PER`, y son 60 columnas, las 60 que el FD
declara para `TVAR_CREA`. `FAC_HOG` vive en `tsdem.csv` **y** en `thogar.csv`.
Esta spec fija el archivo (`tsdem.csv`, precedente de `ACTO MAESTRA35-L7`) y
añade la guarda que nadie había corrido: `G-FAC-HOG-TSDEM-IGUAL-THOGAR`
compara los dos hogar por hogar. Si difieren, la elección de archivo cambia la
cifra y deja de ser un detalle de implementación.

## El recorte, medido antes de rotular

`CUID_INT_15A59` **queda fuera** (no tiene variante `CON_CP` en el FD);
`C-P-RESIDUO-15A59` mide su peso. La rama `SIN_CP` sale como
`C-P-SIN-CP` con delta con signo. Ninguna de las dos se elige sobre la marcha.
Hogares sin carga aportan `0/0` y **no se excluyen**: excluirlos cambiaría la
pregunta.

## Diseño

Se re-muestrean **UPM con reemplazo dentro de `EST_DIS`** y en cada réplica se
recalcula `Σw·num / Σw·den` — **numerador y denominador de la misma réplica**.
2 000 réplicas, `numpy.PCG64`, semilla `20260915`.

## Lo que NO hace

No abre microdato · **no escribe el medidor** (lo escribe el acto de CAJA) ·
no usa ENUT 2019 ni 2009 · no re-abre el `veredicto_acotado` de mesa
(`ACOTADA-EN-EDAD`, firma c1) · no repite el contraste por ocupación de
`Y1`/`Y5` · no adopta nada a `milpa/`.
