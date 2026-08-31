ENCARGO · ACTO MAESTRA32-E15 · MARCO-M-CORRIGE-Y-CENSA-TRANSFERENCIA

SHA de redacción: 899113c (main, merge PR #404 / ADR-232) · Redactado: 31/ago/2026, dirección maestra-32 · Instrucciones vigentes: v2.11 · Estado: LISTO PARA LANZAR — sin compuerta, sin ranuras. No congela nada (la elegibilidad de las celdas nuevas depende de la decisión D-D de mesa, pendiente): produce la tabla corregida y el censo; el congelado v1_1 y su sorteo (A″/B″) vienen después, con D-D dentro.

ENTORNO ASIGNADO: NUBE (cloud_default). NO se lanza en UBUNTU — repo-only (inventarios versionados, milpa/*.yaml, notas). E4 ya cerró; la nube está libre.

CARRILES: este acto corre solo; nada en paralelo. Cascada estándar.

FIRMAS — ninguna nueva; dos correcciones de dirección/ejecutor, con la fuente en el repo

C1 · TRA-M-02, variable. marco-M-congelado-v1_0.tsv trae variable=AP5_1_1 para la celda ENCUCI 2020. AP5_1_1 es un ítem de θ (confianza, 0-10) del par G1.radio_confianza, no el desenlace. El desenlace sellado de ese par, verbatim de milpa/procedencia.yaml (coeficientes_generador_medidos.G1_radio_confianza.nota): "el desenlace es compuesto sobre AP5_17/AP5_18 (todos los contactos de la persona, no la autoridad específica)"; y en forense/notas/2026-08-04-w-coeficientes-generador-paso1.md §1.1: mordida = AP5_17='1' o AP5_18='1', universo con contacto AP5_16_1..10. El parser de E13 tomó el primer token de fuente. Se corrige en v1_1 con estas citas; v1_0 queda intacto (A.10).

C2 · TRA-M-02, ponderador. E13 buscó el ponderador en procedencia.yaml (1,944 líneas) y tramite.yaml (46) y lo dejó NO_ENCONTRADO_1944_LINEAS_REVISADAS — correcto sobre su universo. Existe fuera de él: forense/notas/2026-08-30-compuesta-spec.md:52, verbatim: "Ponderador: FAC_SEL. Estrato: EST_DIS. UPM: UPM_DIS. Fuente: forense/notas/2026-08-04-w-coeficientes-generador-paso1.md §1.1/§3.1." Se corrige con esa cita. (Universo de E13 declarado → cierre VENCIDO EN ALCANCE, no refutado.)

Lo que NO se corrige aquí: grado_dependencia. E13 declaró (cierre, hallazgo 1) que la regla sellada de forense/notas/2026-08-20-act-pil-2-marco.md clasificaría ambas celdas como P0 (parametrizan directamente a G1) y que puso P1 por instrucción de dirección, como desviación declarada. Ese punto es la decisión D-D de mesa (ver conversación de dirección del 31/ago); este acto registra ambos grados por celda (grado_sellado, grado_transferencia) y no elige.

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════

Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no haya ninguno, y si clonas, dilo. Reporta: ruta absoluta · git log -1 --format="%h %s" · git status ⚠️ No arranques desde el home. Si el cliente avisa "launched in your home directory", cámbiate al clon antes de nada.

2 · SHA. Confirma contra qué base trabajas y compáralo con el que el encargo declara. Si main se movió: NO es PARO — refresca, re-deriva lo que dependa del perímetro, y reporta la diferencia antes de editar.

3 · data/raw. AUSENTE NO ES PARO. Es raíz integrada, gitignorada, resuelta por código; un clon fresco siempre nace sin ella. Se crea o se enlaza. Reporta: existe / la enlacé a <ruta> / la creé. ⚠️ Si este acto DESCARGA algo: verifica al cerrar que los payloads quedaron en el CORPUS COMPARTIDO y no solo en tu worktree. Es el defecto de PR #77 y no lo atrapa ningún test.

4 · ENTORNO. "Ubuntu" no distingue nada; la política de red sí. CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE → esperado: sin_variable curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/ Reporta los dos valores crudos. NUNCA curl -I. Si este acto no toca microdato ni red, dilo y salta este punto. ⚠️ [NUEVO v2.11] Un negativo producido por un comando que no examinó archivos no es un negativo (A.13). Todo veredicto negativo —incluida la sonda de este punto— declara cuántos archivos examinó el comando que lo produjo.

5 · ESPEJO. Prohibido derivar cifras del espejo del proyecto: está versiones atrás del repo y contiene archivos que el repo nunca tuvo. Toda cifra sale del clon de (1), con el comando a la vista.

════════════════════════════════════════════════════════════════════

A.2, tercera parte: ls data/raw/ 2>/dev/null | head -1 — se espera ausente. TSV con cabecera #; YAML íntegro con yaml.safe_load; búsquedas en Python UTF-8 (A.13). T03: rutas completas entre backticks.

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección (maestra-32, 31/ago/2026, contra 899113c) ═══

1 · ESTRUCTURA. Familia forense/prereg-duelo-v2/ (marco-M v1_0 congelado + sorteado, CONGELADO-M-v1_0.sha256), inventarios (v1_2, ext-v1_0, fd-v1_1, fd-ext-v1_0), milpa/tramite.yaml (5 reglas, todas dominio: tramite, verificado por E13), milpa/procedencia.yaml (sección A: 6 pares medidos con fuente que nombra encuesta, ola, variable de desenlace y universo).

2 · CONTENIDO. (i) Un censo de transferencia (misma estadística del motor en otra ola/instrumento): NO-ENCONTRADO — candidatos-marco-M-v1_0.tsv tiene 2 filas, ambas de la ola que parametriza la regla; ninguna columna de ola de calibración ni de transferencia. (ii) Cómo emite el motor, verificado: milpa/src/emisor.py:emitir_binaria(regla, conducta) devuelve PrediccionM(valor_punto = s.p) — el punto M de una celda binaria es la probabilidad p de la conducta en el ENTONCES de la regla, sea ASIGNADO o medida. Por eso importa de qué encuesta/ola salió p: contra esa misma ola, M devuelve su propia calibración (circular, P0); contra otra ola u otro instrumento, M predice fuera de muestra (transferencia). (iii) Olas múltiples en el corpus, verificado en el inventario: ENDIREH 2006/2011/2016/2021 (tabla ext), ENVIPE 2023 y 2025, ENIF 2012/2018/2021/2024, ENCUCI 2020, ENCIG 2023, ENNViH 2005 + MxFLS olas 2-3 (CAL-G3), ENFIH 2019, ENASEM 2018/2024. (iv) Esquema R existente, reutilizable sin cambios: forense/prereg-duelo-v2/corridas-R/*.json (R, EE_R, cv, cv_pct, ic95_lo/hi, encuesta, estado, estrato, id_celda, n_codigo_no_valido, codificacion).

3 · COBERTURA RETROACTIVA. El marco original clasificó P0/P1/P2 antes de que existiera un solo coeficiente medido y sin la noción de ola de calibración; E13 copió la desviación que dirección le pidió. Este acto no re-sella nada: añade las dos columnas que faltan para que mesa decida con el dato a la vista.

═══════════════════════════════════════════════════════════════════

0-bis · A.3

Primer commit: este encargo verbatim en forense/encargos/2026-08-31-MAESTRA32-E15-MARCO-M-CORRIGE-Y-CENSA.md. Al cerrar, ## CONSUMIDO con el PR.

Objeto

Producir forense/prereg-duelo-v2/candidatos-marco-M-v1_1.tsv: las 2 filas de v1_0 corregidas (C1, C2) + una fila por cada celda de transferencia encontrada, con ola_calibracion de la regla, grado_sellado, grado_transferencia, transferencia (SI/NO), en_corpus, y la razón. Sin congelar. Sin sortear. Sin emitir.

COMMIT-1 — receta congelada ANTES de recorrer inventarios

forense/notas/2026-08-31-marco-M-v1_1-spec.md: (a) procedencia de p por regla: para tramite.mordida.discrecional/paga_mordida, localizar en tramite.yaml/procedencia.yaml (asignados_probabilidad, secciones medidas) si p es ASIGNADO o MEDIDO y de qué encuesta/ola — cita archivo:línea; eso fija ola_calibracion; (b) lista cerrada de estadísticas del motor a buscar en otras olas: la de la regla (mordida: ENCIG P8_3_1; ENCUCI AP5_17|AP5_18) y los desenlaces de los 6 pares medidos tal como los nombra la sección A (fuente): ENVIPE 2025 BP1_23 (miedo/desconfianza para no denunciar), ENNViH cr27 (tiene ahorros), ENIF 2024 desenlace de G3.familismo_apoyo (leer fuente), y los que la sección A nombre — se copian, no se interpretan; (c) criterio de "misma estadística en otra ola": mismo variable_id en un instrumento de la misma familia y otra ola (inventarios v1_2 ∪ ext ∪ fd-v1_1 ∪ fd-ext), o, si el id cambió entre olas, coincidencia de texto_reactivo por lista de términos declarada aquí; instrumento distinto de la misma familia temática (p.ej. mordida ENCIG↔ENCUCI) cuenta como transferencia de instrumento y se marca así; (d) grado_sellado = el que dicta forense/notas/2026-08-20-act-pil-2-marco.md (cítalo; para celdas que parametrizan directamente al motor → P0); grado_transferencia = P1 si ola/instrumento ≠ ola_calibracion, P0 si coincide — regla escrita aquí, no adjudicada: mesa decide (D-D); (e) B-bis, antes de contar: ≥8 celdas de transferencia en_corpus=SI → el marco-M puede llegar a tamaño de sorteo real bajo D-D; 1-7 → corto, se dice cuáles; 0 → el corpus no tiene otras olas de las estadísticas del motor y la vía (ii) no puede crecer sin (i′). Cierra con: "el primer resultado que produzca este procedimiento es el que se reporta."

COMMIT-2 — corrida única

candidatos-marco-M-v1_1.tsv (columnas de v1_0 + ola_calibracion, grado_sellado, grado_transferencia, transferencia, razon), nota de cierre forense/notas/2026-08-31-marco-M-v1_1-cierre.md con A.13 (filas examinadas por inventario, estadísticas buscadas, celdas por familia y ola), y las dos correcciones con sus citas. Intocables (git diff --stat vacío): candidatos-marco-M-v1_0.tsv, marco-M-congelado-v1_0.tsv, marco-M-sorteado-v1_0.tsv, CONGELADO-M-v1_0.sha256, todo el duelo original, milpa/**.

PERÍMETRO Y CONCURRENCIA

Archivos: forense/encargos/2026-08-31-MAESTRA32-E15-MARCO-M-CORRIGE-Y-CENSA.md · forense/notas/2026-08-31-marco-M-v1_1-spec.md · forense/notas/2026-08-31-marco-M-v1_1-cierre.md · forense/prereg-duelo-v2/candidatos-marco-M-v1_1.tsv · forense/firmas-pendientes.tsv (fila de recibo) · cascada. Nada en paralelo. "Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."

FP pre-asignadas

FP-194–FP-195 (máximo hoy FP-193; FP-192 quedó reservada sin usar por E13 — no la tomes; re-deriva).

ADR y cascada

Candidato re-derivado (deriva, no heredes). El ADR trae C1/C2 con sus citas, la regla (d) declarada como no adjudicada, ola_calibracion de la regla, y el conteo de transferencia con su B-bis. registro-rotulos: MAESTRA32-E15. T25.

CONTADOR

Celdas de transferencia encontradas: N (incluido cero) · defectos de v1_0 corregidos con cita: 2.

Lo que este acto NO hace

No congela v1_1 (A″ tras D-D), no sortea, no emite M, no calcula R, no decide grado_dependencia, no edita v1_0.

Sucesores declarados, no lanzados

MARCO-M-CONGELA-v1_1 (A″) + MARCO-M-SORTEA-v1_1 (B″) con D-D dentro · EMITE-M (nube, emitir_binaria sobre las celdas sorteadas, p con su procedencia a la vista) · R-MARCO-M (caja, esquema corridas-R reutilizado) · L-MARCO-M (fuera del proyecto, sesión limpia, pipeline-L-adv1-m2.py D-iii).
