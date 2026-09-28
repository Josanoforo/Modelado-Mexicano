"""Reconstrucción independiente ENCODAT 2016-2017 · paquete encodat-pisos-sustancias-0001.

Punto: spec-base-metodo.md + spec-base-conductas.md.
IC:    residuales-p3-contrato-ic.md + residuales-p3-modulos-ic.md (firmados, R26).
Salida: CONTRATO-v3.md (firmado, R31).

Uso, desde el directorio de trabajo que contiene paquete/ y salida/:
    python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json, salida/diagnosticos-ic-v1.tsv, salida/diagnostico.json
y salida/entorno.txt.
"""
import hashlib
import json
import platform
import subprocess
import sys

import numpy as np
import pandas as pd

PAQ = "paquete"
SAL = "salida"
IND = "paquete/datos/ENCODAT_2016_2017_Individual.dta"
HOG = "paquete/datos/ENCODAT_2016_2017_Hogar.dta"
ESQUEMA = "paquete/esquema-identidades.tsv"
CONTRATO_IC = "paquete/residuales-p3-contrato-ic.md"
MODULOS_IC = "paquete/residuales-p3-modulos-ic.md"

IDENTIDAD = {
    "paquete": "encodat-pisos-sustancias-0001",
    "version_entrada": "residuales-documentales-v2",
    "sha256_entrada": "c8b50b5727b2317b589a970fabc1b678359afc49406748225044e0dedcbc0ec0",
}

# Columnas autorizadas y usadas (Individual no contiene id_hogar: el vínculo es id_pers[:20]).
COLS_IND = ["id_pers", "ds2", "ds3", "ds9", "ponde_ss", "al1", "al4", "al9", "al11",
            "tb02", "tb05", "tb50", "di1a", "di1b", "di1c", "di1d", "di1e", "di1f", "di1g",
            "di1h", "di1i", "dm1a", "dm1b", "dm1c", "dm1d", "tp1"]
COLS_HOG = ["id_hogar", "est_var", "code_upm", "estrato"]

B = 2000
SEMILLA = 20260923
Q = (0.025, 0.975)
ETIQ_SINGLETON = "IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA"


def sha256_archivo(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def num(x):
    return repr(float(x))


# --------------------------------------------------------------------------- entorno
def escribe_entorno():
    uname = subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout.strip()
    try:
        import openpyxl
        v_openpyxl = openpyxl.__version__
    except Exception:  # pragma: no cover
        v_openpyxl = "no disponible"
    lineas = [
        f"python {sys.version.split()[0]} ({platform.python_implementation()})",
        f"numpy {np.__version__}",
        f"pandas {pd.__version__}",
        f"lector .dta: pandas.read_stata (pandas {pd.__version__}); pyreadstat y dbfread no instalados",
        f"lector .xlsx (solo inspección del FD, no usado por reconstruye.py): openpyxl {v_openpyxl}",
        f"uname -a: {uname}",
    ]
    texto = "\n".join(lineas) + "\n"
    with open(f"{SAL}/entorno.txt", "w", encoding="utf-8") as f:
        f.write(texto)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- datos
def carga():
    ind = pd.read_stata(IND, columns=COLS_IND, convert_categoricals=False, preserve_dtypes=True)
    hog = pd.read_stata(HOG, columns=COLS_HOG, convert_categoricals=False, preserve_dtypes=True)
    return ind.reset_index(drop=True), hog.reset_index(drop=True)


def clave_estrato(v):
    """Cadena opaca del estrato de varianza: est_var es double en el .dta; se escribe como
    entero decimal si es entero (como lo muestra el formato %12.0g), si no con repr."""
    f = float(v)
    return str(int(f)) if f.is_integer() else repr(f)


def arma_base(ind, hog):
    g = {}
    n0 = len(ind)
    g["G-FILAS-INDIVIDUAL"] = n0
    edad_ok = ind.ds3.notna() & (ind.ds3 >= 12) & (ind.ds3 <= 65)
    g["G-FUERA-EDAD-12-65"] = int((~edad_ok).sum())
    peso_ok = np.isfinite(ind.ponde_ss.to_numpy(dtype="float64")) & (ind.ponde_ss.to_numpy() > 0)
    g["G-PESO-NO-POSITIVO-O-NO-FINITO"] = int((edad_ok & ~peso_ok).sum())
    base = ind[edad_ok & peso_ok].copy()  # conserva orden físico
    base["id_hogar"] = base.id_pers.str[:20]

    dup = hog.id_hogar.duplicated(keep=False)
    g["G-HOGAR-ID-DUPLICADO-FILAS"] = int(dup.sum())
    hog_u = hog[~dup]
    m = base.merge(hog_u, on="id_hogar", how="left", indicator=True, sort=False)
    assert len(m) == len(base)
    m.index = base.index
    ambiguo = m.id_hogar.isin(set(hog.id_hogar[dup]))
    sin_hogar = (m["_merge"] != "both") & ~ambiguo
    g["G-JOIN-AMBIGUO"] = int(ambiguo.sum())
    g["G-JOIN-SIN-HOGAR"] = int(sin_hogar.sum())
    diseno_ok = (m["_merge"] == "both") & m.est_var.notna() & np.isfinite(m.est_var.astype("float64")) \
        & m.code_upm.notna() & (m.code_upm.astype(str) != "")
    g["G-DISENO-INCOMPLETO"] = int(((m["_merge"] == "both") & ~diseno_ok).sum())
    g["G-FILAS-DISENO-VALIDO"] = int(diseno_ok.sum())
    excl_diseno = m[~diseno_ok]
    g["G-PESO-EXCLUIDO-POR-DISENO"] = num(excl_diseno.ponde_ss.sum()) if len(excl_diseno) else "0.0"
    b = m[diseno_ok].drop(columns=["_merge"]).copy()
    b["h"] = [clave_estrato(v) for v in b.est_var]
    b["u"] = b.code_upm.astype(str)
    return b, g


def arma_marco(b):
    """Pares (estrato, UPM) distintos del universo base, orden lexicográfico por puntos Unicode."""
    pares = sorted(set(zip(b.h, b.u)))
    for h, u in pares:
        h.encode("utf-8")
        u.encode("utf-8")
    idx_par = {p: i for i, p in enumerate(pares)}
    par_fila = np.array([idx_par[p] for p in zip(b.h, b.u)], dtype=np.int64)
    estratos = sorted(set(h for h, _ in pares))
    grupos = [np.array([i for i, (h, _) in enumerate(pares) if h == e], dtype=np.int64) for e in estratos]
    return pares, par_fila, estratos, grupos


def multiplicidades(n_pares, grupos):
    """M[r, p]: multiplicidad del par p en la réplica r. Generator(PCG64(SEMILLA)) nuevo;
    iteración réplica -> estrato lexicográfico; rng.choice(indices_ordenados, n_h, replace=True).
    Como la receta reinicia el RNG por identidad y el marco es común, M es idéntica para todas
    las identidades; se calcula una vez por identidad llamando a esta función (sin compartir estado)."""
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    M = np.zeros((B, n_pares), dtype=np.int64)
    for r in range(B):
        fila = M[r]
        for g in grupos:
            sel = rng.choice(g, len(g), replace=True)
            np.add.at(fila, sel, 1)
    return M


# --------------------------------------------------------------------------- conductas
def v(s):
    return s.to_numpy(dtype="float64")


def conductas(b):
    """Devuelve dict conducta -> (valido bool, y float, causa_exclusion array de str)."""
    al1, al4, al9, al11 = v(b.al1), v(b.al4), v(b.al9), v(b.al11)
    ds2 = v(b.ds2)
    n = len(b)
    out = {}

    def causa_directa(x, validos):
        c = np.full(n, "", dtype=object)
        c[np.isnan(x)] = "SIN-DATO"
        c[~np.isnan(x) & ~np.isin(x, validos)] = "CODIGO-NO-VALIDO"
        return c

    def causa_codigo(x):
        # etiqueta la causa con el código observado (NS/NR u otro)
        c = np.full(n, "", dtype=object)
        nan = np.isnan(x)
        c[nan] = "SIN-DATO"
        for k in np.unique(x[~nan]):
            c[x == k] = f"CODIGO-{clave_estrato(k)}"
        return c

    no_bebio_nunca = al1 == 2
    no_bebio_12m = (al1 == 2) | (al4 == 2)

    # ALCOHOL-12M: al4 1->1, 2->0; si al4 no es 1/2 y al1 = 2 -> 0.
    ok = np.isin(al4, [1, 2])
    y = np.where(al4 == 1, 1.0, 0.0)
    salto = ~ok & no_bebio_nunca
    val = ok | salto
    c = causa_codigo(al4)
    c = np.where(val, "", np.char.add("al4-", c.astype(str)))
    out["alcohol-12m"] = (val, np.where(val, y, 0.0), c)

    # ALCOHOL-30D: al9 1->1, 2->0; si al9 no es 1/2 y (al1 = 2 o al4 = 2) -> 0.
    ok = np.isin(al9, [1, 2])
    y = np.where(al9 == 1, 1.0, 0.0)
    salto = ~ok & no_bebio_12m
    val = ok | salto
    c = np.where(val, "", np.char.add("al9-", causa_codigo(al9).astype(str)))
    out["alcohol-30d"] = (val, np.where(val, y, 0.0), c)

    # ALCOHOL-EXCESIVO-12M: al11 códigos 1..6 válidos; hombre (ds2=1) 1-4 -> 1, mujer (ds2=2) 1-5 -> 1;
    # resto de 1..6 -> 0; 9 fuera; si al11 no es 1..6 y no bebió en 12 m -> 0.
    ok_codigo = np.isin(al11, [1, 2, 3, 4, 5, 6])
    ok_sexo = np.isin(ds2, [1, 2])
    ok = ok_codigo & ok_sexo
    umbral = np.where(ds2 == 1, 4, 5)
    y = np.where(ok & (al11 <= umbral), 1.0, 0.0)
    salto = ~ok_codigo & no_bebio_12m
    val = ok | salto
    c = np.where(ok_codigo & ~ok_sexo, "ds2-SEXO-NO-VALIDO", np.char.add("al11-", causa_codigo(al11).astype(str)))
    c = np.where(val, "", c)
    out["alcohol-excesivo-12m"] = (val, np.where(val, y, 0.0), c)

    # FUMA-ACTUAL: tb02 1,2 -> 1; 3 -> 0; tb02 sin dato (nulo) y tb05 = 2 -> 0.
    tb02, tb05 = v(b.tb02), v(b.tb05)
    ok = np.isin(tb02, [1, 2, 3])
    y = np.where(np.isin(tb02, [1, 2]), 1.0, 0.0)
    salto = np.isnan(tb02) & (tb05 == 2)
    val = ok | salto
    c = np.where(val, "", np.char.add("tb02-", causa_codigo(tb02).astype(str)))
    out["fuma-actual"] = (val, np.where(val, y, 0.0), c)

    def binaria(x, nombre):
        ok = np.isin(x, [1, 2])
        y = np.where(x == 1, 1.0, 0.0)
        c = np.where(ok, "", np.char.add(f"{nombre}-", causa_codigo(x).astype(str)))
        return ok, np.where(ok, y, 0.0), c

    def alguna(cols, nombre):
        X = np.column_stack([v(b[k]) for k in cols])
        alguno1 = (X == 1).any(axis=1)
        todos2 = (X == 2).all(axis=1)
        val = alguno1 | todos2
        y = np.where(alguno1, 1.0, 0.0)
        todos_nulos = np.isnan(X).all(axis=1)
        algun_9 = (X == 9).any(axis=1)
        c = np.where(todos_nulos, f"{nombre}-TODOS-SIN-DATO",
                     np.where(algun_9, f"{nombre}-SIN-1-CON-NSNR", f"{nombre}-SIN-1-INCOMPLETO"))
        c = np.where(val, "", c)
        return val, np.where(val, y, 0.0), c

    out["cigarro-electronico-alguna-vez"] = binaria(v(b.tb50), "tb50")
    di = ["di1a", "di1b", "di1c", "di1d", "di1e", "di1f", "di1g", "di1h", "di1i"]
    out["droga-ilegal-alguna-vez"] = alguna(di, "di1a-i")
    out["mariguana-alguna-vez"] = binaria(v(b.di1a), "di1a")
    out["droga-medica-sin-receta-alguna-vez"] = alguna(["dm1a", "dm1b", "dm1c", "dm1d"], "dm1a-d")
    out["opiaceos-sin-receta-alguna-vez"] = binaria(v(b.dm1a), "dm1a")
    out["consulto-profesional-por-consumo"] = binaria(v(b.tp1), "tp1")
    return out


def dominios(b):
    """Devuelve dict (eje, segmento) -> (D bool, causa_fuera array)."""
    n = len(b)
    ds2, ds3, ds9, est = v(b.ds2), v(b.ds3), v(b.ds9), v(b.estrato)
    d = {("TOTAL", "TODOS"): np.ones(n, bool)}
    d[("SEXO", "HOMBRE")] = ds2 == 1
    d[("SEXO", "MUJER")] = ds2 == 2
    d[("EDAD", "12-17")] = (ds3 >= 12) & (ds3 <= 17)
    d[("EDAD", "18-34")] = (ds3 >= 18) & (ds3 <= 34)
    d[("EDAD", "35-65")] = (ds3 >= 35) & (ds3 <= 65)
    d[("ESTRATO", "RURAL")] = est == 1
    d[("ESTRATO", "URBANO")] = est == 2
    d[("ESTRATO", "METROPOLITANO")] = est == 3
    adulto = ds3 >= 18
    d[("ESCOLARIDAD", "HASTA-PRIMARIA")] = adulto & np.isin(ds9, [1, 2])
    d[("ESCOLARIDAD", "SECUNDARIA")] = adulto & np.isin(ds9, [3, 4])
    d[("ESCOLARIDAD", "MEDIA-SUPERIOR")] = adulto & np.isin(ds9, [5, 6])
    d[("ESCOLARIDAD", "SUPERIOR")] = adulto & np.isin(ds9, [7, 8, 9])
    # causas de quedar fuera del eje (no pertenecer a ningún segmento del eje)
    causas = {
        "TOTAL": np.full(n, "", dtype=object),
        "SEXO": np.where(np.isin(ds2, [1, 2]), "", np.where(np.isnan(ds2), "ds2-SIN-DATO", "ds2-CODIGO-NO-VALIDO")),
        "EDAD": np.full(n, "", dtype=object),
        "ESTRATO": np.where(np.isin(est, [1, 2, 3]), "", np.where(np.isnan(est), "estrato-SIN-DATO", "estrato-CODIGO-NO-VALIDO")),
        "ESCOLARIDAD": np.where(~adulto, "MENOR-DE-18",
                                np.where(np.isin(ds9, list(range(1, 10))), "",
                                         np.where(ds9 == 99, "ds9-99-NO-CONTESTA",
                                                  np.where(np.isnan(ds9), "ds9-SIN-DATO", "ds9-CODIGO-NO-VALIDO")))),
    }
    return d, causas


# --------------------------------------------------------------------------- estimación
def suma_ordenada(pesos_fila, par_fila, n_pares):
    """Totales por par acumulando filas en orden físico (np.add.at es secuencial en el orden dado)."""
    t = np.zeros(n_pares, dtype=np.float64)
    np.add.at(t, par_fila, pesos_fila)
    return t


def acumula_pares(M, t):
    """sum_p M[:, p] * t[p], acumulado en el orden de los pares (vectorizado sobre réplicas)."""
    acc = np.zeros(M.shape[0], dtype=np.float64)
    for p in range(M.shape[1]):
        acc += M[:, p] * t[p]
    return acc


def cuantil_tipo7(t_ord, q):
    Bn = len(t_ord)
    a = (Bn - 1) * q
    j = int(np.floor(a))
    if j >= Bn - 1:
        return float(t_ord[Bn - 1])
    return float((1 - a + j) * t_ord[j] + (a - j) * t_ord[j + 1])


def main():
    hash_entorno = escribe_entorno()
    hash_contrato = sha256_archivo(CONTRATO_IC)
    hash_modulos = sha256_archivo(MODULOS_IC)

    esquema = pd.read_csv(ESQUEMA, sep="\t", dtype=str, keep_default_na=False)
    ind, hog = carga()
    b, glob = arma_base(ind, hog)
    pares, par_fila, estratos, grupos = arma_marco(b)
    n_pares = len(pares)
    n_singleton = sum(1 for g in grupos if len(g) == 1)
    glob["G-PARES-MARCO"] = n_pares
    glob["G-ESTRATOS-MARCO"] = len(estratos)
    glob["G-ESTRATOS-SINGLETON"] = n_singleton

    w = v(b.ponde_ss)
    cond = conductas(b)
    doms, causas_eje = dominios(b)

    M = None  # ver multiplicidades(): se recalcula con RNG nuevo por identidad
    filas, diag_ic, diag_llaves = [], [], []
    for _, e in esquema.iterrows():
        llave, unidad = e["llave"], e["unidad"]
        conducta, eje, seg = e["conducta"], e["eje"], e["segmento"]
        fila = {"llave": llave, "unidad": unidad}
        dg = {"llave": llave, "conducta": conducta, "eje": eje, "segmento": seg}
        dic = {"llave": llave}
        if conducta not in cond or (eje, seg) not in doms:
            fila.update(estado="NO-RECALCULABLE-DESDE-SPEC",
                        motivo=f"conducta '{conducta}' o eje/segmento '{eje}/{seg}' sin regla en la spec humana")
            filas.append(fila)
            diag_llaves.append(dg)
            continue
        K, y, causa_K = cond[conducta]
        D = doms[(eje, seg)]
        DK = D & K
        # exclusiones
        excl = {}
        fuera_eje = causas_eje[eje]
        for etiqueta, mask in (
            [(f"FUERA-DE-EJE:{c}", (fuera_eje == c)) for c in sorted(set(fuera_eje) - {""})]
            + [("FUERA-DE-SEGMENTO", (fuera_eje == "") & ~D)]
            + [(f"RESPUESTA-NO-VALIDA:{c}", D & (causa_K == c)) for c in sorted(set(causa_K[D]) - {""})]
        ):
            nm = int(mask.sum())
            if nm:
                excl[etiqueta] = {"n": nm, "ponderado": num(w[mask].sum())}
        n_con = int(DK.sum())
        dg["universo_base_diseno_valido"] = len(b)
        dg["n_dominio"] = int(D.sum())
        dg["n_valido"] = n_con
        dg["n_valido_ponderado"] = num(w[DK].sum())
        dg["n_positivos"] = int((DK & (y == 1)).sum())
        dg["exclusiones_en_base"] = excl

        wx = np.where(DK, w * y, 0.0)
        wy = np.where(DK, w, 0.0)
        Xh = suma_ordenada(wx, par_fila, n_pares)
        Yh = suma_ordenada(wy, par_fila, n_pares)
        X = acumula_pares(np.ones((1, n_pares), dtype=np.int64), Xh)[0]
        Y = acumula_pares(np.ones((1, n_pares), dtype=np.int64), Yh)[0]
        n_upm_con = int(np.bincount(par_fila[DK], minlength=n_pares).astype(bool).sum())

        dic.update(n_conocidos=n_con, n_upm_marco=n_pares, n_upm_conocidos=n_upm_con,
                   n_singleton=n_singleton, B=B, semilla=SEMILLA,
                   RNG="numpy.random.Generator(numpy.random.PCG64(20260923)); nuevo por identidad; "
                       "réplica->estrato lexicográfico; rng.choice(indices_ordenados,n_h,replace=True)",
                   regla_marco="pares (est_var,code_upm) distintos del universo base 12-65 con ponde_ss>0 finito "
                               "y diseño válido, antes de filtrar dominio/respuesta; incluye X_hu=Y_hu=0",
                   cuantil="tipo7 lineal; q=0.025,0.975",
                   hash_contrato=hash_contrato, hash_entrada=IDENTIDAD["sha256_entrada"],
                   hash_entorno=hash_entorno)

        if not (Y > 0) or not np.isfinite(Y):
            fila.update(estado="DENOMINADOR-CERO",
                        motivo=f"dominio {eje}/{seg} sin respuestas válidas de {conducta} en el universo con diseño "
                               f"válido (Y=sum(w_i D_i K_i)={num(Y)}, n_conocidos={n_con})")
            dic.update(tipo_incertidumbre="NO-ESTIMABLE-DENOMINADOR-CERO", se="", n_replicas_no_estimables="")
            dg["publicabilidad"] = {"estado": "NO-PUBLICABLE", "razones": ["denominador cero"]}
            filas.append(fila)
            diag_ic.append(dic)
            diag_llaves.append(dg)
            continue

        punto = X / Y
        # réplicas: RNG nuevo por identidad (misma ley que la receta; M no se comparte entre identidades)
        M = multiplicidades(n_pares, grupos)
        Xr = acumula_pares(M, Xh)
        Yr = acumula_pares(M, Yh)
        no_est = (Yr == 0) | ~np.isfinite(Yr)
        with np.errstate(divide="ignore", invalid="ignore"):
            tr = np.where(no_est, np.nan, Xr / np.where(no_est, 1.0, Yr))
        n_no_est = int((no_est | ~np.isfinite(tr)).sum())
        fila.update(estado="RECONSTRUIDO", punto=num(punto))
        tipo = "BOOTSTRAP-UPM-PERCENTIL-DIAGNOSTICO"
        if n_singleton:
            tipo += ";" + ETIQ_SINGLETON
        if n_no_est:
            fila.update(estado_ic="NO-IDENTIFICADA",
                        motivo_ic=f"{n_no_est} de {B} réplicas bootstrap con Y_r=0 o no finitas; "
                                  f"la receta RESIDUALES-P3-IC-v1 anula intervalo y SE")
            se = ""
            lo = hi = None
        else:
            t_ord = np.sort(tr)
            lo, hi = cuantil_tipo7(t_ord, Q[0]), cuantil_tipo7(t_ord, Q[1])
            media = np.mean(tr)
            se_f = float(np.sqrt(np.sum((tr - media) ** 2) / (B - 1)))
            se = num(se_f)
            fila.update(estado_ic="CALCULADO", ic95_inf=num(lo), ic95_sup=num(hi))
        dic.update(tipo_incertidumbre=tipo, se=se, n_replicas_no_estimables=n_no_est)

        # publicabilidad diagnóstica (proporciones)
        razones = []
        if n_con < 100:
            razones.append(f"n_conocidos={n_con}<100")
        if n_upm_con < 5:
            razones.append(f"UPM con conocidos={n_upm_con}<5")
        if n_no_est:
            razones.append(f"{n_no_est} réplicas no estimables")
        pub = {"n_conocidos": n_con, "n_upm_conocidos": n_upm_con}
        if lo is not None:
            ancho = hi - lo
            pub["ancho"] = num(ancho)
            if not ancho <= 0.20:
                razones.append("ancho>0.20")
        if punto > 0:
            if se != "":
                cv = float(se) / punto
                pub["cv"] = num(cv)
                if not cv <= 0.30:
                    razones.append("CV>0.30")
            pub["estado"] = "PUBLICABLE" if not razones else "NO-PUBLICABLE"
        else:
            pub["estado"] = "PUNTO-CERO-REPORTADO-APARTE" if not razones else "PUNTO-CERO-NO-PUBLICABLE"
            razones.append("punto=0: CV no se calcula (sin división)")
        pub["razones"] = razones
        dg["publicabilidad"] = pub
        filas.append(fila)
        diag_ic.append(dic)
        diag_llaves.append(dg)

    doc = {"version": 3, "identidad": IDENTIDAD, "filas": filas}
    with open(f"{SAL}/resultado.json", "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write("\n")

    cols = ["llave", "tipo_incertidumbre", "se", "n_conocidos", "n_upm_marco", "n_upm_conocidos", "n_singleton",
            "n_replicas_no_estimables", "B", "semilla", "RNG", "regla_marco", "cuantil", "hash_contrato",
            "hash_entrada", "hash_entorno"]
    pd.DataFrame(diag_ic, columns=cols).to_csv(f"{SAL}/diagnosticos-ic-v1.tsv", sep="\t", index=False,
                                               lineterminator="\n")

    diagnostico = {
        "identidad": IDENTIDAD,
        "hashes_documentos": {"residuales-p3-contrato-ic.md": hash_contrato,
                              "residuales-p3-modulos-ic.md": hash_modulos,
                              "CONTRATO-v3.md": sha256_archivo("paquete/CONTRATO-v3.md"),
                              "spec-base-metodo.md": sha256_archivo("paquete/spec-base-metodo.md"),
                              "spec-base-conductas.md": sha256_archivo("paquete/spec-base-conductas.md"),
                              "esquema-identidades.tsv": sha256_archivo(ESQUEMA)},
        "global": glob,
        "decisiones": DECISIONES,
        "llaves": diag_llaves,
    }
    with open(f"{SAL}/diagnostico.json", "w", encoding="utf-8") as f:
        json.dump(diagnostico, f, ensure_ascii=False, indent=1)
        f.write("\n")


DECISIONES = [
    {"id": "D1-RECETA-IC",
     "frase": "spec-base-metodo.md §4: «bootstrap de UPM dentro de `est_var`, certeza para UPM única, "
              "`PCG64(20260924)` ... con la receta común por sha256» vs residuales-p3-modulos-ic.md: «Semilla común20260923 "
              "y marco completo son elecciones NUEVAS del contrato diagnóstico; no restauran semillas históricas20260924»",
     "decision": "El IC sigue la receta firmada RESIDUALES-P3-IC-v1 (semilla 20260923, marco completo, singleton se "
                 "sortea a sí mismo). La «receta común por sha256» es código productor no incluido (lo dice el propio "
                 "documento de módulos) y no se usa."},
    {"id": "D2-SINGLETON-ESTADO-IC",
     "frase": "residuales-p3-contrato-ic.md: «Singleton: se sortea a sí mismo ... Registrar cantidad y marcar "
              "IC-CON-UPM-UNICA-VARIANZA-NO-IDENTIFICADA»",
     "decision": "Si hubiera estratos singleton, el IC se calcularía igual (CALCULADO) y la marca iría en "
                 "tipo_incertidumbre del TSV. En este dato el marco no tiene estratos singleton, así que no aplica."},
    {"id": "D3-CADENA-ESTRATO",
     "frase": "«Orden de pares: lexicográfico por cadena opaca de estrato y UPM; conservar bytes y ceros iniciales, "
              "no convertir a enteros»",
     "decision": "est_var viene como double en el .dta (no hay cadena original). Se escribe como entero decimal sin "
                 "ceros («12»), igual que lo muestra su formato %12.0g, y el orden es lexicográfico sobre esa cadena "
                 "(«10» < «2»). code_upm (str) se usa tal cual lo devuelve pandas.read_stata."},
    {"id": "D4-PRECEDENCIA-SALTOS",
     "frase": "spec-base-conductas.md: «1 → 1; 2 → 0; al1 = 2 (nunca) → 0» y análogas para ALCOHOL-30D, "
              "ALCOHOL-EXCESIVO-12M y FUMA-ACTUAL",
     "decision": "La respuesta directa válida rige; la regla de salto solo asigna 0 cuando la variable directa no "
                 "trae código válido. Así una respuesta directa válida nunca se sobrescribe."},
    {"id": "D5-EXCESIVO-RESTO",
     "frase": "«hombres 5+ copas (códigos 1–4), mujeres 4+ (1–5) → 1; resto → 0; no bebió 12 m → 0; 9 fuera»",
     "decision": "«resto» = los demás códigos sustantivos 1–6 de al11 que no alcanzan el umbral. Un bebedor de 12 m "
                 "sin al11 (nulo) queda fuera (no se imputa cero). Sin ds2 ∈ {1,2} no hay umbral: fuera."},
    {"id": "D6-FUMA-SIN-DATO",
     "frase": "«1, 2 → 1; 3 → 0; sin dato y tb05 = 2 (nunca) → 0» y «No imputar NS/NR ni negativos a cero»",
     "decision": "«sin dato» = tb02 nulo (no preguntado). tb02 = 7 (No sabe) o 9 (No responde) queda fuera aunque "
                 "tb05 = 2."},
    {"id": "D7-ALGUNA-VEZ",
     "frase": "«"
              "Alguna vez» de drogas: 1 si algún ítem = 1; 0 si todos = 2; si no, fuera.»",
     "decision": "Se aplica literal a di1a–di1i y dm1a–dm1d: un 1 en cualquier ítem basta aunque otros sean 9 o nulos; "
                 "0 exige los nueve (o cuatro) ítems = 2."},
    {"id": "D8-ESCOLARIDAD",
     "frase": "«ESCOLARIDAD (`ds9`, sólo 18+) ... 99 fuera» y módulos: «marco conjunto base12..65, no reducido a "
              "mayores18 para eje educativo»",
     "decision": "El dominio exige ds3 ≥ 18 y ds9 en el segmento; el marco de UPM es el de toda la base 12–65. "
                 "Códigos de ds9 fuera de 1–9 (99, nulo) quedan fuera del eje."},
    {"id": "D9-ESTRATO-EJE",
     "frase": "«El diseño vive en Hogar: ... estrato rural/urbano/metropolitano `estrato`» y «ESTRATO (1 RURAL, "
              "2 URBANO, 3 METROPOLITANO)»",
     "decision": "El eje ESTRATO usa `estrato` de Hogar unido por id_pers[:20] = id_hogar; los estratos de varianza "
                 "son `est_var`."},
    {"id": "D10-JOIN",
     "frase": "«Sólo se usan `id_hogar` únicos; los no pareados se cuentan (`G-JOIN-SIN-HOGAR`)» y «Join ambiguo ... "
              "es NO-ESTIMABLE-DISENO»",
     "decision": "Los id_hogar duplicados en Hogar se descartan por completo y sus personas se cuentan como join "
                 "ambiguo, fuera del diseño válido. En este dato no hay duplicados ni personas sin hogar."},
    {"id": "D11-DENOMINADOR-CERO",
     "frase": "residuales: «Y=0 es NO-ESTIMABLE, nunca cero»; CONTRATO-v3: «DENOMINADOR-CERO | ... dominio observado "
              "con denominador cero»",
     "decision": "Si Y=0 en el punto, el estado es DENOMINADOR-CERO (el estado específico de v3), con motivo."},
    {"id": "D12-SUMAS",
     "frase": "«sumas float64, totales por par en ese orden y acumulación de pares ordenados»",
     "decision": "Los totales X_hu, Y_hu se acumulan con np.add.at en orden físico de Individual; el punto y cada "
                 "réplica acumulan M_rhu·X_hu par por par en orden lexicográfico (sin BLAS ni Kahan). El punto "
                 "es X/Y con esas mismas sumas por par."},
    {"id": "D13-PUBLICABILIDAD",
     "frase": "«n_conocidos>=100,UPM con conocidos>=5,ancho<=.20,CV<=.30 para punto>0; punto0 se reporta separado "
              "sin división; cualquier réplica no estimable impide publicación»",
     "decision": "UPM con conocidos = pares del marco con al menos una persona en D·K; ancho = ic95_sup − ic95_inf; "
                 "CV = SE/punto. Solo es diagnóstico: no se suprime ninguna celda de resultado.json."},
    {"id": "D14-HASH-CONTRATO",
     "frase": "columnas «hash_contrato, hash_entrada, hash_entorno»",
     "decision": "hash_contrato = sha256 de residuales-p3-contrato-ic.md; hash_entrada = sha256_entrada de la "
                 "identidad; hash_entorno = sha256 de los bytes de salida/entorno.txt."},
    {"id": "D15-M-POR-IDENTIDAD",
     "frase": "«una instancia nueva por identidad, sin saltos ni compartir estado entre conductas»",
     "decision": "Se crea un Generator nuevo por identidad y se recalcula la matriz de multiplicidades (misma "
                 "secuencia para todas, pues el marco es común)."},
]


if __name__ == "__main__":
    main()
