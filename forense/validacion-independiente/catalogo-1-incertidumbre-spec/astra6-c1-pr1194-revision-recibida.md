# Revisión PR1194 y siguiente trabajo

HEAD revisado: df54ad05258ea36c77b9efda44a839e250174d1a. PR abierto al consultar; sin comentarios de revisión. Base declarada11602de8. Fuentes complementarias:1192 fusionado (recibo C1) y1190 fusionado (firmas con alcances explícitos). Los nuevos1195/1196 se detectaron para no duplicar sus encargos; no se revisaron a detalle en este pase.

## Dictamen

Favorable como diagnóstico y propuestas, con una corrección pequeña recomendable antes de fusionar. No firmar por arrastre el protocoloIC, recodificación educativa, filtro de edad ni aperturas. La integración del PR no valida esos contratos.

### Lo que está bien y cambia el siguiente paso

- La tabla799 se comprobó aquí:799llaves únicas;767restauraciones de transporte,31cambios de dominio y1aclaración. La lista nueva también tiene799identidades únicas. El primer intento se preserva.
- IC separa1202marcos2011 diferentes documentados,109reglas de marco nofísica diferentes y562casos cuyo marco efectivo todavía no se cotejó. No atribuye todo aRNG ni recertifica bajo una tolerancia nueva. No dar por resueltas esas562.
- Publicabilidad conserva11casos; cincoCV independientes2021 exceden0.30 en la realización archivada. Las seis2011 esperan adjudicación del universo por sesión01. Esto no determina por sí solo cuál algoritmo está bien ni una conclusión pública cambiada.
- P3 explica que el catálogo acredita identidad publicada, no una especificación humana anterior al productor. Las767 restauraciones y los799contratos nuevos son dos productos distintos. No copiar p3/entradas como si fuera transporte puro.

### Corrección técnica localizada

`p1/protocolo.py`, función exact_law, construye `list(product(...))` antes de comprobar el límite100000. Un solo estrato de12UPM genera12^12=8916100448256tuplas antes de llegar a la guarda; la función puede agotar memoria en vez de rechazar un caso fuera de alcance. Reproducción propia segura: sustituir product por una función espía que lanza excepción; la excepción se produce antes de la guarda. No se materializó la enumeración gigante.

Corregir calculando cardinalidad con enteros Python y corte temprano antes de enumerar; después iterar perezosamente si procede. Añadir prueba de rechazo de un estrato12 y de producto de varios estratos que supere límite. No usar numpy.prod para esta guarda porque puede desbordar enteros. Conservar hash/congelación inicial y registrar versión sucesora del auxiliar con sus nuevas pruebas; no reescribir la congelación para aparentar anterioridad.

Es un defecto del auxiliar sintético, no evidencia de cifras históricas erróneas ni motivo para repetir C1. Ejecuté aquí sus14pruebas sintéticas existentes: pasan; no cubren este caso.

### Condiciones para el próximo lanzamiento

`p3/entradas/insumos-autorizados.json` lista ZIPintegral y diseño muestral, con estadoCOINCIDE. Eso acredita coincidencia de hash; no acredita autorización por alcance ni revisión de filtraciones del documento completo. P3 declara que aún no es paquete listo, de modo que esto es una condición de preparación, no acusación de apertura indebida. Antes de entregar a nueva sesión: revisar cada miembro, excluir resultados observados y demostrar permisos por ola/módulo/campo. No heredar el nombre del archivo como firma de acceso.

Los nuevos contratos incluyen excluirEDAD98/99 globalmente, no solo corregir cortes de edad, y proponenNIV-terminal-v1/algoritmoIC. Deben decidirse por contenido separado: en el reempaquetado se conserva el método anterior. Para IC falta defender diseño/cobertura;14tests de implementación no lo acreditan.

## Encargo adicional recomendado

01-ASTRA6-C1-REEMPAQUETA-VENTANA-1:767identidades2021 y92de pareja física2016, total859 en dos subcohortes. Preparación completa de transporte fiel, sin nuevos cálculos ni adoptar las32definiciones problemáticas. Puede arrancar con1192; consume1194 porHEAD o desde main cuando se fusione. No duplica01/03/04 de la tanda3, con perímetros explícitos.

Enviar02-ADENDA-OPERATIVA-SESION04.md al orquestador actual:10paquetes/333pueden continuar; los92 originales deben apartarse. Si ya se lanzaron, se conserva el intento; nunca cambiar el paquete a mitad de sesión. Ningún validador recibe estos archivos.

1195 corresponde a la sesión05 y1196 a06: no relanzarlas. No se puede inferir de ausencia dePR que las otras sesiones estén libres. El nuevo encargo busca primero su identidad/sucesores para evitar duplicación.

## Alcance de esta revisión

Lectura de cambios, dictámenes, propuestas, auxiliares y tablas799; conteo independiente de llaves/clases y ejecución de14tests sintéticos más reproducción segura del orden incorrecto de la guarda. No se ejecutaron microdatos, contrastes históricos, los10checksP2 dependientes del repo completo, ensamblaje3371, PDFs extraídos ni toda la suite. Las afirmaciones de esos ensayos se atribuyen a la entrega, no a esta revisión. Ninguna modificación o mensaje se publicó enGitHub.

Lanzamiento: un archivo01 a la nueva sesión preparadora; archivo02 a la sesión04 ya existente. El01 contiene misión/adenda/autonomía verbatim, diez secciones y firma previamente aprobada. Este paquete no exige una nueva firma general; solo las decisiones de contenido/acceso afectadas permanecen sujetas a su alcance.
