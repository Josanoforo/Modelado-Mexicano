# ENCARGO · ACTO GEN2-TRAMITE-PENDIENTES-1 · La revisión de pendientes queda sellada: tres firmas cortas asentadas, doce RESULT en una hoja firmable en bloque, cinco NC sin dueño con dueño, y la bandeja del titular en una sola hoja

> ENTORNO: **NUBE** — cero microdato. El hook imprime ENTORNO-DERIVADO; si no coincide, PARA en una línea.

CABECERA · SHA de redacción `31da26e0` (merge de #1001, 22/sep/2026; re-deriva al abrir — hay nueve PR en cola de merge) · una sola sesión (D-17) · MODELO: Opus (P2 deriva valores y universos; el resto es propagación) · MODO: **ABIERTO** · CONTADOR: cero mediciones; mueve `no_corrido_abiertas` a la baja (reportado), `cuenta_gen2` de 4 corridas (SI) y de 3–5 lecturas Codex (NO); **no** adopta ningún RESULT (P2 abre la FP; adopta mesa por merge) · ids raíz de acto (D-24), los deriva `tools/cierre_acto.py`.

## 1 · OBJETIVO
Que lo que la revisión de pendientes produjo (#1000 RECONCILIA-1, #1004 PENDIENTES-CAJA-1) y lo que mesa decidió sobre ella quede en el tablero, y que lo que mesa **no** ha decidido todavía esté escrito como pregunta con opciones — no disperso en dos notas de 300 líneas. «Hecho» = sobre el commit final con `origin/main` fusionado: `decisiones.tsv` con una fila por firma de §2 que sobreviva al lanzamiento; `grep -c PENDIENTE-DE-MESA data/corrida0/corridas.tsv` menor que al abrir en exactamente las 4 corridas de P1(a); una FP nueva con raíz de acto que lista los 12 RESULT con consumidor, valor GEN1, valor GEN2, delta y universo; las cinco NC de P3 con `sucesor` no vacío y ninguna de ellas cerrada sin cita; `forense/notas/<fecha>-BANDEJA-TITULAR.md` con 15 entradas (10 NC + 5 HUMANO), cada una con receta.

## 2 · FIRMAS DE MESA — verbatim; mesa borra la línea que no firme y edita la que quiera; lo que queda es la firma
- **P1(a) · cuenta_gen2 de cuatro corridas Codex:** «FIRMA DE CONTADOR, mesa, 22/sep/2026: `cuenta_gen2 = SI`, no adopta, para `CALC-EDER2017-PRIMERA-UNION-SEXO-COHORTE-0002`, `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001`, `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0002` y `CALC-WBES2023-PRECISION-INTERACCIONES-0001`: microdato con cadena; el PENDIENTE era de etiqueta, no de procedencia.»
- **P1(b) · lecturas WBES/ENIGH del carril Codex (NC-0316, NC-0320, NC-0321, NC-0326):** «Corpus, no motor: `cuenta_gen2 = NO`; se citan en el report TRA como descriptivas sin diseño muestral, con ese rótulo, cuando el report se re-selle. No se insertan en `tramite.yaml` ni en el catálogo.»
- **P1(c) · NC-0259 (190 identidades por acreditar a mano):** «Queda VIGENTE-CAJA sin acreditar hasta que un consumidor concreto las pida; se cierra por demanda, no por limpieza.»
- **P3 · 7ef3-02 (la cifra «18 de 20»):** «Dirección no tiene fuente para «18 de 20»: era una cifra tecleada. La frase del producto se reescribe con la cobertura derivada, 26/35 (R dentro del IC del candidato, v2.16 §4), en el informe v1.3; la NC cierra con esta línea.»
- **P3 · 8e53-04 (configuración del repositorio — solo mesa la puede leer):** «Protección de rama en `main`: ___ · merge queue: ___ · quién puede fusionar: ___.» *(mesa rellena las tres; si no rellena, la NC queda ABIERTA con este texto como pregunta.)*
- **Ya selladas, se citan:** T5/T6 (FP c09b-01, c09b-02, 0af9-01: asentadas en #1004/#1005); dictamen `EN-ESPERA-PANEL` de FP-374 (`FP-260922-GEN2-FP374-RESELLO-1-dfbe-01`, FIRMADA, #998); v2.16 E.2 («la etiqueta basta para contar porque mesa fusiona cada PR») y E.6 («toda ola nueva … nace RESERVADA»).

## 3 · LO QUE DIRECCIÓN SABE — cada línea con su rótulo
- `[LEÍDO]` `forense/notas/2026-09-22-GEN2-PENDIENTES-RECONCILIA-1-nota.md` §3 (289 ítems: 216 VIGENTE · 62 DE-MESA · 9 VENCIDO · 2 DE-CAJA · 0 RESUELTO-NO-ASENTADO · 0 MAL-ROTULADO), §4 (lista DE-MESA: 10 bandeja del titular, ~20 NC DECISIÓN-DE-MESA, 16 FP, 12 RESULT, 4 corridas), §7 (`GEN2-SENAL-1` ya había revisado 18 candidatas a cierre; 0 sobrevivieron).
- `[LEÍDO]` `forense/notas/2026-09-22-GEN2-PENDIENTES-CAJA-1-verificacion.tsv` (rama `claude/gen2-pendientes-caja-1`, PR #1004): 49 filas → 11 RESUELTO-ANTES · 7 RESUELTO · 14 VIGENTE-CAJA · 12 DE-MESA · 5 HUMANO (NC-0156, NC-0166, NC-0202, NC-0278, `TUBERIA-SIDECAR-CUERPO-1-3d08-02`) con recetas H1–H5 en su nota §3.3/§4.
- `[LEÍDO]` Las cinco NC sin dueño, `forense/no-corrido.tsv`: `VALIDACION-INDEPENDIENTE-PILOTOS-1-7ef3-02` (pide la fuente de «18 de 20»; con 35 celdas la cobertura es 26/35 o 30/35); `TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-01` (corridas/resultados.tsv chocan porque cada acto los re-deriva enteros; tocar esto toca E.7); `…-8e53-04` (protección de rama: solo mesa); `CUADERNO-DE-MESA-1-b6dc-02` (tres preguntas de regla: (i) contar por etiqueta, (ii) respaldo en una sola máquina, (iii) ola nueva reservada); `MARCADOR-E-INFORME-1-48d4-02` (`test_01…` falla por redondeo de `share_horas_mujeres_40mas`; F8 veda editarlo a mano).
- `[EJECUTADO]` `grep -c PENDIENTE-DE-MESA data/corrida0/corridas.tsv` → 22 (incluye las 4 de P1(a) y otras; el acto lista cuáles son las 4 por id y no toca las demás). `status` → `N_resultados_gen2_pendientes_adopcion = 12`. `grep "18 de 20|18/20"` → `canon/informe-programa-v1_1.md:53` y ningún RESULT: la cifra no tiene fuente sellada.
- `[EXISTE]` `forense/analisis/senal-1/nc-abiertas-por-clase.tsv` (clase `BANDEJA-TITULAR`, 10 filas). No sé si trae receta por fila: el acto la lee.
- `[SUPUESTO]` Los 12 RESULT pendientes de adopción se listan por comando (`corrida0.py status`/relevo) con su consumidor y su lectura legacy. Si el comando no los expone con valor GEN1, el acto los deriva de `relevo-usos` y `usos.tsv`; si tampoco, la hoja los lista con `valor_GEN1 = NO-DERIVADO` y lo dice.
- ADJUNTOS: ninguno; todo vive en el árbol o en las ramas #1004/#1001.

## 4 · YA HECHO / YA DECIDIDO — búsqueda por OBJETO
- Por id de las 4 corridas: `grep "<CALC>" data/corrida0/decisiones.tsv` → si ya hay fila de contador, se cita y no se duplica. Por id de los 12 RESULT: `grep "<RESULT>" data/corrida0/decisiones.tsv forense/firmas-pendientes.tsv` → si alguno ya está vetado/adoptado, sale de la hoja con cita. Para 8e53-01: `grep -i "canal-publicacion\|c09b-02\|0af9-01" data/corrida0/decisiones.tsv` → la firma T6 (si #1004/#1005 fusionaron; si no, tipo (3): se cita el PR y la NC queda con sucesor, no cerrada).
- Al ejecutor: **repítela tú con tu acceso.**

## 5 · PIEZAS — resultado esperado, no receta
- **P1 · Tres firmas cortas.** (a) fila en `decisiones.tsv` por corrida + `cuenta_gen2 = SI` proyectado por el mecanismo de la casa (`_cuenta_gen2_resuelto`, precedencia fila de mesa); (b) NC-0316/0320/0321/0326 → CERRADAS con la firma como cita y sucesor «cita en TRA v-siguiente»; `cuenta_gen2 = NO` en fila; (c) NC-0259: enmienda fechada, sigue ABIERTA. Queda bien si `status` cuenta las 4 y `corridas.tsv` deja de decir PENDIENTE-DE-MESA en esas 4 y solo en esas.
- **P2 · Hoja de adopción, sin adoptar.** Una FP nueva (raíz de acto) cuyo `qué_se_firma` es la tabla: `RESULT · CALC · consumidor (regla) · valor GEN1 (legacy, con su fuente) · valor GEN2 · delta · universo/unidad/escala · verify (RESULTADO/CONTEXTO) · recomendación del ejecutor (ADOPTAR/VETAR, con razón de una línea)`. Los dos ya vetados se citan como precedente. Regla de adopción en bloque (E.2): el merge del PR que traiga el bloque será la adopción — este acto **no** lo trae. Queda bien si mesa puede firmar la hoja entera con una palabra.
- **P3 · Cinco NC con dueño.** 7ef3-02 → CERRADA con la firma (26/35) y sucesor `informe v1.3 (dirección)`. 8e53-01 → CERRADA por superación citando T6 (canal de publicación en el push a `main`) — si T6 no está en main al abrir, enmienda fechada y sigue ABIERTA. 8e53-04 → con la respuesta de mesa: CERRADA; sin ella: ABIERTA con la pregunta escrita. b6dc-02 → (i) y (iii) cerradas citando v2.16 E.2 y E.6; (ii) enmienda: «es FP `…CORPUS-INTEGRIDAD-3d56-01`, física», sigue ABIERTA. 48d4-02 → sigue ABIERTA; enmienda fechada con el sucesor que F8 nombra (el canal, no la mano). NC-0161/0162 → enmienda fechada: sucesor = adquisición dirigida por id de manifiesto (conversación NUBE-MEDICIÓN), citando el dictamen EN-ESPERA-PANEL de #998.
- **P4 · Bandeja del titular, una hoja.** `forense/notas/<fecha>-BANDEJA-TITULAR.md`: 15 entradas (las 10 NC de clase BANDEJA-TITULAR + las 5 HUMANO de #1004), cada una con: qué escribir · a quién · qué adjuntar · qué esperar · qué NC cierra. Ninguna NC cambia de estado. Queda bien si mesa puede trabajar la hoja sin abrir el repo.
- **P5 · El hallazgo de la revisión.** Una línea en `hallazgos.md`: *«289 pendientes cotejados por objeto (#1000): 0 resueltos sin asentar desde nube — confirmado por SENAL-1; 18 lo estaban desde caja (#1004) porque solo caja podía probarlo; el resto es deuda viva con dueño. El supuesto de dirección "130 PR dejan filas resueltas sin asentar" era falso.»* Con cita a las dos notas.
- «si `[SUPUESTO]` resulta falso» (P2): dicho en §3.

## 6 · LATITUD
DECIDES TÚ: el orden; el formato de la hoja de P2 (TSV embebido en la FP o archivo propio citado); regenerar vistas por comando; ≤ 10 líneas adyacentes declaradas.
PREGUNTAS A MESA (con opciones y recomendación, y sigues): si alguno de los 12 RESULT tiene `verify = NO-REPRODUCE`, ¿entra a la hoja con recomendación VETAR (recomendado) o se excluye? — sigue con los demás.
NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada
a) no aplica (cero microdato) · b) borrar o reescribir texto de una NC/FP (solo `estado`, `sucesor`, enmiendas fechadas) · **c) adoptar cualquiera de los 12 RESULT, o marcar `cuenta_gen2 = SI` fuera de las 4 firmadas** · d) no aplica · e) caja · f) OBJETIVO inalcanzable → PARO como entregable.

## 8 · COMPUERTAS
Ninguna que proteja abrir dato, congelar spec, adoptar o borrar. Orden sugerido: lanzar **después de fusionar #1004** (cierra 18 NC y asienta T5/T6) y #1001 (las 10 firmas): así este acto cita en vez de duplicar.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `data/corrida0/decisiones.tsv` · `forense/firmas-pendientes.tsv` (una FP nueva; ninguna existente cambia salvo por cita) · `forense/no-corrido.tsv` (estado/sucesor/enmiendas de las filas nombradas) · derivados de `corrida0` por comando (`cuenta_gen2` proyectado) · `forense/notas/<fecha>-BANDEJA-TITULAR.md` (nuevo) · nota de cierre · `forense/hallazgos.md` (una línea) · `canon/L0/<raíz>.md` · cascada.
Ajeno que no se toca: `milpa/`, `tramite.yaml`, el catálogo, el informe (v1.3 es de dirección), los CALC, `usos.tsv`/`relevo-usos` (se leen).
Archivos que OTRO ACTO EN VUELO esté tocando ahora: los nueve PR en cola (#1002–#1010) tocan `decisiones.tsv`, `firmas-pendientes.tsv`, `no-corrido.tsv`, `replay-evidencia.tsv` — **lanzar después de la cola de merge**; si arranca antes, ids con raíz y sync por `git merge-file --union` en los archivos de append (los tres fuera de `.gitattributes` union: `replay-evidencia.tsv`, `censo-tests.tsv`, `decisiones.tsv`).
«Si te encuentras escribiendo fuera de esta lista, PARA.»
PERÍMETRO DE CIERRE — permanente (D-21).

## 10 · LO QUE NO HACE · SUCESORES · AUDITORÍA · CIERRE
No hace: no adopta, no mide, no acredita identidades, no edita el informe, no configura GitHub, no escribe correos (P4 los redacta para que mesa los mande).
Sucesores: el PR de adopción en bloque (mesa firma la hoja de P2 → un trámite trae el bloque); informe v1.3 (dirección); adquisición dirigida para F6 (NUBE-MEDICIÓN); el acto de tubería de T6.
Auditoría de rigor extremo: no aplica (afirma sobre el tablero).
Cierre: `## NO-CORRIDO / RESERVAS` y `## CONSUMIDO` los añade /acto al final del archivo archivado; adendas de mesa como archivo propio `<este-encargo>-ADENDA-N.md`.

## NO-CORRIDO / RESERVAS

- **qué:** P1(b) «Corpus, no motor: `cuenta_gen2 = NO` …» · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: choca con la firma 3A del 21/sep (los cuatro CALC ya cuentan SI) · **impacto:** NC-0316/0320/0321/0326 siguen ABIERTAS; `cuenta_gen2` sin cambio · **sucesor:** FP-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-02 · NC-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-01
- **qué:** criterio de «hecho» `grep -c PENDIENTE-DE-MESA data/corrida0/corridas.tsv` menor en exactamente 4 · **por qué:** DIFERIDO-A: canal de publicación T6 (FP-260922-GEN2-PENDIENTES-CAJA-1-c09b-02, opción a) · **impacto:** `corridas.tsv` no refleja las 4 hasta que corra el canal; `status` sí · **sucesor:** conversación TUBERÍA · NC-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-02
- **qué:** P3 · 8e53-04 (los huecos de la firma, en blanco) · **por qué:** DECISIÓN-DE-MESA-PENDIENTE: mesa no rellenó los tres valores · **impacto:** la NC sigue ABIERTA con la pregunta escrita · **sucesor:** mesa (bandeja del titular, entrada 11) · NC-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-04 (existente)

## CONSUMIDO

Ejecutado por el ACTO GEN2-TRAMITE-PENDIENTES-1 en el PR #1011 (rama `claude/festive-hypatia-cerq3p`), ADR-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-01. Adendas: ninguna.
