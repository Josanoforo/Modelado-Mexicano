# ACTO FP29-RECONCILIA — el residual de `conf.06` se adjudica con la especificación que ya existía

### 18 de agosto de 2026 · Entorno **UBUNTU** con corpus montado y red · rama `fp29-reconcilia` · base re-derivada `e563e5d`

---

## §0 · Arranque — los cinco de caja, cada uno con su comando

**1 · Worktree propio.** `git worktree add /home/pc0/mm-fp29-reconcilia -b fp29-reconcilia origin/main`. La creación devolvió dos veces `error: could not write config file .git/config: Device or resource busy` — el defecto de contención de `.git/config` que este proyecto ya tiene registrado. **No se dio por buena la salida del CLI:** se verificó el árbol por separado (`git rev-parse HEAD`, `git branch --show-current`, `git status --short`) y el worktree quedó usable.

**2 · SHA re-derivado, no heredado — y el encargo llegó desfasado.** El encargo declara `SHA: 57984b5`. Contra el remoto real:

```
git merge-base --is-ancestor 57984b5 origin/main  → SÍ (es ancestro)
git rev-list --count 57984b5..origin/main         → 8   (al abrir la sesión)
```

`57984b5` es el merge de `PR #262`; `origin/main` ya estaba en `f3d3f95` (merge de `PR #263`, ACTO COND-ATRIB). **Y volvió a moverse durante el propio arranque de esta sesión**: un segundo `git fetch`, hecho antes de escribir una sola línea, encontró `origin/main = e563e5d` (merge de `PR #268`, ACTO B2-SEMANTICO), con `PR #270`, `#272` y `#273` fusionados en medio. La rama se reseteó a `e563e5d` **antes** de congelar esta especificación, no después. **Base de este acto: `e563e5d`.** No se trabaja contra el SHA del encargo: se trabaja contra el terreno.

**3 · Corpus montado, con el manifiesto como fuente-de-qué-hay.** El worktree nace sin `data/raw` (está en `.gitignore:5-6`) — la tercera parte de la firma A.2 daba vacío. Se montó igual que los demás worktrees, por symlink al corpus compartido, más la configuración de raíces:

```
ln -sfn /home/pc0/mm-corpus/raw data/raw
cp /home/pc0/Modelado-Mexicano/data/raices.local.yaml data/raices.local.yaml
ls data/raw/ | head -1   → 20260813130000.export.CSV.zip
ls data/raw/ | wc -l     → 273
ls "/mnt/c/Users/PC0/Descargas MX" | wc -l → 70
```

**4 · Firma de entorno A.2, las tres partes.**

| Parte | Valor derivado en esta sesión |
|---|---|
| `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` | **vacío** → entorno local, no nube |
| Sonda de red | `curl -I https://www.pewresearch.org/` → **HTTP/2 200** (ver §1) |
| Corpus montado (`ls data/raw/ \| head -1`) | **`20260813130000.export.CSV.zip`** → montado, 273 entradas |

Entorno: `Linux FF-5563 6.18.33.2-microsoft-standard-WSL2 x86_64`. Es UBUNTU con corpus y con red — que es lo que este acto exige, porque abre microdato **y** sondea un portal.

**5 · Cifras con comando.** Toda cifra de esta nota trae el comando o el `archivo:línea` que la produce. Las de §3 salen de scripts commiteados en este mismo acto, no de la memoria del modelo.

**Línea base al abrir**, antes de tocar nada: `python3 tests/check.py --baseline` → **19 FAIL · 124 WARN — LÍNEA BASE: VERDE**.

---

## §1 · Verificación del encargo, re-corrida contra el árbol (no heredada de su cabecera)

| Renglón | Lo que el encargo declara | Lo que se verificó en esta sesión | Veredicto |
|---|---|---|---|
| **LA LEY** | notas `2026-08-04-c06a` §5 (qué calcular), §6 (cuáles NO salen de ENCUCI), §7 (qué desbloquea en R8.3), §8 (límite) | `forense/notas/2026-08-04-c06a-cinco-cifras-conf06-localizadas.md`, 172 líneas, leída completa. §5 trae la tabla por cifra; §6 nombra las tres no-ENCUCI; §7 las cuatro condiciones de `R8.3`; §8 el límite de lectura | **SATISFACE** |
| **ESTÁNDAR** | `benchmark-enlace-invarianza` + ADR-76(d)(4)/ADR-80 "argumento de vinculación declarado" | `forense/benchmark-enlace-invarianza-v1_0.md` (146 líneas) §D10 P4/P5/P6, leído completo. `ADR-80` sellado en `canon/gobernanza-v1_15.md:1124` y `:1206`: se adopta **`ARGUMENTO DE VINCULACIÓN DECLARADO`**, *"anclas de diseño + invarianza parcial"*, **no** la invarianza clásica | **SATISFACE** |
| **SERIES** | WVS ✅ manifiesto · Latinobarómetro ✅ manifiesto · Pew ✗ (0) | WVS: **11 entradas** (`grep -n "^- id:.*wvs" data/manifiesto.yaml`), incluido microdato Wave 7 México 2018 en 6 formatos. Latinobarómetro: `latinobarometro2024_bd_stata` (microdato Stata, 6 691 592 B) + cuestionario + fichas. Pew: **0 entradas** (`grep -i pew data/manifiesto.yaml` → vacío) | **PARCIAL — confirmado** |
| **FILA** | `FP-29` ABIERTA con el método ya cableado (ADR-101) | `forense/firmas-pendientes.tsv:30` → `estado=ABIERTA`, `firmada_en` vacío. Puntero de método añadido por `ADR-101(f)` (`gobernanza:1874`) | **SATISFACE** |
| **RESERVA INTOCABLE** | reconciliar `conf.06` NO da falsador a `R8.3` (marca C3) | `c06a` §7 y `ADR-64(e)` lo dicen los dos. Repetida verbatim en §5 de esta nota y en el ADR | **SATISFACE** |

### 1.1 · Hallazgo A.8 del encargo, verificado — y ampliado por un tercer caso que el encargo no nombra

El encargo advierte que **el manifiesto manda sobre la cola vieja**. Verificado, y es peor de lo que dice:

```
$ grep -in "wvs\|pew\|latinobar" data/cola-adquisicion-2026-08-12.tsv
4:WVS            ... url_conocida=VACIO  CANDIDATA(APERTURA_INDETERMINADA)  palanca=3
54:LATINOBARÓMETRO ... url_conocida=VACIO  CANDIDATA(APERTURA_INDETERMINADA)  palanca=53
```

- **WVS** y **Latinobarómetro** figuran en la cola como `CANDIDATA(APERTURA_INDETERMINADA)` con `url_conocida` **vacía** — y las dos están **adquiridas y registradas** en el manifiesto desde el 12/ago y el 5/ago respectivamente, con microdato real en disco. La cola está **estancada**, exactamente el patrón que `manifiesto.yaml usado_para` ya sufrió antes.
- **Pew no aparece en la cola en absoluto** — cero filas. La tercera de las tres cifras que `FP-29` necesita **nunca fue encolada**. Eso no es una cola desactualizada: es una cola incompleta. Se registra en `hallazgos.md`; corregir la cola es acto sucesor, fuera de perímetro.

---

## §2 · COMMIT 1 · Especificación congelada — escrita ANTES de calcular ninguna proporción

*Este commit no contiene ningún resultado. Los resultados viven exclusivamente en §3, en un commit posterior que **no edita esta sección** — se ve en el diff. Es el mismo mecanismo que `C-06b` usó (`0a2f491` espec / `88c7933` resultados) y que `COND-ATRIB` repitió.*

### 2.1 · Qué adjudica este acto, y qué no

`conf.06` está **cerrado** por `ADR-64` (5/ago/2026) — pero cerró solo su mitad ENCUCI. La cláusula (a) del propio ADR lo dice verbatim: *"**Las otras tres cifras del racimo siguen abiertas:** 12% (WVS 2012), 22% (Latinobarómetro/LAPOP) y 18% (Pew 2025) no son ENCUCI y este ADR no las toca — `conf.06` cierra; **«confianza radial — magnitud» como constructo no queda establecida**"*. Ese residual **es** `FP-29`.

**Este acto adjudica el residual: las tres cifras no-ENCUCI.** No reabre, no recalcula y no toca la mitad ENCUCI: las tres cifras selladas (21.8%=`AP5_1_1`, 32.1%=`AP5_1_3`, 62.1%=`AP5_1_2`, las tres a ≥8/10) se **citan** desde `C-06b`, no se vuelven a correr — el encargo lo dice ("ENCUCI ya barrida") y `ADR-64` es la ley que lo sella.

### 2.2 · La ley aplicada, cifra por cifra (`c06a` §5-§6 como especificación)

`c06a` §5 tiene una sola fila para las tres: *"**12%, 18%, 22%** — No aplica reactivo ENCUCI... Reconciliar exige **series temporales de instrumentos externos** (WVS 7 olas, Pew 2025, Latinobarómetro), no una re-corrida sobre ENCUCI."* §6 las nombra una por una. Traducido a la operación de este acto:

| Cifra | Instrumento que el corpus le atribuye | Qué exige la espec | Qué hay en el manifiesto hoy |
|---|---|---|---|
| **12%** | WVS 2012 (=Wave 6), con variantes "WVS Wave 6" y "WVS Wave 7 12-28%" | La serie WVS | **Wave 7 (2018) sí; Wave 6 (2012) NO** |
| **22%** | Tres atribuciones incompatibles: WVS 2018 · ENAFI/WVS · Latinobarómetro+ENAFI+LAPOP · Latinobarómetro/LAPOP | Resolver la procedencia antes de la magnitud | **WVS Wave 7 (2018) SÍ · Latinobarómetro 2024 SÍ · ENAFI no · LAPOP no** |
| **18%** | Pew Research 2025 (28 333 adultos, presencial, 8 ene–26 abr 2025, publicado 1 dic 2025) | La serie Pew | **NO — cero entradas (C1 lo resuelve)** |

### 2.3 · El argumento de vinculación declarado (`ADR-80`), por par — los cuatro ejes: escala, corte, población, año

`ADR-80` sella el estándar: **anclas de diseño + invarianza parcial hasta donde alcance + juicio experto rotulado como tal**, no invarianza clásica. Aplicado aquí, el ancla de diseño es **la redacción del reactivo**, verificada en el cuestionario de cada instrumento, no supuesta:

| Instrumento | Reactivo | Redacción verificada (fuente) | Escala | Población | Año |
|---|---|---|---|---|---|
| **ENCUCI 2020** | `AP5_1_1` | *"En una escala de cero a diez, como en la escuela, donde cero es nada y diez es completamente, en general ¿cuánto confía en… la mayoría de las personas"* (`FD_ENCUCI2020.pdf` p.21, vía `2026-08-03-cal-conf-faseb-pos5-6` :121-125) | **0-10 ordinal**, corte declarado **≥8/10** (`ADR-64`) | 15+, universo completo sin filtro | 2020 |
| **WVS Wave 7 México** | `Q57` | *"En términos generales, ¿diría usted que se puede confiar en la mayoría de las personas o que se tiene que ser muy cuidadoso al tratar con la gente?"* → 1) Se puede confiar en la mayoría de la gente · 2) Se tiene que ser muy cuidadoso (`F00006635-WVS7_Questionnaire_Mexico_2018_Spanish.pdf`, ítem 57) | **binaria, 2 opciones** | 18+ | **2018** (`A_YEAR`, campo del microdato) |
| **Latinobarómetro 2024** | `P10STGBS` | *"Se puede confiar en la mayoría de las personas"* / *"Uno nunca es lo suficientemente cuidadoso en el trato con los demás"* (etiquetas de valor del `.dta`) | **binaria, 2 opciones** | 18+ | **2024** |
| **Pew Spring 2025** | `Q104` | *"Which of the following comes closer to your view?"* → *"Most people can be trusted"* / *"Most people can't be trusted"* (topline, §1) | **binaria, 2 opciones** | 18+, presencial en México | **2025** |

**Lo que el ancla de diseño sí sostiene, declarado como tal:** WVS `Q57` y Latinobarómetro `P10STGBS` son, en español, **el mismo reactivo con redacción casi idéntica en los dos polos** — polo positivo verbatim igual (*"se puede confiar en la mayoría de las personas"*), polo negativo equivalente (*"se tiene que ser muy cuidadoso al tratar con la gente"* / *"uno nunca es lo suficientemente cuidadoso en el trato con los demás"*). Es el ítem clásico de confianza generalizada, en su formulación estándar.

**Lo que NO sostiene, y se dice antes de medir:** Pew `Q104` **no** usa ese polo negativo. Su alternativa es *"most people can't be trusted"* — una afirmación simétrica sobre la desconfianza, no una recomendación de cautela. La literatura de este mismo programa ya tiene el precedente exacto para no borrar esa diferencia (`benchmark-enlace-invarianza` §D10 P6, y `ADR-64` entera): **comparar operacionalizaciones distintas a través de un mismo rótulo fabrica conflictos que no están en el dato.** Se declara como **invarianza parcial de diseño**: los tres binarios comparten constructo y polo positivo; Pew difiere en el polo negativo. No se corrige, no se ajusta: se nombra.

**Prohibición dura, tomada de Bloque A-bis regla 3 y repetida aquí porque es la que este acto podría violar con más facilidad:** **jamás se promedia entre escalas.** Un 0-10 dicotomizado a ≥8/10 y un binario forzado **no son la misma cantidad**, aunque los dos se llamen "% que confía en la mayoría de las personas". Ninguna cifra de §3 combinará ENCUCI con los binarios en un mismo promedio, rango o punto medio. Los binarios sí son comparables **entre sí** (misma escala, mismo reactivo, ancla de diseño verificada); ENCUCI entra como **serie aparte, con su corte pegado al número**.

### 2.4 · Pre-registro B-bis — los tres desenlaces, escritos antes de ver el dato

Bloque B-bis exige declarar qué significa cada desenlace **antes** de correr, incluido el desenlace en que el falsador no refuta. Para cada una de las cinco cifras del racimo de `conf.06`:

- **CONVERGE** → las mediciones de los instrumentos que comparten escala y reactivo caen en un rango estrecho y sin contradicción de procedencia → se adjudica **rango**, con escala y denominador pegados, y la cifra del corpus queda **reproducida** o **corregida** con su fuente.
- **DIVERGE** → las mediciones difieren más allá de sus IC95% → se adjudica **rango con la divergencia nombrada** (qué instrumento, qué año, qué escala la produce). Divergir **no** es fracasar: una serie que se mueve entre 2018 y 2025 es un hallazgo sobre México, no un defecto del acto.
- **INSUFICIENTE** → **INDECIDIBLE**, con la lista explícita de qué faltó (qué ola, qué instrumento, qué archivo). No se rellena con una cifra plausible ni se hereda la del corpus.

**Y el desenlace que B-bis existe para que no se lea como fracaso:** si una cifra del corpus **se reproduce exacta** contra su fuente primaria, eso es corroboración de la cita, y es el resultado más útil de los tres — significa que el corpus citó bien y que la discusión de `conf.06` sobre esa cifra estaba mal planteada, no que la cifra estuviera mal.

**Regla de precedencia, declarada al sellar y no después:** si una cifra puede clasificarse a la vez como CONVERGE (contra su propio instrumento) y DIVERGE (contra otro instrumento del racimo), **manda CONVERGE para la adjudicación de esa cifra**, y la divergencia con el otro instrumento se reporta como divergencia entre series, no como duda sobre la cifra.

### 2.5 · Estimador, declarado antes de correr

`tests/svystat.py::prop_ultimate_cluster` — conglomerado último, el estimador ya sellado del programa, el mismo que produjo la matriz de `C-06b`. No se reimplementa. Se le pasa `(estrato, upm, peso, y)` con `y∈{0,1}`, y devuelve `p̂`, `SE`, `IC95%`, `n_upm`, `n_estratos_singleton`. Diseño declarado por instrumento en §3. Las no-respuestas se **excluyen, no se imputan** (mismo criterio que `C-06b` con el código 99 de ENCUCI).

### 2.6 · Perímetro y límite de este acto

**Dentro:** `data/manifiesto.yaml` (alta de Pew si se obtiene) · `data_raw`/payload · `forense/notas/` (esta nota) · `canon/gobernanza-v1_15.md` (ADR + cascada del conteo) · `forense/firmas-pendientes.tsv` (`FP-29`) · `forense/hallazgos.md` · `forense/encargos/` · `tests/` (script de corrida).

**Fuera, y declarado:** **canon sustantivo NO** — la propagación a las celdas que citan 16-26% es **acto sucesor**, con su cola derivada escrita en §6 de esta nota. No se edita `corpus/reports/` (mismo criterio que `ADR-64(c)`: corregirlos borraría la evidencia de que el error existió). No se adjudica `R8.3`. No se reabre `conf.06`. No se toca `milpa/procedencia.yaml` ni el corte ≥6/10 del motor. Sin `--freeze`.

---

## §3 · COMMIT 2 · La corrida — resultados, puramente aditivo sobre §2

*Este commit no edita §2. Script: `tests/fp29_series_externas.py`, commiteado con estos resultados. Salida cruda: `data/fp29-series-externas-2026-08-18.json`. Estimador `prop_ultimate_cluster` de `tests/svystat.py`, sin reimplementar. Todo microdato se abrió bajo `unshare -Urn` (sin red en el namespace); las descargas se hicieron fuera de él.*

### 3.1 · C1 · Pew — **OBTENIDO**, en 7 intentos, con salida cruda

| # | Intento | Resultado crudo |
|---|---|---|
| 1 | `curl -I https://www.pewresearch.org/` | `HTTP/2 200`, `server: nginx`, `x-powered-by: WordPress VIP` |
| 2 | `wp-json/wp/v2/search?search=interpersonal%20trust` | `HTTP 200`, cuerpo vacío (0 resultados para esa frase) |
| 3 | `wp-json/wp/v2/search?search=trust&per_page=5` | `HTTP_CODE=200 SIZE=2744` — JSON con 5 posts |
| 4 | `/?s=trust+other+people+Mexico` | `HTTP_CODE=301 SIZE=0` (redirección, no útil) |
| 5 | GET del short-read `2025/12/01/where-most-people-trust-others…` | `HTTP_CODE=200 SIZE=426449` |
| 6 | GET del topline `SR_25.12.01_social-trust_topline.pdf` | `HTTP_CODE=200 SIZE=523726 TYPE=application/pdf` |
| 7 | **A.7** — segunda generación del mismo PDF | `HTTP_CODE=200 SIZE=523726`, **sha256 idéntico byte a byte** → sin token de solicitud |

**Desenlace: `obtenido-y-alta`.** No aplica la fórmula de A.5 — no hubo fallo que declarar. **Y el conocimiento previo no se usó:** la URL del topline no se tecleó de memoria, se derivó del `href` del propio short-read, que a su vez salió del buscador JSON del sitio (intento 3). El portal **no** exige registro, pago ni afiliación.

**Altas en el manifiesto**, por `tests/manifiesto.py --registra` (sha256 derivado del archivo real por la herramienta, nunca tecleado), payload al corpus compartido bajo `data/raw/FP29_PEW_2025/`:

| id | archivo | sha256 | bytes | `--verifica` |
|---|---|---|---|---|
| `pew_gas2025_social_trust_topline` | `FP29_PEW_2025/SR_25.12.01_social-trust_topline.pdf` | `103ef06e…41c334` | 523 726 | **COINCIDE** |
| `pew_gas2025_social_trust_shortread` | `FP29_PEW_2025/pew_shortread_20251201.html` | `34457853…10fdd3` | 426 449 | **COINCIDE** |

**A.7 declarado en la entrada:** el topline es estable entre generaciones (verificado). El HTML **no** se declara estable — es una página renderizada; su hash cambiará con menús y banners. Por eso la cifra se adjudica contra el PDF, no contra la página.

### 3.2 · Lo medido — cada instrumento con su escala pegada al número

**Serie externa A · WVS Wave 7 · México** — `n=1 741`, `A_YEAR=2018`, campo Ene–May 2018, `B_COUNTRY_ALPHA=MEX`, archivo `v5.1` (`version` interna `6-0-0 2024-04-15`), sha256 **COINCIDE** con el manifiesto. Peso `W_WEIGHT` · UPM `I_PSU` · estrato `N_REGION_WVS`.

| Reactivo | Escala | p̂ | SE | IC95% | n útil | Codebook WVS |
|---|---|---|---|---|---|---|
| **`Q57`** — se puede confiar en la mayoría de la gente | **binaria** | **10.51%** | 0.84pp | [8.86%, 12.15%] | 1 738 | **10.5** ✔ |
| `Q58` familia — confía completamente+algo | 4 puntos | 91.90% | 0.70pp | [90.53%, 93.28%] | 1 741 | 73.0+18.9 = **91.9** ✔ |
| `Q59` **vecinos** — completamente+algo | 4 puntos | **49.71%** | 1.35pp | [47.07%, 52.35%] | 1 738 | 14.0+35.6 = **49.6** ✔ |
| `Q60` **conocidos** — completamente+algo | 4 puntos | **43.01%** | 1.24pp | [40.58%, 45.44%] | 1 740 | 10.4+32.6 = **43.0** ✔ |
| `Q61` primera vez — completamente+algo | 4 puntos | 13.10% | 0.90pp | [11.33%, 14.87%] | 1 740 | 2.1+11.0 = **13.1** ✔ |

**Verificación independiente, no buscada a propósito:** las cinco celdas se contrastaron contra el **codebook que el propio WVS publica** para México (`F00011928-World_Values_Survey_Wave_7_2017-2020_Mexico_v3.0.pdf`, tablas `Q57`-`Q61`, `(N)=1,741`). **Coinciden las cinco**, hasta la décima. No es una corroboración de la cifra del corpus: es la validación de mi recodificación y de mi estimador contra la tabulación del productor. Cero estratos singleton en las cinco.

**Serie externa B · Latinobarómetro 2024 · México** — archivo de 17 países, `n_total=19 214`, `n_México=1 200`, `NUMINVES=24`, sha256 **COINCIDE**. Peso `WT` · UPM `CIUDAD` · estrato `TAMCIUD` (proxies declarados: Latinobarómetro **no publica** identificadores formales de estrato/UPM — la varianza es aproximada, y se dice).

| Reactivo | Escala | p̂ | SE | IC95% | n útil |
|---|---|---|---|---|---|
| **`P10STGBS`** — se puede confiar en la mayoría de las personas | **binaria** | **26.06%** | 1.84pp | [22.45%, 29.67%] | 1 183 |

2 estratos singleton de 8 (declarados, no forzados a cero).

**Verificación independiente, tampoco buscada a propósito.** `corpus/reports/Sanción_Social_Horizontal…md:73` afirma: *"Latinobarómetro 2024: **15% regional, 26% México**"*. Recalculado desde el microdato crudo, país por país:

```
México  26.06%   ← el MÁS ALTO de los 17 países
media simple de los 17 países : 15.62%
mediana de los 17 países      : 15.34%
agregado ponderado por n      : 15.60%
```

**Las dos cifras del corpus reproducen.** Y con ellas viene un hecho sobre México que el corpus tiene medido y no dice: **en Latinobarómetro 2024, México es el país con MAYOR confianza interpersonal generalizada de los 17 de América Latina** — por encima de Argentina (24.4%), Chile (21.0%), Colombia (15.3%), Perú (10.0%) y Brasil (5.0%). "Baja confianza" es cierto en absoluto; **"baja para la región" es falso en este instrumento y en esta ola.**

**Serie externa C · Pew · Global Attitudes Spring 2025** — leído del topline `Q104`, no de microdato (Pew no publica microdato internacional en esta entrega). Escala **binaria**.

| País | Spring 2025 | Spring 2024 |
|---|---|---|
| **México** | **18%** | **17%** |
| Turquía (la más baja) | 14% | 14% |
| Suecia (la más alta) | 83% | — |

Denominador declarado por el propio Pew: 28 333 adultos en 24 países no-EE.UU., 8/ene–26/abr 2025; **presencial en México**. El topline **no publica la `n` de México ni SE por país** — por eso esta serie entra **sin IC**, y se dice.

**Serie D · LAPOP/AmericasBarometer · México — `it1`, y NO es el reactivo que el racimo discute**

| Ola | Reactivo | Escala | p̂ | IC95% | n útil |
|---|---|---|---|---|---|
| 2019 | `it1` la gente de su comunidad, muy+algo confiable | 4 puntos | 54.03% | [51.14%, 56.92%] | 1 525 |
| 2021 | idem | 4 puntos | 53.63% | [51.49%, 55.76%] | 2 925 |
| 2023 | idem | 4 puntos | 55.44% | [52.44%, 58.44%] | 1 609 |

*Reserva de diseño en 2021: `upm` toma un valor distinto por observación (UPM = n = 2 925), es decir el identificador de conglomerado es degenerado en esa ola — el IC de 2021 se lee como aproximación de muestreo simple, no como conglomerado último. Declarado, no corregido.*

**El punto sustantivo de esta serie no es su magnitud, es su existencia.** Se hizo la prueba directa sobre el cuestionario ABMex2023 (`lapop_abmex2023_cuestionario.pdf`, en el manifiesto):

```
grep -i "mayoría de las personas|mayoría de la gente|se puede confiar en la mayor|suficientemente cuidadoso"
→ CERO coincidencias
```

**LAPOP no fielda el reactivo de confianza generalizada.** Su único ítem interpersonal es `it1`, sobre *"la gente de su comunidad"*, en escala de 4 puntos.

---

## §4 · La adjudicación — las cinco cifras (más la sexta), con escala y denominador

*Regla de precedencia aplicada tal como se declaró en §2.4: donde una cifra converge contra su propio instrumento y diverge contra otro, manda CONVERGE para la cifra, y la divergencia se reporta como divergencia entre series.*

| # | Cifra | Atribución del corpus | Veredicto | Escala y denominador |
|---|---|---|---|---|
| 1 | **12%** | WVS 2012 (Wave 6) | **INDECIDIBLE — falta la ola** | La Wave 6 (2012) **no está en el manifiesto**; solo la Wave 7. Lo que sí queda fijo: el punto **2018** de esa misma serie es **10.5%** (binaria), no 22% |
| 2 | **21.8%** | ENCUCI 2020 `AP5_1_1` | **SELLADA, no se toca** (`ADR-64`) | 0-10, corte **≥8/10**, `FAC_SEL`, universo completo. `C-06b`: 21.9% [21.1, 22.7], n=21 409 |
| 3 | **22%** | WVS 2018 · ENAFI/WVS · Latinobarómetro · LAPOP | **DIVERGE — dos atribuciones REFUTADAS, una es error de categoría, una INDECIDIBLE** | ver §4.1 |
| 4 | **32.1%** | ENCUCI 2020 `AP5_1_3` | **SELLADA, no se toca** (`ADR-64`) | 0-10, ≥8/10. `C-06b`: 32.3% [31.3, 33.3], n=21 403 |
| 5 | **18%** | Pew Research 2025 | **CONVERGE — REPRODUCIDA EXACTA contra fuente primaria** | binaria, `Q104`, Spring 2025 GAS, presencial en México. Topline: **18** (2025), 17 (2024). Sin IC: Pew no publica SE por país |
| 6 | **62.1%** | ENCUCI 2020 `AP5_1_2` | **SELLADA, no se toca** (`ADR-64`) | 0-10, ≥8/10. `C-06b`: 62.2% [61.2, 63.3], n=21 445 |

### 4.1 · El 22%, atribución por atribución — que es lo que `FP-29` pedía

`FP-29` está redactada así: *"el 22% no es una cifra: son tres atribuciones distintas de la misma cifra en cuatro documentos… No se puede elegir entre tres cifras cuando una no sabe de dónde viene."* Este acto no elige entre cifras: **prueba cada atribución contra su propio instrumento.**

| Atribución | Dónde | Prueba corrida | Resultado |
|---|---|---|---|
| **WVS 2018** | `Confianza_y_Desconfianza…md:9` (*"~22% (WVS 2018)"*); `Moral_Emotions…md:29,186` (*"22% (ENAFI/Encuesta Mundial de Valores)"*) | Medido `Q57` en el microdato Wave 7 México 2018 | **REFUTADA.** WVS 2018 = **10.51%** [8.86, 12.15]. El 22% queda **9.85 pp por encima del límite superior**. Doblemente confirmado: mi corrida **y** el codebook publicado por WVS (10.5) |
| **Latinobarómetro** | `glosario-v5_6.md:84` (*"22% (Latinobarómetro/LAPOP)"*); `Moral_Emotions…md:84` | Medido `P10STGBS`, la única ola en el manifiesto (2024) | **NO SOSTENIDA para 2024** = **26.06%** [22.45, 29.67]; el 22% cae **por debajo** del límite inferior. Sin ola contemporánea a la cita, no se puede refutar para *otra* ola — se dice, no se estira |
| **LAPOP** | `glosario-v5_6.md:84`; `Moral_Emotions…md:84` | Grep sobre el cuestionario ABMex2023 + medición de `it1` en 3 olas | **REFUTADA POR ERROR DE CATEGORÍA.** LAPOP **no tiene** el reactivo generalizado (cero coincidencias). Lo que sí mide, `it1` sobre "la gente de su comunidad" (4 puntos), da **54.0 / 53.6 / 55.4%** en 2019/2021/2023 — otro constructo, otra escala, y a 30 puntos del 22% |
| **ENAFI** | `Moral_Emotions…md:29,84` | Búsqueda en el manifiesto | **INDECIDIBLE.** `grep -ci enafi data/manifiesto.yaml` → **0**. El instrumento no está adquirido; no se opina sobre él |

**Veredicto del 22%, con la divergencia nombrada:** de las cuatro atribuciones que circulan, **dos quedan refutadas contra microdato** (WVS 2018; LAPOP, esta por error de categoría), **una no se sostiene en la única ola disponible** (Latinobarómetro 2024) y **una es indecidible por falta del instrumento** (ENAFI). **Ninguna fuente verificable en el corpus sostiene hoy el 22% como magnitud de confianza interpersonal generalizada en México.** La cifra no queda sustituida por otra: queda **sin procedencia sostenible**, que es precisamente lo que `FP-29` sospechaba y no había probado.

### 4.2 · La hipótesis que emerge, declarada como hipótesis y NO adjudicada

De las siete cantidades medidas o selladas para "la mayoría de las personas" en México, **una sola contiene el 22% en su IC95%: ENCUCI `AP5_1_1` a ≥8/10 — 21.9% [21.1%, 22.7%]**.

Es una coincidencia numérica **sugerente y no suficiente**, y este acto se niega a convertirla en adjudicación por tres razones escritas antes de verla:

1. **`ADR-64(a)` ya declaró el 22% como no-ENCUCI.** Revertir un ADR exige, por su propia cláusula de reversión, *"corrida nueva pre-registrada contra microdato que contradiga la matriz de `C-06b` §3 (no por relectura de reports, no por una cifra nueva sin corte declarado)"*. Una coincidencia de intervalo no es eso.
2. **Es exactamente el modo de fallo que `ADR-64` existe para impedir**: identificar cifras entre sí por proximidad numérica, sin verificar reactivo y corte, es como se fabricó `conf.06` en primer lugar.
3. **Ninguno de los cuatro documentos que citan el 22% menciona ENCUCI**; los cuatro nombran instrumentos externos. Adjudicarlo a ENCUCI sería sustituir la atribución del autor por la del ejecutor.

**Se deja como hipótesis nominada para el acto sucesor**, con la prueba que la resolvería: rastrear la cadena de citas de los cuatro documentos hasta su fuente publicada. **No es una tarea de microdato — es de procedencia documental.**

### 4.3 · Hallazgo nuevo de vinculación: el ancla de diseño no sostiene ni el ORDEN

Esta es la aportación de este acto al estándar `ADR-80`, y no estaba pedida.

Los dos pares de ítems mejor emparejados entre ENCUCI y WVS son casi verbatim: *"la mayoría de las personas que conoce personalmente"* ↔ *"people you know personally"*, y *"las personas que viven en su colonia y localidad"* ↔ *"your neighborhood"*. Bajo el ancla de diseño de `ADR-80`, ese es el mejor caso posible. Y sin embargo:

| Instrumento | conocidos | vecinos | Orden |
|---|---|---|---|
| **ENCUCI 2020** (0-10, ≥8) | **62.2%** | 32.3% | conocidos **>** vecinos, por **29.9 pp** |
| **ENCUCI 2020** (0-10, ≥6) | **77.9%** | 55.4% | conocidos **>** vecinos, por **22.5 pp** |
| **WVS 2018** (4 pts, compl+algo) | 43.0% | **49.7%** | vecinos **>** conocidos, por **6.7 pp** |
| **WVS 2018** (4 pts, solo "completamente") | 10.4% | **14.0%** | vecinos **>** conocidos, por **3.6 pp** |

**El orden se invierte entre los dos instrumentos, y la inversión es robusta al corte en los dos.** Esta comparación **no viola Bloque A-bis regla 3**: no compara niveles entre escalas distintas — compara el **orden interno de cada instrumento**, que es lo único comparable sin función de enlace.

**Qué significa, dicho con cuidado.** El ancla de diseño (redacción casi idéntica, misma referencia metodológica de la OCDE 2017 que `benchmark-enlace-invarianza` §D10 P5 documenta) **no garantizó ni siquiera invarianza de orden** — el nivel más débil de acuerdo imaginable. Es evidencia empírica directa, medida en este acto, de la reserva que el propio benchmark declaró: *"eso es un ancla de **diseño**, no un ancla **estadísticamente verificada** — la distinción que la literatura de invarianza exige no borrar"*. **Hipótesis nombrada y no adjudicada:** efecto de orden de batería (en WVS la secuencia es familia → vecinos → conocidos → desconocidos, que encuadra "conocidos" como *más lejano* que vecinos; en ENCUCI es mayoría → conocidos → colonia). Resolverlo exige un diseño que este acto no tiene.

### 4.4 · Segunda divergencia medida: dos binarios, el mismo año, 9 puntos de diferencia

| Instrumento | Año | Escala | México |
|---|---|---|---|
| Pew `Q104` | **2024** | binaria | **17%** |
| Latinobarómetro `P10STGBS` | **2024** | binaria | **26.06%** [22.45, 29.67] |
| WVS `Q57` | 2018 | binaria | 10.51% [8.86, 12.15] |
| Pew `Q104` | 2025 | binaria | 18% |

**Mismo año, misma escala, mismo constructo, y 9 puntos de separación** — con el 17% de Pew fuera del IC95% de Latinobarómetro. Esto no es ruido: es divergencia de instrumento.

**Y la explicación obvia no funciona — se dice en vez de ocultarse.** En §2.3 se pre-registró que Pew usa un polo negativo distinto (*"most people can't be trusted"*, una afirmación fuerte) frente al polo suave de WVS/Latinobarómetro (*"se tiene que ser muy cuidadoso"* / *"uno nunca es lo suficientemente cuidadoso"*). Un polo negativo suave es más fácil de endosar, así que debería **deprimir** el % de confianza. Eso **explica** WVS (10.5%, polo suave) **<** Pew (17-18%, polo duro), pero **queda contradicho** por Latinobarómetro (26.1%, polo suave) **>** Pew. **La redacción del polo negativo no basta para explicar la dispersión.** Queda nombrada, sin resolver.

**Consecuencia para el constructo, que es lo que `FP-29` gatea:** el rango medible hoy para "confianza interpersonal generalizada en México" es **10.5% – 26.1%** entre instrumentos binarios (2018–2025), y **21.9%** en ENCUCI 0-10 a ≥8/10 (2020) — **cifra que NO se promedia con las anteriores**, porque son escalas distintas y hacerlo es el error de categoría que Bloque A-bis regla 3 prohíbe. El rango de los binarios y el punto de ENCUCI se reportan **por separado, cada uno con su escala pegada**.

---

## §5 · COMMIT 3 · Cierre — `ADR-111`, `FP-29` ejecutada, `FP-58` abierta

**`PR #275`** (`https://github.com/Josanoforo/Modelado-Mexicano/pull/275`), borrador, base `main`, `MERGEABLE` verificado contra el remoto —no contra el texto del CLI, que volvió a dar `could not write config file .git/config: Device or resource busy` al empujar (`git ls-remote --heads origin fp29-reconcilia` → `26c34da`, idéntico a mi `HEAD`).

**`ADR-111`**, sellado en `canon/gobernanza-v1_15.md`. Número derivado, no supuesto: contra `e563e5d`, `únicos 109 · max 109 · huecos []` → **110 contiguo**. *(El encargo decía "ADR base 104"; quedó desfasado por cuatro ADR entre su redacción y su ejecución.)* **Colisión declarada:** `PR #267`, abierto al escribir esto, reclama `ADR-107`, número ya tomado en `main` por `ADR-109`/`B2-SEMANTICO` — **esa colisión es de `PR #267`, no de este acto**; queda en `hallazgos.md`. Renumera quien fusione después; `T15` arbitra.

**Cascada del conteo, derivada por la receta de `T15`** (`grep -rn "[0-9]\+ ADR" canon/ README.md`): `gobernanza-v1_15.md:2` (109→110) · `estado-programa-v1_10.md:27` (tabla) · `estado-programa-v1_10.md:101` (§L0). Verificado después: `grep -rn "109 ADR" canon/ README.md` → **sin resultados**.

**Tablero.** `FP-29` → **`FIRMADA`**, con `ejecutada_en` apuntando a este acto. Sin firma nueva de mesa, y la razón está escrita en `ADR-111(a)`: `ADR-101(f)` ya había establecido que *"el pendiente real = solo la adquisición de las series"* — es decir, ejecución, no decisión. Mismo patrón que `FP-44`/`FP-45` bajo `ADR-94`. **Fila nueva `FP-58`, `ABIERTA`** (max era 57, sin huecos) para lo que sí es de mesa: qué hace el canon con una cifra sin procedencia sostenible, con las tres opciones enunciadas y sin recomendación del ejecutor. Conteo: `FIRMADA` 44→45, `ABIERTA` 10→10 (−1 por `FP-29`, +1 por `FP-58`).

**Nota de método sobre la edición del tablero, porque casi se convierte en un defecto.** El primer intento usó el módulo `csv` de Python y **despojó las comillas de 11 filas ajenas** en un solo round-trip (`git diff --numstat` dio `44 43` donde debía dar `2 1`). Se revirtió con `git checkout --` y se rehizo por **edición de línea, byte-preservante**. Verificado después: `2 1`, 59 líneas × 9 columnas, `FP-33` intacta. Registrado en `hallazgos.md` — es la tercera vez que este cepo muerde en este proyecto y **ningún test lo vigila**.

---

## §6 · Cola derivada para el acto sucesor — las celdas que citan el 22%

*Derivada por comando, no por memoria, y curada a mano para quitar los falsos positivos (Nu Bank "23% de bancarizados", Mitofsky 51.4%, ENIF 36.6% — llevan "22"/"26" pero no son magnitud de confianza interpersonal).* **Este acto no toca ninguna de estas celdas** — son de `FP-58`.

| Archivo:línea | Qué dice hoy | Qué le hace `ADR-111` |
|---|---|---|
| `canon/glosario-v5_6.md:84` | *"quedan 12% (WVS 2012), **22% (Latinobarómetro/LAPOP)** y 18% (Pew 2025) **sin reconciliar** contra ENCUCI"* | **Ya no describe el árbol.** Están reconciliadas: 18% reproduce exacto, 22% no se sostiene, 12% indecidible. La atribución "Latinobarómetro/LAPOP" es la refutada |
| `canon/glosario-v5_6.md:321` | entrada `conf.06`, cerrada por `ADR-64` | Sin cambio en el cierre; el residual ya no está abierto de la misma forma |
| `canon/gobernanza-v1_15.md:2173` | tabla de pendientes, fila `conf.06` con las cinco cifras | Igual |
| `canon/modelo-decision-v4_0.md:554` | §5.0 regla 3, *"ninguna cifra… como establecida salvo tres"* | Las otras tres dejan de estar simplemente "no establecidas": una está confirmada, una refutada, una indecidible |
| `canon/estado-programa-v1_10.md:208` | `conf.06` resuelto por `ADR-64` | Igual |
| `corpus/reports/Confianza_y_Desconfianza…:9` | *"~22% (WVS 2018)… 33% en 1990 → mínimo 16% en 2005, con recuperación parcial"* | **Atribución refutada** (WVS 2018 = 10.5%) **y trayectoria refutada en su punto final** |
| `…:71` | *"baja (~16-22%)… confirmado por WVS (7 oleadas), Latinobarómetro…"* | El extremo superior del rango no tiene fuente sostenible |
| `…:225` | *"Dinamarca 74% vs. México ~22%"* | Comparación internacional apoyada en la cifra sin procedencia |
| `…:295` | *"la interpersonal cayó de 33% a 16% pero se recuperó parcialmente a 22%"* | La "recuperación parcial" es justamente lo que el 10.5% de 2018 no sostiene |
| `corpus/reports/Moral_Emotions…:29, :84, :186` | *"22% (ENAFI/Encuesta Mundial de Valores)"*, *"(Latinobarómetro, ENAFI, LAPOP)"* | Tres de las cuatro atribuciones, dos refutadas y una indecidible |
| **`milpa/refutations.yaml:453`** | `evidencia_contraria:` *"la interpersonal cayó de 33% a 16% y se recuperó…"* | **Es la única celda de la capa ejecutable en la cola** — una refutación se apoya en la trayectoria refutada. Prioridad alta para el sucesor |
| `corpus/reports/Non-Family_Social_Capital…:12` | Pew 1/dic/2025, 18%, *"segundo más bajo tras Turquía (14%)"* | **No entra a la cola: quedó CONFIRMADA exacta contra el topline primario.** Se lista para que el sucesor no la toque por error |

---

## §7 · Auditoría — qué mueve este acto sobre México, y qué no

**Sí mide México.** Este acto produce **cinco cantidades nuevas medidas sobre población mexicana** (WVS `Q57`/`Q58`/`Q59`/`Q60`/`Q61`, Wave 7, n=1 741), **una** más (Latinobarómetro `P10STGBS` 2024, n=1 183), **tres** de LAPOP (`it1`, 2019/2021/2023) y **lee dos** de fuente primaria (Pew 2024/2025). En total, **once cantidades** que antes no estaban medidas en este programa.

**Qué mueve: magnitud de constructo.** "Confianza radial — magnitud" pasa de *"cinco cifras, tres sin reconciliar"* a: tres selladas en ENCUCI (`ADR-64`), una confirmada exacta (Pew 18%), una sin procedencia sostenible (22%) y una indecidible por falta de ola (12%). Y aporta un rango medible declarado por escala: **10.5%–26.1% entre binarios (2018-2025)**, **21.9% en ENCUCI 0-10 a ≥8/10 (2020)**, **nunca promediados entre sí**.

**Qué NO mueve: coeficientes.** **Contadores movidos: 0.** Ni el de condicionales medidas (`12 de 15`), ni el de coeficientes, ni probabilidades del motor, ni fichas del Hito D. No se editó `milpa/procedencia.yaml`, no se tocó el corte ≥6/10 de `radio_confianza`, no se adjudicó `R8.3`. La reserva C3 de `C-06a` §7 sigue vigente y está repetida verbatim en `ADR-111(g)`.

**Sesgo de marcos — WVS, Latinobarómetro y Pew son evidencia (c), y por eso existe la vinculación declarada.** Los tres son instrumentos comparativos internacionales diseñados fuera de México, con un reactivo binario nacido en la literatura anglosajona de capital social. Traerlos a decir algo sobre México exige exactamente lo que `ADR-80` sella: **un argumento de vinculación declarado**, no la suposición de que "confianza interpersonal" significa lo mismo en los cuatro instrumentos. Este acto lo declaró por los cuatro ejes (§2.3) **y encontró que el ancla más fuerte disponible falla** (§4.3): el orden se invierte. Es la crítica calibrada de marcos que Bloque A exige, hecha con una medición y no con una advertencia genérica.

**¿Qué parte podría confundir estructura con "cultura"?** El hallazgo de §3.2 lo corta en su propio terreno: en Latinobarómetro 2024 **México es el país con MAYOR confianza interpersonal de los 17 de América Latina** (26.06%, por encima de Argentina 24.4% y Chile 21.0%; Brasil 5.0% es el más bajo). La lectura *"México, sociedad de baja confianza"* es cierta contra el promedio de la OCDE y **falsa contra su propia región** en ese instrumento y esa ola. Cualquier explicación cultural que trate la baja confianza como rasgo mexicano tiene que explicar por qué México encabeza la región.

**¿Sobregeneralización desde clases medias urbanas?** No aplica a las cifras de este acto — las tres series son nacionalmente representativas con ponderador propio. Sí aplica una reserva de diseño declarada: Latinobarómetro y LAPOP **no publican identificadores formales de estrato/UPM**, así que sus IC usan proxies (`TAMCIUD`/`CIUDAD`, `estratopri`/`upm`) y son aproximados. Está dicho en §3.2, no escondido.

---

## §8 · Límite de lectura y de escritura declarado

**Abierto en esta sesión:** microdato WVS Wave 7 México (CSV v5.1, dentro de su zip) · microdato Latinobarómetro 2024 (`.dta` español, 17 países) · microdato LAPOP México 2019/2021/2023 (`.dta`) · cuestionario WVS7 México español (PDF) · codebook WVS7 México v3.0 (PDF) · cuestionario LAPOP ABMex2023 (PDF) · topline Pew Spring 2025 (PDF) · short-read Pew (HTML). **Todo bajo `unshare -Urn`**; las descargas se hicieron fuera del namespace.

**Leído del repo:** `2026-08-04-c06a…` (completo) · `benchmark-enlace-invarianza-v1_0.md` (completo) · `ADR-64`, `ADR-80`, `ADR-82`, `ADR-101(f)`, `ADR-109` en `gobernanza` · `2026-08-05-c06b…` (§3, tabla) · `2026-08-03-cal-conf-faseb-pos5-6…` (§1.1, enunciado ENCUCI) · `firmas-pendientes.tsv` (fila `FP-29`) · `instrucciones-proyecto-v2_10.md` (A.2, A.3, A.5-A.8, A.12, Bloques A-bis y B-bis) · `tests/svystat.py`, `tests/corpus.py`, `tests/manifiesto.py` · las celdas del corpus citadas una por una en §6.

**NO abierto:** ENCUCI 2020 — **deliberadamente**. Su mitad está sellada por `ADR-64` sobre `C-06b` y reabrirla sin encargo sería rehacer trabajo sellado; todas sus cifras aquí se **citan** de `C-06b`, con `archivo:línea`. Tampoco WVS Wave 6, ni ENAFI (no adquiridos — es lo que los deja INDECIDIBLES).

**NO editado:** `canon/glosario-v5_6.md` · `canon/modelo-decision-v4_0.md` · `milpa/procedencia.yaml` · `milpa/refutations.yaml` · `corpus/reports/**` · `forense/hitoD-preregistro-v2_0.md` · `data/cola-adquisicion-2026-08-12.tsv` · `tests/check.py` · `tests/baseline.json` (**sin `--freeze`**). Las 49 entradas del manifiesto con ruta rota **no se corrigieron** — están registradas en `hallazgos.md` y son acto sucesor.

**Renombre de este archivo, declarado.** La nota se llamaba `2026-08-18-fp29-reconcilia.md` y `T02` la marcó por **colisión de nombre normalizado** con el encargo archivado (`2026-08-18-FP29-RECONCILIA.md`): `T02` normaliza quitando todo lo no alfanumérico y bajando a minúsculas, con lo que los dos daban `20260818fp29reconciliamd`. Renombrada a `2026-08-18-fp29-adjudicacion.md` — que además es lo que el encargo pide de ella ("ficha de adjudicación en notas") — y las cinco referencias se actualizaron por comando (`gobernanza`, `firmas-pendientes.tsv`, el encargo, el script y el manifiesto); `grep` posterior del nombre viejo → sin resultados. Mismo remedio que ya se autorizó en `ACTO APERTURA-ISSP`. Con eso, la corrida vuelve a **19 FAIL · 124 WARN — LÍNEA BASE: VERDE**, idéntica a la de apertura: el `T16` que también apareció era consecuencia aritmética del `FAIL` de `T02`, no un desajuste propio, y se fue con él. **`estado-programa:291` no se tocó** — su cifra sigue siendo la correcta.

**Escrito:** este archivo · `forense/encargos/2026-08-18-FP29-RECONCILIA.md` · `canon/gobernanza-v1_15.md` (`ADR-111` + cabecera) · `canon/estado-programa-v1_10.md` (solo las dos líneas del contador) · `forense/firmas-pendientes.tsv` (`FP-29`, `FP-58`) · `forense/hallazgos.md` (append) · `data/manifiesto.yaml` (2 altas) · `data/fp29-series-externas-2026-08-18.json` · `tests/fp29_series_externas.py` · `data/raw/FP29_PEW_2025/` (payload, no commiteado).
