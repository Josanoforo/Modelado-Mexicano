# MAESTRA36-A1 · P0 · BARRIDO de las dos rutas de descargas contra el manifiesto

**Acto:** MAESTRA36-A1 · ESCANEA-RECURSIVO-Y-REGISTRA-DESCARGAS
**Encargo:** `forense/encargos/2026-09-02-MAESTRA36-A1-ESCANEA-RECURSIVO-Y-REGISTRA-DESCARGAS.md` (SHA de redacción 9af8407)
**Fecha:** 2026-09-02 · **Caja:** Ubuntu (WSL2), clon `/home/pc0/mm-maestra36-a1`
**Herramienta:** `tools/barrido_descargas_vs_manifiesto.py` (creada en este acto, verbatim del anexo del encargo)

> **Frase de sello:** «el primer resultado que produzca este procedimiento es el
> que se reporta». La salida cruda de abajo es la de la PRIMERA corrida del
> script sobre las dos rutas de la firma, en el orden de la firma. No se
> re-corrió para afinarla.

---

## 1 · Lo que contestó la firma de mesa

La firma dice: «tenemos dos carpetas de descargas. `C:\Users\PC0\Descargas MX\Descargas
Manuales` y `C:\Users\PC0\Descargas MX` posiblemente se corrió la estructura de codex
solo para 1 carpeta».

**No son dos carpetas: son una carpeta y su subcarpeta.** El barrido lo mide: al pasar
la segunda ruta por separado, examinó 0 archivos porque sus 76 ya habían sido cubiertos
al recorrer la primera. La intuición de mesa era correcta en la consecuencia (se corrió
sobre una sola cosa) y precisa en la causa una vez nombrada: `--escanea` usaba
`os.listdir`, que ve el nivel superior y no entra a la subcarpeta. Los 76 archivos de
`Descargas Manuales/` no eran para `--escanea` ni «nuevos» ni «ya registrados»:
**no existían**. Por eso a mesa se le volvió a pedir lo que ya había bajado.

Estructura real del árbol, medida (`find -type d`, 2 directorios examinados):

```
/mnt/c/Users/PC0/Descargas MX/
/mnt/c/Users/PC0/Descargas MX/Descargas Manuales/
```

No hay ninguna otra subcarpeta. En particular **no existe `academico/icpsr35024/crosstabs/`**,
que es donde el transfer maestra-35 §7 suponía que vivían los crosstabs del Mexico Panel
(ver §5, P3).

## 2 · Universo (A.13) — una cifra, con un solo mecanismo

El encargo señala que tres actos declararon tres universos distintos sobre esta misma
raíz en dos días: A4 (1/sep) 122 archivos · A1-2 (1/sep) 160 · A1-3 (2/sep) 190. Tres
mecanismos, no tres corpus. Este acto lo mide una vez:

| mecanismo | archivos |
|---|---|
| `tools/barrido_descargas_vs_manifiesto.py` (os.walk, sha256) | **224** |
| `tests/manifiesto.py --escanea` **parchado** (os.walk) | **224** |
| `tests/manifiesto.py --escanea` **sin parchar** (os.listdir) | 148 |
| `find "$RAIZ" -type f` (control independiente) | 224 |

Los dos mecanismos que este acto usa coinciden en **224**, y coinciden también en el
desglose (183 registrados · 41 no registrados · 0 conflictos de nombre). La cifra vieja
de 148 es exactamente el nivel superior; 224 − 148 = 76 = los archivos de la subcarpeta.

## 3 · Salida cruda del barrido, íntegra

```
manifiesto: /home/pc0/mm-maestra36-a1/data/manifiesto.yaml · entradas con sha256: 1065

=== /mnt/c/Users/PC0/Descargas MX
   archivos examinados: 224 · REGISTRADO(sha coincide): 183 · NO-REGISTRADO: 41 · MISMO-NOMBRE-OTRO-SHA: 0
   NO-REGISTRADO       658,933  DescargaMasiva_582026_175614.zip
   NO-REGISTRADO       605,512  DescargaMasiva_682026_95355.zip
   NO-REGISTRADO       604,834  DescargaMasiva_682026_9540.zip
   NO-REGISTRADO       688,618  DescargaMasiva_682026_95418.zip
   NO-REGISTRADO       602,522  DescargaMasiva_682026_95423.zip
   NO-REGISTRADO       602,173  DescargaMasiva_682026_9548.zip
   NO-REGISTRADO       120,320  Descargas Manuales/DecAnuaTipCon (1).xls
   NO-REGISTRADO       120,320  Descargas Manuales/DecAnuaTipCon.xls
   NO-REGISTRADO       265,728  Descargas Manuales/FORMATO_9_Impuesto.xls
   NO-REGISTRADO        92,160  Descargas Manuales/FirEleNumcert.xls
   NO-REGISTRADO        98,304  Descargas Manuales/FirEleNumcontri.xls
   NO-REGISTRADO       153,600  Descargas Manuales/IngresosTributarios.xls
   NO-REGISTRADO        87,040  Descargas Manuales/NumPagTipCon.xls
   NO-REGISTRADO        99,328  Descargas Manuales/NumPagosMedRec.xls
   NO-REGISTRADO       126,464  Descargas Manuales/PorEntFed.xls
   NO-REGISTRADO       117,760  Descargas Manuales/PorTipoContribuyente.xls
   NO-REGISTRADO        69,424  Descargas Manuales/TC-OECD-Trust-Survey-PUM-2021-2023-2025.docx
   NO-REGISTRADO        24,399  Descargas Manuales/export_crudo.txt
   NO-REGISTRADO     2,345,101  Descargas Manuales/itindc_202601.pdf
   NO-REGISTRADO     2,225,169  Descargas Manuales/itindc_202602.pdf
   NO-REGISTRADO       927,252  Descargas Manuales/itindp_202601.pdf
   NO-REGISTRADO       873,759  Descargas Manuales/itindp_202602.pdf
   NO-REGISTRADO       789,913  Descargas Manuales/itinfp_202601.pdf
   NO-REGISTRADO       692,058  Descargas Manuales/itinfp_202602.pdf
   NO-REGISTRADO     1,027,668  Descargas Manuales/itingf_202602.pdf
   NO-REGISTRADO       851,973  Descargas Manuales/itinin_202601.pdf
   NO-REGISTRADO       789,951  Descargas Manuales/itinin_202602.pdf
   NO-REGISTRADO       847,197  Descargas Manuales/itinse_202601.pdf
   NO-REGISTRADO       724,899  Descargas Manuales/itinse_202602.pdf
   NO-REGISTRADO        15,532  LEEME 2-procedencia.txt
   NO-REGISTRADO        15,532  LEEME-procedencia (1).txt
   NO-REGISTRADO        15,532  LEEME-procedencia (2).txt
   NO-REGISTRADO        15,532  LEEME-procedencia (3).txt
   NO-REGISTRADO         1,383  LEEME-procedencia.txt
   NO-REGISTRADO       141,181  descargas.php
   NO-REGISTRADO        24,399  export_crudo.txt
   NO-REGISTRADO        34,831  icpsr35024-ds1-w2-crosstabs-derivadas (1).csv
   NO-REGISTRADO        34,831  icpsr35024-ds1-w2-crosstabs-derivadas (2).csv
   NO-REGISTRADO        34,831  icpsr35024-ds1-w2-crosstabs-derivadas (3).csv
   NO-REGISTRADO        34,831  icpsr35024-ds1-w2-crosstabs-derivadas.csv
   NO-REGISTRADO         3,364  icpsr35024_DS1_W2_crosstabs_derivado_v0.csv

=== /mnt/c/Users/PC0/Descargas MX/Descargas Manuales
   archivos examinados: 0 · REGISTRADO(sha coincide): 0 · NO-REGISTRADO: 0 · MISMO-NOMBRE-OTRO-SHA: 0 · ya cubiertos por una raíz anterior (subcarpeta): 76

A.13: los conteos de arriba son por comando os.walk; un 0 en NO-REGISTRADO con 'archivos examinados' > 0 sí es un negativo.
```

## 4 · Clasificación de los 41 NO-REGISTRADO — a mano, sin script

El script cruza por sha256 contra el manifiesto, pero **no deduplica los hallazgos entre
sí**. Medido aparte (sha256 de las 41 rutas): las 41 rutas son **33 objetos distintos**.
Ocho rutas son copias byte-idénticas de otra ruta del mismo árbol — el patrón `(1)`,
`(2)`, `(3)` que deja el navegador al re-descargar. Eso no las hace ajenas: son el mismo
objeto, y se registra **una ruta por sha256**.

La identidad de cada archivo se verificó abriendo el contenido, no leyendo el nombre
(los `.xls` con `xlrd`, el `.docx` por `word/document.xml`, los `.zip` por su
`DescargaMasivaOD.xml`, los `.pdf` por texto extraído, el `.php` por su `<title>`).

### (a) dato del proyecto CON fila de cola identificable — 23 rutas · 15 objetos

| objeto (ruta canónica) | bytes | sha256 | copias byte-idénticas | fila de cola |
|---|---:|---|---|---|
| `Descargas Manuales/DecAnuaTipCon.xls` | 120 320 | `5965d4af…` | `DecAnuaTipCon (1).xls` | `NUEVA-L6` SAT_MEXICO |
| `Descargas Manuales/FORMATO_9_Impuesto.xls` | 265 728 | `2735dc81…` | — | `NUEVA-L6` SAT_MEXICO |
| `Descargas Manuales/FirEleNumcert.xls` | 92 160 | `e813b6c1…` | — | `NUEVA-L6` SAT_MEXICO |
| `Descargas Manuales/FirEleNumcontri.xls` | 98 304 | `dce5a06c…` | — | `NUEVA-L6` SAT_MEXICO |
| `Descargas Manuales/IngresosTributarios.xls` | 153 600 | `e4eca9de…` | — | `NUEVA-L6` SAT_MEXICO |
| `Descargas Manuales/NumPagTipCon.xls` | 87 040 | `0a146752…` | — | `NUEVA-L6` SAT_MEXICO |
| `Descargas Manuales/NumPagosMedRec.xls` | 99 328 | `975b8f73…` | — | `NUEVA-L6` SAT_MEXICO |
| `Descargas Manuales/PorEntFed.xls` | 126 464 | `51f79b5a…` | — | `NUEVA-L6` SAT_MEXICO |
| `Descargas Manuales/PorTipoContribuyente.xls` | 117 760 | `d14769a7…` | — | `NUEVA-L6` SAT_MEXICO |
| `icpsr35024_DS1_W2_crosstabs_derivado_v0.csv` | 3 364 | `96330f03…` | — | `:19` MEXICO_PANEL_STUDY_2012 |
| `icpsr35024-ds1-w2-crosstabs-derivadas.csv` | 34 831 | `a85c59ae…` | `(1)`, `(2)`, `(3)` | `:19` MEXICO_PANEL_STUDY_2012 |
| `export_crudo.txt` | 24 399 | `daa29e0b…` | `Descargas Manuales/export_crudo.txt` | `:19` MEXICO_PANEL_STUDY_2012 |
| `LEEME-procedencia.txt` | 1 383 | `c98ce68b…` | — | `:19` MEXICO_PANEL_STUDY_2012 |
| `LEEME 2-procedencia.txt` | 15 532 | `9f0a7da9…` | `LEEME-procedencia (1)/(2)/(3).txt` | `:19` MEXICO_PANEL_STUDY_2012 |
| `Descargas Manuales/TC-OECD-Trust-Survey-PUM-2021-2023-2025.docx` | 69 424 | `4a3ac6d7…` | — | `:37` OECD |

**Identidad verificada, no supuesta.** Los nueve `.xls` son estadística tributaria del
SAT: la primera hoja de `IngresosTributarios.xls` dice «Recaudación / Ingresos
tributarios / Ingresos por impuesto (Millones de …)»; la de `PorEntFed.xls`, «Padrón /
Por entidad federativa / Número de contribuyentes activos»; la de `FirEleNumcert.xls`,
«Factura y e.firma / e.firma / Certificados emitidos». Son el objeto de la fila
`SAT_MEXICO`, que estaba en `NO-ACCESIBLE-DESDE-LA-CAJA(firma c1)` porque `sat.gob.mx`
sirve a la caja el cascarón de una SPA sin texto: mesa los bajó a mano, que es
exactamente lo que esa fila pedía.

El `.docx` **no es microdato**: es el formulario *Terms of Use* del OECD Trust Survey
Public Use Microdata File, y su propio texto dice que el acceso se pide firmando y
enviando ese formulario a `govtrustinfo@oecd.org`. Es el instrumento de acceso, no el
dato — ver §5, P3.

### (b) dato del proyecto SIN fila de cola — 18 rutas · 18 objetos

| objeto | bytes | sha256 | qué es |
|---|---:|---|---|
| `Descargas Manuales/itindc_202601.pdf` | 2 345 101 | `446304b3…` | SHCP, Informe Trimestral 2026-T1 · documento completo (70 pp) |
| `Descargas Manuales/itindc_202602.pdf` | 2 225 169 | `29679582…` | SHCP, Informe Trimestral 2026-T2 · documento completo |
| `Descargas Manuales/itindp_202601.pdf` | 927 252 | `c1c14926…` | SHCP 2026-T1 · Deuda Pública |
| `Descargas Manuales/itindp_202602.pdf` | 873 759 | `83977c7e…` | SHCP 2026-T2 · Deuda Pública |
| `Descargas Manuales/itinfp_202601.pdf` | 789 913 | `5b939476…` | SHCP 2026-T1 · Finanzas Públicas |
| `Descargas Manuales/itinfp_202602.pdf` | 692 058 | `b2454dbe…` | SHCP 2026-T2 · Finanzas Públicas |
| `Descargas Manuales/itingf_202602.pdf` | 1 027 668 | `294c159a…` | SHCP 2026-T2 · Informe de Avance de Gestión Financiera |
| `Descargas Manuales/itinin_202601.pdf` | 851 973 | `b55636e5…` | SHCP 2026-T1 · Introducción |
| `Descargas Manuales/itinin_202602.pdf` | 789 951 | `3f868041…` | SHCP 2026-T2 · Introducción |
| `Descargas Manuales/itinse_202601.pdf` | 847 197 | `548fa327…` | SHCP 2026-T1 · Situación Económica |
| `Descargas Manuales/itinse_202602.pdf` | 724 899 | `9ac88caf…` | SHCP 2026-T2 · Situación Económica |
| `DescargaMasiva_582026_175614.zip` | 658 933 | `cc0f6104…` | INEGI · carrito: **8 002 URLs**, 51.00 GB, 136 programas |
| `DescargaMasiva_682026_95418.zip` | 688 618 | `62d6fd42…` | INEGI · carrito: **15 599 URLs**, 14.50 GB, 171 programas |
| `DescargaMasiva_682026_95355.zip` | 605 512 | `0052d378…` | INEGI · carrito: 970 URLs, 27.48 GB (DENUE) |
| `DescargaMasiva_682026_9540.zip` | 604 834 | `d40383d2…` | INEGI · carrito: 568 URLs, 706.69 MB, 51 programas |
| `DescargaMasiva_682026_95423.zip` | 602 522 | `026acbad…` | INEGI · carrito: 71 URLs, 18.43 GB (boletines Sala de Prensa) |
| `DescargaMasiva_682026_9548.zip` | 602 173 | `56ca8b51…` | INEGI · carrito: 3 URLs, 1.21 GB (INV 2020 / SCINCE) |
| `descargas.php` | 141 181 | `361ac35f…` | página guardada de ENSANUT Continua 2024 (no es dato) |

Los once PDF son los *Informes sobre la Situación Económica, las Finanzas Públicas y la
Deuda Pública* de la SHCP, trimestres 1 y 2 de 2026 (identificados por texto extraído:
«II. Informe sobre la situación económica», «VI. Informe de Avance de Gestión Financiera
2026 … Ley de Fiscalización y Rendición de Cuentas de la Federación»). **No hay fila de
cola para SHCP**: las únicas filas `EXT_OF_*` de informes son ASF (`:66`) y SESNA
(`:69`). Entran al manifiesto y al registro como activo sin necesidad — no se les
inventa una `N` de `necesidad-objeto-modelo.tsv`.

Los seis `.zip` de *Descarga Masiva* son la herramienta lanzadora de INEGI
(`DescargaMasivaApp.exe` + `leeme.txt` + `DescargaMasivaOD.xml`), no microdato. El
manifiesto ya tiene siete entradas de esta familia con ese mismo criterio
(`descargamasiva_3072026_*`, `cngmd2023_descarga_masiva_app_y_orden_zip`,
`descargamasiva_1382026_134046`), así que se sigue el precedente. Los seis XML traen
token `aut=` y suman **25 213 URLs de descarga directa de `www.inegi.org.mx`** — es un
inventario de adquisición, y por eso valen su entrada aunque el `.exe` no sea dato.

### (c) ajeno o dudoso — 0 objetos

**La clase (c) está vacía, y es un negativo con universo declarado:** se examinaron los
41 NO-REGISTRADO, uno por uno, abriendo el contenido. Ninguno resultó ajeno al proyecto
ni de identidad dudosa. Es el resultado esperable: `descargas_mx` es carpeta curada, no
el destino por defecto del navegador — es `downloads` la raíz que `manifiesto.py` acota
por extensión justamente por el riesgo que aquí no se materializó (MAP-1b).

Por tanto **FP-258 no se abre por clase (c)**: el encargo la reservó «solo si la clase no
está vacía», y está vacía.

## 5 · Contador derivado de P0 (lo que P2 tiene que registrar)

| concepto | cifra |
|---|---:|
| archivos en el árbol (A.13, os.walk) | 224 |
| ya registrados por sha256 | 183 |
| NO-REGISTRADO (rutas) | 41 |
| NO-REGISTRADO (objetos distintos por sha256) | 33 |
| — clase (a), con fila de cola | 15 |
| — clase (b), sin fila | 18 |
| — clase (c), ajeno o dudoso | **0** |
| rutas que son copia byte-idéntica de otra | 8 |
| MISMO-NOMBRE-OTRO-SHA | 0 |
| de los 33, no promovibles (página guardada `.php`) | 1 |
| **N = entradas nuevas de manifiesto que P2 debe producir** | **32** |

Manifiesto: **1 070 → 1 102** si P2 registra los 32. La cifra se reporta al cerrar
contra lo que el manifiesto realmente tenga, no contra esta previsión.

`MISMO-NOMBRE-OTRO-SHA = 0` es un negativo con universo: el comando examinó 224 archivos
y comparó cada basename contra los 1 070 `archivo:` del manifiesto. Ningún archivo del
disco comparte nombre con una entrada registrada teniendo contenido distinto — no hay
que arbitrar ninguna colisión.

## 6 · Lo que P0 NO decidió

- No se registró nada: P0 es solo lectura y no escribe en el manifiesto.
- No se borró ninguna de las 8 copias duplicadas del disco. Este acto no toca el disco
  de mesa; solo decide qué ruta es la canónica en el manifiesto.
- No se buscó nada en red. Todo veredicto de ausencia de este acto es
  `NO-ENCONTRADO-EN-DISCO` con la ruta examinada, nunca `NO-OBTENIDO`.
