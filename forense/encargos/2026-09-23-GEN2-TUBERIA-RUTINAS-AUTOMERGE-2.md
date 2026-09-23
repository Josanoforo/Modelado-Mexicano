# ENCARGO · ACTO GEN2-TUBERIA-RUTINAS-AUTOMERGE-2 · Enciende el auto-merge de rutinas con la política que mesa firmó (D4-A): main protegida por check VERDE, cola de fusión, y el token fusiona solo PR de rutina

> ENTORNO: **NUBE**. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `f28d1038` (re-deriva al abrir; main movido no es PARO) · una sola sesión, rama propia `acto/gen2-tuberia-rutinas-automerge-2` (D-17) · MODELO: Sonnet · MODO: ABIERTO · ids con raíz de acto (D-24) · perímetro de cierre permanente (D-21) aplica sin enumerarlo · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero mediciones; no adopta; ningún PR que selle corridas se fusiona por este mecanismo, hoy ni nunca.

## 1 · OBJETIVO
Que un PR de rutina (rama `claude/encola-*`, `acto/gen2-tramite-*`, o commit `[deriva]`) se fusione solo cuando `check.py --baseline` está VERDE, pasando por la cola de fusión de GitHub, sin botón de mesa; y que cualquier otro PR siga exigiendo fusión humana. Habilita: que mesa deje de ser el cuello de botella de los trámites (D4).
«Hecho»: un PR de prueba de rama `acto/gen2-tramite-automerge-prueba` con un cambio trivial en `hallazgos.md` se fusiona solo con CI VERDE (cita el run y el merge commit) · un PR de prueba de rama `acto/gen2-prueba-no-rutina` NO se fusiona solo y la nota lo demuestra · la configuración de protección de `main` queda documentada por comando (`gh api repos/:owner/:repo/branches/main/protection` o captura de la API con conteo) · `.github/workflows/` contiene la rutina con la lista cerrada de prefijos verbatim de D4.

## 2 · FIRMAS DE MESA (23/sep/2026, verbatim del chat de dirección; entran al repo por GEN2-TRAMITE-FIRMAS-11 — este encargo las cita, no las asienta)
- **D1** «Integrar los dos, nada es fuera de plazo, todo se utiliza.» (#1030 y #1031 se fusionan; las cuatro emisiones ENVIPE de Astra se adjudican contra la R del piloto 4.)
- **D3** «Que cuenten.» (las adjudicaciones de crédito entran a celdas_validadas vía celda-D)
- **D4** «A, desde ya.» (main exige check.py VERDE; merge queue; el token de Actions fusiona solo PR de rutina: `claude/encola-*`, `acto/gen2-tramite-*`, `[deriva]`; lo que mide lo fusiona mesa)
- **D5** «Ya tengo un disco duro, necesito reformatearlo para dejarlo listo, no ahora, esta semana sí; vence el domingo de esta semana.» (27/sep/2026)
- **D6** «A.» (la vía (i) de relevo lee el eje RESULTADO; CONTEXTO en la nota del pin)
- **D7** «A.» (acto de MOTOR autorizado a editar `milpa/src/motor.py` en las líneas de NC …e8fa-01; los sellos afectados se suceden por CALC nuevos)
- **D8** «A, pero que se explique claramente qué significa.» (INDETERMINADO es valor válido; se define por escrito)
- **D2** no es firma: es una pregunta de mesa («¿por qué seguimos haciendo piloto del piloto?») que contesta el encargo DUELO-ENCIG2025-CIERRE-1 con su firma §2 propuesta.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` `forense/encargos/2026-09-22-GEN2-TUBERIA-RUTINAS-AUTOMERGE-1.md` (#1022): PARO por firma ausente; l.19 cita NC `…CIERRE-SIN-CHOQUE-2-8e53-04` (protección de rama, ABIERTA). Lo que ese acto dejó instalado (workflow, clases de rutina) se reutiliza; no se reescribe. Firmas previas sobre el objeto: e889-01 (auto-merge sí), 9a2c-01 (auto-merge no, sustituida por e889-01 — cita ambas, A.10). D4-A las completa con las tres líneas.
- `[SUPUESTO]` que el token de Actions del repo tiene permiso para fusionar y que mesa tiene admin para la protección de rama. Si el token no puede fusionar, la salida es (ii) de §5 P1: receta de un minuto para mesa, no PARO.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`ls .github/workflows/ | grep -i automerge` → reporta qué dejó #1022. `gh api …/branches/main/protection` → reporta el estado actual (si 404, no hay protección).

## 5 · PIEZAS
- **P1 · Protección de main.** Requisito: status check `check.py --baseline` obligatorio; merge queue activada; sin push directo. Si el acto puede aplicarlo por API con la credencial de la sesión, lo aplica y pega la respuesta; si no, escribe la receta exacta (pantalla, casillas, valores) en la nota y abre FP para que mesa la ejecute en un minuto. **Nunca deshabilita una protección existente.**
- **P2 · Rutina de auto-merge.** Reglas verbatim de D4: fusiona solo si (rama empieza por `claude/encola-` o `acto/gen2-tramite-`, o el último commit empieza por `[deriva]`) y CI VERDE y el PR no toca `data/corrida0/CALC-*` ni `forense/prereg-caja/` (guardia por diff: si toca, no es rutina aunque el prefijo diga que sí). Registra cada fusión automática en `forense/fusiones-automaticas.tsv` (append; union en `.gitattributes`).
- **P3 · Las dos pruebas** de «Hecho». Se borran las ramas de prueba al cerrar (A.14).
- **P4 · Cierre de deuda.** NC `…8e53-04`, `…e889-01/02/03`, `…FIRMAS-8-aa3f-04`: CERRADA con `DECISIÓN-DADA: D4-A (FIRMAS-11)` y este acto como ejecutor.

## 6 · LATITUD
Implementación libre (GitHub auto-merge nativo con `gh pr merge --auto`, o workflow propio). Pregunta a mesa (sigues): si el token no puede fusionar ni con la receta, opciones: PAT de mesa con alcance mínimo · GitHub App · mantener botón. Recomendación: GitHub App.

## 7 · PAROS — lista cerrada
a) no aplica · b) deshabilitar una protección existente, reescribir `verify.yml` fuera del bloque de la rutina, fusionar algo que toque CALC/prereg · c) no aplica · d) no aplica · e) CAJA · f) ya está encendido y funcionando (demuéstralo con un merge automático previo).

## 8 · COMPUERTAS
«La guardia por diff excluye todo PR que toque `data/corrida0/CALC-*` o `forense/prereg-caja/`» protege: **adoptar** (E.2: la adopción es merge de mesa; una corrida fusionada por máquina sería adoptada sin mesa). «Sin deshabilitar protecciones» protege: **borrar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `.github/workflows/automerge-rutinas.yml` (o el nombre que dejó #1022), `forense/fusiones-automaticas.tsv` (nuevo), `.gitattributes` (una línea union), `firmas-pendientes.tsv`/`no-corrido.tsv` (append), nota, L0, cascada. Ajeno: `verify.yml` fuera del bloque de rutinas, `check.py`, `corrida0.py`. En vuelo: FIRMAS-11 (P4 toca `verify.yml` ≤ 10 líneas en el bloque del canal — otro bloque; si el diff choca, quien fusiona segundo rebasa sin renumerar nada), ASTRA-ENVIPE-ADJUDICACION-1, DIN-CREDITO-CELDAS-D-1.

## 10 · LO QUE NO HACE · SUCESORES
No fusiona nada que mida; no cambia CI. Sucesor: ninguno si las dos pruebas pasan; `GEN2-TUBERIA-RUTINAS-AUTOMERGE-3` si el token exige App.

## NO-CORRIDO / RESERVAS
- **qué**: P1 — protección de main (status check `suite` obligatorio) + merge queue, aplicadas por API con la credencial de la sesión. **por qué**: `PARO-PREMISA` — el `[SUPUESTO]` §3 de que la sesión podría aplicarlo resultó falso: no hay tool de branch-protection ni `gh` CLI, y la red directa a `api.github.com` está `DENEGADA-POR-POLITICA`. **impacto**: el workflow de auto-merge queda instalado pero inerte; ningún PR se fusiona solo todavía. **sucesor**: `FP-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-2-1269-01` (receta de un minuto en la nota de cierre §2).
- **qué**: P3 — las dos pruebas de «Hecho» (PR de rutina fusionado solo; PR no-rutina no fusionado). **por qué**: `PARO-PREMISA` — dependen de P1, no corrido. **impacto**: el criterio de «hecho» del encargo no queda demostrado en este acto. **sucesor**: `NC-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-2-1269-02`, re-correr tras P1.

## CONSUMIDO
PR #1048.
