import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]

REL_FIELDS = [
    "worker_id", "necesidad_id", "fuente_canonica", "objeto_evidencia_id",
    "estado_anterior", "estado_propuesto", "tipo_resultado", "evidencia_ref",
    "evidencia_localizador", "evidencia_explicita", "razon",
    "reserva_incertidumbre", "requiere_decision_humana", "siguiente_accion",
]
EVI_FIELDS = [
    "necesidad_id", "fuente_canonica", "objeto_evidencia_id", "tipo_evidencia",
    "evidencia_ref", "evidencia_localizador", "variable_reactivo_tabla",
    "texto_evidencia", "unidad_observacion", "periodo", "universo_muestra",
    "codificacion", "parte_necesidad_cubierta", "parte_necesidad_no_cubierta",
    "uso_potencial_modelo", "transformacion_requerida", "incertidumbre",
    "traza_revision", "siguiente_accion",
]

SOURCE_GAPS = {
    "ENSAFI": ("El registro local describe una hipótesis de variable, pero no aporta diccionario ni texto literal del reactivo para este objeto.", "Abrir el cuestionario/diccionario ENSAFI correspondiente y verificar texto, codificación y desenlace coobservado."),
    "ENCOAP": ("La ficha local documenta diseño, dominios y acceso, pero deja pendiente el mapeo de variables del objeto.", "Abrir cuestionario y diccionario ENCOAP; localizar el reactivo y el desenlace exactos exigidos por la necesidad."),
    "GDELT": ("La ficha local confirma campos de evento y geografía, no una extracción México depurada ni la construcción específica de esta necesidad.", "Extraer un universo México acotado, aplicar deduplicación documentada y mapear CAMEO/actores/respuesta al objeto."),
    "MEXICO_ENTERPRISE_SURVEYS_COMPONENTE_PANEL_CANDIDATO_2006_2010": ("La documentación registra 293 filas y una llave panel candidata, pero no verifica continuidad, comparabilidad ni las variables específicas de la necesidad.", "Abrir diccionario y archivo panel; comprobar dos observaciones por idPANEL2006 y mapear predictor y desenlace requeridos."),
    "MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO": ("El proyecto está indexado, pero el archivo México y su codebook no están descargados ni abiertos localmente.", "Obtener archivo y codebook del proyecto; verificar evento, actor, demanda, respuesta, geografía y cobertura temporal para México."),
    "PUB": ("El padrón está registrado como EN-DISCO-SIN-VERIFICAR y no hay microdato o diccionario abierto para este objeto.", "Localizar el payload oficial concreto del padrón y abrir diccionario/llaves antes de evaluar el vínculo causal o de participación."),
    "WVS": ("La documentación local confirma la fuente y México, pero no reabre variables mexicanas ni codificación para este objeto.", "Abrir cuestionario y codebook Wave 7 México; localizar reactivo, codificación y desenlace coobservado."),
    "BASE_DE_EVENTOS_DE_PROTESTA_EN_MEXICO": ("La ficha local confirma una base de eventos potencial, pero señala acceso por contacto y codebook no disponible.", "Solicitar acceso puntual a la base y codebook; verificar fecha, actor, demanda, respuesta y geografía."),
    "CNGMD": ("La ficha abre el módulo de participación a nivel municipal, pero no mapea comité, contribución sostenida o sanción y no observa conducta individual.", "Abrir cuestionarios de los módulos 2/7 y mapear variables; usar solo como contexto municipal si no existe unidad individual."),
    "ENAFIN": ("La fuente está en portal sin descarga local y no hay variables abiertas para la relación.", "Descargar el levantamiento y diccionario ENAFIN pertinente; mapear variable y desenlace concretos de la necesidad."),
    "ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_DE_LA_POBLACION": ("La ficha documenta microdatos/manuales 2019–2024 y algunos reactivos, pero no el mapeo exacto de este objeto ni comparabilidad entre años.", "Abrir manual y microdato del año objetivo; verificar texto, codificación, comparabilidad y desenlace coobservado."),
    "ENOE": ("El catálogo confirma archivos ENOE en disco, pero la candidatura no identifica un reactivo que mida sanción creíble, utilidad o cinismo.", "Buscar de forma dirigida en diccionarios ENOE una variable explícita del constructo; si no existe, delimitar ausencia por módulos revisados."),
    "IMPACT_EVALUATION_OF_PARENTAL_EMPOWERMENT_PROGRAM": ("La ficha confirma estudio y un archivo endline, pero no abre asignación, llave ni medidas exactas de contribución/sanción.", "Abrir DDI/codebook y datos; verificar asignación, llaves, participación parental y outcome escolar."),
    "MICROCREDIT_IMPACTS_COMPARTAMOS_RCT": ("La ficha confirma RCT, tratamiento y outcomes, pero declara no documentado el reactivo explícito de sensibilidad de estatus.", "Abrir codebook y buscar el reactivo literal de estatus; no inferirlo de gasto, crédito o bienestar."),
    "PRICE_AND_INFORMATION_TYPE_IN_LIFE_MICROINSURANCE_DEMAND": ("La ficha confirma experimento de precio/información y compra, pero los datos/codebook no están localizados y no identifica el comparador exacto.", "Localizar anexos o codebook y verificar brazos, codificación de precio/información y compra efectiva."),
    "REPOSITORIOS_UNAM_COLMEX_ITAM_DATAVERSE_ICPSR": ("La entrada refiere repositorios agregados, no un estudio/payload canónico abierto con diseño alrededor de umbral.", "Identificar un estudio concreto ya indexado, abrir protocolo/datos y verificar umbral, asignación y outcome electoral."),
    "ENFIH2019_FD_XLSX": ("La apertura local no identifica evidencia suficiente para este objeto específico.", "Abrir el diccionario ENFIH y localizar texto y codificación exactos para el constructo y su desenlace coobservado."),
}

rows = list(csv.DictReader((ROOT / "input-candidatas.tsv").open(encoding="utf-8"), delimiter="\t"))
assert len(rows) == 39

relations, evidence = [], []
for r in rows:
    nid, src, oid = r["necesidad_id"], r["fuente_id_canonico"], r["objeto_evidencia_id"]
    ref = r["evidencia_ref"].split(";")[0] if r["evidencia_ref"] else "NO_DETERMINADO"
    locator = f"{nid}|{src}|{oid}"
    gap, action = SOURCE_GAPS[src]
    proposed = "CANDIDATA"
    result_type = "CANDIDATA_CON_CARENCIA"
    explicit = r["evidencia_textual_breve"] or "La ficha local solo indexa la fuente; no contiene evidencia concreta adjudicable para esta relación."
    reason = gap
    covered = "La fuente o dominio temático está identificado en el universo reunido."
    not_covered = gap
    evi_type = "FICHA_LOCAL_NO_CONCLUYENTE"
    var = "NO_DETERMINADO"
    unit = "NO_DETERMINADO"
    period = "NO_DETERMINADO"
    universe = "NO_DETERMINADO"
    coding = "NO_DETERMINADO"
    use = "NO_DETERMINADO hasta verificar la evidencia concreta."
    transform = "NO_APLICA antes de verificar instrumento y variables."

    if nid == "N12" and src == "ENFIH2019_FD_XLSX" and oid == "OE-826b60a87b39ab2aec89c752":
        proposed = "NEGATIVA"
        result_type = "EXISTE-NO-SATISFACE"
        ref = "MAIN:data/abrir4-variables-2026-08-08.tsv:L12"
        locator = "P11_1_5"
        explicit = "11.1 Si hoy tuviera una urgencia economica igual a lo que gana o recibe en un mes, ¿usted podria pagarla con un prestamo de amigos o familiares?"
        reason = "El reactivo mide capacidad percibida de afrontar una urgencia puntual mediante préstamo familiar; no mide una disposición general de apoyo/familismo."
        covered = "Afrontamiento financiero hipotético mediante amigos o familiares."
        not_covered = "Disposición general de apoyo familiar no circular y su conducta asociada."
        action = "Conservar como negativa fuente-específica; buscar un reactivo disposicional solo en una futura fuente ya identificada."
        evi_type = "REACTIVO_EXPLICITO"
        var = "P11_1_5"
        unit = "persona"
        period = "ENFIH 2019"
        universe = "muestra ENFIH 2019; detalle no reabierto en esta ronda"
        coding = "binario Sí/No"
        use = "Indicador de recurso de afrontamiento puntual; no parámetro de familismo_apoyo."
        transform = "Codificación binaria si se usa únicamente como coping financiero."

    relations.append({
        "worker_id": "worker-3", "necesidad_id": nid, "fuente_canonica": src,
        "objeto_evidencia_id": oid, "estado_anterior": "CANDIDATA",
        "estado_propuesto": proposed, "tipo_resultado": result_type,
        "evidencia_ref": ref, "evidencia_localizador": locator,
        "evidencia_explicita": explicit, "razon": reason,
        "reserva_incertidumbre": "La conclusión se limita a la evidencia local abierta; no se infiere contenido ausente.",
        "requiere_decision_humana": "NO", "siguiente_accion": action,
    })
    evidence.append({
        "necesidad_id": nid, "fuente_canonica": src, "objeto_evidencia_id": oid,
        "tipo_evidencia": evi_type, "evidencia_ref": ref,
        "evidencia_localizador": locator, "variable_reactivo_tabla": var,
        "texto_evidencia": explicit, "unidad_observacion": unit, "periodo": period,
        "universo_muestra": universe, "codificacion": coding,
        "parte_necesidad_cubierta": covered, "parte_necesidad_no_cubierta": not_covered,
        "uso_potencial_modelo": use, "transformacion_requerida": transform,
        "incertidumbre": "No se extrapola de la fuente a otras necesidades ni de una ficha temática a evidencia explícita.",
        "traza_revision": f"Revisión dirigida de {ref}; contraste con input y contexto inmutable; sin discovery panorámico.",
        "siguiente_accion": action,
    })

with (ROOT / "worker-3-relaciones.tsv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, REL_FIELDS, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(relations)
with (ROOT / "worker-3-evidencia.tsv").open("w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, EVI_FIELDS, delimiter="\t", lineterminator="\n")
    w.writeheader(); w.writerows(evidence)

summary = {
    "fuentes_asignadas": len({r["fuente_id_canonico"] for r in rows}),
    "candidatas_asignadas": len(rows),
    "candidatas_devuelta": len(relations),
    "confirmadas_nuevas": sum(r["estado_propuesto"] == "CONFIRMADA" for r in relations),
    "negativas_nuevas": sum(r["estado_propuesto"] == "NEGATIVA" for r in relations),
    "candidatas_intactas": sum(r["estado_propuesto"] == "CANDIDATA" for r in relations),
    "no_accesibles_nuevas": sum(r["estado_propuesto"] == "NO_ACCESIBLE" for r in relations),
    "conflictos": sum(r["estado_propuesto"] == "CONFLICTO_MATERIAL" for r in relations),
    "decisiones_humanas": sum(r["requiere_decision_humana"] == "SI" for r in relations),
    "referencias_verificadas": sum(r["estado_propuesto"] in {"CONFIRMADA", "NEGATIVA"} for r in relations),
    "bloqueos": sum(r["tipo_resultado"] in {"BLOQUEO", "NO_ACCESIBLE"} for r in relations),
}
(ROOT / "worker-3-resumen.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
