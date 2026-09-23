#!/usr/bin/env python3
"""Manifiesto de sellos GEN2 y su atestación externa (D-a1..D-a6, GEN2-TUBERIA-SELLO-EXTERNO-1).

`manifiesto`: censa cada sello.json (CALC) y cada sidecar .sha256 (SPEC) bajo
data/corrida0/ y forense/prereg-caja/, con su sha256, el commit que lo introdujo
y el commit de merge (PR) que lo trajo a origin/main. Determinista: dos
corridas sobre el mismo árbol dan el mismo archivo (mismo commit final, mismo
orden de glob).

`stamp`: delta de atestación — compara un manifiesto nuevo contra uno anterior
y solo procesa las filas de sello nuevas.
"""
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CALC_GLOB = "data/corrida0/CALC-*/sello.json"
SPEC_GLOB = "forense/prereg-caja/*.sha256"
PR_RE = re.compile(r"Merge pull request #(\d+)")


def _git(*args, cwd=None):
    r = subprocess.run(["git", *args], cwd=cwd or REPO_ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} -> {r.returncode}: {r.stderr.strip()}")
    return r.stdout.strip()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def first_parent_chain(base: str):
    """Commits de la cadena first-parent de `base`, de más viejo a más nuevo."""
    out = _git("rev-list", "--first-parent", "--reverse", base)
    return out.splitlines() if out else []


def merge_commit_for(add_commit: str, chain: list) -> str | None:
    """Primer commit de `chain` que contiene add_commit como ancestro (búsqueda binaria:
    la cadena first-parent es un orden total de contención)."""
    lo, hi = 0, len(chain)
    while lo < hi:
        mid = (lo + hi) // 2
        r = subprocess.run(
            ["git", "merge-base", "--is-ancestor", add_commit, chain[mid]],
            cwd=REPO_ROOT,
        )
        if r.returncode == 0:
            hi = mid
        else:
            lo = mid + 1
    return chain[lo] if lo < len(chain) else None


def commit_that_added(ruta: str) -> str | None:
    out = _git("log", "--diff-filter=A", "--format=%H", "-1", "--", ruta)
    return out or None


def firma_gpg(commit: str) -> tuple:
    """(%G?, %GK) del commit -- estado y key id de la firma GPG del merge,
    sin verificar contra una llave pública (P2-c, fallback sin red)."""
    out = _git("log", "-1", "--format=%G?%x09%GK", commit)
    estado, key = (out.split("\t") + [""])[:2]
    return estado or "N", key or "SIN-LLAVE"


def censa_filas(base_ref: str = "origin/main"):
    chain = first_parent_chain(base_ref)
    filas = []
    candidatos = []
    for p in sorted(REPO_ROOT.glob(CALC_GLOB)):
        rel = p.relative_to(REPO_ROOT).as_posix()
        candidatos.append(("CALC", p.parent.name, rel))
    for p in sorted(REPO_ROOT.glob(SPEC_GLOB)):
        rel = p.relative_to(REPO_ROOT).as_posix()
        candidatos.append(("SPEC", p.stem, rel))

    cache_firma = {}
    for tipo, id_, rel in candidatos:
        p = REPO_ROOT / rel
        sha = sha256_file(p)
        add_commit = commit_that_added(rel)
        if add_commit is None:
            fecha_commit = "NO-ACCESIBLE"
            pr = merged_at = gpg_estado = gpg_key = "NO-ACCESIBLE"
        else:
            fecha_commit = _git("log", "-1", "--format=%cI", add_commit)
            mc = merge_commit_for(add_commit, chain)
            if mc is None:
                pr = merged_at = gpg_estado = gpg_key = "NO-ACCESIBLE"
            else:
                subj = _git("log", "-1", "--format=%s", mc)
                m = PR_RE.search(subj)
                pr = m.group(1) if m else f"SIN-PR-EN-ASUNTO:{mc[:8]}"
                merged_at = _git("log", "-1", "--format=%cI", mc)
                if mc not in cache_firma:
                    cache_firma[mc] = firma_gpg(mc)
                gpg_estado, gpg_key = cache_firma[mc]
        filas.append(
            {
                "tipo": tipo,
                "id": id_,
                "ruta": rel,
                "sha256": sha,
                "commit": add_commit or "NO-ACCESIBLE",
                "fecha_commit": fecha_commit,
                "pr": pr,
                "merged_at": merged_at,
                "firma_gpg_estado": gpg_estado,
                "firma_gpg_keyid": gpg_key,
            }
        )
    return filas


def escribe_manifiesto(filas, destino: Path):
    cols = ["tipo", "id", "ruta", "sha256", "commit", "fecha_commit", "pr", "merged_at",
            "firma_gpg_estado", "firma_gpg_keyid"]
    lineas = ["\t".join(cols)]
    for f in filas:
        lineas.append("\t".join(f[c] for c in cols))
    cuerpo = "\n".join(lineas) + "\n"
    sha_manifiesto = hashlib.sha256(cuerpo.encode()).hexdigest()
    cuerpo += f"# sha256-manifiesto\t{sha_manifiesto}\n"
    destino.write_text(cuerpo)
    return sha_manifiesto


def cmd_manifiesto(args):
    filas = censa_filas()
    fecha = args.fecha
    destino = REPO_ROOT / "forense" / "sellos" / f"manifiesto-sellos-{fecha}.tsv"
    destino.parent.mkdir(parents=True, exist_ok=True)
    if args.escribe:
        sha = escribe_manifiesto(filas, destino)
        print(f"ESCRITO {destino} filas={len(filas)} sha256-manifiesto={sha}")
    else:
        for f in filas:
            print(f)
        print(f"TOTAL filas={len(filas)} (no escrito; usa --escribe)")


def lee_manifiesto(path: Path):
    filas = []
    for line in path.read_text().splitlines():
        if line.startswith("tipo\t") or line.startswith("# sha256-manifiesto"):
            continue
        p = line.split("\t")
        filas.append({"tipo": p[0], "id": p[1], "ruta": p[2], "sha256": p[3]})
    return filas


def cmd_stamp(args):
    nuevo = censa_filas()
    if args.desde:
        anteriores = {(f["tipo"], f["id"]) for f in lee_manifiesto(Path(args.desde))}
    else:
        anteriores = set()
    delta = [f for f in nuevo if (f["tipo"], f["id"]) not in anteriores]
    if not delta:
        print("SIN-DELTA: ningún sello nuevo desde el manifiesto anterior")
        return
    destino = REPO_ROOT / "forense" / "sellos" / f"manifiesto-sellos-{args.fecha}.tsv"
    destino.parent.mkdir(parents=True, exist_ok=True)
    sha = escribe_manifiesto(delta, destino)
    print(f"DELTA {destino} filas_nuevas={len(delta)} sha256-manifiesto={sha}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("manifiesto", help="Censa todos los sellos y escribe el TSV")
    m.add_argument("--escribe", action="store_true")
    m.add_argument("--fecha", default=None)
    m.set_defaults(func=cmd_manifiesto)

    s = sub.add_parser("stamp", help="Atestigua solo los sellos nuevos desde un manifiesto anterior")
    s.add_argument("--desde", required=True, help="ruta al manifiesto anterior")
    s.add_argument("--fecha", required=True)
    s.set_defaults(func=cmd_stamp)

    args = ap.parse_args()
    if getattr(args, "fecha", None) is None:
        args.fecha = _git("log", "-1", "--format=%cd", "--date=format:%Y-%m-%d")
    args.func(args)


if __name__ == "__main__":
    main()
