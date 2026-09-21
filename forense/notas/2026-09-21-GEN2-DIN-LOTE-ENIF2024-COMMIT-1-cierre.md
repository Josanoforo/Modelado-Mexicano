# Nota de cierre · `ACTO GEN2-DIN-LOTE-ENIF2024-COMMIT-1` · 21/sep/2026 · CAJA

**Qué queda.** El lote de 14 cruces de ENIF 2024 (`ahorra_solo_informal`, 96 celdas, 8
contendientes) queda **congelado según D-22 ampliada, demostrado con salida cruda**: spec humana
v1.0 sellada (`forense/prereg-caja/DIN-lote-enif2024-spec-v1_0.md`, sha `64bb52f2…`, sucesora de la
PROPUESTA de `#967`, intacta), un módulo propio (`tools/lote_enif2024/`) que **importa**
`tools/duelo/cruces_familia.py` (`#968`, sin editar) y lo completa con R3 (raking), cobertura y
B-bis, dos contratos encadenados (`CALC-DIN-LOTE-ENIF2024-EMISIONES-0001` → `…-ADJUDICACION-0001`,
`secuencia_commits` 2 → 3a → 3), tres oros **sellados y verificados**, la simulación de potencia y el
paquete L final. **Contadores:** `N_corridas_selladas` +3 (`CALC-DIN-LOTE-ORO-PILOTO1-EMISIONES-0001--7105a567af3c`,
`…-ADJUDICACION-0001--3dfbc47588fd`, `CALC-DIN-LOTE-ORO-C2IC-0001--a254c50efa24`), las tres
RETROSPECTIVA, ninguna adjudica; `cuenta_gen2 = SI` en las dos del piloto 1 y **`NO` en el oro del
C2-IC** por regla E.1 en cadena (consume `CALC-C2-COMPUESTO-IC-ENIF2024-0001`, que a su vez tomó
sus puntos de `milpa/tramite-ola5-propuesta-v0.yaml`; lo marca el registro, no la spec);
`adoptados_activos` sin cambio; **ningún cruce de 2024 sellado** (`R-EXISTE-EN-ESTE-COMMIT = NO`).

## 1 · Los cuatro requisitos de D-22 ampliada, con la salida cruda

1. `corrida0 preflight CALC-DIN-LOTE-ENIF2024-EMISIONES-0001` → **`PRE-FLIGHT: VERDE`** (único
   aviso: `spec_md_no_esta_en_origin_main`, primera corrida de una spec no fusionada).
   `…-ADJUDICACION-0001` → `BLOQUEADO input_repo_ausente=emisiones_selladas:… input_repo_no_commiteado=emisiones_selladas input_repo_ausente=emisiones_sello:… input_repo_no_commiteado=emisiones_sello`
   — exactamente los bloqueos previstos en `secuencia_commits.preflight_esperado_antes_del_commit_3a`, y ningún otro.
2. `_valida_outputs` **vacío en cada rama terminal**, sobre sintético (`tests/test_lote_enif2024.py`,
   31 tests: todas con soporte · parcial · fuera de soporte global (0 puntuadas, `NO-ADJUDICABLE`,
   B-bis `FALSADOR-DEBIL`) · celda rara vaciada en 2021 · marginal con masa cero en 2024 · ola nueva
   chica · emisiones alteradas → PARO antes de abrir R) y sobre oro (tres sellos con `sello COINCIDE`).
3. **Todo id anulable declarado** por lectura estática: el catálogo de RESULT lo deriva el propio
   medidor (`catalogo_resultados()`), `permite_no_estimable` en 1 655 de 2 184 ids de emisiones y
   1 395 de 2 913 de adjudicación; `corrida0 ensayo` no existe (F4, TUBERÍA) → el ensayo va como test.
4. **Ningún input con hash sobre archivo vivo**: `resultados.json`/`spec.yaml` de CALC sellados y dos
   módulos de código versionado (`cruces_familia.py` `a41bdb07…`, `lote_familia.py` `96821de2…`),
   cuyo sha se emite además como RESULT en cada corrida.

## 2 · Los dos oros (P3 i, ii) y la potencia (P3 iii)

- **Oro (i), piloto 1 (`localidad × edad`, régimen `PILOTO-1`, insumos del piloto).**
  `CALC-DIN-LOTE-ORO-PILOTO1-EMISIONES-0001`: **56 valores cotejados (P2 = C1: P/IC/n; C2: P/IC),
  `CTRL-DELTA-MAX = 5.55e-17`, tol 1e-9 → `REPRODUCE`**. `…-ADJUDICACION-0001`: emisiones
  reproducidas a 1e-10 **antes** de abrir R (`EMISIONES-DELTA-P-MAX = 0.0`), luego **la R del piloto 1
  (32 valores: P/IC/n) a `0.0`**, y el par vetado probado (`ReservaRota: par (sexo, edad) NO autorizado`).
  Lectura ilustrativa, no adjudica: C2 MAE 1.467 pp (= el sellado), R2 1.335, R1 1.202, R3 1.217,
  P2 2.644; ΔMAE(R2) +0.13 pp, IC95 [−0.39, 0.65] → `NADIE-VENCE`; R2 yerra menos que C2 en 4/8; cobertura R-en-IC: C2 7/8, R2 7/8,
  P2 4/8; B-bis mecánico `CORROBORADA`.
- **Oro (ii), C2-IC (9 pares EMITIBLE, 68 celdas, régimen `ARBITRO-2024`).**
  `CALC-DIN-LOTE-ORO-C2IC-0001`: marginales re-derivados = `#971` a **0.0** (15/15); **IC95 del C2
  réplica a réplica `DELTA-IC-MAX = 0.0`** (68/68, tol 1e-10); punto `DELTA-P-MAX = 1.7e-6` con causa
  declarada (el C2-IC redondeó a 6 decimales desde el yaml; el lote usa `#971` a precisión completa).
- **Potencia de la regla v0.3** (`forense/analisis/gen2-din-lote-enif2024-commit-1/potencia-v0_3.md`,
  35 celdas puntuadas de los pilotos, ruido calibrado al EE sellado del piloto 3, 20 000 lotes; cota
  superior): con el efecto **S½ del piloto 3 (1.10 pp)**, P(IC95 despeja 0.5 pp) = **0.52 (15 celdas)
  · 0.78 (35) · 0.85 (44) · 0.94 (68)**; con el de Sλ (1.47 pp): 0.81 · 0.98 · 0.99 · 1.00; con 0.5 pp
  de efecto real, 0.10 en cualquier n. **No cambia la regla.**

## 3 · Lo que este acto encontró distinto de lo que el encargo suponía ([HALLAZGO], §16 de la spec)

- **Q1 · El C2 sellado cubre 9 de 14 pares, no 14.** Los 5 pares con `formalidad` son
  `NO-EMITIBLE` (A-bis 4) en el dictamen sellado; el «C2 restringido a quien trabaja» de F2 no existe
  sellado y exige leer 2024 por `trabaja × eje` (PARO a). Congelado: sin piso, sólo `P2`; `R1/R2/R3`
  `null` declarados. Opciones a mesa: (A, recomendada) así; (B) sucesor sella los 13 marginales
  restringidos antes del COMMIT-2 y una enmienda con archivo propio añade `C2-restringido`; (C) fuera del lote.
- **Q2 · Dos regímenes de universo.** Piloto 1 y PROPUESTA §1: 13 492 personas (18–97, TLOC, centinela
  fuera); árbitro/`#971`/C2-IC: 13 502 con «fuera» por eje. El medidor lo lleva como parámetro; el lote
  usa `PILOTO-1` (la PROPUESTA; el universo no es del ejecutor). La mezcla punto-sellado/réplicas-propias
  es la del piloto 1 y se emite (`RESULT-DIN-LOTE24-EM-M24-<eje>-<cat>-DELTA-SELLADO`; peor 1.2e-3 en el oro).
- **Q3 · `#973` (`tools/agrega_l_v1_0.py`) no está en `main`**: el paquete L lo cita, no lo importa.
- **2024 trae 10 centinelas `98` (fuera) y 5 personas de `97` («97 años y más», dentro bajo `PILOTO-1`; el
  árbitro las saca del eje edad) y 4 códigos 99 de escolaridad (fuera del eje)**; en 2021, 36 centinelas y
  `P3_1_1` (no `NIV`), catálogo del zip **COINCIDE** con el declarado.

## 4 · Pisadas mecánicas, declaradas

`registro --verifica --escribe --lote` tras la fusión de `main` re-derivó `fuente_replay` de cuatro
corridas ajenas (`CALC-DIN-CREDITO-PISOS-ENIF201{2,5,8}-0001`, `CALC-DIN-CREDITO-K8-ENFIH2019-0001`) a
`VERIFY-AISLADO` por asientos que `main` ya traía; ningún veredicto cambió. Durante el acto,
`tools/asienta_replay_aislado.py --help` **escribió** una fila ajena (`CALC-WBES2023-PRECISION-INTERACCIONES-0001`)
en `forense/replay-evidencia.tsv` (ignora los argumentos); se retiró antes de commitear y se anota en hallazgos.

## 5 · Sucesores

COMMIT-2 / 3a / 3 **en otra sesión** (F3), con mesa habiendo sellado antes las capturas `L`
(`PAQUETE-L-LOTE-ENIF2024-v1_0.md` + `prompts.jsonl`, 88 prompts, sha `ad774cec…`). Filas:
`FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-01..04`, `NC-…-6c10-01..03`.
