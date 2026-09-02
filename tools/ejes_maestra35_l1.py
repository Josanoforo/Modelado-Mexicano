#!/usr/bin/env python3
"""ACTO MAESTRA35-L1 · maquinaria de ejes compartida por P2, P3 y P4.

Existe para que el diff sobre cada uno de los tres medidores de MAESTRA34-L5
sea el minimo que el encargo pide -- «gana un parametro de eje, sin cambiar
ninguna otra linea»: un import, una funcion y una rama de CLI. Ninguna linea
del comportamiento anterior de esos medidores cambia.

Los codigos de cada eje NO se inventan aqui: salen del censo `P0`
(`forense/notas/2026-09-02-MAESTRA35-L1-P0-censo.md`), que los leyo del FD o
del catalogo de cada payload, y estan congelados en la spec
(`forense/notas/2026-09-02-MAESTRA35-L1-spec.md`, seccions 1.2, 1.3, 3.1,
4.1 y 5.1).

Vocabulario de veredicto (spec 1.1), y como se opera:
  CORROBORADA  celdas extremas en el signo esperado, IC95 SIN traslape
  CONTRARIA    celdas extremas en signo opuesto, IC95 SIN traslape
  NO-DISCRIMINA IC95 de las extremas se traslapan
  DISCRIMINA   IC95 sin traslape pero el eje no traia signo pre-registrado
  Precedencia: CONTRARIA manda sobre CORROBORADA cuando un mismo eje da ambas
  en tramos distintos. «Tramos distintos» se opera como PARES CONSECUTIVOS a lo
  largo del orden declarado del eje: si algun par consecutivo va en el signo
  esperado sin traslape y otro va en contra sin traslape, el eje es NO MONOTONO
  y el veredicto es CONTRARIA. Esta operacionalizacion es del commit de
  resultados, no de la spec: la spec fijo la regla, no como se recorre el orden.
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calibracion_mordida_encig_serie import wprop_ic_conglomerado  # noqa: E402

FUERA = "(fuera)"

# --- Codificaciones congeladas por el censo P0 -------------------------------
ESC_1DIG = {"0": "hasta primaria", "1": "hasta primaria", "2": "hasta primaria",
            "3": "secundaria", "4": "media superior", "5": "media superior",
            "6": "media superior", "7": "media superior",
            "8": "superior", "9": "superior"}                     # ENCIG 2025
ESC_2DIG = {"00": "hasta primaria", "01": "hasta primaria",
            "02": "hasta primaria", "03": "secundaria",
            "04": "media superior", "05": "media superior",
            "06": "media superior", "07": "media superior",
            "08": "superior", "09": "superior"}                   # ENVIPE 2025
ESC_ENIF = dict(ESC_2DIG, **{"10": "superior", "11": "superior"})  # ENIF 2024
ORD_ESC = ["hasta primaria", "secundaria", "media superior", "superior"]
ORD_EDAD = ["18-29", "30-44", "45-59", "60+"]
ORD_SEXO = ["1 Hombre", "2 Mujer"]
SEXO = {"1": "1 Hombre", "2": "2 Mujer"}


def tramos_edad(serie):
    e = pd.to_numeric(serie, errors="coerce")
    out = pd.Series(FUERA, index=serie.index, dtype=object)
    out[(e >= 18) & (e <= 29)] = "18-29"
    out[(e >= 30) & (e <= 44)] = "30-44"
    out[(e >= 45) & (e <= 59)] = "45-59"
    out[(e >= 60) & (e <= 96)] = "60+"
    return out


class Eje:
    """Un eje: como se deriva la celda, en que orden van las celdas, y que
    signo se pre-registro para p a lo largo de ese orden.

    signo: 'asc'  p sube a lo largo de `orden`
           'desc' p baja a lo largo de `orden`
           None   sin prediccion -> el veredicto maximo posible es DISCRIMINA
    tope: si se da, limita el vocabulario aunque haya signo (usado por el eje
          de cuenta contra el desenlace principal, spec 3.3).
    """

    def __init__(self, nombre, deriva, orden, signo, nota="", tope=None):
        self.nombre, self.deriva = nombre, deriva
        self.orden, self.signo, self.nota, self.tope = orden, signo, nota, tope


def _sin_traslape(a, b):
    return a["hi"] < b["lo"] or b["hi"] < a["lo"]


def _dirige(a, b, signo):
    """Devuelve 'esperado', 'contrario' o None para el par ordenado (a, b)."""
    if signo is None:
        return None
    sube = b["p"] > a["p"]
    esperado = sube if signo == "asc" else not sube
    return "esperado" if esperado else "contrario"


def veredicto(celdas, eje):
    """celdas: lista de dicts en el orden declarado del eje (solo las que
    tienen n>0). Devuelve (veredicto, monotonia)."""
    vivas = [c for c in celdas if c["n"] > 0]
    if len(vivas) < 2:
        return "NO-EVALUABLE (menos de dos celdas con n>0)", "n/a"
    a, b = vivas[0], vivas[-1]
    traslapan = not _sin_traslape(a, b)

    pares = [(vivas[i], vivas[i + 1]) for i in range(len(vivas) - 1)]
    limpios = [(x, y) for x, y in pares if _sin_traslape(x, y)]
    dirs = {_dirige(x, y, eje.signo) for x, y in limpios}
    no_monotono = "esperado" in dirs and "contrario" in dirs
    mono = ("NO MONOTONO (pares consecutivos limpios en los dos sentidos)"
            if no_monotono else
            "monotono o sin pares consecutivos limpios en sentidos opuestos")

    if eje.signo is None:
        v = "NO-DISCRIMINA" if traslapan else "DISCRIMINA"
    elif no_monotono:
        v = "CONTRARIA"          # precedencia declarada en la spec 1.1
    elif traslapan:
        v = "NO-DISCRIMINA"
    else:
        v = ("CORROBORADA" if _dirige(a, b, eje.signo) == "esperado"
             else "CONTRARIA")
    if eje.tope and v == "CORROBORADA":
        v = f"{eje.tope} (tope declarado en la spec: el eje no puede corroborar)"
    return v, mono


def mide_eje(df, eje, d, w, est, upm):
    """Estima una celda por valor del eje. `d`, `w`, `est`, `upm` son SERIES
    ya alineadas con `df` -- este modulo nunca define el desenlace, solo lo
    recibe: el desenlace vive en el medidor de cada pieza."""
    celda = eje.deriva(df)
    dentro = celda != FUERA
    cobertura = float(dentro.mean())
    filas = []
    for k in eje.orden:
        sel = celda == k
        if not sel.any():
            filas.append({"celda": k, "n": 0})
            continue
        p, lo, hi, n, n_est, n_cl = wprop_ic_conglomerado(
            d[sel].to_numpy(dtype=float), w[sel].to_numpy(dtype=float),
            est[sel].tolist(), upm[sel].tolist())
        filas.append({"celda": k, "p": p, "lo": lo, "hi": hi, "n": n,
                      "n_num": int(d[sel].sum()), "n_est": n_est,
                      "n_upm": n_cl, "pobl": float(w[sel].sum())})
    v, mono = veredicto(filas, eje)
    return {"eje": eje.nombre, "cobertura": cobertura, "celdas": filas,
            "veredicto": v, "monotonia": mono, "signo": eje.signo,
            "nota": eje.nota, "n_fuera": int((~dentro).sum())}


def imprime(r, unidad):
    restr = " · UNIVERSO RESTRINGIDO (A-bis 4)" if r["cobertura"] < 0.90 else ""
    print(f"  EJE {r['eje']} · cobertura {r['cobertura']:.4%}"
          f" (fuera {r['n_fuera']:,}){restr}")
    if r["nota"]:
        print(f"    nota: {r['nota']}")
    for c in r["celdas"]:
        if c["n"] == 0:
            print(f"    {c['celda']:<22s} celda vacia")
            continue
        print(f"    {c['celda']:<22s} p̂ = {c['p']:.6f}  "
              f"IC95 = [{c['lo']:.6f}, {c['hi']:.6f}]  "
              f"n = {c['n']:,} {unidad} · num = {c['n_num']:,} · "
              f"estratos = {c['n_est']} · UPM = {c['n_upm']:,}")
    signo = r["signo"] or "sin signo pre-registrado"
    print(f"    signo esperado: {signo} · {r['monotonia']}")
    print(f"    VEREDICTO: {r['veredicto']}")
    print()
