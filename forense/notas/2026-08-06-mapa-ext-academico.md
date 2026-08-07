# RECONCILIA-ACADEMICO-1 · mapa académico consolidado

Fecha: 2026-08-06. Worktree: `/home/pc0/worktrees/mm-mapa-ext-academico-20260806-182642`. Rama: `mapa-ext-academico-20260806-182642`. HEAD: `f542c938a0dcf6d2fa119dbbf8544937ede40219`. Se trabajó sin búsquedas web nuevas y solo sobre evidencia ya revisada por PASADA-1, PASADA-2 y artefactos locales.

## Resultado

El mapa final conserva la unión deduplicada: **20 candidatas**, más tres búsquedas negativas necesarias. Hay 15 prioritarias y cinco secundarias. `origen` distingue `PASADA-1`, `PASADA-2` y `AMBAS`; `reconciliacion` y `decision` registran el resultado estable y la siguiente acción.

### Conservadas de PASADA-1

1. Banxico Competencias Financieras 2019-2024 — prioridad 6; documentación insuficiente; abrir documentación.
2. ISSP Social Networks 2017 México — prioridad 7; documentación insuficiente; abrir documentación.
3. ISSP Family 2012 México — prioridad 8; documentación insuficiente; abrir documentación.
4. CSES México 2018 — prioridad 9; complementaria; abrir documentación.
5. Mass Mobilization México — prioridad 10; complementaria; abrir documentación.
6. ENCOAP 2025 — prioridad 11; apareció en ambas pasadas y se deduplicó.
7. Global Preferences Survey México — prioridad 12; apareció en ambas pasadas y se deduplicó; requiere decisión de mesa por formulario/licencia.

### Conservadas de PASADA-2

Se conservan las 13 candidatas de la pasada: corrupción electoral 2009, Enterprise Survey 2006-2010, Compartamos, educación financiera, Educación Inicial, retornos al capital en León, polarización/estatus ITAM, sismo/confianza, empoderamiento parental, auditorías 2015, microseguro Compartamos, tutores móviles y base electoral municipal 1994-2019. Tutores móviles queda descartada para este ciclo por falta de correspondencia con una condición exacta; no se elimina del mapa.

## Duplicados y contradicciones

Los únicos duplicados entre pasadas son **ENCOAP** y **Global Preferences Survey**. Se consolidaron con origen `AMBAS`; no se duplicaron filas.

No apareció una contradicción material entre las dos pasadas. Sí se resolvieron cuatro sobreafirmaciones internas de PASADA-2:

- Compartamos no queda adjudicado a `sens_estatus`: “social status” es un dominio publicado, pero falta la variable exacta.
- Educación financiera no sustituye hoy `horizonte_temporal`: el pago diferido es tratamiento experimental, no un reactivo de actitud; falta además documentar la llave screener-seguimiento.
- Educación Inicial identifica efectos de un programa de cuidado, no `familismo_obligacion`: falta un ítem literal de deber u obligación.
- Enterprise Survey permite empresa-FE solo en el subconjunto realmente reentrevistado y únicamente después de confirmar comparabilidad de outcomes; no se describe como panel a los dos cortes completos.

## Cinco gates

### 1. Enterprise Survey 2006-2010

- México está incluido en ambas olas.
- La documentación ya revisada declara firmas reentrevistadas y muestra `idPANEL2006`, además de pesos de elegibilidad/atrición.
- La landing 2006 documenta 1,480 empresas; el archivo/diccionario 2010 documenta 293 registros de panel.
- Con al menos dos observaciones por identificador y outcomes comparables, empresa-FE es técnicamente estimable para ese subconjunto. Ambas condiciones deben comprobarse documentalmente antes de especificar la corrida.
- Decisión: `A · ABRIR-DOCUMENTACIÓN-AHORA`.

### 2. Compartamos RCT

- Población: 16,560 mujeres en Nogales, Agua Prieta, Caborca y alrededores, Sonora.
- Tratamiento: expansión/promoción de crédito grupal aleatorizada por comunidad/vecindario.
- Outcomes documentados: préstamos, actividad empresarial, ingreso, trabajo, gasto y bienestar; la publicación nombra un dominio de estatus social.
- Variable exacta de `sens_estatus`: **no documentada** en la evidencia conservada. No se infiere de gasto, consumo ni bienestar.
- Acceso: proyecto de replicación indexado en OpenICPSR; licencia por archivo no verificada y ningún archivo descargado.
- Resultado: degradado de satisfacción documental a `INDEXADO-NO-DESCARGADO` para el uso de estatus; conserva alto valor para crédito/bienestar.

### 3. Educación financiera 2011-2012

- Nombre estable: *Large-Scale Financial Education Program Impact Evaluation 2011-2012*; Banco Mundial, Bruhn, Lara Ibarra y McKenzie.
- Diseño: curso e incentivos aleatorios de pago inmediato/diferido, transporte y testimonial; seguimiento a seis meses.
- Outcomes: ahorro, tarjetas, préstamos, deuda, conocimiento, ingreso, gasto y activos.
- Reactivo exacto de horizonte temporal: **no documentado**. El incentivo diferido no equivale a medir una preferencia temporal.
- Misma muestra/llave: seguimiento de participantes declarado, pero no está confirmada la llave entre screener administrativo y follow-up.
- Acceso: catálogo/DDI público; condición final de descarga no verificada.
- Resultado: `DOCUMENTACIÓN-INSUFICIENTE`; puede calibrar adopción, no sustituir hoy el proxy temporal.

### 4. Experimento electoral 2009

- Geografía: 12 municipios en Jalisco, Morelos y Tabasco.
- Tratamiento: secciones asignadas a volantes con información de corrupción auditada, gasto, pobreza o control.
- Estimando: diferencia causal en participación electoral por asignación; la landing de J-PAL reporta **−1.3 puntos porcentuales** para turnout.
- Datos: J-PAL enlaza una descarga de 545 KB; no fue descargada. Falta abrir únicamente su índice/codebook para la llave de la encuesta posterior.
- Resultado: conserva `SATISFACE-UMBRAL-DOCUMENTAL` y prioridad 1.

### 5. Educación Inicial CIDE–Banco Mundial

- Tratamiento: programa comunitario de educación inicial; 64 localidades tratamiento y 62 control dentro de pares.
- Unidades: niños, cuidadores, hogares y promotores; tres olas 2012-2014.
- Medición: creencias y prácticas de crianza/cuidado. No está documentado un reactivo directo de obligación familiar.
- Desenlace: desarrollo físico, cognitivo, motor y socioemocional infantil.
- Acceso: PUF anonimizado y requisitos de cita publicados; no descargado.
- Resultado: material para cuidado y desarrollo infantil, pero degradado para `familismo_obligacion` hasta leer el instrumento.

## Quince prioridades finales

1. Corrupción electoral 2009.
2. Enterprise Survey 2006-2010.
3. Compartamos RCT.
4. Educación financiera 2011-2012.
5. Educación Inicial CIDE–Banco Mundial.
6. Banxico Competencias Financieras 2019-2024.
7. ISSP Social Networks 2017 México.
8. ISSP Family 2012 México.
9. CSES México 2018.
10. Mass Mobilization México.
11. ENCOAP 2025.
12. Global Preferences Survey México.
13. Retornos al capital en León.
14. Polarización/estatus ITAM.
15. Sismo 2017 y confianza política.

## Fuentes degradadas por documentación insuficiente

Compartamos (`sens_estatus`), educación financiera (`horizonte_temporal` y llave), Educación Inicial (`familismo_obligacion`), sismo/confianza (n final, balance y paquete), Banxico Competencias Financieras, ambos ISSP, empoderamiento parental y auditorías electorales 2015. La degradación limita la afirmación; no elimina la candidata.

## Decisiones A/B/C/D

- `A · ABRIR-DOCUMENTACIÓN-AHORA`: 12 prioridades documentales, sin abrir microdatos.
- `B · MANTENER-EN-ESPERA`: sismo/confianza y cuatro secundarias con menor rendimiento inmediato.
- `C · DESCARTAR-PARA-ESTE-CICLO`: tutores móviles y tres búsquedas negativas cerradas.
- `D · REQUIERE-DECISIÓN-DE-MESA`: Global Preferences Survey, porque el acceso exige formulario de contacto y aceptación de licencia CC BY-NC-SA 4.0.

## Reservas

PASADA-1 llegó a este encargo como lista adjudicada de candidatas, pero sus URLs y fichas completas no están incorporadas en las tres salidas previas de este worktree. Por eso Banxico/ISSP/CSES/Mass Mobilization se conservan sin inventar metadatos faltantes y se marcan para consolidación documental desde los artefactos ya revisados, no mediante nueva búsqueda.

No se descargaron microdatos, no se aceptaron licencias, no se ejecutaron mediciones y no se modificó ningún archivo fuera de las tres salidas autorizadas. No se hizo commit ni push.
