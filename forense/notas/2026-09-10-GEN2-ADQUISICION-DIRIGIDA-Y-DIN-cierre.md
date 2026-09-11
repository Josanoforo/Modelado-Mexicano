# ACTO GEN2-ADQUISICION-DIRIGIDA-Y-DIN · cierre

Fecha: 10 de septiembre de 2026. Rama:
`acto/gen2-adquisicion-dirigida`. PR: `#693`.

## Resultado útil en cinco líneas

1. Se incorporaron tres documentos públicos útiles y verificables: la versión
   de autor Bauchet 2012, Campos 1998 y BANSEFI–PATMIR 2006.
2. Los tres payloads viven fuera de Git bajo la raíz configurada `data_raw` y
   el manifiesto canónico conserva ruta, URL, fecha, hash, tamaño y condición.
3. La búsqueda de tandas abre medición mexicana de participación, selección,
   montos, frecuencia y mecanismos; no fabrica una tasa de incumplimiento.
4. ENAFIN ya satisface N19 y WBES/ENVIPE ya estaban adquiridos; ICPSR, OECD,
   Reuters, ENJUVE y el binario SSRN 2014 quedan como accesos personales.
5. DIN-M-01 conserva su punto descriptivo, pero constante + `folio` se rechaza
   como *ground truth* inferencial mientras no haya diseño oficial ejecutable.

## Fases realizadas y pendientes

- Fase 0, completa: identidad y utilidad separadas por objeto; F5 actualizado
  tras incorporar `origin/main`/PR #687.
- Fase 1, parcial por barrera externa: tres descargas públicas ejecutadas;
  expedientes personales precisados sin fingir envío ni recepción.
- Fase 2, completa: ruta académica mexicana priorizada, variables, población,
  acceso, paso de medición y descartes documentados.
- Fase 3, completa hasta la barrera oficial: joins, pesos y diseño auditados;
  solicitud de réplica/servicio de varianza preparada, no enviada.
- Fase 4, completa para el perímetro ejecutable: manifiesto, registro canónico,
  vista, FP/NC y recibos actualizados. Pendiente sólo la acción del titular o
  una respuesta de tercero en `NC-0151`, y la decisión de mesa en `FP-371`.

## Decisión y contador

Se recomienda a mesa **rechazar** constante + `folio` como verdad inferencial
de DIN-M-01. El punto `0.15558094338412926` sigue siendo descriptivo; SRS y
constante + `folio` sólo son sensibilidades sin dirección garantizada. No nace
un `CALC`, no se adopta un parámetro y el contador de mediciones GEN2 es cero.

## Pruebas

- `tests/manifiesto.py --verifica` sobre los tres IDs: `3/3 COINCIDE`.
- `tests/test_cola_writer.py`: `5/5 OK`.
- `tests/test_manifiesto_seguro.py`: `4/4 OK`.
- Registro/vista: 139 filas y reproducción byte-exacta.
- `tests/check.py --baseline`: `LÍNEA BASE: VERDE`; 3 fallos y 2 264 avisos
  heredados, cero entradas nuevas.

## Obligaciones

| obligación | evidencia | cerrada/residual | siguiente acción |
|---|---|---|---|
| adquisición pública y recibos | `data/manifiesto.yaml`; notas de cartera y tandas | cerrada para los tres objetos obtenidos | consumir por ID de manifiesto, sin copiar el payload a Git |
| cartera D17/FP-314 | nota de cartera; `NC-0151` | residual personal/institucional | titular tramita DUA, formulario y solicitudes; registra comprobante/archivo al recibir |
| evidencia mexicana de tandas | nota de tandas; Campos 1998; BANSEFI 2006; ENNViH | ruta académica cerrada; `NC-0037` residual sin ledger | medir variables propuestas; no interpretar abandono como impago |
| diseño DIN-M-01 | nota DIN; `data/diseno-muestral.yaml`; `FP-371` | residual de decisión y productor | mesa rechaza/autoriza uso; titular envía solicitud oficial si requiere inferencia |
| registro y vistas | cola canónica, vista, FP y NC | cerrada | mantener la cola derivada desde su SSOT |

No se ejecutó compra, negociación comercial, envío externo, aceptación de DUA,
suplantación de identidad, cálculo sucesor ni adopción al motor.
