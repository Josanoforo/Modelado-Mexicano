"""Resumen de estados de salida/resultado.json (sin reescribir nada)."""
import collections
import json

d = json.load(open("salida/resultado.json", encoding="utf-8"))
print(len(d["filas"]), collections.Counter((f["estado"], f.get("estado_ic")) for f in d["filas"]))
for f in d["filas"]:
    if f["estado"] != "RECONSTRUIDO" or f.get("estado_ic") != "CALCULADO":
        print(f)
g = json.load(open("salida/diagnostico.json", encoding="utf-8"))
print(sorted(v["n_valido"] for v in g["por_llave"].values() if "n_valido" in v)[:10])
anchos0 = [f["llave"] for f in d["filas"] if f.get("estado_ic") == "CALCULADO" and f["ic95_inf"] == f["ic95_sup"]]
print("IC ancho cero:", len(anchos0), anchos0[:5])
