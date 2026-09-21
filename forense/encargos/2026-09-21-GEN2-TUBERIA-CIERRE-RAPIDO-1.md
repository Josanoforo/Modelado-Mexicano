# ENCARGO · ACTO GEN2-TUBERIA-CIERRE-RAPIDO-1 · v1.1 · LA SESIÓN VERIFICA EN SEGUNDOS Y EL CI JUZGA · LOS DERIVADOS SALEN DE LOS PR · T16 SE RETIRA Y LA DERIVACIÓN SE HACE UNA VEZ · LA SUITE PASA A ESTRICTA Y SE QUEDA SÓLO CON FAIL/VERDE

**v1.1 sustituye a v1.0.** Cambia el punto (5) de la firma: el canal de WARN no pasa a delta, **se retira**. La clasificación de cada familia la hizo TUBERÍA con la regla de mesa y está en P-C.3.

**CABECERA** · redactado contra `b67d09f5` (re-deriva al abrir; si `main` se movió no es PARO) · **ENTORNO: NUBE**, `cloud_default`, con credenciales de Git y publicación de PR; cero microdato. Si la sesión tiene `gh` con credenciales, hace las sondas de P0; si no, quedan como pregunta a mesa y **no es PARO** · una sola sesión, rama propia (D-17) · **MODO: ABIERTO** · **MODELO SUGERIDO: Opus** · **COMPUERTA: ninguna** — no abre dato, no congela spec, no adopta, no borra (D-20); la re-derivación de P-D escribe vistas derivadas, no resultados · **CONTADOR: `cuenta_gen2 = NO`**; `status` y el contador **no se mueven** · vehículo: `/acto`.

**EL PR NO SE FUSIONA EN ESTE ACTO**: queda propuesto; mesa central fusiona.

**LOTE (D-11): cuatro piezas, en este orden: A → B → C → D.**

**IDS.** Todo con raíz de acto: `ADR-<AAMMDD>-GEN2-TUBERIA-CIERRE-RAPIDO-1-<hhhh>-<NN>`.

**Este acto es el último que corre la suite completa en local para cerrar**: la cascada vieja rige hasta que P-A esté en la rama.

---

## 1 · FIRMA DE MESA, verbatim (21/sep/2026)

> «(1) Antes de empujar, un acto corre solo el subconjunto rápido de la suite; la suite completa la corre el CI una vez en el push y ése es el juez. (2) Los archivos derivados no viajan en los PR: un job del push a main los re-deriva y commitea. (3) T16 se retira; una sola derivación compartida por T32, T32-quater, T45 y el marcador, con salida idéntica; la cascada corre la suite una vez. (4) Los reports GEN1 de T06/T08 se declaran históricos; el baseline se re-congela con lo que ocurre hoy y la suite pasa a estricta. (5) El canal de WARN se retira. Cada familia pasa a FAIL acotado a los archivos que el PR toca, o a un contador del tablero derivado por comando; lo que no sea ninguna de las dos se borra. T10 pasa a FAIL acotado. El baseline deja de guardar WARN. Meta verificable: CONSUMIDO → merge ≤ 10 min de mediana, ≤ 1 re-fusión por PR, suite local ≤ 15 s.»

El punto (5) es el texto corregido que mesa dio el 21/sep, verbatim, en sustitución del original («Los WARN se reportan como delta contra la base»).

**No está en el repo: este acto la asienta (A.12).** Autoriza a este acto sobre: `tests/check.py`, `tools/cierre_acto.py`, `tests/test_marcador_segmento.py` y los tests de T32, T32-quater y T45, los tests que hoy fijan la emisión de WARN, `tools/tablero_programa.py` (los contadores nuevos), `.github/workflows/verify.yml`, y en `.claude/commands/acto.md` los pasos que corren la suite o commitean derivados.

## 2 · PREMISAS VERIFICADAS POR TUBERÍA — con rótulo

**Se sostienen:**
- `EJECUTADO` · T16 sigue registrado en `tests/check.py`, y `acto.md` corre la suite en las líneas **349, 401 y 473**.
- `EJECUTADO` · Después de `#962` entraron **12 PR**: **cero renumeraciones**; re-fusiones entre 0 y 4, **28 en total**.
- `EJECUTADO` · Ningún test comprueba que las vistas derivadas estén al día: sacarlas de los PR **no pone rojo ningún PR**.
- `LEÍDO` · E.7 ya prevé el caso: *«Toda corrida sellada entra a la vista en el mismo acto que la sella, **o su CONTADOR dice "sellada en disco, no registrada"**»*. Sacar los derivados de los PR **no exige cambiar las instrucciones**: exige que el acto use esa segunda forma.
- `EJECUTADO` · Los tests caros nunca fueron los únicos en atrapar un defecto en la ventana medida (T32: 3 fallos, T35: 4, T32-quater: 0; todos junto con otro test).

**No se sostienen, y cambian lo que este acto puede prometer:**

1. **La causa principal de las re-fusiones que quedan no son los derivados, son los archivos de gobierno donde todos añaden.** En los 28 merges de `main` hacia rama de los 12 PR posteriores a `#962`, los archivos que **los dos lados** tocaron: `forense/hallazgos.md` 25 · `forense/no-corrido.tsv` 24 · `canon/gobernanza-v1_15.md` 23 · `canon/registro-rotulos.tsv` 23 · `forense/firmas-pendientes.tsv` 15 · `forense/analisis/ci-guardias/censo-tests.tsv` 14 · `data/INFRAESTRUCTURA-v1_0.md` 10 · y **`corridas.tsv` y `resultados.tsv` 6 cada uno**. Los derivados explican **6 de 28**. Los de gobierno ya son `union` y se resuelven solos **en la fusión local**, pero el botón de GitHub no aplica `union`: dos PR que añaden al final del mismo archivo chocan en el servidor, y eso obliga a re-fusionar. **Este acto hace lo que firma mesa y medirá su efecto, pero la meta de «≤ 1 re-fusión por PR» no se alcanza sólo con él**: hace falta que los actos dejen de añadir líneas a archivos compartidos y escriban **un archivo por entrada**. Ese cambio ya lo autoriza la firma del 21/sep —«lo que se añade a los archivos de gobierno deja de poder chocar entre PR; TUBERÍA elige el mecanismo»— y es el sucesor inmediato (§9).
2. **El subconjunto rápido no cabe en 15 s con las guardias huérfanas dentro.** Medido en local: T02 7.35 s · T22 0.29 · T25 0.44 · T15 0.24 · T27 0.03 · T30 0.02 · T34 0.04 · el verificador de sidecars 0.4 → **~8.8 s**. `ci_guardias.py --ejecuta-huerfanos`: **33.4 s** (37 s de mediana en el runner). Las guardias huérfanas **se quedan en el CI**, que ya las corre, y el subconjunto local es el resto. Así la meta de 15 s se cumple.

**Sin verificar**, `SUPUESTO`: si `main` exige ramas al día, si la protección de `main` deja que un job de Actions empuje a `main`, y si una sesión en la nube puede leer el resultado del CI de su propio PR. P0 los sondea.

**El canal de WARN, medido** (`EJECUTADO` sobre `main` `e860e77f`, salvo rótulo):
- La suite emite hoy **24 384 WARN** —esta mañana eran 14 337: crecen con cada acto— en **9 tests**: T-REPRO 23 859, T-NO-CORRIDO 207, T03 161, T22 76, T10 65, T-SUCESOR-EXISTE 11, T13 3, T-CRON 1, T-ALTA-RELACION 1.
- `tests/baseline.json` guarda **142 WARN** para compararlos en cada corrida.
- Los emiten **dos funciones** de `tests/check.py`, `warn()` y `senal()`, desde **22 sitios** distintos; varios no disparan hoy pero pueden disparar (T12, T20, T21, T23 ×2, T46, T50). `senal()` ya se vuelve FAIL en modo estricto.
- `REPORTADO` por mesa: ningún hallazgo ni `NC` registra una acción tomada por un WARN; las 119 menciones del repo hablan del mecanismo.
- **Consumidores del canal:** `tests/test_suite_warn_estado.py` (su objeto es el propio canal), `tests/test_t_cron.py`, `tests/test_adq_cableado.py` (fija que T-CRON emita con `senal()`), `tests/test_check_parallel.py`, `tests/test_tuberia_ids_union.py` (el caso H3) y `tools/digesto_tramite.py:478`, que lee `d.get("warns", [])` y **no se rompe** si la clave desaparece. `tests/test_corrida0.py` menciona WARN 15 veces: se comprueba si es el canal de la suite o uno propio de `corrida0`, y en el segundo caso no se toca.
- **Fuera del perímetro, a propósito:** `tools/verifica_sidecars.py` emite su propio WARN por la firma D-a5 (encabezado ajeno tras el cuerpo sellado). No es la suite y tiene firma propia: **queda como pregunta a mesa**.

## 3 · YA HECHO — por OBJETO (A.8)

- Carril de derivados: **EXISTE-NO-SATISFACE** — `tools/deriva_cron.sh` y `.claude/commands/deriva.md` abren un PR diario `derivados/<fecha>` (el último, `#952`, sólo tocó el tablero). Es un PR más que mesa fusiona, no un job que re-derive en cada push.
- Subconjunto rápido, derivación compartida, FAIL acotado a lo tocado, contadores de estado en el tablero: **NO-ENCONTRADO**.
- `tests/baseline.json` acepta **15 FAIL**, de los que hoy ocurren **3** (T06 ×2, T08 ×1): los otros 12 (T02 ×10, T16 ×2) están vencidos. Tiene además una clave `warns` que sirve de base para el delta.
- Consumidores de `tests/baseline.json` o del modo `--baseline`: `check.py`, `cierre_acto.py`, `digesto_tramite.py` (de dirección), `tablero_programa.py`, `deriva_cron.sh`, `bitacora.py`, `corpus.py`, `test_t_cron.py`, `test_suite_warn_estado.py`, `test_check_parallel.py`, seis comandos de `.claude/commands/`, la plantilla de PR y `verify.yml`. **Los de `tools/curador_registro/` usan otro baseline propio**: se confirma y no se tocan.

## 4 · PIEZAS — resultado esperado, no receta

**P0 · 0-bis, firma y sondas.** Este encargo verbatim desde el `.md` recibido, con su sello de cuerpo. Chequeo de duplicado por contenido. **Asienta la firma de §1 verbatim.** Y, si hay `gh`: (i) si la protección de `main` exige ramas al día (`required_status_checks.strict`); (ii) si permite que `GITHUB_TOKEN` empuje a `main`; (iii) si la sesión puede leer el resultado del CI de su propio PR. Sin `gh`, las tres van a la nota como preguntas a mesa.

**P-A · La sesión verifica en segundos; el CI juzga.**
1. **Un solo comando para el subconjunto rápido**: T02, T22, T25, T15, T27, T30, T34 y el verificador de sidecars. La lista vive **en un solo sitio**, con una línea por test que diga por qué está —su evidencia de captura en la medición de `#955`—. **Presupuesto: ≤ 15 s en local**, medido y reportado.
2. **`acto.md`**: las tres corridas de la suite (349, 401, 473) se sustituyen por **una** corrida del subconjunto antes de empujar. Donde hoy dice «VERDE», dice: *el juez es el CI del push; si falla, la sesión corrige y vuelve a empujar*. `cierre_acto.py` deja de correr la suite completa dentro de su fase A.
3. **T16 se retira** de `check.py`: cero afirmaciones vigentes que comparar, cero fallos propios en 66. **Sus dos FAIL del baseline salen con él** (P-C).

**P-B · Una sola derivación del árbol, compartida.** T32, T32-quater, T45 y `tests/test_marcador_segmento.py` calculan hoy la misma derivación del árbol real muchas veces —el marcador llama a `deriva()` **11 veces** (~12 s cada una, mismo resultado); T32-quater deriva el registro **5 veces**; T32 corre `status` sobre el árbol real **7 veces**; T45 relanza `corrida0 status` en un subproceso—. Se calcula **una vez por proceso** y cada caso recibe **una copia**, para que ninguno altere lo que ve el siguiente. Una llamada que se haga **a propósito** con datos alterados se deja como está. **Criterio, no negociable**: la salida de cada uno de esos tests —y el conjunto de FAIL y WARN de la suite— es **byte a byte idéntica** antes y después, con el `diff` en la nota.

**P-C · La suite pasa a estricta y se queda sólo con FAIL o VERDE.**
1. **Los reports GEN1 que hacen fallar T06 y T08 se declaran históricos** (E.1: GEN1 es historia). La lista se **deriva** de los FAIL de hoy de T06 y T08, y vive **en un solo sitio**; **los reports no se editan**. T06 y T08 siguen vigilando todo lo demás.
2. **El baseline se re-congela** con lo que ocurre hoy. Tras el punto 1, eso es **cero FAIL aceptados**: el modo línea base queda con la misma semántica que el estricto. El archivo **se conserva** —vacío de FAIL—, para no romper a sus quince consumidores ni a `digesto_tramite.py`, que es de dirección. **El paso de CI «transporte paralelo, compuerta y semántica del baseline» se quita** si, con cero FAIL aceptados, ya no protege nada; si protege algo, se declara qué y se deja.
3. **El canal de WARN se retira de la suite.** `warn()` y `senal()` desaparecen; la suite queda **FAIL o VERDE, nada más**, que es lo que D-16 ya decía. Cada uno de los 22 sitios va a uno de tres destinos. **La clasificación la hizo TUBERÍA con la regla de mesa**; el ejecutor la aplica y, si al leer un sitio encuentra que su mensaje dice otra cosa, lo declara y lo corrige:

| Sitio (test, función) | Hoy | Qué dice | Destino |
|---|---:|---|---|
| T-REPRO (`t35_repro`, dos sitios) | 23 859 | «SELLADA-SIN-ADOPTAR: activo GEN2 y sin consumidor — antigüedad N» | **CONTADOR**: «N RESULT GEN2 sellados sin consumidor activo · el más viejo: X días». Las líneas por RESULT se borran. |
| T-NO-CORRIDO (`t34_no_corrido`) | 207 | «NC ABIERTA desde fecha (N días) — sucesor X» | **CONTADOR**: NC abiertas por antigüedad |
| T22 (`t22_firmas`, dos sitios) | 76 | «FP ABIERTA desde…», «FIRMADA sin ejecutar desde…» | **CONTADOR**: firmas abiertas y firmadas sin ejecutar, por antigüedad |
| T23 (`t23_cableado`, dos sitios) | 0 | «N filas en estado X», «N propuestas no integradas» | **CONTADOR**: cableado por estado |
| T-CRON (`t31_cron`) | 1 | estado del último censo de adquisición | **CONTADOR**: estado del último censo |
| T03 (`t03_dangling_refs`) | 161 | «X cita Y, que no existe» | **FAIL acotado** a archivos que el PR toca. Las 161 viejas → una `NC` de deuda |
| T13 (`t13_version_header`) | 3 | «canon/X sin bloque de cabecera» | **FAIL acotado**. Las 3 viejas → `NC` de deuda |
| T-SUCESOR-EXISTE (`t43_sucesor_existe`, dos sitios) | 11 | «la NC X cita un sucesor que no existe» | **FAIL acotado a las filas** que el PR añade o modifica en `no-corrido.tsv`. Las 11 viejas → `NC` de deuda |
| T10 (`t10_diaspora_unmarked`) | 65 | «muestra de diáspora sin (b)» | **FAIL acotado** —decisión de contenido de mesa—. Las 65 viejas son de reports GEN1, que pasan a históricos con T06/T08 |
| T12 (`t12_counts`) | 0 | «X declara N reglas; el motor tiene M» | **FAIL acotado** al documento que declara y al motor |
| T20 (`t20_cascada_marcada`) | 0 | «ningún sitio con el marcador `T20:HITO-D`» | **FAIL acotado** a `README.md` y `canon/*.md` |
| T21 (`t21_capa2_capa3`) | 0 | «capa2 fuera de la correspondencia» | **FAIL acotado** a `relaciones.tsv` |
| T-ALTA-RELACION (`t38_alta_relacion`) | 1 (sólo en local) | «NO-CORRIDO: falta `jsonschema`» | **FAIL**, sin acotar: un test que no corre en CI es un defecto. En el runner no dispara —la dependencia se instala— y el subconjunto local no lo incluye |
| T46, T50 (sin universo) | 0 | «`.gitattributes` no declara ningún `merge=union`» | **BORRAR**: no obliga a nadie ni cuenta nada; el falsador de cada guarda ya cubre ese caso |
| T16 (dos sitios) | — | — | sale con T16 (P-A.3) |

**Cómo se acota.** La suite calcula **lo que el cambio toca**: en local, contra el `merge-base` con `origin/main`; en el CI de un PR, contra el primer padre de la ref de merge; en el push a `main`, contra `HEAD^1`. Para eso el job `suite` clona con **profundidad 2** desde el principio —no hace `fetch` después (D-23)—. **Si no puede calcular lo tocado, falla en voz alta**; nunca asume «todo» ni «nada».

**La deuda vieja** (T03, T13, T-SUCESOR-EXISTE) se lista **una vez** en `forense/analisis/deuda-warn-1/`, una tabla por familia, y cada familia recibe **una `NC` de deuda** que cita su tabla. Se cierran cuando toque; no bloquean a nadie.

**Los contadores** los deriva `tools/tablero_programa.py` en el tablero —que P-D regenera en el push a `main`—, con el comando a la vista en la nota.

**El baseline deja de guardar WARN**: la clave `warns` y la comparación «WARN nuevos» desaparecen. `tests/test_suite_warn_estado.py`, cuyo objeto es el propio canal, se retira con esa razón; `test_t_cron.py`, `test_adq_cableado.py`, `test_check_parallel.py` y el caso H3 de `test_tuberia_ids_union.py` se adaptan al destino nuevo **sin perder lo que aseveran de fondo**.

**P-D · Los derivados salen de los PR.**
1. **Qué es derivado se decide por dos condiciones, no por lista a mano**: la primera línea lleva la marca `DERIVADO — NO EDITAR` —y no `NO ES DERIVADO`, como `pines-de-mesa.tsv`—, **y** un comando lo regenera **byte a byte idéntico** desde lo committeado, en un clon limpio sin corpus. Candidatos: `data/corrida0/corridas.tsv`, `resultados.tsv`, `usos.tsv`, `demanda-corridas.tsv`, `demanda-resultados.tsv`, `relevo-usos-v1_0.tsv`, `marcador-segmento.tsv` y `forense/tablero/TABLERO-PROGRAMA.md`. El que no cumpla las dos, **se queda en los PR** y la nota dice por qué.
2. **Un job del push a `main`** re-deriva esos archivos por comando y, si cambiaron, los commitea sobre `main`. **Sólo ese job** tiene permiso de escritura (`contents: write`); los demás siguen en lectura. Con `workflow_dispatch` y un modo de ensayo que re-deriva y muestra el `diff` **sin commitear**, para probarlo en la rama de este acto.
3. **La guarda**: en un PR, modificar un archivo derivado **falla en CI**, con el mensaje *«no commitees derivados; el job del push a `main` los re-deriva»*. Probada por mutación.
4. **`acto.md`**: el acto que sella un CALC ya no escribe las vistas; su `CONTADOR` dice **«sellada en disco, no registrada»**, que es la forma que E.7 ya admite. El job la registra al fusionar.
5. **Si la sonda (ii) dice que la protección impide que Actions empuje a `main`**, no es PARO: la sesión sigue con todo lo demás y pregunta a mesa entre (a) permitir a Actions ese empuje y (b) que el job abra o actualice un único PR `derivados/auto`, como el carril diario. **Recomendación de TUBERÍA: (a)**, porque (b) añade un PR que mesa debe fusionar por cada cambio.

**P-E · Cierre.** La cascada nueva, **por primera vez**: subconjunto rápido en local, el CI como juez. `## NO-CORRIDO / RESERVAS` al final; `## CONSUMIDO` con el PR real. Hallazgos: la tabla de §2 —qué archivos causan las re-fusiones—, la tabla de P-C.3, y dos semillas PARA-v2.16: *la verificación local es el subconjunto que atrapa; la suite completa la corre el CI*, y *la suite no tiene tercer estado: un defecto es FAIL acotado a lo que se toca; un estado es un contador* —que sustituye la cláusula de WARN de D-16—.

## 5 · CRITERIO DE «HECHO» — por comando, con salida cruda en la nota

1. La firma está asentada.
2. El subconjunto rápido corre en **≤ 15 s** en local, medido.
3. `acto.md` corre la suite **una vez** —el subconjunto— y `cierre_acto.py` no la corre completa.
4. T16 no está en `check.py`.
5. Las salidas de T32, T32-quater, T45 y el marcador, y el conjunto de FAIL y WARN de la suite, son **idénticos** antes y después de P-B.
6. La suite completa, en modo estricto, da **cero FAIL** sobre el árbol final, y el baseline acepta **cero FAIL**.
7. La suite no emite ningún WARN: su salida es FAIL o VERDE. Cada uno de los 22 sitios está en su destino, con la tabla de P-C.3 en la nota; las tres `NC` de deuda existen; los contadores aparecen en el tablero; y un FAIL acotado se dispara ante una mutación en un archivo tocado y **no** ante la deuda vieja.
8. El ensayo del job de derivados muestra que cada archivo derivado se regenera **byte a byte idéntico**; la guarda de P-D.3 falla ante su mutación.
9. El CI del PR de este acto está en verde. **Ése es el juez.**

## 6 · LATITUD

El cómo es tuyo. Un obstáculo reversible y barato se resuelve y se declara (D-19). Si `main` se mueve, fusiona hacia la rama.

## 7 · PAROS — lista cerrada

Aflojar o quitar una aserción de cualquier test salvo T16 · convertir en FAIL **sin acotar** una familia que hoy tiene deuda vieja —pondría rojo a todos los PR— · que una salida de P-B cambie un byte · editar el texto de un report GEN1 · dar permiso de escritura a otro job que no sea el de derivados · que el job de derivados commitee algo que no sea un archivo derivado · que `status` o el contador cambien · abrir microdato · reescribir la historia · objetivo inalcanzable. **Fuera de esta lista no se para.**

## 8 · PERÍMETRO

Escribes en: `tests/check.py` · `tests/baseline.json` · `tests/test_marcador_segmento.py` y los tests que alimentan T32, T32-quater y T45 (sólo para compartir la derivación) · `tests/test_suite_warn_estado.py` (se retira), `tests/test_t_cron.py`, `tests/test_adq_cableado.py`, `tests/test_check_parallel.py` y `tests/test_tuberia_ids_union.py` (sólo para adaptarlos al destino nuevo) · `tools/tablero_programa.py` (los contadores) · `forense/analisis/deuda-warn-1/` · el comando del subconjunto rápido · `tools/cierre_acto.py` · `.github/workflows/verify.yml` (el job de derivados, la guarda de P-D.3 y, si procede, quitar el paso del baseline) · `.claude/commands/acto.md` (los pasos que corren la suite o commitean derivados) · los archivos derivados de P-D (sólo para probar la regeneración) · `forense/encargos/`, `forense/notas/`, `forense/hallazgos.md`, `forense/no-corrido.tsv` · lo que asienta la firma · y la cascada. Más D-21. **Si te encuentras escribiendo fuera de esta lista, PARA.**

**No tocas:** los reports GEN1 · `tools/digesto_tramite.py` · `tools/corrida0.py` · `tools/curador_registro/` · `tools/verifica_sidecars.py` (su WARN tiene firma propia, D-a5) · los demás comandos de `.claude/commands/`.

## 9 · LO QUE NO LOGRA POR SÍ SOLO, Y EL SUCESOR

La meta **«≤ 1 re-fusión por PR»** necesita el sucesor. Con los datos de §2, los derivados explican 6 de las 28 re-fusiones posteriores a `#962`; el resto viene de los archivos de gobierno donde todos añaden. **Sucesor: un archivo por entrada** para `hallazgos.md`, `no-corrido.tsv`, `gobernanza-v1_15.md`, `registro-rotulos.tsv`, `firmas-pendientes.tsv`, `censo-tests.tsv` e `INFRAESTRUCTURA-v1_0.md`, con sus vistas completas derivadas por comando —y, tras este acto, regeneradas por el mismo job—. Ya lo autoriza la firma del 21/sep.

**Las metas de tiempo** —CONSUMIDO → merge ≤ 10 min de mediana— se miden **después de fusionar**, sobre los PR siguientes: este acto deja escrito el comando que lo mide.

## 10 · FALSADOR

Si en dos semanas una sesión rompe `main` con un FAIL que el subconjunto rápido habría atrapado, el subconjunto está mal elegido. Si el job de derivados deja `main` con una vista distinta de la que su comando produce, el job está mal.
