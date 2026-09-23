# C-ASTRA ENCIG 2025 · escolaridad×sexo · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

Rige exactamente el contrato de modelo, fuentes, resultados, incertidumbre, guardia, fallos y exposición de `ASTRA-ENCIG-EDADXSEXO-spec-v1_0.md`, congelado en el mismo commit, con estas sustituciones explícitas: `B25=logit p25(escolaridad)+logit p25(sexo)-logit p25(nacional)`; `d_t` usa escolaridad×sexo; hay ocho celdas `{hasta primaria, secundaria, media superior, superior}×{1 hombre,2 mujer}`. `NIV` se agrega {00,01,02} → hasta primaria; {03} → secundaria; {04,05,06,07} → media superior; {08,09} → superior. La documentación oficial y los CALC históricos sellados constan en la spec de cruces históricos. El bloque de marginales 2025 publicado declara cobertura 1.000000 tanto para sexo como para escolaridad; los dos ejes y el nacional pertenecen al mismo universo de trámites válidos. Se exige verificar concordancia de celdas con la spec del piloto antes de declarar admisión.

La misma familia normal usa `τ=0.15`, `ω=0.10`, dos olas 2021/2023, nivel 95%, límites en logit con constante 1.959963984540054 y ninguna semilla ni selección posterior. La exposición histórica de esta sesión incluye los residuos 2021/2023 ya sellados; no incluye el cruce 2025. No se importan resultados ni código ENVIPE.
