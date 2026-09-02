ENCARGO · ACTO MAESTRA34-N4 · PLOMERIA-v1_2 — invoca /acto
SHA de redacción: 9d2e69d (merge PR #452 / ADR-277). Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR — las tres decisiones firmadas abajo van dentro. RUTA CRÍTICA: sin P1 mesa no puede correr L v1_2 y MAESTRA34-N3 no arranca.

ENTORNO ASIGNADO: NUBE. NO se lanza en UBUNTU (no abre microdato). MODELO SUGERIDO: Opus (P1 edita herramienta sellada con regresión; P3 carga al motor).
CARRILES: caja libre tras #452; MAESTRA34-A1 (registro de descargas, caja) puede correr en paralelo — perímetros disjuntos (data/, registro del curador) salvo cascada. N3 sigue GATED.
COMPUERTA: ninguna (este encargo archivado por PR [COLA] fusionado por mesa = firma).

FIRMAS DE MESA — verbatim, 1/sep/2026 (un solo mensaje: «DR - a, DF-a, DM- por qué vamos a devolver algo que si hace sentido de acuerdo al motor vs lo que dice la data? es justo lo que queríamos probar, el motor vs data. Si eso da eso da.»). El ejecutor propaga, no decide (SELLA-3).
- DR-a: se autoriza editar runner_l_cli.py (sellado por MAESTRA33-E17, ADR-264) para que derive la dimensión de la spec en vez de traer 11/176 fijo; se re-sella con sha y regresión v1_1=176.
- DF-a: DIN-M-01 queda SIN M este ciclo, declarada como exclusión con razón para N3 (13 de 14); extender F-DD a rangos de ola es sucesor tras la revisión del 8/sep (MAESTRA34-E1), no de este acto.
- DM (sí a (i), (a) en (ii), con la frase «Si eso da eso da»): se sustituye el ASIGNADO 0.62 de tramite.mordida.discrecional por el MEDIDO 0.085118 (ENCIG 2025, serie 8 olas como θ informativa; el 0.62 se conserva REFUTADA-POR-R citando ADR-270/ADR-276); se acepta el mapeo canal↔disparador del ejecutor de L1 (presencial P7_3=1 ≈ «nadie observa»; digital/registrado P7_3∈{3,4,5} ≈ «registro_o_testigos») y tramite.mordida.con_registro carga 0.116 presencial / 0.027358 digital en lugar del 0.12 ASIGNADO. Tier: FUERTE (el que el motor ya declara), clase MEDIDO·p.
- DA-a (1/sep, ya firmada en tanda 1): FP-190 se cierra citando ADR-236 (fase 1), C4 (fase 2-A) y la firma 3 del 1/sep («pasan a externo/adquisición de datos»).

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra 9d2e69d ═══
(1) ESTRUCTURA: forense/prereg-duelo-v2/ (runner, paquete L, corridas-M); milpa/tramite.yaml vía Dominio 4 y precedente de carga MAESTRA32-E20-P0 / MAESTRA34-N1 (ADR-274); tablero (Dominio 9); .claude/commands/acto.md (skill, versionada); forense/encargos/cola/ (estados).
(2) CONTENIDO:
  - runner_l_cli.py:188/190/198/219 traen `11`/`176` literales (PAQUETE-L-v1_2.md §6, con salida `AssertionError: 224 rutas construidas, esperaba 176`) → EXISTE-NO-SATISFACE. Parche propuesto ahí mismo, no aplicado.
  - DIN-M-01: sin M (forense/notas/2026-09-02-marco-M-v1_2-emite-m.md §Hallazgo); corridas-M = 35 archivos; ninguno `DIN-M-01__v1_2` → NO-ENCONTRADO por diseño.
  - Mordida en propuesta: `tramite.mordida.discrecional_encig_serie` (l.461) y `tramite.mordida.con_registro_encig2025` (l.542), ambas MEDIDO·p, PENDIENTE-DE-MESA → EXISTE-SATISFACE como insumo. Motor: l.40 (0.62 ASIGNADO) y l.85 (0.12 ASIGNADO) → son las que se sustituyen.
  - Cola: forense/encargos/cola/2026-09-01-MAESTRA34-N2-MARCO-M-v1_2.md sigue `LISTO-NUBE` con PR #450 fusionado → EXISTE-NO-SATISFACE (falta la marca).
  - acto.md §2.2 ofrece `git log --oneline origin/main | grep -c '<rótulo>'` como verificación de compuerta; ADR-277 midió falso positivo (commit [COLA] bb54f99 nombra rótulos en el asunto) → EXISTE-NO-SATISFACE.
  - FP-190: ABIERTA; su texto ya registra fase 1, fase 2-A y las 6 filas en adquisición.
(3) COBERTURA RETROACTIVA: no aplica.

PIEZAS (un commit por pieza; ninguna estima)
P1 · RUNNER. Aplica el parche de PAQUETE-L-v1_2.md §6 tal cual (n_celdas = len(cargar_celdas_l_spec()); total_esperado derivado; se eliminan los literales 176 en 188/190/198/219). Regresión obligatoria antes de commitear: `--dry-run` con L-spec-v1_1.json → 176 rutas; con L-spec-v1_2.json → 224. Re-sella: sha256 nuevo junto al de E17 (el viejo queda como historia), enmienda fechada en PAQUETE-L-v1_2.md §6 y en la nota de E17. FP-228 pasa de «no lanzable» a «lanzable, mesa corre» con la línea de comando exacta que mesa debe ejecutar. Si el parche toca algo más que esas cuatro líneas, PARO y reporta.
P2 · EXCLUSIÓN DIN-M-01 (DF-a). Escribe forense/prereg-duelo-v2/exclusiones-v1_2.md: celda, razón (F-DD sin rangos de ola, marco congelado clasifica olas 2 y 3 como P0 «panel retenido»), firma DF-a verbatim, y la instrucción para N3: «puntúa 13 de 14; DIN-M-01 se reporta como exclusión con razón, no como NO-APLICA». Abre fila de tablero «F-DD rangos de ola» gateada a MAESTRA34-E1 (8/sep), vence 2026-09-15. No toca el sorteado ni F-DD.
P3 · SELLO MORDIDA (DM). Carga al motor con el procedimiento de MAESTRA34-N1 (descongelamiento acotado a las dos ids; smoke `emitir_binaria == p` por regla): tramite.mordida.discrecional → p 0.085118 / 0.914882, clase MEDIDO·p, ola_calibracion ENCIG 2025, serie_olas verbatim de la propuesta como θ informativa, cabecera REFUTADA-POR-R sobre el 0.62 (no se borra); tramite.mordida.con_registro → disparadores con el mapeo firmado, p 0.116 presencial (id-conducta y cifra exactas de la propuesta l.542+) y 0.027358 digital; el 0.12 queda REFUTADA-POR-R. Entradas de la propuesta → SELLADA con este PR. Si un campo no pasa el esquema de tests/check.py, PARO de la pieza con el nombre del campo.
P4 · TRÁMITE. (a) Cola: N2 → `## CONSUMIDO` con PR #450 y ADR-275 (A.3). (b) FP-190 → FIRMADA-EJECUTADA con las tres citas de DA-a. (c) acto.md §2.2: la verificación de compuerta por rótulo se hace por PRODUCTO (archivo/entrada que el acto gateado debió producir, `git cat-file -e` o `git show origin/main:<ruta>`) y el `grep` del asunto queda como indicio, no como prueba; cita ADR-277 y el commit bb54f99 como el falso positivo medido. Una línea en forense/hallazgos.md.

PERÍMETRO Y CONCURRENCIA: forense/prereg-duelo-v2/{runner_l_cli.py, *.sha256 del runner, PAQUETE-L-v1_2/PAQUETE-L-v1_2.md, exclusiones-v1_2.md} · milpa/tramite.yaml · milpa/tramite-ola5-propuesta-v0.yaml (solo estado SELLADA) · forense/encargos/cola/…N2… (marca) · .claude/commands/acto.md (§2.2) · forense/hallazgos.md · tablero · notas · A.3 · cascada. En paralelo: MAESTRA34-A1 (caja: data/, registro del curador). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar (FP máx 228+, ADR 278 candidato, tras git fetch).
CONTADOR: reglas del motor con p MEDIDA +2 (sustituciones) · prior ASIGNADO refutado y retirado del cálculo −2 · runner re-sellado +1 · cero estimaciones nuevas, declarado.
LO QUE NO HACE: no corre L (es de mesa, FP-228); no extiende F-DD; no re-emite M; no toca corridas-R; no abre Ola 6.
SUCESORES: mesa corre PAQUETE-L-v1_2 (224 llamadas) → PR [L] → extracción con tools/extrae_l_v1_1.py sin editar → MAESTRA34-N3 · MAESTRA34-N5 (Ola 6, gateado a N3) · MAESTRA34-E1 (8/sep) recibe la fila F-DD rangos.

## CONSUMIDO

Ejecutado 2/sep/2026 por `ACTO MAESTRA34-N4 · PLOMERIA-v1_2` con la skill `/acto`
(`ADR-237`), entorno NUBE `cloud_default`, sin abrir microdato ni descargar nada.
`COMPUERTA: ninguna` (declarada por el propio encargo, archivado por PR [COLA]
fusionado por mesa).

Cuatro commits, uno por pieza, en la rama `claude/maestra34-n4-plomeria-d6oz84`:
`P1` re-sella `runner_l_cli.py` (firma DR-a); `P2` exclusión `DIN-M-01` (firma
DF-a); `P3` sella la mordida ENCIG 2025 al motor (firma DM); `P4` trámite
(cola N2, FP-190, `.claude/commands/acto.md` §2.2, firma DA-a). Cascada: `ADR-281`,
`canon/estado-programa-v1_10.md` L0 (280 → 281), `canon/registro-rotulos.tsv`,
`forense/firmas-pendientes.tsv` (FP-228, FP-190, FP-233 nueva),
`forense/hallazgos.md`.

PR: `[MAESTRA34-N4] ACTO MAESTRA34-N4 · PLOMERIA-v1_2` (rama
`claude/maestra34-n4-plomeria-d6oz84`).
