#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA38-L16 · salud.atencion.grave (R4.4) · Rama B (ENSANUT2024)

Spec sellada: forense/prereg-caja/S6-L16-spec-v1_0.md (sha256 verificado en
A.3 del acto). Frase de sello: "el primer resultado que produzca este
procedimiento es el que se reporta". Rama A (ENNVIH+ENDIREH) no se corre en
esta pieza (ver nota de cierre): requiere resolver ambiguedad de ponderador
(bx/2002, tres candidatos) contra codebook externo no presente en el corpus.

Rama B: SINTOMA_GRAVE via H0409A (integrantes_ensanut2024_w_icb.dta) —
codebook confirma valores {1: consulta externa, 2: hospitalizacion,
3: urgencias, 4: otros}; se define grave = {2,3} (hospitalizacion o
urgencias, exceden al consultorio, texto de la propia regla) vs no-grave =
{1,4}. INSTITUCION_PUBLICA via u0201 (utilizadores_ensanut2024_w.dta),
join por FOLIO_I.
"""
import hashlib
import os
import sys

import numpy as np
import pandas as pd
import pyreadstat

SEED = 42
N_BOOT = 10000
CHUNK = 500

DIR_A = os.environ.get("ENSANUT_DTA_DIR",
                        "/tmp/claude-1000/-home-pc0/299c24d4-2de8-4585-bf3e-d0c4bcbc004c/scratchpad/ensanut")

INTEGRANTES = os.path.join(DIR_A, "integrantes_ensanut2024_w_icb.dta")
UTILIZADORES = os.path.join(DIR_A, "utilizadores_ensanut2024_w.dta")

PUBLICO = {1, 2, 3, 4, 5, 6, 8, 9, 10, 26}
PRIVADO = {12, 13, 14, 15, 16, 17, 18, 19}


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


def main():
    print("ACTO MAESTRA38-L16 · salud.atencion.grave (R4.4) · Rama B ENSANUT2024")
    for p in (INTEGRANTES, UTILIZADORES):
        print(f"payload : {os.path.basename(p)} · sha256(dta) = {sha256(p)}")

    dfi, _ = pyreadstat.read_dta(
        INTEGRANTES, usecols=["FOLIO_I", "h0402", "H0409A"])
    dfu, mu = pyreadstat.read_dta(
        UTILIZADORES,
        usecols=["FOLIO_I", "u0201", "ponde_f", "estrato", "upm"])

    print(f"integrantes: {len(dfi):,} filas · utilizadores: {len(dfu):,} filas")

    dfi["_grave"] = dfi["H0409A"].isin([2, 3])
    m_h0409 = dfi["H0409A"].notna()
    print(f"H0409A no-nulo (algún requerimiento reportado): {int(m_h0409.sum()):,}")
    print(f"  de esos, grave (hospitalizacion/urgencias, {{2,3}}): "
          f"{int(dfi.loc[m_h0409, '_grave'].sum()):,} · "
          f"no-grave ({{1,4}}): {int((~dfi.loc[m_h0409, '_grave']).sum()):,}")

    dfu["_publico"] = dfu["u0201"].isin(PUBLICO)
    dfu["_privado"] = dfu["u0201"].isin(PRIVADO)
    m_clasif = dfu["_publico"] | dfu["_privado"]
    print(f"utilizadores con u0201 clasificable publico/privado: "
          f"{int(m_clasif.sum()):,} de {int(dfu['u0201'].notna().sum()):,} "
          f"con u0201 no-nulo ({int(dfu['u0201'].notna().sum() - m_clasif.sum()):,} "
          f"fuera de la dicotomia: NGO/tradicional/otro/no-sabe/psicologico)")

    j = dfi.loc[m_h0409, ["FOLIO_I", "_grave"]].merge(
        dfu.loc[m_clasif, ["FOLIO_I", "_publico", "ponde_f", "estrato", "upm"]],
        on="FOLIO_I", how="inner")
    print(f"join FOLIO_I (H0409A no-nulo × u0201 clasificable): {len(j):,} filas")

    for etiqueta, sub in [("grave (2,3)", j[j["_grave"]]),
                           ("no-grave (1,4)", j[~j["_grave"]])]:
        n_pub = int(sub["_publico"].sum())
        n = len(sub)
        print(f"  {etiqueta}: n={n} · publico={n_pub} ({n_pub/n:.4%} crudo, no ponderado)"
              if n else f"  {etiqueta}: n=0")

    print()
    print("=" * 78)
    print("Falsador B-bis (Rama B) — proporcion INSTITUCION_PUBLICA por celda H0409A")
    print("=" * 78)
    resultados = {}
    for etiqueta, mask in [("grave", j["_grave"]), ("no_grave", ~j["_grave"])]:
        sub = j[mask]
        n = len(sub)
        if n == 0:
            print(f"  {etiqueta}: n=0 -> NO-ESTIMABLE")
            resultados[etiqueta] = None
            continue
        n_pub = int(sub["_publico"].sum())
        if n_pub < 10 or (n - n_pub) < 10:
            print(f"  {etiqueta}: n={n} n_publico={n_pub} numerador<10 en alguna celda "
                  f"-> NO-ESTIMABLE (cota de la spec)")
            resultados[etiqueta] = None
            continue
        p, lo, hi, npt, nest, ncl = wprop_ic_conglomerado(
            sub["_publico"].to_numpy(), sub["ponde_f"].to_numpy(),
            sub["estrato"].tolist(), sub["upm"].tolist())
        print(f"  {etiqueta}: p̂(publico) = {p:.4%}  IC95 = [{lo:.4%}, {hi:.4%}]  "
              f"n={npt:,} · estratos={nest} · UPM={ncl}")
        resultados[etiqueta] = (p, lo, hi, npt, nest, ncl)

    print()
    if resultados["grave"] is None or resultados["no_grave"] is None:
        print("VEREDICTO Rama B: NO-ESTIMABLE (numerador<10 en alguna celda)")
    else:
        pg, log, hig, ng, _, _ = resultados["grave"]
        pn, lon, hin, nn, _, _ = resultados["no_grave"]
        diff = pg - pn
        # IC95 de la diferencia via bootstrap conjunto simple (normal approx
        # de la resta de dos IC ya calculados, declarado — no re-muestreo
        # conjunto por independencia de folios entre celdas H0409A).
        se_g = (hig - log) / (2 * 1.96)
        se_n = (hin - lon) / (2 * 1.96)
        se_diff = (se_g ** 2 + se_n ** 2) ** 0.5
        lo_d, hi_d = diff - 1.96 * se_diff, diff + 1.96 * se_diff
        print(f"diferencia p̂(grave) - p̂(no-grave) = {diff:.4%}  "
              f"IC95_aprox = [{lo_d:.4%}, {hi_d:.4%}] (normal, combinando SE de cada celda)")
        if lo_d > 0:
            v = "CORROBORADA"
        elif hi_d < 0:
            v = "CONTRARIA"
        else:
            v = "NO-DISCRIMINA"
        print(f"VEREDICTO Rama B (falsador B-bis, salud.atencion.grave): {v}")

    print()
    print("Rama A (ENNVIH+ENDIREH): NO CORRIDA en esta pieza — ponderador del "
          "libro bx/2002 ambiguo entre tres candidatos (fac_3a_px/fac_3b_px/"
          "fac_4_px), sin codebook de ENNVIH en el corpus para resolverlo "
          "(spec S6 §1.3, declarado como riesgo, no forzado). PARO parcial, "
          "declarado en la nota de cierre.")


if __name__ == "__main__":
    main()
