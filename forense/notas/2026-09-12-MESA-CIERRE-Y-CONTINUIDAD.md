<!-- RESCATADO POR MESA 15/sep/2026, verbatim de su conversación ChatGPT de origen («Revisa repo y prepara encargos», 12/sep/2026, creado 06:22 UTC). Verificado por dirección: el corte 0b2a39cc (PR #746) que este cierre declara existe y coincide. sha256 del adjunto: cba21b9e4414a3cfacce93e574a003ff21f07b87404071d2b5ecb2b76d96972b. Destino declarado desde el 12/sep/2026 por el propio documento (## 5, línea 90). Archivado bajo ACTO GEN2-SANEA-REGISTRO-Y-RESCATE, cierra NC-0173. -->
# Cierre de mesa GEN2 · Asientos y continuidad

Fecha del barrido: 12 de septiembre de 2026. Jornada tratada: trabajo del 11–12 de septiembre y acuerdos de esta conversación central. Corte consolidado comprobado: `main=0b2a39cc8dbdf03d648c56ee8427a3434a7e7c2c`, después de #746. Los PR #745 y #747 seguían abiertos en la comprobación final.

**Resultado:** los encargos, resultados y reservas principales ya tienen soporte en el repositorio. Falta registrar el aplazamiento operativo de Opus comunicado por Jonás y actualizar la vista de cierre. Hay además pendientes conocidos que necesitan despacho concreto, especialmente el registro ENSANUT. Este documento deja los asientos preparados; no ejecuta cálculos, llamadas, envíos, firmas ni fusiones.

## 1. Lo que ya quedó asentado

| Frente | Estado comprobado | Producto y continuidad |
|---|---|---|
| Servicio de descubrimiento/adquisición | [#739](https://github.com/Josanoforo/Modelado-Mexicano/pull/739) fusionado | Se conserva la vía canónica de selección. #738/#740 son recibos de adquisición, no la corrida pendiente de Opus |
| Encargos de esta mesa | #741 y #743 fusionados | 39/40 y 41/42/43 están archivados en los paquetes de cola. No necesitan otra carga de los mismos documentos |
| **39 · Reactivos** | [#742](https://github.com/Josanoforo/Modelado-Mexicano/pull/742) fusionado | Índice v1.1 con 20,653 identidades lógicas ganadas; 43,020 filas físicas con texto. NC-0100 y NC-0136 permanecen abiertas con residual concreto |
| Consolidación accidental de 39 | Resuelta y documentada en #742 | Las dos sesiones del mismo encargo se consolidaron. La rama del 40 quedó separada. No queda una segunda entrega del 39 por rescatar según el cierre fusionado |
| **40 · Demanda/NC-0165** | [#744](https://github.com/Josanoforo/Modelado-Mexicano/pull/744) fusionado | 207/207 elementos conciliados y NC-0165 cerrada. No equivale a 207 elementos medidos ni a adopción completa del motor |
| **41 · Banxico** | [#746](https://github.com/Josanoforo/Modelado-Mexicano/pull/746) fusionado | CALC-BANXICO-PRODUCTO-DANO-0001: 35 RESULT sellados, 270 estimandos y ficha de consumo. Descripción/asociación urbana por producto; NC-0164 continúa abierta |
| **42 · MOTRAL/N35** | [#747](https://github.com/Josanoforo/Modelado-Mexicano/pull/747) abierto; HEAD `d323d92866572d97843595e0e5668ad5d7279d3d` | Entrega 32 estimandos y 10 diagnósticos, cruce ENOE y corrección del descarte excesivo de MOTRAL 2015. Paper y presentación mexicanos obtenidos. Su integración aún depende del PR |
| **43 · SHED** | [#745](https://github.com/Josanoforo/Modelado-Mexicano/pull/745) abierto; HEAD `b8def3cb935dbbe007bcf392deda0b854eca12da` | Entrega las cinco mediciones y 66 RESULT, con apéndice oficial y denominadores documentados. Conserva uso estadounidense. Su integración aún depende del PR |
| **31 · F5 documental/Opus** | [#728](https://github.com/Josanoforo/Modelado-Mexicano/pull/728) fusionó la preparación | Ejecutable y materialización conservados. FP-373, NC-0160 y NC-0152 siguen abiertas; no hay plan/capturas de esta ejecución documental en main |

Se comprobaron las notas y artefactos de las entregas; no se repitieron las corridas de CAJA. Sus resultados no se promueven a adopciones ni a nuevas firmas desde este barrido.

## 2. Asientos que faltan o necesitan actualizarse

### A. Aplazamiento operativo de Opus — información nueva de esta conversación

**Hecho comunicado por Jonás:** agotó el uso de Claude y retomará la corrida cuando se libere nuevamente, referido como «mañana» en el mensaje de cierre. No se fijó una hora de restablecimiento verificable. El objeto correcto es encargo 31 / FP-373 / PR #728.

**Desfase:** el contrato de ejecución y FP-373 conservan «pendiente de firma; cero llamadas», pero no recogen este aplazamiento por cuota. La pausa no debe borrar el estado de autorización aún registrado ni convertirse en una orden automática al cron.

**Texto listo para el asiento: contratos F5 y enmienda fechada en NC-0160, con referencia a NC-0152:**

> 12/sep/2026 · Mesa central: Jonás informa agotamiento temporal del uso de Claude y difiere la ejecución documental del encargo 31 / FP-373 hasta que se restablezca. La preparación fusionada en #728 se conserva; no repetirla ni confundirla con #738, que corresponde a adquisición. Al retomar, recuperar y archivar la autorización explícita aplicable, verificar identidad del competidor y modalidad de uso, congelar el plan, acreditar transporte y completar las 32 posiciones dentro del techo de 96 solicitudes. Esta anotación registra la pausa; no firma FP-373 ni autoriza FP-374/F6. No se fija una hora ni se programa un disparo automático.

Destino preciso: `forense/prereg-duelo-v2/F5-documental-v1_0/F5-documental-ejecucion-v1_0.md`; `forense/no-corrido.tsv`, fila NC-0160, mediante enmienda y escritor vigente. Enlazar FP-373 sin marcarla FIRMADA. El protocolo y la autorización propuesta ya existen en el encargo 31; no hace falta crear una segunda decisión o una nueva NC.

### B. Estado visible del programa — la cabecera actual está desactualizada

`forense/tablero/TABLERO-PROGRAMA.md` conserva como «Estado vivo derivado» el SHA `86294db` del **9/sep/2026**, y la narrativa principal procede del 8/sep. Por ello no muestra correctamente las fusiones, los pendientes y los resultados de esta jornada.

Actualizar el bloque derivado por `tools/tablero_programa.py --actualiza` y añadir una síntesis fechada con el mapa 31/39/40/41/42/43. Conservar los cortes históricos identificados. No trasladar cifras antiguas a una cabecera con fecha nueva.

Limitación observada del generador: su lectura de cola usa `forense/encargos/cola/*.md`, sin recorrer los subdirectorios donde viven los paquetes 39–43. Regenerar por sí solo no garantiza que estos encargos aparezcan. La síntesis fechada debe enlazar los paquetes y sus PR; cualquier reparación del listado automático queda acotada a esa omisión, sin otra refactorización del tablero.

La cabecera debe conservar la diferencia entre **fusionado**, **entregado en PR** y **pausado**. Los originales de los encargos y sus guías son cortes históricos; actualizar visibilidad mediante enlaces y estado actual, sin reescribir sus autorizaciones verbatim.

### C. Residual del 40 — ya registrado, falta convertir el siguiente paso técnico en despacho

La conciliación está terminada. El contrato actual identifica los pendientes; la siguiente mesa necesita ver cuáles son ejecución técnica y cuáles decisión:

| Objeto | Estado real y siguiente paso | Responsable registrado |
|---|---|---|
| **RES-0063 / RES-0064, ENSANUT** | Medición y adopción previas reconocidas, pero consulta GEN2 todavía no emite por falta de RESULT/corrida0. Preparar un encargo acotado que registre la evidencia existente y pruebe ambos consumidores hasta emisión; no volver a medir ni pedir otra decisión científica | `MOTOR_GEN2_REGISTRO`; no se localizó un PR sucesor específico en el barrido |
| **RES-0028 / NC-0085** | Decidir la propuesta concreta `1 − RESULT-ENVIPE-DEN-P-C2-U4`. D11 autorizó desarrollar la propuesta; no acredita su adopción. La descripción histórica de NC-0085 aún apunta a reconstrucción: añadir el enlace a la propuesta ya disponible | Mesa |
| **RES-0039..0042 / NC-0088** | Elegir entre la apertura estrecha descriptiva `PROPUESTA-ENVIPE-DENUNCIA-SEGURO-v1_0` y una definición nueva. Actualizar la siguiente acción para que no parezca que falta descubrir qué pregunta se está proponiendo | Mesa |
| **NC-0153, ENCIG evento × canal** | Expediente técnico existente; siguiente paso del titular y posterior recepción/verificación. No repetir búsqueda ni presentar una descarga como sustituto de ese acceso | Titular y receptor técnico |

Las tres primeras filas tienen contrato/acción explícitos en `data/adq-demanda-activa-v1_0.json`. Conviene enlazarlos desde las NC históricas y el cierre visible, preservando su antecedente. **No reabrir NC-0165** para agrupar de nuevo lo que ya está separado.

La proyección fusionada del 40 tiene 207 elementos: 9 cubiertos; 70 salidas de evaluación disponibles; 2 mediciones adoptadas sin cobertura contractual GEN2; 6 en acceso; 1 en adopción; 3 bloqueados por datos/uso; 49 en decisión y 67 en preparación. Son categorías de objetos, no 49 firmas nuevas ni 67 cálculos automáticamente autorizados. Estos conteos corresponden al corte de esa proyección; deben regenerarse cuando cambien sus fuentes.

### D. Adquisiciones y traspaso de resultados — consumir las entregas nuevas

Las adquisiciones propuestas al preparar 42/43 avanzaron: #747 ya documenta paper y presentación mexicanos, y #745 el apéndice SHED. No dejarlas otra vez como «por descargar» en la siguiente lista de trabajo.

En #747 existe **NC-0166**, todavía fuera de main en este corte: falta el Appendix C/cuestionario del experimento mexicano, la asignación de 64 bloques, microdato anonimizado y código de tablas 2–5. La entrega informa que el paper termina en Appendix B y no localizó paquete público en la búsqueda dirigida. Al fusionar, conservar esa NC y su vía de acceso; no duplicarla. El titular de N35 conserva la preparación y el eventual envío de esa petición; este cierre no la envía.

Una vez integrados sus cambios, comprobar el enlace de las fichas de Banxico, MOTRAL y SHED desde la demanda, sólo donde exista consumidor y uso compatible. 40 ya está consumido: usar un sucesor para ese trabajo si hace falta, en vez de dejar un «entregar a 40» sin sesión activa. Las fichas son evidencia disponible; no autorizan sustituir parámetros ni cerrar globalmente NC-0164.

## 3. Lo que se conserva sin otro encargo de reparación

- Consolidación de 39: resuelta en #742, incluida su procedencia. No investigar nuevamente las dos ramas.
- NC-0100: 32 identidades DBF pendientes, ya individualizadas. NC-0136: 12,875 filas residuales del lote y 81 grupos históricos externos, con causas. Su continuación se elige por utilidad concreta, no por repetir todo el barrido.
- FP-371/372 y FP-374 mantienen sus reservas. En esta conversación no hubo una nueva decisión que permita marcarlas firmadas.
- Cron: la proyección del 40 conserva cero investigaciones elegidas al corte. El restablecimiento de Claude no habilita un lanzamiento F5 desde adquisición. Las nuevas fuentes se tramitan por su identidad y elegibilidad; no se adelantan en bloque las esperas existentes.
- Numeración de ADR, sincronización y conflictos ordinarios permanecen en las sesiones que integran sus PR. No son otro encargo de mesa.

## 4. Orden de continuidad para la próxima sesión

1. Actualizar únicamente main y el estado de #745/#747. Si se fusionaron, consumir sus entregas y NC-0166; no volver a encargarlas.
2. Retomar 31/FP-373 cuando se restablezca el uso, con el estado de autorización correctamente asentado y el contrato existente. La preparación no se repite.
3. Despachar el registro ENSANUT RES-0063/0064 como siguiente reparación técnica útil.
4. Resolver en mesa las dos decisiones concretas NC-0085 y NC-0088 con sus propuestas ya construidas.
5. Integrar las ofertas Banxico/MOTRAL/SHED y decidir la gestión de acceso del residual DCE; conservar sus límites.

No hay dependencia que obligue a esperar Opus para avanzar el registro ENSANUT o revisar las propuestas.

## 5. Incorporación mínima al repositorio

Destino sugerido de este cierre: `forense/notas/2026-09-12-MESA-CIERRE-Y-CONTINUIDAD.md`. Para asentarlo, refrescar el corte y los dos PR abiertos, incorporar la nota, añadir la enmienda operativa de Opus, actualizar los enlaces de siguiente acción ya resueltos por #744 y renovar el estado visible. Hacerlo en un único cambio documental acotado, conservando las firmas, resultados e identidades de las entregas.

No se ejecutó un acto de escritura al repo desde este barrido. Este archivo contiene el resultado revisable y los textos/destinos concretos para su incorporación; no afirma que esos asientos ya estén fusionados.

## Evidencia principal examinada

- `AGENTS.md` y procedimiento pertinente de `.claude/commands/acto.md`.
- Main `0b2a39c`, metadatos actuales de #728/#738/#742/#744/#745/#746/#747 y antecedentes #739/#741/#743.
- `forense/notas/2026-09-11-GEN2-39-REACTIVOS-RESIDUALES-Y-BUSQUEDA-UTIL-cierre.md`.
- `forense/notas/2026-09-11-GEN2-DEMANDA-CONTRATOS-EJECUCION-NC0165-cierre.md` y proyección de demanda.
- `forense/notas/2026-09-12-GEN2-BANXICO-PRODUCTO-ATRASO-Y-COSTO-cierre.md` y ficha de consumo.
- En las cabezas de #747/#745: sus notas de cierre, ficha del experimento mexicano, artefactos referidos y NC-0166.
- Filas pertinentes de `forense/no-corrido.tsv` y `forense/firmas-pendientes.tsv`, contrato F5, encargo 31 y paquetes 39–43.
- `forense/tablero/TABLERO-PROGRAMA.md` y lectura de cola del generador.
- Mensajes explícitos de Jonás en esta conversación. Los ZIP de agosto no se usan como estado actual del proyecto.
