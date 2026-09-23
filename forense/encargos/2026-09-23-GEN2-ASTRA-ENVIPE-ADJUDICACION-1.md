# ENCARGO · ACTO GEN2-ASTRA-ENVIPE-ADJUDICACION-1 · Las cuatro emisiones ENVIPE 2025 de Astra (#1031) puntuadas contra la R que el piloto 4 ya selló, con el mismo umbral, rotuladas por orden de sello y sin adopción

> ENTORNO: **NUBE** — solo RESULT sellados (la R del piloto 4 y las emisiones de Astra); cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `f28d1038` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-astra-envipe-adjudicacion-1` (D-17) · MODELO: Opus (mide) · MODO: RÍGIDO en el procedimiento del piloto 4 (se hereda verbatim); ABIERTO en logística · ids con raíz de acto (D-24) · perímetro de cierre permanente (D-21) aplica sin enumerarlo · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: sella hasta cuatro corridas (una por cruce) con `cuenta_gen2: SI`, `adopta: NO`; no toca la adjudicación del piloto 4; `celdas_validadas` no cambia (las cuatro celdas-D ya cuentan por el piloto).

## 1 · OBJETIVO
Que exista, sellada, la comparación de C-ASTRA (los cuatro `CALC-ASTRA-ENVIPE-*-0001` de #1031) contra el piso C2 en los cuatro cruces del piloto 4, con la comparación primaria del piloto (diferencia de error medio con IC por réplica de R, umbral del piloto) y el dictamen con el vocabulario cerrado de B-bis. Es la primera medición de si un retador externo vence al piso. Habilita: la adopción de C-ASTRA por firma si vence, y la retroalimentación a ASTRA-1.
«Hecho» sobre el commit final: `ls -d data/corrida0/CALC-ASTRA-ENVIPE-ADJUDICACION-*` = 4 (o menos con NC por cruce NO-CONSTRUIBLE) · cada uno con `sello.json`, asiento en `replay-evidencia.tsv`, `verify` = REPRODUCE · nota con tabla cruce × ΔMAE(IC) × dictamen · marcador `PROSPECTIVA-POR-ORDEN-DE-SELLO` en cada RESULT, con los dos sellos citados (emisión de Astra, R del piloto) y su diff.

## 2 · FIRMAS DE MESA (23/sep/2026, verbatim del chat de dirección; entran al repo por GEN2-TRAMITE-FIRMAS-11 — este encargo las cita, no las asienta)
- **D1** «Integrar los dos, nada es fuera de plazo, todo se utiliza.» (#1030 y #1031 se fusionan; las cuatro emisiones ENVIPE de Astra se adjudican contra la R del piloto 4.)
- **D3** «Que cuenten.» (las adjudicaciones de crédito entran a celdas_validadas vía celda-D)
- **D4** «A, desde ya.» (main exige check.py VERDE; merge queue; el token de Actions fusiona solo PR de rutina: `claude/encola-*`, `acto/gen2-tramite-*`, `[deriva]`; lo que mide lo fusiona mesa)
- **D5** «Ya tengo un disco duro, necesito reformatearlo para dejarlo listo, no ahora, esta semana sí; vence el domingo de esta semana.» (27/sep/2026)
- **D6** «A.» (la vía (i) de relevo lee el eje RESULTADO; CONTEXTO en la nota del pin)
- **D7** «A.» (acto de MOTOR autorizado a editar `milpa/src/motor.py` en las líneas de NC …e8fa-01; los sellos afectados se suceden por CALC nuevos)
- **D8** «A, pero que se explique claramente qué significa.» (INDETERMINADO es valor válido; se define por escrito)
- **D2** no es firma: es una pregunta de mesa («¿por qué seguimos haciendo piloto del piloto?») que contesta el encargo DUELO-ENCIG2025-CIERRE-1 con su firma §2 propuesta.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` #1031 (`codex/astra-interaccion-dinamica-1`, 11 commits) NO está en main al redactar; D1 ordena fusionarlo. El piloto 4 (`acto/gen2-celda-d-piloto-4-encogida-1`, 10 commits, dictamen `FALSADOR DÉBIL` en 4 cruces, nota `…PILOTO-4-ENCOGIDA-1-cierre.md:40-45`) tampoco. **Compuerta: este acto arranca cuando los dos estén en origin/main**; si al abrir falta alguno, PARO (§7 f) y es el entregable.
- `[EJECUTADO]` Orden de sellos: emisiones de Astra selladas 22/sep 20:15 (último commit de la rama antes del recibo); R del piloto sellada en COMMIT-3 `de93beef` 22/sep 20:58. `[EJECUTADO]` `ejecucion.json` de Astra: inputs `envipe2023_csv`, `envipe2024_csv`, `MARGINALES-PUBLICOS`; ningún id 2025. El recibo (#1033) verificó (b) por historial para ENCIG; **para ENVIPE lo verificas tú de nuevo** (`git log -p -S <sha de la R>` sobre la rama de Astra: cero apariciones antes de `de93beef`). Si algún input de Astra resulta ser tabulado de ENVIPE 2025, el rótulo baja a RETROSPECTIVA y se dice; no es PARO.
- `[LEÍDO]` Cruces del piloto 4 (nota de cierre, tabla l.40-45): dominio×sexo (6 celdas), edad×escolaridad-proxy (16), edad×sexo (8), escolaridad-proxy×sexo (8). Astra emitió DOMINIOXSEXO, EDADXESCOLARIDADPROXY, EDADXSEXO, ESCOLARIDADPROXYXSEXO. `[SUPUESTO]` que las definiciones de eje coinciden celda a celda (el recibo lo dio por compatible en «Document pilot 4 cell compatibility», commit de Astra): **es la premisa que verificas primero**; una celda que no empata es NO-PUNTUADA, no se fuerza.
- `[LEÍDO]` Procedimiento del piloto: `forense/prereg-caja/TRA-evade-norma-cruces-encogida-spec-v1_0.md` (rama) + su `spec.yaml` + medidor congelado en `5939e9d4`. Se hereda verbatim: mismo ΔMAE, mismas réplicas de R del árbitro, mismo umbral primario. Ningún parámetro nuevo.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -c ASTRA-ENVIPE-ADJUDICACION` → 0. El piloto 4 no puntuó a C-ASTRA (ADENDA-1: ventana cerrada; el recibo lo confirmó). Nadie más lo ha hecho (`git grep -l 'CALC-ASTRA-ENVIPE' origin/main -- forense/notas` → reporta).

## 5 · PIEZAS
- **P0 · Spec en dos capas antes de tocar RESULT.** `forense/prereg-caja/ASTRA-ENVIPE-ADJUDICACION-spec-v1_0.md` + `spec.yaml`: hereda el procedimiento del piloto por sha; lista de candidatos = {C2 piso, C-ASTRA}; C-ENCOGIDA y C7 no entran (ya adjudicados). Declara antes de abrir: el empate de celdas por texto, qué pasa si un cruce no empata, y el vocabulario B-bis (VENCE · PROPUESTA-CON-RESERVA · NADIE-VENCE · FALSADOR-DÉBIL, el mismo del piloto). COMMIT-1 congela spec + medidor (D-22: preflight VERDE, sintético, ids nulos declarados, ningún hash sobre archivo vivo).
- **P1 · Cuatro corridas.** Inputs por hash: RESULT de R del piloto (`CALC-TRA-EVADE-NORMA-*` COMMIT-3), RESULT de C2 del piloto, RESULT de cada `CALC-ASTRA-ENVIPE-*`. Salida por cruce: ΔMAE con IC95 de las mismas réplicas, celdas puntuadas/no puntuadas, dictamen. COMMIT-2 trae resultados y no edita COMMIT-1.
- **P2 · Nota y consecuencias.** Tabla; una línea de producto: «C-ASTRA {vence | no vence} al piso en {k}/4 cruces de ENVIPE 2025; comparación PROSPECTIVA-POR-ORDEN-DE-SELLO, secundaria al piloto 4». Si VENCE en algún cruce con IC que despeje: fila FP para mesa (adopción de C-ASTRA en esas celdas, con el nombre de Astra en el ADR); si no, NC de retroalimentación para ASTRA-1 con la tabla. Asiento en `replay-evidencia.tsv` por corrida. Anexo en la celda-D de cada cruce: `comparaciones_secundarias:` con el CALC por id — no se toca `champion_actual`.

## 6 · LATITUD
Logística libre. Pregunta a mesa (con opciones, sigues): si el empate de celdas exige una función de enlace entre la escolaridad-proxy de Astra y la del piloto (§4: no se compara entre escalas sin enlace). NO DECIDES: nada del procedimiento heredado.

## 7 · PAROS — lista cerrada
a) abrir microdato de ENVIPE 2025/2026 (este acto no tiene código autorizado) · b) reescribir o re-sellar cualquier CALC del piloto o de Astra · c) mover `champion_actual`, adoptar · d) cambiar el procedimiento heredado (umbral, réplicas, agregador) · e) CAJA · f) #1031 o el piloto 4 no están en origin/main al abrir.

## 8 · COMPUERTAS
«COMMIT-1 antes de leer cualquier RESULT de R» protege: **abrir dato**. «Procedimiento heredado por sha, no copiado a mano» protege: **congelar spec**. «`champion_actual` no se toca; FP si vence» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/ASTRA-ENVIPE-ADJUDICACION-*`, `data/corrida0/CALC-ASTRA-ENVIPE-ADJUDICACION-*`, medidor en `tools/astra/envipe/adjudicacion.py` (nuevo), `replay-evidencia.tsv` (append), los cuatro yaml de celda-D del piloto (solo bloque `comparaciones_secundarias`, append), `firmas-pendientes.tsv`/`no-corrido.tsv` (append), nota, L0, cascada. Ajeno: todo lo demás del piloto y de Astra.
En vuelo: FIRMAS-11, DIN-CREDITO-CELDAS-D-1, AUTOMERGE-2 (nube, misma tanda; union en TSV). `codex/astra3-*` no tocan estos archivos.

## 10 · LO QUE NO HACE · SUCESORES
No adopta, no reabre el piloto, no puntúa ENCIG (eso es DUELO-ENCIG2025-CIERRE-1). Sucesores: firma de adopción si vence; NC a ASTRA-1 si no. Auditoría de rigor extremo: sí aplica a la nota (afirma sobre México): PROSPECTIVA/RETROSPECTIVA en cada frase, unidad persona, escala pp.

## NO-CORRIDO / RESERVAS

- **P0/P1/P2 (spec en dos capas, cuatro corridas, nota) — el encargo entero.** `PARO-ENTORNO`. Compuerta verificada primero (`#1031`/`ec0a8c7` y piloto 4/`#1036`/`73b7f11` los dos en `origin/main`), premisas de §3 verificadas por comando (input_ids de los cuatro `CALC-ASTRA-ENVIPE-*` sin ningún id de 2025; `git log -p -S<sha256 del sello de R>` sobre la rama de Astra → 0 apariciones; empate de celdas por texto ya documentado en `forense/analisis/astra-envipe/admisibilidad.tsv` por la propia rama de Astra, commit `159dc87`). El PARO aparece al verificar que el procedimiento heredado (RÍGIDO desde COMMIT-1, sin parámetro nuevo) propaga la incertidumbre de ΔMAE con réplicas bootstrap de `R` sobre `envipe2025_csv` (`tools/celda_d/marginales_reproduccion.py::replicas_compartidas`, usado en `CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001/adjudicacion.py:217-247`). El CALC sellado del árbitro no guarda esas réplicas crudas (`python3 -c "..."` sobre `resultados.json`: 685 entradas, 0 de tipo lista) — solo escalares de IC ya cerrados para los cuatro candidatos originales (C1/C2/C7/C-ENCOGIDA). C-ASTRA es un quinto candidato sin IC de ΔMAE sellado en ningún lado: reproducir el método exige reabrir `envipe2025_csv` — exactamente el PARO (a) de este mismo encargo ("este acto no tiene código autorizado"). Sustituir el método por uno sin bootstrap conjunto violaría el PARO (d) ("cambiar el procedimiento heredado") y la LATITUD explícita ("NO DECIDES: nada del procedimiento heredado"). Detalle completo con comandos: `forense/notas/2026-09-23-GEN2-ASTRA-ENVIPE-ADJUDICACION-1-cierre.md`. Impacto: cero adjudicación secundaria de C-ASTRA registrada; `celdas_validadas` sin cambio; la comparación primaria con IC que el OBJETIVO pide no se puede emitir en este entorno. Sucesor: `DIFERIDO-A` un acto en CAJA que reabra `envipe2025_csv` únicamente para materializar/re-sellar las réplicas de `R` por celda que el método heredado necesita (sin re-estimar nada del piloto 4), o `DECISION-DE-MESA-PENDIENTE` si mesa prefiere autorizar un método de IC más simple (no bootstrap-conjunto) para este quinto candidato. Fila `NC-260923-GEN2-ASTRA-ENVIPE-ADJUDICACION-1-970c-01`.
