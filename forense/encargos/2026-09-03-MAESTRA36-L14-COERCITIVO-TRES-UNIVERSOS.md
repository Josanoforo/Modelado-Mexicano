ENCARGO · ACTO MAESTRA36-L14 · COERCITIVO-TRES-UNIVERSOS

SHA de redacción: 18fd2bd · v2.12 · Estado: LISTO PARA LANZAR — COMPUERTA: ninguna (L13 fusionado, #502, ADR-312). ENTORNO: UBUNTU (ENOE y .xls del SAT en corpus). NO en NUBE. MODELO: Opus. Invoca /acto.

FIRMA DE MESA (verbatim, arriba, #1). Lectura de dirección: mesa no autoriza sellar sobre el padrón del SAT; pide el universo poblacional. Este acto mide y no adjudica.

A.8, contra 18fd2bd: ENOE en manifiesto → grep -aci '^- id: enoe' data/manifiesto.yaml = 416; el trimestre de corte lo fija P0 (dirección espera 2025-4T o 2026-1T, el que exista con COE y SDEM). SAT: ids firelenumcontri, portipocontribuyente (L13, ADR-312, corte 2025-12). Medición previa bajo lectura A: grep -rn 'ocupad\|PEA\|informal' forense/notas/2026-09-03-MAESTRA36-L13-* → 0 (universo: las tres notas de L13). NO-ENCONTRADO.

P0 · Denominadores ENOE, congelados antes de dividir (COMMIT-1). Del trimestre de corte, con ponderador FAC_TRI sobre SDEM (población ≥ 15 ocupada, CLASE2 = 1): (a) ocupados totales; (b) ocupados informales (EMP_PPAL = 1) y formales; (c) ocupados formales no asalariados (POS_OCU ∈ {2,3} con EMP_PPAL = 2) como aproximación ENOE del «obligado». IC95 por diseño con UPM/EST_D. Los códigos exactos se leen del diccionario ENOE del corpus y se pegan; discordancia con el catálogo → PARO. Frase de sello.

P1 · Las tres razones, misma cifra arriba, tres abajo (COMMIT-2). Numerador único: contribuyentes con e.firma vigente al corte (FirEleNumcontri, L13). p_A = num / ocupados totales · p_B y p_C = las de L13, re-citadas, no recalculadas · además p_A' = num / ocupados formales como puente entre A y B. Escala declarada: proporción administrativa sobre denominador de encuesta — dos fuentes con universos que no coinciden exactamente (personas morales en el numerador; menores de 15 fuera del denominador): se enumeran las incompatibilidades y se acota el efecto de cada una con signo. Nada se compara contra el 0.09 salvo en orden de magnitud; ninguna fila de veredicto: este acto no adjudica, entrega la tabla.

P2 · Tabla para mesa, una página. Las tres lecturas × (denominador, p, IC/cotas, qué incluye, qué excluye, qué confunde). Abajo, la pregunta a mesa, sin recomendación de dirección: «¿A quién describe coercitivo: A, B o C?». Entra a la propuesta como MEDIDO·tabla-de-universos, PENDIENTE-DE-MESA, sin p única.

PERÍMETRO: tools/medidor_l14_coercitivo_universos.py · data/l14-coercitivo-universos-v1_0.json · data/INFRAESTRUCTURA-v1_0.md · milpa/tramite-ola5-propuesta-v0.yaml (append) · forense/notas/…L14-* · forense/hallazgos.md · forense/firmas-pendientes.tsv · cascada. NO toca milpa/tramite.yaml, milpa/procedencia.yaml, data/manifiesto.yaml, data/curacion-registro/**. Frase del perímetro. CONTADOR: S1 sigue en 1, declarado; lo que se mueve es «lecturas de universo medidas para coercitivo: 2 → 3». Sucesor: la letra de mesa (A/B/C) → N13 · SELLA-COERCITIVO con la p de esa lectura.

Línea a hallazgos.md: dirección recomendó sellar coercitivo sobre el padrón del SAT (subpoblación) contra una regla poblacional — A-bis 4 / A.10; mesa lo atrapó.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA36-L14 · COERCITIVO-TRES-UNIVERSOS` el 3/sep/2026,
entorno UBUNTU, worktree `/home/pc0/mm-l14-coercitivo`, con la skill `/acto`
(`ADR-237`). `COMMIT-1` `da68109` (spec congelada), `COMMIT-2` `7f6c676`
(las tres lecturas y la tabla), merge de `origin/main` `57f9575`, cascada
`ADR-314`. **PR: ver el PR abierto contra `main` con el rótulo del acto.**

Desviaciones de la premisa del encargo, declaradas donde no se pueden perder
(`ADR-314`, notas `P0` y `P1`):

1. **`A.8`** declara `grep -aci '^- id: enoe' data/manifiesto.yaml = 416`; el
   árbol de `18fd2bd` da **91** (1 102 entradas `- id:` en total). No es `PARO`:
   el payload se identifica por `sha256`, no por el conteo.
2. **El numerador no es «e.firma vigente al corte».** `firelenumcontri` cuenta
   *primeras* altas acumuladas desde `2004-01` y no da de baja al que caducó.
   Se midió con la premisa corregida y las cinco `p` se declaran cotas
   **superiores**.
3. **«`EST_D`»** no existe en el diccionario ENOE del corpus; con ponderador
   trimestral el estrato es `est_d_tri`. Nomenclatura, no discordancia de código:
   las ocho claves de la spec concuerdan `8/8` con el catálogo del `.zip`.
4. **El criterio del trimestre no desempata**: los dos candidatos existen con
   `COE` y `SDEM`, así que `P0` declaró un criterio propio antes de medir
   (`2025-4T` contiene el corte `2025-12` del numerador).
