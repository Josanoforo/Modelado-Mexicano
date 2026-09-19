#!/usr/bin/env python3
"""Proyecta los RESULT JSON sellados a tres CSV agregados, sin microdatos."""
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CALC = ROOT / "data/corrida0/CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003/resultados.json"
OUT = Path(__file__).resolve().parent
P = "RESULT-ENIGH22-PERFIL-"


def escribe(nombre, filas):
    ruta = OUT / nombre
    campos = list(filas[0]) if filas else []
    with ruta.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos, lineterminator="\n")
        w.writeheader(); w.writerows(filas)
    return ruta


def main():
    res = json.loads(CALC.read_text(encoding="utf-8"))["resultados"]
    pares = [
        ("marginales.csv", "P1-MARGINALES-JSON"),
        ("conjunta.csv", "P2-CONJUNTA-JSON"),
        ("marginales-casos-completos.csv", "P2-MARGINALES-COMPLETOS-JSON"),
    ]
    for nombre, rid in pares:
        ruta = escribe(nombre, json.loads(res[P + rid]))
        print(ruta.relative_to(ROOT))
    (OUT / "embudo.json").write_text(res[P + "EMBUDO-JSON"] + "\n", encoding="utf-8")
    print((OUT / "embudo.json").relative_to(ROOT))


if __name__ == "__main__":
    main()
