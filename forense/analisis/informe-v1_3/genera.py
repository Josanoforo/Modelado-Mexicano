#!/usr/bin/env python3
"""Extrae comparaciones primarias de RESULT sellados, sin abrir microdatos."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / "data/corrida0"
OUT = Path(__file__).with_name("comparaciones-primarias.tsv")

# Cada prefijo nombra una comparación preexistente; las llaves se resuelven
# contra resultados.json, nunca se transcriben números a esta fuente.
ROWS = [
    ("ENIF 2024 · lote", "CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001", "RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-R2-DELTA-MAE-PP", "RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-R2-DELTA-IC95INF", "RESULT-DIN-LOTE24-ADJ-G-PRIMARIO-R2-DELTA-IC95SUP", "persona", "PROSPECTIVA"),
    ("ENCIG 2025 · piloto 3", "CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001", "RESULT-GOB-EXE15-ADJ-2025-S-LAMBDA-DELTA-MAE-PP", "RESULT-GOB-EXE15-ADJ-2025-S-LAMBDA-DELTA-MAE-IC-LO", "RESULT-GOB-EXE15-ADJ-2025-S-LAMBDA-DELTA-MAE-IC-HI", "trámite", "PROSPECTIVA"),
    ("ENVIPE 2026 · SXD", "CALC-DUELO-ENVIPE2026-ADJUDICACION-0001", "RESULT-DUELO26-ADJ-SXD-SL-DELTA-MAE-PP", "RESULT-DUELO26-ADJ-SXD-SL-DELTA-IC95INF", "RESULT-DUELO26-ADJ-SXD-SL-DELTA-IC95SUP", "delito", "PROSPECTIVA"),
    ("ENVIPE 2026 · EXD", "CALC-DUELO-ENVIPE2026-ADJUDICACION-0001", "RESULT-DUELO26-ADJ-EXD-SL-DELTA-MAE-PP", "RESULT-DUELO26-ADJ-EXD-SL-DELTA-IC95INF", "RESULT-DUELO26-ADJ-EXD-SL-DELTA-IC95SUP", "delito", "PROSPECTIVA"),
    ("ENVIPE 2025 · piloto 4 dominio×sexo", "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001", "RESULT-TRA-ENCOGIDA-ARB-DOMxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-PP", "RESULT-TRA-ENCOGIDA-ARB-DOMxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-IC-LO", "RESULT-TRA-ENCOGIDA-ARB-DOMxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-IC-HI", "delito", "PROSPECTIVA"),
    ("ENVIPE 2025 · piloto 4 edad×escolaridad", "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001", "RESULT-TRA-ENCOGIDA-ARB-EDADxESC-G-DELTA-MAE-C-ENCOGIDA-VS-C2-PP", "RESULT-TRA-ENCOGIDA-ARB-EDADxESC-G-DELTA-MAE-C-ENCOGIDA-VS-C2-IC-LO", "RESULT-TRA-ENCOGIDA-ARB-EDADxESC-G-DELTA-MAE-C-ENCOGIDA-VS-C2-IC-HI", "delito", "PROSPECTIVA"),
    ("ENVIPE 2025 · piloto 4 edad×sexo", "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001", "RESULT-TRA-ENCOGIDA-ARB-EDADxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-PP", "RESULT-TRA-ENCOGIDA-ARB-EDADxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-IC-LO", "RESULT-TRA-ENCOGIDA-ARB-EDADxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-IC-HI", "delito", "PROSPECTIVA"),
    ("ENVIPE 2025 · piloto 4 escolaridad×sexo", "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001", "RESULT-TRA-ENCOGIDA-ARB-ESCxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-PP", "RESULT-TRA-ENCOGIDA-ARB-ESCxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-IC-LO", "RESULT-TRA-ENCOGIDA-ARB-ESCxSEX-G-DELTA-MAE-C-ENCOGIDA-VS-C2-IC-HI", "delito", "PROSPECTIVA"),
    ("ENCIG 2025 · cierre edad×sexo C-ASTRA", "CALC-ENCIG-DUELO-2025-ADJUDICACION-0001", "RESULT-ENCIG-DUELO-2025-ADJ-EDADXSEXO-G-C-ASTRA-DELTA-MAE-PP", "RESULT-ENCIG-DUELO-2025-ADJ-EDADXSEXO-G-C-ASTRA-DELTA-MAE-IC-LO", "RESULT-ENCIG-DUELO-2025-ADJ-EDADXSEXO-G-C-ASTRA-DELTA-MAE-IC-HI", "trámite", "PROSPECTIVA"),
    ("ENCIG 2025 · cierre escolaridad×sexo C-ASTRA", "CALC-ENCIG-DUELO-2025-ADJUDICACION-0001", "RESULT-ENCIG-DUELO-2025-ADJ-ESCOLARIDADXSEXO-G-C-ASTRA-DELTA-MAE-PP", "RESULT-ENCIG-DUELO-2025-ADJ-ESCOLARIDADXSEXO-G-C-ASTRA-DELTA-MAE-IC-LO", "RESULT-ENCIG-DUELO-2025-ADJ-ESCOLARIDADXSEXO-G-C-ASTRA-DELTA-MAE-IC-HI", "trámite", "PROSPECTIVA"),
]


def main() -> None:
    cache = {}
    rows = []
    for label, calc, key, lo, hi, unit, temporal in ROWS:
        folder = BASE / calc
        if calc not in cache:
            seal_line = (folder / "sello.sha256").read_text().split()
            assert seal_line[1] == "sello.json"
            actual = hashlib.sha256((folder / "sello.json").read_bytes()).hexdigest()
            assert actual == seal_line[0], calc
            cache[calc] = (json.loads((folder / "resultados.json").read_text())["resultados"], actual)
        values, seal_hash = cache[calc]
        assert isinstance(values[key], (int, float))
        assert isinstance(values[lo], (int, float))
        assert isinstance(values[hi], (int, float))
        rows.append(dict(evaluacion=label, calc=calc, result_delta=key,
                         delta_mae_pp=values[key], result_ic_lo=lo, ic_lo_pp=values[lo],
                         result_ic_hi=hi, ic_hi_pp=values[hi], unidad=unit,
                         temporalidad=temporal, sello_sha256=seal_hash))
    with OUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"comparaciones={len(rows)} calcs={len(cache)}")


if __name__ == "__main__":
    main()
