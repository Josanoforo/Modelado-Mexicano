# Intento bloqueado de consultar ENCIG para la ficha de `R3.2`

**Fecha:** 29 de julio de 2026 (sesión ENCIG, abierta declarando el commit `b28b144`)

---

## Qué se intentó

Con la ficha de `R3.2` (`forense/hitoD-preregistro-v2_0.md`, Nota 4, commit `b28b144`) ya escrita y commiteada, correspondía el paso siguiente de su propio protocolo: consultar ENCIG 2023 para listar, por la Regla de selección de pregunta (`hitoD-preregistro:427-432`), todas las candidatas que cumplan criterio 1 (pregunta/módulo combinado) o criterio 2 / Respaldo 1 (dos preguntas cruzables por microdatos individuales).

Para eso se intentó alcanzar la documentación primaria de INEGI: el cuestionario de ENCIG 2023 y el documento "Estructura de la base de datos" (el diccionario de variables que dice si existe un campo de modalidad de trámite cruzable, por folio individual, con el campo de incidencia de corrupción).

## Qué bloqueó el intento

El proxy de egreso de esta sesión rechazó la conexión a `inegi.org.mx`:

```
$ curl -sS -o /dev/null -w "HTTP %{http_code}\n" \
    https://www.inegi.org.mx/contenidos/programas/encig/2023/doc/encig23_estructura_base_datos.pdf
CONNECT tunnel failed, response 403
```

Confirmado con dos subdominios distintos (`www.inegi.org.mx` y `en.www.inegi.org.mx`), vía `$HTTPS_PROXY/__agentproxy/status`:

```json
"recentRelayFailures": [
  { "host": "www.inegi.org.mx:443",
    "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)" },
  { "host": "en.www.inegi.org.mx:443",
    "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)" }
]
```

Es política de egreso de la organización para esta sesión, no un 404 del sitio ni un rechazo de una ruta específica — `/root/.ccr/README.md`, sección "403/407 from the proxy": *"the destination host is not allowed by your organization's egress policy for this session. Do not retry or route around it — report the blocked host."*

## Lo único visto

`WebSearch` (no pasa por el mismo proxy) devolvió, de un boletín de prensa de INEGI, un dato agregado suelto: *"52.4% realizó el trámite en oficina de gobierno, 16.2% por internet, 15.4% en banco/tienda/farmacia"*. Es una cifra de boletín, no la estructura de microdatos — no dice si esa variable de modalidad vive en la misma tabla/folio que la variable de corrupción por trámite, que es exactamente lo que criterio 1 y criterio 2 exigen verificar.

Se descartó explícitamente usar un espejo del diccionario de datos en otro dominio: sin el sello del publicador original, un documento espejo es tipo (3) — no verificable como fuente primaria — la misma regla que este proyecto ya aplica al espejo del propio proyecto.

## Resultado

**No se reportó ninguna candidata.** Reportar una candidata de criterio 1 o 2 a partir de un snippet de búsqueda, sin haber leído el cuestionario o el diccionario de datos real, habría sido la misma falla que el protocolo de la ficha (`hitoD-preregistro:432`, "obligación de reporte") existe para prevenir.

**No hay veredicto.** Esto no es veredicto D: D es que *ENCIG 2023* no tenga ninguna de las tres formas de la Regla de selección de pregunta — no es que esta sesión no pudiera alcanzar el sitio. Son hechos distintos y no se confunden.

**El requisito de cierre queda en espera:** el veredicto de `R3.2` y la actualización de `estado:192` ("1 de 27 corrida" → 2) no pueden commitearse en el mismo commit sin haber consultado la fuente primaria, y no la hay todavía.

## Cómo se desbloquea

No está en manos de esta sesión. Ver el turno del 29/jul en el que se reportó esto por primera vez para las opciones (ampliar la política de egreso, recibir los documentos primarios por otro canal, o señalar un espejo con sello verificable).
