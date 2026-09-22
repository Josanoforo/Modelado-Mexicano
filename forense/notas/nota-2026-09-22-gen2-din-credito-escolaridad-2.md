# Nota de cierre · ACTO GEN2-DIN-CREDITO-ESCOLARIDAD-2

22/sep/2026, CAJA (`sin_variable`, red 200, corpus montado, 436 archivos
examinados). Encargo: `forense/encargos/2026-09-22-GEN2-DIN-CREDITO-ESCOLARIDAD-2.md`
(sha256 de cuerpo `a44e3c09…3623d`). Firma de mesa del lanzamiento, archivada
y sellada: `…-ESCOLARIDAD-2-ADENDA-1.md` — `FP-260922-GEN2-DIN-CREDITO-PREDICCION-2024-COMMIT-2-3-95ec-01`
opción (a). Rama `acto/gen2-din-credito-escolaridad-2`; 0-bis `0af9d70d`,
COMMIT-1 `64542c24`, COMMIT-2 `1d9322a1`. ADR de raíz
`ADR-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-01`.

**CONTADOR:** una corrida sellada (`CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002--04564bb97815`),
`cuenta_gen2 = SI` por etiqueta de la spec (cabecera del encargo), **no adopta**.
**Sellada en disco, no registrada en la vista publicada** (E.7): ver §5.
`corrida0 status` (proyección por comando) `N_corridas_selladas = 155`.
`celdas_validadas` = 92, sin cambio: esta métrica se deriva del marcador por
segmento y de las celdas-D (`tools/tablero_programa.py::_celdas_validadas`),
y este linaje de crédito no pasa por ninguno de los dos.

## 0 · Premisas del encargo, verificadas

- `[LEÍDO]` §3 (`medidor.py:79-80`, `:154`): **confirmada**. El comentario del
  mapa `niv` está en `:79-83`, el diccionario de dos dígitos en `:84-89` y el
  `code = {c: m._code(d[c]) …}` que incluye `niv` en `:153` (una línea antes de
  la citada). Medido en el `resultados.json` sellado del `-0001`: en K1, los cubos
  HASTA-PRIMARIA, SECUNDARIA y MEDIA-SUPERIOR tienen `N=0` y SUPERIOR tiene `N=283`.
- `[EXISTE]` §3 — ¿afecta a las emisiones? **No.** `-EMISIONES-0001` sólo opera
  sobre los RESULT de los pisos 2012/2015/2018/2021-recorte1870, y en ellos la
  escolaridad cuadra con el nacional (K1: 6 109/6 113, 6 039/6 039,
  12 439/12 446, 12 406/12 406). No se re-emite; la rama prevista no se toma.
- `[SUPUESTO]` §3 — reserva consumida: **se sostiene.** El `-0002` lee las mismas
  columnas (incluida `niv`) de las mismas 9 conductas que la corrida sellada
  del `-0001`. Ningún CALC con predicción sellada y sin adjudicar depende de
  estas celdas (spec §2).
- §4 — ya hecho: **confirmado vacío.** `ls -d …PREDICCION-2024*` → 2 CALC;
  `ESCOLARIDAD-0002` aparece 0 veces en `corridas.tsv` y 0 en `no-corrido.tsv`;
  sin rama, worktree ni PR previos.
- §6 — pregunta a mesa sobre un código sin cubo evidente: **no hizo falta.**
  El único código sin par textual en 2021 es `09` «Especialidad», y sus dos
  homólogos posibles caen en `superior` (spec §1).

## 1 · La corrección y lo heredado

El mapa por texto (`catalogos/niv.csv` 2024 contra `catalogos/p3_1_1.csv` 2021)
sale **idéntico** al `NIV_A_ESCOLARIDAD` del `-0001`. El defecto era sólo pasar
`niv` por `_code()`. El `-0002` lee `niv` con sus dos dígitos y ejecuta **por bytes**
(con sha256) el medidor sellado del `-0001` (guardia incluida), el marco de
`-EJES-0003`, el adjudicador `tools/duelo/credito_prediccion_2024.py` y
`cruces_familia.py`. Sólo reemplaza `PREFIJO` y envuelve `abre_conducta_2024`.
El test del `-0001` sólo exigía que las categorías vistas fueran un
subconjunto de la rejilla (`tests/test_din_credito_prediccion_2024_adjudicacion.py`,
`_falsa_extraccion`), y un cubo vacío cumple eso. El test nuevo
(`tests/test_din_credito_escolaridad_2.py`, 8 falsadores) exige los 4 cubos.
El mutante sin la corrección cae con los 3 cubos vacíos.

## 2 · Resultado (COMMIT-2)

`corrida0 run` → SELLADO. `corrida0 verify` → **REPRODUCE · IDENTICO**
(1346/1346 RESULT). Replay en proceso aislado (`tools/verifica_aislada.py`):
REPRODUCE/IDENTICO, asentado en `forense/replay-evidencia.tsv`.

**Oro (E.5):** `REPRODUCE-ORO`: 666/666 RESULT no-escolaridad del `-0001`,
`MAX-ABS-DIFF = 0.0`. **ORO12** (la regla sellada con la exclusión original,
sobre el R de este CALC) reproduce `duelo-credito-prediccion-2024.json` en
9/9 conductas: mismo retador, veredicto, ΔMAE e IC, bit a bit.

**Eje escolaridad, ENIF 2024, adultos 18-70, unidad persona** (P, IC95, n):

| conducta | hasta primaria | secundaria | media superior | superior |
|---|---|---|---|---|
| K1 tenencia de crédito formal | 0.194 [0.173, 0.217] n=2 501 | 0.299 [0.278, 0.320] n=3 506 | 0.383 [0.360, 0.408] n=3 279 | 0.603 [0.579, 0.626] n=3 090 |
| K2 departamental | 0.119 | 0.179 | 0.242 | 0.354 |
| K2 nómina | 0.003 | 0.027 | 0.032 | 0.063 |
| K2 automotriz | 0.000 (celda rara) | 0.006 | 0.015 | 0.051 |
| K3 informal (algún tipo) | 0.269 | 0.315 | 0.308 | 0.255 |
| K5 rechazo de solicitud | 0.097 | 0.181 | 0.208 | 0.242 |
| K4B autoexclusión por oferta (entre quien nunca tuvo) | 0.232 | 0.246 | 0.223 | 0.194 |
| K6 atraso entre tenedores | 0.230 | 0.269 | 0.229 | 0.192 |

K1 «superior» pasa de 0.762 (n=283, sólo maestría/doctorado, el `-0001`) a
**0.603** (n=3 090). N de los 4 cubos + 3 sin cubo = 12 379 = nacional.

**Veredicto ADJ16** (16 celdas, regla sellada del `-0001`; ΔMAE > 0 = la
tendencia tuvo menor error que persistencia):

| conducta | retador | veredicto | ΔMAE pp | IC95 | ORO12 (= `-0001`) |
|---|---|---|---|---|---|
| K1 | TENDENCIA-SERIE | PROPUESTA-CON-RESERVA | +1.75 | [+0.68, +2.41] | +1.90, mismo veredicto |
| K2-DEPARTAMENTAL | TENDENCIA-2 | NADIE-VENCE | +0.26 | [−1.14, +0.94] | +0.30 |
| K2-NOMINA | **TENDENCIA-SERIE** (antes T-3) | NADIE-VENCE | −0.15 | [−0.38, +0.12] | −0.12 |
| K2-AUTOMOTRIZ | TENDENCIA-3 | NADIE-VENCE | −0.06 (15 celdas) | [−0.45, +0.08] | +0.00 |
| K3 | TENDENCIA-3 | NADIE-VENCE | +0.56 | [−0.84, +0.97] | +0.43 |
| K4A / K4B | — | NO-CONSTRUIBLE-SIN-RETADOR-HABILITADO | — | — | igual |
| K5 | TENDENCIA-SERIE | NADIE-VENCE | +0.69 | [−0.45, +1.17] | +0.75 |
| K6-P-TENEDORES | TENDENCIA-SERIE | PROPUESTA-CON-RESERVA | +2.54 | [+0.48, +3.22] | +2.62, mismo veredicto |

**Ningún veredicto cambia al entrar las 4 celdas de escolaridad.** El único
cambio de fondo es el retador primario de K2-NOMINA, y la conducta sigue en
`NADIE-VENCE`. `VENCE-RETADOR` sigue inalcanzable por diseño (`umbral_vence_pp = inf`,
heredado). Todas las cifras son **PROSPECTIVAS**: las emisiones se sellaron antes
de abrir 2024.

## 3 · Lo que esto NO significa

La pendiente por escolaridad de K1 (0.19 → 0.60) es tenencia, no preferencia.
El rechazo (K5) también sube con la escolaridad (0.10 → 0.24), porque solicitar
es más frecuente arriba. La autoexclusión por oferta (K4B) es parecida en los
cuatro cubos (0.19–0.25). La escolaridad aquí también mide ingreso, empleo
formal y la oferta bancaria de la localidad; no es un rasgo psicológico. No se
promedia con ninguna cifra de unidad hogar ni trámite. Las 16 celdas de una
conducta comparten la muestra de 2024 y no son independientes.

## 4 · Enmienda fechada del `-0001` (22/sep/2026, no edita el archivo sellado)

`CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001`: su **eje escolaridad (4
celdas × 9 conductas) queda VENCIDO-EN-ALCANCE → `CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002`**
(A.10). Sus 12 celdas restantes y su veredicto sobre 12 celdas siguen
vigentes, y el `-0002` los reproduce exacto. El `-0001` sigue `SELLADA`; no
se declara `repite_de`. Asentado también en la fila FP (`ejecutada_en`).
Esta línea de crédito no tiene celda-D: la enmienda vive aquí y en la FP.
`NC-260922-…-95ec-01` → CERRADA.

## 5 · Hallazgo: la vista publicada no puede recibir esta fila

`registro --verifica --escribe --lote CALC-…-ESCOLARIDAD-0002` corre en el
árbol (exit 0) y produce la fila propia (1 corrida, 1 346 RESULT). También
arrastra **21 CALC ajenos ya sellados en `main` que no tienen fila**, entre
ellos el propio `-0001` y `-EMISIONES-0001`: 20 449 RESULT ajenos, 0
transiciones de replay, `usos.tsv` idéntico. Las tres vistas **se
revirtieron al byte de `origin/main`** porque la firma de mesa P4 (§2(2),
`GEN2-TUBERIA-EFICIENCIA-1`: «los archivos derivados no viajan en los PR»)
la hace cumplir la guarda de `enrutamiento-pr` (`tools/derivados_protegidos.py --toca`),
y porque el job de push a main **no** re-deriva `corridas/resultados/usos`
(`verify.yml:369-372`: exigen `--lote`). Resultado: desde `344739d1`
(21/sep) ninguna corrida sellada entra a la vista. E.7 y P4 chocan. Va a mesa
como `FP-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-01`. El criterio de
«hecho» `grep -c ESCOLARIDAD-0002 data/corrida0/corridas.tsv → 1` **no se
cumple en este PR** (NC `-0af9-01`).

## NO-CORRIDO / RESERVAS

Ver el encargo archivado (`## NO-CORRIDO / RESERVAS`) y
`NC-260922-GEN2-DIN-CREDITO-ESCOLARIDAD-2-0af9-01`.

## 6 · Suite

`tests/check.py --rapido`: 0 FAIL · 298 WARN (+1 WARN = FP/NC propias abiertas,
D-16). `tools/ci_guardias.py --ejecuta-huerfanos`: el test propio sale `SKIP
dependencia-pendiente NECESITA-DEPENDENCIA(numpy)`, igual que su hermano;
1 fallido **ajeno y de entorno**: `tests/test_marco_m_en_seco.py` (#999) hace
`cp -al` del repo a `$TMPDIR`, y en esta caja `/tmp` y `/home` son
filesystems distintos (`Invalid cross-device link`). No lo toca este acto.
