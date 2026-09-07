#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/verifica_head_remoto.py -- guard de sólo lectura: HEAD local ==
HEAD remoto vivo (ACTO AUTOMATIZA-2-A · BLINDA-HEAD-PR,
`forense/encargos/2026-09-07-AUTOMATIZA-2-A-BLINDA-HEAD-PR.md`).

QUÉ ES Y QUÉ NO ES. Defecto real que corrige: `PR #572` se fusionó contra
un `HEAD` anterior al último commit de cierre -- el `## CONSUMIDO` quedó
fuera y se incorporó después vía `PR #576`. `/despacha` hace dos pushes
(trabajo del acto, luego estado/bitácora/`## CONSUMIDO`) y no había un
guard final que probara que el remoto terminó exactamente en el `HEAD`
local. Este script SÓLO LEE: nunca push, fetch, commit, merge, abre PR,
llama a la API de GitHub, ni cambia archivos. No se integra en
`tools/cierre_acto.py` -- ese es preflight/cierre de cascada, no guard de
entrega.

Evidencia, siempre contra el remoto vivo (nunca `refs/remotes/origin/*`,
que puede estar stale):
    git rev-parse HEAD
    git ls-remote --heads <remote> refs/heads/<rama>

Estados y exit codes:
    0  PR_HEAD_SINCRONIZADO       -- local == remote
    2  PR_HEAD_DESACTUALIZADO     -- rama existe, SHA remoto != local
    3  RAMA_AUSENTE_EN_ORIGIN     -- ls-remote respondió, sin esa rama
    4  HEAD_REMOTO_NO_VERIFICABLE -- ls-remote falló (remoto no verificable)

Rama ausente y fallo de red/remoto son hallazgos distintos -- nunca se
colapsan en el mismo exit code.

Uso:
    python3 tools/verifica_head_remoto.py
    python3 tools/verifica_head_remoto.py --remote origin --branch <rama>

Sin --branch, se deriva con `git branch --show-current`.
"""
import argparse
import subprocess
import sys


def _rev_parse_head():
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def _current_branch():
    return subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def _ls_remote_heads(remote, branch):
    ref = "refs/heads/{}".format(branch)
    return subprocess.run(
        ["git", "ls-remote", "--heads", remote, ref],
        capture_output=True, text=True,
    )


def verifica(remote, branch):
    """Devuelve (codigo_salida, lineas_de_reporte)."""
    local = _rev_parse_head()
    proc = _ls_remote_heads(remote, branch)

    if proc.returncode != 0:
        lineas = [
            "HEAD_REMOTO_NO_VERIFICABLE",
            "rama={}".format(branch),
            "local={}".format(local),
            "refs_examinadas=0",
        ]
        diagnostico = (proc.stderr or proc.stdout).strip()
        if diagnostico:
            lineas.append("diagnostico={}".format(diagnostico.splitlines()[-1]))
        lineas.append("NO FUSIONAR")
        return 4, lineas

    ref_suffix = "refs/heads/{}".format(branch)
    matches = [
        linea for linea in proc.stdout.splitlines()
        if linea.strip() and linea.split()[-1] == ref_suffix
    ]
    refs_examinadas = len(matches)

    if refs_examinadas == 0:
        return 3, [
            "RAMA_AUSENTE_EN_ORIGIN",
            "rama={}".format(branch),
            "local={}".format(local),
            "refs_examinadas=0",
            "NO FUSIONAR",
        ]

    remote_sha = matches[0].split()[0]

    if remote_sha == local:
        return 0, [
            "PR_HEAD_SINCRONIZADO",
            "rama={}".format(branch),
            "local={}".format(local),
            "remote={}".format(remote_sha),
            "refs_examinadas={}".format(refs_examinadas),
        ]

    return 2, [
        "PR_HEAD_DESACTUALIZADO",
        "rama={}".format(branch),
        "local={}".format(local),
        "remote={}".format(remote_sha),
        "refs_examinadas={}".format(refs_examinadas),
        "NO FUSIONAR",
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Verifica, de sólo lectura, que HEAD local == HEAD "
                     "remoto vivo de una rama."
    )
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--branch", default=None,
                         help="Rama a verificar. Default: git branch --show-current.")
    args = parser.parse_args(argv)

    branch = args.branch or _current_branch()
    codigo, lineas = verifica(args.remote, branch)
    for linea in lineas:
        print(linea)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
