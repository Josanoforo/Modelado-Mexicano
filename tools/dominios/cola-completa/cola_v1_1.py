#!/usr/bin/env python3
"""Cola de medición v1.1 con estado por fila · ACTO GEN2-COLA-COMPLETA-1.

Insumos (ninguno se edita aquí):
  · `forense/analisis/dominios/cola-medicion-v1_0.tsv` en el SHA de redacción del encargo
    (`34949751`, 61 filas): la cola que este acto agota. Se lee de git y no del árbol, porque
    `redictamina_v1_1.py` la re-deriva y la encoge a medida que las afirmaciones se resuelven;
  · `tools/dominios/cola-completa/adjudicacion-v1_0.tsv` — una fila por afirmación con el
    estado que este acto le da y su evidencia (CALC y RESULT citados, pregunta buscada o
    razón). Es texto de decisión, no cifras: ningún valor numérico vive ahí.

Salida: `forense/analisis/dominios/cola-medicion-v1_1.tsv` — la cola v1.0 con el estado de
cada fila (encargo §1 «Hecho»: MEDIDO con CALC citado · NO-CONSTRUIBLE con pregunta buscada ·
DIFERIDO con razón). Regla de fila, declarada antes de adjudicar:
  MEDIDO          ≥ 1 afirmación de la fila MEDIDO (las demás se listan con su estado);
  NO-CONSTRUIBLE  ninguna MEDIDO y todas NO-CONSTRUIBLE;
  DIFERIDO        el resto (la razón de cada afirmación diferida va en la fila).
Toda afirmación de la cola debe tener exactamente una fila de adjudicación; una que falte o
sobre es error (sale 2), no fila sin estado.

    python3 tools/dominios/cola-completa/cola_v1_1.py            # escribe
    python3 tools/dominios/cola-completa/cola_v1_1.py --verifica # byte a byte
"""
from __future__ import annotations

import csv
import subprocess
import io
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
COLA_SHA, COLA_REL = "34949751", "forense/analisis/dominios/cola-medicion-v1_0.tsv"
ADJ = Path(__file__).resolve().parent / "adjudicacion-v1_0.tsv"
OUT = ROOT / "forense/analisis/dominios/cola-medicion-v1_1.tsv"
ESTADOS = ("MEDIDO", "NO-CONSTRUIBLE", "DIFERIDO")
CAMPOS_ADJ = ("id_afirmacion", "dominio", "programa_id", "estado", "calc", "result_ids",
              "veredicto", "razon")


def lee(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader((l for l in fh if not l.startswith("#")), delimiter="\t"))


def estado_fila(estados: list[str]) -> str:
    if "MEDIDO" in estados:
        return "MEDIDO"
    if estados and all(e == "NO-CONSTRUIBLE" for e in estados):
        return "NO-CONSTRUIBLE"
    return "DIFERIDO"


def main(verifica: bool) -> int:
    txt = subprocess.run(["git", "-C", str(ROOT), "show", f"{COLA_SHA}:{COLA_REL}"], check=True,
                         capture_output=True, text=True).stdout
    cola = list(csv.DictReader((l for l in io.StringIO(txt) if not l.startswith("#")), delimiter="\t"))
    adj_rows = lee(ADJ)
    errores = []
    if adj_rows and tuple(adj_rows[0].keys()) != CAMPOS_ADJ:
        errores.append(f"columnas de {ADJ.name}: {tuple(adj_rows[0].keys())} != {CAMPOS_ADJ}")
    adj: dict[str, dict] = {}
    for r in adj_rows:
        if r["id_afirmacion"] in adj:
            errores.append(f"id duplicado en adjudicación: {r['id_afirmacion']}")
        if r["estado"] not in ESTADOS:
            errores.append(f"{r['id_afirmacion']}: estado {r['estado']!r} fuera de {ESTADOS}")
        if r["estado"] == "MEDIDO" and not (r["calc"] and r["result_ids"]):
            errores.append(f"{r['id_afirmacion']}: MEDIDO sin CALC y RESULT citados")
        if r["estado"] != "MEDIDO" and not r["razon"]:
            errores.append(f"{r['id_afirmacion']}: {r['estado']} sin razón")
        adj[r["id_afirmacion"]] = r
    en_cola = set()
    filas = []
    for c in cola:
        ids = [i for i in c["ids"].split(";") if i]
        en_cola.update(ids)
        faltan = [i for i in ids if i not in adj]
        if faltan:
            errores.append(f"fila {c['dominio']}/{c['programa']}: sin adjudicación {faltan}")
            continue
        for i in ids:
            if (adj[i]["dominio"], adj[i]["programa_id"]) != (c["dominio"], c["programa"]):
                errores.append(f"{i}: adjudicado como {adj[i]['dominio']}/{adj[i]['programa_id']}, "
                               f"cola lo pone en {c['dominio']}/{c['programa']}")
        est = [adj[i]["estado"] for i in ids]
        n = Counter(est)
        calcs = sorted({x for i in ids for x in adj[i]["calc"].split(";") if x})
        filas.append({
            "dominio": c["dominio"], "programa": c["programa"], "ola": c["ola"],
            "n_afirmaciones": len(ids), "estado_fila": estado_fila(est),
            "n_medido": n["MEDIDO"], "n_no_construible": n["NO-CONSTRUIBLE"], "n_diferido": n["DIFERIDO"],
            "calc_citados": ";".join(calcs),
            "detalle": " | ".join(f"{i}={adj[i]['estado']}"
                                  + (f"[{adj[i]['veredicto']}]" if adj[i]["veredicto"] else "")
                                  + (f": {adj[i]['razon']}" if adj[i]["estado"] != "MEDIDO" else "")
                                  for i in ids),
            "ids": ";".join(ids),
        })
    sobran = sorted(set(adj) - en_cola)
    if sobran:
        errores.append(f"adjudicaciones sin fila en la cola: {sobran}")
    if errores:
        print("ERROR-COLA-V1_1", *errores, sep="\n  ")
        return 2
    buf = io.StringIO()
    buf.write("# GENERADO por tools/dominios/cola-completa/cola_v1_1.py — no editar\n")
    w = csv.DictWriter(buf, list(filas[0].keys()), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(filas)
    txt = buf.getvalue()
    print("cola v1.1:", len(filas), "filas ·", dict(Counter(f["estado_fila"] for f in filas)),
          "· afirmaciones:", dict(Counter(a["estado"] for a in adj.values())),
          "· sin estado:", sum(1 for f in filas if not f["estado_fila"]))
    if verifica:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == txt
        print(("COINCIDE " if ok else "DIFIERE  ") + str(OUT.relative_to(ROOT)))
        return 0 if ok else 1
    OUT.write_text(txt, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main("--verifica" in sys.argv))
