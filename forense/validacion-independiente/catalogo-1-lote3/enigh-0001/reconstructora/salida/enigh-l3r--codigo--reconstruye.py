#!/usr/bin/env python3
"""Reconstrucción independiente ENIGH 2022 · A-P-COMPLEMENTO (hogares sin remesas).

Punto: paquete/enigh-complemento-restaurado.md
IC:    paquete/residuales-p3-contrato-ic.md + paquete/residuales-p3-modulos-ic.md
Salida: paquete/CONTRATO-v3.md (version 3)

Ejecutar desde el directorio de trabajo: python3 salida/codigo/reconstruye.py
"""
import csv
import hashlib
import json
import math
import os
import platform
import re
import subprocess
import sys

import numpy as np
import pandas as pd

PAQ = "paquete"
SAL = "salida"
CSV = os.path.join(PAQ, "datos", "concentradohogar_enigh2022_ns.csv")
ESQUEMA = os.path.join(PAQ, "esquema-identidades.tsv")
CONTRATO_IC = os.path.join(PAQ, "residuales-p3-contrato-ic.md")
MODULOS_IC = os.path.join(PAQ, "residuales-p3-modulos-ic.md")

# Columnas autorizadas (encargo, límites de acceso). No se lee ninguna otra.
USECOLS = ["folioviv", "foliohog", "factor", "remesas", "est_dis", "upm"]

IDENTIDAD = {
    "paquete": "enigh-0001",
    "version_entrada": "residuales-documentales-v2",
    "sha256_entrada": "b03e4c59c8a8a88b76d4021f189fca9073ce4cc9057d66ec1fbecbc3d5236c13",
}

B = 2000
SEMILLA = 20260923
Q_INF, Q_SUP = 0.025, 0.975

# Número decimal estricto (sin espacios, sin notación especial).
RE_DEC = re.compile(r"^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$")


def sha256_archivo(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def num(x):
    return repr(float(x))


def parse_estricto(s):
    """Devuelve (estado, valor): 'nulo', 'no_numerico' o 'ok'."""
    if s == "":
        return "nulo", None
    if not RE_DEC.match(s):
        return "no_numerico", None
    return "ok", float(s)


def seq_sum(valores):
    """Suma float64 secuencial en el orden dado."""
    tot = 0.0
    for v in valores:
        tot += float(v)
    return tot


def cuantil_tipo7(t_ordenadas, q):
    n = len(t_ordenadas)
    a = (n - 1) * q
    j = int(math.floor(a))
    if j >= n - 1:
        return float(t_ordenadas[n - 1])
    return float((1 - a + j) * t_ordenadas[j] + (a - j) * t_ordenadas[j + 1])


def escribir_entorno():
    ruta = os.path.join(SAL, "entorno.txt")
    uname = subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout.strip()
    lineas = [
        f"python {sys.version.split()[0]} ({sys.version})",
        f"numpy {np.__version__}",
        f"pandas {pd.__version__}",
        "lector: pandas.read_csv (motor C, dtype=str, keep_default_na=False, encoding=utf-8-sig); pyreadstat/dbfread no usados",
        f"platform {platform.platform()}",
        f"uname -a: {uname}",
    ]
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    return sha256_archivo(ruta)


def cargar_esquema():
    with open(ESQUEMA, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def reconstruir_llave(fila_esq, hash_contrato, hash_entorno):
    llave, unidad = fila_esq["llave"], fila_esq["unidad"]
    diag = {"llave": llave, "unidad": unidad, "celda": fila_esq["celda"],
            "conducta": fila_esq["conducta"], "segmento": fila_esq["segmento"]}
    tsv = {"llave": llave, "B": str(B), "semilla": str(SEMILLA),
           "RNG": f"numpy.random.Generator(numpy.random.PCG64({SEMILLA})) numpy {np.__version__}",
           "regla_marco": "pares distintos (est_dis,upm) de hogares concentradohogar con factor finito >0 y est_dis/upm no vacíos, antes de filtrar remesas; incluye pares con X_hu=Y_hu=0",
           "cuantil": "tipo7 lineal q=0.025,0.975",
           "hash_contrato": hash_contrato, "hash_entrada": IDENTIDAD["sha256_entrada"],
           "hash_entorno": hash_entorno}
    for c in ["tipo_incertidumbre", "se", "n_conocidos", "n_upm_marco", "n_upm_conocidos",
              "n_singleton", "n_replicas_no_estimables"]:
        tsv.setdefault(c, "")

    if not (fila_esq["instrumento"] == "ENIGH" and fila_esq["ola"] == "2022"
            and fila_esq["celda"] == "A-P-COMPLEMENTO"
            and fila_esq["conducta"] == "no_recibe_remesas"
            and fila_esq["segmento"] == "TOTAL" and unidad == "HOGAR"):
        motivo = "la única spec humana de punto del paquete cubre ENIGH 2022 A-P-COMPLEMENTO TOTAL HOGAR; esta llave no la cumple"
        tsv["tipo_incertidumbre"] = "SIN-IC"
        return ({"llave": llave, "unidad": unidad, "estado": "NO-RECALCULABLE-DESDE-SPEC",
                 "motivo": motivo}, tsv, dict(diag, estado="NO-RECALCULABLE-DESDE-SPEC", motivo=motivo))

    # Encabezado completo (permitido) para verificar que las columnas existen.
    with open(CSV, encoding="utf-8-sig", newline="") as f:
        encabezado = next(csv.reader(f))
    faltan = [c for c in USECOLS if c not in encabezado]
    if faltan:
        motivo = f"NO-ESTIMABLE-DISENO: faltan columnas {faltan} en concentradohogar"
        tsv["tipo_incertidumbre"] = "SIN-IC"
        return ({"llave": llave, "unidad": unidad, "estado": "NO-ESTIMABLE", "motivo": motivo},
                tsv, dict(diag, estado="NO-ESTIMABLE", motivo=motivo))

    # UTF-8 estricto (encoding_errors='strict'); cadenas opacas sin trim ni conversión.
    df = pd.read_csv(CSV, usecols=USECOLS, dtype=str, keep_default_na=False,
                     na_filter=False, encoding="utf-8-sig", encoding_errors="strict")
    n_filas = len(df)
    diag["n_filas_tabla"] = n_filas

    folioviv = df["folioviv"].tolist()
    foliohog = df["foliohog"].tolist()
    est = df["est_dis"].tolist()
    upm = df["upm"].tolist()
    fac_raw = df["factor"].tolist()
    rem_raw = df["remesas"].tolist()
    del df

    # Llave única folioviv+foliohog.
    llaves_hog = list(zip(folioviv, foliohog))
    n_dup = n_filas - len(set(llaves_hog))
    n_llave_vacia = sum(1 for a, b in llaves_hog if a == "" or b == "")
    diag["n_llave_duplicada"] = n_dup
    diag["n_llave_vacia"] = n_llave_vacia
    if n_dup or n_llave_vacia:
        motivo = f"NO-ESTIMABLE-DISENO: llave folioviv+foliohog no única o vacía (duplicados={n_dup}, vacías={n_llave_vacia})"
        tsv["tipo_incertidumbre"] = "SIN-IC"
        return ({"llave": llave, "unidad": unidad, "estado": "NO-ESTIMABLE", "motivo": motivo},
                tsv, dict(diag, estado="NO-ESTIMABLE", motivo=motivo))

    # Clasificación por fila, en orden físico.
    w = [None] * n_filas
    causas = {"factor_nulo_no_numerico": [], "factor_no_finito_o_no_positivo": [],
              "diseno_faltante": [], "remesas_nula": [], "remesas_no_numerica": [],
              "remesas_negativa": []}
    en_marco = [False] * n_filas
    valido = [False] * n_filas
    y = [0.0] * n_filas
    for i in range(n_filas):
        st, fv = parse_estricto(fac_raw[i])
        if st != "ok":
            causas["factor_nulo_no_numerico"].append(i)
            continue
        w[i] = fv
        if not (math.isfinite(fv) and fv > 0):
            causas["factor_no_finito_o_no_positivo"].append(i)
            continue
        if est[i] == "" or upm[i] == "":
            causas["diseno_faltante"].append(i)
            continue
        en_marco[i] = True
        st, rv = parse_estricto(rem_raw[i])
        if st == "nulo":
            causas["remesas_nula"].append(i)
            continue
        if st == "no_numerico" or not math.isfinite(rv):
            causas["remesas_no_numerica"].append(i)
            continue
        if rv < 0:
            causas["remesas_negativa"].append(i)
            continue
        valido[i] = True
        y[i] = 1.0 if rv == 0 else 0.0  # d=0 (remesas==0) -> complemento

    def peso_excl(idx):
        s = seq_sum(w[i] for i in idx if w[i] is not None and math.isfinite(w[i]))
        return num(s)

    diag["exclusiones"] = {c: {"no_ponderado": len(idx), "ponderado": peso_excl(idx)}
                           for c, idx in causas.items()}
    n_valido = sum(valido)
    diag["n_marco_hogares"] = sum(en_marco)
    diag["n_valido"] = n_valido

    # Paradas del contrato de punto.
    parada = None
    if causas["remesas_nula"]:
        parada = ("NO-ESTIMABLE-NULOS-INESPERADOS",
                  f"{len(causas['remesas_nula'])} hogares con remesas nula; no se sustituyen por cero")
    elif causas["remesas_negativa"]:
        parada = ("NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA",
                  f"{len(causas['remesas_negativa'])} hogares con remesas negativa, sin categoría declarada")
    elif causas["remesas_no_numerica"]:
        parada = ("NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA",
                  f"{len(causas['remesas_no_numerica'])} hogares con remesas no numérica, fuera del mapa d")
    if parada:
        motivo = f"{parada[0]}: {parada[1]}"
        tsv["tipo_incertidumbre"] = "SIN-IC"
        tsv["n_conocidos"] = str(n_valido)
        return ({"llave": llave, "unidad": unidad, "estado": "NO-ESTIMABLE", "motivo": motivo},
                tsv, dict(diag, estado="NO-ESTIMABLE", motivo=motivo))

    # Punto: sumas en orden fijo de llave folioviv+foliohog (orden lexicográfico de cadenas).
    orden_llave = sorted((i for i in range(n_filas) if valido[i]), key=lambda i: llaves_hog[i])
    X = seq_sum(w[i] * y[i] for i in orden_llave)
    Y = seq_sum(w[i] for i in orden_llave)
    X_d1 = seq_sum(w[i] * (1.0 - y[i]) for i in orden_llave)
    n_d0 = sum(1 for i in orden_llave if y[i] == 1.0)
    n_d1 = n_valido - n_d0
    diag["cierre_categorias"] = {
        "n_d0_remesas_cero": n_d0, "n_d1_remesas_positiva": n_d1,
        "n_fuera_de_mapa": len(causas["remesas_negativa"]) + len(causas["remesas_no_numerica"]),
        "suma_factor_d0": num(X), "suma_factor_d1": num(X_d1), "suma_factor_validos": num(Y),
        "cierre_conteo": n_d0 + n_d1 == n_valido,
        "diferencia_ponderada_Y_menos_d0_menos_d1": num(Y - X - X_d1),
    }
    diag["peso_denominador"] = num(Y)
    if Y == 0:
        motivo = "denominador Σ(factor) de hogares válidos igual a cero"
        tsv["tipo_incertidumbre"] = "SIN-IC"
        return ({"llave": llave, "unidad": unidad, "estado": "DENOMINADOR-CERO", "motivo": motivo},
                tsv, dict(diag, estado="DENOMINADOR-CERO", motivo=motivo))
    punto = X / Y
    diag["punto"] = num(punto)

    # Marco de pares (estrato, UPM); totales por par en orden físico de concentradohogar.
    pares = {}
    for i in range(n_filas):
        if not en_marco[i]:
            continue
        k = (est[i], upm[i])
        if k not in pares:
            pares[k] = [0.0, 0.0]
        if valido[i]:  # D_i=1 (TOTAL), K_i=1
            pares[k][0] += w[i] * y[i]
            pares[k][1] += w[i]
    claves = sorted(pares)  # lexicográfico por puntos Unicode (str de Python)
    Xhu = np.array([pares[k][0] for k in claves], dtype=np.float64)
    Yhu = np.array([pares[k][1] for k in claves], dtype=np.float64)
    estratos = []
    for idx, (h, _u) in enumerate(claves):
        if not estratos or estratos[-1][0] != h:
            estratos.append((h, []))
        estratos[-1][1].append(idx)
    estratos = [(h, np.array(ix, dtype=np.int64)) for h, ix in estratos]
    n_upm_marco = len(claves)
    n_upm_conocidos = int(np.sum(Yhu > 0))
    n_singleton = sum(1 for _h, ix in estratos if len(ix) == 1)
    diag["n_estratos"] = len(estratos)

    # Bootstrap empírico no reescalado de UPM.
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    t = np.empty(B, dtype=np.float64)
    no_est = 0
    for r in range(B):
        M = np.zeros(n_upm_marco, dtype=np.int64)
        for _h, ix in estratos:
            sel = rng.choice(ix, len(ix), replace=True)
            np.add.at(M, sel, 1)
        Xr = 0.0
        Yr = 0.0
        for p in range(n_upm_marco):  # acumulación de pares ordenados
            if M[p]:
                Xr += float(M[p]) * float(Xhu[p])
                Yr += float(M[p]) * float(Yhu[p])
        if Yr == 0:
            t[r] = np.nan
            no_est += 1
        else:
            t[r] = Xr / Yr
            if not math.isfinite(t[r]):
                no_est += 1

    tsv.update({"n_conocidos": str(n_valido), "n_upm_marco": str(n_upm_marco),
                "n_upm_conocidos": str(n_upm_conocidos), "n_singleton": str(n_singleton),
                "n_replicas_no_estimables": str(no_est)})
    tipo = "BOOTSTRAP-UPM-NO-REESCALADO-PERCENTIL-DIAGNOSTICO"
    if n_singleton:
        tipo += ";IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA"

    fila = {"llave": llave, "unidad": unidad, "estado": "RECONSTRUIDO", "punto": num(punto)}
    if no_est:
        tsv["tipo_incertidumbre"] = tipo + ";REPLICAS-NO-ESTIMABLES"
        fila["estado_ic"] = "NO-IDENTIFICADA"
        fila["motivo_ic"] = f"{no_est} réplicas bootstrap no estimables (Y_r=0 o no finitas); intervalo y SE nulos por contrato"
        pub = {"publicable": False, "razon": "réplicas no estimables"}
        se = None
    else:
        ts = np.sort(t)
        lo, hi = cuantil_tipo7(ts, Q_INF), cuantil_tipo7(ts, Q_SUP)
        media = seq_sum(t) / B
        se = math.sqrt(seq_sum((float(v) - media) ** 2 for v in t) / (B - 1))
        tsv["tipo_incertidumbre"] = tipo
        tsv["se"] = num(se)
        fila["estado_ic"] = "CALCULADO"
        fila["ic95_inf"] = num(lo)
        fila["ic95_sup"] = num(hi)
        ancho = hi - lo
        diag["ic"] = {"ic95_inf": num(lo), "ic95_sup": num(hi), "se": num(se),
                      "ancho": num(ancho), "media_replicas": num(media)}
        if punto > 0:
            cv = se / punto
            crit = {"n_conocidos>=100": n_valido >= 100,
                    "upm_con_conocidos>=5": n_upm_conocidos >= 5,
                    "ancho<=0.20": ancho <= 0.20, "cv<=0.30": cv <= 0.30,
                    "sin_replicas_no_estimables": True}
            pub = {"publicable": all(crit.values()), "criterios": crit, "cv": num(cv)}
        else:
            pub = {"publicable": None, "razon": "punto 0: se reporta separado sin división (CV no definido)",
                   "criterios": {"n_conocidos>=100": n_valido >= 100,
                                 "upm_con_conocidos>=5": n_upm_conocidos >= 5,
                                 "ancho<=0.20": ancho <= 0.20}}
    diag["publicabilidad"] = dict(pub, nota="regla diagnóstica de residuales-p3-contrato-ic.md; no suprime la celda ni acredita validez inferencial")
    diag.update({"estado": fila["estado"], "estado_ic": fila["estado_ic"],
                 "n_upm_marco": n_upm_marco, "n_upm_conocidos": n_upm_conocidos,
                 "n_singleton": n_singleton, "n_replicas_no_estimables": no_est})
    return fila, tsv, diag


DECISIONES = [
    {"decision": "Punto calculado como Σ(factor·1[remesas==0])/Σ(factor) sobre hogares válidos, sumas float64 secuenciales tras ordenar filas por (folioviv, foliohog) como cadenas (orden lexicográfico por puntos Unicode, sin convertir a entero).",
     "frase": "Σ(factor · 1[d=0])/Σ(factor), sumas en orden fijo de llave."},
    {"decision": "Réplicas bootstrap usan totales por par acumulados en orden físico del CSV, distinto del orden por llave del punto; el punto publicado es el del orden por llave.",
     "frase": "Orden de contribuciones: filas en orden físico de la tabla base declarada: ... concentradohogar para ENIGH"},
    {"decision": "Marco = hogares con factor numérico finito >0 y est_dis y upm no vacíos (cadena vacía = diseño ausente); las filas fuera se cuentan como exclusiones.",
     "frase": "Usar factor finito y >0 ... est_dis y upm son llaves textuales opacas y han de estar presentes en cada fila válida."},
    {"decision": "remesas nula = celda vacía en el CSV; cualquier nula detiene la llave como NO-ESTIMABLE con motivo NO-ESTIMABLE-NULOS-INESPERADOS (estado v3 NO-ESTIMABLE, código en motivo). Mismo tratamiento para negativos (NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA) y para valores no numéricos (tratados como fuera de mapa).",
     "frase": "Nulos de remesas causan NO-ESTIMABLE-NULOS-INESPERADOS; ... Remesas negativa ... parar como NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA"},
    {"decision": "Parseo numérico estricto (regex decimal, sin espacios); cadenas opacas leídas con dtype=str, sin trim ni NA por defecto.",
     "frase": "conservar bytes y ceros iniciales, no convertir a enteros ni rellenar. Validar UTF-8; ... sin trim implícito."},
    {"decision": "D_i=1 para todos los hogares (segmento TOTAL); K_i=1 si remesas numérica ≥0; y_i=1[remesas==0].",
     "frase": "Universo completo de hogares, sin selección por recepción de remesas."},
    {"decision": "rng.choice se aplica sobre los índices globales (en el orden lexicográfico de pares) de los pares del estrato; M_rhu por conteo; X_r y Y_r acumulan M·X_hu en orden de pares con suma secuencial float64 (multiplicación entera·total, no suma repetida).",
     "frase": "por estrato usar rng.choice(indices_ordenados,n_h,replace=True), incluso singleton."},
    {"decision": "Estratos singleton (si existen) se sortean a sí mismos, se registra el conteo y la etiqueta IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA en tipo_incertidumbre, pero estado_ic sigue CALCULADO: el contrato pide marcar, no suprimir.",
     "frase": "Singleton: se sortea a sí mismo, no se colapsa ni descarta; ... Registrar cantidad y marcar IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA."},
    {"decision": "Réplicas no estimables → estado_ic NO-IDENTIFICADA con motivo_ic, manteniendo el punto.",
     "frase": "Si cualquiera no es finita o no estimable, intervalo y SE son nulos; ... Un bloqueo de inferencia se representa con NO-IDENTIFICADA"},
    {"decision": "Formato: se emite v3 (CONTRATO-v3.md firmado) en lugar de v2; campos v3 con los nombres canónicos punto/ic95_inf/ic95_sup.",
     "frase": "donde difieran, rige CONTRATO-v3.md (encargo)"},
    {"decision": "n_conocidos = hogares válidos (D·K=1); n_upm_conocidos = pares del marco con Y_hu>0; hash_contrato = sha256 de residuales-p3-contrato-ic.md; hash_entrada = sha256_entrada de la identidad; hash_entorno = sha256 de salida/entorno.txt.",
     "frase": "columnas tipo_incertidumbre, se, n_conocidos, n_upm_marco, n_upm_conocidos, ... hash_contrato, hash_entrada, hash_entorno"},
    {"decision": "Publicabilidad: CV = SE/punto; ancho = ic95_sup - ic95_inf; se reporta pero no suprime la celda.",
     "frase": "n_conocidos>=100,UPM con conocidos>=5,ancho<=.20,CV<=.30 para punto>0"},
]


def main():
    os.makedirs(SAL, exist_ok=True)
    hash_entorno = escribir_entorno()
    hash_contrato = sha256_archivo(CONTRATO_IC)
    esquema = cargar_esquema()

    filas, tsvs, diags = [], [], []
    for fe in esquema:
        f, t, d = reconstruir_llave(fe, hash_contrato, hash_entorno)
        filas.append(f)
        tsvs.append(t)
        diags.append(d)

    doc = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    cols = ["llave", "tipo_incertidumbre", "se", "n_conocidos", "n_upm_marco", "n_upm_conocidos",
            "n_singleton", "n_replicas_no_estimables", "B", "semilla", "RNG", "regla_marco",
            "cuantil", "hash_contrato", "hash_entrada", "hash_entorno"]
    with open(os.path.join(SAL, "diagnosticos-ic-v1.tsv"), "w", encoding="utf-8", newline="") as fh:
        wr = csv.writer(fh, delimiter="\t", lineterminator="\n")
        wr.writerow(cols)
        for t in tsvs:
            wr.writerow([t.get(c, "") for c in cols])

    codigo = os.path.abspath(__file__)
    diagnostico = {
        "identidad": IDENTIDAD,
        "sha256_implementacion": sha256_archivo(codigo),
        "sha256_documentos": {os.path.basename(p): sha256_archivo(p) for p in
                              [CONTRATO_IC, MODULOS_IC, ESQUEMA,
                               os.path.join(PAQ, "enigh-complemento-restaurado.md"),
                               os.path.join(PAQ, "CONTRATO-v3.md")]},
        "columnas_leidas": USECOLS,
        "llaves": diags,
        "decisiones": DECISIONES,
    }
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as fh:
        json.dump(diagnostico, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


if __name__ == "__main__":
    main()
