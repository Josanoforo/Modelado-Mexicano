# Paquete de ejecución multifase · posterior a PR #685

Fecha: 10 de septiembre de 2026. Autor: ChatGPT, preparación de encargos para mesa y Codex. Estado consultado: `origin/main=486eda19944a94d978791eb423559144de98d16b`. Este paquete es un despacho preparado; todavía no se ejecutaron sus ocho lotes ni se modificó el repo desde esta revisión.

**Objetivo: completar la evaluación y convertir las decisiones ya firmadas en datos, parámetros y operación utilizables durante los siguientes días y semanas.**

## Qué ya está resuelto

**Observado:** [#684](https://github.com/Josanoforo/Modelado-Mexicano/pull/684) fusionó el contrato L v1.4 y su diagnóstico. [#685](https://github.com/Josanoforo/Modelado-Mexicano/pull/685) asentó D01–D20, cerró 14 NC, firmó FP-314/361/363 conservando sus ejecuciones y archivó ambos benchmarks. Su nota reporta 69 NC abiertas y 75 cerradas. La consulta de PR abiertos devolvió cero al corte; esto no descarta trabajo local no publicado.

**Interpretación:** no necesitamos volver a E01, a D20 ni a investigar desde cero D11/D16. **Consecuencia:** este paquete ejecuta E02–E11 agrupados por producto y agrega los tres residuales concretos que facilitan el cierre de los siguientes cálculos.

Fuente consolidada: [cierre de E01](https://github.com/Josanoforo/Modelado-Mexicano/blob/486eda19944a94d978791eb423559144de98d16b/forense/notas/2026-09-10-MESA-CONCILIACION-E01-cierre.md). Los ZIP de agosto son antecedentes y no vuelven a usarse para reconstruir main.

## Archivos para lanzar

Cada MD contiene sus fases, entradas, perímetro, compuertas, pruebas, cadena de cierre y contrato común completo. Adjuntar **un archivo por tarea**, no pegar los ocho en una misma conversación de ejecución. Se puede avanzar una cartera de varias tareas sin pedir otro encargo para cada fase.

| Lote | Resultado | Destino para terminar | Antecedentes |
|---|---|---|---|
| [01 · F5 completa](01-GEN2-F5-COMPLETA.md) | Corpus sucesor, 176/224 posiciones y adjudicación del marco completo | CLI con corpus y cliente del competidor | E02 + E03; D01/D02 |
| [02 · Motor y complementos](02-GEN2-MOTOR-USOS-Y-COMPLEMENTOS.md) | Uso correcto de eventos/poblaciones y propuesta concreta de RES-0028 | Cloud; CLI si requiere nuevo estimador | E04 + D11 de E11 |
| [03 · ENIF población](03-GEN2-ENIF-POBLACION-Y-ADOPCION.md) | A/A adoptado y celda de no trabajadores | CLI con microdatos | E05; D04/D05 |
| [04 · S6/S12/S13](04-GEN2-S6-S12-S13-SUCESORAS.md) | Llave documentada, cálculo entre receptores y cláusula histórica acotada | CLI; documentación preparable en Cloud | E06 + E07; D13/D14/D15 |
| [05 · ENVIPE serie](05-GEN2-ENVIPE-SERIE-COMPLETA.md) | Serie por ola con comparabilidad y huecos explicados | CLI con microdatos | E08; D12 |
| [06 · Adquisición y DIN](06-GEN2-ADQUISICION-DIRIGIDA-Y-DIN.md) | Insumos, tandas académicas y diseño/alternativa inferencial DIN | Cloud + continuación CLI cuando corresponda | E09 + D16 de E11 |
| [07 · SONDA/cron](07-GEN2-SONDA-CRON-PRODUCCION.md) | Configuración única y disparo/recuperación demostrados | CLI Windows/WSL; código preparable en Cloud | E10; D19 |
| [08 · Pruebas/replay](08-GEN2-PRUEBAS-LIMPIAS-Y-REPLAY.md) | Suite sin escritura, guard L0 y fuentes de replay | Cloud + prueba/publicación CLI | NC-0141/0148/0104 |

## Primera tanda recomendada

1. **Lote 01 en CLI:** es el frente principal. Preparar y congelar los insumos aunque el cliente del modelo todavía no esté disponible. No cambiar competidor para aprovechar otra cuenta.
2. **Lote 06 en Cloud:** avanzar fuentes públicas, expedientes y búsqueda dirigida. Las demandas del lote 01 tienen prioridad; no tiene que esperar a que termine la evaluación.
3. **Lote 08 en Cloud:** fases de pruebas/derivador; continuar en CLI cuando necesite un verify real. Corregir NC-0141 temprano reduce el trabajo accidental de los siguientes PR.

Son tareas manuales en ramas/worktrees distintos. Mantener el candado del despacho automático y comprobar cualquier acto local ya corriendo antes de iniciar uno con el mismo objeto. No se exige lanzar subagentes dentro de cada tarea.

## Segunda tanda y secuencia de integración

- **Lote 07:** preparar código después de integrar las modificaciones compartidas de tests del 08, o reconciliarlas antes de su merge; luego probar en Windows/WSL. No debe esperar semanas para demostrar el cron.
- **Lote 02:** puede empezar su lectura y cambios propios mientras corre 01. Publicar su contrato de etiquetas/usos antes de integrar la adopción ENIF de 03.
- **Lote 04:** sus dos piezas documentales son rápidas y no requieren nuevas llamadas; S12 continúa cuando estén disponibles sus insumos.
- **Lotes 03 y 05:** ejecutar en caja conforme a disponibilidad de archivos y recursos, en worktrees separados. Una fuente bloqueada no inmoviliza las olas o dominios restantes.

Los cambios administrativos de canon, NC/FP y vistas coinciden entre PR aunque el trabajo sustantivo sea independiente. **Serializar los merges**, traer main antes de cerrar cada PR y reconciliar sólo sus filas. No imponer un orden total a todos los cálculos: las dependencias reales son insumos y contratos.

| Dependencia | Regla |
|---|---|
| #684/#685 → todos | Ya satisfecha al corte; verificar por ascendencia al lanzar. |
| Corpus 01 F1 → capturas 01 F3 | Obligatoria; no recapturar sobre un paquete defectuoso. |
| Spec 01 F2 → nuevos resultados | Commit previo obligatorio. |
| 06 → 01/03/04/05 | Sólo las fuentes concretas que realmente falten; no bloquea todo el lote. |
| 02 → adopción final 03 | Compatibilidad de etiquetas/uso ENIF; el cálculo 03 puede prepararse antes. |
| 08 → 07 | Reconciliar `tests/check.py` si ambos lo modifican; no una dependencia científica. |
| CALC disponible → 08 F4 | Puede ser uno existente verificable; no tiene que esperar al último cálculo nuevo. |
| Código 07 → operación de caja | Merge de código no sustituye instalación y pruebas reales. |

## Horizonte de trabajo por resultados

**Primeros días:** resolver suite/registro prioritario, preparar corpus sucesor, mover accesos y demostrar la operación del cron. El éxito se mide en bloqueos eliminados e insumos utilizables, no en cantidad de notas.

**Siguiente tramo:** ejecutar evaluación completa, ENIF poblacional, S12 y las olas ENVIPE disponibles. Mantener la adquisición activa para huecos concretos. No es una promesa de duración: modelos, corpus y permisos de caja se comprueban al inicio.

**Semanas siguientes:** incorporar respuestas externas, resolver las propuestas D03/D11/FP-371 que aún necesiten adjudicación y evaluar nuevas versiones de motor en experimentos propios. No recalibrar el M congelado de 01 mientras se lo está evaluando. D21/F6 no se considera elegida por pedir más capacidad de trabajo.

## Prompt de lanzamiento para cada archivo

```text
Ejecuta el encargo adjunto completo en Josanoforo/Modelado-Mexicano.
Consulta origin/main y el estado de tareas/PR del mismo objeto antes de editar.
Respeta las decisiones asentadas por PR #685 y continúa las fases cuyas
compuertas estén satisfechas. No te detengas en proponer un plan.
Usa un worktree y una rama propios. Prepara commits y un PR revisable;
yo hago el merge. Si el entorno no permite una fase, completa las demás
y deja la continuación exacta con evidencia del bloqueo y su residual.
No repitas E01 ni los benchmarks ya registrados. No hagas merges automáticos.
```

## Continuación Cloud → CLI

Continuar el mismo encargo desde la rama/PR y SHA entregados, leyendo el archivo archivado y la tabla de fases. No reiniciar desde main ni volver a producir la misma spec. Verificar integridad de entradas congeladas; usar la raíz real configurada de datos. Las capacidades locales del usuario no se presumen disponibles en Cloud.

Preparación de código, ejecución de una medición, adopción al motor y operación del scheduler tienen comprobantes diferentes. El cierre debe nombrar cuál se alcanzó. Si se integra una fase parcial útil, dejar un sucesor identificado y continuar desde ese merge sin ocultar el residual.

## Límites de decisiones y recursos

La ampliación de cuenta permite dedicar más trabajo; no modifica al modelo competidor de F5 ni acredita disponibilidad de Claude, microdatos o Windows en Cloud. Usar la suscripción/cliente configurado; no abrir gasto de API ni inversión comercial de tandas. Los lotes no incluyen una migración tácita de proveedor.

D03 autoriza diseñar el uso y separar elementos cuando el motor lo necesite; no inventa las tres opciones de población/evento/no respuesta. D11/D16 autorizaron investigación, ya registrada; su aplicación concreta puede dejar una adopción puntual para mesa. No pedir de nuevo D04/D05/D13/D14/D15/D17/D19 cuando ya están asentadas.

## Control de alcance final

Cobertura de antecedentes: E02/E03→01; E04→02; E05→03; E06/E07→04; E08→05; E09→06; E10→07; E11→02/06. E01 no se repite. Los residuales NC-0141/0148/0104 tienen dueño 08, con comprobantes aportados por los lotes de cálculo.

Al terminar cada tarea, el siguiente paso sale de su resultado, no de reconstruir el historial. Ningún encargo transforma falta de respuesta en rechazo de mesa ni una firma en ejecución ficticia.
