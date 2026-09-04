# Encargo "§5 · Encargo M-4 · Escritorio" — ENCUP y los dos cuestionarios internacionales

**SHA de redacción:** `16d9dbdd2f32747fe779b2d486ea6092059aa6e1` (`origin/main`,
verificado por `git fetch origin main` + `git log -1 origin/main` al
abrir esta sesión; coincide con el `HEAD` local, sin divergencia).

**Entorno asignado:** nube o pc0, cualquiera. "No abre microdato, no toca
red más allá de git."

**Estado:** CONSUMIDO — `PR` de la rama
`claude/encup-international-surveys-y2144f`. Ver
`forense/notas/2026-08-05-m4bis-encup-lapop-latinobarometro-bloqueo.md`
y la entrada correspondiente de `forense/hallazgos.md` (2026-08-05):
consumido sin producir el deliverable sustantivo — bloqueado por
entorno (`cloud_default`, sin `data/raw`, sin `/home/pc0/mm-corpus`
montado) antes de abrir un solo PDF. Una sesión futura con acceso real
al corpus (`pc0` o un worktree wireado a él) debe reabrir esta tarea
desde cero; este acto no deja ningún hallazgo de contenido que heredar
para las Partes 1 y 2, solo el mapeo de qué archivos existen y dónde.

**⚠️ Colisión de etiqueta, declarada en el acto que consume este
archivo:** "ENCARGO M-4" y "ENCARGO M-5" ya designaban, en `main`, al
momento de escribir esto, contenido sellado sin relación alguna
(`ADR-63`/R1.3, `ADR-64`/`conf.06`, ambos 5/ago/2026) — y la serie venía
reusada desde el 4/ago (`M-1`→`ADR-60`, `M-2`→`ADR-61`). Este archivo
documenta un encargo *distinto*, que reutiliza la misma etiqueta
numérica. No se renombra el encargo recibido (se archiva verbatim, como
exige la convención); se deja la advertencia aquí para que un grep por
"M-4" no confunda los dos.

---

## Texto del encargo, verbatim

§5 · Encargo M-4 · Escritorio — ENCUP y los dos cuestionarios internacionales
ENTORNO ASIGNADO: nube o pc0, cualquiera. No abre microdato, no toca red más allá de git.

1 · ENCUP 2012. Base de datos y cinco cuestionarios (2001-2012) en disco, todos sin uso asignado. El cruce marca R7.4/R7.5 como NO EXISTE porque "ninguna de las 6 clases trae registro de eventos de respuesta colectiva". ENCUP capta participación en protesta a nivel individuo. Lee los cuestionarios —que son PDF, no microdato— y reporta qué reactivos de participación política y colectiva trae, con su redacción.

2 · LAPOP AmericasBarometer 2023 México y Latinobarómetro 2024. En disco están solo los cuestionarios y las fichas técnicas, no el microdato. Los dos se bajaron para "búsqueda de reactivo de deferencia jerárquica".

Verifica contra el cuestionario, sin bajar nada: ¿qué reactivos de deferencia, confianza institucional y confianza interpersonal traen? ¿Con qué escala? Si el reactivo sirve, el microdato exige registro gratuito — que mesa ya autorizó — y eso es un acto de descarga aparte, no éste.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fc -- "2026-08-05-m4bis-encup-lapop-latinobarometro.md" canon/gobernanza-v1_15.md` → 0 (sin cita en ningún ADR). Rastro fuera de gobernanza, sin nota de cierre propia: canon/citas-sha-obsoletas-purga-2026-08-10.tsv, forense/encargos/2026-08-05-m5bis-cierre-inventarios-catalogo-cruce.md, tests/check.py. Insuficiente para CONSUMIDO, insuficiente para NO-EJECUTADO — rótulo/evidencia parcial, se lista para mesa.

## CERRADO-POR-HISTORIA

Regla mecánica (b) de la resolución de mesa sobre FP-290 (2026-09-04):
sin hermano de rótulo compartido con desenlace ya sellado (regla a no
aplicó -- ver tabla en forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md,
enmienda 2026-09-04), este encargo queda cerrado por antigüedad e
inacción declarada, no por evidencia positiva de ejecución o
sustitución. Si aparece evidencia nueva, esta marca se reabre -- no es
`## CONSUMIDO`.
