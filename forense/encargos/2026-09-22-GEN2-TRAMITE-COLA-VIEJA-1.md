# ENCARGO · ACTO GEN2-TRAMITE-COLA-VIEJA-1 · Los 28 encargos del 11/sep que nadie lanzó: cada uno con su superador por objeto, archivado SUPERADO-POR o VENCIDO, y la cola deja de contarlos como pendientes

> ENTORNO: **NUBE**. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Opus (buscar el superador de 28 objetos es juicio) · MODO: **ABIERTO** · CONTADOR: cero mediciones; «encargos en cola sin consumir» 28 → N (reportado) · ids raíz de acto.

## 1 · OBJETIVO
Que los 28 encargos sin `## CONSUMIDO` (inventario `PENDIENTES-PROGRAMA` §4.1, derivado de `3f48be30`; 13 CAJA, 11 sin entorno, 4 NUBE; series `POST-693/707/723` del 11/sep, anteriores a la plantilla v2.0 y a la regla de señal) reciban, cada uno, **un** veredicto de vocabulario cerrado con cita: `SUPERADO-POR <acto>` (otro acto hizo su objeto) · `VENCIDO` (su premisa cambió y nadie lo hará: A.10) · `VIGENTE-RELANZABLE` (nadie hizo el objeto y sigue valiendo: se reescribe en plantilla v2.1, no se lanza como está). «Hecho» = cada uno de los 28 archivos termina con un apéndice `## CONSUMIDO — <veredicto> · <cita>` (A.3: apéndice, nunca edición del cuerpo); el inventario §4.1 re-derivado da 0 en cola salvo los `VIGENTE-RELANZABLE`, que aparecen con ese rótulo; una nota con la tabla `encargo · objeto · veredicto · cita`.

## 2 · FIRMAS DE MESA
- Verbatim (conversación de dirección, 22/sep/2026): «Sí autorizo que archive por trámite 28 encargos de la cola si ya están superados.» Alcance que dirección lee de esa firma: `SUPERADO-POR` cuando el objeto está hecho por otro acto (cita obligatoria); `VENCIDO` solo cuando la premisa del encargo ya no existe (p. ej. cita una NC cerrada, un CALC sustituido, una ley E0 vencida) — con la cita del cambio; lo demás **no se archiva**: queda `VIGENTE-RELANZABLE` y vuelve a dirección.
- Enmienda de dirección al trámite anterior (hallazgo, no firma): «La cifra «18 de 20» tenía fuente (`#969`, `forense/notas/2026-09-21-GEN2-MARCADOR-E-INFORME-1-cierre.md:46`: 7/8 + 11/12, pilotos 1 y 2); el defecto era citar dos pilotos con tres selladas (26/35). Lo asentado por TRÁMITE-PENDIENTES-1 («era tecleada») se enmienda con fecha; la frase del informe se reescribe igual con 26/35.»

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` Inventario §4.1 (sha `5315092294609423…`): 28 rutas. `[LEÍDO]` `forense/notas/2026-09-22-GEN2-PENDIENTES-RECONCILIA-1-nota.md` §3: «encargos §4.1: 0 ejecutados, verificado por objeto» — verificó que nadie los **ejecutó**, no que nadie hiciera su **objeto** por otro camino: esa es la búsqueda que falta.
- `[SUPUESTO]` La mayoría son `SUPERADO-POR`: entre el 11 y el 22/sep entraron ~200 PR y siete tandas de relevo. Si resulta falso, la tabla lo dice y `VIGENTE-RELANZABLE` vuelve a dirección; el acto no reescribe encargos.
- ADJUNTOS: `PENDIENTES-PROGRAMA__1_.md` · `5315092294609423…` (la lista §4.1 vive ahí; si no viaja, se re-deriva con el generador de 004 o con `grep -L "## CONSUMIDO" forense/encargos/*.md`).

## 4 · YA HECHO / YA DECIDIDO
`grep -L "## CONSUMIDO" forense/encargos/*.md | wc -l` → reporta (28 al redactar); por encargo, `grep -l "<objeto>" forense/notas/*cierre* canon/gobernanza-v1_15.md` por **objeto** (CALC, tabla, regla, NC), nunca por el nombre del encargo. Ramas vivas: ninguna.

## 5 · PIEZAS
- **P1 · Tabla.** Por encargo: objeto (una frase, leída del encargo), búsqueda por objeto (comando + conteo), veredicto, cita. Queda bien si un lector puede reproducir cada veredicto con el comando.
- **P2 · Apéndices.** `## CONSUMIDO — SUPERADO-POR <acto> · <ADR/PR>` o `## CONSUMIDO — VENCIDO · <cita del cambio de premisa>` al final de cada archivo; los `VIGENTE-RELANZABLE` reciben `## ESTADO — VIGENTE-RELANZABLE · reescribir en v2.1 (dirección)` sin CONSUMIDO. Ningún cuerpo se edita.
- **P3 · Enmienda «18 de 20».** Fila fechada en `decisiones.tsv` y en la NC `…7ef3-02` con el texto de §2; línea en `hallazgos.md`.
- **P4 · Nota** con la tabla y el conteo por veredicto; el inventario de 004 lee los apéndices en su siguiente corrida.

## 6 · LATITUD
DECIDES TÚ: orden, cómo buscar por objeto. PREGUNTAS A MESA: si un encargo está **parcialmente** superado (una pieza sí, otra no), ¿`SUPERADO-POR` con la pieza restante como NC nueva (recomendado) o `VIGENTE-RELANZABLE` entero? NO DECIDES: §7.

## 7 · PAROS
a) no aplica · b) editar el cuerpo de un encargo archivado, o borrar archivos · c) no aplica · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
Ninguna. Orden sugerido: después de que 004 entregue el inventario v3 con §4.1 «superador o SIN-SUPERADOR» — si llega antes, este acto verifica esa columna en vez de derivarla; si no, la deriva.

## 9 · PERÍMETRO
Propio: los 28 archivos de `forense/encargos/` (solo apéndice) · `data/corrida0/decisiones.tsv` (una fila) · `forense/no-corrido.tsv` (enmienda 7ef3-02; NC nuevas por piezas restantes) · `forense/hallazgos.md` · nota · `canon/L0/<raíz>.md`. Ajeno: todo lo demás. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No relanza, no reescribe, no borra. Sucesor: dirección reescribe los `VIGENTE-RELANZABLE` en v2.1 si los hay. Auditoría: no aplica. Cierre por /acto.


