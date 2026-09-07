#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tools/limpia_arbol.py --reporta` -- higiene del arbol de trabajo, en
modo REPORTE y solo en modo reporte.

ACTO GEN2-E3 · AUTOMATIZA-GEN2-1, pieza P4 (plan v2.0 §4/§8 Fase I).

QUE ES. Tres hechos sobre el clon, calculados con comandos de git a la
vista, para pegarlos en el ARRANQUE de `/acto`:

  A · WORKTREES vivos (`git worktree list`) -- un worktree olvidado es la
      forma mas comun de que dos sesiones editen el mismo rotulo.
  B · RAMAS LOCALES YA FUSIONADAS a `origin/main` que siguen vivas.
  C · BASE ATRASADA: cuantos commits hay de `HEAD` a `origin/main`
      (`git rev-list --count HEAD..origin/main`).

QUE NO ES, hoy. **No hay `--aplica`.** Borrar un worktree o una rama es
irreversible desde aqui y esa pieza es de `E4`/Fase IV: invocarlo sale con
codigo 2 y el rotulo NO-IMPLEMENTADO, igual que los subcomandos que `E2`
dejo declarados en `tools/corrida0.py`. Este script NUNCA escribe en el
arbol ni en el remoto; su unica accion sobre git es de lectura, y no hace
`fetch` por su cuenta (el ARRANQUE de `/acto` ya corre
`git fetch --prune` antes; un fetch escondido aqui haria que el conteo C
dependiera de cuando se llamo a este script, no del estado que el
operador acaba de mirar).

Exit code: 0 -- reportar que la base esta atrasada NO es un paro; el
ARRANQUE dice que en ese caso se hace `git merge` antes de nada.

Uso::

    python3 tools/limpia_arbol.py --reporta
    python3 tools/limpia_arbol.py --reporta --json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
BASE = "origin/main"


def _git(*args: str) -> tuple[int, str]:
    try:
        r = subprocess.run(["git", *args], cwd=RAIZ, capture_output=True,
                           text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as exc:  # pragma: no cover
        return 1, f"ERROR:{type(exc).__name__}"
    return r.returncode, (r.stdout if r.returncode == 0 else r.stderr).strip()


def worktrees() -> list[dict]:
    cod, salida = _git("worktree", "list", "--porcelain")
    if cod != 0:
        return [{"error": salida}]
    fuera, actual = [], {}
    for linea in salida.splitlines():
        if not linea.strip():
            if actual:
                fuera.append(actual)
            actual = {}
            continue
        clave, _, valor = linea.partition(" ")
        actual[clave] = valor
    if actual:
        fuera.append(actual)
    return fuera


def ramas_fusionadas_vivas() -> list[str]:
    """Ramas locales cuyo tip ya es ancestro de origin/main. `main` misma se
    excluye: no es residuo, es la base."""
    cod, salida = _git("for-each-ref", "--format=%(refname:short)", "refs/heads")
    if cod != 0:
        return []
    vivas = []
    for rama in salida.splitlines():
        if rama in ("main", "master"):
            continue
        c, _ = _git("merge-base", "--is-ancestor", rama, BASE)
        if c == 0:
            vivas.append(rama)
    return vivas


def base_atrasada() -> dict:
    cod, salida = _git("rev-list", "--count", f"HEAD..{BASE}")
    if cod != 0:
        return {"commits_detras": None,
                "nota": f"no se pudo contar contra {BASE}: {salida[:120]}",
                "comando": f"git rev-list --count HEAD..{BASE}"}
    n = int(salida or 0)
    return {"commits_detras": n,
            "al_dia": "SI" if n == 0 else "NO",
            "remedio": None if n == 0 else f"git merge {BASE}  (no es PARO)",
            "comando": f"git rev-list --count HEAD..{BASE}"}


def reporte() -> dict:
    wts = worktrees()
    return {
        "worktrees": {
            "n": len(wts),
            "detalle": wts,
            "comando": "git worktree list --porcelain",
        },
        "ramas_fusionadas_vivas": {
            "n": len(ramas_fusionadas_vivas()),
            "detalle": ramas_fusionadas_vivas(),
            "comando": "git merge-base --is-ancestor <rama> " + BASE,
        },
        "base": base_atrasada(),
        "aplica": "NO-IMPLEMENTADO -- el `--aplica` es E4/Fase IV",
    }


def imprime(r: dict) -> None:
    print("LIMPIA-ARBOL · REPORTE (nunca escribe)")
    w = r["worktrees"]
    print(f"  A · worktrees vivos: {w['n']}   [{w['comando']}]")
    for wt in w["detalle"]:
        print(f"      {wt.get('worktree', '?')}  rama={wt.get('branch', '(detached)')}")
    b = r["ramas_fusionadas_vivas"]
    print(f"  B · ramas locales ya fusionadas a {BASE} y vivas: {b['n']}   [{b['comando']}]")
    for rama in b["detalle"]:
        print(f"      {rama}")
    c = r["base"]
    print(f"  C · base: HEAD esta {c['commits_detras']} commits detras de {BASE} "
          f"(al_dia={c.get('al_dia')})   [{c['comando']}]")
    if c.get("remedio"):
        print(f"      remedio: {c['remedio']}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="limpia_arbol", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reporta", action="store_true", help="reporta (unico modo)")
    ap.add_argument("--aplica", action="store_true",
                    help="[NO-IMPLEMENTADO] E4/Fase IV")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.aplica:
        print("NO-IMPLEMENTADO: `limpia_arbol --aplica` es E4/Fase IV. Este "
              "script solo reporta -- borrar un worktree o una rama es "
              "irreversible y no se decide aqui.", file=sys.stderr)
        return 2
    if not a.reporta:
        ap.print_help()
        return 2
    r = reporte()
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1, sort_keys=True))
    else:
        imprime(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
