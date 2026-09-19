# Lectura ISSP México 2017 · redes de apoyo cotidiano

## Resultado

La corrida sellada usa 1,002 personas entrevistadas en México. `WEIGHT=1` en
todos los casos; por ello n y masa coinciden. La cobertura válida por ítem va de
99.20% a 99.70%. No se acreditaron UPM/estratos ejecutables: todos los puntos y
contrastes quedan rotulados `EE-IC-NO-DISPONIBLES-DISENO-NO-ACREDITADO` y no se
hacen afirmaciones de significación.

| Situación | n válido | Familiar cercano | Familiar lejano | Familia 1+2 | Amigo cercano | Ninguno | Familia: mujeres−hombres |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hogar o jardín | 999 | 59.36% | 5.61% | 64.96% | 15.92% | 3.00% | +8.71 pp |
| Hogar durante enfermedad | 999 | 76.48% | 8.11% | 84.58% | 9.11% | 0.70% | +2.50 pp |
| Hablar al sentirse deprimido | 995 | 53.97% | 6.03% | 60.00% | 29.25% | 3.32% | +4.51 pp |
| Consejo sobre problemas familiares | 997 | 44.53% | 7.62% | 52.16% | 35.11% | 3.21% | +1.59 pp |
| Ocasión social agradable | 994 | 56.64% | 5.84% | 62.47% | 24.85% | 2.41% | +6.65 pp |

El familiar cercano es la categoría individual más frecuente en las cinco
situaciones. La familia agregada alcanza su máximo ante enfermedad y su mínimo
para consejo sobre problemas familiares. La amistad ocupa el segundo lugar
individual en todas las situaciones y es especialmente visible en consejo
familiar y al hablar sobre ánimo deprimido. Esto distingue familia de amistad;
no repite la categoría combinada del CALC monetario Q8a.

Las mujeres muestran una proporción familiar mayor que los hombres en los cinco
ítems. La diferencia descriptiva es mayor para trabajo en hogar/jardín (+8.71
pp) y ocasión social (+6.65 pp), pero sin errores estándar ni intervalos no se
interpreta como diferencia estadísticamente estable ni como efecto de género.

## Ausencia declarada en las cinco situaciones

Hay 981 casos con las cinco respuestas válidas, 97.90% de las 1,002 personas
con peso utilizable. Sobre ese universo común:

- 901 (91.85%) no contestan “ninguno” en situación alguna;
- 80 (8.15%) contestan “ninguno” en al menos una;
- 56 (5.71%) lo hacen en exactamente una, 16 (1.63%) en dos, 6 (0.61%) en
  tres, 1 (0.10%) en cuatro y 1 (0.10%) en las cinco.

La mayor coocurrencia por pareja es ánimo deprimido + consejo sobre problemas
familiares: 14/981 (1.43%). Las demás parejas van de 0.20% a 0.92%. En este
universo, la ausencia declarada aparece con mayor frecuencia en una sola
situación que en varias, aunque existe un grupo pequeño con coocurrencia.
Desconocidos nunca se trataron como ceros.

## RESULT → significado y universo

- `RESULT-ISSP-REDES-Q7[a-e]-FAMILIA-TOTAL`: proporción de códigos 1+2 sobre
  respuestas válidas del ítem correspondiente, México total adulto.
- `RESULT-ISSP-REDES-Q7[a-e]-DELTA-FAMILIA-MUJERES-MENOS-HOMBRES`: resta de
  proporciones familiares, usando el denominador válido específico de cada
  sexo e ítem.
- `RESULT-ISSP-REDES-P3-COBERTURA-COMPLETOS`: masa de casos con cinco
  respuestas válidas / masa de las 1,002 personas con peso utilizable.
- `RESULT-ISSP-REDES-P3-ALGUNA-SITUACION-NINGUNO` y
  `...TODAS-SITUACIONES-NINGUNO`: proporciones sobre los 981 casos completos.
- Los siete `RESULT-...-SHA256` identifican byte a byte las tablas publicadas;
  `RESULT-...-N-MEXICO` identifica la muestra analizada y `RESULT-...-PRECISION`
  conserva la limitación de diseño.

## Qué aporta y qué no mide

Para `familismo_apoyo`, Q7 aporta granularidad situacional y separa familiar
cercano, familiar lejano y amigo cercano. Muestra que la familia declarada es
predominante, pero con intensidad distinta por necesidad y con una presencia
relevante de amistades en apoyo emocional y consejo. No autoriza llamar
“familismo” a todo apoyo ni trasladar las proporciones a una obligación
normativa.

La medición describe a quién acudirían primero. No observa ayuda recibida,
disponibilidad real, dinero, calidad del vínculo, obligación familiar, soledad,
aislamiento, depresión o capital social validado. Tampoco compara 2012 con 2017
como panel, calcula coeficientes del generador ni enlaza personas entre
encuestas.

Estado: **CONSUMIDO** `za6980_q_mx`, `za6980_backgroundvar_mx`,
`za6980_v2_0_0_dta`, `za6980_v2_0_0_sav` y evidencia integrada Q7.

**NO-CORRIDO / RESERVAS:** F6, M, L, HOLDOUT, piloto 3, ZA5900/ISSP 2012,
v26-v30, otros países, adopción y comparación predictiva. Contador/adopción:
`PENDIENTE-DE-MESA`.
