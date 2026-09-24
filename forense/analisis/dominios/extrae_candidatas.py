"""Índice reproducible de pasajes candidatos; no asigna dictámenes ni tiers por inferencia."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_name("candidatas-v1_0.tsv")
SOURCES = sorted((ROOT / "corpus/reports").glob("*.md")) + sorted(
    (ROOT / "corpus/forense").glob("*.md")
)
LEAD = re.compile(r"^\s*(?:\d{1,2}[.)]\s+|[-*]\s+(?:\*\*|\[))")
TIER = re.compile(r"\[(?:EVIDENCIA\s+)?(FUERTE|MEDIA|MEDIO|MEDIA-FUERTE)\]|\bEVIDENCIA\s+(FUERTE|MEDIA)\b", re.I)


def classify(line: str) -> str:
    match = TIER.search(line)
    if not match:
        return "NO-EXPLÍCITO"
    return (match.group(1) or match.group(2)).upper()


def candidates(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    headings = [i for i, line in enumerate(lines) if line.startswith("## ")]
    first_boundary = headings[1] if len(headings) > 1 else min(len(lines), 90)
    seen = set()
    emitted = 0
    for i, line in enumerate(lines):
        if not line.strip() or line.lstrip().startswith(("|", ">")):
            continue
        if i < first_boundary and LEAD.match(line):
            pass
        elif TIER.search(line) and not line.lstrip().startswith("#"):
            pass
        else:
            continue
        raw = line.strip()
        # Líneas de metadatos o rúbricas de tier son índices, no afirmaciones.
        if len(raw) < 35 or raw.lower().startswith(("**tiers", "**evidencia", "- **evidencia")):
            continue
        key = re.sub(r"\W+", "", raw.lower())
        if key in seen:
            continue
        seen.add(key)
        emitted += 1
        yield (str(path.relative_to(ROOT)), digest, i + 1, classify(raw), raw)
    if not emitted:
        for i, line in enumerate(lines):
            raw = line.strip()
            if len(raw) >= 80 and not raw.startswith(("#", "|", ">", "---")):
                yield (str(path.relative_to(ROOT)), digest, i + 1, classify(raw), raw)
                break


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["ruta", "sha256_recalculado", "linea", "tier_literal_en_linea", "pasaje_candidato"])
        for path in SOURCES:
            writer.writerows(candidates(path))


if __name__ == "__main__":
    main()
