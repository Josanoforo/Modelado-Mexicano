# PAQUETE DE RECETAS 3 — MAESTRA37-A2 (7 filas BAJAR)

Cada receta es ≤1 min de trabajo manual en navegador (regla `.claude/commands/adquiere.md`, ADR-261). Detalle completo por fila en `forense/notas/2026-09-04-MAESTRA37-A2-revision-cola.md`.

## 1 · PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND (fila `:39`)
1. Abrir en navegador: `https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2474620`
2. Si Cloudflare presenta un reto, resolverlo (un navegador humano normalmente pasa; el bloqueo detectado por el agente fue `cf-mitigated:challenge`, no un 403 real del origen).
3. Descargar el PDF del paper "Price and Information Type in Microinsurance Demand: Experimental Evidence from Mexico" (Bauchet, 2014).
4. Alternativa si SSRN sigue bloqueando: `https://cenfri.org/research-paper/price-and-information-type-in-life-microinsurance-demand-experimental-evidence-from-mexico/`.

## 2 · EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6 / CompraNet (fila `:63`)
1. Abrir `https://comprasmx.buengobierno.gob.mx/datos-abiertos`.
2. Esperar a que cargue la SPA (Angular) por completo.
3. Ir al ancla "datos_relevantes_de_los_contratos_ingresados_a_la_plataforma".
4. Descargar los enlaces `DD_PIC_CONTRATOS_*.xlsx`, `DD_PIC_EXPEDIENTES.xlsx` y `DD_RUPC_*.xlsx` que la página liste.

## 3 · SICEE (fila `:81`)
1. Seguir la receta ya verificada en `forense/notas/2026-09-01-MAESTRA34-L1-MORDIDA-SERIE-cierre.md`, líneas 183-198 (NO 165-195, esa cita del encargo original apunta a un rango equivocado).

## 4 · TEPJF_ELECCIONES_CONCURRENTES_1991_2018 (fila `NUEVA-L6`)
1. Abrir `https://www.te.gob.mx/publicaciones/`.
2. Esperar a que cargue el catálogo (es una aplicación JavaScript — por eso `curl` solo ve un shell de 2102 B).
3. Escribir "Elecciones concurrentes" en el buscador del catálogo.
4. Abrir la ficha del libro "Elecciones concurrentes y participación electoral en México, 1991-2018" (2020) y descargar el PDF.
5. Si el catálogo no lo lista, alternativa: repositorio del Centro de Capacitación Judicial Electoral.

## 5 · IEEPCO_OAXACA_SERIE_MUNICIPAL — pata 2016 (fila `NUEVA-L3`)
1. Descargar directo: `https://www.ieepco.org.mx/archivos/elecciones-2016/ESTAD%C3%8DSTICA%20CONCEJALES%20%202016.xlsx` (200, 968 301 B, verificado).
2. Nota: patas 2018/2021/2024 NO tienen receta de ≤1 min todavía — quedan `MESA-DECIDE` de un acto sucesor (portal `/autoridades_electas/resultados/`, por consulta).

## 6 · IETAM_TAMAULIPAS_SERIE_MUNICIPAL (fila `NUEVA-L3`)
1. Abrir `https://ietam.org.mx/PortalN/Paginas/EstadisticaEl/Estadistica_Electoral.aspx` en un navegador.
2. Hacer clic en cualquiera de los 43 enlaces `Municipios_2017-2018/<Municipio>.xlsx` listados (el navegador resuelve la ruta relativa real; una URL adivinada por patrón da 404).
3. Descargar; repetir por municipio (43 archivos).
4. Nota: 2021/2024 en esa página son de diputaciones/judicial, no municipal — no sirven para esta fila.

## 7 · PDN_SESNA_S1_S2_S3_S6 — sistemas S1/S2/S6 (fila del encargo N3)
1. Abrir `https://www.plataformadigitalnacional.org/`.
2. Localizar en el menú de sistemas: S1 (declaraciones), S2 (personas en contrataciones), S6 (contratos).
3. Descargar el mismo formato `.json` por entidad federativa que ya se usó para S3 (`PDN_S3v2.zip`).
4. Si el nombre de archivo/endpoint no es evidente, consultar la documentación de estructura en `github.com/PDNMX`.
