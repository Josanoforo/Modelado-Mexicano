#!/usr/bin/env python3
"""Ensambla tres productores propios; juicios editoriales nunca inferidos por código."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PIECES = ("dinero", "tecnologia", "conocimiento")

def assemble():
    summaries = {piece: json.loads((HERE / piece / "resumen.json").read_text()) for piece in PIECES}
    lines = ["# Índice local · dinero, tecnología y conocimiento", "", "Conteos derivados de decisiones editoriales explícitas. Registros de cobertura y filas del mapa pueden solaparse; no son tesis independientes ni muestras.", "", "| Pieza | Registros | Filas mapa | CONFIRMA | MATIZA | ROMPE | SIN-CIFRA | Cifras |", "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for piece, s in summaries.items():
        d = s["dictamenes"]
        n = s["afirmaciones"]
        n = n["registros"] if isinstance(n,dict) else n
        lines.append(f"| {piece} | {n} | {s['mapa_filas']} | {d.get('CONFIRMA',0)} | {d.get('MATIZA',0)} | {d.get('ROMPE',0)} | {d.get('SIN-CIFRA',0)} | {s['cifras']} |")
    lines += ["", "## Productos", ""]
    for piece,s in summaries.items():
        lines += [f"- [{piece}](/" + s["report"] + f"): decisiones, fuentes y verificaciones en `{piece}/`; reglas PROPUESTO-POR-EJECUTOR, sin adopción."]
    lines += ["", "Recibo independiente solicitado en el PR; no acreditado por el autor. C1 no bloquea este lote y sus hallazgos materiales deberán corregir únicamente las conclusiones afectadas.", ""]
    # Links relative to the repository root, not nonexistent filesystem root.
    paths = set()
    for piece, summary in summaries.items():
        paths.add(ROOT / summary["report"])
        paths.update(p for p in (HERE / piece).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    return {HERE / "hashes-producto.json": json.dumps(hashes, ensure_ascii=False, indent=2)+"\n", HERE / "indice-local.md": "\n".join(lines).replace("](/corpus/", "](../../../../corpus/"), HERE / "resumen-lote.json": json.dumps(summaries, ensure_ascii=False, indent=2)+"\n"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args=ap.parse_args()
    for piece in PIECES:
        s=json.loads((HERE/piece/"resumen.json").read_text())
        command=s["comando_verificar"] if args.check else s["comando_generar"]
        if args.self_test:
            command=s.get("comando_self_test",s["comando_verificar"]+["--self-test"])
        subprocess.run(command,cwd=ROOT,check=True)
    for path, content in assemble().items():
        if args.check or args.self_test:
            if not path.exists() or path.read_text()!=content:
                raise SystemExit(f"DIFERENCIA: {path.relative_to(ROOT)}")
        else:
            path.write_text(content)
    print("VERDE: tres piezas e índice local sin diferencias" if args.check else "VERDE: lote producido/verificado")

if __name__=="__main__": main()
