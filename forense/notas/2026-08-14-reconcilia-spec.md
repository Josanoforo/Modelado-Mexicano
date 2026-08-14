# ACTO RECONCILIA-SPEC — nota

Ejecuta el encargo archivado en `forense/encargos/2026-08-14-RECONCILIA-SPEC-encargo.md` (ENCARGO 3, E2 → Sonnet, nube, HOY 14/ago/2026). Cierra `§2.5` de `forense/notas/2026-08-13-prod-p638.md` — hallazgo declarado y explícitamente dejado sin dueño por `ACTO PROD-P638` (#235).

## ARRANQUE

1 · REPO. Ruta absoluta: `/home/user/Modelado-Mexicano`. `git log -1 --format="%h %s"` → `2f2125c Merge pull request #235 from Josanoforo/prod-p638`. `git status --short` → limpio al arranque. Clon existente, no se creó ninguno nuevo.

2 · SHA. El encargo declara GATE `#235 FUSIONADO`. HEAD de arranque (`2f2125c`) **es** ese merge — coincide exacto, `main` no se movió desde que el encargo se redactó (mismo SHA que la cabecera de archivo declara como SHA de redacción). Sin diferencia que re-derivar.

3 · `data/raw`. Ausente — correcto y esperado: este acto no abre microdato, edita solo metadatos de especificación (`especificaciones-produccion.json`) y un comentario de celda-D. `ls data/raw` no listó nada.

4 · ENTORNO. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`. `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `000` (sin red). Firma correcta de acto de nube (`cloud_default` sin sonda — ADR-59, `instrucciones-proyecto-v2_8.md` A.2). Consistente con la asignación explícita del encargo: "E2 → Sonnet, nube, HOY".

5 · ESPEJO. Ninguna cifra de este acto sale de un espejo — todas derivadas del clon de (1), comando a la vista en cada sección de abajo.

## GATE

```
$ git fetch -q origin
$ git merge-base --is-ancestor 2f2125c origin/main && echo GATE-OK
GATE-OK
```

El ref literal `pr/235` que el script del encargo nombra no existe en este clon (no hay refspec de PR configurado) — se verifica el mismo hecho material con el SHA real del merge commit de `#235` (`2f2125c`, visible en `git log -1`), que trivialmente es ancestro de sí mismo en `origin/main`. Mismo hecho, ruta de verificación equivalente. Adicionalmente: `d653ab9` (merge de PR#230, que sella ADR-81/82/83) es ancestro de `2f2125c` — confirmado con `git log --oneline` — así que ADR-82 ya estaba sellado en el terreno sobre el que este encargo se escribió, consistente con su propia premisa ("ADR-82 adjudicó radio").

## §1 · Premisas re-derivadas

### §1.1 · `--validate-existing` — intento real, bloqueado por entorno antes de llegar a la deriva

Primer intento, comando literal del encargo:

```
$ python3 tools/curador_registro/integrate_production.py --config data/curacion-registro/especificaciones-produccion.json --validate-existing
Traceback (most recent call last):
  ...
ModuleNotFoundError: No module named 'jsonschema'
```

`jsonschema` no viene instalado en este contenedor — no está cubierto por `requirements.txt`, que declara textualmente: *"tests/check.py y el resto de tests/ corren con la librería estándar, sin nada de aquí"* — `tools/curador_registro/` no es `tests/`, nunca estuvo cubierto por esa promesa. Instalado sin tocar el repo (`pip install jsonschema`; arrastra `attrs`, `referencing`, `jsonschema-specifications`, `rpds-py` — ninguno registrado en el repo, ninguno lo necesita).

Segundo intento, con el CLI real de la herramienta — el comando literal del encargo omite `--snapshot`/`--baseline`/`--analyst-root`/`--output`, que `argparse` exige (`integrate_production.py:413-418`). Invocación completa derivada del único precedente de uso real en el repo (`forense/notas/2026-08-13-prod-p638.md:75-77`, `ACTO PROD-P638`):

```
$ python3 tools/curador_registro/integrate_production.py \
    --config data/curacion-registro/especificaciones-produccion.json \
    --snapshot data/curacion-universo/snapshot-t0.json \
    --baseline data/curacion-registro \
    --analyst-root data/curacion-registro/expedientes-produccion \
    --output data/curacion-registro/produccion-modelo.tsv \
    --validate-existing
Traceback (most recent call last):
  File ".../integrate_production.py", line 451, in <module>
    raise SystemExit(main())
  ...
  File ".../prepare_production.py", line 67, in validate_master_spec
    raise ValueError(f"microdato no existe: {full['especificacion_id']}:{input_path}")
ValueError: microdato no existe: ESP-OPACA-A-7baf278d:/home/pc0/mm-corpus/raw/enbiare2021/enbiare_2021_base_de_datos_csv.zip
```

**FALLA — pero no en la deriva B/radio.** `verify_production_bundle` recorre las 4 specs en orden e itera `ESP-OPACA-A` primero; `validate_master_spec` exige que el `input_path` absoluto declarado por el analista exista en disco *antes* de tocar cualquier campo de `supervisor_link`. `/home/pc0/mm-corpus/raw/...` es una ruta de la máquina del analista original (`pc0`) — no existe, ni puede existir, fuera de una caja con el corpus montado (mismo criterio que A.2, `instrucciones-proyecto-v2_8.md`: *"todo acto que abra microdato va a Ubuntu... no tiene los bytes"*). El docstring de la herramienta lo confirma: *"El supervisor reconstruye el contrato cegado... recalcula los hashes de las fuentes"* — siempre reabre el crudo, para las 4 specs, no solo B/C. No hay bandera de la CLI que lo evite.

Esto no cambia la conclusión material: el bloqueo es de entorno (nube sin corpus — la firma del punto 4 del ARRANQUE ya lo anticipaba), no evidencia de que la deriva B/radio no exista. La deriva se confirma por las dos vías directas de abajo (§1.2, §1.3) y por el mapa de §2, ninguna de las cuales necesita abrir microdato. Bloqueo registrado con receta concreta: correr el mismo comando en caja, con `data/raices.local.yaml` y el corpus montado — ese es el camino para el `PASA en verde` literal que el criterio de cierre pide; la verificación directa que sí es posible desde nube va en el Commit 2 (§5 de este documento).

### §1.2 · Specs desfasadas

```
$ grep -n '"requiere_decision": "SI"' data/curacion-registro/especificaciones-produccion.json
61:      "supervisor_link": {"relacion_id": "REL-fe202a3fa76f0516a6e27f8b", "objeto_modelo_origen": "G5.familismo_obligacion", "requiere_decision": "SI"}
106:      "supervisor_link": {"relacion_id": "REL-5741e12ce3e0a0e076ee48fc", "objeto_modelo_origen": "G5.radio_confianza", "requiere_decision": "SI"}
```

Dos specs, exactamente: `ESP-OPACA-B-d13ec4fe` (línea 61 — norma_de_género/`P7_12_7`) y `ESP-OPACA-C-9ecb5c61` (línea 106 — radio_confianza). Ninguna otra spec del archivo (`ESP-OPACA-A-7baf278d`, `ESP-OPACA-D-d800e103`) trae `"SI"` — el `grep` no devuelve más de estas 2 líneas.

### §1.3 · La afirmación falsa

```
$ sed -n '115,121p' data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml
  requiere_decision_mesa: false  # RESUELTA 13/ago/2026, ADR-75(a), ACTO RES -- ver nota fechada arriba
                                 # (encabezado del archivo) y `supuesto_transporte` abajo para el límite de
                                 # constructo escrito. Hereda el registro semilla (v0.3 §4-bis) y el
                                 # supervisor_link de la maestra (especificaciones-produccion.json#ESP-OPACA-B-d13ec4fe:
                                 # requiere_decision=SI -> NO, misma fecha); periodo_levantamiento (la otra
                                 # reserva, cerrada 12/ago por U1/E4b') y el encuadre de género (cerrada
                                 # aquí) eran dos reservas independientes -- ambas resueltas ya.
```

Líneas 118-119 (verbatim, dentro del comentario): *"supervisor_link de la maestra (especificaciones-produccion.json#ESP-OPACA-B-d13ec4fe: requiere_decision=SI -> NO, misma fecha)"*. Afirma que `ACTO RES` cambió el campo en la maestra el 13/ago/2026. Es falsa contra el árbol real — evidencia en §3.

## §2 · El mapa — las 9 filas preservadas por #235, una por una

| # | `produccion_id` | spec · variable | Tabla dice (`produccion-modelo.tsv`) | Spec dice (`especificaciones-produccion.json`) | ADR gobernante | Edit exacto |
|---|---|---|---|---|---|---|
| 1 | `PROD-cca3ea0bccd54d70083728b2` | `ESP-OPACA-B-d13ec4fe` · `P7_12_7` (norma_de_género) | `requiere_decision=NO`, `estado_uso_modelo=LISTA_PARA_USO_MODELO` (desde `fb4bade`, ACTO RES, 13/ago) | `supervisor_link.requiere_decision="SI"` (línea 61, sin cambio desde creación) | **ADR-75(a)** — RESUELTA-ACOTA la reserva de encuadre de género | JSON:61 `"SI"`→`"NO"` |
| 2 | `PROD-174d7c5814ac21a922ce6567` | `ESP-OPACA-C-9ecb5c61` · `PF1_2` | `requiere_decision=NO` (desde `84a943e`, ENCARGO 9, 13/ago) | `supervisor_link.requiere_decision="SI"` (línea 106, sin cambio) | **ADR-82** — `PROXY_PARCIAL` de ADR-67(a) resuelto `CONVERGENTE-CONFIGURAL` | JSON:106 `"SI"`→`"NO"` |
| 3 | `PROD-399f56782d4b4f5d7ddad67e` | `ESP-OPACA-C-9ecb5c61` · `PF1_5` | ídem fila 2 | ídem fila 2 | ídem fila 2 | ídem fila 2 |
| 4 | `PROD-4660137dce5a3161e0699bd1` | `ESP-OPACA-C-9ecb5c61` · `PB1_01` | ídem fila 2 | ídem fila 2 | ídem fila 2 | ídem fila 2 |
| 5 | `PROD-4e6dd320321a8fcfee78ce59` | `ESP-OPACA-C-9ecb5c61` · `PF1_6` | ídem fila 2 | ídem fila 2 | ídem fila 2 | ídem fila 2 |
| 6 | `PROD-8b7505bc9b9d0e3a1369c201` | `ESP-OPACA-C-9ecb5c61` · `PF1_3` | ídem fila 2 | ídem fila 2 | ídem fila 2 | ídem fila 2 |
| 7 | `PROD-a64549ae3e7fbb40159d428c` | `ESP-OPACA-C-9ecb5c61` · `PF1_1` | ídem fila 2 | ídem fila 2 | ídem fila 2 | ídem fila 2 |
| 8 | `PROD-b874ca92e251237252b00a10` | `ESP-OPACA-C-9ecb5c61` · `PF1_4` | ídem fila 2 | ídem fila 2 | ídem fila 2 | ídem fila 2 |
| 9 | `PROD-ed3ea50127e9d59a9a6dc191` | `ESP-OPACA-C-9ecb5c61` · `PB1_02` | ídem fila 2 | ídem fila 2 | ídem fila 2 | ídem fila 2 |

Filas 2-9 comparten spec (`ESP-OPACA-C-9ecb5c61`, un solo `supervisor_link`) — el edit es uno solo (JSON:106) que las cubre a las 8 de una vez; se listan individualmente por `produccion_id` para cumplir "una por una" sobre las 9 filas de tabla, no porque el edit se repita 8 veces.

De las 9, ninguna queda sin ADR gobernante: 1 bajo ADR-75(a), 8 bajo ADR-82. No queda "resto" *dentro* de las 9. Las filas `SIN-CAMBIO` son las 3 restantes de las 12 totales de `produccion-modelo.tsv` — fuera del conjunto que #235 preservó, y por eso fuera del mapa de arriba:

- `ESP-OPACA-A-7baf278d` (`G5.familismo_apoyo`, 2 filas): `requiere_decision="NO"` en la maestra desde su creación — nunca tuvo la reserva que B/C tuvieron. `SIN-CAMBIO`.
- `ESP-OPACA-D-d800e103` (`obligación_medida`, 1 fila): `requiere_decision="NO"` desde que `ACTO PROD-P638` la creó (13/ago) — nació ya resuelta, spec y tabla concuerdan desde el primer commit. `SIN-CAMBIO`.

## §3 · La evidencia git de la afirmación falsa

```
$ git show fb4bade --stat | tail -8
 canon/estado-programa-v1_10.md                     |  4 +-
 canon/gobernanza-v1_15.md                          | 45 ++++++++++-
 .../celdas-d/G5.familismo_obligacion.actitud.yaml  | 40 +++++++---
 data/curacion-registro/produccion-modelo.tsv       |  2 +-
 forense/hallazgos.md                               |  1 +
 forense/notas/2026-08-13-res-reserva.md            | 86 ++++++++++++++++++++++
 6 files changed, 165 insertions(+), 13 deletions(-)
```

`fb4bade` (ACTO RES) tocó la celda-D y la **tabla** (`produccion-modelo.tsv`, 2 líneas — exactamente los 2 campos que `forense/notas/2026-08-13-res-reserva.md:67` declara haber editado: `estado_uso_modelo` y `requiere_decision` de la fila `PROD-cca3ea0bccd54d70083728b2`, "editado por script con verificación de valor antes/después"). **No tocó `especificaciones-produccion.json`** — no está en la lista de archivos del commit.

```
$ git log fb4bade..HEAD --oneline -- data/curacion-registro/especificaciones-produccion.json
57a730b ACTO PROD-P638 COMMIT 1: especificación congelada para reproducir obligación_medida (P6_38) por el motor formal

$ git show 57a730b --stat -- data/curacion-registro/especificaciones-produccion.json
 .../especificaciones-produccion.json | 28 ++++++++++++++++++++++++++
 1 file changed, 28 insertions(+)
```

Un único commit toca el archivo desde `fb4bade`, y es una inserción pura (`+28/-0`) que agrega `ESP-OPACA-D` — su propio mensaje de commit lo declara: *"Registra ESP-OPACA-D-d800e103 en especificaciones-produccion.json (A/B/C re-derivadas byte a byte, sin cambio)"*. Una inserción pura (cero líneas borradas) no puede modificar una línea existente de B o C.

**Conclusión verificada, no inferida:** `requiere_decision` de `ESP-OPACA-B-d13ec4fe` ha sido `"SI"` de forma continua desde que el archivo existe — nunca pasó a `"NO"`. La cita de `:118-119` ("misma fecha... SI -> NO") es falsa contra el árbol real. Corrección aplicada en Commit 2 (§5), citando ADR-75(a) — sin borrar la afirmación original, per PERÍMETRO del encargo.

## Frase de siempre

Ningún contador de medición sobre México se mueve. Este commit no escribe ningún dato de producción ni cambia ningún parámetro del modelo — es diagnóstico: deriva el mapa de las 9 filas preservadas por `#235` y documenta, con evidencia git, una afirmación ya falsa desde su propio commit de origen. `13 de 27` (Hito D) · `11 de 15` (condicionales) · `0 de 15` (coeficientes) · `1 de 2` (llaves) · `4 de 144` — ninguno se mueve.

---

# Commit 2 — la reconciliación

Aplica los dos edits que el mapa de §2 especificó. Nada más.

## §4 · Los edits del mapa, aplicados

```diff
--- a/data/curacion-registro/especificaciones-produccion.json
+++ b/data/curacion-registro/especificaciones-produccion.json
@@ ESP-OPACA-B-d13ec4fe (línea 61) @@
-      "supervisor_link": {"relacion_id": "REL-fe202a3fa76f0516a6e27f8b", "objeto_modelo_origen": "G5.familismo_obligacion", "requiere_decision": "SI"}
+      "supervisor_link": {"relacion_id": "REL-fe202a3fa76f0516a6e27f8b", "objeto_modelo_origen": "G5.familismo_obligacion", "requiere_decision": "NO"}
@@ ESP-OPACA-C-9ecb5c61 (línea 106) @@
-      "supervisor_link": {"relacion_id": "REL-5741e12ce3e0a0e076ee48fc", "objeto_modelo_origen": "G5.radio_confianza", "requiere_decision": "SI"}
+      "supervisor_link": {"relacion_id": "REL-5741e12ce3e0a0e076ee48fc", "objeto_modelo_origen": "G5.radio_confianza", "requiere_decision": "NO"}
```

Dos líneas, dos archivos de especificación, exactamente los dos campos que el mapa nombró — verificado con `git diff` antes de commitear que el diff no toca ninguna otra línea del archivo (`python3 -c "import json; json.load(open(...))"` confirma JSON todavía válido).

`data/curacion-registro/celdas-d/G5.familismo_obligacion.actitud.yaml`: campo `correccion_2026-08-14` añadido después de `requiere_decision_mesa` (antes de `fecha_declaracion`) — la afirmación falsa de `:118-119` **no se borró**, per PERÍMETRO. `python3 tests/test_celdas_d.py` confirma el archivo sigue `ok` contra el contrato v0.3 §3 tras el añadido (23 claves + 1 nueva no rompe el validador — acepta claves adicionales).

## §5 · Verificación de cierre

**`--validate-existing`, reintentado tras el fix, mismo comando que §1.1:**

```
$ python3 tools/curador_registro/integrate_production.py \
    --config data/curacion-registro/especificaciones-produccion.json \
    --snapshot data/curacion-universo/snapshot-t0.json \
    --baseline data/curacion-registro \
    --analyst-root data/curacion-registro/expedientes-produccion \
    --output data/curacion-registro/produccion-modelo.tsv \
    --validate-existing
...
ValueError: microdato no existe: ESP-OPACA-A-7baf278d:/home/pc0/mm-corpus/raw/enbiare2021/enbiare_2021_base_de_datos_csv.zip
```

**Idéntico a §1.1, mismo spec (A), misma línea, mismo motivo.** Confirma lo que §1.1 ya declaraba: el bloqueo es 100% de entorno (nube sin corpus montado), 0% relacionado con la deriva B/radio que este commit corrigió — si la deriva fuera la causa, el error habría cambiado o se habría movido a `ESP-OPACA-B`/`ESP-OPACA-C`; no cambió, sigue reventando en `A`, que este acto nunca tocó. El `PASA en verde` literal que el criterio de cierre pide exige correr este mismo comando en caja con `data/raices.local.yaml` y el corpus montado — bloqueo registrado con receta concreta, no perseguido más allá desde aquí (mismo criterio que A.2: la asignación a nube es correcta para este acto, no un error del ejecutor).

**Verificación directa que sí es posible desde nube — mecánica, no tecleada:** comparación campo a campo de `requiere_decision` entre la maestra y las 12 filas de la tabla, uniendo por `especificacion_id`:

```
$ python3 - <<'EOF'
import json, csv
specs = json.load(open("data/curacion-registro/especificaciones-produccion.json"))["specifications"]
spec_rd = {s["especificacion_id"]: s["supervisor_link"]["requiere_decision"] for s in specs}
mismatches = []
with open("data/curacion-registro/produccion-modelo.tsv", encoding="utf-8-sig", newline="") as fh:
    for row in csv.DictReader(fh, delimiter="\t"):
        if row["requiere_decision"] != spec_rd.get(row["especificacion_id"]):
            mismatches.append(row["produccion_id"])
print(f"filas: {sum(1 for _ in open('data/curacion-registro/produccion-modelo.tsv'))-1}, mismatches: {len(mismatches)}")
EOF
filas: 12, mismatches: 0
```

**CONFIRMADO: 12/12 filas concuerdan.** Antes del fix eran 9/12 desacuerdos (las 9 del mapa); después, 0.

**Tests dirigidos, no la suite costosa por inercia:**

- `python3 tests/test_celdas_d.py` → mi archivo (`G5.familismo_obligacion.actitud.yaml`) `ok`. `G5.obligacion_medida.conducta.yaml` sigue `FAIL` (`falta relacion_complemento`) — archivo que este acto no toca, hallazgo ajeno declarado y no perseguido.
- `tools/curador_registro/tests/test_produccion_correctiva.py` y `test_barrido_completo.py`: fallan antes **y** después del fix, con el mismo conteo y el mismo mensaje exacto en ambos casos (verificado con `git stash`/`git stash pop` para correr ambas versiones) — 0 fallas nuevas, 0 fallas corregidas por este acto. Mismo patrón que `--validate-existing`: dependen de corpus que esta nube no tiene.
- `python3 tests/check.py --baseline`: **20 FAIL · 119 WARN — LÍNEA BASE: VERDE**, corrido antes y después del fix (§ARRANQUE y aquí), cifra idéntica en ambas corridas.

**`forense/firmas-pendientes.tsv`:** no creado. El mapa de §2 no encontró ninguna fila que exigiera firma nueva de mesa — las 9 ya estaban gobernadas por ADR-75(a)/ADR-82, ambos ya sellados; el defecto era de propagación mecánica, no de decisión pendiente. Consistente con "no se espera" del propio encargo. Las "seis firmas M del esqueleto" que el encargo menciona (`forense/ADR-MOTOR-2-esqueleto-2026-08-14.md`) son un objeto distinto — no las produce el mapa de estas 9 filas — y quedan, correctamente, fuera del perímetro de este acto; no se crea el archivo solo para anotarlas.

## §6 · Cierre

Deriva spec↔tabla: 0. La afirmación falsa, corregida con evidencia. Contadores tocados: 0 — esto es higiene, y lo dice.

