# Auditoría de cobertura y potencia · informe v1.3

Corte 23/sep/2026. `python3 forense/analisis/informe-v1_3/audita_sellados.py`
recorre **siete CALC de comparación y sus 16 inputs RESULT sellados**, verifica
el hash de los 23 `sello.json` y de cada miembro cubierto y escribe
`auditoria-sellados.tsv`. Se inspeccionaron también `spec.yaml`,
`ejecucion.json`, scripts sellados y los archivos adicionales de cada
directorio. Los 23 `resultados.json` solo conservan escalares: ningún vector
de réplicas emparejadas de ΔMAE. `RESULT-ENIGHDM-POR-OLA-JSON` y
`RESULT-ENIGHDM-RESUMEN-JSON` son tablas textuales, no vectores de réplicas.
No se abrió ni se reejecutó el árbitro R.

| Comparación | Cobertura identificable desde RESULT sellados | Variación de Δ y límite |
|---|---|---|
| Lote ENIF 2024, R2/C2 | R dentro del IC del candidato R2: 39/44 = 0.8864, Wilson descriptivo [0.7602, 0.9505]; `RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-R2-COBERTURA-R-EN-IC-CAND-{FRAC,N}`. | ΔMAE e IC sellados; falta vector de Δ por réplica para varianza y potencia exacta. |
| Piloto 3 ENCIG 2025, S-LAMBDA/C2 | El CALC guarda IC de R por celda, no una serie de cobertura prospectiva de R por IC del retador. | **Sí** guarda EE de ΔMAE = 0.4393525156518415 pp y 10 000 réplicas válidas (`RESULT-GOB-EXE15-ADJ-2025-S-LAMBDA-DELTA-MAE-{EE,B-VALIDAS}`). Varianza escalar = 0.19303063300960166 pp². Falta vector emparejado y distribución de los 15 veredictos para potencia exacta del criterio conjunto. |
| Duelo ENIGH 2024, C-PISO/C-TS | Un punto nacional; `RESULT-ENIGHADJ-CPISO-R-DENTRO-IC-CAND=NO` y C-TS también `NO`. 0/1 no estima cobertura. | Sin EE ni réplicas de Δ; falta incertidumbre conjunta de los dos errores. |
| Duelo ENVIPE 2026, SL/C2 | R dentro del IC de C2: SXD 9/12, EXD 10/12; 19/24 = 0.7917, Wilson descriptivo [0.5953, 0.9076]. SL da SXD 8/12 y EXD 11/12, también 19/24; se mantienen separados por cruce. | Δ e IC por cruce, sin EE ni vector de Δ. |
| Piloto 4 ENVIPE 2025, C-ENCOGIDA/C2 | `G-COBERTURA-CRUCE` mide **cobertura de registros del cruce**, no cobertura de IC. No convertirlo en aciertos predictivos. | EE de R por celda, 10 000 réplicas declaradas en el procedimiento, pero ninguna varianza ni vector de ΔMAE por cruce; falta covarianza entre celdas. |
| Cierre ENCIG 2025, C-ASTRA/C2 | `G-COBERTURA-C-ASTRA-K/N` = 8/8 en edad×sexo y 8/8 en escolaridad×sexo; 16/16 = 1.000, Wilson descriptivo [0.8064, 1.000]. | EE de R y conteos de réplicas por celda; sin vector/EE de ΔMAE por cruce. |
| Crédito K1, ORO12 | Doce celdas elegibles de oro; no se archiva cobertura R dentro de IC de predicción para este bloque como tasa comparable. | Δ, IC y dictamen sellados; sin vector/EE de Δ. |

**Cálculo identificable de potencia, solo como aproximación normal de
planificación.** Con α bilateral = 0.05, diferencia objetivo δ = 0.5 pp y
σ = EE de ΔMAE sellado, la probabilidad de rechazar cero bajo una normal
con varianza fija es
`Φ(δ/σ − 1.95996398454) + Φ(−δ/σ − 1.95996398454)`.
Para S-LAMBDA del piloto 3 da **0.20653**. El segundo retador S-MEDIO
conserva EE = 0.33030599021950924 pp, varianza 0.10910204717489053 pp²,
y la misma operación da **0.32798**. Esto cuantifica únicamente la prueba
bilateral de Δ contra cero bajo esa aproximación; no es potencia del
dictamen de victoria, que además exige 12/15 celdas, ni potencia empírica
validada por el diseño de conglomerados.

Para una potencia conjunta de los demás casos falta exactamente la serie
sellada de **diferencias pareadas por réplica** de piso menos candidato,
con claves de celda/cruce, multiplicidades de UPM dentro de estrato y
covarianza entre celdas; con ella se repetiría el adjudicador completo bajo
efectos prospectivamente declarados y se contaría la fracción que supera
signo, umbral y regla de celdas. Ni los extremos de IC ni los conteos
`B-VALIDAS` contienen esa covarianza. El n efectivo del diseño, si se quiere
proyectar tamaño muestral a otra ola, también requiere sus pesos y efecto de
diseño sellados. No se reconstruyen réplicas desde extremos de IC ni se
reabre R.
