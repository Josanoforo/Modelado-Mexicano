ENCARGO · MAESTRA33-E14 · EVALUACION-OLA6 — invoca /acto (y /mapea)
SHA de redacción: ee6a8a2. ENTORNO: NUBE. COMPUERTA: E13 fusionado (existe el agregado con L); si no, cero commits. MODELO SUGERIDO: Opus.
FIRMA DE MESA (verbatim, 1/sep/2026): «9.Si pero dejando claro cuando se abren o bajo qué criterios se abren» · (2/sep) "no vamos a esperar a esa fecha".
A.8: criterios de apertura sellados en canon/motor-nucleo-medible-v1_0.md (enmienda E11, ADR-259); FP-220 ABIERTA, vence 15/sep; candidatos: los 6 dominios no ACTIVOS — deriva la lista del propio canon, no la heredes.
P1 · Por dominio candidato, aplica los tres criterios con comando: (i) ≥2 encuestas en corpus (manifiesto), (ii) ≥3 reglas candidatas EXISTE-SATISFACE por /mapea sobre las reglas del dominio en modelo-decision-v4_0, (iii) el agregado L-M-R de E13 como contexto (no como criterio de exclusión). Tabla dominio × criterio con veredicto A.4.
P2 · Ranking y, para el primero que cumpla, el encargo REGLAS-OLA6-FASE1 redactado como PENDIENTE-DE-MESA (celdas, instrumentos, universo, lo que se congela en COMMIT-1). Si ninguno cumple: lo dice, con qué le falta a cada uno y a qué fila de adquisición se manda.
P3 · FP-220 → resuelta con este acto (fecha real, no la de vencimiento).
PERÍMETRO: notas, forense/encargos/ (borrador PENDIENTE-DE-MESA), tablero, A.3, cascada. Frase exacta vigente. CONTADOR: cero (evaluación), declarado.
LO QUE NO HACE: no abre ningún dominio; no carga reglas; no mide.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA33-E14 · EVALUACION-OLA6`, 1/sep/2026, entorno
**NUBE** (`cloud_default`), rama `claude/ola6-apertura-criterios-abnp58`,
**`PR #439`** (https://github.com/Josanoforo/Modelado-Mexicano/pull/439).
Commits: `3a397ef` (0-bis A.3, este archivo) · `d4083f7` (P1/P2/P3: tabla
dominio×criterio, ranking, `FP-220` resuelta) · `6dab037` (cascada:
`ADR-264` candidato, recifrado `L0`, `registro-rotulos.tsv`, `T25`) ·
`f19786e` (merge de `origin/main`, `PR #438`/`ACTO MAESTRA33-E17` fusionó
primero y tomó `ADR-264` — renumerado a **`ADR-265`**, contiguo, sin
hueco; conflicto solo en las tres tablas de cascada, resuelto conservando
ambas inserciones en orden de fusión).

`COMPUERTA: E13 fusionado (existe el agregado con L)` — **CUMPLE** por
existencia del documento (`PR #403`, verificado por
`git log --oneline origin/main | grep -i E13`), con la ambigüedad
declarada de que `forense/prereg-duelo-v2/scoreboard-v1_1.md` existe pero
trae `L pendiente: 11 celdas` (cero puntos de `L`) — esa misma ambigüedad
reaparece en el veredicto de P2, no se usó para parar sin evidencia.

Universo de 6 dominios candidatos (salud, tiempo, cooperación, trabajo,
información, comunicación) derivado por comando de
`canon/motor-nucleo-medible-v1_0.md` §1. **Ningún dominio cumple**: cero
de seis alcanza (ii) ≥3 reglas `EXISTE-SATISFACE` por `/mapea` (nunca
corrido contra estos dominios, verificado por
`grep -rn "EXISTE-SATISFACE"`); además el criterio 1 de §3.a (agregado
con `L`) sigue en `L pendiente: 11 celdas de 11` — "lógicamente
imposible" per el propio texto sellado del canon hasta que exista al
menos un punto de `L`. No se redacta `REGLAS-OLA6-FASE1`: se declara qué
falta por dominio (mapeo dirigido en los cuatro mejor posicionados,
segunda encuesta verificada en comunicación, única fila real de
adquisición en tiempo) y a qué fila se enruta, sin abrir fila nueva en
`data/cola-adquisicion-v1_0.tsv` (fuera de perímetro).

`FP-220` (`forense/firmas-pendientes.tsv`): `ABIERTA` → `EJECUTADA`,
`ejecutada_en` = este acto, fecha real **2026-09-01** (no la de
vencimiento, 2026-09-15), por firma de mesa (2/sep, verbatim) "no vamos
a esperar a esa fecha" — edición quirúrgica de una sola fila, verificada
por `git diff` que ninguna otra cambió.

CONTADOR: cero (evaluación) — ningún dominio abierto (`milpa/tramite.yaml`
sin diff), ninguna regla cargada, ninguna medición corrida, `/mapea` no
invocado contra los 6 candidatos. Declarado desde el encargo.
`python3 tests/check.py --baseline`: **VERDE**, `19 FAIL · 166 WARN`, sin
entrada nueva frente a `tests/baseline.json` (dos hallazgos nuevos del
propio cierre — `T15` cita histórica sin marcar en la entrada de
`ADR-263`, `T25` rótulo pelado `E13` en el encargo y la nota de cierre —
ambos corregidos en el camino, declarados). Detalle completo:
`forense/notas/2026-09-01-evaluacion-ola6-cierre.md`. PR abierto contra
`main`, **no fusionado por este acto** — el merge es de mesa.
