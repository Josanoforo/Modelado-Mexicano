# RONDA M · El motor como matriz · Veredicto adversarial

### v1.0 · 13/ago/2026 · revisión de `propuesta-motor-matriz-v0_1.md` **§1-§5** con la rúbrica del veredicto de Ronda 1

> | | |
> |---|---|
> | **ARCHIVO** | `RONDA-M-motor-matriz-veredicto-opus-2026-08-13-v1_0.md` |
> | **CLASE** | Artefacto forense fechado, append-only. Registra el veredicto emitido contra la v0.1 de `propuesta-motor-matriz`; **no se reescribe** si la propuesta se corrige — la corrección vive en la adjudicación de mesa y en una v0.2 |
> | **ORIGEN** | ACTO RONDA-M, `forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md` **§5** (estado `VIVO` al arrancar). Entorno cumplido: sesión **nueva** de Opus, **no** la de MOTOR-1, **no** linaje Fable. Worktree de caja, rama `ronda-m` |
> | **BASE DE CITA** | `3d0d1e5` — la que fija la precisión (a) del §5 del encargo. Toda cita `archivo:línea` de §2/§3 está verificada ahí |
> | **SUITE** | El encargo declara `20 FAIL · 107 WARN` en `3d0d1e5`. **No la re-corrí en ese SHA.** La rama se creó sobre el `origin/main` real, `84b2acf` (#228), **44 commits** por delante; ahí la corrida cruda da **`24 FAIL · 119 WARN`** y `--baseline` da **LÍNEA BASE VERDE** (nada nuevo frente a `tests/baseline.json`, HEAD congelado `0ad9b7b`), antes y después de escribir este archivo. La cifra del encargo es anterior al recongelado de PROC-10-bis COMMIT 3, que subió el WARN esperado de 107 a 119. Y `T16` reporta por su cuenta que `canon/estado-programa-v1_10.md:129,221` y `canon/gobernanza-v1_15.md:764,856` siguen declarando `107 WARN` contra una corrida real de `119`. Divergencia declarada, no silenciada |
> | **VERIFICAS ASÍ** | Ninguna cita de la propuesta se dio por buena: se abrió el archivo. Los conteos (15 celdas de `B`, 11 producciones, 147 filas, 33 necesidades, 22 gl, 13/27, 0/15) se **re-derivaron por comando** sobre el árbol en `3d0d1e5`. Donde el texto era cierto contra su propia base (`76710a0`, 10/ago) y dejó de serlo, va en §6 como **deriva**, nunca como defecto |

---

## 0 · La rúbrica y su estatuto — tres cosas distintas, no una

Precisión (b) del encargo, contestada antes de juzgar. Lo que rige aquí tiene tres estatutos y se citan con la distinción:

1. **Los PRODUCTOS de Ronda 1 son canon.** Los siete umbrales go/no-go y la disposición sobre modelos elegibles entraron por **ADR-68** — verificado en `canon/gobernanza-v1_15.md:906` (adopción del contrato celda-D v0.3 §3), `:912` (los siete umbrales con dos ajustes de mesa), `:916` (M0 `RESUELTO-RECUPERADO`, con la disposición vigente).
2. **La rúbrica con la que juzgo NO es canon.** Sale del **veredicto** — `forense/RONDA1-motor-adaptativo-celda-veredicto-fable-2026-08-11-v1_0.md` §2 —, que es artefacto forense fechado.
3. **El protocolo "2 IA + 1 humano" como método sigue sin sellar.** No lo presento como sellado ni como inexistente: existe, corrió una vez, y no tiene ADR.

**Las ocho clases**, nombradas como clases (el veredicto de Ronda 1 las instancia como `D1`-`D8` sobre otro documento):

| | Clase de defecto |
|---|---|
| **C1** | La clave de identidad está definida de dos maneras incompatibles dentro del mismo documento |
| **C2** | Un campo o una cifra carga dos semánticas sin declararlo |
| **C3** | Vocabulario que colisiona con vocabulario ya sellado; o enum que mezcla ejes y omite categorías reales |
| **C4** | Falta el universo de búsqueda — cierre sin denominador (la clase (a) que A.4 existe para impedir) |
| **C5** | El caso que el diseño necesita no es representable con los campos que trae |
| **C6** | Un campo no es exclusivo, o re-declara lo que otro archivo ya es dueño de decir |
| **C7** | Enumeración incompleta y confusión de nivel de agregación |
| **C8** | Tensión declarada sin mecanismo ni etapa que la detecte |

**Benchmark: sigue sin hacer falta**, misma razón que en Ronda 1 — no se juzga un resultado, se juzga un contrato.

---

## 1 · Veredicto ejecutivo

La arquitectura es adoptable y su artefacto central **no es una invención de esta propuesta**: `gobernanza:461` (inciso (3) del bloque AJUSTE) ya obliga a declarar los momentos antes de ajustar y dice, con esas palabras, que el pre-registro *"hará falta antes de que exista una sola corrida `AJUSTADO`"*. El catálogo de §3.1 es ese artefacto, y hoy no existe. La cadena motor→ponderación→cálculo→demanda separa dos objetos —**π** poblacional y **W** de calibración— que el programa venía nombrando "la ponderación" sin apellido, y la regla de gasto de §3.2 (`:126`) es el primer freno estructural escrito contra la expansión horizontal.

La transcripción es honesta donde la verifiqué: las quince celdas de `B` una por una contra `procedencia.yaml:625-636`, las once producciones del barrido y su reparto 2/8/1, los nueve parámetros, los seis ejes con sus variables, `22 = 7 + 15`, `13/27`, `0/15`, el vocabulario de A.4. **M0 no se repite**: los tres dictámenes compass siguen fuera del repo (`git ls-tree -r 3d0d1e5 | grep -ci compass` → **0**) y la propuesta lo declara en su recuadro de PROCEDENCIA, lo marca tipo (2) leído como (3) y lo manda a mesa como M6 — exactamente la disposición que Ronda 1 pidió.

**Encontré doce defectos materiales y tres defectos de cita. Ninguno es conceptual** — §4 contesta esa pregunta con los cuatro candidatos que probé y por qué los cuatro salieron materiales. Siete de los doce bloquean el sello, y dos de esos siete meten error en el registro desde el día 1: el `ídem` de §5 pone el universo de **ENBIARE** sobre un número de **ENASIC**, y §1.4(c) declara resuelto por cambio de formalismo un gate de compilación que canon dice inejecutable en tres sitios y que "**PERSISTE**".

**Conclusión: APROBAR CON CAMBIOS.**

---

## 2 · Defectos materiales — ordenados por severidad

| # | Defecto | Clase | Evidencia verificada | Efecto sobre resultados | Fix de una línea | ¿Bloquea sello? |
|---|---|---|---|---|---|---|
| **M1** | **El check obligatorio de ADR-30 no se reduce a "un test de una línea sobre signos de columna"** — ni por el lado del contraste ni por el lado del operando | **C5** | Afirmación: `propuesta-motor-matriz-v0_1.md:65` (c). Canon dice lo contrario en tres sitios: `modelo:135` (*"el contraste que ese check exige —quien da cuidado frente a quien lo recibe, bajo el mismo techo— cae exactamente en la dimensión que la malla no resuelve"*), `modelo:227` (*"**H-11 no rescata el check de ADR-30**… El hallazgo **PERSISTE**; es problema del modelo, no de la segmentación"*), `modelo:779`. Y el operando no tiene signo que probar: `procedencia.yaml:629` da `familismo_obligacion: "signo negativo **o no monotónico** — SIN MAGNITUD"`, y `modelo:598` lo escribe como *"`ASIGNADO` y **sin magnitud**"*. La matriz se define sobre esa misma malla (`:33-38`) | Un gate de compilación sellado se da por resuelto por cambio de formalismo. Y §6 lo usa como una de sus tres condiciones de refutación (*"un chequeo de compilación tipo ADR-30 (§1.4.c) imposible de satisfacer"*): el pre-registro de falsación quedaría con una fila inejecutable sin que nadie lo note | Reescribir `:65` (c): *"el check de ADR-30 **no** se reduce a signos de columna — su contraste es intra-hogar y la malla no lo resuelve (`modelo:135,227,779`); bajo la matriz sigue igual de inejecutable y entra al catálogo como demanda `conjunta` no satisfecha"* | **Sí** |
| **M2** | **El libro de demanda de tres clases no puede representar dos de las tres clases de llave de ADR-57(c)** | **C5** | `:122` define `conjunta` como *"reactivo de θ y desenlace **co-observados en el mismo instrumento** (C1–C4, `modelo:153`)"* — que es la clase **(i)** de `gobernanza:627`. Las clases **(ii)** *"experimento natural con grupo de comparación sobre encuestas repetidas"* y **(iii)** *"diseño experimental de terceros… usado como evidencia (a) con su cita"* no son co-observación y no tienen clase de demanda. ADR-57(c) mantiene viva una ruta (ii) nombrada: ENOE como portador de desenlaces laborales, *"p. ej. salario mínimo de franja fronteriza"* | La regla de gasto de `:126` —*"ningún acto de apertura de fuente corre sin citar el `id_momento` o la celda de Θ que lo demanda"*— bloquearía por construcción los actos de las llaves (ii) y (iii): no hay `id_momento` que puedan citar. La "sola fuente de demanda" no es sola | Cuarta fila en la tabla de `:118-122`: clase `identificacion` — *"diseño que produce la conjunta sin co-observación; las tres clases de `gobernanza:627`, verbatim"* | **Sí** |
| **M3** | **El catálogo no tiene campo para el universo de BÚSQUEDA, y el nombre `UNIVERSO` ya está ocupado por el universo estadístico** | **C4** (agravante **C2**) | Campos de `:107-109`: `id_momento · definición · ESCALA declarada · UNIVERSO declarado · nivel · instrumento(s) candidato(s) · rol · estatus de disponibilidad`. `:112` declara que ese `UNIVERSO` sale de *"A-bis reglas 3-4"* — el estadístico. Pero `:124` invoca **A.4** (`instrucciones-proyecto-v2_6.md:238`), que exige declarar *"**en la misma línea** donde se escribe: qué se examinó…, con qué mecanismo, y en qué fecha"* — y ningún campo lo carga (`estatus de disponibilidad` es un token). La tabla de `:168` tampoco tiene columna. El contrato **ya sellado** por ADR-68(a) separa los dos y advierte contra confundirlos: `propuesta-motor-adaptativo-celda-v0_3.md:48,53-54` — *"`universo_instrumento`… **NO es `universo_candidatos`** (qué se barrió al buscar candidatos)"* | Cada `NO-ENCONTRADO` del libro de demanda nacería sin denominador — la clase (a) exacta que A.4 existe para impedir, ahora al nivel del catálogo que gobierna **todo** el gasto del programa | Añadir `universo_candidatos:` a `:107-109` con el nombre **verbatim** de ADR-68(a), y renombrar el campo actual a `universo_instrumento:` | **Sí** |
| **M4** | **La fila de ENASIC hereda por `ídem` el universo de ENBIARE** | **C6** | `:176`: `Distribución familismo_obligacion (ENASIC P7_12_7) │ Θ-lado │ **ídem** │ ídem │ …` — la cadena de `ídem` resuelve a *"escala del reactivo · **universo ENBIARE**"* de `:174`. El archivo dueño dice otra cosa: `data/curacion-registro/produccion-modelo.tsv`, fila `PROD-cca3ea0b…`, `input_path` = `enasic_2022_bd_csv.zip`, `poblacion` = *"Personas de **15 a 60 años**… seleccionadas como 'persona elegida' (una por hogar) — tabla **TPER_ELE**"*, con la advertencia explícita de que `TCSDEMPO`/`TPOB_CUI`/`THOG_UNIP` *"comparten P7_12_7 pero son universos distintos que se traslapan"*. Las otras diez filas son ENBIARE (`enbiare_2021_base_de_datos_csv.zip`, *"18 o más años, alfabeta y hablante de lengua española"*) | El `ídem` borra exactamente la distinción que el archivo dueño escribe en tres líneas para que nadie la borre. Es la clase de error que A-bis regla 4 existe para atrapar, y §5 es la tabla que alimenta el catálogo — el número viajaría al ejecutable con el universo de otra encuesta | Sustituir el `ídem` de `:176` por el `poblacion` verbatim del dueño (TPER_ELE · 15-60 · persona elegida), y prohibir `ídem` en la columna de universo | **Sí** |
| **M5** | **El `15` de §1.4 y el `15` de §4.2/§4.3 no son el mismo objeto** | **C2** | `:65` cuenta *"15 celdas no-cero"* y su propia tabla (`:62`) escribe **SIN MAGNITUD** en G5 × `familismo_obligacion`; `procedencia.yaml:629` y `modelo:598` la escriben igual. Pero `:148` dice *"Con **15 intervalos simultáneos**"* y `:152` *"cambia la clase de **15 `ASIGNADO` puntuales** a `AJUSTADO` con banda"* | Una de las quince no tiene punto que convertir en banda ni intervalo que simultanear, y su spec admite **no monotonicidad**, que un β escalar no expresa. El conteo de salidas del ajuste nace inflado en 1, y con él el chequeo de identificación de `:142` | En `:148`/`:152`: *"14 `ASIGNADO` puntuales + 1 sin magnitud (`familismo_obligacion` en G5), que no entra al ajuste sin decidir antes su forma"* | **Sí** |
| **M6** | **§3.1 traduce el inciso (5) de "POR PERFIL" a "por celda" sin declarar la traducción — y es la traducción que gobernanza declara no verificada** | **C3** | `:112`: *"computabilidad **por celda** o el momento no cuenta para identificar (inciso (5) del bloque AJUSTE, `gobernanza:465`)"*. El texto de `gobernanza:465` —**idéntico en `76710a0` y en `3d0d1e5`**— dice *"un momento solo es utilizable si se puede computar **POR PERFIL**"*, y añade: *"**no hay hoy un chequeo formal ya corrido sobre ejes demográficos** (edad, urbanización, ingreso, acceso digital, migración); son lecturas plausibles de esa tabla, **no una verificación**"* | La obligación central del catálogo se cita con una unidad que el propio inciso marca como no verificada. El catálogo nacería creyendo satisfecha una condición que gobernanza dejó pendiente — y la unidad importa: `modelo` v4.0 retiró el perfil como unidad de población | Citar el inciso verbatim ("POR PERFIL"), remitir a `modelo` §1.1.D como la traducción, y arrastrar la condición abierta de `gobernanza:465` como **precondición declarada** del commit 1 | **Sí** |
| **M7** | **§4.1 importa intacto el `22` de ADR-51 a un formalismo que añade una capa de parámetros (`h_r`) sin decir si entran** | **C2** | `:142` — *"los β (y las 7 libertades de probabilidad; **22 grados de libertad**, ADR-51)"* — exacto contra `gobernanza:457,485` (`22 = 7 + 15`). Pero `:79` introduce `h_r` como *"**elección de mecanismo declarada antes de ajustar** (p. ej. umbral lineal vs. logística), con sensibilidad reportada sobre una familia corta"*, y §8 lo manda a sellar en el commit 1. Un umbral tiene corte; una logística tiene escala. La propuesta no dice si esos parámetros quedan fijos por declaración, entran a los 22, o son un tercer conjunto | `:142` condiciona la identificación a *"número de momentos informativos ≥ número de parámetros libres"* y fija el segundo término en 22. Si `h_r` carga forma, el chequeo corre contra el denominador equivocado — y es el chequeo que `:144` presenta como la ventaja de la matriz sobre el ABM | Una línea en `:142`: *"los parámetros de forma de `h_r` quedan FIJOS por declaración y fuera de los 22; si alguno se ajusta, se cuenta y el 22 deja de ser el denominador"* | **Sí**, antes del commit 1 |
| **M8** | **§4.3 reclama la clase sellada `AJUSTADO` sin nombrar su campo obligatorio `ruta:`, y §4.2 produce una forma de valor que la clase no contempla** | **C3** | `gobernanza:439` (ADR-49 D2) sella `AJUSTADO` y *"**exige campo `ruta:` obligatorio**: `pseudo_panel` \| `momentos` \| `composicion` \| `transversal_con_seleccion`"*, con *"**Nace vacía: cero números `AJUSTADO` hoy**"*. `:152` dice *"Todo β calibrado así es `AJUSTADO` (la clase que ADR-49 selló)"* y no nombra ninguna `ruta:`. `:148` entrega *"una **banda**, reportada como identified set"*; la definición sellada describe *"reproduce los momentos observados de un dato real (media, varianza, transición)"* — número, no conjunto | Los primeros números `AJUSTADO` de la historia del programa nacerían sin el único campo que su ADR hizo obligatorio, y con una forma de valor sobre la que la clase no se pronunció | `:152` declara `ruta: momentos` **verbatim** para toda salida del SMM, y manda a mesa la pregunta acotada: *"¿un identified set es valor admisible de la clase `AJUSTADO`, o exige campo propio?"* | No para revisar; **sí** antes de la primera corrida |
| **M9** | **§1.4(a) conserva la fila `G1 (a/b)` y deja sin dueño un coeficiente que canon ya adjudicó** | **C1** | `:65` (a): *"la fila `G1` de procedencia agrupa lo que ADR-20 desdobló — **el −0.60** está adjudicado a G1a… y G1b está en HIPÓTESIS con 'coeficiente a revisión' (`modelo:371`)"*. Pero `modelo:390-391` (tabla §2.2) ya lo resuelve entero: **G1a** lleva `confianza_institucional[financiera] −0.60` **y** `radio_confianza −0.35`; **G1b** lleva *"a revisión — el generador está contradicho"*, es decir **ninguno**. `modelo:378,724` cuenta **siete** generadores y quince coeficientes; la matriz de `:56-63` tiene **seis** filas | El índice de fila de `B` es una clave pre-desdoble donde canon ya tiene la post-desdoble: `radio_confianza −0.35` se lee como posiblemente de G1b, y `:83` saca a G1b del formalismo sin que se pueda decir qué se lleva. La cuenta de generadores del documento no coincide con la de canon | Partir la fila en `G1a` (−0.60, −0.35) y `G1b` (sin coeficientes, `modelo:390-391`), y decir en `:83` que la excepción de campo medio toca **`h`, no `B`**, porque G1b no aporta ninguna celda | No, pero antes de la primera celda del catálogo |
| **M10** | **§3.1 pone la computabilidad por celda como condición de pertenencia y §3.3 prohíbe mirar el disco hasta después de sellarla** | **C7** | `:112`: computabilidad por celda *"**o el momento no cuenta para identificar**"* — condición de pertenencia. `:130`: *"**commit 1** sella catálogo y roles… ***antes*** de abrir el escaneo de disponibilidad; **commit 2** trae el libro de demanda con estatus"*. La computabilidad por celda es propiedad de (momento × instrumento × discretización `D`): no es decidible sin las variables y el diseño muestral del instrumento — justo lo que la venda del commit 1 prohíbe abrir | O el commit 1 sella computabilidades no verificadas —y el blindaje anti-circularidad protege un catálogo cuyo criterio de admisión ya se coló—, o la venda se rompe en el primer momento. Las dos frases no pueden valer a la vez | Mover la computabilidad de **condición de pertenencia** (commit 1) a **veredicto registrado en commit 2** con vocabulario A.4: el commit 1 sella el momento y su cómputo **pretendido**, no que se pueda | **Sí** — es diseño del commit 1, no se añade después sin ser post-hoc |
| **M11** | **§5 escribe "0 ejercidas" sin denominador y nombra dos de las tres llaves de la lista corta** | **C7** (con **C4**) | `gobernanza:627` lista **tres** con estado verificado: ENNViH/MxFLS; ENASEM + pensión Bienestar; y **ENOE**, *"refutado como ruta de conducta financiera… permanece elegible únicamente como portador de desenlaces laborales para experimentos naturales"*. `:178` nombra las dos primeras y da *"**0 ejercidas**"*. El contador del programa es `llaves de identificación ejercidas: 0 de 2` (`gobernanza:934`), cuyo denominador sale del censo y que el propio canon marca: *"**El 2 es provisional**"* (`gobernanza:978`) | Un contador sin denominador en un documento que escribe todos los demás con el suyo (`9 de 14`, `0 de 15`, `13 de 27`, `4 de 144`). Y la llave omitida es la de clase (ii) — la que **M2** muestra que el libro de demanda no puede representar | `:178` → *"**0 de 2** (denominador provisional, `gobernanza:978`); tercera entrada de la lista corta, ENOE, elegible solo para desenlaces laborales (`gobernanza:627`)"* | No |
| **M12** | **`MECANISMO-NO-CORRIDO` se presenta como "la marca del programa" y no existe en el programa** | **C3** | `:124`: *"más **la marca del programa** `MECANISMO-NO-CORRIDO` cuando nadie ha resuelto la fuente"*. `git grep -l "MECANISMO-NO-CORRIDO" 3d0d1e5` devuelve **un solo archivo: `propuesta-motor-matriz-v0_1.md`**; cero apariciones en `76710a0`. A.4 sella el vocabulario en **cuatro** palabras (*"Vocabulario obligatorio, cuatro palabras"*, `instrucciones-proyecto-v2_6.md:240-245`) | Un quinto término entra a un vocabulario sellado con la autoridad prestada de "el programa", sin ADR y sin dueño | `:124` → *"marca **propuesta aquí**, sin uso previo en el repo — entra a mesa o se retira, y su contenido va en la línea de universo del `NO-ENCONTRADO`"* | No |

---

## 3 · Defectos de cita — materiales, fuera de la tipología de las ocho

Los separo porque no son estructurales: son referencias que no resuelven. En un programa cuya regla es *derivar, no teclear*, una cita muerta cuesta el tiempo de quien la persigue.

| # | Defecto | Evidencia | Fix |
|---|---|---|---|
| **X1** | **`DH-ea9e932f70ce12` no existe** (`:50`) | El id real es **`DH-ea9e932f3970ce12`** — `data/curacion-registro/decisiones-humanas.tsv`, `necesidad_id` N14, ENBIARE, *"¿PB1_01/PB1_02… equivalentes al constructo vigente de `radio_confianza` para uso paramétrico?"*. El id de la propuesta no aparece en **ningún** otro archivo del árbol. La forma corta de `:175` (`DH-ea9e`) sí es prefijo válido | Añadir `39`: `DH-ea9e932f3970ce12` |
| **X2** | **El `−0.40` de G4 se cita a `modelo:398`, que no lo contiene** (`:61`) | `modelo:398` es la nota de homogeneidad de pendientes de **G1a**; menciona `confianza_institucional[justicia]` pero no la magnitud. El dueño del valor es `modelo:394` (tabla §2.2) y `procedencia.yaml:628` | Cambiar la cita a `modelo:394` |
| **X3** | **"la cola del curador… produce exactamente sus 147 filas"** (`:134`) | **147 es correcto**, pero es el conteo de `data/curacion-registro/trabajo-semantico.tsv` (148 líneas − cabecera). La **cola** es `data/curacion-registro/cola-residual.tsv`, que tiene **148** filas. El número no aparece en ningún otro archivo del árbol | Nombrar el archivo del que sale el 147 |

---

## 4 · La pregunta CONCEPTUAL, contestada

El encargo manda **titular y parar** si aparece un defecto conceptual — clase nueva fuera de las ocho, de las que no se arreglan con una edición de una línea a un párrafo. **No encontré ninguno.** Probé cuatro candidatos y los cuatro salieron materiales; los dejo escritos para que se sepa qué se probó, no solo qué se halló.

1. **"La derivación de la demanda es un traslado, no una eliminación, del trabajo a mano."** El catálogo se **escribe** (`:104`, *"Artefacto nuevo, pre-registrado, append-only"*); lo derivado es el libro de demanda a partir de él. Pero la propuesta no lo esconde: `:21` dice que el conjunto de salidas *"es finito, enumerable y **se escribe**"*, y `:130` le pone venda anti-circularidad. La ganancia declarada —una fuente en vez de dos listas, con regla de gasto— se sostiene. **No es defecto.**
2. **"El mecanismo `h_r` es disciplina, no derivación, y por tanto el eslabón 4 no cierra."** Declarado sin regatear en `:79` (*"no la resuelve por magia"*) y acotado en `:156`. Lo que sí falta es **contar sus parámetros** — eso es **M7**, y es material.
3. **"La equivalencia matriz↔ABM se afirma en negrita."** Está calificada en el propio `:77` (*"ABM de agentes **independientes**"*), su excepción está declarada en `:83`, y §10 la marca como enunciado matemático a probar en la spec, no como hecho del corpus. **No es defecto.**
4. **"La arquitectura se construye sobre una malla que canon declara incapaz del contraste que ADR-30 exige."** Es cierto — y es **M1**. Pero refuta una **afirmación de la propuesta sobre** la arquitectura, no la arquitectura: corregido M1, el check vuelve a ser demanda `conjunta` insatisfecha del catálogo y la matriz sigue en pie. **Material.**

Mismo desenlace que Ronda 1 y por la misma razón: ninguno exige teoría nueva, ninguno reabre una decisión sellada.

---

## 5 · Condiciones sobrevenidas — canon se movió bajo la propuesta

**No son defectos del autor.** Verificado: al 10/ago (`76710a0`) nada de esto existía en el árbol — `git ls-tree -r 76710a0` no trae `propuesta-motor-adaptativo-celda-v0_*.md`, ni `forense/RONDA1-*`, ni `data/curacion-registro/celdas-d/`. Al 13/ago sí, y con ADR. **No bloquean la aprobación; bloquean el sello.**

- **S1 · Existe un registro sellado que solapa al catálogo.** ADR-68(a) (`gobernanza:908`) adopta el contrato celda-D v0.3 §3 como formato del registro de comparación de estimadores, con hogar `data/curacion-registro/celdas-d/` — y ya hay dos celdas escritas (`G5.familismo_obligacion.actitud.yaml`, `G5.radio_confianza.encuci_vs_enbiare.yaml`). §1-§5 no declara la relación entre el catálogo de momentos y ese registro. §3.4 hace la pregunta análoga para el curador (M5) y no para éste.
  **Fix:** una pregunta nueva en §9 — *"M7 · ¿el catálogo de momentos es la capa de demanda del registro celda-D de ADR-68(a), o un artefacto hermano con cruce declarado?"*
- **S2 · El `rol:` de §3.1 colisiona con el `rol:` sellado.** `:109` usa `rol (AJUSTE | HOLDOUT | DIAGNÓSTICO)`; ADR-68(a) sella `rol: BASELINE | CHALLENGER | COMPLEMENTO` para el registro vecino. Dos enums con el mismo nombre en la misma familia de artefactos — la clase C3, llegada por el otro lado.
  **Fix:** renombrar el de `:109` a `rol_calibracion:`.

---

## 6 · Deriva del terreno — cifras de §1-§5 que caducaron entre `76710a0` y `3d0d1e5`

Verificadas contra los dos SHA. **No son defectos**; sí caducan la tabla de §5 y una línea de §1.3, y mesa las necesita antes de sellar.

- **`9 de 14` (`:50`, `:120`) → hoy `10 de 15`.** PROC-11 (#224) llevó `D` de 14 a 15; PROC-10-bis (#227) selló la séptima clase `MEDIDO·NACIONAL` (ADR-79(a)) y le entró `norma_de_género`. Y el renombre de ADR-75(b) toca directamente a este documento: la condicional que `:50` y `:176` llaman `familismo_obligacion` **medida por ENASIC `P7_12_7`** es la que pasa a llamarse `norma_de_género`; `obligacion_medida` es la celda nueva, medida por `P6_38`.
- **El estado de esa producción cambió.** `:50` la da como `NO_DETERMINADO` y `:176` como *"DH-332 + CRES-7cb78abf (especificación)"* — cierto en `76710a0`, donde la fila decía `NO_LISTA_CALCULO_NO_DETERMINADO` con `requiere_decision = SI` y `DH-332a13a70cbbf875` estaba `PENDIENTE`. En `3d0d1e5` la fila dice **`LISTA_PARA_USO_MODELO`**, `requiere_decision = NO`, y la DH está **`RESUELTA`**.
- **Una asimetría que vale la pena mirar.** `DH-ea9e932f3970ce12` también pasó a **`RESUELTA`**, pero **las ocho filas de `radio_confianza` siguen en `NO_LISTA_DECISION_HUMANA_PENDIENTE` con `requiere_decision = SI`**. El "frenadas" de `:50`/`:175` sigue siendo cierto en el terreno **aunque la decisión que lo motivaba ya se resolvió**: la decisión se movió y las filas no.
- **ADR-68(f) ya reparte esa θ en dos celdas.** *"`familismo_obligacion` (dos celdas ligadas por brecha-momento, rol COMPLEMENTO — no competencia)"* (`gobernanza:918`). La fila única de `:176` ya no describe el objeto.
- **Fuera de mi perímetro, verificado al paso:** §7.2 dice que `propuesta-motor-como-contexto-2026-07-30.md` *"vive solo en el espejo"*. Era cierto en `76710a0` y **es falso en `3d0d1e5`**: el archivo está en la raíz del repo. Lo anoto por estar verificado; no revisé §7.

---

## 7 · Verificado y NO es defecto

Para que se sepa qué se probó y no solo qué falló. Todo lo de abajo se abrió archivo por archivo en `3d0d1e5`:

- **Los seis ejes**, sus variables ENIGH, módulos y llaves, y el veredicto de P1 `CONJUNTA COMPLETA`: exactos contra `modelo:110-137`, incluida la restricción de nivel hogar con su cita verbatim de P1 (`modelo:129`).
- **El corolario del IPU** (`modelo:173`, *"el IPU reproduce marginales; no fabrica conjuntas que nadie midió"*) y su consecuencia sobre la malla de pares: exacto.
- **Los nueve parámetros** (`modelo:251`), **49 reglas** y perímetro **27** (`modelo:11`), **42 + 7 disparadores** (`modelo:88,601`), **C1-C4** (`modelo:153`): exactos.
- **Las 15 celdas de `B`, una por una**, contra `procedencia.yaml:625-636` — los quince valores, sus signos y el `SIN MAGNITUD` (que es **M5**, no error de transcripción). El no-doble-conteo de `familismo_apoyo` (`procedencia:82-89`) y la marca (b) sobre las escalas de familismo (`procedencia:633-635`): exactos.
- **Las 11 producciones del barrido** y su reparto **2 / 8 / 1**: re-contadas sobre `produccion-modelo.tsv` (12 líneas − cabecera) por `objeto_modelo_origen`. Exacto. Y la atribución de las ocho a una sola decisión también lo es: las ocho comparten `relacion_id = REL-5741e12ce3e0a0e076ee48fc`, que es el de esa DH.
- **`22 = 7 + 15`** (ADR-51) contra `gobernanza:457,485`; **`13/27`** y **`0/15`** contra `README.md:36,38`; **"7 de sus 13 veredictos son `D`"** contra `README:36` (`7D·2B·2A·2E`): exactos.
- **El vocabulario de A.4**, cuatro palabras, y su cita `instrucciones-proyecto-v2_6.md:238`: exacto.
- **M0 no se repite.** Los tres dictámenes compass siguen fuera del repo (`grep -ci compass` sobre el árbol de `3d0d1e5` → **0**) y la propuesta lo declara en PROCEDENCIA, lo marca tipo (2) leído como (3), y lo manda a mesa como M6 — la disposición exacta que Ronda 1 pidió. **Una sola asimetría, menor**, que no subo a §2: `:37-38` llama *"restricciones **heredadas**"* a dos límites, y el segundo (dicotomización, dictamen `wf-8b198c56`) no se hereda de canon sino del espejo. Es una palabra: *"restricción **propuesta** (fuente espejo, M6)"*.

---

## 8 · Conclusión

**APROBAR CON CAMBIOS.**

La arquitectura llena un hueco que un ADR ya declaró abierto —`gobernanza:461` obliga al pre-registro de momentos y dice que hará falta antes de la primera corrida `AJUSTADO`— y lo llena coordinando piezas existentes en vez de duplicarlas. La transcripción del corpus resistió la verificación por muestreo en todos los casos sustantivos, y la procedencia del material del espejo se declara con la honestidad que Ronda 1 exigió.

Pero **§1-§5 no se puede sellar como está**. Siete defectos bloquean, y dos de ellos meten error en el registro desde el primer día: el `ídem` de `:176` pondría el universo de ENBIARE sobre un número de ENASIC —la clase de error que A-bis regla 4 existe para atrapar, y que el archivo dueño escribe en tres líneas para que nadie la cometa—, y `:65`(c) da por resuelto, mediante cambio de formalismo, un gate de compilación que canon declara inejecutable en tres sitios y del que dice que **"PERSISTE"**.

Las doce correcciones son ediciones de una línea, salvo **M10**, que es una reordenación de dos frases entre §3.1 y §3.3. Ninguna exige teoría nueva. Ninguna reabre una decisión sellada. **Ninguna justifica RECHAZAR una arquitectura cuyo fondo es correcto.**

---

## 9 · Perímetro y método de este acto

- **Revisé §1-§5.** No revisé §6-§10 salvo donde un defecto de §1-§5 los alcanza: §6 depende de `:65`(c) (**M1**), y §8/§9 reciben los fixes de **M7**, **M8** y **S1**. El único hallazgo verificado fuera del perímetro va en §6 rotulado como tal.
- **No propuse rediseños.** Cada fix cabe en una línea del documento revisado, con la excepción declarada de M10.
- **No escribí en `canon/`, `milpa/`, `data/`, `tools/` ni `tests/`.** Perímetro de escritura de este acto: **un archivo nuevo en `forense/`** — éste.
- **Suite:** corrida antes y después de escribir el archivo, sobre el HEAD real de la rama. Sin cambio en ninguna de las dos: **`24 FAIL · 119 WARN`** crudo y **LÍNEA BASE VERDE** con `--baseline` (nada nuevo frente a `tests/baseline.json`, HEAD congelado `0ad9b7b`). El `20 FAIL · 107 WARN` de la cabecera es el que declara el encargo para `3d0d1e5`, SHA en el que no la re-corrí; es anterior al recongelado de PROC-10-bis COMMIT 3.

---

## 10 · Módulo de auditoría — acotado

Acotado por v2.3 (`instrucciones-proyecto-v2_6.md:119`): el módulo *"no va en… forenses de proceso"*. Éste lo es — revisa un documento y **no afirma nada sobre México**, así que las siete preguntas temáticas no tienen función aquí. Contesto las dos que sí:

**Contadores movidos por el trabajo que produjo este artefacto: 0.** Es un acto de revisión.

**(v2.1) ¿Qué afirmación sobre el estado del corpus se escribió a mano y no se derivó?** Ninguna cifra de este documento se copió de la propuesta: los conteos (15 celdas de `B`, 11 producciones, 147 filas, 33 necesidades `N1`-`N33`, `22 = 7 + 15`, `13/27`, `0/15`, `7 de 13`) se re-derivaron por comando sobre el árbol en `3d0d1e5`, y las citas `archivo:línea` se abrieron una por una. **Lo único no derivado aquí es el `20 FAIL · 107 WARN` de la cabecera**, que se cita como *declarado por el encargo* y que no re-corrí en `3d0d1e5`; la corrida que sí hice, en el HEAD real de la rama, da `24 FAIL · 119 WARN` crudo y **VERDE** contra `tests/baseline.json`, y `T16` reporta además que cuatro sitios de `canon/` siguen declarando `107 WARN` contra una corrida real de `119`.
