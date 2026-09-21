# GEN2-LIMPIEZA-RAMAS-LOCALES-6 — encargo (A.3, archivado verbatim)

Pegado por el usuario directamente en esta sesión (CAJA, pc0-0d), 21/sep/2026, mientras `#936`
(GEN2-LIMPIEZA-RAMAS-LOCALES-5) seguía abierto.

---

INPUT DE MESA · 21/sep/2026 · a la sesión de limpieza (CAJA). Acto nuevo, rama nueva:
GEN2-LIMPIEZA-RAMAS-LOCALES-6 — el último. MODO: ABIERTO. Pegarlo es el sello de las firmas.

#936 se fusiona como está. Una corrección a su P5, que asientas por enmienda (no edites la nota).

LA «A-MEDIAS» NO LO ES — verifícalo tú antes de creerme [EJECUTADO por dirección, main d5825063]:
 - `git log --first-parent --format='%h %cs %s' origin/main | grep '#669'` →
   d20039a3 2026-09-09: el PR de acto/gen2-f5-recaptura-l SÍ fusionó, y trajo
   forense/prereg-duelo-v2/corridas-L/*__v1_3.json y L-spec-v1_3.json: la medición real.
 - `grep CAPTURA-CORREDOR data/corrida0/demanda-resultados.tsv | grep -o '([0-9]* replicas)' |
   sort | uniq -c` en origin/main → 28 filas, las 28 «(16 replicas)».
 - `head -1 data/corrida0/demanda-resultados.tsv` → «# DERIVADO — NO EDITAR».
Lo que ese worktree tiene sin commitear es la regeneración local de un derivado. Se comparó
contra el HEAD de la rama (9/sep), no contra la historia de main. Y una precisión: el corredor L
son capturas de un LLM por `runner_l_cli.py`, no captura humana.
Comprueba además que los corridas-L de esas 4 celdas en el worktree sean idénticos a los de
origin/main y que no haya capturas sin seguimiento ahí. Si todo cuadra: NC-0433 cierra con esa
evidencia. Si algo NO cuadra, entonces sí hay trabajo sin guardar: PARA esa pieza y dímelo.

FIRMAS — residuos nombrados uno por uno; nada fuera de esta lista
F-1 · recaptura-l: "se descarta la modificación local de data/corrida0/demanda-resultados.tsv
(derivado regenerable) con `git checkout -- <archivo>`, tras la verificación de arriba."
F-2 · gen2-reparacion-cierre-consolidacion-cron: "se borra
data/curacion-registro/cola-adquisicion-registro.tsv.lock (0 bytes, residuo de un lock del
16/sep), tras comprobar que ningún proceso lo tiene abierto."
F-3 · encuci2020-respuesta-por-contacto-cli-2 e issp2017-consistencia-apoyo-familiar-cli-2:
"se borra el controles-medidor.json sin seguimiento, tras comprobar que las copias tienen el
mismo sha256 y que ningún CALC sellado de main lo cita como insumo."
F-4 · codex/autoridad-semantica-enif y llave2-decreto: "se borra su contenido sin seguimiento y
se descartan sus modificaciones, SOLO después de verificar archivo por archivo que el sha256
coincide con el SHA256SUMS archivado en main por #929. Archivo que no coincida: no se toca."
F-5 · codex/optimiza-verificacion-ci-prueba-compuerta: "cuando cumpla 24 h, se archiva el parche
de su único commit como insumo externo con sha256 y se borra con -D."
Después de cada una: `git worktree remove` SIN --force y `git branch -d`. Si -d rechaza una rama
cuyo PR fusionó y cuyo contenido verificaste en main, esa rama —y solo ésa— se borra con -D.

NO SE TOCAN: los tres worktree-agent-* (infraestructura de Claude Code), la rutina de
adquisición y sus worktrees en /tmp, mm-adq, y toda rama EN-CURSO.

PAROS (lista cerrada): borrar un archivo que no esté nombrado arriba · --force · git clean ·
stash drop · push --delete · abrir un resto que por nombre toque una ola reservada (encig25*,
enif2024*, envipe2025*, envipe2026*, eder2025*) · bundles no íntegros.

CIERRE DE LA LÍNEA DE LIMPIEZA. En la nota: estado final crudo por clon; la cuenta completa
270 → N; y una semilla PARA-v2.16: "trabajo sin commitear se juzga contra la historia de
origin/main, no contra el HEAD de su rama; un archivo con cabecera DERIVADO nunca es trabajo sin
guardar". Suite, y DESPUÉS `git rev-parse --is-shallow-repository`.

## NO-CORRIDO / RESERVAS

Ninguno — todas las piezas firmadas se ejecutaron o se declararon explícitamente diferidas
(F-5, `<24h`).

## CONSUMIDO

`PR` (a abrir por esta sesión) — ver `forense/notas/2026-09-21-GEN2-LIMPIEZA-RAMAS-LOCALES-6-cierre.md`.
