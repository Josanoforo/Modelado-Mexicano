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


# ─────────────────────────────────────────────────────────────────────────────
# ACTO MAESTRA35-L1 · P4 — parámetro de eje. ADITIVO: ni una línea de arriba
# cambia y `main()` sigue imprimiendo lo mismo que en MAESTRA34-L5. El
# estimando NO se toca: evade_norma = BP1_20=='2' ∧ BP1_23 ∈ {04,05,06,08},
# la CONJUNTA, unidad DELITO, FAC_DEL. Spec §5.
# ─────────────────────────────────────────────────────────────────────────────
from ejes_maestra35_l1 import (  # noqa: E402
    ESC_2DIG, FUERA, ORD_EDAD, ORD_ESC, ORD_SEXO, SEXO, Eje, imprime,
    mide_eje, tramos_edad)

T_SDEM = ("tsdem_envipe2025/conjunto_de_datos/"
          "conjunto_de_datos_tsdem_envipe2025.csv")
ORD_DOMINIO = ["Rural", "Complemento urbano", "Urbano"]

EJES_P4 = [
    Eje("sexo", lambda d: d["SEXO"].map(SEXO).fillna(FUERA), ORD_SEXO, None,
        "sin signo predicho"),
    Eje("edad", lambda d: tramos_edad(d["EDAD"]), ORD_EDAD, None,
        "el encargo lo dice: tramos de edad sin predicción"),
    Eje("escolaridad_proxy", lambda d: d["_NIV"].map(ESC_2DIG).fillna(FUERA),
        ORD_ESC, None,
        "PROXY de formalidad laboral, que no existe en ENVIPE 2025. La regla "
        "NO predice signo: subsistencia y cinismo empujan en sentidos "
        "opuestos. Veredicto máximo posible: DISCRIMINA"),
    Eje("dominio_urbano_rural",
        lambda d: d["DOMINIO"].map({"U": "Urbano", "C": "Complemento urbano",
                                    "R": "Rural"}).fillna(FUERA),
        ORD_DOMINIO, None,
        "eje PROPIO Y DISTINTO, no el corte de 15 000 que el encargo pedía: "
        "ENVIPE no publica umbral alguno, y R ↔ «menor de 15 000» NO está "
        "verificado en ninguna fuente del payload"),
]


def carga_personas():
    """Tabla de persona de ENVIPE 2025 y la llave delito -> persona que el
    censo P0 declaró: ID_PER. PARA si la llave falla."""
    with zipfile.ZipFile(ZIP) as z, z.open(T_SDEM) as f:
        sd = pd.read_csv(io.BytesIO(f.read()), encoding="latin-1",
                         dtype=str, low_memory=False)
    sd.columns = [c.strip().strip('"') for c in sd.columns]
    for c in ("ID_PER", "NIV"):
        if c not in sd.columns:
            raise SystemExit(f"PARO · falta la columna {c} en tsdem")
        sd[c] = sd[c].astype(str).str.strip().str.strip('"')
    if sd["ID_PER"].nunique() != len(sd):
        raise SystemExit(
            f"PARO · ID_PER no es llave única en tsdem: "
            f"{sd['ID_PER'].nunique():,} para {len(sd):,} filas.")
    return sd.set_index("ID_PER")


def main_ejes():
    print("ACTO MAESTRA35-L1 · P4 · evasion_norma POR EJES · ENVIPE 2025")
    print(f"payload  : {os.path.basename(ZIP)}")
    print(f"sha256   : {sha256(ZIP)}")
    df = carga()
    for c in ("ID_PER", "SEXO", "EDAD", "DOMINIO"):
        if c not in df.columns:
            raise SystemExit(f"PARO · falta la columna de eje {c} en tmod_vic")
        df[c] = df[c].astype(str).str.strip().str.strip('"')
    per = carga_personas()
    huerf = int((~df["ID_PER"].isin(per.index)).sum())
    if huerf:
        raise SystemExit(
            f"PARO · {huerf:,} delitos sin persona en tsdem: la llave del "
            f"censo P0 dejó de valer.")
    df["_NIV"] = df["ID_PER"].map(per["NIV"])
    d = ((df["BP1_20"] == "2") & (df["BP1_23n"].isin(INUTIL))).astype(float)
    print(f"tabla    : tmod_vic · universo BP1_20 ∈ {{1,2}} · n = {len(df):,} "
          f"· UNIDAD = DELITO (no persona) · ponderador FAC_DEL")
    print(f"llave    : ID_PER (tmod_vic -> tsdem) · 0 huérfanos")
    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
        d.to_numpy(), df["_w"].to_numpy(),
        df["EST_DIS"].tolist(), df["UPM_DIS"].tolist())
    print(f"\n  GLOBAL  p̂ = {p:.6f}  IC95 = [{lo:.6f}, {hi:.6f}]  "
          f"n = {n:,} delitos · num = {int(d.sum()):,} · "
          f"estratos = {n_est} · UPM = {n_cl:,}\n")
    salida = [mide_eje(df, e, d, df["_w"], df["EST_DIS"], df["UPM_DIS"])
              for e in EJES_P4]
    for r in salida:
        imprime(r, "delitos")
    print("  ejes AUSENTES en esta fuente, declarados por el censo P0 y no")
    print("  sustituidos: formalidad laboral (ni el FD ni el cuestionario")
    print("  principal traen ítem de prestaciones o seguridad social) y")
    print("  tamaño de localidad al corte de 15 000 (ENVIPE no publica TLOC")
    print("  ni umbral alguno en 6 diccionarios ni en su FD).")
    return salida


if __name__ == "__main__":
    if "--ejes" in sys.argv:
        main_ejes()
    else:
        main()
