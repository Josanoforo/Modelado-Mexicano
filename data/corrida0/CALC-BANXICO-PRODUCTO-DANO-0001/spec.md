# `CALC-BANXICO-PRODUCTO-DANO-0001` — producto, pago y costo percibido Banxico 2019–2024

**Spec congelada antes de ejecutar el medidor o abrir el XLSX en este acto.**
La autorización es el encargo `GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO`,
archivado verbatim en
`forense/encargos/2026-09-12-GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO.md`.
La codificación se fija con el manual Banxico de diciembre de 2024 y la
población con el informe de resultados 2024; los bytes se identifican por las
tres entradas de manifiesto declaradas en `spec.yaml`.

## 1. Fuente, población, unidad y cortes

La fuente es la Encuesta de Satisfacción de las Personas Usuarias de Productos
y Servicios Financieros de Banco de México, archivo integrado 2019–2024. Cada
fila es una persona participante en una ola. Cada ola se trata como corte
transversal separado: no hay documentación ni llave que acredite seguimiento
longitudinal y no se suman masas entre olas. Los productos no son excluyentes y
sus masas tampoco se suman como si fueran personas distintas.

Población de alcance: personas mexicanas de 18 a 70 años con al menos un
producto financiero, residentes en localidades de 50 mil habitantes o más.
No se extrapola a todo México rural ni a personas sin productos. El punto usa
`ponderador` positivo como razón de totales dentro de cada producto y ola.

La primera hoja debe contener 12,408 filas de datos, 142 columnas y las olas
2019–2024. Los filtros de tenencia válidos son `tdc_filtro`, `hip_filtro`,
`per_filtro`, `nom_filtro`, `aut_filtro`; sólo valor `1` entra al universo del
producto. `fecha` identifica la ola y `ponderador` la masa expandida. Peso
ausente, no finito o no positivo no aporta masa y se reporta por separado.

## 2. Variables y códigos congelados

Para cada prefijo de producto se usan `<p>_intereses`, `<p>_comp_pago`,
`<p>_problemas` y `<p>_reclamacion`.

- Costo percibido (`*_intereses`): niveles válidos originales `0..10`;
  `0` corresponde al extremo de intereses percibidos bajos y `10` al de altos
  en el XLSX homologado publicado en 2024. `99` es no sabe/no contestó, `-1`
  es salto/no aplica y blanco se conserva aparte. Es una calificación
  subjetiva, no tasa, CAT, comisión ni monto.
- Pago de tarjeta (`tdc_comp_pago`): `1` pagó el total; `2` pagó al menos el
  mínimo y no se atrasó; `3` se atrasó; `4` no ha pagado; `5` no sabe/no
  contestó; `-1` no aplica. Atraso=`{3}`, impago=`{4}`, daño combinado=`{3,4}`.
- Pago de los otros créditos (`hip|per|nom|aut_comp_pago`): `1` siempre pagó
  puntualmente; `2` a veces se atrasó; `3` casi siempre se atrasó; `4` no ha
  podido pagar; `5` no sabe/no contestó; `-1` no aplica. Atraso=`{2,3}`,
  imposibilidad=`{4}`, daño combinado=`{2,3,4}`.
- Problemas (`*_problemas`): `1` sí, `2` no, `-1` no aplica. Su proporción se
  estima entre tenedores con respuesta `1|2`.
- Reclamación (`*_reclamacion`): `1` sí, `2` no, `-1` salto/no aplica. Su
  universo elegible es exclusivamente `*_problemas=1`; el denominador válido
  conserva sólo reclamación `1|2`. Nunca se usan todos los tenedores.

El manual declara pago en 2019, pero la cobertura física histórica ya mostró
que hipotecario, nómina y automotriz tienen cero respuestas válidas. La spec
predeclara esas tres celdas como **NO-LEVANTADA-EN-BYTES** si todos sus
tenedores tienen `-1`/blanco: estimación nula, nunca cero atraso. Cualquier
contradicción material detiene el medidor.

## 3. Estimandos y denominadores

Se producen cuatro archivos tabulares con el mismo núcleo auditable:
`producto | ola | variable_codigos | universo | n_elegible | n_valido |
n_positivo | masa_elegible | masa_valida | masa_positiva |
faltantes_por_causa | estimacion | unidad | alcance`.

1. `estimandos.csv`: distribución completa de pago por sus cuatro códigos;
   atraso, imposibilidad/impago y daño combinado; proporción con problemas; y
   proporción de reclamación en el subuniverso de personas con problema.
2. `conjunta-costo-pago.csv`: las 44 celdas `costo 0..10 × pago 1..4` por
   producto y ola. El denominador es la masa con ambos reactivos válidos. Se
   publican también celdas de masa cero; si el denominador es nulo, la
   estimación queda nula.
3. `costo-dano-2024.csv`: dentro de cada producto y cada nivel válido de costo
   en 2024, la proporción con daño combinado. Ninguna banda se colapsa y todas
   las celdas conservan tamaño y masa, incluidas las pequeñas.
4. `resumen-producto-ola.csv`: vista compacta de atraso, imposibilidad, daño,
   problemas y reclamación para consumo e interpretación.

En todos los casos, `n_elegible` cuenta filas en el universo definido;
`n_valido` cuenta respuestas con código válido; `n_positivo` cuenta la
categoría/numerador. Las masas incluyen sólo pesos finitos y positivos.
`estimacion=masa_positiva/masa_valida`. Los faltantes se desglosan como
`no_levantada`, `salto_no_aplica`, `no_sabe_no_contesto`, `blanco`,
`codigo_invalido` y `peso_no_positivo`; en la conjunta se separan además por
reactivo.

## 4. Precisión, verificación y alcance

No se calculan EE ni IC: los tres documentos no acreditan en el microdato UPM,
estratos o un procedimiento de varianza replicable. El ponderador sí basta
para los puntos descriptivos autorizados. No se imputa ningún valor.

Un control separado con `openpyxl` vuelve a calcular: (a) el cociente de daño
2024 para tarjeta; (b) reclamación hipotecaria 2024 condicionada a problema;
(c) la celda hipotecaria no levantada en 2019; y (d) los cinco conteos y masas
de tenedores 2024 contra la tabla histórica de #734. Este control no comparte
el lector XML del medidor.

Los resultados describen cortes repetidos. Un cambio temporal sólo se comenta
cuando texto, códigos y universo coinciden; no es transición individual. La
asociación costo–daño es descriptiva dentro de tenedores y está sujeta a
selección, autorreporte y confusión. Cero causalidad, cero adopción al motor,
cero sustitución de CAT o lender exacto; `NC-0164` permanece abierta.

