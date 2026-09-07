# S11 · CRUCE — COMMIT-1 · congela el universo de búsqueda por pieza

`ACTO MAESTRA38-LOTE-CRUCE · A3-cruce + N16 + C + ENVIPE + COERCITIVO + LAPOP-21/23`.
Corrida 6/sep/2026, entorno **CAJA (Ubuntu, corpus montado)**, contra
`origin/main` = `b1be1438634e87cfc68b5ee1e27db0bd92617ac1`. `COMPUERTA: ninguna`
(declaración explícita del encargo). Encargo archivado verbatim en
`forense/encargos/2026-09-06-MAESTRA38-LOTE-CRUCE.md` (0-bis A.3, commit
`a0f167d`, empujado al primer minuto).

**Medición: cero.** Este acto cruza texto de reactivo contra instrumentos
mínimos. No emite veredicto de ninguna regla, no mueve ningún tier, no carga
nada al motor.

---

## 0 · A.8 — premisas del encargo verificadas contra el árbol, ANTES de escribir nada

Cinco. Las cinco se declaran; ninguna se hereda.

### 0.1 · `data/inventario-reactivos-descargas-mx-v1_2.tsv` NO es un archivo nuevo — ya existe en `main`, y está por debajo de `v1_1`

El encargo lo lista como «(nuevo)» en el PERÍMETRO. No lo es:

```
$ git log --oneline -1 -- data/inventario-reactivos-descargas-mx-v1_2.tsv
0cf0d59 [Cierre censo] /mapea las 9 reglas NO-ENCONTRADO contra los FD nuevos
$ wc -l data/inventario-reactivos-descargas-mx-v1_{0,1,2}.tsv
   28949 v1_0    42548 v1_1    28949 v1_2
$ md5sum data/inventario-reactivos-descargas-mx-v1_{0,2}.tsv
7a6d6462b60bdd83f9de47a8484d4c7a  ...-v1_0.tsv
7a6d6462b60bdd83f9de47a8484d4c7a  ...-v1_2.tsv
```

El `v1_2` que hay en `main` es una **copia byte-idéntica de `v1_0`**, 13 599
filas por debajo de `v1_1`. Un consumidor que lea «la versión más alta» hoy
lee **menos** corpus que el que lea `v1_1` — defecto de contenido, no de
formato, y ningún test lo atrapa. Este acto lo corrige de la única forma
compatible con «`v1_1` intacto»: **`v1_2` se reconstruye como superconjunto
estricto de `v1_1`** (`v1_1` + las filas nuevas de este acto), y `v1_1` no se
toca. El archivo se declara reemplazado, no ampliado — se dice, no se
esconde.

### 0.2 · Las tres fuentes de A4 y la base de protesta NO están bajo `descargas_mx` — están bajo `data_raw`

El encargo pide `tools/inventario_reactivos.py --raiz descargas_mx` sobre
ellas. El manifiesto dice otra cosa:

```
$ python3 - # sobre data/manifiesto.yaml, campo archivo: + campo raiz:
LOSMEX     113 entradas   raiz = {'data_raw'}
CULTC        6 entradas   raiz = {'data_raw'}
ECOPRED      1 entrada    raiz = {'data_raw'}
MMAD         2 entradas   raiz = (sin campo raiz:)     # A6_MMAD_PROTESTA_MEXICO/
$ python3 -c "os.walk" sobre "/mnt/c/Users/PC0/Descargas MX"   # raiz descargas_mx
losmexicanos_unam_iij            -> isdir False
cultura_constitucional_unam_iij  -> isdir False
ecopred2014                      -> isdir False
A6_MMAD_PROTESTA_MEXICO          -> isdir False
$ ls -d data/raw/{losmexicanos_unam_iij,cultura_constitucional_unam_iij,ecopred2014,A6_MMAD_PROTESTA_MEXICO}
  las cuatro existen
```

**Desvío declarado, no PARO** (ARRANQUE·2/3): la pieza (a) corre sobre
`data/raw` para estas cuatro subcarpetas, que es donde el manifiesto y el
disco coinciden en ponerlas. El nombre del archivo de salida se conserva
tal como el encargo lo fija (`…-descargas-mx-v1_2.tsv`) porque es el archivo
declarado en el PERÍMETRO y `v1_1` es su base; la procedencia real de cada
fila queda en su `payload_id` y en la cabecera del propio TSV.

### 0.3 · La lista C de 29 relaciones está en `§4` de la nota de A6, no en `§3`, y es un desglose por fuente, no una lista de filas

```
$ grep -n "^#\+ " forense/notas/2026-09-06-MAESTRA38-A6-resultados.md
  §3 = «Controles de soft-404 que este acto deja medidos»
  §4 = «Contra las premisas del encargo», punto 3: «Clase C "28 relaciones". Son 29 …»
```

El `§3` que el encargo cita no contiene la lista. El `§4.3` sí trae el
**conteo y el desglose por fuente**, pero no las 29 filas. «Copiar, no
re-derivar» se cumple así: las 29 filas se derivan mecánicamente de
`data/curacion-registro/relaciones.tsv` y **el desglose resultante se verifica
contra el de A6 §4.3 celda por celda** — si no cuadra, PARA.

```
$ python3 -c  # capa4_apertura_mapeo empieza por NO-ENCONTRADO
n = 29
ENFIH 7 · ENSAFI 6 · ENASIC 3 · ENBIARE 3 · CSES 2 ·
MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO 1 + MASS_MOBILIZATION_PROTEST_DATA_MEXICO 1 (= MMAD 2, «bajo dos nombres distintos») ·
MICROCREDIT_IMPACTS_RANDOMIZED_MICROCREDIT_PROGRAM_PLACEMENT_EXP 1 + MICROCREDIT_IMPACTS_COMPARTAMOS_RCT 1 (= MICROCREDIT ×2) ·
ISSP 1 · EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014 1 (= ECEPIE) ·
DENUNCIA_VINCULADA_CON_TENENCIA_DE_SEGURO 1 · CANAL_DE_ADQUISICION_REFERIDOS_FINTECH 1
```

**Cuadra exacto** con A6 §4.3, incluidas las dos anotaciones («MMAD bajo dos
nombres distintos», «MICROCREDIT ×2»). La derivación se acepta como copia
verificada.

### 0.4 · LAPOP 2021/2023 NO tienen «0 filas en el inventario»

`SELLO-2 §B` (7/sep) dice «en corpus, 0 filas en el inventario» y de ahí sale
la pieza (f). Contra el árbol:

```
$ python3 -c  # payload_id ~ 202[13]_LAPOP en data/inventario-reactivos-descargas-mx-v1_1.tsv
LAPOP2021   262 filas   262 con texto_reactivo
LAPOP2023   585 filas   584 con texto_reactivo   (3 payloads: .dta, .dta (1), .sav)
```

**La premisa no se reproduce**: los dos ya estaban inventariados **con
texto** desde `v1_1` (`MAESTRA37-A1`, 3/sep). El `0` de `SELLO-2` sale
probablemente de haber buscado el rótulo en minúsculas del manifiesto
(`mex_2021_lapop_…`) contra un `payload_id` que en el TSV va con la caja del
nombre de archivo real (`MEX_2021_LAPOP_…`) — identificar por rótulo y no por
identidad. La pieza (f) **no se cancela**: se reorienta a lo único que aún no
estaba verificado, que es la **condición de las tres `se_mueve_si`** — que
`clien1n`, `clien1na`, `vb2`, `AOJ11`, `AOJ12` aparezcan con su texto. Ese
control se corre contra el `.dta` mismo, no contra el inventario.

### 0.5 · `tools/ya_medido.py` — corrido, aunque el encargo declare que «no aplica»

Salida completa en el anexo A.8 del encargo archivado. Resumen:
`R7.3`/`R7.4`/`R7.6`/`R7.7`/`R10.3` → `MEDIDA-EN:` (no se reabren);
`tramite.gobierno_digital.coercitivo` → `NUNCA-MEDIDA` (que es exactamente la
premisa de la pieza (e), «única sin dato»).

---

## 1 · Universo de búsqueda declarado, por pieza — cerrado antes de abrir nada

Ninguna fuente entra a una pieza que no esté en su renglón. Todo veredicto
negativo de este acto declara el denominador de su renglón (A.13).

| pieza | universo de búsqueda (cerrado) | denominador declarado |
|---|---|---|
| **(a)** A3-cruce Ola 6 | `data/raw/losmexicanos_unam_iij/**` (113 archivos) + `data/raw/cultura_constitucional_unam_iij/**` (6) + `data/raw/ecopred2014/**` (1 `.zip`) + `data/raw/A6_MMAD_PROTESTA_MEXICO/**` (2), inventariados a `…-descargas-mx-v1_2.tsv` | **122 archivos**; de ellos **53** despachan con etiqueta (`.sav` 27, `.dta` 25, `.zip` 1) y **69** sólo con nombre de variable (`.csv` 27, `.xls` 22, `.xlsx` 15, `.tab` 1, `.pdf` 3 no despachados) |
| **(b)** N16 · R7.3/R7.6 | ENCUP 2012 (`encup_2012_base_datos_xlsx.xlsx`, 282 var) · CIDE-CSES 2015 (`UNIVERSO-2026-09/CSES/cide_cses2015_{estatal_pre,nacional_pos,nacional_pre}electoral.sav`, 3 archivos, **hoy con 0 filas en todo inventario** → los inventaría este acto) · CSES5 (`cses5_csv.zip`, 605 var) · Latinobarómetro 2024 (`latinobarometro2024_bd_stata.zip`, 333 var con texto) · LAPOP 2019 (221) / 2021 (262) / 2023 (195×3 payloads) | **8 payloads**, sobre `…-descargas-mx-v1_1/v1_2`, `…-ext-v1_0`, `…-v1_2` |
| **(c)** ENVIPE · R7.4 | los tres antecedentes no-espaciales de `C_completo` tal como `forense/prereg-caja/S5-L5-spec-v1_0.md` §3.1 los nombra (`AGRAVIO`, `FALLA_ESTATAL`, `RED_PREVIA`) + `URBANO`, contra todas las olas de ENVIPE presentes en el manifiesto (2011–2025) | **154 ids de manifiesto** con rótulo `envipe`; `7 673` filas en `…-ext-v1_0`, `23 467` en `…-v1_2` |
| **(d)** lista C | las **29** filas de `data/curacion-registro/relaciones.tsv` con `capa4_apertura_mapeo` que empieza por `NO-ENCONTRADO` (§0.3), buscadas por texto en `…-descargas-mx-v1_1` + `…-ext-v1_0` + `…-v1_2` + el `v1_2` nuevo | **29 relaciones** contra **≥ 284 000 filas** de inventario |
| **(e)** coercitivo | instrumento mínimo de `tramite.gobierno_digital.coercitivo` (`milpa/tramite.yaml`) y el `se_mueve_si` de sus dos entradas `coercitivo_*` en `milpa/tramite-ola5-propuesta-v0.yaml`: «tenencia **vigente** de e.firma **por persona**» — contra el inventario completo | los cuatro inventarios juntos |
| **(f)** LAPOP 21/23 | `MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta` y `MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta` bajo `descargas_mx/Descargas Manuales/`, leídos **directo** con `pyreadstat` | **2 archivos**; control = `clien1n`, `clien1na`, `vb2`, `AOJ11`, `AOJ12` |

---

## 2 · Criterio de cruce — «parecido nominal no cuenta» (juicio, declarado antes de aplicarlo)

Un ítem cubre un instrumento mínimo sólo si su **texto** (etiqueta de variable
o texto de reactivo) pregunta lo que el instrumento mínimo pregunta. Tres
etiquetas, y nada entre ellas:

- **`CUBIERTO-POR`** — el texto del ítem interroga el mismo constructo, con la
  misma dirección y sobre la misma población. Se cita fuente + `variable_id` +
  **texto verbatim**. Un nombre de variable sin texto **nunca** puede producir
  `CUBIERTO-POR`: sin texto no hay juicio, hay coincidencia de cadena.
- **`PARCIAL`** — el texto cubre el *driver* o el desenlace, pero no los dos;
  o cubre el constructo sobre una población distinta de la que el instrumento
  mínimo declara. Se cita igual, y se dice qué falta.
- **`SIN-COBERTURA-EN-ESTAS-FUENTES`** — nada en el universo declarado del
  renglón. Va con el denominador (A.13).

Lo que **no** cuenta: que el nombre de la variable se parezca al concepto
(`CONFIANZA`, `P24`, `jefe`); que un ítem mida el mismo dominio con otro
desenlace; que un catálogo mencione la fuente. El defecto que este criterio
existe para no repetir está escrito en `N12 §2.3` y en la firma verbatim del
4/sep.

---

## 3 · Qué NO hace este acto

No mide ninguna regla ni emite `p`. No mueve ningún tier ni `situacion`. No
escribe `S5 v1.1` (la pieza (c) sólo dice si CUBRE). No escribe la spec `N7`
de la pieza (e). No edita `data/curacion-registro/relaciones.tsv`, ni
`data/manifiesto.yaml`, ni `data/cola-adquisicion-v1_0.tsv`, ni
`milpa/tramite.yaml`, ni `milpa/tramite-ola5-propuesta-v0.yaml`, ni las specs
`S1`–`S10`, ni `tests/*.py`, ni `tools/*.py`. No descarga nada (sin red).

**Una pieza que PARA no tumba el lote** — verbatim del encargo. Cada pieza
reporta su propio estado en `forense/notas/2026-09-06-MAESTRA38-LOTE-CRUCE-resultados.md`.

**El primer resultado que produzca este procedimiento es el que se reporta.**
