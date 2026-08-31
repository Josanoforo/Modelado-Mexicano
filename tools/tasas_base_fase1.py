#!/usr/bin/env python3
"""ACTO MAESTRA32-E18 · REGLAS-OLA5-FASE1 — COMMIT-2

Calcula p = proporcion ponderada del desenlace=1 en su universo de
calibracion, para las 5 reglas de la spec congelada
(forense/notas/2026-08-31-reglas-fase1-spec.md), con IC95 por bootstrap
10k replicas seed=42 (declarado: no hay campo de diseno UPM/estrato
reproducible dentro del perimetro de este acto para ninguna de las
cinco fuentes -- ver spec (c) por regla).

No escribe ni lee milpa/tramite.yaml ni milpa/procedencia.yaml.
Solo lee data/raw/**. Escribe su resultado en:
  - milpa/tramite-ola5-propuesta-v0.yaml (via este mismo script, llamado
    aparte por el acto -- este script solo IMPRIME el resultado; quien
    ejecuta el acto pega el output en los dos archivos de destino,
    exactamente como pide el encargo).

Uso:
    python3 tools/tasas_base_fase1.py
"""
import hashlib
import io
import os
import random
import zipfile

import dbfread
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
SEED = 42
N_BOOT = 10000


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wprop_ic_bootstrap(desenlace, peso, n_boot=N_BOOT, seed=SEED):
    """proporcion ponderada + IC95 por bootstrap (remuestreo de filas)."""
    d = list(desenlace)
    w = list(peso)
    n = len(d)
    assert n == len(w)
    sw = sum(w)
    p_hat = sum(wi * di for wi, di in zip(w, d)) / sw
    rng = random.Random(seed)
    boots = []
    idx = list(range(n))
    for _ in range(n_boot):
        sample = [idx[rng.randrange(n)] for _ in range(n)]
        sw_b = sum(w[i] for i in sample)
        sp_b = sum(w[i] * d[i] for i in sample)
        boots.append(sp_b / sw_b)
    boots.sort()
    lo = boots[int(0.025 * n_boot)]
    hi = boots[int(0.975 * n_boot) - 1]
    return p_hat, lo, hi, n


# ─────────────────────────────────────────────────────────────────────
# 1. civico.denuncia.miedo_desconfianza -- ENVIPE 2025
# ─────────────────────────────────────────────────────────────────────
def regla_civico_denuncia():
    zpath = os.path.join(RAW, "envipe2025_csv.zip")
    if not os.path.exists(zpath):
        return {"estado": "NO-ENCONTRADO", "razon": f"{zpath} no existe"}
    sha = sha256(zpath)
    z = zipfile.ZipFile(zpath)
    with z.open(
        "tper_vic2_envipe2025/conjunto_de_datos/"
        "conjunto_de_datos_tper_vic2_envipe2025.csv"
    ) as f:
        vic2 = pd.read_csv(f, encoding="latin-1", low_memory=False)
    with z.open(
        "tmod_vic_envipe2025/conjunto_de_datos/"
        "conjunto_de_datos_tmod_vic_envipe2025.csv"
    ) as f:
        modv = pd.read_csv(f, encoding="latin-1", low_memory=False)

    ap7_cols = [f"AP7_3_{xx:02d}" for xx in range(5, 16)]
    vic2["_disparador"] = (vic2[ap7_cols] == 1).any(axis=1)
    universo_ids = set(vic2.loc[vic2["_disparador"], "ID_PER"])
    n_universo_vic2 = len(universo_ids)

    modv["BPCOD"] = pd.to_numeric(modv["BPCOD"], errors="coerce")
    filas = modv[
        modv["ID_PER"].isin(universo_ids)
        & modv["BPCOD"].between(5, 15)
        & (modv["BP1_20"] == 2)
    ].copy()

    miedo = {1, 2, 6, 8}
    practica = {3, 4, 5, 7}
    filas["BP1_23"] = pd.to_numeric(filas["BP1_23"], errors="coerce")
    filas = filas[filas["BP1_23"].isin(miedo | practica)]
    filas["_desenlace"] = filas["BP1_23"].isin(miedo).astype(int)

    colapso = filas.groupby("ID_PER")["_desenlace"].max().reset_index()
    n_universo = len(colapso)

    pesos = vic2.drop_duplicates("ID_PER").set_index("ID_PER")["FAC_ELE"]
    colapso["_peso"] = colapso["ID_PER"].map(pesos)
    colapso = colapso.dropna(subset=["_peso"])
    n_con_peso = len(colapso)

    p, lo, hi, n = wprop_ic_bootstrap(
        colapso["_desenlace"].tolist(), colapso["_peso"].tolist()
    )
    return {
        "estado": "MEDIDO",
        "sha256_payload": sha,
        "n_universo_disparador_vic2": n_universo_vic2,
        "n_universo_colapsado_persona": n_universo,
        "n_con_ponderador": n_con_peso,
        "p": p,
        "ic95": (lo, hi),
        "n": n,
    }


# ─────────────────────────────────────────────────────────────────────
# 2. dinero.ahorro.tiene_ahorros -- ENNViH olas 2-3, cr27, ola calib=2
# ─────────────────────────────────────────────────────────────────────
def regla_dinero_ahorro():
    base = os.path.join(RAW, "ennvih")
    z5 = os.path.join(base, "ehh05dta_all.zip")
    z9 = os.path.join(base, "ehh09dta_all.zip")
    zw = os.path.join(base, "ehh05w_all.zip")
    for p_ in (z5, z9, zw):
        if not os.path.exists(p_):
            return {"estado": "NO-ENCONTRADO", "razon": f"{p_} no existe"}
    sha5, sha9, shaw = sha256(z5), sha256(z9), sha256(zw)

    def leer_dta(zpath, member):
        with zipfile.ZipFile(zpath) as z:
            with z.open(member) as f:
                data = io.BytesIO(f.read())
        return pd.read_stata(data, convert_categoricals=False)

    pr2 = leer_dta(z5, "ehh05dta_b3b/iiib_pr.dta")
    cr2 = leer_dta(z5, "ehh05dta_b3b/iiib_cr.dta")
    pr3 = leer_dta(z9, "ehh09dta_all/ehh09dta_b3b/iiib_pr.dta")
    cr3 = leer_dta(z9, "ehh09dta_all/ehh09dta_b3b/iiib_cr.dta")

    key = [c for c in pr2.columns if c.lower() == "pid_link"]
    if not key:
        return {"estado": "NO-ENCONTRADO", "razon": "pid_link no localizada en iiib_pr ola2"}
    key = key[0]

    def normaliza_pid(s):
        return s.astype(str).str.strip()

    pr2["_pid"] = normaliza_pid(pr2[key])
    cr2["_pid"] = normaliza_pid(cr2[key])
    pr3["_pid"] = normaliza_pid(pr3[key])
    cr3["_pid"] = normaliza_pid(cr3[key])

    # excluir ronda C (nuevo entrante 2009) de ola 3, patron declarado en cal-g3-puntual
    pr3 = pr3[~pr3["_pid"].str.contains(r"\dC[PH]\d", regex=True, na=False)]
    cr3 = cr3[~cr3["_pid"].str.contains(r"\dC[PH]\d", regex=True, na=False)]

    ola2 = pr2[["_pid", "pr02"]].merge(cr2[["_pid", "cr27"]], on="_pid", how="inner")
    ola3 = pr3[["_pid", "pr02"]].merge(cr3[["_pid", "cr27"]], on="_pid", how="inner")

    # despoja letras de pid ola3 para casar con ola2 (mismo metodo cal-g3-puntual)
    ola3["_pid_num"] = ola3["_pid"].str.replace(r"[A-Za-z]", "", regex=True)
    ola2["_pid_num"] = ola2["_pid"].str.replace(r"[A-Za-z]", "", regex=True)

    m = ola2.merge(ola3, on="_pid_num", how="inner", suffixes=("_o2", "_o3"))
    m = m[m["pr02_o2"].between(1, 7) & m["pr02_o3"].between(1, 7)]
    m = m[m["cr27_o2"].isin([1, 3]) & m["cr27_o3"].isin([1, 3])]
    n_universo_panel = len(m)

    zwf = zipfile.ZipFile(zw)
    wmember = [n for n in zwf.namelist() if n.endswith("_b3b.dta")]
    if not wmember:
        return {"estado": "NO-ENCONTRADO", "razon": "peso fac_3b no localizado en ehh05w_all.zip"}
    with zwf.open(wmember[0]) as f:
        wdf = pd.read_stata(io.BytesIO(f.read()), convert_categoricals=False)
    faccol = [c for c in wdf.columns if c.lower() == "fac_3b"]
    if "folio" not in wdf.columns or "ls" not in wdf.columns or not faccol:
        return {"estado": "NO-ENCONTRADO",
                 "razon": f"columnas folio/ls/fac_3b no localizadas en {wmember[0]}: "
                          f"cols={list(wdf.columns)[:20]}"}
    faccol = faccol[0]
    # pid_link (ola 2) = folio + ls concatenados, sin letras -- construir la
    # misma llave folio+ls a partir de pid_link_o2 para unir el peso.
    m["_folio"] = m["_pid_num"].str.slice(0, 8)
    m["_ls"] = m["_pid_num"].str.slice(8, 10)
    wdf["_folio"] = wdf["folio"].astype(str).str.strip().str.zfill(8)
    wdf["_ls"] = wdf["ls"].astype(str).str.strip().str.zfill(2)
    pesos = wdf.drop_duplicates(["_folio", "_ls"]).set_index(["_folio", "_ls"])[faccol]

    m["_peso"] = m.set_index(["_folio", "_ls"]).index.map(pesos)
    m = m.dropna(subset=["_peso"])
    n_con_peso = len(m)

    m["_desenlace"] = (m["cr27_o2"] == 1).astype(int)
    p, lo, hi, n = wprop_ic_bootstrap(m["_desenlace"].tolist(), m["_peso"].tolist())
    return {
        "estado": "MEDIDO",
        "sha256_payload_ola2": sha5,
        "sha256_payload_ola3": sha9,
        "sha256_payload_peso": shaw,
        "n_universo_panel_pre_peso": n_universo_panel,
        "n_con_ponderador": n_con_peso,
        "p": p,
        "ic95": (lo, hi),
        "n": n,
    }


# ─────────────────────────────────────────────────────────────────────
# 3. familia.apoyo.recibe_dinero_familiares -- ENIF 2024, P9_9_4
# ─────────────────────────────────────────────────────────────────────
def regla_familia_apoyo():
    zpath = os.path.join(RAW, "enif_2024_bd_csv.zip")
    if not os.path.exists(zpath):
        return {"estado": "NO-ENCONTRADO", "razon": f"{zpath} no existe"}
    sha = sha256(zpath)
    z = zipfile.ZipFile(zpath)
    with z.open("TMODULO.csv") as f:
        df = pd.read_csv(f, encoding="latin-1", low_memory=False)

    df["FILTRO_S9_1"] = pd.to_numeric(df["FILTRO_S9_1"], errors="coerce")
    df["EDAD_V"] = pd.to_numeric(df["EDAD_V"], errors="coerce")
    universo = df[(df["FILTRO_S9_1"] == 2) & (df["EDAD_V"] < 71)].copy()
    n_universo = len(universo)

    universo["P9_9_4"] = pd.to_numeric(universo["P9_9_4"], errors="coerce")
    universo = universo[universo["P9_9_4"].isin([1, 2])]
    universo["_desenlace"] = (universo["P9_9_4"] == 1).astype(int)
    universo["FAC_PER"] = pd.to_numeric(universo["FAC_PER"], errors="coerce")
    universo = universo.dropna(subset=["FAC_PER"])
    n_con_peso = len(universo)

    p, lo, hi, n = wprop_ic_bootstrap(
        universo["_desenlace"].tolist(), universo["FAC_PER"].tolist()
    )
    return {
        "estado": "MEDIDO",
        "sha256_payload": sha,
        "n_universo_filtro_edad": n_universo,
        "n_con_ponderador_y_reactivo_valido": n_con_peso,
        "p": p,
        "ic95": (lo, hi),
        "n": n,
    }


# ─────────────────────────────────────────────────────────────────────
# 4. familia.corresidencia.adulto_familiar -- EDER 2017
# ─────────────────────────────────────────────────────────────────────
COR_VARS = ["padre_cor", "madre_cor", "hnos_cor", "suegro_cor", "suegra_cor"]


def regla_familia_corresidencia():
    zpath = os.path.join(RAW, "eder2017", "eder2017_bases_csv.zip")
    if not os.path.exists(zpath):
        return {"estado": "NO-ENCONTRADO", "razon": f"{zpath} no existe"}
    sha = sha256(zpath)
    z = zipfile.ZipFile(zpath)
    with z.open("vivienda.csv") as f:
        vivienda = pd.read_csv(f, encoding="latin-1", low_memory=False)
    with z.open("historiavida.csv") as f:
        hv = pd.read_csv(f, encoding="latin-1", low_memory=False)

    fv_col_v = [c for c in vivienda.columns if c.lower().endswith("folioviv")][0]
    fv_col_h = [c for c in hv.columns if c.lower().endswith("folioviv")][0]

    vivienda["_tipo_adqui_ok"] = vivienda["tipo_adqui"].notna() & (
        vivienda["tipo_adqui"].astype(str).str.strip() != ""
    )
    universo_viv = vivienda[vivienda["_tipo_adqui_ok"]].copy()
    n_universo_viviendas = len(universo_viv)
    pesos_hogar = universo_viv.set_index(fv_col_v)["factor"]

    for c in COR_VARS:
        hv[c] = hv[c].astype(str).str.strip()
    hv["_coreside_fila"] = hv[COR_VARS].eq("1").any(axis=1)
    persona_key = [fv_col_h, "foliohog", "id_pobla"]
    personas = hv.groupby(persona_key)["_coreside_fila"].max().reset_index()
    personas = personas.rename(columns={"_coreside_fila": "_desenlace"})
    personas["_desenlace"] = personas["_desenlace"].astype(int)

    personas["_peso"] = personas[fv_col_h].map(pesos_hogar)
    n_personas_total = len(personas)
    personas = personas.dropna(subset=["_peso"])
    n_con_peso = len(personas)

    p, lo, hi, n = wprop_ic_bootstrap(
        personas["_desenlace"].tolist(), personas["_peso"].tolist()
    )
    return {
        "estado": "MEDIDO",
        "sha256_payload": sha,
        "n_universo_viviendas_tipo_adqui_no_blanco": n_universo_viviendas,
        "n_personas_historiavida_total": n_personas_total,
        "n_con_ponderador": n_con_peso,
        "p": p,
        "ic95": (lo, hi),
        "n": n,
        "nota_ic": "sin campo de diseno UPM/estrato reproducible dentro del "
                   "perimetro de este acto -- bootstrap simple declarado, no "
                   "supuesto de diseno complejo (mismo criterio que las otras 4 reglas)",
    }


# ─────────────────────────────────────────────────────────────────────
# 5. tramite.mordida.discrecional (enmienda) -- ENCUCI 2020
# ─────────────────────────────────────────────────────────────────────
def regla_encuci_mordida():
    zpath = os.path.join(RAW, "BD_ENCUCI2020_dbf.zip")
    if not os.path.exists(zpath):
        return {"estado": "NO-ENCONTRADO", "razon": f"{zpath} no existe"}
    sha = sha256(zpath)
    scratch = os.environ.get("SCRATCH_DBF", "/tmp")
    os.makedirs(scratch, exist_ok=True)
    z = zipfile.ZipFile(zpath)
    member = "ENCUCI_2020_SEC_4_5.dbf"
    extracted = os.path.join(scratch, member)
    z.extract(member, scratch)

    tabla = dbfread.DBF(extracted, encoding="latin-1")
    filas = []
    contacto_cols = [f"AP5_16_{i}" for i in range(1, 11)]
    def _es_1(v):
        try:
            return float(v) == 1.0
        except (TypeError, ValueError):
            return str(v).strip() == "1"

    for row in tabla:
        contacto = any(_es_1(row.get(c)) for c in contacto_cols)
        if not contacto:
            continue
        desenlace = 1 if (_es_1(row.get("AP5_17")) or _es_1(row.get("AP5_18"))) else 0
        try:
            peso = float(row.get("FAC_SEL"))
        except (TypeError, ValueError):
            continue
        filas.append((desenlace, peso))

    n_universo = len(filas)
    if n_universo == 0:
        return {"estado": "NO-ENCONTRADO", "razon": "universo de contacto vacio"}
    desenlaces = [f[0] for f in filas]
    pesos = [f[1] for f in filas]
    p, lo, hi, n = wprop_ic_bootstrap(desenlaces, pesos)
    return {
        "estado": "MEDIDO",
        "sha256_payload": sha,
        "n_universo_contacto": n_universo,
        "p": p,
        "ic95": (lo, hi),
        "n": n,
    }


def fmt(r, nombre):
    print(f"\n=== {nombre} ===")
    if r["estado"] != "MEDIDO":
        print(f"  estado: {r['estado']} -- {r.get('razon')}")
        return
    print(f"  estado: MEDIDO")
    for k, v in r.items():
        if k in ("estado", "p", "ic95"):
            continue
        print(f"  {k}: {v}")
    print(f"  n = {r['n']}")
    print(f"  p = {r['p']:.6f}")
    print(f"  IC95 = [{r['ic95'][0]:.6f}, {r['ic95'][1]:.6f}]")


def main():
    resultados = {}
    resultados["civico.denuncia.miedo_desconfianza"] = regla_civico_denuncia()
    resultados["dinero.ahorro.tiene_ahorros"] = regla_dinero_ahorro()
    resultados["familia.apoyo.recibe_dinero_familiares"] = regla_familia_apoyo()
    resultados["familia.corresidencia.adulto_familiar"] = regla_familia_corresidencia()
    resultados["tramite.mordida.discrecional[enmienda_encuci]"] = regla_encuci_mordida()

    for nombre, r in resultados.items():
        fmt(r, nombre)

    n_medido = sum(1 for r in resultados.values() if r["estado"] == "MEDIDO")
    print(f"\n\nRESUMEN: {n_medido} de {len(resultados)} reglas con p medida.")
    return resultados


if __name__ == "__main__":
    main()
