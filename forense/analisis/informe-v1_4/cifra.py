#!/usr/bin/env python3
"""Cifras del informe v1.4 (ACTO GEN2-CIERRE-SEMANAL-1), una por clave.

Solo lee artefactos del árbol; no escribe. Uso:
    python3 forense/analisis/informe-v1_4/cifra.py <clave>
Claves: cat:<clave de conteos.json del catálogo v1.2> · censo:<clase> ·
cat_origen:<origen_piso> · mapa11:<prefijo de estado_corpus_v1_1> ·
mapa11_dictamen:<dictamen> · familias2027 · legacy_24sep
"""
import csv
import glob
import json
import pathlib
import re
import sys

csv.field_size_limit(sys.maxsize)
ROOT = pathlib.Path(__file__).resolve().parents[3]


def lee(p):
    with open(ROOT / p, newline="", encoding="utf-8") as s:
        return list(csv.DictReader((l for l in s if not l.startswith("#")), delimiter="\t"))


def main(clave: str) -> int:
    tipo, _, arg = clave.partition(":")
    if tipo == "cat":
        v = json.loads((ROOT / "forense/analisis/catalogo/v1_2/conteos-v1_2.json").read_text())[arg]
    elif tipo == "censo":
        v = sum(r["clase_censo"] == arg for r in lee("forense/notas/2026-09-24-GEN2-ENCIG-PISOS-GEN2-1-censo.tsv"))
    elif tipo == "cat_origen":
        v = sum(r["origen_piso"] == arg for r in lee("canon/catalogo-del-mexicano-v1_2.tsv"))
    elif tipo == "mapa11":
        v = sum(r["estado_corpus_v1_1"].startswith(arg) for r in lee("canon/mapa-dominios-v1_1.tsv"))
    elif tipo == "mapa11_dictamen":
        v = sum(r["dictamen"] == arg for r in lee("canon/mapa-dominios-v1_1.tsv"))
    elif tipo == "familias2027":
        v = len({re.sub(r"-spec-v1_.*", "", p) for p in glob.glob(str(ROOT / "forense/prereg-caja/FAMILIA-2027-*-spec-v1_*.md"))})
    elif tipo == "legacy_24sep":
        t = (ROOT / "forense/notas/2026-09-24-GEN2-ADOPCION-BLOQUE-Y-PINES-2-cierre.md").read_text()
        v = int(re.search(r"\| `dependencias_numericas_legacy_activas` \| (\d+) \|", t).group(1))
    else:
        raise SystemExit(f"clave desconocida: {clave}")
    print(v)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
