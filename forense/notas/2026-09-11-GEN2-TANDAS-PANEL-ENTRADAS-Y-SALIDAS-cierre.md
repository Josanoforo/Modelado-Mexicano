# GEN2 TANDAS · panel de entradas y salidas ENNViH

Fecha de ejecución: 11 de septiembre de 2026, CAJA/Ubuntu WSL2. Corrida:
`CALC-TANDAS-ENNVIH-PANEL-0001`. Es sucesora de
`CALC-TANDAS-ENNVIH-0001`; no vuelve a presentar sus prevalencias por ola
como medición nueva.

## Resultado

Las tasas son condicionales al panel observado con `cr04` válido en las dos
entrevistas. No son tasas anuales: la pregunta recuerda los últimos 12 meses,
pero las entrevistas están separadas por más tiempo y los periodos de campo
abarcan 2005–06 y 2009–12.

| par | base y transición | n celda / n base | tasa primaria | tasa cruda | ponderación |
|---|---|---:|---:|---:|---|
| 2002→2005–06 | permanece: sí→sí | 437 / 1,909 | 24.54% | 22.89% | `fac_3bl` longitudinal 2005 |
| 2002→2005–06 | sale: sí→no | 1,472 / 1,909 | 75.46% | 77.11% | `fac_3bl` longitudinal 2005 |
| 2002→2005–06 | entra: no→sí | 724 / 12,996 | 7.32% | 5.57% | `fac_3bl` longitudinal 2005 |
| 2002→2005–06 | no entra: no→no | 12,272 / 12,996 | 92.68% | 94.43% | `fac_3bl` longitudinal 2005 |
| 2005–06→2009–12 | permanece: sí→sí | 342 / 1,145 | 29.87% | 29.87% | no ponderado, panel observado |
| 2005–06→2009–12 | sale: sí→no | 803 / 1,145 | 70.13% | 70.13% | no ponderado, panel observado |
| 2005–06→2009–12 | entra: no→sí | 1,325 / 14,298 | 9.27% | 9.27% | no ponderado, panel observado |
| 2005–06→2009–12 | no entra: no→no | 12,973 / 14,298 | 90.73% | 90.73% | no ponderado, panel observado |

En el primer par aportan masa 14,903 de los 14,905 pares válidos; dos casos
sin factor longitudinal positivo quedan en los conteos crudos, no en la tasa
ponderada. En el segundo par la masa es el conteo de 15,443 pares. El archivo
longitudinal 2009 sólo contiene folios de origen `AP` (cohorte 2002) y no
cubre la cohorte inicial completa de 2005, que también contiene incorporados
`BP`; por eso no se restringió post hoc la población ni se sustituyó un factor
transversal.

## Cobertura, attrition y entradas al universo

| par | cohorte Libro IIIB inicial | respuesta inicial válida | identidad en roster/libro final | Libro IIIB final | par válido | pérdida desde respuesta inicial válida |
|---|---:|---:|---:|---:|---:|---:|
| 2002→2005–06 | 19,802 | 19,802 | 18,268 | 15,035 | 14,905 | 4,897 (24.73%) |
| 2005–06→2009–12 | 20,607 | 20,457 | 19,385 | 16,187 | 15,443 | 5,014 (24.51%) |

La retención de un par válido fue 77.32% entre quienes inicialmente dijeron
sí y 74.98% entre quienes dijeron no en 2002→2005–06. En 2005–06→2009–12 fue
76.08% y 75.44%, respectivamente. Las tablas derivadas descomponen la pérdida
por respuesta inicial, edad y sexo en: no respuesta del ítem, persona activa
sin Libro IIIB, muerte registrada, fuera del hogar, otro estado y ausencia de
registro. Ausencia de registro no se renombra como muerte ni como salida de
una tanda.

Además del panel de la cohorte inicial, hubo 5,552 respuestas válidas finales
en 2005–06 y 7,947 en 2009–12 de personas fuera del Libro IIIB inicial. De
ellas, 4,028 y 4,918 ya figuraban en el roster inicial, y 1,524 y 3,029 no.
Son entradas al universo analítico —por edad, respuesta o incorporación al
panel— y están excluidas de las tasas de transición.

## Qué añade frente a las prevalencias por ola

Las prevalencias puntuales anteriores —14.67% en 2002, 8.58% en 2005–06 y
12.04% en 2009–12— mezclan permanencia, salida, entrada, composición cambiante
y ponderadores transversales de cada ola. El nuevo resultado muestra que la
participación individual es poco estable entre entrevistas: aproximadamente
70%–75% de los participantes observados ya no reportó una tanda en la ola
siguiente, mientras 7%–9% de los no participantes entró. El repunte puntual
de la tercera ola es compatible con mayor entrada y algo más de permanencia,
pero esta corrida no identifica cuánto del cambio agregado se debe a esos
flujos, attrition, incorporación al universo o ponderación. No es una
descomposición poblacional de México.

## Identidad y controles

El enlace 2002→2005–06 usa la receta oficial `folio` a ocho dígitos + `ls` a
dos, igual al `pid_link` de diez dígitos de ENNViH-2. Para 2005–06→2009–12 se
inserta el origen `AP` cuando el primer folio termina en `00` y `BP` en los
demás, y se exige igualdad exacta con el `pid_link` de 12 caracteres de
ENNViH-3. Es la regla de las guías ENNViH-2 §5.2.1/§7.2.2 y ENNViH-3 §5.2.1;
no usa orden de fila, nombre, edad aproximada ni hogar actual.

El runner dio `VERIFY: REPRODUCE`, `CONTEXTO=IDENTICO`, 26/26 resultados y
11/11 insumos coincidentes. Un programa independiente que no importa el
medidor reconstruyó las ocho celdas crudas y las cardinalidades de roster:
38,223 filas/36,947 personas/1,276 identificadores repetidos en ENNViH-2 y
46,342/43,194/3,139 en ENNViH-3. Veredicto: `REPRODUCE`.

Las salidas agregadas son `matrices-transicion.tsv`,
`cobertura-attrition.tsv`, `entradas-universo.tsv` y
`flujos-agregados.svg`, junto con `control-independiente.json`. No contienen
identificadores personales.

## Uso y residual

El resultado es descriptivo. No mide incumplimiento, default por turno,
fraude, daño, ni el efecto causal de conocer a la organizadora. No adopta un
parámetro para R8.2, no modifica el motor y no firma objeto científico. Por
la norma vigente clasifica `NO-SIN-FIRMA-DE-OBJETO`; el contador GEN2 no se
incrementa.

Se resuelve únicamente el residual de crosswalk/attrition panel de NC-0037.
La NC permanece abierta porque sigue faltando un ledger mexicano abierto de
grupos, turnos y pagos, y la vía comercial continúa diferida por D18. No
aplican ADR, L0 ni rótulo nuevos: no hay decisión, adopción ni cambio de
gobernanza que firmar.
