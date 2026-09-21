# MOTRAL — insumo externo (GEN2-LIMPIEZA-RAMAS-LOCALES-4, F-D)

Archivado antes de retirar (`git worktree remove --force`, único caso autorizado) el worktree
`/home/pc0/mm-gen2-motral2015-prioridades-prestaciones-cli-1` (rama
`codex/gen2-motral2015-prioridades-prestaciones-cli-1`), que quedó parado en medio de un
**cherry-pick en conflicto** (no un rebase abortado, como decía el input de mesa — verificado
contra el `git status` real: `You are currently cherry-picking commit 7a648587`, conflicto
`both added` en `medidor.py`).

Dictamen ya cerrado en `forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-3-cierre.md`
(sección P2): `CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001` es **NO-EJECUTABLE** — el sello del
19/sep nunca produjo, ni al sellarse, los ~42 `RESULT-…` que su propio `spec.yaml` contrata (solo
3 keys de diagnóstico de ranking). No es *drift* de entorno: nació incompleto. **No se rescata.**
`NC-0420` (`forense/no-corrido.tsv`) ya cierra con esta razón.

## Archivos

- `motral2015-prioridades-2026-09-20-spec.yaml` — spec sellada, copiada tal cual del worktree.
- `motral2015-prioridades-2026-09-20-medidor-CONFLICTO.py` — **contiene marcadores de conflicto
  de git sin resolver** (`<<<<<<< HEAD` / `=======` / `>>>>>>> 7a64858`). Se archiva tal cual
  estaba en el worktree en el momento de retirarlo — no se resolvió el conflicto, no se limpió.
  Cualquier reintento de rescate futuro debe resolver este conflicto desde cero.
- `motral2015-prioridades-2026-09-20-git-status-cherry-pick-conflicto.txt` — `git status` completo
  del worktree en el momento del archivado.
- `motral2015-prioridades-2026-09-20-git-diff-cherry-pick-conflicto.txt` — `git diff` completo
  (1 archivo, conflicto de `medidor.py`).
- `motral2015-prioridades-2026-09-20-verify-output.txt` — salida cruda de
  `python3 tools/corrida0.py verify CALC-MOTRAL2015-PRIORIDADES-PRESTACIONES-0001`, re-corrida hoy
  en un worktree efímero desde `origin/main` (que no tiene colisión de id, confirmado en #923),
  trayendo el directorio sellado desde el commit `914e92f3` de la propia rama codex (no desde el
  worktree en conflicto). Reproduce el mismo hallazgo que #923 ya citó de memoria: 41
  `outputs_faltantes` (los `P17`/`P16-FIRST`) y 3 `outputs_no_declarados`
  (`RESULT-MOTRAL15-RANKING-{COMPLETOS,JSON,N-ELEGIBLES}`). El dato real
  (`motral2015_bases_datos_dbf.zip`) vive en `/mnt/c/...` y solo es alcanzable con el sandbox
  desactivado para ese comando puntual.

Después de este archivado: worktree retirado con `--force`, rama
`codex/gen2-motral2015-prioridades-prestaciones-cli-1` borrada.
