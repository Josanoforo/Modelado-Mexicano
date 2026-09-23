# `/revisa --post-hoc` · PR #1036 · Piloto 4: encogida en cruces reservados de ENVIPE 2025

**VEREDICTO: NO-FUSIONAR** (post-hoc: el PR ya se fusionó — `73b7f11` — mientras esta
sesión verificaba su compuerta para otro acto; este veredicto es el que la
lista habría dado ANTES de fusionar, y ahora describe un defecto ya en `main`).
Recuento: **3 BLOQUEA · 2 RESERVA · 0 NO-VERIFICADO · 6 NO-APLICA**.

## Identidades del merge

- `BASE` (padre 1, `origin/main` antes del merge): `412f280`
- `HEAD` de la rama fusionada (padre 2, `acto/gen2-celda-d-piloto-4-encogida-1`): `7fc29d1`
- Commit de merge en `origin/main`: `73b7f11` (`Merge pull request #1036 from Josanoforo/acto/gen2-celda-d-piloto-4-encogida-1`)
- Modo: **`--post-hoc`** — no se comenta en GitHub; este archivo es el único
  artefacto, publicado en un PR `[REVISA]` que contiene únicamente esta nota.

## Hallazgos

### H1 — BLOQUEA (punto 2.11 / A.14) — falta `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO`

El encargo archivado (`forense/encargos/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1.md`)
termina en `7fc29d1` en su §10 original, sin ninguna de las dos secciones de
cierre:

```
$ git show 7fc29d1:forense/encargos/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1.md | tail -5
## 10 · NO HACE · SUCESORES · CIERRE
No adopta, no elicita L, no toca cruces vistos. Sucesor: firma de adopción de C-ENCOGIDA si replica; piloto 5 en ENCIG (los dos cruces reservados de `gobierno_digital`). Auditoría: la spec la trae; la nota la contesta. Cierre por /acto.
```

A.14: *"Lo que no se corrió se asienta, o el acto no cierra."* Este acto sí
dejó trabajo fuera de lo pedido (ver H3: el candidato C1 y C7 del §1/§5 no
se ven mencionados con dictamen individual en la nota de cierre más allá del
agregado por cruce) sin ninguna fila `NC-…` que lo asiente. Confirmado
también contra el TSV derivado:

```
$ git diff 412f280...7fc29d1 -- forense/no-corrido.tsv
(vacío)
```

Cero filas nuevas en `forense/no-corrido.tsv`. El acto cerró sin la sección
que A.14 exige como condición de cierre.

### H2 — BLOQUEA (punto 2.8 / D-10 / §9 del encargo) — cascada de cierre no corrió: sin ADR, sin `canon/L0/<raíz>`, sin `registro-rotulos`

El §9 del encargo declara como perímetro propio, explícitamente,
`canon/L0/<raíz>.md`. Ninguna de las tres piezas de la cascada estándar
(`/acto` bloque 5, pasos 1/3/4) aparece en el diff fusionado:

```
$ git diff --name-only 412f280...7fc29d1 -- canon/
(vacío)

$ git diff --name-only 412f280...7fc29d1 -- canon/registro-rotulos.tsv
(vacío)

$ git show 7fc29d1:canon/registro-rotulos.tsv | grep -i "PILOTO-4-ENCOGIDA"
(sin coincidencias)
```

No hay `ADR-<AAMMDD>-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-<hhhh>-NN` en
`canon/gobernanza-v1_15.md`, no hay fragmento en `canon/L0/`, y el rótulo del
acto no está censado en `canon/registro-rotulos.tsv`. El acto produjo
resultado científico (COMMIT-1/2/3, dictamen `FALSADOR-DÉBIL`, cuatro
celdas-D) pero nunca corrió el cierre que lo hace auditable en el registro
de gobernanza — es exactamente el "perímetro de cierre permanente" (D-21)
que el propio encargo cita en su §9 y que quedó sin publicar.

### H3 — BLOQUEA (punto 2.5, cifra no re-derivable por ausencia de registro) — `celdas_validadas` no se puede verificar que subió

El `CONTADOR` de la cabecera promete *"`celdas_validadas` sube por cada
celda PROSPECTIVA (hasta ≈38 …)"*. Sin ADR ni entrada de gobernanza (H2), no
hay dónde leer que el contador efectivamente se movió como registro
oficial del programa — las celdas-D sí quedaron escritas
(`data/curacion-registro/celdas-d/TRA.evade_norma.envipe2025.*.yaml`, 4
archivos) pero la cifra que el encargo prometió reportar en el canon nunca
se escribió donde `E.4` manda leerla (`corrida0.py status` sobre los TSV
derivados). Esta cifra queda **contradicha por ausencia de registro**, no
sólo `NO-VERIFICADA`: el mecanismo que la haría contable (H2) no corrió.

### R1 — RESERVA (punto 2.3, tocado y no declarado, pero con razón visible en los propios commits)

Archivos fuera del perímetro §9 literal: `data/INFRAESTRUCTURA-v1_0.md`,
`tests/check.py`, `tests/test_piloto4_v1_0.py`,
`forense/analisis/ci-guardias/censo-tests.tsv`,
`forense/prereg-caja/TRA-evade-norma-cruces-encogida-enmienda-2.md`,
`forense/encargos/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-ADENDA-1.md`.
Todos caen dentro del "perímetro de cierre permanente" que D-21 exime de
enumeración (test propio cableado a CI, tabla en `INFRAESTRUCTURA`) o son
adendas/enmiendas ya citadas y selladas dentro de la propia secuencia de
commits (`b5a7665`, `7ffa0a0e`). No es desbordamiento silencioso — es
`RESERVA` informativa, no cambia el veredicto.

### R2 — RESERVA (punto 2.9, `check.py --rapido` VERDE pero con 335 WARN preexistentes)

```
$ cd <worktree @ 7fc29d1> && python3 tests/check.py --rapido
...
FAIL: 0 — VERDE
0 FAIL · 335 WARN
```

Cero `FAIL` nuevos atribuibles a este PR; los 335 `WARN` son deuda
preexistente del árbol (`T-NO-CORRIDO`, `T22`, etc., ninguno con el rótulo
de este acto). `RESERVA` informativa: no bloquea, D-16 no adjudica por WARN.

## Tabla de los once puntos

| # | Punto | Estado | Comando |
|---|---|---|---|
| 2.1 | Encargo archivado verbatim, coherente con reporte | **BLOQUEA** (ver H1) | `git log --reverse 412f280..7fc29d1 \| head -1` → 0-bis correcto; pero cierre incompleto |
| 2.2 | Orden spec-antes-de-resultados | PASA | `git log --format='%h %ad %s' --date=iso --reverse 412f280..7fc29d1`: COMMIT-1 `5939e9d` 20:44 antes de COMMIT-2 `eb7f7c2` 20:52; enmienda de cableado `c2eb888` 20:49 solo toca `seed`, declarada D-18, antes de `ejecucion.json` |
| 2.3 | Perímetro declarado vs. tocado | RESERVA (ver R1) | `git diff --name-only 412f280...7fc29d1` vs §9 del encargo |
| 2.4 | Negativos con conteo A.13 | NO-APLICA | El acto no reporta negativos de existencia relevantes al dictamen; los negativos de control (`DELTA-P-MAX=0`) traen su propio conteo en la nota de cierre |
| 2.5 | Cifras re-derivadas | **BLOQUEA** (ver H3) | ausencia de registro de `celdas_validadas` |
| 2.6 | Originales intactos | NO-APLICA | el encargo no exige preservar ningún archivo específico sin editar |
| 2.7 | Escala/universo declarados | PASA | tabla de la nota de cierre trae unidad (pp), universo (n2025 min–max por celda), IC95 |
| 2.8 | ADR/FP/NC con raíz de acto | **BLOQUEA** (ver H2) | `git diff --name-only 412f280...7fc29d1 -- canon/` → vacío |
| 2.9 | `check.py --baseline`/`--rapido` sobre la vista previa | RESERVA (ver R2) | `python3 tests/check.py --rapido` → 0 FAIL, 335 WARN preexistente |
| 2.10 | "Lo que NO hace" respetado | PASA | no adopta (`champion_actual` no tocado), no elicita L, no toca cruces vistos — confirmado en la nota de cierre y ausencia de cambios en `tramite.yaml`/adopción |
| 2.11 | `## NO-CORRIDO / RESERVAS` cotejado | **BLOQUEA** (ver H1) | sección ausente del encargo archivado y de `forense/no-corrido.tsv` |
| 2-bis | REVISA-CALC (identidad/sello/replay) | PASA, con reserva de entorno | dos CALC sellados, `verify` REPRODUCE/IDÉNTICO citado en la nota de cierre (`forense/analisis/gen2-celda-d-piloto-4-encogida-1/evidencia-replay.json`); esta sesión corrió en NUBE y no reabrió microdato — la corroboración de `verify` se toma de la propia nota, no se re-ejecuta aquí (declarado, no oculto) |

`CONTADOR: cero mediciones, declarado (infraestructura).`

## Qué NO revisó este pase

- No se re-corrió `corrida0.py verify` sobre los dos CALC (exige CAJA/microdato
  ENVIPE 2024/2025; esta sesión corre en NUBE). Se citó el `REPRODUCE`/`IDENTICO`
  que la propia nota de cierre reporta, sin corroborarlo de nuevo — es lectura
  documental, no ejecución (Enmienda 1 del bloque 2-ter).
- No se auditó línea por línea el contenido estadístico de `adjudicacion.py`
  ni la fórmula de λ heredada del piloto 3 — el punto 2-bis de identidad/sello
  se limitó a los artefactos de registro (sellos, `ejecucion.json`, asientos
  de replay), no a una relectura matemática de la implementación.
- No se comparó este hallazgo con el recibo paralelo `GEN2-RECIBO-ASTRA-1`
  (ADR `…-4e74-01`, ya en `canon/`) más allá de constatar que ese ADR
  pertenece a otro acto y no cubre el cierre de éste.

Este comentario no aprueba, no fusiona y no empuja nada. Fusionar es firmar,
y firmar es de mesa; en este caso el PR ya se fusionó sin que mesa tuviera
esta lectura — el sucesor natural es que dirección decida si el cierre
faltante (H1/H2/H3) se completa con un acto de continuación (`ADR` + `L0` +
`## NO-CORRIDO`/`## CONSUMIDO` retroactivos sobre el encargo archivado) o si
se declara deuda aceptada con su propia fila `NC-…`.
