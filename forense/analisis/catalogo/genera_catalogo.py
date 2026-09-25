#!/usr/bin/env python3
"""Regenera el inventario de RESULT GEN2, pisos y propuestas.

La unidad de fila es RESULT de punto en su CALC, no extremo de intervalo ni
aparición documental. Las propuestas sin consumo figuran con ese estado,
sin convertirse en adopción por estar en la tabla.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[3]
CORRIDA = ROOT / "data/corrida0"
OUT = ROOT / "forense/analisis/catalogo/inventario-consumo-gen2.tsv"
csv.field_size_limit(sys.maxsize)

FIELDS = [
    "llave", "dominio", "conducta", "instrumento_ola", "segmento",
    "universo_denominador", "unidad_escala", "punto", "ic95_inf",
    "ic95_sup", "naturaleza_ic", "estado_adopcion", "firma", "temporalidad",
    "result_punto", "result_inf", "result_sup", "calc", "sha256_resultados",
    "sha256_sello", "uso", "oferta_compatible", "oferta_valor_ic", "reserva",
]

INSTRUMENT_FALLBACK = {
    "CALC-DINERO-FAMILIARES-VEJEZ-0001-v1_1": "ENIF 2024",
    "CALC-ENSANUT-0001": "ENSANUT 2024",
    "CALC-ENVIPE-RES0028-U4-DERIVADO-0001": "ENVIPE 2025",
    "CALC-EVASION-NORMA-0001-v1_1": "ENVIPE 2025",
    "CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1": "ENIF 2024 (derivado de RESULT)",
    "CALC-R-DIN-M-01-v4": "ENNViH-1 2002",
    "CALC-R-FAM-M-01-v3": "ENIF 2018",
    "CALC-R-TRA-M-02-v3": "ENCUCI 2020",
    "CALC-R-TRA-M-03-v3": "ENCIG 2013",
    "CALC-R-TRA-M-07-v3": "ENCIG 2021",
    "CALC-TIENE-AHORROS-0001-v1_1": "ENIF 2024",
}


# v1_0 quedó congelado (ACTO GEN2-CATALOGO-V1-1-1) sobre una vista que el
# canal `[deriva]` reemplaza. Con `CATALOGO_VISTA_REF=<commit>` las vistas
# derivadas se leen de ese commit y no del árbol: así la regeneración de v1_0
# se comprueba contra la vista con que se congeló, no contra la vigente.
VISTAS = {"resultados.tsv", "usos.tsv", "marcador-segmento.tsv", "corridas.tsv"}


def _lineas(name: str) -> list[str]:
    ref = os.environ.get("CATALOGO_VISTA_REF")
    if ref and name in VISTAS:
        texto = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{ref}:data/corrida0/{name}"],
            capture_output=True, check=True,
        ).stdout.decode("utf-8")
        return texto.splitlines(keepends=True)
    with (CORRIDA / name).open(newline="") as stream:
        return stream.readlines()


def tsv(name: str) -> list[dict[str, str]]:
    return list(csv.DictReader(
        (line for line in _lineas(name) if not line.startswith("#")),
        delimiter="\t",
    ))


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verified(calc: str) -> tuple[dict, str, str]:
    folder = CORRIDA / calc
    seal = folder / "sello.json"
    listed = (folder / "sello.sha256").read_text().split()[0]
    actual = digest(seal)
    if listed != actual:
        raise ValueError(f"sello.sha256 inválido: {calc}")
    mapping = json.loads(seal.read_text())
    result_file = folder / "resultados.json"
    result_hash = digest(result_file)
    if mapping["resultados.json"] != result_hash:
        raise ValueError(f"resultados.json inválido: {calc}")
    data = json.loads(result_file.read_text())["resultados"]
    return data, result_hash, actual


def related(data: dict, point: str, edge: str) -> str:
    # Sólo asociaciones sintácticas inequívocas; el catálogo no inventa IC.
    base = point.removesuffix("-P").removesuffix("-PUNTO")
    ending = "LO" if edge == "INF" else "HI"
    candidates = [
        base + "-IC95" + edge,
        base + "-IC95-" + edge,
        base + "-IC95_" + edge,
        base + "-IC-" + ending,
    ]
    for marker in ("-P-", "-PUNTO-"):
        if marker in point:
            candidates.extend([
                point.replace(marker, "-IC95" + edge + "-", 1),
                point.replace(marker, "-IC-" + ending + "-", 1),
            ])
    hits = [key for key in candidates if key in data]
    return hits[0] if len(hits) == 1 else ""


def companion(data: dict, point: str, suffix: str) -> str:
    base = point.removesuffix("-P").removesuffix("-PUNTO")
    candidates = [base + "-" + suffix]
    if "-P-" in point:
        candidates.append(point.replace("-P-", "-" + suffix + "-", 1))
    hits = [key for key in candidates if key in data]
    return hits[0] if len(hits) == 1 else ""


def main() -> None:
    # ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-4: `valor` REF -> texto sellado.
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "tools"))
    from vista import resuelve_fila  # noqa: PLC0415
    results = {row["resultado_id"]: resuelve_fila(row) for row in tsv("resultados.tsv")}
    uses = [
        row for row in tsv("usos.tsv")
        if row["activo"] == "SI" and row["generacion_leida"] == "GEN2"
    ]
    marker_by_result = {
        row["resultado_id"]: row for row in tsv("marcador-segmento.tsv")
        if row["resultado_id"]
    }
    by_calc: dict[str, tuple[dict, str, str, dict]] = {}
    rows: dict[str, dict[str, str]] = {}
    for use in uses:
        rid = use["corrida0_resultado_id"]
        if not rid:
            raise ValueError(f"uso GEN2 sin RESULT: {use['consumidor']}")
        reg = results[rid]
        calc = reg["spec_id"]
        if reg["estado"] != "SELLADA" or reg["cuenta_gen2"] != "SI":
            raise ValueError(f"RESULT no sellado o no GEN2: {rid}")
        if calc not in by_calc:
            data, result_hash, seal_hash = verified(calc)
            spec = yaml.safe_load((CORRIDA / calc / "spec.yaml").read_text())
            by_calc[calc] = data, result_hash, seal_hash, spec
        data, result_hash, seal_hash, spec = by_calc[calc]
        if rid not in data or str(data[rid]) != reg["valor"]:
            # El TSV puede normalizar un flotante; comparar como número cuando
            # los literales difieren, sin redondear ni tolerancia editorial.
            try:
                same = float(data[rid]) == float(reg["valor"])
            except (TypeError, ValueError):
                same = False
            if not same:
                raise ValueError(f"punto no coincide con CALC: {rid}")
        lower = related(data, rid, "INF")
        upper = related(data, rid, "SUP")
        if bool(lower) != bool(upper):
            raise ValueError(f"IC incompleto: {rid}")
        method_key = companion(data, rid, "METODO-IC")
        denom_key = companion(data, rid, "DENOMINADOR")
        universe = str(spec.get("universo", "NO-DECLARADO-EN-SPEC"))
        surveys = list(dict.fromkeys(re.findall(
            r"\b(?:ENIF|ENCIG|ENVIPE|ENCUCI|ENIGH|ENFIH|ENUT|ENSANUT|EDER)\s*20\d{2}",
            universe + " " + str(spec.get("estimando", "")), re.IGNORECASE,
        )))
        instrument = surveys[0] if surveys else INSTRUMENT_FALLBACK.get(calc, "INSTRUMENTO-NO-IDENTIFICADO")
        if rid == "RESULT-B-ENIGH-2022-P":
            instrument = "ENIGH 2022"
        elif calc == "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001" and "-C2-" in rid:
            instrument = "ENIF 2024 (piso; desarrollo ENIF 2021)"
        elif calc.startswith("CALC-ENCUCI-"):
            instrument = "ENCUCI 2020"
        rule = use["reglas_impacto"]
        domain = rule.split(".")[0] if rule else "SIN-REGLA"
        domain = {"DIN": "dinero", "TRA": "tramite", "CIV": "civico", "FAM": "familia"}.get(
            domain.split("-")[0], domain
        )
        if rid not in rows:
            rows[rid] = {
                "llave": rid,
                "dominio": domain,
                "conducta": use["consumidor"].split(":")[-1],
                "instrumento_ola": instrument,
                "segmento": rule or "VER-ESTIMANDO",
                "universo_denominador": (
                    f"{data[denom_key]} [RESULT:{denom_key}]" if denom_key else universe
                ),
                "unidad_escala": reg["unidad"],
                "punto": str(data[rid]),
                "ic95_inf": str(data[lower]) if lower else "",
                "ic95_sup": str(data[upper]) if upper else "",
                "naturaleza_ic": (
                    str(data[method_key]) if lower and method_key else
                    "IC-DE-SPEC-SIN-CALIBRACION-ACREDITADA" if lower else
                    "SIN-IC-IDENTIFICADO"
                ),
                "estado_adopcion": (
                    "ADOPTADO-POR-FIRMA" if use["tipo_uso"] == "ADOPCION-POR-FIRMA"
                    else "CONSUMO-GEN2-ACTIVO"
                ),
                "firma": (
                    marker_by_result.get(rid, {}).get("decision_ref")
                    or use["pin_de_mesa"]
                    or str(spec.get("etiquetas", {}).get(
                        "cuenta_gen2_firma", "CONSUMO-ACTIVO-SIN-FIRMA-DE-ADOPCION-CITADA"
                    ))
                ),
                "temporalidad": marker_by_result.get(rid, {}).get(
                    "prospectividad", "ORDEN-DE-SELLOS-NO-ACREDITADO-AQUI"
                ),
                "result_punto": rid,
                "result_inf": lower,
                "result_sup": upper,
                "calc": calc,
                "sha256_resultados": result_hash,
                "sha256_sello": seal_hash,
                "uso": use["consumidor"],
                "oferta_compatible": (
                    "SIN-MEDIDA-DE-OFERTA-DE-LA-MISMA-OLA-Y-UNIVERSO"
                    if domain == "dinero" else "NO-APLICA"
                ),
                "oferta_valor_ic": "",
                "reserva": "Revisar identidad estimando, oferta compatible y alcance de firma.",
            }
        else:
            rows[rid]["uso"] += ";" + use["consumidor"]
    for link in tsv("../../forense/analisis/din-oferta-exclusion/enlace-pisos.tsv"):
        # El enlace publicado por ASTRA-3 es contextual. Los pisos históricos
        # no se convierten en adopciones por aparecer en este inventario.
        rid = link["result_piso"]
        calc = link["calc_piso"]
        if rid in rows:
            raise ValueError(f"piso duplicado entre fuentes: {rid}")
        if calc not in by_calc:
            data, result_hash, seal_hash = verified(calc)
            spec = yaml.safe_load((CORRIDA / calc / "spec.yaml").read_text())
            by_calc[calc] = data, result_hash, seal_hash, spec
        data, result_hash, seal_hash, spec = by_calc[calc]
        if rid not in data:
            raise ValueError(f"piso sin RESULT: {rid}")
        reg = results[rid]
        lower = related(data, rid, "INF")
        upper = related(data, rid, "SUP")
        if bool(lower) != bool(upper):
            raise ValueError(f"IC de piso incompleto: {rid}")
        offer_id = link["result_exclusion_oferta"]
        offer_value = ""
        if offer_id:
            # El CALC ASTRA-3 puede estar sellado en disco sin que la vista
            # derivada resultados.tsv se haya publicado todavía (E.7).
            offer_calc = (
                results[offer_id]["spec_id"] if offer_id in results else
                "CALC-DIN-OFERTA-EXCLUSION-ENIF" + link["ola"] + "-0001"
            )
            if offer_calc not in by_calc:
                offer_data, offer_hash, offer_seal = verified(offer_calc)
                offer_spec = yaml.safe_load((CORRIDA / offer_calc / "spec.yaml").read_text())
                by_calc[offer_calc] = offer_data, offer_hash, offer_seal, offer_spec
            offer_data = by_calc[offer_calc][0]
            if offer_id not in offer_data:
                raise ValueError(f"exclusión sin RESULT: {offer_id}")
            offer_lo = related(offer_data, offer_id, "INF")
            offer_hi = related(offer_data, offer_id, "SUP")
            if not offer_lo or not offer_hi:
                raise ValueError(f"exclusión sin IC completo: {offer_id}")
            offer_value = f"{offer_data[offer_id]} [{offer_data[offer_lo]}, {offer_data[offer_hi]}]"
        rows[rid] = {
            "llave": rid,
            "dominio": "dinero",
            "conducta": str(spec.get("estimando", "crédito formal")),
            "instrumento_ola": "ENIF " + link["ola"],
            "segmento": link["eje"] + ":" + link["categoria"],
            "universo_denominador": str(spec.get("universo", link["universo_piso"])),
            "unidad_escala": reg["unidad"],
            "punto": str(data[rid]),
            "ic95_inf": str(data[lower]) if lower else "",
            "ic95_sup": str(data[upper]) if upper else "",
            "naturaleza_ic": "IC-DE-SPEC-SIN-CALIBRACION-ACREDITADA" if lower else "SIN-IC-IDENTIFICADO",
            "estado_adopcion": "PISO-HISTORICO-CONTEXTO; NO-ADOPCION-POR-CATALOGO",
            "firma": "SIN-FIRMA-DE-ADOPCION; PISO-HISTORICO-CONTEXTUAL",
            "temporalidad": "RETROSPECTIVA-HISTORICA",
            "result_punto": rid,
            "result_inf": lower,
            "result_sup": upper,
            "calc": calc,
            "sha256_resultados": result_hash,
            "sha256_sello": seal_hash,
            "uso": "forense/analisis/din-oferta-exclusion/enlace-pisos.tsv",
            "oferta_compatible": (
                offer_id
                if link["estado"] == "ENLACE-CONTEXTUAL"
                else "SIN-ENLACE:" + link["causa"]
            ),
            "oferta_valor_ic": offer_value,
            "reserva": link["alcance"] or link["causa"],
        }
    for marker in tsv("marcador-segmento.tsv"):
        rid = marker["resultado_id"]
        if not rid or rid in rows:
            continue
        if rid not in results:
            raise ValueError(f"marcador con RESULT ausente en vista: {rid}")
        reg = results[rid]
        calc = reg["spec_id"]
        if calc not in by_calc:
            data, result_hash, seal_hash = verified(calc)
            spec = yaml.safe_load((CORRIDA / calc / "spec.yaml").read_text())
            by_calc[calc] = data, result_hash, seal_hash, spec
        data, result_hash, seal_hash, spec = by_calc[calc]
        if rid not in data:
            raise ValueError(f"marcador con RESULT ausente en CALC: {rid}")
        lower = related(data, rid, "INF")
        upper = related(data, rid, "SUP")
        if bool(lower) != bool(upper):
            raise ValueError(f"IC incompleto en marcador: {rid}")
        axis = marker["regla_o_eje_origen"]
        domain = {"DIN": "dinero", "TRA": "tramite", "CIV": "civico", "FAM": "familia"}.get(
            axis.split(".")[0], axis.split(".")[0]
        )
        rows[rid] = {
            "llave": rid,
            "dominio": domain,
            "conducta": axis,
            "instrumento_ola": marker["instrumento"],
            "segmento": marker["eje_o_par"] + ":" + marker["categoria"],
            "universo_denominador": str(spec.get("universo", "VER-SPEC-UNIVERSO")),
            "unidad_escala": reg["unidad"],
            "punto": str(data[rid]),
            "ic95_inf": str(data[lower]) if lower else "",
            "ic95_sup": str(data[upper]) if upper else "",
            "naturaleza_ic": marker["tipo_incertidumbre"] or (
                "IC-DE-SPEC-SIN-CALIBRACION-ACREDITADA" if lower else "SIN-IC-IDENTIFICADO"
            ),
            "estado_adopcion": "PISO-EN-MARCADOR:" + marker["estado"] + "; ADOPCION-POR-VERIFICAR",
            "firma": marker["decision_ref"] or "VER-DECISION-POR-CELDA",
            "temporalidad": marker["prospectividad"] or "NO-DECLARADA",
            "result_punto": rid,
            "result_inf": lower,
            "result_sup": upper,
            "calc": calc,
            "sha256_resultados": result_hash,
            "sha256_sello": seal_hash,
            "uso": marker["celda_id"],
            "oferta_compatible": (
                "SIN-MEDIDA-DE-OFERTA-COMPATIBLE-VERIFICADA" if domain == "dinero"
                else "NO-APLICA"
            ),
            "oferta_valor_ic": "",
            "reserva": "Estado de marcador; no constituye adopción adicional.",
        }
    enut_calcs = (
        "CALC-ENUT-SERIE-2009-2014-NUCLEO-0001",
        "CALC-ENUT2019-NUCLEO-EJES-0001",
        "CALC-ENUT2024-NUCLEO-EJES-0001",
    )
    for calc in enut_calcs:
        if calc not in by_calc:
            data, result_hash, seal_hash = verified(calc)
            spec = yaml.safe_load((CORRIDA / calc / "spec.yaml").read_text())
            by_calc[calc] = data, result_hash, seal_hash, spec
        data, result_hash, seal_hash, spec = by_calc[calc]
        for rid, value in data.items():
            if not rid.endswith("-P") or rid in rows:
                continue
            if rid not in results or results[rid]["cuenta_gen2"] != "SI":
                continue
            reg = results[rid]
            lower = related(data, rid, "INF")
            upper = related(data, rid, "SUP")
            if bool(lower) != bool(upper):
                raise ValueError(f"IC ENUT incompleto: {rid}")
            ola = re.search(r"ENUT(20\d\d)", rid)
            rows[rid] = {
                "llave": rid,
                "dominio": "tiempo-y-cuidado",
                "conducta": str(spec.get("estimando", "VER-SPEC-ESTIMANDO")),
                "instrumento_ola": "ENUT " + ola.group(1) if ola else "ENUT · VER-SPEC",
                "segmento": rid,
                "universo_denominador": str(spec.get("universo", "VER-SPEC-UNIVERSO")),
                "unidad_escala": reg["unidad"],
                "punto": str(value),
                "ic95_inf": str(data[lower]) if lower else "",
                "ic95_sup": str(data[upper]) if upper else "",
                "naturaleza_ic": "IC-DE-SPEC-SIN-CALIBRACION-ACREDITADA" if lower else "SIN-IC-IDENTIFICADO",
                "estado_adopcion": "SELLADO-CONTEXTO; ADOPTABILIDAD-POR-DICTAMINAR",
                "firma": "SIN-FIRMA-DE-ADOPCION",
                "temporalidad": "RETROSPECTIVA",
                "result_punto": rid,
                "result_inf": lower,
                "result_sup": upper,
                "calc": calc,
                "sha256_resultados": result_hash,
                "sha256_sello": seal_hash,
                "uso": "ENUT-NUCLEO-Y-SERIE",
                "oferta_compatible": "NO-APLICA",
                "oferta_valor_ic": "",
                "reserva": "Verificar comparabilidad de definición y unidad entre olas antes de contrastar.",
            }
    enigh_measures = (
        "PREVALENCIA", "REMESAS-MEDIA", "REMESAS-MEDIANA",
        "PARTICIPACION-MEDIA-HOGAR", "PARTICIPACION-AGREGADA",
        "PARTICIPACION-GE50",
    )
    for year in (2016, 2018, 2020, 2022):
        calc = f"CALC-ENIGH{year}-INTENSIDAD-REMESAS-0001"
        data, result_hash, seal_hash = verified(calc)
        spec = yaml.safe_load((CORRIDA / calc / "spec.yaml").read_text())
        by_calc[calc] = data, result_hash, seal_hash, spec
        for name in enigh_measures:
            rid = f"RESULT-ENIGH{str(year)[-2:]}-REMINT-{name}"
            if rid in rows:
                continue
            if rid not in data or rid not in results:
                raise ValueError(f"descriptor ENIGH ausente: {rid}")
            lower = related(data, rid, "INF")
            upper = related(data, rid, "SUP")
            if bool(lower) != bool(upper):
                raise ValueError(f"IC ENIGH incompleto: {rid}")
            rows[rid] = {
                "llave": rid,
                "dominio": "ingreso-y-gasto",
                "conducta": name.lower().replace("-", " ") + " de remesas",
                "instrumento_ola": f"ENIGH {year}",
                "segmento": "hogares receptores; ver universo",
                "universo_denominador": str(spec.get("universo", "VER-SPEC-UNIVERSO")),
                "unidad_escala": results[rid]["unidad"],
                "punto": str(data[rid]),
                "ic95_inf": str(data[lower]) if lower else "",
                "ic95_sup": str(data[upper]) if upper else "",
                "naturaleza_ic": "IC-DE-SPEC-SIN-CALIBRACION-ACREDITADA" if lower else "SIN-IC-IDENTIFICADO",
                "estado_adopcion": "SELLADO-CONTEXTO; NO-ADOPCION-POR-CATALOGO",
                "firma": "SIN-FIRMA-DE-ADOPCION",
                "temporalidad": "RETROSPECTIVA",
                "result_punto": rid,
                "result_inf": lower,
                "result_sup": upper,
                "calc": calc,
                "sha256_resultados": result_hash,
                "sha256_sello": seal_hash,
                "uso": "ENIGH-INTENSIDAD-REMESAS",
                "oferta_compatible": "NO-APLICA",
                "oferta_valor_ic": "",
                "reserva": "Describe hogares receptores e ingreso; no mide gasto general ni efecto causal.",
            }
    adoption_sheet = tsv(
        "../../forense/notas/2026-09-22-GEN2-TRAMITE-PENDIENTES-1-hoja-adopcion.tsv"
    )
    for decision in adoption_sheet:
        rid = decision["result_id"]
        if rid in rows:
            continue
        calc = decision["calc_id"]
        if calc not in by_calc:
            data, result_hash, seal_hash = verified(calc)
            spec = yaml.safe_load((CORRIDA / calc / "spec.yaml").read_text())
            by_calc[calc] = data, result_hash, seal_hash, spec
        data, result_hash, seal_hash, spec = by_calc[calc]
        if rid not in data:
            raise ValueError(f"hoja de adopción sin RESULT: {rid}")
        lower = related(data, rid, "INF")
        upper = related(data, rid, "SUP")
        if bool(lower) != bool(upper):
            raise ValueError(f"IC incompleto en hoja de adopción: {rid}")
        name = rid.split("-")[1]
        domain = {"BANXICO": "dinero", "CTX": "civico", "MOTRAL15": "trabajo", "EDER": "familia"}.get(name, "OTRO")
        adopted = decision["recomendacion_ejecutor"].startswith("ADOPTAR")
        instrument = (
            "Banxico 2024" if name == "BANXICO" else
            "LAPOP " + rid.split("-")[2] if name == "CTX" else
            "MOTRAL 2015" if name == "MOTRAL15" else "EDER"
        )
        rows[rid] = {
            "llave": rid,
            "dominio": domain,
            "conducta": decision["consumidor_regla"],
            "instrumento_ola": instrument,
            "segmento": rid,
            "universo_denominador": decision["universo_unidad_escala"],
            "unidad_escala": results[rid]["unidad"] if rid in results else "VER-SPEC",
            "punto": str(data[rid]) if isinstance(data[rid], (int, float)) else "",
            "ic95_inf": str(data[lower]) if lower else "",
            "ic95_sup": str(data[upper]) if upper else "",
            "naturaleza_ic": "IC-DE-SPEC-SIN-CALIBRACION-ACREDITADA" if lower else "SIN-IC-IDENTIFICADO",
            "estado_adopcion": (
                "FIRMA-ADOPTAR; CONSUMO-PENDIENTE" if adopted else "VETADO-POR-MESA"
            ),
            "firma": "data/corrida0/decisiones.tsv:FP-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-01",
            "temporalidad": "RETROSPECTIVA",
            "result_punto": rid,
            "result_inf": lower,
            "result_sup": upper,
            "calc": calc,
            "sha256_resultados": result_hash,
            "sha256_sello": seal_hash,
            "uso": decision["consumidor_regla"],
            "oferta_compatible": (
                "SIN-MEDIDA-DE-OFERTA-COMPATIBLE-VERIFICADA" if domain == "dinero" else "NO-APLICA"
            ),
            "oferta_valor_ic": "",
            "reserva": decision["recomendacion_ejecutor"],
        }
    calc = "CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0002"
    data, result_hash, seal_hash = verified(calc)
    spec = yaml.safe_load((CORRIDA / calc / "spec.yaml").read_text())
    by_calc[calc] = data, result_hash, seal_hash, spec
    for rid, value in data.items():
        if not rid.endswith("-P") or rid in rows:
            continue
        lower = related(data, rid, "INF")
        upper = related(data, rid, "SUP")
        if bool(lower) != bool(upper):
            raise ValueError(f"IC K2 incompleto: {rid}")
        year = re.search(r"HISTORIA-(20\d\d)-", rid)
        rows[rid] = {
            "llave": rid,
            "dominio": "dinero",
            "conducta": "tenencia de crédito bancario; ver denominador",
            "instrumento_ola": "ENIF " + year.group(1) if year else "ENIF · VER-SPEC",
            "segmento": "NACIONAL",
            "universo_denominador": str(spec.get("universo", "VER-SPEC-UNIVERSO")),
            "unidad_escala": results[rid]["unidad"] if rid in results else "VER-SPEC",
            "punto": str(value),
            "ic95_inf": str(data[lower]) if lower else "",
            "ic95_sup": str(data[upper]) if upper else "",
            "naturaleza_ic": "IC-DE-SPEC-SIN-CALIBRACION-ACREDITADA" if lower else "SIN-IC-IDENTIFICADO",
            "estado_adopcion": "SELLADO-CONTEXTO; NO-ADOPCION-POR-CATALOGO",
            "firma": "forense/encargos/2026-09-22-GEN2-DIN-CREDITO-SERIE-LECTURA-1.md",
            "temporalidad": "RETROSPECTIVA",
            "result_punto": rid,
            "result_inf": lower,
            "result_sup": upper,
            "calc": calc,
            "sha256_resultados": result_hash,
            "sha256_sello": seal_hash,
            "uso": "K2-BANCARIA-HISTORIA-LECTURA",
            "oferta_compatible": "SIN-MEDIDA-DE-OFERTA-COMPATIBLE-VERIFICADA",
            "oferta_valor_ic": "",
            "reserva": "Entre tenedores y población nacional tienen denominadores distintos; no comparar como una misma serie.",
        }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(rows.values(), key=lambda row: row["llave"]))
    print(f"usos_gen2={len(uses)} resultados_unicos={len(rows)} calcs={len(by_calc)}")


if __name__ == "__main__":
    main()
