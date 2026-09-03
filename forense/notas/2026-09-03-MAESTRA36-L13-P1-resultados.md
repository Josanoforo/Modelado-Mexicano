# `ACTO MAESTRA36-L13 · COERCITIVO-SAT-EFIRMA` — P1 · resultados (COMMIT-2)

3/sep/2026 · UBUNTU · `/home/pc0/mm-maestra36-l13` · base `ea45e01`.
Comando: `python3 tools/medidor_l13_sat_efirma.py --mide --json data/l13-sat-efirma-v1_0.json`.

> **«El primer resultado que produzca este procedimiento es el que se reporta.»**
> Lo es. La spec, las dos cotas y el falsador quedaron congelados en `COMMIT-1`
> (`ef144d1`), antes de correr `--mide`; el falsador, además, no lo eligió el
> ejecutor — venía escrito por la dirección en el encargo (`SHA ea45e01`),
> archivado por `A.3` en `ea3bf92`. Esta nota no edita `COMMIT-1`.

## Veredicto

**`AMBIGUA-POR-UNIVERSO` — este acto NO adjudica.**

| | valor | tramo del falsador B-bis |
|---|---|---|
| `p_inf` (denominador amplio: padrón **Total**) | **0.3684** | `ACOTADA` |
| `p_sup` (denominador obligado: `Total − Asalariados PF`) | **0.9211** | `CONTRARIA` |

Las dos cotas caen en tramos distintos. La precedencia que el propio encargo
fijó —«si la cota inferior y la superior caen en filas distintas →
`AMBIGUA-POR-UNIVERSO`, no adjudica»— se aplica tal cual.

## Lo que sí queda medido

Esto es geometría del falsador congelado, no una adjudicación nueva:

- **Ningún punto** del intervalo `[0.3684, 0.9211]` cae en el tramo
  `CORROBORADA-PARCIAL`, cuyo techo es `0.20`. La regla **no queda corroborada
  bajo ninguna de las dos definiciones de universo**.
- La cota **inferior** —la construida sobre el denominador más grande posible,
  que mete a **52 673 672** asalariados que en general no están obligados a
  e.firma— ya está **cuatro veces por encima** del `0.09` asignado. En la escala
  declarada eso es una diferencia de **orden de magnitud y signo**, que es la
  única comparación que la escala autoriza; **no** se afirma «difiere en Z %».
- Que la cota superior llegue a `0.92` es exactamente la señal de que el
  acumulado desde `2004` es una cota **floja** contra un padrón de `2025`.

## Serie 2010–2025 (16 años completos comunes; el encargo pedía ≥ 3)

| año | N acumulado (primeras e.firma) | D amplio (Total) | D obligado | `p_inf` | `p_sup` |
|---|---|---|---|---|---|
| 2010 | 2 752 991 | 33 468 711 | 12 887 741 | 0.0823 | 0.2136 |
| 2013 | 6 587 812 | 41 659 149 | 15 877 175 | 0.1581 | 0.4149 |
| 2016 | 10 250 907 | 56 794 640 | 24 091 657 | 0.1805 | 0.4255 |
| 2019 | 15 149 303 | 77 442 561 | 31 868 297 | 0.1956 | 0.4754 |
| 2022 | 20 829 316 | 82 235 434 | 34 089 367 | 0.2533 | 0.6110 |
| 2025 | **32 331 680** | **87 773 627** | **35 099 955** | **0.3684** | **0.9211** |

(la serie completa año por año está en `data/l13-sat-efirma-v1_0.json`.)

Monótona creciente en las dos cotas. Eso ordena la lectura temporal: **la e.firma
se volvió general después de que el prior fue asignado** — en `2010`, `p_inf` era
`0.0823`, a un pelo del `0.09` de la regla.

## Escala declarada (A-bis 3)

Proporción **administrativa agregada**: un **campo del entorno**, no una
probabilidad individual de conducta. Precedente: firma `p1` (mesa, 2/sep/2026,
`MAESTRA34-L6` transfer §4, propagada por `N5`/`ADR-299`), «tasa nacional
ENDUTIH FUERTE como campo, no conducta».

**No hay IC de diseño**, y no es una omisión: es un censo administrativo, no una
muestra. La incertidumbre es de *definición de universo* y está cuantificada
por las dos cotas, que es lo que el encargo pidió.

## Universo, con lo que le falta dicho

- **Numerador.** `firelenumcontri`, «Contribuyentes que han obtenido el
  certificado de e.firma (**se considera el primer certificado emitido**)»,
  `PF`+`PM`, acumulado `2004-01`→`2025-12` = **32 331 680**. La cláusula del
  propio `.xls` es lo que autoriza el acumulado: sin doble conteo por renovación.
  **No es «vigente»** — el certificado caduca y el acumulado no da de baja a
  quien salió del padrón. `N` es **cota superior** del stock vigente, luego
  `p_inf` y `p_sup` son **ambas** cotas superiores de la adopción vigente.
- **Denominador.** El `.xls` **no** trae columna de «obligados», así que no se
  supone ninguna: se declaran dos cotas, como el encargo instruye.
  `Total` = 87 773 627 (incluye asalariados) y `Total − Asalariados (PF)` =
  35 099 955.

## Defecto de la spec que su propia guardia atrapó

`COMMIT-1` suponía que los `Grandes Contribuyentes (PF)/(PM)` iban **dentro** del
`Total`, y mandó verificarlo por identidad aritmética. **No van dentro:**

```
2010  residuo=    14,247  GC(PF)+GC(PM)=    14,247  IGUAL
2020  residuo=    57,326  GC(PF)+GC(PM)=    57,326  IGUAL
2025  residuo=   142,527  GC(PF)+GC(PM)=   142,527  IGUAL
```

`Total = PF + Asalariados + PM + GC(PF) + GC(PM)`. **Sin efecto sobre `p`**: las
dos cotas se construyen desde `Total` y `Asalariados`, nunca desde la partición,
y los grandes contribuyentes **sí** son obligados, así que quedan correctamente
dentro de `D_obligado`. Se reporta porque la guardia existía para esto y porque
callar un supuesto que resultó falso —aunque sea inocuo— es lo que la casa no
hace. El campo `identidad_total_menos_partes` del JSON lo lleva por año.

## Control de consistencia

`firelenumcert` (certificados emitidos, **con** renovaciones) acumulado a
`2025-12` = **58 388 495**, contra **32 331 680** contribuyentes de primer
certificado: razón **1.81**, coherente con renovación cuatrienal. El control
pasa (`certificados ≥ contribuyentes`). `firelenumcert` no se usa como numerador
porque cuenta certificados, no personas — veredicto `EXISTE-NO-SATISFACE` de `P0`.

## Contador

`S1` (priors `ASIGNADO` sin dato) **1 → 0**: `P0` no paró y `P1` produjo `p`, que
es la condición literal que el encargo fija. **Tensión que la mesa debe resolver
en `N11`, declarada aquí y no escondida:** el dato existe y tiene universo
declarado, pero el veredicto es `AMBIGUA-POR-UNIVERSO` y **no adjudica**. Si la
mesa considera que una medición que no adjudica no cuenta como «dato» para este
contador, `S1` vuelve a `1` en el sucesor. **Cargas al motor: 0.**

## Lo que esta pieza no hace

No sella. No amplía `sin_dato_universo_examinado` (sucesor `N11`). No toca
`milpa/tramite.yaml` ni `milpa/procedencia.yaml`: el prior `0.91`/`0.09`
`ASIGNADO` y el tier `MEDIA-FUERTE` quedan **intactos**. No descarga nada del
SAT. No interpreta «adopción» como voluntariedad: la regla habla de coerción, y
el dato mide cumplimiento **bajo** coerción, que es lo que `falsable_si` pregunta.
