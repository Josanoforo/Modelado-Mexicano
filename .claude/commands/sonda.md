---
description: Investigación lateral reusable — un NO-ENCONTRADO, una fuente bloqueada o un instrumento faltante no se convierte en "no existe" sin declarar qué universo adicional se agotó. Busca fuera del universo ya examinado, clasifica A.4/A.5, entrega candidatas o handoff concreto. No decide por mesa, no descarga, no modifica specs/modelo. Uso — /sonda <código> <definición verbatim> [modo]
argument-hint: <código celda/regla/fuente> <definición verbatim> [CONSTRUCTO|HERMANAS|LATERAL]
---

# `/sonda` — investiga lateral, no decide

Creada por `ACTO GEN2-SONDA-2 · OPERACIONALIZA-SONDA-LATERAL`, operacionalizando
una conducta que ya se ejecutó con éxito tres veces antes de que existiera esta
skill: `PR #197` (`ACTO SONDA-1`, mapa de barreras de 15 fuentes sin descargar),
`PR #524` (`ACTO MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1`, con su enmienda
`SONDA-LATERAL-PENDIENTES` el mismo día) y `PR #542`
(`ACTO MAESTRA38-N12 · SONDA-INSTRUMENTOS-DE-PERCEPCION`). Esta skill no inventa
método nuevo — extrae el patrón que los tres ya demostraron y lo deja invocable
por código/definición en vez de re-redactado cada vez:

- una barrera (Cloudflare, WAF, TLS, login) no prueba inexistencia (`#197`);
- "Universo desconocido" es una categoría con nombre, no un vacío — se explora
  explícitamente, y una ruta oficial fallida no agota una fuente: hay vías
  hermanas (repositorio institucional, API, archivo histórico, mirror,
  replication package, formato alterno) (`#524` y su enmienda);
- un objeto encontrado con `HTTP 200` no es por sí solo el instrumento buscado
  — se verifica por contenido, no por código de respuesta (`#524`);
- si NUBE no puede abrir una candidata, eso no se convierte en negativo — pasa
  a `SIN-FETCH`/CAJA con ficha, nunca en "no existe" (`#542`).

**Esta skill propone, no decide.** No sella una candidata, no adopta un
resultado, no modifica `milpa/**` ni el canon, no descarga por defecto. La
decisión de adquirir, adoptar o cerrar sigue siendo de mesa/DIRECCIÓN.

---

## 0 · Qué NO es esta skill

No es un segundo `/adquiere`: no camina la cola por prioridad, no hace A.7
(doble descarga) ni A.8 de payload. No abre una segunda cola ni un segundo
escritor — el único SSOT de adquisición sigue siendo
`data/curacion-registro/cola-adquisicion-registro.tsv`, escrito por
`tools/curador_registro/tsv_crudo.py::upsert_fila` (el mismo mecanismo que ya
usa `tools/arbitra.py`), proyectado a `data/cola-adquisicion-v1_0.tsv` por
`tools/vista_cola_adquisicion.py`. No es un crawler general ni un indexador de
internet: sondea candidatas concretas para una definición concreta, no
construye un catálogo.

Si esta invocación corre dentro de un `/acto` que ya hizo su propio ARRANQUE
(A.2/A.8), no lo repitas. Si corre sola: confirma que
`tools/busca_reactivos.py` y `tools/curador_registro/tsv_crudo.py` existen — si
falta alguno, PARA.

## 1 · Arranque — declara el estado de entrada

Antes de sondear nada, declara lo que YA se concluyó y sobre qué universo —
casi siempre la salida de `/mapea`, un `NO-ENCONTRADO`/
`HIPÓTESIS-SIN-INSTRUMENTO` de `milpa/tramite*.yaml`, o una fila de la cola en
estado `NO-OBTENIDO-POR-ESTE-AGENTE`/`PENDIENTE-DE-MESA`/`SIN-FETCH`. Esta
skill NUNCA reconstruye esa definición de memoria — si el operador no trae la
definición verbatim, PARA y pídela, mismo criterio que `mapea.md §0`.

Verifica con un comando real cuál fue el universo YA examinado (no lo
adivines): `grep`/`python3 tools/busca_reactivos.py`/lectura de la nota o fila
citada. Esta línea de "estado de entrada" es la que separa un `/sonda` honesto
de uno que redescubre lo mismo con otro nombre.

## 2 · Elige el modo

Los tres modos comparten el mismo procedimiento (declarar universo adicional,
sondear, clasificar, declarar negativo acotado) — lo que cambia es la
pregunta que gobierna qué se busca. Si una invocación real mezcla dos
preguntas (p.ej. "¿hay otra ola Y hay otra vía de acceso a esa ola?"), corre
los dos modos en la misma salida en vez de forzar una sola casilla; no
construyas tres motores separados solo por conservar los tres nombres.

**A. CONSTRUCTO** — *"¿qué otras fuentes/instrumentos podrían medir esta
definición que el universo actual no contiene?"* Para `NO-ENCONTRADO`,
`HIPÓTESIS-SIN-INSTRUMENTO`, o un constructo sin candidata conocida. Busca
**familias de fuente distintas**, no sinónimos dentro del mismo inventario —
eso ya lo cubre `/mapea` §2. Incluye considerar si el tipo de instrumento
correcto es siquiera una encuesta (una definición puede pedir un dato
administrativo — padrón, registro, serie regulatoria — que ningún buscador de
reactivos de encuesta puede encontrar por diseño; declararlo es un resultado
de este modo, no una excusa para no buscar).

**B. HERMANAS** — *"¿existe otra ola, módulo, edición, repositorio,
país/estudio equivalente, release, replication package o miembro de la misma
familia que resuelva el hueco?"* Para cuando la fuente/familia ya se conoce
pero la ola presente no trae la variable, o hay hueco de cobertura temporal.
Verifica primero si el universo local (`busca_reactivos.py` sin filtro de
encuesta, o con `--encuesta` sobre la familia) ya creció desde la última
búsqueda — una fuente indexada DESPUÉS de la búsqueda original invalida la cota
de universo que esa búsqueda declaró, y es en sí mismo un hallazgo a declarar.

**C. LATERAL** — *"la fuente es conocida, ¿existe otra vía legítima para
llegar al mismo objeto?"* Para cuando la ruta principal ya falló (`/adquiere`
agotó sus 4 rutas, o una sonda de red anterior dio `SIN-FETCH`). Explora, según
aplique: API oficial, endpoint de descarga, `distribution.contentUrl`
(JSON-LD), formato alterno, repositorio institucional, Dataverse/DSpace,
replication package, archivo histórico, mirror legítimo (Wayback Machine con
el endpoint crudo `.../id_/...`, no la barra de herramientas), endpoint que
alimente una visualización pública (p.ej. gráficos Datawrapper embebidos
exponen su CSV sin login — hallazgo real de `#524`), documentación/codebook
que revele la ubicación real. **Un fallo HTTP/TLS/Cloudflare/WAF/login no
prueba inexistencia; un `HTTP 200` tampoco prueba que el payload sea el
correcto** — verifica por firma de bytes/contenido, no por código de
respuesta.

## 3 · Sondea — declara cada ruta que se examina

Cada ruta intentada se declara con su comando y su salida cruda — igual que
`/adquiere §3` para descarga, esta skill no acepta "no encontré nada" sin el
comando que lo respalde. Herramientas disponibles, según el modo:

- `python3 tools/busca_reactivos.py --palabra ... [--encuesta ...] --limite N`
  — universo indexado (`v1_2`+`ext`, metadato de texto, sin abrir microdato ni
  red). Declara la línea de universo (A.13) que la salida ya trae.
- `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10-15 <url>` — sonda de
  alcanzabilidad. `000` es ambiguo por sí solo (A.13): confírmalo con un
  segundo mecanismo antes de declarar bloqueo.
- `curl -sS "$HTTPS_PROXY/__agentproxy/status"` — distingue bloqueo de
  política de egreso (NUBE) de host caído. `connect_rejected`/`403 a CONNECT`
  aquí, junto con `curl` en `000`, es la firma de un bloqueo de NUBE — **no de
  inexistencia de la fuente**.
- `WebFetch` como tercer mecanismo independiente cuando el primero y el
  segundo ya apuntan a bloqueo — tres mecanismos distintos con el mismo
  veredicto es más fuerte que uno solo (criterio ya fijado por `#542`).

Si la red del entorno impide comprobar una candidata externa: declara
`SIN-FETCH` (o el estado vigente equivalente que la fila/nota ya use) y
continúa — nunca lo conviertas en "no existe". Un bloqueo de NUBE no es un
PARO de esta skill: sigue declarando candidatas, aunque no pueda verificarlas
byte a byte hoy.

## 4 · Clasifica con el vocabulario vigente

No inventes vocabulario paralelo. Usa A.4 (`mapea.md §4`:
`EXISTE-SATISFACE`/`EXISTE-NO-SATISFACE`/`NO-ENCONTRADO`/`NO-ACCESIBLE`/
`NO-ADQUIRIDA-POR-COSTO`/`HIPÓTESIS-SIN-INSTRUMENTO`) y A.5/los estados de cola
vigentes (`adquiere.md`: `PENDIENTE`/`OBTENIDO`/`OBTENIDO-PARCIAL`/
`NO-OBTENIDO-POR-ESTE-AGENTE(N intentos)`/`NO-ACCESIBLE`/`PENDIENTE-DE-MESA`/
`SIN-FETCH`). Si la fila o nota que este sondeo continúa ya usa un estado más
específico (`SIN-COBERTURA-EN-ESTAS-FUENTES`, `DIFERIDO-A`, etc.), hereda ese
vocabulario en vez de forzar uno de los genéricos de arriba.

Distingue explícitamente, en la nota de cada candidata:

- ninguna candidata satisfactoria encontrada (`NO-ENCONTRADO`, universo
  declarado);
- candidata existente pero insuficiente (`EXISTE-NO-SATISFACE`, con qué
  falta);
- candidata localizada pero no abierta/verificada (`SIN-FETCH`, con la razón
  del bloqueo);
- barrera técnica (host caído, TLS, WAF) vs. barrera de credencial/costo
  (`NO-ACCESIBLE`/`NO-ADQUIRIDA-POR-COSTO`) — no son lo mismo, y confundirlas
  ya causó un revés documentado (`canon/gobernanza-v1_15.md`, casos CNBV/PI:
  una barrera de TLS se había etiquetado `NO-ACCESIBLE` cuando era
  `NO-OBTENIDO-POR-ESTE-AGENTE`);
- ausencia comprobada sólo dentro del universo sondeado hoy, con ese universo
  nombrado.

## 5 · Disciplina del negativo — el requisito central

`/sonda` **nunca** convierte "no apareció en X" en "no existe" sin declarar
qué universo adicional se agotó. Toda conclusión negativa que esta skill
produzca trae, en la misma nota:

1. definición buscada (verbatim);
2. universo YA examinado antes de esta invocación (heredado del §1);
3. universo ADICIONAL que esta invocación sondeó (fuentes/familias/rutas,
   nombradas una por una);
4. formulaciones o rutas usadas, con comando;
5. qué no pudo abrirse, y por qué mecanismo se confirmó el bloqueo;
6. qué queda explícitamente FUERA de este sondeo (lo que ni siquiera se
   intentó) — un negativo que no declara su frontera se lee como cobertura
   total sin haberlo sido.

## 6 · Handoff a adquisición — reusa el escritor, no inventes uno

`/sonda` no reemplaza `/adquiere`. Si esta skill localiza una candidata
concreta que vale la pena intentar adquirir:

1. **A.8 primero**: `grep` contra `data/manifiesto.yaml` y contra
   `data/curacion-registro/cola-adquisicion-registro.tsv` (por nombre/host) —
   evita fichar una candidata que ya tiene fila o ya está `OBTENIDO`. Si ya
   existe una fila para esta fuente, el handoff es un `upsert_fila` con la
   MISMA clave (actualiza la nota, no duplica), no una fila nueva.
2. Resuelve alias contra `data/curacion-registro/aliases-fuentes.tsv` con
   `registra_cola_adquisicion.build_alias_index` (impórtalo, no lo
   reimplementes) — si no resuelve, declara `SIN_ALIAS`, no lo fuerces.
3. Escribe con `tools/curador_registro/tsv_crudo.py::upsert_fila` sobre
   `data/curacion-registro/cola-adquisicion-registro.tsv`, `clave` según
   corresponda: `fila_origen` si esta candidata ya tenía una fila propia de
   otra fuente citable; `fuente_canonica` si es candidata nueva sin fila
   previa (mismo patrón que `PAQUETE-RECETAS-6`/`8`, N12 §5). Campos mínimos:
   `fuente_canonica`, `fuente_canonica_normalizada`, `discordancia_alias`,
   `estado_A4A5` (`PENDIENTE`/`SIN-FETCH`/lo que corresponda), `prioridad`,
   `url_conocida`, `ids_manifiesto`, `origen` (cita esta invocación de
   `/sonda`, el código/definición que intentaba cubrir, y la razón candidata),
   `nota`.
4. Regenera la vista: `python3 tools/vista_cola_adquisicion.py` — nunca edites
   `data/cola-adquisicion-v1_0.tsv` a mano.
5. Si la candidata es una RELACIÓN nueva (necesidad↔fuente↔objeto) y no solo
   una fila de cola, y `alta_relacion.py` ya tiene lo que exige (`necesidad_id`
   existente, columnas completas), puede usarse — pero un alta de relación es
   decisión de mayor peso que un alta de cola; si falta certeza, deja la fila
   de cola sola y declara la relación como pendiente de mesa, no la fuerces.

**El alta en la cola NO significa** `EXISTE-SATISFACE`, ni relación
`CONFIRMADA`, ni resultado adoptado — significa únicamente "vale la pena
intentar adquirir/verificar esta candidata". No modifica `milpa/**` ni
relaciones del modelo por el solo hecho de descubrir una fuente.

Si la candidata NO necesita adquisición (ya está `OBTENIDO`/indexada) —
repórtala, no la re-encoles. Si requiere CAJA/manual — `PENDIENTE`/`SIN-FETCH`
con receta ≤1 min, mismo criterio que `adquiere.md §6.3`. Si no aparece
ninguna candidata — negativo acotado del §5, sin fila nueva.

## 7 · Salida estándar

```
### SONDA · <código>
Definición: "<verbatim>"

Estado de entrada:
<qué había concluido el mecanismo previo y sobre qué universo>

Modo:
CONSTRUCTO | HERMANAS | LATERAL

Universo adicional sondeado:
<fuentes/familias/repositorios/rutas realmente examinados, con comando>

| candidata | fuente/familia | evidencia de existencia | cobertura aparente | acceso | A.4/A.5 | siguiente paso |
|---|---|---|---|---|---|---|
| ... |

NEGATIVO ACOTADO:
<si aplica, qué se agotó exactamente y qué NO fue examinado>

HANDOFF:
- NINGUNO
o
- adquisición: <fuente / fila / estado>
o
- CAJA/manual: <receta concreta>
o
- volver a /mapea con <nuevo universo>, si aplica.

RECOMENDACIÓN:
una sola frase. Propone, no decide — sin verbo de decisión ("se adopta",
"se sella", "se adquiere").
```

## Lo que esta skill no hace

No decide cuál candidata adopta el motor — eso es de mesa/DIRECCIÓN. No
escribe reglas de `milpa/tramite.yaml` ni specs nuevas. No abre microdato por
sí sola (una candidata que exige abrir un payload ya `OBTENIDO` para
verificar contenido es trabajo de CAJA o de un acto posterior con `data/raw`
enlazado, no de esta invocación NUBE). No descarga por defecto — encontrar y
descargar sigue siendo `/adquiere`. No crea una segunda cola, un segundo
escritor ni una rutina/CRON. No trata un `HTTP 200` como evidencia de
contenido ni un fallo de red como evidencia de inexistencia. No re-intenta
indefinidamente la misma ruta ya declarada bloqueada con el mismo mecanismo —
si va a reintentar, cambia el mecanismo o declara por qué esta vez podría ser
distinto (p.ej. tiempo transcurrido, entorno distinto).
