# ENCARGO · GEN2-ADQUISICION-DIRIGIDA-Y-DIN

## Accesos → tandas académicas → diseño de DIN

Fecha de preparación: 10 de septiembre de 2026. Corte verificado: `486eda19944a94d978791eb423559144de98d16b` (merge de #685).

**Destino:** Cloud para búsqueda pública, documentación y solicitudes preparadas; CLI para raíces locales, archivos grandes/restringidos y medición. **Integra:** E09 + aplicación D16 de E11; D08/D12/D16/D17/D18; NC-0151 y residuales de acceso. **Rama:** `acto/gen2-adquisicion-dirigida`.

## Resultado y perímetro

Entregar datos/documentos que desbloqueen mediciones, una búsqueda académica dirigida de tandas y una recomendación concreta para la incertidumbre de DIN-M-01. No otro censo general de fuentes ni repetición de los benchmarks D11/D16 ya archivados.

Leer NC-0151, FP-314/286/343/371, demandas de los otros lotes, `data/manifiesto.yaml`, cola y recetas vigentes, `tools/vista_cola_adquisicion.py`, `tools/curador_registro/registra_cola_adquisicion.py`, `data/corrida0/CALC-R-DIN-M-01-v4/` y el benchmark D16 de `forense/notas/`. Editar sólo demandas/recetas/recibos/manifiesto correspondientes, informes académicos y preparación/cálculo sucesor de diseño si se obtiene. No cambiar scheduler (lote 07) ni adoptar aproximaciones sin firma.

## Fase 0 · Evitar duplicados y fijar utilidad

Por objeto: pregunta/consumidor, identificador exacto, encuesta/ola, contenido ya disponible, vía intentada, barrera y siguiente acción. Un título parecido no satisface el objeto exacto. Prioridad: bloqueos de la evaluación y cálculos autorizados, luego cartera de acceso.

Verificar WBES México 2023 contra lo ya adquirido. Para ENAFIN/Findex individuales, buscar el reactivo requerido y comprobar si el objetivo ya está cubierto: no convertir una receta antigua en bloqueo general. “No encontrado” incluye el universo y consultas examinadas; no equivale a inexistencia mundial.

## Fase 1 · Ejecutar adquisiciones y preparar accesos personales

Cartera: fuentes elegibles para F5; tasa general de corrupción que ENCIG actual no identifica; insumos faltantes de la serie ENVIPE; OCDE Trust; ICPSR 35024; Reuters DNR individual; ENJUVE vía IMJUVE; SSRN 2474620 exacto y pendientes válidos de FP-314.

Realizar descargas públicas autorizadas y verificar lectura, variables, período, unidad y condiciones de uso. Reusar borradores/recetas existentes. Cuando una solicitud exige identidad, firma de DUA o aceptación personal, completar todo el expediente y dejar la acción puntual al titular; no suplantar ni registrar envío sin comprobante. No realizar compra ni negociación comercial de tandas. Las comunicaciones externas siguen la autorización específica vigente; este encargo no inventa destinatarios ni condiciones contractuales.

Ante fallo: uno o dos intentos razonables, alternativa directa y registro de causa; no tormenta de reintentos. Un bloqueo de una fuente no para la cartera. Un acceso concedido no significa que el microdato ya llegó ni que sea apto para el motor.

## Fase 2 · Búsqueda académica dirigida sobre tandas

Partir de autores/estudios y búsquedas ya documentados; seguir cadenas de citas y repositorios de datos. Buscar evidencia mexicana de reputación, incumplimiento, selección, sanciones, frecuencia y monto en ROSCA/tandas. Separar datos individuales, grupos, experimentos y descripciones cualitativas.

Entregar candidatos priorizados con pregunta respondible, población/año, variable exacta, acceso y paso de medición. Papers de participación no sustituyen tasa de incumplimiento; estudios de otro país pueden informar mecanismos, no calibrar México sin reserva. Identificar también descartes útiles para no repetirlos. No fijar una cuota de papers: terminar cuando haya una ruta medible o vías dirigidas agotadas documentadas.

## Fase 3 · Recuperar el diseño de DIN-M-01

Buscar en corpus y productor: estratos, UPM o variables públicas oficiales para varianza, peso de la ola/universo correcto, pesos replicados y método. Verificar relación de `cr27`, `fac_3b`, folio/persona y archivos de enlace contra la spec. Folio de hogar no prueba UPM de muestreo.

Si llega diseño acreditado, congelar un CALC sucesor: enlaces sin expansión accidental, cobertura de diseño, unidades por estrato, pesos y método de varianza. Comparar el punto con el anterior cuando el estimando sea idéntico, y cotejar la incertidumbre con una implementación de referencia del mismo diseño. Un nuevo R no reemplaza al R congelado del lote 01.

Si sólo hay aproximación, entregar sensibilidades justificadas y límites; no llamarla conservadora por eliminar varianza o usar un estrato constante. No inventar DEFF, UPM ni grados de libertad. FP-371 sigue pidiendo el uso inferencial concreto; no bloquear el punto descriptivo que ya está disponible.

## Fase 4 · Entregar al consumidor y cerrar por objeto

Recibo con URL/origen, fecha, objeto, hash, ruta configurada, legibilidad, licencia/condición y responsable de siguiente acción. Incorporar a manifiesto con herramienta vigente; archivos sensibles fuera de Git. Enviar al lote consumidor una referencia a ese recibo, no una copia divergente de la base.

Actualizar SONDA/cola con recetas útiles y motivos de descarte para que el próximo ciclo no redescubra lo agotado. NC-0151 puede quedar parcial si el acceso depende de un tercero; declarar cada pieza. La vía comercial diferida de D18 sólo se reexamina ante propuesta concreta y decisión de mesa. D16 investigación ya está cumplida; cerrar la aplicación sólo con evidencia y firma de uso correspondientes.

**D-14:** reutilizar adquisición/cola existentes. Sólo añadir derivación si un duplicado, pérdida de identidad o bloqueo observado lo exige; escribir defecto, efecto material y comparación de costo. No abrir un rastreador general de literatura ni un servicio nuevo.

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

- `NC-0037`: no apareció un ledger mexicano abierto de grupos, turnos y pagos;
  la ruta comercial permanece diferida por D18.
- `NC-0151`: DUA ICPSR, formulario OECD, solicitud Reuters, PNT ENJUVE y
  sesión para SSRN 2014 exigen identidad, firma o respuesta de tercero.
- `FP-371`: mesa aún debe aceptar o rechazar el uso inferencial concreto; el
  acto recomienda rechazar constante + `folio` como *ground truth*.

## CONSUMIDO

PR: `#693`, rama `acto/gen2-adquisicion-dirigida`, contra `main`. Ejecutado:
`ACTO GEN2-ADQUISICION-DIRIGIDA-Y-DIN` (`ADR-461`, renumerado al integrar
`origin/main` después de los PR #688/#690/#689/#691/#692). Tres documentos públicos
quedaron en `data_raw`, fuera de Git y registrados por manifiesto; se entregó
la ruta académica de tandas y el dictamen DIN, se actualizaron cola/FP/NC y se
preservaron los accesos personales como residuales. Contador: cero. **NO
fusionado por el ejecutor** — mesa revisa y fusiona.
