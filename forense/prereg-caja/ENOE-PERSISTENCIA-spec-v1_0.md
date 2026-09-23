# ENOE · persistencia descriptiva trimestral · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.
RETROSPECTIVA; adopta NO. `CALC-ENOE-PERSISTENCIA-0001` consume únicamente
`RESULT-ENOE-PISOS-TABLA` de `CALC-ENOE-PISOS-0003` con hash fijado en su
`spec.yaml`; no abre microdato. Método escrito antes de leer los valores de
ese RESULT. Medidor `tools/dominios/enoe/persistencia.py`, hash congelado.

Unidad: la celda `(era,conducta,eje,segmento)` de la spec ENOE-PISOS v1.1.
Ingreso mensual **nominal** excluido por no ser comparable entre trimestres
sin deflactor. Los otros 12 estimandos conservan unidad/denominador y se
evalúan separados por era: clásica, ENOEN, post-2023. Las cuatro olas
aisladas 2005/2008/2012/2014 tienen piso pero no pareja adyacente; 2020T2
no se interpola y no hay par 2020T1→2020T3. No se compara ENOEN 2022T4
con post-2023 2023T1 en esta versión.

Para cada destino `t` con ola `t−1` adyacente de la misma era y ambos puntos
definidos: pronóstico de persistencia `p̂_t=p_{t−1}`; error firmado
`p_t−p̂_t`; error absoluto; indicador descriptivo
`p_t∈IC95_diseño(p_{t−1})`. Ese IC **estima el punto de t−1**; su cobertura
del punto t no es cobertura predictiva ni prueba de cambio. Para un tercer
trimestre adyacente previo, se calcula también pronóstico de tendencia
`2 p_{t−1}−p_{t−2}`, acotado a [0,1] para proporciones, y su error absoluto.
El origen usa solo pasado; ninguna regla, amplitud o candidato se elige por
el resultado de la ola destino. No se agregan errores de celdas como ensayos
independientes: comparten personas, UPM y olas.

**IC predictivo calibrado: no estimable.** Un bootstrap separado de puntos
trimestrales no reproduce la dependencia de panel rotatorio: ~4/5 de la
muestra se solapa en trimestres contiguos, con reposición gradual durante
cinco visitas. El corpus no acredita peso longitudinal por persona ni réplica
conjunta entre olas. No se infiere una cola 95% de 9–16 transiciones por era.
Cada fila indica `SIN-COVARIANZA-LONGITUDINAL-PARA-CALIBRAR`; no se presenta
la cobertura descriptiva como validación o ajuste. Cualquier reconstrucción
de panel/intervalo posterior necesitaría CALC sucesor con llave, seguimiento,
ponderación y método congelados antes de hacerlo.

Salidas: un RESULT de texto JSON de filas agregadas por par de olas y dos
enteros de control (`PARES`, `SIN-IC-PREDICTIVO`). No contiene registros ni
identificadores individuales. Verify debe reproducir bytes numéricos dentro
de tolerancia declarada; un replay REAL recibe asiento en
`data/corrida0/replay-evidencia.tsv`.
