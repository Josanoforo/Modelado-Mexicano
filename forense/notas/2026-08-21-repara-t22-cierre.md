# Nota de cierre — `ACTO REPARA-T22`, 21/ago/2026, nube

Encargo: `forense/encargos/2026-08-21-REPARA-T22.md` (`CONSUMIDO`). ADR: `canon/gobernanza-v1_15.md` `ADR-137`.

## ARRANQUE

- **Repo.** Clon existente en `/home/user/Modelado-Mexicano`. `git log -1 --format="%h %s"` → `fc7f0c7 Merge pull request #304 from Josanoforo/claude/sella-m5-v2-benchmark-fh3759`. `git status` → limpio, sobre `claude/repara-t22-firmas-u7q8xv`.
- **SHA contra el declarado.** El encargo declaraba `8b73aee`. `main` se movió a `fc7f0c7` (`PR #304`, `ACTO SELLA-M5-V2` fusionado) entre que se escribió el encargo y que arrancó este acto. No es `PARO`: se refresca (`git fetch origin main`), se re-deriva máximo de `ADR` (`136`, no `135`) y máximo de `FP` (`FP-98`, no `FP-95`) por comando, y se reporta aquí.
- **`data/raw`.** No se usa en este acto. Saltado.
- **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (valor crudo, sin sonda).
- **Espejo.** No usado — toda cifra sale del clon, comando a la vista abajo.
- **Dueña única.** `pgrep -af claude` al arrancar: un solo proceso de sesión (el `claude` de este acto), sin concurrencia detectada.

## Verificación de existencia (A.8)

Reconfirmado contra `fc7f0c7`:
```
$ python3 tests/check.py --baseline 2>&1 | grep -A5 "· T22:"
  · T22: 2
      forense/encargos/2026-08-17-CONSOLIDA-17AGO.md trae un marcador ...
      forense/notas/2026-08-17-consolida.md trae un marcador ...
```
Los dos `FAIL` de arranque coinciden exactamente con lo que el encargo describía para `8b73aee` — el drift de `main` no cambió el censo de `T22`.

## T1 — tabla de costo (medida antes de tocar el regex)

Comando: recorrido de `canon/*.md` + `forense/**/*.md` + `forense/**/*.tsv` (la misma lista que recorre `t22_firmas` (b)), un patrón por fila, insensible a mayúsculas/minúsculas (`re.IGNORECASE`), contra las filas de `dónde` en `forense/firmas-pendientes.tsv` para derivar "sin cita".

| patrón | archivos | sin cita |
|---|---|---|
| `pendiente de mesa` | 16 | 9 |
| `mesa decide` | 38 | 28 |
| `decide mesa` | 4 | 2 |
| `sin sellar` | 34 | 24 |
| `NO SELLADO` | 14 | 8 |
| `acto sucesor` | 26 | 14 |
| `queda abierto` | 16 | 9 |
| `sin resolver` | 69 | 54 |
| `no se resuelve aquí` | 12 | 9 |
| `pendiente de firma` | 1 | 0 |
| `ninguna elegida por este acto` | 1 | 1 |
| `este acto no elige` | 3 | 1 |
| `PROPUESTA` | 184 | 140 |
| `REGISTRADO, NO SELLADO` | 6 | 3 |
| `desvío de alcance` | 5 | 3 |
| `requiere_decision` | 50 | 39 |

Nota sobre las cifras del encargo: el encargo (T5) citaba, de memoria/ejemplo, "`pendiente de mesa` (10 archivos), `mesa decide` (35), `sin sellar` (31), `acto sucesor` (24)" — las cifras re-derivadas hoy (`9`/`38`/`34`/`26`) no coinciden exactamente; se re-derivaron por comando y no se heredaron, siguiendo la misma disciplina que `ADR-135`/`ADR-136` ya dejaron medida ("no heredes estas cifras"). No se ensancha ningún patrón en este commit.

## T2 — las dos reparaciones mecánicas

**(a)** `forense/encargos/2026-08-17-CONSOLIDA-17AGO.md` y `forense/notas/2026-08-17-consolida.md` sumados a `_T22_ARCHIVOS_CONOCIDOS` (`tests/check.py`) — citan verbatim el bloque de patrones de su propia Parte 3 como ejemplo, diagnóstico ya escrito el mismo día en la propia nota. `T22` vuelve a 0 `FAIL`.

**(b)** Exención de `t22_firmas` (b) acotada a filas `ABIERTA`/`FIRMADA` (antes: cualquier fila, incluida `CERRADA`, exentaba el archivo completo para siempre). Medido antes de commitear:
```
archivos que dejan de estar exentos: 21
FAIL nuevos con exención acotada: 3
 - forense/encargos/2026-08-17-EDEC-fuente-unica-decisiones.md
 - forense/encargos/2026-08-18-LANE-A-E0-E5.md
 - forense/notas/2026-08-17-fuente-unica-decisiones.md
```
`3 ≤ 3` — no dispara el `PARA` del encargo (`> 3`). Los tres, leídos uno por uno, resultaron ser el mismo mecanismo de autocaptura verbatim que (a): `EDEC` y su nota reproducen el comando `grep -n "pendiente nombrado\|queda para mesa\|sigue en mesa"` que el propio acto corrió contra `gobernanza-v1_15.md` y describen su resultado ("hits sin fila"); `LANE-A-E0-E5` usa "RANURAS DEL SELLO" como nombre de una sección propia a llenar con firmas de `ADR-100` ya existentes, no una ranura nueva. Los tres se suman también a `_T22_ARCHIVOS_CONOCIDOS`, con su razón. Ninguno es un pendiente real sin registrar.

El propio encargo archivado de este acto (`forense/encargos/2026-08-21-REPARA-T22.md`, verbatim por `A.3`) dispara el mismo mecanismo al citar los patrones de `T22` como parte de su propia descripción — sumado también, mismo criterio.

## T3 — las cuatro filas que se escaparon

Verificado antes de crear filas: `forense/firmas-pendientes.tsv` no tenía, hasta este acto, ninguna fila que citara `mesa-pendientes.md` — las tres secciones del archivo (§1, §2, §3) nunca habían llegado al tablero. Sin duplicado (`grep -n "mesa-pendientes" forense/firmas-pendientes.tsv` → vacío antes de escribir).

Máximo de `FP` re-derivado: `FP-98` (no `FP-95`, heredado del encargo — `ADR-136`/`PR #304` ya lo había subido). Filas nuevas: `FP-99` (`⊕`, `ABIERTA`), `FP-100` (línea `v2.11`, `ABIERTA`), `FP-101` (`ABIERTA`), `FP-102` (`FIRMADA`).

**Desviación deliberada del encargo, con evidencia:** el encargo (T3) pedía marcar `FIRMADA` tanto `mesa-pendientes.md §1` como `§2`, citando "`ADV1-M5 v2 §5`" para `§1`. Verificado leyendo `forense/escala-cinco-casillas-piloto-v2_0.md` completo: no existe un `§5` con ese contenido (la numeración real es §1-§4 más "Las tres correcciones…"/"Qué cambia…"); la sección relevante es **§4**, "Declaración B-bis — qué significa que el falsador no refute". Y esa misma §4 dice, verbatim, en su propia nota de alcance (línea 91 del archivo):

> «Nota de alcance sobre `mesa-pendientes.md` §1: este acto responde a B-bis dentro del vocabulario propio de la escala v2 (posición del intervalo, corroboración vs. falsador débil). No elige entre las cuatro lecturas candidatas de `mesa-pendientes.md` §1 sobre el origen del término «falsador» en la cabecera del encargo original — esa pregunta, sobre procedencia del término, sigue abierta a mesa y no la cierra este acto.»

Es decir: el propio documento que el encargo cita como el sello de `§1` declara explícitamente que NO cierra `§1`. Marcarla `FIRMADA` habría sido fabricar un cierre que el corpus contradice en la misma frase que se citaría como evidencia — exactamente el tipo de error que `A.8`/`A.10` piden nombrar. `FP-101` queda `ABIERTA`, con la cita exacta de por qué. `§2` sí se verificó resuelta (línea 99 del mismo archivo: «Responde también a `mesa-pendientes.md` §2 ... se adopta Opción C») y queda `FIRMADA` como `FP-102`; `mesa-pendientes.md` §2 se marca `RESUELTA` con fecha y cita del ADR. §1 y §3 no se tocan — siguen íntegras, ahora con fila propia de tablero (`FP-101`, `FP-99`).

## T4 — ADR

`ADR-137`, candidateado contra el máximo verificado por `grep -oE 'ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1` → `136`, único, sin huecos. Detalle completo en `canon/gobernanza-v1_15.md`.

## Línea base final

```
$ python3 tests/check.py --baseline
...
  19 FAIL · 142 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json
  (5 entradas de la línea base ya no aparecen — mejora, no bloquea)
────────────────────────────────────────────────────────────────────────
```
`T22`: 19 entradas, **todas `WARN`, cero `FAIL`.** Los 19 `FAIL` restantes de la suite (`T09`, `T05`, `T02`, `T06`, `T08`, `T11`) son preexistentes y ajenos a este acto — ninguno de sus perímetros se toca aquí.

## Desviación deliberada de perímetro, declarada

El perímetro del encargo no listaba `canon/estado-programa-v1_10.md`. Sellar `ADR-137` y sumar cuatro filas a `firmas-pendientes.tsv` mueve el conteo vigente de `ADR`/`FAIL`/`WARN` que ese archivo cita (`T15`/`T16` lo vigilan), y el `Cierre` del encargo exige `python3 tests/check.py --baseline` `VERDE` — no alcanzable dejando esas citas desactualizadas. Mismo patrón que `ADR-136` (`4527a45`, "Corrige CI: recifra estado-programa a ADR-135 tras sella-mesa-6") ya dejó precedentado: la sincronización mecánica de estas cifras es una consecuencia obligada de sellar un ADR, no una ampliación de alcance sustantivo. Se recifra: cabecera (`136 ADR`→`137 ADR`), `L0` (nueva entrada de cascada), y las dos líneas de conteo `FAIL`/`WARN` (`21 FAIL · 138 WARN`→`19 FAIL · 142 WARN`; `T03`/total `138`→`142`). Nada más de ese archivo se toca.

## Perímetro respetado

Tocado: `tests/check.py` (solo bloque `T22`) · `forense/firmas-pendientes.tsv` · `forense/prereg-duelo-v2/mesa-pendientes.md` (solo §2 marcada `RESUELTA`, nada borrado) · `canon/gobernanza-v1_15.md` (`ADR-137`) · `forense/hallazgos.md` · `forense/encargos/` (este archivo) · esta nota · `canon/estado-programa-v1_10.md` (solo las cifras de cascada `ADR`/`FAIL`/`WARN`, desviación declarada arriba). No tocado: `milpa/` · `data/` · `corpus/` · `T25` ni ningún otro test · `forense/escala-cinco-casillas-piloto-*` · `forense/marco-candidatas-piloto-v1_0.tsv` · `forense/prereg-duelo-v2/*.py`.

Contador: medición sobre México = 0.
