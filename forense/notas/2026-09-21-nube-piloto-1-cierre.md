# Cierre · ACTO GEN2-NUBE-PILOTO-1

**Encargo:** `forense/encargos/2026-09-20-GEN2-NUBE-PILOTO-1.md` (archivado verbatim por A.3 en el 0-bis de esta sesión; SHA de redacción declarado `bd9ed2134021c6cd55dbf5e625dbbcb52c63d065`; sha256 del archivado `ed67f208d41058fec391e1059ba267b3451ddde368d25cb6df3aae90d0bb3fc3`).
**Base:** `b8438d7`, `HEAD..origin/main` = 0 y `origin/main..HEAD` = 0 tras `git fetch --prune`.
**Modo:** `RÍGIDO`. **Sesión:** una. **Rama:** `claude/new-session-lvyz4s`.

## 0 · Veredicto en una línea

**PARO (e) — entorno equivocado.** La premisa `[REPORTADO]` del encargo («`milpa-inegi` existe y permite `www.inegi.org.mx`») se verificó y **cayó**: esta sesión corrió en `cloud_default` con el egreso a INEGI bloqueado. Las piezas 2 y 3 dependían de ella de formas distintas: la **pieza 2 no se corrió** (`NC-0423`, `PARO-ENTORNO`); la **pieza 1 se entregó entera**, como el propio encargo previó para este caso; y la **pieza 3 se escribió con lo que salió**, que es el resultado real de medir `cloud_default`.

`cuenta_gen2` **no se movió**. `forense/replay-evidencia.tsv` **no se movió**: sigue en **147** filas.

## 1 · ARRANQUE (Bloque D, verbatim de la salida)

Clon existente, no se clonó nada: `/home/user/Modelado-Mexicano`, `b8438d7 Merge pull request #926 …`, `git status --porcelain` vacío.

Guard de arranque, las cuatro:

- **0.a** `git fetch --prune` · `git rev-list --count HEAD..origin/main` = **0**. (El hook de `SessionStart` había impreso `detras=535 adelante=452` — es una lectura **sin fetch** sobre refs rancias del clon recién nacido; tras el fetch, la base está al día. No es PARO y no hubo merge que hacer.)
- **0.b** árbol limpio.
- **0.c** duplicado: `git ls-remote --heads origin | grep -i nube-piloto` → sin coincidencia · `git worktree list` → 1 (éste) · PR abiertos (`mcp__github__list_pull_requests`, `state=open`, 30 por página) → 1 PR abierto, `#928`, rótulo `GEN2-RELEVO-RECONCILIA-1`, no es éste. Sin duplicado.
- **0.d** higiene, salida cruda:

```
LIMPIA-ARBOL · REPORTE (nunca escribe)
  A · worktrees vivos: 1   [git worktree list --porcelain]
      /home/user/Modelado-Mexicano  rama=refs/heads/claude/new-session-lvyz4s
  B · ramas locales ya fusionadas a origin/main y vivas: 1
      claude/new-session-lvyz4s
  C · base: HEAD esta 0 commits detras de origin/main (al_dia=SI)
  D · ramas remotas sin PR abierto -> fuera_de_politica: NO-VERIFICABLE-SIN-GH
```

**ENTORNO (A.2, tres partes, una sola invocación, salida cruda):**

```
ENTORNO-DERIVADO = NUBE
senal-corpus: montado=NO archivos_examinados=0
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403, x_deny_reason=ausente, via_proxy=SI)
head-vs-origin/main: detras=0 adelante=0 (sin fetch)
worktrees: 1
es-worktree: NO
ramas-locales-con-commits-propios: 1/2
data-raw-en-este-worktree: NO
```

`data/raw` ausente al arrancar: **no es PARO**, se creó (vacía). `data/raices.local.yaml` **ausente** en este clon (gitignorado) — de ahí que la raíz `descargas_mx`, que 335 entradas del manifiesto declaran, resuelva aquí como `RAIZ-NO-CONFIGURADA` y no como `AUSENTE` (A.1, los dos estados no se colapsan).

**Espejo:** ninguna cifra de esta nota sale del espejo del proyecto. Todas se derivaron en esta sesión sobre el clon, con el comando a la vista.

## 2 · El PARO (e), medido por dos vías independientes

El encargo asigna `milpa-inegi` con red `Custom` y exige, como compuerta de **abrir dato**, que el hook diga `red: PERMITIDA` **antes de descargar**.

1. **Hook** (arriba, verbatim): `red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403, x_deny_reason=ausente, via_proxy=SI)`.
2. **El descargador congelado en el `COMMIT-1` de este acto**, contra el id del piloto, salida cruda:

```
enif_2024_enif_2024_bd_csv [data_raw]: NO-OBTENIDO -- NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO(S)
  -- intento 1/1: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
  · receta manual de un minuto: abre https://www.inegi.org.mx/contenidos/programas/enif/2024/microdatos/enif_2024_bd_csv.zip
    en un navegador, guarda el archivo como 'enif_2024_bd_csv.zip' en la raíz 'data_raw', y corre
    `python3 tests/manifiesto.py --verifica --id enif_2024_enif_2024_bd_csv`
    raíz resuelta: AUSENTE -> data_raw (cabecera de data/manifiesto.yaml)

RESUMEN por estado (sin colapsar):
  NO-OBTENIDO: 1
  ids examinados: 1 · entradas leídas del manifiesto: 1629
  data/manifiesto.yaml: NO ESCRITO (firma de mesa 2)
```

Los tres hallazgos que §2 de las instrucciones prohíbe colapsar, separados: esto es **«no pude alcanzar la fuente»** (el CONNECT del proxy devuelve 403 antes de que haya una respuesta de INEGI), **no** «la fuente no tiene el dato» y **no** «nadie corrió el mecanismo contra esta fuente» — el mecanismo se corrió, y es suyo el veredicto. A.5: el fallo es un hecho sobre **este agente en este entorno**, no sobre el portal de INEGI, del que esta sesión no sabe nada.

**Orden declarado, no implícito:** esta sonda se corrió **antes** del `COMMIT-1` que la compuerta de «congelar spec» exige que la preceda. No obtuvo payload, no abrió dato y no movió contador, y su resultado es el primero que el procedimiento produjo y el que aquí se reporta — pero el orden fue el equivocado y va como hallazgo, no como nota al pie.

## 3 · Premisas verificadas — tres caen

Todas contra `b8438d7`, con comando a la vista. Ninguna de las tres toca *qué se mide* ni una firma de mesa, así que ninguna es PARO por sí sola (§2 de v2.15): son de estado del repo, se replantean y se declaran.

| Premisa del encargo | Rótulo | Veredicto | Medido |
|---|---|---|---|
| `data/manifiesto.yaml` en 1 629 entradas / 1 624 payloads | `[LEÍDO]` | **1 629 entradas ✓ · 1 625 payloads** (no 1 624) | `len(ents)`; `sum(1 for e in ents if e.get('url_origen'))` |
| Entrada del piloto: id, archivo, sha256, `tamano_bytes` 3 131 148, `url_origen` | `[LEÍDO]` | **SE SOSTIENE**, campo por campo | lectura de la entrada |
| La entrada trae **`raiz: None` literal**, no ausente | `[LEÍDO]` | **CAE** — `raiz` está **ausente**. Censo del campo en las 1 629: 1 013 ausente · 335 `descargas_mx` · 277 `data_raw` · 4 `reserva_respondentes` · **0 nulos** | `Counter` sobre el campo |
| Cuatro ids con `estado_reserva` | `[LEÍDO]`/guardia | **SE SOSTIENE**: exactamente 4, los que el encargo nombra | filtro por campo |
| **22** ids `banxico_sie_*`, **nueve** con `url_origen` terminada en `.do` | `[EJECUTADO]` | **CAE en los dos números** — son **9** ids, y **0** terminan en `.do` | filtro por prefijo y `endswith('.do')` |
| `tools/corrida0.py::cmd_verify` existe y toma solo `calc_id` | `[LEÍDO]` | no re-verificado en profundidad: la pieza 2 no llegó a invocarlo | — |
| Ningún archivo de `tests/`/`tools/` usa `http.server` | `[EJECUTADO]` | **SE SOSTIENE**: sin precedente que reutilizar; el arnés se escribió | `grep` sobre los dos árboles |
| `milpa-inegi` existe y permite `www.inegi.org.mx` | `[REPORTADO]` | **CAE** — §2 de esta nota | hook + descargador |

**Búsqueda por objeto, repetida con mi acceso (A.8, A.4).** «Descarga por id de manifiesto»: `NO-ENCONTRADO`, universo los **6 298** archivos del clon en `b8438d7`, búsqueda por punto de entrada y por llamada de red. Se confirma lo que la propia cabecera de `tests/manifiesto.py` declara desde el 30/jul como desvío abierto: *«el momento de la descarga en sí sigue sin instrumentar — ahí nacieron los dos hashes tecleados a mano que este script existe para evitar»*. La pieza 1 cierra ese hueco.

## 4 · Pieza 1 — entregada y congelada

`COMMIT-1`: `tests/manifiesto.py --descarga` + `tests/test_descarga_manifiesto.py`. *El primer resultado que produzca este procedimiento es el que se reporta.*

No es herramienta nueva (D-14): extiende el punto de entrada que ya gobierna el manifiesto y **hereda** de `tests/payload_resolver.py` los estados de A.1 en vez de reimplementarlos. El único estado añadido es el cuarto que el encargo autorizó, `DESCARGADO-AHORA`.

Contrato congelado, punto por punto del encargo:

- **Solo por id** (firma 8). `--descarga` exige `--id`; **ningún** parámetro acepta una URL, con ningún nombre, y el test lo verifica leyendo la fuente de `cmd_descarga`. El **host esperado se deriva del `url_origen` que la propia entrada declara** — así no hay lista de hosts tecleada en el código, y por tanto no hay una segunda puerta que ampliar por cuenta propia.
- **Clasificación antes de tocar la red**, sobre `urlsplit(url).path` y no sobre la URL cruda: servlet · página · ruta sin extensión · URL que no es http(s) · valor con prosa → `NO-ACCESIBLE` con el motivo y el valor crudo a la vista.
- **`raiz`**: `resolver_raiz_declarada` devuelve `(nombre, procedencia)` y distingue **ausente**, **presente-con-valor-nulo** y **declarada**. Prohibido y ausente el `entrada.get("raiz", RAIZ_INTEGRADA)` silencioso en este camino. La línea `raíz resuelta: …` sale en cada resultado.
- **Guardia E.6**: se niega ante las cuatro entradas con `estado_reserva`, antes de tocar la red. **No** se niega ante `enif_2024_enif_2024_bd_csv` (firma 4) — verificado explícitamente en el test.
- **`sha256`** calculado sobre lo bajado y comparado contra el del manifiesto **antes** de que el archivo entre a su raíz; discordante → no entra, y el `.parcial` se conserva para inspección.
- **Redirección**: no se sigue **ninguna**. Comparar el host después de seguir el 30x ya habría abierto la conexión al host nuevo; el handler la intercepta, reporta el host final exacto y para (firma 1).
- **No escribe `data/manifiesto.yaml`** (firma 2); lo dice en su propio resumen.

**D-22 — corrió de punta a punta, por subproceso, contra `http.server` local**, con su propio `--root` y su propio manifiesto sintético. `python3 tests/test_descarga_manifiesto.py` → **26 PASS · 0 FAIL**:

1. archivo bueno → `DESCARGADO-AHORA`, payload en la raíz con el sha256 correcto; segunda corrida → `EXISTE-SATISFACE`, no re-descarga.
2. sha256 discordante → `SHA-DISCORDANTE`, el payload **no** entra a la raíz, el `.parcial` queda.
3. redirección a otro host → `REDIRECCION-A-OTRO-HOST` con el host final exacto en la salida, nada en la raíz.
4. `404` → `NO-OBTENIDO` con la fórmula de A.5 y la receta manual.
5. caso de regla, sin red: los **9** `banxico_sie_*` → `NO-ACCESIBLE`, con el conteo del universo en el propio test (A.13), y la premisa corregida cableada (`0 de 9` terminan en `.do`).
6. guardia E.6 sobre las 4 reservadas; 7. el piloto no bloqueado; 8. los tres casos de `raiz`; 9. no hay puerta por URL.

## 5 · Pieza 2 — no corrida

`NC-0423`, razón `PARO-ENTORNO`. El paso 2 del propio encargo es bajar el payload **con la pieza 1**, y el encargo excluye de «hecho» un verify sobre un payload traído a mano (§1). Sin red no hay payload y sin payload no hay verify. No se tocó `data/corrida0/CALC-ENIF-0001/*` ni la fila de replay existente (PARO (b)); no se parcheó nada del medidor congelado (PARO (d)/(g), que no llegó a evaluarse porque el medidor nunca corrió).

**CONTADOR.** El encargo declara «mueve la vista de replay (146 → 147 filas)». Medido al arrancar: `forense/replay-evidencia.tsv` ya tenía **147** líneas, no 146 — la premisa del contador estaba una fila atrás. La vista **queda en 147**: este acto no le añade ninguna fila, porque no produjo ningún veredicto de replay que asentar (E.7 funciona en los dos sentidos: no se asienta lo que no se corrió). `cuenta_gen2`: **no movido**, como el encargo veda.

## 6 · Pieza 3 — escrita con lo que salió

`FP-402`, por la firma 6 («FP-67 se ACOTA a `cloud_default`; no se sustituye hasta que el piloto mida»). **La fila de `FP-67` no se editó ni se borró**: sigue `CERRADA` en `forense/firmas-pendientes.tsv:68`, con su universo de agosto.

Lo que `FP-402` asienta, y lo que **no**:

- En **`cloud_default`**, medido hoy por dos vías, el egreso a INEGI **sigue bloqueado**. Para ese universo, `FP-67` queda **confirmada en su forma actual**, no vencida. Como el encargo anticipó: «Saber que la nube tampoco puede con red abierta es un hallazgo, no un fracaso» — con la precisión de que esta nube **no tenía** la red abierta, así que lo que se midió es la nube de siempre, no la nueva.
- Sobre **`milpa-inegi` con red `Custom`**, `FP-402` no mide nada y lo dice: el entorno no existía. La fila queda **ABIERTA** y ése es su contenido.

## 7 · Lo que este acto NO generaliza (verbatim, a petición de mesa)

> un `REPRODUCE` sobre un payload de 3.1 MB en un host no demuestra que 18.4 GB en 200 hosts funcionen. El piloto prueba que el carril existe, nada más.

Y en este acto ni siquiera eso: **el carril no se probó**, porque no hubo red. Lo que quedó probado es el **descargador**, contra un servidor local y sobre datos sintéticos. Que baje de INEGI es exactamente lo que falta medir.

## 8 · Archivos de soporte pedidos por mesa a media sesión — no alcanzados

Mesa señaló, ya en curso el acto, cinco artefactos en `C:\Users\PC0\Descargas MX` (`censo_nube_v1.py`, `censo-hueco-url-v1_0.tsv`, `censo-licencias-v1_0.tsv`, `CENSO-NUBE-MEDICION-2026-09-20.md`, `TRANSFER-NUBE-MEDICION-2026-09-20.md`).

**`NO-ACCESIBLE`**, y por dos razones que no se colapsan: (a) esa carpeta es el respaldo físico de la raíz lógica `descargas_mx`, que **este entorno no configura** (`data/raices.local.yaml` ausente) — es `RAÍZ-NO-CONFIGURADA`, no `AUSENTE`; (b) es una ruta de la máquina de mesa, fuera del contenedor de esta sesión de nube, que no monta el corpus compartido (`senal-corpus: montado=NO archivos_examinados=0`).

Ninguno de los cinco está en el repo: `NO-ENCONTRADO`, universo los **6 298** archivos del clon en `b8438d7`, búsqueda por nombre sin distinguir mayúsculas sobre los cinco patrones. Ninguno estaba en el perímetro de §9 del encargo y ninguno era insumo de las tres piezas, así que su ausencia no cambió nada de lo entregado. Si son insumo de un acto de censo de licencias, ese acto es **otro** (firma 7: escribir `licencia` en el manifiesto se decide cuando se arme la salida pública) y necesita que lleguen al repo o a una raíz que la sesión resuelva.

## 9 · Preguntas a mesa (no son PARO; el resto del acto siguió)

1. **`milpa-inegi`.** ¿Se crea y se relanza este mismo encargo tal cual —la pieza 1 ya está congelada y probada, así que el relanzamiento es sólo piezas 2 y 3—, o mesa prefiere que el sucesor `NUBE-PILOTO-2` absorba el piloto de 1 payload junto con los 37 de demanda D1? **Recomendación: relanzar NUBE-PILOTO-1 tal cual.** Un piloto de un payload que falle es diagnosticable en minutos; uno de 37 no, y el encargo separó las dos cosas a propósito.
2. **Los cinco artefactos de §8.** ¿Se suben al repo (o a una raíz que la sesión resuelva) como insumo de un acto propio, o se descartan? **Recomendación: acto propio**, porque `censo-licencias-v1_0.tsv` es justo lo que la firma 2 mandó a «un TSV derivado aparte», y meterlo aquí sería escribir fuera del perímetro de §9.
