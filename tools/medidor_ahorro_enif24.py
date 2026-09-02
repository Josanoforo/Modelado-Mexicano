#!/usr/bin/env python3
"""ACTO MAESTRA34-L5 · P4 · tenencia de ahorro (formal ∪ informal), ENIF 2024.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-02-MAESTRA34-L5-P4-spec.md` (COMMIT-1).

RE-MEDICIÓN de `dinero.ahorro.tiene_ahorros` (milpa/tramite.yaml:285-303), que
ya está MEDIDA sobre ENNViH ola 2 (2005-06) con p=0.174804. Esta corrida añade
la ola 2024; NO forma serie con aquella (acervo vs flujo, y universo distinto —
spec §1.6).

Unidad = PERSONA elegida 18+. `tiene_ahorros = 1` sse alguna de
`P5_1_1..P5_1_6` (informal) o `P5_6_1..P5_6_9` (formal) vale '1'.
Ponderador `FAC_PER`, diseño `EST_DIS × UPM_DIS`, bootstrap conglomerado
n_boot=10000 seed=42.
"""
import hashlib
import io
import os
import sys
import zipfile

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calibracion_mordida_encig_serie import wprop_ic_conglomerado  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
ZIP = os.path.join(RAW, "enif_2024_bd_csv.zip")
TABLA = "TMODULO.csv"

INFORMAL = [f"P5_1_{i}" for i in range(1, 7)]
FORMAL = [f"P5_6_{i}" for i in range(1, 10)]
TODAS = INFORMAL + FORMAL

P_2005 = 0.174804  # cifra vigente, ENNViH ola 2 -- NO comparable (spec §1.6)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def carga():
    with zipfile.ZipFile(ZIP) as z, z.open(TABLA) as f:
        df = pd.read_csv(io.BytesIO(f.read()), encoding="latin-1",
                         dtype=str, low_memory=False)
    df.columns = [c.strip().strip('"') for c in df.columns]
    faltan = [c for c in TODAS + ["FAC_PER", "EST_DIS", "UPM_DIS", "EDAD_V"]
              if c not in df.columns]
    if faltan:
        raise SystemExit(f"PARO · faltan columnas en {TABLA}: {faltan}")
    for c in TODAS:
        df[c] = df[c].astype(str).str.strip().str.strip('"')

    edad = pd.to_numeric(df["EDAD_V"], errors="coerce")
    if edad.isna().any() or (edad < 18).any():
        raise SystemExit(
            f"PARO · EDAD_V inválida o menor de 18 en "
            f"{int(edad.isna().sum() + (edad < 18).sum())} filas")
    w = pd.to_numeric(df["FAC_PER"], errors="coerce")
    if w.isna().any() or (w <= 0).any():
        raise SystemExit("PARO · FAC_PER no numérico positivo")
    validas = df[TODAS].isin(["1", "2"]).sum(axis=1)
    if (validas == 0).any():
        raise SystemExit(
            f"PARO · {int((validas == 0).sum())} personas con las 15 variables "
            "de la sección 5 en blanco")
    df["_w"] = w
    df["_edad"] = edad
    return df


def estima(df, cols, etiqueta):
    d = df[cols].eq("1").any(axis=1).astype(float)
    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
        d.to_numpy(), df["_w"].to_numpy(),
        df["EST_DIS"].tolist(), df["UPM_DIS"].tolist())
    return {"etiqueta": etiqueta, "p": p, "lo": lo, "hi": hi, "n": n,
            "n_num": int(d.sum()), "n_est": n_est, "n_upm": n_cl,
            "pobl": float(df["_w"].sum())}


def fmt(r):
    return (f"  {r['etiqueta']}\n"
            f"    p̂ = {r['p']:.6f}   IC95 = [{r['lo']:.6f}, {r['hi']:.6f}]\n"
            f"    n = {r['n']:,} personas · con ahorro = {r['n_num']:,}\n"
            f"    estratos = {r['n_est']} · UPM = {r['n_upm']:,} · "
            f"población expandida = {r['pobl']:,.0f}")


def main():
    print("ACTO MAESTRA34-L5 · P4 · tiene_ahorros · ENIF 2024 (re-medición)")
    print(f"payload  : {os.path.basename(ZIP)}")
    print(f"sha256   : {sha256(ZIP)}")
    df = carga()
    print(f"tabla    : {TABLA} · {len(df):,} personas elegidas · "
          f"EDAD_V {int(df['_edad'].min())}-{int(df['_edad'].max())}")
    print()
    print("PRINCIPAL")
    r = estima(df, TODAS, "formal ∪ informal (P5_1_1..6 ∪ P5_6_1..9)")
    print(fmt(r))
    print()
    print("SENSIBILIDADES PRE-DECLARADAS (spec §1.5)")
    print(fmt(estima(df, FORMAL, "A · solo formal (P5_6_1..9)")))
    print(fmt(estima(df, INFORMAL, "B · solo informal (P5_1_1..6)")))
    print()
    print(f"cifra vigente 2005-06 (ENNViH ola 2): {P_2005}")
    print("NO se compara: acervo vs flujo y universos distintos (spec §1.6).")
    print(f"razón aritmética, solo informativa: {r['p'] / P_2005:.4f}")
    return r


# ─────────────────────────────────────────────────────────────────────────────
# ACTO MAESTRA35-L1 · P2 — parámetro de eje. ADITIVO: ni una línea de arriba
# cambia, y `main()` sigue imprimiendo exactamente lo mismo que en MAESTRA34-L5.
# El desenlace de esta pieza NO es el de L5: allí era la unión formal ∪ informal
# (`tiene_ahorros`); aquí es `ahorra_solo_informal`, exclusivo. Spec §3.
# ─────────────────────────────────────────────────────────────────────────────
from ejes_maestra35_l1 import (  # noqa: E402
    ESC_ENIF, FUERA, ORD_EDAD, ORD_ESC, ORD_SEXO, SEXO, Eje, imprime,
    mide_eje, tramos_edad)

CUENTAS = [f"P5_4_{i}" for i in range(1, 10)]

EJES_P2 = [
    Eje("sexo", lambda d: d["SEXO"].map(SEXO).fillna(FUERA), ORD_SEXO, None,
        "el encargo lo mide y no lo predice"),
    Eje("edad", lambda d: tramos_edad(d["EDAD_V"]), ORD_EDAD, None,
        "sin signo pre-registrado en la spec §3.2"),
    Eje("escolaridad", lambda d: d["NIV"].map(ESC_ENIF).fillna(FUERA),
        ORD_ESC, "desc",
        "G3/informal_sin_puente: solo_informal MÁS alto con menor escolaridad"),
    Eje("localidad",
        lambda d: d["TLOC"].map({"1": "15 000 y mas", "2": "15 000 y mas",
                                 "3": "menor de 15 000",
                                 "4": "menor de 15 000"}).fillna(FUERA),
        ["menor de 15 000", "15 000 y mas"], "desc",
        "MÁS alto en localidades menores de 15 000 (corte exacto del FD)"),
    Eje("formalidad",
        lambda d: d["P3_13"].map({k: "sin seguridad social" if k == "7"
                                  else "con seguridad social"
                                  for k in "1234567"}).fillna(FUERA),
        ["sin seguridad social", "con seguridad social"], "desc",
        "MÁS alto sin trabajo formal; cobertura 68.97 % -> universo restringido"),
]

EJE_CUENTA_PRINCIPAL = Eje(
    "cuenta_formal", lambda d: _celda_cuenta(d),
    ["sin cuenta", "con cuenta"], "desc",
    "NO-FALSABLE contra el principal: P5_4_* gatea a P5_6_*, así que sin "
    "cuenta el desenlace se reduce a informal_cualquiera por construcción "
    "del cuestionario (censo §4.4, spec §3.3)",
    tope="DISCRIMINA")
EJE_CUENTA_SECUNDARIO = Eje(
    "cuenta_formal", lambda d: _celda_cuenta(d),
    ["sin cuenta", "con cuenta"], "desc",
    "contra el secundario SÍ es falsable: informal_cualquiera no está anidado "
    "en la tenencia")


def _celda_cuenta(d):
    tiene = d[CUENTAS].eq("1").any(axis=1)
    nunca = d[CUENTAS].isin(["1", "2"]).sum(axis=1).eq(0)
    return pd.Series([FUERA if nn else ("con cuenta" if t else "sin cuenta")
                      for t, nn in zip(tiene, nunca)], index=d.index)


def desenlaces(df):
    """Los dos desenlaces de la pieza P2, spec §3. El blanco por secuencia en
    P5_6_* cuenta como NO haber ahorrado por esa vía -- misma lectura que
    MAESTRA34-L5 P4 §1.3."""
    informal = df[INFORMAL].eq("1").any(axis=1)
    formal = df[FORMAL].eq("1").any(axis=1)
    return {"ahorra_solo_informal (PRINCIPAL)": (informal & ~formal).astype(float),
            "informal_cualquiera (SECUNDARIO)": informal.astype(float)}


def main_ejes():
    print("ACTO MAESTRA35-L1 · P2 · dinero.ahorro.via_informal POR EJES · ENIF 2024")
    print(f"payload  : {os.path.basename(ZIP)}")
    print(f"sha256   : {sha256(ZIP)}")
    df = carga()   # mismo cargador, mismas guardias, mismo universo que L5
    faltan = [c for c in ["SEXO", "NIV", "TLOC", "P3_13"] + CUENTAS
              if c not in df.columns]
    if faltan:
        raise SystemExit(f"PARO · faltan columnas de eje en {TABLA}: {faltan}")
    print(f"tabla    : {TABLA} · {len(df):,} personas elegidas 18+ · "
          f"unidad = PERSONA · ponderador FAC_PER")
    w, est, upm = df["_w"], df["EST_DIS"], df["UPM_DIS"]
    salida = {}
    for etiqueta, d in desenlaces(df).items():
        print("\n" + "=" * 74)
        print(f"DESENLACE {etiqueta}")
        p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
            d.to_numpy(), w.to_numpy(), est.tolist(), upm.tolist())
        print(f"  GLOBAL  p̂ = {p:.6f}  IC95 = [{lo:.6f}, {hi:.6f}]  "
              f"n = {n:,} personas · num = {int(d.sum()):,} · "
              f"estratos = {n_est} · UPM = {n_cl:,}")
        print()
        ejes = list(EJES_P2) + [EJE_CUENTA_PRINCIPAL if "PRINCIPAL" in etiqueta
                                else EJE_CUENTA_SECUNDARIO]
        salida[etiqueta] = [mide_eje(df, e, d, w, est, upm) for e in ejes]
        for r in salida[etiqueta]:
            imprime(r, "personas")
    return salida


if __name__ == "__main__":
    if "--ejes" in sys.argv:
        main_ejes()
    else:
        main()
