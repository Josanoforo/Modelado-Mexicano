"""Lector de estimadores por segmento: no usa R ni el TSV del marcador."""
from __future__ import annotations

import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
MAPA = ROOT / "milpa/estimadores-por-segmento.yaml"


def estimar(*, regla: str, desenlace: str, instrumento: str, periodo: str,
            ejes: dict[str, str]) -> dict | None:
    """Devuelve la emisión exacta o ``None``; jamás sustituye un nacional."""
    mapa = yaml.safe_load(MAPA.read_text(encoding="utf-8"))
    buscada = {"regla": regla, "desenlace": desenlace, "instrumento": instrumento,
               "periodo": str(periodo), "ejes": {str(k): str(v) for k, v in ejes.items()}}
    for entrada in mapa["estimadores"]:
        identidad = entrada["identidad"]
        if all(identidad[k] == buscada[k] for k in ("regla", "desenlace", "instrumento", "periodo")) and identidad["ejes"] == buscada["ejes"]:
            f = entrada["fuente"]
            resultados = json.loads((ROOT / "data/corrida0" / f["calc"] / "resultados.json").read_text())["resultados"]
            if "punto" in f:
                punto, lo, hi = resultados[f["punto"]], resultados[f["ic95inf"]], resultados[f["ic95sup"]]
            else:
                tabla = json.loads(resultados[f["tabla"]])
                fila = next(x for x in tabla[f["eje"]] if str(x["categoria"]) == str(f["categoria"]))
                punto, (lo, hi) = fila["punto"], fila["ic95"]
            return {"punto": punto, "ic95": [lo, hi], "incertidumbre": entrada["incertidumbre"],
                    "fuente": f["calc"], "estado": entrada["estado"],
                    "identidad": identidad, "resultado": f.get("punto", f.get("tabla"))}
    return None
