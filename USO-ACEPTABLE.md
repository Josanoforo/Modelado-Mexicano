# Uso aceptable

**Esto no es una licencia y no pretende serlo.** Una licencia regula la copia; el
riesgo de este repositorio no está en que alguien lo copie, sino en lo que haga con
él. Las restricciones que importan aquí no son ejecutables por vía legal. Se
declaran de todos modos, porque un modelo que hace afirmaciones sobre poblaciones y
sale al mundo sin decir para qué no sirve es un modelo publicado a medias.

Lo que sigue es la posición explícita del autor. Quien la ignore no infringe la
licencia; simplemente no puede alegar que no se le dijo.

---

## Qué es este modelo

`canon/modelo-decision-v3_3.md` contiene 49 reglas SI-ENTONCES que predicen conducta
esperada por segmento —clase, región, edad, género, escolaridad, formalidad— con una
etiqueta de fuerza de evidencia y una probabilidad asociada.

**De sus 144 números, 4 están medidos. De sus 15 coeficientes de generador, ninguno.**
El resto son valores asignados por juicio, derivados de literatura, sin calibrar
contra datos primarios. Una regla `[FUERTE]` significa que la literatura la sostiene
bien, no que su probabilidad esté medida.

Esto es una síntesis de literatura con estructura de modelo. No es un instrumento
validado.

---

## Usos para los que este modelo no debe emplearse

Ninguno de estos está prohibido por la licencia. Todos son, en opinión del autor,
usos indebidos:

**Decisiones sobre personas concretas.** Otorgamiento o denegación de crédito.
Contratación, despido o promoción. Suscripción de seguros. Fijación de precios
individualizada. Cualquier sistema de puntuación que asigne a una persona un valor
derivado de su segmento y actúe sobre él. El modelo describe distribuciones
poblacionales; aplicarlo a un individuo es un error de categoría, y uno con
consecuencias.

**Perfilamiento de grupos protegidos.** Las segmentaciones del corpus —por clase,
región, escolaridad, formalidad laboral— correlacionan con características
protegidas por la ley mexicana. Usarlas como proxy es discriminación con un paso
intermedio.

**Vigilancia, control migratorio o inteligencia policial.**

**Manipulación política o comercial dirigida** que explote los mecanismos descritos
—desconfianza institucional, ansiedad de estatus, sanción social horizontal— para
inducir conductas contra el interés de las personas afectadas.

**Cualquier presentación que oculte la incertidumbre.** Citar una probabilidad del
modelo sin su tier y sin su marca de procedencia convierte un juicio informado en un
dato duro. Es la forma más común y más fácil de hacer daño con esto.

---

## Una advertencia sobre la inferencia genética

El corpus incluye material de genómica de poblaciones. El reglamento del programa
(`instrucciones-proyecto-v2.md`, Bloque A) prohíbe expresamente la inferencia
ascendencia → conducta de grupo, y sostiene lo contrario: la variación de mestizaje
en México es tal que la genética de poblaciones, bien leída, es argumento **contra**
el determinismo, no a favor.

Cualquier uso de este material para sostener diferencias conductuales entre grupos
por ascendencia contradice de forma directa lo que el corpus afirma. No es una
lectura discutible del material: es su inversión.

---

## Límites declarados que conviene conocer antes de usar nada

- El corpus **sobre-muestrea al clasemediero urbano formal** y sub-muestrea al
  popular informal, que es el peso demográfico dominante. Está declarado, no
  corregido.
- El **sistema indígena-comunal vivo** (asamblea, cargos, tequio, usos y costumbres)
  queda **fuera por diseño**. No es un hueco a rellenar: es otro orden institucional
  que el modelo no cubre y sobre el que no debe extrapolarse.
- Parte de la evidencia proviene de **muestras mexicano-americanas**, sujetas a
  aculturación y selección migratoria. Está marcada `(b)` donde se detectó; la suite
  documenta que el marcado es incompleto.
- **Cero datos primarios propios.**

---

## Si vas a usarlo de todos modos

Cita con `CITATION.cff`. Trae el tier y la marca de procedencia junto a cualquier
cifra. Lee `AVISO-DE-ALCANCE.md`. Y si tu uso cae en la zona gris, abre un issue y
pregunta — es más barato para todos que el resultado.
