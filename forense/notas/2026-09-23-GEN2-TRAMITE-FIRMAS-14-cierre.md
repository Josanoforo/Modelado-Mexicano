# Nota de cierre · ACTO GEN2-TRAMITE-FIRMAS-14

23/sep/2026, entorno NUBE (hook: `ENTORNO-DERIVADO = NUBE`, `senal-corpus: montado=NO archivos_examinados=0`, `red: DENEGADA-POR-POLITICA`; acto no toca microdato ni red, consistente con lo declarado). Sonnet 5, MODO ABIERTO. Base al arrancar y al cerrar: `origin/main = 6a2cd6c7` (0 commits de diferencia, coincide con el SHA de redacción del encargo).

## Verificación de premisas (§4 del acto, A.17)

`[EJECUTADO]` re-verificado: `grep -c 'FIRMAS-14' forense/firmas-pendientes.tsv` → 0 antes de este acto (§4 del encargo, confirmado). Las once FP citadas en §1 están, las once, `ABIERTA` a `6a2cd6c7` — re-derivado por id, no de memoria (`sed -n` sobre `forense/firmas-pendientes.tsv` filas 422/465-503), y coincide exacto con `tools/cierre_acto.py` (`FP · Filas ABIERTA (11)`).

**Corrección de logística, no de qué se mide (§4-2, no es PARO).** El §3 del encargo afirma «`…657c-03` ya cerró con #1078». Verificado: `657c-03` (`FP-260923-GEN2-DUELO-ENCIG2025-CIERRE-1-657c-03`) sí está `FIRMADA`/cerrada, pero el PR real es **#1086** (`ACTO GEN2-CONTADORES-CONSUMO-1`, `git log --oneline --all | grep CONTADORES-CONSUMO-1` → `96e4973 Merge pull request #1086…`), no #1078 — ese número corresponde a otra sincronización de sesión (`aeb5806`, ADENDA-1 de FIRMAS-12/PR #1067). Se declara la diferencia y se sigue: el objetivo (P2, verificar que `657c-03` no siga `ABIERTA` en ninguna vista) sigue alcanzable y no depende del número de PR citado.

## ADENDA-1 (dirección, mid-sesión)

Llegó durante esta sesión `GEN2-TRAMITE-FIRMAS-14-ADENDA-1` (dirección, no mesa): corrige el punto **I** de §1 (`merge_group` ya está en `verify.yml` #1062; Astra entra con recibo de Codex en el PR) y actualiza el rótulo esperado del veredicto de `AUDITORIA-POST-HOC-ASTRA-1` para D/E/F, de `LIMPIO` a `RECIBO-COMPLETO`. Archivada verbatim y sellada en el 0-bis (`forense/encargos/2026-09-23-GEN2-TRAMITE-FIRMAS-14-ADENDA-1.md`, `.cuerpo.sha256`). **No trae firma de mesa**: sigue siendo una recomendación de dirección con texto de firma propuesto, no una firma dada. No cambia el fallback de §2.

## Qué se hizo (§2 del encargo: sin firmas de mesa al lanzar, fallback textual)

Ninguna firma verbatim de mesa llegó con el lanzamiento de este acto. Por §2, el fallback aplica letra por letra:

- **B** (`657c-04`) y **C** (`988c-01`, `FP-260923-GEN2-CONTADORES-CONSUMO-1-988c-01`): campo `estado` de `forense/firmas-pendientes.tsv` pasa de `ABIERTA` a `EJECUTA:CONTADORES-CONSUMO-2` (A.16, token por prefijo). Edición dirigida por línea (Python, sin `csv.writer` de round-trip), verificado con `git diff` que solo esas dos líneas cambiaron.
- **G** (`cfce-01`): `estado` pasa de `ABIERTA` a `EJECUTA:SELLO-EXTERNO-2`, misma técnica de edición, misma verificación.
- **J** (`3d56-01`): sin cambio — ya trae `vence: 2026-09-27` desde `FP-260923-GEN2-TRAMITE-FIRMAS-11-05da-04`; P3 del encargo («`vence:` en J y K») ya está satisfecho para J.
- **K** (`c3fa-05`): sin cambio — «Dueño mesa; fecha a fijar» sigue siendo la única información; P3 no se puede ejecutar para K sin la fecha que §6 pide preguntar a mesa. Declarado en `## NO-CORRIDO / RESERVAS`.
- **A** (`657c-02`), **D** (`1f30-01`), **E** (`1f30-02`), **F** (`e422-01`), **H** (`4296-01`), **I** (`1269-01`): sin firma de mesa, quedan `ABIERTA`, sin cambio. Declaradas, las seis, en `## NO-CORRIDO / RESERVAS` con `DECISIÓN-DE-MESA-PENDIENTE`.

**P2 (cierre de lo ya resuelto).** `657c-03` verificado en las siete vistas que lo mencionan (`forense/firmas-pendientes.tsv`, `forense/no-corrido.tsv`, `forense/hallazgos.md`, `forense/prereg-caja/METRICA-CELDAS-VALIDADAS-spec-v1_0.md`, `canon/gobernanza-v1_15.md`, `canon/registro-rotulos.tsv`, `canon/L0/ADR-260923-GEN2-CONTADORES-CONSUMO-1-988c-01.md`): ninguna lo deja `ABIERTA`. No se edita nada por P2 — «ninguna otra sin verificar por id» (A.17) también se cumple: A, B, C, D, E, F, G, H, I, J, K se releyeron por id antes de heredar su estado (arriba).

## Lo que no se hizo

No se ejecutó ninguna de las once decisiones (§10 del encargo: «No ejecuta ninguna decisión»). Específicamente, sin firma de mesa: A, D, E, F, H, I quedan `ABIERTA`; la fecha de K sigue sin fijar. Detalle y razón de cada una en `## NO-CORRIDO / RESERVAS` del encargo archivado y en `forense/no-corrido.tsv`.

## Contadores

`celdas_validadas`: 219 → 219 (sin cambio, `tools/cierre_acto.py` @ `9556bbb2`). CONTADOR del acto: cero mediciones (declarado en la cabecera del encargo); las adopciones que este acto asienta no mueven ningún contador hasta que `CONTADORES-CONSUMO-2`/el canal corran.

## Suite

`python3 tests/check.py --rapido` → VERDE, 0 FAIL.
