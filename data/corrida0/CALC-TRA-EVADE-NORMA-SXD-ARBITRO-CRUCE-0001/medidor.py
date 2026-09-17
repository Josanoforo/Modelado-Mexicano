#!/usr/bin/env python3
"""Medidor de `CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001` (`COMMIT-3`).

ACTO `GEN2-CELDA-D-PILOTO-2` v1.1. Contrato humano:
`forense/prereg-caja/TRA-evade-norma-sxd12-spec-v1_0.md` (§5, criterio escrito
antes del dato). Deriva `R` —las 12 celdas de ENVIPE 2025 con la receta del
árbitro— y adjudica contra las emisiones **ya selladas** en `COMMIT-2`
(`CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001`, input de repo por sha256).

Este es el primer código del acto que cruza ENVIPE 2025: la ola se carga con
`reservada=False`. El orden lo prueba el historial, no este archivo
(`NC-0313`): el directorio de este CALC no existe en ningún commit anterior
al `COMMIT-3`.

`R` usa `tools/celda_d/marginales_reproduccion.py::cruce`, cuyo punto e IC95
por celda salen de `wprop_ic_conglomerado` (la función del árbitro sellado;
`COMMIT-2` la reprodujo a 5e-7 en los ocho marginales).
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[3]


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


mr = _importa("marginales_reproduccion",
              RAIZ / "tools" / "celda_d" / "marginales_reproduccion.py")

P = "RESULT-TRA-SXD12-ARB"
PE = "RESULT-TRA-SXD12"
CELDAS = list(mr.CELDAS)
S_ROT, D_ROT = mr.ESC_ROTULO, mr.DOM_ROTULO
PISOS = ("C1", "C2")
CHALLENGERS = ("C6", "C7")
CANDIDATOS = ("C1", "C2", "C6", "C7")


def _dentro(p, lo, hi):
    return p is not None and lo <= p <= hi


def _signo(p_lo, p_hi, r, nac):
    """ESTABLE si todo el IC del candidato queda del mismo lado del nacional
    que R; AMBIGUA si el IC cruza el nacional; CONTRARIA si queda entero del
    lado opuesto. INDEFINIDO si R cae exactamente en el nacional."""
    if p_lo is None or p_hi is None or r is None:
        return "NO-ESTIMABLE"
    lado_r = np.sign(r - nac)
    if lado_r == 0:
        return "INDEFINIDO"
    if p_lo > nac and p_hi > nac:
        lado = 1
    elif p_lo < nac and p_hi < nac:
        lado = -1
    else:
        return "AMBIGUA"
    return "ESTABLE" if lado == lado_r else "CONTRARIA"


def medir(inputs, contrato):
    par = contrato["parametros"]
    umbral = int(par["umbral_soporte_n"])
    out = {}
    out[f"{P}-G-INPUT-ENVIPE2025-CSV-SHA256"] = str(inputs["envipe2025_csv"]["sha256"])
    out[f"{P}-G-INPUT-EMISIONES-SHA256"] = str(inputs["emisiones_selladas"]["sha256"])

    # ── emisiones selladas (COMMIT-2) ─────────────────────────────────────
    with open(inputs["emisiones_selladas"]["ruta_absoluta"], encoding="utf-8") as fh:
        raw = json.load(fh)
    emis = raw.get("resultados", raw) if isinstance(raw, dict) else raw
    if isinstance(emis, list):
        emis = {x["id"]: x["valor"] for x in emis}
    out[f"{P}-G-EMISIONES-CORRIDA-ID"] = str(par["emisiones_corrida_id"])
    out[f"{P}-G-EMISIONES-CTRL-ARBITRO-VEREDICTO"] = str(emis[f"{PE}-G-CTRL-ARBITRO-VEREDICTO"])
    out[f"{P}-G-EMISIONES-RESERVA-CRUCE-DERIVADO"] = str(emis[f"{PE}-G-RESERVA-CRUCE-2025-DERIVADO"])

    # ── R · las 12 celdas de ENVIPE 2025, receta del arbitro ──────────────
    ola = mr.carga_ola(inputs["envipe2025_csv"]["ruta_absoluta"], 2025, reservada=False)
    m = ola.meta
    out[f"{P}-G-R-FILAS-ARCHIVO"] = int(m["filas_archivo"])
    out[f"{P}-G-R-FILAS-UNIVERSO"] = int(m["filas_universo"])
    out[f"{P}-G-R-ESCOLARIDAD-FUERA"] = int(m["escolaridad_fuera"])
    out[f"{P}-G-R-DELITOS-SIN-PERSONA"] = int(m["delitos_sin_persona"])
    out[f"{P}-G-R-ESTRATOS"] = int(m["estratos"])
    out[f"{P}-G-R-UPM"] = int(m["upm"])
    nac = mr.marginal(ola, "nacional")["celdas"]["NAC"]
    out[f"{P}-G-R-P-NACIONAL"] = float(nac["p"])
    pnac_sellado = float(par["p_nacional_c5"])
    out[f"{P}-G-R-P-NACIONAL-DELTA-SELLADO"] = float(nac["p"]) - pnac_sellado
    x = mr.cruce(ola, "escolaridad_proxy", "dominio_urbano_rural")
    out[f"{P}-G-R-COBERTURA-CRUCE"] = float(x["cobertura"])

    R, EE, ICR = {}, {}, {}
    fuera25 = 0
    for c in CELDAS:
        s, d = c.split("x")
        cel = x["celdas"][(S_ROT[s], D_ROT[d])]
        out[f"{P}-R-N-{c}"] = int(cel["n"])
        out[f"{P}-R-NUM-{c}"] = int(cel["numerador"])
        sop = "SOPORTE-OK" if cel["n"] >= umbral else "FUERA-DE-SOPORTE"
        fuera25 += sop != "SOPORTE-OK"
        out[f"{P}-SOPORTE-2025-{c}"] = sop
        out[f"{P}-R-P-{c}"] = cel["p"]
        if cel["ic95"] is not None:
            lo, hi = float(cel["ic95"][0]), float(cel["ic95"][1])
            out[f"{P}-R-IC95INF-{c}"], out[f"{P}-R-IC95SUP-{c}"] = lo, hi
            out[f"{P}-R-EE-{c}"] = (hi - lo) / 3.92
            R[c], EE[c], ICR[c] = float(cel["p"]), (hi - lo) / 3.92, (lo, hi)
        else:
            out[f"{P}-R-IC95INF-{c}"] = out[f"{P}-R-IC95SUP-{c}"] = None
            out[f"{P}-R-EE-{c}"] = None
            R[c], EE[c], ICR[c] = None, None, None
    out[f"{P}-G-CELDAS-FUERA-DE-SOPORTE-2025"] = int(fuera25)

    # ── candidatos, desde el sello de COMMIT-2 ────────────────────────────
    cand = {k: {c: emis[f"{PE}-{k}-P-{c}"] for c in CELDAS} for k in CANDIDATOS}
    ic_c = {k: {c: (emis[f"{PE}-{k}-IC95INF-{c}"], emis[f"{PE}-{k}-IC95SUP-{c}"])
                for c in CELDAS} for k in CANDIDATOS}
    sop24 = {c: emis[f"{PE}-C1-SOPORTE-{c}"] for c in CELDAS}
    sop23 = {c: emis[f"{PE}-W23-SOPORTE-{c}"] for c in CELDAS}

    d_pp = {k: {} for k in CANDIDATOS}
    puntuadas = 0
    gana_ambos = {k: 0 for k in CHALLENGERS}
    indecid = {k: 0 for k in CHALLENGERS}
    fuera_alguna = 0
    signo_estable = {k: 0 for k in CANDIDATOS}
    for c in CELDAS:
        r = R[c]
        for k in CANDIDATOS:
            v = cand[k][c]
            d_pp[k][c] = (100.0 * abs(v - r)) if (v is not None and r is not None) else None
            out[f"{P}-D-{k}-{c}"] = d_pp[k][c]
            out[f"{P}-DENTRO-IC-R-{k}-{c}"] = (
                "SI" if (r is not None and _dentro(v, *ICR[c])) else "NO")
            sg = _signo(ic_c[k][c][0], ic_c[k][c][1], r, pnac_sellado)
            out[f"{P}-SIGNO-{k}-{c}"] = sg
            signo_estable[k] += sg == "ESTABLE"
        con_soporte = (out[f"{P}-SOPORTE-2025-{c}"] == "SOPORTE-OK"
                       and sop24[c] == "SOPORTE-OK" and sop23[c] == "SOPORTE-OK")
        fuera_alguna += not con_soporte
        puntuable = (r is not None and con_soporte
                     and all(cand[k][c] is not None for k in CANDIDATOS))
        out[f"{P}-PUNTUADA-{c}"] = "SI" if puntuable else "NO"
        if not puntuable:
            for ch in CHALLENGERS:
                for piso in PISOS:
                    out[f"{P}-VEREDICTO-{ch}-VS-{piso}-{c}"] = "NO-PUNTUADA"
                out[f"{P}-VEREDICTO-CELDA-{ch}-{c}"] = "NO-PUNTUADA"
            continue
        puntuadas += 1
        for ch in CHALLENGERS:
            vered = {}
            for piso in PISOS:
                dl, dm = d_pp[ch][c], d_pp[piso][c]
                ambos_dentro = (_dentro(cand[ch][c], *ICR[c])
                                and _dentro(cand[piso][c], *ICR[c]))
                cerca = abs(dl - dm) < 0.5 * (100.0 * EE[c])
                if ambos_dentro or cerca:          # precedencia: manda INDECIDIBLE
                    vered[piso] = "INDECIDIBLE"
                else:
                    vered[piso] = "GANA-CHALLENGER" if dl < dm else "GANA-PISO"
                out[f"{P}-VEREDICTO-{ch}-VS-{piso}-{c}"] = vered[piso]
            if all(v == "GANA-CHALLENGER" for v in vered.values()):
                gana_ambos[ch] += 1
                out[f"{P}-VEREDICTO-CELDA-{ch}-{c}"] = f"{ch}-VENCE-A-LOS-DOS-PISOS"
            elif any(v == "INDECIDIBLE" for v in vered.values()):
                indecid[ch] += 1
                out[f"{P}-VEREDICTO-CELDA-{ch}-{c}"] = "INDECIDIBLE"
            else:
                out[f"{P}-VEREDICTO-CELDA-{ch}-{c}"] = f"{ch}-NO-VENCE-A-LOS-DOS-PISOS"

    out[f"{P}-G-CELDAS-PUNTUADAS"] = int(puntuadas)
    out[f"{P}-G-CELDAS-FUERA-DE-SOPORTE-ALGUNA-OLA"] = int(fuera_alguna)
    for ch in CHALLENGERS:
        out[f"{P}-G-{ch}-GANA-A-AMBOS-PISOS"] = int(gana_ambos[ch])
        out[f"{P}-G-{ch}-INDECIDIBLES"] = int(indecid[ch])
    for k in CANDIDATOS:
        out[f"{P}-G-SIGNO-ESTABLE-{k}"] = int(signo_estable[k])

    def _mae(k):
        v = [d_pp[k][c] for c in CELDAS
             if out[f"{P}-PUNTUADA-{c}"] == "SI" and d_pp[k][c] is not None]
        return float(np.mean(v)) if v else None

    mae = {k: _mae(k) for k in CANDIDATOS}
    for k in CANDIDATOS:
        out[f"{P}-G-MAE-{k}"] = mae[k]
    for ch in CHALLENGERS:
        for piso in PISOS:
            out[f"{P}-G-SKILL-{ch}-VS-{piso}"] = (
                float(1.0 - mae[ch] / mae[piso])
                if (mae[ch] is not None and mae[piso]) else None)
    definidos = {k: v for k, v in mae.items() if v is not None}
    out[f"{P}-G-MEJOR-CANDIDATO-POR-MAE"] = (
        min(definidos, key=definidos.get) if definidos else "NO-ESTIMABLE")

    # ── parada, en el orden de la spec §5.5 ───────────────────────────────
    umbral_gana = int(par["umbral_celdas_gana"])
    umbral_punt = int(par["umbral_celdas_puntuadas"])
    ganadores = [ch for ch in CHALLENGERS
                 if puntuadas >= umbral_punt and gana_ambos[ch] >= umbral_gana]
    todas_indecidibles = puntuadas > 0 and all(
        out[f"{P}-VEREDICTO-CELDA-{ch}-{c}"] == "INDECIDIBLE"
        for ch in CHALLENGERS for c in CELDAS if out[f"{P}-PUNTUADA-{c}"] == "SI")
    if fuera_alguna >= int(par["umbral_fuera_de_soporte"]):
        veredicto = "FUERA-DE-SOPORTE"
    elif puntuadas < umbral_punt or todas_indecidibles:
        veredicto = "INDECIDIBLE"
    elif ganadores:
        veredicto = "ADJUDICADA"
    else:
        veredicto = "SIN-CANDIDATO-SUPERIOR"
    out[f"{P}-G-VEREDICTO-CELDA-D"] = veredicto
    out[f"{P}-G-CHALLENGER-GANADOR"] = (
        "NINGUNO" if not ganadores else
        ("AMBOS-DECIDE-MESA" if len(ganadores) == 2 else ganadores[0]))

    # ── B-bis, leido mecanicamente ────────────────────────────────────────
    vence = {ch: {piso: sum(1 for c in CELDAS
                            if out[f"{P}-VEREDICTO-{ch}-VS-{piso}-{c}"] == "GANA-CHALLENGER")
                  for piso in PISOS} for ch in CHALLENGERS}
    for ch in CHALLENGERS:
        for piso in PISOS:
            out[f"{P}-G-{ch}-VENCE-A-{piso}-EN-CELDAS"] = int(vence[ch][piso])
    nadie_c1 = all(vence[ch]["C1"] < umbral_gana for ch in CHALLENGERS)
    nadie_c2 = all(vence[ch]["C2"] < umbral_gana for ch in CHALLENGERS)
    lectura = []
    if nadie_c1:
        lectura.append("NADIE-VENCE-A-C1 -> " + par["b_bis_c1"])
    if nadie_c2:
        lectura.append("NADIE-VENCE-A-C2 -> " + par["b_bis_c2"])
    if ganadores:
        lectura.append("VENCE:" + "+".join(ganadores) + " -> " + par["b_bis_c6_c7"])
    if "C7" in ganadores and "C6" not in ganadores:
        lectura.append("C7-VENCE-Y-C6-NO -> " + par["b_bis_c7_no_c6"])
    out[f"{P}-G-B-BIS-LEIDO"] = " || ".join(lectura) if lectura else "NINGUNA-CLAUSULA-APLICA"
    out[f"{P}-G-CONDICION-INDECIDIBLE-VERBATIM"] = (
        par["criterio_indecidible_verbatim"] + "  [" + par["criterio_indecidible_fuente"] + "]")
    out[f"{P}-G-LIMITE-DE-LA-EVALUACION"] = par["limite_de_la_evaluacion"]
    out[f"{P}-G-CHAMPION"] = par["champion"]

    # ── C5 · diagnostico puro ─────────────────────────────────────────────
    dm_ = 0.0
    for c in CELDAS:
        v = (100.0 * abs(pnac_sellado - R[c])) if R[c] is not None else None
        out[f"{P}-C5-DIAG-{c}"] = v
        if v is not None:
            dm_ = max(dm_, v)
    out[f"{P}-G-C5-DIAG-MAX"] = float(dm_)
    return out
