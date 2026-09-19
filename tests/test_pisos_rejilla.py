#!/usr/bin/env python3
"""Falsadores de la rejilla de pisos; no abre microdatos."""
from __future__ import annotations
import csv
import importlib.util
from pathlib import Path
import pandas as pd
import yaml

ROOT=Path(__file__).resolve().parents[1]
SNAP=ROOT/"forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv"
CALCS=[
 "CALC-PISOS-ENVIPE2024-EJES-0002",
 "CALC-PISOS-ENCIG2023-EJES-0002",
 "CALC-PISOS-ENIF2021-EJES-0003",
]

def corre():
    errors=[]
    with SNAP.open(encoding="utf-8",newline="") as fh:
        rows=list(csv.DictReader(fh,delimiter="\t"))
    if len(rows)!=57: errors.append(f"rejilla: {len(rows)} filas, esperaba 57")
    keys=[r["cell_id"] for r in rows]
    if len(keys)!=len(set(keys)): errors.append("rejilla: cell_id duplicado")
    if any(not r["category"] or r["category"].lower()=="nan" for r in rows):
        errors.append("rejilla: categoría vacía/nan")
    status={r["status"] for r in rows}
    if status!={"CONSTRUIBLE","NO-CONSTRUIBLE"}:
        errors.append(f"rejilla: estados inesperados {status}")
    constructible={r["cell_id"] for r in rows if r["status"]=="CONSTRUIBLE"}
    excluded=[r for r in rows if r["status"]=="NO-CONSTRUIBLE"]
    if len(constructible)!=53 or len(excluded)!=4:
        errors.append(f"rejilla: construibles={len(constructible)}, excluidas={len(excluded)}")
    declared=set()
    for calc in CALCS:
        directory=ROOT/"data/corrida0"/calc
        spec=yaml.safe_load((directory/"spec.yaml").read_text(encoding="utf-8"))
        result_ids=[r["id"] for r in spec["resultados"]]
        if len(result_ids)!=len(set(result_ids)):
            errors.append(f"{calc}: RESULT duplicado")
        declared.update(x for x in result_ids if x.endswith("-P"))
        source=(directory/"medidor.py").read_text(encoding="utf-8")
        if "tools.pisos_ejes" in source or "pisos_ejes_v2" in source:
            errors.append(f"{calc}: importa helper mutable")
        if "def _estimate" not in source or "PCG64" not in source:
            errors.append(f"{calc}: medidor no autocontenido")
        if spec.get("sucesor_de") is None:
            errors.append(f"{calc}: falta sucesor_de")
        if spec["etiquetas"].get("cuenta_gen2")!="PENDIENTE-DE-MESA":
            errors.append(f"{calc}: adjudica cuenta_gen2")
    if declared!=constructible:
        errors.append("rejilla/spec: faltan="+str(sorted(constructible-declared))+
                      " sobran="+str(sorted(declared-constructible)))
    if any("P3_13" not in r["reason"] for r in excluded):
        errors.append("exclusión de formalidad sin razón P3_13")
    enif=ROOT/"data/corrida0/CALC-PISOS-ENIF2021-EJES-0003/medidor.py"
    module_spec=importlib.util.spec_from_file_location("pisos_enif_v21",enif)
    module=importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    fixture=pd.DataFrame({
        "P5_4_1":["1","2"], "P5_4_2":["2","2"],
        "P5_7_1":["2",""], "P5_7_2":["",""],
    })
    formal=module._formal(
        fixture, ["P5_4_1","P5_4_2"], ["P5_7_1","P5_7_2"])
    if formal.tolist()!=[False,False]:
        errors.append(f"ENIF: pares posicionales P5_4/P5_7 rotos: {formal.tolist()}")
    return errors

def main():
    errors=corre()
    print(f"tests/test_pisos_rejilla.py · {len(errors)} fallos")
    for error in errors: print("  FAIL "+error)
    return 1 if errors else 0

if __name__=="__main__":
    raise SystemExit(main())
