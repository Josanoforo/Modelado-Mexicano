#!/usr/bin/env python3
"""Reconstrucción independiente ENBIARE 2021 · pisos de bienestar (paquete enbiare-pisos-bienestar-0001).

Ejecutar desde el directorio de trabajo:  python3 salida/codigo/reconstruye.py
Lee solo ./paquete/ (columnas autorizadas) y escribe en ./salida/:
  resultado.json, diagnosticos-ic-v1.tsv, diagnostico.json, entorno.txt

Método de punto: enbiare-metodo-base.md, spec-conductas-base.md, enbiare-ventanas-restauradas.md,
enbiare-edades-propuesta.md (firmado R26a). IC: residuales-p3-contrato-ic.md y
residuales-p3-modulos-ic.md (firmados R26b, uso diagnóstico). Formato: CONTRATO-v3.md (firmado R31).
"""
import hashlib
import json
import math
import os
import platform
import subprocess
import sys

import numpy as np
import pandas as pd

PAQ = "paquete"
SAL = "salida"

IDENTIDAD = {
    "paquete": "enbiare-pisos-bienestar-0001",
    "version_entrada": "residuales-documentales-v2",
    "sha256_entrada": "fc75485a4e49118eacfca104070214c86fa4071b75550234cfc05ffb69c9fbfe",
}

LLAVE = ["FOLIO", "VIV_SEL", "HOGAR", "N_REN"]
COLS_TENBIARE = LLAVE + [
    "TLOC", "FAC_ELE", "EST_DIS", "UPM_DIS", "PA1", "PA5",
    "PD2_1", "PD2_2", "PD2_3", "PD2_4", "PD2_5", "PD2_6", "PD2_7", "PD3_1", "PD3_2",
    "PB1_01", "PB1_02", "PB1_04", "PB1_11", "PB2_1", "PB2_2", "PG6", "PG7",
]
COLS_TSDEM = LLAVE + ["SEXO", "EDAD", "NIVEL"]

# Firmas registradas en FIRMAS-Y-ACCESO.md
FIRMADOS = {
    "enbiare-edades-propuesta.md": "95f614a43f0cc01ea3caaeb59b1ecc59ca4328d351a6b91b2c6fb09c604dd67d",
    "residuales-p3-contrato-ic.md": "f09ffd47ee2bfbb80d210b4af0d2c29c1b0e7515f92ca85a051d3654ab9338bb",
    "residuales-p3-modulos-ic.md": "d360280cd34b7067ef35af8a42091c3c03a352910faba4be33659a41d0006c98",
    "CONTRATO-v3.md": "821a5ecb762eff1f563964a72f1e794b2899e57f66c1f62a28aae008552194eb",
}

# Receta IC (residuales-p3-contrato-ic.md)
B = 2000
SEMILLA = 20260923
Q_INF, Q_SUP = 0.025, 0.975

ESCALAS = {  # conducta del esquema -> variable 0..10 (spec: se publican como media)
    "satisfaccion-vida": "PA1",
    "escalera-cantril": "PA5",
    "confianza-mayoria-gente": "PB1_01",
    "confianza-gente-conocida": "PB1_02",
    "confianza-policia-municipal": "PB1_04",
    "confianza-partidos": "PB1_11",
}
PROPORCIONES = [
    "depresion-cesd7", "ansiedad-gad2", "cuenta-apoyo-familia", "cuenta-apoyo-amistades",
    "tiene-religion", "asiste-servicio-religioso",
]

EDADES_ADULTAS = {"%02d" % a for a in range(18, 97)}  # 18..96 (96 = 96 y más)


def sha256_archivo(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def num(x):
    return repr(float(x))


# ---------------------------------------------------------------- datos

def leer_datos():
    lee = dict(dtype=str, keep_default_na=False, na_filter=False, encoding="utf-8")
    t = pd.read_csv(os.path.join(PAQ, "datos", "TENBIARE.csv"), usecols=COLS_TENBIARE, **lee)
    s = pd.read_csv(os.path.join(PAQ, "datos", "TSDEM.csv"), usecols=COLS_TSDEM, **lee)
    t = t[COLS_TENBIARE].copy()
    t["_orden"] = np.arange(len(t))
    # solo llaves únicas en TSDEM
    dup = s.duplicated(LLAVE, keep=False)
    s_u = s[~dup].copy()
    s_u["_pareado"] = True
    m = t.merge(s_u, on=LLAVE, how="left", validate="many_to_one")
    m = m.sort_values("_orden", kind="stable").reset_index(drop=True)
    m["_pareado"] = m["_pareado"].eq(True)
    for c in ("SEXO", "EDAD", "NIVEL"):
        m[c] = m[c].where(m["_pareado"], "")
    meta = {
        "n_tenbiare": int(len(t)),
        "n_tsdem": int(len(s)),
        "n_tsdem_llaves_duplicadas": int(dup.sum()),
        "n_tenbiare_llaves_duplicadas": int(t.duplicated(LLAVE).sum()),
    }
    return m, meta


def preparar(m):
    w = pd.to_numeric(m["FAC_ELE"], errors="coerce").astype("float64").to_numpy()
    w_ok = np.isfinite(w) & (w > 0)
    est_ok = (m["EST_DIS"].str.strip() != "").to_numpy()
    upm_ok = (m["UPM_DIS"].str.strip() != "").to_numpy()
    diseno_ok = w_ok & est_ok & upm_ok
    pareado = m["_pareado"].to_numpy()
    edad = m["EDAD"].to_numpy()
    edad_adulta = np.isin(edad, list(EDADES_ADULTAS)) | (edad == "98")
    universo = diseno_ok & pareado & edad_adulta
    causa = np.full(len(m), "", dtype=object)
    causa[~w_ok] = "DISENO-FAC_ELE-NO-POSITIVO-O-NO-FINITO"
    causa[w_ok & ~(est_ok & upm_ok)] = "DISENO-ESTRATO-O-UPM-VACIO"
    causa[diseno_ok & ~pareado] = "G-JOIN-SIN-SOCIODEMOGRAFICO"
    sel = diseno_ok & pareado & ~edad_adulta
    causa[sel] = ["EDAD-FUERA-DE-UNIVERSO-CODIGO-" + (e if e != "" else "BLANCO") for e in edad[sel]]
    return dict(w=w, w_ok=w_ok, universo=universo, causa_universo=causa, edad=edad)


def edad_anios(edad):
    """Años para códigos 18..96; NaN para 98 u otros."""
    out = np.full(len(edad), np.nan)
    for i, e in enumerate(edad):
        if e in EDADES_ADULTAS:
            out[i] = float(int(e))
    return out


def segmentos_eje(m, eje, edad):
    """Devuelve dict segmento -> máscara, y máscara de 'clasificable en el eje'."""
    n = len(m)
    if eje == "TOTAL":
        return {"TODOS": np.ones(n, bool)}
    if eje == "SEXO":
        v = m["SEXO"].to_numpy()
        return {"HOMBRE": v == "1", "MUJER": v == "2"}
    if eje == "EDAD":
        a = edad_anios(edad)
        with np.errstate(invalid="ignore"):
            return {
                "18-29": (a >= 18) & (a <= 29),
                "30-44": (a >= 30) & (a <= 44),
                "45-59": (a >= 45) & (a <= 59),
                "60-MAS": (a >= 60) & (a <= 96),
            }
    if eje == "ESCOLARIDAD":
        v = m["NIVEL"].to_numpy()
        return {
            "HASTA-PRIMARIA": np.isin(v, ["00", "01", "02"]),
            "SECUNDARIA": np.isin(v, ["03", "04"]),
            "MEDIA-SUPERIOR": np.isin(v, ["05", "06", "07"]),
            "SUPERIOR": np.isin(v, ["08", "09", "10"]),
        }
    if eje == "TLOC":
        v = m["TLOC"].to_numpy()
        return {"100MIL-MAS": v == "1", "15MIL-99MIL": v == "2",
                "2500-14999": v == "3", "MENOS-2500": v == "4"}
    raise KeyError(eje)


def conducta(m, nombre, edad):
    """Devuelve (K válido, y desenlace, causa de invalidez por fila)."""
    n = len(m)
    causa = np.full(n, "", dtype=object)
    if nombre in ESCALAS:
        v = m[ESCALAS[nombre]].to_numpy()
        codigos = {"%02d" % k: float(k) for k in range(11)}
        K = np.array([x in codigos for x in v])
        y = np.array([codigos.get(x, np.nan) for x in v])
        causa[~K] = "RESPUESTA-FUERA-DE-0-10"
        return K, y, causa
    if nombre == "depresion-cesd7":
        items = ["PD2_%d" % i for i in range(1, 8)]
        vals = {"0": 0, "1": 1, "2": 2, "3": 3}
        comp = np.ones(n, bool)
        punt = np.zeros(n)
        for it in items:
            v = m[it].to_numpy()
            ok = np.isin(v, list(vals))
            comp &= ok
            x = np.array([vals.get(z, 0) for z in v], dtype=float)
            punt += (3.0 - x) if it == "PD2_6" else x
        a = edad_anios(edad)
        es98 = edad == "98"
        with np.errstate(invalid="ignore"):
            corte = np.where((a >= 18) & (a <= 59), 9.0, np.where((a >= 60) & (a <= 96), 5.0, np.nan))
        K = comp & ~es98 & np.isfinite(corte)
        with np.errstate(invalid="ignore"):
            y = np.where(K, (punt >= corte).astype(float), np.nan)
        causa[es98] = "EDAD-NO-DETERMINA-CORTE"
        causa[~es98 & ~comp] = "RESPUESTA-INVALIDA-CESD7-INCOMPLETA"
        return K, y, causa
    if nombre == "ansiedad-gad2":
        vals = {"0": 0, "1": 1, "2": 2, "3": 3}
        v1, v2 = m["PD3_1"].to_numpy(), m["PD3_2"].to_numpy()
        K = np.isin(v1, list(vals)) & np.isin(v2, list(vals))
        s = np.array([vals.get(a, 0) + vals.get(b, 0) for a, b in zip(v1, v2)], dtype=float)
        y = np.where(K, (s >= 3).astype(float), np.nan)
        causa[~K] = "RESPUESTA-INVALIDA-GAD2-INCOMPLETA"
        return K, y, causa
    if nombre in ("cuenta-apoyo-familia", "cuenta-apoyo-amistades"):
        v = m["PB2_1" if nombre == "cuenta-apoyo-familia" else "PB2_2"].to_numpy()
        mapa = {"1": 1.0, "2": 0.0, "3": 0.0}
        K = np.isin(v, list(mapa))
        y = np.array([mapa.get(x, np.nan) for x in v])
        causa[~K] = "RESPUESTA-FUERA-DE-1-2-3"
        return K, y, causa
    if nombre == "tiene-religion":
        v = m["PG6"].to_numpy()
        mapa = {"1": 1.0, "2": 0.0}
        K = np.isin(v, list(mapa))
        y = np.array([mapa.get(x, np.nan) for x in v])
        causa[~K] = "RESPUESTA-FUERA-DE-1-2"
        return K, y, causa
    if nombre == "asiste-servicio-religioso":
        g6, g7 = m["PG6"].to_numpy(), m["PG7"].to_numpy()
        y = np.full(n, np.nan)
        y[(g6 == "1") & (g7 == "1")] = 1.0
        y[(g6 == "1") & (g7 == "2")] = 0.0
        y[(g6 == "2") & (g7 == "")] = 0.0  # blanco por secuencia
        K = np.isfinite(y)
        causa[~K & (g6 == "1")] = "RESPUESTA-INVALIDA-PG7-CON-PG6-1"
        causa[~K & (g6 == "2")] = "RESPUESTA-INVALIDA-PG7-NO-BLANCO-CON-PG6-2"
        causa[~K & ~np.isin(g6, ["1", "2"])] = "RESPUESTA-INVALIDA-PG6"
        return K, y, causa
    raise KeyError(nombre)


# ---------------------------------------------------------------- diseño y bootstrap

def construir_marco(m, universo):
    est = m["EST_DIS"].to_numpy()
    upm = m["UPM_DIS"].to_numpy()
    for x in list(est) + list(upm):  # validar UTF-8 (str ya decodificado; reencode estricto)
        x.encode("utf-8", errors="strict")
    pares = sorted({(est[i], upm[i]) for i in np.flatnonzero(universo)})  # orden por puntos Unicode
    idx = {p: j for j, p in enumerate(pares)}
    par_fila = np.full(len(m), -1, dtype=np.int64)
    for i in np.flatnonzero(universo):
        par_fila[i] = idx[(est[i], upm[i])]
    estratos = []
    actual, lista = None, []
    for j, (h, _u) in enumerate(pares):
        if h != actual:
            if actual is not None:
                estratos.append((actual, np.array(lista, dtype=np.int64)))
            actual, lista = h, []
        lista.append(j)
    if actual is not None:
        estratos.append((actual, np.array(lista, dtype=np.int64)))
    return pares, par_fila, estratos


def multiplicidades(n_pares, estratos, semilla):
    """Instancia nueva de Generator(PCG64(semilla)); réplica -> estrato lexicográfico."""
    rng = np.random.Generator(np.random.PCG64(semilla))
    M = np.zeros((B, n_pares), dtype=np.float64)
    for r in range(B):
        fila = M[r]
        for _h, ind in estratos:
            sel = rng.choice(ind, ind.shape[0], replace=True)
            np.add.at(fila, sel, 1.0)
    return M


_CACHE_M = {}


def multiplicidades_identidad(n_pares, estratos, semilla):
    # Una instancia nueva por identidad con la misma semilla y el mismo marco produce la misma
    # secuencia; se memoriza por (semilla, marco) y se verifica al final con una instancia fresca.
    clave = (semilla, n_pares, tuple((h, tuple(ind.tolist())) for h, ind in estratos))
    if clave not in _CACHE_M:
        _CACHE_M[clave] = multiplicidades(n_pares, estratos, semilla)
    return _CACHE_M[clave]


def totales_por_par(n_pares, par_fila, w, contrib, y):
    """Sumas float64 en orden físico de TENBIARE; ceros explícitos por par."""
    X = [0.0] * n_pares
    Y = [0.0] * n_pares
    for i in np.flatnonzero(contrib):  # índices crecientes = orden físico
        j = int(par_fila[i])
        wi = float(w[i])
        X[j] = X[j] + wi * float(y[i])
        Y[j] = Y[j] + wi
    return np.array(X, dtype=np.float64), np.array(Y, dtype=np.float64)


def acumula_pares(v):
    s = 0.0
    for x in v:
        s = s + float(x)
    return s


def cuantil_tipo7(ordenadas, q):
    Bn = len(ordenadas)
    a = (Bn - 1) * q
    j = int(math.floor(a))
    if j >= Bn - 1:
        return float(ordenadas[Bn - 1])
    return float((1 - a + j) * ordenadas[j] + (a - j) * ordenadas[j + 1])


def bootstrap(M, Xh, Yh):
    Xr = np.zeros(B)
    Yr = np.zeros(B)
    for u in range(Xh.shape[0]):  # acumulación de pares ordenados
        col = M[:, u]
        Xr = Xr + col * Xh[u]
        Yr = Yr + col * Yh[u]
    t = np.full(B, np.nan)
    ok = Yr != 0
    t[ok] = Xr[ok] / Yr[ok]
    no_est = int((~np.isfinite(t)).sum())
    if no_est:
        return None, None, None, no_est
    ordenadas = np.sort(t)
    inf = cuantil_tipo7(ordenadas, Q_INF)
    sup = cuantil_tipo7(ordenadas, Q_SUP)
    media = float(np.mean(t))
    se = math.sqrt(float(np.sum((t - media) ** 2)) / (B - 1))
    return inf, sup, se, 0


# ---------------------------------------------------------------- principal

def entorno_txt():
    un = subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout.strip()
    lineas = [
        "python " + sys.version.replace("\n", " "),
        "numpy " + np.__version__,
        "pandas " + pd.__version__,
        "lector pandas.read_csv (engine C por defecto; dtype=str, keep_default_na=False, na_filter=False, encoding=utf-8)",
        "pyreadstat no instalado (no usado)",
        "dbfread no instalado (no usado)",
        "platform " + platform.platform(),
        "uname -a: " + un,
    ]
    return "\n".join(lineas) + "\n"


def main():
    os.makedirs(SAL, exist_ok=True)

    firmas = {}
    for f, h in FIRMADOS.items():
        real = sha256_archivo(os.path.join(PAQ, f))
        firmas[f] = {"sha256_registrado": h, "sha256_observado": real, "coincide": real == h}
        if real != h:
            raise SystemExit("Documento firmado alterado: " + f)

    ent = entorno_txt()
    with open(os.path.join(SAL, "entorno.txt"), "w", encoding="utf-8") as fh:
        fh.write(ent)
    hash_entorno = hashlib.sha256(ent.encode("utf-8")).hexdigest()
    hash_contrato = FIRMADOS["residuales-p3-contrato-ic.md"]
    hash_codigo = sha256_archivo(os.path.abspath(__file__))

    esquema = pd.read_csv(os.path.join(PAQ, "esquema-identidades.tsv"), sep="\t", dtype=str,
                          keep_default_na=False, na_filter=False)
    assert esquema["llave"].is_unique

    m, meta = leer_datos()
    P = preparar(m)
    w, universo, edad = P["w"], P["universo"], P["edad"]
    pares, par_fila, estratos = construir_marco(m, universo)
    n_pares = len(pares)
    n_singleton = int(sum(1 for _h, ind in estratos if ind.shape[0] == 1))

    def conteo(mask):
        mask = mask & P["w_ok"]
        return int(mask.sum()), acumula_pares(w[mask]) if mask.any() else 0.0

    # exclusiones de universo (comunes a todas las llaves)
    excl_univ = {}
    for c in sorted(set(P["causa_universo"]) - {""}):
        mk = P["causa_universo"] == c
        n_c = int(mk.sum())
        wsum = acumula_pares(w[mk & P["w_ok"]]) if (mk & P["w_ok"]).any() else 0.0
        excl_univ[c] = {"n": n_c, "ponderado": num(wsum)}

    filas, diag_ic, diag_llaves = [], [], []
    for _, e in esquema.iterrows():
        llave, unidad, cond, eje, seg = e["llave"], e["unidad"], e["conducta"], e["eje"], e["segmento"]
        segs = segmentos_eje(m, eje, edad)
        if seg not in segs:
            raise KeyError((eje, seg))
        clasif = np.zeros(len(m), bool)
        for v in segs.values():
            clasif |= v
        D = universo & segs[seg]
        K, y, causa_resp = conducta(m, cond, edad)
        contrib = D & K

        # exclusiones por causa
        excl_eje = {}
        if eje != "TOTAL":
            ne = universo & ~clasif
            if cond == "depresion-cesd7":
                ne98 = ne & (edad == "98")
                n_, w_ = conteo(ne98)
                if n_:
                    excl_eje["EDAD-NO-DETERMINA-CORTE"] = {"n": n_, "ponderado": num(w_)}
                ne = ne & ~(edad == "98")
            if ne.any():
                if eje == "EDAD":
                    etiqueta = "EJE-EDAD-CODIGO-98-FUERA-DE-TRAMO"
                    n_, w_ = conteo(ne)
                    excl_eje[etiqueta] = {"n": n_, "ponderado": num(w_)}
                else:
                    col = {"SEXO": "SEXO", "ESCOLARIDAD": "NIVEL", "TLOC": "TLOC"}[eje]
                    vals = m[col].to_numpy()
                    for v in sorted(set(vals[ne])):
                        n_, w_ = conteo(ne & (vals == v))
                        excl_eje["EJE-%s-NO-CLASIFICABLE-CODIGO-%s" % (col, v if v else "BLANCO")] = {
                            "n": n_, "ponderado": num(w_)}
        excl_seg = {}
        inval = D & ~K
        for c in sorted(set(causa_resp[inval])):
            n_, w_ = conteo(inval & (causa_resp == c))
            excl_seg[c] = {"n": n_, "ponderado": num(w_)}
        n_valido = int(contrib.sum())
        w_valido = acumula_pares(w[contrib]) if contrib.any() else 0.0

        dl = {
            "llave": llave, "conducta": cond, "eje": eje, "segmento": seg,
            "n_dominio": int(D.sum()), "n_valido": n_valido, "ponderado_valido": num(w_valido),
            "exclusiones": {"universo": excl_univ, "eje": excl_eje, "segmento": excl_seg},
        }
        dic = {"llave": llave, "B": str(B), "semilla": str(SEMILLA),
               "RNG": "numpy.random.Generator(numpy.random.PCG64(20260923)) instancia nueva por identidad",
               "regla_marco": "todos los pares (EST_DIS,UPM_DIS) distintos del universo base persona elegida 18+ "
                              "(EDAD 18-96 o 98) con FAC_ELE finito>0 y diseño válido, previo a dominio/respuesta; "
                              "orden lexicográfico por puntos Unicode",
               "cuantil": "tipo7 lineal q=0.025,0.975 sobre 2000 réplicas ordenadas",
               "hash_contrato": hash_contrato, "hash_entrada": IDENTIDAD["sha256_entrada"],
               "hash_entorno": hash_entorno, "n_upm_marco": str(n_pares), "n_singleton": str(n_singleton)}

        if cond in ESCALAS:
            motivo = ("El esquema fija unidad 'proporcion' para esta identidad, pero la spec humana "
                      "(enbiare-metodo-base.md §4 y tabla; residuales-p3-modulos-ic.md 'Escalas0..10 medias') "
                      "define %s 0–10 solo como media; ninguna spec fija corte o categoría que convierta la "
                      "escala en proporción, y copiar una media bajo unidad 'proporcion' convertiría escala."
                      % ESCALAS[cond])
            filas.append({"llave": llave, "unidad": unidad, "estado": "NO-RECALCULABLE-DESDE-SPEC",
                          "motivo": motivo})
            dl.update({"estado": "NO-RECALCULABLE-DESDE-SPEC",
                       "nota_n_valido": "n_valido y exclusiones calculados bajo la validez 0–10 de la spec de media; no hay punto",
                       "publicabilidad": "NO-APLICA-SIN-PUNTO (medias 0..10: SIN-REGLA-PUBLICABILIDAD-ADOPTADA)"})
            dic.update({"tipo_incertidumbre": "SIN-IC-FILA-NO-RECONSTRUIDA", "se": "NA",
                        "n_conocidos": str(n_valido), "n_upm_conocidos": "NA",
                        "n_replicas_no_estimables": "NA"})
            diag_llaves.append(dl)
            diag_ic.append(dic)
            continue

        Xh, Yh = totales_por_par(n_pares, par_fila, w, contrib, y)
        Xtot, Ytot = acumula_pares(Xh), acumula_pares(Yh)
        n_upm_con = int((np.bincount(par_fila[contrib], minlength=n_pares) > 0).sum()) if contrib.any() else 0
        dic.update({"n_conocidos": str(n_valido), "n_upm_conocidos": str(n_upm_con)})
        if Ytot == 0:
            filas.append({"llave": llave, "unidad": unidad, "estado": "DENOMINADOR-CERO",
                          "motivo": "Y=sum(w·D·K)=0 en el dominio observado bajo spec suficiente"})
            dl.update({"estado": "DENOMINADOR-CERO", "publicabilidad": "NO-APLICA-SIN-PUNTO"})
            dic.update({"tipo_incertidumbre": "SIN-IC-DENOMINADOR-CERO", "se": "NA",
                        "n_replicas_no_estimables": "NA"})
            diag_llaves.append(dl)
            diag_ic.append(dic)
            continue
        punto = Xtot / Ytot
        M = multiplicidades_identidad(n_pares, estratos, SEMILLA)
        inf, sup, se, no_est = bootstrap(M, Xh, Yh)
        fila = {"llave": llave, "unidad": unidad, "estado": "RECONSTRUIDO", "punto": num(punto)}
        motivos_pub = []
        if no_est:
            fila.update({"estado_ic": "NO-IDENTIFICADA",
                         "motivo_ic": "%d réplicas bootstrap no estimables (Y_r=0 o no finitas); el contrato "
                                      "anula intervalo y SE" % no_est})
            motivos_pub.append("REPLICAS-NO-ESTIMABLES")
            tipo = "IC-NULO-REPLICAS-NO-ESTIMABLES"
        elif n_singleton > 0:
            fila.update({"estado_ic": "NO-IDENTIFICADA",
                         "motivo_ic": "IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA: %d estratos con UPM única en el marco"
                                      % n_singleton})
            tipo = "IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA"
        else:
            if not (inf <= sup):
                raise AssertionError("extremos desordenados " + llave)
            fila.update({"estado_ic": "CALCULADO", "ic95_inf": num(inf), "ic95_sup": num(sup)})
            tipo = "BOOTSTRAP-UPM-EN-ESTRATO-NO-REESCALADO-PERCENTIL-DIAGNOSTICO"
        filas.append(fila)
        dic.update({"tipo_incertidumbre": tipo, "se": num(se) if se is not None else "NA",
                    "n_replicas_no_estimables": str(no_est)})
        # publicabilidad diagnóstica de proporciones
        if punto == 0:
            pub = "PUNTO-CERO-REPORTE-SEPARADO"
        else:
            if n_valido < 100:
                motivos_pub.append("N_CONOCIDOS<100")
            if n_upm_con < 5:
                motivos_pub.append("UPM_CON_CONOCIDOS<5")
            if se is not None and inf is not None:
                if (sup - inf) > 0.20:
                    motivos_pub.append("ANCHO>0.20")
                if se / punto > 0.30:
                    motivos_pub.append("CV>0.30")
            elif "REPLICAS-NO-ESTIMABLES" not in motivos_pub:
                motivos_pub.append("IC-NO-IDENTIFICADO")
            pub = "PUBLICABLE" if not motivos_pub else "NO-PUBLICABLE:" + ",".join(motivos_pub)
        dl.update({"estado": "RECONSTRUIDO", "publicabilidad": pub,
                   "ancho_ic": num(sup - inf) if inf is not None else None,
                   "cv": num(se / punto) if (se is not None and punto != 0) else None})
        diag_llaves.append(dl)
        diag_ic.append(dic)

    # verificación: instancia fresca reproduce las multiplicidades memorizadas
    verif = None
    if _CACHE_M:
        M_fresca = multiplicidades(n_pares, estratos, SEMILLA)
        verif = bool(np.array_equal(M_fresca, next(iter(_CACHE_M.values()))))
        if not verif:
            raise AssertionError("instancia fresca de RNG no reproduce multiplicidades")

    doc = {"version": 3, "identidad": dict(IDENTIDAD), "filas": filas}
    with open(os.path.join(SAL, "resultado.json"), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    cols = ["llave", "tipo_incertidumbre", "se", "n_conocidos", "n_upm_marco", "n_upm_conocidos",
            "n_singleton", "n_replicas_no_estimables", "B", "semilla", "RNG", "regla_marco", "cuantil",
            "hash_contrato", "hash_entrada", "hash_entorno"]
    with open(os.path.join(SAL, "diagnosticos-ic-v1.tsv"), "w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for d in diag_ic:
            fh.write("\t".join(str(d[c]) for c in cols) + "\n")

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "decisiones.json"), encoding="utf-8") as fh:
        decisiones = json.load(fh)
    diag = {
        "identidad": IDENTIDAD,
        "firmas_verificadas": firmas,
        "sha256_codigo_reconstruye_py": hash_codigo,
        "sha256_entorno_txt": hash_entorno,
        "datos": dict(meta, **{
            "n_universo_base": int(universo.sum()),
            "n_upm_marco": n_pares, "n_estratos_marco": len(estratos), "n_singleton": n_singleton,
            "n_codigo_edad_98_en_universo": int((universo & (edad == "98")).sum()),
            "exclusiones_universo": excl_univ,
            "rng_instancia_fresca_reproduce_multiplicidades": verif,
        }),
        "decisiones_implementacion": decisiones,
        "llaves": diag_llaves,
    }
    with open(os.path.join(SAL, "diagnostico.json"), "w", encoding="utf-8") as fh:
        json.dump(diag, fh, ensure_ascii=False, indent=1)
        fh.write("\n")

    est = pd.Series([f["estado"] for f in filas]).value_counts().to_dict()
    print("filas", len(filas), est)


if __name__ == "__main__":
    main()
