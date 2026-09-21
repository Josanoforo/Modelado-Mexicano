# Origen móvil de cuatro pisos mecánicos sobre la serie ENCIG · spec v1.0

ACTO GEN2-ENCIG-SERIE-Y-TENDENCIA-1 (21/sep/2026), pieza P3 y dictamen P4.
Rótulo de mesa: **RETROSPECTIVA-MECÁNICA** — el 2025 ya se vio, pero ningún
contendiente tiene un parámetro que alguien elija; las cuatro variantes
entran todas o ninguna (PARO b). Este CALC no cambia qué piso está
adjudicado: propone.

Procedimiento congelado en COMMIT-1 (script `tools/encig_origen_movil.py`
con sha256 en la nota del acto y esta spec con sidecar). Su `spec.yaml`
(`CALC-ENCIG-ORIGEN-MOVIL-0001`) se escribe cuando existan los cinco sellos
de la serie, porque sus inputs son esos `resultados.json` con hash — es
identidad de insumos, no procedimiento.

El primer resultado que produzca este procedimiento es el que se reporta.

## 1 · Insumos, todos sellados

- `CALC-ENCIG-SERIE-CANAL-{2015,2017,2019,2021,2023}/resultados.json`
  (P, IC-LO, IC-HI por celda; 11 celdas).
- Ola 2025: `milpa/tramite-ola5-propuesta-v0.yaml`, ids
  `tramite.gobierno_digital.util_sin_coercion_encig2025` (nacional:
  p 0.673393, ic95 [0.663165, 0.683910]) y
  `…_ejes_encig2025` (sexo, edad, escolaridad con ic95). Firmas de mesa a1 y
  s1 (2/sep/2026), copiadas a `milpa/tramite.yaml`; son los mismos R que el
  marcador usa para las diez celdas `SOLO-PISO`. Se usan éstos y no los
  nueve marginales de `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` porque aquéllos
  restringen a casos completos en edad × escolaridad (n 20 088) y la serie
  excluye inválidos solo del eje afectado (n 20 203), como el piso.

## 2 · Los cuatro pisos, en logit, sin parámetros

Para cada celda c y cada ola objetivo k con al menos una ola anterior con
estimación, L_i = logit(p_i), ee_i = (logit(hi_i) − logit(lo_i)) / (2·1.959964):

| piso | predicción L̂_k | mínimo de olas previas |
|---|---|---|
| PERSISTENCIA | L_{k−1} | 1 |
| TENDENCIA-2 | recta por las dos últimas olas, evaluada en el año k | 2 |
| TENDENCIA-3 | mínimos cuadrados (sin pesos) sobre las tres últimas, evaluada en k | 3 |
| TENDENCIA-SERIE | mínimos cuadrados sobre todas las anteriores, evaluada en k | 2 |

Toda predicción es Σ w_i L_i con pesos fijos; var(L̂) = Σ w_i² ee_i² (olas
independientes; misma aproximación que `CALC-PISO-PERSISTENCIA-ERROR-0001`);
IC95 del piso = expit(L̂ ± 1.959964·ee). Para PERSISTENCIA el IC es el
sellado de la ola k−1, verbatim. Un punto con P nulo no existe para su
celda: ni se predice ni predice.

## 3 · Qué se reporta

Por (ola, celda, piso): predicción, error = 100·(p̂ − R) en pp, y CUBRE
(SI si R ∈ IC95 del piso). Por piso: MAE sobre todas sus predicciones; MAE,
cobertura y MAE nacional sobre las **olas comunes** {2021, 2023, 2025} — las
únicas donde los cuatro están definidos; MAE por ola; y contra PERSISTENCIA,
en olas comunes: ΔMAE = MAE_P − MAE_piso y cuántos pares (celda, ola) vence.

## 4 · Dictamen (P4), reglas escritas antes de ver la serie

1. **Sube sostenida** (serie nacional, 6 puntos, 5 pares consecutivos):
   al menos 4 pares con incremento > 0, ningún par con decremento cuyo IC95
   no traslape con el anterior, y cambio total 2015→2025 > 0.
2. **Un piso de tendencia erra materialmente menos que la persistencia:**
   max ΔMAE sobre olas comunes ≥ **3.0 pp** (del orden del error que
   persistencia alcanza en ENVIPE/ENIF: 2–3 pp).
3. Palabra única:
   - `NO-DECIDIBLE` si las olas comparables por texto (P1) son < 3.
   - `CAMBIO-DE-INSTRUMENTO` si P1 declara un cambio de texto o flujo que
     entra en el estimando en alguna ola (`cambio_instrumento_en_ola`); P1
     no lo encontró: el parámetro va `NINGUNA` y la palabra solo puede salir
     si alguien lo cambia a la vista.
   - `TENDENCIA` si (1) y (2).
   - `SALTO-SIN-EXPLICAR` en cualquier otro caso.
4. La consecuencia para mesa (qué piso adjudicar en marginales con
   pendiente y con qué regla se decide que la hay) se escribe en la nota
   como propuesta, con las cifras de este CALC; no en el CALC.
