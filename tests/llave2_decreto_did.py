"""ACTO LLAVE2-DECRETO — DiD del decreto RFN 2019 sobre ENOE.

Corrida de COMMIT 2 sobre el pre-registro congelado en
forense/notas/2026-08-25-llave2-decreto-cierre.md (COMMIT 1). No re-decide
nada del diseño ahi congelado; los ajustes de mecanica de columnas medidos
aqui (mun real vs cve_mun documentado, trans_ppal no discrimina fronterizo)
se declaran en la nota de resultados, no se corrigen hacia atras.
"""
import csv
import io
import math
import zipfile
from collections import defaultdict

import numpy as np

ROOT = "."

# --- 1 · Municipios tratados (Articulo Primero del decreto, ver nota Commit 1 §1.1) ---
TRATADOS = {
    (2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
    (5, 2), (5, 12), (5, 13), (5, 14), (5, 22), (5, 23), (5, 25), (5, 38),
    (8, 5), (8, 15), (8, 28), (8, 35), (8, 37), (8, 42), (8, 52), (8, 53),
    (19, 5),
    (26, 2), (26, 4), (26, 17), (26, 19), (26, 39), (26, 43), (26, 48),
    (26, 55), (26, 59), (26, 60), (26, 70),
    (28, 7), (28, 14), (28, 15), (28, 22), (28, 24), (28, 25), (28, 27),
    (28, 32), (28, 33), (28, 40),
}
assert len(TRATADOS) == 43, len(TRATADOS)
ESTADOS_FRONTERA = {2, 5, 8, 19, 26, 28}

# --- 2 · Las 14 olas, con su zip/csv/era (ver Commit 1 §1.3-1.4) ---
# era: 'clasica' -> fac, est_d ; 'enoen' -> fac_tri, est_d_tri (mun/ent/upm/
# emp_ppal/hrsocup/ingocup/ing_x_hrs/trans_ppal identicos en las dos eras,
# medido en este acto -- el FD documenta CVE_MUN para ENOEN pero la columna
# real de la tabla exportada sigue llamandose "mun")
OLAS = [
    ("2017T1", "pre",  "data/raw/2017trim1_csv.zip", "clasica"),
    ("2017T2", "pre",  "data/raw/2017trim2_csv.zip", "clasica"),
    ("2017T3", "pre",  "data/raw/2017trim3_csv.zip", "clasica"),
    ("2017T4", "pre",  "data/raw/2017trim4_csv.zip", "clasica"),
    ("2018T1", "pre",  "data/raw/2018trim1_csv.zip", "clasica"),
    ("2018T2", "pre",  "data/raw/2018trim2_csv.zip", "clasica"),
    ("2018T3", "pre",  "data/raw/2018trim3_csv.zip", "clasica"),
    ("2018T4", "pre",  "data/raw/2018trim4_csv.zip", "clasica"),
    ("2019T2", "post", "data/raw/enoe_microdatos_post2019/2019trim2_csv.zip", "clasica"),
    ("2019T3", "post", "data/raw/enoe_microdatos_post2019/2019trim3_csv.zip", "clasica"),
    ("2019T4", "post", "data/raw/enoe_microdatos_post2019/2019trim4_csv.zip", "clasica"),
    ("2020T1", "post", "data/raw/enoe_microdatos_post2019/2020trim1_csv.zip", "clasica"),
    ("2020T3", "post", "data/raw/enoe_microdatos_post2019/enoe_n_2020_trim3_csv.zip", "enoen"),
    ("2020T4", "post", "data/raw/enoe_microdatos_post2019/enoe_n_2020_trim4_csv.zip", "enoen"),
]

FAC_COL = {"clasica": "fac", "enoen": "fac_tri"}
ESTD_COL = {"clasica": "est_d", "enoen": "est_d_tri"}


def _find_sdem_name(zf):
    for n in zf.namelist():
        if "sdemt" in n.lower():
            return n
    raise FileNotFoundError("no SDEM* en " + zf.filename)


def _to_int(s):
    s = (s or "").strip()
    if s == "":
        return None
    try:
        return int(s)
    except ValueError:
        return None


def _to_float(s):
    s = (s or "").strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def cargar_ola(ola_id, periodo, zip_path, era):
    """Lee la tabla SDEM de una ola, filtra a los 6 estados fronterizos y
    al universo de persona (§1.5 del pre-registro), regresa lista de dicts.
    """
    fac_col, estd_col = FAC_COL[era], ESTD_COL[era]
    filas = []
    n_leidas = n_estados = n_universo = 0
    with zipfile.ZipFile(zip_path) as zf:
        name = _find_sdem_name(zf)
        with zf.open(name) as f:
            txt = io.TextIOWrapper(f, encoding="latin-1")
            reader = csv.DictReader(txt)
            for row in reader:
                n_leidas += 1
                ent = _to_int(row.get("ent"))
                if ent not in ESTADOS_FRONTERA:
                    continue
                n_estados += 1
                mun = _to_int(row.get("mun"))
                emp_ppal = (row.get("emp_ppal") or "").strip()
                if mun is None or emp_ppal not in ("1", "2"):
                    continue
                n_universo += 1
                fac = _to_float(row.get(fac_col))
                upm = row.get("upm", "").strip()
                estd = row.get(estd_col, "").strip()
                ing_x_hrs = _to_float(row.get("ing_x_hrs"))
                filas.append({
                    "ola": ola_id, "periodo": periodo, "era": era,
                    "ent": ent, "mun": mun,
                    "tratado": 1 if (ent, mun) in TRATADOS else 0,
                    "fac": fac, "upm": upm, "estd": estd,
                    "emp_ppal": emp_ppal, "informal": 1 if emp_ppal == "1" else 0,
                    "ing_x_hrs": ing_x_hrs,
                    "log_wage": math.log(ing_x_hrs) if ing_x_hrs and ing_x_hrs > 0 else None,
                })
    return filas, (n_leidas, n_estados, n_universo)


def media_ponderada(filas, campo, peso="fac"):
    num = den = 0.0
    n = 0
    for r in filas:
        v = r[campo]
        w = r[peso]
        if v is None or w is None:
            continue
        num += w * v
        den += w
        n += 1
    return (num / den if den else None), den, n


def tabla_pretendencia(todas):
    print()
    print("=== Pre-tendencia (8 olas pre, media ponderada por fac) ===")
    print(f"{'ola':8s} {'log_wage_T':>11s} {'log_wage_C':>11s} {'brecha':>8s}  "
          f"{'informal_T':>11s} {'informal_C':>11s} {'brecha':>8s}")
    filas_pre = [r for r in todas if r["periodo"] == "pre"]
    olas = sorted({r["ola"] for r in filas_pre})
    out = []
    for ola in olas:
        ft = [r for r in filas_pre if r["ola"] == ola and r["tratado"] == 1]
        fc = [r for r in filas_pre if r["ola"] == ola and r["tratado"] == 0]
        lwt, _, _ = media_ponderada(ft, "log_wage")
        lwc, _, _ = media_ponderada(fc, "log_wage")
        imt, _, _ = media_ponderada(ft, "informal")
        imc, _, _ = media_ponderada(fc, "informal")
        out.append((ola, lwt, lwc, imt, imc))
        print(f"{ola:8s} {lwt:11.4f} {lwc:11.4f} {lwt-lwc:8.4f}  "
              f"{100*imt:10.2f}% {100*imc:10.2f}% {100*(imt-imc):7.2f}pp")
    return out


def wls_did(todas, outcome, cluster_key):
    """Regresion Y ~ 1 + tratado + post + tratado:post, ponderada por fac,
    con errores estandar robustos por conglomerado (sandwich CR1, con
    correccion de muestra chica al estilo Stata: (G/(G-1))*((n-1)/(n-k))).
    """
    filas = [r for r in todas if r[outcome] is not None and r["fac"] is not None]
    n = len(filas)
    X = np.empty((n, 4))
    y = np.empty(n)
    w = np.empty(n)
    clusters = []
    for i, r in enumerate(filas):
        post = 1.0 if r["periodo"] == "post" else 0.0
        trat = float(r["tratado"])
        X[i] = [1.0, trat, post, trat * post]
        y[i] = r[outcome]
        w[i] = r["fac"]
        clusters.append(cluster_key(r))

    sw = np.sqrt(w)
    Xw = X * sw[:, None]
    yw = y * sw
    XtX = Xw.T @ Xw
    XtX_inv = np.linalg.inv(XtX)
    beta = XtX_inv @ (Xw.T @ yw)
    resid = y - X @ beta  # residuo en escala original (no ponderada)

    # scores por observacion, en la parametrizacion WLS: g_i = w_i * x_i * e_i
    g = (w * resid)[:, None] * X  # (n,4)
    by_cluster = defaultdict(lambda: np.zeros(4))
    for i, c in enumerate(clusters):
        by_cluster[c] += g[i]
    G = len(by_cluster)
    meat = np.zeros((4, 4))
    for gc in by_cluster.values():
        meat += np.outer(gc, gc)
    k = X.shape[1]
    corr = (G / (G - 1)) * ((n - 1) / (n - k)) if G > 1 and n > k else float("nan")
    V = corr * (XtX_inv @ meat @ XtX_inv)
    se = np.sqrt(np.diag(V))
    return {
        "n": n, "G": G, "beta": beta, "se": se,
        "did_beta": beta[3], "did_se": se[3],
        "did_ci95": (beta[3] - 1.959963985 * se[3], beta[3] + 1.959963985 * se[3]),
    }


def reporta_did(nombre, res, umbral=None):
    lo, hi = res["did_ci95"]
    print(f"{nombre}: n={res['n']}, clusters={res['G']}, "
          f"beta_tratado x post = {res['did_beta']:+.4f}  "
          f"SE(cluster)={res['did_se']:.4f}  IC95%=({lo:+.4f}, {hi:+.4f})")
    print("  coeficientes completos [b0(intercepto) b1(tratado) b2(post) b3(tratado:post)]:")
    for nom, b, s in zip(["b0", "b1_tratado", "b2_post", "b3_did"], res["beta"], res["se"]):
        print(f"    {nom:12s} {b:+.5f}  SE={s:.5f}")
    if umbral is not None:
        if lo > -umbral and hi < umbral:
            veredicto = "dentro de (+/-umbral) en las dos direcciones"
        elif lo <= 0 <= hi:
            veredicto = "cruza cero"
        else:
            veredicto = "excluye cero"
        print(f"  umbral={umbral}: IC {veredicto}")


def main():
    todas = []
    conteos = []
    for ola_id, periodo, zip_path, era in OLAS:
        filas, c = cargar_ola(ola_id, periodo, zip_path, era)
        todas.extend(filas)
        conteos.append((ola_id, periodo, era, *c, len(filas)))
        print(f"{ola_id:8s} {periodo:5s} {era:8s} leidas={c[0]:7d} "
              f"6-estados={c[1]:6d} universo={c[2]:6d}")

    print()
    print("total filas universo (6 estados, ocupados, mun no vacio):", len(todas))
    n_trat = sum(1 for r in todas if r["tratado"] == 1)
    n_ctrl = sum(1 for r in todas if r["tratado"] == 0)
    print("tratados:", n_trat, " control:", n_ctrl)

    upm_trat = {(r["ent"], r["mun"], r["upm"]) for r in todas if r["tratado"] == 1}
    print("UPM distintas tratadas (pool pre+post):", len(upm_trat))
    mun_trat_presentes = {(r["ent"], r["mun"]) for r in todas if r["tratado"] == 1}
    print("municipios tratados con al menos 1 observacion:", len(mun_trat_presentes),
          "de 43 ->", sorted(mun_trat_presentes))
    mun_ctrl_presentes = {(r["ent"], r["mun"]) for r in todas if r["tratado"] == 0}
    print("municipios control con al menos 1 observacion:", len(mun_ctrl_presentes), "de 235")

    faltantes = sorted(TRATADOS - mun_trat_presentes)
    print("tratados SIN ninguna observacion (mun suprimido o muestra 0):", faltantes)

    tabla_pretendencia(todas)

    for outcome in ("log_wage", "informal"):
        f_ = [r for r in todas if r[outcome] is not None]
        nt = sum(1 for r in f_ if r["tratado"] == 1)
        nc = sum(1 for r in f_ if r["tratado"] == 0)
        print(f"cobertura {outcome}: N_tratado={nt}  N_control={nc}")

    print()
    print("=== DiD primario: cluster por UPM (ent,mun,upm) ===")
    res_w_upm = wls_did(todas, "log_wage", lambda r: (r["ent"], r["mun"], r["upm"]))
    reporta_did("log(ing_x_hrs)", res_w_upm, umbral=0.05)
    res_i_upm = wls_did(todas, "informal", lambda r: (r["ent"], r["mun"], r["upm"]))
    reporta_did("informal (EMP_PPAL==1)", res_i_upm, umbral=0.05)

    print()
    print("=== Sensibilidad: cluster por municipio (ent,mun) ===")
    res_w_mun = wls_did(todas, "log_wage", lambda r: (r["ent"], r["mun"]))
    reporta_did("log(ing_x_hrs)", res_w_mun, umbral=0.05)
    res_i_mun = wls_did(todas, "informal", lambda r: (r["ent"], r["mun"]))
    reporta_did("informal (EMP_PPAL==1)", res_i_mun, umbral=0.05)

    return todas, conteos, {
        "wage_upm": res_w_upm, "informal_upm": res_i_upm,
        "wage_mun": res_w_mun, "informal_mun": res_i_mun,
        "faltantes": faltantes,
    }


if __name__ == "__main__":
    main()
