#!/usr/bin/env python3
"""
Independent blind re-derivation of CALC-ENVIPE-U4-2012-v1_1, P-C2-U4.

Written WITHOUT reading resultados.json / sello.json / ejecucion.json / medidor.py
of CALC-ENVIPE-U4-2012-v1_1, and WITHOUT reading anything under
data/corrida0/CALC-ENVIPE-U4-2012/ (the v1.0 predecessor's sealed files).

Sources read to build this script (all explicitly allowed as the frozen contract):
  - data/corrida0/CALC-ENVIPE-U4-2012-v1_1/spec.yaml
  - data/corrida0/CALC-ENVIPE-U4-2012-v1_1/spec.md
  - forense/prereg-caja/ENVIPE-2012-U4-spec-v1_1.md
  - forense/prereg-caja/ENVIPE-2012-U4-spec-v1_0.md

Raw microdata: /home/pc0/mm-corpus/raw/envipe2012/base_de_datos_envipe_2012_dbf.zip
"""
import zipfile
import math
import numpy as np

ZIP_PATH = "/home/pc0/mm-corpus/raw/envipe2012/base_de_datos_envipe_2012_dbf.zip"

# ---------------------------------------------------------------------------
# Minimal inline DBF reader (own implementation, per spec.yaml's
# "Lector DBF inline (cabecera + descriptores del propio archivo, latin-1,
# borrados excluidos y contados)"). We trust the file's own header/field
# descriptors over the external FD spreadsheet, per project convention.
# ---------------------------------------------------------------------------

def read_dbf_header(f):
    header = f.read(32)
    n_records = int.from_bytes(header[4:8], "little")
    header_len = int.from_bytes(header[8:10], "little")
    record_len = int.from_bytes(header[10:12], "little")
    codepage = header[29]
    fields = []
    bytes_read = 32
    while True:
        first = f.read(1)
        bytes_read += 1
        if len(first) == 0 or first == b"\r":
            break
        rest = f.read(31)
        bytes_read += 31
        b = first + rest
        name = b[0:11].split(b"\x00")[0].decode("latin-1")
        ftype = chr(b[11])
        flen = b[16]
        fdec = b[17]
        fields.append((name, ftype, flen, fdec))
    # consume any padding up to header_len (rare, but be safe)
    if bytes_read < header_len:
        f.read(header_len - bytes_read)
    return {
        "n_records_declared": n_records,
        "header_len": header_len,
        "record_len": record_len,
        "codepage": codepage,
        "fields": fields,
    }


def iter_dbf_records(f, meta, wanted):
    """Yield dict{field_name: str} for ACTIVE (non-deleted) records only.
    Only `wanted` field names are decoded (memory/speed)."""
    offsets = {}
    pos = 1  # byte 0 of each record is the deletion flag
    for (name, ftype, flen, fdec) in meta["fields"]:
        if name in wanted:
            offsets[name] = (pos, flen)
        pos += flen
    record_len = meta["record_len"]
    n_active = 0
    n_deleted = 0
    n_truncated = 0
    while True:
        rec = f.read(record_len)
        if len(rec) < record_len:
            if len(rec) > 0:
                n_truncated += 1
            break
        flag = rec[0:1]
        if flag == b"*":
            n_deleted += 1
            continue
        n_active += 1
        row = {}
        for name, (o, l) in offsets.items():
            row[name] = rec[o:o + l].decode("latin-1")
        yield row
    iter_dbf_records.stats = {"n_active": n_active, "n_deleted": n_deleted, "n_truncated": n_truncated}


def open_member(zf, name):
    return zf.open(name, "r")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def to_int(text):
    t = text.strip()
    if t == "":
        return None
    try:
        return int(t)
    except ValueError:
        return None


def to_float(text):
    t = text.strip()
    if t == "":
        return None
    try:
        v = float(t)
    except ValueError:
        return None
    if not math.isfinite(v):
        return None
    return v


BPCOD_PERSONALES = set(range(4, 15))  # {04..14}
C1_UNO = {1, 2, 6}
C1_CERO = {3, 4, 5, 7, 8}
C2_UNO = {1, 2, 6, 8}
C2_CERO = {3, 4, 5, 7}
CATALOGO_BP123 = set(range(1, 10)) | {99}  # 01..09, 99 (blank handled separately)

results = {}

# ---------------------------------------------------------------------------
# PASS 1: Tmod_Vic.DBF  (unit: delito)
# ---------------------------------------------------------------------------

zf = zipfile.ZipFile(ZIP_PATH)
results["G-N-MIEMBROS-ZIP"] = len(zf.infolist())

want_mod = {"CONTROL", "VIV_SEL", "HOGAR", "R_SEL", "BPCOD", "BP1_20", "BP1_23", "FAC_DEL", "EST", "UPM"}
with open_member(zf, "Tmod_Vic.DBF") as f:
    meta_mod = read_dbf_header(f)
    rows_mod = list(iter_dbf_records(f, meta_mod, want_mod))
stats_mod = iter_dbf_records.stats

results["PERFIL-DBF-MODULO"] = (
    f"registros_declarados={meta_mod['n_records_declared']}, rlen={meta_mod['record_len']}, "
    f"hlen={meta_mod['header_len']}, campos={len(meta_mod['fields'])}, codepage={meta_mod['codepage']}, "
    f"borrados={stats_mod['n_deleted']}, truncados={stats_mod['n_truncated']}, leidos={stats_mod['n_active']}"
)
results["N-FILAS-MODULO"] = stats_mod["n_active"]

# PERFIL-BPCOD: raw distribution, unweighted, before any filter
bpcod_dist = {}
hogar_est_upm_mod = {}  # household -> set of (EST,UPM) pairs, ALL rows
est_values_mod = set()
delitos_u1 = []  # list of dicts for rows passing U1 filter
n_bp123_blanco = 0
n_bp123_99 = 0
n_bp123_fuera = 0
n_u1_sin_ponderador = 0

for r in rows_mod:
    control = r["CONTROL"].strip()
    viv = r["VIV_SEL"].strip()
    hog = r["HOGAR"].strip()
    hh = (control, viv, hog)
    est = r["EST"].strip()
    upm = r["UPM"].strip()
    est_values_mod.add(est)
    hogar_est_upm_mod.setdefault(hh, set()).add((est, upm))

    bpcod_raw = r["BPCOD"].strip()
    bpcod_dist[bpcod_raw] = bpcod_dist.get(bpcod_raw, 0) + 1
    bpcod_i = to_int(r["BPCOD"])

    bp123_raw = r["BP1_23"]
    bp123_i = to_int(bp123_raw)
    if bp123_raw.strip() == "":
        n_bp123_blanco += 1
    elif bp123_i == 99:
        n_bp123_99 += 1
    elif bp123_i is None or bp123_i not in CATALOGO_BP123:
        n_bp123_fuera += 1

    bp120_raw = r["BP1_20"].strip()

    if (bpcod_i in BPCOD_PERSONALES) and (bp120_raw == "2") and (bp123_i is not None and 1 <= bp123_i <= 8):
        fac_del = to_float(r["FAC_DEL"])
        if fac_del is None or fac_del <= 0:
            n_u1_sin_ponderador += 1
            continue
        delitos_u1.append({
            "hh": hh,
            "r_sel_raw": r["R_SEL"],
            "bp123": bp123_i,
            "fac_del": fac_del,
        })

results["PERFIL-BPCOD"] = str(sorted(bpcod_dist.items()))
results["N-BP1-23-BLANCO"] = n_bp123_blanco
results["N-BP1-23-99"] = n_bp123_99
results["N-BP1-23-FUERA-DE-CATALOGO"] = n_bp123_fuera
results["N-U1-SIN-PONDERADOR"] = n_u1_sin_ponderador

results["G-MOD-N-HOGARES"] = len(hogar_est_upm_mod)
results["G-MOD-N-HOGARES-EST-UPM-MULTI"] = sum(1 for s in hogar_est_upm_mod.values() if len(s) > 1)
results["G-N-EST-DISTINTOS-MODULO"] = len(est_values_mod)
lead_sp = sum(1 for e in est_values_mod if e != e.lstrip())
widths_mod = sorted(set(len(e) for e in est_values_mod))
results["G-PERFIL-DISENO-MODULO"] = f"n_est_distintos={len(est_values_mod)}, anchos={widths_mod}"

# household -> resolved unique (EST,UPM) pair from Tmod_Vic, or None if ambiguous
hh_design_mod = {}
for hh, pairs in hogar_est_upm_mod.items():
    if len(pairs) == 1:
        hh_design_mod[hh] = next(iter(pairs))
    else:
        hh_design_mod[hh] = None

# --- N-U1 / R_SEL blank among U1, P-C1-U1 control ---
n_u1_rsel_blanco = 0
u1_final = []
for d in delitos_u1:
    r_sel_i = to_int(d["r_sel_raw"])
    if r_sel_i is None:
        n_u1_rsel_blanco += 1
        # still counted in N-U1 per spec's definition (N-U1 counts BPCOD/BP1_20/BP1_23/FAC_DEL only);
        # R_SEL blank is a separate/orthogonal count used later to gate U4 attribution.
    u1_final.append((d, r_sel_i))

results["N-U1"] = len(delitos_u1)
results["N-U1-R-SEL-BLANCO"] = n_u1_rsel_blanco

masa_fac_del_u1 = sum(d["fac_del"] for d in delitos_u1)
num_c1 = sum(d["fac_del"] for d in delitos_u1 if d["bp123"] in C1_UNO)
p_c1_u1 = num_c1 / masa_fac_del_u1 if masa_fac_del_u1 > 0 else None
results["MASA-FAC-DEL-U1"] = masa_fac_del_u1
results["P-C1-U1"] = p_c1_u1

REF_P_C1_U1 = 0.29557241046799515
REF_N_U1 = 14532
REF_N_FILAS = 32493
if (
    p_c1_u1 is not None
    and abs(p_c1_u1 - REF_P_C1_U1) <= 1e-9
    and results["N-U1"] == REF_N_U1
    and results["N-FILAS-MODULO"] == REF_N_FILAS
):
    results["G-CONTROL-U1"] = "REPRODUCE"
else:
    results["G-CONTROL-U1"] = "NO-REPRODUCE"

# ---------------------------------------------------------------------------
# PASS 2: tper_vic.dbf (unit: household member row)
# ---------------------------------------------------------------------------

want_per = {"CONTROL", "VIV_SEL", "HOGAR", "R_SEL", "TOT_PER", "FAC_ELE", "EST", "UPM"}
with open_member(zf, "tper_vic.dbf") as f:
    meta_per = read_dbf_header(f)
    hogares_per = {}  # hh -> dict(n_rows, tot_per_set, r_sel_set, fac_ele_set, est_upm_set)
    est_values_per = set()
    n_active_per = 0
    for r in iter_dbf_records(f, meta_per, want_per):
        n_active_per += 1
        hh = (r["CONTROL"].strip(), r["VIV_SEL"].strip(), r["HOGAR"].strip())
        est = r["EST"].strip()
        upm = r["UPM"].strip()
        est_values_per.add(est)
        d = hogares_per.setdefault(hh, {
            "n_rows": 0, "tot_per": set(), "r_sel": set(), "fac_ele": set(), "est_upm": set(),
        })
        d["n_rows"] += 1
        tot_per_i = to_int(r["TOT_PER"])
        d["tot_per"].add(tot_per_i)
        d["r_sel"].add(r["R_SEL"].strip())
        d["fac_ele"].add(r["FAC_ELE"].strip())
        d["est_upm"].add((est, upm))
    stats_per = iter_dbf_records.stats

results["PERFIL-DBF-PERSONAS"] = (
    f"registros_declarados={meta_per['n_records_declared']}, rlen={meta_per['record_len']}, "
    f"hlen={meta_per['header_len']}, campos={len(meta_per['fields'])}, codepage={meta_per['codepage']}, "
    f"borrados={stats_per['n_deleted']}, truncados={stats_per['n_truncated']}, leidos={stats_per['n_active']}"
)
results["N-FILAS-PERSONAS"] = n_active_per
results["G-PER-N-HOGARES"] = len(hogares_per)
results["G-PER-N-HOGARES-FILAS-NE-TOT-PER"] = sum(
    1 for d in hogares_per.values()
    if (len(d["tot_per"]) != 1) or (next(iter(d["tot_per"])) != d["n_rows"])
)
results["G-PER-N-HOGARES-R-SEL-MULTI"] = sum(1 for d in hogares_per.values() if len(d["r_sel"]) > 1)
results["G-PER-N-HOGARES-FAC-ELE-MULTI"] = sum(1 for d in hogares_per.values() if len(d["fac_ele"]) > 1)
results["G-PER-N-HOGARES-EST-UPM-MULTI"] = sum(1 for d in hogares_per.values() if len(d["est_upm"]) > 1)
results["G-N-EST-DISTINTOS-PERSONAS"] = len(est_values_per)
widths_per = sorted(set(len(e) for e in est_values_per))
results["G-PERFIL-DISENO-PERSONAS"] = f"n_est_distintos={len(est_values_per)}, valores={sorted(est_values_per)}, anchos={widths_per}"

# Resolve FAC_ELE per household (rule 1 -> 2 -> 3)
n_hogares_fac_ele_unica = 0

def resolve_fac_ele(fac_ele_text_set):
    global n_hogares_fac_ele_unica
    if len(fac_ele_text_set) == 1:
        txt = next(iter(fac_ele_text_set))
        v = to_float(txt)
        if v is not None and v > 0:
            return v
        # branch 1 gave a single text but it's not a usable positive finite number:
        # fall through to ambiguous (no 2nd distinct value to try) -> None
        return None
    # more than one distinct text -> try branch 2: exactly one finite>0 among them
    finite_positive = [v for v in (to_float(t) for t in fac_ele_text_set) if v is not None and v > 0]
    if len(finite_positive) == 1:
        n_hogares_fac_ele_unica += 1
        return finite_positive[0]
    return None


hh_fac_ele = {}
for hh, d in hogares_per.items():
    hh_fac_ele[hh] = resolve_fac_ele(d["fac_ele"])

# Household R_SEL set (as ints) from tper_vic, for matching against delitos
hh_rsel_set = {}
for hh, d in hogares_per.items():
    ints = set()
    for t in d["r_sel"]:
        i = to_int(t)
        if i is not None:
            ints.add(i)
    hh_rsel_set[hh] = ints

# UPM discordance guard: compare Tmod_Vic resolved UPM vs tper_vic UPM set, per household
n_upm_discorda = 0
for hh, pair in hh_design_mod.items():
    if pair is None:
        continue
    upm_mod = pair[1]
    per_d = hogares_per.get(hh)
    if per_d is None:
        continue
    upms_per = set(u for (_, u) in per_d["est_upm"])
    if upm_mod not in upms_per:
        n_upm_discorda += 1
results["G-N-HOGARES-UPM-DISCORDA-MOD-VS-PER"] = n_upm_discorda

# ---------------------------------------------------------------------------
# PASS 3: tsdem.DBF (unit: household member row)
# ---------------------------------------------------------------------------

want_sdem = {"CONTROL", "VIV_SEL", "HOGAR", "N_REN", "EDAD"}
n_ren_left_sp = 0
n_ren_right_sp = 0
n_ren_no_sp = 0
hogares_sdem_nren = {}  # hh -> dict(n_ren_int -> list of EDAD raw)
hogares_sdem_rowcount = {}

with open_member(zf, "tsdem.DBF") as f:
    meta_sdem = read_dbf_header(f)
    n_active_sdem = 0
    for r in iter_dbf_records(f, meta_sdem, want_sdem):
        n_active_sdem += 1
        hh = (r["CONTROL"].strip(), r["VIV_SEL"].strip(), r["HOGAR"].strip())
        raw_nren = r["N_REN"]
        if raw_nren != raw_nren.lstrip():
            n_ren_left_sp += 1
        elif raw_nren != raw_nren.rstrip():
            n_ren_right_sp += 1
        else:
            n_ren_no_sp += 1
        nren_i = to_int(raw_nren)
        hogares_sdem_nren.setdefault(hh, {}).setdefault(nren_i, []).append(r["EDAD"])
        hogares_sdem_rowcount[hh] = hogares_sdem_rowcount.get(hh, 0) + 1
    stats_sdem = iter_dbf_records.stats

results["PERFIL-DBF-SOCIODEM"] = (
    f"registros_declarados={meta_sdem['n_records_declared']}, rlen={meta_sdem['record_len']}, "
    f"hlen={meta_sdem['header_len']}, campos={len(meta_sdem['fields'])}, codepage={meta_sdem['codepage']}, "
    f"borrados={stats_sdem['n_deleted']}, truncados={stats_sdem['n_truncated']}, leidos={stats_sdem['n_active']}"
)
results["N-FILAS-SOCIODEM"] = n_active_sdem
results["G-TSDEM-PERFIL-N-REN"] = f"izq={n_ren_left_sp}, der={n_ren_right_sp}, sin_espacio={n_ren_no_sp}"
results["G-TSDEM-N-HOGARES"] = len(hogares_sdem_nren)

n_filas_ne_tper = 0
for hh, cnt in hogares_sdem_rowcount.items():
    per_d = hogares_per.get(hh)
    if per_d is None or per_d["n_rows"] != cnt:
        n_filas_ne_tper += 1
results["G-TSDEM-N-HOGARES-FILAS-NE-TPER"] = n_filas_ne_tper

# ---------------------------------------------------------------------------
# Build U4 candidatas and final U4 members
# ---------------------------------------------------------------------------

n_delitos_rsel_blanco2 = 0  # (mirrors N-DELITOS-R-SEL-BLANCO per funnel text, gates U4 not just N-U1)
n_delitos_hogar_sin_tper = 0
n_delitos_rsel_discorda = 0

# candidata key = (hh, r_sel_int) -> list of bp123 ints (attributable delitos)
candidatas = {}
for d, r_sel_i in u1_final:
    hh = d["hh"]
    if r_sel_i is None:
        n_delitos_rsel_blanco2 += 1
        continue
    if hh not in hogares_per:
        n_delitos_hogar_sin_tper += 1
        continue
    if r_sel_i not in hh_rsel_set.get(hh, set()):
        n_delitos_rsel_discorda += 1
        continue
    key = (hh, r_sel_i)
    candidatas.setdefault(key, []).append(d["bp123"])

results["N-DELITOS-R-SEL-BLANCO"] = n_delitos_rsel_blanco2
results["N-DELITOS-HOGAR-SIN-TPER-VIC"] = n_delitos_hogar_sin_tper
results["N-DELITOS-R-SEL-DISCORDA"] = n_delitos_rsel_discorda
results["N-U4-CANDIDATAS"] = len(candidatas)

n_fac_ele_ambiguo = 0
n_tsdem_0 = 0
n_tsdem_1 = 0
n_tsdem_multi = 0
n_edad_menor_18 = 0
n_edad_no_esp = 0
n_diseno_ambiguo = 0
n_sin_diseno = 0

u4_members = []  # dicts: w (FAC_ELE), d1, d2, est, upm (or None)

for (hh, r_sel_i), bp123_list in candidatas.items():
    w = hh_fac_ele.get(hh)
    if w is None:
        n_fac_ele_ambiguo += 1
        continue
    sdem_rows = hogares_sdem_nren.get(hh, {})
    edad_list = sdem_rows.get(r_sel_i, [])
    n_match = len(edad_list)
    if n_match == 0:
        n_tsdem_0 += 1
        continue
    elif n_match > 1:
        n_tsdem_multi += 1
        continue
    else:
        n_tsdem_1 += 1

    edad_raw = edad_list[0]
    edad_i = to_int(edad_raw)
    if edad_i is not None and edad_i < 18:
        n_edad_menor_18 += 1
    if edad_i is None or edad_i in (98, 99):
        n_edad_no_esp += 1

    d1 = 1 if any(b in C1_UNO for b in bp123_list) else 0
    d2 = 1 if any(b in C2_UNO for b in bp123_list) else 0

    pair = hh_design_mod.get(hh)
    if pair is None:
        n_diseno_ambiguo += 1
        n_sin_diseno += 1
        est_u, upm_u = None, None
    else:
        est_u, upm_u = pair

    u4_members.append({"w": w, "d1": d1, "d2": d2, "est": est_u, "upm": upm_u})

results["N-U4-FAC-ELE-AMBIGUO"] = n_fac_ele_ambiguo
results["N-U4-TSDEM-0"] = n_tsdem_0
results["N-U4-TSDEM-1"] = n_tsdem_1
results["N-U4-TSDEM-MULTI"] = n_tsdem_multi
results["N-U4-EDAD-MENOR-18"] = n_edad_menor_18
results["N-U4-EDAD-NO-ESPECIFICADA"] = n_edad_no_esp
results["N-U4-DISENO-AMBIGUO"] = n_diseno_ambiguo
results["N-U4-SIN-DISENO"] = n_sin_diseno
results["N-U4"] = len(u4_members)
results["N-U4-D2-UNO"] = sum(1 for m in u4_members if m["d2"] == 1)
results["N-HOGARES-FAC-ELE-RESUELTO-POR-UNICA-VALIDA"] = n_hogares_fac_ele_unica

if len(u4_members) == 0:
    results["ESTADO"] = "NO-ESTIMABLE-UNIVERSO-VACIO" if len(candidatas) == 0 else "NO-ESTIMABLE-JOIN-VACIO"
    results["P-C2-U4"] = None
    results["P-C1-U4"] = None
    results["MASA-FAC-ELE-U4"] = None
else:
    masa = sum(m["w"] for m in u4_members)
    num_c2 = sum(m["w"] * m["d2"] for m in u4_members)
    num_c1 = sum(m["w"] * m["d1"] for m in u4_members)
    results["MASA-FAC-ELE-U4"] = masa
    results["P-C2-U4"] = num_c2 / masa
    results["P-C1-U4"] = num_c1 / masa
    results["P-C2-U4-COMPLEMENTO"] = 1.0 - results["P-C2-U4"]
    results["ESTADO"] = "CALCULADO"

# ---------------------------------------------------------------------------
# Design summary + bootstrap CI
# ---------------------------------------------------------------------------

design_members = [m for m in u4_members if m["est"] is not None and m["upm"] is not None]
estratos = sorted(set(m["est"] for m in design_members))
upms = sorted(set((m["est"], m["upm"]) for m in design_members))
results["N-ESTRATOS"] = len(estratos)
results["N-UPM"] = len(upms)

# group members by (est, upm)
from collections import defaultdict
by_upm = defaultdict(list)  # (est,upm) -> list of members
for m in design_members:
    by_upm[(m["est"], m["upm"])].append(m)

by_estrato_upms = defaultdict(list)  # est -> list of upm keys
for (est, upm) in by_upm:
    by_estrato_upms[est].append((est, upm))

n_estratos_upm_unica = sum(1 for est, ups in by_estrato_upms.items() if len(ups) == 1)
results["N-ESTRATOS-UPM-UNICA"] = n_estratos_upm_unica
results["METODO-IC"] = (
    "IC-CON-ESTRATOS-DE-UPM-UNICA" if n_estratos_upm_unica > 0 else "IC-BOOTSTRAP-UPM-EN-ESTRATO"
) if design_members else "NO-ESTIMABLE-DISENO-INCOMPLETO"

SEED = 20260909
N_REPLICAS = 2000

if design_members:
    rng = np.random.Generator(np.random.PCG64(SEED))
    estrato_list = sorted(by_estrato_upms.keys())
    # precompute per-upm weighted sums needed for C2 and C1 ratio, and mass
    upm_w = {}
    upm_wd2 = {}
    upm_wd1 = {}
    for key, members in by_upm.items():
        upm_w[key] = sum(mm["w"] for mm in members)
        upm_wd2[key] = sum(mm["w"] * mm["d2"] for mm in members)
        upm_wd1[key] = sum(mm["w"] * mm["d1"] for mm in members)

    boot_c2 = np.empty(N_REPLICAS)
    boot_c1 = np.empty(N_REPLICAS)
    estrato_upm_arrays = {est: by_estrato_upms[est] for est in estrato_list}

    for b in range(N_REPLICAS):
        tot_w = 0.0
        tot_wd2 = 0.0
        tot_wd1 = 0.0
        for est in estrato_list:
            ups = estrato_upm_arrays[est]
            k = len(ups)
            idx = rng.integers(0, k, size=k)  # with replacement, same count as original UPMs in stratum
            for i in idx:
                key = ups[i]
                tot_w += upm_w[key]
                tot_wd2 += upm_wd2[key]
                tot_wd1 += upm_wd1[key]
        boot_c2[b] = tot_wd2 / tot_w if tot_w > 0 else np.nan
        boot_c1[b] = tot_wd1 / tot_w if tot_w > 0 else np.nan

    ic_lo_c2, ic_hi_c2 = np.nanpercentile(boot_c2, [2.5, 97.5])
    ic_lo_c1, ic_hi_c1 = np.nanpercentile(boot_c1, [2.5, 97.5])
    results["IC-LO-C2-U4"] = float(ic_lo_c2)
    results["IC-HI-C2-U4"] = float(ic_hi_c2)
    results["IC-LO-C1-U4"] = float(ic_lo_c1)
    results["IC-HI-C1-U4"] = float(ic_hi_c1)

    # ---- Taylor linearization, lonely.psu="adjust"-style approximation ----
    Rhat = results["P-C2-U4"]  # note: uses ALL U4 members' point (design + no-design);
    # but variance only defined over the design_members' mass. We linearize
    # using the (mass, num) split restricted to design_members' total, i.e.
    # treat design_members as the design-based subpopulation for the CI.
    mass_design = sum(m["w"] for m in design_members)
    num_design = sum(m["w"] * m["d2"] for m in design_members)
    Rhat_design = num_design / mass_design if mass_design > 0 else float("nan")

    # PSU-level totals of the linearized variable z = w*(d2 - Rhat_design)
    psu_totals = {}
    for key, members in by_upm.items():
        psu_totals[key] = sum(mm["w"] * (mm["d2"] - Rhat_design) for mm in members)

    var_terms = []
    lonely_psu_totals = []
    for est in estrato_list:
        ups = estrato_upm_arrays[est]
        n_h = len(ups)
        totals = [psu_totals[u] for u in ups]
        if n_h > 1:
            mean_h = sum(totals) / n_h
            v_h = (n_h / (n_h - 1)) * sum((t - mean_h) ** 2 for t in totals)
            var_terms.append(v_h)
        else:
            # lonely PSU: defer, adjust by centering against the grand mean
            # of all lonely-PSU totals (a standard "adjust" style substitute
            # for a within-stratum contrast that doesn't exist).
            lonely_psu_totals.append(totals[0])

    if len(lonely_psu_totals) >= 2:
        grand_mean = sum(lonely_psu_totals) / len(lonely_psu_totals)
        n_l = len(lonely_psu_totals)
        v_l = (n_l / (n_l - 1)) * sum((t - grand_mean) ** 2 for t in lonely_psu_totals)
        var_terms.append(v_l)
    elif len(lonely_psu_totals) == 1:
        # a single lonely stratum with nothing to center against contributes 0
        # under the "adjust" convention (no usable contrast).
        pass

    V = sum(var_terms)
    if mass_design > 0 and V >= 0:
        ee = math.sqrt(V) / mass_design
    else:
        ee = float("nan")
    results["EE-TAYLOR-C2-U4"] = ee
    Z = 1.959964
    results["IC-LO-TAYLOR-C2-U4"] = Rhat_design - Z * ee
    results["IC-HI-TAYLOR-C2-U4"] = Rhat_design + Z * ee
else:
    for k in ["IC-LO-C2-U4", "IC-HI-C2-U4", "IC-LO-C1-U4", "IC-HI-C1-U4",
              "EE-TAYLOR-C2-U4", "IC-LO-TAYLOR-C2-U4", "IC-HI-TAYLOR-C2-U4"]:
        results[k] = None

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

order = [
    "G-N-MIEMBROS-ZIP", "PERFIL-DBF-MODULO", "N-FILAS-MODULO", "PERFIL-BPCOD",
    "N-BP1-23-BLANCO", "N-BP1-23-99", "N-BP1-23-FUERA-DE-CATALOGO", "N-U1-SIN-PONDERADOR",
    "N-U1", "P-C1-U1", "MASA-FAC-DEL-U1", "G-CONTROL-U1", "N-U1-R-SEL-BLANCO",
    "G-MOD-N-HOGARES", "G-MOD-N-HOGARES-EST-UPM-MULTI", "G-N-EST-DISTINTOS-MODULO", "G-PERFIL-DISENO-MODULO",
    "PERFIL-DBF-PERSONAS", "N-FILAS-PERSONAS", "G-PER-N-HOGARES", "G-PER-N-HOGARES-FILAS-NE-TOT-PER",
    "G-PER-N-HOGARES-R-SEL-MULTI", "G-PER-N-HOGARES-FAC-ELE-MULTI", "G-PER-N-HOGARES-EST-UPM-MULTI",
    "G-N-EST-DISTINTOS-PERSONAS", "G-PERFIL-DISENO-PERSONAS", "N-HOGARES-FAC-ELE-RESUELTO-POR-UNICA-VALIDA",
    "G-N-HOGARES-UPM-DISCORDA-MOD-VS-PER",
    "PERFIL-DBF-SOCIODEM", "N-FILAS-SOCIODEM", "G-TSDEM-PERFIL-N-REN", "G-TSDEM-N-HOGARES",
    "G-TSDEM-N-HOGARES-FILAS-NE-TPER",
    "N-DELITOS-R-SEL-BLANCO", "N-DELITOS-HOGAR-SIN-TPER-VIC", "N-DELITOS-R-SEL-DISCORDA",
    "N-U4-CANDIDATAS", "N-U4-FAC-ELE-AMBIGUO", "N-U4-TSDEM-0", "N-U4-TSDEM-1", "N-U4-TSDEM-MULTI",
    "N-U4-EDAD-MENOR-18", "N-U4-EDAD-NO-ESPECIFICADA", "N-U4-DISENO-AMBIGUO", "N-U4", "N-U4-D2-UNO",
    "N-U4-SIN-DISENO", "MASA-FAC-ELE-U4", "P-C2-U4", "P-C1-U4", "P-C2-U4-COMPLEMENTO",
    "N-ESTRATOS", "N-UPM", "N-ESTRATOS-UPM-UNICA", "METODO-IC",
    "IC-LO-C2-U4", "IC-HI-C2-U4", "IC-LO-C1-U4", "IC-HI-C1-U4",
    "EE-TAYLOR-C2-U4", "IC-LO-TAYLOR-C2-U4", "IC-HI-TAYLOR-C2-U4", "ESTADO",
]

for k in order:
    print(f"{k} = {results.get(k)}")
