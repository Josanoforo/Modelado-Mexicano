#!/usr/bin/env python3
"""ACTO GEN2-VALIDACION-Y-2027-1 · P1 · archiva la salida de una reconstructora en el repo ANTES
de abrir ningún sellado (E.2). Verifica cada línea de salida/SELLO.txt contra los bytes; si una no
casa, PARA. Copia con el prefijo `<paq>--` (T02: sin nombres repetidos en el árbol) y aplana
subcarpetas con `--`; escribe `<paq>--mapa-nombres.tsv` (nombre original → archivado, sha256).

Uso: archiva.py <REC> <paq> [<paq> ...]
"""
import hashlib
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def archiva(REC, paq):
    base = REC / paq
    sal = base / "salida"
    fin = (REC / f"{paq}.fin").read_text()
    if "rc=0" not in fin:
        raise SystemExit(f"PARO · {paq} no terminó con rc=0: {fin!r}")
    sellados = {}
    for linea in (sal / "SELLO.txt").read_text().splitlines():
        if not linea.strip():
            continue
        h, nombre = linea.split(maxsplit=1)
        nombre = nombre.lstrip("*").removeprefix("salida/").removeprefix("./")
        if sha(sal / nombre) != h:
            raise SystemExit(f"PARO · {paq}: {nombre} no casa con SELLO.txt")
        sellados[nombre] = h
    dest = AQUI / paq / "reconstructora"
    if dest.exists():
        raise SystemExit(f"PARO · ya archivado {dest}")
    dest.mkdir(parents=True)
    filas = []
    for p in sorted(x for x in sal.rglob("*") if x.is_file() and "__pycache__" not in x.parts):
        rel = str(p.relative_to(sal))
        nuevo = f"{paq}--" + rel.replace("/", "--")
        shutil.copyfile(p, dest / nuevo)
        filas.append((rel, nuevo, sha(p), "SELLADO" if rel in sellados else "FUERA-DEL-SELLO"))
    for suf in ("transcript.jsonl",):  # inicio/fin/stderr van a lanzamientos.tsv (T02: contenidos repetidos)
        src = REC / f"{paq}.{suf}"
        if src.exists():
            nuevo = f"{paq}--transcript.jsonl" if suf == "transcript.jsonl" else f"{paq}--{suf}.txt"
            shutil.copyfile(src, dest / nuevo)
            filas.append((f"../{paq}.{suf}", nuevo, sha(src), "LANZADOR"))
    with open(dest / f"{paq}--mapa-nombres.tsv", "w", encoding="utf-8") as fh:
        fh.write("original\tarchivado\tsha256\testado\n")
        for f in filas:
            fh.write("\t".join(f) + "\n")
    faltan = set(sellados) - {f[0] for f in filas}
    if faltan:
        raise SystemExit(f"PARO · {paq}: sellados no archivados {faltan}")
    print(paq, len(sellados), "sellados ·", len(filas), "archivados")


if __name__ == "__main__":
    REC = Path(sys.argv[1])
    for paq in sys.argv[2:]:
        archiva(REC, paq)
