# Nota de cierre · ACTO GEN2-RELEVO-TANDA-6

**P1 (replay).** `python3 tools/corrida0.py verify CALC-L-DESDE-CAPTURAS-v1_0`
EJECUTADO: `VERIFY: REPRODUCE (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)`. El
asiento de `forense/replay-evidencia.tsv` ya existía (línea del 21/sep,
`CALC-L-DESDE-CAPTURAS-v1_0--ee2443e8dc40 · REPRODUCE · IDENTICO`), así que
E.7 ya estaba satisfecho antes de este acto — lo que faltaba era que el
**registro** (`data/corrida0/corridas.tsv`, DERIVADO) lo reflejara.
`python3 tools/corrida0.py registro --verifica --escribe --lote
CALC-L-DESDE-CAPTURAS-v1_0` lo deriva correctamente hoy
(`resultado_replay: NO-VERIFICADO -> REPRODUCE`, `contexto_replay: NO-VERIFICADO
-> IDENTICO`) — pero los tres TSV que escribe son `# DERIVADO — NO EDITAR`
(P4, `#984`, `tools/derivados_protegidos.py`): **no se commitean**; el job
de push a `main` los re-deriva. `NC-260922-GEN2-RELEVO-TANDA-5-f54e-01`
(el diagnóstico de `_evidencia_vigente` comparando por cadena ordenada) se
cierra: hoy no reproduce — el veredicto de `verify` y el asiento casan sin
tocar `tools/corrida0.py` (perímetro ajeno, no se tocó).

**P2 (los 18 pines).** PARA. Verificado por mutación directa contra
`pines_mesa.valida_pin` (no por lectura): con la guarda (a) ya en verde,
las 18 filas construidas según F-L (`marco-M::{CIV-M-01,02,04,10,12,13;
FAM-M-05,06,07}::{L-solo,L+corpus}`, `result_gen2=RESULT-LDESC-TABLA-JSON`,
`via=i-CRUDO`) son **`RECHAZADO-SIN-INSUMO-CRUDO`** por la guarda (b)
(`pines_mesa._tiene_crudo`): `CALC-L-DESDE-CAPTURAS-v1_0/spec.yaml` declara
7 inputs, los 7 con `origen: repo`; ninguno `origen: manifiesto` ni con
`manifiesto-capturas` en la ruta, y `dependencias_materiales: []`. Las 224
capturas que el CALC de verdad lee (vía `IN-F5C-PLAN`, un JSON de rutas)
no están declaradas como insumo crudo individual en el spec congelado. La
premisa de F-L («mide desde capturas selladas con hash, que es la vía (i)
de 4.1») es cierta en lo que el CALC *hace*; la guarda mecánica de 4.1 no
lo ve porque el spec no lo declara así. No se tocó `spec.yaml` (congelado,
`#973`, PARO (d)) ni `tools/pines_mesa.py` (TUBERÍA de 4.1). Contador:
**sin cambio** — `dependencias_numericas_legacy_activas` sigue en 146; 0
pines nuevos. `NC-260922-GEN2-RELEVO-TANDA-6-7510-01` abierta,
`DECISION-DE-MESA-PENDIENTE`: si se enmienda el spec (D-18, enmienda de
cableado) para declarar el manifiesto de capturas como insumo crudo, o si
la guarda (b) debe reconocer un `origen: repo` cuya ruta cita el plan de
capturas como insumo crudo indirecto.

**P3 (cierre).** FP `FP-260922-GEN2-RELEVO-TANDA-5-f54e-01` (F-L) sigue
`FIRMADA` — la firma de mesa no cambia; lo que falta no es la firma, es que
el spec o la guarda reconozcan el insumo. Se actualizó su columna de
ejecución con este hallazgo. `NC-260922-GEN2-RELEVO-TANDA-5-f54e-01`
CERRADA por este acto (P1). `NC-260922-GEN2-RELEVO-TANDA-6-7510-01` abierta
(P2). Cero escritura en `milpa/`, en `forense/prereg-duelo-v2/` y en specs
selladas. Cero derivados commiteados (`corridas.tsv`, `resultados.tsv`,
`usos.tsv` quedan como el job de main los re-derive).
