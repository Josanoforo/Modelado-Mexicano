# Lectura · seis interacciones WBES México 2023

Salida determinista: `wbes2023-precision-interacciones.csv`, SHA-256 `067911e668442955a9108d97061dd53727889f91a9112d2f88ee3a447d93f632`. Universo: establecimientos formales privados WBES México 2023; 1,322 establecimientos, 242 estratos, 34 singleton y 1,080 grados de libertad. Los IC son aproximados, condicionales a diseño WR, `wmedian`, desenlaces clasificables y los dos tratamientos publicados para singleton; no hay FPC ni réplicas oficiales.

| Interacción (ventana) | expuestos | sí/no/desconocidos | tasa | IC95 certeza / average | límites por faltantes |
|---|---:|---:|---:|---:|---:|
| Electricidad (2 años) | 44 | 8 / 33 / 3 | 27.61% | 10.09–56.43 / 9.25–58.78% | 27.36–28.25% |
| Agua (2 años) | 14 | 2 / 12 / 0 | 26.37% | 3.82–76.36 / 3.23–79.34% | 26.37–26.37% |
| Construcción (2 años) | 137 | 16 / 111 / 10 | 7.31% | 3.39–15.05 / 3.19–15.88% | 7.00–11.33% |
| Fiscal (último año) | 75 | 8 / 60 / 7 | 5.45% | 1.99–14.05 / 1.84–15.07% | 5.25–8.84% |
| Importación (2 años) | 17 | 0 / 17 / 0 | 0.00% | no estimable (frontera) | 0.00–0.00% |
| Operación (2 años) | 40 | 6 / 32 / 2 | 15.72% | 6.23–34.38 / 5.77–36.23% | 15.29–18.05% |

Los límites por faltantes son de identificación, no IC y se reportan separados; la anchura de cada uno está en el CSV, igual que la anchura del IC. No se infiere un ranking combinando ambas anchuras.

## Contraste único

Fiscal menos operación usa sólo 2 establecimientos doblemente expuestos y con doble desenlace válido (masa 126.375 de 126.375 entre doblemente expuestos, cobertura 100%). Ambos puntos son 31.48%, por lo que la diferencia es 0.00 pp; su EE e IC también son 0 bajo ambos escenarios, y la covarianza de diseño es 0.093053 (certeza) / 0.108263 (average). Esto no identifica mayor riesgo anual: fiscal usa último año y operación dos años. El soporte es extremadamente escaso; no debe sustituirse por dos muestras distintas.

## Mapa RESULT y controles

`RESULT-WBES2023-INT-G-*` identifica tipo, hash, ruta y 62 filas. `RESULT-WBES2023-INT-CONTRASTE-{CERTEZA,AVERAGE}-DIFERENCIA` y `-COVARIANZA` son la diferencia y covarianza del contraste; los demás resultados de tasas están contenidos, con hash, en el CSV determinista. Pruebas ejecutadas: tres sintéticas (desconocidos, universo común/covarianza y frontera/grupo vacío), `spec-check` (317,718 filas de inventario), `run` con 5/5 hashes y `verify` con resultado `REPRODUCE` / contexto `IDENTICO`.

Reserva: los puntos de fiscal y operación del contraste están documentados arriba pero no tienen columnas dedicadas en la primera salida sellada; una sucesión deberá añadirlas sin alterar este sello.
