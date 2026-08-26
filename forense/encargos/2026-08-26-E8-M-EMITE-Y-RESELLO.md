ENCARGO E8 · M-EMITE-Y-RESELLO — ejecuta FP-166 caminos (ii)+(iv): repara el crosswalk, sella el enlace de M, y enmienda F1 el contrato del scoring

Dirección (maestra-30), 26/ago/2026 · Redactado leyendo main=3bc28b1 y la rama acto/e7-r-scoring (6572afd) en esta sesión (clase 1). GATED: no arranca hasta que el PR de acto/e7-r-scoring esté FUSIONADO — tu base debe contener FP-166, marcador-piloto-v1_0.md, DERIVACION-M-v1_0.md y _scoring-intento.json; verifícalo en la compuerta cero.

ENTORNO ASIGNADO: NUBE (cloud_default, repo-only). NO lanzar en UBUNTU ni Codex. Determinista, cero API, cero microdato. Puede correr en paralelo con E10 (NUBE) — perímetros disjuntos salvo gobernanza/estado.

RANURA DE MESA — FP-166, precargada

FIRMA M-FP166: «FIRMO FP-166: caminos (ii)+(iv). (i) queda satisfecho archivando el marcador v1.0 tal como está — no se reescribe; el sucesor produce v1.1. (iii) DECLINADO con razón medida: las 9 celdas arbitrables tienen publicada=NO por diseño del sorteo y el bibliotecario FP-93 ya cerró NO-ENCONTRADO — B queda opcional en el contrato re-sellado, con las casillas que dependan de skill reportadas no evaluable cuando B no exista. AUTORIZO la enmienda F1 fechada de scoring-adv1-m3.py (fila ## F1 · enmienda con hash viejo→nuevo y razón, prereg-corrida:110) y la corrección del defecto de construir_crosswalk.»

Vacía o alterada → solo A.3 + reporte; nada se edita.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test. (Este acto no la toca — repórtalo y sigue.)

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: cloud_default (este acto es NUBE) curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — la contesta quien ESCRIBE el encargo [NUEVO v2.8] ═══ CONTESTADA por dirección, 26/ago/2026 (main 3bc28b1 + rama E7 6572afd, leídas en esta sesión; re-verifica post-merge):

1 · ESTRUCTURA. Gobernantes: milpa/src/emisor.py:486-508 (construir_crosswalk — el código con el defecto) · forense/crosswalk-pregunta-regla-v1_0.tsv (60 filas, salida a re-derivar) · forense/prereg-duelo-v2/scoring-adv1-m3.py (validar_configuracion:225-305 — el contrato a re-sellar) · prereg-corrida-v1_0.md:110 (regla de enmienda F1) · marco-congelado-piloto-v1_0.tsv (intocable). INFRAESTRUCTURA no cubre milpa//prereg-duelo — declarado.

2 · CONTENIDO. El defecto está medido, no supuesto (FP-166(a) + DERIVACION-M-v1_0.md): construir_crosswalk decide con if var and var in l sin comparar la columna encuesta; los 3 CANDIDATO-EMITE de las 15 son falsos positivos de subcadena (P7_1↔AP7_1 de ENCUCI/P7_12_7 de ENASIC · P5_3↔AP5_3_* de ENVIPE-2025/ENCUCI · P2↔la cadena documental "(P2 §2.d)"). Su propio docstring exige un enlace de escala/universo declarado antes de emitir — no sellado en ninguna parte del árbol (barrido del acto E7). El contrato del scoring exige los CUATRO corredores (_scoring-intento.json, salida verbatim) y el piloto tiene uno. Lo que este encargo produce NO existe: crosswalk…v1_1, enlace sellado, enmienda F1 → 0 hits (re-deriva el conteo tú, A.13).

3 · COBERTURA. El crosswalk (21/ago) y el scoring (26/ago) son anteriores al hallazgo (26/ago tarde) — la brecha ES el objeto del acto.

════════════════════════════════════════════════════════════════════

OBJETO

Dejar a M en condiciones de emitir y al scoring en condiciones de arrancar con los corredores que existen — sin correr nada de microdato (eso es E9, sucesor en UBUNTU) y sin tocar el marcador v1.0.

PASOS

0-bis · A.3: commitea este encargo íntegro en forense/encargos/2026-08-26-E8-M-EMITE-Y-RESELLO.md; al cerrar, ## CONSUMIDO con el PR. Rótulo del acto: ACTO MAESTRA30-E8 (D-6, mismo patrón que E4-E7). 1 · Compuerta cero: PR de E7 fusionado (pega el merge); RANURA presente; pega los tres hits de subcadena verbatim desde DERIVACION-M. 2 · Repara construir_crosswalk (milpa/src/emisor.py): el emparejamiento exige coincidencia de encuesta además de la variable, y variable por token exacto (no subcadena). Test nuevo en tests/ que fija los tres falsos positivos como casos negativos y al menos un positivo de control. Cero cambios de lógica fuera de la función. 3 · Sella el enlace SpecCelda → (regla, conducta) que el docstring exige: documento forense/prereg-duelo-v2/enlace-M-v1_0.md — pasada declarada sobre las 60 filas del marco (no solo las 15), solo donde el motor tiene regla real (cita modelo-decision/procedencia por fila); donde no la hay, NO-EMITE con razón. Escala/universo declarados por fila emitible (A-bis 3). Nada se inventa: si tras la pasada honesta M sigue en 0 emitibles sobre las 15 sorteadas, ese es el resultado y se escribe — no se fuerza un enlace. 4 · Re-deriva el crosswalk → forense/crosswalk-pregunta-regla-v1_1.tsv (v1_0 intacto, SUPERADO en cabecera con fecha y ADR), con el conteo nuevo NO-EMITE/EMITE sobre 60 y sobre las 15. 5 · Enmienda F1 del scoring (autorizada en la RANURA): edita validar_configuracion para admitir el subconjunto real — mínimo {(L,solo), (M,principal)}; (L,corpus) y (E,combinacion) opcionales, y B opcional con skill/casillas reportadas no evaluable cuando falte. Ningún otro cambio al script. Registra la enmienda como manda prereg-corrida:110: fila ## F1 · enmienda 2026-08-XX en el prereg con hash viejo (beec0e1c…), hash nuevo y razón — y actualiza la tabla del lanzamiento-L NO (ese doc es histórico del corredor L; decláralo). 6 · De pasada, dos correcciones fechadas autorizadas: (a) marcador-piloto-v1_0.md no se toca; en su lugar, la nota de este acto registra que su reserva sobre FP-163 ("no firmada") está desactualizada — el tablero la tiene FIRMADA (ADR-199); v1.1 lo dirá bien. (b) enmienda fechada a lanzamiento-L-v1_0.md §5 corrigiendo la afirmación falsa sobre el extractor (reportada por E6), texto viejo intacto. 7 · FP-166 → FIRMADA (firmada_en = RANURA verbatim; ejecutada_en = ADR). Nota forense/notas/2026-08-26-e8-m-emite-cierre.md · ADR (máximo por conteo entero; hoy 206 en main, la rama E7 trae 207 — re-deriva post-merge y candidatea; renumera si E9/E10 colisionan) + recifrado · check.py --baseline VERDE · PR.

PERÍMETRO Y CONCURRENCIA

milpa/src/emisor.py (una función) · tests/ (test nuevo + snapshots declarados) · forense/crosswalk-pregunta-regla-v1_1.tsv (nuevo) + cabecera de v1_0 · forense/prereg-duelo-v2/enlace-M-v1_0.md (nuevo) · forense/prereg-duelo-v2/scoring-adv1-m3.py (solo validar_configuracion, bajo enmienda F1) · prereg-corrida-v1_0.md (solo la fila F1·enmienda) · lanzamiento-L-v1_0.md (solo enmienda fechada §5) · tablero (FP-166) · nota · encargo · gobernanza · estado. Concurrentes: E10 (NUBE) y E9 (UBUNTU, gated a este) — colisión esperada en gobernanza/estado/tablero. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

PROHIBIDO

Correr M, R, B o scoring (eso es E9) · tocar marco-congelado, ADR-141, el marcador v1.0, corridas-L/, corridas-R/ · API o red · inventar un enlace donde el motor no tiene regla.

CONTADOR

Cero directo, declarado — habilita el marcador v1.1 (E9). Tablero 1→0 ABIERTA.

## CONSUMIDO

[PR #380](https://github.com/Josanoforo/Modelado-Mexicano/pull/380) — ver `forense/notas/2026-08-26-e8-m-emite-cierre.md` para el detalle de ejecución y `canon/gobernanza-v1_15.md` `ADR-208` para el registro de gobernanza.
