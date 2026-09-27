#!/usr/bin/env python3
"""Ensambla delta por identidad; no materializa datos ni ejecuta validadores."""
import csv, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
def read(path):
    return list(csv.DictReader(path.open(), delimiter="\t"))
def rel(path):
    return str(path.relative_to(REPO))
def main():
    base = read(REPO / "forense/validacion-independiente/catalogo-1-preparacion-lote2/astra6-c1-lote2-entrega-59.tsv")
    one = {r["identidad_historica"]:r for r in read(ROOT / "p1/impedimentos-lote2-p1-delta-identidades.tsv")}
    two = {r["paquete_original"]:r for r in read(ROOT / "p2/impedimentos-lote2-p2-p4-delta-identidades.tsv")}
    three = {r["paquete_original"]:r for r in read(ROOT / "p3/impedimentos-lote2-p3-delta-acceso.tsv")}
    fields = ["paquete_original","estimadores","estado_1185","estado_preparacion_actual","avance_ejecutado","artefactos","impedimento_restante","decision_exacta","estado_validacion"]
    rows = []
    for old in base:
        if old["estado_preparacion"] != "NO-PREPARADO":
            continue
        key = old["paquete_original"]
        assert key in one or key in two or key in three, key
        actions, files, blockers, choices, states = [], [], [], [], []
        if key in one:
            r = one[key]
            assert r["estimadores"] == old["estimadores"]
            actions.append("P1: contrato por identidad redactado; fuentes humanas, disponibilidad y documentos verificados en informes; " + r["estado_preparacion"])
            files.extend([ROOT / "p1" / r["contrato"], ROOT / "p1/impedimentos-lote2-p1-delta-identidades.tsv"])
            blockers.append("P1: " + r["restante_material"])
            choices.append("P1: " + r["delta_desde_1185"])
            states.append(r["estado_preparacion"])
            if key == "b-0001":
                actions.append("EJECUTADO: un punto aislado materializado fuera del clon; sin recálculo ni ensayo B integral")
                files.append(ROOT / "p1/impedimentos-lote2-p1-b-materializacion-recibo.json")
        if key in two:
            r = two[key]
            assert r["estimadores"] == old["estimadores"]
            actions.append("P2/P4: " + r["delta_ejecutado"])
            blockers.append("P2/P4: " + r["impedimentos_secundarios"])
            choices.append("P2/P4: " + r["decision_exacta"])
            states.append(r["estado_actual"])
            files.append(ROOT / "p2/impedimentos-lote2-p2-p4-delta-identidades.tsv")
            if old["dictamen_preparatorio"] == "TOLERANCIA-NUEVA-PENDIENTE-DE-ADOPCION":
                files.extend([ROOT / "p4" / key / ("impedimentos-lote2-p4-"+key+"-contrato.json"), ROOT / "p4/impedimentos-lote2-p4-documentos-resueltos.json"])
            else:
                files.append(ROOT / "p2/impedimentos-lote2-p2-dictamen-y-hoja-firma.md")
        if key in three:
            r = three[key]
            actions.append("P3: " + r["avance_ejecutado"])
            blockers.append("P3: " + r["impedimento_restante"])
            choices.append("P3: " + r["decision_exacta"])
            states.append("APERTURA-REAL-NO-AUTORIZADA;CONTRATO-HERRAMIENTAS-TERMINADOS")
            files.extend([ROOT / "p3/impedimentos-lote2-p3-contratos.json", ROOT / "p3/impedimentos-lote2-p3-hoja-firma.md"])
        for f in files:
            assert f.is_file(), f
        rows.append(dict(zip(fields,[key,old["estimadores"],old["dictamen_preparatorio"]," | ".join(states)," | ".join(actions)," | ".join(dict.fromkeys(rel(f) for f in files))," | ".join(blockers)," | ".join(choices),"NO-EVALUADO"])))
    assert len(rows) == 48 and sum(int(r["estimadores"]) for r in rows) == 32347
    with (ROOT / "impedimentos-lote2-delta-48.tsv").open("w") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n"); w.writeheader(); w.writerows(rows)
    print(json.dumps({"identidades":len(rows),"estimadores":sum(int(r["estimadores"]) for r in rows)},ensure_ascii=False))
if __name__ == "__main__":
    main()
