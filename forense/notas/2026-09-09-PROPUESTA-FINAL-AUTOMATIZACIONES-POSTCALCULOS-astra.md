> **Insumo externo (ChatGPT/Astra) · entregado a dirección 9/sep/2026 · registrado por ACTO GEN2-REVISA-CALC conforme a A.3 y regla de mesa 4 · el texto de abajo no se edita.**

---

# PROPUESTA FINAL · AUTOMATIZACIONES POST-CÁLCULOS GEN2

**ChatGPT (Astra) · 9/sep/2026 · entrega a dirección (Claude).** Revisa y sustituye, como propuesta, el `TRANSFER-AUTOMATIZACIONES-POST-CALCULOS-GEN2` adjunto. Dirección lo adapta al árbol del despacho, registra el acto externo y prepara los encargos; mesa sella mediante merge. **Este documento no implementa herramientas, no activa rutinas ni autoriza ejecuciones de datos.**

> **Principio rector:** automatizar la ejecución y la comprobación de decisiones explícitas; conservar separados estado del artefacto, reproducibilidad, comparabilidad, vigencia y juicio científico.

## 0. Decisión propuesta y alcance verificado

**Recomiendo empezar por REVISA-CALC, integrar después `lote` al siguiente lote real de caja y mantener `delta`, `vigencia` y `siguiente` como tres contratos acotados e independientes.** Hay evidencia para diseñar las cinco capacidades; no se sigue de ello que deban construirse todas antes de volver a medir. Cada acto se justifica por un uso próximo y por D-14. No se crea ninguna rutina programada nueva.

Árbol examinado: **`6e0381bbbc8bd243c23813d3182bcee85e0088bd`**, main obtenido el 9/sep/2026, incluye **PR #651 fusionado**. Lecturas: `/revisa`, funciones y parser de `corrida0`, pruebas pertinentes por inspección, registro/demanda, decisiones, reservas y correctivo C0-D. Consulté también los PR #614 y #651. No reaudité completas todas las corridas citadas por el transfer ni ejecuté microdatos.

| Observado | Interpretación | Consecuencia |
|---|---|---|
| `/revisa` tiene once puntos, revisión de la vista previa del merge y marca de vigencia. No encontré una rama REVISA-CALC en ese archivo. | Falta especializar la revisión, no otro revisor. | Añadir un bloque condicionado y reutilizar las reglas existentes. |
| El parser de `corrida0` no ofrece `lote` ni `siguiente`. `delta` y `vigencia` devolvieron `NO-IMPLEMENTADO`, código 2. Las búsquedas en `tools/` y comandos Claude no localizaron equivalentes del ciclo propuesto; `censo_lote_lapop.py` no es ese orquestador. | Las cinco piezas no están ya resueltas bajo esas interfaces en el universo examinado. | Mantener el backlog, con interfaces propuestas claramente marcadas como futuras. |
| `run` llama a `preflight`, reutiliza su snapshot de inputs y no sobrescribe un CALC sellado. `verify` tiene ejes de contexto y resultado. | Repetir el ritual literalmente puede duplicar aperturas y degradar estados. | `lote` coordina funciones existentes; no reproduce su lógica ni colapsa sus salidas. |
| `registro` sin `--escribe` dio diff vacío en las tres vistas: 106 filas de corridas, 1441 de resultados y 205 de usos. El worktree quedó limpio. | La vía de lectura existe; no necesita otro arreglo FP-359. | Reutilizarla y separar su escritura de la ejecución que produce sellos. |
| #651 produce `INCONCLUSO`, rama de refutación explícita y sucesor `NC-0077`; preserva la comparación histórica. | El correctivo ya está consolidado; no encargar otra vez la reparación #649. | Usar #649 como caso negativo histórico y #651 como positivo de sucesión. |
| `NC-0082` declara que faltó el documento íntegro de la revisión externa. | El problema de transporte de fuentes sí sigue abierto. | El anexo B de esta entrega lo transporta íntegro, con hash; dirección puede registrarlo por el circuito existente. |

Fuentes: [revisor vigente](https://github.com/Josanoforo/Modelado-Mexicano/blob/6e0381bbbc8bd243c23813d3182bcee85e0088bd/.claude/commands/revisa.md), [corrida0](https://github.com/Josanoforo/Modelado-Mexicano/blob/6e0381bbbc8bd243c23813d3182bcee85e0088bd/tools/corrida0.py), [pruebas](https://github.com/Josanoforo/Modelado-Mexicano/blob/6e0381bbbc8bd243c23813d3182bcee85e0088bd/tests/test_corrida0.py), [reservas](https://github.com/Josanoforo/Modelado-Mexicano/blob/6e0381bbbc8bd243c23813d3182bcee85e0088bd/forense/no-corrido.tsv), [origen del diferimiento, PR #614](https://github.com/Josanoforo/Modelado-Mexicano/pull/614), [correctivo #651](https://github.com/Josanoforo/Modelado-Mexicano/pull/651).

## 1. Cambios imprescindibles al transfer

1. **`lote` no es de sólo lectura por dejar `registro` en seco.** `run` escribe ejecución, resultados y sello. La interfaz debe separar previsualización, ejecución y escritura de vistas.
2. **No reducir `verify` a cuatro rótulos.** Preservar `contexto`, `resultado`, `veredicto` y razones, incluido `REPLICA-RESULTADO · CONTEXTO-DISTINTO`. No poder verificar un sello no demuestra que sólo falte corpus.
3. **Tolerancia de adopción no equivale a importancia científica.** `delta` separa equivalencia de representación al grano del consumidor de materialidad sustantiva.
4. **Una ola posterior no vence una medición histórica ni habilita fuga temporal.** `vigencia` evalúa el uso y su corte, no sólo la edad del dato.
5. **Un sucesor declarado no está necesariamente sellado, completo o adoptado.** La cadena y el residual deben verificarse por resultado y consumidor; no elegir la versión mayor por nombre.
6. **La demanda `CORR-*` no es un catálogo de CALC ejecutables.** `siguiente` necesita una correspondencia explícita con `CALC-*`; no inventarla desde `SIN-CANDIDATO` ni desde ids `RES-*`/`RESULT-*` parecidos.
7. **Reproducir no valida la inferencia.** REVISA-CALC mantiene una lectura humana corta sobre estimando, denominador, incertidumbre y adjudicación; #649 pasó la reproducción y aun así necesitó #651.
8. **No instalar una dependencia artificial entre las cinco piezas.** `delta` y `vigencia` pueden informar a `siguiente`, pero su ausencia no impide mostrar preparación mecánica básica. Ninguna bloquea medir mediante el runner vigente.

## 2. ACTO 1 · REVISA-CALC dentro de `/revisa`

### Producto y activación

Un bloque específico en el mismo informe/comentario vigente de `/revisa`. Cero nueva rutina, segundo comentario, revisión formal de aprobación o reparación automática.

Activar por cambios en `data/corrida0/CALC-*/`, specs de `forense/prereg-caja/`, decisiones y vistas de corrida; también por afirmaciones de ejecución/sucesión/adopción en el cuerpo del PR o por citas `corrida0_*` añadidas a consumidores. Un cambio de medidor compartido sólo amplía el conjunto a consumidores afectados demostrables por sus dependencias; no dispara replay de todo el programa.

**Selección acotada:** una fila cambiada del TSV global no obliga a revisar todos los CALC. Comparar filas por identidad, obtener ids afectados y referencias pertinentes. Si el cambio es sólo de firma/adopción, verificar ese efecto y no exigir otra corrida. Si no se puede resolver la correspondencia, declarar el límite.

No usar `CONTADOR: cero` para excluir un CALC: un cálculo envuelto legacy puede no contar y sí requerir revisión de sello y conclusión. Se conservan las exclusiones administrativas de `/revisa`; un `[TRAMITE]` mal clasificado se reporta por su cauce vigente, no se aprovecha para ejecutar otra auditoría.

### Comprobaciones y evidencia

| Pieza | Comprobación mecánica reutilizada | Lectura humana necesaria |
|---|---|---|
| Identidad/sucesión | CALC y RESULT tocados; `estado_calc`; cadena del registro; sellos de antecesoras intactos | Qué objeto cubre la sucesora y qué residual conserva |
| Congelación | Orden por ascendencia de commits, no sólo timestamps; hashes y archivos gobernantes | Si un cambio posterior es spec sucesora declarada; Git no demuestra desconocimiento previo del dato |
| Sello | Validador existente sobre recibo, sidecar y archivos cubiertos | Concordancia entre lo que el PR afirma y lo que quedó sellado |
| Replay | `verify` sólo en entorno permitido; conservar sus ejes y razones | Qué queda sin corroborar y si cambia la conclusión |
| Registro/status | Modo lectura, diferencias atribuibles al PR | Firma y clase E.1 explican por qué puede no moverse un contador |
| Adopción | Cita, generación, valor al grano y consumidor real, con controles existentes | Compatibilidad del estimando con el parámetro; una nota no es una ranura de p |
| Inferencia | Resultados/cobertura y pruebas locales existentes de ramas | ¿La conclusión excede al intervalo, al universo o al diseño? ¿Una secundaria modifica indebidamente la primaria? |

**Entorno:** `/revisa` prohíbe abrir/descargar microdatos en NUBE; que un payload resulte visible no levanta esa prohibición. En NUBE se verifican estáticamente contratos y sellos. Un replay con insumos exclusivamente de repo sólo se ejecuta si está dentro del alcance permitido y del presupuesto; no se activan llamadas LLM, adquisiciones o ejecuciones costosas por el mero diff. Si requiere CAJA, el informe declara `NO-VERIFICADO` con causa y receta para caja. Esa observación del revisor no se escribe como un nuevo estado de CALC.

Conservar la distinción entre **sello inválido**, **contexto no verificable**, **biblioteca ausente**, **input no visible**, **fallo de ejecución** y **divergencia numérica**. El primero puede bloquear la afirmación de sellado aunque ningún microdato esté disponible.

**Pesos propuestos:** contradicción material de identidad, sello, adopción o conclusión → `BLOQUEA`; replay inaccesible por frontera declarada → `NO-VERIFICADO/RESERVA`, sin degradarlo a aprobado; falta legítima de firma o adopción fuera del encargo → explicación, no defecto. Reutilizar los veredictos y la marca de vigencia de `/revisa`, releyendo PR/head/main/cuerpo antes de publicar.

### Aceptación y límites

Calibrar con un grupo mínimo de casos históricos: #634/#644 para semántica de verificación, #647 para adopción, #649→#651 para sucesión y límite de la reproducción. Reutilizar pruebas de sello inmutable, contexto y grano ya existentes. Una calibración documental no se rotula como replay de CAJA.

**Pasa cuando:** detecta una afirmación material falsa, reconoce la sucesora correcta sin pedir reescritura histórica y conserva una reserva de entorno sin inventar divergencia. No exigir que la máquina descubra automáticamente el problema estadístico del #649: el bloque humano debe hacerlo visible y citarlo.

**Perímetro:** `/revisa`, su runbook y pruebas/ayuda mínima que reutilicen el runner. Si basta modificar instrucciones y llamar validadores existentes, no crear script nuevo. No reformar en este acto todo el revisor.

**Límite heredado a resolver sólo si se usa post-hoc:** el archivo vigente combina una prohibición absoluta de commits/push con una instrucción de entregar post-hoc mediante PR propio. No tratar esa contradicción como permiso tácito. La calibración puede producir evidencia local que el ejecutor del acto registra en su PR; cualquier cambio de permisos del revisor debe quedar explícito en el encargo de dirección.

## 3. ACTO 2 · `corrida0 lote`, ejecución explícita y reanudación por artefactos

### Interfaz propuesta, aún no implementada

```bash
# Previsualizar: no corre medidores ni escribe resultados o vistas.
python tools/corrida0.py lote CALC-A CALC-B

# Ejecutar la lista explícita; registro sólo muestra el diff.
python tools/corrida0.py lote CALC-A CALC-B --ejecuta

# Ejecutar y autorizar además la materialización final de las vistas.
python tools/corrida0.py lote CALC-A CALC-B --ejecuta --escribe
```

Dirección puede adaptar los nombres, manteniendo las tres semánticas. `--escribe` sin `--ejecuta` se rechaza para evitar ambigüedad. No incluye commit, push, creación de PR, firma, adopción o cambio de spec.

### Conducta por CALC

1. Validar ids y duplicados, specs declaradas, orden solicitado y dependencias explícitas. No expandir la lista, elegir instrumentos ni crear sucesores. Una dependencia aún no materializada y congelada no se inventa como input futuro.
2. En previsualización, mostrar lo verificable con metadatos y estado; no llamar medidores. Si se ofrece comprobar payloads, identificarlo como inspección adicional permitida en ese entorno, no como evidencia ya obtenida.
3. En ejecución, usar `spec_check` donde su contrato de inventarios sea aplicable. Un FAIL local conserva su razón; un campo que refiere funciones/resultados de repo no debe transformarse en «reactivo ausente de una encuesta». La aplicabilidad se deriva de la spec; no se silencia un FAIL para continuar.
4. Para un CALC nuevo, llamar `run`, que **ya contiene preflight** y ejecuta su snapshot verificado. Mostrar ese preflight en el resumen; no volver a abrir tres veces el mismo corpus para rellenar columnas.
5. Para un CALC sellado, no llamar `run` otra vez. Reportar preexistente y verificar si procede. Un sello inválido o ejecución parcial no se borra para facilitar el relanzamiento: declarar bloqueo local y preservar archivos para un acto correctivo.
6. Ejecutar `verify` permitido y conservar contexto/resultado/veredicto. Derivar `estado_calc` al terminar. `SELLADA` y `REPRODUCE` son columnas distintas.
7. Hacer `registro` y `status` **una vez al cierre del lote**, incluidas sus fallas. Con `--escribe`, materializar sólo si la derivación es válida. Un resultado parcial sin sello puede impedir el registro global: mostrar esa causa y conservar los CALC válidos, sin presentar el registro como actualizado.

### Fallos, continuidad y presupuesto

Un `NO-ESTIMABLE` autorizado por la spec es un resultado científico legítimo, no un fallo técnico del lote. Puede convivir con otros resultados estimables del mismo CALC; no inferir un veredicto global buscando la cadena de texto en cualquier RESULT.

Fallo local → continuar sólo con los CALC independientes cuya ejecución siga siendo segura. Fallo de prerrequisito → omitir dependientes con cita de esa dependencia. Fallo compartido de raíz/librería → omitir o detener **las corridas que lo necesitan**, sin cancelar una corrida exclusivamente de repo por carecer de un corpus ajeno. Filesystem de salida no escribible o identidad global alterada → detener la escritura restante. No construir un motor de DAG: ordenar y saltar sobre la lista explícita y relaciones ya declaradas.

Reanudación: misma lista, reconocer sellos completos y conservarlos; no volver a contarlos como nuevos ni reejecutarlos para producir otro sello. Sin reintentos automáticos en v1. Tiempo y presupuesto se declaran en el encargo; una interrupción conserva resultados ya escritos y marca lo no ejecutado. No hay rollback que borre evidencia.

**Salida mínima:** CALC solicitado, estado previo, spec-check, preflight utilizado, acción run, contexto/resultado/veredicto verify, estado final y razón; al pie, estado de registro y status. Contar solicitados, sellados nuevos, preexistentes y bloqueados/omitidos. Los conteos de replay y desenlaces científicos se muestran aparte: no deben sumar como si fueran categorías excluyentes.

**Códigos de salida propuestos:** 0 = todas las piezas solicitadas llegaron al término técnico previsto; 1 = entrega parcial/fallo técnico local; 2 = petición inválida o imposibilidad de iniciar/continuar el entorno global. El resumen conserva cada código original; el exit global no sustituye la evidencia de `verify`. Un NO-ESTIMABLE legítimo no fuerza exit de error.

**Aceptación:** lote con éxito, fallo local y salida no estimable continúa correctamente; dependiente no corre; rerun no toca sellos; sin `--escribe` no cambia vistas; falta de corpus no impide una corrida independiente de repo. Probar con fixtures pequeños del runner y un lote autorizado real, no con nueva recaptura de pago.

## 4. ACTO 3 · `corrida0 delta`, comparación antes de adopción

La decisión anterior dejó B-7 opcional. **Esta propuesta recomienda activarlo cuando dirección tenga un par y una pregunta de comparación concretos**, empezando por el precedente #647; no declara que aquella decisión ya esté revocada. No bloquea F3 ni crea un umbral universal.

### Contrato

1. Entrada: consumidor y referencias explícitas de ambos valores, con CALC+RESULT en oferta y versión/hash del valor legacy. Una pareja propuesta puede declararse en el encargo/spec o mediante argumentos; no requiere adoptar primero ni escribir una cita falsa en `milpa` para poder compararla.
2. Congelar el legacy **anterior a la sustitución**. No tomar el valor actual del consumidor después de adoptar como si fuera la línea base histórica; podría medir GEN2 contra sí mismo.
3. Leer unidad, escala, dirección, población, periodo y transformación de las fuentes declaradas. Mismo consumidor no demuestra mismo estimando. Ausencia de metadatos → comparabilidad indeterminada; incompatibilidad demostrada → no comparable. Ninguna de las dos produce cero.
4. Identificar la versión efectiva por cadena y sello, sin resolver ids RESULT repetidos mediante la última fila o el nombre de archivo mayor. Si hay bifurcación, residual sin cubrir o sucesora sin sello, no elegir silenciosamente.
5. Emitir cambio firmado `nuevo − anterior` y magnitud absoluta, con unidad. Delta relativo sólo en escala y referencia que lo permitan; referencia cero o magnitud de origen arbitrario → no aplica, con razón. No convertir nulos o estados textuales en números.

**Tres campos separados:**

- **Comparabilidad:** demostrada / incompatibilidad / información insuficiente, con citas.
- **Cambio representado en el consumidor:** igual o distinto al grano/tolerancia declarados; reutilizar el comparador de adopción.
- **Materialidad sustantiva:** sólo bajo un criterio explícito y citado. Si falta, `NO-DETERMINABLE`, aunque el delta sea calculable. No inferirla de la tolerancia numérica.

Caso positivo #647: legacy 0.045694 y oferta 0.04569409956405095 son iguales al grano publicado de seis decimales; el cambio bruto es aproximadamente +9.9564e−8 en proporción. Eso demuestra equivalencia de representación, no una mejora del modelo ni una regla científica de materialidad. Casos negativos: estimandos diferentes, ausencia de ancestro, resultado no estimable y sucesoras ambiguas.

**Salida:** los dos valores/referencias, comparabilidad, transformación, delta y unidad, efecto al grano, criterio de materialidad y resultado. Siempre totales de pares examinados, comparables e indeterminados. «Cero materiales entre cero comparables» nunca se presenta como «GEN1 y GEN2 coinciden».

**Contador existente:** `diferencias_materiales` hoy cuenta presencia de `delta_legacy`, no una clasificación por umbral científico. No rellenar ese campo y heredar el contador sin revisar su semántica. En v1, el informe puede quedar separado y de lectura; si se integra a `status`, el mismo acto debe distinguir comparables, materiales y no determinables, preservando la historia de los ceros anteriores.

**Aceptación:** comparación de #647 correcta, par sin mapa visible, cero de referencia tratado, valor base no muta después de adopción y ninguna regla de materialidad inventada. No modifica valores activos, tiers o specs selladas.

## 5. ACTO 4 · `corrida0 vigencia`, por uso y con alcance

La unidad es **uso activo × resultado identificado × regla temporal/instrumental**. No hay un estado global «verdadero/falso» del dato.

Mantener separadas tres preguntas:

1. **Cadena:** ¿qué antecesora/sucesora declara el registro? ¿La sucesora tiene sello válido y cubre este resultado? ¿Queda residual? Reportar el estado autoritativo existente y cualquier insuficiencia para usar el reemplazo; no cambiar estados del registro desde esta consulta.
2. **Uso:** ¿qué versión sigue leyendo realmente el consumidor? Una nueva oferta no actualiza automáticamente ese uso.
3. **Adecuación temporal:** ¿ese periodo/instrumento cumple la regla del consumidor o del corte de evaluación? Sin regla o sin datos suficientes, vigencia no determinable; ausencia de alerta no equivale a vigencia demostrada.

**Nueva ola:** puede disparar una candidatura de actualización sólo si existe evidencia en manifiesto/adquisición y la regla del uso la hace pertinente. Un `fecha_descarga` posterior no prueba una ola posterior, identidad instrumental equivalente ni que esa ola esté disponible. Distinguir conocida, adquirida, verificada y calculada usando los estados existentes.

**Contraejemplos de aceptación:** una tasa ENIGH 2022 usada para describir 2022 no vence porque exista 2024; un pronóstico con corte anterior no puede actualizarse usando la ola objetivo; una estimación del presente con política de actualización sí genera candidato cuando aparece una ola pertinente. Son pruebas de contrato, no afirmaciones de que esas sustituciones ya ocurrieron.

S6 v3→v4 y marcador v2→v3 son casos reales de sucesión metodológica: no confundirlos con caducidad por calendario. Una firma de contador pendiente tampoco vuelve científicamente obsoleta una corrida.

**Salida:** consumidor, referencia activa, cadena observada, cobertura de sucesora, regla/corte aplicado, candidato con evidencia, razón y siguiente acción sugerida. La máquina puede citar una cola de adquisición/sonda existente; no adquiere, firma, cierra NC ni sustituye valores. Si se incorpora al digesto, es una sección de la rutina vigente, no otro calendario.

**Aceptación:** alerta sobre uso realmente desfasado bajo regla declarada; no alerta por simple edad, ola inaplicable o cambio de contador; bifurcación y sucesión parcial quedan visibles; ninguna fecha se interpreta como decisión automática.

## 6. ACTO 5 · `corrida0 siguiente`, preparación mecánica sin elegir la ciencia

**Producto mínimo:** vista de candidatos declarados y sus bloqueos, no puntuación opaca de «camino más corto». El tiempo/coste no puede inferirse contando cuántos campos faltan.

1. Acotar a la cartera o lote que mesa/dirección prioriza. La importancia científica viene de allí; no de un ranking inventado por la herramienta.
2. Resolver `CORR-*`/`RES-*` a `CALC-*`/`RESULT-*` sólo cuando hay relación explícita. Sin spec candidata, informar necesidad de spec; no fabricar un CALC con ese número. Usar lectores actuales y declarar si las vistas están desfasadas.
3. Consultar `estado_calc`, cadena, dependencias y bloqueos **expresamente vinculados**. Una FP de contador que dice no bloquear medición no impide ejecutar. Texto ambiguo requiere lectura; no se trata como camino despejado.
4. Separar preparación de código/spec, evidencia de disponibilidad de inputs y disponibilidad en **este entorno**. Ver un id de payload en NUBE no certifica bytes/hash disponibles en CAJA. La comprobación final sigue siendo preflight al ejecutar.
5. Mostrar: candidatos comprobados hasta ese nivel, candidatos con comprobación pendiente, bloqueados y ya cubiertos con cita. Ordenar dentro de la prioridad humana por condición comprobada y desempate estable; no llamar «listo» a lo que aún necesita una decisión de estimando.
6. No duplicar trabajos ya cubiertos ni perder residuales porque existe una sucesora de nombre parecido. La cobertura exige el objeto preciso.

**Sin dependencia obligatoria de `delta`/`vigencia`:** si existen, añadir su información; si no, declarar ese límite y seguir mostrando preparación. No simularlos con regex sobre notas ni devolver puntuación cero como si hubieran concluido algo.

**Aceptación:** un CALC realmente ejecutable figura con evidencia; una demanda sin spec no; falta de firma no bloqueante no lo hunde; falta de corpus no aparece como fallo de premisa; una sucesora parcial no oculta residual. Cero ejecución, generación de specs o conexión automática a `/despacha` en v1.

**Gate de economía reforzado:** primero probar el orden propuesto contra una selección humana del siguiente lote. Si la vista no evita trabajo repetido o un despacho incorrecto, conservar la consulta manual y no implementar el ranker. Disponibilidad de datos no basta para justificar una herramienta de priorización.

## 7. D-14, orden de entrega y coste

| Capacidad | Defecto real observado | Cómo puede cambiar un resultado/decisión | Por qué automatizar sería más barato y cuándo parar |
|---|---|---|---|
| REVISA-CALC | Correcciones repetidas de contexto/lector y adjudicación #649→#651 | Puede validarse un artefacto mal interpretado o declararse mal su reproducción | Reutilizar validadores y una lectura específica en la revisión que ya corre; no segundo auditor. Medir duración y falsos bloqueos. |
| lote | #614 difirió el ritual; corridas sucesoras posteriores repiten pasos; FP-359 documenta riesgo de escritura inadvertida | Omisión/confusión de etapas puede declarar entrega completa sin verificación o escribir vistas sin intención | Envoltura pequeña alrededor de funciones existentes, aplicada a un lote real; si no ahorra coordinación, seguir con comandos individuales. No afirmar que ya medimos ese ahorro. |
| delta | NC-0048 dejó sin respuesta comparación GEN1↔GEN2; #647 aporta un par real y diferencia al grano | Un cero sin comparabilidad o materialidad inventada puede decidir una adopción equivocada | Una receta de comparación repetible sobre pares explícitos; lanzar cuando mesa quiera esa comparación. No cartografiar todo el modelo sólo para alimentar la herramienta. |
| vigencia | Sucesoras S6/marcador y residual de firma v4; alcance antiguo de L | Puede leerse versión superada o usarse información posterior al corte | Derivación sobre usos/cadenas/reglas existentes, sin búsqueda de fuentes; si falta regla temporal, pedirla dentro del encargo en vez de automatizar el juicio. |
| siguiente | NC-0072/0076 registran falta de oferta pertinente pese a resultados sellados; demanda contiene recetas ausentes | Puede despacharse una adopción/corrida que no tiene insumos o destino válido | Sólo si el piloto de selección demuestra ahorro; si exige reconstruir todas las correspondencias a mano, no pasa economía y se difiere. |

**Orden práctico:**

1. Registrar esta propuesta y despachar ACTO 1. No incluir implementación de las otras cuatro en ese PR.
2. ACTO 2 unido a un lote de cálculos explícito y próximo; conservar la posibilidad de correr ese lote con comandos vigentes si la automatización se retrasa.
3. ACTO 3 y ACTO 4 independientes, ordenados por la próxima decisión de comparación/actualización. `delta` sigue opcional hasta su autorización concreta; `vigencia` no necesita esperarlo.
4. ACTO 5 tras su piloto de utilidad; no esperar artificialmente a 3/4 ni conectarlo de inmediato a `/despacha`.

Un acto por producto fusionable; no abrir cinco PR simultáneos sobre `tools/corrida0.py`. Compartir funciones existentes, no crear framework, planificador, caché persistente de estados, base de datos o motor de workflows. Si se necesita una pequeña salida estructurada, derivarla de esas funciones; stdout de texto no se convierte en API mediante búsquedas frágiles de palabras.

Cada cierre declara tiempo de implementación, tiempo de uso, caso material protegido y qué quedó manual. Revisar utilidad tras los dos primeros usos; las herramientas conservan además la evaluación de retiro D-14. Una guardia barata puede permanecer aunque el defecto no reincida. El resto del esfuerzo va a medir y adoptar.

## 8. Qué se conserva fuera del encargo

No reimplementar `estado`, `registro`, `status`, T-REPRO, bandeja/conciliación #650 ni SONDA. Usar los controles de reproducción ya existentes; no escribir otra implementación de todos los errores históricos.

No auto-adoptar, auto-firmar, auto-mergear, reparar specs, decidir proxies, elegir instrumentos, dictar causalidad o disparar recapturas. `limpia_arbol --reporta` se conserva; `--aplica` sigue fuera de prioridad. Ninguna de estas capacidades requiere otro digest o activador programado.

En consultas, «siguiente acción» es una recomendación derivada, no un encargo enviado. Nuevos rótulos de presentación no se escriben en FP/NC/CALC como estados paralelos. Cierre de deuda siempre por la rutina autorizada, con cita y estampa de universo; nada se borra.

## 9. Texto de despacho para dirección

**Claude/dirección:** toma este documento como propuesta final de Astra, no como cinco automatizaciones ya autorizadas. Refresca `origin/main`, verifica existencia y colisiones, y archívalo por 0-bis/A.3 antes o junto con el lanzamiento. Reutiliza las reservas existentes; no reserves números de memoria.

Prepara primero **REVISA-CALC** dentro de `/revisa`, con la especialización y casos de aceptación de §2. Mantén el modelo de permisos, el único comentario y la marca de revisión vigente. No añadas ejecución de CAJA a NUBE ni un segundo revisor. Donde el contrato vigente de post-hoc se contradiga, entrega la calibración mediante el ejecutor del acto y somete cualquier cambio de permisos de forma explícita.

Deja preparados los contratos 2–5 para sus próximos usos, conservando las condiciones de §7. Antes de despachar `delta`, confirma que mesa quiere activar B-7 para el par concreto y qué significa materialidad si se necesita ese juicio. Antes de `vigencia`, localiza reglas temporales del uso. Antes de `siguiente`, prueba su utilidad en la cartera elegida.

El anexo B contiene la revisión original del #649 que faltó en #651. Regístrala como documento histórico externo con su procedencia y hash; **no la uses para reabrir automáticamente defectos ya corregidos**. Cuando esté archivada y citada, el trámite puede proponer el cierre de `NC-0082` con esa evidencia. Esto resuelve transporte de fuente, no agrega otra auditoría.

**Criterio final de aceptación:** una revisión CALC distingue integridad, entorno y juicio; un lote no sobrescribe ni confunde entrega parcial con completa; delta no fabrica comparabilidad/materialidad; vigencia respeta el corte del consumidor; siguiente muestra preparación sin elegir ciencia. Cada capacidad debe ahorrar una acción repetida o impedir un error material demostrado. No se exige completar la plataforma para continuar el programa.

## Anexo A · Recetas de verificación existentes

Estas interfaces se verificaron por código y, donde se indica, por ejecución. No son las interfaces futuras de los cinco actos.

```bash
git rev-parse HEAD
python tools/corrida0.py estado CALC-C0D-MARCADOR-v3 --json
python tools/corrida0.py registro
python tools/corrida0.py status --json
python tools/digesto_tramite.py --mesa --id NC-0082 --sin-suite --stdout
```

`registro` se ejecutó sin escritura y produjo diff vacío. `delta` y `vigencia` se invocaron y salieron con código 2 y `NO-IMPLEMENTADO`. `verify` se inspeccionó para conservar sus tres componentes; no se presenta aquí una nueva reproducción independiente del #651. Las consultas de este anexo sirven a dirección para refrescar la fotografía antes del encargo.

## Anexo B · Revisión original del #649, transportada íntegra

El texto que sigue es histórico: se entregó antes de #651. La evidencia de corrección posterior está en §0. Su inclusión aporta la fuente que `NC-0082` declaró ausente; no reemplaza la lectura del correctivo.

Fuente: `REVISION-ADVERSARIAL-PR649.md` · SHA-256: `ccd2219a5522a00db60feebb81eda6353bb9b1153dd4931c2c8df2c2212139fd`. El bloque delimitado a continuación conserva sus bytes UTF-8 completos.

<!-- INICIO FUENTE VERBATIM REVISION-ADVERSARIAL-PR649.md -->
# Revisión adversarial del PR #649

Revisión de ChatGPT (Astra), 9 de septiembre de 2026. Entrega a dirección para valoración y registro; no constituye una firma de mesa ni un encargo despachado.

**Veredicto: la medición es reproducible; la adjudicación exige corrección.** El defecto principal ya afecta al resultado publicado: `NO-DISCRIMINA` se convierte en una explicación que los datos no demuestran. Dos pruebas adversariales descubren además ramas que adjudican incorrectamente resultados inequívocos. Hay una cuarta discrepancia entre el encargo y la condición que activa el sucesor de alcance.

## Alcance y evidencia

Revisé [PR #649](https://github.com/Josanoforo/Modelado-Mexicano/pull/649), ya fusionado el 9/sep/2026 a las 04:16:16 UTC, comparando base `9ce9774e01389be6769fec501832e475462f50b1` con cabeza `cb10eb9ef5e9089141423236800d76ee57a18815`. Merge: `be6b852e309b2991543cd7b4680b1d74d40a8c51`. Los cuatro hallazgos siguientes afectan a piezas añadidas por este PR. El medidor y la spec v1.1 coincidían también con `origin/main` obtenido durante esta revisión.

- Verifiqué los SHA-256 de los **260 insumos** declarados por `CALC-C0D-MARCADOR-v2`.
- Ejecuté directamente `medir(inputs, spec)` con sus bytes y reproduje **152 de 152 resultados exactamente**.
- Ejecuté dos escenarios sintéticos de adjudicación y una mutación de identidad, exclusivamente en memoria, sin modificar artefactos sellados.
- Contrasté encargo, specs, medidor, resultados, nota de cierre y propagación en ADR-426. No ejecuté la suite completa ni recalculé R/M desde microdatos; la reproducción prueba esta transformación, no la validez independiente de todos sus insumos.

## 1. P1 · La incertidumbre se convierte en una explicación demostrada

**Observado.** [Medidor, líneas 380–381](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py#L380) asigna `EXPLICADO-POR-METRICA` cuando el intervalo incluye cero. Implementa fielmente [spec v1.1, §5.2](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/forense/prereg-caja/C0D-MARCADOR-spec-v1_1.md#L150), que afirma que la diferencia es «la sombra de unas pocas celdas con error grande». Esa lectura se propaga a la nota y a [ADR-426](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/canon/gobernanza-v1_15.md#L7446).

Los resultados reproducidos son:

| Comparación | Diferencia de MAE, corpus menos solo |
|---|---:|
| Marginales, universos distintos | +7.9116 pp |
| Universo común de 13 celdas | +4.6978 pp |
| Media de diferencias pareadas | +4.6978 pp |

La igualdad de las dos últimas filas es algebraica: sobre las mismas celdas, `media(|e_corpus| − |e_solo|) = MAE_corpus − MAE_solo`. La métrica sigue siendo el error absoluto en puntos porcentuales. El pareo aporta una evaluación conjunta de la incertidumbre; no elimina la diferencia puntual. El IC95 es `[−0.8022, +11.2747]`.

**Interpretación.** Es correcto decir que la regla preregistrada no confirma una dirección. No es correcto deducir que la diferencia quedó explicada por la métrica, ni que las celdas grandes sean un artefacto por ser grandes. El intervalo también admite un empeoramiento material; no demuestra equivalencia. La concentración en tres celdas es una descripción adicional, no una explicación causal o un criterio de invalidez. Es el mismo límite inferencial que distingue falta de evidencia contra una hipótesis de evidencia a su favor, recogido por la [declaración de la ASA](https://www.tandfonline.com/doi/full/10.1080/00031305.2016.1154108).

**Consecuencia.** El programa puede tratar una comparación inconclusa como un problema ya explicado. El error está tanto en la spec como en su implementación y propagación; cambiar sólo la prosa dejaría el resultado mecánico equivocado.

**Corrección mínima.** Mantener `NO-DISCRIMINA` como destino del hallazgo cuando ése es el resultado. Separar el cambio de universo —medido— de la incertidumbre —medida— y de la causa del patrón —no identificada—. No introducir una prueba de equivalencia o un umbral elegido después de mirar estos datos.

## 2. P2 · Un cambio de posición de M puede anular una primaria concluyente

**Observado.** [Medidor, líneas 378–379](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py#L378) compara la ordenación de los **tres corredores** y da precedencia a `EXPLICADO-POR-UNIVERSO` sobre `CORPUS-ESTORBA`.

Contraejemplo ejecutado con el medidor real: 14 celdas, R=0.20; error absoluto de solo=5 pp y corpus=6 pp. Falta solo en una celda. M tiene error de 4 pp en las 13 comunes y de 34 pp en la excluida. Actualicé también los puntos del agregado de control para que representaran el mismo escenario. Ambos controles pasan.

| Salida | Resultado reproducido |
|---|---|
| Orden marginal | `L_SOLO=5 < L_CORPUS=6 < M=6.1429` |
| Orden común | `M=4 < L_SOLO=5 < L_CORPUS=6` |
| Primaria | `+1 pp`, IC95 `[+1,+1]`, n=13; `CORPUS-ESTORBA` |
| Adjudicación | `EXPLICADO-POR-UNIVERSO` |
| Sucesor | `NO-APLICA` |

**Interpretación.** Sólo M cambia de posición. El contraste corpus–solo conserva el orden y empeora exactamente un punto en todas las parejas. El cambio de ranking de un tercero no explica ese hallazgo. La adjudicación contradice la prioridad declarada de la comparación L↔L.

**Consecuencia.** Es un defecto latente, no la rama que cayó en los datos actuales. Con insumos admisibles puede ocultar una primaria inequívoca y desactivar su sucesor.

**Corrección mínima.** Derivar la adjudicación primaria exclusivamente de L↔L en `U_LL`. Reportar el efecto de igualar universos como diagnóstico separado. Si se conserva una categoría explicativa por universo, su condición debe comprobar el contraste relevante y no puede invalidar evidencia primaria que continúa presente.

## 3. P2 · CORPUS-AYUDA no tiene una adjudicación propia

**Observado.** El [else final, líneas 384–385](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py#L384) también asigna `EXPLICADO-POR-METRICA`. Sin embargo, la spec §5.2 condiciona esa explicación a `NO-DISCRIMINA` y §4 declara que `CORPUS-AYUDA` refuta el hallazgo de empeoramiento.

Contraejemplo ejecutado: R=0.20 en 14 celdas; corpus=0.20, solo=0.30, M=0.22. Universos idénticos y controles conformes. Resultado: media d=−10 pp, IC95 `[−10,−10]`, `CORPUS-AYUDA`; adjudicación: `EXPLICADO-POR-METRICA`.

**Interpretación.** Hay evidencia inequívoca en dirección contraria dentro del escenario. El código la clasifica con una rama cuya condición no se cumple. No es sólo una etiqueta poco expresiva: fusiona dos desenlaces que el encargo exige distinguir.

**Consecuencia.** Defecto latente que no cambia la cifra de esta corrida, pero vuelve incompleta la promesa de tres desenlaces.

**Corrección mínima.** Hacer explícita y exhaustiva la correspondencia entre las ramas: ayuda → hallazgo de empeoramiento refutado con alcance; estorba → confirmado con alcance; no discrimina → inconcluso. Dirección determina los tokens compatibles con el árbol. Eliminar el `else` que convierte cualquier caso restante en explicación.

## 4. P2 · La condición del sucesor de alcance se estrecha respecto del encargo

**Observado.** El [encargo, P3](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/forense/encargos/2026-09-09-GEN2-C0-D-MARCADOR.md#L11) pide nombrar el sucesor de recaptura cuando las capturas sean pre-GEN2. La spec §5.3 y el [medidor, líneas 387–389](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py#L387) sólo lo activan ante `CONFIRMADO-CON-ALCANCE`. En esta corrida sale `NO-APLICA` y [la nota, línea 23](https://github.com/Josanoforo/Modelado-Mexicano/blob/cb10eb9ef5e9089141423236800d76ee57a18815/forense/notas/2026-09-09-GEN2-C0-D-MARCADOR-cierre.md#L23) afirma que el límite de alcance no muerde para esta rama.

**Interpretación.** El resultado estadístico no actualiza el corpus observado. La limitación temporal permanece tanto si el contraste ayuda como si estorba o no discrimina. No identifiqué en las piezas revisadas una autorización independiente para estrechar esa condición; queda como pregunta concreta para dirección si existe fuera de ellas.

**Consecuencia.** Hay dos lecturas en conflicto: la salida mecánica dice que no aplica sucesor y la deuda `NC-0077` sí conserva la recaptura. **La deuda no desapareció**, y eso mitiga el defecto. Pero un consumidor del resultado puede concluir que el alcance quedó resuelto cuando sólo cambió la rama estadística.

**Corrección mínima.** Mantener separadas la conclusión estadística y la necesidad de actualizar el alcance. Reutilizar `NC-0077` como referencia del sucesor de alcance, sin abrir otra deuda ni ejecutar una recaptura en este arreglo. Alinear la nota y el resultado futuro con la condición del encargo, o citar la decisión que la modifica.

## Observaciones menores y límites que no elevo a bloqueo

**13, no 14.** La nota, línea 32, afirma que M gana «sobre estas 14 celdas». Las dos secundarias declaradas y reproducidas tienen n=13. Corregir el enunciado a las 13 celdas comunes y conservar su carácter secundario; no es una falla del cómputo.

**Correspondencia no equivale a identidad de contenido.** Intercambié en memoria las capturas SOLO de CIV-M-01-01 y CIV-M-02-01: los 152 resultados siguieron idénticos y la guardia emitió `CORRESPONDE`. El código construye la llave con el nombre del input y sólo comprueba `variante`, no `id_celda` e `indice` del JSON. No encontré identidades incorrectas en las 224 capturas reales. Además, intercambiar bytes después del sellado sería detenido por los hashes del runner: esta prueba se hizo directamente sobre `medir`, no es una evasión de preflight. Es una limitación de lo que acredita esa guardia, no evidencia de contaminación de esta corrida. Si se refuerza la guardia en una sucesora, basta contrastar ambos campos existentes.

La v1 fallida quedó preservada y la v2 reparó la fuente L. Las reservas de segmentación, adopción, B incompleto y metadatos no se convierten aquí en nuevos hallazgos: ya están declaradas. Tampoco atribuyo a este PR fallos generales de CI o carencias anteriores del corpus.

## Encargo correctivo mínimo propuesto a dirección

Como el PR está fusionado, procede un acto correctivo sucesor, registrado por el circuito vigente; conservar las corridas y los sellos históricos. No hace falta rehacer la infraestructura ni recapturar datos para corregir esta adjudicación.

1. Registrar esta revisión y decidir la corrección de la tabla de adjudicación. El asunto material es qué conclusión permite la evidencia, no la reproducción de los decimales.
2. Preparar spec y medidor sucesores con ramas explícitas, sin veto de M sobre L↔L y con el sucesor de alcance separado del signo del contraste. Elegir identificadores desde el árbol del día.
3. Reejecutar sobre los mismos insumos. Las cifras de la primaria deben permanecer `+4.6978 pp`, IC95 `[−0.8022,+11.2747]`, n=13; el destino debe conservar la incertidumbre sin presentarla como explicación.
4. Validar los dos contraejemplos de esta revisión y el caso real. Son pruebas dirigidas a fallos demostrados. Conservar también la precedencia de controles inválidos y cobertura insuficiente.
5. Corregir mediante cita de sucesión la nota, la adjudicación propagada y el enunciado n=14. Reutilizar `NC-0077`. Mesa sella el acto correctivo mediante su merge.

**Texto sustantivo que sí sostiene la corrida:** «En las 13 celdas comparables, L con corpus tiene un error absoluto medio 4.70 pp mayor que L solo. El IC95 bootstrap va de −0.80 a +11.27 pp: la comparación no discrimina la dirección bajo la regla preregistrada. Igualar el universo reduce la diferencia marginal; no demuestra que el resto esté explicado por la métrica. La conclusión se limita a las capturas y al corpus observados.»

<!-- FIN FUENTE VERBATIM REVISION-ADVERSARIAL-PR649.md -->
