# Pisos por segmento Encuesta Intercensal 2015 (tipo de hogar por sexo de la jefatura) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-COMPLETA-1`, 26/sep/2026, CAJA, rama `acto/gen2-cola-completa-1`,
0-bis `0d4ae74d`. Encargo: `forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md` (§1 (a), cola v1.1:
FAMILIA/ENOE — hogar y jefatura como huella de dominio FAMILIA/RURAL_INDIGENA con la Intercensal). CALC:
`CALC-EIC-HOGARES-2015-0001`. Congelada en el COMMIT-1, **antes** de leer un solo valor de la Intercensal
(sólo el descriptor de archivos `eic2015_fd.xls` y la línea de cabecera de `TR_VIVIENDA15.CSV`).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Payload `eic2015_nacional_csv` (manifiesto), sha256 `efcb4cb1…` COINCIDE; miembro
  `TR_VIVIENDA15.CSV` (uno de dos miembros del zip, el otro es `TR_PERSONA15.CSV`, no se lee). Descriptor:
  `eic2015_fd.xls` (formato de archivos INEGI, hoja `TR_Vivienda`, filas 434–455 — variables auxiliares
  84–87: `TAMLOC`, `TIPOHOG`, `JEFE_SEXO`, `JEFE_EDAD`).
- `[EJECUTADO]` Una sola ola del instrumento: la Encuesta Intercensal 2015 es exploratoria en el manifiesto
  (MAESTRA38-A1 Lote 3, sin regla previa). El Censo 2020 (CCPV, instrumento hermano, ola más reciente de la
  serie censal) es RESERVADO por E.6 y **no es input**; no se abre, no se cita ninguna cifra suya. Sin IC de
  persistencia (una sola ola en corpus).
- `[LEÍDO]` Cabecera de `TR_VIVIENDA15.CSV` (78 columnas) confirma que `TIPOHOG`, `JEFE_SEXO`, `TAMLOC`, `ENT`,
  `FACTOR`, `ESTRATO`, `UPM` existen tal como los usa el medidor; no se leyó ninguna fila de datos.

## 1 · Unidad, universo, diseño

Unidad: **VIVIENDA particular habitada con tipo de hogar registrado** (INEGI construye `TIPOHOG` y
`JEFE_SEXO` a nivel vivienda en `TR_VIVIENDA15`; no hay tabla de hogares separada en esta ola). Peso `FACTOR`
(FD var. 11, factor de expansión de la vivienda). Bootstrap de UPM `UPM` dentro de estrato `ESTRATO`. Válido:
peso > 0, estrato y UPM no vacíos (`M.prepara_diseno`).

Universo (denominador (a), el que usa el medidor para `universo=`): `TIPOHOG` ∈ {1, 2, 3, 5, 6} — todo hogar
con tipo conocido. Quedan fuera: 4 «Hogar no especificado (Familiar)» y 9 «No se sabe la composición»
(FD filas 444, 447). Denominador (b), declarado pero no aplicado como filtro adicional en el código —
se lee de la propia lista cerrada de conductas: **HOGAR-AMPLIADO-ENTRE-FAMILIARES** compara 2 contra {1, 3}
únicamente (excluye 5, 6 además de 4, 9), es decir, sólo dentro de los tres tipos familiares 1/2/3.

## 2 · Conductas (FD `eic2015_fd.xls`, hoja `TR_Vivienda`, variable 85 `TIPOHOG` filas 440–447; variable 86
`JEFE_SEXO` filas 448–450)

Catálogo de `TIPOHOG` (verificado contra el FD): 1 Hogar Nuclear (Familiar) · 2 Hogar Ampliado (Familiar) ·
3 Hogar Compuesto (Familiar) · 4 Hogar no especificado (Familiar) · 5 Hogar unipersonal (No familiar) ·
6 Hogar corresidente (No familiar) · 9 No se sabe la composición.

| conducta | pregunta / variable (FD) | UNO | CERO |
|---|---|---|---|
| HOGAR-AMPLIADO | `TIPOHOG` «Tipo de hogar» — hogar ampliado (familiar) | 2 | 1, 3, 5, 6 |
| HOGAR-NUCLEAR | `TIPOHOG` — hogar nuclear (familiar) | 1 | 2, 3, 5, 6 |
| HOGAR-UNIPERSONAL | `TIPOHOG` — hogar unipersonal (no familiar) | 5 | 1, 2, 3, 6 |
| HOGAR-AMPLIADO-ENTRE-FAMILIARES | `TIPOHOG` — hogar ampliado, sólo contra los otros dos tipos familiares (denominador (b): 1/2/3) | 2 | 1, 3 |

`TIPOHOG` 4 y 9 quedan fuera de las cuatro conductas (ni UNO ni CERO): universo declarado en §1. `TIPOHOG` no
trae texto de pregunta en el FD (es una variable construida por INEGI, no una pregunta literal del
cuestionario); el rótulo de cada categoría es el texto exacto del FD, citado arriba
`[TEXTO-DEL-MEDIDOR, NO-VERIFICADO-AQUÍ → verificado en esta spec contra el FD, ver arriba]`.

## 3 · Ejes (uno a la vez)

- **JEFATURA** (`JEFE_SEXO`, FD var. 86 «Sexo del jefe de la vivienda»): HOMBRE = 1, MUJER = 3. (El FD no trae
  código 2; el medidor usa exactamente {1} y {3}, que coincide con el catálogo — sin discrepancia.)
- **TAMLOC** (`TAMLOC`, FD var. 84 «Tamaño de localidad»): MENOS-2500 = 1 «Menos de 2 500 habitantes» ·
  2500-14999 = 2 «De 2 500 a 14 999 habitantes» · 15MIL-49999 = 3 «De 15 000 a 49 999 habitantes» ·
  50MIL-99999 = 4 «De 50 000 a 99 999 habitantes» · 100MIL-MAS = 5 «100 000 y más habitantes». Los cinco
  rótulos y códigos del medidor coinciden verbatim con el FD.
- **ENTIDAD** (`ENT`): 01–32, catálogo de entidades INEGI estándar; el medidor no trae nombres, sólo claves de
  dos dígitos — no se verifica nombre por entidad, sólo el rango 1–32 contra la cabecera (columna `ENT`
  presente).

TOTAL implícito (todos los ejes se corren también sin partición). Un eje a la vez; nunca cruces.

## 4 · Estimación

Razón ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato (`M.prepara_diseno` + `R.marginales`),
`PCG64(7)` — semilla tomada del `contrato["seed"]["valor"]` al momento de correr `corrida0 run` (no fijada en
esta spec: la fija el contrato de corrida, no el medidor ni esta spec), réplicas de `contrato["parametros"]
["bootstrap_replicas"]`, contrato conservador (una réplica degenerada → sin EE ni IC), como en las specs
hermanas de este acto. Receta común por sha256: `tools/dominios/salud/pisos_diseno.py` (`lee_csv_zip`,
`marginales`) + motor `tools/dominios/confianza/motor_pisos.py` (`prepara_diseno`, `mide_ola`,
`esquema_ola`). Un eje a la vez; nunca cruces.

Diagnóstico previo a la medición (filas `-G-`): `FILAS-LEIDAS` (todo el CSV), `FILAS-DISENO-VALIDO` (tras
`prepara_diseno`), `FILAS-TIPOHOG-CONOCIDO` (universo §1). Etiqueta de diseño `-G-DISENO` la deriva
`prepara_diseno` (`CONGLOMERADOS-ESTRATIFICADO`, esperado aquí por tener peso, estrato y UPM los tres).

**Semilla y réplicas (para recalcular):** `numpy.PCG64(20260929)`, 2000 réplicas, bloques de 50; el valor ejecutable vive en `data/corrida0/CALC-EIC-HOGARES-2015-0001/spec.yaml` (`seed`, `parametros.bootstrap_replicas`) y es este mismo.

## 5 · Controles, secuencia

Sintético en `tests/test_cola_completa_pisos_gen2.py::test_eic_hogares_conducto`: construye un frame sintético
(sin microdato real) con `TIPOHOG` U(1,9), `JEFE_SEXO` U(1,3), `TAMLOC` U(1,5), `ENT` U(1,32), peso/estrato/UPM
sintéticos, primeras 3 filas puestas a NaN (no respuesta); corre `m.mide(...)` y exige que
`HOGAR-AMPLIADO × JEFATURA=MUJER-N` sea > 0, y que el conducto (`corrida0._valida_outputs` vía `_cierra`) pase
sin NaN ni inf y con `resultados:` exactamente igual a `esquema_resultados()`. Este test no incluye una guardia
propia de ola reservada para el Censo 2020 (a diferencia de ENDISEG con su web 2022): la guardia general de
`_guardia_inputs` en el medidor (lista cerrada `INPUTS_REPO | {PAY}`) es la que para si un input extra —
incluido cualquier payload del Censo 2020 — se colara. Ninguna ejecución diagnóstica sobre el dato: la primera
corrida es `corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Escala y unidad:** proporciones de **viviendas** (no de personas ni de hogares en sentido estricto — INEGI
no separa vivienda de hogar en esta tabla; una vivienda puede alojar más de un hogar, pero `TR_VIVIENDA15` sólo
trae el tipo del hogar principal); ninguna cifra se promedia con la unidad PERSONA de otro CALC. **Estructura ≠
cultura:** la prevalencia de jefatura femenina o de hogares ampliados por tamaño de localidad o entidad refleja
composición demográfica, migración y mercado de vivienda (costo de vivienda independiente), no una preferencia
cultural regional por una forma de convivencia; ninguna lectura de este CALC atribuye la variación geográfica a
«cultura» sin controlar composición. **Firewall estructura↔atributo:** JEFATURA y TAMLOC son ejes de exposición
estructural (mercado de vivienda, empleo, migración), no un juicio sobre el hogar. **Evidencia:** (a) datos
primarios de INEGI en México (Encuesta Intercensal 2015, censo de muestra). **Temporalidad:** RETROSPECTIVO
(2015); ninguna cifra PROSPECTIVA; el Censo 2020 queda RESERVADO y fuera de este CALC, así que no hay lectura
de tendencia 2015→2020 en este procedimiento. **Cifra escrita a mano:** ninguna; toda constante numérica de
esta spec (códigos `TIPOHOG`/`JEFE_SEXO`/`TAMLOC`, rango `ENT`, ids de columnas) sale del medidor o del FD
citado en §0/§2/§3.

**Defecto potencial del medidor, reportado (no corregido aquí):** el docstring del medidor describe
`JEFE_SEXO` como código binario 1/3, lo cual el FD confirma exactamente (no hay código 2); no se encontró
ninguna discrepancia código↔catálogo en `TIPOHOG`, `JEFE_SEXO`, `TAMLOC` o `ENT` contra `eic2015_fd.xls`. La
única observación sin resolver es de forma, no de contenido: el docstring del medidor llama «hogar» a lo que
el FD documenta como atributo de la VIVIENDA (`TR_VIVIENDA15`, no una tabla `TR_HOGAR`); se deja declarado en
§1 y §6 de esta spec, no se cambia el medidor.

El primer resultado que produzca este procedimiento es el que se reporta.
