# Calendario ENIF · ASTRA6-C2-ENIF-1

**EJECUTADO · consulta 26/sep/2026 · corte de trabajo `2c646cba93eebc9189a8135a5369bb45e8d29b89`.** Consulta limitada a calendarios y fichas del instrumento; ninguna descarga de microdatos, tabulados ni resultados de ola reservada.

La consulta nueva sí encontró el [calendario oficial del primer semestre de 2027](https://www.inegi.org.mx/contenidos/saladeprensa/doc/cal_2027.pdf), de 15 páginas. Corrige la premisa temporal de la consulta archivada del 23/sep: no se afirma ahora que falte todo calendario 2027. No contiene una entrada de la Encuesta Nacional de Inclusión Financiera. `ENIFARM` es Industria Farmacéutica y no es ENIF. La ausencia en un calendario semestral no prueba cancelación ni ausencia en el segundo semestre.

| Objeto | Fuente oficial consultada | Resultado y alcance |
|---|---|---|
| Calendario 2027 | [PDF INEGI, primer semestre](https://www.inegi.org.mx/contenidos/saladeprensa/doc/cal_2027.pdf) | Disponible; sin entrada ENIF ni fecha de publicación del instrumento. SHA-256 descargado: `320a481cdb1c00cebd78ea1507074a462344206da5f9757819cb1622e5684968`. |
| Calendario 2026 | [PDF INEGI 2026](https://www.inegi.org.mx/contenidos/saladeprensa/doc/cal_2026.pdf) | Consultado; no confirma publicación de una ola ENIF futura. |
| Ficha histórica | [ENIF 2024](https://www.inegi.org.mx/programas/enif/2024/) | Landing consultada; el lector web no extrajo texto. No se deriva fecha futura de esta ficha. |
| Ficha objetivo | [Ruta ENIF 2027](https://www.inegi.org.mx/programas/enif/2027/) | El lector devolvió error interno; no acredita ficha inexistente. |
| Búsqueda nueva | Consultas `site.inegi.org.mx ENIF 2027 calendario difusión` y `site.inegi.org.mx calendario difusión 2027 ENIF` | Devolvieron calendarios y sala de prensa, sin anuncio ENIF identificable; búsqueda negativa de alcance limitado. |

El PDF se descargó con `curl -fLsS`, se leyó con `pdftotext -layout` y se buscó el nombre completo del instrumento; su hash identifica los bytes consultados, no una atestación externa. El PDF permanece como descarga de consulta fuera del árbol; no se modifica el calendario global ni se duplica su archivo histórico.

| Familia | Ola objetivo | Referencia | Levantamiento | Publicación | Estado |
|---|---|---|---|---|---|
| ENIF-AHORRO-FORMAL | ENIF futura comparable, etiqueta provisional `enif_2027` | NO-CONFIRMADA | NO-CONFIRMADO | NO-CONFIRMADA | CONDICIONAL |
| ENIF-HORIZONTE-AHORRO | La misma ola y apertura | NO-CONFIRMADA | NO-CONFIRMADO | NO-CONFIRMADA | CONDICIONAL |

**PROPUESTO-POR-EJECUTOR:** mantener la ventana de seguimiento heredada, 23/sep/2026–23/mar/2028. Es ventana operativa del proyecto, no ventana de publicación anunciada por INEGI. No hay evidencia suficiente para inventar mes o día esperado. “2027” sigue siendo etiqueta de planificación, no año oficial confirmado de referencia, levantamiento o publicación.

Antes de COMMIT-3, el circuito de adquisición identifica la edición efectivamente publicada y documenta por separado referencia, levantamiento y publicación. Ambas familias comparten una sola apertura autorizada y dependen de la misma muestra; no representan dos olas ni dos oportunidades independientes de consultar R. Una edición intermedia exige dictamen de identidad/comparabilidad antes de cambiar la etiqueta objetivo. La falta de anuncio no bloquea código, oro histórico o emisiones internas; mantiene condicionada la activación futura.
