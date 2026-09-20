# GEN2-ENADID2023-UNION-SEXO-EDAD-CLI-2

Encargo archivado verbatim al iniciar la rama
`codex/gen2-enadid2023-union-sexo-edad-cli-2` desde `origin/main` en
`ea88cb3b94ad820bcd92a485eae51ce24ef07fae`. La base revisada por dirección,
`6f365928ada3714a02954a7a5be64eb8013ecc9e`, es ancestro del punto de inicio.

## Mandato y novedad

Mide cómo se distribuye la situación conyugal actual por sexo y edad, cuánto
cambia la proporción de unión libre entre personas actualmente unidas y cuánto
de la diferencia descriptiva por sexo depende de la composición de edad.
Entrega distribución conjunta, incertidumbre compartida y contraste
estandarizado; no otro nacional.

El padre `CALC-ENADID-0001` ya midió las siete categorías de `P3_27` y unión
libre/(unión libre+casada), total y cinco edades. Se reutiliza como control, no
como resultado nuevo. Antes de congelar se buscan equivalentes en resultados,
encargos y ramas; si existe una parte equivalente, se referencia y sólo se
ejecuta el aporte faltante.

## Contrato

- Fuente TSDEM de ENADID 2023; payload/hash resueltos desde la spec del padre y
  el corpus.
- Unidad persona residente 15+, `LLAVE_PER`, `EDAD`, `SEXO`, `FAC_VIV`,
  `EST_DIS`/`UPM_DIS` y las siete categorías nativas de `P3_27`.
- `ESTRATO` sociodemográfico y `UPM` de llave no son variables del diseño.
- Edades heredadas: 15–17, 18–29, 30–44, 45–59 y 60+. Edad 999 y sexo
  desconocido no se reasignan. Sexo desconocido queda como residuo visible.
- No se incorporan variables del módulo femenino ni enlaces que cambien el
  universo.

Antes de ejecutar se congelan spec humana/YAML, medidor, pruebas sintéticas,
salidas y regla de estandarización en COMMIT-1. La operación conoce los
resultados anteriores y es descriptiva, no ciega. COMMIT-2 contiene el primer
resultado y su sello; intentos y sucesores materiales se conservan.

## Tres productos

1. Distribución exhaustiva de siete categorías por sexo×edad y sexo total,
   con N/masa antes y después de filtros, desconocidos, proporciones y
   precisión. Separada de unión libre y separada de matrimonio no se unen.
   Los marginales del padre se reconstruyen por numerador/denominador y
   residuos.
2. Proporción unión libre entre `P3_27∈{1,6}` por sexo×edad y sexo total. Las
   demás categorías están fuera del denominador. Se publica diferencia
   mujeres−hombres por edad usando covarianza de diseño compartida. Denominador
   nulo queda NO-ESTIMABLE.
3. Diferencia bruta frente a diferencia estandarizada por edad sobre sexo
   conocido, edad válida y `P3_27∈{1,6}`. El estándar es la distribución
   ponderada conjunta de los cinco grupos. Cada réplica recalcula tasas y
   pesos. No se redistribuyen pesos si una tasa de sexo falta en un tramo con
   peso positivo. La resta no se llama efecto causal ni porcentaje explicado.

El remuestreo conserva el marco completo de estratos/UPM y usa indicadores de
dominio. Se congelan réplicas compartidas, semilla, singleton, degeneraciones
y precisión. Las pruebas cubren exhaustividad, desconocidos, reconstrucción,
denominador vacío, estándar común, diferencia bruta frente a estandarizada y
un control independiente de punto e incertidumbre.

## Perímetro y publicación

Sólo CALC nuevo/sucesores propios, preregistro y análisis
`enadid2023-union-sexo-edad-cli-2`, prueba propia, asiento de replay propio y
vistas por comandos vigentes. No se editan padre, milpa, gobierno, motor,
decisiones, `corrida0.py`, pruebas generales, EDER, reservas ni piloto 3. No se
aceptan cambios de replay ajeno mediante `--lote`.

Se sella, reproduce, asienta y proyecta; se comprueba segunda proyección
estable. La entrega incluye tablas, mapa RESULT→universo, controles y lectura
sustantiva. `cuenta_gen2=PENDIENTE-DE-MESA`. Pegar este encargo autoriza
commit, push y PR, pero no merge ni adopción.

## NO-CORRIDO / RESERVAS

Ninguno al congelar COMMIT-1; se actualizará en el cierre si aparece una
reserva material.

## CONSUMIDO

Ejecutado en `PR #897`, rama
`codex/gen2-enadid2023-union-sexo-edad-cli-2`. La corrida vigente es
`CALC-ENADID2023-UNION-SEXO-EDAD-0004`; 0001 conserva el intento no sellado
por tipo registral incompatible con contrastes negativos, 0002 permanece
sellado y 0003 conserva la primera corrección incompleta de los conteos de
pesos estándar. 0004 publica `n_numerador` por tramo y `n_denominador` común
sin cambiar ningún estimando. No quedó reserva
material: P1, P2 y P3 son estimables; el residuo visible de sexo desconocido
tiene denominador nulo y se conserva como `NO-ESTIMABLE`, sin bloquear los
productos. `cuenta_gen2=PENDIENTE-DE-MESA`; sin merge ni adopción.
