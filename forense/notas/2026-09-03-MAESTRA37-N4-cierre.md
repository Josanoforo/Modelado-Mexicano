# MAESTRA37-N4 · TRÁMITE-L1-LETRAS-Y-ALIAS — cierre

Acto de trámite mecánico: propaga firmas de mesa ya tomadas, no decide nada
nuevo.

## Qué se propagó

- **D8** (`FP-268`) — mesa: mantener el criterio 2 como está (`ADR-265`,
  firma 9) y re-evaluar salud tras `MAESTRA37-L3`. Ningún texto del canon se
  toca. `FP-268 → FIRMADA`.
- **D9** (`FP-267`) — mesa: una fuente administrativa que mide desenlace Y
  disparador cuenta para (ii) del criterio 2; (i) no se toca. Ejecutado como
  enmienda append-only al criterio 2 en
  `canon/motor-nucleo-medible-v1_0.md` §3.a, citando `ADR-318` como
  procedimiento. `FP-267 → FIRMADA · EJECUTADA`.
- **D10** (`FP-273`) — mesa, benchmark de dirección (3/sep/2026, tres
  fuentes, resumido): (1) el indicador de uso de gobierno digital que la
  OCDE publica (Going Digital, «share of individuals using the Internet to
  interact with public authorities») es de ENCUESTA a personas, no de stock
  de credenciales; (2) los reportes OCDE/G20 sobre identidad digital
  distinguen «adopción entre la población» (inscritos) de uso efectivo, y
  tratan la inscripción como cobertura de infraestructura, no como
  conducta; (3) la e.firma tiene vigencia y renovación (RMF 2026, Anexo 2:
  «e.firma la Firma Electrónica Avanzada que debe estar vigente»), así que
  un acumulado de primeros certificados 2004-2025 cuenta credenciales
  vencidas y titulares inactivos: es cota superior del stock, y el stock no
  es adopción del servicio. Letra: conservar p asignado (0.91/0.09), tier
  MEDIA y campo_administrativo visible con rótulo `COBERTURA-CREDENCIAL ·
  COTA-SUPERIOR`, no adopción; el comparable honesto del 0.09 sigue siendo
  uso reportado por persona con denominador de obligación, que ninguna
  fuente del corpus tiene (`ADR-299`). `FP-273 → FIRMADA`, no
  `REFUTADA-CON-RESERVA`.
- **D11** (`FP-274`) — mesa: renombrar el alias del curador que colisionaba
  con `EXT-OF-05` (SESNA). Ejecutado: `EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI`
  → `DGIS_URGENCIAS_CUBO_IMSS_INEGI` en
  `data/curacion-registro/{relaciones,evidencias,utilidad-modelo,cola-adquisicion-registro}.tsv`.
  `FP-274 → FIRMADA · EJECUTADA`.
- **Enterados por merge, sin más acción**: `FP-271` (recibo de
  `MAESTRA37-L1`), `FP-272` (recibo de `MAESTRA37-N2`), `FP-275` (recibo de
  `MAESTRA37-N3`) → `FIRMADA`.
- `FP-276` — fila nueva, recibo de este propio trámite.

## Qué se renombró

Alias del curador `EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI` →
`DGIS_URGENCIAS_CUBO_IMSS_INEGI` (colisión con `EXT-OF-05`/SESNA registrada
en `FP-274`, `hallazgos.md:614` y sig.). Archivos tocados por el renombre:
`data/curacion-registro/relaciones.tsv` (filas `REL-814040652b29189344a6dc4c`,
`REL-b4c434431bd19bbf369d322d` — los `relacion_id` se re-derivaron con
`tools/curador_registro/baseline.py:relacion_id()` porque cambiar la
`fuente_canonica_normalizada` que participa en su terna hace que el
`relacion_id` original ya no sea determinista; los nuevos ids son
`REL-78d3eaddcfc8a517125b409d` y `REL-52ba7751632b1b331b5758d0`),
`evidencias.tsv`, `utilidad-modelo.tsv` (mismos dos `relacion_id`
propagados como llave foránea) y `cola-adquisicion-registro.tsv`
(`EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI` → `DGIS_URGENCIAS_CUBO_IMSS_INEGI`
en la fila 64, id de fila). `data/cola-adquisicion-v1_0.tsv` se
**regeneró** con `tools/vista_cola_adquisicion.py` (vista derivada, no
editada a mano) para que quede consistente con el registro. `aliases-fuentes.tsv`
no traía el alias — no se le agregó fila nueva, sólo se ejecutó el
renombre. `data/manifiesto.yaml` y el resto de citas históricas en
`forense/notas/**`, `forense/encargos/**` y `canon/gobernanza-v1_15.md`
quedan **fuera de perímetro** (append-only histórico / manifiesto
prohibido) y conservan el nombre antiguo — quien las lea después sabe, por
esta nota, que `EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI` y
`DGIS_URGENCIAS_CUBO_IMSS_INEGI` son el mismo objeto.

`data/curacion-registro/baseline.json` se recifró con
`tools/curador_registro/sync_bootstrap._freeze_manifest` (no a mano):
`python3 tools/curador_registro/baseline.py data/curacion-registro` →
`"ok": true, "errores": []`.

## Qué quedó en VERDE

- `python3 tools/curador_registro/baseline.py data/curacion-registro` →
  `{"ok": true, "errores": []}`.
- `python3 tests/check.py --baseline` → `LÍNEA BASE: VERDE — nada nuevo
  frente a tests/baseline.json`, 19 FAIL (sin cambio frente a la línea
  base heredada; ninguno de los 19 lo introduce este acto).
- Round-trip de `forense/firmas-pendientes.tsv`: de las 267 líneas
  originales, sólo las 7 filas (`FP-267/268/271/272/273/274/275`)
  cambiaron; el resto, 0 diferencias byte a byte contra `HEAD`; se agregó
  1 línea nueva (`FP-276`), total 268.
- Round-trip de los cuatro TSV del curador tocados por D11: en cada uno,
  sólo las líneas que contenían el alias viejo o los dos `relacion_id`
  afectados cambiaron; 0 diferencias en el resto.

## Contador final

firmas propagadas 7 · alias colisionados 1 → 0 · encargos sin `##
CONSUMIDO` 1 → 0 · dominios abiertos 0 → 0 · cargas al motor 0 · medición
de modelo: cero directo, declarado.
