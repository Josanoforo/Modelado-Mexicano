from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

Piso t-1 (ENIF 2021) de las conductas de crédito K1–K7 por los ejes del
marcador. El marco (FAC_ELE, EST_DIS × UPM_DIS, 10 000 remuestras PCG64(42),
un solo plan de réplicas) y los cortes de los ejes se IMPORTAN del medidor
sellado de CALC-PISOS-ENIF2021-EJES-0003 (input `MEDIDOR-EJES-0003`, bytes
verificados por sha256). La rejilla de categorías se LEE de las tablas de
identidad GEN2 (`PISOS-REJILLA-METADATOS`, `PISOS-FORMALIDAD-METADATOS`), y
el reactivo de cada conducta se CONTRASTA contra la fila 2021 de la tabla
de comparabilidad por texto (`CREDITO-COMPARABILIDAD-TEXTO`). No lee nada
de `milpa/`. Spec: DIN-CREDITO-PISOS-ENIF2021-spec-v1_0.md.

Una sola llamada a `_estimate` sobre un marco combinado (filas persona +
filas producto) garantiza que TODAS las conductas y celdas —P y PR—
comparten el mismo plan de réplicas que el piso de ahorro.
"""
import types
from pathlib import Path
import numpy as np
import pandas as pd

PREFIJO = "DIN-CREDITO-PISOS-ENIF2021"
MIEMBRO = "conjunto_de_datos_tmodulo_enif_2021.csv"
CON = "con seguridad social"
SIN = "sin seguridad social"
N_SOPORTE = 200                       # piso de la casa (n sin ponderar)
EJES_REJILLA = ("sexo", "edad", "escolaridad", "localidad", "cuenta")
PRODUCTOS = [f"P6_2_{k}" for k in range(1, 10)]
ATRASOS = [f"P6_4_{k}" for k in range(1, 10)]
INFORMALES = [f"P6_1_{k}" for k in range(1, 6)]
CUENTAS = [f"P5_4_{k}" for k in range(1, 10)]
CANALES = {"1": "SUCURSAL", "2": "APP", "3": "INTERNET",
           "4": "ESTABLECIMIENTO", "5": "PROMOTOR", "6": "OTRO"}

# conducta emitida -> (unidad, fila K de la tabla de comparabilidad,
#                      tokens de reactivo que esa fila debe traer)
CONDUCTAS = [
    ("K1", "P", "K1", ("P6_2_1..P6_2_9", "P6_14")),
    ("K2-DEPARTAMENTAL", "P", "K2", ("P6_2_1",)),
    ("K2-NOMINA", "P", "K2", ("P6_2_3",)),
    ("K2-AUTOMOTRIZ", "P", "K2", ("P6_2_5",)),
    ("K3", "P", "K3", ("P6_1_1..P6_1_5",)),
    ("K4A-AUTOEXCLUSION", "P", "K4", ("P6_15",)),
    ("K4B-OFERTA", "P", "K4", ("P6_15",)),
    ("K4B1-REQUISITOS", "P", "K4", ("P6_15",)),
    ("K4B2-ACCESO", "P", "K4", ("P6_15",)),
    ("K4B3-RECHAZO-ANTICIPADO", "P", "K4", ("P6_15",)),
    ("K5", "P", "K5", ("P6_17",)),
    ("K5-ENTRE-SOLICITANTES", "P", "K5", ("P6_17",)),
    ("K6-PR", "PR", "K6", ("P6_4_1..P6_4_9",)),
    ("K6-P-TENEDORES", "P", "K6", ("P6_4_1..P6_4_9",)),
] + [(f"K7-{v}", "PR", "K7", ("P6_7",)) for v in CANALES.values()]


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _modulo_0003(inputs):
    src = _bytes(inputs["MEDIDOR-EJES-0003"])
    mod = types.ModuleType("medidor_ejes_0003")
    exec(compile(src, "medidor_ejes_0003", "exec"), mod.__dict__)
    return mod


def _tsv(ent):
    """TSV -> lista de dicts, partiendo por tabulador (el módulo csv despoja
    comillas en este proyecto)."""
    lineas = _bytes(ent).decode("utf-8").splitlines()
    lineas = [l for l in lineas if l and not l.startswith("#")]
    cab = lineas[0].split("\t")
    return [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]


def _rejilla(inputs):
    """Categorías por eje, leídas de las tablas de identidad GEN2 (spec §3).
    Falla si falta un eje o la partición de formalidad no es la esperada."""
    filas = [f for f in _tsv(inputs["PISOS-REJILLA-METADATOS"])
             if (f["source_instrument"], f["source_edition"], f["status"])
             == ("ENIF", "2021", "CONSTRUIBLE")]
    ejes: dict[str, list[str]] = {}
    for f in filas:
        ejes.setdefault(f["axis"], [])
        if f["category"] not in ejes[f["axis"]]:
            ejes[f["axis"]].append(f["category"])
    faltan = [e for e in EJES_REJILLA if e not in ejes]
    if faltan:
        raise RuntimeError(f"eje ausente en la tabla de identidad GEN2: {faltan}")
    form = [f for f in _tsv(inputs["PISOS-FORMALIDAD-METADATOS"])
            if (f["source_instrument"], f["source_edition"], f["axis"], f["status"])
            == ("ENIF", "2021", "formalidad", "CONSTRUIBLE")]
    cats = []
    for f in form:
        if f["category"] not in cats:
            cats.append(f["category"])
    if sorted(cats) != sorted([SIN, CON]):
        raise RuntimeError(f"rejilla de formalidad inesperada: {cats}")
    ejes["formalidad"] = cats
    return {e: ejes[e] for e in EJES_REJILLA + ("formalidad",)}


def _comparabilidad(inputs):
    """Fila 2021 de cada conducta en la tabla de comparabilidad por texto;
    el reactivo que este medidor usa debe estar escrito ahí (spec §1)."""
    filas = {f["conducta"]: f for f in _tsv(inputs["CREDITO-COMPARABILIDAD-TEXTO"])
             if f["ola"] == "2021"}
    for cid, unidad, k, tokens in CONDUCTAS:
        f = filas[k]
        if f["veredicto"] != "MISMO-INSTRUMENTO":
            raise RuntimeError(f"{k} 2021 no es fila ancla MISMO-INSTRUMENTO: {f['veredicto']}")
        for t in tokens:
            if t not in f["reactivo"]:
                raise RuntimeError(f"{cid}: el reactivo {t!r} no está en la fila {k}·2021")
        u = f["unidad"]
        if unidad == "PR" and not u.startswith("PR"):
            raise RuntimeError(f"{cid}: unidad PR no coincide con la tabla ({u!r})")
        if unidad == "P" and cid != "K6-P-TENEDORES" and (not u.startswith("P") or u.startswith("PR")):
            raise RuntimeError(f"{cid}: unidad P no coincide con la tabla ({u!r})")
        if cid == "K6-P-TENEDORES" and "agregable a P" not in u:
            raise RuntimeError(f"{cid}: la tabla no declara K6 agregable a P ({u!r})")
    if filas["K8"]["veredicto"] != "NO-ESTIMABLE":
        raise RuntimeError("K8 2021 debería ser NO-ESTIMABLE (FP-404); no se mide")
    return filas


def _dicot(code, unos, ceros):
    out = pd.Series(pd.NA, index=code.index, dtype="Float64")
    out.loc[code.isin(list(ceros))] = 0.0
    out.loc[code.isin(list(unos))] = 1.0
    return out


def medir(inputs, contrato):
    m = _modulo_0003(inputs)
    rejilla = _rejilla(inputs)
    _comparabilidad(inputs)
    z = inputs["enif2021_csv"]["ruta_absoluta"]
    cols = (PRODUCTOS + ATRASOS + INFORMALES + CUENTAS
            + ["P6_7", "P6_14", "P6_15", "P6_17", "P3_10",
               "SEXO", "EDAD", "TLOC", "P3_1_1", "FAC_ELE", "EST_DIS", "UPM_DIS"])
    d = m._csv(z, MIEMBRO, cols)
    d["_w"] = pd.to_numeric(d["FAC_ELE"], errors="coerce")
    d["_est"] = d["EST_DIS"].str.strip(); d["_upm"] = d["UPM_DIS"].str.strip()
    c = {v: m._code(d[v]) for v in cols if v not in ("FAC_ELE", "EST_DIS", "UPM_DIS")}

    # Ejes: los cortes del medidor sellado de -0003 (importados) y el mapa de
    # formalidad de PISOS-ENIF2021-formalidad-spec-v1_0.md §1.
    cu = d[CUENTAS].apply(m._code)
    account = pd.Series(pd.NA, index=d.index, dtype="object")
    account.loc[cu.eq("1").any(axis=1)] = "con cuenta"
    account.loc[cu.eq("2").all(axis=1)] = "sin cuenta"
    formalidad = pd.Series(pd.NA, index=d.index, dtype="object")
    formalidad.loc[c["P3_10"].isin(list("12345"))] = CON
    formalidad.loc[c["P3_10"].eq("6")] = SIN
    ejes_p = {
        "sexo": c["SEXO"].where(c["SEXO"].isin(["1", "2"]), pd.NA),
        "edad": m._age(d["EDAD"]),
        "escolaridad": m._school(d["P3_1_1"]),
        "localidad": m._code(d["TLOC"]).map({"1": "15 000 y mas", "2": "15 000 y mas",
                                             "3": "menor de 15 000", "4": "menor de 15 000"}),
        "cuenta": account,
        "formalidad": formalidad,
    }
    for e, cats in rejilla.items():
        vistos = set(ejes_p[e].dropna().unique())
        if not vistos <= set(cats):
            raise RuntimeError(f"eje {e}: categorías fuera de la rejilla GEN2: {sorted(vistos - set(cats))}")

    # Conductas (unidad P, filas persona). Códigos leídos de la tabla de
    # comparabilidad; spec §2.
    pr = d[PRODUCTOS].apply(m._code)
    tenedor = pr.eq("1").any(axis=1)
    sin_producto = pr.eq("2").all(axis=1)
    y = {}
    y["K1"] = pd.Series(pd.NA, index=d.index, dtype="Float64")
    y["K1"].loc[sin_producto] = 0.0; y["K1"].loc[tenedor] = 1.0
    for cid, v in (("K2-DEPARTAMENTAL", "P6_2_1"), ("K2-NOMINA", "P6_2_3"),
                   ("K2-AUTOMOTRIZ", "P6_2_5")):
        y[cid] = _dicot(c[v], "1", "2")
    inf = d[INFORMALES].apply(m._code)
    y["K3"] = pd.Series(pd.NA, index=d.index, dtype="Float64")
    y["K3"].loc[inf.eq("2").all(axis=1)] = 0.0; y["K3"].loc[inf.eq("1").any(axis=1)] = 1.0
    nunca = sin_producto & c["P6_14"].eq("2")            # base de K4: «nunca ha tenido»
    p615 = c["P6_15"].where(nunca, "")
    for cid, unos in (("K4A-AUTOEXCLUSION", "67"), ("K4B-OFERTA", "123"),
                      ("K4B1-REQUISITOS", "1"), ("K4B2-ACCESO", "2"),
                      ("K4B3-RECHAZO-ANTICIPADO", "3")):
        y[cid] = _dicot(p615, unos, "".join(sorted(set("123456789") - set(unos))))
    y["K5"] = _dicot(c["P6_17"], "1", "23")
    y["K5-ENTRE-SOLICITANTES"] = _dicot(c["P6_17"], "1", "2")
    at = d[ATRASOS].apply(m._code)
    held = pr.eq("1").to_numpy()                            # comparación POSICIONAL (defecto de -0002)
    at_held = at.where(held, "")                            # atraso sólo de productos tenidos
    y["K6-P-TENEDORES"] = pd.Series(pd.NA, index=d.index, dtype="Float64")
    y["K6-P-TENEDORES"].loc[tenedor & (at_held.eq("2").to_numpy() | ~held).all(axis=1)] = 0.0
    y["K6-P-TENEDORES"].loc[tenedor & at_held.eq("1").any(axis=1)] = 1.0
    p67 = c["P6_7"].where(tenedor, "")
    for code, nombre in CANALES.items():
        y[f"K7-{nombre}"] = _dicot(p67, code, "".join(sorted(set("123456") - {code})))

    # Unidad PR de K6: una fila por producto formal tenido (spec §2).
    largos = []
    for k, (pcol, acol) in enumerate(zip(PRODUCTOS, ATRASOS), start=1):
        idx = d.index[pr[pcol].eq("1")]
        if len(idx) == 0:
            continue
        bloque = pd.DataFrame({"_w": d.loc[idx, "_w"], "_est": d.loc[idx, "_est"],
                               "_upm": d.loc[idx, "_upm"], "_producto": k,
                               "_y": _dicot(at.loc[idx, acol], "1", "2").astype("Float64")})
        for e in ejes_p:
            bloque[f"_eje_{e}"] = ejes_p[e].loc[idx]
        largos.append(bloque)
    largo = pd.concat(largos, ignore_index=True) if largos else pd.DataFrame(
        columns=["_w", "_est", "_upm", "_producto", "_y"] + [f"_eje_{e}" for e in ejes_p])

    # Marco combinado: personas primero, productos después; un solo plan.
    persona = pd.DataFrame({"_w": d["_w"], "_est": d["_est"], "_upm": d["_upm"], "_producto": 0})
    for e in ejes_p:
        persona[f"_eje_{e}"] = ejes_p[e]
    big = pd.concat([persona, largo.drop(columns=["_y"])], ignore_index=True)
    n_p = len(persona)
    ejes_b = {e: big[f"_eje_{e}"] for e in ejes_p}
    yb = {}
    for cid in y:
        s = pd.Series(pd.NA, index=big.index, dtype="Float64")
        s.iloc[:n_p] = y[cid].to_numpy()
        yb[cid] = s
    s = pd.Series(pd.NA, index=big.index, dtype="Float64")
    if len(largo):
        s.iloc[n_p:] = largo["_y"].to_numpy()
    yb["K6-PR"] = s

    todos = pd.Series("todos", index=big.index, dtype="object")
    trabaja = pd.Series("universo trabaja", index=big.index, dtype="object").where(
        ejes_b["formalidad"].notna(), pd.NA)
    axes = {"nacional": (todos, ("todos",))}
    axes.update({e: (ejes_b[e], tuple(rejilla[e])) for e in rejilla})
    axes["universo"] = (trabaja, ("universo trabaja",))
    orden = [cid for cid, _u, _k, _t in CONDUCTAS]
    cells = []
    for cid in orden:
        cells += m._cells(f"{PREFIJO}-{cid}", yb[cid], axes)
    out = m._estimate(big, cells, int(contrato["parametros"]["bootstrap_replicas"]),
                      int(contrato["seed"]["valor"]))

    # Guardias (spec §4): unidad por conducta, soporte por celda, coherencia
    # por conducta × eje contra el marginal nacional (formalidad contra el
    # universo de quien trabaja). Coherencia rota -> PARA.
    design = big["_w"].notna() & (big["_w"] > 0) & big["_est"].ne("") & big["_upm"].ne("")
    unidad = {cid: u for cid, u, _k, _t in CONDUCTAS}
    for cell in cells:
        rid = cell["base"]
        n = out[rid + "-N"]
        out[rid + "-SOPORTE"] = "OK" if n >= N_SOPORTE else f"BAJO-N-MENOR-{N_SOPORTE}"
    for cid in orden:
        b = f"RESULT-{PREFIJO}-{cid}"
        out[f"{b}-UNIDAD"] = unidad[cid]
        u = design & yb[cid].notna()
        w = big["_w"].where(u, 0.0).astype(float)
        yv = yb[cid].astype("Float64").fillna(0).astype(float)
        num = lambda s: out[f"{b}-{s}-P"] * out[f"{b}-{s}-DEN-W"] if out[f"{b}-{s}-P"] is not None else 0.0
        den = lambda s: out[f"{b}-{s}-DEN-W"]
        for e, cats in rejilla.items():
            ref = "UNIVERSO-UNIVERSO-TRABAJA" if e == "formalidad" else "NACIONAL-TODOS"
            partes = [f"{m._slug(e)}-{m._slug(cat)}" for cat in cats]
            na = u & ejes_b[e].isna() if e != "formalidad" else pd.Series(False, index=big.index)
            d_num = abs(num(ref) - sum(num(p) for p in partes) - float((w * yv)[na].sum()))
            d_den = abs(den(ref) - sum(den(p) for p in partes) - float(w[na].sum()))
            out[f"{b}-COHERENCIA-{m._slug(e)}-DELTA-NUM-W"] = float(d_num)
            out[f"{b}-COHERENCIA-{m._slug(e)}-DELTA-DEN-W"] = float(d_den)
            out[f"{b}-EJE-{m._slug(e)}-INDEFINIDO-N"] = int(na.sum())
            tol = 1e-6 * max(den(ref), 1.0)
            if d_num > tol or d_den > tol:
                raise RuntimeError(f"COHERENCIA rota: {cid} × {e}: Δnum={d_num} Δden={d_den} (tol {tol})")
        out[f"{b}-N-UNIVERSO"] = int(u.sum())

    # Diagnóstico de flujo y exclusiones (spec §5).
    out.update({
        f"RESULT-{PREFIJO}-FILAS-PERSONAS": int(len(d)),
        f"RESULT-{PREFIJO}-FILAS-PRODUCTO": int(len(largo)),
        f"RESULT-{PREFIJO}-TENEDORES-N": int(tenedor.sum()),
        f"RESULT-{PREFIJO}-SIN-PRODUCTO-N": int(sin_producto.sum()),
        f"RESULT-{PREFIJO}-P6-2-INDEFINIDO-N": int((~tenedor & ~sin_producto).sum()),
        f"RESULT-{PREFIJO}-NUNCA-HA-TENIDO-N": int(nunca.sum()),
        f"RESULT-{PREFIJO}-EX-USUARIOS-N": int((sin_producto & c["P6_14"].eq("1")).sum()),
        f"RESULT-{PREFIJO}-P6-15-FUERA-DE-CATALOGO-N": int((nunca & ~c["P6_15"].isin(list("123456789"))).sum()),
        f"RESULT-{PREFIJO}-P6-15-FUERA-DE-BASE-N": int((~nunca & c["P6_15"].ne("")).sum()),
        f"RESULT-{PREFIJO}-P6-17-FUERA-DE-CATALOGO-N": int((~c["P6_17"].isin(["1", "2", "3"])).sum()),
        f"RESULT-{PREFIJO}-P6-7-NO-SABE-N": int((tenedor & c["P6_7"].eq("9")).sum()),
        f"RESULT-{PREFIJO}-P6-7-BLANCO-EN-TENEDORES-N": int((tenedor & c["P6_7"].eq("")).sum()),
        f"RESULT-{PREFIJO}-P6-7-FUERA-DE-BASE-N": int((~tenedor & c["P6_7"].ne("")).sum()),
        f"RESULT-{PREFIJO}-P6-4-NO-SABE-NO-RESPONDE-N": int(at_held.isin(["8", "9"]).sum().sum()),
        f"RESULT-{PREFIJO}-P6-4-BLANCO-EN-PRODUCTO-TENIDO-N": int((at.eq("").to_numpy() & held).sum()),
        f"RESULT-{PREFIJO}-FORMALIDAD-N-UNIVERSO": int(formalidad.notna().sum()),
        f"RESULT-{PREFIJO}-FORMALIDAD-EXCLUIDOS-P3-10-NO-SABE": int(c["P3_10"].eq("9").sum()),
        f"RESULT-{PREFIJO}-FORMALIDAD-EXCLUIDOS-P3-10-BLANCO": int(c["P3_10"].eq("").sum()),
        f"RESULT-{PREFIJO}-UPM-EN-PLAN": int(len(sorted((big.loc[design, "_est"] + "\t" + big.loc[design, "_upm"]).unique()))),
    })
    return out
