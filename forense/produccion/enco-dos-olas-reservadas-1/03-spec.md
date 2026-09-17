# Spec propuesta · ENCO P10, junio 2025 + junio 2026

Estado exacto: **PREPARADA-NO-AUTORIZA-RESPUESTAS-NI-EMISIONES**.

Esta spec separa adquisición, definición y elegibilidad experimental. Los bytes
están adquiridos y reservados; el estimando está definido; no existe enlace
elegible con M y no se autoriza abrir respuestas, medir, emitir ni ejecutar F6.

## Estimando descriptivo sugerido

Para cada ola por separado:

> Proporción ponderada de personas elegidas de 18 años o más, residentes
> permanentes en viviendas particulares del dominio ENCO, que responden “Sí” a
> P10 sobre posibilidades actuales de ahorrar alguna parte de sus ingresos,
> entre respuestas sustantivas a P10.

- Unidad de respuesta y análisis para P10: una persona elegida, no el hogar ni
  todos sus integrantes.
- Universo elegible: persona de 18 años o más seleccionada para el cuestionario
  básico en una vivienda/hogar elegible del levantamiento mensual.
- Evento: `P10=1`.
- Denominador sustantivo primario: `P10∈{1,2,4}`. “No tiene ingresos” (`4`) es
  una respuesta sustantiva negativa sobre posibilidad actual y permanece en el
  denominador si una futura apertura confirma los mismos códigos observados en
  cabecera/documentación. `P10=3` (No sabe), blanco y faltante se reportan por
  separado y nunca se convierten silenciosamente en No.
- Escala: proporción 0–1; cualquier comparación se expresa en puntos
  porcentuales con conversión explícita.
- Ponderador: `FACTOR` de ENCOCB. Pesos no numéricos, no finitos o no positivos
  invalidan el cálculo; no se corrigen por conveniencia.

Escenario secundario, no elegido: restringir a personas con ingresos. Requeriría
una definición pre-R que use la condición de ingreso acreditada en ENCOCS y una
llave estable con ENCOCB. No se adopta ahora ni se seleccionará según el
resultado. No equivale a eliminar simplemente `P10=4` sin declarar un nuevo
universo.

## Misma regla y comparabilidad

La transformación primaria es idéntica en ambas olas porque las dos cabeceras
conservan P10 (`C1`) y FACTOR (`N6`) y los documentos fijan la misma semántica.
La adición/renombre de geocampos en 2026 se registra como cambio estructural, no
como cambio del estimando. Antes de una medición se debe autorizar una lectura
acotada y confirmar que los valores observados no contienen códigos fuera del
contrato; un código nuevo detiene el cálculo, no se recodifica automáticamente.

El diseño declarado es probabilístico, trietápico, estratificado y por
conglomerados. `UPM` aparece en ENCOCS y FOL conserva información histórica de
panel/estrato, pero los paquetes permitidos no entregan una variable de estrato
operativa inequívoca en ENCOCB ni una receta vigente de varianza/covarianza
interanual. Por ello:

1. una apertura futura puede producir puntos ponderados descriptivos;
2. no se publican EE/IC de diseño hasta fijar llaves, estrato, UPM, FPC y
   tratamiento de la superposición entre olas;
3. un estrato singular se reporta y detiene la inferencia: no se centra,
   colapsa ni ajusta en silencio;
4. no se usa una fórmula de muestras independientes, pues 50% de las viviendas
   puede repetirse al mismo mes del año siguiente.

## Relación con M

`dinero.ahorro.tiene_ahorros` es stock existente de ahorro. ENCO P10 es una
posibilidad actual autopercibida de ahorrar parte del ingreso. El salto entre
stock y posibilidad no está identificado: no se define
`P(posibilidad)=P(tenencia)`, no se toma complemento y no se calibra una con la
otra. Estado obligatorio para ambas olas:
`M-NO-ELEGIBLE-PARA-ESTE-ESTIMANDO`.

La medición descriptiva de P10 seguiría siendo útil para conocer capacidad
percibida de ahorro en dos cortes. No sería una validación ni transferencia de
la regla M sin un puente científico preexistente y aprobado antes de abrir R.

## B, orden y presupuesto posterior

Junio 2025 podría servir después como referencia de persistencia únicamente
para el mismo estimando P10. Este acto no la abre ni fabrica B. Abrirla antes de
sellar emisiones futuras puede consumir la reserva; el orden debe decidirse y
firmarse antes de cualquier lectura.

Hoy no hay celdas experimentalmente elegibles, posiciones, candidatos M ni
llamadas autorizadas. Presupuesto posterior: cero posiciones, cero emisiones,
cero llamadas y cero estimaciones R. Una autorización descriptiva sucesora
podrá abrir sólo los campos/filas necesarios; un enlace científico sucesor
deberá congelarse antes de R y definir entonces presupuesto y orden.

## Gates de una ejecución futura

1. firma explícita que autorice lectura descriptiva y precise si conserva la
   reserva experimental;
2. identidad de ambos ZIP contra manifiesto y extracción acotada de ENCOCB;
3. validación de códigos/llaves sin mostrar previews ni marginales durante el
   preflight;
4. decisión separada sobre varianza, superposición y estratos singulares;
5. para comparar con M, puente científico aprobado antes de R; de lo contrario
   conservar `M-NO-ELEGIBLE-PARA-ESTE-ESTIMANDO`.
