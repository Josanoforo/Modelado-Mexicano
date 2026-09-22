#!/usr/bin/env python3
"""Validación independiente del lote de 44 celdas primarias (GEN2-VALIDACION-INDEPENDIENTE-LOTE-1).

Escrito DESDE la spec humana (`forense/prereg-caja/DIN-lote-enif2024-spec-v1_0.md`), el
cuestionario/descriptor (`data/ahorro-comparabilidad-texto-v1_0.tsv`) y los catálogos crudos
de los zips ENIF 2021/2024, SIN abrir `medidor.py`/`adjudicacion.py`/`spec.yaml`/`resultados.json`
de ningún CALC del lote (`CALC-DIN-LOTE-ENIF2024-EMISIONES-0001`, `…-ADJUDICACION-0001`) ni
`tools/lote_enif2024/` ni `tools/duelo/cruces_familia.py` ni sus tests.

Único input leído de un CALC sellado: los marginales de ENIF 2024 POR EJE de
`CALC-ARBITRO-MARGINALES-ENIF2024-0001` (`#971`), citados por `id` de RESULT — la propia
spec del lote (§4) exige exactamente esto («no se re-miden»; el medidor original hace lo
mismo). Se usan sólo como PUNTO del `C2` sellado; las réplicas de `C2` (para el IC de Δ) se
re-derivan aquí de microdato propio, régimen PILOTO-1, exactamente como #970 (piloto 1) hizo.

Régimen de universo PILOTO-1 (spec §1), idéntico en las dos olas, sin ningún filtro más:
  (1) 18 ≤ edad ≤ 97 (EDAD en 2021, EDAD_V en 2024; 97 cuenta como edad, 98/99 centinelas)
  (2) TLOC ∈ {1,2,3,4}
  (3) ponderador presente y > 0 (FAC_ELE en 2021, FAC_PER en 2024)

D9 := informal AND NOT formal_9
  informal := alguna de P5_1_1..P5_1_6 == "1" (mismo nemónico las dos olas)
  formal_9 := alguna de P5_7_1..P5_7_9 == "1" (2021) | P5_6_1..P5_6_9 == "1" (2024)
Código "1" = Sí; todo lo demás (incl. blanco) cuenta como No. Filas con código fuera de
{"1","2",""} se cuentan (`filas_codigo_fuera_de_dominio`) y NO se descartan.

Escolaridad — mapa por ETIQUETA (spec §2), no por código (04/05 permutados 2021↔2024;
09 se parte en 09/10/11 en 2024):
  hasta-primaria: Ninguno · Preescolar o kínder · Primaria
  secundaria:     Secundaria
  media-superior: Estudios técnicos con secundaria terminada · Normal básica ·
                  Preparatoria o bachillerato · Estudios técnicos con preparatoria terminada
  superior:       Licenciatura o ingeniería (profesional) · Especialidad · Maestría ·
                  Doctorado · Maestría o doctorado (2021)
  fuera:          No sabe (99)
Catálogos leídos crudos de cada zip (`catalogos/p3_1_1.csv` 2021, `catalogos/niv.csv` 2024);
un código presente sin etiqueta declarada para la corrida para (PARO), no se asigna por
cercanía.

Contendientes (spec §4, sólo lo que P1 pide — la comparación que adjudica es una sola,
C2 contra R2; P2/R1/R3 quedan fuera de este acto, SECUNDARIOS y no adjudican aquí):
  R   := p̂24(a,b) empírico, régimen PILOTO-1                         (candidato: NINGUNO, es el árbitro)
  C2  := expit(logit m̂24(a) + logit m̂24(b) − logit m̂24)             (piso; punto = marginales SELLADOS #971)
  δ21(a,b) := logit p̂21(a,b) − [logit m̂21(a) + logit m̂21(b) − logit m̂21]   (marginales 2021 PROPIAS)
  R2  := expit(logit C2 + ½·δ21(a,b))                                  (retador primario, λ=½ fija)
  Δ   := MAE(C2) − MAE(R2) sobre las 44 celdas puntuadas, contra R

Método de varianza (propio, declarado, LATITUD §6 del encargo): bootstrap de conglomerados
estratificado sobre el marco de diseño ENTERO del archivo de cada ola (todas las UPM
presentes, n_h UPM con reemplazo dentro de cada EST_DIS), 10 000 réplicas por ola,
`numpy.random.default_rng` con semilla propia POR OLA (2021 y 2024 son muestras
independientes: sin covarianzas inventadas, cada una con su propio flujo aleatorio); las
máscaras de universo/celda/marginal se aplican DENTRO de cada réplica. Δ_k se recalcula
réplica a réplica con R_k, C2_k (de las réplicas 2024) y R2_k (que usa δ21_k de las
réplicas 2021) de la MISMA k. IC95 = percentiles 2.5/97.5 (interpolación lineal). Estrato
con UPM única: multiplicidad fija = 1 (varianza cero, contado). Mismo método que #970
(`valida_pilotos.py`), para continuidad de convención entre actos de validación.

Salida: resultados_propios_lote.json en este directorio (sufijo `_lote` — T02: el nombre
genérico `resultados_propios.json` colisiona con el de `#970`,
`forense/validaciones/GEN2-VALIDACION-INDEPENDIENTE-PILOTOS-v1_0/`).
"""
from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
RAW = AQUI.parents[2] / "data" / "raw"
B = 10_000
SEED_2021 = 20260922
SEED_2024 = 20260923
BLOQUE = 250

EJES_PRIMARIOS = ["sexo", "edad", "escolaridad", "localidad"]
PARES_PRIMARIOS = [
    ("edad", "sexo"), ("escolaridad", "sexo"), ("localidad", "sexo"),
    ("edad", "escolaridad"), ("escolaridad", "localidad"),
]

NIVELES = {
    "sexo": ["H", "M"],
    "edad": ["E1", "E2", "E3", "E4"],
    "escolaridad": ["HP", "SEC", "MS", "SUP"],
    "localidad": ["L1", "L2"],
}

TRAMO_ESCOLARIDAD_POR_ETIQUETA = {
    "Ninguno": "HP", "Preescolar o kínder": "HP", "Primaria": "HP",
    "Secundaria": "SEC",
    "Estudios técnicos con secundaria terminada": "MS", "Normal básica": "MS",
    "Preparatoria o bachillerato": "MS", "Estudios técnicos con preparatoria terminada": "MS",
    "Licenciatura o ingeniería (profesional)": "SUP", "Especialidad": "SUP",
    "Maestría": "SUP", "Doctorado": "SUP", "Maestría o doctorado": "SUP",
    "No sabe": None,
}

# marginales SELLADOS de ENIF 2024 (CALC-ARBITRO-MARGINALES-ENIF2024-0001, #971), citados
# por id de RESULT — régimen ARBITRO-2024 (13 502; no filtra TLOC ni saca centinelas del
# universo, marca "fuera" por eje). Usados SÓLO como punto de C2 (spec §4: "no se re-miden").
MARGINALES_SELLADOS_2024 = {
    "sexo": {"H": 0.3324892676595783, "M": 0.3785232659603534},
    "edad": {"E1": 0.4320629027722269, "E2": 0.3757090767556958, "E3": 0.3275054698041219, "E4": 0.2773166971496971},
    "escolaridad": {"HP": 0.35159354260032355, "SEC": 0.41563468007153764, "MS": 0.38933841835746036, "SUP": 0.26043792577731173},
    "localidad": {"L1": 0.4092545386928037, "L2": 0.3298680661438076},
    "NAC": 0.35715220063339936,
}
FUENTE_MARGINALES_SELLADOS = {
    "calc": "CALC-ARBITRO-MARGINALES-ENIF2024-0001",
    "ids": [
        "RESULT-ARBITRO-ENIF2024-D9-SEXO-1-P", "RESULT-ARBITRO-ENIF2024-D9-SEXO-2-P",
        "RESULT-ARBITRO-ENIF2024-D9-EDAD-18-29-P", "RESULT-ARBITRO-ENIF2024-D9-EDAD-30-44-P",
        "RESULT-ARBITRO-ENIF2024-D9-EDAD-45-59-P", "RESULT-ARBITRO-ENIF2024-D9-EDAD-60-MAS-P",
        "RESULT-ARBITRO-ENIF2024-D9-ESCOLARIDAD-HASTA-PRIMARIA-P", "RESULT-ARBITRO-ENIF2024-D9-ESCOLARIDAD-SECUNDARIA-P",
        "RESULT-ARBITRO-ENIF2024-D9-ESCOLARIDAD-MEDIA-SUPERIOR-P", "RESULT-ARBITRO-ENIF2024-D9-ESCOLARIDAD-SUPERIOR-P",
        "RESULT-ARBITRO-ENIF2024-D9-LOCALIDAD-15-000-Y-MAS-P", "RESULT-ARBITRO-ENIF2024-D9-LOCALIDAD-MENOR-DE-15-000-P",
        "RESULT-ARBITRO-ENIF2024-D9-TOTAL-TODOS-P",
    ],
    "leido": "2026-09-22, resultados.json de data/corrida0/CALC-ARBITRO-MARGINALES-ENIF2024-0001 (input declarado por la spec §4, no re-medido)",
}


def logit(p):
    p = np.asarray(p, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.log(p / (1.0 - p))


def expit(z):
    return 1.0 / (1.0 + np.exp(-np.asarray(z, dtype=float)))


def piso_log_aditivo(pa, pb, pall):
    for x in (pa, pb, pall):
        if x is None or not np.isfinite(x) or x <= 0.0 or x >= 1.0:
            return None
    return float(expit(logit(pa) + logit(pb) - logit(pall)))


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


class Marco:
    """Marco de diseño de una ola: conjunto de UPM del ARCHIVO (est|upm) + filas a medir."""

    def __init__(self, est_marco: pd.Series, upm_marco: pd.Series, seed: int):
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
        self.seed = seed

    def filas(self, est: pd.Series, upm: pd.Series, w: np.ndarray):
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
        rng = np.random.default_rng(self.seed)
        nombres = list(self.masks)
        S = np.stack([self.masks[k][0] for k in nombres])
        T = np.stack([self.masks[k][1] for k in nombres])
        out = np.full((len(nombres), B), np.nan)
        hs = sorted(self.estratos)
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
            num = Mf @ S.T
            den = Mf @ T.T
            with np.errstate(divide="ignore", invalid="ignore"):
                out[:, b0:b0 + nb] = np.where(den > 0, num / den, np.nan).T
        return {k: out[i] for i, k in enumerate(nombres)}


def ic(v):
    v = v[np.isfinite(v)]
    if len(v) == 0:
        return None, None, 0
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)), int(len(v))


def leer_csv_zip(zip_path: Path, miembro: str, usecols=None):
    zf = zipfile.ZipFile(zip_path)
    raw = zf.open(miembro).read()
    sha = sha256_bytes(raw)
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


def leer_catalogo_zip(zip_path: Path, miembro: str) -> dict:
    zf = zipfile.ZipFile(zip_path)
    raw = zf.open(miembro).read()
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        txt = raw.decode("latin-1")
    df = pd.read_csv(io.StringIO(txt), dtype=str)
    df.columns = [c.strip().strip('"') for c in df.columns]
    cve = df[df.columns[0]].str.strip().str.strip('"')
    descrip = df[df.columns[1]].str.strip().str.strip('"')
    return dict(zip(cve, descrip))


def mapa_tramo(catalogo: dict) -> dict:
    """cve (normalizada por valor entero, «00»≡«0») -> tramo (HP/SEC/MS/SUP/None);
    PARA si una etiqueta del catálogo no está declarada."""
    out = {}
    for cve, etiqueta in catalogo.items():
        if etiqueta not in TRAMO_ESCOLARIDAD_POR_ETIQUETA:
            raise SystemExit(f"PARO: etiqueta de escolaridad sin tramo declarado: {etiqueta!r} (código {cve})")
        out[str(int(cve))] = TRAMO_ESCOLARIDAD_POR_ETIQUETA[etiqueta]
    return out


def normaliza_codigo(serie: pd.Series) -> pd.Series:
    """«00»->"0", «09»->"9": mismo valor entero que la clave del catálogo. Blanco queda blanco."""
    def f(x):
        if x == "":
            return ""
        try:
            return str(int(x))
        except ValueError:
            return x
    return serie.map(f)


def edad_a_tramo(edad: np.ndarray) -> np.ndarray:
    out = np.full(len(edad), "", dtype=object)
    out[(edad >= 18) & (edad <= 29)] = "E1"
    out[(edad >= 30) & (edad <= 44)] = "E2"
    out[(edad >= 45) & (edad <= 59)] = "E3"
    out[(edad >= 60) & (edad <= 97)] = "E4"
    return out


def tloc_a_localidad(tloc: pd.Series) -> np.ndarray:
    return np.where(tloc.isin(["3", "4"]), "L1", np.where(tloc.isin(["1", "2"]), "L2", ""))


def sexo_a_eje(sexo: pd.Series) -> np.ndarray:
    return np.where(sexo == "1", "H", np.where(sexo == "2", "M", ""))


# ----------------------------------------------------------------- ENIF 2021
def carga_2021():
    zp = RAW / "enif2021_csv.zip"
    m_datos = "conjunto_de_datos_tmodulo_enif_2021/conjunto_de_datos/conjunto_de_datos_tmodulo_enif_2021.csv"
    m_cat = "conjunto_de_datos_tmodulo_enif_2021/catalogos/p3_1_1.csv"
    cat = leer_catalogo_zip(zp, m_cat)
    tramo = mapa_tramo(cat)
    cols = ["EDAD", "TLOC", "FAC_ELE", "EST_DIS", "UPM_DIS", "SEXO", "P3_1_1"] + \
        [f"P5_1_{k}" for k in range(1, 7)] + [f"P5_7_{k}" for k in range(1, 10)]
    df, sha, enc = leer_csv_zip(zp, m_datos, usecols=cols)
    n_archivo = len(df)
    edad = pd.to_numeric(df.EDAD, errors="coerce").to_numpy()
    w = pd.to_numeric(df.FAC_ELE, errors="coerce").fillna(0).to_numpy()
    univ = (np.nan_to_num(edad, nan=-1) >= 18) & (np.nan_to_num(edad, nan=-1) <= 97) & df.TLOC.isin(["1", "2", "3", "4"]).to_numpy() & (w > 0)

    informal = np.zeros(n_archivo, dtype=bool)
    for k in range(1, 7):
        informal |= (df[f"P5_1_{k}"] == "1").to_numpy()
    formal9 = np.zeros(n_archivo, dtype=bool)
    for k in range(1, 10):
        formal9 |= (df[f"P5_7_{k}"] == "1").to_numpy()
    d9 = (informal & ~formal9).astype(float)

    dominio_cols = [f"P5_1_{k}" for k in range(1, 7)] + [f"P5_7_{k}" for k in range(1, 10)]
    fuera_dom = np.zeros(n_archivo, dtype=bool)
    for c in dominio_cols:
        fuera_dom |= ~df[c].isin(["1", "2", ""]).to_numpy()

    esc_cod = normaliza_codigo(df.P3_1_1)
    codigos_sin_etiqueta = sorted(set(esc_cod.unique()) - set(tramo.keys()) - {""})
    esc = esc_cod.map(tramo).fillna("").to_numpy()
    loc = tloc_a_localidad(df.TLOC)
    sx = sexo_a_eje(df.SEXO)
    ed = edad_a_tramo(edad)

    return {
        "df_len": n_archivo, "sha256_miembro": sha, "encoding": enc,
        "n_universo": int(univ.sum()), "filas_edad_98_99_o_no_num": int(np.isnan(edad).sum() + ((edad == 98) | (edad == 99)).sum()),
        "filas_codigo_fuera_de_dominio": int(fuera_dom.sum()),
        "codigos_escolaridad_sin_etiqueta": codigos_sin_etiqueta,
        "catalogo_escolaridad_leido": cat,
        "univ": univ, "d9": d9, "sexo": sx, "edad": ed, "escolaridad": esc, "localidad": loc,
        "est_dis": df.EST_DIS, "upm_dis": df.UPM_DIS, "w": w,
    }


# ----------------------------------------------------------------- ENIF 2024
def carga_2024():
    zp = RAW / "enif2024_csv.zip"
    m_datos = "conjunto_de_datos_tmodulo_enif_2024/conjunto_de_datos/conjunto_de_datos_tmodulo_enif2024.csv"
    m_cat = "conjunto_de_datos_tmodulo_enif_2024/catalogos/niv.csv"
    cat = leer_catalogo_zip(zp, m_cat)
    tramo = mapa_tramo(cat)
    cols = ["edad_v", "tloc", "fac_per", "est_dis", "upm_dis", "sexo", "niv"] + \
        [f"p5_1_{k}" for k in range(1, 7)] + [f"p5_6_{k}" for k in range(1, 10)]
    df, sha, enc = leer_csv_zip(zp, m_datos, usecols=cols)
    n_archivo = len(df)
    edad = pd.to_numeric(df.edad_v, errors="coerce").to_numpy()
    w = pd.to_numeric(df.fac_per, errors="coerce").fillna(0).to_numpy()
    univ = (np.nan_to_num(edad, nan=-1) >= 18) & (np.nan_to_num(edad, nan=-1) <= 97) & df.tloc.isin(["1", "2", "3", "4"]).to_numpy() & (w > 0)

    informal = np.zeros(n_archivo, dtype=bool)
    for k in range(1, 7):
        informal |= (df[f"p5_1_{k}"] == "1").to_numpy()
    formal9 = np.zeros(n_archivo, dtype=bool)
    for k in range(1, 10):
        formal9 |= (df[f"p5_6_{k}"] == "1").to_numpy()
    d9 = (informal & ~formal9).astype(float)

    dominio_cols = [f"p5_1_{k}" for k in range(1, 7)] + [f"p5_6_{k}" for k in range(1, 10)]
    fuera_dom = np.zeros(n_archivo, dtype=bool)
    for c in dominio_cols:
        fuera_dom |= ~df[c].isin(["1", "2", ""]).to_numpy()

    esc_cod = normaliza_codigo(df.niv)
    codigos_sin_etiqueta = sorted(set(esc_cod.unique()) - set(tramo.keys()) - {""})
    esc = esc_cod.map(tramo).fillna("").to_numpy()
    loc = tloc_a_localidad(df.tloc)
    sx = sexo_a_eje(df.sexo)
    ed = edad_a_tramo(edad)

    return {
        "df_len": n_archivo, "sha256_miembro": sha, "encoding": enc,
        "n_universo": int(univ.sum()), "filas_edad_98_99_o_no_num": int(np.isnan(edad).sum() + ((edad == 98) | (edad == 99)).sum()),
        "filas_codigo_fuera_de_dominio": int(fuera_dom.sum()),
        "codigos_escolaridad_sin_etiqueta": codigos_sin_etiqueta,
        "catalogo_escolaridad_leido": cat,
        "univ": univ, "d9": d9, "sexo": sx, "edad": ed, "escolaridad": esc, "localidad": loc,
        "est_dis": df.est_dis, "upm_dis": df.upm_dis, "w": w,
    }


def construye_marco(datos, seed):
    marco = Marco(datos["est_dis"], datos["upm_dis"], seed).filas(datos["est_dis"], datos["upm_dis"], datos["w"])
    univ = datos["univ"]
    d9 = datos["d9"]
    ejes = {"sexo": datos["sexo"], "edad": datos["edad"], "escolaridad": datos["escolaridad"], "localidad": datos["localidad"]}
    for eje, niveles in NIVELES.items():
        for niv in niveles:
            marco.agrega(f"M:{eje}:{niv}", univ & (ejes[eje] == niv), d9)
    marco.agrega("M:NAC", univ, d9)
    for a, b in PARES_PRIMARIOS:
        for na in NIVELES[a]:
            for nb in NIVELES[b]:
                marco.agrega(f"R:{a}x{b}:{na}x{nb}", univ & (ejes[a] == na) & (ejes[b] == nb), d9)
    return marco


def main():
    datos21 = carga_2021()
    datos24 = carga_2024()
    if datos21["codigos_escolaridad_sin_etiqueta"] or datos24["codigos_escolaridad_sin_etiqueta"]:
        raise SystemExit(f"PARO: códigos de escolaridad sin etiqueta -> 2021={datos21['codigos_escolaridad_sin_etiqueta']} 2024={datos24['codigos_escolaridad_sin_etiqueta']}")

    marco21 = construye_marco(datos21, SEED_2021)
    marco24 = construye_marco(datos24, SEED_2024)
    reps21 = marco21.replicas()
    reps24 = marco24.replicas()

    def punto(marco, nombre):
        return marco.masks[nombre][3]

    def n_de(marco, nombre):
        return marco.masks[nombre][2]

    marg21 = {eje: {niv: punto(marco21, f"M:{eje}:{niv}") for niv in NIVELES[eje]} for eje in NIVELES}
    marg21_NAC = punto(marco21, "M:NAC")
    marg21_reps = {eje: {niv: reps21[f"M:{eje}:{niv}"] for niv in NIVELES[eje]} for eje in NIVELES}
    marg21_NAC_reps = reps21["M:NAC"]

    marg24_reps = {eje: {niv: reps24[f"M:{eje}:{niv}"] for niv in NIVELES[eje]} for eje in NIVELES}
    marg24_NAC_reps = reps24["M:NAC"]
    marg24_propio = {eje: {niv: punto(marco24, f"M:{eje}:{niv}") for niv in NIVELES[eje]} for eje in NIVELES}
    marg24_propio_NAC = punto(marco24, "M:NAC")

    celdas = {}
    R_puntos, C2_puntos, R2_puntos = [], [], []
    delta_k_acumula = []  # lista de (mae_c2_k_vec, mae_r2_k_vec) por celda, se combina después

    C2k_mat = []  # (44, B)
    R2k_mat = []
    Rk_mat = []
    nombres_celda = []

    for a, b in PARES_PRIMARIOS:
        for na in NIVELES[a]:
            for nb in NIVELES[b]:
                nombre_r = f"R:{a}x{b}:{na}x{nb}"
                n24, R_punto = n_de(marco24, nombre_r), punto(marco24, nombre_r)
                n21, P21_punto = n_de(marco21, nombre_r), punto(marco21, nombre_r)

                C2_punto = piso_log_aditivo(MARGINALES_SELLADOS_2024[a][na], MARGINALES_SELLADOS_2024[b][nb], MARGINALES_SELLADOS_2024["NAC"])
                d21_punto = None
                if P21_punto is not None and marg21[a][na] is not None and marg21[b][nb] is not None and marg21_NAC is not None:
                    d21_punto = float(logit(P21_punto) - (logit(marg21[a][na]) + logit(marg21[b][nb]) - logit(marg21_NAC)))
                R2_punto = None
                if C2_punto is not None and d21_punto is not None:
                    R2_punto = float(expit(logit(C2_punto) + 0.5 * d21_punto))

                # réplicas
                C2_k = expit(logit(marg24_reps[a][na]) + logit(marg24_reps[b][nb]) - logit(marg24_NAC_reps))
                P21_k = reps21[nombre_r]
                d21_k = logit(P21_k) - (logit(marg21_reps[a][na]) + logit(marg21_reps[b][nb]) - logit(marg21_NAC_reps))
                R2_k = expit(logit(C2_k) + 0.5 * d21_k)
                R_k = reps24[nombre_r]

                lo_r, hi_r, nr_r = ic(reps24[nombre_r])
                lo_c2, hi_c2, nr_c2 = ic(C2_k)
                lo_r2, hi_r2, nr_r2 = ic(R2_k)

                soporte = bool(n24 >= 200 and n21 >= 200)
                nombre_celda = f"{a}x{b}:{na}x{nb}"
                celdas[nombre_celda] = {
                    "n_2024": n24, "n_2021": n21, "soporte_n200_ambas_olas": soporte,
                    "R": {"p": R_punto, "ic95": [lo_r, hi_r]},
                    "C2": {"p": C2_punto, "ic95": [lo_c2, hi_c2]},
                    "P2_2021": {"p": P21_punto},
                    "delta21_punto": d21_punto,
                    "R2": {"p": R2_punto, "ic95": [lo_r2, hi_r2]},
                    "dentro_ic_C2": (lo_c2 is not None and R_punto is not None and lo_c2 <= R_punto <= hi_c2),
                    "dentro_ic_R2": (lo_r2 is not None and R_punto is not None and lo_r2 <= R_punto <= hi_r2),
                }
                if soporte and R_punto is not None and C2_punto is not None and R2_punto is not None:
                    R_puntos.append(R_punto); C2_puntos.append(C2_punto); R2_puntos.append(R2_punto)
                    nombres_celda.append(nombre_celda)
                    C2k_mat.append(C2_k); R2k_mat.append(R2_k); Rk_mat.append(R_k)

    R_puntos = np.array(R_puntos); C2_puntos = np.array(C2_puntos); R2_puntos = np.array(R2_puntos)
    MAE_C2 = float(np.mean(np.abs(C2_puntos - R_puntos)))
    MAE_R2 = float(np.mean(np.abs(R2_puntos - R_puntos)))
    delta_punto = MAE_C2 - MAE_R2

    C2k_mat = np.array(C2k_mat); R2k_mat = np.array(R2k_mat); Rk_mat = np.array(Rk_mat)  # (n_celdas_puntuadas, B)
    mae_c2_k = np.nanmean(np.abs(C2k_mat - Rk_mat), axis=0)
    mae_r2_k = np.nanmean(np.abs(R2k_mat - Rk_mat), axis=0)
    delta_k = mae_c2_k - mae_r2_k
    lo_d, hi_d, nr_d = ic(delta_k)

    if lo_d is not None and lo_d > 0.5:
        veredicto = "VENCE-RETADOR"
    elif lo_d is not None and 0 < lo_d <= 0.5:
        veredicto = "PROPUESTA-CON-RESERVA"
    elif lo_d is not None:
        veredicto = "NADIE-VENCE"
    else:
        veredicto = "NO-CALCULABLE"

    cobertura_C2 = float(np.mean([celdas[c]["dentro_ic_C2"] for c in nombres_celda]))
    cobertura_R2 = float(np.mean([celdas[c]["dentro_ic_R2"] for c in nombres_celda]))

    out = {
        "metodo_varianza": __doc__.split("Método de varianza")[1].split("Salida:")[0].strip(),
        "B": B, "seed_2021": SEED_2021, "seed_2024": SEED_2024,
        "fuente_marginales_sellados_2024": FUENTE_MARGINALES_SELLADOS,
        "diagnostico": {
            "2021": {k: v for k, v in datos21.items() if k not in ("univ", "d9", "sexo", "edad", "escolaridad", "localidad", "est_dis", "upm_dis", "w", "catalogo_escolaridad_leido")},
            "2024": {k: v for k, v in datos24.items() if k not in ("univ", "d9", "sexo", "edad", "escolaridad", "localidad", "est_dis", "upm_dis", "w", "catalogo_escolaridad_leido")},
        },
        "catalogo_escolaridad_2021": datos21["catalogo_escolaridad_leido"],
        "catalogo_escolaridad_2024": datos24["catalogo_escolaridad_leido"],
        "marginales_2021_propios": {eje: marg21[eje] for eje in NIVELES}, "marginales_2021_propios_NAC": marg21_NAC,
        "marginales_2024_propios_control": {eje: marg24_propio[eje] for eje in NIVELES}, "marginales_2024_propios_NAC_control": marg24_propio_NAC,
        "marginales_2024_sellados_citados": MARGINALES_SELLADOS_2024,
        "n_celdas_totales": len(celdas), "n_celdas_puntuadas": len(nombres_celda),
        "celdas": celdas,
        "primario": {
            "MAE_C2_pp": MAE_C2 * 100, "MAE_R2_pp": MAE_R2 * 100,
            "delta_MAE_pp_punto": delta_punto * 100,
            "delta_MAE_pp_ic95": [lo_d * 100 if lo_d is not None else None, hi_d * 100 if hi_d is not None else None],
            "n_replicas_delta_finitas": nr_d,
            "veredicto": veredicto,
            "cobertura_C2_frac": cobertura_C2, "cobertura_R2_frac": cobertura_R2,
            "celdas_puntuadas": nombres_celda,
        },
    }
    dest = AQUI / "resultados_propios_lote.json"
    dest.write_text(json.dumps(out, indent=1, ensure_ascii=False, default=lambda o: None) + "\n")
    print("MAE_C2_pp", MAE_C2 * 100)
    print("MAE_R2_pp", MAE_R2 * 100)
    print("delta_MAE_pp_punto", delta_punto * 100)
    print("delta_MAE_pp_ic95", (lo_d * 100 if lo_d is not None else None), (hi_d * 100 if hi_d is not None else None))
    print("veredicto", veredicto)
    print("cobertura_C2_frac", cobertura_C2, "cobertura_R2_frac", cobertura_R2)
    print("n_universo_2021", datos21["n_universo"], "n_universo_2024", datos24["n_universo"])
    print("escrito", dest)


if __name__ == "__main__":
    main()
