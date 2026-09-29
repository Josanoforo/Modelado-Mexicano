"""Reconstrucción independiente CALC-ENVIPE-PERCEPCION-2024-0001 desde paquete/docs/spec-humana.md.

Uso (desde el directorio de trabajo): python3 salida/codigo/reconstruye.py
Lee solo columnas autorizadas; escribe salida/resultado.json y salida/diagnostico.json.
"""
import csv
import json
import os

import numpy as np
import pandas as pd

PAQ = "paquete"
SAL = "salida"

IDENTIDAD = {
    "paquete": "envipe-percepcion-2024-0001",
    "version_entrada": "validacion-continua-1",
    "sha256_entrada": "b20ad44c388d54eba682aafa83cbc736047e0a17705321915ff456cdf77dadaf",
}

COLS_TPER = ["ID_PER", "AP4_3_3", "AP4_4_A", "AP4_10_02", "EDAD", "SEXO", "DOMINIO",
             "CVE_ENT", "FAC_ELE", "EST_DIS", "UPM_DIS"]
COLS_TSDEM = ["ID_PER", "NIV"]

# spec §4
SEMILLA = 20261003
REPLICAS = 2000
BLOQUE = 50

# spec §2: variable, códigos UNO, códigos CERO
CONDUCTAS = {
    "estado-inseguro": ("AP4_3_3", {"2"}, {"1"}),
    "inseguro-caminar-de-noche": ("AP4_4_A", {"3", "4"}, {"1", "2"}),
    "dejo-permitir-menores-salir-solos": ("AP4_10_02", {"1"}, {"2"}),
}

# spec §3
NIV_A_SEG = {"00": "HASTA-PRIMARIA", "01": "HASTA-PRIMARIA", "02": "HASTA-PRIMARIA",
             "03": "SECUNDARIA", "04": "SECUNDARIA", "05": "SECUNDARIA",
             "06": "MEDIA-SUPERIOR", "07": "MEDIA-SUPERIOR",
             "08": "SUPERIOR", "09": "SUPERIOR"}
SEXO_A_SEG = {"1": "HOMBRE", "2": "MUJER"}
DOM_A_SEG = {"U": "URBANO", "C": "COMPLEMENTO-URBANO", "R": "RURAL"}


def lee_csv(ruta, cols):
    # Los CSV del paquete usan CR como terminador de línea.
    return pd.read_csv(ruta, usecols=cols, dtype=str, keep_default_na=False,
                       lineterminator="\r", encoding="utf-8")


def seg_edad(e):
    s = pd.Series(pd.NA, index=e.index, dtype="object")
    s[(e >= 18) & (e <= 29)] = "18-29"
    s[(e >= 30) & (e <= 44)] = "30-44"
    s[(e >= 45) & (e <= 59)] = "45-59"
    s[(e >= 60)] = "60-MAS"
    return s


def rfloat(x):
    return repr(float(x))


def main():
    esquema = pd.read_csv(os.path.join(PAQ, "esquema-identidades.tsv"), sep="\t", dtype=str,
                          keep_default_na=False)

    t = lee_csv(os.path.join(PAQ, "datos", "tper_vic1.csv"), COLS_TPER)
    s = lee_csv(os.path.join(PAQ, "datos", "tsdem.csv"), COLS_TSDEM)
    for c in t.columns:
        t[c] = t[c].str.strip()
    s["ID_PER"] = s["ID_PER"].str.strip()
    s["NIV"] = s["NIV"].str.strip()

    diag_global = {"filas_tper_vic1": int(len(t)), "filas_tsdem": int(len(s))}

    # Diseño válido: peso > 0, estrato y UPM no vacíos
    w = pd.to_numeric(t["FAC_ELE"], errors="coerce")
    valido = (w > 0) & (t["EST_DIS"] != "") & (t["UPM_DIS"] != "")
    diag_global["excl_diseno_invalido"] = int((~valido).sum())
    diag_global["FILAS-DISENO-VALIDO"] = int(valido.sum())
    t = t[valido].copy()
    t["w"] = w[valido].astype(float)

    # Unión NIV: deduplicar tsdem por ID_PER (primera aparición), left join
    n_dup = int(s["ID_PER"].duplicated().sum())
    s = s.drop_duplicates("ID_PER", keep="first")
    diag_global["tsdem_id_per_duplicados_descartados"] = n_dup
    t = t.merge(s, on="ID_PER", how="left", validate="one_to_one")
    diag_global["FILAS-CON-NIV"] = int(t["NIV"].notna().sum())
    diag_global["filas_sin_pareja_tsdem"] = int(t["NIV"].isna().sum())

    # Universo
    edad = pd.to_numeric(t["EDAD"], errors="coerce")
    universo = (edad >= 18) & (edad <= 97)
    diag_global["excl_fuera_universo_edad"] = int((~universo).sum())
    diag_global["excl_fuera_universo_edad_por_codigo"] = {
        str(k): int(v) for k, v in t.loc[~universo, "EDAD"].value_counts().sort_index().items()}
    diag_global["filas_universo"] = int(universo.sum())

    # Estructura de UPM; segmentos por eje (uno a la vez) sobre el orden final
    t = t.sort_values(["EST_DIS", "UPM_DIS"], kind="mergesort").reset_index(drop=True)
    edad = pd.to_numeric(t["EDAD"], errors="coerce")
    universo = ((edad >= 18) & (edad <= 97)).to_numpy()
    segs = {
        "TOTAL": pd.Series("TODOS", index=t.index, dtype="object"),
        "SEXO": t["SEXO"].map(SEXO_A_SEG),
        "EDAD": seg_edad(edad),
        "ESCOLARIDAD": t["NIV"].map(NIV_A_SEG),
        "DOMINIO": t["DOMINIO"].map(DOM_A_SEG),
        "ENTIDAD": t["CVE_ENT"].where(t["CVE_ENT"].isin([f"{i:02d}" for i in range(1, 33)])),
    }
    upm_tab = t[["EST_DIS", "UPM_DIS"]].drop_duplicates().reset_index(drop=True)
    upm_tab["u"] = np.arange(len(upm_tab))
    t = t.merge(upm_tab, on=["EST_DIS", "UPM_DIS"], how="left")
    n_upm = len(upm_tab)
    estratos = []  # (índices de UPM del estrato, n_h) en orden de EST_DIS
    for est, g in upm_tab.groupby("EST_DIS", sort=True):
        estratos.append((est, g["u"].to_numpy()))
    diag_global["n_estratos"] = len(estratos)
    diag_global["n_upm"] = int(n_upm)
    diag_global["n_estratos_upm_unica_certeza"] = int(sum(1 for _, u in estratos if len(u) == 1))

    u_idx = t["u"].to_numpy()
    wv = t["w"].to_numpy()

    # Construye, por llave, vectores por UPM de numerador y denominador
    filas_llave = []
    num_mat = np.zeros((n_upm, len(esquema)))
    den_mat = np.zeros((n_upm, len(esquema)))
    diag_llaves = {}
    for j, r in esquema.iterrows():
        var, unos, ceros = CONDUCTAS[r["conducta"]]
        codigo = t[var]
        y_def = codigo.isin(unos | ceros).to_numpy()
        y = codigo.isin(unos).to_numpy().astype(float)
        seg = segs[r["eje"]]
        en_seg = (seg == r["segmento"]).fillna(False).to_numpy()
        base = universo & en_seg
        dom = base & y_def
        num_mat[:, j] = np.bincount(u_idx[dom], weights=(wv * y)[dom], minlength=n_upm)
        den_mat[:, j] = np.bincount(u_idx[dom], weights=wv[dom], minlength=n_upm)
        excl_cod = codigo[base & ~y_def].replace("", "(blanco)").value_counts().sort_index()
        d = {
            "conducta": r["conducta"], "eje": r["eje"], "segmento": r["segmento"],
            "variable": var,
            "n_valido": int(dom.sum()),
            "n_uno": int((dom & (y == 1)).sum()),
            "suma_pesos_denominador": rfloat(wv[dom].sum()),
            "n_upm_con_casos": int((den_mat[:, j] > 0).sum()),
            "n_segmento_en_universo": int(base.sum()),
            "exclusiones": {
                "diseno_invalido_global": diag_global["excl_diseno_invalido"],
                "fuera_universo_edad_global": diag_global["excl_fuera_universo_edad"],
                "respuesta_fuera_de_UNO_CERO_en_segmento": {str(k): int(v) for k, v in excl_cod.items()},
            },
        }
        if r["eje"] == "ESCOLARIDAD":
            sin_niv = universo & t["NIV"].isna().to_numpy()
            niv_no_clas = universo & t["NIV"].notna().to_numpy() & ~t["NIV"].isin(NIV_A_SEG.keys()).to_numpy()
            d["exclusiones"]["eje_sin_pareja_tsdem_global_universo"] = int(sin_niv.sum())
            d["exclusiones"]["eje_niv_no_clasificable_global_universo"] = {
                (k if k != "" else "(blanco)"): int(v)
                for k, v in t.loc[niv_no_clas, "NIV"].value_counts().sort_index().items()}
        diag_llaves[r["llave"]] = d

    punto_num = num_mat.sum(axis=0)
    punto_den = den_mat.sum(axis=0)

    # Bootstrap de UPM dentro de estrato
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    reps = np.empty((REPLICAS, len(esquema)))
    rep_den_min = np.full(len(esquema), np.inf)
    for b0 in range(0, REPLICAS, BLOQUE):
        nb = min(BLOQUE, REPLICAS - b0)
        mult = np.zeros((nb, n_upm))
        for _, us in estratos:
            nh = len(us)
            if nh == 1:
                mult[:, us] = 1.0  # UPM de certeza
                continue
            draws = rng.integers(0, nh, size=(nb, nh))
            cnt = np.zeros((nb, nh))
            np.add.at(cnt, (np.repeat(np.arange(nb), nh), draws.ravel()), 1.0)
            mult[:, us] = cnt
        rn = mult @ num_mat
        rd = mult @ den_mat
        rep_den_min = np.minimum(rep_den_min, rd.min(axis=0))
        with np.errstate(invalid="ignore", divide="ignore"):
            reps[b0:b0 + nb] = np.where(rd > 0, rn / rd, np.nan)

    filas = []
    for j, r in esquema.iterrows():
        llave = r["llave"]
        d = diag_llaves[llave]
        fila = {"llave": llave, "unidad": r["unidad"]}
        if punto_den[j] <= 0:
            fila["estado"] = "DENOMINADOR-CERO"
            fila["motivo"] = "Dominio observado sin casos válidos (suma de pesos del denominador = 0)."
            d["estado"] = fila["estado"]
            filas.append(fila)
            continue
        p = punto_num[j] / punto_den[j]
        fila["estado"] = "RECONSTRUIDO"
        fila["punto"] = rfloat(p)
        rj = reps[:, j]
        n_deg = int(np.isnan(rj).sum())
        d["replicas_degeneradas"] = n_deg
        if n_deg > 0:
            fila["estado_ic"] = "NO-IDENTIFICADA"
            fila["motivo_ic"] = (f"{n_deg} de {REPLICAS} réplicas bootstrap degeneradas (denominador cero en el "
                                 "dominio); contrato conservador de la spec §4: sin EE ni IC.")
        else:
            lo, hi = np.percentile(rj, [2.5, 97.5])
            fila["estado_ic"] = "CALCULADO"
            fila["ic95_inf"] = rfloat(lo)
            fila["ic95_sup"] = rfloat(hi)
            d["ee_bootstrap"] = rfloat(np.std(rj, ddof=1))
        d["estado"] = fila["estado"]
        d["estado_ic"] = fila["estado_ic"]
        filas.append(fila)

    res = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "decisiones.json"), encoding="utf-8") as fh:
        decisiones = json.load(fh)
    diag = {
        "identidad": IDENTIDAD,
        "parametros": {"semilla": f"numpy.PCG64({SEMILLA})", "replicas": REPLICAS, "bloque": BLOQUE,
                       "percentiles": [2.5, 97.5]},
        "global": diag_global,
        "decisiones_implementacion": decisiones,
        "llaves": diag_llaves,
    }
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as fh:
        json.dump(diag, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main()
