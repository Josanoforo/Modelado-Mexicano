# Nota de cierre — `ACTO INSTRUCCIONES-v2_11`, 21/ago/2026, nube

Encargo: `forense/encargos/2026-08-21-INSTRUCCIONES-v2_11.md` (`CONSUMIDO`). ADR: `canon/gobernanza-v1_15.md` `ADR-142`.

## ARRANQUE

- **Repo.** Clon existente en `/home/user/Modelado-Mexicano`. `git log -1 --format="%h %s"` → `0fe511c Merge pull request #308 from Josanoforo/claude/operador-combinacion-mediana-y43ex2`. `git status` → limpio, sobre `claude/instrucciones-proyecto-v2-11-ue3if5`.
- **SHA contra el declarado.** El encargo declara `gate: #4 fusionado` — `ADR-141`/`ACTO SELLA-OPLUS`, `PR #307`, ya fusionado a `main` vía `PR #308`. `main` no se movió durante este acto (verificado antes y después de escribir). No es `PARO`.
- **`data/raw`.** No se usa en este acto. Saltado.
- **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (valor crudo, sin sonda; este acto no toca microdato ni red).
- **Espejo.** No usado — toda cifra sale del clon, comando a la vista abajo.

## Verificación de existencia (A.8)

**(1) Estructura.** Tablas gobernantes de este dominio: `instrucciones-proyecto-v2_10.md` (texto vigente a copiar), `canon/registro-rotulos.tsv` (espacio `A.N`), `forense/firmas-pendientes.tsv` (fila `FP-100`, ya abierta por `ACTO REPARA-T22`).

**(2) Contenido — `instrucciones-proyecto-v2_11.md` no existía.**
```
$ ls instrucciones-proyecto-v2_11.md
ls: cannot access 'instrucciones-proyecto-v2_11.md': No such file or directory
```
`NO-ENCONTRADO`, universo = raíz del árbol.

**(3) Cobertura retroactiva.** No aplica: es un artefacto nuevo, no una clasificación de "no existe" sobre trabajo previo.

## Rótulo `A.13` — máximo derivado antes de escribir

```
$ grep -oE "^#{0,3} ?A\.[0-9]+ ·" instrucciones-proyecto-v2_10.md
A.1 ·
A.2 ·
A.3 ·
A.4 ·
A.5 ·
A.6 ·
A.7 ·
### A.8 ·
A.9 ·
A.12 ·
### A.10 ·
```
Máximo: `A.12`, sin huecos. Siguiente: `A.13`, libre. No colisiona con la serie independiente de ids de refutación de `milpa/refutations.yaml` (hoy `01`–`28`, incluidos `ref.A.13`…`ref.A.19`) — frontera ya declarada en `A.10` (nota de numeración) y en `canon/registro-rotulos.tsv`: "dos habitantes... viven en documentos distintos... sin colisión práctica". `A.11` sigue libre (v2.9) y no se reclama aquí; `A.7` disputado y sin firma de mesa, no se toca.

## T1 — `instrucciones-proyecto-v2_11.md`

Copia íntegra de v2.10 + una línea al punto 4 del ARRANQUE (Bloque D) + sección `A.13` completa (con "Por qué v2.11" y nota de numeración). Contención verificada por `diff`, no asumida:
```
$ diff instrucciones-proyecto-v2_10.md instrucciones-proyecto-v2_11.md | grep '^<' | wc -l
0
$ wc -l instrucciones-proyecto-v2_10.md instrucciones-proyecto-v2_11.md
  384 instrucciones-proyecto-v2_10.md
  400 instrucciones-proyecto-v2_11.md
```
Cero líneas suprimidas; 16 líneas nuevas. v2.10 es subconjunto estricto de v2.11, mismo criterio que `ADR-91(b)` ya verificó para v2.9⊂v2.10.

## T2 — `A.9`, la mitad del acto

El ADR declara la fecha del pegado explícitamente y no la asume: **`PENDIENTE — no sellada hasta el pegado`**, mismo mecanismo que `ADR-78`/`ADR-81(c)` dejaron precedentado para v2.8 (`gobernanza:1152`, `gobernanza:1250`). Ningún acto con herramientas de repo puede pegar en el proyecto de Claude — vive fuera del repositorio. Queda declarado en `ADR-142(a)`, para que una sesión futura (o enmienda in situ de mesa) registre la fecha el mismo día del pegado.

## T3 — ADR + tablero

`ADR-142`, candidateado contra el máximo verificado por `grep -oE 'ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n -u | tail -1` → `141`, único, sin huecos. `FP-100` verificado existente antes de tocarla (`grep -n "^FP-100" forense/firmas-pendientes.tsv` → una sola fila, abierta por `ACTO REPARA-T22`) — sin duplicar, defecto de `FP-58`. Pasa `ABIERTA`→`FIRMADA`, fecha `2026-08-21`.

Tablero tras este acto: **104 filas · 75 `FIRMADA` · 13 `ABIERTA` · 1 `CERRADA POR PREMISA REFUTADA` · 16 `CERRADA`**, re-derivado por comando, no heredado.

## Consecuencia obligada: recifrado de `canon/estado-programa-v1_10.md`

Mismo precedente que `ADR-136`/`ADR-137` ya dejaron sentado: sellar un `ADR` mueve el conteo vigente que `T15`/`T16` vigilan en `estado-programa`, y no sincronizarlo rompe la línea base. Recifrado: cabecera (`141 ADR`→`142 ADR`), `L0` (nueva entrada de cascada), y la línea de auto-chequeo de la suite (`19 FAIL · 142 WARN`, sin cambio neto — `FP-100` ya contaba como `WARN` de `T22` desde `ACTO REPARA-T22`; el único movimiento es la convergencia de `T15`/`T16`). Nada más de ese archivo se toca.

## Línea base final

```
$ python3 tests/check.py --baseline
...
  19 FAIL · 142 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
────────────────────────────────────────────────────────────────────────
```

## Perímetro respetado

Tocado: `instrucciones-proyecto-v2_11.md` (nuevo) · `forense/firmas-pendientes.tsv` (`FP-100`) · `canon/gobernanza-v1_15.md` (`ADR-142`) · `forense/hallazgos.md` · `forense/encargos/` (este encargo) · esta nota · `canon/estado-programa-v1_10.md` (solo las cifras de cascada `ADR`/`FAIL`/`WARN`, consecuencia obligada, declarada arriba). No tocado: `instrucciones-proyecto-v2_10.md` (se conserva íntegro) · `milpa/` · `data/` · `corpus/` · ningún test.

Contador: medición sobre México = 0.
