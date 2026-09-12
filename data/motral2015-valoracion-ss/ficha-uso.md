# MOTRAL 2015: valoración declarada de seguridad social

## Producto

`estimandos.csv` publica 32 estimandos descriptivos de
`CALC-MOTRAL2015-VALORACION-SS-0001`: P17 afirmativa (total, sexo y edad),
primer lugar de P16 para cada una de cinco prestaciones en esos mismos
cortes, y P17 por acceso a seguridad social del empleo actual entre personas
ocupadas enlazadas con ENOE 2015-T2. Cada fila conserva n, masas ponderadas,
desconocidos, punto, error estándar e intervalo de 95%.

## Universo y lectura permitida

El universo sigue la documentación MOTRAL 2015: personas de 18 a 54 años con
experiencia laboral, entrevista completa (`R_DEF=00`) y condición de
trayectoria válida (`C_TRA` 1 o 2), en la submuestra urbana del módulo. Se usa
`FAC_MOTRAL`. Los errores estándar linealizan una razón con estratos
`CD_A × EST_D` y conglomerados `UPM`; no se aplicó corrección por población
finita y los intervalos normales se truncan a [0,1].

P17 mide una preferencia declarada por un empleo con seguridad social aun si
se deben hacer pagos para obtenerla. No ofrece dos salarios explícitos y no
identifica causalidad ni demuestra que las prestaciones pesen más que
cualquier diferencia salarial. P16 es ordinal: se conserva únicamente el
primer lugar único; no se promedian rangos ni se cuentan cinco filas por
persona. El cruce usa `SEG_SOC` del empleo actual en SDEMT215 y el peso del
módulo, no el factor ENOE.

## Resultado sintético

- P17 afirmativa total: 0.823626705331 (IC95% 0.796632270795–0.850621139866;
  masa 17,498,432 / 21,245,586; n=5,704).
- Primer lugar P16 total: servicio médico 0.474489899955; pensión
  0.199618530173; seguro de vida 0.138649381882; crédito de vivienda
  0.129366701410; accidentes de trabajo 0.057875486580. Las cinco partes
  suman uno sobre 5,698 personas con primer lugar único.
- Entre ocupados enlazados, P17 afirmativa es 0.832233738000 con acceso actual
  a seguridad social (n=2,303) y 0.790530962253 sin acceso (n=2,148). Es una
  comparación descriptiva, no una clasificación de informalidad voluntaria.

## Calidad y trazabilidad

Se observaron 5,696 rankings completos, 2 incompletos con primer lugar único,
6 incompletos sin primer lugar y 0 inconsistentes. Las 7,000 llaves MOTRAL
son únicas; 6,564 enlazan uno-a-uno con SDEM, 436 no enlazan y no hay
duplicados ENOE entre las llaves buscadas. Los 5,704 elegibles enlazan.

La corrida está sellada en
`data/corrida0/CALC-MOTRAL2015-VALORACION-SS-0001/`. El control independiente
`tools/control_motral2015_valoracion.py` reconstruye el cociente P17, la
clasificación de rankings y la cardinalidad del cruce con `dbfread`, sin
importar el lector del medidor.

## Límite respecto de R2.3

Esta capa corrige la afirmación fuente-específica de que MOTRAL 2015 no tenía
preferencia declarada. R2.3
`trabajo.prestaciones.formalidad_pesa_mas_que_salario` sigue sin medirse de
forma estricta: su cierre requeriría elecciones con variación explícita y
predeclarada de salario y prestaciones o una regla de adopción posterior.
