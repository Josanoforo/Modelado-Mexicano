# ACTO CEP · cotejo estimación → payload — COMMIT 1: especificación congelada

**Base:** `fd788a9` (`origin/main`, confirmado por `git fetch origin main` + `git rev-parse origin/main` en este acto — sin desplazamiento; `gu/gdelt-ucdp-recon` sigue sin fusionar). **Manifiesto:** 567 entradas, 563 con `sha256` (`yaml.safe_load` + conteo, este acto) — coincide exacto con lo que el encargo anticipaba para esta base, sin re-derivación. **Censo:** 550 filas (551 líneas con cabecera). **Entorno:** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`; repo-only, sin sonda de red más allá del `fetch` de confirmación de SHA.

Este archivo es COMMIT 1: declara universo, mecanismo y vocabulario **antes de correr el cotejo sobre las 550 filas**. COMMIT 2 (columna nueva en el censo + entrada en `registro-recalculo` + línea en `hallazgos.md`) no edita este archivo — si algo de lo declarado aquí resulta equivocado, se dice en un tercer commit, nunca hacia atrás.

---

## 1 · Universo — ni una fuente más

- **11 filas** de `data/curacion-registro/produccion-modelo.tsv` (columna `hash_microdato`).
- **11 scripts** de `tests/` — el encargo los cuenta como "~10"; enumerados uno a uno son 11, confirmado con `ls` sobre cada ruta antes de escribir esta nota:
  `calg3_fasec.py`, `idg3_corrida.py`, `calx_g3.py`, `hitoD_r7_2_ocho_olas.py`, `r5_1_pension_bienestar.py`, `p3_lca_data.py`, `c06b_conf06_encuci.py`, `w1_p_policial.py`, `cal_conf_faseb_ola2.py`, `cal_conf_faseb_pos4.py`, `cal_conf_faseb_pos5_6.py`.
  Esto no es una fuente nueva frente al encargo — los 11 nombres ya estaban listados en su tabla del §0; "~10" era su propio conteo aproximado.
- **550 filas** de `data/censo-explotacion-2026-08-13.tsv`.

No se abre `data/raw` (ausente, no hace falta), no se toca `relaciones.tsv`, no se añade ningún script ni fila fuera de esta lista.

---

## 2 · Mecanismo de empate — dos vías, nunca colapsadas

### Vía hash (`hash_microdato` ↔ `sha256`)

Exacta. Ya probada 11/11 contra `fd788a9` (comando del §0 del encargo, repetido en este acto sin cambios en el resultado): resuelve a `enbiare2021_bd_csv_zip` (10 filas) y `enasic2022_bd_csv_zip` (1 fila). Cero `NO_DETERMINADO`.

### Vía ruta (literal del script ↔ campo `archivo` del censo/manifiesto)

Inexacta por construcción — un directorio no es un payload. **Refinamiento sobre la tabla del §0 del encargo**, hecho leyendo el código completo de los 11 scripts (no solo el `grep` superficial que produjo esa tabla): ninguno de los 11 resultó ser una cita de directorio genuinamente ambigua. Los cinco que el encargo marcó "resuelven por raíz, sin literal — hay que leerlos" **sí tienen literales** una vez que se sigue la variable raíz hasta su uso; y los dos que el encargo presentó como citando el directorio `data/raw/ennvih/` (`calg3_fasec.py`, `idg3_corrida.py`) también resuelven, siguiendo el código, a nombres de archivo exactos. Verificado además, sobre los 10 scripts que sí abren algo: `grep -n "listdir\|glob(|os\.walk|scandir|iterdir"` → **0 resultados** en los 10 — ninguno enumera un directorio en tiempo de ejecución. Esto es un hallazgo de este COMMIT 1, no una decisión de conveniencia: la categoría `CONSUMIDO-AMBIGUO` se declara igual en el vocabulario (§3) porque el mecanismo la permite, pero se anota aquí, antes de correr, que este universo concreto puede no producir ninguna fila en ella.

**Tabla de citas literales, verificada línea por línea (`RAW`/`RAIZ`/`DATOS` es la constante de raíz del script; la ruta resuelta es relativa a `data/raw/`):**

| script | ruta(s) resuelta(s) (relativa a `data/raw/`) | evidencia (archivo:línea) |
|---|---|---|
| `calg3_fasec.py` | `ennvih/ehh05dta_all.zip`, `ennvih/ehh05lw_all.zip`, `ennvih/ehh09dta_all.zip`, `ennvih/ehh09lw_all.zip` | `DATOS` en L31; diccionario `FICHAS` L151-159 (`datos=`/`peso=` por ola); `abrir(F['datos']/F['peso'], …)` en L362-373 |
| `idg3_corrida.py` | `ennvih/ehh05dta_all.zip`, `ennvih/ehh09dta_all.zip` | `RAIZ` L37; `leer('ehh05dta_all.zip', …)`/`leer('ehh09dta_all.zip', …)` en L84-85, L113-114, L127-128 |
| `calx_g3.py` | **ninguna — ver nota debajo** | docstring L27-33, comentario L59-62; `grep -n "open(\|Path(\|sys.argv\|input(\|read("` sobre el archivo completo (420 líneas) → 0 |
| `hitoD_r7_2_ocho_olas.py` | `envipe2018_csv.zip` … `envipe2025_csv.zip` (8 archivos, `YEARS=range(2018,2026)`) | L30, L45 (`zpath = f"data/raw/envipe{year}_csv.zip"`), bucles `for y in YEARS` en L169 y L192 (confirma que se leen las 8, no solo 2025) |
| `r5_1_pension_bienestar.py` | `enigh2012_nc_csv.zip`, `enigh2014_nc_csv.zip`, `enigh2016_nc_csv.zip`, `enigh2018_nc_csv.zip`, `enigh2020_nc_csv.zip`, `enigh2022_nc_csv.zip` (**6 archivos — el encargo listaba 4, faltaban 2020 y 2022**) | `RAW` L54; diccionario `WAVES` L56-116 (6 claves); `zpath = RAW / cfg["zip_name"]` L132; `__main__` L372: `years = [...] or sorted(WAVES)` — sin argumentos de CLI corre las 6 |
| `p3_lca_data.py` | `enigh2022_nc_csv.zip` | `RAW` L42, `ENIGH_ZIP` L43, `zpath` L60 |
| `c06b_conf06_encuci.py` | `BD_ENCUCI2020_dbf.zip` | `RAW` L26, apertura L78 |
| `w1_p_policial.py` | `BD_ENCUCI2020_dbf.zip` | `RAW` L21, apertura L118 |
| `cal_conf_faseb_ola2.py` | `envipe2025_csv.zip`, `BD_ENCUCI2020_dbf.zip` | `RAW` L19, aperturas L90 y L184 |
| `cal_conf_faseb_pos4.py` | `envipe2025_csv.zip` | `RAW` L18, aperturas L69 y L114 (mismo archivo, dos lecturas) |
| `cal_conf_faseb_pos5_6.py` | `BD_ENCUCI2020_dbf.zip`, `enif2024_csv.zip` | `RAW` L25, aperturas L91 y L228 |

**Nota sobre `calx_g3.py` — caso propio, no colapsado con los otros diez.** Su docstring (L16-18) declara: *"SOLO codebook. Ningún .dta se abre aquí... Las constantes de abajo están transcritas a mano desde los PDF"*. Cita en comentario (L60-62) tres PDF por nombre — `ehh02cb_b2.pdf`, `ehh05cb_b2.pdf`, `ehh09cb_b2.pdf` — pero (a) el script no abre ningún archivo en tiempo de ejecución (verificado arriba, 0 llamadas), y (b) esos tres nombres **no son literal de ningún campo `archivo` del manifiesto** — lo que existe es `ennvih/ehh02cb_all.zip`/`ehh05cb_all.zip`/`ehh09cb_all.zip` (ids `ennvih{1,2,3}_*_hogar_cb`), un ZIP que empaqueta los manuales de **todos** los libros, no el PDF individual del Libro II que el script nombra. Bajo el mecanismo declarado (empate literal exacto, sin resolución semántica — eso es precisamente lo que la reserva de "prohibido elegir uno" de §COMMIT-1 del encargo prohíbe hacer al revés también, es decir, prohíbe que yo "ayude" a resolver `ehh02cb_b2.pdf` hacia `ennvih/ehh02cb_all.zip` por inferencia), `calx_g3.py` no produce ningún empate por vía ruta. Se declara aquí, antes de correr, para que el resultado (si da `SIN-CONSUMO-DETECTADO` para esas filas o si esas filas ni siquiera existen como entradas propias del manifiesto) no se lea como un fallo del mecanismo.

**Empates múltiples contra el mismo payload:** cuando dos o más scripts citan la misma ruta (p. ej. `BD_ENCUCI2020_dbf.zip` × 4 scripts, `envipe2025_csv.zip` × 3, `ennvih/ehh05dta_all.zip` × 2), `consumo_universo_declarado` nombra **todos** los scripts citantes, no solo el primero.

**Precedencia si un payload empatara por ambas vías** (no ocurre en este universo — las dos filas de la vía hash, `enbiare2021_bd_csv_zip` y `enasic2022_bd_csv_zip`, no coinciden con ninguna de las 20 rutas resueltas de la vía ruta, verificado): gana `CONSUMIDO-POR-PRODUCCIÓN`, y `consumo_universo_declarado` declara igual el empate por ruta que quedó subordinado.

**Nota de precisión sobre "veredicto sellado"** (vocabulario, §3): la definición de `CONSUMIDO-POR-CORRIDA` del encargo dice "script que produjo un veredicto sellado". Ese universo de 11 scripts lo fijó el propio encargo, no este COMMIT 1 — pero al menos uno de ellos, `calg3_fasec.py`, declara en su propio docstring (L7-10) que su entregable es "DESCRIPTIVO: sin veredicto de falsación, sin celda CAL, sin entrada al conteo de corridas". La etiqueta `CONSUMIDO-POR-CORRIDA` se aplica igual a sus empates, porque el mecanismo que este acto puede verificar es "el script abre el payload en tiempo de ejecución" — no "el resultado del script quedó adjudicado como veredicto sellado de Hito D", que es territorio de Dominio 6 y de este acto no re-deriva ni adjudica. Se deja escrito para que la etiqueta no se lea más fuerte de lo que el mecanismo mide.

---

## 3 · Vocabulario cerrado — propuesto, mesa puede cambiarlo, fijado antes de correr

| rótulo | condición |
|---|---|
| `CONSUMIDO-POR-PRODUCCIÓN` | empata por hash contra `produccion-modelo.tsv` |
| `CONSUMIDO-POR-CORRIDA` | empata por ruta (archivo, no hash) contra al menos uno de los 11 scripts del universo declarado — ver nota de precisión arriba |
| `CONSUMIDO-AMBIGUO` | el script cita un directorio, no un archivo — N payloads candidatos, todos nombrados, ninguno elegido a dedo. Declarado en el vocabulario aunque §2 ya anota que este universo concreto podría no poblarla |
| `SIN-CONSUMO-DETECTADO` | no empata por ninguna de las dos vías. No es "nadie lo necesita" (A.4: es `NO-ENCONTRADO`, no "no existe"); se dice con qué mecanismo se buscó (ambas vías, siempre) |

**Columnas nuevas, nombre fijado aquí para no renombrar en COMMIT 2:** `consumo_detectado` (el rótulo de arriba) y `consumo_universo_declarado` (universo + mecanismo + fecha en la misma línea, A.4 — deliberadamente **no** llamada `universo_declarado` a secas: esa cabecera ya existe en el censo, columna 9, y describe el universo de `estado`, no el de esta columna nueva; reusar el nombre colisionaría).

---

## 4 · Reserva de escala (A-bis regla 3)

Este acto **no produce ninguna cantidad estimada**. Es una tabla de correspondencia entre lo que ya existe en tres tablas (censo, manifiesto, producción) y lo que once scripts citan en su propio código. Ningún contador de medición sobre México se mueve por este COMMIT 1 ni por el COMMIT 2 que le sigue — lo único que se mueve es si un payload tiene o no consumo trazable, que es un hecho sobre el programa, no sobre México.

---

## 5 · Frase de cierre

**El primer resultado que produzca este procedimiento es el que se reporta.**

---

## Nota fuera de perímetro — índice de infraestructura

`data/INFRAESTRUCTURA-v1_0.md` (Dominio 4, Dominio 6) leído antes de escribir esta nota. Dominio 4 confirma que `produccion-modelo.tsv` (vía `integrate_production.py`) es la tabla correcta para la vía hash — consistente con lo ya usado en el §0 del encargo. Dominio 6 confirma que los veredictos del Hito D solo se adjudican vía el bloque append-only de `hitoD-preregistro-v2_0.md`, no vía ningún script de `tests/` por sí solo — consistente con la nota de precisión de §2 arriba, y con que este acto no toca esa adjudicación.

**Hueco menor, no bloqueante:** ni `forense/registro-recalculo-v1_0.md` ni `data/censo-explotacion-2026-08-13.tsv` tienen fila propia en el índice de Dominio 8 (que sí cubre `hallazgos.md` y `forense/notas/`) — ambos artefactos son del 13/ago, y el índice se construyó el mismo día contra una base anterior (`2b13e88`). No detiene este acto porque el encargo que lo abre ya nombra explícitamente los cuatro archivos de escritura (perímetro, cabecera del encargo) — este acto no necesita derivar esa vía del índice, ya le fue dada. Se anota para quien actualice `INFRAESTRUCTURA-v1_0.md`.
