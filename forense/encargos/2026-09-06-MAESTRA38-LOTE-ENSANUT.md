## REGLA COMÚN (aplica a los cuatro; se archiva con cada uno)

Worktree propio sobre `origin/main`. Antes de evaluar cualquier compuerta: enlazar `data/raw` y copiar `data/raices.local.yaml` desde el clon padre; verificar que no declara `downloads`. A.2 tres partes (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`, sonda `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` fuera del sandbox, `ls data/raw/ | head -1`). Guard de rama: `git ls-remote --heads origin | grep -i <rótulo>` → coincidencia = PARA. Push del 0-bis (archivo verbatim de este encargo en `forense/encargos/2026-09-0X-MAESTRA38-<ACTO>.md`) al primer minuto.

Spec sellada = COMMIT-1: se verifica su `.sha256`, se cita, no se edita; si estaba mal, el COMMIT-2 lo dice y abre fila. Frase de sello en todo acto que mida: «el primer resultado que produzca este procedimiento es el que se reporta».

`tools/ya_medido.py` sobre cada id que se mida, salida pegada en A.8.

Rótulos ADR/FP no vienen preasignados. Se derivan en el 0-bis, contiguos, contra `main` y `git ls-remote --heads origin`; un rótulo reclamado por rama viva no se toma; renumera quien fusiona segundo.

Concurrencia declarada, no serial. Cada acto lista los archivos del que corre en paralelo y no los toca. Al fusionar, si `main` se movió: refresca, re-corre la cascada completa, reporta la diferencia. Orden: L2 ∥ LOTE-ENSANUT → C1 ∥ LOTE-CRUCE.

Anti-PR#77 en todo acto que registre: `ls -la` del corpus compartido al cerrar, no del worktree. Cascada D-10 completa: ADR por comando de la casa, cabecera de gobernanza, recifrado L0, registro-rotulos, T25, `tests/check.py --baseline` VERDE o PARO-reporta; `## CONSUMIDO` con el PR.

Vocabulario: A.4 (EXISTE-SATISFACE / EXISTE-NO-SATISFACE / NO-ENCONTRADO con universo / NO-ACCESIBLE) + D5 (NO-ADQUIRIDA-POR-COSTO). Todo veredicto negativo declara cuántos archivos examinó el comando (A.13). Toda cantidad medida entra con escala y universo declarados (A-bis 3 y 4).

# ENCARGO · ACTO MAESTRA38-LOTE-ENSANUT · L16 + L17 — invoca `/acto` (D-11)

SHA `693ea23` · COMPUERTA: ninguna (LOTE-LAPOP fusionado, #551) · ENTORNO: UBUNTU con corpus (no nube) · MODELO: Opus · SPECS: `forense/prereg-caja/S6-L16-spec-v1_0.md` (`salud.atencion.grave`, R4.4, ENSANUT 2024 adultos `h0402`/`u0201`…; «dos linajes sin reconciliar» — la spec fija cuál se usa; si ambos tienen codebook, se reportan por separado, nunca se promedian), `forense/prereg-caja/S7-L17-spec-v1_0.md` (`salud.vacunacion.disponible`, id de §3.9 información — corregido en `registro-rotulos` por N11; `adultos_ensanut2024_w`, 20+, `a0904`/`a0906`/`a0917`/`a0919a`, ponderador `ponde_f`). Un PR, un ADR, un recibo; commit por pieza.

FIRMAS — verbatim: N10 (dos MEDIBLE-COMO-ESTÁ); D8 «mantener el criterio 2 como está (ADR-265, firma 9)… Ningún texto del canon se toca»; «no quiero hacerlo al mínimo»; 6/sep: «revisa qué encargos podemos correr en paralelo en caja … ahora ya podemos».

A.8 al arrancar: specs y sha; `ya_medido.py` → NUNCA-MEDIDA ×2; inventario v1_1 (adultos 1 682 filas con texto); salud hoy 2 de 5 (L3-BIS: R4.4 grave y R4.3 desabasto); payloads por archivo: `grep -icE "^  archivo:.*adultos_ensanut2024_w" data/manifiesto.yaml` → 5 (6/sep), adolescentes 5, utilizadores 6, integrantes 5, ENCUCI 2.

EJECUCIÓN: por pieza, COMMIT-2 propio — resultados con IC, celdas, n por celda, fila B-bis; una pieza que PARA no tumba el lote. Cada resultado entra a `milpa/tramite-ola5-propuesta-v0.yaml` como entrada nueva con `se_mueve_si` verbatim de su spec; no toca sellos previos ni canon. Escala y universo declarados. Si con estas dos salud queda en ≥ 3 de 5 EXISTE-SATISFACE: se escribe ABRE-CANDIDATO-CON-RESERVA en la nota y se PARA — la apertura es de mesa (D8); la reserva lleva la lista de lo que falta para 5/5 (R4.1 `leve_sin_imss`, R4.2 `hombre_sin_permiso`: instrumento mínimo de L3-BIS/N10).

PERÍMETRO Y CONCURRENCIA. Toca: `data/l16-*`, `data/l17-*` · propuesta (append) · INFRAESTRUCTURA · `forense/notas/2026-09-0X-MAESTRA38-LOTE-ENSANUT-*.md` · hallazgos · tablero · A.3 · cascada. NO toca: canon · `milpa/tramite.yaml` · manifiesto · `registro-rotulos` (salvo cascada). En paralelo corre L2 (archivos arriba). Si te encuentras escribiendo fuera de esta lista, PARA.

FP/ADR: derivados en el 0-bis (FP extra sólo si ABRE-CANDIDATO-CON-RESERVA). CONTADOR: salud EXISTE-SATISFACE 2 → declara · medición: sí.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-LOTE-ENSANUT` (rama `acto/maestra38-lote-ensanut`,
PR pendiente de abrir al momento de este commit). L16 (`salud.atencion.grave`,
Rama B, `NO-DISCRIMINA`) y L17 (`salud.vacunacion.disponible`, Rama B primaria,
`CORROBORADA`; Rama C descriptiva mixta) — ambas Rama A (`ENNVIH`) sin correr,
PARO parcial declarado por ponderador ambiguo sin codebook. Contador de salud
permanece 2 de 5; `ABRE-CANDIDATO-CON-RESERVA` no se disparó. Detalle completo
en `forense/notas/2026-09-06-MAESTRA38-LOTE-ENSANUT-resultados.md`,
`ADR-356` (re-verificado por `MAESTRA38-N14` contra `origin/main` real, sin colisión al momento del push final — la colisión declarada era entre esta rama y `maestra38-l2-mps2012`, dos ramas vivas, no contra `main`; `canon/gobernanza-v1_15.md`), `canon/registro-rotulos.tsv`
(`MAESTRA38-L16`/`MAESTRA38-L17`). `tests/check.py --baseline`: LÍNEA BASE
VERDE (3 FAIL / 171 WARN, sin novedad frente a `tests/baseline.json`).
