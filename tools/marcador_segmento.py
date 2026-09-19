#!/usr/bin/env python3
"""Deriva el índice consumible y el marcador, sin copiar estimaciones.

Las cifras permanecen en los RESULT sellados.  El YAML resultante sólo guarda
identidades y punteros; el lector del motor resuelve los punteros al emitir.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CELDAS = ROOT / "data/curacion-registro/celdas-d"
OUT_MAP = ROOT / "milpa/estimadores-por-segmento.yaml"
OUT_TSV = ROOT / "data/corrida0/marcador-segmento.tsv"

# Cada tupla declara identidad y prefijo RESULT; jamás copia cifras. Las
# categorías son las que las specs v2 congelaron antes de abrir los datos.
PISOS = (
    {"regla": "GOB", "desenlace": "digital_util_sin_coercion",
     "instrumento": "ENCIG", "periodo": "2025", "periodo_fuente": "2023",
     "universo": "evento_tramite_comparable", "calc": "CALC-PISOS-ENCIG2023-EJES-0002",
     "prefijo": "RESULT-PISOS-ENCIG2023-V2-DIGITAL",
     "ejes": {"sexo": ("1", "2"),
              "edad": ("18-29", "30-44", "45-59", "60-mas"),
              "escolaridad": ("hasta-primaria", "secundaria", "media-superior", "superior")}},
    {"regla": "DIN", "desenlace": "ahorro_solo_informal",
     "instrumento": "ENIF", "periodo": "2024", "periodo_fuente": "2021",
     "universo": "persona_elegida_18_mas", "calc": "CALC-PISOS-ENIF2021-EJES-0002",
     "prefijo": "RESULT-PISOS-ENIF2021-V2-D9",
     "ejes": {"sexo": ("1", "2"),
              "edad": ("18-29", "30-44", "45-59", "60-mas"),
              "escolaridad": ("hasta-primaria", "secundaria", "media-superior", "superior"),
              "localidad": ("menos-15000", "15000-y-mas"),
              "cuenta_formal": ("sin-cuenta", "con-cuenta")}},
    {"regla": "TRA", "desenlace": "evade_norma",
     "instrumento": "ENVIPE", "periodo": "2025", "periodo_fuente": "2024",
     "universo": "delito_con_bp1_20_valido", "calc": "CALC-PISOS-ENVIPE2024-EJES-0002",
     "prefijo": "RESULT-PISOS-ENVIPE2024-V2-EVASION",
     "ejes": {"sexo": ("1", "2"),
              "edad": ("18-29", "30-44", "45-59", "60-mas"),
              "escolaridad": ("hasta-primaria", "secundaria", "media-superior", "superior"),
              "dominio": ("R", "C", "U")}},
    {"regla": "CIV", "desenlace": "denuncia",
     "instrumento": "ENVIPE", "periodo": "2025", "periodo_fuente": "2024",
     "universo": "delito_robo_total_vehiculo", "calc": "CALC-PISOS-ENVIPE2024-EJES-0002",
     "prefijo": "RESULT-PISOS-ENVIPE2024-V2-DENUNCIA",
     "ejes": {"cobertura_seguro": ("no-asegurado", "asegurado")}},
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _c2_entries() -> list[dict]:
    entries = []
    for path in sorted(CELDAS.glob("*.yaml")):
        celda = yaml.safe_load(path.read_text(encoding="utf-8"))["celda_d"]
        adjudicadas = celda.get("adjudicacion_por_celda", {})
        if not adjudicadas:
            continue
        regla, desenlace, instrumento_periodo, ejes = celda["id"].split(".")
        instrumento = "ENIF" if "enif" in instrumento_periodo else "ENVIPE"
        periodo = "2024" if instrumento == "ENIF" else "2025"
        nombres_eje = ejes.split("_x_")
        for clave, ref in sorted(adjudicadas.items()):
            partes = clave.split("x")
            entries.append({
                "identidad": {"regla": regla, "desenlace": desenlace,
                              "instrumento": instrumento, "periodo": periodo,
                              "universo": celda["unidad_objetivo"],
                              "ejes": dict(zip(nombres_eje, partes))},
                "tipo": "cruce", "estado": "CONSUMO-ACTIVO",
                "evidencia": ("ACREDITADA-POR-RESULT-NC-0313"
                              if regla == "DIN" else "REPRODUCE/IDENTICO"),
                "evaluacion": "EVALUADA", "adjudicacion": ref["id_candidato"],
                "implementacion": "IMPLEMENTADO-PROPUESTO", "consumo": "ACTIVO",
                "diagnostico_emisor": "FUERA-DE-SELECCION",
                "fuente": {"calc": ref["calc"], "punto": ref["resultado_puntual"],
                            "ic95inf": ref["ic95inf"], "ic95sup": ref["ic95sup"],
                            "decision": ref["decision_ref"], "periodo": periodo},
                "incertidumbre": "bootstrap-composicion-sellada",
            })
    return entries


def _piso_entries() -> list[dict]:
    entries = []
    for piso in PISOS:
        calc, prefijo = piso["calc"], piso["prefijo"]
        resultados = json.loads((ROOT / "data/corrida0" / calc / "resultados.json").read_text())["resultados"]
        for eje, categorias in piso["ejes"].items():
            for categoria in categorias:
                base = f"{prefijo}-{eje}-{categoria}".upper().replace("_", "-")
                refs = {"punto": base + "-P", "ic95inf": base + "-IC-LO",
                        "ic95sup": base + "-IC-HI", "n": base + "-N",
                        "denominador": base + "-DEN-W"}
                faltantes = [rid for rid in refs.values() if rid not in resultados]
                if faltantes:
                    raise ValueError(f"RESULT faltante en {calc}: {faltantes}")
                entries.append({
                    "identidad": {"regla": piso["regla"], "desenlace": piso["desenlace"],
                                  "instrumento": piso["instrumento"], "periodo": piso["periodo"],
                                  "universo": piso["universo"], "ejes": {eje: categoria}},
                    "tipo": "marginal", "estado": "CONSUMO-ACTIVO",
                    "evidencia": "REPRODUCE/IDENTICO", "evaluacion": "SOLO-PISO",
                    "adjudicacion": "PISO-PERSISTENCIA-AUTORIZADO-ADENDA-03",
                    "implementacion": "IMPLEMENTADO-PROPUESTO", "consumo": "ACTIVO",
                    "diagnostico_emisor": "NO-APLICA-A-SELECCION",
                    "fuente": {"calc": calc, **refs, "periodo": piso["periodo_fuente"]},
                    "incertidumbre": "bootstrap-UPM-estratificado-t-1-no-predictiva",
                })
    return entries


def _guardias(entradas: list[dict]) -> None:
    identidades = set()
    for entrada in entradas:
        i, f = entrada["identidad"], entrada["fuente"]
        clave = (i["regla"], i["desenlace"], i["instrumento"], i["periodo"],
                 i["universo"], json.dumps(i["ejes"], sort_keys=True))
        if clave in identidades:
            raise ValueError(f"identidad duplicada: {clave}")
        identidades.add(clave)
        punto = f["punto"]
        if ("IC" in punto or "P-REDERIVADO" in punto
                or not (punto.endswith("-P") or "-P-" in punto)):
            raise ValueError(f"referencia puntual inválida: {punto}")
        if "ARBITRO" in f["calc"] or "HOLDOUT" in punto or punto.endswith("-R"):
            raise ValueError(f"fuga de reserva/HOLDOUT: {f}")
        if entrada["tipo"] == "marginal" and int(f["periodo"]) >= int(i["periodo"]):
            raise ValueError(f"piso marginal circular: {clave}")
        if entrada["diagnostico_emisor"] not in {"FUERA-DE-SELECCION", "NO-APLICA-A-SELECCION"}:
            raise ValueError(f"emisor usado como candidato: {clave}")


def derivar() -> tuple[list[dict], dict]:
    entradas = _c2_entries() + _piso_entries()
    _guardias(entradas)
    fuentes = sorted({e["fuente"]["calc"] for e in entradas})
    mapa = {"version": 1, "derivado": "NO EDITAR", "fuentes_sha256": {
        str(Path("data/corrida0") / calc / "resultados.json"):
        _sha(ROOT / "data/corrida0" / calc / "resultados.json") for calc in fuentes},
        "estimadores": entradas}
    return entradas, mapa


def escribir() -> None:
    entradas, mapa = derivar()
    OUT_MAP.write_text("# DERIVADO — NO EDITAR\n" + yaml.safe_dump(mapa, sort_keys=False,
                       allow_unicode=True), encoding="utf-8")
    campos = ["regla", "desenlace", "instrumento", "periodo", "universo", "ejes",
              "tipo", "estado_evidencia", "estado_evaluacion", "adjudicacion",
              "estado_implementacion", "estado_consumo", "diagnostico_emisor", "calc",
              "periodo_fuente", "resultado_puntual", "resultado_ic95inf",
              "resultado_ic95sup", "resultado_n", "resultado_denominador", "incertidumbre"]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as fh:
        fh.write("# DERIVADO — NO EDITAR\n")
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t")
        w.writeheader()
        for e in entradas:
            i, f = e["identidad"], e["fuente"]
            w.writerow({"regla": i["regla"], "desenlace": i["desenlace"],
                        "instrumento": i["instrumento"], "periodo": i["periodo"],
                        "universo": i["universo"], "ejes": json.dumps(i["ejes"], sort_keys=True),
                        "tipo": e["tipo"], "estado_evidencia": e["evidencia"],
                        "estado_evaluacion": e["evaluacion"], "adjudicacion": e["adjudicacion"],
                        "estado_implementacion": e["implementacion"],
                        "estado_consumo": e["consumo"], "diagnostico_emisor": e["diagnostico_emisor"],
                        "calc": f["calc"], "periodo_fuente": f["periodo"],
                        "resultado_puntual": f["punto"],
                        "resultado_ic95inf": f.get("ic95inf", ""),
                        "resultado_ic95sup": f.get("ic95sup", ""),
                        "resultado_n": f.get("n", ""),
                        "resultado_denominador": f.get("denominador", ""),
                        "incertidumbre": e["incertidumbre"]})


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    escribir()
