# Ambigüedades · recalculo DISCRIMINACION

**Verificación del ZIP.** `sha256sum bd_endireh_2021_csv.zip` =
`e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e`, idéntico
al declarado por la spec (§1) y por el encargo. Verificado antes de leer el
microdato.

Recalculado desde `forense/prereg-caja/ENDIREH-PISOS-2021-DISCRIMINACION-spec-v2_0.md`
únicamente (más FD/cuestionarios y el ZIP de microdato). No se leyó `data/corrida0/CALC-ENDIREH-*`
ni ningún otro artefacto fuera del perímetro permitido.

## N del marco

`RESULT-ENDIREH2021-DIS-N-ELEGIBLES` obtenido por spec: **67086** filas de
`TB_SEC_VIII.csv` (sobre 110127 filas totales del archivo), tras aplicar en
orden: `P8_2 == "1"` (texto crudo) → enlace a `TSDem.csv` con `EDAD` entero en
[15,120] → `FAC_MUJ` real/finito/>0 → `EST_DIS`/`UPM_DIS` no vacíos. Marco de
conglomerados resultante: 17214 pares (estrato, UPM) distintos, agrupados en
617 estratos distintos (`EST_DIS`).

## Puntos donde la spec admitía más de una lectura literal

1. **`prueba_alguna` — "si alguno es 1" / "si ambos son 2".** La spec define
   `prueba_alguna` justo después de `prueba_ingreso`/`prueba_continuidad`
   como "unión de los dos", y dice "1 si alguno es 1; 0 si ambos son 2". Esto
   se puede leer sobre el **valor ya clasificado** de esos dos desenlaces
   (1/0/desconocido) o sobre el **código crudo** (`P8_3_1_1`/`P8_3_1_2`
   recortado). Elegí la primera lectura (sobre el valor clasificado), por ser
   la lectura natural inmediatamente después de definir esos dos desenlaces
   y porque la spec dice explícitamente "unión de los dos [desenlaces]", no
   "unión de los dos campos". En este caso ambas lecturas son equivalentes
   en el resultado: el valor clasificado es 1 syss el código crudo recortado
   es `'1'`, y es 0 syss el código crudo recortado es `'2'` (la función
   `_simple_10` no introduce ninguna otra vía a 1 o 0), así que la elección
   no cambia ninguna celda calculada.
2. **Vacío en `EST_DIS`/`UPM_DIS`/`ID_PER`.** La spec dice "no vacíos (texto
   crudo)" sin decir si un valor de solo espacios cuenta como vacío. Decidí
   que "vacío" es únicamente la cadena `''` (comparación literal), ya que la
   spec insiste en "texto crudo" para estos campos en varias partes y no
   pide recortar espacios aquí (a diferencia de `P8_2`, donde sí lo dice
   explícitamente que NO se recorta, y de los reactivos de desenlace en §3,
   donde sí se recorta). No se observó ninguna fila con `EST_DIS`/`UPM_DIS`
   de solo espacios en el marco resultante, así que la elección no tuvo
   efecto práctico verificable aquí.
3. **Conversión de `EDAD` a entero.** La spec dice "si … `EDAD` no se
   convierte a entero …" sin especificar la función exacta. Usé `int(texto)`
   de Python, que tolera espacios circundantes y ceros a la izquierda
   (`"06"` → 6) pero no decimales ni texto no numérico. No encontré edades
   con formato distinto a dígitos ASCII simples en una inspección de la
   columna.
4. **Orden de las cuatro exclusiones previas (§2).** Implementado en el
   orden literal 1→2→3→4 que da la spec. Las cuatro condiciones son
   independientes entre sí (ninguna depende del resultado de otra), así que
   el orden no cambia el conjunto final del marco; se siguió el orden dado
   por fidelidad al texto, no por necesidad lógica.
5. **Orden de los sorteos del bootstrap (§5.5): "en cada réplica, para cada
   estrato…".** Implementado literalmente como bucle externo por réplica
   (r = 0…199) y bucle interno por estrato (en el orden de primera aparición
   del marco de conglomerados), con una llamada a `rng.integers(0, m, m)`
   por estrato por réplica. No hizo falta reordenar por rendimiento: las 23
   celdas requeridas (200 réplicas × 617 estratos cada una) corrieron en
   ~12 s en total.
6. **Salida numérica cuando `SUPRIMIDA`.** Ninguna de las 23 celdas
   requeridas salió `SUPRIMIDA` (las 23 son `PUBLICABLE`), así que este caso
   no se ejerció. Por instrucción del harness ("vacío si SUPRIMIDA") el
   código deja `punto`/`ic95_inf`/`ic95_sup`/`se` vacíos para cualquier causa
   de supresión (`soporte`, `replicas` o `precision`), sin intentar reportar
   un punto determinista cuando la supresión ocurre después del paso 4.

## Verificación de identidad índice → llave

Se construyó un enumerador general de las 350 celdas (7 desenlaces × 50 ejes/
categorías, en el orden de §3/§4) y se verificó, para cada una de las 23
llaves requeridas por el protocolo, que `(desenlace, eje, categoría)`
coincide exactamente con lo que `protocolo-recalculo-v1_0.md` §1 declara:
`#5..#8` = `prueba_ingreso`×escolaridad×{ninguno,basica,media_superior,
superior}; `#56..#58` = `prueba_continuidad`×escolaridad×{basica,
media_superior,superior}; `#105..#108` = `prueba_alguna`×escolaridad×{las
cuatro}; `#156..#158`/`#206..#208`/`#256..#258`/`#306..#308` = igual patrón
para `despido_embarazo`/`no_renovacion_embarazo`/`reduccion_embarazo`/
`perjuicio_embarazo_alguno`. **Ninguna discrepancia.**

## Consulta a FD / cuestionarios

No hizo falta abrir `endireh2021_fd.pdf` ni los cuestionarios: la spec ya
trae verbatim (§4) la tabla completa `NIV → escolaridad` y los textos de los
reactivos de §3, y los nombres de columna exactos (`P8_2`, `P8_3_1_1`, …,
`EST_DIS`, `UPM_DIS`, `FAC_MUJ`, `DOMINIO`, `T_INSTRUM`, `CVE_ENT`) se
confirmaron contra el encabezado real de `TB_SEC_VIII.csv`/`TSDem.csv` dentro
del ZIP de microdato (permitido: es el insumo, no "otro lado"). Todas esas
columnas existen tal cual en el CSV.

Ninguna otra ambigüedad.
