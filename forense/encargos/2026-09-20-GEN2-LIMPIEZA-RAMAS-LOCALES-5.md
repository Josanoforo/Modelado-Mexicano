# GEN2-LIMPIEZA-RAMAS-LOCALES-5 — encargo (A.3, archivado verbatim)

Pegado por el usuario directamente en esta sesión (CAJA, pc0-0d), mientras cerraba
GEN2-LIMPIEZA-RAMAS-LOCALES-4-CIERRE-FP402, con instrucción de continuar después. 20/sep/2026.

---

ENCARGO · ACTO GEN2-LIMPIEZA-RAMAS-LOCALES-5 · ¿QUÉ ACTO QUEDÓ A MEDIAS? — CADA RAMA Y WORKTREE QUE QUEDA EN LA CAJA, CON SU VEREDICTO, Y EL CIERRE DE LO YA FIRMADO

ENTORNO: CAJA (máquina local). El hook de arranque imprime ENTORNO-DERIVADO; si no dice CAJA, PARA en una línea.

CABECERA · SHA de redacción 1dfb6726 (merge de #929); re-deriva al abrir · una sola sesión, rama propia · MODELO: Sonnet para P1 y P3; P2 exige juicio — si no lo tienes claro, clasifica NO-DETERMINABLE y explica · MODO: ABIERTO · CONTADOR: cuenta_gen2 = NO; cero contadores. Sin sub-agentes con capacidad de escribir a otras sesiones o de preguntar a mesa (incidente asentado en #929): si lanzas un fork, es de solo lectura y su salida la revisas tú antes de actuar.

1 · OBJETIVO

Mesa quiere una sola cosa: no quedar a medias. Que de cada rama y worktree que sigue en la caja se sepa si su trabajo (a) ya está en main, (b) está vivo y en curso, o (c) se quedó a medias — y en ese caso, qué falta para terminarlo o qué se pierde si se abandona. «Hecho» significa: una tabla con una fila por rama local y por worktree, con veredicto y evidencia; lo firmado, ejecutado; y una lista corta «A-MEDIAS» en lenguaje llano para que mesa decida terminar o abandonar, caso por caso.

2 · FIRMAS DE MESA

FP-402 (propuesta por dirección tras verificar contenido; tu lanzamiento con este archivo es el sello; sin texto, P3 no borra las seis): "Se autoriza git branch -D sobre las seis ramas de FP-402, verificando antes que cada una esté en el bundle y que sus insumos archivados estén en origin/main. Ninguna otra." Worktrees descartados (propuesta): "En codex/autoridad-semantica-marco-cobertura-total y marco-produccion-total se autoriza quitar el enlace simbólico .barrido2 (no su destino) para poder retirar el worktree sin --force."

3 · LO QUE DIRECCIÓN SABE
[LEÍDO] Nota de cierre de #929: quedan 39 ramas y 33 worktrees en Modelado-Mexicano, 7 y 2 en mm-adq. Categorías: ~14 «actos vivos con worktree, incluidos actos previos aún no cerrados» · 12 codex/* < 24 h · 6 rechazadas por -d (FP-402) · acto/gen2-celda-d-piloto-2 y claude/tramite-2026-09-17 huérfanas · 4 worktrees sucios (2 archivados, 2 descartados sin acción) · 3 worktree-agent-* · main local. La nota no nombra los ~14. Ése es el hueco que este acto llena.
[EJECUTADO] Las seis de FP-402, contenido cruzado contra origin/main = 1dfb6726: los dos ids de manifiesto que añadían las ramas adq/* (ihsn_mex_2009_ennvih3_metadata, enpol2016_bd_csv_zip) están en main; los tres investigacion-estado/*.json están en main con fecha posterior; el RECIBO-3 de Codex fue sustituido por #872; el diff del 03 está archivado con hash verificado. Único faltante: forense/censo-raiz/2026-09-16.txt no está en main (sí 15, 17 y 18); vive en el parche archivado de censo/2026-09-16.
[EJECUTADO] En origin hoy: acto/gen2-din-credito-comparabilidad-texto-1 (PR #932), claude/clever-dirac-9nb7d8 (GEN2-SENAL-1, en curso), claude/new-session-lvyz4s (#930) y claude/trusting-allen-0y61rq — estas dos últimas son el mismo encargo GEN2-NUBE-PILOTO-1 corrido dos veces; mesa decide cuál fusiona. No las toques.
[SUPUESTO] que las 12 codex/* y las 3 que eran EN-VUELO ya cumplieron 24 h. Si alguna no: se queda y lo dices. (En #929 este mismo supuesto resultó falso.)
[SUPUESTO] que entre los ~14 hay actos cuyo PR fusionó y solo les falta borrar la rama. Si en cambio hay actos sin PR, o con PR cerrado sin fusionar, ésos son los que importan.

4 · YA HECHO / YA DECIDIDO

LIMPIEZA-1 a 4 (#910, #913, #923, #929): inventario, clasificación por contenido contra la historia de main, bundles verificados, 116 + 15 ramas borradas. Decisiones de mesa sobre los 4 worktrees sucios: tomadas en #929. No repitas esa clasificación para lo ya cerrado: parte de su estado final. Verifica que los dos bundles de /home/pc0/ sigan íntegros (git bundle verify + sha256) antes de cualquier borrado.

5 · PIEZAS

P1 · Inventario final, una fila por rama local y una por worktree (los dos clones). Por cada una: último commit (fecha, asunto) · ¿existe en origin? · PR asociado y su estado (gh pr list --head <rama> --state all, o el rastro ## CONSUMIDO en su encargo archivado) · commits sin equivalente en main (git cherry) · rutas exclusivas contra la historia de main · ¿trae data/corrida0/CALC-* con sello que main no tiene? · NC abiertas que nombran ese acto · worktree sucio sí/no. P2 · Veredicto por fila (token en el campo):

EN-CURSO — presente en origin o con commit < 24 h. No se toca.
CERRADO-FALTA-BORRAR — PR fusionado, contenido en main. Se borra en P3.
A-MEDIAS — tiene trabajo propio que no está en main y no está en curso. Para cada una, en tres líneas llanas: qué quería hacer el acto · hasta dónde llegó · qué falta o qué se pierde. Lee su encargo archivado y su ## NO-CORRIDO. No lo termines tú.
SUSTITUIDO — otro acto hizo ese trabajo; di cuál, con PR.
INFRAESTRUCTURA — worktree-agent-*, worktrees de la rutina en /tmp, main local. Se listan, no se tocan.
NO-DETERMINABLE — con por qué. P3 · Ejecutar lo firmado y lo mecánico. git branch -d (minúscula) sobre las CERRADO-FALTA-BORRAR y las codex/* que ya cumplieron 24 h; worktree retirado sin --force tras comprobar que data/raw ahí es symlink o no existe. Las dos huérfanas del clon base (acto/gen2-celda-d-piloto-2, claude/tramite-2026-09-17): -d desde main, que ya es el HEAD del clon. Las seis de FP-402 y los dos .barrido2: solo si la firma viene en el lanzamiento. Si -d rechaza una rama que P2 marcó cerrada: no fuerces; pasa a la lista de mesa con el mensaje crudo. P4 · El día que falta. Restaura forense/censo-raiz/2026-09-16.txt desde el parche archivado, tal cual, con una línea en la nota que diga de dónde salió. Es una bitácora diaria; un hueco de un día sin explicación es peor que un archivo recuperado con procedencia. P5 · Para mesa, al frente de la nota: la lista A-MEDIAS, ordenada por lo que se pierde si se abandona — mediciones primero. Por cada una, dos opciones y tu recomendación: terminar (¿qué encargo haría falta, de qué mesa?) o abandonar (NC de cierre con la razón, diff archivado). Si la lista sale vacía, dilo en la primera línea: es el mejor resultado posible.

6 · LATITUD

Decides tú: cómo obtener el estado de los PR; formato de la tabla; si restauras el censo por git apply parcial o copiando el bloque. Preguntas a mesa y sigues: una rama que parece A-MEDIAS pero cuyo encargo no encuentras. No decides: terminar ni abandonar un acto.

7 · PAROS (lista cerrada)

-D, --force o quitar un symlink fuera de lo firmado · borrar una rama presente en origin o con commit < 24 h · abrir un resto que por nombre toque una ola reservada (encig25*, enif2024*, envipe2025*, envipe2026*, eder2025*) · git clean · stash drop · push --delete · bundles no íntegros. No es paro: clon otra vez superficial (desprofundiza, y reporta qué comando lo causó).

8 · COMPUERTAS

«Bundles íntegros» protege: borrar. Ninguna otra.

9 · PERÍMETRO

En disco: P3 sobre lo firmado y lo mecánico. En el repo: nota, tabla TSV, forense/censo-raiz/2026-09-16.txt, hallazgos.md, NC/FP, cascada. Ajeno: todo worktree EN-CURSO · los worktree-agent-* · la rutina de adquisición · origin salvo el PR propio.

10 · NO HACE · SUCESORES · CIERRE

No termina actos a medias · no rescata mediciones · no decide entre los dos PR del piloto de nube. Sucesores: un encargo por cada A-MEDIAS que mesa decida terminar, redactado por la mesa de tema dueña de ese perímetro. Al cerrar: suite, y después git rev-parse --is-shallow-repository. Estado final crudo de ramas y worktrees por clon. Cascada · ## NO-CORRIDO / RESERVAS · ## CONSUMIDO.

## NO-CORRIDO / RESERVAS

- `NC-0429`: terminar o abandonar `acto/gen2-f5-recaptura-l` (A-MEDIAS) — razón `DECISION-DE-MESA-PENDIENTE`. Sucesor: `FP-403`.
- `NC-0430`: `git branch -D`/limpieza de residuo en 5 worktrees bloqueados (`acto/gen2-reparacion-cierre-consolidacion-cron`, `codex/autoridad-semantica-enif`, `codex/gen2-encuci2020-respuesta-por-contacto-cli-2`, `codex/gen2-issp2017-consistencia-apoyo-familiar-cli-2`, `llave2-decreto`) — razón `DECISION-DE-MESA-PENDIENTE` (ninguno de los residuos está firmado para descartar). Sucesor: nota de cierre, tabla completa.

## CONSUMIDO

`PR` (a abrir por esta sesión) — ver `forense/notas/2026-09-20-GEN2-LIMPIEZA-RAMAS-LOCALES-5-cierre.md`.
