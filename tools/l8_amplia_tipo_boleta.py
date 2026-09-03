#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA35-L8 · CIVICA-8-ENTIDADES -- amplia el panel de L3 con Hidalgo,
Aguascalientes y Veracruz via SICEE (deposito de mesa, ACTO MAESTRA35-A1 relanzamiento).

Hermano de tools/mide_participacion_tipo_boleta.py (ACTO MAESTRA35-L3): importa
sus funciones y NO lo modifica, de modo que la corrida de L3 se reproduce byte a
byte como control de regresion (--control-l3), igual que L3 hizo con L6.

Metodo de lectura, declarado antes de correr nada: se reagrega SIEMPRE desde
CASILLA (mismo metodo que bc_casilla/chihuahua_casilla/zacatecas2016_casilla de
L3), nunca desde el MUN.csv pre-agregado que SICEE tambien publica -- ese MUN.csv
se usa solo como CONTROL cruzado (Sec.1.7.6). Razon medida en el censo (P0): el
MUN.csv de Hidalgo 2020 deja en blanco ACAXOCHITLAN e IXMIQUILPAN (estatus
'GRUPO DE TRABAJO' en el acta), pero su CASILLA.csv trae los votos completos
(16327 y 36412 respectivamente) -- reagregar rescata los 84/84 municipios en vez
de 82/84. El de Veracruz 2017 confirma, al mismo nivel, que CAMARON DE TEJEDA,
EMILIANO ZAPATA y SAYULA DE ALEMAN tienen TOTAL_VOTOS=0 en las DOS tablas: ahi no
hay nada que reagregacion pueda rescatar, es un hueco real de la fuente.

Modos:
    --control-l3     re-corre mide_participacion_tipo_boleta.corre() sobre el
                     panel de L3 (sin tocarlo) y compara con su JSON archivado
    --json <ruta>    corre el modelo ampliado y vuelca el resultado
"""
import argparse, csv, io, json, os, re, sys, unicodedata, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mide_participacion_tipo_boleta as L3

_SICEE = "data/raw/electoral_sicee_local"

# Veracruz renombro MEDELLIN -> MEDELLIN DE BRAVO entre 2017 y 2021 (mismo id
# SICEE, id=106 en ambos anios; verificado por id, no solo por nombre).
_ALIAS = {"MEDELLIN": "MEDELLIN DE BRAVO"}


def _norm(s):
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^A-Za-z0-9 ]", " ", s)
    s = re.sub(r"\s+", " ", s).strip().upper()
    return _ALIAS.get(s, s)


def _num(v):
    if v is None:
        return None
    s = str(v).strip().replace(",", "")
    if s in ("", "-", "--"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _leer_csv(zpath, member):
    with zipfile.ZipFile(zpath) as zf:
        with zf.open(member) as f:
            txt = io.TextIOWrapper(f, encoding="utf-8-sig", errors="replace")
            return list(csv.reader(txt))


def _agrega_casilla(filas):
    """Suma TOTAL_VOTOS y LISTA_NOMINAL por municipio desde CASILLA. Nunca se
    confia en un TOTAL pre-agregado de la fuente sin cruzarlo (Sec.1.7.6)."""
    cab = filas[0]
    i_mun, i_tot, i_ln = cab.index("MUNICIPIO"), cab.index("TOTAL_VOTOS"), cab.index("LISTA_NOMINAL")
    agg = {}
    for r in filas[1:]:
        if max(i_mun, i_tot, i_ln) >= len(r):
            continue
        mun = r[i_mun]
        if not mun or not str(mun).strip():
            continue
        k = _norm(mun)
        tot, ln = _num(r[i_tot]), _num(r[i_ln])
        a = agg.setdefault(k, [0.0, 0.0])
        if tot is not None:
            a[0] += tot
        if ln is not None:
            a[1] += ln
    return agg


def _control_vs_mun_publicado(agg, zpath, member):
    """Cruza contra el MUN.csv que SICEE tambien publica (Sec.1.7.6): |Δvotos|,
    |Δlista nominal|, e identidad TOTAL/LN vs PARTICIPACION publicada si existe."""
    filas = _leer_csv(zpath, member)
    cab = filas[0]
    i_mun, i_tot, i_ln = cab.index("MUNICIPIO"), cab.index("TOTAL_VOTOS"), cab.index("LISTA_NOMINAL")
    i_pct = cab.index("PARTICIPACION") if "PARTICIPACION" in cab else None
    pub = {}
    for r in filas[1:]:
        if i_mun >= len(r) or not r[i_mun]:
            continue
        k = _norm(r[i_mun])
        pub[k] = (_num(r[i_tot]) if i_tot < len(r) else None,
                  _num(r[i_ln]) if i_ln < len(r) else None,
                  (_num(r[i_pct]) if (i_pct is not None and i_pct < len(r)) else None))
    comunes = set(agg) & set(pub)
    dv = max((abs(agg[k][0] - pub[k][0]) for k in comunes if pub[k][0] is not None), default=0.0)
    dl = max((abs(agg[k][1] - pub[k][1]) for k in comunes if pub[k][1] is not None), default=0.0)
    peor_pct, n_pct, mayores_1pp = 0.0, 0, 0
    for k in comunes:
        tot, ln, q = agg[k][0], agg[k][1], pub[k][2]
        if q is None or ln <= 0:
            continue
        qq = q * 100.0 if q <= 1.5 else q
        d = abs(100.0 * tot / ln - qq)
        peor_pct = max(peor_pct, d); n_pct += 1
        if d > 1.0:
            mayores_1pp += 1
    return {"comunes_con_mun_publicado": len(comunes),
            "max_abs_delta_votos_vs_mun_publicado": dv,
            "max_abs_delta_lista_nominal_vs_mun_publicado": dl,
            "identidad_total_sobre_ln_vs_pct_publicado": (
                {"casillas_municipio": n_pct, "max_abs_pp": peor_pct, "n_mayor_1pp": mayores_1pp}
                if n_pct else "fuente no publica PARTICIPACION este anio")}


_ARCHIVOS = {
    ("Hidalgo", 2016): ("sicee_local_hgo_pel_2016.zip", "HGO_PEL_2016/AYUNTAMIENTOS_csv/2016_SEE_AYUN_HGO_{}.csv"),
    ("Hidalgo", 2020): ("sicee_local_hgo_pel_2020.zip", "HGO_PEL_2020/AYUNTAMIENTOS_csv/2020_SEE_AYUN_HGO_{}.csv"),
    ("Aguascalientes", 2016): ("sicee_local_ags_pel_2016.zip", "AGS_PEL_2016/AYUNTAMIENTOS_csv/2016_SEE_AYUN_AGS_{}.csv"),
    ("Aguascalientes", 2019): ("sicee_local_ags_pel_2019.zip", "AGS_PEL_2019/AYUNTAMIENTOS_csv/2019_SEE_AYUN_AGS_{}.csv"),
    ("Aguascalientes", 2021): ("sicee_local_ags_pel_2021.zip", "AGS_PEL_2021/AYUNTAMIENTOS_csv/2021_SEE_AYUN_AGS_{}.csv"),
    ("Aguascalientes", 2024): ("sicee_local_ags_pel_2024.zip", "AGS_PEL_2024/AYUNTAMIENTOS_csv/2024_SEE_AYUN_AGS_{}.csv"),
    ("Veracruz", 2017): ("sicee_local_ver_pel_2017.zip", "VER_PEL_2017/VER_PEL_2017/AYUNTAMIENTOS_csv/2017_SEE_AYUN_VER_{}.csv"),
    ("Veracruz", 2021): ("sicee_local_ver_pel_2021.zip", "VER_PEL_2021/AYUNTAMIENTOS_csv/2021_SEE_AYUN_VER_{}.csv"),
}


def sicee_entidad_anio(entidad, anio):
    zname, patron = _ARCHIVOS[(entidad, anio)]
    zpath = os.path.join(_SICEE, zname)
    agg = _agrega_casilla(_leer_csv(zpath, patron.format("CAS")))
    ctrl = _control_vs_mun_publicado(agg, zpath, patron.format("MUN"))
    datos = {k: (v[0], v[1]) for k, v in agg.items() if v[0] > 0 and v[1] > 0}
    ctrl["municipios_agregados"] = len(agg)
    ctrl["municipios_con_dato_completo"] = len(datos)
    ctrl["sin_dato"] = sorted(k for k, v in agg.items() if not (v[0] > 0 and v[1] > 0))
    return datos, ctrl


# ═══════════════════════════ panel ampliado (P0/P1) ═══════════════════════════
NUEVAS = {"Hidalgo": [2016, 2020], "Aguascalientes": [2016, 2019, 2021, 2024], "Veracruz": [2017, 2021]}
SERIES_L8 = dict(L3.SERIES_L3, **NUEVAS)


def panel_l8():
    P, ctrl = L3.panel_l3()
    ctrl = {"l3": ctrl}
    for ent, anios in NUEVAS.items():
        for a in anios:
            P[(ent, a)], ctrl[f"sicee_{ent}_{a}"] = sicee_entidad_anio(ent, a)
    return P, ctrl


def tratamiento_l8():
    cal = L3.lee_calendario()
    return {(ent, a): L3.dpres_dint(a, cal[ent][a]) for ent, anios in SERIES_L8.items() for a in anios}


def participacion_l8(P):
    y, fuera = {}, []
    for (ent, anio), d in P.items():
        if ent not in SERIES_L8 or anio not in SERIES_L8[ent]:
            continue
        for m, (v, ln) in d.items():
            if ln is None or ln <= 0 or v is None:
                fuera.append((ent, anio, m, "sin dato")); continue
            p = 100.0 * v / ln
            if not (0 < p <= 100):
                fuera.append((ent, anio, m, f"fuera de (0,100]: {p:.4f}")); continue
            y[(ent, anio, m)] = p
    return y, fuera


def universo_l8(P):
    univ, perdidos = {}, {}
    for ent, anios in SERIES_L8.items():
        conj = [set(P[(ent, a)]) for a in anios]
        comun = set.intersection(*conj)
        univ[ent] = comun
        perdidos[ent] = sorted(set.union(*conj) - comun)
    return univ, perdidos


def transiciones_l8(y, univ, D):
    T = []
    for ent, anios in SERIES_L8.items():
        for a, b in zip(anios, anios[1:]):
            dpa, dia = D[(ent, a)]; dpb, dib = D[(ent, b)]
            ddp, ddi = dpb - dpa, dib - dia
            for m in sorted(univ[ent]):
                if (ent, a, m) in y and (ent, b, m) in y:
                    T.append({"entidad": ent, "de": a, "a": b, "municipio": m,
                              "dy": y[(ent, b, m)] - y[(ent, a, m)],
                              "hueco": b - a, "ddp": ddp, "ddi": ddi,
                              "clase": L3.clase_transicion(ddp, ddi),
                              "y0": y[(ent, a, m)], "y1": y[(ent, b, m)]})
    return T


# ═════════════════════ Sec.1.7.7-bis: control de regresion sobre L3 ══════════
def control_regresion_l3():
    """Re-corre mide_participacion_tipo_boleta.corre() (SIN TOCARLO) y exige que
    reproduzca data/l3-resultados-tipo-boleta-v1_0.json BYTE A BYTE. PARO si no."""
    import hashlib
    ref = "data/l3-resultados-tipo-boleta-v1_0.json"
    obtenido = json.dumps(L3.corre(), ensure_ascii=False, indent=1, default=str) + "\n"
    esperado = open(ref, encoding="utf-8").read()
    h_obt = hashlib.sha256(obtenido.encode("utf-8")).hexdigest()
    h_esp = hashlib.sha256(esperado.encode("utf-8")).hexdigest()
    return {"identico_byte_a_byte": obtenido == esperado,
            "sha256_recorrida": h_obt, "sha256_archivada": h_esp,
            "bytes_recorrida": len(obtenido.encode("utf-8")),
            "bytes_archivada": len(esperado.encode("utf-8")),
            "PARO": obtenido != esperado}


def _cuantil(v, q):
    v = sorted(v)
    return v[min(len(v) - 1, max(0, int(q * len(v))))]


def corre():
    ctrl_l6 = L3.control_regresion_l6()
    if ctrl_l6.get("PARO"):
        return {"PARO": True, "control_regresion_l6": ctrl_l6}
    ctrl_l3 = control_regresion_l3()
    if ctrl_l3.get("PARO"):
        return {"PARO": True, "control_regresion_l6": ctrl_l6, "control_regresion_l3": ctrl_l3}

    P, ctrl_lectura = panel_l8()
    D = tratamiento_l8()
    y, fuera = participacion_l8(P)
    univ, perdidos = universo_l8(P)
    T = transiciones_l8(y, univ, D)

    res = {"control_regresion_l6": ctrl_l6, "control_regresion_l3": ctrl_l3,
           "n_transiciones_municipio": len(T),
           "n_municipios_por_entidad": {e: len(univ[e]) for e in univ},
           "municipios_perdidos": perdidos, "fuera_de_rango": fuera,
           "controles_lectura": ctrl_lectura}

    est = L3._ols(T)
    res["estimador"] = {
        "alpha_pp_por_anio": est["hueco"], "beta_pres_pp": est["ddp"], "beta_int_pp": est["ddi"],
        "wild_cluster_alpha": L3.wild_cluster(T, "hueco"),
        "wild_cluster_beta_pres": L3.wild_cluster(T, "ddp"),
        "wild_cluster_beta_int": L3.wild_cluster(T, "ddi"),
        "wild_cluster_contraste_int_menos_pres": L3.wild_cluster_contraste(T),
        "ic95_bootstrap_municipio": L3.boot_municipio(T)}

    est_sa = L3._ols(T, ("ddp", "ddi"))
    res["variante_sin_alpha"] = {"beta_pres_pp": est_sa["ddp"], "beta_int_pp": est_sa["ddi"]}

    clases = {}
    for t in T:
        k = L3.identifica(t["ddp"], t["ddi"])
        clases.setdefault(k, {"n_municipio_transicion": 0, "transiciones": set()})
        clases[k]["n_municipio_transicion"] += 1
        clases[k]["transiciones"].add(f'{t["entidad"]} {t["de"]}->{t["a"]}')
    res["identificacion_del_panel"] = {
        k: {"n_municipio_transicion": v["n_municipio_transicion"], "transiciones": sorted(v["transiciones"])}
        for k, v in clases.items()}
    res["n_transiciones_STAY"] = len({f'{t["entidad"]} {t["de"]}->{t["a"]}' for t in T if t["clase"] == "STAY"})

    # entidad "tratada medible": TRATADO en p0-tratamiento Y con >=1 transicion SWITCH en el panel
    trat = {}
    with open(L3.TRATAMIENTO, encoding="utf-8") as fh:
        lineas = [l.rstrip("\n") for l in fh]
    cab = lineas[1].split("\t")
    for l in lineas[2:]:
        if not l.strip():
            continue
        p = l.split("\t")
        trat[p[cab.index("entidad")]] = p[cab.index("estatus")]
    switch_entidades = {t["entidad"] for t in T if t["clase"] == "SWITCH"}
    res["entidades_tratadas_medibles"] = sorted(e for e in switch_entidades if trat.get(e) == "TRATADO")
    res["n_entidades_tratadas_medibles"] = len(res["entidades_tratadas_medibles"])
    res["entidades_solo_STAY_sin_switch_medible"] = sorted(
        {t["entidad"] for t in T if t["clase"] == "STAY"} - switch_entidades)

    res["por_transicion"] = []
    for ent, anios in SERIES_L8.items():
        for a, b in zip(anios, anios[1:]):
            sub = [t for t in T if t["entidad"] == ent and t["de"] == a]
            if not sub:
                continue
            res["por_transicion"].append({
                "entidad": ent, "de": a, "a": b, "hueco": b - a,
                "tipo_de": L3.etiqueta_pata(a, D[(ent, a)] != (0, 0)),
                "tipo_a": L3.etiqueta_pata(b, D[(ent, b)] != (0, 0)),
                "ddp": sub[0]["ddp"], "ddi": sub[0]["ddi"], "clase": sub[0]["clase"], "n": len(sub),
                "y_de_media": sum(t["y0"] for t in sub) / len(sub),
                "y_a_media": sum(t["y1"] for t in sub) / len(sub),
                "dy_media": sum(t["dy"] for t in sub) / len(sub),
                "dy_mediana": _cuantil([t["dy"] for t in sub], 0.5)})

    stay = [t for t in T if t["clase"] == "STAY"]
    a_stay = (sum(t["dy"] for t in stay) / sum(t["hueco"] for t in stay)) if stay else None
    res["att_por_transicion"] = {"alpha_solo_STAY_pp_por_anio": a_stay, "n_transiciones_STAY_municipio": len(stay)}
    if a_stay is not None:
        for t0 in sorted({(t["entidad"], t["de"], t["a"]) for t in T if t["clase"] == "SWITCH"}):
            ent, a, b = t0
            sub = [t for t in T if t["entidad"] == ent and t["de"] == a and t["clase"] == "SWITCH"]
            media = sum(t["dy"] for t in sub) / len(sub)
            res["att_por_transicion"][f"{ent}_{a}_{b}"] = {
                "delta_bruto_pp": media, "hueco": b - a, "ddp": sub[0]["ddp"], "ddi": sub[0]["ddi"],
                "att_pp": media - a_stay * (b - a), "n": len(sub)}

    res["agregado_estatal"] = []
    for (ent, anio), d in sorted(P.items()):
        if ent not in SERIES_L8 or anio not in SERIES_L8[ent]:
            continue
        sub = {m: d[m] for m in univ[ent] if m in d}
        v = sum(x[0] for x in sub.values()); l = sum(x[1] for x in sub.values())
        res["agregado_estatal"].append({
            "entidad": ent, "anio": anio, "n": len(sub), "votos": v, "lista_nominal": l,
            "participacion_agregada_pp": 100.0 * v / l if l else None,
            "D_pres": D[(ent, anio)][0], "D_int": D[(ent, anio)][1]})

    tam = {}
    for ent, anios in SERIES_L8.items():
        base = P[(ent, anios[0])]
        for m in univ[ent]:
            if m in base:
                tam[(ent, m)] = base[m][1]
    vals = sorted(tam.values()); q1 = _cuantil(vals, 1/3); q2 = _cuantil(vals, 2/3)
    res["heterogeneidad_tamano"] = {"cortes_lista_nominal": [q1, q2]}
    for nom, cond in (("chico", lambda v: v <= q1), ("mediano", lambda v: q1 < v <= q2), ("grande", lambda v: v > q2)):
        Ts = [t for t in T if cond(tam.get((t["entidad"], t["municipio"]), 0))]
        e = L3._ols(Ts) if len(Ts) > 3 else None
        res["heterogeneidad_tamano"][nom] = {"n": len(Ts)} | (
            {"alpha": e["hueco"], "beta_pres": e["ddp"], "beta_int": e["ddi"]} if e else {})

    res["sensibilidad"] = {}
    for nom, filtro in (("sin_hueco_1", lambda t: t["hueco"] != 1),
                        ("sin_Coahuila", lambda t: t["entidad"] != "Coahuila"),
                        ("sin_Durango", lambda t: t["entidad"] != "Durango"),
                        ("solo_entidades_nuevas_de_L3", lambda t: t["entidad"] in ("Baja California", "Chihuahua")),
                        ("solo_panel_de_L6", lambda t: t["entidad"] in ("Coahuila", "Nayarit", "Zacatecas", "Durango")),
                        ("sin_Hidalgo", lambda t: t["entidad"] != "Hidalgo"),
                        ("sin_Aguascalientes", lambda t: t["entidad"] != "Aguascalientes"),
                        ("sin_Veracruz", lambda t: t["entidad"] != "Veracruz"),
                        ("solo_entidades_nuevas_de_L8", lambda t: t["entidad"] in ("Hidalgo", "Aguascalientes", "Veracruz"))):
        Ts = [t for t in T if filtro(t)]
        e = L3._ols(Ts) if len(Ts) > 3 else None
        res["sensibilidad"][nom] = {"n": len(Ts), "entidades": sorted({t["entidad"] for t in Ts})} | (
            {"alpha": e["hueco"], "beta_pres": e["ddp"], "beta_int": e["ddi"]} if e else
            {"nota": "no identificado con este subconjunto"})

    res["descomposicion_L4"] = {
        "delta_L4_pp": 10.4790,
        "componentes_para_2023_no_conc_-> 2024_presidencial_hueco_1": {
            "alpha_x_hueco": est["hueco"] * 1, "beta_pres": est["ddp"],
            "suma_explicada_pp": est["hueco"] * 1 + est["ddp"]}}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--control-l3", action="store_true")
    ap.add_argument("--censo", action="store_true")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    if a.control_l3:
        print(json.dumps(control_regresion_l3(), ensure_ascii=False, indent=1))
        return
    if a.censo:
        for (ent, anio) in sorted(_ARCHIVOS):
            datos, ctrl = sicee_entidad_anio(ent, anio)
            print(json.dumps({"entidad": ent, "anio": anio, "n_con_dato": len(datos), **ctrl},
                             ensure_ascii=False, indent=1, default=str))
        return
    salida = corre()
    texto = json.dumps(salida, ensure_ascii=False, indent=1, default=str)
    if a.json:
        open(a.json, "w", encoding="utf-8").write(texto + "\n")
        print(f"escrito: {a.json}")
    else:
        print(texto)


if __name__ == "__main__":
    main()
