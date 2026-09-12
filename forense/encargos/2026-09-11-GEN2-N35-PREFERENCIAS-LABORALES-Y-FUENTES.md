# 42 · GEN2 · N35: preferencias laborales, medición y fuentes nuevas

ENTORNO: CAJA — Codex CLI Windows/WSL  
RAMA: `acto/gen2-n35-preferencias-laborales-fuentes`  
OBJETO NUEVO: `CALC-MOTRAL2015-VALORACION-SS-0001` (comprobar identidad libre o trabajo ya iniciado).  
PRODUCTO: medir la valoración declarada de seguridad social con MOTRAL 2015, corregir el descarte excesivo del registro y obtener evidencia pública del experimento mexicano de elección laboral.

## Contrato autónomo de ejecución

Repositorio: `Josanoforo/Modelado-Mexicano`. Preparado para Jonás el 12/sep/2026 contra `main=6e634aaaa3dec6ed536bae1ef142a4f7ff56cfae` (#741, paquete 39/40 encolado). 39 y 40 están corriendo. Este archivo se puede entregar solo a Codex CLI en CAJA Windows/WSL.

Al despacharlo, Jonás autoriza abrir y congelar la spec de los estimandos descriptivos definidos en este encargo, adquisición pública pertinente, implementación, ejecución completa con datos reales, registro, commits, push y PR propio. Esa instrucción resuelve la apertura de spec para este objeto; no volver a solicitarla porque un antecedente dijera «mesa decide si abre especificación». No autoriza adopción al motor, causalidad nueva, cambio de tiers, experimento F5, gasto de proveedor, compras o contacto externo. Las fusiones quedan con Jonás.

Lee `AGENTS.md`, el encargo entero y el procedimiento pertinente de `.claude/commands/acto.md`. Reporta worktree absoluto, rama, SHA y estado; usa una tarea por worktree/rama/PR y archiva por el 0-bis vigente. Revisa sólo entregas posteriores del mismo objeto y ejecuta el residual si ya hubo avance. La coordinación conocida de las dos ramas de 39 queda con su sesión; no investigarla ni intervenirla.

Comprueba los IDs de entrada con el resolvedor y manifiesto. Existen las raíces lógicas `data_raw` y `descargas_mx`; no todas las fuentes viven bajo la misma ruta. El corpus compartido de `data_raw` está en `/home/pc0/mm-corpus/raw`. Resuelve montaje, permisos de lectura y dependencias antes de declarar ausencia. Recupera únicamente objetos faltantes o documentos nuevos pertinentes; no rehagas las olas de descarga. Bytes y microdatos permanecen fuera de Git; publica agregados, código e identidades según la vía vigente.

Congela fuente/versión, población, unidad, codificación, pesos, filtros, faltantes, transformaciones y salidas antes del cálculo. Los códigos provienen del documento exacto de cada edición. No ajustes definiciones para recuperar una cifra histórica. Separa estimación nueva, reproducción de un cálculo existente y transcripción de una tabla publicada. No vuelvas a sellar un resultado viejo como medición nueva.

Continúa todas las fases sin pedir otro encargo. Cuando falte una elección científica fuera del contrato, completa primero las partes independientes y entrega opciones concretas. Un fallo de transporte o acceso requiere uno o dos intentos razonables, alternativa directa y residual con objeto/acción; no inventes un dato ni detengas el resto. No enviar solicitudes ni aceptar compromisos de acceso en nombre de Jonás.

Perímetro excluido de los tres encargos: `tools/adq_*`, `tools/adquiere_*`, `data/adq-*`, Task Scheduler, configuración de SONDA, extractor/overlay/buscador de 39, consumidores y emisor de 40, capturas y congelados F5. Reutiliza lectores existentes sin modificarlos cuando sea posible. Cada frente escribe su propio medidor/spec/resultados; los cambios indispensables a un helper compartido se coordinan por archivo y se mantienen mínimos.

Registros y cierres se integran por clave con los escritores canónicos. 40 conserva la conciliación de NC-0165, la proyección general y el cierre global de NC-0164; estos frentes le entregan evidencia consumible, no sobrescriben esa NC ni la cierran por producir una capa parcial. Banxico y SHED actualizan únicamente su propia relación N34. N35 actualiza su relación específica y preserva sus reservas. Las altas de manifiesto/cola y la cascada se concilian sobre el árbol combinado, sin reemplazar tablas enteras.

Finaliza spec → ejecución → CALC/RESULT y sello cuando corresponda → comprobación material → agregados y ficha de uso → registros propios → nota/cierre existente → PR. Propaga contador científico sólo con la autoridad de objeto exigida por el procedimiento; no confundir autorización de cálculo con adopción, ni contar descargas como medición. Pruebas dirigidas y gates requeridos, comparando baseline; no limpiar fallos heredados ni añadir totales rígidos. La entrega no termina en fixtures, diagnóstico o propuesta cuando puede completar la ejecución autorizada.

## Hallazgo material y fuentes ya verificadas

N35 corresponde a `trabajo.prestaciones.formalidad_pesa_mas_que_salario` / R2.3. El registro describe MOTRAL 2012/2015 como carente de preferencia; algunas notas trasladan el examen de la tabla de empleos 2012 a 2015. Se debe corregir únicamente lo que la evidencia contradiga.

El [cuestionario oficial MOTRAL 2015, página 1](https://www.inegi.org.mx/contenidos/programas/motral/2015/doc/motral2015_cuestionario.pdf), sí contiene pregunta 17 sobre preferencia por empleo con seguridad social aun pagando aportaciones y pregunta 16 sobre orden de valoración de cinco prestaciones. Es una capa pertinente que no equivale a comparar dos salarios explícitos. Las preguntas 14–15 aportan percepción de acceso, no preferencia monetaria.

El [IZA DP 14278](https://docs.iza.org/dp14278.pdf), sección 2, documenta el uso de MOTRAL 2015 y su enlace con ENOE de segundo trimestre de 2015. Sirve de mapa del análisis, no de número objetivo que deba recuperarse cambiando filtros.

Otra pista: la [página del autor](https://sites.google.com/site/robertduvalhernandez/research) identifica un experimento de elección de empleo en México de Campos-Vázquez, Duval-Hernández, Juárez y García-Guzmán. La [sesión EEA-ESEM 2026](https://eea-esem-congresses.org/sessions/migration-and-informality) ofrece enlaces «Read paper» y «View». Se verificó esa página; no se lograron recuperar los binarios desde este entorno y no se acreditó un microdato público. El estudio brasileño de título parecido es otro objeto y no se acepta como sustituto mexicano.

La nueva evidencia abre trabajo concreto; no justifica repetir las búsquedas generales de ENIGH/ENOE/MOTRAL ya hechas ni declarar resuelta la frase «pesan más que el salario».

## Fase 1 · Leer el objeto correcto y corregir el alcance

Localiza por ID `motral2015_cuestionario` y `motral2015_bases_datos_dbf`, raíz `descargas_mx`, rutas `UNIVERSO-2026-09/MOTRAL/`. No deduzcas su estructura de `motral2012_empleos`. Conserva los bytes históricos y examina todos los miembros del ZIP 2015 para localizar la tabla de persona seleccionada/perspectiva donde se guardan preguntas 16 y 17.

Confirma variable DBF exacta, tipo, codificación y enlace al reactivo, llaves de persona, ponderador, saltos, rangos y faltantes. `P16`/`P17` nombran aquí preguntas del instrumento: no se garantiza que sean los nombres exactos de columna. El desfase es precisamente lo que debes resolver con diccionario y metadatos.

Recupera descriptor oficial sólo si no está disponible. El microdato ya registrado tiene URL exacta en manifiesto; no descargarlo de nuevo por no verlo en `data/raw`. Si hay otro contenido bajo la URL actual, registra nueva versión, no reemplaces el hash previo.

Emite una corrección fechada y fuente-específica del «sin preferencia» sólo después de esa comprobación. Conserva `EXISTE-NO-SATISFACE` para la comparación salarial estricta si continúa sin estar identificada. No conviertas el error de alcance en una auditoría de todas las fuentes o notas de agosto.

## Fase 2 · Congelar y ejecutar la medición disponible

Este encargo autoriza los siguientes estimandos descriptivos, una vez acreditada la correspondencia del microdato:

- Proporción ponderada de respuesta afirmativa a la pregunta 17 en la población elegible del módulo con respuesta válida.
- Distribución de la prestación elegida en primer lugar en la pregunta 16; las cinco opciones se conservan separadas. No promedies rangos como utilidades cardinales ni cuentes cinco filas de rango como cinco personas.
- Ambos resultados por sexo y dos grupos de edad predeclarados, 18–34 y 35–54, sólo dentro de la población elegible acreditada. Si la documentación oficial fija otro universo, usa el oficial y adapta únicamente los cortes que no tengan población; registra el cambio antes de calcular.
- Entre población ocupada enlazada con ENOE 2015-T2, respuesta a pregunta 17 por cobertura de seguridad social del empleo actual. El cruce es descriptivo; no clasifica automáticamente informalidad voluntaria/involuntaria ni mide causalidad.

El resultado del módulo completo puede correr primero; el cruce ENOE se completa en la misma sesión si los objetos/llaves son accesibles. Antes de unir, comprueba llaves documentadas, tipo y cardinalidad, pérdidas de enlace y peso apropiado. Un identificador que se repite en varios empleos no autoriza un join muchos-a-muchos. No uses el último empleo de la trayectoria como empleo actual por intuición.

Reporta numerador, denominador, masa, n, filtros y desconocidos. Para la prioridad de prestaciones, exige un primer lugar único válido y cuantifica rankings incompletos o inconsistentes; no decidas empates por orden de columnas. EE/IC sólo con diseño acreditado; conservar puntos descriptivos es válido si faltan insumos de varianza.

Crea `CALC-MOTRAL2015-VALORACION-SS-0001` y salidas propias, por ejemplo `data/motral2015-valoracion-ss/`. Congela la spec antes de observar comparaciones. Comprueba independientemente un cociente, el manejo de ranking y la cardinalidad del cruce. No entregues únicamente un inventario de variables.

## Fase 3 · Adquisición dirigida del experimento mexicano

Recupera paper y presentación desde los enlaces de la sesión EEA-ESEM; si la ruta falla, prueba la página de los autores o repositorio institucional correspondiente. Conserva título, autores, fecha/versión, URL y hash. El enlace publicado no se registra como archivo obtenido hasta recibir un documento válido.

Busca sólo el cuestionario, apéndice de diseño, código y datos de replicación de ese mismo estudio: páginas de autores/instituciones, repositorio enlazado y referencias exactas. La búsqueda inicial se limita a ese objeto y sus versiones; no convertirla en bibliografía universal de informalidad. No aceptar términos con compromisos nuevos ni contactar autores.

Extrae del material accesible una ficha de compatibilidad: población/muestra, año, atributos y niveles de salario/prestación, elección observada, aleatorización y resultados publicados pertinentes. Si sólo existen tablas o gráficos, conserva su carácter publicado y precisión; no inventes microdatos ni errores estándar. Una WTP estimada para un cambio concreto de prestación no significa preferencia universal frente a cualquier salario.

Si aparece un paquete reproducible público, adquiere y abre sus archivos; reproduce únicamente las tablas pertinentes al contrato publicado usando código original, documentando dependencias y límites. Esta réplica no autoriza diseñar otra especificación para recuperar un signo ni adoptar su parámetro en México general. Si no hay bytes públicos, deja el impedimento y borrador de petición concreta como residual, sin enviarlo. Completa entretanto toda la medición MOTRAL.

## Fase 4 · Registro, entrega y puente a 40

La relación N35 actual es `REL-31a794c27eca54d8d773df15`, objeto `OE-c78f1d5cea82d64e082219c0`. Actualiza por clave el alcance respaldado y enlaza la nueva medición. En manifiesto conserva identidad/hashes y corrige la nota de uso 2015 con enmienda; no reescribas la evidencia histórica 2012. Una fuente nueva del experimento recibe identidad propia, sin duplicar N35 ni apropiarse del derivador de 40.

39 conserva el índice general. Entrega correspondencias documentales y localizadores para que las incorpore si corresponde, sin editar su overlay o extractor.

Entrega a 40: CALC/RESULT exactos, uso descriptivo permitido, lo que cambió en la evidencia, qué sigue faltando para la comparación salarial y una opción concreta de regla futura. No sustituyas R2.3 ni su tier. Las decisiones de nueva definición/adopción siguen con mesa.

Aceptación: preguntas/localizadores y columnas acreditados, cálculo MOTRAL real, cruce ENOE ejecutado o residual exacto de acceso, fuentes nuevas realmente obtenidas o barrera verificada por objeto, corrección fuente-específica y PR. La adquisición va dentro del encargo; no cerrar con «hay que descargar» cuando el archivo público puede recuperarse.

## Prompt de lanzamiento

> Ejecuta completo el encargo 42 en CAJA y worktree propio. Autorizo abrir/congelar la spec descriptiva de MOTRAL 2015, medir preguntas 16/17 y sus cortes definidos, completar el cruce ENOE viable y adquirir paper/apéndices/replicación pública del experimento mexicano identificado. Corrige sólo el descarte excesivo acreditado: valorar seguridad social no prueba todavía que pese más que cualquier salario. No uses el MOTRAL 2012 como sustituto del 2015. 39 posee índice y 40 demanda/motor; entrega evidencia para ambos sin pisarlos. Continúa hasta resultados, adquisiciones viables y PR. El merge queda conmigo.

## NO-CORRIDO / RESERVAS

- **Qué — `EXPERIMENTO-MEXICANO-PAQUETE-REPRODUCIBLE`:** obtener Appendix
  C/cuestionario, asignación de los 64 bloques, microdato anonimizado y código
  que reproduzca las tablas 2–5 de *Do Workers Value Formal Jobs?*
- **Por qué — `NO-VERIFICABLE-AQUÍ`:** se adquirieron paper y presentación
  públicos del estudio exacto, pero el PDF termina en Appendix B y no se
  localizó paquete público en la sesión EEA-ESEM, páginas de autores, OSF,
  Dataverse, Zenodo o GitHub.
- **Impacto:** la WTP de 0.240 por seguridad social (EE 0.023) queda como
  transcripción publicada, no reproducción ni parámetro adoptable; MOTRAL 2015
  sí se mide independientemente.
- **Sucesor — `NC-0166`:** titular de N35 solicita —sin envío automático—
  Appendix C, bloques, microdato y código; congela una spec sucesora y reproduce
  antes de proponer una regla DCE.

## CONSUMIDO

Ejecutado entre el 11 y 12/sep/2026 por
`ACTO GEN2-N35-PREFERENCIAS-LABORALES-FUENTES` en el worktree
`/home/pc0/mm-gen2-n35-preferencias-laborales-fuentes`, rama
`acto/gen2-n35-preferencias-laborales-fuentes`; entrega revisable en **PR
#747** y gobernanza `ADR-492`.

La spec quedó congelada en `cca8297`; la ejecución real y sus agregados en
`5158580`; el registro N35 y puente descriptivo en `54ee092`; cierre inicial en
`461e626` e integración del `main` que contiene #744 en `d323d92`. El cálculo
publica 32 estimandos y 10 diagnósticos: 42/42 RESULT y 6/6 inputs
`REPRODUCE/IDENTICO`, con control independiente coincidente. P17 total es
82.3626705331% (n=5,704), P16 conserva sus cinco primeras prioridades y el
cruce ENOE tiene 6,564 coincidencias, 436 pérdidas y cero duplicados.

Se adquirieron y registraron paper y presentación del DCE mexicano. Su WTP
0.240 (EE 0.023) sigue siendo transcripción, no réplica ni adopción; `NC-0166`
conserva el paquete público no localizado. R2.3 permanece
`EXISTE-NO-SATISFACE`, sin cambio de motor o tier. Verificación final antes del
commit de consumo: prueba dirigida y control independiente en OK, baseline del
curador sin errores, `corrida0 verify` en REPRODUCE/IDENTICO y
`tests/check.py --baseline` VERDE con los 3 FAIL heredados y cero nuevos.
