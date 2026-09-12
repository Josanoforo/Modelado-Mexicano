# `CALC-TANDAS-ENNVIH-PANEL-0001` — permanencia, entrada y salida de tandas

**Acto:** `GEN2-TANDAS-PANEL-ENTRADAS-Y-SALIDAS`, CAJA. Esta spec y el
medidor se congelan antes de observar las matrices o tasas de transición. La
inspección previa se limitó a documentación oficial, esquemas, códigos,
cardinalidad de identificadores y cobertura de ponderadores; no se tabularon
cruces de `cr04` entre olas.

## Identidad acreditada antes del estimando

La guía oficial de ENNViH-2, §5.2.1 y §7.2.2, ordena construir en ENNViH-1
`pid_link = string(folio, "%08.0f") + string(ls, "%02.0f")`. En ENNViH-2 ese
identificador conserva el folio y LS originales aunque la persona cambie de
hogar. Los hogares originales terminan en `00`; un hogar desdoblado sustituye
esos dos dígitos por el LS del miembro que lo originó. Los LS del roster
original no se reutilizan. Los renglones de quienes salieron permanecen en el
hogar de origen con `ls01a=3`; si la persona fue localizada en otro hogar, su
renglón actual porta el `pid_link` original.

La guía oficial de ENNViH-3, §5.2.1, extiende el identificador a 12 caracteres:
seis dígitos, código de origen del hogar (`AP`=2002, `BP`=2005,
`CP`/`CH`=2009), dos dígitos del hogar y dos del primer LS. Para comparar
ENNViH-2 con ENNViH-3 se inserta `AP` en un `pid_link` de 2005 cuyo folio de
primer registro termina en `00`, y `BP` en los demás. Se exige coincidencia
exacta con el `pid_link` de 12 caracteres de ENNViH-3. `CP`/`CH` son entradas
de 2009 y nunca se fuerzan contra una persona de 2005.

La inspección estructural encontró: `iiib_cr` tiene 19,802 llaves únicas
`folio+ls` en 2002, 20,607 `pid_link` únicos en 2005–06 y 24,927 únicos en
2009–12. El roster 2005 tiene 38,223 filas; sus 1,277 `pid_link` blancos son
exclusivamente `ls01a=3` en hogares terminados en `00`. Reconstruir para esas
filas la llave oficial del roster produce 36,947 personas: 1,276 aparecen en
dos filas (`3` en origen y `4` en el hogar donde fueron halladas) y una queda
sola. El roster 2009 tiene 46,342 filas, 43,194 personas por `pid_link`, 3,139
identificadores repetidos y máximo tres filas por persona. Esos duplicados se
colapsan como estados de una misma persona; una fila de roster jamás se cuenta
como otra persona ni como respuesta.

No se usa orden de fila, nombre, edad aproximada ni coincidencia de hogar
actual. Una violación de formato, unicidad de `iiib_cr` o del caso acreditado
para un `pid_link` blanco aborta.

## Universo y pregunta

Unidad: persona informante directa del Libro IIIB en la ola inicial. La
presencia en `iiib_cr.dta` define la cohorte elegible inicial, pues el Libro
IIIB se administra a personas de 15 años o más. La edad de portada se usa para
describir 15–29, 30–49, 50+ y fuera/faltante; no se usa para borrar una
respuesta de una persona incluida por el propio instrumento. Sexo (`ls04`) se
toma del roster de la ola inicial y se agrupa como hombre (`1`), mujer (`3`) u
otro/faltante.

En cada ola, `cr04` pregunta si en los últimos 12 meses la persona participó en
alguna tanda. Respuestas válidas: `1=sí`, `3=no`. Otro código o faltante es no
respuesta del ítem; nunca se imputa a cero. Se estiman por separado los pares
2002→2005–06 y 2005–06→2009–12. La distancia entre entrevistas no es un año y
las tasas no se anualizan.

## Estimandos y exclusiones

Para cada par, entre personas de la cohorte inicial con `cr04` válido en ambas
olas, se publica la matriz 2×2 y:

- permanencia: `P(cr04_t1=1 | cr04_t0=1, par válido)`;
- salida: `P(cr04_t1=3 | cr04_t0=1, par válido)`;
- entrada: `P(cr04_t1=1 | cr04_t0=3, par válido)`;
- no entrada: `P(cr04_t1=3 | cr04_t0=3, par válido)`.

Cada celda publica `n`, número que aporta masa y masa analítica. También se
publican las versiones no ponderadas dentro del JSON de matriz. El denominador
es el panel observado con respuesta válida en las dos entrevistas: no es la
cohorte completa ni una población nacional sin selección.

Se separan: cohorte elegible inicial; respuesta inicial válida; identidad
presente en roster o Libro IIIB de seguimiento; Libro IIIB de seguimiento; par
válido. Entre quienes tienen respuesta inicial válida, la pérdida analítica se
descompone, con esta precedencia:

1. Libro IIIB y `cr04` válido: `RESPUESTA-VALIDA`;
2. Libro IIIB sin `cr04` válido: `NO-RESPUESTA-ITEM`;
3. roster actual (`ls01a` 1/4/6) sin Libro IIIB:
   `SIN-RESPUESTA-LIBRO-IIIB`;
4. muerte (`ls01a=0` o `ls19d=3`) sin registro actual ni Libro IIIB:
   `MUERTE`;
5. salida del hogar (`ls01a` 3/5) sin Libro IIIB:
   `FUERA-HOGAR-SIN-LIBRO-IIIB`;
6. otra fila de roster, o ninguna fila:
   `OTRO-ROSTER-SIN-LIBRO-IIIB` / `SIN-REGISTRO-SEGUIMIENTO`.

`SIN-REGISTRO-SEGUIMIENTO` no se renombra como muerte ni como abandono de una
tanda; puede contener no localización o no respuesta del hogar que estos
archivos no permiten separar. La retención y sus componentes se tabulan por
participación, edad y sexo iniciales, con denominador de respuesta inicial
válida.

Las respuestas válidas en la ola final cuyo identificador no pertenece a la
cohorte inicial son entradas al universo analítico y quedan fuera de las tasas.
Se distingue si la persona ya figuraba en el roster inicial sin Libro IIIB
(por ejemplo, menor que envejeció al universo o no respuesta del libro) o si
no figuraba en ese roster. No se atribuye un motivo individual adicional.

## Ponderación

Para 2002→2005–06 se usa `fac_3bl` del archivo longitudinal del Libro IIIB de
2005. La documentación oficial declara que estos factores se aplican a las
personas seleccionadas en 2002 y encontradas en el segundo levantamiento, que
es la población de origen del par. Valores ausentes, no finitos o no positivos
se excluyen sólo de la masa y tasa ponderada y se cuentan; permanecen en la
matriz no ponderada.

Para 2005–06→2009–12 el estimando abarca toda la cohorte elegible de 2005,
incluidos miembros incorporados entonces. La nota oficial dice que los
factores longitudinales 2009 siguen el procedimiento de 2005, limitado a la
muestra seleccionada en 2002; el archivo confirma que sus 30,525 filas son
exclusivamente folios `AP` y tiene cinco llaves duplicadas. No corresponde a la
población exacta del par. Por ello este par es no ponderado (masa=conteo), sin
sustituir factores transversales ni restringir post hoc la cohorte.

No se estiman intervalos de diseño, no se modela attrition y ninguna pérdida se
rellena como no participación.

## Controles, salida y alcance

El control independiente reconstruye las dos matrices crudas y cardinalidades
sin importar el medidor. Las vistas derivadas son dos TSV de matrices y
cobertura/attrition, una TSV de entradas y un SVG agregado. Ninguna salida
incluye identificadores de persona.

Este CALC sucede a `CALC-TANDAS-ENNVIH-0001`: responde estabilidad, entrada y
salida entre entrevistas, no repite sus tres prevalencias puntuales. Es
descriptivo; no mide tasa anual, incumplimiento, fraude, turno, daño, efecto de
conocer a la organizadora ni causalidad. No adopta un parámetro para R8.2 y no
generaliza el panel observado a México.
