#!/usr/bin/env python3
"""Reconstrucción independiente CALC-ENDIREH-PISOS-2016-PAREJA-FISICA-0002.

Implementa paquete/metodo.md: prevalencia ponderada de violencia física de pareja
(unión de los nueve actos P13_1_1..9 «vida» y P13_3_1..9 «desde octubre 2015»),
universo A1/A2, ejes univariados, IC95 percentil por bootstrap de UPM dentro de
estrato (500 réplicas, semilla 20260923).

Se ejecuta desde el directorio de trabajo: python3 salida/codigo/reconstruye.py
Solo lee ./paquete/ y solo escribe en ./salida/.
"""
import csv
import hashlib
import json
import os

import numpy as np
import pandas as pd

PAQ = "paquete"
SAL = "salida"
SEMILLA = 20260923
B = 500
IDENTIDAD = {
    "paquete": "endireh-pisos-2016-pareja-fisica-0002",
    "version_entrada": "c1-ventana-v1",
    "sha256_entrada": "6ce9c8a5fdcef8473e666d9fae5b1851c31f899b06f67075f1a7fbe37222a555",
}

ACTOS_VIDA = [f"P13_1_{i}" for i in range(1, 10)]
ACTOS_REC = [f"P13_3_{i}" for i in range(1, 10)]
# Columnas autorizadas (usecols); no se lee ninguna otra.
COLS_XIII = (["ID_VIV", "ID_MUJ", "UPM", "VIV_SEL", "HOGAR"] + ACTOS_VIDA + ACTOS_REC
             + ["FAC_MUJ", "EST_DIS", "UPM_DIS", "DOMINIO", "CVE_ENT", "T_INSTRUM"])
COLS_DEM = ["ID_VIV", "ID_MUJ", "UPM", "VIV_SEL", "HOGAR", "N_REN", "EDAD", "NIV", "SEXO"]

DECISIONES = [
    {
        "tema": "Vínculo TSDem",
        "decision": "Unión 1:1 por ID_MUJ (en TSDem ID_MUJ es único por persona y coincide con el ID_MUJ de la mujer elegida del módulo XIII).",
        "frase_spec": "TSDem por `ID_MUJ` para edad `EDAD` y nivel `NIV`",
    },
    {
        "tema": "EDAD=98 (FD: «Edad no especificada en personas de 15 años o más») y EDAD=97 («97 o más años»)",
        "decision": "Ambos códigos caen numéricamente en 15–120 y se conservan en el universo. 97 se asigna a 60+. 98 no se asigna a ningún grupo de edad (edad desconocida); cuenta en los demás ejes.",
        "frase_spec": "Factor positivo, edad 15–120, A1/A2.",
    },
    {
        "tema": "NIV=99 (no especificado) y NIV=1 (preescolar)",
        "decision": "NIV 1 va a básica por la lista literal «1–3/5–6». NIV 99 o vacío no se asigna a ningún nivel de escolaridad; cuenta en los demás ejes.",
        "frase_spec": "escolaridad 0 ninguno, 1–3/5–6 básica, 4/7–8 media superior/técnica, 9–11 superior",
    },
    {
        "tema": "Unión con respuestas mixtas",
        "decision": "1 si algún acto vale 1, 2 o 3 aunque otros sean 9/blanco; 0 solo si los nueve valen 4; desconocida en cualquier otro caso. Las desconocidas salen del numerador y del denominador (proporción entre respuesta conocida).",
        "frase_spec": "Unión vale 1 si cualquier 1–3, 0 solo si los nueve son 4, desconocido en otro caso.",
    },
    {
        "tema": "Ventana reciente",
        "decision": "Acto reciente = P13_3_i, salvo que P13_1_i=4, en cuyo caso se codifica 4. Si la unión de vida es desconocida, la unión reciente es desconocida. Si P13_1_i∈{1,2,3} y P13_3_i es 9/blanco, el acto reciente es desconocido. Los valores de 13.3 no se contrastan contra la intensidad de 13.1 (p. ej. 13.1=3 con 13.3=2 se toma tal cual).",
        "frase_spec": "Si 13.1=4 un acto reciente se codifica 4 por salto; si unión 13.1 desconocida, unión reciente desconocida.",
    },
    {
        "tema": "Estimador puntual",
        "decision": "Razón ponderada sum(FAC_MUJ*y)/sum(FAC_MUJ) sobre mujeres del dominio con unión conocida.",
        "frase_spec": "factor `FAC_MUJ`",
    },
    {
        "tema": "Conjunto de UPM remuestreado",
        "decision": "UPM_DIS con al menos una mujer del universo (A1/A2, factor>0, edad 15–120), agrupadas por EST_DIS. Las mismas 500 réplicas de multiplicadores sirven para las 92 llaves; en cada dominio las UPM sin casos aportan cero.",
        "frase_spec": "Se remuestrean todas las UPM A1/A2 por estrato, incluyendo aporte cero de las que no tienen casos del dominio",
    },
    {
        "tema": "Esquema de bootstrap",
        "decision": "Bootstrap ingenuo con reemplazo: en cada estrato con n_h UPM se extraen n_h UPM con reemplazo; el peso réplica es FAC_MUJ × veces extraída. Sin reescalamiento Rao-Wu ni corrección (n_h-1)/n_h. Un estrato con una sola UPM la extrae siempre (multiplicador 1, varianza cero).",
        "frase_spec": "Se remuestrean todas las UPM A1/A2 por estrato [...] Singleton autorremuestreado aporta varianza cero.",
    },
    {
        "tema": "Generador y orden de extracción",
        "decision": "numpy.random.default_rng(20260923) (PCG64). Bucle externo réplicas 1..500, bucle interno estratos en orden numérico ascendente de EST_DIS; dentro del estrato, UPM en orden numérico ascendente de UPM_DIS; rng.integers(0, n_h, size=n_h) por estrato.",
        "frase_spec": "500 réplicas, semilla 20260923",
    },
    {
        "tema": "Percentiles",
        "decision": "numpy.percentile con método 'linear' (tipo 7 de Hyndman-Fan) sobre las réplicas finitas; réplicas con denominador cero en el dominio se descartan y se cuentan en el diagnóstico.",
        "frase_spec": "IC percentil 2.5/97.5",
    },
    {
        "tema": "CV",
        "decision": "CV = desviación estándar de las réplicas (ddof=1) / punto. Si p=0 no se evalúa CV (la regla aplica «si p>0»).",
        "frase_spec": "CV≤0.30 si p>0",
    },
    {
        "tema": "UPM con casos",
        "decision": "Número de UPM_DIS distintas con al menos una mujer del dominio con unión conocida (se informa aparte el número de UPM con al menos un caso positivo).",
        "frase_spec": "≥5 UPM con casos",
    },
    {
        "tema": "Supresión",
        "decision": "La regla de publicabilidad se evalúa y se informa en diagnostico.json; resultado.json lleva punto e IC de toda celda estimable, sin suprimir (instrucción del encargo).",
        "frase_spec": "Cada celda exige n de respuesta conocida ≥100, ≥5 UPM con casos, ancho IC≤0.20 y CV≤0.30 si p>0; se suprime si falla.",
    },
    {
        "tema": "Entidad y localidad",
        "decision": "CVE_ENT y DOMINIO del módulo XIII (no de TSDem).",
        "frase_spec": "localidad `DOMINIO` U/C/R, A1/A2 y entidad 01–32",
    },
]


def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def union(codigos):
    """codigos: array (n, 9) de strings. Devuelve float: 1, 0 o NaN."""
    pos = np.isin(codigos, ["1", "2", "3"]).any(axis=1)
    neg = (codigos == "4").all(axis=1)
    out = np.full(codigos.shape[0], np.nan)
    out[neg] = 0.0
    out[pos] = 1.0
    return out


def grupo_edad(e):
    if not np.isfinite(e) or e == 98:
        return None
    e = int(e)
    if 15 <= e <= 29:
        return "15-29"
    if 30 <= e <= 44:
        return "30-44"
    if 45 <= e <= 59:
        return "45-59"
    if e >= 60:
        return "60+"
    return None


NIV_MAP = {0: "ninguno", 1: "basica", 2: "basica", 3: "basica", 5: "basica", 6: "basica",
           4: "media_superior", 7: "media_superior", 8: "media_superior",
           9: "superior", 10: "superior", 11: "superior"}


def main():
    # --- Metadatos del paquete: verificación de hashes del manifiesto ---
    manifiesto = json.load(open(os.path.join(PAQ, "manifiesto.json"), encoding="utf-8"))
    verif_manifiesto = {k: (sha256(os.path.join(PAQ, k)) == v) for k, v in manifiesto["archivos"].items()}
    sha_manifiesto = sha256(os.path.join(PAQ, "manifiesto.json"))

    with open(os.path.join(PAQ, "estimandos.tsv"), encoding="utf-8", newline="") as f:
        estimandos = list(csv.DictReader(f, delimiter="\t"))

    # --- Microdato: solo columnas autorizadas ---
    x = pd.read_csv(os.path.join(PAQ, "datos", "TB_SEC_XIII.csv"), usecols=COLS_XIII,
                    dtype=str, keep_default_na=False)
    d = pd.read_csv(os.path.join(PAQ, "datos", "TSDem.csv"), usecols=COLS_DEM,
                    dtype=str, keep_default_na=False)
    for c in ACTOS_VIDA + ACTOS_REC + ["T_INSTRUM", "DOMINIO", "CVE_ENT"]:
        x[c] = x[c].str.strip()
    m = x.merge(d[["ID_MUJ", "EDAD", "NIV", "SEXO"]], on="ID_MUJ", how="left", validate="1:1")
    conteos = {"filas_TB_SEC_XIII": int(len(x)), "filas_TSDem": int(len(d)),
               "sin_vinculo_TSDem": int(m["EDAD"].isna().sum())}

    m["fac"] = pd.to_numeric(m["FAC_MUJ"], errors="coerce")
    m["edad"] = pd.to_numeric(m["EDAD"], errors="coerce")
    m["niv"] = pd.to_numeric(m["NIV"], errors="coerce")
    univ = (m["T_INSTRUM"].isin(["A1", "A2"]) & (m["fac"] > 0)
            & m["edad"].between(15, 120))
    conteos["A1A2"] = int(m["T_INSTRUM"].isin(["A1", "A2"]).sum())
    conteos["universo"] = int(univ.sum())
    u = m[univ].reset_index(drop=True)
    conteos["universo_EDAD_97"] = int((u["edad"] == 97).sum())
    conteos["universo_EDAD_98"] = int((u["edad"] == 98).sum())
    conteos["universo_NIV_no_asignado"] = int((~u["niv"].isin(list(NIV_MAP))).sum())
    conteos["universo_SEXO"] = {k: int(v) for k, v in u["SEXO"].value_counts().items()}

    # --- Recodificación ---
    v = u[ACTOS_VIDA].to_numpy()
    r = u[ACTOS_REC].to_numpy().copy()
    r[v == "4"] = "4"  # salto: acto no ocurrido en la vida => no ocurrido en ventana reciente
    y_vida = union(v)
    y_rec = union(r)
    y_rec[np.isnan(y_vida)] = np.nan
    conteos["vida_conocida"] = int(np.isfinite(y_vida).sum())
    conteos["vida_desconocida"] = int(np.isnan(y_vida).sum())
    conteos["reciente_conocida"] = int(np.isfinite(y_rec).sum())
    conteos["reciente_desconocida"] = int(np.isnan(y_rec).sum())

    # --- Ejes ---
    u["g_edad"] = [grupo_edad(e) for e in u["edad"]]
    u["g_esc"] = u["niv"].map(NIV_MAP)
    ejes = {
        "nacional": np.full(len(u), "MX", dtype=object),
        "edad": u["g_edad"].to_numpy(dtype=object),
        "escolaridad": u["g_esc"].to_numpy(dtype=object),
        "localidad": u["DOMINIO"].to_numpy(dtype=object),
        "pareja": u["T_INSTRUM"].to_numpy(dtype=object),
        "entidad": u["CVE_ENT"].to_numpy(dtype=object),
    }

    # --- Diseño: UPM por estrato, multiplicadores bootstrap ---
    est = pd.to_numeric(u["EST_DIS"]).to_numpy()
    upm = pd.to_numeric(u["UPM_DIS"]).to_numpy()
    tabla_upm = pd.DataFrame({"est": est, "upm": upm}).drop_duplicates()
    assert tabla_upm["upm"].is_unique, "UPM_DIS en más de un estrato"
    tabla_upm = tabla_upm.sort_values(["est", "upm"]).reset_index(drop=True)
    idx_upm = pd.Series(np.arange(len(tabla_upm)), index=tabla_upm["upm"].to_numpy())
    obs_upm = idx_upm.loc[upm].to_numpy()
    estratos = []
    for h, grp in tabla_upm.groupby("est", sort=True):
        estratos.append(grp.index.to_numpy())
    n_h = np.array([len(s) for s in estratos])
    conteos["estratos"] = int(len(estratos))
    conteos["upm"] = int(len(tabla_upm))
    conteos["estratos_singleton"] = int((n_h == 1).sum())

    rng = np.random.default_rng(SEMILLA)
    mult = np.zeros((B, len(tabla_upm)), dtype=np.float64)
    for b in range(B):
        for s in estratos:
            k = len(s)
            draws = rng.integers(0, k, size=k)
            mult[b, s] = np.bincount(draws, minlength=k)

    fac = u["fac"].to_numpy(dtype=float)

    def estima(y, dom):
        ok = dom & np.isfinite(y)
        n = int(ok.sum())
        if n == 0:
            return None
        w = fac[ok]
        yy = y[ok]
        den = w.sum()
        p = float((w * yy).sum() / den)
        # agregados por UPM (dominio conocido); las demás UPM aportan cero
        num_u = np.bincount(obs_upm[ok], weights=w * yy, minlength=len(tabla_upm))
        den_u = np.bincount(obs_upm[ok], weights=w, minlength=len(tabla_upm))
        num_b = mult @ num_u
        den_b = mult @ den_u
        with np.errstate(invalid="ignore", divide="ignore"):
            rep = np.where(den_b > 0, num_b / den_b, np.nan)
        fin = rep[np.isfinite(rep)]
        lo, hi = np.percentile(fin, [2.5, 97.5], method="linear")
        sd = float(np.std(fin, ddof=1))
        upm_casos = int(np.unique(obs_upm[ok]).size)
        upm_pos = int(np.unique(obs_upm[ok][yy == 1]).size)
        return {"p": p, "lo": float(lo), "hi": float(hi), "n": n, "upm": upm_casos,
                "upm_pos": upm_pos, "sd": sd, "rep": rep, "rep_nan": int(np.isnan(rep).sum()),
                "n_pos": int((yy == 1).sum()), "suma_fac": float(den)}

    filas, diag_filas, replicas = [], [], {}
    for e in estimandos:
        llave, unidad = e["llave"], e["unidad"]
        eje, seg, ven = e["eje"], e["segmento"], e["ventana"]
        y = y_vida if ven == "vida" else y_rec if ven == "desde_octubre_2015" else None
        if y is None or eje not in ejes:
            filas.append({"llave": llave, "unidad": unidad, "estado": "NO-RECALCULABLE-DESDE-SPEC",
                          "motivo": f"eje '{eje}' o ventana '{ven}' no definidos en metodo.md"})
            diag_filas.append({"llave": llave, "estado": "NO-RECALCULABLE-DESDE-SPEC"})
            continue
        dom = ejes[eje] == seg
        res = estima(y, dom)
        if res is None:
            filas.append({"llave": llave, "unidad": unidad, "estado": "DENOMINADOR-CERO",
                          "motivo": f"sin mujeres con respuesta conocida en {eje}={seg}, ventana {ven}"})
            diag_filas.append({"llave": llave, "estado": "DENOMINADOR-CERO", "n": 0})
            continue
        filas.append({"llave": llave, "unidad": unidad, "estado": "RECONSTRUIDO",
                      "punto": repr(float(res["p"])), "estado_ic": "CALCULADO",
                      "ic95_inf": repr(float(res["lo"])), "ic95_sup": repr(float(res["hi"]))})
        ancho = res["hi"] - res["lo"]
        cv = res["sd"] / res["p"] if res["p"] > 0 else None
        fallas = []
        if res["n"] < 100:
            fallas.append("n<100")
        if res["upm"] < 5:
            fallas.append("UPM<5")
        if ancho > 0.20:
            fallas.append("ancho>0.20")
        if cv is not None and cv > 0.30:
            fallas.append("CV>0.30")
        diag_filas.append({
            "llave": llave, "eje": eje, "segmento": seg, "ventana": ven,
            "estado": "RECONSTRUIDO",
            "n": res["n"], "n_positivos": res["n_pos"], "suma_FAC_MUJ": repr(res["suma_fac"]),
            "upm_con_casos": res["upm"], "upm_con_positivos": res["upm_pos"],
            "ancho_ic": repr(float(ancho)), "ee_bootstrap": repr(res["sd"]),
            "cv": None if cv is None else repr(float(cv)),
            "replicas_descartadas_denominador_cero": res["rep_nan"],
            "publicable": not fallas, "fallas_publicabilidad": fallas,
        })
        replicas[llave] = [None if not np.isfinite(t) else repr(float(t)) for t in res["rep"]]

    resultado = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    diagnostico = {
        "identidad": IDENTIDAD,
        "sha256_manifiesto": sha_manifiesto,
        "manifiesto_hashes_coinciden": verif_manifiesto,
        "conteos_agregados": conteos,
        "parametros": {"replicas": B, "semilla": SEMILLA, "generador": "numpy.random.default_rng (PCG64)",
                       "percentiles": [2.5, 97.5], "numpy": np.__version__, "pandas": pd.__version__},
        "decisiones": DECISIONES,
        "filas": diag_filas,
    }
    os.makedirs(SAL, exist_ok=True)
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=1)
        f.write("\n")
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as f:
        json.dump(diagnostico, f, ensure_ascii=False, indent=1)
        f.write("\n")
    # Réplicas agregadas por llave, sin identificadores de UPM ni de persona.
    with open(os.path.join(SAL, "replicas.json"), "w", encoding="utf-8") as f:
        json.dump(replicas, f, ensure_ascii=False)
        f.write("\n")
    print(json.dumps(conteos, ensure_ascii=False))
    print("filas:", len(filas), {s: sum(1 for r in filas if r["estado"] == s) for s in {r["estado"] for r in filas}})
    print("publicables:", sum(1 for r in diag_filas if r.get("publicable")))


if __name__ == "__main__":
    main()
