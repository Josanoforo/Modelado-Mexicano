#!/usr/bin/env python3
"""Piso C2 de `DIN.ahorro_solo_informal.enif2024.localidad_x_edad`, re-medido desde microdato.

ACTO GEN2-PISOS-GEN2-2 (24/sep/2026, CAJA), P2. Contrato humano:
`forense/prereg-caja/ENIF2024-PISOS-AHORRO-INFORMAL-LXE-spec-v1_0.md`, congelado en el
COMMIT-1 antes de ejecutar este archivo sobre ENIF 2024.

QUÉ CAMBIA RESPECTO DE LAS EMISIONES
------------------------------------
`CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` publica `-C2-P` compuesto con
`parametros.marginales_sellados_D9`: seis decimales tecleados de
`milpa/tramite-ola5-propuesta-v0.yaml` y el nacional de `milpa/tramite.yaml`
(cadena legacy; censo P1). Este CALC compone la MISMA fórmula
(`piso_log_aditivo`, `expit(logit p(L) + logit p(E) - logit p)`) con los siete
marginales de UN eje de ENIF 2024 medidos desde el manifiesto (`enif2024_csv`).

NO REIMPLEMENTA NADA
--------------------
Lectura, universo, desenlace D9, bootstrap de conglomerados y agregación se
ejecutan desde los bytes del medidor sellado de las emisiones (input
`medidor_emisiones`, `funcion: CODIGO`), y `piso_log_aditivo` desde
`tests/test_celda_d_c2.py` (el mismo objeto que usaron las emisiones). Misma
semilla (42), mismas 10 000 réplicas, mismo orden de consumo: el
`-C2-P-REDERIVADO` y el `-C2-IC95*` sellados de las emisiones son el oro de este
CALC a 1e-10 (control 1).

GUARDIA: ninguna agrupación combina dos ejes; `_GUARDIA.cruce` se emite.
"""
from __future__ import annotations

import importlib.util
import json
import sys

import numpy as np

P = "RESULT-ENIF2024-PISOS-AHORRO-INFORMAL-LXE"
PE = "RESULT-DIN-LXE8"
PA = "RESULT-ARBITRO-ENIF2024-D9"
CELDAS = ["L1xE1", "L1xE2", "L1xE3", "L1xE4", "L2xE1", "L2xE2", "L2xE3", "L2xE4"]
GRUPOS = ["L1", "L2", "E1", "E2", "E3", "E4", "NAC"]
ARBITRO = {"L1": "LOCALIDAD-MENOR-DE-15-000", "L2": "LOCALIDAD-15-000-Y-MAS",
           "E1": "EDAD-18-29", "E2": "EDAD-30-44", "E3": "EDAD-45-59",
           "E4": "EDAD-60-MAS", "NAC": "TOTAL-TODOS"}
INPUTS = frozenset({"enif2024_csv", "medidor_emisiones", "funcion_c2",
                    "extrae_l", "emisiones_resultados", "emisiones_sello",
                    "arbitro_enif2024_resultados", "arbitro_enif2024_sello"})


class ParoDeGuardia(RuntimeError):
    pass


class _Guardia:
    def __init__(self):
        self.cruce = "NO"

    def registra(self, ejes):
        if len(ejes) > 1:
            self.cruce = "SI"
            raise ParoDeGuardia(f"agrupacion de {len(ejes)} ejes: {ejes}")


_GUARDIA = _Guardia()


def _importa(nombre, ruta):
    s = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(s)
    sys.modules[nombre] = m
    s.loader.exec_module(m)
    return m


def _guardia_inputs(inputs):
    fuera = sorted(set(inputs) - INPUTS)
    faltan = sorted(INPUTS - set(inputs))
    if fuera or faltan:
        raise ParoDeGuardia(f"inputs fuera de la lista {fuera} · faltan {faltan}")


def _json(inp):
    raw = inp.get("bytes")
    if raw is None:
        with open(inp["ruta_absoluta"], "rb") as fh:
            raw = fh.read()
    d = json.loads(raw.decode("utf-8"))
    return d.get("resultados", d)


def _sello_cubre(sello_inp, resultados_inp):
    """El sha256 del resultados.json de repo debe ser el que su sello registra."""
    sello = _json(sello_inp)
    texto = json.dumps(sello)
    return str(resultados_inp["sha256"]) in texto


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    tol = float(par["tol_control_emisiones"])
    tol_arb = float(par["tol_control_arbitro"])
    out = {}

    for sello, res in (("emisiones_sello", "emisiones_resultados"),
                       ("arbitro_enif2024_sello", "arbitro_enif2024_resultados")):
        if not _sello_cubre(inputs[sello], inputs[res]):
            raise ParoDeGuardia(f"{res}: sha256 no registrado en {sello}")

    _c2 = _importa("test_celda_d_c2", inputs["funcion_c2"]["ruta_absoluta"])
    _importa("extrae_l_v1_1", inputs["extrae_l"]["ruta_absoluta"])
    _E = _importa("medidor_emisiones_din", inputs["medidor_emisiones"]["ruta_absoluta"])
    piso_log_aditivo, MarginalDegenerado = _c2.piso_log_aditivo, _c2.MarginalDegenerado

    out[f"{P}-G-INPUT-ENIF2024-CSV-SHA256"] = str(inputs["enif2024_csv"]["sha256"])

    # ── ENIF 2024 · marginales de UN eje (bytes del medidor de las emisiones) ──
    inf24 = list(par["codigos_informal_2024"])
    f9_24 = list(par["codigos_formal_D9_2024"])
    cols24 = inf24 + f9_24 + ["tloc", "edad_v", "fac_per", "est_dis", "upm_dis"]
    df24, _m, _enc = _E._lee_miembro(inputs["enif2024_csv"]["ruta_absoluta"],
                                     "conjunto_de_datos_tmodulo_enif2024.csv", cols24)
    uni = _E._universo(df24, "edad_v", "tloc", "fac_per", inf24 + f9_24)
    u = uni["u"]
    out[f"{P}-G-FILAS-ARCHIVO"] = uni["n_archivo"]
    out[f"{P}-G-FILAS-UNIVERSO"] = uni["n_universo"]
    out[f"{P}-G-FILAS-EDAD-CENTINELA"] = uni["n_centinela"]

    des = _E._desenlaces(u, inf24, f9_24, f9_24)
    tloc = u["tloc"].str.strip().to_numpy()
    edad = u["_edad"].to_numpy()
    tr = par["edad_tramos"]
    agrup = [("L1", ["localidad"], np.isin(tloc, par["localidad_L1_tloc"])),
             ("L2", ["localidad"], np.isin(tloc, par["localidad_L2_tloc"]))]
    agrup += [(e, ["edad"], (edad >= tr[e][0]) & (edad <= tr[e][1]))
              for e in ("E1", "E2", "E3", "E4")]
    agrup.append(("NAC", [], np.ones(len(u), dtype=bool)))
    for _n, ejes, _mk in agrup:
        _GUARDIA.registra(ejes)
    grupos = [(n, mk) for n, _e, mk in agrup]

    est = u["est_dis"].str.strip().to_numpy()
    upm = u["upm_dis"].str.strip().to_numpy()
    claves = np.array([f"{a}\t{b}" for a, b in zip(est, upm)])
    counts, unicas, n_upm, _uu = _E._replicas(est, upm, semilla, n_rep)
    out[f"{P}-G-ESTRATOS"] = int(len(set(est)))
    out[f"{P}-G-UPM"] = int(n_upm)
    m = _E._matriz(grupos, [("D9", des["D9"])])
    W, Y = _E._agrega_por_upm(claves, unicas, u["_w"].to_numpy(), m)
    pt, lo, hi, reps = _E._punto_e_ic(counts, W, Y)
    ix = {n: g for g, (n, _mk) in enumerate(grupos)}
    for n, g in ix.items():
        out[f"{P}-MARG-{n}-N"] = int(grupos[g][1].sum())
        out[f"{P}-MARG-{n}-P"] = float(pt[g, 0])
        out[f"{P}-MARG-{n}-IC95INF"] = float(lo[g, 0])
        out[f"{P}-MARG-{n}-IC95SUP"] = float(hi[g, 0])
    out[f"{P}-G-GUARDIA-CRUCE-DERIVADO"] = _GUARDIA.cruce

    # ── C2 · composición (misma fórmula y mismo código que las emisiones) ──
    def _mg(p):
        return {"desenlace_id": _E.DESENLACE_D9, "p": float(p)}

    c2p, c2lo, c2hi = {}, {}, {}
    no_constr, sin_def = 0, 0
    for c in CELDAS:
        l, e = c.split("x")
        try:
            c2p[c] = float(piso_log_aditivo(_mg(pt[ix[l], 0]), _mg(pt[ix[e], 0]),
                                            _mg(pt[ix["NAC"], 0]))["p"])
        except MarginalDegenerado:
            c2p[c] = None
            no_constr += 1
        vals = []
        rl, re_, rn = reps[:, ix[l], 0], reps[:, ix[e], 0], reps[:, ix["NAC"], 0]
        for a, b, d in zip(rl, re_, rn):
            if not (0.0 < a < 1.0 and 0.0 < b < 1.0 and 0.0 < d < 1.0) \
                    or not (np.isfinite(a) and np.isfinite(b) and np.isfinite(d)):
                sin_def += 1
                continue
            vals.append(piso_log_aditivo(_mg(a), _mg(b), _mg(d))["p"])
        c2lo[c] = float(np.percentile(vals, 2.5)) if vals else None
        c2hi[c] = float(np.percentile(vals, 97.5)) if vals else None
    out[f"{P}-G-C2-CELDAS-NO-CONSTRUIBLES"] = no_constr
    out[f"{P}-G-C2-REPLICAS-SIN-DEFINIR"] = sin_def

    # ── control 1 · oro: las emisiones selladas (mismo código, misma semilla) ──
    emis = _json(inputs["emisiones_resultados"])
    peor, n_disc = 0.0, 0
    for n in GRUPOS:
        if int(emis[f"{PE}-G-C2-MARG-{n}-D9-N"]) != out[f"{P}-MARG-{n}-N"]:
            n_disc += 1
        for suf in ("P", "IC95INF", "IC95SUP"):
            peor = max(peor, abs(float(emis[f"{PE}-G-C2-MARG-{n}-D9-{suf}"])
                                 - out[f"{P}-MARG-{n}-{suf}"]))
    for c in CELDAS:
        for mio, suyo in ((c2p[c], emis[f"{PE}-C2-P-REDERIVADO-{c}"]),
                          (c2lo[c], emis[f"{PE}-C2-IC95INF-{c}"]),
                          (c2hi[c], emis[f"{PE}-C2-IC95SUP-{c}"])):
            if mio is None or suyo is None:
                n_disc += int((mio is None) != (suyo is None))
            else:
                peor = max(peor, abs(float(mio) - float(suyo)))
    out[f"{P}-G-CTRL-EMISIONES-MAX-ABS"] = float(peor)
    out[f"{P}-G-CTRL-EMISIONES-N-DISCORDA"] = int(n_disc)
    ctrl1 = "REPRODUCE" if (peor <= tol and n_disc == 0) else "NO-REPRODUCE"
    out[f"{P}-G-CTRL-EMISIONES-VEREDICTO"] = ctrl1

    # ── control 2 · árbitro marginal ENIF 2024 (universo propio; §3 de la spec) ──
    arb = _json(inputs["arbitro_enif2024_resultados"])
    peor_eq = 0.0
    n_eq_disc = 0
    for n in GRUPOS:
        dp = out[f"{P}-MARG-{n}-P"] - float(arb[f"{PA}-{ARBITRO[n]}-P"])
        dn = out[f"{P}-MARG-{n}-N"] - int(arb[f"{PA}-{ARBITRO[n]}-N"])
        out[f"{P}-G-CTRL-ARBITRO-{n}-DELTA-P"] = float(dp)
        out[f"{P}-G-CTRL-ARBITRO-{n}-DELTA-N"] = int(dn)
        if n in par["control_arbitro_mismo_universo"]:
            peor_eq = max(peor_eq, abs(dp))
            n_eq_disc += int(dn != 0)
    out[f"{P}-G-CTRL-ARBITRO-MISMO-UNIVERSO-MAX-ABS"] = float(peor_eq)
    out[f"{P}-G-CTRL-ARBITRO-VEREDICTO"] = (
        "REPRODUCE" if (peor_eq <= tol_arb and n_eq_disc == 0) else "NO-REPRODUCE")

    # ── control 3 · contra el C2 legacy (descriptivo, MIXTO) ───────────────
    peor_l = 0.0
    for c in CELDAS:
        leg = emis[f"{PE}-C2-P-{c}"]
        d = (c2p[c] - float(leg)) if (c2p[c] is not None and leg is not None) else None
        out[f"{P}-C2-DELTA-LEGACY-{c}"] = d
        if d is not None:
            peor_l = max(peor_l, abs(d))
    out[f"{P}-G-CTRL-C2-LEGACY-MAX-ABS"] = float(peor_l)

    # ── emisión del piso ───────────────────────────────────────────────────
    ic_ok = ctrl1 == "REPRODUCE" and sin_def == 0
    out[f"{P}-G-C2-IC-ESTADO"] = ("EMITIDO" if ic_ok else
                                  f"NO-EMITIDO -- control1={ctrl1} replicas_sin_definir={sin_def}")
    for c in CELDAS:
        out[f"{P}-C2-P-{c}"] = c2p[c]
        out[f"{P}-C2-IC95INF-{c}"] = c2lo[c] if ic_ok else None
        out[f"{P}-C2-IC95SUP-{c}"] = c2hi[c] if ic_ok else None
    out[f"{P}-G-ORIGEN"] = (
        "NUEVO -- marginales de un eje medidos de enif2024_csv (manifiesto); "
        "ningun numero de milpa/ alimenta el punto ni el IC")
    return out
