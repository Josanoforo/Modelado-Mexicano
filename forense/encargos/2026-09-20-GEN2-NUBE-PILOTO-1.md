# ENCARGO · ACTO GEN2-NUBE-PILOTO-1 · al cerrar habrá un descargador por id de manifiesto y un `REPRODUCE` de nube asentado en la vista

> **ENTORNO: NUBE (`milpa-inegi`, red `Custom`)** — el hook de arranque imprime `ENTORNO-DERIVADO`; si no coincide, PARA en una línea.

**CABECERA** · SHA de redacción `bd9ed2134021c6cd55dbf5e625dbbcb52c63d065` (PR #923, 2026-09-20 17:04 -0600; re-sellado sobre `93f68f2e`, 20 commits de deriva, todas las premisas re-derivadas contra el SHA nuevo) · **una sola sesión**, rama propia · **MODELO**: Opus (D-13) · **MODO: RÍGIDO** — la spec y el medidor de `CALC-ENIF-0001` están congelados; la latitud es sobre logística, nunca sobre el procedimiento · **CONTADOR**: mueve la vista de replay (146 → 147 filas); **no debe moverse `cuenta_gen2`** · **CALC-id reservado**: ninguno, este acto no sella corrida nueva.

Redactado contra `forense/encargos/PLANTILLA-ENCARGO-v2_0.md` e instrucciones v2.15. **Estado: aprobado por mesa (20/sep/2026), LANZABLE en cuanto exista `milpa-inegi`.**

---

## 1 · OBJETIVO

Que un acto de medición sobre microdato público corra entero en una sesión de nube, bajando por id de manifiesto solo el payload que declara y verificándolo contra su `sha256`. Habilita el sucesor de escala (los 37 ids de la demanda de PRODUCTO-DINERO, 381.6 MB, un solo host) y la decisión de mesa sobre si la adquisición sigue atada a CAJA.

**«Hecho» significa**: `python3 tools/corrida0.py verify CALC-ENIF-0001` imprime veredicto `REPRODUCE` en `milpa-inegi`, sobre un payload que bajó el descargador de la pieza 1, y su fila entra a `forense/replay-evidencia.tsv` en este mismo acto.

No es hecho: un `REPRODUCE` sellado en disco sin fila en la vista (E.7); un `NO-VERIFICABLE` presentado como `NO-REPRODUCE` (E.3); un verify sobre un payload traído a mano.

---

## 2 · FIRMAS DE MESA — verbatim

**20/sep/2026, primer input:**

> **1** — «Opción (a): solo www.inegi.org.mx en la red Custom, más la lista por defecto de gestores de paquetes. Si una descarga redirige a otro subdominio de INEGI, se reporta el host exacto y mesa lo añade; no se abre \*.inegi.org.mx por adelantado.»
>
> **2** — «Opción (a): el censo de licencias va en un TSV derivado aparte… data/manifiesto.yaml no se toca.»
>
> **4** — «desde hoy la sección de crédito de ENIF 2024 está RESERVADA por firma de mesa (PRODUCTO-DINERO): bajar el payload está permitido — es el mismo archivo que ahorro —; lo que se protege es abrirlo fuera del código autorizado, y eso vive en el medidor, no en el descargador. No lo confundas.»
>
> **5** — «"Hecho" es corrida0 verify → REPRODUCE en una sesión de nube real, con CONTEXTO declarado (será DISTINTO; NO-VERIFICABLE no se degrada a NO-REPRODUCE, E.3).»

**20/sep/2026, segundo input:**

> **6** — «FP-67 se ACOTA a cloud_default; no se sustituye hasta que el piloto mida.» La fila la escribe la pieza 3.
>
> **7** — «El censo de licencias se queda en CINCO clases.» Escribir el campo en el manifiesto NO se hace ahora: se decide cuando se arme la salida pública.
>
> **8** — «Descarga SOLO por id del manifiesto: el subcomando no acepta una URL suelta como argumento. La lista de hosts permitidos la impone el entorno; el código no debe ofrecer otra puerta.»

---

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo

Todo re-derivado contra `bd9ed213` en la sesión de dirección del 20/sep.

- `[EJECUTADO]` `git rev-list --count 93f68f2..HEAD` = **20**. Mi primer conteo dio 5 238: era un artefacto del injerto de un clon `--depth 1`, el mismo defecto que `adbdb3c0` («check.py ya no shallowea el clon que verifica») acaba de corregir en la suite. Se clonó completo y se re-derivó.
- `[LEÍDO]` `data/manifiesto.yaml` sigue en **1 629 entradas / 1 624 payloads**. La entrada del piloto: `id: enif_2024_enif_2024_bd_csv`, `archivo: enif_2024_bd_csv.zip`, `sha256: 00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039`, `tamano_bytes: 3131148`, `url_origen: https://www.inegi.org.mx/contenidos/programas/enif/2024/microdatos/enif_2024_bd_csv.zip`.
- `[LEÍDO]` Esa entrada trae **`raiz: None` literal**, no ausente. La cabecera del manifiesto dice «ausente = `data_raw`»; presente-con-valor-nulo no está cubierto por esa frase.
- `[EJECUTADO]` El `sha256` del manifiesto es idéntico al `input_sha256_efectivos` que la fila de replay de `CALC-ENIF-0001` declara. Comparación en sesión: `True`.
- `[LEÍDO]` `data/corrida0/CALC-ENIF-0001/` tiene los 7 artefactos de corrida sellada; `sello.json` fija `medidor.py = 6ac67a01…`; `spec.yaml` declara `miembro_usado: TMODULO.csv` y un segundo insumo `IN-ENIF-SPEC-SELLADA` que es **de repo** (`forense/prereg-caja/ENIF-AHORRO-spec-v1_0.md`) y no requiere descarga.
- `[LEÍDO]` La fila de replay que hoy existe para este CALC se declara a sí misma `HEREDADO-DEL-REGISTRO-PUBLICADO` / `EVIDENCIA-HISTORICA · NO es verify nuevo ni validación independiente`. **El verify de este acto sería el primero nuevo, y el primero fuera de CAJA.** Esto es lo que le da valor al piloto.
- `[LEÍDO]` `tools/corrida0.py::cmd_verify` existe (línea 2652) y toma solo `calc_id`; devuelve 0 en `REPRODUCE`, 2 en `NO-VERIFICABLE`/`NO-EJECUTABLE`. El único subcomando `NO-IMPLEMENTADO` es `vigencia`.
- `[EJECUTADO]` `python3 tools/entorno.py --arranque` corre y en la sesión de dirección imprime, textual:
  `ENTORNO-DERIVADO = INDETERMINADO` · `senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable` · `red: DENEGADA-POR-POLITICA (http_code=403, http_connect=000, x_deny_reason=host_not_allowed, via_proxy=NO)` · `data-raw-en-este-worktree: NO`.
- `[LEÍDO]` Los cuatro estados de red del hook, en `tools/entorno.py:284-297`: `PERMITIDA` (2xx/3xx) · `DENEGADA-POR-POLITICA` (403 en el CONNECT) · `RESPUESTA-NO-OK(<código>)` · `SIN-RED` (`http_code` 000 o no numérico).
- `[LEÍDO]` `tests/manifiesto.py::cmd_verifica` (líneas 666-707) ya tabula por raíz **sin colapsar** `AUSENTE` / configurada / coincide / no-coincide, con la salida cruda pegada. Los tres estados de A.1 ya están ahí.
- `[EJECUTADO]` `tests/manifiesto.py` no contiene ninguna llamada de red: `grep -E 'urllib|requests|urlopen|httpx'` sobre sus 1 740 líneas → 0 coincidencias.
- `[EJECUTADO]` Ningún archivo de `tests/` ni `tools/` usa `http.server`/`HTTPServer`/`socketserver`: `NO-ENCONTRADO`, universo los dos árboles completos. El arnés de la pieza 1 no tiene precedente que reutilizar; se escribe.
- `[EJECUTADO]` Los 22 ids `banxico_sie_*` siguen en el manifiesto; nueve de ellos tienen `url_origen` que termina en `.do` (endpoints de servlet del SIE). Mi primera regla de clasificación los daba por descargables. **Ése es el caso de prueba que firma mesa.**
- `[REPORTADO]` `milpa-inegi` existe y permite `www.inegi.org.mx`. Lo crea mesa fuera de esta conversación. **No lo he visto.** Verifícalo con el hook antes de tocar nada; si `red` no dice `PERMITIDA`, es el PARO (e).

---

## 4 · YA HECHO / YA DECIDIDO — búsqueda por objeto

Hecho por dirección el 20/sep sobre el clon (universo: 6 268 archivos, luego 6 268+ tras la deriva):

- **Descarga por id**: `NO-ENCONTRADO`. Ningún punto de entrada del repo descarga por id de manifiesto. Los cinco archivos con red (`tools/adq_enoe_*.py`, `tools/adquiere_cron.sh`, `tools/curador_registro/semantic_run.py`) son específicos de fuente. `tools/barrido_descargas_vs_manifiesto.py` (80 líneas, leído entero) es de solo lectura y cruza carpetas locales contra el manifiesto por `sha256`.
- **Decisión de mesa sobre descargas en nube**: `EXISTE-SATISFACE` — `FP-67`, cerrada 19/ago/2026 (`PR #293`, `ADR-127`), asigna la adquisición a UBUNTU porque la nube tiene el egreso a INEGI bloqueado. Estado re-verificado (A.17): sigue cerrada. **Manda, y por eso la pieza 3 existe**: la firma 6 la acota a `cloud_default` en vez de sustituirla. Los otros cinco archivos de lote-nube de agosto declaran los cinco que no descargaron nada.
- **Plantilla de encargo v2.0**: `EXISTE-SATISFACE`. Nació en `fe1c895b` (GEN2-V215), después de mi lectura en `93f68f2`. Mi `NO-ENCONTRADO` anterior era correcto contra aquel SHA y queda **vencido en alcance** (A.10). Este encargo se redacta contra ella.

**Al ejecutor: repite esta búsqueda con tu acceso, que es mejor que el mío.** Si algo de esto ya está hecho, el entregable es decirlo y hacer solo lo que falte.

---

## 5 · PIEZAS — resultado esperado, no receta

### Pieza 1 · El descargador, como subcomando de `tests/manifiesto.py`

**Produce**: un punto de entrada que, dado uno o más `--id` del manifiesto, deja el payload verificado en `data/raw` o dice por qué no, con vocabulario A.4.

No es herramienta nueva (D-14): extiende el punto de entrada que ya gobierna el manifiesto y **hereda de `cmd_verifica` los tres estados de A.1** en vez de reimplementarlos. Si hace falta un estado cuarto («descargado ahora»), se añade sin tocar los tres.

**Contrato que `COMMIT-1` congela:**

- **Solo por id.** El subcomando **no acepta una URL suelta como argumento** (firma 8). La lista de hosts la impone el entorno; el código no ofrece una segunda puerta.
- **Clasificación antes de tocar la red**, derivada y no adivinada: ruta que termina en extensión de archivo → descargable; página de catálogo, buscador o servlet → `NO-ACCESIBLE` con el motivo; `url_origen` que no es http → `NO-ACCESIBLE` con el valor crudo a la vista.
- **`raiz`**: ausente y presente-con-valor-nulo se resuelven explícitamente y se declara cuál se usó. Prohibido `raiz or 'data_raw'` en silencio.
- **Guardias en el código** (E.6): se niega ante los cuatro ids con `estado_reserva` (`enco_2025_junio_dbf_reservado`, `enco_2026_junio_dbf_reservado`, `enco_fd_v5_reservado`, `enco_manual_procedimientos_reservado`). **No** se niega ante `enif_2024_enif_2024_bd_csv`: la reserva de la sección de crédito de ENIF 2024 se protege en el medidor, no aquí (firma 4). Un descargador que la bloqueara estaría protegiendo lo que no le toca.
- **`sha256`** calculado sobre lo descargado contra el del manifiesto; discordante → el archivo no entra a `data/raw`.
- **Redirección**: se reporta el host final exacto; distinto de `www.inegi.org.mx` → para (firma 1).
- **No escribe en `data/manifiesto.yaml`** (firma 2).

**Cómo se sabe que quedó bien — D-22, y esto va antes de la primera descarga real:** el punto de entrada corre **de punta a punta contra un servidor HTTP local de prueba** (`http.server` de la stdlib basta; no hay precedente en el repo que reutilizar), sobre cuatro escenarios: archivo bueno · `sha256` discordante · redirección a otro host · `404`. Un medidor cuyas pruebas solo ejercitan guardias y constantes no es un `COMMIT-1`. A eso se añade el caso de regla: los nueve ids `banxico_sie_*` con `url_origen` terminada en `.do` deben salir `NO-ACCESIBLE` sin tocar la red.

`COMMIT-1` cierra con: *«el primer resultado que produzca este procedimiento es el que se reporta»*.

**Si `[REPORTADO] milpa-inegi permite el host` resulta falso** → PARO (e), y el reporte es el entregable. Las pruebas contra servidor local **sí se pueden correr igual** y se entregan: dejan la pieza 1 lista para el día que el entorno exista.

### Pieza 2 · El piloto — `CALC-ENIF-0001` en nube

**Produce**: un veredicto de replay con sus dos ejes declarados y su fila en la vista.

1. Arranque con `python3 tools/entorno.py --arranque`. **No reimplementes la sonda A.2**: el hook ya la trae en cuatro estados. En `milpa-inegi` la línea `red:` debe decir **`PERMITIDA`**. Si dice `DENEGADA-POR-POLITICA`, `RESPUESTA-NO-OK(<código>)` o `SIN-RED`, es el PARO (e) — y los tres son hechos distintos que no se colapsan al reportarlos.
2. Bajar **un solo id** con la pieza 1: `enif_2024_enif_2024_bd_csv`, 3 131 148 B. Nada más.
3. `python3 tools/corrida0.py verify CALC-ENIF-0001`.
4. Declarar **los dos ejes por separado** (E.3): `RESULTADO` ∈ {REPRODUCE, NO-REPRODUCE, NO-EJECUTABLE} y `CONTEXTO` ∈ {IDENTICO, DISTINTO, NO-VERIFICABLE}. Mesa ya anticipó que el CONTEXTO será `DISTINTO` —el sello original es de CAJA (Ubuntu) con corpus montado; éste es nube con corpus descargado— y **eso no degrada el RESULTADO**. `NO-VERIFICABLE` no se escribe como `NO-REPRODUCE`.
5. Fila nueva en `forense/replay-evidencia.tsv` **en el mismo acto** (E.7), con `procedencia` = verify nuevo en nube y `alcance` diciendo qué la distingue de la fila heredada. La fila vieja no se edita ni se borra. **Escritura en texto plano `split`/`join`, nunca `csv.writer`**: el re-entrecomillado corrompe los TSV de esta casa (`ADR-123(h)`, y §4 del cierre de `LOTE·NUBE-DECISIONES-1`).

**Si el medidor congelado no corre en nube** → PARO (g), no se parcha. Ése es el resultado del acto y se reporta.

### Pieza 3 · El asiento de FP-67

**Produce**: la fila que acota `FP-67` a su universo, por firma 6.

La asignación «adquisición va a UBUNTU» se midió contra `cloud_default` y queda **vencida en alcance** (A.10) para el entorno con red `Custom`. **No se edita la fila vieja**: se añade una nueva con su universo a la vista y con el resultado real de la pieza 2.

**Si la pieza 2 no da `REPRODUCE`, esta pieza se escribe igual**, con lo que haya salido. Saber que la nube tampoco puede con red abierta es un hallazgo, no un fracaso, y es justo lo que mantiene a FP-67 vigente en su forma actual.

---

## 6 · LATITUD

**Decides tú, y lo dices en la nota**: la forma del descargador y de su arnés · el orden de las piezas · nombres de archivo · la ruta de montaje de `data/raw` · reintentos y tiempos de espera · remover obstáculos reversibles y baratos (crear o enlazar `data/raw`, `fetch --unshallow`, instalar una dependencia, regenerar un derivado por comando) · arreglar un defecto adyacente de ≤10 líneas que te impida terminar, declarándolo.

**Preguntas a mesa, con 2–3 opciones y tu recomendación, y sigues con lo demás**: cualquier bifurcación no prevista que cambie qué se entrega.

**No decides**: nada de la sección 7.

`main` movido, `data/raw` ausente al arrancar, un `404` o `503` de INEGI en el primer intento: **ninguno es PARO.** Se resuelven y se declaran.

---

## 7 · PAROS — lista cerrada. Fuera de ella no se para: se resuelve o se pregunta

- **(a)** abrir, derivar o imprimir dato de una ola reservada fuera del código autorizado — aquí: abrir la sección de crédito de ENIF 2024 (firma 4).
- **(b)** borrar, forzar (`-D`, `--force`, `clean`) o reescribir algo sellado — aquí: `data/corrida0/CALC-ENIF-0001/*` y la fila de replay existente.
- **(c)** adoptar, o mover `cuenta_gen2`.
- **(d)** cambiar estimando, universo, umbral, candidato o código de un procedimiento congelado — aquí: tocar `spec.yaml`, `medidor.py` o cualquier `sello.*` para que el verify corra.
- **(e)** entorno equivocado — aquí: el hook no dice `red: PERMITIDA`, o `ENTORNO-DERIVADO` no es el declarado.
- **(f)** el OBJETIVO dejó de ser alcanzable o de tener sentido → PARO, y eso es el entregable.
- **(g)** (MODO RÍGIDO) el código congelado no corre → no se parcha.

Dos paros propios de este acto, que caen bajo (d) y (a) pero conviene nombrar: **el `sha256` de lo descargado no coincide con el del manifiesto** — el payload no es el que la corrida selló, y no se «continúa para ver»; **la descarga redirige a un host distinto de `www.inegi.org.mx`** — se reporta el host exacto y mesa lo añade (firma 1), no se abre por cuenta propia.

---

## 8 · COMPUERTAS — cada una declara qué protege

- `tools/entorno.py --arranque` dice `red: PERMITIDA` y `ENTORNO-DERIVADO` coincide, **antes de descargar** → protege: **abrir dato**.
- `sha256` verificado antes de que el payload entre a `data/raw` → protege: **abrir dato**.
- `COMMIT-1` con el descargador y sus cuatro pruebas contra servidor local corridas, **antes de cualquier descarga real** (D-22) → protege: **congelar spec**.
- Fila en `forense/replay-evidencia.tsv` en el mismo acto que el verify → protege: **adoptar**.

Nada más es compuerta. El orden de las piezas es orden sugerido.

---

## 9 · PERÍMETRO

**Propio**: `tests/manifiesto.py` · el test del subcomando nuevo y su arnés HTTP local · `forense/replay-evidencia.tsv` (append) · `forense/firmas-pendientes.tsv` (append) · `forense/hallazgos.md` · `forense/notas/2026-09-XX-nube-piloto-1-cierre.md` · `canon/gobernanza-*.md` (ADR) · este encargo, marcado `CONSUMIDO`.

**Ajeno que no se toca**: `data/manifiesto.yaml` (firma 2 — y el escritor de la casa es `--registra`, en acto propio) · `data/corrida0/CALC-ENIF-0001/*` (sellado) · cualquier otro `CALC-*` · `milpa/` y `canon/modelo-decision*` (son de PRODUCTO-DINERO) · `tests/baseline.json`.

**PERÍMETRO DE CIERRE — permanente, no hay que pedirlo** (D-21): cablear en CI el test propio · publicar en la vista las filas propias y su asiento de replay · registrar en `data/INFRAESTRUCTURA-v1_0.md` lo que este acto añada al dominio 1 (adquirir/registrar payload) · la cascada de `/acto` · hallazgos, NC y FP propios.

Fuera del perímetro y necesario para terminar → es **latitud** (≤10 líneas, declarado) o es **pregunta**. `FUERA-DE-PERÍMETRO` como razón de una NC queda para lo que de verdad es de otro acto.

**Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.**

---

## 10 · LO QUE NO HACE · SUCESORES · CIERRE

**No hace**: no baja los 37 payloads de la demanda de dinero, baja **uno** · no resuelve ninguna URL de página · no escribe el campo `licencia` en el manifiesto (firma 7: se decide cuando se arme la salida pública) · no adquiere ENIGH 2024 ni los cuestionarios de ENIF 2012/2015 · no adopta ninguna cifra · no toca la sección de crédito de ENIF 2024 · no sustituye FP-67, solo la acota.

**No generaliza, y el cierre debe decirlo con estas palabras** (mesa pidió que vaya verbatim): *un `REPRODUCE` sobre un payload de 3.1 MB en un host no demuestra que 18.4 GB en 200 hosts funcionen. El piloto prueba que el carril existe, nada más.*

**Sucesores declarados, no lanzados**:
- `NUBE-PILOTO-2` — el mismo descargador sobre los 37 ids de demanda D1 (381.6 MB, un host). **Es el que empieza a demostrar escala.** Mientras tanto, PRODUCTO-DINERO corre su comparabilidad de crédito en caja.
- Carril de adquisición: ENIGH 2024, y los cuestionarios de ENIF 2012 y 2015 — **éstos dos primero**: sin ellos PRODUCTO-DINERO no puede comparar por texto esas dos olas.
- Acto de mesa sobre escribir `licencia` en el manifiesto, cuando se arme la salida pública.

**AUDITORÍA**: no aplica. Este acto no afirma nada sobre México; verifica un carril.

**CIERRE**: ADR del acto (número derivado por el comando de la casa al escribir **y** al fusionar; renumera quien fusione segundo) · FP/NC propios derivados, no heredados · `## NO-CORRIDO / RESERVAS` antes de `## CONSUMIDO`, con «Ninguno.» obligatorio si no hubo (A.14) · `tests/check.py --baseline` VERDE o PARO · rama fusionada o borrada (política de cero ramas).

## `## NO-CORRIDO / RESERVAS`

Llenado por `ACTO GEN2-NUBE-PILOTO-1-bis` (21/sep/2026), que reanuda este encargo tras dos intentos que no llegaron a main.

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| **Pieza 2 · El piloto: `CALC-ENIF-0001` en nube** — no corrida por `PR #930`, que paró por PARO (e) en `cloud_default` | `SUSTITUIDO-POR:GEN2-NUBE-PILOTO-1-bis` | Ninguno pendiente. **Qué absorbe el sustituto:** la pieza 2 entera (descarga con la pieza 1 + verify + asiento E.7), corrida aquí con `RESULTADO=REPRODUCE` / `CONTEXTO=DISTINTO`, y la pieza 3 (`FP-404`). **Qué queda huérfano: nada** — la pieza 1 de aquel acto se rescata intacta (`sha256` verificado), su medición de `cloud_default` se incorpora citada a `FP-404` y a la nota, y sus tres líneas de hallazgos se conservan íntegras | `CERRADA` por este mismo acto. Fila `NC-0433`. Escala: `NUBE-PILOTO-2` |
| **Perímetro de cierre permanente (D-21) · cierre anti-PR#77**: «verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree» | `NO-VERIFICABLE-AQUÍ` — en esta caja no hay corpus compartido que verificar: con `data/raw` vacía el hook da `senal-corpus: montado=VACIO archivos_examinados=0` (A.13), no existe `data/raices.local.yaml`, y el contenedor es efímero. **No es un negativo sobre el corpus compartido** (existe y vive en CAJA): es un hecho sobre esta caja (A.5) | Ningún contador. El verify ya consumió el payload y su fila de replay está asentada con el `sha256` a la vista, así que la evidencia no depende de que el archivo sobreviva. Lo abierto es de escala: 381.6 MB en una caja efímera se bajarían una vez por sesión y se tirarían | `NUBE-PILOTO-2` — debe declarar en su spec dónde aterrizan los payloads **antes** de bajar 37 ids. Fila `NC-0434` |
| **Pieza 2, paso 3** — corregir que `corrida0.py verify` devuelva `1` (no `0`) con `RESULTADO=REPRODUCE` y `CONTEXTO=DISTINTO` | `FUERA-DE-PERÍMETRO` — es de `tools/corrida0.py`, que §9 lista como ajeno; y cambiar el contrato de salida de un verificador sellado no es un defecto adyacente de ≤10 líneas | Ninguno en este acto: el veredicto se lee de los dos ejes. El riesgo es de un sucesor que gatee por `rc == 0` y convierta un `REPRODUCE` legítimo en falso negativo — justo lo que `NUBE-PILOTO-2` haría al encadenar 37 verificaciones | `GEN2-CORRIDA0-RENDIMIENTO-1` o el acto que toque `tools/corrida0.py`. Fila `NC-0435` |

**Dejado fuera a propósito, declarado:** la fila `NC-0343` que `PR #930` añadía es de `GEN2-FAM-UNION-ESTIMANDO-1` (`PR #880`), acto ajeno y fuera del perímetro de §9. Ya existe en `origin/main` con su dueño y `estado = ABIERTA`, y este acto no produjo evidencia que la cierre: no se re-añade ni se toca.

Todo lo demás del encargo se corrió: las tres piezas completas, las cuatro compuertas evaluadas, el perímetro de cierre (CI cableado, filas publicadas en la vista, Dominio 1 registrado, cascada corrida, hallazgos/NC/FP propios derivados). **Ningún PARO de la lista cerrada de §7 se disparó en este acto** — el PARO (e) que paró a `PR #930` no se reprodujo: `red: PERMITIDA`.

## `## CONSUMIDO`

A llenar con el PR al cierre (A.3).
