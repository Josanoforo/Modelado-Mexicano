# ADENDA-1 · ACTO GEN2-PENDIENTES-4 · Firma de mesa del 28/sep/2026 y bloque de arranque que la sesión ejecuta sin preguntar

Archivo propio, sellado al recibirse (A.3). No modifica el cuerpo del encargo.

## Firma de mesa — verbatim
Mesa, 28/sep/2026, chat de dirección (maestra 54), en respuesta al encargo y a la frase «autorizas cerrar por diseño lo GEN1 o retirado, y que el acto redacte los encargos como propuestos en cola»: **«Ok con pendientes 4»**.

## INTERPRETACIÓN-DECLARADA (cláusula v1.0 §2)
«Ok» firma las dos autorizaciones tal como el encargo las pide en §2: (a) el acto **cierra por diseño, con cita**, toda NC cuyo objeto sea GEN1 (E.1), un procedimiento retirado por regla 6 (duelo v2 sin camino de emisión, θ, motor legacy), un archivo que ya no existe, o un producto que otro acto ya entregó en main; (b) el acto **redacta los encargos** que las NC «encargo por escribir» piden, agrupados en lotes robustos, plantilla v2.2 completa, archivados como PROPUESTOS-POR-EJECUTOR en `forense/encargos/cola/PROPUESTOS/`, y pone cada NC absorbida con `sucesor = <ese encargo>`; dirección los revisa y mesa los lanza. Sigue vigente la delegación firmada en PENDIENTES-3 (decidir lo reversible; solo lo irreversible vuelve con opciones) y la regla nueva A.14 (cierre hacia atrás; rutas solo con sucesor archivado).

## Bloque de arranque de firmas y premisas (lo hace la sesión, no dirección)
Cada firma citada en §2 del encargo la re-verificas por id contra `forense/firmas-pendientes.tsv` y `forense/analisis/hoja-firmas-21/decisiones-21.tsv` (A.17): FIRMADA → ejecutas; ABIERTA o inexistente → esa pieza nace `NO-LANZADO (firma X)` con el texto de firma listo en la hoja de cierre, y sigues. Cada premisa de §3 la re-derivas por comando: si cae una de logística, replanteas y sigues; si cae una de qué se mide o una firma, PARA solo esa pieza. **No preguntas en el chat**: toda bifurcación reversible la decides y la declaras en `decididas-por-delegacion.tsv` de este acto; toda irreversible va a la hoja de cierre con opciones y texto de firma. Las acciones con identidad de mesa (correos, registros, convenios, `.ots`, publicación) no son piezas: dejas la receta de un minuto y las listas en la hoja de recetas.

## Adjunto
`PENDIENTES-PROGRAMA__5_.md` (inventario v5 de la conversación de tablero): el acto lo archiva verbatim con el sha que calcule al recibirlo, en `forense/analisis/pendientes-4/`.
