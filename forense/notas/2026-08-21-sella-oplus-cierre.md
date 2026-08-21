# Nota de cierre — `ACTO SELLA-OPLUS`, 21/ago/2026, nube

Encargo: `forense/encargos/2026-08-21-SELLA-OPLUS.md` (`CONSUMIDO`). ADR: `canon/gobernanza-v1_15.md` `ADR-141`.

## ARRANQUE

- **Gate.** `#3` (`ADR-140`, `ACTO SELLA-C`, `PR #307`) fusionado. `git log -1 --format="%h %s"` → `cffff43 Merge pull request #307 from Josanoforo/claude/adv1-m6-rewrite-amendments-bykxjf`. `git status` limpio, sobre `claude/operador-combinacion-mediana-y43ex2`.
- **Máximo verificado.** `grep -o "ADR-[0-9]*" canon/gobernanza-v1_15.md | sort -n | tail -1` → `140`, único, sin huecos → este acto candidatea `ADR-141`. `grep -oE "FP-[0-9]+" forense/firmas-pendientes.tsv | sort -t- -k2 -n -u | tail -1` → `FP-104`, sin filas nuevas necesarias: este acto cierra `FP-99`, ya abierta.
- **Fila `FP-99` verificada existente antes de tocarla** — `grep -n "^FP-99" forense/firmas-pendientes.tsv`, una sola coincidencia. No se crea fila nueva (precedente `FP-58`, citado por el propio encargo de `REPARA-T22` que abrió esta fila).
- **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`.

## T1 · `corredor-E-combinacion-LM.py`

Deja de ser propuesta sin sellar. Implementa `combinar_continua`/`combinar_categorica`/`combinar_E` sobre **tres** corredores (`L-solo`, `L+corpus`, `M`), mediana por cuantil para continuas (punto y, cuantil a cuantil, intervalo), moda de tres para categóricas/ordinales con `SIN DECISIÓN` declarada si los tres difieren. Cabecera cita la definición sellada y las cuatro razones de mesa (forecast combination puzzle, mediana vs. media, tres vs. dos, sin entrenar). `if __name__ == "__main__"` sigue lanzando `SystemExit` — **no se ejecuta en este acto**.

## T2 · `mesa-pendientes.md` §3

Sección RESUELTA añadida con fecha `2026-08-21` y cita de `ADR-141`/`FP-99`. Texto original de la PROPUESTA de dos corredores **no se borra** — regla del propio archivo (`§Cómo cerrar este archivo`).

## T3 · ADR + tablero

`canon/gobernanza-v1_15.md`: `ADR-141` nuevo, cabecera `140→141` ADR. `canon/estado-programa-v1_10.md`: cabecera y `L0` recifrados `140→141`, con nota de cascada. `forense/firmas-pendientes.tsv`: `FP-99` `ABIERTA`→`FIRMADA`, `firmada_en=2026-08-21`, `encargo=forense/encargos/2026-08-21-SELLA-OPLUS.md`.

## Cierre

Contador de medición sobre México: **0**. El corredor `E` deja de estar bloqueado (definición sellada existe); sigue sin correr ninguna celda. `forense/hallazgos.md`: línea nueva. Perímetro respetado: `corredor-E-combinacion-LM.py`, `mesa-pendientes.md` (solo marcar RESUELTA), `gobernanza`, `tablero`, `hallazgos`, esta nota, el encargo.
