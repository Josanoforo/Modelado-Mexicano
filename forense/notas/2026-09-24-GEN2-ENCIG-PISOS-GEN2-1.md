# ACTO GEN2-ENCIG-PISOS-GEN2-1 · censo de origen de los pisos C2 · piso ENCIG 2025 re-medido · re-adjudicación -0002

24/sep/2026 · CAJA · rama `acto/gen2-encig-pisos-gen2-1` · 0-bis `19a384ae` (hhhh `19a3`) ·
base `origin/main` `3423b498` (merge de #1112, ADOPCION-2) · encargo
`forense/encargos/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1.md` (SHA de redacción `3d138c66`,
ancestro de la base: `git merge-base --is-ancestor` → sí).

**Contadores, en una línea:** P1 no mueve ninguno (censo); P2 y P3 sellan dos CALC
(`cuenta_gen2: SI`, no adoptan); `celdas_validadas` no cambia de número.

## 0 · ARRANQUE y premisas

- Guard 0: `rev-list HEAD..origin/main` = 0 · árbol limpio · duplicado: 0 ramas remotas, 0 PR
  abiertos, el único worktree es el propio · `limpia_arbol --reporta`: base al día.
- ENTORNO (`tools/entorno.py --sonda-red`): `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`
  · `red=200` · `raices=data_raw:SI descargas_mx:SI` · `corpus=SI(examinados=490)` → CAJA.
  `data/raw` enlazado a `/home/pc0/mm-corpus/raw`; `data/raices.local.yaml` copiado.
- PARO (f) no aplica: `ls data/corrida0 | grep -c 'ENCIG2023-PISOS\|ENCIG-DUELO-2025-ADJUDICACION-0002'` → 0.

| premisa (rótulo) | verificación | resultado |
|---|---|---|
| `[LEÍDO]` `medidor.py:639` copia el `-C2-P` de las emisiones | leído en `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001/medidor.py:637-639` | se sostiene |
| `[EJECUTADO]` `decisiones.tsv` no es fuente del censo; el censo sale de seguir la cadena | `_propaga_envuelto` de `tools/corrida0.py:3947` sobre `_lee_oferta` | se sostiene, **pero** el resolvedor sólo sigue `inputs`: no ve números tecleados en `parametros` (§1) |
| `[SUPUESTO]` piloto 3 y pisos ENVIPE/ENIF del árbitro tienen C2 NUEVO | leído medidor y spec de cada CALC que emite un C2 consumido | **piloto 3: sí. ENIF (DIN) y ENVIPE (TRA): NO** — §1 |
| `[LEÍDO]` P2 = «piso ENCIG **2023** desde microdato» | spec del -0001 §3 y regla de pisos (v2.16 §4) | **premisa falsa**: el piso del duelo es la composición de marginales **2025**; lo legacy son los números, no la ola. Pregunta a mesa, §2 |

## 1 · P1 · Censo de origen de los C2 que consume el marcador

**Universo** (A.4): las 21 celdas-D de `data/curacion-registro/celdas-d/`; el marcador
(`tools/marcador_segmento.py:910-912`, `_celdas_d_c2`) consume como C2 **sólo** las que traen
`champion_actual: C2`, y de ellas cada sub-celda de `adjudicacion_por_celda` con
`id_candidato: C2` (su `calc` + `resultado_puntual`). Las otras 16 celdas-D tienen
`champion_actual` PERSISTENCIA (9, ENIF marginal16), BASELINE (3) o NINGUNO (4): no entran a
ese camino. Mecanismo: el resolvedor de linaje del registro sobre la oferta completa, más la
lectura del medidor y del `spec.yaml` de cada CALC emisor (el resolvedor no ve `parametros`).
Tabla completa, una fila por RESULT: `forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-censo.tsv`.

| celda-D | RESULT C2 | CALC que emite el punto | resolvedor mecánico | **clase del censo** | por dónde pasa la cadena |
|---|---|---|---|---|---|
| `DIN.ahorro_solo_informal.enif2024.localidad_x_edad` | 8 | `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` | NUEVO | **HEREDADO-DE-LEGACY** | `parametros.marginales_sellados_D9` (de `milpa/tramite-ola5-propuesta-v0.yaml`; NAC de `milpa/tramite.yaml`) → `medidor.py:373,391-408`; su control contra el árbitro da **NO-REPRODUCE** (Δ 1.20e-3) |
| `GOB.gobierno_digital.encig2025.edad_x_escolaridad` (piloto 3) | 16 | `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` | NUEVO (fila de mesa) | **NUEVO** | compone C2 de marginales de `encig25_base_datos_csv`; el C2 compuesto legacy sólo es control |
| `GOB.gobierno_digital.encig2025.edad_x_sexo` | 8 | `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` | HEREDADO (fila de mesa, firma S) | **HEREDADO-DE-LEGACY** | `:639` ← emisiones ← `CALC-C2-COMPUESTO-RESERVADAS-0001` ← `milpa/` |
| `GOB.gobierno_digital.encig2025.escolaridad_x_sexo` | 8 | `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` | HEREDADO (fila de mesa, firma S) | **HEREDADO-DE-LEGACY** | ídem |
| `TRA.evade_norma.envipe2025.escolaridad_x_dominio` | 12 | `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` | NUEVO | **HEREDADO-DE-LEGACY** | `parametros.marginales_sellados` (de `milpa/tramite-ola5-propuesta-v0.yaml:1715-1731`; NAC de `milpa/tramite.yaml:497`) → `medidor.py:223,281-291`; su control reproduce a 4.8e-7 |

**Conteo: 5 celdas-D · 52 RESULT consumidos como C2 · 4 celdas-D / 36 RESULT
HEREDADO-DE-LEGACY · 1 celda-D / 16 RESULT NUEVO · 0 HEREDADO-DE-GEN2.** Control positivo del
recuento: el resolvedor devuelve 52 linajes (52 = 8+16+8+8+12) y marca HEREDADO exactamente las
16 que ya tienen fila de mesa.

**Hallazgo del programa (más de 2 celdas → línea para el informe v1.3):** el `[SUPUESTO]` del
encargo cae para ENIF y ENVIPE. Sus pisos C2 se arman con marginales **tecleados en
`parametros`** desde la propuesta legacy, no desde sus inputs de manifiesto. El resolvedor de
linaje sólo recorre `inputs` y los ve NUEVO: es un falso NUEVO de clasificador, no de mesa.
Cada uno de esos CALC re-deriva el mismo C2 desde microdato (`-C2-P-REDERIVADO`): Δ máx
1.04e-3 en DIN y 1.10e-6 en TRA. Es decir, en ENVIPE el número apenas cambia; en ENIF el
control del propio CALC ya decía NO-REPRODUCE.
Línea para el informe v1.3: *«De los 52 pisos C2 que el marcador consume, 36 (4 de 5
celdas-D: ENIF localidad×edad, ENVIPE escolaridad×dominio y los dos cruces con sexo de ENCIG
2025) tienen el punto armado con marginales de la propuesta legacy; sólo el piloto 3 de ENCIG
lo mide desde microdato. Este acto releva los 16 de ENCIG; los 20 de ENIF/ENVIPE van a
GEN2-PISOS-GEN2-2.»*

Pregunta a mesa (§6 del encargo: «si el censo revela que el piloto 3 o el árbitro también
heredan de legacy») y respuesta, §2.

## 2 · Preguntas a mesa y respuestas (24/sep/2026, verbatim)

**Pregunta 1 (P2).** «P2 pide «piso ENCIG 2023 desde microdato», pero el C2 del duelo -0001
está definido como marginales ENCIG **2025** sin interacción (spec §3: expit(L p₂₅(a)+L
p₂₅(b)−L p₂₅)). Lo legacy son los números de esos marginales (6 decimales, tomados de milpa/),
no la ola. El piloto 3 ya resolvió esto re-estimando los marginales 2025 desde microdato, y mesa
lo acreditó NUEVO. Usar 2023 cambiaría el contendiente, que es el PARO (d). ¿Qué mide P2?»
**Respuesta:** «Marginales 2025 (Recommended)» — «C2 con la MISMA definición, re-medido desde
el microdato ENCIG 2025: 11 marginales de un eje, que no están reservados, más la composición y
el IC por réplica. Es el precedente del piloto 3. Control: reproduce
CALC-ARBITRO-MARGINALES-ENCIG2025-0001 a 1e-10 y el C2 sellado a 1e-5. El -0002 hereda todo lo
demás por sha.»

**Pregunta 2 (censo).** «El censo de P1 encontró que el C2 de ENIF (DIN localidad×edad, 8
celdas) y el de ENVIPE (TRA escolaridad×dominio, 12 celdas) también se arma con marginales
tecleados en `parametros` desde milpa/tramite-ola5-propuesta-v0.yaml, con el nacional de
milpa/tramite.yaml. El resolvedor mecánico los ve como NUEVO porque sólo lee `inputs`. DIN
además da NO-REPRODUCE en su control (Δ 0.12 pp); TRA reproduce a 1e-6. ¿Qué se hace con esas
20 celdas?» **Respuesta:** «NC a PISOS-GEN2-2 (Recommended)» — «Quedan en la tabla del censo y
en la línea del informe v1.3, con NC DIFERIDO-A: GEN2-PISOS-GEN2-2, que es lo que el encargo
prevé si salen más de 2 celdas. No se tocan aquí: están fuera del perímetro §9. Sigue abierto
si el marcador debe dejar de consumirlas, como pasó con las 16.»

Consecuencia logística declarada: el CALC del piso se llama `CALC-ENCIG2025-PISOS-GOBDIGITAL-0001`
(y su spec `ENCIG2025-PISOS-GOBDIGITAL-*`), no `ENCIG2023-PISOS-*` como nombraban el «hecho» y el
perímetro §9: el prefijo 2023 venía de la premisa que cayó, y la respuesta 1 de mesa la sustituye.

## 3 · P2 y P3 · congelados en el COMMIT-1

- Piso: `forense/prereg-caja/ENCIG2025-PISOS-GOBDIGITAL-spec-v1_0.md` + `CALC-ENCIG2025-PISOS-GOBDIGITAL-0001/{spec.yaml,medidor.py}`.
- Re-adjudicación: `forense/prereg-caja/ENCIG-DUELO-2025-ADJUDICACION-0002-spec-v1_0.md` +
  `CALC-ENCIG-DUELO-2025-ADJUDICACION-0002/{spec.yaml,medidor.py}`. Hereda por sha el medidor
  del -0001 (`74e8aa49…`) con el diff declarado en su spec §2; el test comprueba por AST que no
  cambió nada más.
- D-22: `tests/test_encig_pisos_gen2.py` (sintético con todas las ramas terminales, oro sobre
  ENCIG 2023 real contra `CALC-PISOS-ENCIG2023-EJES-0002` a 1e-10, guardias, mutantes, herencia
  por AST, identidad de esquema) → 14 passed. `corrida0 preflight` del piso: sólo `no_commiteado`;
  del -0002: sólo `no_commiteado` y los dos inputs del piso aún inexistentes (lo declarado para
  antes del COMMIT-3a).
