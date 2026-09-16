# ACTO GEN2-MEDICION-DEMANDA-2 · cierre — dos tandas del mapa-19 corridas en caja: siete sellos, seis corridas vigentes con cifra, cuatro sucesiones de cableado y un blanco que se escribía `NA`

**Acto:** `ACTO GEN2-MEDICION-DEMANDA-2` · 15/sep/2026 · CAJA (Ubuntu/WSL2, corpus compartido) · Opus · rama `acto/gen2-medicion-demanda-2` · worktree `/home/pc0/mm-gen2-medicion-demanda-2`
**Encargo:** `forense/encargos/2026-09-15-GEN2-MEDICION-DEMANDA-2.md` (A.3, verbatim, 0-bis `bac2894`; lanzamiento de mesa «CAJA — ACTO GEN2-MEDICION-DEMANDA-2», con **firma de contador con OBJETO embebida** verbatim, sin compuerta).
**Insumo:** **tanda 1** = las specs `SPEC-FIJADA` del mapa-19 que `ACTO GEN2-SPECS-DEMANDA-2` congeló en `PR #781` (cuatro, no tres: ver §1); **tanda 2** = las dos que `ACTO GEN2-FIRMAS-MESA-1` congeló en NUBE (`PR #785`, fusionado a las ~19:20 UTC mientras corría la tanda 1; tomado por merge de `origin/main`, conflicto sólo en `decisiones.tsv`, resuelto con la convención de la casa: fila de origin primero, la propia después, verbatim).
**Base:** `582d4e9` (merge de `#779`) al abrir → `5973f12` (`#785`) → `aab1eed` (`#787`) → `48cb08c` (`#782/#783/#786/#788/#790`) → `4acdae2` (`#784`) → `8f9fb51` (`#791`) al cerrar. Cinco merges; el tercero con conflicto en `gobernanza`, `estado-programa`, `registro-rotulos` y `no-corrido` (resueltos: texto de origin primero, el propio después, renumerado) y los tres TSV derivados tomados de origin y re-derivados.
**Commits:** `bac2894` (0-bis) · `fb43c8b` (COMMIT-1 tanda 1: tres `v1_1`) · `67cedcb`/`c6c9c95`/`25937a8` (COMMIT-2 a/b/c) · `6c9a265` (COMMIT-1-bis: `HORIZONTE-v1_1`, tras sellar al padre) · `d3c0e1f` (COMMIT-2d) · `ae19768` (firma tanda 1) · `4eaefc9` (merge #785) · `dc25f3d` (COMMIT-1 tanda 2: dos medidores) · `57f25d1` (COMMIT-2e) · `895e1aa` (COMMIT-2f, `NO-ESTIMABLE`) · `453d6b4` (COMMIT-1-ter: `ENCIG-2023-v1_1`) · `885b911` (COMMIT-2g) · `7138872` (firma tanda 2) · `db0e452` (registro) · cascada.

---

## 0 · ARRANQUE, en cinco líneas

0.a `git rev-list --count HEAD..origin/main` = 0 (`582d4e9`). 0.b árbol limpio. 0.c `ls-remote`/`worktree list`/`gh pr list` sin el rótulo (el único hit de `--search` fue `#782`, de adquisición). 0.d `limpia_arbol --reporta`: base al día, 1 rama fuera de política (`claude/epic-thompson-wbbmg7`, la de `FIRMAS-MESA-1`, entonces sin PR). `data/raw` enlazada a `/home/pc0/mm-corpus/raw` + `data/raices.local.yaml` del worktree predecesor (`descargas_mx` → espejo). `tools/entorno.py --sonda-red`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · red=200 · corpus=SI(examinados=413) · python 3.14.4 · numpy 2.3.5 · pandas 2.3.3`. Espejo del proyecto: ninguna cifra sale de él. Gotcha de caja: el sandbox negó la escritura de `.git/config` del clon padre al primer `push -u` (el push sí entró; `ls-remote` lo confirmó) — el tracking se fijó después, cuando la caja abrió esa ruta.

## 1 · Lo que el lanzamiento suponía y lo que el árbol tenía (A.8)

**(a) Cuatro specs, no tres.** `awk '$4=="SPEC-FIJADA"' corridas.tsv` devolvió `CALC-DINERO-FAMILIARES-VEJEZ-0001`, `CALC-EVASION-NORMA-0001`, `CALC-HORIZONTE-VIA-DERIVADOS-0001`, `CALC-TIENE-AHORROS-0001`. El lanzamiento nombra tres; `EVASION-NORMA` (`CORR-0007`, `RES-0025/0026`) es del mismo `PR #781`, de la misma clase (registro D-15 de una medición ya sellada en `milpa/`) y es fila del mapa-19. El OBJETO de la firma dice «toda corrida que este acto selle sobre spec congelada del mapa-19»: **se corrió también**, como lectura del ejecutor, declarada en el encargo (2.a) y aquí, y con reserva para mesa (`NC-0223`). Si mesa la excluye, se retira su fila de `decisiones.tsv`; el sello queda.

**(b) Ninguna de las cuatro podía correr tal como estaba congelada.** Tres defectos de cableado, ninguno de contenido: (1) las cuatro carpetas venían **sin `spec.md`** (el `spec.yaml` lo nombra por sha256 = el de la spec humana en `prereg-caja/`, pero no lo trae) → `preflight` `BLOQUEADO ausente=…/spec.md` 4/4; (2) tres `script:` apuntan a **scripts legados de `tools/` que no exponen `medir(inputs, contrato)`** (`medidor_ahorro_enif24.py`, `tasas_base_fase1.py`, `medidor_evasion_norma_envipe25.py`; el mapa-19 decía «CAJA · escribir medidor.py», pero un `medidor.py` en la carpeta no corre si `script:` no lo nombra); (3) `HORIZONTE-VIA-DERIVADOS` declaraba `sha256: LEER-AL-EJECUTAR -- …` en sus dos inputs `repo`, que `preflight` lee como `DISCORDA` y bloquea siempre.

**Consecuencia, E.3 (lo congelado no se edita): cuatro sucesiones `v1_1`** en carpeta propia, `repite_de` en la raíz (el registro marca la `v1_0` `SUPERADO→v1_1`), `spec.md` presente, sha reales, `script:` al `medidor.py` propio, y **contrato verbatim** (universo, variables, ponderador, transformación, estimando, parámetros, tolerancia, ids de `RESULT`). Los tres medidores de transcripción **no reimplementan nada**: importan por ruta el script legado que la `v1_0` nombra y reutilizan su cargador y su estimador (`carga()`/`estima()` → `wprop_ic_conglomerado`, seed 42, 10 000 réplicas; `wprop_ic_bootstrap` con `random.Random(42)` para `tasas_base_fase1`), cambiando **sólo la ruta del payload** por la que `preflight` resolvió (P1); verifican que seed/réplicas del contrato igualan los defaults del legado y PARAN si no. Cada `v1_1` se congeló en commit propio antes de abrir un valor, probada contra ZIP sintético (columnas declaradas, valores fabricados) con `contrato_ejecutable()` y `_valida_outputs` reales: 3/3 + guardia estructural 3/3. `HORIZONTE-v1_1` se congeló **después** de sellar a su padre (`TIENE-AHORROS-v1_1`, `CORR-0009`) y toma ese `resultados.json` como input por sha256: el `DEPENDE-DE-CORRIDA-PADRE` quedó mecánico. Sus seis insumos salen **todos de `RESULT` sellados en corrida0** (`CALC-ENIF-0001` trae también `B-P-FORMAL-P`/`B-P-INFORMAL-P` = `A_solo_formal`/`B_solo_informal`, que `milpa/tramite.yaml:1214-1215` cita como su fuente), con guardia `NO-ESTIMABLE-INSUMO-CAMBIO` sobre `parametros.insumos_esperados` (tolerancia 1e-6). `milpa/` no se lee en tiempo de corrida.

**(c) Tanda 2, misma disciplina.** `CALC-ENCIG-2023-0001` y `CALC-ENVIPE-DENUNCIA-SEGURO-0001` llegaron bien formadas (`spec.md` presente, sha reales), sólo `script_ausente`: los dos `medidor.py` se escribieron aquí contra el contrato, sin tocar el `spec.yaml`, y se congelaron en `dc25f3d` tras 7/7 pruebas sintéticas (incluidas: sec_8 con `ID_TRA` duplicada → `NO-ESTIMABLE-LLAVE-NO-UNICA`; `P8_4` con código 2 → `FUERA-DE-MAPA`; ZIP sin catálogos → `CONTRADICE:catalogo-ausente`). Lo abierto antes de congelar: lista de miembros, cabeceras, los cuatro catálogos de ENVIPE (codebook, E.5). Lo que decide el **código** quedó en la cabecera de cada medidor: ENCIG — join por `ID_TRA` con la llave de control `(ID_VIV, ID_PER, ID_TRA, N_TRA)` computada en paralelo y comparada por conjunto de filas; `B-ADOPCION = CON-RESERVA` si `B-COBERTURA < 0.5`; ENVIPE — **bootstrap conjunto** sobre los conglomerados de U (CON, SIN y su diferencia salen de las mismas 2 000 réplicas: la spec pide IC de la diferencia, que dos bootstraps separados no dan); replay independiente por orden de llave con `math.fsum`.

## 2 · Resultados por corrida (un COMMIT-2 por corrida, D-11 leído como GEN2)

### 2.1 · `CALC-TIENE-AHORROS-0001-v1_1` — tenencia de ahorro ENIF 2024 (`CORR-0009` `RES-0031/0032`; **CORR-0009 AGOTADA 9/9**)

| `RESULT` | valor |
|---|---|
| `A-P-TIENE` | **0.6420795665818781** — `A-RELEVA-SELLADO = SI` (Δ −4.3e-07 vs 0.642080) |
| `A-P-NO-TIENE` | 0.35792043341812185; `A-SUMA-UNO = SI:0.000e+00` |
| IC95 (conglomerado EST_DIS×UPM_DIS, 10 000, seed 42) | **[0.630602, 0.653440]** — idéntico al grano publicado |
| `G-N-PERSONAS` / `G-NUMERADOR` | **13 502 / 8 699** (exactos) |

### 2.2 · `CALC-EVASION-NORMA-0001-v1_1` — evasión de norma ENVIPE 2025, unidad delito (`CORR-0007` `RES-0025/0026`)

| `RESULT` | valor |
|---|---|
| `A-P-EVADE` | **0.5627744787844097** — `RELEVA-SELLADO = SI` (Δ +4.8e-07 vs 0.562774) |
| `A-P-CUMPLE` | 0.43722552121559033; suma `SI` |
| IC95 | **[0.551982, 0.573448]** — idéntico |
| `G-N-DELITOS` / `G-NUMERADOR` | **40 280 / 21 761** (exactos) |

### 2.3 · `CALC-DINERO-FAMILIARES-VEJEZ-0001-v1_1` — dinero de familiares para la vejez ENIF 2024 (`CORR-0010` `RES-0033/0034`; **AGOTADA 2/2**, identidad por hash A.7)

| `RESULT` | valor |
|---|---|
| `A-P-RECIBE` | **0.4577065669362348** — `RELEVA-SELLADO = SI` (Δ −4.3e-07 vs 0.457707) |
| `A-P-NO-RECIBE` | 0.5422934330637652; suma `SI` |
| IC95 (bootstrap simple, `random.Random(42)`, 10 000) | **[0.444232, 0.470782]** — idéntico |
| `G-N-PERSONAS` | **11 895** (exacto; es el `n` tras `P9_9_4 ∈ {1,2}` y `FAC_PER` válido, como el legado lo devolvió) |

### 2.4 · `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` — siete derivados deterministas (`CORR-0015` **completa**: `RES-0047/0049/0053/0054/0055/0056/0066`)

| `RESULT` | valor | legacy | Δ |
|---|---|---|---|
| `A-HORIZONTE-NO-CORTO-SIN-SS` | 0.458657 | 0.458657 | 0 |
| `A-HORIZONTE-NO-CORTO-CON-SS` | 0.626870 | 0.626870 | 0 |
| `A-HORIZONTE-NO-CORTO-NO-TRABAJA` | 0.367218 | 0.367218 | 0 |
| `A-AMBAS-VIAS` | 0.20476743 | 0.204767 | +4.3e-07 |
| `A-SOLO-FORMAL` | 0.08015957 | 0.080160 | −4.3e-07 |
| `A-SOLO-INFORMAL` | 0.35715257 | 0.357153 | −4.3e-07 |
| `A-NO-AHORRA` | 0.35792043 | 0.357920 | +4.3e-07 |
| `A-SUMA-UNO-VIA` | `SI:0.000e+00` | | |

Los 4.3e-07 son el redondeo de `milpa/` a 6 decimales: la `v1_1` toma `tiene_ahorros` **sin redondear** del sello del padre (0.6420795666) en vez del 0.642080 de `milpa/`. Dentro de la tolerancia 1e-6 de la spec.

### 2.5 · `CALC-ENVIPE-DENUNCIA-SEGURO-0001` — denuncia por cobertura de seguro, robo total de vehículo, ENVIPE 2025 (`CORR-0007` `RES-0039..0042`; **CORR-0007 AGOTADA 8/8** junto con 2.2 y `CALC-ENVIPE-0001`)

| `RESULT` | valor |
|---|---|
| universo | **U 1 016 · CON 402 · SIN 614** — `DELTA-N-VS-GEN1 = U:+0;CON:+0;SIN:+0`; `G-PARTICION-ESTRATOS = SI`; `G-LLAVE-DELITO = ID_DEL`; catálogos `CONFIRMA` 3/3; soporte `BP2_1` en BPCOD=01 `1:402;2:614;9:12`; `BP1_20` `1:692;2:336` |
| `CON-P-DENUNCIA` | **0.7909064453831163**, IC95 **[0.749985, 0.831673]**, EE 0.0208 (GEN1 0.7909, IC [0.752301, 0.827811]) |
| `CON-P-NO-DENUNCIA` (contada) | 0.20909355461688375; `CON-SUMA-UNO = SI` |
| `SIN-P-DENUNCIA` | **0.6720144369290082**, IC95 **[0.636621, 0.704492]**, EE 0.0176 (GEN1 0.672, IC [0.642490, 0.701624]) |
| `SIN-P-NO-DENUNCIA` (contada) | 0.3279855630709918; suma `SI` |
| `DELTA-CON-MENOS-SIN` | **+0.1189**, IC95 **[0.0637, 0.1716]** (descriptivo, no causal; GEN1 declaró 11.9 pp) |
| diseño | 368 estratos / 909 UPM en U, **191 con UPM única** → `IC-CON-ESTRATOS-DE-UPM-UNICA` (límite inferior de anchura); `G-REPLAY-INDEPENDIENTE = REPLICA` |
| `REPRODUCE-GEN1` | **`NO-REPRODUCE`** → `ADOPCION = LISTADO-PARA-MESA-NO-REPRODUCE`. **Atribuido, no aceptado:** `DELTA-VS-GEN1 = RES-0039:+0.000006445; RES-0040:−0.000006445; RES-0041:+0.000014437; RES-0042:−0.000014437`. La spec fija `grano_gen1_decimales: 6` sobre valores legacy que sólo tienen **4** (0.7909 / 0.672, rellenados a 0.790900 / 0.672000 en `demanda-resultados.tsv`); al grano 4 los cuatro `round(p, 4)` coinciden (0.7909 / 0.2091 / 0.6720 / 0.3280) y los `n` son exactos. Es un `NO-REPRODUCE` de grano, no de cifra. El medidor no se tocó («NO-REPRODUCE no autoriza tocar el medidor»); la decisión es de mesa (`NC-0221`). |

### 2.6 · `CALC-ENCIG-2023-0001` (v1_0) — primer resultado: **`NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:P8_4`**

`G-SOPORTE-P84 = 0:120514;1:4540;FUERA:1082892`, `G-SOPORTE-P73 = 1:69342;…;9:1075;FUERA:5716`. El ZIP de 2023 escribe el blanco como el literal **`NA`** (exportación estilo R; en 2025 era campo vacío), y el medidor congelado sólo reconocía `''`/`b`: trató `NA` como texto fuera de mapa, como su cabecera declaraba. Todo lo demás salió: `G-VEREDICTO-JOIN = JOIN-EXACTO`, `G-JOIN-LLAVE-CONTROL-COINCIDE = COINCIDE`, `G-LLAVE-SEC8-IDTRA-UNICA = UNICA`, `G-PONDERADOR-POR-ARCHIVO = FAC-TRA-DE-SEC7-Y-FAC-P18-SIN-USAR`, 123 186 / 1 207 946 filas, 52 / 26 columnas, `G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA = UNICA` con `ID_TRA` sola `NO-UNICA:112219/123186` (7 644 repetidos — el mismo patrón que 2025). **El primer resultado es el que se reporta:** se selló (`895e1aa`), y se sucedió con `v1_1` en vez de corregir hacia atrás.

### 2.7 · `CALC-ENCIG-2023-0001-v1_1` — mordida por canal ENCIG 2023 (`CORR-0001`, D1 opción (b); **candidatura para mesa**)

Único cambio respecto a la v1_0: `parametros.codificacion.blanco_literal: ["", "b", "NA"]` declarado en la spec y leído por el medidor (el mapa de códigos `{0,1}` / `{1..9}` no se toca). Control: sobre un ZIP sintético con `NA`, la v1_0 da `FUERA-DE-MAPA` y la v1_1 `TASA-REPORTADA`.

| `RESULT` | valor |
|---|---|
| `B-P-PRE-SD` **[PRIMARIO]** | **0.13079648341932204**, IC95 **[0.112386, 0.150883]** — n 10 852 eventos, 299 estratos / 2 797 UPM, 50 con UPM única |
| `B-P-DIG-SD` **[PRIMARIO]** | **0.02340709180348316**, IC95 **[0.018516, 0.029056]** — n 6 005, 286 / 2 288, 51 con UPM única |
| `B-P-NORMAL-*` (contados) | 0.8692035 / 0.9765929; `B-SUMA-PRE-SD = SI`, `B-SUMA-DIG-SD = SI` |
| `H1-VEREDICTO` | **`H1-SOSTENIDA`** (`B-DIFERENCIA-PRE-DIG-SD = +0.1074`, razón 5.59; asociación, no causal) |
| contraste de ola (`CONTRASTE-DE-OLA-NO-SERIE`) | `B-DELTA-2023-VS-2025-PRE-SD = −0.0102` (0.1308 vs 0.1410) · `-DIG-SD = −0.0065` (0.0234 vs 0.0299) — «cuánto difiere esta ola de aquella», nunca «cuánto cambió la mordida» |
| rama CD (secundaria) | `B-P-PRE-CD` 0.1095 (n 9 680) · `B-P-DIG-CD` 0.0223 (n 5 259); 1 918 eventos descartados por dedup |
| canal | `B-N-RESIDUO-CANAL = 6 243`, `B-P-RESIDUO-CANAL = 0.2547` → `DICOTOMIA-ES-PROPIEDAD-DEL-RECORTE` (H3 sostenida) |
| universo | `G-UNIVERSO-DECLARADO = ENTIDADES:32;EST_DIS:347;UPM_DIS:8900;AREAS:NO-DECLARADA-EN-SPEC` (la estampa «82 áreas urbanas» de 2025 no se transporta) |
| `B-ADOPCION` | `LISTADO-PARA-MESA-ESTIMABLE` — **con reserva que la spec no pudo prever (`NC-0222`):** `B-COBERTURA = 1.0` porque el `sec_8` de 2023 trae fila (con `P8_4 = NA`) para **todo** trámite, así que «emparejadas/filas de sec_7» ya no mide la autoselección de 8.3; ésta se ve en `B-N-P84-BLANCO = 100 086` → cobertura efectiva `B-N-U / G-N-FILAS-SEC7 = 23 100 / 123 186 = 0.19`, la misma que 2025 (0.20). Por la regla del código (umbral 0.5 sobre `B-COBERTURA`) salió `ESTIMABLE`; leído con la cobertura efectiva sería `CON-RESERVA`. El estimando es condicional al grupo observado por 8.3, como en 2025. |

## 3 · Verify, sello, firma y registro

Cada corrida: `preflight VERDE` → `run` exit 0 → `sella_sha256 SELLADO` → `verify` **REPRODUCE · CONTEXTO=IDENTICO** ×2 antes de su commit: **14/14**. Sellos: `TIENE-AHORROS-v1_1` `73a703d5…` · `EVASION-NORMA-v1_1` `8076d9ff…` · `DINERO-FAMILIARES-VEJEZ-v1_1` `b9586ca8…` · `HORIZONTE-VIA-DERIVADOS-v1_1` `1c8b329f…` · `ENVIPE-DENUNCIA-SEGURO` `7126e2b0…` · `ENCIG-2023` `e2cf69ee…` · `ENCIG-2023-v1_1` `0bacf574…`. Payloads por hash: `00e4b0b4…` (ENIF 2024, ×2), `8a7a99fd…` (ENVIPE 2025, ×2), `af733d86…` (ENCIG 2023, ×2); inputs `repo` por sha (specs humanas, `resultados.json` de `ENIF-0001`/`ENIF-0002`/`TIENE-AHORROS-v1_1`).

**Firma de contador con OBJETO.** El lanzamiento la trae verbatim («FIRMA DE MESA, mesa, 15 de septiembre de 2026 — OBJETO: cuenta_gen2 = SI para toda corrida que este acto selle sobre spec congelada del mapa-19; no adopta al motor.»). **Siete filas en `data/corrida0/decisiones.tsv`** (`ae19768`, `7138872`), una por corrida sellada, con `CORR`/`RES` que releva y el veredicto de verify. Los `spec.yaml` ajenos (`v1_0` de #781, los dos de #785) conservan `cuenta_gen2: PENDIENTE-DE-MESA` — E.3; las `v1_1` propias llevan `cuenta_gen2: SI` + `cuenta_gen2_firma` verbatim. El registro lee `decisiones.tsv` con precedencia 1: las siete `OFERTA · SELLADA/SUPERADO · GEN2 · cuenta_gen2=SI · «decision de mesa (decisiones.tsv)»`. El merge de mesa perfecciona la firma. Cierra por producto `NC-0200` (medidores), `NC-0201` (firma), `NC-0204` (sucesor nombrado) y `NC-0207` (corrida de las dos de #785); `NC-0193` (tanda 3 de `SPECS-DEMANDA-1`) queda cerrada por producto ajeno: sus dos residuos ya tenían spec en `#781` y aquí quedaron sellados.

**Registro (`corrida0 registro --verifica --escribe`), seco primero.** El seco no listó ninguna transición `NC-0094`: en `corridas.tsv` sólo cambian filas propias (4 `SPEC-FIJADA → SUPERADO→v1_1`, 7 selladas nuevas; 185 filas), `resultados.tsv` 4 913 → **5 122** (+209 filas, +150 ids únicos: los 59 de `ENCIG-2023` v1_0 y v1_1 comparten id por `repite_de`), `usos.tsv` **207 filas, byte a byte idéntico a `origin/main`** (cero adopciones, probado). **Pisadas medidas columna por columna contra `origin/main`, excluyendo las filas propias.** Sobre `5973f12` (`#785`): `IDENTICO` en las tres vistas. Tras fusionar `#782/#783/#786/#788/#790` (`48cb08c`) y re-derivar: `corridas`/`resultados` `IDENTICO`; **`usos.tsv` cambia en 2 filas ajenas — `RES-0047` y `RES-0049` pasan de `LEGACY-GEN1` a `GEN2` citando `RESULT-ENIF-AHO-A-P-NOCORTO-SIN-P`/`-CON-P` (`CALC-ENIF-0001`), y `N_resultados_gen2_adoptados_activos` 16 → 18.** No es adopción de este acto: `PR #788` (`GEN2-RELEVO-USOS-1`, `a7255e0`) escribió esa cita en `milpa/tramite.yaml:1137` y `:1184` y su `usos.tsv` derivado quedó desfasado respecto a su propio `milpa/`; un worktree limpio de `origin/main` proyecta exactamente el mismo flip y el mismo 18 (`corrida0 registro` en seco + `status`). Re-derivar aquí sólo materializa lo que la base ya decía. Tras fusionar `#791` (`8f9fb51`) y re-derivar otra vez: **+1 corrida ajena y +117 `RESULT`** (`CALC-TRIADA-B-PISO-0001`, que `#791` selló en NUBE sin re-derivar el registro) — también materialización de un sello ajeno, no producto de este acto. La pisada de `fuente_replay` de actos anteriores no ocurrió: la base ya traía `VERIFY-EN-ESTA-SESION`.

## 4 · Contador, sin adornos

`python3 tools/corrida0.py status`, base de cierre `8f9fb51` (tras `#791`; su `corridas.tsv` publicado decía 72 porque `#791` no re-derivó — re-derivada, la base vale **73** / 3 372) → este acto:

| contador | `origin/main` | este acto | Δ |
|---|---|---|---|
| `N_corridas_requeridas` | 82 | 82 | 0 |
| **`N_corridas_selladas`** | **72** publicado / **73** re-derivado | **80** | **+7**: 6 vigentes con cifra (`TIENE-AHORROS-v1_1`, `EVASION-NORMA-v1_1`, `DINERO-FAMILIARES-VEJEZ-v1_1`, `HORIZONTE-VIA-DERIVADOS-v1_1`, `ENVIPE-DENUNCIA-SEGURO-0001`, `ENCIG-2023-0001-v1_1`) **+ 1 sellada `NO-ESTIMABLE` y superada** (`ENCIG-2023-0001` v1_0): el contador de la casa cuenta `SUPERADO` sellado con firma; si mesa prefiere no contarla, se retira su fila de `decisiones.tsv` y el Δ queda en +6 (`NC-0224`) |
| **`N_resultados_gen2_sellados`** | **3 255** publicado / 3 372 re-derivado | **3 522** | **+150** ids únicos |
| `N_resultados_gen2_pendientes_adopcion` | 5 | 12 | +7 (los `RESULT` de estas corridas que la propuesta ya cita; adoptar es de mesa) |
| `N_resultados_gen2_adoptados_activos` | 16 (`5973f12`) → **18** (`48cb08c`, por `#788`) | 18 | 0 de este acto (sellar no es adoptar, E.2; el +2 es de `#788`, materializado al re-derivar, ver §3) |
| `N_resultados_gen2_vetados_por_decision` | 2 | 2 | 0 |
| `corredores_envueltos_legacy` | 18 | 18 | 0 |
| `no_corrido_abiertas` | — | — | −5 +4 (cierra `NC-0193`/`0200`/`0201`/`0204`/`0207`; abre `NC-0221..0224`) |

El lanzamiento decía «+3 a +5»: son **+7 en el contador, +6 corridas con cifra**, porque las specs eran cuatro y no tres (§1.a) y porque el primer resultado de `ENCIG-2023` se selló antes de sucederse. Demanda relevada: **`CORR-0007`, `CORR-0009`, `CORR-0010` y `CORR-0015` AGOTADAS** (2 + 2 + 2 + 7 = 13 `RESULT` de demanda, más los 4 de `RES-0039..0042` de `CORR-0007`: **17 de los 94** sin candidato al arrancar el día), y `CORR-0001` con **candidatura** medida por canal (los `RES-0001/0002` son ASIGNADO sin canal; la correspondencia la decide mesa, como la spec declara). Ninguna cifra de `milpa/` se movió.

## 5 · Lo que este acto no hizo

- **No editó** ningún `spec.yaml` ajeno, ninguna spec humana sellada ni ningún script de `tools/` (la interfaz `medir()` que les falta se resolvió por sucesión, no parcheando el legado).
- **No adoptó nada**: `milpa/` intocado; `usos.tsv` idéntico a la base.
- **No corrigió hacia atrás**: `ENCIG-2023-0001` v1_0 se selló `NO-ESTIMABLE` y se sucedió; el `NO-REPRODUCE` de grano de `DENUNCIA-SEGURO` se atribuyó y se dejó a mesa.
- **No descargó nada**; cero llamadas a modelos; cero cambios al motor.
- **Redactó `ADR-514` y `NC-0211..0214`** sabiendo que `PR #788` (`GEN2-RELEVO-USOS-1`) los usaba en su rama; `#788` (ADR-514, NC-0211..0217) y `#790` (ADR-515, NC-0218/0219) fusionaron primero → renumerado a **`ADR-516`** y **`NC-0221..0224`** (sólo en texto propio; las menciones a rangos ajenos se conservan).

D-6 aplicado: el acto se declara `ACTO GEN2-MEDICION-DEMANDA-2` en todo archivo que escribe.
