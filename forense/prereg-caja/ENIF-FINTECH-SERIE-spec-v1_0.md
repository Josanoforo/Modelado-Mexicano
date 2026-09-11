# Prerregistro · ENIF-FINTECH-SERIE v1.0

**Acto:** `GEN2-ENIF-FINTECH-SERIE-DESCRIPTIVA`
**Estado al congelar:** preguntas, universos, codificación, precisión y aceptación fijados antes del primer resultado 2021.
**Sucesión:** formaliza y extiende el sondeo descriptivo ENIF 2024 de `GEN2-ADQ-VERIFICACION-CAJA`; no reescribe ni vuelve a contar aquel resultado.

## 1. Pregunta y unidad

Pregunta descriptiva por ola y familia: entre personas elegidas que declaran tener una cuenta o un crédito contratado por Internet/aplicación en la categoría específica del instrumento, ¿cuál es la distribución ponderada del canal de contratación del **último** producto de esa familia?

Unidad: persona elegida. Cuenta y crédito son estimandos separados. El cruce nunca identifica que el último producto sea el producto fintech declarado; por eso no estima canal del producto fintech exacto, adquisición causal, aprobación, rechazo ni recomendación.

## 2. Correspondencia previa al cálculo

La tabla congelada es `data/corrida0/enif-fintech-correspondencia-v1_0.tsv`.

- **2018:** `NO-ESTIMABLE` para ambas familias. Las baterías enumeran productos tradicionales y “otro”, no una categoría de cuenta/crédito por Internet o aplicación, y no preguntan el canal del último producto. `P5_23` es uso de banca por celular sobre una cuenta bancaria; no se recodifica como tenencia fintech. Además, la población es 18–70, frente a 18+ en 2021/2024. No se abre una categoría “otro” para inferir fintech.
- **2021 cuenta:** `P5_4_8=1` y canal `P5_17`. Se mide como descriptivo propio. No se calcula delta con 2024: en 2024 el criterio añade “(no bancaria)”, cambia los ejemplos y el catálogo del canal incorpora programa social y separa “otro”.
- **2021 crédito:** `P6_2_8=1` y canal `P6_7`. Es comparable con `P6_2_8×P6_6` de 2024 por texto nuclear y catálogo de canal; se permite delta por canal, declarando la deriva del ejemplo Playbusiness→YoTePresto.
- **2024:** control ya publicado en `milpa/procedencia.yaml`; sólo se reproduce puntualmente crédito/app para falsar una receta equivocada. No se emiten nuevos `RESULT-*` numéricos 2024.

Autoridades leídas: cuestionarios y FD ENIF 2018/2021/2024 existentes en el corpus; no se usó la ausencia de texto del inventario como prueba semántica.

## 3. Fuentes congeladas

| rol | id de manifiesto | archivo | sha256 |
|---|---|---|---|
| microdato 2018, sólo correspondencia | `enif2018_csv` | `enif2018_csv.zip` | `51f33ec74ccd596dc74b695587310d02e651923467255520aadc4d9fe13461d5` |
| microdato primario 2021 | `enif2021_csv` | `enif2021_csv.zip` | `0f314fa3733b4b5519486ed4015fca1c9e0864840bcd5944aa7de27796fe5cd9` |
| control 2024 | `enif2024_csv` | `enif2024_csv.zip` | `a3507b4038888247f565f1640a718ef552bb8fc363378e3372a5bf2796bb2e4c` |
| FD 2018 | `enif2018_fd_xlsx` | `enif_2018_fd.xlsx` | `dd8d5c92a7a031505d95da3ee6f00b670f90d5fd5cbd94c744393ffe81b4f6d7` |
| cuestionario 2018 | `enif2018_cuestionario_pdf` | `enif_2018_cuestionario.pdf` | `cda9a0283a39514e404c53aacb1d0200b68b38f29d8e06b4cd2386a4b8b558e9` |
| FD 2021 | `enif2021_fd_zip` | `enif_2021_fd_pdf.zip` | `6f4e3aab705ddb6910607be15aa711eca56ef5060dcc60bc941d201ef3079457` |
| cuestionario 2021 | `enif2021_cuestionario_pdf` | `enif_2021_cuestionario.pdf` | `2fe495a58f2eae73aa3f583d2859de3aa062c4d925453cb6522939c1fea81e16` |
| FD 2024 | `enif2024_fd_xlsx` | `enif_2024_fd.xlsx` | `17e2ad86ce9e4fd5783ee54e9b51ee436b934e002d5736b82094070c74a25db2` |
| cuestionario 2024 | `enif2024_cuestionario_pdf` | `enif_2024_cuestionario.pdf` | `32e37cc13da38691dee20fbffcef3637aeb87b8dac194e64f83bebed8b57ef8b` |

Miembro 2021: `conjunto_de_datos_tmodulo_enif_2021/conjunto_de_datos/conjunto_de_datos_tmodulo_enif_2021.csv`. Miembro de control 2024: `conjunto_de_datos_tmodulo_enif_2024/conjunto_de_datos/conjunto_de_datos_tmodulo_enif2024.csv`.

## 4. Universos, códigos y especiales

### Cuenta 2021

- Filtro: `P5_4_8='1'`; `2` es no tenencia. Blanco u otro código es falta del criterio y se cuenta fuera.
- Denominador: filtro verdadero, `FAC_ELE` finito y positivo, `P5_17∈{1,…,7}`.
- Canal: 1 sucursal; 2 app celular; 3 página de Internet; 4 establecimiento/corresponsal; 5 promotor; 6 empresa donde trabaja; 7 otro.
- `P5_17=9` (“No sabe”), blanco y cualquier código fuera de catálogo se reportan por separado y salen del denominador.

### Crédito 2021

- Filtro: `P6_2_8='1'`; `2` es no tenencia. Blanco u otro código es falta del criterio y se cuenta fuera.
- Denominador: filtro verdadero, `FAC_ELE` finito y positivo, `P6_7∈{1,…,6}`.
- Canal: 1 sucursal; 2 app celular; 3 página de Internet; 4 establecimiento; 5 promotor/llamada; 6 otro.
- `P6_7=9` (“No sabe”), blanco y cualquier código fuera de catálogo se reportan por separado y salen del denominador.

Ponderador 2021: `FAC_ELE`, factor de expansión de la persona; no se sustituye por `FAC_PER` de otra ola. Diseño: `EST_DIS` (estrato) y `UPM_DIS` (UPM), conservados como texto opaco. `EDAD` sólo es guardia de que no haya edad observada menor de 18; no filtra.

## 5. Estimación y precisión

Para cada canal `c`,

`p_c = sum(FAC_ELE * 1[canal=c]) / sum(FAC_ELE)`

sobre el denominador de la familia. Se publican `n` y masa ponderada de numerador, `n` y masa ponderada del denominador, faltantes/especiales, `p`, error estándar e IC95.

La varianza usa linealización de razón por conglomerado último: residual `z_i = I(dominio) w_i(y_i-p)/N_d`, agregado por UPM dentro de estrato sobre la muestra completa con ponderador válido. Los estratos con una sola UPM se cuentan y no aportan grados de libertad; si existen, el método se rotula `ULTIMATE-CLUSTER-CON-ESTRATOS-UPM-UNICA`. Filas del dominio sin diseño entran al punto, no a la varianza, y se cuentan. IC normal truncado a [0,1]. No se usa bootstrap ni semilla.

Las olas son cortes transversales, no panel. No se hacen pruebas de significación ni se agrupan canales después del dato.

## 6. Control independiente y control 2024

`control_independiente.py`, congelado junto con el medidor, reconstruye con una implementación separada para crédito/app 2021: `n` y masa de numerador, `n` y masa de denominador y proporción. No importa código del medidor.

El medidor reproduce puntualmente crédito/app 2024 y sólo emite un guardia textual si `n=200`, masa redondeada `1,178,431` y `p` redondeada a tres decimales `0.575`, valores ya publicados. Cualquier discordancia para la ejecución.

## 7. Aceptación y parada

- Columnas y payloads coinciden con manifiesto; ningún nombre físico se hereda entre olas.
- Las categorías publicadas de cada familia suman 1 dentro de tolerancia `1e-10` antes del redondeo.
- Se reportan denominadores, especiales, pesos inválidos y diseño por familia.
- El control separado de crédito/app coincide con el resultado primario a `1e-12` en proporción y a `1e-6` en masas.
- El control 2024 coincide a la precisión publicada; si no, `NO-REPRODUCE` y no se ajusta el medidor.
- 2018 permanece `NO-ESTIMABLE`, no cero. Cuenta 2021/2024 no recibe delta. Crédito sí puede recibir delta sólo usando los porcentajes 2024 ya publicados.
- Uso: evidencia contextual para `dinero.credito.scoring_alternativo`; `DESCRIPTIVO-NO-CALIBRA`. No modifica tasas del motor ni el M de F5.

## 8. A.8 y contaminación declarada

`python3 tools/ya_medido.py dinero.credito.scoring_alternativo` resolvió la regla a `R1.6` y devolvió `NUNCA-MEDIDA`. Este CALC no mide esa probabilidad del motor: mide un proxy descriptivo de canal y no cambia el estado de la regla.

Antes de congelar se conocían los porcentajes 2024 publicados y la correspondencia de reactivos/códigos; no se conocían ni calcularon las distribuciones 2021. Se abrió una fila del CSV 2021 únicamente para comprobar cabecera/formato y detectar `FAC_ELE`; no se tabuló ningún desenlace.
