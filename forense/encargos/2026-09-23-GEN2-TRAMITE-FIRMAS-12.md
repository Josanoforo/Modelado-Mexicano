# ENCARGO · ACTO GEN2-TRAMITE-FIRMAS-12 · Asienta las cuatro decisiones del 23/sep (tarde), archiva el informe de competencia y su brief como fuentes, y deja en el tablero de mesa la alianza académica como pendiente con dueño

> ENTORNO: **NUBE** — cero microdato. Hook imprime ENTORNO-DERIVADO; si dice CAJA, PARA.

CABECERA · SHA de redacción `7ca31cb4` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-tramite-firmas-12` (D-17) · MODELO: Sonnet · MODO: ABIERTO · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie; adendas como `<este-encargo>-ADENDA-N.md`.
CONTADOR: cero mediciones; no adopta.

## 1 · OBJETIVO
Que las decisiones que mesa tome sobre la hoja de competencia existan en el repo verbatim (A.12), que el informe de competencia y el brief que lo produjo queden archivados con sha como fuentes citables (hoy solo viven en un chat), y que la alianza académica (validador neutral) tenga fila FP con dueño y fecha en vez de vivir en un párrafo.
«Hecho»: `grep -c 'FIRMAS-12' forense/firmas-pendientes.tsv` ≥ 4 (una fila por decisión, FIRMADA con texto verbatim; la de alianza ABIERTA) · `forense/encargos/fuentes/` contiene `INFORME-COMPETENCIA-2026-09-23.md` (sha256 `acbaa795b67017c8…`) y `BRIEF-DEEP-SEARCH-competencia-Mexico-2026-09-23.md` con sus `.sha256`, verificados por comando · `MISION-ASTRA-4-ADENDA-1.md` archivada en `forense/encargos/` con sidecar · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA (propuestas por dirección; mesa las da verbatim al lanzar o las cambia; sin ellas, §7 f)
- **D1** «Se atestigua con un tercero de tiempo todo sello existente y todo COMMIT-1 futuro; la mecánica la elige el ejecutor entre las que respondan; ninguna sustituye al sello interno.» (ejecuta `GEN2-TUBERIA-SELLO-EXTERNO-1`)
- **D2** «El producto se posiciona como benchmark auditable del comportamiento del mexicano; no promete detectar cambios entre olas; declara dónde ganan los otros.» (ejecuta ASTRA-4 U1/U3 vía ADENDA-1; informe v1.3 de dirección)
- **D3** «Segunda pasada del deep search sobre los 30 proveedores PEND antes de afirmar "nadie" en público.» (ejecuta mesa fuera del repo con `BRIEF-DEEP-SEARCH-2`; el resultado se archiva por el siguiente trámite)
- **D4** «AMAI NSE como corte de clase: U1 declara variables por instrumento; U5 lo incorpora si es calculable en ≥ 2 instrumentos; no se abre frente nuevo.» (ejecuta ADENDA-1)
- **Pendiente sin firma (fila ABIERTA):** «Alianza con un laboratorio académico con acceso al laboratorio de microdatos INEGI (CIDE / ITAM) como validador neutral del benchmark.» Dueño: mesa. Vence: fecha que mesa fije.

## 3 · LO QUE DIRECCIÓN SABE
- `[LEÍDO]` Informe de competencia (174 líneas, sha `acbaa795b67017c8`): 33 filas, 30 proveedores PEND, tres propiedades sin dueño entre los revisados, tres más cercanos (YouGov Parallax, Gallup–Simile, Matria AI). `[EJECUTADO]` verificación de dirección: arXiv 2608.28615 y 2609.07305 existen y dicen lo citado; Matria AI existe (Celestial Dynamics, 85 M gemelos, INEGI, Meta SabIA) sin métrica publicada.
- `[EJECUTADO]` `ls forense/encargos/fuentes/` → 4 entradas, ninguna de competencia. `ls forense/analisis | grep -i competencia` → 0.
- ADJUNTOS (los tres viajan con este encargo; sha256 al lado): `INFORME-COMPETENCIA-2026-09-23.md` (el archivo tal cual lo entregó la herramienta, renombrado), `BRIEF-DEEP-SEARCH-competencia-Mexico-2026-09-23.md`, `MISION-ASTRA-4-ADENDA-1.md`.

## 4 · YA HECHO / YA DECIDIDO
`grep -c 'benchmark auditable\|SELLO-EXTERNO' forense/firmas-pendientes.tsv` → 0. FIRMAS-11 (#1049) asentó D1–D8 de la mañana; no las toques. **Repítelo.**

## 5 · PIEZAS
- **P1 · Cuatro filas FIRMADA + una ABIERTA**, texto verbatim de §2, con el acto ejecutor en la columna correspondiente.
- **P2 · Archivo de fuentes.** Los tres adjuntos a `forense/encargos/fuentes/` (el brief y el informe) y `forense/encargos/` (la adenda), con sidecar `.sha256` generado y comparado contra el sha del adjunto; si no coincide, PARO de la pieza y se dice.
- **P3 · Cierre de deuda menor.** La NC que FIRMAS-11 dejó por la hoja de decisiones no archivada (`NO-VERIFICABLE-AQUÍ`, adjunto ausente): si mesa adjunta también `HOJA-DE-DECISIONES-2026-09-23.md` (sha `0fc5b52b57e6b365…`), se archiva y se cierra; si no, sigue abierta y se dice.

## 6 · LATITUD
Orden libre. Pregunta a mesa (sigues): fecha de vencimiento de la fila de alianza.

## 7 · PAROS — lista cerrada
a) no aplica · b) editar una fila FIRMADA previa · c) no aplica · d) no aplica · e) CAJA · f) mesa no dio las firmas o los adjuntos no llegaron (se archiva lo que llegó y se declara el resto).

## 8 · COMPUERTAS
«Texto verbatim; sha de cada adjunto verificado antes de archivar» protege: **adoptar / congelar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/firmas-pendientes.tsv`, `forense/no-corrido.tsv` (append/estado), `forense/encargos/fuentes/*`, `forense/encargos/MISION-ASTRA-4-ADENDA-1.md` (+sidecar), nota, L0, cascada. Ajeno: todo lo demás. En vuelo: SELLO-EXTERNO-1 (no comparte archivos salvo TSV de gobierno: union).

## 10 · LO QUE NO HACE · SUCESORES
No corre el deep search 2, no escribe el informe v1.3. Sucesores: FIRMAS-13 archiva el resultado de la segunda pasada; dirección cita las fuentes archivadas en v1.3.
