from __future__ import annotations
"""El primer resultado que produzca este procedimiento es el que se reporta.

Pisos históricos de las conductas de crédito K1–K7 por los ejes del marcador,
una ola de ENIF por CALC (2018, 2015, 2012), con el MISMO marco que
CALC-DIN-CREDITO-PISOS-ENIF2021-0001 (#943): ponderador de persona, diseño
estrato × UPM, bootstrap de UPM con 10 000 remuestras PCG64(42), un solo
plan de réplicas por corrida, rejilla leída de las tablas de identidad GEN2
y cortes de eje importados por bytes del medidor sellado de -0003.

Un solo medidor, parametrizado por `contrato["parametros"]["ola"]`. Qué
variable cumple cada rol en cada ola NO vive aquí: se LEE del mapa de
prerregistro (`DIN-CREDITO-PISOS-HISTORIA-mapa-v1_0.tsv`, input `MAPA`),
resuelto por texto de pregunta (A.15), y qué conductas entran a cada ola se
CONTRASTA contra la tabla de comparabilidad v1.1 (`CREDITO-COMPARABILIDAD-
TEXTO`): una conducta sólo se emite si su fila K·ola es MISMO-INSTRUMENTO o
CAMBIO-MENOR, y toda conducta CAMBIO-MENOR lleva su matiz en un RESULT
`-MATIZ` (firma de mesa: «entra a la serie con su matiz escrito»).

ORO (encargo GEN2-DIN-CREDITO-HISTORIA-1 §5 P2): este mismo punto de entrada,
con `ola = 2021`, reproduce los 2 939 RESULT de #943 — lo verifica
tests/test_din_credito_pisos_historia.py. Los tres CALC históricos llevan
este archivo byte a byte.

Spec humana: forense/prereg-caja/DIN-CREDITO-PISOS-HISTORIA-spec-v1_0.md.
"""
import io
import struct
import types
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd

CON = "con seguridad social"
SIN = "sin seguridad social"
N_SOPORTE = 200                       # piso de la casa (n sin ponderar)
EJES_REJILLA = ("sexo", "edad", "escolaridad", "localidad", "cuenta")
CANALES = {"1": "SUCURSAL", "2": "APP", "3": "INTERNET",
           "4": "ESTABLECIMIENTO", "5": "PROMOTOR", "6": "OTRO"}
POSITIVOS = ("MISMO-INSTRUMENTO", "CAMBIO-MENOR")
# rol del mapa que gatea cada conducta; None = siempre construible si la fila
# de comparabilidad lo permite.
ROL_DE = {"K1": "credito_bateria", "K2": "k2_departamental", "K3": "k3_items",
          "K4": "k4_motivo", "K5": "k5", "K6": "k6_atraso", "K7": "k7_canal"}
PAYLOAD_DE = {"2021": "enif2021_csv", "2018": "enif2018_csv",
              "2015": "enif_2015_enif_2015_bd_dbf", "2012": "enif_2012_bases_enif2012_dbf"}
MIEMBROS = {
    "2021": [("csv", "conjunto_de_datos_tmodulo_enif_2021.csv")],
    "2018": [("csv", "conjunto_de_datos/tmodulo.csv")],
    "2015": [("dbf", "tmodulo1.DBF"), ("dbf", "tmodulo2.DBF")],
    "2012": [("dbf", "stmodulo1_e2.dbf"), ("dbf", "stsdem_e2.dbf")],
}


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


def _lista(s):
    return [x.strip() for x in s.split(",") if x.strip()]


def _mapa(inputs, ola):
    """Filas del mapa de prerregistro para esta ola: rol -> fila. Un rol sin
    `variables` es un rol NO-CONSTRUIBLE en esa ola (la fila lo dice)."""
    filas = {f["rol"]: f for f in _tsv(inputs["MAPA"]) if f["ola"] == ola}
    obligatorios = ("llave", "ponderador", "diseno", "sexo", "edad", "escolaridad",
                    "localidad", "cuenta", "formalidad", "credito_filtro",
                    "credito_bateria", "k2_departamental", "k2_nomina", "k2_automotriz",
                    "k3_items", "k4_alguna_vez", "k4_motivo", "k5", "k6_atraso", "k7_canal")
    faltan = [r for r in obligatorios if r not in filas]
    if faltan:
        raise RuntimeError(f"mapa sin filas para ola {ola}: {faltan}")
    return filas


def _rejilla(inputs, con_formalidad):
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
    out = {e: ejes[e] for e in EJES_REJILLA}
    if con_formalidad:
        form = [f for f in _tsv(inputs["PISOS-FORMALIDAD-METADATOS"])
                if (f["source_instrument"], f["source_edition"], f["axis"], f["status"])
                == ("ENIF", "2021", "formalidad", "CONSTRUIBLE")]
        cats = []
        for f in form:
            if f["category"] not in cats:
                cats.append(f["category"])
        if sorted(cats) != sorted([SIN, CON]):
            raise RuntimeError(f"rejilla de formalidad inesperada: {cats}")
        out["formalidad"] = cats
    return out


def _conductas(inputs, ola, mapa):
    """Conductas emitidas en esta ola: la fila K·ola de la tabla de
    comparabilidad debe ser MISMO-INSTRUMENTO o CAMBIO-MENOR y el mapa debe
    traer la variable del rol. Devuelve [(cid, unidad, K, tokens)] en el
    orden de #943 y el matiz por K (alcance + nota de la fila)."""
    filas = {f["conducta"]: f for f in _tsv(inputs["CREDITO-COMPARABILIDAD-TEXTO"])
             if f["ola"] == ola}
    if len(filas) != 8:
        raise RuntimeError(f"la tabla de comparabilidad no trae las 8 filas de {ola}: {sorted(filas)}")
    if filas["K8"]["veredicto"] in POSITIVOS:
        raise RuntimeError("K8 no se mide en ninguna ola de ENIF (FP-404)")
    entra = {k: filas[k]["veredicto"] in POSITIVOS for k in ROL_DE}
    for k in ROL_DE:
        en_mapa = bool(mapa[ROL_DE[k]]["variables"].strip())
        if entra[k] and not en_mapa:
            raise RuntimeError(f"{k}·{ola} es {filas[k]['veredicto']} pero el mapa no trae {ROL_DE[k]}")
        if en_mapa and not entra[k]:
            raise RuntimeError(f"{k}·{ola}: el mapa trae {ROL_DE[k]} pero la tabla dice {filas[k]['veredicto']}")
    bat = mapa["credito_bateria"]["variables"]; k6 = mapa["k6_atraso"]["variables"]
    todas = [
        ("K1", "P", "K1", (bat.split(",")[0].rsplit("_", 1)[0],)),
        ("K2-DEPARTAMENTAL", "P", "K2", (mapa["k2_departamental"]["variables"],)),
        ("K2-NOMINA", "P", "K2", (mapa["k2_nomina"]["variables"],)),
        ("K2-AUTOMOTRIZ", "P", "K2", (mapa["k2_automotriz"]["variables"],)),
        ("K3", "P", "K3", (mapa["k3_items"]["variables"].split(",")[0].rsplit("_", 1)[0],)),
        ("K4A-AUTOEXCLUSION", "P", "K4", (mapa["k4_motivo"]["variables"],)),
        ("K4B-OFERTA", "P", "K4", (mapa["k4_motivo"]["variables"],)),
        ("K4B1-REQUISITOS", "P", "K4", (mapa["k4_motivo"]["variables"],)),
        ("K4B2-ACCESO", "P", "K4", (mapa["k4_motivo"]["variables"],)),
        ("K4B3-RECHAZO-ANTICIPADO", "P", "K4", (mapa["k4_motivo"]["variables"],)),
        ("K5", "P", "K5", (mapa["k5"]["variables"],)),
        ("K5-ENTRE-SOLICITANTES", "P", "K5", (mapa["k5"]["variables"],)),
        ("K6-PR", "PR", "K6", (k6.split(",")[0].rsplit("_", 1)[0],)),
        ("K6-P-TENEDORES", "P", "K6", (k6.split(",")[0].rsplit("_", 1)[0],)),
    ] + [(f"K7-{v}", "PR", "K7", (mapa["k7_canal"]["variables"],)) for v in CANALES.values()]
    conductas = [c for c in todas if entra[c[2]]]
    for cid, unidad, k, tokens in conductas:
        f = filas[k]
        for t in tokens:
            if t and t not in f["reactivo"]:
                raise RuntimeError(f"{cid}·{ola}: el reactivo {t!r} no está en la fila {k}·{ola}")
        u = f["unidad"]
        if unidad == "PR" and not u.startswith("PR"):
            raise RuntimeError(f"{cid}: unidad PR no coincide con la tabla ({u!r})")
        if unidad == "P" and cid != "K6-P-TENEDORES" and (not u.startswith("P") or u.startswith("PR")):
            raise RuntimeError(f"{cid}: unidad P no coincide con la tabla ({u!r})")
        if cid == "K6-P-TENEDORES" and "agregable a P" not in u:
            raise RuntimeError(f"{cid}: la tabla no declara K6 agregable a P ({u!r})")
    matiz = {k: (filas[k]["veredicto"], filas[k]["alcance_del_veredicto"]) for k in ROL_DE}
    return conductas, matiz


# ----------------------------------------------------------------- lectura
def _csv_zip(path, sufijo, cols):
    """Como `_csv` de -0003, con los nombres de columna en MAYÚSCULAS (el
    CSV de 2018 los trae en minúsculas)."""
    with zipfile.ZipFile(path) as zf:
        names = [n for n in zf.namelist() if n.lower().endswith(sufijo.lower())]
        if len(names) != 1:
            raise RuntimeError(f"miembro CSV no único: {sufijo}: {names}")
        raw = zf.read(names[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            d = pd.read_csv(io.StringIO(raw.decode(enc)), dtype=str,
                            keep_default_na=False, na_filter=False)
        except UnicodeDecodeError:
            continue
        d.columns = [str(x).strip().upper() for x in d.columns]
        missing = sorted(set(cols) - set(d.columns))
        if missing:
            raise RuntimeError(f"variables ausentes en {sufijo}: {missing}")
        return d[cols].copy()
    raise RuntimeError(f"codificación no reconocida: {sufijo}")


def _dbf_zip(path, miembro, cols):
    """Lector DBF mínimo (dBase III/FoxPro, campos C/N de ancho fijo): lee la
    cabecera del propio archivo —el descriptor de campos, no el FD— y
    devuelve las columnas pedidas como texto sin recortar. Registros
    marcados como borrados (0x2A) se excluyen y se cuentan aparte."""
    with zipfile.ZipFile(path) as zf:
        names = [n for n in zf.namelist() if n.lower() == miembro.lower()]
        if len(names) != 1:
            raise RuntimeError(f"miembro DBF no único: {miembro}: {names}")
        raw = zf.read(names[0])
    n_rec = struct.unpack("<I", raw[4:8])[0]
    h_len, r_len = struct.unpack("<HH", raw[8:12])
    campos = []
    p = 32
    while raw[p] != 0x0D:
        nombre = raw[p:p + 11].split(b"\0")[0].decode("latin-1").strip().upper()
        campos.append((nombre, raw[p + 16]))
        p += 32
    nombres = [c[0] for c in campos]
    missing = sorted(set(cols) - set(nombres))
    if missing:
        raise RuntimeError(f"variables ausentes en {miembro}: {missing}")
    offs = {}
    o = 1
    for nombre, ln in campos:
        offs[nombre] = (o, o + ln)
        o += ln
    if o != r_len:
        raise RuntimeError(f"{miembro}: suma de anchos {o} != longitud de registro {r_len}")
    datos = {c: [] for c in cols}
    borrados = 0
    for i in range(n_rec):
        rec = raw[h_len + i * r_len: h_len + (i + 1) * r_len]
        if len(rec) < r_len:
            raise RuntimeError(f"{miembro}: registro {i} truncado")
        if rec[0:1] == b"*":
            borrados += 1
            continue
        for c in cols:
            a, b = offs[c]
            datos[c].append(rec[a:b].decode("latin-1"))
    d = pd.DataFrame(datos, dtype=str)
    d.attrs["registros_borrados"] = borrados
    return d


def _carga(inputs, ola, mapa):
    """Marco persona de la ola, con las columnas de todos los roles, ya
    unidas por la llave del mapa cuando la sección 6 vive en dos tablas."""
    ruta = inputs[PAYLOAD_DE[ola]]["ruta_absoluta"]
    roles_vars = {r: _lista(f["variables"]) for r, f in mapa.items() if f["variables"].strip()}
    diag = {}
    if ola in ("2021", "2018"):
        cols = sorted({v for r, vs in roles_vars.items() if r != "llave" for v in vs})
        d = _csv_zip(ruta, MIEMBROS[ola][0][1], cols)
    elif ola == "2015":
        llaves = roles_vars["llave"]
        por_miembro = {}
        for r, f in mapa.items():
            if r == "llave" or not f["variables"].strip():
                continue
            por_miembro.setdefault(f["miembro"], set()).update(_lista(f["variables"]))
        t1 = _dbf_zip(ruta, "tmodulo1.DBF", llaves + sorted(por_miembro["tmodulo1.DBF"]))
        t2 = _dbf_zip(ruta, "tmodulo2.DBF", llaves + sorted(por_miembro["tmodulo2.DBF"]))
        if t1.duplicated(llaves).any() or t2.duplicated(llaves).any():
            raise RuntimeError("2015: llave duplicada en TModulo1 o TModulo2")
        d = t1.merge(t2, on=llaves, how="inner", validate="one_to_one")
        if len(d) != len(t1) or len(d) != len(t2):
            raise RuntimeError(f"2015: el join pierde filas: {len(t1)} / {len(t2)} -> {len(d)}")
        diag["REGISTROS-DBF-BORRADOS"] = int(t1.attrs["registros_borrados"] + t2.attrs["registros_borrados"])
    elif ola == "2012":
        llave = roles_vars["llave"]          # CONTROL,VIV_SEL,HOGAR,R_SEL=N_REN
        ll1 = [k.split("=")[0] for k in llave]
        ll2 = [k.split("=")[-1] for k in llave]
        por_miembro = {}
        for r, f in mapa.items():
            if r == "llave" or not f["variables"].strip():
                continue
            por_miembro.setdefault(f["miembro"], set()).update(_lista(f["variables"]))
        t1 = _dbf_zip(ruta, "stmodulo1_e2.dbf", ll1 + sorted(por_miembro["stmodulo1_e2.dbf"]))
        ts = _dbf_zip(ruta, "stsdem_e2.dbf", ll2 + sorted(por_miembro["stsdem_e2.dbf"]))
        for t, ll in ((t1, ll1), (ts, ll2)):
            for k in ll:
                t[k] = t[k].str.strip()
        if t1.duplicated(ll1).any():
            raise RuntimeError("2012: llave duplicada en TMODULO1")
        diag["TSDEM-LLAVE-DUPLICADA-N"] = int(ts.duplicated(ll2).sum())
        ts = ts.drop_duplicates(ll2)         # una persona por renglón; si hubiera dup, gana la primera (contado arriba)
        d = t1.merge(ts, left_on=ll1, right_on=ll2, how="left", validate="one_to_one")
        if len(d) != len(t1):
            raise RuntimeError(f"2012: el join cambia el número de filas: {len(t1)} -> {len(d)}")
        for v in por_miembro["stsdem_e2.dbf"]:
            d[v] = d[v].fillna("")
        diag["FILAS-SIN-SOCIODEMOGRAFICO-N"] = int(d[sorted(por_miembro["stsdem_e2.dbf"])[0]].eq("").sum())
        diag["REGISTROS-DBF-BORRADOS"] = int(t1.attrs["registros_borrados"] + ts.attrs["registros_borrados"])
    else:
        raise RuntimeError(f"ola no prevista: {ola}")
    return d, roles_vars, diag


def _dicot(code, unos, ceros):
    out = pd.Series(pd.NA, index=code.index, dtype="Float64")
    out.loc[code.isin(list(ceros))] = 0.0
    out.loc[code.isin(list(unos))] = 1.0
    return out


def medir(inputs, contrato):
    ola = str(contrato["parametros"]["ola"])
    PREFIJO = f"DIN-CREDITO-PISOS-ENIF{ola}"
    m = _modulo_0003(inputs)
    mapa = _mapa(inputs, ola)
    con_form = bool(mapa["formalidad"]["variables"].strip())
    rejilla = _rejilla(inputs, con_form)
    CONDUCTAS, matiz = _conductas(inputs, ola, mapa)
    d, rv, diag = _carga(inputs, ola, mapa)

    pond = rv["ponderador"][0]
    est, upm = rv["diseno"]
    d["_w"] = pd.to_numeric(d[pond].str.strip(), errors="coerce")
    d["_est"] = d[est].str.strip(); d["_upm"] = d[upm].str.strip()
    c = {v: m._code(d[v]) for r, vs in rv.items() if r not in ("llave", "ponderador", "diseno") for v in vs}

    # Ejes: cortes del medidor sellado de -0003 (importados); cuenta y
    # formalidad con la regla del mapa (filtro/s Sí-No o batería).
    cu = d[rv["cuenta"]].apply(m._code)
    account = pd.Series(pd.NA, index=d.index, dtype="object")
    account.loc[cu.eq("1").any(axis=1)] = "con cuenta"
    account.loc[cu.eq("2").all(axis=1)] = "sin cuenta"
    ejes_p = {
        "sexo": c[rv["sexo"][0]].where(c[rv["sexo"][0]].isin(["1", "2"]), pd.NA),
        "edad": m._age(d[rv["edad"][0]].str.strip()),
        "escolaridad": m._school(d[rv["escolaridad"][0]]),
        "localidad": m._code(d[rv["localidad"][0]]).map({"1": "15 000 y mas", "2": "15 000 y mas",
                                                          "3": "menor de 15 000", "4": "menor de 15 000"}),
        "cuenta": account,
    }
    formalidad = None
    if con_form:
        fv = c[rv["formalidad"][0]]
        formalidad = pd.Series(pd.NA, index=d.index, dtype="object")
        formalidad.loc[fv.isin(_lista(mapa["formalidad"]["codigos_1"]))] = CON
        formalidad.loc[fv.isin(_lista(mapa["formalidad"]["codigos_0"]))] = SIN
        ejes_p["formalidad"] = formalidad
    for e, cats in rejilla.items():
        vistos = set(ejes_p[e].dropna().unique())
        if not vistos <= set(cats):
            raise RuntimeError(f"eje {e}: categorías fuera de la rejilla GEN2: {sorted(vistos - set(cats))}")

    # Tenencia de crédito formal: batería (universal en 2021) gateada por el
    # filtro de la ola cuando lo hay (spec §2).
    BAT = rv["credito_bateria"]
    pr = d[BAT].apply(m._code)
    if "credito_filtro" in rv:
        fl = d[rv["credito_filtro"]].apply(m._code)
        tenedor = pr.eq("1").any(axis=1) | fl.eq("1").any(axis=1)
        sin_producto = fl.eq("2").all(axis=1)
        filtro_si_bateria_no = fl.eq("1").any(axis=1) & pr.eq("2").all(axis=1)
    else:
        tenedor = pr.eq("1").any(axis=1)
        sin_producto = pr.eq("2").all(axis=1)
        filtro_si_bateria_no = pd.Series(False, index=d.index)
    orden = [cid for cid, _u, _k, _t in CONDUCTAS]
    y = {}
    if "K1" in orden:
        y["K1"] = pd.Series(pd.NA, index=d.index, dtype="Float64")
        y["K1"].loc[sin_producto] = 0.0; y["K1"].loc[tenedor] = 1.0
    for cid, rol in (("K2-DEPARTAMENTAL", "k2_departamental"), ("K2-NOMINA", "k2_nomina"),
                     ("K2-AUTOMOTRIZ", "k2_automotriz")):
        if cid in orden:
            v = rv[rol][0]
            s = _dicot(c[v], "1", "2")
            s.loc[sin_producto & c[v].eq("")] = 0.0        # blanco por pase = No
            y[cid] = s
    if "K3" in orden:
        inf = d[rv["k3_items"]].apply(m._code)
        y["K3"] = pd.Series(pd.NA, index=d.index, dtype="Float64")
        y["K3"].loc[inf.eq("2").all(axis=1)] = 0.0; y["K3"].loc[inf.eq("1").any(axis=1)] = 1.0
    nunca = ex = None
    if "k4_alguna_vez" in rv:
        av = c[rv["k4_alguna_vez"][0]]
        nunca = sin_producto & av.eq("2")                    # base de K4: «nunca ha tenido»
        ex = sin_producto & av.eq("1")
    if "K4A-AUTOEXCLUSION" in orden:
        mot = rv["k4_motivo"][0]
        cat4 = _lista(mapa["k4_motivo"]["codigos_0"])
        grupos = [_lista(g) for g in mapa["k4_motivo"]["codigos_1"].split("|")]
        p6 = c[mot].where(nunca, "")
        for cid, unos in zip(("K4A-AUTOEXCLUSION", "K4B-OFERTA", "K4B1-REQUISITOS",
                              "K4B2-ACCESO", "K4B3-RECHAZO-ANTICIPADO"), grupos):
            y[cid] = _dicot(p6, unos, [x for x in cat4 if x not in unos])
    if "K5" in orden:
        k5 = c[rv["k5"][0]]
        y["K5"] = _dicot(k5, "1", _lista(mapa["k5"]["codigos_0"]))
        y["K5-ENTRE-SOLICITANTES"] = _dicot(k5, "1", "2")
    # K6: atraso por producto, posicional con los primeros len(ATR) ítems.
    ATR = rv["k6_atraso"] if "k6_atraso" in rv else []
    at = d[ATR].apply(m._code) if ATR else pd.DataFrame(index=d.index)
    unos6 = _lista(mapa["k6_atraso"]["codigos_1"]) if ATR else []
    ceros6 = _lista(mapa["k6_atraso"]["codigos_0"]) if ATR else []
    held_all = pr.eq("1").to_numpy()
    held = held_all[:, :len(ATR)]                           # comparación POSICIONAL (defecto de -0002)
    if "K6-P-TENEDORES" in orden:
        at_held = at.where(held, "")
        cubierto = pd.Series(held.any(axis=1), index=d.index)
        y["K6-P-TENEDORES"] = pd.Series(pd.NA, index=d.index, dtype="Float64")
        y["K6-P-TENEDORES"].loc[tenedor & cubierto & (at_held.isin(ceros6).to_numpy() | ~held).all(axis=1)] = 0.0
        y["K6-P-TENEDORES"].loc[tenedor & at_held.isin(unos6).any(axis=1)] = 1.0
    else:
        at_held = at
    if "K7-SUCURSAL" in orden:
        p67 = c[rv["k7_canal"][0]].where(tenedor, "")
        for code, nombre in CANALES.items():
            y[f"K7-{nombre}"] = _dicot(p67, code, "".join(sorted(set("123456") - {code})))

    # Unidad PR de K6: una fila por producto formal tenido CON variable de atraso.
    largos = []
    for k, (pcol, acol) in enumerate(zip(BAT, ATR), start=1):
        idx = d.index[pr[pcol].eq("1")]
        if len(idx) == 0:
            continue
        bloque = pd.DataFrame({"_w": d.loc[idx, "_w"], "_est": d.loc[idx, "_est"],
                               "_upm": d.loc[idx, "_upm"], "_producto": k,
                               "_y": _dicot(at.loc[idx, acol], unos6, ceros6).astype("Float64")})
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
    if "K6-PR" in orden:
        s = pd.Series(pd.NA, index=big.index, dtype="Float64")
        if len(largo):
            s.iloc[n_p:] = largo["_y"].to_numpy()
        yb["K6-PR"] = s

    todos = pd.Series("todos", index=big.index, dtype="object")
    axes = {"nacional": (todos, ("todos",))}
    axes.update({e: (ejes_b[e], tuple(rejilla[e])) for e in rejilla})
    if con_form:
        trabaja = pd.Series("universo trabaja", index=big.index, dtype="object").where(
            ejes_b["formalidad"].notna(), pd.NA)
        axes["universo"] = (trabaja, ("universo trabaja",))
    cells = []
    for cid in orden:
        cells += m._cells(f"{PREFIJO}-{cid}", yb[cid], axes)
    out = m._estimate(big, cells, int(contrato["parametros"]["bootstrap_replicas"]),
                      int(contrato["seed"]["valor"]))

    # Guardias (spec §4): unidad y matiz por conducta, soporte por celda,
    # coherencia por conducta × eje contra el marginal nacional (formalidad
    # contra el universo de quien trabaja). Coherencia rota -> PARA.
    design = big["_w"].notna() & (big["_w"] > 0) & big["_est"].ne("") & big["_upm"].ne("")
    unidad = {cid: u for cid, u, _k, _t in CONDUCTAS}
    kde = {cid: k for cid, _u, k, _t in CONDUCTAS}
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
        if ola != "2021":
            ver, alc = matiz[kde[cid]]
            out[f"{b}-VEREDICTO-TEXTO"] = ver
            out[f"{b}-MATIZ"] = alc

    # Diagnóstico de flujo y exclusiones (spec §5), con nombres por rol.
    P = f"RESULT-{PREFIJO}"
    out.update({
        f"{P}-FILAS-PERSONAS": int(len(d)),
        f"{P}-FILAS-PRODUCTO": int(len(largo)),
        f"{P}-TENEDORES-N": int(tenedor.sum()),
        f"{P}-SIN-PRODUCTO-N": int(sin_producto.sum()),
        f"{P}-TENENCIA-INDEFINIDO-N": int((~tenedor & ~sin_producto).sum()),
        f"{P}-K6-ATRASO-NO-SABE-NO-RESPONDE-N": int(at_held.isin(["8", "9"]).sum().sum()) if ATR else 0,
        f"{P}-K6-ATRASO-BLANCO-EN-PRODUCTO-TENIDO-N": int((at.eq("").to_numpy() & held).sum()) if ATR else 0,
        f"{P}-K6-PRODUCTOS-TENIDOS-SIN-VARIABLE-DE-ATRASO-N": int(held_all[:, len(ATR):].sum()),
        f"{P}-UPM-EN-PLAN": int(len(sorted((big.loc[design, "_est"] + "\t" + big.loc[design, "_upm"]).unique()))),
    })
    if "K5" in orden:
        out[f"{P}-K5-FUERA-DE-CATALOGO-N"] = int((~c[rv["k5"][0]].isin(["1", "2", "3"])).sum())
    if nunca is not None:
        out[f"{P}-NUNCA-HA-TENIDO-N"] = int(nunca.sum())
        out[f"{P}-EX-USUARIOS-N"] = int(ex.sum())
    if "K4A-AUTOEXCLUSION" in orden:
        mot = c[rv["k4_motivo"][0]]
        out[f"{P}-K4-MOTIVO-FUERA-DE-CATALOGO-N"] = int((nunca & ~mot.isin(cat4)).sum())
        out[f"{P}-K4-MOTIVO-FUERA-DE-BASE-N"] = int((~nunca & mot.ne("")).sum())
    if "K7-SUCURSAL" in orden:
        k7 = c[rv["k7_canal"][0]]
        out[f"{P}-K7-NO-SABE-N"] = int((tenedor & k7.eq("9")).sum())
        out[f"{P}-K7-BLANCO-EN-TENEDORES-N"] = int((tenedor & k7.eq("")).sum())
        out[f"{P}-K7-FUERA-DE-BASE-N"] = int((~tenedor & k7.ne("")).sum())
    if con_form:
        fv = c[rv["formalidad"][0]]
        out[f"{P}-FORMALIDAD-N-UNIVERSO"] = int(formalidad.notna().sum())
        out[f"{P}-FORMALIDAD-EXCLUIDOS-NO-SABE"] = int(fv.eq("9").sum())
        out[f"{P}-FORMALIDAD-EXCLUIDOS-BLANCO"] = int(fv.eq("").sum())
    if ola != "2021":
        out[f"{P}-FILTRO-SI-BATERIA-TODO-NO-N"] = int(filtro_si_bateria_no.sum())
        out[f"{P}-POBLACION-BASE"] = "persona elegida de 18 a 70 años (diseño de la ola); NACIONAL y 60+ no son conmensurables con 2021 (18+) sin recorte"
        out[f"{P}-FORMALIDAD-EJE"] = "CONSTRUIBLE" if con_form else "NO-CONSTRUIBLE-POR-TEXTO (mapa: rol formalidad)"
        out[f"{P}-CONDUCTAS-EMITIDAS-N"] = int(len(orden))
        for k in ROL_DE:
            out[f"{P}-{k}-VEREDICTO-TABLA"] = matiz[k][0]
        for k, v in diag.items():
            out[f"{P}-{k}"] = v
    return out
