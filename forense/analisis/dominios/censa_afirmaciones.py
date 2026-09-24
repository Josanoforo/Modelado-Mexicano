"""Censo de lectura de hallazgos; no dicta medibilidad ni sustituye el mapa."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).with_name("afirmaciones-para-dictamen-v1_0.tsv")
SOURCES = sorted((ROOT / "corpus/reports").glob("*.md")) + sorted((ROOT / "corpus/forense").glob("*.md"))
SUMMARY = re.compile(r"resumen ejecutivo|hallazgos clave|key findings|executive summary", re.I)
NUMBER = re.compile(r"^\s*\d{1,2}[.)]\s")
TIER = re.compile(r"\[(?:EVIDENCIA\s+)?(FUERTE|MEDIA-FUERTE|MEDIA|MEDIO|SÓLID[OA]|HIPÓTESIS[^]]*|NARRATIVA[^]]*)[^]]*\]|EVIDENCIA\s+(FUERTE|MEDIA)(?:-MEDIA|-FUERTE)?", re.I)
SPECIAL_HEADINGS = {
    "La_arquitectura_invisible_de_la_interacción_social_en_México.md": (47, 180),
    "Psicología__Conducta_y_Sociedad_en_el_México_Contemporáneo__Análisis_Transcultural_y_Estructural.md": (7, 220),
    "Psicología_del_Trabajo_en_México__Un_Mapa_Basado_en_Evidencia.md": (21, 151),
}


def core_lines(path: Path, lines: list[str]) -> list[int]:
    if path.name in SPECIAL_HEADINGS:
        lo, hi = SPECIAL_HEADINGS[path.name]
        selected = [i for i in range(lo - 1, min(hi, len(lines))) if lines[i].startswith("### ")]
        if path.name.startswith("Psicología__Conducta_y_Sociedad"):
            selected = [i for i in selected if i + 1 != 35]  # híbrido honor retirado
            selected.append(44)  # lectura canónica L45 que lo sustituye
            selected.sort()
        return selected
    sections = []
    for i, line in enumerate(lines):
        if line.startswith("## ") and SUMMARY.search(line):
            end = next((j for j in range(i + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
            selected = [j for j in range(i + 1, end) if NUMBER.match(lines[j])]
            if not selected:
                selected = [j for j in range(i + 1, end) if lines[j].startswith(("- **", "* **", "**")) and len(lines[j]) >= 45]
            sections.append(selected)
    if sections:
        return max(sections, key=len)
    # Los forenses sin lista numerada usan viñetas del resumen inicial.
    end = next((i for i, line in enumerate(lines[4:], 4) if line.startswith("## ")), min(len(lines), 40))
    return [i for i in range(3, end) if lines[i].startswith(("- **", "* **")) and len(lines[i]) >= 45]


def tier_of(line: str) -> str:
    found = TIER.search(line)
    return ((found.group(1) or found.group(2)).upper() if found else "NO-EXPLÍCITO")


def main() -> None:
    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(["id_lectura", "ruta", "sha256_recalculado", "linea", "tier_literal", "texto_fuente", "estado_dictamen"])
        for path in SOURCES:
            lines = path.read_text(encoding="utf-8").splitlines()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            selected = core_lines(path, lines)
            if not selected:
                raise ValueError(f"Fuente sin hallazgo capturado: {path}")
            for n, i in enumerate(selected, 1):
                text = lines[i].strip()
                writer.writerow([f"LECTURA-{digest[:8]}-{n:02d}", str(path.relative_to(ROOT)), digest, i + 1, tier_of(text), text, "PENDIENTE-DE-DEDUP-Y-CONTRATO"])


if __name__ == "__main__":
    main()
