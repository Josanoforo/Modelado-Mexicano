# Cierre — distribución de horas de cuidado, ENUT 2024

## Resultado

Entre las 73,891 personas válidas (masa 107,537,532), CON_CP tiene mediana
de 0.58 y p90 de 35.18 horas semanales. El 10% superior de la masa de
personas acumula 59.14% de las horas declaradas. Al condicionar en las 39,837
personas participantes (masa 55,753,440), la mediana sube a 11.25 horas, el
p90 a 55.00 y el decil superior acumula 40.18% de las horas.

| variante/dominio | p25 | p50 | p75 | p90 | horas del 10% superior |
|---|---:|---:|---:|---:|---:|
| CON_CP · todas válidas | 0.00 | 0.58 | 12.00 | 35.18 | 59.14% |
| CON_CP · participantes | 4.00 | 11.25 | 28.00 | 55.00 | 40.18% |
| SIN_CP · todas válidas | 0.00 | 0.00 | 7.00 | 17.75 | 57.50% |
| SIN_CP · participantes | 3.00 | 7.00 | 15.17 | 27.42 | 37.64% |

La masa participante reproduce exactamente la participación del padre:
51.85% CON_CP y 48.90% SIN_CP. Que la concentración baje al excluir ceros
muestra que parte de lo que oculta la media es el margen de participación;
aun entre participantes, el decil superior acumula 40.18% de las horas
CON_CP. Esto describe una distribución concentrada, no desigualdad de
bienestar ni sobrecarga.

## Sexo y contrastes

| dominio CON_CP | sexo | p50 | p90 | horas del 10% superior |
|---|---|---:|---:|---:|
| todas válidas | hombres | 0.00 | 21.00 | 60.77% |
| todas válidas | mujeres | 2.00 | 48.33 | 54.05% |
| participantes | hombres | 7.75 | 34.67 | 39.66% |
| participantes | mujeres | 15.75 | 67.57 | 37.23% |

Las diferencias CON_CP mujer−hombre son +2.00 h en mediana (IC95
[1.83, 2.50]) y +27.33 h en p90 [25.83, 28.83] entre todas las válidas; entre
participantes son +8.00 h [7.42, 8.50] y +32.90 h [31.00, 34.98]. La mayor
media femenina observada por el padre convive así con más ceros entre hombres,
cuantiles femeninos mayores y concentración intragrupo algo menor entre
mujeres. No se infieren mecanismos de género.

SIN_CP−CON_CP reduce, para el total, la mediana en 0.58 h y el p90 en 17.43 h
entre todas las válidas; entre participantes reduce la mediana en 4.25 h y el
p90 en 27.58 h. La fracción del decil superior cambia −1.64 pp y −2.53 pp,
respectivamente. Todos estos IC95 excluyen cero. SIN_CP significa excluir
cuidados pasivos e incluir emocionales según el FD, no «cuidado activo».

## Cobertura, diseño y precisión

El archivo contiene 74,053 filas; el universo común conserva 73,891 y excluye
162 exclusivamente por edad 97/98, igual que el padre. No hay horas faltantes,
no numéricas, negativas ni sobre el máximo documental; tampoco peso o diseño
inválido. El plan se construyó desde las 74,053 filas con peso/diseño válidos:
342 estratos y 4,200 pares estrato–UPM, hash
`f9d796cc153b2aafff5b7f27aa27523397503ee287cca850a1b6f35f10f804dd`.
Ese conjunto coincide exactamente con el del universo válido del padre; no
hay estratos de UPM única.

Las 60 estimaciones y los 22 contrastes tienen 2,000/2,000 réplicas válidas.
Los IC de p25 CON_CP/SIN_CP, p50 SIN_CP en todas las válidas y p50 SIN_CP en
participantes colapsan en un valor por la masa discreta; se etiquetan como tal
y no como ausencia demostrada de error.

Cobertura ponderada de participantes: total 51.85%, hombres 47.46%, mujeres
55.66% para CON_CP; total 48.90%, hombres 44.25%, mujeres 52.94% para SIN_CP.
Las tablas procesables contienen también `n`, masa y cobertura no ponderada.

## Mapa RESULT → estimando / universo

| RESULT | estimando o artefacto | universo |
|---|---|---|
| `A-CON-TODAS-P50/P90/CONCENTRACION` | mediana, p90, fracción de horas del decil superior CON_CP | total de personas válidas, ceros incluidos |
| `A-CON-PARTICIPANTES-P50/P90/CONCENTRACION` | mismos tres estimandos CON_CP | total con CON_CP > 0 |
| `A-CON-BRECHA-TODAS-P50/P90` | mujer menos hombre, mismo plan de réplicas | personas válidas CON_CP |
| `G-N-MARCO/N-VALIDO-COMUN/MASA-VALIDA-COMUN` | tamaños y masa de control | archivo / universo común 12–96 |
| `G-N-ESTRATOS/N-UPM/N-ESTRATOS-UPM-UNICA/PARES-DISENO-SHA256` | identidad del diseño | marco con peso y claves válidos |
| `G-DISTRIBUCION-*` | 60 filas y hash de `enut2024-distribucion-horas-estimaciones.csv` | CON_CP/SIN_CP × 3 sexos × 2 dominios × 5 medidas |
| `G-CONTRASTES-*` | 22 filas y hash de `enut2024-distribucion-horas-contrastes.csv` | SIN−CON pareado y mujer−hombre CON_CP |
| `G-INCIDENCIAS*` | causas de exclusión y diseño | archivo completo |
| `G-INPUT-BD/FD-SHA256` | identidad de payloads | manifiesto/corpus |
| `G-SALIDA-*` | rutas reproducibles | artefactos deterministas del CALC |

Todos los nombres completos llevan el prefijo `RESULT-ENUTDH-` y sus valores
están en `resultados.json`; las tablas deterministas están ligadas por hash.

## Controles y pruebas

* Universo, masa, participación y medias CON_CP/SIN_CP coinciden con el padre
  (diferencias numéricas de redondeo menores a 2e−15).
* Los 4,200 pares estrato–UPM y su hash coinciden entre marco completo,
  universo nuevo y universo del padre.
* Un cálculo independiente agrupado por valor reprodujo los ocho cuantiles
  nacionales y las dos concentraciones nacionales a menos de 1e−15.
* Siete pruebas sintéticas cubren ceros/desconocidos, monotonía, empates y
  orden, cota [0,1], escalamiento, caso `[0,10]`, separación
  mediana/concentración y réplica focal pareada.
* `spec-check`: 14/14 variables OK; 317,718 filas de catálogo examinadas.
* `verify` y replay aislado: `REPRODUCE`, contexto `IDENTICO`, 26/26 RESULT y
  2/2 inputs; evidencia propia asentada en `forense/replay-evidencia.tsv`.
* Dos proyecciones canónicas consecutivas fueron estables: 228 corridas,
  8,955 RESULT y 228 usos; el CALC aparece con replay vigente y no crea uso.

## Integridad y reservas

Hashes: `distribucion.csv` = `fa9170a6…91776`; `contrastes.csv` =
`d944a754…02ad`; `incidencias.json` = `ba74686a…a4b8`; datos =
`25f35626…c4ba`; FD = `4a7dddf1…3f58`. La corrida original es
`CALC-ENUT2024-DISTRIBUCION-HORAS-0001--d3d53fe335bc`, ligada al COMMIT-1
`d3d53fe335bcb2fa98970d0ed59e21853a2be9bc` y sello
`9dbf88e8…c255`.

No se midieron edades, entidades, otros hogares ni 15A59; no se recortó a 168
ni se winsorizó. Las horas pueden superponerse. Contador, consumo y adopción
quedan `PENDIENTE-DE-MESA`.

El detalle de replay, asiento, conteos y hashes de las vistas está en
`replay-registro-enut2024-distribucion-horas.txt`. Los 8,817 avisos generales de proyección son deuda o
diagnósticos heredados; ninguno bloqueó la escritura propia. No se usó
verificación global ni `--lote`.

## Sucesión no numérica

La CI posterior al primer sello detectó cuatro colisiones de basename con el
padre. `CALC-ENUT2024-DISTRIBUCION-HORAS-0002` sucede al intento inicial sin
cambiar universo, seed, estimandos ni cifras; únicamente emite nombres
específicos. El primer `ejecucion.json`, `resultados.json`, sello y tablas se
conservan intactos en `CALC-...-0001` y en el commit `2f0954c`; las rutas
procesables vigentes son las del sucesor `0002`.
