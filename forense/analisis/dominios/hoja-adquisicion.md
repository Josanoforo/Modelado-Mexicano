# ASTRA5-U0 · Hoja de adquisición documental (corte 2026-09-23)

La decisión activa es **DOCUMENTACIÓN-SOLAMENTE** para el diseño de ENOE N. No se solicita ningún microdato ni una encuesta completa. Los otros documentos son piezas exactas identificadas para los cortes siguientes; su adquisición queda en cola hasta revisar sus afirmaciones y permisos.

| Familia / consumidor | Estado | Pieza exacta | Fuente primaria y condición | Reserva / razón | Prioridad y operación |
|---|---|---|---|---|---|
| ENOE 2024 T3 / ASTRA5-U1, filas ENOE-001 a 003 | DOCUMENTACIÓN-SOLAMENTE | `enoe_n_diseno_muestral.pdf`, SHA256 físico `42eaa300fcbd4bec98c2a38f3edb5912bcc2208fe69a54a0c1103b75a85dbd09` | [INEGI, diseño muestral ENOE N](https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/doc/enoe_n_diseno_muestral.pdf), PDF público leído; condiciones de reutilización: comprobar al registrarlo | El PDF no tiene id en `data/manifiesto.yaml`; datos 2024 T3, cuestionario v7 y FD 2024 sí están registrados y sus hashes físicos coinciden. Ola ENOE más reciente reservada. | 1: registrar únicamente este PDF documental en manifiesto por el flujo de adquisición vigente; no descargar microdato. |
| MOCIBA 2021 / ASTRA5-U4 | REUTILIZAR | `mociba2021_cuestionario.pdf`, id `mociba_2021_cuestionario_pdf`; `mociba2021_fd.xlsx`, id `mociba_2021_mociba2021_fd`; datos `mociba_2021_mociba2021_bd_csv` | Cuestionario primario INEGI ya en repo; FD y datos en manifiesto | Verificar permiso de ola antes de cualquier apertura de microdato; el cuestionario ya expone P12 y sus respuestas. | 2: lectura documental y cruce de texto/códigos por U4. |
| ENDUTIH 2024 / ASTRA5-U4 | DOCUMENTACIÓN-SOLAMENTE, EN COLA | `CENDUTIH2024.pdf`, cuestionario específico | [INEGI, cuestionario ENDUTIH 2024](https://www.inegi.org.mx/contenidos/programas/endutih/2024/doc/CENDUTIH2024.pdf); licencia/condición por leer al registro | Datos y FD 2024 ya tienen ids `endutih2024_bd_dbf_zip` y `endutih2024_fd_xlsx`; falta comprobar cuestionario en manifiesto. | 2: verificar texto para uso, banca, trámites y no uso; después registrar solo documento necesario. |
| ENDIREH 2021 / ASTRA5-U2 | DOCUMENTACIÓN-SOLAMENTE, EN COLA | `endireh2021_cuestionario_general.pdf`, `_a.pdf`, `_b.pdf`, `_c.pdf` | [INEGI, materiales ENDIREH 2021](https://www.inegi.org.mx/rnm/index.php/catalog/801/related-materials); licencia/condición por leer al registro | Datos y FD en manifiesto; cuestionarios cambian con situación conyugal. No cerrar medición para violencia/denuncia antes de revisar los cuatro universos. | 3: leer cuestionarios por afirmación y registrar solo las piezas usadas. |
| ENSANUT, ENBIARE, ENADIS, LAPOP, WVS/Latinobarómetro / cola de mesa | REUTILIZAR | Entradas de manifiesto existentes, respectivas por id; no pedir encuesta entera | Inventario local de `data/manifiesto.yaml`, 2026-09-23 | Disponibilidad y permiso específicos por ola pendientes de cotejar con afirmación concreta. | 4: seleccionar reactivo y archivo exacto tras revisión por afirmación. |

**PEW** requiere distinguir el topline público, microdato mexicano, cobertura de la muestra y permiso de uso. Sus nueve entradas de manifiesto son archivos, no nueve muestras ni autorización de apertura.

**Conteos de arranque rederivados por id/archivo/alias en el manifiesto (no muestras únicas):** ENOE 93, MOCIBA 50, ENDUTIH 6, ENDIREH 41, ENSANUT 149, ENBIARE 2, ENADIS 4, LAPOP 10, WVS 10, Latinobarómetro 3. Ningún conteo implica medibilidad de una afirmación.

## NO-CORRIDO / RESERVAS

No se abrió microdato. No se consultó la ola ENOE más reciente. No se leyó cuestionario de ola reservada MOCIBA 2024/2025. Las piezas de cola esperan verificación de reactivo, universo y permiso; no se dictaminan por ausencia de archivo.
