ENCARGO · ACTO MAESTRA34-L4 · CIVICA-Y-CORPUS — invoca /acto (y /adquiere)
SHA de redacción: a39073d (merge PR #458 / ADR-280). Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR — firmas F231-a y F232 dentro. 0-bis A.3: archiva este texto verbatim en forense/encargos/ antes de ejecutar.

ENTORNO ASIGNADO: UBUNTU (caja: corpus, red a OPLE/INE por sonda A.2). NO se lanza en NUBE. MODELO SUGERIDO: Opus (P3 es medidor de dos commits). Un solo acto de caja a la vez.
CARRILES: MAESTRA34-N4 y MAESTRA34-N7 corren en nube (prereg-duelo-v2, milpa, skills, runbooks); perímetros disjuntos salvo cascada; renumera quien fusiona segundo.
COMPUERTA: ninguna.

FIRMAS DE MESA — verbatim, 1/sep/2026: «F231-a, F232-b y a como lo mencionas.» El ejecutor propaga, no decide (SELLA-3).
- F231-a: la entrada `endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf` de data/manifiesto.yaml (declara 2 895 872 B, sha 784410e6…; en disco 102 349 631 B, sha a990a007…) se RE-DERIVA desde el archivo en disco con `tests/manifiesto.py --registra` bajo id nuevo; la vieja se retira con nota que cite FP-231 y ADR-280. No se re-descarga.
- F232-b (principal): contraste ENTRE AÑOS — elección local 2023 (no concurrente) vs local 2024 (concurrente con la federal), mismo estado y mismo municipio, Coahuila y Estado de México. F232-a (robustez, solo si existe): dentro de 2024, municipios/distritos con y sin comicio local concurrente el mismo día, mismo estado. La spec de L1-spec.md l.502-508 y la firma DS-a quedan reconciliadas así; se anota en FP-232.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra a39073d ═══
(1) ESTRUCTURA: Dominio 1 (manifiesto por script); registro del curador en tres capas por la vía que MAESTRA34-N6 documentó en tools/curador_registro/GUIA-CURADOR-REGISTRO.md §alta; Dominio 4 para la estimación (spec → dos commits); codificacion-R-v1_0.tsv NO aplica (esto no es celda del marco): la dicotomización se congela en la nota de spec de P3.
(2) CONTENIDO (todo de MAESTRA34-L3, cierre §3-§4, PR #458):
  - Crosswalk sección→municipio, vintage 2016: EXISTE-SATISFACE en corpus (deriva id: `grep -i "crosswalk\|seccion" data/manifiesto.yaml`); cubre todos los municipios de Coahuila y Edomex.
  - PREP 2024 federal por casilla con LISTA_NOMINAL y SECCION: EXISTE (id `ine_prep2024_base_datos_20240603_2005_zip`), sin municipio (lo da el crosswalk).
  - Local 2023 Coahuila y Edomex: NO-ENCONTRADO en corpus (el corpus llega a 2018 en ambas: zenodo_electoral_precinct_level_mexico_municipal.zip). Local 2024 municipal/distrital de ambas: NO-ENCONTRADO. Cómputos INE 2024: bloquean la IP de mesa; SICEE es SPA (receta en MAESTRA34-L1 cierre l.183-198).
  - ENDIREH 2016: no_coincide=1 por `tests/manifiesto.py --verifica` (FP-231), preexistente.
  - Variación intra-2024 (F232-a): DESCONOCIDA — P1 la verifica antes de comprar nada para ella.
(3) COBERTURA RETROACTIVA: no aplica.

PIEZAS
P1 · ADQUIERE LAS DOS MITADES. `/adquiere`, ≥4 rutas por objeto con salida cruda, A.5 (fallo del agente ≠ fuente inexistente), receta ≤1 min por fallo: (i) Coahuila local 2023 por municipio (gubernatura y/o ayuntamientos/diputaciones — lo que exista) desde el OPLE del estado; (ii) Edomex local 2023 por municipio, ídem; (iii) local 2024 de ambas por municipio (ayuntamientos) desde su OPLE; (iv) como respaldo de (iii), catálogo de casillas/secciones 2024 con lista nominal. Registro por las tres capas (payload → cola del registro → relación con la necesidad cívica y R7.1). Al final de P1, verifica F232-a: ¿hubo en 2024 municipios de Coahuila o Edomex SIN comicio local el 2/jun? Reporta con comando y fuente; si no hay variación, F232-a se declara NO-APLICA y no se compra nada más.
P2 · ENDIREH 2016 (F231-a). Una invocación `--verifica --id endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf` (A.1, salida cruda); `--registra` sobre el archivo en disco con id nuevo (`endireh_2016_bd_mujeres_v2` o el que el script derive), `usado_para` heredado, `nota` citando FP-231/ADR-280 y los dos pares (sha, bytes); la entrada vieja se retira; `--verifica` de nuevo → coincide. Abre `.dbf` y reporta tablas/filas (A.13) para que la adjudicación quede medida, no supuesta. FP-231 → EJECUTADA. Corolario en hallazgos.md: «`--verifica` no está en la suite; un no_coincide solo se ve si alguien lo corre» (queda para E1/mesa; este acto no instrumenta).
P3 · MEDICIÓN CÍVICA CONCURRENTE (F232-b; F232-a si P1 lo habilitó). COMMIT-1, antes de abrir ningún resultado electoral: unidad = municipio; desenlace = participación = votos totales / lista nominal por municipio y año; universo = municipios de Coahuila y Edomex presentes en ambos años; contraste principal = Δ participación 2024−2023 por municipio, con IC95 bootstrap por municipio (seed 42) y, como diagnóstico, Δ del mismo par en Edomex vs Coahuila; robustez (a) = 2024 con vs sin local concurrente, misma métrica, solo si P1 la habilitó; crosswalk 2016 para llevar el PREP federal a municipio, con conteo de secciones sin match (A.13). Escala declarada: puntos porcentuales de participación. Frase de sello: «el primer resultado que produzca este procedimiento es el que se reporta». COMMIT-2: resultados; entrada `civico.participacion.contingente` en milpa/tramite-ola5-propuesta-v0.yaml como MEDIDO·Δ (escala pp, NO probabilidad; B-bis: declara antes qué significa si el Δ es ≈0 — la regla queda acotada, no refutada por falta de contraste), tier PENDIENTE-DE-MESA, con la reserva escrita si el IC cruza cero. Si P1 no trajo alguna de las dos mitades: P3 se ejecuta sobre lo que haya y declara qué universo cubre — no se sustituye una mitad por otra fuente sin anotarlo. CIEGO a corridas-M/L.
P4 · CIERRE. FP-232 → EJECUTADA con la reconciliación firmada; nota de cierre con A.13 por tabla; tablero: recibo. Si P3 midió, redacta (sin lanzar) el sello para mesa en formato RH (qué dice el número, qué opción firmaría, qué cambia en el motor).

PERÍMETRO Y CONCURRENCIA: corpus (payloads nuevos) · data/manifiesto.yaml (vía script) · data/curacion-registro/{cola-adquisicion-registro, aliases-fuentes, evidencias, relaciones, utilidad-modelo}.tsv (vía N6) · data/cola-adquisicion-v1_0.tsv (regenerada) · milpa/tramite-ola5-propuesta-v0.yaml (una entrada) · tools/ (script de P3, nuevo) · forense/notas/ · forense/hallazgos.md · tablero · A.3 · cascada. NO toca milpa/tramite.yaml ni prereg-duelo-v2 (N4). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar (N4/N7 fusionan en paralelo; renumera quien fusiona segundo).
CONTADOR: payloads OBTENIDO +N · fichas corregidas +1 · reglas con Δ MEDIDO +1 si P3 corre completo · cero cargas al motor.
LO QUE NO HACE: no carga al motor (sello de mesa); no re-descarga ENDIREH; no toca corridas ni el marco; no instrumenta --verifica; no baja SICEE (si mesa ya lo dejó en Descargas MX, lo registra como P1-(v)).
SUCESORES: sello de la regla cívica (dirección redacta con firma de mesa) · MAESTRA34-N5 hereda CNGMD y la cívica para Ola 6.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA34-L4 · CIVICA-Y-CORPUS` el 2/sep/2026 en entorno
**UBUNTU**, con la skill `/acto` (`ADR-237`). `ADR-283`. Rama
`acto/maestra34-l4-civica-y-corpus`.

Las cuatro piezas corrieron completas:

- **P1** — 16 payloads `OBTENIDO` con A.7 y las tres capas de registro
  (manifiesto 937→953, cola `OBTENIDO` 54→58, +2 relaciones `CONFIRMADA` contra
  `N25`, que ES `R7.1`). Las DOS mitades que `ADR-278` y `ADR-280` dieron por
  inexistentes estaban en el portal de cada OPLE. `F232-a` contestada con fuente
  primaria: **no hubo municipios sin comicio local el 2/jun/2024** en ninguno de
  los dos estados → robustez (a) `NO-APLICA`, no se compró nada más.
- **P2** — `FP-231` → `EJECUTADA`. La letra de `F231-a` era mecánicamente
  imposible (`--registra` aborta por dedup) y su re-derivación existía desde el
  6/ago; lo pendiente era retirar la entrada vieja. `--verifica` del corpus pasa
  de `no_coincide=1` a `no_coincide=0`.
- **P3** — dos commits. **Δ participación municipal 2024−2023 = `+10.4790 pp`,
  `IC95 [+9.6890, +11.2652]`, n = 163 de 163**, IC que no cruza cero. Entrada
  `civico.participacion.contingente` en `milpa/tramite-ola5-propuesta-v0.yaml`
  como `MEDIDO·Δ`, `tier: PENDIENTE-DE-MESA`. Motor intocado.
- **P4** — `FP-232` → `EJECUTADA` con la reconciliación firmada; cascada
  completa; sello para mesa **redactado y no lanzado** en formato RH.

Desviaciones del encargo, declaradas:

1. **`F231-a` no se pudo ejecutar al pie de la letra** — el `--registra` que
   ordena aborta por dedup de contenido y la re-derivación ya existía. Se ejecutó
   su intención (retirar la vieja con nota que cite `FP-231` y `ADR-280`) y se
   dejó la forma de la retirada declarada para que mesa pueda revocarla.
2. **El crosswalk 2016 dejó de ser necesario para el contraste principal.** El
   encargo lo prescribía para llevar el PREP federal a municipio porque, cuando
   se redactó, faltaba la mitad local de 2024. `P1` la trajo, así que el
   principal es local-contra-local y el crosswalk se ejecutó igualmente como
   **lectura secundaria declarada**, con su conteo de secciones sin
   correspondencia (A.13: 7.77 % en Coahuila, 6.02 % en el Edomex).
3. **El id sugerido para la entrada re-derivada de ENDIREH
   (`endireh_2016_bd_mujeres_v2`) no se usó**: el script no permite crearlo, y el
   id que sobrevive es el que `ENCARGO REPAIR-1` ya había derivado.

Detalle: `forense/notas/2026-09-02-MAESTRA34-L4-cierre.md` y
`forense/notas/2026-09-02-MAESTRA34-L4-P3-spec.md`.
