# Sorteo del marco-M v1.1 — `ACTO MAESTRA33-B2 · MARCO-M-SORTEA-v1_1` (ACTO B″), resultados

## Pre-registro del primer commit (antes de correr el PRNG)

- `SHA_A` (dado literal por el encargo, no re-derivado): `af41796f50baad1737987b7e9a1e737c38ab85f2`. Verificado: (a) `git merge-base --is-ancestor af41796f50baad1737987b7e9a1e737c38ab85f2 origin/main` → ancestro; (b) `git show af41796 --stat` → `Merge pull request #410 from Josanoforo/claude/maestra32-e20-lote-nube-elu7me` — "ACTO MAESTRA32-E20: Load 4 rules, re-emit P1, freeze framework M", que es exactamente el commit que escribe `forense/prereg-duelo-v2/marco-M-congelado-v1_1.tsv` y `CONGELADO-M-v1_1.sha256` (`git log --oneline -- forense/prereg-duelo-v2/marco-M-congelado-v1_1.tsv forense/prereg-duelo-v2/CONGELADO-M-v1_1.sha256` → un solo commit, `77939ce P2 A'' MARCO-M-CONGELA-v1_1: 27 filas, N_elegibles=22 bajo F-DD`, contenido en ese merge). Coincide con la `SHA de redacción` que el propio encargo declara.
- `scope_id = "MARCO-M-v1_1"` (dado literal por el encargo — distinto del `"MARCO-M-v1"` de B′, así que la semilla no puede coincidir con la de B′ ni con la del `ACTO B` original por construcción, §3.4 del reglamento).
- Semilla derivada por `sorteo_v2.semilla_desde_sha_merge(SHA_A, "MARCO-M-v1_1")` (misma función, `sorteo_v2.py:191`, importada sin editar — vía `sorteo_marco_m.py`, que ya la reexporta): **`34354141898495593251517379743390345279`**.
- `N_elegibles`: leído de `forense/prereg-duelo-v2/CONGELADO-M-v1_1.sha256` → `N_elegibles=22`. sha256 recomputado de `marco-M-congelado-v1_1.tsv` (`8e6459dd49869063986daa16cfbb8067575ee7c747e3cadd6a35f1b51d582477`) coincide byte a byte con el declarado en ese archivo. **Control PASA** — sin este control no habría corrida.
- **Hallazgo, no decisión de este acto — columna de elegibilidad correcta.** `marco-M-congelado-v1_1.tsv` trae DOS columnas de elegibilidad: la legacy `elegible` (23 filas `SI`) y la nueva `elegible_v1_1` (22 filas `SI`, bajo el criterio F-DD de `ADR-237`: `(transferencia==SI) AND (en_corpus==SI) AND (la estadística tiene regla en cargar_reglas() post-P0)`, según el propio sidecar `CONGELADO-M-v1_1.sha256`). Esta junta ya fue adjudicada por `FP-208`/`ACTO MAESTRA33-E2 · AGENTE-DESPACHO-1` al encolar este encargo, y el encargo mismo declara `N_elegibles esperado 22` — coincide con `elegible_v1_1`, no con `elegible`. Este acto sortea sobre `elegible_v1_1`. `sorteo_marco_m.cargar_marco_m` (v1_0, no editado) no conoce esta columna y no se usa contra este archivo — ver `sorteo_marco_m_v1_1.py`.
- **Hallazgo, no decisión de este acto — columna `estrato`.** De las 22 filas elegibles, 21 traen `estrato=PENDIENTE` (valor placeholder — las celdas de transferencia que `ACTO MAESTRA32-E15 · MARCO-M-CORRIGE-Y-CENSA` censó no llevaban `estrato` propio, a diferencia de `TRA-M-01`/`TRA-M-02` originales) y solo `TRA-M-02` trae un valor real (`tramite|P1|MEDIA`). El mecanismo de `sortear()` trata `PENDIENTE` como un estrato válido más (agrupa por el valor literal de la columna, sin juzgarlo) — este acto no reclasifica ni inventa un `estrato` mejor: reporta el dato tal como el congelado lo trae, y dirección decide si vale la pena una estratificación real para v1.2.
- Regla de tamaño (`ADR-231` §e, `forense/notas/2026-08-31-marco-M-spec.md`, fijada por `MAESTRA32-E13` antes de ver ningún `N` — la misma función `regla_de_tamano`, no editada, reutilizada tal cual la usó B′): `N≥30 → n_sorteo=15`; `15≤N<30 → n_sorteo=ceil(N/2)`; `N<15 → sin sorteo`. Con `N_elegibles=22`: **`n_sorteo = ceil(22/2) = 11`**; **`cuota_max = floor(0.20·11) = 2`**. A diferencia de B′ (`N=2<15`, identidad), aquí `N=22≥15`: el PRNG **sí** corre.
- Clasificación F-DD por celda (`ADR-237`): ya congelada en la columna `grado_DD` de `marco-M-congelado-v1_1.tsv` para cada fila (no se deriva de nuevo en este acto — sería redescubrir lo que `MAESTRA32-E20` ya selló). Las 22 filas elegibles traen las 22 `grado_DD=P1 PUNTUA` (consistente con el criterio de elegibilidad, que ya excluye por construcción las 5 filas `P0 VERIFICACION-NO-PUNTUA` de calibración — esas 5 se conservan en el archivo pero fuera del universo sorteable). Este acto reporta el valor `grado_DD` real de cada celda que salga sorteada, no lo asume.
- Invocación exacta a ejecutar:
  ```python
  from sorteo_marco_m_v1_1 import cargar_marco_m_v1_1, semilla_desde_sha_merge, regla_de_tamano, sortear_marco_m

  SHA_A = "af41796f50baad1737987b7e9a1e737c38ab85f2"
  semilla = semilla_desde_sha_merge(SHA_A, "MARCO-M-v1_1")
  marco = cargar_marco_m_v1_1()  # marco-M-congelado-v1_1.tsv, filtrado elegible_v1_1=='SI', assert n == N_elegibles de CONGELADO-M-v1_1.sha256
  n_sorteo, cuota_max = regla_de_tamano(len(marco))
  resultado = sortear_marco_m(marco, n_sorteo=n_sorteo, cuota_max=cuota_max, semilla=semilla)
  ```
- Semillas anteriores de la misma familia — no reutilizadas bajo ninguna circunstancia (§3.4, `scope_id` distinto las distingue por construcción): semilla anulada `867948c` (`ADR-135(d)`), semilla del `ACTO B` original (`174266824551963846210387427777144587800`, `scope_id="ACT-PIL-3-v1"`), semilla de B′ (`63114853283919194858838455602446543838`, `scope_id="MARCO-M-v1"`).

**El primer resultado que produzca este procedimiento es el que se reporta.**

---

## Resultado (segundo commit — salida íntegra, una sola corrida)
