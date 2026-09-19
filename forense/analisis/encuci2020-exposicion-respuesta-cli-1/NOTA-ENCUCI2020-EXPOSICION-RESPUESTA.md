# GEN2-ENCUCI2020-EXPOSICION-Y-RESPUESTA-CLI-1 · nota de ejecución

## Resultado

`CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001` quedó ejecutado y sellado desde
el COMMIT-1 `b3151f7d3d683f14cf875b6ba64a4ed4ceed334d`. Corrida
`CALC-ENCUCI2020-EXPOSICION-RESPUESTA-0001--b3151f7d3d68`; sello
`36255f8c39868b79902c63b95ddc3b65fcf2a63e6462de325c7657535ff2ce5e`.
`verify` devuelve `REPRODUCE`, contexto `IDENTICO`, 17/17 RESULT idénticos.

Marco: 21,519 personas, todas con `FAC_SEL` válido; masa ponderada 96,427,583;
281 estratos, 3,096 UPM, cero estratos singleton y llave `ID_PER` única. Los
IC95 son percentiles de 2,000 réplicas de UPM dentro de estrato sobre el marco
completo. Las tablas expresan porcentajes; `n` es muestra sin ponderar.

## Exposición por tipo

| Tipo de contacto | n válido | % Sí | IC95 % | n desconocido | masa desconocida % |
|---|---:|---:|---:|---:|---:|
| AP5_16_1 · policía de tránsito/seguridad pública | 21,465 | 21.01 | [20.13, 21.89] | 54 | 0.189 |
| AP5_16_2 · Ministerio Público | 21,455 | 6.27 | [5.81, 6.75] | 64 | 0.224 |
| AP5_16_3 · jueces | 21,445 | 4.10 | [3.72, 4.53] | 74 | 0.265 |
| AP5_16_4 · salud pública | 21,470 | 42.75 | [41.69, 43.70] | 49 | 0.194 |
| AP5_16_5 · educación pública | 21,444 | 35.29 | [34.09, 36.39] | 75 | 0.257 |
| AP5_16_6 · seguridad social/bienestar | 21,410 | 12.31 | [11.67, 12.93] | 109 | 0.399 |
| AP5_16_7 · gobierno municipal/alcaldía | 21,455 | 17.91 | [16.99, 18.87] | 64 | 0.215 |
| AP5_16_8 · gobierno estatal/federal | 21,453 | 11.84 | [11.13, 12.55] | 66 | 0.216 |
| AP5_16_9 · Guardia Nacional | 21,437 | 4.06 | [3.64, 4.50] | 82 | 0.244 |
| AP5_16_10 · Ejército/Marina | 21,447 | 3.91 | [3.50, 4.31] | 72 | 0.227 |

Contacto con cualquiera: 63.69% (IC95 [62.60, 64.78]), n válido 21,426. Los
93 casos sin clasificación pesan 0.313% del marco. No se suman las filas por
tipo: son contactos coexistentes.

La cuenta exacta cubre 99.294% de la masa (21,317 casos):

| Número de tipos | n categoría | % | IC95 % |
|---|---:|---:|---:|
| 0 | 7,991 | 36.45 | [35.36, 37.54] |
| 1 | 5,098 | 23.15 | [22.43, 23.91] |
| 2 | 3,525 | 16.87 | [16.14, 17.61] |
| 3+ | 4,703 | 23.53 | [22.50, 24.52] |

## Respuesta conjunta entre personas con contacto

`Cob.` es la masa con AP5_17/18 válidas sobre la base del grupo; `n resp.` es
el denominador sin ponderar después de ese filtro. U/C/R son categorías
nativas separadas y no se cruzan con conteo. `Unión` incluye IC95. Las últimas
tres columnas son P(entrega|solicitud), P(entrega|no solicitud) y su diferencia
con IC95.

| Grupo | n base | Cob. % | n resp. | Ninguna % | Sólo solicitud % | Sólo entrega % | Ambas % | Unión % [IC95] | E\|S % | E\|no S % | Diferencia pp [IC95] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| total contacto | 13,435 | 99.84 | 13,411 | 87.40 | 5.24 | 1.97 | 5.40 | 12.60 [11.68, 13.52] | 50.75 | 2.20 | 48.54 [43.84, 53.39] |
| 1 tipo | 5,098 | 99.66 | 5,085 | 93.18 | 3.41 | 1.05 | 2.36 | 6.82 [5.52, 8.29] | 40.90 | 1.12 | 39.78 [29.25, 51.12] |
| 2 tipos | 3,525 | 99.95 | 3,524 | 90.71 | 3.68 | 1.63 | 3.99 | 9.29 [7.86, 10.85] | 52.04 | 1.76 | 50.27 [41.03, 59.76] |
| 3+ tipos | 4,703 | 99.96 | 4,699 | 79.34 | 8.17 | 3.07 | 9.42 | 20.66 [18.71, 22.54] | 53.53 | 3.73 | 49.80 [44.11, 55.68] |
| DOMINIO U | 6,837 | 99.83 | 6,826 | 84.49 | 6.39 | 2.37 | 6.75 | 15.51 [14.18, 16.88] | 51.36 | 2.72 | 48.64 [42.52, 54.57] |
| DOMINIO C | 3,280 | 99.80 | 3,274 | 91.06 | 3.39 | 1.51 | 4.05 | 8.94 [7.23, 10.74] | 54.45 | 1.63 | 52.82 [40.50, 64.55] |
| DOMINIO R | 3,318 | 99.90 | 3,311 | 92.19 | 3.79 | 1.27 | 2.75 | 7.81 [6.55, 9.06] | 41.99 | 1.36 | 40.64 [31.90, 49.67] |

Contrastes con covarianza del mismo sorteo de diseño:

| Contraste | Diferencia pp | IC95 pp |
|---|---:|---:|
| 2−1 tipos, unión | 2.47 | [0.34, 4.55] |
| 2−1 tipos, brecha condicional | 10.49 | [-4.38, 24.64] |
| 3+−1 tipos, unión | 13.84 | [11.35, 16.31] |
| 3+−1 tipos, brecha condicional | 10.02 | [-2.20, 22.12] |

Lectura: la unión de solicitud/entrega se concentra claramente más en personas
que reportaron contacto con 3+ tipos, y en menor medida con dos frente a uno.
Esto describe composición/exposición de personas: los tipos no cuentan
trámites, la encuesta no enlaza AP5_17/18 con una autoridad y la coobservación
no identifica una transacción ni una secuencia. Las brechas condicionales son
grandes en todos los grupos, pero sus diferencias entre conteos tienen IC que
incluyen cero; no se seleccionan ni se causalizan.

## Mapa RESULT → estimando/universo

| RESULT | Estimando y universo |
|---|---|
| `...-EXPOSICION-POR-TIPO` | Diez proporciones Sí entre 1/2, cada una con desconocimiento, marco FAC_SEL válido. |
| `...-CONTACTO-CUALQUIERA` | Cualquier Sí frente a diez No; resto desconocido, marco FAC_SEL válido. |
| `...-COBERTURA-CONTEO-EXACTO` | Masa con diez 1/2 sobre el marco. |
| `...-CONTEO-TIPOS` | Distribución 0/1/2/3+ entre vectores completos. |
| `...-RESPUESTA-CONJUNTA` | Cuatro celdas, unión y condicionales entre contacto + AP5_17/18 válidas, en siete grupos no cruzados. |
| `...-CONTRASTES` | 2−1 y 3+−1 para unión y brecha condicional, diferencia por réplica. |
| `...-CONTROL-NACIONAL` | Cotejo, mismo universo, con CALC-ENCUCI-0001; no resultado nuevo. |
| `...-VALIDACION-PARTICION/UNION` | Identidades algebraicas en total contacto. |
| `...-N-*`, `...-MASA-*`, `...-LLAVE-*`, `...-METODO-IC` | Marco y diagnóstico de diseño. |

## Validaciones, hashes y reservas

- Partición: suma de cuatro celdas menos uno = `0.0`.
- Unión: diferencia contra solicitud + entrega − ambas =
  `2.7755575615628914e-17` (redondeo de float64).
- Control nacional independiente: unión `0.12600561008991654`, delta exacto
  `0` frente al RESULT sellado de CALC-ENCUCI-0001; n 13,411.
- Control independiente de punto/varianza representativa, con lector del CALC
  precedente y linealización WR por UPM: AP5_16_4 =
  `0.4275205077195218`; varianza `2.737175909631291e-05`, SE
  `0.005231802662210503`, IC normal aproximado [0.417266, 0.437775], coherente
  con el IC bootstrap sellado [0.416881, 0.437024].
- Payload `0414fd59…f283`; descriptor `6cd6f747…5638`; preregistro
  `b1aa0fe8…218f`; encargo `fc28eee3…70ca`; medidor `25d1341f…bf80`; prueba
  `7cc7b0c4…8685`; spec humana `5ed2a697…1680`; spec YAML sellada
  `19e5d595…1dea`.
- `spec-check`: 17/17 variables OK en 317,718 filas de inventarios. Prueba
  sintética y `py_compile`: OK. Preflight: VERDE. Sello: COINCIDE. Verify:
  REPRODUCE/IDENTICO.
- Replay dirigido asentado sólo para este CALC. `registro --escribe --lote`
  añadió 1 corrida y 17 RESULT propios; al regenerar la vista completa añadió
  además 20 usos de marcador ya derivados por la lógica vigente del registro,
  sin adjudicación ni edición manual y sin cambiar replay ajeno.
- `CONSUMIDO`: encargo archivado byte a byte; SHA coincide con el original.
- `NO-CORRIDO / RESERVAS`: ENIF2024, ENCIG2025, ENVIPE2025, HOLDOUT y piloto
  3 no se abrieron. No se ejecutó adopción, no se tocó RES-0005/F2, no se
  comparó temporal o causalmente con ENCIG, no se modificaron milpa/canon/
  decisiones/NC/motor/corrida0/tests/check/workflows.
- Adopción y contador: `PENDIENTE-DE-MESA`. Integración: pendiente de Claude/
  mesa. Este acto no fusiona.
