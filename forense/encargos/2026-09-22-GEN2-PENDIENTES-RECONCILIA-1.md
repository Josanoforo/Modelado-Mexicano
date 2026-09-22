# ENCARGO · ACTO GEN2-PENDIENTES-RECONCILIA-1 · El inventario de pendientes del 21/sep, cotejado fila por fila contra main de hoy: lo resuelto queda asentado, lo vencido rotulado, lo de mesa listado, y lo de caja depurado

> ENTORNO: **NUBE** — el hook de arranque imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea.

CABECERA · SHA de redacción `ccd7c0eb` (22/sep/2026 12:32 −06:00; re-deriva al abrir) · una sola sesión (D-17) · MODELO: Opus (D-13: clasificar 200+ filas por objeto es juicio, no receta) · MODO: **ABIERTO** · CONTADOR: cero mediciones; mueve `no_corrido_abiertas` a la baja (reportado, no prometido) y `firmas-pendientes` solo donde una firma ya conste en `decisiones.tsv`; **no** adopta, **no** mueve `N_corridas_selladas` ni `celdas_validadas` · FP/ADR/NC candidatos: raíz de acto (D-24), los deriva `tools/cierre_acto.py`.

## 1 · OBJETIVO
Que el inventario `PENDIENTES-PROGRAMA.md` (derivado de `99a43faf`, 21/sep) deje de describir un árbol que ya no existe: cada una de sus filas cotejada contra `origin/main` de hoy y clasificada con una sola palabra de un vocabulario cerrado — `RESUELTO-NO-ASENTADO` (el árbol ya lo hizo; la fila sigue ABIERTA) · `VIGENTE` · `VENCIDO` (la premisa cambió) · `MAL-ROTULADO` (razón en prosa que es una autorización ya dada, A.16) · `DE-MESA` · `DE-CAJA` — y que lo cerrable desde nube quede cerrado con su cita. Habilita: que mesa decida sobre 88 piezas que sí son suyas y no sobre 200 que ya no lo son; y que el acto de caja gemelo (`GEN2-PENDIENTES-CAJA-1`) reciba una lista depurada, no 49 filas a ciegas.
«Hecho» = sobre el commit final con `origin/main` fusionado: existe `forense/notas/<fecha>-GEN2-PENDIENTES-RECONCILIA-1-clasificacion.tsv` con una fila por ítem del inventario (`seccion · id · veredicto · cita`), y `awk -F'\t' 'NR>1{print $3}' <tsv> | sort | uniq -c` reporta los seis veredictos; toda fila `RESUELTO-NO-ASENTADO` de `no-corrido.tsv` tiene `estado=CERRADA` con `cerrado_por=<este acto>`; ninguna fila `DE-MESA` cambia de estado.

## 2 · FIRMAS DE MESA
Ninguna nueva: este acto asienta y clasifica; no decide. Las firmas que encuentre ya dadas (en `decisiones.tsv`, en encargos archivados con firma verbatim, en ADR) se **citan** para cerrar; una fila cuyo cierre exija una firma que no existe en el repo se rotula `DE-MESA` y se lista en la nota — no se cierra.

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
- `[EJECUTADO]` Inventario adjunto: 806 líneas, sha256 `8d02b03e920c7461…`; cita 29 FP, 234 NC, 29 PR; secciones §1.1–§5.
- `[EJECUTADO]` Diferencias ya visibles entre su corte y main de hoy: firmas ABIERTA **12 → 17** (`firmas-pendientes.tsv`); NC ABIERTA **208 → 212**; ramas en origin **5 → 0** (`git ls-remote --heads origin`: las cinco de §4.2 fusionaron — #989, #987, #994, #988, #985); `N_corridas_selladas` **82 → 154** (`corrida0.py status`), luego parte de §1.5 («corridas que no cuentan») y de §5 (NC-0257, NC-0284: registro/verify en caja) puede estar resuelta por #866/#871/#874 (replay y pisos) — **a comprobar por id de CALC, no por conteo**.
- `[LEÍDO]` Inventario §2.9: 41 filas con razón en prosa (p. ej. `EJECUCION-AUTORIZADA-PARCIAL-POR-MESA-10SEP`, `MEDICION-ACADEMICA-Y-PANEL-REALIZADOS`); el propio inventario dice «revisar primero». A.14 exige razón de la lista cerrada; A.16 exige token en el campo.
- `[LEÍDO]` Inventario §4.1: 28 encargos sin `## CONSUMIDO` — 13 CAJA, 11 sin entorno, 4 NUBE; varios son de las series `POST-693/707/723` del 11/sep, anteriores a la plantilla v2.0 y a la regla de señal. No sé cuáles siguen vigentes: **el acto lo lee por objeto**.
- `[EXISTE]` `tools/digesto_tramite.py --mesa`, `tools/corrida0.py status`, `tools/tablero_programa.py --actualiza`. No sé si el inventario se generó con alguno de ellos ni si hay un generador propio; si lo hay, se reutiliza; si no, el TSV de clasificación es el entregable y no se construye herramienta nueva (D-14).
- `[SUPUESTO]` La mayoría de las filas `SUSTITUIDO-POR` (2), `DECLARADO` (1) y una fracción grande de `FUERA-DE-PERIMETRO` (66) están `RESUELTO-NO-ASENTADO` porque el acto nombrado como sucesor ya corrió. Por qué lo creo: 130 PR en tres días. Si resulta falso, la fila queda `VIGENTE` y no pasa nada.
- ADJUNTOS: `PENDIENTES-PROGRAMA.md` · `8d02b03e920c7461…`. Si no viaja, PARA.

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO
- `ls forense/notas/ | grep -i "PENDIENTES\|RECONCILIA\|CUADERNO"` → reporta; al redactar existe `GEN2-CUADERNO-DE-MESA-1` (21/sep) con otro objeto (decisiones de mesa), no una reconciliación del inventario.
- `grep -c "RESUELTO-NO-ASENTADO" forense/no-corrido.tsv forense/hallazgos.md` → 0 al redactar: el vocabulario de este acto no existe todavía; se declara aquí y se registra en `registro-rotulos`.
- Al ejecutor: **repítela tú con tu acceso.**

## 5 · PIEZAS — resultado esperado, no receta
- **P1 · Re-derivar antes de clasificar.** Cada conteo del §0 del inventario re-derivado hoy por comando (firmas, NC por razón, corridas que no cuentan por `cuenta_gen2`, ramas, encargos sin CONSUMIDO, WARN nuevos, subcomandos sin implementar); tabla «21/sep → hoy» al inicio de la nota. Queda bien si ninguna cifra viene del inventario: todas del árbol.
- **P2 · Clasificación por ítem.** El TSV del «Hecho»: una fila por FP (§1.1), por NC (§1.2, §1.3, §2.1–§2.9, §5), por RESULT en espera de adopción (§1.4), por corrida que no cuenta (§1.5), por encargo sin consumir (§4.1). Para cada `RESUELTO-NO-ASENTADO`, la cita que lo prueba (ADR, PR, commit, fila de `corridas.tsv`, encargo con CONSUMIDO). Queda bien si un lector puede verificar cada veredicto con la cita sin leer la nota.
- **P3 · Asentar lo asentable.** (a) NC `RESUELTO-NO-ASENTADO` → CERRADA con cita y `cerrado_por`. (b) NC `MAL-ROTULADO` (§2.9): razón reemplazada por el token A.14 que corresponde **si** la autorización citada existe en el repo (fila, ADR o encargo con firma verbatim) — y entonces, si además está resuelta, se cierra; si la autorización no se encuentra, queda `VIGENTE` con la prosa intacta y se lista. (c) FP cuya firma ya conste en `decisiones.tsv` → FIRMADA con cita. (d) Encargos §4.1 cuyo objeto ya lo hizo otro acto → sección `## CONSUMIDO — SUPERADO-POR <acto>` añadida al final del archivo (A.3: nunca editando el cuerpo). (e) `SUSTITUIDO-POR` y `DECLARADO` → cerradas si la sustitución consta.
- **P4 · Dos listas de salida, y solo dos.** `DE-MESA`: cada fila con la pregunta en una línea RH (qué se pide, qué desbloquea) — es lo que dirección lleva a mesa; **no se cierra ninguna**. `DE-CAJA`: la §5 depurada — solo lo que de verdad exige corpus, microdato o red, con el comando exacto que caja debe correr por fila; lo que ya resolvió el replay/pisos sale de la lista con su cita. Esta segunda lista **es el insumo de `GEN2-PENDIENTES-CAJA-1`**: se archiva como `forense/notas/<fecha>-PENDIENTES-CAJA-lista-v1_0.tsv` con sha256 en la nota.
- «si `[SUPUESTO]` resulta falso»: pocas filas resueltas → el entregable es igual de válido: un inventario vigente cotejado, y la lista de mesa más larga.

## 6 · LATITUD
DECIDES TÚ: el orden de secciones; cómo cruzar ids (por objeto: CALC, ADR, PR, encargo — nunca por frase); regenerar vistas por comando; reutilizar el generador del inventario si existe; corregir una cita rota ≤ 10 líneas declarándola.
PREGUNTAS A MESA (con opciones y recomendación, y sigues): una fila `DECISION-DE-MESA-PENDIENTE` cuyo objeto ya decidió otra firma posterior con otro rótulo (p. ej. F6 y FP-374) — ¿cierra por superación citando la firma nueva (recomendado) o queda `DE-MESA`? Sigue clasificando las demás mientras tanto.
NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada
a) no aplica (cero microdato) · b) borrar, forzar o reescribir algo sellado — **cerrar una NC no es borrarla**: el texto queda; solo cambian `estado` y `cerrado_por` · c) adoptar (§1.4 se lista, no se adopta) o mover contadores vedados · d) no aplica · e) entorno equivocado · f) OBJETIVO inalcanzable → PARO como entregable.

## 8 · COMPUERTAS
Ninguna que proteja abrir dato, congelar spec, adoptar o borrar. Orden sugerido: P1 antes que todo, porque decide cuántas filas quedan.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/no-corrido.tsv` (estado, cerrado_por, razón solo en `MAL-ROTULADO` con autorización citada) · `forense/firmas-pendientes.tsv` (solo FIRMADA con cita) · `forense/encargos/*` (solo apéndice `## CONSUMIDO — SUPERADO-POR`) · `forense/notas/<fecha>-GEN2-PENDIENTES-RECONCILIA-1-{clasificacion,nota}.*` · `forense/notas/<fecha>-PENDIENTES-CAJA-lista-v1_0.tsv` · `canon/registro-rotulos.tsv` (vocabulario de este acto) · `canon/L0/<ADR-raíz>.md` · hallazgos propios.
Ajeno que no se toca: `data/corrida0/` (ningún registro ni adopción: eso es caja), `decisiones.tsv` (se lee para citar; no se escribe: no hay firma nueva), `milpa/`, specs, CALC, el informe, el estado.
Archivos que OTRO ACTO EN VUELO esté tocando ahora: **ninguno verificado** al redactar (sin ramas vivas). Si `GEN2-PENDIENTES-CAJA-1` arranca antes de que este acto fusione, comparte `no-corrido.tsv`: quien fusione después re-aplica sus cierres (ids con raíz, sin renumerar).
«Si te encuentras escribiendo fuera de esta lista, PARA.»
PERÍMETRO DE CIERRE — permanente (D-21).

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA · CIERRE
No hace: no decide por mesa, no adopta, no registra corridas, no abre payloads, no borra texto de ninguna fila, no construye herramienta nueva.
Sucesores: `GEN2-PENDIENTES-CAJA-1` (consume la lista `DE-CAJA`); `GEN2-TRAMITE-FIRMAS-6` (dirección, con la lista `DE-MESA` contestada por mesa).
Auditoría de rigor extremo: no aplica (afirma sobre el tablero, no sobre México).
Cierre: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` los añade /acto al final del archivo archivado; adendas de mesa como archivo propio `<este-encargo>-ADENDA-N.md`.
