#!/usr/bin/env python3
"""Deriva la tabla viva de juicios explícitos; no asigna dictámenes."""
import argparse
import csv
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
LIVE = BASE.parents[1] / "consumo-familia-1/familia"


def generate(check=False):
    claims = json.loads((BASE / "familia-juicios.json").read_text())["juicios"]
    assert len({r["id"] for r in claims}) == len(claims)
    with (ROOT / "canon/mapa-dominios-v1_1.tsv").open() as f:
        mapa = list(csv.DictReader(f, delimiter="\t"))
    report = json.loads((LIVE / "familia-lectura-y-corte.json").read_text())["report"]
    expected = {r["id_afirmacion"] for r in mapa if r["report"] == report}
    assert expected == {r["mapa_id"] for r in claims if r["mapa_id"]}, "cobertura del mapa"
    for row in claims:
        assert row["razon"] and row["revision_sustantiva"] and row["componentes"]
        assert row["dictamen"] in {"CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"}
    products = {
        LIVE / "familia-afirmaciones.json": json.dumps(claims, ensure_ascii=False, indent=2) + "\n",
        BASE / "familia-resumen.json": json.dumps({
            "registros_cobertura": len(claims), "afirmaciones_mapa": len(expected),
            "dictamenes_registros": dict(sorted(Counter(r["dictamen"] for r in claims).items())),
            "nota": "Registros superpuestos: no son tesis únicas; juicios son la fuente humana explícita.",
        }, ensure_ascii=False, indent=2) + "\n",
    }
    for path, body in products.items():
        if check:
            assert path.read_text() == body, str(path) + " no reproduce"
        else:
            path.write_text(body)
    print("REPRODUCE" if check else "GENERADO", len(claims), "registros; juicios sin reglas automáticas")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    generate(parser.parse_args().check)
