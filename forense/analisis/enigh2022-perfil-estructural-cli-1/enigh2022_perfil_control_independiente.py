#!/usr/bin/env python3
"""Control focal independiente: punto segsoc=1 y EE edad=18-29."""
import argparse
import csv
import io
import json
import math
import zipfile
from pathlib import Path

import numpy as np


MEM = "conjunto_de_datos_poblacion_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh2022_ns.csv"
RID = "RESULT-ENIGH22-PERFIL-P1-MARGINALES-JSON"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--resultados", required=True)
    ap.add_argument("--output", required=True)
    a = ap.parse_args()
    filas = []
    with zipfile.ZipFile(a.zip) as z, z.open(MEM) as b:
        lector = csv.DictReader(io.TextIOWrapper(b, encoding="latin-1", newline=""))
        for x in lector:
            try: edad = int(str(x["edad"]).strip()); w = float(str(x["factor"]).strip())
            except (ValueError, TypeError): continue
            if str(x["parentesco"]).strip()[:1] not in {"1", "2", "3", "5", "6"}: continue
            if not (18 <= edad <= 96 and math.isfinite(w) and w > 0): continue
            filas.append((w, str(x["segsoc"]).strip(), edad, str(x["est_dis"]).strip(), str(x["upm"]).strip()))
    num = sum(w for w, s, *_ in filas if s == "1")
    den = sum(w for w, s, *_ in filas if s in {"1", "2"})
    punto = num / den
    psu = {}
    for w, _s, edad, est, upm in filas:
        v = psu.setdefault((est, upm), np.zeros(2))
        v += (w if 18 <= edad <= 29 else 0.0, w)
    estratos = {}
    for (e, _u), v in sorted(psu.items()): estratos.setdefault(e, []).append(v)
    rng = np.random.Generator(np.random.PCG64(20260919)); reps = np.zeros(1000)
    for i in range(1000):
        total = np.zeros(2)
        for e in sorted(estratos):
            arr = estratos[e]; m = len(arr)
            if m == 1: total += arr[0]
            else:
                for j in rng.integers(0, m, size=m): total += arr[j]
        reps[i] = total[0] / total[1]
    ee = float(np.std(reps, ddof=1))
    sellados = json.loads(Path(a.resultados).read_text(encoding="utf-8"))["resultados"]
    tabla = json.loads(sellados[RID])
    srow = next(x for x in tabla if x["variable"] == "segsoc" and x["codigo"] == "1")
    erow = next(x for x in tabla if x["variable"] == "tramo_edad" and x["codigo"] == "18-29")
    out = {
        "segsoc_1_p_independiente": punto, "segsoc_1_p_sellado": srow["proporcion"],
        "segsoc_1_delta": abs(punto - srow["proporcion"]),
        "edad_18_29_ee_independiente": ee, "edad_18_29_ee_sellado": erow["ee"],
        "edad_18_29_ee_delta": abs(ee - erow["ee"]),
        "n": len(filas), "replicas": 1000,
    }
    Path(a.output).write_text(json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, sort_keys=True))
    # El control usa otra implementación y otro orden del RNG; no se exige
    # identidad de réplicas, sino punto idéntico y EE no degenerado/concordante.
    rel_ee = out["edad_18_29_ee_delta"] / erow["ee"] if erow["ee"] else float("inf")
    if out["segsoc_1_delta"] > 1e-12 or ee <= 0 or rel_ee > 0.10:
        raise SystemExit("CONTROL-INDEPENDIENTE-NO-COINCIDE")


if __name__ == "__main__": main()
