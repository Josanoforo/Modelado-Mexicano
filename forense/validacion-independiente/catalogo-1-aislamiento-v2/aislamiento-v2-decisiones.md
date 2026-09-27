# Disposición y decisión de recepción

PROPUESTO-POR-EJECUTOR. Recibir el lanzador portable y el adaptador v2 como
producto de preparación. Mantener **NO-LANZAR-COMO-CIEGA** en este entorno:
`bwrap: loopback: Failed to create NETLINK_ROUTE socket: Operation not permitted`.
No se elevan privilegios ni se cambia configuración compartida para superar
esa prueba. La alternativa es esperar un entorno con namespaces disponibles;
no mejora el producto portable y por eso no detiene su entrega.

EJECUTADO: `disposicion.py` deriva la hoja por paquete desde la entrega de
#1203 y la prueba de entorno. La fuente y la prueba tienen hashes en
`disposicion-por-paquete.json`. Es una disposición documental; no abre los
contenedores ni microdatos, y no acredita aptitud de un paquete real.

LEÍDO: las propuestas
`FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-01` (ENDIREH2021) y
`FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-02` (ENDIREH2016)
siguen ABIERTA al corte. Módulos, campos, auxiliares y finalidad están en
[`hoja-de-firma-acceso-futuro.md`](../catalogo-1-reempaqueta-ventana/hoja-de-firma-acceso-futuro.md).
Estas firmas propuestas no se conceden aquí. Cada lanzamiento posterior debe
reconsultar el permiso vigente por ola/paquete y usar una sesión nueva,
entrada limpia, ordinal nuevo y contrato fijado antes de revelar referencia.

APTO-TECNICAMENTE requiere que el lanzador haya demostrado canarios desde el
proceso reconstructor y que el paquete concreto pase materialización y
contrato. AUTORIZADO-PARA-ABRIR requiere además firma aplicable. Ninguno
implica adopción ni validez del estimando. En la hoja entregada la aptitud
real permanece NO-VERIFICADO-PARA-PAQUETE-REAL y la apertura no autorizada.

LEÍDO: el lote2 histórico conserva su reserva de separación y las nueve
salidas con alias fueron rechazadas por v1. El producto v2 no rehabilita
aquellos intentos como éxito de v1 ni como validación ciega. Los originales,
productores, sellos y permisos del proyecto se preservan. Las ENDIREH2016
con intento1 conservan ese intento; el siguiente ordinal se deriva del
historial de cada identidad en el lanzamiento futuro, no se rellena aquí.

NO-VERIFICADO: sesión nueva de reconstrucción con aislamiento acreditado en
esta caja. No se transportó la misión a otra sesión. La recomendación para
mesa es recibir el producto, mantener el bloqueo de lanzamiento, y resolver
entorno y permisos de lectura delimitados como decisiones independientes.
