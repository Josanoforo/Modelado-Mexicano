#!/usr/bin/env python3
"""Validación independiente de los tres pilotos celda-D (GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-1).

Escrito DESDE LAS SPECS HUMANAS, el cuestionario/descriptor y los catálogos, sin abrir
`medidor.py`/`adjudicacion.py` de ningún CALC ni sus tests. Produce, por piloto:

  * R por celda (punto + IC95) sobre la ola reservada, receta de la spec.
  * C2 por celda (punto) — dos lecturas: (a) con los marginales SELLADOS que la spec cita
    (piloto 1 y 2: es el punto oficial de C2) y (b) con marginales re-derivados aquí.
  * Marginales de un eje re-derivados (control de la cadena payload → filtro → ponderador).

Método de varianza (propio, declarado): bootstrap de conglomerados estratificado sobre el
marco de diseño ENTERO del archivo (todas las UPM presentes en el archivo, n_h UPM con
reemplazo dentro de cada EST_DIS), 10 000 réplicas, `numpy.random.default_rng(20260921)`;
las máscaras de universo/celda se aplican DENTRO de cada réplica; IC95 = percentiles
2.5/97.5 (interpolación lineal). Las celdas y marginales de una ola comparten réplicas.
Estrato con UPM única: multiplicidad fija = 1 (varianza cero, contado).

Salida: resultados_propios.json en este directorio.
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
RAW = AQUI.parents[2] / "data" / "raw"
B = 10_000
SEED = 20260921
BLOQUE = 250


def logit(p):
    p = np.asarray(p, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.log(p / (1.0 - p))


def expit(z):
    return 1.0 / (1.0 + np.exp(-np.asarray(z, dtype=float)))


def piso_log_aditivo(pa, pb, pall):
    """C2: ausencia de interacción en escala logit (nunca «independencia»)."""
    for x in (pa, pb, pall):
        if x is None or not np.isfinite(x) or x <= 0.0 or x >= 1.0:
            return None
    return float(expit(logit(pa) + logit(pb) - logit(pall)))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class Marco:
    """Marco de diseño de una ola: conjunto de UPM del ARCHIVO (est|upm) + filas a medir."""

    def __init__(self, est_marco: pd.Series, upm_marco: pd.Series):
        llave = est_marco.astype(str).str.strip() + "|" + upm_marco.astype(str).str.strip()
        self.upm_codes, inv = np.unique(llave.to_numpy(), return_inverse=True)
        self.est_por_upm = pd.Series(est_marco.astype(str).str.strip().to_numpy()).groupby(inv).first().to_numpy()
        self.U = len(self.upm_codes)
        self.estratos = {h: np.where(self.est_por_upm == h)[0] for h in np.unique(self.est_por_upm)}
        self.n_estratos = len(self.estratos)
        self.estratos_upm_unica = int(sum(1 for v in self.estratos.values() if len(v) == 1))
        self.masks = {}
        self.upm_idx = None
        self.w = None

    def filas(self, est: pd.Series, upm: pd.Series, w: np.ndarray):
        """Filas a medir (subconjunto del marco): mapea cada fila a su UPM del marco."""
        llave = (est.astype(str).str.strip() + "|" + upm.astype(str).str.strip()).to_numpy()
        pos = {k: i for i, k in enumerate(self.upm_codes)}
        self.upm_idx = np.array([pos[k] for k in llave])
        self.w = np.asarray(w, dtype=float)
        return self

    def agrega(self, nombre: str, mask: np.ndarray, y: np.ndarray):
        m = np.asarray(mask, dtype=bool)
        wy = np.where(m, self.w * y, 0.0)
        ww = np.where(m, self.w, 0.0)
        S = np.bincount(self.upm_idx, weights=wy, minlength=self.U)
        T = np.bincount(self.upm_idx, weights=ww, minlength=self.U)
        n = int(m.sum())
        p = float(S.sum() / T.sum()) if T.sum() > 0 else None
        self.masks[nombre] = (S, T, n, p)
        return n, p

    def replicas(self):
        """Devuelve dict nombre -> vector (B,) de p^(r); None donde el denominador es 0."""
        rng = np.random.default_rng(SEED)
        nombres = list(self.masks)
        S = np.stack([self.masks[k][0] for k in nombres])  # (K,U)
        T = np.stack([self.masks[k][1] for k in nombres])
        out = np.full((len(nombres), B), np.nan)
        hs = sorted(self.estratos)  # orden lexicográfico de EST_DIS
        for b0 in range(0, B, BLOQUE):
            nb = min(BLOQUE, B - b0)
            M = np.zeros((nb, self.U), dtype=np.int32)
            for h in hs:
                idx = self.estratos[h]
                nh = len(idx)
                if nh == 1:
                    M[:, idx[0]] = 1
                    continue
                draws = rng.integers(0, nh, size=(nb, nh))
                cnt = np.apply_along_axis(lambda r: np.bincount(r, minlength=nh), 1, draws)
                M[:, idx] = cnt
            Mf = M.astype(float)
            num = Mf @ S.T  # (nb,K)
            den = Mf @ T.T
            with np.errstate(divide="ignore", invalid="ignore"):
                out[:, b0:b0 + nb] = np.where(den > 0, num / den, np.nan).T
        return {k: out[i] for i, k in enumerate(nombres)}


def ic(v):
    v = v[np.isfinite(v)]
    if len(v) == 0:
        return None, None, 0
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)), int(len(v))


def leer_csv_zip(zip_path: Path, miembro: str, usecols=None, sep_lineas=None):
    zf = zipfile.ZipFile(zip_path)
    raw = zf.open(miembro).read()
    sha = sha256_bytes(raw)
    if sep_lineas:
        raw = raw.replace(sep_lineas, b"\n")
    try:
        txt = raw.decode("utf-8")
        enc = "utf-8"
    except UnicodeDecodeError:
        txt = raw.decode("latin-1")
        enc = "latin-1"
    df = pd.read_csv(io.StringIO(txt), dtype=str, usecols=usecols, keep_default_na=False)
    df.columns = [c.strip().strip('"') for c in df.columns]
    for c in df.columns:
        df[c] = df[c].str.strip()
    return df, sha, enc


def celda_dict(nombre, marco, reps):
    S, T, n, p = marco.masks[nombre]
    lo, hi, nrep = ic(reps[nombre])
    return {"n": n, "p": p, "ic95": [lo, hi], "replicas_definidas": nrep}


# ---------------------------------------------------------------- piloto 1 · ENIF 2024
def piloto1():
    zp = RAW / "enif2024_csv.zip"
    m = "conjunto_de_datos_tmodulo_enif_2024/conjunto_de_datos/conjunto_de_datos_tmodulo_enif2024.csv"
    cols = ["edad_v", "tloc", "fac_per", "est_dis", "upm_dis"] + [f"p5_1_{k}" for k in range(1, 7)] + [f"p5_6_{k}" for k in range(1, 10)]
    df, sha, enc = leer_csv_zip(zp, m, usecols=cols)
    n_archivo = len(df)
    edad = pd.to_numeric(df.edad_v, errors="coerce")
    w = pd.to_numeric(df.fac_per, errors="coerce").fillna(0).to_numpy()
    univ = (edad.between(18, 97)) & df.tloc.isin(["1", "2", "3", "4"]) & (w > 0)
    univ = univ.to_numpy()
    informal = np.zeros(n_archivo, dtype=bool)
    for k in range(1, 7):
        informal |= (df[f"p5_1_{k}"] == "1").to_numpy()
    formal9 = np.zeros(n_archivo, dtype=bool)
    formal7 = np.zeros(n_archivo, dtype=bool)
    for k in range(1, 10):
        f = (df[f"p5_6_{k}"] == "1").to_numpy()
        formal9 |= f
        if k in (1, 2, 3, 4, 5, 8, 9):
            formal7 |= f
    d9 = (informal & ~formal9).astype(float)
    d7 = (informal & ~formal7).astype(float)
    fuera_dom = np.zeros(n_archivo, dtype=bool)
    for c in [f"p5_1_{k}" for k in range(1, 7)] + [f"p5_6_{k}" for k in range(1, 10)]:
        fuera_dom |= ~df[c].isin(["1", "2", ""]).to_numpy()
    loc = np.where(df.tloc.isin(["3", "4"]), "L1", np.where(df.tloc.isin(["1", "2"]), "L2", ""))
    e = edad.to_numpy()
    ed = np.full(n_archivo, "", dtype=object)
    ed[(e >= 18) & (e <= 29)] = "E1"
    ed[(e >= 30) & (e <= 44)] = "E2"
    ed[(e >= 45) & (e <= 59)] = "E3"
    ed[(e >= 60) & (e <= 97)] = "E4"

    marco = Marco(df.est_dis, df.upm_dis).filas(df.est_dis, df.upm_dis, w)  # marco ENTERO del archivo
    for L in ("L1", "L2"):
        for E in ("E1", "E2", "E3", "E4"):
            mk = univ & (loc == L) & (ed == E)
            marco.agrega(f"R9:{L}x{E}", mk, d9)
            marco.agrega(f"R7:{L}x{E}", mk, d7)
    for L in ("L1", "L2"):
        marco.agrega(f"M9:{L}", univ & (loc == L), d9)
    for E in ("E1", "E2", "E3", "E4"):
        marco.agrega(f"M9:{E}", univ & (ed == E), d9)
    marco.agrega("M9:NAC", univ, d9)
    reps = marco.replicas()

    # marginales sellados del árbitro, citados de la spec v1.2 §4.2 (no recalculados)
    sellados = {"E1": 0.432063, "E2": 0.375709, "E3": 0.327505, "E4": 0.277317,
                "L1": 0.409255, "L2": 0.329868, "NAC": 0.357153}
    out = {"fuente": {"zip": zp.name, "miembro": m, "sha256_miembro": sha, "encoding": enc},
           "n_archivo": n_archivo, "n_universo": int(univ.sum()),
           "cobertura_sin_ponderar": float(univ.sum() / n_archivo),
           "filas_edad_98_99": int(edad.isin([98, 99]).sum()),
           "filas_codigo_fuera_de_dominio": int(fuera_dom.sum()),
           "diseno": {"upm": marco.U, "estratos": marco.n_estratos, "estratos_upm_unica": marco.estratos_upm_unica},
           "marginales_propios": {}, "marginales_sellados_citados": sellados, "celdas": {}}
    for k in ("L1", "L2", "E1", "E2", "E3", "E4", "NAC"):
        out["marginales_propios"][k] = celda_dict(f"M9:{k}", marco, reps)
    for L in ("L1", "L2"):
        for E in ("E1", "E2", "E3", "E4"):
            c = f"{L}x{E}"
            r9 = celda_dict(f"R9:{c}", marco, reps)
            r7 = celda_dict(f"R7:{c}", marco, reps)
            c2_sellado = piso_log_aditivo(sellados[L], sellados[E], sellados["NAC"])
            mp = out["marginales_propios"]
            c2_propio = piso_log_aditivo(mp[L]["p"], mp[E]["p"], mp["NAC"]["p"])
            # IC de C2 réplica por réplica con marginales propios
            v = expit(logit(reps[f"M9:{L}"]) + logit(reps[f"M9:{E}"]) - logit(reps["M9:NAC"]))
            lo, hi, nr = ic(v)
            out["celdas"][c] = {"R9": r9, "R7_sensibilidad": r7,
                                "C2_punto_marginales_sellados": c2_sellado,
                                "C2_punto_marginales_propios": c2_propio,
                                "C2_ic95_marginales_propios": [lo, hi],
                                "falsador_D7_ge_D9": bool(r7["p"] >= r9["p"] - 1e-12)}
    return out


# ---------------------------------------------------------------- piloto 2 · ENVIPE 2025
ESC = {"00": "S1", "01": "S1", "02": "S1", "03": "S2", "04": "S3", "05": "S3", "06": "S3", "07": "S3", "08": "S4", "09": "S4"}
DOM = {"R": "D1", "C": "D2", "U": "D3"}


def piloto2():
    zp = RAW / "envipe2025_csv.zip"
    mv = "tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv"
    ms = "tsdem_envipe2025/conjunto_de_datos/conjunto_de_datos_tsdem_envipe2025.csv"
    vic, sha_v, enc_v = leer_csv_zip(zp, mv, usecols=["ID_PER", "ID_DEL", "BP1_20", "BP1_23", "FAC_DEL", "DOMINIO", "EST_DIS", "UPM_DIS"], sep_lineas=b"\r")
    sd, sha_s, enc_s = leer_csv_zip(zp, ms, usecols=["ID_PER", "NIV"], sep_lineas=b"\r")
    assert sd.ID_PER.is_unique, "ID_PER no única en tsdem → PARA (spec §3.1)"
    n_archivo = len(vic)
    filas_bp120_fuera = int((~vic.BP1_20.isin(["1", "2"])).sum())
    u = vic[vic.BP1_20.isin(["1", "2"])].copy()
    w = pd.to_numeric(u.FAC_DEL, errors="coerce")
    assert (w > 0).all() and w.notna().all(), "FAC_DEL no numérico o ≤ 0 → PARA"
    assert (u.EST_DIS != "").all() and (u.UPM_DIS != "").all(), "EST_DIS/UPM_DIS vacío → PARA"
    u = u.merge(sd, on="ID_PER", how="left", indicator=True)
    sin_persona = int((u._merge == "left_only").sum())
    esc = u.NIV.map(ESC).fillna("").to_numpy()
    dom = u.DOMINIO.map(DOM).fillna("").to_numpy()
    y = ((u.BP1_20 == "2") & u.BP1_23.isin(["04", "05", "06", "08"])).to_numpy().astype(float)
    w = w.to_numpy(dtype=float)
    # el universo (BP1_20 ∈ {1,2}) YA es el marco: la spec §3.1 lo define así; las filas
    # con BP1_20 fuera no son delitos del universo del árbitro. Marco = UPM del universo.
    marco = Marco(u.EST_DIS, u.UPM_DIS).filas(u.EST_DIS, u.UPM_DIS, w)
    todo = np.ones(len(u), dtype=bool)
    for S in ("S1", "S2", "S3", "S4"):
        marco.agrega(f"M:{S}", esc == S, y)
        for D in ("D1", "D2", "D3"):
            marco.agrega(f"R:{S}x{D}", (esc == S) & (dom == D), y)
    for D in ("D1", "D2", "D3"):
        marco.agrega(f"M:{D}", dom == D, y)
    marco.agrega("M:NAC", todo, y)
    reps = marco.replicas()
    sellados = {"S1": 0.493221, "S2": 0.567369, "S3": 0.543368, "S4": 0.590093,
                "D1": 0.403310, "D2": 0.522090, "D3": 0.592703, "NAC": 0.562774}
    out = {"fuente": {"zip": zp.name, "tmod_vic": {"miembro": mv, "sha256": sha_v, "encoding": enc_v},
                      "tsdem": {"miembro": ms, "sha256": sha_s, "encoding": enc_s}},
           "n_archivo_tmod_vic": n_archivo, "filas_bp1_20_fuera": filas_bp120_fuera,
           "n_universo": int(len(u)), "delitos_sin_persona": sin_persona,
           "n_escolaridad_clasificable": int((esc != "").sum()),
           "cobertura_escolaridad": float((esc != "").sum() / len(u)),
           "dominio_fuera": int((dom == "").sum()),
           "diseno": {"upm": marco.U, "estratos": marco.n_estratos, "estratos_upm_unica": marco.estratos_upm_unica},
           "marginales_propios": {}, "marginales_sellados_citados": sellados, "celdas": {}}
    for k in ("S1", "S2", "S3", "S4", "D1", "D2", "D3", "NAC"):
        out["marginales_propios"][k] = celda_dict(f"M:{k}", marco, reps)
    mp = out["marginales_propios"]
    for S in ("S1", "S2", "S3", "S4"):
        for D in ("D1", "D2", "D3"):
            c = f"{S}x{D}"
            r = celda_dict(f"R:{c}", marco, reps)
            v = expit(logit(reps[f"M:{S}"]) + logit(reps[f"M:{D}"]) - logit(reps["M:NAC"]))
            lo, hi, nr = ic(v)
            out["celdas"][c] = {"R": r,
                                "C2_punto_marginales_sellados": piso_log_aditivo(sellados[S], sellados[D], sellados["NAC"]),
                                "C2_punto_marginales_propios": piso_log_aditivo(mp[S]["p"], mp[D]["p"], mp["NAC"]["p"]),
                                "C2_ic95_marginales_propios": [lo, hi]}
    return out


# ---------------------------------------------------------------- piloto 3 · ENCIG 2025
def piloto3():
    zp = RAW / "encig25_base_datos_csv.zip"
    mt = "encig2025_04_sec_7.csv"
    mr = "encig2025_02_residentes_sec_2.csv"
    tr, sha_t, enc_t = leer_csv_zip(zp, mt, usecols=["ID_PER", "N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS"])
    re_, sha_r, enc_r = leer_csv_zip(zp, mr, usecols=["ID_PER", "EDAD", "NIV"])
    assert re_.ID_PER.is_unique, "ID_PER no única en residentes → la unión m:1 no está validada"
    n_archivo = len(tr)
    luz = tr[tr.N_TRA == "01"].copy()
    n_luz = len(luz)
    canal_valido = luz.P7_3.isin(["1", "2", "4", "5", "6"])
    fuera_canal = int((~canal_valido).sum())
    u = luz[canal_valido].merge(re_, on="ID_PER", how="left", indicator=True)
    sin_persona = int((u._merge == "left_only").sum())
    edad = pd.to_numeric(u.EDAD, errors="coerce")
    niv = pd.to_numeric(u.NIV, errors="coerce")
    w = pd.to_numeric(u.FAC_TRA, errors="coerce").fillna(0).to_numpy(dtype=float)
    y = u.P7_3.isin(["4", "5"]).to_numpy().astype(float)
    e = edad.to_numpy()
    ed = np.full(len(u), "", dtype=object)
    ed[(e >= 18) & (e <= 29)] = "18-29"
    ed[(e >= 30) & (e <= 44)] = "30-44"
    ed[(e >= 45) & (e <= 59)] = "45-59"
    ed[(e >= 60) & (e <= 96)] = "60-96"
    es = np.full(len(u), "", dtype=object)
    nv = niv.to_numpy()
    es[np.isin(nv, [0, 1, 2])] = "HASTA-PRIMARIA"
    es[nv == 3] = "SECUNDARIA"
    es[np.isin(nv, [4, 5, 6, 7])] = "MEDIA-SUPERIOR"
    es[np.isin(nv, [8, 9])] = "SUPERIOR"
    univ = (ed != "") & (es != "") & (w > 0)  # universo F1-bis: residuo de edad/NIV fuera
    residuo_edad = {str(k): int((e == k).sum()) for k in (97, 98, 99)}
    masa_residuo = {str(k): float(w[e == k].sum()) for k in (97, 98, 99)}
    n_60mas_incl97 = int(((e >= 60) & (e <= 97)).sum())
    # marco de diseño ENTERO de la tabla de trámites (todas las UPM del archivo); filas = u
    marco = Marco(tr.EST_DIS, tr.UPM_DIS).filas(u.EST_DIS, u.UPM_DIS, w)
    EDS = ["18-29", "30-44", "45-59", "60-96"]
    ESS = ["HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"]
    for a in EDS:
        marco.agrega(f"MA:{a}", univ & (ed == a), y)
        marco.agrega(f"MA1:{a}", (ed == a) & (w > 0), y)  # alternativa: marginal de edad sin exigir NIV
        for b in ESS:
            marco.agrega(f"R:{a}|{b}", univ & (ed == a) & (es == b), y)
    for b in ESS:
        marco.agrega(f"MB:{b}", univ & (es == b), y)
        marco.agrega(f"MB1:{b}", (es == b) & (w > 0), y)
    marco.agrega("MT", univ, y)
    marco.agrega("MT1", (w > 0), y)
    reps = marco.replicas()
    out = {"fuente": {"zip": zp.name, "sec_7": {"miembro": mt, "sha256": sha_t, "encoding": enc_t},
                      "residentes_sec_2": {"miembro": mr, "sha256": sha_r, "encoding": enc_r}},
           "n_archivo_tramites": n_archivo, "n_tramites_luz": n_luz, "tramites_luz_canal_fuera": fuera_canal,
           "n_canal_valido": int(len(u)), "tramites_sin_persona": sin_persona,
           "n_universo_cruce": int(univ.sum()),
           "residuo_edad_97_98_99_n": residuo_edad, "residuo_edad_97_98_99_masa": masa_residuo,
           "fraccion_97_en_60mas": float(residuo_edad["97"] / n_60mas_incl97) if n_60mas_incl97 else None,
           "niv_fuera": int((es == "").sum()),
           "diseno": {"upm": marco.U, "estratos": marco.n_estratos, "estratos_upm_unica": marco.estratos_upm_unica},
           "marginales_propios_universo_cruce": {}, "marginales_propios_por_eje": {}, "celdas": {}}
    for a in EDS:
        out["marginales_propios_universo_cruce"][a] = celda_dict(f"MA:{a}", marco, reps)
        out["marginales_propios_por_eje"][a] = celda_dict(f"MA1:{a}", marco, reps)
    for b in ESS:
        out["marginales_propios_universo_cruce"][b] = celda_dict(f"MB:{b}", marco, reps)
        out["marginales_propios_por_eje"][b] = celda_dict(f"MB1:{b}", marco, reps)
    out["marginales_propios_universo_cruce"]["TOTAL"] = celda_dict("MT", marco, reps)
    out["marginales_propios_por_eje"]["TOTAL"] = celda_dict("MT1", marco, reps)
    m1 = out["marginales_propios_universo_cruce"]
    m2 = out["marginales_propios_por_eje"]
    for a in EDS:
        for b in ESS:
            c = f"{a}|{b}"
            r = celda_dict(f"R:{c}", marco, reps)
            v = expit(logit(reps[f"MA:{a}"]) + logit(reps[f"MB:{b}"]) - logit(reps["MT"]))
            lo, hi, nr = ic(v)
            out["celdas"][c] = {"R": r,
                                "C2_punto_marginales_universo_cruce": piso_log_aditivo(m1[a]["p"], m1[b]["p"], m1["TOTAL"]["p"]),
                                "C2_ic95_marginales_universo_cruce": [lo, hi],
                                "C2_punto_marginales_por_eje": piso_log_aditivo(m2[a]["p"], m2[b]["p"], m2["TOTAL"]["p"]),
                                "soporte_2025": "PUNTUADA" if r["n"] >= 200 else "FUERA-DE-SOPORTE"}
    return out


def main():
    cuales = sys.argv[1:] or ["1", "2", "3"]
    res = {"metodo_varianza": __doc__.split("Método de varianza")[1].split("Salida:")[0].strip(),
           "B": B, "seed": SEED}
    if "1" in cuales:
        res["piloto1_DIN_ENIF2024"] = piloto1()
        print("piloto1 listo", flush=True)
    if "2" in cuales:
        res["piloto2_TRA_ENVIPE2025"] = piloto2()
        print("piloto2 listo", flush=True)
    if "3" in cuales:
        res["piloto3_GOB_ENCIG2025"] = piloto3()
        print("piloto3 listo", flush=True)
    dest = AQUI / "resultados_propios.json"
    if dest.exists() and len(cuales) < 3:
        prev = json.loads(dest.read_text())
        prev.update(res)
        res = prev
    dest.write_text(json.dumps(res, indent=1, ensure_ascii=False) + "\n")
    print("escrito", dest)


if __name__ == "__main__":
    main()
