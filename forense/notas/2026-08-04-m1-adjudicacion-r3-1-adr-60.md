# ENCARGO M-1 — adjudicación de `R3.1` → `B`, sello de ADR-60, cierre de la deuda de cascada de ADR-58

**Contadores movidos: Hito D 11 → 12 de 27.** Segundo intento del mismo PR
(#106): el primer intento paró en la verificación de premisas porque los PR
de `sesion/hitoD-r3-1-encig` (#104) y `sesion/pb-descargas-f2` (#105) no
estaban fusionados — ver `forense/notas/2026-08-04-m1-adjudicacion-r3-1-paro.md`.
Mesa los fusionó; este acto re-verificó el terreno completo contra el nuevo
`main` y procedió.

ENCARGO M-1, mesa #20, redactado 4/ago/2026 contra `origin/main = 4dca34c`
(ADR máximo declarado 59). Rama `claude/adjudicar-r3-1-adr-60-4as2g0`.

## 0 · Arranque, segunda verificación (main se movió)

```
$ git fetch origin main
   4dca34c..1c09601  main -> origin/main
$ git log -1 --format="%h %s" origin/main
1c09601 Merge pull request #104 from Josanoforo/sesion/hitoD-r3-1-encig
$ git rev-list --count 4dca34c..origin/main
11
```

`main` avanzó 11 commits: PR #104 (`sesion/hitoD-r3-1-encig`, trae Nota 27)
y PR #105 (`sesion/pb-descargas-f2`) ambos fusionados —
confirmado por `list_pull_requests` (GitHub MCP): los dos `state: closed`,
con commits de merge visibles en `git log`. No es PARO: se refrescó,
re-derivó, y la diferencia se reporta aquí, como instruye §1.2 del
encargo. La rama de este acto (`claude/adjudicar-r3-1-adr-60-4as2g0`) se
sincronizó con `git merge origin/main` (no rebase, para no reescribir el
commit ya empujado del primer intento) — conflicto de una línea en
`forense/hallazgos.md` (dos líneas append-only nuevas al final,
resuelto conservando el orden de llegada real: líneas de `main` primero,
la propia después).

Resto del arranque sin cambio frente al primer intento: repo en
`/home/user/Modelado-Mexicano` (clon existente), `data/raw` ausente (no se
usa), `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (correcto en
nube, ADR-59 cláusula b), fecha local de Mesa (UTC-6) 4/ago/2026 durante
todo el acto (`TZ=America/Mexico_City date`).

### 0.1 · Concurrencia derivada (segunda vez)

```
$ git branch -r
  origin/claude/adjudicar-r3-1-adr-60-4as2g0
  origin/main
```

Los PR de origen (#104, #105) ya no aparecen como ramas remotas —
fusionados y podados (`git remote prune origin`). Ningún PR abierto nuevo
al momento de este acto salvo el propio #106 de esta rama.

## 1 · ADR máximo, receta T15 (re-derivado)

```
$ grep -hoE '^\*\*ADR-[0-9]+' canon/gobernanza-v*.md | grep -oE '[0-9]+' | sort -n -u | tail -3
58
59
60
```

Sin huecos (verificado con `awk` sobre la secuencia 01-60 completa). ADR
máximo antes de sellar = **59**, exacto contra lo declarado por mesa y por
el primer intento — `main` no trajo ningún ADR nuevo en los 11 commits
(los dos PR fusionados no tocan `canon/gobernanza-v1_15.md`). Este acto
sella **ADR-60**, derivado (último+1), no la constante escrita en el
encargo.

## 2 · Verificación de premisas (§2 del encargo)

| # | Premisa | Verificación |
|---|---|---|
| 1 | `main` reportado, ADR máximo = 59 antes de sellar | **Sostiene** — §1 arriba |
| 2 | Nota 27 de `R3.1` en `main`, con propuesta `B` | **Sostiene** — `git show origin/main:forense/hitoD-preregistro-v2_0.md \| grep "Nota 27"` da línea 998, presente. Confirmado también con la premisa de que el PR #104 la trajo. |
| 3 | `R3.1` sin veredicto archivado (antes de este acto) | **Sostiene** — `grep -c '^`R[0-9A-Za-z.]*` → veredicto'` sobre el bloque append-only, antes de escribir: **12 líneas** (11 fichas: `R4.3` cuenta doble por mitad A/B), `R3.1` ausente. Coincide con "11 fichas / 12 líneas" que mesa derivó. |
| 4 | Precedente `R3.2` = `B` archivado + tier `[FUERTE]` en `modelo §7` | **Sostiene** — `hitoD-preregistro:1019` (`R3.2` → `B`, archivado 29/jul, Nota 6); `modelo-decision-v4_0.md:675` (`R3.2 \| L233 \| ... \| [FUERTE] \| Sí`); `check.py` T12 en `[ ok ]` antes y después de este acto. |

Las cuatro premisas sostienen. Se procede a la adjudicación (§3-§6 del
encargo).

## 3 · La adjudicación — línea exacta añadida, y conteo T18

Nota derivada: **Nota 28** (última existente era Nota 27; `28 = 27+1`,
no tecleado — verificado con `grep -c "^### Nota" forense/hitoD-preregistro-v2_0.md`
antes de escribir, dio 27). Insertada **después** de Nota 27 (append-only;
el primer intento de este mismo acto insertó la nota fuera de orden —antes
de Nota 27, no después— y se corrigió en el mismo commit antes de empujar,
sin dejar el error en el historial de la rama publicada).

Línea exacta añadida al final del bloque `## Registro de veredictos
archivados` (`forense/hitoD-preregistro-v2_0.md`), forma canónica de T18:

```
`R3.1` → veredicto `B` — *(archivado 4/ago/2026, narrado en Nota 28, detalle en `hitoD-R3.1`, adjudicado por `gobernanza` ADR-60. Corrida completa (seis cómputos, brecha 9.28pp-32.73pp, sin traslape de IC95%) narrada en Nota 27.)*
```

Verificado con el regex real de T18 (`_VEREDICTO_CANONICO`) antes de
confiar en `check.py`:

```python
>>> import re
>>> re.compile(r"`(R\d+\.\d+)`\s*→\s*veredicto\s*`([A-E])`").findall(bloque)
# 13 líneas, {reales} = 12 ids distintos (R4.3 cuenta una vez)
```

**T18 antes: 11. T18 después: 12.** `estado-programa-v1_10.md:196`
("Paso 2 — EN CURSO. N de 27 corrida") actualizado de 11 a 12 en el mismo
acto — es el único sitio que T18 lee para el contador declarado.

## 4 · Dónde quedó la policía en la partición de `N_TRA` (cláusula (c).3)

**Sin abrir microdato — aritmética pura sobre las tablas ya publicadas de
`forense/hitoD-R3_1-veredicto-v1_0.md` §2.2 y §2.4, y la clasificación
congelada de `forense/hitoD-R3_1-especificacion-v1_0.md §2`.**

La especificación clasifica `N_TRA=20` ("contacto con policías — tránsito,
infracciones, detenciones") como **ALTA** discrecionalidad, con la nota
explícita "el escenario de mordida más documentado en México". La
universo declarado en §3 de la especificación es `ALTA={11,12,13,17,18,20}`
(6 códigos).

El desglose por `N_TRA` individual ejecutado (`hitoD-R3.1` §2.4) solo lista
**cinco** códigos de ALTA — 11 (n=100), 12 (n=76), 13 (n=125), 17 (n=372),
18 (n=288) — cuya suma, **961**, coincide exactamente con el `n` total de
ALTA que `hitoD-R3.1` §2.2 reporta para la interpretación (a) en los tres
regímenes de ponderador (961 en las tres filas). No queda aritméticamente
ningún renglón para `N_TRA=20`: **contribuyó cero filas** a esta corrida.

**Declarado: cae en la rama "excluida"** de las tres que el encargo exigía
distinguir — consistente con que un encuentro de calle con policía
(tránsito/detención) no se codifique como `P7_3=1` ("Instalaciones de
gobierno"), el filtro de universo que la especificación fija para
"presencial estricto" antes de llegar a la partición ALTA/BAJA. La
sospecha de que la composición policial explique la brecha de 6/6 cómputos
**se descarta** para esta corrida: el grupo ALTA que produjo la brecha no
tiene ninguna fila de contacto policial. El `B` aguanda sin ese factor.
Registrado en ADR-60(c).3, hermanado con `W1-P` (misma sospecha, instrumento
de al lado — ENCUCI en vez de ENCIG).

## 5 · Conteos por ítem derivados para la cláusula (f)

Recuento propio, fila por fila, de las 39 celdas de `forense/notas/2026-08-04-x-condicionamiento-y-forma.md §4.1`
(13 celdas por ítem: 2 Formalidad + 4 Edad + 7 Ingreso), **sin usar** el
titular de esa misma nota ("28 de 39 positivas, 12 significativas"), que
el encargo ya advertía que no reproduce:

| Ítem | Positivas | Negativas | Significativas (IC95% excluye 0) |
|---|---|---|---|
| `AP5_1_1` | 11/13 | 2/13 | 2/13 (ambas +) |
| `AP5_1_2` | 9/13 | 4/13 | 2/13 (ambas +) |
| `AP5_1_3` | 13/13 | 0/13 | 5/13 (las cinco +) |
| **Total** | **33/39** | **6/39** | **9/39, las nueve +** |

Confirmado: **33 de 39, no 28**; **9 significativas, no 12** — discrepancia
declarada en ADR-60(f), no corregida en `forense/notas/2026-08-04-x-condicionamiento-y-forma.md`
ni en `milpa/procedencia.yaml:665,685` (misma cifra "28/12" propagada ahí),
por estar fuera de perímetro de este acto — asignado a commit 3 de `W1-P`.
Este ADR usa únicamente 33/9, nunca 28/12.

## 6 · Barrido completo `de 27` / `de 49` — README.md y canon/

| Sitio | Valor viejo | Valor nuevo | Vigente / histórico |
|---|---|---|---|
| `README.md:36` | 11 de 27 (7D·1B·2A·1E) | **12 de 27 (7D·2B·2A·1E)** | Vigente — actualizado |
| `README.md:89` | 38 de 49 | **37 de 49** | Vigente — actualizado |
| `estado-programa-v1_10.md:95` | 11 de 27 (L5) | **12 de 27** | Vigente — actualizado |
| `estado-programa-v1_10.md:99` | 59 ADR (L0) | **60 ADR** | Vigente — actualizado |
| `estado-programa-v1_10.md:122` | 38 de 49 / 16 de 27 sin corrida | **37 de 49 / 15 de 27 sin corrida** | Vigente — actualizado |
| `estado-programa-v1_10.md:196` | 11 de 27 (Paso 2, T18) | **12 de 27** | Vigente — actualizado |
| `estado-programa-v1_10.md:27` | 59 ADR (tabla) | **60 ADR** | Vigente — actualizado |
| `gobernanza-v1_15.md:2` | 59 ADR (cabecera) | **60 ADR** | Vigente — actualizado |
| `gobernanza-v1_15.md:8` | "el último es ADR-59" | **"el último es ADR-60"** | Vigente — actualizado |
| `gobernanza-v1_15.md:358` | 8 de 27 (deuda de ADR-58, 3 adjudicaciones atrás) | **12 de 27** | Vigente — actualizado, deuda cerrada |
| `gobernanza-v1_15.md:647` | Nota de deuda de ADR-58(e), sin marcar | **Marcada cerrada, sin borrar** | Vigente — enmendado (append, no edición) |
| `gobernanza-v1_15.md:736` | 8 de 27 / 19 de 27 / 41 de 49 (tabla §5) | **12 de 27 / 15 de 27 / 37 de 49** | Vigente — actualizado, deuda cerrada |
| `modelo-decision-v4_0.md:64` | 11 de 27 | **12 de 27** | Vigente — actualizado |
| `modelo-decision-v4_0.md:636` | 11 de 27 | **12 de 27** | Vigente — actualizado |
| `modelo-decision-v4_0.md:637` | cita "11 de 27 de arriba" | **cita "12 de 27 de arriba"** | Vigente — actualizado |
| `modelo-decision-v4_0.md:821` | 11 de 27 corridas | **12 de 27 corridas** | Vigente — actualizado |
| `estado-programa-v1_10.md:50` | 24 de 27 (v1.8, 29/jul) | sin cambio | **Histórico** — registro fechado, no se toca |
| `estado-programa-v1_10.md:115` | 27 de 27 | sin cambio | **No aplica** — cuenta fichas, no corridas (declarado así por el propio encargo) |
| `estado-programa-v1_10.md:188` | "Ocho de 27 pre-registradas como probables D" | sin cambio | **Vigente, denominador distinto** — lista estática de fichas predichas D; `R3.1` nunca estuvo en esa lista |
| `gobernanza-v1_15.md:13` | cadena ADR-44 a ADR-58 en §0.1 | sin cambio | **Histórico** — detalle de ADR ya sellados; ADR-60 no se añade a §0.1, mismo patrón que ADR-59 (presupuesto T13) |
| `gobernanza-v1_15.md:355` | "2 de 27" | sin cambio | **Histórico** — ejemplo ilustrativo, explícito en el encargo |
| `gobernanza-v1_15.md:577,589,597,609,783,784` | 3→4, 4→8 de 27, etc. | sin cambio | **Histórico** — cuerpos sellados de ADR-55/56 y su changelog |
| `gobernanza-v1_15.md:685` | (nueva, propia de ADR-60) | — | **Vigente, ADR-37 registro congelado** — no es cifra de corridas |
| `gobernanza-v1_15.md:795` | "48 de 49" citado como error histórico | sin cambio | **Histórico** — changelog de ADR-45 |
| `modelo-decision-v4_0.md:8` | "49 filas" (Registro congelado de IDs) | sin cambio | **No aplica** — denominador de IDs, no de corridas |
| `modelo-decision-v4_0.md:21` | "2 de 27" (changelog v3.4) | sin cambio | **Histórico** — changelog, en la lista NO-TOCAR del encargo |
| `modelo-decision-v4_0.md:354` | "el perímetro de 27" | sin cambio | **No aplica** — denominador, no corridas |

## 7 · Sesión limpia

No se abrió ENCIG, ENCUCI, ningún cuestionario ni serie de microdato. No
se tocó `milpa/procedencia.yaml`, `tests/`, ni `data/`. Se leyó: el
pre-registro completo (`hitoD-preregistro-v2_0.md`), la especificación y
el veredicto de `R3.1` (`hitoD-R3_1-especificacion-v1_0.md`,
`hitoD-R3_1-veredicto-v1_0.md`), `canon/gobernanza-v1_15.md`,
`canon/modelo-decision-v4_0.md`, `canon/estado-programa-v1_10.md`,
`README.md`, `milpa/procedencia.yaml` (solo lectura, para verificar la
convergencia `R3.1`/`W1` y el estado de `radio_confianza` — nunca
escritura), y `forense/notas/2026-08-04-x-condicionamiento-y-forma.md §4.1`.
Sesión queda habilitada para pre-registrar contra cualquier fuente.

## 8 · Suite, corrida al cierre

```
$ python3 tests/check.py --baseline
       motor: 49 reglas · 20 [FUERTE] · 19[MEDIA] · 5[MEDIA-FUERTE] · 2[HIPÓTESIS] · 1[FUERTE como correlación] · 1[FUERTE / MEDIA] · 1[MEDIA / HIPÓTESIS]
  [ ok ]  T12 conteos del motor
  [ ok ]  T15 T-ADR-COUNT
  [ ok ]  T17 T-FICHAS-COUNT
  [ ok ]  T18 T-PASO2-EJECUCION
  [ ok ]  T19a/T19b/T19c
  ...
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

**T12** (conteos del motor) en `[ ok ]` — ningún tier retiquetado contra
ADR-60(b); el motor sigue en 49 reglas, 20 `[FUERTE]`. **T15**
(T-ADR-COUNT) en `[ ok ]` — 60 ADR, sin huecos, propagado a las tres citas
de cabecera. **T18** (T-PASO2-EJECUCION) en `[ ok ]` — 12 declarado =
12 real. `18 FAIL · 95 WARN` sin cambio frente al estado de `main` antes
de este acto (los 18 FAIL/95 WARN son deuda pre-existente, no introducida
aquí) — `--baseline` confirma **VERDE**, nada nuevo.

⚠️ Suite verde no prueba que la cascada esté completa por sí sola — el
barrido de §6 arriba es la verificación real, y es exhaustivo sobre
`README.md` y `canon/*.md`.

## 9 · Perímetro

Se tocó: `forense/hitoD-preregistro-v2_0.md` (solo bloque append-only +
Nota 28, sin editar Notas 1-27 ni el cuerpo), `canon/gobernanza-v1_15.md`
(ADR-60 + cascada de cabecera + cierre de deuda de §647), `canon/estado-programa-v1_10.md`,
`canon/modelo-decision-v4_0.md`, `README.md`, `forense/hallazgos.md`,
`forense/notas/`. No se tocó `milpa/procedencia.yaml`, `tests/`, `data/`,
ningún tier del motor, ni el `−0.35` de `G1·radio_confianza` (pasa de
estado nombrado, no de valor).

## 10 · PR

PR #106 (rama `claude/adjudicar-r3-1-adr-60-4as2g0`), abierto contra
`main`, actualizado con los commits de este segundo intento. **No se
fusionó.** Mesa audita y fusiona.
