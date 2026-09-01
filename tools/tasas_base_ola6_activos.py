#!/usr/bin/env python3
"""ACTO MAESTRA33-E18-P3 · REGLAS-OLA6-ACTIVOS-L1 — COMMIT-2 por regla

Calcula `p` = proporcion ponderada del desenlace=1 en su universo, para las
reglas del lote cuya spec quedo congelada en
`forense/notas/2026-09-01-MAESTRA33-E18-P3-L1-spec.md`.

IC95 por **bootstrap por conglomerado estratificado**: remuestrea UPMs con
reemplazo dentro de cada estrato, 10 000 replicas, seed 42. Es el estimador
ya precedentado en `tools/medicion_familismo.py:274-301` (ACTO MAESTRA32-E16,
ADR-235) -- NO el bootstrap simple por fila de `tools/tasas_base_fase1.py`,
porque las dos fuentes de este lote SI traen campos de diseno verificados
(ENIGH: est_dis/upm en las 6 olas; ENFIH2019: EDIS/UPM_DIS).

Reformulacion exacta usada para que corra en 90k filas x 10k replicas: la
proporcion ponderada solo depende de los totales por conglomerado
(sum de w y sum de w*d por UPM), asi que se remuestrean esos totales, no las
filas. Da el mismo estimador que remuestrear filas enteras dentro de la UPM.

Generador: `numpy.random.default_rng(42)` (PCG64) -- declarado porque NO es
el `random.Random(42)` de la casa; con 6 olas x 10k replicas el generador de
la biblioteca estandar no termina en la corrida unica del acto.

Este script solo IMPRIME. Quien ejecuta el acto pega el resultado en
`milpa/tramite-ola5-propuesta-v0.yaml`, igual que pidio el precedente.

Uso:
    python3 tools/tasas_base_ola6_activos.py [--regla 1|2]
"""
import argparse
import hashlib
import io
import os
import zipfile

import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
SEED = 42
N_BOOT = 10000
CHUNK = 500

# (ola, zip, miembro, columna de ponderador) -- el ponderador cambia de
# nombre entre series y por eso se declara por ola, no una vez.
ENIGH = {
    2012: ("enigh2012_nc_csv.zip",
           "concentradohogar_enigh2012ncv/conjunto_de_datos/concentradohogar.csv",
           "factor_hog"),
    2014: ("enigh2014_nc_csv.zip",
           "concentradohogar_enigh2014ncv/conjunto_de_datos/concentradohogar.csv",
           "factor_hog"),
    2016: ("enigh2016_nc_csv.zip",
           "conjunto_de_datos_concentradohogar_enigh_2016_ns/conjunto_de_datos/"
           "conjunto_de_datos_concentradohogar_enigh_2016_ns.csv", "factor"),
    2018: ("enigh2018_nc_csv.zip",
           "conjunto_de_datos_concentradohogar_enigh_2018_ns/conjunto_de_datos/"
           "conjunto_de_datos_concentradohogar_enigh_2018_ns.csv", "factor"),
    2020: ("enigh2020_nc_csv.zip",
           "conjunto_de_datos_concentradohogar_enigh_2020_ns/conjunto_de_datos/"
           "conjunto_de_datos_concentradohogar_enigh_2020_ns.csv", "factor"),
    2022: ("enigh2022_nc_csv.zip",
           "conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/"
           "conjunto_de_datos_concentradohogar_enigh2022_ns.csv", "factor"),
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wprop_ic_conglomerado(d, w, estrato, upm, n_boot=N_BOOT, seed=SEED):
    """Proporcion ponderada + IC95 por bootstrap de UPMs dentro de estrato.

    d, w: arrays float. estrato, upm: arrays de etiquetas (se combinan en una
    llave de conglomerado, porque la numeracion de UPM puede reiniciarse
    dentro de cada estrato).
    Devuelve (p_hat, lo, hi, n_filas, n_estratos, n_upm).
    """
    d = np.asarray(d, dtype=float)
    w = np.asarray(w, dtype=float)
    p_hat = float((w * d).sum() / w.sum())

    llave = pd.Series(
        [f"{e}\x1f{u}" for e, u in zip(estrato, upm)], dtype="object")
    cl_id, _ = pd.factorize(llave)
    n_cl = cl_id.max() + 1
    # totales por conglomerado
    sw = np.bincount(cl_id, weights=w, minlength=n_cl)
    swd = np.bincount(cl_id, weights=w * d, minlength=n_cl)
    # estrato de cada conglomerado
    est_de_cl = pd.Series(list(estrato)).groupby(cl_id).first().to_numpy()
    orden = np.argsort(pd.factorize(pd.Series(est_de_cl))[0], kind="stable")
    sw, swd = sw[orden], swd[orden]
    est_ord = pd.factorize(pd.Series(est_de_cl[orden]))[0]

    # bloque contiguo por estrato: inicio y tamano por posicion
    tam_est = np.bincount(est_ord)
    inicio_est = np.concatenate([[0], np.cumsum(tam_est)[:-1]])
    inicio = inicio_est[est_ord].astype(np.int64)
    tam = tam_est[est_ord].astype(np.int64)

    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot, dtype=float)
    hecho = 0
    while hecho < n_boot:
        b = min(CHUNK, n_boot - hecho)
        idx = inicio + (rng.random((b, len(sw))) * tam).astype(np.int64)
        boots[hecho:hecho + b] = swd[idx].sum(axis=1) / sw[idx].sum(axis=1)
        hecho += b
    boots.sort()
    lo = float(boots[int(0.025 * n_boot)])
    hi = float(boots[int(0.975 * n_boot) - 1])
    return p_hat, lo, hi, len(d), int(tam_est.size), int(n_cl)


def regla1_remesas():
    """familia.seguro.volatilidad_ausencia_estado -- ENIGH x6, `remesas`>0."""
    print("=" * 72)
    print("REGLA 1 · familia.seguro.volatilidad_ausencia_estado")
    print("  desenlace: recibe_remesas = 1 si concentradohogar.remesas > 0")
    print("=" * 72)
    out = {}
    for ola, (zn, miembro, fac) in ENIGH.items():
        zpath = os.path.join(RAW, zn)
        if not os.path.exists(zpath):
            print(f"  {ola}: NO-ENCONTRADO ({zpath})")
            continue
        sha = sha256(zpath)
        with zipfile.ZipFile(zpath) as z, z.open(miembro) as f:
            df = pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"),
                             low_memory=False)
        df.columns = [c.strip().lstrip("﻿") for c in df.columns]
        for col in ("remesas", fac, "est_dis", "upm"):
            assert col in df.columns, f"{ola}: falta columna {col}"
        rem = pd.to_numeric(df["remesas"], errors="coerce")
        assert rem.isna().sum() == 0, f"{ola}: remesas trae nulos"
        d = (rem > 0).astype(float).to_numpy()
        w = pd.to_numeric(df[fac], errors="coerce").to_numpy()
        p, lo, hi, n, ne, nu = wprop_ic_conglomerado(
            d, w, df["est_dis"].astype(str).to_numpy(),
            df["upm"].astype(str).to_numpy())
        out[ola] = dict(p=p, ic95=[lo, hi], n=n, estratos=ne, upm=nu,
                        ponderador=fac, sha256=sha, pob=float(w.sum()))
        print(f"  ENIGH {ola}: p={p:.6f}  IC95=[{lo:.6f}, {hi:.6f}]  "
              f"n={n}  estratos={ne}  UPM={nu}  pond={fac}")
        print(f"             hogares expandidos={w.sum():,.0f}  sha256={sha[:12]}…")
    return out


def regla2_afore():
    """dinero.planeacion.formal_estable -- ENFIH2019, `C_AFORE`=1."""
    print("=" * 72)
    print("REGLA 2 · dinero.planeacion.formal_estable")
    print("  desenlace: tiene_afore = C_AFORE (0/1 crudo, FD ENFIH2019)")
    print("=" * 72)
    zpath = os.path.join(RAW, "enfih2019", "enfih_2019_base_de_datos_csv.zip")
    if not os.path.exists(zpath):
        print(f"  NO-ENCONTRADO ({zpath})")
        return {}
    sha = sha256(zpath)
    with zipfile.ZipFile(zpath) as z, z.open("TCONCENTRADORA.csv") as f:
        df = pd.read_csv(io.TextIOWrapper(f, encoding="latin-1"),
                         low_memory=False)
    for col in ("C_AFORE", "FAC_HOG", "EDIS", "UPM_DIS"):
        assert col in df.columns, f"falta columna {col}"
    ca = pd.to_numeric(df["C_AFORE"], errors="coerce")
    assert ca.isna().sum() == 0, "C_AFORE trae nulos"
    assert set(ca.unique()) <= {0, 1}, f"C_AFORE fuera de 0/1: {set(ca.unique())}"
    d = ca.astype(float).to_numpy()
    w = pd.to_numeric(df["FAC_HOG"], errors="coerce").to_numpy()
    p, lo, hi, n, ne, nu = wprop_ic_conglomerado(
        d, w, df["EDIS"].astype(str).to_numpy(),
        df["UPM_DIS"].astype(str).to_numpy())
    print(f"  ENFIH 2019: p={p:.6f}  IC95=[{lo:.6f}, {hi:.6f}]  "
          f"n={n}  estratos={ne}  UPM={nu}  pond=FAC_HOG")
    print(f"              hogares expandidos={w.sum():,.0f}  sha256={sha[:12]}…")

    # --- robustez: universo restringido a hogar principal --------------
    m = df["H_PPAL"] == 1
    pp, plo, phi, pn, pne, pnu = wprop_ic_conglomerado(
        d[m.to_numpy()], w[m.to_numpy()],
        df.loc[m, "EDIS"].astype(str).to_numpy(),
        df.loc[m, "UPM_DIS"].astype(str).to_numpy())
    print(f"  [robustez] H_PPAL=1: p={pp:.6f}  IC95=[{plo:.6f}, {phi:.6f}]  n={pn}")

    # --- DESCRIPTIVO, NO es la p de la regla ---------------------------
    # CAT_POS es posicion en el trabajo de la persona de referencia. NO es
    # formalidad (un empleado puede ser informal) y por eso esto NO se sella
    # como condicional: solo muestra si la DIRECCION de la regla se sostiene.
    lab = {0: "no ocupada", 1: "empleado/obrero", 2: "jornalero/peon",
           3: "patron", 4: "por su cuenta", 5: "familiar sin pago"}
    print("  [descriptivo, NO sellado] tasa ponderada de AFORE por CAT_POS:")
    for v in sorted(df["CAT_POS"].unique()):
        mm = (df["CAT_POS"] == v).to_numpy()
        pv = float((w[mm] * d[mm]).sum() / w[mm].sum())
        print(f"      CAT_POS={v} ({lab.get(v, v):<18}) n={mm.sum():>5}  p={pv:.4f}")
    return {2019: dict(p=p, ic95=[lo, hi], n=n, estratos=ne, upm=nu,
                       ponderador="FAC_HOG", sha256=sha, pob=float(w.sum()))}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--regla", choices=["1", "2"], default=None)
    a = ap.parse_args()
    if a.regla in (None, "1"):
        regla1_remesas()
    if a.regla in (None, "2"):
        regla2_afore()
