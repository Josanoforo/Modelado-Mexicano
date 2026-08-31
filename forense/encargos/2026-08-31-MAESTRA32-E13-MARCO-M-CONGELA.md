# ENCARGO · ACTO MAESTRA32-E13 · MARCO-M-CONGELA (ACTO A′) + PROPAGA-3

Redactado: 31/ago/2026, dirección maestra-32 · Estado: LISTO PARA LANZAR. No corre el PRNG (eso es ACTO B′ = MAESTRA32-E14, con semilla derivada del SHA del merge de este acto — protocolo ADR-178/FP-150).

FIRMAS DE MESA (verbatim, ya aprobadas, no reabrir):
F1 · Recibos → FIRMADA: FP-180 (E6), FP-182 (CAL-G3 en el ejecutable, con el enlace de escala declarado por dirección), FP-183 (cobertura-15, 0 de 15), FP-185 (los 2 compuestos), FP-186 (extractor rama a). FP-189 (extractor rama b, ADR-229) nació después: queda ABIERTA, no se infiere.
F2 · D1 revisitada = (ii) con (i′) de fondo: (ii) un marco-M construido con los estadísticos de encuesta que el motor sí emite hoy — todo (regla, conducta) con desenlace sellado en milpa/procedencia.yaml/milpa/tramite.yaml (mismo criterio EMITE de enlace-M-v1_0.md), incluidos los desenlaces de los 6 pares con coeficiente ejecutable de base medida — sorteado con el mismo reglamento del piloto (sorteo-act-pil-3-v2-PROPUESTA.md, ADR-178/FP-150), conservando el marco congelado actual (marco-congelado-piloto-v1_0.tsv) intacto como benchmark L-vs-R; (i′) programa de fondo: reglas nuevas del motor (candidatos de OLA 5) para las 5 celdas sin regla (CIV-08, DIN-11, SFT-04, SFT-06, TIC-06) y cita de θ en canon para las 3 sin θ (DIN-07, TIC-01, EMP-05) — se escribe primero, se mide después. No toca el congelamiento del motor (ADR-68(a)): el marco-M usa reglas existentes.

Familia forense/prereg-duelo-v2/: tablas gobernantes marco-congelado-piloto-v1_0.tsv (60 filas; columnas: id encuesta ola universo variable estimador ponderador escala grado_dependencia publicada cv_arbitro n_no_ponderado frase_discriminacion post_corte_u_ola_retenida dominio dificultad estrato), sorteo-act-pil-3-v2-PROPUESTA.md (reglamento), sorteo_v2.py + tests_sorteo_v2.py (mecanismo), enlace-M-v1_0.md (criterio EMITE), milpa/procedencia.yaml + milpa/tramite.yaml (reglas y desenlaces sellados), cobertura-15-v1_0.tsv (E11).

VERIFICACIÓN previa de dirección: (i) no existe ya un marco-M/candidatos/congelado hermano en forense/prereg-duelo-v2/ — confírmalo tú mismo listando el directorio y contando entradas. (ii) Existe: enlace-M-v1_0.md:33-35 (1 EMITE de 60 = CIV-01 ← regla=tramite.mordida.discrecional, conducta=paga_mordida, procedencia.yaml:937); cobertura-15-v1_0.tsv; coeficientes_generador_sellados (6 entradas con valor_ejecutable, yaml.safe_load). (iii) Reglamento: elegibilidad = grado_dependencia ∈ {P1,P2} ∧ publicada ∈ {SI,NO}; estrato = dominio|grado_dependencia|dificultad; cuota_max = floor(0.20·n_sorteo) de publicada=SI; piso 1 por estrato no vacío (Hamilton); semilla = semilla_desde_sha_merge(SHA_A, scope_id) (ver sorteo_v2.py); cargar_marco(ruta) trae assert n=50 contra el congelado original — para el marco-M NO se edita sorteo_v2.py: B′ (acto futuro, no este) usará un cargador propio.

Objeto — construir un marco hermano sobre el dominio del motor de HOY (el original quedó congelado el 20/ago sobre un universo previo; no se reabre, queda intacto como benchmark).

COMMIT-1 — receta congelada ANTES de recorrer las tablas del motor. Escribe forense/notas/2026-08-31-marco-M-spec.md con:
(a) Criterio "emitible" citado (no inventado): el mismo de enlace-M-v1_0.md (§criterio EMITE) y del docstring de `emisor.construir_crosswalk` si existe en el repo (búscalo; si no existe tal función, dilo con el comando que usaste). Recorre milpa/tramite.yaml y milpa/procedencia.yaml completos con yaml.safe_load (secciones: reglas, desenlaces, condicionales_*, coeficientes_generador_medidos, coeficientes_generador_sellados) y lista los campos que califican, archivo:clave.
(b) Regla de mapeo fila de candidato → columnas del marco (documenta la regla exacta que vas a aplicar): encuesta/ola/variable/universo/ponderador desde el desenlace sellado; estimador = "proporción ponderada" salvo que el desenlace declare otro; escala = binaria/continua según la variable; grado_dependencia (P1/P2, nunca P0 — cita archivo:línea de la definición ADV1-M1 si la encuentras, si no, documenta que no la encontraste con el conteo de archivos revisados y usa un criterio razonable declarado explícitamente); dificultad; dominio ∈ {tramite, civico, dinero, salud, familia, tiempo, cooperacion, trabajo, informacion, comunicacion} con mapa regla→dominio explícito; estrato = dominio|grado_dependencia|dificultad; publicada = NO por defecto salvo que coincida con una fila del marco original (en cuyo caso hereda su valor); cv_arbitro/n_no_ponderado vacíos; frase_discriminacion = una línea con regla+conducta sin valor numérico.
(c) Columnas extra de (A): regla, conducta, clase_procedencia, base_medida (SI si el generador de la regla tiene valor_ejecutable medido en coeficientes_generador_sellados/medidos), en_corpus (SI/NO — intenta verificar contra inventarios si existen en el repo, documenta el método), en_marco_60 (id del marco original si coincide encuesta+variable, vacío si no), elegible (SI/NO con razón).
(d) Controles: CIV-01 (ENCIG 2023 P8_3_1) DEBE aparecer en (A) con en_marco_60=CIV-01 — si no aparece, es PARO documentado (no fuerces el resultado, repórtalo). Ningún candidato sin en_corpus=SI entra a (B).
(e) Pre-registro del sorteo de B′ (NO lo ejecutes, solo documenta la receta): scope_id="MARCO-M-v1"; SHA_A = SHA del merge de este PR (déjalo como placeholder "<SHA_DEL_MERGE_DE_ESTE_PR>" ya que aún no existe); semilla = semilla_desde_sha_merge(SHA_A,"MARCO-M-v1"); regla de tamaño fijada AHORA sin ver N: N≥30→n_sorteo=15; 15≤N<30→n_sorteo=ceil(N/2); N<15→sin sorteo (todas las elegibles); cuota_max=floor(0.20·n_sorteo); estratos y piso 1 Hamilton como el reglamento.
(f) B-bis interpretación (documenta, no adjudiques): N≥30 vía(ii) reproduce el piloto a escala; 15-29 viable más corto; <15 viable sin sorteo; 0 → hallazgo de que el criterio EMITE no alcanza ni los 6 pares medidos.
Cierra el archivo con la frase: "el primer resultado que produzca este procedimiento es el que se reporta."

COMMIT-2 — corrida única, SIGUIENDO EXACTAMENTE la receta de COMMIT-1 (no la reescribas sobre la marcha):
- Recorre milpa/tramite.yaml y milpa/procedencia.yaml con yaml.safe_load, aplica el criterio EMITE, produce:
  (A) forense/prereg-duelo-v2/candidatos-marco-M-v1_0.tsv — TODOS los candidatos con sus columnas (incluidas las extra de (c)), TSV con cabecera, texto plano (NUNCA módulo csv de Python).
  (B) forense/prereg-duelo-v2/marco-M-congelado-v1_0.tsv — subconjunto elegible=SI, mismas columnas que marco-congelado-piloto-v1_0.tsv.
  (C) forense/prereg-duelo-v2/CONGELADO-M-v1_0.sha256 — sha256 del archivo (B) + N_elegibles en el mismo archivo (mira el formato de CONGELADO-v1_0.sha256 existente en el mismo directorio y sigue el mismo patrón).
- Escribe forense/notas/2026-08-31-marco-M-cierre.md: reglas recorridas (conteo), candidatos totales, elegibles, desglose por dominio y por base_medida, resultado del control CIV-01 (presente/ausente, con cita de fila).
- INTOCABLES — verifica con `git diff --stat` al final que estos archivos NO cambiaron: marco-congelado-piloto-v1_0.tsv, CONGELADO-v1_0.sha256, sorteo_v2.py, tests_sorteo_v2.py, enlace-M-v1_0.md, cualquier archivo corridas-*, scoring-adv1-m3.py, todo milpa/**.
- Corre y confirma VERDE: `python3 forense/prereg-duelo-v2/tests_sorteo_v2.py` y `tests/check.py --baseline` (busca la ruta exacta del segundo, probablemente `python3 tests/check.py --baseline` desde la raíz del repo).

PROPAGACIÓN (mismo commit que COMMIT-2, o un tercer commit si el patrón del repo lo pide — revisa cómo cerraron actos anteriores mirando `git log --oneline -30` y algún PR reciente similar, p.ej. busca en forense/encargos/ y en el registro de FP/ADR cómo se hace, y sigue el mismo patrón):
- En forense/firmas-pendientes.tsv: marca FP-180, FP-182, FP-183, FP-185, FP-186 como FIRMADA (verbatim de F1 arriba; en FP-183 anota también la respuesta F2). FP-189 permanece ABIERTA (no la toques a FIRMADA).
- Agrega una fila-grito nueva PROGRAMA-(i′) con el texto: "Mesa firmó (i′) como programa de fondo (31/ago): reglas nuevas OLA 5 para CIV-08 inseguridad percibida en la calle, DIN-11 conocimiento de cuentas sin comisión, SFT-04 ayuda para bañarse (ABVD), SFT-06 acuerdo entre hermanos para el cuidado, TIC-06 trabajo infantil todos los meses; y cita de θ en canon para DIN-07 presupuesto en el hogar, TIC-01 pertenencia a sindicato, EMP-05 situación conyugal joven. Dueño: dirección redacta REGLAS-OLA5-v0 (nube) tras E4; mesa sella. ABIERTA hasta lanzar."
- Agrega también una fila de recibo de este acto mismo (mira el formato exacto de filas anteriores en firmas-pendientes.tsv para replicar columnas).
- Usa FP-190, FP-191, FP-192 como IDs pre-asignados para la fila-grito (i′) y el recibo de este acto (declara cuál usas para cuál).
- Actualiza la "cascada" que corresponda: revisa qué archivos forman la cascada en actos anteriores (probablemente algo como estado-programa, registro-rotulos, un ADR nuevo, gobernanza) mirando cómo cerró el acto anterior más similar (busca "MAESTRA32-E12" o "MAESTRA32-E9" en git log / forense/) y replica el mismo patrón de archivos tocados para MAESTRA32-E13, incluyendo un ADR nuevo (número correcto siguiente — verifica el máximo ADR actual, NO asumas ADR-230, cuenta tú mismo) que cite F1/F2 verbatim, el criterio EMITE citado, N_elegibles, el pre-registro (e) con scope_id, y la declaración de que el marco original queda intacto.
- Registra "MAESTRA32-E13" en el registro-rótulos si existe ese archivo/mecanismo. Actualiza T25 si aplica (búscalo, es un test que verifica rótulos/marcadores).

PERÍMETRO ESTRICTO — SOLO puedes crear/tocar:
forense/encargos/2026-08-31-MAESTRA32-E13-MARCO-M-CONGELA.md (nuevo, con el encargo verbatim que te acabo de dar, y al cerrar agrega "## CONSUMIDO" con referencia al PR)
forense/notas/2026-08-31-marco-M-spec.md (nuevo)
forense/notas/2026-08-31-marco-M-cierre.md (nuevo)
forense/prereg-duelo-v2/candidatos-marco-M-v1_0.tsv (nuevo)
forense/prereg-duelo-v2/marco-M-congelado-v1_0.tsv (nuevo)
forense/prereg-duelo-v2/CONGELADO-M-v1_0.sha256 (nuevo)
forense/firmas-pendientes.tsv (edita)
+ los archivos de "cascada" que identifiques (gobernanza/ADR nuevo, estado-programa, registro-rotulos) — pero solo si existen ya como mecanismo en el repo; si no los encuentras, documenta el conteo de búsqueda y omite ese paso en vez de inventar estructura nueva.

NO TOQUES: nada relacionado con E4/RE-EMPAREJA, ningún archivo del "duelo original", milpa/** (solo lectura), canon/modelo-decision-v4_0.md.

Si en cualquier punto detectas que el perímetro está mal calculado o una premisa del encargo no cuadra con el repo real (p.ej. CIV-01 no aparece, o el patrón de cierre de actos es distinto al que supones), PARA, documenta el hallazgo en las notas, y NO fuerces un resultado falso. Es preferible un resultado parcial honesto a uno completo inventado.

---

## NOTA DE ARRANQUE (contexto de ejecución, no verbatim de dirección)

El encargo declara SHA de redacción `9bd3932`. Al lanzar la rama, `origin/main` ya había avanzado a `b33c38c` (incluye el merge de PR #402, `ACTO MAESTRA32-E4 · RE-EMPAREJA`, ya cerrado). Esto no es `PARO`: la restricción "no lanzar en NUBE mientras E4 corra" ya no aplica porque E4 terminó y fusionó. Se usa `b33c38c` como base real de este acto. Donde el encargo pide "SHA del merge de ESTE PR" para el pre-registro (e), se deja como placeholder `<SHA_DEL_MERGE_DE_ESTE_PR>` — la propia rama de este acto aún no tiene PR al escribir COMMIT-1.

## CONSUMIDO

Cerrado por `ACTO MAESTRA32-E13 · MARCO-M-CONGELA` (rama `acto/maestra32-e13-marco-m-congela`). Ver `forense/notas/2026-08-31-marco-M-spec.md` (COMMIT-1) y `forense/notas/2026-08-31-marco-M-cierre.md` (COMMIT-2 + PROPAGA-3). PR: (ver referencia insertada por el acto al abrir el PR).
