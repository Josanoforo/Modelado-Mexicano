#!/usr/bin/env python3
"""ACTO MAESTRA32-E8 · MEDICION-COMPUESTA — COMMIT-2, corrida única.

Ejecuta exactamente la spec congelada de forense/notas/2026-08-30-compuesta-spec.md
(§a-f) para los dos pares SELLADO-ESCALA·SIN-AGREGACION de
milpa/procedencia.yaml::coeficientes_generador_sellados (G1.radio_confianza,
G4.confianza_institucional[justicia]), y escribe el resultado primario al
ejecutable (--escribe). Sin --escribe solo imprime (modo de auditoría/re-
corrida).

Fuentes: data/raw/BD_ENCUCI2020_dbf.zip (ENCUCI_2020_SEC_4_5.dbf +
ENCUCI_2020_SD.dbf para ejes de condicionamiento), data/raw/envipe2025_csv.zip
(TPer_Vic1 + TPer_Vic2 + TMod_Vic, unidas por ID_PER).

Variancia del β̂ de regresión: generalización por linealización del
estimador de conglomerado-último de tests/svystat.py::prop_ultimate_cluster
(Wolter, "Introduction to Variance Estimation"). Para una pendiente de
mínimos cuadrados ponderados beta = Sxy_w/Sxx_w, la variable de influencia
por observación es
    g_i = w_i * (x_i - xbar_w) * (y_i - yhat_i) / Sxx_w
y se agrega EXACTAMENTE como prop_ultimate_cluster agrega y: mismo
agrupamiento por (estrato, upm), misma fórmula de varianza
sum_h (n_h/(n_h-1)) * sum_i (e_h_i - mean_i e_h_i)^2, sustituyendo residual
de proporción por residual de g. Esto es la linealización estándar de un
coeficiente de regresión bajo diseño complejo (Wolter cap. 6; Binder 1983).
"""
import csv
import io
import math
import os
import sys
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests"))
import dbfmini  # noqa: E402
from svystat import prop_ultimate_cluster  # noqa: E402

import yaml  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
PROCEDENCIA_PATH = os.path.join(ROOT, "milpa", "procedencia.yaml")

Z96 = 1.959963985


# ────────────────────────── utilidades numéricas ──────────────────────────

def to_float(s):
    s = (s or "").strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def weighted_reg_ultimate_cluster(rows):
    """rows: iterable de (estrato, upm, w, x, y) con y en {0,1}, x continua.

    beta = pendiente de la regresion lineal ponderada y ~ b0 + beta*x.
    Variancia por linealizacion + conglomerado ultimo (ver docstring del
    modulo). Devuelve dict con beta, se, ic95, n.
    """
    rows = list(rows)
    n = len(rows)
    if n == 0:
        return None
    W = sum(w for _e, _u, w, _x, _y in rows)
    xbar = sum(w * x for _e, _u, w, x, _y in rows) / W
    ybar = sum(w * y for _e, _u, w, _x, y in rows) / W
    Sxx = sum(w * (x - xbar) ** 2 for _e, _u, w, x, _y in rows)
    Sxy = sum(w * (x - xbar) * (y - ybar) for _e, _u, w, x, y in rows)
    if Sxx == 0:
        return None
    beta = Sxy / Sxx
    b0 = ybar - beta * xbar

    # variable de influencia g_i, agregada como en prop_ultimate_cluster
    g_rows = []
    for est, upm, w, x, y in rows:
        yhat = b0 + beta * x
        g = w * (x - xbar) * (y - yhat) / Sxx
        # prop_ultimate_cluster espera (estrato, upm, peso, y) y hace
        # num = sum(w*y); aqui usamos peso=1 y "y"=g para que agregue g
        # directamente por UPM sin reponderar dos veces.
        g_rows.append((est, upm, 1.0, g))

    # var(beta_hat) = var del total ponderado de g por conglomerado ultimo,
    # MISMA agregacion por (estrato,upm) que prop_ultimate_cluster, pero
    # sobre el TOTAL de g (no una proporcion) -- se reusa el motor
    # sustituyendo p_hat por 0 (g ya esta centrada en su propio total) y
    # tomando var = sum_h (n_h/(n_h-1)) sum_i (e_h_i - mean_e)^2, e_h_i = t_h_i.
    upm_totals = {}
    estrato_upms = {}
    for est, upm, _w, g in g_rows:
        key = (est, upm)
        upm_totals[key] = upm_totals.get(key, 0.0) + g
        estrato_upms.setdefault(est, set()).add(upm)

    var = 0.0
    singleton = 0
    for est, upms in estrato_upms.items():
        n_h = len(upms)
        e_list = [upm_totals[(est, u)] for u in upms]
        if n_h < 2:
            singleton += 1
            continue
        mean_e = sum(e_list) / n_h
        ss = sum((e - mean_e) ** 2 for e in e_list)
        var += (n_h / (n_h - 1)) * ss

    se = math.sqrt(var) if var > 0 else 0.0
    lo, hi = beta - Z96 * se, beta + Z96 * se
    return {"beta": beta, "b0": b0, "se": se, "ic95": (lo, hi), "n": n,
            "n_estratos_singleton": singleton}


def cronbach_alpha(item_matrix):
    """item_matrix: lista de listas, una fila por persona, k columnas (items).
    Todas las filas deben tener los k items presentes (caso completo)."""
    if not item_matrix:
        return None
    k = len(item_matrix[0])
    n = len(item_matrix)
    if k < 2 or n < 2:
        return None
    cols = list(zip(*item_matrix))
    item_vars = []
    for col in cols:
        m = sum(col) / n
        v = sum((c - m) ** 2 for c in col) / (n - 1)
        item_vars.append(v)
    totals = [sum(row) for row in item_matrix]
    mt = sum(totals) / n
    total_var = sum((t - mt) ** 2 for t in totals) / (n - 1)
    if total_var == 0:
        return None
    alpha = (k / (k - 1)) * (1 - sum(item_vars) / total_var)
    return alpha


def kr20(item_matrix):
    """item_matrix: filas de 0/1, k items. KR-20 = caso especial de alpha
    con var(item)=p*(1-p) poblacional (n, no n-1) -- se usa la misma formula
    de Cronbach con las varianzas muestrales; para dicotomicos coincide con
    KR-20 hasta el factor de correccion n/(n-1), que aqui se mantiene
    consistente con cronbach_alpha para no introducir un segundo estimador."""
    return cronbach_alpha(item_matrix)


def signo_significativo(ic):
    lo, hi = ic
    if lo > 0:
        return "positivo, significativo"
    if hi < 0:
        return "negativo, significativo"
    return "no distinguible de cero"


# ────────────────────────── carga de datos: G1 / ENCUCI ──────────────────────────

def cargar_encuci():
    zpath = os.path.join(RAW, "BD_ENCUCI2020_dbf.zip")
    with zipfile.ZipFile(zpath) as z:
        z.extract("ENCUCI_2020_SEC_4_5.dbf", "/tmp" if False else os.environ.get("TMPDIR", "/tmp"))
        z.extract("ENCUCI_2020_SD.dbf", os.environ.get("TMPDIR", "/tmp"))
    tmp = os.environ.get("TMPDIR", "/tmp")
    sec45 = os.path.join(tmp, "ENCUCI_2020_SEC_4_5.dbf")
    sd = os.path.join(tmp, "ENCUCI_2020_SD.dbf")

    campos = ["ID_VIV", "ID_PER", "AP5_1_1", "AP5_1_2", "AP5_1_3",
              "AP5_16_1", "AP5_16_2", "AP5_16_3", "AP5_16_4", "AP5_16_5",
              "AP5_16_6", "AP5_16_7", "AP5_16_8", "AP5_16_9", "AP5_16_10",
              "AP5_17", "AP5_18", "FAC_SEL", "DOMINIO", "ESTRATO",
              "UPM_DIS", "EST_DIS"]
    filas_totales = 0
    universo = []
    for rec in dbfmini.read_dbf(sec45, wanted_fields=campos):
        filas_totales += 1
        contacto = any(to_float(rec.get(f"AP5_16_{i}")) == 1.0 for i in range(1, 11))
        if not contacto:
            continue
        items = [to_float(rec.get(f"AP5_1_{i}")) for i in (1, 2, 3)]
        if any(v is None or v == 99.0 for v in items):
            continue
        ap17 = (rec.get("AP5_17") or "").strip()
        ap18 = (rec.get("AP5_18") or "").strip()
        if ap17 == "1" or ap18 == "1":
            desenlace = 1
        elif ap17 == "2" and ap18 == "2":
            desenlace = 0
        else:
            continue  # indeterminado (9, o ambas ausentes)
        w = to_float(rec.get("FAC_SEL"))
        if w is None:
            continue
        universo.append({
            "id_viv": rec.get("ID_VIV"), "id_per": rec.get("ID_PER"),
            "items": items, "desenlace": desenlace, "w": w,
            "estrato": rec.get("EST_DIS"), "upm": rec.get("UPM_DIS"),
            "dominio": rec.get("DOMINIO"), "estrato_socio": rec.get("ESTRATO"),
        })

    # ejes de condicionamiento: EDAD y POS (formalidad) desde SD.dbf
    demog = {}
    for rec in dbfmini.read_dbf(sd, wanted_fields=["ID_VIV", "ID_PER", "EDAD", "POS"]):
        demog[(rec.get("ID_VIV"), rec.get("ID_PER"))] = {
            "edad": to_float(rec.get("EDAD")), "pos": (rec.get("POS") or "").strip()}
    for fila in universo:
        d = demog.get((fila["id_viv"], fila["id_per"]), {})
        fila["edad"] = d.get("edad")
        fila["pos"] = d.get("pos")

    return filas_totales, universo


# ────────────────────────── carga de datos: G4 / ENVIPE ──────────────────────────

def _leer_csv_zip(z, member, campos):
    with z.open(member) as f:
        data = f.read().decode("latin1")
    partes = data.split("\r")
    header = next(csv.reader([partes[0]]))
    idx = {name: (header.index(name) if name in header else None) for name in campos}
    faltan = [k for k, v in idx.items() if v is None]
    if faltan:
        raise RuntimeError(f"{member}: campos no encontrados: {faltan}")
    out = []
    for linea in partes[1:]:
        if not linea.strip():
            continue
        vals = next(csv.reader([linea]))
        out.append({name: vals[i] for name, i in idx.items()})
    return out


def cargar_envipe():
    zpath = os.path.join(RAW, "envipe2025_csv.zip")
    ITEMS_G4 = ["AP5_4_01", "AP5_4_02", "AP5_4_03", "AP5_4_05", "AP5_4_06", "AP5_4_07", "AP5_4_11"]
    AP73 = [f"AP7_3_{i:02d}" for i in range(5, 16)]

    with zipfile.ZipFile(zpath) as z:
        tper1 = _leer_csv_zip(
            z, "tper_vic1_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2025.csv",
            ["ID_PER"] + ITEMS_G4 + ["FAC_ELE", "EST_DIS", "UPM_DIS", "EDAD", "DOMINIO"])
        tper2 = _leer_csv_zip(
            z, "tper_vic2_envipe2025/conjunto_de_datos/conjunto_de_datos_tper_vic2_envipe2025.csv",
            ["ID_PER"] + AP73)
        tmod = _leer_csv_zip(
            z, "tmod_vic_envipe2025/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv",
            ["ID_PER", "BPCOD", "BP1_23"])

    filas_tper1 = len(tper1)

    disparador = {}
    for r in tper2:
        idp = r["ID_PER"]
        tiene = any((r.get(c) or "").strip() == "1" for c in AP73)
        disparador[idp] = disparador.get(idp, False) or tiene

    PRECEDE_MIEDO = {"01", "02", "06", "08"}
    PRECEDE_PRACTICA = {"03", "04", "05", "07"}
    desenlace_por_persona = {}  # id_per -> None(indeterminado)/0/1, con precedencia miedo>practica
    tiene_practica = set()
    for r in tmod:
        idp = r["ID_PER"]
        bp = (r.get("BP1_23") or "").strip()
        if bp in PRECEDE_MIEDO:
            desenlace_por_persona[idp] = 1
        elif bp in PRECEDE_PRACTICA:
            if desenlace_por_persona.get(idp) != 1:
                desenlace_por_persona[idp] = 0
                tiene_practica.add(idp)
        # bp en {'09','99',''} -> no aporta

    tper1_por_id = {r["ID_PER"]: r for r in tper1}

    universo14285 = [idp for idp, v in disparador.items() if v]
    universo = []
    for idp in universo14285:
        if idp not in desenlace_por_persona:
            continue
        rec = tper1_por_id.get(idp)
        if rec is None:
            continue
        items_raw = {c: (rec.get(c) or "").strip() for c in ITEMS_G4}
        w = to_float(rec.get("FAC_ELE"))
        if w is None:
            continue
        universo.append({
            "id_per": idp, "items_raw": items_raw,
            "desenlace": desenlace_por_persona[idp], "w": w,
            "estrato": rec.get("EST_DIS"), "upm": rec.get("UPM_DIS"),
            "edad": to_float(rec.get("EDAD")), "dominio": rec.get("DOMINIO"),
        })

    return filas_tper1, len(universo14285), universo, ITEMS_G4


# ────────────────────────── G1: cómputo ──────────────────────────

def analizar_g1(universo):
    n = len(universo)
    n_4ago = 13435
    diff_pct = abs(n - n_4ago) / n_4ago * 100

    rows_primaria = []
    rows_secundaria = []
    item_matrix_alpha = []
    for fila in universo:
        items = fila["items"]
        theta_p = (sum(items) / 3.0) / 10.0
        rows_primaria.append((fila["estrato"], fila["upm"], fila["w"], theta_p, fila["desenlace"]))
        theta_s = sum(1 for v in items if v >= 6) / 3.0
        rows_secundaria.append((fila["estrato"], fila["upm"], fila["w"], theta_s, fila["desenlace"]))
        item_matrix_alpha.append(items)

    alpha = cronbach_alpha(item_matrix_alpha)
    reg_p = weighted_reg_ultimate_cluster(rows_primaria)
    reg_s = weighted_reg_ultimate_cluster(rows_secundaria)

    # condicionamiento: formalidad(pos), edad (terciles), n>=30
    cond = {}
    for eje, keyfn in [
        ("formalidad(POS)", lambda f: f.get("pos") or "(vacio)"),
        ("edad_grupo", lambda f: _grupo_edad(f.get("edad"))),
    ]:
        grupos = {}
        for fila in universo:
            g = keyfn(fila)
            grupos.setdefault(g, []).append(fila)
        resultados = []
        for g, filas in sorted(grupos.items()):
            if len(filas) < 30:
                continue
            rows = [(f["estrato"], f["upm"], f["w"],
                      (sum(f["items"]) / 3.0) / 10.0, f["desenlace"]) for f in filas]
            r = weighted_reg_ultimate_cluster(rows)
            if r:
                resultados.append((g, len(filas), r["beta"], r["ic95"]))
        cond[eje] = resultados
    cond["ingreso"] = "NO LOCALIZABLE: ningún campo de ingreso en ENCUCI_2020_SD.dbf/VIV.dbf " \
        "(campos revisados: ambas tablas no traen variable de ingreso monetario; " \
        "limitación declarada, no bloquea el commit -- condicionamiento es diagnóstico)."

    return {
        "n": n, "n_4ago": n_4ago, "diff_pct": diff_pct,
        "alpha": alpha, "primaria": reg_p, "secundaria": reg_s,
        "condicionamiento": cond,
    }


def _grupo_edad(edad):
    if edad is None:
        return "(vacio)"
    if edad < 30:
        return "18-29"
    if edad < 45:
        return "30-44"
    if edad < 60:
        return "45-59"
    return "60+"


# ────────────────────────── G4: cómputo ──────────────────────────

def analizar_g4(universo, items_g4):
    n = len(universo)
    n_4ago = 13023
    diff_pct = abs(n - n_4ago) / n_4ago * 100

    rows_primaria = []
    rows_secundaria = []
    item_matrix_alpha = []
    n_primaria = 0
    n_secundaria = 0
    for fila in universo:
        confia = []
        identificadas = 0
        dicot = []
        completo = True
        for c in items_g4:
            v = fila["items_raw"][c]
            if v in ("1", "2"):
                confia.append(1)
                identificadas += 1
                dicot.append(1)
            elif v in ("3", "4"):
                confia.append(0)
                identificadas += 1
                dicot.append(0)
            else:
                dicot.append(None)
                completo = False
        if identificadas >= 4:
            theta_p = sum(confia) / identificadas
            n_primaria += 1
            rows_primaria.append((fila["estrato"], fila["upm"], fila["w"], theta_p, fila["desenlace"]))
        if completo:
            theta_s = sum(confia) / 7.0
            n_secundaria += 1
            rows_secundaria.append((fila["estrato"], fila["upm"], fila["w"], theta_s, fila["desenlace"]))
            item_matrix_alpha.append(dicot)

    alpha = cronbach_alpha(item_matrix_alpha)  # KR-20 vía caso completo (7/7)
    reg_p = weighted_reg_ultimate_cluster(rows_primaria)
    reg_s = weighted_reg_ultimate_cluster(rows_secundaria)
    reg_s_metodo = "prop_ultimate_cluster-linealizado"
    if reg_s is None or len(rows_secundaria) < 30:
        reg_s_metodo = "n insuficiente para conglomerado-ultimo en caso completo -- ver bootstrap de respaldo"
        reg_s = _bootstrap_respaldo(rows_secundaria) if rows_secundaria else None

    cond = {}
    for eje, keyfn in [
        ("edad_grupo", lambda f: _grupo_edad(f.get("edad"))),
        ("dominio", lambda f: f.get("dominio") or "(vacio)"),
    ]:
        grupos = {}
        for fila in universo:
            g = keyfn(fila)
            grupos.setdefault(g, []).append(fila)
        resultados = []
        for g, filas in sorted(grupos.items()):
            rows = []
            for f in filas:
                confia = []
                identificadas = 0
                for c in items_g4:
                    v = f["items_raw"][c]
                    if v in ("1", "2"):
                        confia.append(1)
                        identificadas += 1
                    elif v in ("3", "4"):
                        confia.append(0)
                        identificadas += 1
                if identificadas >= 4:
                    rows.append((f["estrato"], f["upm"], f["w"], sum(confia) / identificadas, f["desenlace"]))
            if len(rows) < 30:
                continue
            r = weighted_reg_ultimate_cluster(rows)
            if r:
                resultados.append((g, len(rows), r["beta"], r["ic95"]))
        cond[eje] = resultados

    return {
        "n": n, "n_4ago": n_4ago, "diff_pct": diff_pct,
        "n_primaria": n_primaria, "n_secundaria": n_secundaria,
        "alpha": alpha, "primaria": reg_p, "secundaria": reg_s,
        "secundaria_metodo": reg_s_metodo,
        "condicionamiento": cond,
    }


def _bootstrap_respaldo(rows, B=10000, seed=42):
    import random
    if not rows:
        return None
    rnd = random.Random(seed)
    n = len(rows)
    betas = []
    base = weighted_reg_ultimate_cluster(rows)
    if base is None:
        return None
    for _ in range(B):
        muestra = [rows[rnd.randrange(n)] for _ in range(n)]
        W = sum(r[2] for r in muestra)
        if W == 0:
            continue
        xbar = sum(r[2] * r[3] for r in muestra) / W
        ybar = sum(r[2] * r[4] for r in muestra) / W
        Sxx = sum(r[2] * (r[3] - xbar) ** 2 for r in muestra)
        if Sxx == 0:
            continue
        Sxy = sum(r[2] * (r[3] - xbar) * (r[4] - ybar) for r in muestra)
        betas.append(Sxy / Sxx)
    betas.sort()
    if not betas:
        return None
    lo = betas[int(0.025 * len(betas))]
    hi = betas[int(0.975 * len(betas))]
    return {"beta": base["beta"], "ic95": (lo, hi), "n": n, "metodo": f"bootstrap percentil B={len(betas)} seed={seed}"}


# ────────────────────────── impresión ──────────────────────────

def imprimir(g1, g4):
    print("=" * 78)
    print("MAESTRA32-E8 · MEDICION-COMPUESTA -- corrida única, salida cruda")
    print("=" * 78)

    print("\n--- G1.radio_confianza (ENCUCI 2020 SEC_4_5) ---")
    print(f"n universo re-derivado: {g1['n']} (4/ago: {g1['n_4ago']}, diff {g1['diff_pct']:.3f}%)")
    if g1["diff_pct"] > 2:
        print("FALSADOR DISPARADO (>2%): se reporta la diferencia, se sigue con el universo re-derivado (A-bis 4).")
    print(f"alpha de Cronbach (AP5_1_1/2/3, 0-10): {g1['alpha']}")
    p = g1["primaria"]
    print(f"beta primaria (media/10, y=tramite.mordida.discrecional): {p['beta']:.6f} "
          f"IC95[{p['ic95'][0]:.6f},{p['ic95'][1]:.6f}] n={p['n']} -> {signo_significativo(p['ic95'])}")
    s = g1["secundaria"]
    print(f"beta secundaria (prop items>=6): {s['beta']:.6f} "
          f"IC95[{s['ic95'][0]:.6f},{s['ic95'][1]:.6f}] n={s['n']} -> {signo_significativo(s['ic95'])}")
    print("Condicionamiento (n>=30 por celda):")
    for eje, filas in g1["condicionamiento"].items():
        if eje == "ingreso":
            print(f"  {eje}: {filas}")
            continue
        print(f"  eje={eje}")
        for g, n_, beta, ic in filas:
            print(f"    {g}: n={n_} beta={beta:.6f} IC95[{ic[0]:.6f},{ic[1]:.6f}] -> {signo_significativo(ic)}")

    print("\n--- G4.confianza_institucional[justicia] (ENVIPE 2025 TPer_Vic1+TPer_Vic2+TMod_Vic) ---")
    print(f"n universo re-derivado (disparador+desenlace): {g4['n']} (4/ago: {g4['n_4ago']}, diff {g4['diff_pct']:.3f}%)")
    if g4["diff_pct"] > 2:
        print("FALSADOR DISPARADO (>2%): se reporta la diferencia, se sigue con el universo re-derivado (A-bis 4).")
    print(f"n primaria (>=4/7 identificadas): {g4['n_primaria']}  n secundaria (7/7 caso completo): {g4['n_secundaria']}")
    print(f"KR-20 (7 items dicotómicos, caso completo): {g4['alpha']}")
    p = g4["primaria"]
    print(f"beta primaria (prop confianza entre identificadas): {p['beta']:.6f} "
          f"IC95[{p['ic95'][0]:.6f},{p['ic95'][1]:.6f}] n={p['n']} -> {signo_significativo(p['ic95'])}")
    s = g4["secundaria"]
    if s:
        print(f"beta secundaria (caso completo 7/7) [{g4['secundaria_metodo']}]: {s['beta']:.6f} "
              f"IC95[{s['ic95'][0]:.6f},{s['ic95'][1]:.6f}] n={s.get('n')} -> {signo_significativo(s['ic95'])}")
    else:
        print("beta secundaria: no calculable (universo de caso completo vacío o insuficiente)")
    print("Condicionamiento (n>=30 por celda):")
    for eje, filas in g4["condicionamiento"].items():
        print(f"  eje={eje}")
        for g, n_, beta, ic in filas:
            print(f"    {g}: n={n_} beta={beta:.6f} IC95[{ic[0]:.6f},{ic[1]:.6f}] -> {signo_significativo(ic)}")

    print("\n--- Veredictos B-bis (pre-registrados, spec §f) ---")
    for nombre, r in [("G1", g1["primaria"]), ("G4", g4["primaria"])]:
        lo, hi = r["ic95"]
        no_dist = lo <= 0 <= hi
        print(f"{nombre}: IC incluye 0 -> {'SI, sufijo ·NO-DISTINGUIBLE-DE-CERO' if no_dist else 'no'}")
    print("=" * 78)


# ────────────────────────── escritura al ejecutable ──────────────────────────

RESERVA_G1 = (
    "ADR-57 (a): la concordancia de signo entre este β̂ marginal y el ASIGNADO "
    "(G1 -0.35) NO corrobora el asignado -- condicionar (Encargo X, ver "
    "eje_condicionante arriba) mostró que el marginal por ítem no es estable "
    "(33 de 39 celdas invierten el signo, recontado por ADR-61). El compuesto "
    "de este acto (β̂={beta:.6f}) hereda la misma reserva: asociar ≠ identificar."
)
RESERVA_G4 = (
    "ADR-57 (a): los 7 β̂ por ítem son todos negativos y significativos "
    "(6 de 49 celdas condicionadas invierten). El compuesto de este acto "
    "(β̂={beta:.6f}) hereda la misma reserva de asociación marginal: "
    "asociar ≠ identificar. marca_c2 (histórica): comparte desenlace y "
    "universo con G4.exposicion_violencia -- no se combinan entre entradas."
)


def escribir_ejecutable(g1, g4, aplicar):
    with open(PROCEDENCIA_PATH, encoding="utf-8") as fh:
        crudo_texto = fh.read()
    crudo = yaml.safe_load(crudo_texto)
    sellados = crudo["coeficientes_generador_sellados"]

    resultados = {}
    for entrada in sellados:
        if entrada["gen"] == "G1" and entrada["coef"] == "radio_confianza":
            resultados[("G1", "radio_confianza")] = (entrada, g1, "media de AP5_1_1/2/3 en 0-10, /10 -> [0,1]", RESERVA_G1)
        if entrada["gen"] == "G4" and entrada["coef"] == "confianza_institucional":
            resultados[("G4", "confianza_institucional")] = (entrada, g4, "proporción de instituciones (de las 7) en que confía, entre quienes identifican >=4 de 7", RESERVA_G4)

    cambios = []
    for (gen, coef), (entrada, resultado, definicion, reserva_tpl) in resultados.items():
        if resultado["alpha"] is None or resultado["alpha"] < 0.50:
            cambios.append((gen, coef, None, resultado["alpha"], "NO ESCRITO: alpha < 0.50 (hallazgo de dimensionalidad)"))
            continue
        p = resultado["primaria"]
        lo, hi = p["ic95"]
        no_dist = lo <= 0 <= hi
        rotulo_previo = entrada.get("rotulo", "")
        nuevo_rotulo = "ASOCIACION-MEDIDA·COMPUESTO·MARGINAL" + ("·NO-DISTINGUIBLE-DE-CERO" if no_dist else "")
        nuevo_bloque = {
            "valor_ejecutable": round(p["beta"], 6),
            "ic": f"IC95% {lo:.6f},{hi:.6f}",
            "escala": "proporción ponderada [0,1], enlace identidad (ADR-220)",
            "definicion_compuesto": definicion,
            "alpha": round(resultado["alpha"], 4),
            "rotulo": nuevo_rotulo,
            "reserva": reserva_tpl.format(beta=p["beta"]) + f" Rótulo previo (histórico): {rotulo_previo}.",
        }
        cambios.append((gen, coef, nuevo_bloque, resultado["alpha"], "ESCRITO" if aplicar else "PENDIENTE (dry-run)"))

    if aplicar:
        _aplicar_texto(crudo_texto, cambios)
    return cambios


def _aplicar_texto(crudo_texto, cambios):
    lineas = crudo_texto.split("\n")
    out = []
    i = 0
    n = len(lineas)
    # localizamos cada bloque "- gen: X\n  coef: Y" dentro de
    # coeficientes_generador_sellados y le insertamos/actualizamos campos
    # antes de la línea "  fuente:" (última clave de cada entrada).
    pendientes = {(g, c): b for g, c, b, _a, _s in cambios if b is not None}
    dentro_seccion = False
    gen_actual = coef_actual = None
    while i < n:
        linea = lineas[i]
        if linea.strip() == "coeficientes_generador_sellados:":
            dentro_seccion = True
            out.append(linea)
            i += 1
            continue
        if dentro_seccion and linea.startswith("#") and linea.strip().startswith("#") and "═" in linea:
            dentro_seccion = False
        if dentro_seccion and linea.strip().startswith("- gen:"):
            gen_actual = linea.split(":", 1)[1].strip()
        if dentro_seccion and linea.strip().startswith("coef:"):
            coef_actual = linea.split(":", 1)[1].strip()
        if dentro_seccion and linea.strip().startswith("rotulo:") and (gen_actual, coef_actual) in pendientes:
            bloque = pendientes[(gen_actual, coef_actual)]
            indent = linea[:len(linea) - len(linea.lstrip())]
            out.append(f"{indent}rotulo: {bloque['rotulo']}")
            i += 1
            # saltar la vieja línea "reserva:" (puede seguir en la siguiente línea)
            if i < n and lineas[i].strip().startswith("reserva:"):
                out.append(f"{indent}reserva: '{bloque['reserva']}'")
                i += 1
            out.append(f"{indent}valor_ejecutable: {bloque['valor_ejecutable']}")
            out.append(f"{indent}ic: {bloque['ic']}")
            out.append(f"{indent}escala: {bloque['escala']}")
            out.append(f"{indent}definicion_compuesto: '{bloque['definicion_compuesto']}'")
            out.append(f"{indent}alpha: {bloque['alpha']}")
            continue
        out.append(linea)
        i += 1
    nuevo_texto = "\n".join(out)
    with open(PROCEDENCIA_PATH, "w", encoding="utf-8") as fh:
        fh.write(nuevo_texto)
    # verificación
    with open(PROCEDENCIA_PATH, encoding="utf-8") as fh:
        yaml.safe_load(fh)


def main():
    aplicar = "--escribe" in sys.argv

    filas_totales_encuci, universo_g1 = cargar_encuci()
    g1 = analizar_g1(universo_g1)

    filas_tper1, n_disparador, universo_g4, items_g4 = cargar_envipe()
    g4 = analizar_g4(universo_g4, items_g4)

    imprimir(g1, g4)

    cambios = escribir_ejecutable(g1, g4, aplicar)
    print("\n--- Escritura al ejecutable ---")
    for gen, coef, bloque, alpha, estado in cambios:
        print(f"{gen}.{coef}: alpha={alpha} -> {estado}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
