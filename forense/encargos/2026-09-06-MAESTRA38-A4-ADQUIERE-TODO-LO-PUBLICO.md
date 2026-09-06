# A.3 · Encargo verbatim · `ACTO MAESTRA38-A4 · ADQUIERE-TODO-LO-PUBLICO`

Archivado por el propio acto, 6/sep/2026, worktree `/home/pc0/Modelado-Mexicano/.claude/worktrees/agent-a4f8a030e1f577254`, rama `acto/maestra38-a4-adquiere-todo-lo-publico`, tracking `origin/main` en `a5350e59`.

## Encargo original (verbatim, tal como se pegó al invocar el acto)

```
ENCARGO · ACTO MAESTRA38-A4 · ADQUIERE-TODO-LO-PUBLICO — invoca /acto
SHA a5350e59 · sin compuerta · UBUNTU con corpus y red · Opus · worktree propio, data/raw y raices.local.yaml enlazados, guard de rama · primero en la cola (antes de L2, C1, lotes y A3).
FIRMA — verbatim (6/sep): «Lo que pueda bajar caja que lo baje caja, lo que no, dame las ligas y el detalle de qué tengo que bajar».
A.8 contra a5350e59: universo = toda fila de la cola con estado_A4A5 en PENDIENTE / PENDIENTE-DE-MESA / OBTENIDO-PARCIAL / NO-OBTENIDO-POR-ESTE-AGENTE(*) que tenga url_conocida o receta en nota (derívalo por comando; hoy son ~31), más enfih2019_bd_csv_zip (registrado, físicamente ausente, url_origen directa de INEGI) y el paquete ICPSR (registrado, contenido sin inspeccionar).
SPEC — dos commits. COMMIT-1: lista congelada de objetivos con su URL, la pregunta que responden (regla/necesidad) y el criterio de éxito por objeto (nombre esperado, tipo, tamaño aproximado si se sabe); frase de sello. Incluye el unzip -l del paquete ICPSR como primer objeto. COMMIT-2: por objetivo, en este orden: (a) /adquiere con ≥4 rutas y sonda de alcanzabilidad antes de contenido (v2.2, tres hallazgos distintos); (b) lo obtenido: A.7 doble descarga y hash de contenido, testzip, registro por las tres capas, fila OBTENIDO, depósito en la subcarpeta de la fuente; ENFIH se compara contra el sha del manifiesto (COINCIDE → C3 real a 0; hash-discordante → INEGI republicó: entrada nueva, nota sustituye_a); (c) lo no obtenido: NO-OBTENIDO-POR-ESTE-AGENTE EN N INTENTOS con la salida cruda y la razón exacta — EXIGE-CUENTA / EXIGE-SESION-NAVEGADOR (SPA) / EXIGE-SOLICITUD-ESCRITA / HOST-NO-RESPONDE — y receta de un minuto: URL exacta, qué botón, qué nombre va a tener el archivo y dónde depositarlo. (d) ICPSR: si el .dta está en el paquete → extraer, registrar, hallazgo que corrige «sigue sin obtenerse»; si no → leer la página de términos y escribir cuál de las tres razones aplica, sin suponer.
Cierre: PAQUETE-RECETAS-10 = sólo lo que caja no pudo, con receta; es la lista que mesa recibe. Anti-PR#77. FP: recibo + «mesa ejecuta las recetas de PAQUETE-10» (vence 7 días).
PERÍMETRO: manifiesto (+N) · staging (transitorio) · cola + vista · relaciones/procedencias/utilidad + baseline (sólo por alta_relacion.py para fuente nueva) · INFRAESTRUCTURA · forense/notas/…A4-{spec,resultados}.md, …PAQUETE-RECETAS-10.md · hallazgos · tablero · A.3 · cascada. NO toca milpa/**, canon (salvo ADR), specs, Downloads.
ADR-347 · FP-312/313.
CONTADOR: objetivos obtenidos por caja 0 → k de ~33 · recetas para mesa ~33 → declara · medición: cero (adquisición).
```

## ARRANQUE (A.2/A.13), reportado antes de ejecutar

- **0 · GUARD DE RAMA**: `git ls-remote --heads origin | grep -i "maestra38-a4\|A4-ADQUIERE"` → sin coincidencia (exit 1). Rama creada: `acto/maestra38-a4-adquiere-todo-lo-publico`.
- **1 · REPO**: clon existente `/home/pc0/Modelado-Mexicano`, worktree de esta sesión `/home/pc0/Modelado-Mexicano/.claude/worktrees/agent-a4f8a030e1f577254`. No se clonó nada nuevo.
- **2 · SHA**: el worktree nació en `2f0ee33`; `origin/main` real está en `a5350e5` — exactamente el SHA que el encargo declara. Fast-forward `2f0ee33..a5350e5` aplicado antes de tocar nada.
- **3 · `data/raw`**: ausente al nacer el worktree (no es PARO). **Enlazada** a `/home/pc0/mm-corpus/raw` (`ln -sfn`), 376 entradas visibles. `data/raices.local.yaml` copiado desde el clon padre (`descargas_mx: /mnt/c/Users/PC0/Descargas MX`, 169 entradas).
- **4 · ENTORNO**: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable`. Sonda de red `curl -s -o /dev/null -w "%{http_code}" --max-time 25 https://www.inegi.org.mx/` → **`000` dentro del sandbox de bash**, **`200` fuera del sandbox**. Corpus montado: `ls data/raw/ | head -1` → `2005trim1_csv.zip`; el comando examinó **376** entradas. Consecuencia operativa declarada: toda descarga de este acto corre fuera del sandbox de bash.
- **5 · ESPEJO**: ninguna cifra de este acto sale del espejo del proyecto; todas salen de este clon, con el comando a la vista en `forense/notas/2026-09-06-MAESTRA38-A4-spec.md` y `…-resultados.md`.

## COMPUERTA

El encargo declara **`sin compuerta`**. Equivale a `COMPUERTA: ninguna` (§2 de `/acto`): declaración explícita de que no hay compuerta, no dispara verificación. Se pasa directo al paso 3 (0-bis A.3), que es este archivo.

## Adenda recibida durante la ejecución

`forense/encargos/2026-09-06-ADENDA-A4-rutas-PDN.md` (dirección, 6/sep), archivada verbatim en append (A.3) **después** del `COMMIT-1` y **sin editarlo**: añade rutas `R0`–`R7` al objetivo #27, no añade objetivos ni cambia criterios de éxito. Verificada su aplicabilidad con el comando que ella misma pide y **aplicada**.

## CONSUMIDO

**0-bis A.3** (commit `a79d1c9`): este archivo. ARRANQUE reportado (guard de rama sin coincidencia; fast-forward `2f0ee33`→`a5350e5`, exactamente el SHA que el encargo declara; `data/raw` enlazada a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiado del clon padre; sonda de red `000` dentro del sandbox / `200` fuera). COMPUERTA: `sin compuerta`, equivale a `COMPUERTA: ninguna` — no dispara verificación. `git push -u` inmediato, per el paso 0 del ARRANQUE.

**COMMIT-1** (commit `ae8735e`): `forense/notas/2026-09-06-MAESTRA38-A4-spec.md` — lista congelada de **33 objetivos** con URL, pregunta de modelo y criterio de éxito por objeto; frase de sello; `unzip -l` del paquete ICPSR como primer objeto (10 entradas, **cero archivos de datos**, `testzip None`); sonda de alcanzabilidad de los 33 corrida **antes** de pedir contenido (19 con bytes reales confirmados, 14 con obstáculo visible); protocolo de agotamiento v2.2 (≥ 4 rutas **distintas**) congelado ahí mismo. **Dos desviaciones de premisa declaradas antes de ejecutar**: el universo es de **25** filas, no ~31 (comando a la vista); y `ENFIH 2019` **no** está físicamente ausente — su `sha256` COINCIDE con `manifiesto.yaml:4115`, así que la rama «INEGI republicó» del encargo no se ejecuta.

**A.3 append** (commit `22eba8d`): `forense/encargos/2026-09-06-ADENDA-A4-rutas-PDN.md`, verbatim.

**COMMIT-2** (commit `60bc3f4` + cierre): **25 de 33 objetivos obtenidos**, **201 payloads, 5.39 GB** en el corpus compartido, todos con A.7 (doble descarga por `curl` **y** `wget`, `sha256` de contenido idéntico como condición de depósito) y `testzip None` donde aplica. Manifiesto `1315` → `1515` (ciclo `--escanea`/`--promueve` por fuente, 18 fuentes, staging a vacío, `--verifica` sobre `data_raw` `coincide=1195 · no_coincide=0 · ausente=0`). Cola: 18 filas tocadas por línea opaca, 114 intactas byte a byte, `OBTENIDO` `92` → `104`, vista regenerada. `ADENDA aplicada` (`R0`–`R7`): los cuatro bulk oficiales de la PDN bajados vía el bundle React, con `CONTROL-COINCIDE` contra `pdn_s3v2`. Detalle en `forense/notas/2026-09-06-MAESTRA38-A4-resultados.md`.

**Cierre**: `forense/notas/2026-09-06-MAESTRA38-A4-PAQUETE-RECETAS-10.md` — **5 objetos**, no 33: lo único que caja no pudo bajar, cada uno con razón exacta medida (`EXIGE-CUENTA` ×2 · `EXIGE-SESION-NAVEGADOR` · `EXIGE-SOLICITUD-ESCRITA` · `HOST-NO-RESPONDE`) y receta de un minuto donde la hay. Anti-PR#77 verificado: los 201 payloads están en `/home/pc0/mm-corpus/raw`, no sólo en este worktree.

**Cascada**: `ADR-347` (`canon/gobernanza-v1_15.md` §4, candidato derivado contra `346`, contiguo; cabecera `346` → `347 ADR`), `L0` recifrado con la anotación nueva **insertada antes de la anterior** (`canon/estado-programa-v1_12.md`, más su cabecera de conteo), `canon/registro-rotulos.tsv` censa `MAESTRA38-A4`, `forense/firmas-pendientes.tsv` `FP-312` (recibo) y `FP-313` (firma de mesa sobre las recetas, vence 13/sep/2026), `forense/hallazgos.md` +6 entradas, `forense/tablero/TABLERO-PROGRAMA-v1_1.md` §8.13, `data/INFRAESTRUCTURA-v1_0.md` +4 líneas.

**Contador contra lo que el encargo declaró.** «objetivos obtenidos por caja `0` → `k` de ~33»: **k = 25**. «recetas para mesa ~33 → declara»: **5** — se declara la diferencia, y su causa es que caja bajó casi todo. «medición: cero (adquisición)»: cumplido, ningún payload se abrió para medir.

`python3 tests/check.py --baseline`: **LÍNEA BASE VERDE** (3 FAIL / 170 WARN, sin cambio frente a `tests/baseline.json`).

PR de este acto, contra `main`. **No se fusiona**: el merge es de mesa.
