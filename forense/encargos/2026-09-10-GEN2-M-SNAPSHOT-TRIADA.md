# ENCARGO · ACTO GEN2-M-SNAPSHOT-TRIADA

Recibido en mesa 10/sep/2026 (despacho 4/5 de la batería que la firma de
mesa pidió el 9/sep — "necesito que midas al menos 5 encargos a correr en
claude code... dame 5 completos"). Texto verbatim del lanzamiento:

> ENCARGO 4/5 · ACTO GEN2-M-SNAPSHOT-TRIADA
>
> CONGELAR AL MOTOR ANTES DE ENSEÑARLE EL EXAMEN
>
> OBJETIVO: producir el snapshot de M que competirá contra L_SOLO y
> L_CORPUS en exactamente las tareas del marco, sin modificar el motor
> después de mirar los R de evaluación.
>
> CABECERA: NUBE preferente, Opus. Si alguna emisión exige caja, separar
> únicamente esa ejecución, no cambiar el contrato. Cero nuevas
> adquisiciones.
>
> COMPUERTA: contrato TRIADA fusionado. No depende de que ENCARGO 3/5
> haya terminado, porque el snapshot de M no debe mirar R.
>
> FIRMA DE MESA:
> El motor que compite es el motor vigente congelado para evaluación, no
> una versión retocada después de ver los árbitros. Desde este snapshot y
> hasta el cierre del TRIADA-CALC no se adoptan al motor cifras
> procedentes de los targets de evaluación con el propósito de mejorar el
> duelo. Una mejora futura del motor pertenece a otra generación de
> evaluación.
> Esta firma protege la pregunta central contra overfitting accidental.
>
> P1 · CONGELAR IDENTIDAD DEL MOTOR
> Al arrancar:
>
> * derivar `origin/main`;
> * registrar hash del árbol relevante de `milpa/`;
> * hash del emisor;
> * hash/configuración de reglas, conductas, coeficientes y valores que M
>   consume;
> * fecha;
> * versión de herramientas.
>
> Tomar como referencia histórica el estado existente tras PR #674.
> Si entre #674 y este acto cambió materialmente el árbol que alimenta M,
> declarar exactamente qué cambió. No ocultarlo tras el SHA general del
> repo.
>
> P2 · REUSAR O REEMITIR
> Para las 14 celdas:
> primero verificar si los `M-<id>__v1_3.json` existentes fueron
> producidos por exactamente el mismo estado material del motor.
>
> * Si SÍ: reutilizarlos, citando hash y procedencia.
> * Si NO: reemitir M para esas celdas desde el snapshot congelado.
>
> No seleccionar entre M antiguo y M nuevo según cuál quede más cerca de
> R.
> La regla de elección se decide sólo por identidad del snapshot.
>
> P3 · FIREWALL DE OBJETIVO
> Construir para cada celda la cadena de insumos de M suficiente para
> responder: ¿algún valor que M consume es exactamente el árbitro de esa
> misma celda, la misma ola/variable objetivo o una materialización
> directa de ella?
> Estados:
>
> * `LIMPIO-DE-OBJETIVO`.
> * `CONTAMINADO-POR-OBJETIVO`.
> * `INDETERMINADO-POR-PROCEDENCIA`.
>
> No se decide por cercanía numérica.
> Una celda contaminada no se repara aquí. Se etiqueta y queda fuera de
> `U3`.
> Una calibración en otra ola/fuente puede seguir siendo válida para la
> primaria operacional, pero su aptitud para TRANSFERENCIA se decide por
> el corte secundario de la spec TRIADA.
>
> P4 · CALC/SNAPSHOT
> Crear un producto sellado que entregue, por celda:
>
> * id;
> * punto M;
> * snapshot/hash;
> * fuentes/valores materiales consumidos;
> * estado firewall;
> * corrida M reutilizada o nueva;
> * razón de exclusión si la hay.
>
> No calcular error contra R.
> La salida debe poder entregarse al ENCARGO 5/5 sin abrir nuevamente
> `milpa/`.
>
> P5 · SONDA DE INMUTABILIDAD
> Antes y después del snapshot:
> `git diff` de todo el perímetro motor = cero, salvo artefactos nuevos de
> registro/snapshot fuera de `milpa/`.
> Este acto mide al motor; no lo mejora.
>
> PERÍMETRO: artefacto snapshot/CALC M, notas, registro, 0-bis, cascada.
> NO TOCA: `milpa/` salvo lectura, R, L, capturas, extractor,
> calibraciones, adopciones.
> CONTADOR: `cuenta_gen2 = SI` para el snapshot/CALC si entra como
> resultado GEN2 con cadena completa. No crea adopción.
> CIERRE: tabla de 14 celdas con punto M y firewall; NC únicamente para
> contaminaciones/procedencias que cambien `U3`.
> SUCESOR: ENCARGO 5/5.
