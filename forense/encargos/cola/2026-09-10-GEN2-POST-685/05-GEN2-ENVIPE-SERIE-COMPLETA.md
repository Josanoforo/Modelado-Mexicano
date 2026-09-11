# ENCARGO · GEN2-ENVIPE-SERIE-COMPLETA

## Insumos → comparabilidad → serie temporal

Fecha de preparación: 10 de septiembre de 2026. Corte verificado: `486eda19944a94d978791eb423559144de98d16b` (merge de #685).

**Destino:** CLI con microdatos. Cloud prepara correspondencias y código cuando sólo dispone de documentos. **Integra:** E08; D12; NC-0087/0093/0101. **Rama:** `acto/gen2-envipe-serie`.

## Resultado y perímetro

Completar la serie temporal de denuncia con todas las olas comparables y disponibles. Donde falte dato adquirible, adquirirlo; donde cambie el instrumento, mostrar la ruptura. No llenar huecos con interpolaciones presentadas como encuesta.

Leer NC-0101 y su listado, `data/manifiesto.yaml`, `data/corrida0/CALC-ENVIPE-0001/`, los CALC-R CIV pertinentes como referencias, specs/medidores ENVIPE existentes y `tools/ya_medido.py`. Puede crear specs/medidores/resultados de olas pendientes, correspondencia temporal y producto de serie; no modifica R congelados de la tríada.

## Fase 0 · Censo corto por ola y conducta

NC-0101 enumera 2011/2014/2016/2017/2018/2019/2020/2022. Contrastar esa lista con lo efectivamente medido y el manifiesto actual. Para cada pendiente: archivo exacto/hash, legibilidad, cuestionario/diccionario, variable, año de encuesta y año del hecho, unidad, ponderador, diseño y consumidor.

La serie de denuncia y los árbitros de razones de no denuncia no son automáticamente el mismo estimando. Comprobar cada correspondencia antes de reusar un RESULT. Integrar NC-0093 (2022) en este mismo trabajo, sin duplicar obligación.

## Fase 1 · Resolver insumos y correspondencia conceptual

Usar primero el corpus ya adquirido. Ejecutar descarga directa de faltantes públicos por la receta vigente o coordinar la demanda con lote 06; no competir por descargar el mismo objeto. Verificar bytes y contenido, no sólo URL exitosa.

Tabular por ola los códigos/saltos y decidir comparabilidad conceptual del mismo evento. Separar unidad persona, delito y trámite. Un mismo nombre de variable no demuestra mismo significado; cambios de códigos no siempre significan ruptura. Mostrar NS/NR y exclusiones por año.

**Compuerta:** existe una definición defendible por tramo de serie y suficientes insumos. Una ola bloqueada no impide medir las demás. Dejar los datos inaccesibles en su demanda exacta y continuar.

## Fase 2 · Congelar y ejecutar el lote de cálculos

Congelar specs por ola/tramo y medidor antes de producir resultados nuevos. Reutilizar funciones existentes con adaptaciones pequeñas a DBF/CSV; conservar implementaciones históricas donde un sello las requiere. Ejecutar cada ola con preflight/run/verify y manifiesto.

Controles: codificación en los años que cambian; denominadores válidos; pesos/unidad; fuente de diseño; punto de control existente donde el estimando coincida; ausencia de multiplicación de registros. No abrir una auditoría general de todas las olas ya medidas.

## Fase 3 · Producir la serie y explicar qué cambió

Entregar tabla de tasas/intervalos, cobertura, unidad y año de referencia; marcar rupturas de comparabilidad y huecos reales. Puede producir una figura derivada de esa tabla para lectura, sin ocultar cambios de universo. No atribuir causalidad a una tendencia ni promediar años con criterios elegidos después de observarla.

Conectar la serie al consumidor que la solicitó, con fuente por ola. Si eso cambia una regla cuantitativa o modulación del motor todavía no aprobada, entregar el producto disponible y la propuesta concreta, sin sustituir la regla silenciosamente. D12 autoriza la serie; no abre el cruce denuncia/seguro de NC-0088.

## Fase 4 · Cierre por ola

Cerrar NC-0087/0093/0101 según el objeto realmente cubierto. Si una fila agrupa olas, conservar las restantes con sus identidades y causas. Entregar comprobantes estructurados de los CALC nuevos para lote 08; no rederivar vistas globales pisando replay ajeno.

**D-14 para un adaptador por olas, si hace falta:** defecto real: huecos de cálculo e incompatibilidad de formatos/códigos documentados; materialidad: una serie con denominadores distintos puede mostrar tendencias falsas; menor costo: parametrizar el medidor existente evita copiar cálculos manuales por cada año. Sin generalizar a todas las encuestas.

## Contrato de ejecución incluido en este encargo

Este archivo es autocontenido. Su fuente de autoridad es la instrucción de mesa registrada en `forense/encargos/2026-09-10-MESA-CONCILIACION-E01.md` y la solicitud posterior: «dame los siguientes encargos, multi encargos, multifase, para correr en codex cloud o codex cli». E01 y el diagnóstico #684 ya están fusionados: no repetirlos.

**Alcance del despacho:** implementar las fases autorizadas, hacer commits y presentar el resultado en una rama/PR propios para revisión. El merge pertenece a mesa. No ejecutar otro encargo, hacer merges automáticos ni cerrar PR ajenos. Si la plataforma publica el PR por una acción propia, preparar la rama y el contenido para esa misma entrega; no duplicar el PR.

**Arranque obligatorio y corto:** informar ruta absoluta, rama, HEAD y `git status --short`; leer `AGENTS.md` y este archivo; consultar origin/main y PR/rama con el mismo objeto. Reutilizar o continuar el trabajo compatible. Usar un worktree propio, sin limpiar ni cambiar la rama de otra ejecución. Archivar este encargo por 0-bis A.3 antes de modificar el objeto. Las rutas aquí son las verificadas al corte: resolver renombres y colisiones sin reconstruir toda la historia.

**Fases:** avanzar a la siguiente cuando se cumpla su compuerta objetiva; no pedir confirmación entre fases ya autorizadas. Si una depende de caja, credenciales personales, datos ausentes o una decisión científica no tomada, completar el resto y entregar el punto exacto de continuación. No llamar “terminado” al encargo entero si sólo quedó preparado en Cloud. El destino depende de capacidades comprobadas, no del nombre del producto.

**Perímetro administrativo común:** archivo de este encargo, nota de cierre, sus filas FP/NC/cola, referencias de decisiones y cascada vigente en `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_12.md` y `canon/registro-rotulos.tsv`. Cada sección añade archivos sustantivos. Conservar los IDs históricos E02–E11 como antecedentes y apuntarlos al lote correspondiente; no crear una segunda obligación por cambiar el nombre del encargo.

**Cambios concurrentes:** el perímetro es propio aunque otros lotes avancen. Antes de integrar, actualizar con main y reconciliar sólo colisiones de IDs, registros y archivos compartidos del propio acto. No copiar una versión antigua del TSV completo. No relajar el candado del despacho automático. Las entradas congeladas de un experimento se resuelven por versión/hash aunque el árbol avance.

**Medición:** reutilizar resultados sellados cuando coincidan estimando e insumos; para un cálculo nuevo, congelar spec y método en un commit anterior al primer resultado. Resolver datos por manifiesto/raíz configurada; no inventar `/home/...`, no subir microdatos restringidos ni credenciales. Registrar unidad, universo, ponderador, exclusiones, incertidumbre y uso. Los cambios a código usado por un sello exigen preservar su reproducción por la vía existente o crear una sucesora explícita; no romper históricos para modernizar una herramienta.

**Objeto de firma al merge:** propagación de las decisiones de mesa citadas y de los resultados del encargo. Para CALC científicos nuevos, aplicar `cuenta_gen2=SI` con objeto y cita explícitos conforme al contrato vigente; los sucesores técnicos no inflan mediciones independientes. Contar no equivale a adoptar: sólo se activa en el motor lo autorizado por la decisión concreta y sustentado por su evidencia.

**Pruebas y cierre:** validar primero el riesgo material; ejecutar el gate requerido sobre la integración, sin limpiar deuda ajena ni cambiar baseline. Revisar `git diff` después de las pruebas; nunca incorporar con `git add -A` una derivación accidental. Mientras NC-0141 siga viva, registrar y preservar cualquier cambio previo del usuario antes de aislar efectos de la suite; no restaurar a ciegas sobre trabajo ajeno.

Cada fase termina con resultado o bloqueo preciso y prueba. Cierre completo: autorización → resultado/cambio → evidencia → consumidor, si aplica → FP/NC → vistas/cola → PR y merge. Una decisión firmada no cierra una ejecución pendiente. Registrar fecha real, cita y universo; nada se borra ni se rejuvenece por traslado. Si falta una pieza, usar el vocabulario vigente y sucesor concreto.

**Formato final del ejecutor:** resultado útil en cinco líneas; fases realizadas/pendientes; PR y SHA; pruebas; tabla `obligación | evidencia | cerrada/residual | siguiente acción`. No parar en un inventario cuando el entorno permite ejecutar. No continuar por inercia después de satisfacer el resultado.

---

## Bloque de archivo (0-bis A.3) — ejecución

| | |
|---|---|
| **SHA256 del encargo recibido** | `19fb659c6e51ced9ca963c4578795282b7d64f5408d3b61c1869ddc3e665a403` — coincide byte a byte con este archivo ya encolado por `PR #686` |
| **Base real de arranque** | `44134745ce7f19af18a87b153a99de3d506063b0` (`origin/main`, 10/sep/2026) |
| **Worktree** | `/home/pc0/mm-gen2-envipe-serie` |
| **Rama** | `acto/gen2-envipe-serie` |
| **Entorno** | CAJA (Ubuntu/WSL2), `data/raw` montado; 401 archivos examinados por `tools/entorno.py` |
| **Estado** | CERRADO — serie 15/15 publicada; cierre en `forense/notas/2026-09-10-GEN2-ENVIPE-SERIE-COMPLETA-cierre.md` |

## NO-CORRIDO / RESERVAS

- `NC-0153`: validación independiente de los ocho puntos nuevos, sin reutilizar la función decisiva del adaptador común.
- No se adoptó ni recalibró ninguna regla del motor; D12 autoriza el producto de serie, no su activación silenciosa.
- Tras integrar `origin/main`, el guardián `NC-0094` impidió rederivar de nuevo las vistas porque habría movido replay de 32 corridas ajenas. Se conservaron las vistas ya escritas por este lote y los ocho asientos `VERIFY-ESTRUCTURADO`.

## CONSUMIDO

Ejecutado por `ACTO GEN2-ENVIPE-SERIE-COMPLETA`: ocho olas nuevas selladas y reproducibles, producto anual 2010–2024 publicado, `NC-0087/0093/0101` cerradas y validación independiente conservada en `NC-0153`. El merge y cualquier adopción pertenecen a mesa.
