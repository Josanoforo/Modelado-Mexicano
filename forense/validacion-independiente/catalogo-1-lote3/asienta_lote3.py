#!/usr/bin/env python3
"""ACTO GEN2-ASTRA6-C1-LOTE-3 · P3. Dictamen por identidad (404 llaves = 56 ⊂ 312, más 92) y
asiento en data/corrida0/validaciones-independientes.tsv. Vocabulario de ASTRA6-1.

Regla, fijada antes de escribir y aplicada por llave:
- NO-LANZADO (gate): la llave no entró al lote → SOSTENER-SIN-CORROBORACION (nada comparado;
  no es discrepancia).
- Lanzada, compare_v3 = COINCIDE → SOSTENER (no hubo ningún caso).
- Lanzada, punto dentro de tolerancia e IC fuera → SOSTENER. El IC no se adjudica sin margen
  de equivalencia firmado (157c-01 ABIERTA); es el mismo criterio que C1-1 aplicó a 1 873.
- Lanzada, punto fuera, con la causa localizada en una lectura de la spec que la
  reconstructora declaró en insuficiencias.md y con |Δp| < 1 SE sellado → ACOTAR (rótulo).
- Lanzada, punto fuera sin causa localizada o con |Δp| ≥ 1 SE → PROPONER-SUSPENDER.
Asiento: una fila por (spec, RESULT). PASA solo si compare_v3 = COINCIDE en todas las llaves
del RESULT (punto e IC). Si no, NO-PASA, con la tolerancia citada. La vista no admite
duplicados, y una llave ya asentada no se re-asienta.
Uso: python3 asienta_lote3.py [--escribe]"""
import csv, hashlib, json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[3]
L = Path(__file__).resolve().parent
K = "endireh-pisos-2016-pareja-fisica-0002"
T2 = R / "forense/validacion-independiente/catalogo-1-ejecucion-lote2/lote2-tabla-estimadores.tsv"
CMP = L / K / "comparacion/endireh2016-pf-l3--comparacion.json"
SEL = R / "data/corrida0/CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002/resultados.json"
V = R / "data/corrida0/validaciones-independientes.tsv"
OUT = L / "dictamen-lote3.tsv"
ACOTAR = {  # llave -> causa localizada (insuficiencias.md punto 6 de la reconstructora)
    f"RESULT-ENDIREH2016-PF-TABLA#{i}": "edad 60+: el sellado cuenta EDAD=98 («edad no especificada», FD) "
    "como 60+; la reconstructora la excluye; n 9480 vs 9384 = 96 casos"
    for i in (4, 50)}

lee = lambda p: list(csv.DictReader(open(p, encoding="utf-8"), delimiter="\t"))
T = lee(T2)
cmp = json.loads(CMP.read_text())
por_llave = {r["llave"]: r for r in cmp["resultados"]}
sel = json.loads(json.loads(SEL.read_text())["resultados"]["RESULT-ENDIREH2016-PF-TABLA"])
tol = f"tol abs={cmp['tolerancia']['abs']} rel={cmp['tolerancia']['rel']} (tolerancia.json del paquete c1-ventana-v1)"

filas = []
for t in T:
    g56 = t["estado_punto"] == "NO-RECALCULABLE-DESDE-SPEC"
    g312 = t["estado_ic"] == "NO-RECALCULABLE-DESDE-SPEC"
    g92 = t["apartado_por_adenda"] == "True"
    if not (g56 or g312 or g92):
        continue
    grupos = ",".join(g for g, b in (("56", g56), ("312", g312), ("92", g92)) if b)
    if g92:
        c = por_llave[t["llave"]]
        pd_, icd = c["campos"]["punto"]["dentro"], c["campos"]["ic95_inf"]["dentro"] and c["campos"]["ic95_sup"]["dentro"]
        i = int(t["llave"].split("#")[1])
        dp = abs(float(c["campos"]["punto"]["delta"])) / sel[i]["se"]
        if c["estado"] == "COINCIDE":
            d, m = "SOSTENER", "compare_v3 COINCIDE"
        elif pd_ and not icd:
            d, m = "SOSTENER", "punto dentro; IC fuera (bootstrap con otro generador; sin margen de equivalencia firmado, 157c-01)"
        elif not pd_ and t["llave"] in ACOTAR and dp < 1:
            d, m = "ACOTAR", f"{ACOTAR[t['llave']]}; |Δp|={float(c['campos']['punto']['delta']):.3g} ({dp:.2f} SE)"
        else:
            d, m = "PROPONER-SUSPENDER", f"punto fuera sin causa localizada o ≥1 SE ({dp:.2f} SE)"
        filas.append([t["llave"], t["calc"], t["result_id"], t["instrumento"], t["ola"], t["paquete"], grupos,
                      "LANZADO", c["estado"], "DENTRO" if pd_ else "FUERA", "DENTRO" if icd else "FUERA",
                      d, m, "CIEGA-POR-CONTEXTO-NUEVO"])
    else:
        filas.append([t["llave"], t["calc"], t["result_id"], t["instrumento"], t["ola"], t["paquete"], grupos,
                      "NO-LANZADO (gate ACCESO-AUTORIZADO)", "NO-COMPARADO", "", "",
                      "SOSTENER-SIN-CORROBORACION",
                      f"{t['instrumento']} {t['ola']} sin firma de acceso C1 en este acto (ee49-01/02 cubren solo ENDIREH 2021/2016); nada comparado", ""])

cab = ["llave", "calc", "result_id", "instrumento", "ola", "paquete", "grupos_encargo", "gate", "estado_comparador",
       "punto", "ic", "dictamen", "motivo", "rotulo_ceguera"]
assert all("\t" not in x and "\n" not in x for f in filas for x in f)
from collections import Counter
print(len(filas), Counter(f[11] for f in filas), Counter(f[7] for f in filas))

# Asiento: una fila por (spec, RESULT) lanzado
vistos = {(x["spec_id"], x["resultado_id"]) for x in lee(V)}
lanz = [f for f in filas if f[7] == "LANZADO"]
nuevas = []
for (calc, rid) in sorted({(f[1], f[2]) for f in lanz}):
    fs = [f for f in lanz if (f[1], f[2]) == (calc, rid)]
    assert (calc, rid) not in vistos, ("ya asentada", calc, rid)
    todas = all(f[8] == "COINCIDE" for f in fs)
    cnt = Counter(f[11] for f in fs)
    ref = str(CMP.relative_to(R))
    nuevas.append([calc, rid, "PASA" if todas else "NO-PASA", ref, hashlib.sha256(CMP.read_bytes()).hexdigest(),
        f"C1-LOTE3-CIEGA-POR-CONTEXTO-NUEVO {tol}: compare_v3 {sum(f[8]=='COINCIDE' for f in fs)}/{len(fs)} COINCIDE; "
        f"punto dentro {sum(f[9]=='DENTRO' for f in fs)}/{len(fs)}, IC (ambos extremos) dentro {sum(f[10]=='DENTRO' for f in fs)}/{len(fs)}; "
        f"dictamen " + " · ".join(f"{k} {v}" for k, v in sorted(cnt.items())) +
        f"; de {len(fs)} celdas (GEN2-ASTRA6-C1-LOTE-3; sesión reconstructora nueva auditada por transcript: "
        f"Bash sin red y /tmp privado; el proceso claude sí tenía red hacia la API; no es aislamiento por broker)"])
print(nuevas)
if "--escribe" in sys.argv:
    OUT.write_text("\t".join(cab) + "\n" + "".join("\t".join(f) + "\n" for f in filas), encoding="utf-8")
    raw = V.read_bytes()
    assert raw.endswith(b"\n")
    with V.open("a", encoding="utf-8", newline="") as fh:
        for n in nuevas:
            assert all("\t" not in x and "\n" not in x for x in n)
            fh.write("\t".join(n) + "\n")
