"""Contratos ENIF 2024: subcomponentes descriptivos del report financiero."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Behavioral_Finance_Mexicano__Estructura__Adaptación_Racional_y_Cultura_en_el_Ahorro__Crédito_y_Riesgo.md"
FIELDS = ["id_afirmacion", "report", "report_sha256", "localizador", "texto_vigente", "tier_report", "clase", "componente_contrastable", "limite_inferencial", "conducta_unidad_universo", "instrumento_ola", "documento_id_hash_pagina", "pregunta_textual_codigo_respuestas", "estado_verificacion", "dictamen", "dictamen_razon", "datos_id_estado", "reserva", "gen2_existente", "propietario", "siguiente_operacion", "prioridad"]
COMMON = dict(
    report=REPORT,
    report_sha256=hashlib.sha256((ROOT / REPORT).read_bytes()).hexdigest(),
    conducta_unidad_universo="Persona seleccionada de 18 años o más en vivienda particular; ENIF 2024 México, dominios nacional/localidad/región; denominador de cada reactivo según filtro.",
    instrumento_ola="ENIF 2024",
    documento_id_hash_pagina="enif2024_cuestionario_pdf|32e37cc13da38691dee20fbffcef3637aeb87b8dac194e64f83bebed8b57ef8b;enif2024_fd_xlsx|17e2ad86ce9e4fd5783ee54e9b51ee436b934e002d5736b82094070c74a25db2|TMODULO;enif2024_diseno_muestral_pdf|bc59f5f58c32831d3831a1a92ee6707e57e68caf68df1d573b8eb754e2259b76|#1088 RAMA, ausente de main",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Dato, cuestionario y FD ENIF 2024 tienen id y SHA físico coincidente; el diseño muestral oficial está registrado en #1088 y pendiente de merge a main. Texto/código de reactivo primario revisado.",
    datos_id_estado="enif2024_csv|a3507b4038888247f565f1640a718ef552bb8fc363378e3372a5bf2796bb2e4c|físico COINCIDE SHA; U0 no abrió microdato",
    reserva="Verificar autorización de apertura de ENIF 2024 y reglas de confidencialidad en CAJA; esta lectura fue documental.",
    gen2_existente="Revisar RESULT ENIF ya sellados por reactivo/universo antes de nueva corrida; no importar valores GEN1.",
    propietario="ASTRA5-MESA-DINERO",
    siguiente_operacion="Tras merge de #1088, cambiar a MEDIBLE-EN-CORPUS; cotejar alias y RESULT existentes; preregistrar denominador y medición en CAJA.",
    prioridad="4",
)
ROWS = [
    dict(id_afirmacion="ASTRA5-U0-FIN-001", localizador="L9", texto_vigente="Coexisten ahorro formal e informal: 36.6% solo informal, 21.6% ambos, 8.2% solo formal y 33.6% ninguno (ENIF 2024).", tier_report="FUERTE", clase="cifra publicada + síntesis", componente_contrastable="Clasificación exhaustiva de ahorro informal 5.1 y ahorro en cuentas 5.6 durante últimos 12 meses, con cuatro categorías mutuamente excluyentes.", limite_inferencial="Tenencia de cuenta 5.4 no equivale a ahorro efectivo 5.6; prevalencias no prueban que el circuito sea racional ni infraestructura social.", pregunta_textual_codigo_respuestas="Cuestionario §5 pp.12-13: 5.1 ‘En los últimos 12 meses... ¿usted...?’ P5_1_1..6; 5.6 ‘¿usted guardó o ahorró en su [cuenta]?’ P5_6_1..9; 1 Sí/2 No; 5.6 solo para cuenta con 5.4=1. Excluir blanco/no aplica.") ,
    dict(id_afirmacion="ASTRA5-U0-FIN-002", localizador="L11", texto_vigente="Las tandas/cundinas son infraestructura financiera masiva; reporta participación en tandas entre ahorradores ENIF 2024.", tier_report="FUERTE-MEDIA", clase="cifra publicada + interpretación", componente_contrastable="Proporción de adultos que participaron en tanda en los últimos 12 meses y proporción entre quienes reportan cualquier ahorro; cada denominador por separado.", limite_inferencial="P5_1_5 no mide tamaño de la tanda, función de infraestructura ni causalidad de bancarización. Los porcentajes 22% y 32% del report tienen denominadores distintos que requieren reconstrucción.", pregunta_textual_codigo_respuestas="Cuestionario §5 p.12: 5.1 opción 5 ‘¿participó en una tanda?’; FD TMODULO P5_1_5; 1 Sí/2 No; blanco/no aplica fuera del universo.") ,
    dict(id_afirmacion="ASTRA5-U0-FIN-003", localizador="L25", texto_vigente="Brecha de género: 68.0% de hombres vs 58.6% de mujeres tenían cuenta de ahorro formal; 51.4% vs 34.2% tenían afore (ENIF 2024).", tier_report="FUERTE", clase="dos cifras publicadas", componente_contrastable="Tenencia de cuentas 5.4 y de afore 9.1 desagregadas por sexo; especificar si ‘cuenta de ahorro formal’ es cualquier cuenta o 5.4 opción 4.", limite_inferencial="Una diferencia descriptiva por sexo no demuestra mecanismo estructural; el 68.0/58.6 puede corresponder a cualquier cuenta y requiere definición oficial antes de cotejo numérico.", pregunta_textual_codigo_respuestas="Cuestionario §5 p.13: 5.4 ‘¿Usted tiene...?’ P5_4_1..9, 1 Sí/2 No; §9 p.25: 9.1 ‘¿Usted tiene una cuenta de ahorro para el retiro o afore?’ P9_1, 1 Sí/2 No/9 No sabe; sexo de TMODULO/TSDEM.") ,
    dict(id_afirmacion="ASTRA5-U0-FIN-004", localizador="L27", texto_vigente="42.2% tiene afore y 7.9% de ellos hace aportaciones voluntarias (ENIF 2024).", tier_report="FUERTE", clase="cifras publicadas", componente_contrastable="Tenencia de afore P9_1 y aportación voluntaria P9_3 entre quienes tienen afore.", limite_inferencial="P9_3 tiene filtro P9_1=Sí; 7.9% no es proporción de todos los adultos. Las expectativas de depender de apoyos o trabajar en vejez requieren otro reactivo y no quedan contrastadas aquí.", pregunta_textual_codigo_respuestas="Cuestionario §9 pp.25-26: 9.1 ‘¿Usted tiene una cuenta de ahorro para el retiro o afore?’ P9_1, 1 Sí/2 No/9 No sabe; 9.3 ‘¿Usted realiza aportaciones voluntarias a su cuenta de ahorro para el retiro o afore?’ P9_3, 1 Sí/2 No, solo P9_1=1.") ,
    dict(id_afirmacion="ASTRA5-U0-FIN-005", localizador="L29", texto_vigente="Solo 22.9% de adultos tiene algún seguro en ENIF 2024; el report lo llama producto más rezagado.", tier_report="FUERTE", clase="cifra publicada + comparación", componente_contrastable="Tenencia actual de seguro no social según P8_1 en adultos 18+; comparar con otros productos solo armonizando definiciones.", limite_inferencial="P8_1 excluye IMSS, ISSSTE y otros servicios públicos; no mide cobertura de seguridad social ni demuestra que sea el producto más rezagado sin comparar mismos universos. Caída desde 2015 exige armonización de ola.", pregunta_textual_codigo_respuestas="Cuestionario §8 p.23: 8.1 ‘¿Usted tiene algún seguro de auto, de casa, de vida, de gastos médicos u otro (sin considerar... imss o issste)?’ FD TMODULO P8_1; 1 Sí/2 No/9 No sabe.") ,
]


def main() -> None:
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in ROWS:
            writer.writerow(COMMON | row)


if __name__ == "__main__":
    main()
