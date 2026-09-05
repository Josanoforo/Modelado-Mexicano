# Módulo propio v0 — los 19 instrumentos mínimos, redactados como ítems

**Subproducto declarado, no lanzado** (SPEC del encargo `MAESTRA38-N12`).
Este archivo **no** es un pre-registro (no vive en `forense/prereg-caja/`,
no trae `.sha256`, no cita ningún falsador). **No** es una decisión de
levantar módulo propio — es la redacción, en formato de ítem, de los 19
instrumentos mínimos que `forense/notas/2026-09-05-MAESTRA38-N12-sonda.md
§3` clasificó `SIN-COBERTURA-EN-ESTAS-FUENTES` hoy, para que la decisión de
levantarlos (que es adquisición **con costo** — diseño muestral, campo,
captura — y **decisión de mesa**, no una que este acto tome ni sugiera
tácitamente) tenga, si mesa la pide, un borrador de dónde partir en vez de
partir de cero otra vez.

Cada fila trae: **texto** (pregunta, adaptada de `spec.md §1` al formato de
un ítem cerrado cuando `N10` ya lo dejaba en esa forma; sin adaptar cuando
`N10` ya era un ítem), **escala** (propuesta, no validada — ningún ítem de
este archivo ha sido piloteado), **población**. La columna **origen** marca
si el texto es **verbatim** de `N10` o **derivado** (una sola excepción,
declarada dos veces ya en `spec.md §1.6` y aquí).

## 1 · `trabajo`

| id | texto (ítem) | escala (propuesta) | población | origen |
|---|---|---|---|---|
| `trabajo.jerarquia.deferencia_iniciativa_suprimida` | (a) «Cuando no está de acuerdo con una decisión de su jefe o superior directo, ¿se lo dice o prefiere no contradecirlo?» (b) «¿Ha propuesto alguna vez un cambio o idea en su trabajo?» | (a) se lo dice / prefiere no contradecirlo / depende — (b) sí/no, frecuencia si sí | ocupada asalariada | verbatim |
| `trabajo.liderazgo.benevolencia_legitima` | «¿Su jefe o patrón lo trata con respeto y se preocupa por sus empleados, o es autoritario y no se preocupa?» + satisfacción laboral / intención de permanencia | escala de trato (respetuoso-preocupado … autoritario-indiferente, 4-5 puntos) + Likert de satisfacción/permanencia | ocupada | verbatim |
| `trabajo.prestaciones.formalidad_pesa_mas_que_salario` | **derivado, no verbatim** — «Si tuviera que elegir entre un empleo con prestaciones formales (IMSS, aguinaldo, Infonavit) y un salario nominal más alto sin esas prestaciones, ¿cuál elegiría?» +, para quien ya cambió de trabajo, «¿por qué eligió su empleo actual?» (abierta, codificada post-hoc) | elección forzada binaria + codificación abierta de motivo | ocupada | derivado — *driver* (prestaciones vs. salario) ya medido en `ENIGH`/`ENOE`; el ítem de arriba solo cubre el desenlace que falta, ver `spec.md §1.1` |
| `trabajo.rotacion.joven_urbano_sin_culpa` | «En los últimos 12 meses ¿cambió de empleo? ¿Sintió que tenía que justificarlo o dar explicaciones a su familia o entorno?» | sí/no + Likert de presión/justificación percibida | 15-29 urbana ocupada | verbatim |

## 2 · `salud`

| id | texto (ítem) | escala (propuesta) | población | origen |
|---|---|---|---|---|
| `salud.atencion.leve_sin_imss` | «La última vez que tuvo un malestar que usted consideró leve o moderado, ¿a dónde acudió?» | categórica: farmacia con consultorio / se automedicó / consulta médica formal / otro | sin seguridad social | verbatim |
| `salud.prevencion.hombre_sin_permiso` | «En el último año, ¿pospuso un chequeo médico por no tener permiso para faltar al trabajo?» | sí/no +, si sí, cuántas veces | masculina ocupada | verbatim |
| `salud.consumo.sellos_precio_similar` | viñeta: dos productos comparables, uno con más sellos de advertencia, precio similar — «¿cuál elegiría?» (punto de compra o recordado) | elección forzada binaria, repetida con 2-3 pares de producto para robustez | hogares con y sin sustituto barato disponible | verbatim |

## 3 · `tiempo`

| id | texto (ítem) | escala (propuesta) | población | origen |
|---|---|---|---|---|
| `tiempo.puntualidad.formal_vs_social` | dos escenarios a la misma persona: «cita de trabajo con checador» / «reunión social familiar» — margen de tiempo declarado con el que llega a cada uno | minutos (antes/después), numérico abierto, por escenario | general | verbatim |
| `tiempo.compromiso.si_voy_incierto` | «Cuando lo invitan a un evento social y no está seguro de poder asistir, ¿suele decir que sí de todas formas para no quedar mal?» + asistencia real registrada (para contrastar intención vs. conducta) | Likert de frecuencia + sí/no de asistencia real | general | verbatim |
| `tiempo.bomberazo.recursos_escasos_urgencias` | escala de frecuencia de «improvisar / resolver de último momento» ante gastos o urgencias competidoras | Likert de frecuencia (nunca…siempre) | bajos ingresos | verbatim |
| `tiempo.cumplimiento.recordatorio_baja_barrera` | pregunta retrospectiva (o diseño experimental) sobre asistencia a cita con/sin recordatorio recibido | sí/no asistió, cruzado con recordatorio recibido sí/no | con costo por faltar (cita médica/trámite) | verbatim |

## 4 · `cooperación`

| id | texto (ítem) | escala (propuesta) | población | origen |
|---|---|---|---|---|
| `cooperacion.tanda.conoce_organizadora` | «¿Usted conocía personalmente a quien organiza/administra esta tanda antes de entrar?», atado a la misma pregunta de participación que `ENNVIH`/panel Compartamos ya hacen | sí/no | participante de tanda | verbatim |
| `cooperacion.confianza.puente_personal` | «Cuando conoce a alguien por primera vez a través de un conocido en común, paisano o correligionario, ¿confía más en esa persona que en un desconocido sin esa conexión?» | escenario vs. control, Likert de confianza comparada | general | verbatim |

## 5 · `información`

| id | texto (ítem) | escala (propuesta) | población | origen |
|---|---|---|---|---|
| `informacion.credibilidad.allegado_confianza` | «Cuando alguien de confianza (familiar, amigo) le reenvía información, ¿la cree más que si viniera de un medio impersonal?» + «¿lo hace distinto si el tema le parece de alto riesgo?» | Likert de credibilidad comparada, por tipo de tema (bajo/alto riesgo) | general | verbatim |
| `informacion.deferencia.costo_acceso_experto` | idéntico en forma al anterior, con el eje «costo/cercanía del experto formal» en vez de «allegado vs. medio» | Likert de deferencia, cruzado con costo/cercanía declarados | general | verbatim |
| `informacion.escuela.miedo_a_caer_clase_media` | «¿Le preocupa que su situación económica empeore o que sus hijos vivan peor que usted?», ligada a la elección de escuela ya medida | Likert de preocupación + variable de elección de escuela ya existente | hogares clase media | verbatim |

## 6 · `comunicación`

| id | texto (ítem) | escala (propuesta) | población | origen |
|---|---|---|---|---|
| `comunicacion.rechazo.indirecto_face` | viñeta de petición/invitación que el respondente no puede o no quiere cumplir — «¿cuál de estas respuestas se parece más a la suya?» | categórica: «no» directo / fórmula indirecta («vamos a ver», «déjame ver») / otra | general | verbatim |
| `comunicacion.retroalimentacion.privada_publica_capital_social` | viñeta de dar retroalimentación negativa a un subordinado/compañero, en privado vs. en público — desenlace declarado sobre el vínculo | elección forzada (privado/público) + Likert del efecto declarado en el vínculo | general | verbatim |
| `comunicacion.directividad.regional_generacional` | viñeta de desacuerdo con una decisión — «¿su respuesta se parece más a "exijo una explicación" o a una forma indirecta?», cruzada con región y edad ya medidas | categórica directa/indirecta + variables de región/edad ya existentes | general | verbatim |

---

## Qué NO es este archivo

No es un pre-registro (`forense/prereg-caja/`), no tiene `.sha256`, no
define falsador ni `se_mueve_si`. No decide levantar ningún ítem — levantar
cualquiera de estos 19 es **adquisición con costo** (diseño muestral,
trabajo de campo, captura) y **decisión de mesa**, no una conclusión de
este acto de NUBE. No reemplaza la posibilidad, siempre preferible si
`CAJA` la confirma, de que una de las 3 fuentes `SIN-FETCH`
(`…N12-sonda.md §4`) ya mida uno o varios de estos 19 sin necesidad de
levantar nada nuevo — este borrador es el plan B, no el plan A. Las escalas
propuestas no están piloteadas ni validadas; son un punto de partida para
que quien diseñe el módulo real (si mesa lo autoriza) no empiece de cero,
no una especificación cerrada.
