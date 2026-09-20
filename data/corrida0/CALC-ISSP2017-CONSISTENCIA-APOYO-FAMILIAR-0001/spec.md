# Prerregistro · consistencia de elección familiar (ISSP México 2017)

`CALC-ISSP2017-CONSISTENCIA-APOYO-FAMILIAR-0001` describe, sin inferencia
causal, respuestas de la misma persona a Q7a--e (`v21`--`v25`) de ZA6980
v2.0.0. La exposición previa es explícita: el CALC de redes de apoyo ya
publicó los marginales de estas cinco variables; esta corrida no es ciega.

Universo: registros México (`country=484`, `c_alphan=MX`), una persona por
`CASEID`, con peso numérico finito positivo. Respuesta válida es únicamente
1--7. Familia es 1+2; 7 significa ninguno; 8, 9 y vacío no son no-familia.

Productos fijados antes de leer filas: (1) en cinco respuestas válidas,
conteo 0--5 de situaciones con familia, total y SEX=1/2 con residuo;
(2) las diez matrices nativas 7x7 sobre ese universo completo y la
sensibilidad de cada pareja sobre sus dos respuestas válidas; (3) sus tablas
familia/no-familia, acuerdo, discordancias orientadas y condicionales. Las
matrices no se estratifican por sexo. No se calculan EE, IC, bootstrap ni
pruebas: `EE-IC-NO-DISPONIBLES-DISENO-NO-ACREDITADO`.

Esto mide consistencia transversal de elecciones hipotéticas. No es una
escala validada, estabilidad temporal, apoyo recibido, obligación ni efecto
causal. Los universos común y por-pareja se etiquetan y no se comparan como
cambio conductual.
