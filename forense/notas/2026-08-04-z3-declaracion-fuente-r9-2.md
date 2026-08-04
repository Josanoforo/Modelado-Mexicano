# Declaración de fuente · `R9.2` · Encargo Z, commit 1

*(Escrita antes de abrir un solo ZIP de microdato. `R9.2` es la meta-regla del corpus — línea 265: "auditar estructura antes de invocar cultura" — su falsación tiene consecuencias desproporcionadas. Se declara con el mismo cuidado que exige el Bloque C de su propia ficha, línea 270-271: anti-superviviente obligatorio y métrica AUDITADA únicamente.)*

## Candidatas del catálogo — todas, con la razón de la elección

Dominio del falsador: **SAL**, cobertura de vacunación/servicio, con dos piezas separables: (i) cobertura del lado del hogar/beneficiario, (ii) disponibilidad + alcance de campaña del lado del prestador.

| Candidata | Cubre el dominio | Por qué se descarta o se elige |
|---|---|---|
| **ENSANUT CONTINUA 2024** | Sí, para (i) — módulos de vacunación en los cuestionarios de Niños 0-9, Adolescentes y Adultos, verificados por Cartilla Nacional de Salud/Vacunación mostrada al entrevistador | **Elegida para la pieza de cobertura.** Es encuesta de hogar, independiente del prestador — satisface por diseño la parte de "AUDITADA... no auto-reportada por el prestador" para la cobertura misma. |
| DGIS — Otros subsistemas (`data/catalogo-fuentes-v1_0.md:123`) | Parcial, para (ii) — cubos dinámicos y datos abiertos de la Secretaría de Salud | **Descartada explícitamente**, no por ausencia de dato sino por identidad de la fuente: la DGIS es la Dirección General de Información en Salud, parte de la propia Secretaría de Salud — es **el prestador reportándose a sí mismo**. Es exactamente la fuente que la ficha excluye en su línea 271: "la cobertura auto-reportada por el prestador es parte interesada." |
| ENIGH | No | No mide vacunación ni disponibilidad de servicio. |

No se identifica en el catálogo ninguna tercera fuente —ni encuesta ni registro administrativo— que audite disponibilidad de vacuna o alcance de campaña de forma independiente del prestador.

## La elegida, contra el Umbral concreto

**Fuente elegida (cobertura): ENSANUT CONTINUA 2024.** Verificado por lectura de `2 VFINAL Cuestionario niños 0 a 9...pdf`, `3 VFINAL Cuestionario adolescentes...pdf` y `4 VFINAL Cuestionario adultos...pdf` (raíz `descargas_mx`): las tres traen sección dedicada de vacunación, con verificación de Cartilla física ("¿Me puede mostrar la Cartilla?", `M0503`/`D0501`/`A0901`), no solo pregunta de memoria — la cobertura reportada está anclada a documento, no a auto-reporte puro del hogar y mucho menos del prestador.

**Umbral (línea 268):** "Cobertura <60% con disponibilidad y alcance de campaña verificados por fuente independiente del prestador."

- La mitad de **cobertura** de este Umbral SÍ es construible con ENSANUT (hogar, con verificación documental, independiente del prestador).
- La mitad de **disponibilidad y alcance de campaña verificados por tercero** no tiene ninguna fuente candidata en el catálogo. La única fuente con ese tipo de dato (existencia de dosis en unidad, fechas y cobertura geográfica de campaña) es la propia Secretaría de Salud (DGIS) — el prestador. No existe en el catálogo un auditor externo de abasto de vacunas (p. ej. un órgano de fiscalización con datos abiertos de existencias por unidad).

## Qué condición del Umbral no está cubierta

**La mitad de "disponibilidad y alcance de campaña verificados por fuente independiente del prestador" no está cubierta por ninguna fuente del catálogo.** No es una limitación de ENSANUT específicamente — es que **ningún instrumento disponible audita el abasto/alcance de campaña desde fuera del prestador**. Esto coincide, letra por letra, con la fila `D` de la propia escala (línea 273): "si el abasto solo lo reporta el prestador." Verificado contra el catálogo completo (`data/catalogo-fuentes-v1_0.md`), no contra el nombre de una sola variable — es ausencia de instrumento, no de dato dentro de un instrumento.

**Obligación anti-superviviente (línea 270), declarada aquí y pendiente para el commit 2:** antes de cerrar cualquier veredicto, el commit de corrida debe buscar activamente casos de cobertura baja con abasto normal (no solo casos donde el desabasto explica la caída), y archivar los descartes con motivo (ADR-29.b) — esta declaración de fuente no la sustituye ni la adelanta; se ejecuta al abrir el instrumento.

## Variables exactas, universo, ponderador, estrato, UPM

- Tablas: `menores_ensanut2024_w` (0-9 años), `adolescentes_ensanut2024_w` (10-19), `adultos_ensanut2024_w` (20-59); raíz `descargas_mx`.
- Universo previsto: población objetivo de cada esquema de vacunación por grupo de edad (esquema básico en niños; refuerzos en adolescentes/adultos).
- Variable de cobertura: `M0503`/`D0501`/`A0901` (mostró Cartilla) + preguntas de vacuna específica cuando no hay Cartilla.
- Variable de abasto/campaña: **no existe en el catálogo** (ver arriba) — no hay ID de variable que declarar porque no hay instrumento.
- Diseño muestral: ponderador `ponde_f`, estrato `estrato`/`est_sel`, UPM `upm` (misma convención que Nota 17).

## Compromiso de pre-registro

**El primer resultado que produzca este procedimiento es el que se reporta.**
