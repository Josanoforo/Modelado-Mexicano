# REGION · ENVIPE 2024 · spec humana v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

## Decisiones de mesa y alcance

R1 aprobada en la sesión de 23/sep/2026: entidades donde diseño y estimando lo admiten, más regiones oficiales del instrumento; no se crean macroregiones. Para ENVIPE 2024 se estiman las 32 entidades del universo de la encuesta. R2 aprobada en la misma sesión: punto e IC solo si el denominador no ponderado tiene n ≥ 200, varianza de diseño estimable y se satisfacen requisitos oficiales más estrictos si los hubiera. `n=200` es un piso operativo, no una promesa de precisión.

Esta pieza inicial mide `tramite.evasion_norma` / `evade_norma_envipe2025` en la ola histórica 2024, con la misma variable y unidad de la spec `ENVIPE-EVASION-NORMA-spec-v1_0.md`. El universo regional completo de conductas del encargo U5 requiere piezas adicionales; esta spec no cierra ese universo por sí sola.

## Fuente, unidad y geografía

`envipe2024_csv` del manifiesto, miembro `conjunto_de_datos_tmod_vic_envipe2024.csv`. Unidad: delito. Denominador: `BP1_20∈{1,2}`; numerador: `BP1_20=2` y `BP1_23∈{04,05,06,08}` (pérdida de tiempo, trámite largo, desconfianza, actitud hostil). `FAC_DEL` es el factor; `EST_DIS` el estrato; `(EST_DIS, UPM_DIS)` identifica conglomerados. La geografía es `CVE_ENT` de `tsdem`, enlazada por `ID_PER` única, y representa residencia de la víctima. No se interpreta como lugar del delito. No se usa la clave implícita en `ID_DEL` como sustituto de `CVE_ENT`. Fuente de columnas y llave: `fd_envipe2024.pdf`, tablas TSDem y TMod_Vic; codificación del desenlace: `ENVIPE-EVASION-NORMA-spec-v1_0.md`.

## Estimador y regla de publicación

Por entidad g, p_g = Σ FAC_DEL·1(D,g)·Y / Σ FAC_DEL·1(D,g). Se forman 1 000 réplicas compartidas en la ola completa con UPM con reposición dentro de estratos, `numpy.PCG64(20260923)`, usando por hash `tools/celda_d/marginales_reproduccion.py::replicas_compartidas` (`4df2c630179c194345594d959d012b7dd18d94ac93fab3f48b8f6683753dafd6`). Adaptador: `ID_DEL` sintético secuencial solo para la guarda de interfaz; `EST_DIS`, `UPM_DIS` y `_w` conservan su significado de diseño; `_y` de interfaz no se usa para el estimando. El dominio se estima mediante totales de UPM de la ola completa. IC95: percentiles 2.5 y 97.5 de las 1 000 razones. Si una réplica pierde todo el denominador, hay menos de dos UPM de dominio, o la dispersión es cero, estado `VARIANZA-NO-ESTIMABLE`; no se publica punto ni IC. Estratos de una UPM permanecen constantes en cada réplica y se cuentan; ninguna UPM única genera incertidumbre artificial. Si n<200, `SUPRIMIDA-N`. Códigos fuera del denominador no son ceros. Se conserva una fila por entidad con estado y n aun cuando se suprima.

`n_efectivo_kish=(Σw)^2/Σw²` describe dispersión de pesos, no sustituye grados de libertad de diseño. No hay recorte posresultado de precisión. No se combinan olas ni se calibra persistencia en este CALC. Etiqueta temporal: RETROSPECTIVA. `adopta: NO`.

## Auditoría de rigor extremo

La entidad es residencia de la víctima: no evidencia de cultura, lugar del delito ni preferencia. La unidad delito puede repetir hogar/persona; la réplica agrupa por UPM. El marco no identifica población indígena ni clase y no prueba mecanismos psicológicos. La ola 2024 ya se observó: cualquier contraste posterior será RETROSPECTIVA. Un patrón fuerte cambiaría ante una replicación comparable con la misma unidad, cobertura y precisión.
