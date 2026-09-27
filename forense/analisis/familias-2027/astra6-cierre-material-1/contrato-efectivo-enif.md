# Contrato efectivo ENIF · sucesor de alcance

LEÍDO en el corte de arranque y verificado por hashes del inventario portable: para la futura serialización gobierna `tools/familias-2027/enif/contrato-futuro-serializacion-v2.yaml`, función `medir_futuro` en `lector-futuro-serializacion-v2.py`. Su autorización existente es la ADENDA-1 de ENIF; no es autorización de apertura. Los hashes exactos están en inventario-portable.json y hoja-comun.json.

`contrato-futuro.yaml` y `lector.py` se conservan como antecedentes SUSTITUIDOS-EN-ALCANCE respecto del transporte de D-K al conducto. No se editan. El contrato v1 emitía JSON largo; el v2 emite REF a dos tablas propias y declara nulos. Se mantiene estimando, universo, ponderadores, piso, banda, semilla y remuestreo. El ORO-0001 rechazado por el conducto continúa como antecedente sin ejecución sellada; ORO-0002 es el oro efectivo autorizado. No ejecutar run del antecedente.

EJECUTADO: auditoría por identidad del v2 y del medidor ORO-0002, más prueba de I/O exacto y salidas sintéticas por `_fallas_run` de corrida0 (incluye REF, hash y nulos). El código estadístico original sigue byte a byte en su identidad de Git. La auditoría anterior no cubría estos dos archivos.

PROPUESTO-POR-EJECUTOR: aplicar el control de rutas sucesor descrito en adenda-auditoria-propuesta.md al conducto de apertura. Esta nueva envoltura de control requiere aprobación independiente antes de su uso material en COMMIT-3. Los sintéticos no autorizan apertura. Hasta autorización de ola, comparabilidad, soporte y aprobación de la envoltura, el COMMIT-3 permanece cerrado.
