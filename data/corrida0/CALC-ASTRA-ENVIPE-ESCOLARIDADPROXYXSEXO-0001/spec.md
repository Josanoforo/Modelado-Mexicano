# C-ASTRA ENVIPE 2025 · escolaridad_proxy × sexo · v1.0

Estado: procedimiento congelado antes del ajuste histórico y de cualquier lectura del cruce de evaluación.
El primer resultado que produzca este procedimiento es el que se reporta.

## Estimando y fuentes
Unidad DELITO; universo BP1_20 ∈ {1,2}; Y=1 si BP1_20=2 y BP1_23 ∈ {04,05,06,08}. Es la probabilidad conjunta en el universo, no la condicional a no denuncia. FAC_DEL pondera; EST_DIS estratifica; UPM_DIS es conglomerado. 2023 y 2024 son las únicas olas de ajuste. `envipe2023_csv` SHA 0dcc00a7fc37b79806f1bf1b85b12cd090b5ecc8e76983a3a1a861f2ef3fb404; `envipe2024_csv` SHA 90776b2fab6e3666dad1cb5f5f3eb7d6a7699dbfefd4f8f04f07fb01e61a6fb2; licencia INEGI Términos de Libre Uso. Los reactivos, códigos y filtros son los de `prereg-caja-ENVIPE-EVASION-NORMA` y del lector histórico con hash fijado; 2023/24 usan tmod_vic, y NIV se une desde tsdem por ID_PER única. Sexo y edad vienen de tmod_vic. Edad válida 18..96; otros códigos de eje quedan fuera solo de ese eje. Se cuentan vacíos de BP1_23 entre no denunciados y huérfanos del enlace, sin imputarlos. Ponderador positivo y estrato/UPM completos o PARO.

El único dato de 2025 es el segmento público sellado `tramite.evasion_norma_ejes_envipe2025` de `milpa/tramite-ola5-propuesta-v0.yaml` (SHA 93dfa3f9aab250dabf9cbe8c93ccef2012cb763c5367d023f24dbfbd867fbc8f) y el nacional sellado 0.562774. Se extrae solamente ese segmento; el cruce 2025 no se abre. Sus marginales son puntos condicionados, sin réplicas inventadas.

## Rejilla y procedimiento
8 celdas: (hasta primaria, 1 Hombre), (hasta primaria, 2 Mujer), (secundaria, 1 Hombre), (secundaria, 2 Mujer), (media superior, 1 Hombre), (media superior, 2 Mujer), (superior, 1 Hombre), (superior, 2 Mujer). Edad × dominio (NC-0328), escolaridad × dominio y resultados de pilotos anteriores se excluyen del ajuste.

`C2_2025(c)=expit(logit p25(a)+logit p25(b)-logit p25(nacional))`. Para t=2023,2024: `I_t(c)=logit p_t(a,b)-logit p_t(a)-logit p_t(b)+logit p_t(nacional)`. Cada p histórica es suma(FAC_DEL·Y)/suma(FAC_DEL). Una p en frontera se recorta a [1e-6,1-1e-6] antes de logit. Celda vacía en punto o réplica es NO-ESTIMABLE con causa; no elimina las otras celdas.

Modelo normal empírico: `theta24~N(0,tau²)`, `I23|theta24~N(theta24,v23+q)`, `I24|theta24~N(theta24,v24)`, `theta25|theta24~N(theta24,q)`. `v23/v24` son varianzas de 256 réplicas de UPM dentro de EST_DIS, comunes a todas las celdas y marginales de una ola, PCG64(20260922+t). Hiperparámetros por pooling entre celdas: `tau²=max(0,median_c(I23·I24))`; `q=max(0.0004,median_c((I24-I23)^2-v23-v24)/2)`. El mínimo de q regulariza la deriva no identificable por celda con solo dos olas. No hay búsqueda de variantes contra 2025. Media posterior normal por precisión; punto `expit(logit C2 + media posterior de theta24)`. Este ruido por celda y persistencia anual aporta algo distinto del λ fijo de C-ENCOGIDA. No garantiza preservar los marginales.

Intervalo predictivo 95%: 2048 sorteos PCG64(20260922), con índices de réplicas históricas compartidos entre celdas de la misma ola; tau² y q se recalculan en cada sorteo; posterior y evolución anual se simulan. Percentiles 2.5 y 97.5 de la probabilidad predicha. Incorpora ruido histórico, hiperparámetros y deriva temporal; condiciona los marginales 2025. No es IC de R y sus sorteos no se emparejan con las réplicas de R. El piloto conserva su criterio congelado.

Tolerancia replay absoluta 1e-10. Fallo de hash, ruta 2025 de evaluación, llave duplicada, diseño inválido o dependencia mutable detiene la corrida. Toda corrección sustantiva requiere versión nueva y declaración de exposición.
