# GEN2-38 · investigación y adquisición · 2026-10-01

## Selección previa a filas

`python3 tools/adq_doctor.py --selecciona --maximo 5 --json` eligió, en orden,
`ENEM_2024`, `EQD-PANEL_2018` e `INEGI-MMP_2024`: último intento efectivo
2026-09-24, siete días. La salida completa vive en
`forense/adq-log/2026-09-30T230003-151798-seleccion.json`.

## Intentos de adquisición

### ENEM_2024

- Búsqueda web real: `ENEM 2024 Estudio Nacional Electoral México microdatos CIDE`.
- Resultado: no devolvió un payload del ENEM 2024. La página pública de datos
  de Kenneth Greene sí nombra otro objeto, `Mexico 2024 Panel Study`, sin
  enlace de datos; no se equipara con ENEM.
- Resultado verificable del intento: `HTTP 200; text/html; 72082 bytes; la página pública nombra Mexico 2024 Panel Study pero no expone enlace de payload para ENEM_2024`.
- Receta: abrir `https://cses.org/data-download/cses-module-6-2021-2026/`,
  revisar si el release incorporó México y, si no, abrir la página de datos
  del CIDE/ENEM; descargar el archivo que se identifique expresamente como
  ENEM 2024.

### EQD-PANEL_2018

- Búsqueda web real: `Greene Simpser Mexico 2018 panel survey data replication`.
- Resultado: `https://www.kenneth-greene.com/pages/8591` acredita identidad,
  PIs y existencia del `Mexico 2018 Panel Study`, pero la sección no contiene
  enlace de datos o documentación para 2018.
- Resultado verificable del intento: `HTTP 200; text/html; 72082 bytes; Mexico 2018 Panel Study aparece por nombre y PIs, sin href de datos o documentación`.
- Receta: abrir `https://www.kenneth-greene.com/pages/8591`, sección
  “Mexico 2018 Panel Study”; si el icono ofrece un enlace en navegador,
  descargar datos y documentación. Si sigue sin enlace, usar el contacto del
  autor; no automatizar ese contacto.

### INEGI-MMP_2024

- Búsqueda web real: `INEGI medición multidimensional pobreza 2024 programas de cálculo bases descarga`.
- `python3 tools/renderiza_pagina.py https://www.inegi.org.mx/desarrollosocial/pm/ --enlaces '\.(zip|csv|dta|sav|xlsx)$'` produjo exactamente:
  `{"url": "https://www.inegi.org.mx/desarrollosocial/pm/", "navegador": "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe", "fecha_utc": "2026-10-01T07:51:07Z", "estado": "RENDERIZADO", "titulo": "Pobreza Multidimensional (PM)", "bytes": 154038, "sha256": "8e02bc77bf1b0fa1773e080238550c01ab8ae5d95df67d7715125138f412c6fb", "archivo": "/tmp/mm-renderiza/0bcae6656ef3c977.html", "rc": 0, "enlaces": []}`.
- Resultado verificable del intento: `RENDERIZADO; titulo=Pobreza Multidimensional (PM); bytes=154038; enlaces=[]`.
- La búsqueda local sólo halló MMP 2016–2022 y el insumo ENIGH 2024; ninguno
  es el programa/base de cálculo MMP 2024 pedido.
- Receta: abrir `https://www.inegi.org.mx/desarrollosocial/pm/`, activar la
  pestaña de programas/bases y descargar el ZIP rotulado 2024; el tabulado
  `pm_ar_2024.xlsx` no sustituye el objeto.

## Investigación seleccionada

### DEM-AHORRO-STOCK-DURACION-01

- Modos: CONSTRUCTO, HERMANAS, LATERAL.
- Universo local verificado: `busca_reactivos.py --palabra ahorro --limite 20`
  revisó 240072 identidades y reportó 522 candidatas; la muestra vuelve a
  ENIF y no cambia el universo previo.
- Búsqueda web real: `México encuesta ahorro duración meses ahorros fondo emergencia cuestionario universidad`.
- Hallazgo: ENSAFI 2023 publica por separado preguntas de tenencia de ahorros
  y categorías de suficiencia en quincenas/meses. Es evidencia existente ya
  examinada, no una candidata nueva. La duración está expresada como meses de
  ingreso cubiertos y condicionada a quienes declararon ahorro; no acredita
  duración del mismo stock incluyendo ausencia en un campo separado para el
  uso original.
- Alternativa concreta tras más de dos ciclos: mesa puede mantener el bloqueo,
  relabelar el uso acotado de #772 o aprobar explícitamente ENSAFI como proxy
  de cobertura del ingreso, nunca como horizonte puro.
- Frontera siguiente: catálogos variable-por-variable de encuestas financieras
  de universidades estatales distintas de IIEG y archivos históricos no
  indexados de CONDUSEF.

### NC-0170

- Modos: CONSTRUCTO, HERMANAS, LATERAL.
- Consulta externa real: `gh pr view 680`, `701`, `759`, `795`.
- Resultado: los cuatro PR son `MERGED`; #759 y #795 acreditan los retro-sellos
  ya ejecutados. No queda una fuente pública de datos: queda únicamente la
  decisión humana sobre si `[COLA]/[ADQ]` es cuarta categoría exenta.
- Evento de reactivación: firma de mesa de esa decisión. No se repiten los
  retro-sellos ejecutados o reasentados.

### NC-0246

- Modos: CONSTRUCTO, HERMANAS, LATERAL.
- Consultas externas reales por GitHub API: `P3_27_AG`, `CORR-0013` y
  `mociba2015` en `repo:Josanoforo/Modelado-Mexicano`.
- Resultado para cada consulta: `total_count=0`,
  `incomplete_results=true`, sin items. No es un negativo global: confirma
  que no apareció un objeto público nuevo por esa vía.
- Evento de reactivación: asignación del acto MEDICION-DEMANDA para CORR-0013
  o del acto F6-PANEL-CAJA-1/sucesor para MOCIBA. La firma de mesa ya decide el
  destino; esta clasificación no toma otra decisión científica.

## PAQUETE-RECETAS-2026-10-01

Las tres recetas de las secciones ENEM_2024, EQD-PANEL_2018 e
INEGI-MMP_2024 forman el único bloque del día para las filas cerradas en
`NO-OBTENIDO-POR-ESTE-AGENTE`.
