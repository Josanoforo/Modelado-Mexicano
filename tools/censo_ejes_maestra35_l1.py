#!/usr/bin/env python3
"""ACTO MAESTRA35-L1 · P0 · CENSO A.4 de ejes de segmentacion.

Censa, ANTES de medir y SIN cruzar jamas contra el desenlace, lo que el
encargo (`forense/encargos/2026-09-02-MAESTRA35-L1-RECORRE-Y-SEGMENTA.md`)
pide en su punto P0:

  (i)   P1 · si `encig2025_05_sec_8.csv` trae `NT_TIPO` y cual es la llave real
        entre `sec_7` (evento de tramite) y `sec_8`.
  (ii)  P3 · tabla de persona de ENCIG 2025 y llave que liga `ID_TRA` con ella.
  (iii) P4 · tabla de persona de ENVIPE 2025 y llave delito -> persona.
  (iv)  P2-P4 · para cada eje candidato: el item, sus codigos y su denominador
        dentro del universo de la pieza.

Este script SOLO CUENTA marginales de ejes y verifica llaves. No calcula
ninguna proporcion del desenlace, no toca `P8_4` mas alla de definir el
universo, y no tabula ningun eje contra ningun desenlace: eso es el objeto de
los commits posteriores, contra la spec congelada.

Los codigos de cada eje NO se infieren del nombre de la variable: salen del FD
o del catalogo del propio payload, citados en la nota del P0.

Uso: python3 tools/censo_ejes_maestra35_l1.py
"""
import hashlib
import io
import os
import sys
import zipfile

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calibracion_mordida_encig_serie import leer_csv_cr  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "data", "raw")

Z_ENCIG = os.path.join(RAW, "encig25_base_datos_csv.zip")
Z_ENIF = os.path.join(RAW, "enif_2024_bd_csv.zip")
Z_ENVIPE = os.path.join(RAW, "envipe2025_csv.zip")

T_ENVIPE_MOD = ("tmod_vic_envipe2025/conjunto_de_datos/"
                "conjunto_de_datos_tmod_vic_envipe2025.csv")
T_ENVIPE_SDEM = ("tsdem_envipe2025/conjunto_de_datos/"
                 "conjunto_de_datos_tsdem_envipe2025.csv")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def lee_zip_csv(zpath, member, encoding="latin-1"):
    with zipfile.ZipFile(zpath) as z, z.open(member) as f:
        df = pd.read_csv(io.BytesIO(f.read()), encoding=encoding,
                         dtype=str, low_memory=False)
    df.columns = [c.strip().strip('"') for c in df.columns]
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.strip('"')
    return df


def lee_encig(member):
    df = leer_csv_cr(Z_ENCIG, member, encoding="utf-8")
    df.columns = [c.strip().strip('"') for c in df.columns]
    for c in df.columns:
        df[c] = df[c].astype(str).str.strip().str.strip('"')
    return df


def tramos_edad(serie):
    e = pd.to_numeric(serie, errors="coerce")
    out = pd.Series("(fuera/no especificada)", index=serie.index, dtype=object)
    out[(e >= 18) & (e <= 29)] = "18-29"
    out[(e >= 30) & (e <= 44)] = "30-44"
    out[(e >= 45) & (e <= 59)] = "45-59"
    out[(e >= 60) & (e <= 96)] = "60+"
    return out


# Escolaridad. Los tres payloads usan `NIV` con codificaciones DISTINTAS,
# verificadas cada una contra su propio FD/catalogo (ver nota del P0):
#   ENCIG 2025 (FD, 1 digito): 4=carrera tecnica c/secundaria, 5=normal basica
#   ENVIPE 2025 (catalogo niv.csv, 2 digitos): 04=carrera tecnica, 05=normal
#   ENIF 2024 (FD xlsx, 2 digitos): 04=NORMAL BASICA, 05=estudios tecnicos
#     -> ENIF INVIERTE 04/05 respecto de las otras dos; agrupadas al mismo
#        tramo "media superior", la inversion no altera el tramo, pero
#        cualquier uso a nivel de codigo suelto si se veria afectado.
ESC_ENCIG = {"0": "hasta primaria", "1": "hasta primaria", "2": "hasta primaria",
             "3": "secundaria",
             "4": "media superior", "5": "media superior",
             "6": "media superior", "7": "media superior",
             "8": "superior", "9": "superior"}
ESC_ENVIPE = {"00": "hasta primaria", "01": "hasta primaria",
              "02": "hasta primaria", "03": "secundaria",
              "04": "media superior", "05": "media superior",
              "06": "media superior", "07": "media superior",
              "08": "superior", "09": "superior"}
ESC_ENIF = dict(ESC_ENVIPE)
ESC_ENIF.update({"10": "superior", "11": "superior"})  # ENIF separa mtria/dr


def marginal(df, nombre, serie, validos=None):
    """Imprime el marginal del eje y devuelve (cobertura, n_valido, n_total)."""
    vc = serie.value_counts(dropna=False)
    n = len(serie)
    if validos is None:
        validos = [k for k in vc.index if not str(k).startswith("(")]
    nv = int(sum(vc.get(k, 0) for k in validos))
    print(f"    eje {nombre}: cobertura {nv:,}/{n:,} = {nv / n:.4%}")
    for k in sorted(vc.index, key=lambda x: str(x)):
        marca = " " if k in validos else "*"
        print(f"      {marca} {str(k):<26s} {int(vc[k]):>8,}  "
              f"({vc[k] / n:6.2%})")
    return nv / n, nv, n


def sec_encig():
    print("=" * 78)
    print("ENCIG 2025 · payload encig25_base_datos_csv.zip")
    print(f"  sha256 {sha256(Z_ENCIG)}")
    s7 = lee_encig("encig2025_04_sec_7.csv")
    s8 = lee_encig("encig2025_05_sec_8.csv")
    res = lee_encig("encig2025_02_residentes_sec_2.csv")
    a = lee_encig("encig2025_01_sec1_A_3_4_5_8_9_10.csv")

    print("\n  (i) LLAVE sec_7 x sec_8 — la pregunta que el encargo hace")
    print(f"    sec_8 trae NT_TIPO: {'NT_TIPO' in s8.columns}")
    print(f"    sec_7: {len(s7):,} filas · ID_TRA distintos {s7.ID_TRA.nunique():,}"
          f" · (ID_TRA,NT_TIPO) grupos {s7.groupby(['ID_TRA','NT_TIPO']).ngroups:,}")
    print(f"    sec_8: {len(s8):,} filas · ID_TRA distintos {s8.ID_TRA.nunique():,}"
          f" · ID_TRA es llave unica: {s8.ID_TRA.nunique() == len(s8)}")
    print(f"    ID_PER en sec_8: {s8.ID_PER.nunique():,} · N_TRA distintos: "
          f"{s8.N_TRA.nunique()} · {s8.ID_PER.nunique()} x {s8.N_TRA.nunique()}"
          f" = {s8.ID_PER.nunique() * s8.N_TRA.nunique():,}")
    huerf = len(set(s7.ID_TRA) - set(s8.ID_TRA))
    print(f"    ID_TRA de sec_7 sin fila en sec_8 (huerfanos): {huerf:,}")

    s8v = s8[s8.P8_4.isin(["0", "1"])]
    m = s7.merge(s8v[["ID_TRA"]], on="ID_TRA", how="inner")
    print(f"    universo P8_4 in {{0,1}}: {len(s8v):,} filas de sec_8; al bajar"
          f" a evento de sec_7 -> {len(m):,} eventos en "
          f"{m.ID_TRA.nunique():,} ID_TRA")
    print(f"    eventos que una deduplicacion por ID_TRA descartaria: "
          f"{len(m) - m.ID_TRA.nunique():,}")
    rep = m.groupby("ID_TRA").size()
    rep = rep[rep > 1]
    print(f"    ID_TRA con mas de un evento: {len(rep):,}")
    dis = m[m.ID_TRA.isin(rep.index)].groupby("ID_TRA").P7_3.nunique()
    print(f"    ...de esos, con P7_3 distinto entre sus eventos: "
          f"{int((dis > 1).sum()):,}")
    print(f"    valores de P7_3 en sec_7: "
          f"{sorted(s7.P7_3.unique())}")

    print("\n  (ii) TABLA DE PERSONA y llave tramite -> persona")
    print(f"    residentes_sec_2: {len(res):,} filas · ID_PER llave unica: "
          f"{res.ID_PER.nunique() == len(res)} · ID_VIV {res.ID_VIV.nunique():,}")
    inf = set(a.ID_PER)
    print(f"    informantes (sec1_A): {len(inf):,} · presentes en residentes: "
          f"{len(inf & set(res.ID_PER)):,}")
    print(f"    ID_PER de sec_7 presentes en residentes: "
          f"{len(set(s7.ID_PER) - set(res.ID_PER))} ausentes de "
          f"{s7.ID_PER.nunique():,}")
    print("    -> llave declarada: ID_TRA --(sec_7)--> ID_PER --> residentes")

    per = res[res.ID_PER.isin(inf)].set_index("ID_PER")

    for etiq, sub in (
            ("P1 · universo P8_4 in {0,1} y P7_3 valido",
             m[m.P7_3.isin(["1", "2", "3", "4", "5", "6"])]),
            ("P3 · universo N_TRA='01' y P7_3 en {1,2,4,5,6}",
             s7[(s7.N_TRA == "01")
                & (s7.P7_3.isin(["1", "2", "4", "5", "6"]))])):
        print(f"\n  (iv) EJES en el universo de {etiq}")
        print(f"    n del universo (eventos de tramite): {len(sub):,} · "
              f"personas distintas: {sub.ID_PER.nunique():,}")
        idx = sub.ID_PER.map(lambda p: p)
        marginal(sub, "sexo (residentes.SEXO)", idx.map(per.SEXO).fillna("(sin fila)"),
                 ["1", "2"])
        marginal(sub, "edad (residentes.EDAD)",
                 tramos_edad(idx.map(per.EDAD)),
                 ["18-29", "30-44", "45-59", "60+"])
        marginal(sub, "escolaridad (residentes.NIV)",
                 idx.map(per.NIV).map(ESC_ENCIG).fillna("(fuera: blanco/no cod)"),
                 ["hasta primaria", "secundaria", "media superior", "superior"])
        print("    eje tamano de localidad : NO-ENCONTRADO — el universo de "
              "ENCIG es ciudades de 100 mil habitantes o mas (FD, pag. 1); "
              f"NOM_AREAM tiene {sub.ID_PER.map(per.NOM_AREAM).nunique()} "
              "areas, ninguna menor de 100 mil.")
        print("    eje formalidad laboral  : NO-ENCONTRADO — la tabla de "
              "residentes cierra en POS (posicion en la ocupacion); el FD no "
              "trae item de prestaciones ni de seguridad social por el trabajo.")
    return s7, s8, res


def sec_enif():
    print("\n" + "=" * 78)
    print("ENIF 2024 · payload enif_2024_bd_csv.zip")
    print(f"  sha256 {sha256(Z_ENIF)}")
    tm = lee_zip_csv(Z_ENIF, "TMODULO.csv")
    print(f"  TMODULO: {len(tm):,} filas x {len(tm.columns)} columnas · "
          f"LLAVEMOD unica: {tm.LLAVEMOD.nunique() == len(tm)}")
    e = pd.to_numeric(tm.EDAD_V, errors="coerce")
    print(f"  EDAD_V: {int(e.min())}-{int(e.max())} · menores de 18: "
          f"{int((e < 18).sum())}")
    print("  -> los cinco ejes viven en la MISMA tabla; no hace falta llave.")
    print("\n  (iv) EJES en el universo de P2 (las personas elegidas de TMODULO)")
    marginal(tm, "sexo (SEXO)", tm.SEXO, ["1", "2"])
    marginal(tm, "edad (EDAD_V)", tramos_edad(tm.EDAD_V),
             ["18-29", "30-44", "45-59", "60+"])
    marginal(tm, "escolaridad (NIV)",
             tm.NIV.map(ESC_ENIF).fillna("(fuera: 99 no sabe / blanco)"),
             ["hasta primaria", "secundaria", "media superior", "superior"])
    marginal(tm, "tamano de localidad (TLOC)",
             tm.TLOC.map({"1": "15 000 y mas", "2": "15 000 y mas",
                          "3": "menor de 15 000", "4": "menor de 15 000"})
             .fillna("(fuera)"),
             ["15 000 y mas", "menor de 15 000"])
    marginal(tm, "formalidad laboral (P3_13)",
             tm.P3_13.map({"1": "con seguridad social", "2": "con seguridad social",
                           "3": "con seguridad social", "4": "con seguridad social",
                           "5": "con seguridad social", "6": "con seguridad social",
                           "7": "sin seguridad social"})
             .fillna("(fuera: 9 no sabe / b blanco por secuencia)"),
             ["con seguridad social", "sin seguridad social"])
    cta = [f"P5_4_{i}" for i in range(1, 10)]
    falta = [c for c in cta if c not in tm.columns]
    if falta:
        print(f"    PARO · faltan columnas de tenencia de cuenta: {falta}")
    else:
        tiene = tm[cta].eq("1").any(axis=1)
        nunca = tm[cta].isin(["1", "2"]).sum(axis=1).eq(0)
        marginal(tm, "tenencia de cuenta formal (P5_4_1..9)",
                 pd.Series(["(fuera: nunca preguntada)" if nn else
                            ("con cuenta" if t else "sin cuenta")
                            for t, nn in zip(tiene, nunca)], index=tm.index),
                 ["con cuenta", "sin cuenta"])
        print("      NOTA ANIDAMIENTO (hallazgo del P0): P5_6_* — la pata "
              "formal del desenlace — solo se pregunta a quien contesto "
              "P5_4_*='1'. Sin cuenta, todas las P5_6_* quedan en blanco por "
              "secuencia y `ahorra_solo_informal` se reduce a "
              "`informal_cualquiera` por construccion del cuestionario.")
    return tm


def sec_envipe():
    print("\n" + "=" * 78)
    print("ENVIPE 2025 · payload envipe2025_csv.zip")
    print(f"  sha256 {sha256(Z_ENVIPE)}")
    md = lee_zip_csv(Z_ENVIPE, T_ENVIPE_MOD)
    sd = lee_zip_csv(Z_ENVIPE, T_ENVIPE_SDEM)
    print(f"  tmod_vic: {len(md):,} delitos · ID_PER distintos "
          f"{md.ID_PER.nunique():,} · trae SEXO y EDAD en la propia tabla: "
          f"{('SEXO' in md.columns) and ('EDAD' in md.columns)}")
    print(f"  tsdem   : {len(sd):,} personas · ID_PER llave unica: "
          f"{sd.ID_PER.nunique() == len(sd)}")
    huerf = len(set(md.ID_PER) - set(sd.ID_PER))
    print(f"  (iii) llave delito -> persona: ID_PER. Delitos cuyo ID_PER no "
          f"aparece en tsdem: {huerf:,} de {md.ID_PER.nunique():,}")
    per = sd.set_index("ID_PER")
    print("\n  (iv) EJES en el universo de P4 (BP1_20 in {1,2}; unidad delito)")
    u = md[md.BP1_20.isin(["1", "2"])].copy()
    print(f"    n del universo: {len(u):,} delitos · personas distintas "
          f"{u.ID_PER.nunique():,}")
    marginal(u, "sexo (tmod_vic.SEXO)", u.SEXO, ["1", "2"])
    marginal(u, "edad (tmod_vic.EDAD)", tramos_edad(u.EDAD),
             ["18-29", "30-44", "45-59", "60+"])
    marginal(u, "escolaridad (tsdem.NIV via ID_PER)",
             u.ID_PER.map(per.NIV).map(ESC_ENVIPE)
             .fillna("(fuera: 99/blanco/sin fila)"),
             ["hasta primaria", "secundaria", "media superior", "superior"])
    marginal(u, "dominio (tmod_vic.DOMINIO)",
             u.DOMINIO.map({"U": "Urbano", "C": "Complemento urbano",
                            "R": "Rural"}).fillna("(fuera)"),
             ["Urbano", "Complemento urbano", "Rural"])
    print("      NOTA: DOMINIO se publica SIN umbrales de poblacion en el "
          "payload ni en fd_envipe2025.pdf. NO es el corte de 15 000 que el "
          "encargo pide; se declara como eje propio y distinto.")
    print("    eje tamano de localidad (corte 15 000): NO-ENCONTRADO — ENVIPE "
          "2025 no publica TLOC ni umbral alguno; no se sustituye.")
    print("    eje formalidad laboral : NO-ENCONTRADO — tsdem cierra en AP3_10 "
          "(posicion en la ocupacion); ni el FD ni el cuestionario principal "
          "traen item de prestaciones o seguridad social.")
    return md, sd


def main():
    print("ACTO MAESTRA35-L1 · P0 · CENSO A.4 de ejes de segmentacion")
    print("Sin cruzar jamas contra el desenlace: aqui solo hay llaves, codigos")
    print("y denominadores.\n")
    sec_encig()
    sec_enif()
    sec_envipe()
    print("\n" + "=" * 78)
    print("FIN DEL CENSO. Los codigos de cada eje salen del FD o del catalogo")
    print("del propio payload, citados en forense/notas/"
          "2026-09-02-MAESTRA35-L1-P0-censo.md")


if __name__ == "__main__":
    main()
