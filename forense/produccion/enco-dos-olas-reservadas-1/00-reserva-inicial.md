# Reserva prospectiva inicial · ENCO junio 2025 + junio 2026

Estado: `COMMIT-1 · RESERVA-FIJADA · SIN-RESPUESTAS-ABIERTAS`

Acto: `GEN2-ENCO-DOS-OLAS-RESERVADAS-1`

Base al fijar: `origin/main@e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5`

Fecha de fijación: 16/sep/2026 America/Mexico_City (17/sep/2026 UTC)

## Pareja y motivo previo a cualquier cifra

| Rol documental | Periodo fijado | Objeto oficial | Motivo prospectivo |
|---|---|---|---|
| ola anterior | junio 2025 | `enco_2025_junio_dbf.zip` | mismo mes, separación anual |
| ola posterior | junio 2026 | `enco_2026_junio_dbf.zip` | mismo mes, separación anual y exclusión de agosto 2026 |

No había acto vigente que fijara fechas distintas: la proyección, la cola y el
panel sólo pedían dos olas genéricas. La selección no depende de tasas ni de
ningún valor de P10. Ambas olas forman una sola familia ENCO y quedan reservadas
para factibilidad posterior. Ninguna adquiere por este documento el papel de
holdout confirmatorio. El esquema rotatorio puede inducir dependencia entre
meses y hogares; igualar mes no prueba independencia, invariancia del
cuestionario ni ausencia de cambios de diseño.

## Propósito y separación de estados

- **Adquisición completa:** bytes oficiales presentes, identidad e integridad
  registradas, sin afirmar contenido semántico a partir de `testzip`.
- **Definición completa:** P10/equivalente, universo, persona que responde,
  filtro, códigos, factor, diseño, rotación, cobertura y comparabilidad
  acreditados documentalmente para cada fecha.
- **Elegibilidad experimental:** requiere un enlace científico previo con M;
  no nace de adquirir ni definir las olas.

El estimando candidato es la proporción ponderada que responde **Sí** a la
posibilidad actual de ahorrar entre respuestas sustantivas elegibles. Es una
posibilidad percibida, no tenencia de ahorro. La persona seleccionada no se
tratará como atributo de todos los integrantes del hogar.

## Permitido en este acto

- localizar desde páginas o índices oficiales de INEGI las URLs reales de los
  dos paquetes ya fijados;
- hacer una descarga final por paquete y verificar URL final, tipo, tamaño,
  SHA-256 y contenedor;
- listar miembros del ZIP y leer únicamente estructura de DBF (nombres, tipos y
  metadatos), nunca filas;
- obtener hasta dos documentos estructurales imprescindibles si aún faltan;
- depositar los paquetes en la raíz lógica no escaneable
  `reserva_respondentes`, bajo `ENCO/2025-06/` y `ENCO/2026-06/`;
- añadir sólo estas identidades y documentación efectivamente adquirida al
  manifiesto.

## Prohibido en este acto

- abrir registros, previews, muestras, frecuencias, marginales, tasas,
  mínimos/máximos o el DBF de agosto 2026;
- calcular ahorro real, producir CALC/R, ejecutar F6 o llamar brazos/modelos;
- equiparar `P(posibilidad de ahorrar)` con
  `P(dinero.ahorro.tiene_ahorros)` o complementarlas por conveniencia;
- usar junio 2025 para fabricar B, promover paquetes al corpus L o ponerlos en
  `data_raw`;
- sustituir fechas, recorrer meses buscando un resultado, modificar cola/cron,
  reiniciar presupuesto del servicio de adquisición o tocar las cascadas
  diferidas.

## Receta de adquisición fijada

1. Comprobar por identidad si los dos archivos ya existen en la raíz reservada.
2. Confirmar que no hay dueño activo del mismo objetivo y respetar presupuesto,
   lock y exclusiones del servicio existente; este acto no consume ni reinicia
   su cuota genérica.
3. Resolver los enlaces en el índice/página oficial y descargar como máximo los
   dos paquetes fijados. Si una fecha no está publicada, conservar la otra sin
   sustitución.
4. Rechazar HTML disfrazado, error interno o discordancia de periodo. Validar
   ZIP, listar miembros sin contenido y extraer sólo cabeceras DBF con un lector
   que no materialice filas.
5. Publicar atómicamente sin sobreescritura en la raíz lógica
   `reserva_respondentes`, que está fuera de las raíces escaneables generales.
6. Registrar recibos y entradas aditivas únicas de manifiesto. Sólo entonces
   rotular la pieza correspondiente como `OBTENIDA-RESERVADA`.

URLs oficiales localizadas antes de solicitar bytes:

- `https://www.inegi.org.mx/contenidos/programas/enco/microdatos/2025/enco_2025_junio_dbf.zip`
- `https://www.inegi.org.mx/contenidos/programas/enco/microdatos/enco_2026_junio_dbf.zip`

Las URLs provienen del índice masivo oficial versionado; un HTTP 200 posterior
no bastará para declarar adquisición.
