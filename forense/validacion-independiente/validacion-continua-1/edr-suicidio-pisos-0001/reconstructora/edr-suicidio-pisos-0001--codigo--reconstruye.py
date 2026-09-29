"""Reconstrucción CALC-EDR-SUICIDIO-PISOS-0001 desde paquete/docs/spec-humana.md.

Uso (desde el directorio de trabajo):  python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json y salida/diagnostico.json.
"""
import json
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lector_dbf import lee, ruta  # noqa: E402

OLAS = list(range(2015, 2024))
Z = 1.959964
IDENTIDAD = {"paquete": "edr-suicidio-pisos-0001",
             "version_entrada": "validacion-continua-1",
             "sha256_entrada": "192ae5aec4169e11d882ecb36972bc509eac3cd14d00b9f67a61cfdee97aa84f"}

ENT_VALIDAS = [f"{i:02d}" for i in range(1, 33)]
TLOC_MAP = {**{str(i): "MENOS-2500" for i in (1, 2, 3)},
            **{str(i): "2500-14999" for i in (4, 5, 6)},
            **{str(i): "15MIL-99MIL" for i in range(7, 13)},
            **{str(i): "100MIL-MAS" for i in range(13, 18)}}
ESC_MAP = {**{str(i): "PRIMARIA-O-MENOS" for i in (1, 2, 3, 4)},
           **{str(i): "SECUNDARIA" for i in (5, 6)},
           **{str(i): "MEDIA-SUPERIOR" for i in (7, 8)},
           **{str(i): "SUPERIOR" for i in (9, 10)}}
SEXO_MAP = {"1": "HOMBRE", "2": "MUJER"}
EDAD_NO_ESP = {"1098", "2098", "3098", "4998"}


def banda_edad(anios):
    cortes = [(0, 9, "0-9"), (10, 14, "10-14"), (15, 19, "15-19"), (20, 24, "20-24"),
              (25, 29, "25-29"), (30, 44, "30-44"), (45, 59, "45-59")]
    out = pd.Series(pd.NA, index=anios.index, dtype="object")
    for lo, hi, et in cortes:
        out[(anios >= lo) & (anios <= hi)] = et
    out[anios >= 60] = "60-MAS"
    return out


def prepara(ola):
    df, info = lee(ola)
    d = pd.DataFrame(index=df.index)
    causa3 = df["CAUSA_DEF"].str[:3]
    d["causa_no_vacia"] = df["CAUSA_DEF"] != ""
    d["cie"] = d["causa_no_vacia"] & causa3.str.match(r"^X[0-9]{2}$") & causa3.between("X60", "X84")
    col_pres = "PRESUNTO" if ola <= 2021 else "TIPO_DEFUN"
    d["presunto"] = df[col_pres] == "3"
    d["sexo_valido"] = df["SEXO"].isin(["1", "2"])
    d["hombre"] = df["SEXO"] == "1"
    edad = df["EDAD"]
    edad_num = pd.to_numeric(edad, errors="coerce")
    unidad = edad.str[:1]
    d["edad_valida"] = edad_num.notna() & ~edad.isin(EDAD_NO_ESP) & unidad.isin(["1", "2", "3", "4"])
    anios = pd.Series(np.nan, index=df.index)
    anios[d["edad_valida"] & (unidad == "4")] = edad_num - 4000
    anios[d["edad_valida"] & unidad.isin(["1", "2", "3"])] = 0.0
    d["anios"] = anios
    d["e15_44"] = (unidad == "4") & d["edad_valida"] & anios.between(15, 44)
    d["e15_29"] = (unidad == "4") & d["edad_valida"] & anios.between(15, 29)
    d["ocurr_en_ola"] = pd.to_numeric(df["ANIO_OCUR"], errors="coerce") == ola
    # ejes
    d["ax_TOTAL"] = "TODOS"
    d["ax_SEXO"] = df["SEXO"].map(SEXO_MAP)
    d["ax_EDAD"] = banda_edad(anios)
    d["ax_ENT"] = df["ENT_RESID"].where(df["ENT_RESID"].isin(ENT_VALIDAS))
    d["ax_TLOC"] = df["TLOC_RESID"].map(TLOC_MAP)
    d["ax_ESCOLARIDAD"] = df["ESCOLARIDA"].map(ESC_MAP)
    extra = {
        "anio_regis": {str(k): int(v) for k, v in df["ANIO_REGIS"].value_counts().items()},
        "anio_ocur_9999": int((df["ANIO_OCUR"] == "9999").sum()),
        "columna_presunto": col_pres,
        "raw": {c: {str(k): int(v) for k, v in df[c].value_counts().items()}
                for c in ["SEXO", "ENT_RESID", "TLOC_RESID", "ESCOLARIDA", col_pres]},
    }
    return d, info, extra


# conducta -> (universo, numerador, exclusiones del universo por causa)
def conductas(d):
    todas = pd.Series(True, index=d.index)
    cie = d["cie"]
    return {
        "suicidio-cie": (d["causa_no_vacia"], d["cie"],
                         {"causa_vacia": ~d["causa_no_vacia"]}),
        "suicidio-presunto": (todas, d["presunto"], {}),
        "suic-hombre": (cie & d["sexo_valido"], d["hombre"],
                        {"no_suicidio_cie": ~cie, "sexo_no_especificado_en_cie": cie & ~d["sexo_valido"]}),
        "suic-15-44": (cie & d["edad_valida"], d["e15_44"],
                       {"no_suicidio_cie": ~cie, "edad_no_valida_en_cie": cie & ~d["edad_valida"]}),
        "suic-15-29": (cie & d["edad_valida"], d["e15_29"],
                       {"no_suicidio_cie": ~cie, "edad_no_valida_en_cie": cie & ~d["edad_valida"]}),
        "suic-ocurrido-en-ola": (cie, d["ocurr_en_ola"], {"no_suicidio_cie": ~cie}),
    }


def num(x):
    return repr(float(x))


def logit(p):
    return math.log(p / (1.0 - p))


def expit(x):
    return 1.0 / (1.0 + math.exp(-x))


def main():
    esq = pd.read_csv("paquete/esquema-identidades.tsv", sep="\t", dtype=str, keep_default_na=False)
    celdas = {}   # (conducta, eje, segmento, ola) -> dict
    diag_olas = {}
    for ola in OLAS:
        d, info, extra = prepara(ola)
        conc = pd.crosstab(d["cie"], d["presunto"])
        diag_olas[str(ola)] = {
            "archivo": ruta(ola), **info, **extra,
            "concordancia_cie_vs_presunto": {
                "cie_y_presunto": int((d["cie"] & d["presunto"]).sum()),
                "cie_no_presunto": int((d["cie"] & ~d["presunto"]).sum()),
                "presunto_no_cie": int((~d["cie"] & d["presunto"]).sum()),
                "ninguno": int((~d["cie"] & ~d["presunto"]).sum()),
            },
            "conteo_suicidio_cie_por_sexo": {k: int(v) for k, v in
                                             d.loc[d["cie"], "ax_SEXO"].value_counts(dropna=False).items()
                                             if isinstance(k, str)},
        }
        del conc
        for cond, (univ, numer, excl_u) in conductas(d).items():
            excl_u_n = {k: int(v.sum()) for k, v in excl_u.items()}
            for eje in ["TOTAL", "SEXO", "EDAD", "ENT", "TLOC", "ESCOLARIDAD"]:
                ax = d["ax_" + eje]
                en_univ = ax[univ]
                excl_eje = int(en_univ.isna().sum())
                den = en_univ.value_counts()
                nume = ax[univ & numer].value_counts()
                segs = set(esq.loc[(esq.conducta == cond) & (esq.eje == eje), "segmento"])
                for s in segs:
                    celdas[(cond, eje, s, ola)] = {
                        "n_valido": int(den.get(s, 0)),
                        "conteo": int(nume.get(s, 0)),
                        "filas_ola": info["filas_vivas"],
                        "exclusiones_universo_conducta": excl_u_n,
                        "exclusiones_eje_valor_no_asignable": excl_eje,
                    }
        print("ola", ola, "lista", flush=True)

    # puntos
    for c in celdas.values():
        c["p"] = c["conteo"] / c["n_valido"] if c["n_valido"] > 0 else None

    filas, diag_llaves = [], []
    for r in esq.itertuples(index=False):
        ola = int(r.ola)
        c = celdas[(r.conducta, r.eje, r.segmento, ola)]
        fila = {"llave": r.llave, "unidad": r.unidad}
        dg = {"llave": r.llave, "conducta": r.conducta, "eje": r.eje, "segmento": r.segmento,
              "ola": ola, **{k: v for k, v in c.items() if k != "p"}}
        if c["p"] is None:
            fila.update(estado="DENOMINADOR-CERO",
                        motivo=f"universo de {r.conducta} en {r.eje}={r.segmento}, ola {ola}: 0 defunciones")
            filas.append(fila)
            diag_llaves.append(dg)
            continue
        p = c["p"]
        fila.update(estado="RECONSTRUIDO", punto=num(p))
        if ola != 2023:
            fila["estado_ic"] = "SIN-IC"
        else:
            serie = [celdas[(r.conducta, r.eje, r.segmento, o)]["p"] for o in OLAS]
            dg["serie_p"] = [None if x is None else num(x) for x in serie]
            malas = [str(o) for o, x in zip(OLAS, serie) if x is None or x <= 0.0 or x >= 1.0]
            if malas:
                fila["estado_ic"] = "NO-IDENTIFICADA"
                fila["motivo_ic"] = ("tau2 no identificado: logit no finito (p en {0,1} o denominador cero) "
                                     "en ola(s) " + ",".join(malas))
            else:
                lg = [logit(x) for x in serie]
                deltas = [lg[i + 1] - lg[i] for i in range(len(lg) - 1)]
                tau2 = sum(dd * dd for dd in deltas) / len(deltas)
                h = Z * math.sqrt(tau2)
                lo, hi = expit(logit(p) - h), expit(logit(p) + h)
                fila.update(estado_ic="CALCULADO", ic95_inf=num(lo), ic95_sup=num(hi))
                dg["tau2"] = num(tau2)
                dg["n_deltas"] = len(deltas)
        filas.append(fila)
        diag_llaves.append(dg)

    doc = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    os.makedirs("salida", exist_ok=True)
    with open("salida/resultado.json", "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "decisiones.json"),
              encoding="utf-8") as f:
        decisiones = json.load(f)
    resumen = pd.Series([x["estado"] + "/" + x.get("estado_ic", "-") for x in filas]).value_counts()
    diag = {"identidad": IDENTIDAD,
            "resumen_estados": {k: int(v) for k, v in resumen.items()},
            "decisiones_implementacion": decisiones,
            "olas": diag_olas,
            "llaves": diag_llaves}
    with open("salida/diagnostico.json", "w", encoding="utf-8") as f:
        json.dump(diag, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(resumen.to_dict())


if __name__ == "__main__":
    main()
