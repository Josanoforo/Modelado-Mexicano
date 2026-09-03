# `ACTO MAESTRA35-L8` — `P0`, censo del denominador nuevo y tabla de identificación

Commit de `P0`. Censa los payloads SICEE que `ACTO MAESTRA35-A1` (relanzamiento,
`PR #483`) depositó para Hidalgo, Aguascalientes y Veracruz, y re-deriva la
tabla de identificación sobre el universo ampliado. Todo veredicto de este
documento sale de un comando de esta sesión (2/sep/2026), con el código a la
vista en `tools/l8_amplia_tipo_boleta.py` (hermano nuevo de
`tools/mide_participacion_tipo_boleta.py`, que importa y no toca).

---

## §0 · Qué se censó

Fuente: `data/raw/electoral_sicee_local/sicee_local_{hgo,ags,ver}_pel_*.zip`
(14 zips, alta de fuente `sicee_ine`, `REL-6c677146f183f594c0649a61`). De los 14,
solo los que traen carpeta `AYUNTAMIENTOS_csv/` corresponden a una elección de
ayuntamiento real (los demás son `GUBERNATURA`/`DIPUTACIONES_LOC` de años sin
renovación municipal en esa entidad):

| entidad | zips SICEE depositados | con `AYUNTAMIENTOS_csv` | años de ayuntamiento según `p0-tratamiento` |
|---|---|---|---|
| Hidalgo | 2016, 2018, 2020, 2021 | **2016, 2020** | 2016, 2020, **2024** |
| Aguascalientes | 2016, 2018, 2019, 2021, 2024 | **2016, 2019, 2021, 2024** | 2016, 2019, 2021, 2024 |
| Veracruz | 2016, 2017, 2018, 2021 | **2017, 2021** | 2017, 2021, **2025** |

**Hallazgo que corrige el supuesto del encargo.** El encargo previó que la pata
en riesgo fuera 2016 de Hidalgo («si Hidalgo 2016 no trae lista nominal... entra
con 2020→2024 solamente»). Es al revés: **2016 y 2020 SÍ están, completos; no
existe ningún zip SICEE para Hidalgo 2024** (ni para Veracruz 2025). El leg que
falta es el que **cruza hacia el tratamiento**, no el que lo antecede — Hidalgo
entra con **2016→2020 (STAY)**, no con la transición que identificaría su
efecto. La cobertura declarada de SICEE (elecciones locales desde 2015) no
implica que cada entidad tenga *todos* sus años dentro de esa ventana.

## §1 · Método de lectura, decidido por lo que el propio censo mostró

**SICEE publica dos tablas por año: `_CAS.csv`** (por casilla) **y `_MUN.csv`**
(pre-agregada por municipio). El censo reagregó ambas y las cruzó (control
`§1.7.6`, |Δvotos| y |Δlista nominal|):

| | comunes | max|Δ lista nominal| | max|Δ votos| |
|---|---:|---:|---:|
| Hidalgo 2016 | 82/84 | **0.0** | 1642.0 |
| Hidalgo 2020 | 84/84 | **0.0** | 313.0 (municipio) / 36412 a nivel archivo* |
| Aguascalientes 2016/2019/2024 | 11/11 | **0.0** | 0.0 |
| Aguascalientes 2021 | 11/11 | **0.0** | 472.0 |
| Veracruz 2017 | 212/212** | **0.0** | 1006.0 |
| Veracruz 2021 | 212/212 | **0.0** | 6782.0 |

`*` la reagregación por municipio del cuadro de arriba usa el máximo de las
diferencias individuales; a nivel de todo el archivo la suma cruda difiere en
53330 votos, casi enteramente por el caso de abajo. `**` 212 nombres coinciden
por texto; 6 filas en blanco al final del `_CAS.csv` de 2017 no cuentan.

**`LISTA_NOMINAL` reagrega EXACTO (Δ=0.0) en las 8 tablas — sin una sola
excepción.** `TOTAL_VOTOS` **no**. La causa, verificada, no es un error de
lectura: **el `MUN.csv` que SICEE publica excluye municipios cuya acta sigue en
`ESTATUS_ACTA = 'GRUPO DE TRABAJO'`** (trabajo de cómputo aún no consolidado al
momento del corte de la base), mientras que el `CAS.csv` sí trae esos votos.
Verificado nombre por nombre:

- **Hidalgo 2020, `ACAXOCHITLAN` e `IXMIQUILPAN`**: el `MUN.csv` las deja con
  `TOTAL_VOTOS` en blanco (`LISTA_NOMINAL` sí presente). Sus `52` y `132`
  casillas respectivamente **sí** traen voto: `16327` y `36412`, las dos con
  `ESTATUS_ACTA = 'GRUPO DE TRABAJO'` en el `100%` de sus casillas. **`36412`
  es, dígito por dígito, la diferencia de archivo completo de arriba.**
- **Veracruz 2017, `CAMARON DE TEJEDA`, `EMILIANO ZAPATA`, `SAYULA DE ALEMAN`**:
  al revés — **las dos tablas coinciden en `TOTAL_VOTOS = 0`**, con estatus
  mixto (`Acta casilla` y `Grupo de Recuento`, no todo pendiente). No es
  recuperable por reagregación: es un hueco real de la fuente para esos tres
  municipios en 2017, y se declara `NO-OBTENIDO` para esa pata, nombrado.

**Decisión, tomada por lo anterior y no por preferencia:** este acto reagrega
**desde `CASILLA`** para `TOTAL_VOTOS` y `LISTA_NOMINAL`, con el `MUN.csv`
como **control cruzado** únicamente — el mismo método que
`zacatecas2016_municipio_html()`/`bc_casilla()`/`chihuahua_casilla()` de `L3`
ya usan (agregar desde casilla, cruzar contra cualquier tabla independiente).
Aplicarlo aquí **rescata Hidalgo de 82/84 a 84/84** en 2020 sin tocar ningún
criterio del universo.

**`MEDELLIN` (Veracruz 2017) → `MEDELLIN DE BRAVO` (2021), mismo `ID_MUNICIPIO`
SICEE (`106`) en los dos años**: renombre oficial, no municipio nuevo ni
discordancia. Alias añadido, un par, igual que `_ALIAS_MUN` de `L3` para
Rosarito/Batopilas.

**Cinco `ID_MUNICIPIO` de Veracruz 2017 se repiten en el archivo bajo nombres
DISTINTOS** (`58`→Chiconamel/Chicontepec, `79`→Isla/José Azueta/Juan Rodríguez
Clara, `139`→Río Blanco/San Andrés Tenejapan, `161`→Tenampa/Tepatlaxco,
`183`→Tlaquilpa/Tlilapan) — la numeración de `ID_MUNICIPIO` de este export no es
1:1. Por eso el censo identifica municipio por **nombre normalizado** (mismo
método `_norm_mun` de `L3`), nunca por `ID_MUNICIPIO`; ninguna de las dos
tablas se leyó por posición ni por id.

## §2 · Controles aritméticos (§1.7.6), corridos antes de mirar el estimador

| control | resultado |
|---|---|
| Reagregación casilla→municipio, `LISTA_NOMINAL` | **Δ=0.0 en las 8 tablas, sin excepción** |
| Identidad `TOTAL/LN` vs `PARTICIPACION` publicada — Aguascalientes 2016 | `max|Δ|=0.0042pp` en 11 municipios (excelente) |
| Identidad — Veracruz 2017 | `max|Δ|=1.76pp` en 209 municipios, **2** superan 1pp |
| Identidad — Hidalgo 2016 | `max|Δ|=12.59pp` en 82 municipios, **4** superan 1pp — ver abajo |
| Participación fuera de `(0,100]` | **0** en las 864 observaciones municipio-transición del panel final |
| Cobertura vs. tabla de tratamiento (84 Hgo / 11 Ags / 212 Ver) | Hidalgo 84/84 · Aguascalientes 11/11 · Veracruz 212/212 (bruto), 209 con voto en 2017 |

**El defecto de fuente que el control de Hidalgo 2016 atrapó, cuantificado, no
reparado** (mismo principio que `L3 §4` con Chihuahua-Juárez): en **4 de 82**
municipios la columna `PARTICIPACION` que el propio SICEE publica no
reproduce `TOTAL_VOTOS/LISTA_NOMINAL` (peor caso: `MOLANGO DE ESCAMILLA`,
publicada `87.73%`, recalculada `75.14%`, `Δ=12.59pp`); la mediana de los 82 es
`0.0065pp`. La spec (`§1.2`, heredada) nunca usa la columna `PARTICIPACION` de
la fuente para el modelo — solo como control — así que esto no cambia ningún
valor usado, y se declara aquí como hallazgo de calidad de fuente, no como
defecto propio.

## §3 · Tabla de identificación, universo ampliado

`python3 tools/l8_amplia_tipo_boleta.py --censo` corrió sobre las 8 tablas de
arriba (ver salida cruda en el commit). La tabla de identificación
**calendario-completa** (`data/l3-tabla-identificacion-v1_0.tsv`, 73
transiciones / 32 entidades) **no cambia** — es derivada del calendario INE, no
de qué se adquirió, y este acto no toca `data/p0-*`. Lo que sí cambia es
**cuánto de esa tabla entra al panel real** (municipio × transición con dato en
las dos patas), computado por el mismo script, `--json`, antes de congelar
`COMMIT-1` — ver la declaración de secuencia en
`forense/notas/2026-09-02-MAESTRA35-L8-spec.md` para el porqué esta cifra ya se
conocía al escribir la spec.

| | `L3` (panel real) | **`L8` (panel real, ampliado)** |
|---|---:|---:|
| transiciones `STAY` (identifican `α` sin mezcla) | 2 | **4** (cruza el umbral de 3 de `§0.3`) |
| entidades tratadas **medibles** (≥1 `SWITCH` en el panel) | 5 | **7** (meta declarada ≥8 — **sigue ACOTADO**) |
| conglomerados (entidades con ≥1 observación en el panel) | 6 | **9** |
| `p` mínimo alcanzable (wild cluster, `2/2^k`) | 0.03125 | **0.00390625** |
| municipios en el panel | 187 | **864 transiciones-municipio** sobre 9 entidades |

**Hidalgo entra al panel pero NO se vuelve «medible»**: su única transición
obtenible (`2016→2020`) es un `STAY` (ambas patas sin federal) — aporta a la
identificación de `α`, no a la de `β`. Es `TRATADO` (`cohorte g2024`) sin
transición tratada medible, exactamente como `Durango` es `NUNCA-TRATADO` sin
serlo tampoco: dos razones distintas para el mismo resultado (`0`
transiciones-tratamiento medibles). **Aguascalientes** y **Veracruz**, en
cambio, sí se vuelven medibles (Aguascalientes con sus tres transiciones —
`STAY`+2 `SWITCH`—, Veracruz con una `SWITCH` que identifica `β_int`).

**Municipios perdidos de la intersección `§1.3`, nombrados:** Hidalgo, ninguno
(84/84 tras reagregar desde casilla). Veracruz: `CAMARON DE TEJEDA`,
`EMILIANO ZAPATA`, `SAYULA DE ALEMAN` (§1 arriba). Aguascalientes: ninguno.

## §4 · Lo que `P0` deja fijado

* Método de lectura fijado **por lo que el censo mostró**, no por preferencia:
  reagregar desde casilla, cruzar contra el `MUN.csv` de la fuente.
* Hidalgo entra por su `STAY`, no por una transición tratada — corrección
  explícita del supuesto del encargo, declarada aquí y no escondida.
* 3 municipios de Veracruz 2017 quedan `NO-OBTENIDO` con receta: ninguna,
  porque no hay reagregación posible — el hueco está en la fuente misma.
* `n_STAY` cruza el umbral de `3` de `§0.3`: `α` se identificará **sin
  reserva** en este acto (a diferencia de `L3`).
* `k` sube de 6 a 9 conglomerados: el `p` mínimo alcanzable baja de `0.03125` a
  `0.00390625`, más de 8 veces más potencia mecánica que `L3`.
