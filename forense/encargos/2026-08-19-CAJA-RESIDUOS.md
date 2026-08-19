# ENCARGO · CAJA-RESIDUOS — los tres residuos que #278 reportó sin fila

*(Archivado verbatim por regla A.3. Ejecutado en `ACTO CAJA-RESIDUOS`, 19/ago/2026 — ver `forense/notas/2026-08-19-caja-residuos-cierre.md`.)*

---

Redactado por dirección el 19/ago/2026 contra 35c9c9f (main con #278). Re-deriva al arrancar. ENTORNO ASIGNADO: UBUNTU (los tres residuos viven solo en el disco). NO lanzar en NUBE. Corre DESPUÉS de COEF-UNIVERSO (dueña única; COEF está en la caja ahora). Modelo: Opus. 🚫 --freeze.

Los tres residuos (derivados de forense/notas/2026-08-19-limpia-caja-cierre.md §5-§6 y ADR-113 — la ley de fondo; este encargo la ejecuta, no la re-adjudica)

R1 · ~/mm-purga.git (12M). Espejo bare de PURGA-PRIVACIDAD con historia pre-purga completa (168 refs, incluye 9301e59) y artefactos filter-repo/ (commit-map, ref-map). Es a la vez: (a) el único registro de auditoría de la purga, y (b) las 1,737 filas personales purgadas, todavía en disco, y el vector de resurrección que la regla "prohibido empujar ancestría pre-purga" existe para impedir. R2 · ~/mm-paso5 (25M). Tercer clon, f420498 (PASO 5 de la purga), ya fusionado, 0 untracked. Podable sin drama. R3 · mm-reconcilia-puertas. Worktree vivo con contenido único verificado: rama que nunca existió en origin, 5 commits, 2 archivos, su nota trae 122 líneas ausentes de la versión de main. Nadie lo ha adjudicado contra el cierre de FP-29 (#275) ni contra FUSION-PUERTAS (corriendo hoy en NUBE).

VERIFICACIÓN DE EXISTENCIA (dirección, 19/ago)

1 · ESTRUCTURA. Gobiernan: nota #278 §5-§6, ADR-113, tablero. 2 · CONTENIDO. ¿Filas para R1-R3? La nota declara "Ninguna fila nueva" (línea 116) y el tablero no las tiene (derivado hoy: ABIERTAS = FP-26·57·58·60) → NO-ENCONTRADO; este acto las abre. ¿Los mapas de la purga ya están en el repo? git ls-files | grep -iE "commit-map|ref-map" → re-derívalo tú; dirección no lo corrió. 3 · RETRO. ADR-113 es de ayer; sin brecha.

════════ ARRANQUE ════════ 1 · REPO: clon base /home/pc0/Modelado-Mexicano (no clones). Reporta ruta · git log -1 · git status. 2 · SHA: compara contra 35c9c9f; si se movió, refresca y reporta. 3 · data/raw: este acto no abre microdato — dilo. El corpus NO se toca. 4 · ENTORNO (A.2): variable · sonda INEGI · ls data/raw/ | head -1. Crudos. 5 · ESPEJO: cifras solo del disco/clon, comando a la vista. Los conteos de arriba (168 refs, 122 líneas, 12M/25M) se re-derivan. ═════════════════════════

Fases

F1 · R3 primero — hacer visible lo invisible (si mesa no lo empujó ya a mano). git -C /home/pc0/mm-reconcilia-puertas push origin reconcilia-puertas:rescate/reconcilia-puertas-local — push de rama, sin merge. Verifica en ls-remote. Abre fila (id = máx del tablero + 1, derivado al escribir Y al fusionar): "¿El contenido único de reconcilia-puertas-local (122 líneas, 2 archivos) complementa, contradice o duplica el cierre de FP-29 (#275) y el producto de FUSION-PUERTAS? Adjudicación en NUBE con ambos a la vista." Después del push verificado: git worktree remove del worktree (el contenido ya vive en origin). F2 · R1 — auditoría a repo, PII a la trituradora, CON COMPUERTA DE FIRMA. (a) Extrae commit-map y ref-map del espejo; verifica por comando que son solo pares sha↔sha/refs (cero PII: corre la compuerta patrón #274 sobre ellos); commitéalos a forense/purga-privacidad/ con su sha256 y una nota de dos líneas (son el único rastro auditable de qué reescribió la purga). (b) ⛔ PARA AQUÍ salvo firma. La destrucción del espejo es irreversible y elimina la única copia pre-purga. Solo procede si el launcher/mensaje de mesa trae la firma verbatim: "AUTORIZO DESTRUIR mm-purga.git". Sin esa cadena exacta: deja el espejo intacto, marca la fila de R1 como FIRMADA-PENDIENTE-EJECUCIÓN y cierra el acto — eso NO es fracaso. (c) Con firma: shred/rm -rf ~/mm-purga.git, verifica ausencia por ls, y registra en la fila y el ADR: qué se destruyó, bajo qué firma, con los mapas ya a salvo en <sha del commit de (a)>. F3 · R2. rm -rf ~/mm-paso5 tras re-verificar por comando: HEAD ancestro de origin/main y status --porcelain vacío. Pega ambos. F4 · Cierre. Estado final (worktree list, directorios, df -h una línea) · fila(s) de este acto ejecutadas/abiertas según toque · ADR (número derivado al escribir Y al fusionar) · hallazgos.md una línea · nota · encargo CONSUMIDO. Contadores de medición sobre México: 0 — dilo.

Perímetro (fuera de la lista, PARA)

Disco: ~/mm-purga.git · ~/mm-paso5 · /home/pc0/mm-reconcilia-puertas · nada más (corpus y clon base: lectura). Repo: forense/purga-privacidad/ (nuevo) · rama rescate/reconcilia-puertas-local (push, no merge) · tablero (filas de este acto) · canon/gobernanza (ADR) · canon/estado-programa (cascada) · hallazgos.md · nota · este encargo.

Concurrencia

COEF-UNIVERSO precede en la caja. En NUBE hoy: ola-1 + FP57-DECLARA + lo que dirección lance. La adjudicación de contenido de R3 NO es de este acto: este acto solo lo hace visible.

---

**`encargo` → `CONSUMIDO`** (`ACTO CAJA-RESIDUOS`, 19/ago/2026).
