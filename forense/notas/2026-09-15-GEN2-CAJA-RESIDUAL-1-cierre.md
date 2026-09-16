# ACTO GEN2-CAJA-RESIDUAL-1 · dos colas que sólo la caja podía cerrar — nota de cierre

**Fecha:** 15/sep/2026 · **Entorno:** CAJA (Ubuntu/WSL2), corpus montado (`tools/entorno.py --sonda-red`: `commit=2f5cffee075c · git_status=LIMPIO(0) · python=3.14.4 · numpy=2.3.5 pandas=2.3.3 scipy=1.16.3 yaml=6.0.3 pyreadstat=1.3.6 · CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · red=200 · raices=data_raw:SI · corpus=SI(examinados=413)`) · **Base:** `2f5cffe` (`origin/main`, merge de `PR #768`; `git rev-list --count HEAD..origin/main` → `0`) · **Rama:** `acto/gen2-caja-residual-1` · **Encargo:** `forense/encargos/2026-09-15-GEN2-CAJA-RESIDUAL-1.md` (0-bis A.3, llegó pegado en el mensaje de lanzamiento) · **Compuerta:** ninguna declarada · **Modelo:** el encargo sugiere Sonnet; corrió en Opus 5 — se declara, no se disfraza.

**Guard de arranque (0.a–0.d), crudo:** `git rev-list --count HEAD..origin/main` → `0` · `git status --porcelain` → vacío · duplicado: `git ls-remote --heads origin | grep -i caja-residual` → 0, `git worktree list | grep -i caja-residual` → sólo el de este acto, `gh pr list --search "CAJA-RESIDUAL" --state open` → 0 · `tools/limpia_arbol.py --reporta` → `worktrees vivos: 91 · base al_dia=SI · ramas remotas sin PR abierto -> fuera_de_politica: 0` (sale con código 2 por diseño: sólo reporta). `data/raw` enlazada a `/home/pc0/mm-corpus/raw` y `data/raices.local.yaml` copiada del clon padre (ambos gitignorados; ausentes en un worktree nuevo, no es PARO).

## 0 · Qué se pidió y qué salió

| pieza | pedido | salió |
|---|---|---|
| **P1** | `NC-0181`: resolver el contexto de `CALC-B-0001` con corpus montado y asentar `forense/replay-evidencia.tsv` para que los `AVISO` dejen de disparar | **HECHO.** `verify CALC-B-0001` ×3, estable: `REPLICA-RESULTADO · CONTEXTO-DISTINTO` (`CONTEXTO=DISTINTO` por `input_cambiado=IN-B-SELECTOR`; `RESULTADO=REPRODUCE` 90/90). Asiento actualizado con cita; `AVISO REPLAY-CONTRADICE-ASIENTO` para `CALC-B-0001` presente antes, ausente después (§1.3). `NC-0181` CERRADA (3/3 tercios). |
| **P2** | `NC-0126`: verificar `P4_10` contra el archivo real, no el descriptor (A.15); si de verdad está colapsada, declarar el corte acotado con su universo y cerrar | **HECHO.** El archivo trae exactamente 7 códigos `{1,2,3,4,5,8,9}`, sin código aparte para «no tiene ahorros»; el **cuestionario** también imprime la casilla colapsada (código `1`): el colapso está en el instrumento. Corte acotado declarado (§2.3). `NC-0126` CERRADA. |

**Contador, sin adornos: cero mediciones nuevas.** Ningún `RESULT` nuevo, ningún `CALC` nuevo, ninguna adopción (`data/corrida0/*.tsv` no se tocan: el `registro --verifica` de este acto corrió **en seco**, sin `--escribe`). Mueve `NC-0181` y `NC-0126` de `ABIERTA` a `CERRADA` y apaga un `AVISO` por corrida de `registro --verifica` en CAJA.

## 1 · P1 — `CALC-B-0001`: el contexto, resuelto donde sí se puede

### 1.1 · Lo que NUBE no podía y CAJA sí

`SANEA` (`PR #765`) dejó el tercio de `CALC-B-0001` en `NC-0181` porque en NUBE los 4 inputs de manifiesto (ENIGH 2016/2018/2020/2022) salen `RAIZ_NO_CONFIGURADA` y `_evalua_contexto` hace prevalecer `no_verificable_inputs` sobre cualquier otra razón (`tools/corrida0.py:2491`): `NO-VERIFICABLE`, nunca `DISTINTO`. Con corpus montado los 4 inputs `COINCIDE` y el contexto se pronuncia.

### 1.2 · Salida cruda de `python3 tools/corrida0.py verify CALC-B-0001` (tercera de tres corridas idénticas; las 90 líneas `[5/5 RESULT REPRODUCE]` omitidas aquí, todas con `delta=0.0` en flotantes y texto idéntico; `sha256` del log completo `ef663bca4bbea3b9768796427ba42ca3ae82950309d2f15b6c1527e36e4ae695`; exit 1 = veredicto concluyente distinto de `REPRODUCE`, `cmd_verify` sólo devuelve 0 para `REPRODUCE`)

```
VERIFY CALC-B-0001   (data/corrida0/CALC-B-0001)
  [1/5 SELLO] COINCIDE -- sello y todos los archivos que cubre coinciden
  [2/5 SPEC.YAML] IDENTICO  sellado=7feed075d55bf795f921bc7bd0d75ac8bffa60b205822cf1333364a2c67efe16  hoy=7feed075d55bf795f921bc7bd0d75ac8bffa60b205822cf1333364a2c67efe16
  [3/5 INPUT COINCIDE] enigh2016_nc_csv (manifiesto)  sellado=95e30780dfff83305fd1293945a0a5ed04c4e4daed4b0d45b66343db09e8eca1  actual=95e30780dfff83305fd1293945a0a5ed04c4e4daed4b0d45b66343db09e8eca1
  [3/5 INPUT COINCIDE] enigh2018_nc_csv (manifiesto)  sellado=5026cd951c109ac01c466aa22066beb7c6cbdcf7ecfc213967bd961d1243d636  actual=5026cd951c109ac01c466aa22066beb7c6cbdcf7ecfc213967bd961d1243d636
  [3/5 INPUT COINCIDE] enigh2020_nc_csv (manifiesto)  sellado=47417cac13da7dce3a710d86c5767564101086a51666ec674acf27740e0701d4  actual=47417cac13da7dce3a710d86c5767564101086a51666ec674acf27740e0701d4
  [3/5 INPUT COINCIDE] enigh2022_nc_csv (manifiesto)  sellado=3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06  actual=3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06
  [3/5 INPUT DISCORDA] IN-B-SELECTOR (repo)  sellado=886f2da43724f26ead82736eb48cdbba4b4145b51cdedf2b38f2fd1701871d92  hoy=83ff6a064cb0961af32178cbbbe4097358c85e5f59d7b67da138e096d3ea1b2a
  [3/5 INPUT COINCIDE] IN-B-SPEC-SELLADA (repo)  sellado=2376c21a0668a5f57db8cbddcd8cc59dd468dc7e10838f66da3b8156fb93c7ba  hoy=2376c21a0668a5f57db8cbddcd8cc59dd468dc7e10838f66da3b8156fb93c7ba
  [4/5 CONTEXTO] codigo=IDENTICO  commit_informativo=DISTINTO  (FP-358: no gatea)  parametros=IDENTICO  seed=IDENTICO  dependencias=IDENTICO
  CONTEXTO: DISTINTO  razon: input_cambiado=IN-B-SELECTOR

VERIFY: REPLICA-RESULTADO · CONTEXTO-DISTINTO   (CONTEXTO=DISTINTO · RESULTADO=REPRODUCE)
```

**Atribución del `DISTINTO` (un `DISTINTO` se atribuye, no se acepta):** `IN-B-SELECTOR` es `tools/baseline_temporal.py` declarado como input de repo en `data/corrida0/CALC-B-0001/spec.yaml:33-36`. `git log origin/main -- tools/baseline_temporal.py` → `67aa13d 2026-09-11 fix(gen2): autentica selecciones de transferencia` (después del sello `098298ca`, 9/sep); `git show 098298ca327f:tools/baseline_temporal.py | sha256sum` → `886f2da4…` = el sellado; hoy `83ff6a06…`. `git log acto/gen2-caja-residual-1 --not origin/main -- tools/baseline_temporal.py | wc -l` → `0`: no lo cambió este acto. **Precisión sobre lo que `NC-0181` decía:** la fila atribuía el cambio de `CALC-B-0001` a `dependencias_distintas`; en CAJA el eje que lo captura es `input_cambiado=IN-B-SELECTOR` (`dependencias=IDENTICO` en `[4/5]`) — mismo archivo, misma causa (`67aa13d`), distinta columna del verificador. Se asienta lo que el verificador dice, no lo que la fila anticipó.

### 1.3 · El asiento, y la prueba de que el `AVISO` se apagó

`forense/replay-evidencia.tsv`, fila `CALC-B-0001` (1 línea cambiada, 14 columnas antes y después): `resultado_replay` `REPRODUCE` → `REPLICA-RESULTADO · CONTEXTO-DISTINTO`; `contexto_replay` `IDENTICO` → `DISTINTO`; `razones` con el `REDERIVADO 2026-09-15 (…)` y la atribución de arriba; `fecha_verificacion=2026-09-15`; `entorno=CAJA (Ubuntu/WSL2) con corpus montado`; `procedencia=VERIFY-ESTRUCTURADO · ACTO GEN2-CAJA-RESIDUAL-1 (NC-0181)`; `alcance` con las tres corridas y la salvedad «NO es validación independiente del número». Las tres columnas de identidad (`spec_yaml_sha256`, `script_blob_sha256`, `input_sha256_efectivos`) **no se tocan**: son la identidad sellada contra la que `_evidencia_vigente` compara, y el sello `COINCIDE`. **Historia intacta:** el asiento anterior completo (veredicto, procedencia `HEREDADO-DEL-REGISTRO-PUBLICADO · corridas.tsv@66eed1b4f4a3`, alcance, nota) queda copiado verbatim en la columna `nota`, detrás de la referencia a esta nota.

Control positivo y negativo, mismo comando, misma caja, **en seco** (`python3 tools/corrida0.py registro --verifica`, sin `--escribe`; `git status --porcelain` vacío después de cada corrida — no escribe):

- **Antes** del asiento (4 m 38 s, 4 608 líneas): `AVISO · REPLAY-CONTRADICE-ASIENTO: CALC-B-0001 -- esta sesion observa REPLICA-RESULTADO · CONTEXTO-DISTINTO/DISTINTO; el asiento vigente dice REPRODUCE/IDENTICO (DESCONOCIDA) …` — **presente**.
- **Después** del asiento: `grep -c "REPLAY-CONTRADICE-ASIENTO: CALC-B-0001"` → **0** (4 596 líneas; `grep -c "AVISO.*CALC-B-0001"` → 91, todos `CALC-SIN-CONSUMIDOR-ACTIVO` / `RESULT-SIN-CONSUMIDOR`, que no son de este encargo). `AVISOS: 4589 → 4587`: los dos que desaparecen son el de `CALC-B-0001` (este acto) y el de `CALC-M-marco-M-sorteado-v1_3`, que en esta pasada proyectó `REPLICA-RESULTADO` en vez de `NO-REPRODUCE` — el veredicto inestable in-process de `NC-0182`, **no** obra de este acto; por eso esta vez `SECO data/corrida0/corridas.tsv: sin diferencia con el archivo en disco (168 filas)`. Los 6 `REPLAY-NO-VERIFICABLE-HOY` (`CALC-0001`, `-0001-v2`, `-0002`, `C0D-MARCADOR-v3`, `MOTRAL2015`, `SMOKE`) son de payloads en `descargas_mx`, que el sandbox no lee: iguales antes y después.

Las vistas derivadas (`data/corrida0/corridas.tsv`) ya proyectaban `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO / fuente_replay=VERIFY-EN-ESTA-SESION` para `CALC-B-0001` desde `B-MARCO` (`--lote` con causa); por eso este acto **no** corre `--escribe`: el diff en seco de `corridas.tsv` es `1+/1-` y la única fila que cambiaría es `CALC-M-marco-M-sorteado-v1_3` (`NO-REPRODUCE` in-process, el veredicto inestable ya adjudicado por `NC-0182` bajo E.3), no la de `CALC-B-0001`. `resultados.tsv` y `usos.tsv`: `sin diferencia con el archivo en disco`.

## 2 · P2 — `P4_10` verificado por archivo (A.15)

### 2.1 · Qué se abrió, con hash

- `data/raw/enif_2024_bd_csv.zip` — `sha256 00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` = `data/manifiesto.yaml:5551` (`enif_2024_enif_2024_bd_csv`, el payload de `CALC-ENIF-0001`). Miembro `TMODULO.csv`: 19 823 238 bytes, `sha256 5f1be142073f5758cbfb302fd7fb5dbf89c006b00729994207a9f05a46e1b8fd`, 398 columnas, **13 502 filas, 13 502/13 502 con 398 campos** (leído con `zipfile` + split, sin el módulo `csv`).
- `data/raw/enif_2024_fd.xlsx`, hoja `TMODULO` (1 483 filas), fila 290: `4.10 … | P4_10 | Alfanumérico | 1 | 1 | Menos de una semana/ No tiene ahorros` y códigos `2..5, 8, 9`.
- `data/raw/enif_2024_cuestionario.pdf`, p. 9, sección «VULNERABILIDAD FINANCIERA»: «4.10 Si usted dejara de recibir ingresos, ¿por cuánto tiempo podría cubrir sus gastos con sus ahorros? CIRCULE UN SOLO CÓDIGO · Menos de una semana/ No tiene ahorros ……… 1 · Al menos una semana, pero menos de un mes … 2 · … · No responde 8 · No sabe 9».

### 2.2 · Lo que el archivo dice (conteos sin ponderar; verificación del mapa de códigos, no medición)

```
P4_10 valores distintos (bytes crudos): [('1', 4275), ('2', 2443), ('3', 3405), ('4', 1328), ('5', 1479), ('8', 74), ('9', 498)]
longitud de los valores: {1: 13502}      # ni blanco, ni 'b', ni un octavo código
```

**Veredicto A.15: la categoría `1` está colapsada en el archivo Y en el instrumento.** No hay código aparte para «no tiene ahorros», ni blanco por secuencia, ni variable hermana que lo lleve. El descriptor no mentía; y no es un artefacto de publicación que otro archivo pudiera deshacer — el cuestionario impreso ya pide circular un solo código para las dos situaciones.

**¿Se puede descolapsar con otra variable del mismo archivo? No.** El FD de `TMODULO` no trae ninguna pregunta de *stock* («¿tiene ahorros?»: 0 conceptos con `tiene ahorro|tiene dinero ahorrado|cuenta con ahorro`). Lo más cercano es *flujo* — `P5_1_1..6` («de junio de 2023 a la fecha, ¿usted ahorró/guardó…?») y `P5_6_1..9` («¿guardó o ahorró en su cuenta…?»). Cruce, sin ponderar, sólo para mostrar que la casilla es heterogénea:

```
P4_10=1 · ALGUN-FLUJO-12M 1551 · SIN-FLUJO-12M 2724
P4_10=2 · ALGUN-FLUJO-12M 1582 · SIN-FLUJO-12M  861
P4_10=3 · ALGUN-FLUJO-12M 2734 · SIN-FLUJO-12M  671
P4_10=4 · ALGUN-FLUJO-12M 1191 · SIN-FLUJO-12M  137
P4_10=5 · ALGUN-FLUJO-12M 1339 · SIN-FLUJO-12M  140
```

Que 2 724 de 4 275 en el código `1` no reporten ningún flujo de ahorro en 12 meses es compatible con «no tiene ahorros», pero **flujo no es stock**: quien no ahorró este año puede tener ahorros viejos y quien ahorró puede haberlos gastado. El cruce no separa la casilla; sólo confirma que mezcla. No se reporta como estimando y no entra en ningún `RESULT`. **Y no es nuevo:** `CALC-ENIF-0003` (`ADR-506`, P4, `PR #766`) ya selló exactamente estos conteos — `RESULT-ENIF-COB-D-N-1 = 4275`, `RESULT-ENIF-COB-D-N-NINGUNA-VIA-EN-1 = 2724` (Δ 0 contra lo leído aquí con lector independiente) — y la cota ponderada `RESULT-ENIF-COB-D-P-NINGUNA-VIA-EN-1 = 0.6356` [0.616, 0.654], con la que `ADR-506` mandó la adjudicación de `NC-0126` a mesa. Este encargo es esa disposición: se verifica por archivo la premisa que faltaba (que el código no se descolapsa desde ningún archivo) y se cierra con el corte acotado.

### 2.3 · El corte acotado, con su universo — lo que se declara y se cierra

Sobre el universo sellado en `forense/prereg-caja/ENIF-AHORRO-spec-v1_0.md` §3 (personas 18+, en el eje `P3_13` de la familia A, `P4_10 ∈ {1,2,3,4,5}`; `8`/`9` fuera del numerador y del denominador, contados):

- **`horizonte_corto ⇔ P4_10 ∈ {1,2}`** mide **«no dispone de ahorros que cubran al menos un mes de gastos — incluidas las personas sin ahorros»**. No mide «horizonte corto» como rasgo de quien sí ahorra.
- **`horizonte_no_corto ⇔ P4_10 ∈ {3,4,5}`** mide **«dispone de ahorros para al menos un mes»** — ese lado es limpio.
- La partición `{1,2} | {3,4,5}` es exhaustiva y excluyente dentro de su denominador, así que los 4 `RESULT` de la familia A (`RES-0046..0049`) quedan **bien definidos como `1 − p(≥ 1 mes de ahorros)`**; lo que no se sostiene es la lectura «horizonte» pura del numerador. La sensibilidad `S1 ⇔ P4_10 = 1` hereda la misma acotación: «menos de una semana **o** sin ahorros».
- Consecuencia para el motor: cualquier consumidor que lea `RES-0046..0049` como «proporción con horizonte temporal corto» debe leerlas como «proporción sin colchón de un mes». No se edita ninguna spec sellada ni ninguna cita: es semántica, y va aquí y en la fila.

`NC-0126` se cierra con este corte acotado. Lo que sigue sin asignar no es una cola del registro sino una **demanda de instrumento**: un reactivo de stock que separe «no tiene ahorros» — ENIF 2024 no lo trae.

## 3 · Hallazgos

Uno, a `forense/hallazgos.md`: el colapso de `P4_10=1` no es del descriptor sino del instrumento, y la verificación «por archivo» de A.15 tiene que incluir el cuestionario para saber en qué capa nació la casilla — el archivo solo dice *que* está colapsada, el cuestionario dice *que no hay archivo que la descolapse*.

## 4 · Límites declarados

1. La verificación de `CALC-B-0001` acredita reproducibilidad del medidor sellado sobre inputs con hash idéntico; **no** es validación independiente del número.
2. El cruce de §2.2 es sin ponderar y sólo demuestra heterogeneidad; no estima nada.
3. El `AVISO` para `CALC-M-marco-M-sorteado-v1_3` sigue disparando en cada `registro --verifica` (in-process, `NC-0182`, ya adjudicado bajo E.3) — fuera del perímetro de este acto, y se dice.
4. `CALC-SIN-CONSUMIDOR-ACTIVO` ×N y los demás `AVISO` de `registro` no se tocan: no son de este encargo.

## 5 · A.13 — qué se examinó

`verify CALC-B-0001` ×3 (cada una abre los 4 CSV ENIGH y los 2 inputs de repo) · `registro --verifica` ×2 en seco (re-ejecuta todos los medidores sellados verificables; 4 608 líneas la primera) · `TMODULO.csv` (13 502 filas × 398 campos, 1 archivo) · `enif_2024_fd.xlsx` hoja `TMODULO` (1 483 filas) · `enif_2024_cuestionario.pdf` (p. 9 vía `pypdf`) · `git log`/`git show` sobre `tools/baseline_temporal.py` (1 archivo, 2 commits en `origin/main`, 0 en la rama).
