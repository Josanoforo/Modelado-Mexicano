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

PISOS = (
    # nombre, regla/destino, desenlace, instrumento, periodo destino, CALC, RESULT tabla
    ("envipe", "TRA", "evade_norma", "ENVIPE", "2025",
     "CALC-PISOS-ENVIPE2024-EJES-0001", "RESULT-PISOS-ENVIPE2024-EVASION-TABLA"),
    ("encig", "GOB", "digital_util_sin_coercion", "ENCIG", "2025",
     "CALC-PISOS-ENCIG2023-EJES-0001-v1_1", "RESULT-PISOS-ENCIG2023-DIGITAL-V1-1-TABLA"),
    ("enif", "DIN", "ahorro_solo_informal", "ENIF", "2024",
     "CALC-PISOS-ENIF2021-EJES-0001", "RESULT-PISOS-ENIF2021-D9-TABLA"),
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
                "tipo": "cruce", "estado": "IMPLEMENTADO-PROPUESTO",
                "evaluacion": "EVALUADA", "adjudicacion": ref["id_candidato"],
                "fuente": {"calc": ref["calc"], "punto": ref["resultado_puntual"],
                            "ic95inf": ref["ic95inf"], "ic95sup": ref["ic95sup"],
                            "decision": ref["decision_ref"]},
                "incertidumbre": "bootstrap-composicion-sellada",
            })
    return entries


def _piso_entries() -> list[dict]:
    entries = []
    for _, regla, desenlace, instrumento, periodo, calc, rid in PISOS:
        spec = ROOT / "data/corrida0" / calc / "spec.yaml"
        data = json.loads((ROOT / "data/corrida0" / calc / "resultados.json").read_text())
        tabla = json.loads(data["resultados"][rid])
        universo = yaml.safe_load(spec.read_text())["universo"]
        for eje, filas in sorted(tabla.items()):
            for fila in filas:
                if str(fila["categoria"]).lower() == "nan":
                    continue
                entries.append({
                    "identidad": {"regla": regla, "desenlace": desenlace,
                                  "instrumento": instrumento, "periodo": periodo,
                                  "universo": universo, "ejes": {eje: str(fila["categoria"])}},
                    "tipo": "marginal", "estado": "IMPLEMENTADO-PROPUESTO",
                    "evaluacion": "SOLO-PISO", "adjudicacion": "PISO-PERSISTENCIA",
                    "fuente": {"calc": calc, "tabla": rid, "eje": eje,
                                "categoria": str(fila["categoria"])},
                    "incertidumbre": "IC95-muestral-t-1-no-predictiva",
                })
    return entries


def derivar() -> tuple[list[dict], dict]:
    entradas = _c2_entries() + _piso_entries()
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
              "tipo", "estado_evaluacion", "adjudicacion", "estado_consumo", "calc",
              "resultado_puntual", "resultado_ic95inf", "resultado_ic95sup", "incertidumbre"]
    with OUT_TSV.open("w", encoding="utf-8", newline="") as fh:
        fh.write("# DERIVADO — NO EDITAR\n")
        w = csv.DictWriter(fh, fieldnames=campos, delimiter="\t")
        w.writeheader()
        for e in entradas:
            i, f = e["identidad"], e["fuente"]
            w.writerow({"regla": i["regla"], "desenlace": i["desenlace"],
                        "instrumento": i["instrumento"], "periodo": i["periodo"],
                        "universo": i["universo"], "ejes": json.dumps(i["ejes"], sort_keys=True),
                        "tipo": e["tipo"], "estado_evaluacion": e["evaluacion"],
                        "adjudicacion": e["adjudicacion"], "estado_consumo": e["estado"],
                        "calc": f["calc"], "resultado_puntual": f.get("punto", f.get("tabla", "")),
                        "resultado_ic95inf": f.get("ic95inf", ""),
                        "resultado_ic95sup": f.get("ic95sup", ""),
                        "incertidumbre": e["incertidumbre"]})


if __name__ == "__main__":
    argparse.ArgumentParser(description=__doc__).parse_args()
    escribir()
