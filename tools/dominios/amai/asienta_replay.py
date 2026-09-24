"""Asienta en forense/replay-evidencia.tsv los verify aislados de los seis CALC AMAI-NSE.

Lee la salida de `tools/verifica_aislada.py --salida <json>` (argumento 1);
append por línea, sin repetir calc_id. Uso:
python3 -m tools.dominios.amai.asienta_replay <evidencia.json>
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REG = ROOT / "forense/replay-evidencia.tsv"


def main(ruta: str) -> None:
    evidencia = json.loads(Path(ruta).read_text(encoding="utf-8"))
    with REG.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        campos = reader.fieldnames
        existentes = {r["calc_id"] for r in reader}
    with REG.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter="\t", lineterminator="\n")
        for x in evidencia:
            calc = x["calc_id"]
            if calc in existentes or not calc.startswith("CALC-AMAI-NSE-"):
                continue
            ejec = json.loads((ROOT / "data/corrida0" / calc / "ejecucion.json")
                              .read_text(encoding="utf-8"))
            det = x["detalle_verify"]
            num = [v for v in det["deltas"].values() if v is not None]
            ident = x["identidad"]
            w.writerow({
                "calc_id": calc, "corrida_id": ejec["corrida_id"],
                "resultado_replay": x["resultado_replay"], "contexto_replay": x["contexto_replay"],
                "razones": (f"corrida0 verify en proceso aislado (tools/verifica_aislada.py): "
                            f"{x['resultado_replay']} CONTEXTO={x['contexto_replay']}; "
                            f"{len(det['deltas'])}/{len(det['deltas'])} RESULT comparados; "
                            f"max |delta| numerico={max(num) if num else 0.0}; "
                            f"razones_contexto={det['razones_contexto']}"),
                "spec_yaml_sha256": ident["spec_yaml_sha256"],
                "script_blob_sha256": ident["script_blob_sha256"],
                "input_sha256_efectivos": ident["input_sha256_efectivos"],
                "codigo_commit": ejec["git_commit"],
                "fecha_verificacion": x["fecha_verificacion"],
                "entorno": "CAJA; corpus montado",
                "procedencia": "VERIFY-EJECUTADO · GEN2-CLASE-AMAI-1",
                "alcance": "NSE AMAI por hogar y pisos por grupo NSE, retrospectivo; no adopta",
                "nota": "forense/notas/2026-09-24-GEN2-CLASE-AMAI-1-nota.md",
            })
            print(calc)


if __name__ == "__main__":
    main(sys.argv[1])
