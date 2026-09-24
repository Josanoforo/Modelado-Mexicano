"""Contrato documental ENUT 2024 para la brecha de trabajo no remunerado."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md"
FIELDS = ["id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente", "tier_report", "clase", "componente_contrastable", "limite_inferencial", "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina", "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen", "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente", "propietario", "siguiente_operacion", "prioridad"]

ROW = dict(
    id_afirmacion="ASTRA5-U0-TIME-002",
    report=REPORT,
    report_sha256=hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest(),
    localizador="L20; §3 Mapa de evidencia",
    texto_vigente="Mujeres 39.7 y hombres 18.2 horas semanales de trabajo no remunerado; brecha 21.5 horas y cerca de 26 horas en localidades menores a 10 000 habitantes (ENUT 2024). El report infiere menor tiempo disponible para planear/comprometerse.",
    tier_report="MEDIA-FUERTE",
    clase="cifras publicadas + inferencia sobre planeación",
    componente_contrastable="Media de horas semanales de trabajo doméstico, cuidados, comunitario y voluntario por sexo y tamaño de localidad; cotejar construcción de TRAB_NO_REM_VOL y denominador oficial antes de reproducir 39.7/18.2/26.",
    limite_inferencial="Horas no remuneradas no miden directamente planeación ni compromiso temporal. La diferencia no identifica causalidad. Trabajo de autoconsumo y cuidado pasivo requieren tratamiento separado; no sumar variables creadas indiscriminadamente.",
    conducta_unidad_universo="Persona de 12 años o más, residente habitual de vivienda particular en México; actividades de la semana previa; estimaciones nacional y por localidad <10 000 / ≥10 000, con FAC_PER y diseño estratificado multietápico.",
    instrumento_ola="ENUT 2024",
    documento_id_hash_pagina="enut2024_cuestionario_pdf|949752e35fbc54fbe513466eb7caab32cef5010f046cb7777aa8490832769a62|sección VI;enut2024_fd_xlsx|4a7dddf1bc0612f5e72694b146848804edc47d8f00c86e7d34d1cfb8f5ec3f58|TVAR_CREA filas 35/181;enut2024_diseno_muestral_pdf|441a0cc229d62ce7b4829e847738b2b3b631ef05b44958e85b47148ecedbd2a2|§1.2-1.4; #1090 integrado en main 74b28f30",
    pregunta_textual_codigo_respuestas="Cuestionario §VI: ‘Enseguida le preguntaré por el tiempo que utilizó para realizar sus actividades de la semana pasada, es decir, de lunes a domingo’; bloques 6.3-6.17 preguntan actividad Sí/No y ‘¿Cuánto tiempo le dedicó...?’ en horas/minutos de lunes-viernes y sábado-domingo. FD TVAR_CREA fila 35: TRAB_NO_REM_VOL = trabajo no remunerado doméstico, de cuidados y voluntario; fila 181 FAC_PER. Reconstrucción exacta de la variable creada y ceros/no respuesta por cotejar antes de medir.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-EN-CORPUS",
    dictamen_razon="Dato, FD, cuestionario y diseño ENUT 2024 tienen id en main tras #1090; cuatro SHA físicos COINCIDEN. La media es medible, no la inferencia causal sobre planeación.",
    datos_id_estado="enut2024_bd_csv|25f35626464053441b367b24001d255dbca408b5f576e614e0e09ac58691c4ba|físico COINCIDE SHA; U0 no abrió microdato",
    reserva="CAJA verifica permiso de apertura ENUT 2024; el ZIP no se abrió en U0.",
    gen2_existente="Buscar RESULT ENUT 2024 compatible por variable, denominador, sexo y localidad; la corrida previa R5.2 de cuidados no es por sí un RESULT de esta brecha.",
    propietario="ASTRA5-U1",
    siguiente_operacion="U1 consume ids integrados; fija composición de TRAB_NO_REM_VOL, no respuesta, denominador y estimación por sexo/localidad antes de medir.",
    prioridad="3",
)

POBREZA_ESTATAL = dict(
    report=REPORT,
    report_sha256=ROW["report_sha256"],
    localizador="L63; repetición L134",
    tier_report="sin rótulo explícito",
    clase="prevalencia estatal publicada y mecanismo hipotético",
    limite_inferencial="La proporción estatal de pobreza multidimensional no mide horizonte individual de planeación ni demuestra un efecto de escasez. Estados y personas son unidades diferentes; no inferir conducta personal por agregados.",
    conducta_unidad_universo="Personas residentes en la entidad indicada, ENIGH 2024 y metodología INEGI/CONEVAL de pobreza multidimensional, no hogares ni ocupados.",
    instrumento_ola="INEGI Pobreza Multidimensional 2024, reporte 27/25 de 13-ago-2025",
    documento_id_hash_pagina="SIN-ID:pm2024_reporte_resultados.pdf|4da28fe9a3d74633d0275e4c5567576caade48b57aa12b81fecfd9db6781a4f9|p.10, gráficas 6-7; copia física local, sin registro en main; misma fuente de MER-010..012",
    pregunta_textual_codigo_respuestas="Indicador derivado de ingreso corriente per cápita y carencias conforme a metodología CONEVAL retomada por INEGI; no reactivo de planeación temporal.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Porcentaje y unidad publicados en reporte oficial con SHA físico cotejado; falta id documental y RESULT por entidad. Solo se cierra el agregado, no mecanismo psicológico.",
    datos_id_estado="enigh2024_nc_csv|7cbf18fee02c58849356e5495fb851ae4d0330743e34d26e35973f9ad5a1155d|main, microdato NO ABIERTO",
    reserva="Términos de Libre Uso INEGI; registro por MESA-DOCUMENTAL y apertura solo en CAJA autorizada.",
    gen2_existente="Sin RESULT propio de pobreza multidimensional estatal 2024 identificado en main.",
    propietario="ASTRA5-MESA-MOVILIDAD / ASTRA5-U1",
    siguiente_operacion="MESA-DOCUMENTAL registra reporte; U1 no transfiere prevalencia estatal a conducta individual y busca estudio de mecanismo de planeación por separado.",
    prioridad="3",
)

ROWS = [
    ROW,
    POBREZA_ESTATAL | dict(id_afirmacion="ASTRA5-U0-TIME-003", texto_vigente="La pobreza multidimensional en Chiapas fue 66.0% en 2024.", componente_contrastable="INEGI reporte 27/25 p.10, gráficas 6-7: Chiapas 66.0% de personas."),
    POBREZA_ESTATAL | dict(id_afirmacion="ASTRA5-U0-TIME-004", texto_vigente="La pobreza multidimensional en Guerrero fue 58.1% en 2024.", componente_contrastable="INEGI reporte 27/25 p.10, gráficas 6-7: Guerrero 58.1% de personas."),
    POBREZA_ESTATAL | dict(id_afirmacion="ASTRA5-U0-TIME-005", texto_vigente="La pobreza multidimensional en Oaxaca fue 51.6% en 2024.", componente_contrastable="INEGI reporte 27/25 p.10, gráficas 6-7: Oaxaca 51.6% de personas."),
]


def main() -> None:
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)


if __name__ == "__main__":
    main()
