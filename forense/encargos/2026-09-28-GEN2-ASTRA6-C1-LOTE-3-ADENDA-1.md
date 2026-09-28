# ADENDA-1 · ACTO GEN2-ASTRA6-C1-LOTE-3 · Firmas de mesa de §2 (opción A del reconstructor y contrato v3 por sha) y forma de lanzamiento de la sesión reconstructora

Archivo propio, sellado al recibirse (A.3). No modifica el cuerpo del encargo. Recibida el 28/sep/2026, después del 0-bis `0c1f63e7`, en esta misma sesión (receptora), por la herramienta de preguntas a mesa: tres preguntas, tres respuestas. Las preguntas se copian con el texto que mesa tuvo delante; las respuestas, con la etiqueta que mesa eligió.

## 1 · Firma §a — `FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-02`

Pregunta: «Firma §a de la hoja de C1 (FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-02, ABIERTA en origin/main 16ba3d02; no hay ADENDA-1). Texto listo: «Autorizo el reconstructor de opción A para el lote 3 de C1: una sesión nueva de Claude Code, sin historial, con solo el prompt, el paquete y la lista cerrada de herramientas; transcript archivado y auditado». ¿Firmas?»

Respuesta de mesa: **«Firmo A verbatim»**.

Texto firmado (el de §2 del encargo, verbatim): «Autorizo el reconstructor de opción A para el lote 3 de C1: una sesión nueva de Claude Code, sin historial, con solo el prompt, el paquete y la lista cerrada de herramientas; transcript archivado y auditado».

## 2 · Contrato v3 por sha — `FP-260928-GEN2-ASTRA-CONTINUIDAD-C1-1-26a2-01`

Pregunta: «Firma del contrato v3 por sha (FP 26a2-01, ABIERTA). Verifiqué en el árbol que sha256(CONTRATO-v3.md) = 821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb. Texto: «Mesa firma CONTRATO-v3.md con sha256 821a5ecb…94eb como contrato de estados de C1. Esta firma no acredita contexto nuevo ni autoriza acceso … Una corrección material se hace en una versión sucesora con sello nuevo.» ¿Firmas?»

Respuesta de mesa: **«Firmo v3 por sha»**.

Texto firmado (el completo de `forense/analisis/astra-continuidad-c1/hoja-mesa-c1-v1_0.md` §b, que la pregunta abreviaba con «…»): «Mesa firma CONTRATO-v3.md con sha256 821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb como contrato de estados de C1. Esta firma no acredita contexto nuevo ni autoriza acceso: cualquier C1 real exige además CONTEXTO-NUEVO-ACREDITADO y ACCESO-AUTORIZADO por paquete. Una corrección material se hace en una versión sucesora con sello nuevo.»

Comprobación de la receptora antes de preguntar: `sha256sum forense/validacion-independiente/catalogo-1-ejecutor-v3/CONTRATO-v3.md` → `821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb` sobre `16ba3d02`.

## 3 · Quién lanza la sesión reconstructora (latitud §6; preguntado porque cambia quién entrega)

Pregunta: «Cómo se crea la sesión reconstructora (el encargo dice «sesión nueva de Claude Code», Opus, dos transcripts). ¿Quién la lanza?» — opciones: «Yo, con claude -p» / «Tú la abres a mano».

Respuesta de mesa: **«Yo, con claude -p»** — la receptora lanza `claude -p` con modelo Opus, headless, desde un directorio aislado fuera del repo que solo contiene el paquete; lista cerrada de herramientas; sin memoria ni CLAUDE.md; la salida `stream-json` se archiva como transcript y se audita antes de abrir los sellados.

## INTERPRETACIÓN-DECLARADA

- Estas dos firmas ponen en SÍ, **por paquete y con evidencia propia**, los gates CONTEXTO-NUEVO-ACREDITADO (sujeto a la auditoría del transcript de cada paquete) y CONTRATO-FIRMADO. No autorizan ningún paquete concreto ni abren dato: ACCESO-AUTORIZADO sigue saliendo de `ee49-01/02` (ADENDA-1 de RECIBO-ASTRA6-2), delimitado a módulos y campos de su hoja.
- `FP-…-26a2-03` (reserva por paquete) no se preguntó: el encargo (§2) no la lista como pendiente para P0. Sigue ABIERTA; este acto la cita, no la cierra.
- El acto marca FIRMADAS `26a2-01` y `26a2-02` en `forense/firmas-pendientes.tsv` citando esta adenda.
