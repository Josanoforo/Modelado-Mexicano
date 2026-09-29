"""Reconstrucción CALC-ENSU-SERIE-0001 desde paquete/ (spec humana v1.0 + lista cerrada P1).

Uso, desde el directorio de trabajo:  python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json, salida/diagnostico.json, salida/archivos-leidos.txt,
salida/entorno.txt.
"""
import csv
import json
import os
import platform
import subprocess
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "paquete/lib")
import dbfread  # noqa: E402
from dbfread import DBF  # noqa: E402

PAQ = "paquete"
OUT = "salida"
LEIDOS = []

IDENTIDAD = {"paquete": "ensu-serie-0001", "version_entrada": "validacion-continua-1",
             "sha256_entrada": "3fba81d9ad75421ed925fb8ca89405a81df435191207e272904709cf5d8f8522"}
SEMILLA = 20260925
REPLICAS = 1000
DECISIONES = []


def decision(id_, frase, decision_):
    DECISIONES.append({"id": id_, "frase_que_motiva": frase, "decision": decision_})


# --------------------------------------------------------------------------- columnas autorizadas
E1_CB = ["ENT", "CON", "V_SEL", "N_HOG", "H_MUD", "N_REN", "CD", "EDIS", "UPM_DIS", "FACTOR",
         "P1", "P3_3", "P3_4", "P3_6", "P4_1", "P4_2", "P4_3", "P4_4"]
E1_CS = ["ENT", "CON", "V_SEL", "N_HOG", "H_MUD", "N_REN", "SEX", "EDA"]
E2_BASE = ["UPM", "VIV_SEL", "H_MUD", "R_SEL", "CD", "EST_DIS", "UPM_DIS", "FAC_SEL", "BP1_1"]
BP12 = ["BP1_2_03", "BP1_2_08", "BP1_2_09"]
BP_RESTO = ["BP1_3", "BP1_4_3", "BP1_4_4", "BP1_4_6", "BP1_5_1", "BP1_5_2", "BP1_5_3", "BP1_5_4"]
BP3 = ["BP3_5", "BP3_6"]

OLAS = ["2013T3", "2013T4"] + ["%dT%d" % (a, t) for a in range(2014, 2020) for t in (1, 2, 3, 4)] \
    + ["2020T1", "2020T3", "2020T4", "2021T2", "2021T3", "2021T4"] \
    + ["%dT%d" % (a, t) for a in range(2022, 2026) for t in (1, 2, 3, 4)]
T2T4_BP3 = {"2019T2", "2019T4", "2020T3", "2020T4", "2021T2", "2021T4", "2022T2", "2022T4",
            "2023T2", "2023T4", "2024T2", "2024T4", "2025T2", "2025T4"}


def era(ola):
    a = int(ola[:4])
    if a <= 2015:
        return "E1"
    if a <= 2020:
        return "E2"
    return "E3"


def columnas_cb(ola):
    """Columnas autorizadas de la CB por ola (lista del encargo)."""
    e = era(ola)
    if e == "E1":
        return list(E1_CB)
    cols = list(E2_BASE)
    if ola != "2016T1":
        cols += BP12
    cols += BP_RESTO
    if ola >= "2016T3":
        cols.append("BP1_8_1")
    if ola >= "2017T1":
        cols.append("BP1_9_1")
    if ola in T2T4_BP3:
        cols += BP3
    if ola in ("2020T3", "2020T4"):
        cols += ["SEX", "EDAD"]
    if e == "E3":
        cols += ["SEXO", "EDAD"]
    return cols


def columnas_cs(ola):
    e = era(ola)
    if e == "E1":
        return list(E1_CS)
    if e == "E2":
        return ["UPM", "VIV_SEL", "H_MUD", "N_REN", "SEX", "EDA" if ola < "2017T3" else "EDAD"]
    return None


# --------------------------------------------------------------------------- lectores
def lee_dbf(ruta, cols):
    """Lee SOLO las columnas pedidas: dbfread da la cabecera (offsets); de cada registro se
    cortan únicamente los bytes de esas columnas."""
    LEIDOS.append(ruta)
    t = DBF(ruta, load=False)
    nombres = [f.name for f in t.fields]
    faltan = [c for c in cols if c not in nombres]
    if faltan:
        raise KeyError("%s sin columnas %s" % (ruta, faltan))
    off = 1
    pos = {}
    for f in t.fields:
        pos[f.name] = (off, f.length)
        off += f.length
    hl, rl, nrec = t.header.headerlen, t.header.recordlen, t.header.numrecords
    enc = t.encoding
    with open(ruta, "rb") as fh:
        fh.seek(hl)
        buf = fh.read(rl * nrec)
    arr = np.frombuffer(buf, dtype=np.uint8)[: rl * nrec].reshape(nrec, rl)
    vivo = arr[:, 0] != ord("*")
    out = {}
    for c in cols:
        o, ln = pos[c]
        sub = np.ascontiguousarray(arr[vivo, o:o + ln])
        raw = sub.view("S%d" % ln).ravel()
        out[c] = pd.Series([x.decode(enc, errors="replace").strip() for x in raw], dtype=object)
    return pd.DataFrame(out), int((~vivo).sum())


def lee_csv(ruta, cols):
    LEIDOS.append(ruta)
    with open(ruta, "rb") as fh:
        h = next(csv.reader([fh.readline().decode("latin-1")]))
    h = [x.strip().lstrip("﻿").lstrip("ï»¿") for x in h]
    faltan = [c for c in cols if c not in h]
    if faltan:
        raise KeyError("%s sin columnas %s" % (ruta, faltan))
    idx = [h.index(c) for c in cols]
    df = pd.read_csv(ruta, usecols=idx, dtype=str, keep_default_na=False, encoding="latin-1")
    df.columns = [h[i] for i in sorted(idx)]
    df = df[cols]
    for c in cols:
        df[c] = df[c].astype(str).str.strip()
    return df, 0


def num(s):
    return pd.to_numeric(s.mask(s == ""), errors="coerce")


def norm_llave(s):
    """Normaliza componentes de llave: sin espacios; si es dígito, sin ceros a la izquierda."""
    s = s.astype(str).str.strip()
    dig = s.str.fullmatch(r"\d+")
    s = s.where(~dig, s.str.lstrip("0").replace("", "0"))
    return s


def cd2(s):
    s = s.astype(str).str.strip()
    dig = s.str.fullmatch(r"\d+")
    return s.where(~dig, s.str.zfill(2))


# --------------------------------------------------------------------------- conductas
# (id, variable 2016+, variable E1, códigos sí, universo, disponible desde)
CONDUCTAS = {
    "c01-inseg-ciudad": ("BP1_1", "P1", {2}, {1, 2, 9}),
    "c02-inseg-calle": ("BP1_2_03", None, {2}, {1, 2, 9}),
    "c03-inseg-cajero": ("BP1_2_08", None, {2}, {1, 2, 9}),
    "c04-inseg-transporte": ("BP1_2_09", None, {2}, {1, 2, 9}),
    "c05-expect-empeora": ("BP1_3", None, {4}, {1, 2, 3, 4, 9}),
    "c06-testigo-robos": ("BP1_4_3", "P3_3", {1}, {1, 2, 9}),
    "c07-testigo-pandillas": ("BP1_4_4", "P3_4", {1}, {1, 2, 9}),
    "c08-testigo-disparos": ("BP1_4_6", "P3_6", {1}, {1, 2, 9}),
    "c09-habito-objetos-valor": ("BP1_5_1", "P4_1", {1}, {1, 2, 3, 9}),
    "c10-habito-caminar-noche": ("BP1_5_2", "P4_2", {1}, {1, 2, 3, 9}),
    "c11-habito-visitar": ("BP1_5_3", "P4_3", {1}, {1, 2, 3, 9}),
    "c12-habito-menores": ("BP1_5_4", "P4_4", {1}, {1, 2, 3, 9}),
    "c13-policia-mun-confianza": ("BP1_9_1", None, {1, 2}, {1, 2, 3, 4, 9}),
    "c14-policia-mun-efectiva": ("BP1_8_1", None, {1, 2}, {1, 2, 3, 4, 9}),
    "c15-corrupcion-policia": ("BP3_6", None, {1}, {1, 2, 9}),
}


def indicadores(df, cond, ola):
    """Devuelve (en_universo bool, y 0/1) o None si el reactivo no existe en la ola."""
    v16, v1, si, univ = CONDUCTAS[cond]
    var = v1 if era(ola) == "E1" else v16
    if var is None or var not in df.columns:
        return None
    x = num(df[var])
    u = x.isin(list(univ))
    if cond == "c15-corrupcion-policia":
        u = u & (num(df["BP3_5"]) == 1)
    y = x.isin(list(si)).astype(float)
    return u.to_numpy(), y.to_numpy()


def edad_seg(e):
    out = pd.Series(pd.NA, index=e.index, dtype=object)
    out[(e >= 18) & (e <= 29)] = "18-29"
    out[(e >= 30) & (e <= 44)] = "30-44"
    out[(e >= 45) & (e <= 59)] = "45-59"
    out[(e >= 60) & (e <= 97)] = "60-MAS"
    return out


# --------------------------------------------------------------------------- carga por ola
def carga(ola):
    o = ola.lower()
    e = era(ola)
    cols = columnas_cb(ola)
    if e == "E3":
        cb, borr = lee_csv("%s/datos/ensu_%s_cb.csv" % (PAQ, o), cols)
    else:
        cb, borr = lee_dbf("%s/datos/ensu_%s_cb.dbf" % (PAQ, o), cols)
    diag = {"filas_cb": int(len(cb)), "registros_dbf_borrados": borr}
    fac = "FACTOR" if e == "E1" else "FAC_SEL"
    est = "EDIS" if e == "E1" else "EST_DIS"
    w = num(cb[fac])
    ex_fac = ~(w > 0)
    ex_est = (cb["CD"] == "") | (cb[est] == "")
    ex_upm = cb["UPM_DIS"] == ""
    diag["excl_factor_no_positivo_o_vacio"] = int(ex_fac.sum())
    diag["excl_estrato_vacio"] = int((ex_est & ~ex_fac).sum())
    diag["excl_upm_vacia"] = int((ex_upm & ~ex_fac & ~ex_est).sum())
    ok = ~(ex_fac | ex_est | ex_upm)
    cb = cb[ok].reset_index(drop=True)
    w = w[ok].reset_index(drop=True).to_numpy(dtype=float)
    diag["n_marco_valido"] = int(len(cb))
    cb["_W"] = w
    cb["_ESTRATO"] = cd2(cb["CD"]) + "|" + cb[est].astype(str)
    cb["_UPM"] = cb["_ESTRATO"] + "|" + cb["UPM_DIS"].astype(str)
    cb["_CD"] = cd2(cb["CD"])

    # sexo y edad
    sexo = pd.Series(np.nan, index=cb.index)
    edad = pd.Series(np.nan, index=cb.index)
    motivo_eje = pd.Series("", index=cb.index, dtype=object)
    if e == "E3":
        sexo = num(cb["SEXO"])
        edad = num(cb["EDAD"])
        diag["fuente_sexo_edad"] = "CB SEXO/EDAD"
    else:
        ccs = columnas_cs(ola)
        cs, _ = lee_dbf("%s/datos/ensu_%s_cs.dbf" % (PAQ, o), ccs)
        diag["filas_cs"] = int(len(cs))
        if e == "E1":
            kcb = ["ENT", "CON", "V_SEL", "N_HOG", "H_MUD", "N_REN"]
            kcs = kcb
            ecol = "EDA"
        else:
            kcb = ["UPM", "VIV_SEL", "H_MUD", "R_SEL"]
            kcs = ["UPM", "VIV_SEL", "H_MUD", "N_REN"]
            ecol = ccs[-1]
        kb = pd.Series("", index=cb.index, dtype=object)
        for c in kcb:
            kb = kb + "|" + norm_llave(cb[c])
        ks = pd.Series("", index=cs.index, dtype=object)
        for c in kcs:
            ks = ks + "|" + norm_llave(cs[c])
        vc = ks.value_counts()
        dup = set(vc[vc > 1].index)
        diag["cs_llaves_duplicadas"] = int(len(dup))
        csu = cs.assign(_K=ks)[~ks.isin(dup)].set_index("_K")
        es_dup = kb.isin(dup)
        en_cs = kb.isin(csu.index)
        motivo_eje[es_dup] = "G-CS-DUPLICADA"
        motivo_eje[~es_dup & ~en_cs] = "G-JOIN-SIN-CS"
        m = kb.where(en_cs)
        sexo = num(m.map(csu["SEX"]).fillna(""))
        edad = num(m.map(csu[ecol]).fillna(""))
        diag["fuente_sexo_edad"] = "CS por llave %s -> %s" % ("+".join(kcb), "+".join(kcs))
        diag["G-CS-DUPLICADA"] = int(es_dup.sum())
        diag["G-JOIN-SIN-CS"] = int((~es_dup & ~en_cs).sum())
        diag["cb_llaves_duplicadas"] = int(kb.duplicated(keep=False).sum())
        if ola in ("2020T3", "2020T4"):
            s_cb = num(cb["SEX"])
            e_cb = num(cb["EDAD"])
            both = en_cs.to_numpy()
            diag["control_2020_cb_vs_cs_sexo_coincide"] = int((s_cb[both] == sexo[both]).sum())
            diag["control_2020_cb_vs_cs_edad_coincide"] = int((e_cb[both] == edad[both]).sum())
            diag["control_2020_unidos"] = int(both.sum())
    seg_sexo = pd.Series(pd.NA, index=cb.index, dtype=object)
    seg_sexo[sexo == 1] = "HOMBRE"
    seg_sexo[sexo == 2] = "MUJER"
    seg_edad = edad_seg(edad)
    diag["sexo_fuera_de_catalogo_o_ausente"] = int(seg_sexo.isna().sum())
    diag["edad_fuera_de_eje_o_ausente"] = int(seg_edad.isna().sum())
    diag["edad_98_99"] = int(edad.isin([98, 99]).sum())
    diag["edad_97"] = int((edad == 97).sum())
    diag["edad_menor_18"] = int((edad < 18).sum())
    cb["_SEXO"] = seg_sexo
    cb["_EDAD"] = seg_edad
    return cb, diag


# --------------------------------------------------------------------------- bootstrap
def replicas(cb):
    """Multiplicadores de UPM (REPLICAS x nUPM). Estratos y UPM en orden lexicográfico;
    por estrato con n_h>=2 se sortean n_h UPM con reemplazo (una matriz REPLICAS x n_h);
    estrato de UPM única = certeza (multiplicador 1)."""
    upms = np.array(sorted(cb["_UPM"].unique()))
    est_de_upm = np.array([u.rsplit("|", 1)[0] for u in upms])
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    M = np.ones((REPLICAS, len(upms)), dtype=np.float64)
    estratos = sorted(set(est_de_upm))
    cert = 0
    inicio = {}
    for i, s in enumerate(est_de_upm):
        inicio.setdefault(s, [i, i])
        inicio[s][1] = i + 1
    for s in estratos:
        a, b = inicio[s]
        n = b - a
        if n == 1:
            cert += 1
            continue
        d = rng.integers(0, n, size=(REPLICAS, n))
        cnt = np.zeros((REPLICAS, n))
        np.add.at(cnt, (np.repeat(np.arange(REPLICAS), n), d.ravel()), 1.0)
        M[:, a:b] = cnt
    upm_idx = pd.Index(upms).get_indexer(cb["_UPM"])
    return M, upm_idx, {"n_upm": int(len(upms)), "n_estratos": len(estratos),
                        "estratos_upm_unica_certeza": cert}


def estima(w, y, sel, M, upm_idx, nupm):
    n = int(sel.sum())
    if n == 0:
        return {"N": 0}
    ws = w[sel]
    p = float(np.sum(ws * y[sel]) / np.sum(ws))
    num_u = np.bincount(upm_idx[sel], weights=ws * y[sel], minlength=nupm)
    den_u = np.bincount(upm_idx[sel], weights=ws, minlength=nupm)
    Rn = M @ num_u
    Rd = M @ den_u
    r = {"N": n, "P": p}
    deg = int((Rd <= 0).sum())
    r["replicas_degeneradas"] = deg
    if deg:
        return r
    reps = Rn / Rd
    lo, hi = np.percentile(reps, [2.5, 97.5])
    r["LO"], r["HI"] = float(lo), float(hi)
    return r


# --------------------------------------------------------------------------- principal
def main():
    os.makedirs(OUT, exist_ok=True)
    for f in ("esquema-identidades.tsv", "CONTRATO-v3.md", "FIRMAS-Y-ACCESO.md",
              "docs/spec-humana.md", "docs/lista-cerrada-P1.md"):
        LEIDOS.append("%s/%s" % (PAQ, f))
    esq = pd.read_csv("%s/esquema-identidades.tsv" % PAQ, sep="\t", dtype=str,
                      keep_default_na=False)

    decision("D01-remuestreo", "bootstrap de UPM dentro de estrato, `PCG64(20260925)`, 1 000 réplicas",
             "Por ola, un solo juego de 1000 réplicas sobre el marco válido completo, compartido por todas "
             "las celdas de la ola (\"mismo marco, semilla y réplicas\"). En cada estrato (CD+EST_DIS/EDIS) "
             "con n_h>=2 se sortean n_h UPM con reemplazo (n_h de n_h, sin reescalar); multiplicador = veces "
             "sorteada. Generador reiniciado con PCG64(20260925) en cada ola; estratos en orden "
             "lexicográfico, una llamada rng.integers(0,n_h,size=(1000,n_h)) por estrato.")
    decision("D02-certeza", "UPM única de certeza",
             "Estrato con una sola UPM: no se remuestrea (multiplicador 1 en todas las réplicas).")
    decision("D03-degenerada", "contrato conservador (réplica degenerada → sin IC)",
             "Réplica degenerada = réplica cuyo denominador ponderado de la celda es 0 (proporción "
             "indefinida). Si hay al menos una, estado_ic=NO-IDENTIFICADA con motivo_ic.")
    decision("D04-percentil", "percentiles 2.5/97.5",
             "numpy.percentile con interpolación lineal (método por defecto) sobre las 1000 proporciones replicadas.")
    decision("D05-edad97", "`60-MAS` = 60–96; 98/99 «no especificada» fuera del eje",
             "El código 97 («97 o más años», FD 2016 CS) entra en 60-MAS: la spec solo excluye 98/99 y el "
             "segmento es 60 y más; el rango 60–96 refleja el catálogo 18..96 de FD recientes.")
    decision("D06-sexo-edad-E2", "Sexo y edad por las llaves de la lista §2",
             "2016T1–2020T4 (E2, incluidos 2020T3/T4 que también traen SEX/EDAD en CB) toman sexo/edad de CS "
             "por UPM+VIV_SEL+H_MUD+R_SEL -> UPM+VIV_SEL+H_MUD+N_REN; CB SEX/EDAD de 2020 solo como control de conteo.")
    decision("D07-llave-normalizada", "llave CB→CS",
             "Componentes de llave con espacios recortados; si son solo dígitos se comparan sin ceros a la izquierda "
             "(R_SEL/N_REN pueden venir con distinto relleno).")
    decision("D08-universo", "el resto de códigos (blanco, fuera de catálogo) sale del universo",
             "Universo = código en la lista 'universo' de §3; numerador = código 'sí'. C15: BP3_5=1 y BP3_6∈{1,2,9}.")
    decision("D09-dbf-columnas", "de las filas solo estas columnas",
             "DBF: dbfread solo para la cabecera; de cada registro se cortan los bytes de las columnas autorizadas. "
             "Registros marcados como borrados ('*') se descartan.")
    decision("D10-celda-vacia", "Una celda sin personas emite `N`=0 y `P`/IC nulos",
             "Celda con N=0 en universo -> estado DENOMINADOR-CERO.")
    decision("D11-ic-calculado", "percentiles 2.5/97.5",
             "IC percentil emitido como CALCULADO aunque sea de ancho cero (p. ej. celda solo con UPM de certeza).")

    filas, diag_llaves, diag_olas = [], {}, {}
    for ola in OLAS:
        sub = esq[esq.ola == ola]
        if sub.empty:
            continue
        cb, dg = carga(ola)
        M, upm_idx, dm = replicas(cb)
        dg.update(dm)
        diag_olas[ola] = dg
        w = cb["_W"].to_numpy()
        cache = {}
        for _, r in sub.iterrows():
            cond, eje, seg = r.conducta, r.eje, r.segmento
            if cond not in cache:
                cache[cond] = indicadores(cb, cond, ola)
            ind = cache[cond]
            base = {"llave": r.llave, "unidad": r.unidad}
            dl = {"ola": ola, "conducta": cond, "eje": eje, "segmento": seg,
                  "n_marco_valido": dg["n_marco_valido"]}
            if ind is None:
                base.update(estado="NO-ESTIMABLE",
                            motivo="reactivo de %s no existe en %s (spec §2: no emite)" % (cond, ola))
                filas.append(base)
                diag_llaves[r.llave] = dl
                continue
            u, y = ind
            if eje == "TOTAL":
                dom = np.ones(len(cb), bool)
            elif eje == "SEXO":
                dom = (cb["_SEXO"] == seg).fillna(False).to_numpy(bool)
            elif eje == "EDAD":
                dom = (cb["_EDAD"] == seg).fillna(False).to_numpy(bool)
            elif eje == "CIUDAD":
                dom = (cb["_CD"] == seg).to_numpy(bool)
            else:
                raise ValueError(eje)
            sel = dom & u
            dl["n_dominio"] = int(dom.sum())
            dl["excl_fuera_de_universo"] = int((dom & ~u).sum())
            est = estima(w, y, sel, M, upm_idx, M.shape[1])
            dl["n_valido"] = est["N"]
            if "replicas_degeneradas" in est:
                dl["replicas_degeneradas"] = est["replicas_degeneradas"]
            diag_llaves[r.llave] = dl
            if est["N"] == 0:
                base.update(estado="DENOMINADOR-CERO",
                            motivo="celda sin personas en universo (N=0) en %s" % ola)
            else:
                base.update(estado="RECONSTRUIDO", punto=repr(float(est["P"])))
                if "LO" in est:
                    base.update(estado_ic="CALCULADO", ic95_inf=repr(float(est["LO"])),
                                ic95_sup=repr(float(est["HI"])))
                else:
                    base.update(estado_ic="NO-IDENTIFICADA",
                                motivo_ic="%d de %d réplicas bootstrap degeneradas (denominador 0); "
                                          "contrato conservador: sin IC" % (est["replicas_degeneradas"], REPLICAS))
            filas.append(base)
        print(ola, len(sub), dg["n_marco_valido"], file=sys.stderr)

    orden = {k: i for i, k in enumerate(esq.llave)}
    filas.sort(key=lambda f: orden[f["llave"]])
    assert len(filas) == len(esq) == len({f["llave"] for f in filas})
    doc = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open("%s/resultado.json" % OUT, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
    with open("%s/diagnostico.json" % OUT, "w", encoding="utf-8") as fh:
        json.dump({"decisiones": DECISIONES, "por_ola": diag_olas, "por_llave": diag_llaves},
                  fh, ensure_ascii=False, indent=1)

    # entorno y archivos leídos
    libs = sorted({os.path.relpath(m.__file__) for m in list(sys.modules.values())
                   if getattr(m, "__file__", None) and os.path.abspath(m.__file__).startswith(
                       os.path.abspath("%s/lib" % PAQ))})
    manual = ["%s/docs/%s" % (PAQ, f) for f in sorted(os.listdir("%s/docs" % PAQ)) if f.endswith(".pdf")]
    with open("%s/archivos-leidos.txt" % OUT, "w") as fh:
        vistos = []
        for x in LEIDOS + manual + libs:
            if x not in vistos:
                vistos.append(x)
        fh.write("\n".join(vistos) + "\n")
    with open("%s/entorno.txt" % OUT, "w") as fh:
        fh.write("python %s\n" % sys.version.replace("\n", " "))
        fh.write("numpy %s\npandas %s\n" % (np.__version__, pd.__version__))
        fh.write("dbfread %s (paquete/lib)\n" % getattr(dbfread, "__version__", "?"))
        fh.write("pdftotext (poppler, lectura manual de FD): %s\n" % subprocess.run(
            ["pdftotext", "-v"], capture_output=True, text=True).stderr.splitlines()[0])
        fh.write("uname -a: %s\n" % subprocess.run(["uname", "-a"], capture_output=True,
                                                   text=True).stdout.strip())


if __name__ == "__main__":
    main()
