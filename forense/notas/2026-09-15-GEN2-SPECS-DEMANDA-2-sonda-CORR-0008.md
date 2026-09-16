# SONDA · CORR-0008 — NO-HAY-DISEÑO-PÚBLICO (ENNViH/MxFLS olas 2-3)

**Acto:** `ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026, NUBE, sobre `origin/main = da9b47a361143d408cd9fd9c20d17b101c4fe381`.

### Definición (verbatim, del encargo)

> `/sonda` (CONSTRUCTO/HERMANAS/LATERAL) sobre ... la NO-HAY-DISEÑO-PUBLICO: candidatas con A.4/A.5, SIN-FETCH donde nube no abra, receta manual de un minuto donde haya credencial.

Objeto exacto: diseño muestral publicado / pesos replicados oficiales para
`ENNVIH` olas 2 (2005-06) y 3 (2009-12), necesarios para el IC de diseño de
`CORR-0008` (2 `RESULT`) y, transversalmente, para `G3/horizonte_temporal`
(§`SONDA-CORR-0018`) y para `S7-L17` Rama A (`prereg-caja-S7-L17 §0.3`).

### Estado de entrada

`data/corrida0/mapa-demanda-19-corr-v1_0.tsv:CORR-0008`:
`BLOQUEADA · NO-HAY-DISENO-PUBLICO`, sucesor `NC-0156 · MESA`. Identidad de
payload YA corregida (`NC-0188`): los tres archivos `ENNViH` están en
manifiesto con `sha256` verificado. `forense/no-corrido.tsv:NC-0156`
(`ABIERTA`, 10/sep/2026): **expediente técnico ya completo y listo** —
`forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/03-ENNVIH-DIN-S6.md`,
estado `BORRADOR FINAL; LISTO-PARA-TITULAR; NO ENVIADO`, correo redactado al
contacto oficial (`support@ennvih-mxfls.org`), pidiendo pesos replicados o
servicio oficial de varianza para 4 estimandos (`DIN-M-01`, `S6` C1/C3/C4) —
**no incluye explícitamente los 2 `RESULT` de `CORR-0008`** ni los de
`G3/horizonte_temporal`, aunque son el mismo instrumento/ola.

### Modo

**LATERAL** (la fuente/familia ya se conoce — `ENNViH`/`MxFLS` — la pregunta
es si hay otra vía al diseño que la solicitud por correo ya en curso) +
**HERMANAS** breve (¿hay un repositorio/réplica con el diseño publicado que
la solicitud por correo no necesitaría?).

### Universo adicional sondeado, con comando

Tres mecanismos independientes, los tres con el mismo veredicto:

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://www.ennvih-mxfls.org/english/documentation.html
000  (exit 56, connect_rejected)
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://www.rand.org/well-being/social-and-behavioral-policy/data/FLS/MxFLS.html
000  (exit 56, connect_rejected)
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 12 https://www.icpsr.umich.edu/web/ICPSR/search/studies?q=Mexican+Family+Life+Survey
000  (exit 56, connect_rejected)
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 12 https://www.openicpsr.org
000  (exit 56, connect_rejected)
$ curl -sS "$HTTPS_PROXY/__agentproxy/status" | grep -A3 "www.ennvih-mxfls.org"
    { "kind": "connect_rejected", "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)", "host": "www.ennvih-mxfls.org:443" }
```

Segundo mecanismo (herramienta `WebFetch`, independiente del proxy `curl`):

```
WebFetch(url="https://www.ennvih-mxfls.org/english/documentation.html", ...)
-> {"error_type":"EGRESS_BLOCKED","domain":"www.ennvih-mxfls.org", ...}
```

**Control de calibración (A.13):** se sondeó también `www.inegi.org.mx` —
fuente que otros actos de este mismo proyecto citan como alcanzable desde
`cloud_default` en fechas recientes (`ACTO GEN2-SPECS-DEMANDA-1`, cabecera:
`"curl -s -o /dev/null -w %{http_code} https://www.inegi.org.mx/"` como
parte del `ARRANQUE`) — y dio el **mismo** `connect_rejected`. **Hallazgo
declarado:** la política de egreso de *esta* sesión (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`)
bloquea salida HTTPS general de forma más estricta que la que sesiones
previas de este mismo entorno documentaron — no es una señal sobre
`ENNViH`/`MxFLS`/`ICPSR` en particular, es la política de red de hoy. Se
declara aquí porque **cambia la interpretación de cualquier `NO-ENCONTRADO`
web de este acto**: ningún sondeo de red de esta sesión puede distinguir
"la fuente no existe" de "esta sesión no puede salir a internet".

### Tabla de candidatas

| candidata | fuente/familia | evidencia de existencia | cobertura aparente | acceso | A.4/A.5 | siguiente paso |
|---|---|---|---|---|---|---|
| Solicitud por correo ya redactada (`support@ennvih-mxfls.org`) | canal oficial, ENNViH/MxFLS | expediente completo, `LISTO-PARA-TITULAR` | 4 estimandos ya cubiertos (`DIN-M-01`, `S6`); **NO** cubre explícitamente `CORR-0008` (2 `RESULT`) ni `G3/horizonte_temporal` | requiere que **mesa/titular envíe el correo con identidad real** — no es SIN-FETCH, es `SOLICITUD-PREPARADA` (vocabulario ya vigente en `NC-0156`) | `EXPEDIENTE-TECNICO-LISTO; DECISION-DE-MESA-PENDIENTE` (heredado, sin cambio) | mesa decide si amplía el correo ya redactado para cubrir también `CORR-0008`/`G3-horizonte_temporal` en la misma solicitud (mismo instrumento, mismo contacto, cero costo marginal de canal) — **receta de un minuto**: agregar un párrafo al correo ya escrito, no crear expediente nuevo |
| Documentación pública del sitio oficial (`documentation.html`) | ENNViH/MxFLS oficial | **SIN-FETCH** en esta sesión (bloqueo de red confirmado por 3 mecanismos, ver arriba) | desconocida — no examinada | bloqueado por política de egreso de NUBE, no por la fuente | **SIN-FETCH** | CAJA o una sesión con política de red distinta re-intenta el mismo `curl`/`WebFetch` |
| RAND MxFLS landing page | espejo/co-productor (RAND coproduce MxFLS con INSP/UIA) | **SIN-FETCH** en esta sesión | desconocida | bloqueado por política de egreso | **SIN-FETCH** | ídem |
| ICPSR / openICPSR (posible depósito de réplica pública) | repositorio institucional | **SIN-FETCH** en esta sesión — ni siquiera se confirmó si MxFLS tiene depósito ahí | desconocida | bloqueado por política de egreso | **SIN-FETCH** | ídem — es la vía más prometedora para un diseño **público sin necesidad de correo** (ICPSR suele publicar documentación de diseño sin restricción, aunque el microdato exija licencia) y **no se pudo ni empezar a verificar** en esta sesión |

### NEGATIVO ACOTADO

**No se declara negativo material.** Lo único que esta sonda concluye con
certeza es que **la red de esta sesión específica no permite verificar
ninguna candidata web** — no que las candidatas no existan. El universo
adicional que **no** se pudo examinar (frontera explícita): contenido real
de `documentation.html`, de la página de RAND, y de un posible depósito
ICPSR/openICPSR de MxFLS — los tres quedan **SIN-FETCH**, no
`NO-ENCONTRADO`. El único universo que sí se examinó con certeza es el
`forense/expedientes-acceso/` ya escrito (LATERAL interno, no requiere red).

### HANDOFF

- **NINGUNO a cola de adquisición** — GATED a `ACTO ADQUISICION-CONTINUA`
  por perímetro de este acto; y en todo caso el objeto (diseño muestral, no
  microdato descargable por URL directa) no es una fila de cola típica.
- **Mesa/titular**: el expediente `03-ENNVIH-DIN-S6.md` ya está listo para
  enviarse — ampliarlo para cubrir `CORR-0008` y `G3/horizonte_temporal`
  (mismo instrumento, mismo canal) es la acción de menor costo disponible
  hoy.
- **CAJA (o cualquier sesión sin el bloqueo de red de hoy)**: re-intentar
  los tres `curl`/`WebFetch` de arriba contra `documentation.html`, RAND, e
  ICPSR/openICPSR — ninguno se pudo verificar desde esta sesión.

### RECOMENDACIÓN

`NC-0156` permanece `ABIERTA` sin cambio de fondo; el hallazgo nuevo de
esta pieza es que el expediente ya redactado no cubre `CORR-0008` ni
`G3/horizonte_temporal` y podría ampliarse sin canal nuevo, y que el
bloqueo de red de esta sesión (confirmado, no específico de `ENNViH`)
impide cualquier verificación adicional hasta que corra en un entorno con
otra política de egreso.
