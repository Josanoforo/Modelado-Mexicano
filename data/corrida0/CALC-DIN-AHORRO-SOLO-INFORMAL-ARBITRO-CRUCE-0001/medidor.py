#!/usr/bin/env python3
"""Medidor de `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001` (`COMMIT-3`).

ACTO `GEN2-CELDA-D-PILOTO-1`. Contrato humano:
`forense/prereg-caja/DIN-ahorro-solo-informal-lxe8-spec-v1_2.md`.

**Aquí — y sólo aquí — se levanta la reserva.** Este es el commit en que el
cruce `localidad × edad` de ENIF 2024 se deriva. Las emisiones de los
candidatos ya estaban **selladas** cuando esto corrió
(`CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001--2053b255543c`, `COMMIT-2`,
con `RESULT-…-G-R-EXISTE-AL-CERRAR = "NO"` en su propio sello): el orden del
diff es el sello, y es auditable.

El medidor **reusa el motor de bootstrap del CALC de emisiones**, importándolo
por ruta: la misma función, la misma semilla, el mismo orden de consumo. `R` y
`C1` no pueden diferir por implementación.

`D9` (nueve tipos de cuenta) es el desenlace **primario**; `D7` (siete) se
emite como **sensibilidad que NO adjudica**.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[3]
EMISIONES = RAIZ / "data" / "corrida0" / "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001"

# El motor de medición del CALC de emisiones, importado por ruta y sin editar:
# misma lectura, mismo universo, mismo bootstrap, misma semilla.
_s = importlib.util.spec_from_file_location("medidor_emisiones",
                                            EMISIONES / "medidor.py")
_E = importlib.util.module_from_spec(_s)
sys.modules["medidor_emisiones"] = _E
_s.loader.exec_module(_E)

P = "RESULT-DIN-LXE8-ARB"
PE = "RESULT-DIN-LXE8"
CELDAS = ["L1xE1", "L1xE2", "L1xE3", "L1xE4", "L2xE1", "L2xE2", "L2xE3", "L2xE4"]


def _dentro(p, lo, hi):
    return p is not None and lo is not None and hi is not None and lo <= p <= hi


def medir(inputs, contrato):
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    umbral_n = int(par["umbral_soporte_n"])
    out = {}

    out[f"{P}-G-INPUT-ENIF2024-CSV-SHA256"] = str(inputs["enif2024_csv"]["sha256"])
    out[f"{P}-G-INPUT-EMISIONES-SHA256"] = str(inputs["emisiones_selladas"]["sha256"])
    emis = json.loads(inputs["emisiones_selladas"]["bytes"].decode("utf-8"))["resultados"]
    out[f"{P}-G-EMISIONES-CORRIDA-ID"] = json.loads(
        (EMISIONES / "ejecucion.json").read_text(encoding="utf-8"))["corrida_id"]

    # ── R · el cruce de ENIF 2024 ──────────────────────────────────────────
    inf = list(par["codigos_informal_2024"])
    f9 = list(par["codigos_formal_D9_2024"])
    f7 = list(par["codigos_formal_D7_2024"])
    cols = inf + f9 + ["tloc", "edad_v", "fac_per", "est_dis", "upm_dis"]
    df, _m, _e = _E._lee_miembro(inputs["enif2024_csv"]["ruta_absoluta"],
                                 "conjunto_de_datos_tmodulo_enif2024.csv", cols)
    uni = _E._universo(df, "edad_v", "tloc", "fac_per", inf + f9)
    u = uni["u"]
    out[f"{P}-G-R-FILAS-ARCHIVO"] = uni["n_archivo"]
    out[f"{P}-G-R-FILAS-UNIVERSO"] = uni["n_universo"]
    out[f"{P}-G-R-FILAS-EDAD-CENTINELA"] = uni["n_centinela"]
    out[f"{P}-G-R-COBERTURA-SIN-PONDERAR"] = uni["cobertura_sin_ponderar"]
    out[f"{P}-G-R-COBERTURA-PONDERADA"] = uni["cobertura_ponderada"]
    out[f"{P}-G-R-FILAS-CODIGO-FUERA-DE-DOMINIO"] = uni["filas_fuera_de_dominio"]

    des = _E._desenlaces(u, inf, f9, f7)
    tloc = u["tloc"].str.strip().to_numpy()
    edad = u["_edad"].to_numpy()
    tr = par["edad_tramos"]
    loc = {"L1": np.isin(tloc, par["localidad_L1_tloc"]),
           "L2": np.isin(tloc, par["localidad_L2_tloc"])}
    eda = {e: (edad >= tr[e][0]) & (edad <= tr[e][1]) for e in ("E1", "E2", "E3", "E4")}
    # AQUÍ se construye la llave (localidad, edad). Es el objeto de COMMIT-3.
    grupos = [(c, loc[c.split("x")[0]] & eda[c.split("x")[1]]) for c in CELDAS]
    grupos.append(("NACIONAL", np.ones(len(u), dtype=bool)))
    desen = [("D9", des["D9"]), ("D7", des["D7"])]

    est = u["est_dis"].str.strip().to_numpy()
    upm = u["upm_dis"].str.strip().to_numpy()
    claves = np.array([f"{a}\t{b}" for a, b in zip(est, upm)])
    counts, unicas, n_upm, upm_unica = _E._replicas(est, upm, semilla, n_rep)
    out[f"{P}-G-R-ESTRATOS"] = int(len(set(est)))
    out[f"{P}-G-R-UPM"] = int(n_upm)
    out[f"{P}-G-R-ESTRATOS-UPM-UNICA"] = int(upm_unica)

    m = _E._matriz(grupos, desen)
    W, Y = _E._agrega_por_upm(claves, unicas, u["_w"].to_numpy(), m)
    pt, lo_, hi_, _r = _E._punto_e_ic(counts, W, Y)

    monot = "VERIFICADA"
    brecha_max = 0.0
    fuera_soporte = 0
    R, EE, ICR = {}, {}, {}
    for g, c in enumerate(CELDAS):
        n_c = int(grupos[g][1].sum())
        out[f"{P}-R-D9-N-{c}"] = n_c
        if n_c < umbral_n:
            fuera_soporte += 1
        out[f"{P}-SOPORTE-2024-{c}"] = ("SOPORTE-OK" if n_c >= umbral_n
                                        else "FUERA-DE-SOPORTE")
        for d, etq in ((0, "D9"), (1, "D7")):
            v, a, b = pt[g, d], lo_[g, d], hi_[g, d]
            ok = n_c > 0 and np.isfinite(v)
            out[f"{P}-R-{etq}-P-{c}"] = float(v) if ok else None
            out[f"{P}-R-{etq}-IC95INF-{c}"] = float(a) if ok and np.isfinite(a) else None
            out[f"{P}-R-{etq}-IC95SUP-{c}"] = float(b) if ok and np.isfinite(b) else None
        if np.isfinite(pt[g, 0]) and np.isfinite(pt[g, 1]):
            brecha_max = max(brecha_max, abs(float(pt[g, 1]) - float(pt[g, 0])))
            if pt[g, 1] + 1e-12 < pt[g, 0]:
                monot = "VIOLADA"
        ee = (float(hi_[g, 0]) - float(lo_[g, 0])) / 3.92
        out[f"{P}-R-D9-EE-{c}"] = ee
        R[c] = float(pt[g, 0]) if np.isfinite(pt[g, 0]) else None
        EE[c] = ee
        ICR[c] = (float(lo_[g, 0]), float(hi_[g, 0]))
    out[f"{P}-G-R-MONOTONIA-D9-SUBSET-D7"] = monot
    out[f"{P}-G-BRECHA-D9-D7-MAX"] = float(brecha_max)
    out[f"{P}-G-CELDAS-FUERA-DE-SOPORTE-2024"] = fuera_soporte
    gn = len(CELDAS)
    out[f"{P}-G-R-P-NACIONAL-D9"] = float(pt[gn, 0])
    out[f"{P}-G-R-P-NACIONAL-D7"] = float(pt[gn, 1])

    # ── adjudicación por celda, con el criterio escrito antes del dato ─────
    cand = {
        "C1": {c: emis[f"{PE}-C1-D9-P-{c}"] for c in CELDAS},
        "C2": {c: emis[f"{PE}-C2-P-{c}"] for c in CELDAS},
        "C3": {c: emis[f"{PE}-C3-LSOLO-P-{c}"] for c in CELDAS},
    }
    sop21 = {c: emis[f"{PE}-C1-SOPORTE-{c}"] for c in CELDAS}

    d_abs = {k: {} for k in cand}
    puntuadas, gana_ambos, indecidibles = 0, 0, 0
    for c in CELDAS:
        r = R[c]
        for k in cand:
            v = cand[k][c]
            d_abs[k][c] = (abs(v - r) if (v is not None and r is not None) else None)
            out[f"{P}-D-{k}-{c}"] = d_abs[k][c]
        puntuable = (r is not None
                     and out[f"{P}-SOPORTE-2024-{c}"] == "SOPORTE-OK"
                     and sop21[c] == "SOPORTE-OK"
                     and all(cand[k][c] is not None for k in cand))
        out[f"{P}-PUNTUADA-{c}"] = "SI" if puntuable else "NO"
        if not puntuable:
            for piso in ("C1", "C2"):
                out[f"{P}-VEREDICTO-C3-VS-{piso}-{c}"] = "NO-PUNTUADA"
            out[f"{P}-VEREDICTO-CELDA-{c}"] = "NO-PUNTUADA"
            continue
        puntuadas += 1
        vered = {}
        for piso in ("C1", "C2"):
            dl, dm = d_abs["C3"][c], d_abs[piso][c]
            ambos_dentro = (_dentro(cand["C3"][c], *ICR[c])
                            and _dentro(cand[piso][c], *ICR[c]))
            cerca = abs(dl - dm) < 0.5 * EE[c]
            if ambos_dentro or cerca:          # precedencia: manda INDECIDIBLE
                vered[piso] = "INDECIDIBLE"
                indecidibles += 1
            else:
                vered[piso] = "GANA-CHALLENGER" if dl < dm else "GANA-PISO"
            out[f"{P}-VEREDICTO-C3-VS-{piso}-{c}"] = vered[piso]
        if all(v == "GANA-CHALLENGER" for v in vered.values()):
            gana_ambos += 1
            out[f"{P}-VEREDICTO-CELDA-{c}"] = "C3-VENCE-A-LOS-DOS-PISOS"
        elif any(v == "INDECIDIBLE" for v in vered.values()):
            out[f"{P}-VEREDICTO-CELDA-{c}"] = "INDECIDIBLE"
        else:
            out[f"{P}-VEREDICTO-CELDA-{c}"] = "C3-NO-VENCE-A-LOS-DOS-PISOS"

    out[f"{P}-G-CELDAS-PUNTUADAS"] = puntuadas
    out[f"{P}-G-C3-GANA-A-AMBOS-PISOS"] = gana_ambos
    out[f"{P}-G-C3-INDECIDIBLES"] = indecidibles

    def _mae(k):
        v = [d_abs[k][c] for c in CELDAS
             if out[f"{P}-PUNTUADA-{c}"] == "SI" and d_abs[k][c] is not None]
        return float(np.mean(v)) if v else float("nan")

    mae = {k: _mae(k) for k in cand}
    for k in cand:
        out[f"{P}-G-MAE-{k}"] = mae[k]
    for piso in ("C1", "C2"):
        out[f"{P}-G-SKILL-C3-VS-{piso}"] = float(1.0 - mae["C3"] / mae[piso])

    # ── parada, con las cuatro salidas admisibles y sin ganador forzado ────
    if fuera_soporte >= 3:
        veredicto = "FUERA-DE-SOPORTE"
    elif puntuadas < int(par["umbral_celdas_puntuadas"]):
        veredicto = "INDECIDIBLE"
    elif gana_ambos >= int(par["umbral_celdas_gana"]):
        veredicto = "ADJUDICADA"
    elif indecidibles > 0 and gana_ambos == 0 and all(
            out[f"{P}-VEREDICTO-CELDA-{c}"] == "INDECIDIBLE"
            for c in CELDAS if out[f"{P}-PUNTUADA-{c}"] == "SI"):
        veredicto = "INDECIDIBLE"
    else:
        veredicto = "SIN-CANDIDATO-SUPERIOR"
    out[f"{P}-G-VEREDICTO-CELDA-D"] = veredicto
    out[f"{P}-G-B-BIS-C1"] = par["b_bis_c1"]
    out[f"{P}-G-B-BIS-C2"] = par["b_bis_c2"]
    out[f"{P}-G-CONDICION-INDECIDIBLE-VERBATIM"] = (
        par["criterio_indecidible_verbatim"] + "  ["
        + par["criterio_indecidible_fuente"] + "]")
    out[f"{P}-G-LIMITE-DE-LA-EVALUACION"] = par["limite_de_la_evaluacion"]
    out[f"{P}-G-CHAMPION"] = par["champion"]

    # ── C5 · diagnóstico puro ──────────────────────────────────────────────
    pnac = float(par["p_nacional_c5"])
    dm_ = 0.0
    for c in CELDAS:
        v = abs(pnac - R[c]) if R[c] is not None else None
        out[f"{P}-C5-DIAG-{c}"] = v
        if v is not None:
            dm_ = max(dm_, v)
    out[f"{P}-G-C5-DIAG-MAX"] = float(dm_)
    return out
