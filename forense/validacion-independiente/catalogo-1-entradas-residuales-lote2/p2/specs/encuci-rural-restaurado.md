# ENCUCI 2020 · protesta rural con agravio · entrada humana sucesora

Estado: RESTAURACION-DE-ENTREGA. Fuente humana sellada de 09/sep/2026, §3.5. No crea contrato ni adopción.

Identidad: `RESULT-ENCUCI-B-P-RUR-AGR`. Celda `B-P-RUR-AGR`.
Conducta: protesta alguna vez en la vida rural con agravio.
Unidad: persona seleccionada de 15+; proporción [0,1]. La etiqueta de segmento de salida es `agravio_rural`; un nombre de consumidor no define el entorno.

Unir `SEC_6_7_8` con `SEC_4_5` por `ID_PER`, con llaves únicas; sin pareja quedan fuera y se cuentan. Usar `FAC_SEL` de SEC_6_7_8 finito y positivo. Normalizar los códigos numéricos de reactivos, aceptando 1 y 1.000000000000000 como 1. Exigir AP7_3_5 y AP4_3_2 en {1,2}; blancos/9 quedan fuera y se cuentan, sin imputar cero. DOMINIO es texto con espacios exteriores retirados, en {U,C,R}. Rural es {R}; C es complemento urbano y queda junto a U para urbano. Esta identidad filtra DOMINIO=R y AP4_3_2=1.

Numerador Σ(FAC_SEL · 1[AP7_3_5=1]); denominador Σ(FAC_SEL) en la misma celda válida. AP7_3_5=2 aporta cero al numerador. Denominador cero produce NO-ESTIMABLE-UNIVERSO-VACIO. No usar el recorte de contacto de la familia mordida para protesta.

Salida comparada: documento y filas exactamente según `esquema-salida-v2.md` del contenedor; `llave` y `unidad` se copian literalmente de `esquema-identidades.tsv`, `punto` contiene la proporción reconstruida y `estado_ic=SIN-IC` si no se calcula intervalo. Celda B-P-RUR-AGR, segmento agravio_rural, unidad de observación PERSONA, n válido, peso denominador y exclusiones son metadatos auxiliares separados de la salida comparada. IC solo bajo contrato P3. No contiene referencias ni tolerancias nuevas.
