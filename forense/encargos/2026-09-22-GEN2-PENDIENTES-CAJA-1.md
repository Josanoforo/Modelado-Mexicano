# ENCARGO · ACTO GEN2-PENDIENTES-CAJA-1 · Lo que el inventario dejó «esperando a caja», verificado en caja fila por fila: cada estatus asentado con salida cruda, lo registrable registrado, lo humano devuelto a mesa con receta

> ENTORNO: **CAJA (Ubuntu, corpus montado)** — el hook de arranque imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea. NO se lanza en nube: toda fila de esta lista existe porque nube no pudo.

CABECERA · SHA de redacción `ccd7c0eb` (22/sep/2026; re-deriva al abrir) · una sola sesión (D-17) · MODELO: Opus (verificar 40–50 estados distintos con lectura de causa) · MODO: **ABIERTO** · CONTADOR: cero mediciones nuevas; puede mover `N_corridas_selladas` y `N_resultados_gen2_sellados` si registra corridas ya selladas (reportado con `status` antes/después), y `no_corrido_abiertas` a la baja; **no** adopta · FP/ADR/NC candidatos: raíz de acto (D-24).

## 1 · OBJETIVO
Que cada fila del inventario `PENDIENTES-PROGRAMA.md` §5 («lo que espera a caja», 49 filas al 21/sep) —o de la lista depurada `PENDIENTES-CAJA-lista-v1_0.tsv` si `GEN2-PENDIENTES-RECONCILIA-1` ya fusionó— tenga un estatus **verificado en el entorno que la fila pedía**, con el comando y su salida cruda: `RESUELTO` (se hizo aquí y se asienta) · `RESUELTO-ANTES` (otro acto ya lo hizo; se cita y se cierra) · `VIGENTE-CAJA` (sigue abierta con causa medida) · `HUMANO` (exige identidad o comprobante externo; se devuelve a mesa con receta manual de un minuto, A.5). Habilita: que ninguna fila del programa quede «esperando a caja» por no haberse probado en caja.
«Hecho» = sobre el commit final con `origin/main` fusionado: `forense/notas/<fecha>-GEN2-PENDIENTES-CAJA-1-verificacion.tsv` con una fila por ítem (`id · comando · salida_resumida · veredicto · cita`) y `awk -F'\t' 'NR>1{print $4}' <tsv> | sort | uniq -c` reporta los cuatro veredictos; toda NC `RESUELTO`/`RESUELTO-ANTES` está `CERRADA` con `cerrado_por=<este acto>`; ninguna `HUMANO` cambia de estado.

## 2 · FIRMAS DE MESA
Ninguna nueva. Las firmas que una fila exija para cerrarse y que **no** consten en el repo → la fila es `HUMANO` o `DE-MESA`, se lista, no se cierra. La regla de registro ya sellada se cita, no se pide: E.7 (v2.16) — «toda corrida sellada entra a la vista en el mismo acto que la sella … ningún veredicto de replay se publica sin asiento».

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
- `[EJECUTADO]` Inventario adjunto: sha256 `8d02b03e920c7461…`, derivado de `99a43faf` (21/sep). §5 lista 49 filas con razones `NO-VERIFICABLE-AQUI`, `PARO-ENTORNO`, `DIFERIDO-A`, y algunas con prosa.
- `[EJECUTADO]` Desde ese corte main incorporó `#866` (replay: evidencia aislada por CALC, `corridas.tsv` reescrita) y `#871/#874` (pisos por eje), entre otros; `N_corridas_selladas` pasó de 82 a **154**. Luego NC-0257 («corrida0 registro --verifica --escribe» en caja), NC-0284 («NO SE REGISTRA… verify CALC-ENCRIGE…») y parte de §1.5 pueden estar `RESUELTO-ANTES` — **se comprueba por id de CALC en `corridas.tsv` y por asiento en `replay-evidencia.tsv`**, no por el conteo.
- `[LEÍDO]` Clases de fila en §5, por lo que piden: (i) **registro/verify** con corpus (NC-0257, NC-0284, NC-0228 «re-derivar corridas.tsv/resultados.tsv para SUPERADO->id»); (ii) **lectura de FD/catálogos** que solo están en `data/raw` (NC-0270, NC-0301 «97/98/99 código por código», NC-0236 y NC-0259 «acreditar correspondencias/identidades», NC-0246 «usar las 9 195 identidades»); (iii) **red a fuentes** (NC-0202 «re-intenta el mismo curl», NC-0278 «tres fuentes externas de Astra»); (iv) **humano** (NC-0156 ENNViH solicitud, NC-0166 Appendix C, NC-0120 «observar una recuperación real de StartWhenAvailable» — una espera, no una tarea); (v) **lecturas WBES/ENIGH de Codex fuera del directorio canónico** (NC-0316, NC-0321, NC-0326) que piden inserción o decisión de mesa — no son de caja: se rotulan `DE-MESA` o `RESUELTO-ANTES` si un recibo ya las movió.
- `[EXISTE]` `tools/verifica_aislada.py` o su equivalente del carril Codex (`#866`: «verifica cada CALC en proceso aislado»). No sé su nombre exacto ni su interfaz: **el acto lo localiza** (`ls tools/ | grep -i "verif\|aisl\|replay"`) y lo usa; si no existe, `verify` por CALC en subproceso, uno por uno (NC-0182: nunca en bloque en un proceso).
- `[SUPUESTO]` Ninguna fila de §5 exige abrir una ola reservada. Por qué lo creo: son actos de registro, lectura de FD y sondas. Si resulta falso —una fila pide leer ENVIPE 2026 o ENIGH 2024 fuera del código congelado—, rama prevista: PARO a) **solo para esa fila**, que queda `VIGENTE-CAJA` con la razón, y el acto sigue.
- ADJUNTOS: `PENDIENTES-PROGRAMA.md` · `8d02b03e920c7461…`. Si `GEN2-PENDIENTES-RECONCILIA-1` ya fusionó, manda su `PENDIENTES-CAJA-lista-v1_0.tsv` (lista depurada) sobre §5; si no, §5 tal cual.

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO
- Por cada CALC citado en §5 y §1.5: `grep -c "<CALC>" data/corrida0/corridas.tsv` y `grep -c "<CALC>" forense/replay-evidencia.tsv` — si ambos > 0, la fila es `RESUELTO-ANTES` con cita a `#866`/al acto que asentó.
- Por cada NC: leer `estado` y `cerrado_por` en `no-corrido.tsv` **antes** de tocarla (A.17: un bloqueador citado se re-verifica de estado).
- Al ejecutor: **repítela tú.**

## 5 · PIEZAS — resultado esperado, no receta
- **P1 · Registro y verificación (clase i).** Para cada corrida sellada sin fila en la vista o sin asiento: verificación **aislada por CALC** con los dos ejes (E.3), asiento en `replay-evidencia.tsv` con cita, y **una** escritura `registro --escribe --lote <todas las asentadas>`; `status` antes/después. Un `NO-REPRODUCE` lleva causa hasta la fila o queda «causa pendiente»; un `NO-VERIFICABLE` no se degrada. Nada se fuerza (`--force` prohibido). Queda bien si el guardia `REPLAY-PISADO` reporta cero pisadas no nombradas.
- **P2 · Lecturas de FD y catálogos (clase ii).** Cada fila que pedía abrir un FD/catálogo de `data/raw`: se abre, se cita archivo y texto (A.15c: por texto, no por nombre), y la NC cierra o queda `VIGENTE-CAJA` con lo que el FD dice. Las acreditaciones masivas (NC-0236: 643+451+26+32 correspondencias; NC-0259: 190 identidades) **no se hacen aquí**: se mide cuántas quedan y se declara el tamaño con comando; si mesa quiere acreditarlas es acto propio.
- **P3 · Sondas de red (clase iii).** Cada `curl`/fetch que nube no pudo: se reintenta **una vez** desde caja, salida cruda; `NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO` + receta manual si falla (A.5). Prohibido concluir sobre un portal desde memoria.
- **P4 · Devolución de lo humano (clase iv) y de lo de mesa (clase v).** Lista `HUMANO` con receta de un minuto por fila (a quién escribir, qué adjuntar, qué esperar); lista `DE-MESA` con la pregunta en una línea. Ninguna cambia de estado.
- **P5 · La tabla del «Hecho»** y la nota: qué se cerró, qué sigue, qué se devolvió, y la diferencia entre lo que el inventario decía que esperaba a caja y lo que de verdad esperaba (esa diferencia es un hallazgo: `hallazgos.md`).
- «si `[SUPUESTO]` resulta falso»: la fila queda `VIGENTE-CAJA` con PARO a) declarado; el resto sigue.

## 6 · LATITUD
DECIDES TÚ: el orden; enlazar `data/raw` si el hook lo pide; instalar una dependencia que `verify` necesite; regenerar derivados por comando; subprocesos por CALC; arreglar ≤ 10 líneas adyacentes declarándolo (p. ej. una ruta de FD mal citada).
PREGUNTAS A MESA (con opciones y recomendación, y sigues): si `registro --escribe` sigue parando por corridas ajenas sin asiento que **no** están en el inventario, ¿se asientan también (recomendado: sí, están a una invocación y es la doctrina de E.7) o se lista y se para ahí?
NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada
a) abrir, derivar o imprimir dato de una ola reservada fuera del código autorizado — **por fila**, no para el acto · b) borrar, forzar o reescribir algo sellado (`--force`, `--lote` con corridas no verificadas aquí) · c) adoptar, o mover un contador vedado · d) no aplica · e) entorno equivocado (nube) · f) OBJETIVO inalcanzable → PARO como entregable.

## 8 · COMPUERTAS
«Ningún otro acto de caja en vuelo — protege: borrar» (comparten `corridas.tsv`, `resultados.tsv`, `usos.tsv`, `replay-evidencia.tsv`; dos escritores sobre los derivados es el defecto que E.7(3) nombra). Se comprueba con `git ls-remote --heads origin` al arrancar y se declara.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/replay-evidencia.tsv` (asientos, append) · derivados de `corrida0` (`corridas.tsv`, `resultados.tsv`, `usos.tsv`, …) por comando · `forense/no-corrido.tsv` (estado y `cerrado_por` de las filas de la lista; nada más) · `forense/notas/<fecha>-GEN2-PENDIENTES-CAJA-1-{verificacion.tsv,nota.md}` · `forense/hallazgos.md` · `canon/L0/<ADR-raíz>.md` · FP/NC propios.
Ajeno que no se toca: ningún `CALC-*/` (sellos intactos), `milpa/`, specs, el crosswalk de tablas FD (NC-0236/0259: se mide, no se acredita), `decisiones.tsv`.
Archivos que OTRO ACTO EN VUELO esté tocando ahora: **ninguno verificado** al redactar. `GEN2-PENDIENTES-RECONCILIA-1` (nube) toca `no-corrido.tsv`: quien fusione después re-aplica sus cierres por id (raíz de acto, sin renumerar). Lanzar este acto **después** de que RECONCILIA fusione ahorra trabajo (lista depurada) pero no es compuerta.
«Si te encuentras escribiendo fuera de esta lista, PARA.»
PERÍMETRO DE CIERRE — permanente (D-21).

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA · CIERRE
No hace: no mide nada nuevo, no adopta, no fuerza registros, no acredita correspondencias masivas, no escribe correos ni solicitudes (eso es humano), no abre olas reservadas.
Sucesores: `GEN2-TRAMITE-FIRMAS-6` (dirección) con las listas `HUMANO` y `DE-MESA`; un acto propio si mesa ordena acreditar NC-0236/0259.
Auditoría de rigor extremo: no aplica (afirma sobre el aparato).
Cierre: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` los añade /acto al final del archivo archivado; adendas como archivo propio.

## NO-CORRIDO / RESERVAS

- **qué:** P1 · «y **una** escritura `registro --escribe --lote <todas las asentadas>`» — la escritura se hizo en caja, pero la vista re-derivada (`corridas.tsv` sha256 `fd903c41…`, `resultados.tsv` sha256 `0e27682f…`) no viaja en el PR. · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: la guarda bloqueante `verify.yml:546` (firma de mesa 21/sep §2(2)) impide que un PR toque un derivado y el job del push a `main` no corre `registro`; respuesta de mesa del 22/sep, verbatim: «PR sin derivados + FP a mesa (Recomendado)». · **impacto:** la vista publicada sigue sin 21 corridas selladas (18 sin fila, 3 todavía `SPEC-FIJADA`) y con 13 filas `NO-VERIFICADO` que ya tienen asiento; `corrida0 status` no cambia (154 / 44177). · **sucesor:** `FP-260922-GEN2-PENDIENTES-CAJA-1-c09b-02` (fila `NC-260922-GEN2-PENDIENTES-CAJA-1-c09b-01`).
- **qué:** P2 · NC-0270, consecuencia de la confirmación: subir `evidencia_grado` de la fila `localidad` en `data/crosswalk-ejes-arbitro-modelo-v1_0.tsv`. · **por qué:** FUERA-DE-PERÍMETRO: la tabla es de `GEN2-CROSSWALK-EJES-1` y el perímetro de este encargo no la nombra. · **impacto:** ninguno sobre veredictos (MAPEO-N-A-1 no cambia); sólo el grado de evidencia declarado. · **sucesor:** `NC-260922-GEN2-PENDIENTES-CAJA-1-c09b-02` (mesa ordena el acto que edite la fila).
- **qué:** P1 · «Un `NO-REPRODUCE` lleva causa hasta la fila» — `CALC-PISO-PERSISTENCIA-ERROR-0001` sale `NO-EJECUTABLE` (no NO-REPRODUCE) con causa hasta la fila: importa `tools/marcador_segmento.py` vivo. · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: una corrida sellada no se reescribe (E.3); reproducirla exige un CALC sucesor con el marcador congelado como constancia (D-22(4)). · **impacto:** su replay vigente queda `NO-EJECUTABLE`; `status` no cambia. · **sucesor:** `NC-260922-GEN2-PENDIENTES-CAJA-1-c09b-03`.
- **qué:** P3 · «se reintenta **una vez** desde caja» — 5 URL no obtenidas (ENNViH 404; RAND, ICPSR, openICPSR, OUP 403; respuesta del sitio, no del proxy). · **por qué:** NO-VERIFICABLE-AQUÍ: NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO (A.5); recetas manuales H3 y H4 en la nota §4. · **impacto:** NC-0202 y NC-0278 siguen `ABIERTA` (`HUMANO`); ninguna conclusión se apoya en lo no obtenido. · **sucesor:** `GEN2-TRAMITE-FIRMAS-6` con la lista `HUMANO` (NC-0202, NC-0278).
