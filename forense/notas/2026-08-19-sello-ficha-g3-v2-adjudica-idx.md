# Nota del acto · ACTO SELLO-FICHA-G3-V2 — el gate abre, el diseño se sella, la ejecución ya corrida se adjudica

**Fecha:** 19/ago/2026 · **Rama:** `claude/sello-ficha-g3-v2-coeficiente-pnojt6` · **ADR:** `ADR-107` · **Encargo:** `forense/encargos/2026-08-19-SELLO-FICHA-G3-V2.md`

Esta rama corrió el mismo encargo dos veces. La primera corrida (18/ago, commit `04ddf2e`) verificó el gate contra el árbol de ese momento, lo encontró **no cumplido** (`FP-15 ABIERTA`, `milpa/src/` ausente, Entrada 5 `ABIERTA`, `LANE-A-E0-E5` `VIVO`) y repitió exactamente la conducta del acta precedente (#262): PARA, una línea fechada añadida a `forense/notas/2026-08-18-sello-ficha-g3-gate-e0e5-no-cumplido.md`, nada más tocado. El usuario retomó la sesión ("retoma") después de que `LANE-A-E0-E5` fusionara (`PR #266`). Esta nota documenta la segunda corrida, la que sí ejecuta.

---

## 0 · ARRANQUE

1. **REPO.** `git fetch origin main` → `cb0d98f` (merge de `PR #266`). `git merge origin/main` sobre la rama de trabajo, limpio (`ort`, sin conflicto), 38 archivos, `milpa/src/` aterriza. `git merge-base --is-ancestor origin/main HEAD` → confirmado.
2. **SHA.** Encargo declara `57984b5`; re-derivado contra `cb0d98f` — avance limpio, `57984b5` es su ancestro (verificado con `git log origin/main --oneline`).
3. **`data/raw`.** Ausente (`test -d data/raw` → no existe). No se usó microdato en este acto — la lectura de `procedencia.yaml`/notas ya archivadas es lectura de repo, no apertura de corpus.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`.
5. **ESPEJO.** Ninguno usado.

## 1 · Gate — re-verificado, esta vez cumplido

Las cuatro señales del encargo, contra el árbol tras el merge de `origin/main`:

| señal | acta precedente (18/ago) | esta corrida (19/ago) |
|---|---|---|
| `FP-15` (`firmas-pendientes.tsv:16`) | `ABIERTA` | **`CERRADA`** |
| `milpa/src/` | ausente | **existe** (9 módulos: `celdas.py`, `clases.py`, `matriz.py`, `momentos.py`, `motor.py`, `pi.py`, `procedencia.py`, `salida.py`, `theta.py`) |
| Entrada 5 (`registro-recalculo-v1_0.md:41`) | `ABIERTA` | **`RECALCULADO — SIN CAMBIO`** (`ACTO LANE-A-E0-E5`) |
| `forense/encargos/2026-08-18-LANE-A-E0-E5.md` | `Estado: VIVO` | **`Estado: CONSUMIDO`**, este PR citado |

Las cuatro coinciden: el gate abrió. Se procede.

## 2 · C1 — el prompt fiel, y lo que encontró después de la primera respuesta

**Primera pregunta (`AskUserQuestion`), texto verbatim de la cabecera:**

> Gate abierto (FP-15 CERRADA, milpa/src/ existe, Entrada 5 con veredicto, LANE-A-E0-E5 CONSUMIDO). Antes de sellar `ficha-id-g3` (FP-11) — el diseño de identificación intra-persona de G3 sobre horizonte_temporal, vía panel MxFLS olas 2-3, exposición AFORE — tres puntos que mesa debe leer:
>
> (1) QUÉ ESTIMA: promueve `CAL-G3` (descriptivo) a intento de identificación bajo llave (i) de ADR-57(c) — panel con desenlace en el instrumento. Criterio en razón (RR), no en puntos porcentuales.
> (2) CONTAMINACIÓN CONFESADA (Paso 0): quien diseñó esto ya vio el resultado de Fase C — declarado y acotado, no evitado. El diseño del Paso 2 se hizo exclusivamente sobre lo que queda fuera de esa superficie.
> (3) VENTANA: hereda D-10, panel 2005-2012 — no extrapolable fuera de esa ventana.
>
> Y el hallazgo que la verificación independiente (2026-08-05, §2(3)) deja sin resolver: el margen del chequeo de alcanzabilidad de ID-C es de solo 0.013 sobre el umbral 1.25 (~1%), con un solo escenario (el más generoso posible), no el barrido completo que el precedente CRH sí corrió. No bloquea el sello por construcción, pero cualquiera que retome esto debe resolverlo antes de confiar en ID-C como desenlace practicable.
>
> Además: los 3 payloads MxFLS (ennvih2_2005_hogar_cb, ennvih3_2009_hogar_cb, ennvih3_2009_hogar_q) están AUSENTES en este entorno de nube — EXEC-FICHA-G3 nacería gateado a adquisición de corpus, no ejecutable hoy.
>
> ¿Qué decide mesa? — opciones: **(a) Sello tal cual** / (b) Sello con corrección / (c) No se sella.

**Respuesta de mesa, verbatim:** *"(a) Sello tal cual"*.

**Lo que se encontró después de recibir esa respuesta, antes de escribir el ADR.** Al construir C2/C3, se leyó `milpa/procedencia.yaml:1005-1041` para localizar dónde entraría la futura estampa `A.10` — y ahí ya existe una entrada completa, `coeficientes_generador_medidos.G3_horizonte_temporal`, clase `GATE·ID-X`, escrita el 5/ago/2026 (commit `9154072`, `PR #209`) por `ENCARGO CORRIDA-IDG3`. Esa corrida abrió microdato real (`data/raw/ennvih/*.zip`, `pandas.read_stata`), construyó la muestra analítica completa (jefatura exacta contra manual de codificación, enlace de panel vía `pid_link`, `TB33` determinado, `ah03h` no faltante) y recalculó el gate `ID-X` con n reales: **primaria (jefe, n_util=762) `IC95%sup=1.483`; sensibilidad (algún miembro, n_util=1,562) `IC95%sup=1.372`** — ninguna alcanza `<1.25`. Se declaró explícitamente *"no adjudica su propia fila — la propone; mesa adjudica"* y *"0 de 15 sigue en 0 de 15"*. Catorce días después, esa adjudicación seguía sin darse.

Esto significa que el `C1` original — fiel al texto del encargo — no le dio a mesa la información completa: preguntó sobre un diseño a punto de ejecutarse cuando la ejecución ya había corrido dos semanas antes. La primera respuesta de mesa ("(a) sello tal cual") sigue siendo válida sobre el diseño, pero no resuelve qué hacer con `C3` (`EXEC-FICHA-G3`), porque escribirlo como "corre y reporta" sería relanzar un procedimiento ya hecho. Se volvió a mesa con una segunda pregunta, antes de escribir ningún ADR.

**Segunda pregunta (`AskUserQuestion`), texto verbatim:**

> CORRIDA-IDG3 (5/ago) ya ejecutó la identificación con microdato real y propuso fila ID-X (compuerta inalcanzable, IC95%sup 1.483/1.372, ambas por encima de 1.25) — sin adjudicar, sin mover 0 de 15. Esto cambia qué debe ser C3 (EXEC-FICHA-G3): ¿escribirlo como una NUEVA corrida (redundante con lo ya hecho), o como el acto que ADJUDICA la fila ID-X ya propuesta, cerrando el ciclo que quedó abierto desde agosto? — opciones: **(a) C2 sella diseño + adjudica ID-X ahora (recomendado)** / (b) EXEC-FICHA-G3 como re-verificación independiente / (c) Detener y llevar el hallazgo a mesa sin proponer texto.

**Respuesta de mesa, verbatim:** *"C2 sella diseño + adjudica ID-X ahora (recomendado)"*.

Las dos firmas de mesa entran verbatim a `firmas-pendientes.tsv:12`, columna `firmada_en`, y sostienen `ADR-107`.

## 3 · C2 — el sello (ejecutado con la corrección declarada en el encargo archivado)

`ADR-107` (`canon/gobernanza-v1_15.md`) hace dos cosas en un acto, autorizadas por las dos respuestas de mesa:

1. **Sella el diseño.** `ficha-id-g3-v1_0.md` pasa de `PROPUESTA DE SELLO COMPLETA` a `SELLADA`, sin enmienda de texto — mesa eligió (a), no (b). Solo se tocó el bloque de estado del archivo, per perímetro.
2. **Adjudica `ID-X`.** No se declara "la ejecución es acto propio... `0 de 15` se mueve allí, no aquí" (texto literal de C2, escrito bajo la premisa de que la ejecución era futura) — se declara que la ejecución **ya ocurrió** (`CORRIDA-IDG3`) y se adjudica aquí: compuerta inalcanzable, ningún coeficiente producido, `0 de 15` no se mueve **en ningún acto**, ni aquí ni en uno futuro — la ruta queda cerrada salvo que mesa reabra con un panel nuevo.

`milpa/procedencia.yaml` no se tocó: la entrada `GATE·ID-X` que `CORRIDA-IDG3` escribió el 5/ago ya es correcta y completa; este ADR la adjudica por referencia, no por edición. Estampa `A.10`: acotada 2005-2012 (ventana del panel ENNViH/MxFLS olas 2-3, `D-10`), declarada explícitamente no extrapolable.

`FP-11` → `FIRMADA` (de `FIRMADA-CONDICIONAL`). `firmada_en` lleva las dos respuestas verbatim de mesa. `ejecutada_en` — que C2, literalmente, decía que quedaría vacío — se pobló citando `CORRIDA-IDG3` y `ADR-107`, porque dejarlo vacío habría sido falso: la ejecución ya existe en el árbol.

## 4 · C3 — por qué no se escribió `EXEC-FICHA-G3`

El encargo pedía "EXEC-FICHA-G3, escrito VIVO (no lanzado)... COMMIT B corre y reporta en RR con IC". No se escribió. Razón, verificada dos veces:

- **Ya corrió.** `CORRIDA-IDG3` es exactamente ese COMMIT B — corrió con microdato real, reportó en RR con IC, y su IC no despejó (`IC que no despeja = propuesta con reserva, no adjudicación`, texto literal de C3) — es precisamente lo que pasó: propuso `ID-X` con reserva, sin adjudicar. Escribir un nuevo encargo para repetir ese procedimiento no agrega nada — `tests/idg3_corrida.py` ya es reproducible y ya se reprodujo (`tests/idx_g3.py` sin modificar, `IC95%sup=1.237` idéntico al sellado).
- **No sería ejecutable aquí de todas formas.** Verificado hoy: `python3 tests/manifiesto.py --verifica --id ennvih2_2005_hogar_cb` / `ennvih3_2009_hogar_cb` / `ennvih3_2009_hogar_q` — las tres `AUSENTE`, mismo resultado que `S-IDG3` reportó el 5/ago para este mismo tipo de entorno de nube. Un `EXEC-FICHA-G3` escrito hoy nacería gateado a adquisición, exactamente como el encargo anticipaba que podía pasar ("si faltan, EXEC nace gateado a adquisición y LO DICES") — y lo dice: no hay EXEC porque no hace falta relanzar algo que ya corrió con microdato real en un entorno que sí lo tenía montado.

## 5 · C4 — cierre

- **ADR ×2:** el encargo pedía dos ADR (uno para C2, uno para el cierre del gate/re-verificación si aplica). Este acto solo produjo `ADR-107` — el gate ya estaba cerrado por `LANE-A-E0-E5` (`ADR` propio de ese acto, no de este), y la adjudicación de `ID-X` se hizo en el mismo ADR que sella el diseño, no en uno separado, porque son la misma decisión de mesa tomada en el mismo acto (dos preguntas, un ADR). Declarado como desviación, no oculto.
- **Cascada:** `canon/estado-programa-v1_10.md:27,101` (106→107 ADR) y la cláusula propia `- a 107 después...` donde `ESTADO-SPLIT` dejó la lista (una por línea).
- **Nota:** este documento.
- **`hallazgos.md`:** entrada añadida, ver abajo.
- **`CONSUMIDO`:** `forense/encargos/2026-08-19-SELLO-FICHA-G3-V2.md`, archivado y marcado consumido en el mismo acto que lo ejecuta (A.3 permite esto cuando el encargo llega por conversación).

**Auditoría sobre México: cero en este acto.** El movimiento real — la ejecución que sí abrió microdato y sí produjo una cifra sobre la relación exposición-desenlace, o en este caso, sobre la compuerta que la impide — vivió en `CORRIDA-IDG3`, el 5 de agosto, no aquí. Este acto adjudica, no mide.

**Contra la simplificación que el propio encargo advierte.** "El primer coeficiente" no es lo que pasó. Pasó lo contrario: la primera ruta de identificación con llave sellada de los 15 coeficientes del generador se probó con microdato real y **no alcanzó** — la compuerta se cerró, no se abrió. `0 de 15` sigue en `0 de 15`, y esta adjudicación es la razón formal, con mesa firmando, de por qué esa ruta concreta (ENNViH/MxFLS, llave (i), panel 2005-2012) no va a producir ese primer coeficiente. Un parámetro, acotado, de 15 — y este acto declara que, por esta vía, no se alcanza.

## 6 · Perímetro y lo que no se hizo

Tocado: `canon/gobernanza-v1_15.md` (`ADR-107`, cabecera), `forense/ficha-id-g3-v1_0.md` (solo bloque de estado), `forense/firmas-pendientes.tsv` (`FP-11`), `canon/estado-programa-v1_10.md` (solo cascada de conteo), este archivo, `forense/hallazgos.md`, `forense/encargos/2026-08-19-SELLO-FICHA-G3-V2.md` (nuevo, archivado y `CONSUMIDO` en el mismo acto), `forense/notas/2026-08-18-sello-ficha-g3-gate-e0e5-no-cumplido.md` (una línea, corrida anterior de esta misma rama).

No tocado: `canon/modelo-decision-v4_0.md`, `hitoD-preregistro-v2_0.md`, `milpa/procedencia.yaml` (la entrada de `CORRIDA-IDG3` queda intacta), `milpa/src/**`, `tests/`. No se abrió microdato en este acto — los tres payloads MxFLS verificados `AUSENTE`, arriba. No se corrió `--freeze`.

## 7 · Marcador T22 — falso positivo, explicado (A.12)

`tests/check.py` (T22, protección (b)) marca este archivo por `_T22_MARCADOR_PENDIENTE` (`PROPUESTA.*mesa`), en §3: la frase cita el estado viejo de la ficha ("`PROPUESTA DE SELLO COMPLETA` a `SELLADA`, sin enmienda de texto — mesa eligió...") — dos términos sin relación citados uno junto al otro, mismo patrón que el acto precedente (#262, §6) ya documentó para el mismo género de coincidencia. No es una ranura nueva sin registrar: `FP-11` ya tiene su fila, pasa a `FIRMADA` en este mismo acto (§3 arriba), y no queda ninguna decisión pendiente sin resolver que este archivo esconda. Excluido vía `_T22_ARCHIVOS_CONOCIDOS` en `tests/check.py`.
