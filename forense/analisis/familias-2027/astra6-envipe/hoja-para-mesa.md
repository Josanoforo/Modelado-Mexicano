# Hoja local ENVIPE · FP-260926-GEN2-ASTRA6-C2-ENVIPE-1-7045-01

Dos familias con emisiones congeladas para una ola futura; cero con atestación externa verificada; publicación 2027 no confirmada y ventana septiembre 2027 inferida.

**PROPUESTO-POR-EJECUTOR:** conservar ambas familias y adoptar las precisiones de v1.3 (marco de diseño completo común, gates por dominio, p0 fijo, reglas de frontera); mantener CONDICIONAL hasta metadatos comparables y autorización de ola. Cero retadores. Alternativa: retirar una familia si el cambio mínimo relevante de mesa es menor que la resolución del escenario; no ajustar banda, soporte o piso tras R.

| Familia | n | Estratos propios | UPM propias | Singleton dominio | Kish (no n de diseño) | P compatible δ=τ=0 | MDE 80% (proporción) |
|---|---:|---:|---:|---:|---:|---:|---|
| DENUNCIA_U4 | 13023 | 725 | 7830 | 83 | 5636.75 | 0.8323 | [-0.037, 0.037] |
| EVASION_NORMA | 40280 | 739 | 10694 | 23 | 14848.00 | 0.9250 | [-0.035, 0.035] |

EJECUTADO: cálculo de 27 escenarios δ/τ y MDE direccional sobre réplicas legítimas conjuntas. Los MDE son escenarios condicionados al diseño/precisión 2025, no efectos temporales estimados ni eficacia predictiva. En ±2 pp predomina INDETERMINADO; la banda no se cambia por ello. Sensibilidad temporal τ=1/2 pp está en potencia.json; shock común hipotético preserva dependencia. Kish mide concentración de pesos y no reemplaza precisión de diseño.

El marco completo tiene 746 estratos, 13742 UPM y 0 singleton. Los singleton de dominio no son singleton del marco: esas UPM varían en réplicas dentro de su estrato completo. No se fundieron estratos ni se descartaron UPM. El método nuevo no cambia IC sellados ni acredita cobertura nominal. Fuente: diagnostico.json y auxiliares-spec.yaml congelada antes de registro histórico.

La misión ya está firmada en el encargo archivado por #1166: no se duplica «Acordado». Esta fila nueva propone contenido técnico; no registra una firma dada. Para COMMIT-3: ficha/descriptor, comparabilidad, adaptador nominal probado, autorización específica y única apertura conjunta. Atestación: enviar el inventario al circuito de mesa; manifiesto sin comprobante no es OTS.
