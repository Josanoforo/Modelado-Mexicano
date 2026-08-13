# ACTO ADJ-4 · cuatro firmas de mesa en un solo acto — nota de cierre

**Naturaleza.** Acto de sellado. Mesa dicta las cuatro firmas en el propio texto de lanzamiento del acto (archivado verbatim en `forense/encargos/2026-08-13-adj4-firmas-mesa.md`, A.3). El ejecutor propaga y deriva — no decide, no reescribe texto sellado, no amplía el alcance. Entorno: NUBE, repo-only, sin red, sin microdato.

---

## 0 · ARRANQUE — premisas del encargo, corridas antes de tocar nada

```
$ grep -c "EJERCIDA_" forense/registro-llaves-identificacion-v1_0.md
8
$ grep -oE '\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -nu | tail -1
72
$ python3 tests/check.py --baseline 2>&1 | tail -4
18 FAIL · 105 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 948ad70343320b62f000d31fd39e2b2b68336ad9)
```

**Premisa 1, interpretada correctamente antes de leerla como bloqueo.** El `8` crudo no es una llave ya ejercida — es exactamente el modo de falla que el propio `registro-llaves-identificacion-v1_0.md` §4 declara para el `grep -c 'EJERCIDA_'` ingenuo: cuenta también las cuatro filas del vocabulario de `estado` (§2: `EJERCIDA_CORROBORA`/`EJERCIDA_ACOTA`/`EJERCIDA_REFUTA`/`EJERCIDA_INDECISA`) y la prosa que las menciona, no solo la columna `estado` de la tabla de llaves (§3). La receta corregida de ese mismo §4 (acotada a `## 3 · Tabla de llaves`, columna 6) da `0` contra el archivo tal como estaba — verificado antes de firmar nada, ver §1 abajo. No había fila `EJERCIDA_*` sellada de antemano: **no PARA**.

**Premisa 2.** `72` — máximo ADR en `gobernanza-v1_15.md` antes de este acto. Confirma que el próximo ADR, si la receta de alguna de las cuatro firmas lo pide, es `ADR-73` contra esta base (`19d885d`) — colisionó con `PR #203` (ALIAS-P), que derivó el mismo número contra la misma base y fusionó primero; renumerado a `ADR-74` al fusionar `origin/main`, ver §5.

**Premisa 3.** `18 FAIL · 105 WARN`, LÍNEA BASE VERDE contra `tests/baseline.json` (HEAD congelado `948ad70`, el propio Commit 3 de ENLACE-1). Punto de partida verificado antes de revertir nada en §4.

SHA de arranque: `19d885d` (HEAD de la rama antes de este acto, merge PR #200).

---

## 1 · Firma (a) — `R5.1-D2` → `EJERCIDA_INDECISA`, fila B

**Firma, verbatim:** *"Adjudico fila B, `EJERCIDA_INDECISA`."*

**La trampa, nombrada por el propio encargo, verificada aquí.** El transfer del 12-13/ago que dispatchó este acto titula la fila con el veredicto de `forense/notas/2026-08-12-e4c-r5-1-d2-commit8-resultado.md` — literalmente titulado *"Commit 8: resultado — veredicto PROPUESTO: fila A (refutación)"* — pero ese veredicto quedó retirado **dentro del propio E4c**, antes de que el transfer se escribiera:

- Commit 9 (`forense/notas/2026-08-12-e4c-r5-1-d2-commit9-monto-gasto.md:62`): *"Se retira la propuesta de fila A del Commit 8, sin editarlo — se propone B en su lugar."* Motivo: Commit 8 §4 usó un proxy de **ingreso** per cápita para "monto documentado como suficiente" — Commit 9 corrige con la medida sellada (`gasto_mon`, no ingreso) y la razón monto/gasto baja de 20.0%/29.1% a **29.0%** media ponderada, por debajo del criterio sellado (60-63%) y del piso de 33%.
- Commit 10 (`forense/notas/2026-08-12-e4c-r5-1-d2-commit10-incertidumbre-razon.md:56`, §4): calcula el IC95% de la razón (linealización de cociente + ultimate cluster) en dos variantes de varianza — (26.16%, 31.94%) dominio y (25.95%, 32.14%) extensión-cero, **enteras por debajo del 33%** — y confirma, verbatim: *"No cambia la fila propuesta (B, `EJERCIDA_INDECISA`) ni la precedencia citada en Commit 9 §7."*

Por la precedencia sellada `A → E → B → C → D` (ADR-71(b)), la cláusula de "monto insuficiente" de B gana sobre A y sobre E sin excepción por magnitud del DiD — ambos desenlaces de `R5.1-D2` sí cumplen `DiD<10pp`-o-signo-contrario (Commit 8 §2: transferencia +2.32pp, corresidencia −0.81pp), pero eso solo satisface una de las tres condiciones conjuntivas de la fila A; la segunda (monto suficiente) falla.

**Esta firma sigue al repo, no al titular del transfer** — instrucción explícita del encargo, verificada aquí línea por línea antes de firmar.

**El contador se mueve por la receta propia del archivo, no por decreto de este encargo.** Corrida contra `forense/registro-llaves-identificacion-v1_0.md` tal como queda escrito tras la firma:

```
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -E '^\| `' | awk -F'|' '{print $6}' | grep -c 'EJERCIDA_'
1
$ sed -n '/^## 3 · Tabla de llaves/,/^## /p' forense/registro-llaves-identificacion-v1_0.md \
    | grep -cE '^\| `'
2
```

`1 de 2` — coincide exacto con lo que el encargo esperaba (`0 de 2 → 1 de 2`). Detalle completo, con la firma y la cita línea por línea, en `forense/registro-llaves-identificacion-v1_0.md` §5 (nueva).

---

## 2 · Firma (b) — rótulo de cota adoptado, `ADR-74(a)` (redactado como `ADR-73`, renumerado — §5)

**Firma, verbatim:** *"Adopto el rótulo de MAP-A §7 verbatim."*

`ADR-67` (`gobernanza:862`) dejó dos cifras sin cerrar en la misma oración: un tablero placeholder (`COTA_SUPERIOR_NO_RECONCILIADA`) y "958 programas hoy conocidos (0.52%)" sin receta citada. `forense/notas/2026-08-12-map-a-cota-universo.md` §7 reconstruyó el mecanismo de los tres denominadores (D1=35,708 activos T0 / 958 nombres de programa crudos, D2=825 fichas del catálogo RNM vía export CSV — verificado dos veces bit-idéntico y cruzado independientemente contra la paginación HTML, `page=55`×15=825 exacto —, D3=197 relaciones/75 fuentes) y propuso, sin sellar (*"mesa decide en acto propio"*), el rótulo verbatim que este acto adopta íntegro en `ADR-74(a)`.

**Corrección de lectura, misma fuente (MAP-A §5/§7).** El `958` sí tiene receta mecánica real (`awk -F'\t' 'NR>1{print $2}' data/curacion-universo/universo-declarado-t0.tsv | sort -u | wc -l` = 958, verificado) — pero cuenta cadenas de `fuente_programa` **sin deduplicar** (10 variantes nombran solo "Censo de Población y Vivienda"). La lectura correcta de "5 instrumentos de 958 programas (0.52%)" es **"5 de 958 nombres de programa no deduplicados"** — la fracción real es más alta, no cuantificada (exigiría deduplicar `fuente_programa`, acto propio, no ejecutado).

**Propagación, sin reescribir texto sellado.** Por el mismo principio que `ADR-67` sentó ("VENCIDO EN ALCANCE — no refutado, no borrado, no vigente para el territorio nuevo"), `gobernanza:862` no se reescribe: gana dos anotaciones entre paréntesis, apuntando a `ADR-74(a)`, donde vive el rótulo completo y la estampa de universo (mecanismo = endpoint de exportación CSV del catálogo RNM/INEGI, fecha = 12/ago/2026, `data/universo-cota-2026-08-12.tsv`). Texto completo del ADR en `canon/gobernanza-v1_15.md`, entre `ADR-73` (ALIAS-P) y `## 5. Deuda declarada`.

---

## 3 · Firma (c) — registro-recalculo, entradas 0 y 1

### 3.1 · Entrada 1 (Censo v1.1) — `RECALCULADO — CAMBIA`, copiada verbatim

El texto de cierre ya estaba propuesto, verbatim, en `forense/notas/2026-08-13-censo-v1_1-abrir4-enasem.md` §12 ("Propuesta de cierre — Entrada 1..."). Se copió sin reescribir a la columna `estado` de la fila 1 de `forense/registro-recalculo-v1_0.md` §1, con la nota (no dentro del texto copiado, aparte, para no violar "cópialo, no lo reescribas") de que el `0 de 2` que esa propuesta cita para `llaves de identificación ejercidas` seguía exacto cuando se escribió — la firma (a) de este mismo acto lo mueve a `1 de 2` por una razón enteramente distinta y concurrente, no por relación causal con el censo.

**Por qué necesita ADR propio — no es discrecional.** `ADR-72`, sección "Criterio de salida" (texto sellado): *"`RECALCULADO — CAMBIA` (se propaga con su ADR)."* La regla vive también, idéntica, en la cabecera de `registro-recalculo-v1_0.md` §1. `ADR-74(b)` es ese vehículo — ratifica el movimiento concreto de las tres filas (12/13/14, `SIN-RUTA`→`RUTA-C`) sin declarar canon la taxonomía de rutas en general (que sigue sin sellarse, per `censo-estimabilidad-coeficientes-v1_1.md` §1, verbatim).

### 3.2 · Entrada 0 (cotejo censo↔relaciones.tsv) — `RECALCULADO — SIN CAMBIO`, cotejo nuevo de las 12 filas restantes

**La trampa que el propio censo v1.1 dejó nombrada, respetada.** `censo-v1_1` §12 declaró explícitamente que **no** proponía cierre para la Entrada 0 porque su alcance (las 15 filas del censo) es más ancho que el suyo (solo las 9 `SIN-RUTA` de v1.0). Cerrarla sin más habría sido, textualmente, "una conclusión más ancha que su universo" — el defecto que `ADR-72` existe para prohibir. Este acto hace el trabajo que faltaba: el cotejo de las 12 filas restantes (todas menos 12/13/14, ya resueltas por la Entrada 1).

**Mecanismo — `necesidad_id`, decidible por lectura para las 15 filas, sin ambigüedad.** `data/curacion-registro/necesidad-objeto-modelo.tsv` mapea las 15 filas del censo de coeficientes 1:1 contra `N1`-`N15`, en el mismo orden:

| censo | `objeto_modelo_origen` | `necesidad_id` |
|---|---|---|
| 1 · G1 `confianza_institucional` | `G1.confianza_institucional` | `N1` |
| 2 · G1 `radio_confianza` | `G1.radio_confianza` | `N2` |
| 3 · G2 `sens_estatus` | `G2.sens_estatus` | `N3` |
| 4 · G2 `aversion_riesgo` | `G2.aversion_riesgo` | `N4` |
| 5 · G3 `horizonte_temporal` | `G3.horizonte_temporal` | `N5` |
| 6 · G3 `aversion_riesgo` | `G3.aversion_riesgo` | `N6` |
| 7 · G3 `familismo_apoyo` | `G3.familismo_apoyo` | `N7` |
| 8 · G4 `exposicion_violencia` | `G4.exposicion_violencia` | `N8` |
| 9 · G4 `confianza_institucional[justicia]` | `G4.confianza_institucional` | `N9` |
| 10 · G4 `horizonte_temporal` | `G4.horizonte_temporal` | `N10` |
| 11 · G4 `sens_estatus` | `G4.sens_estatus` | `N11` |
| 12 · G5 `familismo_apoyo` | `G5.familismo_apoyo` | `N12` (ya resuelta, Entrada 1) |
| 13 · G5 `familismo_obligacion` | `G5.familismo_obligacion` | `N13` (ya resuelta, Entrada 1) |
| 14 · G5 `radio_confianza` | `G5.radio_confianza` | `N14` (ya resuelta, Entrada 1) |
| 15 · G6 `deferencia` | `G6.deferencia` | `N15` |

Ninguna de las 15 filas resultó indecidible por lectura — el mapeo es directo, verbatim, sin necesitar juicio semántico (a diferencia del cruce que `censo-v1_1` §6 tuvo que hacer a mano para N12/N13/N14 antes de que este TSV se usara para esto).

**Cotejo de las 12 restantes (`N1`-`N11`, `N15`) contra `capa4_apertura_mapeo`/`clasificacion_relacion` de `data/curacion-registro/relaciones.tsv`, salida cruda:**

```python
import csv
from collections import defaultdict, Counter
rows = defaultdict(list)
with open("data/curacion-registro/relaciones.tsv", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        rows[row["necesidad_id"]].append(row)
```

| `necesidad_id` | filas en `relaciones.tsv` | `capa4_apertura_mapeo` observados |
|---|---|---|
| `N1` | 1 | `SIN_APERTURA_EXPLICITA`×1 |
| `N2` | 4 | `(vacío)`×3 · `INDEXADO-NO-DESCARGADO`×1 |
| `N3` | 12 | `(vacío)`×1 · `INDEXADO-NO-DESCARGADO`×2 · `NO-ENCONTRADO`×4 · `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO`×1 · `SATISFACE-UMBRAL-DOCUMENTAL`×2 · `SIN_APERTURA_EXPLICITA`×2 |
| `N4` | 9 | `(vacío)`×1 · `EXISTE-NO-SATISFACE`×2 · `NO-ENCONTRADO`×2 · `SIN_APERTURA_EXPLICITA`×4 |
| `N5` | 8 | `(vacío)`×2 · `INDEXADO-NO-DESCARGADO`×1 · `SIN_APERTURA_EXPLICITA`×5 |
| `N6` | 6 | `(vacío)`×1 · `SIN_APERTURA_EXPLICITA`×5 |
| `N7` | 1 | `SIN_APERTURA_EXPLICITA`×1 |
| `N8` | 3 | `SIN_APERTURA_EXPLICITA`×3 |
| `N9` | 1 | `SIN_APERTURA_EXPLICITA`×1 |
| `N10` | 8 | `EXISTE-NO-SATISFACE`×3 · `NO-ENCONTRADO`×1 · `SIN_APERTURA_EXPLICITA`×4 |
| `N11` | 2 | `SIN_APERTURA_EXPLICITA`×2 |
| `N15` | 7 | `(vacío)`×2 · `MAPEADO-NO-SATISFACE`×1 · `SIN_APERTURA_EXPLICITA`×4 |
| **TOTAL** | **62** | ningún `EXISTE-SATISFACE` en ninguna fila |

**Resultado: ninguna de las 12 necesidades trae, en ninguna de sus 62 filas, la combinación `capa4_apertura_mapeo=EXISTE-SATISFACE` + `clasificacion_relacion=CONFIRMADA`** — la firma que marcó las tres filas de G5 (N12/N13/N14) como desacuerdo real. Los valores presentes son todos de candidatura sin resolver (`SIN_APERTURA_EXPLICITA`, `INDEXADO-NO-DESCARGADO`) o negativos (`NO-ENCONTRADO`, `EXISTE-NO-SATISFACE`, `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO`, `MAPEADO-NO-SATISFACE`) — ninguno contradice la clasificación vigente del censo (`RUTA-A`/`RUTA-I`/`RUTA-C`/`SIN-RUTA` según corresponda a cada fila).

**Cierre: `RECALCULADO — SIN CAMBIO`.** Con las 15 filas ahora cotejadas (antes: 3 de 15, cotejo parcial que la propia enmienda de `ADR-72` declaró explícitamente) y sin desacuerdo nuevo, la Entrada 0 se sostiene — el censo, en el estado a que lo deja la Entrada 1 de este mismo acto (`censo-v1_1`, con 12/13/14 ya en `RUTA-C`), no está en desacuerdo con `relaciones.tsv` en ninguna de sus 15 filas. `SIN CAMBIO` no exige ADR propio (`ADR-72`, "Criterio de salida": solo `CAMBIA` lo exige).

---

## 4 · Firma (d) — baseline revertido a `e7cd99d`, defecto de ENLACE-1 arreglado

**Firma, verbatim:** *"Se revierte el recongelado de ENLACE-1 commit 4."*

**Verificación previa a revertir.** `git show e7cd99d:tests/baseline.json` vs. el vigente: la única diferencia real es el `head` (`2cb39c9`→`948ad70`, el recongelado en sí), tres entradas `T16` (consecuencia aritmética de una `T03` nueva) y una entrada `T03` nueva: *"`forense/encargos/2026-08-13-enlace1-mapeo-id-manifiesto.md` cita PLANENLACECAPA220260813.md, que no existe."* Nada más cambió entre `e7cd99d` y el recongelado de Commit 4 (`8c10225`) — confirma que revertir no pierde ningún hallazgo legítimo de los 19 commits fusionados desde entonces (todos mantuvieron `--baseline` VERDE en su propio momento).

**El defecto, real y propio de ENLACE-1, no heredado.** El Commit 3 de ese mismo acto (`948ad70`, *"quita backticks de citas gitignoradas/no-repo (T03)"*) corrigió dos ubicaciones (`forense/hallazgos.md`, la nota `2026-08-13-enlace1-commit1-reglas-mapeo.md` §8) pero no tocó el propio archivo de encargo (`forense/encargos/2026-08-13-enlace1-mapeo-id-manifiesto.md:7`), que cita entre backticks el mismo documento externo (PLANENLACECAPA220260813.md, subido por el usuario para lanzar el encargo, nunca un archivo del repo). Commit 4 (`8c10225`) no lo arregló — lo congeló en `tests/baseline.json` como si fuera deuda aceptada.

**Arreglo.** Se quitaron los backticks de la cita en `forense/encargos/2026-08-13-enlace1-mapeo-id-manifiesto.md:7` (queda como texto plano, sin colgar) — mismo mecanismo que el Commit 3 ya usó para las otras dos ubicaciones. No se tocó ninguna otra parte del archivo (perímetro: "solo la cita colgante").

**Consecuencia aritmética, propagada en el mismo commit conceptual (COMMIT 2 de este acto).** El WARN real bajó de 105 a 104 (un `T03` menos). `canon/gobernanza-v1_15.md:760,852` y `canon/estado-programa-v1_10.md:130,222` declaraban `105 WARN`/`18 FAIL · 105 WARN` como vigente (no historia fechada bajo el formato que `T16` exime) — las cuatro se actualizaron a `104`, con nota de la baja. Sin esto, `T16` habría quedado en rojo por una discrepancia que el propio arreglo de T03 provoca mecánicamente, no por un defecto nuevo.

**Verificación final.**

```
$ python3 tests/check.py --baseline 2>&1 | tail -4
18 FAIL · 104 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 2cb39c9ceff4abe76d895a9739242c2e5d056516)
(3 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

VERDE contra `e7cd99d`, como el encargo exige al cierre.

---

## 5 · Propagación, colisión de numeración, y verificación de cierre (COMMIT 2 + merge)

**Colisión de numeración con `PR #203` (ALIAS-P + MOTOR-DIAG) — cuarta vez que pasa, resuelta con el mismo mecanismo que las tres anteriores.** COMMIT 1 y COMMIT 2 (abajo) se escribieron y sellaron localmente como `ADR-73`, derivado correctamente contra `origin/main = 19d885d` (72 únicos, contiguo — verificado con la receta de T15 antes del primer commit, misma disciplina que ya exigió ADR-71). Mientras tanto, `PR #203` (ENCARGO B · ALIAS-P + MOTOR-DIAG, sobre `tools/curador_registro/via_capa2.py`) selló su **propio** `ADR-73` contra la misma base, y fusionó primero a `origin/main`. Ambos números son correctos contra el terreno que cada uno tenía delante al sellar — ninguno de los dos erró; gana quien fusionó primero, exactamente el criterio que ya resolvió `ADR-69`/`PR #175` → `ADR-70`, y que forzó las dos renumeraciones de `ADR-71` en el propio ACTO M-6.

**Resolución.** `git fetch origin main` + `git merge origin/main` — dos conflictos reales, ambos por inserción en el mismo punto de dos ramas independientes: `canon/gobernanza-v1_15.md` (el cuerpo del ADR nuevo, entre `ADR-72` y `## 5. Deuda declarada`) y `canon/estado-programa-v1_10.md` (la misma línea de cascada de §L0, un único párrafo de texto continuo). Resuelto conservando **ambas** narrativas, en el orden en que fusionaron — el `ADR-73` de ALIAS-P íntegro y sin tocar, seguido del ADR de este acto renumerado a `ADR-74` (todas sus referencias internas `ADR-73(a)`/`ADR-73(b)` → `ADR-74(a)`/`ADR-74(b)`, y el límite "ADR-48 a ADR-72" de la cláusula de versión sube a "ADR-48 a ADR-73", porque ahora hay un ADR intermedio antes del suyo). Cabecera de `gobernanza` y tabla de `estado-programa` suben a `74 ADR`. Ninguna referencia de ALIAS-P a su propio `ADR-73` se tocó — no era de este acto tocarla.

**Estructura de commits.** COMMIT 1 (`267527c`) y COMMIT 2 (`4bd96ef`) escriben las cuatro firmas, sus derivaciones propias, y la propagación de contadores — como `ADR-73`, antes de la colisión. Un tercer commit (este mismo cambio) fusiona `origin/main` y renumera a `ADR-74`, sin dejar hueco. `llaves de identificación ejercidas 0→1` y la propagación de WARN `105→104` (`gobernanza-v1_15.md:760,852`, `estado-programa-v1_10.md:130,222`) no fueron tocadas por el merge — ALIAS-P no las tocó, auto-merge limpio.

**Contadores declarados que NO se mueven (verificados, no tecleados):**

```
$ grep -n "13 de 27 corridas archivadas" canon/estado-programa-v1_10.md   # Hito D, sin tocar
$ grep -n "modelo-decision-v4_0.md:277" forense/registro-llaves-identificacion-v1_0.md  # fuente del 9 de 14
$ grep -c "^| [0-9]\+ |" forense/censo-estimabilidad-coeficientes-v1_1.md  # 0 de 15: coeficientes en escala del motor, ninguno tocado
$ awk -F'\t' 'NR>1 && $10=="SI"' data/curacion-registro/relaciones.tsv | wc -l
43
```

`13 de 27` · `9 de 14` · `0 de 15` · `capa2 SI 43` — los cuatro confirmados sin movimiento por este acto.

**T15/T18/T20, vigilando la cascada — los tres limpios tras COMMIT 2**, verificado con la suite completa (§4 arriba). Ningún test truena; no hubo que maquillar nada.

---

## 6 · Lo que este acto NO hace

No corre ningún diseño nuevo ni recalcula ningún estimador de `R5.1-D2` — adjudica sobre lo que E4c ya produjo. No dedupica `fuente_programa` — declara el hallazgo, no lo ejecuta (del tamaño de un acto propio). No sella la taxonomía `RUTA-A`/`RUTA-I`/`RUTA-C`/`SIN-RUTA` del censo como canon en general. No abre microdato, no toca `milpa/`, no toca `data/` fuera de lectura. No reabre ningún cierre de búsqueda (ADR-52 A, ADR-54 íntegros). No toca `forense/hitoD-preregistro-v2_0.md` — el denominador 27 (ADR-67(c)) no se toca.

---

*Nota de cierre de ACTO ADJ-4, 13/ago/2026. Encargo archivado en `forense/encargos/2026-08-13-adj4-firmas-mesa.md` (A.3).*
