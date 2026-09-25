#!/usr/bin/env python3
"""Piso C2 de `TRA.evade_norma.envipe2025.escolaridad_x_dominio`, re-medido desde microdato.

ACTO GEN2-PISOS-GEN2-2 (24/sep/2026, CAJA), P2. Contrato humano:
`forense/prereg-caja/ENVIPE2025-PISOS-EVADE-NORMA-SXD-spec-v1_0.md`, congelado en el
COMMIT-1 antes de ejecutar este archivo sobre ENVIPE 2025.

QUÉ CAMBIA RESPECTO DE LAS EMISIONES
------------------------------------
`CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` publica `-C2-P` compuesto con
`parametros.marginales_sellados` (seis decimales de
`milpa/tramite-ola5-propuesta-v0.yaml:1715-1731`; nacional de
`milpa/tramite.yaml:497`): cadena legacy (censo P1). Este CALC compone la MISMA
fórmula con los ocho marginales de UN eje de ENVIPE 2025 (4 escolaridad, 3
dominio, nacional) medidos desde el manifiesto (`envipe2025_csv`).

NO REIMPLEMENTA NADA
--------------------
Universo, ejes, punto, IC de cada marginal y réplicas compartidas salen del
módulo congelado `tools/celda_d/marginales_reproduccion.py` (input
`receta_marginales`, `funcion: CODIGO`), que carga la ola con `reservada=True`:
el cruce lanza `ReservaRota` y la guardia se prueba en cada corrida. Misma
semilla (42) y réplicas que las emisiones: su `-C2-P-REDERIVADO`, `-C2-IC95*` y
`-G-M25-MARG-*` sellados son el oro de este CALC a 1e-10 (control 1).
"""
from __future__ import annotations

import importlib.util
import json
import sys

import numpy as np

P = "RESULT-ENVIPE2025-PISOS-EVADE-NORMA-SXD"
PE = "RESULT-TRA-SXD12"
PA = "RESULT-ARBITRO-ENVIPE2025-EVASION"
GRUPOS = ["S1", "S2", "S3", "S4", "D1", "D2", "D3"]
ARBITRO = {"S1": "ESCOLARIDAD-HASTA-PRIMARIA", "S2": "ESCOLARIDAD-SECUNDARIA",
           "S3": "ESCOLARIDAD-MEDIA-SUPERIOR", "S4": "ESCOLARIDAD-SUPERIOR",
           "D1": "DOMINIO-RURAL", "D2": "DOMINIO-COMPLEMENTO-URBANO",
           "D3": "DOMINIO-URBANO", "NAC": "TOTAL-TODOS"}
INPUTS = frozenset({"envipe2025_csv", "receta_marginales", "ejes_l1",
                    "calibracion_ic", "funcion_c2", "emisiones_resultados",
                    "emisiones_sello", "arbitro_envipe2025_resultados",
                    "arbitro_envipe2025_sello"})


class ParoDeGuardia(RuntimeError):
    pass


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
    return str(resultados_inp["sha256"]) in json.dumps(_json(sello_inp))


def _pct(v, q):
    return float(np.percentile(v, q)) if len(v) else None


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    tol = float(par["tol_control_emisiones"])
    tol_arb = float(par["tol_control_arbitro"])
    out = {}

    for sello, res in (("emisiones_sello", "emisiones_resultados"),
                       ("arbitro_envipe2025_sello", "arbitro_envipe2025_resultados")):
        if not _sello_cubre(inputs[sello], inputs[res]):
            raise ParoDeGuardia(f"{res}: sha256 no registrado en {sello}")

    _c2 = _importa("test_celda_d_c2", inputs["funcion_c2"]["ruta_absoluta"])
    mr = _importa("marginales_reproduccion", inputs["receta_marginales"]["ruta_absoluta"])
    piso_log_aditivo, MarginalDegenerado = _c2.piso_log_aditivo, _c2.MarginalDegenerado
    celdas_c2 = list(mr.CELDAS)
    rot = {**{s: mr.ESC_ROTULO[s] for s in ("S1", "S2", "S3", "S4")},
           **{d: mr.DOM_ROTULO[d] for d in ("D1", "D2", "D3")}}

    out[f"{P}-G-INPUT-ENVIPE2025-CSV-SHA256"] = str(inputs["envipe2025_csv"]["sha256"])

    # ── ENVIPE 2025 · marginales de UN eje, ola cargada como RESERVADA ─────
    ola = mr.carga_ola(inputs["envipe2025_csv"]["ruta_absoluta"], 2025, reservada=True)
    m = ola.meta
    out[f"{P}-G-FILAS-ARCHIVO"] = int(m["filas_archivo"])
    out[f"{P}-G-FILAS-UNIVERSO"] = int(m["filas_universo"])
    out[f"{P}-G-ESCOLARIDAD-FUERA"] = int(m["escolaridad_fuera"])
    out[f"{P}-G-DOMINIO-FUERA"] = int(m["dominio_fuera"])
    out[f"{P}-G-ESTRATOS"] = int(m["estratos"])
    out[f"{P}-G-UPM"] = int(m["upm"])
    rep = mr.replicas_compartidas(ola, semilla, n_rep)
    marg = {e: mr.marginal(ola, e, replicas=rep)
            for e in ("escolaridad_proxy", "dominio_urbano_rural", "nacional")}
    cel = {g: marg["escolaridad_proxy" if g.startswith("S") else
                   "dominio_urbano_rural"]["celdas"][rot[g]] for g in GRUPOS}
    cel["NAC"] = marg["nacional"]["celdas"]["NAC"]
    for g in GRUPOS + ["NAC"]:
        c = cel[g]
        out[f"{P}-MARG-{g}-N"] = int(c["n"])
        out[f"{P}-MARG-{g}-P"] = c["p"]
        out[f"{P}-MARG-{g}-IC95INF"] = c["ic95"][0] if c["ic95"] else None
        out[f"{P}-MARG-{g}-IC95SUP"] = c["ic95"][1] if c["ic95"] else None
    try:
        mr.cruce(ola, "escolaridad_proxy", "dominio_urbano_rural")
        out[f"{P}-G-GUARDIA-CRUCE-DERIVADO"] = "SI"
        raise ParoDeGuardia("la ola reservada dejo cruzar: defecto de guardia")
    except mr.ReservaRota:
        out[f"{P}-G-GUARDIA-CRUCE-DERIVADO"] = "NO"

    # ── C2 · composición (misma fórmula y mismo código que las emisiones) ──
    def _mg(p):
        return {"desenlace_id": par["c2_desenlace_id"], "p": float(p)}

    c2p, c2lo, c2hi = {}, {}, {}
    no_constr, sin_def = 0, 0
    for c in celdas_c2:
        s, d = c.split("x")
        try:
            c2p[c] = float(piso_log_aditivo(_mg(cel[s]["p"]), _mg(cel[d]["p"]),
                                            _mg(cel["NAC"]["p"]))["p"])
        except (MarginalDegenerado, TypeError):
            c2p[c] = None
            no_constr += 1
        rs, rd, rn = cel[s]["replicas"], cel[d]["replicas"], cel["NAC"]["replicas"]
        ok = (np.isfinite(rs) & np.isfinite(rd) & np.isfinite(rn)
              & (rs > 0) & (rs < 1) & (rd > 0) & (rd < 1) & (rn > 0) & (rn < 1))
        sin_def += int((~ok).sum())
        with np.errstate(all="ignore"):
            lc2 = np.where(ok, np.log(rs / (1 - rs)) + np.log(rd / (1 - rd))
                           - np.log(rn / (1 - rn)), np.nan)
        c2r = 1.0 / (1.0 + np.exp(-lc2[ok]))
        c2lo[c], c2hi[c] = _pct(c2r, 2.5), _pct(c2r, 97.5)
    out[f"{P}-G-C2-CELDAS-NO-CONSTRUIBLES"] = no_constr
    out[f"{P}-G-C2-REPLICAS-SIN-DEFINIR"] = sin_def

    # ── control 1 · oro: las emisiones selladas (mismo módulo, misma semilla) ──
    emis = _json(inputs["emisiones_resultados"])
    peor, n_disc = 0.0, 0
    for g in GRUPOS:
        if int(emis[f"{PE}-G-M25-MARG-{g}-N"]) != out[f"{P}-MARG-{g}-N"]:
            n_disc += 1
        for suf in ("P", "IC95INF", "IC95SUP"):
            peor = max(peor, abs(float(emis[f"{PE}-G-M25-MARG-{g}-{suf}"])
                                 - float(out[f"{P}-MARG-{g}-{suf}"])))
    peor = max(peor, abs(float(emis[f"{PE}-G-M25-P-NACIONAL"]) - float(out[f"{P}-MARG-NAC-P"])))
    for c in celdas_c2:
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

    # ── control 2 · árbitro marginal ENVIPE 2025 (-P a tol, -N exacto) ─────
    arb = _json(inputs["arbitro_envipe2025_resultados"])
    peor_a, n_a = 0.0, 0
    for g in GRUPOS + ["NAC"]:
        dp = float(out[f"{P}-MARG-{g}-P"]) - float(arb[f"{PA}-{ARBITRO[g]}-P"])
        dn = int(out[f"{P}-MARG-{g}-N"]) - int(arb[f"{PA}-{ARBITRO[g]}-N"])
        out[f"{P}-G-CTRL-ARBITRO-{g}-DELTA-P"] = dp
        out[f"{P}-G-CTRL-ARBITRO-{g}-DELTA-N"] = dn
        peor_a = max(peor_a, abs(dp))
        n_a += int(dn != 0)
    out[f"{P}-G-CTRL-ARBITRO-MAX-ABS"] = float(peor_a)
    out[f"{P}-G-CTRL-ARBITRO-VEREDICTO"] = (
        "REPRODUCE" if (peor_a <= tol_arb and n_a == 0) else "NO-REPRODUCE")

    # ── control 3 · contra el C2 legacy (descriptivo, MIXTO) ───────────────
    peor_l = 0.0
    for c in celdas_c2:
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
    for c in celdas_c2:
        out[f"{P}-C2-P-{c}"] = c2p[c]
        out[f"{P}-C2-IC95INF-{c}"] = c2lo[c] if ic_ok else None
        out[f"{P}-C2-IC95SUP-{c}"] = c2hi[c] if ic_ok else None
    out[f"{P}-G-ORIGEN"] = (
        "NUEVO -- marginales de un eje medidos de envipe2025_csv (manifiesto); "
        "ningun numero de milpa/ alimenta el punto ni el IC")
    return out
