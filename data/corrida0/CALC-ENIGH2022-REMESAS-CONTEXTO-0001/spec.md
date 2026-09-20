# CALC-ENIGH2022-REMESAS-CONTEXTO-0001

Prerregistro y contrato congelado de incidencia e intensidad contable de
remesas por tamaño de localidad y estrato socioeconómico, por separado, en
hogares de ENIGH 2022. Lo autoriza
`GEN2-ENIGH2022-REMESAS-CONTEXTO-CLI-2` el 19/sep/2026.

## Exposición y novedad

Antes de congelar se conocen los resultados nacionales de `CALC-ENIGH-0001`
y `CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`, y el catálogo y los marginales de
personas de `CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003`. No se conocen resultados
de remesas por los dos contextos de este acto. La búsqueda previa en repo,
encargos, ramas y PR no encontró medición equivalente. La novedad son los
perfiles contextuales y los contrastes predefinidos; los nacionales son sólo
controles. El perfil estructural usa personas y su peso no se traslada aquí.

## Fuente, unidad y variables

Payload `enigh2022_nc_csv`, SHA-256
`3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06`.
Se abre sólo `conjunto_de_datos_concentradohogar_enigh2022_ns.csv`. El
diccionario del mismo ZIP documenta una fila por hogar, llave
`folioviv+foliohog`, `factor` de hogar, `est_dis`/`upm`, `tam_loc`,
`est_socio`, `remesas` como P041 (“Ingresos provenientes de otros países”) e
`ing_cor`, que incluye `remesas` dentro de transferencias. No se interpreta
remesas como toda transferencia familiar. Como clasificación, monto, ingreso,
peso y diseño viven en la misma fila hogar, no hay enlace; se exige llave 1:1.

La unidad monetaria heredada es pesos de 2022 por trimestre normalizado. No se
anualiza, deflacta, imputa, trunca, winsoriza ni construye ingreso
contrafactual.

## Catálogos y comparaciones congeladas

`tam_loc`: 1 “Localidades con 100 000 y más habitantes”; 2 “15 000 a
99 999”; 3 “2 500 a 14 999”; 4 “menos de 2 500”. `est_socio`: 1 “Bajo”; 2
“Medio bajo”; 3 “Medio alto”; 4 “Alto”. Se publica total, las cuatro
categorías nativas y un residuo para ausente/desconocido, incluso vacíos.
Nunca se abre localidad×estrato.

Únicos contrastes, definidos como primer término menos segundo:

1. localidad de menor tamaño frente a mayor: `tam_loc=4 - tam_loc=1`;
2. estrato inferior frente a superior: `est_socio=1 - est_socio=4`.

Cada uno se calcula para prevalencia, participación media por hogar y
proporción con participación ≥0.5. Los estratos intermedios quedan en tablas,
sin contrastes.

## Universos y estimandos

El marco conserva los 90,102 hogares. Hogar elegible para puntos: `factor`
finito y positivo. Remesas ausentes/no numéricas/no finitas y negativas se
cuentan separadas y nunca pasan a cero. En cada grupo se informa n y masa
elegible, remesas válidas/no válidas, receptores (`remesas>0`) y prevalencia
con denominador de remesas válidas. El total se reconstruye con numeradores y
denominadores, no promediando porcentajes.

Entre receptores se estiman media ponderada y mediana ponderada de remesas.
La mediana es la inversa izquierda de la CDF: menor valor observado cuya masa
acumulada alcanza al menos 0.5, sin interpolación. El dominio de participación
añade `ing_cor>0` válido y reporta n/masa y exclusiones por ausente/no finito,
cero y negativo. En ese único dominio se estiman, sin intercambiarlos:

- media de razones: `sum(factor*remesas/ing_cor)/sum(factor)`;
- razón de sumas: `sum(factor*remesas)/sum(factor*ing_cor)`;
- proporción ponderada con `remesas/ing_cor >= 0.5`.

Se conserva la guardia `remesas <= ing_cor + 0.01`. Las incompatibilidades se
cuentan y pesan; no se eliminan. Los cocientes se publican como diagnóstico y
el grupo queda marcado `REPORTADO-CON-INCOMPATIBILIDAD`.

## Precisión y degeneración

Todos los grupos y contrastes comparten 2,000 réplicas de bootstrap de UPM con
reemplazo dentro de `est_dis`, `numpy.PCG64`, semilla `20260919`. El marco
completo determina multiplicidades comunes; los dominios se aplican dentro de
cada réplica. Una UPM única se remuestrea a sí misma y aporta variación cero.
Se publican percentiles 2.5/97.5 para prevalencia, media y mediana de monto y
los tres estimandos de participación. Los contrastes se restan réplica a
réplica, nunca desde extremos de IC marginales.

Si falta diseño en cualquier fila del marco no se fabrican IC iid. Un punto
con denominador nulo es `null`. Una réplica con denominador nulo es degenerada
y se cuenta; el IC se publica con las réplicas finitas si existe al menos una,
con su soporte explícito, o queda `null` con causa. No hay umbral de tamaño de
celda para ocultar puntos. Se informa número de estratos, UPM, singletons,
réplicas válidas y degeneradas.

## Controles, lectura y límites

El total debe reproducir, en universo idéntico, prevalencia, media/mediana de
remesas y los tres cocientes de los dos antecedentes. Un cálculo focal
independiente reproduce la media nacional mediante `math.fsum` y calcula su
EE linealizado por UPM dentro de estrato; no sustituye los IC prioritarios.

La conclusión separará frecuencia de recepción e intensidad condicional: un
grupo puede recibir menos frecuentemente y mostrar mayor participación entre
receptores. `est_socio` no se llamará pobreza, decil ni ingreso. No se infiere
quién emigró ni efecto protector, dependencia causal, trayectoria,
volatilidad o respuesta a choques a partir de una ola transversal.

