# ACTO RETRIAGE-4 — nota de cierre

**20 de agosto de 2026 · entorno UBUNTU · modelo Opus · `origin/main = 54da215` · `ADR-138`**
**Encargo:** `forense/encargos/2026-08-20-RETRIAGE-4.md` (`FP-86`, firma de mesa verbatim: «**A1**»).

---

## 0 · ARRANQUE, las cinco líneas

**1 · REPO.** Clon existente `/home/pc0/Modelado-Mexicano`, refrescado; worktree propio en `/home/pc0/mm-retriage-4`, rama `retriage-4`. `git log -1 --format="%h %s"` → `54da215 Merge pull request #306 from Josanoforo/claude/repara-t22-firmas-u7q8xv`. `git status` limpio al arrancar.

**2 · SHA.** El encargo se escribió contra `54da215`. Al arrancar, `main` local estaba en `9f4ea60`, **33 commits detrás** de `origin/main`. **No es PARO** (regla del propio ARRANQUE): se refrescó por `merge --ff-only`, se re-derivó todo el perímetro contra el árbol nuevo y se reporta la diferencia aquí. El worktree nació de `origin/main`, no del `main` viejo.

**3 · `data/raw`.** No existía en el worktree nuevo. **La enlacé** a `/home/pc0/mm-corpus/raw` (`ln -s`, exit 0; `data/raw -> /home/pc0/mm-corpus/raw`). No se escribió ni un byte en el corpus compartido: este acto no descarga nada.

**4 · ENTORNO — las TRES partes de `A.2`, no dos.**

```
CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE   → sin_variable
curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/   → 200
ls data/raw/ 2>/dev/null | head -1    → 20260813130000.export.CSV.zip
```
Corpus montado: **289 entradas, 7.2 G**.

**5 · ESPEJO.** Ninguna cifra de este acto sale del espejo del proyecto. Todas salen del clon de (1), con el comando a la vista.

**Y una nota de infraestructura, no de contenido:** `git worktree add` emitió dos veces `error: could not write config file .git/config: Device or resource busy`. Es el bind-mount de sandbox ya diagnosticado en el programa, **no** un fallo de git: el worktree quedó creado y correcto, verificado por `git log -1` y `git branch --show-current` dentro de él.

---

## 1 · `T0` — el numerador, con receta probada

El encargo se negó a pasar la cifra de partida: *"intenté derivarla y mi receta dio 3 contra el 13 declarado. La receta estaba mal y no heredo un número que no pude reproducir."* **Tenía razón en no heredarlo, y su `3` tiene explicación exacta.**

**La receta:**

```bash
awk '/^## Registro de veredictos archivados/{f=1;next} f && /^## /{f=0} f' \
    forense/hitoD-preregistro-v2_0.md \
  | command grep -oP '^`R[0-9]+\.[0-9]+`(?= → veredicto `[A-E]`)' \
  | sort -u | wc -l
```

Recorta al bloque designado por `ADR-40` —la única sección que un test puede leer, por diseño— y **deduplica ids**, que es la parte que decide: el bloque tiene **14 líneas** y **13 reglas distintas**, porque `R4.3` ocupa dos líneas (mitad A y mitad B). Contar líneas da 14; contar reglas da 13, y el denominador de 27 es de reglas.

**Probada contra cuatro estados históricos cuya respuesta el propio archivo declara** — no contra la respuesta de hoy:

| SHA | fecha | receta | lo que el archivo declaraba en ese estado |
|---|---|---|---|
| `d962906` | 3/ago | **3** | `Nota 12`, escrita al día siguiente: *"el contador (`3 de 27`)"* |
| `5fb3d5b` | 4/ago | **11** | `11 de 27` |
| `09a48e1` | 4/ago | **12** | `12 de 27` |
| `665188d` | 5/ago | **13** | `13 de 27` |
| `HEAD` antes de este acto | 20/ago | **13** | `13 de 27` |

**Cuadra en los cinco.** Es además la misma receta que el oráculo `T18` implementa (conjunto de ids dentro del bloque designado, `tests/check.py:_VEREDICTO_CANONICO`), y la misma que `CONF-17` corrida B corrió el 5/ago obteniendo `13` — dos verificaciones independientes que no se buscaron.

**De dónde salía el `3` del encargo:** es el contador **vigente el 3/ago/2026**, correcto en su momento y citado después en prosa. No era una receta rota; era una cifra correcta de otro instante leída como si fuera de hoy. **Es exactamente el defecto que `ADR-40` creó el bloque designado para impedir**, y sobrevivió porque la prosa que lo cita sigue ahí, como debe (append-only).

---

## 2 · `T0` — los instrumentos, `A.1`, una invocación por `--id`

Cuatro invocaciones separadas, salida cruda en `/scratchpad` y pegada aquí en su forma útil:

| `--id` | raíz | resultado |
|---|---|---|
| `zenodo_electoral_precinct_level_mexico_municipal` | `data_raw` | **COINCIDE** — `sha256` y 739,952,144 bytes |
| `r7_3_pub_beneficiarios_bienestar_csv` | `data_raw` | **COINCIDE** — 114,046 bytes |
| `r8_1_contraloria_social_2019_2025_csv` | `data_raw` | **COINCIDE** — 520 bytes |
| `adq15_brasdefer_actos_de_habla` | `data_raw` | **COINCIDE** — 262,019 bytes |

**Ninguna de las tres respuestas que no se colapsan se disparó**: cero `AUSENTE`, cero `raíz-no-configurada`, cero `hash-discordante`. El resumen por raíz salió sin colapsar en las cuatro: `data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0`.

---

## 3 · La premisa del encargo, verificada contra el árbol

El encargo afirmaba que `R7.1` · `R7.3` · `R8.1` · `R10.1` son *"las únicas sin declaración previa de inejecutabilidad y sin triar"*. **Verificado por comando, no por lectura:**

- Las 27 fichas, por encabezado: `command grep -cE "^## R[0-9]" forense/hitoD-preregistro-v2_0.md` → **27**.
- Las 13 archivadas, por la receta de §1.
- La diferencia da **14 abiertas**: `R1.4 R2.1 R2.2 R3.4 R7.1 R7.3 R7.4 R7.5 R8.1 R8.2 R8.3 R10.1 R10.2 R10.3`.
- Menos las **nueve** pre-registradas como probable `D` (`R1.4 R2.1 R2.2 R7.4 R7.5 R8.2 R8.3 R10.2 R10.3`) y `R3.4` (bloqueada por spec, asignada a `EMISOR-M`) → quedan **exactamente las cuatro**.
- *"Sin triar"* también se verificó: las **siete** fichas B-bis que existen (`hitoD-R1_1|R4_1|R4_2|R4_3|R7_2|R9_1|R9_2-bbis-triage-v1_0.md`) son todas de reglas ya archivadas. **Ninguna de las cuatro tenía ficha B-bis ni especificación congelada previa.**

**La premisa del encargo se sostiene entera.** Se dice porque no siempre ha sido así, y el acto anterior de esta familia (`LOTE-RETRIAGE`) encontró la suya falsa.

---

## 4 · Las cuatro fichas — dos commits cada una, `PARO` por ficha y no por lote

| ficha | COMMIT A | COMMIT B | desenlace | ¿archiva? |
|---|---|---|---|---|
| **`R7.1`** | spec congelada | Δ pareado **6.5330 pp**, `IC95% [0.7331, 12.3329]`, n=40,162 | **rama 1 → propuesta `A`** | **no** — mesa adjudica (`FP-103`) |
| **`R7.3`** | spec congelada | ningún instrumento reúne las 4 piezas del RDD | **rama 1+2 → propuesta `C`** | **no** — clase de `C` a firma (`FP-104`) |
| **`R8.1`** | spec congelada | `Q3` con cobertura **cero** en 4 instrumentos | **rama 4 → `D`** | **sí** — `ADR-55`/`ADR-56` |
| **`R10.1`** | spec congelada | 3/6 vs 3/6, Δ **0.00 pp**, `IC95% [−56.58, +56.58]` | **rama 4 → no adjudica** | **no** — sin fila |

Y un **tercer commit** en `R10.1`, el primero que este programa ejerce: la spec estaba mal en dos puntos nombrables y se dice sin corregirla hacia atrás (`forense/hitoD-R10_1-defecto-spec-v1_0.md`).

**Ninguna ficha paró.** Las cuatro corrieron completas. Lo que se declara por ficha, y no por lote, es el desenlace: dos propuestas, un archivo, y una que no adjudica.

---

## 5 · El contador

> ## **Hito D archivadas: 13 → 14 de 27**

**Los dos extremos derivados con la receta de §1, ninguno tecleado.** Es el primer contador de medición que se mueve desde el **5/ago/2026** — quince días.

**Lo mueve `R8.1` → `D`, y solo `R8.1`.** `R7.1` (propuesta `A`) y `R7.3` (propuesta `C`) **no** lo mueven, por la doctrina que `ADR-55` fijó verbatim: *"se propone, mesa adjudica"*. `R10.1` no lo mueve porque no propone fila.

**Si mesa firma `FP-103` y `FP-104`, el contador llega a `16 de 27` sin una corrida nueva** — las dos corridas ya están hechas y archivadas.

**Cascada, ocho sitios marcados más un complementario:** `README.md:36` (y su desglose `7D`→`8D`) · `estado:95`, `estado:275` · `gobernanza:360`, `gobernanza:2796` · `modelo:65`, `modelo:700`, `modelo:885` · `estado:201` (`49−14=35`, `27−14=13`).

---

## 6 · Desviaciones de perímetro, declaradas y no descubiertas después

El perímetro del encargo era: *"forense/hitoD-R7_1|R7_3|R8_1|R10_1-\*.md · forense/hitoD-preregistro-v2_0.md (solo el registro de veredictos) · salidas · gobernanza · tablero · estado-programa (cascada) · hallazgos · nota · encargo"*. **Se salió de él tres veces, las tres mecánicas y las tres por exigencia de un test:**

1. **`tests/check.py`** — una entrada de censo en `_T25_ARCHIVOS_CONOCIDOS` para el encargo archivado verbatim, cuyo `E3` pelado (cita de `ACTO E3-TRIAGE`) dispara `T25`. El remedio es el que el propio mensaje del test nombra, y el precedente es del mismo día (`ACT-PIL-2`). **No cambia ninguna regla del test.**
2. **`README.md` y `canon/modelo-decision-v4_0.md`** — cinco líneas de contador marcadas `T20:HITO-D`. Dejarlas quietas habría metido `FAIL` nuevos en la suite. Se tocan **solo** las cifras; **ningún tier se retiqueta** (`ADR-60(b)`: el tier del motor y el veredicto de Hito D son ejes distintos, y `R8.1` sigue `[FUERTE]`).
3. **`tests/hitod_r7_1_concurrencia.py`, `tests/hitod_r7_3_rdd_constructibilidad.py`, `tests/hitod_r8_1_contribucion.py`, `tests/hitod_r10_1_rechazo_poder.py`** — los cuatro scripts de corrida. Van en `tests/` por la convención que `tests/ficha_r51_d3.py`, `tests/r5_1_pension_bienestar.py` y `tests/calg3_fasec.py` ya establecieron: **una cifra derivada por comando exige que el comando exista y sea corrible por otro.**

**Microdato: solo lectura**, sin excepción. `data/raw` es enlace al corpus compartido y no se escribió nada ahí. Los archivos internos que hubo que extraer (`all_states_final.zip`) se extrajeron al *scratchpad*, no al corpus.

---

## 7 · Lo que este acto NO hizo, dicho para que no se busque

- **No adjudicó nada.** `R7.1` y `R7.3` quedan como propuestas.
- **No tocó `R3.4`.** El encargo la excluyó y la asignó a `EMISOR-M`.
- **No tocó las nueve pre-registradas como probable `D`.**
- **No corrió ningún diseño sustituto.** La prohibición se escribió en `hitoD-R7.3-especificacion §5.3` **antes** de saber si el original corría, y se respetó: no hay RDD por edad sobre ayuda genérica, no hay correlación ecológica padrón×voto, no hay dif-en-dif entre entidades, no hay tasa de pago de agua de LAPOP 2021.
- **No recodificó las 12 transcripciones de `R10.1`** tras encontrar que la regla léxica fallaba. La razón está en `hitoD-R10.1-defecto-spec §3` y es la frase más importante del acto: un codificador único que ya vio el resultado equivocado y sabe qué número le conviene no produce una corrección, produce un sesgo con etiqueta de corrección.
- **No numeró `D-07` ni `D-08`.** Se proponen (`FP-105`, `FP-106`).
- **No tocó `milpa/`.** Falsar una regla no es calibrar un coeficiente (`ADR-47`).

---

## 8 · Suite

**19 FAIL · 142 WARN** al arrancar y **19 FAIL · 142 WARN** al cerrar — la suite no se movió ni un punto en todo el acto, verificado por `diff` de la lista de tests entre las dos corridas. Los dos `FAIL` que este acto llegó a introducir se atraparon y se cerraron dentro del acto: el `T25` del encargo verbatim (§6.1) y un `T20` autoinfligido al escribir el marcador literal dentro de la prosa del ADR — registrado en `hallazgos`, porque **un marcador de test no distingue uso de mención**, que es la misma familia del defecto que `ADR-40` resolvió para los veredictos.

---

## 9 · Sucesores nombrados, para que no haya que re-derivarlos

1. **Adjudicación de `FP-103` y `FP-104`** — dos filas de contador ya medidas, esperando firma. Es la vía más barata que existe hoy al `16 de 27`.
2. **`hitoD-R10.1-especificacion-v2_0`** — codificación pragmática, segundo codificador con acuerdo reportado, arista rama-4 → `C`, y techo de `n` declarado en la primera página. **Con 6 por brazo ninguna codificación resuelve 15 pp**, y una v2.0 que no lo diga repetirá este acto con mejor coloración.
3. **Adquirir PRESEEA** (`NO-ACCESIBLE` desde el 5/ago, ausente del corpus, verificado) — es lo único que subiría el `n` de `R10.1`.
4. **Dos ítems, no un instrumento**, para `R8.1`: repetir el módulo de agua de LAPOP 2021 en una segunda ola y añadirle un ítem de corte de servicio. **Lo que NO desbloquea `R8.1` es más inventarios de comités** — el brazo de control no puede estar en ningún inventario, por construcción.
5. **`R7.3` tiene ventana con fecha de caducidad**: su discontinuidad natural vivió en 2019-2021 y la universalización de 2022 la borró. Si alguien va a intentarlo, es contra datos de esos años.
