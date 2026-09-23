"""Contrato ENVIPE 2025 para cifra negra; ninguna apertura de microdato."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Psicología_Política_y_Comportamiento_Cívico_del_Mexicano_Contemporáneo__Una_Lectura_Anti-Esencialista_desde_Abajo__2026_.md"
FIELDS = ["id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente", "tier_report", "clase", "componente_contrastable", "limite_inferencial", "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina", "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen", "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente", "propietario", "siguiente_operacion", "prioridad"]
ROW = dict(
    id_afirmacion="ASTRA5-U0-POL-002", report=REPORT,
    localizador="L16", texto_vigente="La cifra oculta (93.2%) no es tolerancia al delito sino cálculo ante un sistema que no resuelve.",
    tier_report="FUERTE", clase="cifra publicada + atribución de mecanismo",
    componente_contrastable="Proporción de delitos experimentados en 2024 que no fueron denunciados o para los cuales no se inició carpeta; separar no denuncia y no apertura de carpeta.",
    limite_inferencial="La no denuncia/carpeta es respuesta y trámite por incidente; no identifica tolerancia cultural ni cálculo racional individual. No equiparar 93.2% a proporción de personas ni a delitos denunciados sin investigación efectiva. El diseño distingue factores de delitos del hogar 01-04 y personales 05-15 y ajusta repetición >5.",
    conducta_unidad_universo="Incidente delictivo reportado por persona seleccionada de 18+ en vivienda particular; hechos de 2024, encuesta ENVIPE 2025.",
    instrumento_ola="ENVIPE 2025, módulo de victimización para delitos de 2024",
    documento_id_hash_pagina="envipe2025_cuest_modulo_pdf|21df38610b21c481382dfb05cf8061e87216d97557c665b2e6e50aacaa216d27|§1 p. módulo;envipe2025_fd_pdf|83fe02467b661d64e8638d882b242b0e534b8383e683a3fcbeadd66ead777fad|BP1_20/BP1_21/BP1_24;envipe2025_diseno_muestral_pdf|f60661545c2980026619370b69b7d7d3988ab62100cfa7a9b33ac76b4a7f0e69|main e792419c|pp.10-11",
    pregunta_textual_codigo_respuestas="Módulo §1: 1.20 ‘¿Acudió ante el Ministerio Público o Fiscalía Estatal a denunciar el delito?’ BP1_20 1 Sí/2 No; 1.21 ‘¿Algún(a) otro(a) integrante de este hogar acudió a denunciar...?’ BP1_21 1 Sí/2 No (aplica por tipo delictivo); 1.24 ‘¿El Ministerio Público o Fiscalía Estatal abrió una carpeta de investigación?’ BP1_24 1 Sí/2 No/9 No sabe; filtros por delito y no respuesta según cuestionario/FD.",
    estado_verificacion="CERRADA", dictamen="MEDIBLE-EN-CORPUS",
    dictamen_razon="Microdato, módulo, FD y diseño ENVIPE 2025 tienen ids en main tras #1089/e792419c y SHA físicos coincidentes. La pregunta primaria se verificó; la cifra negra aún requiere reglas por tipo y factor de incidentes y no tiene RESULT adjudicado aquí.",
    datos_id_estado="envipe2025_csv|8a7a99fd90ce9d03229759ba0ad84db4fba98b5bb1f5c85eef7d718b007816fa|físico COINCIDE SHA; U0 no abrió microdato",
    reserva="ENVIPE 2026 permanece vedada; ENVIPE 2025 requiere verificación de condiciones de apertura en CAJA para nueva medición.",
    gen2_existente="Revisar CALC/RESULT ENVIPE 2025 ya sellados antes de duplicar; ninguna cifra GEN1 es input de GEN2.",
    propietario="ASTRA5-U3", siguiente_operacion="Fijar denominador de incidentes, filtro de delitos, denuncia/carpeta, factor por tipo y ajuste >5 antes de cualquier cálculo; cotejar RESULT solo con misma ola y universo.", prioridad="3",
)


def main() -> None:
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerow(ROW | {"report_sha256": hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest()})


if __name__ == "__main__":
    main()
