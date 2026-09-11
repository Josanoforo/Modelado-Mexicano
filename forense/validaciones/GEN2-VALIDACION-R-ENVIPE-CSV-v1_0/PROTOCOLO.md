# Protocolo v1.0 · validación independiente de tres R ENVIPE CSV

**Fijado:** 11 de septiembre de 2026, antes de ejecutar el cálculo de contraste de este acto.

## Alcance y exposición previa

Se validarán solamente `CALC-R-CIV-M-10`, `CALC-R-CIV-M-12` y
`CALC-R-CIV-M-13`: ENVIPE 2021/2023/2024, que corresponden a delitos de
2020/2022/2023. No se medirán las ocho olas de `#697`, las olas DBF ni
`CIV-M-01/-02/-04`.

El ejercicio **no es ciego ni una prehipótesis original**. Antes de fijar este
protocolo la sesión leyó los tres `resultados.json`, la spec y la nota histórica;
por tanto conoce puntos, EE, IC, CV, embudos y el rótulo histórico de UPM única.
Esos valores no eligen definición, filtros, algoritmo ni tolerancias: sólo se
abren de nuevo para comparar después de que los autocontroles independientes
pasen.

## Fuentes e identidad exigida

| Celda | Encuesta / hechos | payload | SHA-256 del ZIP | miembro de datos exacto |
|---|---|---|---|---|
| `CIV-M-10` | 2021 / 2020 | `envipe2021_csv` | `88153c67ff3666be511dab3f3b483226a0af9f0e8683bd8dbfba8d616ddbfdd1` | `conjunto_de_datos_TMod_Vic_ENVIPE_2021/conjunto_de_datos/conjunto_de_datos_TMod_Vic_ENVIPE_2021.csv` |
| `CIV-M-12` | 2023 / 2022 | `envipe2023_csv` | `0dcc00a7fc37b79806f1bf1b85b12cd090b5ecc8e76983a3a1a861f2ef3fb404` | `tmod_vic_envipe2023/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2023.csv` |
| `CIV-M-13` | 2024 / 2023 | `envipe2024_csv` | `90776b2fab6e3666dad1cb5f5f3eb7d6a7699dbfefd4f8f04f07fb01e61a6fb2` | `tmod_vic_envipe2024/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2024.csv` |

Antes de estimar, el ejecutable deberá verificar el SHA-256 de cada ZIP y la
existencia única del miembro literal. También fijará en la evidencia el nombre y
SHA-256 internos del diccionario de `TMod_Vic` y del catálogo `BP1_23`, y
verificará las columnas `ID_PER`, `ID_DEL`, `BPCOD`, `BP1_23`, `FAC_DEL`,
`EST_DIS` y `UPM_DIS`. Los cuestionarios de módulo y descriptores se verifican
contra estos ids y hashes del manifiesto:

| Ola | cuestionario (id · SHA-256) | descriptor (id · SHA-256) |
|---|---|---|
| 2021 | `envipe2021_cuest_modulo_pdf` · `390ef00ec15cabb9dcdf86d9fa79e108cea4ef1a2e8fdfcf4f4c409794636e0c` | `envipe2021_fd_pdf` · `d85775241d6f427d6dd6643bce973ed0bdbfca4e0b0d6a9b02265e8327179945` |
| 2023 | `envipe2023_cuest_modulo_pdf` · `98d3c632cc038c4a9a1ff129efb63f6d1ac786f46e4886aaaf5aff92b4cdf5b4` | `envipe2023_fd_pdf` · `743c260e89a6c5d6f2fcc6eac0f1884c40bc6b437164b34e13ba6fe1caf1be63` |
| 2024 | `envipe2024_cuest_modulo_pdf` · `7628127d5e9bd4424737f7a8cb60bbded28e21c2242d1f412c86367e03836e28` | `envipe2024_fd_pdf` · `f8d72038595746ceac21e5096462b277e757d7501bd3a1b61ac86bf9fc0d57d5` |

La documentación primaria de diseño es la serie oficial del INEGI
“ENVIPE. Diseño muestral”: 2021 (`UPC 889463902454`), 2023
(`UPC 889463912637`) y 2024 (`UPC 889463920014`). Las tres describen un diseño
probabilístico, estratificado, multietápico y por conglomerados; proporciones por
estimador de razón y precisión por series de Taylor con conglomerados últimos.
No se conservará una descarga nueva en el repo.

## Cantidad a reconstruir

Unidad: **DELITO**, una fila de `TMod_Vic`; no se colapsan varios delitos de la
misma persona. El universo `U_R` exige:

1. `BPCOD` entero en `01..15` (todos los tipos, no sólo personales);
2. `BP1_23` entero en `01..09`;
3. `FAC_DEL` finito y estrictamente positivo.

`y=1` para `BP1_23 ∈ {01,02,06}` y `y=0` para
`{03,04,05,07,08,09}`. `99`, blanco y cualquier otro código quedan fuera.
No se filtra `BP1_20`, no se usa `FAC_DEL_AM` ni un peso de persona. El punto es
`R = Σ FAC_DEL·y / Σ FAC_DEL`. Numerador y denominador se acumulan como
`Decimal`; los identificadores `EST_DIS`/`UPM_DIS` son texto opaco, sin
conversión numérica, relleno ni conjetura sobre su ancho.

El embudo contará tabla completa; `BPCOD` inválido; `BP1_23` blanco, `99`,
`01..09` y otro; ponderador inválido; diseño vacío; frecuencia `01..09`; `n`;
personas y delitos por persona; numerador y denominador ponderados.

## Incertidumbre y dos preguntas separadas

### A. Reproducción del contrato histórico

Se programará de la definición, sin importar ni copiar `medidor.py`,
`tools/arbitra.py`, `tools/valida_envipe_independiente.py` o
`tests/svystat.py`. Para cada UPM observada en `U_R` se sumará
`z_hi = Σ FAC_DEL·(y-R)`. Por estrato con `m_h>1` se sumará
`m_h/(m_h-1)·Σ(z_hi-z̄_h)^2`; la raíz, dividida por `ΣFAC_DEL`, es el EE.
Un estrato restringido con una UPM aporta cero **sólo para reproducir el
contrato histórico**. El IC histórico es normal, bilateral 95 %, con
`z=1.959963984540054`, recortado a `[0,1]`; `CV=EE/R`.

### B. Suficiencia inferencial del diseño observado

Igualar el EE de A no acredita B. Para cada estrato se comparará el número de
UPM en tres ámbitos: `U_R`, toda `TMod_Vic`, y toda `TVivienda` del mismo ZIP.
Las UPM presentes fuera de `U_R` se conservarán con contribución linealizada
cero en un cálculo diagnóstico de dominio. Se reportarán por separado:

- singletons creados al restringir a `U_R`;
- singletons que persisten en `TMod_Vic`;
- singletons que persisten en `TVivienda`;
- UPM adicionales recuperadas en cada ámbito;
- EE/IC diagnóstico al conservar las UPM observables de `TVivienda`.

La comparación de dominio no se escogerá por cercanía al productor y no lo
reescribirá. Si `TVivienda` no contiene el diseño completo, o un singleton
persiste sin acreditación documental como unidad de certeza, la aptitud
inferencial quedará `NO-ACREDITADA` para ese componente. No se llamará
“conservador” ni “límite inferior” a ningún IC por intuición: añadir ceros puede
ensanchar o estrechar una varianza según los totales entre UPM.

## Autocontroles previos al corpus

El ejecutable abortará antes de leer/comparar los productores salvo que pasen
estos casos con resultado calculado a mano:

1. pesos `1` y `3`, desenlaces `1` y `0` → numerador `1`, denominador `4`,
   `R=0.25`;
2. `99`, blanco, `BPCOD=16` y peso no positivo quedan fuera con su contador;
3. dos delitos de la misma `ID_PER` siguen siendo `n=2`;
4. estrato A con dos UPM `(w,y)=(1,1),(1,0)` y estrato B singleton
   `(2,1)` → `R=0.75`, varianza histórica `0.0625`, `EE=0.25`;
5. dominio con dos UPM de puntuaciones `+0.5,-0.5` → `EE=0.5`; al conservar
   una tercera UPM de puntuación cero → `EE=sqrt(0.1875)`, prueba de que la
   dirección del cambio no está predeterminada.

## Tolerancias y veredictos

- Conteos, frecuencias, numerador y denominador enteros: igualdad exacta.
- Punto: diferencia absoluta `≤ 1e-12` (proporción; muy inferior a una unidad
  en el noveno decimal y a la precisión publicada de seis decimales).
- EE y CV: diferencia absoluta `≤ 1e-10`; extremos del IC `≤ 2e-10`, para
  absorber sólo orden de suma en `float64`, no una diferencia metodológica.

Cada celda tendrá tres veredictos distintos:

- `concordancia_numerica`: punto, EE/IC/CV bajo el contrato histórico;
- `validacion_punto`: identidad, universo, codificación, pesos y aritmética;
- `aptitud_inferencial`: si la varianza puede sostenerse con el diseño completo
  observable, o el componente exacto que queda sin acreditar.

Los outputs congelados de los tres `CALC` son sólo lectura. La eventual
integración con el contrato de linaje/adopción del encargo 17 se hará únicamente
si ese contrato está fusionado en `main`; este acto no incorpora su rama.
