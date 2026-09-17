# ACTO GEN2-MANTENIMIENTO-4

> Archivado por A.3 (0-bis) — texto **verbatim** del mensaje de dirección
> que lanzó este acto, 17/sep/2026. No se edita en ningún otro punto salvo
> las secciones `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` que la cascada
> añade al final (pasos 10 y 11 de `/acto`).

---

ENCARGO · ACTO GEN2-MANTENIMIENTO-4 · WARN→ESTADO: LA SUITE DEJA DE PONERSE EN ROJO POR CONTAR SU PROPIO RUIDO
CABECERA · redactado contra `1746e1a` (merge de #846); re-deriva al abrir — si #849 ya fusionó, mejor: sincroniza antes de tocar `tests/` · ENTORNO: NUBE — cero microdato · COMPUERTA: #848 (TRÁMITE-4) y #846 (CORTE-EDAD-1) en `origin/main` — cumplida al redactar · MODELO SUGERIDO: Sonnet (cambio de código acotado con firma ya dada; sube a Opus solo si T16 exige rediseño) · FP/ADR/NC: deriva al cierre, no heredes (máximos hoy: FP-384, NC-0303, ADR-537; #849 traerá los suyos — sincroniza y renumera si fusiona antes) · vehículo: `/acto`.
FIRMA DE MESA que gobierna (verbatim, ya sellada y propagada; se cita, no se pide): `data/corrida0/decisiones.tsv`, objeto `suite:WARN-nuevos-son-estado`: "LOS WARN NUEVOS SON ESTADO REPORTABLE, NO RUIDO: la rutina de derivados reporta «solo FAIL nuevos y WARN nuevos», de modo que un WARN nuevo entra al reporte diario" (origen `forense/encargos/2026-09-16-GEN2-RUTINA-DERIVADOS-1.md:18`, propagada por ADR-534).
VERIFICACIÓN DE EXISTENCIA (A.8, dirección, contra `1746e1a`):

* (1) Estructura: `tests/check.py` (T16 `T-SUITE-SELF-CHECK` :839-880; `--baseline` contra `tests/baseline.json`), cabecera L0 de `canon/gobernanza-v1_15.md:231` ("→ 3 FAIL · 4380 WARN"), `forense/rutinas.tsv` (huellas). Cubren.
* (2) Contenido, medido: sobre `1746e1a` la suite da 4 FAIL · 4381 WARN, ROJO, y el único FAIL nuevo es T16: "declara 3 FAIL · 4380 WARN vigente; la corrida real da 4381". El agente de rutina lo reprodujo: VERDE ×2, ROJO ×3 sobre el mismo árbol + `DIGESTO-2026-09-17.md` (`forense/rutinas.tsv`, huella PARO del 17/sep). Consecuencia medida en 24 h: tres renumeraciones y tres recifrados de cabecera (#844, #846, #849) para cuadrar una cifra que cambia con cada merge. Un mecanismo que hace esto: NO-ENCONTRADO — `grep -n "WARN nuevos" tests/check.py` → reporta el conteo.
* (3) Cobertura retroactiva: la firma es del 16/sep; T16 es anterior (ADR-2xx); ningún acto la ha ejecutado en código.

PIEZAS
P1 · T16 deja de asertar el total de WARN. T16 compara contra la afirmación vigente solo el número de FAIL; el total de WARN pasa a informativo: se imprime, no se asierta. La cabecera L0 conserva su formato pero su cifra de WARN queda rotulada `(informativo)`; un desfase de WARN no produce FAIL. Los canónicos que hoy declaran "N FAIL · M WARN vigente" no se editan hacia atrás: T16 los lee como históricos si el FAIL cuadra.
P2 · `--baseline` adjudica por FAIL y reporta WARN nuevos como estado. El veredicto VERDE/ROJO se calcula solo sobre FAIL frente a `tests/baseline.json`; los WARN nuevos frente a la línea base se listan (id de test + primera línea) bajo un rótulo `WARN NUEVOS (estado, no adjudican)`, que es lo que la firma pide y lo que la rutina de derivados ya consume. T22 (firmas ABIERTA) y T34 (no-corrido ABIERTA) conservan sus WARN con edad, como contador. `tests/baseline.json` se regenera una vez con el comando de la casa, y el diff se pega.
P3 · Prueba y huella. Test nuevo: añadir un archivo neutro a `forense/digesto/` no cambia el veredicto de `--baseline`. Corrida antes/después pegada. `forense/rutinas.tsv`: la huella PARO del 17/sep recibe enmienda fechada "causa: T16 asertaba WARN; resuelto por ADR-<este>". Línea en `hallazgos.md`: "T16 asertaba el total de WARN; cada merge lo movía; costó tres renumeraciones en una noche (#844, #846, #849) y un PARO de rutina (#850)".
PERÍMETRO Y CONCURRENCIA: `tests/check.py` · `tests/baseline.json` · `tests/test_suite_warn_estado.py` (nuevo) · `canon/gobernanza-v1_15.md` (cabecera L0 + ADR) · `forense/rutinas.tsv` (enmienda) · `forense/hallazgos.md` · nota de cierre · cascada. No toca `tests/test_motor_holdout.py` (NC-0305 es otro acto), ningún test sustantivo, `milpa/`, specs ni resultados. En paralelo: PR #849 (piloto, pendiente de fusión — si fusiona a mitad, sincroniza y renumera), #850 y el despacho (rutina: `forense/digesto/`, `rutinas.tsv` — este acto no los fusiona ni los edita; se fusionan después de éste). «Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»
CONTADOR: cero mediciones, dicho sin disfraz. Mueve: `--baseline` deja de dar ROJO por artefacto (medido antes/después). LO QUE NO HACE: no cambia ningún test sustantivo · no toca NC-0305 · no fusiona los PR de rutina · no edita canónicos hacia atrás. SUCESOR: fusión de #850 y del despacho; la corrección de `test_a2` (NC-0305). CIERRE: cascada + `## NO-CORRIDO / RESERVAS` + `## CONSUMIDO`.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| `forense/rutinas.tsv`: enmienda fechada a la huella PARO del 17/sep ("causa: T16 asertaba WARN; resuelto por `ADR-539`") | `NO-VERIFICABLE-AQUÍ` — la fila PARO del 17/sep todavía no existe en `origin/main`: la trae la rutina paralela `#850`, sin fusionar, y este acto declara explícitamente en su perímetro que no fusiona ni edita `#850` | la huella queda sin su causa explicada hasta que `#850` fusione y la fila exista en el árbol | `NC-0314`, `DIFERIDO-A:PR#850` |
| `test_a2` de `tests/test_motor_holdout.py` (guardia de firma completa vs. append-only) | `FUERA-DE-PERÍMETRO` — el encargo lo excluye por nombre («No toca `tests/test_motor_holdout.py` (`NC-0305` es otro acto)») | la guardia sigue sin corregir; no bloquea (ese archivo no corre en `tests/check.py`) | `NC-0305` |
| Fusión de `#849`/`#850` y del despacho de la cola | `FUERA-DE-PERÍMETRO` — el encargo prohíbe explícitamente fusionar o editar los PR de rutina paralelos | ninguno propio de este acto; `#850` sigue `PARO` hasta que ese ciclo lo resuelva | `DIFERIDO-A:PR#850` |
