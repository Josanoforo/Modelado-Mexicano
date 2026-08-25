# Cierre `ACTO CONGELA-SORTEA` (Acto A) — 25/ago/2026

**Encargo:** `forense/encargos/2026-08-25-PACK-CONGELA-SORTEA.md`. **ADR:** `ADR-179` (`canon/gobernanza-v1_15.md`). **Fila de tablero:** `FP-154` (`forense/firmas-pendientes.tsv`), nace `FIRMADA`. **Entorno:** NUBE (`cloud_default`).

## Compuerta F0-A

Firma de mesa recibida como línea propia, fuera de la cita del encargo (candado de autocaptura, `FP-63`):

> `FIRMO: para el piloto v1 gobierna el marco vigente de 60 bajo FP-150/ADR-178; las 253 de #349/#352 son pool de saturación (marco-produccion-total-v1_0.tsv se lee como pool-candidatas-autorizadas), no marco v1; FP-82 queda satisfecha como barrido y medición de la oferta. Fijo n_sorteo=15 dentro del rango pre-registrado 12–15. Procede CONGELA-SORTEA.`

A.8 re-corrido en fresco contra `dfdf4fd`: tablero sin fila que adjudique el ruling, `n_sorteo` libre en el reglamento (rango 12-15, línea 121), congelado/ejecutable ausentes (solo homónimos ajenos), `DIN-09.frase_discriminacion` seguía defectuosa. Nada de esto ya estaba hecho — se procedió.

## Qué se hizo

1. **`ADR-179`** (`canon/gobernanza-v1_15.md`): ruling de mesa con tres incisos (a) marco de 60 gobierna, 253 = pool de saturación, `FP-82` satisfecha en su objetivo de barrido; (b) `n_sorteo=15`, cuota dura `floor(0.20·15)=3`; (c) sucesores (corrección `DIN-09`, congelado, `sorteo_v2.py`, `tests_sorteo_v2.py`, Acto B). Cabecera de gobernanza recifrada 178→179.
2. **`FP-154`** en `forense/firmas-pendientes.tsv`, nace `FIRMADA` con el verbatim íntegro, `gatea` = Acto B y la lectura del pool en versiones futuras del marco.
3. **`DIN-09.frase_discriminacion`** (`forense/marco-candidatas-piloto-v1_0.tsv`) corregida quirúrgicamente: la afirmación de que SF5-2021 es "la misma pregunta que DIN-08/SF7" era falsa (refutado por la propia columna `publicada` de la fila — el manual 2021 trae SF5/SF6/SF7 como tres reactivos distintos, SF7 sin cambio de mnemónico). Verificado por `git diff`: una sola línea, una sola fila, ninguna otra celda tocada.
4. **`forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv`**: copia byte a byte del marco post-corrección (`cmp` limpio).
5. **`forense/prereg-duelo-v2/CONGELADO-v1_0.sha256`**: sha256 del congelado y del reglamento.
6. **`forense/prereg-duelo-v2/sorteo_v2.py`**: implementación de §2-§2.3 del reglamento sellado por `ADR-178`. Universo `P1/P2 × {SI,NO}` con `assert len == 50`. Deriva semilla vía `derivar_seed_scope` (`scoring-adv1-m3.py:685`), reutilizada, no reinventada. PRNG: `random.Random` de la librería estándar (numpy no disponible en este entorno; el reglamento cita PCG64 como ejemplo, no mandato — declarado en el docstring del módulo). **No corre el PRNG en este acto.**
7. **`forense/prereg-duelo-v2/tests_sorteo_v2.py`**: los tres casos de §5 (normal, infactibilidad+fallback, límite de cuota) más determinismo (misma semilla, mismo marco ⇒ mismo resultado) y sanity de carga del congelado. **12/12 verdes.**
8. **`canon/estado-programa-v1_10.md`**: recifrado 178→179 en la cabecera de artefactos y en la línea L0 (§ programa), con nota fechada 25/ago/2026 citando este cierre: "congelado listo, sorteo pendiente de semilla de merge".

## Qué NO se hizo (perímetro)

No se corrió el sorteo real ni se derivó una semilla numérica — el SHA de merge de este PR no existe todavía (§3.1/§3.3 del reglamento). No se tocó `data/curacion-universo/**` ni `tools/**`. No se reabrió ni podó el marco de 60. No se movió Hito D. No se tocaron otras celdas de `DIN-09` ni otras filas del marco.

## Suite

`timeout 900 python3 tests/check.py --baseline` corrido antes y después del acto (sin `--freeze`). Cifras medidas, no declaradas por adelanto.

## Siguiente paso

Mesa fusiona el PR de este acto. El SHA de ese merge es la semilla en potencia del Acto B (`ACTO SORTEA`), que no puede lanzarse antes de que ese commit exista en `main`.
