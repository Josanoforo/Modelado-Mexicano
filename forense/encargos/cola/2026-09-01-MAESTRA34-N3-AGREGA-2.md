ESTADO: CONSUMIDO — PR #503 (MAESTRA36-N2, sesión manual)
ENTORNO: NUBE
ENCOLADO: 2026-09-02 · gesto de encolado, precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026)
BITACORA:
- 2026-09-02 · LISTO-NUBE · encolado por PR [COLA] encola MAESTRA34-L1/N1/N2/L2/N3. COMPUERTA propia: MAESTRA34-L2 fusionado con R v1_2 completo (o parcial declarado) Y PR `[L] corridas v1_2` de mesa fusionado Y L-extraido-v1_2.tsv producido con la MISMA regla de extracción congelada de MAESTRA33-E21 (tools/extrae_l_v1_1.py sin editar; si hay que editarlo, PARO y a mesa). Si falta cualquiera, cero commits.
- 2026-09-03 · EN-CURSO · sesión de nube claude/despacha-MAESTRA34-N3-AGREGA-2
- 2026-09-03 · PARO-REPORTADO · ENMIENDA 4 (commit `59b88b1`/`3be4bad`, 3/sep 05:52–05:55 UTC) reafirma "P1 puntúa 13 de 14 aplicando exclusiones-v1_2.md (DIN-M-01) como exclusión con razón", pero `forense/prereg-duelo-v2/exclusiones-v1_2.md` ya trae un apéndice posterior (`ACTO MAESTRA35-L5`, commit `3b9191d`, 2/sep 17:20:59 -06:00 = 23:20:59 UTC — anterior a ENMIENDA 4 y ya en `origin/main`): "Exclusión LEVANTADA por firma de mesa d2 (2/sep/2026)... N3/N5 puntúan 14 de 14, con la reserva de (a)." Verificado: `corridas-R/DIN-M-01.json` existe (`estado: COMPUTADO`, `diseno: DISENO-APROXIMADO`, con `EE_R` y `EE_R_sin_diseno`) y su campo `puntua` dice literalmente "SI, por firma de mesa d1 (FP-249)... Esa mitad la ejecutan MAESTRA35-N3/N5, no ACTO MAESTRA35-L5" — exige que N3 calcule z con las dos EE y decida si el veredicto de la celda cambia entre ellas (si cambia: AMBIGUA-POR-DISEÑO, no cuenta como puntuada; si no cambia: cuenta). Comandos: `git log -1 --format='%ci %s' 3b9191d` → `2026-09-02 17:20:59 -0600 MAESTRA35-L5: propaga las firmas de mesa d1/d2 sobre FP-249`; `git merge-base --is-ancestor 3b9191d HEAD` → `yes`. No se puede determinar si dirección desconocía el levantamiento al redactar ENMIENDA 4, o lo ignoró deliberadamente: ejecutar "13 de 14" contradice el verbatim vigente de exclusiones-v1_2.md; ejecutar "14 de 14 con reserva" añade al procedimiento un cálculo que ninguna enmienda de N3 describe. Cero commits sustantivos; cero push de trabajo de P1-P3. Pide firma de mesa que resuelva cuál de las dos lecturas rige.
- 2026-09-03 · ENMIENDA 5 (mesa) resuelve el PARO: corrige ENMIENDA 1/línea 42 y ENMIENDA 4/línea 93 (VENCIDAS EN ALCANCE por `d2`), P1 puntúa 14 de 14. Implementa `d1` con `forense/prereg-duelo-v2/din_m_01_doble_ee.py` (nuevo, no toca `tools/score_marco_m.py`): `DIN-M-01` calculada con `EE_R` y `EE_R_sin_diseno`, mismo veredicto (FUERA-DE-BANDA) en ambas → cuenta como puntuada, no AMBIGUA-POR-DISEÑO. Contador: celdas puntuadas v1_2: 0 → 1 de 14 (`DIN-M-01`); las 13 restantes de P1/P2/P3 quedan fuera de este perímetro, pendientes. Ver `forense/notas/2026-09-03-enmienda-5-din-m-01-doble-ee-cierre.md`.
- 2026-09-03 · EN-CURSO · sesión manual MAESTRA36-N2 por instrucción de mesa (precedente ADR-248); reset del PARO de ENMIENDA 4 resuelto por ENMIENDA 5 (PR #501)
- 2026-09-03 · CONSUMIDO · P1/P2/P3 completos por sesión manual MAESTRA36-N2 (PR #503): 14 de 14 celdas puntúan, scoreboard-v1_2-AGREGADO.md publicado, FP-220/FP-260 actualizadas, ADR-311. Detalle en forense/notas/2026-09-03-MAESTRA36-N2-cierre.md y en la sección CONSUMIDO de forense/encargos/2026-09-03-MAESTRA36-N2-CIERRA-N3-AGREGA-2.md

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

ENCARGO · ACTO MAESTRA34-N3 · AGREGA-2 — invoca /acto (y /score)
SHA de redacción: 8598a72. Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: GATED — ENCOLADO por firma D4-a (1/sep): «D4-a» = los tres encargos de la cadena se archivan en forense/encargos/cola/ en un solo PR [COLA] y /despacha los toma por orden de nombre cuando su compuerta se cumpla. La fusión de ese PR es la firma. Es MAESTRA33-E13 (ADR-269) sobre v1_1 ∪ v1_2.

ENTORNO ASIGNADO: NUBE. NO se lanza en UBUNTU. MODELO SUGERIDO: Opus.
COMPUERTA: MAESTRA34-L2 fusionado con R v1_2 completo (o parcial declarado) Y PR `[L] corridas v1_2` de mesa fusionado Y L-extraido-v1_2.tsv producido con la MISMA regla de extracción congelada de MAESTRA33-E21 (tools/extrae_l_v1_1.py sin editar; si hay que editarlo, PARO y a mesa). Si falta cualquiera, cero commits.
FIRMA DE MESA: scoring v1_1 sellado (E12, ADR-25x — deriva el número): unidades EE(R), delta 0.5, proporción en banda + mediana |z|, L-vs-M pareada, B NO-APLICA. Sin firma nueva.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra 8598a72 ═══
(1) ESTRUCTURA: procedimiento-scoring-v1_1.md + sha; agregado_v1_1.py; tools/score_marco_m.py; scoreboard-v1_1{,-AGREGADO,-AGREGADO-b}.md EXISTE-SATISFACE.
(2) CONTENIDO: `ls forense/prereg-duelo-v2 | grep -i "v1_2\|AGREGADO-c"` → NO-ENCONTRADO (1/sep).
(3) COBERTURA RETROACTIVA: no aplica.

PIEZAS
P1 · Agregado sellado sobre v1_1 ∪ v1_2 sin editar el procedimiento; n total, celdas puntuadas, exclusiones declaradas por celda.
P2 · scoreboard-v1_2-AGREGADO.md con la pregunta doble y sus IC (pareado L_solo−M, L+corpus−M). Declarar si el IC cruza cero; no adjudicar si cruza.
P3 · Insumo al tablero: FP-220 (Ola 6, criterio ≥8 celdas L∩M) y la fila sucesora de FP-221 reciben el conteo real L∩M derivado aquí; nota en motor-nucleo-medible si el criterio de activación del corredor E se cumple (no lo activa: eso es firma de mesa).

PERÍMETRO Y CONCURRENCIA: forense/prereg-duelo-v2/scoreboard-v1_2-AGREGADO.md (+ salida de agregado) · notas · tablero · A.3 · cascada. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar.
CONTADOR: celdas puntuadas 11 → N; scoreboard +1; declarado.
LO QUE NO HACE: no edita el procedimiento de scoring; no re-corre R, M ni L; no activa el corredor E; no abre Ola 6.
SUCESOR: MAESTRA34-E1 · REVISION-FALSADORES (dirección, fecha según D5).

## ENMIENDA DE DIRECCIÓN — 1/sep/2026, contra 9d2e69d (A.3: el verbatim de arriba no se edita; esta enmienda gobierna sobre él)

Se añade al pie de forense/encargos/cola/2026-09-01-MAESTRA34-N3-AGREGA-2.md.

Hallazgo que la motiva: la sesión que sostuvo N3 el 1/sep reportó la compuerta con «faltan 2 de 3» — PR [L] corridas v1_2 y L-extraido-v1_2.tsv. La segunda no tenía dueño en la cadena MAESTRA34 (en v1_1 la produjo un acto propio, MAESTRA33-E21). Defecto de dirección, no del ejecutor.

COMPUERTA (sustituye a la del verbatim): MAESTRA34-L2 fusionado (ya: PR #452, ADR-277) Y PR `[L] corridas v1_2` de mesa fusionado en origin/main, verificado por PRODUCTO: `git show origin/main:forense/prereg-duelo-v2/corridas-L/ | grep -c "__v1_2"` = 224 (14 celdas × 2 variantes × k=8), no por asunto de commit. Si falta, cero commits.

P0 (nueva, antes de P1) · EXTRACCIÓN v1_2. Corre `tools/extrae_l_v1_1.py` SIN EDITAR sobre las 224 capturas → `L-extraido-v1_2.tsv` + sha, con la misma regla congelada de E21 (ADR-272). Reporta extraíbles / no extraíbles con conteo A.13 (precedente v1_1: 171/176). Si el extractor necesita cambio para v1_2: PARO de todo el acto y reporte a mesa — no se parcha dentro de N3.

P1–P3: sin cambio, salvo que P1 puntúa 13 de 14 aplicando `forense/prereg-duelo-v2/exclusiones-v1_2.md` (DIN-M-01, firma DF-a, escrita por MAESTRA34-N4) como exclusión con razón, no como NO-APLICA.

PERÍMETRO: se añade forense/prereg-duelo-v2/L-extraido-v1_2.tsv (+ sha). Todo lo demás igual.
CONTADOR: se añade «L extraídos v1_2: 0 → N».

## ENMIENDA 2 — 2/sep/2026, contra 6330ea3 (A.3: el verbatim de arriba no se edita; esta enmienda gobierna sobre él y sobre la ENMIENDA 1 en lo que la contradice)

PROCEDENCIA DE ESTE TEXTO, declarada: redactado por `ACTO L-CORRIDAS-v1_2` bajo la firma de mesa `DL-(1)` (2/sep/2026), que ordena «appendea la enmienda 2 a N3». Ningún texto verbatim de mesa llegó a la sesión ejecutora para esta enmienda: la sustancia de abajo se deriva de un defecto medido en ese mismo acto, no de un dictado. Mesa confirma o sustituye.

Hallazgo que la motiva: **la COMPUERTA de la ENMIENDA 1 no puede abrir tal como está escrita.** Verifica el producto con `git show origin/main:forense/prereg-duelo-v2/corridas-L/ | grep -c "__v1_2"` = 224, y **el sufijo `__v1_2` no existe en la nomenclatura de `corridas-L/`**: los archivos se llaman `L-<id>-M__<variante>__<indice>.json`, sin versión de spec. Medido el 2/sep contra `origin/main` = `6330ea3`, con control positivo `A.13`: el comando tal cual devuelve **0**; el mismo comando con un patrón que sí existe (`L-CIV-M-01-M`) devuelve **16**; el árbol lista **296** `.json`. No es un cero de la corrida — es un cero de un verificador que presupone un sufijo inexistente. Defecto de dirección heredado de la nomenclatura, no del ejecutor; queda como fila `FP-235` (`ABIERTA`) del tablero.

COMPUERTA (sustituye a la de la ENMIENDA 1): `MAESTRA34-L2` fusionado (ya: PR #452, ADR-277) Y PR `[L] corridas v1_2` de mesa fusionado en `origin/main`, verificado **por producto y por derivación de la spec**, no por asunto de commit ni por sufijo en el nombre. Comando:

```
python3 - <<'EOF'
import importlib.util, subprocess, sys
from pathlib import Path
D = Path("forense/prereg-duelo-v2").resolve()
s = importlib.util.spec_from_file_location("runner_l_cli", D / "runner_l_cli.py")
r = importlib.util.module_from_spec(s); sys.modules["runner_l_cli"] = r
s.loader.exec_module(r)
r._CARGA.L_SPEC_JSON = D / "L-spec-v1_2.json"
arbol = set(subprocess.run(["git","show","origin/main:forense/prereg-duelo-v2/corridas-L/"],
                           capture_output=True, text=True, check=True).stdout.split())
rutas = {ruta.name for *_, ruta, _ in r._iter_plan()}
print("rutas de la spec v1_2:", len(rutas), "| presentes en origin/main:", len(rutas & arbol))
EOF
```

Debe imprimir `224` y `224`. Si el segundo número es menor, faltan capturas y la compuerta NO abre — cero commits. Control positivo obligatorio antes de creerle a un cero: el mismo bloque contra `L-spec-v1_1.json` debe dar `176` y `176`.

Composición de esas 224, para que el conteo no se lea mal: **96** son capturas reanudadas de la corrida v1.1 (`ba7bfa7`) y **128** son nuevas de `ACTO L-CORRIDAS-v1_2`. `corridas-L/` queda con **424** `.json` en total (las 224 de v1.2 más las 80 de v1.1 que v1.2 no comparte más las 120 del marco piloto). **Ningún conteo global del directorio sirve como compuerta** — hay que derivar las rutas de la spec, como arriba.

ASIMETRÍA DE ESQUEMA que P0 debe declarar, no descubrir: las **128** capturas nuevas traen `sha256_prompt` y `params` (esquema de 9 claves de `carga_l_v1_1.py:130`, más `modelo_real`); las **96** reanudadas **no** — la corrida v1.1 las perdió (0 de 176; control positivo: las 8 del piloto `CIV-08` sí las traen). Su equivalencia de prompt quedó **re-derivada, no verificada**, en `forense/notas/2026-09-02-L-corridas-v1_2-cierre.md` §3. Si `tools/extrae_l_v1_1.py` necesitara `sha256_prompt` para extraer, fallaría sobre exactamente esas 96 y no sobre las 128: eso sería el PARO que la ENMIENDA 1 ya prevé («si el extractor necesita cambio para v1_2: PARO de todo el acto y reporte a mesa»), y hay que reportarlo como asimetría de esquema, no como defecto de extracción.

P0–P3: sin cambio respecto de la ENMIENDA 1, salvo la compuerta y la declaración de arriba.

RATIFICACIÓN, verbatim: «Ratificada por dirección (Fable) el 2/sep/2026 contra el reporte de esta sesión: sustituye íntegramente el texto de compuerta que dirección había dictado en conversación (grep -c "__v1_2" = 224), que era inejecutable por el mismo defecto de FP-235. La asimetría de esquema (128 capturas con sha256_prompt/params, 96 sin ellos, re-derivación anexa) queda declarada para P0; el extractor no la trata como fallo.»

---

## ENMIENDA 3 — 3/sep/2026, contra 9badd3c (A.3: el verbatim de arriba no se edita; esta enmienda gobierna sobre las ENMIENDAS 1 y 2 en lo que las precisa)

P0 corre `tools/extrae_l_v1_1.py` sin editar el archivo, con override en runtime de dos constantes de módulo, mismo patrón que `PAQUETE-L-v1_2.md` §4 autorizó para `runner_l_cli.py` (firma `MAESTRA33-E17`): (i) `CORRIDAS_L` → directorio temporal con enlaces simbólicos a las 224 capturas de las 14 celdas de `L-spec-v1_2.json`, seleccionadas por id de celda derivado de la spec, no por sufijo; (ii) `SALIDA_TSV` → `forense/prereg-duelo-v2/L-extraido-v1_2.tsv`. Control positivo antes de escribir: el mismo override apuntado a las 176 capturas de v1_1 reproduce `L-extraido-v1_1.tsv` byte a byte; si no, PARO y a mesa. `sha256` del script pegado en la nota; `--regresion` corrido y en verde. Firma de mesa verbatim: «Autorizo el parche a la línea 136 y el override de las cuatro constantes; mi firma es la fusión de este PR. — mesa, 3/sep/2026».

PERÍMETRO: se añade `tools/extrae_l_v1_1.py`, edición acotada a la línea 136 y la constante `CELDAS_ESPERADAS`; se añade `forense/prereg-duelo-v2/L-extraido-v1_2-notas-cierre.md`.

---

## ENMIENDA 4 — 3/sep/2026 (A.3: el verbatim de arriba no se edita; esta enmienda gobierna sobre las ENMIENDAS 1–3 en lo que las supera)

P0 ejecutado fuera de esta cola por PR #497 (`6019bd7`): script parcheado sha `efb71de1…`, `L-extraido-v1_2.tsv` y `L-extraido-v1_2-notas-cierre.md` en `origin/main`, sellos v1_1 intactos. N3 verifica su existencia (A.8) y no repite P0; arranca en P1 (13 de 14, exclusión DIN-M-01 con razón). La ENMIENDA 3 queda superada por producto. Firma de mesa: la fusión de este PR. — mesa, 3/sep/2026

---

## ENMIENDA 5 — 3/sep/2026, contra `e8bf0de` (A.3: el verbatim de arriba no se edita; esta enmienda corrige las ENMIENDAS 1 y 4 en lo que quedaron VENCIDAS EN ALCANCE)

Corrige la ENMIENDA 1 (línea 42, "13 de 14") y la ENMIENDA 4 (línea 93,
"arranca en P1 (13 de 14, exclusión DIN-M-01 con razón)"): ambas quedaron
**VENCIDAS EN ALCANCE** (A.10) por la firma de mesa `d2` del 2/sep/2026
(`ACTO MAESTRA35-L5 · R-DIN-M-01`, `exclusiones-v1_2.md:31-34`, verbatim):
«Exclusión LEVANTADA por firma de mesa `d2`... N3/N5 puntúan **14 de 14**,
con la reserva de (a).» `d2` es posterior a `DF-a` (la firma que ambas
enmiendas citaban) y ya vive en `origin/main` desde antes de la ENMIENDA 4
(`3b9191d`, 2/sep 23:20:59 UTC, ancestro de `HEAD`) — la lectura "13 de 14"
contradice el verbatim vigente.

**P1 puntúa 14 de 14**: `DIN-M-01` entra con `R` de
`corridas-R/DIN-M-01.json` (`DISEÑO-APROXIMADO`, `FP-249` FIRMADA),
conforme a `exclusiones-v1_2.md:31-34` (`d2`, verbatim, arriba) y
`exclusiones-v1_2.md:36-42` (`d1`, verbatim): «una `R` con
`DISEÑO-APROXIMADO` SÍ puntúa, con la reserva escrita en el JSON y en el
scoreboard: `EE_R` es cota inferior (factor de diseño ≈1.20 medido;
conglomerado de viviendas no público). El scoreboard reporta `z` con las
DOS `EE` (aproximada y sin diseño); si el veredicto de la celda cambia
entre las dos, la celda se marca AMBIGUA-POR-DISEÑO y no cuenta como
puntuada. Si no cambia, cuenta.»

**Implementación de `d1`**, obligatoria y no cubierta hoy por
`tools/score_marco_m.py` (lee solo `EE_R`, líneas 80-87): para `DIN-M-01`,
`z` se calcula dos veces —con `EE_R` y con `EE_R_sin_diseno`, ambos ya en
`corridas-R/DIN-M-01.json`— sin editar el procedimiento sellado
(`procedimiento-scoring-v1_1.md`) ni `agregado_v1_1.py`: un paso adicional
en el mismo acto,
`forense/prereg-duelo-v2/din_m_01_doble_ee.py` (nuevo), que reporta ambas
`z` (`z_L`, `z_M`, `dif_pareada_z = z_L − z_M`, misma unidad y comparación
principal de `procedimiento-scoring-v1_1.md` §1/§3) y su veredicto de
banda. Resultado en
`forense/prereg-duelo-v2/din-m-01-doble-ee-resultado.json` y en
`forense/notas/2026-09-03-enmienda-5-din-m-01-doble-ee-cierre.md`: con
`EE_R` y con `EE_R_sin_diseno` el veredicto es el mismo
(FUERA-DE-BANDA en ambas) — **no cambia** → la celda **cuenta** como
puntuada, no queda AMBIGUA-POR-DISEÑO. La reserva de `d1` (`EE_R` cota
inferior, factor de diseño `1.1997866170250338`) queda escrita en ese
resultado y en la nota de cierre, para el scoreboard.

PERÍMETRO: se añade el paso/script de las dos `EE` bajo
`forense/prereg-duelo-v2/` (`din_m_01_doble_ee.py` +
`din-m-01-doble-ee-resultado.json`), nombrado arriba, más la nota de
cierre. `tools/score_marco_m.py` **no se edita** (si hiciera falta, PARO y
a mesa).

CONTADOR: «celdas puntuadas v1_2: 0 → 1 de 14» (`DIN-M-01`, con reserva de
diseño, sin AMBIGUA-POR-DISEÑO); las AMBIGUA-POR-DISEÑO se reportan aparte
(ninguna en este acto). Las 13 celdas restantes quedan fuera del perímetro
de esta enmienda — P1/P2/P3 completos siguen pendientes.

Firma de mesa: la fusión de este PR. — mesa, 3/sep/2026
