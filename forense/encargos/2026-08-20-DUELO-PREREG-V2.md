**SHA de redacción:** `origin/main` al arrancar esta sesión (worktree ya checked out sobre `claude/duelo-prereg-v2-reconciliacion-2arcw9`); re-derivable con `git rev-parse origin/main` — no re-verificado contra un valor previo porque este encargo no lo declaró por separado (llegó como instrucción directa de sesión, no como adjunto de mesa).
**Entorno asignado:** NUBE (repo-only). NO Ubuntu — textual en la cabecera de la instrucción. Sin research vivo fuera del repo.
**Estado:** `CONSUMIDO` por este mismo acto, `ACTO DUELO-PREREG-V2`, 20/ago/2026.
**Gate de arranque:** `T-SELLO` y `ACT-PIL-2` fusionados — confirmado (ambos encargos consumidos en `forense/encargos/`).
**Bloque VERIFICACIÓN DE EXISTENCIA:** contestado aquí por quien ejecuta. `forense/TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md` → existe, 58 líneas, leído completo. `forense/marco-candidatas-piloto-v1_0.tsv` → existe, 61 filas de datos + cabecera, leído completo, no editado. `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` → existe, §B M5 y §C D-ii localizados y citados verbatim. `FP-70` → localizada en `forense/hallazgos.md` (entrada 2026-08-19) y `forense/notas/2026-08-19-lote-ubuntu-adq-1-cierre.md`, leída, no editada. `forense/prereg-duelo-v2/` → no existía, creado por este acto.
**Nota de archivo, no del original:** este documento llegó a la sesión como instrucción de tarea directa (sin adjuntos de mesa aparte del propio texto de la instrucción). El texto que sigue es una transcripción fiel del encargo recibido, condensada en su estructura (ARRANQUE/entregables/perímetro/prohibiciones) para archivo, sin alterar ningún requisito sustantivo.

---

## Encargo · `DUELO-PREREG-V2` — nube, Opus, gate: `T-SELLO` y `ACT-PIL-2` fusionados

**Contexto:** proyecto de auditoría forense/metodológica con actos numerados en secuencia, artefactos previos en `forense/*.md`/`forense/*.tsv`, compuertas ("gates") que exigen pausar y subir a mesa ante ambigüedad, prohibiciones explícitas sobre archivos/directorios.

**Paso 0 — lectura obligatoria:** `TRANSFER-MAESTRA-FASE-CALCULO-2026-08-19.md` §5 · `marco-candidatas-piloto-v1_0.tsv` (leer, NO reconstruir, NO re-enumerar candidatas) · `CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §B M5 (tabla verbatim a sellar como T1) y nota `D-ii` · `D-iv` (EE reales para T4) · `FP-70` (ABIERTA, leer como fuente de EE, NUNCA escribir/tocar) · revisar si existe `forense/prereg-duelo-v2/` (crear si no) · revisar tablero/gobernanza/hallazgos/encargos para el patrón de cierre de actos previos.

**Entregables:**
- **T1.** Tabla `ADV1-M5` sellada — copia VERBATIM de §B M5, citando `D-ii`, en `forense/escala-cinco-casillas-piloto-v1_0.md`. Nombre estable `ADV1-M5`, nunca solo "M5". **COMPUERTA B-bis:** si el texto no especifica claramente (a) qué significa que "el falsador no refute" y (b) la precedencia entre las cinco casillas, PARAR de sellar T1, documentar opciones abiertas en `forense/prereg-duelo-v2/mesa-pendientes.md`, no decidir la ambigüedad.
- **T2.** Script de tubería L (`ADV1-M2`) en `forense/prereg-duelo-v2/`: sin humano en el bucle; modelo+versión+fecha+temperatura como parámetros explícitos; k=5-10 corridas sin descarte con dispersión; dos variantes `L-solo`/`L+corpus`; hashes de los cuatro corredores (L, M, B, E) antes de que exista R. NO se ejecuta, solo se escribe.
- **T3.** Script de scoring (`ADV1-M3`) en `forense/prereg-duelo-v2/`: skill = 1 - error/error(B); CRPS/interval-score y Brier contra R como distribución, nunca contra un punto; `INDECIDIBLE` con sus dos condiciones exactas; calibración al 80% independiente; `M3-bis` distribucional.
- **T4.** Deriva banda TOST y margen material a partir de los EE REALES citados en `D-iv`, sin calcular ningún estimado puntual sobre México, en `forense/prereg-duelo-v2/banda-tost-margen-v1_0.md`, marcado PROPUESTA PARA MESA (no auto-firmado). Enumerar las cinco vías de `NO-ENCONTRADO` del artefacto oficial de EE. `FP-70` como fuente, sin tocarla. Evitar "EE de diseño" teóricos.
- **T5.** Corredores B y E como specs ejecutables en `forense/prereg-duelo-v2/`: B = tasa base de última ola pública o persistencia; E = combinación mecánica `L⊕M` pre-registrada (si `⊕` no está definido en el corpus, proponer la combinación más simple y documentar la ambigüedad para mesa). No ejecutados.
- **Contador:** el marcador de medición sobre México queda en 0 — pre-registro por diseño. Añadir/dejar lista la fila del Δ de este acto en el tablero existente, valor 0, sin llenar más.

**Perímetro estricto:** `forense/escala-cinco-casillas-piloto-v1_0.md` (nuevo) · `forense/prereg-duelo-v2/` (nuevo, scripts y fichas) · el archivo de tablero existente (solo agregar la fila del Δ) · archivo(s) de gobernanza/nota/hallazgos/encargo para registrar el cierre del acto.

**Prohibido:** escribir en `milpa/` · calcular ningún estimado puntual sobre México · editar `forense/marco-candidatas-piloto-v1_0.tsv` · escribir/editar `FP-70` · correr los scripts de T2/T3/T5 · usar `--freeze` en git · research vivo fuera del repo.

**Cierre:** commit descriptivo en español, push a `claude/duelo-prereg-v2-reconciliacion-2arcw9`, sin PR salvo pedido explícito.

---

**Resolución (registrada por el ejecutor al cerrar):** COMPUERTA B-bis se activó en T1 — `ADV1-M5` queda copiada verbatim pero NO sellada; las dos ambigüedades (más una tercera, la definición de `⊕` en T5) están documentadas sin resolver en `forense/prereg-duelo-v2/mesa-pendientes.md`. T2-T5 y el contador se completaron según la spec. Ver `forense/notas/2026-08-20-duelo-prereg-v2-cierre.md` para el detalle de cierre completo.
