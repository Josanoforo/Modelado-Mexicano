#!/usr/bin/env python3
"""Guardián de ENIGH 2024 para el duelo prospectivo — único código autorizado
a tocar la ola reservada antes de COMMIT-3.

ACTO `GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, P4. E.6 (instrucciones-proyecto):
«el único código autorizado a tocar la ola reservada se congela en COMMIT-1
con guardia de una sola variable de agrupación». Molde:
`tools/celda_d/marginales_reproduccion.py` (ENVIPE, ajeno al perímetro de
este acto — no se importa, no se edita; guardia propia, mismo principio).

**Por qué la guardia es más simple que la de ENVIPE.** El duelo ENIGH 2024
(`forense/prereg-caja/DISENO-duelo-prospectivo-ENIGH2024-v1_0.md §3`) declara
el nivel cruce **fuera de alcance**: no hay ejes, no hay `marginal(ola, eje)`
con una lista de ejes admitidos. Hay UNA sola celda nacional
(`remesas > 0`, unidad hogar). La «variable de agrupación única» de este
guardián es, literalmente, que sólo se lee LA COLUMNA `remesas` (más las de
diseño/llave que la acompañan) — ninguna otra columna de `concentradohogar`
se toca, y no existe ninguna función que reciba un nombre de columna como
parámetro: no hay superficie para pedir "otra cosa".

QUÉ HACE
--------
  · `carga_hogares(ruta_zip, miembro, *, reservada)` — lee SOLO
    `folioviv, foliohog, factor, remesas, est_dis, upm` del miembro
    `concentradohogar` declarado; nada más se abre del zip (ni otras
    columnas, ni otros miembros). Devuelve un `MarcoHogares` inmutable con
    `huella` (sha256 de la tupla ordenada de `(folioviv, foliohog, remesas)`)
    y `reservada` congelado en el objeto.
  · `nacional(marco)` — la ÚNICA celda: proporción de hogares con
    `remesas > 0`, ponderada por `factor`, con IC95 bootstrap de UPM dentro
    de `est_dis` (mismo método que `CALC-ENIGH{2016,2018,2020}-INTENSIDAD-
    REMESAS-0001`, ya sellados en este acto). Lanza `ReservaRota` si
    `marco.reservada` es `True` — el CALC de emisiones (COMMIT-2) carga con
    `reservada=True` y NO puede llamar a `nacional()` directamente: solo
    `emite_bajo_reserva()` (abajo) puede, y esa función es la ÚNICA
    autorizada a estar en la cadena de llamada de un CALC con
    `etiquetas.tipo` que declare `EMISION-BAJO-RESERVA` en su `spec.yaml`
    (verificado por `contrato["parametros"]["autoriza_reserva"] is True`,
    que solo `corrida0.py run` puede fijar desde una spec ya committeada —
    no hay forma de pasarlo desde un intérprete interactivo sin editar un
    archivo versionado primero).
  · `emite_bajo_reserva(marco, autoriza)` — el único punto de entrada que
    puede levantar la reserva de `nacional()`, y solo si `autoriza is True`
    Y `marco.reservada is True` (ambos, no uno): una llamada con
    `autoriza=True` sobre un marco `reservada=False` (COMMIT-3, ola ya no
    reservada) es un error de programación, no una autorización — lanza
    `ValueError`, no se silencia.

Falsador (D-14): si algún acto futuro deriva `remesas>0` de ENIGH 2024 sin
pasar por este módulo, este guardián no evitó nada y se revisa.
"""
from __future__ import annotations

import csv
import hashlib
import io
import math
import zipfile
from dataclasses import dataclass

import numpy as np

COLUMNAS = ("folioviv", "foliohog", "factor", "remesas", "est_dis", "upm")


class ReservaRota(RuntimeError):
    pass


def _texto(v):
    if v is None:
        return None
    s = str(v).lstrip("﻿").lstrip("ï»¿").strip().strip('"')
    return s or None


def _numero(v):
    s = _texto(v)
    if s is None:
        return None
    try:
        x = float(s.replace(",", ""))
    except ValueError:
        return None
    return x if math.isfinite(x) else None


@dataclass(frozen=True)
class MarcoHogares:
    filas: tuple
    reservada: bool
    huella: str


def _huella(filas):
    """sha256 de (folioviv, foliohog, remesas) en el orden leído -- una
    re-huella posterior que no coincida detecta un marco alterado."""
    canon = "|".join(f"{f['folioviv']}:{f['foliohog']}:{f['remesas']}" for f in filas)
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def carga_hogares(ruta_zip: str, miembro: str, *, reservada: bool) -> MarcoHogares:
    """Lee SOLO las columnas de COLUMNAS del miembro concentradohogar
    declarado. No abre ningún otro miembro del zip, no lee ninguna otra
    columna. `reservada` se congela en el objeto devuelto -- no se puede
    cambiar después de cargar."""
    with zipfile.ZipFile(ruta_zip) as zf:
        with zf.open(miembro) as fh:
            texto = io.TextIOWrapper(fh, encoding="latin-1", newline="")
            lector = csv.DictReader(texto)
            if lector.fieldnames is None:
                raise ValueError(f"{miembro}: cabecera ausente")
            mapa = {_texto(c).lower(): c for c in lector.fieldnames}
            faltan = [c for c in COLUMNAS if c not in mapa]
            if faltan:
                raise ValueError(f"{miembro}: columnas ausentes {faltan}")
            filas = []
            for r in lector:
                fila = {c: _texto(r.get(mapa[c], "")) for c in COLUMNAS}
                filas.append(fila)
    filas = tuple(filas)
    return MarcoHogares(filas=filas, reservada=bool(reservada), huella=_huella(filas))


def _calcula_nacional(marco: MarcoHogares, replicas: int = 2000, seed: int = 20260921) -> dict:
    if marco.huella != _huella(marco.filas):
        raise ReservaRota("marco alterado tras carga_hogares: huella no coincide")
    validos, contrib = [], []
    n_peso_invalido = n_r_invalido = 0
    for f in marco.filas:
        peso = _numero(f["factor"])
        remesa = _numero(f["remesas"])
        if peso is None or peso <= 0:
            n_peso_invalido += 1
            continue
        if remesa is None or remesa < 0:
            n_r_invalido += 1
            continue
        validos.append((_texto(f["est_dis"]), _texto(f["upm"]), peso, remesa))
    if not validos:
        return {"estado": "NO-ESTIMABLE-SIN-HOGARES-VALIDOS", "p": None, "ic95": None,
                "n_validos": 0, "n_peso_invalido": n_peso_invalido,
                "n_remesas_invalido": n_r_invalido}
    masa_total = sum(v[2] for v in validos)
    masa_recept = sum(v[2] for v in validos if v[3] > 0)
    p = masa_recept / masa_total

    conglomerados = {}
    for est, upm, peso, remesa in validos:
        if est is None or upm is None:
            continue
        c = conglomerados.setdefault((est, upm), [0.0, 0.0])
        c[0] += peso
        c[1] += peso if remesa > 0 else 0.0
    ic = None
    if conglomerados:
        estratos = {}
        for (est, _upm), (w, wr) in conglomerados.items():
            estratos.setdefault(est, []).append((w, wr))
        bloques = [np.array(estratos[e], dtype=float) for e in sorted(estratos)]
        if bloques:
            rng = np.random.Generator(np.random.PCG64(seed))
            vals = []
            for _r in range(replicas):
                tot_w = tot_wr = 0.0
                for bloque in bloques:
                    k = bloque.shape[0]
                    idx = rng.integers(0, k, size=k)
                    tot_w += bloque[idx, 0].sum()
                    tot_wr += bloque[idx, 1].sum()
                vals.append(tot_wr / tot_w if tot_w > 0 else np.nan)
            vals = np.array(vals)
            fin = vals[np.isfinite(vals)]
            if fin.size:
                ic = (float(np.percentile(fin, 2.5)), float(np.percentile(fin, 97.5)))
    return {"estado": "REPORTADO", "p": p, "ic95": ic,
            "n_validos": len(validos), "n_peso_invalido": n_peso_invalido,
            "n_remesas_invalido": n_r_invalido,
            "masa_total": masa_total, "masa_receptores": masa_recept}


def nacional(marco: MarcoHogares) -> dict:
    """La única celda. Lanza ReservaRota si marco.reservada es True -- para
    una ola reservada, sólo emite_bajo_reserva() puede llegar aquí."""
    if marco.reservada:
        raise ReservaRota(
            "nacional() llamada directo sobre un marco reservada=True -- "
            "usa emite_bajo_reserva() desde un CALC de emisiones autorizado")
    return _calcula_nacional(marco)


def emite_bajo_reserva(marco: MarcoHogares, autoriza: bool) -> dict:
    """Único punto de entrada que puede levantar la reserva. Exige
    marco.reservada is True Y autoriza is True; cualquier otra combinacion
    es un error de programacion, no un permiso implicito."""
    if not marco.reservada:
        raise ValueError(
            "emite_bajo_reserva() sobre un marco reservada=False: no hace "
            "falta autorizar nada, llama a nacional() directo")
    if autoriza is not True:
        raise ReservaRota(
            "emite_bajo_reserva() sin autoriza=True explicito sobre una "
            "ola reservada")
    return _calcula_nacional(marco)
