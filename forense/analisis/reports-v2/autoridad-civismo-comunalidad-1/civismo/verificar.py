"""Control dirigido de cobertura y cifras del reporte cívico."""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]

def main() -> None:
    summary = json.loads((HERE / "resumen.json").read_text())
    with (HERE / "afirmaciones.tsv").open() as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    with (ROOT / "canon/mapa-dominios-v1_1.tsv").open() as f:
        original = [r for r in csv.DictReader(f, delimiter="\t") if summary["report"].replace("reports-v2", "reports") in r["report"]]
    assert len(original) == summary["mapa_filas"]
    assert len(rows) == summary["registros"]
    assert {r["id_afirmacion"] for r in original} <= {r["id_afirmacion"] for r in rows}
    assert len({r["id_afirmacion"] for r in rows}) == len(rows)
    assert all(r["razon_especifica"] and r["evidencia"] for r in rows)
    assert sum(summary["dictamenes"].values()) == len(rows)
    report = (ROOT / summary["report"]).read_text()
    source = (HERE / "fuentes.md").read_text()
    assert "FP-57" in report and "LANGSTON25" in source
    assert "ENVIPE 2026" in source and "no se abrió" in source
    assert "12.86%" in report and "sin cargo" in report.lower()
    assert "61.04%" in report and "59.8%" in report
    with (ROOT / "data/corrida0/resultados.tsv").open() as f:
        next(f)
        ledger = {r["resultado_id"]: r for r in csv.DictReader(f, delimiter="\t") if r["resultado_id"] in summary["cifras"]}
    assert len(ledger) == len(summary["cifras"])
    for rid in summary["cifras"]:
        r = ledger[rid]
        assert r["estado"] == "SELLADA" and r["cuenta_gen2"] == "SI"
        assert r["validacion_independiente"] == "NO-HECHA"
        assert rid in (HERE / "cifras.md").read_text()
        assert r["valor"] in (HERE / "cifras.md").read_text()
    print(f"VERDE: {len(original)} filas del mapa y {len(rows)-len(original)} desdobles/extra, {len(ledger)} RESULT, reservas declaradas")

if __name__ == "__main__":
    main()
