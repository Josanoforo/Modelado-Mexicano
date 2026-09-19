"""Perfil estructural de personas ENIGH 2022, conforme a spec v1.0."""
from __future__ import annotations

import csv
import hashlib
import io
import itertools
import json
import math
import zipfile

import numpy as np


ZIP_ID = "enigh2022_nc_csv"
P = "RESULT-ENIGH22-PERFIL-"
MIEMBROS = {
    "poblacion": "conjunto_de_datos_poblacion_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh2022_ns.csv",
    "concentrado": "conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh2022_ns.csv",
    "hogares": "conjunto_de_datos_hogares_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_hogares_enigh2022_ns.csv",
}
COLUMNAS = {
    "poblacion": ["folioviv", "foliohog", "numren", "parentesco", "edad", "segsoc", "factor", "est_dis", "upm"],
    "concentrado": ["folioviv", "foliohog", "tam_loc", "est_socio"],
    "hogares": ["folioviv", "foliohog", "celular", "conex_inte"],
}
CATEGORIAS = {
    "segsoc": [("1", "Sí"), ("2", "No")],
    "tramo_edad": [("18-29", "18–29"), ("30-44", "30–44"), ("45-59", "45–59"), ("60-96", "60–96")],
    "tam_loc": [("1", "100 000 y más"), ("2", "15 000 a 99 999"), ("3", "2 500 a 14 999"), ("4", "Menos de 2 500")],
    "est_socio": [("1", "Bajo"), ("2", "Medio bajo"), ("3", "Medio alto"), ("4", "Alto")],
    "conex_inte": [("1", "Sí"), ("2", "No")],
    "celular": [("1", "Sí"), ("2", "No")],
}
FUENTES = {
    "segsoc": "ENIGH 2022 Descripción de la base, p. 75",
    "tramo_edad": "ENIGH 2022 Descripción de la base, p. 65; corte operativo 18–96",
    "tam_loc": "ENIGH 2022 Descripción de la base, pp. 45 y 186",
    "est_socio": "ENIGH 2022 Descripción de la base, pp. 46 y 186",
    "conex_inte": "ENIGH 2022 Descripción de la base, p. 54",
    "celular": "ENIGH 2022 Descripción de la base, p. 54",
}
EJES = ("segsoc", "tramo_edad", "tam_loc", "est_socio")


def _texto(v):
    return str(v or "").lstrip("\ufeff").lstrip("ï»¿").strip().strip('"')


def _clave_hogar(r):
    return (_texto(r["folioviv"]).zfill(10), _texto(r["foliohog"]))


def _clave_persona(r):
    return _clave_hogar(r) + (_texto(r["numren"]),)


def _entero(v):
    t = _texto(v)
    if not t or not t.isdigit():
        return None
    return int(t)


def _peso(v):
    try:
        x = float(_texto(v))
    except ValueError:
        return None
    return x if math.isfinite(x) and x > 0 else None


def _tramo(edad):
    if 18 <= edad <= 29:
        return "18-29"
    if edad <= 44:
        return "30-44"
    if edad <= 59:
        return "45-59"
    return "60-96"


def _leer(zf, nombre):
    with zf.open(MIEMBROS[nombre]) as bruto:
        texto = io.TextIOWrapper(bruto, encoding="latin-1", newline="")
        lector = csv.DictReader(texto)
        if lector.fieldnames is None:
            raise ValueError(f"{nombre}: cabecera ausente")
        mapa = {_texto(c).lower(): c for c in lector.fieldnames}
        faltan = [c for c in COLUMNAS[nombre] if c not in mapa]
        if faltan:
            raise ValueError(f"{nombre}: columnas ausentes {faltan}")
        return [{c: r.get(mapa[c], "") for c in COLUMNAS[nombre]} for r in lector]


def _indice_unico(filas, nombre):
    indice = {}
    for r in filas:
        k = _clave_hogar(r)
        if k in indice:
            raise ValueError(f"{nombre}: llave hogar duplicada {k}")
        indice[k] = r
    return indice


def _masa(filas):
    return float(sum(r["_w"] for r in filas if r.get("_w") is not None))


def _r(x):
    return None if x is None or not math.isfinite(float(x)) else round(float(x), 12)


def _canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def _bootstrap(contrib, estratos, upms, grupos, n_estimandos, replicas, seed):
    """Un plan de remuestreo compartido para todos los cocientes."""
    salida = {"precision": "BOOTSTRAP-UPM-EN-ESTRATO", "replicas": replicas}
    if any(not e or not u for e, u in zip(estratos, upms)):
        salida["precision"] = "PRECISION-NO-DISPONIBLE-DISENO-INCOMPLETO"
        salida["ratios"] = None
        return salida
    pares = sorted(set(zip(estratos, upms)))
    pos = {p: i for i, p in enumerate(pares)}
    matriz = np.zeros((len(pares), contrib.shape[1]), dtype=float)
    for i, p in enumerate(zip(estratos, upms)):
        matriz[pos[p]] += contrib[i]
    por_estrato = {}
    for i, (e, _u) in enumerate(pares):
        por_estrato.setdefault(e, []).append(i)
    rng = np.random.Generator(np.random.PCG64(seed))
    totales = np.zeros((replicas, contrib.shape[1]), dtype=float)
    for e in sorted(por_estrato):
        idx = por_estrato[e]
        m = len(idx)
        if m == 1:
            totales += matriz[idx[0]]
        else:
            mult = rng.multinomial(m, np.full(m, 1.0 / m), size=replicas)
            totales += mult @ matriz[idx]
    nums = totales[:, :n_estimandos]
    dens = totales[:, n_estimandos:]
    ratios = np.full_like(nums, np.nan)
    for j, g in enumerate(grupos):
        ok = dens[:, g] > 0
        ratios[ok, j] = nums[ok, j] / dens[ok, g]
    salida.update({
        "ratios": ratios,
        "n_estratos": len(por_estrato),
        "n_upm": len(pares),
        "n_estratos_upm_unica": sum(len(x) == 1 for x in por_estrato.values()),
    })
    return salida


def calcular(poblacion, concentrado, hogares, replicas=1000, seed=20260919):
    pkeys = set()
    for r in poblacion:
        k = _clave_persona(r)
        if k in pkeys:
            raise ValueError(f"poblacion: llave persona duplicada {k}")
        pkeys.add(k)
    conc = _indice_unico(concentrado, "concentradohogar")
    hog = _indice_unico(hogares, "hogares")

    embudo = {k: {"n": 0, "masa": 0.0} for k in (
        "marco_poblacion", "integrantes_hogar", "excl_domesticos", "excl_huespedes",
        "excl_parentesco_otro", "excl_edad_invalida", "excl_menor_18",
        "excl_mayor_96", "excl_peso_invalido", "universo_principal")}
    principales = []
    for raw in poblacion:
        r = dict(raw)
        r["_w"] = _peso(r["factor"])
        embudo["marco_poblacion"]["n"] += 1
        if r["_w"] is not None:
            embudo["marco_poblacion"]["masa"] += r["_w"]
        par = _texto(r["parentesco"])
        pref = par[:1]
        if pref not in {"1", "2", "3", "5", "6"}:
            motivo = "excl_domesticos" if pref == "4" else "excl_huespedes" if pref == "7" else "excl_parentesco_otro"
            embudo[motivo]["n"] += 1
            if r["_w"] is not None:
                embudo[motivo]["masa"] += r["_w"]
            continue
        embudo["integrantes_hogar"]["n"] += 1
        if r["_w"] is not None:
            embudo["integrantes_hogar"]["masa"] += r["_w"]
        edad = _entero(r["edad"])
        if edad is None:
            motivo = "excl_edad_invalida"
        elif edad < 18:
            motivo = "excl_menor_18"
        elif edad > 96:
            motivo = "excl_mayor_96"
        elif r["_w"] is None:
            motivo = "excl_peso_invalido"
        else:
            motivo = None
        if motivo:
            embudo[motivo]["n"] += 1
            if r["_w"] is not None:
                embudo[motivo]["masa"] += r["_w"]
            continue
        hkey = _clave_hogar(r)
        cr, hr = conc.get(hkey), hog.get(hkey)
        r.update({
            "tramo_edad": _tramo(edad),
            "segsoc": _texto(r["segsoc"]),
            "tam_loc": _texto(cr["tam_loc"]) if cr else "",
            "est_socio": _texto(cr["est_socio"]) if cr else "",
            "celular": _texto(hr["celular"]) if hr else "",
            "conex_inte": _texto(hr["conex_inte"]) if hr else "",
            "_hkey": hkey,
        })
        principales.append(r)
        embudo["universo_principal"]["n"] += 1
        embudo["universo_principal"]["masa"] += r["_w"]

    universo_n = len(principales)
    universo_masa = _masa(principales)
    validos = {v: {c for c, _ in cats} for v, cats in CATEGORIAS.items()}
    cobertura = {}
    for v in CATEGORIAS:
        ok = [r for r in principales if r[v] in validos[v]]
        cobertura[v] = {
            "valid_n": len(ok), "valid_masa": _masa(ok),
            "missing_n": universo_n - len(ok), "missing_masa": universo_masa - _masa(ok),
        }
    completos = [r for r in principales if all(r[v] in validos[v] for v in EJES)]
    completo_n, completo_masa = len(completos), _masa(completos)

    definiciones = []
    grupos_nombres = list(CATEGORIAS) + ["conjunta"]
    grupo_idx = {g: i for i, g in enumerate(grupos_nombres)}
    for v, cats in CATEGORIAS.items():
        for c, etiqueta in cats:
            definiciones.append({"pieza": "P1", "variable": v, "codigo": c, "etiqueta": etiqueta, "grupo": grupo_idx[v]})
    for combo in itertools.product(*(CATEGORIAS[v] for v in EJES)):
        definiciones.append({
            "pieza": "P2", "grupo": grupo_idx["conjunta"],
            **{v: combo[i][0] for i, v in enumerate(EJES)},
            "etiqueta": " × ".join(x[1] for x in combo),
        })
    for v in EJES:
        for c, etiqueta in CATEGORIAS[v]:
            definiciones.append({"pieza": "P2-MARGINAL", "variable": v, "codigo": c, "etiqueta": etiqueta, "grupo": grupo_idx["conjunta"]})
    k = len(definiciones)
    indice_p1 = {(d["variable"], d["codigo"]): i for i, d in enumerate(definiciones) if d["pieza"] == "P1"}
    indice_joint = {tuple(d[v] for v in EJES): i for i, d in enumerate(definiciones) if d["pieza"] == "P2"}
    indice_jm = {(d["variable"], d["codigo"]): i for i, d in enumerate(definiciones) if d["pieza"] == "P2-MARGINAL"}
    contrib = np.zeros((universo_n, k + len(grupos_nombres)), dtype=float)
    ns = np.zeros(k, dtype=int)
    masas = np.zeros(k, dtype=float)
    soportes = [set() for _ in range(k)]
    estratos, upms = [], []
    for fila_i, r in enumerate(principales):
        w = r["_w"]
        estrato, upm = _texto(r["est_dis"]), _texto(r["upm"])
        estratos.append(estrato); upms.append(upm)
        psu = (estrato, upm)
        for v in CATEGORIAS:
            if r[v] in validos[v]:
                contrib[fila_i, k + grupo_idx[v]] = w
                j = indice_p1[(v, r[v])]
                contrib[fila_i, j] = w; ns[j] += 1; masas[j] += w; soportes[j].add(psu)
        if all(r[v] in validos[v] for v in EJES):
            contrib[fila_i, k + grupo_idx["conjunta"]] = w
            combo = tuple(r[v] for v in EJES)
            j = indice_joint[combo]
            contrib[fila_i, j] = w; ns[j] += 1; masas[j] += w; soportes[j].add(psu)
            for v in EJES:
                j = indice_jm[(v, r[v])]
                contrib[fila_i, j] = w; ns[j] += 1; masas[j] += w; soportes[j].add(psu)

    boot = _bootstrap(contrib, estratos, upms, [d["grupo"] for d in definiciones], k, replicas, seed)
    ratios = boot["ratios"]
    denominadores = {**{v: cobertura[v]["valid_masa"] for v in CATEGORIAS}, "conjunta": completo_masa}
    filas_salida = []
    for j, d in enumerate(definiciones):
        den_nombre = grupos_nombres[d["grupo"]]
        den = denominadores[den_nombre]
        p = masas[j] / den if den > 0 else None
        if ns[j] == 0:
            ee = lo = hi = None; nrep = 0; estado = "CERO-MUESTRAL"
        elif ratios is None:
            ee = lo = hi = None; nrep = 0; estado = "OBSERVADA-PRECISION-NO-DISPONIBLE"
        else:
            rr = ratios[:, j]; rr = rr[np.isfinite(rr)]
            nrep = int(rr.size)
            ee = float(np.std(rr, ddof=1)) if rr.size > 1 else None
            lo, hi = (float(np.percentile(rr, 2.5)), float(np.percentile(rr, 97.5))) if rr.size else (None, None)
            estado = "OBSERVADA"
        base = {
            "n": int(ns[j]), "numerador_ponderado": _r(masas[j]), "denominador_ponderado": _r(den),
            "proporcion": _r(p), "ee": _r(ee), "ic95_lo": _r(lo), "ic95_hi": _r(hi),
            "replicas_validas": nrep, "upm_n": len(soportes[j]), "estado": estado,
            "unidad": "persona", "universo": "integrantes del hogar de 18 a 96 años con factor persona válido",
        }
        if d["pieza"] == "P1":
            cov = cobertura[d["variable"]]
            base.update({
                "variable": d["variable"], "codigo": d["codigo"], "etiqueta": d["etiqueta"],
                "universo_n": universo_n, "universo_masa": _r(universo_masa),
                **{x: _r(y) if "masa" in x else y for x, y in cov.items()}, "fuente": FUENTES[d["variable"]],
            })
        elif d["pieza"] == "P2":
            base.update({v: d[v] for v in EJES}); base["etiqueta"] = d["etiqueta"]
        else:
            base.update({"variable": d["variable"], "codigo": d["codigo"], "etiqueta": d["etiqueta"]})
        filas_salida.append((d["pieza"], base))

    marg = [x for pz, x in filas_salida if pz == "P1"]
    joint = [x for pz, x in filas_salida if pz == "P2"]
    jmarg = [x for pz, x in filas_salida if pz == "P2-MARGINAL"]

    # Implementación separada de puntos: sumas directas, sin usar la matriz.
    deltas = []
    for row in marg:
        vv = [r for r in principales if r[row["variable"]] == row["codigo"]]
        deltas.append(abs(_masa(vv) - row["numerador_ponderado"]))
    for row in joint:
        vv = [r for r in completos if all(r[v] == row[v] for v in EJES)]
        deltas.append(abs(_masa(vv) - row["numerador_ponderado"]))
    max_delta_control = max(deltas, default=0.0)

    # La suma de celdas debe coincidir con marginales directas de casos completos.
    deltas_marg = []
    for row in jmarg:
        celdas = [x for x in joint if x[row["variable"]] == row["codigo"]]
        deltas_marg.extend([
            abs(sum(x["n"] for x in celdas) - row["n"]),
            abs(sum(x["numerador_ponderado"] for x in celdas) - row["numerador_ponderado"]),
        ])
        if row["proporcion"] is not None and all(x["proporcion"] is not None for x in celdas):
            deltas_marg.append(abs(sum(x["proporcion"] for x in celdas) - row["proporcion"]))
    max_delta_marg = max(deltas_marg, default=0.0)
    for x in embudo.values():
        x["masa"] = _r(x["masa"])
    return {
        "embudo": embudo, "marginales": marg, "conjunta": joint, "marginales_completos": jmarg,
        "universo_n": universo_n, "universo_masa": universo_masa,
        "completo_n": completo_n, "completo_masa": completo_masa,
        "sin_match_concentrado_n": sum(_clave_hogar(r) not in conc for r in principales),
        "sin_match_hogares_n": sum(_clave_hogar(r) not in hog for r in principales),
        "diseno_faltante_n": sum(not _texto(r["est_dis"]) or not _texto(r["upm"]) for r in principales),
        "bootstrap": boot, "max_delta_control": max_delta_control, "max_delta_marg": max_delta_marg,
    }


def medir(inputs, contrato):
    with zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"]) as zf:
        datos = {nombre: _leer(zf, nombre) for nombre in MIEMBROS}
    par = contrato["parametros"]
    r = calcular(datos["poblacion"], datos["concentrado"], datos["hogares"], int(par["bootstrap_replicas"]), int(contrato["seed"]["valor"]))
    marg = _canon(r["marginales"]); joint = _canon(r["conjunta"]); jmarg = _canon(r["marginales_completos"]); emb = _canon(r["embudo"])
    b = r["bootstrap"]
    return {
        P + "P1-ESTADO": "ESTIMADO",
        P + "P2-ESTADO": "ESTIMADO",
        P + "P3-ESTADO": "NO-ESTIMABLE-POR-DEFINICION-NO-ACREDITADA",
        P + "P3-EVIDENCIA": "ENIGH2022-DESCRIPCION-BASE-PP75:5-ANOS-VS-OCTUBRE-2005;UNIVERSO-Y-SALTOS-NO-ACREDITADOS",
        P + "EMBUDO-JSON": emb,
        P + "EMBUDO-SHA256": _sha(emb),
        P + "UNIVERSO-N": r["universo_n"],
        P + "UNIVERSO-MASA": _r(r["universo_masa"]),
        P + "JOIN-SIN-MATCH-CONCENTRADO-N": r["sin_match_concentrado_n"],
        P + "JOIN-SIN-MATCH-HOGARES-N": r["sin_match_hogares_n"],
        P + "DISENO-FALTANTE-N": r["diseno_faltante_n"],
        P + "DISENO-N-ESTRATOS": int(b.get("n_estratos", 0)),
        P + "DISENO-N-UPM": int(b.get("n_upm", 0)),
        P + "DISENO-N-ESTRATOS-UPM-UNICA": int(b.get("n_estratos_upm_unica", 0)),
        P + "METODO-IC": b["precision"],
        P + "BOOTSTRAP-REPLICAS": int(b["replicas"]),
        P + "P1-MARGINALES-JSON": marg,
        P + "P1-MARGINALES-SHA256": _sha(marg),
        P + "P1-N-FILAS": len(r["marginales"]),
        P + "P2-CONJUNTA-JSON": joint,
        P + "P2-CONJUNTA-SHA256": _sha(joint),
        P + "P2-N-CELDAS": len(r["conjunta"]),
        P + "P2-COMPLETOS-N": r["completo_n"],
        P + "P2-COMPLETOS-MASA": _r(r["completo_masa"]),
        P + "P2-PERDIDA-N": r["universo_n"] - r["completo_n"],
        P + "P2-PERDIDA-MASA": _r(r["universo_masa"] - r["completo_masa"]),
        P + "P2-MARGINALES-COMPLETOS-JSON": jmarg,
        P + "P2-MARGINALES-COMPLETOS-SHA256": _sha(jmarg),
        P + "P2-N-MARGINALES-COMPLETOS": len(r["marginales_completos"]),
        P + "CONTROL-MAX-DELTA-PUNTOS": _r(r["max_delta_control"]),
        P + "CONTROL-MAX-DELTA-MARGINALIZACION": _r(r["max_delta_marg"]),
        P + "USO": "DESCRIPTIVO-NO-ADOPTA-PI-NO-RELEVA-RES-0165-A-0170",
    }
