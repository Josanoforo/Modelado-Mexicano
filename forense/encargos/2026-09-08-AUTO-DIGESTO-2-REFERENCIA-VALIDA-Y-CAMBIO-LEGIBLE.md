# ACTO AUTO-DIGESTO-2 · REFERENCIA-VALIDA-Y-CAMBIO-LEGIBLE

Encargo propuesto, listo para ejecución antes de iniciar los cálculos solicitados por mesa.

Repositorio: `Josanoforo/Modelado-Mexicano`.  
Base comprobada: `origin/main = 6f46976c345731b6cdb13ccfb6ca0b59d4a16ba3`, merge de PR #623.  
Fecha: 8 de septiembre de 2026.

## Objetivo

Completar dos condiciones pendientes del digesto incremental integrado por PR #622:

1. No producir un diff comparable cuando el hash de la referencia recuperada contradice el declarado por el digesto anterior.
2. Mostrar los valores anteriores y nuevos de los campos modificados de una reserva, además de sus cambios de estado.

La entrega es un parche acotado con pruebas de regresión. Este encargo no ejecuta mediciones, no recalibra el motor y no implementa `corrida0 delta`. Preparar este documento no significa que el parche ya esté aplicado.

## Premisas comprobadas y reproducción

La revisión sobre la base indicada encontró:

- `seccion_h()` detecta un hash discrepante, escribe «NO coincide», pero continúa y declara `BASE-COMPARABLE`, con `h_error = None`.
- Al cambiar únicamente el campo `impacto`, la tabla muestra `MODIFICADA (impacto) | ABIERTA | ABIERTA`; no aparecen el impacto anterior ni el nuevo.
- Ambos comportamientos se reprodujeron mediante `_Repo`, el repositorio Git temporal del arnés de `tests/test_digesto_nc.py`. No se modificaron datos del proyecto.
- La referencia automática utilizada por el `main` revisado sí tiene hash coincidente. El primer hallazgo es un defecto del tratamiento de referencias incongruentes; no acredita corrupción del corte real.
- Las 14 pruebas actuales del digesto pasan y ya están conectadas a la suite mediante `T39`. Reutilizar esa conexión.

## Inicio y perímetro

Leer `AGENTS.md`, este encargo y el contrato de AUTO-DIGESTO-1. Usar un worktree limpio y una rama propios; reportar ruta absoluta, rama, HEAD y estado del árbol. Actualizar `origin/main` y comprobar que los dos defectos siguen presentes. Si ya se corrigió uno, completar únicamente el otro.

Archivos de implementación:

- `tools/digesto_tramite.py`: validación de integridad de la referencia y presentación de cambios en H.
- `tests/test_digesto_nc.py`: regresiones de esos dos comportamientos, reutilizando el arnés existente.
- `.claude/commands/tramite.md`: solo si hace falta reflejar el comportamiento de parada o la presentación final.
- El encargo archivado y los archivos de cierre que exija el procedimiento vigente; usar las herramientas existentes para sus actualizaciones.

No modificar el motor, parámetros, corpus, baseline de pruebas, scheduler, CI ni CALC sellados. No reconstruir digestos históricos. No cerrar `NC-0032`: la observación de ejecuciones periódicas reales sigue siendo una condición distinta. No ampliar la tarea para resolver `NC-0027`, la ambigüedad de SHA corto o deuda incidental.

## Ajuste 1 · El hash incongruente detiene el diff

Dentro de `seccion_h()`, cuando existe un hash declarado en `H-REF` y el TSV recuperado no coincide con él:

1. Comparar con `_hash_tsv()`, conservando la normalización de transporte vigente.
2. Registrar `h_error` con una causa identificable, por ejemplo `HASH-REFERENCIA-NO-COINCIDE`. Incluir SHA de referencia y hashes esperado y obtenido para poder resolver el problema.
3. Terminar la sección antes de calcular o presentar el delta. No declarar `BASE-COMPARABLE`, `SIN-CAMBIOS` ni conteos de novedades sobre esa referencia.
4. Utilizar el flujo de error existente de `main()`: salida no exitosa, código 2, y ninguna escritura del nuevo digesto. Conservar el archivo anterior byte a byte.
5. Aplicar la misma validación al modo `--stdout`: puede explicar el error, pero no emitir un diff aparentemente válido.

No reemplazar silenciosamente la referencia dañada por otra más antigua. El operador debe corregir la referencia o usar conscientemente el mecanismo explícito de diagnóstico ya disponible.

Conservar los casos legítimos existentes: primera emisión sin base; historial no recuperable; referencia explícita válida; digestos antiguos sin hash declarado. La ausencia de un hash histórico se etiqueta como tal y no se confunde con una discrepancia comprobada.

## Ajuste 2 · Valores anteriores y nuevos legibles

Mantener una fila principal por ID afectado. Para cada campo modificado, presentar su valor anterior y su valor actual. Se permite una columna de detalle o un bloque asociado al ID; elegir la solución más simple que siga siendo legible con textos largos.

Ejemplo ilustrativo, ajeno a las reservas reales:

| ID | Cambio | Antes | Después |
|---|---|---|---|
| NC-EJEMPLO | MODIFICADA: impacto | Impide correr la celda A | Impide correr las celdas A y B |
| NC-OTRO | MODIFICADA: sucesor | E5 | C0-C |

Contrato de presentación:

- Si cambian estado y contenido, mostrar ambos en la misma reserva y mantener un solo ID en el total de afectados.
- Si cambian varios campos, identificar cada campo y sus dos valores con un orden estable.
- Distinguir un valor vacío de la ausencia de una reserva. Conservar las categorías actuales de alta y ausencia; una desaparición no es un cierre.
- Reutilizar la neutralización de marcadores vigente. Escapar barras verticales y tratar saltos de línea para que el texto no rompa las tablas Markdown. La representación no modifica el TSV fuente ni la comparación de contenido completo.
- Aplicar el límite de texto existente cuando corresponda y declarar la truncación. Los conteos se calculan antes de truncar.
- Facilitar la consulta íntegra de ambos valores mediante referencias a los cortes anterior y actual del TSV. Un enlace solo al archivo actual no permite recuperar el contenido anterior.

No cambiar cómo se determinan los IDs afectados para resolver un problema de presentación. No crear una segunda base de datos, un nuevo formato de estado o una opción obligatoria adicional.

## Pruebas de regresión

Añadir casos al archivo existente, en repositorios temporales. Deben demostrar los defectos sobre la versión anterior y pasar con el parche.

**Referencia incongruente:** publicar un digesto válido en el fixture; alterar únicamente su hash declarado y versionarlo; invocar la comparación automática. Comprobar error explícito y ausencia de delta comparable. Probar el CLI con un archivo de salida previamente existente: devuelve 2 y conserva sus bytes. Incluir `--stdout` sin escrituras. Mantener un caso de referencia válida que siga pasando.

**Cambio de contenido:** publicar un corte con `impacto = IMPACTO_ANTERIOR`; cambiarlo a `IMPACTO_NUEVO`, manteniendo el estado. Comprobar que ambos textos aparecen asociados al campo y a la misma reserva. Repetir para cambio de sucesor y para cambio simultáneo de estado/contenido, sin duplicar el ID afectado.

**Formato del detalle:** usar en esos mismos fixtures un valor vacío, texto largo, una barra vertical y un salto de línea. Comprobar representación legible, truncación declarada cuando corresponda y conservación de los valores fuente. Mantener la validación de marcadores del generador.

Ejecutar:

```bash
python3 tests/test_digesto_nc.py
```

El número final de casos se reporta según lo realmente implementado. No sustituir los 14 casos previos ni fijar un conteo cosmético.

Ejecutar una vez la suite de baseline exigida por el flujo para el diff final. Hacer una demostración de solo lectura sobre el árbol real, con `--stdout --sin-suite`, y comprobar que la referencia válida sigue funcionando. No volver a ejecutar la suite completa por cada ejemplo.

## Cierre y entrega

El parche queda listo cuando:

- Un hash discrepante impide presentar o publicar el diff, preservando la salida anterior.
- Un cambio de contenido muestra qué había y qué hay ahora.
- Los dos casos de regresión, los casos previos y la conexión existente a T39 siguen operativos.
- El diff respeta el perímetro y no altera resultados del modelo ni artefactos sellados.

Entregar el cambio en una rama propia, con texto de PR listo y publicación conforme a la autorización de mesa. No fusionar automáticamente. El cierre debe incluir los ejemplos antes/después, comandos y resultados de pruebas, y cualquier reserva material. Distinguir CI remoto confirmado de validación local.

Completado este parche, terminar el encargo y reportar el digesto listo para acompañar los cálculos. No convertir este trabajo en otro ciclo de infraestructura ni declarar que los requisitos sustantivos de cada cálculo quedaron satisfechos por corregir el digesto.

## Referencias

- [PR #622: digesto incremental integrado](https://github.com/Josanoforo/Modelado-Mexicano/pull/622).
- [Generador en la base revisada](https://github.com/Josanoforo/Modelado-Mexicano/blob/6f46976c345731b6cdb13ccfb6ca0b59d4a16ba3/tools/digesto_tramite.py).
- [Pruebas existentes del digesto](https://github.com/Josanoforo/Modelado-Mexicano/blob/6f46976c345731b6cdb13ccfb6ca0b59d4a16ba3/tests/test_digesto_nc.py).

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Ninguno. | — | Los dos ajustes pedidos (hash incongruente detiene el diff; valores antes/después de campos modificados) se implementaron y probaron completos; los 14 casos previos y la conexión a T39 siguen operativos; no se tocó el motor, parámetros, corpus, baseline de pruebas, scheduler, CI ni CALC sellados; no se reconstruyeron digestos históricos; `NC-0032` sigue ABIERTA (condición distinta, no tocada); `NC-0027`, la ambigüedad de SHA corto y deuda incidental no se ampliaron. | Ninguno. | — |

## CONSUMIDO

Ejecutado por [PR #625](https://github.com/Josanoforo/Modelado-Mexicano/pull/625). ADR-405. Ambos ajustes implementados, 6 casos de regresión nuevos (20 en total), `tests/check.py --baseline` VERDE.
