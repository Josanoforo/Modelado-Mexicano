#!/usr/bin/env python3
"""ACTO MAESTRA36-L12 · MPS-2012-CROSSTABS — medidor de las piezas P0..P4.

Ejecuta la spec CONGELADA en
`forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada.md` (COMMIT-1).

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

# spec Sec.2: mapeo candidato CONGELADO. 08/11/12/13 NO son candidato.
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


def newcombe(k1, n1, k0, n0):
    """IC95 de la diferencia p1-p0 por el hibrido de scores de Newcombe.

    Punto = p1-p0 (no el centro de Wilson). Limites por raiz cuadrada de la
    suma de las distancias al limite correspondiente de cada Wilson.
    """
    if n1 == 0 or n0 == 0:
        return (None, None, None, None)
    p1, l1, u1 = wilson(k1, n1)
    p0, l0, u0 = wilson(k0, n0)
    d = p1 - p0
    lo = d - math.sqrt((p1 - l1) ** 2 + (u0 - p0) ** 2)
    hi = d + math.sqrt((u1 - p1) ** 2 + (p0 - l0) ** 2)
    return (d, lo, hi, (hi - lo) / 2.0)


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
def p1_r77(v0, der):
    """R7.7: mitad turnout (T1) y mitad vote-choice (T6). Falsador B-bis."""
    # --- turnout, T1 agregando los cuatro estratos
    tur = {}
    for r in v0:
        if r["tabla"] != "T1":
            continue
        ofr = 1 if r["fila"] == "ofrecieron=1" else 0
        voto = r["columna"] == "voto=1"
        d = tur.setdefault(ofr, {"voto": 0, "n": 0})
        d["n"] += int(r["n_sin_ponderar"])
        if voto:
            d["voto"] += int(r["n_sin_ponderar"])
    dt, lot, hit, semi_t = newcombe(tur[1]["voto"], tur[1]["n"],
                                    tur[0]["voto"], tur[0]["n"])

    # --- vote-choice, T6 restringido a celdas candidato -> candidato
    vc, fuera = {}, {"filas_no_candidato": 0, "cols_no_candidato": 0, "n_excluido": 0}
    for r in der:
        if r["tabla"] != "T6":
            continue
        n = int(r["n"])
        pr, pc = PARTIDO.get(r["row_code"]), PARTIDO.get(r["col_code"])
        if pr is None or pc is None:
            fuera["n_excluido"] += n
            fuera["filas_no_candidato"] += n if pr is None else 0
            fuera["cols_no_candidato"] += n if pc is None else 0
            continue
        ofr = int(r["control_code"])
        d = vc.setdefault(ofr, {"cambio": 0, "n": 0})
        d["n"] += n
        if pr != pc:
            d["cambio"] += n
    dv, lov, hiv, semi_v = newcombe(vc[1]["cambio"], vc[1]["n"],
                                    vc[0]["cambio"], vc[0]["n"])

    # --- falsador B-bis: el semi-ancho se evalua ANTES de mirar el signo
    umbral = 0.15
    if semi_v is None or semi_v > umbral:
        veredicto = "NO-DISCRIMINA"
        razon = (f"semi-ancho del IC95 de Delta_vote-change = "
                 f"{semi_v:.4f} > {umbral} (+-15 pp). Rama de precedencia.")
    elif (lot <= 0 <= hit) and (lov <= 0 <= hiv):
        veredicto = "CORROBORADA"
        razon = "IC95 de Delta_turnout y de Delta_vote-change contienen 0."
    elif not (lov <= 0 <= hiv):
        veredicto = "CONTRARIA"
        razon = "IC95 de Delta_vote-change queda fuera de 0."
    else:
        veredicto = "NO-DISCRIMINA"
        razon = "ninguna rama del falsador se satisface limpiamente."

    return {
        "regla": "R7.7", "tier_canon": "MEDIA",
        "enunciado": "dadiva + broker -> compra turnout, no vote-choice",
        "turnout_T1": {
            "ofrecidos": {"voto": tur[1]["voto"], "n": tur[1]["n"],
                          "p": wilson(tur[1]["voto"], tur[1]["n"])},
            "no_ofrecidos": {"voto": tur[0]["voto"], "n": tur[0]["n"],
                             "p": wilson(tur[0]["voto"], tur[0]["n"])},
            "delta": dt, "ic95": [lot, hit], "semi_ancho": semi_t,
            "excluye_cero": not (lot <= 0 <= hit),
        },
        "vote_change_T6": {
            "ofrecidos": {"cambio": vc[1]["cambio"], "n": vc[1]["n"],
                          "p": wilson(vc[1]["cambio"], vc[1]["n"])},
            "no_ofrecidos": {"cambio": vc[0]["cambio"], "n": vc[0]["n"],
                             "p": wilson(vc[0]["cambio"], vc[0]["n"])},
            "delta": dv, "ic95": [lov, hiv], "semi_ancho": semi_v,
            "excluye_cero": not (lov <= 0 <= hiv),
            "excluido_por_no_candidato": fuera,
        },
        "umbral_no_discrimina_semi_ancho": umbral,
        "veredicto_Bbis": veredicto,
        "razon_veredicto": razon,
        "reservas": [
            "panel NO ponderado: proporciones muestrales crudas, no comparables "
            "contra coeficientes de indice ni contra estimaciones ponderadas",
            f"n de ofrecidos en T6 (candidato->candidato) = {vc[1]['n']}; el panel "
            "'Si' completo de T6 es 48 y el marginal del estudio 63 -- el encargo "
            "supuso 63 para esta pieza y es la cifra equivocada",
            "W2_P41 es autorreporte de OFERTA RECIBIDA, no de venta del voto: "
            "la prevalencia bruta es un piso, no una estimacion",
            "W2_P41 no esta asignado al azar (targeting por partido, localidad y "
            "vulnerabilidad): esto es ASOCIACION, no coeficiente identificado. "
            "PROHIBIDO escribir 'el efecto de la compra de voto es X'",
        ],
        "entra_al_motor": False,
    }


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
            dd, lo, hi, semi = newcombe(d[expuesto]["PRI"], d[expuesto]["tot"],
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
        dd, lo, hi, semi = newcombe(agg[expuesto]["PRI"], agg[expuesto]["tot"],
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
def p4_pendiente(der):
    """Que falta de verdad, tras comprobar T6-T9 contra disco."""
    presentes = sorted({r["tabla"] for r in der})
    return {
        "P1_se_lanza": "T6" in presentes,
        "tablas_en_disco": presentes,
        "premisa_del_encargo_refutada": (
            "el encargo supuso 'T6-T9 no han sido exportadas'. T6, T7a, T7b, T8 y "
            "T9a SI estan. Corroborado por ADR-310 y por la nota de MAESTRA36-A1."),
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
        "FP": "FP-261",
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
            "spec_congelada": "forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada.md",
            "fuente": "ICPSR 35024 Mexico Panel Study 2012, DS1, ola 2 (W2), "
                      "tabulador en linea 'Explore Data'",
            "doi": "https://doi.org/10.3886/ICPSR35024.v1",
            "P0_censo_y_estampa": p0,
            "P1_R7_7_vote_choice": p1_r77(v0, der),
            "P2_R7_3_R7_6_replica": p2_r73_r76(v0),
            "P3_experimento_de_lista": p3_lista(der),
            "P4_pendiente_de_mesa": p4_pendiente(der),
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
