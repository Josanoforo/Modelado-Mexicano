# Notas de cierre -- tools/extrae_l_v1_1.py (P2, A.13)

Corrida real sobre las 176 capturas `corridas-L/*-M-*.json`.

- OK -- 176 capturas examinadas (censo exhaustivo, A.13), 0 editadas.
- OK -- TSV escrito en forense/prereg-duelo-v2/L-extraido-v1_1.tsv
- Conteo NO-EXTRAIBLE por variante (A.13):
-   L-solo:    3 NO-EXTRAIBLE / 88 examinadas
-   L+corpus:  2 NO-EXTRAIBLE / 88 examinadas
-   total NO-EXTRAIBLE: 5 / 176

Ver regresión CIV-08 con `python3 tools/extrae_l_v1_1.py --regresion`.
Regresión sobre 8 capturas de piloto CIV-08 (A.13: 8 examinadas)
archivo                                      piloto  regla(x100)  regla_raw  coincide?
CIV-08__L-solo__01.json                        61.0         70.0     0.7000         NO
CIV-08__L-solo__02.json                        23.5         23.5     0.2350         SI
CIV-08__L-solo__03.json                        30.0         20.0     0.2000         NO
CIV-08__L-solo__04.json                        74.8         73.0     0.7300         NO
CIV-08__L-solo__05.json                        62.0         61.0     0.6100         NO
CIV-08__L-solo__06.json                        68.5         67.0     0.6700         NO
CIV-08__L-solo__07.json                        67.0         67.0     0.6700         SI
CIV-08__L-solo__08.json                        None         None                    SI

Coinciden (mismo NO-EXTRAIBLE, o mismo valor tras x100): 3/8
Divergen en valor: 5/8
Piloto NO-DISPONIBLE, regla SI extrae (o viceversa): 0/8

Declaración honesta de por qué NO se fuerza la coincidencia (encargo P2):
1. UNIDAD: el piloto guardó valor_extraido en escala porcentual sin dividir
   (61.0, 23.5), no en [0,1]. La regla congelada normaliza a [0,1] (regla-
   extraccion-L-v1_1.md paso 6) -- por eso la comparación de arriba multiplica
   por 100 antes de comparar, y el TSV real (P2, corrida sobre las 176) queda
   en [0,1], NO en la unidad del piloto.
2. CRITERIO DE SELECCION: el piloto (CIV-08 indice 1, valor 61.0) no tomó el
   primer número que aparece en el texto -- el primer número por posición ahí
   es el rango del reactivo específico ('67-73%', mercado), y el piloto en
   cambio eligió una cifra posterior, etiquetada por el propio texto como
   'dato público de INEGI' (más autoritativa) sobre la percepción general.
   La regla congelada de este acto NO pondera fuente/autoridad (regla paso 7,
   declarado explícitamente antes de correrla) -- toma el primer número por
   posición, sin ese juicio. Esta es la causa de la divergencia en el indice 1,
   no un error del extractor: es la consecuencia declarada de congelar una
   regla mecánica en vez de repetir el juicio humano/de modelo del piloto.
