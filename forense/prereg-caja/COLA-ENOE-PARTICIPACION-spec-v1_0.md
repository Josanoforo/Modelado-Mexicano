# Participación económica y NINI 18-24 por sexo, ENOE 2024T4 (FAMILIA/ENOE) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-COMPLETA-1`, 26/sep/2026, CAJA, rama `acto/gen2-cola-completa-1`,
0-bis `0d4ae74d`. Encargo: `forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md` (§1 (a), cola v1.1:
FAMILIA/ENOE). CALC: `CALC-ENOE-PARTICIPACION-2024T4-0001`. Congelada en el COMMIT-1, **antes** de leer un
solo valor de ENOE 2024T4 (sólo el descriptor de archivos y la línea de cabecera del CSV).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Payload `enoe_2024_4t_microdatos` (manifiesto), sha256 `817f28d2…` COINCIDE; miembro
  `ENOE_SDEMT424.csv` (tabla sociodemográfica de 2024T4). Descriptor: `enoe_325_fd_c_bas_amp.pdf`
  («Encuesta Nacional de Ocupación y Empleo (ENOE). Estructura de la base de datos. 2025», tabla
  SDEMT), corroborado contra el criterio de universo que el propio FD imprime literal: «UNIVERSO: para
  el uso de las variables se debe aplicar el criterio R_DEF= 00 y C_RES=1 o 3 y EDAD 15 a 98 AÑOS».
- `[EJECUTADO]` Una sola ola del instrumento: 2024T4 es el trimestre que el report cita («diciembre
  2024»). ENOE 2026T2 (tabla final de CORPUS-COMPLETO) queda RESERVADA y el boletín 2026T1 ya fue
  consumido para informalidad (C4 de FIRMAS-16); ninguno de los dos es input de este CALC, que no mide
  informalidad. Sin IC de persistencia: un solo trimestre.
- `[LEÍDO]` El FD no trae una variable derivada de participación económica más allá de `Clase1`
  (PEA/PNEA) ni de «ni estudia ni trabajo» para jóvenes: ambas se construyen aquí a partir de variables
  crudas (§2), como en el resto de la cola.

## 1 · Unidad, universo, diseño

Unidad: **persona de 15+ años en el universo estándar de ENOE** (el de
`tools/dominios/enoe/pisos_v1_2.py`): `r_def` = 0 (código `00`, «entrevista completa») y `c_res` ∈ {1, 3}
(FD: 1 «Residente habitual», 3 «Nuevo residente»; excluye 2, no residente), `eda` de 15 a 98 (tope del
FD). Peso `fac_tri` (FD: «ponderador que permite obtener los resultados trimestrales»). Bootstrap de UPM
(`upm`) dentro de estrato (`est_d_tri`). Válido: peso > 0, estrato y UPM no vacíos (`M.prepara_diseno`).

## 2 · Conductas (por texto de pregunta / variable precodificada, FD tabla SDEMT)

| conducta | definición (texto del FD) | UNO | CERO |
|---|---|---|---|
| PARTICIPA-ECONOMICAMENTE | `Clase1` «Clasificación de la población en PEA y PNEA» (1 «Población económicamente activa» · 2 «Población no económicamente activa»), sobre 15+ | 1 | 2 |
| NO-ESTUDIA-NI-OCUPADO-18-24 | entre 18–24 años: `CS_P17` «¿...asiste actualmente a la escuela?» (1 Sí · 2 No · 9 No sabe) = 2, y `Clase2` «Clasificación de la población ocupada y desocupada; disponible y no disponible» (1 Ocupado · 2 Desocupado · 3 Disponible · 4 No disponible) ≠ 1 | `CS_P17`=2 y `Clase2`≠1 | `CS_P17`=1 (asiste) o `Clase2`=1 (ocupado) |
| MUJER-ENTRE-NO-ESTUDIA-NI-OCUPADO-18-24 | entre quienes cumplen la conducta anterior (derivada, no una pregunta): `SEX` «Sexo» (1/2) | 2 (mujer) | 1 (hombre) |

`CS_P17` = 9 («No sabe») y cualquier código fuera de {1,2} en `CS_P17`/`Clase2` quedan fuera de la
conducta NINI (no cuentan como 0 ni como 1): así lo hace `derivadas()` del medidor
(`joven & conocido`, con `conocido = CS_P17 ∈ {1,2} y Clase2 finito`). `MUJER-ENTRE-NO-ESTUDIA-NI-OCUPADO-18-24`
sólo tiene soporte donde la conducta NINI ya dio 1 (es un piso condicional, no un eje de la anterior).

**[TEXTO-DEL-MEDIDOR, NO-VERIFICADO-AQUÍ]:** ninguno — los tres textos de pregunta de §2 se verificaron
contra el FD `enoe_325_fd_c_bas_amp.pdf` en esta sesión.

## 3 · Ejes (uno a la vez)

TOTAL · SEXO (`sex`: 1 Hombre / 2 Mujer) · EDAD (`eda`, cinco tramos: 15-17, 18-24, 25-44, 45-64, 65+) ·
LOCALIDAD (`t_loc_tri`, cuatro tramos: 100MIL-MAS, 15MIL-99MIL, 2500-14999, MENOS-2500 — el FD trae los
códigos 1-4 sin la etiqueta textual en esta edición del documento; la convención de tamaño de localidad
es la estándar de ENOE ya usada en `tools/dominios/enoe/pisos_v1_2.py` y en `ENOE-PISOS-spec-v1_2.md`) ·
ESCOLARIDAD (`niv_ins`: 1 «Primaria incompleta» · 2 «Primaria completa» · 3 «Secundaria completa» · 4
«Medio superior y superior»; el FD trae un quinto código 5 «No especificado» que el medidor no mapea
—queda fuera del eje, no como categoría adicional) · ENTIDAD (`ent`, 01-32).

## 4 · Estimación

Razón ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato (UPM única del estrato = de certeza,
multiplicidad 1 en toda réplica), `PCG64(semilla)` (semilla del contrato de corrida, no fija en el
código), réplicas del contrato (`bootstrap_replicas`), bloques de 50, percentiles 2.5/97.5, contrato
conservador (una réplica degenerada → sin EE ni IC: `tools/dominios/salud/pisos_diseno.py::marginales`).
Receta común por sha256: `tools/dominios/salud/pisos_diseno.py` + motor
`tools/dominios/confianza/motor_pisos.py` (mismos módulos que el resto de la cola GEN2-COLA-COMPLETA-1,
importados como bytes desde `inputs["receta_pisos_salud"]`/`inputs["motor_pisos_confianza"]` — ambos
`INPUTS_REPO`, exigidos de origen repo por la guardia). Un eje a la vez; nunca cruces.

**Semilla y réplicas (para recalcular):** `numpy.PCG64(20261004)`, 2000 réplicas, bloques de 50; el valor ejecutable vive en `data/corrida0/CALC-ENOE-PARTICIPACION-2024T4-0001/spec.yaml` (`seed`, `parametros.bootstrap_replicas`) y es este mismo.

## 5 · Controles, secuencia

Sintético en `tests/test_cola_completa_pisos_gen2.py` (`test_enoe_participacion_conducto`): construye un
frame ENOE sintético con las 13 columnas de `columnas()`, corre `mide()` y verifica que
`NO-ESTUDIA-NI-OCUPADO-18-24 × EDAD × 45-64` sea `None` (fuera del rango 18-24, sin soporte en ese
cruce) y que el resultado pase el conducto de sellado (`corrida0._valida_outputs`, sin NaN/inf) con
`spec.yaml["resultados"]` exactamente igual a `esquema_resultados()`
(`test_spec_yaml_resultados_es_el_esquema`). `test_guardia_ola_reservada_o_excluida_para` prueba que un
input `enoe_2026_2t_csv` (2026T2, ola reservada) hace que `_guardia_inputs` levante `ParoDeGuardia`.
Ninguna ejecución diagnóstica sobre el dato: la primera corrida es `corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Escala y unidad:** proporciones de personas de 15+ (PARTICIPA-ECONOMICAMENTE) o de jóvenes de 18-24
(NO-ESTUDIA-NI-OCUPADO-18-24 y su derivada por sexo); ninguna se promedia con otra unidad ni con otro
trimestre. **Estructura ≠ cultura:** una `MUJER-ENTRE-NO-ESTUDIA-NI-OCUPADO-18-24` más alta que su
complemento de hombres no es «preferencia femenina por no trabajar ni estudiar»: la variable no captura
por qué (cuidado no remunerado, matrimonio temprano, falta de oferta laboral o educativa en la
localidad); leerla como estructura de oportunidades y de división del trabajo doméstico, no como rasgo.
**Evidencia:** (a) datos primarios en México (ENOE 2024T4, microdato). **Temporalidad:** RETROSPECTIVO;
un solo trimestre, sin IC de persistencia; ninguna cifra PROSPECTIVA. **Cifra escrita a mano:** ninguna
— toda constante de código (sha256, universo, semilla) sale del medidor o del descriptor.

El primer resultado que produzca este procedimiento es el que se reporta.
