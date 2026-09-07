# ACTO MAESTRA38-C1 · RE-ASIENTO — nota de cierre

7 de septiembre de 2026 · entorno **CAJA (UBUNTU) con corpus** · base `origin/main = ef80502`
Encargo archivado por A.3: `forense/encargos/2026-09-07-MAESTRA38-C1-RE-ASIENTO.md`
Spec congelada: `prereg-caja-S3-C1` (`forense/prereg-caja/S3-C1-spec-v1_0.md`)

---

## 0 · ARRANQUE y ENTORNO — lo que no cuadró

`COMPUERTA: ninguna` (declaración explícita, no dispara verificación).

| # | resultado |
|---|---|
| 0 · guard de rama | `git ls-remote --heads origin` exit 0, control positivo `refs/heads/main` presente, **0** coincidencias `C1`. |
| 1 · repo | `/home/pc0/Modelado-Mexicano`, clon existente. Estaba 44 commits atrás; `git status` limpio. |
| 2 · SHA | FF a `ef80502` (PR #571). Main se movió otra vez a `b1be143` durante el 0-bis — re-derivado al cierre, no es PARO. |
| 3 · data/raw | existe: symlink a `/home/pc0/mm-corpus/raw`, 397 entradas; `data/raices.local.yaml` presente. |
| 4 · entorno | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE = sin_variable` · `curl` INEGI = **200** · `ls data/raw/` = `2005trim1_csv.zip`. |

**Dos premisas de entorno del encargo no se sostienen.** (a) El encargo declara «sin red»: hay red (INEGI 200, `git fetch` y `gh` funcionan). No se usó para bajar nada. (b) La raíz `descargas_mx` (`/mnt/c/…`) es **invisible dentro del sandbox** de esta sesión: `ls` devuelve `No such file or directory`, **0 archivos examinados** (A.13). Fuera del sandbox: **194** archivos. Medido en `via_capa2.py`, la diferencia es exacta: `COINCIDE=92 · AUSENTE=117` adentro contra `COINCIDE=209 · AUSENTE=0` afuera — **los 7 diffs propuestos son idénticos en las dos vistas**, así que la ceguera no contaminó ninguna decisión. Todo comando que toca esa raíz se corrió fuera del sandbox y se declara aquí.

---

## 1 · Correcciones de premisa, antes de escribir nada

**`N45` no existe.** El encargo pide el re-asiento a «`R4.5`/`N45`» y el alta «de `N42`–`N45`». Contra el árbol: `R4.5` es **`N41`**; `N43`/`N44` tienen **0** ocurrencias en todo el repo; `N45` aparece en **un solo** archivo, `2026-09-04-MAESTRA38-N3-PRE-REGISTRO-DE-CAJA.md:5`, que llama «`N42`–`N45` de salud» a las cuatro altas que el árbol tiene como **`N38`–`N41`** — desplazamiento de cuatro lugares, propagado de un encargo al siguiente. La spec congelada §3 ya traía `N41` y el `relacion_id` esperado. **Se siguió la spec, no el rótulo del encargo.**

**Las 7 premisas del encargo, re-verificadas en el 0-bis:** (i) ✔ 3 filas `PENDIENTE` con id de regla en la columna de fuente — pero de `data/curacion-registro/cola-adquisicion-registro.tsv`, que es la **fuente**; `data/cola-adquisicion-v1_0.tsv` es vista generada. (ii) ✔ máximo real `N41`, `N42`–`N45` ausentes — reducido a `N42`, ver arriba. (iii) ✔ `FP-288` `ABIERTA`; las 4 filas identificadas **por la nota que cita `enfih2019_bd_csv_zip`**, no por rótulo; sha `be372533…2ef4d5` correcto. (iv) ✔ el `.zip` Stata: **0** en manifiesto (el `grep -cE "APIPIE|6667"` da 77 porque cuenta las 24 entradas hermanas — el nombre exacto da 0). (v) ✔ `0` en `hallazgos.md`. (vi) ✔ 223 líneas, `SE ENLAZA` 20, `N36` 11. (vii) ✔ ambos ids ENNViH 2002 registrados — `ADR-357` los dio por ausentes y estaban.

---

## 2 · Piezas ejecutadas

**(a0) Alta de `N42`** (`R8.4`, `cooperacion.faena.sancion_social_pueblo_mestizo`, `canon/modelo-decision-v4_0.md:567`). `MAESTRA38-N11:72` la propuso sin ejecutar por estar fuera de su perímetro; `C1` la ejecuta. `N43`–`N45` **no** se dan de alta y se dice por qué.

**(a) Re-asiento.** `alta_relacion.py --dry-run` con la entrada pre-registrada de la spec §3 (extraída verbatim del bloque `yaml`; única normalización: `\s+ → ' '` en las celdas, porque el escalar plegado `>` deja un `\n` final que el escritor de TSV rechaza) derivó **`REL-e7c3700e98be2d9aa7bbd55e`**, exactamente el id pre-registrado. Aplicado. La fila vieja `REL-54b26887b70cada846e1207c` **no se borra ni se mueve** (el script no reescribe filas existentes): se le anota `SUPERADA-POR REL-e7c3700e98be2d9aa7bbd55e (N41)` en la `nota`, mecanismo que la spec §4 ya fijaba. Las 7 relaciones no-etiquetado bajo `N36` **no se tocan** — `L3-BIS` adjudicó que se quedan.

**(b) Tres relaciones `CANDIDATA`.** Ejecuta la firma del 5/sep verbatim: «una necesidad sobre una fuente que ya está en corpus es una relación CANDIDATA, no una fila de cola».

| regla | necesidad | fuente | relacion_id | payloads |
|---|---|---|---|---|
| `R4.3` | `N36` | `CERO_DESABASTO` | `REL-2fa1c0ddb0bd7c2776e43ea8` | 2 ids Cero Desabasto |
| `R8.1` | `N28` | `CNGMD` | `REL-fbda9054154ac31de9be4eff` | 2 ids CNGMD m2 |
| `R8.4` | `N42` | `CNGMD` | `REL-ec408a0b6399f198bcdb5776` | `cngmd2023_m2_marco_regulatorio_csv` |

`CERO_DESABASTO` y `CNGMD` no están en `aliases-fuentes.tsv`, así que el script exigió `alias_decidido` explícito (no infiere por parecido): se declaró con el nombre que ya existe **verbatim** como `fuente_canonica_normalizada` en `relaciones.tsv`. `aliases-fuentes.tsv` **no** se editó.

**Identidad no plegada, declarada:** la fila de cola de `R4.3` cita también `inmujeres_macu_indicadores_territoriales_xlsx` (MACU / Observatorio de Cuidados). MACU **no tiene fuente canónica propia**, y meterlo bajo `CERO_DESABASTO` habría conflado dos fuentes en una fila. Queda citado en la `nota` de `REL-2fa1c0dd…`, **no** en su `id_manifiesto`, y su alta como fuente aparte se declara para mesa (`FP-328` (b)). Las tres filas de cola pasan a `SUPERADA-POR <relacion_id>` con nota; **ninguna se borra**. Vista regenerada con `tools/vista_cola_adquisicion.py` (134 filas).

**(c) `ENFIH`-4 / `FP-288`.** Las 4 filas se identifican por la nota que cita `enfih2019_bd_csv_zip` **con** `necesidad_id` en `{N3, N10, N13, N14}` — el id lo citan **8** filas, y `FP-288` sólo nombra 4. `--verifica --id enfih2019_bd_csv_zip` → **COINCIDE** (sha256 + 4 404 049 B, 1 archivo examinado). Escritos `id_manifiesto` + `sha256_fuente`; `via_capa2.py --escribe` las promovió `SI_O_REFERENCIADO → SI`. `FP-288` → **EJECUTADA** por la opción (i).

Dos correcciones que esta pieza obliga a declarar:

1. **`via_capa2.py` no tiene bandera `--vincula`.** `FP-288` opción (i) la nombra; `--help` sólo ofrece `--root` y `--escribe`. El enlace se escribió como edición preservando texto y `via_capa2` derivó `capa2`/`capa3` después.
2. **El contador «`SE ENLAZA` 20 → 24» es inalcanzable.** El marcador `SE ENLAZA` ya vivía en la `nota` de las 4 filas: Frente D escribió el marcador y dejó `id_manifiesto = NO_DETERMINADO`. Era **mención, no enlace** — exactamente la sustancia de `FP-288`. Sigue en 20. El contador que sí se movió: `capa2_manifiesto = SI`, **86 → 93** (+7 = 4 `ENFIH` + 3 altas de (b)).

**Reserva nueva:** las otras **4** filas que citan el mismo id (`N12`×2, `N4`×2) no se tocaron. `FP-328` (a).

**(d) Los 18 de L2-LISTA.** Una invocación por id, tres resultados sin colapsar: **COINCIDE = 18 · NO_COINCIDE = 0 · AUSENTE = 0** (2 `list_cran_*` + 16 `10_7910_dvn_*`). **La premisa de «16 nuevos» no se reproduce:** ninguno de los dos censos del 6/sep los cuenta como nuevos — los listan como «ya registrado». El falso positivo real ya lo corrigió `MAESTRA38-CENSO-CLON` (`PR #559`) y eran **136 residuos del clon `ACADEMICO-list-cran`**. Un `--escanea` de hoy deja de esa carpeta **2** archivos en staging, y son `meta-*.json` de metadatos. **Nada se promovió de ahí**; el clon `ACADEMICO-list-cran/` no se tocó (regla #559).

**(e) APIPIE.** `MEX_2016_APIPIE_v01_M_Stata.zip`, 618 383 B, `sha256 c2dfe2c7…f5b1`, en `descargas_mx` desde el 6/sep 01:57 **sin registrar**. `zipfile.testzip()` **OK**, 6 miembros y los 6 son `.dta` — es el microdato que a las 24 entradas hermanas les faltaba. Promovido como **`mex_2016_apipie_v01_m_stata`**; `--verifica` **COINCIDE**. Manifiesto **1567 → 1568**. Fila de cola → `OBTENIDO` con la reserva del encargo verbatim.

Dos desvíos declarados: el **prefijo `adq15_wb6667_` no es alcanzable** (`tests/manifiesto.py::_derivar_id` deriva el id del basename; ese script está fuera de perímetro) — el vínculo de familia queda en `usado_para`. Y **A.7 doble descarga no es reproducible**: el payload lo bajó el autor a mano tras `EXIGE-CREDENCIAL`; lo que se corrió es sha256+tamaño contra disco y validación estructural del zip.

**(f)** Siete entradas en `forense/hallazgos.md`, incluida la del encargo sobre WB 6667.

**(g)** `baseline.py` → `{"ok": true}`, `errores: []`. `baseline.json` recifrado con `sync_bootstrap._freeze_manifest`, el mismo escritor que usa `alta_relacion.py`. `via_capa2` en lectura: sin diffs nuevos tras aplicar.

**(h) Ponderador ENNViH 2002 — sólo lista, no adjudica.** `data/ennvih2002-ponderadores-candidatos-v1_0.tsv`, **13** candidatos.

Tres hechos que `ADR-357` no tenía:

1. **El codebook sí está en corpus** (`ennvih1_2002_hogar_cb` = `ennvih/ehh02cb_all.zip`, 11 PDF incluido `ehh02cb_bx.pdf` del libro Proxy). Va en **deflate64**: `zipfile` de Python aborta limpio, pero **`tar.exe` de Windows extrae el miembro con el tamaño exacto y el contenido todo `00`** — leerlo así habría dado «el codebook no documenta el ponderador» en falso. Resuelto con `zipfile-deflate64` en un `--target` aislado del scratchpad.
2. **Los pesos no están ni en el codebook ni en el microdato.** `ehh02dta_all.zip`: **137** miembros `.dta` examinados, **0** con columna `fac*`. Los 11 codebooks: **0** ocurrencias de `fac` (control positivo: 340 376 B de texto extraído de `ehh02cb_bx.pdf`). Viven en `ennvih/ehh02w_all.zip`, un `.dta` por libro, y el documento que los explica es `ennvih/calculo-de-factores-de-expansion.pdf` §1.2.
3. **La ambigüedad tiene causa medible y hay un cuarto candidato.** `fac_3a_px`/`fac_3b_px`/`fac_4_px` comparten **la misma etiqueta verbatim** (`'FACTOR DE EXPANSIÓN LIBRO PROXY'`); se separan por `n > 0`: 21 631 / 21 645 / **9 037** de 35 677. Y `fac_s` (`'FACTOR DE EXPANSIÓN LIBRO SALUD'`, 7 587) es el único cuyo nombre nombra el dominio de `R4.4`/`R9.2`.

**Dos falsos negativos que la tabla estuvo a punto de publicar:** (a) `n_no_nulo = 35 677` en las 11 variables de persona — el archivo guarda `0`, no faltante, así que esa columna **no discrimina**; (b) `folio` es cadena con ceros a la izquierda (`'00001000'`) en los pesos y `float64` (`2000.0`) en el microdato: sin normalizar la llave, el join da **0 en las 13 filas**. Normalizada: **1 903/1 903** filas del libro Proxy y **35 664** folios de hogar. Ninguno de los dos levanta excepción.

---

## 3 · CONTADOR — declarado contra lo que el encargo pidió

| contador | pedido | medido |
|---|---|---|
| relaciones de salud bajo `N` correcto | +1 | **+1** (`REL-e7c3700e98be2d9aa7bbd55e`, `N41`) |
| `CANDIDATA` | +3 | **+4** (158 → 162: las 3 de (b) **más** el re-asiento de (a), que la spec fija como `CANDIDATA`) |
| filas de cola con id de regla | 3 → 0 | **3 → 0** |
| `SE ENLAZA` | 20 → 24 | **20 → 20** — inalcanzable, ver §2(c). El que se movió: `capa2 = SI` **86 → 93** |
| payloads | +1 | **+1** (manifiesto 1567 → 1568) |
| candidatos a ponderador ENNViH | 0 → k | **0 → 13** |
| necesidades | (implícito) | 41 → **42** |
| medición del motor | cero | **cero** — ningún `p`, ningún IC, ninguna `R` |

---

## 4 · Perímetro

**Tocado:** `data/curacion-registro/{relaciones,evidencias,utilidad-modelo,necesidad-objeto-modelo,cola-adquisicion-registro}.tsv` + `baseline.json` · `data/cola-adquisicion-v1_0.tsv` (vista) · `data/manifiesto.yaml` (+1) · `data/manifiesto-staging.yaml` · `data/ennvih2002-ponderadores-candidatos-v1_0.tsv` (nuevo) · `forense/hallazgos.md` · `forense/firmas-pendientes.tsv` · `forense/encargos/` (A.3) · esta nota · cascada.

**No tocado, verificado:** `milpa/**` · `canon/` salvo la cascada · `data/l*-*` · `forense/prereg-caja/` · el clon `ACADEMICO-list-cran/` (regla #559) · `tests/*.py` · `tools/*.py` · `data/curacion-registro/aliases-fuentes.tsv`.
