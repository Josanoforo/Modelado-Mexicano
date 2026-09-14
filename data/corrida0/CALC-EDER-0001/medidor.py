"""`CALC-EDER-0001` — re-estimación con diseño muestral de la tasa de fase 1
`familia.corresidencia.adulto_familiar` (EDER 2017).

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-DISENO-FASE1-CIERRE`, ANTES
DE LEER UN SOLO VALOR DEL MICRODATO. Spec sellada que lo gobierna:
`forense/prereg-caja/EDER-CORRESIDENCIA-DISENO-spec-v1_0.md`
(`prereg-caja-EDER-CORRESIDENCIA-DISENO`, sha `b6c75544…`).

Lo único abierto al escribir este archivo: el manifiesto, `eder2017_fd.pdf`,
`eder2017_descripcion_calculoR.pdf`, la lista de miembros del ZIP, la primera
línea (cabecera) de los cinco `.csv`, el conteo de líneas de `vivienda.csv` y
`antecedentes.csv`, `data/diseno-muestral.yaml`, el inventario, la propuesta
`tramite-ola5-propuesta-v0.yaml`, `tools/tasas_base_fase1.py` (cuyo
estimando se reproduce paso a paso, E.3) y `demanda-*.tsv`.

Sucesor de la tasa de fase 1 (p=0.996086, n=14887, `factor`). NO releva
ninguna `CORR-*`, NO toca `milpa/` ni ningún sello previo.
"""
from __future__ import annotations

import io
import math
import zipfile

import numpy as np
import pandas as pd

# ── constantes de la spec congelada ───────────────────────────────────────

ZIP_ID = "eder_2017_eder2017_bases_csv"
T_VIV = "vivienda.csv"
T_HV = "historiavida.csv"
T_ANT = "antecedentes.csv"

COR_VARS = ["padre_cor", "madre_cor", "hnos_cor", "suegro_cor", "suegra_cor"]
COLS_VIV = ["folioviv", "tipo_adqui", "factor", "est_dis", "upm"]
COLS_HV = ["folioviv", "foliohog", "id_pobla"] + COR_VARS
COLS_ANT = ["folioviv", "foliohog", "id_pobla", "factor_per"]

SEP = "␟"          # separador de llave compuesta: no aparece en el dato


# ── utilidades ────────────────────────────────────────────────────────────

def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como cadena."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _cod(s):
    """Texto -> entero si parsea como flotante finito de parte fraccionaria
    nula; `None` en cualquier otro caso. Sólo se usa en la guardia de tipo
    G-4; el estimando sucesor usa la CADENA exacta `'1'` (fase 1, E.3)."""
    if s is None:
        return None
    t = str(s).strip()
    if not t:
        return None
    try:
        f = float(t)
    except ValueError:
        return None
    if f != f or f in (float("inf"), float("-inf")):
        return None
    e = int(f)
    return e if float(e) == f else None


def _perfil(valores):
    anchos = {}
    for v in valores:
        anchos[len(v)] = anchos.get(len(v), 0) + 1
    return ";".join(f"ancho={k}:{anchos[k]}" for k in sorted(anchos)) or "vacio"


def _cabecera(zf, miembro):
    """Primera línea del CSV, decodificada como fase 1 (latin-1): el BOM UTF-8
    queda como prefijo del primer nombre. Es metadato, no valor."""
    with zf.open(miembro) as fh:
        return fh.readline().decode("latin-1").rstrip("\r\n").split(",")


def _col(nombres, sufijo):
    """Resuelve una columna por sufijo (el BOM contamina el primer nombre)."""
    exactos = [c for c in nombres if c == sufijo]
    if exactos:
        return exactos[0]
    cand = [c for c in nombres if c.endswith(sufijo)]
    return cand[0] if cand else None


def _lee_csv(zf, miembro, columnas, dtype_str=()):
    """Lee SOLO las columnas pedidas con la misma lectura que fase 1
    (`encoding='latin-1'`, `low_memory=False`); `est_dis`/`upm` como texto
    crudo. Devuelve `(df, faltantes, n_columnas_cabecera)` con las columnas
    renombradas a su nombre sin BOM."""
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
    """Bootstrap de UPM CON REEMPLAZO dentro de estrato, conservando el número
    de UPM por estrato. Un estrato con UNA sola UPM se re-muestrea a sí mismo:
    aporta varianza cero, no se colapsa y no se descarta. Devuelve
    `(serie_p, n_estratos, n_upm, n_estratos_upm_unica)`."""
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
    for e in estratos:                       # orden fijo: np.unique ordena
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
    """EE de p = Σwd/Σw por linealización: z_i = w_i (d_i − p)/Σw, totales
    por UPM, Σ_h n_h/(n_h−1) Σ_j (z_hj − z̄_h)². Estrato con UNA UPM: entra
    con (z_h1 − z̄_global)² y factor 1 — aproximación DECLARADA de
    `survey.lonely.psu="adjust"`, la receta R de INEGI para EDER."""
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


# ── medidor ───────────────────────────────────────────────────────────────

def medir(inputs, contrato):
    par = contrato["parametros"]
    replicas = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    z95 = float(par["z_95"])
    tol = float(par["umbral_replica_gen1"])
    grano = int(par["grano_milpa_decimales"])
    gen1 = par["valores_gen1_referencia"]
    n_gen1 = par["n_gen1_referencia"]
    cod = par["codificacion"]
    cor_vars = list(cod["cor_vars"])
    UNO = str(cod["cor_uno_cadena"])

    P = "RESULT-EDER-"
    out = {P + s: None for s in par["sufijos_result"]}
    # Un `entero` declarado NUNCA puede salir null: arranca en 0 y toda rama
    # de salida lo deja escrito. Un `texto` declarado arranca NO-ESTIMABLE.
    for s in par["sufijos_result"]:
        entero = (s.startswith(("G-N-", "A-N-", "B-N-")) or s == "A-DELTA-N-VS-GEN1")
        texto = ("VEREDICTO" in s or "REPRODUCE" in s or "METODO-IC" in s or
                 s.startswith(("G-LLAVE", "G-PERFIL", "G-UPM-ANIDA")) or
                 s == "A-ADOPCION-P3" or s == "B-CLAUSULA-SE-MUEVE-SI")
        if entero:
            out[P + s] = 0
        elif texto:
            out[P + s] = "NO-ESTIMABLE"

    def para(v_a, v_b=None, estructura=None):
        out[P + "A-VEREDICTO"] = v_a
        out[P + "B-VEREDICTO"] = v_b if v_b is not None else v_a
        if estructura is not None:
            out[P + "G-VEREDICTO-ESTRUCTURA"] = estructura
        out[P + "A-ADOPCION-P3"] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    # ── G-1 · miembros del ZIP ────────────────────────────────────────────
    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    miembros = set(zf.namelist())
    out[P + "G-N-MIEMBROS-ZIP"] = len(miembros)
    for m in (T_VIV, T_HV, T_ANT):
        if m not in miembros:
            return para(f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{m}",
                        estructura=f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{m}")

    # ── G-2 · columnas (cabecera primero, valores después) ────────────────
    viv, falt, ncol_v = _lee_csv(zf, T_VIV, COLS_VIV, dtype_str=("est_dis", "upm"))
    out[P + "G-N-COLUMNAS-VIVIENDA"] = ncol_v
    if falt:
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}",
                    estructura=f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}")
    hv, falt, ncol_h = _lee_csv(zf, T_HV, COLS_HV)
    out[P + "G-N-COLUMNAS-HISTORIAVIDA"] = ncol_h
    if falt:
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}",
                    estructura=f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}")
    ant, falt, ncol_a = _lee_csv(zf, T_ANT, COLS_ANT)
    out[P + "G-N-COLUMNAS-ANTECEDENTES"] = ncol_a
    if falt:
        # la familia B se cae; A sigue
        ant = None
        out[P + "B-VEREDICTO"] = f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}"
        out[P + "G-VEREDICTO-ESTRUCTURA"] = f"NO-ESTIMABLE-COLUMNA-AUSENTE:{falt[0]}"
    else:
        out[P + "G-VEREDICTO-ESTRUCTURA"] = "ESTRUCTURA-OK"

    out[P + "G-N-FILAS-VIVIENDA"] = int(len(viv))
    out[P + "G-N-FILAS-HISTORIAVIDA"] = int(len(hv))
    out[P + "G-N-FILAS-ANTECEDENTES"] = int(len(ant)) if ant is not None else 0

    # ── G-3 · llaves ──────────────────────────────────────────────────────
    llave_viv_unica = bool(viv["folioviv"].is_unique)
    out[P + "G-LLAVE-VIVIENDA-FOLIOVIV-UNICA"] = "SI" if llave_viv_unica else "NO"
    if ant is not None:
        terna_unica = not bool(ant.duplicated(["folioviv", "foliohog", "id_pobla"]).any())
        out[P + "G-LLAVE-ANTECEDENTES-TERNA-UNICA"] = "SI" if terna_unica else "NO"
    else:
        terna_unica = False

    # ── G · perfil del diseño en vivienda.csv (texto crudo) ───────────────
    est_txt = viv["est_dis"].fillna("").astype(str).str.strip()
    upm_txt = viv["upm"].fillna("").astype(str).str.strip()
    fac_v = pd.to_numeric(viv["factor"], errors="coerce")
    out[P + "G-N-VIVIENDA-SIN-EST-DIS"] = int((est_txt == "").sum())
    out[P + "G-N-VIVIENDA-SIN-UPM"] = int((upm_txt == "").sum())
    out[P + "G-N-VIVIENDA-SIN-FACTOR"] = int((~np.isfinite(fac_v.to_numpy(dtype=float)) |
                                             (fac_v.fillna(0).to_numpy() <= 0)).sum())
    out[P + "G-PERFIL-EST-DIS"] = _perfil(est_txt[est_txt != ""].tolist())
    out[P + "G-PERFIL-UPM"] = _perfil(upm_txt[upm_txt != ""].tolist())
    out[P + "G-N-EST-DIS-DISTINTOS-VIVIENDA"] = int(est_txt[est_txt != ""].nunique())
    out[P + "G-N-UPM-DISTINTOS-VIVIENDA"] = int(upm_txt[upm_txt != ""].nunique())
    con_dis = (est_txt != "") & (upm_txt != "")
    cruzan = (pd.DataFrame({"e": est_txt[con_dis], "u": upm_txt[con_dis]})
              .drop_duplicates().groupby("u")["e"].nunique())
    n_cruzan = int((cruzan > 1).sum())
    out[P + "G-N-UPM-QUE-CRUZAN-ESTRATO"] = n_cruzan
    out[P + "G-UPM-ANIDA-EN-EST-DIS"] = "SI" if n_cruzan == 0 else "NO"

    # ── G-4 · trampa de tipo, medida ──────────────────────────────────────
    padre_txt = hv["padre_cor"].astype(str).str.strip()
    n_cad = int((padre_txt == UNO).sum())
    n_num = int(sum(1 for v in padre_txt.tolist() if _cod(v) == 1))
    out[P + "G-N-PADRE-COR-CADENA-UNO"] = n_cad
    out[P + "G-N-PADRE-COR-NUMERICO-UNO"] = n_num
    if n_cad and n_cad == n_num:
        out[P + "G-VEREDICTO-TIPO-COR"] = "CADENA-Y-NUMERO-COINCIDEN"
    elif n_num and not n_cad:
        out[P + "G-VEREDICTO-TIPO-COR"] = "SOLO-NUMERO-ACIERTA"
    elif n_cad and not n_num:
        out[P + "G-VEREDICTO-TIPO-COR"] = "SOLO-CADENA-ACIERTA"
    elif not n_cad and not n_num:
        out[P + "G-VEREDICTO-TIPO-COR"] = "NINGUNO-ACIERTA"
    else:
        out[P + "G-VEREDICTO-TIPO-COR"] = "CADENA-Y-NUMERO-DIFIEREN"

    if not llave_viv_unica:
        return para("NO-ESTIMABLE-LLAVE-NO-UNICA")

    # ── §2 · el estimando de fase 1, paso a paso ──────────────────────────
    # 1. universo de viviendas: tipo_adqui no nulo y no blanco
    ta_ok = viv["tipo_adqui"].notna() & (viv["tipo_adqui"].astype(str).str.strip() != "")
    universo_viv = viv[ta_ok]
    out[P + "A-N-VIVIENDAS-TIPO-ADQUI-NO-BLANCO"] = int(len(universo_viv))
    out[P + "A-N-VIVIENDAS-EXCLUIDAS-TIPO-ADQUI-BLANCO"] = int((~ta_ok).sum())
    pesos_hogar = universo_viv.set_index("folioviv")["factor"]
    est_de_viv = pd.Series(est_txt.values, index=viv["folioviv"].values)
    upm_de_viv = pd.Series(upm_txt.values, index=viv["folioviv"].values)

    # 2-3. persona y desenlace (cadena exacta '1' en alguna fila)
    for c in cor_vars:
        hv[c] = hv[c].astype(str).str.strip()
    hv["_cor"] = hv[cor_vars].eq(UNO).any(axis=1)
    personas = (hv.groupby(["folioviv", "foliohog", "id_pobla"])["_cor"]
                .max().reset_index().rename(columns={"_cor": "_d"}))
    personas["_d"] = personas["_d"].astype(int)
    out[P + "A-N-PERSONAS-HISTORIAVIDA"] = int(len(personas))

    # 4. peso = factor de la vivienda del universo; sin peso -> fuera
    personas["_w"] = personas["folioviv"].map(pesos_hogar)
    personas["_w"] = pd.to_numeric(personas["_w"], errors="coerce")
    w_ok = personas["_w"].notna() & np.isfinite(personas["_w"].to_numpy(dtype=float)) & (personas["_w"] > 0)
    out[P + "A-N-SIN-PONDERADOR"] = int((~w_ok).sum())
    U = personas[w_ok].copy()
    out[P + "A-N-U"] = int(len(U))
    if len(U) == 0:
        return para("NO-ESTIMABLE-UNIVERSO-VACIO")

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
    out[P + "A-DELTA-N-VS-GEN1"] = int(len(U)) - int(n_gen1["U_A"])
    dgr = round(pA, grano) - ref
    out[P + "A-ADOPCION-P3-DELTA"] = _num(dgr)
    out[P + "A-ADOPCION-P3"] = ("LISTADO-PARA-MESA-REPRODUCE"
                                if out[P + "A-REPRODUCE-GEN1"] == "REPRODUCE" and abs(dgr) < 1e-12
                                else "LISTADO-PARA-MESA-NO-REPRODUCE")

    # ── §3.3 · sensibilidad de ponderador (B) ─────────────────────────────
    if ant is None:
        return out
    if not terna_unica:
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
    lo1, hi1 = float(gen1["A_IC_LO_FASE1"]), float(gen1["A_IC_HI_FASE1"])
    out[P + "B-CLAUSULA-SE-MUEVE-SI"] = ("DENTRO-DEL-IC-FASE1" if lo1 <= pB <= hi1
                                         else "FUERA-DEL-IC-FASE1")
    return out
