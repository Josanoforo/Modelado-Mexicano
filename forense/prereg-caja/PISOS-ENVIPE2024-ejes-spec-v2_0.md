# PISOS ENVIPE 2024 por ejes · sucesor v2.0

El primer resultado que produzca este procedimiento es el que se reporta.

Prerregistro correctivo de `CALC-PISOS-ENVIPE2024-EJES-0001`. La exposición
histórica del cálculo defectuoso impide tratar esta corrida como piloto ciego.

- Unidad: delito; ponderador `FAC_DEL`; diseño `EST_DIS × UPM_DIS`.
- Evasión: universo `BP1_20 ∈ {1,2}`; caso = `BP1_20=2` y
  `BP1_23 ∈ {04,05,06,08}`.
- Denuncia: universo `BPCOD=01`, `BP1_20 ∈ {1,2}` y `BP2_1 ∈ {1,2}`;
  caso = `BP1_20=1`; eje de seguro por `BP2_1`.
- Ejes: sexo; edad 18–29, 30–44, 45–59, 60–96; escolaridad homologada;
  y dominio para evasión.
- IC95: 10 000 remuestras de UPM dentro de estrato, PCG64(42). Un único
  plan de réplicas se comparte por todas las celdas y desenlaces.
- Valores inválidos o ausentes se excluyen solo del eje afectado. Una celda
  sin soporte devuelve punto/IC nulos y conserva N, denominador y réplicas válidas.
