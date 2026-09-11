# `CALC-TANDAS-ENNVIH-0001` — participación individual en tandas

**Acto:** `GEN2-TANDAS-MEDICION-ACADEMICA`, CAJA. Esta spec y su medidor se
congelan en un commit anterior a la primera lectura de valores de los
microdatos. La inspección previa se limitó a manifiesto, miembros de los ZIP,
metadatos de columnas, cuestionarios, codebooks y guías de usuario.

## Estimando primario

Por separado para ENNViH-1 (2002), ENNViH-2 (levantada desde mediados de 2005
y concluida en 2006) y ENNViH-3 (iniciada a mediados de 2009 y concluida en
2012), estimar la proporción ponderada de personas de 15 años o más que
contestó sí a:

> En los últimos 12 meses, ¿ha participado usted en alguna tanda?

Unidad: persona que respondió el Libro IIIB. Numerador: `cr04=1`.
Denominador: `cr04` en `{1,3}` y factor puntual `fac_3b` finito y positivo.
Punto: `sum(fac_3b * 1[cr04=1]) / sum(fac_3b)`. Se publica también `n`, casos
afirmativos, masa ponderada, faltantes de respuesta y de ponderador, y la
proporción no ponderada como tabulación auxiliar. No se promedian olas: cada
una representa su propio periodo y población puntual.

El cruce dentro de cada ola usa exclusivamente la identidad oficial
`folio + ls` de esa ola entre `iiib_cr.dta`, `iiib_portad.dta` y el ponderador
del Libro IIIB. `pid_link` no se usa. Las llaves se canonizan como texto
(`folio` a 8 dígitos y `ls` a 2 en 2002/2005; las llaves alfanuméricas 2009 se
conservan). El primer intento, posterior al commit de congelamiento, abortó
antes de producir cifras porque 2002 guarda la misma llave numérica en crédito
y textual con ceros en ponderadores. El diagnóstico posterior mostró además
duplicados exactos de llave en ponderadores 2005/2009: se colapsan sólo si hay
cero o un único valor positivo distinto de `fac_3b`; más de uno aborta. Esta
corrección de representación no depende de resultados. Duplicados restantes
abortan. La ausencia de factor puntual —observada en personas seguidas que no
pertenecen al universo puntual— se cuenta y excluye, como fijó desde el inicio
la definición del denominador; una edad ausente sólo excluye del corte etario.

## Cortes mínimos

Se repite el punto primario en tres grupos de la edad declarada en la portada
del mismo Libro IIIB: 15–29, 30–49 y 50 años o más. Edades menores de 15,
mayores de 120 o no numéricas salen sólo del corte, contadas y no imputadas;
permanecen en el estimando total si `cr04` y `fac_3b` son válidos.

## Cantidades secundarias

Sólo entre participantes (`cr04=1`) y con el indicador de monto igual a 1:

- 2002/2005: monto aportado (`cr05a_2`), monto recibido (`cr05b_2`) y monto
  que recibirá (`cr05c_2`) se mantienen separados. Se reportan media y mediana
  ponderadas, `n` y masa. Son pesos nominales del periodo de cada ola; no se
  interpretan como cuota periódica ni se deflactan.
- 2009–2012: `cr05_2` es el monto recibido **o por recibir** de la última
  tanda. No se denomina aporte. Se reporta en pesos nominales.
- 2009–2012: la duración de la última tanda se toma de `cr05a_1` y de la
  columna correspondiente a días/semanas/meses. Se homologa a días con
  `1`, `7` y `365.25/12`, respectivamente, y se reportan media/mediana
  ponderadas, `n`, masa y conteo por unidad original. Esto no es periodicidad
  de aportación.

Montos/duraciones no finitos o negativos se excluyen y cuentan. Cero se
conserva como respuesta numérica. No hay winsorización ni imputación.

## Diseño, controles y límites

Los ZIP de ponderadores sólo ofrecen `folio`, `ls`, `fac_3b`; no ofrecen UPM,
estrato ni réplicas. Se publican puntos descriptivos sin IC. No se hereda
`folio` como conglomerado, no se inventa un diseño y no se llama conservador a
un intervalo inexistente.

Control independiente predeclarado: las frecuencias crudas de `cr04` deben
reproducir los codebooks del Libro IIIB: 2002 `sí=2,469`, `no=17,333`;
2005–06 `sí=1,505`, `no=18,952`; 2009–12 `sí=2,497`, `no=20,960`. Cualquier
desacuerdo aborta.

La medición es descriptiva. No mide conocimiento de la organizadora,
reputación, turno, cuota incumplida, sanción ni causalidad; `rg08_11` queda
fuera porque es una expectativa hipotética. Su uso permitido en R8.2 es un
escenario/base de prevalencia de participación y de exposición potencial al
mecanismo, sujeto a firma del objeto. No cambia probabilidades del motor.
