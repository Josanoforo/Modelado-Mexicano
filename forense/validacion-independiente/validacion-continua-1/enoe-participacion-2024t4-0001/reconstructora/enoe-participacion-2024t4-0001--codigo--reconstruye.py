#!/usr/bin/env python3
"""Reconstrucción independiente de CALC-ENOE-PARTICIPACION-2024T4-0001 desde paquete/.

Implementa en prosa propia el método de paquete/docs/spec-humana.md:
razón ponderada Σw·y/Σw por dominio (un eje a la vez), IC95 por bootstrap de UPM
dentro de estrato, PCG64(20261004), 2000 réplicas en bloques de 50, percentiles 2.5/97.5,
contrato conservador (una réplica degenerada -> sin IC).

Uso (desde el directorio de trabajo):  python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json y salida/diagnostico.json.
"""
import csv
import json
import os
import sys

import numpy as np
import pandas as pd

RAIZ = os.getcwd()
PAQ = os.path.join(RAIZ, "paquete")
SAL = os.path.join(RAIZ, "salida")

IDENTIDAD = {
    "paquete": "enoe-participacion-2024t4-0001",
    "version_entrada": "validacion-continua-1",
    "sha256_entrada": "e590568f18737bc0bbf5e5ede4ac92b4cc5fc59bc5b9418018a7b3c4f86401d5",
}

# Únicas columnas autorizadas del microdato.
COLUMNAS = ["r_def", "c_res", "eda", "sex", "cs_p17", "clase1", "clase2",
            "t_loc_tri", "niv_ins", "ent", "fac_tri", "est_d_tri", "upm"]

SEMILLA = 20261004
REPLICAS = 2000
BLOQUE = 50

EDAD_TRAMOS = {"15-17": (15, 17), "18-24": (18, 24), "25-44": (25, 44),
               "45-64": (45, 64), "65-MAS": (65, 98)}
LOCALIDAD = {"100MIL-MAS": 1, "15MIL-99MIL": 2, "2500-14999": 3, "MENOS-2500": 4}
ESCOLARIDAD = {"PRIMARIA-INCOMPLETA": 1, "PRIMARIA-COMPLETA": 2,
               "SECUNDARIA-COMPLETA": 3, "MEDIA-SUPERIOR-Y-SUPERIOR": 4}
SEXO = {"HOMBRE": 1, "MUJER": 2}


def num(s):
    return pd.to_numeric(s.astype(str).str.strip(), errors="coerce")


def carga():
    d = pd.read_csv(os.path.join(PAQ, "datos", "sdemt424.csv"), usecols=COLUMNAS,
                    dtype=str, keep_default_na=False, encoding="latin-1")
    n_total = len(d)
    r_def, c_res, eda = num(d["r_def"]), num(d["c_res"]), num(d["eda"])
    fac = num(d["fac_tri"])
    est = d["est_d_tri"].astype(str).str.strip()
    upm = d["upm"].astype(str).str.strip()

    excl = {}
    m_rdef = r_def == 0
    excl["r_def_distinto_de_0"] = int((~m_rdef).sum())
    m_cres = m_rdef & c_res.isin([1, 3])
    excl["c_res_fuera_de_1_3"] = int((m_rdef & ~m_cres).sum())
    m_eda = m_cres & eda.between(15, 98)
    excl["eda_fuera_de_15_98_o_vacia"] = int((m_cres & ~m_eda).sum())
    m_fac = m_eda & (fac > 0)
    excl["fac_tri_no_positivo_o_vacio"] = int((m_eda & ~m_fac).sum())
    m_est = m_fac & (est != "")
    excl["est_d_tri_vacio"] = int((m_fac & ~m_est).sum())
    m_upm = m_est & (upm != "")
    excl["upm_vacia"] = int((m_est & ~m_upm).sum())

    x = pd.DataFrame({
        "eda": eda[m_upm].to_numpy(),
        "sex": num(d.loc[m_upm, "sex"]).to_numpy(),
        "cs_p17": num(d.loc[m_upm, "cs_p17"]).to_numpy(),
        "clase1": num(d.loc[m_upm, "clase1"]).to_numpy(),
        "clase2": num(d.loc[m_upm, "clase2"]).to_numpy(),
        "t_loc_tri": num(d.loc[m_upm, "t_loc_tri"]).to_numpy(),
        "niv_ins": num(d.loc[m_upm, "niv_ins"]).to_numpy(),
        "ent": num(d.loc[m_upm, "ent"]).to_numpy(),
        "w": fac[m_upm].to_numpy(dtype=float),
        "est": est[m_upm].to_numpy(),
        "upm": upm[m_upm].to_numpy(),
    })
    return x, n_total, excl


def conductas(x):
    """Devuelve dict conducta -> vector y (1, 0 o NaN = fuera de la conducta)."""
    y = {}
    c1 = x["clase1"].to_numpy()
    y["participa-economicamente"] = np.where(c1 == 1, 1.0, np.where(c1 == 2, 0.0, np.nan))

    eda = x["eda"].to_numpy()
    cs = x["cs_p17"].to_numpy()
    c2 = x["clase2"].to_numpy()
    joven = (eda >= 18) & (eda <= 24)
    conocido = np.isin(cs, [1, 2]) & np.isfinite(c2)
    nini = np.full(len(x), np.nan)
    ok = joven & conocido
    nini[ok] = ((cs[ok] == 2) & (c2[ok] != 1)).astype(float)
    y["no-estudia-ni-ocupado-18-24"] = nini

    sx = x["sex"].to_numpy()
    muj = np.full(len(x), np.nan)
    sop = (nini == 1) & np.isin(sx, [1, 2])
    muj[sop] = (sx[sop] == 2).astype(float)
    y["mujer-entre-no-estudia-ni-ocupado-18-24"] = muj
    return y


def mascara_segmento(x, eje, seg):
    """Devuelve (mascara del segmento, mascara 'eje sin categoría mapeada')."""
    n = len(x)
    if eje == "TOTAL":
        return np.ones(n, bool), np.zeros(n, bool)
    if eje == "SEXO":
        v = x["sex"].to_numpy()
        return v == SEXO[seg], ~np.isin(v, list(SEXO.values()))
    if eje == "EDAD":
        v = x["eda"].to_numpy()
        lo, hi = EDAD_TRAMOS[seg]
        return (v >= lo) & (v <= hi), ~((v >= 15) & (v <= 98))
    if eje == "LOCALIDAD":
        v = x["t_loc_tri"].to_numpy()
        return v == LOCALIDAD[seg], ~np.isin(v, list(LOCALIDAD.values()))
    if eje == "ESCOLARIDAD":
        v = x["niv_ins"].to_numpy()
        return v == ESCOLARIDAD[seg], ~np.isin(v, list(ESCOLARIDAD.values()))
    if eje == "ENTIDAD":
        v = x["ent"].to_numpy()
        return v == int(seg), ~np.isin(v, list(range(1, 33)))
    raise KeyError(eje)


def diseno(x):
    """Índice de UPM (par estrato-UPM) y estructura por estrato, en orden determinista."""
    est_num = pd.to_numeric(pd.Series(x["est"]), errors="coerce")
    upm_num = pd.to_numeric(pd.Series(x["upm"]), errors="coerce")
    claves = pd.DataFrame({"est": x["est"], "upm": x["upm"],
                           "en": est_num, "un": upm_num})
    uniq = claves.drop_duplicates(["est", "upm"]).sort_values(
        ["en", "est", "un", "upm"], kind="mergesort").reset_index(drop=True)
    uniq["idx"] = np.arange(len(uniq))
    idx = claves.merge(uniq[["est", "upm", "idx"]], on=["est", "upm"], how="left")["idx"].to_numpy()
    estratos = []
    for _, g in uniq.groupby(["en", "est"], sort=True):
        estratos.append(g["idx"].to_numpy())
    return idx, len(uniq), estratos


def multiplicidades(rng, n_upm, estratos, b):
    """Matriz b x n_upm de multiplicidades: remuestreo con reemplazo de n_h UPM dentro de
    cada estrato; estrato con UPM única = certeza (multiplicidad 1)."""
    m = np.zeros((b, n_upm))
    filas = np.arange(b)[:, None]
    for ids in estratos:
        nh = len(ids)
        if nh == 1:
            m[:, ids[0]] = 1.0
            continue
        sel = rng.integers(0, nh, size=(b, nh))
        np.add.at(m, (np.broadcast_to(filas, sel.shape), ids[sel]), 1.0)
    return m


def fmt(v):
    return repr(float(v))


def main():
    x, n_total, excl_glob = carga()
    y = conductas(x)
    idx, n_upm, estratos = diseno(x)
    w = x["w"].to_numpy()

    esquema = []
    with open(os.path.join(PAQ, "esquema-identidades.tsv"), encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            esquema.append(r)

    # Agregados por UPM para numerador y denominador de cada llave.
    tareas = []
    diag_llaves = []
    for r in esquema:
        cond, eje, seg = r["conducta"], r["eje"], r["segmento"]
        seg_m, sin_cat = mascara_segmento(x, eje, seg)
        yy = y[cond]
        conocida = np.isfinite(yy)
        dom = seg_m & conocida
        num_u = np.bincount(idx[dom], weights=(w * yy)[dom], minlength=n_upm)
        den_u = np.bincount(idx[dom], weights=w[dom], minlength=n_upm)
        tareas.append((num_u, den_u))
        diag_llaves.append({
            "llave": r["llave"], "conducta": cond, "eje": eje, "segmento": seg,
            "n_valido": int(dom.sum()),
            "suma_pesos": fmt(w[dom].sum()),
            "n_upm_con_casos": int((den_u > 0).sum()),
            "exclusiones": {
                "universo_y_diseno_global": sum(excl_glob.values()),
                "eje_sin_categoria_mapeada": int(sin_cat.sum()),
                "fuera_del_segmento": int((~seg_m & ~sin_cat).sum()),
                "en_segmento_fuera_de_la_conducta": int((seg_m & ~conocida).sum()),
            },
        })

    NUM = np.vstack([t[0] for t in tareas])  # k x n_upm
    DEN = np.vstack([t[1] for t in tareas])
    k = NUM.shape[0]

    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    reps = np.empty((REPLICAS, k))
    degenerada = np.zeros(k, bool)
    hechas = 0
    while hechas < REPLICAS:
        b = min(BLOQUE, REPLICAS - hechas)
        m = multiplicidades(rng, n_upm, estratos, b)
        rn = m @ NUM.T
        rd = m @ DEN.T
        with np.errstate(divide="ignore", invalid="ignore"):
            q = rn / rd
        degenerada |= ~(np.isfinite(q) & (rd > 0)).all(axis=0)
        reps[hechas:hechas + b] = q
        hechas += b

    filas = []
    for i, r in enumerate(esquema):
        dn = DEN[i].sum()
        fila = {"llave": r["llave"], "unidad": r["unidad"]}
        dg = diag_llaves[i]
        if not dn > 0:
            fila["estado"] = "DENOMINADOR-CERO"
            fila["motivo"] = ("dominio observado vacío: ninguna persona válida del universo cumple "
                              "el segmento con la conducta definida (Σw = 0)")
            dg["resultado"] = "DENOMINADOR-CERO"
        else:
            p = NUM[i].sum() / dn
            fila["estado"] = "RECONSTRUIDO"
            fila["punto"] = fmt(p)
            if degenerada[i]:
                fila["estado_ic"] = "NO-IDENTIFICADA"
                fila["motivo_ic"] = ("al menos una réplica bootstrap degenerada (denominador cero o "
                                     "razón no finita); contrato conservador: sin EE ni IC")
                dg["replicas_degeneradas"] = int((~np.isfinite(reps[:, i])).sum())
            else:
                lo, hi = np.percentile(reps[:, i], [2.5, 97.5])
                fila["estado_ic"] = "CALCULADO"
                fila["ic95_inf"] = fmt(lo)
                fila["ic95_sup"] = fmt(hi)
            dg["resultado"] = fila["estado_ic"]
        filas.append(fila)

    doc = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "decisiones.json"),
              encoding="utf-8") as f:
        decisiones = json.load(f)

    diag = {
        "calc": "CALC-ENOE-PARTICIPACION-2024T4-0001",
        "filas_microdato": n_total,
        "exclusiones_globales_secuenciales": excl_glob,
        "n_universo_valido": int(len(x)),
        "diseno": {"n_estratos": len(estratos), "n_upm_estrato_par": n_upm,
                   "estratos_con_upm_unica": int(sum(len(e) == 1 for e in estratos)),
                   "semilla": SEMILLA, "replicas": REPLICAS, "bloque": BLOQUE},
        "decisiones": decisiones,
        "llaves": diag_llaves,
    }
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as f:
        json.dump(diag, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    sys.exit(main())
