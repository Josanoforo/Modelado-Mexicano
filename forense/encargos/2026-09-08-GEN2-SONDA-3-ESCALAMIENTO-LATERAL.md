# ENCARGO · ACTO GEN2-SONDA-3 · ESCALAMIENTO-LATERAL — propuesta de Astra (ChatGPT), validada por dirección, adaptada al circuito

**SHA de redacción:** `9bd1a439` (fusión de PR #640, `GEN2-T35-DISEÑO`) — `origin/main` al momento de redactar. Al arrancar este acto `origin/main` había avanzado a `351fd25` (merge de PR #639, `GEN2-UNIVERSO-C`, cascada no relacionada: `data/manifiesto.yaml`, `cola-adquisicion`, ADR-417); `9bd1a439` sigue siendo ancestro directo de ese `HEAD` — sin divergencia, sin merge necesario.
**Entorno asignado:** NUBE — este acto no toca microdato ni red a fuentes.
**Estado:** VIVO

## Bloque VERIFICACIÓN DE EXISTENCIA (A.8, Parte 2)

Comprobado contra `9bd1a439` y contra `origin/main` vigente (`351fd25`) al arrancar:

- `.claude/commands/sonda.md`, `.claude/commands/adquiere.md`, `.claude/commands/mapea.md`, `AGENTS.md` → existen (`ls`).
- `#632`/`#635`/`#637` fusionados: verificado con `git log --merges --oneline origin/main` (`51fec05` PR #635, `2f86da6` PR #637; #632 fichado hacia atrás por #637 per `forense/encargos/2026-09-08-GEN2-SONDA-2-RETRO.md`).
- «Deep Research»: `grep -rc "Deep Research" forense/notas/2026-09-08-GEN2-SONDA-CAJA-1.md` → `0`. No adjuntados en el lanzamiento de este acto → procedencia tipo (3), se ejecuta P4 con la lista de supuestos §8 autocontenida, sin buscar fuera ni reconstruir de memoria.
- Cobertura retroactiva: `forense/notas/2026-09-08-GEN2-SONDA-CAJA-1.md` (524 líneas) leída completa para P1 — nota de ampliación y cierre de SONDA-CAJA-1, no solo la descripción inicial de #635.

## Objetivo

Ejecutar, verbatim en su contenido sustantivo, la propuesta de escalamiento lateral de Astra (ChatGPT) que dirección validó el 8/sep/2026 («revisa la propuesta de Chatgpt Astra»), adaptada al circuito de este repositorio (0-bis, cascada, `cierre_acto.py`). Principio rector, conservado y gobernante: «rigor suficiente para avanzar; auditoría solo cuando cambia el resultado.»

## Piezas

**P0 · Fichar al entrar (A.3).** Este mismo 0-bis, antes de cualquier edición sustantiva — rompe el patrón de los dos actos previos del linaje (#632, #635), que corrieron sin fichar primero.

**P1 · Antecedentes.** Leídos: `.claude/commands/sonda.md`, `.claude/commands/adquiere.md`, `forense/notas/2026-09-08-GEN2-SONDA-CAJA-1.md` completa. Deep Research: ninguno adjuntado — no se buscan fuera del repo. Terreno confirmado, sin discrepancias que exijan PARO.

**P2 · `/sonda` gana criterio.** `.claude/commands/sonda.md` se amplía con: selección de vías por pertinencia (objeto/examinado/condición-faltante/mejor-expectativa — estrategia ≠ vía de recuperación; dos buscadores no prueban dos vías; mirrors pueden ser una sola copia); repertorio activado por evidencia y no por checklist (objeto exacto, consumidores y código, republicadores, frontend/SPA con la nota «un grep sin coincidencias no cierra esta vía», archivos históricos acotados, plataforma por señales reales, documentación y handoff humano); disciplina de nota en tres renglones (Observado / Interpretación / Consecuencia) con los seis ejemplos (NXDOMAIN, 403, directorio bloqueado, 200, fallo-de-entorno, fecha de captura); segunda pasada crítica antes de todo negativo material (cinco preguntas, breve, mismo ejecutor, sin cuotas universales — «tres clases»/«dos archivos web» quedan prohibidas explícitamente como cuota); formato del negativo material (alcance · vías examinadas · vías pendientes con motivo · razón de parada · próxima acción; un paro por presupuesto declara el límite, no presenta el universo como agotado). Los límites de acceso vigentes se conservan verbatim: la inspección de código no autoriza evadir autenticación, CAPTCHA, WAF ni control alguno.

**P3 · `/adquiere` gana dos matices.** `SONDA-LATERAL-RECOMENDADA` como recomendación en nota, no estado nuevo ni recursión automática. Al recibir una vía de `/sonda`: identidad contra corpus considerando que un mirror cambia hostname; distingue misma-fuente-otra-ruta / edición nueva / extracto / fuente distinta; escritor canónico vs. vista regenerada. Completitud técnica proporcional en exportaciones/API (paginación, total declarado, señales de truncamiento); si no se confirma, cobertura parcial o desconocida — verbatim: «dos descargas idénticas no demuestran que se descargaron todas las filas». Completar `/adquiere` cierra la caminata, no agota la fuente.

**P4 · Depuración de los Deep Research.** Los seis supuestos que NO se incorporan quedan en `.claude/commands/sonda.md` como sección de advertencias: SODA3/SODA2.1, 403≠ASN, SHA256 vs CDX digest, DuckDB remoto, source maps, tabulados≠microdatos — con la línea de cierre: los estudios son repertorio, las capacidades se confirman al usarse.

**P5 · Validación y encargo sucesor.** El piloto (modos CONSTRUCTO/HERMANAS/LATERAL) es sucesor GATEADO a este PR fusionado, no pieza de este acto. Este acto revisa el diff de P2/P3/P4, corre `tests/check.py --baseline` (fallos heredados se comparan contra base, no se limpian), cero tests de frases/formatos, y deja escrito en `forense/encargos/cola/` el encargo del piloto CAJA con: selección del negativo material por derivación (comando sobre la cola vigente filtrando `NO-ENCONTRADO`/`OBTENIDO-PARCIAL` con faltante material/`NO-OBTENIDO-POR-ESTE-AGENTE`, cruzado contra consumidores vigentes), excluyendo re-descargar el RUPC histórico por demostración, presupuesto explícito, y los tres finales válidos: dato recuperado, ruta verificada, o negativo mejor acotado — nunca una adquisición fabricada.

**P6 · Devolución.** Nota de cierre con: ruta del 0-bis; encargo del piloto y su compuerta; perímetro efectivo y diferencias contra la propuesta original (Deep Research a procedencia (3), piloto a sucesor, fichaje P0); estado real en una palabra.

## Perímetro

`.claude/commands/sonda.md` · `.claude/commands/adquiere.md` · `forense/encargos/` (este 0-bis + el encargo sucesor del piloto en `cola/`) · `forense/hallazgos.md` (una línea) · `forense/no-corrido.tsv` · nota de cierre · cascada estándar. Prohibido verbatim: cron, cola nueva, manifiesto, downloader, catálogo general, skill por técnica, esquema nuevo de estados, helpers fuera de esta lista.

## COMPUERTA

**COMPUERTA: ninguna.**

## Gate D-14 (contestado)

Defecto real ya ocurrido: #635, dos negativos prematuros corregidos (RUPC recuperado vía republicador tras 4 rutas oficiales fallidas; JS de Bienestar re-leído). Material: un negativo prematuro escribe una clasificación A.4 falsa que mesa consume. Costo: edición de dos documentos de comando, cero mecanismos nuevos. Pasa con holgura.

## FIRMA DE MESA

Verbatim, 8/sep/2026: «revisa la propuesta de Chatgpt Astra» — validada por dirección; el lanzamiento de este acto la convierte en orden.
