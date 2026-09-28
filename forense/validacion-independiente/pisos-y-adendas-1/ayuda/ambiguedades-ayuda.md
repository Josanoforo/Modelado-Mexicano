# Ambigüedades · recalculo AYUDA

**Verificación del ZIP.** `sha256sum bd_endireh_2021_csv.zip` =
`e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e`, idéntico
al declarado por la spec (§1) y por el encargo. Verificado antes de leer el
microdato.

Recalculado desde `forense/prereg-caja/ENDIREH-PISOS-2021-AYUDA-spec-v2_0.md`
únicamente. No se leyó `data/corrida0/CALC-ENDIREH-*` ni ningún otro artefacto
fuera del perímetro permitido.

## N del marco

`RESULT-ENDIREH2021-AYU-N-ELEGIBLES` obtenido por spec: **68540** filas de
`TB_SEC_XIV.csv` (sobre 110127 filas totales), tras aplicar en orden:
`T_INSTRUM` (texto crudo) ∈ {A1,A2} → enlace a `TSDem.csv` con `EDAD` entero
en [15,120] → `FAC_MUJ` real/finito/>0 → `EST_DIS`/`UPM_DIS` no vacíos.
Marco de conglomerados: 16846 pares (estrato, UPM), 617 estratos.

## Alcance de este recálculo

El protocolo (§1) solo pide `#115` (`razon_14`×nacional). Como `razon_14`
solo tiene celda nacional y depende exclusivamente de: (a) `violencia`
(clasificador sobre los 38 actos de 14.1), (b) `ayuda`/`denuncia`
(`P14_7_1`/`P14_7_2`, solo si `violencia=1`) y (c), si `ayuda=0` y
`denuncia=0`, de `P14_22_14` de `TB_SEC_XIV_2.csv` enlazado por `ID_PER`, el
código no calcula `ayuda`/`denuncia` sobre los demás ejes (edad, localidad,
etc.) ni `institucion_01..10`/`razon_01..02, 03..13, 15` — no hacen falta
para la única llave pedida. Sí construye el enumerador de índices completo
(117 slots) para verificar la identidad de la llave requerida.

## Puntos donde la spec admitía más de una lectura literal

1. **Corrección de identidad de `#115` (motivo de esta adenda).** La v1
   describía la casilla 14 de 14.22 como "desconocía servicios"; el FD/
   cuestionario dicen "No sabía que existían leyes para sancionar la
   violencia". Esta adenda v2.0 ya trae el texto correcto verbatim en §3 y
   §6 ("`#115` = `razon_14` × nacional = «No sabía que existían leyes para
   sancionar la violencia»"), así que no hubo ambigüedad que resolver aquí:
   el código mide `P14_22_14` tal cual la spec indica, sin depender de la
   etiqueta textual.
2. **Enlace a `TB_SEC_XIV_2.csv` por `ID_PER` con posible repetición.** La
   spec dice "enlazado por `ID_PER` (si el `ID_PER` falta en ese archivo,
   desconocido)" sin aclarar qué pasa si `ID_PER` se repitiera en
   `TB_SEC_XIV_2.csv` (a diferencia del enlace a `TSDem`, donde sí se
   explicita "vale la última fila leída"). Por consistencia con esa regla
   general (declarada como implícita también para este acto: "enlace
   `TSDem` por `ID_PER`" y, por extensión razonable, cualquier enlace por
   `ID_PER`), usé el mismo criterio ("última fila leída gana"). Verifiqué
   directamente sobre el ZIP que `ID_PER` es único en `TB_SEC_XIV_2.csv`
   (110127 valores no vacíos, todos distintos), así que esta regla no tuvo
   ningún caso real que ejercer.
3. **`EST_DIS`/`UPM_DIS`/`T_INSTRUM` vacío o crudo.** Mismo criterio literal
   que en las otras dos specs: comparación exacta contra `''` para "vacío",
   sin recortar espacios en los campos de filtro (`T_INSTRUM`).
4. **Semilla de `razon_14`.** La spec (§5.5) dice que para
   `institucion_*`/`razon_*` (que "solo tienen celda nacional") la semilla
   usa "solo el nombre del desenlace", con el ejemplo explícito
   `razon_14`. Se aplicó literalmente: `texto_semilla = 'razon_14'` (NO
   `'razon_14' + 'nacional' + 'MX'`).
5. **`n_fijos` / orden de columnas al leer `TB_SEC_XIV.csv`.** El código lee
   las columnas por nombre exacto de encabezado (no por posición fija en el
   archivo), así que el orden real de columnas en el CSV no afecta el
   resultado; se verificó contra el encabezado real del ZIP que las 7
   columnas fijas (`ID_PER`,`T_INSTRUM`,`FAC_MUJ`,`EST_DIS`,`UPM_DIS`,
   `P14_7_1`,`P14_7_2`) y las 38 columnas `P14_1_*` (con sufijo `AB` en
   `{23,24,35,36,37,38}`) existen todas.
6. **Salida numérica cuando `SUPRIMIDA`.** No se ejerció: la única celda
   requerida salió `PUBLICABLE`.

## Verificación de identidad índice → llave

Enumerador general de los 117 slots (`ayuda`×46, `denuncia`×46,
`institucion_01..10`, `razon_01..15`, en el orden de §6). Para la llave
requerida: `#115` = `razon_14`×nacional×`MX`. **Coincide exactamente** con lo
que declara `protocolo-recalculo-v1_0.md` §1 ("`#115` (`razon_14` ×
nacional)"). Ninguna discrepancia.

## Consulta a FD / cuestionarios

No hizo falta abrir el FD ni el cuestionario A más allá de lo ya citado
verbatim en la spec (los quince textos de 14.22, incluida la casilla 14, ya
están en §3). Los nombres de columna (`T_INSTRUM`, `P14_1_*`, `P14_7_1`,
`P14_7_2`, `P14_22_14`, `EST_DIS`, `UPM_DIS`, `FAC_MUJ`) se confirmaron contra
el encabezado real de `TB_SEC_XIV.csv`/`TB_SEC_XIV_2.csv`/`TSDem.csv` dentro
del ZIP.

Ninguna otra ambigüedad.
