# ACTO MESA-CONCILIACION-E01 · cierre

## Resultado

Las veinte decisiones recibidas quedaron asentadas con objeto, fecha, fuente y
sucesor. La vista de firmas pasa de tres preguntas realmente abiertas
(`FP-361`, `FP-363`, `FP-371`) a una (`FP-371`): las dos primeras ya están
decididas y su ejecución sigue visible como `NC-0065`/`NC-0064`. `FP-314`
queda firmada por D17 y su cartera no ejecutada continúa como `NC-0151`.

El universo NC pasa de 82 a 69 filas `ABIERTA`: se cierran catorce obligaciones
acreditadas y nace un residual de ejecución; las obligaciones S6/S12 reutilizan
NC-0065/0064. No se borró ninguna
obligación por el solo hecho de decidirla.

## Conciliación antes/después

| objeto | antes | después | evidencia / residual |
|---|---|---|---|
| FP-234 | GATED | EJECUTADA | F-DD v1.1 de MAESTRA35-N2 + levantamiento `d2` documentado por MAESTRA36-N2; no firma el EE/IC aproximado |
| FP-314 | pendiente de firma | FIRMADA | D17; ejecución en NC-0151/ENCARGO-E09 |
| FP-361 | ABIERTA | FIRMADA | D13 A; ejecución documental en NC-0065/ENCARGO-E06 |
| FP-363 | ABIERTA | FIRMADA | D14 B; cálculo sucesor en NC-0064/ENCARGO-E07 |
| FP-371 | ABIERTA | ABIERTA | benchmark D16 cumplido; tratamiento inferencial concreto aún requiere ENCARGO-E09/ENCARGO-E11 y firma |
| NC-0018 | ABIERTA | CERRADA | 14/14 CALC-R vigentes; no adopción al motor |
| NC-0019 | ABIERTA | CERRADA | corredor sucesor v1.3 ejecutó 224 posiciones; no se afirma ejecución v1.2; NC-0146 conserva el problema científico |
| NC-0029 | ABIERTA | ABIERTA | residuales separados: ENCARGO-E03 (L) y ENCARGO-E04 (motor/adopciones) |
| NC-0032 | ABIERTA | CERRADA | commits reales `f0f6bb7` (9/sep) y `fe5d131` (10/sep); no prueba cron continuo |
| NC-0037 | ABIERTA | ABIERTA | D17/D18: ENCARGO-E09 académica/pública; comercial diferida |
| NC-0040 | ABIERTA | CERRADA | `rutinas.tsv` trae PR `[REVISA]` y comentarios `MM-REVISA:v2` corroborados por API |
| NC-0041 | ABIERTA | CERRADA | D20: relectura acotada de #621 bajo RUTINAS-2 P1; veredicto histórico intacto |
| NC-0043 | ABIERTA | ABIERTA | decisión D15 asentada; corrección documental ENCARGO-E06 pendiente |
| NC-0063/0071 | ABIERTA | CERRADA | `CALC-0003-v4 cuenta_gen2=SI` ya existe en `decisiones.tsv` |
| NC-0067 | ABIERTA | CERRADA | T-YAMEDIDO usa UTC y `t30b` prueba el cambio de día |
| NC-0085 | ABIERTA | ABIERTA | benchmark D11 registrado; aplicación RES-0028 pendiente ENCARGO-E11 |
| NC-0087/0093/0101 | ABIERTA | ABIERTA | D12 asentada; serie ENCARGO-E08 y adquisición sólo de faltantes ENCARGO-E09 |
| NC-0089 | ABIERTA | CERRADA | decisiones D13/D14 asentadas; ejecuciones siguen en NC-0065/0064 |
| NC-0092/0102 | ABIERTA | CERRADA | CALC-TRIADA-0001 consume los R por identidad; no adopta al motor |
| NC-0095 | ABIERTA | CERRADA | FP-370 ejecutada; codificación R sucesora sellada |
| NC-0103 | ABIERTA | CERRADA | asiento añadido para CALC-R-CIV-M-01/02/04 desde sus firmas de spec |
| NC-0104 | ABIERTA | ABIERTA | faltan comprobante VERIFY-ESTRUCTURADO y derivación efectiva de fuentes/vistas |
| NC-0132 | ABIERTA | CERRADA | ADR-441 y rótulo ENIF reconciliados en canon |
| NC-0140/0145 | CERRADA | CERRADA | se citan; ningún replay/cascada duplicado |
| NC-0146/0147 | ABIERTA | ABIERTA | D01/D02 asentadas; ejecución ENCARGO-E02→ENCARGO-E03 pendiente |

## D20 · alcance exacto

La revisión histórica es del fundamento temporal de PR #621 sobre #619, no de
GEN1 ni de la antigüedad de datos científicos. Las observaciones se evalúan en
la fecha y SHA donde se produjeron; un cambio posterior de main no las vuelve
falsas. Una huella histórica se conserva y una compuerta vigente se rederiva
antes de actuar. La comprobación inmediatamente antes de escribir ya vive en
`.claude/commands/despacha.md` §7-pre. No se reabre ni modifica ninguno de los
dos PR y no se generaliza el resultado a una auditoría histórica completa.

## Asientos y anexos

- `data/corrida0/decisiones.tsv`: 20 objetos D01–D20 y tres asientos
  `cuenta_gen2=SI` de CIV-M-01/02/04. D21 no aparece.
- Benchmark D11: investigación cerrada; adopción RES-0028 abierta.
- Benchmark D16: investigación cerrada; FP-371 abierta.
- Originales externos acreditados por los hashes registrados en el A.3.

## Lo que no se ejecutó

No se ejecutó ENCARGO-E02–ENCARGO-E11, no se abrió microdato, no hubo llamadas a modelos, no se
modificó el motor, no se compraron datos y no se tocó el scheduler de la caja.
Las 69 NC abiertas conservan obligaciones reales; este acto sólo cambió sus
preguntas de decisión por instrucciones ejecutables cuando mesa ya decidió.

## Validación

- Pruebas dirigidas del digesto/estado: `test_digesto_nc.py` (21/21),
  `test_digesto_candidatas.py`, `test_digesto_mesa.py` (10/10),
  `test_digesto_fecha.py` y `test_estado_comun.py` (6/6), todas en verde.
- `python3 tests/check.py --baseline`: línea base **VERDE**, cero entradas nuevas;
  permanecen 3 FAIL y 2203 WARN heredados por el baseline, sin modificarlo.
- `git diff --check`: limpio. `cierre_acto.py --sin-suite`: 454 ADR en las tres
  superficies, rótulo presente, una sola FP abierta (`FP-371`) y cero NC
  huérfanas. `## CONSUMIDO` se completa con la identidad del PR.
- Vista puntual de mesa: `NC-0103` y `FP-361` aparecen como «Ya resuelto —
  presentación, no re-preguntar». Conteo final: 69 NC abiertas y 75 cerradas.
- `tools/corrida0.py registro` se ejecutó sólo en dry-run: propuso 35
  transiciones en `corridas.tsv` por contexto de replay y ninguna diferencia en
  `resultados.tsv`/`usos.tsv`. No se aplicó: no sustituye el
  `VERIFY-ESTRUCTURADO` ni la derivación efectiva exigidos por `NC-0104`.
