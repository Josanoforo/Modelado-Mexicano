# GEN2-VALIDACION-INDEPENDIENTE-2 — cierre

Encargo: `forense/encargos/2026-09-15-GEN2-VALIDACION-INDEPENDIENTE-2.md`
(archivado verbatim, 0-bis A.3). Entorno CAJA (Ubuntu/WSL2), corpus
compartido montado (`/home/pc0/mm-corpus/raw`), Sonnet ejecuta, Opus
supervisa (`feedback_subagentes_sonnet_yo_superviso`). Worktree
`/home/pc0/mm-gen2-validacion-independiente-2`, rama
`acto/gen2-validacion-independiente-2`, base `origin/main = 0cdbd72`
(merge de `PR #789`, `ACTO GEN2-MEDICION-DEMANDA-2`). El clon base
(`~/Modelado-Mexicano`) estaba parado en `censo/2026-09-11`, no en
`main` — verificado antes de confiar en su árbol de trabajo
(`feedback_verify_via_origin_not_worktree`); todo este acto lee y
escribe contra un worktree propio recién creado desde `origin/main`.

## §0 · E.2, verbatim

`instrucciones-proyecto-v2_13.md:446` — «Ningún número entra a GEN2 sin
cadena completa nacida con él… Tres preguntas distintas que nunca se
colapsan: ¿se reproduce? (automatizable: verify) · ¿pasó validación
independiente? (instrumentable; reservada a lo que puede cambiar signo,
tier, clasificación, marcador o coeficiente central) · ¿se adopta?
(humana, por merge de mesa).»

Este acto ejerce el segundo eje, exclusivamente. No adopta nada (tercer
eje) y no re-corre `verify` sobre las corridas selladas (primer eje, ya
hecho por sus actos de sellado).

## §1 · Las cuatro corridas y por qué son bin 2

Confirmado contra el árbol, no contra el encargo (los rótulos del
encargo no se toman por buena fe —
`feedback_encargo_premisa_se_verifica_contra_el_arbol`):

- **`CALC-EDER-0002`** (`familia.corresidencia.adulto_familiar_actual`
  con diseño, `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1`, `PR #766`). Cambia
  `coeficiente central` (el punto `A-P` es el sucesor propuesto de una
  regla con IC de diseño que antes no existía) y su hermana
  `CALC-EDER-0001` es exactamente la corrida que `NC-0183` cita para
  el cambio de tier MEDIA→FUERTE de `adulto_familiar` (misma familia,
  mismo lector, mismo método de varianza — el encargo nombra «EDER-0002»
  como abreviatura de la pieza del lote que hereda esa materialidad, no
  como el CALC que `NC-0183` cita literalmente; se declara la precisión
  aquí para no heredar la imprecisión del encargo).
- **`CALC-ENCIG-2023-0001-v1_1`** (`ACTO GEN2-MEDICION-DEMANDA-2`,
  `PR #789`). `RES-0007/RES-0008` de `tramite.mordida.con_registro` son
  hoy `ASIGNADO SIN CANAL` (`0.88/0.12`); esta corrida mide el mismo
  estimando **por canal** (presencial `B-P-PRE-SD`, digital
  `B-P-DIG-SD`) — releva directamente ese `ASIGNADO` si mesa adopta.
  Cambia clasificación/marcador (`ASIGNADO`→`MEDIDO`).
- **`CALC-ENVIPE-U4-2012-v1_1`** (`ACTO GEN2-LOTE-MEDICION-PENDIENTE-1`,
  `PR #766`). Cambia coeficiente central: primer IC de diseño para
  `U4` en 2012 (antes sin ruta declarada, `NC-0099`).
- **`CALC-ENIF-0003`** (`ACTO GEN2-LOTE-MEDICION-PENDIENTE-1`,
  `PR #766`). Cambia clasificación: adjudica H1 (¿qué cifra es
  `66.89 %`?) y acota `NC-0126` (P4_10=1) — ambos con consecuencia de
  mesa pendiente.

`CAJA-SUCESORES-1` (worktree hermano `/home/pc0/mm-gen2-caja-sucesores-1`,
en vuelo durante este acto, encargo `NC-0211/0215/0169/0208`) es quien
deriva el resto del bin 2; este acto no lo espera ni lo toca — perímetro
disjunto, ningún archivo compartido con su encargo.

## §2 · Método: control ciego por subagente aislado

`spec.yaml` de un CALC ya sellado **es parte de la identidad sellada**
(E.3: «spec.yaml forma parte de la identidad sellada»). Editarlo rompe
el sello — medido una vez ya en este mismo lote: `fcddf9a` revirtió un
intento de escribir `cuenta_gen2` directo en los 4 `spec.yaml` de
`FP-375` porque `T-CORRIDA0`/`T-REPRO` fallaban con `RESULT-SIN-SELLO`.
Este acto no repite ese error.

Para cada una de las cuatro corridas se lanzó un subagente Sonnet fresco
(sin el contexto de esta sesión — no forkeado, para preservar ceguera
real) en un worktree `isolation:worktree` propio, con instrucción
explícita de **no leer** `resultados.json` / `sello.json` /
`sello.sha256` / `ejecucion.json` / `medidor.py` del CALC objetivo ni
de sus hermanos/predecesores (`repite_de`), ni las notas de cierre del
acto que lo selló, ni grepear su id en `canon/gobernanza-v1_15.md`. Sí
se le permitió leer `spec.yaml`/`spec.md`/la spec sellada en
`forense/prereg-caja/` (el contrato congelado en COMMIT-1, que es lo
que hay que implementar, no el resultado) y el corpus crudo. Cada
subagente escribió su propio script desde cero (sin copiar ningún
script del repo) y reportó sus propios números; esta sesión —que sí
conocía los valores sellados de antemano, por ser quien compara— nunca
ejecutó ni guió el cómputo, solo lo encargó y lo auditó después. Esto
replica el patrón ya usado en el programa para «control positivo
externo» (`gobernanza-v1_15.md:7640`, control R-ENVIPE-SERIE: «este
acto no abrió `tools/arbitra.py` en ningún momento… dos implementaciones
escritas sin verse coinciden bit a bit»), aplicado aquí con aislamiento
de proceso en vez de solo disciplina declarada.

Los cuatro scripts quedan citados en
`forense/prereg-caja/validacion-independiente-caja2/`:
`EDER-0002-control.py`, `ENIF-0003-control.py`,
`ENVIPE-U4-2012-v1_1-control.py`, `ENCIG-2023-0001-v1_1-control.py`.

## §3 · Resultados, corrida por corrida

**`CALC-EDER-0002`** — ciego real (el blind nunca vio el sello). `A-P`
propio `0.0575307139` vs sellado `0.057530713852769505`, `Δ≈-1.5e-10`
— prácticamente al bit pese a bootstrap con semilla y réplicas propias
distintas. Todo el embudo estructural (94101/23831/16687/9397, split
jefe/cónyuge 9771/6916, `d=1/d=0` 522/8875, 289 estratos, 3150 UPM, 9
estratos de UPM única) coincide exacto. `B-P` (sensibilidad
`factor_per`) propio `0.0563744` vs sellado `0.05637443857402519`,
coincide. **PASA** en `A-P` y `B-P`.

**`CALC-ENIF-0003`** — ciego real. Las seis fracciones de cobertura
(`68.97/67.53/68.06` ponderada y no ponderada, universo triple
`66.89`/`65.50`) reproducen al 6º decimal en los cinco casos donde el
sellado también reproduce, y el subagente **encontró por su cuenta**
que `0.668937` NO reproduce al 6º decimal (Δ 7.3e-05) — el mismo
veredicto negativo `NO-REPRODUCE` que trae el sello, descubierto sin
haberlo visto. Los cuatro puntos de la cota P4 (dominio 1: `0.6356` vs
`0.635576…`; dominio 2: `0.3771` vs `0.377147…`) coinciden a 4 cifras;
todos los conteos (4275/2443/3405/1328/1479/74/498, 4973/3969, etc.)
exactos. **PASA** en `C-VEREDICTO-H1`, `C-VEREDICTO-0-668937`,
`C-VEREDICTO-66-89`, `D-P-NINGUNA-VIA-EN-1`, `D-P-NINGUNA-VIA-EN-2`.

**`CALC-ENVIPE-U4-2012-v1_1`** — parcialmente ciego, y el propio
subagente lo declaró antes de reportar números: `spec.yaml` disclosa el
punto `P-C2-U4` de v1.0 como control esperado (v1.1 solo cambia la
fuente del par `EST/UPM` para el IC, el punto es el mismo por diseño) —
así que `P-C2-U4` **no** se marca como validado a ciegas aquí (coincidió
exacto, pero no era un blanco ciego). Lo genuinamente nuevo — cuántos
estratos/UPM cubre el diseño de `Tmod_Vic` (355/6486/44 con UPM única)
y el IC bajo ese diseño — sí era desconocido al arrancar el subagente,
y coincide exacto en los tres conteos y casi exacto en el IC de Taylor
(`[0.321187,0.355606]` propio vs `[0.3211872…,0.3556064…]` sellado). El
IC bootstrap difiere más (`[0.32259,0.35480]` propio vs
`[0.322115,0.355328]` sellado) — esperado: dos bootstraps
independientes con semilla propia nunca coinciden al bit, y el
precedente del programa ya declara esto fuera del alcance de la
validación («eso es validación independiente del punto — no del EE»,
`gobernanza-v1_15.md:7640`). **PASA** en `N-ESTRATOS`, `N-UPM`,
`N-ESTRATOS-UPM-UNICA`, `IC-LO-TAYLOR-C2-U4`, `IC-HI-TAYLOR-C2-U4`.
`P-C2-U4` y el IC bootstrap quedan `NO-HECHA` — no porque hayan fallado,
sino porque el diseño de este control no probó ninguno de los dos a
ciegas.

**`CALC-ENCIG-2023-0001-v1_1`** — ciego real. `B-P-PRE-SD`
`0.13079648341932204` y `B-P-DIG-SD` `0.02340709180348316`: **idénticos
al bit** contra el sello, con `n` (10852/6005), estratos (299/286), UPM
(2797/2288) y UPM-única (50/51) también idénticos. `H1-VEREDICTO`
(`H1-SOSTENIDA`) y `B-VEREDICTO-CANAL`
(`DICOTOMIA-ES-PROPIEDAD-DEL-RECORTE`) coinciden. **Discrepancia real,
declarada y no adoptada**: la rama secundaria/no-adoptable CD
(deduplicada) no coincide — sellado `B-N-PRE-CD=9680`/
`B-N-DIG-CD=5259`/`B-N-EVENTOS-DESCARTADOS-POR-DEDUP=1918` vs propio
`9649`/`5253`/`3577` — el criterio de qué fila conservar entre
duplicados de `ID_TRA` no está fijado por la spec y las dos
implementaciones lo resolvieron distinto. Como la propia spec declara
la rama CD «SECUNDARIOS DECLARADOS, NO adoptables… existe solo para
comparabilidad», esta discrepancia no toca ningún RESULT marcado
`PASA` aquí, pero queda como hallazgo para quien in the futuro fije la
regla de deduplicación de `ID_TRA` con `NT_TIPO`. **PASA** en
`B-P-PRE-SD`, `B-P-DIG-SD`, `H1-VEREDICTO`, `B-VEREDICTO-CANAL`.

## §4 · El aparato no tenía cómo registrar esto sin romper el sello

`tools/corrida0.py` ya resolvía `cuenta_gen2` con precedencia de
`decisiones.tsv` sobre la etiqueta del spec (`_cuenta_gen2_resuelto`,
precisamente el remedio que `fcddf9a` introdujo tras revertir la
edición directa de `spec.yaml`), pero `validacion_independiente` seguía
leyéndose solo de `_etiqueta(spec, "validacion_independiente", …)` —
sin ruta de decisión, es decir: sin forma de registrar una validación
post-sello sin repetir el mismo error que `fcddf9a` ya corrigió para
`cuenta_gen2`. Se añadió `_validacion_independiente_resuelta(calc_id,
rid, spec, decisiones)`, mismo patrón, con una diferencia deliberada:
precedencia **por RESULT** (objeto `<calc_id>:<rid>` en
`decisiones.tsv`), no por CALC entero — E.2 reserva la validación a los
RESULT materiales, no a cada fila diagnóstica (`G-`/conteos) de la
corrida, y marcar `PASA` a nivel de CALC completo cuando solo se
re-derivó el punto primario sería sobre-declarar cobertura
(`feedback_declare_more_not_less` corre en ambas direcciones: ni menos
de lo verificado, ni más). Las columnas `validacion_ref` y
`alcance_validacion` de `resultados.tsv` ya existían en el esquema
(vacías, `NO-DECLARADO-EN-EL-REGISTRO`) — se conectaron a los mismos
campos `ref=`/`alcance=` de la decisión, no se inventó esquema nuevo.

`data/corrida0/decisiones.tsv` recibe 16 filas nuevas, objeto
`<calc_id>:<RESULT-id>`, decisión
`validacion_independiente=PASA·ref=<script>·alcance=<qué exactamente>·<delta>`,
fuente citando este acto y la disciplina de ceguera seguida. Ningún
`spec.yaml` sellado se tocó. `tests/check.py --baseline` sigue VERDE
(3 FAIL preexistentes T06/T08, sin novedad) antes y después de la
edición de `tools/corrida0.py` y de las 16 filas.

## §5 · Contador

`corrida0.py status` (dry-run, `registro` sin `--escribe`, sin tocar
ningún TSV): `resultados_con_validacion_independiente` **199 → 215**
(+16, exactamente las filas citadas arriba). `N_corridas_selladas`
confirmado en **80** (coincide con la premisa del encargo: 63→80 desde
el transfer). Ningún otro contador se mueve — no se corrió `--verifica`
sobre ninguna corrida ajena, no se tocó `milpa/`, no se adoptó nada.

**PENDIENTE, no ejecutado por esta sesión**: `corrida0.py registro
--escribe` (materializar `corridas.tsv`/`resultados.tsv`/`usos.tsv`
desde `decisiones.tsv` — el paso que en este mismo lote ya se describe
como «sin esto el 207 no baja aunque se firme todo», `NC-0211` del
encargo hermano de `CAJA-SUCESORES-1`) fue bloqueado por el
clasificador de modo automático de esta sesión («Modify Shared
Resources»). El dry-run (`registro` sin `--escribe`) confirma que el
diff es exactamente las 16 filas de `validacion_independiente`/
`validacion_ref`/`alcance_validacion` y nada más — no hay transición de
`resultado_replay`/`contexto_replay` pendiente que `--lote` necesite
cubrir. Queda para que el usuario autorice el paso o para el sucesor
que corra con permiso de escritura sobre las tres vistas derivadas.

## Qué NO hace este acto

No adopta ningún RESULT a `milpa/` — el tercer eje de E.2 sigue humano.
No re-corre `verify` sobre ninguna corrida sellada (primer eje, ya
resuelto). No toca `CAJA-SUCESORES-1` ni su worktree. No marca `PASA`
ningún RESULT que el control ciego no haya reportado con número propio
comparado — específicamente, no marca `P-C2-U4` de `ENVIPE-U4-2012-v1_1`
(conocido de antemano, no ciego) ni la rama CD de `ENCIG-2023` (no
coincidió). No corrige la discrepancia CD — se declara, no se resuelve
aquí. No relanza `registro --escribe` sin autorización.
