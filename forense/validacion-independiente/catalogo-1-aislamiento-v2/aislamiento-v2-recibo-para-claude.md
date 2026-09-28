# Recibo solicitado · ASTRA6 C1 aislamiento y adaptador v2

EJECUTADO: producto de preparación no ciega, solo sintéticos. El lanzador
materializa una allowlist en raíz nueva fuera del clon; inspecciona TAR antes
de extraer; el proceso usa una frontera local y falla cerrado cuando no
puede aislarse. El adaptador v2 conserva original y derivada con mapa/hashes,
congela código/entrada/contrato/tolerancia y exige el hash externo del
manifiesto antes de comparar. V1 e intentos históricos intactos.

EJECUTADO: circuito portable con referencia sintética independiente fuera
de la entrada del reconstructor. COINCIDE y DISCREPA comprobados; unidades
incompatibles y alteración posterior rechazadas. Los resultados de pruebas
y el hash de congelación se consultan en
`aislamiento-v2-evidencia-circuito.json` y `aislamiento-v2-verificacion.json`.
El archivo `aislamiento-v2-circuito-congelado.tar.gz` conserva los bytes del
circuito verificable; `aislamiento-v2-objetos-sha256.json` identifica objetos.

EJECUTADO: prueba de entorno real NO-LANZAR-COMO-CIEGA en
`prueba-entorno.json`. Bubblewrap falla antes de ejecutar canarios internos
por NETLINK_ROUTE Operation not permitted. NO-VERIFICADO: denegaciones desde
un reconstructor aislado y sesión nueva controlada en este entorno. La
disponibilidad de una herramienta de sesiones no acredita aislamiento ni
control de red. No se relaja la caja ni se transporta la misión.

LEÍDO: #1203 y firmas ee49-01/02 ABIERTA; disposición por paquete derivada
en `disposicion-por-paquete.json`. No hay apertura ni adopción. El lote2
conserva su reserva de separación; los nueve rechazos de v1 siguen siendo
rechazos de v1. Recomendación y alternativa en `aislamiento-v2-decisiones.md`.

Comandos desde la raíz del worktree:

```bash
python3 tools/validacion/astra6_aislamiento_v2/test_producto.py -q
python3 tools/validacion/astra6_aislamiento_v2/verifica_entrega.py
python3 tools/validacion/astra6_aislamiento_v2/aislamiento.py probe
python3 tools/validacion/astra6_aislamiento_v2/circuito.py --output /tmp/astra6-circuito-recibo-nuevo
python3 tools/validacion/astra6_aislamiento_v2/adaptador.py --help
python3 tools/validacion/astra6_aislamiento_v2/aislamiento.py --help
python3 tests/check.py --rapido --baseline
git diff --check
```

El probe sale 2 cuando no hay aislamiento suficiente; es el rechazo esperado.
El circuito requiere destino nuevo y no acredita ceguera. `verifica_entrega.py`
comprueba hashes externos, extrae el archivo conservado a un temporal propio
y verifica la congelación contra el ancla externa.

El hash externo está en `aislamiento-v2-evidencia-circuito.json`, campo
`manifest_sha256`; nunca se sustituye por uno recalculado del artefacto que
se verifica. La identidad del contrato v2 se fija en el commit de producto;
ajustarlo tras un lanzamiento real exige versión nueva. PROPUESTO: recibir
producto portable sin autorizar apertura, fusión ni adopción automática.

INTERPRETACIÓN-DECLARADA: el recibo usa prefijo propio para evitar la colisión
de nombres genéricos que T02 detectó en el arranque. Conserva función y
contenido solicitado de recibo-para-claude; no cambia la convención compartida.
Se solicita recepción por circuito de mesa en el PR; no se afirma obtenida.
