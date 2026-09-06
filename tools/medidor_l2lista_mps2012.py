#!/usr/bin/env python3
"""Medidor de `MAESTRA38-L2-LISTA` — ejecuta `prereg-caja-S10-L2-LISTA` §2
sobre `data/mexico.tab` (paquete list, @e088e5f, sha256 fe1014..c04488).

Escala: proporciones 0-1 (S10 §5). Sin ponderar (S10 §1).
IC95: analitico para §2.1 y §2.2; bootstrap no parametrico (B=10000,
percentil, semilla fija) para §2.3, §2.4 y §2.5 -- el contraste lista-directa
usa las MISMAS filas en ambos terminos, asi que sus dos estimadores estan
correlacionados y una formula de independencia sobreestimaria el IC.
"""
import json, sys, numpy as np

RUTA = "/mnt/c/Users/PC0/Descargas MX/ACADEMICO-list-cran/data/mexico.tab"
SHA256 = "fe101499b591d90d9e2122f439e26306fcdeab443e42d14f9455e9efa1c04488"
COMMIT = "e088e5f88af5f3d3f7d61dcffe6d7eb6d28c5120"
B = 10000
SEMILLA = 20260906


def carga(ruta=RUTA):
    """Lector explicito: la cabecera trae 25 nombres y las filas 26 campos
    (el campo 0 son los rownames de R). No se usa el modulo csv."""
    raw = open(ruta, encoding="utf-8").read().rstrip("\n").split("\n")
    hdr = [c.strip('"') for c in raw[0].split("\t")]
    filas = [r.split("\t") for r in raw[1:]]
    anchos = set(len(r) for r in filas)
    assert anchos == {len(hdr) + 1}, f"ancho inesperado {anchos} vs {len(hdr)}+1"
    rownames = [r[0].strip('"') for r in filas]
    assert len(set(rownames)) == len(rownames), "rownames no unicos"
    d = {}
    for j, nom in enumerate(hdr):
        col = [r[j + 1].strip('"') for r in filas]
        d[nom] = np.array([np.nan if v in ("NA", "") else float(v) for v in col])
    return d, hdr, rownames


def ic_wilson(k, n, z=1.959963985):
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h


def dif_medias(y, t):
    """Estimador estandar del experimento de lista (Blair & Imai 2012):
    media del conteo en tratamiento menos media en control."""
    y1, y0 = y[t == 1], y[t == 0]
    est = y1.mean() - y0.mean()
    se = np.sqrt(y1.var(ddof=1) / len(y1) + y0.var(ddof=1) / len(y0))
    return est, se, len(y1), len(y0)


def pct(a):
    return float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))


def main():
    d, hdr, rownames = carga()
    n = len(rownames)
    y, t, direct = d["mex.y.all"], d["mex.t"], d["mex.direct"]
    out = {"fuente": {"archivo": "data/mexico.tab", "paquete": "list",
                      "repo": "github.com/SensitiveQuestions/list",
                      "commit": COMMIT, "sha256": SHA256},
           "spec": "prereg-caja-S10-L2-LISTA",
           "escala": "proporciones 0-1", "ponderador": "NINGUNO (S10 §1)",
           "ic95": {"§2.1": "analitico (dif. de medias, varianzas desiguales)",
                    "§2.2": "Wilson binomial",
                    "§2.3/§2.4/§2.5": f"bootstrap no parametrico percentil, B={B}, semilla={SEMILLA}"}}

    # ---- P0: universo y nombres, contra S10 §1 y §2 ------------------------
    p0 = {"n_real": n, "n_preregistrado": 1004, "n_coincide": n == 1004,
          "n_columnas_cabecera": len(hdr), "n_campos_por_fila": len(hdr) + 1,
          "campo_0": "rownames de R (unicos, no consecutivos) - no es una variable",
          "columnas_reales": hdr}
    esperadas = ["mex.direct", "mex.wealth", "mex.urban", "mex.loyal", "mex.t", "mex.votecard"]
    p0["columnas_esperadas_presentes"] = {c: (c in hdr) for c in esperadas}
    p0["y_del_Rd_presente"] = "y" in hdr
    p0["conteo_de_lista_usado"] = "mex.y.all"
    p0["nota_y"] = ("man/mexico.Rd documenta una variable `y` ('number of items that make "
                    "respondents angry') que NO existe en data/mexico.tab: esa glosa es "
                    "arrastre de otro dataset del paquete. El conteo de lista de Mexico es "
                    "`mex.y.all` ('the number of activities that respondent did', 0-4), que "
                    "es el que corresponde al wording de cuatro actividades del propio .Rd.")
    p0["mex_cleanelections_rango_real"] = [float(np.nanmin(d["mex.cleanelections"])),
                                           float(np.nanmax(d["mex.cleanelections"]))]
    p0["nota_cleanelections"] = ("el .Rd la declara indicador 0-1; el dato real va 0-4. "
                                 "No se usa en ningun estimando de S10 §2; se declara.")
    out["P0_universo"] = p0

    # ---- S10 §4: condicion de entrada, verificada mecanicamente ------------
    mx1, mx0 = float(y[t == 1].max()), float(y[t == 0].max())
    cond = {"max_conteo_tratamiento": mx1, "max_conteo_control": mx0,
            "items_tratamiento_implicados": mx1, "items_control_implicados": mx0,
            "regla": "lista tratamiento = lista control + UN item",
            "cumple": bool(mx1 == 4 and mx0 == 3),
            "wording_item_anadido": "Exchange your vote for a gift, favor, or access to a service",
            "item_es_venta_del_voto": True,
            "fuente_wording": "man/mexico.Rd (\\description + \\details)"}
    out["S10_4_condicion_de_entrada"] = cond
    if not cond["cumple"]:
        out["veredicto"] = "PROPUESTA-REFUTADA-POR-DISENO"
        json.dump(out, open("data/l2lista-resultados-v1_0.json", "w"), indent=2, ensure_ascii=False)
        print("PROPUESTA-REFUTADA-POR-DISENO"); return

    rng = np.random.default_rng(SEMILLA)
    idx = rng.integers(0, n, size=(B, n))

    # ---- §2.1 prevalencia por lista ---------------------------------------
    est1, se1, n1, n0 = dif_medias(y, t)
    z = 1.959963985
    out["e1_prevalencia_por_lista"] = {
        "estimador": "diferencia de medias tratamiento-control (Blair & Imai 2012)",
        "estimacion": float(est1), "se": float(se1),
        "ic95": [float(est1 - z * se1), float(est1 + z * se1)],
        "n_tratamiento": int(n1), "n_control": int(n0),
        "media_tratamiento": float(y[t == 1].mean()), "media_control": float(y[t == 0].mean())}

    # ---- §2.2 prevalencia directa -----------------------------------------
    k = int(np.nansum(direct)); nd = int((~np.isnan(direct)).sum())
    lo, hi = ic_wilson(k, nd)
    out["e2_prevalencia_directa"] = {"variable": "mex.direct", "si": k, "n": nd,
                                     "estimacion": k / nd, "ic95": [float(lo), float(hi)]}

    # ---- §2.3 contraste lista - directa (bootstrap) ------------------------
    bl = np.array([y[i][t[i] == 1].mean() - y[i][t[i] == 0].mean() for i in idx])
    bd = np.array([np.nanmean(direct[i]) for i in idx])
    bc = bl - bd
    est3 = est1 - k / nd
    lo3, hi3 = pct(bc)
    out["e3_contraste_lista_menos_directa"] = {
        "estimacion": float(est3), "ic95": [lo3, hi3],
        "ic95_incluye_0": bool(lo3 <= 0 <= hi3),
        "semiancho_ic95": float((hi3 - lo3) / 2)}

    # ---- §2.4 heterogeneidad ----------------------------------------------
    het = {}
    med_w = float(np.median(d["mex.wealth"]))
    estratos = {
        "mex.wealth": ("mediana de mex.wealth = %.4f (variable continua; corte por mediana, declarado)" % med_w,
                       {"bajo (<=mediana)": d["mex.wealth"] <= med_w,
                        "alto (>mediana)": d["mex.wealth"] > med_w}),
        "mex.urban": ("indicador 0/1", {"rural (0)": d["mex.urban"] == 0, "urbano (1)": d["mex.urban"] == 1}),
        "mex.loyal": ("indicador 0/1", {"no leal (0)": d["mex.loyal"] == 0, "leal (1)": d["mex.loyal"] == 1}),
    }
    for var, (nota, grupos) in estratos.items():
        het[var] = {"corte": nota, "estratos": {}}
        for etq, m in grupos.items():
            ym, tm, dm = y[m], t[m], direct[m]
            e, se, a, b = dif_medias(ym, tm)
            kk = int(np.nansum(dm)); nn = int((~np.isnan(dm)).sum())
            pos = np.flatnonzero(m); nm = len(pos)
            bi = rng.integers(0, nm, size=(B, nm))
            bl_ = np.array([ym[i][tm[i] == 1].mean() - ym[i][tm[i] == 0].mean() for i in bi])
            bd_ = np.array([np.nanmean(dm[i]) for i in bi])
            l3, h3 = pct(bl_ - bd_)
            ll, hh = pct(bl_)
            het[var]["estratos"][etq] = {
                "n": int(nm), "n_tratamiento": int(a), "n_control": int(b),
                "e1_lista": float(e), "e1_ic95_analitico": [float(e - z * se), float(e + z * se)],
                "e1_ic95_bootstrap": [ll, hh],
                "e2_directa": kk / nn,
                "e3_contraste": float(e - kk / nn), "e3_ic95": [l3, h3],
                "e3_ic95_incluye_0": bool(l3 <= 0 <= h3)}
    out["e4_heterogeneidad"] = het

    # ---- §2.5 participacion verificada x directa ---------------------------
    vc = d["mex.votecard"]
    ok = ~np.isnan(vc) & ~np.isnan(direct)
    v1 = direct[ok & (vc == 1)]; v0 = direct[ok & (vc == 0)]
    p1, p0_ = float(v1.mean()), float(v0.mean())
    bdif = np.array([direct[i][ok[i] & (vc[i] == 1)].mean() - direct[i][ok[i] & (vc[i] == 0)].mean()
                     for i in idx])
    l5, h5 = pct(bdif)
    lo1, hi1 = ic_wilson(int(v1.sum()), len(v1)); lo0, hi0 = ic_wilson(int(v0.sum()), len(v0))
    out["e5_participacion_verificada_x_directa"] = {
        "instrumento": "mex.votecard - turnout VERIFICADO POR ENCUESTADOR (enumerator-verified), "
                       "distinto de mex.vote (autodeclarado). NO es SIN-INSTRUMENTO.",
        "tabla_2x2": {
            "verificado_voto_1": {"n": int(len(v1)), "directa_si": int(v1.sum()),
                                  "tasa": p1, "ic95": [float(lo1), float(hi1)]},
            "verificado_voto_0": {"n": int(len(v0)), "directa_si": int(v0.sum()),
                                  "tasa": p0_, "ic95": [float(lo0), float(hi0)]}},
        "diferencia_de_proporciones": p1 - p0_, "ic95": [l5, h5],
        "ic95_incluye_0": bool(l5 <= 0 <= h5)}

    json.dump(out, open("data/l2lista-resultados-v1_0.json", "w"), indent=2, ensure_ascii=False)
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
