# CRÉDITO 2024 · eje escolaridad medido bien · spec v1.0

CALC: `CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002`. ACTO
GEN2-DIN-CREDITO-ESCOLARIDAD-2, 22/sep/2026, CAJA. Encargo archivado por
A.3 en `forense/encargos/2026-09-22-GEN2-DIN-CREDITO-ESCOLARIDAD-2.md`
(sha256 de cuerpo `a44e3c090a7b95565c651b480cb33d84b1b7f1691474bb8fe173d785bca3623d`);
firma de mesa en `…-ESCOLARIDAD-2-ADENDA-1.md` (sha256 de cuerpo
`290c0d2b2803908d33ab0794a7661dff17834e2f94c4cad917a8e01ff2770258`):
`FP-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01`, opción (a).

Sucesor, **no edición**, de `CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001`
(sellado, corrida `…--7219a9bcd364`, `REPRODUCE`/`IDENTICO`). El `-0001` no se
toca (E.3); sus 12 celdas no-escolaridad siguen vigentes y aquí son **oro**.
No se declara `repite_de`: eso marcaría el `-0001` entero como superado, y
sólo su eje escolaridad queda `VENCIDO-EN-ALCANCE → -0002` (A.10).

Escrita sin abrir ninguna fila de microdato. Leído para escribirla: el
código y los `resultados.json` sellados que se citan abajo, y —estructura,
A.15— los catálogos `catalogos/niv.csv` (TMODULO 2024) y
`catalogos/p3_1_1.csv` (TMODULO 2021) y las filas del diccionario de datos
de `niv`/`p3_1_1`, dentro de los zips del manifiesto.

El primer resultado que produzca este procedimiento es el que se reporta.

## 0 · Qué cambia y qué no

**Cambia una sola cosa: el mapa `niv` → cuatro cubos se aplica sobre los dos
dígitos de `niv` intactos.** El `-0001`
(`medidor.py:153`, `code = {c: m._code(d[c]) …}`) pasaba `niv` por `_code()`
de `CALC-PISOS-ENIF2021-EJES-0003` (`medidor.py:31-32`, regex `^0+(?=\d)`),
diseñada para el código de un dígito de 2021: "01".."09" pasaban a "1".."9"
y no calzaban con las llaves de dos dígitos de `NIV_A_ESCOLARIDAD`
(`medidor.py:84-89`). Medido en su `resultados.json`: K1 con
HASTA-PRIMARIA/SECUNDARIA/MEDIA-SUPERIOR `N=0` y SUPERIOR `N=283` de 12 379
(sólo `niv` 10/11).

**No cambia nada más** (encargo §5, paro d): candidatos, criterio,
vocabulario de veredicto (incluido lo inalcanzable por diseño y
`NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO`), universo 18-70, lista blanca de
9 conductas, `fac_per`, diseño `est_dis`/`upm_dis`, dicotomización, 10 000
réplicas `PCG64(42)` del marginal y 10 000 réplicas sintéticas
`PCG64(20260922)` con su orden de consumo. Todo eso **no se re-escribe: se
ejecuta por bytes** desde los archivos sellados (§2).

## 1 · Mapa `niv` 2024 → cubo, por texto del catálogo (A.15c)

Árbitro: el mapa de `_school()` sobre `P3_1_1` 2021
(`CALC-PISOS-ENIF2021-EJES-0003/medidor.py:41-45`: 0-2 hasta_primaria,
3 secundaria, 4-7 media_superior, 8-9 superior), leído contra el texto de
`conjunto_de_datos_tmodulo_enif_2021/catalogos/p3_1_1.csv`. Diccionario 2024:
«Pregunta P3.1.1 ¿Hasta qué año o grado aprobó usted en la escuela? - NIVEL,
2, C, niv, niv, "00...11,99"» — dos caracteres, tipo carácter.

| `niv` 2024 | texto `catalogos/niv.csv` 2024 (verbatim) | par textual 2021 (`p3_1_1`) | cubo |
|---|---|---|---|
| 00 | Ninguno | 0 Ninguno | hasta_primaria |
| 01 | Preescolar o kínder | 1 Preescolar o kínder | hasta_primaria |
| 02 | Primaria | 2 Primaria | hasta_primaria |
| 03 | Secundaria | 3 Secundaria | secundaria |
| 04 | Normal básica | 5 Normal básica | media_superior |
| 05 | Estudios técnicos con secundaria terminada | 4 Estudios técnicos con secundaria terminada | media_superior |
| 06 | Preparatoria o bachillerato | 6 Preparatoria o bachillerato | media_superior |
| 07 | Estudios técnicos con preparatoria terminada | 7 Estudios técnicos con preparatoria terminada | media_superior |
| 08 | Licenciatura o ingeniería (profesional) | 8 Licenciatura o ingeniería (profesional) | superior |
| 09 | Especialidad | — (sin par textual; ver abajo) | superior |
| 10 | Maestría | 9 Maestría o doctorado | superior |
| 11 | Doctorado | 9 Maestría o doctorado | superior |
| 99 | No sabe | 99 No sabe | sin cubo |

`04`/`05` vienen en orden inverso a 2021 (4/5): mismo cubo, sin efecto.
**`09` Especialidad** es el único código sin par textual: es un posgrado
posterior a la licenciatura; sus dos homólogos posibles en 2021 (8
Licenciatura y 9 Maestría o doctorado) caen ambos en `superior`, así que el
cubo es evidente y **no se lleva a mesa** (encargo §6: la pregunta es para
«un código sin cubo evidente»). Se declara aquí.

El mapa resultante es **idéntico** al `NIV_A_ESCOLARIDAD` del `-0001`
(`medidor.py:84-89`): aquel mapa era correcto; el defecto era sólo `_code`.
El test lo exige.

**Lectura de `niv` (`_niv_dos_digitos`):** el valor se toma del marco crudo
(`abierto["marco"]["niv"]`, leído por `_csv` de `-EJES-0003` con
`dtype=str`), se recortan blancos, y un dígito suelto (`"1"`) se completa a
`"01"` — mismo código; nunca se quita un cero. Vacío o `99` → sin cubo (NA),
fuera de las 4 celdas de escolaridad, como en 2021.

## 2 · Lo heredado, por bytes (inputs `origen: repo` con sha256)

| input | archivo | sha256 | uso |
|---|---|---|---|
| `MEDIDOR-ADJ-0001` | `data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001/medidor.py` | `01091733…3ee348` | guardia `abre_conducta_2024`, `COLUMNA_2024`, `_desenlace`, `medir()` |
| `MEDIDOR-EJES-0003` | `data/corrida0/CALC-PISOS-ENIF2021-EJES-0003/medidor.py` | `d069f38b…fea06a3` | `_csv`, `_cells`, `_estimate` (vía el `-0001`) |
| `R-ADJ-0001` | `…-ADJUDICACION-0001/resultados.json` | `95f027ef…864e26` | oro (§3) |
| `EMISIONES-0001` | `…-EMISIONES-0001/resultados.json` | `aa0db17c…3008cd` | candidatos (§4) |
| `ADJUDICADOR-0001` | `tools/duelo/credito_prediccion_2024.py` | `808a3c17…537a337` | regla de adjudicación del commit_3 |
| `CRUCES-FAMILIA` | `tools/duelo/cruces_familia.py` | `a41bdb07…f9ee3b` | `adjudica()`/`puntuadas()` de referencia |

(sha completos en `spec.yaml`.) `medidor.py` de este CALC carga el módulo del
`-0001` y reemplaza en su espacio de nombres exactamente dos nombres:
`PREFIJO` → `DIN-CREDITO-PREDICCION-2024-ESC2` (ids propios: el registro para
con `ID-DUPLICADO` si dos CALC sin cadena `repite_de` emiten el mismo id) y
`abre_conducta_2024` → envoltura que **primero llama a la guardia sellada**
(que sigue lanzando `ReservaRota` antes de abrir el ZIP) y después reescribe
sólo `ejes["escolaridad"]` y `codigos["niv"]` con §1. `medir()` es el del
`-0001`, sin copia.

**Reserva (encargo §3 `[SUPUESTO]`, verificado):** este código lee las mismas
columnas (incluida `niv`, en `cols_base` de las 9 conductas) de las mismas 9
conductas que la corrida sellada del `-0001` ya leyó con su guardia; ningún
CALC del árbol con predicción sellada y sin adjudicar depende de estas celdas
(los tres CALC sin `ejecucion.json` que citan ENIF 2024 —`DINERO-FAMILIARES-VEJEZ-0001`,
`HORIZONTE-VIA-DERIVADOS-0001`, `TIENE-AHORROS-0001`— son de ahorro y tienen
sucesor `v1_1` corrido). No queda celda no derivada que la reserva proteja.

**Emisiones (encargo §3 `[EXISTE]`, verificado): el defecto NO las afecta.**
`-EMISIONES-0001` sólo opera sobre los RESULT sellados de los pisos
2012/2015/2018/2021-recorte1870, cuya escolaridad está completa: suma de N de
los 4 cubos de K1 contra `NACIONAL-TODOS-N` = 6 109/6 113, 6 039/6 039,
12 439/12 446, 12 406/12 406. No se re-emite: la rama prevista en §3 del
encargo no se toma.

## 3 · Oro de las 12 celdas sanas (E.5)

Todo RESULT del `-0001` cuyo id no contiene `-ESCOLARIDAD-` (12 celdas × 6
campos × 9 conductas + `N-UNIVERSO` y `FILAS-18-70` × 9 = **666** ids) se
compara con su par `ESC2` de este CALC. Tolerancia absoluta
`oro_tolerancia_abs = 1e-10` (la `tolerancia` sellada del `-0001`); `None`
sólo casa con `None`. Se espera Δ = 0 exacto: `_estimate` sortea las réplicas
sobre el marco de diseño entero (no depende de qué celdas se piden) y la
matriz conserva forma y orden (16 columnas); sólo cambian las máscaras de
las 4 celdas de escolaridad. Salida: `ORO-N-COMPARADOS`, `ORO-N-DISCORDANTES`,
`ORO-MAX-ABS-DIFF`, `ORO-VEREDICTO` (`REPRODUCE-ORO` | `NO-REPRODUCE-ORO`),
`ORO-PRIMEROS-DISCORDANTES`. **Si sale `NO-REPRODUCE-ORO`, el hallazgo es ése
y el acto para en f) con el diff** (encargo §5).

Diagnóstico por conducta: `ESCOLARIDAD-N-SIN-CUBO` = `NACIONAL-TODOS-N` −
suma de N de los 4 cubos (personas con `niv` 99 o vacío).

## 4 · Adjudicación: la regla sellada, con universo actualizado (A.10)

La regla es la de `-ADJUDICACION-0001/spec.yaml` `regla_adjudicacion` y
`DIN-CREDITO-PREDICCION-2024-ADJUDICACION-spec-v1_1.md` §6, ejecutada por
bytes (`ADJUDICADOR-0001::adjudica_conducta`, con `CRUCES-FAMILIA`): piso
`PERSISTENCIA`; retador primario la `TENDENCIA-X` habilitada de menor MAE
puntual; ΔMAE = MAE(piso) − MAE(retador) en pp, IC95 percentil de 10 000
réplicas sintéticas desde el SE analítico; `umbral_vence_pp = inf`
(`VENCE-RETADOR` inalcanzable por diseño), `umbral_reserva_pp = 0`;
cobertura «R dentro del IC del candidato» con Wilson. Un generador nuevo
`PCG64(20260922)` por bloque, mismo orden de consumo (9 conductas × 16 celdas
× R + 4 candidatos, 10 000 draws siempre): las celdas no-escolaridad reciben
las mismas réplicas que en el `-0001`.

- **`ADJ16` (primario de este acto):** `ESCOLARIDAD_EXCLUIDA = ∅` → hasta 16
  celdas puntuables por conducta. Es el veredicto re-sellado con universo
  actualizado.
- **`ORO12` (oro del conducto, no veredicto):** la misma regla con la
  exclusión original de las 4 celdas de escolaridad, sobre el R de este CALC.
  Debe reproducir el veredicto del `-0001`
  (`data/corrida0/duelo-credito-prediccion-2024.json`, sha256
  `5b123e16…` al congelar). Se contrasta en la nota; no se sella contra ese
  JSON (es un derivado vivo, D-22 (4)).

Contexto oferta-antes-que-preferencia (v2.16 §3): K4B-OFERTA y K5 de la misma
celda se publican con K1/K2-*/K3 en la nota, fuera del ΔMAE, como en el
`-0001`.

## 5 · Ramas terminales probadas antes de congelar (D-22)

`tests/test_din_credito_escolaridad_2.py`, sobre zips sintéticos con la forma
de TMODULO 2024 y los insumos sellados reales: (1) mapa == `-0001`, 12
códigos; (2) `niv=01` → hasta_primaria y `niv=10` → superior, con dos dígitos
y con uno; (3) la guardia sellada para `"*"`, lista, `""`, `None`, `"k1"`,
conducta ajena; (4) `medir()` normal: `_valida_outputs == []`, 4 cubos con
N>0, N-SIN-CUBO = filas 99, sin no-finitos; `niv` de un dígito da la misma
salida; (5) masa cero (sin `03`: SECUNDARIA N=0, P=None), celda rara
(K2-AUTOMOTRIZ SUPERIOR P=0), cero puntuadas (R vacío → sin retador),
parcial (R roto del `-0001`: 13 elegibles en K1): el conducto las acepta;
(6) `ORO12` sobre el R real del `-0001` reproduce el JSON del duelo;
(7) `_oro` detecta una diferencia de 1e-9; (8) `resultados:` ==
`esquema_resultados()`. Nulos declarados con `permite_no_estimable` en todo
`-P`/`-IC-*`/ΔMAE/IC/MAE/cobertura; ningún `NaN`/`inf` en la salida.

## 6 · Lo que esta spec no hace

No edita el `-0001` ni ningún CALC sellado; no re-emite; no cambia
candidatos, criterio, universo, ponderador ni semillas; no fija umbral de
materialidad; no adopta (`adopta: NO`, `cuenta_gen2: SI` por la cabecera del
encargo). No mide K7 ni el eje `cuenta` (fuera de la lista blanca, como en el
`-0001`).
