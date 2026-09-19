# Cruces históricos ENCIG 2023/2021 · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

## Estimando y documentación previa

Proporción de **trámites** de pago ordinario de luz (`N_TRA=01`) realizados por
un integrante seleccionado, con `P7_3` válida en {01,02,04,05,06}, cuyo medio
fue internet o cajero/kiosco inteligente (`P7_3` en {04,05}). Escala de la
proporción y de su residuo descriptivo en logit; evidencia clase (a). El
universo no representa a quienes no realizaron trámites.

Comparabilidad documental, establecida antes de abrir las respuestas:

- ENCIG 2021, cuestionario general oficial, páginas impresas 15–16/PDF 15–16,
  sección VII: “Ahora le preguntaré por el último (TRÁMITE O PAGO) que usted
  realizó durante 2021” y P7.3 “¿A qué tipo de lugar acudió o a qué medio
  recurrió para realizar el trámite o pago?”. Códigos: 1 instalaciones de
  gobierno, 2 banco/comercio/farmacia, 3 teléfono, 4 internet, 5 cajero o
  kiosco, 6 módulos móviles, 7 no concluido, 8 otro, 9 no sabe/no responde.
- ENCIG 2023, cuestionario general oficial, sección VII, declara experiencias
  durante 2023 y la misma P7.3 con los mismos códigos. Los descriptores de
  ambas olas documentan `N_TRA=01` como pago ordinario de luz, `FAC_TRA` como
  factor de expansión de trámites, y `EST_DIS`/`UPM_DIS` como diseño.
- Los cuestionarios y descriptores documentan sexo 1/2, edad 01…96 (97 y
  98/99 no entran en 60–96) y `NIV` 00…09. Escolaridad es una agregación, no
  una categoría nativa: {00,01,02}, {03}, {04,05,06,07}, {08,09}.

Fuentes: `encig21_cuestionario.pdf` (sha256
`9ee829815e8dca5ebe562b26afb006dcec475840bf27a206a0b838534041e45a`),
`encig21_estructura_base_datos.pdf` (`365c031bf48af4c6d65a8e5422c6cf0362500efd37cd0e924e3c1fe38b965dd2`),
`encig23_cuestionario.pdf` (`65000ad38419da504e46b34a0a2426f218d1ba6e604ad37a14762bbd07881e1e`)
y `encig23_estructura_base_datos.pdf`
(`eb89820cd58af0d8799387a376b9e60b062ed59daea74cdbea7ff3b4ee13a906`).

## Rejillas, universo común y residuos

Orden canónico: sexo {1,2}; edad {18–29,30–44,45–59,60–96}; escolaridad
{hasta-primaria, secundaria, media-superior, superior}. Cruces completos:
sexo×edad, sexo×escolaridad y edad×escolaridad. No se colapsan celdas.

Para cada cruce, `p(a,b)`, `p(a)`, `p(b)` y `p` se calculan sobre el mismo
dominio de casos completos de sus dos ejes. Por separado se publican los
residuos de cada eje válido cuyo otro eje es desconocido. La reconstrucción
por numeradores y denominadores, nunca por promedio de tasas, debe reproducir
los marginales sellados de `CALC-PISOS-ENCIG2023-EJES-0002` con tolerancia
absoluta `1e-10`. Si la coincidencia requiere añadir residuos fuera de la
rejilla sustantiva, el cruce queda `PARO-COHERENCIA-UNIVERSO`; se conserva su
diagnóstico pero no se elige ganador mientras afecte la comparación completa.

## Estimación e incertidumbre

`δ = logit p(a,b) − logit p(a) − logit p(b) + logit p`.

Una única secuencia PCG64(20260919) produce 10 000 remuestras de UPM con
reposición dentro de estrato, compartidas por los cuatro términos, todas las
celdas y los tres cruces de cada ola. Una UPM singleton conserva multiplicidad
uno. Todos los trámites de una persona viajan juntos porque se comprueba que la
persona pertenece a una sola UPM; no hay segundo bootstrap de filas/personas.
El marco completo de UPM se conserva al estimar dominios.

EE es la desviación estándar muestral de réplicas; IC95, percentiles 2.5/97.5.
No hay clipping, pseudocuentas ni suavizado. Denominador cero o probabilidad
0/1 deja `δ` sin número. Si cualquier réplica de una cantidad degenera, se
informa cuántas fueron válidas y su precisión queda nula: no se presenta la
distribución restante como IC incondicional.

Por celda se publica n de trámites, personas distintas, personas con evento,
personas sin evento, solapamiento, numerador/denominador ponderados, p, EE e
IC95, δ, EE e IC95, réplicas válidas y causa.

## §2 del brief aprobado — verbatim

1. **Elegible:** el cruce donde **todas** sus celdas tienen `n₂₀₂₃ ≥ 200` trámites sin ponderar (regla de soporte de la casa, spec del piloto 2 §3.4). No se colapsan categorías para rescatar un cruce.
2. **Puntaje:** media sobre celdas de `|δ₂₃,ab| / EE(δ₂₃,ab)`, con `δ = logit p(a,b) − [logit p(a) + logit p(b) − logit p]`.
3. **Se elige** el elegible de mayor puntaje. Empate (diferencia < 10 % del mayor): gana el que tenga mayor concordancia de signo de δ entre 2021 y 2023 si 2021 resultó construible (§3.3); si no, el de menos celdas.
4. **Condición de no-piloto:** si en el cruce elegido **ninguna** celda tiene IC95 de δ₂₃ que excluya 0, el veredicto es `SIN-PODER-DE-FALSACION`: no hay piloto 3 en ENCIG, y eso es un resultado, no un fracaso.

La concordancia usa todas las celdas comparables, sin seleccionar las
significativas; signo cero es signo propio. Cobertura asimétrica no produce
ventaja. Ramas no resueltas por el texto aprobado —ninguno elegible, puntajes
degenerados, empate persistente entre rejillas de igual tamaño o concordancia
empatada— producen el token específico o `SELECCION-PENDIENTE-DE-REGLA`, no
una prioridad inventada. El resultado derivado enumera ambos CALC y sus sellos.

## Guardia y diagnóstico

Allowlist de payloads: exclusivamente `encig23_base_datos_csv` y
`encig2021_csv`, cada uno en su CALC. Los patrones `encig25`, `encig_2025` y
cualquier alias/año 2025 son prohibidos. El diagnóstico permitido después de
COMMIT-1 comprueba miembros esperados, columnas, llaves, cardinalidad m:1,
diseño y pertenencia persona–UPM; sí lee las variables declaradas 2021/2023 y
no calcula ni imprime p, δ, puntajes o selección por una vía distinta.

ENCIG 2025 permanece RESERVADA. Este cálculo no estima S½, Sλ, R ni emisiones.

