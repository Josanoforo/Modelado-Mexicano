#!/usr/bin/env python3
"""ACTO MAESTRA36-L12 · MPS-2012-CROSSTABS — medidor de las piezas P0..P4.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada-bis-v3.md` (COMMIT-1-bis),
que manda sobre la spec de COMMIT-1: el encargo v3 sustituye integras v1 y v2.

INSTRUMENTO DE SEGUNDA MANO: salida del tabulador en linea "Explore Data" de
ICPSR 35024, NO el microdato (35024-0001-Data.dta exige membresia -> A.4
NO-ACCESIBLE). Conteos SIN PONDERAR, sin estrato ni UPM, ola panel (ronda 2,
n~1555). Clase de procedencia (3) reportada, marca SIN-FETCH (A.6).
Tier maximo alcanzable MEDIA con reserva. NINGUNA celda entra al motor.

Entradas (raiz `descargas_mx`, sha256 verificado contra data/manifiesto.yaml):
  icpsr35024_DS1_W2_crosstabs_derivado_v0.csv  -> T1 T2 T3 T4
  icpsr35024-ds1-w2-crosstabs-derivadas.csv    -> T5 T6 T7a T7b T8 T9a
  export_crudo.txt / LEEME-procedencia.txt / LEEME 2-procedencia.txt
Salida: data/l12-mps2012-v1_0.json
"""
import csv
import hashlib
import json
import math
import os
import sys

# ---------------------------------------------------------------- payloads
# sha256 declarados en data/manifiesto.yaml (origin/main, ADR-310, A1 P2).
PAYLOADS = {
    "icpsr35024_ds1_w2_crosstabs_derivado_v0": (
        "icpsr35024_DS1_W2_crosstabs_derivado_v0.csv",
        "96330f0353dd173cd7dec5ff9c351d8504085bf38a6dbee3df9242b8271ebb6d"),
    "icpsr35024_ds1_w2_crosstabs_derivadas": (
        "icpsr35024-ds1-w2-crosstabs-derivadas.csv",
        "a85c59aea0e9a586e1555a51f63e27d2252fb13c611297a803e71d6b499e8379"),
    "export_crudo": (
        "export_crudo.txt",
        "daa29e0b8830ac854572631501d72e31cb52c6eaca074355d700e9ae88ff053d"),
    "leeme_procedencia": (
        "LEEME-procedencia.txt",
        "c98ce68bda7cf5866848231bd33097e71e5f6641f8d153b42f4bdbd42231297a"),
    "leeme_2_procedencia": (
        "LEEME 2-procedencia.txt",
        "9f0a7da9d591a84c92ad799c875c9d4e7461cb33f695436c0d7d798764e75d20"),
}

# spec Sec.1: marginales del codebook citados por LEEME-procedencia.txt
MARGINALES_CODEBOOK = {"W2_P41=1": 63, "W2_P7=1": 971, "W2_P40=1": 60}

# spec bis Sec.C: codigos de P8/W2_P8 que cuentan como voto por partido.
# 08 (mas de una casilla de DIFERENTE partido) no es atribuible; 11 anulo;
# 12 blanco; 13 no voto. Los nueve restantes son partidarios.
CODIGOS_PARTIDARIOS = {"01", "02", "03", "04", "05", "06", "07", "09", "10"}

# Desenlace SECUNDARIO (spec de COMMIT-1, YA VISTO): mapeo a partido/coalicion.
PARTIDO = {"01": "PAN",
           "02": "PRI", "04": "PRI", "09": "PRI",
           "03": "AMLO", "05": "AMLO", "06": "AMLO", "10": "AMLO",
           "07": "QUADRI"}

Z = 1.959963984540054  # normal 97.5

# ---------------------------------------------------------------- estadistica
def wilson(k, n):
    """IC95 de una proporcion por score de Wilson. Devuelve (p, lo, hi)."""
    if n == 0:
        return (None, None, None)
    p = k / n
    d = 1 + Z * Z / n
    centro = (p + Z * Z / (2 * n)) / d
    semi = (Z / d) * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n))
    return (p, centro - semi, centro + semi)


def wald(k1, n1, k0, n0):
    """IC95 normal de la diferencia p1-p0 sobre conteos crudos (spec bis Sec.D)."""
    if n1 == 0 or n0 == 0:
        return (None, None, None, None)
    p1, p0 = k1 / n1, k0 / n0
    ee = math.sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)
    d = p1 - p0
    return (d, d - Z * ee, d + Z * ee, Z * ee)


def media_y_var(dist):
    """Media y varianza muestral (n-1) de una distribucion {valor: conteo}."""
    n = sum(dist.values())
    if n < 2:
        return (None, None, n)
    m = sum(v * c for v, c in dist.items()) / n
    ss = sum(c * (v - m) ** 2 for v, c in dist.items())
    return (m, ss / (n - 1), n)


# ---------------------------------------------------------------- E/S
def sha256(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as fh:
        for blq in iter(lambda: fh.read(1 << 20), b""):
            h.update(blq)
    return h.hexdigest()


def raiz_descargas(repo):
    """Lee data/raices.local.yaml sin dependencias: solo la clave descargas_mx."""
    with open(os.path.join(repo, "data", "raices.local.yaml"), encoding="utf-8") as fh:
        for linea in fh:
            if linea.startswith("descargas_mx:"):
                return linea.split(":", 1)[1].strip()
    raise SystemExit("PARO: data/raices.local.yaml no declara descargas_mx")


def lee_csv(ruta):
    # El modulo csv despoja comillas y corrompe TSV ajenos en este repo, pero
    # aqui la fuente ES csv con comillas propias (las etiquetas traen comas).
    with open(ruta, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- P0
def p0_censo(rutas, v0, der):
    """Censo, estampa y cuadre de los tres marginales de control."""
    est = {p: {"archivo": os.path.basename(rutas[p]),
               "sha256": sha256(rutas[p]),
               "sha256_manifiesto": PAYLOADS[p][1]} for p in PAYLOADS}
    for p, d in est.items():
        d["coincide"] = (d["sha256"] == d["sha256_manifiesto"])
    if not all(d["coincide"] for d in est.values()):
        return {"estado": "PARO", "motivo": "sha256 no coincide con manifiesto",
                "payloads": est}

    # T1: ofrecieron=1, sumado sobre los cuatro estratos de W2_P36C.
    t1_ofr = sum(int(r["n_sin_ponderar"]) for r in v0
                 if r["tabla"] == "T1" and r["fila"] == "ofrecieron=1")
    # T4: condicionaron=1, total_fila sobre los cuatro estratos.
    t4_cond = sum(int(r["n_sin_ponderar"]) for r in v0
                  if r["tabla"] == "T4" and r["fila"] == "condicionaron=1"
                  and r["columna"] == "total_fila")
    # T8: N total (solo contiene a quien declaro haber votado -> W2_P7=1).
    t8_n = sum(int(r["n"]) for r in der if r["tabla"] == "T8")

    cuadre = {}
    for clave, sub, estratificado in (("W2_P41=1", t1_ofr, True),
                                      ("W2_P40=1", t4_cond, True),
                                      ("W2_P7=1", t8_n, False)):
        marg = MARGINALES_CODEBOOK[clave]
        if estratificado:
            ok = sub <= marg          # el hueco son los casos sin W2_P36C
            veredicto = "CUADRA" if ok else "EXCEDE-EL-MARGINAL"
        else:
            ok = sub == marg          # T8 no esta estratificado: sin hueco
            veredicto = "CUADRA-EXACTO" if ok else "DISCORDA"
        cuadre[clave] = {"marginal_codebook": marg, "reconstruido": sub,
                         "estratificado_por_W2_P36C": estratificado,
                         "casos_sin_control": (marg - sub) if estratificado else 0,
                         "ok": ok, "veredicto": veredicto}

    tablas_v0, tablas_der = {}, {}
    for r in v0:
        tablas_v0[r["tabla"]] = tablas_v0.get(r["tabla"], 0) + 1
    for r in der:
        tablas_der[r["tabla"]] = tablas_der.get(r["tabla"], 0) + 1

    return {
        "estado": "OK" if all(c["ok"] for c in cuadre.values()) else "PARO",
        "payloads": est,
        "censo_celdas": {"derivado_v0": tablas_v0, "derivadas": tablas_der,
                         "total_derivadas": sum(tablas_der.values())},
        "cuadre_marginales": cuadre,
        "estampa": {
            "instrumento": "SEGUNDA MANO (tabulador en linea 'Explore Data' de ICPSR)",
            "ponderador": "NINGUNO -- conteos sin ponderar; sin estrato ni UPM",
            "universo": "ola panel ronda 2 (julio 2012), n~1555",
            "microdato": "35024-0001-Data.dta NO-ACCESIBLE (membresia institucional, A.4)",
            "clase_procedencia": "(3) reportada",
            "marca": "SIN-FETCH (A.6)",
            "tier_maximo_alcanzable": "MEDIA con reserva",
            "entra_al_motor": False,
        },
        "discordancias_A1_resueltas": {
            "1_LEEME2_declara_solo_T6": {
                "declarado": "Tabla T6 ... 257 celdas",
                "medido": f"{sum(tablas_der.values())} celdas en {len(tablas_der)} tablas",
                "resolucion": ("NO es contradiccion: las Adendas 1-3 del propio archivo "
                               "declaran T7a/T7b/T8/T9a/T5 y marcan el texto original "
                               "VENCIDO EN ALCANCE. Re-sello por crecimiento de universo."),
            },
            "2_nombres_de_archivo_inexistentes": {
                "declarado": "export_crudo_mesa_2026-09-02.txt y T5_lista_W2.txt",
                "medido": "export_crudo.txt; T5 derivado dentro del CSV de derivadas",
                "resolucion": ("El contenido se identifica por sha256 e identidad, no por "
                               "rotulo. Los cinco payloads coinciden con el manifiesto."),
            },
        },
    }


# ---------------------------------------------------------------- P1
def _t6_contraste(der, clave):
    """Agrega T6 por control W2_P41 bajo una funcion de 'cambio'.

    clave(row_code, col_code) -> True si cuenta como cambio. El universo son
    siempre las celdas con AMBOS codigos partidarios (spec bis Sec.C/D).
    """
    vc, fuera = {}, {"n_excluido": 0, "filas_no_partidarias": 0,
                     "cols_no_partidarias": 0}
    for r in der:
        if r["tabla"] != "T6":
            continue
        n, rc, cc = int(r["n"]), r["row_code"], r["col_code"]
        if rc not in CODIGOS_PARTIDARIOS or cc not in CODIGOS_PARTIDARIOS:
            fuera["n_excluido"] += n
            fuera["filas_no_partidarias"] += n if rc not in CODIGOS_PARTIDARIOS else 0
            fuera["cols_no_partidarias"] += n if cc not in CODIGOS_PARTIDARIOS else 0
            continue
        d = vc.setdefault(int(r["control_code"]), {"cambio": 0, "n": 0})
        d["n"] += n
        if clave(rc, cc):
            d["cambio"] += n
    return vc, fuera


def p1_r77(v0, der):
    """R7.7: turnout (T1) + vote-choice (T6), falsador B-bis, robustez T7."""
    # --- turnout, T1 agregando los cuatro estratos de W2_P36C
    tur = {}
    for r in v0:
        if r["tabla"] != "T1":
            continue
        ofr = 1 if r["fila"] == "ofrecieron=1" else 0
        d = tur.setdefault(ofr, {"voto": 0, "n": 0})
        d["n"] += int(r["n_sin_ponderar"])
        if r["columna"] == "voto=1":
            d["voto"] += int(r["n_sin_ponderar"])
    dt, lot, hit, semi_t = wald(tur[1]["voto"], tur[1]["n"],
                                tur[0]["voto"], tur[0]["n"])

    # --- vote-change PRIMARIO (v3): P8 != W2_P8 sobre el CODIGO
    vc, fuera = _t6_contraste(der, lambda rc, cc: rc != cc)
    dv, lov, hiv, semi_v = wald(vc[1]["cambio"], vc[1]["n"],
                                vc[0]["cambio"], vc[0]["n"])

    # --- vote-change SECUNDARIO (spec de COMMIT-1): mapeo a partido. YA VISTO.
    vp, _ = _t6_contraste(der, lambda rc, cc: PARTIDO[rc] != PARTIDO[cc])
    dp, lop, hip, semi_p = wald(vp[1]["cambio"], vp[1]["n"],
                                vp[0]["cambio"], vp[0]["n"])

    # --- falsador B-bis: el semiancho se evalua ANTES de mirar el signo
    umbral = 0.15
    if semi_v is None or semi_v > umbral:
        veredicto = "NO-DISCRIMINA"
        razon = (f"semiancho del IC95 (Wald) de Delta_vote-change = {semi_v:.4f} "
                 f"> {umbral} (+-15 pp). Rama de precedencia.")
    elif (lot <= 0 <= hit) and (lov <= 0 <= hiv):
        veredicto = "CORROBORADA"
        razon = "IC95 de Delta_turnout y de Delta_vote-change contienen 0."
    elif not (lov <= 0 <= hiv):
        veredicto = "CONTRARIA"
        razon = "IC95 de Delta_vote-change queda fuera de 0."
    else:
        veredicto = "NO-DISCRIMINA"
        razon = "ninguna rama del falsador se satisface limpiamente."

    def celda(k, n, campo):
        return {campo: k, "n": n, "p": wilson(k, n)}

    return {
        "regla": "R7.7", "tier_canon": "MEDIA",
        "enunciado": "dadiva + broker -> compra turnout, no vote-choice",
        "turnout_T1": {
            "ofrecidos": celda(tur[1]["voto"], tur[1]["n"], "voto"),
            "no_ofrecidos": celda(tur[0]["voto"], tur[0]["n"], "voto"),
            "delta": dt, "ic95_wald": [lot, hit], "semiancho": semi_t,
            "excluye_cero": not (lot <= 0 <= hit),
        },
        "vote_change_T6_PRIMARIO_v3": {
            "desenlace": "P8 != W2_P8 (comparacion de CODIGO), universo de codigos partidarios",
            "ofrecidos": celda(vc[1]["cambio"], vc[1]["n"], "cambio"),
            "no_ofrecidos": celda(vc[0]["cambio"], vc[0]["n"], "cambio"),
            "delta": dv, "ic95_wald": [lov, hiv], "semiancho": semi_v,
            "excluye_cero": not (lov <= 0 <= hiv),
            "excluido_por_codigo_no_partidario": fuera,
        },
        "vote_change_T6_SECUNDARIO_ya_visto": {
            "rotulo": "YA-VISTO-BAJO-SPEC-ANTERIOR",
            "desenlace": ("partido(P8) != partido(W2_P8), PAN={01} PRI={02,04,09} "
                          "AMLO={03,05,06,10} QUADRI={07} -- spec de COMMIT-1 (b6efa1f)"),
            "ofrecidos": celda(vp[1]["cambio"], vp[1]["n"], "cambio"),
            "no_ofrecidos": celda(vp[0]["cambio"], vp[0]["n"], "cambio"),
            "delta": dp, "ic95_wald": [lop, hip], "semiancho": semi_p,
            "excluye_cero": not (lop <= 0 <= hip),
            "declaracion": ("este contraste se corrio bajo la spec v1/v2 ANTES de que "
                            "apareciera el encargo v3, asi que P1 bajo v3 NO es ciega: "
                            "su desenlace es un vecino cercano de este. Se publica junto "
                            "al primario en vez de esconderse."),
        },
        "umbral_no_discrimina_semiancho": umbral,
        "veredicto_Bbis": veredicto,
        "razon_veredicto": razon,
        "reservas": [
            "panel NO ponderado: proporciones muestrales crudas, no comparables "
            "contra coeficientes de indice ni contra estimaciones ponderadas",
            f"n de ofrecidos en el universo de la pieza = {vc[1]['n']}; el panel 'Si' "
            "completo de T6 es 48 y el marginal del estudio 63. El encargo (v1 y v3) "
            "supuso 63 para esta pieza y es la cifra equivocada",
            "W2_P41 es autorreporte de OFERTA RECIBIDA, no de venta del voto: "
            "la prevalencia bruta es un piso, no una estimacion",
            "la seleccion de quien recibe oferta NO es aleatoria (targeting por "
            "partido, localidad y vulnerabilidad): esto es ASOCIACION, no coeficiente "
            "identificado. PROHIBIDO escribir 'el efecto de la compra de voto es X'",
        ],
        "entra_al_motor": False,
    }


def p1_robustez(der):
    """T7a/T7b por W2_PX8 (urbano/rural/mixto). Rotulo ROBUSTEZ: no adjudica."""
    # T7a: W2_P41 x W2_P7 | W2_PX8 -> turnout por ambito
    t7a = {}
    for r in der:
        if r["tabla"] != "T7a":
            continue
        d = t7a.setdefault(r["control_label"], {})
        d.setdefault(r["row_code"], {"voto": 0, "n": 0})
        n = int(r["n"])
        d[r["row_code"]]["n"] += n
        if r["col_code"] == "1":
            d[r["row_code"]]["voto"] += n
    ambitos = {}
    for amb, d in t7a.items():
        ofr, no = d.get("1"), d.get("0")
        if not ofr or not no:
            continue
        dd, lo, hi, semi = wald(ofr["voto"], ofr["n"], no["voto"], no["n"])
        ambitos[amb] = {
            "ofrecidos": {"voto": ofr["voto"], "n": ofr["n"],
                          "p": wilson(ofr["voto"], ofr["n"])},
            "no_ofrecidos": {"voto": no["voto"], "n": no["n"],
                             "p": wilson(no["voto"], no["n"])},
            "prevalencia_oferta": ofr["n"] / (ofr["n"] + no["n"]),
            "delta_turnout_pp": None if dd is None else dd * 100,
            "ic95_pp": [None, None] if lo is None else [lo * 100, hi * 100],
        }
    # T7b: W2_P41 x W2_P8 | W2_PX8 -> nivel de voto por ambito
    t7b = {}
    for r in der:
        if r["tabla"] != "T7b":
            continue
        n, cc = int(r["n"]), r["col_code"]
        d = t7b.setdefault(r["control_label"], {}).setdefault(
            r["row_code"], {"n": 0, "PRI": 0, "PAN": 0, "AMLO": 0})
        d["n"] += n
        if cc in CODIGOS_PARTIDARIOS:
            d[PARTIDO[cc]] = d.get(PARTIDO[cc], 0) + n
    nivel = {}
    for amb, d in t7b.items():
        nivel[amb] = {}
        for cod, dd in d.items():
            et = "ofrecidos" if cod == "1" else "no_ofrecidos"
            nivel[amb][et] = {"n": dd["n"],
                              "PRI": dd["PRI"], "p_PRI": wilson(dd["PRI"], dd["n"]),
                              "AMLO": dd["AMLO"], "p_AMLO": wilson(dd["AMLO"], dd["n"]),
                              "PAN": dd["PAN"], "p_PAN": wilson(dd["PAN"], dd["n"])}
    return {"rotulo": "ROBUSTEZ", "adjudica": False,
            "T7a_turnout_por_ambito": ambitos,
            "T7b_nivel_de_voto_por_ambito": nivel,
            "nota": ("no mueve el veredicto de P1 por spec. Las celdas de ofrecidos "
                     "por ambito son de una o dos decenas de casos: descriptivo.")}


# ---------------------------------------------------------------- P2
def p2_r73_r76(v0):
    """T3/T4 x W2_P8 con control W2_P36C. NO adjudica: replica no sellada."""
    salida = {}
    for tabla, expuesto, no_expuesto, var in (
            ("T3", "oportunidades=1", "oportunidades=0", "W2_P39B"),
            ("T4", "condicionaron=1", "condicionaron=0", "W2_P40")):
        por_estrato, agg = {}, {expuesto: {"PRI": 0, "tot": 0},
                               no_expuesto: {"PRI": 0, "tot": 0}}
        for r in v0:
            if r["tabla"] != tabla:
                continue
            n, e, col = int(r["n_sin_ponderar"]), r["estrato_W2_P36C"], r["columna"]
            d = por_estrato.setdefault(e, {expuesto: {"PRI": 0, "tot": 0},
                                           no_expuesto: {"PRI": 0, "tot": 0}})
            if col == "total_fila":
                d[r["fila"]]["tot"] += n
                agg[r["fila"]]["tot"] += n
            elif col == "PRI":
                d[r["fila"]]["PRI"] += n
                agg[r["fila"]]["PRI"] += n
        estratos = {}
        for e, d in sorted(por_estrato.items()):
            dd, lo, hi, semi = wald(d[expuesto]["PRI"], d[expuesto]["tot"],
                                        d[no_expuesto]["PRI"], d[no_expuesto]["tot"])
            estratos[e] = {
                "expuesto": {"PRI": d[expuesto]["PRI"], "n": d[expuesto]["tot"],
                             "p": wilson(d[expuesto]["PRI"], d[expuesto]["tot"])},
                "no_expuesto": {"PRI": d[no_expuesto]["PRI"], "n": d[no_expuesto]["tot"],
                                "p": wilson(d[no_expuesto]["PRI"], d[no_expuesto]["tot"])},
                "delta_pp": None if dd is None else dd * 100,
                "ic95_pp": [None, None] if lo is None else [lo * 100, hi * 100],
                "semi_ancho_pp": None if semi is None else semi * 100,
            }
        dd, lo, hi, semi = wald(agg[expuesto]["PRI"], agg[expuesto]["tot"],
                                    agg[no_expuesto]["PRI"], agg[no_expuesto]["tot"])
        salida[tabla] = {
            "variable_expuesto": var, "desenlace": "voto PRI (W2_P8)",
            "control": "W2_P36C (secreto percibido, 1-4)",
            "por_estrato": estratos,
            "agregado": {
                "expuesto": {"PRI": agg[expuesto]["PRI"], "n": agg[expuesto]["tot"],
                             "p": wilson(agg[expuesto]["PRI"], agg[expuesto]["tot"])},
                "no_expuesto": {"PRI": agg[no_expuesto]["PRI"], "n": agg[no_expuesto]["tot"],
                                "p": wilson(agg[no_expuesto]["PRI"], agg[no_expuesto]["tot"])},
                "delta_pp": dd * 100, "ic95_pp": [lo * 100, hi * 100],
                "semi_ancho_pp": semi * 100, "excluye_cero": not (lo <= 0 <= hi),
            },
            "rotulo": "REPLICA-DE-SEGUNDA-MANO-NO-SELLADA",
        }
    salida["_nota"] = (
        "NO ADJUDICA. Las lecturas preliminares (+2.0 / -3.8 pp, n 21) ya fueron "
        "vistas por mesa y direccion antes de esta spec: secuencia rota. Esta pieza "
        "sirve de contexto a N10, no de sello. No mueve el veredicto de R7.3 ni de R7.6.")
    salida["_reglas"] = ["R7.3 (FUERTE)", "R7.6 (MEDIA)"]
    salida["entra_al_motor"] = False
    return salida


# ---------------------------------------------------------------- P3
def p3_lista(der):
    """Experimento de lista T5: diferencia de medias B-A por ola. NC(9) excluido."""
    dists = {}
    for r in der:
        if r["tabla"] != "T5":
            continue
        cod = int(r["row_code"])
        if cod == 9:                    # NC: excluido, como lo hace el tabulador
            dists.setdefault(r["row_var"], {"nc": 0})["nc"] += int(r["n"])
            continue
        dists.setdefault(r["row_var"], {"nc": 0})[cod] = int(r["n"])

    olas = {}
    for nombre, a, b in (("ola1_marzo", "P35A", "P35B"),
                         ("ola2_julio", "W2_P35A", "W2_P35B")):
        da = {k: v for k, v in dists[a].items() if k != "nc"}
        db = {k: v for k, v in dists[b].items() if k != "nc"}
        ma, va, na = media_y_var(da)
        mb, vb, nb = media_y_var(db)
        d = mb - ma
        ee = math.sqrt(vb / nb + va / na)
        olas[nombre] = {
            "lista_A": {"var": a, "media": ma, "n_valid": na, "nc_excluidos": dists[a]["nc"]},
            "lista_B": {"var": b, "media": mb, "n_valid": nb, "nc_excluidos": dists[b]["nc"]},
            "delta": d, "ee": ee, "t": d / ee,
            "ic95": [d - Z * ee, d + Z * ee],
            "excluye_cero": (d - Z * ee) * (d + Z * ee) > 0,
            "delta_pct": d * 100,
        }
    olas["contraste_con_pregunta_directa"] = {
        "directa_W2_P41_pct": 5.5,
        "razon_lista_sobre_directa_ola2": olas["ola2_julio"]["delta_pct"] / 5.5,
        "limite": ("las dos cifras NO miden el mismo estimando: W2_P41 pregunta si le "
                   "OFRECIERON; el item de la lista, SI el supuesto 2 se sostiene, "
                   "pregunta por conducta propia. El factor mezcla subreporte con "
                   "diferencia de constructo y no se puede repartir con estas tablas."),
    }
    olas["clase"] = "MEDIDO.Delta de segunda mano"
    olas["NO_es"] = "p de regla"
    olas["secuencia"] = ("ROTA: la lectura 18.8% ya estaba escrita en la Adenda 3 de "
                         "LEEME 2-procedencia.txt antes de congelar esta spec.")
    olas["supuesto_no_verificado_que_lo_gobierna"] = (
        "que lista B = lista A + UN item y que ese item sea la venta del voto. El "
        "texto de los items NO esta en estas salidas. Hasta leerlo en el cuestionario "
        "de ICPSR 35024, la cifra es PROPUESTA CON RESERVA, no prevalencia medida.")
    olas["prohibido"] = "escribir 'subio de 6.9% a 18.8%': los IC de las dos olas se traslapan"
    olas["entra_al_motor"] = False
    return olas


# ---------------------------------------------------------------- P4
def p4_exploratorio(der):
    """T8 y T9a: inventario con IC, rotulo EXPLORATORIO. SIN veredicto.

    Entra solo a la nota; NO entra a milpa/tramite-ola5-propuesta-v0.yaml.
    """
    # --- T8: W2_P53 (marca en credencial) x W2_P7 (voto declarado)
    t8, t8_no_voto = {}, 0
    for r in der:
        if r["tabla"] != "T8":
            continue
        n = int(r["n"])
        if r["col_code"] == "1":
            t8[r["row_label"]] = t8.get(r["row_label"], 0) + n
        else:
            t8_no_voto += n
    n8 = sum(t8.values())
    corroborado = max(t8.items(), key=lambda kv: kv[1]) if t8 else (None, 0)
    t8_out = {
        "universo": "quien declaro haber votado (W2_P7=1)", "n": n8,
        "celdas": {k: {"n": v, "p": wilson(v, n8)} for k, v in sorted(t8.items())},
        "columna_no_voto": t8_no_voto,
        "limite_medido": (
            "la columna 'no voto' es CERO en todas las filas: W2_P53 solo se "
            "pregunto a quien declaro haber votado. NO hay no-votantes en el "
            "denominador, asi que T8 NO puede calibrar sobrerreporte de "
            "participacion, que era la funcion que el plan le asignaba."),
        "advertencia": (
            "los estados 'no pudo ver', 'no trae credencial' y 'se niega a mostrar' "
            "son NO-VERIFICABLE, no falso: colapsarlos con 'no tiene marca' y "
            "'afirma haber votado sin marca' produce una tasa de mentira inflada "
            "por rechazo a mostrar identificacion, que es otro fenomeno."),
        "corroborado_por_marca": {"etiqueta": corroborado[0], "n": corroborado[1],
                                  "p": wilson(corroborado[1], n8)},
    }

    # --- T9a: W2_P36D (percepcion de compra de voto) x W2_P41 (oferta recibida)
    t9 = {}
    for r in der:
        if r["tabla"] != "T9a":
            continue
        d = t9.setdefault(r["row_label"], {"ofrecido": 0, "n": 0})
        d["n"] += int(r["n"])
        if r["col_code"] == "1":
            d["ofrecido"] += int(r["n"])
    t9_out = {k: {"ofrecido": v["ofrecido"], "n": v["n"],
                  "p": wilson(v["ofrecido"], v["n"])} for k, v in t9.items()}
    tot_n = sum(v["n"] for v in t9.values())
    tot_o = sum(v["ofrecido"] for v in t9.values())

    return {
        "rotulo": "EXPLORATORIO", "veredicto": None, "adjudica": False,
        "entra_a_la_propuesta": False, "entra_al_motor": False,
        "T8_marca_en_credencial": t8_out,
        "T9a_percepcion_x_oferta": {
            "celdas": t9_out, "n_total": tot_n, "ofrecidos_total": tot_o,
            "prevalencia_global": wilson(tot_o, tot_n),
            "prohibido": (
                "escribir 'la percepcion de compra de voto es sobre todo vivencia'. "
                "Las dos variables son de la MISMA ola (sin orden temporal), el "
                "sentido mas probable es el inverso (recibir el regalo produce el "
                "reporte), y aun entre quienes estan TOTALMENTE de acuerdo la gran "
                "mayoria NO recibio oferta: la percepcion excede a la experiencia "
                "por un orden de magnitud."),
            "NS_no_se_colapsa": (
                "no saber y negar son estados distintos; una celda con numerador 0 "
                "sostiene 'ninguna observada en esta muestra', no 'cero ofertas'."),
        },
    }


def p4_pendiente(der):
    """Que falta de verdad, tras comprobar T6-T9 contra disco."""
    presentes = sorted({r["tabla"] for r in der})
    return {
        "P1_se_lanza": "T6" in presentes,
        "tablas_en_disco": presentes,
        "premisa_del_encargo_refutada": (
            "el encargo (v1 y v3) supone que T6-T9 no han sido LEIDAS EN VALOR por "
            "nadie. LEEME 2-procedencia.txt trae tres adendas de direccion del 2/sep "
            "con ICs, t, p y gradientes en valor de T5, T6, T7a, T7b, T8 y T9a. Lo "
            "unico que ninguna adenda calcula es el contraste de vote-change de P1."),
        "pendiente_de_mesa_real": {
            "T9b": "W2_P38A x W2_P38B, control P46 -- no aparece en disco",
            "serie_ronda_1": ["P40 x P7", "P40 x P8", "P38B x P8 | P36C", "P39 x P8"],
            "control_negativo": ("ninguna tabla del disco usa P40, P39 ni P38B como "
                                 "variable de fila o columna"),
            "texto_de_los_items_P35A_P35B": (
                "leer el cuestionario: es lo unico que convierte P3 de propuesta en medicion"),
        },
        "receta_para_mesa": ("Explore Data -> Crosstabs; T9b: fila W2_P38A, columna "
                             "W2_P38B, control P46, exportar. Serie ronda 1: las cuatro "
                             "de arriba, sin control salvo la tercera (control P36C)."),
        "FP": "FP-263",
    }


# ---------------------------------------------------------------- main
def main():
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raiz = raiz_descargas(repo)
    rutas = {p: os.path.join(raiz, arch) for p, (arch, _) in PAYLOADS.items()}
    faltan = [r for r in rutas.values() if not os.path.exists(r)]
    if faltan:
        raise SystemExit("PARO: payloads no encontrados:\n  " + "\n  ".join(faltan))

    v0 = lee_csv(rutas["icpsr35024_ds1_w2_crosstabs_derivado_v0"])
    der = lee_csv(rutas["icpsr35024_ds1_w2_crosstabs_derivadas"])

    p0 = p0_censo(rutas, v0, der)
    if p0["estado"] == "PARO":
        salida = {"acto": "MAESTRA36-L12", "P0": p0,
                  "P1": "NO-LANZADA: P0 en PARO", "P2": None, "P3": None}
    else:
        salida = {
            "acto": "MAESTRA36-L12 · MPS-2012-CROSSTABS",
            "fecha": "2026-09-03",
            "spec_congelada": ["forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada.md (COMMIT-1)",
                               "forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada-bis-v3.md (COMMIT-1-bis, manda)"],
            "fuente": "ICPSR 35024 Mexico Panel Study 2012, DS1, ola 2 (W2), "
                      "tabulador en linea 'Explore Data'",
            "doi": "https://doi.org/10.3886/ICPSR35024.v1",
            "P0_censo_y_estampa": p0,
            "P1_R7_7_vote_choice": p1_r77(v0, der),
            "P1_robustez_T7": p1_robustez(der),
            "P2_R7_3_R7_6_replica": p2_r73_r76(v0),
            "P3_experimento_de_lista": p3_lista(der),
            "P4_exploratorio_T8_T9a": p4_exploratorio(der),
            "pendiente_de_mesa": p4_pendiente(der),
        }
    salida["cargas_al_motor"] = 0

    dest = os.path.join(repo, "data", "l12-mps2012-v1_0.json")
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(salida, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"escrito {os.path.relpath(dest, repo)}")
    if "--json" not in sys.argv:
        return
    json.dump(salida, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
