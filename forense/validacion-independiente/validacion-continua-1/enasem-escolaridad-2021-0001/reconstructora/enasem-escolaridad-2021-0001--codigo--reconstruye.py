"""Reconstrucción CALC-ENASEM-ESCOLARIDAD-2021-0001 desde paquete/ (spec humana v1.0).

Uso, desde el directorio de trabajo:  python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json (CONTRATO-v3) y salida/diagnostico.json.
"""
import csv
import json
import os

import numpy as np
import pandas as pd

PAQ = "paquete"
SAL = "salida"
CSV = os.path.join(PAQ, "datos", "sect_a_2021.csv")
ESQUEMA = os.path.join(PAQ, "esquema-identidades.tsv")

# Únicas columnas autorizadas (FIRMAS-Y-ACCESO / encargo).
COLS = ["YRSCHOOL", "SEX_21", "AGE_21", "FACTORI_21", "EST_DIS_21", "UPM_DIS_21"]

IDENTIDAD = {
    "paquete": "enasem-escolaridad-2021-0001",
    "version_entrada": "validacion-continua-1",
    "sha256_entrada": "f76eddec9aae60712adaba5f93d1dbd6585f1e25008a506f4fbcbcf881e65bd5",
}

# spec §4
SEMILLA = 20260930
REPLICAS = 2000
BLOQUE = 50
PCTS = (2.5, 97.5)

# spec §2: UNO / CERO sobre YRSCHOOL
CONDUCTAS = {
    "sin-escolaridad": (set(range(0, 1)), set(range(1, 23))),
    "seis-anos-o-menos": (set(range(0, 7)), set(range(7, 23))),
}
# spec §3
TRAMOS_EDAD = {"50-59": (50, 59), "60-69": (60, 69), "70-79": (70, 79), "80-MAS": (80, 130)}
SEXO = {"HOMBRE": 1, "MUJER": 2}

DECISIONES = [
    {
        "decision": "Bootstrap de UPM: en cada estrato con n_h UPM se sortean n_h UPM con reemplazo (equiprobables); "
                    "el peso de réplica es FACTORI_21 x multiplicidad de su UPM. Sin reescalamiento Rao-Wu ni n_h-1.",
        "frase": "«Razón ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato (UPM única del estrato = de certeza)»",
    },
    {
        "decision": "Estrato con una sola UPM: se trata como de certeza, multiplicador 1 en todas las réplicas "
                    "(no ocurre en el dato: los 4 estratos tienen >1 UPM).",
        "frase": "«(UPM única del estrato = de certeza)»",
    },
    {
        "decision": "Generador numpy.random.Generator(numpy.random.PCG64(20260930)); 2000 réplicas generadas en 40 bloques "
                    "de 50; en cada bloque, para cada estrato en orden numérico ascendente, rng.integers(0, n_h, size=(50, n_h)) "
                    "sobre las UPM del estrato ordenadas por id numérico. El orden de consumo del generador no lo fija la spec.",
        "frase": "«Semilla y réplicas (para recalcular): numpy.PCG64(20260930), 2000 réplicas, bloques de 50»",
    },
    {
        "decision": "Un solo juego de réplicas de UPM, construido sobre el marco universo+diseño válido (antes de excluir "
                    "YRSCHOOL en blanco), compartido por las 14 llaves.",
        "frase": "«Válido: peso > 0, estrato y UPM no vacíos (M.prepara_diseno)» y «vía M.mide_ola»",
    },
    {
        "decision": "IC = percentiles 2.5 y 97.5 de las 2000 réplicas con numpy.percentile (interpolación lineal por defecto).",
        "frase": "«percentiles 2.5/97.5»",
    },
    {
        "decision": "Réplica degenerada = réplica cuyo denominador Σw_rep del dominio (filas con y en UNO/CERO) es 0 o cuyo "
                    "valor no es finito; si hay al menos una, la llave queda RECONSTRUIDO con estado_ic NO-IDENTIFICADA.",
        "frase": "«contrato conservador (una réplica degenerada → sin EE ni IC)»",
    },
    {
        "decision": "YRSCHOOL en blanco (o fuera de 0–22) sale del numerador y del denominador de cada llave.",
        "frase": "«cualquier valor fuera de 0–22 (blanco al leer el CSV, por ejemplo) queda fuera de las dos listas UNO/CERO»",
    },
    {
        "decision": "Tramos de edad cerrados por ambos extremos en años enteros: 50–59, 60–69, 70–79, 80–130 (acotado por el "
                    "universo a <=120).",
        "frase": "«cuatro tramos ... 50-59, 60-69, 70-79, 80-MAS con 80-130 como cierre abierto»",
    },
    {
        "decision": "Universo y diseño se aplican antes de cualquier eje: 50 <= AGE_21 <= 120, FACTORI_21 > 0, EST_DIS_21 y "
                    "UPM_DIS_21 no vacíos (lexema tras strip).",
        "frase": "«el universo es 50 <= AGE_21 <= 120 ... Peso FACTORI_21 > 0 ... Válido: peso > 0, estrato y UPM no vacíos»",
    },
]


def num(x):
    return repr(float(x))


def carga():
    df = pd.read_csv(CSV, usecols=COLS, dtype=str, keep_default_na=False)
    for c in COLS:
        df[c] = df[c].str.strip()
    n0 = len(df)
    age = pd.to_numeric(df["AGE_21"], errors="coerce")
    w = pd.to_numeric(df["FACTORI_21"], errors="coerce")
    exc = {}
    m_edad_menor = age < 50
    m_edad_fuera = (age > 120) | age.isna()
    exc["AGE_21<50"] = int(m_edad_menor.sum())
    exc["AGE_21>120_o_no_numerico(888/999)"] = int((m_edad_fuera & ~m_edad_menor).sum())
    univ = ~m_edad_menor & ~m_edad_fuera
    m_w = ~(w > 0)
    exc["FACTORI_21<=0_o_vacio"] = int((univ & m_w).sum())
    m_dis = (df["EST_DIS_21"] == "") | (df["UPM_DIS_21"] == "")
    exc["EST_DIS_21_o_UPM_DIS_21_vacio"] = int((univ & ~m_w & m_dis).sum())
    ok = univ & ~m_w & ~m_dis
    d = pd.DataFrame({
        "age": age[ok].astype(int).values,
        "sex": pd.to_numeric(df.loc[ok, "SEX_21"], errors="coerce").values,
        "w": w[ok].astype(float).values,
        "est": pd.to_numeric(df.loc[ok, "EST_DIS_21"]).astype(int).values,
        "upm": pd.to_numeric(df.loc[ok, "UPM_DIS_21"]).astype(int).values,
        "ys": pd.to_numeric(df.loc[ok, "YRSCHOOL"], errors="coerce").values,
    })
    return d, n0, exc


def multiplicadores(d):
    """Matriz (REPLICAS, n_filas) de multiplicidades de UPM por réplica."""
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    estratos = sorted(d["est"].unique())
    upms = {h: np.array(sorted(d.loc[d["est"] == h, "upm"].unique())) for h in estratos}
    # índice (estrato, posición) de cada fila
    pos = np.empty(len(d), dtype=np.int64)
    for h in estratos:
        m = (d["est"] == h).values
        pos[m] = np.searchsorted(upms[h], d.loc[m, "upm"].values)
    M = np.empty((REPLICAS, len(d)), dtype=np.float64)
    for b0 in range(0, REPLICAS, BLOQUE):
        nb = min(BLOQUE, REPLICAS - b0)
        for h in estratos:
            nh = len(upms[h])
            m = (d["est"] == h).values
            if nh == 1:
                M[b0:b0 + nb, m] = 1.0
                continue
            draws = rng.integers(0, nh, size=(nb, nh))
            cnt = np.stack([np.bincount(r, minlength=nh) for r in draws]).astype(np.float64)
            M[b0:b0 + nb, m] = cnt[:, pos[m]]
    info = {int(h): int(len(upms[h])) for h in estratos}
    return M, info


def main():
    d, n0, exc_univ = carga()
    M, upm_por_estrato = multiplicadores(d)

    with open(ESQUEMA, newline="", encoding="utf-8") as f:
        esquema = list(csv.DictReader(f, delimiter="\t"))

    filas, diag = [], []
    for e in esquema:
        llave, unidad = e["llave"], e["unidad"]
        conducta, eje, seg = e["conducta"], e["eje"], e["segmento"]
        dg = {"llave": llave, "conducta": conducta, "eje": eje, "segmento": seg, "ola": e["ola"]}
        if conducta not in CONDUCTAS or e["ola"] != "2021" or eje not in ("TOTAL", "SEXO", "EDAD"):
            filas.append({"llave": llave, "unidad": unidad, "estado": "NO-RECALCULABLE-DESDE-SPEC",
                          "motivo": "conducta/eje/ola no definidos por la spec humana"})
            dg["motivo"] = filas[-1]["motivo"]
            diag.append(dg)
            continue
        if eje == "TOTAL":
            dom = np.ones(len(d), dtype=bool)
        elif eje == "SEXO":
            dom = (d["sex"] == SEXO[seg]).values
        else:
            lo, hi = TRAMOS_EDAD[seg]
            dom = ((d["age"] >= lo) & (d["age"] <= hi)).values
        uno, cero = CONDUCTAS[conducta]
        ys = d["ys"]
        es_uno = ys.isin(list(uno)).values
        es_cero = ys.isin(list(cero)).values
        valido = dom & (es_uno | es_cero)
        y = es_uno.astype(np.float64)
        n_dom = int(dom.sum())
        dg.update({
            "n_filas_csv": n0,
            "exclusiones_universo_diseno": exc_univ,
            "n_universo_diseno_valido": int(len(d)),
            "n_fuera_de_segmento": int(len(d) - n_dom),
            "n_segmento": n_dom,
            "exclusiones_en_segmento": {"YRSCHOOL_blanco_o_fuera_0_22": int(n_dom - valido.sum())},
            "n_valido": int(valido.sum()),
            "n_uno": int((valido & es_uno).sum()),
            "n_upm_con_casos_validos": int(d.loc[valido, "upm"].nunique()),
            "suma_pesos_validos": float(d["w"].values[valido].sum()),
        })
        w = d["w"].values * valido
        den = w.sum()
        if den <= 0:
            filas.append({"llave": llave, "unidad": unidad, "estado": "DENOMINADOR-CERO",
                          "motivo": "dominio sin casos válidos con peso positivo"})
            diag.append(dg)
            continue
        p = float((w * y).sum() / den)
        Wr = M * w  # (R, n)
        den_r = Wr.sum(axis=1)
        num_r = Wr @ y
        with np.errstate(divide="ignore", invalid="ignore"):
            rep = num_r / den_r
        degeneradas = int((~(den_r > 0) | ~np.isfinite(rep)).sum())
        dg["replicas"] = REPLICAS
        dg["replicas_degeneradas"] = degeneradas
        fila = {"llave": llave, "unidad": unidad, "estado": "RECONSTRUIDO", "punto": num(p)}
        if degeneradas > 0:
            fila["estado_ic"] = "NO-IDENTIFICADA"
            fila["motivo_ic"] = f"{degeneradas} réplica(s) bootstrap degenerada(s) (denominador cero); contrato conservador sin IC"
        else:
            lo, hi = np.percentile(rep, PCTS)
            fila.update({"estado_ic": "CALCULADO", "ic95_inf": num(lo), "ic95_sup": num(hi)})
            dg["ee_bootstrap_ddof1"] = float(np.std(rep, ddof=1))
        filas.append(fila)
        diag.append(dg)

    resultado = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
        f.write("\n")
    diagnostico = {
        "identidad": IDENTIDAD,
        "parametros": {"generador": "numpy.random.PCG64", "semilla": SEMILLA, "replicas": REPLICAS,
                       "bloque": BLOQUE, "percentiles": list(PCTS)},
        "upm_por_estrato_marco_bootstrap": upm_por_estrato,
        "llaves": diag,
        "decisiones": DECISIONES,
    }
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as f:
        json.dump(diagnostico, f, ensure_ascii=False, indent=2)
        f.write("\n")


if __name__ == "__main__":
    main()
