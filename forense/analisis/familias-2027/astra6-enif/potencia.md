# Potencia y utilidad de las dos pruebas ENIF

EJECUTADO: análisis generado desde `RESULT-FAMILIA-ENIF-ORO-POTENCIA` de `CALC-FAMILIA-2027-ENIF-ORO-0002`, tabla REF autenticada por hash; puntos y soporte desde los RESULT del mismo auxiliar. La reproducción histórica y la reproducción de las emisiones están acreditadas separadamente. Ninguna cifra siguiente evalúa R futura.

El auxiliar proporciona 13502 personas, 190 estratos y 2164 UPM; soporte SI. Las familias comparten muestra y réplica: correlación del ruido muestral 0.8256. Una sola ola futura y una apertura conjunta, dos resultados dependientes.

La siguiente tabla muestra el escenario de precisión histórica (escala SE=1), sin deriva temporal añadida. Δ es el cambio supuesto R−p0 y se compara con la banda fija ±2 pp. Cada frecuencia es una proporción del simulador empírico, no una potencia acreditada contra un diseño futuro conocido.

| Familia | Δ supuesto | Compatible | Indeterminado | Desvío material |
|---|---:|---:|---:|---:|
| AHORRO-FORMAL | 0.00 pp | 86.30% | 13.70% | 0.00% |
| HORIZONTE-AHORRO | 0.00 pp | 97.30% | 2.70% | 0.00% |
| AHORRO-FORMAL | 2.00 pp | 1.90% | 95.00% | 3.10% |
| HORIZONTE-AHORRO | 2.00 pp | 3.05% | 94.90% | 2.05% |
| AHORRO-FORMAL | 3.00 pp | 0.00% | 58.50% | 41.50% |
| HORIZONTE-AHORRO | 3.00 pp | 0.00% | 46.10% | 53.90% |
| AHORRO-FORMAL | 4.00 pp | 0.00% | 6.10% | 93.90% |
| HORIZONTE-AHORRO | 4.00 pp | 0.00% | 1.70% | 98.30% |

El cambio mínimo positivo que produce al menos 80% de desvíos materiales en este escenario es AHORRO-FORMAL: 3.65 pp, HORIZONTE-AHORRO: 3.40 pp. Se busca en grilla de 0 a 10 pp, paso .05 pp; incluye superar la banda material de 2 pp. Es MDE de una conclusión de desvío respecto a la banda, no de un test frente a cero. El escenario justo en el borde de la banda tiende a quedar indeterminado; no es fracaso del contraste ni motivo para mover el umbral.

Sensibilidad temporal conjunta: la deriva añadida es normal y compartida entre familias; no fue estimada desde una serie temporal. Estas probabilidades conservan la dependencia del ruido histórico. Se muestra Δ supuesto=4 pp y escala SE=1.

| SD deriva compartida | Ambas conclusiones informativas | Formal: desvío | Ambas vías: desvío |
|---|---:|---:|---:|
| 0.00 pp | 93.75% | 93.90% | 98.30% |
| 0.50 pp | 86.75% | 87.90% | 92.90% |
| 1.00 pp | 76.85% | 77.75% | 82.60% |

Los 54 escenarios completos están en [potencia.tsv](potencia.tsv): cambios positivos de 0/1/2/3/4/5 pp, escalas del error estándar .75/1/1.5 y SD de deriva 0/.5/1 pp. No se empareja otra ola por número de réplica. Los cambios negativos sólo tendrían simetría aproximada y no se presentan como una medición. Kish individual describe dispersión de pesos, no reemplaza la precisión de diseño.

PROPUESTO-POR-EJECUTOR: conservar ambas familias para la misma ola. El protocolo puede producir una conclusión informativa bajo estabilidad local y distinguir desviaciones positivas mayores que la banda; no promete distinguir con alta probabilidad todo cambio de 2 pp. Mantener banda y soporte congelados, comunicar el resultado indeterminado cuando corresponda y no seleccionar una familia ganadora. Compartir muestra implica que dos resultados no duplican evidencia independiente.

Reservas materiales: el ruido futuro, el diseño y la deriva temporal son desconocidos; este simulador no acredita cobertura nominal ni eficacia predictiva, calibración general, estabilidad entre olas o adopción. Primario futuro d_k=R_k−p0 con piso fijo: no se agrega incertidumbre histórica al contraste. Fecha oficial ENIF no confirmada, atestación externa pendiente y apertura futura sin ejecutar. El contrato de serialización futura v2 está preparado y autorizado sólo para su adaptación de salida; COMMIT-3 requiere descriptor comparable, autoridad e identidad/hash reales antes de abrir.

La identidad conceptual de ambas vías y la coincidencia numérica del oro se documentan en [oro-comparacion.json](oro-comparacion.json); no se denomina horizonte temporal a la intersección de vías.
