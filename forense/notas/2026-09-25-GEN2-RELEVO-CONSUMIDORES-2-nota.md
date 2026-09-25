# Nota de cierre · ACTO GEN2-RELEVO-CONSUMIDORES-2

25/sep/2026 · encargo `forense/encargos/2026-09-24-GEN2-RELEVO-CONSUMIDORES-2.md`
(SHA de redacción `9632a880`, sello de cuerpo `23a4b831…`) ·
ADR `ADR-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-01` · 0-bis `e760e5bd` · PR #1138.

**Contadores movidos: tres.** `dependencias_numericas_legacy_activas` 137 → 135,
`legacy_activas_por_consumidor__procedencia` 40 → 39 y
`legacy_activas_por_consumidor__catalogo_de_momentos` 23 → 22, en árbol re-derivado
(`forense/analisis/relevo-consumidores/status-{antes,despues}-consumidores2.txt`). **No se movieron**
`marco_del_duelo` (43) ni `celdas_D` (6): ninguna de esas filas tiene un RESULT GEN2 que
pase las guardas; cada una lleva NC (§4). `N_resultados_gen2_adoptados_activos` queda en 81:
el RESULT que citan las dos lecturas relevadas ya estaba adoptado por `milpa/tramite.yaml`
(el contador cuenta RESULT distintos, no citas). Esto contradice la frase del encargo
«`adoptados` sube por cada cita» y se declara aquí. Adopción = merge de mesa (E.2).

## 1 · Arranque

- Repo `/home/user/Modelado-Mexicano`; `HEAD = 9632a880` = SHA de redacción;
  `git rev-list --count HEAD..origin/main` → 0; árbol limpio.
- Duplicado (0.c): `git ls-remote --heads origin | grep -ic relevo` → 0; `git worktree list` → 1
  (el propio); PR abiertos «RELEVO-CONSUMIDORES» → solo #1136 (`[deriva]`, ajeno).
- Entorno (hook `SessionStart`, crudo): `ENTORNO-DERIVADO = NUBE` · `senal-corpus: montado=NO
  archivos_examinados=0` · `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` ·
  `red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403)`. El encargo declara NUBE:
  coinciden. Ninguna pieza abrió microdato.
- COMPUERTA: ninguna. MODO «AUTÓNOMO», fuera del vocabulario de D-18: se trató como ABIERTO,
  con la cláusula v1.0 como latitud.

## 2 · Premisas re-verificadas

| premisa | rótulo | verificación | resultado |
|---|---|---|---|
| legacy 137; los cuatro sin cambio | EJECUTADO | `corrida0.py status` sobre `9632a880` | se sostiene (40/23/43/6) |
| FIRMAS-16 da B1–B5 | — | sin encargo, rama ni fila FIRMADA en el repo | **no está**; B4 se toma de la letra del encargo; B3 (= FP `a157-03`) sigue ABIERTA y no se aplicó |
| B4: `T-REPRO` lo cubre «sin código nuevo» (propuesta #1115) | LEÍDO | el caminante de `_ids_corrida0_declarados` llaveaba por `conducta/id/clave` y sin sección | **no se sostiene**: hicieron falta 7 líneas en `tools/corrida0.py` (D-21) |
| pines firmados no aplicados | — | `status`: 27 aplicados en el marco + 3 de `tramite` (el consumidor ya lleva marca); cero rechazos | no quedaba ninguno por aplicar |
| el marco son «parámetros de diseño (umbrales, λ, listas)» | SUPUESTO | los 43 consumidores: 28 `:L:`, 14 `:AGREGADO`, 1 `:M` | **no se sostiene**: son emisiones y agregados del duelo, no parámetros |
| celdas-D: «RESULT del champion vigente» | SUPUESTO | YAML: DIN/TRA `champion NINGUNO`, G5 ×3 BASELINE GEN1 sin CALC; GOB `C2`, cuya adjudicación ingiere RESULT de otra corrida | **no se sostiene** para ninguna de las seis |
| el escritor hay que extenderlo a procedencia y catálogo | SUPUESTO | V1–V3 solo escriben `tramite.yaml` | se sostiene; V4 lo hace |

## 3 · Lo que se hizo

- **Escritor V4** (`tools/escribe_relevo_consumo.py --relevo-consumidores-2`): las guardas de 4.1
  (+D6) por vía (i) (CALC SELLADA, `cuenta_gen2=SI`, replay afirmativo en RESULTADO, insumo
  crudo sin ingestión); diff seco por defecto; rechazo atómico si ya hay una cita distinta;
  idempotente (la segunda corrida da `SIN-DIFF`).
  - `procedencia.yaml:asignados_probabilidad:civico.denuncia.con_seguro`: `valores`
    [0.78, 0.22] → [0.790906, 0.209094], más `corrida0_resultado_id`,
    `corrida0_generacion: GEN2` y `clase_respaldo` (B4). Comprueba cardinalidad y suma.
  - Catálogo M08: seis columnas de relevo añadidas al final del TSV (firma N, unidad DELITO).
    Las 13 columnas selladas quedan idénticas byte a byte en las 24 líneas.
- **Registro** (`tools/corrida0.py`, D-21): la marca de procedencia se llavea con sección +
  `regla` (la misma llave que escribe la demanda), y el valor materializado de una lista
  `valores` es su primera categoría, la del RESULT citado.
- **Tests** `tests/test_escribe_relevo_consumidores2.py`: una prueba por llave, más negativos
  (cita distinta, cardinalidad, CALC que ingiere). Con los de V1–V3: 36/36.
- **Pin de celda-D GOB, probado y retirado**: la guarda lo rechaza con
  `RECHAZADO-RESULT-INGERIDO` (`CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` ingiere
  `CALC-ENCIG2021-CRUCES-HISTORICOS-0003/resultados.json`). No se forzó; no queda fila nueva en
  `pines-de-mesa.tsv`.

## 4 · Tabla final (P5) y residuo

Derivada por `forense/analisis/relevo-consumidores/tabla_final.py` →
`tabla-consumidores-v1_0.tsv` (universo: usos activos del registro en los cuatro buckets;
cada fila cae en una regla declarada, y cero salen `SIN-DICTAMEN`).

| consumidor | relevadas | antes relevadas por pin | NC |
|---|---|---|---|
| procedencia | 1 | 0 | 39: 7 β̂ de generador (CAJA) · 8 coeficientes asignados · 12 probabilidades asignadas · 12 θ condicionales |
| catálogo | 1 (M08) | 0 | 22: 6 AJUSTE sin identidad · 2 derivados sin champion (M05, M23) · 14 HOLDOUT |
| marco | 0 | 27 | 43: 42 L/AGREGADO (se propone HISTÓRICO-SIN-RELEVO) · DIN-M-01:M (ENNViH, CAJA) |
| celdas-D | 0 | 0 | 6: sin champion GEN2 citable (una, GOB, por guarda) |

NC `NC-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-01..11`, una por consumidor × razón y cada una
con la lista de sus slots. Los ids de raíz de acto admiten dos dígitos (`-\d{2}`, `RE_FP_NUEVA`),
así que 110 NC individuales no cabían; la granularidad por fila vive en la tabla.
Pendientes de mesa para FIRMAS-17: `FP-260925-GEN2-RELEVO-CONSUMIDORES-2-e760-01` (20
ASIGNADO de procedencia), `-02` (8 momentos AJUSTE/derivados) y `-03` (42 del marco,
HISTÓRICO-SIN-RELEVO), cada una con recomendación y texto de firma.

## 5 · Módulo de auditoría (§5)

- Escala y unidad: M08 queda relevado en unidad **DELITO** (robo total de vehículo, `FAC_DEL`),
  no PERSONA; va rotulado en `discrepancia_gen1`, y la firma N es la que lo autoriza. En la
  entrada de procedencia, `clase_respaldo` dice la misma unidad. No se promedia con ninguna
  cifra de unidad persona.
- Ninguna cifra se tecleó: los valores vienen de `resultados.json` del CALC sellado, leído por
  el escritor.
- PROSPECTIVA / RETROSPECTIVA: no aplica; no se emitió ni se adjudicó nada.
- `T-REPRO` (`check.t35_repro`, árbol final): 0 FAIL. `check.py --rapido`: 0 FAIL.
