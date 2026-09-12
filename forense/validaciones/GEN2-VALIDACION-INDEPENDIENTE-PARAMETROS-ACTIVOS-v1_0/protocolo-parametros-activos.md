# Protocolo v1.0 · validación independiente de parámetros activos

**Fijado:** 11 de septiembre de 2026, antes de ejecutar el contraste contra los
`resultados.json` productores.

## Perímetro y exposición previa

El perímetro se congela en las 16 entradas de
`forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_1.json` bajo
`salidas_gen2_directas`, snapshot efectivo posterior a la fusión de `#720`.
Son 16 consumidores, 16 `RESULT` distintos y seis `spec_id`, agrupados en cinco
payloads: ENCIG 2025, ENCUCI 2020, ENIF 2024, ENVIPE 2025 y ENIGH 2022.

No existe validación reutilizable por identidad exacta `(spec_id, resultado_id)`:
las 21 filas previas de `data/corrida0/validaciones-independientes.tsv` se
refieren exclusivamente a tres corridas `CALC-R-CIV-M-*`, no a estos 16
`RESULT`.

La ejecución **no es ciega**. El investigador ya leyó el snapshot, las specs y
los valores publicados. La independencia que se acredita es de implementación:
el ejecutable vecino se escribió desde las definiciones y fuentes originales;
no importa ni lee ningún `medidor.py` para producir los valores. Los
`resultados.json` productores se abren sólo después de completar autocontroles y
mediciones desde el corpus.

## Tabla de trabajo congelada

| familia | consumidores | RESULT | fuente | definición / transformación | trabajo |
|---|---:|---|---|---|---|
| ENVIPE | 1 | `RESULT-ENVIPE-DEN-P-C2-U4` | ENVIPE 2025 | persona con al menos un delito personal no denunciado en U1; máximo de `BP1_23∈{01,02,06,08}`; `FAC_ELE` | medir punto, n y masa; comprobar enlace |
| ENCUCI-A | 1 | `RESULT-ENCUCI-A-P-CUALQUIERA` | ENCUCI 2020 | persona con contacto, respuestas válidas; `AP5_17=1 OR AP5_18=1`; `FAC_SEL` | medir punto, n y masa; comprobar enlace |
| ENCUCI-B | 2 | `RESULT-ENCUCI-B-P-{URB,RUR}-AGR` | ENCUCI 2020 | persona, join único por `ID_PER`; protesta `AP7_3_5`, agravio `AP4_3_2=1`, urbano `{U,C}` o rural `{R}`; `FAC_SEL` | medir ambas celdas una vez por familia |
| ENIF-A | 2 | `RESULT-ENIF-AHO-A-P-CORTO-{SIN,CON}-P` | ENIF 2024 | persona, `P4_10∈{1,2}` sobre `1..5`, por `P3_13=7` o `P3_13∈{1..4}`; `FAC_PER` | medir celdas y masas |
| ENIF-B | 2 | `RESULT-ENIF-AHO-B-P-{FORMAL,INFORMAL}-P` | ENIF 2024 | persona; cualquier sí en `P5_6_*` o `P5_1_*`; denominador total con `FAC_PER` | medir ambos puntos; no forzar suma a uno |
| ENIF-C | 2 | `RESULT-ENIF-AHO-C-P-DESCONFIA-{CONOCE,NOCONOCE}-P` | ENIF 2024 | persona sin cuenta que responde `P5_20`; numerador `03`; eje `P5_23`; `FAC_PER` | medir celdas y masas |
| ENIF-población | 1 | `RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P` | ENIF 2024 | persona no trabajadora (`P3_8=8 OR P3_9=7`), `P4_10∈1..5`; corto `{1,2}`; `FAC_PER` | medir junto con las otras ENIF |
| ENCIG-A | 1 | `RESULT-ENCIG-MOR-A-P-SOL1` | ENCIG 2025 | persona urbana 18+; `P8_3_1=1` sobre `{1,2}`; `FAC_P18` | medir punto, n y masa |
| ENCIG-B | 2 | `RESULT-ENCIG-MOR-B-P-{PRE,DIG}-SD` | ENCIG 2025 | evento de trámite sin deduplicar; join `ID_TRA`; `P8_4=1` por canal presencial `1` o digital `{3,4,5}`; `FAC_TRA` | conservar multiplicidad y medir celdas |
| ENCIG-C | 1 | `RESULT-ENCIG-MOR-C-P-ADOPTA` | ENCIG 2025 | trámite de luz `N_TRA=01`; canal `{4,5}` frente a `{1,2,6}`; `FAC_TRA` | medir punto, n y masa |
| ENIGH | 1 | `RESULT-B-ENIGH-2022-P` | ENIGH-NC 2022 | hogar de `concentradohogar`; `remesas>0`; `factor` | medir punto, n y hogares expandidos |

Los complementos que consumen el motor no forman parte de las 16 salidas
directas. Cuando existen, se acreditan por el padre y la transformación, no se
cuentan como otra medición independiente.

## Fuentes originales e identidad

El ejecutable exige los siguientes SHA-256 antes de medir:

| payload | SHA-256 |
|---|---|
| `encig25_base_datos_csv.zip` | `47daf2f732366ad842b7f60c784be9d61db68a00ae1a693980ec6a683e0d9e12` |
| `BD_ENCUCI2020_dbf.zip` | `0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283` |
| `enif_2024_bd_csv.zip` | `00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` |
| `envipe2025_csv.zip` | `8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa` |
| `enigh2022_nc_csv.zip` | `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06` |

También se verifican los documentos primarios leídos: estructura ENCIG
`09e1b19b…e623a2`, descriptor ENCUCI `6cd6f747…475638`, descriptor ENIF
`17e2ad86…db2`, cuestionario ENIF `32e37cc1…f8b`, descriptor ENVIPE
`83fe0246…77fad` y cuestionario de módulo ENVIPE `21df3861…16d27`.

Esos originales confirman población/unidad y los reactivos decisivos: ENCIG
declara `FAC_P18` para persona y `FAC_TRA` para trámites; ENCUCI declara
`FAC_SEL`, solicitud 5.17, entrega 5.18, agravio 4.3.2 y protesta 7.3.5; ENIF
declara `FAC_PER` y los códigos de actividad, horizonte y ahorro; ENVIPE enruta
delitos `05..15` a 1.23 tras `BP1_20=2`; ENIGH define `remesas` en el
concentrado a nivel hogar.

## Llaves, multiplicidad, no respuesta y aritmética

- Las llaves son texto opaco. `ID_PER` debe ser único en las tablas de persona
  usadas para joins; `ID_TRA` debe ser único en ENCIG sección 8, pero se conserva
  su multiplicidad en sección 7 para la rama `SD`.
- Blanco, `b`, no numérico y los códigos de no respuesta quedan fuera cuando la
  definición exige una respuesta válida. Nunca se convierten a cero.
- Los factores deben ser finitos y estrictamente positivos.
- Numerador y denominador se acumulan como `Decimal` a partir del texto de la
  fuente. El punto es `Σw·y / Σw`.
- Se conserva por cantidad `n`, numerador y denominador, además de contadores de
  exclusión y filas leídas por fuente.

## Tolerancias y alcance del veredicto

Para los productores que conservan precisión completa, el punto pasa con
`|delta| ≤ 1e-12`. Los siete puntos ENIF se publican deliberadamente a seis
decimales; para ellos se fija **antes del contraste** `|delta| ≤ 5e-7`, media
unidad del último decimal publicado. Conteos y masas declaradas comparan de
forma exacta.

`PASA` acredita identidad de fuente, población, unidad, codificación,
ponderador, transformación, punto y enlace al consumidor. No acredita
incertidumbre de diseño, causalidad, independencia de muestra ni una nueva
medición del contador científico. Ningún EE/IC se compara en este acto.

## Autocontroles anteriores al productor

El ejecutable aborta antes de abrir cualquier `resultados.json` si no pasan:

1. pesos `1` y `3`, desenlaces `1` y `0` → punto `0.25`;
2. peso nulo, negativo, infinito, blanco y código no integral se rechazan;
3. un join con llave repetida en el lado consumidor conserva dos eventos;
4. el lector DBF sintético respeta cabecera, anchos, selección de campos y
   registros borrados;
5. la carga del snapshot resuelve exactamente 16 pares consumidor/RESULT sin
   duplicados.
