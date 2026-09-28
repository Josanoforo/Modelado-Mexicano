# Nota de cierre · GEN2-ASTRA-CONTINUIDAD-C2-1 · 28/sep/2026

28/sep/2026 · `ACTO GEN2-ASTRA-CONTINUIDAD-C2-1` (NUBE, AUTÓNOMO-AMPLIO, 0-bis `ba6ccd23`, base e584ee5f; SHA de redacción `3a7b61db`). Encargo `forense/encargos/2026-09-28-GEN2-ASTRA-CONTINUIDAD-C2-1.md`. Claude retoma el carril C2 de Codex. P1: `forense/analisis/familias-2027/EXPEDIENTE-v1_0.md` + `familias-2027-estado-v1_0.tsv`, con 8 filas (6 familias Astra + ENOE-INFORMALIDAD y ENSU-CAMPECHE de frontera-1). Estados: 5 BLOQUEADA, 1 SUSPENDIDA (PAGO-DIGITAL) y 2 NO-LANZAR-TODAVIA. COMMIT-2 NO-HAY y OTS no en las 8 filas; 16/16 sha OK. P2: 39 singleton ENOE reproducidos por comando desde el artefacto agregado (no desde el diseño; NC ba6c-01); consulta INEGI en borrador, no enviada. P3: hashes 7/7, 7/7, 32/32 y 18/18; oros RETROSPECTIVA sin retador; 8 cruces vistos enumerados (E.6: cruce, no ola). P4: 21 NC de C2 → 2 CERRADA (7045-04, 996b-01), 6 DECISIÓN, 13 SIGUE-ABIERTA; hoja para mesa; FP nueva ba6c-01. Premisa caída: 71cf-01 sigue ABIERTA, no firmada. Cero mediciones; no adopta; no abre reservas. Nota: `forense/notas/2026-09-28-GEN2-ASTRA-CONTINUIDAD-C2-1-cierre.md`.

## Verificaciones (EJECUTADO)
- Base: `git rev-list --count HEAD..origin/main` = 0 al arrancar. Duplicado: 0 ramas, 0 PR abiertos, 1 worktree.
- Entorno: el hook dio ENTORNO-DERIVADO = NUBE, igual al del encargo. Corpus montado = NO, 0 archivos examinados. No se tocó microdato.
- `git diff --stat origin/main -- forense/prereg-caja forense/prereg-duelo-v2 data/corrida0` = vacío: no cambió ninguna emisión ni spec.
- Conteo singleton: salida cruda en el EXPEDIENTE §2.
- `familias-2027-estado-v1_0.tsv`: ninguna celda vacía en gate_faltante ni en estado (lector CSV).

## Premisas
- [LEÍDO → FALSA] «`71cf-01` ya firmada»: la fila sigue ABIERTA. Es una premisa de estado, no de medición, y no es PARO: va en la hoja como pendiente.
- [SUPUESTO → parcial] «las seis familias tienen spec humana y spec.yaml»: ENIF y ENVIPE no tienen yaml en prereg-caja, y el tablero cita el spec.yaml del CALC. Es un hallazgo, no un PARO.
- [REPORTADO → sostenida] «ambos grupos y escenarios obligatorios»: está en `potencia/calcula.py:17-50`, pero no en la spec del paquete.
- La rama prevista en §5 se tomó: el diseño ENOE no está en el corpus de la nube, así que el conteo sale del artefacto agregado y la receta es para caja.

## Trabajo por subagentes
P1, P2+P3 y P4 corrieron en subagentes con perímetro propio. El hilo principal ensambló y verificó los dos cierres de NC por `git merge-base --is-ancestor`.
