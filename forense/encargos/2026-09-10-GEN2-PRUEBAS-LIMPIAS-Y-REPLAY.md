# Archivo 0-bis A.3 · ACTO GEN2-PRUEBAS-LIMPIAS-Y-REPLAY

- **SHA de redacción:** `486eda19944a94d978791eb423559144de98d16b` (merge de PR #685).
- **SHA de ejecución:** `origin/main = 44134745ce7f19af18a87b153a99de3d506063b0` (merge de PR #686); el corte de redacción es ancestro.
- **Entorno asignado:** NUBE para pruebas/derivador y CLI Ubuntu con corpus para comprobante real/publicación.
- **Estado:** CONSUMIDO por PR #690.

## VERIFICACIÓN DE EXISTENCIA (A.8; ejecutor, 10/sep/2026)

- **Estructura:** existen `tests/check.py`, `tests/test_corrida0.py`, `tests/test_cierre_acto.py`, `tools/cierre_acto.py`, `tools/corrida0.py`, `forense/replay-evidencia.tsv` y las tres vistas `data/corrida0/{corridas,resultados,usos}.tsv`.
- **Contenido:** `t_cmd_demanda_aplica_fp339` llama `C.cmd_demanda(None)` con las rutas reales y después lee `C.SALIDA/demanda-resultados.tsv`; la regla compartida `L0_ADR_RE` ya exige unicidad en `cierre_acto.py`; las tres vistas publicadas carecen de columna de fuente, aunque `forense/replay-evidencia.tsv` distingue procedencia y alcance.
- **Cobertura retroactiva:** `NC-0141`, `NC-0148` y `NC-0104` existen y siguen `ABIERTA` en `forense/no-corrido.tsv`. La evidencia heredada está sembrada, pero falta un comprobante real `VERIFY-ESTRUCTURADO` y su fuente persistida en las tres vistas. PR #682/#683 son antecedentes, no objetos a reabrir.

---

# ENCARGO · GEN2-PRUEBAS-LIMPIAS-Y-REPLAY

## Pruebas sin escritura → evidencia de replay → vistas con fuente

Fecha de preparación: 10 de septiembre de 2026. Corte verificado: `486eda19944a94d978791eb423559144de98d16b` (merge de #685).

**Destino:** Cloud para pruebas/derivador; CLI con corpus para comprobante real y publicación de vistas. **Integra:** residuales NC-0141/0148/0104. Complementa E03/E05/E07/E08, sin repetir #682/#683/#685. **Rama:** `acto/gen2-pruebas-replay`.

## Resultado y perímetro

Eliminar dos tropiezos medidos del circuito de entrega y completar la trazabilidad de replay que sigue pendiente. No una refactorización general de corrida0 ni una auditoría de todos los cálculos.

Leer `tests/check.py`, `tests/test_corrida0.py`, `tests/test_cierre_acto.py`, `tools/cierre_acto.py`, `tools/corrida0.py`, `forense/replay-evidencia.tsv`, specs/recibos del CALC elegido y las tres vistas de `data/corrida0/`. Puede editar pruebas afectadas, el derivador/esquema mínimo de fuente, consumidores que deban leer la columna y evidencia/vistas. No altera mediciones ni reescribe sellos o baseline.

**Observado:** NC-0141 localiza el test que reescribe demanda sobre el árbol real; NC-0148 documenta ancla L0 duplicada no atrapada por test; #685 dejó NC-0104 abierta y no aplicó 35 transiciones proyectadas en dry-run. **Consecuencia:** no repetir aquella derivación global a ciegas.

## Fase 1 · Aislar la escritura de las pruebas

Reproducir de forma acotada `t_cmd_demanda_aplica_fp339`. Mover su escritura a un árbol temporal/fixture con los insumos necesarios. Mantener la aserción sustantiva de que la demanda se aplica correctamente; no limitarse a ocultar o revertir el efecto después del test.

Comprobar hashes/status antes y después del test y su invocación desde T32: los archivos de trabajo permanecen intactos, incluyendo cambios previos legítimos. No “solucionar” el problema con `git checkout`, limpieza global o mock que impida probar la escritura real en el fixture. Cerrar NC-0141 tras integración y prueba.

## Fase 2 · Detectar L0 duplicada

Reutilizar la regla de unicidad que exige `cierre_acto.py`; agregar aserción dirigida en la suite vigente. Fixture con un ancla, duplicada y ausente. Debe detectar duplicación aunque las cifras coincidan y no generar un falso fallo por una cita histórica literal. No reordenar anotaciones ni normalizar canon completo. Cerrar NC-0148 con el test integrado.

## Fase 3 · Completar fuente en las tres vistas

Extender mínimamente la derivación de `corridas.tsv`, `resultados.tsv` y `usos.tsv` para identificar el comprobante/fuente de replay correspondiente. Revisar cabeceras y consumidores antes de añadir columnas; usar nombres compatibles elegidos contra el código actual. No inventar la misma fuente para todo.

Para un uso/resultados de varias procedencias, mantener la correspondencia a su corrida/evidencia sin atribuir una verificación conjunta inexistente. Distinguir evidencia histórica heredada, verify real y dato no verificable con las categorías vigentes. `registro --fuentes` impreso no satisface por sí solo la columna persistida exigida por NC-0104.

Pruebas con un comprobante real simulado por fixture, uno heredado y uno ausente; coherencia entre las tres vistas y consumidores. El fixture prueba el aparato, no la ejecución histórica.

## Fase 4 · Comprobante real en CLI y publicación controlada

Elegir una corrida con corpus disponible, preferentemente una nueva del lote 01/03/04/05. Si esas aún no existen, usar una sellada y verificable sin recalcularla. Enumerar su ID exacto y alcance antes de ejecutar. Obtener VERIFY-ESTRUCTURADO mediante el mecanismo existente, fecha/entorno, insumos y ambos ejes; persistir el comprobante sin fingir que ya estaba archivado.

Derivar primero en seco con `registro --fuentes`; inspeccionar las transiciones. Publicar vistas sólo con un lote explícito y razones para las corridas cuya transición está autorizada en este encargo. La adición de una columna no autoriza degradar el replay de otras 35 corridas. Si faltan insumos ajenos, conservar el veredicto respaldado según el mecanismo vigente o dejar pendiente la publicación incompatible; no usar `--force` ni ampliar el lote para silenciar la compuerta.

Si una transición ajena requiere adjudicación, entregar tabla concreta: ID, antes/después, input, hash y causa. Continuar las piezas de test ya completas; no inventar nuevas decisiones sobre resultados por cerrar el trámite.

## Fase 5 · Cierre con dos requisitos satisfechos

NC-0104 requiere tanto comprobante real como fuente/derivación efectiva de las tres vistas. Si sólo uno está cubierto, conservar el otro sin volver a pedir firma de contador. Citar #682/#683 como antecedentes resueltos y no reabrir NC-0140/0145.

Entregar PR y tabla de los tres NC. Las fases 1/2 pueden integrarse primero si la prueba de caja tarda, con residual de ejecución explícito; no bloquear otros cálculos por el estado de una vista que no usan para su resultado.

**D-14, tres piezas:** escritura accidental de la suite → puede colar datos ajenos en PR → fixture temporal más barato que respaldar/restaurar a mano en cada acto; duplicado L0 → abortó una cascada → una aserción reutiliza una regla existente; fuente de replay incompleta → confunde evidencia heredada con verificación actual → derivar columnas del registro existente evita conciliación manual. No nuevo registro paralelo.

## Contrato de ejecución incluido en este encargo

Este archivo es autocontenido. Su fuente de autoridad es la instrucción de mesa registrada en `forense/encargos/2026-09-10-MESA-CONCILIACION-E01.md` y la solicitud posterior: «dame los siguientes encargos, multi encargos, multifase, para correr en codex cloud o codex cli». E01 y el diagnóstico #684 ya están fusionados: no repetirlos.

**Alcance del despacho:** implementar las fases autorizadas, hacer commits y presentar el resultado en una rama/PR propios para revisión. El merge pertenece a mesa. No ejecutar otro encargo, hacer merges automáticos ni cerrar PR ajenos. Si la plataforma publica el PR por una acción propia, preparar la rama y el contenido para esa misma entrega; no duplicar el PR.

**Arranque obligatorio y corto:** informar ruta absoluta, rama, HEAD y `git status --short`; leer `AGENTS.md` y este archivo; consultar origin/main y PR/rama con el mismo objeto. Reutilizar o continuar el trabajo compatible. Usar un worktree propio, sin limpiar ni cambiar la rama de otra ejecución. Archivar este encargo por 0-bis A.3 antes de modificar el objeto. Las rutas aquí son las verificadas al corte: resolver renombres y colisiones sin reconstruir toda la historia.

**Fases:** avanzar a la siguiente cuando se cumpla su compuerta objetiva; no pedir confirmación entre fases ya autorizadas. Si una depende de caja, credenciales personales, datos ausentes o una decisión científica no tomada, completar el resto y entregar el punto exacto de continuación. No llamar “terminado” al encargo entero si sólo quedó preparado en Cloud. El destino depende de capacidades comprobadas, no del nombre del producto.

**Perímetro administrativo común:** archivo de este encargo, nota de cierre, sus filas FP/NC/cola, referencias de decisiones y cascada vigente en `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_12.md` y `canon/registro-rotulos.tsv`. Cada sección añade archivos sustantivos. Conservar los IDs históricos E02–E11 como antecedentes y apuntarlos al lote correspondiente; no crear una segunda obligación por cambiar el nombre del encargo.

**Cambios concurrentes:** el perímetro es propio aunque otros lotes avancen. Antes de integrar, actualizar con main y reconciliar sólo colisiones de IDs, registros y archivos compartidos del propio acto. No copiar una versión antigua del TSV completo. No relajar el candado del despacho automático. Las entradas congeladas de un experimento se resuelven por versión/hash aunque el árbol avance.

**Medición:** reutilizar resultados sellados cuando coincidan estimando e insumos; para un cálculo nuevo, congelar spec y método en un commit anterior al primer resultado. Resolver datos por manifiesto/raíz configurada; no inventar `/home/...`, no subir microdatos restringidos ni credenciales. Registrar unidad, universo, ponderador, exclusiones, incertidumbre y uso. Los cambios a código usado por un sello exigen preservar su reproducción por la vía existente o crear una sucesora explícita; no romper históricos para modernizar una herramienta.

## CONSUMIDO

Consumido por PR #690, rama `acto/gen2-pruebas-replay`.

- Fases 1 y 2 completas: escritura confinada al fixture temporal; guard de unicidad L0 integrado y probado.
- Fase 3 completa en derivador y fixtures: `fuente_replay` conserva correspondencia en corridas, resultados y usos.
- Fase 4 parcial por compuerta efectiva: `CALC-ENVIPE-0001` verificó 39/39 con contexto idéntico y dejó comprobante `VERIFY-ESTRUCTURADO`; la publicación del lote explícito se negó antes de escribir por 64 transiciones de 32 corridas ajenas. Las vistas conservaron sus hashes.
- `NC-0141` y `NC-0148` cerradas. `NC-0104` permanece abierta hasta publicar efectivamente la fuente en las tres vistas; tabla exacta y continuidad en `forense/notas/2026-09-10-GEN2-PRUEBAS-LIMPIAS-Y-REPLAY-cierre.md`.
- Reserva administrativa: candidato `ADR-455` en colisión declarada con PR #687; quien fusione segundo renumera contra `main`.

**Objeto de firma al merge:** propagación de las decisiones de mesa citadas y de los resultados del encargo. Para CALC científicos nuevos, aplicar `cuenta_gen2=SI` con objeto y cita explícitos conforme al contrato vigente; los sucesores técnicos no inflan mediciones independientes. Contar no equivale a adoptar: sólo se activa en el motor lo autorizado por la decisión concreta y sustentado por su evidencia.

**Pruebas y cierre:** validar primero el riesgo material; ejecutar el gate requerido sobre la integración, sin limpiar deuda ajena ni cambiar baseline. Revisar `git diff` después de las pruebas; nunca incorporar con `git add -A` una derivación accidental. Mientras NC-0141 siga viva, registrar y preservar cualquier cambio previo del usuario antes de aislar efectos de la suite; no restaurar a ciegas sobre trabajo ajeno.

Cada fase termina con resultado o bloqueo preciso y prueba. Cierre completo: autorización → resultado/cambio → evidencia → consumidor, si aplica → FP/NC → vistas/cola → PR y merge. Una decisión firmada no cierra una ejecución pendiente. Registrar fecha real, cita y universo; nada se borra ni se rejuvenece por traslado. Si falta una pieza, usar el vocabulario vigente y sucesor concreto.

**Formato final del ejecutor:** resultado útil en cinco líneas; fases realizadas/pendientes; PR y SHA; pruebas; tabla `obligación | evidencia | cerrada/residual | siguiente acción`. No parar en un inventario cuando el entorno permite ejecutar. No continuar por inercia después de satisfacer el resultado.
