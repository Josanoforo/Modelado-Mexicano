# ACTO ADQ-ENOE-PRE2019 — cierre

*20 de agosto de 2026 · entorno UBUNTU · Opus · `ADR-143` · gate `#1` fusionado · base `89c939b` (`PR #309`)*

---

## 0 · ARRANQUE, las cinco líneas

| # | qué | valor crudo |
|---|---|---|
| 1 | **REPO** | Clon existente `/home/pc0/Modelado-Mexicano` · `89c939b Merge pull request #309 …` · `git status` limpio. Worktree propio `/home/pc0/mm-adq-enoe-pre2019`, rama `adq-enoe-pre2019` |
| 2 | **SHA** | `89c939b` = `origin/main`. `main` no se movió durante el acto (re-verificado antes de escribir el ADR) |
| 3 | **`data/raw`** | Existía en el clon como symlink a `/home/pc0/mm-corpus/raw`; **la enlacé** igual en el worktree nuevo. **Este acto SÍ descarga** — la verificación de corpus compartido está en §2 |
| 4 | **ENTORNO** | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → **sin variable** (esperado) · `curl … https://www.inegi.org.mx/` → **`200`** |
| 5 | **ESPEJO** | No se usó. Toda cifra de esta nota sale del clon de (1) con su comando |

**Concurrencia.** `pgrep -af claude` sólo vio mi propio shell — y eso no prueba que no haya otra sesión (`CAJA-RESIDUOS` ya midió que `pgrep` no ve una sesión de agente concurrente). Cruzado con `git reflog`: última entrada `2026-08-20 19:29`, la mía. Dueña única.

**Gate.** `#1` del lote. `gh pr list --state open` → **vacío**: todo el lote estaba fusionado al arrancar, así que el gate se cumple sea cual sea el item que ocupe el `#1`.

---

## 1 · La premisa, re-verificada como el encargo pide — y dos precisiones

**Exacta en lo esencial.** `data/indice-descarga-masiva-2026-08-05.tsv` trae **243** filas `enoe` con año anterior a 2019, serie continua desde 2005, y los catorce conteos anuales coinciden uno por uno con los que el encargo cita.

**Precisión 1, de cifra.** *«en .zip de microdato»* son **240** de las 243; las otras 3 son PDF de `doc`. Y **1** de las 243 ya estaba en el manifiesto (un PDF), ninguna de las 240 de microdato.

**Precisión 2, y ésta cambió el diseño del acto.** El índice registra **sólo** la ruta `/microdatos/` de INEGI. La ruta `/datosabiertos/` —de la que vinieron **los 28 payloads ENOE post-2019 que ya estaban en disco**— es invisible en él. Sondeadas las dos antes de bajar nada: `/datosabiertos/` **no sirve ninguna ola de 2017 ni `2018T1`/`2018T2`** — `200` con `text/html` de `2263` bytes, el soft-404 de INEGI que `ADR-130` ya había medido. Seis trimestres, y caen justo sobre el borde del decreto. Un acto que hubiera supuesto *«bajo todo por donde vinieron los de 2019»* se habría llevado seis páginas HTML con nombre de `.zip`. De ahí la decisión, congelada en COMMIT A §2 antes de la primera descarga: **el período pre se adquiere uniformemente por `/microdatos/`**, la única ruta completa sobre él.

---

## 2 · T1 · Adquisición — y las dos advertencias del encargo, contestadas

**27 payloads.** Doce olas `2016T1`–`2018T4` (`/microdatos/`, csv), un puente `2018T4` por `/datosabiertos/`, cuatro olas-sonda `2005T1`/`2008T1`/`2012T1`/`2014T1`, y diez descriptores de instrumento de las dos eras. 466 MB de microdato más 14 MB de PDF.

**⚠️ «Verifica que los payloads quedaron en el CORPUS COMPARTIDO» (defecto de `PR #77`).** El script escribe **directamente** en `/home/pc0/mm-corpus/raw` — no en el worktree — y descarga a un scratch **dentro** de esa misma raíz para que el `os.replace` final sea atómico. Verificado al cerrar por tres vías: `ls` de los 27 contra la ruta absoluta del corpus (**27**), los mismos archivos visibles desde `/home/pc0/Modelado-Mexicano/data/raw/` (el **clon principal**, no el worktree), y `tests/manifiesto.py --verifica` → **`27/27 COINCIDE`**. El scratch quedó limpio.

**⚠️ «Antes de bajar, consulta el manifiesto por cada id» (`A.8`, defecto de `ACTO R`/`ACTO R″`).** Corrido **antes** de la primera descarga y escrito en COMMIT A §1: de 37 ids ENOE en el manifiesto, el único con año 2005-2018 era `enoe_con_basedatos_proy2010_pdf`, un PDF de metodología; de 29 archivos ENOE en `data/raw`, ninguno pre-2019. Cero riesgo de duplicado. Y una **segunda línea de defensa que no dependía de mi lectura**: `tests/manifiesto.py --registra` deduplica por `sha256` y aborta si el contenido ya está bajo otro id — `27/27` pasaron sin colisión.

**Discrepancia declarada, no resuelta.** `FP-64` dice *«36 payloads»* de ENOE. Ninguno de los dos conteos de este acto la reproduce (29 archivos en `data/raw`, 37 ids en el manifiesto antes de bajar). Las tres cuentan poblaciones distintas y ninguna refuta a las otras, pero la cifra de la fila no se reproduce y queda dicho.

---

## 3 · T2 · El barrido — el entregable que el encargo anticipó, con una evidencia que no pedía

**El veredicto pedido, y es el Desenlace 2 de COMMIT A §6:** las **14 filas** salen `EXISTE-NO-SATISFACE` o `NO-ENCONTRADO`, cero `EXISTE-SATISFACE`. **ENOE queda descartado por Razón 1 con universo declarado.** Universo: 16 PDF, **5,021,037 caracteres**, dos extractores, 118 términos congelados antes de abrir nada, **76 con cero aciertos**. La adjudicación fila por fila está en `forense/notas/2026-08-20-adq-enoe-pre2019-resultados.md` §1.1; el resumen es que **cada acierto sustantivo vive en un reactivo que ya estaba adjudicado**: `ahorr` es siempre `P3M7` (*«préstamos personales y/o caja de ahorro»*, prestación del patrón), `riesgo` es *«el trabajo era riesgoso»*, `violencia` es una categoría del motivo de migración. Y `confia`/`confianza` **no aparecen ni una vez** en cinco millones de caracteres.

**La evidencia que el encargo no pidió y que es la que de verdad cierra la pregunta.** *«Puede que las olas viejas sí traigan lo que las nuevas no»* es una afirmación de **diferencia de conjuntos**. Un léxico puede fallar por elegir mal los términos; una diferencia de conjuntos sobre el inventario **completo** de variables, no. Corrida: de las **553** variables que las 12 olas pre-2019 traen, **cero** faltan en las 29 olas post-2019 — `SOLO_PRE = 0`. Y contra olas-sonda de **2005, 2008, 2012 y 2014**, las dos eras de instrumento: **0 huérfanas** en las cinco tablas de cada una. La ENOE sólo **ganó** variables (75, casi todas de diseño y geografía). La hipótesis queda refutada por conjunto, no por muestreo.

**Por qué las olas-sonda no eran adorno.** Al abrir `CAL-ENOE Fase A` descubrí que los tres cuestionarios que gobiernan `2016`-`2018` (`c_bas_v5`, `c_amp_v5`, `c_sdem_v4`) **ya estaban** en el universo que ese acto leyó el 31/jul. Es decir: barrer sólo la ventana que COMMIT A pre-registró habría re-barrido el mismo instrumento y no habría contestado nada. La hipótesis del encargo sólo puede ser cierta en las eras **anteriores** — la `14ymas`, cuyos descriptores (`fd_c_amp_v1`…, `fd_c_bas_v1`…) **ningún acto del proyecto había abierto**. De ahí las dos extensiones sobre COMMIT A, declaradas en commit posterior y **sin editar la ficha congelada**, como su propia §ESTADO manda.

**Y la adquisición no fue en balde, aunque el barrido salga negativo.** Las claves que un DiD por franja fronteriza necesita —`ENT`+`MUN`, `FAC`, `UPM`, `EST_D`, `T_LOC`— están **en las dos eras**. El antes/después es construible; lo que falta es el pre-registro de diseño. Con dos advertencias medidas para quien lo escriba: `MUN` no está en `COE1`/`COE2` (hay que traerlo por la llave de hogar), y el post-2019 añade `FAC_TRI`/`FAC_MEN` **junto a** `FAC`.

---

## 4 · T3 · La adjudicación, y lo que salió de ella

**Las tres filas del registro, no una muestra.** `CAL-G3` → **(i)** (ya rotulada así, sólo trasladada a columna propia). `R5.1-D2` y `R5.1-D3` → **(ii)**, con los tres elementos de la definición sellada **escritos** en sus pre-registros y no inferidos por parecido: corte natural (el cambio de regla de elegibilidad de 2019), grupo de comparación explícito, encuestas repetidas transversales.

**La consecuencia que `FP-64` no sacó.** Su titular dice que la llave (ii) *«sigue sin renglón operativo en ningún archivo del programa»*. Adjudicadas las tres, eso queda refutado por el propio registro: **la (ii) tiene dos renglones, y son las dos únicas llaves ejercidas del programa.** La (i) tiene una y está en cero. El `2 de 3` del contador es **enteramente (ii)**. Lo que faltaba no era una llave; era la etiqueta.

**La columna nueva va al final de la tabla a propósito**, porque `T24` lee `estado` por posición y la receta congelada de §4 del registro también.

---

## 5 · `T24` — el vigía, y el modo de falla que estaba a una columna de distancia

El encargo advierte que `T24` es binario y que *«cualquier fila nueva rompe la suite»*. Este acto **no añade filas**, así que esa advertencia no se activó. Pero al mirar el vigía para no romperlo apareció algo peor, y medido:

**El índice vecino (`veredicto`) contiene `EJERCIDA_` en 2 de 3 filas, exactamente igual que `estado`.** Así que **quitar** una columna antes de `estado` dejaba a `T24` derivando `2 de 3` — el valor correcto — **en verde, desde la columna equivocada**. No es hipotético: se probó, y el código viejo daba verde falso. Insertar una columna daba el modo benigno (falla, pero culpando a `estado-programa` de una discrepancia que no era suya).

`T24` ahora deriva la posición de `estado` del **encabezado** y la cruza contra la que la receta congela; si divergen, lo dice nombrando la columna y la posición. Probado con los dos adversarios. Es el único cambio en `tests/check.py`, como el perímetro manda.

---

## 6 · Contadores

| contador | antes | después | por qué |
|---|---|---|---|
| **`llaves de identificación ejercidas`** | `2 de 3` | **`2 de 3`** | Adjudicar la **clase** de una fila existente no toca su `estado`, y `T24` deriva numerador y denominador sólo de `estado`. Derivado con la receta congelada de §4 después de escribir la columna, no supuesto |
| **`β con ruta`** | `9 de 15` | **`9 de 15`** | Derivado de `censo-estimabilidad-coeficientes-v1_2` (`RUTA-A` 3 · `RUTA-I` 1 · `RUTA-C` 5 · `SIN-RUTA` 6). Este acto **no toca** el censo, `milpa/procedencia.yaml` ni `data/coef-universo-v1_0.tsv`. `N5` (`G3.horizonte_temporal`) ya decía *«ruta ENOE de ADR-49 D1 NO se re-propone»* — el barrido de T2 confirma que eso era correcto, y no lo cambia |
| `13 de 27` (Hito D) · `15 coeficientes, cero medidos` · `9 de 14` · `4 de 144` | — | **sin mover** | Ninguno entra al perímetro |
| conteo de ADR | `142` | **`143`** | Cascada obligada, propagada a `gobernanza` (cabecera) y `estado-programa` (cabecera y `L0`) en el mismo acto |
| suite | `19 FAIL · 142 WARN` | **`19 FAIL · 144 WARN`** | +3 filas `ABIERTA` (`FP-105`/`106`/`107`), −1 porque `FP-64` sale de `ABIERTA` a `FIRMADA` **con `ejecutada_en` puesto**. Cero FAIL nuevos |

**Tablero.** `FP-64` `ABIERTA`→`FIRMADA` (mesa firmó (b), este acto lo ejecutó, las dos mitades). Nacen `FP-105` (la contradicción entre `ADR-57(c)` y la Razón 1), `FP-106` (las dos rutas de INEGI no son intercambiables y el corpus ya las mezcla sobre el corte), `FP-107` (un `NO-ENCONTRADO` del programa derivado sobre un tercio del texto de sus PDF).

---

## 7 · Lo que vuelve a mesa, y por qué no lo decidí yo

**`FP-105` es la fila que gobierna lo que sigue, y nació de tener que ejecutar el encargo.** El encargo dice que si el barrido sale negativo, *«ENOE queda descartado por Razón 1 … y la llave (ii) vuelve a mesa»*. Escribí el negativo. Pero **no puedo escribir «ENOE queda descartado de la llave (ii)»**, porque `ADR-57(c)` —sellado— dice de ENOE exactamente lo contrario, y lo dice **citando como razón el mismo hallazgo** que `FP-64` usa como Razón 1:

> *«su panel rotativo queda refutado como ruta de conducta financiera (`CAL-ENOE` Fase A, 31/jul: el instrumento no trae reactivo de ahorro/crédito/deuda/planeación); **permanece elegible únicamente como portador de desenlaces laborales para experimentos naturales** (p. ej. salario mínimo de franja fronteriza).»*

`ADR-57(c)` separó las dos mitades a propósito: la ausencia de reactivo de θ refuta la ruta **(i)** —el panel, que necesita el desenlace *en el instrumento*— y **no toca la (ii)**, porque en un experimento natural la exposición la pone la **política**, no el cuestionario. Y el ejemplo que nombra es el mismo decreto del 1/ene/2019 que esta adquisición acaba de habilitar.

**Lo que el barrido descartó es a ENOE como fuente de exposición θ** —que ya estaba dicho desde el 31/jul y que este acto extiende de un constructo a los nueve y de una era a todas—, **no a ENOE de la llave (ii)**. Son dos cosas distintas, y sólo mesa puede decidir cuál gobierna, porque enmendar `ADR-57(c)` es firma suya. Las tres opciones están escritas en `FP-105`.

**Y esto es exactamente lo que la firma de mesa pedía.** *«No hicimos una estructura tan robusta para que el resultado sea por no adquirir»*: el dato está adquirido, registrado y verificado, la Razón 2 está cerrada por medición, y la llave (ii) vuelve a mesa con la adquisición hecha y con dos renglones ejercidos que nadie había contado — no como excusa.

---

## 8 · Lo que este acto NO hizo

No enmendó `ADR-57(c)` ni `ADR-67(c)`. No escribió ningún pre-registro de diseño sobre ENOE — adquirir no es diseñar, y `FP-105` gatea esa escritura. No leyó el `DOF` ni derivó los municipios de la franja fronteriza (se intentó; `dof.gob.mx` respondió `200` a la raíz pero la nota redirigió a otra fecha y el índice del día devolvió 0 coincidencias sobre **1** archivo descargado, que por `A.13` es un negativo sobre esa descarga y no sobre el `DOF`). No midió potencia: nada dice sobre si el `n` por municipio fronterizo sostiene un DiD. No cubrió los módulos temáticos anexos de la ENOE, que no viajan en el ZIP trimestral — hueco nombrado, no cerrado. No editó `bbis-adq-enoe-pre2019`, congelado antes de la primera descarga. No usó agentes: el acto entero corrió en una sola sesión, así que la instrucción de que fueran Sonnet no llegó a aplicarse.
