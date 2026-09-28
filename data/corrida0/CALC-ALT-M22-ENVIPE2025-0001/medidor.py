"""Pisos descriptivos RETROSPECTIVOS de CALC-ALTERNOS-LOTE-1: proporciones
ponderadas por celda (nacional, grupo, cruce) con IC bootstrap de UPM dentro
de estrato, y diferencias pareadas entre dos reactivos sobre la misma base.

El primer resultado que produzca este procedimiento es el que se reporta.
Gobernado por la spec humana que cita `spec_md` en el spec.yaml de cada CALC.
El mismo código, autocontenido, se congela en cada CALC del acto; lo que
cambia por CALC (payload, tabla, universo, diseño, reactivos, grupos, códigos)
viene en `parametros`. Lee por `tools/corpus_loader.py::cargar` (caché Parquet
con constancia sha256, o el miembro original como texto crudo), fijado por
sha256. Nunca elige un código: los códigos vienen de la spec, por texto de
pregunta (A.15).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
LOADER = RAIZ / "tools" / "corpus_loader.py"


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def _ref(objeto, nombre="tabla.json"):
    """COMMIT-1-bis (conducto D-22 COMMIT-C): la tabla va a `tablas/` de ESTE
    CALC y el RESULT la cita por REF con su sha256. No cambia qué se mide."""
    calc = Path(__file__).resolve().parent
    carpeta = calc / "tablas"
    if carpeta.is_symlink():
        raise PermissionError("tablas no puede ser enlace")
    carpeta.mkdir(exist_ok=True)
    destino = carpeta / nombre
    raw = (json.dumps(objeto, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False) + "\n").encode("utf-8")
    if destino.exists() and destino.read_bytes() != raw:
        raise PermissionError("tabla existente discordante: no reescribir")
    destino.write_bytes(raw)
    return f"REF:data/corrida0/{calc.name}/tablas/{nombre}#sha256:{hashlib.sha256(raw).hexdigest()}"



def _loader(sha_esperado):
    if _sha(LOADER) != sha_esperado:
        raise ValueError("GUARDIA: sha256 de tools/corpus_loader.py no es el fijado")
    spec = importlib.util.spec_from_file_location("corpus_loader_fijado", LOADER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _cod(s):
    """Código como texto canónico: '01'->'1', 1.0->'1', ' 2 '->'2'; vacío->None."""
    def uno(v):
        if v is None or (isinstance(v, float) and math.isnan(v)) or v is pd.NA:
            return None
        t = str(v).strip()
        if t == "" or t.lower() in ("nan", "<na>", "none"):
            return None
        try:
            f = float(t)
            if math.isfinite(f) and f == int(f):
                return str(int(f))
        except ValueError:
            pass
        return t
    return s.map(uno).astype(object)


def _num(s):
    return pd.to_numeric(s.astype(object).map(lambda v: None if v is None or v is pd.NA else str(v).strip() or None),
                         errors="coerce")


def _conteos_bootstrap(estrato, upm, reps, seed):
    """Matriz reps x n_upm de veces que cada UPM entra, UPM con reemplazo
    dentro de estrato (k UPM -> k extracciones); estrato de UPM única fija."""
    llaves = pd.DataFrame({"e": estrato.astype(str), "u": upm.astype(str)})
    upms = llaves.drop_duplicates().sort_values(["e", "u"]).reset_index(drop=True)
    pos = {(e, u): i for i, (e, u) in enumerate(zip(upms["e"], upms["u"]))}
    rng = np.random.Generator(np.random.PCG64(seed))
    C = np.zeros((reps, len(upms)), dtype=np.float64)
    unica = 0
    for e, g in upms.groupby("e", sort=True):
        idx = g.index.to_numpy()
        k = len(idx)
        if k == 1:
            C[:, idx[0]] = 1.0
            unica += 1
            continue
        tiros = rng.integers(0, k, size=(reps, k))
        for j in range(k):
            C[:, idx[j]] = (tiros == j).sum(axis=1)
    fila_upm = np.fromiter((pos[(e, u)] for e, u in zip(llaves["e"], llaves["u"])),
                           dtype=np.int64, count=len(llaves))
    return C, fila_upm, len(upms), upms["e"].nunique(), unica


def _por_upm(fila_upm, n_upm, valores):
    return np.bincount(fila_upm, weights=valores, minlength=n_upm)


def _ic(C, num_u, den_u):
    d = C @ den_u
    with np.errstate(invalid="ignore", divide="ignore"):
        r = (C @ num_u) / d
    fin = r[np.isfinite(r)]
    if not len(fin):
        return None, 0
    return [float(np.quantile(fin, 0.025)), float(np.quantile(fin, 0.975))], int(len(fin))


def medir(inputs, contrato):
    par = contrato["parametros"]
    cl = _loader(par["corpus_loader_sha256"])
    pid = par["payload_id"]
    if _sha(inputs[pid]["ruta_absoluta"]) != par["hash_payload_sha256"]:
        raise ValueError("GUARDIA: sha256 del payload no es el fijado")
    dis = par.get("diseno") or {}
    cols = set()
    for f in par.get("universo_filtros", []):
        cols.add(f["variable"])
    for it in par["items"]:
        cols.add(it["variable"])
    for g in par.get("grupos", []):
        cols.add(g["variable"])
    for k in ("estrato", "peso"):
        if dis.get(k):
            cols.add(dis[k])
    cols.update(dis.get("upm") or [])
    union = par.get("union")
    derivadas = par.get("derivadas", [])
    nombres_derivados = {dv["nombre"] for dv in derivadas}
    for dv in derivadas:
        for comp in dv.get("variables", []):
            cols.add(comp)
        for comp in dv.get("componentes", []):
            cols.add(comp["variable"])
    traidas = set(union["columnas"]) if union else set()
    propias = (cols - nombres_derivados - traidas) | ({union["llave"]} if union else set())
    df = cl.cargar(pid, par["tabla"], columnas=sorted(propias))
    fuente = df.attrs.get("fuente", "")
    n_filas = int(len(df))
    faltan = sorted(propias - set(df.columns))
    if faltan:
        raise ValueError(f"faltan variables: {faltan}")
    embudo_union = {}
    if union:
        d2 = cl.cargar(pid, union["tabla"], columnas=sorted({union["llave"], *union["columnas"]}))
        fuente += " + " + d2.attrs.get("fuente", "")
        k2 = _cod(d2[union["llave"]])
        if k2.duplicated().any():
            raise ValueError(f"GUARDIA: llave {union['llave']} no única en {union['tabla']}")
        d2 = d2.assign(_k=k2.to_numpy()).drop(columns=[union["llave"]])
        df = df.assign(_k=_cod(df[union["llave"]]).to_numpy()).merge(d2, on="_k", how="left", validate="m:1")
        embudo_union = {"filas_sin_enlace": int(df[union["columnas"][0]].isna().sum())}
    for dv in derivadas:
        if dv["tipo"] == "alguno":
            X = pd.concat([_cod(df[v]) for v in dv["variables"]], axis=1)
            si = X.isin([str(c) for c in dv["si"]]).any(axis=1)
            no = X.isin([str(c) for c in dv["no"]]).all(axis=1)
        elif dv["tipo"] == "y":
            ver = [_cod(df[c["variable"]]).isin([str(x) for x in c["verdad"]]) for c in dv["componentes"]]
            fal = [_cod(df[c["variable"]]).isin([str(x) for x in c["falso"]]) for c in dv["componentes"]]
            si = pd.concat(ver, axis=1).all(axis=1)
            no = pd.concat(fal, axis=1).any(axis=1)
        else:
            raise ValueError(f"derivada de tipo desconocido: {dv['tipo']}")
        df[dv["nombre"]] = np.where(si, "1", np.where(no, "2", None))
    # universo
    en_u = pd.Series(True, index=df.index)
    embudo = {"n_filas": n_filas, **embudo_union}
    for f in par.get("universo_filtros", []):
        ok = _cod(df[f["variable"]]).isin([str(x) for x in f["validos"]])
        embudo["fuera_por_" + f["variable"]] = int((en_u & ~ok).sum())
        en_u &= ok
    if union:
        enlazada = df[union["columnas"][0]].notna()
        embudo["fuera_por_sin_enlace"] = int((en_u & ~enlazada).sum())
        en_u &= enlazada
    w = _num(df[dis["peso"]]) if dis.get("peso") else pd.Series(1.0, index=df.index)
    peso_ok = w.notna() & np.isfinite(w) & (w > 0)
    embudo["fuera_por_peso"] = int((en_u & ~peso_ok).sum())
    en_u &= peso_ok
    con_ic = bool(dis.get("estrato")) and bool(dis.get("upm"))
    if con_ic:
        est = _cod(df[dis["estrato"]])
        partes = [_cod(df[c]) for c in dis["upm"]]
        upm = partes[0].astype(str)
        for p in partes[1:]:
            upm = upm + "|" + p.astype(str)
        dis_ok = est.notna() & partes[0].notna()
        embudo["fuera_por_diseno"] = int((en_u & ~dis_ok).sum())
        en_u &= dis_ok
    d = df[en_u].reset_index(drop=True)
    w = w[en_u].reset_index(drop=True).to_numpy(float)
    embudo["n_universo"] = int(len(d))
    reps = int(par["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    n_min = int(par["n_minimo"])
    if con_ic and len(d):
        C, fila_upm, n_upm, n_est, unica = _conteos_bootstrap(
            est[en_u].reset_index(drop=True), upm[en_u].reset_index(drop=True), reps, seed)
        embudo.update({"n_upm": n_upm, "n_estratos": n_est, "estratos_upm_unica": unica})
    # grupos -> etiqueta por fila (None si fuera de niveles)
    etiquetas = {}
    for g in par.get("grupos", []):
        c = _cod(d[g["variable"]])
        lab = pd.Series([None] * len(d), dtype=object)
        for nivel, codigos in g["niveles"].items():
            lab[c.isin([str(x) for x in codigos])] = nivel
        etiquetas[g["clave"]] = lab
    celdas = [("NACIONAL", pd.Series(True, index=d.index))]
    for g in par.get("grupos", []):
        for nivel in g["niveles"]:
            celdas.append((f"{g['clave']}={nivel}", etiquetas[g["clave"]] == nivel))
    for a, b in par.get("cruces", []):
        for na in next(x for x in par["grupos"] if x["clave"] == a)["niveles"]:
            for nb in next(x for x in par["grupos"] if x["clave"] == b)["niveles"]:
                celdas.append((f"{a}={na}&{b}={nb}",
                               (etiquetas[a] == na) & (etiquetas[b] == nb)))
    # reactivos
    val = {}
    for it in par["items"]:
        x = _cod(d[it["variable"]])
        validos = [str(v) for v in it["validos"]]
        falt = [str(v) for v in it.get("faltantes", [])]
        sust = x.isin(validos)
        nr = x.isna() | x.isin(falt)
        fuera = int((~sust & ~nr).sum())
        val[it["clave"]] = (sust.to_numpy(bool), x.isin([str(v) for v in it["evento"]]).to_numpy(bool),
                            int(nr.sum()), fuera)
    tabla = {"_embudo": embudo, "_fuente_lectura": fuente,
             "_metodo_ic": ("bootstrap UPM con reemplazo dentro de estrato, percentiles 2.5/97.5, "
                            f"{reps} réplicas, semilla {seed}") if con_ic else "SIN-DISENO-DECLARADO: sin IC"}
    for it in par["items"]:
        sust, ev, nr, fuera = val[it["clave"]]
        filas = {"variable": it["variable"], "evento": [str(v) for v in it["evento"]],
                 "n_no_respuesta": nr, "n_fuera_de_escala": fuera}
        if fuera:
            filas["estado"] = "ESCALA-DISCREPANTE"
            tabla[it["clave"]] = filas
            continue
        for nombre, m in celdas:
            mk = m.to_numpy(bool) & sust
            n = int(mk.sum())
            if n < n_min:
                filas[nombre] = {"estado": "NO-ESTIMABLE", "n": n, "p": None, "ic95": None}
                continue
            num = w * (mk & ev)
            den = w * mk
            p = float(num.sum() / den.sum())
            ic, rv = (None, 0)
            if con_ic:
                ic, rv = _ic(C, _por_upm(fila_upm, n_upm, num), _por_upm(fila_upm, n_upm, den))
            filas[nombre] = {"estado": "ESTIMADA", "n": n, "n_evento": int((mk & ev).sum()),
                             "p": p, "ic95": ic, "masa_ponderada": float(den.sum()),
                             "replicas_validas": rv}
        tabla[it["clave"]] = filas
    for dif in par.get("diferencias", []):
        sa, ea, *_ = val[dif["a"]]
        sb, eb, *_ = val[dif["b"]]
        filas = {"definicion": f"p({dif['a']}) - p({dif['b']}) sobre filas sustantivas en ambos"}
        for nombre, m in celdas:
            mk = m.to_numpy(bool) & sa & sb
            n = int(mk.sum())
            if n < n_min:
                filas[nombre] = {"estado": "NO-ESTIMABLE", "n": n, "diferencia": None, "ic95": None}
                continue
            den = w * mk
            na_, nb_ = w * (mk & ea), w * (mk & eb)
            dlt = float((na_.sum() - nb_.sum()) / den.sum())
            ic = None
            if con_ic:
                D = C @ _por_upm(fila_upm, n_upm, den)
                with np.errstate(invalid="ignore", divide="ignore"):
                    r = (C @ _por_upm(fila_upm, n_upm, na_) - C @ _por_upm(fila_upm, n_upm, nb_)) / D
                fin = r[np.isfinite(r)]
                ic = [float(np.quantile(fin, 0.025)), float(np.quantile(fin, 0.975))] if len(fin) else None
            filas[nombre] = {"estado": "ESTIMADA", "n": n, "diferencia": dlt, "ic95": ic}
        tabla[dif["clave"]] = filas
    mascaras = dict(celdas)
    for con in par.get("contrastes", []):
        sust, ev, *_ = val[con["item"]]
        ma = mascaras[con["celda_a"]].to_numpy(bool) & sust
        mb = mascaras[con["celda_b"]].to_numpy(bool) & sust
        fila = {"definicion": f"p({con['item']} | {con['celda_a']}) - p({con['item']} | {con['celda_b']})",
                "n_a": int(ma.sum()), "n_b": int(mb.sum())}
        if min(fila["n_a"], fila["n_b"]) < n_min:
            fila.update({"estado": "NO-ESTIMABLE", "diferencia": None, "ic95": None})
        else:
            na_, da_ = w * (ma & ev), w * ma
            nb_, db_ = w * (mb & ev), w * mb
            fila["diferencia"] = float(na_.sum() / da_.sum() - nb_.sum() / db_.sum())
            fila["ic95"] = None
            if con_ic:
                pu = lambda v: C @ _por_upm(fila_upm, n_upm, v)
                with np.errstate(invalid="ignore", divide="ignore"):
                    r = pu(na_) / pu(da_) - pu(nb_) / pu(db_)
                fin = r[np.isfinite(r)]
                fila["ic95"] = [float(np.quantile(fin, 0.025)), float(np.quantile(fin, 0.975))] if len(fin) else None
            fila["estado"] = "ESTIMADA"
        tabla["CONTRASTE:" + con["clave"]] = fila
    return {par["result_filas"]: n_filas,
            par["result_tabla"]: _ref(tabla)}
