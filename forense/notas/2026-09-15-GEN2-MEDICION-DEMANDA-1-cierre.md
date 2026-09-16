# ACTO GEN2-MEDICION-DEMANDA-1 · cierre — dos tandas de la demanda, corridas: seis contratos de nube, seis corridas selladas en caja, seis `REPRODUCE`

**Acto:** `ACTO GEN2-MEDICION-DEMANDA-1` · 15/sep/2026 · CAJA (Ubuntu/WSL2, corpus compartido) · Opus · rama `acto/gen2-medicion-demanda-1` · worktree `/home/pc0/mm-gen2-medicion-demanda-1`
**Encargo:** `forense/encargos/2026-09-15-GEN2-MEDICION-DEMANDA-1.md` (A.3, verbatim, 0-bis `614929c`; lanzamiento de mesa «2 · CAJA», con **firma de contador con OBJETO embebida**, sin compuerta de merge).
**Insumo:** las specs que `ACTO GEN2-SPECS-DEMANDA-1` (NUBE, encargo 1) congeló, en dos tandas. **Tanda 1** (`COMMIT-1` `2cfc37e` de su rama, traído a esta caja **por cherry-pick, byte a byte** en `27c92c3`: 4 `spec.yaml` + 4 `spec.md` + 4 specs humanas selladas con sidecar; fusionada después como `PR #775`, `ADR-510`). **Tanda 2** (`PR #776`, fusionada ~17:00 UTC: `CALC-ENSANUT-0001` sobre la spec humana ya sellada `S7-L17 v1.1`, y `CALC-L8-CONVERSION-0001` con `L8-CONVERSION-PRESIDENCIAL-spec-v1_0`), tomada por merge de `origin/main`. Ninguna spec se editó. El encargo 1 declara que **sigue vivo con una tanda 3** (residuos de `CORR-0009`/`CORR-0007`); y un acto hermano, `GEN2-SPECS-DEMANDA-2` (`PR #781`, abierto), congeló cuatro specs más de otro perímetro.
**Base:** `2e25e6c` al abrir (PR #772) → `b983988` tras merge (PR #773) → `da9b47a` (PR #775, el encargo 1) → `62faadb` (PR #774, `GEN2-ADOPCION-VENTANILLA-3`, firma de `FP-375`) → `ca77b03` (PR #776, tanda 2 del encargo 1) al cerrar. Cinco merges; el último con conflicto en los cuatro archivos que ambos actos escriben (`decisiones.tsv`, `no-corrido.tsv`, `corridas.tsv`, `resultados.tsv`): los dos primeros resueltos con la convención de la casa (fila de `origin/main` primero, la propia después, verbatim); los dos derivados se tomaron de `origin/main` y se **re-derivaron** con `registro --verifica --escribe` (§3).
**Commits:** `614929c` (0-bis) · `77aabcb` (merge main) · `27c92c3` (COMMIT-1 del encargo 1, cherry-pick) · `d13529e` (COMMIT-1-bis: cuatro medidores congelados) · `13d303a`/`ea469c1`/`5ec2549`/`d2ce1be` (COMMIT-2 a/b/c/d: sellos) · `3ab7278` (firma en `decisiones.tsv`) · `89f2d2c` (registro) · `1e26c2d` (cascada) · `4a4fab0` (CONSUMIDO) · `b2e6ac8`/`6e3591c` (merge #774 + re-derivación) · `1cd5870` (merge #776, tanda 2) · `f055cc4` (COMMIT-1-bis tanda 2: dos medidores) · `dc996ed`/`285cd93` (COMMIT-2 e/f) · `1352b96` (firma tanda 2) · `44344cc` (registro) · cascada final.

---

## 0 · ARRANQUE, en cinco líneas

0.a `git rev-list --count HEAD..origin/main` = 0 (`2e25e6c`); +5 al consumir la tanda (PR #773), fusionados sin conflicto. 0.b árbol limpio. 0.c `ls-remote`/`worktree list`/`gh pr list` sin el rótulo. 0.d `limpia_arbol --reporta`: base al día, 1 rama fuera de política (`claude/amazing-noether-l1iegk`, la del encargo 1, todavía sin PR en ese momento). `data/raw` enlazada a `/home/pc0/mm-corpus/raw` (+ `raices.local.yaml` del clon padre). `tools/entorno.py`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · corpus=SI(examinados=413) · numpy 2.3.5 · pandas 2.3.3 · red=no-ejecutada` (este acto no descarga). Espejo: ninguna cifra sale de él.

## 1 · Qué llegó del encargo 1 y qué faltaba

Al arrancar, la rama del encargo 1 traía **cero specs** (sólo su 0-bis, 15:36 UTC). No fue PARO: el lanzamiento dice «arranca con la primera tanda, no espera a que termine entero». La tanda 1 cayó a las 16:02 UTC con cuatro contratos `D-15` completos (`spec.yaml` + `spec.md` + spec humana sellada con sha256) y **sin `medidor.py`** — el encargo 1 lo declaró como «se hizo distinto» (`NC-0192`): en nube, sin corpus y sin `numpy`/`pandas`, un medidor no probado contra ningún payload sería peor insumo que ninguno.

**Los cuatro medidores se escribieron aquí, contra el contrato, y se congelaron en un commit propio (`d13529e`) ANTES de abrir un solo valor.** Prueba previa al congelado, sin tocar el corpus: payloads sintéticos fabricados con la forma que cada spec declara (miembro anidado y BOM para ENIGH; `\r\n` y miembro bajo directorio para ENFIH; tres tablas con join de terna y de `folioviv` para EDER; `\r` solo como terminador para ENUT), `medir()` sobre `contrato_ejecutable(spec)` real, y `set(keys) == set(declarados)` + tipos con el mismo `_valida_outputs` de `tools/corrida0.py`: 4/4 sin problemas; guardia estructural (ZIP sin miembros) 4/4 con el conjunto completo de `RESULT` y `NO-ADOPTABLE-NO-ESTIMABLE`. Las columnas declaradas se verificaron por **metadato** (`data/inventario-reactivos-v1_2.tsv`, 178 247 filas): 0 faltantes en los ocho miembros, salvo `FAC_HOG` en `tvar_crea.csv`, que es exactamente el hallazgo A.15 que la spec ENUT pre-declara (`G-FAC-HOG-EN-TVAR-CREA = AUSENTE`, confirmado luego con el dato).

Lo que decide el **código** y no la spec quedó declarado en la cabecera de cada medidor para que se pueda refutar; lo material: (a) el share poblacional de mujeres 40+ (ENUT) se pondera con `FAC_PER` — la spec dice «ponderada» sin nombrar el ponderador, `FAC_HOG` sigue siendo el único ponderador de la razón, y sólo `FAC_PER` hace comparable el 0.2657 de GEN1 (reprodujo: 0.2657197); (b) en EDER, `A-N-SIN-CLASIFICAR` cuenta **todo** primer código fuera de LIBRE ∪ DIRECTO y al universo entran LIBRE, DIRECTO y el 37 declarado; una persona con `factor_per` no finito o negativo sale sin `RESULT` propio (la spec la nombra en `filtros` sin declararle uno) — resultó 0; (c) el IC se calcula sobre las filas del universo con diseño; si ninguna lo tiene, `NO-ESTIMABLE-DISENO-INCOMPLETO`.

`preflight` 4/4 `VERDE` (aviso esperado: `spec_md_no_esta_en_origin_main`, primera corrida de una spec aún no fusionada).

**Tanda 2 (`PR #776`), misma disciplina.** `CALC-ENSANUT-0001` declaraba **dos** bloqueos de preflight: el medidor (de CAJA) y `input_manifiesto_NO-VISIBLE-EN-ESTE-CONTEXTO` — el payload `adultos_ensanut2024_w.stata.stata.zip` vive bajo la raíz lógica `descargas_mx` (`/mnt/c`), que el sandbox de esta caja no lee (`FP-352`). Se resolvió por la vía de `LOTE-LAPOP`: espejo byte a byte a `/home/pc0/mm-corpus/descargas_mx_espejo/` (fuera del sandbox), identidad probada por `sha256 = 0fa8f443…` y `tamano_bytes = 4 196 284` contra `data/manifiesto.yaml`, y `descargas_mx` de `data/raices.local.yaml` (gitignorada) apuntada al espejo; `ejecucion.json` registra la raíz lógica, nunca la física. Antes de escribir el medidor se leyó **sólo metadato** del `.dta` (`pyreadstat … metadataonly=True`): 841 columnas, 12 924 filas, y la etiqueta de valor del bloque `a0927` es `{1: 'Sí', 2: 'No'}` — con eso el mapa de mención queda fijado por codebook, no supuesto. Medidor probado contra un `.dta` sintético escrito con `pyreadstat.write_dta` dentro de un ZIP (`_valida_outputs` 28/28; guardia estructural completa). `CALC-L8-CONVERSION-0001` es determinista sobre un artefacto **del repo** (`data/l8-resultados-tipo-boleta-v1_0.json`, `origen: repo`, verificado por sha256): su medidor se probó contra ese JSON real antes de congelarse — no es microdato, la spec lo cita verbatim — y contra un JSON vacío (guardia `NO-ESTIMABLE-INSUMO-DISCORDA`). Congelados en `f055cc4`; `preflight` 2/2 `VERDE`.

## 2 · Resultados por corrida (un COMMIT-2 por corrida, D-11 leído como GEN2)

### 2.1 · `CALC-ENIGH-0001` — `R5.1`, remesas ENIGH 2022, del lado de la regla (releva `CORR-0011`: `RES-0035`/`RES-0036`)

| `RESULT` | valor |
|---|---|
| `A-P` | **0.04569409956405095** — `A-REPRODUCE-GEN1 = REPRODUCE` (Δ +9.96e-08 vs 0.045694) y **`A-REPLICA-B0001 = REPLICA-RESULTADO` con Δ = 0.0 exacto** contra `CALC-B-0001` |
| `A-P-COMPLEMENTO` (contado) | 0.9543059004359491; `A-SUMA-UNO = SI` |
| `A-N-U` | **90 102** (Δ 0 vs GEN1 y vs `CALC-B-0001`); `A-N-SIN-PONDERADOR = 0`; `A-N-SIN-DISENO = 0`; `A-HOGARES-EXPANDIDOS = 37 560 123.0` (idéntico a B-0001) |
| IC95 de diseño (2 000 réplicas, seed 20260915) | **[0.043713, 0.047699]**, `IC-DE-DISENO` (560 estratos, 10 211 UPM, **0** con UPM única); `A-DELTA-IC-VS-B0001 = −1.15e-05` (semillas y réplicas distintas: lectura informativa) |
| estructura | 319 miembros, 126 columnas, llave `folioviv+foliohog` única, 0 nulos en `remesas`, `est_dis` ancho 3, `upm` ancho 7 |
| `A-ADOPCION` | `LISTADO-PARA-MESA-REPRODUCE` |

Lo que esta corrida añade a lo que `CALC-B-0001` ya tenía: el mismo punto **del lado de la regla** (sin `T9`), el complemento contado y la vía de adopción; no levanta la restricción de `T9` sobre el ensayo B.

### 2.2 · `CALC-ENFIH-0001` — `R1.2`, tenencia de Afore ENFIH 2019 (releva `CORR-0012`: `RES-0037`/`RES-0038`)

| `RESULT` | valor |
|---|---|
| `A-P` | **0.5385022873715912** — `REPRODUCE` (Δ +2.87e-07 vs 0.538502) |
| `A-P-COMPLEMENTO` | 0.46149771262840883; `A-SUMA-UNO = SI`; soporte de `C_AFORE` = `0:7568;1:10197`, 0 nulos |
| `A-N-U` | **17 765** (Δ 0); `A-HOGARES-EXPANDIDOS = 36 644 680.0` |
| IC95 de diseño | **[0.526825, 0.550261]**, `IC-DE-DISENO` (407 estratos, 3 270 UPM, 0 con UPM única); anchura −0.00048 vs GEN1 [0.5267, 0.550616] |
| `B-P` (`H_PPAL = 1`, sensibilidad) | **0.5400909603898933**, `B-N-U = 17 386` (Δ 0 vs GEN1 0.540091 / 17 386); IC [0.528278, 0.551880]; `B-DELTA-VS-A = +0.00159` |
| `C-PERFIL-CAT-POS` (descriptivo, no sellado) | `0: n=4354 p=0.383 · 1: n=8154 p=0.723 · 2: n=987 p=0.294 · 3: n=390 p=0.569 · 4: n=3428 p=0.416 · 5: n=452 p=0.352` |
| `A-ADOPCION` | `LISTADO-PARA-MESA-REPRODUCE` |

### 2.3 · `CALC-EDER-0003` — `R5.3`, tipo de PRIMERA unión, EDER 2017 (releva `CORR-0013`: `RES-0043`/`RES-0044`)

| `RESULT` | valor |
|---|---|
| censo | 886 976 filas persona-año · 23 831 personas en `antecedentes` · 23 548 viviendas; terna y `folioviv` únicas; `G-VEREDICTO-TIPO-CODIGO = CADENA-ENTERA` |
| conteos sin ponderar | `A-N-PRIMER-NO-CERO = 18 689` **COINCIDE** con L7; LIBRE **9 044** / DIRECTO **9 643** / sin clasificar **2** (el 37) → `A-CONTEOS-COINCIDEN-L7 = COINCIDE`; `A-CENSURA-IZQUIERDA = AUSENTE` |
| embudo | `A-N-U = 18 689`: 0 sin `factor_per`, 0 con `factor_per = 0`, 0 sin vivienda, 0 sin diseño; `A-PERSONAS-EXPANDIDAS = 45 443 693.0` |
| `A-P-LIBRE` | **0.4809714298527631**, IC95 de diseño **[0.469175, 0.492482]**, `IC-DE-DISENO` (0 estratos con UPM única) |
| `A-P-DIRECTO` (contado) | **0.518945786382282**; `A-SUMA-PARTICION = SI` (LIBRE + DIRECTO + peso del 37) |
| `B-COHORTE-P-LIBRE` (secundario) | `≤1970 = 0.3047 [0.2848, 0.3246] n 4 001 · 1971-80 = 0.3902 [0.3731, 0.4081] n 6 274 · 1981-90 = 0.5723 [0.5549, 0.5890] n 5 905 · 1991+ = 0.7729 [0.7521, 0.7923] n 2 509` |
| `A-DELTA-VS-GEN1` | `NO-APLICA-ESTIMANDO-DISTINTO` (constante declarada: GEN1 mide situación conyugal actual en ENADID 2023) |
| `A-ADOPCION` | `LISTADO-PARA-MESA` |

Soporte del primer código no-cero: `1:8646 · 2:4316 · 3:338 · 4:4934 · 12:142 · 13:17 · 14:54 · 17:173 · 18:7 · 26:19 · 27:19 · 28:1 · 37:2 · 46:7 · 47:6 · 48:3 · 126:5` — ningún código fuera del mapa. El gradiente de cohorte (0.30 → 0.77) es descriptivo y **no** sucede la segmentación sellada de `milpa/`.

### 2.4 · `CALC-ENUT-0001` — `R5.2`, reparto del cuidado ENUT 2024, estimador de razón (releva `CORR-0014`: `RES-0045`)

| `RESULT` | valor |
|---|---|
| `A-R` | **0.22148146779116093** — `REPRODUCE` al grano 4 (0.2215; Δ −1.85e-05) |
| IC95 de diseño de la razón (numerador y denominador de la misma réplica) | **[0.213152, 0.229784]**, `IC-DE-DISENO` (0 estratos con UPM única); GEN1 [0.213145, 0.229966] |
| `A-SHARE-POBLACIONAL-MUJERES-40MAS` (`FAC_PER`) | **0.2657196810038365** (GEN1 0.2657); `A-R-MENOS-SHARE = −0.0442` |
| universo | **29 181** hogares COINCIDE · 74 053 personas · 17 394 con carga · 11 557 sin mujer 40+ · **4 200** UPM · 0 sin `FAC_HOG` |
| guardas | `G-FAC-HOG-EN-TVAR-CREA = AUSENTE` (60 columnas) · **`G-FAC-HOG-TSDEM-IGUAL-THOGAR = IGUAL`** (la elección de archivo es inocua: hogar por hogar, 0 diferencias) · `G-FAC-PER-NO-CONSTANTE-EN-HOGAR = CONFIRMADO` · `G-DISENO-CONSTANTE-EN-HOGAR = SI` · 0 nulos en las cuatro `CON_CP` |
| secundarios | `C-P-RESIDUO-15A59 = 0.1576` (el recorte declarado pesa **15.8 %** de las horas si se incluyera) · `C-P-SIN-CP = 0.1980` · `C-DELTA-CON-CP-VS-SIN-CP = +0.0235` |
| `A-ADOPCION` | `LISTADO-PARA-MESA-REPRODUCE` |

La guarda nueva del encargo 1 (§2.1 de su mapa) **muerde en la lectura y no en la cifra**: `FAC_HOG` de `tsdem.csv` y de `thogar.csv` son iguales en los 29 181 hogares, así que el texto de `milpa/tramite.yaml:1036` («`FAC_HOG` … en `tvar_crea.csv`») sigue siendo falso en la letra (`NC-0196`) sin haber movido el número.

### 2.5 · `CALC-ENSANUT-0001` — `S7-L17` Rama B, razón de no vacunación ENSANUT 2024 (releva `CORR-0017`: `RES-0063`/`RES-0064`)

| `RESULT` | valor |
|---|---|
| `A-P-LOGISTICA` (unidad = mención) | **0.7777616409222661** — `REPRODUCE` (Δ −3.6e-07 vs 0.777762) |
| `A-P-NO-LOGISTICA` (contado) | 0.22223835907773398; `A-SUMA-UNO = SI` |
| embudo | **254** menciones / **179** personas / 49 con más de una mención; desglose `152;28;16;47;11` → `A-DESGLOSE-COINCIDE-GEN1 = COINCIDE`; 0 sin ponderador, 0 sin diseño; 257 428 celdas ausentes del bloque (NaN = no respondió, fuera de todo) |
| soporte del bloque, antes del mapa | `1:254; 2:798` (sólo Sí/No, como el codebook) |
| IC95 de diseño por `est_sel` (2 000 réplicas) | **[0.707920, 0.839468]**, `IC-CON-ESTRATOS-DE-UPM-UNICA` (**30** estratos con UPM única → límite inferior); GEN1 estratificó por `estrato` urbanidad y publicó [0.672777, 0.857561] |
| `B-P-PERSONA` (secundario) | **0.8563813**; `B-DELTA-MENCION-VS-PERSONA = −0.0786` — la elección de unidad vale **7.9 pp**: `ponde_f` es de persona y la primaria lo aplica a menciones (hallazgo A.15 del encargo 1, ahora con cifra) |
| `C-P-POR-VACUNA` | Influenza 0.618 (n 118) · Neumococo 0.856 (52) · Tétanos 0.903 (43) · Otra 0.824 (41) |
| `A-ADOPCION` | `LISTADO-PARA-MESA-REPRODUCE` |

### 2.6 · `CALC-L8-CONVERSION-0001` — conversión presidencial, tres celdas derivadas (releva `CORR-0016`: `RES-0050/0051/0052`)

| `RESULT` | valor |
|---|---|
| insumo | `G-SHA256-INSUMO = COINCIDE` (`30f3e16d…`); 40 medias, 0 ausentes; `beta_pres_pp = 4.016715486813227` → `delta = 0.040167` |
| anclas | `p0` mín 0.305096 · máx 0.710438 · media 0.579663 · mediana 0.609369 → `G-ANCLAS-COINCIDEN-GEN1 = COINCIDE` al grano 4 |
| `A-P-MINIMO / MAXIMO / MEDIA` | **0.345267 / 0.750567 / 0.619867** — `REPRODUCE` exacto (Δ 0.0 en las tres); `A-CLIP-ACTIVO = NO` |
| grano (hallazgo del encargo 1, verificado) | `con_ancla_r4 = 0.345267;0.750567;0.619867 · sin_redondear = 0.345263;0.750605;0.619830 · diferencia_max = 3.8e-05` — sin el redondeo del ancla a 4 decimales las celdas **no** reproducen |
| riesgo declarado | `C-IC-BETA-ROZA-CERO = SI` (IC95 wild-cluster [0.049, 7.887] pp, p 0.0413, 9 conglomerados); vía intermedia `CONTIENE-CERO = SI`, no se reabre |
| `A-ADOPCION` | `LISTADO-PARA-MESA-REPRODUCE` — rotulado `DERIVADO-ECOLOGICO`, no causal |

## 3 · Verify, sello y registro

Cada corrida: `run` exit 0 → `sella_sha256` SELLADO → `verify` **REPRODUCE · CONTEXTO=IDENTICO**, y un segundo `verify` aislado tras el último commit de cada tanda: **12/12 REPRODUCE**. Sellos: `CALC-ENIGH-0001` `4f8517e9…`, `CALC-ENFIH-0001` `dd2e92cc…`, `CALC-EDER-0003` `9d6d0533…`, `CALC-ENUT-0001` `fe50e5e8…`, `CALC-ENSANUT-0001` `66dfa413…`, `CALC-L8-CONVERSION-0001` `3d16bc12…` (cubren `spec.yaml`, `medidor.py`, `ejecucion.json`, `resultados.json`). Inputs resueltos por hash: `3b2b0bc9…` (ENIGH 2022), `be372533…` (ENFIH 2019), `bcc7eb90…` (EDER 2017), `25f35626…` (ENUT 2024), `0fa8f443…` (ENSANUT 2024 adultos, raíz `descargas_mx`), `30f3e16d…` (JSON de L8, repo) más los FD y las specs selladas.

**Firma de contador con OBJETO.** El lanzamiento la trae verbatim («Firma de contador con OBJETO embebida desde el lanzamiento — para no repetir el hueco de FP-375 …»); autoridad mesa, fecha 15/sep/2026, OBJETO = cada corrida sellada aquí sobre spec del encargo 1. Se escribió como **seis filas en `data/corrida0/decisiones.tsv`** (`3ab7278` y `1352b96`) citando ese párrafo; `_cuenta_gen2_resuelto` da precedencia a `decisiones.tsv` sobre la etiqueta `PENDIENTE-DE-MESA` que traen los cuatro `spec.yaml` del encargo 1 (que **no se editan**, E.3). Registro: las seis `OFERTA · SELLADA · GEN2 · cuenta_gen2=SI · «decision de mesa (decisiones.tsv)»`. El merge de mesa perfecciona la firma. Esto cierra por producto `NC-0192` (medidores) y `NC-0198` (firma), fusionadas con `PR #775` a mitad de este cierre.

**Registro (`corrida0 registro --verifica --escribe`), tres pasadas y una re-derivación.** Sobre la base `b983988`: primera pasada `PARO · REPLAY-PISADO (NC-0094)` por `CALC-M-marco-M-sorteado-v1_3` (proyectó `NO-REPRODUCE · CONTEXTO-DISTINTO`); `verify` aislado 2/2 → `REPLICA-RESULTADO · CONTEXTO-DISTINTO`: el mismo veredicto inestable in-process que `NC-0182` ya asienta; **no se nombró en `--lote`** y la segunda pasada escribió con cero pisadas (`89f2d2c`). Al fusionar `PR #774` (`62faadb`) los dos derivados entraron en conflicto: se tomaron de `origin/main` y se re-derivaron. Esa base traía **11 corridas ajenas con `resultado_replay`/`contexto_replay = NO-VERIFICADO`** (`CALC-B-MARCO-{ENCIG,ENIGH,ENVIPE,MAE}-0001`, `CALC-EDER-0001/0002`, `CALC-ENIF-0003`, `CALC-ENVIPE-U4-2012` y `-v1_1`, `CALC-F5-REANALISIS-0001`, `CALC-SHED2025-BNPL-DANO-0001`) — el blanqueo que `NC-0094` describe, producido por una re-derivación sin `--verifica` o desde un entorno donde no ejecutan. La pasada con `--verifica` de esta caja las **llena** (`NO-VERIFICADO → REPRODUCE · IDENTICO`, 22 campos); es transición legítima y se autorizó nombrándolas en `--lote` con esta causa (tercera pasada, exit 0).

Escrito: `corridas.tsv` **174 filas** (las cuatro filas sin sufijo de commit que `PR #775` registró como spec-sin-corrida pasan a sus ids sellados `CALC-…--<commit>`), `resultados.tsv` 4 743 → **4 862** (+119 `RESULT`: 26 + 31 + 33 + 29), `usos.tsv` **207 filas, mismo conjunto de (resultado, consumidor, tipo) y misma aptitud que `origin/main`** (cero adopciones, probado). **Pisadas medidas contra `origin/main` = `62faadb`, columna por columna, excluyendo las cuatro filas propias:** `fuente_replay` pasa de `HEREDADO-DEL-REGISTRO-PUBLICADO`/`VERIFY-CITADO-DE-NOTA-DE-CIERRE` a `VERIFY-EN-ESTA-SESION` en 79 corridas / 3 303 `RESULT` / 16 usos — la pisada inevitable de `--verifica` (se declara, no se evita: la alternativa borra veredictos); `resultado_replay` y `contexto_replay` en las 11 corridas del `--lote` (llenadas, arriba); ninguna otra columna de ninguna fila ajena cambia. **Cuarta pasada, tras fusionar `PR #776` y sellar la tanda 2** (`44344cc`, exit 0, sin `--lote`: las 11 ya venían llenas de la pasada anterior): `corridas.tsv` 174, `resultados.tsv` **4 913** (+51: 28 + 23), `usos.tsv` 207 con el mismo conjunto y aptitud; pisadas ajenas idénticas a las ya declaradas (`fuente_replay` en 79/3 303/16 y las 11 llenadas).

## 4 · Contador, sin adornos

`python3 tools/corrida0.py status`, antes → después. Dos bases, porque `PR #774` fusionó a mitad del cierre y firmó `FP-375` (+3 corridas ajenas al contador: `CALC-EDER-0002`, `CALC-ENVIPE-U4-2012-v1_1`, `CALC-ENIF-0003`; `-U4-2012` v1.0 superada): sobre la base de arranque `b983988` la tanda 1 movió **63 → 67**; sobre la base de cierre `ca77b03` (PR #776; medida en un worktree limpio de `origin/main`, idéntica en estos contadores a `62faadb`) las dos tandas mueven **66 → 72**:

| contador | `origin/main` = `ca77b03` | este acto | Δ |
|---|---|---|---|
| `N_corridas_requeridas` | 82 | 82 | 0 |
| **`N_corridas_selladas`** | **66** (63 antes de #774) | **72** | **+6** (`CALC-ENIGH-0001`, `CALC-ENFIH-0001`, `CALC-EDER-0003`, `CALC-ENUT-0001`, `CALC-ENSANUT-0001`, `CALC-L8-CONVERSION-0001`, todas `cuenta_gen2 = SI` por la firma del lanzamiento) |
| **`N_resultados_gen2_sellados`** | **3 085** (2 882 antes de #774) | **3 255** | **+170** (119 + 51) |
| `N_resultados_gen2_adoptados_activos` | 16 | 16 | 0 (sellar no es adoptar, E.2) |
| `corredores_envueltos_legacy` | 18 | 18 | 0 (las seis son GEN2 limpias: microdato o artefacto de repo + spec sellada + FD como inputs) |
| `no_corrido_abiertas` | — | — | −2 +2 (cierra `NC-0192`/`NC-0198`, abre `NC-0204`/`NC-0205`) |

Demanda relevada: **6 de las 19 `CORR` sin candidato** (`CORR-0011`, `CORR-0012`, `CORR-0013`, `CORR-0014`, `CORR-0016`, `CORR-0017`), **12 de los 94 `RESULT`** de demanda (`RES-0035/0036`, `RES-0037/0038`, `RES-0043/0044`, `RES-0045`, `RES-0050/0051/0052`, `RES-0063/0064`). Los seis puntos adoptables **reproducen GEN1** al grano que GEN1 publicó (o replican `CALC-B-0001` exacto) y los de microdato nacen con IC de diseño; ninguno mueve una cifra de `milpa/` — la adopción es de mesa. El lanzamiento decía «de 63 hacia 82»: este acto recorre 6 de los 19 escalones, que son exactamente los contratos del encargo 1 que existían al cerrar; de los 13 restantes, 2 son la tanda 3 del encargo 1 (residuos de `CORR-0009`/`CORR-0007`, construibles), 4 tienen contrato en `PR #781` (`GEN2-SPECS-DEMANDA-2`, otro acto y otro OBJETO), y 6 esperan las tres decisiones de mesa que el encargo 1 dejó armadas (`NC-0197`).

## 5 · Lo que este acto no hizo

- **No corrió la tanda 3** del encargo 1 (residuos de `CORR-0009` `RES-0031/0032/0065` y de `CORR-0007` `RES-0025/0026`): sus contratos no existen todavía (`NC-0193`, «el encargo sigue VIVO con la tanda 3»). Sucesor: `ACTO GEN2-MEDICION-DEMANDA-2`, con la misma firma de contador (el OBJETO del lanzamiento cubre «todas las corridas cuya spec el encargo 1 vaya congelando»).
- **No corrió las cuatro specs de `PR #781`** (`ACTO GEN2-SPECS-DEMANDA-2`: `CALC-DINERO-FAMILIARES-VEJEZ-0001`, `CALC-EVASION-NORMA-0001`, `CALC-HORIZONTE-VIA-DERIVADOS-0001`, `CALC-TIENE-AHORROS-0001`): son de otro acto y de otro encargo; la firma de contador de este lanzamiento nombra al encargo 1 y no se estira. Además `PR #781` está abierto y colisionó con este acto en `ADR-511` y `NC-0200..0203`: fusionó primero, este acto renumeró a `ADR-512` y `NC-0204`/`NC-0205`.
- **No adoptó nada**: `milpa/` intocado; `usos.tsv` se compara contra la base en §3.
- **No editó ninguna spec ni `spec.yaml` del encargo 1** (E.3): las seis etiquetas `cuenta_gen2: PENDIENTE-DE-MESA` siguen en su `COMMIT-1`; la firma vive en `decisiones.tsv`, que es donde el registro la lee primero.
- **Cerró `NC-0192`/`NC-0198`** en `forense/no-corrido.tsv` por producto (los seis medidores existen y las seis firmas están en `decisiones.tsv`), una vez que `PR #775`/`#776` fusionaron y las filas entraron a este árbol.
- **No descargó nada**; cero llamadas a modelos; cero cambios al motor.

D-6 aplicado: el acto se declara `ACTO GEN2-MEDICION-DEMANDA-1` en todo archivo que escribe.
