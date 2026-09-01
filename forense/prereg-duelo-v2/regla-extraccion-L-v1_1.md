# Regla de extracción congelada — `L-extraido-v1_1` (P1 de MAESTRA33-E21)

Encargo: `forense/encargos/2026-09-01-MAESTRA33-E21-EXTRAE-L-V1_1.md`. Este
documento es el COMMIT-1 del acto: la regla se congela AQUÍ, antes de tocar
las 176 capturas. `tools/extrae_l_v1_1.py` (P2) la aplica sin cambiarla.

## Inspección — 5 capturas, elegidas por ÍNDICE FIJO (no por contenido)

`ls corridas-L | grep -- '-M-' | sed 's/__.*//' | sort -u` da, en orden, las
celdas-M: `L-CIV-M-01-M`, `L-CIV-M-06-M`, `L-CIV-M-08-M`, … Las dos
PRIMERAS por ese orden son `CIV-M-01` y `CIV-M-06`. El índice fijo pedido
por el encargo (1ª captura de cada variante, de las dos primeras celdas) da
4 capturas; la 5ª es la 1ª captura de la variante `L-solo` de la TERCERA
celda en el mismo orden (`CIV-M-08`) — elegida por continuar la misma regla
de índice (siguiente celda de la lista), no porque su contenido llamara la
atención:

1. `L-CIV-M-01-M__L+corpus__01.json`
2. `L-CIV-M-01-M__L-solo__01.json`
3. `L-CIV-M-06-M__L+corpus__01.json`
4. `L-CIV-M-06-M__L-solo__01.json`
5. `L-CIV-M-08-M__L-solo__01.json`

## Lo que la inspección encontró sobre el formato real de `texto_crudo`

- El encabezado de la sección de estimación NO es uniforme: aparece como
  `## Estimación` (capturas 2, 4), `## Estimación puntual (...)` (dentro de
  la captura 1, como sub-nivel `###`... en realidad aparece como `###
  Estimación puntual` en algunos, `## Respuesta` en otras — capturas 1
  (heading raíz `## Estimación` sí presente), 3 y 5 (`## Respuesta`, sin la
  palabra "Estimación" en ningún encabezado).
- Cuando no hay ningún encabezado con la palabra "Estimaci-", el cuerpo del
  texto igual puede traer números utilizables más abajo (captura 5), o no
  traer ninguno reconocible bajo la regla de abajo.
- Las cifras aparecen como: decimal en `[0,1]` (`≈ 0.32`), porcentaje simple
  (`≈ 25 %`, `61.0%`), rango de porcentaje con signo `%` repetido en ambos
  extremos (`20 %–27 %`) o con un solo `%` al final (`20–30 %`), y rango
  decimal (`0.25 – 0.40`).
- Todas las 5 capturas inspeccionadas abren con una frase de cobertura
  ("No conozco/no tengo/no cuento con el dato exacto...") y AÚN ASÍ, en 4 de
  5, dan un número más abajo. La regla de abajo NO trata esa frase de
  cobertura como razón automática de NO-EXTRAIBLE — solo la ausencia de
  número lo es (ver piloto CIV-08, que también abre con esa frase y aun así
  tiene `valor_extraido` numérico en 7 de 8 réplicas).

Sin mirar R, M ni ningún scoreboard en este paso — la regla sale solo de la
forma del texto en L.

## Regla congelada

1. **Localizar la sección.** Buscar la primera línea que sea un encabezado
   Markdown (`#`+) cuyo texto contenga, sin importar mayúsculas/acentos,
   la subcadena "estimaci" (cubre "Estimación", "Estimación puntual",
   etc.). Si no existe tal encabezado en todo el documento, la "sección" es
   el documento completo (fallback empírico — captura 5 de la inspección).
2. **Delimitar la sección.** Si se localizó un encabezado, la sección corre
   desde esa línea hasta la siguiente línea que sea un encabezado del MISMO
   nivel (mismo número de `#`) o de nivel más alto (menos `#`), o hasta el
   final del documento si no hay tal encabezado siguiente.
3. **Extraer el primer número**, buscando dentro de la sección, en el orden
   en que aparece en el texto (no por prioridad de forma), la primera
   coincidencia de cualquiera de estos patrones:
   - Rango de porcentaje: `N[-–—]N%` (con o sin `%` repetido en el primer
     número, con o sin espacio antes del signo) → **punto medio**, luego
     `/100`.
   - Porcentaje simple: `N%` (con o sin `≈`/`~` antes) → `/100`.
   - Decimal explícito no seguido de `%`: `0.NN` → tal cual (ya en
     `[0,1]`).
   Un número de 4 cifras sin `%` ni forma decimal (años como `2017`,
   códigos como `AP4_4_03`) nunca coincide con ninguno de los tres patrones
   — no hace falta una exclusión aparte.
4. **Sin número extraíble en la sección → `NO-EXTRAIBLE`**, `valor` vacío.
   Esto incluye el caso "no sé"/"sin dato" SOLO cuando, además, no hay
   ningún número en la sección bajo los patrones de (3).
5. **Punto medio para rangos**, como arriba.
6. **Unidad de almacenamiento:** el TSV guarda `valor` ya normalizado a
   `[0,1]` (porcentajes divididos entre 100), tal como pide el encargo.
   Se declara aquí, ANTES de aplicar la regla, que esto difiere de la
   convención observada en las capturas del piloto CIV-08, donde
   `valor_extraido` quedó grabado en escala porcentual sin dividir (`61.0`,
   `23.5`, no `0.61`, `0.235`) — la regresión (P2) documenta esa diferencia
   de unidad explícitamente; no se reinterpreta el piloto para que cuadre.
7. **No pondera fuente ni confianza.** La regla no distingue "dato oficial
   verificado" de "recuerdo no verificado" — toma el primer número que
   cumpla (3), en el orden del texto, sin juicio de calidad. Esto es una
   limitación conocida y declarada, no un descuido: el encargo pide una
   regla mecánica y congelada, no un segundo juicio humano por celda.
8. **No mira R, M ni el scoreboard** en ningún punto de (1)-(7).

## Frase de sello

> Esta regla queda CONGELADA a partir de este commit, aplicable SIN
> EXCEPCIÓN a las 176 capturas de `corridas-L/*-M-*.json`, derivada
> únicamente de la forma del texto en las 5 capturas de índice fijo de
> arriba, sin mirar contenido adicional, sin mirar R, sin mirar M, sin
> mirar el scoreboard. `tools/extrae_l_v1_1.py` implementa exactamente
> los pasos (1)-(8); cualquier cambio posterior a esta regla es un acto
> nuevo, no una edición de este documento.
