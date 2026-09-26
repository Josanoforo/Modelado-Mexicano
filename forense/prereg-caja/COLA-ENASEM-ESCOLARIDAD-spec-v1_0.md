# Escolaridad y años de educación en personas de 50+, ENASEM 2021 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-COMPLETA-1`, 26/sep/2026, CAJA, rama `acto/gen2-cola-completa-1`,
0-bis `0d4ae74d`. Encargo: `forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md` (§1 (a), cola v1.1:
GÉNERO/ENASEM-ENDISEG-ENSU-ENVIPE, DINERO/CONEVA-ENASEM). CALC: `CALC-ENASEM-ESCOLARIDAD-2021-0001`. Congelada
en el COMMIT-1, **antes** de leer un solo valor de ENASEM (sólo el manifiesto, el FD y la línea de cabecera del
CSV). **El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Payload `enasem2021_bd_csv_zip` (manifiesto), sha256 `68b8f7ec…` COINCIDE con
  `data/raw/enasem2021/enasem_2021_bd_csv.zip`; miembro `SECT_A_C_D_E_PC_F_H_I_2021.csv` (cabecera leída, 986
  columnas, sin abrir filas). Descriptor: `enasem2021_fd_xlsx`, sha256 `00f5dfae…` COINCIDE con
  `data/raw/enasem2021/enasem_2021_fd.xlsx`, hoja `SECT_A_C_D_E_PC_F_H_I_2021` para la conducta y hoja
  `MASTER_FOLLOW_UP_FILE_2021` para las variables de identificación/diseño (`SEX_21`, `AGE_21`, `FACTORI_21`,
  `EST_DIS_21`, `UPM_DIS_21`: comunes a todos los archivos de la ronda 2021 y documentadas ahí, no en la hoja
  del archivo de sección; se confirma que las seis columnas de `COLS_CRUDAS` existen literalmente en la cabecera
  del CSV, incluyendo `YRSCHOOL` — no `YRSCHOOL_21` ni `YRSCHOOL_18`, que son variables distintas del mismo FD:
  `YRSCHOOL_18` es «Años de Educación (solo para nuevas parejas)», 00…19, otra pregunta).
- `[EJECUTADO]` Corpus ENASEM: 2018, 2021, 2024. 2024 (`enasem2024_bd_csv_zip`) es la ola más reciente del
  programa y queda RESERVADA (E.6): no se abre, no se nombra como input, no se lee su FD ni sus tabulados. Se
  abre 2021 (una sola ola abierta; sin IC de persistencia entre olas — el medidor no compara 2018 vs 2021).
- `[LEÍDO]` El FD no trae una variable derivada de «escolaridad» por tramos (primaria/secundaria/etc.) para el
  archivo de sección A-C-D-E-PC-F-H-I: sólo `YRSCHOOL`, años de educación en conteo (00…22), y su gemela
  `YRSCHOOL_18` para cónyuges nuevos del panel (no usada aquí). La definición de SIN-ESCOLARIDAD /
  SEIS-ANOS-O-MENOS de §2 es de esta spec, sobre el conteo.

## 1 · Unidad, universo, diseño

Unidad: **persona entrevistada de 50 años o más** (`AGE_21`, FD hoja `MASTER_FOLLOW_UP_FILE_2021`: «Edad 2021»,
alfanumérico 017…107, con 888 «No responde» y 999 «No sabe» fuera de rango — el universo es `50 <= AGE_21 <= 120`, así que 888/999 quedan fuera; ver §7). Peso `FACTORI_21` («Factor
individual 2021», 0…116633) > 0. Bootstrap de UPM `UPM_DIS_21` («Unidad primaria de muestreo de diseño»,
00000001…00012514) dentro de estrato `EST_DIS_21` («Estrato de diseño 2021», 1…4). Válido: peso > 0, estrato y
UPM no vacíos (`M.prepara_diseno`).

## 2 · Conductas (FD `enasem2021_fd_xlsx`, hoja `SECT_A_C_D_E_PC_F_H_I_2021`, variable `YRSCHOOL`)

| conducta | pregunta (texto del FD) | UNO | CERO |
|---|---|---|---|
| SIN-ESCOLARIDAD | «Años de Educación» (`YRSCHOOL`, alfanumérico 2, códigos válidos 00…22) [TEXTO-DEL-MEDIDOR, NO-VERIFICADO-AQUÍ: el FD no da el enunciado exacto que se leyó al informante, sólo el nombre de la variable derivada; se confirma contra el FD que `YRSCHOOL` existe con ese nombre y ese rango] | 0 | 1–22 |
| SEIS-ANOS-O-MENOS | misma variable `YRSCHOOL` | 0–6 | 7–22 |

El FD no documenta blancos, «no responde» ni «no sabe» para `YRSCHOOL` (a diferencia de `AGE_21` o `A2A2_1`,
que sí traen 88/99/888/999 catalogados): el rango válido documentado es cerrado 00…22 y el medidor no declara un
código de no respuesta para esta variable — cualquier valor fuera de 0–22 (blanco al leer el CSV, por ejemplo)
queda fuera de las dos listas UNO/CERO por construcción de `mide_ola` (no aporta a ninguna categoría declarada).

## 3 · Ejes (uno a la vez)

TOTAL · SEXO (`SEX_21`, FD hoja `MASTER_FOLLOW_UP_FILE_2021`: «Sexo», 1 Hombre / 2 Mujer → HOMBRE/MUJER) · EDAD
(`AGE_21`, cuatro tramos fijados en el medidor antes de ver la distribución: 50-59, 60-69, 70-79, 80-MAS con
80-130 como cierre abierto). No hay eje de entidad, tamaño de localidad ni escolaridad-tramo adicional: el
medidor no los declara y esta spec no los añade.

## 4 · Estimación

Razón ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato (UPM única del estrato = de certeza), semilla y
número de réplicas tomados del contrato de ejecución (`contrato["seed"]["valor"]`,
`contrato["parametros"]["bootstrap_replicas"]`; el pre-registro no fija aquí un valor de semilla propio de este
CALC — lo fija el contrato de la corrida, igual que en ENDISEG/MMSI donde §4 sí cita `PCG64(...)` explícito;
DISCREPANCIA declarada en §7), bloques de 50, percentiles 2.5/97.5, contrato conservador (una réplica degenerada
→ sin EE ni IC), vía `M.mide_ola`. Receta común por sha256: `tools/dominios/salud/pisos_diseno.py` (módulo
`receta_pisos_salud`) + motor `tools/dominios/confianza/motor_pisos.py` (módulo `motor_pisos_confianza`), ambos
inyectados como bytes de input repo (`INPUTS_REPO = {"receta_pisos_salud", "motor_pisos_confianza"}`) y su
sha256 se registra en el resultado (`{P}-G-INPUT-*-SHA256`). Un eje a la vez; nunca cruces.

**Semilla y réplicas (para recalcular):** `numpy.PCG64(20260930)`, 2000 réplicas, bloques de 50; el valor ejecutable vive en `data/corrida0/CALC-ENASEM-ESCOLARIDAD-2021-0001/spec.yaml` (`seed`, `parametros.bootstrap_replicas`) y es este mismo.

## 5 · Controles, secuencia

Sintético en `tests/test_cola_completa_pisos_gen2.py::test_enasem_conducto` (frame sintético con `yrschool`
0–22, `sex_21` 1–2, `age_21` 30–100 —incluye edades bajo 50 para ejercitar el filtro de universo—,
`factori_21` 1–99, `est_dis_21` 1–4, `upm_dis_21` 1–70; corre `m.mide` con 20 réplicas y cierra con
`corrida0._valida_outputs` contra `esquema_resultados()`, sin NaN ni inf) y
`test_guardia_ola_reservada_o_excluida_para[CALC-ENASEM-ESCOLARIDAD-2021-0001-enasem2024_bd_csv_zip]` (guardia
que PARA si `enasem2024_bd_csv_zip` entra como input, vía `EXCLUIDOS_PREFIJO = ("enasem2024",)`). También cubierto
por `test_spec_yaml_resultados_es_el_esquema[CALC-ENASEM-ESCOLARIDAD-2021-0001]` (el `spec.yaml` del CALC declara
exactamente `esquema_resultados()`). Ninguna ejecución diagnóstica sobre el dato: la primera corrida es
`corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Escala y unidad:** proporciones de personas de 50+ años; ninguna se promedia con otra unidad (hogar, panel).
**Autorreporte de escolaridad:** años de educación autorreportados en una encuesta de salud y envejecimiento
dependen de memoria y de convención local sobre qué cuenta como «año aprobado»; SIN-ESCOLARIDAD mezcla nunca
haber asistido con no completar el primer año, y el FD no distingue ambos casos dentro de `YRSCHOOL = 0`.
**Estructura ≠ cultura:** una escolaridad más baja por tramo de edad (80-MAS vs 50-59) es cohorte educativa
histórica de México (expansión de la educación primaria a partir de los 1960s-70s), no una diferencia cultural
entre grupos de edad. **Panel longitudinal:** ENASEM sigue a las mismas personas desde 2001; la ola 2021 es un
corte transversal de ese panel con su propio factor individual (`FACTORI_21`), no una muestra fresca —esto no
cambia la lectura de proporción pero explica por qué el estrato de diseño es de apenas 1…4 categorías (diseño
heredado del panel, no un estrato geográfico fino). **Evidencia:** (a) datos primarios en México.
**Temporalidad:** RETROSPECTIVO; ninguna cifra PROSPECTIVA. **Cifra escrita a mano:** ninguna.

## 7 · Discrepancias medidor↔descriptor/spec, declaradas (D-15, latitud punto 1)

1. **Universo con guardia de 888/999 en `AGE_21`.** El FD documenta `AGE_21` con 888 «No responde» y 999 «No sabe»
   además del rango real 017…107. El borrador del medidor filtraba sólo `>= 50`; al revisar esta spec contra el FD,
   antes del COMMIT-1, el universo pasó a `(AGE_21 >= 50) & (AGE_21 <= 120)`, que deja fuera 888/999 (declarado).
2. **Semilla y réplicas no fijadas en el pre-registro (a diferencia de ENDISEG/MMSI).** ENDISEG y MMSI fijan en
   su §4 un generador y semilla explícitos (`PCG64(20260926)`, `PCG64(20260927)`); esta spec no puede fijar una
   semilla propia porque el medidor (`medir`) toma `replicas` y `semilla` del `contrato` de ejecución, no de una
   constante del módulo. Se declara como diferencia de forma respecto a las otras dos plantillas, no como
   defecto: el mecanismo (bootstrap de UPM, bloques de 50, percentiles 2.5/97.5) es el mismo motor por sha256.
3. **`YRSCHOOL` sin código de no respuesta catalogado en el FD.** A diferencia de casi toda otra variable del
   archivo (que trae 88/99/888/999 etc.), el FD no documenta un código de blanco/no-respuesta para `YRSCHOOL`
   (sólo el rango cerrado 00…22). El docstring del medidor dice «blanco fuera»: esto es consistente con que
   `mide_ola` sólo asigna a las listas UNO/CERO declaradas (0 y 1–22 cubren todo el rango documentado), por lo
   que cualquier valor realmente en blanco al leer el CSV queda fuera sin necesidad de un código explícito. No
   se considera defecto.

El primer resultado que produzca este procedimiento es el que se reporta.
