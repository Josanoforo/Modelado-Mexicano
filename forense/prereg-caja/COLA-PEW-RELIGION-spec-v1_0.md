# Pisos por segmento PEW Global Attitudes 2024 (afiliación religiosa, cambio de religión, creencia en Dios) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-COMPLETA-1`, 26/sep/2026, CAJA, rama `acto/gen2-cola-completa-1`,
0-bis `0d4ae74d`. Encargo: `forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md` (§1 (a), cola v1.1:
CONFIANZA / religiosidad vía PEW Global Attitudes, complemento del bloque RELIGIOSIDAD/CCPV). CALC:
`CALC-PEW-RELIGION-2024-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor de PEW 2024
(sólo el diccionario de variables/valores, el cuestionario y el topline — nunca el `.sav`/`.csv` de
microdato).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Payload `pew_gas_spring2024` (manifiesto), sha256 `1fb75a86…` COINCIDE. Miembro leído por
  el medidor: `Pew Research Center Global Attitudes Spring 2024 Dataset.sav` (`miembro_sufijo=".sav"`),
  filas `country` = 35 (México), vía `M.lee(..., pais=("country", 35))`. Descriptor: el zip trae también
  `Pew Research Center Global Attitudes Spring 2024 Data Dictionary.xlsx` (hojas `Variables`/`Values`),
  `...Questionnaire.pdf` y `...Topline.pdf`; se leyeron sólo estos tres para esta spec (ninguna fila de
  microdato).
- `[EJECUTADO]` Una sola ola abierta: el manifiesto trae también `pew_gas_spring2025`
  (`EXCLUIDOS_PREFIJO = ("pew_gas_spring2025",)` en el medidor, línea 24); ese payload es la ola más
  reciente del programa y **queda RESERVADA** (E.6) — no se abrió, no se listó su contenido, no se citó
  ninguna cifra suya. El medidor declara la guardia (`_guardia_inputs`) y el test
  (`tests/test_cola_completa_pisos_gen2.py::test_guardia_ola_reservada_o_excluida_para[...pew_gas_spring2025]`)
  prueba que PARA si ese payload entra como input.
- `[LEÍDO]` `religion_combined`, `religion_christian` y `religion_none` traen en el diccionario la
  advertencia **"NOT FOR POINT ESTIMATES. Only groups with sufficient sample size to report on
  separately are populated."** (Data Dictionary, hoja `Variables`, posiciones 210–212). El topline
  público (`...Topline.pdf`) no reporta ninguna de las tres, coherente con esa advertencia. El docstring
  del medidor ya declara esta advertencia y que el grupo católico en México sí está poblado; esta spec
  la mantiene: la cifra de CATOLICO/SIN-RELIGION es de este procedimiento, no la publicada por Pew.
- `[LEÍDO]` El diccionario no trae `estrato`/`upm` para el archivo público 2024 (ninguna variable de
  diseño más allá de `weight`); mismo tratamiento que ENDISEG/MMSI cuando falta diseño: bootstrap
  ponderado de entrevistas, «MAS-PONDERADO-SIN-ESTRATO» (`M.prepara_diseno(..., estrato=None,
  upm=None)`), cada entrevista su propia UPM.

## 1 · Unidad, universo, diseño

Unidad: **persona entrevistada en México, 18+** (filtro de universo del medidor: `age` entre 18 y 97
inclusive). Peso `weight` (Data Dictionary: `Weight`, escala). Sin estrato ni UPM en el archivo público:
bootstrap ponderado de individuos («MAS-PONDERADO-SIN-ESTRATO»). Válido para el diseño: peso finito > 0
(`M.prepara_diseno`); la validez de universo (18+) se aplica aparte, sobre el diseño ya válido.

**Códigos de no-respuesta de edad:** el cuestionario (`Q109a. What is your age?`, p. 41) documenta `97`
(«97 or older»), `98 Don't know` y `99 Refused`. El universo es `18 <= age <= 97`: 98 y 99 quedan fuera (corrección
hecha antes del COMMIT-1 al revisar esta spec contra el cuestionario; el borrador del medidor admitía hasta 110).

## 2 · Conductas (por Data Dictionary hojas `Variables`/`Values`; texto verificado contra cuestionario y apéndice A)

| conducta | variable y texto | UNO | CERO |
|---|---|---|---|
| CATOLICO | `religion_christian` — dict: «Q18b. Religion - Christians. NOT FOR POINT ESTIMATES…»; valor 1 = `Catholic` (Values: 1 Catholic · 2 Protestant · 3 Orthodox · 99 Everyone else). Derivada del medidor (`derivadas`): sobre filas con `religion_combined` en código válido (1–7, 99; Values: 1 Christian · 2 Muslim · 3 Jewish · 4 Buddhist · 5 Hindu · 6 Other · 7 Religiously unaffiliated · 99 Everyone else sin muestra suficiente), UNO si además `religion_christian` = 1. Verificado contra Apéndice A (México, Q18): código 1 del reactivo crudo `Roman Catholic` se filtra como «CHRISTIAN» y puebla `religion_christian`=1 (`Catholic`) [TEXTO-DEL-MEDIDOR verificado contra Appendix A] | `religion_christian`=1 sobre válido | válido y no (`religion_christian`=1) |
| SIN-RELIGION | `religion_combined` — dict: «Q18a. Religion - combined…»; valor 7 = `Religiously unaffiliated`. Derivada: sobre válido (1–7, 99), UNO si `religion_combined`=7 | 7 | 1–6, 99 (válido, ≠7) |
| CAMBIO-DE-RELIGION | `religion_switch` — dict: «Q21. Religion - Switching. Indicates whether a person belongs to a different religion than the one they were raised in as a child.» (Values: 1 `Switched religions between childhood and adulthood` · 2 `Did not switch`) | 1 | 2 |
| CREE-EN-DIOS | `god` — dict/cuestionario: **«Q27. Do you believe in God, or not?»** (`ASK ALL EXCEPT IN TUNISIA`; Values: 1 Yes · 2 No · 8 Don't know (DO NOT READ) · 9 Refused (DO NOT READ)) | 1 | 2 |

`religion_combined`/`religion_christian` no traen texto de pregunta localizado por país en el
cuestionario público (`Q18 CURRENT RELIGION: QUESTION WORDING… VARY BY SURVEY COUNTRY, REFER TO
APPENDIX A`): el Apéndice A sólo publica las categorías de respuesta por país (verificadas arriba), no
el enunciado exacto que leyó el entrevistador en México. El enunciado que trae el medidor (docstring) se
mantiene [TEXTO-DEL-MEDIDOR, NO-VERIFICADO-AQUÍ] para la redacción exacta de la pregunta; los **códigos**
1–99 sí quedan verificados contra Data Dictionary + Apéndice A. Códigos 8/9 (`god`) y cualquier código
fuera de 1–7/99 (`religion_combined`) quedan fuera por diseño (ni UNO ni CERO), como hace el medidor.

## 3 · Ejes (uno a la vez)

TOTAL · SEXO (`gender` — dict: «Q108. Gender of respondent» ASK ALL EXCEPT IN AUSTRALIA AND THE U.S.;
Values 1 Male · 2 Female) · EDAD (`age` — «Q109a. What is your age?»; cortes fijos del motor 18-29,
30-44, 45-59, 60-MAS — 98/99 fuera del universo, §1) · ESCOLARIDAD (`d_educ_mexico` — dict: «Q110MEX.
What is the highest level of school you have completed or the highest degree you have received?»;
Values 1 No formal education · 2 Incomplete primary · 3 Complete primary · 4 Incomplete secondary ·
5 Complete secondary · 6 General bachillerato · 7 Commercial career degree · 8 Technical career degree ·
9 Complete preparatory · 10 Complete universitary studies · 11 Master's degree · 12 Doctorate · 98/99
DK/Refused fuera). El medidor agrupa (`ESCOL`): HASTA-PRIMARIA 1–3 · SECUNDARIA 4–5 · MEDIA-SUPERIOR
6–9 (incluye las dos carreras técnica/comercial, códigos 7–8, junto con bachillerato general 6 y
preparatoria completa 9) · SUPERIOR 10–12. La agrupación 7–8 dentro de MEDIA-SUPERIOR es una lectura del
medidor (carrera técnica/comercial como pista de nivel medio superior en México, no universitaria); no
es un error de código (los valores 7 y 8 existen y están en ese rango), se declara como interpretación
del medidor, no de esta spec.

## 4 · Estimación

Razón ponderada Σw·y/Σw, bootstrap ponderado de entrevistas (sin UPM: cada fila su propia unidad de
remuestreo, `M.prepara_diseno(peso="weight", estrato=None, upm=None)`), `PCG64(semilla del contrato)`,
réplicas = `contrato["parametros"]["bootstrap_replicas"]`, bloques de 50, percentiles 2.5/97.5, contrato
conservador (una réplica degenerada → sin EE ni IC) — mismo motor y misma receta que ENDISEG/MMSI (§4 de
esas specs): `tools/dominios/salud/pisos_diseno.py` (`R`) + `tools/dominios/confianza/motor_pisos.py`
(`M`), ambos consumidos por sha256 como input `origen: repo` (`INPUTS_REPO = {"receta_pisos_salud",
"motor_pisos_confianza"}`), nunca importados por ruta viva. Un eje a la vez; nunca cruces.

**Semilla y réplicas (para recalcular):** `numpy.PCG64(20261002)`, 2000 réplicas, bloques de 50; el valor ejecutable vive en `data/corrida0/CALC-PEW-RELIGION-2024-0001/spec.yaml` (`seed`, `parametros.bootstrap_replicas`) y es este mismo.

## 5 · Controles, secuencia

Sintético en `tests/test_cola_completa_pisos_gen2.py::test_pew_religion_derivadas_y_conducto`: construye
un frame sintético (sin microdato real) con las columnas de `columnas()`, corre `m.mide(...)` y prueba
que el diseño sale `MAS-PONDERADO-SIN-ESTRATO`; luego `_cierra()` exige que
`corrida0._valida_outputs(...)` no marque ninguna fila mala contra `esquema_resultados()` (todas las
ramas terminales — con soporte, sin soporte, categoría vacía, fuera de universo, código de no
respuesta, peso faltante — pasan el conducto sin NaN/inf) y que `spec.yaml["resultados"]` sea
exactamente `esquema_resultados()`. `test_guardia_ola_reservada_o_excluida_para[...pew_gas_spring2025]`
prueba que `_guardia_inputs` lanza `ParoDeGuardia` si el payload 2025 (reservado) entra como input.
Ninguna ejecución diagnóstica sobre el dato real: la primera corrida es `corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Escala y unidad:** proporciones de personas entrevistadas en México, 18+ (población general vía panel
online/telefónico del programa, no censo); ninguna se promedia con otra unidad ni con otro país de la
ola. **Autorreporte de creencia y afiliación ≠ conducta religiosa observada:** afiliación declarada,
creencia en Dios y cambio de religión son respuestas de entrevista; no miden práctica (asistencia,
oración) ni intensidad. **Estructura ≠ cultura:** un gradiente de CATOLICO o CREE-EN-DIOS por
escolaridad o edad es primero composición social del panel (cohortes, urbanidad, acceso al medio de
levantamiento), no «secularización generacional» leída directo del corte transversal. **Advertencia
propia de Pew:** `religion_combined`/`religion_christian`/`religion_none` están rotuladas «NOT FOR POINT
ESTIMATES» por el propio productor (§0); esta spec estima de todos modos porque el grupo católico en
México está poblado, y lo declara: la cifra es de este procedimiento, no la publicada por Pew.
**Evidencia:** (a) datos primarios, país declarado (México, `country`=35) dentro de una ola
multinacional. **Temporalidad:** RETROSPECTIVO (levantamiento 2024); ninguna cifra PROSPECTIVA; sin IC
de persistencia (una sola ola abierta, E.6; 2025 reservada). **Cifra escrita a mano:** ninguna — la
única constante numérica de esta spec fuera del sha256 del payload y de los códigos de catálogo es el
corte de universo 18–97, que es del medidor (§1), citado, no inventado aquí.

El primer resultado que produzca este procedimiento es el que se reporta.
