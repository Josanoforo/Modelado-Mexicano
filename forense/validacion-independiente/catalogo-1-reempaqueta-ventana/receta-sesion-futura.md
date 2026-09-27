# Receta para un intento futuro · entrada c1-ventana-v1

PROPUESTO-POR-EJECUTOR. Esta receta no lanza un validador en la preparación.
Los comandos exactos por paquete están en `entrega-por-paquete.tsv` y
`comandos-materializacion-documental.sh`. Ejecutarlos desde la raíz del
repositorio solo materializa documentos en destinos nuevos bajo /tmp.
Si el destino ya existe, se rechaza; elegir otro destino nuevo conserva
el primero. `materializar_ventana_v1.py` verifica contenedor y todos los
miembros, rechaza rutas, enlaces y destinos dentro de worktrees del proyecto.

1. Resolver las firmas de acceso de `hoja-de-firma-acceso-futuro.md`.
   `COINCIDE` en insumos acredita hash, nunca permiso. La matriz actual
   no demuestra autorización para una nueva lectura raw. La copia opaca
   de preparación no satisface este paso.
2. Confirmar desde el expediente externo qué intentos/revelaciones existían
   antes del lanzamiento. El original de 2016 ya tuvo intento1 en sesión04:
   entrada 2026-09-27T05:09:02.066745Z, recibo congelado 05:14:38.291970Z.
   Ese recibo dice CONGELADO-SIN-REVELAR al corte consultado; no acredita
   ausencia de revelaciones posteriores. Registrar las posteriores con hora
   y fuente, sin entregar sus contenidos al nuevo validador. El sucesor
   nunca sustituye el original ni cambia una sesión viva.
3. Ejecutar el comando documental de la fila elegida. Comprobar la identidad
   del manifiesto recibido y la columna ventana con el adaptador versionado
   `transporte_v1.filas(bytes, ventana=True)`. No montar este expediente,
   tabla de entrega, catálogo, mapas, recibos ni adjuntos de dirección.
4. Solo después del permiso de lectura, materializar el ZIP de la fila
   autorizada como bytes opacos; origen/hash/copia de preparación están
   en `permisos/transporte-opaco-preparacion.json`. Verificar de nuevo el
   hash y limitar las lecturas a los módulos/campos firmados. Los documentos
   semánticos revisados ya están dentro del tar. La sesión no descarga
   insumos ni consulta URLs del listado de procedencia.
5. El lanzador futuro monta exclusivamente entrada, raw autorizado y trabajo
   vacío, con configuración e historial nuevos. Verificar mediante pruebas
   negativas que no accede al clon, al historial, al corpus ajeno ni a
   credenciales host. El proceso que llama a la API y las herramientas del
   validador deben tener políticas de red comprobadas por separado.
   NC-beee-08 sigue abierta: el lanzador anterior no acredita aislamiento
   de red. Si no se puede acreditar la política efectiva, conservar
   RED-NO-AISLADA y resolver esa reserva antes de afirmar ceguera; un prompt
   que prohíbe navegar no es una barrera técnica.
6. Entregar a una sesión realmente nueva únicamente el prompt mínimo
   de este expediente y el directorio verificado. Recalcular con código
   propio, congelar código/objetos/hashes antes de cualquier revelación y
   devolver el recibo. Comparación y dictamen pertenecen a otro acto.

La prueba local demuestra extracción documental fuera del clon y hashes
de copias opacas; no demuestra una sesión enjaulada ni red aislada.
`prueba-aislamiento-documental.json` preserva esa distinción. No editar
SAFE, lanzadores o scripts compartidos de 03/04 para ejecutar esta receta.
