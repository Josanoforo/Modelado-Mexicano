# CALC-ENADID-0001 · situación conyugal actual, ENADID 2023

Mide, entre personas de 15 años y más, (a) la distribución exhaustiva de las
siete respuestas documentales de P3_27 y (b) la proporción en unión libre
entre quienes actualmente están casadas(os) o en unión libre. Publica total y
15–17, 18–29, 30–44, 45–59 y 60+. El complemento del segundo estimando se
llama «actualmente casadas(os)»; el del primero, «no unión libre». Ninguno se
llama matrimonio directo ni tipo de primera unión.

Unidad: residente en `TSDEM.csv`; llave `LLAVE_PER`; edad `EDAD`; peso
`FAC_VIV`; estrato `EST_DIS`; UPM `UPM_DIS`. El FD acredita que `ESTRATO` es
sociodemográfico y `UPM` integra la llave: no se usan para precisión.
`P3_27_AG` es una agrupación derivada y no gobierna códigos. El cuestionario
aplica P3_27 desde 12 años; 15+ es el recorte analítico pedido, declarado y
conserva 15–17 para cerrar el total.

El punto es razón de totales ponderados. La varianza WR de Taylor para razón
se calcula por UPM dentro de estrato sobre la muestra completa: fuera del
dominio aporta cero. IC95 logit-t, `gl=sum_h(m_h-1)`. Un estrato singleton no
equivale a varianza cero: recibe el aporte medio de los estratos no singleton
y no aporta grados de libertad. Sin FPC acreditada. Diseño incompleto,
frontera o gl nulos producen
precisión no disponible con causa. Desconocidos, edad 999 y pesos no positivos
se cuentan y nunca se convierten en respuestas negativas. Las categorías
válidas ajenas a {unión libre, casada(o)} se publican como fuera del
denominador condicional, no como desconocidas. Llave duplicada
aborta; no hay enlace porque todas las variables viven en TSDEM.

Las siete categorías son: 1 unión libre; 2 separada(o) de unión libre; 3
separada(o) de matrimonio; 4 divorciada(o); 5 viuda(o); 6 casada(o); 7
soltera(o). Esta operación es descriptiva, prospectivamente congelada pero no
ciega: ya existen cifras legacy 0.1905/0.8095 y celdas condicionales por edad.
No mide garantía institucional, mecanismo causal ni primera unión.
