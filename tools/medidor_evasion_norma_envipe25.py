#!/usr/bin/env python3
"""ACTO MAESTRA34-L5 · P3 · evasión de norma percibida inútil, ENVIPE 2025.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-02-MAESTRA34-L5-P3-spec.md` (COMMIT-1).

Regla `tramite.evasion_norma` (milpa/tramite.yaml:203-228, clase ASIGNADO,
`evade_norma p=0.66`, probabilidades declaradas NO CALIBRADAS por la regla, que
además pide «no reportar con decimales»).

Unidad = DELITO. Universo = delitos con `BP1_20 ∈ {1,2}`.
`evade_norma = 1 ⟺ BP1_20==2 Y BP1_23 ∈ {04,05,06,08}`.
Ponderador `FAC_DEL`, diseño `EST_DIS × UPM_DIS`, bootstrap conglomerado
n_boot=10000 seed=42, reutilizando `wprop_ic_conglomerado`.

Lo que se estima es la CONJUNTA P(no denunció ∧ razón de norma inútil | enfrentó
la norma), NO la condicional de la regla — spec §1.5.
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
ZIP = os.path.join(RAW, "envipe2025_csv.zip")
TABLA = ("tmod_vic_envipe2025/conjunto_de_datos/"
         "conjunto_de_datos_tmod_vic_envipe2025.csv")

INUTIL = {"04", "05", "06", "08"}   # perdida de tiempo · tramites largos ·
                                    # desconfianza · actitud hostil
EXTORSION = "02"                    # sensibilidad A


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def dos_digitos(s):
    s = str(s).strip().strip('"')
    if s in ("", "b", "B", "nan"):
        return ""
    return s.zfill(2)


def carga():
    with zipfile.ZipFile(ZIP) as z, z.open(TABLA) as f:
        df = pd.read_csv(io.BytesIO(f.read()), encoding="latin-1",
                         dtype=str, low_memory=False)
    df.columns = [c.strip().strip('"') for c in df.columns]
    for c in ("BP1_20", "BP1_23", "FAC_DEL", "EST_DIS", "UPM_DIS", "BPCOD"):
        if c not in df.columns:
            raise SystemExit(f"PARO · falta la columna {c} en {TABLA}")
    df["BP1_20"] = df["BP1_20"].astype(str).str.strip().str.strip('"')
    df["BP1_23n"] = df["BP1_23"].map(dos_digitos)

    fuera = set(df["BP1_20"].unique()) - {"1", "2"}
    if fuera:
        raise SystemExit(f"PARO · BP1_20 con valores fuera de {{1,2}}: {fuera}")
    w = pd.to_numeric(df["FAC_DEL"], errors="coerce")
    if w.isna().any() or (w <= 0).any():
        raise SystemExit(
            f"PARO · FAC_DEL no numérico positivo en "
            f"{int(w.isna().sum() + (w <= 0).sum())} filas")
    if df["EST_DIS"].isna().any() or df["UPM_DIS"].isna().any():
        raise SystemExit("PARO · EST_DIS/UPM_DIS con faltantes")
    df["_w"] = w
    return df


def estima(df, numerador, etiqueta):
    d = ((df["BP1_20"] == "2") & (df["BP1_23n"].isin(numerador))).astype(float)
    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
        d.to_numpy(), df["_w"].to_numpy(),
        df["EST_DIS"].tolist(), df["UPM_DIS"].tolist())
    return {"etiqueta": etiqueta, "p": p, "lo": lo, "hi": hi, "n": n,
            "n_num": int(d.sum()), "n_est": n_est, "n_upm": n_cl,
            "pobl": float(df["_w"].sum())}


def fmt(r):
    return (f"  {r['etiqueta']}\n"
            f"    p̂ = {r['p']:.6f}   IC95 = [{r['lo']:.6f}, {r['hi']:.6f}]\n"
            f"    n = {r['n']:,} delitos · numerador = {r['n_num']:,}\n"
            f"    estratos = {r['n_est']} · UPM = {r['n_upm']:,} · "
            f"población expandida = {r['pobl']:,.0f}")


def main():
    print("ACTO MAESTRA34-L5 · P3 · evasion_norma · ENVIPE 2025")
    print(f"payload  : {os.path.basename(ZIP)}")
    print(f"sha256   : {sha256(ZIP)}")
    df = carga()
    nd = int((df["BP1_20"] == "2").sum())
    print(f"tabla    : tmod_vic · {len(df):,} delitos · "
          f"denunciaron {len(df) - nd:,} · no denunciaron {nd:,}")
    print()
    print("PRINCIPAL")
    r = estima(df, INUTIL, "BP1_20=2 ∧ BP1_23∈{04,05,06,08} · norma inútil o extractiva")
    print(fmt(r))
    print()
    print("SENSIBILIDADES PRE-DECLARADAS (spec §1.7)")
    ra = estima(df, INUTIL | {EXTORSION}, "A · + código 02 (miedo a extorsión)")
    print(fmt(ra))
    bp = pd.to_numeric(df["BPCOD"], errors="coerce")
    sub = df[bp.between(5, 15)].copy()
    rb = estima(sub, INUTIL, "B · universo BPCOD 5..15 (delitos personales)")
    print(fmt(rb))
    print()
    print("LECTURA SECUNDARIA (contexto, no es el estimando de la regla)")
    nod = df[df["BP1_20"] == "2"].copy()
    rc = estima(nod, INUTIL, "composición entre quienes NO denunciaron")
    print(fmt(rc))
    print()
    print("prior ASIGNADO a contrastar: evade_norma = 0.66 "
          "(no calibrado; la regla pide no reportar con decimales)")
    print(f"razón p̂/prior = {r['p'] / 0.66:.4f}")
    return r


if __name__ == "__main__":
    main()
