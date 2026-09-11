<!--
SHA de redacción: 486eda19944a94d978791eb423559144de98d16b
Entorno asignado: Cloud; CLI sólo para nuevos estimadores que requieran microdatos
Estado: CONSUMIDO
Fuente verbatim: forense/encargos/cola/2026-09-10-GEN2-POST-685/02-GEN2-MOTOR-USOS-Y-COMPLEMENTOS.md
sha256 del cuerpo: 4c589782f6c062e1437999afa0ee299d0127184ca7c7a4a4f69fa86885ab2f94
-->

# ENCARGO · GEN2-MOTOR-USOS-Y-COMPLEMENTOS

## Uso de parámetros → semántica → integración verificable

Fecha de preparación: 10 de septiembre de 2026. Corte verificado: `486eda19944a94d978791eb423559144de98d16b` (merge de #685).

**Destino:** Cloud para trazado, cambios documentales/código y pruebas; CLI sólo para nuevos estimadores que requieran microdatos. **Integra:** E04 + aplicación D11 de E11; D03/D06/D07/D08/D09/D10/D11. **Rama:** `acto/gen2-motor-usos`.

## Resultado que se exige

Que cada parámetro opere sobre la población y el evento que realmente mide. Entregar cambios utilizables en los consumidores autorizados y una propuesta concreta donde aún falte decisión; no una renombrada general ni otro inventario de todas las reglas.

**Observado:** #685 asentó estas decisiones; quedan NC-0137/0138/0139, NC-0127/0107/0111/0105/0121/0122 y NC-0085 con ejecución pendiente. **Consecuencia:** leer sus consumidores, no volver a pedir las mismas firmas.

## Entradas y perímetro sustantivo

Leer las filas citadas, usos/resultados de corrida0, `milpa/tramite.yaml`, `milpa/procedencia.yaml`, las entradas pertinentes de `milpa/tramite-ola5-propuesta-v0.yaml` y el código que las consume; cuestionarios/specs ENCUCI, ENCIG, ENIF y ENIGH relacionados. Leer `forense/notas/BENCHMARK-D11-COMPLEMENTOS-Y-USO-EN-MOTOR.md`.

Editar sólo los consumidores localizados de RES-0005/0006, tasas deduplicadas, proxy fintech, desconfianza/mal servicio, procedencia ENIGH y RES-0028, además de sus pruebas/specs sucesoras. Enumerar rutas exactas en P0. No editar los snapshots M/R de la tríada ni reescribir sellos. Coordinar la adopción ENIF A/A con lote 03: este lote es dueño de etiqueta/uso; el 03, de cálculo/adopción del nuevo dominio.

## Fase 0 · Derivar el mapa de uso

Para cada objeto: activador → dominio elegible → evento/resultado → parámetro → consumidor. Encontrar llamadas reales y pruebas; no asumir que una variable de un YAML ya está conectada al motor. Identificar tasas sin consumidor y consumidor sin respaldo, sólo en este perímetro.

## Fase 1 · Propagar las decisiones inequívocas

Aplicar “desconfianza o mal servicio”; preservar alias si hay compatibilidad. Limitar ENCIG al grupo observado. Usar el proxy fintech sólo como canal del último producto entre personas con fintech. Recuperar fuente/ola por conducta ENIGH: si el linaje es ambiguo, conservar la ambigüedad; no fabricar una media multianual.

Mantener sin adopción las dos tasas deduplicadas discrepantes de D07. Usar variantes validadas sólo si coincide la unidad. Si ello deja una función necesaria sin parámetro, proponer deduplicación prospectiva por unidad/evento y ejecutarla si la definición queda determinada por el instrumento y el uso autorizado; no buscar el desempate que reproduzca el número viejo.

## Fase 2 · Solicitud y entrega en ENCUCI

Separar en el diseño del motor solicitud S, entrega E y unión cuando correspondan a transiciones distintas. P(E) no es P(S), P(E|S) ni 1−P(S). No multiplicar dos marginales para fabricar la conjunta.

Derivar del punto de activación si se necesita probabilidad entre contactos o carga poblacional. La segunda exige modelar exposición. Conservar las cuatro combinaciones S/E posibles y los faltantes según cuestionario; no imponer E⊆S por intuición. Un Sí en uno de los componentes puede definir la unión pese a que el otro falte; dos valores indeterminados no son No.

Si el repo y el uso determinan la elección, implementar la separación con nombres y pruebas precisos. Si queda una elección sustantiva de población, evento o no respuesta sin autoridad, preparar las variantes y una pregunta de mesa en lenguaje claro, con impacto cuantificado si hay datos. No activar una nueva tasa bajo un “A/A/A” que mesa nunca dictó; continuar F1 y F3.

## Fase 3 · Aplicar D11 al complemento exacto

Reconstruir el padre, códigos incluidos/excluidos y universo de RES-0028. Verificar si “otra razón” coincide con una categoría del cuestionario o significa “resto de este recorte”. Propagar dependencia: q=1−p; por réplica, q[b]=1−p[b]; no dos draws independientes. Para una partición de varias categorías, conservar sus covarianzas.

No repetir el benchmark: ya está registrado. Entregar ficha exacta con fórmula, universo, incertidumbre y consumidor. D11 autorizó investigación/aplicación propuesta, no la firma final de adopción de este objeto. Mantener NC-0085 abierta en el residual que corresponda hasta esa firma y propagación.

## Fase 4 · Pruebas del comportamiento y entrega

Fixtures: no contacto; solicitud sin entrega; entrega sin solicitud; ambas; faltantes lógicos; cambio de universo; complemento con suma uno; dos consumidores que comparten padre. Verificar que el motor no aplica una tasa condicional fuera de su dominio ni cuenta dos confirmaciones por un complemento. Comparar resultado del flujo afectado antes/después; no exigir suite de todo el motor por un cambio de etiqueta.

Entregar PR con componentes completos y reservas separadas. Añadir demanda exacta de tasa general ENCIG al mecanismo vigente y remitir al lote 06; no llamar adquisición a esa inscripción. Cerrar NC únicamente por consumidor efectivamente corregido. No bloquear todas las mejoras por D03 o D11 si sólo una adopción concreta espera mesa.

**D-14 si se añade derivación:** defecto real: confusión solicitud/entrega y dominio documentada; materialidad: cambia decisiones simuladas; costo: reutilizar el cálculo y probar el punto de uso evita correcciones manuales repetidas. No crear una capa general de indicadores.

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

## NO-CORRIDO / RESERVAS

- `NC-0085`: la adopción final de RES-0028 requiere firma de mesa.
- `NC-0107`: las dos tasas ENCIG deduplicadas discrepantes siguen sin adopción.
- `NC-0111` y `NC-0152`: falta una tasa general ENCIG con denominador general.
- `NC-0121`/`NC-0122`: no se fabricó serie fintech ni canal exacto de producto.
- El merge y la eventual renumeración por la colisión de `ADR-455` son de mesa.

## CONSUMIDO

Ejecutado en la rama `acto/gen2-motor-usos` y presentado para revisión en
PR #689. Commits de ejecución: `6134100` y `9263d2d`; el archivo fue archivado
antes del objeto en `c655c65`. Resultado y residuales:
`forense/notas/2026-09-10-GEN2-MOTOR-USOS-Y-COMPLEMENTOS-cierre.md`.
El merge y la reconciliación de la colisión declarada de `ADR-455` con PR #687
pertenecen a mesa.
