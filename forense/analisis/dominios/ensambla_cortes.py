"""Une contratos cerrados en un corte parcial; no publica canon/mapa-dominios."""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "mapa-parcial-v0_1.tsv"
FILES = [
    "corte-enoe-v1_0.tsv",
    "corte-tecnologia-v1_0.tsv",
    "corte-tecnologia-adicional-v1_0.tsv",
    "corte-endireh-v1_0.tsv",
    "corte-politica-v1_0.tsv",
    "corte-confianza-v1_0.tsv",
    "corte-capital-social-v1_0.tsv",
    "corte-autoridad-v1_0.tsv",
    "corte-finanzas-v1_0.tsv",
    "corte-seguridad-v1_0.tsv",
    "corte-tiempo-v1_0.tsv",
    "corte-merito-v1_0.tsv",
    "corte-humor-v1_0.tsv",
]


def main() -> None:
    rows = []
    header = None
    for name in FILES:
        with (ROOT / name).open(encoding="utf-8", newline="") as stream:
            reader = csv.DictReader(stream, delimiter="\t")
            if header is None:
                header = reader.fieldnames
            elif reader.fieldnames != header:
                raise ValueError(f"Columnas incompatibles: {name}")
            rows.extend(reader)
    if any(row["estado_verificacion"] != "CERRADA" or not row["dictamen"] for row in rows):
        raise ValueError("Corte parcial contiene filas sin dictamen")
    ids = [row["id_afirmacion"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("IDs duplicados")
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, header, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: row["id_afirmacion"]))


if __name__ == "__main__":
    main()
