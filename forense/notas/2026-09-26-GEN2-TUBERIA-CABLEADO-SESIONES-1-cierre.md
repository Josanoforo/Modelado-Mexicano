# Nota de cierre · ACTO GEN2-TUBERIA-CABLEADO-SESIONES-1 · ADR-260926-GEN2-TUBERIA-CABLEADO-SESIONES-1-0038-01

26/sep/2026 · entorno **NUBE** (hook: `ENTORNO-DERIVADO = NUBE`, corpus no montado, 0 archivos examinados; no abre microdato ni red de INEGI). Rama `claude/new-session-ibivey` (fijada por la plataforma). Encargo `forense/encargos/2026-09-26-GEN2-TUBERIA-CABLEADO-SESIONES-1.md`, 0-bis `003857e`. SHA de redacción `34949751` = base (`git rev-list --count HEAD..origin/main` → 0). MODO AUTÓNOMO-AMPLIO (cláusula v1.0 `3fbc487684b77b7f`).

**CONTADOR: cero mediciones; no adopta.** Contadores propios: bloqueos del hook = 3 (los tres de P7, `forense/analisis/cableado/bloqueos.tsv`), 0 escapes.

## Interrupción de permisos (declarada)
A mitad del acto, el clasificador del modo automático de Claude Code negó continuar por «auto-modificación» (el acto edita `.claude/settings.json`, `CLAUDE.md` y `AGENTS.md`). La sesión se detuvo, commiteó solo `tools/hook_lectura.py` y pidió autorización; mesa respondió en chat, verbatim: «Autorizado». Después de eso se aplicó el resto.

## Piezas (gate D-14 en cada una: defecto real · efecto · costo)
- **P1 · Hook** — `tools/hook_lectura.py`, cableado en `.claude/settings.json` como `PreToolUse` con matcher `Bash|Read`. Bloquea con salida 2: (a) `cat`/`less`/`more` o Read sin rango sobre > 200 líneas (cuenta saltos de línea en el momento, lo mismo que `wc -l`); (b) lectura completa de un derivado (los de `CLAUDE.md` más `data/curacion-universo/*.tsv` y `canon/L0/HISTORICO.md`); (c) `git log -p`/`--patch` sin `--`; (d) pytest sin `-q`. Escape: `# --permitir-lectura-completa` en el comando Bash, que se registra como ESCAPE. Read no admite bandera, así que su escape es Bash. Excepciones por ruta: `forense/encargos/*.md` y `/root/.claude/uploads/*`, porque /acto lee y archiva encargos completos. **Read sí es interceptable**, demostrado en vivo abajo; no hace falta el sucesor «-2» por ese motivo. Defecto: la regla de RENDIMIENTO-1 era solo consejo. Costo: un proceso Python por llamada a Bash o Read.
- **P2 · Espejo** — la fuente única es `canon/REGLAS-DE-LECTURA.md`. `CLAUDE.md` la importa con `@`; `AGENTS.md` la copia entre marcadores y `tests/test_cableado_sesiones.py::test_agents_espejo_de_reglas` exige igualdad byte a byte. `AGENTS.md` gana también la lectura obligatoria de la memoria, la cláusula de autonomía y la regla R(a) de Astra/Codex. Para Codex, `tools/ci_guardias.py` gana `guardia_lectura()`: marca WARN si el diff de la rama contra `origin/main` añade `cat`/`less` de un derivado; no hace fetch (D-23) y corre dentro de `--ejecuta-huerfanos`, que ya está en CI.
  - La cláusula de autonomía se cita por su id `3fbc487684b77b7f`, con el texto LEÍDO de `forense/encargos/2026-09-24-GEN2-TUBERIA-RENDIMIENTO-1.md` §6. El sha256 de ese texto renderizado no reproduce el id (da `1dae3792ac0f7321`): el id se cita, no se re-deriva.
  - **Las «cinco reglas de Astra del 23/sep»: NO-ENCONTRADO.** Universo: `rg` sobre `forense/`, `canon/` y `AGENTS.md` con «cinco reglas», «reglas de Astra» y «R(a)|R(b)». El historial de `AGENTS.md` no se puede consultar porque el clon es superficial. En su lugar se cita la regla firmada R(a) (`FP-260923-GEN2-AUDITORIA-POST-HOC-ASTRA-1-39d2-01`). Queda como NC.
- **P3 · Memoria** — `canon/MEMORIA-OPERATIVA.md` tiene 47 líneas (límite 80), con el texto de dirección de §11. Cambios de la sesión: el marcador `[T-MEM: …]` pasa a `<!-- T-MEM:INICIO/FIN -->`, y se añade una línea en §2 que apunta al índice derivado de herramientas. `tools/memoria_operativa.py` tiene tres modos: `--escribe` (paso explícito), `--verifica` (solo lee) y `--lista`.
  - **Decisiones:** la ventana de 14 días se ancla al último corte del TSV (la firma más reciente), no al reloj, para que el bloque dependa solo del TSV. Se muestran 12 de 121 filas y el resto se lista por comando. El índice completo de `tools/` con su docstring va a `forense/analisis/cableado/herramientas.tsv` (168 herramientas), porque no cabe en 80 líneas.
  - **Cableado:** paso 3.8 T-MEM en `/tramite`, con perímetro ampliado solo al bloque marcado; una línea en el ARRANQUE de `/acto`. `.claude/hooks/arranque_memoria.py` corre después de `entorno.py --arranque` (intacto) e imprime 15 líneas de la memoria más `status` con tope de 8 s: `corrida0.py status` tardó **2 min 27 s** en esta nube, así que al arranque aparece el aviso con el comando.
- **P4 · Subagentes** — la regla está en `canon/REGLAS-DE-LECTURA.md` (espejada en `AGENTS.md`), con un ejemplo de invocación de `Agent` y su equivalente en Codex.
- **P5 · Restos de RENDIMIENTO-1** (ae2a-01..03):
  - `ci_guardias --ejecuta-huerfanos` corre los huérfanos en paralelo (un hilo por núcleo) y los de pytest en un solo lote `pytest -q -n auto` si `pytest-xdist` está instalado; si el lote falla, los re-corre uno por uno para nombrar al culpable. Se añadió `pytest-xdist` a la línea de instalación del job de huérfanos en `verify.yml`, y solo a esa línea.
  - `pyproject.toml` mínimo (`package = false`) y `uv.lock` (`uv lock`: 40 paquetes, 0,67 s). Un test exige que la lista del pyproject sea igual a `requirements.txt`.
- **P6 · Caché Parquet** — DIFERIDO-A caja (NC).
- **P7 · Prueba de arranque** — detalle abajo.
- **Defectos adyacentes (≤ 10 líneas, D-21):**
  - `tests/test_claude_md_lectura.py` ahora sigue los `@import` de `CLAUDE.md` y exime este encargo, que cita `cat data/corrida0/resultados.tsv` como intento deliberado de P7 (A.3: el encargo no se edita).
  - `.gitattributes`: `bloqueos.tsv merge=union` (D-21: los actos solo añaden filas).

## Tiempos (EJECUTADO, 4 núcleos, esta nube)
- `ci_guardias.py --ejecuta-huerfanos`: **antes 9 min 38 s**, **después 6 min 29 s**. Mismos 160 ejecutados y 79 saltados.
  - Fallidos locales: antes 61, después 54. En los dos casos son sobre todo dependencias ausentes en esta nube.
  - Cambios en el conjunto de fallas: 7 tests que fallaban antes pasan después (p. ej. `test_consulta.py`, `test_escribe_relevo_motor34.py`); no se diagnosticó por qué.
  - `test_claude_md_lectura.py` falló en la corrida «después» por el cambio de `CLAUDE.md` y se corrigió arriba.
- `tests/check.py --rapido`: 5,6 s, 0 FAIL.
- Tiempos de CI leídos de los logs del PR: ver NC (-03).

## P7 · Arranque real
- **Hook en vivo en esta misma sesión.** Claude Code recargó `settings.json` sin reiniciar. Los tres intentos deliberados se bloquearon con salida 2 y quedaron en `bloqueos.tsv`:
  - `git log -p -n 1 | head -n 2` → (c)
  - `cat data/corrida0/resultados.tsv` → (b)
  - Read de `data/manifiesto.yaml` → (b)
- **Líneas que carga un arranque:**
  - Antes: `entorno --arranque` 10 + `CLAUDE.md` 27 + instrucciones 112 = **149**.
  - Después: 10 + `arranque_memoria` 18 + `CLAUDE.md` 15 + `REGLAS` 21 + `MEMORIA` 47 + instrucciones 112 = **223** (+74).
  - La apuesta: 74 líneas fijas contra la exploración de arranque que hoy redescubre el régimen. Ahorrar esos 5 000 tokens queda como SUPUESTO de dirección, no medido aquí.
- **Una sesión nueva sobre la rama no se abrió** desde aquí: ver NC (-04).

## Compuertas
- «El hook bloquea; no edita ni borra nada»: solo lee y añade filas a su registro; lo prueba `test_hook_read_y_registro`.
- «Memoria: secciones a mano intactas»: `memoria_con()` reemplaza solo el tramo entre marcadores; lo prueba `test_memoria_cabe_y_bloque_coincide`.
- «AGENTS = CLAUDE»: `test_agents_espejo_de_reglas`.

## Módulo de auditoría
No aplica: el acto no afirma nada sobre México. Movió 0 contadores de medición.
