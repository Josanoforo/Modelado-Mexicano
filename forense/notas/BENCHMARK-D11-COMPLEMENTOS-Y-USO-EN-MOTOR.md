# D11 · Complementos, proporciones y uso en el motor

Fecha: 10 de septiembre de 2026. Propuesta metodológica para dirección y mesa; no es una firma de adopción. Investigación web con fuentes primarias. Objeto inmediato: NC-0085 / RES-0028; aplicación relacionada: D03, D04 y D05.

**Principio: una transformación puede ser un estimador válido sin convertirse en una segunda observación independiente.**

## 1. Qué cambia respecto de la recomendación anterior

La regla «derivado, no medición independiente» es útil para el linaje. Sería incorrecto convertirla en «un complemento nunca sirve para estimar o alimentar el motor». La decisión depende del evento que representa, su población y el tratamiento de su incertidumbre.

**Observado en el repo:** la ficha D11 identifica RES-0028 como complemento dentro de un recorte ENVIPE; #670 resolvió complementos ENCIG, con otro alcance. **Interpretación:** copiar aquella decisión no demuestra que aquí “lo demás” signifique “otra razón” del cuestionario. **Consecuencia:** reconstruir la partición de este objeto antes de adoptar. La codificación de los R recientes —denominador BP1_23 01..09— tampoco debe trasladarse al consumidor histórico sin comprobar que sea el mismo estimando. [Registro NC-0085](https://github.com/Josanoforo/Modelado-Mexicano/blob/e81aa27bf3999989fc029a18e49352f27088e230/forense/no-corrido.tsv).

## 2. Benchmark: qué hacen las referencias

| Fuente primaria consultada | Hallazgo relevante | Aplicación propuesta |
|---|---|---|
| Parker, Talih, Malec y colaboradores, NCHS, *Data Presentation Standards for Proportions* (2017; actualización 2021), sección “Complementary Proportions” | Una proporción y su complemento comparten error estándar y anchura de intervalo, pero pueden diferir en precisión relativa y utilidad de presentación. | Evaluar el significado y la fiabilidad de cada etiqueta; conservar la dependencia matemática. No copiar umbrales institucionales de publicación como reglas universales del motor. [Informe](https://www.cdc.gov/nchs/data/series/sr_02/sr02_175.pdf). |
| CDC/NHANES, tutorial oficial de estimación de varianza | Pesos, estratos y conglomerados cumplen funciones distintas. El análisis de un subgrupo necesita conservar información del diseño completo. | No obtener la incertidumbre de un dominio como si fuera una muestra aleatoria simple aislada. [Tutorial](https://wwwn.cdc.gov/nchs/nhanes/tutorials/varianceestimation.aspx). |
| Lumley, documentación de `svyciprop` | Hay métodos específicos para intervalos de proporciones, especialmente cerca de los extremos; los métodos descritos tienen límites en proporciones exactamente 0 o 1. | Elegir y registrar el método antes de evaluar resultados; evitar que un intervalo degenerado se interprete como certeza. [Referencia](https://r-survey.r-forge.r-project.org/pkgdown/docs/reference/svyciprop.html). |
| West, Berglund y Heeringa (2008), *A closer examination of subpopulation analysis of complex-sample survey data* | El artículo compara dos formas de analizar dominios y sus consecuencias inferenciales. Se consultó la ficha y el resumen del editor, no el texto completo. | Referencia académica para profundizar la implementación de dominios; las recomendaciones operativas aquí se apoyan además en el tutorial oficial leído. [Artículo](https://www.stata-journal.com/article.html?article=st0153). |

Esto es un benchmark dirigido al problema, no una revisión sistemática exhaustiva.

## 3. Contrato matemático propuesto

Las expresiones siguientes son derivaciones algebraicas de esta propuesta.

Para un evento binario observado en un universo elegible fijo U, con los mismos pesos y reglas de validez:

\[
\hat p=\frac{\sum_{i\in U}w_iY_i}{\sum_{i\in U}w_i},\qquad
\hat q=1-\hat p.
\]

Entonces:

\[
\operatorname{Var}(\hat q)=\operatorname{Var}(\hat p),\qquad
\operatorname{Cov}(\hat p,\hat q)=-\operatorname{Var}(\hat p).
\]

Si el intervalo de p es [l,u], el intervalo obtenido por la misma transformación para q es [1−u,1−l]. Las réplicas también se transforman: q[b]=1−p[b]. No se generan dos incertidumbres independientes.

Para varias categorías mutuamente excluyentes, q=1−Σp[j] exige propagar también las covarianzas entre categorías. Para eventos que se solapan, la unión es p(S∪E)=p(S)+p(E)−p(S∩E). Entrega no es el complemento de solicitud.

**Faltantes:** 1−p(Y | respuesta válida) describe el complemento entre respuestas válidas. No recupera automáticamente el comportamiento de quien no respondió, no fue elegible o no recibió la pregunta. La falta de respuesta se muestra con su propio denominador y, cuando sea material, sensibilidad.

## 4. Qué debe hacer el motor

1. **Resolver el contexto antes de aplicar la tasa.** Un parámetro entre personas con contacto con funcionarios se utiliza después de activar ese contexto. No se aplica a toda la población como probabilidad incondicional.
2. **Conservar el significado literal.** El complemento de “miedo, extorsión o desconfianza” es “las demás razones incluidas en este universo”, salvo prueba de que coincide con una categoría específica del cuestionario.
3. **Citar un origen y una transformación.** En las superficies existentes: CALC/RESULT padre, fórmula, universo, fuente/ola, ponderador, exclusiones y consumidor. Mantener el rótulo DERIVADO cuando corresponda a la gramática vigente; sin estado paralelo ni contador nuevo.
4. **Compartir la incertidumbre.** Para una decisión binaria, usar una probabilidad y su complemento; no sortear ambos parámetros por separado. Para solicitud y entrega, estimar una distribución conjunta o transiciones condicionadas según las preguntas disponibles.
5. **Separar conteo y adopción.** Una transformación no duplica evidencia independiente. La forma de contabilizar resultados técnicos sigue las reglas del registro; la adopción cita el uso concreto, sin inflar el número de mediciones independientes.

En D03, la implementación debe probar las cuatro combinaciones solicitud/entrega. No puede imponer “toda entrega estuvo precedida de solicitud” si el instrumento no lo garantiza. En D05, la tasa poblacional requiere ponderar cada dominio por su masa poblacional; el promedio simple de tasas de trabajadores y no trabajadores no sirve.

## 5. Casos límite y validación propuesta

| Caso | Resultado exigido |
|---|---|
| p=0.30, intervalo [0.25,0.35], mismo universo | q=0.70, intervalo [0.65,0.75]; cada réplica suma uno. |
| Se excluyó una categoría real antes de calcular p | El complemento no se llama “todos los demás” de la población original. Se publica el recorte. |
| Una variable es 9/NS/NR | No se convierte automáticamente en cero; la regla lógica puede resolver una unión si el otro componente es afirmativo, pero no todas las combinaciones faltantes. |
| p(S)=0.20, p(E)=0.15 y p(S∩E)=0.10 | Unión=0.25; ni 0.35 ni 0.80. |
| Entrega afirmativa y solicitud negativa | Combinación admitida o exclusión justificada por el instrumento; nunca borrada para imponer una teoría. |
| Dominio vacío, peso inválido o denominador cero | No estimable, con razón y alcance. |
| Proporción observada 0 o 1 | No afirmar certidumbre poblacional a partir de varianza empírica cero; aplicar el método y advertencia especificados. |
| Dos consumidores heredan el mismo RESULT | Comparten linaje y dependencia; no cuentan como dos confirmaciones independientes. |
| Cambia ola, unidad o regla de elegibilidad | Se requiere correspondencia demostrada o estimando sucesor. |

Estas pruebas se incorporan al cálculo/consumidor afectado. No requieren un sistema general nuevo.

## 6. Encargo de aplicación de D11

**Resultado:** una ficha sucesora para RES-0028 con su partición completa y una recomendación verificable de uso en el motor.

**Entrada:** este benchmark; NC-0085; consumidor RES-0028; cálculo padre; cuestionario, diccionario y reglas de exclusión de esa ola; decisión #670 como antecedente acotado.

**Trabajo:** reconstruir numerador y denominador; tabular qué incluye y excluye cada código; comprobar que fórmula y etiqueta representan el mismo evento; reproducir punto e incertidumbre con el diseño disponible; documentar el uso del motor y la dependencia con su padre. Si no coincide con una categoría literal, proponer el nombre descriptivo preciso. No recalcular todo ENVIPE.

**Cierre:** la solicitud de benchmark queda cumplida al registrar este documento y la recomendación. NC-0085 sólo se cierra cuando el tratamiento elegido se propaga al consumidor con cita, alcance y merge. Mesa pidió investigar: este informe no inventa su firma para adoptar una alternativa.

**Recomendación a mesa:** permitir complementos válidos con linaje e incertidumbre compartida; para RES-0028, adoptar únicamente la etiqueta y universo que la reconstrucción demuestre. Si se quiere “otras razones” sobre una población diferente, abrir un estimando sucesor.
