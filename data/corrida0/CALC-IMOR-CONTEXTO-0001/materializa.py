#!/usr/bin/env python3
"""Materializa tablas y SVG con identificadores gráficos deterministas."""
from pathlib import Path

import matplotlib

matplotlib.rcParams["svg.hashsalt"] = "CALC-IMOR-CONTEXTO-0001"

from medidor import materializar  # noqa: E402


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[3]
    materializar(root)
    for svg in (root / "data/analisis-imor-contexto-temporal").glob("*.svg"):
        clean = "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n"
        svg.write_text(clean, encoding="utf-8")
