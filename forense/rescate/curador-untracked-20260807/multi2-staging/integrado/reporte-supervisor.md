# Reporte supervisor Multi2

- Integración aceptada: `true`.
- Modo real: `parallel_subagents`; tres workers arrancaron simultáneamente y el cuarto al liberarse una ranura.
- Candidatas inspeccionadas: 157/157, pertenecientes a 71 fuentes asignadas una sola vez.
- Cambios aceptados: 10, todos `CANDIDATA → NEGATIVA` con referencia local y localizador verificados.
- Candidatas restantes: 147, cada una con carencia, incertidumbre y siguiente acción.
- Errores de integración, conflictos y decisiones humanas: 0/0/0.

## Resultado sustantivo

Las negativas nuevas delimitan diez usos que no satisfacen la relación pedida: orientación futura ENSAFI sin desenlace G4; confianza ENCUCI sin outcome financiero común; seguro ENVIPE restringido a robo total de vehículo; préstamo familiar ENFIH como liquidez de emergencia y no disposición general; corpus Brasdefer sin microdato/replicación requerida; ECCO sin frecuencia conductual ni panel de desempeño; ACLED local agregado mes×año; y SICS agregado nacional×año sin comité ni sanción.

No hubo confirmaciones nuevas. Siguen utilizables las cuatro mediciones ya confirmadas: apoyo familiar ENBIARE (PB2_1), obligación familiar ENASIC (P7_12_7, dos identidades del universo), y puente confianza×dificultad económica ENBIARE (PB1_01/02 con PF1_1..6).

Además, tres negativas conservan mediciones parciales útiles fuera de la relación completa: AP5_1_1/2/3 de ENCUCI para confianza; BP2_1 de ENVIPE para seguro en robo total de vehículo; y P11_1_5 de ENFIH para capacidad de financiar una urgencia mediante préstamo familiar.

## Bloqueos

Se registraron 16 bloqueos concretos. Predominan payload/codebook no disponible localmente, documentos con acceso aún no abierto y columnas derivadas sin texto/codificación (`IMPULSIVID`, `CONF_FINAN`). No se convirtieron en negativas. Las acciones siguientes están individualizadas en `pendientes-siguiente-accion.tsv`.

## Conservación

El registro mantiene exactamente 200 claves semánticas activas y separa 111 artefactos rechazados. No desapareció ninguna negativa, no se tocó ningún estado protegido y no hubo narrowing.
