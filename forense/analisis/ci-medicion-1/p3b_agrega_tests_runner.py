#!/usr/bin/env python3
"""P3 (agregación) · a partir de tiempos-tests-runner.tsv y
fallos-tests-runner.tsv (P3, log crudo por corrida), agrega por test:
mediana/p90 de duración en runner, y evidencia de fallo (conteo, último,
si fue en rama de PR o en push a main).
"""
import csv
import statistics as st
from collections import defaultdict

tiempos = defaultdict(list)
with open("tiempos-tests-runner.tsv") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        try:
            tiempos[row["test"]].append(float(row["duracion_s"]))
        except ValueError:
            continue

with open("tiempos-tests-runner-agg.tsv", "w") as f:
    f.write("test\tn\tmediana_s\tp90_s\n")
    for test, vals in sorted(tiempos.items()):
        vals.sort()
        med = st.median(vals)
        p90 = vals[min(len(vals) - 1, int(round(0.9 * (len(vals) - 1))))]
        f.write(f"{test}\t{len(vals)}\t{round(med,2)}\t{round(p90,2)}\n")

fallos = defaultdict(lambda: {"n": 0, "ultimo": "", "en_pr": 0, "en_push": 0})
with open("fallos-tests-runner.tsv") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        d = fallos[row["test"]]
        d["n"] += 1
        d["ultimo"] = max(d["ultimo"], row["run_id"])  # proxy de orden; se cruza con runs.json en el ensamblado
        if row["evento"] == "pull_request":
            d["en_pr"] += 1
        elif row["evento"] == "push":
            d["en_push"] += 1

with open("fallos-tests-runner-agg.tsv", "w") as f:
    f.write("test\tn_fallos\tultimo_run_id\tfallos_en_pr\tfallos_en_push\n")
    for test, d in sorted(fallos.items(), key=lambda kv: -kv[1]["n"]):
        f.write(f"{test}\t{d['n']}\t{d['ultimo']}\t{d['en_pr']}\t{d['en_push']}\n")

print(f"{len(tiempos)} tests con tiempo agregado; {len(fallos)} tests con >=1 fallo")
