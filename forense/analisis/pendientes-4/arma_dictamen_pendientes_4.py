#!/usr/bin/env python3
"""arma_dictamen_pendientes_4.py -- ACTO GEN2-PENDIENTES-4: adjudica las propuestas de los investigadores de
solo lectura (`evidencia/`) y arma los grupos de destino de cada NC ABIERTA. No escribe el libro:
eso lo hace `aplica_dictamen_pendientes_4.py` sobre el `dictamen-pendientes-4.tsv` que este script emite.

Regla de adjudicación (la fija el acto, antes de mirar los resultados):
  * un CERRAR-* entra solo si DOS verificadores independientes lo CONFIRMAN (lente «reproduce»:
    re-corre los comandos; lente «suficiencia»: ¿cierra exactamente lo que la fila pedía?).
    Un cierre sin las dos confirmaciones NO se aplica: pasa a la segunda pasada (re-ruteo).
  * HOJA-DECISION de la primera pasada pasa a la segunda: D-19 estricto (solo lo irreversible va
    a mesa) y la ADENDA-1 ordena decidir y declarar lo reversible.
  * NO-CONCLUYENTE pasa a la segunda pasada.
  * ABSORBER, HOJA-RECETA, CANAL y MANTENER-DUENO son finales de la ronda que los emite.
El estado final de una fila es el de su última ronda (ronda 2 = lotes R-*).

    python3 arma_dictamen_pendientes_4.py --pools <dir-res>                    # agrega y reporta
    python3 arma_dictamen_pendientes_4.py --reruta <dir-res> <dir-batches>     # escribe lotes R-n de la 2ª pasada
"""
import glob
import json
import os
import sys
from collections import Counter, defaultdict


def carga(res):
    """{key: {'rows': {id: fila}, 'ver': {lens: {id: reg}}}} para cada lote con research."""
    out = {}
    for p in sorted(glob.glob(os.path.join(res, "*.research.json"))):
        key = os.path.basename(p)[: -len(".research.json")]
        rows = {r["id"]: r for r in json.load(open(p, encoding="utf-8"))}
        ver = {}
        for lens in ("reproduce", "suficiencia"):
            q = os.path.join(res, f"{key}.verif-{lens}.json")
            if os.path.exists(q):
                ver[lens] = {r["id"]: r for r in json.load(open(q, encoding="utf-8"))}
        out[key] = {"rows": rows, "ver": ver}
    return out


def confirmado(lote, i):
    v = lote["ver"]
    return all(v.get(l, {}).get(i, {}).get("veredicto") == "CONFIRMA" for l in ("reproduce", "suficiencia"))


def estado_final(datos):
    """{id: {'ronda':1|2,'key':k,'fila':fila,'estado':...,'objeciones':[...]}} usando la última ronda."""
    fin = {}
    for ronda, prefijo in ((1, False), (2, True)):
        for key, lote in datos.items():
            if key.startswith("R-") != prefijo:
                continue
            for i, f in lote["rows"].items():
                v = f["verdict"]
                if v.startswith("CERRAR"):
                    if confirmado(lote, i):
                        est = "CERRAR"
                        obj = []
                    else:
                        est = "REFUTADO"
                        obj = [f"[{l}] {lote['ver'].get(l, {}).get(i, {}).get('razon', 'SIN-VERIFICACIÓN')}"
                               for l in ("reproduce", "suficiencia")
                               if lote["ver"].get(l, {}).get(i, {}).get("veredicto") != "CONFIRMA"]
                elif v == "HOJA-DECISION":
                    est, obj = ("HOJA-DECISION" if ronda == 2 else "DECISION-A-CLASIFICAR"), []
                elif v == "NO-CONCLUYENTE":
                    est, obj = "NO-CONCLUYENTE", []
                else:
                    est, obj = v, []
                fin[i] = {"ronda": ronda, "key": key, "fila": f, "estado": est, "objeciones": obj}
    return fin


def main():
    if "--pools" in sys.argv or "--reruta" in sys.argv:
        modo = "--reruta" if "--reruta" in sys.argv else "--pools"
        res = sys.argv[sys.argv.index(modo) + 1]
        datos = carga(res)
        fin = estado_final(datos)
        print(f"lotes con research: {len(datos)} · NC con estado: {len(fin)}")
        print(dict(Counter(f["estado"] for f in fin.values())))
        if modo == "--pools":
            for est in sorted({f["estado"] for f in fin.values()}):
                print(f"\n## {est}: {sum(1 for f in fin.values() if f['estado'] == est)}")
            return 0
        bdir = sys.argv[sys.argv.index(modo) + 2]
        pend = [(i, f) for i, f in fin.items()
                if f["estado"] in ("REFUTADO", "NO-CONCLUYENTE", "DECISION-A-CLASIFICAR") and f["ronda"] == 1]
        # el libro trae la fila completa en el lote original
        libro = {}
        for p in glob.glob(os.path.join(bdir, "*.json")):
            if os.path.basename(p).startswith(("_", "R-")):
                continue
            for r in json.load(open(p, encoding="utf-8")):
                libro[r["id"]] = r
        pend.sort(key=lambda x: (x[1]["estado"], x[0]))
        lotes = defaultdict(list)
        n = 0
        for k, (i, f) in enumerate(pend):
            lotes[f"R-{k // 9 + 1}"].append({
                "motivo": {"REFUTADO": "REFUTADO", "NO-CONCLUYENTE": "NO-CONCLUYENTE",
                           "DECISION-A-CLASIFICAR": "DECISION-A-CLASIFICAR"}[f["estado"]],
                "row": libro[i], "prior": f["fila"], "objeciones": f["objeciones"]})
            n += 1
        for key, filas in lotes.items():
            with open(os.path.join(bdir, f"{key}.json"), "w", encoding="utf-8") as fh:
                fh.write("[\n" + ",\n".join(json.dumps(x, ensure_ascii=False) for x in filas) + "\n]\n")
        print(f"segunda pasada: {n} filas en {len(lotes)} lotes: {sorted(lotes)}")
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
