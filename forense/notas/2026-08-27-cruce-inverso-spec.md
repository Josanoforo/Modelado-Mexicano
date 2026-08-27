# Especificación congelada — `ACTO MAESTRA31-E5 · CRUCE-INVERSO`

`COMMIT-1` (A.3), 27/ago/2026. Congelada ANTES de correr el cruce contra `data/inventario-reactivos-v1_0.tsv`. Universo declarado: `main = 07b1452` (confirmado `origin/main` al arranque, sin diferencia).

## 1 · Extracción de las 79

La regex de forma de dirección, `[A-Z]{1,4}[0-9]+(_[0-9A-Z]+)*`, corrida cruda sobre `milpa/procedencia.yaml` + `milpa/tramite.yaml`, sí reproduce **79** distintos (verificado por comando propio antes de tocar nada más). Pero "de forma" es literal: captura también identificadores de generador (`G1`…`G6`), marcas de decisión de ADR (`D1`…`D4`), referencias de sección/hito (`C1`, `C3`, `R3`, `R3_2`, `E1`, `S2`, `V1`, `W1`, `X2`, `M2`, `P1`, `P2`, `P9`), estadística (`IC95`), compuertas (`IDG3`), rótulos de programa (`NUBE2`, `R101`) y una fuente-año sin token de reactivo (`ENIF2024`). Ninguno de esos es una variable de encuesta — son metadata interna del propio `procedencia.yaml`.

**Receta propia, declarada antes de cruzar:**

1. Partir los dos YAML en bloques separados por línea en blanco (unidad = una entrada/párrafo del archivo).
2. Descartar todo bloque que no mencione, en alguna de sus líneas, el nombre de una encuesta conocida (`ENCIG`, `ENVIPE`, `ENCUCI`, `ENIF`, `ENNViH`, `MxFLS`) — un token sin instrumento nombrado en su mismo párrafo no es citable como variable de este método.
3. Dentro de los bloques que sí nombran una encuesta, aplicar la regex de forma de dirección línea por línea.
4. Descartar dos clases de coincidencia de forma que no son variables por construcción, no por mera ausencia en el inventario:
   - Terminadas en `_XX` (comodín de rango declarado explícitamente en el propio archivo, p. ej. `AP5_4_XX`, no un reactivo concreto).
   - Los seis identificadores de generador `G1`…`G6` (nombres internos del motor, `canon/modelo-decision-v4_0.md`, no reactivos de encuesta).
5. Para cada token retenido, registrar también la encuesta+año (si el año aparece a menos de una palabra del nombre de encuesta en la misma línea, si no en la última mención vista en el bloque) — es el "instrumento declarado por el motor" contra el que se juzga `EXISTE-SATISFACE` vs. `EXISTE-NO-SATISFACE`.

**Resultado: 39 → 59 según el filtro se aplique por bloque-completo o línea-por-línea con arrastre; la versión final usada (línea por línea con arrastre del último instrumento visto en el bloque) da 59, no 79.** Se manda ésta, no la de dirección: **el conteo propio difiere del declarado (79) y se declara aquí, antes de ver el cruce.**

**Control positivo (`CANDIDATO-EMITE` v1.1):** los tres casos sirven de prueba — `CIV-01/ENCIG/P8_3_1`, `CIV-06/ENCUCI/AP5_3_8`, `CIV-07/ENVIPE/BP1_20` — los tres sobreviven el filtro propio (`P8_3_1`, `AP5_3_8`, `BP1_20` están en el conjunto de 59). La receta no pierde ningún caso conocido; lo que pierde son 20 coincidencias de forma que el propio archivo usa como notación interna, no como variable.

**Limitación declarada, no resuelta:** el filtro de co-ocurrencia con nombre de encuesta no es perfecto — deja pasar algunos residuales de forma similar (p. ej. `P1`, `P9`, `IC95`, `ENIF2024` aparecen en párrafos que sí nombran una encuesta cercana, sin ser ellos mismos un reactivo). Esto se reporta explícitamente en el resultado de Q3 (§4 abajo) en vez de perseguirse con una tercera vuelta de regex — una vuelta más de ajuste después de ver casos concretos es exactamente lo que la frase de sello prohíbe.

## 2 · Regla de emparejamiento (token exacto)

- **Token:** coincidencia exacta de cadena contra la columna `variable_id` de `data/inventario-reactivos-v1_0.tsv` (sin normalizar mayúsculas/minúsculas — los 59 tokens del motor son todos mayúsculas por construcción de la regex, y así se comparan).
- **Normalización de instrumento:** `procedencia.yaml`/`tramite.yaml` nombran la encuesta en prosa (`ENCIG`, `ENVIPE`, `ENCUCI`, `ENIF`, `ENNViH`/`MxFLS`) más un año suelto (`ENCIG 2023`); la columna `instrumento` del inventario usa `familia+año` pegado en minúsculas (`encig2023`, `envipe2025`). Regla declarada: `instrumento_inventario ~ (familia, año)` si `lower(familia_motor) == prefijo_alfabético(instrumento_inventario)` y (`año_motor is None` o `año_motor == sufijo_numérico(instrumento_inventario)`). Sin este mapeo, ninguna fila del inventario podría casar nunca con una cita del motor — es la trampa que el encargo advierte, declarada aquí antes de correr, no descubierta al chocar.
- **Ola:** la columna `ola` del inventario está en `NO_DETERMINADO` en el 100% de las filas muestreadas para los instrumentos relevantes (verificado por comando); la ola real vive codificada en el propio nombre del instrumento (`encig2011` … `encig2025` son olas distintas de la misma familia). Por tanto Q2 (conteo de olas) se opera sobre el conjunto de valores distintos de `instrumento` que llevan la variable, no sobre la columna `ola`.

## 3 · Esquema de salida y escala A.4

`data/cruce-inverso-v1_0.tsv`, una fila por variable del motor (59 filas):

| columna | contenido |
|---|---|
| `variable_id` | el token |
| `veredicto_a4` | `EXISTE-SATISFACE` \| `EXISTE-NO-SATISFACE` \| `NO-ENCONTRADO` |
| `instrumentos_declarados_por_motor` | lista `familia:año` (o `familia:sin-ano`) extraída del párrafo |
| `n_citas_en_motor` | cuántas veces aparece el token en los dos YAML |
| `payloads_en_inventario` | `payload_id` donde aparece, si existe |
| `instrumentos_en_inventario` | valores de `instrumento` donde aparece, si existe |
| `n_olas_distintas` | Q2: cardinalidad de `instrumentos_en_inventario` |
| `olas_detalle` | mismo listado, explícito |

Escala A.4 de Q1: `EXISTE-SATISFACE` = aparece en el inventario bajo un instrumento cuya familia+año casa con lo declarado por el motor · `EXISTE-NO-SATISFACE` = aparece en el inventario pero bajo una familia/año distinta a la declarada · `NO-ENCONTRADO` = el token no aparece en ninguna fila de `variable_id` (universo: 36,809 valores distintos de esa columna, 178,246 filas, comando en el cierre).

## 4 · B-bis — qué significaría cada resultado, antes de ver el dato

- **Q1 alto (la mayoría `EXISTE-SATISFACE`):** corrobora que el motor cita variables reales, en el instrumento correcto — un resultado interesante por sí mismo, no un no-hallazgo. Se reporta como corroboración, no se minimiza.
- **Q1 bajo (la mayoría `NO-ENCONTRADO`):** ninguna variable se relaja para subirlo; se reporta tal cual, con el comando y universo al lado por cada fila `NO-ENCONTRADO`.
- **Q2 alto (variables en muchas olas):** oportunidad de panel/réplica no explotada por el motor hoy — el motor cita una variable puntual sin saber que vive en 8+ rondas del mismo instrumento.
- **Q2 = 0 (todas las que existen viven en una sola ola):** no hay oportunidad de panel oculta en esta receta; el motor ya está citando la única ola disponible.
- **Q3 confirmando el techo (los 13 `ASIGNADO_PROBABILIDAD`, u otros, sin ninguna cita):** dice que el límite del emparejamiento por token es estructural (juicio puro, sin reactivo que citar), no arreglable con más corpus.
- **Q3 refutando el techo (los 13 sí citan algo):** contradice `forense/perimetro-alcanzable-v1_0.md` y se reporta como discrepancia a re-derivar, no se oculta.

## 5 · Frase de sello

«El primer resultado que produzca este procedimiento es el que se reporta.»
