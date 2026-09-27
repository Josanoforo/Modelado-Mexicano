# PR1194 · Corrección localizada del auxiliar sintético · versión sucesora

EJECUTADO: `p1/protocolo_v2.py` reemplaza la enumeración anticipada únicamente en el auxiliar sucesor. Calcula la cardinalidad con enteros Python y corte temprano antes de llamar a `product`; después itera combinaciones de posiciones de sorteo de forma perezosa. Conserva multiplicidades y contribuciones cero. El límite100000 permanece idéntico. `p1/protocolo.py`, los14tests iniciales y `p1/congelacion-protocolo.json` permanecen byte a byte intactos; el nuevo auxiliar no se presenta como congelado antes de la revisión.

EJECUTADO:18tests v2 pasan:14 originales ejecutados con `exact_law` sucesor y4 regresiones adicionales. Los casos12UPM, producto de varios estratos y cardinalidad mayor que64bits rechazan antes de cualquier enumeración, comprobado con espía que fallaría si se invocara. El caso multiestrato pequeño conserva la masa exacta y multiplicidades. No se materializó la enumeración gigante. Hashes de v2 fijados antes de sus pruebas en `p1/astra6-c1-p1-congelacion-auxiliar-v2.json`; salida en `p1/astra6-c1-p1-pruebas-auxiliar-v2.log`.

LEÍDO: revisión recibida en `astra6-c1-pr1194-revision-recibida.md`, sobre HEADdf54ad05. Se incorpora como dictamen favorable de diagnóstico con corrección localizada, sin convertirlo en aprobación del protocoloIC, escolaridad, edad o accesos. Las562 identidades cuyo marco efectivo falta cotejar siguen pendientes. Las seis publicabilidades2011 siguen condicionadas a sesión01. Esta corrección no cambia cifras ni estados históricos y no vuelve a ejecutar C1.

Condición de preparación futura: COINCIDE en `p3/entradas/insumos-autorizados.json` significa coincidencia de hash. No prueba autorización por ola/módulo/campo ni ausencia de resultados observados en el ZIP o documento integral. Antes de cualquier entrega a nueva sesión, el preparador revisará todos los miembros, excluirá resultados observados y demostrará permisos por alcance. `p3/entradas/` sigue siendo borrador de contratos nuevos, nunca transporte puro ni paquete listo.

Continuidad: la preparación de859 identidades en dos subcohortes corresponde al encargo01 citado en la revisión; la adenda para sesión04 corresponde a su orquestador actual. Esos archivos no fueron adjuntados a esta sesión. No se infiere autorización para enviar mensajes externos ni se relanzan sesiones. Esta sesión completa la corrección del PR1194; mantiene separadas las decisiones de contenido y los preparativos de transporte.

Verificación: `python3 forense/validacion-independiente/catalogo-1-incertidumbre-spec/p1/test_sinteticos_v2.py`. Estas pruebas acreditan implementación y rechazo seguro, no diseño inferencial ni cobertura nominal. Registros y reservas originales del PR conservados; no hay nuevas mediciones, adopciones o aperturas.

Gate rápido final0FAIL597WARN (`p1/astra6-c1-p1-gate-auxiliar-v2.log`). Primer pase sólo excedió15s (18.04s); repetición sin cambiar código ni presupuesto pasa.
