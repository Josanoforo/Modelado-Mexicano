"""Verificación estructural de salida/resultado.json frente a CONTRATO-v3 (solo lectura)."""
import json
import math
import re

import pandas as pd

def sin_dup(pares):
    ks = [k for k, _ in pares]
    assert len(ks) == len(set(ks)), f"nombre duplicado {ks}"
    return dict(pares)

doc = json.load(open("salida/resultado.json", encoding="utf-8"), object_pairs_hook=sin_dup)
assert set(doc) == {"version", "identidad", "filas"} and doc["version"] == 3
assert set(doc["identidad"]) == {"paquete", "version_entrada", "sha256_entrada"}
assert re.fullmatch(r"[0-9a-f]{64}", doc["identidad"]["sha256_entrada"])
esq = pd.read_csv("paquete/esquema-identidades.tsv", sep="\t", dtype=str, keep_default_na=False)
llaves = [f["llave"] for f in doc["filas"]]
assert llaves == esq.llave.tolist() and len(set(llaves)) == len(llaves)
assert [f["unidad"] for f in doc["filas"]] == esq.unidad.tolist()
dec = re.compile(r"-?[0-9]+(\.[0-9]+)?([eE][-+]?[0-9]+)?")
for f in doc["filas"]:
    for k in ("punto", "ic95_inf", "ic95_sup"):
        if k in f:
            assert dec.fullmatch(f[k]) and math.isfinite(float(f[k])), f
    if f["estado"] == "RECONSTRUIDO":
        assert "punto" in f and f["estado_ic"] in ("CALCULADO", "SIN-IC", "NO-IDENTIFICADA")
        if f["estado_ic"] == "CALCULADO":
            assert float(f["ic95_inf"]) <= float(f["ic95_sup"])
        else:
            assert "ic95_inf" not in f and "ic95_sup" not in f
        if f["estado_ic"] == "NO-IDENTIFICADA":
            assert f["motivo_ic"]
    else:
        assert "punto" not in f and f.get("motivo")
print("contrato OK", len(doc["filas"]))
for f in doc["filas"]:
    if f.get("estado_ic") == "NO-IDENTIFICADA":
        print(f["llave"], "|", f["motivo_ic"])
d = json.load(open("salida/diagnostico.json", encoding="utf-8"))
print("control H>M 2023:", d["olas"]["2023"]["conteo_suicidio_cie_por_sexo"])
for o, v in d["olas"].items():
    print(o, v["concordancia_cie_vs_presunto"])
