# ENCARGO · COND-ATRIB — los β̂ marginales pagan su deuda de condicionamiento (A-bis 1-4, B-bis)

**SHA de redacción:** `68a3466` (`PR #257`, `origin/main`) · Entorno asignado: UBUNTU, worktree con corpus (`data/raw` montada). NO nube — abre microdato.
**Estado:** CONSUMIDO — ACTO COND-ATRIB, `PR #263` (rama `cond-atrib`, worktree `/home/pc0/Modelado-Mexicano-barrido2`), 18/ago/2026. Commits 1-4 (especificación congelada, corrida, cierre, cascada) más un commit de fusión (`origin/main` avanzó a `PR #261`/`PR #262` durante la ejecución, `ADR-104` provisional se renumeró a `ADR-105` por colisión real con `ACTO NOTAS-P3`).
**Gate:** lanzado tras la fusión de `gate-durable-v7` (`PR #260`), confirmado vía `gh api .../pulls/260` (`merged: true`) antes de arrancar, no vía estado de worktree.

> Archivado bajo A.3 por la sesión que lo ejecutó. Texto verbatim; lo único añadido es esta cabecera y la marca de estado.

---

## Texto verbatim del encargo

ENCARGO · COND-ATRIB — los β̂ marginales pagan su deuda de condicionamiento (A-bis 1-4, B-bis)

SHA de redacción: 68a3466 (#257, origin/main) · Entorno: UBUNTU, worktree con corpus (data_raw montada). NO nube — abre microdato. Estado: VIVO · Gate: lanzar después de que gate-durable-v7 fusione (esa caja está ocupada y este acto no debe convivir con la corrida). 🚫 Sin --freeze · red cero durante apertura de microdato (unshare -Urn, doctrina del barrido).

Por qué este acto

milpa/procedencia.yaml carga entradas con clase literal "PENDIENTE — medición condicional por atributos NO CORRIDA en este acto" y β̂ rotulados "marginal (sin condicionar sobre atributos)" / "TRUNCADO". Es exactamente la deuda que A-bis (v2.4) instituyó el día que se midió por primera vez: un β̂ sin condicionamiento es una asociación (regla 1), y el 4/ago los tres estimados invirtieron el signo al estratificar. Nadie escribió el acto que corre ese condicionamiento. Este es.

════ ARRANQUE ════ 1 REPO: el worktree de la caja (post-fusión del gate); git fetch origin --prune; reporta ruta · git log -1 · git status --short. Rama nueva desde origin/main. 2 SHA: contra 68a3466+lo fusionado; re-deriva citas por contenido. 3 CORPUS: ls data/raw/ | head -3 · localiza los payloads del universo (C1) vía data/manifiesto.yaml — AUSENTE del clon NO es PARO; ausente del corpus SÍ (repórtalo como NO-ENCONTRADO con universo). 4 ENTORNO (A.2, tres partes): variable cruda · sonda INEGI (nunca -I) · corpus montado. Esperado: sin_variable · 200 · montado. 5 ESPEJO: toda cifra del worktree con comando. ════════════════

VERIFICACIÓN DE EXISTENCIA — contestada por quien escribe, contra 68a3466
la deuda, con línea:   procedencia.yaml:306-308 (grupo condicionales_escalares_confianza_generica,
                       clase "PENDIENTE — … NO CORRIDA")  +  clases "…marginal…" (≥3 entradas β̂;
                       una TRUNCADA)                                          EXISTE-NO-SATISFACE
universo declarado:    :914 "Personas 18+ de ENVIPE 2025 (TMod_Vic) que dispararon AP7_3_XX=1…"
                       · :945 "MISMO universo… n=13,023"                      EXISTE-SATISFACE
el precedente:         A-bis reglas 1-4 (instrucciones v2.4) + los 3 signos invertidos del 4/ago
encargo previo:        grep -rln "COND-ATRIB\|condicional por atributos" forense/encargos/ → re-córrelo;
                       al redactar: NO-ENCONTRADO — este es el primero

Lo primero que haces (C0): deriva tú la lista completa de entradas afectadas — grep -n "marginal\|PENDIENTE.*condicional" milpa/procedencia.yaml — con id, clase, instrumento y universo de cada una. No heredes mi "3"; el número que salga es el denominador del acto.

PERÍMETRO

milpa/procedencia.yaml (solo las clases/anotaciones de las entradas derivadas en C0 — ningún otro número) · forense/notas/ (la ficha B-bis y los resultados) · canon/gobernanza-v1_15.md (ADR) · estado-programa cascada :27/:101 (⚠️ FP-48) · hallazgos.md (append) · forense/encargos/. NO toca milpa/refutations.yaml, el modelo, el pre-registro del Hito D, ni tools/. Fuera de lista: PARA.

C1 · COMMIT A — la especificación, congelada ANTES de abrir un solo dato

Por cada entrada de C0, en una ficha B-bis propia: (1) instrumento y payload exactos (id_manifiesto + sha, verificados contra el censo/ledger del barrido); (2) universo restringido verbatim del yaml; (3) ponderador (derívalo del diccionario del instrumento — no lo supongas); (4) los ejes de condicionamiento disponibles derivados del diccionario (candidatos típicos: sexo, grupo de edad, escolaridad, tamaño de localidad — pero la lista válida es la del diccionario), con cortes/dicotomizaciones declarados; (5) la escala del estimando (diferencia de proporciones — regla 3: no se compara contra otra escala jamás); (6) qué significa cada desenlace, declarado antes (B-bis): signo estable en todas las celdas → el marginal queda corroborado como robusto dentro de este universo (y se dice así, no "identificado" — regla 2); signo discordante → el marginal no es robusto, y nada más — prohibido escribir "el verdadero β es X"; celdas sin n → se reporta la cobertura y se acota (regla 4: universo restringido no se reconcilia contra poblacional). Cierra el commit con la frase ritual: "el primer resultado que produzca este procedimiento es el que se reporta."

C2 · COMMIT B — la corrida, sin editar el A

Corre exactamente lo congelado. Reporta por celda: n, θ̂/β̂, IC, y el marginal recalculado sobre el mismo universo de las celdas (regla 4). Un punto que cruza umbral con IC que no lo despeja no adjudica — se reporta como propuesta con la reserva escrita (A-bis, contraparte). Si la especificación resultó mal, tercer commit que lo diga; nunca se corrige hacia atrás.

C3 · Cierre

Actualiza la clase de cada entrada en procedencia.yaml al resultado real — p. ej. "MEDIDO·β̂ condicionado por [ejes]; signo [estable|discordante]; universo [verbatim]" — citando la ficha. ADR (número re-derivado dos veces) · cascada · nota · hallazgos.md · encargo CONSUMIDO. Auditoría: este acto SÍ mide México — declara qué contador mueve: las entradas de C0 salen de "PENDIENTE/marginal", y si algún condicionado queda con signo estable e IC que despeja, di explícitamente si eso toca o no el contador de coeficientes en escala del modelo (hoy 0 de 15) — la respuesta esperada es NO (esto sigue siendo asociación condicionada, no identificación; el primero sigue reservado a FP-11). Escala declarada en cada cantidad (pregunta v2.4 del módulo). Ninguna cifra tecleada. NO hace: no identifica causalmente nada · no toca refutations ni tiers · no abre instrumentos fuera de los que C0 derive.
