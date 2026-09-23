#!/usr/bin/env python3
"""Deriva las lecturas legacy activas y su siguiente operación sin adoptar."""
from __future__ import annotations

import csv
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "forense/analisis/astra4-relevo/inventario-operativo.tsv"
FIELDS = [
    "slot", "consumidor", "tipo_uso", "generacion_actual", "valor_actual",
    "estimando_requerido", "calc_candidato", "result_candidato",
    "valor_candidato", "veredicto", "veredicto_sellado_ref", "via_autorizada",
    "replay_ref", "firma_o_pin", "siguiente_operacion", "razon",
]


def main() -> None:
    with (ROOT / "data/corrida0/usos.tsv").open(newline="") as stream:
        uses = list(csv.DictReader((x for x in stream if not x.startswith("#")), delimiter="\t"))
    active = {u["resultado_id"]: u for u in uses if u["activo"] == "SI" and u["generacion_leida"].startswith("LEGACY")}
    candidates = json.loads(subprocess.run(
        [sys.executable, str(ROOT / "tools/relevo_usos.py"), "--json"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout)
    by_slot = {row["resultado_id"]: row for row in candidates}
    if set(active) != set(active) & set(by_slot):
        raise ValueError("slot activo sin clasificación de relevo")
    rows = []
    for slot, use in sorted(active.items()):
        item = by_slot[slot]
        verdict = item["veredicto"]
        path = use["consumidor"].split(":", 1)[0]
        if path.startswith("forense/prereg-duelo-v2/") or path == "milpa/procedencia.yaml":
            action = "DICTAMINAR-HISTORICO-SIN-RELEVO-POR-FILA-O-MEDIR-SI-SIGUE-CONSUMO"
        elif path == "milpa/catalogo-momentos-v0_1.tsv":
            action = "MEDIR-CALC-O-PLAN-FECHADO-CON-DEPENDENCIA"
        elif verdict == "LISTADO-PARA-MESA":
            action = "FP-DE-IDENTIDAD-Y-PIN; SIN-AUTOADOPCION"
        elif verdict in {"VETADO-POR-DECISION", "NO-ADOPTABLE-POR-VEREDICTO-SELLADO"}:
            action = "NUEVO-CALC-EXACTO-O-DICTAMEN-DE-IMPEDIMENTO"
        elif item["razon"].startswith("CORR-CON-CALC-SIN-RESULT-FIJADO"):
            action = "RESOLVER-CONFLICTO-DE-RESULT-Y-FP"
        else:
            action = "PREPARAR-CALC-RELEVO-DESDE-CRUDO-CON-SPEC-CONGELADA"
        rows.append({
            "slot": slot,
            "consumidor": use["consumidor"],
            "tipo_uso": use["tipo_uso"],
            "generacion_actual": use["generacion_leida"],
            "valor_actual": item["valor_legacy"],
            "estimando_requerido": use["reglas_impacto"] + ":" + use["consumidor"].split(":")[-1],
            "calc_candidato": item["calc_candidato"],
            "result_candidato": item["result_gen2_candidato"],
            "valor_candidato": item["valor_gen2"],
            "veredicto": verdict,
            "veredicto_sellado_ref": item["veredicto_sellado_ref"],
            "via_autorizada": item["canal"] or "NINGUNA-ACREDITADA",
            "replay_ref": item["corrida_oferta"],
            "firma_o_pin": item["resolucion_vigente"] or use["pin_de_mesa"],
            "siguiente_operacion": action,
            "razon": item["razon"],
        })
    if len(rows) != 146:
        raise ValueError(f"el contador de 146 cambió a {len(rows)}; revisar status")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"legacy_activos={len(rows)}")


if __name__ == "__main__":
    main()
