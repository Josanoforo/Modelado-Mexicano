#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · ensambla canon/reglas-contrastadas-v1_2.tsv.

v1.1 queda intacta (PARO b). v1.2 = v1.1 byte a byte, salvo las filas de regla
dictaminadas por las hijas de este acto (`forense/analisis/medicion-carriles-2/
*-dictamenes.tsv`, clase = regla). Para cada una exige que el CALC tenga
sello.json y que el `resultado_id` exista en su spec.yaml. Escribe también
conteos-reglas.json. La cabecera de v1.1 repite `tier_declarado`: se trabaja por
índice de columna (primera aparición), nunca por dict."""
import glob
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
V11 = RAIZ / "canon/reglas-contrastadas-v1_1.tsv"
V12 = RAIZ / "canon/reglas-contrastadas-v1_2.tsv"
DIR = RAIZ / "forense/analisis/medicion-carriles-2"

lineas = V11.read_text(encoding="utf-8").split("\n")
cab = lineas[0].split("\t")
ix = {k: cab.index(k) for k in ("regla_id", "dictamen", "resultado_id", "calc", "punto", "ic95_inf",
                                 "ic95_sup", "unidad", "detalle_dictamen")}
dict_frag = {}
for f in sorted(glob.glob(str(DIR / "*-dictamenes.tsv"))):
    L = Path(f).read_text(encoding="utf-8").split("\n")
    h = L[0].split("\t")
    for l in L[1:]:
        if not l:
            continue
        r = dict(zip(h, l.split("\t")))
        if r["clase"] != "regla":
            continue
        assert r["id"] not in dict_frag, f"regla dictaminada dos veces: {r['id']}"
        calc = RAIZ / "data/corrida0" / r["calc"]
        assert (calc / "sello.json").exists(), f"sin sello: {r['calc']}"
        assert f"id: {r['resultado_id']}," in (calc / "spec.yaml").read_text(encoding="utf-8"), r["resultado_id"]
        dict_frag[r["id"]] = (Path(f).name, r)

hechas, antes, despues = [], 0, 0
out = [lineas[0]]
for l in lineas[1:]:
    if not l:
        out.append(l)
        continue
    c = l.split("\t")
    antes += c[ix["dictamen"]].startswith("SIN-CIFRA")
    if c[ix["regla_id"]] in dict_frag:
        frag, r = dict_frag[c[ix["regla_id"]]]
        assert c[ix["dictamen"]].startswith("SIN-CIFRA"), f"ya tenía dictamen: {r['id']}"
        c[ix["dictamen"]] = r["dictamen"]
        for k in ("resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad"):
            c[ix[k]] = r[k]
        c[ix["detalle_dictamen"]] = f"MC2 ({frag}): {r['detalle']} · antes (v1.1): {c[ix['detalle_dictamen']]}"
        hechas.append(r["id"])
        l = "\t".join(c)
    despues += l.split("\t")[ix["dictamen"]].startswith("SIN-CIFRA")
    out.append(l)
faltan = sorted(set(dict_frag) - set(hechas))
assert not faltan, f"reglas dictaminadas sin fila en v1.1: {faltan}"
V12.write_text("\n".join(out), encoding="utf-8")
conteos = {"sin_cifra_v1_1": antes, "sin_cifra_v1_2": despues, "reglas_dictaminadas": sorted(hechas),
           "fragmentos": sorted({v[0] for v in dict_frag.values()})}
(DIR / "conteos-reglas.json").write_text(json.dumps(conteos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(json.dumps(conteos, ensure_ascii=False))
