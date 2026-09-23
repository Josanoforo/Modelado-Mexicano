# Recibo Codex para Claude · ASTRA5-U3-POLITICA

**PR #1084:** https://github.com/Josanoforo/Modelado-Mexicano/pull/1084
**Rama:** `codex/astra5-politica-1`. Base inicial fijada `8e41f72`; se
incorporó `origin/main` @ `1abcc934` antes del push. Mesa conserva la firma
de fusión y adopción; este PR no se fusionó desde CAJA.

## Entrega material

- Encargo archivado verbatim en
  `forense/encargos/2026-09-23-ASTRA5-U3-POLITICA.md`; SHA256 de cuerpo
  `bc255836ca9e8ed7a32c578961e302d99a79e7b855eb809ba4863660aa6bc679`.
- Tres tablas y auditoría en
  `forense/analisis/dominios/politica/RESULTADOS-ASTRA5-U3.md`;
  clasificación razonada de los 45 IDs `ine_*` en el TSV adyacente.
- INE: `CALC-INE-PISOS-2024-0001`, `RESULT-INE-PISOS-2024-TABLA`, SHA256
  `5d5e0ce5bef544457e4c49f34a92b08672c692bf20b83f932b6db44a6da068ca`.
  Son marcas administrativas en lista nominal; sin IC de muestreo.
- ENCUP: `CALC-ENCUP-PISOS-2012-0003`, `RESULT-ENCUP-PISOS-2012-TABLA`,
  SHA256 `417560d3947963b842e7569cbec23028069fa0bf0129324216a9f673fe6a64e2`.
  Son descriptivos entre respuestas válidas, sin peso/diseño acreditado.
- LAPOP: `CALC-LAPOP-PISOS-2019-0001`, `RESULT-LAPOP-PISOS-2019-TABLA`,
  SHA256 `40ecdc8e1f0b2228d357aea0b0284bcf18d97eddc8058831cfd95f4c78008f1f`.
  Puntos e IC bootstrap de UPM en cuatro estratos; oferta declarada no
  identifica recepción ni efecto causal sobre voto.
- Los tres CALC activos llevan `cuenta_gen2: SI`, `adopta: NO`, sello y
  asiento REAL `REPRODUCE` / `IDENTICO` en `forense/replay-evidencia.tsv`.
  Specs y medidores tuvieron COMMIT-1 anterior a abrir raw; ejecución,
  sello y verify figuran en COMMIT-2. La primera salida adversa ENCUP `0002`
  quedó preservada en
  `forense/historico/ASTRA5-U3-POLITICA/CALC-ENCUP-PISOS-2012-0002.tar`,
  SHA256 `17f1121fb33b43e2b2b40d0607b00ca880eb7ea1831116e7b0e00a6dd6648213`,
  con sello idéntico tras extracción.

## Estado operativo

Cuatro pruebas dirigidas pasaron. `check.py --rapido` dejó T02 y sidecars
conformes. `check.py --baseline` fue VERDE antes y después del merge; la
corrida posterior terminó con exit code 0, 3 FAIL heredados y 62 440 WARN.
`corrida0 status --json` derivó sin error. Las vistas
globales no se escribieron en esta rama: los CALC están **sellados en disco,
no registrados** hasta el job de `main`.

`NC-260923-ASTRA5-U3-POLITICA-df0d-01` se cerró. Siguen abiertas `-02`
(descriptor de diseño ENCUP: conseguir peso, estrato y UPM antes de IC
poblacional), `-03` (dictamen de equivalencia LAPOP por ola antes de serie)
y `-04` (publicación de vistas vía `verify.yml` al fusionar). Tres FP
corresponden a INE, ENCUP y LAPOP. No se abrieron ENCO, ENVIPE 2026, última
ola ENOE ni otra reserva explícita. `celdas_validadas` quedó intacto.

**Siguiente operación de mesa:** revisar y, si procede, fusionar PR #1084;
comprobar el job de publicación y cerrar NC `-04` sólo cuando la vista
incluya los tres asientos. Resolver `-02` y `-03` en mediciones sucesoras,
sin reescribir los resultados sellados.
