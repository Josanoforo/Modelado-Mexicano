# BORRADOR — error de persistencia de formalidad ENIF

Estado: **NO CONGELADO; NO EJECUTAR CON DATOS**. La mesa eligió **B: persona
18–70** el 22/sep/2026. Se leyó íntegra la misión Astra 3. Este texto documenta
solo la preparación autorizada por `03-U3-ENIF-FORMALIDAD-ERROR.md`. Los nuevos
inputs 2021/2024 requieren un encargo ampliado de medición antes del freeze.

## Identidades e insumos

Seis identidades: `ahorra_solo_informal`, `informal_cualquiera` y
`horizonte_corto` por `con seguridad social` / `sin seguridad social`.
La tabla de identidad procede del metadato del piso
`PISOS-ENIF2021-formalidad-metadatos-v1_0.tsv` (SHA256
`8cf59f8ba487ac350173bb7c80ef6d6ed1918ebb6df2b50dea6df6c18ffc5d0f`).
El piso sellado 2021 es `CALC-PISOS-ENIF2021-FORMALIDAD-0001/resultados.json`
(SHA256 `2b5f1274f3b700900e40366e333cff1a820b6db7aaded0a68a0b81ac95e6e4ff`).
El árbitro 2024 es `CALC-ARBITRO-MARGINALES-ENIF2024-0001/resultados.json`
(SHA256 `552aef42c92cc70ded24bebb4c3e295739b95b346644e624cd22c8392916ecc4`).
Ambos contratos describen persona elegida 18+ en formalidad y desenlace definido.
Los cuatro RESULT del árbitro cubren D9 e informal_cualquiera por formalidad.
No declaran dos RESULT `horizonte_corto × formalidad`; esas llaves quedan
sin objetivo en la tabla de referencia 18+, sin sustituirlas por YAML legado.
La tabla `identidad-referencia-18plus.tsv` reconstruye las seis identidades
originales, pero **no es entrada ejecutable** bajo la decisión B. Los dos
RESULT sellados citados arriba son 18+ y tampoco son entradas numéricas para B.
El CALC de crédito 2021 con recorte 18–70 tiene otros desenlaces, aunque cita
el metadato de formalidad; no sustituye estas seis estimaciones.

## Procedimiento propuesto

Para cada llave exacta, verificar hashes, universo, P e IC95 de ambos lados.
Si falta un lado o falla compatibilidad, emitir `NO-COMPARABLE` y causa, con
diferencia e IC nulos. Si son comparables, aplicar el procedimiento de
`CALC-PISO-PERSISTENCIA-ERROR-0001`: `d_pp = 100(R − piso)`;
`se_R = (HI_R − LO_R)/(2 × 1.959964)` y análogo para piso;
`IC95(d) = d_pp ± 100 × 1.959964 × sqrt(se_R² + se_piso²)`.
Se supone independencia entre olas y se aproxima un IC posiblemente asimétrico
por una normal simétrica. El IC resultante no es bootstrap directo de la resta.
`PERSISTE` significa únicamente que ese IC incluye cero; en otro caso, `CAMBIA`.
No es prueba de equivalencia ni prueba de que la diferencia verdadera sea cero.

Para B se requieren seis pisos ENIF2021 18–70 y seis R ENIF2024 18–70,
con P e IC de cada lado, definidos y congelados antes de abrir microdatos.
La autorización de esos nuevos insumos/perímetro está pendiente. El error
18–70 sería un producto distinto: por sí solo no mide el error de las seis
celdas originales 18+ ni permite cerrar NC-0414/0431.

## Estado de exposición

EJECUTADO/LEÍDO: metadatos, misión íntegra, specs y esquema del procedimiento
heredado.
No se abrieron valores de `resultados.json`; sus hashes se calcularon sobre
bytes sin tabular. No se emitió diferencia ni clasificación real. Antes de
cualquier lectura cuantitativa debe cerrarse este prerregistro con sidecar y
spec.yaml, medidor completo y commit de freeze. **El primer resultado que
produzca el procedimiento congelado es el que se reporta.**
