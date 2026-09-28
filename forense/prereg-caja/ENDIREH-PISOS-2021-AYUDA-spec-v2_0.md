# ENDIREH-PISOS-2021-AYUDA · spec humana v2.0 (ADENDA-DE-SPEC, D-15)

Acto `GEN2-PISOS-Y-ADENDAS-1` (P4), 28/sep/2026. **Sucede en texto** a la spec humana sellada `data/corrida0/CALC-ENDIREH-PISOS-2021-AYUDA-0001/spec.md` (sha256 `791b77391cf6357adcc221f0291c26e1384b2e6d15315f82e520ecc2e5db9370`), que **no se toca**, como tampoco su `spec.yaml` (`52741639…ec89`), su `medidor.py` (`a6b4d56f…34c7`) ni su `RESULT` sellado (`sello.json` `38c2c5b3…2417`). No abre CALC nuevo ni cambia un número: corrige la identidad escrita de una celda y declara lo que el código sellado ya hacía y la v1 no decía (D-15).

**Qué faltaba (fila de `forense/validacion-independiente/specs-insuficientes-v1_0.tsv`, `D15-IDENTIDAD-CONTRADICTORIA`, NC `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-03`, 1 llave, `#115`):** la v1 describe la casilla 14 de 14.22 como «desconocía servicios»; el FD 2021 (p. 632, `P14_22_14`) y el cuestionario A (14.22) dicen **«No sabía que existían leyes para sancionar la violencia»**. El código siempre midió `P14_22_14`; lo que estaba mal era el texto. Esta versión trae además, verbatim del FD (pp. 629–632), los quince textos de 14.22, y declara las reglas implícitas (exclusiones previas, texto crudo, enlaces, marco de UPM, semilla, orden de llaves). Escrita **leyendo el código que midió** (permitido para escribir la adenda, no para validar; encargo P4).

## 1 · Origen

- Microdato: ZIP `endireh2021_bd_csv_zip`, sha256 `e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e`. Miembros por **nombre base exacto** (exactamente uno de cada uno): `TB_SEC_XIV.csv`, `TB_SEC_XIV_2.csv`, `TSDem.csv`. `latin-1`, CSV con encabezado, campos como texto.
- FD `endireh2021_fd_pdf` (sha256 `5c30a3f7f88123ca672f1042ec3b5c37cc1d7989f07fd23ecbf088cca6dda180`); cuestionario A `endireh2021_cuestionario_a_pdf` (sha256 `d2de0f03b8d347b298f7355312953d772a94edf21443bded042dd2a2ec487ae1`).

## 2 · Unidad, universo y exclusiones previas

Unidad: mujer de 15+ con cuestionario A (pareja actual). Una fila de `TB_SEC_XIV.csv` entra al **marco** si y sólo si, en este orden:
1. `T_INSTRUM` (texto crudo) es `A1` o `A2`.
2. `EDAD` de la fila de `TSDem.csv` con el mismo `ID_PER` (diccionario sobre filas con `ID_PER` no vacío; si se repitiera, vale la última) es entero en 15–120; si no hay enlace o no cumple, la fila **sale del marco** (todos los ejes).
3. `FAC_MUJ` real, finito y > 0.
4. `EST_DIS` y `UPM_DIS` no vacíos (texto crudo).

`RESULT-ENDIREH2021-AYU-N-ELEGIBLES` = filas del marco (sin ponderar).

## 3 · Desenlaces

Códigos comparados tras recortar espacios.

**Violencia de pareja (filtro de ayuda/denuncia)**: los 38 actos de 14.1 (`P14_1_1`…`P14_1_22`, `P14_1_23AB`, `P14_1_24AB`, `P14_1_25`…`P14_1_34`, `P14_1_35AB`…`P14_1_38AB`; desde el inicio de la relación actual). Clasificador: 1 si algún valor es `1`, `2` o `3`; 0 si **todos** son `4`; si no, desconocido.

- `ayuda` = `P14_7_1` («¿Pidió apoyo, información o servicios en alguna dependencia pública o de gobierno, a un grupo o asociación o una institución privada?»), sólo si violencia = 1: `1`→1, `2`→0, lo demás desconocido. Si violencia ≠ 1, desconocido.
- `denuncia` = `P14_7_2` (ella o alguien de su familia presentó queja o denunció ante alguna autoridad), misma regla.
- `institucion_01…10` = `P14_8_1…10` sólo si `ayuda = 1` (`1`→1, `2`→0, resto desconocido): 01 Instituto de las Mujeres · 02 alguna línea de atención telefónica · 03 algún organismo o asociación civil · 04 CAVI (Centro de Atención a la Violencia Intrafamiliar) o equivalente · 05 Centro de Justicia para las Mujeres · 06 Defensoría Pública · 07 clínica, centro de salud u hospital público (ISSSTE, IMSS, Servicios de salud del estado) · 08 consultorio médico, clínica u hospital privado · 09 DIF · 10 Otra institución. Prevalencias **entre solicitantes de ayuda**; pueden sumar más de 100%.
- `razon_01…15` = `P14_22_1…15` de `TB_SEC_XIV_2.csv` enlazado por `ID_PER` (sin enlace → desconocido), sólo si `ayuda = 0` **y** `denuncia = 0`: `1`→1 (sí), `0`→0 («no se declaró como respuesta afirmativa»), `9`/blanco/otro → desconocido. Textos verbatim del FD (cuestionario A, 14.22 «¿Por qué razón no lo comentó o no buscó ayuda o denunció el hecho?»):
  01 Por miedo de las consecuencias · 02 Por vergüenza · 03 Porque su esposo o pareja la amenazó · 04 Pensó que no le iban a creer · 05 Por sus hijos(as) · 06 Porque no quería que su familia se enterara · 07 Porque la convencieron de no hacerlo · 08 Porque se trató de algo sin importancia que no le afectó · 09 Porque su esposo o pareja dijo que iba a cambiar · 10 Porque su esposo tiene derecho a reprenderla · 11 Porque él no va a cambiar · 12 No sabía cómo y dónde denunciar · 13 No confía en las autoridades · **14 No sabía que existían leyes para sancionar la violencia** · 15 Otro.
  Motivos no exclusivos; cada uno con su propio denominador de respuestas conocidas.

## 4 · Ejes y categorías

`ayuda` y `denuncia`: ejes univariados en este orden — `nacional` (`MX`); `edad` (`15-29`, `30-44`, `45-59`, `60+` = 60–120); `escolaridad` (de `NIV` de `TSDem`, FD 2021, pregunta 2.7 «¿Hasta qué año o grado aprobó (NOMBRE) en la escuela?», convertido a entero: 00 Ninguno → `ninguno`; 01 Preescolar, 02 Primaria, 03 Secundaria, 05 Estudios técnicos o comerciales con primaria terminada, 06 Estudios técnicos o comerciales con secundaria terminada → `basica`; 04 Preparatoria o bachillerato, 07 Estudios técnicos o comerciales con preparatoria terminada, 08 Normal con primaria o secundaria terminada → `media_superior`; 09 Normal licenciatura, 10 Licenciatura o profesional, 11 Posgrado (Especialidad, Maestría o Doctorado) → `superior`; otro/blanco → fuera de las celdas de escolaridad; `GRA` no se usa); `localidad` (`DOMINIO` crudo: `U`, `C`, `R`); `pareja` (`T_INSTRUM` crudo: `A1`, `A2`); `entidad` (`CVE_ENT` crudo: `01`…`32`). `institucion_*` y `razon_*`: sólo `nacional`.

## 5 · Estimación por celda

Ponderador `FAC_MUJ` sin normalizar; estrato `EST_DIS` y UPM `UPM_DIS` como texto opaco; conglomerado = par (estrato, UPM).

1. Seleccionadas = filas del marco en la categoría (todas si `nacional`) con desenlace no desconocido; `n`, `upm` (pares distintos entre ellas).
2. `n < 100` o `upm < 5` → `SUPRIMIDA` (`soporte`).
3. Marco de conglomerados = **todos** los pares del marco completo de §2, en orden de primera aparición en el archivo; `num = Σ FAC_MUJ × desenlace`, `den = Σ FAC_MUJ` sobre las seleccionadas; los demás pares (0, 0) se quedan.
4. `p = Σnum / Σden`.
5. Bootstrap `R = 500`; `numpy.random.default_rng(s)` (PCG64), `s = 20260923 + Σ ord(c)` sobre `desenlace + eje + categoría` (para `institucion_*`/`razon_*`, sólo el nombre del desenlace, p. ej. `razon_14`). Estratos en orden de primera aparición en el marco de conglomerados; por réplica y estrato con `m` conglomerados, `rng.integers(0, m, m)`; réplica = `Σnum/Σden`.
6. Réplica no finita → `SUPRIMIDA` (`replicas`).
7. IC percentil 2.5/97.5 (`numpy.quantile`, lineal); `se` con `ddof = 1`.
8. Ancho > 0.20 o (`p > 0` y `se/p > 0.30`) → `SUPRIMIDA` (`precision`); si no, `PUBLICABLE`.

## 6 · Salida y llaves

`RESULT-ENDIREH2021-AYU-TABLA`, lista JSON: `ayuda` × 46 celdas (1 + 4 + 4 + 3 + 2 + 32) índices 0–45; `denuncia` × 46: 46–91; `institucion_01…10`: 92–101; `razon_01…15`: 102–116. Llave `…-TABLA#k` = celda de índice `k`; **`#115` = `razon_14` × nacional = «No sabía que existían leyes para sancionar la violencia»**.

## 7 · Lo que esta medición no es

GEN2 descriptivo RETROSPECTIVO; unidad persona (mujer con pareja actual). Mide respuestas declaradas bajo el filtro; no estima subregistro total ni preferencias libres; ninguna razón demuestra elección sin restricciones (miedo y barreras de información o institucionales se mantienen separados de «sin importancia»). No adopta nada.
