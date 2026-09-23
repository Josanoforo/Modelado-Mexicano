# REGION-ENVIPE2025-DENUNCIA-U4 · spec humana v1.0

El primer resultado que produzca este procedimiento es el que se reporta. ENVIPE 2025, delitos personales del año de referencia, personas víctimas `ID_PER` como unidad final U4, 32 entidades de **residencia** de `TPER_VIC2`; no entidad de ocurrencia. R1/R2 de mesa: dominio estatal admitido, publicar punto e IC solo con n no ponderado del denominador ≥200, varianza estimable y requisito oficial más estricto; conservar supresiones con cifras nulas. `adopta: NO`, **RETROSPECTIVA**.

La codificación y unidad son las de `CALC-ENVIPE-0001/spec.md` y la firma de mesa FP-391 para `RES-0027`/`RES-0028`. En `TMOD_VIC`: delitos personales `BPCOD∈{05..15}`, `BP1_20=2` (no denunciados), razón principal `BP1_23∈{01..08}`. Colapsar por `ID_PER` con máximo de la clase C2 `BP1_23∈{01,02,06,08}`; el denominador U4 es persona con al menos un delito de ese universo, no delito. `denuncia_con_miedo_o_desconfianza` es esa tasa; `denuncia_por_otra_razon` es el complemento **solo dentro del U4 recortado**. `09`, `99` y blanco quedan fuera, sin imputarlos. La conducta complementaria no afirma exhaustividad del cuestionario. La unidad, códigos, denominador y factor `FAC_ELE` son los del RESULT consumidor `RESULT-ENVIPE-DEN-P-C2-U4`, no los de `FAC_DEL`.

`TPER_VIC2` aporta `CVE_ENT`, `FAC_ELE`, `EST_DIS`, `UPM_DIS`; `ID_PER` debe ser único y todo ID del universo debe enlazar. Los dos desenlaces se estiman sobre el diseño completo con réplicas de UPM dentro de estrato compartidas, 1 000, semilla PCG64 `20260923`, IC percentil, n y Kish. Se pinan código, adaptador, estadística y función compartida por SHA. Los RESULT `-JSON` conservan réplicas conjuntas sin ID ni pesos individuales. El control positivo nacional posterior compara la razón U4 con el RESULT sellado, sin copiarlo al estimador.

## Auditoría de rigor extremo

«Otra razón» es complemento del recorte U4, no frecuencia de todas las demás respuestas reales. Una persona con varios delitos cuenta una vez mediante máximo; cambiar a delito altera el estimando. El marco y el instrumento no justifican atribución causal, cultural ni predicción futura por estado de residencia.
