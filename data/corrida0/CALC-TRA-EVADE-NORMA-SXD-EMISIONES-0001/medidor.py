#!/usr/bin/env python3
"""Medidor de `CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001` (`COMMIT-2`).

ACTO `GEN2-CELDA-D-PILOTO-2` v1.1 (relanzamiento, 17/sep/2026). Contrato
humano: `forense/prereg-caja/TRA-evade-norma-sxd12-spec-v1_0.md`, congelado
en `COMMIT-1` antes de abrir microdato, junto con este archivo. Firmas 1 y 2
de mesa (17/sep/2026), verbatim en el encargo archivado.

Interfaz estable del plan v2.0 §4 (B-1): `medir(inputs, contrato) -> dict`.
El medidor no abre `spec.yaml`: recibe el contrato normalizado.

QUÉ ABRE, Y QUÉ NO
------------------
  · **ENVIPE 2024, entera** — ola de desarrollo: `C1` (el cruce
    `escolaridad_proxy × dominio_urbano_rural`), `I₂₄`, `n₂₀₂₄` de soporte.
  · **ENVIPE 2023, entera** — insumo de `C7`: el cruce y `I₂₃`.
  · **ENVIPE 2025, SÓLO marginales de UN EJE** — `escolaridad_proxy`,
    `dominio_urbano_rural`, `nacional`. Alimentan el IC de `C2` por réplicas
    compartidas y el control de reproducción del árbitro sellado.

GUARDIA DE RESERVA, mecánica y no promesa
-----------------------------------------
Todo lo que toca ENVIPE 2025 pasa por
`tools/celda_d/marginales_reproduccion.py` (congelado en `COMMIT-1`): la ola
se carga con `reservada=True` (parámetro `ola_reservada` del contrato),
`marginal(ola, grupo: str)` sólo admite UN eje por firma, la ola se re-huella
en cada llamada y `cruce()` LANZA `ReservaRota` sobre una ola reservada. Este
medidor lo PRUEBA en cada corrida —intenta el cruce y registra que la guardia
lo rechazó— y lo emite como `RESULT-…-G-RESERVA-CRUCE-2025-DERIVADO`. Ese
RESULT es función del código, no del árbol (lección `NC-0313`): replica.

`C2` NO REIMPLEMENTA SU FÓRMULA: importa `piso_log_aditivo` de
`tests/test_celda_d_c2.py` (contrato pinado con fixtures sintéticos).
"""
from __future__ import annotations

import importlib.util
import math
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
_c2 = _importa("test_celda_d_c2", RAIZ / "tests" / "test_celda_d_c2.py")
piso_log_aditivo = _c2.piso_log_aditivo
MarginalDegenerado = _c2.MarginalDegenerado

P = "RESULT-TRA-SXD12"
CELDAS = list(mr.CELDAS)                         # S1xD1 … S4xD3
S_ROT, D_ROT = mr.ESC_ROTULO, mr.DOM_ROTULO      # S1 -> "hasta primaria", …
GRUPOS = ["S1", "S2", "S3", "S4", "D1", "D2", "D3"]
DESENLACE_ID = "evade_norma::BP1_20==2 AND BP1_23 in {04,05,06,08}"
ROTULO_SUPUESTO = "ausencia de interaccion en escala logit"


def _logit(p):
    return math.log(p / (1.0 - p))


def _expit(z):
    return 1.0 / (1.0 + math.exp(-z))


def _abierto(p):
    return p is not None and np.isfinite(p) and 0.0 < p < 1.0


def _pct(v, q):
    return float(np.percentile(v, q)) if len(v) else None


def _marg(p):
    return {"desenlace_id": DESENLACE_ID, "p": float(p)}


def _celda_de(c):
    s, d = c.split("x")
    return S_ROT[s], D_ROT[d]


def _grupo_rotulo(g):
    return S_ROT[g] if g.startswith("S") else D_ROT[g]


def _eje_de(g):
    return "escolaridad_proxy" if g.startswith("S") else "dominio_urbano_rural"


def _emite_ola(out, w, ola, rep):
    m = ola.meta
    out[f"{P}-G-{w}-FILAS-ARCHIVO"] = int(m["filas_archivo"])
    out[f"{P}-G-{w}-FILAS-UNIVERSO"] = int(m["filas_universo"])
    out[f"{P}-G-{w}-FILAS-BP1_20-FUERA"] = int(m["filas_bp1_20_fuera"])
    out[f"{P}-G-{w}-DELITOS-SIN-PERSONA"] = int(m["delitos_sin_persona"])
    out[f"{P}-G-{w}-ESCOLARIDAD-FUERA"] = int(m["escolaridad_fuera"])
    out[f"{P}-G-{w}-DOMINIO-FUERA"] = int(m["dominio_fuera"])
    out[f"{P}-G-{w}-BP1_23-VACIO-EN-NO-DENUNCIA"] = int(m["bp1_23_vacio_en_no_denuncia"])
    out[f"{P}-G-{w}-NUMERADOR"] = int(m["numerador"])
    out[f"{P}-G-{w}-ESTRATOS"] = int(m["estratos"])
    out[f"{P}-G-{w}-UPM"] = int(m["upm"])
    out[f"{P}-G-{w}-ESTRATOS-UPM-UNICA"] = int(rep.estratos_upm_unica)
    out[f"{P}-G-{w}-ENCODING-TMODVIC"] = str(m["encoding_tmod_vic"])
    out[f"{P}-G-{w}-COBERTURA-ESCOLARIDAD"] = (
        1.0 - m["escolaridad_fuera"] / m["filas_universo"]) if m["filas_universo"] else 0.0


def _emite_marginales(out, w, marg):
    """`marg` = {eje: resultado de marginal()}. Emite las 7 celdas de eje y el
    nacional; devuelve {grupo: celda} para uso interno (con réplicas)."""
    celdas = {}
    for g in GRUPOS:
        c = marg[_eje_de(g)]["celdas"][_grupo_rotulo(g)]
        celdas[g] = c
        out[f"{P}-G-{w}-MARG-{g}-N"] = int(c["n"])
        out[f"{P}-G-{w}-MARG-{g}-P"] = c["p"]
        out[f"{P}-G-{w}-MARG-{g}-IC95INF"] = c["ic95"][0] if c["ic95"] else None
        out[f"{P}-G-{w}-MARG-{g}-IC95SUP"] = c["ic95"][1] if c["ic95"] else None
    nac = marg["nacional"]["celdas"]["NAC"]
    celdas["NAC"] = nac
    out[f"{P}-G-{w}-P-NACIONAL"] = nac["p"]
    return celdas


def _interaccion(cruce_w, celdas_w):
    """I(s,d) = logit p(s,d) − [logit p(s) + logit p(d) − logit p], punto y
    réplica a réplica sobre el MISMO remuestreo de la ola. Devuelve
    {celda: (punto | None, replicas ndarray | None, n_sin_definir)}."""
    res = {}
    for c in CELDAS:
        s, d = c.split("x")
        cel = cruce_w["celdas"][_celda_de(c)]
        ps, pd_, pn = celdas_w[s], celdas_w[d], celdas_w["NAC"]
        punto = None
        if all(_abierto(x["p"]) for x in (cel, ps, pd_, pn)):
            punto = (_logit(cel["p"])
                     - (_logit(ps["p"]) + _logit(pd_["p"]) - _logit(pn["p"])))
        reps, sin_def = None, 0
        if cel["replicas"] is not None:
            a, b, e, f = (cel["replicas"], ps["replicas"], pd_["replicas"],
                          pn["replicas"])
            ok = (np.isfinite(a) & np.isfinite(b) & np.isfinite(e) & np.isfinite(f)
                  & (a > 0) & (a < 1) & (b > 0) & (b < 1)
                  & (e > 0) & (e < 1) & (f > 0) & (f < 1))
            sin_def = int((~ok).sum())
            with np.errstate(all="ignore"):
                la, lb, le, lf = (np.log(a / (1 - a)), np.log(b / (1 - b)),
                                  np.log(e / (1 - e)), np.log(f / (1 - f)))
            reps = np.where(ok, la - (lb + le - lf), np.nan)
        res[c] = (punto, reps, sin_def)
    return res


def medir(inputs, contrato):
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    umbral = int(par["umbral_soporte_n"])
    ola_reservada = int(par["ola_reservada"])
    out = {}

    for iid, clave in (("envipe2023_csv", "ENVIPE2023-CSV"),
                       ("envipe2024_csv", "ENVIPE2024-CSV"),
                       ("envipe2025_csv", "ENVIPE2025-CSV"),
                       ("envipe2023_fd_pdf", "ENVIPE2023-FD"),
                       ("envipe2024_fd_pdf", "ENVIPE2024-FD"),
                       ("envipe2025_fd_pdf", "ENVIPE2025-FD")):
        out[f"{P}-G-INPUT-{clave}-SHA256"] = str(inputs[iid]["sha256"])

    # ── 2024 · ola de desarrollo: cruce completo, marginales, I₂₄ ─────────
    ola24 = mr.carga_ola(inputs["envipe2024_csv"]["ruta_absoluta"], 2024,
                         reservada=False)
    rep24 = mr.replicas_compartidas(ola24, semilla, n_rep)
    _emite_ola(out, "W24", ola24, rep24)
    marg24 = {e: mr.marginal(ola24, e, replicas=rep24) for e in mr.EJES}
    cel24 = _emite_marginales(out, "W24", marg24)
    x24 = mr.cruce(ola24, "escolaridad_proxy", "dominio_urbano_rural",
                   replicas=rep24)
    out[f"{P}-G-COBERTURA-CRUCE-2024"] = float(x24["cobertura"])

    # ── 2023 · insumo de C7: cruce, marginales, I₂₃ ───────────────────────
    ola23 = mr.carga_ola(inputs["envipe2023_csv"]["ruta_absoluta"], 2023,
                         reservada=False)
    rep23 = mr.replicas_compartidas(ola23, semilla, n_rep)
    _emite_ola(out, "W23", ola23, rep23)
    marg23 = {e: mr.marginal(ola23, e, replicas=rep23) for e in mr.EJES}
    cel23 = _emite_marginales(out, "W23", marg23)
    x23 = mr.cruce(ola23, "escolaridad_proxy", "dominio_urbano_rural",
                   replicas=rep23)
    out[f"{P}-G-COBERTURA-CRUCE-2023"] = float(x23["cobertura"])

    # ── 2025 · RESERVADA: sólo marginales de UN eje, por el módulo congelado ─
    ola25 = mr.carga_ola(inputs["envipe2025_csv"]["ruta_absoluta"],
                         ola_reservada, reservada=True)
    rep25 = mr.replicas_compartidas(ola25, semilla, n_rep)
    _emite_ola(out, "M25", ola25, rep25)
    marg25 = {e: mr.marginal(ola25, e, replicas=rep25) for e in mr.EJES}
    cel25 = _emite_marginales(out, "M25", marg25)
    out[f"{P}-G-RESERVA-OLA"] = str(ola_reservada)
    # La guardia se PRUEBA, no se promete: el cruce sobre la ola reservada
    # tiene que ser rechazado por el módulo congelado.
    try:
        mr.cruce(ola25, "escolaridad_proxy", "dominio_urbano_rural")
        derivado, guardia = "SI", "NO-LANZO -- DEFECTO"
    except mr.ReservaRota as exc:
        derivado, guardia = "NO", f"ReservaRota: {exc}"
    out[f"{P}-G-RESERVA-CRUCE-2025-DERIVADO"] = derivado
    out[f"{P}-G-RESERVA-GUARDIA-PROBADA"] = guardia

    # ── control de reproducción del árbitro sellado (2025) ────────────────
    sell = par["marginales_sellados"]
    tol_p, tol_ic = float(par["control_arbitro_tol_p"]), float(par["control_arbitro_tol_ic"])
    peor_p, peor_ic = 0.0, 0.0
    for g in GRUPOS + ["NAC"]:
        c, s = cel25[g], sell[g]
        d_p = float(c["p"]) - float(s["p"])
        out[f"{P}-G-CTRL-ARBITRO-{g}-DELTA-P"] = d_p
        out[f"{P}-G-CTRL-ARBITRO-{g}-DELTA-N"] = int(c["n"]) - int(s["n"])
        d_lo = float(c["ic95"][0]) - float(s["ic95"][0])
        d_hi = float(c["ic95"][1]) - float(s["ic95"][1])
        out[f"{P}-G-CTRL-ARBITRO-{g}-DELTA-IC95INF"] = d_lo
        out[f"{P}-G-CTRL-ARBITRO-{g}-DELTA-IC95SUP"] = d_hi
        peor_p = max(peor_p, abs(d_p))
        peor_ic = max(peor_ic, abs(d_lo), abs(d_hi))
    out[f"{P}-G-CTRL-ARBITRO-DELTA-P-MAX"] = float(peor_p)
    out[f"{P}-G-CTRL-ARBITRO-DELTA-IC-MAX"] = float(peor_ic)
    out[f"{P}-G-CTRL-ARBITRO-VEREDICTO"] = (
        "REPRODUCE" if (peor_p <= tol_p and peor_ic <= tol_ic) else "NO-REPRODUCE")

    # ── C1 · persistencia del cruce 2024 · soporte ────────────────────────
    fuera24, fuera23 = 0, 0
    for c in CELDAS:
        cel = x24["celdas"][_celda_de(c)]
        out[f"{P}-C1-N-{c}"] = int(cel["n"])
        out[f"{P}-C1-NUM-{c}"] = int(cel["numerador"])
        sop = "SOPORTE-OK" if cel["n"] >= umbral else "FUERA-DE-SOPORTE"
        fuera24 += sop != "SOPORTE-OK"
        out[f"{P}-C1-SOPORTE-{c}"] = sop
        out[f"{P}-C1-P-{c}"] = cel["p"]
        r = cel["replicas"]
        ok = r[np.isfinite(r)] if r is not None else np.array([])
        out[f"{P}-C1-IC95INF-{c}"] = _pct(ok, 2.5)
        out[f"{P}-C1-IC95SUP-{c}"] = _pct(ok, 97.5)

        cel3 = x23["celdas"][_celda_de(c)]
        out[f"{P}-W23-N-{c}"] = int(cel3["n"])
        sop3 = "SOPORTE-OK" if cel3["n"] >= umbral else "FUERA-DE-SOPORTE"
        fuera23 += sop3 != "SOPORTE-OK"
        out[f"{P}-W23-SOPORTE-{c}"] = sop3
        out[f"{P}-W23-P-{c}"] = cel3["p"]
        r3 = cel3["replicas"]
        ok3 = r3[np.isfinite(r3)] if r3 is not None else np.array([])
        out[f"{P}-W23-IC95INF-{c}"] = _pct(ok3, 2.5)
        out[f"{P}-W23-IC95SUP-{c}"] = _pct(ok3, 97.5)
    out[f"{P}-G-C1-CELDAS-FUERA-DE-SOPORTE-2024"] = int(fuera24)
    out[f"{P}-G-W23-CELDAS-FUERA-DE-SOPORTE"] = int(fuera23)

    # ── interacciones por ola ─────────────────────────────────────────────
    i24 = _interaccion(x24, cel24)
    i23 = _interaccion(x23, cel23)
    for c in CELDAS:
        for w, ii in (("I24", i24), ("I23", i23)):
            punto, reps, _sd = ii[c]
            out[f"{P}-{w}-{c}"] = punto
            ok = reps[np.isfinite(reps)] if reps is not None else np.array([])
            out[f"{P}-{w}-IC95INF-{c}"] = _pct(ok, 2.5)
            out[f"{P}-{w}-IC95SUP-{c}"] = _pct(ok, 97.5)

    # ── C2 · piso log-aditivo sobre los marginales SELLADOS de 2025 ───────
    no_constr, sin_def_c2, sin_def_c6, sin_def_c7 = 0, 0, 0, 0
    for c in CELDAS:
        s, d = c.split("x")
        try:
            p_c2 = piso_log_aditivo(_marg(sell[s]["p"]), _marg(sell[d]["p"]),
                                    _marg(sell["NAC"]["p"]))["p"]
        except MarginalDegenerado:
            p_c2 = None
            no_constr += 1
        out[f"{P}-C2-P-{c}"] = float(p_c2) if p_c2 is not None else None
        try:
            out[f"{P}-C2-P-REDERIVADO-{c}"] = float(piso_log_aditivo(
                _marg(cel25[s]["p"]), _marg(cel25[d]["p"]),
                _marg(cel25["NAC"]["p"]))["p"])
        except MarginalDegenerado:
            out[f"{P}-C2-P-REDERIVADO-{c}"] = None

        rs, rd, rn = (cel25[s]["replicas"], cel25[d]["replicas"],
                      cel25["NAC"]["replicas"])
        ok = (np.isfinite(rs) & np.isfinite(rd) & np.isfinite(rn)
              & (rs > 0) & (rs < 1) & (rd > 0) & (rd < 1) & (rn > 0) & (rn < 1))
        sin_def_c2 += int((~ok).sum())
        with np.errstate(all="ignore"):
            lc2 = np.where(ok, np.log(rs / (1 - rs)) + np.log(rd / (1 - rd))
                           - np.log(rn / (1 - rn)), np.nan)
        c2r = 1.0 / (1.0 + np.exp(-lc2[ok]))
        out[f"{P}-C2-IC95INF-{c}"] = _pct(c2r, 2.5)
        out[f"{P}-C2-IC95SUP-{c}"] = _pct(c2r, 97.5)

        # ── C6 · logit C2 + I₂₄ · réplica k de 2025 con réplica k de 2024 ─
        p24, r24, _ = i24[c]
        p23, r23, _ = i23[c]
        if p_c2 is not None and p24 is not None:
            out[f"{P}-C6-P-{c}"] = _expit(_logit(p_c2) + p24)
        else:
            out[f"{P}-C6-P-{c}"] = None
        if r24 is not None:
            ok6 = ok & np.isfinite(r24)
            sin_def_c6 += int((~ok6).sum())
            c6r = 1.0 / (1.0 + np.exp(-(lc2[ok6] + r24[ok6])))
        else:
            sin_def_c6 += n_rep
            c6r = np.array([])
        out[f"{P}-C6-IC95INF-{c}"] = _pct(c6r, 2.5)
        out[f"{P}-C6-IC95SUP-{c}"] = _pct(c6r, 97.5)

        # ── C7 · logit C2 + (I₂₃ + I₂₄)/2 · réplica k de las tres olas ────
        if p_c2 is not None and p24 is not None and p23 is not None:
            out[f"{P}-C7-P-{c}"] = _expit(_logit(p_c2) + 0.5 * (p23 + p24))
        else:
            out[f"{P}-C7-P-{c}"] = None
        if r24 is not None and r23 is not None:
            ok7 = ok & np.isfinite(r24) & np.isfinite(r23)
            sin_def_c7 += int((~ok7).sum())
            c7r = 1.0 / (1.0 + np.exp(-(lc2[ok7] + 0.5 * (r23[ok7] + r24[ok7]))))
        else:
            sin_def_c7 += n_rep
            c7r = np.array([])
        out[f"{P}-C7-IC95INF-{c}"] = _pct(c7r, 2.5)
        out[f"{P}-C7-IC95SUP-{c}"] = _pct(c7r, 97.5)

    out[f"{P}-G-C2-DESENLACE-ID"] = DESENLACE_ID
    out[f"{P}-G-C2-ROTULO-SUPUESTO"] = ROTULO_SUPUESTO
    out[f"{P}-G-C2-FORMA"] = "expit(logit p25(s) + logit p25(d) - logit p25)"
    out[f"{P}-G-C2-ESTADO"] = ("PISO-ADMISIBLE" if no_constr == 0
                               else "DIAGNOSTICO-POR-REPLIEGUE")
    out[f"{P}-G-C2-CELDAS-NO-CONSTRUIBLES"] = int(no_constr)
    out[f"{P}-G-C2-REPLICAS-SIN-DEFINIR"] = int(sin_def_c2)
    out[f"{P}-G-C6-REPLICAS-SIN-DEFINIR"] = int(sin_def_c6)
    out[f"{P}-G-C7-REPLICAS-SIN-DEFINIR"] = int(sin_def_c7)
    out[f"{P}-G-C6-FORMA"] = "expit(logit C2 + I24(s,d))"
    out[f"{P}-G-C7-FORMA"] = "expit(logit C2 + (I23(s,d) + I24(s,d))/2)"
    out[f"{P}-G-INCERTIDUMBRE"] = (
        "IC95 percentil 2.5/97.5 de replicas bootstrap de conglomerado "
        "estratificado, UN remuestreo por ola compartido por todos sus grupos; "
        "C6/C7 combinan la replica k de cada ola (muestras independientes), sin "
        "covarianzas inventadas")

    # ── C4 · INEJECUTABLE · C5 · NO-APLICA ────────────────────────────────
    out[f"{P}-G-C4-ESTADO"] = (
        "INEJECUTABLE -- la matriz B*theta(x) -> h_r no puede emitir: faltantes "
        "con nombre. Bajo ADR-531 compite si puede; no puede.")
    out[f"{P}-G-C4-FALTANTES"] = " | ".join(par["c4_faltantes"])
    out[f"{P}-G-C5-ESTADO"] = (
        "NO-APLICA -- el emisor es el arbitro con otro nombre; " + par["c5_cita"])
    out[f"{P}-G-C5-P-NACIONAL"] = float(par["p_nacional_c5"])
    out[f"{P}-G-L-ESTADO"] = "NO-ENTRA -- por firma de mesa (Firma 1: `Sin L`)"
    return out
