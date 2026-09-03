# ENCARGO · RESCATE-CURADOR

Estado: CONSUMIDO · SHA de redacción: `cb0d98f` (#266) · Ejecutado contra `cb0d98f`→`6ded00c`→`e6864ed`→`6650047` (re-derivado a cada paso, nunca asumido) · PR: **#274** · Cierre: `ADR-112` (candidato `111` al escribir; `PR #275`/`FP29-RECONCILIA` tomó `111` primero al fusionar, renumerado por comando) · `FP-59` (candidata `FP-58` al escribir; `PR #275` tomó `FP-58` primero, renumerada) · Origen: `FP-55` (`NOTAS-P3`, #261) + decisión `D-4` de mesa en `MESA-19AGO` (PR #267).

Archivado retroactivamente (A.3): el texto original se recibió en dos versiones dentro de la misma conversación — v1 (alcance limitado al worktree `curador`, corrió únicamente `§0`/el bundle) y v2 (abajo, verbatim, la que gobernó el resto del acto: expande a los 26 worktrees de `w-limpieza §4`). La corrección de premisa (`ACTO Z` ya había cerrado el titular de "590 commits" un día antes de que `NOTAS-P3` abriera `FP-55`) se descubrió **verificando el repo antes de escribir**, no estaba en ninguna de las dos versiones del encargo, y se resolvió con la DIRECTIVA de mesa citada íntegra abajo, seguida de ocho precisiones adicionales de mesa (segunda adenda) que corrigieron el propio plan de ejecución de esa directiva contra el árbol real.

---

## v2 — el encargo operativo (verbatim)

ENCARGO · RESCATE-CURADOR — los 590 del worktree, y de paso los otros 25 que nadie adjudicó

SHA de redacción: cb0d98f (#266) · Entorno: UBUNTU (la caja; el trabajo es sobre refs locales del clon base) · Modelo: Opus · Estado: VIVO Gate: caja libre — después de que B2-SEMANTICO cierre y fusione. (El paso 0 puede haberlo corrido ya mesa a mano; entonces se verifica, no se repite.) Origen: FP-55 (NOTAS-P3, #261) + decisión D-4 de mesa en MESA-19AGO. Ley de contexto: forense/notas/2026-08-13-w-limpieza-worktrees.md §2-§5 — inventario de 37, 11 borrados FUSIONADO, 26 sobreviven (§4, tabla con commits-sin-empujar), y §5.5 declara a Modelado-Mexicano-curador (590, ancestor=NO, tooling real: curador.py, supervisor.py, tests, multi1-staging/, multi2-staging/) "la pieza más grande del inventario sin adjudicar — candidato a su propio acto". Este es ese acto — y adjudica también a los otros 25, porque §5 los dejó vivos sin veredicto. 🚫 Sin --freeze · read-only sobre los worktrees viejos: nada se commitea EN ellos, nada se rebasa, nada se borra hasta el paso 4.

════ ARRANQUE ════ los 5 estándar de caja + regla del pkill (ningún proceso ajeno vivo; staging con dueño) + una adicional: git worktree list completo, crudo, como primera salida — es tu mapa.

VERIFICACIÓN DE EXISTENCIA (contra cb0d98f — re-córrela)
la tabla de los 26:        w-limpieza §4 (ramas, conteos 590…299, worktrees)      EXISTE-SATISFACE
la fila:                    FP-55 — estado tras MESA-19AGO: derívalo (FIRMADA con D-4, o ABIERTA)
el bundle de mesa:          ~/respaldo-worktrees/*.bundle — puede existir ya       A VERIFICAR (paso 0)
qué llegó a main de los 3 con nombre (filas 20-22: p-lapop 424 · regla-elegibilidad 304 ·
  cruce-catalogo 299):      sus entregables SÍ parecen estar en main por otros PRs — verifícalo por
                            contenido (las notas e4c/preregistro/cruce viven en forense/), no por sha  A DERIVAR
PERÍMETRO

Escribe SOLO: forense/notas/ (la nota de este acto: inventario + mapa de contención + cosecha) · forense/firmas-pendientes.tsv (FP-55) · gobernanza (ADR) · cascada de estado (post-split: derivada) · hallazgos.md (append) · forense/encargos/ · y, para la cosecha del paso 3, ramas NUEVAS rescate/<línea> con PRs normales — jamás la rama vieja directa. Fuera de eso — incluidos los 26 worktrees, el corpus y data/ — read-only estricto.

Paso 0 · El bundle — crear-o-verificar, idempotente

Si mesa ya lo corrió: sha256sum del archivo, tamaño y git bundle verify — se registra y no se repite. Si no: mkdir -p ~/respaldo-worktrees && git -C <clon-base> bundle create ~/respaldo-worktrees/mm-todas-$(date +%Y%m%d).bundle --all && sha256sum ~/respaldo-worktrees/mm-todas-*.bundle --all desde el clon base cubre las 26 ramas de un golpe — los worktrees comparten el mismo .git, así que un solo bundle congela todo el riesgo, no solo el curador. Registra sha256 + ruta + tamaño en la fila y en la nota. Desde aquí la pérdida ya no es posible; lo que sigue es orden.

Paso 1 · Inventario del curador + mapa de contención de los otros 25

1a — curador: git log --oneline --stat origin/main..codex/curador-baseline-semantico, resumido por directorio: qué líneas de trabajo contiene (curador.py / supervisor.py / tests / multi*-staging / otro), fechas primera-última, y diff real contra main de tools/curador_registro/ — el tooling de main evolucionó por otra vía (lista cerrada ADR-95): el diff dice qué es novedad y qué es versión vieja de lo mismo. 1b — contención: para cada una de las otras 25 ramas: git merge-base --is-ancestor <rama> codex/curador-baseline-semantico → CONTENIDA (bundle+curador ya la cubren; adjudicada por contención) o NO-CONTENIDA (entra al paso 3 con línea propia). La cadena descendente 590→575→…→477 de los wt-* de Codex huele a un mismo linaje — el mapa lo dice con comando, no con olfato.

Paso 2 · Prompt único a mesa — la cosecha se decide, no se asume

Con el inventario en pantalla (líneas de trabajo del curador + las NO-CONTENIDAS + el veredicto por-contenido de las filas 20-22): opciones por línea — FUSIONAR (cherry-pick a rescate/<línea>, tests, PR normal) / ARCHIVAR (queda en el bundle, con nombre, sin PR) / DESCARTAR con acta. Mesa marca; nada se cosecha sin su marca.

Paso 3 · La cosecha (solo lo marcado FUSIONAR)

Por línea: rama nueva desde origin/main → cherry-pick selectivo (nunca merge de la rama vieja: su base es ancestral y arrastraría regresiones — el diff de dos puntos de hoy mostró −2,352 líneas ilusorias por exactamente esa razón) → suite VERDE → PR normal con el mapa de qué commits del bundle trae. Conflictos contra el tooling vigente se resuelven a favor de main, salvo que la marca de mesa diga lo contrario para esa línea.

Paso 4 · Cierre

FP-55 → FIRMADA/ejecutada (bundle sha + veredicto por rama: CONTENIDA n · FUSIONADA n · ARCHIVADA n · DESCARTADA n — los cuatro suman 26) · ADR (re-derivado ×2; base hoy: 106) · cascada · nota · hallazgos.md · CONSUMIDO. Los worktrees marcados DESCARTAR/ARCHIVAR se limpian (worktree remove + branch -D solo ahora, con el bundle verificado como red). Auditoría: contadores México: cero — acto de entorno, como el ACTO W del que desciende; lo que mueve: 26 incógnitas → 26 veredictos con red de bundle. Nada de memoria: contención por comando, cosecha por marca de mesa.

---

## DIRECTIVA · cierre de RESCATE-CURADOR — respuesta de mesa, verbatim

DIRECTIVA · cierre de RESCATE-CURADOR — respuesta de mesa a tu pregunta, con las dos cosas a la vez

Contra 6ded00c (#273) · ADR base al redactar: 107 — re-deriva al escribir y al fusionar.

Tu verificación previa valió el acto entero: el titular estaba vencido y lo probaste con comando. Se procede así — no se retiene nada:

1 · La corrección entra a la nota, con ACTO Z como fuente

El encargo que recibiste queda corregido por esta directiva (archívalo CONSUMIDO con la directiva pegada como adenda). La nota del acto abre con el reframe, citando forense/notas/2026-08-13-z-inventario-curador.md:3-4 verbatim: contenido único NINGUNO; los 590 son historia pre-purga (merge-base = 9301e59, 29/jul; HEAD en canon/remapeo-shas-purga-2026-08-10.tsv). Estilo A.10: el sello de w-limpieza/FP-55 fue correcto contra su universo (método git-history) y ACTO Z ya lo había cerrado un día antes sin que nadie cruzara las referencias — la prudencia de NOTAS-P3 no se refuta; el número sí. Ese no-cruce es hallazgo propio: una línea en hallazgos.md.

2 · El barrido de los otros 24 — dos comandos, cierra la tabla §4 entera

Por cada rama restante de w-limpieza §4: git merge-base origin/main <rama> (¿= 9301e59?) y ¿su HEAD ∈ remapeo-shas-purga…tsv? → adjudicación PURGA-ARTIFACT en tabla (las que no cuadren, quedan nombradas con lo que salió). Con eso los conteos 575…299 dejan de ser 24 incógnitas.

3 · Protección del untracked — el riesgo real que encontraste

Mesa corre ya el tar (comando entregado aparte); tu paso: verifica sha256+tar -t del archivo. Luego el rescate limpio:

Worktree propio nuevo desde origin/main (git worktree add ../mm-rescate -b rescate/curador-untracked origin/main). La caja tiene dueña (b2-semantico): prohibido tocar su worktree, staging, .barrido2/ o el corpus; tu escritura vive solo en ../mm-rescate y ~/respaldo-worktrees/.
Copia SOLO los untracked listados (tools/curador_registro/* del worktree viejo, multi1-staging/, multi2-staging/) a forense/rescate/curador-untracked-20260807/ — NO a tools/: la lista de ADR-95 es cerrada; promover algo al tooling vivo es adjudicación posterior con marca de mesa, no parte de este rescate.
Compuerta PII antes de cualquier push: la purga existió por 1,737 filas de datos personales; barre el contenido (grep conservador: CURP/RFC/teléfono/email/nombre+apellido en filas de datos; los .tsv de staging con lupa). Hit ⇒ ese archivo NO entra al commit, queda solo en el tar, y se anota qué y dónde.
Prohibido empujar ancestría pre-purga, hoy y siempre — cualquier push de esas ramas resucita los blobs purgados. El rescate viaja únicamente en commits nuevos sobre origin/main.
PR normal con el inventario de qué archivos trae y de dónde.
4 · barrido-completo y la relación N1-N33

Dentro del mismo acto: fila nueva en el tablero para Modelado-Mexicano-barrido-completo (883 untracked / 51MB, cero commits, cero PR — riesgo real ya asentado en tu reporte; el tar de mesa ya lo cubre). Y la pregunta que dejaste abierta se responde con comando en el PR: compara uso de N1-N33 y archivos entre ambos cuerpos → MISMA-OBRA-EN-DOS-MITADES / TEMAS-COINCIDENTES-OBRAS-DISTINTAS / NO-DETERMINADO con qué faltó. Su rescate-commit es acto sucesor, no de hoy.

5 · Cierre

FP-55 → FIRMADA/ejecutada con el desglose: historia=PURGA-ARTIFACT (ACTO Z + tu barrido de 24) · untracked=PR rescate/curador-untracked · tar sha256 como red · fila nueva de barrido-completo abierta. ADR (re-derivado ×2, y ojo: b2-semantico trae 106/107 en su rama — la colisión al fusionar es segura, síguele el protocolo) · cascada derivada · nota · hallazgos.md · encargo CONSUMIDO. Los worktrees adjudicados PURGA-ARTIFACT no se borran en este acto — limpieza física es acto aparte, con el bundle+tar verificados como red. Auditoría: México cero; lo que mueve: 26 incógnitas → 26 veredictos, y ~1.7MB de ingeniería real fuera de riesgo.

---

## SEGUNDA ADENDA · ocho precisiones de dirección, verbatim

ADELANTE con la vía que propones — ADR nuevo que cita y corrige, sin tocar ADR-110 — con ocho precisiones de dirección, verificadas contra el repo:

1 · CORRIGE TU PREMISA PRIMERO. origin/main NO se ha movido: sigue en e6864ed (#267), cero commits encima, derivado por fetch al escribir esto. PR #274 es TU PR y está ABIERTO (refs/pull/274/head = 64609c4). Tu "7 PRs en ~75 min" es real solo relativo a tu base vieja — todo ya vive bajo e6864ed. Re-deriva tu foto antes de escribir una línea, y que tu ADR no afirme "#274 fusionado" en ninguna parte.

2 · TODO VIAJA EN TU MISMA RAMA, dentro de #274: ADR correctivo + fila FP-55 + nota. Un solo merge atómico (rescate + corrección + cierre); ejecutada_en=PR #274 auto-referencial es patrón ya usado (A.3, "archivado y CONSUMIDO en el mismo acto"). Nada en PR aparte.

3 · CLASIFICACIÓN EXACTA. La conclusión de ADR-110(d) ("no hay contenido que rescatar ni riesgo de pérdida") se corrige como CONCLUSIÓN MÁS ANCHA QUE SU UNIVERSO DECLARADO (A.10 Corolario 2 / ADR-67(b)) — su universo está a la vista en el propio ADR: git diff --diff-filter=A sobre lo commiteado, que no puede ver untracked por construcción. NO es VENCIDO EN ALCANCE: el contenido (7/ago) precede al sello; el universo no creció, la conclusión nació excedida. Y dilo con las dos mitades: el fondo de mesa sobre el titular 590 (VENCIDO por ACTO Z) queda INTACTO — corriges la extensión del ejecutor, no la firma.

4 · Tu ADR porta estampa A.10 propia: SHA contra el que derivas, universo examinado (rama, untracked rescatado, barrido de 24 worktrees), y denominador si existe — si no existe, se escribe que no existe.

5 · NÚMERO: re-deriva al escribir Y al fusionar. Hoy main da máx 110 → candidato 111, pero hay tres actos en vuelo (ADQ-15 y REFIRMA-OPACA en UBUNTU, FP29-RECONCILIA con PR #275 abierto) — colisión esperada; el propio ADR-110 se renumeró tres veces.

6 · FILA FP-55: completa ejecutada_en/encargo como la fila lo pide. Para el estado final, deriva la convención del tablero por precedente (FP-15 quedó CERRADA tras ejecutarse) — mesa dijo verbatim "se corrige y cierra".

7 · PERÍMETRO: canon/gobernanza (ADR nuevo), forense/firmas-pendientes.tsv (SOLO fila FP-55), canon/estado-programa (solo cascada, derivada de donde el split la dejó), tu nota, y lo que tu directiva ya te asigna. Si te encuentras escribiendo fuera de esta lista, PARA. T22 sobre tus archivos propios: patrón _T22_ARCHIVOS_CONOCIDOS (precedente #261/#262), no freeze.

8 · Contadores de medición sobre México que mueve este cierre: cero. Dilo en una línea, sin justificarlo.

---

Detalle completo, comando por comando: `forense/notas/2026-08-18-rescate-curador-cierre.md`.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-18-RESCATE-CURADOR.md" canon/gobernanza-v1_15.md` → 4: citado bajo ADR-112 en canon/gobernanza-v1_15.md, con lenguaje de ejecución (archivado/ejecutado) en el bloque correspondiente. Marca ausente en el archivo era defecto de trámite, no evidencia de no-ejecución.
