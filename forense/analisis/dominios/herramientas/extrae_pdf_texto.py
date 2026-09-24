#!/usr/bin/env python3
"""Llena la caché de texto por página que usa u0pdf.py: pdftotext -layout de cada PDF registrado
en data/manifiesto.yaml (raíz data_raw por defecto; --raiz descargas_mx exige la ruta real en
data/raices.local.yaml y, en esta caja, correr fuera del sandbox). Omite olas reservadas
(ENOE 2026, ENVIPE 2026, ENCO) y todo id con estado_reserva. Caché: $U0_CACHE/pdftxt/<id>.txt."""
import os, re, subprocess, sys, yaml
from pathlib import Path
REPO = Path(__file__).resolve().parents[4]
CACHE = Path(os.environ.get("U0_CACHE", os.path.join(os.environ.get("TMPDIR", "/tmp"), "u0-cache"))) / "pdftxt"
RES = re.compile(r"enoe_?2026|envipe_?2026|(^|[_/])enco[_0-9/]", re.I)
raiz = sys.argv[sys.argv.index("--raiz") + 1] if "--raiz" in sys.argv else "data_raw"
base = REPO / "data/raw" if raiz == "data_raw" else Path(yaml.safe_load(open(REPO / "data/raices.local.yaml"))[raiz])
CACHE.mkdir(parents=True, exist_ok=True)
n = ok = 0
for e in yaml.safe_load(open(REPO / "data/manifiesto.yaml", encoding="utf-8")):
    a = e.get("archivo") or ""
    if not a.lower().endswith(".pdf") or e.get("raiz", "data_raw") != raiz: continue
    if e.get("estado_reserva") or RES.search(e["id"]) or RES.search(a): continue
    n += 1
    p = base / a
    if p.exists() and subprocess.run(["pdftotext", "-layout", str(p), str(CACHE / f"{e['id']}.txt")]).returncode == 0:
        ok += 1
print(f"{ok} de {n} PDF de la raíz {raiz} extraídos a {CACHE}")
