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

## 6 · ADENDA-1 — P5 motor (FIRMAS-16 B1, B2) y B3

`forense/encargos/2026-09-24-GEN2-RELEVO-CONSUMIDORES-2-ADENDA-1.md` (encargo revisado,
archivado verbatim y sellado al recibirse; el cuerpo original no se tocó). Base re-derivada:
`origin/main` avanzó 19 commits (PISOS-GEN2-2); se fusionó sin conflicto.

**Firmas** — FIRMAS-16 (#1137) **no ha fusionado**; su letra se leyó en la rama
`claude/new-session-uzhtuf` (lectura tipo 3, §2) y se sigue porque el encargo lo manda («si
no ha fusionado, se toma lo firmado y se declara»). Verbatim, FIRMADA 24/sep/2026:
- a157-01 (B1) «SÍ: `emitir_binaria` devuelve el par GEN2 medido donde conducta y disparador coinciden; los ocho ASIGNADO se retiran; donde no coinciden, se conserva con rótulo.»
- a157-02 (B2) «SÍ: las cuatro conductas NO-ADOPTAR-NC-0107 salen del consumo vivo (rol histórico, sin sortear).»
- a157-03 (B3) «SÍ: una partición sellada (`CORTES_C1`, RES-0165..0170) no es lectura numérica; `tipo_uso corte_pi` fuera del contador; ejecuta RELEVO-CONSUMIDORES-2.»
- 23e3-01 (B4) «(a) campos en la propia entrada (`corrida0_resultado_id`, `corrida0_generacion`, `clase_respaldo`); ejecuta RELEVO-CONSUMIDORES-2.» — es lo que ya aplicó P1.

Esto **corrige** lo que dijo §2 de esta nota: B3 no estaba en el repo al cerrar la primera
vez; ahora está firmada y se ejecuta.

**B1, par por par (INTERPRETACIÓN-DECLARADA de «coinciden»):**

| llave | ¿coinciden conducta y disparador? | operación |
|---|---|---|
| `util_sin_coercion:adopta` / `:rechaza_servicio` (RES-0019/0020) | SÍ — el universo medido impone sin coerción ni riesgo fiscal (firma a1) | retirado el ASIGNADO 0.71/0.29; devuelve el par GEN2 de `*_encig2025_luz` |
| `discrecional:paga_mordida` / `:tramite_normal` (RES-0001/0002) | NO — el hermano mide SOLICITUD (P8_3), no pago | conservado con rótulo `ASIGNADO-CONSERVADO-B1` |
| `con_registro:tramite_normal` / `:paga_mordida` (RES-0007/0008) | NO — proxy descriptivo del grupo P8_4, no pago | ídem |
| `evasion_norma:evade_norma` / `:cumple_norma` (RES-0023/0024) | NO — el RESULT es la conjunta, la regla la condicional | ídem |

Excepción a A.16, declarada: el rótulo de `discrecional:paga_mordida` va en un comentario
propio encima de la línea, porque las M selladas M-TRA-M-01/02 citan esa línea por texto
exacto (`tools/emite_m.py:cita_p`); con el rótulo en la línea, la regresión P2 fallaba
(`test_regresion_p2_pasa`, probado).

**Qué cambió y dónde:** escritor V5 `tools/escribe_relevo_consumo.py --motor-b1-b2` (diff seco,
idempotente, rechazo atómico; guardas de 4.1 sobre el hermano: CALC sellado, `cuenta_gen2`,
replay afirmativo, `p` = RESULT a seis decimales) · `milpa/src/emisor.py`, solo `emitir_binaria`:
`rol_uso: historico` → NO-EMITE · `tools/corrida0.py`: B2 da uso `activo=NO` leído del YAML
vivo; B3 saca `corte_pi` del contador y lo deja visible en
`legacy_fuera_del_contador_por_firma__corte_pi`.

Premisa que cayó: regenerar la demanda derivada (`corrida0.py demanda`) arrastra 25 RES nuevos
(RES-0212..0236) y renumera `corrida_natural`; la demanda en main ya estaba desfasada. Asignar
números es paso explícito de otro acto (D-23): **no se regeneró**, y B2 se lee del YAML.

**Tests:** `tests/test_emisor_fidelidad.py` fijaba `adopta` = 0.71 ASIGNADO; se actualizó a la
semántica firmada (el propio test pide «truenar» cuando el par gradúe). Suite del motor y del
escritor: los 3 fallos que quedan son idénticos por nombre a la línea base sin estos cambios
(`test_tramite_cinco_reglas_diez_probabilidades`, `test_motor_gen2_explicito::test_01`/`test_08`,
preexistentes). T-REPRO y T-LEGACY-DESGLOSE-SUMA: 0 FAIL. `check.py --rapido`: 0 FAIL.

**Contadores tras la adenda** (`status-despues-adenda1-consumidores2.txt`): legacy 137 → **123**;
motor 25 → **13** (−6 B3, −2 B1, −4 B2); procedencia 39; catálogo 22; marco 43; celdas-D 6;
adoptados 81 sin cambio (los RESULT citados por B1 ya estaban adoptados por los hermanos).
Tabla P6 re-derivada con el bucket motor.

**No editado, a propósito:** las NC `a157-05..08, 11, 12, 20..25` (resueltas por B1/B2/B3) y las
FP `a157-01..03`. #1137 las reescribe en su sitio; editarlas aquí duplicaría ids en la unión
(T47). Su cierre queda en NO-CORRIDO de la adenda.
