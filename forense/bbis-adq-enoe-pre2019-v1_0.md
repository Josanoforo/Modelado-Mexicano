# ADQ-ENOE-PRE2019 · Ficha B-bis — el barrido pre-registrado y el plan de adquisición, congelados antes de abrir ningún ZIP pre-2019

### `bbis-adq-enoe-pre2019` · **v1.0** · 20 de agosto de 2026 · **COMMIT A — ESPECIFICACIÓN CONGELADA**

> | | |
> |---|---|
> | **ARCHIVO** | `bbis-adq-enoe-pre2019-v1_0.md` |
> | **NOMBRE ESTABLE** | **`bbis-adq-enoe-pre2019`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La ficha B-bis del `ACTO ADQ-ENOE-PRE2019`, que ejecuta la opción **(b)** de `FP-64` (firma de mesa verbatim: *«B2 (no hicimos una estructura tan robusta para que el resultado sea por no adquirir)»*). Congela **antes** de descargar nada: qué olas se adquieren y por qué criterio (§2), con qué términos se barren los 9 constructos (§4), qué cuenta como acierto y qué no (§5), y qué desenlace del barrido significa qué (§6) |
> | **QUÉ NO ES** | No adjudica ningún veredicto de Hito D · no mueve `13 de 27` · no sella ninguna llave de identificación nueva · no escribe un pre-registro de diseño para ENOE (adquirir no es diseñar) · no cierra `FP-64`, que es firma de mesa |
> | **VERIFICAS ASÍ** | §4 enumera **todos** los términos del barrido, fijados antes de abrir un solo cuestionario pre-2019 · §5 cierra el vocabulario de veredicto con `A.4` · §6 declara los dos desenlaces posibles y qué hace cada uno con la llave (ii) · §7 declara el falsador y lo que este acto NO puede concluir |
> | **ESTADO** | **CONGELADO.** COMMIT B no edita este archivo. Si la especificación estaba mal, lo dice un commit posterior — nunca se corrige hacia atrás |

---

## 0 · Contaminación de esta sesión — declarada antes que nada

**Lo que esta sesión YA vio antes de congelar esta ficha, y es contaminación real:** el veredicto del barrido *moderno*. `data/coef-universo-v1_0.tsv:14` (fila `TODOS-LOS-15`) dice, sobre los **6 cuestionarios post-2019 que sí están en disco**, `NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO`, con la razón escrita: *«ahorro, credito, deuda y riesgo SI aparecen, pero solo como prestacion laboral (caja de ahorro, credito Infonavit) o como razon de cierre de negocio; nunca como bateria de actitud o planeacion»*. `FP-64` lo repite como su Razón 1.

**Por qué esa contaminación es grave aquí y cómo se acota.** Sé la respuesta que dio el instrumento moderno. Si escribiera los términos *después* de mirar los cuestionarios viejos, podría —sin querer— elegirlos para reproducir el resultado que ya conozco. Por eso §4 los fija ahora, y por eso son **más anchos** que los que el veredicto moderno necesitaría: incluyen deliberadamente términos que el barrido moderno **no** reporta haber probado (el script que lo produjo, `scratchpad/enoe_pdf_scan.py`, **nunca se commiteó** — verificado: `git log --all -- '*enoe_pdf_scan*'` sale vacío, así que sus términos exactos son irrecuperables y este barrido **no puede** heredarlos, solo re-derivarlos).

**Lo que esta sesión NO había abierto al congelar esta ficha:** ningún cuestionario ENOE anterior a 2019, ningún diccionario de datos pre-2019, ningún ZIP de microdato pre-2019 — ninguno existe todavía en `data/raw` (verificado en §1). El barrido de §4 corre contra material que al momento de congelar esta ficha **no está en el árbol ni en el disco**.

---

## 1 · A.8 — lo que ya está, verificado por comando antes de bajar nada

`A.8` existe porque `ACTO R`/`ACTO R″` bajaron lo que ya estaba y produjeron entradas duplicadas bajo ids distintos, lo que obligó a retractar un acto el 12/ago/2026. Comandos corridos contra el árbol de este worktree, **antes** de la primera descarga:

| pregunta | comando | salida |
|---|---|---|
| ¿hay ids ENOE pre-2019 en el manifiesto? | `re.findall(r'^- id: (\S+)', manifiesto)` filtrado por `enoe` y por año `2005`-`2018` | **1**: `enoe_con_basedatos_proy2010_pdf` — un PDF de metodología, no microdato |
| ¿hay payloads ENOE pre-2019 en disco? | `ls /home/pc0/mm-corpus/raw \| grep -i enoe` | **29 archivos, ninguno pre-2019** — 28 `conjunto_de_datos_enoe*_20{19..26}_*t_csv.zip` más `enoe_n_trim3_2020-trim4_2022.zip` |
| ¿cuántos ids ENOE hay en total? | mismo comando sin filtro de año | **37** |

**Conclusión de A.8: ninguna de las 12 olas que §2 manda adquirir existe hoy, ni en `data/manifiesto.yaml` ni en el corpus compartido.** Cero riesgo de duplicado bajo id distinto. Confirma, por comando propio y no por herencia, la Razón 2 de `FP-64` (*«no hay ola de microdato ENOE anterior a 2019 T1 en disco… el único pre-2019 es un PDF de metodología»*) — con una precisión de cifra: `FP-64` dice **36 payloads**, este conteo da **29 archivos ENOE en `data/raw`** y **37 ids ENOE en el manifiesto**; las tres cifras cuentan poblaciones distintas (archivos en disco vs. ids del manifiesto vs. lo que contara `FP-64`) y ninguna refuta a la otra, pero **la cifra de `FP-64` no se reproduce con ninguno de los dos conteos de arriba** y queda declarada como discrepancia, no resuelta por este acto.

---

## 2 · Qué olas se adquieren, y el criterio — fijado antes de bajar

**El corte.** El decreto de estímulos fiscales para la **Región Fronteriza Norte** (Zona Libre de la Frontera Norte) rige **desde el 1/ene/2019**. El antes/después que `FP-64` opción (b) manda habilitar necesita, por tanto, olas **anteriores** a `2019T1` — y las posteriores ya están en disco (`2019T1`…`2026T1`, con el hueco de `2020T2`, que es la suspensión de la ENOE por la pandemia).

**Criterio de selección, declarado:** se adquieren **12 trimestres consecutivos, `2016T1`–`2018T4`**, porque:

1. **Los 4 inmediatamente adyacentes al corte (`2018T1`–`2018T4`)** son el período pre indispensable: sin ellos no hay antes/después de ninguna clase.
2. **Los 8 anteriores (`2016`–`2017`)** son lo que permite *probar* tendencias paralelas en vez de suponerlas. No es adorno: la reserva sellada de `R5.1-D3` en `forense/registro-llaves-identificacion-v1_0.md` §3 dice, verbatim, que *«el supuesto de tendencias paralelas está escrito y **no verificado** — el placebo 2014→2018 sigue sin correr»*. Adquirir sólo el período adyacente reproduciría en ENOE exactamente esa deuda.
3. **Se corta en 2016 y no antes** porque 12 trimestres pre bastan para un placebo de 8 contra un pre de 4, y porque cada ola adicional cuesta ~30 MB de corpus compartido sin cambiar qué se puede probar. Las olas 2005–2015 quedan **disponibles y no adquiridas**, declarado aquí para que no se lea como que no existen: el índice las trae completas (§3).

**Anticipación.** El decreto **rige desde el 1/ene/2019** (premisa del encargo, no re-derivada aquí: este acto **no leyó el `DOF`** — se intentó, `dof.gob.mx` respondió `200` a la raíz pero la nota buscada redirigió a otra fecha y el índice del 31/dic/2018 devolvió 0 coincidencias sobre **1** archivo descargado, que por `A.13` es un negativo sobre esa descarga, no sobre el `DOF`). Un decreto que rige el 1/ene fue público antes de esa fecha, así que `2018T4` es un trimestre potencialmente contaminado por anticipación **sin necesidad de fijar la fecha exacta de publicación**. No se excluye de la adquisición —excluirlo de la *adquisición* sería decidir el diseño desde el almacén— pero se declara aquí, antes de bajarlo, para que cualquier diseño posterior tenga que decir si lo usa o lo tira.

**Formato:** `csv`. Es el formato de los 28 payloads ENOE post-2019 ya en disco (`conjunto_de_datos_enoe_YYYY_Nt_csv.zip`); `dbf`/`dta`/`sav` existen en el índice y **no** se adquieren.

**Distribución: `/microdatos/`, uniforme para las 12 olas.** INEGI sirve la ENOE por dos rutas distintas y este acto midió las dos (§3). La razón de elegir `/microdatos/` está en §3 y es un hallazgo, no una preferencia.

**Puente de distribución, 1 payload extra.** Se adquiere **además** `2018T4` por la ruta `/datosabiertos/` — la misma ola en los dos empaquetados. Cuesta ~42 MB y convierte en **medición** lo que si no sería un supuesto: si las dos rutas sirven las mismas tablas y las mismas variables, se comprueba comparando esa ola contra sí misma, no afirmándolo.

**Total pre-registrado: 13 payloads** (12 microdatos csv + 1 datosabiertos csv).

---

## 3 · Los dos caminos de INEGI, y el hoyo medido en uno de ellos

`data/indice-descarga-masiva-2026-08-05.tsv` sólo registra la ruta `/microdatos/`. La ruta `/datosabiertos/` —de la que vinieron **todos** los payloads ENOE post-2019 que hoy están en disco, según `url_origen` en `data/manifiesto.yaml`— es **invisible en ese índice**. Sondeadas hoy las dos con `curl -r 0-0` (petición de rango, nunca `curl -I`), contra `www.inegi.org.mx`:

| ola | `/datosabiertos/` | `/microdatos/` |
|---|---|---|
| `2016T1`–`2016T4` | `206`, zip real | `206`, zip real |
| `2017T1`–`2017T4` | **`200`, `text/html`, 2263 bytes — soft-404** | `206`, zip real |
| `2018T1`, `2018T2` | **`200`, `text/html`, 2263 bytes — soft-404** | `206`, zip real |
| `2018T3`, `2018T4` | `206`, zip real | `206`, zip real |
| `2005T1`, `2010T1`, `2013T1`, `2014T1`, `2015T1` | `206`, zip real | `206`, zip real (índice) |

**El hoyo: `/datosabiertos/` no sirve ninguna ola de 2017 ni `2018T1`/`2018T2` — seis trimestres, y caen justo sobre el borde del decreto.** No es un 404 honesto: es el `200` de INEGI que ya está medido en este proyecto como soft-404 (`ACT-PIL-2`, `ADR-130`). Un acto que hubiera supuesto «bajo todo por donde vinieron los de 2019» habría obtenido seis páginas HTML de 2263 bytes con nombre de `.zip`, y sólo un `sha256` contra tamaño lo habría delatado.

**Por eso se elige `/microdatos/`:** es la única ruta **completa** sobre el período pre, y la uniformidad *dentro* del período pre manda sobre el parecido con el período post — un DiD sobre transversales repetidas compara estimaciones entre olas del pre y del post, y una discontinuidad de empaquetado *dentro* del pre es la que rompe la comparación. La comparabilidad pre↔post **no se afirma aquí: se mide** en COMMIT B con el puente de `2018T4` (§2).

---

## 4 · El barrido — los 9 constructos y sus términos, congelados

**Los 9 constructos** son los de `milpa/procedencia.yaml:270-281` tras los 15 coeficientes, tal como `forense/hitoE-campana-medicion-v2_0.md:247` los enumera: `aversion_riesgo`, `confianza_institucional`, `deferencia`, `exposicion_violencia`, `familismo_apoyo`, `familismo_obligacion`, `horizonte_temporal`, `radio_confianza`, `sens_estatus`. Por `ADR-28.b`, `confianza_institucional` **no es escalar**: es un vector de 6 componentes, así que el barrido reporta **14 filas**, no 9.

**Normalización, fijada:** minúsculas, acentos plegados (`á→a`…), búsqueda por subcadena. Un término escrito aquí sin acento empareja la forma acentuada del documento y viceversa.

| # | fila | términos pre-registrados |
|---|---|---|
| 1 | `aversion_riesgo` | riesgo · arriesg · incertidumbre · apost · azar · loteria · sorteo · garantizado · asegurad · seguro de · preferiria · perdida · precautorio |
| 2 | `confianza_institucional[seguridad]` | policia · ejercito · marina · guardia nacional · seguridad publica |
| 3 | `confianza_institucional[educacion]` | escuela · maestro · profesor · sep · educacion publica |
| 4 | `confianza_institucional[salud]` | imss · issste · hospital · clinica · centro de salud · medico · seguro popular · insabi |
| 5 | `confianza_institucional[electoral]` | ine · ife · eleccion · partido politico · voto · campana electoral |
| 6 | `confianza_institucional[justicia-policia]` | juez · ministerio publico · tribunal · fiscalia · denuncia · juzgado |
| 7 | `confianza_institucional[financiera]` | banco · banca · afore · caja de ahorro · sofom · cooperativa de ahorro · financiera |
| 8 | `deferencia` | obedec · autoridad · jerarqui · acatar · permiso de · jefe · mandar · sumis · respetar a |
| 9 | `exposicion_violencia` | violencia · delito · robo · asalto · agresion · inseguridad · victima · amenaza · extorsion · homicidio · secuestro · golpe |
| 10 | `familismo_apoyo` | ayuda de · apoyo de · pariente · familiar · remesa · red de apoyo · presta · cuidado de · se hacen cargo |
| 11 | `familismo_obligacion` | obligacion · deber de · mantener a · responsable de · cuidar a · hacerse cargo · sostener a · manutencion |
| 12 | `horizonte_temporal` | ahorr · futuro · plazo · planea · planific · jubilac · retiro · pension · afore · prevision · meta · proyecto de vida |
| 13 | `radio_confianza` | confia · confianza · vecino · desconocido · extrano · comunidad · la mayoria de la gente · amistad |
| 14 | `sens_estatus` | estatus · posicion social · prestigio · clase social · nivel socioeconomico · apariencia · que diran · respetad · vergüenza · pena |

**Dos universos, no uno — y el segundo es más fuerte que el primero.**

- **Universo A · cuestionarios.** Los cuestionarios de la ENOE vigentes en el período `2016`–`2018`, texto completo extraído. Es lo que `FP-64` barrió para el instrumento moderno, y es lo que el encargo nombra.
- **Universo B · diccionarios de las olas adquiridas.** Nombres y etiquetas de variable de las 12 olas de §2, leídos de los propios ZIP. **Es evidencia más fuerte que A**: si una variable existe en el dato, existe — no depende de que el PDF del cuestionario que se encontró sea el de la versión correcta de ese año. `FP-64` no lo corrió; este acto sí.

Ambos universos se declaran con su cardinalidad (`A.13`: *un negativo producido por un comando que no examinó archivos no es un negativo*) — cuántos archivos, cuántos caracteres, con el comando a la vista.

---

## 5 · Qué cuenta como acierto — vocabulario cerrado de `A.4`

La pregunta del barrido **no** es «¿aparece la palabra?». `FP-64` ya sabe que aparecen: la Razón 1 dice que `ahorro`, `credito`, `deuda` y `riesgo` **sí** aparecen en los cuestionarios modernos, y aun así ENOE queda descartado. La pregunta es si aparecen **como EXPOSICIÓN θ** — un rasgo o disposición del sujeto que el motor pueda usar como variable independiente — o sólo como **DESENLACE** / atributo administrativo.

| veredicto | significa | ejemplo del propio `FP-64` |
|---|---|---|
| `EXISTE-SATISFACE` | el reactivo mide una **disposición, actitud, preferencia o plan** del sujeto, con universo poblacional y no restringido a un subgrupo por diseño de la pregunta | una batería tipo «¿qué tanto confía usted en…?» o «¿prefiere X seguro o Y incierto?» |
| `EXISTE-NO-SATISFACE` | el término aparece, pero como **prestación laboral**, **razón administrativa**, **boilerplate legal**, o **hecho de universo restringido** | *«caja de ahorro»*, *«crédito Infonavit»* (prestación); *«razón de cierre del negocio»* (desenlace); Art. 45 de la Ley del SNIEG (boilerplate) |
| `NO-ENCONTRADO` | el término no aparece en el universo examinado — **con el universo declarado** (`A.13`) | — |
| `NO-ACCESIBLE` | el material del período no se pudo obtener | — |

**Regla de precedencia, declarada al sellar y no después:** si una misma fila tiene aciertos de dos clases, gana `EXISTE-SATISFACE` — basta **un** reactivo utilizable como exposición para que la fila cuente como cubierta. La fila cae a `EXISTE-NO-SATISFACE` sólo si **todos** sus aciertos son de esa clase.

---

## 6 · Los dos desenlaces, declarados antes de ver el dato

`B-bis` exige decir qué pasa si el falsador **no** refuta. Aquí el falsador es el barrido y lo que estaría refutando es la Razón 1 de `FP-64`.

**Desenlace 1 — alguna de las 14 filas sale `EXISTE-SATISFACE`.** La Razón 1 **no se sostiene para el instrumento pre-2019**: las olas viejas traen lo que las nuevas no. ENOE recupera candidatura viva para la llave (ii) con exposición nombrada, la adquisición de §2 pasa de precaución a insumo, y lo que vuelve a mesa es una propuesta de diseño, no una excusa. **Este acto NO escribiría ese diseño** — nombrar la exposición no es pre-registrar un DiD — pero sí diría exactamente qué reactivo, en qué ola y en qué cuestionario.

**Desenlace 2 — las 14 filas salen `EXISTE-NO-SATISFACE` o `NO-ENCONTRADO`.** La Razón 1 **se extiende al instrumento pre-2019** y ENOE queda **descartado por Razón 1 con universo declarado** — que es, verbatim del encargo, *«eso es el entregable»*. La adquisición **no se retracta**: la Razón 2 de `FP-64` queda cerrada por medición (las olas existen y están registradas), de modo que si mesa admite otro corte natural sobre ENOE, o si un acto futuro encuentra la exposición en un módulo que este barrido no cubrió, el dato ya está en el corpus y no hay que volver a pedir permiso para bajarlo. La llave (ii) vuelve a mesa **sin candidato de exposición en ENOE** y con la adquisición hecha.

**Interesante bajo corroboración, dicho antes de ver el dato:** el Desenlace 1 sería el más informativo de los dos — sería la primera vez en este programa que un instrumento pierde capacidad de medición entre versiones, y convertiría *«la ENOE no mide actitudes»* de propiedad del instrumento en propiedad de **una versión** del instrumento. El Desenlace 2 es el esperado a priori (la ENOE es una encuesta de ocupación y empleo, no de actitudes) y por eso mismo el que más se parece a confirmar lo que ya se creía — es donde hay que vigilar el sesgo, no en el otro.

---

## 7 · Falsador, y lo que este acto NO puede concluir

**Falsador del barrido:** que exista, en cualquiera de los dos universos, un reactivo o variable que mida una disposición del sujeto en alguno de los 9 constructos. Un solo acierto de esa clase refuta el Desenlace 2.

**Lo que este acto no puede concluir, escrito antes de correr:**

1. **Un `NO-ENCONTRADO` no prueba que la ENOE nunca lo midió.** Prueba que no está en el universo examinado. La ENOE ha tenido módulos temáticos anexos (`ENOE`+módulo) que no viajan en el ZIP trimestral; si el barrido sale negativo, ese hueco queda **nombrado, no cerrado**.
2. **Adquirir no es diseñar.** Ninguna fila del registro de llaves nace en este acto. `FP-64` opción (b) dice *«adquirir olas ENOE pre-2019 y mantenerlo»* — mantener la candidatura no es sellar la llave.
3. **El decreto no se verifica aquí.** Este acto no lee el `DOF`, no deriva los 43 municipios de la franja fronteriza, y no fija el grupo de tratamiento. Eso es diseño, y es lo que vuelve a mesa.
4. **El barrido no mide potencia.** Que un reactivo exista no dice si su `n` sostiene un DiD por municipio fronterizo. Nada de eso se estima en este acto.

---

## 8 · Contadores que este acto mueve

**Ninguno de los contadores de medición sobre México se mueve.** Ni `13 de 27` (Hito D), ni `15 coeficientes, cero medidos`, ni `9 de 14`, ni `4 de 144`.

**`Llaves de identificación ejercidas: 2 de 3`** — el contador que `ADR-67(c)` abrió — se examina en §3 del registro por el `T3` de este acto (adjudicación de clase de `R5.1-D2` contra la taxonomía de tres clases de `ADR-57(c)`). **Adjudicar la clase de una fila existente no cambia su `estado`**, y el numerador y el denominador de `T24` se derivan **sólo** de la columna `estado`. La cifra prevista al congelar esta ficha es, por tanto, **`2 de 3` → `2 de 3`**, sin movimiento; COMMIT B la deriva con la receta de §4 del registro y la reporta aunque no se mueva.
