Universo `N_TRA=01` y P7_3 válida; unidad trámite; proporción y residuo δ en escala logit; evidencia clase (a).

# ENCIG 2023/2021 · cruces históricos

## RESULT

`SELECCION-PENDIENTE-DE-DEFINICION`.

No se elige cruce ni se abre piloto 3. En 2023, sexo×edad y
edad×escolaridad sólo reconstruyen los marginales sellados cuando se añade un
residuo de 107 trámites (masa ponderada 571 754) cuya edad queda fuera de la
rejilla efectiva 18–96. La regla congelada exige parar esos cruces y pedir una
definición; no autoriza convertir 97/98/99 en 60+, eliminar el residuo ni
comparar puntajes sobre universos distintos. Sexo×escolaridad sí es coherente
y elegible, pero declararlo ganador por descarte violaría la regla aprobada.

El artefacto mecánico de selección es `02-seleccion.json`; consume exactamente:

- `CALC-ENCIG2023-CRUCES-HISTORICOS-0002`, sello
  `b0476ca5a461ee38fe545b69bf82b9ec8225103b283f6a9d4a48204932cb3772`.
- `CALC-ENCIG2021-CRUCES-HISTORICOS-0003`, sello
  `6c6b594d76f3a7ef79f10b391aa3296ed2f297ec025623003e9f5216124d2e4a`.

## Resumen de 2023

| Cruce | Celdas | n mínimo | Coherencia | Soporte | Puntaje | IC95 δ excluye 0 |
|---|---:|---:|---|---|---:|---:|
| sexo×edad | 8 | 1 644 | PARA: residuo edad | elegible | 0.7945 | 0 |
| sexo×escolaridad | 8 | 1 239 | coherente | elegible | 0.8708 | 1 |
| edad×escolaridad | 16 | 70 | PARA: residuo edad | no elegible | 2.1535 | 7 |

Los puntajes de cruces en PARA se publican como diagnóstico pero no ordenan
candidatos. Que siete celdas de edad×escolaridad tengan IC puntual que excluye
cero no rescata una rejilla no elegible ni constituye evidencia confirmatoria
independiente después de seleccionar entre celdas y cruces.

## Comparabilidad y 2021

Cuestionario y descriptor acreditan el mismo reactivo P7.3, códigos, tipo de
trámite, ponderador y categorías demográficas. Se construyó 2021 con el mismo
contrato conceptual: n universo/diseño 21 152, join demográfico sin faltantes.
Presenta el mismo problema estructural de edad: 104 trámites fuera de la
rejilla (masa 672 707). Por tanto 2021 no resuelve la incoherencia previa ni se
usa para inventar una ventaja por cobertura.

## Tablas y precisión

`tabla-celdas-2023.tsv` y `tabla-celdas-2021.tsv` publican, para las 32 celdas
de cada ola: trámites, personas, personas con/sin evento y solape, NUM/DEN
ponderados, p/EE/IC95, δ/EE/IC95, réplicas válidas y causa. `03-controles.tsv`
resume residuos, soporte, coherencia y señal por cruce.

Las 10 000 réplicas se regeneran exactamente a partir de los CALC sellados:
payload/hash, script blob, PCG64(20260919), orden canónico de UPM y regla de
singleton están en `ejecucion.json`, `spec.yaml` y el script. No se guardan
filas ni identificadores en Git. Este conjunto es el artefacto reproducible
equivalente para covarianzas/δ; una propagación posterior debe reejecutar el
mismo plan, no suponer independencia desde los EE publicados.

El selector ya no codifica IDs `0001` ni confía en sellos introducidos a mano:
deriva `spec_id` de cada `resultados.json`, exige que coincida con el directorio
y `spec.yaml`, verifica los tres hashes de `sello.json` y comprueba su hash
contra `sello.sha256`. Regenerado desde 2023-0002 y 2021-0003, produce bytes
idénticos a `02-seleccion.json`; una prueba de regresión exige esa igualdad.

El replay aislado de ambos CALC devuelve `RESULTADO=REPRODUCE` y
`CONTEXTO=DISTINTO` por `codigo_distinto`: el blob vigente contiene la
corrección posterior del selector, mientras los blobs y sellos congelados se
preservan. La salida estructurada está en `evidencia-replay-aislado.json` y
sus dos asientos vigentes en `forense/replay-evidencia.tsv`. La proyección
acotada publicó sólo 2 corridas y 1 156 RESULT propios (580 de 2023 y 576 de
2021); añadió cero usos y verificó como multiconjunto que ninguna fila ajena
cambiara.

Control independiente focalizado, 2023 sexo=1×escolaridad=superior: punto
ponderado `0.7343988774689564` y EE bootstrap `0.011701926247801479`; ambos
coinciden exactamente con el CALC sellado. El primer cálculo focal que omitía
UPM de dominio cero dio un EE distinto; se descartó porque no conservaba el
marco de diseño, tal como exige la spec.

## Lectura sustantiva

δ es un residuo descriptivo respecto de aditividad en logit, no una
interacción causal ni psicología de grupos. Edad y escolaridad pueden reflejar
acceso digital y alfabetización por cohorte. El universo excluye a quienes no
hicieron trámites y describe población con contacto institucional, no a toda
la población mexicana.

## CONSUMIDO

- `encig23_base_datos_csv` (`af733d…393d`).
- `encig2021_csv` (`c92ea3…c56a`).
- Cuestionarios y estructuras oficiales 2021/2023 citados en la spec.
- `CALC-PISOS-ENCIG2023-EJES-0002/resultados.json` (`bd13a9…8568`).
- Encargo y cuatro adjuntos archivados verbatim con hashes en `adjuntos/`.

## NO-CORRIDO / RESERVAS

- ENCIG 2025 y sus tres cruces: `RESERVADA`, no abiertos.
- Piloto 3, S½, Sλ, R y emisiones compuestas: no ejecutados.
- Selección final: pendiente de definición de mesa sobre la coherencia de la
  rejilla de edad; no equivale a `SIN-PODER-DE-FALSACION`.
- Adopción/consumo activo: ninguno; la publicación central no elige cruce.
