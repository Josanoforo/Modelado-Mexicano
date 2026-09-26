# FAMILIA-2027-ENIF-AHORRO-FORMAL · spec humana v1.3

## Estimando y fuente fija

Primario: proporción ponderada en U_B que declara ahorro formal en los últimos doce meses: F=1 si cualquier P5_6_1…P5_6_9 vale 1; F=0 cuando ninguna respuesta acredita la vía. Numerador Σ FAC_PER·F; denominador Σ FAC_PER en U_B. No medir tenencia de cuenta P5_4 ni usar FILTRO_S5_1 como fuente; son objetos distintos/control.

Reactivos cerrados P5_6: 1 nómina; 2 pensión; 3 apoyos de gobierno; 4 cuenta de ahorro; 5 cheques; 6 depósito a plazo; 7 fondo de inversión; 8 cuenta por internet/app no bancaria; 9 otra cuenta. Cada componente pregunta haber guardado dinero en esa cuenta, no sólo poseerla. Fuente de definiciones y periodo: data/corrida0/CALC-ENIF-0001/spec.yaml y spec humana ENIF-AHORRO-spec-v1_0.md. Cotejo instrumental futuro obligatorio.

Piso: RESULT-ENIF-AHO-B-P-FORMAL-P de CALC-ENIF-0001, sello.json SHA-256 `0c90801873c91ac109219fbe3bf88632fc6aa8a6bcef637f9876398e95f76de6`. Leer valor del RESULT y validar su archivo/hashes por separado. Resultado sellado redondeado: el oro directo se compara bajo tolerancia de representación explícita del paquete; nunca sustituye ni reescribe el piso. Incertidumbre conjunta nueva pertenece al auxiliar, no al RESULT histórico.

## Contrato prospectivo común

**PROPUESTO-POR-EJECUTOR, ACTO ASTRA6-C2-ENIF-1.** Sucesora aditiva de v1.2; versiones, CALC y sellos previos intactos. El encargo firmado autoriza desarrollar el paquete; no adopta resultados, no modifica procedimientos históricos y no abre olas reservadas. La hoja U4 declara que v1.2 era propuesta técnica sin YAML ni COMMIT-1 ejecutable. La congelación del paquete técnico presente ocurre en su COMMIT-1, antes del oro y de cualquier registro histórico del auxiliar autorizado.

Instrumento objetivo: una ola ENIF futura etiquetada 2027, condicionada a fecha oficial de publicación dentro de 23/sep/2026–23/mar/2028; referencia histórica 2024. Fechas de levantamiento y publicación futuras: consultar evidencia local de calendario del acto; el nombre no acredita fecha. Unidad: persona elegida de 18 años y más residente en vivienda particular. Escala: proporción [0,1]; contexto histórico del reactivo: junio de 2023 a entrevista (últimos doce meses), según spec sellada ENIF-0001. El cotejo futuro debe conservar duración y significado del periodo, sin exigir el mismo año literal.

Universo U_B: todas las personas elegidas de TMODULO con FAC_PER finito >0. EDAD_V es guardia de población, no filtro oportunista: conservar códigos oficiales 97 (97 y más) y 98 (edad no especificada) del contrato histórico. Edad válida fuera del universo 18+ o esquema distinto sin equivalencia documentada: NO-COMPARABLE. Peso inválido se cuenta y excluye del punto; cualquier persona sin peso/diseño incumple el gate de soporte y deja el dictamen NO-ESTIMABLE. Ningún cero sustituye falta de columna ni tabla vacía.

FAC_PER es ponderador persona; FAC_VIV/FAC_HOG no son sustitutos. LLAVEMOD identifica la persona; exigir unicidad. EST_DIS y UPM_DIS se conservan como cadenas opacas, incluida su representación y ceros. Sin agrupación post hoc ni selección de subgrupos. Universo, variables, pesos y equivalencia se verifican antes de permitir evaluación.

Códigos históricos: formal P5_6_j admite 1=sí, 2=no y b=blanco por secuencia/no tiene esa cuenta; informal P5_1_k admite 1=sí y 2=no. Blanco formal no acredita ahorro ni se excluye de U_B. Lista completa de columnas obligatoria; un componente ausente produce NO-ESTIMABLE. Un código desconocido no se convierte en sí ni se borra del denominador. Si aparecieran NS/NR futuros, conservarlos en U_B, enumerar número y masa FAC_PER por componente y aplicar la regla literal de evidencia afirmativa: un 1 establece la vía, ausencia de 1 no la establece. Esto describe evidencia afirmativa observada, no ausencia de ahorro latente. El gate previo exige cotejar significado, saltos y universo del instrumento: exclusión prescrita que cambie U_B, recodificación no equivalente o ambigüedad de concepto produce NO-COMPARABLE; ausencia de dato necesario para verificarlo produce NO-ESTIMABLE. No imputar ni renormalizar.

## Contraste y dictamen

Piso p0 fijo resuelto desde RESULT sellado y hash, nunca cifra escrita en un consumidor. Primario d=R−p0, error absoluto |d|. La incertidumbre histórica no se agrega a ese primario; auxiliares de incertidumbre/potencia son diagnósticos separados y no sustituyen el oro histórico. Banda propuesta común ±0.02 en proporción (±2 pp), decisión práctica, no precisión acreditada ni tolerancia de replay del CALC.

Soporte: n≥10,000, estratos≥150 y UPM≥1,000, cero personas sin peso/diseño. Son pisos operativos heredados de v1.2, no certificación de potencia. Bootstrap de UPM dentro de estrato con diseño oficial: 2,000 réplicas, al menos 1,000 válidas y denominador válido en al menos 95%; semillas y RNG concretos en YAML/código COMMIT-1. Estrato con una sola UPM sin método válido previamente congelado: NO-ESTIMABLE para dictamen. Misma apertura y mismas multiplicidades por réplica para ambos outcomes; no independencia ficticia ni emparejamiento de olas por índice.

Guardar R_k, d_k=R_k−p0, IC95 percentil de d_k, soporte, masa de códigos y fracción |d_k|≤0.02. Sin reconstruir réplicas desde extremos marginales. Antes de etiquetas estadísticas: cambio material de estimando/universo/unidad/códigos/pesos → NO-COMPARABLE; falta de soporte, componentes o IC válido → NO-ESTIMABLE.

Con IC finito y ordenado [L,U]: COMPATIBLE-CON-TOLERANCIA si −0.02≤L y U≤0.02; DESVÍO-MATERIAL si U<−0.02 o L>0.02; INDETERMINADO en cualquier otro caso. Límites de la banda incluidos sólo en compatible. Casos (pp): [−2,2] compatible; [0.7,1.3] compatible; [2,2.5] indeterminado; [2.01,2.5] desvío; [−5,5] indeterminado. No se exige incluir cero.

El dictamen sólo permite afirmar compatibilidad local respecto a este estimando, piso y ola; no CALIBRADO, causalidad, estabilidad entre olas ni cobertura nominal. ΔMAE y B-bis: NO-APLICABLE, cero retadores externos. Escenarios de potencia/variación temporal se identifican por sus supuestos, sin ajustar margen/soporte ni retirar familias por conveniencia.

## Activación y cierre

COMMIT-1 fija spec YAML/código material/dependencias/semillas/guardias antes de registros históricos auxiliares; COMMIT-2 congela emisión p0 sin R futura. COMMIT-3 sólo por autorización de ola, reserva y metadatos aceptados, una única apertura ENIF con primer resultado conservado. No activar adquisición ni escribir manifiesto. Adaptación nominal de nombres sólo mediante mapa documentado que preserve significado; cambio sustantivo requiere enmienda firmada antes de abrir R.

Fecha oficial ausente mantiene CONDICIONAL sin impedir código/emisión. Atestación interna y externa son estados separados y requieren comprobante. La aceptación del instrumento futuro sigue pendiente: una lista blanca histórica no promete descriptor futuro conocido. La evidencia del acto distingue emisión, reproducción histórica, oro directo y diagnóstico auxiliar.
