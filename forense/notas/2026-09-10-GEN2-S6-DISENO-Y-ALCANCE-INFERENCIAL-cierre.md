# Cierre · GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL

La equivalencia estadística no está acreditada. Los puntos C1/C3/C4 se
conservan; sus IC y veredictos históricos se leen condicionados al bootstrap
por localidad, que queda como sensibilidad y no como varianza del diseño
oficial. R4.4 permanece `[MEDIA]` y no se crea un CALC sucesor.

| obligación | evidencia | cerrada/residual | siguiente acción |
|---|---|---|---|
| Contraste oficial | `ennvih1_muestra_diseno` (180 UPM, 3 estratos socioeconómicos), documentación de factores y FAQ; contraste completo en la nota principal | CERRADA: no hay equivalencia explícita ni aproximación admitida | reabrir sólo ante documentación nueva concreta del productor |
| Impacto C1/C3/C4 | tabla inicial de `2026-09-10-GEN2-S6-DISENO-Y-ALCANCE-INFERENCIAL-contraste.md`, trazada a `resultados.json` | CERRADA: puntos y alcance separados de la incertidumbre | consumidores preservan puntos y rotulan IC como sensibilidad |
| Enmienda sucesora | `S6-L16-spec-v1_5.md` + sidecar | CERRADA; históricos intactos | usar v1.5 para toda lectura prospectiva de S6 |
| Decisión de uso | `FP-372` | RESIDUAL DE MESA | elegir recomendación descriptiva+sensibilidad o diferir todo uso inferencial |
| Vía oficial | `NC-0156`; solicitud DIN existente, no enviada | RESIDUAL EXTERNO | titular decide enviar; si llega vía ejecutable, continuar en CAJA con spec previa |
| Avisos 12/13 | sección de consumidores en la nota principal | CERRADA COMO ENTREGA | integrar sólo en los actos dueños de esas rutas; no tocar snapshots ni vistas globales aquí |

Pruebas materiales: hashes oficiales y de v1.4 verificados; sidecar v1.5
`sha256sum -c` OK; tabla cotejada contra los RESULT JSON; YAML parseable;
`git diff --check`; `tests/check.py --baseline` verde frente al baseline (tres
FAIL históricos, ningún FAIL nuevo). La primera corrida del baseline detectó
la copia duplicada del encargo y la colisión nominal de la nota; ambas se
reconciliaron y la repetición quedó verde.

