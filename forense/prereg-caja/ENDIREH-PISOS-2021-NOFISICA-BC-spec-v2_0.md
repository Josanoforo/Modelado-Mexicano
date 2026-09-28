# ENDIREH-PISOS-2021-NOFISICA-BC · spec humana v2.0 (ADENDA-DE-SPEC, D-15)

Acto `GEN2-PISOS-Y-ADENDAS-1` (P4), 28/sep/2026. **Sucede en texto** a la spec humana sellada `data/corrida0/CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001/spec.md` (sha256 `ae27d5d972002908ff72eb028e50eda8cde5cdb565ae8475a3a5483fdf5c7f0f`), que **no se toca**, como tampoco su `spec.yaml` (`9a619dd7…c6f9a`), su `medidor.py` (`1fc4766d…a1d3`) ni su `RESULT` sellado (`sello.json` `5e226851…a7e`). No abre CALC nuevo ni cambia un número: declara lo que el código sellado ya hacía y la v1 no decía, para que la spec humana baste para recalcular sin leer el código (D-15).

**Qué faltaba (fila de `forense/validacion-independiente/specs-insuficientes-v1_0.tsv`, `D15-RECODIFICACION-AUSENTE`, NC `NC-260927-GEN2-RECIBO-ASTRA6-1-beee-02`, 8 llaves):** la correspondencia de `NIV` a ninguno/básica/media superior/superior. La otra fila de esta spec (`PAQUETE-SIN-IDENTIDAD-DE-VENTANA`, 471 llaves) es defecto del paquete ciego, no de la spec, y **no** es objeto de esta adenda (propuesta `NADA`); aun así §3 y §6 declaran la ventana de cada celda y el orden de las llaves. Al escribir esta versión leyendo el código se declaran también: exclusión previa por edad, factor y diseño; texto crudo en los campos de filtro; enlaces por `ID_PER`; marco completo de UPM; semilla por celda; orden de celdas. Escrita **leyendo el código que midió** (permitido para escribir la adenda, no para validar; encargo P4).

## 1 · Origen

- Microdato: ZIP `endireh2021_bd_csv_zip`, sha256 `e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e`. Miembros localizados por **nombre base exacto** (exactamente uno de cada uno): `TB_SEC_XIV.csv`, `TB_SEC_XIV_2.csv`, `TSDem.csv`. Codificación `latin-1`, CSV con encabezado, campos como texto.
- Documentación: FD `endireh2021_fd_pdf` (sha256 `5c30a3f7f88123ca672f1042ec3b5c37cc1d7989f07fd23ecbf088cca6dda180`); cuestionarios A/B/C (`d2de0f03…7ae1`, `beffe06a…e689`, `793a87df…77be`).

## 2 · Unidad, universo y exclusiones previas

Unidad: mujer de 15+ (una fila de `TB_SEC_XIV.csv`). Una fila entra al **marco** si y sólo si, en este orden:
1. `T_INSTRUM` (texto crudo, sin recortar) es `A1`, `A2`, `B1`, `B2` o `C1` (pareja actual A; exesposo/expareja B; novio/pareja actual o última C1). `C2` (sin relación) y cualquier otro valor quedan fuera por diseño.
2. Edad: `EDAD` de la fila de `TSDem.csv` con el mismo `ID_PER` (diccionario `ID_PER → (EDAD, NIV)` sobre filas de `TSDem` con `ID_PER` no vacío; si se repitiera, vale la última leída). Sin enlace, no entero, o fuera de 15–120 → la fila **sale del marco** (de todos los ejes y desenlaces).
3. `FAC_MUJ` real, finito y > 0; si no, sale.
4. `EST_DIS` y `UPM_DIS` no vacíos (texto crudo); si no, sale.

`RESULT-ENDIREH2021-NF-BC-N-ELEGIBLES` = número de filas del marco (sin ponderar).

## 3 · Desenlaces

Códigos de reactivos comparados tras recortar espacios. **Clasificador de actos** sobre una lista de valores: 1 si alguno es `1`, `2` o `3` (ocurrió muchas veces / pocas veces / una vez); 0 si la lista no está vacía y **todos** son `4` (no ocurrió); si no, desconocido (`9`, blanco o salto sin positivo).

**Actos de 14.1** (`P14_1_<i>`, desde el inicio de la relación; en B incluye después de la separación): `i = 1…38`; los seis actos `23, 24, 35, 36, 37, 38` usan el sufijo `AB` (`P14_1_23AB`, …) y **C1 no los pregunta**: para C1 se omiten de toda lista. Grupos:
- `emocional_control`: 10–24 · `sexual`: 25–29 · `digital`: 30–31 · `economica_patrimonial`: 32–38 · `no_fisica_alguna`: 10–38.

Para cada grupo, dos ventanas (dos desenlaces con denominador propio):
- `<grupo>__vida_relacion` = clasificador sobre los `P14_1_*` del grupo (según instrumento).
- `<grupo>__desde_octubre_2020` = sólo si el de vida no es desconocido: clasificador sobre la lista que, para cada acto del grupo, toma `4` si el `P14_1_*` recortado es `4` y, si no, el valor de `P14_3_<mismo sufijo>` (14.3, octubre 2020 a la entrevista, mismos códigos 1–4). Si el de vida es desconocido, éste también.

**Ayuda y denuncia B/C** (sólo `B1`, `B2`, `C1`; para `A1`/`A2` son desconocidos): violencia = clasificador sobre **todos** los actos 1–38 de 14.1 (físicos 1–9 incluidos; para C1 sin los seis `AB`). Si violencia = 1:
- `ayuda_bc` = `P14_7_1` («¿Pidió apoyo, información o servicios en alguna dependencia pública o de gobierno, a un grupo o asociación o una institución privada?»): `1`→1, `2`→0, lo demás desconocido.
- `denuncia_bc` = `P14_7_2` (ella o alguien de su familia presentó queja o denunció ante una autoridad): igual.
Si violencia ≠ 1, ambos desconocidos. Ventana en la salida: `desde_inicio_relacion`.
- `institucion_bc_01…10` = `P14_8_1…10` (1→1, 2→0, resto desconocido) sólo si `ayuda_bc = 1`; si no, desconocido.
- `razon_bc_01…15` = `P14_22_1…15` de `TB_SEC_XIV_2.csv` enlazado por `ID_PER` (si el `ID_PER` falta en ese archivo, desconocido): `1`→1, `0`→0 («no se declaró como respuesta afirmativa»), lo demás desconocido; sólo si `ayuda_bc = 0` y `denuncia_bc = 0`.

## 4 · Ejes y categorías (univariados; sin cruces)

Orden fijo:
1. `nacional`: `MX`.
2. `edad`: `15-29`, `30-44`, `45-59`, `60+` (60–120).
3. `escolaridad` (de `NIV` de `TSDem`, FD 2021, pregunta 2.7; convertido a entero):

   | código `NIV` (texto del FD) | categoría |
   |---|---|
   | 00 Ninguno | `ninguno` |
   | 01 Preescolar · 02 Primaria · 03 Secundaria · 05 Estudios técnicos o comerciales con primaria terminada · 06 Estudios técnicos o comerciales con secundaria terminada | `basica` |
   | 04 Preparatoria o bachillerato · 07 Estudios técnicos o comerciales con preparatoria terminada · 08 Normal con primaria o secundaria terminada | `media_superior` |
   | 09 Normal licenciatura · 10 Licenciatura o profesional · 11 Posgrado (Especialidad, Maestría o Doctorado) | `superior` |
   | blanco, no entero u otro entero | sin categoría: fuera de las celdas de escolaridad, dentro de los demás ejes |

   `GRA` no se usa.
4. `localidad`: `DOMINIO` crudo: `U`, `C`, `R`.
5. `pareja`: `T_INSTRUM` crudo: `A1`, `A2`, `B1`, `B2`, `C1`.
6. `entidad`: `CVE_ENT` crudo: `01` … `32`.

## 5 · Estimación por celda

Ponderador `FAC_MUJ` **sin normalizar**; estrato `EST_DIS` y UPM `UPM_DIS` como **texto opaco**; conglomerado = par (estrato, UPM).

1. Seleccionadas = filas del marco en la categoría (todas si `nacional`) con desenlace no desconocido; `n` = su número; `upm` = pares distintos entre ellas.
2. `n < 100` o `upm < 5` → `SUPRIMIDA` (`soporte`).
3. Marco de conglomerados = **todos** los pares del **marco completo** de §2, en orden de primera aparición en el archivo; cada par con `num = Σ FAC_MUJ × desenlace` y `den = Σ FAC_MUJ` sobre las seleccionadas; pares sin seleccionadas llevan (0, 0) y se quedan.
4. `p = Σnum / Σden`.
5. Bootstrap `R = 200`; `numpy.random.default_rng(s)` (PCG64), `s = 20260923 + Σ ord(c)` sobre el texto `desenlace + eje + categoría` (para los desenlaces de grupo, `desenlace` es `<grupo>__<ventana>`; para `institucion_bc_*` y `razon_bc_*`, que sólo tienen celda nacional, el texto es el nombre del desenlace solo). Estratos en orden de primera aparición en el marco de conglomerados; en cada réplica y estrato con `m` conglomerados, `rng.integers(0, m, m)` índices con reemplazo, sumando `num` y `den`; réplica = `Σnum/Σden` (no finita si `Σden = 0`).
6. Alguna réplica no finita → `SUPRIMIDA` (`replicas`).
7. IC = percentiles 2.5/97.5 (`numpy.quantile`, lineal); `se` con `ddof = 1`.
8. `ic95_sup − ic95_inf > 0.20` o (`p > 0` y `se/p > 0.30`) → `SUPRIMIDA` (`precision`); si no, `PUBLICABLE`.

## 6 · Salida y llaves

`RESULT-ENDIREH2021-NF-BC-TABLA`, lista JSON en este orden: (a) grupos en el orden de §3 × ventanas (`vida_relacion`, `desde_octubre_2020`) × ejes/categorías de §4 (49 celdas por desenlace): índices 0–489; (b) `ayuda_bc` × 49 celdas: 490–538; (c) `denuncia_bc` × 49: 539–587; (d) `institucion_bc_01…10`, nacional: 588–597; (e) `razon_bc_01…15`, nacional: 598–612. La llave `…-TABLA#k` es la celda de índice `k` (p. ej. `#495` = `ayuda_bc` × `escolaridad` × `ninguno`; `#544` = `denuncia_bc` × `escolaridad` × `ninguno`). Cada celda de salida lleva `resultado`, `ventana`, `eje`, `categoria` y los campos de §5.

## 7 · Lo que esta medición no es

GEN2 descriptivo RETROSPECTIVO de una ola ya vista; unidad persona (mujer). Las prevalencias A/B/C son cortes de instrumento (relaciones distintas), no se suman entre sí ni entre grupos; «no quiso» no se lee como elección sin restricciones; no estima subregistro total. No adopta nada.
