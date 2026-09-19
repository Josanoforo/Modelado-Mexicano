# ENADID 2023 · unión actual por sexo y edad

## Resultado

`CALC-ENADID2023-UNION-SEXO-EDAD-0002` es la corrida aceptada. Mide situación
conyugal **actual**, no primera unión. El intento 0001 quedó no sellado por un
tipo registral incorrecto para diferencias con signo; el sucesor conservó el
método y corrigió sólo tipo e identidades RESULT.

Entre personas actualmente en unión libre o casadas, la proporción en unión
libre baja con la edad en ambos sexos. La comparación mujeres−hombres es
positiva a los 15–17, pero negativa desde 18–29 hasta 60+. El tramo 15–17 tiene
sólo 694 observaciones en el denominador y un intervalo más ancho.

| Edad | Hombre | Mujer | Mujer−hombre (IC95%) |
|---|---:|---:|---:|
| 15–17 | 88.57% | 96.71% | +8.15 pp [1.15, 15.15] |
| 18–29 | 71.32% | 68.95% | −2.37 pp [−3.39, −1.35] |
| 30–44 | 43.00% | 40.47% | −2.53 pp [−3.24, −1.82] |
| 45–59 | 25.04% | 22.68% | −2.36 pp [−3.03, −1.69] |
| 60+ | 14.24% | 10.58% | −3.66 pp [−4.26, −3.07] |
| 15+ bruto | 34.10% | 35.17% | +1.06 pp [0.85, 1.28] |

La distribución completa nacional muestra que el agregado por sexo mezcla
perfiles de edad y estados fuera de la unión actual. Las siete categorías
nativas permanecen separadas:

| P3_27 actual | Hombre | Mujer |
|---|---:|---:|
| Unión libre | 19.32% | 18.81% |
| Separada(o) de unión libre | 3.14% | 5.07% |
| Separada(o) de matrimonio | 2.23% | 3.54% |
| Divorciada(o) | 1.73% | 2.60% |
| Viuda(o) | 2.79% | 9.21% |
| Casada(o) | 37.34% | 34.68% |
| Soltera(o) | 33.44% | 26.08% |

El detalle sexo×edad de estas siete filas, con n, masas, EE e IC, está en
`distribucion.csv`. En las categorías centrales, la unión libre alcanza su
máximo en 30–44 para hombres (29.58%) y mujeres (28.22%); después cae mientras
el matrimonio actual gana peso. La viudez explica parte importante de la
diferencia en edades mayores y no se confunde con matrimonio ni con separación.

## Estandarización por edad

El estándar común estimado dentro del universo `SEXO∈{1,2}`, edad válida y
`P3_27∈{1,6}` asigna 0.46% a 15–17, 14.66% a 18–29, 33.52% a 30–44, 31.08% a
45–59 y 20.27% a 60+. Tasas y pesos se recalcularon en cada una de las 800
réplicas compartidas.

| Cantidad | Punto | IC95% |
|---|---:|---:|
| Tasa estandarizada, hombres | 35.95% | [35.43, 36.49] |
| Tasa estandarizada, mujeres | 33.32% | [32.81, 33.83] |
| Diferencia bruta mujer−hombre | +1.06 pp | [0.85, 1.28] |
| Diferencia estandarizada mujer−hombre | −2.63 pp | [−2.87, −2.40] |
| Bruta−estandarizada | +3.70 pp | [3.56, 3.83] |

Al fijar la composición de edad, el signo se invierte. Esto significa que la
composición etaria modifica materialmente la comparación descriptiva agregada;
la resta de 3.70 puntos porcentuales no es un efecto causal ni un porcentaje
explicado.

## Universo, filtros y residuos

TSDEM contiene 359,018 residentes y masa 129,477,554. Después del recorte a
edad válida 15+ quedan 276,849 y masa 99,982,443; sexo conocido y `P3_27`
válida no quitan casos adicionales. El denominador de unión actual contiene
152,834 personas y masa 54,989,025. Las categorías 2–5 y 7 quedan fuera de
ese denominador, no como desconocidas.

El control independiente separa las 82,169 filas fuera de los cinco tramos:
82,015 son menores de 15 (masa 29,435,905) y 154 tienen edad 999/no
especificada (masa 59,206). El campo histórico de `auditoria.json`
`edad_999_o_no_valida_n=82169` debe leerse como “fuera de los cinco tramos”;
su nombre es demasiado estrecho, pero el flujo y los resultados no cambian.
Hay cero sexo desconocido entre 15+, cero `P3_27` desconocida, cero peso
inválido y cero diseño faltante. Por eso las filas visibles de residuo de sexo
son `NO-ESTIMABLE:DENOMINADOR-NULO`; ningún producto solicitado queda bloqueado.

Diseño: 659 `EST_DIS`, 15,214 pares `EST_DIS`/`UPM_DIS`, 56 estratos
singleton, gl=14,555. El ajuste promedio singleton multiplica toda la matriz
de covarianza por 1.0928689884. No se usaron `ESTRATO`, `UPM`, `P3_27_AG`,
variables del módulo femenino ni enlaces.

## Controles

El control independiente usa `csv`/`numpy`/`scipy` y no importa el medidor.
Reconstruye todas las masas P1/P2 del padre por sexo más residuo: delta máximo
0. Revisa exhaustividad de las siete categorías (residuo máximo de
serialización 1.1e-12), pesos estándar (suma 1), el contraste 30–44 y la
estandarización completa. La diferencia máxima frente a punto/EE/IC publicados
es 4.55e-13. El hash del payload, la llave única y los parámetros de diseño
también coinciden.

## Mapa RESULT → universo

| RESULT | Universo / contenido |
|---|---|
| `RESULT-ENADID-USE2-P1-TABLA-SHA256` | Siete categorías por sexo×cinco edades y sexo total; residuo de sexo visible |
| `RESULT-ENADID-USE2-P2-TABLA-SHA256` | `P3_27=1 / P3_27∈{1,6}` por sexo×edad/total y diferencias mujer−hombre |
| `RESULT-ENADID-USE2-P3-TABLA-SHA256` | Sexo conocido, edad válida, `P3_27∈{1,6}`; pesos comunes, tasas, brechas y resta |
| `RESULT-ENADID-USE2-DIF-BRUTA-MH` | Diferencia mujer−hombre sin fijar composición de edad |
| `RESULT-ENADID-USE2-DIF-ESTANDAR-MH` | Diferencia mujer−hombre con los cinco pesos comunes estimados |
| `RESULT-ENADID-USE2-BRUTA-MENOS-ESTANDAR` | Diferencia bruta menos estandarizada; descriptiva, no causal |
| `RESULT-ENADID-USE2-FLUJO-SHA256` | N y masas antes/después de filtros |
| `RESULT-ENADID-USE2-AUDITORIA-SHA256` | Llave, residuos y marco de diseño |
| `RESULT-ENADID-USE2-REPLICAS` / `SEMILLA` | 800 / 20260919 |
| `RESULT-ENADID-USE2-SALIDA` | Directorio de las tablas |

Estado: medición sellada, replay aislado `REPRODUCE/IDENTICO`, validación
independiente terminada y asiento proyectado; adopción ninguna;
`cuenta_gen2=PENDIENTE-DE-MESA`. La segunda proyección fue estable byte a byte:
`corridas.tsv=38b6aa1123e1f5368e13089fe7a3a9b0a94f1440cf9425e6b6eaa78adccacbfb`,
`resultados.tsv=1598d495fa81861dc7f4ed03dd075d05a6653781c423f4121d46e98ab359ee51`
y `usos.tsv=939a06e39277a184490263b24cd86a537301cf0bed918271eba51c68e95ef1bd`.
Frente a `origin/main`, ninguna de las 223 corridas preexistentes cambió
`resultado_replay` ni `contexto_replay`, y `usos.tsv` no cambió. Las filas
derivadas ajenas que aparecieron al regenerar corresponden sólo a contratos ya
presentes de ENCIG e ISSP; no constituyen adopción nueva.

## NO-CORRIDO / RESERVAS

Ninguno. El residuo de sexo es nulo y por eso no tiene punto, sin impedir P1,
P2 o P3.
