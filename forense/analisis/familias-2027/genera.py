#!/usr/bin/env python3
"""Regenerate the six human-readable, conditional family protocols."""
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
        "support": "n no ponderada ≥ 10,000; ≥150 estratos y ≥1,000 UPM utilizables; cero personas sin peso/diseño; el CALC 2024 tiene n=13,502, 190 estratos, 2,164 UPM y cero sin diseño.",
        "missing": "Conservar el denominador B fijado por FAC_PER válido; clasificar el código de ahorro exactamente como en el cuestionario 2024. Respuesta NS/NR o blanco queda fuera del numerador, no se imputa como no ahorro; reportar n y masa de ponderador excluidos. Si no puede reconstruirse el mismo dominio, NO-ESTIMABLE.",
        "comparability": "Mismo universo persona 18+, reactivo y categorías que definen ahorro formal, FAC_PER y regla de dominio. Recodificación que conserve significado y partición documentable: sensibilidad descriptiva sin cambiar la primaria. Cambio de universo, ponderador o concepto: NO-COMPARABLE.",
        "precision": "El padre guarda IC95 por bootstrap de UPM dentro de estrato: [0.274161, 0.296777], 190 estratos, 2,164 UPM, sin estrato de UPM única; no guarda las réplicas. La media del IC no mide incertidumbre del error prospectivo ni potencia. Hace falta el vector de réplicas futuras emparejadas con el piso fijo y n efectivo para IC del error/potencia.",
        "activation": "Fecha oficial de publicación dentro de 23/sep/2026–23/mar/2028; cuestionario público cotejado; ninguna ola intermedia cambia la identidad del estimando; especificación técnica y código congelados antes de abrir esa única ola.",
    },
    {
        "slug": "ENIF-HORIZONTE-AHORRO", "instrument": "ENIF", "target": "2027", "prior": "2024",
        "unit": "persona de 18+ (estimando derivado de tres proporciones ENIF)", "estimand": "proporción de ambas vías de ahorro según HVD: solo formal + solo informal − tiene ahorros; identidad y denominadores fijados por CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1",
        "calc": "CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1", "result": "RESULT-HVD-A-AMBAS-VIAS",
        "hash": "1c8b329fb2088d24298acb3081e9bb2d2366dce05c6e238d282271d251d92609",
        "support": "n común de referencia ≥10,000 personas 18+; denominadores/olas armonizados y cada componente identificable. ENIF padre: n=13,502, 190 estratos y 2,164 UPM. El derivado no tiene su propio n efectivo.",
        "missing": "No imputar ni renormalizar componentes. Si falta cualquier componente o cambia el universo de una de las tres fuentes futuras, no calcular HVD y dictaminar NO-ESTIMABLE; publicar conteos y componentes disponibles como diagnósticos sin sustituir el primario.",
        "comparability": "Requiere invariancia de la definición de ahorro formal, informal y tenencia total, con mismas personas y periodo de referencia. El resultado histórico es aritmética determinista sobre tres proporciones selladas, no estimación conjunta: CALC declara expresamente que no hay IC95 propio por falta de covarianza entre corridas. La futura evaluación no lo llamará calibrado ni comparará R con un IC histórico.",
        "precision": "No existe vector de réplicas conjuntas ni covarianza entre insumos sellados, ni n efectivo del derivado; no se puede estimar varianza histórica o potencia sin reabrir/recalcular bajo una nueva unidad autorizada. Hace falta archivo de réplicas conjuntas de los tres componentes (mismo esquema de UPM/estrato) o medición futura diseñada para estimar directamente la proporción conjunta. No combinar extremos de IC.",
        "activation": "Condiciones comunes de ENIF, más prueba de que el instrumento futuro identifica los tres componentes bajo el mismo universo y permite estimar directamente HVD. Si sólo es posible reconstruir una suma de marginales sin unión individual, NO-ELEGIBLE.",
    },
    {
        "slug": "ENCIG-PAGO-DIGITAL", "instrument": "ENCIG", "target": "2027", "prior": "2025",
        "unit": "trámite del universo C ENCIG MOR (FAC_TRA)", "estimand": "proporción ponderada de pagos de luz digital/autoservicio P7_3∈{4,5} sobre U_C; RESULT-ENCIG-MOR-C-P-ADOPTA",
        "calc": "CALC-ENCIG-0001", "result": "RESULT-ENCIG-MOR-C-P-ADOPTA",
        "hash": "9db7e8f292dc4acd43ee1107b00fe7e1c6097d6abaa3b8c78444107b6cbf58d7",
        "support": "n elegible ≥10,000 trámites, ≥100 estratos y ≥1,000 UPM; residuos/códigos fuera de la partición ≤1% del peso elegible; sin unidad sin FAC_TRA. En ENCIG 2025: U_C n=20,203, 441 estratos, 8,486 UPM; residuo=189 filas, pero el CALC no registra su masa ponderada: el límite de 1% es comprobación futura, no dato ya acreditado.",
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
        "support": "n elegible ≥10,000 personas, ≥100 estratos y ≥1,000 UPM; NS/NR+blanco ≤2% del peso de A; cero unidades sin FAC_P18. ENCIG 2025: A n=40,042, 442 estratos y 9,172 UPM; 94 NS/NR en P8_3_1, cero blancos y cero sin diseño/ponderador.",
        "missing": "Códigos 9/NS/NR/blanco quedan no válidos, no negativos. Denominador primario = universo A con respuesta válida P8_3_1, como el estimador sellado; informar también cobertura sobre A. Si faltantes exceden 2% de peso A, NO-ESTIMABLE; no imputar.",
        "comparability": "Mismo evento solicitud directa, pregunta P8_3_1 o equivalencia textual documentada, categorías sí/no, universo A, FAC_P18 y diseño EST_DIS/UPM_DIS. No mezclar los otros incisos de SOLANY con SOL1. Cambio de evento, informante o recorte del universo: NO-COMPARABLE. El CALC histórico registra 94 NS/NR pero no el peso expandido faltante; el umbral de 2% debe comprobarse en el vector/payload futuro y no se afirma aquí que se cumpla en 2025.",
        "precision": "CALC-ENCIG-0001 guarda IC95 [0.080867,0.089021], bootstrap UPM dentro de estrato, 2,000 réplicas, seed 20260909/PCG64; ningún estrato de UPM única. No guarda vector de réplicas: no derivar de ahí EE exacta, IC del error o potencia. Requiere vector futuro del contraste emparejado piso−R y n efectivo.",
        "activation": "Condiciones comunes ENCIG, con texto/saltos equivalentes de P8_3_1 y acceso a FAC_P18/diseño. Misma apertura ENCIG que pago digital; dos outcomes en protocolo sellado previo, sin dos accesos ni selección posterior.",
    },
    {
        "slug": "ENVIPE-DENUNCIA-U4", "instrument": "ENVIPE", "target": "2027", "prior": "2025",
        "unit": "persona víctima en U4 con FAC_ELE", "estimand": "proporción persona de motivo C2 de no denuncia en U4, FAC_ELE; RESULT-ENVIPE-DEN-P-C2-U4",
        "calc": "CALC-ENVIPE-0001", "result": "RESULT-ENVIPE-DEN-P-C2-U4",
        "hash": "18310f8adb6fb5963038d67c2e8a7eaba50e09c062dddbc579e918f090cbde16",
        "support": "n personas U4 ≥5,000, ≥100 estratos y ≥1,000 UPM; cero sin FAC_ELE/diseño. ENVIPE 2025 U4: n=13,023, masa FAC_ELE=14,982,594; el método tiene 83 estratos de UPM única en U1, por lo que su IC subestima anchura verdadera y sirve como diagnóstico, no prueba de calibración.",
        "missing": "Preservar la regla C2/U4 completa, códigos y exclusiones de personas/delitos del CALC. NS/NR/blanco/fuera de universo nunca se convierten a no denuncia. Si falta un componente del universo, el código de motivo o FAC_ELE, NO-ESTIMABLE; publicar conteos de no respuesta y U4 sin ajustar el punto.",
        "comparability": "Mismo dominio U4/persona, persona con ≥1 delito elegible U1, codificación C2, FAC_ELE y diseño de tper_vic2. No sustituir FAC_DEL/U1 (unidad delito). Requiere verificar BP1_23/FAC_ELE y saltos del cuestionario. Cambios en esas piezas o en la composición U4: NO-COMPARABLE.",
        "precision": "Histórico: CALC-ENVIPE-0001 declara 2,000 réplicas (seed 20260909/PCG64) y conserva IC95 [0.283020,0.305799], n=13,023 U4, pero ningún vector de réplicas; 83 estratos con una UPM en U1 generan varianza cero. Los conteos de diseño se publican para U1, no U4; la exigencia futura ≥100 estratos/≥1,000 UPM es una verificación nueva específica del universo U4. La proporción de estratos únicos específica U4 no está declarada. No usar su cobertura como evidencia calibrada. Hace falta archivo futuro de réplicas U4 y n efectivo; no recomputar desde extremos.",
        "activation": "Fecha/cuestionario confirmados, código C2 y universo U4 cotejados con la ficha vigente del instrumento. Abrir una sola vez la ola ENVIPE para ambas familias U4, sin abrir ENVIPE 2026 ni microdato de olas reservadas durante esta continuación.",
    },
    {
        "slug": "ENVIPE-EVASION-NORMA", "instrument": "ENVIPE", "target": "2027", "prior": "2025",
        "unit": "delito con BP1_20∈{1,2} y FAC_DEL", "estimand": "proporción conjunta ponderada evade_norma = (BP1_20=2 y BP1_23∈{04,05,06,08}) sobre delitos con BP1_20∈{1,2}, FAC_DEL; RESULT-EVASIONNORMA-A-P-EVADE",
        "calc": "CALC-EVASION-NORMA-0001-v1_1", "result": "RESULT-EVASIONNORMA-A-P-EVADE",
        "hash": "8076d9ff1e18ab1fe6ac7168600810580cabe99c1df9373ee21c8b40e9d2abe8",
        "support": "n delitos válidos ≥10,000, ≥100 estratos y ≥1,000 UPM; cero sin BP1_20, BP1_23, FAC_DEL o diseño. ENVIPE 2025: n=40,280, numerador=21,761 y 10,694 UPM; el CALC no conserva conteos de estratos/UPM únicos, que se exigirán al futuro ejecutor.",
        "missing": "Es tasa conjunta en todo el universo BP1_20∈{1,2}; BP1_23 sólo clasifica a no denunciados. Valores vacíos/código no válido se informan como faltante y nunca se imputan a 0. Si faltantes del disparador o desenlace superan 1% del peso potencial o la ausencia impide distinguir skip legítimo de pérdida, NO-ESTIMABLE.",
        "comparability": "Misma unidad delito, disparador BP1_20, códigos normalizados BP1_23, FAC_DEL, EST_DIS/UPM_DIS y categorías {04,05,06,08}. No comparar con el derivado persona/U4 ni con el condicional entre no denunciantes (no estimable en la spec vigente). Cambio en categorías que definen norma: NO-COMPARABLE.",
        "precision": "spec legado declara bootstrap de conglomerado estratificado, 10,000 réplicas, seed 42; punto 0.562774, IC95 [0.551982,0.573448], n=40,280. Sin vector guardado, no se deriva IC del error ni potencia; el futuro CALC debe exportar por réplica el resultado R y diferencia con piso. Se requieren n efectivo y conteos de estratos/UPM únicos.",
        "activation": "Condiciones comunes ENVIPE; verificar equivalencia BP1_20/BP1_23, categorías, universo de delitos y pesos de 2025. Una apertura compartida con denuncia-U4; mantener dos outcomes y sus soportes separados.",
    },
]


def body(f: dict) -> str:
    return f"""# FAMILIA-2027-{f['slug']} · spec humana condicional v1.1

**Estado: CONDICIONAL.** “2027” es etiqueta de trabajo. La publicación oficial está NO-CONFIRMADA en el calendario INEGI 2026 consultado el 23/sep/2026; no inferir fecha de levantamiento o publicación por el nombre. No se abre dato futuro.

## Estimando cerrado y piso

- Instrumento/ola objetivo: {f['instrument']} {f['target']}; referencia: {f['prior']}; fecha oficial de levantamiento y publicación: NO-CONFIRMADAS. Unidad: **{f['unit']}**, escala: proporción [0,1]. Estimando único: {f['estimand']}.
- Piso inmutable: `{f['result']}` de `{f['calc']}`, cuyo `sello.json` tiene SHA-256 `{f['hash']}`. La identidad del archivo y el valor RESULT se comprueban por separado; la tolerancia de este protocolo no altera la tolerancia numérica del CALC.
- Si una ola intermedia altera universo, reactivo, códigos o unidad, no se sustituye el piso ni se elige otro estimando después de ver R: se emite `NO-COMPARABLE` o `NO-ESTIMABLE` según la regla de abajo.

## Propuesta técnica para decisión pre-dato

- **Tolerancia material propuesta:** ±2.0 puntos porcentuales (pp) alrededor del punto fijo. Se propone como margen de discrepancia descriptiva y falsador local; no es tolerancia de reproducción de bytes y no prueba equivalencia psicológica/general. Reportar siempre el error absoluto continuo y el signo.
- **Soporte mínimo propuesto:** {f['support']} Debe cumplirse además un IC futuro computable con al menos 1,000 réplicas válidas de 2,000 planificadas y sin denominador nulo en más de 5% de réplicas. Incumplimiento: `NO-ESTIMABLE` (sin relajar umbrales tras R).
- **Faltantes:** {f['missing']}
- **Comparabilidad:** {f['comparability']}

## Dictamen prospectivo congelado

Antes de abrir la ola, COMMIT-1 congela especificación YAML, código, variables, pesos, universo, soporte, tratamiento de faltantes, regla de comparabilidad y semillas; se reserva una única apertura por instrumento y se reporta el primer resultado generado.

1. Estimar R con el estimando y soporte anteriores; usar el diseño oficial identificado en el cuestionario/descriptor. Bootstrap de UPM dentro de estrato, estrato conservado; compartir las réplicas para los dos outcomes de una misma ola cuando el universo y diseño lo permitan. No presentar IC exacto si estratos de UPM única aportan varianza cero.
2. Calcular por réplica `d_k = R_k - piso` y `e_k = abs(d_k)` usando pares del mismo remuestreo. Reportar IC95 percentil de `d_k`, MAE/error puntual y proporción de réplicas con `abs(d_k) ≤ 2 pp`. No reconstruir réplicas desde extremos de IC marginales.
3. Dictamen: `CALIBRADO-LOCAL` sólo si el punto cae dentro de ±2 pp **y** IC95 de `d` contiene cero **y** su anchura es interpretable bajo el diseño; significa compatibilidad local con este piso/ola/estimando, no calibración general. `DESVÍO-MATERIAL` si el IC95 queda completamente más allá de +2 o −2 pp. `INDETERMINADO` si el IC cruza un límite de ±2 pp, el intervalo no es interpretable o la precisión no permite clasificar. `NO-ESTIMABLE` por soporte/faltantes; `NO-COMPARABLE` por cambio de constructo/unidad.
4. El punto dentro del IC histórico por sí solo no genera `CALIBRADO`. Para una sola realización, se informa compatibilidad puntual y cobertura descriptiva; no se afirma cobertura nominal ni persistencia general. Sin un segundo objeto, ΔMAE y superioridad B-bis son `NO-APLICABLE`.

## Precisión disponible y brecha

{f['precision']}

La tolerancia ±2 pp es una decisión práctica propuesta, no una potencia acreditada. Efecto mínimo detectable, potencia y error tipo I **no son calculables** con los artefactos actuales. La condición de apertura exige guardar el vector por réplica, soporte efectivo y conteos de UPM/estratos; si esos archivos no se producen, el resultado futuro queda `INDETERMINADO` o `NO-ESTIMABLE`, nunca se fabrica incertidumbre.

## Condiciones verificables para activación

{f['activation']}

Además, las dos familias del mismo instrumento se evalúan en una sola apertura y un mismo paquete de réplica cuando técnicamente comparten diseño. Son dos estimandos predeclarados con resultados conjuntos, no dos oportunidades independientes de mirar R ni una selección de ganador.

Fuente de selección: catálogo U1, commit `0ac21b6c`. Este artefacto propone protocolo; no autoriza microdatos, olas reservadas, otro piloto, otro retador ni CALC en esta unidad.
"""


def main() -> None:
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
        path = OUT / f"FAMILIA-2027-{f['slug']}-spec-v1_1.md"
        text = body(f)
        path.write_text(text)
        digest = hashlib.sha256(text.encode()).hexdigest()
        path.with_name(path.name + ".sha256").write_text(f"{digest}  {path.name}\n")
    print(f"familias_actualizadas={len(FAMILIES)}")


if __name__ == "__main__":
    main()
