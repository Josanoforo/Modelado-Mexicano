"""Hitos documentales del procedimiento CED art. 34; sin inferencia penal."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Ausencia_sin_certeza__duelo_y_pérdida_ambigua_en_familias_de_personas_desaparecidas_en_México.md"
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
    localizador="L18; desarrollo del procedimiento art. 34",
    tier_report="sin rótulo explícito",
    clase="acto institucional documentado",
    limite_inferencial="Documento del Comité contra la Desaparición Forzada, no sentencia penal ni decisión de la Asamblea General. La decisión de remitir la cuestión no prueba por sí sola un delito concreto, la culpabilidad de funcionarios o un efecto psicológico individual. El anuncio del presidente del 4/abr/2025 requiere pieza propia.",
    conducta_unidad_universo="Expediente México ante Comité CED en aplicación de artículo 34 de la Convención; unidad acto procesal, no encuesta ni persona desaparecida.",
    instrumento_ola="CED/C/MEX/A.34/D/1, decisión adoptada en 30º período 9-19/mar/2026, distribuida 17/abr/2026; párrafos 33-37 y 122-123",
    documento_id_hash_pagina="SIN-ID:ced_mex_a34_2026.pdf|39fe6ee50aba61739e3f9ff856498f2b05b67f9675c4afcb66b080cc1fa8a6db|pp.6,20 §III y §V;https://docstore.ohchr.org/SelfServices/FilesHandler.ashx?enc=%2BSInD1MGWlfLOwSnMLOch2VA6hZ%2Fe7GNMdQpcCejvaExNjNVcpZGWD0vB0cdB4VOcsB4aXawakh1Za19rldXZA%3D%3D;HTML-oficial:6bbabd7da0a84eae71351bf49e50646f973f0e866f78b7f21aa36e6e99074a66",
    pregunta_textual_codigo_respuestas="No cuestionario: lectura de párrafos de decisión ONU y fecha de distribución. Los actos de solicitud, respuesta, examen y remisión son etapas separadas.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Documento primario ONU completo PDF físico con símbolo, fecha, párrafo y SHA; copia HTML oficial previa con SHA distinta. No id en manifiesto por perímetro U0 ni RESULT analítico.",
    datos_id_estado="Documento público agregado; ningún microdato abierto ni RESULT compatible.",
    reserva="PDF/HTML oficiales conservados para lectura local; condiciones de redistribución por MESA-DOCUMENTAL. No convertir activación/remisión en condena, ni afirmar decisión posterior de Asamblea sin acto específico.",
    gen2_existente="No existe RESULT; afirmación es acto documental.",
    propietario="ASTRA5-MESA-DUELO / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar PDF/HTML, versión/condiciones/SHA; localizar anuncio 4/abr/2025 y eventual acto de Asamblea por símbolo y fecha antes de actualizar estado procesal.",
    prioridad="3",
)
ROWS = [
    BASE | dict(
        id_afirmacion="ASTRA5-U0-DUEL-001",
        texto_vigente="El CED decidió pedir información a México en su 28º período y presentó la solicitud conforme al artículo 34 el 24 de junio de 2025.",
        componente_contrastable="CED/C/MEX/A.34/D/1 párrs.33-34: documentación recibida febrero-abril 2025; Comité decidió solicitar información en 28º período y transmitió solicitud 24/jun/2025. No documenta en ese párrafo la frase de activación presidencial 4/abr.",
        localizador="L18, componente abril-junio 2025",
    ),
    BASE | dict(
        id_afirmacion="ASTRA5-U0-DUEL-002",
        texto_vigente="En decisión adoptada en marzo y distribuida el 17 de abril de 2026, el CED decidió llevar la situación de México a consideración de la Asamblea General y pidió transmitir la decisión.",
        componente_contrastable="CED/C/MEX/A.34/D/1 encabezado y párr.122: decisión de remisión a Asamblea General mediante Secretario General; el párr.123 plantea posibles medidas, no consigna que la Asamblea ya actuó.",
        localizador="L18, componente marzo-abril 2026",
    ),
    BASE | dict(
        id_afirmacion="ASTRA5-U0-DUEL-003",
        texto_vigente="El CED concluyó en el párr.121 que había indicios fundados de desapariciones forzadas en varios ataques generalizados o sistemáticos en México, con la calificación señalada en su decisión.",
        componente_contrastable="CED/C/MEX/A.34/D/1 párr.121: juicio de indicios fundados del Comité en procedimiento artículo 34; no es condena penal ni determinación de responsabilidad individual.",
        localizador="L18, componente indicios y calificación",
        siguiente_operacion="Registrar decisión y separar estándar de indicios del Comité de condena judicial; examinar eventual respuesta de Asamblea solo cuando exista acto propio.",
    ),
]


def main():
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)


if __name__ == "__main__":
    main()
