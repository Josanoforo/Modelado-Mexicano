> **Insumo externo (ChatGPT/Astra) · entregado a dirección 9/sep/2026 · registrado por ACTO GEN2-REGISTRO-REPLAY conforme a A.3 y regla de mesa 4 · hallazgo principal reproducido por dirección en clon propio, 23 corridas · el texto de abajo no se edita**

---

# Propuesta incremental a dirección · mejoras derivadas de las notas de PR

**Astra → Claude · 9 de septiembre de 2026 · PROPUESTA para adaptar, registrar y despachar.**

**Principio rector: cada lote debe conservar la evidencia que ya ganó y reducir trabajo repetido, sin convertir a la máquina en quien decide.**

## 1. Dictamen y corte

Sí procede una mejora incremental. Priorizaría **la conservación de evidencia de replay**, **la identidad de las fuentes antes del siguiente lote ENCIG/ENCUCI** y **la estabilidad de los tests**. En paralelo, corresponde alinear el protocolo del revisor y hacer practicable la conciliación ya aprobada. No hace falta otro sistema de automatizaciones.

Revisión de las descripciones y comentarios accesibles de la ventana **PR #631–#659**, con contraste dirigido contra código y documentos relevantes. Es una revisión de patrones operativos; **no es una certificación adversarial completa de los 29 diffs ni una reproducción de sus mediciones**.

| Superficie | Corte utilizado |
|---|---|
| Repositorio | `Josanoforo/Modelado-Mexicano` |
| Estado consolidado examinado | `4497029ab585a56559603f7f544d1c3df5768eb4`, merge de #657 |
| Trabajo todavía propuesto en la consulta | #658, censo; #659, digesto, ambos abiertos |
| Entorno de esta revisión | Lectura de GitHub y worktree separado; sin replay con microdatos |
| Verificación local | Comparación en memoria del registro publicado contra `_filas_registro(verifica=False)` y consulta de `status`; sin `--escribe` |
| Contexto histórico | ZIP de sesión y espejo del 7 de agosto, inspeccionados como antecedentes; no usados como autoridad sobre septiembre |

Dirección debe actualizar este corte contra `origin/main` al despachar, comprobar si los hallazgos siguen abiertos y conservar las partes que aún tengan efecto. Los PR abiertos se citan como propuestas. Los números de este documento describen este corte; no deben convertirse en constantes del programa.

## 2. Lo que ya está cubierto

| Antecedente | Lectura al corte | Consecuencia |
|---|---|---|
| Revisión adversarial #649 | #651 aplicó el correctivo; #654 archivó el original y cerró `NC-0082` | No volver a encargar esa corrección ni la recuperación del documento |
| Gobierno de decisiones | #650 incorporó la vista `--mesa`, protocolo de cobertura y bucle de cierre | Mejorar su ejecución; no diseñar otra bandeja ni otro registro |
| Propuesta de automatizaciones postcálculos | #654 incorporó `REVISA-CALC` en `/revisa` | Extender el mecanismo existente |
| Primera adopción ENVIPE del lote #653 | #656 propagó la cita primaria y cerró `NC-0084` | No tratarla como adopción pendiente |
| Complemento `RES-0028` | `NC-0085` sigue abierta: no procede presentarlo como medición independiente por ser `1-p` | Mantener la decisión de universo/codificación en mesa |
| `delta` | `NC-0091`: pendiente de decisión, “cuando mesa lo pida” | No convertirlo en requisito general de los próximos cálculos |

Fuentes: [#650](https://github.com/Josanoforo/Modelado-Mexicano/pull/650), [#651](https://github.com/Josanoforo/Modelado-Mexicano/pull/651), [#654](https://github.com/Josanoforo/Modelado-Mexicano/pull/654), [#656](https://github.com/Josanoforo/Modelado-Mexicano/pull/656) y [`no-corrido.tsv` al corte](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/forense/no-corrido.tsv).

## 3. Reparación prioritaria: conservar el significado y la procedencia del replay

### Evidencia

**Observado.** #657 y `NC-0094` registran dos defectos: regenerar sin `--verifica` sustituye veredictos previos por `NO-VERIFICADO`; regenerar con `--verifica` cambia resultados ajenos según la disponibilidad de datos en la caja ejecutora. La nota reporta 14 filas en su comparación y siete cambios ajenos incluso usando verificación.

La comprobación de esta revisión tiene otro universo: las filas publicadas en el `main` posterior a #657. En ese corte, la derivación en memoria sin verificar cambia **23 filas, dos campos por fila**. Ejemplos:

| Corrida | Publicado: resultado / contexto | Derivación sin verificar |
|---|---|---|
| `CALC-ENVIPE-0001--06223f3dc02d` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` |
| `CALC-MOTOR-celdas-semilla--4aa0d51f02d9` | `NO-REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` |
| `CALC-0001--174c269a07b6` | `NO-EJECUTABLE / DISTINTO` | `NO-VERIFICADO / NO-VERIFICADO` |

La causa se ve en `_lee_oferta`: inicializa ambos campos con `NO_VERIFICADO`; `_filas_registro` los proyecta y `registro --escribe` escribe las tres vistas. `verify()` documenta, por su parte, que no escribe artefactos canónicos. [Código al corte](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/tools/corrida0.py), [#657](https://github.com/Josanoforo/Modelado-Mexicano/pull/657).

**Interpretación.** Las columnas mezclan evidencia de una verificación previa con la capacidad de verificar en la sesión presente. El problema puede ocultar un resultado adverso, además de borrar uno favorable. Cambiar `NO-REPRODUCE` por “no verificado ahora” no demuestra que la discrepancia desapareció.

**Consecuencia.** Reparar `NC-0094` antes de volver a usar una regeneración global como cierre rutinario de un lote. No resolverla imponiendo un replay global: eso conserva el problema de entorno y añade costo.

### Conducta propuesta

1. **Contención inmediata:** calcular el diff antes de escribir. Si una regeneración sin replay eliminaría evidencia identificada, parar antes de modificar cualquiera de las tres vistas y listar los IDs afectados. No añadir una opción de borrado silencioso. Es una protección transitoria, no el cierre definitivo de `NC-0094`.
2. **Separar evidencia histórica de observación de esta sesión.** Una ejecución que hoy no dispone del corpus informa su limitación; no invalida por ello un replay anterior. Un fallo nuevo con contexto idéntico tampoco puede quedar oculto detrás del último éxito.
3. **Dar fuente a la proyección.** Reutilizar el comprobante versionado de verificación, si existe y contiene identidad suficiente. Dirección debe localizarlo. Si falta, registrar la salida estructurada y su procedencia en la nota de cierre existente, fuera de los bytes sellados, y hacer que el registro la cite. Los TSV derivados no se convierten en su propia fuente. Un veredicto heredado sin comprobante suficiente sigue siendo evidencia histórica de alcance limitado, nunca un replay recién acreditado.
4. **Identidad mínima de la evidencia:** corrida/ejecución, sello o hash del recibo, spec, código, inputs efectivamente verificados, fecha, entorno y los dos ejes resultado/contexto con sus razones. Reutilizar los campos existentes; no inventar otra máquina de estados. Cambios de identidad impiden presentar la evidencia anterior como vigente para el objeto nuevo.
5. **Actualización explícita y acotada:** verificar las corridas del lote autorizado, registrar su evidencia y regenerar una vez. El comando de lectura y `verify()` conservan su comportamiento sin escritura implícita. No se alteran sellos ni resultados para alojar metadatos nuevos.

La representación exacta del comprobante es el punto de adaptación de dirección. El contrato anterior es obligatorio: **no borrar, no arrastrar evidencia a otra identidad, no fingir verificación actual y no esconder resultados contradictorios**.

### Validación de aceptación

- Registrar un lote nuevo no modifica el contenido probatorio de corridas ajenas sin razón explícita.
- Un segundo registro sobre el mismo corte es idempotente.
- Una sesión sin corpus no borra evidencia obtenida en CAJA.
- Cambiar un input o la spec impide reutilizar el comprobante como evidencia actual.
- Un `NO-REPRODUCE` posterior permanece visible junto a su contexto; conservar historia no significa privilegiar el último éxito.
- Reproducir el caso de 23 filas en un fixture o copia temporal demuestra primero el defecto y después la protección. No hacer 23 replays para probar un problema de registro.

## 4. Dos correcciones pequeñas para los siguientes cálculos

### 4.1. Resolver el instrumento por consumidor

**Observado.** `_instrumento()` toma la primera fuente con forma de instrumento en la regla. En el árbol examinado, `RES-0003`, cuya conducta es `paga_mordida_encig2025` y cuyo payload declarado es `encig25_base_datos_csv`, y `RES-0005`, asociado a `paga_mordida_encuci2020` y `encuci2020_bd_dbf`, quedan bajo `CORR-0001`, rotulado `ENCIG2023`. #653 también advierte la mezcla para el próximo lote. [#653](https://github.com/Josanoforo/Modelado-Mexicano/pull/653), [demanda de corridas](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/data/corrida0/demanda-corridas.tsv), [demanda de resultados](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/data/corrida0/demanda-resultados.tsv).

**Interpretación.** La fuente de una regla con varias conductas no identifica necesariamente la fuente de cada resultado. Agrupar por ese rótulo puede producir un encargo con instrumentos o periodos mezclados.

**Consecuencia.** Corregir esta agrupación antes del lote ENCIG/ENCUCI; no esperar a `lote` o `siguiente` para resolverla.

**Propuesta:** resolver la identidad a partir de la referencia explícita del consumidor y sus fuentes declaradas; contrastarla con el manifiesto y, cuando exista, con la spec. Los sufijos de nombres son pistas para detectar una discrepancia, no autoridad suficiente para corregirla. Si no hay una correspondencia inequívoca, emitir la ambigüedad y detener esa apertura. Las aperturas independientes pueden continuar.

El encargo debe declarar cómo conservar las referencias históricas si la derivación cambia los grupos `CORR-*`: mostrar correspondencia antes/después; no reasignar silenciosamente un ID ya citado ni renumerar sellos. Si no existe una fila NC específica, dirección decide dónde registrar este defecto; **`NC-0088` trata de denuncia condicionada a seguro, no de esta identidad**, y no debe reutilizarse.

**Validación:** una regla de fixture con conductas ENCIG2025 y ENCUCI2020 no se agrupa bajo ENCIG2023; invertir el orden de `fuente` no cambia la identidad; una fuente ambigua no se resuelve por “la primera”.

### 4.2. Tests que sobrevivan a un lote legítimo y al cambio de huso

**Observado.** `T-STATUS-SMOKES` afirma totales absolutos del árbol real: actualmente 11 corridas, 901 resultados sellados, 631 IDs GEN2 y dos adopciones. Su texto acumula actualizaciones por las firmas y lotes de #636, #647, #655, #656 y #657. Además, `NC-0080` documenta que el mismo test general cambia de veredicto según el huso; `t30_yamedido()` usa `datetime.date.today()`. [Test de corrida0](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/tests/test_corrida0.py), [test de cobertura](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/tests/check.py).

**Interpretación.** Un falsador destinado a impedir que LEGACY infle GEN2 se ha convertido también en un freno al crecimiento legítimo. El reloj local introduce otra causa de divergencia que no depende del cambio revisado.

**Consecuencia y propuesta:**

- Llevar las expectativas exactas a un fixture pequeño, con conteos calculables a mano: replay LEGACY, corrida autorizada, sucesora y consumidor adoptado. Probar explícitamente cada contribución y la regla de firma vigente.
- Mantener sobre el árbol real únicamente las comprobaciones pertinentes de integridad y presencia de las firmas concretas. No reemplazar `11` por un `>=11` que deje pasar inflación; tampoco usar la misma función para generar el esperado y el observado.
- El crecimiento legítimo del siguiente lote no debe exigir editar este test. Introducir deliberadamente un replay contado indebidamente o retirar una firma exigible sí debe hacerlo fallar.
- Fijar una fecha de evaluación y un huso explícitos en el test temporal, con posibilidad de inyectarlos en la prueba. Probar el mismo instante a ambos lados de la medianoche local. Usar UTC como opción propuesta, sujeta a la convención vigente del programa.
- No cerrar `NC-0080` porque hoy ambas ejecuciones salgan verdes: el paso de fecha puede ocultar el defecto sin repararlo.

## 5. Alinear el revisor con la evidencia y la materialidad

**Observado A.** La revisión de #643 emitió `NO-FUSIONAR` exclusivamente por 429 WARN declarados frente a 428 derivados. El propio comentario localizó la causa: el cierre de una pendiente disminuyó T22 en uno; la línea base seguía verde. `/revisa` §2.5 exige actualmente bloquear toda cifra contradicha. [Revisión de #643](https://github.com/Josanoforo/Modelado-Mexicano/pull/643#issuecomment-5593911041).

**Observado B.** La revisión de #656 declara cero `NO-VERIFICADO` y cero reservas, pero reconoce que no reprodujo la sonda de consumo reportada ni el replay con microdatos. Para la adopción considera suficiente que `p` no cambió y que la cita coincide. El PR también regeneró los TSV, operación cuyo defecto quedó registrado después en `NC-0094`. [Revisión de #656](https://github.com/Josanoforo/Modelado-Mexicano/pull/656#issuecomment-5597538643).

**Interpretación.** Los pesos pueden detener una corrección inocua mientras el resumen transmite más cobertura de la que se ejecutó. La igualdad de `p` no acredita por sí sola la nueva cadena de consumo; tampoco demuestra un fallo de esa cadena. La reserva debe describir exactamente qué no se comprobó.

**Consecuencia: una enmienda al protocolo existente, sin otro bot.**

1. Cada afirmación relevante lleva evidencia ejecutada, evidencia documental citada o limitación explícita. La evidencia citada no se rotula como ejecución propia. “No aplica” exige que el punto quede fuera del objeto del PR, no que sea costoso comprobarlo.
2. El resumen de veredicto debe concordar con su tabla y sus excepciones. Una comprobación aplicable no ejecutada se declara `NO-VERIFICADO` y tiene el peso previsto. Dirección debe armonizar esta regla con REVISA-CALC y el contrato vigente, sin cambiar comentarios históricos.
3. Comparar números sobre el mismo SHA/vista previa, universo, fecha y entorno. Un dato viejo en la descripción se corrige; no se justifica por ser pequeño.
4. Proponer `RESERVA` para un desajuste meramente informativo cuyo origen esté localizado y que no cambie una compuerta ni oculte un fallo. Conservar `BLOQUEA` cuando cambia identidad, universo, estimación, consumo, decisión o resultado material. La cifra de WARN no determina por sí sola la severidad: un único WARN puede advertir algo material.
5. Revisar cambios de valores en columnas de evidencia aunque el archivo sea `DERIVADO`. Que el diff sea una regeneración esperada no acredita que todas sus transiciones sean correctas.
6. Para una adopción de cita con `p` idéntico, comprobar la relación consumidor → RESULT → corrida y, si el encargo exige la sonda de consumo, ejecutar la prueba permitida o declarar su falta. La identidad del valor no sustituye esa comprobación.

**Validación propuesta:** usar #643 como caso de cifra auxiliar corregible y #656 como caso de alcance declarado. Añadir el caso adverso de `NO-REPRODUCE → NO-VERIFICADO` en un diff derivado. Basta una calibración documentada del protocolo; no encargar ahora un clasificador automático de severidad.

## 6. Hacer ejecutable la conciliación aprobada y alinear el tablero

### 6.1. Descubrimiento completo antes de agotar la lectura humana

**Observado.** El PR abierto #659 declara 53 NC abiertas, una revisada (`NC-0040`) y 52 no revisadas por presupuesto. Es correcto que se rotule INCOMPLETO. El runbook vigente ya exige buscar todas las abiertas y citar candidatas; esa obligación no basta para que la sesión alcance a hacerlo. La vista `--mesa` cruza FP explícitas del sucesor, pero no sustituye la lectura de evidencias en notas y encargos. [#659](https://github.com/Josanoforo/Modelado-Mexicano/pull/659), [runbook](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/.claude/commands/tramite.md), [derivador](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/tools/digesto_tramite.py).

**Interpretación.** El problema ya no es diseñar un bucle de cierre: es que su descubrimiento consume el presupuesto de la sesión. Una sola corrida incompleta no prueba que todas las rutinas fallen, pero sí demuestra que aún no se puede prometer cobertura por ciclo.

**Consecuencia y propuesta:** incorporar al **mismo derivador** una pasada de localización sobre todas las filas abiertas y las fuentes que ya admite el runbook. Reutilizar lectores y tokens. Emitir para cada cruce el ID, objeto, ruta al SHA, fragmento, tipo de evidencia y comprobación humana restante. Excluir como prueba los digestos, la repetición de la obligación y un PR abierto. Coincidencia textual produce candidato, nunca cierre.

La pasada debe devolver su universo completo: cuántas abiertas examinó, candidatas localizadas, referencias no resolubles y filas sin evidencia localizable. Si falta una fuente o la búsqueda se trunca, declarar el alcance incompleto. **No exigir solo coincidencia de ID:** incluir referencias explícitas a sucesora, encargo y objeto; lo que únicamente tenga relación semántica sigue requiriendo lectura humana.

En el trámite existente, examinar primero evidencia recién aparecida y luego los casos no revisados más antiguos, tomando el pendiente de lectura del último digesto. No volver a empezar siempre por la primera fila. El digesto es memoria de trabajo, no prueba de cierre ni estado paralelo. Registrar los IDs aún no revisados y la edad de su última revisión conocida.

`NC-0040` sirve como calibración: presentar la consulta corroborada y su alcance frente al criterio literal de la fila. Dirección resuelve si satisface la obligación completa; después el trámite propaga la evidencia autorizada, sin volver a pedir una decisión ya asentada.

**Límite explícito:** la garantía “toda cerrable es candidata en una rutina” se puede comprobar mecánicamente para evidencias enlazables dentro del universo cubierto. Para cierres que exigen lectura semántica, hace falta completar esa lectura o declarar el ciclo incompleto. No rebajar el criterio original ni prometer que un buscador lo satisface por sí solo. Si la misma deuda de lectura reaparece en el siguiente ciclo, llevarla a dirección en la bandeja existente para ajustar el alcance o presupuesto; no crear otra rutina.

**Validación:** cubrir el conjunto completo de abiertas de un corte; localizar firma sucesora sin cerrar automáticamente; ignorar PR abierto; detectar evidencia nueva aunque el TSV no cambió; conservar `NC-0055` cuando la premisa siga falsa; demostrar que un ciclo truncado enumera residuales y que el siguiente no los omite.

### 6.2. Alineación documental en un acto acotado

**Observado.** El tablero publicado mantiene un bloque llamado “Estado vivo derivado” estampado `c55320b`, con cero corridas GEN2 selladas y cero adopciones. El comando actual devuelve **11 selladas, dos adopciones, 203 dependencias legacy y 53 NC abiertas**. La tabla histórica está fechada, lo cual es correcto; el bloque presentado como vivo está atrasado. Además, G2 aún exige implementar `vigencia` y `delta` antes de la primera adopción, frente a dos adopciones consolidadas y `NC-0091` opcional.

`NC-0083` dejó pendiente indicar el plan vigente porque no encontró los tokens literales `plan_vigente`/`instrucciones_vigentes`. El tablero sí contiene una fila curada “Plan CORRIDA-0”, donde hoy cita el plan anterior. El documento `agente-tramite-v1_0.md` conserva el perímetro original de tres rutas, mientras el runbook incorpora después `rutinas.tsv` y las tres columnas autorizadas de `no-corrido.tsv`. [Tablero](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/forense/tablero/TABLERO-PROGRAMA.md), [documento del agente](https://github.com/Josanoforo/Modelado-Mexicano/blob/4497029ab585a56559603f7f544d1c3df5768eb4/forense/agente-tramite-v1_0.md).

**Interpretación.** Son desalineaciones entre superficies existentes. No prueban que el cron cargue un prompt antiguo: esa configuración externa no fue inspeccionada. Tampoco obligan a crear un campo nuevo para poder citar un plan.

**Consecuencia y propuesta:**

- Refrescar el bloque con `tools/tablero_programa.py --actualiza`, en un encargo cuyo perímetro incluya el tablero. Conservar las tablas históricas fechadas.
- Anotar el plan firmado vigente en la fila curada equivalente y corregir G2 con cita a las decisiones posteriores. No escoger el plan por “archivo de versión más alta”: puede ser una propuesta.
- Resolver `NC-0083` con la evidencia de esa propagación. Mantener `NC-0055` hasta comprobar su obligación completa; un mero refresh no necesariamente sustituye el cuerpo curado pedido en esa fila.
- Marcar la descripción original del agente como histórica o añadir una enmienda de precedencia que remita al runbook actual. No ampliar por inferencia el perímetro de trámite para editar el tablero.
- Dirección comprueba una vez qué instrucciones consume la rutina desplegada. Si carga el runbook vigente, no hay nada que reinstalar. No crear un monitor adicional para una posibilidad no verificada.

## 7. Gate D-14 y costo delimitado

Las tres respuestas quedan escritas para cada cambio mecánico. El ahorro se apoya en incidentes concretos; **no se inventa una medición de horas ahorradas**.

| Pieza | Defecto real ya ocurrido | Por qué es material | Por qué puede costar menos que corregir a mano |
|---|---|---|---|
| Registro de replay | `NC-0094`; 23 filas cambian en el ensayo al corte | Puede desaparecer un veredicto adverso y confundirse entorno con validez | Evita revisar/reparar columnas ajenas o repetir todos los replays en cada lote; usar el registro y recibos existentes |
| Identidad por consumidor | `CORR-0001` agrupa payloads ENCIG2025/ENCUCI2020 como ENCIG2023 | Cambia la apertura y la fuente del cálculo encargado | Corregir una resolución y probarla una vez evita separar mal cada lote posterior |
| Tests de conteo y fecha | Reajustes repetidos de T-STATUS; `NC-0080` | Bloquean entregas legítimas y vuelven variable la evaluación | Fixture pequeño y reloj explícito sustituyen cambios repetidos por cada firma, lote o huso |
| Localización de candidatas | #659: 52 de 53 abiertas sin revisar en el ciclo reportado | Retrasa conciliaciones que pueden desbloquear trabajo o evitar decisiones repetidas | Un recorrido de fuentes en el derivador existente sustituye búsquedas manuales repetidas; medir su duración y utilidad antes de adoptarlo |

Los cambios de protocolo y las correcciones de documentos **no se convierten en automatizaciones**. Si la localización no reduce el trabajo sobre el caso real, no ampliar su complejidad: mantener el protocolo y ajustar la capacidad de lectura. Si la conservación de replay exige infraestructura que exceda estos componentes, despachar primero la contención y dejar explícitamente abierta la reparación completa.

**Presupuesto de componentes:** modificaciones acotadas en `corrida0.py`, sus tests y el test temporal; una extensión de `digesto_tramite.py`; enmiendas a `/revisa`, `/tramite` y documentos afectados. **Cero servicios, cero cron adicionales, cero base de datos, cero motor de workflows y cero registro de estados paralelo.** No encargar una refactorización general.

## 8. Despacho sugerido a Claude

1. **Registrar esta propuesta como acto externo por 0-bis A.3.** Archivar el original completo, con procedencia, antes de adaptarlo. No sustituirlo por este resumen ni reconstruirlo desde citas. Mantener separada la adaptación de dirección y declarar cualquier cambio de alcance.
2. **Encargo de integridad del registro:** `NC-0094`, conservación de evidencia y pruebas dirigidas. Es la prioridad antes de otra regeneración global. Su cierre exige la solución completa, no solamente el freno preventivo.
3. **Encargo de preparación del siguiente lote:** identidad ENCIG/ENCUCI y tests estables. Delimitar la migración de referencias que resulte necesaria antes de tocar derivaciones históricamente citadas. No medir ni adjudicar nuevas probabilidades dentro del acto de herramientas.
4. **Encargo de operación:** localización en el derivador, calibración del revisor y alineación documental. Un acto delimitado; el trámite posterior usa la rutina existente para proponer cierres, siempre con cita y estampa de universo.

En cada encargo, incluir los archivos fuente que se piden archivar, los destinos de firma y las propagaciones necesarias dentro de su perímetro. `NC-0082` ya cerrada no se reabre; `NC-0097`, si sigue abierta al despachar, requiere asentar las firmas de los tres R donde corresponda, no volver a medir ni firmarlas por inferencia. No reservar números ADR/FP/NC desde este documento: dirección los adapta contra el árbol del día.

**Orden condicionado al trabajo real:** la identidad debe quedar resuelta antes del lote ENCIG/ENCUCI; no bloquea por sí sola una apertura ENVIPE independiente. `delta`, `vigencia`, `lote` y `siguiente` conservan el alcance y la prioridad acordados en la propuesta anterior. Esta revisión no los hace obligatorios ni los duplica.

Mesa sella con el merge. Esta entrega propone los cambios; no registra firmas ni modifica el repositorio.

## Anexo breve · comprobación reproducible del hallazgo principal

Desde un checkout limpio del SHA indicado, sin microdatos y sin escritura del registro:

```python
from tools import corrida0 as C

publicado = {
    fila['corrida_id']: fila
    for fila in C._leer_tsv_derivado(C.VISTA_CORRIDAS)
}
propuesto = C._filas_registro(verifica=False)
cambios = []
for fila in propuesto['corridas']:
    anterior = publicado.get(fila['corrida_id'])
    if anterior is None:
        continue
    for campo in ('resultado_replay', 'contexto_replay'):
        if anterior[campo] != fila[campo]:
            cambios.append((fila['corrida_id'], campo,
                            anterior[campo], fila[campo]))
print(len({cambio[0] for cambio in cambios}))  # 23 en este corte
print(C.status(imprime=False))
```

Se ejecutó esta comparación y la consulta de estado; se inspeccionaron las causas en código. No se ejecutó una suite general ni se reprodujeron las estimaciones científicas, porque no se modificó código y el objeto de esta revisión es preparar mejoras operativas con evidencia suficiente. La implementación deberá pasar las validaciones dirigidas anteriores y la compuerta vigente del repo.
