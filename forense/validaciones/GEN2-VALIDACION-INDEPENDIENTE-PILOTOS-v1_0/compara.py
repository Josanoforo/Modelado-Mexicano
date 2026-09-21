#!/usr/bin/env python3
"""P2/P3/P4 · compara resultados_propios.json (P1, commit 19d35aba) contra los resultados.json
sellados de los seis CALC. Se corre DESPUÉS del commit de P1 — el orden del diff es la prueba.

Tolerancias:
  * punto (R, C2, marginales): la del tipo `proporcion` de las specs = abs 1e-10 sobre la
    misma receta. Como este código NO es la misma receta, se reporta además la diferencia en
    pp y se clasifica: |Δ| ≤ 1e-6 → IDÉNTICO; ≤ 0.05 pp → COINCIDE; > 0.05 pp → DIFERENCIA.
  * IC (plan de réplicas distinto, declarado en valida_pilotos.py): COINCIDE si
    |Δ inf| y |Δ sup| ≤ 1.0 pp Y razón de semianchos propio/sellado ∈ [0.80, 1.25];
    si no, DIFERENCIA-IC (se explica).
Escribe comparacion-pilotos.json y comparacion-pilotos.md.
"""
from __future__ import annotations

import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]
PROP = json.loads((AQUI / "resultados_propios.json").read_text())


def sellado(calc):
    r = json.loads((RAIZ / "data" / "corrida0" / calc / "resultados.json").read_text())["resultados"]
    if isinstance(r, list):
        return {it["id"]: it.get("valor") for it in r}
    return {k: (v.get("valor") if isinstance(v, dict) else v) for k, v in r.items()}


def clas_punto(a, b):
    if a is None or b is None:
        return None, "NO-COMPARABLE"
    d = (a - b) * 100
    return d, ("IDÉNTICO" if abs(a - b) <= 1e-6 else "COINCIDE" if abs(d) <= 0.05 else "DIFERENCIA")


def clas_ic(mio, sel):
    if None in mio or None in sel:
        return "NO-COMPARABLE", None
    dlo = (mio[0] - sel[0]) * 100
    dhi = (mio[1] - sel[1]) * 100
    hw_m = (mio[1] - mio[0]) / 2
    hw_s = (sel[1] - sel[0]) / 2
    razon = hw_m / hw_s if hw_s else None
    ok = abs(dlo) <= 1.0 and abs(dhi) <= 1.0 and razon is not None and 0.80 <= razon <= 1.25
    return ("COINCIDE" if ok else "DIFERENCIA-IC"), {"d_inf_pp": dlo, "d_sup_pp": dhi, "razon_semiancho": razon}


def resumen_piloto(filas, nombre, n_esperado):
    puntos = [f for f in filas if f["tipo"] in ("R", "C2")]
    max_d = max(abs(f["d_pp"]) for f in puntos if f["d_pp"] is not None)
    clases = {}
    for f in puntos:
        clases[f["clase"]] = clases.get(f["clase"], 0) + 1
    ics = [f for f in filas if f["tipo"] == "R-IC"]
    clases_ic = {}
    for f in ics:
        clases_ic[f["clase"]] = clases_ic.get(f["clase"], 0) + 1
    return {"piloto": nombre, "celdas": n_esperado, "max_abs_d_pp_punto": max_d, "clases_punto": clases, "clases_ic": clases_ic}


def p4(celdas_R_mias, celdas_C2, ic_C2_mias, puntuadas):
    """Error del piso con MIS números: MAE(C2 vs R) en pp y cobertura de IC(C2) sobre R."""
    errs, cubre, n = [], 0, 0
    for c in puntuadas:
        r = celdas_R_mias[c]
        c2 = celdas_C2[c]
        if r is None or c2 is None:
            continue
        errs.append(abs(c2 - r) * 100)
        lo, hi = ic_C2_mias[c]
        if lo is not None and lo <= r <= hi:
            cubre += 1
        n += 1
    return {"MAE_pp": sum(errs) / len(errs) if errs else None, "max_err_pp": max(errs) if errs else None,
            "ic_C2_cubre_R": cubre, "celdas_puntuadas": n}


out = {"pilotos": {}, "P4": {}}
md = ["# Comparación P2 · propios (commit `19d35aba`, a ciegas) vs sellados", ""]

# ------------------------------------------------------------------- piloto 1
p = PROP["piloto1_DIN_ENIF2024"]
arb = sellado("CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001")
emi = sellado("CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001")
filas = []
md += ["## Piloto 1 · DIN · ENIF 2024 · `localidad × edad` (8 celdas)", "",
       "| celda | n propio | n sellado | R9 propio | R9 sellado | Δ pp | clase | IC propio | IC sellado | clase IC | C2 propio (marg. sellados) | C2 sellado | Δ pp | clase |",
       "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for c, v in p["celdas"].items():
    rs = arb[f"RESULT-DIN-LXE8-ARB-R-D9-P-{c}"]
    ns = arb[f"RESULT-DIN-LXE8-ARB-R-D9-N-{c}"]
    ics = [arb[f"RESULT-DIN-LXE8-ARB-R-D9-IC95INF-{c}"], arb[f"RESULT-DIN-LXE8-ARB-R-D9-IC95SUP-{c}"]]
    c2s = emi[f"RESULT-DIN-LXE8-C2-P-{c}"]
    c2sr = emi[f"RESULT-DIN-LXE8-C2-P-REDERIVADO-{c}"]
    d, cl = clas_punto(v["R9"]["p"], rs)
    d2, cl2 = clas_punto(v["C2_punto_marginales_sellados"], c2s)
    d3, cl3 = clas_punto(v["C2_punto_marginales_propios"], c2sr)
    clic, detic = clas_ic(v["R9"]["ic95"], ics)
    r7s = arb[f"RESULT-DIN-LXE8-ARB-R-D7-P-{c}"]
    d7, cl7 = clas_punto(v["R7_sensibilidad"]["p"], r7s)
    filas += [{"celda": c, "tipo": "R", "propio": v["R9"]["p"], "sellado": rs, "n_propio": v["R9"]["n"], "n_sellado": ns, "d_pp": d, "clase": cl},
              {"celda": c, "tipo": "R-IC", "propio": v["R9"]["ic95"], "sellado": ics, "clase": clic, "detalle": detic},
              {"celda": c, "tipo": "C2", "propio": v["C2_punto_marginales_sellados"], "sellado": c2s, "d_pp": d2, "clase": cl2},
              {"celda": c, "tipo": "C2-REDERIVADO", "propio": v["C2_punto_marginales_propios"], "sellado": c2sr, "d_pp": d3, "clase": cl3},
              {"celda": c, "tipo": "R7-sensibilidad", "propio": v["R7_sensibilidad"]["p"], "sellado": r7s, "d_pp": d7, "clase": cl7}]
    md.append(f"| {c} | {v['R9']['n']} | {ns} | {v['R9']['p']:.6f} | {rs:.6f} | {d:+.4f} | {cl} | [{v['R9']['ic95'][0]:.4f}, {v['R9']['ic95'][1]:.4f}] | [{ics[0]:.4f}, {ics[1]:.4f}] | {clic} | {v['C2_punto_marginales_sellados']:.6f} | {c2s:.6f} | {d2:+.4f} | {cl2} |")
# marginales
md += ["", "Marginales de un eje (D9, ENIF 2024) — propios vs `…-G-C2-MARG-*` sellados del CALC de emisiones y vs los públicos del árbitro citados en la spec:", "",
       "| marginal | n propio | n sellado | p propio | p sellado (CALC) | Δ pp | p público árbitro (spec) | Δ pp vs público |", "|---|---|---|---|---|---|---|---|"]
ETIQ1 = {"L1": "localidad <15 000", "L2": "localidad >=15 000", "E1": "edad 18-29", "E2": "edad 30-44", "E3": "edad 45-59", "E4": "edad 60+", "NAC": "nacional"}
for k, v in p["marginales_propios"].items():
    ps = emi[f"RESULT-DIN-LXE8-G-C2-MARG-{k}-D9-P"]
    ns = emi[f"RESULT-DIN-LXE8-G-C2-MARG-{k}-D9-N"]
    pub = p["marginales_sellados_citados"][k]
    d, cl = clas_punto(v["p"], ps)
    dpub, _ = clas_punto(v["p"], pub)
    filas.append({"celda": k, "tipo": "MARGINAL", "propio": v["p"], "sellado": ps, "n_propio": v["n"], "n_sellado": ns, "d_pp": d, "clase": cl, "publico_arbitro": pub, "d_pp_vs_publico": dpub})
    md.append(f"| {ETIQ1[k]} | {v['n']} | {ns} | {v['p']:.6f} | {ps:.6f} | {d:+.4f} | {pub} | {dpub:+.4f} |")
res1 = resumen_piloto(filas, "piloto1", 8)
punt1 = list(p["celdas"])
out["pilotos"]["piloto1"] = {"resumen": res1, "filas": filas}
out["P4"]["piloto1"] = p4({c: v["R9"]["p"] for c, v in p["celdas"].items()},
                          {c: v["C2_punto_marginales_sellados"] for c, v in p["celdas"].items()},
                          {c: v["C2_ic95_marginales_propios"] for c, v in p["celdas"].items()}, punt1)
out["P4"]["piloto1"]["MAE_C2_sellado_pp"] = arb["RESULT-DIN-LXE8-ARB-G-MAE-C2"] * 100

# ------------------------------------------------------------------- piloto 2
p = PROP["piloto2_TRA_ENVIPE2025"]
arb = sellado("CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001")
emi = sellado("CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001")
filas = []
md += ["", "## Piloto 2 · TRA · ENVIPE 2025 · `escolaridad × dominio` (12 celdas)", "",
       "| celda | n propio | n sellado | R propio | R sellado | Δ pp | clase | IC propio | IC sellado | clase IC | C2 propio (marg. sellados) | C2 sellado | Δ pp | clase |",
       "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for c, v in p["celdas"].items():
    rs = arb[f"RESULT-TRA-SXD12-ARB-R-P-{c}"]
    ns = arb[f"RESULT-TRA-SXD12-ARB-R-N-{c}"]
    ics = [arb[f"RESULT-TRA-SXD12-ARB-R-IC95INF-{c}"], arb[f"RESULT-TRA-SXD12-ARB-R-IC95SUP-{c}"]]
    c2s = emi[f"RESULT-TRA-SXD12-C2-P-{c}"]
    c2sr = emi[f"RESULT-TRA-SXD12-C2-P-REDERIVADO-{c}"]
    d, cl = clas_punto(v["R"]["p"], rs)
    d2, cl2 = clas_punto(v["C2_punto_marginales_sellados"], c2s)
    d3, cl3 = clas_punto(v["C2_punto_marginales_propios"], c2sr)
    clic, detic = clas_ic(v["R"]["ic95"], ics)
    filas += [{"celda": c, "tipo": "R", "propio": v["R"]["p"], "sellado": rs, "n_propio": v["R"]["n"], "n_sellado": ns, "d_pp": d, "clase": cl},
              {"celda": c, "tipo": "R-IC", "propio": v["R"]["ic95"], "sellado": ics, "clase": clic, "detalle": detic},
              {"celda": c, "tipo": "C2", "propio": v["C2_punto_marginales_sellados"], "sellado": c2s, "d_pp": d2, "clase": cl2},
              {"celda": c, "tipo": "C2-REDERIVADO", "propio": v["C2_punto_marginales_propios"], "sellado": c2sr, "d_pp": d3, "clase": cl3}]
    md.append(f"| {c} | {v['R']['n']} | {ns} | {v['R']['p']:.6f} | {rs:.6f} | {d:+.4f} | {cl} | [{v['R']['ic95'][0]:.4f}, {v['R']['ic95'][1]:.4f}] | [{ics[0]:.4f}, {ics[1]:.4f}] | {clic} | {v['C2_punto_marginales_sellados']:.6f} | {c2s:.6f} | {d2:+.4f} | {cl2} |")
md += ["", "Marginales de un eje (ENVIPE 2025) — propios vs `…-G-M25-MARG-*` sellados:", "",
       "| marginal | n propio | n sellado | p propio | p sellado | Δ pp | clase |", "|---|---|---|---|---|---|---|"]
ETIQ2 = {"S1": "hasta primaria", "S2": "secundaria", "S3": "media superior", "S4": "superior", "D1": "rural", "D2": "complemento urbano", "D3": "urbano", "NAC": "nacional"}
for k, v in p["marginales_propios"].items():
    key = "P-NACIONAL" if k == "NAC" else f"MARG-{k}-P"
    ps = emi[f"RESULT-TRA-SXD12-G-M25-{key}"]
    ns = emi[f"RESULT-TRA-SXD12-G-M25-MARG-{k}-N"] if k != "NAC" else emi["RESULT-TRA-SXD12-G-M25-FILAS-UNIVERSO"]
    d, cl = clas_punto(v["p"], ps)
    filas.append({"celda": k, "tipo": "MARGINAL", "propio": v["p"], "sellado": ps, "n_propio": v["n"], "n_sellado": ns, "d_pp": d, "clase": cl})
    md.append(f"| {ETIQ2[k]} | {v['n']} | {ns} | {v['p']:.6f} | {ps:.6f} | {d:+.4f} | {cl} |")
res2 = resumen_piloto(filas, "piloto2", 12)
out["pilotos"]["piloto2"] = {"resumen": res2, "filas": filas}
out["P4"]["piloto2"] = p4({c: v["R"]["p"] for c, v in p["celdas"].items()},
                          {c: v["C2_punto_marginales_sellados"] for c, v in p["celdas"].items()},
                          {c: v["C2_ic95_marginales_propios"] for c, v in p["celdas"].items()}, list(p["celdas"]))
out["P4"]["piloto2"]["MAE_C2_sellado_pp"] = arb["RESULT-TRA-SXD12-ARB-G-MAE-C2"]

# ------------------------------------------------------------------- piloto 3
p = PROP["piloto3_GOB_ENCIG2025"]
adj = sellado("CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001")
emi = sellado("CALC-GOB-DIGITAL-EXE-EMISIONES-0002")
filas = []
md += ["", "## Piloto 3 · GOB · ENCIG 2025 · `edad × escolaridad` (16 celdas, 15 PUNTUADA)", "",
       "| celda | n propio | n sellado | R propio | R sellado | Δ pp | clase | IC propio | IC sellado | clase IC | C2 propio (marg. propios, universo del cruce) | C2 sellado | Δ pp | clase | soporte sellado |",
       "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
punt3 = []
for c, v in p["celdas"].items():
    cs = c.replace("|", "-")
    rs = adj[f"RESULT-GOB-EXE15-ADJ-2025-{cs}-R-P"]
    ns = adj[f"RESULT-GOB-EXE15-ADJ-2025-{cs}-N-2025"]
    ics = [adj[f"RESULT-GOB-EXE15-ADJ-2025-{cs}-R-P-IC-LO"], adj[f"RESULT-GOB-EXE15-ADJ-2025-{cs}-R-P-IC-HI"]]
    c2s = emi[f"RESULT-GOB-EXE15-2025-{cs}-C2-P"]
    ic_c2s = [emi[f"RESULT-GOB-EXE15-2025-{cs}-C2-P-IC-LO"], emi[f"RESULT-GOB-EXE15-2025-{cs}-C2-P-IC-HI"]]
    sop = adj[f"RESULT-GOB-EXE15-ADJ-2025-{cs}-SOPORTE"]
    if sop == "PUNTUADA":
        punt3.append(c)
    d, cl = clas_punto(v["R"]["p"], rs)
    d2, cl2 = clas_punto(v["C2_punto_marginales_universo_cruce"], c2s)
    d2b, cl2b = clas_punto(v["C2_punto_marginales_por_eje"], c2s)
    clic, detic = clas_ic(v["R"]["ic95"], ics)
    clic2, detic2 = clas_ic(v["C2_ic95_marginales_universo_cruce"], ic_c2s)
    filas += [{"celda": c, "tipo": "R", "propio": v["R"]["p"], "sellado": rs, "n_propio": v["R"]["n"], "n_sellado": ns, "d_pp": d, "clase": cl, "soporte_sellado": sop},
              {"celda": c, "tipo": "R-IC", "propio": v["R"]["ic95"], "sellado": ics, "clase": clic, "detalle": detic},
              {"celda": c, "tipo": "C2", "propio": v["C2_punto_marginales_universo_cruce"], "sellado": c2s, "d_pp": d2, "clase": cl2},
              {"celda": c, "tipo": "C2-ALTERNATIVA-marginales-por-eje", "propio": v["C2_punto_marginales_por_eje"], "sellado": c2s, "d_pp": d2b, "clase": cl2b},
              {"celda": c, "tipo": "C2-IC", "propio": v["C2_ic95_marginales_universo_cruce"], "sellado": ic_c2s, "clase": clic2, "detalle": detic2}]
    md.append(f"| {c} | {v['R']['n']} | {ns} | {v['R']['p']:.6f} | {rs:.6f} | {d:+.4f} | {cl} | [{v['R']['ic95'][0]:.4f}, {v['R']['ic95'][1]:.4f}] | [{ics[0]:.4f}, {ics[1]:.4f}] | {clic} | {v['C2_punto_marginales_universo_cruce']:.6f} | {c2s:.6f} | {d2:+.4f} | {cl2} | {sop} |")
md += ["", "Marginales de un eje (ENCIG 2025, universo del cruce F1-bis) — propios vs `…-MARGINAL-*` sellados:", "",
       "| marginal | n propio | n sellado | p propio | p sellado | Δ pp | clase |", "|---|---|---|---|---|---|---|"]
mapa = {"18-29": "EDAD-18-29", "30-44": "EDAD-30-44", "45-59": "EDAD-45-59", "60-96": "EDAD-60-96",
        "HASTA-PRIMARIA": "ESC-HASTA-PRIMARIA", "SECUNDARIA": "ESC-SECUNDARIA", "MEDIA-SUPERIOR": "ESC-MEDIA-SUPERIOR", "SUPERIOR": "ESC-SUPERIOR", "TOTAL": "ALL-ALL"}
for k, v in p["marginales_propios_universo_cruce"].items():
    ps = emi[f"RESULT-GOB-EXE15-2025-MARGINAL-{mapa[k]}-P"]
    ns = emi[f"RESULT-GOB-EXE15-2025-MARGINAL-{mapa[k]}-N"]
    d, cl = clas_punto(v["p"], ps)
    filas.append({"celda": k, "tipo": "MARGINAL", "propio": v["p"], "sellado": ps, "n_propio": v["n"], "n_sellado": ns, "d_pp": d, "clase": cl})
    md.append(f"| {k} | {v['n']} | {ns} | {v['p']:.6f} | {ps:.6f} | {d:+.4f} | {cl} |")
res3 = resumen_piloto(filas, "piloto3", 16)
out["pilotos"]["piloto3"] = {"resumen": res3, "filas": filas, "puntuadas_selladas": punt3}
out["P4"]["piloto3"] = p4({c: v["R"]["p"] for c, v in p["celdas"].items()},
                          {c: v["C2_punto_marginales_universo_cruce"] for c, v in p["celdas"].items()},
                          {c: v["C2_ic95_marginales_universo_cruce"] for c, v in p["celdas"].items()}, punt3)
out["P4"]["piloto3"]["MAE_C2_sellado_pp"] = adj["RESULT-GOB-EXE15-ADJ-2025-C2-MAE-PP"]

# ------------------------------------------------------------------- resumen
md += ["", "## Resumen", "", "| piloto | celdas | máx |Δ| punto (pp) | clases punto | clases IC de R |", "|---|---|---|---|---|"]
for k in ("piloto1", "piloto2", "piloto3"):
    r = out["pilotos"][k]["resumen"]
    md.append(f"| {k} | {r['celdas']} | {r['max_abs_d_pp_punto']:.4f} | {r['clases_punto']} | {r['clases_ic']} |")
md += ["", "## P4 · error del piso con los números propios (celdas PUNTUADA)", "",
       "| piloto | celdas | MAE(C2 vs R) propio pp | MAE sellado pp | máx err pp | IC95(C2) propio cubre R |", "|---|---|---|---|---|---|"]
tot_cub, tot_n, maes = 0, 0, []
for k in ("piloto1", "piloto2", "piloto3"):
    q = out["P4"][k]
    md.append(f"| {k} | {q['celdas_puntuadas']} | {q['MAE_pp']:.3f} | {q['MAE_C2_sellado_pp']:.3f} | {q['max_err_pp']:.3f} | {q['ic_C2_cubre_R']}/{q['celdas_puntuadas']} |")
    tot_cub += q["ic_C2_cubre_R"]
    tot_n += q["celdas_puntuadas"]
    maes.append((q["MAE_pp"], q["celdas_puntuadas"]))
mae_global = sum(m * n for m, n in maes) / tot_n
out["P4"]["global"] = {"celdas_puntuadas": tot_n, "MAE_ponderado_por_celdas_pp": mae_global, "ic_C2_cubre_R": tot_cub}
md.append(f"| **total** | {tot_n} | {mae_global:.3f} (media ponderada por celdas) | — | — | {tot_cub}/{tot_n} |")
(AQUI / "comparacion-pilotos.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
(AQUI / "comparacion-pilotos.md").write_text("\n".join(md) + "\n")
print("\n".join(md[-12:]))
