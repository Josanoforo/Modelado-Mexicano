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


if __name__ == "__main__":
    main()
