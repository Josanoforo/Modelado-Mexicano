# Glosario del registro (`data/corrida0/`)

Este documento define, por escrito, valores del registro que el código ya
emite pero que no tenían definición en prosa (firma de mesa D8, 23/sep/2026:
«A, pero que se explique claramente qué significa.» — ACTO
GEN2-TRAMITE-FIRMAS-11).

## `INDETERMINADO`

**Campo:** `origen_numerico` (columna de `data/corrida0/corridas.tsv`;
también aparece en el campo `ayuntamientos` de
`data/p0-calendario-ayuntamientos-v1_0.tsv`, con el mismo significado
genérico — «no se pudo determinar», no «no hubo dato» ni «vale cero»).

**Qué significa.** `INDETERMINADO` es lo que el registro emite cuando el
mecanismo que deriva `origen_numerico` no puede seguir la cadena de
procedencia (E.2: SPEC → CALC → INPUTS → CÓDIGO → ENTORNO → EJECUCIÓN →
RESULT → USO) hasta una respuesta limpia de `NUEVO` / `HEREDADO` / `MIXTO`.
En `tools/corrida0.py` (`_deriva_origen_numerico` y funciones relacionadas,
~línea 3897), esto ocurre en tres casos concretos:

1. El input que se está clasificando es **METADATO**, no **DATO** (un
   `spec.yaml`, un `sello.json`, un `sello.sha256`, un `ejecucion.json`):
   estos archivos no tienen "origen numérico" propio, no son la cifra.
2. El input es un **dictamen** (un veredicto textual: `EQUIVALENTE`,
   `NO-CONSTRUIBLE`, etc.), no un número: la pregunta "¿de dónde salió este
   número?" no aplica.
3. Un **TSV sin campo `funcion`** — el registro no puede distinguir si esa
   fila es dato de entrada o resultado derivado porque la tabla misma no
   lo declara.

En todos los casos, el registro **no puede derivar** el origen — no es que
el dato esté ausente ni que el origen sea desconocido por descuido: es que
la pregunta, para ese input, no tiene la forma que el mecanismo sabe
resolver.

**Qué NO implica.**
- **No bloquea `cuenta_gen2`.** La decisión de si una corrida cuenta como
  GEN2 la toma mesa (E.2, adopción por bloque); `INDETERMINADO` en
  `origen_numerico` es información sobre la cadena de un input, no un veto
  automático sobre el RESULT que lo consume. (Distinto del caso de
  `linaje.py` que niega `MEDICION-GEN2` sobre un RESULT cuyo origen
  *heredado* no está acreditado — ver NC-0392: ahí el bloqueo es explícito
  y nombrado, no una consecuencia implícita de ver `INDETERMINADO`.)
- **No bloquea adopción.** Adoptar un RESULT es un acto de mesa sobre el
  RESULT, no sobre el `origen_numerico` de sus inputs de METADATO.
- **No es un error ni un `FAIL`.** Es una clasificación válida y esperada
  para METADATO y dictámenes — la mayoría de las filas `INDETERMINADO` en
  `corridas.tsv` son exactamente eso.

**Quién lo refina.** `INDETERMINADO` no se "corrige" a mano ni se sustituye
con un valor supuesto. Si el input es TUBERÍA (una tabla derivada sin campo
`funcion`), el acto que toque `_funcion_de_dependencia` en
`tools/corrida0.py` es el único autorizado a estrechar el criterio —
declarando el campo `funcion` que falta, no reclasificando la fila desde
fuera. Un acto que encuentre un `INDETERMINADO` que le parece evitable no lo
edita: lo reporta como hallazgo y, si aplica, abre una NC con sucesor
`TUBERÍA` (o el que corresponda).

**Falsador.** Si un `INDETERMINADO` alguna vez bloquea una adopción de mesa
o mueve `cuenta_gen2` sin que una firma de mesa lo autorice explícitamente
por su propio nombre, esta definición está mal y se corrige.
