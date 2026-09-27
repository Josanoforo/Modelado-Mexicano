# Archivo de documentos recibidos · ASTRA6 tanda2

Los ocho archivos adjuntados por mesa se conservan byte a byte, con sus nombres originales, dentro de `ASTRA6-tanda2-adjuntos-originales.tar.gz`. `ASTRA6-tanda2-rutas-archivadas.json` identifica miembro y SHA-256. El manifiesto recibido también enumera 02, que no fue adjuntado: no se copió ni ejecutó.

Solo el encargo 01 tiene cuerpo operativo en la raíz de encargos y CONSUMIDO al cierre. Los cuatro encargos restantes se conservan como documentos recibidos dentro del contenedor; no tienen firma nueva ni estado de ejecución. Los adjuntos embebidos se cotejaron por bytes y SHA-256: misión y adenda reutilizan `forense/encargos/fuentes/ASTRA6-mision-20260926/`; cláusula reutiliza `forense/encargos/CLAUSULA-AUTONOMIA-v1_0.md`. No se duplican sus firmas.

El hash original del 01 es de bytes completos. Su sidecar de cuerpo usa la normalización N de `tools/sella_sha256.py` (blancos finales y un salto final), conservando los bytes originales en el contenedor. Se corrigió el sidecar local inicial antes de publicar: no se alteró ningún sello científico o histórico.

Extracción, por ejemplo: `tar -xOf forense/encargos/fuentes/ASTRA6-tanda2-20260926/ASTRA6-tanda2-adjuntos-originales.tar.gz 04-2026-09-26-ASTRA6-C3-CONSUMO-FAMILIA-2.md`.
