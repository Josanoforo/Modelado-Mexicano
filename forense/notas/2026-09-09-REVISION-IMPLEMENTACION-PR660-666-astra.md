Insumo externo (ChatGPT/Astra) · 9/sep/2026 · registrado por ACTO GEN2-ADQ-CONTRATO-FIX · H1 confirmado textual por dirección · el texto de abajo no se edita

---

# Revisión adversarial de implementación · PR #660, #662, #663, #665 y #666

**Dictamen: implementación parcial; todavía no acredita cableado listo de extremo a extremo.** Hay correcciones reales y pruebas satisfactorias, pero quedan defectos reproducibles en autorización, selección temporal y conciliación, además de verificaciones operativas expresamente pendientes.

Revisión de Astra, 9 de septiembre de 2026. Documento para dirección/Claude: registrar por 0-bis A.3, contrastar con `origin/main` del despacho y convertir las correcciones en encargo. Este documento no firma decisiones ni modifica el repositorio.

## Alcance y estampa

Código integrado examinado: `Josanoforo/Modelado-Mexicano`, commit `f0f6bb75f0046c8913861c43d85bb381c3e8af2e`, merge de #666. Se contrastaron las propuestas anteriores sobre notas de PR y cableado SONDA/adquisición con los cambios y notas de los cinco PR indicados. Los ZIP de agosto son antecedentes, no evidencia del estado operativo de septiembre.

Al cierre de la consulta, `main` ya avanzó a `ffeeca2cd1a9df65f513f1b286b35761c1fcf806` mediante #667. Las pruebas aquí declaradas pertenecen al corte #666; no constituyen revisión científica del lote ENIF de #667. Dirección debe comprobar la persistencia de los hallazgos en el SHA que encargue.

| PR | Resultado de esta revisión |
|---|---|
| [#660 · Registro replay](https://github.com/Josanoforo/Modelado-Mexicano/pull/660) | Conserva evidencia y separa historia de verificación actual. Falta rechazar identidad incompleta al determinar vigencia. |
| [#662 · Preparación de lote](https://github.com/Josanoforo/Modelado-Mexicano/pull/662) | Mejora derivación de identidad y pruebas independientes del tamaño del árbol. No apareció un defecto bloqueante confirmado dentro de las comprobaciones realizadas. |
| [#663 · Operación 1](https://github.com/Josanoforo/Modelado-Mexicano/pull/663) | Añade candidatas al digesto y calibración de revisión. El buscador omite evidencia situada después de la primera mención. |
| [#665 · Cableado](https://github.com/Josanoforo/Modelado-Mexicano/pull/665) | Repara transporte, escalamiento y varias huellas. Persisten problemas en el contrato de selección y en la lectura del éxito operativo. |
| [#666 · Verificación CAJA](https://github.com/Josanoforo/Modelado-Mexicano/pull/666) | Documenta ejecución real y límites. Deja activos ambos disparadores y pendiente la primera corrida posterior al arreglo. |

## Hallazgos que requieren corrección

### H1 · P1 — Una negación de autorización se interpreta como autorización

**Observado.** En `tools/adq_doctor.py:358–365`, `_autorizada()` comprueba solamente si la nota contiene la subcadena `AUTORIZADA`. Una fila `PENDIENTE` con nota `SONDA-LATERAL-RECOMENDADA NO-AUTORIZADA`, sin invocación nominal, entra en `elegidos`. Se reprodujo ejecutando `selecciona_filas()`. `NO AUTORIZADA` presenta el mismo problema de subcadena.

**Interpretación.** La función no verifica una autorización afirmativa ni su cita. La selección contradice el límite humano establecido para el handoff de SONDA. Esto demuestra elegibilidad incorrecta, no una descarga no autorizada observada en producción.

**Consecuencia y corrección mínima.** Leer una autorización explícita e inequívoca en el campo vigente, conforme a A.16, con referencia verificable. Ausencia, negación o ambigüedad deben excluir con razón. No basta cambiar a una expresión con límites de palabra: seguiría aceptando «NO AUTORIZADA». Invocar una fila por nombre tampoco debe sustituir una autorización si el contrato requiere ambas.

**Aceptación.** Fixtures negativos para ausencia, negación con espacio, negación con guion y cita ajena; positivo para autorización afirmativa correspondiente a esa fila. Ningún caso negativo aparece en elegidos.

### H2 · P2 — La edad usa la primera fecha; no el último intento efectivo

**Observado.** En `tools/adq_doctor.py:340–355`, dos llamadas a `search()` devuelven la primera coincidencia. Para `intento efectivo 2026-09-01; intento efectivo 2026-09-08`, la función devuelve **1 de septiembre**. Para una descripción del intento del 6/sep que cita `forense/notas/2026-09-03-anterior.md`, devuelve **3 de septiembre**. Ambos contraejemplos se ejecutaron.

**Interpretación.** El plazo de reintento puede vencer antes de tiempo; el orden por antigüedad también queda alterado. Una fecha de referencia documental no demuestra un intento.

**Consecuencia y corrección mínima.** Derivar el último intento efectivo de entradas explícitamente identificadas. Fechas en nombres de archivo, descubrimientos y referencias no deben entrar en el cómputo. Si una nota histórica no permite decidir, declarar fecha indeterminada y llevarla a conciliación; no presentar una fecha inferida como medida. Dirección debe fijar el tratamiento de esa indeterminación antes de habilitar reintentos automáticos.

**Aceptación.** Múltiples intentos en distinto orden textual, descubrimiento posterior sin descarga, fecha en enlace, fecha inválida y ausencia de fecha. El cambio de fecha de una cita no modifica la elegibilidad.

### H3 · P2 — Nombrar una fila no implementa la excepción que promete el selector

**Observado.** `selecciona_filas()` documenta que las filas nominalmente pedidas pueden saltar estados que no se activan en bloque. Sin embargo, una fila `SIN-FETCH`, con nota `AUTORIZADA por mesa` y su fuente en `nombradas`, termina excluida como «estado fuera del contrato». La excepción evita el primer filtro, pero no encuentra después una rama de admisión. Contraejemplo ejecutado sobre la función actual.

**Interpretación.** El handoff puede seguir sin funcionar aun después de autorizar e invocar la fila. Admitir todas las filas nominales indiscriminadamente sería otra vulneración del contrato.

**Consecuencia y corrección mínima.** Dirección debe alinear selector, skill y runbook: definir si la autorización transforma primero el estado canónico o permite una excepción acotada. Implementar esa única conducta, con cobertura, objeto y cita comprobados. Incluir también el residual `OBTENIDO-PARCIAL` en la matriz de casos, sin habilitar su descarga completa por defecto.

**Aceptación.** Probar el recorrido real de una fila desde propuesta SONDA hasta selección del objeto faltante autorizado; no basta probar cada herramienta aisladamente.

### H4 · P2 — El digesto puede perder un cierre en el mismo documento

**Observado.** En `tools/digesto_tramite.py:1555–1591`, `_busca_candidatas_fila_k()` usa `texto.find(rid)` una sola vez. Si la primera ventana reproduce el texto del pendiente, hace `continue` sobre todo el archivo. Fixture ejecutado: primera mención `NC-0999` con la obligación original; más adelante, la misma ID con sucesora firmada y evidencia nueva. Resultado: ninguna candidata. Al conservar solamente la segunda mención, sí produce candidata.

**Interpretación.** Agregar contexto histórico a una nota puede hacer desaparecer una evidencia que antes detectaba. Por ello todavía no se cumple el objetivo de que toda fila cerrable aparezca en la siguiente rutina.

**Consecuencia y corrección mínima.** Examinar todas las apariciones con identidad completa y aplicar exclusiones por aparición, deduplicando después. Declarar archivos ilegibles como universo incompleto. La coincidencia sigue siendo candidata; el cierre humano debe conservar cita y estampa. Para sucesoras sin mención literal de la ID original, explicitar el seguimiento de referencias que realmente puede derivarse y el residual de lectura humana.

**Aceptación.** Primera mención excluida y segunda válida; varias candidatas en un archivo; ID que es prefijo de otra; fuente ilegible; sucesora enlazada sin repetición de ID. El tope de presentación no debe ocultar indefinidamente las filas posteriores: la rutina debe poder recorrer todas las candidatas.

### H5 · P2 — La señal de éxito de TCRON no incorpora la publicación fallida

**Observado.** `tests/check.py:5610–5614`, `_t_cron_exitosa()`, solo exige `invocado=si` y `exit=0`. Ejecutada con `publicacion=FALLIDA(1)`, devuelve `True`. El runner nuevo sí cuenta fallos de publicación y puede terminar con exit 4, pero la huella conserva por separado la salida del agente.

**Interpretación.** El predicado sigue midiendo finalización del agente; no basta como acreditación de operación completa. El contraejemplo prueba una laguna del consumidor de huellas, no acredita que ya se haya publicado en producción una huella contradictoria.

**Consecuencia y corrección mínima.** Distinguir explícitamente «agente terminó» de «corrida completó las obligaciones de publicación». Actualizar el criterio que acredite el día para interpretar fallos explícitos, conservando tratamiento declarado de huellas históricas sin ese campo. Revisar además el camino de publicación inicial del censo (`tools/adquiere_cron.sh`, alrededor de 527–550), que todavía registra algunos fallos sin incorporarlos al contador nuevo, y la recuperación cuando el push existe pero el PR diario no llegó a crearse.

**Aceptación.** Agente 0/publicación fallida; push fallido persistente; push recuperado; rama remota sin PR; huella histórica; PR fusionado con rama eliminada. Una prueba de runner completo debe comprobar salida, recibo y señal del vigilante conjuntamente.

### H6 · P2 — La identidad incompleta se acepta como evidencia vigente de replay

**Observado.** `tools/corrida0.py:2923–2936` compara cada hash solamente si el valor asentado no está vacío. Un recibo con resultado `REPRODUCE`, contexto `IDENTICO` y sin hashes devuelve `(True, '')` frente a una ejecución con identidad nueva. Contraejemplo ejecutado. Las **26 filas reales examinadas sí tienen los tres campos de identidad completos**.

**Interpretación.** Es una laguna de validación ante evidencia incompleta, no una corrupción demostrada de las 26 filas. Los vacíos funcionan como comodines justo donde la vigencia debería necesitar identidad.

**Consecuencia y corrección mínima.** Exigir identidad suficiente antes de proyectar vigencia; conservar recibos incompletos como historia con limitación expresa. Mantener un tratamiento explícito para cálculos sin insumos, sin equiparar esa situación a información ausente.

**Aceptación.** Vaciar por separado cada hash, cambiarlo y probar el caso sin insumos declarado. La ausencia de identidad nunca debe certificar que dos objetos son idénticos.

## Operación real: qué demuestra #666 y qué falta

**Observado en el registro de CAJA.** El 9/sep hubo dos arranques a las 07:30:07: el proceso 491 del cron legado perdió el lock y salió 3; el 371 ejecutó durante 228 segundos y terminó 0. La nota correlaciona el stdout exclusivo del crontab y `LastTaskResult=0` de Windows para atribuir al programador de Windows la corrida ganadora. El canal Operational estaba deshabilitado. Esta revisión leyó esa evidencia publicada; no accedió directamente a Windows.

**Interpretación.** Sí hubo rastro de ejecución. El lock contuvo la doble invocación, pero no convierte dos calendarios activos en un despliegue concluido. La corrida matutina precede a la fusión de #665 y no valida en vivo sus arreglos.

**Consecuencia.** Mantener abiertas y ejecutar las obligaciones ya registradas, sin crear duplicados:

- **NC-0114:** primera corrida de producción posterior al arreglo y correlación del recorrido.
- **NC-0119:** retirar el crontab legado después de esa comprobación, asentando la retirada en el registro correspondiente.
- **NC-0120:** habilitar la evidencia de eventos con la intervención requerida y observar recuperación de un disparo perdido. Tener `StartWhenAvailable=True` no prueba la recuperación.
- **NC-0115:** alinear autoridad del horario entre sus consumidores; la gracia TERM→KILL ya tiene default operativo, aunque falta su configuración central.
- **NC-0123:** reparar o declarar la ceguera del índice de reactivos a ENIF. Es una mejora material de SONDA ya identificada: no necesita otra fila de deuda para el mismo objeto.

El piloto SONDA halló cobertura parcial usando material ENIF ya presente. Es evidencia útil del sondeo y de su límite, pero no una prueba del handoff de descarga de un objeto ausente. Las reservas NC-0121/0122 pertenecen al alcance del instrumento y a la decisión sobre el proxy; no deben confundirse con fallos del cron.

## Validación ejecutada y despacho recomendado

En el corte indicado: `tests/test_adq_cableado.py` — **27 pruebas, 0 fallos**; `tests/test_corrida0.py` — **82 casos, 82 correctos**; `tests/test_adq_doctor.py` — **5 pruebas, 0 fallos**; `tests/test_digesto_candidatas.py` — **OK**. Además se ejecutaron los contraejemplos descritos. No se descargó corpus, no se invocó el agente productivo ni se alteró el programador de CAJA.

Encargar primero H1–H3 y H5 como reparación del contrato SONDA/adquisición, con una prueba conjunta de selección, ejecución y publicación; después H4 y H6 dentro de los derivadores existentes. La aceptación operativa requiere observar la versión desplegada: SHA, run_id, disparador, salida, recibo y PR deben corresponder a la misma corrida. Después se retira el disparador legado conforme a NC-0119.

No propongo una automatización nueva: son correcciones de piezas ya implantadas. Si dirección amplía el alcance con una guardia o rutina nueva, debe pasar D-14 por escrito: defecto real citado, daño material y costo menor que la conciliación manual. Registro por A.3, encargo con pruebas negativas, y cierre con cita y estampa del universo. El merge de mesa sella el acto; las verificaciones de CAJA no observadas permanecen pendientes.
