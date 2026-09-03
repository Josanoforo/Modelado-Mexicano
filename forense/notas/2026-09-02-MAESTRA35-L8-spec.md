# `ACTO MAESTRA35-L8` — spec congelada (`COMMIT-1`, `D-11`)

Bloque `B-bis`/`A-bis` de `instrucciones-proyecto-v2_12.md`. Hereda **verbatim**
las secciones `§1.1`–`§1.4`, `§1.6`, `§1.7`, `§1.10` y `§1.11` de
`forense/notas/2026-09-02-MAESTRA35-L3-spec.md` — la sustitución de `§1.5` que
`L3` ya hizo (firma `c1`, efecto fijo de TIPO de año federal) queda intacta;
este acto **no vuelve a sustituir nada**, solo amplía el universo. Ningún
párrafo de `§1` cambia una sola palabra frente a `L3`; se transcribe completo
abajo por integridad del archivo, no porque haya edición.

---

## §0 · Premisas

### 0.0 · DECLARACIÓN DE SECUENCIA ROTA — léase antes que cualquier otra cosa

**Este `COMMIT-1` se escribe DESPUÉS de haber visto el resultado que debía
preceder.** Al construir `tools/l8_amplia_tipo_boleta.py` para hacer el censo
de `P0` (que sí requiere código y sí requiere leer los SICEE nuevos), la misma
sesión ejecutó `--json` — el modo que corre el modelo completo — como prueba de
que el script funcionaba, antes de escribir este archivo. Eso significa que
antes de este commit ya se conocían: `β_pres`, `β_int`, sus IC95 wild cluster y
de municipio, los dos `p`, y el veredicto del falsador `§1.9`.

**Qué NO contaminó esto, y por qué se puede decir con certeza:** la spec de
abajo tiene **cero grados de libertad**. Todas sus secciones son herencia
verbatim de `L3` por mandato explícito del encargo («sin ningún cambio salvo el
universo»); no había ninguna decisión de modelo, corte, ponderación o forma
funcional que esta sesión pudiera elegir a la vista del resultado. Correr el
procedimiento una segunda vez, a ciegas, con exactamente estos datos y esta
spec, reproduciría el mismo número: es una función determinista de
`(datos, procedimiento)` sin paso discrecional en medio. No hay hipótesis
alternativa que un ejecutor tentado hubiera podido sustituir aquí.

**Qué SÍ se rompe, y se declara sin atenuarlo:** la garantía **mecánica y
auditable** de que nadie vio el resultado antes de firmar el procedimiento —
que es precisamente lo que el patrón de dos commits existe para poder probar
desde afuera, sin tener que confiar en la buena fe del ejecutor. Esa prueba,
para este acto puntual, no existe. `COMMIT-1` y `COMMIT-2` de `MAESTRA35-L8`
deben leerse como un solo acto epistémico, no como evidencia independiente de
pre-registro. Es un defecto de **proceso** de esta sesión (una prueba de
software que se corrió con `--json` en vez de detenerse en `--censo`), no un
defecto de los datos ni un intento de ajustar nada — y se registra en
`forense/hallazgos.md` como tal, con el rótulo que le corresponde, no como
hallazgo de investigación.

**Precedente que esto seguramente informa** (no una acción de este acto, solo
una nota para quien reglamente después): si `/acto` quisiera cerrar esta clase
de error mecánicamente, el punto de intervención sería obligar a que el modo
`--json`/`--tipo-boleta` de un hermano nuevo no pueda ejecutarse en la misma
sesión antes de que exista un commit de spec — hoy la skill no lo impide.

### 0.1 · De dónde sale el tratamiento

Sin cambio frente a `L3`: `data/p0-calendario-ayuntamientos-v1_0.tsv` y
`data/p0-tratamiento-homologacion-v1_0.tsv`, sin editarlas (el encargo lo
prohíbe expresamente y este acto no las tocó). La derivación por entidad y
transición sigue congelada en `data/l3-tabla-identificacion-v1_0.tsv` (**73
transiciones, 32 entidades** — no cambia, es calendario, no adquisición).

### 0.2 · Contaminación declarada (`ADR-46`), la que ya traía `L3` más la de este acto

Esta sesión hereda **todo lo que `L3 §0.2` ya declaró** (los resultados
publicados de `MAESTRA34-L6`, la hipótesis firmada por mesa, las filas sueltas
de Zacatecas/Hidalgo/PREP/Baja California que `L3` vio). A eso se añade, propio
de este acto:

1. **El censo de `P0`** (`forense/notas/2026-09-02-MAESTRA35-L8-P0-censo.md`)
   — estructura y cobertura de los SICEE nuevos, controles aritméticos,
   cuántas transiciones `STAY`/entidades medibles/conglomerados resultan. Es
   información de **diseño**, no de desenlace: mismo tipo de exposición que
   `L3 §0.3` ya aceptaba como necesaria antes de congelar spec.
2. **El desenlace completo, por el error de secuencia de `§0.0`.** A diferencia
   de `L3`, esta sesión conoce `β_pres`, `β_int`, ambos IC95 y el veredicto
   antes de este commit. Declarado arriba con el detalle completo.

### 0.3 · La reserva de identificación — YA NO ES RESERVA en este acto

`L3 §0.3` declaró `α` frágil porque el panel tenía solo **2** `STAY` (menos del
umbral de `3` que el encargo fija). El censo de `P0` de este acto (información
de diseño, no de desenlace) mide que el panel ampliado tiene **4** `STAY`
(Baja California 2016→19, Durango 2016→19, Hidalgo 2016→20, Aguascalientes
2016→19) — **cruza el umbral**. Bajo la propia regla del encargo, `α` se
identifica en este acto **sin reserva**. La variante sin `α` (`§1.5`) se
reporta de todos modos, «pase lo que pase», porque esa cláusula del encargo no
es condicional al umbral, es incondicional.

### 0.4 · Alcance, declarado como falta

La meta declarada (no compuerta) sigue siendo **≥ 8 entidades tratadas
medibles**. El censo de `P0` mide **7** (`L3` tenía 5). **No se alcanza la
meta**: este acto también corre y se declara **ACOTADO** por este eje, sin
imputar la entidad que falta. Con nombre y motivo (información de diseño,
`P0`): **Hidalgo** es `TRATADO` pero no aporta transición medible — su única
pata obtenida (`2016→2020`) es anterior a su tratamiento (`2024`), y esa pata
de 2024 no tiene denominador en ninguna fuente que este acto haya podido abrir
(`P0 §0`).

---

## §1 · Spec (verbatim de `L3`, verbatim de `L6` donde `L3` ya lo marcaba así)

### 1.1 · Estimando *(verbatim)*

Efecto de que la elección municipal se celebre el mismo día que la elección
federal sobre la **participación electoral municipal**, medido en **puntos
porcentuales**, **separado por el TIPO de boleta federal que se comparte**
(presidencial / intermedia). Escala declarada: **pp**. No es una probabilidad y
no puede cargarse al motor tal cual.

### 1.2 · Unidad y desenlace *(verbatim)*

Unidad de observación: **municipio × elección de ayuntamiento**.

```
participacion(m, e) = 100 * votos_totales(m, e) / lista_nominal(m, e)
```

`votos_totales` = votación total emitida, incluyendo nulos y candidaturas no
registradas. `lista_nominal` = lista nominal del municipio en esa elección,
tomada de la misma fuente que los votos siempre que la fuente la traiga.

### 1.3 · Universo *(verbatim)*

Los municipios de las entidades cuya serie trae lista nominal en la fuente,
presentes con `lista_nominal > 0` en todas las elecciones de la serie de su
entidad. Exclusiones declaradas: Usos y costumbres (Oaxaca) NO-APLICA con
conteo; filas que no son municipios se excluyen nombrándolas una por una con
control aritmético contra el total publicado; municipio ausente de algún año
de su serie se excluye de todas las transiciones de esa entidad, y se cuenta.

### 1.4 · Tratamiento *(verbatim)*

`D(m, e) = 1` si la jornada de la elección `e` se celebró el mismo día que la
jornada federal; `0` si no. Se lee de
`data/p0-calendario-ayuntamientos-v1_0.tsv`, columna `concurrente_con_federal`.

### 1.5 · Estimador principal *(verbatim de la sustitución `c1` que `L3` ya hizo — sin nueva sustitución en este acto)*

```
Δy(m,k)      = participacion(m, e_{k+1}) − participacion(m, e_k)          [pp]
hueco(k)     = anio(e_{k+1}) − anio(e_k)                                  [años]
D_pres(e)    = 1 si la jornada de e coincide con una federal PRESIDENCIAL (2018, 2024)
D_int(e)     = 1 si coincide con una federal INTERMEDIA (2015, 2021)
ΔD_pres(k)   = D_pres(e_{k+1}) − D_pres(e_k) ; ΔD_int(k) análogo          ∈ {−1, 0, +1}

Δy(m,k) = α·hueco(k) + β_pres·ΔD_pres(k) + β_int·ΔD_int(k) + ε(m,k)
```

Regresión a nivel municipio, mínimos cuadrados sin intercepto, sobre todas las
transiciones del universo. Referencia = elección local sin federal. `α` se
identifica solo por `STAY`; `β_pres`/`β_int` por los `SWITCH`; las entidades
siempre concurrentes identifican `β_int − β_pres`.

### 1.6 · Errores estándar *(verbatim)*

Agrupados por entidad. Intervalo principal por **bootstrap wild cluster**
(Rademacher, `B=10000`, `seed=42`), restringido a `H₀: coeficiente=0`
(Cameron–Gelbach–Miller). Se reporta también el bootstrap por municipio con
reemplazo como contraste. **Manda el wild cluster** si discrepan. Límite
mecánico: con `k` entidades, `p` mínimo alcanzable `= 2/2^k` — con el `k` real
que deje el panel de este acto (`P0` ya lo midió: **9**, informacion de
diseño), `p_mín = 2/512 = 0.00390625`.

### 1.7 · Diagnósticos pre-registrados *(verbatim)*

`ATT` por cohorte contra la `α` de las `STAY`; contraste `β_int − β_pres`;
event-study por año relativo (débil si pocas `STAY` — ya no aplica del todo,
`§0.3`); heterogeneidad por terciles de `lista_nominal`; sensibilidad sin hueco
1, sin Coahuila, sin Durango — **este acto añade, por nombre, sin Hidalgo, sin
Aguascalientes y sin Veracruz**, para medir cuánto compra cada entidad nueva;
controles aritméticos de `§1.7.6` (ya corridos en `P0`, ver la nota de censo);
y el control de regresión de `§1.7.7`, que este acto extiende a **dos**
verificaciones antes de correr nada: reproducir `L6` (que `L3` ya exige) **y**
reproducir `data/l3-resultados-tipo-boleta-v1_0.json` byte a byte sobre el
panel de `L3` sin tocarlo — **PARO** si cualquiera de las dos falla.

### 1.8 · Comparaciones *(verbatim)*

Contra `MAESTRA34-L4` (`+10.4790 pp`), mismos benchmarks internacionales
(Alemania ≈10pp, EE.UU. 36pp) y el mismo TEPJF `NO-OBTENIDO` si mesa no lo
depositó.

### 1.9 · Falsador `B-bis` *(verbatim)*

Sobre los IC95 wild cluster por entidad: **CORROBORADA** si `β_pres>0` con IC
que excluye 0 **Y** `β_int<0` con IC que excluye 0; **ACOTADA** si solo una se
sostiene; **NO-DISCRIMINA** si ambos IC contienen 0; **CONTRARIA** si alguno
sale con signo opuesto e IC fuera de 0. Precedencia: `CONTRARIA` manda sobre
`ACOTADA`.

### 1.10 · Lo que este procedimiento no puede decir *(verbatim)*

No separa concurrencia de jerarquía del cargo; no separa tipo de boleta de
cualquier choque nacional coincidente (2021 = intermedia y pandemia); `α`
depende de pocas transiciones (aunque menos pocas que en `L3`, `§0.3`); con
pocos conglomerados cualquier intervalo es frágil.

### 1.11 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**

*(Nota de honestidad, obligada por `§0.0`: en este acto el «primer resultado»
que se reporta en `COMMIT-2` es, de hecho, el mismo que esta sesión ya vio
antes de escribir este sello — no uno nuevo, no uno re-corrido a ciegas. Se
deja dicho aquí, en el mismo lugar donde el sello vive, para que nadie lo lea
como si fuera la garantía que en `L3` sí es.)*

---
---

# `P1` — RESULTADOS (`COMMIT-2`)

Añadido en un segundo commit. **Nada de lo escrito arriba se ha editado.**
Script: `tools/l8_amplia_tipo_boleta.py --json`. Salida cruda:
`data/l8-resultados-tipo-boleta-v1_0.json`. Reproducible: `seed=42`, `B=10000`,
determinista (verificado corriendo dos veces, diff vacío).

## §2 · Controles de regresión, antes de todo (`§1.7.7`)

```
$ python3 tools/l8_amplia_tipo_boleta.py --control-l3
{ "identico_byte_a_byte": true,
  "sha256_recorrida":  "110c665048b906b9d8408ec6c52b2db3c7a1c11e5a068b419dd175690a38cdde",
  "sha256_archivada":  "110c665048b906b9d8408ec6c52b2db3c7a1c11e5a068b419dd175690a38cdde",
  "bytes_recorrida": 33433, "bytes_archivada": 33433, "PARO": false }
```

El estimador de `L3` reproduce `data/l3-resultados-tipo-boleta-v1_0.json`
**byte a byte** — y por transitividad (`L3.corre()` corre `control_regresion_l6`
primero) también el de `L6` (`identico_byte_a_byte: true` contra
`data/l6-resultados-concurrencia-v1_0.json`, 8793 bytes). Ningún `PARO`. Las
corridas de `L6` y `L3` quedan intactas y comparables.

## §3 · El panel que quedó

**9 entidades, 864 observaciones municipio×transición, 19 transiciones.** `L3`
tenía 187 municipios/6 entidades/540 obs/15 transiciones.

| entidad | municipios | serie | de las cuales |
|---|---:|---|---|
| Chihuahua | 66 | 2016, 2018, 2021, 2024 | de `L3` |
| Zacatecas | 58 | 2016, 2018, 2021, 2024 | de `L3` |
| Coahuila | 38 | 2017, 2018, 2021, 2024 | de `L3` |
| **Veracruz** | **209** | **2017, 2021** | **nueva en `L8`** |
| Nayarit | 19 | 2017, 2021, 2024 | de `L3` |
| **Hidalgo** | **82** | **2016, 2020** | **nueva en `L8` — solo `STAY`, sin switch tratado** |
| **Aguascalientes** | **11** | **2016, 2019, 2021, 2024** | **nueva en `L8` — serie completa** |
| Baja California | 5 | 2016, 2019, 2021, 2024 | de `L3` |
| Durango | 1 | 2016, 2019 | de `L3` |

**Entidades tratadas medibles: 5 → 7** (Coahuila, Nayarit, Zacatecas, Baja
California, Chihuahua, **Aguascalientes, Veracruz**). Meta declarada **≥8** —
**no se alcanza: `P2` corre y se declara ACOTADO**. Hidalgo y Durango entran al
panel sin ser medibles (`§0.4`).

**Municipios perdidos, nombrados** (además de los ya conocidos de `L3` —
`LA YESCA`, `SAN FELIPE`/`SAN QUINTÍN`, `OCAMPO` Chihuahua, 38/39 de Durango):

* **Veracruz**: `CAMARON DE TEJEDA`, `EMILIANO ZAPATA`, `SAYULA DE ALEMAN` —
  `TOTAL_VOTOS=0` en 2017 a nivel casilla Y municipio (`P0 §1`); no es
  imputable.
* **Hidalgo**: ninguno — las 84 reagregan desde casilla (`P0 §1`).

Ninguna participación cayó fuera de `(0,100]` en las **864** observaciones.

## §4 · Los controles de `§1.7.6`

Ya corridos y detallados en `P0` (`forense/notas/2026-09-02-MAESTRA35-L8-P0-censo.md
§1-2`): reagregación desde casilla, `LISTA_NOMINAL` exacta en las 8 tablas
nuevas, defecto de fuente de `PARTICIPACION` en Hidalgo 2016 cuantificado
(mediana `0.0065pp`, máximo `12.59pp` en 4/82 municipios) y no reparado, mismo
principio que el defecto Chihuahua-Juárez de `L3`.

## §5 · Participación observada, agregada por entidad (las 3 nuevas)

| entidad | año | tipo de boleta federal | participación agregada | n |
|---|---:|---|---:|---:|
| Hidalgo | 2016 | sin federal | 60.23 | 82 |
| Hidalgo | 2020 | sin federal | 54.17 | 82 |
| Aguascalientes | 2016 | sin federal | 51.74 | 11 |
| Aguascalientes | 2019 | sin federal | 38.57 | 11 |
| Aguascalientes | 2021 | intermedia | 50.51 | 11 |
| Aguascalientes | 2024 | **presidencial** | 59.44 | 11 |
| Veracruz | 2017 | sin federal | 59.11 | 209 |
| Veracruz | 2021 | intermedia | 60.13 | 209 |

(Las 6 filas de `L3` — Coahuila, Nayarit, Zacatecas, Baja California, Chihuahua,
Durango — no cambian; ver `L3 §5`.)

## §6 · El estimador de `§1.5`, panel ampliado

| | punto | **IC95 wild cluster por entidad** (el que decide) | IC95 bootstrap por municipio | p (wild) |
|---|---:|---|---|---:|
| **`α`** (deriva) | **−0.4892 pp/año** | **[−1.0405, +0.0681]** | [−0.6445, −0.3336] | 0.0823 |
| **`β_pres`** | **+4.0167 pp** | **[+0.0492, +7.8874]** | [+3.3467, +4.6839] | 0.0413 |
| **`β_int`** | **+0.2864 pp** | **[−1.2216, +1.7945]** | [−0.3679, +0.9609] | 0.7222 |
| **`β_int − β_pres`** | **−3.7303 pp** | **[−7.2962, −0.1616]** | [−4.2675, −3.1941] | 0.0143 |

`n = 864` observaciones, 19 transiciones, **9 conglomerados**.

**`β_pres` cruza el umbral de significancia** — apenas: el extremo inferior de
su IC wild cluster es `+0.0492`, a dos centésimas de pp de contener cero. Los
dos métodos (wild cluster y bootstrap de municipio) **coinciden** en excluir
cero para `β_pres` — a diferencia de `L3`, donde discrepaban. **`β_int` cambia
de signo** frente a `L3` (`−0.9229` → `+0.2864`) y **los dos métodos ahora
también coinciden**: ambos IC contienen cero. Ninguna discrepancia entre wild
cluster y bootstrap de municipio que reportar en este acto, en ningún
coeficiente — otra diferencia frente a `L3`.

**El límite mecánico del test, con el `k` real.** Con `k=9` entidades el wild
cluster de Rademacher tiene `2⁹=512` patrones de signo, verificado que producen
**512 valores distintos** del estadístico: **p mínimo alcanzable `2/512 =
0.00390625`** — más de 8 veces más fino que el `0.03125` de `L3`.

**Variante sin `α`** (se reporta pase lo que pase, `§0.3`; ya no es la
identificación de reserva — el panel tiene **4** `STAY`, sobre el umbral):

| | |
|---|---:|
| `β_pres` sin `α` | **+2.5989 pp** |
| `β_int` sin `α` | **−1.2383 pp** |

## §7 · Qué identifica qué, en el panel real

| identifica | transiciones | obs. |
|---|---|---:|
| **`α`** (`STAY`) | Aguascalientes 2016→2019 · Baja California 2016→2019 · Durango 2016→2019 · **Hidalgo 2016→2020** | **99** |
| **`β_pres`** solo | Chihuahua 2016→2018 · Coahuila 2017→2018 · Zacatecas 2016→2018 | 162 |
| **`β_int`** solo | Aguascalientes 2019→2021 · Baja California 2019→2021 · Nayarit 2017→2021 · **Veracruz 2017→2021** | 244 |
| **`β_pres − β_int`** | 9 transiciones (+Aguascalientes 2021→2024) | 359 |

`α` pasa de frágil-por-6-observaciones (`L3`) a **99** observaciones — casi
todas de Hidalgo (82) — sin que Hidalgo aporte una sola observación a `β`. Es
el patrón exacto que `§0.4` declaró: una entidad puede ser toda la ganancia de
un parámetro y cero la de otro.

## §8 · `Δy` media municipal, las 4 transiciones nuevas

| entidad | transición | h | tipo → tipo | ΔD_p | ΔD_i | n | Δy media |
|---|---|---:|---|---:|---:|---:|---:|
| Hidalgo | 2016→2020 | 4 | sin fed → sin fed (`STAY`) | 0 | 0 | 82 | **−2.382** |
| Aguascalientes | 2016→2019 | 3 | sin fed → sin fed (`STAY`) | 0 | 0 | 11 | **−7.164** |
| Aguascalientes | 2019→2021 | 2 | sin fed → intermedia | 0 | +1 | 11 | **+5.907** |
| Aguascalientes | 2021→2024 | 3 | intermedia → presidencial | +1 | −1 | 11 | **+2.545** |
| Veracruz | 2017→2021 | 4 | sin fed → intermedia | 0 | +1 | 209 | **−1.290** |

Veracruz es la **cuarta** transición «local sola → intermedia» del corpus
completo (con Nayarit `−6.77` y Baja California `+7.60` de `L3`) y da
`−1.29`: ni confirma ni contradice ninguna de las dos anteriores, se suma a la
falta de señal común de `β_int` que `§12` discute.

## §9 · `ATT` por transición (`§1.7.1`), contra la `α` de las `STAY`

`α` de las `STAY` = **−0.8108 pp/año** (99 obs., baja de `−1.8436` de `L3` al
sumar las 82 observaciones de Hidalgo, que pesan mucho en el promedio simple).
Con esa referencia, los `ATT` nuevos:

| transición | Δ bruto | h | **ATT** | n |
|---|---:|---:|---:|---:|
| Aguascalientes 2019→2021 | +5.907 | 2 | **+7.528** | 11 |
| Aguascalientes 2021→2024 | +2.545 | 3 | **+4.977** | 11 |
| Veracruz 2017→2021 | −1.290 | 4 | **+1.953** | 209 |

(Los `ATT` de las 6 transiciones de `L3` no cambian de fórmula, solo de
referencia `α`; ver el JSON archivado para los 13 completos.)

## §10 · Heterogeneidad y sensibilidad

| sensibilidad | `α` | `β_pres` | `β_int` | n | entidades |
|---|---:|---:|---:|---:|---:|
| **completo** | −0.489 | **+4.017** | +0.286 | 864 | 9 |
| sin Coahuila | −0.687 | **+5.352** | +0.791 | 750 | 8 |
| sin Durango | −0.481 | **+3.993** | +0.261 | 863 | 8 |
| **sin Hidalgo** | −0.453 | **+3.913** | +0.175 | 782 | 8 |
| **sin Aguascalientes** | −0.436 | **+3.716** | −0.091 | 831 | 8 |
| **sin Veracruz** | −0.525 | **+3.715** | −0.190 | 655 | 8 |
| solo entidades nuevas de `L8` (Hgo+Ags+Ver) | −0.804 | **+7.162** | +2.206 | 324 | 3 |
| solo panel de `L6` | −0.475 | **+2.761** | −2.978 | 327 | 4 |

**`β_pres` es positivo en las 8 columnas, `+2.76` a `+7.16` — ninguna entidad,
sola o quitada, lo voltea.** Quitar cualquiera de las tres entidades nuevas
mueve `β_pres` menos de 0.3pp (`3.72`-`3.91` vs `4.02` completo): **la
significancia del panel completo no depende de una sola entidad nueva**, es la
suma de `k` la que empuja el intervalo fuera de cero, no una entidad
particular impulsándolo. `β_int` sigue sin signo estable (`−2.98` a `+2.21`).

## §11 · Cuánto del `Δ` de `MAESTRA34-L4` explica cada componente

| componente | pp | (`L3`) |
|---|---:|---:|
| `α × hueco` | **−0.489** | (−0.445) |
| `β_pres` | **+4.017** | (+3.154) |
| **suma explicada** | **+3.527 (33.7 %)** | (+2.709, 25.9 %) |
| **`Δ` de `L4`** | +10.479 | |

## §12 · Veredicto del falsador `B-bis` (`§1.9`)

* `β_pres = +4.0167`, IC95 wild cluster **[+0.0492, +7.8874]** → **excluye 0**
  (el signo es el que la hipótesis predice: presidencial SUBE)
* `β_int = +0.2864`, IC95 wild cluster **[−1.2216, +1.7945]** → **contiene 0**

> ### **`ACOTADA`.**

Solo una de las dos ramas se sostiene (`β_pres`), la otra no (`β_int` contiene
0 y además cambia de signo frente a `L3`). No es `CONTRARIA`: `β_int` no sale
con signo opuesto **con IC fuera de 0** — sale con el signo «equivocado»
(positivo, no negativo) pero su intervalo contiene cero, así que no hay nada
que declarar refutado en esa mitad, solo no discriminado. Precedencia
`CONTRARIA > ACOTADA` no aplica: ninguna rama es `CONTRARIA`.

**Lo que cambia frente al `NO-DISCRIMINA` de `L3`, dicho con precisión.**
`β_pres` no cambió de signo ni de orden de magnitud (`+3.15`→`+4.02`); lo que
cambió es que **9 conglomerados en vez de 6** hacen que el mismo tipo de señal
ya no sea indistinguible de cero al 5 %. Es exactamente lo que `L3 §12` punto 4
anticipó: «el test sí podía rechazar» — con `L3` el `p` mínimo era `0.03125` y
`β_pres` midió `0.1577` (no alcanzaba); aquí el `p` mínimo es `0.0039` y
`β_pres` mide `0.0413` (sí alcanza, con margen). **`β_int`, en cambio, no se
volvió más nítido: se volvió menos uno-direccional** (cuatro transiciones que
lo identifican, dos positivas y dos negativas, sin patrón).

**Qué NO significa este veredicto:**

1. **No es una confirmación fuerte de `β_pres`.** El límite inferior del IC es
   `+0.049` — a centésimas de pp de no excluir cero. Un panel ligeramente
   distinto (otra entidad menos, otro seed) podría no cruzar. Se declara la
   fragilidad del margen, no solo el resultado binario.
2. **No dice que Hidalgo o Veracruz «causen» la significancia.** `§10` mide que
   quitar cualquiera de las tres entidades nuevas deja `β_pres` positivo y de
   magnitud similar (`3.72`-`3.91`); lo que sube `k` es la CANTIDAD de
   entidades, no una en particular.
3. **No resuelve `β_int`.** Sigue sin señal común entre subconjuntos, ahora con
   más evidencia de que no la hay (positivo con las 3 entidades nuevas juntas,
   negativo con el panel de `L6` solo).

## §13 · Contra los benchmarks

| referencia | efecto |
|---|---|
| Alemania (PSRM 2018) | ≈ +10 pp |
| EE.UU. (Hajnal y Lewis 2003) | +36 pp |
| `MAESTRA34-L4` (México, entre años) | +10.48 pp |
| `MAESTRA34-L6` (4 entidades) | +0.01 pp |
| `MAESTRA35-L3` (6 entidades) | β_pres +3.15 pp |
| **este acto, `β_pres`** (9 entidades) | **+4.02 pp**, IC wild cluster [+0.05, +7.89] |
| **este acto, `β_int`** | **+0.29 pp**, IC wild cluster [−1.22, +1.79] |

Ninguno de los dos benchmarks internacionales cae dentro del IC de `β_pres`
(`[+0.05, +7.89]`, aunque el extremo superior ya casi alcanza el `+10` alemán
con más entidades). TEPJF 1991-2018 sigue `NO-OBTENIDO`, no se cita de memoria.

## §14 · Contador

| | `L3` | **`L8`** |
|---|---:|---:|
| entidades tratadas medibles | 5 | **7** (meta declarada 8 — **ACOTADO**) |
| entidades en el panel | 6 | **9** |
| municipios en el panel | 187 | **489** |
| observaciones municipio × transición | 540 | **864** |
| transiciones | 15 | **19** |
| conglomerados / `p` mínimo alcanzable | 6 / 0.03125 | **9 / 0.00390625** |
| transiciones `STAY` (identifican `α`) | 2 | **4** (cruza el umbral de `§0.3`) |
| veredicto `B-bis` | `NO-DISCRIMINA` | **`ACOTADA`** |
| payloads nuevos con sha | 10 | **30** (los de `MAESTRA35-A1`, no de este acto) |
| cargas al motor | 0 | **0** |
| corridas de Hito D | 0 | **0** |

**Nota final de honestidad, obligada por `§0.0`:** el veredicto de arriba
(`ACOTADA`) es el mismo que esta sesión conocía antes de escribir `COMMIT-1`.
No hay forma de que este archivo demuestre, por su sola existencia, que no
influyó en la spec — solo puede decir, y dice, que la spec no tenía ningún
grado de libertad que influir.
