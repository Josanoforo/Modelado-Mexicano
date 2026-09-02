# ACTO MAESTRA34-L5 · P3 · `tramite.evasion_norma` — SPEC CONGELADA

**COMMIT-1 de la pieza P3.** Se escribe **antes de calcular ningún desenlace**.
De ENVIPE 2025 se han tocado hasta aquí: el descriptor de archivos
(`fd_envipe2025.pdf`, 7 207 líneas), la lista de 137 columnas de `tmod_vic` y los
**denominadores** — 40 280 delitos, `BP1_20` con 4 110 «sí denunció» y 36 170
«no», `BP1_23` no-blanco en 36 040 y solo entre los `BP1_20=2` (P0 · §4). **No se
ha mirado la distribución de `BP1_23` por código**, que es el desenlace.

**Prior que se pone a prueba** (`milpa/tramite.yaml:203-228`, clase ASIGNADO, tier
MEDIA, con `nota_calibracion` que dice «PROBABILIDADES NO CALIBRADAS … No reportar
con decimales»): `evade_norma p=0.66` / `cumple_norma p=0.34`, bajo
`situacion: enfrenta_norma_percibida_inutil_o_extractiva`,
`disparadores: {sancion_creible: false}`, `contexto_norma: {percibida_util: false}`.

**Fuente elegida: ENVIPE 2025**, no ENCUCI 2020. El encargo autoriza las dos; el
censo prefirió ENVIPE porque su reactivo es **conductual** (dejó de denunciar) y
el de ENCUCI es **actitudinal** (`AP5_11=3`: «las personas *pueden* desobedecer la
ley si esta es injusta»), y el encargo pide «proporción que **declara incumplir**».
Razonamiento completo en P0 · §4.

---

## §1 · Spec

### 1.1 Payload y tabla

| campo | valor |
|---|---|
| payload | `data/raw/envipe2025_csv.zip` · id de manifiesto `envipe2025_csv` (`data/manifiesto.yaml:306`) · `sha256 = 8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` |
| tabla | `tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv` (módulo de victimización) |
| encoding | `latin-1` (el que ya usa `tools/tasas_base_fase1.py` para esta misma tabla) |
| unidad de análisis | **DELITO**. Cada delito sufrido es una ocasión distinta de enfrentar la norma de denunciar |

### 1.2 Universo

**Todos los delitos con `BP1_20 ∈ {1,2}`** — es decir, todos aquellos sobre los
que consta si se denunció o no. Contados en P0: **40 280**, sin pérdida
(`BP1_20` está completo). No se restringe por tipo de delito: la norma de
denunciar ante el Ministerio Público aplica a todos.

La corrida **verifica y PARA** si: `BP1_20` tiene valores fuera de `{1,2}`;
`FAC_DEL` no es numérico positivo en toda fila; o `EST_DIS`/`UPM_DIS` faltan.

### 1.3 Desenlace y dicotomización

`BP1_20` — «¿Acudió ante el Ministerio Público o Fiscalía Estatal a denunciar el
delito?» (1 Sí · 2 No).
`BP1_23` — «¿Cuál fue la razón principal por la que no denunció…?», preguntada
solo a quien respondió `BP1_20=2`.

```
evade_norma = 1  ⟺  BP1_20 == 2  Y  BP1_23 ∈ {04, 05, 06, 08}
evade_norma = 0  en cualquier otro caso (denunció, o no denunció por otra razón)
```

| código | etiqueta INEGI | ¿numerador? | por qué |
|---|---|---|---|
| `04` | Pérdida de tiempo | **sí** | la norma se declara **inútil** con esas palabras |
| `05` | Trámites largos y difíciles | **sí** | la norma se declara **costosa e inútil** |
| `06` | Desconfianza en la autoridad | **sí** | la institución que aplica la norma se declara **no fiable** |
| `08` | Por actitud hostil de la autoridad | **sí** | la institución se declara **extractiva/hostil** |
| `01` | Por miedo al (a la) agresor(a) | no | el obstáculo es el agresor, no la norma |
| `02` | Por miedo a que lo (la) extorsionaran | no en el principal | extractiva, pero por **miedo**; va en la sensibilidad A |
| `03` | Delito de poca importancia | no | juicio sobre el delito, no sobre la norma |
| `07` | No tenía pruebas | no | obstáculo probatorio, no juicio sobre la norma |
| `09` / `99` / blanco | Otra / NS-NR / blanco | no | sin contenido interpretable |

Los códigos se **normalizan a dos dígitos con relleno de ceros** antes de
comparar, de modo que `4` y `04` se traten igual sin depender de cómo los escriba
el CSV.

### 1.4 El disparador `sancion_creible: false` — premisa externa, no medición

ENVIPE **no** mide la credibilidad de la sanción, y ninguna fuente del censo lo
hace (P0 · §4: en ENCUCI 2020, `sanci`/`castig`/`impunidad`/`multa` dan cero
aciertos sobre 3 081 líneas de descriptor). Aquí el disparador **se cumple por
construcción del caso**, no por el dato: en México **no existe sanción por no
denunciar un delito del que se fue víctima**, así que `sancion_creible = false`
vale para todo el universo. Es una **premisa jurídica externa declarada como
juicio de este acto**, no un hallazgo de ENVIPE, y así se reportará.

### 1.5 Lo que se estima, dicho con precisión

`BP1_23` solo se pregunta a quien **no** denunció. Por tanto la percepción de
inutilidad de la norma se observa **únicamente entre los evasores**, y la
condicional que la regla escribe —P(evade | enfrenta ∧ norma percibida inútil ∧
sin sanción creíble)— **no es estimable con esta fuente**, ni con ninguna que el
censo haya ubicado.

Lo que se estima es la **conjunta**:

> **p̂ = P( no denunció **y** dio una razón que declara la norma inútil o
> extractiva | enfrentó la norma )**

que es literalmente lo que el encargo pide («proporción que declara incumplir una
norma percibida como inútil»). **No se reportará como si fuera la condicional**, y
esta distinción no se puede diluir después: está congelada aquí.

### 1.6 Ponderador, diseño e intervalo

| campo | valor |
|---|---|
| ponderador | **`FAC_DEL`** — factor de expansión de **delito**, que es la unidad. No `FAC_ELE` (persona) ni `FAC_DEL_AM` (áreas metropolitanas) |
| estrato · UPM | `EST_DIS` · `UPM_DIS` |
| IC95 | bootstrap **conglomerado estratificado**, `n_boot = 10 000`, `seed = 42`, con `wprop_ic_conglomerado` de `tools/calibracion_mordida_encig_serie.py` |
| escala | proporción en [0, 1] |

Nota deliberada: la regla hermana `civico.denuncia.miedo_desconfianza` usó
`wprop_ic_bootstrap`, **sin** conglomerado. Esta pieza usa el estimador
conglomerado porque ENVIPE es muestra por UPM y el intervalo simple sería
demasiado angosto. La diferencia de estimador se declara; no se corrige la pieza
ajena.

### 1.7 Sensibilidades y lectura secundaria — pre-declaradas

- **Sensibilidad A** · añadir `02` («por miedo a que lo extorsionaran») al
  numerador: es la institución declarada **extractiva** de la forma más literal
  posible, pero mediada por miedo. Reportada aparte, nunca como principal.
- **Sensibilidad B** · restringir el universo a delitos con `BPCOD` entre 5 y 15
  (delitos personales), que es el rango que usó `civico.denuncia.miedo_desconfianza`,
  para que el traslape con esa cifra sea auditable.
- **Lectura secundaria** (contexto, **no** es el estimando de la regla):
  P(`BP1_23 ∈ {04,05,06,08}` | `BP1_20 = 2`) — composición de motivos entre quienes
  no denunciaron.

### 1.8 Traslape con una cifra ya medida — declarado antes de medir

`civico.denuncia.miedo_desconfianza` (`milpa/tramite.yaml:258+` y el acumulador,
p=0.294313, `ACTO MAESTRA32-E18`) sale de **la misma fuente y la misma variable**.
No es la misma cantidad, y las diferencias son cuatro:

| eje | `civico.denuncia.miedo_desconfianza` | esta pieza |
|---|---|---|
| unidad | persona (`ID_PER`, colapsando delitos con `max`) | **delito** |
| ponderador | `FAC_ELE` | **`FAC_DEL`** |
| denominador | víctimas que **no** denunciaron | **todas** las víctimas que enfrentaron la norma |
| numerador | `BP1_23 ∈ {1,2,6,8}` («miedo») contra `{3,4,5,7}` («práctica») | `BP1_23 ∈ {04,05,06,08}` («norma inútil o extractiva») |
| IC | bootstrap simple | bootstrap **conglomerado** |

Las dos particiones **se cruzan**: mi numerador toma `06` y `08` de su grupo
«miedo» y `04` y `05` de su grupo «práctica». Ninguna es subconjunto de la otra.
Por eso las dos cifras **no son comparables entre sí** y ninguna valida a la otra.
Se dice ahora, no después de ver los números.

### 1.9 Lo que este resultado no será

- No es «la tasa de evasión de normas en México»: es la de **una** norma concreta
  —denunciar un delito ante el Ministerio Público— elegida porque es la única del
  censo donde conducta, percepción de la norma y ausencia de sanción coinciden.
- La regla `tramite.evasion_norma` distingue en su `nota_segmentacion` dos
  evasiones que el agregado confunde (subsistencia y cinismo de clase alta). Esta
  medición **no** las separa y no pretende hacerlo.
- El prior 0.66 se declara a sí mismo no calibrado y pide expresamente «no
  reportar con decimales». El contraste se hará en esos términos.

---

## §2 · Sello

**El primer resultado que produzca este procedimiento es el que se reporta.**

---

## §3 · RESULTADO (COMMIT-2 de la pieza)

Corrida: `python3 tools/medidor_evasion_norma_envipe25.py`.
Payload `data/raw/envipe2025_csv.zip`,
`sha256 = 8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa`
— el mismo que ya está sellado en `milpa/tramite.yaml` para
`civico.denuncia.miedo_desconfianza`: misma copia del payload, verificado.
Las cuatro guardias de §1.2 pasaron: `BP1_20` sin valores fuera de `{1,2}`,
`FAC_DEL` numérico positivo en las 40 280 filas, `EST_DIS`/`UPM_DIS` completos.

### 3.1 Principal

| campo | valor |
|---|---|
| estimando | P(no denunció **∧** dio una razón que declara la norma inútil o extractiva \| enfrentó la norma) |
| **p̂** | **0.562774** |
| **IC95** | **[0.551982, 0.573448]** |
| n | 40 280 delitos · numerador 21 761 |
| estratos · UPM | 739 · 10 694 |
| población expandida | 35 595 875 delitos |
| ponderador | `FAC_DEL` |

### 3.2 Sensibilidades y lectura secundaria

| variante | p̂ | IC95 | n |
|---|---|---|---|
| **A** · + código `02` (miedo a extorsión) | 0.569696 | [0.559419, 0.579881] | 40 280 |
| **B** · universo `BPCOD` 5-15 (delitos personales) | 0.560515 | [0.547948, 0.572800] | 24 762 |
| *lectura secundaria* · composición entre quienes **no** denunciaron | 0.618640 | [0.606950, 0.629748] | 36 170 |

Las dos sensibilidades mueven el resultado menos de un punto porcentual: la cifra
no depende de dónde se ponga el código `02` ni de si se incluyen los delitos del
hogar. La lectura secundaria (0.6186) **no es el estimando de la regla** — tiene
otro denominador — y se reporta solo como contexto: de cada 100 delitos no
denunciados, 62 lo fueron porque la norma o la autoridad se percibieron inútiles,
lentas, no fiables u hostiles.

### 3.3 Contraste con el prior — **no refutado**

| | prior ASIGNADO | medido | razón |
|---|---|---|---|
| `evade_norma` | 0.66 | **0.562774** | **0.8527** |
| `cumple_norma` | 0.34 | 0.437226 | 1.2860 |

Criterio de refutación del encargo: «más del doble o mitad». La razón es **0.85**:
el prior **no queda refutado**. Error relativo **14.7 %**.

La `nota_calibracion` de esta regla pide expresamente **«no reportar con
decimales»**, y se respeta: leído como la regla misma manda, el prior dice **≈2 de
cada 3** y el dato dice **≈0.56, algo más de la mitad**. La dirección se sostiene
—cuando la norma se percibe inútil y no hay sanción, la mayoría evade— y la
magnitud queda por debajo de lo asignado, sin acercarse al umbral de refutación.

### 3.4 Reservas — todas escritas antes de medir

1. **Es una conjunta, no la condicional de la regla** (§1.5). `BP1_23` solo se
   pregunta a los no denunciantes, así que P(evade | norma percibida inútil) no es
   estimable con esta fuente. Quien cite este número como si fuera la condicional
   lo estará citando mal.
2. **`sancion_creible: false` es premisa jurídica externa** (§1.4), no medición de
   ENVIPE.
3. **Una norma, no las normas.** Es la norma de denunciar un delito ante el
   Ministerio Público. No se generaliza a «evasión de normas en México».
4. **No separa las dos evasiones** que la `nota_segmentacion` de la regla exige
   distinguir (subsistencia y cinismo de clase alta); la fuente no lo permite y
   este acto no lo pretende.
5. **No es comparable con `civico.denuncia.miedo_desconfianza`** (§1.8): distinta
   unidad, distinto ponderador, distinto denominador, particiones cruzadas y
   distinto estimador de intervalo. Que 0.562774 y 0.294313 salgan de la misma
   variable de la misma encuesta **no** los hace confrontables.
