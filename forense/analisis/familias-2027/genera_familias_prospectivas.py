#!/usr/bin/env python3
"""Generate additive v1.2 human protocols; earlier proposal versions stay intact."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "forense/prereg-caja"

# Tolerances are practical decision margins in percentage points, not the
# numerical replay tolerances declared by the historical CALCs.
FAMILIES = [
    {
        "slug": "ENIF-AHORRO-FORMAL", "instrument": "ENIF", "target": "2027", "prior": "2024",
        "unit": "persona de 18+", "estimand": "proporción ponderada de personas 18+ con ahorro formal (denominador compartido B de ENIF AHO; FAC_PER)",
        "calc": "CALC-ENIF-0001", "result": "RESULT-ENIF-AHO-B-P-FORMAL-P",
        "hash": "0c90801873c91ac109219fbe3bf88632fc6aa8a6bcef637f9876398e95f76de6",
        "numerator_denominator": "Numerador = suma(FAC_PER) entre U_B personas 18+ con cualquier P5_6_1…P5_6_9='1'. Denominador = suma(FAC_PER) de todas las personas 18+ con FAC_PER finito >0 (U_B), no sólo quienes respondieron sí/no. El contrato histórico sólo declara 1, 2 y blanco 'b'; 'b' significa que no tiene esa cuenta. Si ningún tipo vale 1, la persona aporta 0 y se cuenta en B-N-SIN-NINGUNA-CUENTA. Si la ola futura incorpora NS/NR, mantenerlos contados dentro del denominador bajo la regla literal '1 si alguno es 1; 0 si ninguno', con desglose explícito; si no se puede aplicar sin ambigüedad o cambia el sentido del código, NO-COMPARABLE/NO-ESTIMABLE según falte equivalencia o soporte.",
        "support": "n no ponderada ≥ 10,000; ≥150 estratos y ≥1,000 UPM utilizables; cero personas sin peso/diseño; el CALC 2024 tiene n=13,502, 190 estratos, 2,164 UPM y cero sin diseño.",
        "support_rationale": "n=10,000 conserva 74% del n histórico (13,502); 150/190 estratos y 1,000/2,164 UPM son pisos operativos explícitos, no límites calculados de error.",
        "missing": "No excluir del denominador los blancos de P5_6_j: el contrato CALC-ENIF-0001 especifica que 'b' significa no tiene esa cuenta; con ningún código 1, formal_cualquiera=0 y se cuenta aparte. El contrato sellado no declara NS/NR en P5_6_j. Si la ola futura los incorpora, permanecerán en U_B, se reportarán por código y masa FAC_PER y la regla literal histórica les da 0 sólo cuando ningún componente sea 1; no se hará imputación distinta. Si el instrumento los define como falta que debe excluirse, cambiaría el denominador y sería NO-COMPARABLE; sin conteos/masa para verificar, NO-ESTIMABLE.",
        "comparability": "Mismo universo persona 18+, reactivo y categorías que definen ahorro formal, FAC_PER y regla de dominio. Recodificación que conserve significado y partición documentable: sensibilidad descriptiva sin cambiar la primaria. Cambio de universo, ponderador o concepto: NO-COMPARABLE.",
        "precision": "El padre guarda IC95 por bootstrap de UPM dentro de estrato: [0.274161, 0.296777], 190 estratos, 2,164 UPM, sin estrato de UPM única; no guarda las réplicas. La media del IC no mide incertidumbre del error prospectivo ni potencia. Hace falta el vector de réplicas futuras emparejadas con el piso fijo y n efectivo para IC del error/potencia.",
        "activation": "Fecha oficial de publicación dentro de 23/sep/2026–23/mar/2028; cuestionario público cotejado; ninguna ola intermedia cambia la identidad del estimando; especificación técnica y código congelados antes de abrir esa única ola.",
    },
    {
        "slug": "ENIF-HORIZONTE-AHORRO", "instrument": "ENIF", "target": "2027", "prior": "2024",
        "unit": "persona de 18+ (estimando derivado de tres proporciones ENIF)", "estimand": "proporción de ambas vías de ahorro según HVD: solo formal + solo informal − tiene ahorros; identidad y denominadores fijados por CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1",
        "calc": "CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1", "result": "RESULT-HVD-A-AMBAS-VIAS",
        "hash": "1c8b329fb2088d24298acb3081e9bb2d2366dce05c6e238d282271d251d92609",
        "numerator_denominator": "Estimando futuro directo: numerador = suma(FAC_PER) de personas U_B para quienes se observan ambas vías, formal e informal (al menos un P5_6_j=1 y un P5_1_k=1); denominador = suma(FAC_PER) de todas las personas 18+ con FAC_PER finito >0 (mismo U_B de ENIF-AHORRO-FORMAL). El contrato formal admite blanco 'b' como no tener esa cuenta; P5_1_k sólo declara códigos 1/2. Nuevos NS/NR/códigos no válidos se conservan y detallan en U_B pero no establecen una vía: sólo la conjunción de respuestas afirmativas entra al numerador; excluirlos del denominador cambiaría el universo. La cifra histórica HVD no equivale a ese conteo individual: es identidad de marginales sellados sin covarianza.",
        "support": "n común de referencia ≥10,000 personas 18+; ≥150 estratos y ≥1,000 UPM utilizables en el universo común; denominadores armonizados y cada componente identificable. ENIF padre: n=13,502, 190 estratos y 2,164 UPM. El derivado histórico no tiene su propio n efectivo.",
        "support_rationale": "Se comparte el gate del padre ENIF-AHO: n=10,000 (74% de su n=13,502), ≥150/190 estratos y ≥1,000/2,164 UPM. Se exige soporte común real para la intersección; el CALC derivado no aporta n efectivo propio.",
        "missing": "Para la estimación prospectiva conjunta, persona permanece en U_B; blanco 'b' en P5_6 significa no tener esa cuenta, y P5_1/P5_6 sólo establecen una vía si al menos un código vale 1. NS/NR/códigos no válidos permanecen en denominador y se enumeran por componente, pero no acreditan una vía ni entran al numerador; no se renormaliza. Excluirlos o reinterpretarlos como respuestas sí cambiaría universo/outcome y sería NO-COMPARABLE. Si se preserva el contrato pero falta outcome conjunto o réplica emparejada, NO-ESTIMABLE; no calcular por inclusión-exclusión de marginales como sustituto del primario prospectivo.",
        "comparability": "Requiere invariancia de la definición de ahorro formal, informal y tenencia total, con mismas personas y periodo de referencia. El resultado histórico es aritmética determinista sobre tres proporciones selladas, no estimación conjunta: CALC declara expresamente que no hay IC95 propio por falta de covarianza entre corridas. La futura evaluación no lo llamará calibrado ni comparará R con un IC histórico.",
        "precision": "No existe vector de réplicas conjuntas ni covarianza entre insumos sellados, ni n efectivo del derivado; no se puede estimar varianza histórica o potencia sin reabrir/recalcular bajo una nueva unidad autorizada. Hace falta archivo de réplicas conjuntas de los tres componentes (mismo esquema de UPM/estrato) o medición futura diseñada para estimar directamente la proporción conjunta. No combinar extremos de IC.",
        "activation": "Condiciones comunes de ENIF, más prueba de que el instrumento futuro identifica los tres componentes bajo el mismo universo y permite estimar directamente HVD. Si sólo es posible reconstruir una suma de marginales sin unión individual, NO-ELEGIBLE.",
    },
    {
        "slug": "ENCIG-PAGO-DIGITAL", "instrument": "ENCIG", "target": "2027", "prior": "2025",
        "unit": "trámite del universo C ENCIG MOR (FAC_TRA)", "estimand": "proporción ponderada de pagos de luz digital/autoservicio P7_3∈{4,5} sobre U_C; RESULT-ENCIG-MOR-C-P-ADOPTA",
        "calc": "CALC-ENCIG-0001", "result": "RESULT-ENCIG-MOR-C-P-ADOPTA",
        "hash": "9db7e8f292dc4acd43ee1107b00fe7e1c6097d6abaa3b8c78444107b6cbf58d7",
        "numerator_denominator": "Numerador = suma(FAC_TRA) de trámites del universo U_C con P7_3∈{4,5}. Denominador = suma(FAC_TRA) de trámites tipo 01 (N_TRA=1) con P7_3∈{1,2,4,5,6} y FAC_TRA finito >0. Códigos 3,7,8,9 y blanco quedan fuera del denominador, se cuentan y se ponderan como residuo; en particular NS/NR/blanco no se recodifican a canal presencial o digital.",
        "support": "n elegible ≥10,000 trámites, ≥100 estratos y ≥1,000 UPM; residuos/códigos fuera de la partición ≤1% del peso elegible; sin unidad sin FAC_TRA. En ENCIG 2025: U_C n=20,203, 441 estratos, 8,486 UPM; residuo=189 filas, pero el CALC no registra su masa ponderada: el límite de 1% es comprobación futura, no dato ya acreditado.",
        "support_rationale": "n=10,000 es 49% del n histórico 20,203; ≥100/441 estratos y ≥1,000/8,486 UPM fijan un piso conservador de cobertura de diseño, no una precisión calculada. El límite de residuo 1% también es un gate operativo, pendiente de masa ponderada.",
        "missing": "Mantener como residuo aparte los canales no incluidos y NS/NR/blancos; no recodificarlos a presencial/digital. Pérdida de FAC_TRA o clave de diseño excluye la unidad del IC y se reporta; si supera 1% del peso elegible, NO-ESTIMABLE. No deduplicar sin aplicar la llave ID_TRA+NT_TIPO verificada.",
        "comparability": "Mismo servicio luz, evento de pago, unidad trámite, canal digital={4,5}, no adopta={1,2,6}, universo C, FAC_TRA y llaves de evento. Canal nuevo/ambiguo conserva residuo; si cambia el significado de pago o la unidad/denominador, NO-COMPARABLE. No interpretar el resultado como digitalización general.",
        "precision": "CALC-ENCIG-0001 conserva IC95 [0.662900,0.684530], bootstrap de UPM dentro de estrato (2,000 réplicas); 8 estratos de UPM única, de modo que el IC es límite inferior de anchura verdadera. No se guardaron las réplicas; el IC marginal no da varianza del error contra el punto fijo. Hace falta vector futuro por réplica y n efectivo para IC de error/potencia.",
        "activation": "Fecha y cuestionario oficial confirmados; misma definición de evento y servicio; instrumento mantiene identificación de estrato, UPM, FAC_TRA y tipo de evento. Apertura compartida con ENCIG-SOLICITUD-MORDIDA.",
    },
    {
        "slug": "ENCIG-SOLICITUD-MORDIDA", "instrument": "ENCIG", "target": "2027", "prior": "2025",
        "unit": "persona adulta de universo A ENCIG MOR (FAC_P18)", "estimand": "proporción ponderada con solicitud directa de beneficio, P8_3_1=1, universo A y FAC_P18; RESULT-ENCIG-MOR-A-P-SOL1",
        "calc": "CALC-ENCIG-0001", "result": "RESULT-ENCIG-MOR-A-P-SOL1",
        "hash": "9db7e8f292dc4acd43ee1107b00fe7e1c6097d6abaa3b8c78444107b6cbf58d7",
        "numerator_denominator": "Numerador = suma(FAC_P18) de personas del universo A con P8_3_1=1. Denominador primario = suma(FAC_P18) de personas del universo A con P8_3_1∈{1,2}; no es sólo el subconjunto afirmativo y no incluye P8_3_1=9/blanco/no numérico. Reportar esas no respuestas aparte en conteo y peso, y además la cobertura del universo A. Éste es el universo del estimador histórico CALC-ENCIG-0001.",
        "support": "n elegible ≥10,000 personas, ≥100 estratos y ≥1,000 UPM; NS/NR+blanco ≤2% del peso de A; cero unidades sin FAC_P18. ENCIG 2025: A n=40,042, 442 estratos y 9,172 UPM; 94 NS/NR en P8_3_1, cero blancos y cero sin diseño/ponderador.",
        "support_rationale": "n=10,000 es 25% del n histórico 40,042; ≥100/442 estratos y ≥1,000/9,172 UPM son pisos operativos, no garantía inferencial. El tope 2% limita cuánto puede diferir el universo de respuesta válida del universo A; el CALC histórico no conserva la masa faltante para certificarlo.",
        "missing": "El contrato histórico define U_A con P8_3_1∈{1,2} y FAC_P18 positivo; códigos 9/NS/NR, blanco/no numérico se excluyen del punto, se cuentan aparte y no se imputan como 'no'. Por ello el estimando es entre respuesta válida (denominador U_A válido), no sobre toda A. Informar pérdida de cobertura contra A; si el peso excluido supera 2% del peso potencial A, NO-ESTIMABLE. Si futuro cambia el tratamiento de estos casos o el denominador, NO-COMPARABLE con el piso sellado.",
        "comparability": "Mismo evento solicitud directa, pregunta P8_3_1 o equivalencia textual documentada, categorías sí/no, universo A, FAC_P18 y diseño EST_DIS/UPM_DIS. No mezclar los otros incisos de SOLANY con SOL1. Cambio de evento, informante o recorte del universo: NO-COMPARABLE. El CALC histórico registra 94 NS/NR pero no el peso expandido faltante; el umbral de 2% debe comprobarse en el vector/payload futuro y no se afirma aquí que se cumpla en 2025.",
        "precision": "CALC-ENCIG-0001 guarda IC95 [0.080867,0.089021], bootstrap UPM dentro de estrato, 2,000 réplicas, seed 20260909/PCG64; ningún estrato de UPM única. No guarda vector de réplicas: no derivar de ahí EE exacta, IC del error o potencia. Requiere vector futuro del contraste emparejado piso−R y n efectivo.",
        "activation": "Condiciones comunes ENCIG, con texto/saltos equivalentes de P8_3_1 y acceso a FAC_P18/diseño. Misma apertura ENCIG que pago digital; dos outcomes en protocolo sellado previo, sin dos accesos ni selección posterior.",
    },
    {
        "slug": "ENVIPE-DENUNCIA-U4", "instrument": "ENVIPE", "target": "2027", "prior": "2025",
        "unit": "persona víctima en U4 con FAC_ELE", "estimand": "proporción persona de motivo C2 de no denuncia en U4, FAC_ELE; RESULT-ENVIPE-DEN-P-C2-U4",
        "calc": "CALC-ENVIPE-0001", "result": "RESULT-ENVIPE-DEN-P-C2-U4",
        "hash": "18310f8adb6fb5963038d67c2e8a7eaba50e09c062dddbc579e918f090cbde16",
        "numerator_denominator": "Numerador = suma(FAC_ELE) de personas U4 cuyo colapso C2 vale 1: entre sus delitos U1 elegibles hay al menos uno con BP1_23∈{01,02,06,08}. Denominador = suma(FAC_ELE) de personas con al menos un delito U1 elegible; cada persona entra una vez. U1 exige delito personal BPCOD∈{05…15}, BP1_20=2 y BP1_23∈{01…08}; BP1_23=99 (NS/NR) y blanco no forman U1 según CALC-ENVIPE-0001. Se cuentan aparte; el blanco pese a BP1_20=2 queda fuera del universo de delito, y una persona sin otro delito U1 no entra al denominador. Las personas con U1 y sin C2 positivo son el complemento (todos sus delitos U1 caen en {03,04,05,07}).",
        "support": "n personas U4 ≥5,000, ≥100 estratos y ≥1,000 UPM; cero sin FAC_ELE/diseño. ENVIPE 2025 U4: n=13,023, masa FAC_ELE=14,982,594; el método tiene 83 estratos de UPM única en U1, por lo que su IC subestima anchura verdadera y sirve como diagnóstico, no prueba de calibración.",
        "support_rationale": "n=5,000 retiene 38% del U4 histórico (13,023); se propone un piso menor por tratarse de un dominio persona-submuestra. ≥100 estratos/≥1,000 UPM es un gate de diseño nuevo: el CALC no conserva sus conteos específicos en U4, así que no se presenta como potencia ni soporte ya acreditado.",
        "missing": "Preservar literalmente la cascada histórica U1→U4. BP1_23=99 (NS/NR), blanco y códigos fuera de {01…08} se excluyen del U1 estimable y se cuentan aparte; no se convierten a motivo C2=0. El denominador persona U4 sólo contiene personas con al menos un delito que sí pertenece a U1. Reportar, además, delitos potenciales excluidos por 99/blanco y personas con todos sus delitos potenciales excluidos, con conteos/peso si el diseño lo permite. Si el futuro recalcula U4 incluyéndolos como no denuncia o cambia el colapso max, el universo cambia y es NO-COMPARABLE; faltando detalle para aplicar el contrato, NO-ESTIMABLE.",
        "comparability": "Mismo dominio U4/persona, persona con ≥1 delito elegible U1, codificación C2, FAC_ELE y diseño de tper_vic2. No sustituir FAC_DEL/U1 (unidad delito). Requiere verificar BP1_23/FAC_ELE y saltos del cuestionario. Cambios en esas piezas o en la composición U4: NO-COMPARABLE.",
        "precision": "Histórico: CALC-ENVIPE-0001 declara 2,000 réplicas (seed 20260909/PCG64) y conserva IC95 [0.283020,0.305799], n=13,023 U4, pero ningún vector de réplicas; 83 estratos con una UPM en U1 generan varianza cero. Los conteos de diseño se publican para U1, no U4; la exigencia futura ≥100 estratos/≥1,000 UPM es una verificación nueva específica del universo U4. La proporción de estratos únicos específica U4 no está declarada. No usar su cobertura como evidencia calibrada. Hace falta archivo futuro de réplicas U4 y n efectivo; no recomputar desde extremos.",
        "activation": "Fecha/cuestionario confirmados, código C2 y universo U4 cotejados con la ficha vigente del instrumento. Abrir una sola vez la ola ENVIPE para ambas familias U4, sin abrir ENVIPE 2026 ni microdato de olas reservadas durante esta continuación.",
    },
    {
        "slug": "ENVIPE-EVASION-NORMA", "instrument": "ENVIPE", "target": "2027", "prior": "2025",
        "unit": "delito con BP1_20∈{1,2} y FAC_DEL", "estimand": "proporción conjunta ponderada evade_norma = (BP1_20=2 y BP1_23∈{04,05,06,08}) sobre delitos con BP1_20∈{1,2}, FAC_DEL; RESULT-EVASIONNORMA-A-P-EVADE",
        "calc": "CALC-EVASION-NORMA-0001-v1_1", "result": "RESULT-EVASIONNORMA-A-P-EVADE",
        "hash": "8076d9ff1e18ab1fe6ac7168600810580cabe99c1df9373ee21c8b40e9d2abe8",
        "numerator_denominator": "Numerador = suma(FAC_DEL) de delitos con BP1_20=2 y BP1_23∈{04,05,06,08}. Denominador = suma(FAC_DEL) de todos los delitos con BP1_20∈{1,2} y peso positivo, incluidos los denunciados (BP1_20=1). El CALC histórico define evade_norma=0 sólo fuera del conjunto numerador dentro de ese universo; BP1_23=99/blanco/código no válido entre no denunciados se cuentan explícitamente, y bajo transformación literal quedan en 0, no salen del denominador. No confundir con una tasa condicional entre no denunciados.",
        "support": "n delitos válidos ≥10,000, ≥100 estratos y ≥1,000 UPM; cero sin BP1_20, BP1_23, FAC_DEL o diseño. ENVIPE 2025: n=40,280, numerador=21,761 y 10,694 UPM; el CALC no conserva conteos de estratos/UPM únicos, que se exigirán al futuro ejecutor.",
        "support_rationale": "n=10,000 es 25% del n histórico 40,280; ≥100 estratos/≥1,000 UPM es un mínimo operativo por diseño frente a los 10,694 UPM registrados. El CALC legado no conserva los conteos de estratos/UPM únicos: esos gates son nuevos y no acreditan precisión.",
        "missing": "BP1_20 fuera de {1,2} o sin FAC_DEL no entra y se reporta como exclusión. Para BP1_20=1, BP1_23 es salto estructural y outcome=0. Para BP1_20=2, el CALC histórico fija outcome=1 sólo con BP1_23∈{04,05,06,08}, y 0 en cualquier otro caso, incluidos 99/blanco/código no válido; se cuentan aparte para transparentar la clasificación heredada. Aplicar esa regla literal conserva comparabilidad, aunque no es evidencia de que NS/NR sean ausencia real de evasión. Si se desea estimar otra respuesta faltante o excluirla, cambiarían el numerador/denominador efectivo y la comparabilidad: NO-COMPARABLE; si faltan sus conteos/masa para evaluar la regla, NO-ESTIMABLE. No reclasificar según R.",
        "comparability": "Misma unidad delito, disparador BP1_20, códigos normalizados BP1_23, FAC_DEL, EST_DIS/UPM_DIS y categorías {04,05,06,08}. No comparar con el derivado persona/U4 ni con el condicional entre no denunciantes (no estimable en la spec vigente). Cambio en categorías que definen norma: NO-COMPARABLE.",
        "precision": "spec legado declara bootstrap de conglomerado estratificado, 10,000 réplicas, seed 42; punto 0.562774, IC95 [0.551982,0.573448], n=40,280. Sin vector guardado, no se deriva IC del error ni potencia; el futuro CALC debe exportar por réplica el resultado R y diferencia con piso. Se requieren n efectivo y conteos de estratos/UPM únicos.",
        "activation": "Condiciones comunes ENVIPE; verificar equivalencia BP1_20/BP1_23, categorías, universo de delitos y pesos de 2025. Una apertura compartida con denuncia-U4; mantener dos outcomes y sus soportes separados.",
    },
]


def body(f: dict) -> str:
    return f"""# FAMILIA-2027-{f['slug']} · spec humana condicional v1.2

**Estado: CONDICIONAL.** “2027” es etiqueta de trabajo. La publicación oficial está NO-CONFIRMADA en el calendario INEGI 2026 consultado el 23/sep/2026; no inferir fecha de levantamiento o publicación por el nombre. No se abre dato futuro.

## Estimando cerrado y piso

- Instrumento/ola objetivo: {f['instrument']} {f['target']}; referencia: {f['prior']}; fecha oficial de levantamiento y publicación: NO-CONFIRMADAS. Unidad: **{f['unit']}**, escala: proporción [0,1]. Estimando único: {f['estimand']}.
- Piso inmutable: `{f['result']}` de `{f['calc']}`, cuyo `sello.json` tiene SHA-256 `{f['hash']}`. La identidad del archivo y el valor RESULT se comprueban por separado; la tolerancia de este protocolo no altera la tolerancia numérica del CALC.
- Si una ola intermedia altera universo, reactivo, códigos o unidad, no se sustituye el piso ni se elige otro estimando después de ver R: se emite `NO-COMPARABLE` o `NO-ESTIMABLE` según la regla de abajo.
- **Numerador y denominador:** {f['numerator_denominator']}

## Propuesta técnica para decisión pre-dato

- **Tolerancia material propuesta:** ±2.0 puntos porcentuales (pp) alrededor del punto fijo: dos unidades por cada cien en la escala del estimando. Se elige como margen absoluto pequeño, redondo, común y fácil de interpretar entre tasas base muy distintas; usar un margen relativo haría variar el error tolerado entre familias. Es una decisión práctica, no una conclusión empírica, ni precisión/potencia acreditada, equivalencia psicológica o la tolerancia numérica del CALC. Reportar siempre error absoluto y signo.
- **Soporte mínimo propuesto:** {f['support']} Justificación operativa: {f['support_rationale']} Los conteos/estratos/UPM mínimos filtran soporte muy ralo y permiten exigir presencia suficiente de diseño; no certifican precisión, potencia, cobertura nominal ni suficiencia para detectar 2 pp. Además, el IC futuro requiere ≥1,000 réplicas válidas de 2,000 y denominador válido en ≥95% de réplicas. Incumplimiento: `NO-ESTIMABLE`; no relajar tras R.
- **Faltantes:** {f['missing']}
- **Comparabilidad:** {f['comparability']}

## Dictamen prospectivo congelado

Antes de abrir la ola, COMMIT-1 congela especificación YAML, código, variables, pesos, universo, soporte, tratamiento de faltantes, regla de comparabilidad y semillas; se reserva una única apertura por instrumento y se reporta el primer resultado generado.

1. Primero resuelve la compuerta: si el estimando/universo/unidad/códigos/pesos no son equivalentes, `NO-COMPARABLE`; si falta soporte, dato para el contraste o un IC válido conforme al diseño, `NO-ESTIMABLE`. Un estrato de una UPM que aporte varianza cero deja el IC como límite inferior de anchura; salvo que antes de abrir se haya fijado un método de varianza válido para ese caso, no sirve para dictaminar y queda `NO-ESTIMABLE`. Sólo con ambas compuertas superadas y un intervalo finito ordenado se asigna exactamente una etiqueta estadística.
2. Ejecutar bootstrap de UPM dentro de estrato con el diseño oficial. Compartir apertura y réplica entre familias de una misma ola; nunca tratar outcomes del mismo instrumento como oportunidades independientes de observar R. Guardar cada `R_k`, y calcular directamente `d_k = R_k - p0` en cada réplica (p0 es el punto histórico fijo), más error puntual con signo, |d|, y fracción de réplicas con |d_k|≤0.02. Obtener IC95 percentil de los `d_k`; no reconstruir réplicas desde extremos de IC marginales. Si el diseño produce varianza cero por estratos de una UPM, reportarlo como limitación del IC y no afirmar calibración/cobertura.
3. Para IC95=[L,U] en proporción (equivale a pp tras multiplicar por 100), reglas cerradas: `COMPATIBLE-CON-TOLERANCIA` si **−0.02 ≤ L y U ≤ +0.02** (equivale a todo el IC dentro de [−2,+2] pp, límites incluidos); `DESVÍO-MATERIAL` si **U < −0.02 o L > +0.02** (estrictamente separado de la banda); `INDETERMINADO` en todo otro caso, incluidos intervalos anchos y los que sólo tocan la banda por un extremo. No se exige que el IC contenga cero: un IC estrecho [0.007,0.013] queda compatible. La regla clasifica un contraste local, no calibra un sistema.
4. Casos de comprobación (pp): [−5,+5]→INDETERMINADO; [+0.7,+1.3]→COMPATIBLE-CON-TOLERANCIA aunque no incluye 0; [+2.1,+3]→DESVÍO-MATERIAL; [−2,+2]→COMPATIBLE-CON-TOLERANCIA; [+2,+2.5] y [−2.5,−2]→INDETERMINADO; [+2.01,+2.5]→DESVÍO-MATERIAL. Con intervalo válido, ordenado y finito estas tres etiquetas son mutuamente excluyentes y exhaustivas.
5. Una sola comparación dentro de tolerancia permite decir únicamente **compatible con esta tolerancia local** para este estimando, piso y ola. No permite declarar `CALIBRADO`, calibración general, estabilidad entre olas ni cobertura nominal. Sin segundo objeto, ΔMAE y superioridad B-bis son `NO-APLICABLE`.

## Precisión disponible y brecha

{f['precision']}

La banda ±2 pp es una decisión práctica propuesta, no precisión acreditada. Efecto mínimo detectable, potencia y error tipo I **no son calculables** con los artefactos actuales. La condición de apertura exige guardar el vector de diferencias por réplica, soporte efectivo y conteos de UPM/estratos; si faltan, el resultado queda `NO-ESTIMABLE`, nunca se fabrica incertidumbre.

## Condiciones verificables para activación

{f['activation']}

Además, las dos familias del mismo instrumento se evalúan en una sola apertura y un mismo paquete de réplica cuando técnicamente comparten diseño. Son dos estimandos predeclarados con resultados conjuntos, no dos oportunidades independientes de mirar R ni una selección de ganador.

Fuente de selección: catálogo U1, commit `0ac21b6c`. Este artefacto propone protocolo; no autoriza microdatos, olas reservadas, otro piloto, otro retador ni CALC en esta unidad.
"""


def classify_interval(lower_pp: float, upper_pp: float) -> str:
    """Classify a valid, finite CI for d in percentage points."""
    if lower_pp > upper_pp:
        raise ValueError("intervalo invertido")
    if -2.0 <= lower_pp and upper_pp <= 2.0:
        return "COMPATIBLE-CON-TOLERANCIA"
    if upper_pp < -2.0 or lower_pp > 2.0:
        return "DESVÍO-MATERIAL"
    return "INDETERMINADO"


def check_synthetic_cases() -> None:
    cases = {
        (-5.0, 5.0): "INDETERMINADO",
        (0.7, 1.3): "COMPATIBLE-CON-TOLERANCIA",
        (2.1, 3.0): "DESVÍO-MATERIAL",
        (-2.0, 2.0): "COMPATIBLE-CON-TOLERANCIA",
        (2.0, 2.5): "INDETERMINADO",
        (-2.5, -2.0): "INDETERMINADO",
        (2.01, 2.5): "DESVÍO-MATERIAL",
    }
    for interval, expected in cases.items():
        actual = classify_interval(*interval)
        if actual != expected:
            raise SystemExit(f"DICTAMEN_SINTETICO_DISTINTO {interval}: {actual} != {expected}")


def main() -> None:
    check_synthetic_cases()
    for f in FAMILIES:
        calc = ROOT / "data/corrida0" / f["calc"]
        actual = hashlib.sha256((calc / "sello.json").read_bytes()).hexdigest()
        if actual != f["hash"]:
            raise SystemExit(f"SELLO_DISTINTO {f['calc']}: {actual}")
        sidecar = (calc / "sello.sha256").read_text().split()[0]
        if sidecar != f["hash"]:
            raise SystemExit(f"SIDECAR_DISTINTO {f['calc']}: {sidecar}")
        values = json.loads((calc / "resultados.json").read_text())["resultados"]
        if f["result"] not in values or not isinstance(values[f["result"]], (int, float)):
            raise SystemExit(f"RESULT_AUSENTE {f['calc']} {f['result']}")
        path = OUT / f"FAMILIA-2027-{f['slug']}-spec-v1_2.md"
        text = body(f)
        path.write_text(text)
        digest = hashlib.sha256(text.encode()).hexdigest()
        path.with_name(path.name + ".sha256").write_text(f"{digest}  {path.name}\n")
    print(f"familias_generadas_v1_2={len(FAMILIES)} dictamenes_sinteticos=7")


if __name__ == "__main__":
    main()
