# Frontera del lanzador v2

PROPUESTO-POR-EJECUTOR, preparación no ciega. Fuente: encargo
ASTRA6-C1-AISLAMIENTO-Y-ADAPTADOR-2, P1/P2. No autoriza lecturas futuras.

El orquestador conoce el clon y selecciona explícitamente pares `path,sha256`.
`materialize` exige destino nuevo fuera del clon y valida todos los bytes antes
de copiar. Rechaza rutas absolutas, ascendentes, enlaces en cada componente,
archivos especiales y nombres de productores/resultados/credenciales conocidos.
La revisión humana de la allowlist sigue siendo necesaria: el nombre no permite
descubrir un secreto o documento de dirección disfrazado. No se copia el historial.

Para TAR, `materialize_archive` inspecciona todos los miembros antes de escribir,
rechaza duplicados, enlaces duros/simbólicos, dispositivos y rutas peligrosas.
Sólo copia miembros regulares presentes en la allowlist; límite de expansión
predeterminado 64 MiB. No usa `extractall`. ZIP no es entrada aceptada.

El proceso reconstructor recibe `/entrada` de sólo lectura y espacio efímero
`/tmp`, `/salida`, `/proc`, `/dev`. El runtime de sólo lectura es una allowlist:
ejecutable Python resuelto, módulos `.py` y paquetes de su biblioteca estándar,
`lib-dynload` y bibliotecas concretas obtenidas por `ldd` de Python/extensiones.
No monta árboles `/usr`, `/lib`, `/lib64`, raíz del host, `/home`, `/mnt`, `/etc`
ni `/tmp` del host; excluye `site-packages` y `dist-packages`. Las bibliotecas
se resuelven sin enlaces y deben quedar bajo `/usr/lib`. El runtime del sistema
forma parte de la base confiada, sin secretos ni resultados del proyecto.
Paquetes científicos externos requieren una nueva allowlist de runtime explícita.
No se transmite entorno heredado, stdin, credenciales ni descriptores abiertos.
La salida exportable es stdout/stderr; `/salida` no persiste en el host.

Bubblewrap crea namespaces de usuario, red, PID, IPC, UTS y montajes, elimina
capacidades y abre nueva sesión. El reconstructor no establece conexiones al
broker/API. El orquestador realiza ese transporte fuera de la frontera: entrega
una solicitud ya preparada y recibe stdout; no entrega claves al proceso local.
No hay excepción de red ni puente de sockets dentro del sandbox. La conexión
de una sesión de agente remota requiere implementación y evidencia propia del
orquestador; el lanzador local no certifica memoria/contexto de ese servicio.

`probe_environment` ejecuta primero un proceso dentro de esa misma frontera.
Cuando puede arrancar, intenta leer un archivo permitido, modificarlo, leer
un canario sintético exterior, conectar por TCP a un listener propio y enviar
UDP a TEST-NET 192.0.2.1 dentro de la red aislada. Sólo cinco canarios aprobados
permiten `APTO-TECNICAMENTE`. `run_isolated` repite esa prueba y falla cerrado.
No eleva privilegios ni cambia configuración del host para superar un canario.
La fuente materializada y runtime deben permanecer inmóviles durante la ejecución;
un operador host malicioso o modificación concurrente de montajes queda fuera
de la garantía, igual que sesión nueva, autorización epistemológica y permisos.

EJECUTADO en este entorno: `python3 tools/validacion/astra6_aislamiento_v2/aislamiento.py probe`.
Salida 2, `NO-LANZAR-COMO-CIEGA`: `bwrap: loopback: Failed to create NETLINK_ROUTE
socket: Operation not permitted`. El proceso canario no arrancó; lecturas y
conexiones del reconstructor son NO-VERIFICADAS aquí. No se simula aprobación.
Una prueba directa anterior obtuvo el mismo rechazo. No hubo escalación.

Comandos reproducibles (allowlist JSON es una lista de objetos con sólo `path`
y `sha256`; los SHA proceden de los bytes autorizados):

```sh
python3 tools/validacion/astra6_aislamiento_v2/aislamiento.py materialize --source /ruta/paquete --destination /tmp/entrada-nueva --allowlist /ruta/allowlist.json
python3 tools/validacion/astra6_aislamiento_v2/aislamiento.py materialize --source /ruta/paquete.tar --destination /tmp/entrada-tar-nueva --allowlist /ruta/allowlist.json
python3 tools/validacion/astra6_aislamiento_v2/aislamiento.py probe
python3 tools/validacion/astra6_aislamiento_v2/aislamiento.py run --root /tmp/entrada-nueva -- /usr/bin/python3 -I /entrada/reconstructor.py
```

Opción recomendada: conservar el producto portable y NO lanzar validación ciega
en este entorno. Repetir canarios en entorno autorizado con namespaces efectivos,
runtime inspeccionado, sesión nueva y permiso aplicable antes de cada intento.
`APTO-TECNICAMENTE` nunca equivale a `AUTORIZADO-PARA-ABRIR`.
