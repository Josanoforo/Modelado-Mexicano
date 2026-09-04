# ENCARGO · ACTO MAESTRA38-N4 · PROPAGA-Y-PAGA — invoca /acto

SHA: 0ff3d710 · COMPUERTA: ninguna · ENTORNO: NUBE · NO en CAJA · MODELO: Sonnet. CARRILES: N3 (disjunto); N5 (canon/propuesta — este acto no toca milpa/ ni canon/modelo-decision).
FIRMA — verbatim: la misma de N3 + §3 de este documento (archivado con el 0-bis).
A.8: FP-287 ABIERTA con tests existentes (ls tests/test_cola_writer.py tests/test_manifiesto_seguro.py → 2); FP-286 ABIERTA, 28 filas con informe en forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md; FP-293 con lista en forense/notas/2026-09-04-baseline-fail-absorbidos.md; grep -c "T-A3\|T-FIRMAS-2" tests/check.py → 0 (reporta); writer de cola de INFRA-1 (nombre por ls tools/curador_registro/, se declara).
SPEC (un PR, un ADR, commit por pieza):
P1 · FP-287 → EJECUTADA (#529). FP-286: 28 letras por writer, estado + nota citando fila del informe; 11 recetas → PENDIENTE-DE-MESA; PAQUETE-RECETAS-5 consolidado (11 + ICPSR + WB + PDN). FP-286 → EJECUTADA.
P2 · FP-293 pagos: T09 ×8 (añadir bloque (c) de matiz en cada cita — texto mínimo, en el report que la contiene), T05 ×5 (entradas de glosario, una por constructo, con la definición que el motor usa), T11 ×1. Aceptados: T02 (excluir forense/rescate/ del barrido de T02), T06 (nota en baseline: valores por fuente/año; el test gana etiqueta de año sólo si cabe en ≤10 líneas, si no se acepta), T08 (nota). baseline.json recifrado: 19 → 5 absorbidos declarados. FP-293 → EJECUTADA.
P3 · T-A3 y T-FIRMAS-2 en tests/check.py, cada uno con docstring citando su defecto real (#530, #518; FP-290/291). Control positivo: los dos deben FALLAR contra 0ff3d710 (N1-lite sin encargo) y pasar tras P4.
P4 · Archivar retroactivamente el encargo de N1-lite (texto verbatim del chat del 4/sep, con nota «archivado post-hoc por N4») → ## CONSUMIDO con #530. Hallazgo: tercera omisión de A.3 en 48 h.
PERÍMETRO. Toca: tablero · cola + vista · corpus/reports/*.md (sólo los 8 sitios de T09 y el de T11) · canon/glosario*.md (5 entradas) · tests/check.py (dos tests + exclusión T02) · tests/baseline.json · forense/encargos/2026-09-04-MAESTRA38-N1-lite-*.md (nuevo) · forense/notas/…PAQUETE-RECETAS-5.md · hallazgos · A.3 · cascada. NO toca: data/manifiesto.yaml · milpa/** · canon/modelo-decision* · tools/**. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR: ADR-337 · FP-297 recibo. CONTADOR: abiertas 6 → 3 (263, 282, 288) · FAIL absorbidos 19 → 5 · tests con defecto real +2 · medición: cero.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N4 · PROPAGA-Y-PAGA` (4/sep/2026, rama
`claude/maestra38-n4-encargo-1tbqqv`). `ADR-337`/`FP-297` citados aquí no
existían en el árbol al arrancar el acto (máximo real: `ADR-335`/`FP-294`)
— D-13 exige re-derivar por el comando de la casa, no heredar de prosa; el
acto tomó `ADR-336`/`FP-295` (recibo de esta pieza).

**P1 — ejecutado.** `FP-287` → EJECUTADA (ya cubierta por
`tests/test_cola_writer.py`/`tests/test_manifiesto_seguro.py`, `PR #529`).
`FP-286` → EJECUTADA: las 28 filas reciben `nota` vía
`tsv_crudo.upsert_fila(clave=fuente_canonica)` citando la sección del
informe (`forense/notas/2026-09-03-MAESTRA37-A2-revision-cola.md` §2); 4
(9, 12, 25, 27) pasan a `PENDIENTE-DE-MESA` con receta verificada,
consolidadas en `forense/notas/2026-09-04-MAESTRA38-N4-PAQUETE-RECETAS-5.md`
— **6 recetas reales, no las 11 que este encargo citaba** (de las 12
`MESA-DECIDE`, solo 6 traen receta de navegador verificable en su propio
texto; `WB`=fila 12/`ENAFIN` y `PDN`=fila 28 calzan con los rótulos de este
encargo, `ICPSR` no rindió ningún candidato).

**P2 — ejecutado.** `FP-293` → EJECUTADA: `T09`×8 y `T05`×5 pagados con
contenido real (bloque `(c)` en `corpus/reports/*.md`; 5 entradas en
`canon/glosario-v5_6.md` §16); `T11`×1 corregido (cuantificador absoluto
suavizado). `T02` corregido (`forense/rescate/` excluido del barrido
completo). `T06`/`T08` con nota de aceptación — `T06` sí ganó etiqueta de
año por cita (cupo en <10 líneas de cambio). `tests/baseline.json`
recifrado: **19 → 3 FAIL absorbidos declarados, no 5** — este encargo
asumía que P3 sumaría 2 absorbidos más; P3 no se ejecutó.

**P3/P4 — NO ejecutados.** P4 pedía archivar retroactivamente un encargo
("N1-lite", texto verbatim de un chat del 4/sep) y marcarlo
`## CONSUMIDO` con `#530`. Búsqueda exhaustiva antes de escribir nada
(`git log --all -S "N1-lite"` sobre todo blob de todo ref; `grep -rn` sobre
el árbol de trabajo completo; los 11 commits de `PR #530` revisados uno por
uno con `git show --stat`) no encuentra ese texto en ningún lugar accesible
del repositorio — `PR #530` resulta ser la restauración de
`FP-291`/`FP-292` (`ADR-335`), sin relación con N1-lite. Bajo `MAESTRA38`
solo existen `A1` y `N2`, archivados y `CIERRE`'d: ni `N1` ni `N1-lite`
arrancaron nunca en este árbol. Fabricar el archivo con contenido inventado
y marcarlo `## CONSUMIDO` habría sido un forjado — exactamente lo que A.3
existe para impedir (corolario verbatim de `convencion.md`: "un encargo que
cita un archivo inexistente está mal escrito... si el texto no está en el
repo, va pegado inline o el encargo no se lanza"; aquí no llegó pegado en
el mensaje que invocó `/acto`). P3 (`T-A3`/`T-FIRMAS-2`, docstring citando
`#530`/`#518`/`FP-290`/`FP-291`) dependía de P4 para su control positivo y
tampoco se ejecutó — además, verificado que `#530`/`#518` no corresponden a
ningún defecto real de `T02`/`T05`/`T06`/`T08`/`T09`/`T11`. Detalle
completo: `forense/hallazgos.md` (entrada del 4/sep/2026, `MAESTRA38-N4`).

**Verificación.** `python3 tests/check.py --baseline`: LÍNEA BASE VERDE (3
FAIL · 170 WARN, sin entradas nuevas frente al `baseline.json` recifrado).

**FP/ADR reales de esta pieza.** `ADR-336` (no `ADR-337`) ·
`FP-295` recibo (no `FP-297`). PR de este acto, contra `main`.
