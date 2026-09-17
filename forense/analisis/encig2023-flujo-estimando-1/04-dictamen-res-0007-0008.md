# Dictamen para `RES-0007/0008`

## Decisión recomendada

**Rechazar la correspondencia propuesta con los consumidores actuales.**

- `RES-0008` → `tramite.mordida.con_registro:paga_mordida`:
  **NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR**.
- `RES-0007` → `tramite.mordida.con_registro:tramite_normal`, como complemento
  de pago: **NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR**.

No se recomienda sustituir 0.12/0.88, adoptar el 0.204431 ni usar el nuevo
rango en `milpa`. Sí se recomienda conservar el agregado padre como
descripción de marcas de tipo condicionada al flujo y conservar el sucesor
como conjunto identificado de circunstancia de solicitud/intento por evento.

## Fundamento documental

El cuestionario oficial ENCIG 2023, SHA-256
`65000ad38419da504e46b34a0a2426f218d1ba6e604ad37a14762bbd07881e1e`,
establece en la página PDF/impresa 20 que `P8_3` pregunta por solicitud o
intento directo, petición de tercero e insinuación o condiciones. Si las tres
respuestas son 2 o 9, salta a la sección IX. En la página PDF/impresa 21,
`P8_4` sólo selecciona el tipo de trámite donde se suscitaron esas
circunstancias; `P8_5` pregunta cuántas repeticiones estuvieron afectadas y
`P8_6` distingue “No le dio nada” de los intervalos de monto.

Así, `P8_4=1` no demuestra pago. Tampoco demuestra que todos los eventos de
un tipo repetido fueron positivos. La similitud entre “mordida” y el contexto
de la sección no salva ninguna de las dos faltas de correspondencia.

## Resultado cuantitativo

La clasificación real cerró el universo completo:

- 23,100 eventos (masa 63,712,439) con respuesta válida observada;
- 99,924 (337,524,702) con salto negativo lógico;
- 162 (987,961) con elegibilidad no determinable;
- cero fuera de universo, cero faltantes aplicables y cero contradicciones.

La unión de los 123,186 eventos con 38,966 personas fue exacta y sin
multiplicación. El padre se reprodujo sin cambio: numerador 13,024,773,
denominador 63,712,439 y 0.2044306136200499. Pero 1,195 de los 4,540 tipos
positivos tienen eventos repetidos; replicar la marca no crea desenlaces.

Para una pregunta distinta y correctamente rotulada —circunstancia de
solicitud/intento por evento— las masas forman la partición:

- `W_universo=402,225,102` (`n=123,186`);
- `W_positivo_conocido=5,844,827` (`n=3,345`);
- `W_negativo_conocido=388,212,368` (`n=116,688`);
- `W_desconocido=8,167,907` (`n=3,153`).

La banda básica de la partición es [0.014531, 0.034838]. La restricción
documental “al menos un evento positivo por tipo marcado” estrecha el límite
inferior y deja el conjunto identificado en **[0.021119, 0.034838]**. Es una
banda de faltantes y agregación por tipo, no un IC; no se calculó precisión
muestral nueva.

## Reserva material y opción de mesa

El resultado sucesor sólo sería adoptable después de crear o renombrar un
consumidor cuyo desenlace sea solicitud/intento, no pago. Si mesa necesita
pago efectivo, debe diseñar otro estimando apoyado en la secuencia
`P8_5/P8_6`; este acto no la midió ni la autoriza por implicación.

La reserva residual del conjunto es estrecha pero real: 162 eventos tienen
elegibilidad indeterminada y, dentro de tipos positivos repetidos, no se sabe
qué ocurrencia cargó la circunstancia. Escoger el punto medio, imputar por
canal o heredar el IC del padre no está justificado.
