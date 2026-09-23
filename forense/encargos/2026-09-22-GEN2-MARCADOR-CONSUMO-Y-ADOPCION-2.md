# ENCARGO · ACTO GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2 · El marcador consume lo que los pilotos, el lote y los duelos ya adjudicaron; ENIF entra con reserva de ancho; la razón de cuidado se enlaza sin medir

> ENTORNO: **NUBE** — cero microdato: todo está sellado. Hook; si no coincide, PARA.

CABECERA · SHA `3f48be30` · una sola sesión · MODELO: Opus · MODO: **ABIERTO** · CONTADOR: cero mediciones; `estimadores-por-segmento.yaml` n_celdas 20+15 → N (derivado); estados del marcador RESERVADA → EVALUADA/CONSUMIDA para lo ya adjudicado (reportado); `celdas_validadas` no cambia (cuenta desde sellos, no desde el marcador) · ids raíz de acto · lote de tres piezas afines (D-11).

## 1 · OBJETIVO
(P1) Que `tools/marcador_segmento.py --escribe` **consuma adjudicaciones**: lea celdas-D (`data/curacion-registro/celdas-d/*.yaml`), CALC de adjudicación de duelos y lotes (`CALC-DUELO-*-ADJUDICACION-*`, `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-*`, `CALC-GOB-DIGITAL-EXE-*`), y pase cada cruce/celda de `RESERVADA` a `EVALUADA-PROSPECTIVA` / `EVALUADA-RETROSPECTIVA` / `CONSUMIDA-SIN-PILOTO` según el orden de sellos — hoy 16 filas `EMITIDA-SIN-R` y decenas `RESERVADA` describen un árbol de hace tres días. (P2) Que la firma F2 de FIRMAS-7 (ENIF 2024, 32 marginales, ADOPTAR-CON-RESERVA-DE-ANCHO) llegue al yaml por el tool, con el IC rotulado. (P3) Que la celda `reparto_hogar` de cuidado quede enlazada (piso 2019 = 0.238, R 2024 = RAZON-NUCLEO-NACIONAL, ambos sellados sobre el núcleo) y las 10 `sexo_edad` marcadas `NO-CONSTRUIBLE-POR-CRUCE` (firma (b′), #1007). «Hecho» = `marcador-segmento.tsv` re-derivado sin editar a mano: 0 filas `EMITIDA-SIN-R` cuyo R exista en un CALC sellado; los 24 cruces del duelo ENVIPE 2026 y los 14 del lote con estado y rótulo; `NC-…PILOTO-3-COMMIT-2-3-v1_3-3619-01` CERRADA; yaml con las 32 de ENIF (`tipo_incertidumbre = "calibrado: un solo choque 2018→2021, conservador"`); fila ENUT enlazada y 10 `NO-CONSTRUIBLE-POR-CRUCE`; guardias T-RESERVA/T-EMISOR/T-PISO en verde.

## 2 · FIRMAS DE MESA
Ya selladas, se citan: FP-383 (marcador sobre el catálogo); firma 17/sep (piso adoptado); `adopcion:piso-t1-marginales-por-instrumento` (#1002); F2 en FIRMAS-7 (#1015: ADOPTAR-CON-RESERVA-DE-ANCHO); (a)(b′)(c) de ENUT (#1007). Ninguna nueva.

## 3 · LO QUE DIRECCIÓN SABE
- `[EJECUTADO]` `data/corrida0/marcador-segmento.tsv`: 16 `EMITIDA-SIN-R` (9 de `via_informal` ENIF 2024, 3 de `gobierno_digital` ENCIG 2025, 4 de `evasion_norma` ENVIPE 2025); decenas de `RESERVADA` en `via_informal`. `[LEÍDO]` NC `…PILOTO-3-COMMIT-2-3-v1_3-3619-01`: «`edadxescolaridad` sigue RESERVADA tras `--escribe` (sin diff): la herramienta solo levanta…» — la herramienta no consume adjudicaciones. `[EJECUTADO]` `milpa/estimadores-por-segmento.yaml`: 20 cruces + las 15 ENVIPE de #1002; 0 de ENIF; `n_emitidas_sin_evaluar: 206`.
- `[SUPUESTO]` El lote ENIF 2024 derivó R para sus 14 cruces en COMMIT-3, y el piloto 3 para `edadxescolaridad` ENCIG: esas filas son `EVALUADA`, no `EMITIDA-SIN-R`. El acto lo lee de los CALC por id; lo que no encuentre sellado sigue `RESERVADA`.
- `[SUPUESTO]` `ADOPTADO_ACTIVO` no se moverá por P2 hasta que el canal (`GEN2-TUBERIA-CANAL-PUBLICACION-1`) publique la vista; se dice, no se fuerza.
- ADJUNTOS: ninguno.

## 4 · YA HECHO / YA DECIDIDO
`grep -c "consume\|adjudicacion" tools/marcador_segmento.py` → reporta; `grep -c "enif" milpa/estimadores-por-segmento.yaml` → 0 al redactar; `ls forense/encargos/ | grep -i "ENLACE-MARCADOR\|CONSUMO"` → 0. Ramas vivas: `DUELO-ENVIPE2026-MARGINALES-2` (caja) — sin archivo común.

## 5 · PIEZAS
- **P1 · Consumo.** El tool lee las tres fuentes de adjudicación por id, deriva el rótulo por orden de sellos (v2.16 §4: emisión sellada antes de R = PROSPECTIVA), escribe estado y `adjudicado_id`; un test con un CALC de fixture por fuente. Los cruces cuyo R existe pero cuya emisión se selló **después** (si los hay) → `EVALUADA-RETROSPECTIVA`, dicho.
- **P2 · ENIF con reserva de ancho.** Las 32 marginales entran al yaml con `champion = PERSISTENCIA(t−1)`, punto de `CALC-PISOS-ENIF2021-EJES-0001`, IC de `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001`, `tipo_incertidumbre` rotulado; `decision_ref` = fila F2.
- **P3 · ENUT.** Fila `reparto_hogar` → `SOLO-PISO` con `piso_fuente = CALC-ENUT2019-NUCLEO-EJES-0001`, R = `RAZON-NUCLEO-NACIONAL`; las 10 `sexo_edad` → `NO-CONSTRUIBLE-POR-CRUCE` citando la guardia de `tools/enut_nucleo.py`.
- **P4 · Cierres y nota.** NC 3619-01 CERRADA; la lista real de `RESERVADA` (lo que de verdad nadie ha visto) pegada en la nota: **es el insumo del piloto 4 (`GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1`)**.

## 6 · LATITUD
DECIDES TÚ: estructura del consumo, orden. PREGUNTAS A MESA: un cruce con R derivado en un CALC **no** de adjudicación (p. ej. un descriptivo Codex) — ¿`CONSUMIDA-SIN-PILOTO` (recomendado: se vio, no se adjudicó) o se ignora? NO DECIDES: §7.

## 7 · PAROS
a) derivar cualquier R nuevo (este acto solo lee sellos) · b) editar yaml/TSV a mano o CALC · c) adoptar fuera de F2 y de lo ya firmado · d) no aplica · e) caja · f) inalcanzable.

## 8 · COMPUERTAS
Ninguna que proteja las cuatro cosas. Orden sugerido: después de #1015 (F2 en main).

## 9 · PERÍMETRO
Propio: `tools/marcador_segmento.py` + test · `data/corrida0/marcador-segmento.tsv` (por tool) · `milpa/estimadores-por-segmento.yaml` (por tool) · `forense/no-corrido.tsv` · nota · `canon/L0/<raíz>.md`. Ajeno: CALC, celdas-D (lectura), `tramite.yaml`. «Si te encuentras escribiendo fuera de esta lista, PARA.»

## 10 · NO HACE · SUCESORES · CIERRE
No mide, no deriva R, no adopta fuera de firma. Sucesor: `GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1` lee la lista real de reservadas. Auditoría: no aplica. Cierre por /acto.


