# ENCARGO · LOTE · NUBE-DECISIONES-1 — seis cierres de tablero en un acto

> **Estado: `CONSUMIDO`** — ver cierre al pie.

**Archivado bajo `A.3` al cierre: el encargo llegó inline de dirección y no tenía archivo en el árbol; se archiva aquí, verbatim, para que el acto sea auditable contra su instrucción** — mismo patrón que `forense/encargos/2026-08-19-FP57-DECLARA.md` ya usó.

---

## Texto original, verbatim

LOTE · NUBE-DECISIONES-1 — seis cierres de tablero en un acto

Redactado por dirección el 19/ago/2026 contra b4a9b3f (#292). Re-deriva al arrancar. ENTORNO ASIGNADO: NUBE (repo-only). NO Ubuntu. Modelo: Opus. 🚫 --freeze.

### Doctrina de LOTE (primera vez que se usa; aplica a todo el acto)

Un lote = una sesión, un PR, N tareas en el orden listado, commits con prefijo T\<n\>. PARO por tarea, no por lote: si T\<k\> para, se reporta (el reporte ES el entregable de esa tarea) y se sigue con T\<k+1\> salvo dependencia declarada. Cada tarea cierra con su línea de contador ("T\<n\> movió: X"). Perímetro del lote = unión de los perímetros por tarea; escribir fuera de la unión = PARA global. Un ADR del lote con subsección por tarea. Filas nuevas: máximo id derivado al escribir y al fusionar. Las compuertas de firma son por tarea: una cadena ausente detiene solo SU tarea. Dependencias de este lote: ninguna entre tareas.

### ════════ ARRANQUE ════════

1 · REPO: clon existente; ruta · git log -1 · git status. 2 · SHA: contra b4a9b3f; si se movió, refresca y reporta. 3 · data/raw: no se toca — dilo y salta. 4 · ENTORNO: la variable cruda · type grep (y si envuelve algo, command grep para todo veredicto) · regla nueva medida ayer: un negativo producido por un comando que no examinó archivos no es un negativo — pega siempre el conteo de archivos examinados junto a cada NO-ENCONTRADO. 5 · ESPEJO: nada del espejo; cifras del clon con comando a la vista. ═════════════════════════

### T0 · El commit colgante de fp57 (deuda de 30 segundos, tres recordatorios ya)

git cherry-pick 12e3b6c (rama claude/fp57-declara-…, 1 adelante: el backfill del número de PR #279 en fila y encargo). Verifica que aplicó limpio. Al fusionar este lote, esa rama queda a 0 y mesa la borra. Contador: 0.

### T1 · FP-66 — el contador de condicionales deja de contar por cadena

Ley: fila FP-66. La fórmula txt.count('clase: "MEDIDO-…') puede contar dos veces la misma condicional. Deriva el valor VERDADERO parseando estructura (yaml/parser real, no substring), compara contra el declarado ("12 de 15"), y: si difiere, corrige el declarado con tu derivación a la vista y di cuánto mentía; si coincide, la fórmula era frágil pero no mordió — dilo igual. Corrige la fórmula en tests/test_motor_procedencia.py/T19b por parser, no por otra cadena. Fila FP-66 → ejecutada. Contador: el que resulte, con su derivación.

### T2 · FP-62 — adjudicación de rescate/reconcilia-puertas-local

Ley: fila FP-62. El addendum de la propia rama (f169abd) declara "PR #208 (nube) ya cerró este encargo". Verifica: diff de sus 122 líneas únicas y 2 archivos contra main (#208, #275/ADR-111, #280/FP-12-cerrada-sin-fusionar). Veredicto por contenido: DUPLICA (→ archiva la nota única como forense/notas/…-reconcilia-puertas-local-historico.md con procedencia, y deja dicho que la rama se borra al fusionar) · COMPLEMENTA (→ rescata lo que agregue como enmienda in situ fechada donde toque) · CONTRADICE (→ NO resuelvas: fila nueva con el conflicto exacto). Fila FP-62 → ejecutada. Contador: 0 salvo rescate sustantivo.

### T3 · FP-64 — candidatos para la llave (ii)

Ley: fila FP-64 + ADR-57(c) (experimento natural con grupo de comparación sobre encuestas repetidas; ENOE descartado por dos razones — léelas y hónralas). Deriva candidatos contra esos criterios: ENSU (trimestral, ciudades), ENCO (mensual), olas ENVIPE/ENSAFI, evaluaciones CONEVAL/IPA con grupo de comparación, y lo que el manifiesto ya tenga (crúzalo contra data/coef-universo-v1_0.tsv). Tabla: candidato · diseño posible · qué evento/corte natural · veredicto A.4 · qué falta para ejercerla. NO adjudicas: si UN candidato queda EXISTE-SATISFACE con diseño escribible, la fila pasa a "propuesta lista, firma de mesa"; si ninguno, NO-ENCONTRADO con universo y la fila lo registra. Contador: 0 (este es el paso previo al que sí mueve).

### T4 · FP-65 — la corroboración ENBIARE contra ADR-109(d)

Ley: fila FP-65 + forense/bbis-radio-confianza-enbiare-v1_0.md. El par PB1_01×PB1_02 NO refutó con espec congelada. Adjudica la relación con ADR-109(d) (que revocó REL-51392f82): si la corroboración acota o revierte esa revocación, patrón corrige-sin-tocar (ADR nuevo cita al viejo, estampa A.10, universo de cada uno a la vista); consecuencia explícita sobre G1b/radio_confianza en el motor con su clase de procedencia. B-bis manda: di qué significa exactamente que el falsador no refutara — corroborada, acotada, o falsador débil — según lo que la ficha congelada declaró. Fila FP-65 → ejecutada. Contador: si re-tieriza G1b, dilo con la clase vieja→nueva.

### T5 · FP-67 — el entorno de la adquisición de U2/EV-1

Ley: fila FP-67. Adjudicación trivial y ya medida: la descarga de CV/EE/IC va a UBUNTU (nube tiene egreso a INEGI bloqueado por política, medido por dos vías). Escribe la asignación en la fila (ejecutada; la ejecución material vive en LOTE-UBUNTU-ADQ-1 T1) y cita el hallazgo. Contador: 0.

### T6 · FP-68 y FP-69 — dos sellos de mesa, con compuerta por fila

⛔ Cada una SOLO con su cadena en el mensaje de lanzamiento; sin cadena, esa fila queda "material listo, firma pendiente" y sigues. FP-68 (FIRMO FP-68: ADR-67(c) gobierna): la colisión de contadores se resuelve a favor de ADR-67(c) — un veredicto de diseño por regla de elegibilidad NO cuenta en el 27 de Hito D; el renglón de R5.1-D3 alimenta la métrica llaves de identificación ejercidas. Propaga: corrige la declaración de ADR-110(a) sin tocarla (patrón conocido), y deriva el contador de llaves que resulte (di si queda 2 de 2, con la definición a la vista). FP-69 (FIRMO FP-69: B se sella): el veredicto EJERCIDA_INDECISA (fila B) de R5.1-D3 entra al registro append-only de hitoD-preregistro tal como la precedencia sellada A→E→B→C→D lo produjo — DiD −1.82pp IC95 (−5.11, +1.48) cruza cero y la compuerta de monto empeora (29.05%→26.45%) recalculada al universo primario. Hito D queda 13 de 27, honesto. Contador por tarea: el de llaves si FP-68 firma; Hito D no se mueve y se dice.

### Cierre del lote

ADR del lote (número derivado al escribir Y al fusionar; hoy máx ≥125) · hallazgos.md una línea por hallazgo real · nota del lote con la tabla T0–T6 y sus contadores · este encargo CONSUMIDO · tests/check.py --baseline VERDE en tu árbol final.

### Perímetro (unión; fuera = PARA)

tests/test_motor_procedencia.py (T1) · forense/notas (T2, T4) · milpa/refutations.yaml y canon/modelo-decision solo pasajes G1b (T4) · canon/hitoD-preregistro (T6, append) · tablero (FP-62/64/65/66/67/68/69) · gobernanza (ADR) · estado-programa (cascada + contadores que T1/T6 deriven) · hallazgos · nota · este encargo · el cherry-pick T0.

---

## CONSUMIDO

**Ejecutado por `LOTE·NUBE-DECISIONES-1`, 19/ago/2026, `ADR-126`.** Las siete tareas (`T0`-`T6`) corrieron en orden, ninguna paró. Tres correcciones de premisa material, encontradas y declaradas contra el propio texto de este encargo: `FP-62` citaba `FP-29` en vez de `FP-10`/`FP-12` como cierre de referencia; `FP-65` nombraba `G1b/radio_confianza`, que no existe — el coeficiente real vive en `G1a`/`G5`; `FP-69` anticipaba `"2 de 2"` como resultado del sello, cuando la propia receta del registro ya daba `2 de 3` (el denominador había subido antes, por acto distinto). Ninguna corrección cambió el fondo de lo que dirección pedía — las tres se declaran porque `AGENTS.md` exige distinguir discrepancia material de cosmética, y las tres eran materiales (apuntaban a la fila, el coeficiente o el contador equivocado). `canon/hitoD-preregistro-v2_0.md`, nombrado en el perímetro para `T6`, no se tocó: escribir ahí habría sido mecánicamente incorrecto (`ADR-67(c)`, `T18`/`T20`) — declarado en vez de ejecutado por seguir la letra. Detalle completo, tarea por tarea, con cada contador y su derivación: `forense/notas/2026-08-19-lote-nube-decisiones-1-cierre.md`. ADR del lote: `canon/gobernanza-v1_15.md`, `ADR-126`. `tests/check.py --baseline`: **21 FAIL · 118 WARN, LÍNEA BASE: VERDE**, sin `--freeze`.
