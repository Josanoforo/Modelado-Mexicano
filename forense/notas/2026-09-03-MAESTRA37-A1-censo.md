# MAESTRA37-A1 · P0 — censo de lo nuevo en `descargas_mx` y mapeo de ids (COMMIT-1)

3/sep/2026 · rótulo `MAESTRA37-A1` · congelado ANTES de registrar nada.

Raíz `descargas_mx` = `/mnt/c/Users/PC0/Descargas MX` (por `data/raices.local.yaml`).


## 0 · Cifras crudas

- Archivos en el árbol de la raíz (recursivo, `os.walk`): **373**.
- Con `mtime >= 2026-09-03`: **149** — 131 en `ENSANUT2024-v2026-09-01/`, 17 sueltos en la raíz, 1 en `ICPSR_35024/`.
- **El encargo esperaba 129 en la subcarpeta; hay 131.** No es un error de mesa: la página viva
  declara 169 `ArchId` únicos, de los que 38 son `.spss` (excluidos por mesa) → 169 − 38 = **131**.
  Los 131 depositados tienen `ArchId` en la página; ninguno quedó sin procedencia.
- Colisiones de nombre contra el manifiesto (campo `archivo`): **0** — las entradas previa (fecha_descarga 2026-07-30; contenido con fecha interna 2026-01-08)
  llevan el basename pelado y las nuevas llevan `ENSANUT2024-v2026-09-01/<archivo>`, así que
  el guard de `--escanea` (mismo nombre, sha distinto → CONFLICTO) **no se dispara**; no hay
  nada que rodear.

## 1 · Bloque ENSANUT v2 — veredicto A.7 por archivo

| veredicto | n |
|---|---|
| CONTENIDO-DISTINTO | 10 |
| IDENTICO-YA-REGISTRADO | 6 |
| NUEVO-SIN-HOMONIMO | 115 |
| **total** | **131** |

`IDENTICO-YA-REGISTRADO` = el sha256 del archivo depositado ya está en el manifiesto bajo otro
id (los cuestionarios PDF/DOCX de julio, mismo byte). El registrador dedupica por hash y **no**
los va a registrar: es correcto, y se declara aquí para que el conteo cierre.

### 1.1 · Los 10 con homónimo previa (fecha_descarga 2026-07-30; contenido con fecha interna 2026-01-08) (zip Y contenido interno)

| archivo (v2) | id de la entrada previa | sha zip viejo→nuevo | interno: tamaño / fecha / sha viejo→nuevo | veredicto |
|---|---|---|---|---|
| `adolescentes_ensanut2024_w.csv.csv.zip` | `adolescentes_ensanut2024_w_csv_csv` | `3c5f21ef6158…` → `2b164ca9bd96…` | 4,240,707 / 2026-01-08 / `4e7308418308…` → 4,210,882 / 2026-09-01 / `4c61b21e00fa…` | CONTENIDO-DISTINTO |
| `adolescentes_ensanut2024_w.stata.stata.zip` | `adolescentes_ensanut2024_w_stata_stata` | `b528e00511ad…` → `47251c90bd41…` | 16,288,917 / 2026-01-08 / `56d5d07e6130…` → 16,575,279 / 2026-09-01 / `e36db7a5c267…` | CONTENIDO-DISTINTO |
| `hogar_ensanut2024_w_icb.csv.csv.zip` | `hogar_ensanut2024_w_icb_csv_csv` | `fb27bb64c3fb…` → `3dabe62e71ec…` | 6,391,078 / 2026-01-08 / `8bccd58efb80…` → 6,402,083 / 2026-09-01 / `03820d3fb286…` | CONTENIDO-DISTINTO |
| `integrantes_ensanut2024_w_icb.csv.csv.zip` | `integrantes_ensanut2024_w_icb_csv_csv` | `1dc1277b38b1…` → `c3aac85e9ea9…` | 23,120,111 / 2026-01-08 / `288bfa3b4a0e…` → 22,746,129 / 2026-09-01 / `d4d38f4d80fa…` | CONTENIDO-DISTINTO |
| `menores_ensanut2024_w.csv.csv.zip` | `menores_ensanut2024_w_csv_csv` | `df07aa31dfc8…` → `5143efedb8eb…` | 5,193,434 / 2026-01-08 / `01d9efbd467b…` → 5,159,135 / 2026-09-01 / `1a1e75d6bbd6…` | CONTENIDO-DISTINTO |
| `menores_ensanut2024_w.stata.stata.zip` | `menores_ensanut2024_w_stata_stata` | `cadf52a7127a…` → `02da5c14b593…` | 20,767,441 / 2026-01-08 / `d14f735d1f07…` → 21,074,435 / 2026-09-01 / `9adb7d7fce13…` | CONTENIDO-DISTINTO |
| `nse_Integrantes_ensanut_2024.csv.csv.zip` | `nse_integrantes_ensanut_2024_csv_csv` | `0315bc625b26…` → `0d83bf5473ac…` | 1,958,708 / 2026-01-08 / `6b5e2dc8dbb9…` → 1,994,727 / 2026-09-01 / `f5aed581ba0e…` | CONTENIDO-DISTINTO |
| `nse_hogar_ensanut_2024.csv.csv.zip` | `nse_hogar_ensanut_2024_csv_csv` | `685e33d003ca…` → `58db6c66c7cf…` | 388,338 / 2026-01-08 / `1e27ea54ae8c…` → 399,311 / 2026-09-01 / `e542a5f43b9c…` | CONTENIDO-DISTINTO |
| `utilizadores_ensanut2024_w.csv.csv.zip` | `utilizadores_ensanut2024_w_csv_csv` | `2836f15464e0…` → `997009ea0168…` | 1,392,437 / 2026-01-08 / `fe0273877bc0…` → 1,366,670 / 2026-09-01 / `1292371fb67e…` | CONTENIDO-DISTINTO |
| `utilizadores_ensanut2024_w.stata.stata.zip` | `utilizadores_ensanut2024_w_stata_stata` | `1fb44754452e…` → `b40a4dce264e…` | 5,152,126 / 2026-01-08 / `dd6c84e7ae80…` → 5,197,750 / 2026-09-01 / `707f590099d6…` | CONTENIDO-DISTINTO |

Los diez cambian el **contenido interno**, no sólo el empaquetado: ningún sha interno coincide,
y la fecha interna salta de `2026-01-08` a `2026-09-01` en los diez. Cero `RE-EMPAQUETADO`.
El hecho que mesa midió se reproduce exacto: `adolescentes_ensanut2024_w.dta` 16 288 917 B
(`56d5d07e61300ed0…`, 8/ene) → 16 575 279 B (`e36db7a5c267d30e…`, 1/sep).

### 1.2 · Los 6 idénticos a una entrada ya registrada

| archivo (v2) | id ya registrado | archivo de esa entrada |
|---|---|---|
| `adolescentes_ensanut2024_w.Cuestionarios.pdf` | `3_vfinal_cuestionario_adolescentes_ensanut_2024_etiquetas_cuestionarios` | `3 VFINAL Cuestionario adolescentes ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |
| `adultos_ensanut2024_w.Cuestionarios.pdf` | `4_vfinal_cuestionario_adultos_ensanut_2024_etiquetas_cuestionarios` | `4 VFINAL Cuestionario adultos ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |
| `hogar_ensanut_2024_etiquetas.Cuestionarios.pdf` | `1_vfinal_cuestionario_hogar_ensanut_2024_etiquetas_cuestionarios` | `1 VFINAL Cuestionario Hogar ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |
| `indice_bienestar.Cuestionarios.docx` | `indice_de_bienestar_cuestionarios` | `Indice de Bienestar.Cuestionarios.docx` |
| `menores_ensanut2024_w.Cuestionarios.pdf` | `2_vfinal_cuestionario_nios_0_a_9_ensanut_2024_etiquetas_cuestionarios` | `2 VFINAL Cuestionario nios 0 a 9 ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |
| `utilizadores_ensanut2024_w.Cuestionarios.pdf` | `5_vfinal_cuestionario_utilizadores_ensanut_2024_etiquetas_cuestionarios` | `5 VFINAL Cuestionario utilizadores ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf` |

### 1.3 · Copias sueltas en la raíz (las seis que mesa bajó primero)

| archivo suelto | copia en la subcarpeta | sha |
|---|---|---|
| `adultos_ensanut2024_w.stata.stata.zip` | `ENSANUT2024-v2026-09-01/adultos_ensanut2024_w.stata.stata.zip` | `0fa8f4436fa4…` |
| `nse_Integrantes_ensanut_2024.stata.stata.zip` | `ENSANUT2024-v2026-09-01/nse_Integrantes_ensanut_2024.stata.stata.zip` | `15426e13b941…` |
| `integrantes_ensanut2024_w_icb.stata.stata.zip` | `ENSANUT2024-v2026-09-01/integrantes_ensanut2024_w_icb.stata.stata.zip` | `20a9fae339da…` |
| `hogar_ensanut2024_w_icb.stata.stata.zip` | `ENSANUT2024-v2026-09-01/hogar_ensanut2024_w_icb.stata.stata.zip` | `440ff69a24d8…` |
| `adultos_ensanut2024_w.csv.csv.zip` | `ENSANUT2024-v2026-09-01/adultos_ensanut2024_w.csv.csv.zip` | `80c255f88242…` |
| `nse_hogar_ensanut_2024.stata.stata.zip` | `ENSANUT2024-v2026-09-01/nse_hogar_ensanut_2024.stata.stata.zip` | `fe6a01d2b5c3…` |

**Byte-idénticas** (mismo sha256). Se registra la copia de la subcarpeta; la suelta queda como
constancia y la bloquea el dedup por hash del propio registrador — no se borra nada del disco de mesa.

## 2 · Bloque ICPSR

| archivo | copias byte-idénticas | tamaño | formato |
|---|---|---|---|
| `ICPSR35024-ds1-w2-tabulados-T5-T9-derivados-2026-09-02.csv` | 5 (`(1)`…`(4)`) | 58 237 B | CSV, 647 filas + cabecera |
| `LEEME-ICPSR35024-ds1-w2-tabulados-T5-T9-procedencia-2026-09-02.txt` | 5 (`(1)`…`(4)`) | 35 212 B | texto |
| `ICPSR_35024/35024-Questionnaire-spanish.pdf` | 1 | 1 252 847 B | PDF |

Esquema del CSV (cabecera literal): `tabla,control_var,control_code,control_label,row_var,row_code,
row_label,col_var,col_code,col_label,n` — tabulados T5–T9 de la ola 2, en formato largo, una fila por
celda. El `LEEME` declara la procedencia: **salida de tabulador en línea pegada por el operador**,
no lectura de microdato; clase de procedencia (3) reportada, no verificada. Es la ronda 1; T9b no
aparece con nombre propio (el CSV cubre T5–T9 en un solo archivo).

## 3 · Bloque PDN (SESNA)

`PDN_S3v2.zip`, 1 459 284 B, 34 miembros: un directorio `faltas_graves_de_servidores_publicos/`
con un `.json` por entidad (`<entidad>_s3_servidores_publicos.json`), fechados 9/may/2025.
Es **sólo el S3**. La fila de cola pide `S1_S2_S3_S6` → el veredicto de cola es **OBTENIDO-PARCIAL**.

## 4 · Mapeo congelado de ids (D13)

Convención D13: `<slug del basename>__v2026_09_01`. El slug es el que `_derivar_id` produce
(basename sin la última extensión, no la ruta). `sustituye_a` = el id previa (fecha_descarga 2026-07-30; contenido con fecha interna 2026-01-08) cuando hay homónimo.

| id nuevo | archivo | sustituye_a |
|---|---|---|
| `actividad_fisica_ensanut2024_w_adultos_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/actividad_fisica_ensanut2024_w-adultos.Catálogo.xlsx` | `ninguno` |
| `actividad_fisica_ensanut2024_w_adultos_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/actividad_fisica_ensanut2024_w-adultos.Cuestionarios.pdf` | `ninguno` |
| `actividad_fisica_ensanut2024_w_adultos_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/actividad_fisica_ensanut2024_w-adultos.csv.csv.zip` | `ninguno` |
| `actividad_fisica_ensanut2024_w_adultos_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/actividad_fisica_ensanut2024_w-adultos.stata.stata.zip` | `ninguno` |
| `actividad_fisica_ensanut2024_w_ni_os_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/actividad_fisica_ensanut2024_w-niños.Catálogo.xlsx` | `ninguno` |
| `actividad_fisica_ensanut2024_w_ni_os_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/actividad_fisica_ensanut2024_w-niños.Cuestionarios.pdf` | `ninguno` |
| `actividad_fisica_ensanut2024_w_ni_os_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/actividad_fisica_ensanut2024_w-niños.csv.csv.zip` | `ninguno` |
| `actividad_fisica_ensanut2024_w_ni_os_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/actividad_fisica_ensanut2024_w-niños.stata.stata.zip` | `ninguno` |
| `adolescentes_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/adolescentes_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `adolescentes_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/adolescentes_ensanut2024_w.csv.csv.zip` | `adolescentes_ensanut2024_w_csv_csv` |
| `adolescentes_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/adolescentes_ensanut2024_w.stata.stata.zip` | `adolescentes_ensanut2024_w_stata_stata` |
| `adultos_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/adultos_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `adultos_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/adultos_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `adultos_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/adultos_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `antropometria_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/antropometria_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `antropometria_ensanut2024_w_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/antropometria_ensanut2024_w.Cuestionarios.pdf` | `ninguno` |
| `antropometria_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/antropometria_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `antropometria_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/antropometria_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `ensasangre24_determinaciones_micronutrimentos_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/ensasangre24_determinaciones_micronutrimentos.Catálogo.xlsx` | `ninguno` |
| `ensasangre24_determinaciones_micronutrimentos_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/ensasangre24_determinaciones_micronutrimentos.csv.csv.zip` | `ninguno` |
| `ensasangre24_determinaciones_micronutrimentos_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/ensasangre24_determinaciones_micronutrimentos.stata.stata.zip` | `ninguno` |
| `etiquetado_ensanut2924_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/etiquetado_ensanut2924_w.Catálogo.xlsx` | `ninguno` |
| `etiquetado_ensanut2924_w_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/etiquetado_ensanut2924_w.Cuestionarios.pdf` | `ninguno` |
| `etiquetado_ensanut2924_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/etiquetado_ensanut2924_w.csv.csv.zip` | `ninguno` |
| `etiquetado_ensanut2924_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/etiquetado_ensanut2924_w.stata.stata.zip` | `ninguno` |
| `formato_muestras_sangre_ensanut_2024_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/formato_muestras_sangre_ensanut_2024.Cuestionarios.pdf` | `ninguno` |
| `frec_adul_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_adul_ensanut2024_w_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_ensanut2024_w.Cuestionarios.pdf` | `ninguno` |
| `frec_adul_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_adul_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_adul_rec_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_rec_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_adul_rec_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_rec_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_adul_rec_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_rec_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_adul_sup_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_sup_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_adul_sup_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_sup_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_adul_sup_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_sup_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_adul_tor_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_tor_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_adul_tor_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_tor_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_adul_tor_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_adul_tor_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_es_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_es_ensanut2024_w_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_ensanut2024_w.Cuestionarios.pdf` | `ninguno` |
| `frec_es_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_es_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_es_rec_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_rec_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_es_rec_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_rec_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_es_rec_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_rec_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_es_sup_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_sup_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_es_sup_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_sup_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_es_sup_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_sup_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_es_tor_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_tor_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_es_tor_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_tor_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_es_tor_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_es_tor_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_pr_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_pr_ensanut2024_w_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_ensanut2024_w.Cuestionarios.pdf` | `ninguno` |
| `frec_pr_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_pr_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_pr_rec_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_rec_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_pr_rec_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_rec_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_pr_rec_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_rec_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_pr_sup_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_sup_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_pr_sup_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_sup_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_pr_sup_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_sup_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `frec_pr_tor_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_tor_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `frec_pr_tor_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_tor_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `frec_pr_tor_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/frec_pr_tor_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `hogar_ensanut2024_w_icb_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/hogar_ensanut2024_w_icb.Catálogo.xlsx` | `ninguno` |
| `hogar_ensanut2024_w_icb_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/hogar_ensanut2024_w_icb.csv.csv.zip` | `hogar_ensanut2024_w_icb_csv_csv` |
| `hogar_ensanut2024_w_icb_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/hogar_ensanut2024_w_icb.stata.stata.zip` | `ninguno` |
| `integrantes_ensanut2024_w_icb_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/integrantes_ensanut2024_w_icb.Catálogo.xlsx` | `ninguno` |
| `integrantes_ensanut2024_w_icb_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/integrantes_ensanut2024_w_icb.csv.csv.zip` | `integrantes_ensanut2024_w_icb_csv_csv` |
| `integrantes_ensanut2024_w_icb_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/integrantes_ensanut2024_w_icb.stata.stata.zip` | `ninguno` |
| `lactancia_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/lactancia_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `lactancia_ensanut2024_w_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/lactancia_ensanut2024_w.Cuestionarios.pdf` | `ninguno` |
| `lactancia_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/lactancia_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `lactancia_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/lactancia_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `menores_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/menores_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `menores_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/menores_ensanut2024_w.csv.csv.zip` | `menores_ensanut2024_w_csv_csv` |
| `menores_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/menores_ensanut2024_w.stata.stata.zip` | `menores_ensanut2024_w_stata_stata` |
| `nse_integrantes_ensanut_2024_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/nse_Integrantes_ensanut_2024.Catálogo.xlsx` | `ninguno` |
| `nse_integrantes_ensanut_2024_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/nse_Integrantes_ensanut_2024.csv.csv.zip` | `nse_integrantes_ensanut_2024_csv_csv` |
| `nse_integrantes_ensanut_2024_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/nse_Integrantes_ensanut_2024.stata.stata.zip` | `ninguno` |
| `nse_hogar_ensanut_2024_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/nse_hogar_ensanut_2024.Catálogo.xlsx` | `ninguno` |
| `nse_hogar_ensanut_2024_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/nse_hogar_ensanut_2024.csv.csv.zip` | `nse_hogar_ensanut_2024_csv_csv` |
| `nse_hogar_ensanut_2024_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/nse_hogar_ensanut_2024.stata.stata.zip` | `ninguno` |
| `plomo_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/plomo_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `plomo_ensanut2024_w_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/plomo_ensanut2024_w.Cuestionarios.pdf` | `ninguno` |
| `plomo_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/plomo_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `plomo_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/plomo_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `r24hrs_ensanut_2024_cuestionarios__v2026_09_01` | `ENSANUT2024-v2026-09-01/r24hrs_ensanut_2024.Cuestionarios.pdf` | `ninguno` |
| `rec24h_alim_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_alim_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_alim_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_alim_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_alim_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_alim_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `rec24h_desc_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_desc_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_desc_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_desc_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_desc_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_desc_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `rec24h_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `rec24h_obte_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_obte_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_obte_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_obte_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_obte_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_obte_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `rec24h_rev_alim_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_alim_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_rev_alim_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_alim_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_rev_alim_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_alim_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `rec24h_rev_desc_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_desc_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_rev_desc_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_desc_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_rev_desc_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_desc_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `rec24h_rev_obte_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_obte_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_rev_obte_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_obte_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_rev_obte_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_obte_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `rec24h_rev_rec_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_rec_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_rev_rec_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_rec_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_rev_rec_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_rec_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `rec24h_rev_sup_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_sup_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_rev_sup_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_sup_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_rev_sup_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_rev_sup_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `rec24h_sup_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_sup_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `rec24h_sup_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_sup_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `rec24h_sup_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/rec24h_sup_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `sangre_hemoglobina_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/sangre_hemoglobina_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `sangre_hemoglobina_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/sangre_hemoglobina_ensanut2024_w.csv.csv.zip` | `ninguno` |
| `sangre_hemoglobina_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/sangre_hemoglobina_ensanut2024_w.stata.stata.zip` | `ninguno` |
| `utilizadores_ensanut2024_w_cat_logo__v2026_09_01` | `ENSANUT2024-v2026-09-01/utilizadores_ensanut2024_w.Catálogo.xlsx` | `ninguno` |
| `utilizadores_ensanut2024_w_csv_csv__v2026_09_01` | `ENSANUT2024-v2026-09-01/utilizadores_ensanut2024_w.csv.csv.zip` | `utilizadores_ensanut2024_w_csv_csv` |
| `utilizadores_ensanut2024_w_stata_stata__v2026_09_01` | `ENSANUT2024-v2026-09-01/utilizadores_ensanut2024_w.stata.stata.zip` | `utilizadores_ensanut2024_w_stata_stata` |

Total de ids nuevos de ENSANUT v2: **125** (131 − 6 ya registrados por sha).

## 5 · P1 · A.7 doble descarga (previo a todo registro)

Receta usada, la que mesa midió — la página no trae enlaces, es POST a sí misma:

```
curl -s --max-time 300 -o <destino> -e <URL> --data "ArchId<b64>=" <URL>
URL = https://ensanut.insp.mx/encuestas/ensanutcontinua2024/descargas.php
<b64> = base64 de "01-Componente de SALUD/<carpeta>/<archivo>" (y análogo para nutrición),
        leído de los 169 ArchId de la página VIVA (no del descargas.php de julio que mesa
        guardó: ese es de la versión previa (fecha_descarga 2026-07-30; contenido con fecha interna 2026-01-08) y no describe lo que hoy sirve el portal).
```

- Archivos re-bajados: **131 / 131**.
- HTTP distinto de 200: **0**. `content_type`: `application/zip`, `application/pdf`,
  `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` según extensión.
- **COINCIDE por sha256 con lo depositado: 131 / 131. NO-COINCIDE: 0.**

El bloqueo que mesa observó era del cliente (el navegador devolvía la página en vez del
zip para algunos componentes); con la receta POST el servidor entrega los 131.
