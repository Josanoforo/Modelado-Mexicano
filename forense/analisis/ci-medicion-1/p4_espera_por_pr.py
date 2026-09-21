#!/usr/bin/env python3
"""P4 · ACTO GEN2-TUBERIA-CI-MEDICION-1. Espera de CI por PR fusionado desde
el 18/sep: corridas por PR (via head_branch en runs.json), canceladas,
tiempo total de runner y de reloj. Script de un solo uso.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone

REPO = "Josanoforo/Modelado-Mexicano"


def parse_ts(s):
    if not s:
        return None
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def main():
    prs = json.loads(
        subprocess.run(
            [
                "gh", "pr", "list", "--state", "merged",
                "--search", "merged:>=2026-09-18",
                "--json", "number,title,mergedAt,createdAt,headRefName,baseRefName",
                "--limit", "500",
            ],
            capture_output=True, text=True, check=True,
        ).stdout
    )
    with open("runs.json") as f:
        runs = json.load(f)
    with open("jobs.json") as f:
        jobs_por_run = json.load(f)

    por_rama = {}
    for r in runs:
        por_rama.setdefault(r.get("head_branch", ""), []).append(r)

    filas = []
    for pr in prs:
        rama = pr["headRefName"]
        corridas = por_rama.get(rama, [])
        n_corridas = len(corridas)
        canceladas = sum(1 for c in corridas if c.get("conclusion") == "cancelled")
        tiempo_reloj = 0.0
        tiempo_runner = 0.0
        for c in corridas:
            ini = parse_ts(c.get("run_started_at"))
            fin = parse_ts(c.get("updated_at"))
            if ini and fin:
                tiempo_reloj += (fin - ini).total_seconds()
            for j in jobs_por_run.get(str(c["id"]), []):
                ji = parse_ts(j.get("started_at"))
                jf = parse_ts(j.get("completed_at"))
                if ji and jf:
                    tiempo_runner += (jf - ji).total_seconds()
        filas.append(
            {
                "pr": pr["number"],
                "titulo": pr["title"][:80],
                "rama": rama,
                "creado": pr["createdAt"],
                "fusionado": pr["mergedAt"],
                "n_corridas": n_corridas,
                "canceladas": canceladas,
                "tiempo_reloj_s": round(tiempo_reloj, 1),
                "tiempo_runner_s": round(tiempo_runner, 1),
            }
        )

    con_corridas = [f for f in filas if f["n_corridas"] > 0]
    sin_corridas = [f for f in filas if f["n_corridas"] == 0]
    sys.stderr.write(
        f"PRs examinados: {len(filas)}; con >=1 corrida hallada por rama: {len(con_corridas)}; "
        f"sin corrida (rama borrada antes de indexar / rama distinta al PR): {len(sin_corridas)}\n"
    )

    with open("espera-ci-por-pr.tsv", "w") as f:
        f.write("pr\ttitulo\trama\tcreado\tfusionado\tn_corridas\tcanceladas\ttiempo_reloj_s\ttiempo_runner_s\n")
        for r in filas:
            f.write(
                f"{r['pr']}\t{r['titulo']}\t{r['rama']}\t{r['creado']}\t{r['fusionado']}\t"
                f"{r['n_corridas']}\t{r['canceladas']}\t{r['tiempo_reloj_s']}\t{r['tiempo_runner_s']}\n"
            )
    with open("pr-sin-corrida-indexada.tsv", "w") as f:
        f.write("pr\ttitulo\trama\n")
        for r in sin_corridas:
            f.write(f"{r['pr']}\t{r['titulo']}\t{r['rama']}\n")
    sys.stderr.write("Escrito espera-ci-por-pr.tsv y pr-sin-corrida-indexada.tsv\n")


if __name__ == "__main__":
    main()
