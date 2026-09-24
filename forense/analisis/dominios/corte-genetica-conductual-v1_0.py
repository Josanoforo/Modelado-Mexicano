"""Contratos de la revisión publicada de estudios PRS, sin inferencia mexicana."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Genetica_y_Conducta_del_Mexicano_Contemporaneo__Canal_Individual_vs__Estructura.md"
FIELDS = [
    "id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente",
    "tier_report", "clase", "componente_contrastable", "limite_inferencial",
    "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina",
    "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen",
    "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente",
    "propietario", "siguiente_operacion", "prioridad",
]
SHA = hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest()
BASE = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L199; síntesis L214,L224,L228",
    tier_report="sin rótulo explícito",
    clase="revisión bibliográfica de representación en estudios poligénicos",
    limite_inferencial="Son porcentajes de publicaciones, no de participantes ni de precisión predictiva; el 3.8% combina tres categorías y no estima la fracción mexicana. Las frecuencias 2008-17 no describen automáticamente la literatura actual ni validan puntuación clínica.",
    conducta_unidad_universo="733 estudios de polygenic scoring publicados entre 2008 y 2017, identificados por búsqueda PubMed 23/ene/2018 y criterios de Duncan et al.; unidad de recuento estudio, no individuo.",
    instrumento_ola="Duncan et al., Nature Communications 10:3328 (2019), DOI 10.1038/s41467-019-11112-0; revisión 2008–2017",
    documento_id_hash_pagina="SIN-ID:duncan2019_prs_ncomms.pdf|a5a08fa5c0bebd52705b295513300911e0e8839ab23b604b6447bb9f531fc9a8|pp.1-2 Fig.1 y p.7 Métodos;https://www.laramieduncan.com/_files/ugd/e135a9_2674e9e2791a4628b57264b6f8aa8ca9.pdf",
    pregunta_textual_codigo_respuestas="Sin reactivo de encuesta: revisión PRISMA de estudios PRS; búsqueda produjo 1,226 registros, 733 estudios de puntuación poligénica elegibles. Clasificación de ascendencia de cohortes según publicaciones originales.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Artículo final primario CC BY 4.0 con PDF/SHA físicos y método/denominador cotejados; se cierran solo proporciones publicadas de estudios. Id documental y RESULT propios faltan.",
    datos_id_estado="Lista suplementaria de 733 estudios no abierta/descargada por U0; sin RESULT propio.",
    reserva="Artículo CC BY 4.0; PDF físico local, registro documental pendiente. No trasladar a prevalencia genética, conducta grupal o rendimiento de PRS mexicano.",
    gen2_existente="Sin RESULT de revisión PRS 2008–17 compatible en main.",
    propietario="ASTRA5-MESA-GENETICA / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar artículo/licencia/hash y suplemento; para actualidad repetir revisión con corte propio; para México exigir evaluación predictiva independiente por rasgo.",
    prioridad="3",
)
LINNER = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L17; detalle L120-L129; síntesis L214,L228",
    tier_report="sin rótulo explícito",
    clase="GWAS y validación predictiva de tolerancia general al riesgo",
    limite_inferencial="124 es número de SNP líderes, no de loci: esos SNP están en 99 loci para tolerancia general. El artículo final cuenta 444 loci distintos fusionados entre siete fenotipos; 611 loci es cifra de una versión de trabajo, no la final. El R² incremental de 1.6% en una cohorte UKB de hermanos no es predicción individual confiable ni efecto en mexicanos. No compara su peso causal con precio, impuestos o estructura social mexicana.",
    conducta_unidad_universo="GWAS general de tolerancia al riesgo: n=939,908 descubrimiento UKB/23andMe, muestras de ascendencia europea; score LDpred validado en UKB-siblings n≈35,000, excluyendo la cohorte de entrenamiento; siete fenotipos relacionados para recuento global de loci.",
    instrumento_ola="Karlsson Linnér et al., Nature Genetics 51:245–257 (2019), DOI 10.1038/s41588-018-0309-3, artículo final",
    documento_id_hash_pagina="SIN-ID:linner2019_ngen_final.pdf|a2f4515e35d2c5d3ee36fe95c855a58e07a7f559a54843d95243da760fb9e63d|pp.245-248 Fig.1/Tabla1;https://personal.eur.nl/thurik/Research/Articles/NG%20Risk%20Linner%20et%20al%202019.pdf;trabajo-2018:3e25e4125486d3d9967f7ea163777119d806fe922d2bf532ca9fadbe2c57828a",
    pregunta_textual_codigo_respuestas="Tolerancia general al riesgo: autorreporte de disposición a asumir riesgos; score LDpred; poder predictivo es aumento de R² tras controlar sexo, año de nacimiento y diez componentes principales. No cuestionario mexicano.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Artículo final primario de coautor físico con DOI/SHA, cifras y método leídos. Se separa versión de trabajo de publicación final; no hay id documental ni RESULT propio.",
    datos_id_estado="Genotipos UKB/23andMe y cohortes de validación no abiertos/descargados U0; sin RESULT propio.",
    reserva="© autores bajo licencia exclusiva Springer Nature 2019; PDF solo local, no redistribuir. No trasladar a predicción individual, grupo mexicano o jerarquía causal sin evidencia propia.",
    gen2_existente="Sin RESULT GWAS/PRS Karlsson Linnér compatible en main.",
    propietario="ASTRA5-MESA-GENETICA / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar referencia/versión/hash/condiciones; cotejar suplemento de variantes y R² por cohorte. Para México requerir validación y un estimando causal de entorno comparable.",
    prioridad="3",
)
ROWS = [
    BASE | dict(
        id_afirmacion="ASTRA5-U0-GENBEH-001",
        texto_vigente="Duncan et al. encontraron que 67% de 733 estudios PRS publicados de 2008 a 2017 incluyeron exclusivamente participantes de ascendencia europea.",
        componente_contrastable="Proporción de estudios con cohorte exclusivamente europea en revisión de 733 estudios PRS, no porcentaje de GWAS generales ni de participantes.",
    ),
    BASE | dict(
        id_afirmacion="ASTRA5-U0-GENBEH-002",
        texto_vigente="En la misma revisión 2008–2017, solo 3.8% de estudios PRS concernieron a cohortes africanas, latinas/hispanas o indígenas combinadas.",
        componente_contrastable="Porcentaje combinado de estudios de tres grupos en revisión de 733 publicaciones; no 3.8% para cada grupo ni población mexicana.",
    ),
    LINNER | dict(
        id_afirmacion="ASTRA5-U0-GENBEH-003",
        texto_vigente="El GWAS final de Karlsson Linnér et al. identificó 124 SNP líderes de tolerancia general al riesgo, agrupados en 99 loci, en una muestra de descubrimiento n=939,908.",
        componente_contrastable="124 SNP líderes independientes aproximados (LD r²<0.1) en 99 loci definidos por LD/vecindad; no 124 loci como dice el report.",
    ),
    LINNER | dict(
        id_afirmacion="ASTRA5-U0-GENBEH-004",
        texto_vigente="Al fusionar asociaciones de siete GWAS de rasgos relacionados, el artículo final reportó 444 loci distintos.",
        componente_contrastable="703 asociaciones de locus entre siete GWAS se fusionan por distancia ≤250 kb en 444 loci distintos en el artículo final; el 611 del report corresponde a otra versión/definición y no se adopta como cifra final.",
    ),
    LINNER | dict(
        id_afirmacion="ASTRA5-U0-GENBEH-005",
        texto_vigente="El score LDpred de tolerancia general al riesgo añadió 1.6 puntos porcentuales de R² en la cohorte de validación UKB-siblings, n≈35,000.",
        componente_contrastable="R² incremental 1.6% tras sexo, año de nacimiento y diez PCs, usando GWAS que excluyó UKB-siblings; no es porcentaje de conducta causada por un gen ni utilidad clínica mexicana.",
        localizador="L125-L127; síntesis L214,L228",
    ),
]


def main():
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)


if __name__ == "__main__":
    main()
