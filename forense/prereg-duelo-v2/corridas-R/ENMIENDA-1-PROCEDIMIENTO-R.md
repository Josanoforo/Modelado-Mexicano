# ENMIENDA 1 al PROCEDIMIENTO R v1.0 — antes de correr, no hacia atrás

**ACTO MAESTRA30-E7 · R-SCORING**, 26/ago/2026. Commit propio, posterior al `COMMIT-1` y **anterior** al `COMMIT-2`. El `PROCEDIMIENTO-R-v1_0.md` **no se edita**: lo que sigue lo enmienda por adición, conforme al mandato del encargo («si el COMMIT-1 tenía un error, tercer commit lo dice; nunca se corrige hacia atrás»).

**Ninguno de los tres puntos de abajo se descubrió mirando un valor.** Los tres salen de catálogos y descriptores de archivo — nombres y etiquetas de variable, que es lo que esta fase permite leer. Al cerrar esta enmienda **sigue sin abrirse un solo valor de microdato**.

---

## A · Faltaba la regla de codificación `y → {0,1}`

El `COMMIT-1` congeló estimador, varianza, payload, tabla, columna y diseño, pero **no** cómo se recodifica la respuesta a `{0,1}`. Sin esa regla el estimador no está determinado. Se congela aquí, por celda, con la etiqueta verbatim del catálogo o descriptor:

| celda | variable | catálogo / descriptor | `y = 1` cuando | `y = 0` cuando | excluidos del universo |
|---|---|---|---|---|---|
| CIV-08 | `AP4_4_03` | `catalogos/ap4_4_03.csv`: 1 Seguro(a) · 2 Inseguro(a) · 3 No aplica · 9 NS/NR | `== "2"` (**Inseguro**) | `== "1"` | `3`, `9`, vacío |
| DIN-03 | `P7_1` | `fd_enif2012.xlsx` hoja `TMODULO2`: 1 Sí | `== "1"` | `== "2"` | resto, vacío |
| DIN-05 | `P8_1_1` | `enfih_2019_fd.xlsx` hoja `TModulo`: 1 Sí | `== "1"` | `== "2"` | resto, vacío |
| DIN-11 | `P5_3` | `catalogos/p5_3.csv`: 1 Sí · 2 No | `== "1"` | `== "2"` | resto, vacío |
| SFT-04 | `H16D_18` | `enasem_2018_fd.xlsx`: códigos `1,2,8,9`; 1 Sí | `== "1"` | `== "2"` | `8`, `9`, vacío |
| SFT-06 | `F55_24` | `enasem_2024_fd.xlsx`: códigos `1,2,8,9`; 1 Sí | `== "1"` | `== "2"` | `8`, `9`, vacío |
| TIC-01 | `p3i` | `catalogos/p3i.csv`: 1 Sí · 2 No · 9 No sabe | `== "1"` | `== "2"` | `9`, vacío |
| TIC-08 | `P7_15` | `fd_endutih2024.xlsx`: `[1-2]`; 1 Sí | `== "1"` | `== "2"` | resto, vacío |
| TIC-12 | `p3n` | `catalogos/p3n.csv`, 10 categorías + 99 No sabe | ver **C** | ver **C** | `99`, vacío |

**CIV-08 lleva la polaridad invertida y se dice aquí, no después.** El código `1` es *Seguro(a)*, pero la celda mide **inseguridad percibida** (su `frase_discriminacion`: «Inseguridad percibida en la calle es el indicador ENVIPE más publicado»). Por eso `y=1` es el código **`2`**. Congelar esto antes de correr es justamente lo que impide elegir la polaridad que haga cuadrar el resultado.

**Regla general de no-respuesta:** todo código de no-respuesta, no-aplica o vacío **sale del denominador** — no se imputa, no se cuenta como `0`. El `N` efectivo de cada celda queda escrito en su JSON.

---

## B · `TIC-06` — el `COMMIT-1` nombró la tabla equivocada, y al ir a corregirla la SpecCelda no cierra

**El error del `COMMIT-1`:** puso `ENTI2022_05A11.DBF`, que es la tabla de **5 a 11 años**. El universo de la SpecCelda es de **12 a 17 años**. La tabla estaba mal.

**Y la corrección no se puede hacer**, porque la `SpecCelda` de TIC-06 apunta a cuatro referentes que no concuerdan entre sí:

| campo del marco | dice | qué es en el árbol |
|---|---|---|
| `variable` | `P2` | en `ENTI2022_VIV.DBF`, `P2` es «¿Todas estas personas comparten un mismo gasto para comer?» (Sí/No) — nada laboral |
| `universo` | tabla `ENTI2022_CB12A17.DBF` | **no existe**; las siete tablas del payload son `05A11`, `12A17`, `COE1`, `COE2`, `HOG`, `SDEM`, `VIV` |
| `estimador` | categoría «Tiene menos de un año en este trabajo» | es **`P5F15`**, y vive en **`ENTI2022_COE1.DBF`** (`enti_2022_fd.pdf`, campo 161) |
| `frase_discriminacion` | «Trabajar todos los meses del año» | es **`P5F14`** — **otra categoría distinta** de la que el estimador nombra (campo 160) |

Cuatro referentes, ninguno compatible con los otros tres. Elegir entre `P2`, `P5F14` y `P5F15` sería **inventar la spec**, y el marco congelado es artefacto sellado (`sha256 3a0dcf01…0c3742e2`, pineado en F1): **este acto no lo edita.**

**`TIC-06` pasa a `RESERVA-SPEC-INCONSISTENTE`.** No se computa `R`. Las celdas arbitrables bajan de **10 a 9**.

---

## C · `TIC-12` — «por categoría» no es un escalar

El estimador verbatim es «proporcion ponderada (por categoria de medio de entero)» sobre una escala `categorica k=10`. Eso es un **vector**, y el scoring necesita un escalar. Se congela así:

- **`R` principal = proporción ponderada de la categoría `8`** («Por medio de un familiar, amigo o conocido»). Es la categoría que la propia `frase_discriminacion` señala: «red personal contra anuncio contra bolsa formal […] toca `cooperacion.confianza.puente_personal`».
- **`y=1` si `p3n == "8"`, `y=0` si `p3n` es cualquier otra categoría válida `1..10`; `99` y vacío salen del denominador.**
- **El vector completo de las 10 categorías se escribe igualmente** en el JSON de la celda, cada una con su `EE`. La elección de la categoría 8 como principal queda **declarada aquí, antes de correr**, y el vector permite verla contra las otras nueve.

---

## D · Recuento tras la enmienda

| `estado_R` | celdas | cuáles |
|---|---:|---|
| arbitrable | **9** | CIV-08, DIN-03, DIN-05, DIN-11, SFT-04, SFT-06, TIC-01, TIC-08, TIC-12 |
| `RESERVA-SIN-MICRODATO` | 4 | DIN-07, EMP-02, EMP-04, EMP-05 |
| `RESERVA-SIN-PAYLOAD` | 1 | DOC-06 |
| `RESERVA-SPEC-INCONSISTENTE` | 1 | TIC-06 |

La frase de cierre del `COMMIT-1` sigue rigiendo sin cambio: «el primer resultado que produzca este procedimiento es el que se reporta».
