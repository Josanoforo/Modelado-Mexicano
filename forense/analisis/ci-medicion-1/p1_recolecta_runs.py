#!/usr/bin/env python3
"""P1 · ACTO GEN2-TUBERIA-CI-MEDICION-1 (21/sep/2026)
Descarga el universo de corridas de verify.yml desde el 18/sep hasta la
cabeza, via `gh api`. Script de un solo uso: no es infraestructura.

Uso:
    python3 p1_recolecta_runs.py

Escribe:
    runs.json            -- lista cruda de corridas (gh api, un objeto por corrida)
    universo-corridas.tsv -- P1: id, evento, rama, commit, intento, conclusion, creacion, inicio, fin
"""
import json
import subprocess
import sys

REPO = "Josanoforo/Modelado-Mexicano"
WORKFLOW = "verify.yml"
DESDE = "2026-09-18"


def gh_api(path, extra=None):
    cmd = ["gh", "api", path]
    if extra:
        cmd += extra
    out = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def fetch_all_runs():
    runs = []
    page = 1
    per_page = 100
    while True:
        path = (
            f"repos/{REPO}/actions/workflows/{WORKFLOW}/runs"
            f"?per_page={per_page}&page={page}&created=%3E%3D{DESDE}"
        )
        data = gh_api(path)
        batch = data.get("workflow_runs", [])
        runs.extend(batch)
        total = data.get("total_count", 0)
        sys.stderr.write(f"pagina {page}: {len(batch)} corridas (acumulado {len(runs)}/{total})\n")
        if len(batch) < per_page or len(runs) >= total:
            break
        page += 1
    return runs


def main():
    runs = fetch_all_runs()
    with open("runs.json", "w") as f:
        json.dump(runs, f, indent=1)
    sys.stderr.write(f"TOTAL corridas examinadas: {len(runs)}\n")

    with open("universo-corridas.tsv", "w") as f:
        f.write("id\tevento\trama\tcommit\tintento\tconclusion\tstatus\tcreado\tiniciado\tactualizado\turl\n")
        for r in runs:
            f.write(
                "\t".join(
                    str(x)
                    for x in [
                        r["id"],
                        r.get("event", ""),
                        r.get("head_branch", ""),
                        r.get("head_sha", "")[:12],
                        r.get("run_attempt", ""),
                        r.get("conclusion") or "",
                        r.get("status", ""),
                        r.get("created_at", ""),
                        r.get("run_started_at", ""),
                        r.get("updated_at", ""),
                        r.get("html_url", ""),
                    ]
                )
                + "\n"
            )
    sys.stderr.write("Escrito universo-corridas.tsv\n")


if __name__ == "__main__":
    main()
