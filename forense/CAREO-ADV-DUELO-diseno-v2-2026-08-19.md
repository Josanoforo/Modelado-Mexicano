# CAREO · ADV-DUELO — cuatro corridas + deep search, adjudicadas — y el DISEÑO v2 que sustituye al §5
**Dirección, 19/ago/2026. Insumos: ADV-1 ×2 (Opus/Fable), ADV-2 ×2, deep search compass-5. Este documento sustituye el §5 de APERTURA-FASE-CALCULO y se sella junto con ella como v1.2 (acto §T-SELLO, que además committea los cinco informes a `forense/adv-duelo/`).**

> **Nota de aterrizaje (20/ago/2026 · `ACTO SELLA-ADV` T1, fuera del alcance formal de "los cuatro" de la compuerta):** careo de dirección del 19/ago/2026 sobre los cinco insumos adversariales (`ADV-1 ×2`, `ADV-2 ×2`, deep search compass-5), recibido junto con los cuatro documentos de la compuerta de arranque. El paquete de lanzamiento no le asignó sha256 propio — se archiva porque es la fuente verbatim de los mecanismos `ADV1-M1`…`ADV1-M6` que `D-4` sella (ver el ADR de este acto) y de las decisiones `D-i`…`D-iv` que anteceden a las `D-1`…`D-6` de mesa. sha256 del adjunto tal como se recibió (declarado aquí por primera vez, sin hash previo contra el cual verificar): `a4d2b7322a6aa16831e8ec2e147634eccb55a7f7e7bd5f86acca85181778ac83`. Archivado verbatim, sin edición de cuerpo.

## §A · Matriz de convergencia y adjudicación
| Hallazgo | Corridas | Veredicto CAREO | Vive en |
|---|---|---|---|
| Contaminación de L (memorización de tabulados) | **5/5** | INCORPORADO | M1 filtros + sondas |
| Circularidad de M (parametrizado sobre la familia de R) | **5/5** | INCORPORADO | M1 grados P0/P1/P2 |
| No-independencia L↔R de 2.º orden | 4/5 | INCORPORADO | M1 filtro de discriminación |
| Scoring impropio · árbitro sin incertidumbre · sin calibración | **5/5** | INCORPORADO | M3 |
| Baseline B obligatorio | **5/5** | INCORPORADO | Corredor B |
| "≥X de N" sin poder (falso ganador ≈77% bajo H0 con N=12) | **5/5** | INCORPORADO — v1 pasa a **piloto sin veredicto** | M4 |
| Redactor de L conoce el motor · varianza LLM | **5/5** | INCORPORADO | M2 tubería ciega |
| Set elegido por el dueño de M | **5/5** | INCORPORADO | M1 marco+sorteo |
| Tabla de consecuencias con "ambos lejos de R" | **5/5** | INCORPORADO | M5, cinco casillas |
| Gates del GO de proceso → de resultado | 4/5 | INCORPORADO (3 de 7) | M6 |
| Ensemble E = L⊕M como corredor | 3/5 | INCORPORADO (costo ≈0; responde la pregunta del híbrido) | Corredor E |
| Techo de predictibilidad ex ante (FFC; Park normaliza vs test-retest) | 3/5 | INCORPORADO | M4 |
| Marcador distribucional anti-aplanamiento (Bisbee: varianza sub-representada, ~48% coef. difieren) | 2/5 | INCORPORADO como secundario | M3-bis |
| Dos variantes de L (con/sin corpus tierizado) | 1/5 | INCORPORADO — columna extra de la tubería, "vale casi tanto como el duelo" | M2 |
| Sonda placebo (indicador inexistente) · frase de discriminación por pregunta · prohibir "supera" en el piloto | 2-3/5 | INCORPORADOS (costo ≈0) | M1/M4 |
| Regla semanal anti-Goodhart (admisibilidad; descarte documentado = producción plena) | 4/5 | INCORPORADO | Regla de fase |
| Barrido complementario del corpus (etiqueta-cita + k=5 aserciones/report con semilla + prioridad por carga) | 3/5 | ACEPTADO **en paralelo** — programa propio, no bloquea el duelo | BARRIDO-CORPUS-MUESTREO |
| ODD/TRACE formal · corredor humano H · multiplicidad fina (Holm) sobre rebanadas | 1-2/5 | **DIFERIDOS a v2.1 con razón**: no cierran una vía de ganador falso; las rebanadas quedan exploratorias | — |
| Auditor externo del set | 2/5 | SUSTITUIDO en piloto por marco pre-registrado + sorteo con semilla pública; el límite se declara | M1 |

**Los números que gobiernan este careo:** con N=12 y "≥7", *alguien* gana ~77% de las veces bajo igualdad perfecta (ambas demoliciones lo calcularon por separado, mismo número) · la rúbrica top-tier calificó el diseño v1 en **6/24** · el veredicto real exige **N≈35-70** según el efecto · el FFC fija la expectativa: en este dominio, hasta los mejores apenas superan un baseline simple — "ambos lejos de R" no es anomalía, es el desenlace más probable · Hewitt et al. 2024 (r=0.90 en estudios *no publicados*) prueba que el control de contaminación por construcción funciona · **NO EXISTE un duelo publicado LLM-vs-ABM con árbitro de microdato oficial mexicano — seríamos el primero, razón para que el aparato sea impecable.**

## §B · DISEÑO v2 — Comparación pre-registrada (sustituye "duelo")
**Corredores: cuatro.** **L** (LLM, en dos variantes etiquetadas: L-solo y L+corpus) · **M** (motor, cada celda con su grado de dependencia visible) · **B** (baseline tonto obligatorio: tasa base de la última ola pública o persistencia) · **E** (combinación mecánica L⊕M pre-registrada, por script).

**M1 · El marco antes que las celdas.** 40–60 preguntas candidatas construidas ANTES de saber qué celdas están listas, cada una como spec ejecutable (encuesta, ola, universo, variable, estimador, ponderador, escala). Filtros de admisión, todos verificables: **(i) no-publicada** — prueba del bibliotecario 15 min; máximo 20% publicadas y esas van a "control de memoria", fuera del marcador; **(ii) grado de dependencia respecto de R** — P0 (misma encuesta+ola que parametrizó M) fuera del marcador, a anexo de plomería; P1 (misma familia, otra ola) puntúa aparte; P2 (fuente distinta o desenlace documentado) peso pleno; **cuota: ≥1/3 del set en P2, con ≥2 desenlaces documentados no-encuesta**; **(iii) árbitro decidible** — CV de R bajo el umbral de la semaforización INEGI (acuerdo CAC-007/01/2018) y piso de n no ponderado; **(iv) frase de discriminación** pre-registrada (por qué L y M podrían divergir); **(v) ≥3-5 celdas post-corte u ola-retenida** (parametrizar con la ola vieja, arbitrar con la nueva, simétrico para L y M). Sondas transversales: **perturbación** (reformular universo/escala en margen que cambia el valor real — la memoria no se mueve, el modelado sí), **canario** (pedir a L la cifra textual y su fuente), **placebo** (un indicador plausible inexistente). Estratificación dominio × grado × dificultad, con cuota de condicionales/subgrupo — el motor existe para heterogeneidad, un duelo de promedios nacionales no toca su razón de ser. **Sorteo con semilla pública** dentro de estratos; piloto = las primeras 12–15 del orden sorteado; lo no producido se registra SKIP con motivo.

**M2 · Elicitación mecánica y ciega.** Un script toma la spec y produce las respuestas sin humano en el bucle: L con modelo+versión+fecha+temperatura fijados, **k=5–10 corridas**, agregado pre-registrado (mediana+cuantiles; self-consistency en categóricas), TODAS las corridas registradas sin descarte, dispersión reportada; las sesiones L las corre **alguien/algo ajeno a las celdas de M** (sesiones limpias, como estas adversariales); dos variantes L-solo / L+corpus. M emite punto e intervalo de su incertidumbre de parámetros. Hashes de los cuatro corredores comprometidos **antes de que R exista**.

**M3 · Scoring propio con el árbitro incierto adentro.** Por celda: **skill = 1 − error/error(B)**; CRPS/interval-score en continuas, Brier en categóricas, evaluado contra **R como distribución** (Normal(R̂, EE) o su IC), nunca contra el punto. **INDECIDIBLE** si ambos caen dentro del IC de R o si |d_L−d_M| < 0.5·EE(R). Calibración (cobertura empírica de intervalos al 80%) reportada como resultado independiente. **M3-bis, secundario:** donde R es microdato, distancia de forma (KS/Wasserstein), razón de varianzas como alarma de aplanamiento, y ≥1 corte por subgrupo mexicano por celda.

**M4 · El piloto no declara ganador.** Pre-registrado y firmado: productos del piloto = (i) diferencia media de skill L−M con IC por permutación, (ii) calibración por corredor, (iii) conteo de INDECIDIBLES y SKIPS publicado al mismo tamaño que el marcador, (iv) **el N requerido para v2** (≈20 para 80/20; ≈35-40 para 70/30; ≈65-70 para 65/35), (v) techo de predictibilidad por celda declarado ex ante (qué explica el predictor trivial). **Prohibida la palabra "supera" en toda comunicación del piloto.**

**M5 · Tabla de consecuencias, cinco casillas, firmada antes de la primera celda.** (1) L más cerca → "en estos momentos el canal LLM quedó más cerca del dato"; NO licencia "el motor sobra" (procedencia, contrafactuales e interpretabilidad no se puntuaron). (2) M más cerca → "el motor transportó mejor que la memoria del LLM"; NO licencia "M es bueno" salvo skill material sobre B. (3) Empate-TOST dentro de banda pre-declarada. (4) **Ninguno supera a B** → ninguno utilizable v1; re-tierización dirigida sin coronación. (5) **Ambos fuera del IC de R en la mayoría** → el fenómeno no es predecible con estas herramientas hoy; consecuencia propia, y es la casilla que el FFC dice esperar. Cláusula de alcance: ningún resultado autoriza abandonar L ni M para usos no muestreados — el duelo mide estimación de cantidades encuestables y nada más.

**M6 · GO con dientes.** De los 7 umbrales, **≥3 de resultado**: cuotas de M1 cumplidas por comando (P2, CV, sondas corridas) · cobertura de intervalos de M ≥60% de celdas puntuadas · M>B en ≥2/3 de celdas puntuadas. Al menos un umbral lo determina la naturaleza, no el equipo.

**Regla de fase, enmendada:** cada semana produce una celda **admisible** o una fila del marcador — un descarte con causa documentada cuenta como producción plena; "nada y se dice" es métrica de salud, no de falla.

**En paralelo, programa propio (no bloquea):** BARRIDO-CORPUS-MUESTREO — coherencia etiqueta-cita en los ~30 reports (~20 min c/u) + k=5 aserciones al azar por report con semilla pública (tasa de error estimada publicable, re-auditoría completa solo si dispara umbral) + prioridad a nodos que sostienen parámetros del motor.

**Fuera de v2, a propósito:** ODD/TRACE formal, corredor humano H, corrección de multiplicidad fina — ninguno cierra una vía de ganador falso; v2.1.

## §C · Decisiones de mesa (sustituyen a las tres anteriores)
**D-i** · Firma por escrito el estatus **PILOTO SIN VEREDICTO** de v1 (la condición que ambas demoliciones ponen para que todo lo demás sea defendible). **D-ii** · Firma la **tabla de cinco casillas de M5 antes de la primera celda** — "incluso un piloto imperfecto es seguro si su peor resultado deja de ser pivote estratégico y pasa a ser dato". **D-iii** · Autoriza el marco de 40–60 candidatas y el sorteo con semilla pública, y designa quién corre la tubería L (propuesta: sesiones limpias fuera del proyecto, mismo patrón que estas adversariales). **D-iv** · La banda TOST y el margen material NO se firman ahora: el acto de pre-registro los deriva de los EE reales del set y te trae el número con su justificación (firmar una constante a ciegas sería el defecto v2.1 de siempre).

## §D · Acto sucesor
**DUELO-PREREG-V2** (nube, Opus, tras el §T-SELLO): committea este careo + los cinco informes a `forense/adv-duelo/` · escribe el pre-registro ejecutable (marco de candidatas como specs, script de tubería L, script de scoring, tabla M5 con las firmas D-i/D-ii citadas verbatim) · abre las filas que toque con máximo id derivado. Costo total estimado del v2 sobre v1 (convergente entre corridas): **12–15 sesiones**, de las cuales ~6 son escritura/scripts y el resto es regenerar el set bajo el criterio de admisión — "ese es el precio honesto de que el duelo signifique algo".
