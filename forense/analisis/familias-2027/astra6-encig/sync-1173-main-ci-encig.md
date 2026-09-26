# Sync posterior a #1173 · ENCIG

EJECUTADO: #1173 fusionado como `e8de0f2853d406f344d6b1ac05735f18767ee4ed`; fetch origin y merge de main en `a63c40ee12ad7ea405ac367c2a2ec36cf5380ab6`. Conflicto único data/INFRAESTRUCTURA-v1_0.md resuelto conservando las entradas ENCIG y de ambos lotes reports. Otros registros compartidos se integraron por merge vigente.

EJECUTADO: T02 detectó cuatro nombres normalizados ENCIG/ENVIPE (calendario.md,arranque.md,potencia.json,commit-1-hashes.json/commit1-hashes.json). Se registran solo los pares exactos en EXCEPTED_NAME_GROUPS de tests/check.py: nombres genéricos por instrumento con contenido e identidad propios; no exención por prefijo ni por contenido. Guardias focales comprobaron aceptación de pares, rechazo de tercer archivo ajeno y rechazo de duplicación de contenido. No se renombran rutas congeladas ni se cambia contrato/lector/sellos.

EJECUTADO: verificador ENCIG --verifica VERDE después del merge, 50 pruebas propias pasan y los tres CALC reproducen. Corrección T02 de cinco líneas, con alcance CI autorizado por mesa en esta continuación. Comprobación rápida tras corrección: ver salida de la sesión; la pasada anterior con cuatro colisiones no era verde. El PR #1172 permanece sin fusionar, revisión Claude/atestación externas siguen pendientes según recibo.
