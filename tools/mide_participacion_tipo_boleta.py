#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACTO MAESTRA35-L3 · CIVICA-TIPO-DE-BOLETA — medidor por TIPO de boleta federal.

Hermano de tools/l6_estimador_concurrencia.py (ACTO MAESTRA34-L6): importa sus
lectores y NO lo modifica, de modo que la corrida de L6 se reproduce byte a byte
como control de regresion (--control-l6).

Sustituye la tendencia lineal de L6 (unica gamma) por un efecto fijo de TIPO de
anio federal, que es la firma c1 de mesa (2/sep/2026):

    Dy(m,k) = alpha*hueco(k) + beta_pres*DD_pres(k) + beta_int*DD_int(k) + e(m,k)

Modos:
    --tabla-identificacion   escribe la tabla de identificacion (P0), TSV a stdout
    --control-l6             re-corre el estimador de L6 y compara con su JSON
    --json <ruta>            corre el modelo de arriba y vuelca el resultado
"""
import argparse, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CALENDARIO = "data/p0-calendario-ayuntamientos-v1_0.tsv"
TRATAMIENTO = "data/p0-tratamiento-homologacion-v1_0.tsv"

# Anios federales de la ventana y su TIPO. Fuente: el propio calendario del INE
# ya cifrado en data/p0-calendario-ayuntamientos-v1_0.tsv (columna
# nota_concurrencia dice "anio federal" para 2018, 2021 y 2024) mas el hecho
# constitucional de que la eleccion presidencial cae cada seis anios (2018, 2024)
# y la intermedia en el punto medio (2015, 2021).
TIPO_FEDERAL = {2015: "intermedia", 2018: "presidencial",
                2021: "intermedia", 2024: "presidencial"}


# ───────────────────────────── calendario y tipos ─────────────────────────────
def lee_calendario(ruta=CALENDARIO):
    """{entidad: {anio: concurrente_bool}} leido por linea (nunca con csv)."""
    cal = {}
    with open(ruta, encoding="utf-8") as fh:
        lineas = [l.rstrip("\n") for l in fh]
    cab = lineas[1].split("\t")
    i_ent, i_anio = cab.index("entidad"), cab.index("anio_jornada")
    i_conc, i_ayto = cab.index("concurrente_con_federal"), cab.index("ayuntamientos")
    for l in lineas[2:]:
        if not l.strip():
            continue
        p = l.split("\t")
        if p[i_ayto] != "SI":
            continue
        cal.setdefault(p[i_ent], {})[int(p[i_anio])] = (p[i_conc] == "SI")
    return cal


def dpres_dint(anio, concurrente):
    """D_pres, D_int de una eleccion local, segun la spec §1.5 de este acto."""
    if not concurrente:
        return 0, 0
    t = TIPO_FEDERAL.get(anio)
    return (1 if t == "presidencial" else 0), (1 if t == "intermedia" else 0)


def clase_transicion(dp, di):
    if dp == 0 and di == 0:
        return "STAY"
    return "SWITCH"


def etiqueta_pata(anio, conc):
    if not conc:
        return "sin-federal"
    return TIPO_FEDERAL.get(anio, "federal-?")


# ────────────────────────── P0 · tabla de identificacion ──────────────────────
def tabla_identificacion(ventana=(2015, 2024)):
    """Una fila por entidad x transicion consecutiva, para TODAS las entidades
    del calendario. Se escribe ANTES de abrir un solo resultado."""
    cal = lee_calendario()
    trat = {}
    with open(TRATAMIENTO, encoding="utf-8") as fh:
        lineas = [l.rstrip("\n") for l in fh]
    cab = lineas[1].split("\t")
    for l in lineas[2:]:
        if not l.strip():
            continue
        p = l.split("\t")
        trat[p[cab.index("entidad")]] = (p[cab.index("estatus")], p[cab.index("cohorte")])

    filas = []
    for ent in sorted(cal):
        anios = sorted(a for a in cal[ent] if ventana[0] <= a <= ventana[1])
        for a, b in zip(anios, anios[1:]):
            dpa, dia = dpres_dint(a, cal[ent][a])
            dpb, dib = dpres_dint(b, cal[ent][b])
            ddp, ddi = dpb - dpa, dib - dia
            est, coh = trat.get(ent, ("?", ""))
            filas.append({
                "entidad": ent, "de": a, "a": b, "hueco": b - a,
                "tipo_de": etiqueta_pata(a, cal[ent][a]),
                "tipo_a": etiqueta_pata(b, cal[ent][b]),
                "dD_pres": ddp, "dD_int": ddi,
                "clase": clase_transicion(ddp, ddi),
                "estatus_entidad": est, "cohorte": coh,
                "identifica": identifica(ddp, ddi)})
    return filas


def identifica(ddp, ddi):
    if ddp == 0 and ddi == 0:
        return "alpha"
    if ddp != 0 and ddi == 0:
        return "beta_pres (+alpha)"
    if ddp == 0 and ddi != 0:
        return "beta_int (+alpha)"
    return "beta_pres - beta_int (+alpha)"


def imprime_tabla(filas):
    cols = ["entidad", "de", "a", "hueco", "tipo_de", "tipo_a", "dD_pres",
            "dD_int", "clase", "identifica", "estatus_entidad", "cohorte"]
    print("\t".join(cols))
    for f in filas:
        print("\t".join(str(f[c]) for c in cols))


def resumen_identificacion(filas, solo=None):
    """Conteo de transiciones por parametro identificado. `solo` = conjunto de
    entidades del panel; None = universo entero del calendario."""
    sub = [f for f in filas if solo is None or f["entidad"] in solo]
    c = {}
    for f in sub:
        c[f["identifica"]] = c.get(f["identifica"], 0) + 1
    return {"n_transiciones": len(sub), "por_parametro": c,
            "n_STAY": sum(1 for f in sub if f["clase"] == "STAY"),
            "n_SWITCH": sum(1 for f in sub if f["clase"] == "SWITCH"),
            "entidades": sorted({f["entidad"] for f in sub})}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tabla-identificacion", action="store_true")
    ap.add_argument("--resumen", action="store_true")
    a = ap.parse_args()
    if a.tabla_identificacion:
        filas = tabla_identificacion()
        imprime_tabla(filas)
        if a.resumen:
            print("\n# RESUMEN (universo del calendario):", file=sys.stderr)
            print(json.dumps(resumen_identificacion(filas), ensure_ascii=False,
                             indent=1), file=sys.stderr)
        return
    ap.error("elige un modo")


if __name__ == "__main__":
    main()
