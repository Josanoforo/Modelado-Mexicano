#!/usr/bin/env python3
"""P4 (complemento) · ACTO GEN2-TUBERIA-CI-MEDICION-1. Re-verificación
propia (no heredada) de dos cifras que TUBERÍA reportó como antecedente
(re-fusiones de main y renumeración por PR): cuenta commits de merge de
`main`/`origin/main` en el historial de cada PR fusionado desde el 18/sep,
via `gh pr view <n> --json commits`.
"""
import csv
import json
import re
import subprocess
import sys

REPO = "Josanoforo/Modelado-Mexicano"


def main():
    prs = [row["pr"] for row in csv.DictReader(open("espera-ci-por-pr.tsv"), delimiter="\t")]
    filas = []
    for i, n in enumerate(prs):
        out = subprocess.run(
            ["gh", "pr", "view", n, "--repo", REPO, "--json", "commits"],
            capture_output=True, text=True,
        )
        if out.returncode != 0:
            filas.append((n, "NO-ACCESIBLE", "", ""))
            continue
        data = json.loads(out.stdout)
        msgs = [c["messageHeadline"] for c in data.get("commits", [])]
        n_merge_main = sum(
            1 for m in msgs if re.search(r"[Mm]erge (branch|remote-tracking branch)\s*'?(origin/)?main'?", m)
        )
        n_adr_renum = sum(1 for m in msgs if re.search(r"renumer", m, re.I))
        filas.append((n, str(n_merge_main), str(n_adr_renum), str(len(msgs))))
        if (i + 1) % 20 == 0:
            sys.stderr.write(f"{i+1}/{len(prs)}\n")

    with open("refusiones-por-pr.tsv", "w") as f:
        f.write("pr\tn_merge_main_commits\tn_commits_renumeracion\tn_commits_total\n")
        for row in filas:
            f.write("\t".join(row) + "\n")

    con_refusion = sum(1 for r in filas if r[1].isdigit() and int(r[1]) >= 1)
    con_2mas = sum(1 for r in filas if r[1].isdigit() and int(r[1]) >= 2)
    con_renum = sum(1 for r in filas if r[2].isdigit() and int(r[2]) >= 1)
    n_ok = sum(1 for r in filas if r[1].isdigit())
    print(f"PRs examinados: {len(filas)} (con dato legible: {n_ok})")
    print(f"con >=1 commit de merge de main: {con_refusion} ({100*con_refusion/n_ok:.1f}%)")
    print(f"con >=2 commits de merge de main: {con_2mas} ({100*con_2mas/n_ok:.1f}%)")
    print(f"con >=1 commit de mensaje 'renumer...': {con_renum}")


if __name__ == "__main__":
    main()
