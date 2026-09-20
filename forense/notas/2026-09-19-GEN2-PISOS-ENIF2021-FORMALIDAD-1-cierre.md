# ACTO GEN2-PISOS-ENIF2021-FORMALIDAD-1 · CIERRE — las seis celdas de formalidad × {ahorra_solo_informal, informal_cualquiera, horizonte_corto} tienen piso t−1 en ENIF 2021 (`CALC-PISOS-ENIF2021-FORMALIDAD-0001`, REPRODUCE/IDENTICO); el enlace al marcador PARA por perímetro

Encargo archivado por A.3: `forense/encargos/2026-09-19-GEN2-PISOS-ENIF2021-FORMALIDAD-1.md`.
Spec congelada (COMMIT-1 `977c5dd`): `forense/prereg-caja/PISOS-ENIF2021-formalidad-spec-v1_0.md`
(sha256 `50b471e3…`). Resultados (COMMIT-2 `4a0ec38`): `data/corrida0/CALC-PISOS-ENIF2021-FORMALIDAD-0001/`.

## 0 · Arranque, compuerta, exposición

- Entorno: CAJA (Ubuntu/WSL2), Opus 5, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` vacío,
  `tools/entorno.py --sonda-red` → `montado=SI (examinados=419)`, `raices data_raw:SI`,
  `red=200`. Worktree nuevo: `data/raw` enlazado a `/home/pc0/mm-corpus/raw` y
  `data/raices.local.yaml` copiado del clon padre (no es PARO).
- Compuerta `#908 fusionado`: al primer intento (`origin/main = 1bb9e2c` = SHA de
  redacción) `gh pr view 908` daba `OPEN` y `git ls-tree origin/main` no traía ningún
  `*enut2019*` → **PARO con cero commits**, reportado. Mesa fusionó (`8a842af`,
  `MERGED`); relanzado sobre `8a842af` (10 commits tras el SHA de redacción).
- Guard 0.c: rótulo ausente en `git ls-remote`, `git worktree list` y `gh pr list`.
  CALC-id reservado libre: `git grep -l CALC-PISOS-ENIF2021-FORMALIDAD-0001` → 0
  aciertos en 6/6 ramas remotas (fuera del propio encargo archivado).
- A.8: `tools/ya_medido.py` para `dinero.ahorro.via_informal_ejes_enif2024` y
  `dinero.ahorro.horizonte_corto_ejes_enif2024` → `MEDIDA-EN: tramite-ola5-propuesta-v0.yaml`
  (son las reglas del árbitro 2024; este acto mide su piso 2021, no las reglas).
- Exposición (ADR-46): FD y cuestionarios 2021/2024, yaml del árbitro (con sus `p` de
  2024 a la vista), medidor de -0003; **ningún microdato abierto antes del COMMIT-1**.
- Incidente lateral, sin efecto: `python3 tools/asienta_replay_aislado.py --help` no tiene
  argparse y ESCRIBE (`asientos_nuevos=1`, una fila WBES ajena en
  `forense/replay-evidencia.tsv`); revertida con `git checkout` antes de cualquier commit.

## 1 · P0 · Lecturas por texto (detalle en la spec §1–§2)

(a) `P3_10` (2021) ≡ `P3_13` (2024): mismo texto de pregunta, misma instrucción, mismo
residual único; única diferencia de contenido = ISSSTE federal/estatal fundido (`2`) en
2021 y partido (`2`,`3`) en 2024, dentro del lado «con»; no mueve la dicotomía. Mapa
congelado: `{1..5}`→con, `{6}`→sin, `9`/blanco fuera y contados. Filtro de flujo leído
del cuestionario en ambas olas: (trabajó o tuvo trabajo, o verificación de actividad
afirmativa) ∧ no es trabajador(a) sin pago → **el mismo universo**; el diagnóstico
`FLUJO-DISCORDANCIA-N = 0` (8 881 filas alcanzadas por flujo = 8 805 en `1..6` + 76 «no
sabe») lo confirma sobre el dato.
(b) `P4_10` existe en 2021 con el mismo texto, los mismos siete códigos, el mismo
nemónico y sin filtro → **CONSTRUIBLE**; se miden las seis.

## 2 · P2 · Resultados (`CALC-PISOS-ENIF2021-FORMALIDAD-0001`, primera corrida)

`enif2021_csv` (`0f314fa3…`), `conjunto_de_datos_tmodulo_enif_2021.csv`, 13 554 personas;
`FAC_ELE`, `EST_DIS × UPM_DIS`, 10 000 réplicas `PCG64(42)` compartidas, IC percentil.
Universo `P3_10 ∈ {1..6}` = 8 805 (excluidos: 4 673 blanco por secuencia, 76 «no sabe»,
0 fuera de catálogo).

| desenlace | celda | p | IC95 | n | denominador ponderado |
|---|---|---|---|---|---|
| D9 | sin-seguridad-social | 0.441029 | [0.422842, 0.459052] | 4953 | 32684040 |
| D9 | con-seguridad-social | 0.345204 | [0.324945, 0.364792] | 3852 | 24532995 |
| D9 | trabaja | 0.399942 | [0.386440, 0.413697] | 8805 | 57217035 |
| INFORMAL-CUALQUIERA | sin-seguridad-social | 0.562820 | [0.545559, 0.579911] | 4953 | 32684040 |
| INFORMAL-CUALQUIERA | con-seguridad-social | 0.620711 | [0.598881, 0.641611] | 3852 | 24532995 |
| INFORMAL-CUALQUIERA | trabaja | 0.587642 | [0.574289, 0.600718] | 8805 | 57217035 |
| HORIZONTE-CORTO | sin-seguridad-social | 0.348697 | [0.330543, 0.366767] | 4795 | 31750911 |
| HORIZONTE-CORTO | con-seguridad-social | 0.206676 | [0.188324, 0.225347] | 3762 | 24039841 |
| HORIZONTE-CORTO | trabaja | 0.287501 | [0.273345, 0.301543] | 8557 | 55790752 |

`B-VALIDAS = 10 000` en las 9 celdas. Desenlace indefinido dentro del universo: 0 (D9),
0 (informal_cualquiera), 248 (horizonte_corto: `P4_10 ∈ {8,9}`).
**Control de coherencia (A-bis 4):** `COHERENCIA-DELTA-NUM-W` = 0.0, 0.0 y 1.9e-09 —
sobre el universo de quien trabaja, las dos celdas reproducen el total de ese mismo
universo. No se compara contra el nacional de -0003 (otro universo).
Lectura acotada (módulo de auditoría del encargo): «sin seguridad social» ahorra más
sólo por vía informal y con horizonte más corto; «con seguridad social» ahorra más por
vía informal *cualquiera* — el signo cambia entre los dos desenlaces de ahorro, así
que «los informales ahorran en tandas» no se sostiene ni como resumen. Es acceso y
proxy de seguridad social, no cultura; 2021 es dato de pandemia.

Replay: `corrida0 verify` → REPRODUCE/IDENTICO; `tools/verifica_aislada.py` (proceso
nuevo) → REPRODUCE/IDENTICO, 67/67 RESULT, 3/3 inputs COINCIDE, evidencia en
`forense/analisis/gen2-pisos-enif2021-formalidad-1/evidencia-replay-pisos-enif2021-formalidad-2026-09-19.json`
(renombrada desde `evidencia-replay-aislado.json` porque T02 la colisionaba con la de
ENADID) y asiento propio en `forense/replay-evidencia.tsv` antes de publicar (E.7).
Registro: `corrida0 registro --verifica --escribe --lote CALC-PISOS-ENIF2021-FORMALIDAD-0001`
tras fusionar `origin/main` (`adcfa97`, `#911`/`#912`): +1 corrida, +67 RESULT, `usos.tsv`
byte a byte idéntico; **pisadas ajenas = 0** en corridas/resultados/usos (multiset
contra `HEAD` excluyendo las filas propias). `cuenta_gen2 = PENDIENTE-DE-MESA`
(`FP-396`); no adopta.

Tabla de identidad propia: `forense/prereg-caja/PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv`
(6 filas CONSTRUIBLE, `cell_id` = RESULT `-P`, mismo esquema que la rejilla; consumer
`dinero.ahorro.tiene_ahorros.segmentacion_ejes_enif2024` para los dos desenlaces de
ahorro —el que la rejilla usa— y `dinero.ahorro.horizonte_corto_ejes_enif2024` para
el tercero). Test `tests/test_pisos_enif2021_formalidad.py`: rejilla emitida == rejilla
del árbitro (categorías leídas del yaml), 6/6 RESULT sellados, sidecar y fuente.

## 3 · P3 · Enlace al marcador: PARA por perímetro (NC-0384)

Se intentó la «una línea» del encargo: añadir la tabla nueva a la tupla de
`lee_tabla_identidad()` en `tools/marcador_segmento.py` (patrón de `#908`). Resultado
crudo de `tests/test_marcador_segmento.py`: **`FALLA -- 6 caso(s)`**, los seis
`T-ENLACE-BIYECTIVO: RESULT-PISOS-ENIF2021-FORMALIDAD-…-P es CONSTRUIBLE y no enlaza
con ninguna fila MARGINAL`. Causas, todas fuera de una línea: (1) `indice_identidad()`
indexa por `(consumer, outcome, axis, category)` con `setdefault` — las cuatro filas
selladas `NO-CONSTRUIBLE` de la rejilla tienen la misma llave y ganan por orden; hacer
que la tabla nueva las *suceda* es una regla de precedencia nueva; (2)
`MAPA_CONSUMER` no tiene `dinero.ahorro.horizonte_corto_ejes_enif2024`; (3)
`CALC_PISOS_SELLADOS` no lista el CALC nuevo (sin eso, aun enlazadas saldrían
`CONSTRUIBLE-EN-TABLA-SIN-RESULT-SELLADO`). Y aun resuelto todo eso, la guardia 3 del
mismo test exige que la causa `P3_13 comparable no existe en ENIF 2021` siga apareciendo
en alguna fila SIN-PISO mientras esté en la tabla sellada. Revertido (`git checkout`);
`tools/marcador_segmento.py` no cambia. Marcador re-derivado con `--escribe`: diff 0;
`sin_piso = 21` (11 ENUT 2019 · 4 `NO-CONSTRUIBLE:P3_13 comparable no existe en ENIF 2021`
· 6 `SIN-CONSUMER-EN-TABLA-DE-IDENTIDAD`), `cobertura_de_piso = 73`. La causa errónea de
las 4 filas de la rejilla no se edita (tabla sellada): queda **sucedida en el árbol**
por la tabla nueva y asentada en `hallazgos.md`; el marcador la seguirá transportando
hasta el sucesor.

## 4 · Perímetro y contadores

| pieza | estado |
|---|---|
| P0 (a)/(b) | hecho, en la spec |
| P1 COMMIT-1 | `977c5dd` (spec md + sidecar, spec.yaml, medidor) |
| P2 COMMIT-2 | `4a0ec38` (CALC sellado, tabla, test, replay aislado) |
| P3 enlace marcador | PARA, NC-0384 |
| P3 marcador re-derivado | `--escribe`, diff 0, `sin_piso` 21→21 |
| cascada | `ADR-559`, L0, `FP-396`, `NC-0384`–`NC-0385`, hallazgo, rótulo |

No tocado: la tabla de identidad de la rejilla, `CALC-PISOS-ENIF2021-EJES-*`,
`tools/pisos_ejes.py`, ENIF 2024, el yaml del árbitro (se lee como input con sha256),
`tools/marcador_segmento.py`. Contadores que mueve: corridas GEN2 selladas +1
(`PENDIENTE-DE-MESA`); `sin_piso` 0; adopciones 0. Semilla PARA-v2.15 del encargo (todo
NO-CONSTRUIBLE por ausencia de variable cita texto de pregunta y secciones del FD)
queda asentada en `hallazgos.md`, no se edita `instrucciones-proyecto-v2_14.md`.
