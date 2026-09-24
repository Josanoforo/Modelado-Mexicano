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
]


def main():
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)


if __name__ == "__main__":
    main()
