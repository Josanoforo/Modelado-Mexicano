# ENCARGO · ACTO GEN2-TUBERIA-CANAL-REPARACION-1 · El canal de publicación empuja `[deriva]` con la deploy key exenta en la regla, en vez del token del bot; `verify.yml` gana el evento `merge_group`; se prueba con un push real y `origin/main` muestra por fin el 87 y los sellados sin fila

> ENTORNO: **NUBE**. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `ae19a710` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-tuberia-canal-reparacion-1` (D-17) · MODELO: Sonnet · MODO: ABIERTO · ids con raíz de acto (D-24) · perímetro de cierre permanente (D-21) aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero mediciones; no adopta; `adoptados_activos`, `celdas_validadas` y las filas de la vista se mueven **solo** porque el canal por fin corre (`registro --escribe --lote`), nunca a mano; se reporta antes/después.

## 1 · OBJETIVO
Que los dos pasos de `verify.yml` que hacen `git push origin HEAD:main` (l.430 y l.492 al redactar; autorización por `GITHUB_TOKEN` en l.364-369) firmen con la deploy key `canal-deriva` (secreto `CANAL_DERIVA_SSH_KEY`), exenta en el ruleset «main protegida»; que el workflow también dispare en `merge_group` (requisito para activar la cola de fusión, D4); y que el primer push real a `main` tras este cambio publique la vista completa. Habilita: `adoptados_activos` 72 → 87 (FIRMAS-10 lo midió), los 27+ sellados sin fila, `celdas_validadas` por encima de 92 (piloto 4 ya fusionado), y AUTOMERGE-2.
«Hecho» sobre el commit final con origin/main fusionado: un run de Actions posterior al merge, citado por id, donde el paso «Re-deriva por comando y commitea [deriva]» pasa y «Canal de publicación» no está `skipped` · `git log --author=canal-deriva\|github-actions origin/main -1` muestra un commit `[deriva]` posterior al merge · `python3 tools/corrida0.py status` en clon fresco: `adoptados_activos` = 87 (o el valor que el derivador dé, citado) y 0 selladas sin fila por el lector CSV · `grep -c merge_group .github/workflows/verify.yml` ≥ 1 · nunca `--force`, `--excluye` ni vistas a mano.

## 2 · FIRMAS DE MESA
D4-A (23/sep, verbatim «A, desde ya»; asentada por GEN2-TRAMITE-FIRMAS-11): main exige check VERDE, merge queue, el token fusiona solo rutinas. Mesa ejecutó el MANUAL-canal-deploy-key (adjunto) antes de lanzar este encargo: **si no lo ejecutó, §7 f.**

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` NC `NC-260923-GEN2-TRAMITE-FIRMAS-11-05da-01`: el paso `[deriva]` falla `git push origin HEAD:main` con GH013 («Required status check "check" is expected») en los runs `35810893285` (#1028) y `35816949850` (#1039); el paso del canal queda `skipped`. Causa: ruleset «main protegida», bypass solo `Repository admin · pull requests only`.
- `[EJECUTADO]` (captura de mesa 23/sep) la lista de bypass del ruleset ofrece Deploy keys, roles, y apps instaladas (Claude, Copilot); **no** ofrece GitHub Actions. De ahí la deploy key.
- `[LEÍDO]` `verify.yml:350-369`: el push se autoriza con `http.https://github.com/.extraheader` + `GITHUB_TOKEN` (sin `actions/checkout`, D-23). Los dos push en l.430 y l.492. El `if` del canal excluye commits `[deriva]` (sin bucle).
- `[REPORTADO]` por mesa: deploy key `canal-deriva` con escritura y secreto `CANAL_DERIVA_SSH_KEY` creados; bypass `Deploy keys · Always allow`. **Verifícalo tú antes de tocar el yml**: `gh api repos/Josanoforo/Modelado-Mexicano/keys` (o la API pública con conteo) muestra una llave `canal-deriva` con `read_only: false`; el secreto no se puede leer, se verifica por el run de prueba (P3). Si la llave no existe: §7 f.
- `[SUPUESTO]` que un push con deploy key dispara `on: push` del workflow (documentado por GitHub: solo los push con `GITHUB_TOKEN` no disparan). Si no dispara, el canal igual corrió en el job que empujó; se declara y no es PARO.
- ADJUNTOS: `MANUAL-canal-deploy-key-2026-09-23.md` (sha256 al lado; se archiva verbatim en `forense/encargos/fuentes/`).

## 4 · YA HECHO / YA DECIDIDO
`grep -c 'CANAL_DERIVA\|ssh-agent\|merge_group' .github/workflows/verify.yml` → 0 al redactar. AUTOMERGE-2 (rama abierta) PARÓ en P1 por falta de credencial y no toca estos pasos. FIRMAS-11 P4 diagnosticó y no reparó (excedía 10 líneas). **Repítelo.**

## 5 · PIEZAS
- **P1 · Push por SSH con la deploy key.** En el job que empuja: cargar la privada desde `secrets.CANAL_DERIVA_SSH_KEY` en un agente (`webfactory/ssh-agent` fijado por sha, o `ssh-agent`+`ssh-add` manual con `known_hosts` de github.com), cambiar el remoto de push a `git@github.com:Josanoforo/Modelado-Mexicano.git` **solo para el push** (fetch sigue por https), y quitar el `extraheader` del token en ese paso. Los dos push (l.430, l.492) usan el mismo mecanismo. Identidad del commit: `canal-deriva <canal-deriva@users.noreply.github.com>`. Sin cambiar nada del contenido que se deriva ni de `registro`.
- **P2 · `merge_group`.** `on:` gana `merge_group:` con `types: [checks_requested]`; el job `check` corre igual en ese evento. No se activa la cola aquí (es casilla de mesa); se deja lista y se dice en la nota que el segundo viaje a Rulesets es «Require merge queue».
- **P3 · Prueba real.** Merge de este PR por mesa → el push a `main` dispara el run; se cita el id y se pegan las líneas de salida de los dos pasos. Si el push `[deriva]` es rechazado: pegar el error crudo; si es GH013 otra vez, la fila Deploy keys quedó en «pull requests only» → NC con receta de un minuto para mesa, no se toca el yml. Antes/después de `status` en la nota.
- **P4 · Cierre de deuda.** Con P3 verde: cerrar `…FIRMAS-11-05da-01` y las once NC del canal que FIRMAS-11 dejó ABIERTAS por premisa (`c09b-01`, `c2b4-02`, `7d98-01`, `7d98-04`, `0af9-01`, `009f-01`, `ef6f-01`, `9428-01`, `aa3f-01`, `ff56-01`, `ff56-03`, `7492-01` — verifica cada id y estado, A.17) con `SUSTITUIDO-POR: GEN2-TUBERIA-LOTE-ESTRICTO-1 + este acto`. Sin P3 verde no se cierra ninguna.

## 6 · LATITUD
Implementación del agente SSH libre. Obstáculos reversibles: `gh`, `known_hosts`. Pregunta a mesa (sigues con P2): solo si la llave no tiene escritura o el secreto no existe (receta de un minuto). NO DECIDES: activar la cola.

## 7 · PAROS — lista cerrada
a) no aplica · b) `--force`, `--excluye`, escribir una vista a mano, tocar `registro` en `corrida0.py`, o cambiar el `if` que excluye `[deriva]` · c) mover contadores a mano · d) no aplica · e) CAJA · f) la deploy key `canal-deriva` no existe o no tiene escritura al abrir → PARO, y decirlo con el comando es el entregable.

## 8 · COMPUERTAS
«El push firma con la deploy key y el contenido lo produce el derivador» protege: **adoptar** (E.2: la vista publica lo que mesa ya fusionó; no se cuela nada). «Sin `--force` ni vistas a mano» protege: **borrar/reescribir**. «P4 solo con P3 verde» protege: **borrar** (deuda).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `.github/workflows/verify.yml` (bloques de autorización/push l.350-369, los dos push, `on:`), `forense/encargos/fuentes/MANUAL-canal-deploy-key-2026-09-23.md`, `no-corrido.tsv` (edición de estado de las filas citadas + append), `hallazgos.md`, nota, L0, cascada. Ajeno: `tools/corrida0.py`, vistas, CALC, AUTOMERGE-2 (su yml es otro archivo; si tocó `verify.yml`, rebasar). En vuelo: AUTOMERGE-2 (rama abierta), ASTRA-ENVIPE-ADJUDICACION-1, MOTOR-DEUDA-LOTE-1, `codex/astra3-*` (no tocan CI).

## 10 · LO QUE NO HACE · SUCESORES
No activa la cola, no fusiona nada solo, no cambia qué publica el canal. Sucesores: mesa activa «Require merge queue»; `GEN2-TUBERIA-RUTINAS-AUTOMERGE-2` se relanza (P1 y P3 pendientes) o -3 si hace falta.

## NO-CORRIDO / RESERVAS

- **qué:** P1 · Push por SSH con la deploy key `canal-deriva`.
  **por qué:** `SUSTITUIDO-POR:fc14cd8` — commit directo a `main` («Publica vistas de corrida mediante PR verificado», 23/sep/2026, `jonieqsa@gmail.com`), fusionado a `main` **después** de redactarse este encargo (SHA de redacción `ae19a710`) pero **antes** de que esta sesión llegara a tocar `verify.yml`. Ese commit reemplazó los dos `git push origin HEAD:main` del job `guardias` por un mecanismo distinto: el job abre un PR automático (`derivados/auto-<run_id>`) contra `main` con el `GITHUB_TOKEN` normal, y nunca empuja a `main` directo — la regla protegida deja de rechazarlo por `GH013` porque ya no hay push directo que rechazar, no porque una llave lo exente. Verificado al arrancar la sesión de cierre: `grep -n "push origin HEAD:main" .github/workflows/verify.yml` → 0 resultados (solo queda `git push origin "HEAD:refs/heads/$BRANCH"`, a una rama nueva). Implementar P1 tal como el encargo lo pedía habría reintroducido el push directo a `main` que ese mismo commit quitó el mismo día.
  **impacto:** ninguno sobre el objetivo del encargo (evitar que el canal muera con `GH013`) — ya está resuelto por otra vía. La deploy key `canal-deriva` / secreto `CANAL_DERIVA_SSH_KEY` del `MANUAL-canal-deploy-key-2026-09-23.md` (adjunto, archivado en `forense/encargos/fuentes/`) queda sin uso para este objetivo; mesa indicó en el chat de dirección (23/sep) que no lo ejecutaría ahora («No se ejecutará ahorita ... se resuelve a final de esta semana, domingo»), y con P1 superado ya no es necesario ejecutarlo para este acto.
  **sucesor:** N/A — resuelto por `fc14cd8`, no por este acto ni por un sucesor.

- **qué:** P3 · Prueba real del push firmado con la deploy key.
  **por qué:** `SUSTITUIDO-POR:fc14cd8` — no hay push por SSH que probar (P1 no corrió, ver arriba). La prueba real del mecanismo VIGENTE (PR automático) ya existe de forma independiente: hay dos PR abiertos por ese mecanismo, `#1057` y `#1059` («`[deriva] vistas generadas tras ...`»), pendientes de que mesa los fusione.
  **impacto:** `N_resultados_gen2_adoptados_activos` sigue en 72 (medido con `python3 tools/corrida0.py status` en esta sesión, commit `84a3aa8`), no en 87, hasta que mesa fusione `#1057`/`#1059` — no por falla del canal, sino porque nadie los ha fusionado todavía. `celdas_validadas` en 92 (Δ0 sobre lo medido al abrir).
  **sucesor:** mesa (fusionar `#1057` y `#1059` cuando lo decida — no es de este acto tocarlos, están fuera de su perímetro §9).

- **qué:** P4 · Cierre de deuda (`…FIRMAS-11-05da-01` y las once NC del canal).
  **por qué:** `DECISIÓN-DE-MESA-PENDIENTE` — el encargo condicionaba el cierre a «P3 verde», y P3 (en su forma original, prueba del push por SSH) no aplica; la forma vigente de «verde» —`#1057`/`#1059` fusionados y publicando la vista— tampoco ocurrió en esta sesión (mesa no los fusionó). Cerrar estas NC sin esa verificación sería exactamente el riesgo que el propio encargo nombró en §7-f para el mecanismo viejo: adoptar sobre una premisa no confirmada.
  **impacto:** las 27+ corridas selladas sin fila y `adoptados_activos` (72→87 medido por FIRMAS-10) siguen sin publicarse en la vista; las once NC (`c09b-01`, `c2b4-02`, `7d98-01`, `7d98-04`, `0af9-01`, `009f-01`, `ef6f-01`, `9428-01`, `aa3f-01`, `ff56-01`, `ff56-03`, `7492-01`) siguen `ABIERTA`.
  **sucesor:** quien cierre `#1057`/`#1059` (mesa) — o un acto de tramite/cierre posterior que verifique la vista ya publicada y entonces cierre estas NC por objeto (A.17).

- **qué:** el resto del encargo (P2 — `merge_group`).
  **por qué:** ejecutado — no aplica.
  **impacto:** ninguno.
  **sucesor:** N/A.

## CONSUMIDO

Ejecutado por `/acto` sobre `forense/encargos/2026-09-23-GEN2-TUBERIA-CANAL-REPARACION-1.md`, rama `acto/gen2-tuberia-canal-reparacion-1`, PR [#1062](https://github.com/Josanoforo/Modelado-Mexicano/pull/1062). ADR raíz: `ADR-260923-GEN2-TUBERIA-CANAL-REPARACION-1-95ec-01`. Suite `--rapido` VERDE (0 FAIL) en cada commit de esta rama. No se fusiona en este acto: mesa fusiona.
