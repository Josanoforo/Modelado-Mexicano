#!/usr/bin/env python3
"""Genera docs/one-pager.pdf desde docs/one-pager.md.

Fuente única: el PDF no repite texto a mano, renderiza el mismo Markdown
que Pages serviría como HTML. Quita el front matter Jekyll y resuelve los
tags Liquid `{{ '/x' | relative_url }}` a rutas planas para el render
standalone (fuera de Jekyll no hay motor Liquid).

Requiere `markdown` y `weasyprint` (`pip install --break-system-packages
markdown weasyprint`); si no están instalados, el comando falla en voz alta
en vez de producir un PDF a medias.

Uso: python3 tools/genera_pdf_one_pager.py
"""
from __future__ import annotations

import pathlib
import re

import markdown
from weasyprint import HTML

ROOT = pathlib.Path(__file__).resolve().parents[1]
FUENTE = ROOT / "docs/one-pager.md"
SALIDA = ROOT / "docs/one-pager.pdf"

CSS = """
@page { size: Letter; margin: 2cm; }
body { font-family: Georgia, "Times New Roman", serif; color: #1a1a1a; line-height: 1.4; font-size: 10.5pt; }
h1 { font-size: 20pt; border-bottom: 2px solid #1a1a1a; padding-bottom: 6px; }
h2 { font-size: 13pt; margin-top: 1.4em; color: #2a2a2a; }
table { border-collapse: collapse; width: 100%; margin: 0.6em 0; font-size: 9.5pt; }
th, td { border: 1px solid #999; padding: 4px 6px; text-align: left; }
th { background: #eee; }
code { background: #f0f0f0; padding: 0 3px; font-size: 0.92em; }
a { color: #06c; text-decoration: none; }
p, li { orphans: 3; widows: 3; }
"""


def quita_front_matter(texto: str) -> str:
    if texto.startswith("---\n"):
        fin = texto.index("\n---\n", 4)
        return texto[fin + 5:]
    return texto


def resuelve_liquid(texto: str) -> str:
    def reemplaza(m: re.Match) -> str:
        ruta = m.group(1)
        if ruta in ("/", ""):
            return "index.html"
        return ruta.lstrip("/") + ".html"

    return re.sub(r"\{\{\s*'([^']*)'\s*\|\s*relative_url\s*\}\}", reemplaza, texto)


def main() -> None:
    texto = FUENTE.read_text(encoding="utf-8")
    texto = quita_front_matter(texto)
    texto = resuelve_liquid(texto)
    cuerpo_html = markdown.markdown(texto, extensions=["tables", "extra"])
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{cuerpo_html}</body></html>"
    HTML(string=html, base_url=str(ROOT / "docs")).write_pdf(str(SALIDA))
    print(f"escrito: {SALIDA.relative_to(ROOT)} ({SALIDA.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
