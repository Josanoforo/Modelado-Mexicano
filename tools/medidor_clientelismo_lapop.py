#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3 — piezas (a) y (a') sobre LAPOP Mexico.

(a)  R7.7 `civico.clientelismo.turnout_no_vote_choice` — LAPOP 2019.
     La oferta de dadiva (`clien1na`) mueve la ASISTENCIA (`vb2`) y no la
     ELECCION (`vb3n`). Dos piernas, una corrida.
(a') R7.3 `civico.voto.agencia_con_secreto` / R7.6 `civico.voto.clientelar_si_observable`
     — LAPOP 2023. La transferencia (`mexwf1_19`) mueve la intencion de voto
     por el oficialismo (`vb20`) solo donde el voto NO se percibe secreto
     (`countfair3`).

Las dos olas viven en la raiz `descargas_mx` de `data/manifiesto.yaml`, no en
`data/raw` — un worktree nuevo la resuelve con `data/raices.local.yaml`
(gitignorada). Este modulo tambien exporta el cargador y el bootstrap de
conglomerado que usa `medidor_protesta_lapop.py`.

Uso:
    python3 tools/medidor_clientelismo_lapop.py --censo
    python3 tools/medidor_clientelismo_lapop.py --mide --json data/l9-clientelismo-v1_0.json
"""
import argparse, hashlib, json, os, random, sys

RAICES_LOCAL = "data/raices.local.yaml"
SEED = 42
REPLICAS = 10000

# Los payloads que este acto abre, por id de data/manifiesto.yaml.
PAYLOADS = {
    "2019": ("mexico_lapop_americasbarometer_2019_v1_0_w",
             "Descargas Manuales/Mexico LAPOP AmericasBarometer 2019 v1.0_W.dta"),
    "2021": ("mex_2021_lapop_americasbarometer_v1_2_w",
             "Descargas Manuales/MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta"),
    "2023": ("mex_2023_lapop_americasbarometer_v1_0_w",
             "Descargas Manuales/MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta"),
    "2006": ("518939279mexico_lapop_final_2006_data_set_092906",
             "Descargas Manuales/518939279mexico_lapop_final 2006 data set 092906.dta"),
}


def raiz(nombre="descargas_mx"):
    """Resuelve una raiz de data/manifiesto.yaml. PARA si no esta configurada:
    un worktree nuevo nace sin data/raices.local.yaml y un `no existe` que en
    realidad es `no configurada` es el falso negativo que A.13 persigue."""
    if not os.path.exists(RAICES_LOCAL):
        raise SystemExit(
            f"PARO: falta {RAICES_LOCAL}. La raiz '{nombre}' no esta configurada en "
            f"este worktree — esto NO es 'el payload no existe'. Escribe el archivo "
            f"con la linea `{nombre}: <ruta>` (valor de la casa en "
            f"forense/notas/2026-08-06-map1b-censo-raices.md:68).")
    for linea in open(RAICES_LOCAL, encoding="utf-8"):
        linea = linea.split("#")[0].strip()
        if linea.startswith(nombre + ":"):
            return linea.split(":", 1)[1].strip()
    raise SystemExit(f"PARO: {RAICES_LOCAL} no define '{nombre}'.")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def carga(ola):
    """Devuelve (DataFrame, meta, ruta, sha256). Verifica el payload por
    identidad (sha256 contra el manifiesto), no por nombre de archivo."""
    import pyreadstat
    pid, rel = PAYLOADS[ola]
    path = os.path.join(raiz(), rel)
    if not os.path.exists(path):
        raise SystemExit(f"PARO: payload ausente en disco: {path} (id {pid})")
    df, meta = pyreadstat.read_dta(path)
    return df, meta, path, sha256(path)


def sha_manifiesto(pid):
    """El sha256 que data/manifiesto.yaml declara para ese id, o None."""
    import re
    txt = open("data/manifiesto.yaml", encoding="utf-8").read()
    for ent in re.split(r"\n(?=- id: )", txt):
        m = re.match(r"- id: (\S+)", ent)
        if m and m.group(1) == pid:
            s = re.search(r"\n  sha256: (\S+)", ent)
            return s.group(1) if s else None
    return None


# ───────────────────────────── estimador ─────────────────────────────

def _cod(v):
    """LAPOP codifica los faltantes como 'a'/'b'/'c' (NS/NR/Inaplicable) y
    pyreadstat los entrega como NaN o como str. Devuelve int o None."""
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        return int(s) if s.isdigit() else None
    try:
        if v != v:      # NaN
            return None
        return int(v)
    except (TypeError, ValueError):
        return None


def prop_bootstrap(filas, replicas=REPLICAS, seed=SEED):
    """filas: lista de (estrato, upm, peso, y) con y en {0,1}.

    Proporcion ponderada + IC95 por bootstrap de conglomerado: se remuestrean
    con reemplazo las UPM DENTRO de cada estrato (el diseno de LAPOP y de las
    ENIF/ENCUCI de INEGI), nunca las personas — remuestrear personas ignora el
    efecto de diseno y estrecha el IC de mentira.
    """
    filas = list(filas)
    if not filas:
        return None
    # Totales por UPM, precomputados: cada replica suma 2 numeros por UPM en vez
    # de recorrer sus filas. Mismo resultado exacto, y sin esto una fuente con
    # 3 096 conglomerados (ENCUCI) no termina en 10 000 replicas.
    tot = {}
    for est, upm, w, y in filas:
        k = (est, upm)
        a = tot.get(k)
        if a is None:
            tot[k] = [w, w * y]
        else:
            a[0] += w
            a[1] += w * y
    estratos = {}
    for (est, upm) in tot:
        estratos.setdefault(est, []).append((est, upm))
    por_upm = tot

    def punto(claves):
        num = den = 0.0
        for k in claves:
            a = tot[k]
            den += a[0]
            num += a[1]
        return num / den if den else None

    p_hat = punto(list(por_upm))
    rng = random.Random(seed)
    reps = []
    for _ in range(replicas):
        claves = []
        for est, lst in estratos.items():
            n = len(lst)
            if n < 2:                      # estrato singleton: entra tal cual
                claves.extend(lst)
                continue
            claves.extend(lst[rng.randrange(n)] for _ in range(n))
        p = punto(claves)
        if p is not None:
            reps.append(p)
    reps.sort()
    lo = reps[int(0.025 * len(reps))]
    hi = reps[min(len(reps) - 1, int(0.975 * len(reps)))]
    n_upm = len(por_upm)
    return {
        "p": p_hat,
        "ic95": [lo, hi],
        "n": len(filas),
        "numerador": sum(1 for _e, _u, _w, y in filas if y == 1),
        "n_estratos": len(estratos),
        "n_upm": n_upm,
        "estratos_singleton": sum(1 for l in estratos.values() if len(l) < 2),
        "replicas": len(reps),
        "poblacion_expandida": sum(w for _e, _u, w, _y in filas),
    }


def diff_bootstrap(filas_a, filas_b, replicas=REPLICAS, seed=SEED):
    """Diferencia de proporciones p(A) - p(B) con el MISMO remuestreo de UPM
    para las dos ramas: A y B comparten estrato/UPM, y tratarlas como
    independientes sobreestima la varianza de la diferencia (mismo argumento
    que tests/svystat.py::diff_ultimate_cluster hace para la version analitica).
    """
    marc = [(e, u, w, y, "A") for e, u, w, y in filas_a] + \
           [(e, u, w, y, "B") for e, u, w, y in filas_b]
    if not marc:
        return None
    # Mismo precomputo que prop_bootstrap, con cuatro acumuladores por UPM
    # (peso y peso*y, para la rama A y para la B).
    tot = {}
    for est, upm, w, y, g in marc:
        k = (est, upm)
        a = tot.get(k)
        if a is None:
            a = tot[k] = [0.0, 0.0, 0.0, 0.0]
        if g == "A":
            a[0] += w; a[1] += w * y
        else:
            a[2] += w; a[3] += w * y
    estratos = {}
    for (est, upm) in tot:
        estratos.setdefault(est, []).append((est, upm))
    por_upm = tot

    def punto(claves):
        n_a = d_a = n_b = d_b = 0.0
        for k in claves:
            a = tot[k]
            d_a += a[0]; n_a += a[1]; d_b += a[2]; n_b += a[3]
        if not d_a or not d_b:
            return None
        return n_a / d_a - n_b / d_b

    d_hat = punto(list(por_upm))
    rng = random.Random(seed)
    reps = []
    for _ in range(replicas):
        claves = []
        for est, lst in estratos.items():
            n = len(lst)
            if n < 2:
                claves.extend(lst)
                continue
            claves.extend(lst[rng.randrange(n)] for _ in range(n))
        d = punto(claves)
        if d is not None:
            reps.append(d)
    reps.sort()
    return {
        "d": d_hat,
        "ic95": [reps[int(0.025 * len(reps))],
                 reps[min(len(reps) - 1, int(0.975 * len(reps)))]],
        "replicas_validas": len(reps),
        "replicas_pedidas": replicas,
    }


# ───────────────────────────── P0 · censo A.4 ─────────────────────────────

# Lo que el censo busca, por regla. Un `None` en `hallado` lo llena la corrida.
CENSO_ITEMS = {
    "2019": ["clien1na", "clien1n", "clien4a", "clien4b", "vb2", "vb3n", "vb10",
             "vb20", "prot3", "vic1ext", "ur", "estratosec", "cct1b",
             "mexwf1_19", "wt", "upm", "estratopri", "cluster", "q1", "q2",
             "ed", "q10new"],
    "2021": ["clien1na", "clien1n", "vb2", "vb3n", "prot3", "countfair3",
             "mexwf1_19", "wt", "upm", "estratopri"],
    "2023": ["clien1na", "clien1n", "countfair1", "countfair3", "vb2", "vb3n",
             "vb20", "mexwf1_19", "ur", "estratosec", "wt", "upm",
             "estratopri", "strata"],
    "2006": ["PROT1", "PROT2", "VIC1", "UR", "TAMANO", "ESTRATOPRI", "UPM"],
}


def censo(olas=("2019", "2021", "2023", "2006")):
    """Censo A.4: item, codigos, denominador, ponderador, diseno, unidad.
    Reporta MARGINALES; no cruza ninguna variable contra el desenlace."""
    salida = []
    for ola in olas:
        pid, _rel = PAYLOADS[ola]
        df, meta, path, sha = carga(ola)
        sha_man = sha_manifiesto(pid)
        print(f"\n{'=' * 78}\nLAPOP MEXICO {ola} · id {pid}")
        print(f"  archivo   : {path}")
        print(f"  sha256    : {sha}")
        print(f"  manifiesto: {sha_man}  -> {'COINCIDE' if sha == sha_man else 'DIFIERE'}")
        print(f"  filas={len(df)}  columnas={len(df.columns)}")
        for var in CENSO_ITEMS[ola]:
            if var not in df.columns:
                print(f"    {var:12s} NO-ENCONTRADO en esta ola")
                salida.append({"ola": ola, "var": var, "estado": "NO-ENCONTRADO"})
                continue
            s = df[var]
            cods = [_cod(v) for v in s]
            validos = sum(1 for c in cods if c is not None)
            marg = {}
            for c in cods:
                if c is not None:
                    marg[c] = marg.get(c, 0) + 1
            etq = meta.column_names_to_labels.get(var, "")
            vlab = meta.variable_value_labels.get(var, {}) or {}
            print(f"    {var:12s} n_val={validos:5d} ({validos / len(df):5.1%})  "
                  f"distintos={len(marg):3d}  {str(etq)[:58]}")
            salida.append({"ola": ola, "var": var, "estado": "EXISTE",
                           "etiqueta": str(etq), "n_validos": validos,
                           "n_filas": len(df), "marginal": marg,
                           "codigos": {str(k): str(v) for k, v in vlab.items()}})
    return salida


# ─────────────────────── P1 · medicion (COMMIT-2) ───────────────────────
# Todo lo de aqui abajo ejecuta la spec congelada en
# forense/notas/2026-09-02-MAESTRA35-L9-spec.md §2 y §3. Nada se decide aqui.

MIN_NUMERADOR = 10          # spec §1.3, guardia de celda
COBERTURA_MIN = 0.90        # spec §1.3, universo restringido A-bis 4

# spec §0.5 — guardias de lectura con valor esperado, congeladas antes de correr
GUARDIAS = {
    "2019": {"filas": 1580, "clien1na_val": 1578, "clien1na_si": 271,
             "prot3_val": 1576, "prot3_si": 112},
    "2023": {"filas": 1622, "mexwf1_19_val": 1615, "mexwf1_19_si": 363,
             "countfair3_val": 1542},
}


def _guardia(nombre, obtenido, esperado):
    if obtenido != esperado:
        raise SystemExit(f"PARO (guardia de lectura §0.5): {nombre} = {obtenido}, "
                         f"esperado {esperado}. El lector no leyo lo que la spec congelo.")
    return True


def _control_regresion(filas, p_boot, etiqueta):
    """spec §1.1: el punto del bootstrap y el de la linealizacion tienen que
    coincidir byte a byte; solo el IC puede diferir."""
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tests"))
    import svystat
    r = svystat.prop_ultimate_cluster(filas)
    if r is None:
        return None
    if abs(r["p_hat"] - p_boot) > 1e-12:
        raise SystemExit(f"PARO (control de regresion §1.1): {etiqueta} "
                         f"bootstrap p={p_boot!r} vs linealizacion p={r['p_hat']!r}")
    return {"p_hat_linealizado": r["p_hat"], "ic95_linealizado": list(r["ic95"]),
            "n_upm": r["n_upm_total"], "estratos_singleton": r["n_estratos_singleton"]}


def _celda(filas, etiqueta):
    """Proporcion de una celda, con la guardia de numerador de §1.3."""
    r = prop_bootstrap(filas)
    if r is None:
        return {"etiqueta": etiqueta, "estado": "NO-ESTIMABLE", "motivo": "celda vacia", "n": 0}
    if r["numerador"] < MIN_NUMERADOR:
        return {"etiqueta": etiqueta, "estado": "NO-ESTIMABLE",
                "motivo": f"numerador {r['numerador']} < {MIN_NUMERADOR} (guardia §1.3)",
                "n": r["n"], "numerador": r["numerador"]}
    r["etiqueta"] = etiqueta
    r["estado"] = "ESTIMADA"
    r["control_regresion"] = _control_regresion(filas, r["p"], etiqueta)
    return r


def _dif(fa, fb, etiqueta, ca, cb):
    """Diferencia p(A)-p(B). NO-ESTIMABLE si cualquiera de las dos celdas lo es."""
    if ca.get("estado") != "ESTIMADA" or cb.get("estado") != "ESTIMADA":
        return {"etiqueta": etiqueta, "estado": "NO-ESTIMABLE",
                "motivo": f"celda no estimable: {ca.get('motivo') or cb.get('motivo')}"}
    d = diff_bootstrap(fa, fb)
    d["etiqueta"] = etiqueta
    d["estado"] = "ESTIMADA"
    d["excluye_cero"] = (d["ic95"][0] > 0) or (d["ic95"][1] < 0)
    d["signo"] = "+" if d["d"] > 0 else "-"
    return d


def _filas(df, cols, y_fn, filtro=None, est="estratopri", upm="upm", peso="wt"):
    """Arma (estrato, upm, peso, y) aplicando la codificacion de LAPOP."""
    out = []
    for i in range(len(df)):
        v = {c: _cod(df[c].iloc[i]) for c in cols}
        if any(v[c] is None for c in cols):
            continue
        if filtro and not filtro(v):
            continue
        y = y_fn(v)
        if y is None:
            continue
        out.append((int(df[est].iloc[i]), int(df[upm].iloc[i]),
                    float(df[peso].iloc[i]), y))
    return out


def _pieza_a(df):
    """spec §2 — R7.7: la dadiva compra asistencia, no eleccion."""
    res = {"pieza": "a", "reglas": ["R7.7"],
           "id_modelo": ["civico.clientelismo.turnout_no_vote_choice"],
           "fuente": "LAPOP Mexico 2019", "spec": "§2"}

    # --- pierna ASISTENCIA ---
    of = _filas(df, ["clien1na", "vb2"], lambda v: 1 if v["vb2"] == 1 else 0,
                lambda v: v["clien1na"] == 1)
    no = _filas(df, ["clien1na", "vb2"], lambda v: 1 if v["vb2"] == 1 else 0,
                lambda v: v["clien1na"] == 2)
    c_of = _celda(of, "asistencia | ofrecieron")
    c_no = _celda(no, "asistencia | no ofrecieron")
    res["asistencia"] = {"ofrecieron": c_of, "no_ofrecieron": c_no,
                         "delta": _dif(of, no, "Δ_asistencia", c_of, c_no)}

    # --- pierna ELECCION (condicionada a haber votado; colisionador declarado) ---
    res["eleccion"] = {}
    for nom, cod in (("PRI_principal", 103), ("MORENA_secundario", 101)):
        vo = _filas(df, ["clien1na", "vb2", "vb3n"],
                    lambda v, c=cod: 1 if v["vb3n"] == c else 0,
                    lambda v: v["clien1na"] == 1 and v["vb2"] == 1)
        vn = _filas(df, ["clien1na", "vb2", "vb3n"],
                    lambda v, c=cod: 1 if v["vb3n"] == c else 0,
                    lambda v: v["clien1na"] == 2 and v["vb2"] == 1)
        a = _celda(vo, f"{nom} | ofrecieron")
        b = _celda(vn, f"{nom} | no ofrecieron")
        res["eleccion"][nom] = {"ofrecieron": a, "no_ofrecieron": b,
                                "delta": _dif(vo, vn, f"Δ_eleccion_{nom}", a, b)}

    # --- ejes secundarios sobre la pierna de asistencia (spec §2) ---
    def tramo_ed(e):
        return "0-6" if e <= 6 else "7-9" if e <= 9 else "10-12" if e <= 12 else "13+"
    ejes = {}
    for nom, col, etq in (("ur", "ur", {1: "urbano", 2: "rural"}),
                          ("sexo", "q1", {1: "hombre", 2: "mujer"})):
        ejes[nom] = {}
        for k, lab in etq.items():
            fo = _filas(df, ["clien1na", "vb2", col],
                        lambda v: 1 if v["vb2"] == 1 else 0,
                        lambda v, k=k: v["clien1na"] == 1 and v[col] == k)
            fn = _filas(df, ["clien1na", "vb2", col],
                        lambda v: 1 if v["vb2"] == 1 else 0,
                        lambda v, k=k: v["clien1na"] == 2 and v[col] == k)
            ca, cb = _celda(fo, f"{lab}|of"), _celda(fn, f"{lab}|no")
            ejes[nom][lab] = {"ofrecieron": ca, "no_ofrecieron": cb,
                              "delta": _dif(fo, fn, f"Δ_{lab}", ca, cb)}
    ejes["escolaridad"] = {}
    for lab in ("0-6", "7-9", "10-12", "13+"):
        fo = _filas(df, ["clien1na", "vb2", "ed"],
                    lambda v: 1 if v["vb2"] == 1 else 0,
                    lambda v, l=lab: v["clien1na"] == 1 and tramo_ed(v["ed"]) == l)
        fn = _filas(df, ["clien1na", "vb2", "ed"],
                    lambda v: 1 if v["vb2"] == 1 else 0,
                    lambda v, l=lab: v["clien1na"] == 2 and tramo_ed(v["ed"]) == l)
        ca, cb = _celda(fo, f"{lab}|of"), _celda(fn, f"{lab}|no")
        ejes["escolaridad"][lab] = {"ofrecieron": ca, "no_ofrecieron": cb,
                                    "delta": _dif(fo, fn, f"Δ_{lab}", ca, cb)}
    res["ejes_secundarios"] = ejes
    return res


def _pieza_a_bis(df):
    """spec §3 — R7.3 / R7.6: la agencia se conserva con secreto y cede sin el."""
    res = {"pieza": "a-bis", "reglas": ["R7.3", "R7.6"],
           "id_modelo": ["civico.voto.agencia_con_secreto",
                         "civico.voto.clientelar_si_observable"],
           "fuente": "LAPOP Mexico 2023", "spec": "§3"}
    n_vb20 = sum(1 for v in df["vb20"] if _cod(v) is not None)
    res["cobertura_vb20"] = n_vb20 / len(df)
    res["universo_restringido"] = res["cobertura_vb20"] < COBERTURA_MIN

    ramas = {"SECRETO": (1,), "OBSERVABLE": (2, 3)}
    for rama, cods in ramas.items():
        fa = _filas(df, ["mexwf1_19", "countfair3", "vb20"],
                    lambda v: 1 if v["vb20"] == 2 else 0,
                    lambda v, c=cods: v["mexwf1_19"] == 1 and v["countfair3"] in c,
                    est="strata")
        fb = _filas(df, ["mexwf1_19", "countfair3", "vb20"],
                    lambda v: 1 if v["vb20"] == 2 else 0,
                    lambda v, c=cods: v["mexwf1_19"] == 2 and v["countfair3"] in c,
                    est="strata")
        ca = _celda(fa, f"oficialismo | ayuda=Si, {rama}")
        cb = _celda(fb, f"oficialismo | ayuda=No, {rama}")
        res[rama] = {"ayuda_si": ca, "ayuda_no": cb,
                     "delta": _dif(fa, fb, f"Δ_{rama}", ca, cb)}
    ds, do = res["SECRETO"]["delta"], res["OBSERVABLE"]["delta"]
    if ds.get("estado") == "ESTIMADA" and do.get("estado") == "ESTIMADA":
        res["delta_diferencia"] = {"valor": do["d"] - ds["d"],
                                   "nota": "diferencia de dos diferencias; su IC no se "
                                           "reporta porque la spec no lo pre-registro"}
    else:
        res["delta_diferencia"] = {"estado": "NO-ESTIMABLE"}
    return res


def mide(ruta_json=None):
    df19, _m19, p19, s19 = carga("2019")
    df23, _m23, p23, s23 = carga("2023")

    # spec §0.5 — guardias de lectura, antes de estimar nada
    g = GUARDIAS["2019"]
    _guardia("2019 filas", len(df19), g["filas"])
    _guardia("2019 clien1na validos",
             sum(1 for v in df19["clien1na"] if _cod(v) is not None), g["clien1na_val"])
    _guardia("2019 clien1na si",
             sum(1 for v in df19["clien1na"] if _cod(v) == 1), g["clien1na_si"])
    g = GUARDIAS["2023"]
    _guardia("2023 filas", len(df23), g["filas"])
    _guardia("2023 mexwf1_19 validos",
             sum(1 for v in df23["mexwf1_19"] if _cod(v) is not None), g["mexwf1_19_val"])
    _guardia("2023 mexwf1_19 si",
             sum(1 for v in df23["mexwf1_19"] if _cod(v) == 1), g["mexwf1_19_si"])
    _guardia("2023 countfair3 validos",
             sum(1 for v in df23["countfair3"] if _cod(v) is not None), g["countfair3_val"])
    print("guardias de lectura §0.5: OK")

    out = {"acto": "MAESTRA35-L9 · REGLAS-ACTIVOS-L3",
           "spec": "forense/notas/2026-09-02-MAESTRA35-L9-spec.md",
           "estimador": f"proporcion ponderada; IC95 bootstrap de conglomerado, "
                        f"{REPLICAS} replicas, seed {SEED}, remuestreo de UPM dentro de estrato",
           "aviso_ponderador": "wt de LAPOP Mexico es constante = 1 en 2019 y 2023: la "
                               "proporcion ponderada es identica a la simple y todo el "
                               "efecto de diseno vive en el conglomerado (spec §1.2)",
           "payloads": [{"id": PAYLOADS["2019"][0], "sha256": s19,
                         "coincide_manifiesto": s19 == sha_manifiesto(PAYLOADS["2019"][0])},
                        {"id": PAYLOADS["2023"][0], "sha256": s23,
                         "coincide_manifiesto": s23 == sha_manifiesto(PAYLOADS["2023"][0])}],
           "piezas": [_pieza_a(df19), _pieza_a_bis(df23)]}
    if ruta_json:
        json.dump(out, open(ruta_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("escrito", ruta_json)
    _imprime(out)
    return out


def _fmt(c):
    if c.get("estado") != "ESTIMADA":
        return f"NO-ESTIMABLE ({c.get('motivo')})"
    if "p" in c:
        return (f"p={c['p']:.6f}  IC95=[{c['ic95'][0]:.6f},{c['ic95'][1]:.6f}]  "
                f"n={c['n']} num={c['numerador']}")
    return (f"d={c['d']:+.6f}  IC95=[{c['ic95'][0]:+.6f},{c['ic95'][1]:+.6f}]  "
            f"{'EXCLUYE 0' if c['excluye_cero'] else 'contiene 0'}")


def _imprime(out):
    for pz in out["piezas"]:
        print(f"\n{'=' * 74}\nPIEZA {pz['pieza']} · {'/'.join(pz['reglas'])} · {pz['fuente']}")
        if pz["pieza"] == "a":
            print("  ASISTENCIA")
            for k in ("ofrecieron", "no_ofrecieron"):
                print(f"    {k:16s} {_fmt(pz['asistencia'][k])}")
            print(f"    {'Δ_asistencia':16s} {_fmt(pz['asistencia']['delta'])}")
            for nom, blk in pz["eleccion"].items():
                print(f"  ELECCION · {nom}")
                for k in ("ofrecieron", "no_ofrecieron"):
                    print(f"    {k:16s} {_fmt(blk[k])}")
                print(f"    {'Δ_eleccion':16s} {_fmt(blk['delta'])}")
            for eje, celdas in pz["ejes_secundarios"].items():
                print(f"  eje {eje}")
                for lab, blk in celdas.items():
                    print(f"    {lab:10s} {_fmt(blk['delta'])}")
        else:
            print(f"  cobertura vb20 = {pz['cobertura_vb20']:.4%} · "
                  f"universo_restringido = {pz['universo_restringido']}")
            for rama in ("SECRETO", "OBSERVABLE"):
                print(f"  {rama}")
                for k in ("ayuda_si", "ayuda_no"):
                    print(f"    {k:12s} {_fmt(pz[rama][k])}")
                print(f"    {'Δ':12s} {_fmt(pz[rama]['delta'])}")
            print(f"  Δ_diferencia = {pz['delta_diferencia']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--censo", action="store_true")
    ap.add_argument("--mide", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.censo:
        filas = censo()
        if a.json:
            json.dump(filas, open(a.json, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            print(f"\nescrito {a.json}")
        return
    if a.mide:
        mide(a.json)
        return
    ap.print_help()


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
