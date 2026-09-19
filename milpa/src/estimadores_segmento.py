"""Lector de estimadores por segmento: no usa R ni el TSV del marcador."""
from __future__ import annotations

import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
MAPA = ROOT / "milpa/estimadores-por-segmento.yaml"


def estimar(*, regla: str, desenlace: str, instrumento: str, periodo: str,
            universo: str, ejes: dict[str, str]) -> dict | None:
    """Devuelve la emisión exacta o ``None``; jamás sustituye un nacional."""
    mapa = yaml.safe_load(MAPA.read_text(encoding="utf-8"))
    buscada = {"regla": regla, "desenlace": desenlace, "instrumento": instrumento,
               "periodo": str(periodo), "universo": universo,
               "ejes": {str(k): str(v) for k, v in ejes.items()}}
    for entrada in mapa["estimadores"]:
        identidad = entrada["identidad"]
        if all(identidad[k] == buscada[k] for k in
               ("regla", "desenlace", "instrumento", "periodo", "universo")) and identidad["ejes"] == buscada["ejes"]:
            f = entrada["fuente"]
            resultados = json.loads((ROOT / "data/corrida0" / f["calc"] / "resultados.json").read_text())["resultados"]
            punto, lo, hi = resultados[f["punto"]], resultados[f["ic95inf"]], resultados[f["ic95sup"]]
            return {"punto": punto, "ic95": [lo, hi], "incertidumbre": entrada["incertidumbre"],
                    "fuente": f["calc"], "fuente_periodo": f["periodo"],
                    "estado": entrada["estado"],
                    "estados": {"evidencia": entrada["evidencia"],
                                "evaluacion": entrada["evaluacion"],
                                "adjudicacion": entrada["adjudicacion"],
                                "implementacion": entrada["implementacion"],
                                "consumo": entrada["consumo"]},
                    "identidad": identidad, "resultado": f["punto"],
                    "n": resultados.get(f.get("n")),
                    "denominador_ponderado": resultados.get(f.get("denominador"))}
    return None
