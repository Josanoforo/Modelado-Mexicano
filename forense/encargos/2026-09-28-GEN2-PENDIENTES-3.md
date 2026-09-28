# ENCARGO · ACTO GEN2-PENDIENTES-3 · El libro de NC tiene 497 filas abiertas y crece porque cada acto abre rutas hacia adelante y ninguno cierra las que lo nombran: 75 filas cuyo sucesor ya corrió, 222 sin dueño, 219 que esperan un entorno con corpus que ningún acto de nube podía tocar, 110 con id anterior al régimen. Este acto barre el libro entero **por objeto y con delegación de mesa** —cierra lo cerrable, decide lo reversible, asigna lo asignable a actos que existen— y deja instalado el mecanismo que impide que vuelva a pasar: al cerrar, todo acto dictamina las NC que lo nombran, y ninguna ruta se abre sin sucesor archivado

> ENTORNO: **CAJA** — 219 filas (ESPERA-DATO 122 + NO-VERIFICABLE-AQUÍ 97) exigen el corpus montado para verificarse; el resto se resuelve desde el repo. Hook imprime ENTORNO-DERIVADO; si dice cloud_default o milpa-inegi, PARA. Sesión ligera salvo cuando abra una base para verificar (nunca para recalcular).

CABECERA · SHA de redacción `98f80cc7` (re-deriva al abrir) · una sesión, rama propia; PR por bloque (mecanismo · vencidas · espera-dato · asignar · decisión) · MODELO: **Opus** (cada fila es un juicio sobre un objeto) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto · D-21 aplica.
CONTADOR: cero mediciones; no adopta. Mueve `no_corrido_abiertas` hacia abajo **solo por cierres con cita** (producto, diseño, decisión delegada, sucesor archivado que la absorbe). **Este acto no abre NC**: lo que no pueda cerrar queda con dueño de la lista cerrada de P4; lo irreversible va a una hoja al cierre.

## 1 · OBJETIVO
(P1) **El mecanismo, primero (D-14: 75 vencidas y 117 cierres sin acto declarado son el defecto real).** Dos cambios en `/acto` (`tools/cierre_acto.py` o donde viva la cascada) con test huérfano: (i) **cierre hacia atrás**: al cerrar, el acto obtiene por comando las NC ABIERTAS cuyo `sucesor` lo nombra (por nombre con frontera, como PENDIENTES-2 dejó el clasificador) y **exige dictamen de cada una** — `CERRADA (producto: ruta · comando)` · `SIGUE-ABIERTA (sucesor archivado nuevo)` · `SIN-OBJETO (cita)` — y falla la cascada si alguna queda sin dictamen; `cerrado_por` obligatorio. (ii) **rutas con sucesor real**: una NC con razón FUERA-DE-PERÍMETRO o DIFERIDO-A solo entra al libro si su `sucesor` nombra un encargo **archivado** (`forense/encargos/`, `cola/` incluida) o un acto en vuelo por rama; si no, la guardia la rechaza y el acto la escribe como línea en `forense/hallazgos.md`. Lo anterior es la regla A.14 ampliada que mesa firmó hoy (§2); se registra en `gobierno/` como delta v2.17→v2.17.1 para la HISTORIA.
(P2) **Las 75 VENCIDA-CANDIDATA y las candidatas RESUELTO-ANTES** (§E y §L del inventario): por objeto, `CERRADA-POR-PRODUCTO` con ruta y comando, o `SUCESOR-SIN-PRODUCTO` reasignada a un acto archivado o en vuelo (nunca a un nombre que no existe).
(P3) **Las 219 que esperan dato o entorno**: en caja, abrir lo que la fila pedía verificar (existencia de variable, sha, payload por id, etiqueta, fila en vista) y cerrar con cita lo que ya se cumple; lo que exige una ola reservada queda `ESPERA-APERTURA (ola, id)` con la firma que la abriría; lo que exige un dato no adquirido queda `ESPERA-ADQUISICION (fuente, estado A4/A5, solicitud)` apuntando a OBTENCION-EXTERNA-1 o a la cola. Nada de «no existe».
(P4) **Las 222 ASIGNAR, las 63 DECISIÓN, las 110 de id numérico y las 11 HUMANO.** Bajo la delegación de mesa: prosa sin sucesor → se decide la reversible y se cierra, o se asigna a un acto archivado o en vuelo que la cubra (CALC-ALTERNOS, PISOS-DOMINIOS, C1-SUCESORES, TUBERIA-3, TABLERO-CARRILES, CIERRE-SEMANAL-3); acto nombrado sin encargo → el acto vigente que lo absorbió, o `CERRADA-POR-DISEÑO` si su objeto desapareció; id numérico → si su objeto es GEN1 o un procedimiento retirado, `CERRADA-POR-DISEÑO (E.1: GEN1 es historia)` con cita, si no, se trata como las demás; DECISIÓN → cruzar con `decisiones-21.tsv` y ADENDA-1 de TRAMITE-FIRMAS-21: las ya firmadas se cierran con la firma; las de verdad pendientes van a la hoja **con opciones**; HUMANO → lista de 11 con receta de un minuto cada una, para mesa, y siguen ABIERTAS con `plazo`. Lista cerrada de dueños al cierre: `MESA (fecha)` · `CAJA (encargo archivado)` · `ADQUISICION (solicitud o fuente en cola)` · `APERTURA (ola, firma)`.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: `nc_por_clase.py --json` → `VENCIDA-CANDIDATA` = 0 y `ASIGNAR` = 0; toda NC ABIERTA tiene `sucesor` de la lista cerrada de dueños (regex declarada en el test; filas fuera: 0) · toda fila cerrada por este acto tiene `cerrado_por` y `fecha_cierre` · el test de P1 pasa sobre un acto sintético que nombra una NC (falla sin dictamen; pasa con él) · la guardia de rutas rechaza una NC sintética sin sucesor archivado · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA
Mesa, 28/sep/2026, chat de dirección, verbatim: «quiero cerrar la mayor cantidad de pendientes posibles». Dirección propuso en el mismo chat, y mesa firma con su respuesta a ese mensaje (viaja verbatim en ADENDA-1): (a) **delegación** — el acto decide por sí mismo la opción reversible de toda NC sin decisión de mesa pendiente, cierra por producto y por diseño con cita, y solo lo irreversible (D-19) vuelve en una hoja; (b) **regla nueva A.14 (v2.17.1)** — al cerrar, todo acto dictamina las NC que lo nombran como sucesor; FUERA-DE-PERÍMETRO y DIFERIDO-A solo con sucesor archivado o en vuelo, si no, hallazgo de una línea. Firmas previas que este acto aplica: ADENDA-1 de TRAMITE-FIRMAS-21 (78 renglones), ADENDA-1 de HOJA-FIRMAS-21-1 (22 letras). E.1 (GEN1 es historia), A.4, A.15, A.17, D-21.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `98f80cc7` · `no-corrido.tsv`: 1 066 filas, 497 ABIERTA; por razón: NO-VERIFICABLE-AQUÍ 97, FUERA-DE-PERÍMETRO 73, DIFERIDO-A 76 (61 + 8 SIN-ASIGNAR + 7 TUBERIA), DECISIÓN 50, PARO-PREMISA 37, PARO-ENTORNO 8; por quien abrió: id numérico legacy 110, RECIBO-ASTRA6-2 17, -3 11, CONSUMO-Y-GASTO-PISOS-1 9, OBTENCION-EXTERNA-1 9, ASTRA5 14, RELEVO 14; abiertas por día 21–28/sep: 48, 27, 57, 52, 35, 67, 40, 69.
- [LEÍDO] Inventario v4 (adjunto): clases HUMANO 11 · DECISIÓN 63 · VENCIDA-CANDIDATA 75 · EN-CURSO 4 · ESPERA-DATO 122 · ASIGNAR 222 (prosa sin sucesor 91, acto sin encargo 85, sin sucesor 46); §M: 124 abiertas y 103 cerradas entre `11602de8` y `98f80cc7`, 40 cierres sin acto declarado; §C: 9 filas donde `nc_por_clase.py` aún dice NO-ENCONTRADO con encargo archivado (frontera de nombre: PENDIENTES-2 lo corrigió en parte; verificar y terminar).
- [LEÍDO] Cierres ya hechos que no se repiten: PENDIENTES-2 (12 vencidas, 12 filas rotas, tokens), TRAMITE-FIRMAS-21 (19 NC-pregunta por delegación, 78 renglones asentados), DEMANDA-DICTAMEN-1 (NC de la demanda con dictamen: se citan).
- [EXISTE] `tools/nc_por_clase.py`, `tools/cierre_acto.py` (cascada), `tools/consulta.py`, `forense/analisis/pendientes-2/`.

ADJUNTO: `PENDIENTES-PROGRAMA__4_.md` (inventario v4; el acto lo archiva verbatim con el sha que calcule, en `forense/analisis/pendientes-3/`).

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'PENDIENTES-3'` → 0. Consumidos y citados: TRAMITE-PENDIENTES-1/2, PENDIENTES-CAJA-1, PENDIENTES-RECONCILIA-1, SENAL-1, NC-DECISIONES-1, TRAMITE-FIRMAS-21. En vuelo: CALC-ALTERNOS, C1-SUCESORES, PISOS-DOMINIOS (caja: **no cerrar sus NC ni las que los nombren hasta que fusionen**; se citan como EN-CURSO), TUBERIA-3 y TABLERO-CARRILES-1 (nube; `no-corrido.tsv`: rebase antes de cerrar, nunca la misma fila), el `[deriva]`.

## 5 · PIEZAS
P1 → P2 → P4 → P3 (caja al final, con todo lo demás cerrado y el libro más chico). Rama prevista: fila cuyo objeto está en un acto en vuelo → EN-CURSO con el nombre de la rama; fila que pide algo que otra fila ya cerró → duplicada, cerrada con cita a la primera; conflicto de merge en el TSV → rebase y re-derivar el «hecho».

## 6 · LATITUD — amplia por delegación
Todo lo reversible se decide y se declara en una tabla `forense/analisis/pendientes-3/decididas-por-delegacion.tsv` (id · opción · razón). Orden, PR, agrupación: tuyos. PREGUNTA A MESA: una hoja al cierre solo con lo irreversible y con opciones. NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir una ola reservada o recalcular · b) borrar filas del libro; editar sellos, RESULT, firmas · c) adoptar; cerrar sin cita; asignar a un acto que no existe · d) no aplica · e) NUBE · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Ningún cierre sin cita; ninguna asignación a nombre inexistente» protege **borrar** (deuda escondida) · «Verificar no es recalcular» protege **abrir dato** · «El mecanismo con test antes del barrido» protege **borrar** (que el libro vuelva a crecer por rutas).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/no-corrido.tsv` (estado, sucesor, cerrado_por, fecha_cierre, razón normalizada), `tools/cierre_acto.py` (P1) y su test huérfano, la guardia de rutas, `gobierno/` (delta v2.17.1 registrado para la HISTORIA; el cuerpo v2.17 no se edita), `forense/analisis/pendientes-3/`, `forense/hallazgos.md`, nota, L0, cascada. Ajeno: `firmas-pendientes.tsv` fuera del append, sellos, specs, vistas. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No mide, no adopta, no abre reservadas, no cierra NC de actos en vuelo, no envía nada con identidad (las 11 HUMANO se listan para mesa). Sucesores: INSTRUCCIONES-V217-1 `-2` (absorbe el delta v2.17.1 en el cuerpo del proyecto cuando mesa lo pegue); CIERRE-SEMANAL-3 (cita el libro después del barrido). Sin módulo de auditoría. El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-PENDIENTES-3-ADENDA-N.md`, selladas al recibirse.

## NO-CORRIDO / RESERVAS

Ninguno.

Este acto no abre NC (encargo, CABECERA). Límites declarados en `forense/notas/2026-09-28-GEN2-PENDIENTES-3-cierre.md` § Límites: cierres por producto muestreados (8 re-ejecutados), cuatro cierres que dependen de jobs de CI sin log leído, y P3 verificó existencia/sha/metadatos sin abrir bases. Lo que no se cerró queda con dueño de la lista cerrada (332 ABIERTA; 240 MESA, 43 EN-CURSO, 27 ADQUISICION, 18 APERTURA, 6 CAJA); lo irreversible y la bandeja del titular están en `forense/analisis/pendientes-3/hoja-mesa-pendientes-3.md`.

## CONSUMIDO

PR #1307 (`claude/gen2-pendientes-3`), ADR-260928-GEN2-PENDIENTES-3-6e2d-01.
