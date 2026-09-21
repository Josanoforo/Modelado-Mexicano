#!/usr/bin/env python3
"""P5 (insumo) · evidencia de captura por paso de verify.yml: cuántas veces
falló, cuándo por última vez, y si algún fallo fue en rama de PR (el test
atrapó algo ANTES de fusionar) o en push a main (algo se coló). Fuente:
jobs-pasos.tsv (P2) + runs.json (P1) para evento/rama/fecha.
"""
import csv
import json

with open("runs.json") as f:
    runs = {str(r["id"]): r for r in json.load(f)}

filas = list(csv.DictReader(open("jobs-pasos.tsv"), delimiter="\t"))

agg = {}
for row in filas:
    key = (row["job"], row["paso"])
    r = runs.get(row["run_id"], {})
    d = agg.setdefault(key, {"n_corridas": 0, "n_fail": 0, "ultimo_fail": "", "fail_en_pr": 0, "fail_en_push": 0})
    if row["paso_conclusion"] in ("success", "failure"):
        d["n_corridas"] += 1
    if row["paso_conclusion"] == "failure":
        d["n_fail"] += 1
        fecha = r.get("created_at", "")
        if fecha > d["ultimo_fail"]:
            d["ultimo_fail"] = fecha
        if r.get("event") == "pull_request":
            d["fail_en_pr"] += 1
        elif r.get("event") == "push":
            d["fail_en_push"] += 1

with open("evidencia-pasos-verify.tsv", "w") as f:
    f.write("job\tpaso\tn_corridas_completas\tn_fail\tultimo_fail\tfail_en_pr\tfail_en_push\n")
    for (job, paso), d in sorted(agg.items(), key=lambda kv: -kv[1]["n_fail"]):
        f.write(
            f"{job}\t{paso}\t{d['n_corridas']}\t{d['n_fail']}\t{d['ultimo_fail']}\t"
            f"{d['fail_en_pr']}\t{d['fail_en_push']}\n"
        )
print("Escrito evidencia-pasos-verify.tsv")
