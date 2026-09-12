# 39 · GEN2 · Reactivos pendientes y búsqueda útil para SONDA

ENTORNO: CAJA — Codex CLI en Windows/WSL
RAMA PROPUESTA: `acto/gen2-reactivos-residuales-busqueda-util`
RESULTADO: recuperar texto documental pendiente, publicarlo en el índice vigente y demostrar búsquedas que antes fallaban por falta de metadatos.

## Autoridad, corte y ejecución

Encargo preparado para Jonás el 12 de septiembre de 2026. Repositorio: `Josanoforo/Modelado-Mexicano`. Corte actualizado y verificado: `main=015407b9a59359481285bf343ad561dfd7026e8b`; #737 y #739 fusionados. #738, #740 y #728 también están fusionados; el merge de #728 no sustituye la autorización científica de F5. GitHub sólo muestra la rama de censo #727 además de main; no acredita si hay sesiones locales sin publicar. Este archivo sucede al texto 39 incluido en el transfer, conservando su alcance.

Al despachar este documento, Jonás autoriza implementación, recuperación de documentación pública pertinente, ejecución sobre el corpus, commits, push y PR propio. Continúa todas las fases sin solicitar otro encargo. La fusión queda con Jonás. No autoriza nuevas adopciones, compra, contacto externo ni cambios al experimento F5.

Lee `AGENTS.md`, este encargo completo y el procedimiento pertinente de `.claude/commands/acto.md`; reporta worktree absoluto, rama, SHA y estado. Archiva el encargo mediante el 0-bis vigente y completa la cadena de cierre existente, sin crear registros paralelos. Actualiza únicamente antecedentes pertinentes desde main y PR abiertos. Si existe una entrega posterior equivalente, consúmela y ejecuta el residual real; no repitas #737. Los procesos locales de otras sesiones no se deducen de GitHub: revisa las asignaciones disponibles antes de escribir.

## Por qué este trabajo puede correr ahora

#739 reconstruye demanda, corrige selección/reanudación y protege suficiencia→motor. Este encargo mejora la recuperación documental que consume SONDA. Usa las interfaces de #737 y #739 ya fusionadas. Puede avanzar en paralelo con el encargo 40 de NC-0165: 39 posee extracción e índice; 40 posee conciliación, contratos y ruteo científico. Ninguno necesita esperar al otro para comenzar.

La ausencia de un resultado en un índice con poco texto no acredita ausencia de una variable. El cierre de #737 cuantifica este residual dentro del lote prioritario:

| Familia | Filas históricas | Con texto en overlay | Pendientes |
|---|---:|---:|---:|
| ENVIPE | 31,140 | 1,248 | 29,892 |
| ENNViH | 17,181 | 17,176 | 5 |
| ENCUCI | 458 | 2 | 456 |
| ENIF | 6,747 | 3,572 | 3,175 |
| ENSAFI | 369 | 369 | 0 |
| Total | 55,895 | 22,367 | 33,528 |

Son conteos publicados, no cifras objetivo para fabricar cobertura. Reproduce el corte pertinente y distingue filas físicas, identidades lógicas, etiquetas y preguntas completas. Las 823 pendientes DBF de NC-0100 están incluidas en ENVIPE; no se suman otra vez. Los 81 grupos históricamente ciegos fuera de cobertura no equivalen al lote de cinco familias.

## Perímetro y concurrencia

Reutiliza principalmente:

- `tools/actualiza_reactivos_contexto.py` y `tools/busca_reactivos.py`.
- `data/reactivos-contexto-fuentes-v1_0.tsv`, `data/reactivos-contexto-verificados-v1_0.tsv` y el overlay vigente.
- Los índices históricos como entrada inmutable, con sus identidades por posición.
- `tests/test_reactivos_contexto.py` y las pruebas existentes del buscador.
- El cierre `forense/notas/2026-09-11-GEN2-REACTIVOS-CON-TEXTO-Y-BUSQUEDA-cierre.md` y el encargo 34 archivado bajo `forense/encargos/cola/2026-09-12-GEN2-POST-726/`.

No modificar `tools/adq_*`, `tools/adquiere_*`, `data/adq-*`, las instrucciones de SONDA/adquisición, Task Scheduler, el clon `/home/pc0/mm-adq`, `consulta_gen2`, el motor ni paquetes F5. Esos archivos y comportamientos quedan fuera de 39; el encargo 40 puede ajustar demanda/contratos/ruteo dentro de su propio perímetro. Tampoco lanzar el cron desde esta sesión.

Usa worktree propio y el corpus compartido como entrada mediante el resolvedor/montaje existente. Temporales y caché en destino propio. Para documentos públicos nuevos, registra identidad y procedencia mediante el procedimiento existente; no reemplaces bytes bajo un hash histórico. Las altas de manifiesto y los cambios de NC-0100/NC-0136 se concilian por clave sobre el árbol combinado. No restaure tablas enteras de tu rama para resolver concurrencia.

## Fase 1 · Identificar la causa de cada grupo pendiente

Reproduce la cobertura del lote con el extractor vigente. Agrupa residuales por instrumento, ola, tabla/miembro y motivo: documento ausente, extractor incompleto, correspondencia ambigua, etiqueta técnica, pregunta no localizada u otra causa acreditada.

Orden de trabajo: ENCUCI → ENVIPE DBF 2012/2013/2015 → ENIF residual → resto de ENVIPE → cinco residuales ENNViH. ENSAFI y los textos ya recuperados sirven de control de conservación. Prioriza reparaciones reutilizables por familia de formatos frente a cientos de correcciones manuales.

Lee el cuestionario/diccionario para establecer correspondencias. No abras valores de personas para obtener etiquetas. Las fuentes nativas que permiten leer sólo metadatos pueden usarse con ese modo. El resultado de esta fase debe conducir inmediatamente a extracción real, no ser una entrega independiente de inventario.

## Fase 2 · Recuperar documentación y reparar extracción

Busca primero documentos y metadatos existentes del objeto exacto. Si falta el diccionario/cuestionario, localiza y descarga la publicación oficial correspondiente a esa ola y tabla; conserva URL, fecha, hash y localizador. No descargues de nuevo todo el microdato si basta su descriptor.

Extiende el extractor existente en los formatos que causen el residual: tablas PDF multipágina, XLS/XLSX, diccionarios DBF o etiquetas nativas, según lo encontrado. OCR local sólo cuando sea necesario sobre documentación pública; verifica texto y correspondencia antes de publicarlo como literal.

Conserva separados:

- pregunta literal, etiqueta de variable y descripción administrativa;
- categorías de respuesta, universo/filtro y pregunta;
- contexto editorial para búsqueda y texto atribuido a la fuente.

No propagues texto entre olas sólo porque coincide el código. Una correspondencia debe incluir instrumento, ola, tabla/miembro y variable. Las ambigüedades permanecen explícitas, con acción específica. Para llaves o ponderadores sin pregunta, publica la etiqueta acreditada como tal; no inventes un reactivo ni ocultes esas filas del denominador para mejorar el porcentaje.

## Fase 3 · Publicar el índice y conectarlo al buscador

Genera la salida en destino propio y aplica la política vigente de sucesión. Conserva los índices históricos, su orden y sus citas. Si hay que crear una versión sucesora del overlay, enlázala desde la ruta vigente de búsqueda y conserva el mapa de identidades.

Mantén procesamiento incremental por objeto, caché por hash y versión del extractor, y publicación atómica. Conserva los textos acreditados que no pertenezcan al lote actual. La actualización debe poder ejecutarse desde otra sesión mediante un comando exacto y las dependencias documentadas.

No construyas otro servicio de indexación ni otra tarea periódica. El cron podrá consumir el buscador actualizado por su mecanismo de despliegue, sin crear un despliegue o un servicio adicional en este encargo.

## Fase 4 · Demostrar utilidad sobre documentos reales

Entrega comparaciones antes/después para consultas respaldadas por la documentación inspeccionada:

- ENCUCI: al menos un reactivo pertinente distinto de los dos ya recuperados por #737.
- ENVIPE DBF: identidad de víctima/evento, denuncia o razón de no denuncia en las olas documentadas, según sus reactivos reales.
- ENIF: ahorro, producto financiero o canal, distinguiendo claramente el constructo encontrado del solicitado.

Reutiliza como regresión las consultas de tandas ENNViH y atraso/afrontamiento ENSAFI. No basta aumentar hits de palabras generales: muestra variable exacta, tipo de texto, documento/hoja/página y por qué antes no podía recuperarse. Una mejora del buscador no equivale a resolver NC-0126, NC-0122 ni otra necesidad científica.

Verifica específicamente una variable repetida entre tablas/olas para prevenir una asignación falsa; una segunda ejecución sin cambios debe reutilizar caché y conservar el contenido. Ejecuta las pruebas dirigidas pertinentes, sin añadir tests de totales rígidos que haya que cambiar con cada lote legítimo.

## Fase 5 · Cierre completo del perímetro

Entrega el índice utilizable, el extractor corregido, el buscador conectado y las demostraciones reales en un PR. El informe debe explicar cada grupo residual del lote: resuelto, texto técnico acreditado, documento realmente no disponible o correspondencia aún no acreditada. Las partes bloqueadas necesitan objeto, evidencia del impedimento y siguiente acción; no basta «queda para otra sesión».

No se exige inventar texto ni obtener cobertura imposible. Sí se exige recorrer los grupos del lote y completar las reparaciones viables, aprovechando documentos ya disponibles. No detenerse tras los primeros ejemplos si la misma corrección permite resolver el resto.

Actualiza sólo el residual pertinente de NC-0100 y NC-0136 con los escritores vigentes. Cierra NC-0100 únicamente si su conjunto DBF queda acreditado. NC-0136 conserva el alcance externo al lote y sus obligaciones restantes. Registra el cierre administrativo aplicable sin adjudicar adopciones ni contador científico.

Para consumo por 40 y por el servicio fusionado en #739, incluye en la nota: SHA del extractor/índice, comando de actualización, identidades ganadas, límites del negativo de búsqueda y residual pendiente. No edites configuración de adquisición ni recrees una NC existente. Al sincronizar, conserva los contratos y la información de 40; sólo 39 modifica el residual sustantivo de NC-0100/NC-0136. Los cambios compartidos se integran por clave con los escritores canónicos. Si 40 aún no consume esta versión, deja comando e identidad exactos para que lo haga, sin convertir su espera en bloqueo de tu PR.

## Criterios de aceptación

1. El incremento proviene de metadatos/documentos verificables y tiene correspondencia exacta por objeto.
2. El buscador operativo recupera el nuevo texto, no sólo un archivo auxiliar desconectado.
3. Las citas históricas, fuentes previas y trabajo concurrente se conservan.
4. Cada grupo pendiente del lote tiene desenlace y acción, sin confundir cobertura textual con suficiencia científica.
5. Hay ejecución real, salida reproducible y PR; ninguna modificación al cron, motor o F5.

## Prompt de lanzamiento

> Ejecuta íntegramente el encargo 39 adjunto en un worktree propio. Autorizo las fases, recuperación de documentación pública pertinente, implementación, ejecución real, commits, push y PR; el merge queda conmigo. #739 ya está fusionado. El encargo 40 lleva en paralelo la conciliación de NC-0165, demanda y ruteo; coordina sólo los registros compartidos. Tu responsabilidad es reducir los puntos ciegos documentales del lote prioritario de #737 y dejar el buscador consumiendo la mejora. Continúa entre fases sin pedir otro encargo; no cierres sólo con diagnóstico, fixtures o ejemplos aislados si puedes completar el resto del lote.

## NO-CORRIDO / RESERVAS

- `NC-0100` — `DIFERIDO-A:NC-0100`: quedan 32 identidades DBF por acreditar con correspondencia exacta: nueve de ENVIPE 2013 y 23 de 2015. No copiar texto por nombre entre olas ni inventar las cinco preguntas no localizadas en el descriptor oficial.
- `NC-0136` — `DIFERIDO-A:NC-0136`: quedan 12,875 filas del lote prioritario, clasificadas por causa en el residual v1.1, y 81 grupos históricamente ciegos fuera de este lote. Un negativo del índice no demuestra ausencia de variable.
- El encargo 40 y su rama no fueron incorporados: el solapamiento accidental fue entre dos sesiones del encargo 39 y quedó consolidado en PR #742.

## CONSUMIDO

Consumido por PR #742. La implementación e índice de ambas sesiones accidentales del encargo 39 quedaron consolidados en `de1d2ed`; el cierre administrativo, NC-0100/NC-0136, ADR-490, rótulo e infraestructura quedaron en `54137a0`. La fusión permanece reservada a Jonás.
