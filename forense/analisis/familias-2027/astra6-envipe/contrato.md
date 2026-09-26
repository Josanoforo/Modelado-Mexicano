# Contrato común ENVIPE · ASTRA6-C2-ENVIPE-1

**PROPUESTO-POR-EJECUTOR, 26/sep/2026.** Fuente: encargo firmado archivado, ambas specs v1.2 y hoja global del 23/sep. La firma «Acordado» activa misión/adenda; no abre reservas ni adopta resultados. Las v1.2 se presentan expresamente como propuestas y su recibo #1076 mantiene CONDICIONAL. Consulta puntual del registro de firmas por los nombres de estas familias y acto: sin firma específica encontrada que congele este nuevo código. No se modifica ningún protocolo, hash o productor histórico.

## Identidad y contraste

Dos familias y una sola ola objetivo etiquetada ENVIPE 2027. Edición futura, año de referencia del delito, levantamiento y publicación son campos separados. La referencia futura queda **NO-CONFIRMADA**, corrigiendo la referencia 2025 que v1.2 arrastraba; se acepta sólo con ficha oficial previa a R. ENVIPE 2026 permanece reservada y fuera de este acto. La edición histórica abierta sirve de oro y diagnóstico, no de evaluación prospectiva.

| Familia | Unidad y ponderador | Outcome y denominador | Piso inmutable |
|---|---|---|---|
| DENUNCIA-U4 | Persona, FAC_ELE | U1: BPCOD 05–15, BP1_20=2, BP1_23 01–08; U4: persona con ≥1 U1. Outcome max de BP1_23 en 01,02,06,08. Cada persona una vez. | RESULT-ENVIPE-DEN-P-C2-U4 / CALC-ENVIPE-0001 |
| EVASION-NORMA | Delito, FAC_DEL | Denominador: BP1_20 1/2, peso positivo. Outcome conjunto BP1_20=2 y BP1_23 en 04,05,06,08. Incluye denunciados con outcome 0. | RESULT-EVASIONNORMA-A-P-EVADE / CALC-EVASION-NORMA-0001-v1_1 |

La unión persona-delitos exige llave persona unívoca, marco persona sin duplicados, delitos sin orfandad y diseño consistente. FAC_ELE se toma una vez de persona, FAC_DEL de cada delito; no intercambiarlos. BP1_23 se normaliza nominalmente a códigos de dos dígitos sin reinterpretar su significado. U4 excluye 99/blanco/no válidos de U1, cuenta exclusiones aparte y no trata una persona sin U1 como C2=0. Evasión conserva 99/blanco/no válidos entre no denunciados como 0 dentro del denominador histórico y los cuenta aparte; ese 0 es transformación heredada, no ausencia acreditada del mecanismo.

Los puntos p0 se leen por RESULT y se comprueban contra los hashes de sello completos conservados en las specs v1.3. No se copian cifras a mano. Primario: d_k=R_k−p0 fijo; no propagación de incertidumbre histórica ni emparejamiento de olas por índice. No hay retador, pérdida comparativa, ΔMAE ni superioridad B-bis. La etiqueta evasión no constituye identificación causal.

## Diseño y reglas ejecutables

**PROPUESTO-POR-EJECUTOR:** bootstrap estrato-UPM con 2,000 réplicas, PCG64 y seed 20260909; un solo plan generado sobre marco persona completo con diseño válido. Ordenar estratos/UPM y remuestrear, en cada estrato, tantas UPM como hay, con reemplazo. Transportar multiplicidades a persona y delito por llaves; mantener dependencia conjunta entre outcomes. No remuestrear filas de delito ni construir planes filtrados independientes. Guardar vectores R y d por familia y sus réplicas comunes.

Soporte U4: n≥5,000; evasión: n≥10,000; cada denominador necesita ≥100 estratos y ≥1,000 UPM efectivos, cero falta de peso/diseño, ≥1,000 réplicas válidas y denominador válido en ≥95% de las 2,000. Publicar n efectivo de pesos, conteos por diseño, exclusiones con masas y singletons específicos de cada universo. Un conteo U1 no acredita U4. Los pisos operativos no garantizan potencia ni cobertura.

Sin método de varianza válido aprobado previo a R, cualquier singleton contribuyente deja el dictamen **NO-ESTIMABLE**. Un plan que mantenga esos singleton con multiplicidad uno produce un IC de diagnóstico con anchura potencialmente subestimada; ni ese IC ni escenarios derivados habilitan compatibilidad/desvío. No fusionar estratos o inventar corrección para superar el gate.

Comparabilidad fallida de unidad/universo/reactivo/códigos/peso → NO-COMPARABLE; esquema insuficiente, falta de soporte o IC inválido → NO-ESTIMABLE. Sólo luego IC95 percentil finito ordenado de d: COMPATIBLE-CON-TOLERANCIA si −0.02≤L y U≤0.02; DESVÍO-MATERIAL si U<−0.02 o L>0.02; INDETERMINADO en otro caso. No ajustar banda ni gates tras R. Una conclusión es local a familia, piso y ola; no calibración general ni acierto futuro.

## Congelación, oro y activación

COMMIT-1 fija specs humanas/YAML, lector material explícito, dependencias, guardias, whitelist de campos y archivos, semilla, pruebas sintéticas y de mutación; los hashes se computan sobre bytes finales. El código no importa productores históricos vivos. Toda adaptación futura puramente nominal exige documentación y nueva verificación previa a apertura; cambio sustantivo detiene comparabilidad y requiere acto propio. No se promete que el descriptor futuro sea conocido.

Auxiliares históricos autorizados tienen spec previa a la lectura y sello propio. Reproducción de emisiones y ejecución del oro histórico se acreditan por separado; ninguno acredita predicción. La potencia temporal se informa como escenarios con supuestos/dependencia, estados y cambio mínimo detectable; no se infieren réplicas de extremos ni se sustituye el piso. Las limitaciones de singleton se conservan en escenarios.

COMMIT-2 sella emisiones de p0 sin R futura y sin retadores. Activación futura requiere identidad de ola, ficha de referencia/publicación, cuestionario/descriptor/pesos/diseño equivalentes, reserva por canal existente, autorización de código y una sola apertura para ambas familias. Este acto no descarga ni abre la ola objetivo, no modifica manifiesto ni otorga autorización futura. Calendarización desconocida conserva CONDICIONAL. Atestación externa exige comprobante verificable: SELLADO-INTERNAMENTE, ENVIADO-A-ATESTACIÓN y ATESTIGUADO-EXTERNAMENTE son estados distintos.
