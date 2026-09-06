#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA38-L5 · civico.protesta.agravio_urbano (R7.4) — multi-ola LAPOP.

Implementa S5-L5-spec-v1_0.md §1-§5 (forense/prereg-caja/). Lista cerrada de
olas: 2004, 2006, 2019 (2021/2023 no traen variable de protesta, excluidas
del falsador por la propia spec §1).

Diseno muestral por ola (resuelto por el censo A.4 de este acto, ya
commiteado; ver data/l4-l5-l18-censo-v1_0.json):
  2004: estrato mestrat, conglomerado msec, SIN PONDERAR (wt vacia, 0/1556).
  2006: estrato ESTRATOPRI, conglomerado UPM, SIN PONDERAR (wt/WT ausentes).
  2019: estrato estratopri, conglomerado upm, wt=1 constante (verificado).

No se usa `_filas` de tools/medidor_clientelismo_lapop.py (esa funcion hace
`float(df[peso])`, y 2004/2006 no tienen columna de peso utilizable — se
rompe en 2006, NO-ENCONTRADO, y en 2004 la columna existe pero esta vacia).
Este modulo arma sus propias tuplas `(estrato, upm, peso, y)` en `_armar()`,
con `peso=1.0` constante para 2004/2006 y `peso=wt` (verificado =1 constante)
para 2019 — misma forma de tupla que `prop_bootstrap`/`diff_bootstrap`
(reusadas tal cual, vía `_celda`/`_dif` de la casa) esperan.

Uso:
    python3 tools/medidor_l5_protesta_multiola.py --mide --json data/l5-protesta-multiola-v1_0.json
"""
import argparse, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from censo_lote_lapop import carga, resuelve  # noqa: E402
from medidor_clientelismo_lapop import (  # noqa: E402
    sha_manifiesto, _cod, _celda, _dif, MIN_NUMERADOR, REPLICAS, SEED,
)

SPEC = "forense/prereg-caja/S5-L5-spec-v1_0.md"

# spec §0.5 / caja — guardia de lectura 2019 heredada de L9 §0.5
GUARDIA_2019 = {"filas": 1580, "prot3_val": 1576, "prot3_si": 112}


def _guardia(nombre, obtenido, esperado):
    if obtenido != esperado:
        raise SystemExit(f"PARO (guardia de lectura): {nombre} = {obtenido}, "
                         f"esperado {esperado}. El lector no leyo lo que la spec/caja congelo.")
    return True


# ─────────────────────────── dicotomizaciones (§3) ───────────────────────

def _agravio_una_var(v, col):
    """2004/2006: AGRAVIO = 1 si vic1/VIC1==1, 0 si ==2, missing en cualquier
    otro codigo (3=NS/NC en 2004, 8=NS en 2006 — no son 'no', son no-respuesta,
    asi que no cuentan como AGRAVIO=0)."""
    c = v[col]
    if c == 1:
        return 1
    if c == 2:
        return 0
    return None


def _agravio_2019(v):
    """vic1ext==1 o vicbar4a==1 => 1. AGRAVIO=0 solo si AMBAS aplicables dicen
    'no' (vic1ext==2 y vicbar4a==0). Si una falta y la otra no es '1', queda
    sin determinar (None) — no se puede afirmar 'todas las aplicables son no'
    cuando una de las dos no respondio. Decision de caja, no fijada por la
    spec verbatim; ver desviaciones."""
    a, b = v.get("vic1ext"), v.get("vicbar4a")
    if a == 1 or b == 1:
        return 1
    if a == 2 and b == 0:
        return 0
    return None


def _falla_baja(v, col):
    """aoj12/AOJ12: BAJA (1) si en {3,4} (Poco/Nada); ALTA (0) si en {1,2}
    (Mucho/Algo); missing en otro codigo (8=NS, o 'a'/'b'/'c' ya filtrados
    por _cod)."""
    c = v[col]
    if c in (3, 4):
        return 1
    if c in (1, 2):
        return 0
    return None


def _red_previa_dos_var(v, c6, c9):
    """2004/2006: 1 si cp6/CP6 o cp9/CP9 in {1,2,3} (cualquier frecuencia
    distinta de 'nunca'); 0 solo si AMBAS valen 4 (nunca). Missing si alguna
    no es {1,2,3,4} (8=NS) y la otra tampoco confirma el 1."""
    a, b = v.get(c6), v.get(c9)
    if a in (1, 2, 3) or b in (1, 2, 3):
        return 1
    if a == 4 and b == 4:
        return 0
    return None


def _red_previa_una_var(v, c6):
    """2019: solo cp6 (cp9/lapop-e8 ausentes) — cobertura parcial, declarada."""
    a = v.get(c6)
    if a in (1, 2, 3):
        return 1
    if a == 4:
        return 0
    return None


def _urbano(v, col):
    c = v[col]
    if c in (1, 2, 3, 4):
        return 1
    if c == 5:
        return 0
    return None


def _protesta_frecuencia(v, col):
    """prot1/PROT1 (2004/2006): recodificacion pre-registrada §1.2 —
    1 (algunas veces) => 1; 2 (casi nunca) + 3 (nunca) => 0."""
    c = v[col]
    if c == 1:
        return 1
    if c in (2, 3):
        return 0
    return None


def _protesta_2019(v):
    c = v["prot3"]
    if c == 1:
        return 1
    if c == 2:
        return 0
    return None


# ───────────────────────── construccion por ola ──────────────────────────

def _indicadores(df, ola):
    """Devuelve un dict de listas paralelas (longitud n) con los indicadores
    codificados (0/1/None) y las claves de diseno (estrato/upm como int o
    None), listas para armar filas ad hoc por celda."""
    n = len(df)
    r = resuelve

    if ola == "2004":
        c_vic1, c_aoj12, c_cp6, c_cp9 = r(df, "vic1"), r(df, "aoj12"), r(df, "cp6"), r(df, "cp9")
        c_tam, c_prot1 = r(df, "tamano"), r(df, "prot1")
        c_est, c_upm = r(df, "mestrat"), r(df, "msec")
        c_mzona = r(df, "mzona")
        c_e8 = r(df, "e8")
        out = {"est": [], "upm": [], "agravio": [], "falla_baja": [],
               "red_previa": [], "urbano": [], "ur_alt": [], "protesta": [],
               "e8": []}
        for i in range(n):
            v = {"vic1": _cod(df[c_vic1].iloc[i]), "aoj12": _cod(df[c_aoj12].iloc[i]),
                 "cp6": _cod(df[c_cp6].iloc[i]), "cp9": _cod(df[c_cp9].iloc[i]),
                 "tamano": _cod(df[c_tam].iloc[i]), "prot1": _cod(df[c_prot1].iloc[i])}
            out["est"].append(int(df[c_est].iloc[i]))
            out["upm"].append(int(df[c_upm].iloc[i]))
            out["agravio"].append(_agravio_una_var(v, "vic1"))
            out["falla_baja"].append(_falla_baja(v, "aoj12"))
            out["red_previa"].append(_red_previa_dos_var(v, "cp6", "cp9"))
            out["urbano"].append(_urbano(v, "tamano"))
            out["ur_alt"].append(_cod(df[c_mzona].iloc[i]))  # mzona: 1=Urbana,2=Rural — analogo de ur
            out["protesta"].append(_protesta_frecuencia(v, "prot1"))
            out["e8"].append(_cod(df[c_e8].iloc[i]))
        return out

    if ola == "2006":
        c_vic1, c_aoj12, c_cp6, c_cp9 = r(df, "VIC1"), r(df, "AOJ12"), r(df, "CP6"), r(df, "CP9")
        c_tam, c_prot1, c_prot2 = r(df, "TAMANO"), r(df, "PROT1"), r(df, "PROT2")
        c_est, c_upm = r(df, "ESTRATOPRI"), r(df, "UPM")
        c_ur = r(df, "UR")
        c_e8 = r(df, "E8")
        out = {"est": [], "upm": [], "agravio": [], "falla_baja": [],
               "red_previa": [], "urbano": [], "ur_alt": [], "protesta": [],
               "prot1_cod": [], "prot2": [], "e8": []}
        for i in range(n):
            v = {"VIC1": _cod(df[c_vic1].iloc[i]), "AOJ12": _cod(df[c_aoj12].iloc[i]),
                 "CP6": _cod(df[c_cp6].iloc[i]), "CP9": _cod(df[c_cp9].iloc[i]),
                 "TAMANO": _cod(df[c_tam].iloc[i]), "PROT1": _cod(df[c_prot1].iloc[i])}
            out["est"].append(int(df[c_est].iloc[i]))
            out["upm"].append(int(df[c_upm].iloc[i]))
            out["agravio"].append(_agravio_una_var(v, "VIC1"))
            out["falla_baja"].append(_falla_baja(v, "AOJ12"))
            out["red_previa"].append(_red_previa_dos_var(v, "CP6", "CP9"))
            out["urbano"].append(_urbano(v, "TAMANO"))
            out["ur_alt"].append(_cod(df[c_ur].iloc[i]))
            out["protesta"].append(_protesta_frecuencia(v, "PROT1"))
            out["prot1_cod"].append(v["PROT1"])
            out["prot2"].append(_protesta_frecuencia({"PROT1": _cod(df[c_prot2].iloc[i])}, "PROT1"))
            out["e8"].append(_cod(df[c_e8].iloc[i]))
        return out

    if ola == "2019":
        c_v1, c_vb = r(df, "vic1ext"), r(df, "vicbar4a")
        c_aoj12, c_cp6 = r(df, "aoj12"), r(df, "cp6")
        c_tam, c_prot3 = r(df, "tamano"), r(df, "prot3")
        c_est, c_upm, c_wt = r(df, "estratopri"), r(df, "upm"), r(df, "wt")
        c_ur = r(df, "ur")
        out = {"est": [], "upm": [], "peso": [], "agravio": [], "agravio_vicbar4a": [],
               "falla_baja": [], "red_previa": [], "urbano": [], "ur_alt": [],
               "protesta": []}
        for i in range(n):
            v = {"vic1ext": _cod(df[c_v1].iloc[i]), "vicbar4a": _cod(df[c_vb].iloc[i]),
                 "aoj12": _cod(df[c_aoj12].iloc[i]), "cp6": _cod(df[c_cp6].iloc[i]),
                 "tamano": _cod(df[c_tam].iloc[i]), "prot3": _cod(df[c_prot3].iloc[i])}
            out["est"].append(int(df[c_est].iloc[i]))
            out["upm"].append(int(df[c_upm].iloc[i]))
            out["peso"].append(float(df[c_wt].iloc[i]))
            out["agravio"].append(_agravio_2019(v))
            out["agravio_vicbar4a"].append(v["vicbar4a"])
            out["falla_baja"].append(_falla_baja(v, "aoj12"))
            out["red_previa"].append(_red_previa_una_var(v, "cp6"))
            out["urbano"].append(_urbano(v, "tamano"))
            out["ur_alt"].append(_cod(df[c_ur].iloc[i]))
            out["protesta"].append(_protesta_2019(v))
        return out

    raise ValueError(ola)


def _armar(ind, mask_idx, ola, use_peso=False):
    """filas (est, upm, peso, y) para los indices en mask_idx, y=protesta."""
    out = []
    for i in mask_idx:
        y = ind["protesta"][i]
        if y is None:
            continue
        peso = ind["peso"][i] if use_peso else 1.0
        out.append((ind["est"][i], ind["upm"][i], peso, y))
    return out


def _celda_contraste_urbano(ind, filtro_fn, etiqueta, ola, use_peso=False):
    """Construye la celda urbana y rural bajo un filtro dado (funcion sobre i)
    y devuelve (c_urb, c_rur, delta) via _celda/_dif de la casa."""
    n = len(ind["urbano"])
    idx_urb = [i for i in range(n) if ind["urbano"][i] == 1 and filtro_fn(i)]
    idx_rur = [i for i in range(n) if ind["urbano"][i] == 0 and filtro_fn(i)]
    f_urb = _armar(ind, idx_urb, ola, use_peso)
    f_rur = _armar(ind, idx_rur, ola, use_peso)
    c_urb = _celda(f_urb, f"{etiqueta} | urbano ({ola})")
    c_rur = _celda(f_rur, f"{etiqueta} | rural ({ola})")
    d = _dif(f_urb, f_rur, f"{etiqueta} ({ola})", c_urb, c_rur)
    return {"urbano": c_urb, "rural": c_rur, "delta": d}


def _resumen_e8(vals, etiqueta):
    cods = [c for c in vals if c is not None and c <= 10]  # 88=NS ya excluido por rango
    n = len(cods)
    if n == 0:
        return {"etiqueta": etiqueta, "n": 0, "media": None}
    return {"etiqueta": etiqueta, "n": n, "media": sum(cods) / n,
            "min": min(cods), "max": max(cods),
            "nota": "escala 1(desaprueba firmemente)-10(aprueba firmemente); "
                    "disposicion normativa a que OTROS participen, no asistencia "
                    "propia (§0.4) — NO entra a RED_PREVIA ni a ninguna celda del falsador"}


def _pieza_ola(ola, df, sha, sha_man, coincide, use_peso=False):
    ind = _indicadores(df, ola)
    n = len(df)
    res = {"ola": ola, "n_filas": n, "sha256": sha, "sha256_manifiesto": sha_man,
           "coincide_manifiesto": coincide, "ponderado": use_peso}

    # ── C_completo: dentro de AGRAVIO=1 & FALLA_BAJA=1 & RED_PREVIA=1 ──
    def filtro_completo(i):
        return (ind["agravio"][i] == 1 and ind["falla_baja"][i] == 1
                and ind["red_previa"][i] == 1)
    res["C_completo"] = _celda_contraste_urbano(
        ind, filtro_completo, "C_completo (agravio∧falla_baja∧red_previa)", ola, use_peso)

    # ── diagnosticas: un solo antecedente ──
    res["C_agravio"] = _celda_contraste_urbano(
        ind, lambda i: ind["agravio"][i] == 1, "C_agravio (agravio=1)", ola, use_peso)
    res["C_falla"] = _celda_contraste_urbano(
        ind, lambda i: ind["falla_baja"][i] == 1, "C_falla (falla_baja)", ola, use_peso)
    res["C_red"] = _celda_contraste_urbano(
        ind, lambda i: ind["red_previa"][i] == 1, "C_red (red_previa=1)", ola, use_peso)

    # ── marginales de los cuatro antecedentes + protesta, para verificacion ──
    def marg(nombre):
        vals = ind[nombre]
        m = {}
        for v in vals:
            if v is not None:
                m[v] = m.get(v, 0) + 1
        return {"n_validos": sum(m.values()), "marginal": {str(k): v for k, v in sorted(m.items())}}
    res["marginales"] = {k: marg(k) for k in ("agravio", "falla_baja", "red_previa", "urbano", "protesta")}

    # ── verificacion cruzada URBANO vs ur/mzona (en paralelo, no sustituye) ──
    ur_alt = ind.get("ur_alt")
    if ur_alt is not None and any(v is not None for v in ur_alt):
        coincide_n = sum(1 for i in range(n)
                         if ind["urbano"][i] is not None and ur_alt[i] is not None)
        iguales = sum(1 for i in range(n)
                      if ind["urbano"][i] is not None and ur_alt[i] is not None
                      and ((ind["urbano"][i] == 1 and ur_alt[i] == 1)
                           or (ind["urbano"][i] == 0 and ur_alt[i] == 2)))
        nombre_alt = "mzona (Tipo de localidad, 1=Urbana/2=Rural y mixto)" if ola == "2004" \
            else ("UR" if ola == "2006" else "ur")
        res["urbano_verificacion_cruzada"] = {
            "variable": nombre_alt, "n_comparable": coincide_n,
            "coinciden_con_tamano": iguales,
            "pct_coincide": (iguales / coincide_n) if coincide_n else None}

    # ── 2019: sub-eje vicbar4a (agravio familiar) por separado ──
    if ola == "2019":
        av = ind["agravio_vicbar4a"]
        m = {}
        for v in av:
            if v is not None:
                m[v] = m.get(v, 0) + 1
        res["agravio_vicbar4a_marginal"] = {"n_validos": sum(m.values()),
                                            "marginal": {str(k): v for k, v in sorted(m.items())}}

    # ── LAPOP-E8, eje secundario (2004/2006 solamente) — nunca al falsador ──
    if "e8" in ind:
        res["lapop_e8"] = _resumen_e8(ind["e8"], f"e8 ({ola})")

    # ── 2006: PROT2, pieza separada, gateada por PROT1 en {1,2} ──
    if ola == "2006":
        n_prot1_elegible = sum(1 for c in ind["prot1_cod"] if c in (1, 2))
        idx_gate = [i for i in range(n) if ind["prot1_cod"][i] in (1, 2)]
        f_prot2 = []
        for i in idx_gate:
            y = ind["prot2"][i]
            if y is None:
                continue
            f_prot2.append((ind["est"][i], ind["upm"][i], 1.0, y))
        # PROT2 como pieza global (sin cruzar por entorno: la spec la separa,
        # no exige su propio C_completo) — se reporta su tasa simple y n.
        c_prot2 = _celda(f_prot2, "PROT2 (subuniverso PROT1∈{1,2})")
        res["PROT2_pieza_separada"] = {
            "n_elegibles_prot1": n_prot1_elegible,
            "n_validos_prot2": len(f_prot2),
            "celda": c_prot2,
            "reserva": ("universo ANIDADO en el desenlace: PROT1∈{1,2} ya es "
                       "'alguna vez protesto' (algunas veces o casi nunca); sobre "
                       "ese subuniverso PROT2 no pregunta 'quien protesta' sino "
                       "'quien de los que alguna vez protestaron lo hizo el ultimo "
                       "ano'. No se cruza contra AGRAVIO/FALLA/RED/URBANO — la "
                       "spec la declara pieza separada, no otra celda del "
                       "falsador (S5 §1.2 / §3.1).")}

    return res


# ─────────────────────────────── veredicto §4 ─────────────────────────────

def _signo_positivo_limpio(delta):
    d = delta.get("delta", {})
    return d.get("estado") == "ESTIMADA" and d.get("excluye_cero") and d["d"] > 0


def _signo_negativo_limpio(delta):
    d = delta.get("delta", {})
    return d.get("estado") == "ESTIMADA" and d.get("excluye_cero") and d["d"] < 0


def _veredicto(piezas):
    """spec §4 — el veredicto sale de C_completo por ola; si las tres olas dan
    C_completo NO-ESTIMABLE, sale de las tres diagnosticas tomadas juntas."""
    veredicto_por_ola = {}
    for p in piezas:
        d = p["C_completo"]["delta"]
        if d.get("estado") != "ESTIMADA":
            veredicto_por_ola[p["ola"]] = {"estado": "NO-ESTIMABLE", "motivo": d.get("motivo")}
        elif d["excluye_cero"] and d["d"] > 0:
            veredicto_por_ola[p["ola"]] = {"estado": "CORROBORADA", "d": d["d"], "ic95": d["ic95"]}
        elif d["excluye_cero"] and d["d"] < 0:
            veredicto_por_ola[p["ola"]] = {"estado": "CONTRARIA", "d": d["d"], "ic95": d["ic95"]}
        else:
            veredicto_por_ola[p["ola"]] = {"estado": "NO-DISCRIMINA", "d": d["d"], "ic95": d["ic95"]}

    alguna_estimable = any(v["estado"] != "NO-ESTIMABLE" for v in veredicto_por_ola.values())

    if alguna_estimable:
        # Alguna ola SI estimo C_completo: el veredicto principal sale de esa(s).
        estados = [v["estado"] for v in veredicto_por_ola.values() if v["estado"] != "NO-ESTIMABLE"]
        if "CONTRARIA" in estados:
            veredicto = "CONTRARIA"
        elif all(e == "CORROBORADA" for e in estados):
            veredicto = "CORROBORADA"
        else:
            veredicto = "NO-DISCRIMINA"
        return {
            "veredicto": veredicto,
            "base": "C_completo (§4) — al menos una ola lo estimo",
            "por_ola": veredicto_por_ola,
        }

    # Las tres olas cayeron por guardia en C_completo — anticipado por §3.1.
    # El veredicto sale de las tres diagnosticas juntas (§4 fila NO-ESTIMABLE).
    diag_por_ola = {}
    for p in piezas:
        diag_por_ola[p["ola"]] = {
            "C_agravio": "limpio+" if _signo_positivo_limpio(p["C_agravio"]) else
                         ("limpio-" if _signo_negativo_limpio(p["C_agravio"]) else "no-discrimina/no-estimable"),
            "C_falla": "limpio+" if _signo_positivo_limpio(p["C_falla"]) else
                       ("limpio-" if _signo_negativo_limpio(p["C_falla"]) else "no-discrimina/no-estimable"),
            "C_red": "limpio+" if _signo_positivo_limpio(p["C_red"]) else
                     ("limpio-" if _signo_negativo_limpio(p["C_red"]) else "no-discrimina/no-estimable"),
        }
    todas = [p[k] for p in piezas for k in ("C_agravio", "C_falla", "C_red")]
    algun_negativo_limpio = any(_signo_negativo_limpio(d) for d in todas)
    todas_positivas_limpias = all(_signo_positivo_limpio(d) for d in todas)

    if algun_negativo_limpio:
        veredicto = "CONTRARIA (sobre la diagnostica especifica que dio signo negativo limpio; ver detalle por ola)"
    elif todas_positivas_limpias:
        veredicto = "CORROBORADA-DEL-PATRON-POR-PARTES (nunca de C_completo; §4 precedencia)"
    else:
        veredicto = "NO-DISCRIMINA (las diagnosticas no van todas limpias en el mismo signo)"

    return {
        "veredicto": veredicto,
        "base": ("C_completo NO-ESTIMABLE en las tres olas (anticipado por §3.1) — el "
                "corazon de la regla de cuatro factores, que los tres antecedentes "
                "juntos y no por separado son los que el entorno urbano canaliza, "
                "NO SE MIDIO (§4)"),
        "por_ola_C_completo": veredicto_por_ola,
        "diagnosticas_por_ola": diag_por_ola,
    }


# ────────────────────────────────── mide ──────────────────────────────────

def mide(ruta_json=None):
    df04, m04, p04, s04, pid04 = carga("2004_dta")
    df06, m06, p06, s06, pid06 = carga("2006_dta")
    df19, m19, p19, s19, pid19 = carga("2019")

    _guardia("2019 filas", len(df19), GUARDIA_2019["filas"])
    c_prot3 = resuelve(df19, "prot3")
    _guardia("2019 prot3 validos", sum(1 for v in df19[c_prot3] if _cod(v) is not None),
             GUARDIA_2019["prot3_val"])
    _guardia("2019 prot3 si", sum(1 for v in df19[c_prot3] if _cod(v) == 1),
             GUARDIA_2019["prot3_si"])
    print("guardia de lectura 2019 (heredada de L9 §0.5 / spec §2): OK\n")

    pz04 = _pieza_ola("2004", df04, s04, sha_manifiesto(pid04), s04 == sha_manifiesto(pid04), use_peso=False)
    pz06 = _pieza_ola("2006", df06, s06, sha_manifiesto(pid06), s06 == sha_manifiesto(pid06), use_peso=False)
    pz19 = _pieza_ola("2019", df19, s19, sha_manifiesto(pid19), s19 == sha_manifiesto(pid19), use_peso=True)
    piezas = [pz04, pz06, pz19]

    veredicto = _veredicto(piezas)

    out = {
        "acto": "MAESTRA38-L5 · civico.protesta.agravio_urbano (R7.4)",
        "spec": SPEC,
        "spec_sha256": "74816097008b84a14a04d83dbcce850f0bb3644ae34bfe0867ab5d928ded1eb6",
        "estimador": (f"proporcion ponderada; IC95 bootstrap de conglomerado, {REPLICAS} "
                     f"replicas, seed {SEED}, remuestreo de UPM dentro de estrato "
                     f"(reusa prop_bootstrap/diff_bootstrap de tools/medidor_clientelismo_lapop.py)"),
        "diseno_por_ola": {
            "2004": {"estrato": "mestrat", "upm": "msec", "ponderador": "NINGUNO (wt vacia, 0/1556)"},
            "2006": {"estrato": "ESTRATOPRI", "upm": "UPM", "ponderador": "NINGUNO (wt/WT NO-ENCONTRADO)"},
            "2019": {"estrato": "estratopri", "upm": "upm", "ponderador": "wt (=1 constante, verificado)"},
        },
        "guardia_2019": GUARDIA_2019,
        "min_numerador": MIN_NUMERADOR,
        "piezas": {"2004": pz04, "2006": pz06, "2019": pz19},
        "veredicto_falsador_Bbis": veredicto,
        "notas_spec": {
            "C_agravio_NO_es_la_replicacion_que_la_spec_anuncia": (
                "CORRECCION (post-verificacion adversarial del propio acto). spec §3.1 anuncia "
                "C_agravio como 'replicacion de tercera ola' del diseno ya corroborado por "
                "L9 §4 (+5.60pp [+2.32,+8.96]) y L11 §2 (+3.72pp [+2.22,+5.22], Enmienda D2-d, "
                "CARGADA-A-MOTOR, tier FUERTE). NO LO ES. Aquellas dos cifras son el diseno C2 "
                "de L9 (agravio varia, entorno fijo en urbano). Lo que §3.1 define literalmente "
                "-- 'una por antecedente, 2x2 cada una, CONTRA URBANO' -- y lo que este medidor "
                "calcula es fijar AGRAVIO=1 y contrastar urbano vs rural: eso es estructuralmente "
                "el C1 de L9, el que ALLI cayo por guardia (rural-victima n=65, num=7). Y aqui "
                "vuelve a caer, en las tres olas (num rural 5, 4, 2). La replicacion anunciada NO "
                "OCURRIO -- no por omision, sino porque la unica forma de C_agravio que la spec "
                "pre-registra es la que no se puede estimar. La forma C2 NO se computo: §0.3 la "
                "excluye explicitamente, y anadir una celda que la spec no pre-registro es tan "
                "defecto como omitir una que si. Tension interna de la spec sellada (§3.1 contra "
                "§0.3), declarada y no resuelta a mano por el ejecutor: FP-315. Las cifras "
                "+5.60/+3.72 siguen siendo citas correctas de D2-d; lo que estaba mal era "
                "atribuirlas a lo que esta pieza calculo. NO se reabre D2-d ni la fila D de "
                "R7.4 (ADR-158)."),
            "lo_nuevo": "C_falla y C_red (antecedentes que L9 no tenia) y el intento de C_completo.",
            "e8_excluido": "LAPOP-E8 (2004/2006) es aprobacion normativa de que OTROS "
                "participen, no asistencia propia (§0.4) — reportado aparte, fuera de "
                "RED_PREVIA y de toda celda del falsador.",
        },
    }
    if ruta_json:
        json.dump(out, open(ruta_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("escrito", ruta_json)
    _imprime(out)
    return out


def _fmt(c):
    if not c or c.get("estado") != "ESTIMADA":
        return f"NO-ESTIMABLE ({(c or {}).get('motivo')})"
    if "p" in c:
        return (f"p={c['p']:.6f}  IC95=[{c['ic95'][0]:.6f},{c['ic95'][1]:.6f}]  "
                f"n={c['n']} num={c['numerador']}")
    return (f"d={c['d']:+.6f}  IC95=[{c['ic95'][0]:+.6f},{c['ic95'][1]:+.6f}]  "
            f"{'EXCLUYE 0' if c['excluye_cero'] else 'contiene 0'}")


def _imprime(out):
    for ola, pz in out["piezas"].items():
        print(f"\n{'=' * 78}\nOLA {ola} · n={pz['n_filas']} · ponderado={pz['ponderado']} · "
              f"sha256 coincide_manifiesto={pz['coincide_manifiesto']}")
        for clave in ("C_completo", "C_agravio", "C_falla", "C_red"):
            blk = pz[clave]
            print(f"  {clave}")
            print(f"    urbano  {_fmt(blk['urbano'])}")
            print(f"    rural   {_fmt(blk['rural'])}")
            print(f"    delta   {_fmt(blk['delta'])}")
        if "urbano_verificacion_cruzada" in pz:
            vc = pz["urbano_verificacion_cruzada"]
            print(f"  verificacion cruzada urbano vs {vc['variable']}: "
                  f"{vc['coinciden_con_tamano']}/{vc['n_comparable']} coinciden "
                  f"({vc['pct_coincide']:.2%})" if vc['pct_coincide'] is not None else "  verificacion cruzada: sin datos")
        if "lapop_e8" in pz:
            e = pz["lapop_e8"]
            print(f"  LAPOP-E8 (eje secundario, fuera del falsador): n={e['n']} media={e.get('media')}")
        if "PROT2_pieza_separada" in pz:
            p2 = pz["PROT2_pieza_separada"]
            print(f"  PROT2 (pieza separada, gateada PROT1∈{{1,2}}): "
                  f"elegibles={p2['n_elegibles_prot1']} validos={p2['n_validos_prot2']} "
                  f"{_fmt(p2['celda'])}")
    print(f"\n{'=' * 78}\nVEREDICTO Bbis: {out['veredicto_falsador_Bbis']['veredicto']}")
    print(f"  base: {out['veredicto_falsador_Bbis']['base']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mide", action="store_true")
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.mide:
        mide(a.json)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
