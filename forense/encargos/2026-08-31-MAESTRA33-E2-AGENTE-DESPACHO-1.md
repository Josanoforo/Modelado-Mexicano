ENCARGO · MAESTRA33-E2 · AGENTE-DESPACHO-1 — invoca /acto
SHA de redacción: af41796 (merge PR #410 / ADR-238). ENTORNO: NUBE (Claude Code) — NO UBUNTU, NO doble. COMPUERTA: el PR de MAESTRA33-E1 (rama claude/agente-tramite-d13-k01d40) fusionado en origin/main; si no está, la skill se niega con cero commits. MODELO SUGERIDO: Opus, ultrathink.
FIRMA DE MESA (verbatim, 31/ago/2026): "Siguiente automatización" — continúa la instauración del modelo D-13/ADR-237 ordenada por mesa.

VERIFICACIÓN DE EXISTENCIA (A.8, contestada por dirección contra af41796):
· forense/encargos/cola/: NO-ENCONTRADO (ls -d → no existe). Convención LISTO-NUBE/EN-CURSO: NO-ENCONTRADO — grep -rln "LISTO-NUBE|despacha|DESPACHO" .claude/ forense/encargos/ canon/gobernanza-v1_15.md → 2 archivos, ambos usan la palabra como doctrina, ninguno la implementa. Universo: árbol completo salvo .git y data/raw, 31/ago/2026.
· .claude/commands/acto.md: EXISTE-NO-SATISFACE — ejecuta UN encargo que le entregan; no elige de una cola ni corre recurrente.
· Agente de trámite (E1, en vuelo): EXISTE-NO-SATISFACE — papeleo y digesto, no ejecución de encargos.

PIEZAS (COMMIT-1 congela las specs; "el primer resultado que produzca este procedimiento es el que se reporta"):
P1 · Convención de cola: forense/encargos/cola/ con una línea ESTADO en cabecera: LISTO-NUBE → EN-CURSO (fecha+sesión) → CONSUMIDO (A.3, con su PR) o PARO-REPORTADO (con la razón verbatim). Regla dura, escrita en el runbook: a la cola SOLO se entra por PR fusionado a main — el merge de mesa es la autorización; el agente jamás ejecuta nada que no esté en main.
P2 · .claude/commands/despacha.md — skill del agente: tick = arranque ligero (clon, SHA); CANDADO: si existe un EN-CURSO en la cola o una rama remota de acto abierta, reporta y termina sin tocar nada (una sesión nube a la vez, mecánico); si no, toma el LISTO-NUBE más antiguo con ENTORNO: NUBE, lo marca EN-CURSO en un commit propio, y lo ejecuta con /acto verbatim. Nunca edita el contenido de un encargo; premisa que no se sostiene = PARO-REPORTADO, que es entregable, y no reintenta solo. Encargos ENTORNO: CAJA los lista como "esperando caja" y no los toca. CONTADOR del tick: el que muevan los encargos que ejecuta; el despacho en sí, cero.
P3 · forense/agente-despacho-v1_0.md — runbook: prompt exacto (≤5 líneas) para la segunda tarea recurrente de mesa (sugerida: 2 veces por día hábil, desfasada de la de trámite), qué esperar, y falsador a 1 mes: si ejecuta algo fuera de cola/main, o dos sesiones nube llegan a coincidir por su causa, se apaga la tarea y se anota — mismo criterio que D-10..D-13.
P4 · Commitea el PRIMER elemento de la cola con ESTADO: LISTO-NUBE: el ANEXO B″ de abajo, verbatim, como forense/encargos/cola/2026-08-31-MAESTRA33-B2-MARCO-M-SORTEA-v1_1.md.

PERÍMETRO Y CONCURRENCIA: este acto toca .claude/commands/despacha.md, forense/encargos/cola/ (nueva), forense/agente-despacho-v1_0.md, la fila de recibo en firmas-pendientes.tsv, el archivo A.3 propio y la cascada de cierre. E1 (trámite) toca tablero y digesto: renumera quien fusiona segundo. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR candidatos: siguientes libres tras lo que E1 consuma — deriva del árbol al cerrar, no heredes. CONTADOR: cero mediciones, declarado (infraestructura).
LO QUE NO HACE: no crea ni redacta encargos (eso es dirección); no ejecuta CAJA; no firma; no corre dos actos a la vez; no reintenta PAROs; no toca canon/ salvo cascada.
SUCESORES: LOTE-CAJA (FP-204 corresidencia + piezas R — lo redacta dirección y corre en TU máquina) · AGENTE-ADQUISICION-1 (caja, tercera automatización).

──── ANEXO · B″ (primer elemento de la cola; ejecutará el despachador, no este acto) ────
ENCARGO · MAESTRA33-B2 · MARCO-M-SORTEA-v1_1 — invoca /acto · ESTADO: LISTO-NUBE
SHA de redacción: af41796. ENTORNO: NUBE — NO UBUNTU. MODELO SUGERIDO: Sonnet (receta congelada, cero juicio). COMPUERTA: marco-M-congelado-v1_1.tsv y CONGELADO-M-v1_1.sha256 en main (verificados por dirección; re-verifica hash antes de sortear).
A.8: sorteo v1_0 EXISTE (sorteo-marco-M-resultados-v1_0.md); resultados v1_1 NO-ENCONTRADO (ls forense/prereg-duelo-v2/, 31/ago/2026).
COMMIT-1 (congela antes de correr): semilla = semilla_desde_sha_merge("af41796f50baad1737987b7e9a1e737c38ab85f2", "MARCO-M-v1_1") — función existente en sorteo_v2.py:191, que NO se edita (cargadores propios si hace falta, precedente del reglamento ADR-178); universo = filas elegibles de marco-M-congelado-v1_1.tsv (N_elegibles esperado 22 — deriva, no heredes); regla de tamaño = ADR-231 §e leída del árbol; celdas P0-calibración entran VERIFICACION-NO-PUNTUA (F-DD). Frase de sello incluida.
COMMIT-2: forense/prereg-duelo-v2/sorteo-marco-M-resultados-v1_1.md con semilla, comando, lista sorteada y clasificación P0/P1 por celda. CONTADOR: celdas sorteadas v1_1 de 0 → N. LO QUE NO HACE: no emite puntos M ni abre corridas-R/ (ciego). Si lanzas agentes que sean en sonnet. Necesito que todo quede cableado no quiero espacios donde después me digan que faltó unir tal o cual parte del proceso.
