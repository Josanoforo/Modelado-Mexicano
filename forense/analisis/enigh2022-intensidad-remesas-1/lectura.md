# ENIGH 2022 · monto e intensidad contable de remesas

**Estado: EJECUTADO y SELLADO; no INTEGRADO ni ADOPTADO.** La medición añade
la distribución de montos y el peso contable de las remesas entre receptores;
no cambia R5.1 ni convierte una sección transversal en evidencia causal.

## Resultado usable

| estadístico | estimación | IC95 de diseño |
|---|---:|---:|
| Media de remesas | **14,455.43 pesos** | descriptor sin IC |
| Mediana ponderada de remesas | **8,310.32 pesos** | descriptor sin IC |
| Participación media por hogar | **30.49%** | [29.44%, 31.53%] |
| Participación agregada (razón de masas) | **27.47%** | [26.19%, 28.85%] |
| Hogares con participación ≥50% | **24.15%** | [22.51%, 25.74%] |

Los montos están en **pesos de 2022 por trimestre normalizado**. El universo
contiene 90,102 hogares, masa expandida 37,560,123. Son receptores 5,208,
equivalentes a 1,716,276 hogares expandidos. La prevalencia resultante,
4.569409956%, replica exactamente `CALC-ENIGH-0001`; funciona sólo como
control positivo, no como resultado nuevo.

Los 5,208 receptores tuvieron `ing_cor>0`: el dominio de participación no
perdió hogares ni masa. Hubo cero ponderadores inválidos, remesas faltantes o
negativas, ingresos corrientes faltantes/no finitos, iguales a cero o
negativos, y cero casos donde `remesas` excediera `ing_cor` fuera de la
tolerancia de un centavo.

## Por qué las dos participaciones difieren

La participación media por hogar da a cada hogar su peso de expansión y luego
promedia `remesas/ing_cor`. La participación agregada suma primero 24,809.5
millones de pesos trimestrales de remesas y 90,318.9 millones de ingreso
corriente, y después divide las masas. La primera es **3.02 puntos
porcentuales** mayor: los hogares con menor ingreso corriente relativo pesan
más en la media de cocientes que en la razón de masas. Ninguna de las dos debe
sustituir a la otra.

La media mayor que la mediana también muestra una distribución de montos
asimétrica: el promedio está 74% por encima de la mediana. No se winsorizó ni
se crearon deciles o subgrupos después de observar el resultado.

## Incertidumbre y alcance

Los IC usan 2,000 réplicas PCG64, semilla 20260916, remuestreo de UPM dentro
de 560 estratos y 10,211 UPM. El remuestreo mantuvo los 90,102 hogares del
marco, con contribuciones cero fuera del dominio. No hubo filas sin diseño,
estratos con UPM única ni réplicas no estimables. Los montos se dejaron como
descriptores sin IC, según la prioridad fijada.

Esto describe participación contable entre hogares que reportaron remesas en
2022. No identifica dependencia causal, pérdida de ingreso si cesaran las
remesas, volatilidad, ausencia del Estado, respuesta a choques, aseguramiento
ni efecto protector. Tampoco constituye validación estadística independiente:
usa el mismo microdato que el cálculo de prevalencia.

## Decisión que habilita

Para una lectura descriptiva de `familia.seguro.volatilidad_ausencia_estado`,
mesa ya puede distinguir tres hechos: sólo 4.57% de hogares son receptores; en
ese grupo el hogar promedio registra 30.49% de su ingreso corriente como
remesas; y la masa total de remesas representa 27.47% de la masa de ingreso
corriente del mismo grupo. Estos datos habilitan contexto de magnitud, pero no
justifican mover el parámetro, tier o veredicto de R5.1.

## Inserción lista para el informe de familia

> ENIGH 2022 muestra que 4.57% de los hogares recibió remesas (control que
> replica la medición previa). Entre los hogares receptores, el monto mediano
> ponderado fue 8,310 pesos de 2022 por trimestre normalizado y el promedio,
> 14,455 pesos. Las remesas representaron en promedio 30.49% del ingreso
> corriente de cada hogar receptor (IC95 29.44%-31.53%), mientras la razón de
> las masas de remesas e ingreso fue 27.47% (IC95 26.19%-28.85%); 24.15% de
> esos hogares obtuvo al menos la mitad de su ingreso corriente de remesas
> (IC95 22.51%-25.74%). La diferencia entre 30.49% y 27.47% responde a
> estimandos distintos. Son participaciones contables transversales: no miden
> dependencia causal, pérdida contrafactual, volatilidad ni capacidad de
> aseguramiento familiar.

## CIERRE COMPARTIDO DIFERIDO

Después del trámite de Opus, mesa sólo necesita decidir si incorpora la
inserción descriptiva al informe de familia. Si la acepta, la integración
serial debe enlazar este CALC como derivación del mismo payload, conservar
`validacion_independiente=NO-HECHA` y propagar entonces los registros
compartidos que correspondan. Este acto no escribe decisiones, firmas,
hallazgos, estado, rótulos, tableros, contadores ni colas.
