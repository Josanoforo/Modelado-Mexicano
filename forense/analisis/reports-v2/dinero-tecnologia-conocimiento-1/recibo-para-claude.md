# Recibo solicitado · dinero, tecnología y conocimiento

Solicito recibo técnico por el circuito de mesa del PR, sin mensajes externos. No se afirma que exista revisión independiente ni aceptación de estos productos.

Objetos: los tres homónimos en corpus/reports-v2 y las carpetas dinero/, tecnologia/ y conocimiento/. `indice-local.md` y `resumen-lote.json` derivan cobertura/dictámenes desde decisiones editoriales explícitas; `hashes-producto.json` conserva SHA-256 de cada objeto por pieza. Encargo original archivado por #1191, commit 9df094900, verificado idéntico al recibido; su hash y los adjuntos constan en `adjuntos-verificados.json`.

Comandos desde la raíz del repositorio:

```sh
python3 forense/analisis/reports-v2/dinero-tecnologia-conocimiento-1/verifica_lote.py
python3 forense/analisis/reports-v2/dinero-tecnologia-conocimiento-1/verifica_lote.py --check
python3 forense/analisis/reports-v2/dinero-tecnologia-conocimiento-1/verifica_lote.py --self-test
python3 tests/check.py --rapido --baseline
```

Revisión solicitada: todas las ROMPE, cifras centrales/unidades/denominadores, separación de frecuencia y mecanismo, fuentes primarias efectivamente leídas y límites de comparación. Las cifras selladas no adoptadas solo pueden presentarse provisionales; ninguna vetada se usa como piso. Revisar dependencias de C1 por llave/alias/linaje y la declaración de vistas atrasadas.

Reservas: no se abrieron microdatos ni resultados futuros/reservados; el dato externo tiene alcance propio, nunca RESULT ficticio. Coincidencia numérica, validez del estimando, adopción y predicción son preguntas distintas. C1 no bloquea la reescritura, y un hallazgo material posterior exige corregir solo el contenido afectado. Reglas de `hoja-para-mesa.md` PROPUESTO-POR-EJECUTOR; no se adoptan ni se modifica el motor.

EJECUTADO/LEÍDO y resultados verificables: ver `nota-cierre.md`, `verificaciones.md` y productos por pieza. PROPUESTO: recepción editorial y consideración futura de reglas. Pendiente: recibo independiente y decisión de mesa.
