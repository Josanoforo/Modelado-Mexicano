ENCARGO · ACTO MAESTRA38-CRON-3 · HUELLA-REAL-Y-PRUEBA-EN-CAJA — caja mm-adq, Sonnet, invoca /acto
dirección (Fable) · 6/sep/2026 · contra origin/main = ef9ba36 · ramas vivas: censo/2026-09-06 (#556), acto/maestra38-cron-diagnostico-clean (#557), claude/cron-registro-canonico-onfk76 (#558) · decidido en conversación; la firma es el merge

Orden previo, de mesa, antes de lanzar: fusionar #556 y #557 (D-a, firmada). #558 no se fusiona: este acto lo corrige encima y abre un PR que lo sustituye; #558 se cierra con la nota «superado por CRON-3».

Firmas verbatim
«no puede ser que no esté identificado ni sepamos si se usa o cuando» (6/sep) — es la razón de la huella real.
D-b: obligar a [ADQ] a dejar huella siempre · D-c: re-escanear tras [ADQ-PDN] · D-d: nota en /acto — las tres firmadas en conversación.
Revisión de #558 (dictamen de dirección, verificado contra la rama)

Conserva: forense/cron/REGISTRO-CRON-v1_0.md · fila INFRAESTRUCTURA · T31 T-CRON + tests/test_t_cron.py · nota D-d en acto.md · línea de hallazgos. Corrige: (1) [ADQ] en adquiere_cron.sh:76-91 se escribe antes de claude -p con N = filas de la cola y 0 fijo — no es huella, es constante; (2) el append [ADQ-PDN] (:171-174) cae después del push de censo/<fecha> (:106-110) y nunca se commitea; (3) falta cascada: ADR, fila TSV del tablero, A.3 del encargo.

ARRANQUE

Caja mm-adq, clon /home/pc0/mm-adq — no un worktree nuevo: el crontab apunta a este clon. git fetch origin && git checkout -B acto/maestra38-cron-3 origin/claude/cron-registro-canonico-onfk76 && git rebase origin/main (tras fusionar #556/#557). A.2 tres partes; crontab -l pegado en el 0-bis. Guard de rama. 0-bis al minuto: archivar este encargo verbatim en forense/encargos/2026-09-06-MAESTRA38-CRON-3-HUELLA-REAL-Y-PRUEBA.md (A.3).

COMMIT-1 · Especificación de la huella (congelada antes de tocar el script)

La huella [ADQ] es una línea por corrida, escrita al final, con lo que pasó de verdad, y se commitea en la rama censo/<fecha> con su propio commit ([ADQ] <fecha>), después del claude -p o de cualquier PARO. Formato único:

[ADQ] <fecha> <HH:MM>: invocado=<si|no> motivo=<-|PARO-RAIZ|PARO-RED|PARO-PROMPT|PARO-CORPUS> exit=<código|-> duracion=<s> commits_nuevos=<k> ramas_nuevas=<j> archivos_modificados=<m>

commits_nuevos = git rev-list --count <HEAD antes>..<HEAD después> en el clon; ramas_nuevas = diferencia de git ls-remote --heads origin | wc -l antes/después; archivos_modificados = git status --short | wc -l tras la corrida. Si invocado=no, los tres últimos son 0 medidos, no supuestos. Con esto la pregunta «¿se usa?» tiene respuesta cada día hábil: invocado=si exit=0 commits_nuevos=0 significa «corrió y no produjo nada», que es distinto de «no corrió», y ambos son distintos de «no sabemos». [ADQ-PDN] (días 1–3): el re-escaneo se añade al censo y se commitea en la misma rama con [ADQ-PDN] <fecha>; fuera de ventana escribe una línea [ADQ-PDN] <fecha>: fuera de ventana (también commiteada, para que el día 4 no parezca silencio). Frase de sello: «el primer resultado que produzca este procedimiento es el que se reporta».

COMMIT-2 · Cambios
tools/adquiere_cron.sh: quitar las líneas 76–91 de #558 (capturar HEAD_ANTES, RAMAS_ANTES, T0 justo antes del paso 2.5; función huella_adq() que arma la línea del COMMIT-1, hace git checkout censo/<fecha> (si existe; si no, la crea), >> $CENSO_FILE, git commit -m "[ADQ] <fecha>", git push, git checkout main; se llama en todos los exit 1 (líneas 41, 185, 196, 202 — con invocado=no y su motivo) y tras la línea 212 con el CODIGO_SALIDA real. El [ADQ-PDN] igual, con su propio commit. Ningún otro cambio de lógica.
Cascada que a #558 le faltó: ADR derivado por el comando de la casa (grep -oE '^\*\*ADR-[0-9]+' … | tail -1, contiguo, contra main + ramas vivas); fila en forense/firmas-pendientes.tsv (RECIBO, no requiere firma) además del .md; registro-rotulos; recifrado L0; tests/check.py --baseline VERDE o PARO-reporta.
crontab: pega crontab -l antes; si la línea no trae PATH= explícito, añade la de REGISTRO-CRON-v1_0.md §2 (sólo PATH y ruta absoluta del log — el horario 30 7 * * 1-5 no se toca); pega crontab -l después. Es la lectura (c) del diagnóstico, que quedó sin probar por falta de disparo automático.
P1 · Prueba de extremo a extremo, dos veces

(a) Corrida manual completa: cd /home/pc0/mm-adq && ./tools/adquiere_cron.sh. Éxito = rama censo/2026-09-06 (o -cron-HHMM) con tres commits visibles: [CENSO], [ADQ-PDN] … fuera de ventana, [ADQ] … invocado=si exit=<c> … — o invocado=no motivo=<PARO-…> si la caja paró, que también es éxito de la huella. Pega git log --oneline origin/censo/2026-09-06* -5 y el archivo del censo completo. (b) Corrida forzando un PARO (por ejemplo data/raices.local.yaml renombrado 30 s): éxito = línea [ADQ] … invocado=no motivo=PARO-RAIZ … commits_nuevos=0 commiteada. Restaura y verifica git status limpio. Lo que este acto no puede probar y lo dice: el disparo automático. Primera evidencia: censo/2026-09-07 con tres commits, lunes 07:35. T31 lo vigila desde el martes.

PERÍMETRO Y CONCURRENCIA

Toca: tools/adquiere_cron.sh · forense/cron/REGISTRO-CRON-v1_0.md (§1 trabajo 3: formato de huella; §3 calendario: «tres commits por día») · forense/firmas-pendientes.tsv · canon (sólo ADR + cabecera) · registro-rotulos · forense/notas/2026-09-06-MAESTRA38-CRON-3-{spec,resultados}.md · hallazgos · A.3 · cascada. Hereda de #558 sin re-editar: check.py, test_t_cron.py, INFRAESTRUCTURA, acto.md. NO toca: manifiesto · cola · milpa/** · nada de A6/L2/ENSANUT. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo. Concurrencia: solo en mm-adq mientras corre (usa el clon del cron). A6, L2 y ENSANUT pueden seguir en sus worktrees; no comparten archivos con este acto salvo la cascada.

Lo que NO hace

No cambia el horario ni la ventana del cron. No decide si [ADQ]/claude -p se retira (D-b (3): se decide en dos semanas con la huella a la vista). No mide nada.

## CONSUMIDO

Ejecutado por la sesión Sonnet que corrió `/acto` en `mm-adq`, 6/sep/2026. `PR #560` (censo/2026-09-06, tres commits) sobre la corrida real; el resto del código/cascada de este acto en la rama `acto/maestra38-cron-3` (PR abierto tras este commit).

Premisas del encargo que NO se sostuvieron contra el árbol, declaradas en `forense/notas/2026-09-06-MAESTRA38-CRON-3-spec.md` y en `ADR-354`: (1) dirección fusionó `PR #558` por error antes de lanzar el acto -- se tomó como base en vez de sustituirlo con un PR nuevo. (2) `PARO-RAIZ` no detiene el script antes de `claude -p` -- P1(b) se corrió forzando `PARO-CORPUS` en su lugar. (3) La concurrencia declarada ("A6 ... en sus worktrees; no comparten archivos") no se sostuvo: una adenda de dirección a mitad de sesión confirmó que `MAESTRA38-A6` corre en este mismo clon `mm-adq`, con `data/manifiesto-staging.yaml` modificado sin commitear durante toda la sesión -- nunca tocado por este acto. (4) Colisión de numeración con `PR #561`/`MAESTRA38-A6`: ambos derivaron `ADR-353`/`FP-324` de forma independiente contra el mismo `main`; `#561` fusionó primero (`957a3080`), así que este acto renumeró a `ADR-354`/`FP-325` al sincronizar (`ADR-354`).

Resultado: los dos defectos de código de `PR #558` corregidos y probados dos veces en la caja real (no en sesión de nube); crontab instalado con `PATH=` explícito y verificado; disparo automático sigue sin poder probarse (primera evidencia posible: `censo/2026-09-07`, lunes).
