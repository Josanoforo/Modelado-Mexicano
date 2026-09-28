# Recibo solicitado · ASTRA6-C3-AUTORIDAD-CIVISMO-COMUNALIDAD-1

Solicito recibo técnico por el circuito de mesa del [PR #1240](https://github.com/Josanoforo/Modelado-Mexicano/pull/1240). Esta solicitud no acredita que Claude haya revisado o aceptado los reports.

**Objetos.** Tres homónimos exactos de Autoridad, Civismo y Comunalidad en `corpus/reports-v2/`; expedientes `autoridad/`, `civismo/`, `comunalidad/` y archivos comunes de este lote. [Índice](indice-local.md), [resumen derivado](resumen-lote.json), [hashes SHA-256](hashes-producto.json), [cierre](cierre.md) y [hoja para mesa](hoja-firma.md). El encargo original tiene cuerpo inalterado en el archivo canónico de tanda5 (#1237); el 0-bis propio `3a1f0be1` conserva los mismos bytes en historial. El manifiesto de tanda5 fija el SHA crudo antes del pie de consumo.

La continuación `ASTRA6-C3-CIERRE-1240-1` está archivada en `forense/encargos/2026-09-27-ASTRA6-C3-CIERRE-1240-1.md` (0-bis `28d69156`; SHA crudo del cuerpo recibido `99b3d6d4c09d85f1132c31a7b20afc9712a055e39a6b95ecf3e1fef7bd6cca27`). Su cierre añade la interpretación de las premisas vencidas y la revisión dirigida, sin duplicar los objetos editoriales.

**Comandos desde raíz del repositorio:**

```sh
python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/autoridad/verifica.py
python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/civismo/verificar.py
python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/comunalidad/verifica.py
python3 forense/analisis/reports-v2/autoridad-civismo-comunalidad-1/verifica_lote.py --check
python3 tests/check.py --baseline --parallel
```

**Revisión solicitada.** Cobertura de las 122 filas de mapa y las 57 unidades/desdobles añadidos; cada ROMPE y su evidencia contraria específica; relaciones prosa–tabla; las dos cifras RESULT provisionales de Civismo, decisión del momento 08 en `decisiones.tsv:292` y ausencia de validación independiente; alcance del portal IEEPCO; denominadores de participación electoral; distinción entre autoridad formal, voz efectiva y mecanismo psicológico. Verificar que el texto usa literatura según lectura real (texto íntegro, pasaje o resumen) y no traslada muestras urbanas, organizacionales o de diáspora a todo México.

**Estados.** EJECUTADO: reportes, tablas, productores, controles locales y archivo del encargo. LEÍDO: originales y fuentes según expedientes. PROPUESTO: recepción editorial y reglas SI–ENTONCES para posible consumidor posterior. NO-VERIFICADO: mecanismos causales, cifras históricas sin contrato, recibo independiente y firma de contenido. Cero apertura de olas reservadas, nuevas corridas o adopciones.

**Gate ejecutado.** `tests/check.py --baseline --parallel` exit 0, LÍNEA BASE VERDE sin FAIL nuevos; salida y demás controles en [verificaciones](verificaciones.md). Los tres FAIL absolutos son heredados y el gate los compara con baseline; 151 WARN nuevos se listan como estado, sin rutas propias en ese listado. Este resultado no equivale a recibo sustantivo independiente.
