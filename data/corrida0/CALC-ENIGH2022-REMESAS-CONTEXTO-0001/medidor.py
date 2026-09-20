"""Remesas por localidad y estrato socioeconomico, hogares ENIGH 2022."""
from __future__ import annotations

import csv
import io
import json
import math
import zipfile

import numpy as np


ZIP_ID = "enigh2022_nc_csv"
P = "RESULT-ENIGH22-REMCTX-"
MIEMBRO = (
    "conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/"
    "conjunto_de_datos_concentradohogar_enigh2022_ns.csv"
)
COLUMNAS = ["folioviv", "foliohog", "factor", "remesas", "ing_cor",
            "tam_loc", "est_socio", "est_dis", "upm"]
CATALOGOS = {
    "tam_loc": [("1", "100 000 y más"), ("2", "15 000 a 99 999"),
                ("3", "2 500 a 14 999"), ("4", "Menos de 2 500")],
    "est_socio": [("1", "Bajo"), ("2", "Medio bajo"),
                  ("3", "Medio alto"), ("4", "Alto")],
}
METRICAS = ("prevalencia", "remesas_media", "remesas_mediana",
            "participacion_media", "participacion_agregada", "ge50")


def _texto(x):
    if x is None:
        return None
    s = str(x).lstrip("\ufeff").lstrip("ï»¿").strip().strip('"')
    return s or None


def _numero(x):
    s = _texto(x)
    if s is None:
        return None
    try:
        v = float(s.replace(",", ""))
    except ValueError:
        return None
    return v if math.isfinite(v) else None


def mediana_ponderada(valores, pesos):
    v = np.asarray(valores, dtype=float)
    w = np.asarray(pesos, dtype=float)
    ok = np.isfinite(v) & np.isfinite(w) & (w > 0)
    if not np.any(ok):
        return None
    orden = np.argsort(v[ok], kind="stable")
    vv, ww = v[ok][orden], w[ok][orden]
    pos = int(np.searchsorted(np.cumsum(ww), ww.sum() / 2.0, side="left"))
    return float(vv[min(pos, len(vv) - 1)])


def _abre(zf):
    with zf.open(MIEMBRO) as fh:
        rd = csv.reader(io.TextIOWrapper(fh, encoding="latin-1", newline=""))
        try:
            head = [(_texto(x) or "").lower() for x in next(rd)]
        except StopIteration:
            return [], COLUMNAS, 0
        idx = {c: head.index(c) for c in COLUMNAS if c in head}
        falta = [c for c in COLUMNAS if c not in idx]
        filas = [{c: (r[idx[c]] if c in idx and idx[c] < len(r) else None)
                  for c in COLUMNAS} for r in rd if r]
        return filas, falta, len(head)


def _j(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def _f(x):
    return float(x) if x is not None and math.isfinite(float(x)) else None


def _metricas(a, idx, ew):
    if idx.size == 0:
        return [None] * 6
    w = ew[idx]
    rv = a["rem_val"][idx]
    rec = rv & (a["r"][idx] > 0) & (w > 0)
    den_prev = w[rv].sum()
    prev = w[rec].sum() / den_prev if den_prev > 0 else None
    if np.any(rec):
        wr, rr = w[rec], a["r"][idx][rec]
        rmedia = np.dot(wr, rr) / wr.sum()
        rmed = mediana_ponderada(rr, wr)
    else:
        rmedia = rmed = None
    part = rec & a["ing_pos"][idx]
    if np.any(part):
        wp, rp, yp = w[part], a["r"][idx][part], a["y"][idx][part]
        ratio = rp / yp
        pmedia = np.dot(wp, ratio) / wp.sum()
        pag = np.dot(wp, rp) / np.dot(wp, yp) if np.dot(wp, yp) > 0 else None
        ge = wp[ratio >= .5].sum() / wp.sum()
    else:
        pmedia = pag = ge = None
    return [_f(x) for x in (prev, rmedia, rmed, pmedia, pag, ge)]


def _perfiles(a):
    out = [("total", "TOTAL", "Total", np.flatnonzero(a["w_ok"]))]
    for eje in ("tam_loc", "est_socio"):
        validos = {c for c, _ in CATALOGOS[eje]}
        for codigo, etiqueta in CATALOGOS[eje]:
            out.append((eje, codigo, etiqueta,
                        np.flatnonzero(a["w_ok"] & (a[eje] == codigo))))
        out.append((eje, "RESIDUO", "Ausente/desconocido",
                    np.flatnonzero(a["w_ok"] & ~np.isin(a[eje], list(validos)))))
    return out


def _fila_tabla(a, eje, codigo, etiqueta, idx, punto, tol):
    w = a["w"][idx]
    rv = a["rem_val"][idx]
    rec = rv & (a["r"][idx] > 0)
    part = rec & a["ing_pos"][idx]
    ing_missing = rec & ~a["ing_fin"][idx]
    ing_zero = rec & a["ing_fin"][idx] & (a["y"][idx] == 0)
    ing_neg = rec & a["ing_fin"][idx] & (a["y"][idx] < 0)
    incompat = part & (a["r"][idx] > a["y"][idx] + tol)
    inval = ~rv
    neg = a["rem_fin"][idx] & (a["r"][idx] < 0)
    miss = ~a["rem_fin"][idx]
    estado = "VACIA" if idx.size == 0 else (
        "REPORTADO-CON-INCOMPATIBILIDAD" if np.any(incompat) else "REPORTADO")
    d = {
        "eje": eje, "codigo": codigo, "etiqueta": etiqueta, "estado": estado,
        "elegibles_n": int(idx.size), "elegibles_masa": float(w.sum()),
        "remesas_validas_n": int(rv.sum()), "remesas_validas_masa": float(w[rv].sum()),
        "remesas_no_validas_n": int(inval.sum()), "remesas_no_validas_masa": float(w[inval].sum()),
        "remesas_ausentes_no_finitas_n": int(miss.sum()),
        "remesas_negativas_n": int(neg.sum()),
        "receptores_n": int(rec.sum()), "receptores_masa": float(w[rec].sum()),
        "participacion_n": int(part.sum()), "participacion_masa": float(w[part].sum()),
        "ing_cor_ausente_no_finito_n": int(ing_missing.sum()),
        "ing_cor_ausente_no_finito_masa": float(w[ing_missing].sum()),
        "ing_cor_cero_n": int(ing_zero.sum()), "ing_cor_cero_masa": float(w[ing_zero].sum()),
        "ing_cor_negativo_n": int(ing_neg.sum()), "ing_cor_negativo_masa": float(w[ing_neg].sum()),
        "r_mayor_y_n": int(incompat.sum()), "r_mayor_y_masa": float(w[incompat].sum()),
    }
    d.update(dict(zip(METRICAS, punto)))
    return d


def _clusters(a):
    pares = [(a["est"][i], a["upm"][i]) for i in range(len(a["w"]))]
    if any(x is None or y is None for x, y in pares):
        return None, None, None
    unicos = sorted(set(pares))
    mapa = {k: i for i, k in enumerate(unicos)}
    fila_cluster = np.asarray([mapa[k] for k in pares], dtype=int)
    estratos = {}
    for i, (est, _upm) in enumerate(unicos):
        estratos.setdefault(est, []).append(i)
    return fila_cluster, [np.asarray(estratos[e], dtype=int) for e in sorted(estratos)], unicos


def _independiente_media(a, fila_cluster, bloques):
    rec = a["w_ok"] & a["rem_val"] & (a["r"] > 0)
    den = math.fsum(float(x) for x in a["w"][rec])
    media = math.fsum(float(x) for x in (a["w"][rec] * a["r"][rec])) / den
    z = np.zeros(int(fila_cluster.max()) + 1)
    np.add.at(z, fila_cluster[rec], a["w"][rec] * (a["r"][rec] - media))
    var = 0.0
    for b in bloques:
        if len(b) > 1:
            var += len(b) / (len(b) - 1) * float(np.square(z[b] - z[b].mean()).sum())
    return media, math.sqrt(var) / den


def _vacio(estado):
    return {
        P + "ESTADO": estado, P + "N-FILAS": 0, P + "N-COLUMNAS": 0,
        P + "LLAVE-HOGAR-UNICA": "NO-EVALUADO", P + "TABLA-JSON": "[]",
        P + "CONTRASTES-JSON": "[]", P + "DISENO-JSON": "{}",
        P + "CONTROLES-JSON": "{}", P + "INDEPENDIENTE-JSON": "{}",
        P + "RECONSTRUCCION-JSON": "{}", P + "CATALOGOS-JSON": _j(CATALOGOS),
    }


def medir(inputs, contrato):
    par = contrato["parametros"]
    replicas = int(par["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    tol = float(par["tolerancia_componente_pesos"])
    with zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"]) as zf:
        if MIEMBRO not in set(zf.namelist()):
            return _vacio("NO-ESTIMABLE-MIEMBRO-AUSENTE")
        filas, falta, ncol = _abre(zf)
    out = _vacio("NO-ESTIMABLE")
    out[P + "N-FILAS"], out[P + "N-COLUMNAS"] = len(filas), ncol
    if falta:
        out[P + "ESTADO"] = "NO-ESTIMABLE-COLUMNAS:" + ",".join(falta)
        return out
    llaves = [(_texto(x["folioviv"]), _texto(x["foliohog"])) for x in filas]
    if any(None in k for k in llaves) or len(set(llaves)) != len(llaves):
        out[P + "LLAVE-HOGAR-UNICA"] = "NO"
        out[P + "ESTADO"] = "NO-ESTIMABLE-LLAVE"
        return out
    out[P + "LLAVE-HOGAR-UNICA"] = "SI"
    n = len(filas)
    nums = {c: [_numero(x[c]) for x in filas] for c in ("factor", "remesas", "ing_cor")}
    a = {
        "w": np.asarray([x if x is not None else 0.0 for x in nums["factor"]]),
        "r": np.asarray([x if x is not None else 0.0 for x in nums["remesas"]]),
        "y": np.asarray([x if x is not None else 0.0 for x in nums["ing_cor"]]),
        "tam_loc": np.asarray([_texto(x["tam_loc"]) for x in filas], dtype=object),
        "est_socio": np.asarray([_texto(x["est_socio"]) for x in filas], dtype=object),
        "est": [_texto(x["est_dis"]) for x in filas],
        "upm": [_texto(x["upm"]) for x in filas],
    }
    a["w_ok"] = np.asarray([x is not None and x > 0 for x in nums["factor"]])
    a["rem_fin"] = np.asarray([x is not None for x in nums["remesas"]])
    a["rem_val"] = a["rem_fin"] & (a["r"] >= 0)
    a["ing_fin"] = np.asarray([x is not None for x in nums["ing_cor"]])
    a["ing_pos"] = a["ing_fin"] & (a["y"] > 0)
    perfiles = _perfiles(a)
    puntos = [_metricas(a, idx, a["w"]) for *_x, idx in perfiles]
    tabla = [_fila_tabla(a, eje, cod, et, idx, pt, tol)
             for (eje, cod, et, idx), pt in zip(perfiles, puntos)]
    fila_cluster, bloques, clusters = _clusters(a)
    reps = np.full((replicas, len(perfiles), len(METRICAS)), np.nan)
    metodo = "NO-ESTIMABLE-DISENO-INCOMPLETO"
    if fila_cluster is not None and clusters:
        rng = np.random.Generator(np.random.PCG64(seed))
        for b in range(replicas):
            mult = np.zeros(len(clusters))
            for bloque in bloques:
                elegido = bloque[rng.integers(0, len(bloque), size=len(bloque))]
                np.add.at(mult, elegido, 1.0)
            ew = a["w"] * mult[fila_cluster]
            for g, (*_x, idx) in enumerate(perfiles):
                vals = _metricas(a, idx, ew)
                reps[b, g] = [np.nan if x is None else x for x in vals]
        metodo = "BOOTSTRAP-UPM-EN-ESTRATO-PERCENTIL"
    for g, row in enumerate(tabla):
        for m, nombre in enumerate(METRICAS):
            vals = reps[:, g, m]
            fin = vals[np.isfinite(vals)]
            row[nombre + "_replicas_validas"] = int(fin.size)
            row[nombre + "_replicas_degeneradas"] = int(replicas - fin.size)
            row[nombre + "_ic95_lo"] = float(np.percentile(fin, 2.5)) if fin.size else None
            row[nombre + "_ic95_hi"] = float(np.percentile(fin, 97.5)) if fin.size else None
            row[nombre + "_ic_causa"] = None if fin.size else (
                "GRUPO-O-DENOMINADOR-NULO" if fila_cluster is not None else "DISENO-INCOMPLETO")
    pos = {(e, c): i for i, (e, c, _l, _idx) in enumerate(perfiles)}
    contrastes = []
    for eje, a_cod, b_cod, etiqueta in (
        ("tam_loc", "4", "1", "menor_tamaño_menos_mayor_tamaño"),
        ("est_socio", "1", "4", "inferior_menos_superior"),
    ):
        ia, ib = pos[(eje, a_cod)], pos[(eje, b_cod)]
        for nombre in ("prevalencia", "participacion_media", "ge50"):
            m = METRICAS.index(nombre)
            punto = None if puntos[ia][m] is None or puntos[ib][m] is None else puntos[ia][m] - puntos[ib][m]
            dif = reps[:, ia, m] - reps[:, ib, m]
            fin = dif[np.isfinite(dif)]
            contrastes.append({"eje": eje, "direccion": etiqueta,
                               "codigo_a": a_cod, "codigo_b": b_cod,
                               "estimando": nombre, "diferencia": _f(punto),
                               "ic95_lo": float(np.percentile(fin, 2.5)) if fin.size else None,
                               "ic95_hi": float(np.percentile(fin, 97.5)) if fin.size else None,
                               "replicas_validas": int(fin.size),
                               "replicas_degeneradas": int(replicas-fin.size)})
    total = tabla[0]
    ref = par["controles_nacionales"]
    controles = {k: {"observado": total[k], "referencia": float(v),
                     "delta": (total[k] - float(v)) if total[k] is not None else None,
                     "estado": "REPLICA-RESULTADO" if total[k] is not None and abs(total[k]-float(v)) <= float(par["tolerancia_controles"]) else "NO-REPLICA"}
                 for k, v in ref.items()}
    indep_media, indep_ee = _independiente_media(a, fila_cluster, bloques)
    reconstruccion = {}
    for eje in ("tam_loc", "est_socio"):
        rs = [x for x in tabla if x["eje"] == eje]
        reconstruccion[eje] = {
            "elegibles_n_suma": sum(x["elegibles_n"] for x in rs),
            "elegibles_masa_suma": sum(x["elegibles_masa"] for x in rs),
            "remesas_validas_masa_suma": sum(x["remesas_validas_masa"] for x in rs),
            "receptores_masa_suma": sum(x["receptores_masa"] for x in rs),
            "prevalencia_reconstruida": (sum(x["receptores_masa"] for x in rs) /
                                           sum(x["remesas_validas_masa"] for x in rs)) if sum(x["remesas_validas_masa"] for x in rs) else None,
        }
    out.update({
        P + "ESTADO": "REPORTADO" if all(x["estado"] != "REPORTADO-CON-INCOMPATIBILIDAD" for x in tabla) else "REPORTADO-CON-INCOMPATIBILIDAD",
        P + "TABLA-JSON": _j(tabla), P + "CONTRASTES-JSON": _j(contrastes),
        P + "DISENO-JSON": _j({"metodo": metodo, "replicas": replicas,
            "estratos": len(bloques) if bloques else 0, "upm": len(clusters) if clusters else 0,
            "estratos_upm_unica": sum(len(x)==1 for x in bloques) if bloques else 0,
            "filas_sin_diseno": 0 if fila_cluster is not None else n}),
        P + "CONTROLES-JSON": _j(controles),
        P + "INDEPENDIENTE-JSON": _j({"remesas_media_fsum": indep_media,
            "delta_vs_principal": indep_media-total["remesas_media"],
            "ee_linealizado_upm_en_estrato": indep_ee}),
        P + "RECONSTRUCCION-JSON": _j(reconstruccion),
    })
    return out

