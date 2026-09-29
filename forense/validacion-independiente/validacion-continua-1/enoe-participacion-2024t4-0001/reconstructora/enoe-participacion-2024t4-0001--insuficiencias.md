# Insuficiencias de la spec humana

Las 136 llaves tienen punto e IC calculados. Ninguna llave queda como `NO-RECALCULABLE-DESDE-SPEC` ni como `BLOQUEADO-POR-ACCESO`: las 13 columnas autorizadas alcanzan para el método. Lo que sigue es lo que la spec no fija. Afecta **el IC95 de las 136 llaves** (el punto no depende de esto) y cada punto se resolvió con una decisión registrada en `diagnostico.json` → `decisiones`:

1. **Diseño del bootstrap (todas las llaves, IC):** la spec no dice si se sacan n_h o n_h−1 UPM por estrato, ni si los pesos se reescalan (Rao-Wu u otro). Tampoco dice cómo se identifica la UPM cuando un mismo `upm` aparece en varios estratos; eso pasa con 532 UPM en el universo válido (D2, D3).
2. **Secuencia de números aleatorios (todas las llaves, IC):** la spec fija PCG64(20261004), 2000 réplicas y bloques de 50. No fija el orden de consumo del generador (estratos, UPM, llamada por bloque), así que los extremos del IC no se pueden reproducir bit a bit contra otra implementación (D4).
3. **Interpolación de percentiles (todas las llaves, IC):** no se especifica. Se usa la lineal de numpy (D5).
4. **Definición de "réplica degenerada" (todas las llaves, IC):** no se define. Aquí es denominador cero o razón no finita, y no se presentó en ninguna llave (D6).
5. **NINI, frase sobre Clase2 (grupos NO-ESTUDIA-NI-OCUPADO-18-24 y MUJER-ENTRE-…):** "fuera de {1,2} en CS_P17/Clase2" contradice la tabla de §2 y "Clase2 finito". Se siguió la tabla. Con estos datos no cambia nada, porque Clase2 ∈ {1..4} en el universo (D7).
6. **MUJER-ENTRE-NO-ESTUDIA-NI-OCUPADO-18-24 × SEXO (2 llaves):** la spec no dice si este cruce es trivial o si se suprime. Se reporta 0 (HOMBRE) y 1 (MUJER), con IC degenerado en el punto (D8).
7. **Codificación del CSV:** no se declara. Se leyó como latin-1 (D1).
