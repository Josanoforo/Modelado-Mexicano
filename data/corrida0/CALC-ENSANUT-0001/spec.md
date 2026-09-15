# `CALC-ENSANUT-0001` — cara mecánica

Gobierna esta corrida la spec SELLADA `forense/prereg-caja/S7-L17-spec-v1_1.md`
(**`prereg-caja-S7-L17`**, `sha256 5b9b6055122b1ea14a1bd82503fd84889c7a064a08c04e443c07ae6866ac59d2`),
**Rama B** (primaria de esa pieza). Este archivo no la sustituye: la resume en
la forma que `spec.yaml` cablea. Donde los dos digan cosas distintas, **manda
la sellada**.

**Acto:** `ACTO GEN2-SPECS-DEMANDA-1` tanda 2, 15/sep/2026, **NUBE**, sobre `d117ef1`.
**Releva:** `CORR-0017` → **2** `RESULT`: `RES-0063`, `RES-0064`.
Consumidor: `milpa/tramite.yaml:salud.vacunacion.disponible_ensanut2024` (`R9.2`).

**CONGELADO en el COMMIT-1, en NUBE, antes de abrir un solo byte de microdato.**

---

## Por qué este CALC no trae spec humana nueva

`CORR-0017` es el único de los 19 cuya **capa humana de `D-15` ya estaba
sellada** — desde el 5/sep/2026, con dos versiones (`v1.0` y `v1.1`). Lo que
faltaba era **la capa ejecutable**. Escribir una segunda spec humana sería
duplicar un sellado, que `E.3` prohíbe. Este `spec.yaml` cablea la Rama B de
la `v1.1` y nada más.

## Qué mide

| | |
|---|---|
| payload | `adultos_ensanut2024_w_stata_stata__v2026_09_01` (`0fa8f443…`) |
| archivo | `adultos_ensanut2024_w.dta` |
| desenlace | bloque `a0927` — 20 variables `a0927{a..e}{1..4}`: **letra = razón, dígito = vacuna** |
| `RAZON_LOGISTICA` | `a0927a?` (no había vacunas) ∪ `a0927c?` (no estaba quien aplica) |
| ponderador | `ponde_f` |
| diseño | `estrato` · `est_sel` · `upm` |

## Las dos decisiones que esta spec toma y la sellada dejó abiertas

1. **La unidad de observación es la MENCIÓN, no la persona — y se dice.**
   `milpa/tramite.yaml:1041` declara el universo como *«254 menciones "Sí"
   (179 personas distintas)»*. `ponde_f` es un ponderador **de persona**:
   aplicado a filas de mención, una persona con dos menciones entra con su
   peso **dos veces**. La primaria reproduce ese universo (es el de la cifra
   GEN1) y `B-P-PERSONA` mide la misma proporción **colapsando a persona**,
   con `B-DELTA-MENCION-VS-PERSONA` con signo. Ninguna de las dos se elige
   sobre la marcha.
2. **A.15 contra el inventario VIGENTE, no el que la sellada citó.** La `v1.1`
   verifica el bloque `a0927` contra `inventario-reactivos-descargas-mx-**v1_1**`;
   `A.15(a)` exige el vigente. Re-verificado aquí contra **`v1_2`**: las 20
   variables existen en `adultos_ensanut2024_w.dta` con `sha256_12 0fa8f4436fa4`
   — el mismo del manifiesto — y su `texto_reactivo` confirma el mapeo
   letra=razón/dígito=vacuna de `ADR-357`/`FP-326`. **El negativo no cambia de
   signo; lo que cambia es que ahora está verificado contra el inventario que
   manda.**

## Lo que NO hace

No abre microdato · **no escribe el medidor** (lo escribe el acto de CAJA) ·
**no mide la Rama A** (ENNViH — la sellada la deja condicionada a §0.3, sin
resolver) ni la **Rama C** (adolescentes): ninguna de las dos tiene `RESULT`
en `CORR-0017` · no escribe spec humana nueva · no adopta nada a `milpa/`.
