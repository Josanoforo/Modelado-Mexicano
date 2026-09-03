#!/usr/bin/env python3
"""ACTO MAESTRA35-L7 · familia.cuidado.recae_mujeres_40mas (R5.2) · ENUT 2024.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-02-MAESTRA35-L7-spec.md` (COMMIT-1).

R5.2 del modelo (canon/modelo-decision-v4_0.md:536): «SI se trata de cuidado
(mayores, niños, enfermos) ENTONCES recae sobre mujeres 40+». R5.2 ya tiene
un veredicto Hito D PROPUESTO (no archivado) vía `forense/notas/
2026-08-04-y5-veredicto-r5-2.md` + `...y1-operacionalizacion-r5-2-enut.md`
(ENUT 2024, diseño de CONTRASTE por ocupación: reducción% ocupada-formal vs.
no-ocupada, con control de "varón disponible"). Esta pieza mide algo
DISTINTO y complementario -- la PROPORCIÓN DEL TOTAL DE HORAS DE CUIDADO DEL
HOGAR que hacen las mujeres 40+ (reparto/carga, no contraste por ocupación)
-- y NO repite esa medición.

ENUT 2019 fue investigado y NO se usa: no tiene tabla `tvar_crea` (variables
ya agregadas); habría que reconstruir "CON_CP" (cuidado pasivo/vigilancia)
desde ~40 ítems crudos de horas/minutos en 5 sub-módulos (6.11-6.15) sin
ningún precedente validado en este repo para esa bucketización -- riesgo de
la misma clase de defecto que `feedback_spec_congelada_puede_salir_degenerada`
ya documentó, bajo presupuesto que no permite validarlo con el mismo rigor.
ENUT 2024 SÍ tiene `tvar_crea.csv` con las variables ya agregadas y
validadas por el precedente Y1 (4/ago/2026, ya usado y citado por mesa).

Desenlace 1 -- horas de cuidado por sexo × tramo de edad (descriptivo,
media ponderada, NO proporción binaria): reusa `wprop_ic_conglomerado` con
`d` continuo (la función no exige binario, solo pondera y bootstrapea sumas).

Desenlace 2 -- proporción del total de horas de cuidado del HOGAR que
aportan mujeres 40+: estimador de RAZÓN (Σ w·num / Σ w·den), NO proporción
de un binario -- función nueva `wratio_ic_conglomerado` en este archivo,
mismo esquema de bootstrap por conglomerado que `wprop_ic_conglomerado`
(mismo estrato/UPM, mismo n_boot/seed), generalizado a dos sumas.

`horas_cuidado` = CUID_ESP_INT_HOG_CON_CP + CUID_INT_0A5_CON_CP +
CUID_INT_6A14_CON_CP + CUID_INT_60MAS_CON_CP -- IDÉNTICA a la definición ya
usada por el precedente Y1 (`...y1-operacionalizacion-r5-2-enut.md §Desenlace`),
reusada, no redefinida.

Unidad: PERSONA para D1 (ponderador FAC_PER); HOGAR para D2 (ponderador
FAC_HOG, tomado de `tsdem.csv` -- FAC_PER no es constante dentro de hogar,
verificado; FAC_HOG y EST_DIS/UPM_DIS sí lo son, verificado). Bootstrap
conglomerado n_boot=10000 seed=42.
"""
import hashlib
import os
import sys
import zipfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ejes_maestra35_l1 import Eje, imprime, mide_eje, tramos_edad  # noqa: E402
from calibracion_mordida_encig_serie import wprop_ic_conglomerado  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
ZIP = os.path.join(RAW, "enut2024_bd_csv.zip")

CUID_COLS = ["CUID_ESP_INT_HOG_CON_CP", "CUID_INT_0A5_CON_CP",
             "CUID_INT_6A14_CON_CP", "CUID_INT_60MAS_CON_CP"]

EJE_SEXO_EDAD = Eje(
    "sexo_edad", lambda d: d["_sexo_edad"], None, None,
    "descriptivo: media de horas_cuidado por sexo × tramo de edad; sin "
    "signo pre-registrado -- veredicto máximo posible DISCRIMINA")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def wratio_ic_conglomerado(num, den, w, estrato, upm, n_boot=10000, seed=42):
    """Estimador de razón Σ(w·num)/Σ(w·den), bootstrap por conglomerado
    (mismo esquema de resampleo que wprop_ic_conglomerado, generalizado a
    dos sumas en vez de una proporción de binario)."""
    num = np.asarray(num, dtype=float)
    den = np.asarray(den, dtype=float)
    w = np.asarray(w, dtype=float)
    r_hat = float((w * num).sum() / (w * den).sum())

    llave = pd.Series([f"{e}\x1f{u}" for e, u in zip(estrato, upm)],
                       dtype="object")
    cl_id, _ = pd.factorize(llave)
    n_cl = cl_id.max() + 1
    swn = np.bincount(cl_id, weights=w * num, minlength=n_cl)
    swd = np.bincount(cl_id, weights=w * den, minlength=n_cl)
    est_de_cl = pd.Series(list(estrato)).groupby(cl_id).first().to_numpy()
    orden = np.argsort(pd.factorize(pd.Series(est_de_cl))[0], kind="stable")
    swn, swd = swn[orden], swd[orden]
    est_ord = pd.factorize(pd.Series(est_de_cl[orden]))[0]

    tam_est = np.bincount(est_ord)
    inicio_est = np.concatenate([[0], np.cumsum(tam_est)[:-1]])
    inicio = inicio_est[est_ord].astype(np.int64)
    tam = tam_est[est_ord].astype(np.int64)

    rng = np.random.default_rng(seed)
    boots = np.empty(n_boot, dtype=float)
    hecho = 0
    CHUNK = 500
    while hecho < n_boot:
        b = min(CHUNK, n_boot - hecho)
        idx = inicio + (rng.random((b, len(swn))) * tam).astype(np.int64)
        boots[hecho:hecho + b] = swn[idx].sum(axis=1) / swd[idx].sum(axis=1)
        hecho += b
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return r_hat, float(lo), float(hi), int(w.sum() > 0) and len(num), n_cl


def carga():
    with zipfile.ZipFile(ZIP) as z:
        tv = pd.read_csv(z.open("tvar_crea.csv"), dtype=str, low_memory=False)
        ts = pd.read_csv(z.open("tsdem.csv"), dtype=str, low_memory=False,
                          usecols=["LLAVEHOG", "FAC_HOG"])
    necesarias = (CUID_COLS + ["LLAVEHOG", "EDAD", "SEXO", "FAC_PER",
                                "EST_DIS", "UPM_DIS"])
    faltan = [c for c in necesarias if c not in tv.columns]
    if faltan:
        raise SystemExit(f"PARO · faltan columnas en tvar_crea.csv: {faltan}")
    for c in CUID_COLS:
        val = pd.to_numeric(tv[c], errors="coerce")
        if val.isna().any():
            raise SystemExit(f"PARO · {c} no numérico en "
                              f"{int(val.isna().sum())} filas")
        tv[c] = val
    tv["_horas_cuidado"] = tv[CUID_COLS].sum(axis=1)
    edad = pd.to_numeric(tv["EDAD"], errors="coerce")
    if edad.isna().any():
        raise SystemExit("PARO · EDAD no numérica")
    w = pd.to_numeric(tv["FAC_PER"], errors="coerce")
    if w.isna().any() or (w <= 0).any():
        raise SystemExit("PARO · FAC_PER no numérico positivo")
    tv["_edad"] = edad
    tv["_w"] = w

    hog_const = tv.groupby("LLAVEHOG")[["EST_DIS", "UPM_DIS"]].nunique()
    if (hog_const != 1).any().any():
        raise SystemExit("PARO · EST_DIS/UPM_DIS no constantes dentro de hogar")

    ts_g = ts.drop_duplicates("LLAVEHOG").set_index("LLAVEHOG")["FAC_HOG"]
    faltan_hog = set(tv["LLAVEHOG"]) - set(ts_g.index)
    if faltan_hog:
        raise SystemExit(f"PARO · {len(faltan_hog)} hogares de tvar_crea "
                          "sin FAC_HOG en tsdem")
    tv["_fac_hog"] = tv["LLAVEHOG"].map(ts_g).astype(float)
    return tv


def main():
    print("ACTO MAESTRA35-L7 · familia.cuidado · ENUT 2024")
    print(f"payload  : {os.path.basename(ZIP)}")
    print(f"sha256   : {sha256(ZIP)}")
    df = carga()
    print(f"tabla    : tvar_crea.csv · {len(df):,} personas · "
          f"{df['LLAVEHOG'].nunique():,} hogares")
    print()

    print("=" * 78)
    print("D1 · horas de cuidado por sexo × tramo de edad (media ponderada, "
          "unidad = PERSONA)")
    print("=" * 78)
    df["_edad_tramo"] = tramos_edad(df["_edad"].astype(str))
    edad_amplio = pd.Series("(fuera)", index=df.index, dtype=object)
    e = df["_edad"]
    edad_amplio[(e >= 12) & (e <= 17)] = "12-17"
    edad_amplio[(e >= 18) & (e <= 29)] = "18-29"
    edad_amplio[(e >= 30) & (e <= 39)] = "30-39"
    edad_amplio[(e >= 40) & (e <= 59)] = "40-59"
    edad_amplio[(e >= 60)] = "60+"
    sexo_txt = df["SEXO"].map({"1": "hombre", "2": "mujer"})
    df["_sexo_edad"] = sexo_txt.str.cat(edad_amplio, sep=" · ")

    orden_se = [f"{s} · {a}" for a in
                ["12-17", "18-29", "30-39", "40-59", "60+"]
                for s in ["hombre", "mujer"]]
    eje = Eje("sexo_edad", lambda d: d["_sexo_edad"], orden_se, None,
              "descriptivo, sin signo pre-registrado")
    r_d1 = mide_eje(df, eje, df["_horas_cuidado"], df["_w"],
                     df["EST_DIS"], df["UPM_DIS"])
    imprime(r_d1, "personas (horas/semana promedio, no proporción)")

    print("=" * 78)
    print("D2 · proporción del total de horas de cuidado del HOGAR que "
          "hacen mujeres 40+ (unidad = HOGAR, razón)")
    print("=" * 78)
    df["_mujer40"] = (df["SEXO"] == "2") & (df["_edad"] >= 40)
    df["_horas_mujer40"] = np.where(df["_mujer40"], df["_horas_cuidado"], 0.0)

    hog = df.groupby("LLAVEHOG").agg(
        total_hogar=("_horas_cuidado", "sum"),
        cuidado_mujeres40=("_horas_mujer40", "sum"),
        fac_hog=("_fac_hog", "first"),
        est_dis=("EST_DIS", "first"),
        upm_dis=("UPM_DIS", "first"),
        n_integrantes=("_horas_cuidado", "size"),
    ).reset_index()

    n_con_carga = int((hog["total_hogar"] > 0).sum())
    print(f"hogares totales: {len(hog):,} · con alguna hora de cuidado "
          f"registrada (total_hogar>0): {n_con_carga:,} "
          f"({n_con_carga/len(hog):.4%})")
    n_sin_mujer40 = int((~hog["LLAVEHOG"].isin(
        df.loc[df['_mujer40'], 'LLAVEHOG'])).sum())
    print(f"hogares sin ninguna mujer 40+ (aportan 0 al numerador, "
          f"correctamente, sin excluirse del denominador): {n_sin_mujer40:,}")

    r_hat, lo, hi, n, n_cl = wratio_ic_conglomerado(
        hog["cuidado_mujeres40"].to_numpy(), hog["total_hogar"].to_numpy(),
        hog["fac_hog"].to_numpy(), hog["est_dis"].tolist(),
        hog["upm_dis"].tolist())
    print(f"  proporción del total de horas de cuidado del hogar hecha por "
          f"mujeres 40+:")
    print(f"  r̂ = {r_hat:.6f}  IC95 = [{lo:.6f}, {hi:.6f}]  "
          f"n_hogares = {len(hog):,} · UPM = {n_cl:,}")

    # sobre el subconjunto de hogares CON carga de cuidado (la razón entre
    # hogares sin carga es 0/0, ya excluida algebraicamente arriba; esta
    # segunda cifra es descriptiva, sobre el universo donde la pregunta
    # "quién carga" tiene sentido)
    hog_con = hog[hog["total_hogar"] > 0]
    r2, lo2, hi2, n2, ncl2 = wratio_ic_conglomerado(
        hog_con["cuidado_mujeres40"].to_numpy(), hog_con["total_hogar"].to_numpy(),
        hog_con["fac_hog"].to_numpy(), hog_con["est_dis"].tolist(),
        hog_con["upm_dis"].tolist())
    print(f"  MISMO, solo hogares con total_hogar>0 (descriptivo, universo "
          f"restringido):")
    print(f"  r̂ = {r2:.6f}  IC95 = [{lo2:.6f}, {hi2:.6f}]  "
          f"n_hogares = {len(hog_con):,} · UPM = {ncl2:,}")

    return {"d1_sexo_edad": r_d1,
            "d2_razon_todos": {"r": r_hat, "lo": lo, "hi": hi, "n": len(hog)},
            "d2_razon_con_carga": {"r": r2, "lo": lo2, "hi": hi2,
                                    "n": len(hog_con)}}


if __name__ == "__main__":
    main()
