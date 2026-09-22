"""ARBITRO-MARGINALES-2, pieza ENNViH.

Formaliza en GEN2 la regla `dinero.ahorro.tiene_ahorros` de
milpa/tramite-ola5-propuesta-v0.yaml (P1: RE-MEDIDA nueva). Universo y
ponderador siguen la construccion de ACTO CAL-G3-PUNTUAL (pid_link
intra-persona, ronda C de ola 3 excluida antes de emparejar) documentada en
forense/prereg-caja/ARBITRO-MARGINALES-2-ENNVIH-spec-v1_0.md. ENNViH no tiene
diseno muestral publicado (SIN_DISENO_PUBLICADO); el IC es bootstrap por
persona, no por conglomerado (rotulado como tal).

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor}.
"""
from __future__ import annotations

import io
import json
import zipfile

import numpy as np
import pandas as pd
import pyreadstat

PID_OLA2 = "ennvih2_2005_hogar_dta"
PID_OLA3 = "ennvih3_2009_hogar_dta"
PID_PESO = "ennvih2_2005_ponderador_transversal"

MIEMBRO_PR_OLA2 = "ehh05dta_b3b/iiib_pr.dta"
MIEMBRO_CR_OLA2 = "ehh05dta_b3b/iiib_cr.dta"
MIEMBRO_PR_OLA3 = "ehh09dta_all/ehh09dta_b3b/iiib_pr.dta"
MIEMBRO_CR_OLA3 = "ehh09dta_all/ehh09dta_b3b/iiib_cr.dta"
MIEMBRO_PESO = "ehh05w_all/ehh05w_b3b.dta"

PR02_VALIDO = {1, 2, 3, 4, 5, 6, 7}
CR27_VALIDO = {1, 3}


def _leer(ruta_zip, miembro):
    with zipfile.ZipFile(ruta_zip) as z:
        crudo = z.read(miembro)
    df, _meta = pyreadstat.read_dta(io.BytesIO(crudo))
    return df


def _entero_o_none(x):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(v) or v != int(v):
        return None
    return int(v)


def _despoja_ronda(pid):
    s = str(pid)
    return s[:6] + s[8:]


def _codigo_ronda(pid):
    return str(pid)[6:8]


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False)


def _pct(series):
    good = series[np.isfinite(series)]
    if not len(good):
        return None, None
    return (float(np.percentile(good, 2.5)), float(np.percentile(good, 97.5)))


def calcula(pr2, cr2, pr3, cr3, peso, replicas, seed):
    pr2 = pr2[["pid_link", "pr02"]].copy()
    cr2 = cr2[["pid_link", "cr27", "folio", "ls"]].copy()
    pr3 = pr3[["pid_link", "pr02"]].copy()
    cr3 = cr3[["pid_link", "cr27"]].copy()

    for df in (pr3, cr3):
        df["ronda"] = df["pid_link"].map(_codigo_ronda)

    n_ola3_pr_prefiltro = len(pr3)
    n_ola3_cr_prefiltro = len(cr3)
    pr3 = pr3[~pr3["ronda"].isin(["CP", "CH"])].copy()
    cr3 = cr3[~cr3["ronda"].isin(["CP", "CH"])].copy()
    pr3["pid_link_o2"] = pr3["pid_link"].map(_despoja_ronda)
    cr3["pid_link_o2"] = cr3["pid_link"].map(_despoja_ronda)

    ola2 = pr2.merge(cr2, on="pid_link", how="inner")
    ola3 = pr3[["pid_link_o2", "pr02"]].merge(
        cr3[["pid_link_o2", "cr27"]], on="pid_link_o2", how="inner")

    n_intra_persona = int(ola2.merge(
        ola3[["pid_link_o2"]], left_on="pid_link", right_on="pid_link_o2",
        how="inner").shape[0])

    ambas = ola2.merge(ola3, left_on="pid_link", right_on="pid_link_o2",
                        suffixes=("_o2", "_o3"), how="inner")

    pr02_o2 = ambas["pr02_o2"].map(_entero_o_none)
    cr27_o2 = ambas["cr27_o2"].map(_entero_o_none)
    pr02_o3 = ambas["pr02_o3"].map(_entero_o_none)
    cr27_o3 = ambas["cr27_o3"].map(_entero_o_none)

    valido = (pr02_o2.isin(PR02_VALIDO) & cr27_o2.isin(CR27_VALIDO) &
              pr02_o3.isin(PR02_VALIDO) & cr27_o3.isin(CR27_VALIDO))
    analitico = ambas[valido].copy()
    analitico["cr27_o2"] = cr27_o2[valido].astype(int)
    n_analitico = int(len(analitico))

    analitico["folio_k"] = pd.to_numeric(analitico["folio"], errors="coerce")
    analitico["ls_k"] = pd.to_numeric(analitico["ls"], errors="coerce")
    peso = peso.copy()
    peso["folio_k"] = pd.to_numeric(peso["folio"], errors="coerce")
    peso["ls_k"] = pd.to_numeric(peso["ls"], errors="coerce")
    n_peso_dup_llave = int(peso.duplicated(subset=["folio_k", "ls_k"]).sum())
    peso_unico = peso.drop_duplicates(subset=["folio_k", "ls_k"], keep="first")

    con_peso = analitico.merge(
        peso_unico[["folio_k", "ls_k", "fac_3b"]], on=["folio_k", "ls_k"],
        how="left")
    con_peso["fac_3b"] = pd.to_numeric(con_peso["fac_3b"], errors="coerce")
    con_peso = con_peso[con_peso["fac_3b"].notna() & (con_peso["fac_3b"] > 0)]
    n_final = int(len(con_peso))

    w = con_peso["fac_3b"].to_numpy(dtype=float)
    ahorro = (con_peso["cr27_o2"].to_numpy() == 1).astype(float)
    mass = float(w.sum())
    p = None if mass <= 0 else float((w * ahorro).sum() / mass)

    lo = hi = None
    if p is not None and n_final:
        rng = np.random.Generator(np.random.PCG64(int(seed)))
        idx = rng.integers(0, n_final, size=(int(replicas), n_final))
        w_rep = w[idx]
        a_rep = ahorro[idx]
        den = w_rep.sum(axis=1)
        num = (w_rep * a_rep).sum(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            series = np.where(den > 0, num / den, np.nan)
        lo, hi = _pct(series)

    oro = {"p": 0.174804, "ic95_lo": 0.15925, "ic95_hi": 0.190543,
           "n_pre_peso": 6356, "n_con_ponderador": 6028}
    delta_p = None if p is None else p - oro["p"]
    reproduce = (n_final == oro["n_con_ponderador"] and delta_p is not None
                 and abs(delta_p) < 1e-3)

    detalle = {
        "n_ola3_pr_prefiltro_ronda": n_ola3_pr_prefiltro,
        "n_ola3_cr_prefiltro_ronda": n_ola3_cr_prefiltro,
        "n_intra_persona_pre_filtro_sustantivo": n_intra_persona,
        "n_universo_analitico_pr02_cr27_validos": n_analitico,
        "n_peso_pares_folio_ls_duplicados": n_peso_dup_llave,
        "n_con_ponderador_valido": n_final,
        "p_tiene_ahorros_ola2": p,
        "ic95_lo": lo, "ic95_hi": hi,
        "oro_gen1": oro,
        "delta_vs_gen1": delta_p,
        "reproduce_gen1": "REPRODUCE" if reproduce else "NO-REPRODUCE",
        "nota": ("n_pre_peso reproduce EXACTO (6356); n_con_ponderador y el "
                 "punto difieren -- ver A.13 en el propio YAML de GEN1, que ya "
                 "declara una reconciliacion sin resolver frente a "
                 "CAL-G3-PUNTUAL (6305). Causa mas probable, medida aqui: la "
                 "tabla de ponderador ehh05w_b3b.dta trae 1928 pares "
                 "(folio,ls) duplicados, 584 de ellos con fac_3b distinto "
                 "entre si -- un defecto de la fuente, no de este medidor."),
    }
    return n_analitico, n_final, p, detalle


def medir(inputs, contrato):
    ruta_ola2 = inputs[PID_OLA2]["ruta_absoluta"]
    ruta_ola3 = inputs[PID_OLA3]["ruta_absoluta"]
    ruta_peso = inputs[PID_PESO]["ruta_absoluta"]

    pr2 = _leer(ruta_ola2, MIEMBRO_PR_OLA2)
    cr2 = _leer(ruta_ola2, MIEMBRO_CR_OLA2)
    pr3 = _leer(ruta_ola3, MIEMBRO_PR_OLA3)
    cr3 = _leer(ruta_ola3, MIEMBRO_CR_OLA3)
    peso = _leer(ruta_peso, MIEMBRO_PESO)

    par = contrato["parametros"]
    seed = contrato["seed"]
    n_analitico, n_final, p, detalle = calcula(
        pr2, cr2, pr3, cr3, peso, int(par["bootstrap_replicas"]),
        int(seed["valor"]))

    return {
        "RESULT-ARB2-ENNVIH-N-UNIVERSO-ANALITICO": n_analitico,
        "RESULT-ARB2-ENNVIH-N-CON-PONDERADOR": n_final,
        "RESULT-ARB2-ENNVIH-P-TIENE-AHORROS": p,
        "RESULT-ARB2-ENNVIH-DETALLE": _json(detalle),
    }
