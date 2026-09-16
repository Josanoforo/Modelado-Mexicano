# GEN2-38 · recorrido descubrimiento → adquisición → suficiencia

Fecha: 2026-09-16. Entorno: CAJA/WSL2. `data/raw` resolvió a
`/home/pc0/mm-corpus/raw`; `https://www.inegi.org.mx/` respondió HTTP 200 desde
`200.23.8.5` antes de caminar filas. La selección canónica de adquisición dio
cero elegidos. Se ejecutaron, en el orden entregado, las tres investigaciones.

## DEM-AHORRO-STOCK-DURACION-01

Versión: `2026-09-15-stock-ausencia-y-duracion-separados-v1`.

Modos: CONSTRUCTO, HERMANAS, LATERAL. Búsquedas web reales nuevas:

- `site:condusef.gob.mx encuesta ahorro duración ahorros meses cuestionario México`
- `site:cnbv.gob.mx cuestionario ahorro cuánto tiempo cubrir gastos ahorros encuesta`
- `site:repositorio.unam.mx encuesta ahorro duración stock ahorros cuestionario México`

Los resultados volvieron a ENSAFI 2023 y materiales divulgativos de CONDUSEF,
familia declarada como ya examinada. El resultado pertinente separa tenencia de
ahorro y monto expresado en quincenas/meses de ingreso entre quienes ahorran,
pero no añade un instrumento distinto ni justifica repetir la descarga. Un test
autoadministrado de CONDUSEF pregunta por tiempo para sostener gastos si se pierde
el empleo y, separadamente, si se ahorra; no es encuesta probabilística ni mide
duración del mismo stock. No se creó candidata ni se tomó una decisión científica.

Estado: `continua`. Frontera: repositorios académicos estatales distintos de
UNAM/IIEG y archivos no indexados de cuestionarios CNBV/CONDUSEF. Cursor:
examinar una encuesta estatal con catálogo variable por variable; no repetir
ENIF, EACF, ENSAFI, Findex, ENFIH, IIEG ni el catálogo Banco Mundial. Tras más
de dos ciclos sin avance, la alternativa concreta permanece: presentar a mesa
el relabel acotado autorizado por #772, sin ejecutarlo aquí.

Suficiencia: identidad PARCIAL; concepto NO_ACREDITADA; población ACREDITADA;
selección/no respuesta ACREDITADA; unidad ACREDITADA; temporalidad PARCIAL;
diseño ACREDITADA; identificación NO_APLICA; uso INCOMPATIBLE; pregunta ABIERTA.

## NC-0202

Versión: `2026-09-15-ennvih-diseno-publico-v1`.

Modos: LATERAL, HERMANAS. Búsqueda web real:
`ENNViH MxFLS Berumen 2007 sample design PSU strata public documentation`.
El sitio oficial expone páginas de pesos de ENNViH-2/3 y el PDF
`calculation_weights_mxfls.pdf`. A.8 encontró que el mismo objeto ya estaba en
el manifiesto como `ennvih3_2009_factores_exp`; `tests/manifiesto.py --verifica`
confirmó 337947 bytes. La lectura acredita selección por región/estrato/UPM/USM,
ajuste por no respuesta, proyección, calibración y ponderadores transversales y
longitudinales. No entrega identificadores públicos ejecutables de UPM/estrato
ni réplicas. No se repitió la descarga.

Estado: `evidencia_existente`; la pregunta original sigue ABIERTA. Frontera:
tablas públicas de pesos ENNViH-2/3 y depósito ICPSR 118971, para comprobar si
algún archivo separado contiene variables de varianza. Cursor: inspeccionar
metadatos/columnas de pesos sin reabrir guías ni contactar; si sólo hay factores,
mantener la solicitud humana NC-0156.

Suficiencia: identidad ACREDITADA; concepto ACREDITADA; población ACREDITADA;
selección/no respuesta PARCIAL; unidad ACREDITADA; temporalidad ACREDITADA;
diseño PARCIAL; identificación NO_APLICA; uso INCOMPATIBLE; pregunta ABIERTA.

## NC-0162

Versión: `AUTO-NC-v1-32c70b700f7f`.

Modos: CONSTRUCTO, HERMANAS, LATERAL. Búsquedas web reales:

- `site:inegi.org.mx/programas/enpol/2016 microdatos descriptor archivos ENPOL 2016`
- `site:inegi.org.mx/programas/enaproce/2018 microdatos descriptor archivos`
- `site:inegi.org.mx/programas/encrige/2016 microdatos descriptor archivos`
- `site:inegi.org.mx/programas/enjuve microdatos 2010 cuestionario`

La búsqueda localizó el portal oficial y JSON-LD de ENPOL 2016 con descarga CSV
pública. Se creó el residual `ENPOL_2016_MICRODATOS_CSV` con autoridad
`AUTORIZADA-POR-ALCANCE:Jonas/2026-09-12/GEN2-38/ENPOL_2016_MICRODATOS_CSV`.
Dos descargas HTTP 200 produjeron 16801537 bytes idénticos, SHA-256
`a405ed7777b8f51d338347e6cef94c5daa05f00625b6cd1709ecd49d6ab06997`; `python3
-m zipfile -t` resultó OK. El payload quedó en
`data/raw/enpol2016/enpol_2016_csv.zip` y el manifiesto lo registró como
`enpol2016_bd_csv_zip`. La fila residual quedó `OBTENIDO-PARCIAL`.

Uso permitido: documentar y preparar la ola 2016 de la familia retenida
`R11-TRA-ENPOL-MORDIDA`. Brecha: falta FD 2016, confirmar el reactivo, universo,
codificación, ponderador y comparabilidad con 2021; una familia adicional no
completa las 6 piloto + 12 confirmatorias ni autoriza evaluar un M renovado.
No se abrió el microdato y no se adoptó científicamente la familia. La relación
queda pendiente: `NC-0162` no existe como `necesidad_id` en
`necesidad-objeto-modelo.tsv`, y forzar un alta inventaría la decisión de qué
objeto del modelo representa.

Estado: `candidata_publica`. Frontera: FD oficial ENPOL 2016 y las familias
retenidas R03/R06/R08 todavía sin material suficiente. Cursor: localizar el FD
2016 por API/JSON-LD o RNM, adquirirlo si es público y verificar sólo estructura;
no evaluar M hasta disponer del conjunto reservado requerido.

Suficiencia: identidad ACREDITADA; concepto PARCIAL; población ACREDITADA;
selección/no respuesta PARCIAL; unidad ACREDITADA; temporalidad PARCIAL; diseño
PARCIAL; identificación NO_APLICA; uso APTA_ALCANCE_MENOR; pregunta ABIERTA.
