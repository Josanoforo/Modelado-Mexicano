#!/usr/bin/env python3
"""Audita el CALC de cada comparación y sus inputs RESULT sellados, sin leer R."""
import csv
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "data/corrida0"
DEST = Path(__file__).resolve().parent / "auditoria-sellados.tsv"
MAIN = [
    "CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001",
    "CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001",
    "CALC-ENIGH-DUELO-ADJUDICACION-0001",
    "CALC-DUELO-ENVIPE2026-ADJUDICACION-0001",
    "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001",
    "CALC-ENCIG-DUELO-2025-ADJUDICACION-0001",
    "CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002",
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


paths = {BASE / name for name in MAIN}
for name in MAIN:
    spec = yaml.safe_load((BASE / name / "spec.yaml").read_text())
    paths.update(ROOT / i["ruta"].split("/resultados.json")[0]
                 for i in spec.get("inputs", [])
                 if i.get("ruta", "").startswith("data/corrida0/")
                 and i["ruta"].endswith("/resultados.json"))

rows = []
for folder in sorted(paths):
    assert folder.exists(), folder
    manifest = json.loads((folder / "sello.json").read_text())
    assert all(sha(folder / name) == digest for name, digest in manifest.items()), folder
    expected = (folder / "sello.sha256").read_text().split()[0]
    assert sha(folder / "sello.json") == expected, folder
    result = json.loads((folder / "resultados.json").read_text())["resultados"]
    vectors = [(k, len(v)) for k, v in result.items() if isinstance(v, (list, dict))]
    # Tablas JSON en texto se inspeccionan aparte; no son réplicas de Δ.
    long_text = [(k, len(v)) for k, v in result.items()
                 if isinstance(v, str) and len(v) > 1000]
    files = sorted(x.name for x in folder.iterdir() if x.is_file())
    rows.append(dict(calc=folder.name, papel="COMPARACION" if folder.name in MAIN else "INPUT-SELLADO",
                     archivos=";".join(files), sello_sha256=expected,
                     result_n=len(result), ee_n=sum(k.endswith("-EE") for k in result),
                     replicas_validas_n=sum("B-VALIDAS" in k for k in result),
                     vectores_json=len(vectors), textos_largos=";".join(k for k, _ in long_text),
                     vector_delta_pareado="NO-ARCHIVADO"))

assert len(rows) == 23 and not any(int(x["vectores_json"]) for x in rows)
with DEST.open("w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
print(f"sellos=COINCIDE/{len(rows)}; vectores_delta=0; comparaciones={len(MAIN)}")
