#!/usr/bin/env python3
"""
Independent (blind) re-derivation for E.2 validation of CALC-ENCIG-2023-0001-v1_1.
Written WITHOUT reading resultados.json / sello.json / medidor.py of the sealed CALC.
Author: independent second implementation, 2026-09-15.

Reads the frozen contract (spec.yaml / spec.md / ENCIG-MORDIDA-2023-spec-v1_0.md) and
computes B-P-PRE-SD and B-P-DIG-SD (weighted proportion of P8_4=1 trámite-events by
channel, SD/undeduplicated branch), plus funnel counts, join-key uniqueness checks,
and bootstrap CIs, entirely from the raw ENCIG 2023 CSV microdata.

Inputs:
  encig2023_04_sec_7.csv  (channel P7_3, weight FAC_TRA, design EST_DIS/UPM_DIS, keys)
  encig2023_05_sec_8.csv  (outcome P8_4, design, keys; NOT the weight -- FAC_P18 there
                            is a different weight on a different universe and MUST NOT
                            be used)
"""

import csv

import numpy as np
import pandas as pd

SEC7_PATH = "encig2023_04_sec_7.csv"
SEC8_PATH = "encig2023_05_sec_8.csv"

# blanco_literal per spec.yaml parametros.codificacion (v1_1's own declared fix):
# 2023's CSV export writes blanks as the literal string 'NA' (R-style export), not
# empty string or 'b'. All three count as "blank" for this contract.
BLANCO = {"", "b", "NA"}

STR_COLS_SEC7 = ["ID_TRA", "ID_PER", "ID_VIV", "N_TRA", "NT_TIPO",
                  "CVE_ENT", "UPM", "V_SEL", "R_ELE", "EST_DIS", "UPM_DIS"]
STR_COLS_SEC8 = ["ID_TRA", "ID_PER", "ID_VIV", "N_TRA", "EST_DIS", "UPM_DIS"]

USECOLS_SEC7 = STR_COLS_SEC7 + ["P7_3", "FAC_TRA"]
USECOLS_SEC8 = STR_COLS_SEC8 + ["P8_4", "FAC_P18"]

PRE_CODES = {"1"}
DIG_CODES = {"3", "4", "5"}
P73_MAP = {str(i) for i in range(1, 10)}  # 1..9
P84_MAP = {"0", "1"}

RNG_SEED = 20260915
N_BOOT = 2000


def read_raw(path, usecols):
    # keep_default_na=False + na_values=[] : pandas must NOT auto-convert the literal
    # string "NA" to NaN -- that is exactly the blank-literal fact we need to see raw.
    return pd.read_csv(
        path,
        usecols=usecols,
        dtype=str,
        keep_default_na=False,
        na_values=[],
        na_filter=False,
        encoding="utf-8",
    )


def classify_blank(series):
    """Return boolean mask: True where value is one of the blanco_literal tokens."""
    return series.isin(BLANCO)


def weighted_bootstrap_ci(df, upm_col, est_col, w_col, d_col, n_boot, seed):
    """
    Bootstrap CI: resample UPM (upm_col) with replacement WITHIN stratum (est_col),
    keeping the number of UPM per stratum fixed. A stratum with a single UPM
    re-samples itself every time (zero variance contribution from that stratum).
    Point estimator on each replicate: sum(w*d)/sum(w) over the expanded (with
    repetition) set of rows belonging to the drawn UPMs.
    """
    rng = np.random.Generator(np.random.PCG64(seed))

    # Only rows with non-missing design keys enter the bootstrap (can't resample a
    # cluster that doesn't exist); this is a judgement call, documented in the report.
    design_ok = (df[est_col] != "") & (df[upm_col] != "")
    dd = df.loc[design_ok]

    w = dd[w_col].to_numpy(dtype=float)
    d = dd[d_col].to_numpy(dtype=float)
    est = dd[est_col].to_numpy()
    upm = dd[upm_col].to_numpy()

    # group row indices by (estrato, upm)
    strata = {}
    for i, e in enumerate(est):
        strata.setdefault(e, {}).setdefault(upm[i], []).append(i)

    strata_upms = {e: list(u.keys()) for e, u in strata.items()}

    reps = np.empty(n_boot, dtype=float)
    for b in range(n_boot):
        idx_list = []
        for e, upms in strata_upms.items():
            k = len(upms)
            draw = rng.choice(upms, size=k, replace=True)
            for u in draw:
                idx_list.extend(strata[e][u])
        idx = np.array(idx_list, dtype=int)
        sw = w[idx].sum()
        reps[b] = (w[idx] * d[idx]).sum() / sw if sw > 0 else np.nan

    lo, hi = np.nanpercentile(reps, [2.5, 97.5])
    n_estratos_upm_unica = sum(1 for u in strata_upms.values() if len(u) == 1)
    return lo, hi, len(strata_upms), sum(len(u) for u in strata_upms.values()), n_estratos_upm_unica, design_ok.sum(), (~design_ok).sum()


def main():
    out = {}

    sec7 = read_raw(SEC7_PATH, USECOLS_SEC7)
    sec8 = read_raw(SEC8_PATH, USECOLS_SEC8)

    out["G-N-FILAS-SEC7"] = len(sec7)
    out["G-N-FILAS-SEC8"] = len(sec8)
    # full column count from the file header (not just the subset we usecols'd)
    with open(SEC7_PATH, newline="") as fh:
        hdr7 = next(csv.reader(fh))
    with open(SEC8_PATH, newline="") as fh:
        hdr8 = next(csv.reader(fh))
    out["G-N-COLUMNAS-SEC7"] = len([c for c in hdr7 if c != ""])
    out["G-N-COLUMNAS-SEC8"] = len([c for c in hdr8 if c != ""])

    # --- G-2: (CVE_ENT,UPM,V_SEL,R_ELE,N_TRA) unique in sec_7? (informative)
    key_decl = sec7[["CVE_ENT", "UPM", "V_SEL", "R_ELE", "N_TRA"]]
    dup_decl = key_decl.duplicated(keep=False)
    out["G-LLAVE-SEC7-DECLARADA-UNICA"] = (
        "UNICA" if not dup_decl.any()
        else f"NO-UNICA:{key_decl[dup_decl].drop_duplicates().shape[0]}/{dup_decl.sum()}"
    )

    # --- G-3: (ID_TRA, NT_TIPO) unique in sec_7? (informative)
    key_idtra_nt = sec7[["ID_TRA", "NT_TIPO"]]
    dup_idtra_nt = key_idtra_nt.duplicated(keep=False)
    out["G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA"] = (
        "UNICA" if not dup_idtra_nt.any()
        else f"NO-UNICA:{key_idtra_nt[dup_idtra_nt].drop_duplicates().shape[0]}/{dup_idtra_nt.sum()}"
    )

    # --- ID_TRA alone unique in sec_7? (context for CD branch, not a spec RESULT id
    #     but explicitly asked for by the task)
    dup_idtra_sec7 = sec7["ID_TRA"].duplicated(keep=False)
    n_idtra_repetidos_sec7 = sec7.loc[dup_idtra_sec7, "ID_TRA"].nunique()
    out["G-LLAVE-SEC7-IDTRA-UNICA"] = (
        "UNICA" if not dup_idtra_sec7.any()
        else f"NO-UNICA:{n_idtra_repetidos_sec7}/{dup_idtra_sec7.sum()}"
    )
    out["G-N-IDTRA-REPETIDOS-SEC7"] = int(n_idtra_repetidos_sec7)

    # --- G-4: ID_TRA unique in sec_8? THIS IS BLOCKING.
    dup_idtra_sec8 = sec8["ID_TRA"].duplicated(keep=False)
    idtra_sec8_unique = not dup_idtra_sec8.any()
    out["G-LLAVE-SEC8-IDTRA-UNICA"] = (
        "UNICA" if idtra_sec8_unique
        else f"NO-UNICA:{sec8.loc[dup_idtra_sec8,'ID_TRA'].nunique()}/{dup_idtra_sec8.sum()}"
    )

    if not idtra_sec8_unique:
        out["G-VEREDICTO-JOIN"] = "NO-ESTIMABLE-LLAVE-NO-UNICA"
        print_report(out, aborted=True)
        return

    # --- G-5: control key (ID_VIV,ID_PER,ID_TRA,N_TRA) vs primary key ID_TRA:
    #     does joining on the control key produce the SAME set of matched row-pairs
    #     as joining on ID_TRA alone?
    merged_primary = sec7.merge(sec8, on="ID_TRA", how="inner", suffixes=("_7", "_8"))
    merged_control = sec7.merge(
        sec8, on=["ID_VIV", "ID_PER", "ID_TRA", "N_TRA"], how="inner", suffixes=("_7", "_8")
    )
    n_primary = len(merged_primary)
    n_control = len(merged_control)
    join_exacto = (n_primary == n_control)
    out["G-JOIN-LLAVE-CONTROL-COINCIDE"] = (
        "COINCIDE" if join_exacto else f"DIFIERE:{n_primary}/{n_control}"
    )
    out["G-VEREDICTO-JOIN"] = "JOIN-EXACTO" if join_exacto else "JOIN-NO-EXACTO"

    if not join_exacto:
        print_report(out, aborted=True)
        return

    # --- raw support of P8_4 and P7_3 (before any filtering), over the full source
    #     tables (informative RESULT, not restricted to matched rows)
    p84_support = sec8["P8_4"].value_counts().to_dict()
    p73_support = sec7["P7_3"].value_counts().to_dict()
    out["G-SOPORTE-P84"] = ";".join(f"{k}:{v}" for k, v in sorted(p84_support.items()))
    out["G-SOPORTE-P73"] = ";".join(f"{k}:{v}" for k, v in sorted(p73_support.items()))

    # out-of-map guard: any P8_4 code outside {0,1,blanco}? any P7_3 outside {1..9,blanco}?
    p84_bad = set(p84_support) - P84_MAP - BLANCO
    p73_bad = set(p73_support) - P73_MAP - BLANCO
    if p84_bad:
        out["G-VEREDICTO-JOIN"] += f" | NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:P8_4({p84_bad})"
        print_report(out, aborted=True)
        return
    if p73_bad:
        out["G-VEREDICTO-JOIN"] += f" | NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:P7_3({p73_bad})"
        print_report(out, aborted=True)
        return

    # --- G-6: weight-by-file guard. FAC_TRA must come from sec_7; FAC_P18 (sec_8) unused.
    out["G-PONDERADOR-POR-ARCHIVO"] = "FAC-TRA-DE-SEC7-Y-FAC-P18-SIN-USAR"

    # --- funnel: matched vs unmatched sec_7 rows
    idtra_in_sec8 = set(sec8["ID_TRA"])
    matched_mask_sec7 = sec7["ID_TRA"].isin(idtra_in_sec8)
    n_emparejadas = int(matched_mask_sec7.sum())
    n_sec7_sin_pareja = int((~matched_mask_sec7).sum())
    out["B-N-EMPAREJADAS"] = n_emparejadas
    out["B-N-SEC7-SIN-PAREJA"] = n_sec7_sin_pareja
    out["B-COBERTURA"] = n_emparejadas / out["G-N-FILAS-SEC7"]

    # matched frame (SD: every sec_7 row kept, joined onto its single sec_8 partner)
    m = merged_primary.copy()  # already the inner join sec_7 x sec_8 on ID_TRA (SD, since sec_7 not deduped)
    assert len(m) == n_emparejadas, (len(m), n_emparejadas)

    # rename channel/outcome cols post-merge suffixing
    # EST_DIS/UPM_DIS exist in both -> suffixed _7/_8; spec says take from sec_7 side.
    m["EST_DIS_use"] = m["EST_DIS_7"]
    m["UPM_DIS_use"] = m["UPM_DIS_7"]

    # P8_4 blank/non-numeric filter
    p84_blank_mask = classify_blank(m["P8_4"])
    p84_numeric_mask = m["P8_4"].isin(P84_MAP)
    p84_valid_mask = p84_numeric_mask & ~p84_blank_mask
    n_p84_blanco = int((~p84_valid_mask).sum())
    out["B-N-P84-BLANCO"] = n_p84_blanco

    # FAC_TRA finite > 0 filter
    fac_tra_num = pd.to_numeric(m["FAC_TRA"], errors="coerce")
    fac_tra_valid_mask = fac_tra_num.notna() & np.isfinite(fac_tra_num) & (fac_tra_num > 0)
    n_sin_ponderador = int((~fac_tra_valid_mask).sum())
    out["B-N-SIN-PONDERADOR"] = n_sin_ponderador

    # universe U_B (SD)
    u_mask = p84_valid_mask & fac_tra_valid_mask
    U = m.loc[u_mask].copy()
    U["FAC_TRA_f"] = fac_tra_num[u_mask]
    U["d"] = (U["P8_4"] == "1").astype(float)
    out["B-N-U"] = len(U)
    out["B-MASA-FAC-TRA-U"] = float(U["FAC_TRA_f"].sum())

    # design-missing rows
    n_sin_diseno = int(((U["EST_DIS_use"] == "") | (U["UPM_DIS_use"] == "")).sum())
    out["B-N-SIN-DISENO"] = n_sin_diseno

    # channel classification within U_B
    p73 = U["P7_3"]
    pre_mask = p73.isin(PRE_CODES)
    dig_mask = p73.isin(DIG_CODES)
    residuo_mask = ~(pre_mask | dig_mask)
    out["B-N-RESIDUO-CANAL"] = int(residuo_mask.sum())
    residuo_w = U.loc[residuo_mask, "FAC_TRA_f"].sum()
    total_w = U["FAC_TRA_f"].sum()
    out["B-P-RESIDUO-CANAL"] = float(residuo_w / total_w) if total_w > 0 else None
    out["B-VEREDICTO-CANAL"] = (
        "DICOTOMIA-ES-PROPIEDAD-DEL-RECORTE" if out["B-N-RESIDUO-CANAL"] > 0
        else "CANAL-DICOTOMICO-EN-EL-INSTRUMENTO"
    )

    out["B-N-PRE-SD"] = int(pre_mask.sum())
    out["B-N-DIG-SD"] = int(dig_mask.sum())

    # CD branch: dedup sec_7 by ID_TRA, first row in file order, BEFORE the join
    sec7_cd = sec7.drop_duplicates(subset="ID_TRA", keep="first")
    n_events_dropped_by_dedup_from_sec7 = len(sec7) - len(sec7_cd)
    merged_cd = sec7_cd.merge(sec8, on="ID_TRA", how="inner", suffixes=("_7", "_8"))
    p84_blank_cd = classify_blank(merged_cd["P8_4"])
    p84_valid_cd = merged_cd["P8_4"].isin(P84_MAP) & ~p84_blank_cd
    fac_cd = pd.to_numeric(merged_cd["FAC_TRA"], errors="coerce")
    fac_valid_cd = fac_cd.notna() & np.isfinite(fac_cd) & (fac_cd > 0)
    U_cd = merged_cd.loc[p84_valid_cd & fac_valid_cd].copy()
    U_cd["FAC_TRA_f"] = fac_cd[p84_valid_cd & fac_valid_cd]
    U_cd["d"] = (U_cd["P8_4"] == "1").astype(float)
    pre_cd = U_cd["P7_3"].isin(PRE_CODES)
    dig_cd = U_cd["P7_3"].isin(DIG_CODES)
    out["B-N-PRE-CD"] = int(pre_cd.sum())
    out["B-N-DIG-CD"] = int(dig_cd.sum())
    n_pre_cd_w = U_cd.loc[pre_cd, "FAC_TRA_f"].sum()
    n_dig_cd_w = U_cd.loc[dig_cd, "FAC_TRA_f"].sum()
    out["B-P-PRE-CD"] = float((U_cd.loc[pre_cd, "FAC_TRA_f"] * U_cd.loc[pre_cd, "d"]).sum() / n_pre_cd_w) if n_pre_cd_w > 0 else None
    out["B-P-DIG-CD"] = float((U_cd.loc[dig_cd, "FAC_TRA_f"] * U_cd.loc[dig_cd, "d"]).sum() / n_dig_cd_w) if n_dig_cd_w > 0 else None
    # events dropped by dedup that were actually IN U_B (SD) -- rows of U_B whose ID_TRA
    # appears more than once in sec_7 minus one kept
    dup_ids_in_U = U["ID_TRA"][U["ID_TRA"].duplicated(keep=False)]
    out["B-N-EVENTOS-DESCARTADOS-POR-DEDUP"] = int(len(U) - U["ID_TRA"].nunique())

    # --- primary point estimates (SD)
    def weighted_prop(mask):
        w = U.loc[mask, "FAC_TRA_f"]
        d = U.loc[mask, "d"]
        sw = w.sum()
        return float((w * d).sum() / sw) if sw > 0 else None

    p_pre_sd = weighted_prop(pre_mask)
    p_dig_sd = weighted_prop(dig_mask)
    out["B-P-PRE-SD"] = p_pre_sd
    out["B-P-DIG-SD"] = p_dig_sd

    def weighted_prop_same_denom(numer_mask, denom_mask):
        # numerator restricted to numer_mask, denominator is the FULL channel mask
        # (matches spec: complements counted directly on d==0, same denominator as p)
        w_denom = U.loc[denom_mask, "FAC_TRA_f"]
        sw = w_denom.sum()
        w_numer = U.loc[numer_mask, "FAC_TRA_f"]
        return float(w_numer.sum() / sw) if sw > 0 else None

    p_normal_pre_sd = weighted_prop_same_denom(pre_mask & (U["d"] == 0), pre_mask)
    p_normal_dig_sd = weighted_prop_same_denom(dig_mask & (U["d"] == 0), dig_mask)
    out["B-P-NORMAL-PRE-SD"] = p_normal_pre_sd
    out["B-P-NORMAL-DIG-SD"] = p_normal_dig_sd
    out["B-SUMA-PRE-SD"] = f"SI:{abs(p_pre_sd + p_normal_pre_sd - 1.0):.2e}" if p_pre_sd is not None else "NO:sin-punto"
    out["B-SUMA-DIG-SD"] = f"SI:{abs(p_dig_sd + p_normal_dig_sd - 1.0):.2e}" if p_dig_sd is not None else "NO:sin-punto"

    out["B-DIFERENCIA-PRE-DIG-SD"] = p_pre_sd - p_dig_sd if (p_pre_sd is not None and p_dig_sd is not None) else None
    out["B-RAZON-PRE-DIG-SD"] = (p_pre_sd / p_dig_sd) if (p_pre_sd is not None and p_dig_sd and p_dig_sd != 0) else None

    # --- bootstrap CIs (design-based, UPM-in-strato resample)
    U_pre = U.loc[pre_mask]
    U_dig = U.loc[dig_mask]

    (lo_pre, hi_pre, n_est_pre, n_upm_pre, n_est_1upm_pre, n_ok_pre, n_bad_pre
     ) = weighted_bootstrap_ci(U_pre, "UPM_DIS_use", "EST_DIS_use", "FAC_TRA_f", "d", N_BOOT, RNG_SEED)
    (lo_dig, hi_dig, n_est_dig, n_upm_dig, n_est_1upm_dig, n_ok_dig, n_bad_dig
     ) = weighted_bootstrap_ci(U_dig, "UPM_DIS_use", "EST_DIS_use", "FAC_TRA_f", "d", N_BOOT + 1, RNG_SEED)

    out["B-IC-LO-PRE-SD"] = lo_pre
    out["B-IC-HI-PRE-SD"] = hi_pre
    out["B-IC-LO-DIG-SD"] = lo_dig
    out["B-IC-HI-DIG-SD"] = hi_dig
    out["B-N-ESTRATOS-PRE-SD"] = n_est_pre
    out["B-N-UPM-PRE-SD"] = n_upm_pre
    out["B-N-ESTRATOS-UPM-UNICA-PRE-SD"] = n_est_1upm_pre
    out["B-N-ESTRATOS-DIG-SD"] = n_est_dig
    out["B-N-UPM-DIG-SD"] = n_upm_dig
    out["B-N-ESTRATOS-UPM-UNICA-DIG-SD"] = n_est_1upm_dig
    out["B-METODO-IC"] = (
        "IC-CON-ESTRATOS-DE-UPM-UNICA" if (n_est_1upm_pre > 0 or n_est_1upm_dig > 0)
        else "IC-BOOTSTRAP-UPM-EN-ESTRATO"
    )

    # --- H1: direction hypothesis
    if p_pre_sd is None or p_dig_sd is None:
        out["H1-VEREDICTO"] = "H1-NO-EVALUABLE"
    else:
        out["H1-VEREDICTO"] = "H1-SOSTENIDA" if p_pre_sd > p_dig_sd else "H1-NO-SOSTENIDA"

    # --- contrast vs 2025 (values from the frozen spec.yaml itself, not from a
    #     forbidden sealed-answer file)
    REF_2025_PRE_SD = 0.1410407168724654
    REF_2025_DIG_SD = 0.029867554626649372
    out["B-DELTA-2023-VS-2025-PRE-SD"] = p_pre_sd - REF_2025_PRE_SD if p_pre_sd is not None else None
    out["B-DELTA-2023-VS-2025-DIG-SD"] = p_dig_sd - REF_2025_DIG_SD if p_dig_sd is not None else None

    out["B-VEREDICTO"] = "TASA-REPORTADA"
    out["B-ADOPCION"] = (
        "LISTADO-PARA-MESA-ESTIMABLE" if (out["B-COBERTURA"] and out["B-N-U"] > 0)
        else "NO-ADOPTABLE-NO-ESTIMABLE"
    )

    print_report(out, aborted=False)


def print_report(out, aborted):
    print("=" * 70)
    print("INDEPENDENT CONTROL RUN -- CALC-ENCIG-2023-0001-v1_1 (blind)")
    print("=" * 70)
    for k, v in out.items():
        print(f"{k}: {v}")
    if aborted:
        print("\n*** ABORTED: guard fired, no point estimate computed. ***")


if __name__ == "__main__":
    main()
