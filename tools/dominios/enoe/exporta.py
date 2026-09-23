"""Vista derivada de CALC ENOE sellado; no lee microdato."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CALC = "CALC-ENOE-PISOS-0003"
RESULT = "RESULT-ENOE-PISOS-TABLA"
CAMPOS = ("ola", "era", "conducta", "eje", "segmento", "unidad", "punto",
          "ic95_lo", "ic95_hi", "n", "n_efectivo_kish", "upm", "calidad",
          "resultado_id", "calc_id", "sello_sha256", "calibracion")


def main():
    d = RAIZ / "data" / "corrida0" / CALC
    sello = d / "sello.sha256"
    if not sello.exists():
        raise SystemExit("CALC sin sello")
    sello_hash = hashlib.sha256(sello.read_bytes()).hexdigest()
    data = json.loads((d / "resultados.json").read_text())
    filas = json.loads(data["resultados"][RESULT])
    out = RAIZ / "forense" / "analisis" / "dominios" / "enoe" / "pisos-v1_0.tsv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS, delimiter="\t")
        w.writeheader()
        for fila in filas:
            w.writerow({**fila, "resultado_id": RESULT, "calc_id": CALC,
                        "sello_sha256": sello_hash,
                        "calibracion": "SIN-COVARIANZA-LONGITUDINAL-PARA-CALIBRAR"})
    print(f"{out}: {len(filas)} celdas, sello.sha256 {sello_hash}")


if __name__ == "__main__":
    main()
