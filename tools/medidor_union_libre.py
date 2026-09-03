#!/usr/bin/env python3
"""ACTO MAESTRA35-L7 · familia.union.baja_garantia_institucional (R5.3).

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-02-MAESTRA35-L7-spec.md` (COMMIT-1).

R5.3 del modelo (canon/modelo-decision-v4_0.md:537): «SI hay baja garantía
institucional del matrimonio ENTONCES la unión libre es opción racional».
R5.3 NO tiene ficha de Hito D archivada (censado: `grep -rl "R5_3"
forense/` → 0 hits, a diferencia de R5.2/R1.1/R7.2). El disparador «baja
garantía institucional» no está medido en ningún instrumento del corpus:
esta pieza mide la TASA BASE de unión libre con ejes (apparatus B-bis,
"regla de señal" v2.3), no la condicional causal.

Dos desenlaces, dos instrumentos, NO promediados entre sí (son preguntas
distintas, ninguna sustituye a la otra):

  D1 · EDER 2017 -- tipo de PRIMERA unión (retrospectivo, panel de vida).
       `edo_civil1` (historiavida.csv), primer código no-cero por persona en
       orden de `anio_retro`. Catálogo completo verificado contra el FD
       (`eder2017_fd.pdf`, "Descripción de la base de datos", catálogo de
       `edo_civil1`): {1,12,13,14,17,18,126} = unión libre (inicio, o
       transición posterior a inicio de unión libre); {2,3,4,26,27,28,46,
       47,48} = matrimonio directo (civil/religioso/ambos, inicio o
       transición). Códigos {6,7,8,60,70,80} (divorcio/separación/viudez)
       NUNCA aparecen como primer-no-cero (verificado: 0 casos) -- sin
       censura izquierda que corrija. Código 37 (n=2) queda sin clasificar,
       declarado, no forzado.
       Eje: cohorte de nacimiento (`anio_nac`), 4 tramos.
  D2 · ENADID 2023 -- situación conyugal ACTUAL (transversal). `p3_27_ag`
       (TSDEM.csv), condicional a estar actualmente casado(a) O en unión
       libre (código 2 o 3) -- se excluye soltero/separado/divorciado/viudo
       del denominador porque la regla compara las DOS formas
       institucionales alternativas, no la población general (que incluye
       a quien nunca formó pareja). La prevalencia SIN condicionar
       (19.05% sobre 15+ completo) se declara en el censo como cifra
       adicional, no como el desenlace medido.
       Eje: tramos de edad (`tramos_edad`, `ejes_maestra35_l1` -- proxy
       imperfecto de cohorte: ENADID no trae año de nacimiento en TSDEM;
       edad transversal mezcla efecto-cohorte con efecto-etapa-de-vida,
       declarado, no corregido).
"""
import os
import sys
import zipfile

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ejes_maestra35_l1 import Eje, FUERA, imprime, mide_eje, tramos_edad  # noqa: E402
from calibracion_mordida_encig_serie import sha256, wprop_ic_conglomerado  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")
ZIP_EDER = os.path.join(RAW, "eder2017", "eder2017_bases_csv.zip")
ZIP_ENADID = os.path.join(RAW, "base_datos_enadid23_csv.zip")

LIBRE = {"1", "12", "13", "14", "17", "18", "126"}
DIRECTO = {"2", "3", "4", "26", "27", "28", "46", "47", "48"}


def tramos_cohorte(serie):
    a = pd.to_numeric(serie, errors="coerce")
    out = pd.Series(FUERA, index=serie.index, dtype=object)
    out[(a >= 1961) & (a <= 1970)] = "1961-1970"
    out[(a >= 1971) & (a <= 1980)] = "1971-1980"
    out[(a >= 1981) & (a <= 1990)] = "1981-1990"
    out[(a >= 1991)] = "1991+"
    return out


EJE_COHORTE = Eje(
    "cohorte_nacimiento", lambda d: tramos_cohorte(d["anio_nac"]),
    ["1961-1970", "1971-1980", "1981-1990", "1991+"], "asc",
    "baja garantía institucional del matrimonio es más reciente/creciente "
    "-> cohortes más jóvenes, más unión libre como primera unión")

EJE_EDAD = Eje(
    "tramo_edad", lambda d: tramos_edad(d["edad"]),
    ["18-29", "30-44", "45-59", "60+"], "desc",
    "proxy de cohorte (ENADID no trae año de nacimiento): más jóvenes, más "
    "unión libre -> p baja con la edad")


def carga_eder():
    """EDER 2017: primer estado civil no-cero por persona, con sus ejes."""
    with zipfile.ZipFile(ZIP_EDER) as z:
        hv = pd.read_csv(z.open("historiavida.csv"), dtype=str,
                          encoding="utf-8-sig", low_memory=False,
                          usecols=["folioviv", "foliohog", "id_pobla",
                                    "anio_retro", "anio_nac", "edo_civil1"])
        ant = pd.read_csv(z.open("antecedentes.csv"), dtype=str,
                           encoding="utf-8-sig",
                           usecols=["folioviv", "foliohog", "id_pobla",
                                     "factor_per"])
        per = pd.read_csv(z.open("persona.csv"), dtype=str,
                           encoding="utf-8-sig",
                           usecols=["folioviv", "foliohog", "id_pobla",
                                     "nivel_inst"])
        viv = pd.read_csv(z.open("vivienda.csv"), dtype=str,
                           encoding="utf-8-sig",
                           usecols=["folioviv", "tam_loc", "est_dis", "upm"])

    llave3 = ["folioviv", "foliohog", "id_pobla"]
    hv["_anio_retro_n"] = pd.to_numeric(hv["anio_retro"], errors="coerce")
    hv = hv.sort_values(llave3 + ["_anio_retro_n"])
    nocero = hv[hv["edo_civil1"].astype(str) != "0"]
    primero = nocero.groupby(llave3, as_index=False).first()

    censurados = primero[primero["edo_civil1"].isin(
        {"6", "7", "8", "60", "70", "80"})]
    if len(censurados):
        raise SystemExit(
            f"PARO · {len(censurados)} personas con primer-no-cero en "
            "{6,7,8,60,70,80} -- posible censura izquierda no contemplada "
            "en la spec")

    n0 = len(primero)
    m = primero.merge(ant, on=llave3, how="left")
    if m["factor_per"].isna().sum():
        raise SystemExit(
            f"PARO · {int(m['factor_per'].isna().sum())} huérfanos en join "
            "con antecedentes.csv")
    m = m.merge(viv, on="folioviv", how="left")
    if m["est_dis"].isna().sum() or m["upm"].isna().sum():
        raise SystemExit("PARO · huérfanos en join con vivienda.csv")
    assert len(m) == n0, "el join cambió el número de filas"

    m["tipo1"] = m["edo_civil1"].map(
        lambda c: "union_libre" if c in LIBRE
        else ("matrimonio_directo" if c in DIRECTO else None))
    return m


def carga_enadid():
    with zipfile.ZipFile(ZIP_ENADID) as z:
        cols = ["edad", "sexo", "p3_27_ag", "est_dis", "upm_dis", "fac_viv"]
        df = pd.read_csv(z.open("TSDEM.csv"), dtype=str,
                          encoding="utf-8-sig", low_memory=False,
                          usecols=lambda c: c.lower() in cols)
    df.columns = [c.lower() for c in df.columns]
    return df


def main():
    print("ACTO MAESTRA35-L7 · familia.union.libre · EDER 2017 + ENADID 2023")
    print()

    # ---------------------------------------------------------------- EDER
    print("=" * 78)
    print(f"D1 · EDER 2017 (payload eder_2017_eder2017_bases_csv)")
    print(f"sha256   : {sha256(ZIP_EDER)}")
    m = carga_eder()
    print(f"personas con primer estado civil no-cero: {len(m):,}")
    print(m["edo_civil1"].where(
        m["edo_civil1"].isin(LIBRE | DIRECTO), "OTRO").value_counts())
    sin_clasificar = int((m["tipo1"].isna()).sum())
    print(f"sin clasificar (código ambiguo, declarado no forzado): "
          f"{sin_clasificar}")
    universo = m[m["tipo1"].notna()].copy()
    d = (universo["tipo1"] == "union_libre").astype(float)
    w = pd.to_numeric(universo["factor_per"])
    est, upm = universo["est_dis"], universo["upm"]
    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
        d.to_numpy(), w.to_numpy(), est.tolist(), upm.tolist())
    print(f"  GLOBAL  p̂(unión libre como 1a unión) = {p:.6f}  "
          f"IC95 = [{lo:.6f}, {hi:.6f}]  n = {n:,}")
    print()
    r_eder = mide_eje(universo, EJE_COHORTE, d, w, est, upm)
    imprime(r_eder, "personas")

    # -------------------------------------------------------------- ENADID
    print("=" * 78)
    print(f"D2 · ENADID 2023 (payload enadid2023_base_datos_csv)")
    print(f"sha256   : {sha256(ZIP_ENADID)}")
    e = carga_enadid()
    e15 = e[pd.to_numeric(e["edad"], errors="coerce") >= 15].copy()
    print(f"universo 15+: {len(e15):,}")
    print("p3_27_ag value_counts (15+):")
    print(e15["p3_27_ag"].value_counts(dropna=False))
    w_all = pd.to_numeric(e15["fac_viv"])
    p_bruta = (w_all * (e15["p3_27_ag"] == "3").astype(float)).sum() / w_all.sum()
    print(f"  prevalencia BRUTA (sobre 15+ completo, no condicionada, "
          f"CENSO no desenlace formal): {p_bruta:.6f}")
    print()

    pareja = e15[e15["p3_27_ag"].isin(["2", "3"])].copy()
    print(f"universo condicional (casada(o) o unión libre): {len(pareja):,}")
    d2 = (pareja["p3_27_ag"] == "3").astype(float)
    w2 = pd.to_numeric(pareja["fac_viv"])
    est2, upm2 = pareja["est_dis"], pareja["upm_dis"]
    p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
        d2.to_numpy(), w2.to_numpy(), est2.tolist(), upm2.tolist())
    print(f"  GLOBAL  p̂(unión libre | pareja) = {p:.6f}  "
          f"IC95 = [{lo:.6f}, {hi:.6f}]  n = {n:,}")
    print()
    r_enadid = mide_eje(pareja, EJE_EDAD, d2, w2, est2, upm2)
    imprime(r_enadid, "personas")

    return {"eder": r_eder, "enadid": r_enadid, "enadid_prevalencia_bruta": p_bruta}


if __name__ == "__main__":
    main()
