# Adenda · REPARA-PROPAGA-15 — extensión de perímetro autorizada tras el PARA

Emitida por dirección, 24/ago/2026, tras verificar el reporte del PARA contra `origin/main = fb02421` y la rama `claude/readme-modelo-decision-sync-jmb8sn = 4f5603b`.

**Autoriza.** Exactamente lo que el PARA pidió: tocar `canon/estado-programa-v1_10.md`, que el encargo original omitió. Nada más se añade al perímetro.

**Contexto verificado por dirección.** El defecto que el encargo mandaba reparar lo había cerrado ya el commit `f585f6f` («Solve CI: propagate Hito D 14→15…») dentro del propio PR de `SELLA-AGO24`, posterior a la nota de corroboración y anterior a la fusión. Dirección derivó la premisa del encargo de esa nota — narración fechada — y no de `grep` sobre los archivos: defecto de dirección, clase `§7-1` del transfer / `A.8(2)`. El cierre por no-existencia de `ACTO REPARA-PROPAGA-15` es correcto y se queda.

**Ejecutado.**
- `canon/estado-programa-v1_10.md` recifrado 146→147 en la cabecera de tabla (`:27`) y en `L0` (`:103`), párrafo de recifrado citando `ACTO REPARA-PROPAGA-15`/`ADR-147`, «cerrado por no-existencia; recifrado autorizado por adenda de dirección tras PARA». Dos citas inline adicionales de `146 ADR` (en la propia narración fechada del recifrado 146→147 de `ACTO EMISOR-M-2`, líneas `:207` y `:299`) marcadas `{cita-historica}` — son historia, no se editan.
- `python3 tests/check.py --baseline`: **19 FAIL · 147 WARN**, `LÍNEA BASE: VERDE`.
- `ADR-147` recibe dos cláusulas nuevas, `(c)` y `(d)`, sin editar `(a)`/`(b)` ya escritas — la numeración de la adenda («(b)»/«(c)») se desplazó a `(c)`/`(d)` porque `(b)` ya existía con otro contenido.
- Una línea más en `forense/hallazgos.md`: el defecto de premisa de dirección y esta adenda como cierre.
- Esta adenda commiteada junto al encargo ya consumido.

**Cascada al fusionar.** Re-derivar el máximo de ADR sobre el árbol fusionado; si otro acto tomó `147` mientras tanto, renumerar — regla de la casa.
