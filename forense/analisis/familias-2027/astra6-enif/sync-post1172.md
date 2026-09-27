# Sync ENIF tras #1172

EJECUTADO: #1172 fusionó en ea97dfb1c29b61b664feb9ffb9932c8bc45b9e50; fetch y merge de main realizados. Se resolvió el único conflicto en tests/check.py conservando las excepciones de main y agregando ENIF al grupo exacto de recibos.

EJECUTADO: T02 detectó ocho colisiones nuevas por nombres entre paquetes ENCIG/ENIF/ENVIPE; se añadieron grupos exactos (sin excepción por prefijo). Los contenidos son distintos y los archivos materiales permanecen en rutas congeladas. No se editó código/spec/sello material ENIF, ni tablas o registros históricos ajenos.

EJECUTADO: cierre.py --verifica vuelve a VERDE sobre main incorporado: oro y ambas emisiones REPRODUCE/IDENTICO, 32 pruebas dirigidas pasan. Chequeo rápido y CI remoto se registran por separado. PR #1174 permanece abierto; no se fusiona.
