ESTADO: LISTO-NUBE
ENTORNO: NUBE
ENCOLADO: 2026-09-02 · gesto de encolado, precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026)
BITACORA:
- 2026-09-02 · LISTO-NUBE · encolado por PR [COLA] encola MAESTRA34-L1/N1/N2/L2/N3. COMPUERTA propia: MAESTRA34-L2 fusionado con R v1_2 completo (o parcial declarado) Y PR `[L] corridas v1_2` de mesa fusionado Y L-extraido-v1_2.tsv producido con la MISMA regla de extracción congelada de MAESTRA33-E21 (tools/extrae_l_v1_1.py sin editar; si hay que editarlo, PARO y a mesa). Si falta cualquiera, cero commits.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

ENCARGO · ACTO MAESTRA34-N3 · AGREGA-2 — invoca /acto (y /score)
SHA de redacción: 8598a72. Redacta dirección (Fable), 1/sep/2026, contra v2.12. Estado: GATED — ENCOLADO por firma D4-a (1/sep): «D4-a» = los tres encargos de la cadena se archivan en forense/encargos/cola/ en un solo PR [COLA] y /despacha los toma por orden de nombre cuando su compuerta se cumpla. La fusión de ese PR es la firma. Es MAESTRA33-E13 (ADR-269) sobre v1_1 ∪ v1_2.

ENTORNO ASIGNADO: NUBE. NO se lanza en UBUNTU. MODELO SUGERIDO: Opus.
COMPUERTA: MAESTRA34-L2 fusionado con R v1_2 completo (o parcial declarado) Y PR `[L] corridas v1_2` de mesa fusionado Y L-extraido-v1_2.tsv producido con la MISMA regla de extracción congelada de MAESTRA33-E21 (tools/extrae_l_v1_1.py sin editar; si hay que editarlo, PARO y a mesa). Si falta cualquiera, cero commits.
FIRMA DE MESA: scoring v1_1 sellado (E12, ADR-25x — deriva el número): unidades EE(R), delta 0.5, proporción en banda + mediana |z|, L-vs-M pareada, B NO-APLICA. Sin firma nueva.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra 8598a72 ═══
(1) ESTRUCTURA: procedimiento-scoring-v1_1.md + sha; agregado_v1_1.py; tools/score_marco_m.py; scoreboard-v1_1{,-AGREGADO,-AGREGADO-b}.md EXISTE-SATISFACE.
(2) CONTENIDO: `ls forense/prereg-duelo-v2 | grep -i "v1_2\|AGREGADO-c"` → NO-ENCONTRADO (1/sep).
(3) COBERTURA RETROACTIVA: no aplica.

PIEZAS
P1 · Agregado sellado sobre v1_1 ∪ v1_2 sin editar el procedimiento; n total, celdas puntuadas, exclusiones declaradas por celda.
P2 · scoreboard-v1_2-AGREGADO.md con la pregunta doble y sus IC (pareado L_solo−M, L+corpus−M). Declarar si el IC cruza cero; no adjudicar si cruza.
P3 · Insumo al tablero: FP-220 (Ola 6, criterio ≥8 celdas L∩M) y la fila sucesora de FP-221 reciben el conteo real L∩M derivado aquí; nota en motor-nucleo-medible si el criterio de activación del corredor E se cumple (no lo activa: eso es firma de mesa).

PERÍMETRO Y CONCURRENCIA: forense/prereg-duelo-v2/scoreboard-v1_2-AGREGADO.md (+ salida de agregado) · notas · tablero · A.3 · cascada. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar.
CONTADOR: celdas puntuadas 11 → N; scoreboard +1; declarado.
LO QUE NO HACE: no edita el procedimiento de scoring; no re-corre R, M ni L; no activa el corredor E; no abre Ola 6.
SUCESOR: MAESTRA34-E1 · REVISION-FALSADORES (dirección, fecha según D5).
