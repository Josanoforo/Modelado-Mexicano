# Prerregistro · ENADID 2023 · unión actual por sexo y edad

Contrato humano congelado antes de abrir valores de personas para
`CALC-ENADID2023-UNION-SEXO-EDAD-0001`. Los únicos accesos previos fueron a
hashes, miembros del ZIP, ficha descriptiva y cuestionario. Gobiernan los
parámetros de `data/corrida0/CALC-ENADID2023-UNION-SEXO-EDAD-0001/spec.yaml`;
este texto explica el propósito y no duplica parámetros modificables.

La operación es descriptiva, transversal y no ciega. Antes de congelar se
conocían todos los resultados del padre `CALC-ENADID-0001`, incluidos sus
puntos e intervalos nacionales y por edad. El padre será control marginal, no
resultado nuevo. Una búsqueda en `main`, resultados, encargos, análisis,
ramas remotas y PR no encontró el cruce sexo×edad ni esta estandarización.

Se publican tres productos sobre residentes de 15+ en `TSDEM`: (P1) las siete
categorías nativas de `P3_27` por sexo y edad; (P2) unión libre entre quienes
están actualmente en unión libre o casadas(os), y el contraste
mujeres−hombres; (P3) ese contraste bruto y estandarizado a una distribución
común de edad. Separada(o) de unión libre y separada(o) de matrimonio siguen
siendo categorías distintas. `P3_27_AG` y el módulo femenino no se usan.

Sexo documental: 1 hombre, 2 mujer. Cualquier otro valor queda como residuo
visible y no se reasigna. Edad 999/no numérica tampoco se reasigna. Los cinco
grupos exhaustivos son 15–17, 18–29, 30–44, 45–59 y 60+. El cuestionario aplica
3.27 a personas de 12 años o más; 15+ es el recorte analítico heredado.

El punto es razón de masas `FAC_VIV`. La incertidumbre usa 800 réplicas
compartidas Rao–Wu reescaladas: dentro de cada `EST_DIS` con `m>1` UPM se
extraen `m-1` UPM con reemplazo y el multiplicador es
`m/(m-1) × frecuencia`; semilla PCG64 20260919. El marco se construye con
todas las filas de TSDEM con peso y diseño válidos antes de indicar sexo,
edad, respuesta o unión. `UPM_DIS` es la UPM y `EST_DIS` el estrato; nunca
`UPM`/`ESTRATO`. Los estratos singleton permanecen constantes en las réplicas
y toda la matriz de covarianza se multiplica por
`H_total/H_no_singleton`, equivalente a asignarles el aporte promedio de los
estratos no singleton del padre. No hay FPC acreditada. Grados de libertad:
`sum_h(m_h-1)`.

Los IC de proporciones y pesos son logit-t; los contrastes son t simétricos.
Una proporción en frontera conserva EE pero no IC logit. Denominador nulo es
`NO-ESTIMABLE:DENOMINADOR-NULO`. Si una réplica tiene denominador nulo, la
precisión de esa cantidad y de sus derivados es
`NO-DISPONIBLE:REPLICA-DEGENERADA`; no se imputa ni se convierte en cero.

En P3 el universo es sexo conocido, edad válida y `P3_27∈{1,6}`. Los pesos
estándar son las cinco participaciones ponderadas de edad entre ambos sexos
juntos. Dentro de cada réplica se recalculan pesos y tasas por sexo×edad. Si
un sexo carece de denominador en un tramo cuyo peso estándar es positivo, no
se redistribuye: su tasa estandarizada y contrastes derivados quedan no
estimables, sin impedir P1/P2. `bruta−estandarizada` es una descomposición
descriptiva de composición, no efecto causal ni porcentaje explicado.

La ejecución escribirá `distribucion.csv`, `union_condicional.csv`,
`estandarizacion.csv`, `flujo.csv` y `auditoria.json`. Las reconstrucciones
usan masas de numerador y denominador, incluido el residuo de sexo
desconocido; nunca promedios simples. El contador queda
`PENDIENTE-DE-MESA` y no hay adopción.
