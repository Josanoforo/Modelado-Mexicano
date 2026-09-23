"""Corte documental de confianza institucional en LAPOP 2023."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Psicología_Política_y_Comportamiento_Cívico_del_Mexicano_Contemporáneo__Una_Lectura_Anti-Esencialista_desde_Abajo__2026_.md"
FIELDS = [
    "id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente",
    "tier_report", "clase", "componente_contrastable", "limite_inferencial",
    "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina",
    "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen",
    "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente",
    "propietario", "siguiente_operacion", "prioridad",
]
ROW = dict(
    id_afirmacion="ASTRA5-U0-POL-001",
    report=REPORT,
    localizador="L14, Hallazgo 1",
    texto_vigente="La jerarquía de confianza institucional es una calibración racional del desempeño; confianza alta en instituciones que funcionan, baja en partidos y policía.",
    tier_report="FUERTE",
    clase="conclusión interpretativa con cifras publicadas",
    componente_contrastable="Distribución comparada de confianza declarada en policía y partidos políticos; no se usan porcentajes de otras fuentes como si fueran LAPOP.",
    limite_inferencial="B18/B21 no preguntan desempeño, extorsión ni mecanismo de calibración racional. No prueban causalidad ni confianza en familia, universidad o Marina con este par de reactivos.",
    conducta_unidad_universo="Persona mexicana de edad para votar; LAPOP México 2023, muestra probabilística nacional (N=1,622 en reporte técnico).",
    instrumento_ola="AmericasBarometer/LAPOP México 2023",
    documento_id_hash_pagina="lapop_abmex2023_cuestionario_mexico|0cf179c783d74f779eb7b0f0d880a59d6bfbd0c4ae53e394563f7a26c954b2d2|p.16;abmex2023_technical_report_v4_0_final_eng_231117|f12f33d7c957f2020eb3e7a2c49e9bc21fe0372b501f753fcbfcb929541e4b05",
    pregunta_textual_codigo_respuestas="B18 ‘¿Hasta qué punto tiene confianza usted en la Policía?’; B21 ‘¿Hasta qué punto tiene usted confianza en los partidos políticos?’; ambos 1 Nada–7 Mucho, 888888 No sabe y 988888 No responde.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-EN-CORPUS",
    dictamen_razon="Cuestionario, reporte técnico de diseño y microdato México 2023 ya tienen ids en manifiesto. El PDF técnico físico contrastado por SHA coincide; disponibilidad física del microdato en raíz descargas_mx pendiente de CAJA.",
    datos_id_estado="mex_2023_lapop_americasbarometer_v1_0_w|4a9410a53cde9d11edeb23465bdbadce8a6abcc18330b6eebe2a4493be6e765c|raíz descargas_mx NO CONFIGURADA aquí; hash declarado, no recalculado",
    reserva="Datos sujetos a licencia click de LAPOP y reglas de protección de respondentes; verificar condiciones y permiso de apertura antes de CAJA.",
    gen2_existente="Consumir mediciones de confianza ya selladas si su pregunta/universo coinciden; no hay RESULT nuevo aquí.",
    propietario="ASTRA5-U3",
    siguiente_operacion="Montar raíz descargas_mx en CAJA, verificar hash/licencia del dataset existente y preregistrar escala y diseño. No volver a descargar el reporte técnico.",
    prioridad="3",
)


def main():
    row = ROW | {"report_sha256": hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest()}
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
