# Puente a 40 · N35 preferencias laborales

## Oferta exacta

- `CALC-MOTRAL2015-VALORACION-SS-0001--cca8297b03bd`, 42 RESULT sellados,
  de los cuales 32 son estimandos descriptivos y 10 son diagnósticos.
- Resultado principal: `RESULT-MOTRAL15-P17-TOTAL-P` = 0.823626705331
  (IC95% 0.796632270795–0.850621139866; 17,498,432 / 21,245,586;
  n=5,704).
- Prioridad principal: `RESULT-MOTRAL15-P16-FIRST-TOTAL-MEDICO-P` =
  0.474489899955; las otras cuatro partes y todos los cortes están en
  `data/motral2015-valoracion-ss/estimandos.csv`.
- Cruce actual: `RESULT-MOTRAL15-ENOE-P17-CON-ACCESO-P` = 0.832233738000
  y `RESULT-MOTRAL15-ENOE-P17-SIN-ACCESO-P` = 0.790530962253.

## Uso permitido

Descripción de valoración declarada en MOTRAL 2015 y comparación descriptiva
por cobertura de seguridad social del empleo actual enlazado con ENOE. No es
un efecto causal, no clasifica informalidad voluntaria, no calibra el motor y
no autoriza adopción.

## Qué cambió y qué falta

Se corrige sólo la afirmación de que MOTRAL 2015 no contiene preferencia:
P16 ordena cinco prestaciones y P17 pregunta por empleo con seguridad social
aun pagando. R2.3 estricta continúa `EXISTE-NO-SATISFACE`: P17 no varía
salarios explícitos.

El paper mexicano de marzo de 2026 sí publica una elección DCE con ingreso y
prestaciones: WTP base por seguridad social = 0.240 del ingreso (EE 0.023),
transcripción, no reproducción. No hay paquete público localizado y el
“Appendix C” anunciado no está en el PDF obtenido.

## Opción concreta de regla futura

Sin sustituir R2.3: abrir una regla separada del tipo
`trabajo.formalidad.wtp_seguridad_social_dce`, cuya unidad sea la WTP como
fracción del ingreso para el cambio `sin → con seguridad social`, condicionada
al menú, población urbana 25–64 y versión del diseño. Congelar primero el
estimando, el tratamiento del trap, la escala de ingreso, el transporte y el
criterio de adopción; exigir el paquete reproducible antes de usar el 0.240
como parámetro.
