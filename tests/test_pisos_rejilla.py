#!/usr/bin/env python3
"""Falsadores de la rejilla de pisos; no abre microdatos."""
from __future__ import annotations
import ast
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import tarfile
import yaml

ROOT=Path(__file__).resolve().parents[1]
SNAP=ROOT/"forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv"
DELIVERY=ROOT/"forense/pisos-rejilla-entrega.tsv"
CATALOGS=ROOT/"forense/prereg-caja/PISOS-REJILLA-escolaridad-catalogos-v1_0.tsv"
ARCHIVE=ROOT/"forense/historico/PR-868-2d662e78/artefactos-pisos.tar.gz"
CALCS=[
 "CALC-PISOS-ENVIPE2024-EJES-0002",
 "CALC-PISOS-ENCIG2023-EJES-0002",
 "CALC-PISOS-ENIF2021-EJES-0003",
]

def _formal_posicional_en_fuente(source: str) -> bool:
    """Falsador stdlib para la reparación ENIF; CI no instala pandas.

    La prueba funcional se conserva cuando pandas está disponible. Esta
    inspección de AST garantiza además que un runner mínimo siga verificando
    el defecto exacto: la negación combina P5_4/P5_7 por posición antes de
    reducir la fila, en vez de alinear etiquetas de columnas distintas.
    """
    tree=ast.parse(source)
    function=next((node for node in tree.body
                   if isinstance(node,ast.FunctionDef) and node.name=="_formal"),None)
    if function is None:
        return False
    normalized="".join(ast.unparse(function).split())
    required=(
        "no=(a.eq('2').to_numpy()|s.eq('2').to_numpy()).all(axis=1)",
        "out.loc[no&~yes]=False",
        "out.loc[yes]=True",
    )
    return all(fragment in normalized for fragment in required)

def corre():
    errors=[]
    with SNAP.open(encoding="utf-8",newline="") as fh:
        rows=list(csv.DictReader(fh,delimiter="\t"))
    with DELIVERY.open(encoding="utf-8",newline="") as fh:
        delivered=list(csv.DictReader(fh,delimiter="\t"))
    if len(rows)!=57: errors.append(f"rejilla: {len(rows)} filas, esperaba 57")
    identity=("cell_id","input_id","outcome","source_instrument","source_edition",
              "source_reference_period","target_instrument","target_edition",
              "target_reference_period","unit","axis","category","status","reason",
              "consumer","metadata_source","metadata_source_sha256")
    frozen_identities={tuple(r[k] for k in identity) for r in rows}
    delivered_identities={tuple(r[k] for k in identity) for r in delivered}
    if frozen_identities!=delivered_identities:
        errors.append("rejilla/entrega: identidad completa (incluidos desenlace y unidad) difiere")
    if len(delivered)!=len(delivered_identities):
        errors.append("entrega: identidad completa duplicada")
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
        seal=json.loads((directory/"sello.json").read_text(encoding="utf-8"))
        digest=hashlib.sha256((directory/"medidor.py").read_bytes()).hexdigest()
        if seal.get("medidor.py")!=digest:
            errors.append(f"{calc}: el sello no cubre el medidor autocontenido")
    if declared!=constructible:
        errors.append("rejilla/spec: faltan="+str(sorted(constructible-declared))+
                      " sobran="+str(sorted(declared-constructible)))
    if any("P3_13" not in r["reason"] for r in excluded):
        errors.append("exclusión de formalidad sin razón P3_13")
    for row in delivered:
        numeric=(row["point"],row["ic_lo"],row["ic_hi"],row["n"],row["den_w"],row["b_validas"])
        if row["status"]=="CONSTRUIBLE" and (not all(numeric) or not row["calc_id"]):
            errors.append(f"{row['cell_id']}: RESULT numérico incompleto")
        if row["status"]=="NO-CONSTRUIBLE" and (any(numeric) or row["calc_id"]):
            errors.append(f"{row['cell_id']}: dictamen mezclado con resultados")
    with (ROOT/"data/corrida0/usos.tsv").open(encoding="utf-8",newline="") as fh:
        usage=list(csv.DictReader((line for line in fh if not line.startswith("#")),delimiter="\t"))
    floor_ids={r["cell_id"] for r in delivered if r["status"]=="CONSTRUIBLE"}
    if any(r["resultado_id"] in floor_ids for r in usage):
        errors.append("usos: un piso nuevo tiene consumo productivo antes de adopción")
    with CATALOGS.open(encoding="utf-8",newline="") as fh:
        catalogs=list(csv.DictReader(fh,delimiter="\t"))
    expected={"ENVIPE":("NIV",10),"ENCIG":("NIV",10),"ENIF":("P3_1_1",10)}
    for instrument,(variable,count) in expected.items():
        subset=[r for r in catalogs if r["instrumento"]==instrument]
        if len(subset)!=count or {r["variable"] for r in subset}!={variable}:
            errors.append(f"catálogo escolaridad {instrument}: variable/códigos incompletos")
        if {r["categoria_piso"] for r in subset}!={"hasta_primaria","secundaria","media_superior","superior"}:
            errors.append(f"catálogo escolaridad {instrument}: categorías incompletas")
    if hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()!="5640cb318c2f5b6d542a2796e2ab1914d80b984a43e2fdce39029827b1009c92":
        errors.append("archivo histórico PR #868: hash incorrecto")
    with tarfile.open(ARCHIVE,"r:gz") as archive:
        archived=set(archive.getnames())
    for calc in ("ENVIPE2024","ENCIG2023","ENIF2021"):
        prefix=f"PR-868-2d662e78/data/corrida0/CALC-PISOS-{calc}-EJES-0002/"
        if not all(prefix+name in archived for name in ("spec.yaml","medidor.py","ejecucion.json","resultados.json","sello.json","sello.sha256")):
            errors.append(f"archivo histórico PR #868: {calc} incompleto")
    enif=ROOT/"data/corrida0/CALC-PISOS-ENIF2021-EJES-0003/medidor.py"
    enif_source=enif.read_text(encoding="utf-8")
    if not _formal_posicional_en_fuente(enif_source):
        errors.append("ENIF: la negación formal no combina P5_4/P5_7 por posición")
    try:
        import pandas as pd
    except ImportError:
        pd=None
    if pd is not None:
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
