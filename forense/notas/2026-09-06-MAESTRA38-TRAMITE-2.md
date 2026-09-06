# ACTO MAESTRA38-TRAMITE-2 · FIRMAS-DE-HOY-Y-ADQUIERE — 6/sep/2026

Trámite: recibos y propagación de firmas ya tomadas en conversación de
dirección (mesa, 6/sep). Sin decisión propia — firma verbatim de mesa que
rige el mecanismo: «Si hay decisiones que tomar las revisamos en la
conversación primero tú y yo y luego los encargos salen con todo decidido
mi firma es el merge del PR».

## A.8 al arrancar — medido, no supuesto

```
awk -F'\t' '$6 ~ /^ABIERTA/{print $1}' forense/firmas-pendientes.tsv
```
→ `FP-263, FP-288, FP-303, FP-316, FP-317, FP-323, FP-324` (7 filas, no 10:
`FP-314` está en estado `PENDIENTE DE FIRMA`, `FP-315` y `FP-325` en
`RECIBO` — ninguna de las tres arranca con `ABIERTA`. El encargo asumía 10;
la medición real trae 7. Se anota la discrepancia y se procede sobre los
ids nombrados explícitamente por el encargo, que no dependen de este
conteo.)

```
grep -n -iE "TLS|nginx|403|mantenimiento" .claude/commands/adquiere.md
```
→ 2 líneas antes de este acto (l.126, l.191), ninguna regla de cierre —
confirmado.

```
grep -c "APIPIE" forense/hallazgos.md
```
→ 0 — confirmado, no se duplica (la línea la pone C1, no este acto).

## Filas que cambiaron en `forense/firmas-pendientes.tsv` y por qué

- **FP-323** → `CERRADA-RECIBO`, `firmada_en` = este PR. Recibo puro de
  ACTO MAESTRA38-CRON-3, sin decisión pendiente.
- **FP-325** → `CERRADA-RECIBO`, `firmada_en` = este PR. Recibo puro de
  ACTO MAESTRA38-CRON . DIAGNOSTICO-Y-ARREGLO.
- **FP-317** → `FIRMADA`, `firmada_en` = «A.7: `list::mexico` hermana de
  `ICPSR_35024`, no fusionada — firma de mesa por merge de
  MAESTRA38-TRAMITE-2, 6/sep». Decisión de dirección propuesta en
  conversación y no objetada por mesa; lanzar este encargo la firma.
- **FP-324** → `FIRMADA-PARCIAL`: (1) la regla nueva (fallo de TLS no es
  evidencia sobre el acceso) y (2) el cambio de `PI` de `NO-ACCESIBLE` a
  `NO-OBTENIDO-POR-ESTE-AGENTE` quedan firmadas aquí, en `/adquiere`; (3)
  las 5 recetas de PAQUETE-RECETAS-11 siguen abiertas como acción de mesa
  — se anota en la misma fila (T-FIRMAS no exige una fila por sub-decisión;
  no se abre fila nueva).
- **FP-314** → `nota` en `estado` gana: «prioridad alta, mesa 7–8/sep; #1
  ICPSR paquete Data convierte L2 en MEDICIÓN — firma verbatim 6/sep:
  "Necesito registrar la opción 2 como pendiente de alta prioridad, lo
  haría mañana o pasado mañana"».
- **FP-316** y **FP-315** → `nota` en `estado` gana: «decisión propuesta
  por dirección 6/sep; se ejecuta en MAESTRA38-CARGA-LAPOP; lanzarlo la
  firma».

## `.claude/commands/adquiere.md` §3

Párrafo nuevo, «Cuatro cosas que no son evidencia de inaccesibilidad
(medidas, no supuestas)», con las cuatro medidas de A4/A6 y su nota de
origen citada por ruta (`forense/notas/2026-09-06-MAESTRA38-A4-resultados.md`
para (i)-(iii); `forense/notas/2026-09-06-MAESTRA38-A6-resultados.md` para
(iv)). Repo-side: no hay copia en el proyecto que sincronizar (A.9 no
aplica) y no entra a `instrucciones-proyecto` (v2.3: la skill ya es el
vehículo).

## Suite

`tests/check.py --baseline` → LÍNEA BASE: VERDE, 3 FAIL / 171 WARN, nada
nuevo frente a `tests/baseline.json`. `T-FIRMAS-2` sigue en verde: ninguna
ranura nueva sin fila (las siete filas tocadas ya existían).

## Contador

Filas `ABIERTA`: 7 → 4 (`FP-323`, `FP-325` cerradas; `FP-317` firmada; las
que quedan: `FP-263`, `FP-288`, `FP-303`, `FP-316` — `FP-324` pasa a
`FIRMADA-PARCIAL`, no a `ABIERTA`). Reglas de cierre en `/adquiere`: 0 → 4.
Medición: cero.
