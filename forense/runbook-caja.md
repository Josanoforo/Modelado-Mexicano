# Runbook de caja (UBUNTU/WSL) — `corrida0`

Notas operativas para quien corre `tools/corrida0.py` (`preflight`/`run`/`verify`)
dentro de la caja. No hay receta general de la caja todavía — este archivo nace
con la única línea que `ACTO GEN2-CHECADOR-2 · TRES-DEFECTOS-CORRIDA0`
(`forense/encargos/2026-09-09-GEN2-CHECADOR-2-tres-defectos-corrida0.md`) debía
documentar (`FP-352`); se amplía cuando aparezca la siguiente pieza real.

- **`/mnt/c` y el sandbox de Bash de Claude Code.** El sandbox por defecto no
  expone `/mnt/c` (ni la red real) — medido por `ACTO GEN2-E5 · CALC-0001..0003`
  (`forense/notas/2026-09-08-codebooks-abiertos-y-specs-congeladas.md §6`):
  `corrida0 preflight` sobre un payload cuya raíz lógica sea `descargas_mx` sale
  `NO-VISIBLE-EN-ESTE-CONTEXTO` (aviso, no bloqueo, desde `FP-352`) dentro del
  sandbox por defecto, y `COINCIDE` fuera de él. El rodeo ya en uso, declarado
  por `GEN2-E5` y por `GEN2-SONDA-CAJA-1`
  (`forense/notas/2026-09-08-GEN2-SONDA-CAJA-1.md`): correr con
  `dangerouslyDisableSandbox: true` (parámetro del tool `Bash`) cuando el CALC
  o la sonda toquen una raíz externa al repo (`descargas_mx`), o correr el
  comando fuera de Claude Code por completo. No es un hallazgo de `/sonda` ni
  un defecto de la raíz — es una propiedad del sandbox de esta caja.
