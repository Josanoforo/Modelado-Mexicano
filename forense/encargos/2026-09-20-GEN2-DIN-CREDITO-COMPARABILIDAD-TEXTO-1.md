# ENCARGO · ACTO GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1

**Archivado verbatim por 0-bis A.3 el 20/sep/2026.** Texto recibido de dirección pegado en la sesión, sin editar. Dirección depositó en `descargas_mx` sólo `2026-09-20-GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1.md.sha256` (`73c074de6486be46aa58494924c3677b03256ade87ab93763f9095175ea8054b`) y no el `.md`; el archivo de abajo es el texto pegado (tablas aplanadas por el pegado), así que su sha256 no coincide con el declarado. Se declara, no se colapsa.

---

ENCARGO · ACTO GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1 · al cerrar existe la tabla que dice, conducta por conducta y ola por ola, si la sección de crédito de ENIF pregunta lo mismo — y con qué unidad

ENTORNO: CAJA — el hook de arranque imprime ENTORNO-DERIVADO. Si no dice CAJA, PARA en una línea. La descarga por id en nube todavía no existe y este acto vive de PDF y hojas de cálculo del corpus montado.

CABECERA · SHA de redacción bd9ed213 (origin/main al redactar; 8d639a01, el que cita mesa, es su ancestro — verificado con git merge-base --is-ancestor); re-deriva al abrir, y si main se movió no es PARO · una sola sesión, rama propia · MODELO: Opus (hay juicio de comparabilidad en cada fila; no es receta) · MODO: ABIERTO, con un núcleo RÍGIDO declarado — toda lectura de ENIF 2024 se limita a cuestionario, FD y modelo de datos; abrir cualquier miembro de datos de 2024 es PARO (§7 a). No hay código congelado que heredar, así que el PARO (g) no aplica · CONTADOR: cuenta_gen2 = NO-APLICA — este acto no sella ninguna corrida y no debe mover N_corridas_selladas, N_resultados_* ni adoptados_activos. Lo que mueve es una tabla nueva registrada y sus NC/FP · CALC-id reservado: ninguno · FP/ADR/NC: deriva al cierre, no heredes (máximos al redactar: FP-401, NC-0422, ADR-567).

1 · OBJETIVO

Que exista data/credito-comparabilidad-texto-v1_0.tsv: 8 conductas (K1–K8) × 5 olas de ENIF (2012, 2015, 2018, 2021, 2024) = 40 filas, cada una con su veredicto de comparabilidad, su unidad (persona / producto de crédito) y su universo poblacional, leídos del texto de la pregunta y del flujo del cuestionario, nunca del nombre de la variable.

Esto habilita el paso siguiente del dominio y hoy es su cuello de botella: ninguna conducta de crédito tiene piso, porque nadie ha medido los marginales de crédito de ENIF 2021, y no se pueden medir sin saber antes qué es comparable con qué.

«Hecho» significa: un comando cuenta 40 filas de datos, 0 celdas vacías en las columnas obligatorias, y cada fila cuyo veredicto no sea NO-VERIFICABLE-AQUÍ trae la cita literal del reactivo (o el texto buscado y las secciones recorridas, si el veredicto es negativo). Más la nota, la fila en INFRAESTRUCTURA y el test cableado en CI.

2 · FIRMAS DE MESA

Verbatim, 20/sep/2026, conversación de dirección PRODUCTO-DINERO:

ORDEN — «Primero el encargo de comparabilidad por texto de crédito. El piloto de ahorro después.»

D2 — «2018 entra a la serie de crédito solo donde el texto de la pregunta lo permita; se acepta por adelantado que varias conductas cierren NO-CONSTRUIBLE en 2018, con la cita del texto buscado (A.15).»

D3 — «Se admiten como ejes de segmento rechazo de crédito, requisitos y bancarización, si la lectura por texto confirma que ENIF los pregunta. ADR-35 se respeta: el motor no modela al prestamista. FP-61 no se toca aquí.»

RESERVA — «La sección de crédito de ENIF 2024 queda RESERVADA desde hoy, con el hueco declarado: el par "crédito por app" (n=200) está visto y consumido; no se relanza sobre él.»

ALCANCE v0 (19–20/sep) — «Confirmo el alcance v0 y en paralelo medimos crédito.»

LISTA K1–K8 — aprobada por mesa el 20/sep como lista cerrada del dominio crédito, con la partición de K4 y la no-fusión de empeño con gota a gota como sus dos piezas de más valor.

3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
[EJECUTADO] data/manifiesto.yaml tiene las cinco olas de ENIF. Cuestionario solo en 2018, 2021 y 2024 (enif2018_cuestionario_pdf, enif2021_cuestionario_pdf, enif2024_cuestionario_pdf). Para 2012 y 2015 hay FD, modelo de datos y bases (dbf/sav) y NO hay cuestionario: grep -oE "enif[a-z0-9_]*cuestionario[a-z0-9_]*" data/manifiesto.yaml | sort -u devuelve seis ids, los tres pares de 2018/2021/2024 y ninguno más.
[LEÍDO] forense/prereg-caja/ENIF-FINTECH-SERIE-spec-v1_0.md:17-20: 2018 es NO-ESTIMABLE para cuenta y crédito fintech — las baterías enumeran productos tradicionales y «otro», no hay categoría por Internet/aplicación, no se pregunta el canal del último producto, y la población es 18–70 frente a 18+ en 2021/2024. 2021 crédito usa P6_2_8 y canal P6_7, comparable con P6_2_8 × P6_6 de 2024 por texto nuclear y catálogo. De 2024 «sólo se reproduce puntualmente crédito/app para falsar una receta equivocada».
[EJECUTADO] Ese es el único sitio del repo donde se abrió la sección de crédito de ENIF. Universo: 100 specs humanas en forense/prereg-caja/ + 166 spec.yaml en data/corrida0/. grep -rln "P6_" devuelve 9 archivos; 4 son ENSAFI, 2 son ENCUCI (AP6_, cívico), 2 son la pareja ENIF-FINTECH-SERIE / CALC-ENIF-FINTECH-0001. Ninguna spec cubre K1–K8.
[EJECUTADO] De los 580 encargos archivados en forense/encargos/, uno solo menciona ENIF y crédito a la vez (2026-08-25-R34-BC-MECANISMO.md), y ninguno hace comparabilidad por texto de ENIF.
[LEÍDO] NC-0304 (piloto 1, forense/encargos/2026-09-16-GEN2-CELDA-D-PILOTO-1.md:34): P5_6_k mide tenencia de tarjeta de débito en 2021 y conducta de ahorro en 2024; el equivalente verbatim de 2021 es P5_7_k. El piloto paró con cero emisiones. El defecto que este encargo previene ya costó una sesión en ahorro.
[LEÍDO] forense/notas/nota-2026-09-20-gen2-celda-d-piloto-3-ejecucion-paro.md §2: el molde de la tabla de tres columnas (redacción · opciones y códigos · filtro, flujo y catálogo) y el vocabulario MISMO-INSTRUMENTO / CAMBIO-MENOR / CAMBIO-DE-INSTRUMENTO, con la exigencia de decir por qué lo que cambió no entra en el estimando. Se reutiliza aquí tal cual.
[REPORTADO] (mesa, censo de NUBE-MEDICIÓN, 20/sep) los 37 payloads del dominio están en INEGI con URL directa y licencia libre, 381.6 MB; ENIGH 2024 no está en el corpus. No uso ninguna de estas dos líneas como premisa de funcionamiento: este acto no descarga nada.
[REPORTADO] de los tres reportes del corpus, las hipótesis de partida de K1–K8 (37.3% con crédito formal; departamental 22.6% > bancaria 15.7%; «no le gusta endeudarse» 38.4% y «no le interesa» 25.8%; 27.3% de endeudados con atraso en ENSAFI 2023). Son hipótesis, no mediciones nuestras, y no se usan para validar ninguna lectura de texto. Si una cifra del reporte contradice lo que dice el cuestionario, manda el cuestionario.
[SUPUESTO] que las cinco olas tienen una sección de crédito identificable como tal. Si resulta falsa para alguna ola —por ejemplo, si 2012 reparte crédito entre varias secciones o no lo separa de ahorro— eso no es PARO: se declara la estructura real de esa ola y la fila se resuelve con el vocabulario de §5.
4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO

Busqué, contra bd9ed213: el objeto «comparabilidad por texto de la sección de crédito de ENIF» y el objeto «medición de crédito a nivel persona».

dónde    universo    términos    resultado
forense/prereg-caja/ + data/corrida0/*/spec.yaml    100 + 166    P6_, credito|crédito    EXISTE-NO-SATISFACE — solo ENIF-FINTECH-SERIE toca crédito de ENIF, y solo canal fintech
data/corrida0/ (CALC)    187 entradas    cred|deuda|prest|tanda|moros    EXISTE-NO-SATISFACE — Banxico producto/daño, IMOR, ENSAFI atraso, tandas ENNViH. Ninguno con microdato ENIF a nivel persona
forense/encargos/    580 .md    ENIF ∧ crédito; «comparabilidad por texto»    NO-ENCONTRADO para este objeto
forense/no-corrido.tsv    422 NC    credito|crédito|enif + ABIERTA    ninguna NC abierta tiene a este acto como sucesor
ramas vivas    5 remotas    —    acto/gen2-celda-d-piloto-3-commit-1-v1_1 está viva y es del piloto 3 (ENCIG). No toca este perímetro

Al ejecutor: repite esta búsqueda con tu acceso, que es mejor que el mío. Si encuentras que alguna fila ya está resuelta en otro sitio, el entregable es decirlo y hacer solo lo que falte.

5 · PIEZAS — resultado esperado, no receta

P1 · Inventario por instrumento (A.15). Por ola, qué secciones del cuestionario y del FD contienen crédito, con el conteo de reactivos de cada una y el nombre literal de la sección. Queda bien si: ninguna afirmación negativa posterior se apoya en algo que no esté en este inventario.

P2 · La tabla — data/credito-comparabilidad-texto-v1_0.tsv. 40 filas, conducta × ola. Columnas mínimas: conducta (K1…K8) · ola · veredicto · reactivo (identificador tal como aparece en el FD) · texto_literal · opciones_y_codigos · filtro_y_flujo · unidad · poblacion_base · fuente (archivo + sha256/16 + página o fila) · secciones_fd_recorridas · nota.

Vocabulario del veredicto, lista cerrada:

veredicto    cuándo
MISMO-INSTRUMENTO    redacción, opciones, códigos, filtro y flujo idénticos
CAMBIO-MENOR    algo cambió y se escribe por qué no entra en el estimando de esa conducta
CAMBIO-DE-INSTRUMENTO    cambió algo que sí entra en el estimando
NO-ESTIMABLE    la ola no pregunta la conducta. Obliga a citar el texto buscado y las secciones del FD recorridas (A.15). No vale «no existe la variable»
NO-VERIFICABLE-AQUÍ    2012 y 2015 sin cuestionario: el FD y el modelo de datos llegan hasta donde lleguen y el límite se declara. No se degrada a NO-ESTIMABLE

La consecuencia de cada veredicto vive en esta tabla y en ningún otro sitio. En el piloto 3, la consecuencia de una guardia estaba escrita en el encargo con una semántica y en el código con otra, y costó una sesión. Aquí no se repite el veredicto en prosa con otras palabras.

P3 · Unidad, por conducta y por ola. P (persona elegida) o PR (producto de crédito), leída del flujo —a quién se le pregunta, cuántas veces, si es «el último crédito» o «¿tiene usted…?»—, no del nombre de la variable. Rama prevista: si la unidad cambia entre olas para la misma conducta, esa conducta cierra CAMBIO-DE-INSTRUMENTO aunque el texto sea idéntico. Una tasa de personas y una de productos no se comparan sin función de enlace (A-bis 3).

P4 · Población base y universo, por ola. [LEÍDO] en 2018 es 18–70 y en 2021/2024 es 18+. Verifícalo por texto en las cinco y escríbelo por fila. Rama prevista: si la base difiere, la fila no es MISMO-INSTRUMENTO aunque el reactivo lo sea; es CAMBIO-MENOR con el recorte declarado, o CAMBIO-DE-INSTRUMENTO si el recorte toca el segmento de interés.

P5 · La verificación de D3. ¿ENIF pregunta, y en qué olas: (a) haber solicitado crédito formal y haber sido rechazado; (b) los motivos de no tener crédito, con al menos una opción de exclusión por oferta (no cumple requisitos, no tiene comprobante de ingresos, no tiene historial, se lo negaron) separable de la autoexclusión declarada (no le gusta endeudarse, no le interesa); (c) bancarización? Veredicto por ola con el texto literal de cada opción. Rama prevista y es la importante: si (b) no es separable en ninguna ola, K4 no es construible en ENIF y el dominio pierde su celda central. Eso es entregable, no fracaso: se declara y la pregunta a mesa es si K4b se busca en ENSAFI 2023 o ENFIH 2019 como triangulación rotulada. Sigue con el resto mientras tanto.

P6 · Ficha de límites. Qué queda fuera y por qué, en vocabulario A.4 (EXISTE-SATISFACE · EXISTE-NO-SATISFACE · NO-ENCONTRADO con dónde y con qué términos · NO-ACCESIBLE). Incluye el hueco de la reserva: el par «crédito por app» de 2024 está visto y no se relanza.

P7 · El test. Un test de forma sobre la tabla (40 filas, columnas obligatorias no vacías, veredictos dentro de la lista cerrada, toda fila negativa con texto buscado). Corre sobre un caso sintético antes de correr sobre la tabla real (D-22): el piloto 3 murió porque se declaró congelado un medidor cuyo punto de entrada nunca había corrido. El test se cablea en CI.

6 · LATITUD

Decides tú, y lo dices en la nota: el orden de las piezas · las herramientas de extracción (pdftotext -raw/-layout u otra) · el nombre y la forma exacta de las columnas más allá de las mínimas · enlazar o crear data/raw · instalar una dependencia · regenerar un derivado por comando · corregir una cita rota · arreglar un defecto adyacente de ≤ 10 líneas que te impida terminar, declarándolo.

Preguntas a mesa con 2–3 opciones y tu recomendación, y sigues con lo demás: la rama de P5 si K4b no es separable · cualquier bifurcación que cambie qué conductas entran a la serie.

No decides: nada de §7.

7 · PAROS — lista cerrada. Fuera de ella no se para: se resuelve o se pregunta
(a) Abrir, derivar o imprimir cualquier miembro de datos de ENIF 2024 (TMODULO.csv o cualquier otro), o relanzar el par «crédito por app» ya consumido. Leer el cuestionario, el FD y el modelo de datos de 2024 NO es abrir dato reservado: es exactamente lo que este acto viene a hacer.
(b) Borrar, forzar (-D, --force, clean) o reescribir algo sellado.
(c) Adoptar cualquier cosa, o mover un contador: cuenta_gen2 se queda en NO-APLICA.
(d) Cambiar estimando, universo, umbral o código de un procedimiento congelado ajeno.
(e) ENTORNO-DERIVADO ≠ CAJA.
(f) El objetivo dejó de ser alcanzable —por ejemplo, los PDF del corpus no abren— y eso es el entregable.

(g) no aplica: no hay código congelado en este acto.

8 · COMPUERTAS

«Los documentos de las cinco olas verificados por sha256sum contra data/manifiesto.yaml, con los tres estados de A.1 sin colapsar (AUSENTE · raíz-no-configurada · hash-discordante) y la salida cruda pegada» protege: abrir dato. Un veredicto de comparabilidad sobre un PDF cuya identidad no se estableció no vale nada.

Todo lo demás en este encargo es orden sugerido, no compuerta.

9 · PERÍMETRO

Propio: data/credito-comparabilidad-texto-v1_0.tsv + su .meta · su fila en data/INFRAESTRUCTURA-v1_0.md · el test nuevo y su cableado en CI · forense/notas/2026-09-2X-GEN2-DIN-CREDITO-COMPARABILIDAD-TEXTO-1-cierre.md · NC y FP propias · forense/hallazgos.md · el archivo verbatim de este encargo con su sha256 (0-bis, A.3) · la cascada de /acto.

Ajeno, no se toca y por qué: milpa/tramite.yaml y milpa/tramite-ola5-propuesta-v0.yaml — K1–K8 no se escriben como reglas aquí, no hay nada medido que las sostenga · data/corrida0/ y cualquier CALC — este acto no estima · el marcador y data/curacion-registro/celdas-d/ — perímetro de DIRECCIÓN, que está propagando la adopción de la celda-D de ahorro · tools/corrida0.py · ENIGH, ENSAFI y ENFIH, que aquí solo se nombran como sucesores · la rama del piloto 3.

Perímetro de cierre, permanente y no hay que pedirlo (D-21): cablear el test en CI · registrar la tabla en INFRAESTRUCTURA · ## NO-CORRIDO / RESERVAS (con «Ninguno.» obligatorio si no hay) antes de ## CONSUMIDO · hallazgos, NC y FP propias.

«Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»

10 · LO QUE NO HACE · SUCESORES · AUDITORÍA · CIERRE

No hace: no mide ninguna proporción · no crea ningún CALC · no abre microdato de ninguna ola · no escribe reglas en el trámite · no elige el cruce del piloto de ahorro · no descarga nada · no decide si K4b migra a otro instrumento.

Sucesores, en este orden:

Marginales de crédito de ENIF 2021 (y 2018 donde el texto lo permita) — es el piso del dominio y hoy no existe. Sin él, cada conducta de crédito nace SIN-PISO y no hay nada que acote a los retadores.
La regla de elección del cruce del piloto de ahorro, que escribe dirección cerrando los dos huecos de la regla de ENCIG: la consecuencia de cada guardia en un solo sitio, y congelado solo si el punto de entrada ya corrió (D-22).
Adquisición de los cuestionarios de ENIF 2012 y 2015 → mesa → NUBE-MEDICIÓN. Mientras no lleguen, esas dos olas viven en NO-VERIFICABLE-AQUÍ y no se fuerzan.

Auditoría (§5 de las instrucciones). Este acto no produce ninguna cifra sobre conducta en México: lo único que afirma es sobre el instrumento. Aun así, tres líneas obligatorias en la nota: (1) que dos olas pregunten lo mismo habilita medir y no dice qué se va a encontrar; (2) el universo de ENIF es población de 18+ (18–70 en 2018) en viviendas, con submuestreo conocido del mundo rural y de localidades pequeñas — cualquier conducta de crédito leída ahí sobre-representa al urbano bancarizado; (3) la razón por la que K4 va partido: «no le gusta endeudarse» y «no cumplo los requisitos» producen la misma conducta observada —no tener crédito formal— y significan cosas opuestas. Colapsarlas es exactamente el defecto de leer estructura como cultura, y es el que este dominio tiene más cerca.

Cierre: cascada de /acto · ## NO-CORRIDO / RESERVAS · ## CONSUMIDO con el PR · primera línea de la nota: universo, unidad, escala y clase de evidencia.

Falsador de este encargo, a tres meses: si el sucesor 1 (marginales de crédito 2021) tiene que volver a leer el texto de algún reactivo que esta tabla ya clasificó, la tabla no sirvió y se revisa su diseño de columnas.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| P2 · «cada fila cuyo veredicto no sea NO-VERIFICABLE-AQUÍ trae la cita literal del reactivo» — cumplido; las 16 filas de 2012 y 2015 llevan `NO-VERIFICABLE-AQUÍ` con `limite_fd` | `NO-VERIFICABLE-AQUÍ`: el corpus no tiene los cuestionarios de 2012 ni 2015; el FD trae texto, opciones y códigos pero no pases ni filtros (`NC-0423`) | el sucesor 1 no puede extender la serie a 2012/2015; ningún contador se mueve | DIFERIDO-A: adquisición de cuestionarios ENIF 2012/2015 (sucesor 3, mesa → NUBE-MEDICIÓN) |
| K8 · destino del último crédito (unidad PR) como conducta de la serie | `DECISIÓN-DE-MESA-PENDIENTE`: 2021/2024 no lo preguntan (NO-ESTIMABLE con texto buscado); 2012–2018 lo preguntan con unidad P, multirrespuesta y filtro nómina/personal/grupal (`NC-0424`) | K8 sin piso posible en ENIF 2021; serie K1–K7 | `FP-402` (recomendación: serie propia P en 2012–2018) |
| K2 · familia bancaria 2021↔2024 | `DECISIÓN-DE-MESA-PENDIENTE`: 6.2.2 de 2024 amplía «bancaria» a «u otra institución financiera», CAMBIO-DE-INSTRUMENTO (`NC-0425`) | la familia bancaria no entra a la serie 2021–2024 sin enlace; departamental, nómina y automotriz sí | `FP-402` (recomendación: no comparar en serie; descriptivo rotulado) |
| Regeneración completa de `forense/analisis/ci-guardias/censo-tests.tsv` con `--censo` | `FUERA-DE-PERÍMETRO`: en esta caja reclasifica 74 filas ajenas (numpy/pandas presentes); es del acto `GEN2-CI-GUARDIAS-VIVAS-1` o de quien gobierne el censo. Aquí se añadió sólo la fila del test propio | ninguno para este acto; `--ejecuta-huerfanos` → 0 fallidos, 0 huérfanos nuevos | SIN-ASIGNAR |

Piezas P1, P3, P4, P5, P6, P7 y la cascada de cierre: corridas completas. La rama de P5 («K4b no separable en ninguna ola») no se abrió porque K4(a)/(b) es separable en 2018/2021/2024.
