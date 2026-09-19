# ENCARGO · GEN2-RECIBO-CODEX-3 · versión integrada para ejecución paralela

**Base:** `843a5f977e024ef5d74863e95856c763bee9e58d`, 19/sep/2026. **Entorno asignado:** Codex CLI documental, sin abrir microdatos; se adapta el original de nube para esta tanda. **Sesión:** una sola, nueva, worktree propio y rama `codex/gen2-recibo-codex-3` o equivalente libre. **Compuerta inicial:** v2.14 y #865 en main, satisfecha en la base revisada, verificar al abrir. **Modelo:** Codex asignado, sin llamadas externas. **Contador:** acto sin mediciones nuevas; no atribuye incrementos de GEN2. **Entrega:** un PR completo, sin merge.

## Resultado

Dejar aplicadas las firmas y el veto, resolver el trámite pendiente de #865/#866 por producto, corregir sucesores operativos y entregar a Claude antecedentes utilizables para marcador/adopción. Absorbe el aterrizaje 01-bis, ya obsoleto por el merge de #865. No crea un recibo futuro solo porque la rama contrato ya integrada figure como pendiente en el texto antiguo.

Puedes empezar inmediatamente en paralelo con A. Las decisiones firmadas, el recibo de contrato, infraestructura y rutinas no esperan sus mediciones. Los cierres que dependen de publicación/replay se completan tras incorporar el merge de A, dentro del mismo encargo.

## Autoridad, fuentes y premisas

Lee AGENTS.md, instrucciones v2.14, este encargo, `00-PLAN-Y-LANZAMIENTO.md`, el original `ENCARGO-GEN2-RECIBO-CODEX-3-2026-09-19.md`, los briefs 00/01, TRÁMITE-5, el encargo 01 y los fragmentos de estado. Se adjuntan completos en fuentes. Este documento prevalece en los ajustes operativos que enumera; conserva los originales intactos y su procedencia.

No necesitas un slash command `/acto` disponible en Codex. Ejecuta el procedimiento aplicable con las herramientas existentes. La ausencia del comando no es un bloqueo sustantivo. Una sesión por encargo; si otra sesión ya ejecuta este recibo, continúa aquella o coordina el traspaso sin duplicarlo.

En main revisado, las 18 NC nombradas en el recibo siguen ABIERTA y no aparecen las filas de decisiones FP-379/FP-385 por objeto buscado. #865 y #867 están fusionados; #868 está abierto y no constituye adopción consolidada. Re-verifica cada objeto: si ya está resuelto, cita su producto y ejecuta el delta.

La comparación con `09681abe`/`782293a` es contexto histórico. Toda cifra de estado actual se deriva del HEAD vigente. No uses los ZIP de agosto como fuente de conteos ni autoridad actual.

## B1 · Firmas, veto y sucesores: ejecutar lo ya decidido

Archiva el original con sus verbatim. Propaga por objeto y evita filas duplicadas:

- D1, mesa «El dueño del marcador es acá»: construcción y adopción quedan en `GEN2-MARCADOR-REDISENO-1`, lado Claude. Corrige referencias operativas mutables que aún difieran a `GEN2-MARCADOR-ADOPCION-CLI-1`, especialmente §13 del estado. Conserva los encargos, firmas y notas históricos; agrega la cancelación/sustitución fechada en sus registros sin reescribir el pasado.
- D2, mesa «si vetado»: registra `veto:pisos-866` para los cuatro CALC originales. Re-verifica usos en main y distinguelos de #868. El veto alcanza a esos cuatro, no por inferencia a sus futuros sucesores, ni a los 20 C2 de los pilotos. Tampoco adopta los sucesores al medirlos.
- D3, propuesta de sucesión del ENCIG original y de dejar de contar, permanece pendiente si no hay firma posterior comprobable. Prepara una única fila de decisión con contexto y efecto derivado. No ejecutes la propuesta ni infieras que cambiar a SUPERADO altera el contador. A puede registrar técnicamente sucesores correctos; esa relación no es una firma de contador.

Completa las decisiones del trámite con sus verbatim leídos de la fuente:

| Objeto | Acción |
|---|---|
| NC-0274 | Firma ADR-531/FP-377 fechada 16/sep; conservar sellos y cerrar por propagación. |
| NC-0328 | Edad × dominio ENVIPE queda RESERVA-CONSUMIDA-SIN-PILOTO; cerrar sin habilitar otro piloto. |
| NC-0227 | #682/#719/#726/#728 como huérfanos aceptados; una excepción, sin encargos retrospectivos ficticios. |
| NC-0255 y NC-0256 | Demanda de medición conforme al universo vigente de relevo, priorizando CANDIDATO-GEN2. Conservar 153/12 como foto histórica del verbatim; derivar el estado actual aparte. |
| NC-0237 | Enmienda de diferimiento a F6; sigue abierta según el recibo actual. No cerrar por llamarla genéricamente parte de los siete cierres. |
| NC-0254 | Cerrar la NC por la decisión; RES-0043/0044 permanecen SIN-CANDIDATO con sucesor ENADID 2023. No confundir primera unión EDER con situación conyugal actual. |

Aplica RES-0043/0044 mediante la fuente/generador de relevo. Si no soporta la decisión, queda autorizada la corrección mínima de `tools/relevo_usos.py` o su fuente canónica que la haga persistente; genera la tabla y prueba esa consecuencia. No edites la tabla derivada manualmente ni abandones la subpieza por ausencia de una bandera concreta. Esta ampliación sustituye el PARO del recibo original para ese caso.

Enmienda NC-0024/0076/0239/0300 con el sucesor Claude y el alcance del diseño firmado. Permanecen abiertas hasta su producto real. No cierres esas cuatro porque #868 contenga un prototipo.

## B2 · Recibo completo del contrato y de las decisiones de pilotos

Recibe #865 por sus productos actuales, no por su descripción de PR posiblemente desactualizada. Completa `piloto-1:C2-tres-decisiones`, `piloto-1:FP-379-enmienda-D9` y `piloto-2:firma` con FP-379, su enmienda y FP-385, leídas del tablero y las fuentes firmadas. Reutiliza la adopción C2 ya registrada; registrar una firma no acredita consumo en main.

Compara §13 vigente con `seccion-13.md` y con P3 de `fuentes/01-CONTRATO-Y-TRAMITE.md`. Ese encargo autorizó explícitamente corregir: interpretación de status/contador, denominadores 97/117, distinción decisión/representación/consumo y afirmaciones incompatibles de escalas. **No caracterices esas correcciones como una decisión unilateral ni abras una FP para reautorizarlas.** Archiva el encargo 01 como procedencia de conversación externa; su incorporación actual no prueba que se archivara antes en el repo.

Lista cambios y omisiones por afirmación, con su respaldo. Completa el contenido sustantivo respaldado que haya quedado omitido; conserva el cuerpo histórico y L0. No restaures errores demostrados para conseguir literalidad ni copies el estado adjunto completo sobre el vigente. Solo una elección sustantiva realmente nueva y no resuelta se eleva a mesa con alternativas y consecuencia concreta.

Completa infraestructura de celdas-D/E1/replay/catálogo según archivos reales, huella de rutina ADR-539 y recibos pendientes de #851/#852/#853/#855, incluida la acción residual de mesa de #855. Primero busca ADR por objeto para evitar duplicados. Revisa NC-0305 por contrato y uso reales; no la cierres por una etiqueta de versión sola.

## B3 · Recibo de replay y defectos: cerrar por producto

Recibe #866 y los productos pertinentes de A. Por producto, registra script aislado, escritor de asientos, specs/medidores, resultados y vistas. Si presentas antes/después de status, ejecútalo sobre los commits correspondientes en worktrees de lectura o cita evidencia primaria ya disponible con el alcance exacto. Separa sellos físicos, filas publicadas, clasificación GEN2 y usos. No atribuyas causalidad entre escribir una vista y cambiar N_corridas_selladas sin demostrarla.

Revisa NC-0315, NC-0284/0285/0286/0287/0288 y NC-0329 una por una. Lee qué producto pedía cada fila; un asiento puede resolver replay y dejar otra parte abierta. No cierres en bloque.

**Prueba correcta de NC-0315:** `registro` sin escritura sirve para derivar, pero no ejecuta necesariamente el guardia de escritura. Inspecciona `_transiciones_replay` sobre esa proyección y comprueba `_para_si_pisa_replay` en memoria, o un equivalente de lectura que demuestre el mismo criterio. Después de la publicación de A, la regeneración ordinaria debe ser coherente. Solo entonces cierra con «remedio superado: asentar, no excluir». No pruebes el cierre escribiendo vistas desde B durante la fase paralela.

Conserva NC-0313 y el NO-REPRODUCE global de DIN con el alcance observado. Los puntos/IC C2 que reproducen se describen separadamente. Las limitaciones de acceso y ausencia de evidencia son estados diferentes.

Añade, sin duplicarla, la línea: «un veredicto de replay no se publica sin asiento en la fuente; verify que imprime y no asienta es media verificación».

Recibe los defectos de los pisos en un solo expediente. Los siete del brief son hechos a verificar; el impacto cuantitativo de BP1_20 inválido viene de A. P5_6 de 2021 ya tiene evidencia documental en la spec DIN: tarjeta de débito; cita su origen y la confirmación de FD de A. No lo presentes indefinidamente como pregunta sin contestar.

Comprueba también sucesión, fijación del código real y salida numérica por celda. Si A ya entrega el remedio, registra defecto histórico y corrección en el mismo recibo, cerrando la NC por producto; no crees una deuda abierta artificial ya resuelta. Los originales siguen vetados y preservados.

Conserva las seis semillas PARA-v2.15 del recibo original como observaciones breves, con respaldo o carácter de propuesta. No construyas nuevos guardias ni una reforma normativa en este encargo.

## B4 · Integración, derivados y entrega a Claude

Durante el paralelo, A es el único dueño de replay y las vistas corrida0. B trabaja sus fuentes y no escribe esos derivados. Puedes avanzar casi todo este recibo y dejar señaladas las comprobaciones pendientes del producto A.

Tras el merge de A, incorpora main, verifica mapa y resultados, termina los cierres dependientes y regenera demanda/registro/relevo afectados por tus decisiones con sus comandos. Esta fase final autoriza a B escribir los derivados ya entregados por A; nunca ambos escritores simultáneamente. No traigas las vistas de #868 ni uses OURS/THEIRS para sustituir la regeneración.

No reejecutes CALC ni modifiques `replay-evidencia.tsv`. Una transición nueva de replay que no estaba cubierta por A exige identificar su causa; no amplíes `--lote` por comodidad. Propagar un veto puede cambiar adopción/clasificación y eso debe distinguirse de un cambio de veredicto de replay.

Deja una nota de entrega a `GEN2-MARCADOR-REDISENO-1` con:
- SHA y mapa técnico de pisos publicados, exclusiones y reserva de contador que aún requiera firma.
- Decisiones de los 20 C2 y alcance de NC-0313.
- Veto a los cuatro antiguos y distinción entre medición disponible y consumo activo.
- #868, su SHA, archivos del prototipo y pruebas reportadas, todos como trabajo propuesto a revisar por Claude, sin declararlo válido o adoptado por herencia.
- Pendientes reales de identificación/crosswalk/reservas, sin convertir 97+20 en un denominador ni afirmar 117.

No selles el informe v1.1 como si ya existiera adopción segmentada en main. El informe final debe seguir al marcador y consumidor efectivos de Claude.

## Perímetro y parada

Dueño de: `forense/no-corrido.tsv`, `hallazgos.md`, `firmas-pendientes.tsv`, `data/corrida0/decisiones.tsv`, ADR/gobernanza/registro-rótulos, tablero, rutinas, infraestructura, estado vigente y citas operativas indispensables, fuente/generador/derivado de relevo para RES-0043/0044, nota de entrega y archivo propios. Demanda/vistas corrida0 solo en la integración final descrita.

No modifica CALC, specs numéricas, fuente de replay, `tools/corrida0.py`, motor, mapa de adopción, marcador, celdas-D, R, crosswalk, θ ni cron. No abre microdatos. «Si te encuentras escribiendo fuera de esta lista, PARA» aplica a la pieza no autorizada, sin deshacer lo ya resuelto.

Cierres y firmas se ejecutan con fecha real y verbatim/procedencia. Deriva ADR/FP/NC al cierre y renumera después de sincronizar. Preserva decisiones históricas; una corrección fechada no las reemplaza silenciosamente.

Ejecuta controles pertinentes de referencias/decisiones y del relevo si lo modificaste, más baseline al cierre. Corrige fallos introducidos; reporta heredados y WARN sin convertirlos en un proyecto de limpieza ni redefinir el baseline.

Entrega PR con HEAD remoto; tabla de objetos resueltos, condicionados y realmente pendientes de mesa; comandos y evidencia mínima; `NO-CORRIDO / RESERVAS` y `CONSUMIDO`. No crees RECIBO-CODEX-4 para trabajo absorbido aquí, no fusiones ni borres ramas por la antigua fórmula «cero ramas»: el cierre definitivo de Git sigue a la revisión humana.
