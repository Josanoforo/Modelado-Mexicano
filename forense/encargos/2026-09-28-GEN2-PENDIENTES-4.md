# ENCARGO · ACTO GEN2-PENDIENTES-4 · De las 334 NC abiertas, 239 llevan dueño «MESA (2026-10-05)», pero solo 7 son decisiones de mesa: 171 dicen «encargo por escribir» (138 ya decididas por delegación y devueltas igual), 39 son recetas personales, 18 esperan al canal o a una hoja. Este acto convierte cada una en lo que es: cierra por diseño lo que es GEN1 o procedimiento retirado, **redacta él mismo los encargos** que las 171 piden —agrupados en lotes robustos, plantilla v2.2, como PROPUESTOS-POR-EJECUTOR en cola para que dirección revise y mesa lance—, cierra lo que el canal ya publicó, deja una sola hoja con las recetas de mesa y otra con las 7 decisiones con opciones, y corrige el dueño de cada fila para que el tablero deje de decir que el 72 % espera a mesa

> ENTORNO: **NUBE** — libro de NC, encargos, notas, vistas. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `9d2550b9` (re-deriva al abrir) · una sesión, rama propia; PR por bloque · MODELO: **Opus** (redactar encargos y cerrar por diseño es juicio de guía) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0; mesa 28/sep: «tratémoslo como guía explorador») · ids con raíz de acto · D-21 aplica.
CONTADOR: cero mediciones; no adopta. Mueve `no_corrido_abiertas` hacia abajo por cierres con cita. **No abre NC**; no devuelve nada a mesa que no sea una decisión con opciones o una acción con identidad.

## 1 · OBJETIVO
(P1) **Cierre por diseño con cita.** Toda NC con dueño MESA cuyo objeto sea GEN1, un procedimiento retirado (duelo v2 sin camino de emisión por regla 6, θ, motor legacy), un archivo que ya no existe, o un producto que otro acto ya entregó en main: `CERRADA-POR-DISEÑO (E.1 / regla 6 / commit que lo retiró)` o `CERRADA-POR-PRODUCTO (ruta · comando)`. Empieza por las 47 numéricas (`NC-0xxx`) y por las 138 «decididas por delegación» de `forense/analisis/pendientes-3/decididas-por-delegacion.tsv`: la delegación ya estaba firmada; aquí se ejecuta.
(P2) **Los encargos, redactados.** Lo que de verdad falta por producir se agrupa por producto y entorno en **el menor número de encargos robustos** (sugerido: CALC-ALTERNOS-LOTE-2 · PISOS-DOMINIOS-Y-REGLAS-2 · RELEVO-TRAMITE-CAJA-2 · un lote de tubería/tests · un lote de curación/corpus; la sesión decide), cada uno completo según `PLANTILLA-ENCARGO-v2_2.md`, con premisas rotuladas, «hecho» por comando, perímetro y las NC que absorbe listadas en su §4; se archivan en `forense/encargos/cola/PROPUESTOS/` con sidecar y **cada NC absorbida pasa a `sucesor = <ese encargo>`** (la guardia de rutas lo acepta: está archivado). Dirección los revisa y mesa los lanza; no se lanzan desde aquí.
(P3) **Canal, hojas y dueños.** Las «cerrable al fusionar el [deriva]»: si el canal ya publicó (`git log` de vistas), cerrar con cita; si no, dueño `CANAL (rama)`. Las 39 HUMANO en **una** hoja para mesa, deduplicada contra R46–R49 y las seis solicitudes de OBTENCION-EXTERNA-1 (una acción, una fila, receta de un minuto). Las 7 decisiones reales y las «hoja de irreversibles» en **una** hoja RH con opciones y texto de firma. Y en el libro, dueño corregido con la lista cerrada (`DIRECCION-ENCARGO (nombre)` · `MESA-ACCION (fecha)` · `MESA-DECISION (hoja)` · `CANAL` · `CAJA (encargo)` · `ADQUISICION` · `APERTURA`), token en el campo (A.16).
(P4) **Cierre.** Conteos por comando antes/después por dueño y por tipo de cierre; la nota dice cuántos encargos redactó y cuántas NC absorbe cada uno.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: 0 filas ABIERTA con `sucesor` que contenga «encargo por escribir» o «cierre por diseño propuesto» · toda fila ABIERTA con dueño de la lista cerrada de P3 (regex en test; fuera: 0) · `MESA-DECISION` ≤ el número de renglones de la hoja de decisiones (cada uno con opciones) · cada encargo PROPUESTO en cola tiene sidecar, pasa el test de plantilla y lista sus NC · `nc_por_clase.py --json`: ASIGNAR 0, VENCIDA 0 · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
Mesa, 28/sep/2026, chat de dirección, sobre PENDIENTES-3 (viaja verbatim en ADENDA-1): la **delegación** — el acto decide lo reversible, cierra por producto y por diseño con cita, solo lo irreversible vuelve con opciones — y la **regla nueva A.14** (cierre hacia atrás; rutas solo con sucesor archivado). Mesa, hoy, en respuesta a este mensaje: **autoriza cerrar por diseño lo que sea GEN1 o procedimiento retirado (E.1, regla 6) y que el acto redacte los encargos que las NC piden, como propuestos en cola**. E.1, regla 6, A.4, A.16, A.17, D-21.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `9d2550b9` · 334 ABIERTA; `sucesor` MESA 239, EN-CURSO 42, ADQUISICION 27, APERTURA 18, CAJA 6. Dentro de MESA: «encargo por escribir» 171 (138 «decididas por delegación»; 8 nombran CALC-ALTERNOS-LOTE-2, 5 PISOS-DOMINIOS-Y-REGLAS-2), HUMANO/receta 39, «hoja de irreversibles» y «cerrable al fusionar el [deriva]» 18, decisiones con opciones 7, «cierre por diseño propuesto» 3, paraguas 1. Por acto que las abrió: numéricas 47, CALC-ALTERNOS-LOTE-1 9, RELEVO-MOTOR-34 7, PISOS-DOMINIOS 6, C1-SUCESORES 6, RECIBO-ASTRA6-2/3 9. `decididas-por-delegacion.tsv`: 168 filas (DUEÑO-MESA 138, CIERRA 30).
- [LEÍDO] Inventario v5 de la conversación de tablero (adjunto; archivar con sha): sus conteos coinciden con el TSV; su nota 1 explica que ASIGNAR y VENCIDA bajaron a 0 por reclasificación, no por cierre. §F lista las 240 con `sucesor` completo.
- [EXISTE] `forense/encargos/PLANTILLA-ENCARGO-v2_2.md` (INSTRUCCIONES-V217-1), `forense/encargos/cola/`, `tools/nc_por_clase.py` con el cierre hacia atrás y la guardia de rutas (PENDIENTES-3).

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'PENDIENTES-4'` → 0. Consumidos y citados: PENDIENTES-2/-3, TRAMITE-FIRMAS-21, NC-DECISIONES-1. En vuelo: CIERRE-Y-PRODUCTO-3, MAPA-DOMINIOS-Y-LICENCIAS-1, APERTURAS-PREREGISTRADAS-1 (nube), MEDICION-CARRILES-2 y VALIDACION-Y-2027-1 (caja): sus NC y las que los nombren no se tocan (EN-CURSO); rebase antes de cerrar; nunca la misma fila.

## 5 · PIEZAS
P1 → P3 (canal y dueños) → P2 → P4. Rama prevista: NC cuyo producto pide caja y no cabe en ningún lote existente → un encargo propuesto nuevo, no NC; NC duplicada de otra → cerrada con cita a la primera.

## 6 · LATITUD — de guía
Cuántos encargos, cómo agruparlos, qué cerrar por diseño con qué cita, formato de las hojas: tuyos. PREGUNTA A MESA: solo la hoja de decisiones. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato · b) borrar filas; editar sellos, RESULT, firmas · c) adoptar; cerrar sin cita; lanzar un encargo propuesto; asignar a nombre inexistente · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Cierre solo con cita» protege **borrar** · «Encargos propuestos, no lanzados» protege **adoptar** · «Dueño de lista cerrada en el campo» protege **borrar** (deuda escondida como «mesa»).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/no-corrido.tsv` (estado, sucesor, cerrado_por, fecha_cierre), `forense/encargos/cola/PROPUESTOS/` (nuevo), `forense/analisis/pendientes-4/` (hojas, tablas, inventario v5 archivado), `firmas-pendientes.tsv` (append de las 7), nota, L0, cascada. Ajeno: encargos archivados, sellos, vistas, `canon/`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no adopta, no lanza encargos, no envía nada con identidad. Sucesores: dirección revisa y mesa lanza los PROPUESTOS; el tablero de carriles y el inventario v6 leen los dueños nuevos. Sin módulo de auditoría. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-PENDIENTES-4-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

Ninguno.

Este acto no abre NC (encargo, CABECERA). Tres decisiones declaradas, sin pieza sin ejecutar, en `forense/notas/2026-09-29-GEN2-PENDIENTES-4-cierre.md` § Premisas que cayeron: la lectura de «`MESA-DECISION` ≤ renglones de la hoja» (renglones distintos citados, 28 ≤ 28, con 42 NC), 16 encargos propuestos en lugar de los cinco lotes sugeridos (D-11: hasta cuatro piezas afines por encargo) y 24 filas de firma en lugar de las 7 previstas. Límites declarados en la misma nota § Límites (citas de cierre que dependen de un PR verificadas por el estado del PR y de sus runs, sin leer logs de job; 10 de las 122 premisas `[EJECUTADO]` de los propuestos muestreadas). Lo que no se cerró queda con dueño de la lista cerrada (284 ABIERTA: DIRECCION-ENCARGO 154 · MESA-DECISION 42 · MESA-ACCION 40 · CANAL 23 · APERTURA 17 · ADQUISICION 7 · CAJA 1). Adenda de este encargo: `forense/encargos/2026-09-28-GEN2-PENDIENTES-4-ADENDA-1.md`.

## CONSUMIDO

PR #1326 (`claude/new-session-snmood`), ADR-260928-GEN2-PENDIENTES-4-12d9-01. Adenda: `forense/encargos/2026-09-28-GEN2-PENDIENTES-4-ADENDA-1.md`. Nota de cierre: `forense/notas/2026-09-29-GEN2-PENDIENTES-4-cierre.md`.
