# `CALC-TRIADA-0001` — espejo del contrato TRIADA (`ACTO GEN2-F5-TRIADA-CALC`, P1)

**Qué es.** La cara humana de `spec.yaml`. Este CALC **ejecuta** la spec
sellada `forense/prereg-duelo-v2/F5-contrato-triada-spec-v1_1.md`
(`sha256 db6b24c579e72dc705c772200ca2c4066bd9708cc6c06c85c5101d56b081b4f5`,
verificada contra `origin/main = c439065`); **no la enmienda, no la
reinterpreta y no la edita**. Todo lo que sigue es copia citada por hash de
esa spec o de los productos sellados de los `ENCARGO 1/5 · 2/5 · 3/5 · 4/5`.
Donde la spec dice una cosa y este documento parecería decir otra, gobierna
la spec sellada.

**Acto:** `GEN2-F5-TRIADA-CALC` (`ENCARGO 5/5`), NUBE, 10/sep/2026.
**Base:** `origin/main = c439065` (merge de `PR #680`,
`ACTO GEN2-R-COMPLETA-MARCO`). **Cero microdato, cero red, cero llamadas
nuevas a ningún modelo.** Todos los insumos son archivos ya versionados.

---

## 0 · Compuerta, por producto (verificada antes de escribir esta spec)

| # | Producto exigido por el encargo | Ruta | `sha256` en `origin/main` |
|---|---|---|---|
| 1 | extractor L v1.3 | `tools/extrae_l_v1_3.py` | `ecfbd8491f9b353d9eebdb25f0afa6eddf4f0d3082cff50c3db7d8f5ddd8ff5e` |
| 1 | manifiesto de extracción | `forense/prereg-duelo-v2/manifiesto-extraccion-L-v1_3.json` | `a1e5d609fe0044eef44d3365b308004daeaa8d511f4692464b422e1296e75809` |
| 2 | spec TRIADA sellada | `forense/prereg-duelo-v2/F5-contrato-triada-spec-v1_1.md` | `db6b24c579e72dc705c772200ca2c4066bd9708cc6c06c85c5101d56b081b4f5` |
| 3 | `UR` congelado | `forense/prereg-duelo-v2/universo-triada-v1_4.tsv` | `840fc68ce7261686426221effbf9df313ef17e2876fa6345b3c00589bab80f80` |
| 3 | árbitros R sellados | 14 `CALC-R-*` citados en la columna `fuente_R` | 14/14 con `resultados.json`+`sello.json`+`sello.sha256`+`spec.yaml` |
| 4 | snapshot M congelado + firewall por celda | `forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json` | `b53ac6d51d1b50ce929fdf1b3e14b124c11db39fb216a15d7073a287ed3f065c` |

**4/4 cumplida.** Ningún sustituto improvisado.

---

## 1 · `U0` — copiado, no re-derivado

Las 14 celdas del marco `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv`,
tal como `F5-contrato-triada-spec-v1_1.md` §1.1 las fija:

```
CIV-M-01 · ENVIPE · 2012      CIV-M-02 · ENVIPE · 2013
CIV-M-04 · ENVIPE · 2015      CIV-M-10 · ENVIPE · 2021
CIV-M-12 · ENVIPE · 2023      CIV-M-13 · ENVIPE · 2024
DIN-M-01 · ENNViH/MxFLS · 2002 (ola 1)
FAM-M-01 · ENIF · 2018
FAM-M-05 · ENIGH · 2016       FAM-M-06 · ENIGH · 2018       FAM-M-07 · ENIGH · 2020
TRA-M-02 · ENCUCI · 2020      TRA-M-03 · ENCIG · 2013       TRA-M-07 · ENCIG · 2021
```

## 2 · `UR` — congelado en 14/14, leído del sidecar

`F5-contrato-triada-spec-v1_1.md` §1.2 cerró `UR` en **14/14** tras
`GEN2-R-COMPLETA-MARCO`, con sidecar vigente `universo-triada-v1_4.tsv`.
Este CALC **lee** ese sidecar (columna `en_UR`); no lo recalcula, no lo
amplía y no lo reduce. Prohibido mover `UR` después de observar errores.

## 3 · Regla para `U3` — la única puerta de entrada (§1.3, verbatim)

```
U3 = { i ∈ UR : L_SOLO tiene punto válido en i
              ∧ L_CORPUS tiene punto válido en i
              ∧ M tiene punto válido en i
              ∧ i no está CONTAMINADA-POR-OBJETIVO }
```

- **Punto válido de `L_SOLO`/`L_CORPUS`:** agregado por celda (§5 de este
  documento) sobre réplicas cuyo `valor_extraido` produjo el **extractor
  v1.3 validado**. Una celda sin ninguna réplica `EXTRAIBLE` no tiene punto.
- **Punto válido de `M`:** punto del snapshot M v1.0 sellado con
  `estado_M = EMITE`.
- Una celda **no** sale de `U3` porque su error sea grande. El filtro es
  sobre insumo disponible/válido, nunca sobre el resultado.

## 4 · Los tres contendientes — y quién no lo es

`L_SOLO`, `L_CORPUS`, `M`. **`R` es árbitro, nunca contendiente. `B` es
diagnóstico, nunca contendiente** (§7). No hay cuarto.

## 5 · Regla de agregación de `L` — heredada sin cambio

`k = 8` réplicas por celda × variante. Agregado por celda = **mediana** de
las réplicas con `valor_extraido` `EXTRAIBLE`
(`forense/prereg-duelo-v2/pipeline-L-adv1-m2.py::agregar_continua`, la misma
que `F5-duelo-contemporaneo-spec-v1_0.md` §5 cita y que `CALC-DUELO-0001`
aplicó). **La mediana ya estaba elegida antes de este contrato y este acto
no la reabre.** Una réplica `NO-EXTRAIBLE` o `AMBIGUA` cuenta en cobertura:
no se sustituye por cero ni se descarta en silencio. Las 8 réplicas de una
celda **no** son 8 tareas independientes.

## 6 · Snapshot `M` y árbitros `R`

- `M`: un punto por celda del snapshot sellado de `ENCARGO 4/5`. **`M` no se
  calibra, no se retoca y no se re-emite en este acto.**
- `R`: punto árbitro por celda con su `EE`, leído de los `CALC-R-*` sellados
  citados por el sidecar. **`R` no se completa ni se re-computa aquí.**

## 7 · Métrica — MAE en puntos porcentuales (§3)

```
error_X,i = |predicción_X,i − R_i|   (×100, escala `binaria` de las 14 celdas)
MAE_X     = media(error_X,i)  sobre el MISMO U3, X ∈ {L_SOLO, L_CORPUS, M}
```

## 8 · Δ pareados — las tres, ninguna omitible (§3)

```
Δ(A,B) = media(error_A − error_B)     — negativo favorece A
```

1. `Δ(L_CORPUS, L_SOLO)` 2. `Δ(M, L_SOLO)` 3. `Δ(M, L_CORPUS)`

Las tres sobre el **mismo** `U3`. Si no lo fueran, el cómputo para; no se
improvisa un universo por par.

## 9 · Bootstrap y banda (§4)

- **mismas celdas de `U3`** en cada réplica;
- **mismos índices de remuestreo para los tres contendientes** — un solo
  vector de índices por réplica, reutilizado por las tres pareadas;
- **10,000 réplicas**; **`seed = 42`** (`FP-168`, heredada — no se introduce
  una segunda semilla); **IC95** por cuantil tipo 7
  (`scoring-adv1-m3.py::_cuantil_7`), con
  `generar_indices_bootstrap`/`derivar_seed_scope` reutilizados sin editar;
- **banda `δ = 0.5 pp`**, fijada antes del resultado.

## 10 · Escala pareada exhaustiva (§4, copiada)

| Condición sobre IC95 de `Δ(A,B)` | Veredicto |
|---|---|
| completamente `< −0.5 pp` | `A-GANA` |
| completamente `> +0.5 pp` | `B-GANA` |
| completamente dentro de `[−0.5, +0.5]` | `EMPATE-PRACTICO` |
| cualquier otro caso | `INCONCLUSO` |

## 11 · Escala global (§4, copiada)

| Condición | Veredicto |
|---|---|
| `X` gana sus dos comparaciones **y** no tiene menor cobertura de celdas que ellos | `GANADOR-TRIADA-X` |
| Ningún contendiente lo satisface | `SIN-GANADOR-UNICO` |
| Identidad, contaminación o cobertura rompe la comparación | `NO-ADJUDICABLE-POR-CONTROL` |

**El ranking puntual de `MAE_X` se reporta siempre**, aun si la escala
global no corona a nadie: ranking descriptivo y adjudicación con banda son
dos cosas distintas y se presentan por separado.

## 12 · Cobertura (§5)

Sobre `U0` **y** `UR`, por contendiente: celdas elegibles, celdas con punto,
réplicas `L` válidas de las `k=8`, abstenciones/no-extraíbles/ambiguas,
contaminaciones con su cadena, y exclusiones con motivo. Prohibido proclamar
ganador usando sólo `U3` si tiene peor cobertura que un rival — la condición
de §11 ya lo exige mecánicamente.

## 13 · Secundaria TRANSFERENCIA (§6)

`M` entra a la secundaria en una celda **sólo** si su `ola_calibracion` no
usa una ola posterior a la que la celda evalúa, bajo el criterio mecánico
heredado de `F5 v1.0` §2: **cita con año ≥ ola de la celda, o sin año
determinable, excluye**. Si no cumple, la celda se marca
`M-NO-COMPARABLE-EN-TRANSFERENCIA`. La secundaria **no veta ni reemplaza**
la primaria y **nunca** es condición de `GANADOR-TRIADA-X`.

## 14 · `B` — piso diagnóstico, fuera de la adjudicación (§7)

`B` no entra a `U3`, ni al ranking, ni a la adjudicación, ni a la condición
de `GANADOR-TRIADA-X`, ni tiene veto. Se reporta al final sólo si aporta
información.

## 15 · Controles que este CALC mide (no hereda)

1. **Identidad de captura** — las 224 capturas contra el manifiesto sellado
   de `F5-RECAPTURA-L` (`sha256` + tripleta `id_celda`/`variante`/`índice`
   en nombre, manifiesto y JSON).
2. **Re-derivación de la extracción** — el extractor v1.3 sellado se corre
   aquí sobre las 224 capturas y su salida se coteja captura por captura
   contra el manifiesto de extracción de `ENCARGO 1/5`. Cualquier
   discordancia fuerza `NO-ADJUDICABLE-POR-CONTROL`.
3. **Firewall de `M`** — `estado_firewall` por celda del snapshot, más un
   control propio: `punto_M == R` al grano de float sería contaminación
   directa.
4. **Mismo `U3` para las tres pareadas** — se verifica y se reporta.

---

## 16 · Cierre de P1 (frase obligatoria del encargo, verbatim)

> **El primer resultado producido por este procedimiento es el reportado. No
> se amplía universo, no se cambia agregación, no se recalibra M y no se
> vuelve a capturar L después de observar el ranking.**

Todos los `RESULT` de este CALC quedan **declarados en `spec.yaml` antes de
calcular**, en el mismo `COMMIT-1` que congela este documento y el medidor.
El medidor se escribe y se congela aquí; se ejecuta en el `COMMIT-2`
(`preflight → run → verify`). Un defecto material descubierto produce
`PARO`/`INCONCLUSO`, no una reparación dentro del mismo cómputo.
