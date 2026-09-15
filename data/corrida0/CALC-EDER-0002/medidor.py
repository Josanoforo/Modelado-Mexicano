"""`CALC-EDER-0002` — re-estimación con diseño muestral de
`familia.corresidencia.adulto_familiar_actual` (EDER 2017, ventana ACTUAL,
universo Jefe/Cónyuge de `MAESTRA33-C1`).

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1`
(pieza P1, `NC-0184`), ANTES DE LEER UN SOLO VALOR DEL MICRODATO. Spec sellada
que lo gobierna: `forense/prereg-caja/EDER-CORRESIDENCIA-ACTUAL-DISENO-spec-v1_0.md`.

Hermano de `data/corrida0/CALC-EDER-0001/medidor.py` (mismo lector, misma
varianza de diseño, mismas guardias de estructura); cambia el estimando, que
reproduce paso a paso `tools/tasas_base_corresidencia_actual.py` (E.3).
"""
from __future__ import annotations

import io
import math
import zipfile

import numpy as np
import pandas as pd

ZIP_ID = "eder_2017_eder2017_bases_csv"
T_VIV = "vivienda.csv"
T_PER = "persona.csv"
T_HV = "historiavida.csv"
T_ANT = "antecedentes.csv"

COLS_VIV = ["folioviv", "tipo_adqui", "factor", "est_dis", "upm"]
COLS_PER = ["folioviv", "foliohog", "id_pobla", "parentesco"]
COLS_HV = ["folioviv", "foliohog", "id_pobla"]
COLS_ANT = ["folioviv", "foliohog", "id_pobla", "factor_per"]

SEP = "␟"


def _num(v):
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _perfil(valores):
    anchos = {}
    for v in valores:
        anchos[len(v)] = anchos.get(len(v), 0) + 1
    return ";".join(f"ancho={k}:{anchos[k]}" for k in sorted(anchos)) or "vacio"


def _cabecera(zf, miembro):
    with zf.open(miembro) as fh:
        return fh.readline().decode("latin-1").rstrip("\r\n").split(",")


def _col(nombres, sufijo):
    exactos = [c for c in nombres if c == sufijo]
    if exactos:
        return exactos[0]
    cand = [c for c in nombres if c.endswith(sufijo)]
    return cand[0] if cand else None


def _lee_csv(zf, miembro, columnas, dtype_str=()):
    """Misma lectura que C1 y que la hermana: `latin-1`, `low_memory=False`,
    sólo las columnas pedidas, renombradas sin BOM."""
    cab = _cabecera(zf, miembro)
    mapa, faltantes = {}, []
    for c in columnas:
        real = _col(cab, c)
        if real is None:
            faltantes.append(c)
        else:
            mapa[real] = c
    if faltantes:
        return None, faltantes, len(cab)
    dtype = {real: str for real, c in mapa.items() if c in dtype_str}
    with zf.open(miembro) as fh:
        df = pd.read_csv(io.BytesIO(fh.read()), encoding="latin-1",
                         low_memory=False, usecols=list(mapa),
                         dtype=dtype or None)
    return df.rename(columns=mapa), [], len(cab)


def _p(desenlace, peso):
    sw = float(np.sum(peso))
    if sw <= 0:
        return None
    return float(np.sum(peso * desenlace) / sw)


def _claves_diseno(estrato, upm):
    claves = np.array([f"{e}{SEP}{u}" for e, u in zip(estrato, upm)])
    upm_unicas, inverso = np.unique(claves, return_inverse=True)
    estr_de_upm = np.array([k.split(SEP)[0] for k in upm_unicas])
    return upm_unicas, inverso, estr_de_upm


def _bootstrap(d, w, estrato, upm, replicas, semilla):
    n = len(estrato)
    if n == 0:
        return None, 0, 0, 0
    upm_unicas, inverso, estr_de_upm = _claves_diseno(estrato, upm)
    n_upm = len(upm_unicas)
    estratos = np.unique(estr_de_upm)
    sw = np.bincount(inverso, weights=w, minlength=n_upm)
    swd = np.bincount(inverso, weights=w * d, minlength=n_upm)
    rng = np.random.Generator(np.random.PCG64(semilla))
    a_sw, a_swd = np.zeros(replicas), np.zeros(replicas)
    n_una = 0
    for e in estratos:
        pos = np.flatnonzero(estr_de_upm == e)
        k = len(pos)
        if k == 1:
            n_una += 1
            a_sw += sw[pos[0]]
            a_swd += swd[pos[0]]
            continue
        elegidas = rng.integers(0, k, size=(replicas, k))
        a_sw += sw[pos][elegidas].sum(axis=1)
        a_swd += swd[pos][elegidas].sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        serie = np.where(a_sw > 0, a_swd / np.where(a_sw > 0, a_sw, 1.0), np.nan)
    return serie, len(estratos), n_upm, n_una


def _taylor(d, w, estrato, upm):
    n = len(estrato)
    if n == 0:
        return None
    W = float(np.sum(w))
    if W <= 0:
        return None
    p = float(np.sum(w * d) / W)
    z = w * (d - p) / W
    upm_unicas, inverso, estr_de_upm = _claves_diseno(estrato, upm)
    z_psu = np.bincount(inverso, weights=z, minlength=len(upm_unicas))
    zbar_global = float(z_psu.mean())
    var = 0.0
    for e in np.unique(estr_de_upm):
        pos = np.flatnonzero(estr_de_upm == e)
        k = len(pos)
        if k == 1:
            var += (float(z_psu[pos[0]]) - zbar_global) ** 2
        else:
            zh = z_psu[pos]
            var += k / (k - 1) * float(np.sum((zh - zh.mean()) ** 2))
    return math.sqrt(var)


def _pct(serie):
    if serie is None:
        return None, None
    v = serie[~np.isnan(serie)]
    if v.size == 0:
        return None, None
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def medir(inputs, contrato):
    par = contrato["parametros"]
    replicas = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    z95 = float(par["z_95"])
    tol = float(par["umbral_replica_gen1"])
    grano = int(par["grano_milpa_decimales"])
    gen1 = par["valores_gen1_referencia"]
    esp = par["embudo_c1_esperado"]
    cod = par["codificacion"]
    C_JEFE, C_CONY = str(cod["jefe"]), str(cod["conyuge"])
    C_ASC, C_SUE = str(cod["ascendiente"]), str(cod["suegro"])
    CATALOGO = {str(c) for c in cod["catalogo_parentesco"]}

    P = "RESULT-EDER-ACT-"
    out = {P + s: None for s in par["sufijos_result"]}
    for s in par["sufijos_result"]:
        entero = s.startswith(("G-N-", "A-N-", "B-N-")) or s == "A-DELTA-N-VS-GEN1"
        texto = ("VEREDICTO" in s or "REPRODUCE" in s or "METODO-IC" in s or
                 s.startswith(("G-LLAVE", "G-PERFIL", "G-UPM-ANIDA")) or
                 s in ("A-ADOPCION", "A-EMBUDO-C1"))
        if entero:
            out[P + s] = 0
        elif texto:
            out[P + s] = "NO-ESTIMABLE"

    def para(v_a, v_b=None, estructura=None):
        out[P + "A-VEREDICTO"] = v_a
        out[P + "B-VEREDICTO"] = v_b if v_b is not None else v_a
        if estructura is not None:
            out[P + "G-VEREDICTO-ESTRUCTURA"] = estructura
        out[P + "A-ADOPCION"] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    # ── G-1 · miembros ────────────────────────────────────────────────────
    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    miembros = set(zf.namelist())
    out[P + "G-N-MIEMBROS-ZIP"] = len(miembros)
    for m in (T_VIV, T_PER, T_HV):
        if m not in miembros:
            return para(f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{m}",
                        estructura=f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{m}")

    # ── G-2 · columnas ────────────────────────────────────────────────────
    viv, falt, ncol_v = _lee_csv(zf, T_VIV, COLS_VIV, dtype_str=("est_dis", "upm"))
    out[P + "G-N-COLUMNAS-VIVIENDA"] = ncol_v
    if falt:
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}",
                    estructura=f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}")
    per, falt, ncol_p = _lee_csv(zf, T_PER, COLS_PER, dtype_str=("parentesco",))
    out[P + "G-N-COLUMNAS-PERSONA"] = ncol_p
    if falt:
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}",
                    estructura=f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}")
    hv, falt, ncol_h = _lee_csv(zf, T_HV, COLS_HV)
    out[P + "G-N-COLUMNAS-HISTORIAVIDA"] = ncol_h
    if falt:
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}",
                    estructura=f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}")
    ant = None
    if T_ANT in miembros:
        ant, falt, ncol_a = _lee_csv(zf, T_ANT, COLS_ANT)
        out[P + "G-N-COLUMNAS-ANTECEDENTES"] = ncol_a
        if falt:
            ant = None
            out[P + "B-VEREDICTO"] = f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}"
    else:
        out[P + "B-VEREDICTO"] = f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{T_ANT}"
    out[P + "G-VEREDICTO-ESTRUCTURA"] = ("ESTRUCTURA-OK" if ant is not None
                                         else "ESTRUCTURA-OK-SIN-ANTECEDENTES")

    out[P + "G-N-FILAS-VIVIENDA"] = int(len(viv))
    out[P + "G-N-FILAS-PERSONA"] = int(len(per))
    out[P + "G-N-FILAS-HISTORIAVIDA"] = int(len(hv))
    out[P + "G-N-FILAS-ANTECEDENTES"] = int(len(ant)) if ant is not None else 0

    # ── G-3 · llaves ──────────────────────────────────────────────────────
    llave_viv_unica = bool(viv["folioviv"].is_unique)
    out[P + "G-LLAVE-VIVIENDA-FOLIOVIV-UNICA"] = "SI" if llave_viv_unica else "NO"
    terna_per_unica = not bool(per.duplicated(["folioviv", "foliohog", "id_pobla"]).any())
    out[P + "G-LLAVE-PERSONA-TERNA-UNICA"] = "SI" if terna_per_unica else "NO"
    terna_ant_unica = False
    if ant is not None:
        terna_ant_unica = not bool(ant.duplicated(["folioviv", "foliohog", "id_pobla"]).any())
        out[P + "G-LLAVE-ANTECEDENTES-TERNA-UNICA"] = "SI" if terna_ant_unica else "NO"

    # ── G · perfil del diseño en vivienda.csv ─────────────────────────────
    est_txt = viv["est_dis"].fillna("").astype(str).str.strip()
    upm_txt = viv["upm"].fillna("").astype(str).str.strip()
    fac_v = pd.to_numeric(viv["factor"], errors="coerce")
    out[P + "G-N-VIVIENDA-SIN-EST-DIS"] = int((est_txt == "").sum())
    out[P + "G-N-VIVIENDA-SIN-UPM"] = int((upm_txt == "").sum())
    out[P + "G-N-VIVIENDA-SIN-FACTOR"] = int((~np.isfinite(fac_v.to_numpy(dtype=float)) |
                                             (fac_v.fillna(0).to_numpy() <= 0)).sum())
    out[P + "G-PERFIL-EST-DIS"] = _perfil(est_txt[est_txt != ""].tolist())
    out[P + "G-PERFIL-UPM"] = _perfil(upm_txt[upm_txt != ""].tolist())
    con_dis = (est_txt != "") & (upm_txt != "")
    cruzan = (pd.DataFrame({"e": est_txt[con_dis], "u": upm_txt[con_dis]})
              .drop_duplicates().groupby("u")["e"].nunique())
    n_cruzan = int((cruzan > 1).sum())
    out[P + "G-N-UPM-QUE-CRUZAN-ESTRATO"] = n_cruzan
    out[P + "G-UPM-ANIDA-EN-EST-DIS"] = "SI" if n_cruzan == 0 else "NO"

    # ── G-5 · catálogo de parentesco ──────────────────────────────────────
    per["parentesco"] = per["parentesco"].fillna("").astype(str).str.strip()
    out[P + "G-N-PARENTESCO-FUERA-DE-CATALOGO"] = int((~per["parentesco"].isin(CATALOGO)).sum())

    if not llave_viv_unica or not terna_per_unica:
        return para("NO-ESTIMABLE-LLAVE-NO-UNICA")

    # ── §2 · el estimando de C1, paso a paso ──────────────────────────────
    ta_ok = viv["tipo_adqui"].notna() & (viv["tipo_adqui"].astype(str).str.strip() != "")
    universo_viv = viv[ta_ok]
    out[P + "A-N-VIVIENDAS-TIPO-ADQUI-NO-BLANCO"] = int(len(universo_viv))
    out[P + "A-N-VIVIENDAS-EXCLUIDAS-TIPO-ADQUI-BLANCO"] = int((~ta_ok).sum())
    pesos_hogar = universo_viv.set_index("folioviv")["factor"]
    est_de_viv = pd.Series(est_txt.values, index=viv["folioviv"].values)
    upm_de_viv = pd.Series(upm_txt.values, index=viv["folioviv"].values)

    # 2. ids_eder: ternas de historiavida como texto strip (C1 verbatim)
    ids_eder = set(zip(hv["folioviv"].astype(str).str.strip(),
                       hv["foliohog"].astype(str).str.strip(),
                       hv["id_pobla"].astype(str).str.strip()))
    out[P + "G-N-PERSONAS-HISTORIAVIDA"] = int(len(ids_eder))

    # 3. por hogar, roster COMPLETO
    per["_hogar"] = list(zip(per["folioviv"], per["foliohog"]))
    por_hogar = per.groupby("_hogar")["parentesco"].agg(
        _hay_cod6=lambda s: (s == C_ASC).any(),
        _hay_cod7=lambda s: (s == C_SUE).any(),
    )
    per["_id3"] = list(zip(per["folioviv"].astype(str).str.strip(),
                           per["foliohog"].astype(str).str.strip(),
                           per["id_pobla"].astype(str).str.strip()))
    per_eder = per[per["_id3"].isin(ids_eder)]
    out[P + "A-N-PERSONAS-ROSTER-EN-EDER"] = int(len(per_eder))

    # 4. ego = jefe o cónyuge
    ego = per_eder[per_eder["parentesco"].isin([C_JEFE, C_CONY])].copy()
    out[P + "A-N-EGO-JEFE-O-CONYUGE"] = int(len(ego))
    out[P + "A-N-EGO-JEFE"] = int((ego["parentesco"] == C_JEFE).sum())
    out[P + "A-N-EGO-CONYUGE"] = int((ego["parentesco"] == C_CONY).sum())
    ego = ego.join(por_hogar, on="_hogar")

    # 5. desenlace
    es_jefe = ego["parentesco"] == C_JEFE
    es_cony = ego["parentesco"] == C_CONY
    asc = (es_jefe & ego["_hay_cod6"]) | (es_cony & ego["_hay_cod7"])
    sue = (es_jefe & ego["_hay_cod7"]) | (es_cony & ego["_hay_cod6"])
    ego["_d"] = (asc | sue).astype(int)
    out[P + "A-N-EGO-CON-ASCENDIENTE"] = int(asc.sum())
    out[P + "A-N-EGO-CON-SUEGRO"] = int(sue.sum())

    # 6. peso = factor de la vivienda del universo
    ego["_w"] = pd.to_numeric(ego["folioviv"].map(pesos_hogar), errors="coerce")
    w_ok = ego["_w"].notna() & np.isfinite(ego["_w"].to_numpy(dtype=float)) & (ego["_w"] > 0)
    out[P + "A-N-SIN-PONDERADOR"] = int((~w_ok).sum())
    U = ego[w_ok].copy()
    out[P + "A-N-U"] = int(len(U))
    if len(U) == 0:
        return para("NO-ESTIMABLE-UNIVERSO-VACIO")

    # G-4 · embudo de C1 como guardia con valor esperado
    disc = []
    for clave, rid in (("n_filas_persona", "G-N-FILAS-PERSONA"),
                       ("n_personas_historiavida", "G-N-PERSONAS-HISTORIAVIDA"),
                       ("n_ego_jefe_o_conyuge", "A-N-EGO-JEFE-O-CONYUGE"),
                       ("n_u", "A-N-U")):
        if int(esp[clave]) != int(out[P + rid]):
            disc.append(f"{rid}={out[P + rid]}!={esp[clave]}")
    out[P + "A-EMBUDO-C1"] = "EMBUDO-COINCIDE" if not disc else "EMBUDO-DISCORDA:" + ";".join(disc)

    U["_est"] = U["folioviv"].map(est_de_viv).fillna("").astype(str)
    U["_upm"] = U["folioviv"].map(upm_de_viv).fillna("").astype(str)
    dis_ok = (U["_est"] != "") & (U["_upm"] != "")
    out[P + "A-N-SIN-DISENO"] = int((~dis_ok).sum())
    n_viv_u_sin = int(((est_de_viv.reindex(universo_viv["folioviv"]).fillna("") == "") |
                       (upm_de_viv.reindex(universo_viv["folioviv"]).fillna("") == "")).sum())
    out[P + "G-VEREDICTO-DISENO"] = ("DISENO-PRESENTE" if n_viv_u_sin == 0 else
                                     (f"DISENO-PARCIAL:{n_viv_u_sin}" if n_viv_u_sin < len(universo_viv)
                                      else "NO-ESTIMABLE-DISENO-AUSENTE"))

    d = U["_d"].to_numpy(dtype=float)
    w = U["_w"].to_numpy(dtype=float)
    out[P + "A-N-D-UNO"] = int((d == 1).sum())
    out[P + "A-N-D-CERO"] = int((d == 0).sum())
    out[P + "A-MASA-FACTOR-U"] = _num(np.sum(w))
    pA = _p(d, w)
    out[P + "A-P"] = _num(pA)
    out[P + "A-P-COMPLEMENTO"] = _num(_p(1.0 - d, w))
    out[P + "A-SUMA"] = _num(pA + out[P + "A-P-COMPLEMENTO"]) if pA is not None else None
    out[P + "A-VEREDICTO"] = "TASA-REPORTADA"

    def varianza(pref, dd, ww, est, upmv, mask):
        if mask.sum() == 0:
            out[P + pref + "METODO-IC"] = "NO-ESTIMABLE-DISENO-INCOMPLETO"
            return
        serie, n_e, n_u, n_una = _bootstrap(dd[mask], ww[mask], est[mask], upmv[mask],
                                            replicas, semilla)
        out[P + pref + "N-ESTRATOS"] = int(n_e)
        out[P + pref + "N-UPM"] = int(n_u)
        out[P + pref + "N-ESTRATOS-UPM-UNICA"] = int(n_una)
        lo, hi = _pct(serie)
        out[P + pref + "IC-LO"] = _num(lo)
        out[P + pref + "IC-HI"] = _num(hi)
        out[P + pref + "METODO-IC"] = ("IC-CON-ESTRATOS-DE-UPM-UNICA" if n_una > 0
                                       else "IC-BOOTSTRAP-UPM-EN-ESTRATO")
        ee = _taylor(dd[mask], ww[mask], est[mask], upmv[mask])
        pp = _p(dd, ww)
        out[P + pref + "EE-TAYLOR"] = _num(ee)
        if ee is not None and pp is not None:
            out[P + pref + "IC-LO-TAYLOR"] = _num(pp - z95 * ee)
            out[P + pref + "IC-HI-TAYLOR"] = _num(pp + z95 * ee)

    varianza("A-", d, w, U["_est"].to_numpy(), U["_upm"].to_numpy(), dis_ok.to_numpy())

    # ── §4.1 · control positivo del punto ─────────────────────────────────
    ref = float(gen1["A_P"])
    delta = pA - ref
    out[P + "A-DELTA-VS-GEN1"] = _num(delta)
    out[P + "A-REPRODUCE-GEN1"] = "REPRODUCE" if abs(delta) <= tol else "NO-REPRODUCE"
    out[P + "A-DELTA-N-VS-GEN1"] = int(len(U)) - int(gen1["N_U"])
    dgr = round(pA, grano) - ref
    out[P + "A-ADOPCION-DELTA"] = _num(dgr)
    out[P + "A-ADOPCION"] = ("LISTADO-PARA-MESA-REPRODUCE"
                             if out[P + "A-REPRODUCE-GEN1"] == "REPRODUCE" and abs(dgr) < 1e-12
                             else "LISTADO-PARA-MESA-NO-REPRODUCE")

    # ── §3.3 · sensibilidad de ponderador (B) ─────────────────────────────
    if ant is None:
        return out
    if not terna_ant_unica:
        out[P + "B-VEREDICTO"] = "NO-ESTIMABLE-LLAVE-NO-UNICA"
        return out
    fp = ant.set_index(["folioviv", "foliohog", "id_pobla"])["factor_per"]
    UB = U.merge(fp.rename("_fp").reset_index(), on=["folioviv", "foliohog", "id_pobla"],
                 how="left")
    UB["_fp"] = pd.to_numeric(UB["_fp"], errors="coerce")
    sin = UB["_fp"].isna()
    fpv = UB["_fp"].fillna(np.nan).to_numpy(dtype=float)
    cero = (~sin) & (fpv == 0)
    inval = (~sin) & (~np.isfinite(fpv) | (fpv < 0))
    ok = (~sin) & np.isfinite(fpv) & (fpv > 0)
    out[P + "B-N-SIN-FACTOR-PER"] = int(sin.sum())
    out[P + "B-N-FACTOR-PER-CERO"] = int(cero.sum())
    out[P + "B-N-FACTOR-PER-INVALIDO"] = int(inval.sum())
    out[P + "B-N-U"] = int(ok.sum())
    if ok.sum() == 0:
        out[P + "B-VEREDICTO"] = "NO-ESTIMABLE-UNIVERSO-VACIO"
        return out
    UBk = UB[ok]
    dB = UBk["_d"].to_numpy(dtype=float)
    wB = UBk["_fp"].to_numpy(dtype=float)
    disB = ((UBk["_est"] != "") & (UBk["_upm"] != "")).to_numpy()
    out[P + "B-N-SIN-DISENO"] = int((~disB).sum())
    out[P + "B-MASA-FACTOR-PER-U"] = _num(np.sum(wB))
    pB = _p(dB, wB)
    out[P + "B-P"] = _num(pB)
    out[P + "B-VEREDICTO"] = "TASA-REPORTADA"
    varianza("B-", dB, wB, UBk["_est"].to_numpy(), UBk["_upm"].to_numpy(), disB)
    out[P + "B-DELTA-VS-A"] = _num(pB - pA)
    return out
