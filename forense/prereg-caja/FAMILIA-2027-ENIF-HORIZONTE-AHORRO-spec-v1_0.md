# FAMILIA-2027-ENIF-HORIZONTE-AHORRO · spec humana condicional v1.0

**Estado: CONDICIONAL, NO LISTA PARA FIRMA DE APERTURA.** El nombre 2027 es un identificador de carpeta, no una fecha publicada. Consultado el calendario INEGI 2026 el 23/sep/2026; fecha oficial de publicación de ENIF 2027: **NO-CONFIRMADA**. No se abre dato futuro con este borrador.

## Estimando cerrado y piso

- Instrumento/ola objetivo: ENIF 2027; levantamiento y publicación: NO-CONFIRMADOS. Antes de firmar, mesa coteja cuestionario futuro, FD, pesos, población y periodicidad con la ola 2024.
- Estimando único: horizonte de ahorro por ambas vías bajo la definición HVD. Unidad de observación: **persona**; escala del punto **proporción [0,1]**. No se agregan otros estimandos tras observar R.
- Piso congelado en este borrador: `RESULT-HVD-A-AMBAS-VIAS` de `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` (ola 2024); SHA-256 de `sello.json`: `1c8b329fb2088d24298acb3081e9bb2d2366dce05c6e238d282271d251d92609`. Su valor se lee del RESULT, no se transcribe como parámetro de producto. Si una ola intermedia cambia la identidad, esta spec se declara NO-ELEGIBLE; no se sustituye el piso a posteriori.

## Regla futura de evaluación del piso

El ejecutor futuro congela en COMMIT-1 la spec YAML, el medidor efectivo, los códigos, el marco de bootstrap UPM dentro de estrato y el universo elegible **antes de leer** la nueva ola. El primer resultado que produzca el procedimiento es el que se reporta, incluso adverso o NO-ESTIMABLE. Habrá un solo acceso de evaluación a R para lo sellado a tiempo; una regla añadida después de R no entra. Reserva de la nueva ola por canal de adquisición; solo la levanta el código congelado o decisión escrita de mesa.

Métrica primaria de piso: error absoluto en puntos porcentuales entre el punto histórico fijo y el R futuro del mismo estimando, además del indicador de si R cae en el IC histórico si ese IC tiene calibración acreditada. El IC de incertidumbre para el error se obtendrá de réplicas del R futuro con el piso fijo, con unidad y regla de soporte idénticas. No hay segundo contendiente: **ΔMAE, victoria frente a otro modelo y B-bis de superioridad = NO-APLICABLE**. Vocabulario cerrado para el piso: `CALIBRADO`, `SUBCOBERTURA`, `NO-ESTIMABLE`, `NO-COMPARABLE`. Se informa también el error como magnitud continua; no se elige un umbral después de R.

## Condiciones para firma

1. Fecha oficial de publicación de ENIF 2027 dentro de la ventana 23/sep/2026–23/mar/2028 y texto de cuestionario futuro aún pendientes.
2. Umbral material, soporte mínimo, tratamiento de faltantes y regla de comparabilidad por cambio de reactivo deben fijarse por mesa antes de COMMIT-1. No se hereda automáticamente el 0.5 pp de otras evaluaciones.
3. Precisión/potencia de la regla de piso: **NO-CALCULABLE** desde este RESULT puntual. Faltan el vector histórico de réplicas emparejadas, n efectivo y varianza de diseño de la diferencia para fijar efecto mínimo detectable, α y potencia objetivo. No se reconstruye varianza desde extremos de IC.
4. Resultado si el futuro falsador no refuta: conservar el piso solo para el estimando, unidad, ola y tolerancia sellados; nunca concluir persistencia general de conducta ni detectar cambios entre olas.

Fuente de selección: catálogo U1, commit `0ac21b6c`, contrastado aquí con RESULT y sello del CALC. Comparte apertura de ENIF 2027 con otras familias de ese instrumento, sin consumir R más de una vez.
