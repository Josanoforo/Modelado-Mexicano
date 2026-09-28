# Insuficiencias de la spec humana

Ninguna de ellas impidió calcular una llave. Son puntos que la spec no fijó y que se cerraron con una decisión registrada en `diagnostico.json` → `decisiones`.

## Todas las llaves (IC)

- **Receta de IC contradictoria entre documentos.** `spec-base-metodo.md` §4 remite a «la spec ENSANUT §4» y a «la receta común por sha256», que no vienen en el paquete, y fija `PCG64(20260924)` con «certeza para UPM única». La receta firmada (`residuales-p3-*`, R26) fija 20260923 y dice que el singleton se sortea a sí mismo. Se aplicó la receta firmada (D1). La firma R26 la subordina a un protocolo, FP-…-157c-01, cuyo texto no está en el paquete (solo su sha256). Tampoco están fijados el margen de equivalencia ni el control simultáneo («se fijarán por mesa»). El IC es, por tanto, solo de reproducibilidad diagnóstica: no certifica cobertura del 95 %.
- **Cadena opaca del estrato.** La receta pide ordenar por la «cadena opaca» de estrato y UPM, sin convertir a enteros. Pero `est_var` es numérico (double) en el `.dta`, así que no hay cadena original que conservar. La representación elegida (D3) fija el orden de los estratos y, con él, la secuencia del RNG.
- **Estado de IC con singleton.** La spec no dice si un IC con singleton va como `CALCULADO` o como `NO-IDENTIFICADA` (D2). No aplica aquí: el marco no tiene estratos singleton.
- **`hash_contrato` / `hash_entorno`.** No se define qué bytes se hashean (D14).

## Por conducta (punto)

- **ALCOHOL-12M, ALCOHOL-30D, ALCOHOL-EXCESIVO-12M, FUMA-ACTUAL**: no se fija qué regla gana si la respuesta directa y la regla de salto chocan (D4).
- **ALCOHOL-EXCESIVO-12M**: «resto → 0» es ambiguo para bebedores de 12 m sin `al11` y para personas sin `ds2` válido (D5).
- **FUMA-ACTUAL**: «sin dato» no aclara si incluye los códigos 7/9 de `tb02` (D6).
- **CONSULTO-PROFESIONAL-POR-CONSUMO**: «universo = a quien el cuestionario se lo preguntó». El filtro de pase del cuestionario no está descrito en la spec y no se leyó el PDF. En la práctica el universo es quien tiene `tp1` ∈ {1, 2}. El N se reporta en `diagnostico.json`.
- **CIGARRO-ELECTRONICO-ALGUNA-VEZ**: la regla «1 / 2» no dice si quien no fue preguntado (`tb50` nulo) debe valer 0. Se dejó fuera, sin imputar.
- **ESCOLARIDAD**: la spec no dice qué hacer con los códigos de `ds9` distintos de 1–9 y 99 (D8).
