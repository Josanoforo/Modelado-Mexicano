**CONSUMIDO — `ADR-163`, `ACTO BIBLIOTECARIO-56`, 25/ago/2026. Resultado: los dos pasos corridos sobre las 56 filas del universo — 24 `SI` · 24 `NO` · 8 `PENDIENTE-FUERA-DE-INDICE`; la cuota (i) de `ADV1-M1` revienta medida (`28 de 60` = 46.7 % contra un tope de 20 %). Detalle: `forense/notas/2026-08-25-bibliotecario-56-cierre.md`.**

---

ENCARGO 1 · ACTO BIBLIOTECARIO-56 — la prueba pendiente del marco (FP-93)

*(Texto de dirección, 25/ago/2026, archivado verbatim conforme a `A.3`; su SHA de redacción es `21ab042`, el `origin/main` del momento en que se recibió.)*

ENTORNO: UBUNTU (índices + corpus) · Opus · Firma: FP-93 quedó como ejecución pendiente desde el 20/ago; el procedimiento de dos pasos ya está diseñado en la propia fila. · CONTADOR: cero — etiqueta filas del marco, no mide (v2.3). ARRANQUE: clon existente · SHA del momento · data/raw enlazada (vacío = PARO) · firma de entorno tres partes (A.2: sin_variable + sonda INEGI + ls data/raw/). EXISTENCIA (dirección): las 56 filas PENDIENTE-BIBLIOTECARIO viven en forense/marco-candidatas-piloto-v1_0.tsv (re-deriva el conteo — MARCO-SATURA no lo tocó, verificado en su cierre); el diseño de dos pasos está en el texto de FP-93 (léelo del tablero, no de memoria). TAREAS: (1) ejecuta los dos pasos sobre cada una de las 56 — paso 1 índices, paso 2 abrir el archivo y buscar la cifra adentro; veredicto por fila con vocabulario A.4 y conteo de archivos por negativo; (2) escribe el resultado en la columna que la propia fila del marco espera (deriva el nombre del TSV, no lo inventes); (3) FP-93 → FIRMADA+ejecutada; (4) nota 2026-08-25-bibliotecario-56.md con el resumen: cuántas pasan, cuántas caen, y qué le hace eso a las cuotas del marco. PERÍMETRO: forense/marco-candidatas-piloto-v1_0.tsv (solo esa columna) · tablero · gobernanza · estado · nota · encargo.

---

## Cómo se ejecutó, y las dos desviaciones declaradas

**1 · El rótulo «56 filas PENDIENTE-BIBLIOTECARIO» se re-derivó y no se sostiene; el número 56 sí.** El marco trae **50** celdas con esa etiqueta literal, desde el commit que lo creó (`89a76ed`) hasta hoy. El 56 reconcilia como `50 PENDIENTE-BIBLIOTECARIO + 6 NO por aserto estructural`, que es exactamente lo que `ACT-PIL-2` contó cuando escribió *«4 `SI`, 0 `NO` por búsqueda, 56 `PENDIENTE-BIBLIOTECARIO`»* (`forense/notas/2026-08-20-act-pil-2-marco.md:191`). El acto corrió sobre las **56** —el universo completo del filtro (i), `60 − 4 SI`— y reporta los dos números por separado. No es un `PARO`: la premisa del encargo apunta al conjunto correcto con el rótulo equivocado.

**2 · La nota se escribió como `2026-08-25-bibliotecario-56-cierre.md`, no con el nombre literal que pide el punto (4).** El nombre literal colisiona bajo `T02` con este mismo encargo archivado: la normalización del test (minúsculas, sin caracteres no alfanuméricos) manda los dos a `20260825bibliotecario56md`. El sufijo `-cierre` es la convención ya usada por el resto de las notas del repo y resuelve la autocolisión sin inventar nomenclatura nueva.

**3 · El punto (2) se resolvió derivando el nombre de la columna, no inventándolo,** como el encargo exige: `awk` sobre el TSV localiza `PENDIENTE-BIBLIOTECARIO` **sólo** en la columna 10, `publicada` — la misma que `ACT-PIL-2` declaró que llevaría la forma `SI|NO|PENDIENTE :: prueba :: resultado`, verificable con `cut -f10`. Es la única columna del marco que este acto tocó, verificado campo a campo.

**4 · El contador se respetó en cero.** No se movió Hito D (`18 de 27`), ni el duelo, ni condicionales, ni coeficientes; no se registró ningún payload en `data/manifiesto.yaml` pese a haber descargado 922 archivos publicados (viven en `scratchpad`, se leyeron y no se incorporaron).

**Lo que el encargo no previó y el acto entrega igual:** el diseño de `FP-93` no alcanza 8 de las 56 filas por construcción (los dos índices son 100 % `inegi.org.mx` y esas filas las publica Banxico/CNBV o BMV/HR Ratings) — `FP-134`; y la respuesta al punto (4) sobre las cuotas es que la de publicadas **se rompe por un factor de 2.3** y su arreglo es firma de mesa — `FP-133`.
