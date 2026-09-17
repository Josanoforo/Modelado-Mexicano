# Estructura y contrato documental confirmado

Estado: `ESTRUCTURA-LEÍDA · CERO-REGISTROS · SIN-TASAS`.

## Correspondencia de archivos

| Periodo | Básico | Socioeconómico | Vivienda |
|---|---|---|---|
| junio 2025 | `encocb_0625.DBF` | `encocs_0625.DBF` | `encoviv_0625.DBF` |
| junio 2026 | `encocb_0626.DBF` | `encocs_0626.DBF` | `encoviv_0626.DBF` |

En ambas cabeceras del cuestionario básico existen `N_REN` (`C`, longitud
2), `P10` (`C`, longitud 1) y `FACTOR` (`N`, longitud 6), además de P1–P15.
La tabla socioeconómica trae `ELEGIDO`, `UPM`, `FACTOR` y `FAC_P18` en ambas
olas. La inspección terminó en el byte de fin de cabecera DBF: no leyó un solo
registro ni derivó tamaño muestral, frecuencia, mínimo, máximo o marginal.

Hay una modificación estructural visible que no debe ocultarse: en 2026 se
renombran algunos identificadores geográficos (`ENT`→`CVE_ENT`, por ejemplo) y
se agregan `CVE_MUN`/`CVEGEO` en las tablas básica y socioeconómica; la tabla de
vivienda también cambia nombres geográficos. P10, su tipo/longitud y FACTOR se
mantienen. Esto sostiene una misma transformación descriptiva para P10, pero
no prueba por sí solo que todos los detalles del diseño sean invariantes.

## Qué confirman los documentos

- El cuestionario básico vigente en el corpus (`c_enco_b_v4`, SHA-256
  `f7e9d6b9…`) dice “sólo para personas de 18 años y más”. P10 pregunta si
  **usted** tiene actualmente posibilidades de ahorrar parte de sus ingresos:
  1 Sí, 2 No, 3 No sabe, 4 No tiene ingresos. No pregunta si ya posee ahorro.
- El descriptor `fd_enco_v5` liga ENCOCB con P10, N_REN, FACTOR y FOL. Es un
  descriptor histórico; se usa para correspondencia, no como prueba solitaria
  de invariancia actual.
- El manual de procedimientos (2016, pp. impresas 5, 7, 17 y 31) distingue el
  hogar como unidad de observación y a **una sola persona elegida** de 18 años o
  más para el cuestionario básico. La selección es automática/aleatoria entre
  integrantes elegibles; por tanto P10 no es un atributo de todos los miembros.
- La RNM oficial de ENCO 2025 confirma población de 18+ residente permanente
  en viviendas particulares del dominio, cobertura de las principales zonas
  urbanas con representación nacional, muestreo probabilístico trietápico,
  estratificado y por conglomerados, selección aleatoria final de una persona y
  2 336 viviendas mensuales.
- La ficha metodológica oficial publicada en 2026 conserva 32 ciudades,
  periodicidad mensual, 2 336 viviendas, esquema probabilístico trietápico,
  estratificado y por conglomerados, y panel rotatorio 4 meses en muestra, 8 de
  descanso y 4 de regreso.

## Rotación, dependencia y exposición

El manual/RNM divide la muestra en ocho paneles: sustituye dos cada mes,
conserva 75% entre meses consecutivos y vuelve a observar 50% de las viviendas
al mismo mes del año siguiente. Junio 2025 y junio 2026 no son muestras
independientes. Una diferencia o persistencia interanual requiere una varianza
que represente la superposición; no se permite sumar varianzas como si fueran
dos cortes independientes.

Al consultar la ficha metodológica 2026, el buscador expuso incidentalmente un
tabulado oficial de P10 para el mes anterior a la ola seleccionada. El valor no
se copia aquí ni en fixtures, y las respuestas de junio continúan cerradas, pero
se retira toda pretensión de cegamiento perfecto para la pieza 2026: estado
`RESPUESTAS-JUNIO-NO-ABIERTAS · CEGAMIENTO-FAMILIA-PARCIAL`.
