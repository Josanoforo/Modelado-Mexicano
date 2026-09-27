# Reconstrucción independiente enigh-0001

Entrega anterior a revelación. No se accedió a resultados esperados ni se
solicitaron al preparador. La única llave se intentó revisar y quedó
NO-RECALCULABLE-DESDE-SPEC, con cifras vacías y motivo en reconstruccion.tsv.
No hay una estimación identificada que pueda congelarse legítimamente.

metodo.md define familia A, hogares que reciben remesas, remesas > 0,
ponderador factor. estimandos.tsv solicita no_recibe_remesas, deja celda vacía
y unidad VER-SPEC. No hay un enlace explícito ni una regla de transformación
para la llave RESULT-ENIGH-A-P-COMPLEMENTO. El nombre de esa llave no se usa
para inferir el complemento, el segmento ni la identidad del resultado.

La descripción de la base, tabla Concentradohogar, variables #6 est_dis,
#7 upm y #8 factor, respalda el diseño y las llaves de texto. La variable
#51 remesas representa ingresos de otros países, construida con clave P041.
El cuestionario de mayores, apartado de ingresos, también identifica P041.
Estas definiciones documentan la variable, pero no asignan la llave pedida.
Se consultaron localmente los documentos humanos; no se usaron fuentes web.

reconstruir.py verifica hashes, identifica el miembro CSV, valida hogares,
valores y llaves, y produce el TSV, recibo e inventario del ZIP. Incluye un
motor de proporción ponderada y bootstrap para la familia A, sin asignarlo
a una llave ni ejecutarlo sobre raw. El motor conserva las llaves como texto,
remuestrea n_h UPM en cada estrato con reemplazo y mantiene los pesos originales.
Usa PCG64, semilla 20260915, 2000 réplicas y percentiles 2.5/97.5.
Orden lexicográfico, bucle réplica/estrato e interpolación lineal son convenciones
de implementación explícitas, no detalles garantizados por la especificación.
Los estratos únicos permanecen fijos y activan el aviso prescrito.

Reproducción con los insumos originales montados en /entrada y /raw:

```sh
python3 reconstruir.py
python3 -m unittest -v test_motor.py
```

El recibo fija versiones de Python y NumPy, hashes de todas las entradas,
hash del miembro leído, tolerancia y conteos de validación. entradas_zip.json
conserva nombres, tamaños y CRC de los miembros; el SHA256 del ZIP completo
protege el contenedor. entrada/ conserva las entradas textuales sin modificarlas.
El repositorio excluye datos raw, PDF y extracciones de documentación.
No se comparó contra resultados externos ni se afirmó cumplimiento numérico
de la tolerancia, pues ninguna llave tiene una cifra identificada.
