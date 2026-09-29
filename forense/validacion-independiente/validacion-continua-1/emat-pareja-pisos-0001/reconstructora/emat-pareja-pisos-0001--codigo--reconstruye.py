#!/usr/bin/env python3
"""Reconstrucción CALC-EMAT-PAREJA-PISOS-0001 desde paquete/docs/spec-humana.md.

Uso (desde el directorio de trabajo):  python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json y salida/diagnostico.json.

Acceso: de cada MATRIyy.dbf se lee la cabecera (lista de campos) y, de las
filas, sólo los bytes de las 12 columnas autorizadas; ninguna otra columna se
decodifica. No se imprime ninguna fila.
"""
import json
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "paquete/lib")
from dbfread import DBF  # noqa: E402  (sólo cabecera)

PAQ = "paquete"
SAL = "salida"
OLAS = list(range(2010, 2024))
Z = 1.959964
IDENTIDAD = {
    "paquete": "emat-pareja-pisos-0001",
    "version_entrada": "validacion-continua-1",
    "sha256_entrada": "ce83abdc757dce2c6f0d83afc8dc41a5b33a30e3fee516d5dabef7caf2cf7a6e",
}
PERMITIDAS = ["ENT_REGIS", "TAM_LOC_RE", "ANIO_REGIS", "GENERO", "SEXO_CON1", "SEXO_CON2",
              "EDAD_CON1", "EDAD_CON2", "CONACTCON1", "CONACTCON2", "ESCOL_CON1", "ESCOL_CON2"]


# ---------------------------------------------------------------- lectura
def lee_dbf(ruta):
    """Cabecera con dbfread; filas: sólo bytes de las columnas permitidas."""
    t = DBF(ruta, load=False)
    hl, rl, n = t.header.headerlen, t.header.recordlen, t.header.numrecords
    offs, pos = {}, 1  # byte 0 de cada registro = marca de borrado
    for f in t.fields:
        offs[f.name] = (pos, f.length, f.type)
        pos += f.length
    faltan = [c for c in PERMITIDAS if c not in offs]
    if faltan:
        raise SystemExit(f"{ruta}: faltan columnas {faltan}")
    raw = np.memmap(ruta, dtype=np.uint8, mode="r", offset=hl, shape=(n, rl))
    vivo = raw[:, 0] != ord("*")
    out = {}
    for c in PERMITIDAS:
        p, L, typ = offs[c]
        s = np.ascontiguousarray(raw[:, p:p + L]).view(f"S{L}").ravel()
        s = pd.Series(s).str.decode("latin-1").str.strip()
        if c == "ENT_REGIS":
            out[c] = s
        else:
            out[c] = pd.to_numeric(s.replace("", np.nan), errors="coerce")
    df = pd.DataFrame(out)
    info = {"campos_cabecera": len(t.fields), "registros_cabecera": int(n),
            "registros_borrados": int((~vivo).sum())}
    return df[vivo].reset_index(drop=True), info


# ---------------------------------------------------------------- segmentos
def seg_tloc(v):
    return pd.Series(np.select([v.between(1, 3), v.between(4, 6), v.between(7, 12), v.between(13, 17)],
                               ["MENOS-2500", "2500-14999", "15MIL-99MIL", "100MIL-MAS"], default=""),
                     index=v.index)


def seg_escol(v):
    return pd.Series(np.select([v.between(1, 4), v == 5, v == 6, v == 7],
                               ["PRIMARIA-O-MENOS", "SECUNDARIA", "PREPARATORIA", "PROFESIONAL"], default=""),
                     index=v.index)


def seg_sexo(v):
    return pd.Series(np.select([v == 1, v == 2], ["HOMBRE", "MUJER"], default=""), index=v.index)


ENTS = [f"{i:02d}" for i in range(1, 33)]


def seg_ent(v):
    return v.where(v.isin(ENTS), "")


# ---------------------------------------------------------------- conductas
def matrimonio(df):
    """Devuelve dict conducta -> (numerador bool, universo bool, causas{nombre: bool})."""
    e1, e2 = df.EDAD_CON1, df.EDAD_CON2
    v1, v2 = e1.between(12, 98), e2.between(12, 98)
    menor = e1.between(12, 17) | e2.between(12, 17)
    ca1, ca2 = df.CONACTCON1, df.CONACTCON2
    es1, es2 = df.ESCOL_CON1, df.ESCOL_CON2
    g = df.GENERO
    u_ms = g.isin([1, 2])
    u_m18 = (v1 & v2) | menor
    u_at = ca1.isin([1, 2]) & ca2.isin([1, 2])
    u_me = es1.between(1, 7) & es2.between(1, 7)
    return {
        "m-mismo-sexo": (g == 2, u_ms, {"genero_fuera_1_2": ~u_ms}),
        "m-con-menor-18": (menor, u_m18,
                           {"alguna_edad_fuera_12_98_sin_contrayente_12_17": ~u_m18}),
        "m-ambos-trabajan": ((ca1 == 1) & (ca2 == 1), u_at, {"algun_conact_fuera_1_2": ~u_at}),
        "m-misma-escolaridad": (u_me & (es1 == es2), u_me, {"alguna_escol_fuera_1_7": ~u_me}),
    }


def contrayentes(df):
    """Apila las dos filas por matrimonio (CON1, CON2)."""
    partes = []
    for k in ("1", "2"):
        partes.append(pd.DataFrame({
            "edad": df[f"EDAD_CON{k}"], "sexo": df[f"SEXO_CON{k}"],
            "escol": df[f"ESCOL_CON{k}"], "conact": df[f"CONACTCON{k}"],
            "tloc": df.TAM_LOC_RE,
        }))
    return pd.concat(partes, ignore_index=True)


BINS_EDAD = {"c-edad-12-19": (12, 19), "c-edad-20-24": (20, 24), "c-edad-25-29": (25, 29),
             "c-edad-30-34": (30, 34), "c-edad-35-39": (35, 39), "c-edad-40-mas": (40, 98)}


def contrayente_conductas(c):
    ev = c.edad.between(12, 98)
    uc = c.conact.isin([1, 2])
    d = {}
    for k, (a, b) in BINS_EDAD.items():
        d[k] = (c.edad.between(a, b), ev, {"edad_fuera_12_98": ~ev})
    d["c-trabaja"] = (c.conact == 1, uc, {"conact_fuera_1_2": ~uc})
    d["c-edad-media"] = (None, ev, {"edad_fuera_12_98": ~ev})
    return d


# ---------------------------------------------------------------- cálculo
def calcula():
    esquema = pd.read_csv(f"{PAQ}/esquema-identidades.tsv", sep="\t", dtype=str, keep_default_na=False)
    celdas = {}   # (conducta, eje, segmento, ola) -> dict
    diag_ola = {}
    for ola in OLAS:
        ruta = f"{PAQ}/datos/matri{ola % 100:02d}.dbf"
        df, info = lee_dbf(ruta)
        n = len(df)
        e = pd.concat([df.EDAD_CON1, df.EDAD_CON2])
        s = pd.concat([df.SEXO_CON1, df.SEXO_CON2])
        info.update({
            "filas_vivas": n,
            "anio_regis_distinto_de_ola": int((df.ANIO_REGIS != ola).sum()),
            "anio_regis_valores": {str(int(k)) if not pd.isna(k) else "vacío": int(v)
                                   for k, v in df.ANIO_REGIS.value_counts(dropna=False).items()},
            "genero_fuera_1_2": int((~df.GENERO.isin([1, 2])).sum()),
            "edades_contrayente_99": int((e == 99).sum()),
            "edades_contrayente_fuera_12_99": int((~e.between(12, 99)).sum()),
            "sexo_contrayente_fuera_1_2": int((~s.isin([1, 2])).sum()),
            "ent_regis_fuera_01_32": int((~df.ENT_REGIS.isin(ENTS)).sum()),
            "tam_loc_re_99_o_fuera_1_17": int((~df.TAM_LOC_RE.between(1, 17)).sum()),
            "contrayente_escol_8_9_o_fuera_1_7": int((~pd.concat([df.ESCOL_CON1, df.ESCOL_CON2]).between(1, 7)).sum()),
        })
        diag_ola[str(ola)] = info

        # matrimonio
        ejes_m = {"TOTAL": pd.Series("TODOS", index=df.index), "ENT": seg_ent(df.ENT_REGIS),
                  "TLOC": seg_tloc(df.TAM_LOC_RE)}
        for cond, (num, uni, causas) in matrimonio(df).items():
            for eje, seg in ejes_m.items():
                for sg in seg[seg != ""].unique():
                    m = seg == sg
                    celdas[(cond, eje, sg, ola)] = cel_prop(num, uni, causas, m)
        # contrayente
        c = contrayentes(df)
        ejes_c = {"TOTAL": pd.Series("TODOS", index=c.index), "SEXO": seg_sexo(c.sexo),
                  "ESCOLARIDAD": seg_escol(c.escol), "TLOC": seg_tloc(c.tloc)}
        for cond, (num, uni, causas) in contrayente_conductas(c).items():
            for eje, seg in ejes_c.items():
                for sg in seg[seg != ""].unique():
                    m = seg == sg
                    if num is None:
                        celdas[(cond, eje, sg, ola)] = cel_media(c.edad, uni, causas, m)
                    else:
                        celdas[(cond, eje, sg, ola)] = cel_prop(num, uni, causas, m)
        print(f"ola {ola}: {n} filas vivas", file=sys.stderr)

    # tau2 por conducta x eje x categoría (sólo proporciones)
    tau2 = {}
    for _, r in esquema[["conducta", "eje", "segmento"]].drop_duplicates().iterrows():
        k3 = (r.conducta, r.eje, r.segmento)
        if r.conducta == "c-edad-media":
            continue
        d2, pares = [], []
        for a, b in zip(OLAS[:-1], OLAS[1:]):
            pa = celdas.get(k3 + (a,), {}).get("p")
            pb = celdas.get(k3 + (b,), {}).get("p")
            if pa is not None and pb is not None and 0 < pa < 1 and 0 < pb < 1:
                d2.append((logit(pb) - logit(pa)) ** 2)
                pares.append(f"{a}-{b}")
        tau2[k3] = {"tau2": (sum(d2) / len(d2)) if d2 else None, "pares": pares}

    filas, diag_llaves = [], {}
    for _, r in esquema.iterrows():
        k3 = (r.conducta, r.eje, r.segmento)
        ola = int(r.ola)
        cel = celdas.get(k3 + (ola,))
        fila = {"llave": r.llave, "unidad": r.unidad}
        dg = {"conducta": r.conducta, "eje": r.eje, "segmento": r.segmento, "ola": ola}
        if cel is None or cel["n_valido"] == 0:
            fila["estado"] = "DENOMINADOR-CERO"
            fila["motivo"] = ("segmento sin filas en la ola" if cel is None else
                              "segmento con filas pero ninguna en el universo de la conducta")
            dg.update(cel or {"n_segmento": 0, "n_valido": 0})
        else:
            p = cel["p"]
            fila["estado"] = "RECONSTRUIDO"
            fila["punto"] = repr(float(p))
            dg.update(cel)
            if r.conducta == "c-edad-media":
                fila["estado_ic"] = "SIN-IC"
            elif ola != 2023:
                fila["estado_ic"] = "SIN-IC"
            else:
                t = tau2[k3]
                dg["tau2"] = None if t["tau2"] is None else repr(float(t["tau2"]))
                dg["tau2_pares"] = t["pares"]
                if not (0 < p < 1):
                    fila["estado_ic"] = "NO-IDENTIFICADA"
                    fila["motivo_ic"] = f"p 2023 = {repr(float(p))} fuera de (0,1): logit no definido"
                elif t["tau2"] is None:
                    fila["estado_ic"] = "NO-IDENTIFICADA"
                    fila["motivo_ic"] = "tau2 no definido: ningún par de olas consecutivas con p en (0,1)"
                else:
                    h = Z * math.sqrt(t["tau2"])
                    lo, hi = expit(logit(p) - h), expit(logit(p) + h)
                    fila["estado_ic"] = "CALCULADO"
                    fila["ic95_inf"] = repr(float(lo))
                    fila["ic95_sup"] = repr(float(hi))
        dg.pop("p", None)
        filas.append(fila)
        diag_llaves[r.llave] = dg

    # controles §5 (post-sello, sólo se reporta la diferencia)
    ms23 = celdas[("m-mismo-sexo", "TOTAL", "TODOS", 2023)]["numerador"]
    n22 = diag_ola["2022"]["filas_vivas"]
    controles = {
        "conteo_m_mismo_sexo_2023": ms23, "referencia_pareja_012": 6606, "diferencia_012": ms23 - 6606,
        "n_total_2022": n22, "referencia_pareja_001": 507052, "diferencia_001": n22 - 507052,
    }
    return filas, diag_llaves, diag_ola, controles


def cel_prop(num, uni, causas, m):
    u = uni & m
    nv = int(u.sum())
    x = int((num & u).sum())
    return {"n_segmento": int(m.sum()), "n_valido": nv, "numerador": x,
            "exclusiones": {k: int((v & m).sum()) for k, v in causas.items()},
            "p": (x / nv) if nv else None}


def cel_media(edad, uni, causas, m):
    u = uni & m
    nv = int(u.sum())
    return {"n_segmento": int(m.sum()), "n_valido": nv, "suma_edades": int(edad[u].sum()),
            "exclusiones": {k: int((v & m).sum()) for k, v in causas.items()},
            "p": float(edad[u].astype("float64").mean()) if nv else None}


def logit(p):
    return math.log(p / (1 - p))


def expit(x):
    return 1 / (1 + math.exp(-x))


DECISIONES = [
    {"id": "D1-universo-filas", "frase": "Matrimonio: todas las filas vivas del DBF.",
     "decision": "Se usan todos los registros no marcados como borrados; ANIO_REGIS distinto de la ola se "
                 "reporta como diagnóstico y NO se excluye (§1 lo lista entre 'Diagnósticos por ola')."},
    {"id": "D2-edad-valida", "frase": "C-EDAD-MEDIA (media de edad 12–98) · C-EDAD-{…} (proporción; universo edad válida)",
     "decision": "Edad válida = 12..98 (99 = No especificada y cualquier otro valor excluidos). 40-MAS = 40..98."},
    {"id": "D3-menor-18", "frase": "algún contrayente de 12–17; universo: ambas edades válidas, o la condición se cumple",
     "decision": "Numerador: EDAD_CON1 o EDAD_CON2 en 12..17. Universo: (ambas en 12..98) o numerador."},
    {"id": "D4-misma-escolaridad", "frase": "`ESCOL_CON1`=`ESCOL_CON2`; universo ambos en 1–7",
     "decision": "Igualdad de código crudo 1..7 (no de los grupos del eje ESCOLARIDAD)."},
    {"id": "D5-eje-contrayente", "frase": "Contrayente: TOTAL · SEXO · ESCOLARIDAD (primaria o menos 1–4 / secundaria 5 / preparatoria 6 / profesional 7) · TLOC.",
     "decision": "SEXO y ESCOLARIDAD son los del propio contrayente (SEXO_CONk, ESCOL_CONk); TLOC es el TAM_LOC_RE "
                 "del matrimonio. Contrayentes con sexo fuera de {1,2}, escolaridad 8/9 o TAM_LOC_RE 99 quedan "
                 "fuera de ese eje (no de TOTAL)."},
    {"id": "D6-ejes-matrimonio", "frase": "ENT (entidad de registro, 32) · TLOC (localidad de registro: <2 500 = rangos 1–3; …)",
     "decision": "ENT_REGIS '01'..'32'; otros códigos quedan fuera del eje ENT. TAM_LOC_RE 99 queda fuera de TLOC."},
    {"id": "D7-tau2-pares", "frase": "τ² … = media de Δ² en logit entre olas consecutivas con p ∈ (0,1)",
     "decision": "Pares de años calendario adyacentes (y, y+1) en que ambas p están en (0,1); τ² = suma de Δ² / "
                 "número de pares válidos. Un par con algún p en {0,1} se omite (no se empalma con la ola siguiente)."},
    {"id": "D8-ic-solo-2023", "frase": "IC calibrado sobre el piso 2023: expit(logit p ± 1.959964·√τ²)",
     "decision": "El IC se calcula sólo para las llaves de ola 2023 (p = piso 2023); las olas 2010–2022 van "
                 "RECONSTRUIDO con estado_ic SIN-IC porque la spec no define IC para ellas."},
    {"id": "D9-edad-media-sin-ic", "frase": "τ² por conducta × eje × categoría (proporciones)",
     "decision": "C-EDAD-MEDIA no es proporción: τ² no está definido → estado_ic SIN-IC en todas las olas."},
    {"id": "D10-ic-no-identificada", "frase": "expit(logit p ± 1.959964·√τ²)",
     "decision": "Si p 2023 ∈ {0,1} (logit indefinido) o no hay pares válidos para τ², estado_ic NO-IDENTIFICADA con motivo."},
    {"id": "D11-sin-supresion", "frase": "Registro completo: sin diseño muestral, sin EE ni IC de diseño",
     "decision": "Ninguna celda se suprime por tamaño; ee de diseño = 0."},
    {"id": "D12-unidad-literal", "frase": "Las columnas conducta, eje, segmento y ola del esquema dicen qué estima cada llave.",
     "decision": "C-EDAD-MEDIA se reporta en años aunque la unidad literal del esquema diga 'proporcion'; la unidad se copia literal."},
]


def main():
    filas, diag_llaves, diag_ola, controles = calcula()
    os.makedirs(SAL, exist_ok=True)
    with open(f"{SAL}/resultado.json", "w", encoding="utf-8") as f:
        json.dump({"version": 3, "identidad": IDENTIDAD, "filas": filas}, f, ensure_ascii=False, indent=1)
    estados = {k: int(v) for k, v in pd.Series([r["estado"] for r in filas]).value_counts().items()}
    est_ic = {k: int(v) for k, v in pd.Series([r.get("estado_ic", "-") for r in filas]).value_counts().items()}
    with open(f"{SAL}/diagnostico.json", "w", encoding="utf-8") as f:
        json.dump({
            "identidad": IDENTIDAD,
            "acceso": {"columnas_leidas": PERMITIDAS,
                       "nota": "cabecera DBF completa leída (nombres/tipos/largos); de las filas sólo se "
                               "decodifican los bytes de las columnas listadas"},
            "resumen": {"filas": len(filas), "estado": estados, "estado_ic": est_ic},
            "por_ola": diag_ola,
            "controles_seccion_5": controles,
            "decisiones": DECISIONES,
            "por_llave": diag_llaves,
        }, f, ensure_ascii=False, indent=1)
    print(json.dumps({"estado": estados, "estado_ic": est_ic, "controles": controles}, ensure_ascii=False))


if __name__ == "__main__":
    main()
