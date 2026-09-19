# Tanda GEN2 · resultados, publicación y recibo

Fecha: 19/sep/2026. Repositorio: `Josanoforo/Modelado-Mexicano`.
Base verificada: `843a5f977e024ef5d74863e95856c763bee9e58d`.
Dos encargos completos, dos sesiones y dos PR. Trabajo simultáneo; integración final secuencial.

## Decisión de organización

Se ejecutan en paralelo:

| Carril | Encargo | Entorno | Resultado verificable |
|---|---|---|---|
| A | `GEN2-PISOS-REJILLA-CLI-1` · archivo 04 | Codex CLI, Ubuntu/WSL, corpus | Sucesores de pisos en categorías y universos comparables, ambos desenlaces ENIF, referencias numéricas por celda, replay y publicación resueltos. |
| B | `GEN2-RECIBO-CODEX-3` · archivo 05 | Codex CLI documental, sin microdatos | Veto y firmas propagados, trámites resueltos por producto, estado coherente y entrega de antecedentes al dueño del marcador. |

El recibo se adapta de nube a CLI documental para poder correr esta tanda con Codex. Mantiene su alcance de ejecución de firmas; ninguna decisión epistemológica nueva se delega al ejecutor. No lo lances simultáneamente en Claude y Codex.

Se respeta D1 de los documentos recibidos: **Claude conserva construcción del marcador y adopción por celda**, bajo `GEN2-MARCADOR-REDISENO-1`. El encargo Codex 03 y sus adendas de integración quedan sustituidos en su trabajo futuro por esta distribución. La localización del corpus y la reparación de pisos/replay pasan a A. El marcador y consumidor que ya produjo Codex se preservan para revisión y reutilización por Claude.

## Estado comprobado y ajustes a los briefs

1. #865 ya está fusionado, en `7453f513`; **no se lanza 01-bis** para aterrizar una rama ya integrada. Sus pendientes y correcciones operativas van completos a B.
2. #867, instrucciones v2.14, ya está fusionado; la compuerta inicial del recibo está satisfecha. Main es `843a5f9`.
3. #868 está abierto, HEAD revisado `9e9e89225f0d986cf51b955940ebee7526809f1b`, rama `codex/gen2-marcador-adopcion-cli-1`. Incluye publicación de replay y un consumidor de 20 C2, pero no sucesores de pisos. Su cuerpo declara un bloqueo de acceso a tres payloads; esa ausencia es un reporte de sesión que A debe verificar en caja. **No se fusiona #868 como sustituto de esta tanda.**
4. Los errores de rejilla y universos siguen en los pisos de #866. A conserva los cuatro originales y produce sucesores; los antiguos permanecen vetados para consumo.
5. ENIF se amplía explícitamente a `ahorra_solo_informal` e `informal_cualquiera`. La referencia de trabajo pasa a ENVIPE 15 + ENCIG 10 + ENIF 28 = **53 celdas potencialmente construibles**, no una cuota. Las cuatro celdas de formalidad ENIF, dos por desenlace, se dictaminan aparte. La cobertura sobre el árbitro completo se deriva; 74 no es una constante impuesta.
6. En el recibo original, `registro` sin escritura no prueba por sí solo que REPLAY-PISADO permita escribir. B comprobará además las transiciones y el guardia en memoria, sin escribir. A realiza la publicación.
7. El encargo 01 entregado en esta conversación **autorizaba expresamente** corregir cuatro errores materiales del insumo §13. Viaja en `fuentes/01-CONTRATO-Y-TRAMITE.md`. B diferencia esas correcciones autorizadas de omisiones del encargo. No fabrica una nueva decisión pendiente para volver a autorizar lo ya mandado.
8. La pregunta sobre P5_6 de ENIF 2021 tiene una respuesta documental en la spec sellada de DIN emisiones §0.1: tarjeta de débito. A confirma el FD de 2021 y usa tenencia de cuenta, no el nombre de variable como equivalencia.
9. La D3 de contador sigue pendiente: **sucesión técnica, clasificación GEN2 y adopción son cosas diferentes**. No se promete que SUPERADO disminuya el contador. A no adjudica `cuenta_gen2=SI`; B prepara la decisión faltante sin firmarla.
10. Para obtener resultados completos se amplía de forma acotada el perímetro original de A: acceso/recuperación de archivos, publicación de replay pendiente y, solo si es necesario, compatibilidad mínima para leer la sucesión ya declarada. B puede corregir la fuente o el caso mínimo del generador de relevo para aplicar RES-0043/0044 y actualizar referencias operativas al sucesor correcto.

## Propiedad y concurrencia

| Superficie | Dueño durante el trabajo paralelo |
|---|---|
| Corpus, configuración local, preflight y replay real | A |
| Specs nuevas, medidores, CALC sucesores, mapa de pisos y test de rejilla | A |
| `forense/replay-evidencia.tsv` | A |
| `tools/corrida0.py` | A, únicamente compatibilidad técnica indispensable; nunca adopción/consumidores |
| Demanda y vistas `corridas/resultados/usos` | A hasta su integración; B solo las regenera al cierre, después de incorporar A |
| Firmas, decisiones, NC, hallazgos, ADR, infraestructura, rutinas y estado | B |
| `tools/relevo_usos.py` y su derivado | B, únicamente RES-0043/0044 |
| Marcador, consumidor, celdas-D, motor, crosswalk y θ | Fuera de ambos; dueño posterior Claude |
| Notas y archivo de insumos | Cada carril, con rutas propias |

Ambas sesiones empiezan sobre main, con worktrees independientes. No uses la misma carpeta ni ejecutes dos escritores sobre los mismos archivos. Cada sesión archiva su encargo y fuentes en una carpeta con su rótulo; los originales viajan sin cambios de bytes.

La nota técnica de A suministra los hechos que B incorpora a los registros canónicos. A no abre una segunda NC paralela por cada defecto ya recibido por B. Un riesgo urgente se identifica en la nota de A para que B lo asiente, sin ocultarlo.

## Qué hacer con la sesión y el PR #868

En la misma sesión de Codex que llevaba el 03, entrega el encargo A. Primero debe preservar sus cambios y el SHA remoto de #868. No se borra ni se reescribe el historial. Si quedan cambios locales, se guardan en un commit de avance explícito antes de cambiar de worktree.

A continúa desde un worktree nuevo sobre main y una rama propia de pisos. Puede reutilizar la evidencia útil de #868, validándola, pero **no incorpora sus lectores, mapa de adopción, marcador ni vistas que mezclen adopciones**. Las vistas se regeneran desde fuentes.

B deja una entrega a Claude con el PR, SHA y lista de archivos reutilizables de #868. El cierre o transferencia administrativa de ese PR corresponde a su responsable después de preservar la entrega; estos encargos no lo cierran ni lo fusionan automáticamente.

## Orden de trabajo e integración

1. Lanza A y B ahora. A recupera acceso y mide; B ejecuta firmas y completa el recibo independiente de las nuevas mediciones.
2. A entrega y se revisa por contenido: identidades, universo, resultados por celda, controles y publicación. Se fusiona A cuando esté materialmente completo.
3. B incorpora ese merge, resuelve los cierres de replay que dependían de A y regenera los derivados afectados por sus decisiones. Entrega su PR completo; no crea RECIBO-CODEX-4 por una dependencia ya incluida aquí.
4. Se fusiona B. Claude recibe pisos publicados, veto histórico, mapa de resultados, pendientes explícitos y el prototipo de #868 para terminar `GEN2-MARCADOR-REDISENO-1`.

No se exige que B espere para empezar. Solo su cierre dependiente del replay espera a la integración de A. Ninguna sesión fusiona por iniciativa propia.

## Inputs de lanzamiento

**Sesión A, preferiblemente la que llevaba el 03:**

> Aplica la nueva distribución de responsabilidades del plan adjunto. Preserva #868 y cualquier cambio local; suspende la implementación del marcador y la adopción en Codex. Ejecuta íntegramente `04-GEN2-PISOS-REJILLA-CLI-1.md`, que absorbe acceso al corpus, reparación/publicación de replay y medición completa de pisos, incluidos ambos desenlaces ENIF. Trabaja en un worktree propio sobre main y entrega un PR completo. No fusiones.

**Sesión B, nueva sesión documental de Codex CLI:**

> Ejecuta íntegramente `05-GEN2-RECIBO-CODEX-3.md`. #865 y v2.14 ya están fusionados: verifica el estado actual y comienza sin esperar el carril A. Aplica firmas y veto, termina el trámite y prepara el recibo. Incorpora el PR de A para cerrar únicamente las piezas que dependan de sus productos y entrega tu PR completo. No abras microdatos, no modifiques el marcador ni fusiones.

Adjunta a ambas sesiones este paquete completo; cada encargo identifica qué fuentes necesita. No lances otro 03 ni un tercer lote de las supuestas 23 corridas: el brief retira esa propuesta por falta de specs.

## Aceptación de la tanda

- Mediciones nuevas comparables y publicadas, o exclusión semántica/de soporte demostrada por celda. Falta de acceso no se disfraza de NO-CONSTRUIBLE.
- Código real congelado con el diseño, fuente de replay válida y referencias de resultados consumibles.
- Firmas aplicadas, veto inequívoco, demanda/relevo/estado consistentes y deuda residual atribuida a su dependencia real.
- Cero adopciones nuevas de los cuatro pisos vetados; cero pérdida del trabajo de #868; entrega concreta al responsable Claude.

Fuentes: los tres adjuntos actuales, el encargo 01 y los originales incluidos; consultas GitHub a main y PR #865/#866/#867/#868. La revisión de preparación no abrió microdatos ni ejecutó cálculos de caja. Los encargos vuelven a comprobar premisas materiales al abrir.
