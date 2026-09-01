---
description: Camina data/cola-adquisicion-v1_0.tsv por prioridad e intenta adquisición programática fila por fila — payload al corpus compartido si hay éxito, receta de navegador ≤1 minuto si no. Uso — /adquiere [N] (N = máximo de filas a caminar en esta invocación; vacío = todas las elegibles)
argument-hint: [N filas, opcional]
---

# `/adquiere` — camina la cola, no la reescribas de memoria

Creada por `ACTO MAESTRA33-A1 · AGENTE-ADQUISICION-1` (31/ago/2026, `ADR-242`
candidato). Ejecuta el mecanismo de `data/cola-adquisicion-v1_0.tsv`, no un
resumen de él. `data/cola-adquisicion-2026-08-12.tsv` y las cuatro
`data/cola-ext-*-2026-08-06.tsv` quedan como histórico — esta skill lee y
escribe **solo** la tabla `v1_0`.

---

## 0 · Arranque mínimo

Si esta invocación corre dentro de un `/acto` que ya hizo su propio ARRANQUE
(A.2/A.8/`data/raw`), no lo repitas. Si corre sola, confirma antes de tocar
una sola fila:

1. `ls -la data/raw` — si falta, `ln -s /home/pc0/mm-corpus/raw data/raw`
   (gitignorado, un worktree fresco siempre nace sin él — no es PARO).
2. `echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-<sin_variable>}"` — esperado
   `<sin_variable>` (CAJA, no NUBE). Esta skill descarga; si el valor no es
   `<sin_variable>`, PARA y repórtalo — no adquieras desde la nube.
3. `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/`
   — confirma red real antes de caminar la tabla entera.

## 1 · Selección de filas

Lee `data/cola-adquisicion-v1_0.tsv` completa (es la fuente viva; no leas las
cinco tablas de agosto salvo para resolver un puntero `origen` concreto que
esta caminata cite).

Elegibles para esta caminata, en este orden:

1. `estado_A4A5 == PENDIENTE`, ordenadas por `prioridad` ascendente cuando la
   prioridad es puramente numérica (filas heredadas de
   `cola-adquisicion-2026-08-12.tsv`, columna `palanca`); las filas con
   prioridad prefijada por tabla de origen (`academico-N`, `civil-N`,
   `general-N`, `oficial-N` — sin escala común con la numérica) van después,
   en el orden en que aparecen en el archivo.
2. `estado_A4A5 == NO-OBTENIDO-POR-ESTE-AGENTE(N intentos)` — **solo** si el
   operador las nombra explícitamente en `$ARGUMENTS` o si han pasado ≥7 días
   desde la última fecha registrada en su columna `nota`; un anfitrión que
   falló hace una hora no cambia de estado por reintentarlo de inmediato.

**Nunca** caminan filas `OBTENIDO` (A.8 ya resuelto) ni `NO-ACCESIBLE` (barrera
declarada — crédito, institucional, comercial — que un `curl` no cambia; si el
operador quiere reintentar una `NO-ACCESIBLE` específica, tiene que nombrarla).

Si `$ARGUMENTS` trae un número `N`, camina como máximo las primeras `N` filas
elegibles por el orden de arriba. Vacío = todas las elegibles de esta
invocación (puede ser una caminata larga — decláralo al cerrar, no la cortes
en silencio).

## 2 · A.8 por fila, ANTES de intentar nada

Para cada fila seleccionada, **antes** de la primera petición de red:

```
grep -i "<fragmento del nombre>\|<host de url_conocida si lo hay>" data/manifiesto.yaml
```

Criterio de acierto (el mismo que `ACTO ADQ-15` fijó y que este acto verificó
que sigue siendo el correcto): **host exacto de `url_origen` Y al menos un
patrón de nombre/ruta**. Un acierto de un solo lado se inspecciona a mano
antes de aceptarlo — ver `forense/notas/2026-08-18-adquisicion-material-15-fuentes.md`
§2 para el caso `GLOBAL_PREFERENCES_SURVEY` (no cruza por nombre, se habría
vuelto a bajar entera sin este paso).

- **Coincide** → no descargues nada. Actualiza la fila: `estado_A4A5=OBTENIDO`,
  `ids_manifiesto=<los ids encontrados>`, nota: `A.8: ya estaba en el
  manifiesto, no se repitió (<fecha>)`.
- **No coincide** → procede al paso 3.

⚠️ Este paso es el que el encargo llama "no re-sondea lo ya OBTENIDO" — no es
opcional ni un `try/except` alrededor de la descarga: es un `grep` que corre
primero.

## 3 · Intento de descarga programática — protocolo de rutas múltiples (ACTO MAESTRA33-A3, ADR pendiente)

Por fila, **al menos 4 rutas** se intentan (con comando y código de respuesta
crudo, cada una) antes de que la fila pueda cerrar en
`NO-OBTENIDO-POR-ESTE-AGENTE`. Ninguna ruta se salta en silencio — si una no
aplica al payload (p.ej. no existe formato alterno conocido), la nota lo dice
explícitamente («(iii) no aplica: solo hay SAV publicado»), no se omite sin
mención:

1. **(i) URL directa** del payload conocido o localizado, con UA de navegador
   real (ver reglas de abajo).
2. **(ii) API / descarga masiva del portal** — para INEGI, la canasta XML
   (precedente `ACTO O`, `ACTO P·LOTE-1/2`); para otros portales, el
   endpoint de descarga masiva o `distribution.contentUrl` (JSON-LD
   `schema.org`) si el portal lo publica.
3. **(iii) Formato alterno del mismo instrumento** — CSV↔DTA↔SAV↔XLSX; si el
   portal publica el mismo microdato en más de un formato, un formato
   bloqueado no cierra la fila mientras otro formato siga sin probar.
4. **(iv) Espejo académico o repositorio** — Datos Abiertos, IPUMS
   International, Harvard Dataverse, u otro repositorio de terceros que aloje
   el mismo instrumento. Si el espejo existe pero esta caminata no lo abre
   byte a byte (por ejemplo, requiere cuenta o el archivo es grande), márcalo
   `SIN-FETCH` en la nota — es evidencia de que la ruta existe, no un
   `OBTENIDO`.

Solo después de agotar las 4 rutas (o de anotar por qué una no aplica) la fila
puede cerrar en `NO-OBTENIDO-POR-ESTE-AGENTE(N intentos)` con su receta de
navegador (§6).

- User-Agent de navegador real en toda petición (`curl -A`), nunca el UA por
  defecto de `curl`/`requests` — varios portales de este corpus (CNBV, INEGI)
  bloquean UAs de librería antes de bloquear por IP.
- `--max-time` explícito por intento (30-60s razonable; los hosts que truncan
  TLS de este corpus — `laoms.org`, `ift.org.mx` — no se benefician de
  esperar más).
- Sin paralelismo agresivo ni barrido de rutas por fuerza bruta. Un candidato
  = como mucho unas pocas peticiones deliberadas (landing, JSON-LD/API si
  aplica, el archivo). Si la URL no se conoce, ubícala con la misma disciplina
  que `ACTO ADQ-15` documentó para INEGI: `www.inegi.org.mx` sirve `200` con
  una página de 2263 B para **cualquier** ruta inexistente (soft-404) — un
  `200` no es éxito por sí solo; compara tamaño/`Content-Type` contra un
  candidato conocido-vacío antes de aceptarlo. La vía real suele ser el
  JSON-LD `schema.org` que la página de programa incrusta
  (`distribution.contentUrl`).
- **No** intentes credenciales, formularios de registro, ni clickwrap — eso es
  exactamente lo que convierte una fila en `NO-ACCESIBLE`, no en un fallo a
  reintentar con más fuerza.

## 4 · A.7 — doble descarga si el formato puede variar sin avisar

Todo payload que SÍ llegue se baja **dos veces** y se compara:

1. `sha256` crudo — si coincide, listo.
2. Si el `sha256` crudo difiere, identifica **qué campo exacto** varía antes
   de concluir nada (contador de visitas, orden no determinista de un
   `<select>`, token rotatorio, `mtime` de un ZIP generado al vuelo son los
   cuatro patrones ya vistos en este corpus) — si el contenido de fondo
   coincide, no es `PARO`.
3. **Verifica estructura, no solo tamaño**, antes de aceptar cualquiera de las
   dos descargas como buena: `%%EOF` en PDF, directorio central legible
   (`zipfile.testzip()`) en ZIP, `json.load` limpio en JSON. `ACTO ADQ-15`
   encontró un PDF de 4 979 926 B servido por `ift.org.mx` **sin** `%%EOF` que
   una comparación de solo-tamaño habría aceptado como bueno — la doble
   descarga sin verificación de estructura no lo habría atrapado, porque las
   dos bajadas truncadas coincidían entre sí.

## 5 · Éxito

1. El payload va a `data/raw/` (el symlink al corpus compartido,
   `/home/pc0/mm-corpus/raw`). **Verifica con `ls -la data/raw` que el archivo
   vive ahí y no solo en un directorio temporal del worktree** — es el defecto
   de `PR #77`, ningún test lo atrapa.
2. `tests/manifiesto.py --registra --id <id> --usado-para "<qué fila de la
   cola satisface>" --url-origen "<url real>" --descargado-por "agente,
   directamente de <host>" --fecha-descarga <hoy, YYYY-MM-DD>` (más
   `--formato`/`--licencia`/`--nota` si aplican). El script deriva
   `sha256`/tamaño/entorno del archivo real — nunca los teclees.
3. Actualiza la fila en `data/cola-adquisicion-v1_0.tsv`:
   `estado_A4A5=OBTENIDO`, `ids_manifiesto=<id(s) nuevos>`, nota con fecha y
   comando.

## 6 · Fallo

**Nunca** escribas "no existe", "no está disponible" ni ninguna variante como
conclusión de un fallo de descarga — eso es un juicio A.5/A.6 que este agente
no está autorizado a emitir, y ni el fallo de hoy ni el conocimiento del
modelo lo sostienen. Lo único que se escribe es lo que un comando produjo.

1. Estado: `NO-OBTENIDO-POR-ESTE-AGENTE(N intentos)`, donde `N` = intentos
   previos registrados en la fila (si los hay) **+** los de esta caminata.
   Nunca reinicies el contador.
2. Nota: salida cruda relevante (código `curl`, mensaje exacto — p.ej.
   `curl 35 TLS connect error` no es lo mismo que `curl 52 Empty reply`, y la
   distinción importa para quien reintente), y si se probó dentro **y** fuera
   de algún control de red, decláralo (A.5).
3. **RECETA de navegador, ≤1 minuto, verbatim ejecutable por un humano o por
   Claude in Chrome**: URL exacta a abrir, clics necesarios en orden, nombre
   de archivo esperado al terminar. Sin esto el fallo no está completo.

## 7 · Cierre de la caminata

1. `data/cola-adquisicion-v1_0.tsv` queda con **todas** las filas caminadas
   actualizadas — ninguna se deja a medio actualizar entre estados.
2. **Paquete de recetas**, un solo bloque, todas las filas que esta caminata
   cerró en `NO-OBTENIDO-POR-ESTE-AGENTE` o que reclasificó a `NO-ACCESIBLE`,
   listas para que mesa (o Claude in Chrome) las ejecute en un barrido —no
   dispersas por el commit.
3. **CONTADOR**: payloads `OBTENIDO` antes → después de esta caminata,
   declarado (adquisición, no medición — no altera ningún falsador de
   Hito D).
4. Commit de la caminata cita esta skill y la fecha; no reabre la cascada de
   `/acto` (ADR/registro-rotulos/T25) salvo que el propio `/acto` que invocó
   esta skill lo pida en su propio CIERRE.

## Lo que esta skill no hace

No abre ni analiza el contenido semántico de ningún payload — solo verifica
integridad de contenedor (tamaño, hash, `%%EOF`/directorio central/parseo).
No compra ni crea cuentas en portales de pago o con muro de credencial: eso
convierte la fila en `NO-ACCESIBLE`, fin de esta caminata para esa fila. No
toca `milpa/**`. No re-decide la prioridad de una fila — hereda la que
`data/cola-adquisicion-v1_0.tsv` ya declara; si mesa la cambia, la cambia ahí.
