"""P4 (3/3) · GEN2-PISOS-Y-ADENDAS-1: compara la recalculación (commit fd54ddbd8, anterior a esta
apertura) contra los RESULT sellados, con la tolerancia fijada en protocolo-recalculo-v1_0.md §3.
Escribe comparacion.tsv y dictamen.tsv en esta carpeta."""
import csv, json, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
CALCS = {"discriminacion": ("CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001", "RESULT-ENDIREH2021-DIS-TABLA"),
         "nofisica-bc": ("CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001", "RESULT-ENDIREH2021-NF-BC-TABLA"),
         "ayuda": ("CALC-ENDIREH-PISOS-2021-AYUDA-0001", "RESULT-ENDIREH2021-AYU-TABLA")}
cmp_rows, dict_rows = [], []
for c, (calc, rid) in CALCS.items():
    tabla = json.loads(json.loads((RAIZ / "data/corrida0" / calc / "resultados.json").read_text())["resultados"][rid])
    rec = list(csv.DictReader(open(AQUI / c / f"recalculo-{c}.tsv", encoding="utf-8"), delimiter="\t"))
    fallas = []
    for r in rec:
        k = int(r["llave"].split("#")[1]); s = tabla[k]
        ident = (s["resultado"], s["eje"], s["categoria"]) == (r["desenlace"], r["eje"], r["categoria"])
        a = ident and s["estado"] == r["estado"] and int(s["n"]) == int(r["n"])
        if s["estado"] == "PUBLICABLE" and r["estado"] == "PUBLICABLE":
            dp = abs(float(r["punto"]) - s["p"]); b = dp <= 1e-10
            lo, hi = float(r["ic95_inf"]), float(r["ic95_sup"]); slo, shi = s["ic95"]
            dext = max(abs(lo - slo), abs(hi - shi)) * 100
            semi = ((hi - lo) / 2) / ((shi - slo) / 2)
            cc = dext <= 1.0 and 0.80 <= semi <= 1.25
            ic_exacto = max(abs(lo - slo), abs(hi - shi)) <= 1e-10
        else:
            dp = dext = semi = ""; b = cc = r["estado"] == s["estado"]; ic_exacto = ""
        ok = a and b and cc
        if not ok:
            fallas.append(f"{r['llave']}:{'a' if not a else ''}{'b' if not b else ''}{'c' if not cc else ''}")
        cmp_rows.append([calc, r["llave"], r["desenlace"], r["eje"], r["categoria"], s["estado"], r["estado"], s["n"], r["n"],
                         s.get("p", ""), r["punto"], dp, s.get("ic95", ["", ""])[0], s.get("ic95", ["", ""])[1],
                         r["ic95_inf"], r["ic95_sup"], dext, semi, ic_exacto, "CUMPLE" if ok else "FALLA"])
    dict_rows.append([calc, c, len(rec), len(rec) - len(fallas), "PASA" if not fallas else "NO-PASA", ";".join(fallas)])
H = ["calc", "llave", "desenlace", "eje", "categoria", "estado_sellado", "estado_recalc", "n_sellado", "n_recalc",
     "p_sellado", "p_recalc", "abs_delta_p", "ic_inf_sellado", "ic_sup_sellado", "ic_inf_recalc", "ic_sup_recalc",
     "max_delta_extremo_pp", "razon_semianchos", "ic_exacto_1e-10", "criterio"]
with open(AQUI / "comparacion.tsv", "w", encoding="utf-8") as f:
    f.write("\t".join(H) + "\n" + "\n".join("\t".join(map(str, x)) for x in cmp_rows) + "\n")
with open(AQUI / "dictamen.tsv", "w", encoding="utf-8") as f:
    f.write("calc\tadenda\tllaves\tcumplen\tdictamen\tfallas\n" + "\n".join("\t".join(map(str, x)) for x in dict_rows) + "\n")
for x in dict_rows: print(*x, sep="\t")
