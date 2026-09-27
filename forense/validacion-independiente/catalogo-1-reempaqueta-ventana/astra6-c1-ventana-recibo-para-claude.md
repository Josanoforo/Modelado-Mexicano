# Recibo para Claude · ASTRA6-C1-REEMPAQUETA-VENTANA-1

Solicitado por circuito de mesa en el PR propio; revisión externa no obtenida.
No es un recibo independiente concedido por el autor.

EJECUTADO: cinco sucesores documentales,859 identidades transportadas;
método/tolerancia históricos intactos y ventanas exactas. Cero recálculos,
comparaciones, adopciones o validadores lanzados. Cero identidades listas
para ejecutar: permiso de lectura futura NO-DEMOSTRADO, red/lanzador pendiente.

| Paquete | Identidades | SHA-256 original | SHA-256 sucesor |
|---|---:|---|---|
| endireh-pisos-2021-comunitaria-0001 | 100 | 9261eeb9b8ca7e95f66ee57b271f53e9fe6a08feff85377306126025a5e04d0b | 4aa160aa5c2ad11c7f41b5168128172923b5b2a7ccc1390c2f3486dcf8262333 |
| endireh-pisos-2021-escolar-0001 | 96 | 5e33677ef0904bcca544f450cdbbe6969f0884f86f606944cf3429ddd4d1be7a | 63294181486790a8087b40c88abce31fbf54a862911a5a367aac0d7dba1bac3c |
| endireh-pisos-2021-laboral-0001 | 100 | c56fd015b88af8659d19e8f771a20bc81839500d51e28d1c5efd08b2a9fa6c6f | a32351efd04157e2d24688990e1f9aeb40b525537e6bcf9d94bcb95f0670bd1e |
| endireh-pisos-2021-nofisica-bc-0001 | 471 | 37e0d9f4c235d915557f635c2ac9409e9cbf87d97d115ff4362589641ba304d9 | 5f4ff9a9633163356d43a145868637d237ad802432e7eaa20ab6a433b4cb0054 |
| endireh-pisos-2016-pareja-fisica-0002 | 92 | 2a10840b5638e22bb733de9f57990e052fe7b5398ab98474a32ea0c64c1f56df | 6ce9c8a5fdcef8473e666d9fae5b1851c31f899b06f67075f1a7fbe37222a555 |

EJECUTADO: mapa, identidad, procedencia y reactivos en `procedencia/`;
matriz permisos, disponibilidad y copia opaca en `permisos/`; extracción
documental fuera clon en `prueba-aislamiento-documental.json`.
LEÍDO: fuente publicada firmada, no spec independiente anterior al productor;
#1194 OPEN HEADdf54ad05, no adopción de contratos/IC propuestos.
LEÍDO: original92 ya tuvo intento1 en04; recibo logístico congelado sin
revelación al corte, no estado posterior. Históricos y32 D-15 preservados.

Comandos reproducibles, desde la raíz del worktree:

```bash
python3 -m unittest discover -s forense/validacion-independiente/catalogo-1-reempaqueta-ventana/pruebas -q
python3 forense/validacion-independiente/catalogo-1-reempaqueta-ventana/herramientas/transporte_v1.py --mapa forense/validacion-independiente/catalogo-1-reempaqueta-ventana/procedencia/mapa-ventanas.tsv --config forense/validacion-independiente/catalogo-1-reempaqueta-ventana/documentos-revisados/config-p2.json
python3 tests/check.py --rapido
```

La reconstrucción documental del segundo comando debe conservar exactamente
los hashes anteriores; nunca resellar históricos para hacerla pasar.
Los comandos de extracción seguros por contenedor están en
`entrega-por-paquete.tsv` y `comandos-materializacion-documental.sh`;
no calculan ni abren raw. Doce pruebas dirigidas PASS y cinco contenedores
reproducidos; la extracción a /tmp se probó realmente.

PROPUESTO-POR-EJECUTOR: acceso futuro por las dos filas de
`hoja-de-firma-acceso-futuro.md`; usar `receta-sesion-futura.md` después
del permiso y de comprobar el aislamiento efectivo. Un prompt sin acceso
a resultados no acredita por sí solo aislamiento de red. NC-beee-08
conservada; no tocar SAFE/03/04 ni pasar este encargo al validador.

Solicito revisar identidad exacta, límites del diff, contaminación de
contenido, permisos y distinción entre transporte y validación. Mesa
puede recibir el transporte y resolver las propuestas de acceso sin
adoptar resultados estadísticos. No fusionar por ejecutor.

PR propio #1203: https://github.com/Josanoforo/Modelado-Mexicano/pull/1203.
Recibo solicitado; pendiente, sin fusión ni revisión externa declarada.
