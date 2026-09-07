## REGLA COMÚN (aplica a los cuatro; se archiva con cada uno)

Worktree propio sobre `origin/main`. Antes de evaluar cualquier compuerta: enlazar `data/raw` y copiar `data/raices.local.yaml` desde el clon padre; verificar que no declara `downloads`. A.2 tres partes (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`, sonda `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` fuera del sandbox, `ls data/raw/ | head -1`). Guard de rama: `git ls-remote --heads origin | grep -i <rótulo>` → coincidencia = PARA. Push del 0-bis (archivo verbatim de este encargo en `forense/encargos/2026-09-0X-MAESTRA38-<ACTO>.md`) al primer minuto.

Spec sellada = COMMIT-1: se verifica su `.sha256`, se cita, no se edita; si estaba mal, el COMMIT-2 lo dice y abre fila. Frase de sello en todo acto que mida: «el primer resultado que produzca este procedimiento es el que se reporta».

`tools/ya_medido.py` sobre cada id que se mida, salida pegada en A.8.

Rótulos ADR/FP no vienen preasignados. Se derivan en el 0-bis, contiguos, contra `main` y `git ls-remote --heads origin`; un rótulo reclamado por rama viva no se toma; renumera quien fusiona segundo.

Concurrencia declarada, no serial. Cada acto lista los archivos del que corre en paralelo y no los toca. Al fusionar, si `main` se movió: refresca, re-corre la cascada completa, reporta la diferencia. Orden: L2 ∥ LOTE-ENSANUT → C1 ∥ LOTE-CRUCE.

Anti-PR#77 en todo acto que registre: `ls -la` del corpus compartido al cerrar, no del worktree. Cascada D-10 completa: ADR por comando de la casa, cabecera de gobernanza, recifrado L0, registro-rotulos, T25, `tests/check.py --baseline` VERDE o PARO-reporta; `## CONSUMIDO` con el PR.

Vocabulario: A.4 (EXISTE-SATISFACE / EXISTE-NO-SATISFACE / NO-ENCONTRADO con universo / NO-ACCESIBLE) + D5 (NO-ADQUIRIDA-POR-COSTO). Todo veredicto negativo declara cuántos archivos examinó el comando (A.13). Toda cantidad medida entra con escala y universo declarados (A-bis 3 y 4).
# ENCARGO · ACTO MAESTRA38-N14 · CIERRA-LOTE-ENSANUT (renumera, asienta, abre fila)

SHA base: `origin/acto/maestra38-lote-ensanut` (PR #565) · COMPUERTA: ninguna para arrancar; ver PREMISA · ENTORNO: UBUNTU con corpus · MODELO: Sonnet · ORIGEN: auditoría de dirección del 6/sep sobre el reporte de `MAESTRA38-LOTE-ENSANUT`, contra el diff real de la rama.

**PREMISA DECLARADA, se verifica en el 0-bis y gobierna la pieza (1):** `MAESTRA38-L2` (PR #564) fusiona PRIMERO. Ambas ramas reclaman `ADR-356`; la regla de la casa es que **renumera quien fusiona segundo**, y ENSANUT es el segundo. Si al arrancar `#564` NO está fusionado y `#565` sí, la premisa se invirtió → **PARA y reporta**, no renumeres a ciegas. Si ninguno está fusionado, ejecuta igual las piezas (2)–(5) y deja (1) para el final, re-derivando contra `origin/main` en ese momento.

**Este acto NO fusiona ningún PR. La firma es de mesa.** Trabaja sobre la rama existente `acto/maestra38-lote-ensanut` y empuja ahí (el PR #565 se actualiza solo). No abras rama nueva ni PR nuevo.

## Hallazgos de la auditoría que este acto cierra

(A) `canon/gobernanza-v1_15.md` de esta rama declara `**ADR-356`, y `maestra38-l2-mps2012` declara el mismo `**ADR-356`. `git merge-tree` entre las dos ramas da 4 conflictos.
(B) `forense/tablero/TABLERO-PROGRAMA-v1_1.md` NO aparece en el diff de la rama, pese a que el reporte declaró «cascada D-10 completa» y el perímetro lo incluía.
(C) La nota de resultados declara que el codebook **invierte la asignación letra/dígito que la spec `S7-L17` asumía**. La regla común manda: spec sellada, si estaba mal, el COMMIT-2 lo dice **y abre fila**. Se dijo; no se abrió fila. `forense/hallazgos.md` tampoco está en el diff.
(D) Aparecen `tools/medidor_l16_atencion_grave.py` y `tools/medidor_l17_vacunacion_disponible.py` (360 líneas) fuera del perímetro declarado; y al revés, `data/l16-*` y `data/l17-*` — que el perímetro nombraba como la salida — **no existen**: las celdas viven sólo en la prosa de la nota.

## EJECUCIÓN — commit por pieza

**(1) Renumerar `ADR-356` → el primer libre contra `origin/main` ya movido.** Re-deriva el máximo con el comando de la casa contra `main` fusionado (no contra la rama), toma el contiguo, no saltes números. Renumerar **no es buscar-y-reemplazar**: una línea de `canon/` es un párrafo. Toca cada sitio donde el rótulo vive — bloque de `canon/gobernanza-v1_15.md`, cabecera, `canon/registro-rotulos.tsv`, `canon/estado-programa-v1_12.md` (L0 recifrado, verifica por CONTEO que la línea L0 no quedó duplicada), la nota de resultados, el `## CONSUMIDO` del encargo — y re-deriva otra vez justo antes del push final por si `main` se movió entre medias. Verifica al cerrar que NO queda ningún ADR duplicado: el rótulo viejo debe dar 0 en la rama, y el nuevo exactamente 1 en gobernanza.

**(2) Recibo en el tablero.** Asienta en `forense/tablero/TABLERO-PROGRAMA-v1_1.md` el recibo del lote con el rótulo ADR ya renumerado: L16 R4.4 NO-DISCRIMINA (con las dos p, sus IC95 y las n), L17 CORROBORADA (p, IC95, n), el PARO parcial de la rama A de ambas specs (ENNVIH+ENDIREH, ponderador `bx`/2002 ambiguo, 3 candidatos, sin codebook resolutorio en corpus), y que salud permanece **2 de 5** — el lote midió falsadores, no clasificó ids nuevos.

**(3) Abrir la fila que la spec mal escrita exige.** Deriva un `FP` nuevo contiguo (máx actual 325; re-deriva contra `main` y `git ls-remote --heads origin`) en `forense/firmas-pendientes.tsv`: la spec sellada `S7-L17-spec-v1_0.md` asumía una asignación letra/dígito del bloque `a0927` que el codebook invierte. La spec **NO se edita** (está sellada); la fila registra el defecto, cita el sha256 de la spec, dice qué se midió realmente y pide a mesa decidir si se sella una `v1_1`. Añade además la línea correspondiente en `forense/hallazgos.md`.

**(4) Sacar las celdas a `data/`.** Escribe `data/l16-atencion-grave-v1_0.tsv` y `data/l17-vacunacion-disponible-v1_0.tsv` con las celdas realizadas — por celda: n, numerador, proporción, IC95 inferior/superior, estratos y UPM, universo y escala declarados. Las cifras salen de re-correr los dos medidores, no de copiar la prosa. **Si al re-correr una cifra no reproduce la de la nota, eso es el entregable: PARA esa pieza y repórtalo** — no ajustes la nota para que cuadre. Registra los archivos nuevos en `data/INFRAESTRUCTURA-v1_0.md` (T27).

**(5) Regularizar el perímetro.** En la nota de resultados, una línea declarando que el acto escribió en `tools/` fuera del perímetro del encargo, con la razón, y que el perímetro del encargo estaba mal calculado — no el atajo. No borres los medidores: son el instrumento de (4).

## PERÍMETRO
Toca: `canon/{gobernanza-v1_15.md, registro-rotulos.tsv, estado-programa-v1_12.md}` (sólo por renumeración y cascada) · `forense/tablero/TABLERO-PROGRAMA-v1_1.md` · `forense/firmas-pendientes.tsv` · `forense/hallazgos.md` · `forense/notas/2026-09-06-MAESTRA38-LOTE-ENSANUT-resultados.md` · `forense/encargos/2026-09-06-MAESTRA38-LOTE-ENSANUT.md` (sólo `## CONSUMIDO`) · `data/l16-*`, `data/l17-*` · `data/INFRAESTRUCTURA-v1_0.md` · `tools/medidor_l1{6,7}_*.py` (sólo si (4) revela un defecto) · este encargo archivado en `forense/encargos/`.
NO toca: `forense/prereg-caja/**` (las specs están selladas) · `milpa/**` (ya asentado por el lote) · `manifiesto` · `cola` · `data/l2-*` ni nada de la rama de L2 · ningún merge.

## CIERRE
`tests/check.py --baseline` VERDE o PARO-reporta. Cascada D-10 en lo que la renumeración toque. Reporta: rótulo ADR final, `FP` derivado, confirmación por conteo de que no hay ADR duplicado ni L0 duplicada, y si alguna cifra de (4) no reprodujo.