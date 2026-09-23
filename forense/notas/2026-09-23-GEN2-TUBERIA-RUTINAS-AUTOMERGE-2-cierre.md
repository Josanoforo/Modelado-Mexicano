# Nota de cierre · ACTO GEN2-TUBERIA-RUTINAS-AUTOMERGE-2

ADR: `ADR-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-2-1269-01` (raíz de acto: `1269`, hex del 0-bis `e1269c7`).
Entorno: **NUBE** (`ENTORNO-DERIVADO=NUBE`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, red `DENEGADA-POR-POLITICA`, corpus no montado, 0 archivos examinados — A.13). Sonnet 5. MODO ABIERTO. Sin sub-agentes.

## 1 · Qué pedía el encargo, qué se construyó

D4-A (firma de mesa 23/sep/2026, §2 del encargo, verbatim: «A, desde ya» sobre «main exige check.py VERDE; merge queue; el token de Actions fusiona solo PR de rutina: `claude/encola-*`, `acto/gen2-tramite-*`, `[deriva]`; lo que mide lo fusiona mesa») pedía tres piezas:

- **P1 · Protección de main.** NO se pudo aplicar por API: esta sesión no tiene ningún tool de administración de branch protection (`gh api`, `gh` CLI, ni una llamada REST genérica) en su superficie de herramientas de GitHub, y la red saliente directa (curl a `api.github.com` fuera del servidor MCP) está `DENEGADA-POR-POLITICA`. Queda como receta para mesa (abajo) y como `FP-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-2-1269-01`.
- **P2 · Rutina de auto-merge.** Construida: `.github/workflows/automerge-rutinas.yml`. Se dispara en `workflow_run` al completar "Verificación del corpus" (el job `suite`, `check.py --baseline`). Ubica el PR por SHA vía la API de búsqueda (`search/issues?q=...+sha:<sha>`), verifica **las cuatro condiciones de D4** en este orden:
  1. rama `claude/encola-*` / `acto/gen2-tramite-*`, o último commit `[deriva]*` (lista cerrada, verbatim);
  2. el `workflow_run` que disparó el job ya es `conclusion == success` (condición del trigger, no se re-verifica con una segunda llamada);
  3. guardia por diff — ningún archivo del PR empieza por `data/corrida0/CALC-` ni `forense/prereg-caja/` (paginado hasta 1000 archivos);
  4. el PR sigue `open` y `mergeable != false` en el instante de fusionar.
  Si las cuatro se cumplen: `PUT .../pulls/{n}/merge` (squash) con el `GITHUB_TOKEN` del job, y registra la fila en `forense/fusiones-automaticas.tsv` (append vía API de contenidos, `.gitattributes` con `merge=union`). Sin actions de marketplace (mismo criterio que `verify.yml`): solo `curl`+`jq` contra la API de GitHub, con el `GITHUB_TOKEN` que Actions inyecta — ningún secreto nuevo.
  El workflow queda **instalado pero inerte** hasta que P1 esté aplicado: sin merge queue ni status check obligatorio, un PR puede fusionarse a mano en paralelo (o nunca disparar el `workflow_run` si `main` no exige el check), pero la rutina en sí misma no fusiona nada que no cumpla las cuatro condiciones — no hay forma de que dispare sobre un PR no-rutina.
  No se creó `forense/rutinas-clases-v1_0.tsv` aparte (que NC `…e889-01` esperaba): la tabla de clases quedó embebida en el propio workflow (los `case` de rama/commit) — latitud explícita del encargo («implementación libre»). Si un sucesor prefiere una tabla externa versionada aparte, es un refactor de forma, no de regla.
- **P3 · Las dos pruebas de «Hecho».** NO ejecutadas: dependen de P1 (sin protección de main + merge queue, no hay canal por el que la rutina se dispare de forma verificable contra las reglas de fusión reales — un merge por API sin protección activa demostraría solo que el token puede fusionar, no que el mecanismo respeta las cuatro condiciones bajo la política de `main` que el encargo pide demostrar). Queda `NC-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-2-1269-02`, sucesor: re-correr tras P1.

## 2 · Receta para mesa (P1, un minuto, `Settings → Branches → main`)

1. **Branch protection rule** sobre `main`:
   - ☑ Require a pull request before merging.
   - ☑ Require status checks to pass before merging → añadir el check **`suite`** (el job de `.github/workflows/verify.yml`, `Verificación del corpus`). Sin ese check, la rutina nunca ve un `workflow_run` con `conclusion=success` que citar, así que no fusiona nada — instalar el check no cambia el comportamiento actual (nadie fusiona sin verlo hoy tampoco), solo lo hace obligatorio a nivel de plataforma.
   - ☑ Require branches to be up to date before merging (opcional; recomendado si se activa merge queue, ver abajo).
   - ☐ NO marcar "Include administrators" si mesa quiere seguir pudiendo fusionar manualmente sin pasar por el check en una emergencia — a discreción de mesa, no lo decide este acto (no es de la lista cerrada de PAROS ni de compuertas de §8, es una preferencia operativa).
2. **Merge queue** (misma pantalla, sección "Merge queue"): ☑ Require merge queue. Método de fusión: squash (coherente con el `merge_method` que usa el workflow).
3. **Allow auto-merge** (Settings → General → Pull Requests): ☑ activar — es un requisito independiente de GitHub para que `PUT .../merge` funcione limpio con merge queue encendida; sin él, la API puede rechazar el merge con 405.
4. Nada de esto deshabilita una protección existente (§8 del encargo, compuerta **borrar**): hoy `main` no tiene ninguna regla (`404` esperado en `gh api .../branches/main/protection` — no verificado en esta sesión por la misma ausencia de tool, se infiere de que ningún PR previo la reportó configurada).

## 3 · Cierre de deuda (P4)

Cerradas con `DECISION-DADA: D4-A (este ADR)`, citando la línea exacta que las responde:
`NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04`, `NC-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-1-e889-01/02/03`, `NC-260923-GEN2-TRAMITE-FIRMAS-8-aa3f-02/04`, y `FP-260923-GEN2-TRAMITE-FIRMAS-9-97dc-01` (marcada `FIRMADA`, citando D4 verbatim).

`FP-260923-GEN2-TUBERIA-RUTINAS-AUTOMERGE-1-e889-01` ya estaba `FIRMADA` desde antes de este acto (no se toca).

## 4 · Módulo de auditoría — no carga

Este artefacto no afirma nada sobre México (§5 de las instrucciones): es aparato de CI/CD. No corren las preguntas de §5.

## 5 · CONTADOR

Cero mediciones; no adopta; ningún PR que selle corridas se fusiona por este mecanismo (la guardia por diff lo impide por diseño, hoy y en cualquier corrida futura de este workflow, salvo que alguien edite el propio `.github/workflows/automerge-rutinas.yml` — y eso mismo no es un PR de rutina bajo sus propias reglas, así que nunca podría auto-fusionarse a sí mismo).

## 6 · Suite

`python3 tests/check.py --rapido` → ver salida cruda en el commit de cascada.
