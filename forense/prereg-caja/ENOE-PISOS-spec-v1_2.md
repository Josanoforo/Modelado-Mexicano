# ENOE pisos trimestrales · spec v1.2

**El primer resultado que produzca este procedimiento es el que se reporta.**
Acto ASTRA5-U1-TRABAJO-ENOE, `CALC-ENOE-PISOS-0003`. RETROSPECTIVA.
U0: `8f7e8de0`, tres filas cerradas; copia byte idéntica
`forense/analisis/dominios/enoe/U0-corte-consumido.tsv` (SHA-256
`fb7a0385b70278cff5c84ecaf3abb6b44fdc4a0e21ae1fdb832f4f03e81a79ac`).
Las otras conductas se fijan por el mandato específico y el descriptor oficial,
no por mirar resultados. Medidor efectivo:
`tools/dominios/enoe/pisos_v1_2.py`, importado por shim con hash verificado antes
de abrir la primera ola. Versiones: Python 3.14.4, pandas 2.3.3,
numpy 2.3.5, PyYAML 6.0.3. Prueba sintética antes del freeze:
`tests/test_astra5_enoe_sintetico.py`.

## Insumos y matriz previa

`data/enoe-olas-elegibles-preparacion-v1_0.tsv` identifica 43 paquetes únicos
por año/trimestre; `data/enoe-reactivos-olas-v1_0.tsv` fija 13 conductas × 43
olas (559 filas), texto/código/universo/era. Todos los ids de microdato van
en `spec.yaml` con hash del manifiesto. Se abre **solo SDEM** de cada ZIP;
COE básico/ampliado y FD se leyeron documentalmente para justificar las
variables precodificadas. `/microdatos/` prevalece sobre `/datosabiertos/`
cuando hay duplicado. 2026T1 no es input: los dos ids siguen reservados en el
manifiesto. INEGI lista 2026T2 como último publicado al corte, ausente del
corpus. No se mira ese tabulado.

## Unidad, códigos y denominadores

Unidad **persona de 15–98 años**, aun en los paquetes antiguos con mínimo
original menor; `R_DEF=00`, `C_RES∈{1,3}`, ponderador positivo, `EST_D` y
`UPM` presentes. ENOE clásica usa `FAC`/`EST_D`; ENOEN y post-2023 usan
`FAC_TRI`/`EST_D_TRI`. El instrumento documenta SDEM como capa de
preclasificación del cuestionario de ocupación y empleo; los códigos no son
rasgos psicológicos. Los blancos no son valores observados; donde el propio
precódigo define pertenencia por código 1, el resto de ocupados válidos es 0.

| Conducta | Reactivo o precódigo | Denominador | Punto y unidad |
| --- | --- | --- | --- |
| empleo_informal | `EMP_PPAL=1` informal; 2 formal | `CLASE2=1`, `EMP_PPAL∈{1,2}` | proporción |
| sector_informal | `TUE_PPAL=1` sector informal; 2 fuera, blanco formal | todos los ocupados `CLASE2=1` | proporción |
| subocupacion | `SUB_O=1` sí subocupado | todos los ocupados | proporción |
| busca_otro_trabajo | `BUSQUEDA=1` busca adicional; 2 no | ocupados con 1/2 | proporción |
| pluriempleo | sección VII; `T_TRA=2` dos trabajos; 1 uno | ocupados con 1/2 | proporción |
| sin_contrato_escrito | COE `P3i` contrato por escrito; derivada `TIP_CON=5` sin; 1–4 con; 6 no especificado | `REMUNE2C∈{1,2}` y `TIP_CON∈{1,…,5}`, ocupado | proporción |
| jornada_mas_50_horas | COE `P5b` horas semana pasada; `HRSOCUP>50` | ocupado con `HRSOCUP∈[1,168]` | proporción |
| desocupacion | `CLASE2=2` | PEA `CLASE1=1` | proporción |
| desaliento_desistio | `PNEA_EST=1` disponible que desistió | PNEA clasificada 1–6 | proporción |
| desaliento_sin_posibilidades | `PNEA_EST=2` no busca por considerar que no hay posibilidades | PNEA clasificada 1–6 | proporción |
| no_participacion_obligaciones | `PNEA_EST=4` otras obligaciones | PNEA clasificada 1–6 | proporción |
| horas_ocupado | `HRSOCUP∈[1,168]` | ocupados con horas válidas | media semanal |
| ingreso_ocupado_nominal | COE `P6b`/`INGOCUP∈[1,999998]` | ocupados con ingreso mensual positivo válido | media nominal, pesos/mes |

`PNEA_EST=4` **no se rotula cuidados**: el código no distingue el cuidado de
otras obligaciones. Cuidado específico queda `NO-ESTIMABLE-CON-SDEM` en el
cierre; requeriría COE P2G2, texto/códigos y saltos por era. Ningún silencio
se cuenta como desaliento. `TUE_PPAL` no se usa como sinónimo de empleo
informal. No se usa el descriptor «trabajo riesgoso» para aversión al riesgo.

`HRSOCUP` es la clasificación oficial de horas de trabajo de la semana,
incluidas las categorías válidas para varios trabajos según su precódigo;
ocupados ausentes sin 1–168 horas salen del denominador de jornada y media.
No se imputa cero. `INGOCUP` es ingreso mensual nominal; cero, blanco, `999999`
y fuera de [1,999998] no se imputan. **No se deflacta**: no hay deflactor
oficial con id y hash en este contrato. Su media es descripción de cada ola,
sin comparación de poder de compra entre trimestres ni calibración de ingreso
real. Media no se cambia por mediana tras ver el resultado.

## Ejes, soporte y diseño

Se estiman cortes **univariados**: nacional; sexo `SEX` 1/2; edad 15–29,
30–44, 45–59, 60+; escolaridad oficial `NIV_INS` 1 primaria incompleta,
2 primaria completa, 3 secundaria, 4 medio superior y superior; tamaño de
localidad `T_LOC` 1/2/3/4; entidad `ENT` 01–32. No hay cruces ni resultados
municipales. El rótulo de escolaridad 4 preserva la categoría oficial y no
separa superior de media superior. Una categoría faltante solo sale de su eje.

Punto `Σw·y/Σw`; IC95 percentil con **200 réplicas** de UPM con reemplazo
dentro de estrato, semilla `PCG64(42+i_ola)`. Un plan por ola compartido en
todas sus celdas, y UPM sin miembros de un dominio se conservan con subtotal
cero. Se conserva `n`, `n_efectivo_kish=(Σw)²/Σw²`, número de UPM y calidad
por CV de réplicas: ALTA `<15%`, MODERADA `15–<30%`, BAJA `≥30%` o punto 0.
Se suprime punto e IC cuando `n<100`, `n_efectivo_kish<100`, menos de 2 UPM
en el dominio o menos de 95% réplicas válidas. `n_efectivo_kish` es diagnóstico
de pesos, no reemplaza el diseño: UPM y CV se reportan por separado.

## Serie y límites fijados antes del dato

Las 43 olas conservan periodicidad trimestral con huecos reales: tres cortes
documentales 2005/2008/2012/2014; tramo continuo 2016T1–2020T1; hueco
2020T2 (ETOE, no ENOE); ENOEN 2020T3–2022T4; post-2023. La misma columna
no autoriza comparar como serie homogénea a través del cambio de modo.
No se interpola. Ingreso nominal no se contrasta temporalmente. La tabla de
puntos e IC de diseño es el piso transversal de cada ola elegible.

Transición formal/informal **NO IDENTIFICADA CON ESTOS INSUMOS**: el panel
rotatorio de cinco visitas existe, pero los pesos publicados son transversales;
no hay ponderador longitudinal por persona ni attrition acreditada para el
enlace de hogares/personas. No se empareja por edad/sexo ni se restan
prevalencias para simular entradas/salidas.

Persistencia temporal se evaluará solo dentro de eras y con olas trimestrales
adyacentes, origen móvil, sin ola destino en el ajuste. La comparación de
puntos de prevalencia se describe como retrospectiva. **No se emite IC
predictivo calibrado** sin réplica conjunta que preserve el solapamiento del
panel entre trimestres; los IC del CALC son de diseño **dentro** de cada ola.
El estado de calibración de esta versión es
`SIN-COVARIANZA-LONGITUDINAL-PARA-CALIBRAR`. No hay prueba de cambio entre
olas ni adjudicación causal.

La salida principal es un RESULT `texto` JSON de filas agregadas, sin
identificadores individuales, cada una con `ola,era,conducta,eje,segmento,
unidad,punto,ic95_lo,ic95_hi,n,n_efectivo_kish,upm,calidad`. La vista TSV
posterior añade `RESULT-ENOE-PISOS-TABLA`, CALC y hash del sello a **cada
fila** sin alterar el resultado. Si una columna de conducta falta, solo esa
conducta/ola queda `NO-ESTIMABLE-COLUMNA-AUSENTE`; si faltan llave, peso o
estrato, la corrida aborta antes de sellar y se conserva el diagnóstico.

## Enmienda v1.1 antes de su ejecución

`CALC-ENOE-PISOS-0001` (COMMIT-1 `6c28ac24`) realizó su primera llamada a
`run` y **falló sin producir RESULT ni sello** al llegar a 2022T2:
`ValueError: 2022T2: faltan columnas obligatorias ['r_def']`. Su log
íntegro está en `forense/analisis/dominios/enoe/run-v1_0-fallo.log`, SHA256
`ba03bb420b70df48a651db3ca71bcdd308d0171b072a4ca357768860337bc8e0`.
El diagnóstico de cabecera, sin leer valores, mostró BOM UTF-8 en esa ola;
el lector latin-1 convirtió `r_def` en `ï»¿r_def`. Además, todas las olas
ENOEN/post-2023 llaman `t_loc_tri` a la clasificación trimestral de localidad,
que v1.0 omitía. El sucesor v1.1 **solo** detecta BOM y elige UTF-8-sig para
esa cabecera, y usa `t_loc_tri` si existe, `t_loc` si no. Ninguna definición
de conducta, denominador, eje, supresión, semilla o ponderador cambia.
La prueba `tests/test_astra5_enoe_v1_1.py` construye el encabezado fallido
y comprueba la localidad antes de congelar esta versión. El código v1.0 y
su spec permanecen intactos. El primer resultado que produzca **v1.1** es
el que se reporta.

## Enmienda v1.2 antes de su ejecución

`CALC-ENOE-PISOS-0002` (COMMIT-1 `83f5dd03`) ejecutó hasta 2025T3 y
**falló sin RESULT ni sello**: `ValueError: 2025T3: faltan columnas
obligatorias ['ent']`. Log íntegro `forense/analisis/dominios/enoe/run-v1_1-fallo.log`,
SHA256 `9f522a8e5baadf7ccd4dc767422723cec36584fca09e88fe684b0398c05b6ee6`.
Los 43 encabezados, solo estructura, muestran que 2025T3/T4 sustituyen `ent`
por `cve_ent`; ninguna otra ola pierde una columna obligatoria. V1.2 mapea
`cve_ent` a la **misma entidad de dos dígitos** donde `ent` no existe.
Se probó con CSV sintético `tests/test_astra5_enoe_v1_2.py` antes de este
freeze. No cambia estimando, semilla, n, réplicas, ni códigos de conducta.
Las versiones v1.0 y v1.1 quedan intactas, con ambos fallos registrados.
El primer resultado que produzca **v1.2** es el que se reporta.
