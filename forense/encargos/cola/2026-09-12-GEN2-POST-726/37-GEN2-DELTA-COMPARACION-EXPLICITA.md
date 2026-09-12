# 37 · Delta: comparar resultados sin inventar equivalencia

ENTORNO: CAJA

## Contrato de ejecución autónomo

Repositorio: `Josanoforo/Modelado-Mexicano`. Entorno: Codex CLI en CAJA Windows/WSL. Este MD contiene el encargo completo.

Al despacharlo, Jonás autoriza las fases y el alcance expreso de este documento, los commits, push y PR. La fusión queda con Jonás. No se firman por extensión adopciones, materialidad científica, FP-371/372/373/374, F6 ni acceso comercial. No enviar correos/formularios, aceptar compromisos de terceros o comprar; sí descargar material público y usar accesos previamente autorizados.

Lee `AGENTS.md`; reporta worktree absoluto, rama, SHA y estado. Usa worktree/rama propios. Contrasta main y PR abiertos pertinentes antes de editar: los encargos 27–32 están en ejecución o integración y no deben duplicarse. Corte de esta propuesta: main `e37367581d5186ce4d4cf497377c83ebcd61cf93`, #721–724 fusionados, #725–728 abiertos. El estado cambia: toma el efectivo al comenzar.

Resuelve montaje y dependencias antes de la ejecución. El corpus compartido sirve como entrada; temporales y resultados intermedios van al directorio de cada tarea. No sobrescribas archivos que otra sesión está leyendo. Publica incorporaciones por identidad y de forma atómica con los mecanismos existentes, preservando hashes, padres, sellos y evidencia ajena. No uses salidas GEN1 como insumo numérico GEN2 ni reetiquetes datos conocidos como retenidos.

Reutiliza herramientas y decisiones existentes. Evita otra cola, otro scheduler y wrappers sin necesidad. Valida los riesgos concretos y ejecuta sobre trabajo real: no entregues sólo fixtures, un inventario o un plan. Continúa las fases sin pedir otro encargo. Si una parte depende de un acceso externo, termina las independientes y deja el objeto y acción precisos; no inventes datos ni cierre completo.

Cierra encargo → resultado → evidencia → registros/vistas pertinentes → nota → ADR/L0/rótulo cuando aplique → PR. Actualiza filas comunes por clave canónica; quien integra después concilia y deriva desde el árbol conjunto, sin restaurar tablas completas de su rama. Pruebas dirigidas y gates aplicables, sin limpiar CI heredada ni rehacer la auditoría general.

## Resultado encargado y autorización

Implementar la capacidad de comparación repetible que `corrida0 delta` aún declara `NO-IMPLEMENTADO`. El despacho autoriza B-7 para pares explícitos y su demostración real. No autoriza un criterio nuevo de materialidad ni adopciones automáticas.

Casos útiles: el par histórico de #647 documentado en la propuesta de automatizaciones y las comparaciones permitidas de la serie ENIF/fintech de #706. Las cifras/identidades exactas deben recuperarse de evidencia sellada, no copiarse de este documento como si fueran fuente.

## Fase 1 · Contrato que ya existe

Lee `tools/corrida0.py` (stub, identidad y resolvedores), `forense/notas/2026-09-09-PROPUESTA-FINAL-AUTOMATIZACIONES-POSTCALCULOS-astra.md` §4, NC-0091/0048 y las specs/cierres de los pares elegidos. Busca implementaciones equivalentes antes de escribir una.

Entrada: identidad/versiones explícitas de ambos objetos, fuente del valor anterior al cambio, RESULT de oferta, consumidor/uso y contrato de comparabilidad. No inferir pares por parecido de nombre ni usar el valor actual ya adoptado como su propia línea base.

## Fase 2 · Comparación mecánica con límites científicos

Implementa en módulo propio y usa los resolvedores canónicos. Separa:

- identidad y reproducibilidad de las referencias;
- comparabilidad de unidad, población, evento, códigos, periodo y transformación;
- diferencia numérica en unidad original, puntos porcentuales cuando corresponda y cambio relativo sólo con base no nula;
- igualdad al grano publicado/tolerancia de representación;
- materialidad sustantiva sólo con criterio explícito y citado; si no existe, `NO-DETERMINABLE`.

Una comparación temporal intencional admite periodos distintos bajo su contrato; no exige año igual por inercia ni ignora una ruptura metodológica. No usar tolerancia de adopción como umbral de importancia. No convertir cambios observados en significancia, mejora causal o superioridad de GEN2.

El legado se lee únicamente como referencia de comparación; no se convierte en input de cálculo/emisión GEN2. Complementos mantienen referencia al padre y transformación. Faltantes, NO-ESTIMABLE, selección ambigua y denominador cero conservan estado explícito.

## Fase 3 · Ejecución real y salida útil

Ejecuta al menos:

1. El caso #647, cuyo valor histórico publicado es 0.045694 y la oferta documentada 0.04569409956405095: localizar originales, mostrar diferencia y equivalencia a seis decimales; materialidad no determinada sin criterio.
2. Un par temporal de crédito fintech 2021/2024 permitido por la spec de #706, con su definición de proxy visible.
3. La comparación no permitida por ruptura en cuenta fintech, o un par sin correspondencia científica acreditada: debe rechazar el delta sustantivo y explicar la causa.
4. Base cero o resultado ausente como protección dirigida, sin fabricar una nueva fuente real.

Si una referencia del caso histórico no se recupera, no inventarla: demostrar otro par autorizado inequívoco y registrar esa ausencia. Entrega JSON/TSV y lectura humana. Cuenta pares examinados, comparables y no determinables; «cero materiales entre cero comparables» no significa coincidencia general.

## Fase 4 · Conexión y cierre

Integra la entrada `corrida0 delta` sustituyendo únicamente su stub, con ayuda y ejemplos; modo lectura por defecto, salidas en destino explícito. No escribir `delta_legacy`, mover parámetros, cambiar tiers, re-sellar ni alterar contadores sin contrato aplicable. Puede entregar informe autónomo: no depende de `vigencia`, otra adopción o F6.

El encargo 30 puede tocar `tools/corrida0.py`. Desarrolla el módulo y ejemplos en paralelo; al integrar el pequeño adaptador CLI consume los cambios de 30 si ya están publicados y conserva su overlay. Si siguen simultáneos, delimitar ese único bloque y conciliarlo por función al merge, sin reemplazar el archivo completo. No demorar el cálculo de 30 por este accesorio.

Cierra NC-0091 sólo con la capacidad utilizable. NC-0048 mezcla implementación y correspondencia/materialidad: conciliar únicamente lo acreditado, dejando su decisión histórica pendiente si sigue sin contrato. Entrega resultados y comando listo para la siguiente comparación, con pruebas dirigidas de referencias, cero y rupturas. No agregar una nueva rutina programada.

## NO-CORRIDO / RESERVAS

- No se compararon los 211 RESULT históricos citados por `NC-0048`: no hay
  correspondencias explícitas y verificables para ese universo. La fila queda
  ABIERTA con el contrato y la acción sucesora precisos.
- No se declaró materialidad científica, adopción, firma, F6 ni acceso
  comercial; tampoco se modificaron `delta_legacy`, motor, tiers, specs,
  sellos, vistas, contadores o cron.

## CONSUMIDO

Consumido el 11/sep/2026 por `ACTO GEN2-DELTA-COMPARACION-EXPLICITA` en la
rama `acto/gen2-delta-comparacion-explicita`, worktree
`/home/pc0/mm-gen2-delta-comparacion-explicita`. Implementación base en
`4503dc7`; publicado como PR #733.

Resultado: `corrida0 delta` implementa `GEN2-DELTA-1` y ejecuta tres pares
reales con JSON, TSV y lectura humana: #647 coincide a seis decimales,
crédito/app ENIF 2024−2021 produce −12.303002012 pp descriptivos y cuenta/app
se rechaza por ruptura. Tres materialidades quedan `NO-DETERMINABLE` porque el
acto no inventa criterio. `NC-0091` cierra; `NC-0048` conserva abierto el
universo histórico sin correspondencia explícita. Cero adopciones, re-sellos,
cambios a motor o contador científico. Evidencia y límites en
`forense/notas/2026-09-11-GEN2-DELTA-COMPARACION-EXPLICITA-cierre.md` y
`ADR-486`, renumerado al integrar primero PR #731 como ADR-484 y después
PR #729 como ADR-485.
