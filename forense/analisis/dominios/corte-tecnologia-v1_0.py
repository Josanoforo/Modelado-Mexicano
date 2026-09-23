"""Corte documental ENDUTIH y frontera MOCIBA; no abre microdatos."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Adopción_y_Resistencia_Tecnológica_en_México__La_Paradoja_de_la_Baja_Confianza_Institucional.md"

FIELDS = [
    "id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente",
    "tier_report", "clase", "componente_contrastable", "limite_inferencial",
    "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina",
    "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen",
    "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente",
    "propietario", "siguiente_operacion", "prioridad",
]

ROW = dict(
    id_afirmacion="ASTRA5-U0-TEC-001",
    report=REPORT,
    localizador="L17; corrección de alcance L94",
    texto_vigente="83.1% de la población de 6+ usó internet en 2024; del 16.9% que no usa, 9.5% ‘no sabe usarlo’; el report lo interpreta como barrera de alfabetización, no de actitud.",
    tier_report="SÓLIDO (rótulo propio; no se traduce a FUERTE)",
    clase="cifra publicada + interpretación",
    componente_contrastable="Uso de internet en tres meses (P7_1) y distribución de motivo principal de no uso (P7_2); proporciones separadas con denominadores explícitos.",
    limite_inferencial="Autorreporte de motivo único no identifica causa estructural ni preferencia latente; no autoriza inferencia específica sobre población indígena sin diseño representativo. 9.5% exige comprobar si el denominador publicado es toda la población o solo no usuarios.",
    conducta_unidad_universo="Persona elegida de 6 años o más en vivienda particular; P7_2 solo si P7_1=2; México 2024.",
    instrumento_ola="ENDUTIH 2024",
    documento_id_hash_pagina="endutih2024_cuestionario_pdf|95514c5fe0a000bfaf29062a9cf9225ec64674dbb83df6a44a3dceda13187800|p.8;endutih2024_fd_xlsx|ecdf95924b0b31e2593fdfabe69cf88ecbc5c90a40b3fa3caa9f8427147a96de|tic_2024_usuarios filas 101-110;endutih2024_diseno_muestral_pdf|97ee8088cd12d3112e1d0f3bf4bafb1bb11a9175b93b3dfb9bab61e08833b612",
    pregunta_textual_codigo_respuestas="7.1 ‘En los últimos tres meses, ¿ha utilizado internet en este hogar o fuera de él?’ P7_1: 1 Sí/2 No. 7.2 ‘¿Por qué no utiliza internet?’ P7_2: 1 sin acceso aunque sabe usarlo; 2 no sabe; 3 no interesa/necesita; 4 falta recursos; 5 discapacidad; 6 privacidad/seguridad; 7 no le permiten; 8 otra razón.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-EN-CORPUS",
    dictamen_razon="Datos, FD, cuestionario y diseño 2024 registrados en manifiesto; hashes físicos documentales coinciden. P7_1 y P7_2 tienen universos distintos.",
    datos_id_estado="endutih2024_bd_dbf_zip|ef723ed125c81c4a9036b74fab67f520de007a2d52c5e0b03d4ebec509e1ae87|físico COINCIDE SHA, microdato NO ABIERTO",
    reserva="Permiso de apertura por ola pendiente de comprobar en CAJA; ninguna apertura aquí.",
    gen2_existente="#1085 RAMA, ausente de main: RESULT-ENDUTIH-PISOS-2024-TABLA / CALC-ENDUTIH-PISOS-2024-0001 / resultados SHA 4c0a3b05b6ecef3e9d7e760163cc6a6691ceaf384fa522e620bbe9b663088c25; cotejar P7_2 por denominador.",
    propietario="ASTRA5-U4",
    siguiente_operacion="Consumir RESULT de #1085 solo con estado rama hasta merge y verificar que P7_1/P7_2 y denominadores coincidan con este contrato.",
    prioridad="2",
)


def main():
    row = ROW | {"report_sha256": hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest()}
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
