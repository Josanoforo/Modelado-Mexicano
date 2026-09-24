# ASIGNACIÓN FINAL · Sesión #1079 (ASTRA-5 U0 · mapa de dominios) · 24/sep/2026
**Dirección (Claude) con decisión de mesa: opción 1, kit autorizado con condiciones. Esta asignación completa el acto; no abre uno nuevo. Firma de mesa: la regla de permiso que mesa agrega en `/permissions` antes de que la sesión escriba la herramienta — esa regla es la firma; no hace falta fila FP.**

## 0 · Lo que mesa hace primero (un minuto)
`/permissions` → Allow, tres reglas: escritura de `herramientas/u0red.py` y `tests/test_u0red.py`; ejecución de `python herramientas/u0red.py`; ejecución de `curl.exe` (Windows, vía interop). Hasta que estén, la sesión no escribe la herramienta; si mesa no las agrega, se pasa a la opción 2 (§4) sin preguntar de nuevo.

## 1 · La herramienta `herramientas/u0red.py` — condiciones que van en el propio archivo
- **Solo lectura**: peticiones GET; ninguna escritura fuera de `forense/analisis/dominios/`.
- **Lista blanca de dominios**, la que la sesión ya probó: CNBV, CONDUSEF, planeacion.sep.gob.mx, dgcs.unam.mx (curl.exe por cadena TLS incompleta); migrationpolicy.org (cabeceras de navegador); web.archive.org con `id_` (Cloudflare/captcha: CIDH, Crisis Group, Hofstede, CONASAMI, CONAPRED); api.openalex.org (obras académicas). Un dominio fuera de la lista no se intenta: se registra `FUERA-DE-LISTA`.
- **Bitácora por URL** (`forense/analisis/dominios/bitacora-u0red-<fecha>.tsv`): url · ruta usada (curl-win / ua-navegador / wayback-id_ / openalex) · código · bytes · sha256 del cuerpo si lo hubo · fecha · resultado ∈ {EXISTE, NO-ENCONTRADO, NO-ACCESIBLE, FUERA-DE-LISTA}.
- **Rótulo de entorno en el docstring**: `ENTORNO-DEPENDIENTE: máquina de mesa (curl.exe por interop)`. Una sesión de nube o de caja no puede dar la herramienta por disponible (A.2); si la invoca y no está `curl.exe`, sale `NO-EJECUTABLE-AQUÍ`, no un error críptico.
- **Justificación D-14 en el docstring**: defecto real = 131 fuentes NO-ACCESIBLES desde el sandbox; cambia una clasificación (existencia de fuente); cuesta menos que verificar a mano.
- **Test** (`tests/test_u0red.py`, huérfano en CI): la lista blanca es cerrada; una URL fuera de lista no dispara red; la bitácora tiene las columnas declaradas; con `curl.exe` ausente devuelve `NO-EJECUTABLE-AQUÍ`.

## 2 · Una sola pasada sobre las 131 filas «existencia no comprobada»
- Tandas de agentes; **un intento por ruta de la receta** por URL, en el orden que la receta indique; nada de reintentos abiertos.
- Resultado por fila en el mapa: `EXISTE` (con URL final, código, fecha, sha del cuerpo) · `NO-ENCONTRADO` (dónde y con qué ruta; A.4, nunca «no existe») · `NO-ACCESIBLE` (ruta intentada y error). Ninguna fila cambia de dictamen sustantivo (MEDIBLE-CON-ADQUISICIÓN / NO-MEDIBLE) por esta pasada: solo cambia la columna de existencia de fuente. Si una fila sí debería cambiar de dictamen, se anota como propuesta, no se cambia.
- **Corte de tiempo**: si la pasada excede lo que la sesión estime razonable para cerrar hoy, se corta; lo que quede va a NO-CORRIDO con `DIFERIDO-A: GEN2-ASTRA5-U5-ADQUISICION-1` y la bitácora parcial. El mapa no espera.
- Reensamblar; `--verifica` byte a byte otra vez; las 27 pruebas + la nueva en verde.

## 3 · Cierre del acto (cascada completa, sin excepciones)
- ADR con raíz de acto que registre: el mapa (1 396 afirmaciones: 208 / 768 / 420, con la fila de la pasada: cuántas de las 131 quedaron en cada estado), las tablas derivadas, la hoja de adquisición derivada, **y la herramienta con su condición de entorno** (para que nadie en nube la dé por hecha).
- Fragmento L0, `registro-rotulos`, `check.py --baseline` VERDE.
- **NO-CORRIDO / RESERVAS**: las filas que sigan `NO-ACCESIBLE` (con ruta y error), los diez contratos `EN-MEDICIÓN` (RESULT sellado sin fila en la vista: `DIFERIDO-A: GEN2-TUBERIA-VISTA-NORMALIZADA-2`, pasan a MEDIDO con el primer `[deriva]`), y lo que la pasada dejó fuera por corte de tiempo. «Ninguno.» no aplica aquí.
- Receta archivada como `forense/analisis/dominios/receta-acceso-fuentes-2026-09-24.md`: lo que funcionó y lo que no (Edge headless no pasa Cloudflare; CONASAMI/CONAPRED/Hofstede solo por Wayback), para que U5 la herede sin redescubrirla.
- **CONSUMIDO** con el PR; cuerpo del PR #1079 actualizado con las cifras finales derivadas. El merge es de mesa.

## 4 · Si mesa no agrega las reglas de permiso
Opción 2 tal cual la sesión la propuso: cerrar ahora con las 131 en NO-CORRIDO como `NO-ACCESIBLE-DESDE-SANDBOX`, receta archivada, sucesor `GEN2-ASTRA5-U5-ADQUISICION-1` (corre en caja con red real y hereda la receta). Sin rodeos y sin volver a preguntar.

## 5 · Lo que esta asignación NO hace
No toca `data/manifiesto.yaml` (adquirir es `/adquiere` en caja); no descarga payloads (solo comprueba existencia; un PDF que baje para verificar queda en `forense/analisis/dominios/` como constancia con sha, no en el corpus); no cambia dictámenes; no abre acto nuevo.

## Sucesor
`GEN2-ASTRA5-U5-ADQUISICION-1` (caja): dirección lo escribe sobre el mapa fusionado, con la hoja de adquisición derivada y la bitácora de esta pasada como insumo.
