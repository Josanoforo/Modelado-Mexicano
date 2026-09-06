#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA38-L17 · salud.vacunacion.disponible (R9.2) · Ramas B (primaria)
y C (corroboración de tasa). Spec sellada:
forense/prereg-caja/S7-L17-spec-v1_0.md (sha256 verificado en A.3 del acto).

Codebook confirma que el §2 de la spec invirtió la asignación letra/dígito:
la LETRA (a-e) es la RAZÓN declarada, el DÍGITO (1-4) es la VACUNA
(1=Influenza, 2=Neumococo, 3=Tétanos, 4=Otra) — verificado contra las
etiquetas del .dta, no asumido del inventario (que no las despliega en una
sola fila legible, tal como la spec §2 ya advertía). Reasignación declarada,
no forzada al patrón original de la spec.

Rama A (ENNVIH) no se corre: mismo pendiente de ponderador de bx/2002 que
L16, y además sujeta a la reserva de diseño §0.3 (post-tratamiento) no
resuelta por falta de codebook ENNVIH en el corpus.
"""
import hashlib
import os

import numpy as np
import pandas as pd
import pyreadstat

SEED = 42
N_BOOT = 10000
CHUNK = 500

DIR_A = os.environ.get("ENSANUT_DTA_DIR",
                        "/tmp/claude-1000/-home-pc0/299c24d4-2de8-4585-bf3e-d0c4bcbc004c/scratchpad/ensanut")
ADULTOS = os.path.join(DIR_A, "adultos_ensanut2024_w.dta")
ADOLESC = os.path.join(DIR_A, "adolescentes_ensanut2024_w.dta")

RAZONES = {"a": "no_habia_vacunas", "b": "no_derechohabiente",
           "c": "no_estaba_quien_aplica", "d": "enfermo", "e": "otra_razon"}
LOGISTICA = {"a", "c"}
VACUNAS = ["1", "2", "3", "4"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wprop_ic_conglomerado(d, w, estrato, upm, n_boot=N_BOOT, seed=SEED):
    """Verbatim del estimador de tools/calibracion_mordida_encig_serie.py."""
    d = np.asarray(d, dtype=float)
    w = np.asarray(w, dtype=float)
    p_hat = float((w * d).sum() / w.sum())

    llave = pd.Series(
        [f"{e}\x1f{u}" for e, u in zip(estrato, upm)], dtype="object")
    cl_id, _ = pd.factorize(llave)
    n_cl = cl_id.max() + 1
    sw = np.bincount(cl_id, weights=w, minlength=n_cl)
    swd = np.bincount(cl_id, weights=w * d, minlength=n_cl)
    est_de_cl = pd.Series(list(estrato)).groupby(cl_id).first().to_numpy()
    orden = np.argsort(pd.factorize(pd.Series(est_de_cl))[0], kind="stable")
    sw, swd = sw[orden], swd[orden]
    est_ord = pd.factorize(pd.Series(est_de_cl[orden]))[0]

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


def rama_b():
    print("=" * 78)
    print("Rama B (primaria) — razon de no vacunacion, adultos_ensanut2024_w")
    print("=" * 78)
    cols = [f"a0927{l}{v}" for l in RAZONES for v in VACUNAS]
    df, meta = pyreadstat.read_dta(
        ADULTOS, usecols=["FOLIO_I", "ponde_f", "estrato", "upm"] + cols)
    print(f"payload : adultos_ensanut2024_w.dta · sha256(dta) = {sha256(ADULTOS)}")
    print(f"personas en el .dta: {len(df):,}")

    # una fila = una mencion (persona x vacuna x razon marcada 'Si'=1)
    filas = []
    for l, nombre in RAZONES.items():
        for v in VACUNAS:
            col = f"a0927{l}{v}"
            m = df[col] == 1
            if m.sum() == 0:
                continue
            sub = df.loc[m, ["FOLIO_I", "ponde_f", "estrato", "upm"]].copy()
            sub["_razon"] = nombre
            sub["_logistica"] = l in LOGISTICA
            filas.append(sub)
    men = pd.concat(filas, ignore_index=True)
    print(f"total de menciones 'Si' (persona x vacuna x razon): {len(men):,} "
          f"({men['FOLIO_I'].nunique():,} personas distintas)")
    print("desglose por razon (conteo crudo de menciones):")
    print(men["_razon"].value_counts())

    n = len(men)
    n_log = int(men["_logistica"].sum())
    if n < 20 or min(n_log, n - n_log) < 10:
        print(f"\nn={n} n_logistica={n_log} numerador<10 en alguna celda -> NO-ESTIMABLE")
        return
    p, lo, hi, npt, nest, ncl = wprop_ic_conglomerado(
        men["_logistica"].to_numpy(), men["ponde_f"].to_numpy(),
        men["estrato"].tolist(), men["upm"].tolist())
    print(f"\np̂(RAZON_LOGISTICA) = {p:.4%}  IC95 = [{lo:.4%}, {hi:.4%}]  "
          f"n={npt:,} menciones · estratos={nest} · UPM={ncl}")
    if lo > 0.5:
        v = "CORROBORADA"
    elif hi < 0.5:
        v = "CONTRARIA"
    else:
        v = "NO-DISCRIMINA"
    print(f"VEREDICTO Rama B (falsador B-bis primario, salud.vacunacion.disponible): {v}")


def rama_c():
    print()
    print("=" * 78)
    print("Rama C (corroboracion de tasa) — adolescentes_ensanut2024_w")
    print("=" * 78)
    cols = ["d0321j", "d0321p", "d0508", "d05041", "d05051"]
    df, meta = pyreadstat.read_dta(
        ADOLESC, usecols=["FOLIO_I", "ponde_f", "estrato", "upm"] + cols)
    print(f"payload : adolescentes_ensanut2024_w.dta · sha256(dta) = {sha256(ADOLESC)}")
    print(f"personas en el .dta: {len(df):,}")
    for c in cols:
        sub = df[df[c].isin([1, 2])]
        n = len(sub)
        if n == 0:
            print(f"  {c}: n=0 -> NO-ESTIMABLE")
            continue
        d = (sub[c] == 1).to_numpy()
        n_si = int(d.sum())
        if min(n_si, n - n_si) < 10:
            print(f"  {c}: n={n} n_si={n_si} numerador<10 en alguna celda -> NO-ESTIMABLE")
            continue
        p, lo, hi, npt, nest, ncl = wprop_ic_conglomerado(
            d, sub["ponde_f"].to_numpy(), sub["estrato"].tolist(), sub["upm"].tolist())
        if lo > 0.5:
            v = "CORROBORADA (mayoria acepta)"
        elif hi < 0.5:
            v = "CONTRARIA (mayoria NO acepta)"
        else:
            v = "NO-DISCRIMINA"
        print(f"  {c}: p̂(aceptó) = {p:.4%}  IC95 = [{lo:.4%}, {hi:.4%}]  "
              f"n={npt:,} · estratos={nest} · UPM={ncl}  -> {v}")


def main():
    print("ACTO MAESTRA38-L17 · salud.vacunacion.disponible (R9.2)")
    rama_b()
    rama_c()
    print()
    print("Rama A (ENNVIH): NO CORRIDA en esta pieza — mismo pendiente de "
          "ponderador ambiguo (bx/2002) que L16 §S6/S7, mas la reserva de "
          "diseno §0.3 (ce19d_2/hs16d_2 posiblemente post-tratamiento, no "
          "confirmable sin codebook de ENNVIH en el corpus). PARO parcial, "
          "declarado en la nota de cierre; no bloquea el veredicto de la "
          "Rama B, que es la primaria de esta spec.")


if __name__ == "__main__":
    main()
