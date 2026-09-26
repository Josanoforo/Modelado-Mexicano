#!/usr/bin/env python3
"""Medidor ENSU · pisos por segmento, serie trimestral y dictamen por serie.

ACTO GEN2-SEGURIDAD-ENSU-SERIE-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/ENSU-SERIE-spec-v1_0.md y la lista cerrada
forense/analisis/seguridad-ensu/lista-cerrada-P1.md, congeladas en el COMMIT-1
antes de leer un solo valor de microdato ENSU. Este archivo se deposita byte a
byte como `medidor.py` en los dos CALC del acto y despacha por
`parametros.punto_de_entrada`:

  · `pisos`  (CALC-ENSU-PISOS-0001): trimestres de `parametros.olas`, conductas
    x {TOTAL, SEXO, EDAD, ENT, CIUDAD}, un eje a la vez.
  · `serie`  (CALC-ENSU-SERIE-0001): todos los trimestres abiertos 2013T3-2025T4,
    conductas x {TOTAL, SEXO, EDAD}; más CIUDAD sólo para C01-INSEG-CIUDAD; y,
    en la misma corrida, τ² de persistencia por eje y cadencia y el dictamen
    DONDE-CAMBIO por serie (código `tools/series/dictamen.py` ejecutado desde
    sus bytes hasheados).

Lo heredado (bootstrap de UPM dentro de estrato, resumen conservador, `num`) se
ejecuta desde los bytes de la receta común `tools/dominios/salud/pisos_diseno.py`
(input `receta_pisos`). No elige reactivos: la lista cerrada vive en `CONDUCTAS`
y en la spec humana. 2026 es el año RESERVADO (E.6): ninguna ruta puede
resolver a él.
"""
from __future__ import annotations

import hashlib
import io
import math
import re
import struct
import types
import zipfile

import numpy as np
import pandas as pd

ANIOS = tuple(range(2013, 2026))
PAY = {a: f"ensu{a}_bd" for a in ANIOS}          # id lógico -> se resuelve en spec.inputs
INPUTS_REPO = frozenset({"receta_pisos", "dictamen_series"})
Q = ("P", "IC-LO", "IC-HI", "N")

# Lista cerrada (lista-cerrada-P1.md §3). (id, mnemónico 2016+, mnemónico 2013-2015,
# códigos "sí", códigos del universo, cadencia).
CONDUCTAS = (
    ("C01-INSEG-CIUDAD", "BP1_1", "P1", (2,), (1, 2, 9), "T"),
    ("C02-INSEG-CALLE", "BP1_2_03", None, (2,), (1, 2, 9), "T"),
    ("C03-INSEG-CAJERO", "BP1_2_08", None, (2,), (1, 2, 9), "T"),
    ("C04-INSEG-TRANSPORTE", "BP1_2_09", None, (2,), (1, 2, 9), "T"),
    ("C05-EXPECT-EMPEORA", "BP1_3", None, (4,), (1, 2, 3, 4, 9), "T"),
    ("C06-TESTIGO-ROBOS", "BP1_4_3", "P3_3", (1,), (1, 2, 9), "T"),
    ("C07-TESTIGO-PANDILLAS", "BP1_4_4", "P3_4", (1,), (1, 2, 9), "T"),
    ("C08-TESTIGO-DISPAROS", "BP1_4_6", "P3_6", (1,), (1, 2, 9), "T"),
    ("C09-HABITO-OBJETOS-VALOR", "BP1_5_1", "P4_1", (1,), (1, 2, 3, 9), "T"),
    ("C10-HABITO-CAMINAR-NOCHE", "BP1_5_2", "P4_2", (1,), (1, 2, 3, 9), "T"),
    ("C11-HABITO-VISITAR", "BP1_5_3", "P4_3", (1,), (1, 2, 3, 9), "T"),
    ("C12-HABITO-MENORES", "BP1_5_4", "P4_4", (1,), (1, 2, 3, 9), "T"),
    ("C13-POLICIA-MUN-CONFIANZA", "BP1_9_1", None, (1, 2), (1, 2, 3, 4, 9), "T"),
    ("C14-POLICIA-MUN-EFECTIVA", "BP1_8_1", None, (1, 2), (1, 2, 3, 4, 9), "T"),
    ("C15-CORRUPCION-POLICIA", "BP3_6", None, (1,), (1, 2, 9), "S"),
)
FILTRO = {"C15-CORRUPCION-POLICIA": ("BP3_5", (1,))}   # universo condicionado
NOMBRES = tuple(c[0] for c in CONDUCTAS)

EDADES = (("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 96))
SEXOS = ("HOMBRE", "MUJER")
ENTIDADES = tuple(f"{i:02d}" for i in range(1, 33))
CIUDADES = tuple(f"{i:02d}" for i in range(1, 97))       # unión catálogos FD 2016 y 2025
EJES_BASE = {"SEXO": SEXOS, "EDAD": tuple(e for e, _, _ in EDADES)}
Z = 1.959964

ERA1_FIN = "2015T4"          # 2013T3-2015T4: cuestionario P*, llaves ENT/CON/V_SEL
ERA3_INI = "2021T2"          # desde aquí SEXO/EDAD viven en CB
REDISENO = "2016T1"          # par 2015T4->2016T1: CAMBIO-DOCUMENTADO (FD 2016)
T2020 = "2020T3"             # par 2020T1->2020T3: sección 1.6 sustituida (FD sep 2020)
POST_16 = frozenset({"C13-POLICIA-MUN-CONFIANZA", "C14-POLICIA-MUN-EFECTIVA"})


class ParoDeGuardia(RuntimeError):
    pass


# ═══════════════════════════ lectura ═══════════════════════════

def _base(ruta):
    return re.split(r"[/!]", ruta)[-1].lower()


def miembros(zbytes, ruta=""):
    """Recorre zips anidados; produce (ruta, bytes) de cada DBF/CSV."""
    z = zipfile.ZipFile(io.BytesIO(zbytes))
    for i in z.infolist():
        if i.is_dir() or i.filename.startswith("__MACOSX"):
            continue
        n = i.filename.lower()
        if n.endswith(".zip"):
            yield from miembros(z.read(i), ruta + i.filename + "!")
        elif n.endswith((".dbf", ".csv")):
            yield ruta + i.filename, z.read(i)


RX_CB = re.compile(r"^ensu_cb_?(sec1_2_3_)?(\d{2})(\d{2})\.(dbf|csv)$")
RX_CS = re.compile(r"^ensu_cs_?(\d{2})(\d{2})\.(dbf|csv)$")
TRIM = {"03": 1, "06": 2, "09": 3, "12": 4}


def ola_de(ruta, rx):
    m = rx.match(_base(ruta))
    if not m:
        return None
    mm, aa = m.group(m.lastindex - 2), m.group(m.lastindex - 1)
    if mm not in TRIM:
        return None
    return f"20{aa}T{TRIM[mm]}"


def lee_dbf(b, columnas=None):
    nrec = struct.unpack("<I", b[4:8])[0]
    hl = struct.unpack("<H", b[8:10])[0]
    rl = struct.unpack("<H", b[10:12])[0]
    campos, p = [], 32
    while p < hl - 1 and b[p] != 0x0D:
        nombre = b[p:p + 11].split(b"\0")[0].decode("latin-1").strip().upper()
        campos.append((nombre, b[p + 16]))
        p += 32
    desp, off = {}, 1
    for nombre, largo in campos:
        desp[nombre] = (off, largo)
        off += largo
    pedidas = [c for c in (columnas or [n for n, _ in campos]) if c in desp]
    datos = {c: [] for c in pedidas}
    for r in range(nrec):
        s = hl + r * rl
        reg = b[s:s + rl]
        if not reg or reg[:1] == b"*":
            continue
        for c in pedidas:
            o, l = desp[c]
            datos[c].append(reg[o:o + l].decode("latin-1").strip())
    return pd.DataFrame(datos, dtype=str)


def lee_csv(b, columnas=None):
    for enc in ("utf-8-sig", "latin-1"):
        try:
            t = b.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    df = pd.read_csv(io.StringIO(t), dtype=str, keep_default_na=False)
    df.columns = [c.strip().strip('"').upper() for c in df.columns]
    if columnas:
        df = df[[c for c in columnas if c in df.columns]]
    return df.apply(lambda s: s.str.strip())


def lee(ruta, b, columnas=None):
    cols = [c.upper() for c in columnas] if columnas else None
    return lee_dbf(b, cols) if ruta.lower().endswith(".dbf") else lee_csv(b, cols)


def tablas(payload_bytes):
    """{ola: {"cb": (ruta, bytes), "cs": (ruta, bytes)}} de un payload anual."""
    out = {}
    for ruta, b in miembros(payload_bytes):
        o = ola_de(ruta, RX_CB)
        if o:
            out.setdefault(o, {})["cb"] = (ruta, b)
            continue
        o = ola_de(ruta, RX_CS)
        if o:
            out.setdefault(o, {})["cs"] = (ruta, b)
    return out


# ═══════════════════════════ marco por trimestre ═══════════════════════════

def _norm(s):
    s = s.astype(str).str.strip()
    return s.where(~s.str.fullmatch(r"\d+"), s.str.lstrip("0").replace("", "0"))


def _llave(df, cols):
    return pd.concat([_norm(df[c]) for c in cols], axis=1).agg("|".join, axis=1)


def marco(ola, cb_ruta, cb_bytes, cs_ruta, cs_bytes, R):
    """DataFrame por persona seleccionada con _w, _est, _upm, _sexo, _edad, _ent, _cd
    y las columnas de conducta; más diagnósticos."""
    n = R.num
    era1 = ola <= ERA1_FIN
    era3 = ola >= ERA3_INI
    reac = sorted({(c[2] if era1 else c[1]) for c in CONDUCTAS if (c[2] if era1 else c[1])}
                  | {v for v, _ in FILTRO.values()})
    if era1:
        diseno = ["CD", "EDIS", "UPM_DIS", "FACTOR", "ENT", "CON", "V_SEL", "N_HOG", "H_MUD", "N_REN"]
    else:
        diseno = ["CD", "EST_DIS", "UPM_DIS", "FAC_SEL", "UPM", "VIV_SEL", "H_MUD", "R_SEL"]
        diseno += ["SEXO", "EDAD"] if era3 else []
    cb = lee(cb_ruta, cb_bytes, diseno + reac)
    diag = {"PERSONAS": int(len(cb))}
    faltan = [c for c in diseno if c not in cb.columns]
    if faltan:
        raise ParoDeGuardia(f"{ola}: columnas de diseño ausentes en {cb_ruta}: {faltan}")
    if era3:
        sexo, edad = cb["SEXO"], cb["EDAD"]
        diag["JOIN-SIN-CS"] = 0
        diag["CS-DUPLICADA"] = 0
    else:
        cs = lee(cs_ruta, cs_bytes)
        sx = "SEX" if "SEX" in cs.columns else "SEXO"
        ed = "EDA" if "EDA" in cs.columns else "EDAD"
        if era1:
            kcb = _llave(cb, ["ENT", "CON", "V_SEL", "N_HOG", "H_MUD", "N_REN"])
            kcs = _llave(cs, ["ENT", "CON", "V_SEL", "N_HOG", "H_MUD", "N_REN"])
        else:
            kcb = _llave(cb, ["UPM", "VIV_SEL", "H_MUD", "R_SEL"])
            kcs = _llave(cs, ["UPM", "VIV_SEL", "H_MUD", "N_REN"])
        t = pd.DataFrame({"k": kcs, "s": cs[sx], "e": cs[ed]})
        dup = t["k"].duplicated(keep=False)
        diag["CS-DUPLICADA"] = int(t.loc[dup, "k"].nunique())
        t = t[~dup].set_index("k")
        diag["JOIN-SIN-CS"] = int((~kcb.isin(t.index)).sum())
        sexo = kcb.map(t["s"])
        edad = kcb.map(t["e"])
    w = n(cb["FACTOR" if era1 else "FAC_SEL"])
    est_col = "EDIS" if era1 else "EST_DIS"
    cd = _norm(cb["CD"]).str.zfill(2)
    est = cd + "-" + cb[est_col].astype(str).str.strip()
    upm = cb["UPM_DIS"].astype(str).str.strip()
    ok = (w.gt(0) & cb[est_col].astype(str).str.strip().ne("") & upm.ne("")).to_numpy()
    diag["PERSONAS-DISENO-VALIDO"] = int(ok.sum())
    f = pd.DataFrame({"_w": np.asarray(w, dtype=float), "_est": est, "_upm": est + "|" + upm, "_cd": cd})
    if era1:
        f["_ent"] = _norm(cb["ENT"]).str.zfill(2)
    else:
        f["_ent"] = cb["UPM"].astype(str).str.strip().str.zfill(7).str[:2]
    s = n(pd.Series(sexo)).to_numpy()
    f["_sexo"] = np.where(s == 1, "HOMBRE", np.where(s == 2, "MUJER", None))
    e = n(pd.Series(edad)).to_numpy()
    cat = np.full(len(f), None, dtype=object)
    for c, lo, hi in EDADES:
        cat[(e >= lo) & (e <= hi)] = c
    f["_edad"] = cat
    for c in reac:
        f[c] = n(cb[c]).to_numpy() if c in cb.columns else np.nan
    f = f[ok].reset_index(drop=True)
    cds = sorted(set(f["_cd"]))
    diag["CIUDADES"] = len(cds)
    diag["CIUDADES-SHA256"] = hashlib.sha256(",".join(cds).encode()).hexdigest()
    return f, diag


def y_de(conducta, f, ola):
    nombre, v16, v13, si, univ, _ = next(c for c in CONDUCTAS if c[0] == conducta)
    col = v13 if ola <= ERA1_FIN else v16
    if col is None or col not in f.columns:
        raise ParoDeGuardia(f"{conducta} declarada disponible en {ola} sin columna en el cuestionario")
    v = f[col].to_numpy(dtype=float)
    u = np.isin(v, univ)
    if conducta in FILTRO:
        fc, fv = FILTRO[conducta]
        u &= np.isin(f[fc].to_numpy(dtype=float), fv)
    y = np.where(np.isin(v, si), 1.0, 0.0)
    y[~u] = np.nan
    return y


# ═══════════════════════════ ids ═══════════════════════════

def rid(pref, conducta, ola, eje, cat, q):
    return f"{pref}-{conducta}-{ola}-{eje}-{cat}-{q}"


def celdas(punto, conducta):
    """[(eje, cats)] que emite `punto` para `conducta` (sin TOTAL)."""
    ejes = list(EJES_BASE.items())
    if punto == "pisos":
        return ejes + [("ENT", ENTIDADES), ("CIUDAD", CIUDADES)]
    if conducta == "C01-INSEG-CIUDAD":
        return ejes + [("CIUDAD", CIUDADES)]
    return ejes


def celdas_ola(punto, conducta, ola):
    out = [("TOTAL", ("TODOS",))]
    for eje, cats in celdas(punto, conducta):
        if eje == "CIUDAD" and ola <= ERA1_FIN:
            continue          # 2013-2015: FD sin catálogo de ciudades (spec §2)
        out.append((eje, cats))
    return out


def prefijo(punto):
    return {"pisos": "RESULT-ENSU-PISOS", "serie": "RESULT-ENSU-SERIE"}[punto]


# ═══════════════════════════ dictamen (serie) ═══════════════════════════

def par_estado(conducta, eje, a, b, diag):
    """Estado documental del par (a, b) — spec §5, reglas R1-R4, en ese orden."""
    if b == REDISENO:
        return "CAMBIO-DOCUMENTADO"                                   # R1
    if b == T2020 and conducta in POST_16:
        return "CAMBIO-DOCUMENTADO"                                   # R2
    if eje != "CIUDAD" and diag[a]["CIUDADES-SHA256"] != diag[b]["CIUDADES-SHA256"]:
        return "CAMBIO-DOCUMENTADO"                                   # R3
    return "COMPARABLE"                                               # R4


def dictamenes(out, olas_por_conducta, diag, D):
    pref = prefijo("serie")
    res = {}
    for cad in ("T", "S"):
        filas, valores = [], {}
        for c in CONDUCTAS:
            if c[5] != cad:
                continue
            nom = c[0]
            olas = olas_por_conducta[nom]
            for eje, cats in [("TOTAL", ("TODOS",))] + celdas("serie", nom):
                for cat in cats:
                    sid = f"{nom}|{eje}|{cat}"
                    serie = [o for o in olas if not (eje == "CIUDAD" and o <= ERA1_FIN)]
                    for i, o in enumerate(serie):
                        ids = {q: rid(pref, nom, o, eje, cat, q) for q in ("P", "IC-LO", "IC-HI")}
                        for q, k in ids.items():
                            valores[k] = out.get(k)
                        filas.append({
                            "serie_id": sid, "ola": o, "eje": eje,
                            "par_con_anterior": (par_estado(nom, eje, serie[i - 1], o, diag) if i else ""),
                            "result_p": ids["P"], "result_lo": ids["IC-LO"], "result_hi": ids["IC-HI"],
                            "marca_2020": "SI" if ("2020" in o or (i and "2020" in serie[i - 1])) else "NO",
                        })
        r, tau, _ = D.evalua(filas, valores)
        res[cad] = (r, tau)
    return res


def emite_dictamen(out, res):
    pdct = "RESULT-ENSU-DICTAMEN"
    for cad, (r, tau) in res.items():
        nomcad = {"T": "TRIMESTRAL", "S": "SEMESTRAL"}[cad]
        for eje in ("TOTAL", "SEXO", "EDAD", "CIUDAD"):
            if cad == "S" and eje == "CIUDAD":
                continue
            v = tau.get(eje)
            out[f"{pdct}-TAU2-{nomcad}-{eje}"] = float(v) if v is not None else None
        for sid, d in r.items():
            base = f"{pdct}-{sid.replace('|', '-')}"
            out[f"{base}-K"] = int(d["k"])
            out[f"{base}-N-FUERA"] = int(d["n_fuera"])
            out[f"{base}-DICTAMEN"] = d["dictamen"]
            out[f"{base}-DIRECCION"] = d["direccion"] or "NINGUNA"
            dp = d["delta_pp"]
            out[f"{base}-DELTA-PP"] = float(dp) if dp is not None and math.isfinite(dp) else None
            out[f"{base}-OLA-INI"] = d["olas"][0] if d["olas"] else "NINGUNA"
            out[f"{base}-OLA-FIN"] = d["olas"][-1] if d["olas"] else "NINGUNA"
            out[f"{base}-N-CAMBIO-DOCUMENTADO"] = sum(
                1 for p in d["pares"] if p["estado"] == "CAMBIO-DOCUMENTADO")
    return out


# ═══════════════════════════ orquestación ═══════════════════════════

def _modulo(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


def _fin(x):
    if x is None:
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def _guardia(inputs, contrato):
    params = contrato["parametros"]
    esperados = set(INPUTS_REPO) | {params["payloads"][str(a)] for a in ANIOS}
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for a in ANIOS:
        ruta = str(inputs[params["payloads"][str(a)]].get("ruta_absoluta") or "")
        if not ruta:
            raise ParoDeGuardia(f"payload {a} sin ruta resuelta")
        if "2026" in ruta.rsplit("/", 1)[-1] or "/2026/" in ruta:
            raise ParoDeGuardia(f"payload {a} resuelve al año RESERVADO 2026 (E.6): {ruta}")
    for k in INPUTS_REPO:
        if inputs[k].get("bytes") is None:
            raise ParoDeGuardia(f"`{k}` sin bytes: se exige origen repo")


def mide(tabs, disponibilidad, punto, olas_pedidas, replicas, semilla, R, D=None):
    """tabs: {ola: {"cb": (ruta, bytes), "cs": (ruta, bytes)}}."""
    pref = prefijo(punto)
    out, diag = {}, {}
    olas_por_conducta = {c: [o for o in disponibilidad[c] if o in olas_pedidas] for c in NOMBRES}
    for ola in olas_pedidas:
        t = tabs.get(ola) or {}
        if "cb" not in t or (ola < ERA3_INI and "cs" not in t):
            raise ParoDeGuardia(f"{ola}: tabla CB/CS ausente en el payload")
        cs = t.get("cs") or (None, None)
        f, dg = marco(ola, *t["cb"], *cs, R)
        diag[ola] = dg
        conds = {c: y_de(c, f, ola) for c in NOMBRES if ola in olas_por_conducta[c]}
        for c, y in conds.items():
            ejes = {}
            for eje, cats in celdas_ola(punto, c, ola)[1:]:
                col = {"SEXO": "_sexo", "EDAD": "_edad", "ENT": "_ent", "CIUDAD": "_cd"}[eje]
                ejes[eje] = (f[col].to_numpy(dtype=object), cats)
            r = R.marginales(f, {c: y}, ejes, f["_w"].to_numpy(), "_est", "_upm", replicas, semilla)
            for eje, cats in celdas_ola(punto, c, ola):
                for cat in cats:
                    x = r.get((c, eje, cat)) or {}
                    out[rid(pref, c, ola, eje, cat, "P")] = _fin(x.get("p"))
                    out[rid(pref, c, ola, eje, cat, "IC-LO")] = _fin(x.get("lo"))
                    out[rid(pref, c, ola, eje, cat, "IC-HI")] = _fin(x.get("hi"))
                    out[rid(pref, c, ola, eje, cat, "N")] = int(x.get("n", 0))
        for k in ("PERSONAS", "PERSONAS-DISENO-VALIDO", "JOIN-SIN-CS", "CS-DUPLICADA", "CIUDADES"):
            out[f"{pref}-G-{ola}-{k}"] = int(dg[k])
        out[f"{pref}-G-{ola}-CIUDADES-SHA256"] = dg["CIUDADES-SHA256"]
    if punto == "serie":
        emite_dictamen(out, dictamenes(out, olas_por_conducta, diag, D))
    return out


def medir(inputs, contrato):
    _guardia(inputs, contrato)
    p = contrato["parametros"]
    punto = p["punto_de_entrada"]
    replicas = int(p["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo("receta_pisos", inputs["receta_pisos"]["bytes"])
    D = _modulo("dictamen_series", inputs["dictamen_series"]["bytes"])
    olas = list(p["olas"])
    anios = sorted({int(o[:4]) for o in olas})
    tabs = {}
    for a in anios:
        ruta = inputs[p["payloads"][str(a)]]["ruta_absoluta"]
        with open(ruta, "rb") as fh:
            tabs.update(tablas(fh.read()))
    out = mide(tabs, p["disponibilidad"], punto, olas, replicas, semilla, R, D)
    pref = prefijo(punto)
    out[f"{pref}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{pref}-G-SEED"] = semilla
    out[f"{pref}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos"].get("sha256"))
    out[f"{pref}-G-INPUT-DICTAMEN-SHA256"] = str(inputs["dictamen_series"].get("sha256"))
    out[f"{pref}-G-OLA-RESERVADA"] = "ENSU 2026 -- RESERVADA (E.6), no es input; último trimestre abierto 2025T4"
    return out


# ═══════════════════════════ esquema ═══════════════════════════

def _fila(i, tipo, unidad, nulo=False):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if nulo:
        f["permite_no_estimable"] = True
    return f


def esquema_resultados(punto, olas, disponibilidad):
    pref = prefijo(punto)
    f = []
    for ola in olas:
        for k, u in (("PERSONAS", "filas"), ("PERSONAS-DISENO-VALIDO", "filas"), ("JOIN-SIN-CS", "filas"),
                     ("CS-DUPLICADA", "llaves"), ("CIUDADES", "ciudades")):
            f.append(_fila(f"{pref}-G-{ola}-{k}", "entero", u))
        f.append(_fila(f"{pref}-G-{ola}-CIUDADES-SHA256", "texto", "sha256 de los códigos CD presentes"))
    for c in NOMBRES:
        for ola in olas:
            if ola not in disponibilidad[c]:
                continue
            for eje, cats in celdas_ola(punto, c, ola):
                for cat in cats:
                    f += [_fila(rid(pref, c, ola, eje, cat, "P"), "proporcion", "proporción ponderada de personas 18+", True),
                          _fila(rid(pref, c, ola, eje, cat, "IC-LO"), "proporcion", "IC95 diseño, inferior", True),
                          _fila(rid(pref, c, ola, eje, cat, "IC-HI"), "proporcion", "IC95 diseño, superior", True),
                          _fila(rid(pref, c, ola, eje, cat, "N"), "entero", "personas sin ponderar")]
    if punto == "serie":
        pdct = "RESULT-ENSU-DICTAMEN"
        for cad, ejes in (("TRIMESTRAL", ("TOTAL", "SEXO", "EDAD", "CIUDAD")), ("SEMESTRAL", ("TOTAL", "SEXO", "EDAD"))):
            for eje in ejes:
                f.append(_fila(f"{pdct}-TAU2-{cad}-{eje}", "flotante", "τ² de persistencia (logit²)", True))
        for c in NOMBRES:
            for eje, cats in [("TOTAL", ("TODOS",))] + celdas("serie", c):
                for cat in cats:
                    base = f"{pdct}-{c}-{eje}-{cat}"
                    f += [_fila(f"{base}-K", "entero", "olas en el tramo"),
                          _fila(f"{base}-N-FUERA", "entero", "pares fuera del IC calibrado"),
                          _fila(f"{base}-DICTAMEN", "texto", "vocabulario DONDE-CAMBIO"),
                          _fila(f"{base}-DIRECCION", "texto", "SUBE/BAJA/NINGUNA"),
                          _fila(f"{base}-DELTA-PP", "flotante", "p_fin - p_ini, puntos porcentuales", True),
                          _fila(f"{base}-OLA-INI", "texto", "trimestre"),
                          _fila(f"{base}-OLA-FIN", "texto", "trimestre"),
                          _fila(f"{base}-N-CAMBIO-DOCUMENTADO", "entero", "pares")]
    for k, t, u in (("BOOTSTRAP-REPLICAS", "entero", "réplicas"), ("SEED", "entero", "semilla"),
                    ("INPUT-RECETA-SHA256", "texto", "sha256"), ("INPUT-DICTAMEN-SHA256", "texto", "sha256"),
                    ("OLA-RESERVADA", "texto", "declaración")):
        f.append(_fila(f"{pref}-G-{k}", t, u))
    return f
