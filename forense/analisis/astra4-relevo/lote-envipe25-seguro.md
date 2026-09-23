# ASTRA4-U2 · lote ENVIPE 2025, denuncia según seguro

23/sep/2026. Cuatro filas afines `RES-0039/0040/0041/0042`. La spec humana
`forense/prereg-caja/ENVIPE-DENUNCIA-SEGURO-spec-v1_0.md`, su YAML y
medidor quedaron congelados y ejecutados en el acto anterior; no se reabre
R ni se cambia el procedimiento para mejorar el resultado. Se consume el
CALC sellado `CALC-ENVIPE-DENUNCIA-SEGURO-0001` como evidencia, no como
adopción. `sello.json` coincide con sidecar SHA-256
`7126e2b09ef4bfb8fedceeabc12d3e94c1b9395ccd0216fc88050e31635af7a7`;
`forense/replay-evidencia.tsv` registra `CONTEXTO=IDENTICO` y
`RESULTADO=REPRODUCE` (19/sep/2026). Ese replay confirma la corrida GEN2,
no que reproduzca los literales GEN1.

| Fila | RESULT exacto | GEN2 | GEN1 | Diferencia GEN2−GEN1 |
|---|---|---:|---:|---:|
| `RES-0039` con seguro, denuncia | `RESULT-ENVIPE-SEG-CON-P-DENUNCIA` | 0.7909064453831163 | 0.790900 | +0.000006445 |
| `RES-0040` con seguro, no denuncia | `RESULT-ENVIPE-SEG-CON-P-NO-DENUNCIA` | 0.20909355461688375 | 0.209100 | −0.000006445 |
| `RES-0041` sin seguro, denuncia | `RESULT-ENVIPE-SEG-SIN-P-DENUNCIA` | 0.6720144369290082 | 0.672000 | +0.000014437 |
| `RES-0042` sin seguro, no denuncia | `RESULT-ENVIPE-SEG-SIN-P-NO-DENUNCIA` | 0.3279855630709918 | 0.328000 | −0.000014437 |

**Correspondencia:** ENVIPE 2025, payload `envipe2025_csv`, unidad delito,
robo total de vehículo `BPCOD=01`, `BP2_1=1/2` para seguro y `BP1_20=1/2`
para denuncia, peso `FAC_DEL`; los complementos se contaron en el mismo
estrato. La corrección sellada al prereg de denuncia general fija `CORR-0007`
para estas cuatro filas. El otro `CALC-ENVIPE-0001` no mide esta condición.

**Dictamen:** `RESULT-ENVIPE-SEG-REPRODUCE-GEN1=NO-REPRODUCE`, porque las
cuatro diferencias rebasan la tolerancia predeclarada `1e-6` en proporción.
`RESULT-ENVIPE-SEG-ADOPCION=LISTADO-PARA-MESA-NO-REPRODUCE`.
`cuenta_gen2=PENDIENTE-DE-MESA`; no hay pin ni escritor aplicado a estas
cuatro conductas. Su lectura efectiva sigue LEGACY-GEN1. Una firma de mesa
debe decidir si adopta la nueva medición pese a la diferencia, con objeto
exacto, antes de preparar el diff del escritor de `milpa/tramite.yaml`;
ninguna tolerancia se relaja retrospectivamente. El contrato de ese escritor
requiere el valor previo exacto, identidad de universo/escala y replay.
