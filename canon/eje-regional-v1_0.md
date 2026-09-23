# Eje regional v1.0 · avance medido

**ARCHIVO**: `canon/eje-regional-v1_0.md`  
**NOMBRE ESTABLE**: eje regional v1.0  
**ESTADO**: propuesta; adopta NO; RETROSPECTIVA.

Fuente única de cifras: `python3 tools/astra/region/publica.py`, que lee diecinueve CALC sellados. La tabla TSV conserva las filas suprimidas. Esta entrega aún no cubre todas las conductas adoptadas/adoptables ni todas las olas del mandato U5; por tanto, no acredita cierre integral.

## Decisiones de geografía y publicación

R1: entidades solo donde el diseño y el estimando lo admiten; ENIF 2024 usa sus seis regiones oficiales. R2: punto e IC solo con n≥200, varianza estimable y cualquier requisito oficial más estricto. ENVIPE y ENCIG son entidades de residencia, no ubicación del delito o trámite.

## Filas medidas (818)

- PUBLICABLE: 661
- SUPRIMIDA-N: 157

Las filas tienen nivel geográfico explícito y un RESULT por punto y límite. Los IC de diseño y predictivos calibrados ocupan filas distintas; estos últimos citan dos CALC. Todas las cifras son RETROSPECTIVA. La repetición conjunta de réplicas por ola se conserva dentro del RESULT `-JSON` de cada CALC sin identificadores ni pesos individuales.

## Auditoría de rigor extremo

El estado de residencia no equivale a una ciudad ni al lugar del evento. ENCIG cubre un marco urbano y ENIF solo seis regiones: no permiten inferir todos los habitantes de cada estado. Los niveles reflejan también oferta, recursos e instituciones; no prueban preferencias culturales. No hay medida de clase o pertenencia indígena en estas filas. Una variación regional requeriría una comparación histórica con unidades, geografía e IC comparables; esta tabla no promete detectar cambios futuros.

La [cobertura conocida](../forense/analisis/region/cobertura-conocida-v1_0.md) explicita conductas aún pendientes. El [mapa descriptivo](../forense/analisis/region/mapa-estabilidad-v1_0.md) y la [hoja de mesa](../forense/analisis/region/HOJA-EJE-REGIONAL-para-mesa.md) mantienen esas reservas; adopta: NO.
