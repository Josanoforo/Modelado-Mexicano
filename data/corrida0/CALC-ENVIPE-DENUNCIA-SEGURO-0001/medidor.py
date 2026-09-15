"""`CALC-ENVIPE-DENUNCIA-SEGURO-0001` -- denuncia condicionada a cobertura de
seguro, robo total de vehiculo (BPCOD=01), ENVIPE 2025, unidad DELITO.
Releva `CORR-0007` `RES-0039/0040/0041/0042` (opcion A firmada, OBJETO 10).

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN CAJA POR `ACTO GEN2-MEDICION-DEMANDA-2` (15/sep/2026)
EN UN COMMIT PROPIO, ANTES DE ABRIR UN SOLO VALOR DEL MICRODATO. El contrato
(`spec.yaml`, congelado en NUBE por `ACTO GEN2-FIRMAS-MESA-1`, `PR #785`) no
se edita. Spec humana sellada: `forense/prereg-caja/ENVIPE-DENUNCIA-SEGURO-spec-v1_0.md`
(sha `1ccb0d92…`).

Lo unico abierto al escribir este archivo, ademas del contrato: la LISTA de
miembros del ZIP, la CABECERA (nombres de columna) del archivo de victimas, y
los cuatro catalogos declarados (`catalogos/bpcod.csv`, `bp1_20.csv`,
`bp2_1.csv`, `fac_del.csv`) -- codebook, E.5. Ningun valor de ninguna fila.

Lo que decide el CODIGO y no la spec, declarado para que se pueda refutar:
  · BOOTSTRAP CONJUNTO. Un solo bootstrap sobre los conglomerados
    (EST_DIS, UPM_DIS) de U entero -- UPM con reemplazo dentro de estrato,
    conservando el numero de UPM por estrato, seed 20260915, PCG64, 2000
    replicas -- y en CADA replica se recalculan los dos puntos (CON, SIN) y su
    diferencia. Asi CON-IC, SIN-IC, los EE y DELTA-IC salen de las MISMAS
    replicas (la spec pide IC de la diferencia, que dos bootstraps separados
    no pueden dar). N-EST-DIS-DISTINTOS / N-UPM-DISTINTAS / N-ESTRATOS-UPM-UNICA
    se cuentan sobre U, como la spec los define.
  · Orden de exclusion para los conteos: BPCOD != '01' primero; dentro de
    BPCOD=01, BP2_1 fuera de {1,2} y BP1_20 fuera de {1,2} se cuentan cada uno
    sobre TODAS las filas de BPCOD=01 (no son excluyentes entre si); el
    ponderador se juzga sobre las filas que pasaron los tres codigos.
  · Blanco/NaN en los soportes se escribe 'b', como el propio catalogo bp2_1.
  · CATALOGO-*: CONFIRMA si el catalogo del ZIP trae los codigos del mapa con
    la descripcion esperada ('01' -> empieza con «Robo total de veh»; '1' ->
    «Si», '2' -> «No», leidos en UTF-8, que es como INEGI escribe los
    catalogos); CONTRADICE:<detalle> en otro caso. Un codigo OBSERVADO en U
    que no este en su catalogo -> NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:<col>.
  · REPLAY-INDEPENDIENTE: segunda pasada ordenando U por la llave que resulto
    unica, acumulando con `math.fsum` (otra aritmetica que la suma en orden de
    lectura); REPLICA si los 8 valores caen dentro de 1e-10.
  · G-SHA256-SPEC-YAML y G-SHA256-SCRIPT hashean los BYTES de los archivos
    hermanos; el medidor no parsea `spec.yaml` (doctrina del runner).
"""
from __future__ import annotations

import hashlib
import io
import math
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

P = "RESULT-ENVIPE-SEG-"
ZIP_ID = "envipe2025_csv"
SPEC_ID = "IN-ENVIPE-SEG-SPEC-SELLADA"
M_VIC = "tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv"
CAT = {
    "BPCOD": "tmod_vic_envipe2025/catalogos/bpcod.csv",
    "BP1_20": "tmod_vic_envipe2025/catalogos/bp1_20.csv",
    "BP2_1": "tmod_vic_envipe2025/catalogos/bp2_1.csv",
}
COLS = ["BPCOD", "BP2_1", "BP1_20", "FAC_DEL", "EST_DIS", "UPM_DIS",
        "ID_DEL", "ID_VIV", "ID_HOG", "ID_PER"]
TOL = 1.0e-10
AQUI = Path(__file__).resolve().parent


# ── utilidades ────────────────────────────────────────────────────────────

def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _num(v):
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _norm(c: str) -> str:
    return str(c).lstrip("﻿").lstrip("ï»¿").strip().strip('"').upper()


def _txt(s: pd.Series) -> pd.Series:
    """cadena cruda: strip de espacios y comillas; NaN -> '' (blanco)."""
    return s.fillna("").astype(str).str.strip().str.strip('"')


def _soporte(s: pd.Series) -> str:
    vc = s.replace("", "b").value_counts()
    return ";".join(f"{k}:{int(v)}" for k, v in sorted(vc.items(), key=lambda kv: str(kv[0])))


def _perfil_anchos(s: pd.Series) -> str:
    vc = s.str.len().value_counts()
    return ";".join(f"ancho={int(k)}:{int(v)}" for k, v in sorted(vc.items()))


def _catalogo(zf, miembro: str, col: str) -> dict:
    """{codigo: descripcion} del catalogo del ZIP (UTF-8, terminador CR)."""
    crudo = zf.read(miembro).decode("utf-8", errors="replace").replace("\r\n", "\n").replace("\r", "\n")
    df = pd.read_csv(io.StringIO(crudo), dtype=str)
    df.columns = [_norm(c) for c in df.columns]
    if col not in df.columns:
        return {}
    dcol = [c for c in df.columns if c != col][0]
    return {str(k).strip(): str(v).strip() for k, v in zip(df[col], df[dcol])}


def _si_no(txt: str) -> str:
    t = txt.strip().lower()
    return "si" if t in ("sí", "si") else ("no" if t == "no" else t)


# ── el medidor ────────────────────────────────────────────────────────────

def medir(inputs: dict, contrato: dict) -> dict:
    R = {}

    def put(suf, val):
        R[P + suf] = val

    par = contrato.get("parametros") or {}
    cod = par["codificacion"]
    gen1 = par["valores_gen1_referencia"]
    n_gen1 = par["n_gen1_referencia"]
    replicas = int(par.get("bootstrap_replicas", 2000))
    seed = int(contrato["seed"]["valor"])
    grano = int(par.get("grano_gen1_decimales", 6))
    BPCOD_U = str(cod["bpcod_universo"])
    CON, SIN = str(cod["bp2_1_con_seguro"]), str(cod["bp2_1_sin_seguro"])
    DEN, NODEN = str(cod["bp1_20_denuncia"]), str(cod["bp1_20_no_denuncia"])

    # ── G: identidad ──────────────────────────────────────────────────────
    put("G-SHA256-PAYLOAD", str(inputs[ZIP_ID]["sha256"]))
    put("G-SHA256-SPEC-SELLADA", str(inputs[SPEC_ID]["sha256"]))
    put("G-SHA256-SPEC-YAML", _sha(AQUI / "spec.yaml"))
    put("G-SHA256-SCRIPT", _sha(Path(__file__).resolve()))

    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    nombres = zf.namelist()
    put("G-N-MIEMBROS-ZIP", len(nombres))

    enteros_g = ["G-N-FILAS-VICTIMAS", "G-N-COLUMNAS-VICTIMAS", "G-N-FUERA-DE-BPCOD-01",
                 "G-N-SEGURO-INVALIDO", "G-N-DENUNCIA-INVALIDA", "G-N-SIN-PONDERADOR",
                 "G-N-PESOS-NO-POSITIVOS", "G-N-SIN-DISENO", "G-N-U", "G-N-EST-DIS-DISTINTOS",
                 "G-N-UPM-DISTINTAS", "G-N-ESTRATOS-UPM-UNICA", "CON-N-U", "CON-N-DENUNCIA",
                 "CON-N-NO-DENUNCIA", "SIN-N-U", "SIN-N-DENUNCIA", "SIN-N-NO-DENUNCIA"]
    flot = ["G-SUMA-PESOS-U", "CON-SUMA-PESOS", "CON-P-DENUNCIA", "CON-P-NO-DENUNCIA",
            "CON-EE-DENUNCIA", "CON-IC-LO", "CON-IC-HI", "SIN-SUMA-PESOS", "SIN-P-DENUNCIA",
            "SIN-P-NO-DENUNCIA", "SIN-EE-DENUNCIA", "SIN-IC-LO", "SIN-IC-HI",
            "DELTA-CON-MENOS-SIN", "DELTA-IC-LO", "DELTA-IC-HI"]
    textos = ["G-LLAVE-DELITO", "G-CATALOGO-BPCOD", "G-CATALOGO-BP2-1", "G-CATALOGO-BP1-20",
              "G-SOPORTE-BPCOD", "G-SOPORTE-BP2-1", "G-SOPORTE-BP1-20", "G-PARTICION-ESTRATOS",
              "G-PERFIL-EST-DIS", "G-PERFIL-UPM-DIS", "G-REPLAY-INDEPENDIENTE", "CON-SUMA-UNO",
              "SIN-SUMA-UNO", "METODO-IC", "DELTA-VS-GEN1", "REPRODUCE-GEN1", "DELTA-N-VS-GEN1"]

    def rendirse(razon: str):
        for s in enteros_g:
            R.setdefault(P + s, 0)
        for s in flot:
            R.setdefault(P + s, None)
        for s in textos:
            R.setdefault(P + s, razon if s in ("G-LLAVE-DELITO", "G-REPLAY-INDEPENDIENTE",
                                               "REPRODUCE-GEN1", "G-PARTICION-ESTRATOS",
                                               "CON-SUMA-UNO", "SIN-SUMA-UNO", "DELTA-VS-GEN1",
                                               "DELTA-N-VS-GEN1") else "NO-APLICA")
        R[P + "METODO-IC"] = "NO-ESTIMABLE-DISENO-INCOMPLETO"
        for s in ("G-SUMA-PESOS-U", "CON-SUMA-PESOS", "SIN-SUMA-PESOS"):
            if R.get(P + s) is None:
                R[P + s] = 0.0        # sumas de pesos sin permite_no_estimable: cero contado, no null
        put("ADOPCION", "NO-ADOPTABLE-NO-ESTIMABLE")
        return R

    if M_VIC not in nombres:
        return rendirse(f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{M_VIC}")

    # ── lectura, como la declara la spec ──────────────────────────────────
    crudo = zf.read(M_VIC)
    df = pd.read_csv(io.BytesIO(crudo), encoding="latin-1", low_memory=False, dtype=str)
    df.columns = [_norm(c) for c in df.columns]
    put("G-N-FILAS-VICTIMAS", int(len(df)))
    put("G-N-COLUMNAS-VICTIMAS", int(df.shape[1]))
    faltan = [c for c in COLS if c not in df.columns]
    if faltan:
        return rendirse("NO-ESTIMABLE-COLUMNA-AUSENTE:" + ";".join(faltan))

    for c in ["BPCOD", "BP2_1", "BP1_20", "EST_DIS", "UPM_DIS", "ID_DEL", "ID_VIV", "ID_HOG", "ID_PER"]:
        df[c] = _txt(df[c])

    # ── catalogos (codebook del propio ZIP) ───────────────────────────────
    cats = {}
    for col, m in CAT.items():
        cats[col] = _catalogo(zf, m, col) if m in nombres else None
    cb = cats["BPCOD"]
    if cb is None:
        put("G-CATALOGO-BPCOD", "CONTRADICE:catalogo-ausente")
    elif BPCOD_U in cb and cb[BPCOD_U].lower().startswith("robo total de veh"):
        put("G-CATALOGO-BPCOD", "CONFIRMA")
    else:
        put("G-CATALOGO-BPCOD", f"CONTRADICE:{BPCOD_U}={cb.get(BPCOD_U)!r}")
    for col, key, a, b in (("BP2_1", "G-CATALOGO-BP2-1", CON, SIN),
                           ("BP1_20", "G-CATALOGO-BP1-20", DEN, NODEN)):
        c = cats[col]
        if c is None:
            put(key, "CONTRADICE:catalogo-ausente")
        elif _si_no(c.get(a, "")) == "si" and _si_no(c.get(b, "")) == "no":
            put(key, "CONFIRMA")
        else:
            put(key, f"CONTRADICE:{a}={c.get(a)!r};{b}={c.get(b)!r}")

    # ── soportes y filtros, CONTADOS ──────────────────────────────────────
    put("G-SOPORTE-BPCOD", _soporte(df["BPCOD"]))
    es01 = df["BPCOD"] == BPCOD_U
    put("G-N-FUERA-DE-BPCOD-01", int((~es01).sum()))
    v01 = df[es01]
    put("G-SOPORTE-BP2-1", _soporte(v01["BP2_1"]))
    put("G-SOPORTE-BP1-20", _soporte(v01["BP1_20"]))
    seg_ok = v01["BP2_1"].isin([CON, SIN])
    den_ok = v01["BP1_20"].isin([DEN, NODEN])
    put("G-N-SEGURO-INVALIDO", int((~seg_ok).sum()))
    put("G-N-DENUNCIA-INVALIDA", int((~den_ok).sum()))

    # codigo observado en U que no este en su catalogo -> fuera de mapa
    for col, key in (("BP2_1", "G-CATALOGO-BP2-1"), ("BP1_20", "G-CATALOGO-BP1-20")):
        c = cats[col]
        if c is not None:
            obs = set(v01[col].unique()) - {""}      # el blanco no es un codigo: se cuenta como invalido, no como fuera de mapa
            if obs - set(c.keys()):
                return rendirse(f"NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:{col}")
    if cb is not None and BPCOD_U not in cb:
        return rendirse("NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA:BPCOD")

    u = v01[seg_ok & den_ok].copy()
    w = pd.to_numeric(u["FAC_DEL"].fillna("").astype(str).str.strip().str.replace(",", ""),
                      errors="coerce")
    sin_pond = w.isna() | ~np.isfinite(w.fillna(0.0))
    no_pos = (~sin_pond) & (w <= 0)
    put("G-N-SIN-PONDERADOR", int(sin_pond.sum()))
    put("G-N-PESOS-NO-POSITIVOS", int(no_pos.sum()))
    u = u[~(sin_pond | no_pos)].copy()
    u["_w"] = w[~(sin_pond | no_pos)].astype(float)
    put("G-N-U", int(len(u)))
    if len(u) == 0:
        return rendirse("NO-ESTIMABLE-UNIVERSO-VACIO:U")

    # ── llave de delito ───────────────────────────────────────────────────
    if u["ID_DEL"].is_unique:
        llave = ["ID_DEL"]; put("G-LLAVE-DELITO", "ID_DEL")
    elif not u.duplicated(subset=["ID_DEL", "ID_VIV", "ID_HOG", "ID_PER"]).any():
        llave = ["ID_DEL", "ID_VIV", "ID_HOG", "ID_PER"]
        put("G-LLAVE-DELITO", "ID_DEL+ID_VIV+ID_HOG+ID_PER")
    else:
        put("G-LLAVE-DELITO", "NO-UNICA")
        return rendirse("NO-ESTIMABLE-LLAVE-NO-UNICA")

    # ── diseno ────────────────────────────────────────────────────────────
    sin_dis = (u["EST_DIS"] == "") | (u["UPM_DIS"] == "")
    put("G-N-SIN-DISENO", int(sin_dis.sum()))
    put("G-PERFIL-EST-DIS", _perfil_anchos(u["EST_DIS"]))
    put("G-PERFIL-UPM-DIS", _perfil_anchos(u["UPM_DIS"]))
    ud = u[~sin_dis]
    put("G-N-EST-DIS-DISTINTOS", int(ud["EST_DIS"].nunique()))
    pares = ud.groupby(["EST_DIS", "UPM_DIS"], sort=True).size()
    put("G-N-UPM-DISTINTAS", int(len(pares)))
    upm_por_est = pares.groupby(level=0).size()
    n_unica = int((upm_por_est == 1).sum())
    put("G-N-ESTRATOS-UPM-UNICA", n_unica)

    # ── puntos, sumas en orden fijo de fila ───────────────────────────────
    put("G-SUMA-PESOS-U", _num(float(u["_w"].sum())))
    con = u[u["BP2_1"] == CON]
    sin = u[u["BP2_1"] == SIN]
    put("CON-N-U", int(len(con))); put("SIN-N-U", int(len(sin)))
    res_part = len(con) + len(sin) - len(u)
    put("G-PARTICION-ESTRATOS", "SI" if res_part == 0 else f"NO:{res_part}")

    def puntos(sub, pref):
        n_d = int((sub["BP1_20"] == DEN).sum()); n_nd = int((sub["BP1_20"] == NODEN).sum())
        put(f"{pref}-N-DENUNCIA", n_d); put(f"{pref}-N-NO-DENUNCIA", n_nd)
        sw = 0.0; swd = 0.0; swn = 0.0
        for wi, di in zip(sub["_w"].tolist(), sub["BP1_20"].tolist()):
            sw += wi
            if di == DEN:
                swd += wi
            elif di == NODEN:
                swn += wi
        put(f"{pref}-SUMA-PESOS", _num(sw))
        if len(sub) == 0 or sw <= 0:
            put(f"{pref}-P-DENUNCIA", None); put(f"{pref}-P-NO-DENUNCIA", None)
            put(f"{pref}-SUMA-UNO", f"NO-ESTIMABLE-UNIVERSO-VACIO:U_{pref}")
            return None, None, sw
        p, q = swd / sw, swn / sw            # complemento CONTADO, nunca 1 - p
        put(f"{pref}-P-DENUNCIA", _num(p)); put(f"{pref}-P-NO-DENUNCIA", _num(q))
        r = abs(p + q - 1.0)
        put(f"{pref}-SUMA-UNO", "SI" if r <= TOL else f"NO:{r:.3e}")
        return p, q, sw

    p_con, q_con, sw_con = puntos(con, "CON")
    p_sin, q_sin, sw_sin = puntos(sin, "SIN")

    # ── bootstrap conjunto sobre los conglomerados de U ───────────────────
    if len(ud) == 0:
        for s in ["CON-EE-DENUNCIA", "CON-IC-LO", "CON-IC-HI", "SIN-EE-DENUNCIA", "SIN-IC-LO",
                  "SIN-IC-HI", "DELTA-IC-LO", "DELTA-IC-HI"]:
            put(s, None)
        put("METODO-IC", "NO-ESTIMABLE-DISENO-INCOMPLETO")
    else:
        g = ud.assign(_con=(ud["BP2_1"] == CON).astype(float),
                      _sin=(ud["BP2_1"] == SIN).astype(float),
                      _den=(ud["BP1_20"] == DEN).astype(float))
        g["sw_con"] = g["_w"] * g["_con"]; g["swd_con"] = g["_w"] * g["_con"] * g["_den"]
        g["sw_sin"] = g["_w"] * g["_sin"]; g["swd_sin"] = g["_w"] * g["_sin"] * g["_den"]
        agg = g.groupby(["EST_DIS", "UPM_DIS"], sort=True)[["sw_con", "swd_con", "sw_sin", "swd_sin"]].sum()
        bloques = [agg.loc[[e]].to_numpy(dtype=float) for e in sorted(agg.index.get_level_values(0).unique())]
        rng = np.random.Generator(np.random.PCG64(seed))
        rep = np.empty((replicas, 4), dtype=float)
        for r in range(replicas):
            tot = np.zeros(4)
            for b in bloques:
                k = b.shape[0]
                tot += b[rng.integers(0, k, size=k)].sum(axis=0)
            rep[r] = tot
        with np.errstate(divide="ignore", invalid="ignore"):
            pc = rep[:, 1] / rep[:, 0]
            ps = rep[:, 3] / rep[:, 2]
        dl = pc - ps

        def ic(x, pref):
            f = x[np.isfinite(x)]
            if f.size == 0:
                put(f"{pref}-IC-LO", None); put(f"{pref}-IC-HI", None)
                return None
            put(f"{pref}-IC-LO", _num(float(np.percentile(f, 2.5))))
            put(f"{pref}-IC-HI", _num(float(np.percentile(f, 97.5))))
            return float(np.std(f, ddof=1)) if f.size > 1 else None

        put("CON-EE-DENUNCIA", _num(ic(pc, "CON")))
        put("SIN-EE-DENUNCIA", _num(ic(ps, "SIN")))
        ic(dl, "DELTA")
        put("METODO-IC", "IC-CON-ESTRATOS-DE-UPM-UNICA" if n_unica > 0 else "IC-DE-DISENO")

    put("DELTA-CON-MENOS-SIN", _num(None if p_con is None or p_sin is None else p_con - p_sin))

    # ── replay independiente: orden de llave, acumulacion fsum ────────────
    uo = u.sort_values(llave, kind="stable")
    rep_vals = []
    for cual in (CON, SIN):
        sub = uo[uo["BP2_1"] == cual]
        sw = math.fsum(sub["_w"]); swd = math.fsum(sub.loc[sub["BP1_20"] == DEN, "_w"])
        swn = math.fsum(sub.loc[sub["BP1_20"] == NODEN, "_w"])
        rep_vals += [sw, (swd / sw) if sw > 0 else None, (swn / sw) if sw > 0 else None]
    ref = [sw_con, p_con, q_con, sw_sin, p_sin, q_sin]
    peor = 0.0
    for a, b in zip(ref, rep_vals):
        if a is None or b is None:
            continue
        peor = max(peor, abs(a - b) / (abs(a) if abs(a) > 1 else 1.0))
    put("G-REPLAY-INDEPENDIENTE", "REPLICA" if peor <= TOL else f"NO-REPLICA:{peor:.3e}")

    # ── contraste GEN1 (referencia, nunca filtro) ─────────────────────────
    leg = {"RES-0039": float(gen1["RES_0039_CON_P_DENUNCIA"]), "RES-0040": float(gen1["RES_0040_CON_P_NO_DENUNCIA"]),
           "RES-0041": float(gen1["RES_0041_SIN_P_DENUNCIA"]), "RES-0042": float(gen1["RES_0042_SIN_P_NO_DENUNCIA"])}
    hoy = {"RES-0039": p_con, "RES-0040": q_con, "RES-0041": p_sin, "RES-0042": q_sin}
    if any(v is None for v in hoy.values()):
        put("DELTA-VS-GEN1", None); put("REPRODUCE-GEN1", "NO-ESTIMABLE")
        put("ADOPCION", "NO-ADOPTABLE-NO-ESTIMABLE")
    else:
        put("DELTA-VS-GEN1", ";".join(f"{k}:{hoy[k] - leg[k]:+.9f}" for k in leg))
        rep_ok = all(round(hoy[k], grano) == round(leg[k], grano) for k in leg)
        put("REPRODUCE-GEN1", "REPRODUCE" if rep_ok else "NO-REPRODUCE")
        put("ADOPCION", "LISTADO-PARA-MESA-REPRODUCE" if rep_ok else "LISTADO-PARA-MESA-NO-REPRODUCE")
    put("DELTA-N-VS-GEN1",
        f"U:{len(u) - int(n_gen1['U_TOTAL']):+d};CON:{len(con) - int(n_gen1['U_CON']):+d};"
        f"SIN:{len(sin) - int(n_gen1['U_SIN']):+d}")
    return R
