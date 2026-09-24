# ADR raíz · ASTRA5-U2 ENDIREH · 23/septiembre/2026

**Decisión propuesta para mesa, sin adopción:** el producto ENDIREH es un conjunto de pisos descriptivos retrospectivos por cuestionario, ámbito y ventana. Cada cifra publicada lleva CALC, RESULT, hash, factor, diseño, soporte y supresión. La matriz [conducta × ola × ámbito](endireh-matriz-conducta-ola-ambito.tsv) es el índice de mediciones y dictámenes; los seis TSV sucesores son tablas de consumo. Los nueve CALC de #1093 permanecen sellados e intactos.

## Fundamentación y alcance

1. **Universo y estructura.** 2021/2016 separan A1/A2, B1/B2, C1 y C2 según pregunta; 2011 separa A/B/C, y 2006 MC/MD/MS. 2003 entrevista mujeres de 15+ con pareja residente. Nunca se imputa «no» por salto, blanco, 9 o embarazo no ocurrido.
2. **Ventanas.** Vida de relación, desde octubre del año anterior, últimos cinco años de empleo, año escolar/laboral y situación al entrevistar son objetos distintos. Una unión de actos es por mujer con elegibilidad común; no es suma de prevalencias. El agregado 70.1% U0 carece de contraste directo en este paquete.
3. **Diseño.** Los CALC 2006–2021 usan sus factores, estratos y UPM propios; 200 réplicas agregadas por celda publicable y reglas de supresión fijadas antes del dato. El diseño 2003 está publicado por INEGI, pero el ZIP distribuido no liga cada registro a UPM y estrato, de modo que falta el IC exigido. Se dicta dependencia externa y ninguna tabla 2003.
4. **Temporalidad.** Los puntos e IC son retrospectivos dentro de ola. No se calcula IC predictivo, cambio social, calibración ni adopción: `SIN-HISTORIA-PARA-CALIBRAR`. Un análisis futuro debe homologar actos/universos y probar una transición no usada en el ajuste.
5. **Publicación.** Los RESULT están sellados en disco y sus tablas preparadas para revisión. Estado: **sellada en disco, no registrada** hasta el canal de publicación y la firma de mesa; esta rama crea PR sin fusionar.

## Alternativas examinadas y razón de descarte

- Sumar prevalencias escolar, laboral, comunitaria, familiar y pareja para reproducir 70.1% duplicaría a mujeres expuestas en varios ámbitos y mezclaría denominadores.
- Tratar 2016 7.3 como parte de actos interpersonales 7.9 o 2021 8.3 como 8.9 mezclaría discriminación por embarazo con violencia interpersonal. Se midieron por CALC separados.
- Usar `LLAVE` 2003 como UPM por interpretación de dígitos no documentada inventaría el diseño. Solo una llave oficial por registro o réplicas equivalentes resolvería NC-2003.
- Forzar 2006/2011 a códigos 2016/2021 cambiaría actos, elegibilidad y ventanas. Cada spec se basó en su cuestionario/FD.

Esta decisión no modifica el contador de `celdas_validadas` ni los procedimientos anteriores. Aislados sobre la base de la rama, los seis CALC nuevos pasaron de 219 a 225 corridas selladas y de 65,567 a 65,579 RESULT GEN2 sellados. Después de integrar el `origin/main` concurrente (último: `d2fa8efd`, #1098), la vista derivada final es 234 corridas y 65,599 RESULT GEN2; `celdas_validadas=219`. El [registro de cierre](endireh-registro-cierre.tsv), el [FP/NC](endireh-fp-nc.md) y el recibo documentan sellos, replay y residuales.
