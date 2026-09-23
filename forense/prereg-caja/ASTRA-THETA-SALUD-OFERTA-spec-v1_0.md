# ASTRA-THETA-SALUD-OFERTA · preregistro v1.0

Estado al sellar: **sin abrir `ALL.tab` ni `clustmatchlist.tab`**. Primer
resultado del procedimiento será el resultado reportado, incluso cero,
contrario al mecanismo, impreciso o no estimable. Consumidor investigado:
`RES-0087`, `milpa/procedencia.yaml:asignados_probabilidad:salud.atencion.leve_sin_imss`
(`asignados_probabilidad[5]`), canon R4.1 (§3.4). Este estudio **no estima
directamente** el vector condicional `[0.66,0.24,0.10]`.

## Intervención, población y estimando

King et al. (2009) asignaron al azar 50 pares de conglomerados de salud de
seis entidades a la oferta de Seguro Popular: promoción de afiliación,
recursos para instalaciones y medicamentos. La fuente primaria de la
asignación es la réplica DOI `10.7910/DVN/P6NC0M`, archivos
`Eval/define.treatment.R` y `Eval/control.matches.R` en
`replicatelancet.tar.gz`, cotejados con `clustmatchlist.tab`. La geografía
causal es el conglomerado de residencia y atención; la entidad solo
describe el marco. Basal 2005 y seguimiento tras ~10 meses en 2006.

Población: personas de 18 años o más en el basal, sin IMSS obligatorio
(`P01D1401 != 1`) ni voluntario (`P01D1601 != 3`) al inicio, con respuesta
conocida en esos reactivos; ambos brazos según asignación original. No se
filtra por seguro **posterior**, enfermedad posterior, uso posterior ni
afiliación efectiva: son variables afectables por el tratamiento. El
denominador primario son todas las personas elegibles con seguimiento
observado. Si `ALL.tab` no permite enlazar basal y seguimiento por persona,
no se sustituirá por muestra transversal sin nueva versión del protocolo.

Desenlace binario por persona en seguimiento: 1 si el motivo de la consulta
fue respiratorio (`P10E0401=3`: tos/gripe/catarro/bronquitis/neumonía)
**y** el lugar fue farmacia (`P10E0501=9`); 0 si no hubo consulta o hubo
otra consulta con respuesta válida. Se excluirá por valor desconocido de
motivo/lugar solo si la consulta ocurrió y alguna de esas preguntas es
necesaria para clasificar el evento; se reportará su fracción por brazo.
La correspondencia basal de placebo es `P11D0401=3` y `P11D0501=9`.
La categoría respiratoria incluye neumonía y por ello **no equivale a
"leve-moderado"**; el lugar «farmacia» no distingue consultorio anexo de
compra sin consulta. Se reportarán estos dos límites como parte del
dictamen, nunca como corrección posresultado.

Estimando primario: ITT medio entre personas elegibles al inicio de la
oferta compuesta sobre la probabilidad del **evento conjunto** definido
arriba, en puntos porcentuales. No se divide por la proporción con
padecimiento ni se condiciona en usuarios de salud posteriores. No es
efecto de afiliación efectiva ni de cada componente; ninguna función
de enlace con θ está aprobada. Un efecto distinto de cero mostraría que
una intervención de acceso mueve ese evento, no la magnitud de la
probabilidad condicional del motor.

## Medidor e incertidumbre

Unir por ID de persona/hogar exactamente según README; verificar unicidad
y que cada conglomerado pertenezca a un solo par/brazo. Si `ALL.tab` ya
combina las olas, usar sus columnas basales y `.T2` finales sin otro merge.
Exigir 50 pares completos (100 conglomerados) en el archivo de asignación,
sin reasignar ni reemplazar pares. Para cada brazo de cada par calcular la
media de Y entre elegibles seguidos; diferencia tratamiento-control por
par. Estimador principal: media **no ponderada de las 50 diferencias**
en puntos porcentuales, que estima el promedio de pares del experimento,
no la media nacional. IC95% de Student con 49 grados de libertad sobre
esas diferencias; prueba de aleatorización de 100,000 inversiones de signo
de par, semilla fija `20260923`, para H0 aguda de efecto nulo. Reportar
también n personas elegibles, seguidas, pares, conglomerados y tasas de
seguimiento. Sin extrapolación nacional ni ponderadores de ENSANUT/ENCIG:
la incertidumbre usa la unidad sorteada y el diseño de pares.

Guardias previas a estimar: hashes de manifiesto; códigos y columnas del
codebook; 50 pares completos y una asignación por conglomerado; ID único;
≥1 elegible observado por brazo/par. Si alguna falla, emitir **NO-ESTIMABLE**
con causa, sin reemplazar grupos, códigos o fechas. La ausencia de peso
poblacional no altera el estimando de pares; impide llamarlo nacional.

## Falsaciones y consecuencias fijadas

1. Balance basal del mismo evento y de edad, sexo y seguro IMSS: publicar
   diferencias por pares e IC. Desequilibrio basal del evento cuyo IC95%
   excluya cero rebaja la lectura a efecto aleatorizado con balance fallido;
   el estimador y muestra no se cambian. No declarar prueba de la
   aleatorización fallida solo por un p pequeño.
2. Atrición: diferencia de proporción seguida entre brazos por par, IC95%.
   Si valor absoluto supera 5 pp **o** su IC excluye cero, el efecto
   condicionado a seguimiento se rotula `ASOCIACION-MEDIDA` por posible
   selección postasignación; no se informa como ITT identificado.
3. Clasificación/missing del desenlace: si >5% de elegibles seguidos tiene
   consulta no clasificable, o diferencia por brazo >2 pp, rotular
   `ASOCIACION-MEDIDA` y mostrar límite de Manski simple 0/1 por brazo.
4. Integridad del tratamiento: discrepancia entre código de asignación y
   lista de pares, o faltan pares, implica NO-ESTIMABLE. No se usa afiliación
   efectiva como tratamiento.
5. Precisión: si IC incluye cero, resultado inconcluso respecto del signo;
   si queda cerca de cero con IC estrecho, acota solo este evento conjunto.

El argumento de identificación descansa en sorteo de conglomerados, no en
regresión de seguro observado. El tratamiento se compone de seguro, mejoras
y medicamentos. La intervención podría afectar enfermedad y búsqueda de
consulta además de elección de proveedor; por eso la medición es una
prueba reducida de R4.1 y no un θ cargable. Para usarla en el motor mesa
debe aprobar un enlace nuevo con incidencia de necesidad previa y medición
separada de consultorio anexo o elegir una intervención distinta. No se
modifica canon, procedencia, E1, decisiones ni reservas.

## Fuente y orden de trabajo

Fuente primaria: [King et al., descripción del ensayo](https://gking.harvard.edu/files/abs/spi-abs.shtml?page=0%2C0%2C0%2C0%2C1)
y [Harvard Dataverse V6.2](https://doi.org/10.7910/DVN/P6NC0M).
README y codebooks HTML pre/post descargados para leer estructura, no
desenlaces. Dataverse declara que no especifica condiciones de uso y
recomienda contactar a sus responsables; adquisición debe documentar
ese término y la base de uso antes de abrir la tabla. El corpus compartido
`/home/pc0/mm-corpus/raw` tiene ENSANUT, no esta réplica. Registrar
microdato/llaves/codebooks por `codex/adq-*` con id/hash/tamaño. Después
de **commit de este freeze**, verificar estructura limitada a variables
listadas, ensayo sintético de pares, `preflight → run → verify` y conservar
todo resultado, incluso falsaciones adversas. Si no se puede registrar o
usar lícitamente el microdato, no se produce una cifra sustituta.
