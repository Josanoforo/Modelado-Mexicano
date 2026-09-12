# Ficha de compatibilidad: experimento mexicano de elección laboral

## Identidad y versión

Campos-Vázquez, Duval-Hernández, Juarez y García-Guzmán, *Do Workers Value
Formal Jobs? A Discrete Choice Experiment in Mexico*. Se conservaron el
paper de marzo de 2026 y la presentación creada el 18 de agosto de 2026,
ambos publicados desde la sesión EEA-ESEM 2026. Sus identidades están en
`fuentes-experimento.tsv` y `data/manifiesto.yaml`; los PDF quedan fuera de
Git en la raíz lógica `data_raw`.

## Población, muestra y elección

Encuesta cara a cara en hogares durante septiembre–octubre de 2024. El marco
cubre personas de 25–64 años de las diez áreas metropolitanas más grandes de
México; una persona elegible se seleccionó aleatoriamente por hogar usando
edad y sexo. El paper reporta 4,833 participantes (3,557 ocupados). Cada
persona enfrentó cuatro pares experimentales y una pregunta trampa; debía
elegir A o B, sin opción de omitir ni elegir ninguna. Las estimaciones
principales conservan las 3,922 personas (81%) que contestaron correctamente
la trampa.

## Atributos y niveles

| Atributo | Niveles publicados |
| --- | --- |
| Seguridad social | sí; no |
| Duración | permanente; contrato anual renovable |
| Jornada/horario | 20 h flexible; 20 h fijo; 40 h flexible; 40 h fijo |
| Autonomía | completa; alguna; ninguna |
| Traslado | 15; 20; 60 minutos |
| Ingreso mensual | 0%; +10%; +20%; +25% respecto del ingreso actual o imputado, escalado por horas |

Las opciones no se etiquetaron como “formales” o “informales”. El diseño
D-eficiente produjo 256 pares divididos en 64 bloques; a nivel persona se
aleatorizaron bloque, orden de los pares, posición izquierda/derecha y la
ubicación de la trampa entre el tercer y quinto menú.

## Resultados publicados pertinentes

El modelo logit condicional reporta WTP como proporción del ingreso mensual,
con errores estándar agrupados por persona. En el modelo base (15,688
observaciones; 3,922 personas), seguridad social vale 0.240 (EE 0.023),
contrato permanente 0.125 (0.015), horario de 20 h flexible 0.056 (0.023),
autonomía alguna 0.252 (0.024), autonomía completa 0.254 (0.024); 40 h fijo,
40 h flexible y traslado de 60 minutos requieren compensaciones de 0.172,
0.119 y 0.114, respectivamente. Las cifras son transcripciones de la tabla 2
del paper, no una reproducción.

El mismo documento reporta valoración de seguridad social de 0.261 entre
ocupados formales y 0.175 entre informales, y estima que 24%–32% de quienes
tienen empleos informales estarían mejor en su empleo observado que en los
contrafactuales formales definidos. Estos resultados dependen de cambios y
contrafactuales concretos: no autorizan una preferencia universal de
prestaciones frente a cualquier salario.

## Reproducibilidad y residual exacto

La búsqueda dirigida revisó la sesión EEA-ESEM, las páginas públicas de
Robert Duval-Hernández y Laura Juárez, y búsquedas exactas del título en OSF,
Dataverse, Zenodo y GitHub. Al 11 de septiembre de 2026 no se identificó un
paquete público de cuestionario, datos ni código del estudio. El paper dice
que el instrumento completo está en “Appendix C”, pero el PDF obtenido tiene
48 páginas, termina en Appendix B y no contiene ese apéndice.

Residual: solicitar, sin enviar desde este acto, la versión exacta de marzo de
2026 del cuestionario/Appendix C, el archivo de asignación de 64 bloques, el
microdato anonimizado y el código que produce las tablas 2–5. Sólo después se
podrían reproducir las tablas pertinentes y evaluar una regla futura de R2.3.
