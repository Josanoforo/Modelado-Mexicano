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

## 4 · P2 · piso sellado (`CALC-ENCIG2025-PISOS-GOBDIGITAL-0001--94d00ae8a855`)

Primer y único `run` sobre ENCIG 2025, tras el COMMIT-1 (`c59233fc`) y la fusión de
`origin/main` (preflight VERDE en los dos momentos). 171 RESULT. Universo: 124 314 filas de
sec_7 → 20 203 trámites en universo y con diseño válido (189 `P7_3` fuera; 0 sin demografía).

| control (umbral de la spec §3) | valor | veredicto |
|---|---|---|
| marginales vs `CALC-ARBITRO-MARGINALES-ENCIG2025-0001` (`-P` 1e-10, `-N` exacto) | max \|Δ\| = 0.0 · 0 N discordantes | REPRODUCE |
| C2 vs `-C2-P-RECALCULADO` del -0001 y C2-IC vs su IC (1e-10) | 0.0 y 0.0 | REPRODUCE |
| C2 nuevo vs C2 legacy del -0001 (1e-5; descriptivo, MIXTO) | max \|Δ\| = 5.56e-7 | REPRODUCE |
| IC de C2 por réplica | 16/16 celdas | EMITIDO |

Asiento E.7: `tools/verifica_aislada.py` → REPRODUCE · IDENTICO, 171/171, max \|Δ\| 0.0.

## 5 · P3 · re-adjudicación (`CALC-ENCIG-DUELO-2025-ADJUDICACION-0002--e28f8accd675`)

COMMIT-3a (`sha256` del piso en el spec) → preflight VERDE → primer `run`. 521 RESULT.
**Oro del -0001 (E.5): REPRODUCE**, 230 ids (16 celdas × 13 sufijos + 22 de marginales), max
\|Δ\| = 0.0. Controles: marginales REPRODUCE (0.0); `CTRL-C2` 0.0 en los dos cruces (antes 3.0e-7 y
5.6e-7: ahora C2 *es* la composición en la ola). Verify aislado: REPRODUCE · IDENTICO, 521/521.

| cruce | MAE C2 (pp) -0002 · -0001 | ΔMAE C7 [IC95] | ΔMAE C-ENCOGIDA [IC95] | ΔMAE C-ASTRA [IC95] | GANADORES | **B-bis** | champion propuesto |
|---|---|---|---|---|---|---|---|
| edad × sexo | 0.965721 · 0.965719 | 0.1893 [−0.3674, 0.5654] | 0.1897 [−0.1693, 0.3342] | 0.1912 [−0.2658, 0.4799] | NINGUNO | **FALSADOR-DEBIL** | C2 |
| escolaridad × sexo | 1.007115 · 1.007109 | −0.4524 [−0.4877, 0.3323] | −0.2445 [−0.2452, 0.2655] | −0.3455 [−0.3663, 0.3180] | NINGUNO | **CORROBORADA** → SIN-CANDIDATO-SUPERIOR | C2 |

Agregado: **FALSADOR-DEBIL** (igual que el -0001). Nadie vence y nadie queda con reserva; el piso no
vencido es el estimador adjudicado (firma 17/sep). Comparado id por id con el -0001, el mayor
cambio numérico es 5.56e-5 pp (`D-C2` de superior × mujer, = 100 × el Δ de C2); de los textos sólo
cambian `G-MARCA-EMISIONES` y `G-SELLOS-EMISIONES`, que el diff declarado reescribe; **ningún
veredicto cambia**. El piso cambió de cadena, no de valor (\|Δ\| ≤ 5.6e-7): la re-adjudicación
confirma el cierre del -0001 con un piso de origen NUEVO, no es un cierre distinto. Por celda:

| cruce · celda | n 2025 | R (IC95) | C2 -0002 (IC95 NACE-CON-R) | C2 -0001 (legacy) | Δ C2 | \|C2−R\| pp |
|---|---|---|---|---|---|---|
| EDADXSEXO · 18-29×1 | 1489 | 0.7545 (0.7169, 0.7898) | 0.758481 (0.7305, 0.7861) | 0.758481 | -2.5e-07 | 0.397 |
| EDADXSEXO · 18-29×2 | 1317 | 0.7485 (0.7115, 0.7841) | 0.744834 (0.7163, 0.7724) | 0.744834 | -7.6e-08 | 0.364 |
| EDADXSEXO · 30-44×1 | 3331 | 0.7756 (0.7501, 0.7993) | 0.780967 (0.7625, 0.7983) | 0.780968 | -3.0e-07 | 0.538 |
| EDADXSEXO · 30-44×2 | 3677 | 0.7739 (0.7527, 0.7940) | 0.768203 (0.7501, 0.7855) | 0.768203 | -1.4e-07 | 0.571 |
| EDADXSEXO · 45-59×1 | 2803 | 0.6920 (0.6648, 0.7181) | 0.677089 (0.6555, 0.6978) | 0.677089 | -2.6e-07 | 1.490 |
| EDADXSEXO · 45-59×2 | 2996 | 0.6480 (0.6211, 0.6742) | 0.660899 (0.6380, 0.6834) | 0.660899 | -4.7e-08 | 1.287 |
| EDADXSEXO · 60-96×1 | 2331 | 0.4976 (0.4663, 0.5287) | 0.484825 (0.4595, 0.5103) | 0.484825 | -7.2e-08 | 1.273 |
| EDADXSEXO · 60-96×2 | 2144 | 0.4485 (0.4154, 0.4829) | 0.466590 (0.4418, 0.4923) | 0.466590 | +1.7e-07 | 1.806 |
| ESCOLARIDADXSEXO · HASTA-PRIMARIA×1 | 1086 | 0.4129 (0.3678, 0.4574) | 0.400590 (0.3684, 0.4333) | 0.400590 | -1.8e-07 | 1.233 |
| ESCOLARIDADXSEXO · HASTA-PRIMARIA×2 | 1213 | 0.3717 (0.3300, 0.4146) | 0.383167 (0.3515, 0.4164) | 0.383166 | +5.6e-08 | 1.150 |
| ESCOLARIDADXSEXO · SECUNDARIA×1 | 2040 | 0.5775 (0.5417, 0.6124) | 0.573479 (0.5462, 0.6005) | 0.573479 | +1.2e-07 | 0.399 |
| ESCOLARIDADXSEXO · SECUNDARIA×2 | 2176 | 0.5520 (0.5183, 0.5859) | 0.555505 (0.5286, 0.5829) | 0.555505 | +3.6e-07 | 0.352 |
| ESCOLARIDADXSEXO · MEDIA-SUPERIOR×1 | 2674 | 0.6922 (0.6652, 0.7190) | 0.686379 (0.6650, 0.7077) | 0.686379 | -2.5e-08 | 0.585 |
| ESCOLARIDADXSEXO · MEDIA-SUPERIOR×2 | 2908 | 0.6652 (0.6374, 0.6934) | 0.670428 (0.6480, 0.6927) | 0.670428 | +1.9e-07 | 0.521 |
| ESCOLARIDADXSEXO · SUPERIOR×1 | 4198 | 0.8004 (0.7793, 0.8206) | 0.818368 (0.8024, 0.8335) | 0.818367 | +3.8e-07 | 1.801 |
| ESCOLARIDADXSEXO · SUPERIOR×2 | 3908 | 0.8274 (0.8097, 0.8444) | 0.807245 (0.7919, 0.8223) | 0.807244 | +5.6e-07 | 2.014 |

## 6 · Registro, consumo y prueba de T-REPRO(g)

- **Celdas-D** (`GOB.gobierno_digital.encig2025.{edad_x_sexo,escolaridad_x_sexo}`): `champion_actual`
  sigue en **C2**; `adjudicacion_por_celda` ahora cita el -0002 (`…-ADJ2-…-C2-P`, IC `-C2-IC-LO/HI`);
  `margen_material` = MAE del -0002; `momentos_holdout_refs` = corrida del -0002. El bloque del -0001
  se conserva como `adjudicacion_por_celda_0001` (histórico; el marcador no lo lee) y la cabecera
  recibe un párrafo añadido. `candidatos` no se toca. No existe el campo `comparaciones_secundarias`
  en ninguna de las 21 celdas-D ni en ningún tool (`grep -rn` → 0): no hay nada que conservar ahí.
- **`decisiones.tsv`** (34 filas añadidas): `cuenta_gen2=SI` para los dos CALC (CONTADOR del encargo,
  verbatim); `origen_numerico=NUEVO` para los 16 `-C2-P` del piso y los 16 del -0002. La fila del -0002
  hace falta porque el resolvedor agrega **todo** el CALC citado: el piso declara `MIXTO` en 18 RESULT
  descriptivos (C2 nuevo − C2 legacy), que no alimentan el punto. Resolvedor después de las filas:
  32/32 `-C2-P` NUEVO, y los dos CALC con `cuenta_gen2=SI`. Las 16 filas HEREDADO del -0001 **se
  conservan** (siguen siendo verdad sobre el -0001).
- **Marcador re-derivado en el árbol** (`marcador_segmento.py --escribe` ×2, no commiteado; sha
  `8ab89bb2…53ba`): 16 filas citan el -0002 y 0 el -0001. `tests/check.py --baseline --parallel` con ese
  marcador: **T35 T-REPRO 0 FAIL** (sólo WARN). El único FAIL nuevo frente a la línea base fue
  T02 (esta nota colisionaba por nombre con el encargo); se renombró a `-cierre.md`.
- **Contadores:** `celdas_validadas` 219 → 219 (Δ0, `tools/celdas_validadas.py`); dos corridas
  selladas nuevas con `cuenta_gen2=SI`; adopciones de retadores: 0.
- **Firma asentada (A.12):** Decisión 1 de ADOPCION-2 → `FP-260924-GEN2-ENCIG-PISOS-GEN2-1-19a3-01`
  FIRMADA/EJECUTADA; `FP-…-e0db-01` y `FP-…-749c-01` quedan cerradas por ella (sustituye a S).

## 7 · Reservas declaradas

1. **C7 y C-ENCOGIDA siguen construidos sobre el C2 legacy** (son emisiones selladas del -0001, PROSPECTIVAS).
   Re-emitirlos después de R los volvería retrospectivos; la diferencia de su base es ≤ 5.6e-7. No se tocan.
2. **C2 del -0002 es RETROSPECTIVA**: el piso se selló después de que el -0001 derivó R (E.6, cruce visto).
   Su fórmula no tiene variante y no lee R; el rótulo va en `G-MARCA` del piso y en `G-MARCA-EMISIONES` del -0002.
3. **El resolvedor de linaje no ve números tecleados en `parametros`** (P1): es la causa de que DIN y TRA
   salgan NUEVO sin serlo. No se corrige aquí (`tools/corrida0.py` es motor, fuera de §9) → NC.
4. **El nombre del CALC del piso** no es el del «hecho» del encargo (`ENCIG2023-…`), por la respuesta 1 de mesa.

## 8 · Auditoría (afirma sobre México)

Contadores: dos corridas selladas, 0 adopciones, `celdas_validadas` sin cambio. **Escala:** proporciones de
**trámites** de pago de luz (N_TRA = 01), ENCIG 2025, ciudades de 100 mil habitantes o más; nada se
promedia con cifras por persona ni se extiende a lo rural. **Lectura:** el gradiente por escolaridad (0.38–0.82 en C2)
y por edad describe **acceso y oferta** (cuenta bancaria o tarjeta, conectividad, recibo a nombre propio) antes que
preferencia; el denominador es quien pagó, no quien pudo pagar. **PROSPECTIVA vs RETROSPECTIVA:** retadores
PROSPECTIVA; C2 del -0002 RETROSPECTIVA; ninguna frase las suma. **Cifra escrita a mano:** ninguna; todas salen
de `resultados.json` sellados, con el comando en esta nota.
