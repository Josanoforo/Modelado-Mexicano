"""Contratos publicados de cohortes genómicas; no emite recomendaciones clínicas."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Mexican_Population_Genomics__2025-2026_Scientific_and_Market_Opportunity_Update.md"
FIELDS = [
    "id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente",
    "tier_report", "clase", "componente_contrastable", "limite_inferencial",
    "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina",
    "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen",
    "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente",
    "propietario", "siguiente_operacion", "prioridad",
]
SHA = hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest()
MEXVAR = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L29; repetición L11,L43",
    tier_report="sin rótulo explícito",
    clase="descripción de muestra y catálogo genómico publicados",
    limite_inferencial="Muestra genotipada de 6,011 personas y variantes curadas no constituyen prevalencia nacional de enfermedad ni validación de utilidad clínica. Las 42,769 variantes de relevancia biomédica proceden de bases heterogéneas y no son todas patogénicas, accionables o indicación de prueba/dosis. La plataforma no demuestra que paneles europeos fallen para cada mexicano.",
    conducta_unidad_universo="Mexican Biobank, 6,011 participantes de 898 localidades en 32 estados, genotipados con MEGA; individuos de la cohorte, no censo ni muestra probabilística nacional acreditada en este contrato.",
    instrumento_ola="Barberena-Jonas et al., Nature Medicine 2026, DOI 10.1038/s41591-025-04100-z, Mexican Biobank/MexVar",
    documento_id_hash_pagina="SIN-ID:mexvar2026_nmed.pdf|d7da73784aa63099d602756837be9635ac56452244446a6de0bbe807709be46c|pp.725-727 y Métodos;https://www.nature.com/articles/s41591-025-04100-z.pdf",
    pregunta_textual_codigo_respuestas="No encuesta de actitud. Genotipos MEGA de ~1.8 millones de variantes; las 42,769 variantes curadas están genotipadas en MXB y figuran en al menos una de PharmGKB, OMIM, ClinVar o GWAS Catalog. Definición de relevancia incluye riesgo, diagnóstico o respuesta, con niveles de evidencia distintos.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Artículo final primario físico con DOI/SHA/licencia cotejados; resumen, métodos y distinción curación/acción leídos. Falta id documental y RESULT independiente; se cierra solo agregado publicado.",
    datos_id_estado="MXB genotipos individuales no abiertos/descargados por U0; plataforma MexVar consultada como publicación agregada, sin RESULT propio.",
    reserva="Artículo CC BY 4.0 con atribución; PDF local, registro documental pendiente. Uso clínico, consentimiento y beneficio individual quedan fuera sin validación y autorización específicas.",
    gen2_existente="Sin RESULT propio compatible de MXB/MexVar identificado en main.",
    propietario="ASTRA5-MESA-GENOMICA / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Mesa documental registra DOI, versión, CC BY y SHA; mesa genómica coteja reporting summary/suplementos, criterios de inclusión y clases de evidencia antes de aplicaciones clínicas.",
    prioridad="3",
)
MCPS = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L31; repetición L12,L43",
    tier_report="sin rótulo explícito",
    clase="comparación de cohortes secuenciadas publicada",
    limite_inferencial="MCPS es cohorte de Ciudad de México, UKB cohorte de Reino Unido; sus miembros fueron seleccionados/filtrados genéticamente y difieren en edad, entorno y exposiciones. La razón de momios ajustada no es prevalencia nacional México/Reino Unido ni efecto causal de ascendencia o una intervención clínica.",
    conducta_unidad_universo="MCPS n=136,401 participantes de Ciudad de México con probabilidad ≥95% de ascendencia americana mezclada; UKB n=416,118 con probabilidad ≥95% europea; ambos tras control de calidad, secuenciación exómica y panel de 15 genes CH.",
    instrumento_ola="Wen et al., Nature Genetics 2025, DOI 10.1038/s41588-025-02085-6, MCPS vs UKB",
    documento_id_hash_pagina="SIN-ID:mcps_ch2025_ngen.pdf|b27b26fd8ed68a00541b34040dedb75649528c637d497f997cdce56dc3caeb3f|pp.572-574, Figura 1 y Métodos;https://www.nature.com/articles/s41588-025-02085-6.pdf",
    pregunta_textual_codigo_respuestas="CH: variantes somáticas detectadas por MuTect2 en exomas y filtradas contra catálogo predefinido de mutaciones en 15 genes impulsores validados; no reactivo de encuesta. Comparación logística de CH ajustada por edad, sexo y tabaquismo; sensibilidad añade cobertura de secuenciación.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Artículo final primario físico, SHA/DOI/licencia y resumen/método cotejados. Faltan id documental y RESULT independiente; se cierra cifra publicada sin abrir exomas ni afirmar causa.",
    datos_id_estado="Exomas MCPS/UKB NO ABIERTOS NI DESCARGADOS U0; sin RESULT propio compatible identificado.",
    reserva="Artículo CC BY 4.0 con atribución; PDF local, registro pendiente. No usar OR poblacional para consejo genético o cribado sin validez clínica y autorización.",
    gen2_existente="Sin RESULT propio CH MCPS vs UKB compatible en main.",
    propietario="ASTRA5-MESA-GENOMICA / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Mesa documental registra artículo/hash; mesa genómica coteja suplementos, definición de CH, covariables y sesgos de cohortes antes de inferencia clínica.",
    prioridad="3",
)
ROWS = [
    MEXVAR | dict(id_afirmacion="ASTRA5-U0-GENOM-001", texto_vigente="Mexican Biobank incluyó 6,011 personas de 898 localidades en los 32 estados en el artículo Nature Medicine 2026.", componente_contrastable="Tamaño y cobertura territorial del conjunto genotipado descritos por Barberena-Jonas et al.; la amplitud geográfica no certifica prevalencias nacionales representativas."),
    MEXVAR | dict(id_afirmacion="ASTRA5-U0-GENOM-002", texto_vigente="MexVar publicó resultados de frecuencia para 42,769 variantes genotipadas de relevancia biomédica de Mexican Biobank.", componente_contrastable="42,769 variantes curadas por presencia en bases biomédicas y genotipadas en MXB; subconjunto clínico de alto nivel es menor: 58 SNP PGx de 22 genes y 99 variantes ClinVar patogénicas/probablemente patogénicas con MAF no cero en 33 genes ACMG SF, según cuerpo del artículo.", siguiente_operacion="Registrar artículo/suplementos; separar 42,769 curadas de subgrupos PGx/ClinVar accionables y de cualquier resultado terapéutico individual."),
    MCPS | dict(id_afirmacion="ASTRA5-U0-GENOM-003", texto_vigente="En las cohortes exómicas seleccionadas, CH fue menos frecuente en MCPS que en UKB: OR ajustada MCPS/UKB 0.59 (IC95 0.57–0.61).", componente_contrastable="Nature Genetics 2025: MCPS n=136,401 y UKB n=416,118; CH 3.12% vs 4.92% con panel de 15 genes, OR ajustada MCPS/UKB 0.59, IC95 0.57–0.61; comparación de cohortes, no de países.", siguiente_operacion="Registrar artículo y suplementos; reproducir solo con gobernanza de datos autorizada, no usar OR como consejo individual ni atribuir diferencia solo a ancestría."),
]


def main():
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)


if __name__ == "__main__":
    main()
