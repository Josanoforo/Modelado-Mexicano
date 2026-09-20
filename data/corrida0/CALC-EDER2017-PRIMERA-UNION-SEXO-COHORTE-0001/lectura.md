# Lectura · primera unión por sexo y cohorte

En las 18,689 personas con primera unión observada y ponderador válido, la
proporción de primera unión libre fue 48.10% (masa expandida 45,443,693):
47.59% en mujeres y 48.76% en hombres. No hubo sexo ni cohorte desconocidos,
2 casos quedaron sin clasificar (0.008% ponderado), no hubo primera
observación de disolución y no hubo empates incompatibles en el año mínimo.
La auditoría completa está en `tablas/resultados.json`.

Dentro de cada cohorte, la diferencia mujer−hombre de primera unión libre fue
−1.69 pp (≤1970; IC95 −5.81, 2.38), −1.80 pp (1971--80; −5.04, 1.40), −2.15
pp (1981--90; −5.52, 1.21) y −7.97 pp (1991+; −12.15, −4.02). La última es el
único contraste de cohorte cuyo IC no incluye cero.

En el universo común sexo×cohorte, la diferencia cruda es −1.16 pp (IC95
−3.13, 0.87). Los pesos de referencia conjuntos son 22.37%, 33.21%, 29.97% y
14.46% para las cuatro cohortes en orden. Con esa composición común, la
diferencia es −2.77 pp (IC95 −4.56, −0.92): estandarizar la composición cambia
la diferencia en −1.61 pp (IC95 −2.22, −0.97). Hay soporte en las ocho celdas,
por lo que no se redistribuyeron pesos.

Esto compara solamente a quienes ya tienen primera unión observada. Las
cohortes jóvenes han tenido menos tiempo para unirse, y la encuesta no cubre
a quienes fallecieron o salieron del marco. No identifica cambio causal,
riesgo de formar unión, efecto de sexo ni prevalencia conyugal actual.

| Alcance | Artefacto | Resultado / límite |
|---|---|---|
| Primera unión EDER | `tablas/perfiles.csv` | Libre/directo/residual por total, sexo, cohorte e intersección |
| Brechas y precisión | `tablas/contrastes.csv` | Bootstrap estratificado de 2,000 réplicas PCG64 |
| Composición común | `tablas/pesos_estandarizacion.csv` | Referencia conjunta, recalculada en réplicas |
| Diseño y enlaces | `tablas/resultados.json` | Singleton conservado; IC no garantizado |
