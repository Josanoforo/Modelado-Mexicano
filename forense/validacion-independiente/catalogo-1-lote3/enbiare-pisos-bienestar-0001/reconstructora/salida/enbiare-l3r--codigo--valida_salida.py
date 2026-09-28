#!/usr/bin/env python3
"""Validación estructural de salida/resultado.json contra CONTRATO-v3.md (sin referencias)."""
import json
import re
from collections import Counter

import pandas as pd

ESTADOS = {"RECONSTRUIDO", "NO-EVALUADO", "NO-RECALCULABLE-DESDE-SPEC", "BLOQUEADO-POR-ACCESO",
           "DENOMINADOR-CERO", "NO-ESTIMABLE"}
DEC = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")


def sin_duplicados(pares):
    d = {}
    for k, v in pares:
        if k in d:
            raise ValueError("nombre duplicado " + k)
        d[k] = v
    return d


def main():
    with open("salida/resultado.json", encoding="utf-8") as fh:
        doc = json.load(fh, object_pairs_hook=sin_duplicados)
    assert list(doc) == ["version", "identidad", "filas"] and doc["version"] == 3
    assert set(doc["identidad"]) == {"paquete", "version_entrada", "sha256_entrada"}
    assert re.fullmatch(r"[0-9a-f]{64}", doc["identidad"]["sha256_entrada"])
    s = pd.read_csv("paquete/esquema-identidades.tsv", sep="\t", dtype=str, keep_default_na=False)
    assert [f["llave"] for f in doc["filas"]] == s["llave"].tolist()
    assert [f["unidad"] for f in doc["filas"]] == s["unidad"].tolist()
    c = Counter()
    for f in doc["filas"]:
        assert f["estado"] in ESTADOS
        if f["estado"] == "RECONSTRUIDO":
            assert DEC.match(f["punto"])
            c[f["estado_ic"]] += 1
            if f["estado_ic"] == "CALCULADO":
                assert DEC.match(f["ic95_inf"]) and DEC.match(f["ic95_sup"])
                assert float(f["ic95_inf"]) <= float(f["ic95_sup"])
            elif f["estado_ic"] == "NO-IDENTIFICADA":
                assert f["motivo_ic"] and "ic95_inf" not in f and "ic95_sup" not in f
        else:
            assert f.get("motivo")
            assert not any(k in f for k in ("punto", "ic95_inf", "ic95_sup"))
            assert f.get("estado_ic", "SIN-IC") == "SIN-IC"
    print("resultado.json OK", Counter(f["estado"] for f in doc["filas"]), dict(c))

    t = pd.read_csv("salida/diagnosticos-ic-v1.tsv", sep="\t", dtype=str, keep_default_na=False)
    assert t["llave"].tolist() == s["llave"].tolist()
    print("diagnosticos-ic-v1.tsv", t.shape, t["tipo_incertidumbre"].value_counts().to_dict(),
          "replicas no estimables", t["n_replicas_no_estimables"].value_counts().to_dict())

    with open("salida/diagnostico.json", encoding="utf-8") as fh:
        d = json.load(fh)
    print(json.dumps(d["datos"], ensure_ascii=False))
    print(Counter(l["publicabilidad"] for l in d["llaves"]))
    print(len(d["decisiones_implementacion"]), "decisiones")


if __name__ == "__main__":
    main()
