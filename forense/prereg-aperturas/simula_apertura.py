#!/usr/bin/env python3
"""Simula la receta de apertura de un expediente, sin payload y sin tocar el clon.

ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026). D-23: todo ocurre en un `git worktree` temporal
(se borra al terminar); el clon que verifica no cambia.

    python3 forense/prereg-aperturas/simula_apertura.py <X> [<X> ...]    # X = PROGRAMA-OLA; `--todos` = todos

Pasos (los de `RECETA-APERTURA-<X>.md` §4): copia el árbol de trabajo de `forense/prereg-aperturas/` al
worktree; en su `data/manifiesto.yaml` levanta la custodia de los payloads del contrato (sólo texto: quita
`estado_reserva`, `raiz: data_raw`); copia el contrato a `data/corrida0/CALC-APERTURA-<X>-0001/spec.yaml`;
commit local; `corrida0 preflight`. Imprime el veredicto y los bloqueos. En NUBE el payload no existe: el
único resultado aceptable es VERDE con avisos `NO-VISIBLE-EN-ESTE-CONTEXTO` (FP-352), nunca un bloqueo.
"""
from __future__ import annotations

import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))


def _sh(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=600)


def _levanta_custodia(manifiesto: str, ids: set[str]) -> int:
    """Edita por texto el bloque `- id: <pid>` del manifiesto del worktree: quita `estado_reserva` y fija
    `raiz: data_raw`. Devuelve cuántas entradas tocó."""
    lineas = open(manifiesto, encoding="utf-8").read().split("\n")
    out, dentro, tocadas, tiene_raiz = [], False, 0, False
    for ln in lineas:
        m = re.match(r"^- id: (\S+)\s*$", ln)
        if m:
            if dentro and not tiene_raiz:
                out.append("  raiz: data_raw")
            dentro = m.group(1).strip("'\"") in ids
            tocadas += dentro
            tiene_raiz = False
            out.append(ln)
            continue
        if dentro and re.match(r"^  estado_reserva:", ln):
            continue
        if dentro and re.match(r"^  raiz:", ln):
            out.append("  raiz: data_raw")
            tiene_raiz = True
            continue
        out.append(ln)
    if dentro and not tiene_raiz:
        out.append("  raiz: data_raw")
    open(manifiesto, "w", encoding="utf-8").write("\n".join(out))
    return tocadas


def simula(x: str, wt: str) -> tuple[str, str]:
    contrato = os.path.join(AQUI, x, f"APERTURA-{x}-spec.yaml")
    spec = yaml.safe_load(open(contrato, encoding="utf-8"))
    ids = {e["id"] for e in spec["inputs"] if e["origen"] == "manifiesto"}
    n = _levanta_custodia(os.path.join(wt, "data", "manifiesto.yaml"), ids)
    d = os.path.join(wt, "data", "corrida0", spec["calc_id"])
    os.makedirs(d, exist_ok=True)
    shutil.copy(contrato, os.path.join(d, "spec.yaml"))
    _sh(["git", "add", "-A"], wt)
    _sh(["git", "-c", "user.email=simula@local", "-c", "user.name=simula", "commit", "-qm", f"simula {x}"], wt)
    r = _sh([sys.executable, "tools/corrida0.py", "preflight", spec["calc_id"]], wt)
    final = [ln for ln in r.stdout.splitlines() if ln.startswith("PRE-FLIGHT:") or "VEREDICTO" in ln.upper()]
    avisos = sum("NO-VISIBLE-EN-ESTE-CONTEXTO" in ln for ln in r.stdout.splitlines())
    return (f"payloads={len(ids)} custodia_levantada={n} avisos_no_visible={avisos}",
            (final[-1] if final else r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-300:]))


def main(argv):
    xs = argv or []
    if "--todos" in xs:
        xs = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(AQUI, "*", "APERTURA-*-spec.yaml")))
    malos = 0
    for x in xs:
        base = tempfile.mkdtemp(prefix="simula-apertura-")
        wt = os.path.join(base, "wt")
        try:
            _sh(["git", "worktree", "add", "-q", "--detach", wt, "HEAD"], RAIZ)
            destino = os.path.join(wt, "forense", "prereg-aperturas")
            shutil.rmtree(destino, ignore_errors=True)
            shutil.copytree(AQUI, destino, ignore=shutil.ignore_patterns("__pycache__"))
            info, veredicto = simula(x, wt)
            ok = "VERDE" in veredicto and "BLOQUEADO" not in veredicto
            malos += not ok
            print(f"{x}: {info} · {veredicto}")
        finally:
            _sh(["git", "worktree", "remove", "--force", wt], RAIZ)
            shutil.rmtree(base, ignore_errors=True)
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
