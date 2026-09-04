ENCARGO · ACTO MAESTRA37-N8 · CONSOLIDA-DECISIONES — invoca /acto

SHA de redacción: 2e79d153 · COMPUERTA: PR de INFRA-1 fusionado, verificada POR PRODUCTO (test -f tools/curador_registro/alta_relacion.py o el módulo que la aloje). No cumplida → cero commits, reporta con A.13. ENTORNO ASIGNADO: NUBE. NO en CAJA. MODELO SUGERIDO: Sonnet (propagación; la única pieza con juicio —D2-f, enmienda de canon— trae el texto dictado aquí). CARRILES: N9 (nube, encargos/ — disjunto), MAESTRA38-A1 (caja — manifiesto y cola; este acto NO añade filas a la cola, sólo edita estado/nota de filas existentes; si INFRA-1 entregó el writer, se usa; si no, tsv_crudo.py).

FIRMAS DE MESA — verbatim: §0 íntegro. Este documento se archiva con el 0-bis (A.3) y es la fuente de cada letra; el ejecutor propaga, no decide (SELLA-3).

═══ A.8 contra 2e79d153 ═══ (1) ESTRUCTURA: tablero; milpa/tramite.yaml (17 reglas) y milpa/tramite-ola5-propuesta-v0.yaml (17 situacion: PENDIENTE-DE-MESA por conteo directo — el digesto da 0 porque su patrón no lee ese campo, defecto a una línea de hallazgos); canon/modelo-decision-v4_0.md §7; data/curacion-registro/necesidad-objeto-modelo.tsv (41 N, N36 única de salud); cola 112 filas; forense/prereg-duelo-v2/runner_l_cli.py. (2) CONTENIDO: FP-179/235/240/259/284 ABIERTA; FP-280 decisión pendiente; cinco filas comerciales NO-ACCESIBLE; grep -c "NO-ADQUIRIDA-POR-COSTO" data/curacion-registro/*.tsv .claude/commands/mapea.md → 0 (vocabulario nuevo, se documenta en mapea.md §4 junto a A.4). (3) COBERTURA: nada retroactivo.

SPEC — un PR, un ADR (el ADR incluye la enmienda de canon de D2-f como inciso propio), un recibo. Un commit por bloque: P1 · D2-a (propagación mecánica, 7 entradas) + D2-b/c/d/e/g con se_mueve_si verbatim de la tabla; cargas D2-c/D2-d con smoke emitir_binaria()==p; prior 0.09 REFUTADO-POR-COTA, cuerpo intacto. Motor 17 → 20 reglas (declara el real). P2 · D2-f: enmienda append en canon/modelo-decision-v4_0.md §7 (0 líneas borradas): R7.3 [FUERTE]→[MEDIA], dos instrumentos citados con IC, se_mueve_si verbatim, estampa A.10. P3 · D1: alta_relacion.py × 4 (spec por archivo, textos de FP-284 verbatim), re-asiento de las ocho altas de A1 §5.1 bajo su N real (la de etiquetado → R4.5; las siete CANDIDATA quedan bajo N36 con nota), baseline.py {"ok": true}. P4 · D3: runner_l_cli.py (nombre __<spec>, modelo_real en corrida), sin re-correr; una línea en el registro sellado de L v1_1/v1_2: «capturas anteriores a v1_3 no traen modelo_real ni spec en nombre». P5 · Cola y vocabulario: D5 (cinco filas → NO-ADQUIRIDA-POR-COSTO, definición en mapea.md §4), D6 (dos filas → PENDIENTE-DE-MESA con receta), D7 (nota en PDN_SESNA). mapea.md §4 gana la línea: «un NO-ENCONTRADO de agente no cierra una fila de la cola; la cierra mesa con informe de hermanas a la vista (firma 3/sep/2026)». P6 · Tablero: FP-179 EJECUTADA con (2) CERRADA-SIN-SUCESOR; FP-235/240 EJECUTADA; FP-284 EJECUTADA; FP-280 FIRMADA (b); FP-259 FIRMADA (iii) (ejecuta INFRA-2). Hallazgos: dos líneas (digesto ciego a situacion:; 7 entradas cargadas sin propagar situacion).

PERÍMETRO Y CONCURRENCIA. Toca: milpa/tramite.yaml · milpa/tramite-ola5-propuesta-v0.yaml · milpa/procedencia.yaml (sólo el prior 0.09) · canon/modelo-decision-v4_0.md (append §7) · canon/gobernanza-v1_15.md · data/curacion-registro/{necesidad-objeto-modelo,relaciones,procedencias,utilidad-modelo,cola-adquisicion-registro}.tsv + baseline.json (por alta_relacion.py/writer) · .claude/commands/mapea.md §4 · forense/prereg-duelo-v2/runner_l_cli.py · forense/firmas-pendientes.tsv · forense/hallazgos.md · A.3 · cascada. NO toca: data/manifiesto.yaml · tests/manifiesto.py · tools/curador_registro/*.py · forense/encargos/* (N9) · canon/motor-nucleo-medible-v1_0.md · corridas-L existentes. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR: ADR-328 (INFRA-1 toma 328 si fusiona antes → 329) · FP-285 recibo. CONTADOR: firmas propagadas 12 · motor 17 → 20 · sellos sin carga +5 · necesidades 41 → 45 · filas ABIERTA 4 → 0 (FP-259 queda FIRMADA hasta INFRA-2) · medición: cero, declarado. Lo que NO hace. No mide; no re-corre L; no toca la cola con filas nuevas; no decide letras.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA37-N8 · CONSOLIDA-DECISIONES` (4/sep/2026, NUBE), rama
`claude/acto-maestra37-consolidacion-1ekmtd`. `PR #523`. `ADR-328` (acto principal) y `ADR-329` (enmienda de canon
D2-f, inciso propio). Piezas deferidas y documentadas, no forzadas: (1) una séptima
entrada D2-a con `situacion` desactualizada, declarada por la firma de mesa, no se
localizó en `milpa/tramite.yaml` -- 6 encontradas, no 7; (2) el re-asiento de las ocho
altas de A1 §5.1 en `relaciones.tsv`/`evidencias.tsv`/`utilidad-modelo.tsv` bajo su `N`
real se intentó y `baseline.py` lo rechazó (`relacion_id no determinista`) -- revertido,
sucesor declarado. `python3 tests/check.py --baseline`: ROJO por 2 `FAIL` de `T22`
pre-existentes contra dos encargos de agosto sin fila en `firmas-pendientes.tsv`,
verificados anteriores a este acto (no introducidos por él, fuera de su perímetro --
territorio de D9, explícitamente excluido de este acto).
