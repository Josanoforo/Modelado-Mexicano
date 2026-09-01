# MAESTRA33-S2 · SELLA-2-REGLAS-ACTIVOS — cierre

Encargo: `forense/encargos/2026-09-01-MAESTRA33-S2-SELLA-2-REGLAS-ACTIVOS.md`
(dirección, maestra-33, redactado en tres mensajes el 1/sep/2026, archivado
verbatim en 0-bis A.3). Ejecutado con la skill `/acto` de `ADR-237`, entorno
**NUBE** (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`).

## ARRANQUE

Repo: clon existente, sin clonar de nuevo. `git status` limpio en todo el
acto. `origin/main` avanzó dos veces mientras se redactaba el encargo
(`b827824` → `39e832d` por `PR #443`); refrescado por `git merge origin/main`
sobre la rama del acto (sin conflictos), declarado en el commit de 0-bis A.3.
`data/raw` ausente (esperado en nube); el acto no abre microdato. Espejo del
proyecto no usado para ninguna cifra.

## COMPUERTA — cumplida por letra, no por sustancia (declarado por dirección)

El Mensaje 2 del encargo pedía «al menos un PR REGLAS-ACTIVOS-L<n>
(MAESTRA33) fusionado Y firma de mesa escrita fuera de corchetes». Verificado
mecánicamente: `PR #443` (`ACTO MAESTRA33-E18 · MAPEA-DENTRO-DE-ACTIVOS`)
fusiona `forense/encargos/2026-09-01-MAESTRA33-E18-P3-REGLAS-OLA6-ACTIVOS-L1.md`
— el único lote `REGLAS-ACTIVOS-L<n>` que existe (`L2`/`L3` declarados no
abiertos por el propio lote). La firma fuera de corchetes existía en el
propio Mensaje 2 (`AP7_1 re-etiquetar sí, P4_10 no reabrir`, referida a
`FP-217`/`C8-b`).

Dirección corrige en el Mensaje 3: el lote de `PR #443` es **spec
redactada** (`LISTO-CAJA`, ninguna `p` medida, las 3 reglas candidatas
`PENDIENTE-VERIFICACIÓN-EN-ACTO-SUCESOR`/`PENDIENTE-DE-MESA`), no un lote
**ejecutado**. La compuerta correcta pide un PR de *ejecución* (con `p`
medida, entradas `MEDIDO·p` en `milpa/tramite-ola5-propuesta-v0.yaml` que lo
citen) — inexistente hoy. **Se cumplió por letra, no por sustancia.** Este
acto registra la corrección en la cabecera del encargo archivado (A.3 no
edita el verbatim) y procede con el alcance reducido que dirección fija.

## P1 · SIN INSUMO, declarado

Cero reglas `SELLADA` para cargar al motor: el único lote existente
(`REGLAS-ACTIVOS-L1`, de `E18`) es redactado, no ejecutado — ninguna `p`
medida, dos de las tres candidatas con `PENDIENTE-VERIFICACIÓN` y la tercera
sin `variable_id` fijado (`civico.participacion.contingente`,
`PENDIENTE-DE-MESA`). `milpa/tramite.yaml` (8 reglas, verificado sin diff en
todo el acto) y `milpa/tramite-ola5-propuesta-v0.yaml` (estado, sin diff)
quedan intactos — no hay nada que cargar, descongelar ni devolver.

`S2` se relanza cuando exista: (a) un PR de EJECUCIÓN del lote
`REGLAS-ACTIVOS-L1` (o de `MIDE-PAGA-MORDIDA`) con `p` medida contra
microdato real en Ubuntu, con entradas `MEDIDO·p` citando ese PR en
`milpa/tramite-ola5-propuesta-v0.yaml`; y (b) firma de mesa por regla
(cada regla del lote firmada individualmente, no un sello por lote genérico),
escrita fuera de corchetes.

## P2 · FP-179 (cinco de seis entradas resueltas) + C8-b

`forense/firmas-pendientes.tsv`:

- **FP-179** (`ENMIENDA FECHADA`, edición quirúrgica de una sola fila,
  verificada por `git diff` que ninguna otra fila cambió): (1) `EJECUTADA`,
  (2) `EJECUTADA`, (4) `CONSUMIDA` y (5) `EJECUTADA-EN-ADR-134`/`CONFIRMA` ya
  venían resueltas de actos previos (`E3`, `E12`, `E8`, `C7`); (3)
  (mediciones diferidas de `FP-172`) queda resuelta hoy — derivaba a
  `FP-217`/`C8`, y su sucesor `C8-b` cierra con la firma de mesa verbatim del
  1/sep (`AP7_1 re-etiquetar sí, P4_10 no reabrir`), registrada en `FP-223`.
  **Cinco de seis entradas resueltas.** `FP-179` **no se cierra**: (6)
  (adquisición WVS ola 7) sigue `EN CURSO` (`ACTO MAESTRA33-A1`, receta de
  navegador pendiente) — declarado 5/6, no forzado a 6/6.
- **FP-223** (nueva, sucesora de `FP-217`/`C8-b`): `ABIERTA` → `FIRMADA`
  directamente al crearse, con la firma de mesa verbatim del 1/sep: «AP7_1
  re-etiquetar sí, P4_10 no reabrir». Se firma (i) `AP7_1` se reetiqueta en
  `data/cruce-inverso-v1_1.tsv` — es colisión de mnemónico ENCUCI/ENVIPE
  (defecto de etiqueta ya diagnosticado por `FP-217`), no variable nueva por
  medir; (ii) `P4_10` **no** se reabre — la `SUBDETERMINACION` queda
  bloqueada por `ACTO ESCALAS-COMPLETAS-P1` tal como estaba, mesa no ordena
  trabajo nuevo sobre ella hoy. Ninguna de las dos acciones se ejecuta en
  este acto (P2 registra la firma, no la reetiqueta): la reetiquetación de
  `AP7_1` en el cruce queda para el acto sucesor que toque
  `data/cruce-inverso-v1_1.tsv`, fuera de perímetro de `S2`.
- **FP-219**: **no tocada** — ya `CERRADA` por `ACTO MAESTRA33-E13 ·
  AGREGA-1` (`PR #444`), verificado por `git diff` que la fila no cambió en
  este acto.

## CONTADOR

Cero: `milpa/tramite.yaml` sin diff, `milpa/tramite-ola5-propuesta-v0.yaml`
sin diff, ningún corredor corrido, ninguna `p` medida. Declarado desde el
encargo (alcance de dirección, Mensaje 3, punto 4).

## Cascada

Ver `canon/gobernanza-v1_15.md` (entrada nueva), `canon/estado-programa-v1_10.md`
(`L0` recifrado), `canon/registro-rotulos.tsv` (fila `MAESTRA33-S2`). El ADR
declara el alcance real: **propagación de tablero; sello sin insumo** — no
carga ninguna regla al motor.
