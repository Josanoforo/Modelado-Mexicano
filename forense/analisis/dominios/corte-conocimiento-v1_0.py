"""Dictámenes documentales PISA 2022 del report de conocimiento."""

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_suffix(".tsv")
REPORT = "corpus/reports/Report_26__The_Contemporary_Mexican_and_Knowledge__Expertise__Education_and_Information_as_Decision_Behavior.md"
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
    localizador="L25,L58; PISA 2022",
    tier_report="FUERTE",
    clase="evaluación educativa internacional de estudiantes escolarizados",
    limite_inferencial="PISA evalúa estudiantes elegibles de 15 años en escuelas, no adultos, todos los jóvenes de 15 años ni actitudes de familias hacia educación. En México n=6288 alumnos de 280 escuelas representan cerca de 64% de la población total de 15 años. La tabla OCDE da intervalo de rango 54–64 para matemáticas, no sustenta lugar puntual 51/81 del report. Puntaje y proficiencia son estimandos distintos; ninguno identifica causalidad o valoración familiar.",
    conducta_unidad_universo="Estudiantes de 15 años inscritos en escuelas y elegibles de México en PISA 2022; 6288 participantes en 280 escuelas, representan aproximadamente 1,393,700 estudiantes y 64% de toda la cohorte de 15 años.",
    instrumento_ola="OECD PISA 2022 resultados matemáticas, lectura y ciencias; ficha México Vols. I-II 2023 y Vol. I tabla I.2.4/I.B1.2.1/I.B1.3.1",
    documento_id_hash_pagina="SIN-ID:astra5_oecd_pisa2022_mexico_factsheet.pdf|8be7ac8ca27f9b37bf142ed82e9b3342c7b67a2086dfe267d997c5055bfe0558|pp.1-3,8;https://www.oecd.org/content/dam/oecd/en/publications/reports/2023/11/pisa-2022-results-volume-i-and-ii-country-notes_2fca04b9/mexico_515c0d35/519eaf88-en.pdf;SIN-ID:astra5_oecd_pisa2022_volume1.pdf|84bb19ca15ba075b780bc0b37498510a5a53e2028bc8fbda19586ac88d21a025|pp.29,66 tabla I.2.4;https://www.oecd.org/content/dam/oecd/en/publications/reports/2023/12/pisa-2022-results-volume-i_76772a36/53f23881-en.pdf",
    pregunta_textual_codigo_respuestas="Prueba PISA de matemáticas 2022: puntuación escalada y umbral de nivel 2; no pregunta de aprecio o aspiración familiar.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Dos PDF primarios OCDE físicos con SHA, ola, tablas y universo leídos; falta id documental en manifiesto U0 y no hay RESULT propio.",
    datos_id_estado="Microdatos PISA no abiertos ni descargados U0; sin RESULT compatible.",
    reserva="© OECD 2023; PDF para lectura local, condiciones de redistribución por MESA-DOCUMENTAL. Evitar rango único 51/81 no acreditado y no inferir opinión de familias de rendimiento estudiantil.",
    gen2_existente="Sin RESULT PISA compatible en main.",
    propietario="ASTRA5-MESA-CONOCIMIENTO / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar dos PDF/versiones/licencia/SHA; contrastar tabla exacta y error de rango; adquirir pregunta de aspiración familiar por instrumento distinto.",
    prioridad="3",
)
ENPECYT = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L20,L78,L91; ENPECYT 2017",
    tier_report="FUERTE",
    clase="encuesta probabilística de actitudes a ciencia y tecnología",
    limite_inferencial="Adultos 18+ en viviendas de localidades urbanas ≥100 mil habitantes, no población nacional rural ni jóvenes. Interés en inventos/descubrimientos/tecnología es distinto de respetar a investigadores o apoyar gasto estatal. El boletín 272/18 reporta 92.2% en texto y 92.3% en numeralia para inversión; ficha web y boletín difieren en fechas de campo, pendientes de versión. No inferir confianza individual en científicos del interés agregado.",
    conducta_unidad_universo="Personas seleccionadas de 18 años y más en 3,200 viviendas de áreas urbanas de ≥100 mil habitantes, ENPECYT 2017 México; muestra estratificada por conglomerados/bietápica según ficha INEGI.",
    instrumento_ola="INEGI/CONACYT ENPECYT 2017, cuestionario sección IV A pregunta 1 rubro 3 y sección 25 pregunta 1; comunicado 272/18, 20/jun/2018",
    documento_id_hash_pagina="SIN-ID:astra5_enpecyt2017_boletin272_18.pdf|8cf0c1a6dc8addd7475b1e48e94d62e7f5fe9b32667185e0315ca9315203925c|pp.1-2, nota técnica/numeralia;https://en.www.inegi.org.mx/contenidos/saladeprensa/boletines/2018/OtrTemEcon/ENPECYT2018_06.pdf;SIN-ID:astra5_enpecyt2017_cuestionario.pdf|90526e38a60f476e1aa1124b7f5d8f496e45b78f091d2dcb2ffcc32913ceb281|sección IV A pregunta 1/ítem 3 y sección 25/ítem 1;https://www.inegi.org.mx/contenidos/programas/enpecyt/2017/doc/enpecyt2017_cuest.pdf",
    pregunta_textual_codigo_respuestas="Interés IV A P1 ítem3: muy grande=1, grande=2, moderado=3, nulo=4; inversión sección25 ítem1: muy de acuerdo=1, de acuerdo=2, en desacuerdo=3, muy en desacuerdo=4, no sabe=5.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Boletín y cuestionario INEGI físicos con SHA; universo y reactivos exactos leídos. El agregado 92.2/92.3 y fechas de campo requieren conciliación editorial; no RESULT propio ni ids U0.",
    datos_id_estado="Microdato ENPECYT no abierto/descargado U0; sin RESULT compatible.",
    reserva="Documentos oficiales para lectura local; registro/licencia por MESA-DOCUMENTAL. No extender a México rural ni unir con Wellcome regional. Boletín texto 92.2 versus numeralia 92.3 y fechas ficha/boletín discordantes.",
    gen2_existente="Sin RESULT ENPECYT compatible en main.",
    propietario="ASTRA5-MESA-CONOCIMIENTO / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar boletín/cuestionario/licencia/SHA; cotejar tabulado publicado y ficha metodológica para 92.2/92.3 y fechas, sin abrir microdatos antes de autorización.",
    prioridad="3",
)
WELLCOME = dict(
    report=REPORT,
    report_sha256=SHA,
    localizador="L20,L78,L91; Wellcome 2018",
    tier_report="FUERTE",
    clase="índice regional de confianza en científicos",
    limite_inferencial="El 27% agrega Centroamérica y México: Costa Rica, República Dominicana, El Salvador, Guatemala, Haití, Honduras, México, Nicaragua y Panamá. No es estimación exclusiva de México ni comparable directamente con interés ENPECYT urbano 18+. Índice de cinco ítems entre población 15+ Gallup World Poll, no una pregunta única ni medición de respeto al experto accesible.",
    conducta_unidad_universo="Personas 15+ de región Centroamérica y México en Gallup World Poll 2018/Wellcome Global Monitor; nueve países enumerados en capítulo 1.",
    instrumento_ola="Wellcome Global Monitor 2018, informe publicado 2019, Trust in Scientists Index, cinco ítems, rango 1–4; capítulo 3 y Box 3.2",
    documento_id_hash_pagina="SIN-ID:astra5_wellcome_global_monitor2018.pdf|eea01061dd982e280dba6964b38d3476a71610b029283bd9368661834435cb8d|pp.12,52-54;https://wellcome.org/sites/default/files/wellcome-global-monitor-2018.pdf",
    pregunta_textual_codigo_respuestas="Cinco ítems de confianza en científicos país, precisión, universidades beneficio público y transparencia de financiación, empresas beneficio público; mucho=4, algo=3, poco=2, nada=1; índice requiere ≥3 respuestas válidas, bajo 1 a <2.5.",
    estado_verificacion="CERRADA",
    dictamen="MEDIBLE-CON-ADQUISICIÓN",
    dictamen_razon="Informe primario físico con SHA, lista regional, universo y construcción del índice leídos; cierra atribución regional únicamente. Sin id documental ni RESULT México.",
    datos_id_estado="Microdato Wellcome/Gallup no abierto/descargado U0; sin RESULT México.",
    reserva="© Wellcome 2019, PDF para lectura local; registro/condiciones por MESA-DOCUMENTAL. Prohibido presentar 27% como México solo o como correlación individual con ENPECYT.",
    gen2_existente="Sin RESULT Wellcome país compatible en main.",
    propietario="ASTRA5-MESA-CONOCIMIENTO / ASTRA5-MESA-DOCUMENTAL",
    siguiente_operacion="Registrar PDF/SHA/licencia; si se requiere México aislado, obtener tabla país y corte índice con permiso y método antes de contrastar con ENPECYT.",
    prioridad="3",
)
ROWS = [
    BASE | dict(
        id_afirmacion="ASTRA5-U0-CONOC-001",
        texto_vigente="Los estudiantes mexicanos elegibles de 15 años obtuvieron una media de 395 puntos en matemáticas en PISA 2022.",
        componente_contrastable="OECD Vol. I Tabla I.2.4 p.66: media 395, IC95% 391–399; intervalo de rango 54–64 de 81 países/economías, por lo que 51º puntual del report no se valida.",
    ),
    BASE | dict(
        id_afirmacion="ASTRA5-U0-CONOC-002",
        texto_vigente="En PISA 2022, 66% de los estudiantes mexicanos evaluados quedó por debajo del nivel 2 de competencia matemática.",
        componente_contrastable="Ficha OCDE México pp.2-3: 34% alcanza al menos nivel 2, 66% por debajo; promedio OCDE 69% alcanza nivel 2. Esta tasa no mide rechazo a educación.",
    ),
    BASE | dict(
        id_afirmacion="ASTRA5-U0-CONOC-003",
        texto_vigente="La muestra PISA 2022 México incluyó 6,288 estudiantes en 280 escuelas y representó alrededor de 64% de la población total de 15 años.",
        componente_contrastable="Ficha OCDE México sección Key features/The students: n6288, 280 escuelas, ~1,393,700 estudiantes representados, 64% de cohorte de 15 años; deja fuera población no escolarizada/elegible.",
        localizador="L25,L58; universo y cobertura PISA",
    ),
    ENPECYT | dict(
        id_afirmacion="ASTRA5-U0-CONOC-004",
        texto_vigente="En ENPECYT 2017, 75.0% de adultos de áreas urbanas de 100 mil habitantes o más declaró interés al menos moderado por inventos, descubrimientos científicos o desarrollo tecnológico.",
        componente_contrastable="Boletín 272/18 p.1 y numeralia: 8.4% muy grande + 27.4% grande + 39.2% moderado = 75.0%; 25.0% nulo. Cuestionario IV A P1 ítem3. No equivale a interés por ciencia exacta ni confianza en científico.",
    ),
    ENPECYT | dict(
        id_afirmacion="ASTRA5-U0-CONOC-005",
        texto_vigente="El boletín ENPECYT 2017 atribuye alrededor de 92% de acuerdo con mayor inversión pública en investigación científica, con discrepancia interna 92.2% en texto y 92.3% en numeralia.",
        componente_contrastable="Cuestionario sección25 ítem1 códigos 1+2; comunicado 272/18 titular/cuerpo 92.2%, numeralia final total 92.3%. La diferencia 0.1 punto no se resuelve por selección arbitraria; no prueba confianza individual ni monto presupuestal.",
        localizador="L20,L78,L91; apoyo inversión y discrepancia",
    ),
    WELLCOME | dict(
        id_afirmacion="ASTRA5-U0-CONOC-006",
        texto_vigente="Wellcome Global Monitor 2018 reporta 27% de confianza baja en científicos para la región Centroamérica y México conjunta.",
        componente_contrastable="Informe 2019 cap.3 p.54: 27% bajo índice en nueve países de Centroamérica y México; Box 3.2 pp.52-53 construye índice de cinco preguntas. No es dato exclusivo de México ni misma muestra ENPECYT 2017.",
    ),
]


def main() -> None:
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(ROWS)


if __name__ == "__main__":
    main()
