#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA34-L6 · P3 — estimador del efecto de la concurrencia.

Ejecuta, sin desviarse, la spec congelada en
forense/notas/2026-09-02-MAESTRA34-L6-P2-spec.md (COMMIT-1).

    Dy(m,k) = gamma * hueco(k) + beta * DeltaD(k) + e(m,k)

a nivel municipio, sobre transiciones entre elecciones municipales consecutivas.
IC principal por bootstrap wild cluster (Rademacher) sobre las entidades.
"""
import os, sys, json, math, random, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l6_lectores as L

S = L.SERIE
L4 = "data/raw/electoral_local_2023_2024"
SEED, B = 42, 10000

# ------------------------------------------------------------------ el panel
def panel():
    P = {}   # (entidad, anio) -> {municipio: (votos, lista_nominal)}
    ctrl = {}

    # ---- Coahuila (IEC): 2017 no concurrente, 2018/2021/2024 concurrentes
    P[("Coahuila", 2017)], e = L.coahuila_municipio(
        os.path.join(S, "iec_coahuila_2017_ayuntamientos_x_municipio.xlsx"), 5)
    ctrl["coahuila2017_excluidas"] = [x[0] for x in e]
    P[("Coahuila", 2018)], e = L.coahuila_municipio(
        os.path.join(S, "iec_coahuila_2018_ayuntamientos_x_municipio.xlsx"), 10)
    ctrl["coahuila2018_excluidas"] = [x[0] for x in e]
    P[("Coahuila", 2021)], _ = L.coahuila_municipio(
        os.path.join(S, "iec_coahuila_2021_ayuntamientos_x_municipio.xlsx"), 6)
    P[("Coahuila", 2024)], _ = L.coahuila_municipio(
        os.path.join(L4, "iec_coahuila_2024/Ayuntamientos2024_X_Municipio.xlsx"), 6)

    # ---- Nayarit (IEE): votos en la tabla de computos, denominador en PDF aparte
    for anio, arch, hoja in ((2017, "iee_nayarit_2017_ayuntamientos.xlsx", "Concentrado"),
                             (2021, "iee_nayarit_2021_ayuntamientos.xlsx", "Concentrado"),
                             (2024, "iee_nayarit_2024_ayuntamientos.xlsx", "ConcentradoMR")):
        votos, cols = L.nayarit_votos(os.path.join(S, arch), hoja)
        ln = L.nayarit_lista_nominal(os.path.join(S, f"iee_nayarit_{anio}_lista_nominal.pdf"))
        P[("Nayarit", anio)] = {k: (votos[k], ln[k]) for k in votos if k in ln and ln[k] > 0}
        ctrl[f"nayarit{anio}_cols_sumadas"] = cols
        ctrl[f"nayarit{anio}_sin_ln"] = sorted(set(votos) - set(ln))

    # ---- Zacatecas (IEEZ): casilla -> municipio
    for anio, arch, hoja, hd in (
            (2018, "ieez_zacatecas_2018_ayto_x_casilla.xlsx", "20180712_2313_COMP_AYU_Zac (2)", 1),
            (2021, "ieez_zacatecas_2021_computos.xlsx", "20210720_1830_COMP_AYU_Zac", 2),
            (2024, "ieez_zacatecas_2024_computos.xlsx", "AYUNTAMIENTOS", 3)):
        P[("Zacatecas", anio)], _ = L.zacatecas_casilla(os.path.join(S, arch), hoja, hd)

    # ---- Durango (IEPC): 2016 SOLO la capital (el archivo publicado no trae mas),
    #      2019 estatal. La transicion queda por tanto sobre 1 municipio.
    d16, (n16, sub16, gran16) = L.durango2016_municipio_capital(
        os.path.join(S, "iepc_durango_2016_resultados.xlsx"))
    P[("Durango", 2016)] = {"DURANGO": (gran16[0], gran16[1])}   # fila de gran total publicada
    ctrl["durango2016"] = {"casillas_sumadas": n16, "subtotales_descartados": sub16,
                           "gran_total_publicado": [gran16[0], gran16[1]],
                           "suma_casillas": [d16["DURANGO"][0], d16["DURANGO"][1]]}
    P[("Durango", 2019)], (ok, mal, _cab) = L.durango2019_csv(
        os.path.join(S, "iepc_durango_2019_x_casilla.zip"))
    ctrl["durango2019"] = {"casillas_ok": ok, "casillas_descartadas": mal}
    return P, ctrl

# ---- calendario: D = 1 si la jornada local coincidio con la federal (P0)
D = {("Coahuila", 2017): 0, ("Coahuila", 2018): 1, ("Coahuila", 2021): 1, ("Coahuila", 2024): 1,
     ("Nayarit", 2017): 0, ("Nayarit", 2021): 1, ("Nayarit", 2024): 1,
     ("Zacatecas", 2018): 1, ("Zacatecas", 2021): 1, ("Zacatecas", 2024): 1,
     ("Durango", 2016): 0, ("Durango", 2019): 0}
SERIES = {"Coahuila": [2017, 2018, 2021, 2024], "Nayarit": [2017, 2021, 2024],
          "Zacatecas": [2018, 2021, 2024], "Durango": [2016, 2019]}

# ------------------------------------------------------------ transformaciones
def participacion(P):
    y, fuera = {}, []
    for (ent, anio), d in P.items():
        for m, (v, ln) in d.items():
            if ln is None or ln <= 0 or v is None:
                fuera.append((ent, anio, m, "sin dato")); continue
            p = 100.0 * v / ln
            if not (0 < p <= 100):
                fuera.append((ent, anio, m, f"fuera de (0,100]: {p:.4f}")); continue
            y[(ent, anio, m)] = p
    return y, fuera

def universo(P):
    """Municipios presentes en TODAS las elecciones de la serie de su entidad."""
    univ, perdidos = {}, {}
    for ent, anios in SERIES.items():
        conj = [set(P[(ent, a)]) for a in anios]
        comun = set.intersection(*conj)
        univ[ent] = comun
        perdidos[ent] = sorted(set.union(*conj) - comun)
    return univ, perdidos

def transiciones(y, univ):
    T = []
    for ent, anios in SERIES.items():
        for a, b in zip(anios, anios[1:]):
            dD = D[(ent, b)] - D[(ent, a)]
            for m in sorted(univ[ent]):
                if (ent, a, m) in y and (ent, b, m) in y:
                    T.append({"entidad": ent, "de": a, "a": b, "municipio": m,
                              "dy": y[(ent, b, m)] - y[(ent, a, m)],
                              "hueco": b - a, "dD": dD,
                              "y0": y[(ent, a, m)], "y1": y[(ent, b, m)]})
    return T

# ------------------------------------------------------------------ estimacion
def ols(T):
    """Dy = gamma*hueco + beta*dD, sin intercepto (hueco=0 => Dy=0)."""
    sxx = syy = sxy = sxd = syd = sdd = 0.0
    for t in T:
        h, d, dy = t["hueco"], t["dD"], t["dy"]
        sxx += h * h; sdd += d * d; sxd += h * d; sxy += h * dy; syd += d * dy
    det = sxx * sdd - sxd * sxd
    if abs(det) < 1e-12: return None, None
    gamma = (sdd * sxy - sxd * syd) / det
    beta = (sxx * syd - sxd * sxy) / det
    return gamma, beta

def wild_cluster(T, B=B, seed=SEED):
    """Bootstrap wild cluster (Rademacher) sobre ENTIDADES, restringido bajo H0
    de beta=0 (Cameron-Gelbach-Miller): la referencia correcta con pocos grupos."""
    rnd = random.Random(seed)
    g0, b0 = ols(T)
    # residuos bajo H0: beta = 0
    sxx = sum(t["hueco"] ** 2 for t in T); sxy = sum(t["hueco"] * t["dy"] for t in T)
    g_h0 = sxy / sxx
    res = [t["dy"] - g_h0 * t["hueco"] for t in T]
    ents = sorted({t["entidad"] for t in T})
    betas = []
    for _ in range(B):
        s = {e: (1.0 if rnd.random() < 0.5 else -1.0) for e in ents}
        Tb = [dict(t, dy=g_h0 * t["hueco"] + s[t["entidad"]] * r) for t, r in zip(T, res)]
        gb, bb = ols(Tb)
        if bb is not None: betas.append(bb)
    betas.sort()
    lo = betas[int(0.025 * len(betas))]; hi = betas[int(0.975 * len(betas)) - 1]
    p = sum(1 for x in betas if abs(x) >= abs(b0)) / len(betas)
    # IC por inversion: b0 +- cuantiles de la distribucion bajo H0
    return {"beta": b0, "gamma": g0,
            "ic95_wild_cluster": [b0 - hi, b0 - lo],
            "p_wild_cluster": p, "B": len(betas)}

def boot_municipio(T, B=B, seed=SEED):
    rnd = random.Random(seed)
    n = len(T); bs = []
    for _ in range(B):
        Tb = [T[rnd.randrange(n)] for _ in range(n)]
        g, b = ols(Tb)
        if b is not None: bs.append(b)
    bs.sort()
    return [bs[int(0.025 * len(bs))], bs[int(0.975 * len(bs)) - 1]]

def att_por_cohorte(T):
    """ATT(g) = media de Dy en la transicion SWITCH-ON de la cohorte, menos
    gamma_hat * hueco, con gamma_hat estimada SOLO de las transiciones dD=0."""
    ctrl = [t for t in T if t["dD"] == 0]
    gamma = sum(t["dy"] for t in ctrl) / sum(t["hueco"] for t in ctrl)
    out = {"gamma_solo_controles_pp_por_anio": gamma,
           "n_transiciones_control": len(ctrl)}
    for t0 in sorted({(t["entidad"], t["de"], t["a"]) for t in T if t["dD"] == 1}):
        ent, a, b = t0
        sub = [t for t in T if t["dD"] == 1 and t["entidad"] == ent and t["de"] == a]
        media = sum(t["dy"] for t in sub) / len(sub)
        out[f"ATT_{ent}_{a}_{b}"] = {"delta_bruto_pp": media, "hueco": b - a,
                                     "att_pp": media - gamma * (b - a), "n": len(sub)}
    return out

def cuantil(v, q):
    v = sorted(v); return v[min(len(v) - 1, max(0, int(q * len(v))))]

# ----------------------------------------------------------------------- main
def main():
    P, ctrl = panel()
    y, fuera_rango = participacion(P)
    univ, perdidos = universo(P)
    T = transiciones(y, univ)
    res = wild_cluster(T)
    res["ic95_bootstrap_municipio"] = boot_municipio(T)
    res["n_transiciones"] = len(T)
    res["n_municipios_por_entidad"] = {e: len(univ[e]) for e in univ}
    res["municipios_perdidos"] = perdidos
    res["fuera_de_rango"] = fuera_rango
    res["controles_lectura"] = ctrl
    res["att_por_cohorte"] = att_por_cohorte(T)

    # resumen por transicion
    res["por_transicion"] = []
    for ent, anios in SERIES.items():
        for a, b in zip(anios, anios[1:]):
            sub = [t for t in T if t["entidad"] == ent and t["de"] == a]
            if not sub: continue
            res["por_transicion"].append({
                "entidad": ent, "de": a, "a": b, "hueco": b - a, "dD": sub[0]["dD"],
                "n": len(sub),
                "y_de_media": sum(t["y0"] for t in sub) / len(sub),
                "y_a_media": sum(t["y1"] for t in sub) / len(sub),
                "dy_media": sum(t["dy"] for t in sub) / len(sub),
                "dy_mediana": cuantil([t["dy"] for t in sub], 0.5)})

    # heterogeneidad por tamano (terciles de lista nominal en la primera eleccion)
    tam = {}
    for ent, anios in SERIES.items():
        base = P[(ent, anios[0])]
        for m in univ[ent]: tam[(ent, m)] = base[m][1]
    vals = sorted(tam.values()); q1 = cuantil(vals, 1/3); q2 = cuantil(vals, 2/3)
    res["heterogeneidad_tamano"] = {}
    for nom, cond in (("chico", lambda v: v <= q1), ("mediano", lambda v: q1 < v <= q2),
                      ("grande", lambda v: v > q2)):
        Ts = [t for t in T if cond(tam[(t["entidad"], t["municipio"])])]
        g, b = ols(Ts)
        res["heterogeneidad_tamano"][nom] = {"n": len(Ts), "beta_pp": b, "gamma": g,
                                             "corte_ln": [q1, q2]}

    # sensibilidad: fuera la transicion de hueco 1
    Ts = [t for t in T if t["hueco"] != 1]
    g, b = ols(Ts)
    res["sensibilidad_sin_hueco1"] = {"beta_pp": b, "gamma": g, "n": len(Ts)}
    Ts = [t for t in T if t["entidad"] != "Durango"]
    g, b = ols(Ts)
    res["sensibilidad_sin_durango"] = {"beta_pp": b, "gamma": g, "n": len(Ts)}

    # agregados estatales (suma de votos / suma de lista nominal), para lectura
    res["agregado_estatal"] = []
    for (ent, anio), d in sorted(P.items()):
        v = sum(x[0] for x in d.values()); l = sum(x[1] for x in d.values())
        res["agregado_estatal"].append({"entidad": ent, "anio": anio, "n": len(d),
                                        "votos": v, "lista_nominal": l,
                                        "participacion_agregada_pp": 100.0 * v / l,
                                        "D": D[(ent, anio)]})

    # lectura 1.7.3: el ciclo presidencial/intermedia con la concurrencia FIJA
    res["ciclo_con_concurrencia_fija"] = [
        {"entidad": t["entidad"], "de": t["de"], "a": t["a"], "dy_media_pp": t["dy_media"],
         "lectura": "las dos elecciones son concurrentes (dD=0): el cambio NO puede ser concurrencia"}
        for t in res["por_transicion"] if t["dD"] == 0
        and D[(t["entidad"], t["de"])] == 1 and D[(t["entidad"], t["a"])] == 1]

    # descomposicion del Delta de MAESTRA34-L4 (+10.4790 pp, 2023 -> 2024)
    res["descomposicion_L4"] = {
        "delta_L4_pp": 10.4790,
        "delta_2021_2024_concurrencia_fija": {t["entidad"]: t["dy_media"]
            for t in res["por_transicion"]
            if t["de"] == 2021 and t["a"] == 2024 and t["dD"] == 0}}
    print(json.dumps(res, ensure_ascii=False, indent=1, default=str))

if __name__ == "__main__":
    main()
