# ENIF 2024 · derivados de horizonte de ahorro y vía formal/informal — pre-registro congelado de `CALC-HORIZONTE-VIA-DERIVADOS-0001`

### `prereg-caja-ENIF-HORIZONTE-VIA-DERIVADOS` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/ENIF-HORIZONTE-VIA-DERIVADOS-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-ENIF-HORIZONTE-VIA-DERIVADOS`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro de `CALC-HORIZONTE-VIA-DERIVADOS-0001`: releva `CORR-0015` completa — los 7 `RESULT` (`RES-0047`, `RES-0049`, `RES-0053`, `RES-0054`, `RES-0055`, `RES-0056`, `RES-0066`), **todos DERIVADOS por aritmética exacta** de `RESULT` ya sellados en `CALC-ENIF-0001` y `CALC-ENIF-0002`, más las dos sensibilidades ya citadas en `milpa/tramite.yaml` sobre `dinero.ahorro.tiene_ahorros`. **Cero microdato, cero bootstrap propio.** |
> | **QUÉ NO ES** | No es una medición nueva: ningún `RESULT` de esta spec tiene IC95 propio — son funciones deterministas (complemento `1-p`, o inclusión-exclusión) de puntos ya medidos con diseño. No re-abre `CALC-ENIF-0001` ni `CALC-ENIF-0002` (`E.3`, no se editan). No toca `milpa/tramite.yaml`. |
> | **VERIFICAS ASÍ** | CAJA (o cualquier sesión con el repo) confirma que los cuatro insumos (`RESULT-ENIF-AHO-A-P-CORTO-SIN-P`, `RESULT-ENIF-AHO-A-P-CORTO-CON-P` de `CALC-ENIF-0001`; `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P` de `CALC-ENIF-0002`; y `tiene_ahorros_enif2024`/`A_solo_formal`/`B_solo_informal` de `milpa/tramite.yaml`) siguen sellados con los valores de §1, y que los 7 derivados de §2 reproducen los 7 valores legacy de `data/corrida0/demanda-resultados.tsv` dentro de tolerancia exacta. |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026, entorno **NUBE**, sobre `origin/main = da9b47a361143d408cd9fd9c20d17b101c4fe381`.

**Regla consumidora:** `dinero.ahorro.horizonte_corto` (complemento), `dinero.ahorro.horizonte_no_corto_con_seguridad_social` (complemento), `dinero.ahorro.via_informal` (partición completa), `dinero.ahorro.horizonte_no_trabajadores` (complemento) — cuatro reglas de `milpa/tramite.yaml`, cada una consumiendo uno o más de los 7 `RESULT`.

---

## 0 · A.8/P3 — el encadenamiento a la corrida padre, con la condición escrita

`data/corrida0/mapa-demanda-19-corr-v1_0.tsv` marca `CORR-0015`
`BLOQUEADA · DEPENDE-DE-CORRIDA-PADRE`, sucesor `"TANDA-2, despues de
CORR-0009"`, con la nota: *"Los 7 RESULT son DERIVADOS (peldaño 3) de la
familia A y de la familia B de CORR-0009 ... No tienen payload propio y no
pueden tener spec propia antes de que su corrida padre esté relevada
entera. Congelarlos ahora fijaría un complemento sobre un punto que
todavía puede cambiar."`

**Condición escrita, y verificada antes de congelar esta spec:**
`CORR-0009` queda **agotada (9/9 `RESULT`)** en este mismo acto
(`prereg-caja-ENIF-TIENE-AHORROS`, §3 de esa spec) — 6 vía `CALC-ENIF-0001`
(ya sellado antes de este acto), 1 (`RES-0065`) vía `CALC-ENIF-0002` (ya
sellado antes de este acto, corregido en §0.3 de esa spec), 2
(`RES-0031`/`RES-0032`) vía `CALC-TIENE-AHORROS-0001` (esta misma tanda).
**La condición se cumple**: los cuatro insumos que `CORR-0015` deriva
(`RESULT-ENIF-AHO-A-P-CORTO-SIN-P`, `RESULT-ENIF-AHO-A-P-CORTO-CON-P`,
`RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P`, y el par
`tiene_ahorros_enif2024`/`no_tiene_ahorros_enif2024`) están **todos
sellados y ninguno cambia** en esta tanda — el punto sobre el que se
congela el complemento ya no puede moverse. Verificado con comando:

```
$ grep -rl "RESULT-ENIF-AHO-A-P-CORTO-SIN-P\|RESULT-ENIF-AHO-A-P-CORTO-CON-P" data/corrida0/*/resultados.json
data/corrida0/CALC-ENIF-0001/resultados.json
$ grep -rl "RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P" data/corrida0/*/resultados.json
data/corrida0/CALC-ENIF-0002/resultados.json
$ ls data/corrida0/CALC-ENIF-0001/sello.json data/corrida0/CALC-ENIF-0002/sello.json
data/corrida0/CALC-ENIF-0001/sello.json
data/corrida0/CALC-ENIF-0002/sello.json
```

Ambos `CALC` traen `sello.json` (SELLADOS). Los 7 `RESULT` de `CORR-0015`
**no dependen del residuo de `CORR-0009`** en ningún sentido que pueda
moverlos: son función exclusivamente de los 4 insumos ya sellados citados
arriba, ninguno de los cuales cambió al cerrar `CORR-0009` en este acto (la
congelación de `RES-0031`/`RES-0032` en `CALC-TIENE-AHORROS-0001` **no
altera** ningún valor previamente sellado — sólo les da capa 2).

---

## 1 · Insumos, todos ya sellados

| `RESULT`/campo insumo | valor | fuente sellada |
|---|---|---|
| `RESULT-ENIF-AHO-A-P-CORTO-SIN-P` | `0.541343` | `CALC-ENIF-0001/resultados.json` (trabaja sin seguridad social) |
| `RESULT-ENIF-AHO-A-P-CORTO-CON-P` | `0.373130` | `CALC-ENIF-0001/resultados.json` (trabaja con seguridad social) |
| `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P` | `0.632782` | `CALC-ENIF-0002/resultados.json` (no trabaja) |
| `tiene_ahorros_enif2024` | `0.642080` | `milpa/tramite.yaml:641`, releado por `CALC-TIENE-AHORROS-0001` (esta tanda) |
| `no_tiene_ahorros_enif2024` | `0.357920` | ídem, complemento |
| `A_solo_formal` (sensibilidad) | `0.284927` | `milpa/tramite.yaml:667`, `enmienda_enif2024.sensibilidades_pre_declaradas` |
| `B_solo_informal` (sensibilidad) | `0.561920` | `milpa/tramite.yaml:668`, ídem |

Ninguno de estos 7 valores se recalcula: se **leen**, con cita a
archivo+línea, y se combinan por aritmética exacta declarada en §2.

---

## 2 · Transformación (determinista, sin bootstrap propio)

**Familia horizonte (complemento simple, `1-p`, sobre el mismo dominio):**

```
horizonte_no_corto_sin_ss         = 1 - RESULT-ENIF-AHO-A-P-CORTO-SIN-P       = 1 - 0.541343 = 0.458657   # RES-0047
horizonte_no_corto_con_ss         = 1 - RESULT-ENIF-AHO-A-P-CORTO-CON-P       = 1 - 0.373130 = 0.626870   # RES-0049
horizonte_no_corto_no_trabajadores = 1 - RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P = 1 - 0.632782 = 0.367218   # RES-0066
```

**Familia vía informal/formal (inclusión-exclusión sobre `tiene_ahorros`,
partición completa en 4 celdas mutuamente excluyentes):**

```
ambas          = A_solo_formal + B_solo_informal - tiene_ahorros_enif2024
              = 0.284927 + 0.561920 - 0.642080 = 0.204767                  # RES-0054 (ahorra_ambas_vias)
solo_formal    = A_solo_formal - ambas   = 0.284927 - 0.204767 = 0.080160  # RES-0055 (ahorra_solo_formal)
solo_informal  = B_solo_informal - ambas = 0.561920 - 0.204767 = 0.357153  # RES-0053 (ahorra_solo_informal)
no_ahorra      = no_tiene_ahorros_enif2024 = 0.357920                     # RES-0056 (no_ahorra)
```

Identidad de verificación (los cuatro suman 1 exacto, universo completo sin
residuo): `ambas + solo_formal + solo_informal + no_ahorra = 1.0`.

**Por qué es inclusión-exclusión y no una cuarta medición.** `A_solo_formal`
y `B_solo_informal` son, pese al nombre, `P(F)` y `P(I)` totales (formal
total, informal total — el nombre en `milpa/` viene de la sensibilidad que
los introdujo, no de la celda que aquí se deriva): `P(F∩I) = P(F) + P(I) -
P(F∪I)`, identidad de conjuntos exacta, sin supuesto de independencia. Se
verifica que **no** se asumió independencia: `P(F)×P(I) =
0.284927×0.561920 = 0.160096 ≠ 0.204767` — el dato real tiene más
solapamiento que el que la independencia predeciría (ahorradores duales
correlacionados), y la fórmula usada es la identidad exacta, no la
aproximación.

---

## 3 · `estimando`

**Descriptivo, sin incertidumbre nueva.** Los 7 `RESULT` son funciones
deterministas de puntos ya medidos con diseño — **no llevan IC95 propio**:
declararlo sería inventar precisión que esta derivación no produce (el IC95
de una diferencia o combinación de proporciones exige covarianza entre las
corridas originales, que no está disponible sin re-correr el bootstrap
conjunto — fuera de perímetro de esta pieza, que es aritmética de
registro, no medición). Tolerancia: `abs=1e-6` en los 7 valores, `abs=1e-9`
en la identidad de suma.

---

## 4 · `resultados` que releva

`CORR-0015` completa: `RES-0047`, `RES-0049`, `RES-0053`, `RES-0054`,
`RES-0055`, `RES-0056`, `RES-0066` — 7 de 7. `CORR-0015` queda **agotada**.

## 5 · Qué NO hace este acto

No abre ningún `.csv`/`.dta`. No re-corre `CALC-ENIF-0001` ni
`CALC-ENIF-0002`. No calcula IC95 de ningún derivado. No toca
`milpa/tramite.yaml`.

**El primer resultado que produzca este procedimiento es el que se
reporta.**
