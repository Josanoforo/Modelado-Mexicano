ACTO GEN2-TRAMITE-FIRMAS-1 · PROPAGA-FIRMAS · nota del acto

Encargo archivado verbatim: `forense/encargos/2026-09-08-GEN2-TRAMITE-FIRMAS-1-PROPAGACION.md`.

## §0 · Qué hace esta nota

Propaga, sin decidir, las seis firmas de mesa del 8/sep/2026 (D-1 a D-6) sobre cinco piezas (P1-P5). D-1 no la ejecuta este acto. D-2 a D-6 se propagan aquí, con el cruce mecánico que D-4 exige antes de tocar FP-286/FP-343.

## §1 · P1 · FP-348 SELLADA

Firma D-2 verbatim: «la idea central de todo este proyecto es un LLM puede superar a LLM con dato (todo el corpus), si esto no está claro ahorita entonces no estamos comparando correctamente.»

Directiva de diseño que esta firma instala: el selector B (`tools/baseline_temporal.py`, GEN2-T10) se adopta como piso común de los tres contendientes. C0-D queda instruido a que su comparación de primera clase sea la pareada `L_SOLO` ↔ `L_CORPUS` (la tesis del programa), con `M` como tercer contendiente y `B` como piso de los tres, todo bajo el mismo corte informativo del selector. El ensayo remesas ENIGH 2016→2022 queda autorizado para C0-B.

Hallazgo que C0-D debe adjudicar, no enterrar: el diagnóstico D4 vigente (`grep -o` sobre `agregado-v1_3-resultado.json`, 8/sep/2026) muestra `L_SOLO_vs_M` (3 apariciones) y `L_CORPUS_vs_M` (2 apariciones) pero ningún par `L_SOLO` vs `L_CORPUS`; las cifras sueltas son L_SOLO 11.69 pp · L_CORPUS 19.60 pp · M 4.51 pp — el corpus EMPEORA al LLM en el diagnóstico actual, sin comparación pareada sellada. C0-D lo convierte en veredicto o lo explica.

`forense/firmas-pendientes.tsv`: FP-348 `ABIERTA` → `FIRMADA`, `firmada_en` = la firma D-2 verbatim de arriba, con la glosa de directiva íntegra en el propio campo `estado` (token al inicio, A.16).

## §2 · P2 · FP-347 CERRADA, VENCIDO-EN-ALCANCE

Verificación de existencia contra `7e2a608a`/`d8b5f0b` (8/sep/2026): `grep -c "aviso_M" forense/prereg-duelo-v2/corredor_l_v1_2.py` → `0`. Ningún consumidor GEN2 lee `aviso_M`. `DIN-M-01` ya emite (p=0.174804, `ADR-398`). Aplicando D-3 («está bien que hagamos la corrección en otro encargo, solo que si ese requisito es de Gen1 entonces ya no es lo que necesitamos pues estamos en gen 2») al hecho verificado: el requisito de corregir el `aviso_M` es prosa histórica de Gen1 que GEN2 no consume — cierra `VENCIDO-EN-ALCANCE`, sin acto sucesor, sin tocar el JSON sellado (E.3).

`forense/firmas-pendientes.tsv`: FP-347 `ABIERTA` → `CERRADA, VENCIDO-EN-ALCANCE`, `ejecutada_en` = 2026-09-08 (este acto).

## §3 · P3 · el cruce que D-4 exige (FP-343/FP-286)

Firma D-4 verbatim: «siempre y cuando estemos súper seguros que no se usan o usarán o contienen algo relevante.»

Este acto NO cierra en bloque: cruza mecánicamente las 28 filas de `forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md` contra el estado vigente de `data/curacion-registro/cola-adquisicion-registro.tsv` (columna `estado_A4A5`, actualizada por A4/A5/A6 desde el 3/sep) y contra el uso por consumidor (`milpa/`, `canon/modelo-decision-v4_0.md`, specs vigentes de `forense/prereg-duelo-v2/`).

Comando base: `awk -F'\t' -v n="<fuente_canonica>" '$2==n{print $5"\t"$8}' data/curacion-registro/cola-adquisicion-registro.tsv`, corrido para las 28 filas, 8/sep/2026.

### 3.a · CERRADAS — objeto OBTENIDO o ya cerrado por A4/A5/A6 (15 de 28)

| # | fuente_canonica | fila_origen | estado_A4A5 | cita |
|---|---|---|---|---|
| 1 | IMPACT_EVALUATION_OF_MOBILE_PEDAGOGICAL_TUTORS_2016 | cola-adquisicion-v1_0.tsv:6 | OBTENIDO | `adq15_wb6667_*` (24 payloads doc+DDI) + `mex_2016_apipie_v01_m_stata` |
| 2 | SE | cola-adquisicion-v1_0.tsv:20 | CERRADA-PREEXISTENTE | cerrada por acto previo a este cruce |
| 5 | BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO | cola-adquisicion-v1_0.tsv:28 | OBTENIDO | `a6_mmad_protesta_v16_dta;a6_mmad_protesta_csv` |
| 14 | EARTHQUAKE_TRUST_LAPOP_2017 | cola-adquisicion-v1_0.tsv:58 | OBTENIDO | fila registro, receta BAJAR de N4-A2 ejecutada |
| 15 | IMSS_BIENESTAR_ACCIONES_DE_INFRAESTRUCTURA | cola-adquisicion-v1_0.tsv:59 | OBTENIDO | fila registro, receta BAJAR de N4-A2 ejecutada |
| 18 | EXT_OF_11_REUNE_REDECO | cola-adquisicion-v1_0.tsv:70 | OBTENIDO | fila registro, receta BAJAR de N4-A2 ejecutada |
| 19 | ENVIPE_EXTRACCION_TEXTO_REACTIVO | cola-adquisicion-v1_0.tsv:76 | OBTENIDO | fila registro, receta BAJAR de N4-A2 ejecutada |
| 20 | BANXICO_ENCUESTA_COMPETENCIAS_FINANCIERAS_EXTRACCION_TEXTO | cola-adquisicion-v1_0.tsv:78 | CERRADA-PREEXISTENTE | ya OBTENIDO desde ago/2026 (manifiesto.yaml), problema es de extracción, no adquisición |
| 21 | DIN-11_CONOCIMIENTO_CUENTAS_SIN_COMISION_SIN_CANDIDATA | cola-adquisicion-v1_0.tsv:79 | CERRADA-PREEXISTENTE | payload ya en `manifiesto.yaml` (ENIF 2015/2018) |
| 23 | SICEE | cola-adquisicion-v1_0.tsv:81 | OBTENIDO | `a6_sicee_catalogo_elecciones_federales` + 3 más |
| 24 | TEPJF_ELECCIONES_CONCURRENTES_1991_2018 | cola-adquisicion-v1_0.tsv:NUEVA-L6 | OBTENIDO | fila registro, receta BAJAR de N4-A2 ejecutada |
| 25 | IEEPCO_OAXACA_SERIE_MUNICIPAL | cola-adquisicion-v1_0.tsv:NUEVA-L3 | OBTENIDO | superada por A4/A6 tras haber sido MESA-DECIDE en la nota original |
| 26 | IETAM_TAMAULIPAS_SERIE_MUNICIPAL | cola-adquisicion-v1_0.tsv:NUEVA-L3 | OBTENIDO | fila registro, receta BAJAR de N4-A2 ejecutada |
| 27 | INEGI_CNGF | cola-adquisicion-v1_0.tsv:NUEVA-L6 | OBTENIDO | superada por A4/A6 tras haber sido MESA-DECIDE en la nota original |
| 28 | PDN_SESNA_S1_S2_S3_S6 | forense/encargos/2026-09-03-MAESTRA37-N3-SELLA-CIVICA-COERCITIVO-Y-PROPAGA.md | OBTENIDO | `pdn_s3v2` |

### 3.b · CERRADAS COMO HISTORIA — objeto no existe / nadie lo compone, cero consumidores hoy (3 de 28)

Criterio D-4: se cierran solo las que combinan (i) razón NO-BAJAR-PORQUE original de "no existe como dataset publicado/composable" y (ii) cero referencias de consumidor verificadas hoy.

| # | fuente_canonica | estado_A4A5 | verificación de consumidor | veredicto |
|---|---|---|---|---|
| 3 | CANAL_DE_ADQUISICION_REFERIDOS_FINTECH | NO-ENCONTRADO | `grep -rIn "CANAL_DE_ADQUISICION_REFERIDOS_FINTECH" milpa/ canon/modelo-decision*` → 0 | cierra: concepto de mercadeo sin fuente publicada, tres sondeos independientes (6/ago, 1/sep, 3/sep) coinciden en cero candidatos |
| 16 | MERCER_GPTW_CLIMA_DESEMPENO | NO-ADQUIRIDA-POR-COSTO | `grep -rIn "MERCER\|GPTW" milpa/ canon/modelo-decision*` → 0 | cierra: producto B2B por cotización, ningún punto final es un archivo descargable; R2.2/R10.2 ya archivadas con veredicto D (`ADR-196`/`ADR-199`) sobre censo dedicado que confirma EXISTE-NO-SATISFACE |
| 22 | SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS_SIN_CANDIDATA | NO-ENCONTRADO | `grep -rIn "SFT-06\|cuidado_entre_hermanos" milpa/ canon/modelo-decision*` → 0 | cierra: ENASIC sondeado completo no trae el ítem, SABE México sin microdato público y su propia fuente es evidencia cualitativa (19 casos), no un reactivo estandarizado |

### 3.c · VIVAS — devueltas a mesa, no cerradas (10 de 28)

Costo/qué-desbloquea, para que mesa decida en conversación (no en este acto):

1. **HOMESCAN_CONSUMER_PANEL_SERVICES** (NO-ADQUIRIDA-POR-COSTO) — qué: panel de compra de hogares comercial NielsenIQ. Costo: pedir ficha de cobertura sin contratar (días-semanas, $0), o no gastar (R1.4 ya cerrado con veredicto D firmado, `ADR-187`). Desbloquea: nada obligatorio — solo exploración de marca real vs. sustituto funcional, ya cubierta por el veredicto vigente.
2. **PANEL_DE_COMPRA_DE_HOGARES** (NO-ADQUIRIDA-POR-COSTO) — misma familia que HOMESCAN/Kantar. Costo: mismo patrón de solicitud institucional. Desbloquea: nada obligatorio, mismo veredicto D ya firmado.
3. **REGISTRO_DE_TANDAS_Y_REPUTACION** (NO-ADQUIRIDA-POR-COSTO) — qué: base propietaria de reputación en tandas. Costo: solicitud formal a empresa comercial, sin garantía. Desbloquea: variable de incumplimiento/reputación para R8.2/N29, hoy cubierta parcialmente por fuentes afines.
4. **REGISTRO_OPERATIVO_DE_TANDAS_DIGITALES** (NO-ADQUIRIDA-POR-COSTO) — qué: TandaMás, base operativa cerrada. Costo: convenio institucional (semanas-meses, sin garantía) vs. cerrar NO-ACCESIBLE. Desbloquea: mismo hueco que (3), sin sustituto hoy.
5. **ENAFIN** (OBTENIDO-PARCIAL — tabulados públicos ya en corpus, microdato de empresa no) — qué: tasa de rechazo por sin-historial POR SEGMENTO (N19). Costo: dos rutas con costo distinto, ninguna ≤1 min. Desbloquea: el cruce exacto que N19 pide; hoy solo el agregado nacional está cubierto.
6. **PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND** (OBTENIDO-PARCIAL — dos PDF hermanos SSRN ya en corpus, objeto exacto Bauchet SSRN 2474620 no) — qué: comparador de marca en seguro de vida. Costo: alta de hermana en `aliases-fuentes.tsv` (firma A.7) para lo ya bajado, o perseguir el original tras Cloudflare (minutos-días, éxito incierto). Desbloquea: ninguno de los dos cierra R1.4 por sí solo (falta comparador de marca en ambos casos).
7. **OECD** (OBTENIDO-PARCIAL — TDG/integridad pública ya en corpus, el microdato Trust Survey PUM no, formulario en disco) — qué: microdato LAC 2025 recolectado en México por INEGI. Costo: enviar el formulario ya descargado a `govtrustinfo@oecd.org`, revisión discrecional, espera sin plazo. Desbloquea: robustecer la reserva del eje 3 (ISSP 2017) o alimentar 3 candidatas de N30 aún `APERTURA_INDETERMINADA` — R8.3 ya está cerrada y firmada, no depende de esto.
8. **PI** (NO-OBTENIDO-POR-ESTE-AGENTE, 4 rutas agotadas) — qué: scoring alternativo CNBV vía `portafolioinfo.cnbv.gob.mx`, tablero Power-BI sin URL fija de exportación. Costo: adquisición dedicada fuera de perímetro de `/adquiere` (navegar filtros y exportar a mano). Desbloquea: cobertura de vivienda para N19-scoring_alternativo; la regla `dinero.credito.scoring_alternativo` ya tiene `[MEDIA]` fijo en `canon/modelo-decision-v4_0.md:504`, así que esto no reabre ningún veredicto, solo lo robustecería.
9. **EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6** / EXT-OF-05 (OBTENIDO-PARCIAL — CompraNet5 contratos/expedientes 2019-2023 en corpus, catálogo histórico completo no) — qué: ampliar cobertura temporal de contrato/procedimiento/proveedor. Costo: ~951MB, duplica trabajo de identidad A.7. Desbloquea: nada que el veredicto A.4 ya fijado (hueco de sanción) necesite — solo cobertura temporal adicional.
10. **INEGI_CNGF** — reclasificado de MESA-DECIDE original: aunque `estado_A4A5` marca OBTENIDO (documentación, cuestionarios, marco conceptual), el CSV de datos abiertos propiamente dicho sigue detrás de JS y cero necesidades de `relaciones.tsv` citan hoy esta fuente (verificado, misma búsqueda que la nota original). Se mantiene vivo por transparencia del cruce, no porque bloquee algo: mesa puede cerrarlo NO-BAJAR-PORQUE en su próxima pasada si acepta que documentación ya obtenida es suficiente.

Nota sobre `DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO` (fila 4): `estado_A4A5` pasó de NO-ACCESIBLE a OBTENIDO-PARCIAL (payloads CONDUSEF de registros de instituciones financieras/usuarios de seguro). No se cierra aquí: el objeto original (cruce denuncia↔tenencia de seguro a nivel de registro individual) no está confirmado como satisfecho por ese payload — D-4 exige estar súper seguros, y esta pieza no lo está. Queda en la lista de arriba de facto, incluida como advertencia, no como ítem con costo — mesa decide si el payload CONDUSEF cierra algo o no.

`forense/firmas-pendientes.tsv`: FP-286 y FP-343 `ABIERTA`/`EJECUTADA` (según fila) → `FIRMADA-PARCIAL` (cerradas: 18 de 28 — 15 por (a) + 3 por (b); vivas: 10 de 28, lista arriba), hasta la segunda pasada de mesa sobre §3.c.

## §4 · P4 · FP-342 CERRADA

Firma D-5 verbatim: «revisa primero el repo para entenderlo, ya nos ha pasado muchas veces que queremos re-descubrir la rueda cuando la solución ya está.»

`forense/notas/2026-08-13-w-limpieza-worktrees.md:11` ya diagnosticaba, el 13/ago/2026, el mismo bind-mount `devtmpfs` sobre `.git/config`/`.git/hooks` que FP-342 (7/sep/2026) redescubrió sin buscar: la causa es el harness del sandbox del propio agente, no la caja de mesa; el rodeo documentado allí mismo resuelve la escritura y está en uso desde agosto. Precedente asentado en `forense/hallazgos.md` (§5 abajo) para que la próxima vez que un síntoma "nuevo" aparezca en la caja, se busque antes de re-diagnosticar.

`forense/firmas-pendientes.tsv`: FP-342 `ABIERTA` → `CERRADA`, `ejecutada_en` = 2026-09-08, cita `forense/notas/2026-08-13-w-limpieza-worktrees.md:11`.

## §5 · P5 · la pila D-6, de un plumazo

Firma D-6 verbatim: «firmamos todo de un plumazo.»

(a) **NC-0027 → CERRADA.** La corrección vive en `CALC-MOTOR-celdas-semilla-v2` (medidor con raíz correcta, 1 `dirname`; registro `SUPERADO→v2`, PR #622). El v1 sellado queda como historia (E.3).

(b) **NC-0031 → CERRADA.** El merge de PR #620 fue la aceptación de la convención de rama.

(c) **`forense/hallazgos.md` gana la línea:** «APARATO-GEN2-PRE-E5=READY · GO-E5-0=SI (PR #614, cuerpo del PR; asentado por firma D-6 del 8/sep)».

(d) **`.claude/commands/despacha.md`** gana la re-verificación del candado inmediatamente antes de escribir la huella, no solo al arrancar — la mejora que el `[REVISA]` de PR #619 propuso tras medir tres hechos caducados en 100 minutos. La nota de ese revisor vive en `claude/revisa-post-hoc-619`; fusionarla es de mesa (este acto no la toca, `NO-CORRIDO` abajo), pero la mejora queda instalada en `.claude/commands/despacha.md` directamente por este acto.

## §6 · Verificación de existencia — A.8 (ya contestada en el propio encargo, contra `7e2a608a`, re-verificada aquí contra `d8b5f0b` tras el fast-forward de 7 commits al arrancar): sin diferencia material — ninguno de los 7 commits nuevos toca `forense/firmas-pendientes.tsv`, `forense/no-corrido.tsv`, `forense/hallazgos.md`, `.claude/commands/despacha.md` ni el corredor L GEN2.
