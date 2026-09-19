#!/usr/bin/env python3
"""Asienta únicamente la evidencia aislada de los cruces históricos ENCIG."""
from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = Path(__file__).with_name("evidencia-replay-encig-cruces-historicos-2026-09-19.json")
REGISTER = ROOT / "forense/replay-evidencia.tsv"
ALLOWED = {
    "CALC-ENCIG2023-CRUCES-HISTORICOS-0002",
    "CALC-ENCIG2021-CRUCES-HISTORICOS-0003",
}
HEAD = [
    "calc_id", "corrida_id", "resultado_replay", "contexto_replay", "razones",
    "spec_yaml_sha256", "script_blob_sha256", "input_sha256_efectivos",
    "codigo_commit", "fecha_verificacion", "entorno", "procedencia", "alcance", "nota",
]


def main() -> int:
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    if {item.get("calc_id") for item in evidence} != ALLOWED:
        raise SystemExit("evidencia fuera del lote ENCIG autorizado")
    with REGISTER.open(encoding="utf-8", newline="") as stream:
        old = list(csv.DictReader(stream, delimiter="\t"))
    if not old or list(old[0]) != HEAD:
        raise SystemExit("esquema replay-evidencia.tsv inesperado")
    by_id = {row["calc_id"]: row for row in old}
    added = []
    for item in evidence:
        calc_id = item["calc_id"]
        execution = json.loads((ROOT / "data/corrida0" / calc_id / "ejecucion.json").read_text(encoding="utf-8"))
        identity = item["identidad"]
        if execution.get("spec_yaml_sha256") != identity["spec_yaml_sha256"]:
            raise SystemExit(f"{calc_id}: spec_yaml_sha256 no coincide")
        if execution.get("script_blob_sha256") != identity["script_blob_sha256"]:
            raise SystemExit(f"{calc_id}: script_blob_sha256 no coincide")
        inputs = ",".join(f"{key}={value}" for key, value in sorted(execution.get("input_sha256", {}).items()))
        if inputs != identity["input_sha256_efectivos"]:
            raise SystemExit(f"{calc_id}: input_sha256_efectivos no coincide")
        if item.get("exit_code") != 0 or item.get("detalle_verify", {}).get("resultado") != "REPRODUCE":
            raise SystemExit(f"{calc_id}: replay no reproduce")
        if calc_id in by_id:
            existing = by_id[calc_id]
            keys = ("corrida_id", "resultado_replay", "contexto_replay", "spec_yaml_sha256",
                    "script_blob_sha256", "input_sha256_efectivos")
            expected = {
                "corrida_id": execution["corrida_id"],
                "resultado_replay": item["resultado_replay"],
                "contexto_replay": item["contexto_replay"],
                **identity,
            }
            if any(existing[key] != expected[key] for key in keys):
                raise SystemExit(f"{calc_id}: asiento previo contradictorio")
            continue
        reasons = "; ".join(item["detalle_verify"].get("razones_contexto", []))
        added.append({
            "calc_id": calc_id,
            "corrida_id": execution["corrida_id"],
            "resultado_replay": item["resultado_replay"],
            "contexto_replay": item["contexto_replay"],
            "razones": f"{reasons}; RESULTADO=REPRODUCE" if reasons else "RESULTADO=REPRODUCE",
            "spec_yaml_sha256": identity["spec_yaml_sha256"],
            "script_blob_sha256": identity["script_blob_sha256"],
            "input_sha256_efectivos": identity["input_sha256_efectivos"],
            "codigo_commit": execution["git_commit"],
            "fecha_verificacion": item["fecha_verificacion"],
            "entorno": "CAJA (Ubuntu/WSL2) con corpus montado",
            "procedencia": "VERIFY-AISLADO · GEN2-ENCIG-CRUCES-HISTORICOS-CLI-1",
            "alcance": "replay de los dos CALC consumidos por 02-seleccion.json; sin adopción ni apertura de 2025",
            "nota": "forense/analisis/gen2-encig-cruces-historicos-cli-1/evidencia-replay-encig-cruces-historicos-2026-09-19.json",
        })
    with REGISTER.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=HEAD, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(old + added)
    print(f"asientos_nuevos={len(added)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
