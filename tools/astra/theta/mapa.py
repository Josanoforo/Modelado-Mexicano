"""Deriva el universo ASTRA-2 desde procedencia sin leer microdatos.

Los campos de diseño son una lectura documental conservadora. Un RESULT
propuesto identifica la fila del mapa; no representa una corrida ni adopción.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "milpa/procedencia.yaml"
OUT = ROOT / "forense/analisis/astra-theta/mapa-v1_0.tsv"
RELEVO = ROOT / "data/corrida0/relevo-usos-v1_0.tsv"

REPORTS = {
    "G1": "corpus/reports/Confianza_y_Desconfianza_en_México__Anatomía_Psicológica_de_una_Sociedad_Dual.md",
    "G2": "corpus/reports/El_Clasemediero_Mexicano__Identidad__Ansiedad_de_Estatus_y_el_Miedo_Racional_a_Caer.md",
    "G3": "corpus/reports/El_Mexicano_y_el_Tiempo__Estructura__no_Cultura__en_la_Planeación_y_el_Compromiso_Temporal.md",
    "G4": "corpus/reports/El_Efecto_Ambiental_de_la_Violencia_Crónica_en_México__Cómo_el_Miedo_Reorganiza_la_Conducta_Psicológica_de_la_Población.md",
    "G5": "corpus/reports/La_familia_mexicana_como_sistema_psicológico__entre_el_afecto__la_obligación_y_la_adaptación_económica.md",
    "G6": "corpus/reports/Autoridad_y_jerarquía_en_el_México_contemporáneo__anatomía_psicológica_de_un_sistema_dual.md",
    "dinero": "corpus/reports/Behavioral_Finance_Mexicano__Estructura__Adaptación_Racional_y_Cultura_en_el_Ahorro__Crédito_y_Riesgo.md",
    "salud": "corpus/reports/Health__Body__Food_and_Substance_Use_in_Mexico__The_Behavioral_Layer_of_Decisions__Environment_and_Structure.md",
    "tramite": "corpus/reports/Adopción_y_Resistencia_Tecnológica_en_México__La_Paradoja_de_la_Baja_Confianza_Institucional.md",
    "civico": "corpus/reports/Psicología_Política_y_Comportamiento_Cívico_del_Mexicano_Contemporáneo__Una_Lectura_Anti-Esencialista_desde_Abajo__2026_.md",
}

COND_BLOCKS = (
    "condicionales_confianza_institucional",
    "condicionales_escalares",
    "condicionales_escalares_confianza_generica",
    "condicionales_escalares_exposicion_violencia",
    "condicionales_escalares_medido_nacional",
)

FIELDNAMES = (
    "id_mapa", "resultado_id", "tipo_necesidad", "consumidor",
    "llave_theta", "ruta_yaml", "regla_generador", "mecanismo_y_limite",
    "tier_estado", "fuentes_decisivas", "poblacion_unidad", "desenlace",
    "exposicion", "escala_enlace_vigente", "magnitud_faltante",
    "variacion_candidata", "diseno_y_fuente_asignacion", "datos_id_ola_geografia_llave",
    "reserva_disponibilidad", "supuesto_critico", "amenaza_principal",
    "falsador", "viabilidad", "proximo_paso",
)


def compact(value: object) -> str:
    if isinstance(value, (list, dict)):
        return yaml.safe_dump(value, allow_unicode=True, default_flow_style=True).strip()
    return " ".join(str(value or "").split())


def basic(kind: str, consumer: str, key: str, path: str) -> dict[str, str]:
    number = basic.counter = basic.counter + 1
    return {
        "id_mapa": f"AT-{number:02d}",
        "resultado_id": "",
        "tipo_necesidad": kind,
        "consumidor": consumer,
        "llave_theta": key,
        "ruta_yaml": path,
        "regla_generador": consumer,
        "mecanismo_y_limite": "Hipótesis del canon; la dirección del corpus no identifica esta magnitud.",
        "tier_estado": "ASOCIACION/ASIGNADO según procedencia; ARGUMENTO_EXPLICITO=0 en E1",
        "fuentes_decisivas": "canon/integrador-psicologia-mexicano.md | canon/modelo-decision-v4_0.md | milpa/procedencia.yaml",
        "poblacion_unidad": "Por fijar según instrumento; evitar transporte fuera de su marco",
        "desenlace": "Conducta nombrada por el consumidor; definición exacta pendiente",
        "exposicion": key,
        "escala_enlace_vigente": "NO-DECLARADO para efecto causal; verificar esquema E1/ADR-220",
        "magnitud_faltante": "Contraste identificado compatible con la llave y su universo",
        "variacion_candidata": "SIN-VARIACIÓN-CONOCIDA-EN-UNIVERSO-REVISADO",
        "diseno_y_fuente_asignacion": "No preregistrable sin fuente primaria de asignación",
        "datos_id_ola_geografia_llave": "Revisados catálogo de fuentes, procedencia y registro de llaves; sin enlace causal acreditado",
        "reserva_disponibilidad": "No abrir reserva:*; disponibilidad de microdato por confirmar",
        "supuesto_critico": "Asignación independiente de desenlaces potenciales, condicionada según diseño",
        "amenaza_principal": "Confusión estructural y selección",
        "falsador": "Contraste pretratamiento/placebo adecuado a una asignación todavía no localizada",
        "viabilidad": "SIN-DISEÑO-IDENTIFICADO",
        "proximo_paso": "Buscar fuente primaria de variación y cotejar reactivo/geografía antes de spec",
    }


basic.counter = 0


def main() -> None:
    p = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
    canon_lines = (ROOT / "canon/modelo-decision-v4_0.md").read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, str]] = []
    sealed = {(x["gen"], x["coef"]): x for x in p["coeficientes_generador_sellados"]}
    sealed_index = {(x["gen"], x["coef"]): i for i, x in enumerate(p["coeficientes_generador_sellados"])}
    assert len(sealed) == 7
    for group_index, group in enumerate(p["asignados_coeficiente"]["detalle"]):
        gen = group["gen"]
        for coef, assigned in group["coefs"].items():
            path = f"asignados_coeficiente.detalle[{group_index}].coefs.{coef}"
            row = basic("coeficiente_ejecutable" if (gen, coef) in sealed else "coeficiente_asignado", f"generador:{gen}", f"{gen}.{coef}", path)
            row["fuentes_decisivas"] += " | " + REPORTS[gen] + " | forense/estado-motor-v1_0.md"
            row["mecanismo_y_limite"] = f"{gen} utiliza {coef}; signo asignado={assigned}. El corpus fundamenta mecanismo/dirección, no la magnitud causal."
            row["magnitud_faltante"] = f"Efecto causal de {coef} sobre salida de {gen}, no el β̂ asociativo existente"
            if (gen, coef) in sealed:
                s = sealed[(gen, coef)]
                row["ruta_yaml"] = f"coeficientes_generador_sellados[{sealed_index[(gen, coef)]}]"
                row["fuentes_decisivas"] += " | milpa/procedencia.yaml:" + path
                row["escala_enlace_vigente"] = compact(s["escala"])
                row["tier_estado"] = compact(s["rotulo"])
                row["datos_id_ola_geografia_llave"] = compact(s["fuente"])
                row["reserva_disponibilidad"] = "Medición previa abierta según procedencia; verificar ola antes de nueva lectura"
            if gen == "G3" and coef == "horizonte_temporal":
                row["datos_id_ola_geografia_llave"] = "ENNViH olas 2-3; CAL-G3, forense/registro-llaves-identificacion-v1_0.md"
                row["amenaza_principal"] = "Confusión temporal intra-persona aun con primeras diferencias"
                row["variacion_candidata"] = "CAL-G3: variación intra-persona ENNViH, no asignación exógena"
                row["diseno_y_fuente_asignacion"] = "Primeras diferencias ya corridas; fuente de shock exógeno al horizonte no localizada"
                row["viabilidad"] = "PANEL-DISPONIBLE-SIN-IDENTIFICACION-CAUSAL"
            if coef in {"sens_estatus", "aversion_riesgo", "deferencia", "familismo_obligacion"}:
                row["viabilidad"] = "FALTA-MEDICION/ESCALA"
                row["proximo_paso"] = "Validar reactivo del constructo en población mexicana y enlace de escala antes de buscar asignación"
            rows.append(row)

    assert len(rows) == 15
    for index, item in enumerate(p["asignados_probabilidad"]):
        key = item["regla"]
        family = key.split(".")[0]
        row = basic("asignado_probabilidad", f"regla:{key}", key, f"asignados_probabilidad[{index}]")
        row["fuentes_decisivas"] += " | " + REPORTS[family] + " | " + compact(item.get("fuente_citada"))
        row["mecanismo_y_limite"] = compact(item.get("que_sostiene_de_verdad"))
        row["magnitud_faltante"] = "Probabilidad condicional causal/estructural de conducta; vector asignado=" + compact(item["valores"])
        row["poblacion_unidad"] = "Persona elegible para la regla; verificar dominio del instrumento"
        row["desenlace"] = key
        row["exposicion"] = "Condición SI del texto literal en canon/modelo-decision-v4_0.md §3"
        matches = [(line_no, line) for line_no, line in enumerate(canon_lines, 1)
                   if re.search(r"`" + re.escape(key) + r"`", line)
                   and "**SI**" in line and "**id:**" in line]
        if matches:
            line_no, line = matches[-1]
            row["regla_generador"] = f"canon/modelo-decision-v4_0.md:{line_no}:{key}"
            row["exposicion"] = compact(line.split("**ENTONCES**")[0].replace("**SI**", "SI"))[:450]
            row["desenlace"] = compact(line.split("**ENTONCES**", 1)[1].split("— PORQUE", 1)[0])[:450]
            row["fuentes_decisivas"] += f" | canon/modelo-decision-v4_0.md:{line_no}"
            if key == "civico.denuncia.con_seguro":
                row["exposicion"] = "Robo de vehículo asegurado; cobertura previa al delito"
                row["desenlace"] = "Denuncia del robo para activar trámite del seguro"
            if key == "tramite.gobierno_digital.util_sin_coercion":
                row["exposicion"] = "Oferta de servicio digital útil y sin amenaza coercitiva"
                row["desenlace"] = "Adopción del servicio digital"
        if family == "tramite":
            row["datos_id_ola_geografia_llave"] = "ENCIG 2021/2023: encig_2021_encig21_base_datos_csv / encig23_base_datos_csv, estatal urbano alto; ID_TRA+ID_PER, P7_1/P7_2 lugar del trámite, P7_3 canal; calendario de asignación ausente"
            row["fuentes_decisivas"] += " | forense/analisis/astra-theta-adq/recibo-encig-historica.md@1d99b5f0"
            row["reserva_disponibilidad"] = "2021/2023 accesibles y hash verificado por apoyo adq; 2017/2019/2025 requieren cotejo de id/hash antes de consumo"
            row["amenaza_principal"] = "Digitalización endógena, mezcla de trámite y selección de usuarios"
            if key in {"tramite.mordida.discrecional", "tramite.mordida.con_registro"}:
                row["fuentes_decisivas"] += " | " + REPORTS["civico"]
                row["variacion_candidata"] = "Oferta de renovación vehicular digital por entidad/año; CDMX 2019 y Tabasco 2023 documentados, calendario nacional incompleto"
                row["diseno_y_fuente_asignacion"] = "DiD entidad×trámite×ola candidato; comunicados ADIP/SEMOVI y Tabasco; fecha efectiva/servicios y controles por verificar"
                row["datos_id_ola_geografia_llave"] = "ENCIG 2017/2019/2021/2023/2025, entidad×código 05; 2021/23 IDs verificados encig_2021_encig21_base_datos_csv/encig23_base_datos_csv; ID_TRA+ID_PER, P7_1/P7_2 lugar, P7_3 canal, P8_3 mordida; 05 mezcla servicios"
                row["viabilidad"] = "FALTA-CALENDARIO-Y-TRATAMIENTO-EXACTO"
                row["proximo_paso"] = "Adquirir calendario y cobertura efectiva por servicio; cotejar code 05 y soporte antes de congelar"
        elif family == "salud":
            row["datos_id_ola_geografia_llave"] = "ENSANUT: ola, geografía y texto de atención por cotejar documentalmente"
            row["amenaza_principal"] = "Necesidad de salud y acceso simultáneos; oferta endógena"
            if key == "salud.atencion.leve_sin_imss":
                row["fuentes_decisivas"] += " | King et al. 2009 Seguro Popular DOI:10.7910/DVN/P6NC0M, README y codebooks públicos"
                row["poblacion_unidad"] = "Adultos sin IMSS al inicio en 100 conglomerados de salud de seis estados; residencia define conglomerado"
                row["desenlace"] = "Evento conjunto de consulta respiratoria en farmacia en seguimiento, no P(farmacia|necesidad leve) del θ"
                row["exposicion"] = "Sorteo de oferta Seguro Popular + mejora de instalaciones/medicamentos en 50 pares de conglomerados"
                row["variacion_candidata"] = "Asignación aleatoria inicial de 74 pares; 50 pares en seguimiento analítico 2005-06 (selección de pares a auditar)"
                row["diseno_y_fuente_asignacion"] = "ITT por pares; fuente primaria Eval/define.treatment.R y Eval/control.matches.R de la réplica DOI:10.7910/DVN/P6NC0M"
                row["datos_id_ola_geografia_llave"] = "ALL.tab + clustmatchlist.tab adquiridos por #1037; 647 columnas ALL omiten P11D0401/P11D0501 y P10E0401/P10E0501_T2; tablas de visitas originales faltantes"
                row["reserva_disponibilidad"] = "Dataverse V6.2 registrado por adq@37cfd059; hashes verificados; términos recomiendan contacto; encabezado leído solo tras freeze c529cdf0"
                row["supuesto_critico"] = "Aleatorización por pares intacta; atrición no diferencial; códigos comparables; no condicionar en consulta posterior"
                row["amenaza_principal"] = "Intervención compuesta y desenlace conjunto: no identifica probabilidad condicional θ ni consultorio anexo"
                row["falsador"] = "Balance basal del mismo evento y de IMSS; atrición por brazo; integridad de 50 pares"
                row["viabilidad"] = "ASIGNACION-ALEATORIA; NO-ESTIMABLE-EN-REPLICA-PUBLICA-PARA-EFECTO-REDUCIDO; NO-THETA-DIRECTO"
                row["proximo_paso"] = "Obtener tabla de visitas basal y homóloga final, seguro individual y llaves; auditar 74 pares iniciales frente a 50 observados antes de estimar"
        elif key == "civico.denuncia.con_seguro":
            row["datos_id_ola_geografia_llave"] = "ENVIPE 2025; sin usar cruces reservados ASTRA-1 ni ENVIPE 2026"
            row["amenaza_principal"] = "Aseguramiento seleccionado por ingreso, vehículo, delito y zona"
            row["variacion_candidata"] = "Cambio legal de cobertura automotriz federal por año/modelo; enlace a variables ENVIPE no comprobado"
            row["viabilidad"] = "FALTA-LLAVE-DE-EXPOSICION-Y-ASIGNACION"
        if key == "tramite.gobierno_digital.coercitivo":
            row["tier_estado"] = "REFUTADO-POR-COTA; prior no consumible"
            row["viabilidad"] = "NO-CONSUMIBLE-VIGENTE"
        rows.append(row)

    assert len(rows) == 28
    for block in COND_BLOCKS:
        for name, item in p[block].items():
            if not isinstance(item, dict) or "clase" not in item:
                continue
            path = f"{block}.{name}"
            row = basic("condicional_theta", f"Theta.valor:{name}", name, path)
            row["regla_generador"] = "milpa/src/theta.py:Theta.valor; correspondencia con generador por canon §2"
            row["tier_estado"] = compact(item["clase"])
            row["fuentes_decisivas"] += " | " + compact(item.get("fuente"))
            row["mecanismo_y_limite"] = "Distribución del constructo ya medida en dominio declarado; no identifica respuesta causal de una conducta."
            row["poblacion_unidad"] = compact(item.get("universo") or item.get("fuente"))[:350]
            row["desenlace"] = "Distribución condicional de " + name
            row["exposicion"] = compact(item.get("eje_condicionante"))
            row["magnitud_faltante"] = "Distribución θ(x) cargable para celdas autorizadas; causalidad separada"
            row["datos_id_ola_geografia_llave"] = compact(item.get("fuente"))[:500]
            row["escala_enlace_vigente"] = "milpa/theta-esquema-e1-v1_0.yaml:" + name + "; no inferir enlace causal"
            row["supuesto_critico"] = "Comparabilidad del reactivo y soporte de celdas; no implica identificación causal"
            row["viabilidad"] = "MEDICION-PARCIAL-SIN-CARGA-E1"
            row["proximo_paso"] = "Cruzar esquema E1 y consumidor real; medir sólo celdas con soporte y decisión de adopción"
            rows.append(row)

    assert len(rows) == 40, len(rows)
    assert [sum(r["tipo_necesidad"] == k for r in rows) for k in (
        "coeficiente_ejecutable", "coeficiente_asignado", "asignado_probabilidad", "condicional_theta"
    )] == [7, 8, 13, 12]
    with RELEVO.open(encoding="utf-8", newline="") as file:
        next(file)  # comentario '# DERIVADO — NO EDITAR'
        relevo = [r for r in csv.DictReader(file, delimiter="\t")
                  if r["consumidor"].startswith("milpa/procedencia.yaml:")]
    assert len(relevo) == 40
    by_identity = {}
    for r in relevo:
        kind = r["tipo_uso"]
        token = r["consumidor"].rsplit(":", 1)[1]
        by_identity[(kind, token)] = r
    assert len(by_identity) == 40
    for row in rows:
        kind = row["tipo_necesidad"]
        if kind == "condicional_theta":
            block, name = row["ruta_yaml"].split(".", 1)
            token = f"{block}/{name}"
        else:
            token = row["llave_theta"]
        source = by_identity.pop((kind, token))
        assert source["veredicto"] == "SIN-CANDIDATO"
        row["resultado_id"] = source["resultado_id"]
        row["consumidor"] = source["consumidor"]
        row["fuentes_decisivas"] += " | data/corrida0/relevo-usos-v1_0.tsv:" + source["resultado_id"]
    assert not by_identity
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} filas -> {OUT}")


if __name__ == "__main__":
    main()
