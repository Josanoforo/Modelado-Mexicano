#!/usr/bin/env python3
"""P2 (análisis, corregido) · ACTO GEN2-TUBERIA-CI-MEDICION-1.

El primer análisis (p2_analiza.py) agregaba `job=check` de corridas de
eras distintas de verify.yml bajo un solo nombre, mezclando el job
monolítico viejo (un solo job "check" que hacía TODO, hasta el 20/sep
~02:00) con el job de compuerta rápido actual (un solo paso, ~10-30s).
Este script segmenta por FIRMA de job (el conjunto de nombres de job
presentes en la corrida), que es la huella real de qué versión de
verify.yml corrió esa corrida -- más confiable que una fecha de corte,
porque distintos PRs corren con la versión de verify.yml de su propia
rama hasta que re-fusionan main (exactamente el defecto que el mandato
de este acto describe).
"""
import json
import statistics as st
from datetime import datetime, timezone

def parse_ts(s):
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def mediana_p90(vals):
    if not vals:
        return None, None
    vals = sorted(vals)
    med = st.median(vals)
    idx = min(len(vals) - 1, int(round(0.9 * (len(vals) - 1))))
    return round(med, 2), round(vals[idx], 2)


NOMBRES_ERA = {
    ("check",): "ERA1-monolitico (un solo job check, hasta 20/sep ~02:00)",
    ("adicionales", "check", "suite"): "ERA2-split-3job (suite+adicionales+check, sin guardias)",
    ("adicionales", "check", "guardias", "suite"): "ERA3-mas-guardias (suite+adicionales+guardias+check)",
    ("adicionales", "check", "guardias", "preflight-calc", "suite"): "ERA4-actual (+preflight-calc, desde PR #948)",
    (): "ERA0-sin-jobs (cancelada antes de programar ningun job)",
}


def main():
    with open("runs.json") as f:
        runs = {str(r["id"]): r for r in json.load(f)}
    with open("jobs.json") as f:
        jobs_por_run = json.load(f)

    era_de_run = {}
    for rid, jl in jobs_por_run.items():
        firma = tuple(sorted(j["name"] for j in jl))
        era_de_run[rid] = NOMBRES_ERA.get(firma, f"ERA-DESCONOCIDA{firma}")

    # censo de eras con rango de fechas
    censo = {}
    for rid, era in era_de_run.items():
        fecha = runs[rid]["created_at"]
        d = censo.setdefault(era, {"n": 0, "min": fecha, "max": fecha})
        d["n"] += 1
        d["min"] = min(d["min"], fecha)
        d["max"] = max(d["max"], fecha)

    with open("censo-eras-verify.tsv", "w") as f:
        f.write("era\tn_corridas\tprimera_vista\tultima_vista\n")
        for era, d in sorted(censo.items(), key=lambda kv: kv[1]["min"]):
            f.write(f"{era}\t{d['n']}\t{d['min']}\t{d['max']}\n")

    # por (era, job, paso)
    por_paso = {}
    por_job = {}
    for rid, jobs in jobs_por_run.items():
        era = era_de_run[rid]
        for j in jobs:
            ji, jf = parse_ts(j.get("started_at")), parse_ts(j.get("completed_at"))
            if ji and jf:
                por_job.setdefault((era, j["name"]), []).append((jf - ji).total_seconds())
            for s in j.get("steps", []) or []:
                si, sf = parse_ts(s.get("started_at")), parse_ts(s.get("completed_at"))
                if not (si and sf):
                    continue
                por_paso.setdefault((era, j["name"], s["name"]), []).append((sf - si).total_seconds())

    with open("duracion-por-paso-por-era.tsv", "w") as f:
        f.write("era\tjob\tpaso\tn\tmediana_s\tp90_s\n")
        for (era, job, paso), vals in sorted(
            por_paso.items(), key=lambda kv: (kv[0][0], -st.median(kv[1]))
        ):
            med, p90 = mediana_p90(vals)
            f.write(f"{era}\t{job}\t{paso}\t{len(vals)}\t{med}\t{p90}\n")

    with open("duracion-por-job-por-era.tsv", "w") as f:
        f.write("era\tjob\tn\tmediana_s\tp90_s\n")
        for (era, job), vals in sorted(por_job.items(), key=lambda kv: (kv[0][0], -st.median(kv[1]))):
            med, p90 = mediana_p90(vals)
            f.write(f"{era}\t{job}\t{len(vals)}\t{med}\t{p90}\n")

    print("Escrito censo-eras-verify.tsv, duracion-por-paso-por-era.tsv, duracion-por-job-por-era.tsv")


if __name__ == "__main__":
    main()
