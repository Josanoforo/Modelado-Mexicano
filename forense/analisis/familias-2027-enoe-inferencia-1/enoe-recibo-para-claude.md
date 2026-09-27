# Recibo para Claude · ASTRA6-C2-ENOE-INFERENCIA-1

Solicitud de recepción independiente por circuito de mesa en el PR propio. Recibo NO OBTENIDO. Propuesta de contenido FP-260927-GEN2-ASTRA6-C2-ENOE-INFERENCIA-1-310e-01; fusión/adopción sólo mesa.

EJECUTADO: producto recomendado NO-LANZAR-TODAVIA por incertidumbre no identificada del oro2024T4, con solicitud específica para decidir. Revisar enoe-hoja-decision.md, receta-humana.md, documentacion/fuentes.md y fuentes.json, diagnostico/enoe-auditoria.json y diagnostico.md, potencia/enoe-potencia-resultados.json y escenarios.tsv. Hashes entregables en enoe-producto.sha256; hashes de insumos consumidos en resultados de potencia. Fuente única tanda4 y acta propia; firma citada sin duplicación. Preparación informada/no ciega.

EJECUTADO: mismo ID enoe_2024_4t_microdatos, sólo ENOE_SDEMT424.csv; ZIP verificado antes de leer. No ola nueva, reservada o futura. Los puntos históricos y objetos frontera-1 se conservan. Sólo agregados por estrato/grupo; sin código UPM ni identificadores personales en PR. Scripts propios bajo tools/familias-2027/enoe_inferencia_1/. Documentos públicos se fijan por URL/fecha/hash, PDFs fuera del PR.

Comandos reproducibles desde raíz del worktree en CAJA:

```bash
python3 tools/familias-2027/enoe_inferencia_1/enoe_diagnostico.py --oro data/raw/enoe_microdatos_post2019/enoe_2024_trim4_csv.zip --salida /tmp/enoe-auditoria-replay.json
cmp /tmp/enoe-auditoria-replay.json forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/enoe-auditoria.json
python3 tools/familias-2027/enoe_inferencia_1/prueba_sintetica.py
python3 forense/analisis/familias-2027-enoe-inferencia-1/potencia/test_sucesor.py
python3 forense/analisis/familias-2027-frontera-1/potencia/frontera_test_potencia.py
python3 forense/analisis/familias-2027-enoe-inferencia-1/potencia/calcula_sucesor.py --diagnostico forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/enoe-auditoria.json
sha256sum -c forense/analisis/familias-2027-enoe-inferencia-1/enoe-producto.sha256
python3 tests/check.py --rapido --baseline
python3 tools/cierre_acto.py --sin-suite --encargo forense/encargos/2026-09-27-ASTRA6-C2-ENOE-INFERENCIA-1-ACTA-EJECUCION.md
```

EJECUTADO: sintéticos y once pruebas de potencia pasan; replay coincide. Gate final y límites de verificación en enoe-gate-final.txt y enoe-cierre.md. La potencia completa es no calculable: se entregan seis filas null y NO-LANZAR, no un número obtenido de varianza parcial. La certeza sintética sólo demuestra un componente en diseño artificial de una etapa.

PROPUESTO: mantener no lanzamiento, solicitar a INEGI estructura de selección/crosswalk de UPM y regla singleton/certeza o réplicas oficiales compatibles. Revisar el supuesto de unidades UPM reutilizadas entre estratos antes de atribuir independencia física. No escoger colapso por mejorar potencia.

NO-VERIFICADO: revisión independiente, adopción y recibo; acierto futuro; regla oficial para singleton y códigos UPM repetidos. No se solicitan ni conceden automáticamente apertura, COMMIT-3 o cambio de bandas. La solicitud documental está redactada; no se ha enviado a terceros.

Entrega: [PR#1222](https://github.com/Josanoforo/Modelado-Mexicano/pull/1222); recepción independiente solicitada en su cuerpo, no obtenida.
