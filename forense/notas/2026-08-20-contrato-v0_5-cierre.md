# Nota de cierre · `ACT-PIL-1 · CONTRATO-v0_5`

**Procedencia.** Encargo recibido como texto de tarea (sin adjuntos), 20/ago/2026, entorno NUBE (repo-only), gateado por `PR #295` fusionado (`ACTO SELLA-ADV`, `ADR-128`). Refina el borrador §5 de `forense/encargos/2026-08-20-SELLA-ADV.md` — el texto ejecutado añade `variante_corredor` como campo hermano de `rol` y gatea `estado_decidibilidad` por `vocabulario_version` en vez de exigirlo sin condición; ver `ADR-129` para el detalle completo de cada diferencia. Sella `ADR-129`. Detalle sustantivo del acto: `propuesta-motor-adaptativo-celda-v0_5.md` y la propia entrada de `ADR-129`. Esta nota archiva la evidencia cruda que el encargo pidió pegar.

## ARRANQUE — los cinco puntos

1. **Repo.** `/home/user/Modelado-Mexicano`, rama `claude/act-pil-1-contrato-v0-5-ow1nj5`, `git status` limpio al arrancar.
2. **SHA.** `7d38cb039b8ebc82a01aa6d27da8d80c2357a2ea` — coincide con el `7d38cb0` que citaba el encargo; sin `origin/main` adicional que consultar más allá del HEAD de esta rama, que ya trae `PR #295` fusionado (confirmado: `ADR-128` legible, `canon/registro-rotulos.tsv` ya existe en este SHA).
3. **`data/raw`:** no se usa. No existe, no se monta, no se consulta.
4. **Entorno**, valor crudo, sin sonda:
   ```
   $ echo "ENV_VAR=$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE"
   ENV_VAR=cloud_default
   ```
5. **Espejo:** prohibido, y no se consultó ninguno — sesión sin acceso a nada fuera de este repositorio.

**Dueña única**, `pgrep -af claude`:
```
493  /bin/sh -c ... environment-manager task-run --stdin --session cse_019jqBJJhgWg45igQjHhrRUW ...
497  /usr/local/bin/environment-manager task-run --stdin --session cse_019jqBJJhgWg45igQjHhrRUW ...
529  claude --output-format=stream-json ... --model claude-sonnet-5 ...
2569 /bin/bash -c ... eval 'echo ... && pgrep -af claude' ...   # el propio comando, se cita a sí mismo
```
Un único proceso `claude` (529) y sus wrappers de entorno (493/497); la línea 2569 es la propia invocación de este comando (contiene el literal `pgrep -af claude` en su línea de comando, coincide consigo misma). Ninguna otra sesión.

## VERIFICACIÓN DE EXISTENCIA (A.8) — re-derivada, no heredada

**(1)** `propuesta-motor-adaptativo-celda-v0_4.md` + `tests/test_celdas_d.py`, indexadas en `data/INFRAESTRUCTURA-v1_0.md` Dominio 5 (línea 152: *"Dominio 5 · Registrar una celda-D del piloto"*) — confirmado leyendo las dos, no solo el índice.

**(2)** `v0_5` `NO-ENCONTRADO`:
```
$ ls propuesta-motor-adaptativo-celda-v0_*.md
propuesta-motor-adaptativo-celda-v0_1.md
propuesta-motor-adaptativo-celda-v0_2.md
propuesta-motor-adaptativo-celda-v0_3.md
propuesta-motor-adaptativo-celda-v0_4.md
```
`BASELINE_INGENUO`/`ENSAMBLE`/`estado_decidibilidad`, `NO-ENCONTRADO` en `tests/test_celdas_d.py`:
```
$ grep -n "BASELINE_INGENUO\|ENSAMBLE\|estado_decidibilidad" tests/test_celdas_d.py
(sin resultados)
```
Archivo completo leído (no solo el grep) antes de confirmar la ausencia — el error del turno anterior que el encargo señaló era confiar en el conteo sin abrir el archivo; aquí se abrió completo.

**(3)** Sin brecha retroactiva:
```
$ git log -1 --format='%h %ci' -- data/curacion-registro/celdas-d/
fe1df36 2026-08-17 21:08:18 +0000
$ git log -1 --format='%h %ci' -- tests/test_celdas_d.py
f3873c2 2026-08-13 23:18:26 -0600
```
Ambos anteriores al 20/ago/2026.

## T2(e) — derivación propia de los rótulos `D` en `ADR-128`

Tabla completa en `propuesta-motor-adaptativo-celda-v0_5.md` §3(e) y en `ADR-129`(c). Resumen: `1×D-1, 1×D-2, 5×D-4, 3×D-5, 6×D-6, 1×D-iv`, contados a mano sobre el texto completo de la entrada `ADR-128` (título + incisos (a)-(g) + "NO hace" + "Cascada" + cierre), coincide exacto con lo que el encargo esperaba.

## T2(e) — por qué `T25` NO se amplía a `D` (hallazgo central de este acto)

Cambio hecho, verificado, y revertido — en ese orden, dentro de la misma sesión:

```
$ sed -i 's/(M|E)-?/(M|E|D)-?/' tests/check.py   # (edición real, no shell -- vía Edit tool)
$ python3 -c "
import sys; sys.path.insert(0,'tests'); import check
check.FAILS.clear(); check.t25_rotulos()
print(len(check.FAILS), 'FAIL')"
67 FAIL
```
67 archivos de `canon/`+`forense/`, no censados en `_T25_ARCHIVOS_CONOCIDOS`, traen un `Dn`/`D-n` pelado. De esos, **46 caen en el rango `D-1`..`D-6`** — no es solo ruido de dos dígitos, fácil de descartar por convención:

```
$ python3 -c "... re.search(r'\`D-?[1-6]\`', m) ..."
46 fails dentro de D-1..D-6, entre ellos:
  forense/notas/2026-08-19-doc-backfill-cierre.md -> D-6
  forense/notas/2026-08-18-rescate-curador-cierre.md -> D-4
  forense/notas/2026-08-19-corte-edad-convencion-cierre.md -> D-2
  forense/encargos/2026-08-19-U2-EV1.md -> D-5
  forense/encargos/2026-08-19-MESA-19AGO.md -> D-5
  forense/encargos/2026-08-19-FICHA-R51-D3.md -> D-1
  ... (lista completa: salida del comando arriba, 46 líneas)
```
Todos fechados entre el 31/jul y el 19/ago/2026 — **antes** de que `ADR-128` sellara el espacio `D` de hoy (20/ago). Ninguno puede ser una cita del piloto ADV-DUELO; son usos genéricos y preexistentes de "D" como marcador de punto/decisión, exactamente el fenómeno que `canon/registro-rotulos.tsv` ya tenía anotado sin derivar, en la fila `N, R, H, S, U, D`: *"namespaces nombrados por el paquete de lanzamiento (8-33 usos c/u); este acto no re-derivó cada valor individualmente"*.

**Decisión:** revertir el regex a `(M|E)` (diff final vacío en `tests/check.py` contra el HEAD de arranque) y declarar el hallazgo, en vez de forzar 46+ archivos a `_T25_ARCHIVOS_CONOCIDOS` sin verificarlos uno por uno — que además excede el perímetro declarado de este acto (*"`tests/check.py` (solo el regex de `T25`)"*) y el criterio que T3 de este mismo encargo pide aplicar: *"si falla, el cambio está mal diseñado — se corrige el cambio, no lo que rompe"*. `canon/registro-rotulos.tsv` sí registra `D-1`…`D-6`/`D-i`…`D-iv` (T2(e), mitad "registro" cumplida); la mitad "vigía" queda declarada como hallazgo abierto para un acto futuro con perímetro propio para censar el espacio `D` completo.

## T3 — validador, salida cruda

```
$ python3 tests/test_celdas_d.py
G5.familismo_obligacion.actitud.yaml [G5.familismo_obligacion.actitud]: ok
G5.obligacion_medida.conducta.yaml [G5.obligacion_medida.conducta]: ok
G5.radio_confianza.encuci_vs_enbiare.yaml [G5.radio_confianza.encuci_vs_enbiare]: ok

3 archivo(s) de celda-D validan contra propuesta-motor-adaptativo-celda-v0_5.md §3.
```

**Verificación de que el validador sí valida** (once casos sintéticos contra `errors_for()` en memoria, sin escribir en `data/`):

| # | caso | esperado | resultado |
|---|---|---|---|
| 1 | `vocabulario_version: 0.5` sin `estado_decidibilidad` | FALLA | `falta 'estado_decidibilidad' (v0.5 §3(b), obligatorio bajo vocabulario_version 0.5)` |
| 2 | `vocabulario_version: 0.5` con `estado_decidibilidad: SKIP:sin_dato` | PASA | `[]` |
| 3 | `vocabulario_version: 0.4` sin `estado_decidibilidad` | PASA (compuerta) | `[]` |
| 4 | `estado_decidibilidad: GANADOR` (con `vocabulario_version: 0.4`) | FALLA | `estado_decidibilidad inválido: 'GANADOR' …` |
| 5 | `vocabulario_version: 0.9` | FALLA | `vocabulario_version inválida: 0.9 …` |
| 6 | `margen_material: 0.05` | PASA | `[]` |
| 7 | `margen_material: PENDIENTE-DERIVACION` | PASA | `[]` |
| 8 | `margen_material: 'como un 5%'` | FALLA | `margen_material inválido: 'como un 5%' …` |
| 9 | `variante_corredor: L-mixto` | FALLA | `variante_corredor inválida: 'L-mixto' …` |
| 10 | `rol: ENSAMBLE_VIEJO` | FALLA | `rol inválido: 'ENSAMBLE_VIEJO' …` |
| 11 | `rol: ENSAMBLE`, sin `variante_corredor` | PASA | `[]` |

Los seis casos ilegales fallan; los cinco legales pasan. Comando completo, reproducible, en la sesión que produjo esta nota (no comiteado como test nuevo — el encargo no lo pidió y el perímetro no lo nombra).

## T4 — `milpa/src/motor.py`, antes y después

**Verificado por lectura de `milpa/src/motor.py::evaluar()`, antes de correr nada:** solo lee `estado_operativo`, `tipo_adjudicacion` e `id` de cada celda. Ninguno de los cinco cambios de vocabulario (`rol`, `resultado`/`estado_decidibilidad`, `margen_material`, `vocabulario_version`) es un campo que el motor toque — así que una salida idéntica antes/después no es casualidad, es la consecuencia directa de qué lee el módulo.

**ANTES** (SHA `7d38cb0`, antes de cualquier edición de este acto):
```
$ python3 -c "from milpa.src import motor, salida; import json; r=motor.correr(); print(json.dumps(r, ensure_ascii=False)); print('HASH:', salida.hash_salida(r))"
{"version_motor": "0.1.0", "semilla": 0, "contador_condicionales_medidas": 12, "celdas_no_cero_en_B": 15, "coeficientes_puntuales": 14, "coeficientes_sin_magnitud": 1, "momentos_total": 22, "momentos_ajuste": 8, "momentos_holdout": 14, "holdout_reproducidos": 0, "resultados": [{"celda_id": "G5.familismo_obligacion.actitud", "tipo_adjudicacion": "CALIBRACION_CONJUNTA", "estado_operativo": "LISTO", "veredicto": "EXISTE-NO-SATISFACE", ...}, {"celda_id": "G5.obligacion_medida.conducta", ..., "veredicto": "EXISTE-NO-VERIFICADO", ...}, {"celda_id": "G5.radio_confianza.encuci_vs_enbiare", ..., "veredicto": "EXISTE-NO-VERIFICADO", ...}]}
HASH: 01d5bc1ef963c466c11bc8df1fb2b2161d910d203234487da8fde6af606d966c
```

**DESPUÉS** (con `propuesta-motor-adaptativo-celda-v0_5.md`, `tests/test_celdas_d.py`, `canon/registro-rotulos.tsv`, `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md` ya editados):
```
$ python3 -c "from milpa.src import motor, salida; import json; r=motor.correr(); print(json.dumps(r, ensure_ascii=False)); print('HASH:', salida.hash_salida(r))"
{"version_motor": "0.1.0", "semilla": 0, "contador_condicionales_medidas": 12, "celdas_no_cero_en_B": 15, "coeficientes_puntuales": 14, "coeficientes_sin_magnitud": 1, "momentos_total": 22, "momentos_ajuste": 8, "momentos_holdout": 14, "holdout_reproducidos": 0, "resultados": [{"celda_id": "G5.familismo_obligacion.actitud", "tipo_adjudicacion": "CALIBRACION_CONJUNTA", "estado_operativo": "LISTO", "veredicto": "EXISTE-NO-SATISFACE", ...}, {"celda_id": "G5.obligacion_medida.conducta", ..., "veredicto": "EXISTE-NO-VERIFICADO", ...}, {"celda_id": "G5.radio_confianza.encuci_vs_enbiare", ..., "veredicto": "EXISTE-NO-VERIFICADO", ...}]}
HASH: 01d5bc1ef963c466c11bc8df1fb2b2161d910d203234487da8fde6af606d966c
```

**Mismo hash, mismos tres veredictos.** `data/curacion-registro/celdas-d/*.yaml` y `milpa/src/` no se tocaron en ningún momento de este acto.

## `--baseline`, antes y después

**Antes** (antes de cualquier edición): `21 FAIL · 120 WARN`, `LÍNEA BASE: VERDE`.

**Después**: ver cierre de esta nota / `ADR-129` — salida cruda pegada tras terminar todas las escrituras del acto, sección final de esta nota.

## Perímetro tocado, verificado contra lo declarado

`propuesta-motor-adaptativo-celda-v0_5.md` (nuevo) · banner en `propuesta-motor-adaptativo-celda-v0_4.md` · `tests/test_celdas_d.py` · `tests/check.py` (tocado y revertido — diff vacío) · `canon/registro-rotulos.tsv` · `canon/gobernanza-v1_15.md` (`ADR-129`, cabecera de conteo) · `canon/estado-programa-v1_10.md` (cascada de conteo de ADR — extensión mínima de perímetro, ver `ADR-129`) · `forense/encargos/2026-08-20-SELLA-ADV.md` (línea `Estado`) · esta nota · `forense/hallazgos.md`. No se tocó `data/curacion-registro/celdas-d/*.yaml`, `milpa/`, `data/`, `corpus/`, ni nada del perímetro de `ACT-PIL-2`.

## Contador

Medición sobre México movida por este acto: **0**, dicho. `13 de 27` (Hito D), `11 de 15` (condicionales), `15 coeficientes cero medidos`, `4 de 144`, llaves de identificación ejercidas: todos intactos. El cascarón queda listo para recibir celdas del piloto v2.

---

## Salida final de `python3 tests/check.py --baseline`

_(pegada tras terminar todas las escrituras de este acto, dos corridas idénticas verificadas — determinista)_

```
════════════════════════════════════════════════════════════════════════
  VERIFICACIÓN DEL CORPUS
════════════════════════════════════════════════════════════════════════
  [ ok ]  T01 fuente única de verdad
  [FAIL]  T02 duplicados nombre/contenido  (2 fail)
  [warn]  T03 referencias colgantes  (47 warn)
  [ ok ]  T04 ADR-33 diagonal en ENTONCES
  [FAIL]  T05 ADR-32.c constructos en glosario  (5 fail)
  [FAIL]  T06 consistencia numérica  (2 fail)
  [ ok ]  T07 vocabulario de tiers
  [FAIL]  T08 mapa de evidencia por report  (1 fail)
  [FAIL]  T09 marco (c) usado como causa  (8 fail)
  [warn]  T10 diáspora (b) sin marcar  (65 warn)
  [FAIL]  T11 afirmaciones de estado absolutas  (1 fail)
       motor: 49 reglas · 20 [FUERTE] · 20`[FUERTE]` · 19`[MEDIA]` · 5`[MEDIA-FUERTE]` · 2`[HIPÓTESIS]` · 1`[FUERTE como correlación]` · 1`[FUERTE / MEDIA]` · 1`[MEDIA / HIPÓTESIS]`
  [ ok ]  T12 conteos del motor
  [warn]  T13 cabecera de versión ADR-36  (1 warn)
  [ ok ]  T14 T-INVENTARIO
  [ ok ]  T15 T-ADR-COUNT
  [ ok ]  T17 T-FICHAS-COUNT
  [ ok ]  T18 T-PASO2-EJECUCION
  [ ok ]  T19a cabecera cruzada estado→modelo
  [ ok ]  T19b contador 14 cruzado (modelo)
  [ ok ]  T19c portada derivada (README)
  [ ok ]  T20 T-CASCADA-MARCADA
  [ ok ]  T21 T-CAPA2-CAPA3
  [FAIL]  T22 T-FIRMAS  (2 fail, 7 warn)
  [ ok ]  T23 T-CABLEADO
  [ ok ]  T24 T-LLAVES-EJERCIDAS
  [ ok ]  T25 T-ROTULOS
  [ ok ]  T16 T-SUITE-SELF-CHECK

────────────────────────────────────────────────────────────────────────
  WARN (120)
────────────────────────────────────────────────────────────────────────
  · T10: 65
  · T03: 47
  · T22: 7
  · T13: 1

────────────────────────────────────────────────────────────────────────
  FAIL (21)
────────────────────────────────────────────────────────────────────────
  · T09: 8
  · T05: 5
  · T02: 2
  · T06: 2
  · T22: 2
  · T08: 1
  · T11: 1

════════════════════════════════════════════════════════════════════════
  21 FAIL · 120 WARN
════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
  (1 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
────────────────────────────────────────────────────────────────────────
```

**Idéntico a la corrida "antes" de este acto** (`21 FAIL · 120 WARN`, `LÍNEA BASE VERDE`) — mismo desglose por test, categoría por categoría. Dos hallazgos intermedios se abrieron y cerraron dentro de la misma sesión, antes de este cierre: `T15` marcó `FAIL` transitorio (una cita `128 ADR` involuntaria dentro del propio texto nuevo de `ADR-129`, explicando la cascada — reformulada para no repetir el patrón `\d+\s*ADR\b`) y `T16` marcó `FAIL` en cascada (mismo origen). Ninguno de los dos llegó a un commit — corregidos antes de cerrar, verificados por esta misma corrida.
