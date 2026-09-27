# Entrega a mesa y receta de atestación

EJECUTADO: inventario-portable.json es sucesor aditivo de los inventarios ENIF/ENCIG/ENVIPE conservados. Fija archivos transportables de Git, incluidas enmienda ENCIG, drivers efectivos, contratos v1/v2 como antecedente/sucesor, oros, emisiones, tablas y padres de pisos. No contiene raw ni caches. Los raw autorizados se identifican por id/nombre/hash para montarlos solo en CAJA. El comprobante de envío y el de OTS son null. Estado actual SELLADO-INTERNAMENTE.

En un clon limpio con historia, ejecutar:

```bash
python3 tools/familias-2027/cierre-material-1/verifica_cierre_material.py --verifica --hoja --pruebas --evidencia
```

El comando autentica el inventario contra su blob entregado en Git, compara todos los archivos, coteja COMMIT-1 con la enmienda y prueba rutas/hash/REF. Para transportar a mesa: el clon y su historia (o un bundle de la rama) más inventario-portable.json, inventario-portable.sha256 y paquete-control-hashes.json. La historia de COMMIT-1 es testigo independiente requerido por la verificación; una carpeta sin Git no basta. En CAJA, montar data/raw y comprobar los tres ids del inventario. No ejecutar `--replay` si replay-ejecutado.json ya existe; se conserva la primera evidencia.

Mesa, por canal aprobado: integrar estos objetos al siguiente manifiesto de sellos; generar/enviar la prueba OTS; conservar comprobante real con identidad exacta del manifiesto/paquete; verificarlo en un acto independiente y registrar la transición de estado. Este acto no envía mensajes ni solicita OTS a terceros. No se reescriben testimonios originales ni se atestiguan solo hashes anteriores de drivers sustituidos.

Las ventanas y su procedencia están por familia en hoja-comun.json. ENIF no tiene publicación confirmada; su seguimiento operativo no es ventana oficial. ENCIG tiene ventana esperada del programa SNIEG; ENVIPE tiene ventana propuesta y fecha no confirmada. No se repite la búsqueda ENVIPE2026 ni se abre esa ola.
