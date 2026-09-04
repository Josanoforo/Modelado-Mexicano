---
description: Dada la definición de una celda o θ, corre ≥3 formulaciones de búsqueda con tools/busca_reactivos.py, devuelve tabla de candidatas con vocabulario A.4 y una recomendación que DIRECCIÓN revisa. Uso — /mapea <código> <definición verbatim>
argument-hint: <código celda/θ> <definición verbatim de la fila>
---

# `/mapea` — propone, no decide

Creada por `ACTO MAESTRA33-E7 · MAPEADOR-1` (31/ago-1/sep/2026). El
argumento es un código de celda o θ (`CIV-08`, `radio_confianza`, lo que
sea) y su definición **verbatim**, copiada de la fila que la nombra (el
marco, un tablero, un encargo) — esta skill nunca inventa ni parafrasea
la definición de entrada, y nunca abre el marco congelado ni el
crosswalk por su cuenta para completarla: si el operador no trae
definición, PARA y pídela.

Esta skill **propone candidatas, no decide** cuál usa el motor. La
decisión — sellar una candidata, pedir adquisición nueva, o dejar la
celda `NO-ENCONTRADO` — es de DIRECCIÓN. Nada de lo que sigue escribe una
regla ni una spec (fuera de perímetro, ver `LO QUE NO HACE` al final).

---

## 1 · Arranque mínimo

Si esta invocación corre dentro de un `/acto` que ya hizo su propio
ARRANQUE, no lo repitas. Si corre sola: `ls tools/busca_reactivos.py` —
si falta, PARA (esta skill no funciona sin su P1). No toca `data/raw`,
no toca red: las dos tablas que `busca_reactivos.py` lee son metadato de
texto ya extraído.

## 2 · Deriva ≥3 formulaciones de la definición

Ninguna formulación se copia de una corrida anterior sobre otra celda —
cada una sale de LEER la definición de este argumento. Como piso, tres
formulaciones de naturaleza distinta (no tres sinónimos del mismo
sustantivo):

1. **Literal** — las palabras de la definición tal cual (sustantivo y
   verbo principal), plegadas. Si la definición es una frase completa
   («ayuda para bañarse»), prueba también la subcadena más corta que
   siga siendo específica («bañarse»/«bañar» antes que «ayuda», que es
   genérico y ahoga la señal con ruido).
2. **Sinónimo/alterno** — cómo un instrumento distinto nombraría lo
   mismo (registro civil vs. coloquial, término INEGI vs. términos de
   otras encuestas — p.ej. «cónyuge» junto a «esposo/esposa/pareja»).
3. **Regex de variable o patrón compuesto** — cuando la definición trae
   un candidato de nombre de variable reconocible (siglas, patrón tipo
   `SITUA_CONYUGAL`) o cuando el literal solo (paso 1) da demasiado
   ruido y hace falta `--regex` con alternancia (`a|b|c`) para acotar en
   una sola pasada.

Declara las ≥3 formulaciones ANTES de correr la primera — moverlas
después de ver un resultado parcial es exactamente el defecto que
`revisa.md` (punto 2) nombra para otro contexto: decidir el criterio
después de ver el dato invalida el criterio.

Si la definición ya nombra la encuesta candidata (p. ej. viene con
"ENVIPE" al lado), una de las ≥3 corre **sin** `--encuesta` de todas
formas — un filtro de encuesta equivocado no debe esconder un acierto en
otra fuente; correr al menos una formulación abierta es lo que lo
atrapa.

## 3 · Ejecuta cada formulación

```
python3 tools/busca_reactivos.py --palabra "<término>" [--palabra "<término-2>" ...] \
    [--encuesta <substr>] [--tipo <substr>] --limite 30
```

La salida declara qué tabla(s)/raíz(ces) examinó (`--tablas`, o `hoy` por
defecto = v1_2+ext); esa línea de universo (A.13) va literal a la tabla
del paso 5 — declara también, en la misma nota, qué tabla NO se corrió
(p.ej. `descargas_mx` si `--tablas` no la incluyó), para que un
`NO-ENCONTRADO` no se lea como cobertura total del corpus cuando no lo fue
(cierra `DE1`, `forense/hallazgos.md`).

o con `--regex "<patrón>"` en vez de `--palabra`. Corre las ≥3 tal como
se declararon en el paso 2 — no edites una formulación a media corrida.
Copia el comando exacto y su línea `# candidatas: N total, mostrando M`
(la salida ya trae el universo examinado, A.13 — no lo vuelvas a
calcular a mano).

## 4 · Clasifica cada candidata distinta con vocabulario A.4

Unifica las filas que las ≥3 formulaciones devolvieron (una candidata
puede repetirse entre formulaciones — cuenta una vez, cita cuál
formulación la trajo primero). Para cada candidata distinta:

- **`EXISTE-SATISFACE`** — el `texto`/`variable` de la candidata
  operacionaliza la definición sin faltante: el reactivo pregunta,
  literalmente o por equivalencia directa, lo que la definición pide.
- **`EXISTE-NO-SATISFACE`** — hay candidata en el dominio correcto pero
  falta algo (ventana temporal, unidad de análisis, universo, o mide un
  parámetro adyacente y no el que la definición nombra). **Declara qué
  falta en la misma línea** — no basta con el rótulo.
- **`NO-ENCONTRADO`** — ninguna candidata en el universo examinado sirve.
  **Declara con qué términos y sobre qué universo se buscó** (A.4) — las
  ≥3 formulaciones del paso 2, tal cual, son esa declaración; no se
  resume como "no se encontró nada".
- **`NO-ACCESIBLE`** — solo si `busca_reactivos.py` no pudo correr sobre
  alguna fuente declarada (falta el archivo, error de lectura). Distinto
  de `NO-ENCONTRADO`: A.13 — cero filas examinadas no es un negativo, es
  un comando que no corrió.
- **`NO-ADQUIRIDA-POR-COSTO`** *(D5, firma de mesa 3/sep/2026, propagado
  por `ACTO MAESTRA37-N8 · CONSOLIDA-DECISIONES`)* — la fuente es
  comercial, con costo declarado (ALTO u otro), y mesa **decide no
  contratarla**, sin haber contactado al proveedor. **Distinto de
  `NO-ACCESIBLE`**: `NO-ACCESIBLE` es un muro técnico o de credencial que
  un agente no pudo cruzar; `NO-ADQUIRIDA-POR-COSTO` es una decisión de
  mesa sobre presupuesto, con la fuente en principio alcanzable si
  alguien pagara. No se reclasifica a `NO-ACCESIBLE` sin que mesa lo
  reabra.

Un `NO-ENCONTRADO` de agente **no cierra** una fila de la cola de
adquisición: la cierra mesa, con el informe de hermanas a la vista
(firma de mesa, 3/sep/2026). Un agente puede clasificar, nunca adjudicar
el cierre de una fila.

Un `texto_reactivo` vacío en la candidata (frecuente — ver docstring de
`busca_reactivos.py`) no es por sí solo `NO-ENCONTRADO` de esa fila: se
clasifica por lo que `variable`/`tabla` sí dan a leer, con esa limitación
declarada en la nota.

## 5 · Tabla de salida + UNA recomendación

Devuelve, por código consultado:

```
### <código> — "<definición verbatim>"

Formulaciones corridas: (1) ... (2) ... (3) ...

| candidata | encuesta | ola | tabla | variable | texto | tipo | en_corpus | A.4 |
|---|---|---|---|---|---|---|---|---|
| v1_2:NNNNN | ... | ... | ... | ... | ... | ... | SI/NO | EXISTE-SATISFACE |

**Nota por candidata que no sea EXISTE-SATISFACE limpio:** qué falta o
qué términos/universo se agotaron (A.4), una línea cada una.

**RECOMENDACIÓN (propuesta, no sellada):** una frase — cuál candidata
(si hay `EXISTE-SATISFACE`), o "ninguna candidata satisface; universo
agotado, considerar adquisición" (si todo cae `NO-ENCONTRADO`/
`EXISTE-NO-SATISFACE`). Sin verbo de decisión ("se adopta", "se sella")
— DIRECCIÓN es quien decide.
```

Si el mismo código ya tiene un reactivo propio conocido por otra vía
ajena a esta búsqueda (crosswalk, marco), esta skill no lo verifica ni
lo cita — está fuera de su perímetro (ver abajo); la tabla de arriba es
únicamente lo que la búsqueda por definición encontró.

## Lo que esta skill no hace

No decide cuál candidata usa el motor — DIRECCIÓN revisa la
recomendación y sella aparte. No escribe reglas de `milpa/tramite.yaml`
ni specs nuevas. No abre microdato — solo las dos tablas de texto de
`busca_reactivos.py`. No abre ni edita el marco congelado ni el
crosswalk `procedencia.yaml`/`tramite.yaml` — la definición de entrada
es la única fuente de la consulta. No reintenta una formulación ya
corrida con el mismo término esperando un resultado distinto.
