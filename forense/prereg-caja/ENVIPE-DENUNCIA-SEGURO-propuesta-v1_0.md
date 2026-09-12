# Propuesta de especificación — denuncia condicionada a seguro

Estado: **PROPUESTA; NO FIRMADA; NO EJECUTAR NI ADOPTAR**

Necesidad: `NC-0088`

Elementos: `RES-0039`, `RES-0040`, `RES-0041`, `RES-0042`

## Elección pendiente

La apertura histórica documentada es estrecha: delito de robo total de
vehículo (`BPCOD=01`), estratificado por cobertura de seguro (`BP2_1`), con
denuncia/no denuncia observada en `BP1_20`. No mide motivos de no denuncia ni
una tasa general para todo delito.

Opción A — **estrecha descriptiva (recomendada)**

- fuente/ola: `envipe2025_csv`, ENVIPE 2025;
- unidad: delito;
- población: registros con `BPCOD=01` y respuesta válida de seguro y denuncia;
- capas: `BP2_1` define con/sin seguro; `BP1_20` define denuncia/no denuncia;
- ponderador: `FAC_DEL`;
- diseño: `EST_DIS` y `UPM_DIS`;
- estimandos: las dos probabilidades de denuncia por estrato de seguro y sus
  complementos exactos dentro del mismo estrato;
- propósito: describir la asociación seguro–denuncia en esa apertura, sin
  interpretación causal ni extrapolación a otros delitos.

Opción B — **definición nueva de motor**

Redefinir población, unidad, tratamiento de cobertura, desenlace y uso en el
motor. Esta opción requiere una decisión científica nueva y una spec distinta;
no puede heredar silenciosamente los cuatro valores legacy.

## Controles mínimos si se firma la opción A

El futuro medidor debe declarar negativos y faltantes, tamaños sin ponderar por
celda, sumas de pesos, puntos, EE e IC95 con el diseño indicado, particiones que
suman uno dentro de tolerancia, hashes de payload/spec/script y un replay
independiente. `tools/medidor_denuncia_seguro_envipe25.py` es cobertura técnica
localizada, no autoridad para correr ni adoptar.

La mesa debe firmar una opción antes de ejecutar. Este documento hace visible
la elección; no la toma.
