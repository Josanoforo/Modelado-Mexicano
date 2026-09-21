#!/usr/bin/env python3
"""P2 · ACTO GEN2-TUBERIA-CI-MEDICION-1 (21/sep/2026)
Para cada corrida de runs.json (P1), baja jobs+pasos via `gh api`.
Script de un solo uso.

Uso:
    python3 p2_recolecta_jobs.py

Lee:  runs.json
Escribe:
    jobs.json          -- {run_id: [job, ...]} crudo
    jobs-pasos.tsv      -- P2: run_id, job, paso, inicio, fin, conclusion, duracion_s
"""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone

REPO = "Josanoforo/Modelado-Mexicano"


def gh_api(path):
    for intento in range(3):
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True)
        if out.returncode == 0:
            return json.loads(out.stdout)
        sys.stderr.write(f"reintento {intento+1} para {path}: {out.stderr[:200]}\n")
        time.sleep(2)
    raise RuntimeError(f"fallo persistente: {path} :: {out.stderr[:300]}")


def parse_ts(s):
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def main():
    with open("runs.json") as f:
        runs = json.load(f)

    jobs_por_run = {}
    fallidas = []
    for i, r in enumerate(runs):
        run_id = r["id"]
        path = f"repos/{REPO}/actions/runs/{run_id}/jobs?per_page=100"
        try:
            data = gh_api(path)
        except RuntimeError as e:
            sys.stderr.write(f"NO-ACCESIBLE run {run_id}: {e}\n")
            fallidas.append(run_id)
            continue
        jobs_por_run[str(run_id)] = data.get("jobs", [])
        if (i + 1) % 25 == 0:
            sys.stderr.write(f"{i+1}/{len(runs)} corridas procesadas\n")

    with open("jobs.json", "w") as f:
        json.dump(jobs_por_run, f, indent=1)

    sys.stderr.write(
        f"TOTAL corridas con jobs leidos: {len(jobs_por_run)}/{len(runs)}; "
        f"NO-ACCESIBLE: {len(fallidas)} {fallidas}\n"
    )

    with open("jobs-pasos.tsv", "w") as f:
        f.write("run_id\tjob\tjob_conclusion\tpaso\tpaso_conclusion\tinicio\tfin\tduracion_s\n")
        for run_id, jobs in jobs_por_run.items():
            for j in jobs:
                job_name = j.get("name", "")
                job_concl = j.get("conclusion") or ""
                for s in j.get("steps", []) or []:
                    ini = parse_ts(s.get("started_at"))
                    fin = parse_ts(s.get("completed_at"))
                    dur = (fin - ini).total_seconds() if ini and fin else ""
                    f.write(
                        "\t".join(
                            str(x)
                            for x in [
                                run_id,
                                job_name,
                                job_concl,
                                s.get("name", ""),
                                s.get("conclusion") or "",
                                s.get("started_at") or "",
                                s.get("completed_at") or "",
                                dur,
                            ]
                        )
                        + "\n"
                    )
    sys.stderr.write("Escrito jobs-pasos.tsv\n")

    with open("corridas-fallidas-p2.tsv", "w") as f:
        f.write("run_id\n")
        for rid in fallidas:
            f.write(f"{rid}\n")


if __name__ == "__main__":
    main()
