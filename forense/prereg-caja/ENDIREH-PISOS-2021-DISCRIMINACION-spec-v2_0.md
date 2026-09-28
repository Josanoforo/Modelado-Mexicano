# ENDIREH-PISOS-2021-DISCRIMINACION · spec humana v2.0 (ADENDA-DE-SPEC, D-15)

Acto `GEN2-PISOS-Y-ADENDAS-1` (P4), 28/sep/2026. **Sucede en texto** a la spec humana sellada `data/corrida0/CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001/spec.md` (sha256 `f3921bd3fb3e301acc9105bcf4015904c7061a9fab42f619394621e36cc9a8fb`), que **no se toca**, como tampoco su `spec.yaml` (`7eadbe7b…93e3`), su `medidor.py` (`66af57e4…0514`) ni su `RESULT` sellado (`sello.json` `8f3cfe19…356e`). Esta versión no abre CALC nuevo ni cambia un número: declara por escrito lo que el código sellado ya hacía y la v1 no decía, para que la spec humana baste para recalcular sin leer el código (D-15).

**Qué faltaba (fila de `forense/validacion-independiente/specs-insuficientes-v1_0.tsv`, `D15-RECODIFICACION-AUSENTE`, NC `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-02`, 23 llaves):** la correspondencia de `NIV` a ninguno/básica/media superior/superior. Además, al escribir esta versión leyendo el código se declaran otras seis reglas que la v1 dejaba implícitas: (1) exclusión previa por edad, factor y diseño, que saca a la mujer de **todos** los ejes; (2) comparación de campos de filtro sobre el texto crudo; (3) enlace `TSDem` por `ID_PER`; (4) marco completo de UPM del bootstrap; (5) semilla por celda; (6) orden de las celdas y significado de la llave `#k`. Escrita **leyendo el código que midió** (permitido para escribir la adenda, no para validar; encargo P4).

## 1 · Origen

- Microdato: ZIP `endireh2021_bd_csv_zip`, sha256 `e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e`. Se leen dos miembros, localizados por **nombre base exacto** (debe haber exactamente uno de cada nombre en el ZIP): `TB_SEC_VIII.csv` y `TSDem.csv`. Codificación `latin-1`, CSV con encabezado, todos los campos como texto.
- Documentación: FD `endireh2021_fd_pdf` (sha256 `5c30a3f7f88123ca672f1042ec3b5c37cc1d7989f07fd23ecbf088cca6dda180`); cuestionarios A/B/C (`d2de0f03…7ae1`, `beffe06a…e689`, `793a87df…77be`). La pregunta 8.3 tiene el mismo texto en A/B/C.

## 2 · Unidad, universo y exclusiones previas

Unidad: mujer de 15 años o más (una fila de `TB_SEC_VIII.csv`). Una fila entra al **marco** si y sólo si se cumplen, en este orden:
1. `P8_2` es exactamente el texto `1` (trabajó al menos una semana por salario, pago o ganancia de octubre 2016 a la entrevista). Comparación sobre el texto crudo del campo, sin recortar espacios. `2`, blanco, `9` y cualquier otro valor quedan fuera — nunca cuentan como «sin discriminación».
2. Edad: se toma `EDAD` de `TSDem.csv` de la fila cuyo `ID_PER` es igual al `ID_PER` de la fila de `TB_SEC_VIII` (diccionario `ID_PER → (EDAD, NIV)` construido con las filas de `TSDem` con `ID_PER` no vacío; si un `ID_PER` se repitiera, vale la última fila leída). Si no hay enlace, o `EDAD` no se convierte a entero, o el entero está fuera de 15–120, la fila **sale del marco** (de todos los ejes, incluido el nacional).
3. `FAC_MUJ` se convierte a número real; si no se puede, no es finito o es ≤ 0, la fila sale del marco.
4. `EST_DIS` y `UPM_DIS` no vacíos (texto crudo); si alguno está vacío, sale del marco.

El marco resultante se reporta como `RESULT-ENDIREH2021-DIS-N-ELEGIBLES` (conteo de filas, sin ponderar).

## 3 · Desenlaces (siete; cada uno con su propio denominador)

Los códigos de los reactivos se comparan tras recortar espacios. Valor 1 = positivo, 0 = negativo, «desconocido» = fuera del denominador de esa celda.

- `prueba_ingreso` — `P8_3_1_1` «¿Le pidieron una prueba de embarazo como requisito para trabajar?»: `1`→1; `2`→0; todo lo demás desconocido.
- `prueba_continuidad` — `P8_3_1_2` «¿Le pidieron prueba de embarazo como requisito para continuar en su trabajo o renovarle el contrato?»: igual.
- `prueba_alguna` — unión de los dos: 1 si alguno es `1`; 0 si **ambos** son `2`; si no, desconocido.
- `despido_embarazo` (`P8_3_2_1`), `no_renovacion_embarazo` (`P8_3_2_2`), `reduccion_embarazo` (`P8_3_2_3`): «por embarazarse» la despidieron / no le renovaron el contrato / le bajaron el salario o prestaciones. Códigos `1` sí, `2` no, `3` no estuvo embarazada en ese periodo, `9`/blanco desconocido. Para un reactivo: `3`→desconocido (inelegible, **no** negativo); `1`→1; `2`→0; lo demás desconocido.
- `perjuicio_embarazo_alguno` — sobre los tres `P8_3_2_*`: si los tres son `3` → desconocido; si alguno es `1` → 1; si los tres son `2` → 0; cualquier otra mezcla (p. ej. `2` y `3` sin `1`, o algún `9`/blanco sin `1`) → desconocido.

Ventana de los siete: de octubre de 2016 a la entrevista (texto de la pregunta 8.2/8.3). Rótulo de ventana en la salida: `octubre_2016_a_entrevista`.

## 4 · Ejes y categorías (univariados; sin cruces)

Orden fijo de ejes y categorías:
1. `nacional`: `MX` (todas las filas del marco).
2. `edad` (de `EDAD` de `TSDem`): `15-29` (15–29), `30-44` (30–44), `45-59` (45–59), `60+` (60–120).
3. `escolaridad` (de `NIV` de `TSDem`, FD 2021, pregunta 2.7 «¿Hasta qué año o grado aprobó (NOMBRE) en la escuela?»; se convierte a entero, así `04` y `4` son el mismo código):

   | código `NIV` (texto del FD) | categoría |
   |---|---|
   | 00 Ninguno | `ninguno` |
   | 01 Preescolar · 02 Primaria · 03 Secundaria · 05 Estudios técnicos o comerciales con primaria terminada · 06 Estudios técnicos o comerciales con secundaria terminada | `basica` |
   | 04 Preparatoria o bachillerato · 07 Estudios técnicos o comerciales con preparatoria terminada · 08 Normal con primaria o secundaria terminada | `media_superior` |
   | 09 Normal licenciatura · 10 Licenciatura o profesional · 11 Posgrado (Especialidad, Maestría o Doctorado) | `superior` |
   | blanco, no convertible a entero, o cualquier otro entero | sin categoría: la mujer **no** entra a ninguna celda de escolaridad, pero sí a los demás ejes |

   `GRA` no se usa. Nota de lectura: 05/06 (técnicos con primaria o secundaria) van a básica y 07 (técnico con preparatoria) a media superior; es la agrupación del código sellado, no la de otras fuentes.
4. `localidad`: valor crudo de `DOMINIO` de `TB_SEC_VIII`, categorías `U`, `C`, `R`.
5. `pareja` (instrumento): valor crudo de `T_INSTRUM`, categorías `A1`, `A2`, `B1`, `B2`, `C1`, `C2`.
6. `entidad`: valor crudo de `CVE_ENT`, categorías `01` … `32`.

Una mujer cuyo valor de eje no está en la lista no entra a ninguna celda de ese eje.

## 5 · Estimación por celda (desenlace × eje × categoría)

Ponderador `FAC_MUJ` **sin normalizar**. Diseño: estrato `EST_DIS`, UPM `UPM_DIS`, tratados como **texto opaco** (sin convertir a número ni rellenar). Unidad de conglomerado = par (estrato, UPM).

1. **Seleccionadas**: filas del marco que están en la categoría (o todas, si el eje es `nacional`) y cuyo desenlace no es desconocido. `n` = número de seleccionadas; `upm` = número de pares (estrato, UPM) distintos entre las seleccionadas.
2. **Soporte**: si `n < 100` o `upm < 5` → celda `SUPRIMIDA`, causa `soporte`.
3. **Marco de conglomerados**: **todos** los pares (estrato, UPM) presentes en el **marco completo** (§2, no sólo en la celda), en orden de primera aparición recorriendo las filas en el orden del archivo. A cada par se le asignan dos sumas sobre las seleccionadas: `num = Σ FAC_MUJ × desenlace`, `den = Σ FAC_MUJ`; los pares sin seleccionadas llevan (0, 0) y **se quedan** en su estrato.
4. **Punto**: `p = Σnum / Σden` (sobre todos los pares).
5. **Bootstrap**: `R = 200` réplicas. Generador `numpy.random.default_rng(s)` (PCG64) con semilla por celda `s = 20260923 + Σ ord(c)` sobre los caracteres del texto `desenlace + eje + categoría` concatenados sin separador (p. ej. `prueba_ingreso` + `edad` + `15-29`). Estratos en orden de primera aparición al recorrer el marco de conglomerados del paso 3. En cada réplica, para cada estrato con `m` conglomerados, se sortean `m` índices con reemplazo con `rng.integers(0, m, m)` y se suman sus `num` y `den`; la réplica es `Σnum/Σden` (o no finita si `Σden = 0`). Un estrato con un solo conglomerado se re-sortea a sí mismo (varianza cero).
6. Si alguna réplica no es finita → `SUPRIMIDA`, causa `replicas`.
7. **IC**: percentiles 2.5 y 97.5 de las réplicas (`numpy.quantile`, interpolación lineal por defecto); `se` = desviación estándar de las réplicas con `ddof = 1`.
8. **Precisión**: si `ic95_sup − ic95_inf > 0.20`, o `p > 0` y `se/p > 0.30` → `SUPRIMIDA`, causa `precision`.
9. Si no, `PUBLICABLE` con `p`, `ic95`, `se`, `n`, `upm`, `masa_ponderada = Σden` y las réplicas agregadas.

## 6 · Salida y llaves

`RESULT-ENDIREH2021-DIS-TABLA` es una lista JSON en el orden: desenlaces en el orden de §3 (`prueba_ingreso`, `prueba_continuidad`, `prueba_alguna`, `despido_embarazo`, `no_renovacion_embarazo`, `reduccion_embarazo`, `perjuicio_embarazo_alguno`) × ejes y categorías en el orden de §4. Son 7 × 50 = 350 celdas, índices 0–349. La llave `RESULT-ENDIREH2021-DIS-TABLA#k` es la celda de índice `k` de esa lista (p. ej. `#5` = `prueba_ingreso` × `escolaridad` × `ninguno`; `#105` = `prueba_alguna` × `escolaridad` × `ninguno`). Sólo se validan llaves de celdas `PUBLICABLE`.

## 7 · Lo que esta medición no es

GEN2 descriptivo RETROSPECTIVO de una ola ya vista; unidad persona (mujer); prevalencias condicionadas al filtro 8.2 y, para los desenlaces de embarazo, a la respuesta al módulo (no estiman la proporción de todas las trabajadoras embarazadas si hay subcaptura). No se suma a violencia laboral 8.9; no se infiere causa ni transición temporal. No adopta nada: la adopción del RESULT sellado ya es de mesa y esta versión no la toca.
