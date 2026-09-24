# Re-adjudicación del cierre ENCIG 2025 con piso de cadena limpia · CALC -0002 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-ENCIG-PISOS-GEN2-1`, 24/sep/2026, CAJA, rama
`acto/gen2-encig-pisos-gen2-1`, 0-bis `19a384ae`. Encargo:
`forense/encargos/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1.md` (P3). Congelada en el COMMIT-1,
antes de sellar el piso (P2) y antes de correr este árbitro.

Firma que la ordena, verbatim del encargo §2 (Decisión 1 de ADOPCION-2, mesa 24/sep/2026):
«Las 16 celdas -C2-P de CALC-ENCIG-DUELO-2025-ADJUDICACION-0001 salen del consumo del
marcador como medición, rotuladas «piso de origen legacy, no adoptable», hasta que un acto en
caja re-mida el piso ENCIG 2023 desde microdato y re-adjudique el cierre con un CALC sucesor
-0002 que cite ese piso por id; el acto cuenta primero cuántos otros C2 de celdas-D tienen
origen HEREDADO de legacy.» La ola del piso la precisó mesa el mismo día: marginales **2025**
(respuesta verbatim en `ENCIG2025-PISOS-GOBDIGITAL-spec-v1_0.md` §0).

## 1 · Herencia por identidad de archivo

Todo el procedimiento es el del -0001 y **no se re-decide aquí**:

| pieza | archivo sellado | sha256 |
|---|---|---|
| spec humana | `forense/prereg-caja/ENCIG-DUELO-2025-cierre-spec-v1_0.md` | `2cf3bb9578b44df8329f65f5cde7c83fc254c68125be229a67bc310f1df8623d` |
| medidor | `data/corrida0/CALC-ENCIG-DUELO-2025-ADJUDICACION-0001/medidor.py` (= `tools/encig/duelo_2025/duelo.py`) | `74e8aa49938616299f7464e4a7cf8a94a46b83a3550ec52552587510debf86d4` |

Mismos: estimando, universo, celdas, receta ENCIG (`31d7cf3b…`), R (10 000 réplicas,
`PCG64(20260919)`), soporte (`n ≥ 200`, `round(k/3)`), regla primaria (`_estado_gana` del
piloto 4 por AST, `ed6e80b8…`), **umbral 0.5 pp**, B-bis y su precedencia, cobertura,
**contendientes** (C2 piso; C7, C-ENCOGIDA, C-ASTRA retadores; C1 referencia), las dos
emisiones selladas del -0001 (`509a501b…`, `f56b0201…`, `889b7def…`, `e3d84557…`) y sus
guardias de sello. Regla 6 (sin retadores nuevos) y PARO d: nada de eso cambia.

## 2 · El único cambio de procedimiento, y lo que se añade

**Cambio:** el punto C2 de cada celda deja de ser el `-C2-P` de la emisión (copiado de
`CALC-C2-COMPUESTO-RESERVADAS-0001`, cadena a `milpa/`) y pasa a ser
`RESULT-ENCIG2025-PISOS-GOBDIGITAL-{CRUCE}-{a}-X-{b}-C2-P` de
`CALC-ENCIG2025-PISOS-GOBDIGITAL-0001`, **por id**. La fórmula es la misma; cambian los
números de origen (medidos del manifiesto en vez de tecleados a seis decimales). C7 y
C-ENCOGIDA siguen siendo las emisiones selladas (construidas en su día sobre el C2 legacy):
no se re-emiten, porque re-emitirlas después de ver R las volvería retrospectivas.

**Diff del medidor, completo** (el resto de funciones es idéntico por AST; lo comprueba
`tests/test_encig_pisos_gen2.py`):
- `PA = "…-ADJ2"` (ids propios; el -0001 conserva los suyos) y constantes `PA0001`, `PISO`;
- `INPUTS_ADJUDICACION_REPO` + `piso_c2_resultados`, `piso_c2_sello`,
  `adjudicacion_0001_resultados`;
- `_guardia_piso` (nueva, llamada al entrar): sha256 del `resultados.json` del piso = el de
  su `sello.json`; el piso declara `CTRL-MARGINALES-VEREDICTO` y `CTRL-0001-VEREDICTO` =
  `REPRODUCE` y `ORIGEN` = `NUEVO…`; si no, **PARA** sin leer el cruce;
- en `adjudicar`, `cand["C2"][c] := piso[id_piso_c2(c)]`; el punto de la emisión se conserva
  como `-C2-P-EMISION-0001` (descriptivo);
- `_control_oro_0001` (nuevo, E.5): todo lo que no depende de C2 — marginales `M-*`,
  `R-P/IC/EE`, `N-2025`, `DELTA-25`, `C2-P-RECALCULADO`, `C2-IC-LO/HI` y `D-{C7,C-ENCOGIDA,
  C-ASTRA,C1}` — reproduce el `resultados.json` sellado del -0001 **a `1e-10`**, id por id
  (`G-CTRL-ORO-0001-*`); un `NO-REPRODUCE` se reporta, no se ajusta;
- rótulos: `G-MARCA-EMISIONES` dice que C2 es **RETROSPECTIVA** (piso sellado después de R,
  cruce visto E.6) y los retadores siguen **PROSPECTIVA**; `G-FUENTE-C2`;
- esquema (`esquema_adjudicacion`, `_fila`): los `-C2-P` declaran `dependencias_numericas:
  [piso_c2_resultados]`; filas nuevas `-C2-P-EMISION-0001`, `G-FUENTE-C2`, `G-CTRL-ORO-0001-*`.

## 3 · Qué se espera y qué no se decide aquí

La diferencia entre el C2 legacy y el medido es del orden de `1e-6` (el control 2 del -0001
la midió en ≤ 5.6e-7). **No se predice el dictamen:** el -0002 corre y su primer resultado es
el que se reporta, aunque difiera del -0001. Dictamen y registro con el vocabulario del -0001
§4.1–§4.2: `champion_actual: C2` si el piso no fue vencido, controles `REPRODUCE` e IC de C2
en 8/8; si no, `NINGUNO`. **Este acto no adopta retadores.**

## 4 · Secuencia (E.6, heredada)

COMMIT-1: esta spec, la del piso, los dos `spec.yaml`, los dos medidores y el test.
COMMIT-2: `corrida0 run` del piso, sello, asiento. COMMIT-3a: este `spec.yaml` recibe el
sha256 del `resultados.json` y del `sello.json` del piso (única edición admitida;
`preflight` antes de esto: BLOQUEADO **sólo** por esos dos inputs). COMMIT-3: `corrida0
run` del -0002, sello, celdas-D, `decisiones.tsv`, asientos.

## 5 · Auditoría (afirma sobre México)

Hereda la del -0001 §9: proporciones de **trámites** de pago de luz en ciudades de 100 mil
habitantes o más; gradientes de edad y escolaridad como **acceso y oferta** antes que
preferencia; sexo, si muestra interacción, primero composición (quién es titular del
contrato). **PROSPECTIVA vs RETROSPECTIVA:** C2 del -0002 RETROSPECTIVA; C7/C-ENCOGIDA/
C-ASTRA/C1 PROSPECTIVA; ninguna frase de producto las mezcla. Contadores: una corrida
sellada; `celdas_validadas` no cambia de número (las dos celdas-D ya cuentan).

El primer resultado que produzca este procedimiento es el que se reporta.
