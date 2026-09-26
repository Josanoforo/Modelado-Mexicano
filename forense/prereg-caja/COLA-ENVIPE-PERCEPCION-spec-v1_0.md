# Pisos por segmento ENVIPE 2024 (percepción de inseguridad y cambio de hábitos por temor al delito) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-COMPLETA-1`, 26/sep/2026, CAJA, rama `acto/gen2-cola-completa-1`,
0-bis `0d4ae74d`. Encargo: `forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md` (§1 (a), cola v1.1:
VIOLENCIA/ENVIPE). CALC: `CALC-ENVIPE-PERCEPCION-2024-0001`. Congelada en el COMMIT-1, **antes** de leer un solo
valor de ENVIPE (sólo el descriptor/catálogos de variables y la línea de cabecera de los CSV).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Payload `envipe2024_csv` (manifiesto `data/manifiesto.yaml`), sha256 `90776b2f…` COINCIDE
  (verificado por `sha256sum` sobre `data/raw/envipe2024_csv.zip`). Miembros leídos:
  `tper_vic1_envipe2024/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2024.csv` (persona elegida, sección
  4 «Percepción sobre seguridad pública») y `tsdem_envipe2024/conjunto_de_datos/conjunto_de_datos_tsdem_envipe2024.csv`
  (sociodemográfico del hogar, sólo escolaridad `NIV`, unida por `ID_PER`). Catálogos de código:
  `tper_vic1_envipe2024/catalogos/{ap4_3_3,ap4_4_a,ap4_10_02,sexo,dominio}.csv` y `tsdem_envipe2024/catalogos/niv.csv`
  (dentro del mismo ZIP; no hay FD/PDF separado para ENVIPE datos abiertos, el descriptor es el propio catálogo del
  paquete). Cuestionario: `data/raw/cuest_principal_envipe2024.pdf` («INEGI. Encuesta Nacional de Victimización y
  Percepción sobre Seguridad Pública 2024. ENVIPE. Cuestionario principal. 2024»).
- `[EJECUTADO]` Una sola ola en corpus: ENVIPE 2024 abierta; ENVIPE 2026 (la más reciente de la serie) queda
  **RESERVADA** (`decisiones.tsv` `reserva:envipe2026`; medidor la excluye por prefijo `EXCLUIDOS_PREFIJO` y la
  guardia `_guardia_inputs` para si aparece entre los inputs). E.6: se abre 2024 y se declara; sin IC de
  persistencia (no se compara contra otra ola en este CALC).
- `[LEÍDO]` El medidor sólo toma tres reactivos de la sección 4 del cuestionario principal (percepción, no
  victimización): `AP4_3_3` (nivel estado), `AP4_4_A` (caminar de noche) y `AP4_10_02` (dejar de permitir salir
  solos a menores). No usa la sección de victimización delictiva (5.x) ni las de instituciones (6.x en adelante).
- `[LEÍDO]` `tsdem` es la tabla de personas del hogar (todas las edades, todas las personas), no sólo la persona
  elegida: la unión por `ID_PER` puede no encontrar pareja si `tsdem` no trae a esa persona con ese id, o puede
  encontrar más de una fila por `ID_PER` repetido entre hogares; el medidor deduplica por `id_per` en `une()` y
  cuenta explícitamente las filas sin `niv` (`FILAS-CON-NIV` vs `FILAS-DISENO-VALIDO`) en vez de asumir cobertura
  total.

## 1 · Unidad, universo, diseño

Unidad: **persona elegida de 18+** (`EDAD` entre 18 y 97, tabla `tper_vic1`). Peso `FAC_ELE` (factor de expansión
de la persona elegida). Bootstrap de UPM `UPM_DIS` dentro de estrato `EST_DIS`. Válido: peso > 0, estrato y UPM no
vacíos (receta `prepara_diseno`). Universo de las tres conductas: `EDAD >= 18` y `EDAD <= 97` (constante en el
medidor); código de edad fuera de ese rango, o en blanco, queda fuera del universo, no de la fila (la fila entra
al diseño si el peso/estrato/UPM son válidos; el universo lo filtra `mide_ola` aparte, vía la máscara `universo`).

## 2 · Conductas (por texto de pregunta, cuestionario principal ENVIPE 2024, catálogos del paquete de datos abiertos)

| conducta | pregunta (texto del cuestionario) | UNO | CERO |
|---|---|---|---|
| ESTADO-INSEGURO | «4.3 ¿En términos de delincuencia, considera que vivir en (ÁMBITO GEOGRÁFICO) es... seguro? / inseguro?», ámbito ESTADO (`AP4_3_3`; catálogo: 1 seguro, 2 inseguro, 9 No sabe/no responde) | 2 | 1 |
| INSEGURO-CAMINAR-DE-NOCHE | «4.4a En términos de delincuencia, dígame ¿qué tan seguro(a) se siente al caminar solo(a) por la noche en los alrededores de su vivienda?» (`AP4_4_A`; catálogo: 1 Muy seguro(a), 2 Seguro(a), 3 Inseguro(a), 4 Muy Inseguro(a), 5 No aplica, 9 No sabe/no responde) | 3, 4 | 1, 2 |
| DEJO-PERMITIR-MENORES-SALIR-SOLOS | «4.10 Durante 2023, por temor a ser víctima de algún delito (robo, asalto, secuestro, etcétera), ¿dejó de… permitir que los (las) menores de edad que viven en el hogar salgan solos(as)?» (`AP4_10_02`; catálogo: 1 Sí, 2 No, 3 No aplica, 9 No sabe/no responde) | 1 | 2 |

Todo otro código (no sabe/no responde `9`, no aplica `3`/`5`, blanco) queda fuera. El eje `AP4_3_3` es una de tres
sub-preguntas de 4.3 (colonia/localidad, municipio/demarcación, estado); el medidor sólo lee la de nivel estado
(`AP4_3_3`), lo declara así.

## 3 · Ejes (uno a la vez)

TOTAL · SEXO (`SEXO`: 1 Hombre, 2 Mujer) · EDAD (18-29, 30-44, 45-59, 60+) · ESCOLARIDAD (`NIV` de `tsdem`, unida
por `ID_PER`: hasta primaria 00-02, secundaria 03-05, media superior 06-07, superior 08-09; catálogo confirma
00 Ninguno, 01 Preescolar, 02 Primaria, 03 Secundaria, 04 Carrera técnica con secundaria terminada, 05 Normal
básica, 06 Preparatoria o bachillerato, 07 Carrera técnica con preparatoria terminada, 08 Licenciatura o
profesional, 09 Maestría o doctorado) · DOMINIO (`DOMINIO`: U Urbano, C Complemento urbano, R Rural) · ENTIDAD
(`CVE_ENT` 01-32). Sin cruces entre ejes.

## 4 · Estimación

Razón ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato (UPM única del estrato = de certeza), semilla y
réplicas fijadas en el contrato (`contrato["seed"]["valor"]`, `contrato["parametros"]["bootstrap_replicas"]`),
bloques de 50, percentiles 2.5/97.5, contrato conservador (una réplica degenerada → sin EE ni IC). Receta común
por sha256: `tools/dominios/salud/pisos_diseno.py` (input repo `receta_pisos_salud`) + motor
`tools/dominios/confianza/motor_pisos.py` (input repo `motor_pisos_confianza`); el medidor declara el sha256 de
ambos en el resultado (`{P}-G-INPUT-{...}-SHA256`). Un eje a la vez; nunca cruces.

**Semilla y réplicas (para recalcular):** `numpy.PCG64(20261003)`, 2000 réplicas, bloques de 50; el valor ejecutable vive en `data/corrida0/CALC-ENVIPE-PERCEPCION-2024-0001/spec.yaml` (`seed`, `parametros.bootstrap_replicas`) y es este mismo.

## 5 · Controles, secuencia

Sintético en `tests/test_cola_completa_pisos_gen2.py::test_envipe_union_y_conducto` (rama terminal por
`corrida0._valida_outputs`; construye `tper_vic1` y `tsdem` sintéticos con `id_per` deliberadamente desalineados
para forzar filas sin pareja, y verifica `FILAS-CON-NIV < FILAS-DISENO-VALIDO`, es decir que la unión no rellena
huecos). Guardia `_guardia_inputs`/`ParoDeGuardia`: para si un input fuera de la lista `{receta_pisos_salud,
motor_pisos_confianza, envipe2024_csv}` entra, o si el payload trae prefijo `envipe2026`/`envipe_2026`/
`cc1_inegi_envipe_2026` (ola reservada). Ninguna ejecución diagnóstica sobre el dato: la primera corrida es
`corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Escala y unidad:** proporciones de personas de 18+; ninguna se promedia con otra unidad. **Percepción ≠
victimización:** las tres conductas miden percepción de inseguridad y cambio de hábito declarado, no si la
persona fue víctima de un delito; una cifra alta de «dejó de permitir salir solos a menores» es temor
declarado, no incidencia delictiva medida por este CALC. **Estructura ≠ cultura:** diferencias por sexo,
escolaridad o entidad en la percepción de inseguridad reflejan exposición desigual al espacio público, cobertura
mediática y contexto local (tasas delictivas, presencia policial), no un «rasgo» de la población de esa
entidad o grupo. **Evidencia:** (a) datos primarios en México. **Temporalidad:** RETROSPECTIVO (4.10 pregunta
por lo sucedido durante 2023, un año antes del levantamiento 2024); ninguna cifra PROSPECTIVA. **Cifra escrita a
mano:** ninguna.

## 7 · Discrepancias medidor↔descriptor

Ninguna encontrada: los tres códigos de conducta (`AP4_3_3`, `AP4_4_A`, `AP4_10_02`), sus catálogos de valores y
sus columnas de diseño (`FAC_ELE`, `EST_DIS`, `UPM_DIS`, `CVE_ENT`, `DOMINIO`, `SEXO`, `NIV`) casan con los
catálogos del paquete de datos abiertos y con el texto del cuestionario principal ENVIPE 2024. El texto de las
tres preguntas es `[TEXTO-DEL-MEDIDOR, VERIFICADO CONTRA EL CUESTIONARIO]` (arriba, §2).

El primer resultado que produzca este procedimiento es el que se reporta.
