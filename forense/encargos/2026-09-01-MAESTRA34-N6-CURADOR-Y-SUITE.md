ENCARGO · ACTO MAESTRA34-N6 · CURADOR-Y-SUITE — invoca /acto
SHA de redacción: 3c3ab3a (merge PR #454). Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR — firmas DT-a y DN-a dentro. Va ANTES que MAESTRA34-L3 (caja): deja la suite utilizable en caja.

ENTORNO ASIGNADO: NUBE. NO se lanza en UBUNTU (no abre payloads; toda evidencia de contenido se cita del cierre de MAESTRA34-A1, que sí los abrió). MODELO SUGERIDO: Opus (edita un test y el registro del curador con validador).
CARRILES: MAESTRA34-N4 puede correr en paralelo en nube (perímetros disjuntos: prereg-duelo-v2, milpa, acto.md vs tests/check.py, curacion-registro). L3 en caja espera a este merge.
COMPUERTA: ninguna (archivado por PR [COLA] fusionado por mesa = firma).

FIRMAS DE MESA — verbatim, 1/sep/2026: «DT - Revisa bien el repo y asegurate de que efectivamente los payloads ya los vigila el manifiesto con sha, si es así entonces A. DN-a. DS-a.» Verificación de dirección contra 3c3ab3a: 845 entradas en data/manifiesto.yaml, 841 payloads con sha256 de 64 hex derivado por tests/manifiesto.py (las 4 sin sha son «hechos», no payloads) → condición de mesa cumplida → DT-a rige. El ejecutor propaga, no decide (SELLA-3).
- DT-a: T27 exenta data/raw/**; línea base recongelada; se declara en hallazgos.md que la dirección inversa (archivo en corpus sin entrada en manifiesto) queda sin test hasta que ocurra un huérfano medido.
- DN-a: acto con perímetro completo del curador: necesidad para R4.3, SICEE completa, relaciones de Cero Desabasto y DGIS urgencias, validador en verde.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra 3c3ab3a ═══
(1) ESTRUCTURA: tests/check.py (T27 l.3806-3830, lista _T_INFRA_ARCHIVOS_CONOCIDOS l.3555; tests/baseline.json congelado en c6a0d72); data/curacion-registro/{necesidad-objeto-modelo.tsv, relaciones.tsv, evidencias.tsv, utilidad-modelo.tsv, aliases-fuentes.tsv, cola-adquisicion-registro.tsv} + tools/curador_registro/baseline.py (tres invariantes: toda relación con ≥1 procedencia en evidencias; utilidad 1:1 con relaciones; len(evidencias)−len(relaciones) = fusiones) — FP-230 verbatim; INFRAESTRUCTURA D1 declara relaciones.tsv «SIN VÍA de script».
(2) CONTENIDO: T27 en caja: 30 761 entradas nuevas, todas T27, medido tres veces por A1 (cierre §5-§6) → EXISTE-NO-SATISFACE. R4.3 en necesidad-objeto-modelo.tsv: `grep -c "R4.3" data/curacion-registro/necesidad-objeto-modelo.tsv` → pega la salida; A1 lo midió como sin N asignada. SICEE: fila en cola-adquisicion-registro.tsv y aliases-fuentes.tsv (A1) → EXISTE; en relaciones.tsv → NO-ENCONTRADO (bloqueado por FP-230). Cero Desabasto (base histórica, 11 036 filas: fecha, institución, entidad, CLUES, componente) y DGIS urgencias (descriptor + microdato): OBTENIDO en manifiesto por A1 (ids: deriva de `grep -n "cerodesabasto\|urgencias" data/manifiesto.yaml`); relación con R4.3 → NO-ENCONTRADO.
(3) COBERTURA RETROACTIVA: relaciones.tsv se cargó en bloque una vez (16180e6); nada posterior pasó por ella salvo via_capa2 → toda fuente de agosto/septiembre es invisible para la capa de relación por construcción. Se declara.

PIEZAS (un commit por pieza)
P1 · T27 (DT-a). En tests/check.py, T27 excluye toda ruta bajo data/raw/ (y cualquier raíz de data/raices.local.yaml) — un `continue` con comentario que cite FP-229, ADR-278 y esta firma; no se toca _T_INFRA_ARCHIVOS_CONOCIDOS. Recongela tests/baseline.json con el comando de la casa y anota el SHA. Una línea en forense/hallazgos.md: «dirección inversa manifiesto←corpus sin test; se instrumenta (T28) el día que aparezca un huérfano medido en data/raw» (v2.3). FP-229 → EJECUTADA.
P2 · NECESIDAD R4.3 (DN-a). Fila nueva en necesidad-objeto-modelo.tsv para R4.3 (desabasto → abandono de tratamiento / familia cuidadora → adherencia), con el texto de la regla verbatim de canon/modelo-decision-v4_0.md y objeto de evidencia = registro individual de desabasto + urgencias. ID de necesidad: deriva el siguiente libre (`cut -f1 … | sort -V | tail -1`), no heredes.
P3 · RELACIONES (DN-a, FP-230). En una sola escritura coherente: evidencias.tsv (procedencia = cierre de A1 y sus ids de manifiesto, con sha), relaciones.tsv (SICEE ↔ N25/N26 y la necesidad cívica concurrente; Cero Desabasto ↔ R4.3; DGIS urgencias ↔ R4.3 y N de salud que A1 mapeó), utilidad-modelo.tsv (proyección 1:1). Cierra con `python3 tools/curador_registro/baseline.py <baseline>` en VERDE — si el validador exige un campo que no puedes derivar, PARO de la pieza con el campo nombrado. Documenta la vía en GUIA-CURADOR-REGISTRO.md (sección nueva «alta de fuente nueva en tres tablas») e INFRAESTRUCTURA D1 pasa de «SIN VÍA» a citar esa sección. FP-230 → EJECUTADA.
P4 · TRÁMITE. Tablero: recibos; nota de cierre con conteo A.13 de filas tocadas por tabla; `via_capa2.py --root .` en lectura para confirmar que capa2 de las relaciones nuevas resuelve SI.

PERÍMETRO Y CONCURRENCIA: tests/check.py (solo T27) · tests/baseline.json · data/curacion-registro/{necesidad-objeto-modelo, relaciones, evidencias, utilidad-modelo}.tsv · tools/curador_registro/GUIA-CURADOR-REGISTRO.md · data/INFRAESTRUCTURA-v1_0.md (D1, una celda) · forense/hallazgos.md · tablero · notas · A.3 · cascada. En paralelo: N4 (nube). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar (FP máx 230+, ADR 279 candidato; N4 puede tomarlo antes — renumera quien fusiona segundo).
CONTADOR: tests utilizables en caja 0→1 (T27) · necesidades +1 · relaciones +N (declara) · cero estimaciones.
LO QUE NO HACE: no abre payloads; no descarga; no toca el manifiesto; no mide; no abre Ola 6 (eso es N5 con estos insumos).
SUCESORES: MAESTRA34-L3 (caja) · MAESTRA34-N5 hereda las relaciones de salud.

## CONSUMIDO

`PR #456` — https://github.com/Josanoforo/Modelado-Mexicano/pull/456 ·
rama `claude/maestra34-n6-launch-8tbvaj`, base `e4af4ed` (`origin/main`),
1/sep/2026, `ADR-279`, entorno NUBE, `COMPUERTA: ninguna`.

Seis commits: `[P1]` `6eb8d93` · `[P2]` `0e12bab` · `[P3]` `b0b74a2` ·
`[P4]` `cad4010` · `[CASCADA]` · este `[CONSUMIDO]`.

`FP-229` → EJECUTADA · `FP-230` → EJECUTADA.
Cierre: `forense/notas/2026-09-01-MAESTRA34-N6-cierre.md`.
Suite: `python3 tests/check.py --baseline` → VERDE.
Validador del curador: `python3 tools/curador_registro/baseline.py data/curacion-registro` → `"ok": true`.

Sucesores vivos: `MAESTRA34-L3` (caja, su compuerta era el merge de este acto) ·
`MAESTRA34-N5` hereda las relaciones de salud (`N36`).
