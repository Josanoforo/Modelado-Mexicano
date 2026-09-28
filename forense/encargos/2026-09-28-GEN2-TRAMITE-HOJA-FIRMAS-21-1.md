# ENCARGO · ACTO GEN2-TRAMITE-HOJA-FIRMAS-21-1 · Una sola hoja para mesa que junte todo lo que hoy espera firma —56 FP abiertas, las 30 letras de NC-DECISIONES-1, las hojas de RECIBO-ASTRA6-2/-3, del mapa de instrumentos alternos, de OBTENCION-EXTERNA-1 (solicitudes con identidad), de CORPUS-LICENCIAS-1 (restricciones) y de los tres actos de continuidad de Astra si ya cerraron—, deduplicada por objeto, con situación · opciones · recomendación · texto de firma por renglón, y con las dos decisiones nuevas del mapa (gasto de HOLDOUT; reserva de cinco olas) al frente. Es la hoja que mesa contesta; el asiento lo hace TRAMITE-FIRMAS-21 después

> ENTORNO: **NUBE** — lee TSV de gobierno, hojas y notas; escribe una hoja y una tabla. Cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `643a8198` (re-deriva al abrir) · una sesión, rama propia · MODELO: **Opus** (deduplicar por objeto y redactar opciones es juicio) · MODO: **AUTÓNOMO-AMPLIO** (cláusula v1.0) · ids con raíz de acto (D-24) · D-21 aplica.
CONTADOR: **cero mediciones; no adopta; no firma; no asienta**. No cambia el estado de ninguna FP ni NC: produce la hoja.

## 1 · OBJETIVO
Mesa pidió (27/sep) opciones por decisión, no solo recomendación, y que nada que cierre «por falta de dato» se firme sin obtención previa. Hoy la firma está repartida en ocho fuentes; este acto la junta.
(P1) **Inventario por objeto.** Universo: toda FP ABIERTA en `forense/firmas-pendientes.tsv` (56 al corte) + las 30 letras de `forense/analisis/nc-decisiones/hoja-2026-09-27.md` + las hojas: `recibo-astra6-2/`, `recibo-astra6-3/`, `mapa-instrumentos-alternos/hoja-para-mesa-…md`, `obtencion-externa-1/solicitudes/` y `registros-con-identidad.md`, `corpus-licencias-1/` (NC de licencias restrictivas), y `astra-continuidad-c1/c2/c3` si están en main. Cada renglón se ancla a **un objeto** (fila del catálogo, ola, contrato, regla, programa, portal): dos FP sobre el mismo objeto se funden en un renglón con `YA-CUBIERTA-POR` o `MISMA-DECISIÓN` (A.12: una firma, una fila). Lo ya firmado (beee-01/02, las 7 de Codex de la ADENDA-1 de ASTRA6-2, FIRMAS-20) se lista como cubierto, no se vuelve a pedir.
(P2) **Las dos decisiones nuevas, al frente y con opciones completas.** (a) **HOLDOUT**: M09–M23 tienen `rol_calibracion = HOLDOUT` en `milpa/catalogo-momentos-v0_1.tsv`; calcular cualquiera lo gasta. Opciones que la hoja debe presentar con su costo: gastar todos los HOLDOUT ahora como pisos descriptivos RETROSPECTIVOS (se gana cobertura, se pierde la prueba); gastar solo los que ninguna familia 2027 vaya a usar como R (lista derivada del expediente C2); no gastar ninguno y medir con instrumentos que no sean el momento (lo que el mapa llama «combinable»); o convertir cada uno en familia 2027 con emisión sellada antes de la ola. (b) **Reserva de cinco olas** (ENCRIGE 2020, ENVE 2024, CSES M5, ENDUTIH 2025, ENIF 2024 m7): estado real en el manifiesto por id (campo `reserva`), qué CALC las necesita, y opciones por ola: RESERVADA (solo la abre código congelado de una prueba pre-registrada) · ABIERTA-COMO-VISTA (mesa por escrito; sirve para describir y calibrar, nunca como R) · ABIERTA-PARCIAL (columnas nombradas, como ENIGH 2024). Sin recomendación de dirección aquí: el acto presenta; dirección la añade al recibir la hoja.
(P3) **Renglón por decisión, en RH.** Formato fijo: `id(s)` · objeto · situación (2 líneas) · qué se te pide · opciones (todas, con lo que cuesta cada una) · recomendación del acto que la propuso (rotulada: «recomendación del recibo -3», «del mapa», «de NC-DECISIONES-1») · lo que exige antes (OBTENCIÓN-PREVIA hecha o pendiente: cita el dictamen) · texto de firma listo. Agrupar por tipo de decisión: apertura de dato · adopción/veto · contrato/procedimiento · acciones de mesa con identidad (solicitudes de EXTERNA-1, registros, disco, `.ots`) · forma. Las que dependen de un acto en vuelo (continuidad C1/C2/C3) se listan con «espera <acto>» y no se piden hoy.
(P4) **Tabla máquina.** `forense/analisis/hoja-firmas-21/decisiones-21.tsv` (renglon · ids fundidos · objeto · tipo · fuente · requiere_obtencion_previa · obtencion_hecha(cita) · estado) y un conteo por tipo en la nota. Es lo que TRAMITE-FIRMAS-21 recorre al asentar.

«Hecho», por comando sobre el commit final con `origin/main` fusionado: toda FP ABIERTA aparece en `decisiones-21.tsv` (ids sin renglón: 0) · ningún objeto aparece en dos renglones (duplicados por objeto: 0) · cada renglón tiene `opciones` con ≥ 2 entradas y `texto_de_firma` no vacío · las decisiones (a) y (b) de P2 están, con estado de reserva por id verificado en el manifiesto · la hoja existe · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
Mesa 27/sep, verbatim: «Además de que ni opciones me diste para cada una, solo la recomendación» y «todo lo que requiera búsqueda de fuentes, datos etc, lo hacemos para obtenerlos antes de decidir nada»; mesa 26/sep: «no más microencargos … una hoja de firmas al cierre, no una FP por instrumento»; §0 («lo que dirección lleva a mesa va resuelto: estado re-verificado, recomendación con su razón y texto de firma listo»); A.12; A.17 (todo pendiente se re-verifica de estado antes de llevarse a mesa: una FP que ya cerró un acto no se lista). Este acto no firma nada.

## 3 · LO QUE DIRECCIÓN SABE
- [EJECUTADO] `643a8198` · FP ABIERTA: 56 (22 de actos ASTRA) · NC ABIERTA: 490. Consumidos desde el 27/sep: NC-DECISIONES-1 (#1213, 30 letras, FP `f2e5-01..30`), RECIBO-ASTRA6-2 (hoja; 7 FP firmadas por ADENDA-1), RECIBO-ASTRA6-3 (#1248: 13 NC, 5 FP), MAPA-INSTRUMENTOS-ALTERNOS-1 (64 pares; hoja con letras A1, A2, D1, I1; §«Antes de firmar» con HOLDOUT y cinco olas), OBTENCION-EXTERNA-1 (#1259: 179 fuentes, 146 OBTENIDO, 11 NO-OBTENIDO-POR-ESTE-AGENTE, 6 SOLICITUD-PREPARADA; siete solicitudes redactadas en `solicitudes/a..g`), CORPUS-LICENCIAS-1, PENDIENTES-2, CIERRE-SEMANAL-2, RESUMEN-SUITE-1. En vuelo: ASTRA-CONTINUIDAD-C1/C2/C3 (tres ramas `claude/new-session-*`).
- [LEÍDO] Hoja del mapa §«Antes de firmar»: HOLDOUT y cinco olas «sin campo `estado_reserva`; por la letra de E.6 podrían estarlo; mientras mesa no decida, el mapa las trata como no abiertas». [EJECUTADO] manifiesto: 175 entradas con campo de reserva (cc1 138, ENSANUT 24, oe1 6, ENCODAT 3, ENOE 2, ENCO 2): ninguna de las cinco olas trae el campo: la duda es real, no un olvido de lectura.
- [LEÍDO] Hoja v2 de dirección (`HOJA-FIRMAS-21-v2-opciones-2026-09-27.md`, adjunta): las 30 letras con opciones verbatim y línea de dirección; A1/A2/D1/I1 marcadas «no se deciden hoy» → ahora tienen dictamen (OBTENCION-PREVIA-1 + mapa + EXTERNA): el renglón lo dice.
- [REPORTADO] La hoja de RECIBO-ASTRA6-3 declara «5 FP nuevas y decisiones sin fila»: las sin fila se listan como renglón con `ids fundidos = (sin FP)` y la nota lo señala para que TRAMITE-FIRMAS-21 las acuñe.

ADJUNTO: `HOJA-FIRMAS-21-v2-opciones-2026-09-27.md` (dirección); se archiva verbatim con el sha calculado al recibir.

## 4 · YA HECHO / YA DECIDIDO — por objeto
`git ls-tree -r --name-only origin/main forense/encargos | grep -c 'HOJA-FIRMAS-21\|TRAMITE-FIRMAS-21'` → 0. Homónimos: TRAMITE-FIRMAS-11…-20 (asentaron; su formato de hoja es el modelo), NC-DECISIONES-1 (produjo hoja, no asentó). En vuelo: los tres de continuidad (sus hojas entran si están en main al cerrar; si no, se citan como «espera»), INSTRUCCIONES-V217-1 (misma fecha; disjunto).

## 5 · PIEZAS
P1 → P2 → P3 → P4. Rama prevista: una FP cuyo objeto ya cerró un acto (A.17) se marca `SUPERADA (cita)` en la tabla y no va a la hoja; una FP con texto ilegible se lee en su nota de origen, no se interpreta.

## 6 · LATITUD
Agrupación, orden, redacción: tuyos. Puedes proponer opciones que ninguna fuente listó, rotuladas PROPUESTO-POR-EJECUTOR. PREGUNTA A MESA: ninguna (la hoja es la pregunta). NO DECIDES: nada de §7.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir dato · b) editar una FP, NC, fila FIRMADA o sello · c) firmar, asentar o adoptar; presentar una recomendación como firma · d) no aplica · e) CAJA · f) objetivo inalcanzable.

## 8 · COMPUERTAS
«Un objeto, un renglón» protege **adoptar** (A.12) · «Toda opción con su costo; ninguna decisión sin obtención previa citada» protege **borrar** (deuda cerrada por suposición).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/analisis/hoja-firmas-21/` (hoja, tabla, adjunto archivado), nota, L0, cascada. Ajeno: `firmas-pendientes.tsv`, `no-corrido.tsv`, `decisiones.tsv` (nada se edita), `canon/`, `milpa/`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · LO QUE NO HACE · SUCESORES · CIERRE
No firma, no asienta, no adopta, no cierra NC. Sucesores: dirección añade su recomendación a (a) y (b) y entrega la hoja a mesa; `GEN2-TRAMITE-FIRMAS-21` asienta lo firmado con las firmas verbatim; `GEN2-CALC-ALTERNOS-LOTE-1` (caja) se escribe con lo que mesa decida sobre HOLDOUT y reservas. Sin módulo de auditoría (no afirma sobre México). El cuerpo no lleva campos para rellenar; `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio) y `## CONSUMIDO` las añade /acto. Adendas: `2026-09-28-GEN2-TRAMITE-HOJA-FIRMAS-21-1-ADENDA-N.md`, selladas al recibirse.
