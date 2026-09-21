#!/usr/bin/env python3
"""P4 (complemento) · ACTO GEN2-TUBERIA-CI-MEDICION-1. Re-verificación
propia (no heredada) de dos cifras que TUBERÍA reportó como antecedente
(re-fusiones de main y renumeración por PR).

CORREGIDO por ADENDA-1: la primera versión contaba re-fusión por MENSAJE
de commit (`Merge branch 'main'`/`Merge remote-tracking branch`), y esa
forma sólo cubre la mitad de cómo la casa escribe sus re-fusiones -- la
otra mitad usa mensajes como "GEN2-…: merge origin/main (…) y renumera",
que el patrón no reconocía, subcontando por dos. Ahora cuenta TODO commit
con dos padres en la rama del PR (`gh api .../pulls/{n}/commits`, campo
`parents`), sin mirar el mensaje -- es la definición mecánica de
"re-fusión" (un merge commit), no una lista de frases.
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
            ["gh", "api", f"repos/{REPO}/pulls/{n}/commits?per_page=100"],
            capture_output=True, text=True,
        )
        if out.returncode != 0:
            filas.append((n, "NO-ACCESIBLE", "", ""))
            continue
        commits = json.loads(out.stdout)
        if len(commits) >= 100:
            sys.stderr.write(f"AVISO: PR {n} tiene >=100 commits, posible truncado (per_page=100)\n")
        n_merge = sum(1 for c in commits if len(c.get("parents", [])) >= 2)
        msgs = [c["commit"]["message"] for c in commits]
        n_adr_renum = sum(1 for m in msgs if re.search(r"renumer", m, re.I))
        filas.append((n, str(n_merge), str(n_adr_renum), str(len(commits))))
        if (i + 1) % 20 == 0:
            sys.stderr.write(f"{i+1}/{len(prs)}\n")

    with open("refusiones-por-pr.tsv", "w") as f:
        f.write("pr\tn_merge_2padres\tn_commits_renumeracion\tn_commits_total\n")
        for row in filas:
            f.write("\t".join(row) + "\n")

    con_refusion = sum(1 for r in filas if r[1].isdigit() and int(r[1]) >= 1)
    con_2mas = sum(1 for r in filas if r[1].isdigit() and int(r[1]) >= 2)
    con_renum = sum(1 for r in filas if r[2].isdigit() and int(r[2]) >= 1)
    n_ok = sum(1 for r in filas if r[1].isdigit())
    print(f"PRs examinados: {len(filas)} (con dato legible: {n_ok})")
    print(f"con >=1 commit de 2 padres (re-fusion): {con_refusion} ({100*con_refusion/n_ok:.1f}%)")
    print(f"con >=2 commits de 2 padres (re-fusion): {con_2mas} ({100*con_2mas/n_ok:.1f}%)")
    print(f"con >=1 commit de mensaje 'renumer...': {con_renum}")


if __name__ == "__main__":
    main()
