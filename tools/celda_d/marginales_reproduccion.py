#!/usr/bin/env python3
"""Control de reproducción del árbitro marginal, congelado como CÓDIGO.

ACTO `GEN2-CELDA-D-PILOTO-2` v1.1 (relanzamiento, 17/sep/2026). Firma 2 de
mesa, verbatim: «El control de reproducción se congela como código en
COMMIT-1 con guardia de una sola variable de agrupación; toda lectura de
ENVIPE 2025 antes de COMMIT-2 fuera de ese script es PARO.»

Este archivo es **el único código autorizado a tocar ENVIPE 2025 antes del
COMMIT-3**. Existe porque la regla de prosa no alcanzó dos veces: la sesión
anterior derivó el cruce reservado con un script exploratorio en scratchpad
«por descuido de diseño del loop», y mesa la cerró.

QUÉ HACE
--------
  · `carga_ola(zip, anio, reservada=...)` — lee `tmod_vic` y `tsdem` de una
    ola de ENVIPE, aplica el universo de `prereg-caja-ENVIPE-EVASION-NORMA`
    (`BP1_20 ∈ {1,2}`, unidad DELITO, `FAC_DEL`) y deriva los dos ejes con
    la MISMA construcción que el árbitro selló (`tools/ejes_maestra35_l1.py`
    :: `ESC_2DIG`, importado — no copiado). Devuelve una `Ola` inmutable con
    HUELLA (sha256 del vector `ID_DEL` en orden de archivo).
  · `marginal(ola, grupo: str)` — estima las celdas de UN eje. La guardia no
    es un comentario:
      - `grupo` es UN `str` posicional; no hay `*grupos`, no hay lista. Pasar
        dos lanza `TypeError`; pasar una lista lanza `TypeError`.
      - `grupo` tiene que ser uno de `EJES`; la celda se deriva DENTRO de la
        función desde las columnas crudas. Un eje inventado («a x b», una
        columna pre-construida) lanza `ValueError`.
      - la `Ola` se re-huella antes de contar: una ola filtrada o alterada
        tras cargarla (la otra forma de cruzar — «marginal de escolaridad
        sobre las filas rurales») lanza `ReservaRota`.
  · `cruce(ola, eje_a, eje_b)` — las 12 celdas. Lanza `ReservaRota` si la
    ola está marcada `reservada=True`. El CALC de emisiones carga 2025 con
    `reservada=True` (parámetro del contrato); el CALC del árbitro (COMMIT-3)
    la carga con `reservada=False`, y el sello del COMMIT-2 es anterior.
  · `replicas_compartidas(ola, seed, n_rep)` — UN remuestreo estratificado de
    UPM por ola, compartido por todos los grupos y celdas de esa ola, para
    que `C2`, `C6` y `C7` se combinen réplica a réplica sin covarianzas
    inventadas (mismo diseño que `FP-379 D3` del primer piloto).
  · `cotejo(m, sellados, tol_p, tol_ic)` — re-derivado contra sellado, con
    Δ con signo; nunca ajusta.

El punto y el IC95 de cada celda salen de `wprop_ic_conglomerado`
(`tools/calibracion_mordida_encig_serie.py`), la MISMA función con la que el
árbitro selló `milpa/tramite-ola5-propuesta-v0.yaml:1672-1731` — importada,
no reimplementada. Las réplicas compartidas son ADEMÁS de eso, para los
candidatos; no sustituyen al IC del árbitro.

Sin argumentos de CLI este archivo no abre nada. Ver `__main__`.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import io
import json
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
TOOLS = RAIZ / "tools"


def _importa(nombre: str, ruta: Path):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


# La construcción del eje es la del árbitro: mismo objeto, no una copia.
_EJES_L1 = _importa("ejes_maestra35_l1", TOOLS / "ejes_maestra35_l1.py")
ESC_2DIG = _EJES_L1.ESC_2DIG
ORD_ESC = list(_EJES_L1.ORD_ESC)
FUERA = _EJES_L1.FUERA
_CAL = _importa("calibracion_mordida_encig_serie",
                TOOLS / "calibracion_mordida_encig_serie.py")
wprop_ic_conglomerado = _CAL.wprop_ic_conglomerado

ORD_DOMINIO = ["Rural", "Complemento urbano", "Urbano"]
DOMINIO_MAP = {"U": "Urbano", "C": "Complemento urbano", "R": "Rural"}
INUTIL = frozenset({"04", "05", "06", "08"})   # BP1_23: pérdida de tiempo ·
                                               # trámites largos · desconfianza ·
                                               # actitud hostil (spec §2.2)

# Rótulos cortos de celda, congelados en la spec humana §1.
ESC_ROTULO = {"S1": "hasta primaria", "S2": "secundaria",
              "S3": "media superior", "S4": "superior"}
DOM_ROTULO = {"D1": "Rural", "D2": "Complemento urbano", "D3": "Urbano"}
CELDAS = [f"{s}x{d}" for s in ("S1", "S2", "S3", "S4") for d in ("D1", "D2", "D3")]

EJES = ("escolaridad_proxy", "dominio_urbano_rural", "nacional")

COLUMNAS_TMOD = ("ID_DEL", "ID_PER", "BP1_20", "BP1_23", "FAC_DEL",
                 "EST_DIS", "UPM_DIS", "DOMINIO")
COLUMNAS_TSDEM = ("ID_PER", "NIV")


class ReservaRota(RuntimeError):
    """Se intentó cruzar, filtrar o alterar una ola fuera de lo autorizado."""


class Paro(RuntimeError):
    """Premisa de la spec falsa en el archivo: se PARA, no se reporta cifra."""


# ══ lectura ════════════════════════════════════════════════════════════════

def _lee_miembro(zip_path, sufijo_miembro, usecols):
    """UN miembro del zip. Los .zip de INEGI mezclan UTF-8 y latin-1 entre
    olas y entre catálogos y microdato: se intenta utf-8 y se cae a latin-1
    DECLARANDO la caída. Los CSV de 2020-2024 terminan línea con `\\r` solo:
    se normaliza antes de pandas."""
    with zipfile.ZipFile(zip_path) as zf:
        candidatos = [n for n in zf.namelist() if n.endswith(sufijo_miembro)]
        if len(candidatos) != 1:
            raise Paro(f"{sufijo_miembro}: {len(candidatos)} miembros en el zip")
        nombre = candidatos[0]
        crudo = zf.read(nombre)
    for enc in ("utf-8", "latin-1"):
        try:
            texto = crudo.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:                                            # pragma: no cover
        raise Paro(f"{sufijo_miembro}: ni utf-8 ni latin-1")
    texto = texto.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")
    df = pd.read_csv(io.StringIO(texto), dtype=str, keep_default_na=False,
                     na_filter=False, low_memory=False)
    df.columns = [c.strip().strip('"').lstrip("﻿") for c in df.columns]
    faltan = [c for c in usecols if c not in df.columns]
    if faltan:
        raise Paro(f"{sufijo_miembro}: columnas ausentes {faltan} "
                   f"(hay {len(df.columns)})")
    for c in usecols:
        df[c] = df[c].astype(str).str.strip().str.strip('"')
    return df[list(usecols)].copy(), nombre, enc


def _dos_digitos(s: str) -> str:
    s = str(s).strip().strip('"')
    if s in ("", "b", "B", "nan"):
        return ""
    return s.zfill(2)


def _huella(df: pd.DataFrame) -> str:
    h = hashlib.sha256()
    h.update(str(len(df)).encode())
    h.update(b"\x1f")
    h.update("\n".join(df["ID_DEL"].tolist()).encode("utf-8"))
    return h.hexdigest()


@dataclass(frozen=True)
class Ola:
    anio: int
    df: pd.DataFrame = field(repr=False, compare=False)
    huella: str
    reservada: bool
    meta: dict = field(compare=False)


def carga_ola(zip_path, anio: int, *, reservada: bool = False) -> Ola:
    """Universo de `prereg-caja-ENVIPE-EVASION-NORMA` sobre una ola, con los
    dos ejes derivados como el árbitro. Guardias que PARAN, verbatim del
    medidor sellado (`tools/medidor_evasion_norma_envipe25.py::carga`):
    `BP1_20` fuera de {1,2} dentro del universo es imposible por construcción
    (el universo ES ese filtro; las filas fuera se CUENTAN); `FAC_DEL` no
    numérico o <= 0 PARA; `EST_DIS`/`UPM_DIS` vacíos PARAN; `ID_PER` no única
    en `tsdem` PARA. Delitos sin persona en `tsdem` NO paran aquí (el árbitro
    sí paraba, con 0 huérfanos en 2025): se cuentan y quedan `(fuera)` de
    escolaridad -- para 2023/2024 nadie lo ha medido antes y un PARO ciego
    costaría el acto; el conteo se emite y, en 2025, el control de
    reproducción lo delata si difiere de 0."""
    zip_path = Path(zip_path)
    tmod, m_tmod, e_tmod = _lee_miembro(
        zip_path, f"conjunto_de_datos_tmod_vic_envipe{anio}.csv", COLUMNAS_TMOD)
    sdem, m_sdem, e_sdem = _lee_miembro(
        zip_path, f"conjunto_de_datos_tsdem_envipe{anio}.csv", COLUMNAS_TSDEM)
    n_archivo = len(tmod)

    en_universo = tmod["BP1_20"].isin(["1", "2"])
    n_fuera_bp1_20 = int((~en_universo).sum())
    df = tmod.loc[en_universo].copy()
    df["BP1_23n"] = df["BP1_23"].map(_dos_digitos)

    w = pd.to_numeric(df["FAC_DEL"], errors="coerce")
    malos = int(w.isna().sum() + (w <= 0).sum())
    if malos:
        raise Paro(f"ENVIPE {anio}: FAC_DEL no numérico positivo en {malos} filas")
    if (df["EST_DIS"] == "").any() or (df["UPM_DIS"] == "").any():
        raise Paro(f"ENVIPE {anio}: EST_DIS/UPM_DIS con faltantes")
    df["_w"] = w.astype(float)

    if sdem["ID_PER"].nunique() != len(sdem):
        raise Paro(f"ENVIPE {anio}: ID_PER no es llave única en tsdem: "
                   f"{sdem['ID_PER'].nunique():,} para {len(sdem):,} filas")
    niv = sdem.set_index("ID_PER")["NIV"]
    df["_NIV"] = df["ID_PER"].map(niv)
    n_huerfanos = int(df["_NIV"].isna().sum())
    df["escolaridad_proxy"] = df["_NIV"].map(ESC_2DIG).fillna(FUERA)
    df["dominio_urbano_rural"] = df["DOMINIO"].map(DOMINIO_MAP).fillna(FUERA)
    df["nacional"] = "NAC"
    df["_y"] = ((df["BP1_20"] == "2") & df["BP1_23n"].isin(INUTIL)).astype(float)
    df = df.reset_index(drop=True)

    meta = {
        "anio": anio, "zip": str(zip_path), "miembro_tmod_vic": m_tmod,
        "miembro_tsdem": m_sdem, "encoding_tmod_vic": e_tmod,
        "encoding_tsdem": e_sdem, "filas_archivo": n_archivo,
        "filas_universo": int(len(df)), "filas_bp1_20_fuera": n_fuera_bp1_20,
        "delitos_sin_persona": n_huerfanos,
        "escolaridad_fuera": int((df["escolaridad_proxy"] == FUERA).sum()),
        "dominio_fuera": int((df["dominio_urbano_rural"] == FUERA).sum()),
        "bp1_23_vacio_en_no_denuncia": int(((df["BP1_20"] == "2")
                                            & (df["BP1_23n"] == "")).sum()),
        "numerador": int(df["_y"].sum()),
        "estratos": int(df["EST_DIS"].nunique()),
        "upm": int((df["EST_DIS"] + "\x1f" + df["UPM_DIS"]).nunique()),
        "poblacion_expandida": float(df["_w"].sum()),
    }
    return Ola(anio=anio, df=df, huella=_huella(df), reservada=reservada, meta=meta)


def _verifica(ola: Ola) -> None:
    if not isinstance(ola, Ola):
        raise TypeError("se esperaba una Ola producida por carga_ola()")
    if _huella(ola.df) != ola.huella:
        raise ReservaRota(
            f"ENVIPE {ola.anio}: la ola fue filtrada o alterada tras cargarla "
            "-- agrupar sobre un subconjunto es cruzar por otra vía")


# ══ bootstrap de conglomerados estratificado, compartido por ola ══════════

@dataclass(frozen=True)
class Replicas:
    huella_ola: str
    seed: int
    n_rep: int
    counts: np.ndarray = field(repr=False, compare=False)   # (n_rep, n_upm)
    pos_fila: np.ndarray = field(repr=False, compare=False)  # fila -> upm
    n_upm: int
    estratos_upm_unica: int


def replicas_compartidas(ola: Ola, seed: int, n_rep: int) -> Replicas:
    """`n_h` UPM con reemplazo dentro de cada estrato, UN generador
    (`numpy.random.PCG64(seed)`), estratos en orden lexicográfico de
    `EST_DIS` y UPM en orden lexicográfico de `UPM_DIS`. Dos corridas sobre
    los mismos bytes dan los mismos `n_rep` vectores. Devuelve `counts`
    (cuántas veces entra cada UPM en cada réplica): `counts @ Y` da los
    totales de golpe para cualquier grupo de la ola."""
    _verifica(ola)
    est = ola.df["EST_DIS"].to_numpy()
    upm = ola.df["UPM_DIS"].to_numpy()
    claves = np.array([f"{e}\t{u}" for e, u in zip(est, upm)])
    unicas, primeras, pos_fila = np.unique(claves, return_index=True,
                                           return_inverse=True)
    upm_est = est[primeras]                          # estrato de cada UPM única
    pos_por_estrato: dict[str, list[int]] = {}
    for pos, e in enumerate(upm_est):
        pos_por_estrato.setdefault(e, []).append(pos)
    n_upm = len(unicas)
    rng = np.random.Generator(np.random.PCG64(seed))
    bloques = []
    for e in sorted(pos_por_estrato):
        pos = np.asarray(pos_por_estrato[e], dtype=np.int64)
        bloques.append(pos[rng.integers(0, len(pos), size=(n_rep, len(pos)))])
    idx = np.concatenate(bloques, axis=1)
    counts = np.empty((n_rep, n_upm), dtype=np.int32)
    for r in range(n_rep):
        counts[r] = np.bincount(idx[r], minlength=n_upm)
    unica = sum(1 for e in pos_por_estrato if len(pos_por_estrato[e]) == 1)
    return Replicas(huella_ola=ola.huella, seed=int(seed), n_rep=int(n_rep),
                    counts=counts, pos_fila=pos_fila.astype(np.int64),
                    n_upm=int(n_upm), estratos_upm_unica=int(unica))


def _reps_de_mascara(ola: Ola, rep: Replicas, mask: np.ndarray) -> np.ndarray:
    """p^(r) del grupo `mask` en cada réplica; NaN si el denominador es 0."""
    w = ola.df["_w"].to_numpy() * mask
    y = w * ola.df["_y"].to_numpy()
    W = np.bincount(rep.pos_fila, weights=w, minlength=rep.n_upm)
    Y = np.bincount(rep.pos_fila, weights=y, minlength=rep.n_upm)
    out = np.empty(rep.n_rep, dtype=float)
    for a in range(0, rep.n_rep, 1000):
        c = rep.counts[a:a + 1000].astype(np.float64)
        den = c @ W
        num = c @ Y
        with np.errstate(invalid="ignore", divide="ignore"):
            out[a:a + 1000] = np.where(den > 0, num / den, np.nan)
    return out


# ══ la función con guardia ═════════════════════════════════════════════════

def _celda_estimada(ola: Ola, mask: np.ndarray, rep: Replicas | None) -> dict:
    df = ola.df
    n = int(mask.sum())
    fila = {"n": n, "numerador": int(df["_y"].to_numpy()[mask].sum()),
            "poblacion": float(df["_w"].to_numpy()[mask].sum())}
    if n == 0:
        fila.update({"p": None, "ic95": None, "estratos": 0, "upm": 0,
                     "replicas": None})
        return fila
    sub = df.loc[mask]
    p, lo, hi, _n, n_est, n_cl = wprop_ic_conglomerado(
        sub["_y"].to_numpy(dtype=float), sub["_w"].to_numpy(dtype=float),
        sub["EST_DIS"].tolist(), sub["UPM_DIS"].tolist())
    fila.update({"p": float(p), "ic95": [float(lo), float(hi)],
                 "estratos": int(n_est), "upm": int(n_cl)})
    fila["replicas"] = _reps_de_mascara(ola, rep, mask) if rep is not None else None
    return fila


def _orden(grupo: str) -> list[str]:
    return {"escolaridad_proxy": ORD_ESC, "dominio_urbano_rural": ORD_DOMINIO,
            "nacional": ["NAC"]}[grupo]


def marginal(ola: Ola, grupo: str, *, replicas: Replicas | None = None) -> dict:
    """Celdas de UN eje de una ola. `grupo` es un `str` POSICIONAL ÚNICO --
    no hay `*grupos`, no hay lista; el eje se deriva aquí, desde columnas
    crudas, y sólo puede ser uno de `EJES`. Ver docstring del módulo."""
    if not isinstance(grupo, str):
        raise TypeError(f"grupo debe ser UN str, llegó {type(grupo).__name__}: "
                        "una sola variable de agrupación por firma")
    if grupo not in EJES:
        raise ValueError(f"grupo {grupo!r} no es un eje autorizado {EJES}; la "
                         "celda se deriva dentro de esta función, no se recibe")
    _verifica(ola)
    if replicas is not None and replicas.huella_ola != ola.huella:
        raise ReservaRota("las réplicas no son de esta ola")
    celda = ola.df[grupo].to_numpy()
    dentro = celda != FUERA
    out = {"anio": ola.anio, "eje": grupo, "n_universo": int(len(ola.df)),
           "n_fuera": int((~dentro).sum()),
           "cobertura": float(dentro.mean()) if len(ola.df) else 0.0,
           "celdas": {}}
    for k in _orden(grupo):
        out["celdas"][k] = _celda_estimada(ola, celda == k, replicas)
    return out


def cruce(ola: Ola, eje_a: str, eje_b: str, *,
          replicas: Replicas | None = None) -> dict:
    """Las celdas del cruce `eje_a × eje_b`. PROHIBIDO sobre una ola marcada
    reservada: lanza `ReservaRota`. No hay bandera que lo salte."""
    if ola.reservada:
        raise ReservaRota(f"ENVIPE {ola.anio} está RESERVADA: el cruce no se "
                          "deriva hasta que las emisiones estén selladas")
    for g in (eje_a, eje_b):
        if not isinstance(g, str) or g not in EJES or g == "nacional":
            raise ValueError(f"eje {g!r} no válido para un cruce")
    if eje_a == eje_b:
        raise ValueError("un cruce exige dos ejes distintos")
    _verifica(ola)
    a = ola.df[eje_a].to_numpy()
    b = ola.df[eje_b].to_numpy()
    dentro = (a != FUERA) & (b != FUERA)
    out = {"anio": ola.anio, "ejes": [eje_a, eje_b],
           "n_universo": int(len(ola.df)), "n_fuera": int((~dentro).sum()),
           "cobertura": float(dentro.mean()) if len(ola.df) else 0.0,
           "celdas": {}}
    for ka in _orden(eje_a):
        for kb in _orden(eje_b):
            out["celdas"][(ka, kb)] = _celda_estimada(ola, (a == ka) & (b == kb),
                                                      replicas)
    return out


# ══ control de reproducción ════════════════════════════════════════════════

def cotejo(m: dict, sellados: dict, tol_p: float, tol_ic: float) -> dict:
    """Re-derivado menos sellado, celda por celda, con signo. `sellados` es
    `{rotulo_de_celda: {p, ic95, n}}`. Nunca ajusta nada."""
    filas = {}
    peor_p, peor_ic = 0.0, 0.0
    for k, s in sellados.items():
        r = m["celdas"].get(k)
        if r is None or r["p"] is None:
            filas[k] = {"estado": "NO-ESTIMABLE"}
            continue
        d_p = r["p"] - float(s["p"])
        d_n = r["n"] - int(s["n"])
        fila = {"delta_p": d_p, "delta_n": d_n}
        if s.get("ic95") not in (None, "NO-APLICA"):
            fila["delta_ic95inf"] = r["ic95"][0] - float(s["ic95"][0])
            fila["delta_ic95sup"] = r["ic95"][1] - float(s["ic95"][1])
            peor_ic = max(peor_ic, abs(fila["delta_ic95inf"]),
                          abs(fila["delta_ic95sup"]))
        peor_p = max(peor_p, abs(d_p))
        filas[k] = fila
    veredicto = ("REPRODUCE" if peor_p <= tol_p and peor_ic <= tol_ic
                 else "NO-REPRODUCE")
    return {"filas": filas, "delta_p_max": peor_p, "delta_ic_max": peor_ic,
            "veredicto": veredicto, "tol_p": tol_p, "tol_ic": tol_ic}


# ══ CLI: sólo marginales, nunca el cruce ═══════════════════════════════════

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Marginales de UN eje de una ola de ENVIPE (unidad delito, "
                    "FAC_DEL). Nunca deriva un cruce.")
    ap.add_argument("--zip", required=True)
    ap.add_argument("--anio", type=int, required=True)
    ap.add_argument("--eje", choices=EJES, action="append", required=True)
    a = ap.parse_args(argv)
    ola = carga_ola(a.zip, a.anio, reservada=True)
    salida = {"meta": ola.meta, "marginales": {}}
    for eje in a.eje:
        m = marginal(ola, eje)
        for c in m["celdas"].values():
            c.pop("replicas", None)
        salida["marginales"][eje] = m
    print(json.dumps(salida, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
