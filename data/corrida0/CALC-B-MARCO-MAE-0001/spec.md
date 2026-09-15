# `CALC-B-MARCO-MAE-0001` — el asiento de `B` sobre el marco de 14 celdas: cobertura, `err_pp`, control positivo y `MAE_pp(B)` con su `n`

Cara **local** de la spec sellada `forense/prereg-caja/B-MARCO-spec-v1_0.md`
(`prereg-caja-B-MARCO`, §5–§6). Manda la sellada. `medidor.py` y este archivo se
congelan en el `COMMIT-1` de `ACTO GEN2-B-MARCO`; **`spec.yaml` se instancia después
de que los tres CALC de serie sellen**, porque declara sus `resultados.json` por
sha256 (patrón de `CALC-C0D-MARCADOR-v3` / `IN-V2-RESULTADOS`). La regla no cambia
entre uno y otro momento: es el medidor.

## 1 · Qué hace

Por cada celda del marco (14, verificadas contra `marco-M-sorteado-v1_3.tsv`): cita
`P_B` de su CALC de serie (o de `CALC-B-0001` en FAM-M-06/07), lee el `R` sellado de
`corridas-R/<celda>.json`, calcula `err_pp = 100·(P_B − R)` (puntos porcentuales de
una proporción ponderada, A-bis.3) y el control positivo `Δ = P_obs − R` en tres ramas
pre-declaradas (`REPRODUCE-EXACTO` ≤ 1e-10 · `REPRODUCE-AL-GRANO` < 1e-6 ·
`NO-REPRODUCE`). Por brazo: `MAE_pp(B)` sobre las celdas cubiertas, **con su `n` y su
lista**, máximo absoluto y su celda, cobertura antes (2) y después. Las cuatro celdas
no-construibles salen `SIN-B` con su razón; no se rellenan.

## 2 · Qué NO hace

No lee `M` ni `L`, no ordena corredores, no adjudica: el veredicto de la tríada no se
toca. No compara `MAE_pp(B)` contra ningún otro MAE (A-bis.4: eso lo hace la nota,
descriptivamente y diciendo el universo).

## 3 · Envoltura, declarada antes de correr

Es el **único** CALC de la familia que lee `corridas-R/` (árbitros GEN1): por la regla
E.1 del registro es `envuelto_legacy = SI` por construcción. **No se le escribe firma
de contador**: consume un número GEN1 y forzar `cuenta_gen2 = SI` sería
miscategorizar para mover un contador.
