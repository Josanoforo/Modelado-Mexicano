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
