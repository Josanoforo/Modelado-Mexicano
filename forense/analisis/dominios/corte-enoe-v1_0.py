"""Corte verificado de afirmaciones ENOE; no estima valores ni abre microdatos."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT_TIME = "corpus/reports/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md"
REPORT_WORK = "corpus/reports/Psicología_del_Trabajo_en_México__Un_Mapa_Basado_en_Evidencia.md"
DOC_Q = "enoe_cuestionario_basico_v7_pdf|7ee25f114a493cd4136bb086f7fa3a2f6db1fe7300dc5839ec2a7de9c3efa698"
DOC_FD = "enoe_123_fd_c_bas_amp_pdf|920a1db58ee30527bae48d0d1f45e47c8f17a9302b2dc743cf296228aa205a61"
DATA = "enoe_2024_3t_csv|f384a1b8872e051856ed2241289400302b13a8701489b1c596390452c183cd01"
DESIGN = "enoe_n_diseno_muestral.pdf|42eaa300fcbd4bec98c2a38f3edb5912bcc2208fe69a54a0c1103b75a85dbd09"

COMMON = dict(
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Datos, cuestionario y FD registrados; falta exclusivamente registrar diseño muestral ENOE N en manifiesto. PDF oficial leído y hash recalculado.",
    conducta_unidad_universo="Persona de 15 años o más en vivienda particular; denominador específico por variable; ENOE 2024 T3 básico.",
    instrumento_ola="ENOE 2024 T3, cuestionario básico v7",
    documento_id_hash_pagina=f"{DOC_Q};{DOC_FD};diseño externo:{DESIGN}",
    datos_id_estado=f"{DATA};físico COINCIDE SHA, microdato NO ABIERTO",
    reserva="ENOE ola más reciente reservada; 2024 T3 solo hash de envoltura comprobado, no leído",
    gen2_existente="Reusar contratos ENOE del repo; ningún RESULT nuevo en este acto",
    propietario="ASTRA5-U1",
    siguiente_operacion="Registrar exclusivamente el PDF de diseño muestral en manifiesto mediante adquisición documental autorizada; luego preregistrar estimando y abrir ola no reservada en CAJA.",
    prioridad="1",
)

ROWS = [
    dict(
        id_afirmacion="ASTRA5-U0-ENOE-001",
        report=REPORT_TIME,
        localizador="L14",
        texto_vigente="La informalidad laboral se ubicó en 55.7% de la población ocupada en 2024; esto es contexto estructural, no cultura.",
        tier_report="FUERTE",
        clase="cifra publicada + interpretación",
        componente_contrastable="Proporción de ocupados con empleo informal en 2024 T3 (punto trimestral, no reproduce automáticamente la cifra anual publicada).",
        limite_inferencial="EMP_PPAL describe clasificación laboral; no observa horizonte de planeación, racionalidad psicológica ni causa cultural. La cifra de 2026 requiere ola reservada y no se contrasta aquí.",
        pregunta_textual_codigo_respuestas="COE P1: ‘¿La semana pasada trabajó por lo menos una hora?’ (p.2, 1 Sí/2 No); FD SDEM EMP_PPAL (p.27, 1 empleo informal/2 formal); EMP_PPAL es variable derivada, no respuesta directa.",
    ),
    dict(
        id_afirmacion="ASTRA5-U0-ENOE-002",
        report=REPORT_WORK,
        localizador="L3",
        texto_vigente="Over half work without a formal contract.",
        tier_report="NO-EXPLÍCITO",
        clase="cifra publicada sin tier local",
        componente_contrastable="Entre trabajadores subordinados elegibles, proporción sin contrato escrito en empleo principal.",
        limite_inferencial="Contrato escrito no equivale a formalidad laboral completa; la base de todos los ocupados no es el universo de P3I. No comprueba confianza, lealtad ni relación con jefe.",
        pregunta_textual_codigo_respuestas="COE P3i: ‘¿En este empleo... cuenta con un contrato por escrito?’ (p.5); FD COE1 P3I (p.72, 1 Sí/2 No/9 No sabe; blanco/no aplica según filtro).",
    ),
    dict(
        id_afirmacion="ASTRA5-U0-ENOE-003",
        report=REPORT_WORK,
        localizador="L59",
        texto_vigente="28.7% working over 50 hours, en el argumento sobre largas jornadas y estrés.",
        tier_report="NO-EXPLÍCITO",
        clase="cifra publicada sin tier local",
        componente_contrastable="Proporción de ocupados que trabajaron más de 50 horas en la semana de referencia.",
        limite_inferencial="Horas semanales no prueban burnout, presentismo, vínculo emocional ni jornada anual de 2,207 horas; no se importa el 28.7% como resultado GEN2.",
        pregunta_textual_codigo_respuestas="COE P5b: ‘¿Qué días y cuántas horas le dedicó... a su trabajo la semana pasada?’ (p.7); FD COE1 P5B_THRS (p.76, 001–998 horas, 999 no especificado); excluir códigos no sustantivos según spec.",
    ),
]


def main():
    keys = ["id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente", "tier_report", "clase", "componente_contrastable", "limite_inferencial", "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina", "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen", "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente", "propietario", "siguiente_operacion", "prioridad"]
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, keys, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in ROWS:
            full = COMMON | row
            full["report_sha256"] = hashlib.sha256((ROOT / full["report"]).read_bytes()).hexdigest()
            writer.writerow(full)


if __name__ == "__main__":
    main()
