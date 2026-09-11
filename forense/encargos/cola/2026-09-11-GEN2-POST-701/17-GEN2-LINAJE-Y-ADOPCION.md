# ENCARGO 17 · GEN2-LINAJE-Y-ADOPCION

ENTORNO: NUBE
RAMA: acto/gen2-linaje-adopcion
COMPUERTA: no científica; trabajar desde main actual y coordinar las vistas con 09/#696.
MODELOS: cero llamadas. MICRODATOS: ninguno.

## Resultado útil

Cerrar la entrada demostrada que permite citar como GEN2 un RESULT numéricamente heredado y corregir la clasificación por ruta. Entregar una única resolución reutilizable por registro, T35 y el emisor, conservando las decisiones de contador ya firmadas. No crear un motor de grafos general ni exigir migrar todo el repo para que una medición nueva pueda avanzar.

## Premisas verificadas

En main #694, `_inputs_legacy_de` permite `./milpa/tramite.yaml`; `_propaga_envuelto` no propaga un padre LEGACY que no tenga `envuelto_legacy=SI`; TRIADA-0002 pierde la marca al pasar por snapshot; ocho CALC-R son marcados por la ruta de un archivo de código. T35 acepta un fixture GEN2/cuenta=NO/envuelto=SI adoptado por un consumidor GEN2. Adjuntos: `PRUEBAS-CANDADOS-GEN2.py` y su JSON; si no se adjuntan, estos casos están descritos aquí y pueden reconstruirse con los fixtures de `tests/test_corrida0.py`.

No asumir que los ocho R están libres de toda influencia por ser código: inspeccionar qué funciones ejecutan y qué leen. No asumir que una firma de contador vuelve apto todo resultado para cualquier uso.

## Fase 1 · Contrato pequeño y casos reales

Leer plan GEN2 §§1/2/5/7, regla E.1 y su adenda T9, `_lee_oferta`, `_inputs_legacy_de`, `_propaga_envuelto`, `_cuenta_gen2_resuelto`, `_filas_registro`, T35 y decisiones pertinentes. Levantar únicamente estos casos: un smoke, un wrapper M, un árbitro R recién medido con código histórico, un resultado adoptado genuino y las dos tríadas.

Definir en las estructuras existentes los ejes mínimos: generación administrativa/contador; origen numérico; función de cada dependencia; aptitud para el uso pedido. Valores propuestos: origen nuevo, heredado, mixto o indeterminado; dependencia dato/código/metadato/control histórico. Son nombres de implementación, no nuevos tiers científicos.

Resolver por RESULT y por uso cuando un CALC mezcla resultados distintos: un análisis nuevo de un baseline antiguo puede contar como trabajo, sin que sus puntos heredados se conviertan en parámetros recién medidos. Conservar `cuenta_gen2=SI` firmado para C0D/tríadas y reportar su herencia separadamente. Conservar procedencia histórica tras una reestimación del mismo dato: nueva ejecución no significa muestra independiente.

## Fase 2 · Resolver identidad y propagar el origen

Normalizar rutas relativas, separadores y componentes `.`/`..` dentro del repo antes de clasificar. Verificar resolución material cuando exista el archivo, incluidos enlaces, sin permitir que una ruta externa sea asumida limpia. No rechazar sólo por prefijo parecido a un archivo (`tramite.yaml.otro`), ni perder linaje por un nombre alternativo.

Seguir los intermediarios observados: RESULT→CALC, referencias de snapshots, y manifiestos colectivos. Un padre `LEGACY-GEN1` inicia herencia aunque no haya sido descubierto por una ruta prohibida. Un intermediario sin origen acreditado devuelve indeterminado; nunca “limpio” por ausencia de patrón. Tratar ciclos y enlaces irresolubles explícitamente.

Separar código reutilizado de números reutilizados con evidencia de qué función ejecuta. No trasladar `correr-R.py` sólo para que desaparezca la marca. Para módulos con código y resultados embebidos, no basta una extensión `.py`: identificar la ruta numérica usada. Si no puede acreditarse de forma breve, dejar reserva del uso, sin bloquear medidas independientes.

La resolución debe producir un camino explicable desde el consumidor hasta la fuente, no sólo un booleano. Reutilizar los identificadores/hashes ya existentes. Añadir metadatos sucesores o un overlay derivado si las specs están congeladas: no re-sellar historia.

## Fase 3 · Usar el mismo criterio en adopción y revisión

Registro y T35 consultan la misma función de aptitud: un consumidor que se presenta como medición GEN2 no acepta un resultado numéricamente legacy/mixto/indeterminado sólo porque trae `generacion=GEN2` y el mismo valor. Tampoco se usa `cuenta_gen2` como sustituto de aptitud: un permiso de contar análisis no adopta cifras.

Usos históricos o de baseline continúan cuando están explícitamente identificados. Las excepciones válidas no borran el linaje. Un uso descriptivo/calibración de una medición nueva se diferencia de una confirmación independiente; esta última requiere roles de evaluación que se completan en 19.

Comprobar las 16 adopciones presentes al corte y sus sucesoras actuales. Si alguna pierde aptitud, devolver el RESULT, motivo, consumidor e impacto exactos. No declarar inválidas las 16 por el contraejemplo. No sustituir valores ni cerrar reservas científicas para que el nuevo check pase. Si aparece un falso positivo de linaje, resolverlo con fuente.

## Fase 4 · Pruebas y publicación

Pruebas mínimas: ruta canónica y equivalentes dan el mismo origen; copia/intermediario conserva origen; padre LEGACY inicia herencia; código estadístico histórico contrastado no se confunde con tasa copiada; hijo/nieto y orden inverso; origen desconocido no da limpio; wrapper adoptado como GEN2 se rechaza; RESULT nuevo válido se acepta; excepción de contador conserva origen; un CALC con resultados de distinto rol no los promociona en bloque.

Validar sobre fixtures y los casos reales de fase 1. Ejecutar 35 tests de corredores/84 de corrida0 o sus sucesores pertinentes. Integrar la publicación 09/#696 primero si ya existe, o entregar el cambio sin pisar su PR. Regenerar vistas desde evidencia vigente; no reejecutar 150 corridas ni sustituir veredictos de replay. Conciliar sólo filas afectadas por este arreglo, preservar firmas y negativos previos.

## Perímetro, dependencia y aceptación

Código: `tools/corrida0.py`, T35 en `tests/check.py`, pruebas de corrida0/corredores y un módulo pequeño sólo si evita duplicación material. Datos: metadatos de linaje sucesores y vistas derivadas coordinadas con 09. No editar medidores sellados, capturas ni probabilidades de milpa.

Aceptación: contraejemplo de adopción rechazado; falsos negativos de ruta/intermediario resueltos; reutilización de código evaluada por función; contador firmado intacto; herencia visible sin reclasificación masiva ciega; contrato utilizable por 18/19. Puede empezar ahora en Cloud; no esperar al final de la auditoría de todas las reglas.

## Contrato de ejecución, incluido para usar este archivo por separado

**Autoridad y lanzamiento.** La mesa pidió comprobar los candados GEN1→GEN2 y ajustar Gen2 aun si exige trabajo más robusto. Este encargo concreta esa solicitud; al entregarlo al ejecutor autoriza el perímetro descrito, commits, push y PR propio. El merge sigue siendo de mesa. No concede nuevas adopciones científicas, gasto de modelos ni una declaración de superioridad. Las decisiones previas válidas se conservan; una firma de contador no certifica independencia numérica.

**Arranque.** Lee `AGENTS.md`, este encargo completo, `.claude/commands/acto.md` y sólo las instrucciones sustantivas pertinentes. Reporta ruta absoluta, rama, HEAD y `git status --short`. Consulta main, PR y ramas por objeto para evitar duplicados; usa worktree propio. Archiva por el 0-bis vigente. El corte de preparación fue main #694, SHA `4816101e506f527d018dd2c47467a8b57bfbd487`, con #695–699 abiertos. Revalida únicamente cambios posteriores que afecten tu perímetro. Los ZIP de agosto son historia, no la base operativa.

**Integración.** Deriva ADR/NC/FP al cerrar, sin reservar números; quien integra después renumera y concilia sólo sus filas. Conserva filas ajenas por identidad y significado. Usa `tools/cierre_acto.py` según el procedimiento vigente, primero en seco; deja una sola ancla L0. No cambies `/despacha`, cierres PR ajenos ni borres worktrees. Actualiza las vistas globales sólo donde se autoriza expresamente; jamás reemplaces un TSV por una copia vieja. Los merges se serializan.

**Datos e historia.** Cloud trabaja código, documentos y agregados. Microdatos sólo en CAJA, con raíces y hashes del manifiesto. No reescribir specs, scripts, snapshots, capturas, resultados ni sellos congelados: usa sucesoras y enmiendas de alcance. Un control histórico no selecciona receta, filtro, ponderador ni variante por cercanía. Recalcular sobre la misma muestra puede ser trabajo GEN2, pero no es automáticamente evidencia independiente. Procedencia, reproducción, validación, adopción y uso en evaluación son estados distintos.

**Perímetro administrativo.** Encargo archivado, nota de cierre, filas directamente afectadas de decisiones/no-corrido/firmas/cola y cascada existente en gobernanza/estado/rótulos. No crear otra plataforma de gobernanza, base de datos o coordinador de tareas. Automatiza sólo defectos materiales reproducidos y con mantenimiento menor que el coste de repetición.

**Pruebas y cierre.** Pruebas materiales dirigidas, baseline requerido y diff final. No reparar fallos históricos ajenos para obtener una suite cosméticamente verde. Las pruebas adversariales adjuntas documentan defectos: después del arreglo sus salidas deberán cambiar según el contrato, no preservarse como oráculo del comportamiento correcto. Ninguna prueba escribe sobre el árbol científico real. Entrega `obligación | evidencia | consumidor/alcance | cierre o residual` y PR/HEAD. Una reserva mixta conserva su residual. No cerrar por nombre coincidente, sello o firma de contador solamente.

Continúa entre fases autorizadas. Ante una decisión científica nueva, prepara opciones concretas y termina las fases independientes; no conviertas una recomendación en firma. Cero llamadas nuevas a modelos y cero envío de solicitudes a terceros en estos tres encargos.


**Actualización comprobada al cierre:** main avanzó a `a63fd4ccc40204cf5215d466a593b4e1491bdda6` por #699 y #696. No cambió el código objeto de las sondas. 09 ya está fusionado: partir de sus vistas y no repetir su publicación. 14–16 están encolados por #699. Esta actualización prevalece sobre referencias de coordinación redactadas al corte inicial.
