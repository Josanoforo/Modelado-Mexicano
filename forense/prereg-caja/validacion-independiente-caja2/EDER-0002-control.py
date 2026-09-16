#!/usr/bin/env python3
"""
Independent blind re-derivation of CALC-EDER-0002 (A-P, B-P, CIs).

Written from scratch based ONLY on the frozen contract in:
  data/corrida0/CALC-EDER-0002/spec.yaml
  data/corrida0/CALC-EDER-0002/spec.md
  forense/prereg-caja/EDER-CORRESIDENCIA-ACTUAL-DISENO-spec-v1_0.md

No sealed result file (resultados.json / sello.json / medidor.py) was read
before this script produced its own numbers.

Estimand: among EDER-2017 respondents aged 20-54 (in historiavida.csv) whose
own parentesco is Jefe(1) or Conyuge(2), in a vivienda with non-blank
tipo_adqui and finite positive `factor`: the weighted proportion that today
co-reside with an ascendant (parentesco 6) or a parent-in-law (parentesco 7),
reading the FULL household roster of persona.csv, with the 6/7 meaning
inverted depending on whether ego is Jefe or Conyuge.
"""
import zipfile
import io
import numpy as np
import pandas as pd

ZIP_PATH = "/home/pc0/mm-corpus/raw/eder2017/eder2017_bases_csv.zip"
SEED = 12345          # own choice; spec's 2000/20260914 not required to be matched
N_BOOT = 2000
Z95 = 1.959964

def read_member(z, name):
    with z.open(name) as f:
        raw = f.read()
    df = pd.read_csv(io.BytesIO(raw), encoding="latin-1", low_memory=False)
    # resolve BOM'd first column by suffix, as spec instructs
    df.columns = [c.split("ï»¿")[-1] if "ï»¿" in c else c for c in df.columns]
    df.columns = [c.lstrip("﻿") for c in df.columns]
    return df

def to_key_str(s):
    return s.astype(str).str.strip()

def main():
    z = zipfile.ZipFile(ZIP_PATH)
    members = z.namelist()
    print("ZIP members:", members)

    persona = read_member(z, "persona.csv")
    vivienda = read_member(z, "vivienda.csv")
    historiavida = read_member(z, "historiavida.csv")
    antecedentes = read_member(z, "antecedentes.csv")

    print("\n--- structural counts ---")
    print("G-N-MIEMBROS-ZIP:", len(members))
    print("G-N-COLUMNAS-VIVIENDA:", vivienda.shape[1])
    print("G-N-COLUMNAS-PERSONA:", persona.shape[1])
    print("G-N-COLUMNAS-HISTORIAVIDA:", historiavida.shape[1])
    print("G-N-COLUMNAS-ANTECEDENTES:", antecedentes.shape[1])
    print("G-N-FILAS-VIVIENDA:", len(vivienda))
    print("G-N-FILAS-PERSONA:", len(persona))
    print("G-N-FILAS-HISTORIAVIDA:", len(historiavida))
    print("G-N-FILAS-ANTECEDENTES:", len(antecedentes))

    # --- keys as opaque strings ---
    for df in (persona, vivienda, historiavida, antecedentes):
        assert "folioviv" in df.columns, df.columns.tolist()
    persona["folioviv"] = to_key_str(persona["folioviv"])
    persona["foliohog"] = to_key_str(persona["foliohog"])
    persona["id_pobla"] = to_key_str(persona["id_pobla"])
    persona["parentesco"] = to_key_str(persona["parentesco"])

    historiavida["folioviv"] = to_key_str(historiavida["folioviv"])
    historiavida["foliohog"] = to_key_str(historiavida["foliohog"])
    historiavida["id_pobla"] = to_key_str(historiavida["id_pobla"])

    antecedentes["folioviv"] = to_key_str(antecedentes["folioviv"])
    antecedentes["foliohog"] = to_key_str(antecedentes["foliohog"])
    antecedentes["id_pobla"] = to_key_str(antecedentes["id_pobla"])

    vivienda["folioviv"] = to_key_str(vivienda["folioviv"])
    vivienda["est_dis"] = to_key_str(vivienda["est_dis"])
    vivienda["upm"] = to_key_str(vivienda["upm"])

    # distinct triples in historiavida = EDER respondent universe (20-54)
    hv_triples = set(zip(historiavida["folioviv"], historiavida["foliohog"], historiavida["id_pobla"]))
    print("G-N-PERSONAS-HISTORIAVIDA (distinct triples):", len(hv_triples))

    # uniqueness checks
    viv_dupe = vivienda["folioviv"].duplicated().any()
    persona_triple = list(zip(persona["folioviv"], persona["foliohog"], persona["id_pobla"]))
    persona_dupe = pd.Series(persona_triple).duplicated().any()
    print("G-LLAVE-VIVIENDA-FOLIOVIV-UNICA:", "NO" if viv_dupe else "SI")
    print("G-LLAVE-PERSONA-TERNA-UNICA:", "NO" if persona_dupe else "SI")

    # --- vivienda universe filter: tipo_adqui not null/blank ---
    tipo_adqui_raw = vivienda["tipo_adqui"].astype(str)
    tipo_adqui_blank = vivienda["tipo_adqui"].isna() | (tipo_adqui_raw.str.strip() == "") | (tipo_adqui_raw.str.strip().str.lower() == "nan")
    vivienda_universo = vivienda[~tipo_adqui_blank].copy()
    print("A-N-VIVIENDAS-TIPO-ADQUI-NO-BLANCO:", len(vivienda_universo))
    print("A-N-VIVIENDAS-EXCLUIDAS-TIPO-ADQUI-BLANCO:", int(tipo_adqui_blank.sum()))

    # factor finite > 0 on vivienda universe (indexed by folioviv)
    factor_num = pd.to_numeric(vivienda_universo["factor"], errors="coerce")
    factor_ok = np.isfinite(factor_num) & (factor_num > 0)
    # map folioviv -> factor (only rows with ok factor go into the weight map;
    # since folioviv is unique in vivienda, a simple map suffices)
    factor_map = dict(zip(vivienda_universo.loc[factor_ok, "folioviv"], factor_num[factor_ok]))
    estdis_map = dict(zip(vivienda_universo["folioviv"], vivienda_universo["est_dis"]))
    upm_map = dict(zip(vivienda_universo["folioviv"], vivienda_universo["upm"]))

    # --- per-household roster flags over FULL persona.csv ---
    grp = persona.groupby(["folioviv", "foliohog"])["parentesco"]
    hay6 = grp.apply(lambda s: (s == "6").any())
    hay7 = grp.apply(lambda s: (s == "7").any())
    hay6.name = "hay6"
    hay7.name = "hay7"
    hogar_flags = pd.concat([hay6, hay7], axis=1).reset_index()

    parentesco_catalog = set(str(i) for i in range(1, 10))
    fuera_catalogo = (~persona["parentesco"].isin(parentesco_catalog)).sum()
    print("G-N-PARENTESCO-FUERA-DE-CATALOGO:", int(fuera_catalogo))

    # --- ego candidates: triple in historiavida AND parentesco in {1,2} ---
    persona["_triple"] = list(zip(persona["folioviv"], persona["foliohog"], persona["id_pobla"]))
    in_eder = persona["_triple"].isin(hv_triples)
    print("A-N-PERSONAS-ROSTER-EN-EDER:", int(in_eder.sum()))

    ego = persona[in_eder & persona["parentesco"].isin(["1", "2"])].copy()
    print("A-N-EGO-JEFE-O-CONYUGE:", len(ego))
    print("A-N-EGO-JEFE:", int((ego["parentesco"] == "1").sum()))
    print("A-N-EGO-CONYUGE:", int((ego["parentesco"] == "2").sum()))

    ego = ego.merge(hogar_flags, on=["folioviv", "foliohog"], how="left")

    jefe_mask = ego["parentesco"] == "1"
    conyuge_mask = ego["parentesco"] == "2"
    # jefe: ascendant=hay6, suegro=hay7 ; conyuge: ascendant=hay7 (inverted), suegro=hay6 (inverted)
    ascendiente = np.where(jefe_mask, ego["hay6"], ego["hay7"])
    suegro = np.where(jefe_mask, ego["hay7"], ego["hay6"])
    d = (ascendiente.astype(bool) | suegro.astype(bool)).astype(int)
    ego["d"] = d
    print("A-N-EGO-CON-ASCENDIENTE:", int(ascendiente.astype(bool).sum()))
    print("A-N-EGO-CON-SUEGRO:", int(suegro.astype(bool).sum()))

    # weight = factor from vivienda universe map; ego without weight -> dropped, counted
    ego["factor_w"] = ego["folioviv"].map(factor_map)
    sin_ponderador = ego["factor_w"].isna().sum()
    print("A-N-SIN-PONDERADOR:", int(sin_ponderador))

    U_A = ego[ego["factor_w"].notna()].copy()
    n_u = len(U_A)
    print("A-N-U:", n_u)

    embudo = {
        "n_filas_persona": len(persona),
        "n_personas_historiavida": len(hv_triples),
        "n_ego_jefe_o_conyuge": int((in_eder & persona["parentesco"].isin(["1", "2"])).sum()),
        "n_u": n_u,
    }
    expected = {"n_filas_persona": 94101, "n_personas_historiavida": 23831,
                "n_ego_jefe_o_conyuge": 16687, "n_u": 9397}
    print("A-EMBUDO-C1 observed:", embudo, "expected:", expected,
          "-> ", "EMBUDO-COINCIDE" if embudo == expected else "EMBUDO-DISCORDA")

    print("A-N-D-UNO:", int((U_A["d"] == 1).sum()))
    print("A-N-D-CERO:", int((U_A["d"] == 0).sum()))

    U_A["est_dis"] = U_A["folioviv"].map(estdis_map)
    U_A["upm"] = U_A["folioviv"].map(upm_map)
    sin_diseno = U_A["est_dis"].isna().sum() + 0  # counted separately below properly
    sin_diseno = (U_A["est_dis"].isna() | U_A["upm"].isna()).sum()
    print("A-N-SIN-DISENO:", int(sin_diseno))

    w = U_A["factor_w"].to_numpy(dtype=float)
    dvec = U_A["d"].to_numpy(dtype=float)
    A_P = (w * dvec).sum() / w.sum()
    A_P_COMP = (w * (1 - dvec)).sum() / w.sum()
    print("A-MASA-FACTOR-U:", w.sum())
    print("A-P:", A_P)
    print("A-P-COMPLEMENTO:", A_P_COMP)
    print("A-SUMA:", A_P + A_P_COMP)

    A_delta_gen1 = A_P - 0.057531
    print("A-DELTA-VS-GEN1:", A_delta_gen1, "-> REPRODUCE" if abs(A_delta_gen1) <= 1e-6 else "-> NO-REPRODUCE")
    print("A-DELTA-N-VS-GEN1:", n_u - 9397)

    # --- design: estratos/upm counts on U_A with design ---
    U_A_des = U_A.dropna(subset=["est_dis", "upm"])
    n_estratos = U_A_des["est_dis"].nunique()
    upm_pairs = U_A_des[["est_dis", "upm"]].drop_duplicates()
    n_upm = len(upm_pairs)
    estrato_upm_counts = upm_pairs.groupby("est_dis").size()
    n_estratos_upm_unica = int((estrato_upm_counts == 1).sum())
    print("A-N-ESTRATOS:", n_estratos)
    print("A-N-UPM:", n_upm)
    print("A-N-ESTRATOS-UPM-UNICA:", n_estratos_upm_unica)

    # --- bootstrap CI: resample UPM w/ replacement within estrato, same count/stratum ---
    def bootstrap_ci(df_des, weight_col, d_col, n_boot, seed):
        rng = np.random.Generator(np.random.PCG64(seed))
        # build stratum -> list of upm ids (unique, one draw unit per upm)
        strat_to_upms = df_des.groupby("est_dis")["upm"].unique().to_dict()
        # pre-index rows by (est_dis,upm) for fast lookup
        grouped = df_des.groupby(["est_dis", "upm"])
        group_keys = list(grouped.groups.keys())
        group_w = {k: grouped.get_group(k)[weight_col].to_numpy(dtype=float) for k in group_keys}
        group_d = {k: grouped.get_group(k)[d_col].to_numpy(dtype=float) for k in group_keys}

        estimates = np.empty(n_boot)
        strata = list(strat_to_upms.keys())
        for b in range(n_boot):
            num = 0.0
            den = 0.0
            for est in strata:
                upms = strat_to_upms[est]
                m = len(upms)
                if m == 1:
                    chosen = upms  # resamples itself
                else:
                    idx = rng.integers(0, m, size=m)
                    chosen = upms[idx]
                for u in chosen:
                    key = (est, u)
                    wv = group_w[key]
                    dv = group_d[key]
                    num += (wv * dv).sum()
                    den += wv.sum()
            estimates[b] = num / den if den > 0 else np.nan
        lo, hi = np.nanpercentile(estimates, [2.5, 97.5])
        return lo, hi, estimates

    A_lo, A_hi, A_est = bootstrap_ci(U_A_des, "factor_w", "d", N_BOOT, SEED)
    print(f"A-IC-LO: {A_lo}, A-IC-HI: {A_hi} (bootstrap, {N_BOOT} reps, seed={SEED})")
    print("A-METODO-IC:", "IC-CON-ESTRATOS-DE-UPM-UNICA" if n_estratos_upm_unica > 0 else "IC-BOOTSTRAP-UPM-EN-ESTRATO")

    # --- Taylor linearization SE (secondary, simple ratio-mean variance approx) ---
    def taylor_se(df_des, weight_col, d_col):
        # standard ratio-estimator Taylor SE for a weighted mean under
        # stratified clustered design; lonely.psu="adjust" -> treat single-UPM
        # stratum's contribution to variance as 0 (no crash / drop).
        p_hat = (df_des[weight_col] * df_des[d_col]).sum() / df_des[weight_col].sum()
        W = df_des[weight_col].sum()
        var = 0.0
        for est, g in df_des.groupby("est_dis"):
            upms = g["upm"].unique()
            if len(upms) < 2:
                continue  # adjust: contributes 0 variance
            cluster_tot_e = []  # per-UPM: sum(w*(d - p_hat))
            for u in upms:
                gu = g[g["upm"] == u]
                cluster_tot_e.append((gu[weight_col] * (gu[d_col] - p_hat)).sum())
            cluster_tot_e = np.array(cluster_tot_e)
            n_h = len(cluster_tot_e)
            mean_e = cluster_tot_e.mean()
            var += (n_h / (n_h - 1)) * ((cluster_tot_e - mean_e) ** 2).sum()
        var = var / (W ** 2)
        return np.sqrt(var)

    A_se = taylor_se(U_A_des, "factor_w", "d")
    print("A-EE-TAYLOR:", A_se)
    print("A-IC-LO-TAYLOR:", A_P - Z95 * A_se, "A-IC-HI-TAYLOR:", A_P + Z95 * A_se)

    A_adopcion_delta = round(A_P, 6) - 0.057531
    print("A-ADOPCION-DELTA:", A_adopcion_delta)
    reproduce = abs(A_delta_gen1) <= 1e-6
    if reproduce:
        print("A-ADOPCION: LISTADO-PARA-MESA-REPRODUCE")
    else:
        print("A-ADOPCION: LISTADO-PARA-MESA-NO-REPRODUCE")

    # ================= B: sensitivity with factor_per =================
    ant_triple_dupe = pd.Series(list(zip(antecedentes["folioviv"], antecedentes["foliohog"], antecedentes["id_pobla"]))).duplicated().any()
    print("G-LLAVE-ANTECEDENTES-TERNA-UNICA:", "NO" if ant_triple_dupe else "SI")

    ant_map = antecedentes.set_index(["folioviv", "foliohog", "id_pobla"])["factor_per"]
    ego2 = U_A.copy()
    ego2["_triple"] = list(zip(ego2["folioviv"], ego2["foliohog"], ego2["id_pobla"]))
    fp = ego2["_triple"].map(ant_map.to_dict())
    fp_num = pd.to_numeric(fp, errors="coerce")

    sin_factor_per = fp.isna().sum()
    factor_per_cero = (fp_num == 0).sum()
    factor_per_invalido = ((~np.isfinite(fp_num)) & fp.notna()).sum() + (fp_num < 0).sum()
    # avoid double counting NaN in invalido: only count non-null, non-finite/negative
    factor_per_invalido = int(((fp.notna()) & ((~np.isfinite(fp_num.fillna(np.nan))) | (fp_num < 0)) & (fp_num != 0)).sum())

    print("B-N-SIN-FACTOR-PER:", int(sin_factor_per))
    print("B-N-FACTOR-PER-CERO:", int(factor_per_cero))
    print("B-N-FACTOR-PER-INVALIDO:", factor_per_invalido)

    fp_ok = fp.notna() & (fp_num > 0) & np.isfinite(fp_num)
    U_B = ego2[fp_ok].copy()
    U_B["factor_per_w"] = fp_num[fp_ok]
    n_u_b = len(U_B)
    print("B-N-U:", n_u_b)

    U_B_des = U_B.dropna(subset=["est_dis", "upm"])
    sin_diseno_b = (U_B["est_dis"].isna() | U_B["upm"].isna()).sum()
    print("B-N-SIN-DISENO:", int(sin_diseno_b))

    wb = U_B["factor_per_w"].to_numpy(dtype=float)
    dbv = U_B["d"].to_numpy(dtype=float)
    B_P = (wb * dbv).sum() / wb.sum()
    print("B-MASA-FACTOR-PER-U:", wb.sum())
    print("B-P:", B_P)

    n_estratos_b = U_B_des["est_dis"].nunique()
    upm_pairs_b = U_B_des[["est_dis", "upm"]].drop_duplicates()
    n_upm_b = len(upm_pairs_b)
    estrato_upm_counts_b = upm_pairs_b.groupby("est_dis").size()
    n_estratos_upm_unica_b = int((estrato_upm_counts_b == 1).sum())
    print("B-N-ESTRATOS:", n_estratos_b)
    print("B-N-UPM:", n_upm_b)
    print("B-N-ESTRATOS-UPM-UNICA:", n_estratos_upm_unica_b)

    B_lo, B_hi, B_est = bootstrap_ci(U_B_des, "factor_per_w", "d", N_BOOT, SEED + 1)
    print(f"B-IC-LO: {B_lo}, B-IC-HI: {B_hi}")
    print("B-METODO-IC:", "IC-CON-ESTRATOS-DE-UPM-UNICA" if n_estratos_upm_unica_b > 0 else "IC-BOOTSTRAP-UPM-EN-ESTRATO")

    B_se = taylor_se(U_B_des, "factor_per_w", "d")
    print("B-EE-TAYLOR:", B_se)
    print("B-IC-LO-TAYLOR:", B_P - Z95 * B_se, "B-IC-HI-TAYLOR:", B_P + Z95 * B_se)

    print("B-DELTA-VS-A:", B_P - A_P)


if __name__ == "__main__":
    main()
