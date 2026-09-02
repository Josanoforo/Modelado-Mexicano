ESTADO: LISTO-NUBE
ENTORNO: NUBE
ENCOLADO: 2026-09-02 · gesto de encolado, precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026)
BITACORA:
- 2026-09-02 · LISTO-NUBE · encolado por PR [COLA] encola MAESTRA34-L1/N1/N2/L2/N3. COMPUERTA propia: MAESTRA34-L2 fusionado con R v1_2 completo (o parcial declarado) Y PR `[L] corridas v1_2` de mesa fusionado Y L-extraido-v1_2.tsv producido con la MISMA regla de extracción congelada de MAESTRA33-E21 (tools/extrae_l_v1_1.py sin editar; si hay que editarlo, PARO y a mesa). Si falta cualquiera, cero commits.

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
