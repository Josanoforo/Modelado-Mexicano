"""`CALC-ENVIPE-U4-2012` — `U4` (unidad PERSONA, `FAC_ELE`) en ENVIPE 2012 por
la ruta declarada: delito -> persona por `(hogar, R_SEL)`; ponderador y diseño
por hogar desde `tper_vic.dbf`; existencia verificada en `tsdem.DBF` por
`N_REN == R_SEL`, con cardinalidad medida.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1`
(pieza P2, `NC-0099`), ANTES DE LEER UN SOLO VALOR DEL MICRODATO. Spec sellada:
`forense/prereg-caja/ENVIPE-2012-U4-spec-v1_0.md`. Lector DBF copiado de
`CALC-R-CIV-M-01/medidor.py`; varianza copiada de `CALC-EDER-0001/medidor.py`.
"""
from __future__ import annotations

import math
import struct
import zipfile

import numpy as np

SEP = "␟"
BORRADO = 0x2A


def _lee_dbf(crudo: bytes, columnas):
    nrec, hlen, rlen = struct.unpack("<IHH", crudo[4:12])
    codepage = crudo[29]
    campos, pos, despl = [], 32, 1
    while pos + 32 <= hlen and crudo[pos] != 0x0D:
        b = crudo[pos:pos + 32]
        nombre = b[0:11].split(b"\x00")[0].decode("latin-1").strip().upper()
        largo = b[16]
        campos.append((nombre, despl, largo))
        despl += largo
        pos += 32
    mapa = {n: (o, l) for n, o, l in campos}
    faltantes = [c for c in columnas if c not in mapa]
    perfil = (f"nrec_cabecera={nrec};rlen={rlen};hlen={hlen};"
              f"n_campos={len(campos)};codepage=0x{codepage:02x}")
    if faltantes:
        return [], faltantes, perfil
    filas, borrados, truncados = [], 0, 0
    for i in range(nrec):
        a = hlen + i * rlen
        reg = crudo[a:a + rlen]
        if len(reg) < rlen:
            truncados += 1
            break
        if reg[0] == BORRADO:
            borrados += 1
            continue
        filas.append({c: reg[mapa[c][0]:mapa[c][0] + mapa[c][1]].decode("latin-1")
                      for c in columnas})
    perfil += f";registros_borrados={borrados};registros_truncados={truncados};n_leidos={len(filas)}"
    return filas, [], perfil


def _codigo(s):
    t = str(s).strip() if s is not None else ""
    if not t:
        return None
    try:
        return int(t)
    except ValueError:
        return None


def _flotante(s):
    t = str(s).strip() if s is not None else ""
    if not t:
        return None
    try:
        f = float(t)
    except ValueError:
        return None
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _num(v):
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _p(d, w):
    sw = float(np.sum(w))
    if sw <= 0:
        return None
    return float(np.sum(w * d) / sw)


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


def _perfil_texto(valores):
    anchos = {}
    for v in valores:
        k = f"len{len(v)}"
        anchos[k] = anchos.get(k, 0) + 1
    bordes = sum(1 for v in valores if v != v.strip())
    return ";".join(f"{k}={anchos[k]}" for k in sorted(anchos)) + f";bordes_con_espacio={bordes}"


def medir(inputs, contrato):
    par = contrato["parametros"]
    replicas = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    z95 = float(par["z_95"])
    tol = float(par["tolerancia_control_u1"])
    cod = par["codificacion"]
    ref = par["control_u1_referencia"]
    T_MOD, T_PER, T_SD = par["tablas"]["modulo"], par["tablas"]["personas"], par["tablas"]["sociodem"]
    C1_UNO = {int(x) for x in cod["C1_uno"]}
    C1_CERO = {int(x) for x in cod["C1_cero"]}
    C2_UNO = {int(x) for x in cod["C2_uno"]}
    PERSONALES = {int(x) for x in cod["bpcod_personales"]}
    HOGAR_KEYS = ("CONTROL", "VIV_SEL", "HOGAR")

    P = "RESULT-ENVIPE-U4-12-"
    out = {P + s: None for s in par["sufijos_result"]}
    for s in par["sufijos_result"]:
        if s.startswith(("N-", "G-N-", "G-PER-N-", "G-TSDEM-N-")):
            out[P + s] = 0
        elif s in ("ESTADO", "METODO-IC", "G-CONTROL-U1") or s.startswith(("PERFIL", "G-TSDEM-PERFIL", "G-PERFIL")):
            out[P + s] = "NO-ESTIMABLE"

    def para(estado):
        out[P + "ESTADO"] = estado
        return out

    zf = zipfile.ZipFile(inputs[par["payload_id"]]["ruta_absoluta"])
    miembros = set(zf.namelist())
    out[P + "G-N-MIEMBROS-ZIP"] = len(miembros)
    for m in (T_MOD, T_PER, T_SD):
        if m not in miembros:
            return para(f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{m}")

    # ── Tmod_Vic ──────────────────────────────────────────────────────────
    mod, falt, perfil_mod = _lee_dbf(zf.read(T_MOD), list(HOGAR_KEYS) + ["R_SEL", "BPCOD", "BP1_20", "BP1_23", "FAC_DEL"])
    out[P + "PERFIL-DBF-MODULO"] = perfil_mod
    if falt:
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{T_MOD}:{falt[0]}")
    out[P + "N-FILAS-MODULO"] = len(mod)
    bp = {}
    for f in mod:
        k = f["BPCOD"].strip()
        bp[k] = bp.get(k, 0) + 1
    out[P + "PERFIL-BPCOD"] = ";".join(f"{k}={bp[k]}" for k in sorted(bp))

    u1 = []
    n_blanco = n_99 = n_fuera = n_sinw = 0
    for f in mod:
        c = _codigo(f["BP1_23"])
        if c is None:
            n_blanco += 1
        elif c == 99:
            n_99 += 1
        elif not (1 <= c <= 9):
            n_fuera += 1
        b = _codigo(f["BPCOD"])
        if b in PERSONALES and _codigo(f["BP1_20"]) == 2 and c is not None and 1 <= c <= 8:
            w = _flotante(f["FAC_DEL"])
            if w is None or w <= 0:
                n_sinw += 1
                continue
            u1.append({"hogar": tuple(f[k].strip() for k in HOGAR_KEYS), "r_sel": _codigo(f["R_SEL"]),
                       "r_sel_txt": f["R_SEL"].strip(), "cod": c, "w": w})
    out[P + "N-BP1-23-BLANCO"] = n_blanco
    out[P + "N-BP1-23-99"] = n_99
    out[P + "N-BP1-23-FUERA-DE-CATALOGO"] = n_fuera
    out[P + "N-U1-SIN-PONDERADOR"] = n_sinw
    out[P + "N-U1"] = len(u1)
    if u1:
        w1 = np.array([r["w"] for r in u1], dtype=float)
        d1 = np.array([1.0 if r["cod"] in C1_UNO else 0.0 for r in u1])
        p1 = _p(d1, w1)
        out[P + "P-C1-U1"] = _num(p1)
        out[P + "MASA-FAC-DEL-U1"] = _num(np.sum(w1))
        ok = (abs(p1 - float(ref["P_C1_U1"])) <= tol and len(u1) == int(ref["N_U1"])
              and len(mod) == int(ref["N_FILAS_TABLA"]))
        out[P + "G-CONTROL-U1"] = "REPRODUCE" if ok else "NO-REPRODUCE"
    else:
        out[P + "G-CONTROL-U1"] = "NO-COMPARABLE"
    out[P + "N-U1-R-SEL-BLANCO"] = sum(1 for r in u1 if r["r_sel"] is None)

    # ── tper_vic: por hogar ───────────────────────────────────────────────
    per, falt, perfil_per = _lee_dbf(zf.read(T_PER), list(HOGAR_KEYS) + ["N_INF", "R_SEL", "TOT_PER", "FAC_ELE", "EST", "UPM"])
    out[P + "PERFIL-DBF-PERSONAS"] = perfil_per
    if falt:
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{T_PER}:{falt[0]}")
    out[P + "N-FILAS-PERSONAS"] = len(per)
    hog = {}
    for f in per:
        h = tuple(f[k].strip() for k in HOGAR_KEYS)
        g = hog.setdefault(h, {"n": 0, "tot": set(), "rsel": set(), "fac": [], "dis": set()})
        g["n"] += 1
        g["tot"].add(f["TOT_PER"].strip())
        g["rsel"].add(f["R_SEL"].strip())
        g["fac"].append(f["FAC_ELE"].strip())
        g["dis"].add((f["EST"].strip(), f["UPM"].strip()))
    out[P + "G-PER-N-HOGARES"] = len(hog)
    out[P + "G-PER-N-HOGARES-FILAS-NE-TOT-PER"] = sum(
        1 for g in hog.values() if len(g["tot"]) != 1 or _codigo(next(iter(g["tot"]))) != g["n"])
    out[P + "G-PER-N-HOGARES-R-SEL-MULTI"] = sum(1 for g in hog.values() if len(g["rsel"]) > 1)
    out[P + "G-PER-N-HOGARES-FAC-ELE-MULTI"] = sum(1 for g in hog.values() if len(set(g["fac"])) > 1)
    out[P + "G-PER-N-HOGARES-EST-UPM-MULTI"] = sum(1 for g in hog.values() if len(g["dis"]) > 1)
    out[P + "G-PERFIL-DISENO-PERSONAS"] = ("ESTRATO[" + _perfil_texto([f["EST"] for f in per]) + "] UPM["
                                          + _perfil_texto([f["UPM"] for f in per]) + "]")
    # resolución §3.1
    n_unica_valida = 0
    resuelto = {}
    for h, g in hog.items():
        facs = set(g["fac"])
        if len(facs) == 1:
            w = _flotante(next(iter(facs)))
        else:
            validas = [x for x in g["fac"] if (_flotante(x) is not None and _flotante(x) > 0)]
            if len(validas) == 1:
                w = _flotante(validas[0])
                n_unica_valida += 1
            else:
                w = "AMBIGUO"
        dis = next(iter(g["dis"])) if len(g["dis"]) == 1 else None
        rsel = _codigo(next(iter(g["rsel"]))) if len(g["rsel"]) == 1 else None
        resuelto[h] = {"w": w, "dis": dis, "rsel": rsel}
    out[P + "N-HOGARES-FAC-ELE-RESUELTO-POR-UNICA-VALIDA"] = n_unica_valida

    # ── tsdem ─────────────────────────────────────────────────────────────
    sd, falt, perfil_sd = _lee_dbf(zf.read(T_SD), list(HOGAR_KEYS) + ["N_REN", "EDAD"])
    out[P + "PERFIL-DBF-SOCIODEM"] = perfil_sd
    if falt:
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{T_SD}:{falt[0]}")
    out[P + "N-FILAS-SOCIODEM"] = len(sd)
    sdh = {}
    nren_perf = {}
    for f in sd:
        h = tuple(f[k].strip() for k in HOGAR_KEYS)
        sdh.setdefault(h, []).append((_codigo(f["N_REN"]), _codigo(f["EDAD"])))
        t = f["N_REN"]
        k = ("izq" if t != t.lstrip() else "der" if t != t.rstrip() else "sin_espacio")
        nren_perf[k] = nren_perf.get(k, 0) + 1
    out[P + "G-TSDEM-PERFIL-N-REN"] = ";".join(f"{k}={nren_perf[k]}" for k in sorted(nren_perf))
    out[P + "G-TSDEM-N-HOGARES"] = len(sdh)
    out[P + "G-TSDEM-N-HOGARES-FILAS-NE-TPER"] = sum(
        1 for h, g in hog.items() if len(sdh.get(h, [])) != g["n"]) + sum(1 for h in sdh if h not in hog)

    # ── U4: colapso GEN1 y ruta ───────────────────────────────────────────
    por_persona = {}
    n_hogar_sin_per = n_rsel_disc = n_rsel_blanco = 0
    for r in u1:
        if r["r_sel"] is None:
            n_rsel_blanco += 1
            continue
        g = resuelto.get(r["hogar"])
        if g is None:
            n_hogar_sin_per += 1
            continue
        if g["rsel"] != r["r_sel"]:
            n_rsel_disc += 1
            continue
        pid = (r["hogar"], r["r_sel"])
        q = por_persona.setdefault(pid, {"d1": 0, "d2": 0, "n": 0})
        q["d1"] = max(q["d1"], 1 if r["cod"] in C1_UNO else 0)
        q["d2"] = max(q["d2"], 1 if r["cod"] in C2_UNO else 0)
        q["n"] += 1
    out[P + "N-DELITOS-HOGAR-SIN-TPER-VIC"] = n_hogar_sin_per
    out[P + "N-DELITOS-R-SEL-DISCORDA"] = n_rsel_disc
    out[P + "N-DELITOS-R-SEL-BLANCO"] = n_rsel_blanco
    out[P + "N-U4-CANDIDATAS"] = len(por_persona)
    if not por_persona:
        return para("NO-ESTIMABLE-UNIVERSO-VACIO")

    filas = []
    n_fac_amb = n_t0 = n_t1 = n_tm = n_men18 = n_edad_ne = n_dis_amb = 0
    for (h, rsel), q in por_persona.items():
        g = resuelto[h]
        if g["w"] == "AMBIGUO" or g["w"] is None or g["w"] <= 0:
            n_fac_amb += 1
            continue
        matches = [e for (nr, e) in sdh.get(h, []) if nr == rsel]
        if len(matches) == 0:
            n_t0 += 1
            continue
        if len(matches) > 1:
            n_tm += 1
            continue
        n_t1 += 1
        edad = matches[0]
        if edad is None or edad in (98, 99):
            n_edad_ne += 1
        elif edad < 18:
            n_men18 += 1
        if g["dis"] is None:
            n_dis_amb += 1
            e, u = "", ""
        else:
            e, u = g["dis"]
        filas.append({"w": g["w"], "d1": q["d1"], "d2": q["d2"], "e": e, "u": u})
    out[P + "N-U4-FAC-ELE-AMBIGUO"] = n_fac_amb
    out[P + "N-U4-TSDEM-0"] = n_t0
    out[P + "N-U4-TSDEM-1"] = n_t1
    out[P + "N-U4-TSDEM-MULTI"] = n_tm
    out[P + "N-U4-EDAD-MENOR-18"] = n_men18
    out[P + "N-U4-EDAD-NO-ESPECIFICADA"] = n_edad_ne
    out[P + "N-U4-DISENO-AMBIGUO"] = n_dis_amb
    out[P + "N-U4"] = len(filas)
    if not filas:
        return para("NO-ESTIMABLE-JOIN-VACIO")

    w4 = np.array([r["w"] for r in filas], dtype=float)
    d41 = np.array([r["d1"] for r in filas], dtype=float)
    d42 = np.array([r["d2"] for r in filas], dtype=float)
    e4 = np.array([r["e"] for r in filas])
    m4 = np.array([r["u"] for r in filas])
    out[P + "N-U4-D2-UNO"] = int((d42 == 1).sum())
    out[P + "MASA-FAC-ELE-U4"] = _num(np.sum(w4))
    p2 = _p(d42, w4)
    out[P + "P-C2-U4"] = _num(p2)
    out[P + "P-C1-U4"] = _num(_p(d41, w4))
    out[P + "P-C2-U4-COMPLEMENTO"] = _num(_p(1.0 - d42, w4))
    mask = (e4 != "") & (m4 != "")
    out[P + "N-U4-SIN-DISENO"] = int((~mask).sum())
    if mask.sum() == 0:
        out[P + "METODO-IC"] = "NO-ESTIMABLE-DISENO-INCOMPLETO"
    else:
        serie, n_e, n_u, n_una = _bootstrap(d42[mask], w4[mask], e4[mask], m4[mask], replicas, semilla)
        out[P + "N-ESTRATOS"] = int(n_e)
        out[P + "N-UPM"] = int(n_u)
        out[P + "N-ESTRATOS-UPM-UNICA"] = int(n_una)
        lo, hi = _pct(serie)
        out[P + "IC-LO-C2-U4"] = _num(lo)
        out[P + "IC-HI-C2-U4"] = _num(hi)
        out[P + "METODO-IC"] = "IC-CON-ESTRATOS-DE-UPM-UNICA" if n_una > 0 else "IC-BOOTSTRAP-UPM-EN-ESTRATO"
        ee = _taylor(d42[mask], w4[mask], e4[mask], m4[mask])
        out[P + "EE-TAYLOR-C2-U4"] = _num(ee)
        if ee is not None:
            out[P + "IC-LO-TAYLOR-C2-U4"] = _num(p2 - z95 * ee)
            out[P + "IC-HI-TAYLOR-C2-U4"] = _num(p2 + z95 * ee)
        serie1, _, _, _ = _bootstrap(d41[mask], w4[mask], e4[mask], m4[mask], replicas, semilla)
        lo1, hi1 = _pct(serie1)
        out[P + "IC-LO-C1-U4"] = _num(lo1)
        out[P + "IC-HI-C1-U4"] = _num(hi1)
    out[P + "ESTADO"] = "CALCULADO"
    return out
