# ENCARGO 19 · GEN2-EVALUACION-SIN-FUGAS

ENTORNO: NUBE
RAMA: acto/gen2-evaluacion-sin-fugas
COMPUERTA: pruebas y diseño inmediatos; integrar 17 y el snapshot de 18 antes de evaluar un M renovado.
MODELOS: cero capturas nuevas en este encargo. MICRODATOS: ninguno para las fases técnicas.

## Resultado útil

Entregar un calculador sucesor con controles efectivos de contaminación, identidad, entradas y comparabilidad; separar reanálisis del panel conocido de una evaluación prospectiva que pueda sostener conclusiones nuevas. Debe impedir que una celda marcada contaminada se puntúe y que lecturas fuera del snapshot resuelto cambien la evaluación silenciosamente.

## Evidencia de partida

En main #694, `tools/calcula_f5_completa.py` acepta CIV-M-01 en U3 aun si `estado_firewall=CONTAMINADO-POR-OBJETIVO` o `identidad_confirmada=false`. Su wrapper TRIADA-0002 emite 27 resultados con `inputs={}` y lee 224 capturas+14 JSON R no enumerados como inputs directos. El snapshot publicado tiene sus 14 filas marcadas limpias; el contraejemplo no demuestra contaminación de todas ellas.

TRIADA-0002 quedó SIN-GANADOR-UNICO con U3=12/14. No confundir esa corrida con la anterior TRIADA-0001, U3=3/14. #698 analiza el panel conocido y propone 32 posiciones para cobertura documental; conservar su carácter exploratorio y su limitación de incertidumbre/familias.

## Fase 1 · Sucesión y contrato

Leer las specs F5 contrato-tríada v1.1/completa v1.0, ambos CALC TRIADA, el snapshot M, universo R y calculador. Registrar cuáles cláusulas de protección se conservan. Crear una sucesora; no editar `tools/calcula_f5_completa.py` ni ningún medidor fijado por hash sólo para que una corrida vieja parezca haber usado la nueva protección.

Fijar la conducta ante contaminación, falta de identidad, procedencia indeterminada, ausencia de punto, malformación y desajuste de estimando. Propuesta mecánica coherente con los contratos: no puntuar celda inelegible; conservarla en cobertura/exclusiones; si una violación compromete la comparación congelada, emitir NO-ADJUDICABLE-POR-CONTROL. No recortar después de observar errores para mejorar el ranking.

Verificar que los IDs del plan, marco, snapshot y R sean únicos y correspondan. No confiar en que `punto_M` sea numérico: requiere cadena y contrato válidos para el propósito. Estado desconocido nunca equivale a limpio. Reutilizar la clasificación de 17; no inferir independencia por encuesta/ola distinta o por no encontrar la cadena.

## Fase 2 · Fijar la clausura de inputs y consumirla

En el formato ya existente, enumerar o manifestar colectivamente las 224 capturas, 14 resultados R, snapshot M y código material. Cada miembro debe tener identidad y hash verificados. Identidad del prompt no sustituye hash de respuesta. Resolver todo una vez para la ejecución; el medidor usa bytes/rutas del snapshot resuelto, no rutas globales del árbol vivo ni valores cableados ignorando el contrato.

Los parámetros ejecutables viven en el contrato: bootstrap, semilla, delta, tolerancia, número de posiciones y selección. Evitar una segunda verdad hardcoded que diverja del YAML. Validar que el contrato consumido coincide con lo fijado. Mantener los valores históricos al construir el primer control sobre ese contrato, no elegir otros buscando significación.

Instrumentar las lecturas pertinentes o aislar el directorio de datos para verificar que el calculador sólo lee las dependencias resueltas. No convertir esto en un framework de sandbox universal: el riesgo observado está en esta ruta. Distinguir código/imports de datos; una allowlist del test debe atrapar un JSON R o respuesta extra y no fallar por imports normales.

## Fase 3 · Controles adversariales y reanálisis rotulado

Pruebas: celda contaminada no entra; identidad falsa/desconocida no entra; modificación de captura con mismo prompt se detecta; cambio de R o snapshot rompe identidad; faltante no se vuelve cero; duplicado/ID extraño se rechaza; copia/rename de objetivo mantiene origen; padre/derivado de R sigue reservado; parámetros de contrato se respetan; baseline íntegro reproduce las cifras donde los criterios sean iguales.

Aplicar las comprobaciones nuevas al material existente como **reanálisis diagnóstico**, nunca como pre-registro retrospectivo. Mostrar para cada celda el criterio, fuente, decisión de elegibilidad y efecto en cobertura. Si los metadatos actuales no permiten confirmar una cadena, decir indeterminado; no completar por suposición. Si cambian el conjunto puntuable o las cifras, dejar ambos resultados lado a lado con sus contratos; no reemplazar el veredicto histórico.

No proclamar que el nuevo análisis “rescata” un ganador: cualquier resultado de este panel ya conocido es diagnóstico tras la inspección. La falta de independencia y la diferencia de estimando no se resuelven estrechando un IC.

## Fase 4 · Dos productos científicos separados

**A. Uso documental.** Reutilizar la propuesta de #698 si sigue vigente: contextual versus fuente dirigida para DIN/TRA, con fuentes propias y trazables. El resultado prueba capacidad de extraer el dato permitido por el tratamiento. Si el dato objetivo está explícito en el documento, eso es recuperación/verificación documental, no generalización; no atribuir ventaja predictiva a copiarlo. Una tabla derivada del propio R no cuenta como fuente independiente nueva. No ejecutar las 32 posiciones bajo este encargo.

**B. Transferencia o generalización de M.** Diseñar un conjunto realmente reservado frente al ajuste/desarrollo del equipo, con unidad de partición apropiada por ola/familia/muestra y disponibilidad al corte. El panel de 14 ya visto no se renombra HOLDOUT. Crear otra conversación no borra la exposición. Reestimaciones del mismo dato, complementos, traducciones y etiquetas nuevas no crean independencia.

Para cada celda candidata, fijar la tarjeta común M/R: población, unidad, evento, códigos, ponderador/transformación, fecha de referencia, disponibilidad, función de R y criterio de comparación. No alimentar M con R ni con un antecesor materializado del mismo objetivo, directa o indirectamente. No resolver diferencias de unidad por cercanía numérica. Para uso documental exacto puede permitirse la fuente; para transferencia retenida debe mantenerse fuera del ajuste y del acceso del competidor según diseño.

Explicitar arquitectura/hipótesis aprendidas de Gen1, componentes modificados con los errores de F5, selección de modelos, incertidumbre de R, variación de L, dependencia de celdas y población a la que se quiere generalizar. Las réplicas L no son nuevas familias independientes. Diseñar la muestra según precisión/materialidad deseada, no simplemente porque 14 o 32 es un número disponible.

Fuentes metodológicas ya verificadas para el principio de separación: Cawley y Talbot (2010), https://www.jmlr.org/papers/v11/cawley10a.html. No prescribe aquí aplicar validación cruzada a todas las encuestas; adaptar la separación al estimando. La exposición del LLM en preentrenamiento no puede certificarse sólo desde este repo: declarar el límite y acreditar el contexto experimental controlado.

## Fase 5 · Decisión concreta y cierre

Entregar dos specs propuestas separadas, costes expresados en celdas/brazos/réplicas/llamadas y requisitos de fuente, criterio de éxito, parada y tratamiento de faltantes. Señalar qué evidencia todavía falta para ejecutar y qué queda autorizado por decisiones anteriores. No usar el plan Pro como permiso de API ni cambiar el competidor experimental al modelo que ejecuta Codex.

Mesa recibe la elección concreta de experimento y sus consecuencias. Mientras tanto, este encargo puede cerrar técnicamente con el calculador protegido, pruebas y reanálisis utilizable, sin abrir F6 ni nuevas llamadas.

## Perímetro y aceptación

Nuevos archivos de calculador/spec/medidor y pruebas; interfaz común de 17 mediante import; snapshot nuevo de 18 sólo tras integrarlo. No modificar las capturas o sellos históricos ni corregir parámetros de milpa desde R. El cierre técnico no necesita que 18 migre todas las reglas: basta con tener definidos los contratos y los casos de prueba; una evaluación posterior usa únicamente el snapshot elegible.

Aceptación: controles negativos cambian la elegibilidad/veredicto según regla previa; los miembros de inputs quedan fijados y son los realmente leídos; legado/same-data no se blanquea por nombre; comparabilidad por celda acreditada o exclusión con causa; propuesta de evaluación nueva con presupuesto y preguntas diferenciadas; historial intacto. Puede desarrollarse en paralelo con 17/18 en rutas nuevas, coordinando la API y sin duplicar el resolver.

## Contrato de ejecución, incluido para usar este archivo por separado

**Autoridad y lanzamiento.** La mesa pidió comprobar los candados GEN1→GEN2 y ajustar Gen2 aun si exige trabajo más robusto. Este encargo concreta esa solicitud; al entregarlo al ejecutor autoriza el perímetro descrito, commits, push y PR propio. El merge sigue siendo de mesa. No concede nuevas adopciones científicas, gasto de modelos ni una declaración de superioridad. Las decisiones previas válidas se conservan; una firma de contador no certifica independencia numérica.

**Arranque.** Lee `AGENTS.md`, este encargo completo, `.claude/commands/acto.md` y sólo las instrucciones sustantivas pertinentes. Reporta ruta absoluta, rama, HEAD y `git status --short`. Consulta main, PR y ramas por objeto para evitar duplicados; usa worktree propio. Archiva por el 0-bis vigente. El corte de preparación fue main #694, SHA `4816101e506f527d018dd2c47467a8b57bfbd487`, con #695–699 abiertos. Revalida únicamente cambios posteriores que afecten tu perímetro. Los ZIP de agosto son historia, no la base operativa.

**Integración.** Deriva ADR/NC/FP al cerrar, sin reservar números; quien integra después renumera y concilia sólo sus filas. Conserva filas ajenas por identidad y significado. Usa `tools/cierre_acto.py` según el procedimiento vigente, primero en seco; deja una sola ancla L0. No cambies `/despacha`, cierres PR ajenos ni borres worktrees. Actualiza las vistas globales sólo donde se autoriza expresamente; jamás reemplaces un TSV por una copia vieja. Los merges se serializan.

**Datos e historia.** Cloud trabaja código, documentos y agregados. Microdatos sólo en CAJA, con raíces y hashes del manifiesto. No reescribir specs, scripts, snapshots, capturas, resultados ni sellos congelados: usa sucesoras y enmiendas de alcance. Un control histórico no selecciona receta, filtro, ponderador ni variante por cercanía. Recalcular sobre la misma muestra puede ser trabajo GEN2, pero no es automáticamente evidencia independiente. Procedencia, reproducción, validación, adopción y uso en evaluación son estados distintos.

**Perímetro administrativo.** Encargo archivado, nota de cierre, filas directamente afectadas de decisiones/no-corrido/firmas/cola y cascada existente en gobernanza/estado/rótulos. No crear otra plataforma de gobernanza, base de datos o coordinador de tareas. Automatiza sólo defectos materiales reproducidos y con mantenimiento menor que el coste de repetición.

**Pruebas y cierre.** Pruebas materiales dirigidas, baseline requerido y diff final. No reparar fallos históricos ajenos para obtener una suite cosméticamente verde. Las pruebas adversariales adjuntas documentan defectos: después del arreglo sus salidas deberán cambiar según el contrato, no preservarse como oráculo del comportamiento correcto. Ninguna prueba escribe sobre el árbol científico real. Entrega `obligación | evidencia | consumidor/alcance | cierre o residual` y PR/HEAD. Una reserva mixta conserva su residual. No cerrar por nombre coincidente, sello o firma de contador solamente.

Continúa entre fases autorizadas. Ante una decisión científica nueva, prepara opciones concretas y termina las fases independientes; no conviertas una recomendación en firma. Cero llamadas nuevas a modelos y cero envío de solicitudes a terceros en estos tres encargos.


**Actualización comprobada al cierre:** main avanzó a `a63fd4ccc40204cf5215d466a593b4e1491bdda6` por #699 y #696. No cambió el código objeto de las sondas. 09 ya está fusionado: partir de sus vistas y no repetir su publicación. 14–16 están encolados por #699. Esta actualización prevalece sobre referencias de coordinación redactadas al corte inicial.

## NO-CORRIDO / RESERVAS

- **qué:** `Fase 4 · A. Uso documental — No ejecutar las 32 posiciones bajo este encargo.` · **por qué:** `DECISIÓN-DE-MESA-PENDIENTE` · **impacto:** no se ejecutan 32 llamadas ni cambia `NC-0152`; la spec sólo deja congelables fuentes, éxito y parada · **sucesor:** `FP-373`.
- **qué:** `Fase 4 · B. Transferencia o generalización de M — Diseñar un conjunto realmente reservado.` · **por qué:** `DECISIÓN-DE-MESA-PENDIENTE` · **impacto:** no se ejecutan piloto/confirmación, no se abre F6 y no cambia ningún contador o adopción · **sucesor:** `FP-374`.
- **qué:** `COMPUERTA: integrar 17 y el snapshot de 18 antes de evaluar un M renovado.` · **por qué:** `DECISIÓN-DE-MESA-PENDIENTE` · **impacto:** el reanálisis usa sólo el snapshot histórico y no emite veredicto sobre un M renovado · **sucesor:** `FP-374`.

## CONSUMIDO

Consumido el 11/sep/2026 en la rama
`acto/gen2-evaluacion-sin-fugas`, PR #713. El reanálisis protegido quedó
sellado como `CALC-F5-REANALISIS-0001`: 245 inputs directos coinciden,
`U3=0` y veredicto `NO-ADJUDICABLE-POR-CONTROL`; el resultado histórico
permanece intacto. Los actos 17 y 18 se integraron por sus interfaces reales,
sin presentar el snapshot sucesor como evaluación retenida. `FP-373/374` y
`NC-0159/0160/0161` conservan las decisiones y ejecuciones pendientes.
`ADR-473`; contador cero. El PR queda abierto y el ejecutor no realizó merge.
