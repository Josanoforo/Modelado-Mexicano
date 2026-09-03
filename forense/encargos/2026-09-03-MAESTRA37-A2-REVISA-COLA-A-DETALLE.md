ENCARGO · ACTO MAESTRA37-A2 · REVISA-COLA-A-DETALLE — invoca /acto

SHA de redacción: 2e79d153 · COMPUERTA: PR de N8 fusionado (mismo archivo de cola; N8 reclasifica estados, éste añade informe por fila). ENTORNO ASIGNADO: NUBE con red (cloud_default; sonda INEGI como control positivo de red). NO descarga: este acto lee, sondea y recomienda; descargar es de MAESTRA38-A1 y de mesa. MODELO SUGERIDO: Opus (búsqueda de hermanas y juicio de identidad de fuente; Codex si mesa prefiere — es CLI, no exige caja).

FIRMA DE MESA — verbatim: la de «Descargas manuales» en §0. Regla que la traduce: ninguna fila se cierra por veredicto de agente; el entregable es información para que mesa decida.

═══ A.8 ═══ Cola: 112 filas; no OBTENIDO/CERRADA: 29 (9 PENDIENTE, 9 NO-ACCESIBLE, 7 NO-OBTENIDO-POR-ESTE-AGENTE, 2 OBTENIDO-PARCIAL, 1 NO-ACCESIBLE-DESDE-LA-CAJA, 1 firma c1) — tras N8: 5 pasan a NO-ADQUIRIDA-POR-COSTO y 2 a PENDIENTE-DE-MESA; el universo de este acto es lo que quede no OBTENIDO, derivado al arrancar. .claude/commands/adquiere.md ya exige ≥4 rutas y receta ≤1 min (ADR-261) — se reutiliza, no se rediseña. aliases-fuentes.tsv (14 fuentes) es la tabla de hermanas conocidas.

SPEC — dos commits. COMMIT-1: lista congelada de filas y, por fila, la pregunta que la fila responde (regla/necesidad que la cita, derivada de relaciones.tsv/necesidad-objeto-modelo.tsv; si ninguna la cita, se dice — es información para mesa, no cierre). COMMIT-2, por fila: (a) cuatro rutas con salida cruda (A.5), sonda de alcanzabilidad antes de contenido (v2.2); (b) hermanas: mismo objeto en otra fuente/portal/espejo/año, con la distinción de identidad de A.7 (mismo contenido, distinta envoltura ≠ fuente distinta); (c) qué exactamente trae cada candidata (tabla de variables / temas si hay FD público) y qué le falta contra la pregunta de (a); (d) recomendación en tres valores: BAJAR (receta ≤1 min) · NO-BAJAR-PORQUE (razón sustantiva) · MESA-DECIDE (dos opciones con costo). Ningún NO-ENCONTRADO sin universo, términos y fecha en la misma línea (A.4/A.13). Salida: forense/notas/2026-09-0X-MAESTRA37-A2-revision-cola.md + PAQUETE-RECETAS-3 + nota append por fila en la cola (writer de INFRA-1), sin cambiar estado_A4A5.

PERÍMETRO. Toca: data/curacion-registro/cola-adquisicion-registro.tsv (sólo columna nota, append) · vista T26 · forense/notas/…A2… · forense/notas/…PAQUETE-RECETAS-3.md · tablero · A.3 · cascada. NO toca: estado_A4A5 · data/manifiesto.yaml · aliases-fuentes.tsv (propone hermanas, no las da de alta) · milpa/**. No descarga. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR: ADR-330 (deriva) · FP-288 recibo · FP-289: «mesa firma la clasificación final de las N filas con el informe a la vista» (vence a 7 días). CONTADOR: filas con informe 0 → N · medición: cero.

## BLOQUEADO — COMPUERTA no satisfecha

3/sep/2026, verificado contra `origin/main` tras `git fetch`: no existe
ningún `MAESTRA37-N8` (encargo, PR, ni commit) en el árbol. `git log --all
--oneline --grep='N8' -i` sólo encuentra `MAESTRA34-N8-FECHAS-SON-LIMITES`
y `MAESTRA35-N8-SELLA-L7`, ninguno sobre
`data/curacion-registro/cola-adquisicion-registro.tsv`. La COMPUERTA de
este acto («PR de N8 fusionado») **no está satisfecha**. Por protocolo de
`/acto` ante compuerta no satisfecha, el SPEC (dos commits) **no se
ejecutó**: no se congeló el universo de filas, no se sondeó ninguna ruta,
no se buscaron hermanas, no se tocó la columna `nota` de la cola. Detalle
en `forense/notas/2026-09-03-MAESTRA37-A2-bloqueo.md`. Sucesor natural:
redactar y correr `MAESTRA37-N8` (reclasificación de estados) antes de
reintentar este acto, o instrucción explícita de mesa/dirección para
proceder sin él.
