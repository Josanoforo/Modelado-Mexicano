ENCARGO · ACTO MAESTRA38-N3 · PRE-REGISTRO-DE-CAJA — invoca /acto

SHA: 0ff3d710 · COMPUERTA: ninguna · ENTORNO: NUBE · NO en CAJA · MODELO: Opus (escribe specs que después no se pueden corregir hacia atrás; Fable si el ejecutor lo pide para L2). CARRILES: N4 en nube (tablero/cola/tests — disjunto: este acto sólo escribe specs y milpa/propuesta append).
FIRMA — verbatim (4/sep): «Caja sigue indispuesta. Revisa los prs recientes y piensa en que podemos aprovechar nube, automatizaciones, decisiones, encargos. Lo que nos acerque a que cuando exista caja podamos continuar.»
A.8 contra 0ff3d710: no existe ningún COMMIT-1 sellado para MAESTRA38-A2, L2 ni C1 (ls forense/notas/ | grep -c "spec-congelada.*\(A2\|L2\|C1\)" → 0); los insumos de diseño sí están en main: encargos de los tres actos (GAP-FISICO §3–§5; L2 v2 con dos ramas; C1), data/inventario-reactivos-descargas-mx-v1_1.tsv (42 548 filas, en repo), relaciones.tsv, necesidad-objeto-modelo.tsv (N42–N45 de salud), lista de ítems MPS por número en L12 (W2_P…), FD de ICPSR 35024 ya en manifiesto (documentación).
SPEC — tres specs, un commit cada una, cada una cerrada con la frase «el primer resultado que produzca este procedimiento es el que se reporta» y su sha256 en forense/prereg-caja/:
	•	S1 · MAESTRA38-A2 recenso: universo (dos raíces, downloads excluida), comandos exactos en orden, patrones B (auxiliar/copia) con la regla de exclusión escrita, umbral C ≤ 10, tabla nominal de depósitos de mesa con los nombres esperados (ICPSR .dta, WB 6667, PDN S1/S2/S6, 11 recetas), ENFIH-4 con el sha esperado de enfih2019_bd_csv_zip tomado del manifiesto.
	•	S2 · L2 rama MEDICIÓN y rama TEXTO: variables por número de ítem para R7.3, R7.6 y el experimento de lista (derivadas del FD de ICPSR ya registrado y de la nota de L12), ponderador esperado del .dta, universo, dicotomizaciones, celdas, y —para TEXTO— la lista de ítems cuyo texto sostiene o tumba cada lectura de L12. Las dos ramas en un archivo; la caja declara cuál corre.
	•	S3 · C1 re-asiento: las 7 relaciones bajo N36 con su N destino (adjudicación de L3-BIS, verbatim), formato de entrada de alta_relacion.py ya llenado por relación, y las 4 ENFIH con id y sha esperados.
Además: enmienda append en milpa/tramite-ola5-propuesta-v0.yaml bajo las dos entradas de L12: «spec de medición de primera mano sellada en S2, pendiente de .dta».
PERÍMETRO. Toca: forense/prereg-caja/{S1-A2,S2-L2,S3-C1}-spec-v1_0.md + .sha256 (nuevo dir) · milpa/tramite-ola5-propuesta-v0.yaml (append) · INFRAESTRUCTURA (registro del dir) · tablero (recibo) · A.3 · cascada. NO toca: data/** · tests/** · tools/** · canon (salvo ADR). Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR: ADR-336 · FP-296 recibo. CONTADOR: specs selladas 0 → 3 · medición: cero (pre-registro).

## CONSUMIDO

Ejecutado por `ACTO MAESTRA38-N3 · PRE-REGISTRO-DE-CAJA` (4/sep/2026,
entorno NUBE, rama `claude/tres-specs-prereg-caja-swkfhw`). Tres specs
selladas en `forense/prereg-caja/` (dir nuevo), un commit cada una:

- `S1-A2-spec-v1_0.md` + `.sha256` (`dcf035a`) — recenso: universo
  corregido a tres raíces (`data_raw`/`descargas_mx`/`downloads`,
  ésta última excluida — el encargo decía "dos raíces", `tests/
  manifiesto.py:62-67` documenta tres), comandos en orden, patrones B
  y umbral C fijados por primera vez (sin precedente previo con esos
  nombres), tabla nominal de depósitos de mesa — ninguno ha ocurrido
  todavía, y "11 recetas" no tiene respaldo textual en el árbol.
- `S2-L2-spec-v1_0.md` + `.sha256` (`2759801`) — rama MEDICIÓN (`R7.3`/
  `R7.6`, experimento de lista, ponderador declarado no determinable
  sin abrir el codebook) y rama TEXTO (tabla T1–T9b, wording ausente
  del repo salvo etiquetas de `P8`/`W2_P8`) del futuro `MAESTRA38-L2`
  sobre ICPSR 35024 — continúa el sucesor ya nombrado en el árbol como
  `MAESTRA37-L2 · MPS-CODEBOOK-Y-P3`.
- `S3-C1-spec-v1_0.md` + `.sha256` (`b617e85`, re-sellado en `bf0fae5`
  tras corregir una cita de ruta pelada que `tests/check.py` T03
  atrapó) — re-asiento: **corrige la premisa del encargo contra el
  registro real** — `MAESTRA37-L3-BIS` adjudica `N`-destino a 1 de 8
  relaciones bajo `N36` (etiquetado → `N41`), no a 7; entrada YAML ya
  llenada para `alta_relacion.py` con `relacion_id` esperado
  `REL-e7c3700e98be2d9aa7bbd55e` (verificado por control contra la
  fórmula real de `baseline.py`); 4 filas `ENFIH` de `FP-288` con
  `id_manifiesto`/`sha256` esperados.

Además (`0f9e9db`): enmienda append en `milpa/tramite-ola5-propuesta-
v0.yaml` bajo las dos entradas de `L12`; registro de `forense/prereg-
caja/` en `data/INFRAESTRUCTURA-v1_0.md`; recibo en `forense/tablero/
TABLERO-PROGRAMA.md`. Cascada (`14a0725`): `ADR-336` (coincide con lo
que este encargo anticipaba) · `FP-295` recibo (el encargo citaba
`FP-296`; máximo real en `forense/firmas-pendientes.tsv` era `FP-294`
— D-13 exige re-derivar, no heredar de prosa) · `canon/estado-
programa-v1_11.md` L0 recifrado y sus dos citas de "335 ADR" · `canon/
registro-rotulos.tsv` censa `MAESTRA38-N3`. `python3 tests/check.py
--baseline`: 19 FAIL / 172 WARN, LÍNEA BASE VERDE.

Contador: specs selladas 0 → 3, cumplido. Medición: cero, cumplido —
ningún commit de esta pieza abre microdato, corre censo real, ejecuta
`alta_relacion.py` ni mueve tier alguno. PR de este acto, contra
`main`.
