#!/usr/bin/env python3
"""
Independent (blind) re-derivation of CALC-ENIF-0003 (P3 coverage reconciliation +
P4 P4_10=1 decomposition bounds), for the E.2 independent-validation check.

Written WITHOUT reading data/corrida0/CALC-ENIF-0003/{medidor.py,resultados.json,
sello.json,ejecucion.json} or any forense/notas file about the sealed answer.
Based solely on:
  - data/corrida0/CALC-ENIF-0003/spec.yaml
  - data/corrida0/CALC-ENIF-0003/spec.md
  - forense/prereg-caja/ENIF-COBERTURA-Y-P410-spec-v1_0.md
  - the raw ENIF 2024 microdata zip.
"""
import zipfile
import io
import csv
import math
import json
import numpy as np

ZIP_PATH = "/home/pc0/mm-corpus/raw/enif_2024_bd_csv.zip"
MEMBER = "TMODULO.csv"
SEED = 20260909
N_BOOT = 1000

# ---------- 1. read TMODULO.csv (utf-8-sig with fallback to latin-1, all cells as stripped strings) ----------

def read_tmodulo(zip_path, member):
    z = zipfile.ZipFile(zip_path)
    raw = z.read(member)
    try:
        text = raw.decode("utf-8-sig")
        encoding_used = "utf-8-sig"
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
        encoding_used = "latin-1"
    reader = csv.DictReader(io.StringIO(text))
    rows = [{k: (v.strip() if v is not None else "") for k, v in row.items()} for row in reader]
    return rows, encoding_used

rows, encoding_used = read_tmodulo(ZIP_PATH, MEMBER)
n_tmodulo = len(rows)


def to_float(s):
    try:
        f = float(s)
        if math.isfinite(f):
            return f
    except (ValueError, TypeError):
        pass
    return None


for r in rows:
    r["_FAC_PER_f"] = to_float(r.get("FAC_PER", ""))

fac_valid_rows = [r for r in rows if r["_FAC_PER_f"] is not None and r["_FAC_PER_f"] > 0]
n_fac_per_valido = len(fac_valid_rows)
n_sin_fac_per = n_tmodulo - n_fac_per_valido
masa_fac_per = sum(r["_FAC_PER_f"] for r in fac_valid_rows)

# ---------- domains ----------
P3_13_VALIDOS = {"1", "2", "3", "4", "5", "6", "7"}
P3_13_DOMINIO = {"1", "2", "3", "4", "5", "6", "7", "9", ""}
P4_10_VALIDOS = {"1", "2", "3", "4", "5"}
P4_10_DOMINIO = {"1", "2", "3", "4", "5", "8", "9"}

n_fuera_dominio_p3_13 = sum(1 for r in rows if r.get("P3_13", "") not in P3_13_DOMINIO)
n_fuera_dominio_p4_10 = sum(1 for r in rows if r.get("P4_10", "") not in P4_10_DOMINIO)

n_p3_13_1_7 = sum(1 for r in rows if r.get("P3_13", "") in P3_13_VALIDOS)
n_p3_13_9 = sum(1 for r in rows if r.get("P3_13", "") == "9")
n_p3_13_blanco = sum(1 for r in rows if r.get("P3_13", "") == "")

n_universo_triple = sum(
    1 for r in rows
    if r.get("P3_13", "") in P3_13_VALIDOS and r.get("P4_10", "") in P4_10_VALIDOS
)

p4_10_counts = {k: sum(1 for r in rows if r.get("P4_10", "") == k) for k in ["1", "2", "3", "4", "5", "8", "9"]}

# ---------- P3 fractions ----------
frac_1_7_np = n_p3_13_1_7 / n_tmodulo
frac_universo_triple_np = n_universo_triple / n_tmodulo

sum_fac_1_7 = sum(r["_FAC_PER_f"] for r in fac_valid_rows if r.get("P3_13", "") in P3_13_VALIDOS)
sum_fac_1_7_9 = sum(
    r["_FAC_PER_f"] for r in fac_valid_rows if r.get("P3_13", "") in (P3_13_VALIDOS | {"9"})
)
sum_fac_triple = sum(
    r["_FAC_PER_f"] for r in fac_valid_rows
    if r.get("P3_13", "") in P3_13_VALIDOS and r.get("P4_10", "") in P4_10_VALIDOS
)

frac_1_7_pond = sum_fac_1_7 / masa_fac_per
frac_1_7_9_pond = sum_fac_1_7_9 / masa_fac_per
frac_universo_triple_pond = sum_fac_triple / masa_fac_per

# ---------- veredictos mecanicos ----------
def r2(x):
    return round(100 * x, 2)


def r6(x):
    return round(x, 6)


veredicto_68_97 = "REPRODUCE" if r2(frac_1_7_np) == 68.97 else "NO-REPRODUCE"
veredicto_67_53 = "REPRODUCE" if r2(frac_1_7_pond) == 67.53 else "NO-REPRODUCE"
veredicto_68_06 = "REPRODUCE" if r2(frac_1_7_9_pond) == 68.06 else "NO-REPRODUCE"

# Build the table of the seven fractions explicitly, per spec (C-* fraction results)
tabla_siete_fracciones = {
    "FRAC-P3-13-1-7-NO-PONDERADA": frac_1_7_np,
    "FRAC-P3-13-1-7-9-NO-PONDERADA": (
        sum(1 for r in rows if r.get("P3_13", "") in (P3_13_VALIDOS | {"9"})) / n_tmodulo
    ),
    "FRAC-UNIVERSO-TRIPLE-NO-PONDERADA": frac_universo_triple_np,
    "FRAC-P3-13-1-7-PONDERADA": frac_1_7_pond,
    "FRAC-P3-13-1-7-9-PONDERADA": frac_1_7_9_pond,
    "FRAC-UNIVERSO-TRIPLE-PONDERADA": frac_universo_triple_pond,
}
# note: spec.yaml sufijos_result lists 6 C-FRAC-* ids (not 7); "siete fracciones" in estimando
# text likely counts these 6 plus the {1..7,9} no-ponderada variant implicitly referenced in
# prereg text table (which lists 7 rows total incl. C-N-P3-13-1-7 and C-N-UNIVERSO-TRIPLE as
# counts, not fractions). I use the six proportion RESULT ids in sufijos_result as "the table"
# for the 66.89 localization scan, per my own judgment (documented in report).

localizadas = [name for name, val in tabla_siete_fracciones.items() if r2(val) == 66.89]
veredicto_66_89 = ("LOCALIZADA:" + ";".join(localizadas)) if localizadas else "NO-LOCALIZADA"

if r6(frac_universo_triple_np) == 0.668937:
    veredicto_0_668937 = "REPRODUCE:NO-PONDERADA"
elif r6(frac_universo_triple_pond) == 0.668937:
    veredicto_0_668937 = "REPRODUCE:PONDERADA"
else:
    veredicto_0_668937 = "NO-REPRODUCE"

veredicto_H1 = "REPRODUCIDA" if (n_universo_triple == 9031 and n_tmodulo == 13502) else "REFUTADA"

# guardias contra el log GEN1 (L7)
gen1_p4_10 = {"1": 4275, "2": 2443, "3": 3405, "4": 1328, "5": 1479, "8": 74, "9": 498}
discordancias = []
for k, v in gen1_p4_10.items():
    if p4_10_counts[k] != v:
        discordancias.append(f"P4_10={k}:{p4_10_counts[k]}!={v}")
if n_p3_13_1_7 != 9312:
    discordancias.append(f"P3_13_1_7:{n_p3_13_1_7}!=9312")
veredicto_guardias_gen1 = "COINCIDEN" if not discordancias else "DISCORDAN:" + ";".join(discordancias)

# ---------- 2. P4: ninguna_via proxy ----------
INFORMAL = [f"P5_1_{i}" for i in range(1, 7)]
FORMAL = [f"P5_6_{i}" for i in range(1, 10)]


def ninguna_via(r):
    for c in INFORMAL:
        if r.get(c, "") == "1":
            return False
    for c in FORMAL:
        if r.get(c, "") == "1":
            return False
    return True


for r in rows:
    r["_ninguna_via"] = ninguna_via(r)

# D0_k universes: FAC_PER valid and P4_10 = k
def domain_p410(rowset, ks):
    return [r for r in rowset if r.get("P4_10", "") in ks]

D0_1 = domain_p410(fac_valid_rows, {"1"})
D0_2 = domain_p410(fac_valid_rows, {"2"})
D0_35 = domain_p410(fac_valid_rows, {"3", "4", "5"})


def weighted_frac(rowset, pred):
    num = sum(r["_FAC_PER_f"] for r in rowset if pred(r))
    den = sum(r["_FAC_PER_f"] for r in rowset)
    return (num / den) if den > 0 else None, num, den


n_d0_1 = len(D0_1)
n_ninguna_via_en_1 = sum(1 for r in D0_1 if r["_ninguna_via"])
p_ninguna_via_en_1, _, _ = weighted_frac(D0_1, lambda r: r["_ninguna_via"])

n_d0_2 = len(D0_2)
n_ninguna_via_en_2 = sum(1 for r in D0_2 if r["_ninguna_via"])
p_ninguna_via_en_2, _, _ = weighted_frac(D0_2, lambda r: r["_ninguna_via"])

n_d0_35 = len(D0_35)
n_ninguna_via_en_35 = sum(1 for r in D0_35 if r["_ninguna_via"])
p_ninguna_via_en_35, _, _ = weighted_frac(D0_35, lambda r: r["_ninguna_via"])

n_ninguna_via_total = sum(1 for r in fac_valid_rows if r["_ninguna_via"])
p_ninguna_via_total, _, _ = weighted_frac(fac_valid_rows, lambda r: r["_ninguna_via"])

# universos del lote ENIF-1 (verbatim de spec.yaml/universo)
U_A_SIN = [r for r in fac_valid_rows if r.get("P3_13", "") == "7" and r.get("P4_10", "") in P4_10_VALIDOS]
U_A_CON = [r for r in fac_valid_rows if r.get("P3_13", "") in {"1", "2", "3", "4"} and r.get("P4_10", "") in P4_10_VALIDOS]


def bloque_universo(U):
    n_u = len(U)
    n_p410_1 = sum(1 for r in U if r.get("P4_10", "") == "1")
    n_p410_1_nv = sum(1 for r in U if r.get("P4_10", "") == "1" and r["_ninguna_via"])
    p_p410_1_nv, _, den_u = weighted_frac(U, lambda r: r.get("P4_10", "") == "1" and r["_ninguna_via"])
    U_1 = [r for r in U if r.get("P4_10", "") == "1"]
    frac_de_p410_1_que_es_nv, _, _ = weighted_frac(U_1, lambda r: r["_ninguna_via"])
    U_12 = [r for r in U if r.get("P4_10", "") in {"1", "2"}]
    frac_de_corto12_que_es_p410_1_nv, _, _ = weighted_frac(
        U_12, lambda r: r.get("P4_10", "") == "1" and r["_ninguna_via"]
    )
    return {
        "n_u": n_u,
        "n_p410_1": n_p410_1,
        "n_p410_1_nv": n_p410_1_nv,
        "p_p410_1_nv": p_p410_1_nv,
        "frac_de_p410_1_que_es_nv": frac_de_p410_1_que_es_nv,
        "frac_de_corto12_que_es_p410_1_nv": frac_de_corto12_que_es_p410_1_nv,
        "U_1": U_1,
    }


bloque_sin = bloque_universo(U_A_SIN)
bloque_con = bloque_universo(U_A_CON)

# ---------- 3. Bootstrap CI (UPM_DIS within EST_DIS, 1000 reps, seed 20260909, PCG64) ----------
# Resolve ambiguity (documented in report): the bootstrap resamples PSU clusters (EST_DIS,
# UPM_DIS) *within the specific domain/universe being estimated* (not the whole TMODULO frame),
# i.e. a domain-cluster bootstrap. Rows lacking EST_DIS or UPM_DIS are excluded from the
# resampling frame (per spec filtros) but would still count in the point estimate (none found
# missing in this run, see report).


def bootstrap_ci(rowset, pred, seed=SEED, n_boot=N_BOOT):
    elig = [r for r in rowset if r.get("EST_DIS", "") != "" and r.get("UPM_DIS", "") != ""]
    n_missing = len(rowset) - len(elig)
    if not elig:
        return None, None, n_missing, "IC-BOOTSTRAP-UPM-EN-ESTRATO", 0

    fac = np.array([r["_FAC_PER_f"] for r in elig], dtype=float)
    ind = np.array([1.0 if pred(r) else 0.0 for r in elig], dtype=float)
    est_arr = np.array([r["EST_DIS"] for r in elig])
    upm_arr = np.array([r["UPM_DIS"] for r in elig])

    strata = {}
    n_estratos_upm_unica = 0
    for est in np.unique(est_arr):
        mask = est_arr == est
        upms_in_stratum = upm_arr[mask]
        unique_upms, inv = np.unique(upms_in_stratum, return_inverse=True)
        idx_in_full = np.where(mask)[0]
        # map each unique upm to the row positions (within full elig array) belonging to it
        upm_to_rows = [idx_in_full[inv == ui] for ui in range(len(unique_upms))]
        strata[est] = upm_to_rows
        if len(unique_upms) == 1:
            n_estratos_upm_unica += 1

    rng = np.random.Generator(np.random.PCG64(seed))
    ests = []
    for _b in range(n_boot):
        mult = np.zeros(len(elig), dtype=float)
        for est, upm_to_rows in strata.items():
            k = len(upm_to_rows)
            draws = rng.integers(0, k, size=k)
            counts = np.bincount(draws, minlength=k)
            for ci, cnt in enumerate(counts):
                if cnt:
                    mult[upm_to_rows[ci]] += cnt
        w = fac * mult
        den = w.sum()
        if den > 0:
            ests.append(float((w * ind).sum() / den))
    lo, hi = np.percentile(ests, [2.5, 97.5])
    metodo = "IC-CON-ESTRATOS-DE-UPM-UNICA" if n_estratos_upm_unica > 0 else "IC-BOOTSTRAP-UPM-EN-ESTRATO"
    return float(lo), float(hi), n_missing, metodo, n_estratos_upm_unica


ic_lo_1, ic_hi_1, nm1, metodo1, unica1 = bootstrap_ci(D0_1, lambda r: r["_ninguna_via"])
ic_lo_2, ic_hi_2, nm2, metodo2, unica2 = bootstrap_ci(D0_2, lambda r: r["_ninguna_via"])
ic_lo_sin, ic_hi_sin, nm_sin, metodo_sin, unica_sin = bootstrap_ci(
    bloque_sin["U_1"], lambda r: r["_ninguna_via"]
)
ic_lo_con, ic_hi_con, nm_con, metodo_con, unica_con = bootstrap_ci(
    bloque_con["U_1"], lambda r: r["_ninguna_via"]
)

n_estratos_upm_unica_total = unica1 + unica2 + unica_sin + unica_con
metodo_global = (
    "IC-CON-ESTRATOS-DE-UPM-UNICA" if n_estratos_upm_unica_total > 0 else "IC-BOOTSTRAP-UPM-EN-ESTRATO"
)

# ---------- report ----------
out = {
    "G-ENCODING-USADO": encoding_used,
    "C-N-TMODULO": n_tmodulo,
    "C-N-FAC-PER-VALIDO": n_fac_per_valido,
    "G-N-SIN-FAC-PER": n_sin_fac_per,
    "G-N-FUERA-DE-DOMINIO-P3-13": n_fuera_dominio_p3_13,
    "G-N-FUERA-DE-DOMINIO-P4-10": n_fuera_dominio_p4_10,
    "C-N-P4-10-k": p4_10_counts,
    "C-N-P3-13-1-7": n_p3_13_1_7,
    "C-N-P3-13-9": n_p3_13_9,
    "C-N-P3-13-BLANCO": n_p3_13_blanco,
    "C-N-UNIVERSO-TRIPLE": n_universo_triple,
    "C-MASA-FAC-PER": masa_fac_per,
    "C-FRAC-P3-13-1-7-NO-PONDERADA": frac_1_7_np,
    "C-FRAC-UNIVERSO-TRIPLE-NO-PONDERADA": frac_universo_triple_np,
    "C-FRAC-P3-13-1-7-PONDERADA": frac_1_7_pond,
    "C-FRAC-P3-13-1-7-9-PONDERADA": frac_1_7_9_pond,
    "C-FRAC-UNIVERSO-TRIPLE-PONDERADA": frac_universo_triple_pond,
    "tabla_siete_fracciones": tabla_siete_fracciones,
    "C-VEREDICTO-68-97": veredicto_68_97,
    "C-VEREDICTO-67-53": veredicto_67_53,
    "C-VEREDICTO-68-06": veredicto_68_06,
    "C-VEREDICTO-66-89": veredicto_66_89,
    "C-VEREDICTO-0-668937": veredicto_0_668937,
    "C-VEREDICTO-H1": veredicto_H1,
    "C-VEREDICTO-GUARDIAS-GEN1": veredicto_guardias_gen1,
    "D-N-1": n_d0_1,
    "D-N-NINGUNA-VIA-EN-1": n_ninguna_via_en_1,
    "D-P-NINGUNA-VIA-EN-1": p_ninguna_via_en_1,
    "D-P-NINGUNA-VIA-EN-1-IC-LO": ic_lo_1,
    "D-P-NINGUNA-VIA-EN-1-IC-HI": ic_hi_1,
    "D-N-2": n_d0_2,
    "D-N-NINGUNA-VIA-EN-2": n_ninguna_via_en_2,
    "D-P-NINGUNA-VIA-EN-2": p_ninguna_via_en_2,
    "D-P-NINGUNA-VIA-EN-2-IC-LO": ic_lo_2,
    "D-P-NINGUNA-VIA-EN-2-IC-HI": ic_hi_2,
    "D-N-3-5": n_d0_35,
    "D-N-NINGUNA-VIA-EN-3-5": n_ninguna_via_en_35,
    "D-P-NINGUNA-VIA-EN-3-5": p_ninguna_via_en_35,
    "D-N-NINGUNA-VIA-TOTAL": n_ninguna_via_total,
    "D-P-NINGUNA-VIA-TOTAL": p_ninguna_via_total,
    "D-N-U-A-SIN": bloque_sin["n_u"],
    "D-N-P410-1-SIN": bloque_sin["n_p410_1"],
    "D-N-P410-1-NINGUNA-VIA-SIN": bloque_sin["n_p410_1_nv"],
    "D-P-P410-1-NINGUNA-VIA-SIN": bloque_sin["p_p410_1_nv"],
    "D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-SIN": bloque_sin["frac_de_p410_1_que_es_nv"],
    "D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-SIN-IC-LO": ic_lo_sin,
    "D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-SIN-IC-HI": ic_hi_sin,
    "D-FRAC-DE-CORTO-12-QUE-ES-P410-1-NINGUNA-VIA-SIN": bloque_sin["frac_de_corto12_que_es_p410_1_nv"],
    "D-N-U-A-CON": bloque_con["n_u"],
    "D-N-P410-1-CON": bloque_con["n_p410_1"],
    "D-N-P410-1-NINGUNA-VIA-CON": bloque_con["n_p410_1_nv"],
    "D-P-P410-1-NINGUNA-VIA-CON": bloque_con["p_p410_1_nv"],
    "D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-CON": bloque_con["frac_de_p410_1_que_es_nv"],
    "D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-CON-IC-LO": ic_lo_con,
    "D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-CON-IC-HI": ic_hi_con,
    "D-FRAC-DE-CORTO-12-QUE-ES-P410-1-NINGUNA-VIA-CON": bloque_con["frac_de_corto12_que_es_p410_1_nv"],
    "D-N-ESTRATOS-UPM-UNICA-ALGUN-IC": n_estratos_upm_unica_total,
    "D-METODO-IC": metodo_global,
    "n_faltantes_est_upm": {"D0_1": nm1, "D0_2": nm2, "U1_SIN": nm_sin, "U1_CON": nm_con},
}

print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
