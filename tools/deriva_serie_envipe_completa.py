#!/usr/bin/env python3
"""Deriva la vista anual 2010–2024 de p(C1,U1) desde RESULT sellados.

No calcula estimandos: selecciona campos de quince resultados existentes y
falla si hay huecos, años duplicados o una corrida no calculada.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/corrida0/envipe-serie-denuncia-v1_0.tsv"

WAVES = {
    2011: ("CALC-ENVIPE-SERIE-2011", "RESULT-ENVIPE-SERIE-2011", "BP1_21", "DBF", "INSTRUMENTACION-NOMINAL-Y-RESIDUALES"),
    2012: ("CALC-R-CIV-M-01", "RESULT-R-CIV-M-01", "BP1_23", "DBF", "NINGUNA-EN-C1-U1"),
    2013: ("CALC-R-CIV-M-02", "RESULT-R-CIV-M-02", "BP1_23", "DBF", "NINGUNA-EN-C1-U1"),
    2014: ("CALC-ENVIPE-SERIE-2014", "RESULT-ENVIPE-SERIE-2014", "BP1_23", "DBF", "NINGUNA-EN-C1-U1"),
    2015: ("CALC-R-CIV-M-04", "RESULT-R-CIV-M-04", "BP1_23", "DBF", "NINGUNA-EN-C1-U1"),
    2016: ("CALC-ENVIPE-SERIE-2016", "RESULT-ENVIPE-SERIE-2016", "BP1_23", "DBF", "NINGUNA-EN-C1-U1"),
    2017: ("CALC-ENVIPE-SERIE-2017", "RESULT-ENVIPE-SERIE-2017", "BP1_23", "DBF", "NINGUNA-EN-C1-U1"),
    2018: ("CALC-ENVIPE-SERIE-2018", "RESULT-ENVIPE-SERIE-2018", "BP1_23", "CSV", "NINGUNA-EN-C1-U1"),
    2019: ("CALC-ENVIPE-SERIE-2019", "RESULT-ENVIPE-SERIE-2019", "BP1_23", "CSV", "NINGUNA-EN-C1-U1"),
    2020: ("CALC-ENVIPE-SERIE-2020", "RESULT-ENVIPE-SERIE-2020", "BP1_23", "CSV", "NINGUNA-EN-C1-U1"),
    2021: ("CALC-R-CIV-M-10", "RESULT-R-CIV-M-10", "BP1_23", "CSV", "NINGUNA-EN-C1-U1"),
    2022: ("CALC-ENVIPE-SERIE-2022", "RESULT-ENVIPE-SERIE-2022", "BP1_23", "CSV", "NINGUNA-EN-C1-U1"),
    2023: ("CALC-R-CIV-M-12", "RESULT-R-CIV-M-12", "BP1_23", "CSV", "NINGUNA-EN-C1-U1"),
    2024: ("CALC-R-CIV-M-13", "RESULT-R-CIV-M-13", "BP1_23", "CSV", "NINGUNA-EN-C1-U1"),
    2025: ("CALC-ENVIPE-0001", "RESULT-ENVIPE-DEN", "BP1_23", "CSV", "NINGUNA-EN-C1-U1"),
}

FIELDS = ["anio_hecho", "ola_encuesta", "p_c1_u1", "ic95_boot_lo", "ic95_boot_hi",
          "n_u1", "unidad", "ponderador", "reactivo", "formato", "comparabilidad",
          "calc_id", "result_id_punto"]


def main() -> None:
    rows = []
    for wave, (calc, prefix, variable, fmt, break_) in WAVES.items():
        p = ROOT / "data/corrida0" / calc / "resultados.json"
        result = json.loads(p.read_text(encoding="utf-8"))["resultados"]
        if calc == "CALC-ENVIPE-0001":
            point = result[prefix + "-P-C1-U1"]
            # La primera corrida nombró el mismo bootstrap simplemente IC-LO/HI.
            lo = result[prefix + "-IC-LO-C1-U1"]
            hi = result[prefix + "-IC-HI-C1-U1"]
            n = result[prefix + "-N-U1"]
        else:
            assert result[prefix + "-ESTADO"] == "CALCULADO"
            point = result[prefix + "-P-C1-U1"]
            lo = result[prefix + "-IC-BOOT-LO-C1-U1"]
            hi = result[prefix + "-IC-BOOT-HI-C1-U1"]
            n = result[prefix + "-N-U1"]
        rows.append({
            "anio_hecho": wave - 1, "ola_encuesta": wave,
            "p_c1_u1": f"{point:.12f}", "ic95_boot_lo": f"{lo:.12f}",
            "ic95_boot_hi": f"{hi:.12f}", "n_u1": n,
            "unidad": "DELITO-PERSONAL-NO-DENUNCIADO",
            "ponderador": "FAC_DEL", "reactivo": variable, "formato": fmt,
            "comparabilidad": break_, "calc_id": calc,
            "result_id_punto": prefix + "-P-C1-U1",
        })
    years = [r["anio_hecho"] for r in rows]
    assert years == list(range(2010, 2025)), years
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"SERIE-COMPLETA {len(rows)}/15 · {years[0]}-{years[-1]} · {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
