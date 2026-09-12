# 40 · GEN2 · Demanda conciliada y ejecución de NC-0165

ENTORNO: CAJA — Codex CLI en Windows/WSL  
RAMA PROPUESTA: `acto/gen2-demanda-contratos-ejecucion-nc0165`  
RESULTADO: identificar qué necesita realmente cada consumidor, reconocer lo ya decidido o medido y ejecutar el trabajo accesible del lote; dejar SONDA recibiendo brechas concretas y el motor respetando sus contratos.

Preparado para Jonás el 12 de septiembre de 2026, después de revisar el repositorio y después el transfer. Corte: `main=015407b9a59359481285bf343ad561dfd7026e8b`. #739 está fusionado. Su infraestructura es la base de trabajo; NC-0165 conserva la conciliación pendiente.

## Autoridad y continuación

Al despachar este documento, Jonás autoriza su implementación, inspección del corpus en CAJA, recuperación pública pertinente, búsquedas reales, ejecución de recetas cuyo objeto y uso ya estén autorizados, correcciones materiales de enlace/ruteo, commits, push y PR propio. Continúa entre fases sin pedir otro encargo. La fusión queda con Jonás.

Esta autorización permite ejecutar y comprobar decisiones existentes; no convierte una recomendación en firma. Una definición científica nueva o una adopción nueva se presenta con su objeto exacto, alternativas, recomendación y consecuencia, después de terminar el trabajo independiente. Preparar una propuesta de spec o adopción no autoriza activarla. No conceder firmas de contador por inferencia.

Quedan fuera: llamadas del experimento F5 y sustitución de su modelo, apertura de F6, compras, convenios, envío de correos/formularios y compromisos con identidad personal. La operación de investigación pública por Codex sigue la autorización y presupuestos vigentes de #739. No hace falta pedir nuevamente permiso para esas operaciones ya autorizadas.

## Arranque y evidencia de partida

1. Lee `AGENTS.md`, este archivo completo y el procedimiento pertinente de `.claude/commands/acto.md`. Reporta worktree absoluto, rama, HEAD y `git status --short`. Usa worktree propio y archiva el encargo por el 0-bis vigente.
2. Actualiza `origin/main` y busca sólo trabajo posterior pertinente. En el corte únicamente estaban publicadas `main` y `censo/2026-09-11`; no había una rama para 39 o NC-0165. Esto no acredita ausencia de sesiones locales. Comprueba worktrees/asignaciones disponibles y evita duplicar una sesión que ya cubra este objeto.
3. Usa el corpus compartido `/home/pc0/mm-corpus/raw` mediante el resolvedor/montaje de #736. Comprueba los IDs concretos que vayas a consumir. Si no aparecen en este worktree, resuelve montaje/ruta antes de declarar falta de datos. No rehagas el censo completo ni descargues otra vez todo el corpus.
4. Lee los siguientes insumos conforme los necesites; no reconstruyas los más de 700 PR:

- `data/adq-demanda-activa-v1_0.json`, `data/adq-investigacion.yaml`.
- `tools/adq_investigacion.py`, `tools/integra_demanda_motor_sonda.py`, `tools/adq_suficiencia.py`.
- `data/corrida0/usos.tsv`, `resultados.tsv`, `demanda-resultados.tsv`, `decisiones.tsv`; resolver y escritores vigentes de corrida0.
- `forense/no-corrido.tsv`, `forense/firmas-pendientes.tsv`.
- `data/curacion-registro/necesidad-objeto-modelo.tsv`, `utilidad-modelo.tsv`, `relaciones.tsv`, `evidencias.tsv`.
- `forense/encargos/2026-09-10-MESA-CONCILIACION-E01.md` y su cierre; actos sucesores sólo para las decisiones aplicables.
- `forense/notas/2026-09-11-GEN2-38-demanda-motor-sonda-correctivo.md`.
- Contratos vigentes de consulta, uso y sucesión de #710/#712/#720/#729/#731/#739.

Los ZIP de agosto sirven como antecedentes si falta una pieza histórica material; no son autoridad sobre el árbol actual. Respeta encabezados, comentarios y lectores canónicos de los TSV: no trates una línea de comentario como cabecera ni reemplaces vistas derivadas a mano.

## Defectos observados que delimitan el encargo

La proyección de #739 incluye 207 elementos: 16 adoptados y 191 en preadopción. Publica 9 cubiertos, 3 bloqueados por ahorro, 4 pendientes de acceso, 144 de preparación y 47 de decisión científica. Son clasificaciones iniciales, no 191 cálculos faltantes ni 47 firmas nuevas.

Se observó en `proyecta_elementos()`:

- Las ofertas no adoptadas se vinculan buscando `RES-xxxx` dentro del nombre del RESULT. Esto no basta para encontrar sucesores cuyo identificador use otra nomenclatura.
- `SIN-RECETA` agrega `DECISION_CIENTIFICA`; tener una receta parcial agrega `PREPARACION`, antes de resolver integralmente decisiones y sucesores.
- Las decisiones se recogen por un conjunto limitado de coincidencias de objeto; su presencia en la salida no resuelve por sí sola la precedencia de la etapa.
- `RES-0028` aparece con NC-0165 y preparación, sin enlazar la reserva de adopción NC-0085 ya explícita en el repositorio.
- `RES-0095` y `RES-0125` apuntan a campos R de `marco-M-sorteado-v1_3.tsv`. Se deben contrastar sus sucesores; no tratarlos automáticamente como nuevas probabilidades para M.
- Las 45 NC con descripción mínima incluyen obligaciones técnicas/documentales, como verificar una herramienta, archivar un documento o esperar un caso futuro. `aplica_contrato_cientifico=true` por defecto no acredita que todas sean preguntas científicas. Entre los contratos explícitos también existe infraestructura, como NC-0136.

La meta es corregir el efecto material de estas simplificaciones: trabajo duplicado, firmas innecesarias, búsqueda mal dirigida u oferta omitida. No limpiar toda deuda histórica de las NC técnicas.

## Fase 1 · Conciliar la demanda por consumidor y propósito

Recorre los 207 elementos del corte —o el universo sucesor que resulte de main— y agrupa por contrato compartido, conservando la identidad de cada fila. Distingue:

- probabilidad o coeficiente operativo del motor;
- árbitro R y campos de evaluación, incluidos EE/IC y auxiliares;
- supuesto estructural, corte, momento o transformación;
- referencia histórica, sustituida, diferida o vigente según evidencia.

Para cada elemento, sigue consumidor → contrato/decisión → CALC/RESULT o dependencia → uso permitido → sucesor. Un sello científico o una firma de contador no equivale a adopción; un R conocido no se vuelve predictor independiente por cambiarle la etiqueta.

Conserva una correspondencia reproducible entre las filas de entrada y su destino. `activo=SI` es el universo inicial del registro, no prueba de vigencia científica de todo archivo histórico al que apunta. Una referencia sustituida necesita evidencia y sucesor exactos; no desactives filas para mejorar cobertura ni edites marcos congelados. Refleja la conciliación en la vista vigente y, sólo donde corresponda, mediante sus escritores canónicos.

Vincula ofertas con identidad y compatibilidad documentadas. Puedes usar nombres para localizar candidatos; antes de admitir un enlace acredita fuente, ola, estimando, unidad, población, transformación y propósito. Prioriza metadatos existentes; si falta una relación indispensable, añade el vínculo mínimo respaldado a la estructura vigente. No construyas otra base de datos ni un sistema general de ontologías.

Resuelve el primer bloqueo real. Si existe resultado y falta una firma concreta de adopción, no lo envíes a adquisición. Si ya existe una decisión de método y falta código, no vuelvas a preguntar el método. Si un punto es utilizable y el IC no está identificado, separa ambos usos. Los pendientes técnicos llevan contrato operativo y responsable, sin exigirles población o reactivo ficticios.

Desenlace de esta fase: demanda conciliada que alimente las fases siguientes, no un PR aislado de inventario.

## Fase 2 · Completar contratos con el respaldo disponible

Para cada familia científica vigente, completa los campos que realmente determinan su resultado:

`consumidor y propósito | decisión/autoridad | constructo/estimando | población | periodo | unidad | variables/reactivos y codificación | numerador/denominador y filtros | fuente/ID | llaves | ponderador/diseño según uso | transformación | aceptación | oferta/sucesor | primer faltante | ejecutor y siguiente acción`.

Se pueden compartir contratos entre consumidores compatibles; conserva sus dependencias y límites particulares. Un complemento no duplica muestra ni información. Una categoría colapsada no se separa por intuición. Una tasa por persona/tipo de trámite no se presenta como riesgo por evento. Una asociación no identifica un efecto causal.

El criterio de aceptación proviene de la definición y decisión vigentes. No inventes umbrales científicos para completar columnas. Si el campo depende de una elección no tomada, identifica exactamente el campo y presenta opciones; completa los demás campos y continúa con las familias independientes.

Conciliación obligatoria de las 52 NC del corte: determinar naturaleza, vigencia del objeto, dueño y relación con consumidores. Completa científicamente sólo las que lo requieran y la evidencia permita. No cierres una reserva operativa porque no pertenezca a SONDA, ni declares científicamente completos contratos rellenados con «por definir». Separa en la salida contratos científicos completos/incompletos y contratos operativos; no uses su cociente como suficiencia del motor.

## Fase 3 · Casos concretos y orden de trabajo

Empieza por estos grupos; después completa la conciliación del resto del universo por familias. El orden persigue dependencias y utilidad, no cercanía a cifras antiguas.

| Grupo | Trabajo exigido | Límite que conserva |
|---|---|---|
| `RES-0028` / NC-0085 | Recuperar contrato del complemento ENVIPE, universo, padre y propuesta/decisión efectiva. Corregir su vínculo y preparar la opción de adopción si sigue pendiente. | D11 autorizó investigación/propuesta; no firmó automáticamente la adopción. «No tuvo la razón del padre» no significa «tuvo alguna otra razón». |
| `RES-0039`–`RES-0042` / NC-0088 | Localizar contrato de dos capas para denuncia × seguro, ofertas y fuentes; ejecutar sólo la receta vigente autorizada, si existe. Si falta definición, dejar spec propuesta con elección exacta. | No derivar condicionales por independencia ni cambiar persona por delito sin decisión. |
| R y campos de evaluación, empezando por `RES-0095` y `RES-0125` | Cruzar CALC-R, codificaciones, marcos y universos sucesores; separar lo histórico, lo ya ejecutado y la reserva de incertidumbre. | No convertir R en M ni abrir capturas o roles retenidos. FP-371 afecta uso inferencial DIN, no borra el punto descriptivo. |
| `RES-0063`/`RES-0064` y reglas con receta parcial | Localizar la medición ENSANUT y su autoridad; determinar si falta preparación real, vínculo, validación o adopción. Aplicar el mismo criterio a las demás familias con receta. | La cifra legacy no selecciona el filtro ni acredita el contrato GEN2. |
| Corrupción, NC-0107/NC-0111/NC-0153 | Consumir D07/D08 y los sucesores; distinguir regla/proxy por unidad, tasa solicitada y expediente de acceso. | No reiniciar una búsqueda general ni declarar nuevamente pendiente una decisión ya asentada. |
| Horizonte `RES-0046`/`0048`/`0065` y complementos | Conservar NC-0126 y guardias por consumidor; relacionar dependencias sin duplicar una misma necesidad. | IIEG Jalisco no resuelve persona/nacional ni descolapsa la categoría. No liberar valores ni complementos por una etiqueta de aptitud. |
| Coeficientes, asignados, cortes y momentos | Comprobar si el objeto es supuesto autorizado, estimando, transformación o referencia sustituida. Identificar qué dato o decisión necesita realmente. | Un supuesto puede ser explícito; no se presenta como medición. No se activa automáticamente en GEN2. |
| NC-0122/NC-0164/NC-0037 | Incorporar los usos menores ya acreditados y sus fronteras actuales. | No rebautizar proxy fintech, descripción de daño o permanencia en tandas como canal exacto, causalidad o impago. |

La tabla no exige que todos estos grupos produzcan cálculos nuevos: exige resolver su situación con evidencia. Ninguno termina sólo con «motor-gen2: completar contrato» si ya se pudo identificar el objeto, el faltante y la acción.

## Fase 4 · Corregir la derivación y poner a trabajar la ruta correcta

Integra la conciliación en `tools/adq_investigacion.py` y su configuración/insumos mínimos. Conserva una vista derivada reproducible, con evidencia de las decisiones y correspondencias que utiliza. Reutiliza el resolver, los escritores y el esquema vigentes; no dupliques manualmente los 207 registros.

Para las brechas de datos verificadas, el contrato de SONDA debe contener pregunta/versionado, consumidores exactos, qué falta, por qué lo disponible no cumple, candidato o estrategia de búsqueda, evidencia aceptable y frontera ya recorrida. Reutiliza NC existentes; crea una necesidad nueva sólo si es un objeto distinto y no cabe correctamente en el contrato previo. No produzcas una NC por cada campo complementario.

Recalcula selección con la fecha real. Las necesidades públicas realmente listas deben llegar por la vía canónica de #739, sin editar una lista fija de elegidos. Comprueba también que preparación/cálculo/adopción, incertidumbre pendiente de mesa y acceso personal queden con su ejecutor correcto.

No cambies el calendario ni los presupuestos del cron. NC-0122/0126/0164 conservan su revisión del 11/octubre salvo evidencia nueva estructurada de su versión exacta. Completar administrativamente un contrato no constituye una pista nueva ni reinicia búsquedas agotadas. Una necesidad distinta, respaldada y elegible sí puede entrar ahora.

Si 39 publica metadatos nuevos, consúmelos por el buscador vigente e identifica el aporte exacto. Si aún no está integrado, continúa con el índice disponible y fuentes oficiales directas; un negativo del índice parcial no prueba ausencia de dato.

## Fase 5 · Ejecutar hasta un resultado real

Elige el lote de ejecución por consumidor útil, contrato ya autorizado, insumos accesibles y pocas dependencias. Declara sus objetos antes de abrir resultados de control. Concluye todas las piezas viables de ese lote, no sólo un ejemplo mientras dejas la misma reparación sin aplicar al resto compatible.

- **Ya ejecutado y compatible:** consume la evidencia y corrige el enlace/estado. Comprueba el recorrido real hasta la consulta o consumidor correspondiente. No repitas todas las corridas para justificar un asiento.
- **Preparación o cálculo pendiente con receta firmada:** prepara IDs/llaves, congela la identidad de la ejecución conforme a la vía vigente, ejecuta en CAJA, registra CALC/RESULT y verifica el aspecto material nuevo. Preserva sellos históricos; crea sucesora si cambian método o contrato. No habilites nuevos usos por el simple hecho de calcular.
- **Brecha pública lista para SONDA:** realiza la investigación efectiva del lote seleccionado con la ruta existente, persiste cursor/evidencias por versión y adquiere candidatos compatibles dentro del alcance público autorizado. Abre los datos/documentos pertinentes, registra por escritores canónicos y evalúa suficiencia. Continúa preparación/cálculo sólo si su receta ya está autorizada.
- **Adopción pendiente:** prepara consumidor + RESULT + uso + compatibilidad + impacto + prueba en modo propuesto. La adopción no entra a producción sin la firma aplicable. Un PR técnico fusionado no suple una decisión científica ausente.
- **Decisión o acceso externo:** entrega la elección concreta o expediente ya preparado con el dato faltante exacto. No paralices por ello el trabajo independiente.

Demostración mínima sustantiva: consultas reales antes/después de los enlaces corregidos y al menos un recorrido real de trabajo disponible —consumo de una medición ya autorizada, cálculo pendiente autorizado o investigación pública elegible— con su desenlace. Una investigación puede concluir que una fuente no satisface; eso no cierra la pregunta original. Si tras conciliar no hay ningún cálculo autorizado ni búsqueda elegible, documenta ese resultado con los casos concretos y entrega las propuestas listas; no simules actividad ni reabras una espera para cumplir una cuota.

No basta entregar código, fixtures y otra cola sin comprobar que el ejecutor o consumidor utiliza la mejora. Tampoco se exige agotar toda la demanda histórica, obtener un acceso externo o firmar nuevas adopciones dentro de esta sesión.

## Fase 6 · Integración, validación proporcional y cierre

Perímetro propio: conciliación/contratos/ruteo de demanda, vínculos mínimos con consumidores/ofertas, derivador existente, pruebas materiales de esos cambios, lote autorizado declarado en fase 5 y su salida real. Cambios mínimos al consumidor sólo cuando sean necesarios para una decisión ya firmada y estén identificados en el lote. No refactorices todo el motor.

39 posee `tools/actualiza_reactivos_contexto.py`, `tools/busca_reactivos.py`, overlays y residual de NC-0100/NC-0136. 40 consume su salida y puede ajustar la clasificación de esas obligaciones en la proyección, pero no duplica su extracción ni sobrescribe sus cierres. Respeta las reservas y bloqueos cortos del servicio de adquisición; no pises un ciclo activo ni lances un duplicado.

Manifiesto, no-corrido, decisiones, relaciones, vistas y registros compartidos se actualizan por clave sobre el árbol combinado, con los escritores vigentes. Deriva ADR/NC/FP cuando correspondan; no reserves números ni reemplaces tablas completas para resolver un conflicto. No cierres el censo #727 desde este encargo: en el corte sólo añade ocho archivos de censo y no bloquea la entrega.

Pruebas dirigidas a los defectos observados:

1. Una oferta pertinente cuyo ID no incluye `RES-xxxx` puede enlazarse mediante evidencia exacta; un parecido de nombre no basta.
2. Una decisión o sucesor acreditado evita pedir otra firma o repetir preparación; una firma de contador no habilita adopción.
3. NC-0085 y RES-0028 quedan unidos con su estado real; un R histórico no se activa como M.
4. Un pendiente técnico no se cuenta como contrato científico incompleto y conserva dueño/acción.
5. La necesidad pública lista llega al selector; espera de acceso y trabajo ya delegado no se transforman en búsqueda.
6. Las tres salidas bloqueadas de horizonte conservan `NO_COVERAGE`, sin valor ni fallback, y un consumidor apto sigue funcionando.

Reutiliza pruebas existentes. No añadas tests de totales fijos ni repitas la batería completa de #739. Ejecuta los gates requeridos por el procedimiento/CI y compara fallos heredados con baseline; no amplíes el trabajo por formato o deuda ajena. Ninguna prueba altera datos científicos reales. Mantén el esfuerzo de control cerca del 20% salvo riesgo material demostrado.

Cierra la parte operativa de NC-0165 sólo si todo el universo inicial tiene destino conciliado y las obligaciones pendientes quedan enlazadas a contratos/acciones específicos y ejecutores reales. Esto no significa que todo el motor esté medido. Si quedan consumidores sin conciliar, conserva NC-0165 abierta con sus identidades; no la cierres trasladando la misma frase genérica a otro pendiente.

Completa el archivo de encargo, nota breve, filas propias y cadena existente de cierre (`tools/cierre_acto.py` conforme al procedimiento, primero en seco), sin otra plataforma de seguimiento. Entrega PR revisable; Jonás fusiona.

## Criterios de aceptación y salida de la sesión

- El universo activo del corte queda explicado por identidad, propósito, contrato/sucesor, estado real y próxima acción; ningún elemento desaparece para elevar cobertura.
- Las ofertas y decisiones se usan sustantivamente para resolver la etapa. Los campos desconocidos son específicos, no plantillas que fingen completitud.
- La demanda científica se distingue de pendientes técnicos, historia y evaluación. Una medición compartida no se cuenta como varios descubrimientos independientes.
- Hay consumo/ejecución real según fase 5. Datos, cálculo, validación, adopción y aptitud de uso conservan sus diferencias.
- Los pendientes de mesa son decisiones realmente nuevas o aún abiertas, con opciones y evidencia. Las solicitudes de acceso conservan su acción humana concreta.
- No se alteran congelados históricos, presupuestos F5, decisiones previas ni barreras de #739. No se emite GEN1 de forma silenciosa.

Reporta primero: qué consumidores avanzaron y cómo; qué se puede usar hoy; qué bloqueos desaparecieron; qué decisión concreta queda; PR y HEAD. Adjunta una tabla compacta `consumidor/grupo | antes | después | evidencia | uso | pendiente/ejecutor`. Incluye los conteos sólo como resumen del trabajo explicado, nunca como medida de verdad o suficiencia.

## Prompt de lanzamiento

> Ejecuta íntegramente el encargo 40 adjunto en CAJA y worktree propio. Autorizo la conciliación de NC-0165, correcciones de enlace/ruteo, investigación y adquisición públicas pertinentes, ejecución real de recetas ya autorizadas, commits, push y PR; el merge queda conmigo. #739 ya está fusionado. No presentes los 191 elementos preadopción como 191 cálculos ni las 47 etiquetas de mesa como 47 firmas nuevas. Resuelve decisiones y sucesores, completa contratos y lleva el lote viable hasta consumo o ejecución real. El 39 puede correr en paralelo y posee extracción/índice; consume su interfaz. Continúa entre fases sin pedirme otro encargo. Las nuevas definiciones, adopciones y llamadas F5 requieren su autorización específica; termina antes todo lo independiente.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Adopción de `RES-0028` | DECISIÓN-DE-MESA-PENDIENTE | el complemento U4 queda propuesto y `NO_COVERAGE`; no se altera el motor | `NC-0085`; mesa firma o rechaza la adopción |
| Cálculo de `RES-0039..0042` | DECISIÓN-DE-MESA-PENDIENTE | no se ejecuta una apertura científica no firmada | `NC-0088`; mesa elige la spec estrecha o una definición nueva |
| Alta corrida0 de `RES-0063/0064` | DIFERIDO-A:MOTOR_GEN2_REGISTRO | la medición/adopción previa se reconoce, pero consulta GEN2 no emite hasta declarar RESULT | motor-gen2-registro completa el asiento sin volver a medir |
| Solicitud nacional evento×canal ENCIG | NO-VERIFICABLE-AQUÍ | `RES-0009/0011` siguen sin adopción; no se envía con identidad inventada | titular presenta expediente `NC-0153`; receptor verifica |
| Búsqueda pública adicional | SUSTITUIDO-POR:SELECTOR-GEN2-38 | cero tareas elegibles al corte; no se reabre una espera para inflar actividad | revisiones/indicios estructurados de cada contrato |
| Ejecución F5 | FUERA-DE-PERÍMETRO | cero llamadas, transferencias o cambios de presupuesto | `FP-373/FP-374`; requiere autorización específica |

## CONSUMIDO

Ejecutado en `PR #744`, `GEN2-DEMANDA-CONTRATOS-EJECUCION-NC0165`.
La rama entrega la conciliación 207/207, el cierre acotado de `NC-0165`,
consultas reales y la nota de cierre; Jonás conserva la fusión.
