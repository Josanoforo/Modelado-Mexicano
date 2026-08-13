ENCARGO APERTURA-ISSP · los dos módulos con México, a nivel variable
SHA de redacción: b17a6f6 (merge #195) — derivado por git log -1 contra clon fresco, 13/ago/2026.
Entorno asignado: Ubuntu Claude Code, sesión con corpus. No usa red. NO Claude cloud (no tiene los bytes). NO lo lances mientras corran tres sesiones en la misma caja — ver §0.2.
Estado: CONSUMIDO — `PR #200` (rama `wt-apertura-issp-1786589980`, merge `19d885d`, ancestro confirmado de `fd788a9`). *Corrección de ACTO E2, 13/ago/2026: este archivo seguía marcado `VIVO` pese a estar fusionado; ver `forense/notas/2026-08-13-e2-cierre.md`.*

Archivado per forense/encargos/convencion.md (Regla A.3) como primer commit de este acto, antes de ejecutar el bloque de ARRANQUE.

---

**Nombre de archivo, desviado de §2 y declarado:** el encargo (§2, verbatim abajo) pedía este archivo en `forense/encargos/2026-08-13-apertura-issp.md` — mismo nombre base que `forense/notas/2026-08-13-apertura-issp.md`, en otro directorio. Esa colisión disparaba `T02` (`tests/check.py`) como FAIL nuevo contra `tests/baseline.json`, con dos entradas `T16` como eco del mismo corrimiento de conteo. Renombrado a `2026-08-13-AI-apertura-issp.md` (prefijo `AI-`, mismo mecanismo que ya usaron `forense/encargos/2026-08-13-A-censo-explotacion.md` y `forense/encargos/2026-08-13-A7-indice-infraestructura.md` el mismo día) tras confirmarlo con el usuario (VENTANA 1) — no decidido unilateralmente; este acto había reportado la colisión sin auto-otorgarse esa autorización. Verificado: con el renombre, `T02` deja de disparar y las dos entradas `T16` desaparecen con él — mismo mecanismo, no dos arreglos. Detalle completo en `forense/notas/2026-08-13-apertura-issp.md`, §12.

---

Texto completo del encargo, tal como se lanzó (verbatim, incluida la ruta original de este mismo archivo en §2 — no se edita el texto verbatim aunque la ejecución real haya desviado por la razón de arriba):

---

§0 · Por qué existe este acto, y qué NO lo bloquea
0.1 · Lo pidió el acto anterior, por escrito, y lleva dos días parado

forense/notas/2026-08-13-r2-registro-via-completa.md §4, verbatim:

"Las otras 6 necesidades quedan repartidas entre los módulos 2012 y 2017 (ambos con México presente) sin que el corpus haya distinguido antes cuál corresponde a cuál con precisión de item — eso excede lo que este acto puede cerrar sin abrir cada reactivo contra cada necesidad, y es justamente el trabajo de una apertura a nivel variable (M-APERTURA), no de este acto. Reportado a mesa."

Este acto es esa apertura.

0.2 · Las dependencias, verificadas una por una — solo una es real
Dependencia supuesta    Veredicto    Evidencia
"Espera a que ENLACE-1 fusione"    FALSA    El perímetro de ABRIR-4 (forense/encargos/2026-08-07-abrir-4.md) es exhaustivo y no incluye relaciones.tsv. Un acto de apertura escribe a su propio TSV fechado. Cero colisión con el Carril A.
"Hace falta un lector de .dta"    FALSA    ACTO R″ ya abrió los tres módulos con pandas.io.stata.StataReader; su nota declara que pip install no fue necesario.
"Tocar el lector cae bajo el congelamiento de motor"    FALSA y doblemente inaplicable    ADR-70(d) congela tools/curador_registro/. Este acto no toca tools/ ni tests/ — lee con script de scratch, como hizo R″.
"Hace falta que mesa firme algo"    FALSA    Ninguna firma pendiente sobre el mecanismo. Este acto no reabre ADR-52A/54 — eso sí es de mesa, con este reporte enfrente.
"Hay corpus en la máquina, y alcanza descargas_mx"    REAL — es el punto 3 del ARRANQUE    Los 16 payloads ISSP tienen raiz: descargas_mx, no data/raw. Se verifica distinto.
"Hay capacidad de caja"    REAL — y es de operación, no del encargo    3 OOM-kills el 12/ago (10:44:14, 13:29:57, 13:32:21), uno invocado por un proceso claude, con 15 GiB. Regla derivada: una sesión a la vez, dos como máximo. Si ENLACE-1 y SONDA-1 siguen corriendo, este es el tercero: espera a que cierre uno.
0.3 · Lo que ISSP trae y a ABRIR-4 le faltó

ABRIR-4 abrió ENSAFI 2023 y halló IMPULSIVID sin poder decir qué mide: "[SIN TEXTO DE REACTIVO — ENSAFI no trae diccionario en este corpus; nombre de columna derivada, hallada por lectura manual del encabezado]". ZA5900 trae 7 PDFs, incluido ZA5900_cdb.pdf (codebook, 5.97 MB), registrado y nunca abierto a nivel de contenido — R″ lo declaró explícitamente así para no sobre-afirmar.

§1 · Los payloads, con id exacto — no hay que buscarlos

Derivados del manifiesto en esta redacción (data/manifiesto.yaml, 554 entradas). Verifica hash una invocación por --id y pega la salida cruda de cada una. Las tres respuestas NO se colapsan: AUSENTE · raíz-no-configurada · hash-discordante.

ZA6980 — ISSP 2017 Social Networks and Social Resources · México N=1002 de 44,492 (c_alphan=MX, verificado en el dato real por R″)
id_manifiesto    archivo    bytes
za6980_q_mx    ZA6980_q_mx.pdf (cuestionario México)    247,978
za6980_backgroundvar_mx    ZA6980_backgroundvar_mx.pdf    220,092
za6980_v2_0_0_dta    ZA6980_v2-0-0.dta.zip → .dta 30,341,248 B    3,144,289
ZA5900 — ISSP 2012 Family and Changing Gender Roles IV · México N=1527 de 61,754 (C_ALPHAN, mayúsculas — esquema distinto, release más vieja)
id_manifiesto    archivo    bytes    abierto antes
za5900_cdb    ZA5900_cdb.pdf (codebook)    5,971,210    NO
za5900_q_mx    ZA5900_q_mx.pdf (cuestionario México)    228,950    solo portada
za5900_bq    ZA5900_bq.pdf (basic questionnaire)    500,702    NO
za5900_backgroundvar_mx    ZA5900_backgroundvar_mx.pdf    668,385    NO
za5900_mr    ZA5900_mr.pdf (methodology report)    319,274    NO
za5900_overview    ZA5900_overview.pdf    231,846    NO
za5900_questionnaire_development_report    idem .pdf    2,339,766    NO
za5900_v4_0_0_dta    ZA5900_v4-0-0.dta.zip    4,916,181    solo C_ALPHAN
FUERA DE ALCANCE, por declaración: ZA7600

za7600_v3_0_0_dta / za7600_v3_0_0_sav. ISSP 2019 Social Inequality V. México: 0 de 44,975 — MX nunca aparece, verificado en el dato real por R″. Ya clasificado EXISTE-NO-SATISFACE. No se abre, no se re-verifica, y N3 no se sirve desde ISSP — la cola liga N3 explícitamente a este módulo y el dato lo cierra. Si encuentras razón para reabrirlo, PARA y repórtala; no lo abras por completismo.

§2 · PERÍMETRO Y CONCURRENCIA

ESCRIBE: data/apertura-issp-variables-2026-08-13.tsv (nuevo) · forense/notas/2026-08-13-apertura-issp.md (1 nota) · forense/hallazgos.md (append, merge local siempre — el editor web de conflictos está prohibido) · forense/encargos/2026-08-13-apertura-issp.md (este archivo, A.3).

NO ESCRIBE: data/manifiesto.yaml · data/curacion-registro/** (incluido relaciones.tsv — es del Carril A) · data/universo-puertas-*.tsv (es de SONDA-1, que corre) · canon/** · milpa/** · tools/** · tests/** · forense/hitoD-preregistro-v2_0.md · forense/censo-estimabilidad-*.md · data/raw/** y la raíz descargas_mx (solo lectura).

Si te encuentras escribiendo fuera de la primera lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

En paralelo: ENLACE-1 (relaciones.tsv) y SONDA-1 (universo-puertas). Perímetros disjuntos salvo hallazgos.md, que es merge=union. GitHub no honra merge=union: aparecerá como conflicto en la interfaz y auto-resuelve limpio en local. Merge local siempre, main HACIA la rama.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

1 · REPO. Clon existente. Ruta absoluta · git log -1 --format="%h %s" · git status. No arranques desde el home. Worktree propio: wt-apertura-issp-$(date +%s).

2 · SHA. Base declarada b17a6f6. ENLACE-1 y SONDA-1 pueden haberlo movido. Refresca y reporta la diferencia. NO es PARO.

3 · CORPUS — este es el punto que sí puede parar el acto, y es distinto del de ABRIR-4. Los payloads ISSP no están en data/raw: tienen raiz: descargas_mx, que se resuelve por data/raices.local.yaml (gitignorado, no se hereda al crear worktree). Cópialo si falta. Verifica y reporta crudo:

bash
test -f data/raices.local.yaml && grep -c "descargas_mx" data/raices.local.yaml   # reporta el valor
python3 tests/manifiesto.py --verifica --id za5900_cdb                            # esperado: COINCIDE
python3 tests/manifiesto.py --verifica --id za6980_v2_0_0_dta                     # esperado: COINCIDE

Si la raíz descargas_mx no está configurada o los dos --verifica no dan COINCIDE: PARA — entorno equivocado. Este acto no descarga nada; no hay verificación de corpus compartido al cerrar.

4 · ENTORNO. Firma de tres partes, y aquí manda la tercera: echo "[$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE]" · la sonda de red no aplica, decláralo y salta · python3 -c "import pandas; print(pandas.__version__)" — R″ usó pandas.io.stata.StataReader sin instalar nada; si aquí falta, repórtalo antes de improvisar. Reporta los tres crudos.

5 · ESPEJO. Ninguna cifra del espejo del proyecto. Todo sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

§3 · COMMIT 1 — pre-registro: los términos ANTES de abrir nada
3.1 · La rejilla

7 necesidades × 2 módulos = 14 celdas. Las 7 se copian verbatim de la columna necesidad de data/abrir4-variables-2026-08-08.tsv (derívalas del archivo, no de este encargo; si difieren, reporta la diferencia y usa las del archivo):

3.11 sens_estatus (G2,G4) · 4.6 aversion_riesgo (G2,G3) · 10 horizonte_temporal (G4) · 12 familismo_apoyo (no-ENIF) · 13 familismo_obligacion · 14 puente radio_confianza · theta subjetivos (ENBIARE-like)

3.2 · Los términos de búsqueda, por necesidad, escritos antes de abrir

Uno por necesidad, en inglés y español (los codebooks GESIS son en inglés; los cuestionarios _q_mx en español). Deriva los términos del texto de la necesidad y del censo (forense/censo-estimabilidad-coeficientes-v1_0.md §5, filas correspondientes) — no de memoria.

3.3 · El universo de apertura, declarado por módulo (A.4)

Qué se va a leer y en qué orden. Propuesta: documentación primero, microdato después — el codebook dice qué mide una variable; el .dta solo dice que existe. Para ZA5900: cdb → q_mx → bq → backgroundvar_mx → .dta. Para ZA6980: q_mx → backgroundvar_mx → .dta. Si inviertes el orden, di por qué.

3.4 · Lo que R″ ya vio de pasada, y hay que confirmar o desmentir

R″ leyó solo la portada de ZA5900_q_mx.pdf y reportó tres ítems sin buscarlos:

V27 — "Adult children are important source of help for elderly parents"
V35 / V36 — provisión y costo del cuidado a mayores

Y concluyó que ZA5900 es el candidato más directo de los tres módulos para familismo_obligacion, más que ZA6980. Eso es una observación de portada, clase (3): se verifica contra el codebook en este acto, no se hereda. Si V27 no dice eso, ese es el hallazgo.

3.5 · Pre-registro de falsación (B-bis) — qué significa NO encontrar

Escrito antes de ver el dato, porque después no vale:

La tasa base está medida y es baja. ABRIR-4 cerró 13 de 28 celdas en NO-ENCONTRADO, 11 EXISTE-NO-SATISFACE y solo 4 EXISTE-SATISFACE. Una corrida que vuelva con 2 o 3 celdas útiles de 14 está dentro de lo esperado y no es un fracaso.
Si una necesidad vuelve NO-ENCONTRADO en los dos módulos: eso acota, no refuta. Se escribe con universo + términos + fecha en la misma línea, y cierra la pregunta "¿ISSP sirve para esto?" con evidencia, que es más de lo que hay hoy.
Si 14 puente radio_confianza vuelve con desenlace_coobservado_en_mismo_instrumento = SÍ: ese es el resultado más interesante que este acto puede producir, y hay que decirlo ahora para que el ejecutor no lo lea como ruido. La fila 14 es uno de los dos huecos estructurales del censo (filas 10 y 14) — los que el propio censo declara que no se arreglan bajando más de lo mismo, exigen fuente nueva o puente. ZA6980 es "Social Networks and Social Resources": confianza y apoyo social ante dificultad, un solo cuestionario, una sola muestra. Si los dos están ahí, el hueco estructural se cierra por puente, y eso pesa más que cualquier contador de este programa.
Precedencia, declarada al sellar: si una celda satisface EXISTE-SATISFACE por documentación pero el .dta no trae la variable, manda el .dta — el codebook describe el instrumento internacional, el archivo trae lo que México respondió. Se anota la discrepancia, no se colapsa.
3.6 · La reserva que este acto no puede saltarse

Co-observación limpia NO es identificación. ABRIR-4 ya lo escribió en una de sus 28 filas, verbatim: "co-observacion limpia = asociacion, no identificacion, sin llave ADR-57(c): no es panel, no hay grupo de comparacion de experimento natural, no es diseno experimental de terceros". ISSP es transversal. Encontrar reactivo y desenlace en la misma muestra habilita una asociación; llamarla coeficiente identificado sería meter un número falso al ejecutable. La columna llave_ADR57c se llena Ninguna salvo que exista evidencia de lo contrario, y no la hay.

Cierra el commit con: "el primer resultado que produzca este procedimiento es el que se reporta."

§4 · COMMIT 2 — los veredictos

No edita el commit 1. Si la especificación estaba mal, un tercer commit lo dice; nunca se corrige hacia atrás.

Produce data/apertura-issp-variables-2026-08-13.tsv con el contrato exacto de abrir4-variables, 14 columnas, mismo orden (derívalo del encabezado del archivo, no de este encargo):

instrumento · id_manifiesto · sha256_verificado · necesidad · variable_encontrada ·
texto_del_reactivo · escala · tabla · n_filas ·
desenlace_coobservado_en_mismo_instrumento · es_panel · llave_ADR57c ·
clasificacion_a4 · universo_declarado

Por celda:

texto_del_reactivo — texto literal del codebook o del cuestionario, con el archivo y la página. Si no hay texto, se escribe entre corchetes por qué, como hizo ABRIR-4. Un nombre de columna sin texto no es un reactivo.
escala — valores observados en el .dta, con el comando. Dirección y sentido solo si la documentación los declara.
n_filas — el N de México, no el N del archivo internacional. ZA6980 = 1002, ZA5900 = 1527, y se re-deriva, no se copia de aquí.
desenlace_coobservado_en_mismo_instrumento — la columna que decide la fila 14. SÍ solo si reactivo y desenlace están en la misma tabla y la misma muestra México, con las dos variables nombradas.
es_panel — NO, con la inferencia estructural declarada (ISSP es transversal repetido; los módulos son estudios distintos, no olas del mismo).
clasificacion_a4 — vocabulario cerrado: EXISTE-SATISFACE / EXISTE-NO-SATISFACE (y qué falta) / NO-ENCONTRADO (dónde y con qué términos). Las palabras "no existe", "inexistente" y "no hay fuente" están prohibidas.
universo_declarado — qué se examinó, con qué mecanismo, en qué fecha. En la misma línea. Si no cabe en una línea, la clasificación no está lista.

Suite ×3 antes del push (el molde de ABRIR-4, y la tercera es la que atrapó el T03 que rompió PR #154):

con corpus enlazado
con data/raw desenlazada
con los gitignorados de config retirados (data/raices.local.yaml, data/secretos.local.yaml)

T03: no cites archivos gitignorados entre backticks en la nota. --baseline debe seguir VERDE contra e7cd99d. Si un test truena, ese es el hallazgo — no se maquilla.

§5 · QUÉ NO HACE ESTE ACTO
No reabre ADR-52A ni ADR-54. Eso es de mesa, vía E-CE v1.1, con este reporte enfrente.
No toca relaciones.tsv. Ni capa2, ni capa4, ni id_manifiesto. El acto que propague estos veredictos al registro es posterior y tiene su propio perímetro.
No calcula ningún β ni ninguna θ. Encuentra reactivos y declara co-observación. Estimar es otro acto, con su propio pre-registro.
No abre ZA7600. México = 0, verificado.
No promete destrabar los tres SIN-RUTA. La fila 13 del censo está bloqueada por otra razón —es el único de los 15 coeficientes sin magnitud asignada, solo dirección hipotética bajo ADR-30— y ningún reactivo la desbloquea por sí solo. Las filas 12 y 14 sí son alcanzables. Decir esto antes de correr es lo que impide que el acto se lea como fracaso si vuelve con dos de tres.
§6 · CONTADOR

Celdas de la rejilla 7 × 2 con clasificación A.4 derivada de apertura byte a byte, y — el titular si ocurre — si 14 puente radio_confianza vuelve co-observada en un solo instrumento.

Y la línea honesta al cierre: este acto no mueve capa2, ni Hito D, ni llaves. Mueve la única cosa que hoy impide que ISSP sirva para algo: saber qué reactivo hay dentro.
