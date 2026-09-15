# Cierre · ACTO GEN2-VERIFICACION-CAJA-2 — lo que sólo la caja puede certificar, segunda tanda

**Acto:** `ACTO GEN2-VERIFICACION-CAJA-2` · 14/sep/2026 · CAJA (Ubuntu/WSL2, corpus montado, red INEGI 200) · base `origin/main = 016d325` (PR #760) en el 0-bis, `a29d873` (PR #759) al abrir la ejecución
**Encargo:** `forense/encargos/2026-09-14-GEN2-VERIFICACION-CAJA-2.md` (A.3, verbatim, `569705b`)
**Compuerta:** `GATED a PR del ACTO GEN2-DISENO-FASE1-CIERRE fusionado` — verificada por producto: `gh pr view 760` → `MERGED` (2026-09-14T20:15:16Z), `git merge-base --is-ancestor 016d325 origin/main` → sí, `forense/encargos/2026-09-14-GEN2-DISENO-FASE1-CIERRE.md` con `## CONSUMIDO` en `origin/main`. Primer intento (11:28 CST, contra `11c8783`) paró con cero commits.
**Salidas crudas de `verify`:** §3 de esta nota (una invocación por corrida, dos pasadas aisladas)

---

## 0 · El titular

Las dos filas viejas de la clase «certificación que exige los bytes» quedan resueltas con lo que la caja puede decir y sólo con eso:

- **`NC-0062` muere.** `CALC-0001`, `CALC-0002` y `CALC-0003-v2` salen **`REPRODUCE · IDENTICO`** en `corrida0 verify` con el corpus montado: 54/54, 29/29 y 128/128 `RESULT` con `delta = 0`, `SELLO COINCIDE`, `SPEC.YAML IDENTICO`, todos los `INPUT COINCIDE` por `sha256`, `CONTEXTO IDENTICO` (código, parámetros, semilla y dependencias; `commit_informativo DISTINTO` no gatea por `FP-358`). Dos pasadas aisladas por corrida, 6/6 idénticas. Ninguna semilla, dependencia ni código se tocó.
- **`NC-0100` se cierra con saldo declarado, no con acreditación inventada.** De las 32 identidades: **7 `ACREDITADA`**, **18 `ACREDITADA-CON-NOTA`**, **7 `NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL`**. Las siete no localizadas son las **cinco `AP5_*` de 2015** que el encargo ya sospechaba (el PDF oficial salta de `AP5_6_01` a `AP5_7_2` entre las páginas 26 y 27) **más las dos `EST_SOC` de 2013**, que el encargo suponía «técnicas» acreditables con nota y que el FD oficial de 2013 **no trae en ninguna celda** (documenta `EST`, 3 caracteres; el DBF trae además `EST_SOC`, 1 carácter).

**Contador: no.** Este acto no mide nada nuevo. Los tres replays son evidencia de hoy sobre corridas selladas el 8/sep (E.3); ninguna adopción (`usos.tsv` idéntico a `origin/main`). Las tres corridas ya contaban `cuenta_gen2 = SI` por firma de mesa del 8/sep en `decisiones.tsv` — la premisa del encargo («`cuenta_gen2 = NO` por diseño») describe el mecanismo E.4 de los replays legacy, no el estado de estas tres filas; en ambos casos el replay no mueve ningún contador.

---

## 1 · Arranque, premisas y universo (A.8 / A.13)

- **Colisión resuelta antes de tocar nada.** El worktree `~/mm-gen2-verificacion-caja-2` y el 0-bis `569705b` (14:37 CST) los creó otra sesión de esta misma caja que tomó este encargo y quedó caída desde las 14:44 con `API Error … EAI_AGAIN`. Se reportó a mesa con la evidencia (transcripción de esa sesión, sin commits posteriores, árbol limpio) y mesa cerró la sesión caída y ordenó continuar sobre su 0-bis. No se rehizo el 0-bis; se hizo `git merge origin/main` (8 commits, PR #759) y `git push -u` inmediato del rótulo.
- **Entorno (una invocación, `tools/entorno.py --sonda-red`):** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable` · red `200` · corpus `SI (examinados=413)` · raíces `data_raw:SI descargas_mx:SI` · `python 3.14.4 · numpy 2.3.5 · pandas 2.3.3 · scipy 1.16.3 · pyreadstat 1.3.6 · yaml 6.0.3` — **idénticas** a `dependencias_materiales` de `ejecucion.json` de las tres corridas. Nada se instaló.
- **Las 32 identidades se re-derivaron por diferencia de conjuntos**, no por el rótulo de la fila: `data/inventario-reactivos-v1_2.tsv` (419 filas `envipe2013`, 485 `envipe2015`) menos las claves `(instrumento, payload, miembro, variable)` presentes en `data/inventario-reactivos-contexto-v1_1.tsv` (43 020 filas con texto) → **9 + 23 = 32**, exactamente las que `NC-0100` y `data/reactivos-contexto-residual-v1_1.tsv` enumeran.
- **Descriptores oficiales, identidad por bytes:** `data/raw/envipe2013/fd_envipe2013.xlsx` (`sha256 7e842826e3f7…`, 192 702 B, `manifiesto.yaml: envipe_2013_fd_envipe2013`) y `data/raw/envipe2015/fd_envipe2015.pdf` (`sha256 1042ab57b015…`, 1 852 255 B, 77 páginas, `envipe_2015_fd_envipe2015`). Las copias que viajan **dentro** de `bd_envipe13_dbf.zip` (`FD_ENVIPE13.xlsx`) y `bd_envipe2015_dbf.zip` (`fd_envipe2015.pdf`) son **byte-idénticas** a las de bodega (mismo `sha256`), así que no hay «otro descriptor oficial» que consultar.
- **DBF leídos por su cabecera (descriptor de campo, no FD):** 2013 `tmod_vic.dbf` 120 campos / 47 117 registros y `tper_vic.dbf` 246 / 82 933; 2015 `THogar.dbf` 13 / 87 919, `TPer_Vic1.dbf` 168 / 84 507, `TPer_Vic2.dbf` 141 / 84 507, `TSDem.dbf` 22 / 327 543, `TVivienda.dbf` 18 / 85 729. Se leyeron **códigos distintos** (no frecuencias) de cuatro columnas para caracterizar la estructura: `EST_SOC` (2013, ambos DBF) = {1,2,3,4}; `ESTRATO` (2015, `TPer_Vic1`) = {1,2,3,4}; `AP5_7_1` = {' ',1,2,9}; `AP5_3_02` = {1,2,3,9}. Ningún valor de persona, ninguna tabulación.

---

## 2 · P1 — las 32 identidades, una por una (vocabulario A.4)

Criterio aplicado, declarado antes de la tabla: **`ACREDITADA`** = nombre, etiqueta, tipo y longitud coinciden entre descriptor oficial y cabecera del DBF (`Alfanumérico` ↔ `C`). **`ACREDITADA-CON-NOTA`** = la entrada existe con nombre, etiqueta y longitud, y la discrepancia es técnica y se explica: el FD declara `Numérico` y el DBF almacena el código como carácter (`C`) de la misma longitud — un solo patrón, repetido; o la identidad existe en el descriptor pero **no es una variable** (las siete «documentales» de 2013). **`NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL`** = el mnemónico no aparece en ninguna celda/carácter del descriptor oficial; no se rebusca en otra fuente ni se rellena por analogía.

### 2.1 · ENVIPE 2013 — `fd_envipe2013.xlsx` (hojas `TViviend`, `Thogar`, `TSDem`, `TPer_Vic`, `TMod_Vic`, `Catálogo de entidades`, `Catálogo de municipios`)

| # | miembro | variable | DBF (tipo, long.) | veredicto | cita textual del descriptor (hoja, fila) |
|---|---|---|---|---|---|
| 1 | `tmod_vic.dbf` | `EST_SOC` | `C`, 1 | **NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL** | `TMod_Vic` no trae `EST_SOC`. Su bloque «Campos empleados para el diseño muestral» (filas 622–634) documenta `FAC_DEL`, `DOM` («Dominio», `U/C/R`, 1), **`EST`** («Estrato de diseño muestral», `Alfanumérico`, `"001 … 303"`, 3) y `UPM` (5). El DBF trae **ambos**, `EST` `C(3)` y `EST_SOC` `C(1)`; el segundo no está descrito. Códigos observados de `EST_SOC`: {1,2,3,4} — coinciden con el dominio de `ESTRATO` documentado en 2015, lo que sugiere el estrato socioeconómico, pero **la sugerencia no es acreditación**. |
| 2 | `tper_vic.dbf` | `EST_SOC` | `C`, 1 | **NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL** | Idéntico patrón en `TPer_Vic`, filas 1041–1055: `FAC_HOG`, `FAC_ELE`, `DOM`, **`EST`** (fila 1053: «Estrato de diseño muestral · EST · Alfanumérico · "001 … 303" · 3»), `UPM`. `EST_SOC` ausente. |
| 3 | `Catálogo de entidades` | «INEGI. Encuesta Nacional de Victimización y Percepción sobre Inseguridad Pública 2013. Descripción de archivos (FD).» | — (hoja, no DBF) | **ACREDITADA-CON-NOTA** | Es la celda `A1` (fila 1) de la hoja, verbatim. **No es una variable:** es el título del documento que encabeza cada hoja; la fila del inventario es un artefacto de `INSPECT_XLSX` que tomó la cabecera como `variable_id`. No hay reactivo que acreditar ni nada que pedir a INEGI. |
| 4 | `Catálogo de municipios` | ídem | — | **ACREDITADA-CON-NOTA** | ídem, fila 1 de la hoja. |
| 5 | `TMod_Vic` | ídem | — | **ACREDITADA-CON-NOTA** | ídem, fila 1 de la hoja. |
| 6 | `TPer_Vic` | ídem | — | **ACREDITADA-CON-NOTA** | ídem, fila 1 de la hoja. |
| 7 | `TSDem` | ídem | — | **ACREDITADA-CON-NOTA** | ídem, fila 1 de la hoja. |
| 8 | `TViviend` | ídem | — | **ACREDITADA-CON-NOTA** | ídem, fila 1 de la hoja. |
| 9 | `Thogar` | ídem | — | **ACREDITADA-CON-NOTA** | ídem, fila 1 de la hoja. |

A.13 del negativo de `EST_SOC`: se examinaron **las 7 hojas del libro, 10 305 celdas no vacías**; la cadena `SOC` aparece sólo en cinco nombres de municipio (Socoltenango, San Pedro Sochiápam, Santiago Sochiapan, Sochiapa, Soconusco). Control positivo: el mismo barrido localiza `EST`, `UPM`, `FAC_*` y `VIV_SEL` en sus filas.

### 2.2 · ENVIPE 2015 — `fd_envipe2015.pdf` (77 pp.; «Tabla TVivienda» pp. 9–11, «Tabla THogar» p. 12, «Tabla TSDem» pp. 13–15, «Tabla TPer_Vic1» pp. 15–32, «Tabla TPer_Vic2» pp. 32–50; cada tabla cierra con «Campos empleados para el diseño muestral»)

| # | miembro | variable | DBF (tipo, long.) | veredicto | cita textual del descriptor (página) |
|---|---|---|---|---|---|
| 10 | `THogar.dbf` | `DOMINIO` | `C`, 1 | **ACREDITADA** | p. 12, diseño muestral: «Dominio · DOMINIO · Alfanumérico · U Urbano / C Complemento urbano / R Rural · 1» |
| 11 | `THogar.dbf` | `HOGAR` | `C`, 2 | ACREDITADA-CON-NOTA | p. 12: «Control del hogar · HOGAR · Numérico · 01…99 · 2» — `Numérico` en FD, `C` en DBF, misma longitud |
| 12 | `THogar.dbf` | `R_SEL` | `C`, 2 | ACREDITADA-CON-NOTA | p. 12: «Número de renglón de la persona seleccionada · R_SEL · Numérico · 01…30,b · Renglón del seleccionado · 2» — ídem |
| 13 | `THogar.dbf` | `UPM` | `C`, 7 | ACREDITADA-CON-NOTA | p. 12: «Unidad primaria de muestreo · UPM · Numérico · 0100001…3299999 · 7» — ídem (nota: es la UPM identificadora; la de diseño es `UPM_DIS`, 5, ya acreditada) |
| 14 | `THogar.dbf` | `VIV_SEL` | `C`, 2 | ACREDITADA-CON-NOTA | p. 12: «Vivienda seleccionada · VIV_SEL · Numérico · 01…99 · 2» — ídem |
| 15 | `TPer_Vic1.dbf` | `AP5_3_02` | `C`, 1 | **NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL** | ver bloque de abajo |
| 16 | `TPer_Vic1.dbf` | `AP5_4_02` | `C`, 1 | **NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL** | ver bloque de abajo |
| 17 | `TPer_Vic1.dbf` | `AP5_5_02` | `C`, 1 | **NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL** | ver bloque de abajo |
| 18 | `TPer_Vic1.dbf` | `AP5_6_02` | `C`, 1 | **NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL** | ver bloque de abajo |
| 19 | `TPer_Vic1.dbf` | `AP5_7_1` | `C`, 1 | **NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL** | ver bloque de abajo |
| 20 | `TPer_Vic1.dbf` | `AREAM` | `C`, 2 | ACREDITADA-CON-NOTA | p. 16: «Área Metropolitana · AREAM · Numérico · 01 Distrito Federal … 14 Aguascalientes · 2» — `Numérico`/`C` |
| 21 | `TPer_Vic1.dbf` | `DOMINIO` | `C`, 1 | **ACREDITADA** | p. 32 (continuación del bloque de diseño de TPer_Vic1 abierto en p. 31, antes de «Tabla TPer_Vic2»): «Dominio · DOMINIO · Alfanumérico · U/C/R · 1» |
| 22 | `TPer_Vic1.dbf` | `ESTRATO` | `C`, 1 | ACREDITADA-CON-NOTA | p. 32: «Estrato · ESTRATO · Numérico · 1 / 2 / 3 / 4 · 1» — `Numérico`/`C`; códigos observados en el DBF {1,2,3,4} = los declarados |
| 23 | `TPer_Vic1.dbf` | `HOGAR` | `C`, 2 | ACREDITADA-CON-NOTA | p. 15: «Control del hogar · HOGAR · Numérico · 01…99 · 2» |
| 24 | `TPer_Vic1.dbf` | `RESUL_H` | `C`, 1 | **ACREDITADA** | p. 16: «Resultado de la visita al hogar · RESUL_H · Alfanumérico · A Entrevista completa con victimización / B Entrevista completa sin victimización · 1» |
| 25 | `TPer_Vic1.dbf` | `R_SEL` | `C`, 2 | ACREDITADA-CON-NOTA | p. 16: «Renglón de la persona seleccionada · R_SEL · Numérico · 01…30 · 2» |
| 26 | `TPer_Vic2.dbf` | `DOMINIO` | `C`, 1 | **ACREDITADA** | p. 50 (bloque de diseño de TPer_Vic2, abierto en p. 49): «Dominio · DOMINIO · Alfanumérico · U/C/R · 1» |
| 27 | `TPer_Vic2.dbf` | `ESTRATO` | `C`, 1 | ACREDITADA-CON-NOTA | p. 50: «Estrato · ESTRATO · Numérico · 1 / 2 / 3 / 4 · 1» |
| 28 | `TPer_Vic2.dbf` | `RESUL_H` | `C`, 1 | **ACREDITADA** | p. 32: «Resultado de la visita al hogar · RESUL_H · Alfanumérico · A / B · 1» |
| 29 | `TPer_Vic2.dbf` | `R_SEL` | `C`, 2 | ACREDITADA-CON-NOTA | p. 32: «Renglón de la persona seleccionada · R_SEL · Numérico · 01…30 · 2» |
| 30 | `TSDem.dbf` | `DOMINIO` | `C`, 1 | **ACREDITADA** | p. 15 (bloque de diseño de TSDem, antes de «Tabla TPer_Vic1»): «Dominio · DOMINIO · Alfanumérico · U/C/R · 1» |
| 31 | `TSDem.dbf` | `RESUL_H` | `C`, 1 | **ACREDITADA** | p. 13: «Resultado de la visita al hogar · RESUL_H · Alfanumérico · A / B / C Entrevista sin información de la persona elegida · 1» |
| 32 | `TVivienda.dbf` | `AREAM` | `C`, 2 | ACREDITADA-CON-NOTA | p. 9, «I. DATOS DE IDENTIFICACIÓN»: «Área Metropolitana · AREAM · Numérico · 01 Distrito Federal … 14 Aguascalientes · 2» |

**Las cinco `AP5_*` (filas 15–19), con el hueco a la vista.** La página 26 termina en `AP5_6_01` («5.6 ¿Qué tan efectivo considera el desempeño de la (del)(AUTORIDAD)? · Policía de Tránsito de su Municipio [Tlaxcala (3)] · AP5_6_01 · Numérico · 1 Muy efectivo … 4 Nada efectivo») con la marca «(Continúa)». La página 27 abre con los códigos restantes de esa misma variable («9 No sabe / no responde · b blanco») y salta a **«5.7 … Policía Preventiva Municipal [DF (3)] · AP5_7_2»**, seguida de `AP5_3_03`/`AP5_4_03`/`AP5_5_03`/`AP5_6_03`/`AP5_7_3` (Policía Estatal). Entre una página y otra faltan, en el orden que el propio patrón del PDF exige, **`AP5_7_1`** (5.7 para Policía de Tránsito) y **`AP5_3_02`, `AP5_4_02`, `AP5_5_02`, `AP5_6_02`** (5.3–5.6 para Policía Preventiva Municipal). La cabecera de `TPer_Vic1.dbf` trae las cinco exactamente en ese hueco (`… AP5_6_01, AP5_7_1, AP5_3_02, AP5_4_02, AP5_5_02, AP5_6_02, AP5_7_2 …`), y sus códigos observados calzan con las preguntas vecinas (`AP5_7_1` = {' ',1,2,9} como toda 5.7; `AP5_3_02` = {1,2,3,9} como `AP5_3_01`). Es decir: el descriptor oficial **omitió una sección**, y el archivo la trae. A.13 del negativo: `pdftotext -layout` (4 717 líneas) y `pdfplumber` sobre **los 117 174 caracteres de las 77 páginas** (incluidos los que caen fuera del recorte visible; cero anotaciones en pp. 26–27): **0 apariciones** de cualquiera de los cinco mnemónicos; control positivo en el mismo barrido: `AP5_3_01` (p. 26), `AP5_3_03` y `AP5_7_2` (p. 27), `AP5_8` (p. 31). **No se rellena por analogía**: el veredicto `NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL` es el entregable; si mesa quiere el texto oficial de esas cinco preguntas, la vía es la solicitud de titular (§5).

**Saldo P1:** 32 = **7 ACREDITADA** (2015: `DOMINIO` ×4 —`THogar`, `TPer_Vic1`, `TPer_Vic2`, `TSDem`— y `RESUL_H` ×3 —`TPer_Vic1`, `TPer_Vic2`, `TSDem`) · **18 ACREDITADA-CON-NOTA** (7 «documentales» 2013 + 11 técnicas 2015 con `Numérico`/`C`) · **7 NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL** (2 `EST_SOC` 2013 + 5 `AP5_*` 2015). La fila `NC-0100` esperaba «2 EST_SOC técnicas» acreditables con nota: **no lo son** — es el hallazgo de esta pieza.

---

## 3 · P2 — los replays a su destino (salida cruda de `corrida0 verify`, una invocación por corrida)

**Vehículo registrado, sin tocar sellos:** el recibo de cada corrida se asentó como **fila nueva** en `forense/replay-evidencia.tsv` (`procedencia = VERIFY-ESTRUCTURADO · ACTO GEN2-VERIFICACION-CAJA-2`, `fecha_verificacion = 2026-09-14`, identidad `spec_yaml_sha256 / script_blob_sha256 / input_sha256_efectivos` copiada de `ejecucion.json`). Las filas anteriores de los mismos `calc_id` (`HEREDADO-DEL-REGISTRO-PUBLICADO`, `fecha DESCONOCIDA`, `NO-EJECUTABLE/DISTINTO` para 0001/0002) **quedan intactas como historia** (E.3: nada se reescribe; el recibo nuevo se añade con su fecha). 75 → 78 filas.

**Entorno del replay, declarado:** `CALC-0003-v2` lee `data_raw` y corrió **dentro** del sandbox de la sesión. `CALC-0001` y `CALC-0002` leen la raíz `descargas_mx`, que el sandbox de esta caja no puede leer (lista de denegación de `/mnt`): dentro del sandbox `CALC-0001` sale `INPUT AUSENTE ×3 → CONTEXTO DISTINTO → NO-EJECUTABLE` (`PyreadstatError: File … does not exist`) — **artefacto del sandbox, no del dato**, el mismo que documentan `MAESTRA38-LOTE-LAPOP` y `GEN2-ADQ-VERIFICACION-CAJA`. Se repitió **fuera del sandbox** (el corpus es el objeto del acto), y ésa es la salida que se reporta. No se espejó nada, no se cambió la configuración local de raíces (archivo gitignorado, per-worktree).

### `CALC-0003-v2` (`CALC-0003-v2--cdebb607728c`, ENNViH 2002, sandbox)

```
VERIFY CALC-0003-v2   (data/corrida0/CALC-0003-v2)
  [1/5 SELLO] COINCIDE -- sello y todos los archivos que cubre coinciden
  [2/5 SPEC.YAML] IDENTICO  sellado=af90be95f8135e8c992badcbece90dedf1e27c54658a606feb37f731e87cae19  hoy=af90be95f8135e8c992badcbece90dedf1e27c54658a606feb37f731e87cae19
  [3/5 INPUT COINCIDE] ennvih1_2002_hogar_dta (manifiesto)  sellado=8b9b5190… actual=8b9b5190…
  [3/5 INPUT COINCIDE] ennvih1_2002_ponderador (manifiesto)  sellado=bbe80068… actual=bbe80068…
  [3/5 INPUT COINCIDE] IN-S6-SPEC-SELLADA (repo)  sellado=c1cd3b63… hoy=c1cd3b63…
  [4/5 CONTEXTO] codigo=IDENTICO  commit_informativo=DISTINTO  (FP-358: no gatea)  parametros=IDENTICO  seed=IDENTICO  dependencias=IDENTICO
  CONTEXTO: IDENTICO
  [5/5 RESULT REPRODUCE] × 128  (todos delta=0.0 o None por tipo; ningún NO-REPRODUCE)
VERIFY: REPRODUCE   (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)   exit=0
```

### `CALC-0001` (`CALC-0001--174c269a07b6`, CIDE-CSES 2015, fuera del sandbox)

```
VERIFY CALC-0001   (data/corrida0/CALC-0001)
  [1/5 SELLO] COINCIDE -- sello y todos los archivos que cubre coinciden
  [2/5 SPEC.YAML] IDENTICO  sellado=38bfd857c58e49aa9b72756700efb19dc138748a4e825cfe03f40127946cad8f  hoy=38bfd857…
  [3/5 INPUT COINCIDE] cide_cses2015_nacional_poselectoral (manifiesto)  sellado=1ef01a17… actual=1ef01a17…
  [3/5 INPUT COINCIDE] cide_cses2015_nacional_preelectoral (manifiesto)  sellado=85432d32… actual=85432d32…
  [3/5 INPUT COINCIDE] cide_cses2015_estatal_preelectoral (manifiesto)  sellado=7cf0e9e9… actual=7cf0e9e9…
  [3/5 INPUT COINCIDE] IN-S12-SPEC-SELLADA (repo)  sellado=870522a3… hoy=870522a3…
  [4/5 CONTEXTO] codigo=IDENTICO  commit_informativo=DISTINTO  (FP-358: no gatea)  parametros=IDENTICO  seed=IDENTICO  dependencias=IDENTICO
  CONTEXTO: IDENTICO
  [5/5 RESULT REPRODUCE] × 54  (p. ej. RESULT-C1-POSEL-OFERTA-P-T1: sellado=0.37922545290553505 · hoy=0.37922545290553505 · delta=0.0; RESULT-C2BIS-PVOTO3-P: 0.5989810241496706 · delta=0.0)
VERIFY: REPRODUCE   (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)   exit=0
```

### `CALC-0002` (`CALC-0002--f57ad1cd8f96`, LAPOP 2019/2021/2023, fuera del sandbox)

```
VERIFY CALC-0002   (data/corrida0/CALC-0002)
  [1/5 SELLO] COINCIDE -- sello y todos los archivos que cubre coinciden
  [2/5 SPEC.YAML] IDENTICO  sellado=5d0c88a358cfec1525378b294694b8e0fa44ab7edffec3f6a9903e14be7e669e  hoy=5d0c88a3…
  [3/5 INPUT COINCIDE] mexico_lapop_americasbarometer_2019_v1_0_w (manifiesto)  sellado=c88f79eb… actual=c88f79eb…
  [3/5 INPUT COINCIDE] mex_2021_lapop_americasbarometer_v1_2_w (manifiesto)  sellado=153fb0f8… actual=153fb0f8…
  [3/5 INPUT COINCIDE] mex_2023_lapop_americasbarometer_v1_0_w (manifiesto)  sellado=4a9410a5… actual=4a9410a5…
  [3/5 INPUT COINCIDE] IN-S13-SPEC-SELLADA (repo)  sellado=c41235b8… hoy=c41235b8…
  [4/5 CONTEXTO] codigo=IDENTICO  commit_informativo=DISTINTO  (FP-358: no gatea)  parametros=IDENTICO  seed=IDENTICO  dependencias=IDENTICO
  CONTEXTO: IDENTICO
  [5/5 RESULT REPRODUCE] × 29  (p. ej. RESULT-CTX-2019-P-ALTO: sellado=0.7862745098039216 · hoy=0.7862745098039216 · delta=0.0; RESULT-CTX-2023-IC-LO: 0.6843195210395104 · delta=0.0)
VERIFY: REPRODUCE   (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)   exit=0
```

**Segunda pasada aislada** (misma invocación, mismo entorno, `NC-0182` a la vista): `CALC-0001` `REPRODUCE · IDENTICO` 54/54 · `CALC-0002` 29/29 · `CALC-0003-v2` 128/128 — 6/6 pasadas idénticas.

### Re-derivación de las vistas (`registro`), medida columna por columna

1. `corrida0 registro` en seco tras el asiento: **sin `--verifica`** las vistas cambiarían los dos ejes de **10 corridas ajenas** (blanquea a `NO-VERIFICADO` las cuatro `CALC-B-MARCO-*`, `CALC-EDER-0001`, `CALC-F5-REANALISIS-0001` y `CALC-SHED2025-BNPL-DANO-0001`, que no tienen asiento; y revierte `CALC-B-0001` y los dos `CALC-MOTOR-celdas-semilla*` a asientos que `NC-0181` ya declaró contradichos). **No se escribió así.**
2. `corrida0 registro --verifica --escribe --lote CALC-0001,CALC-0002` **fuera del sandbox** (para que los medidores de `descargas_mx` reejecuten de verdad), primera pasada (4 min 41 s): **`PARO · REPLAY-PISADO (NC-0094)`** — `CALC-M-marco-M-sorteado-v1_3--8f09149b968e · resultado_replay: REPLICA-RESULTADO · CONTEXTO-DISTINTO -> NO-REPRODUCE · CONTEXTO-DISTINTO`; ninguna vista escrita. **Es `NC-0182` reproducida** (veredicto inestable in-process): `verify` aislado ×2 de esa corrida → `REPLICA-RESULTADO · CONTEXTO-DISTINTO` (33/33 RESULT, contexto distinto por `IN-EMITE-M`/`IN-TRAMITE`/`IN-PROCEDENCIA`) las dos veces. **No se nombró en `--lote`** — no se publica un veredicto que no se sostiene aislado.
3. Segunda pasada del mismo comando (4 min 39 s): escribió `corridas.tsv` (164), `resultados.tsv` (4 483), `usos.tsv` (207). Avisos que **no** son de este acto y quedan como estaban: `REPLAY-CONTRADICE-ASIENTO` para `CALC-B-0001` y los dos `CALC-MOTOR-celdas-semilla*` (`NC-0181`, fuera de perímetro); `REPLAY-NO-VERIFICABLE-HOY` para `CALC-C0D-MARCADOR-v3` y `CALC-SMOKE-0001` (proyectan su asiento, no degradan).
4. **Pisadas medidas contra `origin/main` excluyendo mis dos corridas:** `corridas.tsv` 164 = 164 filas, **0 transiciones en `resultado_replay`/`contexto_replay` sobre ajenas**, 2 filas ajenas con sólo `fuente_replay` cambiada (`CALC-0001-v2`, `CALC-MOTRAL2015-VALORACION-SS-0001`: de asiento citado a `VERIFY-EN-ESTA-SESION`, porque esta sesión también las reprodujo con la raíz legible); `resultados.tsv` 3 575 = 3 575, 0 transiciones, 163 filas con sólo `fuente_replay` (54 + 29 mías, 38 + 42 de esas dos ajenas); **`usos.tsv` idéntico** → cero adopciones, mecánico. Mis dos filas: `NO-EJECUTABLE/DISTINTO → REPRODUCE/IDENTICO`, `fuente_replay = VERIFY-EN-ESTA-SESION · verify(CALC-000n)`.

---

## 4 · Hallazgos

- **El descriptor oficial de ENVIPE 2015 omite una sección entera** (cinco variables entre las pp. 26 y 27) y el de 2013 **no documenta `EST_SOC`** aunque el archivo lo traiga en dos tablas. Ninguno de los dos huecos se puede cerrar desde el corpus sin inventar; ambos son material para la vía de titular (§5).
- **La premisa «2 EST_SOC técnicas» de `NC-0100` era falsa en la letra:** no era una etiqueta técnica por acreditar, era una variable ausente del descriptor. Diferencia de conjuntos y lectura del descriptor entero, no la etiqueta de la fila residual, es lo que lo mostró.
- **`NC-0182` se reproduce por tercera vez** (B-MARCO, DISENO-FASE1-CIERRE en seco, aquí en `--escribe`): la primera pasada in-process de `registro --verifica` degrada `CALC-M-marco-M-sorteado-v1_3` y la segunda no. Sigue sin dueño.

---

## 5 · P3 — el saldo

| pieza | resultado | fila | estampa |
|---|---|---|---|
| P1 · 32 identidades | 7 `ACREDITADA` · 18 `ACREDITADA-CON-NOTA` · 7 `NO-LOCALIZADA-EN-DESCRIPTOR-OFICIAL` (tabla §2) | **`NC-0100` → CERRADA** (acreditadas + no-localizadas declaradas es cierre válido, por letra del encargo) | `ACTO GEN2-VERIFICACION-CAJA-2`, 2026-09-14 |
| P2 · `CALC-0001` | `REPRODUCE · IDENTICO`, 54/54, 2/2 pasadas | asiento nuevo en `replay-evidencia.tsv`; vista re-derivada con `--lote` | ídem |
| P2 · `CALC-0002` | `REPRODUCE · IDENTICO`, 29/29, 2/2 | ídem | ídem |
| P2 · `CALC-0003-v2` | `REPRODUCE · IDENTICO`, 128/128, 2/2 | asiento nuevo (el anterior tenía `fecha DESCONOCIDA`); vista sin transición | ídem |
| `NC-0062` | las tres corridas que lista llegan a `REPRODUCE · IDENTICO` con corpus; el sucesor que la fila pedía («CAJA con corpus montado + numpy/pandas/scipy») fue este acto | **CERRADA** | ídem |
| reserva DBF (`NC-0100` en `2026-09-09-GEN2-R-SERIE-DBF`) | enmienda fechada en `forense/notas/2026-09-09-GEN2-R-SERIE-DBF-cierre.md` §10 (original intacto) | — | ídem |
| para titular | texto oficial de `AP5_3_02/4_02/5_02/6_02/7_1` (ENVIPE 2015) y de `EST_SOC` (ENVIPE 2013): **no se abre solicitud**; si mesa la firma, va por la vía comprobada del expediente `04-INEGI-ENCIG-NC-0153` (`forense/expedientes-acceso/2026-09-11-GEN2-EXPEDIENTES-ACCESO-21/`, Contacto INEGI / `atencion.usuarios@inegi.org.mx`), como expediente hermano, sin fila gemela de `NC-0100` | `NC-0185` (`DECISIÓN-DE-MESA-PENDIENTE`) | ídem |

**Contador, en una línea:** ninguno se mueve — replays legacy no cuentan (E.4), ninguna adopción, ningún CALC nuevo; las tres corridas ya contaban por firma del 8/sep.

---

## 6 · Límites declarados

- Los replays de `CALC-0001`/`CALC-0002` se corrieron **fuera del sandbox de la sesión** por la política de lectura de `/mnt`; el archivo leído es el mismo (`sha256` de cada input `COINCIDE` con el sello). Quien relance en una caja con `descargas_mx` legible obtendrá la misma salida sin esa salvedad.
- `fuente_replay` de dos corridas ajenas cambió de asiento citado a `VERIFY-EN-ESTA-SESION` (§3.4). Es una pisada de una columna descriptiva, no de evidencia; se declara y no se «arregla» a mano (los TSV son derivados).
- La acreditación es contra el **descriptor oficial** (FD) y la **cabecera** del DBF. No se abrió ningún cuestionario (`ENVIPE13_Cuest.zip`, `cuestionarios_envipe2015.zip`) para «encontrar» las AP5_*: el encargo lo prohíbe y el cuestionario no es el descriptor.
- Las siete «documentales» de 2013 son filas auxiliares sin reactivo; corregir cómo el inventario las clasifica está fuera de perímetro (`data/inventario-reactivos*.tsv`, `tools/inventario_reactivos*.py`).

## 7 · A.13 — qué se examinó

`fd_envipe2013.xlsx`: 7 hojas, 10 305 celdas no vacías. `fd_envipe2015.pdf`: 77 páginas, 117 174 caracteres (`pdfplumber`), 4 717 líneas (`pdftotext -layout`). Cabeceras DBF: 11 archivos (5 de 2013, 6 de 2015), 897 campos; 7 de ellos alojan las 25 identidades DBF. Columnas con códigos leídos: 4 (§1). `verify`: 3 corridas × 2 pasadas + 1 control sandboxed + 2 aisladas de `CALC-M-marco-M-sorteado-v1_3`. `registro --verifica --escribe`: 2 pasadas. Sesión concurrente: transcripción `da874d0c…`, última actividad 14:53 CST.
