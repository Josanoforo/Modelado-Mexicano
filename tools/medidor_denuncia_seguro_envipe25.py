#!/usr/bin/env python3
"""ACTO MAESTRA35-L7 · civico.denuncia.sin_seguro / con_seguro · ENVIPE 2025.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-02-MAESTRA35-L7-spec.md` (COMMIT-1).

R7.2 del modelo (canon/modelo-decision-v4_0.md:499): «SI el delito no tiene
cobertura de seguro y el agresor es identificable ENTONCES no denuncia».
El falsador GENERAL de Hito D (comparar cobertura ENTRE clases de delito) ya
tiene veredicto D archivado (hitoD-preregistro Nota 11, 4/ago/2026):
`BP2_1` (cobertura de seguro) es degenerada fuera de `BPCOD=01` (robo de
vehículo) -- 1 028 de 40 280 filas, el 100% de ellas BPCOD=01. Ese veredicto
no se toca aquí. Esta pieza mide la TASA BASE (apparatus B-bis, "regla de
señal" v2.3) DENTRO de BPCOD=01 -- comparación intra-clase, no el cruce
entre clases que Hito D exige y que el instrumento no permite.

Esta misma celda (denuncia por BP2_1, dentro de BPCOD=01) ya fue calculada,
de forma independiente, DOS veces: `hitoD-R7_2-veredicto-v1_0.md §2.4`
(4/ago/2026, primer cómputo) y `hitoD-R7_2-revision-v1_0.md §2` (4/ago/2026,
recálculo independiente sin heredar números). Esta es la TERCERA
reproducción independiente, vía el estimador `wprop_ic_conglomerado` (el
mismo de MAESTRA35-L1/L5) y el apparatus de ejes CORROBORADA/CONTRARIA/
NO-DISCRIMINA (`tools/ejes_maestra35_l1.py`) -- ninguno de los dos
documentos anteriores usaba ese apparatus ni producía una entrada para
`milpa/tramite-ola5-propuesta-v0.yaml`, que es lo que esta pieza añade.

Unidad = DELITO (fila de TMod_Vic, no persona: una persona puede aportar
más de un delito). Ponderador FAC_DEL, diseño EST_DIS×UPM_DIS, bootstrap
conglomerado n_boot=10000 seed=42 (wprop_ic_conglomerado).
"""
import hashlib
import io
import os
import sys
import zipfile

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ejes_maestra35_l1 import Eje, imprime, mide_eje  # noqa: E402
from calibracion_mordida_encig_serie import wprop_ic_conglomerado  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
ZIP = os.path.join(RAW, "envipe2025_csv.zip")
DATOS = "tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv"

CATALOGO_BPCOD = {
    "01": "Robo total de vehículo", "02": "Robo accesorios/refacciones",
    "03": "Vandalismo", "04": "Robo casa habitación",
    "05": "Robo/asalto calle o transporte", "06": "Robo otra forma",
    "07": "Fraude bancario", "08": "Fraude al consumidor", "09": "Extorsión",
    "10": "Amenazas", "11": "Golpes/lesión por agresión", "12": "Secuestro",
    "13": "Hostigamiento/intimidación sexual", "14": "Violación sexual",
    "15": "Otros delitos",
}

EJE_SEGURO = Eje(
    "cobertura_seguro", lambda d: d["BP2_1"].map({"2": "no asegurado",
                                                    "1": "asegurado"}),
    ["no asegurado", "asegurado"], "asc",
    "regla R7.2, línea 179 del modelo: 'SI es robo de vehículo asegurado "
    "ENTONCES sí denuncia' -- signo esperado: asegurado > no asegurado")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def carga():
    with zipfile.ZipFile(ZIP) as z, z.open(DATOS) as f:
        df = pd.read_csv(io.BytesIO(f.read()), encoding="latin-1",
                          dtype=str, low_memory=False)
    faltan = [c for c in ["BPCOD", "BP2_1", "BP1_20", "FAC_DEL", "EST_DIS",
                           "UPM_DIS"] if c not in df.columns]
    if faltan:
        raise SystemExit(f"PARO · faltan columnas en {DATOS}: {faltan}")
    for c in ["BPCOD", "BP2_1", "BP1_20"]:
        df[c] = df[c].astype(str).str.strip().str.strip('"')
    w = pd.to_numeric(df["FAC_DEL"], errors="coerce")
    if w.isna().any() or (w <= 0).any():
        raise SystemExit("PARO · FAC_DEL no numérico positivo")
    df["_w"] = w
    return df


def guardias(df):
    """Guardias de cobertura/degeneración -- verificadas ANTES de estimar
    nada (lección feedback_spec_congelada_puede_salir_degenerada: cobertura
    del universo es la guardia que atrapa, no el rango de p)."""
    v01 = df[df["BPCOD"] == "01"]
    fuera = df[df["BPCOD"] != "01"]
    # BP2_1 ya pasó por carga() (astype(str)), así que un blanco real llega
    # aquí como la CADENA "nan", no como NaN -- verificado empíricamente
    # (spec_congelada: no asumir cómo se marca el blanco, censarlo).
    n_fuera_novacio = int((~fuera["BP2_1"].isin(["", "nan"])).sum())
    if n_fuera_novacio != 0:
        raise SystemExit(
            f"PARO · {n_fuera_novacio} filas con BP2_1 no-blanco fuera de "
            "BPCOD=01 -- la premisa censada (degeneración estructural) no "
            "se sostiene contra este CSV")
    n_bp1_20_valido = int(v01["BP1_20"].isin(["1", "2"]).sum())
    if n_bp1_20_valido != len(v01):
        raise SystemExit(
            f"PARO · BP1_20 solo válido en {n_bp1_20_valido} de {len(v01)} "
            "filas de BPCOD=01 -- universo incompleto")
    n_bp2_1_valido = int(v01["BP2_1"].isin(["1", "2", "9"]).sum())
    if n_bp2_1_valido != len(v01):
        raise SystemExit(
            f"PARO · BP2_1 fuera de {{1,2,9}} en "
            f"{len(v01) - n_bp2_1_valido} filas de BPCOD=01")


def censo_denominador_por_delito(df):
    """P0 -- denominador de denuncia por tipo de delito, las 15 clases.
    Contexto declarado, NO es la prueba del falsador (§2.6 de
    hitoD-R7_2-veredicto): cobertura de seguro no varía entre clases."""
    filas = []
    for cod in sorted(df["BPCOD"].unique()):
        sub = df[df["BPCOD"] == cod]
        d = (sub["BP1_20"] == "1").astype(float)
        p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
            d.to_numpy(), sub["_w"].to_numpy(),
            sub["EST_DIS"].tolist(), sub["UPM_DIS"].tolist())
        con_seguro = int((sub["BP2_1"] == "1").sum())
        filas.append({"bpcod": cod, "delito": CATALOGO_BPCOD.get(cod, "?"),
                       "n": n, "p_denuncia": p, "lo": lo, "hi": hi,
                       "n_con_bp2_1_valido": con_seguro})
    return filas


def main():
    print("ACTO MAESTRA35-L7 · civico.denuncia · ENVIPE 2025")
    print(f"payload  : {os.path.basename(ZIP)}")
    print(f"sha256   : {sha256(ZIP)}")
    df = carga()
    print(f"tabla    : {DATOS} · {len(df):,} filas (delito) · unidad = DELITO")
    guardias(df)
    print()

    print("=" * 78)
    print("CENSO P0 -- denominador de denuncia por tipo de delito (BPCOD)")
    print("=" * 78)
    for r in censo_denominador_por_delito(df):
        print(f"  {r['bpcod']} {r['delito']:<38s} n={r['n']:>6,}  "
              f"p_denuncia={r['p_denuncia']:.4f}  IC95=[{r['lo']:.4f},{r['hi']:.4f}]  "
              f"BP2_1 válido={r['n_con_bp2_1_valido']}")
    print()
    print("BP2_1 (cobertura de seguro) válido por BPCOD -- confirma degeneración D:")
    for cod, sub in df.groupby("BPCOD"):
        vc = sub["BP2_1"].value_counts(dropna=False).to_dict()
        print(f"  {cod}: {vc}")
    print()

    print("=" * 78)
    print("MEDICIÓN -- dentro de BPCOD=01 (robo de vehículo), único universo "
          "donde BP2_1 tiene masa")
    print("=" * 78)
    universo = df[(df["BPCOD"] == "01") & (df["BP2_1"].isin(["1", "2"]))].copy()
    excluidos_9 = int((df[df["BPCOD"] == "01"]["BP2_1"] == "9").sum())
    print(f"universo : BPCOD='01' ∧ BP2_1∈{{1,2}} · n={len(universo):,} "
          f"(excluidos BP2_1='9' no especificado: {excluidos_9})")
    d = (universo["BP1_20"] == "1").astype(float)
    w, est, upm = universo["_w"], universo["EST_DIS"], universo["UPM_DIS"]

    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
        d.to_numpy(), w.to_numpy(), est.tolist(), upm.tolist())
    print(f"  GLOBAL (BPCOD=01)  p̂ = {p:.6f}  IC95 = [{lo:.6f}, {hi:.6f}]  "
          f"n = {n:,} · num = {int(d.sum()):,} · estratos = {n_est} · UPM = {n_cl:,}")
    print()

    r = mide_eje(universo, EJE_SEGURO, d, w, est, upm)
    imprime(r, "delitos")

    print("CONTROL DE REGRESIÓN contra hitoD-R7_2-veredicto/revisión "
          "(4/ago/2026, ya publicados, no heredados aquí):")
    print("  esperado  asegurado=79.1%  no_asegurado=67.2%  brecha=11.9pp")
    obt_aseg = next(c for c in r["celdas"] if c["celda"] == "asegurado")["p"]
    obt_noaseg = next(c for c in r["celdas"] if c["celda"] == "no asegurado")["p"]
    print(f"  obtenido  asegurado={obt_aseg*100:.1f}%  "
          f"no_asegurado={obt_noaseg*100:.1f}%  "
          f"brecha={(obt_aseg-obt_noaseg)*100:.1f}pp")
    return {"censo": censo_denominador_por_delito(df), "eje": r,
            "universo_n": len(universo)}


if __name__ == "__main__":
    main()
