# Cartera secundaria · Reuters Digital News Report individual México

Estado: **DIFERIDO-POR-DEMANDA-NO-DEFINIDA; NO LISTO PARA ENVIAR; NO ENVIADO**.

## Evidencia del diferimiento

El 11 de septiembre de 2026 se cruzaron `dnr2025_questionnaire` y los
consumidores vigentes en `data/curacion-registro/relaciones.tsv`,
`data/curacion-registro/utilidad-modelo.tsv`,
`data/corrida0/demanda-resultados.tsv`, `canon/`, `milpa/` y
`forense/prereg-duelo-v2/`. No existe coincidencia Reuters/DNR ni un consumidor
que fije año, población, reactivo o estimando.

Ya están registrados el cuestionario 2025, reporte y nueve tablas topline de
México. Solicitar microdato individual sólo para completar inventario sería
inventar una necesidad. Por eso el residual de FP-314/NC-0151 se conserva, pero
no bloquea los otros cinco expedientes.

## Alcance mínimo propuesto si aparece consumidor

Una reapertura debe nombrar primero regla/uso y congelar estimando. El candidato
mínimo que el cuestionario 2025 permite evaluar —sin afirmar que hoy se
necesita— es:

- país México y año 2025;
- `Q6_2016_1` (confianza en la mayoría de las noticias) y `Q6_2016_6`
  (confianza en las noticias que la persona consume);
- `Q10`/`Q10a_new2017` sólo si el consumidor pregunta por vía principal de
  acceso; no pedir toda la batería digital por defecto;
- ponderador final, variables de diseño liberadas, edad, sexo/género, educación
  y región amplia sólo si son necesarias para el contraste;
- producto: diferencia entre confianza general y confianza en noticias elegidas,
  o su heterogeneidad por vía de acceso, con agregados y sin reidentificación.

Antes de contacto se debe confirmar que la versión México conserva esos nombres
y fijar si el agregado público ya responde la pregunta. Sólo entonces se
comprueba el canal vigente y se redacta una solicitud con uso real. No hay dato
personal que llenar ni destinatario que presentar hoy.

## Criterio de reapertura y recepción

Reabrir únicamente con `consumidor | pregunta | año | variables | por qué
topline no basta | salida esperada` completo. Si se envía después, registrar
acuse y restricciones; conservar microdatos fuera de Git y verificar país,
año, muestra, pesos, diccionario y hash. Una negativa no afecta los toplines ya
obtenidos.
