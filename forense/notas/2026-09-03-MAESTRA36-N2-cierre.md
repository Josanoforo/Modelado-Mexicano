# `MAESTRA36-N2 · CIERRA-N3-AGREGA-2` — cierre

Ejecuta P1/P2/P3 de `ACTO MAESTRA34-N3 · AGREGA-2`
(`forense/encargos/cola/2026-09-01-MAESTRA34-N3-AGREGA-2.md`, cuerpo +
ENMIENDA 5), en sesión manual de nube fuera de `/despacha`, por
instrucción explícita de mesa (precedente `ADR-248`,
`ACTO MAESTRA33-B2`). Encargo archivado en
`forense/encargos/2026-09-03-MAESTRA36-N2-CIERRA-N3-AGREGA-2.md` (A.3).

## ARRANQUE (Bloque D, punto 1)

- Repo: `/home/user/Modelado-Mexicano`, clon existente, no se clonó otro.
- `git log -1`: `ea45e01 Merge pull request #500 …` — coincide con el SHA
  de redacción declarado; `git status` limpio antes de empezar.
- `git fetch origin main` → `origin/main` = `ea45e01` (mismo SHA, no se
  movió). `git merge-base --is-ancestor ea45e01 origin/main` → ancestro.
- `data/raw/`: listado vacío (`ls data/raw/ 2>/dev/null | head -1` → sin
  salida) — esperado en nube, este acto no abre microdato ni red (punto 4
  del ARRANQUE saltado por instrucción explícita del encargo, sección
  ENTORNO ASIGNADO). `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`,
  coincide con `ENTORNO ASIGNADO: NUBE (cloud_default)`.
- Espejo del proyecto: no se derivó ninguna cifra de él — todas las
  cifras de esta nota salen del clon, con comando a la vista.

**COMPUERTA:** `ninguna` (declarada explícitamente en el encargo — todas
las legs de N3 quedan verificadas por producto en su propia
VERIFICACIÓN DE EXISTENCIA). No dispara verificación mecánica adicional.

## P1 · Agregado sellado v1_2 (14 de 14 celdas)

`forense/prereg-duelo-v2/agregado_v1_2.py` (nuevo) IMPORTA
`agregado_v1_1.py` **por ruta, sin editarlo** (mismo patrón que
`agregado_v1_1b.py` ya usa) y sobreescribe, por monkeypatch quirúrgico,
en la instancia importada:

1. `MARCO_TSV` → `marco-M-sorteado-v1_2.tsv`.
2. `UNIVERSO_11` (nombre heredado, sin renombrar) → las 14 celdas de
   v1.2: `CIV-M-01/02/04/10/12/13`, `DIN-M-01`, `FAM-M-01/05/06/07`,
   `TRA-M-02/03/07`.
3. `_leer_m` → intenta `M-<id>.json` (7 celdas heredadas de v1.1, mismo
   `M`) y si no existe, `M-<id>__v1_2.json` (7 celdas nuevas). Verificado
   por `ls corridas-M/` antes de escribir el script — los dos patrones
   son reales, no supuestos.
4. `_leer_l_variante` → lee de `L-extraido-v1_2.tsv` (224 filas: 14
   celdas × 2 variantes × 8 réplicas) en vez de `valor_extraido` (null en
   las capturas crudas), mismo patrón que `agregado_v1_1b.py` con
   `L-extraido-v1_1.tsv`.

`tools/score_marco_m.py`, `agregado_v1_1.py` y
`procedimiento-scoring-v1_1.md` **sin editar** — verificado
(`git diff` limpio sobre los tres, ver Perímetro abajo).

**14 de 14 celdas puntúan.** `0` marcadas `VERIFICACION-NO-PUNTUA` bajo
F-DD (`grado_DD` de las 14 filas de `marco-M-sorteado-v1_2.tsv` = `P1
PUNTUA`). `DIN-M-01` entra con su `EE_R` real (aproximada, cota inferior)
de `corridas-R/DIN-M-01.json`; la reserva `d1` (veredicto igual con
`EE_R_sin_diseno`, `din-m-01-doble-ee-resultado.json`, ENMIENDA 5) se
**cita, no se recalcula** — `0` celdas `AMBIGUA-POR-DISEÑO`.

Conteo A.13 (de `agregado-v1_2-resultado.json`):

| | n |
|---|---|
| celdas con R (`estado=COMPUTADO`) | 14 de 14 |
| celdas con M (`estado_M=EMITE`) | 14 de 14 |
| celdas con L-solo | 13 de 14 (`CIV-M-04` sin punto: sus 8 réplicas L-solo son NO-EXTRAIBLE) |
| celdas con L+corpus | 14 de 14 |
| L∩M (cualquier variante, con M) | 14 de 14 |
| extraíbles v1_2 (`L-extraido-v1_2.tsv`, leído no recalculado) | 191 EXTRAIBLE / 33 NO-EXTRAIBLE de 224 |

Comando: `python3 forense/prereg-duelo-v2/agregado_v1_2.py` → escribe
`forense/prereg-duelo-v2/agregado-v1_2-resultado.json` y lo imprime a
stdout. Determinismo verificado: dos corridas consecutivas producen
bytes idénticos (`diff` vacío).

### Control de regresión v1_1 (obligatorio antes de P1)

Se re-ejecutaron `agregado_v1_1.py` y `agregado_v1_1b.py`
**sin editarlos**, comparando la salida fresca contra el JSON
trackeado en git (`agregado-v1_1-resultado.json`,
`agregado-v1_1b-resultado.json`):

```
cp agregado-v1_1-resultado.json /tmp/orig.json
python3 forense/prereg-duelo-v2/agregado_v1_1.py > /tmp/fresh.json
diff /tmp/orig.json forense/prereg-duelo-v2/agregado-v1_1-resultado.json
```

**Resultado: NO byte-idéntico**, pero la única diferencia está en el
bloque `tra_m_02_informativo` (`R`, `EE_R`, `R_estado`: antes
`NO-ENCONTRADO`/`null`, ahora `COMPUTADO`/valores reales) — porque
`corridas-R/TRA-M-02.json` **ahora existe** (llegó con el trabajo de
v1.2, `MAESTRA35-L4`, posterior al 1/sep cuando se selló el JSON de
v1.1). Ese bloque es informativo, **fuera** del universo de 11 celdas de
v1.1 (`TRA-M-02` no estaba sorteada en `marco-M-sorteado-v1_1.tsv`,
`FP-213`). Verificado campo por campo: `universo_11`, `celdas`,
`agregado_marginal_por_corredor`, `comparacion_principal_pareada`,
`veredicto` y `conteo_l_interseccion_m_fp221` — **todos idénticos** entre
la corrida fresca y el JSON trackeado. Mismo resultado, mismo patrón,
para `agregado_v1_1b.py`.

**Interpretación declarada, no forzada:** el encargo (P1, verbatim) pide
comparar "byte a byte con `scoreboard-v1_1-AGREGADO-b.md`" — ese archivo
es prosa redactada a mano a partir del JSON, nunca fue ni pudo ser la
salida cruda de un script (formato markdown vs JSON); un diff mecánico de
stdout contra él nunca sería idéntico, con o sin regresión real. Se
verificó en su lugar (a) identidad byte a byte del JSON trackeado salvo
el campo informativo ya explicado, y (b) que las cifras que
`scoreboard-v1_1-AGREGADO-b.md` narra (n=11, proporciones 0.0 en los tres
corredores, medianas 16.84/30.23/31.39, pareado IC `[-106.35,+3.65]`,
veredicto `INDETERMINADO`, `conteo_l_interseccion_m_fp221.n=11`)
coinciden con el JSON regenerado. **No es PARO**: el procedimiento
sellado y los dos scripts no cambiaron; la única diferencia proviene de
que el árbol de datos creció (R real de `TRA-M-02` llegó después), no de
una edición del procedimiento. Los dos JSON regenerados se descartaron
(`git checkout --`) tras la verificación — no se commitea ninguna
regeneración de artefactos v1.1, fuera del perímetro de este acto.

## P2 · `scoreboard-v1_2-AGREGADO.md`

Mismo formato que `scoreboard-v1_1-AGREGADO(-b).md`. Contenido completo:
tabla de 14 celdas (`M`, `R`, `EE(R)`, `z_M`, `L-solo`, `z_L_solo`,
`L+corpus`, `z_L_corpus`), agregado marginal por corredor (`M`
n=14, `L_SOLO` n=13, `L_CORPUS` n=14; el único punto dentro de banda de
las 41 combinaciones es `FAM-M-06`/`L+corpus`, `z=-0.03`).

**Pregunta doble, dos IC pareados:**

| comparación | universo | punto | IC 95% | ¿cruza cero? | veredicto |
|---|---|---|---|---|---|
| `L_SOLO_vs_M` (principal, contrato F1) | 13 | −28.99 | [−74.02, +9.40] | SÍ | `INDETERMINADO` — no se adjudica |
| `L_CORPUS_vs_M` (secundaria, diagnóstico) | 14 | −13.09 | [−59.70, +27.05] | SÍ | `INDETERMINADO` — no se adjudica |

`L_CORPUS_vs_M` **no existía** como cálculo en `agregado_v1_1.py` (el
módulo base solo computa la comparación principal sellada,
`L_SOLO_vs_M`). Se añadió en `agregado_v1_2.py` reutilizando, **sin
copiar ni editar**, `_bootstrap_pareado_z` y `_adjudicar` del módulo base
— mismas funciones que ya usa la comparación principal, aplicadas a los
pares `(z_L_corpus, z_M)`.

**Reservas** (`scoreboard-v1_2-AGREGADO.md` §6): (a) `d1`/`DIN-M-01`,
citada de `din-m-01-doble-ee-resultado.json`, no recalculada; (b) F-DD, 0
de 14 celdas `VERIFICACION-NO-PUNTUA`; la única reserva F-DD viva
(`FP-234`, rangos de ola) ya no bloquea a `DIN-M-01` (LEVANTADA por `d2`
antes de este acto); (c) 96 de 224 capturas `L` reanudadas de v1.1 sin
`sha256_prompt`/`params` (ENMIENDA 2 de la cola) — su equivalencia de
prompt con las 128 nuevas está **re-derivada, no verificada**
(`forense/notas/2026-09-02-L-corridas-v1_2-cierre.md` §3); este acto la
cita como reserva abierta, no la resuelve.

## P3 · Tablero

- **`FP-220`** (`EVALUACION-OLA6`): se anexó a `ejecutada_en` el insumo
  v1.2 (agregado de 14 celdas). El criterio de apertura de Ola 6 (S3.a
  criterio 1: agregado con `L` sobre los **4 dominios ACTIVO**) sigue sin
  poder evaluarse — este scoreboard mide marco-M, no los 4 dominios; este
  acto no reevalúa Ola 6, eso es `N5`.
- **`FP-260`** (nueva, sucesora de `FP-221`): conteo real `L∩M` de v1.2 =
  **14 de 14** (≥8). Reafirma lo que `FP-221` ya reportaba con `n=11`
  para v1.1 — el criterio de activación del corredor `E`
  (`canon/motor-nucleo-medible-v1_0.md` §3.b) sigue **CUMPLIDO por
  conteo**. Este acto **no activa** el corredor `E` (`LO QUE NO HACE` del
  encargo) — deja el recibo para que dirección decida.
- **`canon/motor-nucleo-medible-v1_0.md` §3.b**: una línea declara el
  criterio cumplido por conteo (14 celdas comunes + scoring v1_1
  sellado), sin activarlo. **Hallazgo colateral, no corregido por este
  acto** (fuera de perímetro): el criterio ya estaba cumplido desde
  `MAESTRA33-E21` (2/sep/2026, `n=11≥8` con scoring ya sellado desde
  1/sep) y nunca se había declarado en el canon — esta línea lo declara
  ahora, con la cifra de v1.2, no retroactivamente con la de v1.1.

## Perímetro tocado (verificado, `git diff --stat` contra `ea45e01`)

- `forense/encargos/2026-09-03-MAESTRA36-N2-CIERRA-N3-AGREGA-2.md` (nuevo, A.3)
- `forense/encargos/cola/2026-09-01-MAESTRA34-N3-AGREGA-2.md` (solo línea 1 + BITACORA)
- `forense/prereg-duelo-v2/agregado_v1_2.py` (nuevo)
- `forense/prereg-duelo-v2/agregado-v1_2-resultado.json` (nuevo)
- `forense/prereg-duelo-v2/scoreboard-v1_2-AGREGADO.md` (nuevo)
- `forense/firmas-pendientes.tsv` (FP-220 anexado, FP-260 nueva)
- `canon/motor-nucleo-medible-v1_0.md` (§3.b, una línea)
- esta nota
- cascada (siguiente commit): `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_11.md`, `canon/registro-rotulos.tsv`, `forense/hallazgos.md` si aplica
- `forense/encargos/cola/2026-09-01-MAESTRA34-N3-AGREGA-2.md` línea 1 → `CONSUMIDO` (P-cierre, tras la cascada)

**NO tocado** (verificado): `milpa/**`, `corridas-R/`, `corridas-M/`,
`corridas-L/`, `L-extraido-*`, `procedimiento-scoring-v1_1.md`,
`agregado_v1_1.py`, `agregado_v1_1b.py`, `tools/score_marco_m.py`,
`tools/extrae_l_v1_1.py`, `exclusiones-v1_2.md`, `data/**`.

## Anti-PR#77

No aplica: este acto no descargó nada (no toca red ni microdato, ARRANQUE
punto 4 saltado por instrucción explícita del encargo). Declarado, no
omitido.

## CONTADOR

Celdas puntuadas v1_2: `0 → 14 de 14` (0 `AMBIGUA-POR-DISEÑO`). Scoreboard
v1_2: `0 → 1`. L∩M v1_2: `14` (reportado a `FP-220`/`FP-260`).
