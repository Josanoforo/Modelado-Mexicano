# REGION-IC-PREDICTIVO · spec humana v1.0

El primer resultado que produzca este procedimiento es el que se reporta. Esta derivación consume exclusivamente RESULT regionales sellados, sin reabrir microdatos. R1 y R2 del 23/sep/2026 se heredan: 32 entidades de residencia ENVIPE y ENCIG, seis regiones oficiales ENIF, y solo puntos/IC publicados con n≥200 y varianza estimable. Conserva `adopta: NO`; toda evaluación es **RETROSPECTIVA**.

## Calendario y constructos

| Instrumento / constructo | Ajuste exclusivo | Piso → evaluación |
|---|---|---|
| ENVIPE, evasión de denuncia por delito | 2023→2024 | 2024→2025 |
| ENCIG, canal digital de luz por trámite | 2017→2019, 2019→2021, 2021→2023 | 2023→2025 |
| ENIF, ahorro informal cualquiera, persona 18–70 | 2018→2021 | 2021→2024 |

La codificación ENCIG 2025 viene del RESULT `adopta_encig2025_luz`; coincide con la serie histórica cotejada. La serie ENIF 18–70 no se mezcla con el portafolio 2024 18+. El complemento ENVIPE es el mismo evento invertido y no añade entrenamiento ni cobertura independiente. Cada fuente y el código quedan pinados por SHA en la spec ejecutable.

## Regla heredada y estado

Para cada geografía publicable en ambos extremos de una transición de ajuste, `Δ=logit(p_b)−logit(p_a)`. En cada instrumento, `τ²` es la media de los promedios de `Δ²` por transición; cada transición y cada geografía elegible dentro de ella tienen igual peso. Solo entran probabilidades e IC estrictamente interiores a (0,1), con IC ordenado y estado PUBLICABLE. Se congela `τ²` y el intervalo del piso **antes de leer** el RESULT de evaluación. `ee_m=(logit(IC_sup)−logit(IC_inf))/(2·1.959964)` y `IC_pred=expit(logit(p_piso)±1.959964·sqrt(ee_m²+τ²))`, regla de `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001` y `CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001`. Sin `τ²` o piso apto: `SIN-COMPARABILIDAD`, límites nulos. El dato posterior solo decide si el punto observado cae dentro del intervalo ya congelado.

La adaptación geográfica usa un único `τ²` por instrumento/constructo; no estima un parámetro independiente por entidad con una sola transición. Reportar los intervalos como **predictivos retrospectivos**, no como IC de diseño, prueba de cambio sostenido, validación prospectiva ni promesa de detección futura. La cobertura puntual entre geografías dependientes no tiene aquí IC por conglomerado defendible: solo una transición de evaluación por serie, y las entidades/regiones no son UPM intercambiables. Se publica el conteo descriptivo y el límite. No se aplica multiplicidad ni significación simultánea.

## Auditoría de rigor extremo

La escasez de transiciones de ENVIPE y ENIF vuelve `τ²` inestable; incluso ENCIG tiene solo tres transiciones de ajuste. La varianza de cambio entre olas no identifica causas culturales ni administrativas. Un punto fuera del IC predictivo no demuestra cambio sostenido. La representatividad estatal de ENVIPE/ENCIG no remueve sus límites de universo y ENIF permanece regional. `origen_numerico: HEREDADO`, `cuenta_gen2: NO`.
