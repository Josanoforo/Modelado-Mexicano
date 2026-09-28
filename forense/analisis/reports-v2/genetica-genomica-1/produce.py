#!/usr/bin/env python3
"""Derive a joint claim table from editorial decisions; never infer judgments."""

import argparse
import csv
import hashlib
import io
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MAP = ROOT / "canon/mapa-dominios-v1_1.tsv"
PIECES = {
    "conducta": (
        "corpus/reports/Genetica_y_Conducta_del_Mexicano_Contemporaneo__Canal_Individual_vs__Estructura.md",
        "corpus/reports-v2/Genetica_y_Conducta_del_Mexicano_Contemporaneo__Canal_Individual_vs__Estructura.md",
    ),
    "genomica": (
        "corpus/reports/Mexican_Population_Genomics__2025-2026_Scientific_and_Market_Opportunity_Update.md",
        "corpus/reports-v2/Mexican_Population_Genomics__2025-2026_Scientific_and_Market_Opportunity_Update.md",
    ),
}
FIELDS = ("pieza", "id", "mapa_id", "dictamen", "razon", "razon_sin_cifra", "fuente", "fuente_url", "resultado", "trace")
VERDICTS = {"CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_map():
    with MAP.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def build():
    whole_map = read_map()
    table = []
    coverage = {}
    hashes = {str(MAP.relative_to(ROOT)): sha(MAP)}
    for piece, (original, report) in PIECES.items():
        decision_path = HERE / piece / "decisiones.json"
        decisions = json.loads(decision_path.read_text(encoding="utf-8"))
        if not isinstance(decisions, list):
            raise ValueError(f"{piece}: decisiones.json debe ser lista")
        expected = {r["id_afirmacion"] for r in whole_map if r["report"] == original}
        observed = [r.get("mapa_id", "") for r in decisions if r.get("mapa_id")]
        missing = sorted(expected - set(observed))
        extra = sorted(set(observed) - expected)
        duplicate = sorted(k for k, n in Counter(observed).items() if n != 1)
        if missing or extra or duplicate:
            raise ValueError(f"{piece}: mapa faltante={missing}, ajeno={extra}, duplicado={duplicate}")
        identifiers = [r.get("id", "") for r in decisions]
        if not all(identifiers) or len(set(identifiers)) != len(identifiers):
            raise ValueError(f"{piece}: id vacío o duplicado")
        rows = []
        for decision in decisions:
            row = {key: str(decision.get(key, "")).strip() for key in FIELDS if key != "pieza"}
            if row["dictamen"] not in VERDICTS:
                raise ValueError(f"{piece}/{row['id']}: dictamen inválido")
            if not row["razon"] or not row["fuente"] or not row["trace"]:
                raise ValueError(f"{piece}/{row['id']}: falta razón, fuente o traza")
            if row["dictamen"] == "SIN-CIFRA" and not row["razon_sin_cifra"]:
                raise ValueError(f"{piece}/{row['id']}: falta razón SIN-CIFRA")
            if row["resultado"] and not row["resultado"].startswith("RESULT-"):
                raise ValueError(f"{piece}/{row['id']}: resultado no es RESULT")
            row = {"pieza": piece, **row}
            rows.append(row)
        table.extend(rows)
        for name in (original, report):
            path = ROOT / name
            hashes[name] = sha(path)
        hashes[str(decision_path.relative_to(ROOT))] = sha(decision_path)
        coverage[piece] = {
            "original": original,
            "report": report,
            "mapa_filas": len(expected),
            "afirmaciones": len(rows),
            "afirmaciones_fuera_mapa": sum(not r["mapa_id"] for r in rows),
            "dictamenes": dict(sorted(Counter(r["dictamen"] for r in rows).items())),
            "mapa_ids": sorted(expected),
        }
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(table)
    return {
        HERE / "tabla-afirmaciones.tsv": out.getvalue(),
        HERE / "cobertura.json": json.dumps(coverage, ensure_ascii=False, indent=2) + "\n",
        HERE / "hashes-producto.json": json.dumps(dict(sorted(hashes.items())), ensure_ascii=False, indent=2) + "\n",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare generated files without writing")
    args = parser.parse_args()
    products = build()
    for path, content in products.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"DIFERENCIA: {path.relative_to(ROOT)}")
        else:
            path.write_text(content, encoding="utf-8")
    print("VERDE: tabla, cobertura y hashes actuales")


if __name__ == "__main__":
    main()
