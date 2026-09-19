# ENCARGO CODEX CLI · GEN2-REPLAY-Y-PISOS-CLI-1

Fecha de preparación: 19/sep/2026. Repositorio: `Josanoforo/Modelado-Mexicano`.
Base revisada: `9eff694ecff8e74d2aed05fe5fac9e4d530363fc` (merge de #860).
Revisión 1.1: incorpora el original `ENCARGO-GEN2-REPLAY-ASIENTOS-1-2026-09-17.md`, recibido después de preparar la primera versión de este encargo.

## Resultado que debes entregar

Desbloquear la publicación de las corridas ya selladas y producir los pisos de persistencia por eje que sí pueden medirse en ENVIPE 2024, ENCIG 2023 y ENIF 2021. Un PR con esas mediciones selladas, evidencia de replay y vistas derivadas coherentes. El objetivo es alimentar estimadores por segmento, no aumentar contadores.

Absorbe `GEN2-PISOS-PERSISTENCIA-1` y su dependencia `GEN2-REPLAY-ASIENTOS-1`. **Ambos originales están ahora en `fuentes/`.** Conserva sus bytes y procedencia; este documento adapta y agrupa su ejecución para Codex CLI. El original REPLAY fue redactado contra `e46e7e4`, antes de incorporar las dos corridas del piloto 2; de ahí su referencia a 38 o 40, que se vuelve a derivar al abrir.

Puede arrancar en paralelo con el 01, en worktree independiente. No requiere que el contrato v0.6 ya esté fusionado para medir. La adopción efectiva queda a cargo del 03; tú entregas la cadena y el mapa de resultados completos.

## Operación y límites

1. Lee este documento, `AGENTS.md`, los originales PISOS y REPLAY-ASIENTOS y la firma del 17/sep en `fuentes/`. Reporta ruta absoluta, rama, HEAD y estado del worktree; actualiza referencias con `git fetch --prune` y trabaja sobre main vigente. Conserva el trabajo de otras sesiones. Si ya comenzaste con la primera versión del 02, continúa en esa misma rama: conserva el encargo archivado y añade esta revisión como adenda trazable; no reinicies, no borres trabajo ni repitas verificaciones ya hechas en procesos aislados con evidencia suficiente en esta ejecución.
2. Busca duplicados por este rótulo, `GEN2-PISOS-PERSISTENCIA-1` y `GEN2-REPLAY-ASIENTOS-1` en worktrees, ramas remotas y PR abiertos. Si ya hay un resultado fusionado, verifica sus productos y continúa con el delta; si hay una ejecución equivalente viva, resuelve su continuidad antes de duplicarla.
3. Entorno: Codex CLI en Ubuntu/WSL con el corpus compartido montado. Reutiliza las raíces configuradas del clon padre en el worktree. Si falta una ruta, verifica la configuración y el censo antes de declarar ausente el payload. No publiques rutas sensibles ni microdatos. No inventes rutas de Windows ni copies el corpus al repo.
4. Autorizados: cambios del perímetro, commits, push de la rama y un PR. No autorizado: merge. Archiva este encargo y sus fuentes reales; `/acto` no es una dependencia de software de Codex. Aplica el procedimiento relevante con herramientas del repo y la precedencia de `AGENTS.md`.
5. No hagas llamadas a Claude/OpenAI ni otras API de modelos, no repitas elicitaciones y no adquieras fuentes nuevas por defecto. Los pisos se calculan con el corpus existente. Los replay utilizan capturas ya selladas cuando las necesitan; si un corredor exigiría una llamada nueva, reporta esa dependencia y preserva la evidencia histórica admisible.

**Compuerta original de REPLAY:** piloto 2 v1.1 fusionado, con sus dos CALC y adjudicación disponibles. Estaba cumplida en la base revisada, posterior a #858; confírmala por producto al arrancar. La antigua compuerta de PISOS (merge de REPLAY) se sustituye expresamente en este lote por la finalización comprobada de Fase 1 antes de la publicación de los pisos. Specs primero no autoriza saltar la reparación del registro. No ejecutes otra tarea manual de caja que escriba estos mismos derivados en paralelo; el 01 sí puede correr porque no abre microdatos. No detengas ni reconfigures el cron como parte de este encargo.

## Firma y alcance sustantivo

> Un piso no vencido en su celda-D es el estimador adjudicado de esa celda y se adopta salvo veto de mesa. Se adoptan las 20 celdas de ADR-538 y ADR-542 (piso C2) como estimadores por celda de sus reglas consumidoras. El vocabulario celda-D v0.6 lo escribe. Los retadores son credencial para emitir donde no hay piso, no sustitutos del piso donde lo hay.

El diseño firmado y el PISOS original fijan además persistencia de la ola anterior como piso marginal por defecto. Mides `p_{t−1}(desenlace | eje=categoría)`; no evalúas si predice mejor la ola actual. Su IC95 describe incertidumbre muestral en t−1: **no** incertidumbre predictiva de t, ni deriva temporal, ni causalidad. Esa limitación debe viajar al consumidor, no perderse en la nota.

## Fase 0 · Congela las specs de pisos antes de abrir cualquier microdato

**Orden dentro de este lote:** primero specs y COMMIT-1; después replay; después cálculo de pisos. Así una verificación de corridas antiguas no abre microdatos antes de congelar el diseño nuevo. No exijas que los datos históricos nunca hayan sido vistos por nadie; este no es un nuevo piloto ciego.

Lee metadatos, cuestionarios, FD, inventarios y resultados ya sellados. No abras respuestas individuales, ni ejecutes medidores reales o una corrida “en seco”, antes de COMMIT-1. Los metadatos ya extraídos pueden usarse; si el descriptor está dentro de un ZIP, leer únicamente su miembro documental no autoriza leer el CSV de respuestas.

Por cada celda objetivo fija:

- Identidad completa: regla, desenlace, instrumento, edición y periodo de referencia, unidad de observación, eje y categoría. En ENVIPE edición y periodo del delito no se confunden.
- Universo, filtros, centinelas y tratamiento de no respuesta tal como el árbitro define ese estimando. `60+` no basta: constan límites efectivos y códigos excluidos. No unifiques silenciosamente universos diferentes entre ejes.
- Correspondencia por texto y catálogo entre olas. Cambiar de nombre de variable no invalida equivalencia; reutilizar el mismo nombre tampoco la acredita. En ENIF, `P5_6_k` 2021 no mide lo mismo que en 2024: aplica lo acreditado sobre `P5_7_k` y D9 en ADR-538.
- Ponderador, estrato, UPM y llaves propios de la ola anterior. En ENIF 2021 `FAC_ELE`, no `FAC_PER`. Misma lógica estadística no significa exigir idéntico nombre de columna.
- Estimador y varianza: bootstrap de diseño con 10 000 réplicas, seed 42, siguiendo el esquema sellado pertinente de conglomerados/estratos. Define dominio, pesos replicados, estratos con una UPM, denominadores vacíos y reglas de soporte. No sustituyas por bootstrap i.i.d. de personas/delitos. Reutiliza el código acreditado cuando sea compatible; comparte réplicas dentro del instrumento cuando corresponda.
- Tolerancias de reproducción y referencia del futuro consumidor. Las referencias aún no implementadas se rotulan como tales.

Universo de trabajo inicial, a comprobar por equivalencia:

| Ola anterior | Destino actual | Ejes/desenlaces |
|---|---|---|
| ENVIPE 2024 | ENVIPE 2025 | evasión de norma: sexo, edad, escolaridad_proxy, dominio; denuncia con seguro: cobertura_seguro. Referencia inicial 13 + 2 celdas. |
| ENCIG 2023 | ENCIG 2025 | gobierno digital útil sin coerción: sexo, edad, escolaridad. Referencia inicial 10. |
| ENIF 2021 | ENIF 2024 | **ahorro solo informal**, desenlace principal D9: sexo, edad, escolaridad, localidad, cuenta_formal. Referencia inicial 14. |

La suma de esas referencias es **39**, sujeta a comparabilidad, no “40 obligatorias”. `formalidad` no entra: P3_13 no está en 2021. No midas EDER, ENUT ni horizonte corto en este lote.

**Atención al universo de 74:** la entrada ENIF de ejes tiene dos desenlaces: `ahorra_solo_informal` e `informal_cualquiera`, con 16 celdas cada uno. Este encargo cubre el primero; no reduzcas dos resultados distintos a una clave `(regla,eje,categoría)` ni declares que el segundo quedó cubierto. Tampoco amplíes el lote para medirlo sin que sea necesario para el objetivo definido.

Una diferencia sustantiva de reactivo/universo produce `NO-CONSTRUIBLE` en esa celda, con motivo concreto; no contamina las construibles de otros instrumentos. Si una equivalencia requiere una decisión sustantiva nueva, delimita ese subconjunto y continúa con el resto.

Crea una spec humana por instrumento, sidecar y `spec.yaml` en los CALC correspondientes. Usa los ids originales `CALC-PISOS-ENVIPE2024-EJES-0001`, `CALC-PISOS-ENCIG2023-EJES-0001`, `CALC-PISOS-ENIF2021-EJES-0001` solo si están libres. Congela medidor y diseño, ejecuta `spec-check` apropiado sin leer respuestas y haz COMMIT-1 conjunto. Un instrumento sin celdas construibles recibe dictamen; no fabriques un CALC sellado vacío para alcanzar tres.

## Fase 1 · Reparar la evidencia de replay y publicar lo que ya existe

### 1.1 Delimita el conjunto real

Cruza directorios con sello válido, `corridas.tsv` por `spec_id` y evidencia vigente en `forense/replay-evidencia.tsv`. Identifica (a) sellados sin fila publicada y (b) publicados cuyo veredicto se perdería por asiento ausente/no vigente. Reutiliza `_identidad_replay`, `_evidencia_vigente` y `_proyecta_replay` o sus equivalentes vigentes. Los 16 + 24 del 17/sep son referencia; usa unión de ids y no supongas que serán 40.

No rellenes asientos copiando el REPRODUCE del TSV derivado: la vista no puede certificarse a sí misma. **Cada CALC que aún requiera asiento en este conjunto recibe verificación fresca aislada en la presente ejecución**, como exige el original; una nota histórica de REPRODUCE no sustituye ese paso. Si main ya incorporó el producto de este acto, conserva los asientos vigentes y verifica solo el remanente. Tampoco repitas un replay ya realizado correctamente en esta misma rama al recibir esta revisión: incorpora su salida e identidad. La evidencia histórica sirve para comparar y preservar lo conocido si hoy falta capacidad, no para inventar la fecha o el resultado de una verificación fresca.

### 1.2 Verifica con aislamiento por CALC

Crea `tools/verifica_aislada.py`, o reutiliza un equivalente existente demostrado. Por CALC lanza un proceso separado con `python3 tools/corrida0.py verify <CALC>` o un wrapper que importe `verify(..., imprime=False)` y serialice su resultado en un **subproceso nuevo**. Devuelve RESULTADO y CONTEXTO separados, razones/deltas por RESULT, tolerancias aplicadas y la terna de identidad (`spec_yaml_sha256`, `script_blob_sha256`, `input_sha256_efectivos`). Conserva salida cruda por CALC en el artefacto de evidencia citado; la nota puede resumir y enlazar esa salida, sin repetir páginas de logs. No uses `registro --verifica` para ejecutar todo en un proceso: ADR-540/NC-0182 ya documentan interferencia por módulos compartidos.

Incluye `tests/test_verifica_aislada.py` con un fixture barato y sintético que demuestre la separación real de procesos y que resultado/contexto/identidad no se mezclan entre invocaciones. Comprueba la propagación de un fallo o limitación como tal; no devuelvas REPRODUCE por código de salida únicamente. Es una prueba del defecto de aislamiento ya observado, no un test por cada CALC.

Esta fase puede reabrir inputs de olas actuales **solo para reproducir corridas existentes cuyo contenido ya fue sellado**. No descubre cruces, no mide reservas nuevas y no altera specs/resultados originales. En la fase de pisos siguiente, ninguna ola actual se abre. Un replay que solo puede hacerse abriendo una reserva no consumida queda delimitado, no se fuerza.

Conserva el veredicto real, razones por RESULT, identidad, fecha, entorno y procedencia. Un NO-EJECUTABLE no borra un REPRODUCE histórico vigente. Un NO-REPRODUCE numérico nuevo sí es material y detiene el consumo afectado.

**NC-0313:** en DIN emisiones, `RESULT-DIN-LXE8-G-R-EXISTE-AL-CERRAR` cambió de NO a SI al aparecer R después. No edites el CALC ni sustituyas el veredicto global por REPRODUCE. Conserva la discrepancia y su alcance; comprueba específicamente los puntos/IC C2 si su consumo depende de ello. La nota existente reporta 220/221 resultados iguales, pero la ejecución debe reportar lo observado, sin usar 220/221 como condición prefijada.

### 1.3 Asienta y escribe

Completa la fuente de replay con el mecanismo existente; si no hay escritor, un script local pequeño que respete el esquema y valide identidad es suficiente. No hace falta crear otro servicio ni otro ledger. Añade los nuevos asientos sin reescribir los históricos, con las 14 columnas del esquema vigente: `calc_id`, `corrida_id`, `resultado_replay`, `contexto_replay`, `razones`, `spec_yaml_sha256`, `script_blob_sha256`, `input_sha256_efectivos`, `codigo_commit`, `fecha_verificacion`, `entorno`, `procedencia`, `alcance`, `nota`. La procedencia distingue la verificación aislada de este acto de cualquier evidencia previa. No inventes fechas.

Para un publicado sin asiento, si el fresco coincide, registra que sostiene el veredicto publicado y cita su fecha cuando esté acreditada; si no está, declara desconocida. Si difiere de forma concluyente, conserva ambas evidencias, registra la causa y abre o actualiza una NC de esa corrida con consumidores e impacto; reutiliza NC-0313 donde corresponda, sin duplicarla. Si hay solo limitación de acceso/entorno, conserva el token devuelto por el instrumento y su contexto: no normalices NO-EJECUTABLE/NO-VERIFICABLE a NO-REPRODUCE. No permitas que un nuevo asiento de limitación desplace una evidencia concluyente vigente; registra la limitación por separado cuando lo requiera el lector. Esa limitación no autoriza nombrar la corrida en `--lote` para degradar su veredicto publicado.

Deriva primero con `registro --fuentes` o `registro` sin escritura. Luego una sola escritura del lote de reparación mediante `registro --escribe`; usa `--lote` solo para los CALC cuyos cambios de veredicto estén expresamente justificados por evidencia concluyente obtenida. **`--lote` autoriza transiciones; no selecciona el conjunto a verificar.** El P3 original decía nombrar todas las asentadas, mientras P2 excluía las no verificables: aquí se explicita el conjunto mínimo de transiciones justificadas. Nunca lo conviertas en permiso masivo para degradar evidencias ajenas. Una proyección sin cambios ajenos no necesita esa excepción. La posterior publicación de las nuevas mediciones de pisos es otra escritura legítima, no una repetición del lote de replay.

Si una identidad impide publicar el conjunto, corrige dentro de este alcance la fuente del problema; no desactives REPLAY-PISADO. Un conflicto numérico real se reporta por id y se excluye del consumo posterior. Conserva el trabajo útil medido aunque la publicación quede materialmente bloqueada, con estado explícito y receta concreta.

Si el guardia nombra una corrida fuera del conjunto delimitado, detén esa escritura y reporta id/causa; no amplíes `--lote` para callarlo ni añadas `--excluye`. `git status` no vacío puede deberse a las specs recién creadas: verifica el diff de las vistas concretas y el resultado del comando, no uses el árbol sucio como prueba de que se publicaron.

### 1.4 Cierres del REPLAY original, por producto

- NC-0315: cierra cuando el bloqueo de registro quede resuelto por asientos y publicación, con el texto «remedio superado: asentar, no excluir»; si sigue bloqueado, enmienda el remedio y conserva abierta la deuda.
- NC-0284/0285/0286/0288: cierra o conserva cada una según su CALC y efecto real, sin cierre en bloque por acabar el script. Revisa igualmente el efecto sobre NC-0329, que incorpora las dos corridas del piloto 2.
- Añade la línea de hallazgo original, citada: «un veredicto de replay no se publica sin asiento en la fuente; verify que imprime y no asienta es media verificación». No crees una nueva capa de gobernanza.
- Corrige la explicación del contador del original: `status()` deriva en memoria y filtra GEN2; no lee simplemente el número de filas publicadas. Publicar puede dejar `N_corridas_selladas` intacto. La nota separa ese número, sellos físicos y nuevas filas publicadas; no afirma un 80→N causado por la escritura ni que el contador haya permanecido una semana por ese motivo sin acreditarlo.

## Fase 2 · Mide los pisos y entrégalos listos para el consumidor

Abre únicamente ENVIPE 2024, ENCIG 2023 y ENIF 2021 y sus insumos documentales declarados. No abras ENVIPE 2025, ENCIG 2025 ni ENIF 2024 para recalcular marginales, afinar universos o evaluar este piso. Usa las definiciones y R ya sellados solo como metadatos del destino, no como objetivo de ajuste.

Por instrumento: `preflight → run → verify`, conservando la separación COMMIT-1/specs frente a COMMIT-2/resultados. Un CALC por instrumento construible, con punto, IC, n sin ponderar, denominador ponderado si procede, universo, diseño y escala. Usa el esquema de RESULT de la casa; varios RESULT auxiliares no son varias celdas nuevas. Cuenta GEN2 bajo las reglas existentes y la firma del encargo; no reetiquetes derivados de GEN1 para inflar la cuenta.

Antes de publicar, asienta el replay de cada CALC nuevo con su identidad. Escribe vistas mediante el generador ya desbloqueado; reporta sellada/publicada por separado. Guarda en una tabla breve de entrega, o en la nota si ya es legible por máquina, cada identidad completa → CALC → RESULT puntual → IC → n → construible/no construible → consumidor previsto.

No modifiques la fuente de adopción que construirá el 03 ni los YAML de pilotos que modifica el 01. No declares `ADOPTADO_ACTIVO` por medir, por firmar o por figurar en una tabla. La decisión de piso por defecto ya está dada; el 03 materializa su consumo y actualiza el marcador.

## Perímetro, pruebas y cierre

Specs/sidecars y tres nuevos CALC de pisos; medidores y un helper estadístico mínimo si la reutilización lo necesita; evidencia de replay; `tools/verifica_aislada.py` y su prueba; salida por CALC citada; derivados de corrida0 por comando; nota de resultados y archivo del encargo/originales/adenda si aplica; NC realmente resueltas y cascada mínima existente. Los CALC anteriores permanecen intactos: que el lote cree CALC de pisos no autoriza editar un sello previo. No cambies `tools/corrida0.py`, reglas de aptitud, `tramite.yaml`, propuesta del árbitro, catálogo, crosswalk, celdas-D, θ ni cron.

Prioriza controles que cambian la cifra: sentido de códigos, denominadores, llaves/join sin multiplicar observaciones, bootstrap de diseño y reproducción determinista. Verifica al menos un estimador puntual por una ruta independiente simple con las mismas definiciones; no declares validación independiente de todos los IC por repetir el mismo bootstrap. No añadas tests de formato por cada celda. Ejecuta el baseline pertinente al cierre; conserva fallos heredados identificados.

No repares todo el inventario. Hasta aproximadamente 20% en control, salvo identidad/codificación/escala o contradicciones numéricas materiales. Un bloqueo externo se verifica una o dos veces y se entrega con receta, sin inventar una corrida ni pedir acceso que ya tiene el corpus compartido.

Antes del PR sincroniza main; si el 01 ya fusionó, conserva su contrato/estado y regenera los derivados. Las fuentes selladas de esta rama no se renumeran ni se reescriben por conflictos de documentación. Deriva los números de ADR/NC nuevos conforme al repo, sin abrir una NC por cada detalle cosmético.

Entrega: PR y HEAD remoto; número real de asientos recuperados, cambios de replay materiales y corridas publicadas; instrumentos y celdas medidas; exclusiones por texto/universo; mapa de RESULT listo para 03; status antes/después distinguiendo sus filtros. Incluye `NO-CORRIDO / RESERVAS` y `CONSUMIDO` con PR real. No fusiones. Éxito: pisos utilizables con cadena suficiente y el bloqueo de publicación resuelto, o el residuo material exacto identificado sin perder las mediciones obtenidas.
