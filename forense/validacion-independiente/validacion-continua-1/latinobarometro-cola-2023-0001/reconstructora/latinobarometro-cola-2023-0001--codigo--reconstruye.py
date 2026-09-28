#!/usr/bin/env python3
"""Reconstrucción independiente de CALC-LATINOBAROMETRO-COLA-2023-0001 desde paquete/docs/spec-humana.md.

Uso (desde el directorio de trabajo): python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json y salida/diagnostico.json.
"""
import csv
import json
import os

import numpy as np
import pandas as pd

PAQ = "paquete"
OUT = "salida"
DTA = os.path.join(PAQ, "datos", "latinobarometro2023_esp.dta")
ESQUEMA = os.path.join(PAQ, "esquema-identidades.tsv")

IDENTIDAD = {
    "paquete": "latinobarometro-cola-2023-0001",
    "version_entrada": "validacion-continua-1",
    "sha256_entrada": "06c601418c4d5527fe51e70762a771ec605b223ad6ebd3d7f0286093ea6a94c2",
}

# Columnas autorizadas (únicas que se leen del microdato).
COLS = ["idenpa", "wt", "edad", "sexo", "REEEDUC_1", "tamciud", "S2",
        "P1ST", "P11STGBS_A", "P15STGBS", "P13ST_E"]

# spec §2: regla ("bin", columna, [UNO], [CERO])
C4 = ([1, 2], [3, 4])
CONDUCTAS = {
    "satisfecho-con-la-vida": ("P1ST", [1, 2], [3, 4]),
    "satisfecho-con-la-democracia": ("P11STGBS_A", [1, 2], [3, 4]),
    "aprueba-gobierno-del-presidente": ("P15STGBS", [1], [2]),
    "oro-confia-gobierno": ("P13ST_E", C4[0], C4[1]),
}

# spec §3: ejes
EJES = {
    "TOTAL": (None, {"TODOS": None}),
    "SEXO": ("sexo", {"HOMBRE": [1], "MUJER": [2]}),
    "EDAD": ("edad", {"18-29": (18, 29), "30-44": (30, 44), "45-59": (45, 59), "60-MAS": (60, None)}),
    "ESCOLARIDAD": ("REEEDUC_1", {"HASTA-BASICA": [1, 2, 3], "MEDIA": [4, 5], "SUPERIOR": [6, 7]}),
    "TAMLOC": ("tamciud", {"MENOS-20MIL": [1, 2, 3], "20MIL-100MIL": [4, 5, 6], "100MIL-MAS": [7, 8]}),
    "CLASE-SUBJETIVA": ("S2", {"ALTA-MEDIA-ALTA": [1, 2], "MEDIA": [3], "MEDIA-BAJA": [4], "BAJA": [5]}),
}

# spec §4
SEED = 20260928
REPS = 2000
BLOQUE = 50
PCT = (2.5, 97.5)

DECISIONES = [
    {"id": "D1-remuestreo",
     "frase": "bootstrap ponderado de entrevistas (sin estrato ni UPM declarados: cada entrevista es su propia UPM, un solo estrato",
     "decision": "Cada réplica extrae n entrevistas con reemplazo (n = entrevistas válidas para el diseño) del único estrato; "
                 "peso de réplica = wt * (veces extraída). Sin reescalado Rao-Wu (n-1)."},
    {"id": "D2-rng-bloques",
     "frase": "numpy.PCG64(20260928), 2000 réplicas, bloques de 50",
     "decision": "Un solo numpy.random.Generator(PCG64(20260928)); 40 bloques sucesivos de 50 réplicas; en cada bloque "
                 "rng.integers(0, n, size=(50, n)) y conteos por bincount. Las mismas 2000 réplicas se usan para las 68 llaves."},
    {"id": "D3-percentiles",
     "frase": "percentiles 2.5/97.5",
     "decision": "numpy.percentile con interpolación lineal (default) sobre las 2000 razones replicadas."},
    {"id": "D4-degenerada",
     "frase": "contrato conservador — una réplica degenerada da EE/IC vacíos",
     "decision": "Si en alguna réplica el denominador del dominio (suma de pesos de réplica con conducta válida) es 0, "
                 "IC vacío: estado_ic NO-IDENTIFICADA, manteniendo el punto."},
    {"id": "D5-marco",
     "frase": "toda conducta fuera de universo sale NaN",
     "decision": "El marco del bootstrap son las entrevistas de México con wt finito > 0; el universo (edad >= 18) se "
                 "aplica volviendo NaN la conducta, no quitando filas del marco (en México no hay menores de 18)."},
    {"id": "D6-denominador",
     "frase": "Razón ponderada Σw·y/Σw ... fuera de la lista cerrada queda NaN",
     "decision": "Σw y Σw·y sólo sobre filas del dominio con y no NaN (códigos fuera de UNO/CERO excluidos del denominador)."},
    {"id": "D7-edad",
     "frase": "cuatro tramos: 18-29, 30-44, 45-59, 60-MAS",
     "decision": "Tramos cerrados por edad entera en años cumplidos; 60-MAS = edad >= 60."},
    {"id": "D8-segmento-invalido",
     "frase": "CLASE-SUBJETIVA (S2 ...: 1 Alta · 2 Media Alta · 3 Media · 4 Media Baja · 5 Baja",
     "decision": "Códigos del eje fuera de las listas (p. ej. S2 negativos) no pertenecen a ningún segmento; siguen en TOTAL."},
]


def lee():
    d = pd.read_stata(DTA, columns=COLS, convert_categoricals=False)
    n_archivo = len(d)
    d = d[pd.to_numeric(d["idenpa"], errors="coerce") == 484].copy()
    n_pais = len(d)
    for c in COLS:
        d[c] = pd.to_numeric(d[c], errors="coerce").astype(float)
    wt = d["wt"].to_numpy()
    valido = np.isfinite(wt) & (wt > 0)
    excl_wt = int((~valido).sum())
    d = d[valido].reset_index(drop=True)
    return d, {"filas_archivo": n_archivo, "filas_mexico": n_pais,
               "excluidas_wt_no_valido": excl_wt, "marco_diseno": len(d)}


def recodifica(x, uno, cero):
    y = np.full(len(x), np.nan)
    y[np.isin(x, uno)] = 1.0
    y[np.isin(x, cero)] = 0.0
    return y


def mascara_segmento(d, eje, seg):
    col, segs = EJES[eje]
    if col is None:
        return np.ones(len(d), dtype=bool)
    regla = segs[seg]
    x = d[col].to_numpy()
    if eje == "EDAD":
        lo, hi = regla
        m = np.isfinite(x) & (x >= lo)
        if hi is not None:
            m &= x <= hi
        return m
    return np.isin(x, regla)


def replicas(n):
    rng = np.random.Generator(np.random.PCG64(SEED))
    cuentas = np.empty((REPS, n), dtype=np.float64)
    for b in range(REPS // BLOQUE):
        idx = rng.integers(0, n, size=(BLOQUE, n))
        for j in range(BLOQUE):
            cuentas[b * BLOQUE + j] = np.bincount(idx[j], minlength=n)
    return cuentas


def fmt(x):
    return repr(float(x))


def main():
    d, cab = lee()
    n = len(d)
    w = d["wt"].to_numpy()
    universo = np.isfinite(d["edad"].to_numpy()) & (d["edad"].to_numpy() >= 18)
    cuentas = replicas(n)
    W = cuentas * w[None, :]

    with open(ESQUEMA, newline="", encoding="utf-8") as fh:
        esquema = list(csv.DictReader(fh, delimiter="\t"))

    filas, diag = [], []
    for r in esquema:
        llave, unidad = r["llave"], r["unidad"]
        conducta, eje, seg, ola = r["conducta"], r["eje"], r["segmento"], r["ola"]
        dg = {"llave": llave, "conducta": conducta, "eje": eje, "segmento": seg, "ola": ola}
        if ola != "2023" or conducta not in CONDUCTAS or eje not in EJES or seg not in EJES[eje][1]:
            filas.append({"llave": llave, "unidad": unidad, "estado": "NO-RECALCULABLE-DESDE-SPEC",
                          "motivo": "conducta/eje/segmento/ola no definidos en la spec humana"})
            dg["nota"] = "no definido en spec"
            diag.append(dg)
            continue
        col, uno, cero = CONDUCTAS[conducta]
        x = d[col].to_numpy()
        y = recodifica(x, uno, cero)
        y[~universo] = np.nan
        seg_m = mascara_segmento(d, eje, seg)
        yv = np.isfinite(y)
        dom = seg_m & yv
        dg.update({
            "marco_diseno": n,
            "en_segmento": int(seg_m.sum()),
            "excluidas_fuera_universo_en_segmento": int((seg_m & ~universo).sum()),
            "excluidas_codigo_fuera_de_UNO_CERO_en_segmento": int((seg_m & universo & ~yv).sum()),
            "codigos_excluidos_en_segmento": {str(int(k)): int(v) for k, v in
                                               pd.Series(x[seg_m & universo & ~yv]).value_counts().sort_index().items()},
            "n_valido": int(dom.sum()),
            "suma_w_valido": fmt(w[dom].sum()),
        })
        den = w[dom].sum()
        if dom.sum() == 0 or den <= 0:
            filas.append({"llave": llave, "unidad": unidad, "estado": "DENOMINADOR-CERO",
                          "motivo": "dominio sin entrevistas válidas (Σw = 0) bajo la spec"})
            diag.append(dg)
            continue
        p = float((w[dom] * y[dom]).sum() / den)
        yz = np.where(dom, y, 0.0)
        den_r = W @ dom.astype(float)
        num_r = W @ yz
        degeneradas = int((den_r <= 0).sum())
        dg["replicas_degeneradas"] = degeneradas
        fila = {"llave": llave, "unidad": unidad, "estado": "RECONSTRUIDO", "punto": fmt(p)}
        if degeneradas > 0:
            fila["estado_ic"] = "NO-IDENTIFICADA"
            fila["motivo_ic"] = (f"{degeneradas} de {REPS} réplicas bootstrap degeneradas (denominador 0); "
                                 "la spec fija contrato conservador: IC vacío")
        else:
            pr = num_r / den_r
            lo, hi = np.percentile(pr, PCT)
            fila["estado_ic"] = "CALCULADO"
            fila["ic95_inf"] = fmt(lo)
            fila["ic95_sup"] = fmt(hi)
            dg["ee_bootstrap"] = fmt(np.std(pr, ddof=1))
        filas.append(fila)
        diag.append(dg)

    res = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open(os.path.join(OUT, "resultado.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    out_diag = {
        "identidad": IDENTIDAD,
        "filtro": "idenpa = 484; universo edad >= 18; válido wt finito > 0",
        "conteos_marco": cab,
        "excluidas_edad_menor_18_en_marco": int((~universo).sum()),
        "diseno": "MAS-PONDERADO-SIN-ESTRATO (bootstrap ponderado de entrevistas)",
        "bootstrap": {"generador": f"numpy.random.Generator(PCG64({SEED}))", "replicas": REPS,
                      "bloque": BLOQUE, "percentiles": list(PCT)},
        "decisiones": DECISIONES,
        "llaves": diag,
    }
    with open(os.path.join(OUT, "diagnostico.json"), "w", encoding="utf-8") as fh:
        json.dump(out_diag, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    main()
