ESTADO: CONSUMIDO — PR #688; S6 v1.4, S12 v1.2, S13 v1.1 y
`CALC-0001-v2` entregados; NC-0065/0064/0043 cerradas.

BITÁCORA: ejecución y cierre en
`forense/encargos/2026-09-10-GEN2-S6-S12-S13-SUCESORAS.md` y
`forense/notas/2026-09-10-GEN2-SOCIALES-SUCESORAS-cierre.md`.

──── CUERPO VERBATIM RECIBIDO DE DIRECCIÓN ────

# ENCARGO · GEN2-S6-S12-S13-SUCESORAS

## Documentar llave → medir receptores → acotar historia

Fecha de preparación: 10 de septiembre de 2026. Corte verificado: `486eda19944a94d978791eb423559144de98d16b` (merge de #685).

**Destino:** CLI recomendado para completar las tres piezas. Cloud ejecuta documentación y preparación; continúa en CLI para S12. **Integra:** E06 + E07; D13/D14/D15; NC-0065/0064/0043. FP-361 y FP-363 ya están firmadas. **Rama:** `acto/gen2-sociales-sucesoras`.

## Resultado y perímetro

Tres entregables acotados de la familia de specs: S6 con llave de hogar explícita, S12 con la nueva comparación entre receptores y S13/R10.3 con la cláusula histórica correctamente limitada. No repetir firmas ni encargar un diagnóstico general de salud/política/comunicación.

Leer `forense/prereg-caja/S6-L16-spec-v1_3.md`, `S12-CSES-spec-v1_1.md`, `S13-R10-3-spec-v1_0.md`, `data/corrida0/CALC-0003-v4/`, las filas NC/FP y los consumidores concretos. Puede editar sólo sucesoras de estas specs, sus referencias/consumidores y el nuevo CALC S12 con sus pruebas. Preservar todas las specs selladas y hashes históricos.

## Fase 1 · S6: publicar el procedimiento ya probado

Crear S6 v1.4 si la ranura sigue libre; en caso contrario, verificar si la sucesora ya cumple el objeto. Documentar `folio`, enlace hacia c_portad, cardinalidad, cobertura y faltantes de estrato/localidad usados por v4. Referenciar la evidencia del join, no repetir el cálculo sólo por añadir la tabla.

**Aceptación:** un ejecutor puede reconstruir el enlace correcto desde la spec, sin inferir una llave por nombre. NC-0065 cierra por entrega documental efectiva. El cambio no resuelve otras reservas de salud o reponderación que pertenecen a FP-332.

## Fase 2 · S13: corregir la cláusula con alcance temporal

Conservar evidencia de 2004 y el estatus vigente de R10.3. Registrar la ausencia del desenlace requerido en las olas 2019/2021/2023 ya examinadas. Esas fuentes no permiten repetir la batería original. No llamar inexistente al dato en toda fuente posible, ni cambiar FUERTE/MEDIA por cuenta propia.

Definir el disparador concreto de reexamen: fuente nueva que mida la pregunta original o decisión explícita sobre otro estimando. No reabrir la misma búsqueda cada día ni reactivar por simple envejecimiento. Corregir la referencia del consumidor y cerrar NC-0043 por decisión de alcance ejecutada, sin afirmar réplica.

## Fase 3 · S12: congelar la nueva pregunta

Dentro de receptores de oferta/amenaza, comparar alineados y no alineados según variables disponibles. Definir población, exposición/clasificación, desenlace, ventana, ponderador, diseño, faltantes y soporte antes del cálculo. Consultar etiquetas y saltos reales; no inventar variables.

La pregunta es descriptiva/asociativa. Condicionar a receptores puede introducir selección: no identifica el efecto causal de recibir oferta/amenaza ni responde a la comparación original que no era estimable. Mantener aquel resultado histórico.

**Compuerta:** ambos grupos y desenlace existen, están definidos y tienen soporte. Si falta un insumo adquirible, registrar demanda hacia lote 06 y completar F1/F2. Falta de datos no autoriza sustituir el desenlace.

## Fase 4 · Calcular S12 y propagar

Crear CALC sucesor con spec congelada, ejecución y verify. Reportar tamaños brutos/ponderados, contraste, intervalo y límites por grupo. Comprobar por una vía independiente el numerador/denominador decisivo; no duplicar una función para llamarla validación independiente.

Cerrar NC-0064 cuando exista resultado o imposibilidad acreditada con el tratamiento acordado; una FP firmada no significa cálculo realizado. Entregar las tres piezas por separado en la tabla de cierre. Si Cloud completó dos de tres, puede publicar un PR parcial con ese alcance y transferencia precisa a CLI; no marcar todo CONSUMIDO.

**Límite:** no incorpora nuevas tasas al motor salvo uso específicamente autorizado y sustentado; un hallazgo asociativo no crea una regla causal. No se necesita infraestructura adicional: utilizar specs, CALC y registro existentes.

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
