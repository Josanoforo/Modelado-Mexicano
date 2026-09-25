# Informe del programa · v1.3 — Benchmark del Mexicano

**Modelado Mexicano — «Psicología del Mexicano Contemporáneo».**
Documento del programa, escrito para mesa y para un comprador escéptico.
24 de septiembre de 2026.

### `informe-programa` · **v1.3** · DOCUMENTO DEL PROGRAMA

> | | |
> |---|---|
> | **ARCHIVO** | `informe-programa-v1_3.md` |
> | **CONVIVE CON** | `informe-programa-v1_2.md` (22/sep/2026), que **no se edita ni se retira** — `informe-programa` no está en el universo de T01 (`modelo`, `glosario`, `gobernanza`, `estado`; verificado <!-- comando: python3 -c "import sys; sys.path.insert(0,'tests'); import check; check.t01_single_source(); print('FAILS_T01:', len(check.FAILS))" -->), así que v1.2 sigue viva como historia (E.1). v1.3 reencuadra el programa como **benchmark auditable** (firma D2, §2) y cierra la etapa de retadores; no reabre ningún veredicto de v1.2. |
> | **VERIFICAS ASÍ** | cada cifra de este documento trae, en su propia línea, un comentario HTML con el prefijo `comando:` seguido del comando que la reproduce, que se re-ejecuta contra el árbol (mismo patrón que `canon/estado-programa-v1_16.md`, verificado por `tests/test_estado_derivado.py`) o cita un `RESULT-*` sellado ya extraído a `forense/analisis/informe-v1_3/comparaciones-primarias.tsv`. `tests/test_informe_derivado.py` re-corre los primeros. |
> | **NOMBRE ESTABLE** | **`informe-programa`** — cítalo así, **nunca por nombre de archivo**; la versión vigente en este corte es v1.3 |

> **Estampa de universo (A.10), global.** Derivado contra `origin/main = 8358b891`
> (el mismo commit que este acto declaró al abrir, re-verificado: `git rev-list
> --count HEAD..origin/main` = 0 al 0-bis). Acto de **NUBE sin corpus montado**
> (`python3 tools/entorno.py`: `acceso_corpus.montado=NO`,
> `acceso_corpus.archivos_examinados=0`, `red=DENEGADA-POR-POLITICA`).
> **Fuentes: sólo el registro derivado y las corridas selladas que ya viven en
> el repo.** Este documento no abre microdato, no llama a ningún modelo, no
> sella ninguna corrida y **no adjudica nada** — lee lo que otros actos ya
> sellaron y lo compone.
>
> **Lo que este documento NO es.** No es SALIDA para cliente: es su insumo. No
> re-abre ningún veredicto: los de v1.2 siguen vigentes (lote ENIF 2024
> `PROPUESTA-CON-RESERVA`; piloto 3 `FALSADOR-DEBIL`, `champion_actual: C2`
> desde firma F3); los de las seis evaluaciones de la etapa de retadores
> (abajo) siguen siendo los que sus propios CALC sellaron. No adopta ningún
> candidato. No publica en Zenodo — esa receta queda para mesa (§5).

---

## 0 · En una página

Este programa mide, con el microdato oficial, cómo se comporta el mexicano
por segmento, y prueba sus propias predicciones antes de que INEGI publique
la siguiente ola. En **6** evaluaciones prospectivas selladas
<!-- comando: python3 forense/analisis/informe-v1_3/censo_evaluaciones.py --clave n_evaluaciones -->,
sobre **4** instrumentos (ENCIG, ENIF, ENIGH, ENVIPE)
<!-- comando: python3 forense/analisis/informe-v1_3/censo_evaluaciones.py --clave instrumentos -->
y **137** celdas de cruce
<!-- comando: python3 forense/analisis/informe-v1_3/censo_evaluaciones.py --clave n_celdas_total -->
(más el punto nacional del duelo ENIGH 2024, que no es una celda de cruce),
la predicción más simple —lo que la gente dijo en la ola anterior— nunca fue
vencida con intervalo que despejara el umbral por ninguno de los **6**
retadores construidos en la casa (encogida, tendencia, C1/C7, suavizados, AP,
θ sin emitir) ni por el retador externo (Astra, familia C-ASTRA) en ENCIG
2025 <!-- comando: grep -n "Siete familias de retador" canon/estado-programa-v1_16.md -->.
Una sola propuesta con reserva (crédito K1, tendencia de serie, ΔMAE +1.90
pp, IC95 [0.62, 2.65] pp) con umbral inalcanzable por diseño
(`umbral_vence_pp: inf` en la spec del CALC que la adjudica)
<!-- comando: grep -n "umbral_vence_pp: inf" canon/informe-programa-v1_3-ANEXO.md -->.
Ese resultado no es un fracaso del modelado: es el hallazgo. El comportamiento
reportado del mexicano es estable entre olas en los dominios medidos, y
cualquier producto que prometa detectar cambios grandes de conducta entre
encuestas debería probarse contra esta línea base antes de venderse. Por eso
el producto se llama Benchmark del Mexicano y no gemelo digital.

**`VENCE` puro: 0 de 18 dictámenes de celda-D**
<!-- comando: grep -h "^  veredicto:" data/curacion-registro/celdas-d/*.yaml | sed -E 's/ *#.*//; s/^  veredicto: *//' | sort | uniq -c -->
(5 `NADIE-VENCE` · 2 `NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO` · 2
`PROPUESTA-CON-RESERVA` · 6 `FALSADOR-DEBIL` · 3 `SIN-CANDIDATO-SUPERIOR`; 3 de
las 21 celdas-D no traen campo `veredicto` — anteriores al vocabulario de
retadores). La regla de salida de θ (`FP-…-8a1f-06`: si ni el piloto 3, ni la
familia R2 del lote ENIF 2024, ni los cruces de ENVIPE 2026 vencen con un
retador con interacción, se retiran `g()` y `Theta.valor`) tiene sus **tres**
condiciones satisfechas — piloto 3: ningún retador con interacción venció;
lote ENIF 2024 R2: retador no adjudicado, cuenta como «no venció»; ENVIPE
2026 (marginal `civico.denuncia.con_seguro`): `NO-CONSTRUIBLE`, fila no
ocupada, que por el aparato «no cuenta como derrota»
<!-- comando: grep -n "8a1f-06" forense/firmas-pendientes.tsv -->.
**El retiro de código de `g()`/`Theta.valor` no ha corrido** — es una decisión
estratégica de mesa, no la ejecución mecánica de la firma; sucesor: el acto
que cierre `FP-…-8a1f-06`.

**Contadores que movió el trabajo que produjo este informe** (v2.16 del
módulo de auditoría): **cero**. Este acto no adopta, no sella ninguna
corrida y no escribe `data/corrida0/marcador-segmento.tsv`; sólo lee. Los
contadores citados abajo (`celdas_validadas=219`, `celdas_d_adoptadas_activas
=17`, `N_corridas_selladas=246`) son los que ya estaban en `origin/main` al
abrir este acto <!-- comando: python3 tools/corrida0.py status | rg "^(celdas_validadas|N_corridas_selladas)=" -->.

---

## 1 · El marcador, con la etapa de retadores cerrada

### 1.1 · Dos vistas del marcador que no se funden: la comprometida y la de hoy

`data/corrida0/marcador-segmento.tsv`, tal como vive **commiteado** en
`origin/main`, trae **214** filas
<!-- comando: tail -n +2 data/corrida0/marcador-segmento.tsv | wc -l -->,
la misma cifra que v1.1/v1.2 citaban: **20 PROSPECTIVA · 59 RETROSPECTIVA ·
89 IDENTICO-EMISOR-ES-ARBITRO · 16 EMITIDA-SIN-R · 30 SIN-EMISION**
(heredado v1.2 §1.1, sin cambio en el archivo commiteado).

Corriendo `python3 tools/marcador_segmento.py --json` **sin** `--escribe`
(modo de sólo lectura; verificado que no toca el árbol:
`git status --porcelain` vacío antes y después) sobre el mismo `origin/main`,
el derivador proyecta **243** filas, no 214: **20 PROSPECTIVA · 75
RETROSPECTIVA · 89 IDENTICO-EMISOR-ES-ARBITRO · 29 EMITIDA-SIN-R · 30
SIN-EMISION**, con `ADOPTADO-POR-FIRMA` en **52** filas de cruce y **15**
filas de marginal (ENVIPE, sin cambio) y `sin_piso` sin cambio en **15**
<!-- comando: python3 tools/marcador_segmento.py --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['total_filas'], d['sin_piso'], d['estimador_adoptado'])" -->.
La diferencia (214→243, +29 filas) es el efecto acumulado de las celdas-D
adoptadas entre el 22 y el 24/sep (el lote de crédito ENIF 2024 con
`champion_actual: PERSISTENCIA`, entre otras — `celdas_d_adoptadas_activas`
pasó de 6 a 17 en el mismo lapso, §1.2). **Esta proyección no está
commiteada**: como en v1.2, se declara aquí «en árbol, no en el canal» hasta
que un acto de aparato corra `--escribe` y lo publique — ningún número de
`marcador-segmento.tsv` se edita a mano desde este informe (candado E.5: lo
sellado se cita, no se re-mide; lo no sellado se proyecta y se declara así).

### 1.2 · `celdas_validadas` y `celdas_d_adoptadas_activas`, re-derivados hoy

**`celdas_validadas` = 219**, no 92 como citaba v1.2 (22/sep)
<!-- comando: python3 tools/corrida0.py status | rg '^celdas_validadas=' -->.
El salto 92→219 **no ocurrió por trabajo de esta sesión ni de ayer**: es un
cambio de **definición** de la métrica —crédito por conducta agregada +
sufijo `-D-C2` de ENCIG 2025— fusionado el 23/sep por `PR #1086`
(`tools/celdas_validadas.py::DEFINICION_DESDE = "38dd709"`)
<!-- comando: python3 tools/corrida0.py status | rg '^celdas_validadas_definicion_desde=' -->.
**Corrección de premisa** (este acto, no el encargo): el encargo de dirección
citaba «definición vigente desde commit de #1078»; ese PR
(`GEN2-TRAMITE-FIRMAS-12`, rescate de su ADENDA-1) no toca
`tools/celdas_validadas.py` — cero menciones en su historia de archivo
<!-- comando: git log --oneline -- tools/celdas_validadas.py | { grep -ci "firmas-12" || true; } -->.
El commit real es `38dd709` (`PR #1086`, `ACTO GEN2-CONTADORES-CONSUMO-1`)
<!-- comando: git log --oneline -- tools/celdas_validadas.py | grep -c 38dd709 -->
<!-- comando: git log --merges --oneline | grep -E "^[0-9a-f]+ Merge pull request #1086 " | wc -l -->.
La misma confusión #1078/#1086 ya había sido corregida una vez antes, para
otra fila, por `GEN2-TRAMITE-FIRMAS-14` (23/sep) — no es un hallazgo nuevo de
esta sesión, es una cita recurrente de dirección que este acto vuelve a
corregir. De los 219: **20 PROSPECTIVA · 59 RETROSPECTIVA**, reportadas
aparte y nunca fundidas (firma P, §2)
<!-- comando: python3 tools/corrida0.py status | rg '^celdas_validadas_(prospectiva|retrospectiva)=' -->.

**`celdas_d_adoptadas_activas` = 17 de 21**, no 6 como citaba v1.2
<!-- comando: python3 tools/tablero_programa.py | rg 'celdas_d_adoptadas_activas' -->,
por instrumento: **ENIF (DIN) 10 · ENCIG (GOB) 3 · ENVIPE (TRA) 1**, más
**3** fuera de esas tres encuestas (`G5.*`, baseline ENASIC/ENCUCI, dominio
cultura/tiempo/capital social, no confecciones con ENIF/ENCIG/ENVIPE)
<!-- comando: python3 -c "
import sys; sys.path.insert(0,'tools')
import tablero_programa as TP
r = TP._celdas_d_adoptadas_activas()
from collections import Counter
print(Counter(d['celda_d'].split('.')[0] for d in r['detalle']))
" -->.
Las **4** celdas-D sin adoptar son las cuatro `TRA.evade_norma.envipe2025.*`
de piloto 4 con `champion_actual: NINGUNO` (dominio×sexo, edad×escolaridad
proxy, edad×sexo, escolaridad proxy×sexo — «Piloto 4 ENVIPE 2025», §2 abajo)
<!-- comando: grep -l "champion_actual: NINGUNO" data/curacion-registro/celdas-d/TRA.evade_norma.envipe2025.*.yaml | wc -l -->.
**Nota de vocabulario (hallazgo de esta sesión, para que no se repita):**
`legacy_activas_por_consumidor__celdas_D` (un contador de `corrida0.py
status`, hoy en **6**) cuenta dependencias numéricas legacy activas de las
celdas-D, no adopciones — es un contador distinto de
`celdas_d_adoptadas_activas`; que ambos coincidieran en «6» el 22/sep fue
casualidad de fecha, no identidad de definición
<!-- comando: python3 tools/corrida0.py status | rg '^legacy_activas_por_consumidor__celdas_D=' -->.

Heredado de v1.2 §1.2, sin cambio (se cita, no se re-mide): `SIN-PISO-POR-
DISEÑO` sigue distinguiendo ENUT 2024 (11 filas, `CAMBIO-DE-INSTRUMENTO`) y
EDER 2017 (4 filas, cohorte re-observada) del resto de `sin_piso`; el cruce
`reparto_hogar × sexo_edad` de ENUT sigue `RESERVADA`; las celdas hermanas
del núcleo común de ENUT siguen sin CALC sellado
(`NC-260921-GEN2-ENUT-PISOS-Y-SERIE-1-308c-01`, ABIERTA).

---

## 2 · Cobertura por candidato — pilotos, lote, marginales y las seis
evaluaciones de la etapa cerrada

**Intervalo binomial: Wilson (score), z = 1.959964** — heredado de v1.1/v1.2,
sin `scipy` en este entorno de nube.

> **ADVERTENCIA QUE VIAJA CON TODO INTERVALO DE ABAJO (heredada).** Las
> celdas de una misma ola comparten marco muestral, estratos, UPM y réplicas
> de bootstrap. **No son ensayos independientes.** Todos estos intervalos son
> demasiado angostos.

### Los tres pilotos y el lote ENIF 2024 (heredado v1.2 §2.1–§2.2, sin
cambio — se citan, no se re-miden)

| piso C2 | cobertura | Wilson 95% |
|---|---:|---|
| piloto 1 · ENIF 2024, persona | 7/8 | [0.529, 0.978] |
| piloto 2 · ENVIPE 2025, delito | 11/12 | [0.646, 0.985] |
| piloto 3 · ENCIG 2025, trámite | 8/15 | [0.301, 0.752] |
| **los tres** | **26/35 = 0.743** | **[0.579, 0.858]** |

Celda-D del piloto 3: `GOB.gobierno_digital.encig2025.edad_x_escolaridad`
(nota de cierre: `forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md`)
<!-- comando: ls forense/notas/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-2-3-v1_3-cierre.md -->.
Lote ENIF 2024 (14 cruces, 44 celdas puntuadas de 96): `C2` MAE 1.8729 pp,
cobertura 75.0%; `R2` (interacción histórica encogida) MAE 1.3931 pp,
cobertura 88.6%. **Comparación primaria: `ΔMAE(C2−R2) = 0.4798 pp, IC95
[0.0975, 0.7151]`** — despeja 0 pero no el umbral de 0.5 pp ⇒
`VEREDICTO-PRIMARIO = PROPUESTA-CON-RESERVA`. B-bis: `NO-CAE-EN-NINGUNA-FILA`
(cobertura de `C2` < 80% en un par primario). Detalle completo: v1.2 §2.2,
sin cambio.

Crédito 2021→2024, backtest de persistencia: persistencia gana en 7 de 9
marginales (`PR #987`, heredado v1.2 §2.3). Marginales, persistencia t−1:
14/57 = 25% (ENIF 6/32 · ENVIPE 8/15 · ENCIG 0/10; heredado v1.2 §2.4).

### Duelo ENIGH 2024 (hogar; punto nacional, sin cruce adjudicable —
PROSPECTIVA)

`CALC-ENIGH-DUELO-ADJUDICACION-0001`. Error absoluto: `C-PISO` 0.622 pp,
`C-TS` 0.441 pp (`RESULT-ENIGHADJ-CPISO-ABS-ERROR-PP`,
`RESULT-ENIGHADJ-CTS-ABS-ERROR-PP`)
<!-- comando: grep -n "RESULT-ENIGHADJ-CPISO-ABS-ERROR-PP" canon/informe-programa-v1_3-ANEXO.md -->.
`C-TS` gana el punto pero no la condición retrospectiva: B-bis-1
`CORROBORADA`, B-bis-2 `ACOTADA`, B-bis-3/4 `FALSADOR-DEBIL`. No hay IC de
ΔMAE para este punto — es una comparación de un solo punto nacional, unidad
**hogar**, no se promedia con ninguna cifra por persona, delito o trámite de
las demás filas de esta tabla. **Sin celda-D**: esta evaluación no tiene
objeto en `data/curacion-registro/celdas-d/` (es un punto nacional, no un
cruce con universo de celda) — verificado, 0 coincidencias
<!-- comando: { grep -l "envipe2026\|ENIGH\|civico" data/curacion-registro/celdas-d/*.yaml || true; } | wc -l -->.
Nota de cierre: `forense/notas/2026-09-22-GEN2-ENIGH2024-DUELO-COMMIT-2-3-cierre.md`
<!-- comando: ls forense/notas/2026-09-22-GEN2-ENIGH2024-DUELO-COMMIT-2-3-cierre.md -->.

### Duelo ENVIPE 2026 (delito; 12 celdas SXD y 12 EXD — PROSPECTIVA)

`CALC-DUELO-ENVIPE2026-ADJUDICACION-0001`. SL: SXD ΔMAE −0.431 pp [−0.910,
0.360]; EXD ΔMAE +0.361 pp [−0.405, 0.773]
<!-- comando: grep -n "RESULT-DUELO26-ADJ-SXD-SL-DELTA-MAE-PP" forense/analisis/informe-v1_3/comparaciones-primarias.tsv -->.
**`NADIE-VENCE` en ambos cruces** — los dos IC cruzan cero. Las emisiones
ASTRA de esta ola quedan selladas pero sin adjudicación por decisión de
mesa; no se añaden como candidato adoptable. **Sin celda-D**: ola nueva sin
objeto todavía en `data/curacion-registro/celdas-d/`
<!-- comando: { grep -l "envipe2026\|ENIGH\|civico" data/curacion-registro/celdas-d/*.yaml || true; } | wc -l -->.
Notas de cierre: `forense/notas/2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1-cierre.md`
y `forense/notas/2026-09-23-GEN2-DUELO-ENVIPE2026-MARGINALES-2-cierre.md`
<!-- comando: ls forense/notas/2026-09-22-GEN2-DUELO-ENVIPE2026-EJECUCION-1-cierre.md forense/notas/2026-09-23-GEN2-DUELO-ENVIPE2026-MARGINALES-2-cierre.md -->.

### Piloto 4 ENVIPE 2025 (delito; 4 cruces, 38 celdas puntuadas —
PROSPECTIVA)

`CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001`. C-ENCOGIDA frente
a C2, ΔMAE [IC95] pp:

| cruce | ΔMAE (pp) | IC95 | B-bis |
|---|---:|---|---|
| dominio × sexo | 0.307 | [−0.773, 0.946] | FALSADOR-DEBIL |
| edad × escolaridad (proxy) | 0.351 | [−0.067, 0.520] | FALSADOR-DEBIL |
| edad × sexo | 0.104 | [−0.309, 0.335] | FALSADOR-DEBIL |
| escolaridad (proxy) × sexo | 0.439 | [−0.197, 0.524] | FALSADOR-DEBIL |

<!-- comando: grep -n "RESULT-TRA-ENCOGIDA-ARB-DOMxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-PP" forense/analisis/informe-v1_3/comparaciones-primarias.tsv -->

Cuatro IC cruzan cero. `champion_actual` sigue `NINGUNO` en las cuatro
celdas-D de este piloto — `TRA.evade_norma.envipe2025.dominio_x_sexo`,
`.edad_x_escolaridad_proxy`, `.edad_x_sexo`, `.escolaridad_proxy_x_sexo`
(§1.2) <!-- comando: grep -l "champion_actual: NINGUNO" data/curacion-registro/celdas-d/TRA.evade_norma.envipe2025.*.yaml | wc -l -->:
un piso no vencido que no se adopta porque mesa no ha resuelto la reserva de
este grupo, no porque el piso haya perdido. La lectura es prospectiva
respecto de R: emisiones COMMIT-2, R COMMIT-3. Nota de cierre:
`forense/notas/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-cierre.md`
<!-- comando: ls forense/notas/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-cierre.md -->.

### Cierre ENCIG 2025 (trámite; 2 cruces de 8 celdas — PROSPECTIVA;
piso re-adjudicado por `PR #1116`)

`CALC-ENCIG-DUELO-2025-ADJUDICACION-0002` (re-adjudicación del `-0001` con
piso `C2` re-medido desde microdato ENCIG 2025 en vez de marginales legacy
tecleados — §3.5). C-ASTRA frente a C2:

| cruce | ΔMAE (pp) | IC95 | B-bis | champion propuesto |
|---|---:|---|---|---|
| edad × sexo | 0.1912 | [−0.2658, 0.4799] | FALSADOR-DEBIL | C2 |
| escolaridad × sexo | −0.3455 | [−0.3663, 0.3180] | CORROBORADA → SIN-CANDIDATO-SUPERIOR | C2 |

<!-- comando: grep -n "GOB.gobierno_digital.encig2025.edad_x_sexo" data/curacion-registro/celdas-d/GOB.gobierno_digital.encig2025.edad_x_sexo.yaml | head -1 -->

**Agregado: `FALSADOR-DEBIL`** (idéntico al `-0001`: el mayor cambio numérico
frente al piso legacy es 5.56e-5 pp; ningún veredicto cambió — §3.5). Ninguno
de los dos cruces despeja cero ni el umbral de 0.5 pp. Celdas-D:
`GOB.gobierno_digital.encig2025.edad_x_sexo` y `.escolaridad_x_sexo`.
Notas de cierre: `forense/notas/2026-09-23-GEN2-DUELO-ENCIG2025-CIERRE-1-cierre.md`
(adjudicación `-0001`) y `forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-cierre.md`
(piso re-medido, `-0002`, §3.5)
<!-- comando: ls forense/notas/2026-09-23-GEN2-DUELO-ENCIG2025-CIERRE-1-cierre.md forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-cierre.md -->.

### Lectura que NO se debe hacer (heredada de v1.2 §3d, extendida)

Ninguna de las seis evaluaciones de esta sección produjo un `VENCE` puro
(§0). «El retador X mejoró el MAE» sin la etiqueta `NADIE-VENCE` /
`FALSADOR-DEBIL` / `PROPUESTA-CON-RESERVA` de su propia fila es la lectura
que este informe prohíbe explícitamente. Los signos de ΔMAE de esta tabla
siguen la convención `MAE(piso) − MAE(candidato)`: positivo favorece al
candidato, y aun así ningún candidato de las cuatro evaluaciones nuevas de
esta sección (ENIGH, ENVIPE 2026, piloto 4, cierre ENCIG) fue adoptado.

---

## 2.5 · Corroboración externa

Dos estudios independientes, en otros países y con otros instrumentos,
encuentran lo mismo: contra el Korea Media Panel Survey, la ola previa erró
**3.7** pp donde el sintético calibrado erró **7.0–7.5** pp (arXiv
2608.28615); contra la verdad por celda, recitar la tabla nacional (**4.85**
pp) venció a los contratos de simulación (arXiv 2609.07305)
<!-- comando: grep -n "persistir la ola previa 3.7 pp" canon/informe-programa-v1_3-ANEXO.md -->
<!-- comando: grep -n "recitar la tabla nacional 4.85 pp" canon/informe-programa-v1_3-ANEXO.md -->.
[literatura]; no se promedian con nuestras cifras — son instrumentos, países
y unidades de medición distintos (proporciones de uso de servicios digitales
en Corea; opciones de encuesta en tres países, no delitos, hogares ni
trámites mexicanos).

El informe de competencia que sustenta el mapa de oferta de esta sección está
archivado en `forense/encargos/fuentes/INFORME-COMPETENCIA-2026-09-23.md`
(SHA-256 `acbaa795…`, cotejado en `origin/main` vivo el 23/sep/2026 por
`FIRMAS-13`); revisa 33 filas y deja 30 proveedores `PEND` — sus negativos
son «no encontrado en lo buscado», no prueba de inexistencia en México.
Dónde ganan los otros: preguntas arbitrarias en minutos (YouGov Parallax,
Toluna), compras observadas (Worldpanel), granularidad de manzana (Matria).
Los números de escala que estos proveedores anuncian son afirmaciones
propias, no verificación independiente de desempeño predictivo — este
informe no los adopta ni los refuta, sólo los cita.

---

## 3 · Qué enseñaron el lote, ENCIG, crédito y las cuatro evaluaciones
nuevas

**(a) El piso simple aguanta más de lo que el piloto 3 solo sugería**
(heredado v1.2 §3a, sin cambio): en el lote, `C2` (1.87 pp) sigue siendo el
punto de referencia; en crédito, la persistencia gana 7 de 9 sin que un
retador entre a competir.

**(b) La interacción encogida es señal repetida y sigue sin adjudicar**
(heredado v1.2 §3b): `S-LAMBDA` del piloto 3 y `R2` del lote son la misma
forma de resultado dos veces — mejora medida, IC que no toca cero, criterio
de victoria no satisfecho.

**(c) Nadie explica los saltos de nivel** (heredado v1.2 §3c, `SALTO-SIN-
EXPLICAR` de ENCIG, sin cambio).

**(d) Las cuatro evaluaciones nuevas repiten el mismo patrón, en instrumentos
y unidades distintas.** ENIGH (hogar, punto nacional): el retador gana el
punto pero no la condición retrospectiva — `FALSADOR-DEBIL` en dos de
cuatro B-bis. ENVIPE 2026 (delito, ola nueva completa): `NADIE-VENCE` en los
dos cruces, IC que cruzan cero por ambos lados. Piloto 4 ENVIPE 2025 (delito,
cuatro cruces): cuatro IC cruzan cero, `FALSADOR-DEBIL` en las cuatro.
Cierre ENCIG 2025 (trámite, piso re-medido desde microdato por `PR #1116`,
§3.5): `FALSADOR-DEBIL` agregado, sin que el origen nuevo del piso cambie el
veredicto. **Cero `VENCE` puro en seis evaluaciones, cuatro instrumentos, 137
celdas de cruce** (§0).

**(e) Lectura que NO se debe hacer** (heredada v1.2 §3d, extendida a las
cuatro evaluaciones nuevas, §2.6).

---

## 3.5 · De dónde venían los pisos

El censo de `PR #1116` encontró que **4 de 5** celdas-D consumidas por el
marcador como piso `C2` tenían ese piso armado con marginales **tecleados**
en `milpa/tramite-ola5-propuesta-v0.yaml` (nacional de `milpa/tramite.yaml`),
no derivados de su `inputs` declarado
<!-- comando: rg -F "4 de 5" forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-cierre.md -->.
La tesis sobrevive —el piso ganó aunque estuviera peor especificado—, pero
ningún estimador adoptable puede tener esa cadena: el acto `PISOS-GEN2-2`
re-mide cada piso legacy desde microdato y re-adjudica con sucesores; este
informe reporta la tabla «pisos por origen» antes y, cuando cierre, después.

**Tabla «pisos por origen», las 5 celdas-D que el marcador consume como
`C2`** (fuente: `forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-censo.tsv`,
52 filas, una por RESULT consumido):

| celda-D | RESULT `C2` | CALC que emite el punto | clase del censo | por dónde pasa la cadena |
|---|---:|---|---|---|
| `DIN.ahorro_solo_informal.enif2024.localidad_x_edad` | 8 | `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` | **HEREDADO-DE-LEGACY** | `parametros.marginales_sellados_D9` de `milpa/tramite-ola5-propuesta-v0.yaml`; control contra el árbitro: **NO-REPRODUCE** (Δ 1.20e-3) |
| `GOB.gobierno_digital.encig2025.edad_x_escolaridad` (piloto 3) | 16 | `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` | **NUEVO** | compone `C2` desde marginales de microdato ENCIG 2025; el `C2` compuesto legacy queda sólo como control |
| `GOB.gobierno_digital.encig2025.edad_x_sexo` | 8 | `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001/-0002` | **HEREDADO-DE-LEGACY → releva­do por este acto** | `medidor.py:639` ← emisiones ← `CALC-C2-COMPUESTO-RESERVADAS-0001` ← `milpa/`; re-medido por `PR #1116` en `CALC-ENCIG2025-PISOS-GOBDIGITAL-0001`, Δ ≤ 5.6e-7 |
| `GOB.gobierno_digital.encig2025.escolaridad_x_sexo` | 8 | ídem | ídem | ídem |
| `TRA.evade_norma.envipe2025.escolaridad_x_dominio` | 12 | `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` | **HEREDADO-DE-LEGACY** | `parametros.marginales_sellados` de `milpa/tramite-ola5-propuesta-v0.yaml:1715-1731`; control: reproduce a 4.79e-7 |

**Conteo: 5 celdas-D · 52 RESULT consumidos como `C2` · 4 celdas-D / 36
RESULT `HEREDADO-DE-LEGACY` · 1 celda-D / 16 RESULT `NUEVO`**
<!-- comando: cut -f5 forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-censo.tsv | tail -n +2 | sort | uniq -c -->.
De los cuatro `HEREDADO-DE-LEGACY`, este mismo `PR #1116` ya **relevó** los
dos cruces de ENCIG 2025 (16 RESULT) re-midiendo el piso desde microdato
(`CALC-ENCIG2025-PISOS-GOBDIGITAL-0001`, `CALC-ENCIG-DUELO-2025-
ADJUDICACION-0002`; ningún veredicto cambió, Δ ≤ 5.6e-7 — «Cierre ENCIG 2025»,
§2 arriba). Quedan **20
RESULT / 2 celdas-D** (ENIF localidad×edad, ENVIPE escolaridad×dominio) con
piso todavía legacy, diferidos a `GEN2-PISOS-GEN2-2` por decisión de mesa
(24/sep): «NC a PISOS-GEN2-2 (Recommended)» — no se tocan en este informe
(fuera de perímetro §9)
<!-- comando: grep -n "NC a PISOS-GEN2-2" forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-cierre.md -->.

**Estado de `GEN2-PISOS-GEN2-2` a este corte: en curso, sin fusionar.** Tiene
rama abierta (`acto/gen2-pisos-gen2-2`) con un COMMIT-1 de specs congeladas y
un censo de origen generalizado en curso (125 filas, tipo (3): reportado por
otra sesión, no verificado aquí, no se cita como hecho)
<!-- comando: git log --all --oneline | grep -c "GEN2-PISOS-GEN2-2" -->
<!-- comando: git log origin/main --oneline | { grep -c "GEN2-PISOS-GEN2-2" || true; } -->.
Cuando cierre, este informe se actualiza con la tabla «después» y el commit
de cierre, tal como el encargo lo pide.

---

## 4 · Qué puede afirmar el producto hoy, y qué no

**Puede afirmar, con corrida sellada detrás:**

1. Que predice celdas de cruce que no ha visto, **seis veces** (tres pilotos
   + lote ENIF 2024 + piloto 4 ENVIPE 2025 + cierre ENCIG 2025, dejando
   aparte el punto nacional de ENIGH y el duelo ENVIPE 2026 que no adjudicó
   piso ganador), con **79 + 38 + 16 = 133** celdas puntuadas contando sólo
   las de cruce evaluadas contra un candidato con IC, y que el error del
   piso va de 1.47 a 3.41 pp en pilotos, 1.87 pp en el lote, 0.31–2.69 pp en
   piloto 4 y 0.97–1.01 pp en el cierre ENCIG 2025.
2. Que en esos cruces **sabe cuánto se equivoca**, con el intervalo binomial
   y su advertencia de dependencia, **acotado a los cruces ya vistos**
   (heredado F-LOTE, v1.2 §2.2).
3. Que la interacción encogida **mejora medida y repetida** al piso, sin que
   eso adjudique nada: ninguna de las seis evaluaciones de la etapa cerrada
   produjo un `VENCE` puro (§0).
4. **17 celdas-D adoptadas activas** de 21 (ENIF 10 · ENCIG 3 · ENVIPE 1 ·
   otras 3), y **219 celdas validadas** (`celdas_validadas_definicion_desde
   = 38dd709`, PR #1086, no #1078 como citaba dirección — §1.2), de las
   cuales **20 son prospectivas**, reportadas aparte y nunca fundidas con
   las 59 retrospectivas (firma P, `ACTO GEN2-ADOPCION-BLOQUE-Y-PINES-1`,
   24/sep) <!-- comando: python3 tools/corrida0.py status | rg '^celdas_validadas=' -->.
5. **7 de 31 dominios del corpus con medición sellada y consolidada**
   (dinero/ENIF, trámites/ENCIG, seguridad/ENVIPE, tiempo/ENUT,
   ingreso/ENIGH, trabajo/ENOE, tecnología/ENDUTIH+MOCIBA), **2 más con
   `CALC` sellado sin consolidar como dominio** (ENDIREH, política/vida
   cívica INE·ENCUP·LAPOP) — corrige la premisa de dirección («5» y la
   lista «ENOE, ENDIREH, INE/ENCUP/LAPOP, MOCIBA/ENDUTIH…»: ENOE y
   MOCIBA/ENDUTIH ya sellaron entre el 22 y el 24/sep, vía `ASTRA5-U1`/`U4`)
   <!-- comando: grep -n "31 reports temáticos" README.md -->.
   El mapa por afirmación (`PR #1079`, `canon/mapa-dominios-v1_0.tsv`, 1 396
   filas) dictamina **208 MEDIBLE-EN-CORPUS · 768 MEDIBLE-CON-ADQUISICIÓN ·
   420 NO-MEDIBLE-POR-DISEÑO**
   <!-- comando: tail -n +2 canon/mapa-dominios-v1_0.tsv | cut -f18 | sort | uniq -c -->.
   ENSANUT, ENCODAT y ENBIARE siguen sin iniciar.

**No puede afirmar, y este informe lo dice antes de que lo pregunten:**

- **No le gana a un modelo de lenguaje en el nivel nacional** (heredado
  v1.1/v1.2, sin corrida nueva que lo toque).
- **No conoce su error fuera de cruces con la misma confianza** (heredado
  v1.2 §4: cobertura de persistencia en marginales 14/57 = 25%).
- **No explica por qué el nivel salta entre olas** (heredado v1.2 §4,
  `SALTO-SIN-EXPLICAR`).
- **La regla de salida de θ está satisfecha en sus tres condiciones, pero el
  retiro de código no ha corrido** (§0) — es una decisión estratégica
  declarada, no una ejecución mecánica.
- **Cuatro de cada cinco pisos `C2` que el marcador consume tenían números
  tecleados en su cadena de origen** (§3.5); dos celdas-D (20 RESULT) siguen
  así, diferidas a `GEN2-PISOS-GEN2-2`, todavía en curso.
- **No compone por segmento** (sin cambio respecto a v1.1/v1.2,
  ADR-91/ADR-531).

---

## 5 · Lo que viene

**Se cierra la construcción de retadores.** Seis evaluaciones prospectivas,
cuatro instrumentos, siete familias de retador (seis en la casa + Astra),
cero `VENCE` puro — el hallazgo es la línea base, no un candidato que la
supere (§0). El frente prospectivo pasa a las familias 2027 pre-registradas
(U4), una por ola futura, con a lo sumo un retador externo. El producto
avanza por **adopción**, no por medición: catálogo, relevo del motor, eje
regional y de clase, dónde sí cambió el mexicano.

**Sellado externo de todo lo emitido: manifiesto de 344 sellos**
<!-- comando: wc -l < forense/sellos/manifiesto-sellos-2026-09-23.tsv -->,
**cero `.ots`** <!-- comando: find . -iname "*.ots" | wc -l -->:
`GEN2-TUBERIA-SELLO-EXTERNO-1` intentó OpenTimestamps y una TSA RFC 3161,
ambos con `PARO-ENTORNO` (sin egress saliente en esta política de red); el
fallback en uso es la firma GPG del merge. **`SELLO-EXTERNO-2` no ha
corrido** <!-- comando: git log --all --oneline | { grep -ci "sello-externo-2" || true; } -->;
OpenTimestamps sigue **pendiente de mesa** (`FP-260923-GEN2-TUBERIA-SELLO-
EXTERNO-1-cfce-01`, ABIERTA).

**En curso, sin fusionar a este corte** (declarado, no se espera):
`GEN2-PISOS-GEN2-2` (§3.5, rama `acto/gen2-pisos-gen2-2`, COMMIT-1 ya
congelado), `GEN2-DONDE-CAMBIO-EL-MEXICANO-1` (rama
`acto/gen2-donde-cambio-el-mexicano-1`) y `GEN2-CLASE-AMAI-1` (rama
`acto/gen2-clase-amai-1`)
<!-- comando: git ls-remote --heads origin | grep -Ec "acto/gen2-(pisos-gen2-2|donde-cambio-el-mexicano-1|clase-amai-1)" -->.
Ninguna de las tres había fusionado a `origin/main` al momento de escribir
este informe. v1.4 las incorpora cuando cierren.

---

## 6 · Módulo de auditoría de rigor extremo

*Obligatorio en todo artefacto que afirme algo sobre México (§5 de las
instrucciones). Contestado, no rellenado.*

**¿Se confunde pobreza, violencia o informalidad con cultura?** No, sin
cambio respecto a v1.2: este documento sigue sin afirmación causal sobre
conducta. El gradiente por escolaridad y edad del cierre ENCIG 2025 («Cierre
ENCIG 2025», §2) se lee como **acceso y oferta** (cuenta bancaria, conectividad, recibo a nombre
propio), no preferencia — el denominador es quien pagó, no quien pudo pagar
(heredado del propio cierre de `PR #1116`).

**¿Sobregeneralización desde clase media urbana formal?** Sin cambio: el
piloto 3 y el cierre ENCIG 2025 (universo urbano, 100 mil+ habitantes) son
los más expuestos. ENIGH y ENVIPE conservan cobertura más amplia en la
medida en que sus instrumentos la tienen.

**¿Sesgo de marcos o de muestras estadounidenses/europeas?** No en este
informe: todo lo local es microdato INEGI. La corroboración externa (§2.5)
es explícitamente **no mexicana** y se etiqueta como tal; no entra en
ninguna media del programa.

**¿Qué cambiaría con foco rural, indígena o popular?** El piloto 3, el
cierre ENCIG 2025 y ENCIG en general (universo urbano) desaparecerían. El
lote ENIF 2024 y ENVIPE conservan cobertura rural en la medida en que sus
instrumentos la tienen. El sistema indígena-comunal vivo sigue fuera por
diseño.

**¿Qué parece psicológico y es incentivo racional?** El mismo ejemplo de
v1.2 (salto de ENCIG) más un caso nuevo: el hallazgo de §3.5 —cuatro de
cinco pisos con números tecleados— es un **defecto de método**, no un
hallazgo psicológico; se lee como tal y no se disfraza de conducta.

**¿Dónde hay evidencia débil e intuición fuerte?** En la comparación primaria
del cierre ENCIG 2025 («Cierre ENCIG 2025», §2): el piso se re-midió desde microdato y el
veredicto no cambió (Δ ≤ 5.6e-7), lo cual es evidencia **a favor** de que el
hallazgo no dependía del defecto de método — pero es una sola re-medición,
sobre dos cruces, y no generaliza a las otras 20 celdas C2 legacy que
`PISOS-GEN2-2` todavía no ha tocado.

**¿Qué sería peligroso leído en simple?** Cinco frases: (1) «se cerró la
etapa de retadores porque el motor no sirve» — no, se cerró porque **ningún
retador vencía y seguir construyendo retadores sobre carriles ya probados
no tenía sentido** (decisión estratégica de mesa, no un veredicto técnico
sobre el motor); (2) «C-ASTRA venció en escolaridad×sexo» sin el
calificativo `SIN-CANDIDATO-SUPERIOR` («Cierre ENCIG 2025», §2); (3) cualquier
ΔMAE de las cuatro evaluaciones nuevas de §2 citado sin su IC; (4) «cuatro de
cinco pisos están mal» leído como que las
adjudicaciones están mal — el piso re-medido dio el mismo veredicto (§3.5);
(5) «144 sellos GPG son criptográficamente equivalentes a OpenTimestamps» —
no lo son, es un fallback declarado, no el objetivo.

**[v2.16] ¿Qué cifra es PROSPECTIVA y cuál RETROSPECTIVA, y se mezclan en
alguna frase?** Las cuatro evaluaciones nuevas de §2 (ENIGH, ENVIPE 2026,
piloto 4, cierre ENCIG) son **PROSPECTIVA** (emisiones selladas antes de
abrir R, por CALC), igual que el lote y los tres pilotos (heredado). El piso
re-adjudicado del cierre ENCIG 2025 (`-0002`, §3.5) es **RETROSPECTIVA**: se
selló después de que el `-0001` derivó R (cruce visto, E.6) — así lo declara
`G-MARCA` del piso y `G-MARCA-EMISIONES` del `-0002`, y no se mezcla con el
ΔMAE prospectivo del mismo cruce. El backtest de crédito (heredado v1.2
§2.3) sigue **RETROSPECTIVA**; el origen móvil de ENCIG sigue
**RETROSPECTIVA-MECÁNICA**. Ninguna frase de este documento mezcla las dos
columnas.

**[v2.16] ¿Qué unidad tiene cada cifra y se promedia con otra?** Pilotos y
lote (heredado v1.2): persona/delito/trámite, no se promedian. Duelo ENIGH
2024: unidad **hogar**, no se promedia con nada más de este documento.
Duelo ENVIPE 2026 y piloto 4: delito, no se promedian entre sí pese a ser el
mismo instrumento y unidad — son cruces y cortes distintos. Cierre ENCIG
2025: trámite. El «137 celdas» de §0 es un **conteo de celdas evaluadas**,
no una cifra en pp — se puede sumar entre encuestas porque es la misma
pregunta binaria «¿se puntuó?»; los MAE de cada fila **no** se promedian
entre encuestas ni entre unidades.

**[v2.4, heredada] ¿En qué escala está cada cantidad?** Declarado al pie de
cada tabla. Todo lo nuevo de este informe (las cuatro evaluaciones nuevas de
§2 y §2.5) está en puntos porcentuales para MAE/ΔMAE de proporciones, salvo
el error absoluto de ENIGH (también pp, pero de una cifra a nivel hogar, no
de proporción de
personas/trámites/delitos).

**[v2.3, heredada] ¿Cuántos contadores movió este trabajo?** **Cero** (§0).
Este acto es de sólo lectura: no adopta, no sella, no escribe
`marcador-segmento.tsv` ni `decisiones.tsv`.

---

## 7 · Lo que este informe deja abierto

- **`GEN2-PISOS-GEN2-2` no ha cerrado** (§3.5, §5): 20 RESULT / 2 celdas-D
  (ENIF, ENVIPE) siguen con piso legacy tecleado; este informe reporta el
  censo «antes», no el «después».
- **`GEN2-DONDE-CAMBIO-EL-MEXICANO-1` y `GEN2-CLASE-AMAI-1` no han cerrado**
  (§5): sus hallazgos, si los hay, no están reflejados aquí.
- **El retiro de código de `g()`/`Theta.valor` no ha corrido** (§0), pese a
  que las tres condiciones de la regla de salida están satisfechas.
- **El intervalo binomial correcto sigue pendiente**, heredado de v1.1/v1.2:
  Wilson es lo que hay sin `scipy`.
- **`SELLO-EXTERNO-2` (OpenTimestamps) sigue pendiente de mesa** (§5):
  ninguna fecha comprometida.
- **La proyección de `marcador_segmento.py` (243 filas) no está commiteada**
  (§1.1): un acto de aparato tiene que correr `--escribe` y publicarla al
  canal antes de que este número deje de citarse con la salvedad «en árbol».
- **El detalle por celda del backtest de crédito 2024 no está en este
  informe** (heredado v1.2 §7, sin cambio: no alcanzable en NUBE sin abrir
  el CALC completo).
