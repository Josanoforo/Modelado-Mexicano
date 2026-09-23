#!/usr/bin/env python3
"""Medidor de `CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001` (`COMMIT-2`).

ACTO `GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1`. Contrato humano:
`forense/prereg-caja/TRA-evade-norma-cruces-encogida-spec-v1_0.md`, congelado
en `COMMIT-1` antes de abrir microdato, junto con este archivo. Firmas de
mesa `FP-260922-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-a5a0-01` (§2) y `-a5a0-02`
(§6), verbatim en `forense/firmas-pendientes.tsv`.

QUÉ ABRE, Y QUÉ NO
------------------
  · **ENVIPE 2024, entera** — ola de desarrollo: `C1` (persistencia) para
    los cuatro cruces, `I₂₄`, `n₂₀₂₄` de soporte.
  · **ENVIPE 2023, entera** — insumo de `C7`/`C-ENCOGIDA`: `I₂₃`.
  · **ENVIPE 2025 — SÓLO marginales de UN eje**, igual que el piloto 2: se
    abre con `reservada=True` (la guardia bloquea el CRUCE, no el
    marginal) para obtener las réplicas bootstrap que `C2`/`C7`/
    `C-ENCOGIDA` necesitan réplica a réplica; el PUNTO de cada marginal se
    contrasta contra el ya SELLADO en
    `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001/resultados.json` (input de
    repo, sha256 pinado) como control de reproducción — el mismo mecanismo
    que `TRA-evade-norma-sxd12` (piloto 2) usó para su propio `C2`.

GUARDIA DE RESERVA, mecánica y no promesa
-----------------------------------------
Todo lo que toca 2025 pasa por `tools/celda_d/marginales_reproduccion.py`
(congelado, no se edita aquí). El cruce de 2025 vive únicamente en
`CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001` (`COMMIT-3`).
Este medidor prueba la guardia en cada corrida: intenta `mr.cruce()` sobre
la ola 2025 y registra que la guardia lo rechazó.

Cuatro cruces, cuatro candidatos: `C1` (persistencia 2024), `C2` (marginales
2025 sin interacción), `C7` (interacción promediada 2023-24, sin encoger),
`C-ENCOGIDA` (misma interacción, encogida por `λ_cruce` -- método de
momentos Empirical-Bayes, UNA λ por cruce, spec §2.1, derivada aquí mismo
de `I₂₃`/`I₂₄`: ningún CALC histórico previo midió estos cuatro cruces).
No hay `C6`. `L` no entra (firma §2, "sin L").
"""
from __future__ import annotations

import importlib.util
import json
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

P = "RESULT-TRA-ENCOGIDA"
DESENLACE_ID = "evade_norma::BP1_20==2 AND BP1_23 in {04,05,06,08}"

FP_A = "FP-260922-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-a5a0-01"
FP_B = "FP-260922-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-a5a0-02"

# ── los cuatro cruces, y sus rótulos cortos ──────────────────────────────
CRUCES = {
    "DOMxSEX": ("dominio_urbano_rural", "sexo"),
    "EDADxESC": ("edad", "escolaridad_proxy"),
    "EDADxSEX": ("edad", "sexo"),
    "ESCxSEX": ("escolaridad_proxy", "sexo"),
}
CORTO = {
    "escolaridad_proxy": {"hasta primaria": "EP1", "secundaria": "EP2",
                          "media superior": "EP3", "superior": "EP4"},
    "dominio_urbano_rural": {"Rural": "D1", "Complemento urbano": "D2",
                             "Urbano": "D3"},
    "sexo": {"1 Hombre": "X1", "2 Mujer": "X2"},
    "edad": {"18-29": "A1", "30-44": "A2", "45-59": "A3", "60+": "A4"},
}
ORDEN_EJE = {"escolaridad_proxy": mr.ORD_ESC, "dominio_urbano_rural": mr.ORD_DOMINIO,
             "sexo": mr.ORD_SEXO, "edad": mr.ORD_EDAD}

# Ids del CALC ya sellado con los 13 marginales de 2025 (control de
# reproducción; NUNCA se usan como única fuente de las réplicas).
IDS_MARGINALES_2025 = {
    ("sexo", "1 Hombre"): "RESULT-ARBITRO-ENVIPE2025-EVASION-SEXO-1",
    ("sexo", "2 Mujer"): "RESULT-ARBITRO-ENVIPE2025-EVASION-SEXO-2",
    ("edad", "18-29"): "RESULT-ARBITRO-ENVIPE2025-EVASION-EDAD-18-29",
    ("edad", "30-44"): "RESULT-ARBITRO-ENVIPE2025-EVASION-EDAD-30-44",
    ("edad", "45-59"): "RESULT-ARBITRO-ENVIPE2025-EVASION-EDAD-45-59",
    ("edad", "60+"): "RESULT-ARBITRO-ENVIPE2025-EVASION-EDAD-60-MAS",
    ("escolaridad_proxy", "hasta primaria"): "RESULT-ARBITRO-ENVIPE2025-EVASION-ESCOLARIDAD-HASTA-PRIMARIA",
    ("escolaridad_proxy", "secundaria"): "RESULT-ARBITRO-ENVIPE2025-EVASION-ESCOLARIDAD-SECUNDARIA",
    ("escolaridad_proxy", "media superior"): "RESULT-ARBITRO-ENVIPE2025-EVASION-ESCOLARIDAD-MEDIA-SUPERIOR",
    ("escolaridad_proxy", "superior"): "RESULT-ARBITRO-ENVIPE2025-EVASION-ESCOLARIDAD-SUPERIOR",
    ("dominio_urbano_rural", "Rural"): "RESULT-ARBITRO-ENVIPE2025-EVASION-DOMINIO-RURAL",
    ("dominio_urbano_rural", "Complemento urbano"): "RESULT-ARBITRO-ENVIPE2025-EVASION-DOMINIO-COMPLEMENTO-URBANO",
    ("dominio_urbano_rural", "Urbano"): "RESULT-ARBITRO-ENVIPE2025-EVASION-DOMINIO-URBANO",
}
NACIONAL_ID = "RESULT-ARBITRO-ENVIPE2025-EVASION-TOTAL-TODOS"

N_MINIMO = 200
OLAS_SOPORTE = ("2023", "2024", "2025")
FUERA_DE_SOPORTE_EX_ANTE: dict = {cid: set() for cid in CRUCES}  # ninguna, a priori


def celdas(cruce_id):
    a, b = CRUCES[cruce_id]
    return [(ka, kb) for ka in ORDEN_EJE[a] for kb in ORDEN_EJE[b]]


def celda_corta(cruce_id, ka, kb):
    a, b = CRUCES[cruce_id]
    return f"{CORTO[a][ka]}x{CORTO[b][kb]}"


def prefijo(cruce_id):
    return f"{P}-{cruce_id}"


class ParoDeGuardia(RuntimeError):
    pass


def _fp_estado(tsv_bytes: bytes, fp_id: str):
    texto = tsv_bytes.decode("utf-8")
    for linea in texto.splitlines()[1:]:
        campos = linea.split("\t")
        if campos and campos[0] == fp_id:
            return campos[5] if len(campos) > 5 else None
    return None


def _guardia_firmas(inputs):
    tsv = inputs["firmas_pendientes_tsv"]["bytes"]
    for fp_id in (FP_A, FP_B):
        estado = _fp_estado(tsv, fp_id)
        if estado != "FIRMADA":
            raise ParoDeGuardia(f"{fp_id}: estado={estado!r}, se exige FIRMADA")


def _logit(p):
    return math.log(p / (1.0 - p))


def _expit(z):
    return 1.0 / (1.0 + math.exp(-z))


def _abierto(p):
    return p is not None and np.isfinite(p) and 0.0 < p < 1.0


def _pct(v, q):
    return float(np.percentile(v, q)) if len(v) else None


def _lee_json(inputs, iid):
    raw = json.loads(inputs[iid]["bytes"].decode("utf-8"))
    resultados = raw.get("resultados", raw) if isinstance(raw, dict) else raw
    if isinstance(resultados, list):
        resultados = {x["id"]: x["valor"] for x in resultados}
    return resultados


def _marginales_2025_sellados(inputs):
    """{eje: {categoria: p}} y el nacional, leídos del CALC ya sellado. NO
    abre ningún zip aquí -- es el control, no la fuente de réplicas."""
    resultados = _lee_json(inputs, "marginales_2025_resultados")
    out: dict = {}
    for (eje, cat), rid in IDS_MARGINALES_2025.items():
        if f"{rid}-P" not in resultados:
            raise ParoDeGuardia(f"marginal sellado ausente: {rid}-P")
        out.setdefault(eje, {})[cat] = {
            "p": float(resultados[f"{rid}-P"]),
            "ic95": (float(resultados[f"{rid}-IC-LO"]), float(resultados[f"{rid}-IC-HI"])),
            "n": int(resultados[f"{rid}-N"]),
        }
    out["nacional"] = {"p": float(resultados[f"{NACIONAL_ID}-P"])}
    return out


def _interaccion_celda(p_ab, p_a, p_b, p_nac):
    if not all(_abierto(x) for x in (p_ab, p_a, p_b, p_nac)):
        return None
    return _logit(p_ab) - (_logit(p_a) + _logit(p_b) - _logit(p_nac))


def _interaccion_replicas(r_ab, r_a, r_b, r_nac):
    ok = (np.isfinite(r_ab) & np.isfinite(r_a) & np.isfinite(r_b) & np.isfinite(r_nac)
          & (r_ab > 0) & (r_ab < 1) & (r_a > 0) & (r_a < 1)
          & (r_b > 0) & (r_b < 1) & (r_nac > 0) & (r_nac < 1))
    with np.errstate(all="ignore"):
        l_ab = np.log(r_ab / (1 - r_ab))
        l_a = np.log(r_a / (1 - r_a))
        l_b = np.log(r_b / (1 - r_b))
        l_nac = np.log(r_nac / (1 - r_nac))
    reps = np.where(ok, l_ab - (l_a + l_b - l_nac), np.nan)
    return reps, int((~ok).sum())


def _lambda_cruce(deltas_23, ee_23, deltas_24, ee_24, celdas_fuera_ex_ante):
    """Método de momentos Empirical-Bayes, spec §2.1. `deltas_*`/`ee_*`:
    {celda_corta: valor|None}. Sólo entran celdas con ambos deltas
    definidos, fuera de FUERA_DE_SOPORTE_EX_ANTE de este cruce."""
    dbar, var = [], []
    incluidas = []
    for c in deltas_23:
        if c in celdas_fuera_ex_ante:
            continue
        d23, d24 = deltas_23[c], deltas_24[c]
        e23, e24 = ee_23.get(c), ee_24.get(c)
        if None in (d23, d24, e23, e24):
            continue
        dbar.append((d23 + d24) / 2.0)
        var.append((e23 ** 2 + e24 ** 2) / 4.0)
        incluidas.append(c)
    k = len(dbar)
    if k < 2:
        return {"lambda": 0.0, "tau2": 0.0, "sigma_bar2": 0.0, "var_entre": 0.0,
                "k": k, "celdas": incluidas, "estado": "K-INSUFICIENTE"}
    var_entre = float(np.var(dbar, ddof=1))
    sigma2 = float(np.mean(var))
    tau2 = max(0.0, var_entre - sigma2)
    lam = tau2 / (tau2 + sigma2) if (tau2 + sigma2) > 0 else 0.0
    return {"lambda": float(lam), "tau2": float(tau2), "sigma_bar2": float(sigma2),
            "var_entre": float(var_entre), "k": int(k), "celdas": incluidas,
            "estado": "K-SUFICIENTE"}


def medir(inputs, contrato):
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    umbral = int(par["n_minimo_celda"])
    ola_reservada = int(par["ola_reservada"])
    out: dict = {}

    _guardia_firmas(inputs)

    for iid, clave in (("envipe2023_csv", "ENVIPE2023-CSV"),
                       ("envipe2024_csv", "ENVIPE2024-CSV"),
                       ("envipe2025_csv", "ENVIPE2025-CSV"),
                       ("marginales_2025_resultados", "MARGINALES-2025-SELLADOS")):
        out[f"{P}-G-INPUT-{clave}-SHA256"] = str(inputs[iid]["sha256"])

    ejes_necesarios = sorted({e for par2 in CRUCES.values() for e in par2})

    # ── 2024 · ola de desarrollo: marginales por eje + los cuatro cruces ──
    ola24 = mr.carga_ola(inputs["envipe2024_csv"]["ruta_absoluta"], 2024, reservada=False)
    rep24 = mr.replicas_compartidas(ola24, semilla, n_rep)
    marg24 = {e: mr.marginal(ola24, e, replicas=rep24) for e in (*ejes_necesarios, "nacional")}
    cel24 = {e: marg24[e]["celdas"] for e in marg24}
    nac24 = cel24["nacional"]["NAC"]
    out[f"{P}-G-W24-N-UNIVERSO"] = int(ola24.meta["filas_universo"])
    out[f"{P}-G-W24-P-NACIONAL"] = nac24["p"]

    # ── 2023 · insumo de C7/C-ENCOGIDA: marginales + los cuatro cruces ────
    ola23 = mr.carga_ola(inputs["envipe2023_csv"]["ruta_absoluta"], 2023, reservada=False)
    rep23 = mr.replicas_compartidas(ola23, semilla, n_rep)
    marg23 = {e: mr.marginal(ola23, e, replicas=rep23) for e in (*ejes_necesarios, "nacional")}
    cel23 = {e: marg23[e]["celdas"] for e in marg23}
    nac23 = cel23["nacional"]["NAC"]
    out[f"{P}-G-W23-N-UNIVERSO"] = int(ola23.meta["filas_universo"])
    out[f"{P}-G-W23-P-NACIONAL"] = nac23["p"]

    # ── 2025 · marginales de UN eje por llamada, ola marcada reservada ────
    ola25 = mr.carga_ola(inputs["envipe2025_csv"]["ruta_absoluta"], ola_reservada, reservada=True)
    rep25 = mr.replicas_compartidas(ola25, semilla, n_rep)
    marg25 = {e: mr.marginal(ola25, e, replicas=rep25) for e in (*ejes_necesarios, "nacional")}
    cel25 = {e: marg25[e]["celdas"] for e in marg25}
    nac25 = cel25["nacional"]["NAC"]
    out[f"{P}-G-M25-N-UNIVERSO"] = int(ola25.meta["filas_universo"])

    # la guardia se PRUEBA: el cruce sobre la ola reservada tiene que fallar
    try:
        mr.cruce(ola25, "escolaridad_proxy", "dominio_urbano_rural")
        derivado, guardia = "SI", "NO-LANZO -- DEFECTO"
    except mr.ReservaRota as exc:
        derivado, guardia = "NO", f"ReservaRota: {exc}"
    out[f"{P}-G-RESERVA-CRUCE-2025-DERIVADO"] = derivado
    out[f"{P}-G-RESERVA-GUARDIA-PROBADA"] = guardia

    # ── control de reproducción contra el CALC ya sellado (2025) ──────────
    sell = _marginales_2025_sellados(inputs)
    tol_p = float(par["control_arbitro_tol_p"])
    tol_ic = float(par["control_arbitro_tol_ic"])
    peor_p, peor_ic = 0.0, 0.0
    for eje in ejes_necesarios:
        for cat in ORDEN_EJE[eje]:
            c = cel25[eje][cat]
            s = sell[eje][cat]
            d_p = float(c["p"]) - s["p"]
            peor_p = max(peor_p, abs(d_p))
            if c["ic95"] is not None:
                d_lo = float(c["ic95"][0]) - s["ic95"][0]
                d_hi = float(c["ic95"][1]) - s["ic95"][1]
                peor_ic = max(peor_ic, abs(d_lo), abs(d_hi))
    d_pnac = float(nac25["p"]) - sell["nacional"]["p"]
    peor_p = max(peor_p, abs(d_pnac))
    out[f"{P}-G-CTRL-ARBITRO-DELTA-P-MAX"] = float(peor_p)
    out[f"{P}-G-CTRL-ARBITRO-DELTA-IC-MAX"] = float(peor_ic)
    out[f"{P}-G-CTRL-ARBITRO-VEREDICTO"] = (
        "REPRODUCE" if (peor_p <= tol_p and peor_ic <= tol_ic) else "NO-REPRODUCE")

    # ── C-ASTRA · ¿existe un candidato externo sellado al abrir? ──────────
    out[f"{P}-G-C-ASTRA-ESTADO"] = str(par.get("c_astra_estado", "NO-ENTRA -- ningún CALC-ASTRA-* sellado al abrir este COMMIT (ADENDA-1)"))

    # ── por cruce ──────────────────────────────────────────────────────
    for cruce_id, (eje_a, eje_b) in CRUCES.items():
        pre = prefijo(cruce_id)
        x24 = mr.cruce(ola24, eje_a, eje_b, replicas=rep24)
        x23 = mr.cruce(ola23, eje_a, eje_b, replicas=rep23)
        out[f"{pre}-G-COBERTURA-CRUCE-2024"] = float(x24["cobertura"])
        out[f"{pre}-G-COBERTURA-CRUCE-2023"] = float(x23["cobertura"])

        deltas23, ee23, deltas24 = {}, {}, {}
        fuera_ex_ante = FUERA_DE_SOPORTE_EX_ANTE[cruce_id]

        for ka, kb in celdas(cruce_id):
            c = celda_corta(cruce_id, ka, kb)
            base = f"{pre}-{c}"

            # C1 · persistencia 2024
            cel_24 = x24["celdas"][(ka, kb)]
            sop24 = "SOPORTE-OK" if cel_24["n"] >= umbral else "FUERA-DE-SOPORTE"
            out[f"{base}-C1-N"] = int(cel_24["n"])
            out[f"{base}-C1-SOPORTE-2024"] = sop24
            out[f"{base}-C1-P"] = cel_24["p"]
            r24 = cel_24["replicas"]
            ok24 = r24[np.isfinite(r24)] if r24 is not None else np.array([])
            out[f"{base}-C1-IC-LO"] = _pct(ok24, 2.5)
            out[f"{base}-C1-IC-HI"] = _pct(ok24, 97.5)

            cel_23 = x23["celdas"][(ka, kb)]
            sop23 = "SOPORTE-OK" if cel_23["n"] >= umbral else "FUERA-DE-SOPORTE"
            out[f"{base}-W23-N"] = int(cel_23["n"])
            out[f"{base}-W23-SOPORTE"] = sop23

            # interacciones 2023/2024
            pa24, pb24 = cel24[eje_a][ka]["p"], cel24[eje_b][kb]["p"]
            pa23, pb23 = cel23[eje_a][ka]["p"], cel23[eje_b][kb]["p"]
            i24 = _interaccion_celda(cel_24["p"], pa24, pb24, nac24["p"])
            i23 = _interaccion_celda(cel_23["p"], pa23, pb23, nac23["p"])
            out[f"{base}-I24"] = i24
            out[f"{base}-I23"] = i23
            reps_i24 = reps_i23 = None
            if cel_24["replicas"] is not None:
                reps_i24, sd24 = _interaccion_replicas(
                    cel_24["replicas"], cel24[eje_a][ka]["replicas"],
                    cel24[eje_b][kb]["replicas"], nac24["replicas"])
                ok_i24 = reps_i24[np.isfinite(reps_i24)]
                out[f"{base}-I24-IC-LO"] = _pct(ok_i24, 2.5)
                out[f"{base}-I24-IC-HI"] = _pct(ok_i24, 97.5)
                out[f"{base}-I24-EE"] = float(np.std(ok_i24, ddof=1)) if len(ok_i24) > 1 else None
            else:
                out[f"{base}-I24-IC-LO"] = out[f"{base}-I24-IC-HI"] = out[f"{base}-I24-EE"] = None
            if cel_23["replicas"] is not None:
                reps_i23, sd23 = _interaccion_replicas(
                    cel_23["replicas"], cel23[eje_a][ka]["replicas"],
                    cel23[eje_b][kb]["replicas"], nac23["replicas"])
                ok_i23 = reps_i23[np.isfinite(reps_i23)]
                out[f"{base}-I23-IC-LO"] = _pct(ok_i23, 2.5)
                out[f"{base}-I23-IC-HI"] = _pct(ok_i23, 97.5)
                out[f"{base}-I23-EE"] = float(np.std(ok_i23, ddof=1)) if len(ok_i23) > 1 else None
            else:
                out[f"{base}-I23-IC-LO"] = out[f"{base}-I23-IC-HI"] = out[f"{base}-I23-EE"] = None

            deltas23[c] = i23
            deltas24[c] = i24
            ee23[c] = out[f"{base}-I23-EE"]

            # C2 · piso log-aditivo, marginales de 2025 SELLADOS (punto) +
            # réplicas propias (IC), réplica a réplica
            pa25, pb25 = sell[eje_a][ka]["p"], sell[eje_b][kb]["p"]
            pnac25 = sell["nacional"]["p"]
            p_c2 = (_expit(_logit(pa25) + _logit(pb25) - _logit(pnac25))
                    if all(_abierto(x) for x in (pa25, pb25, pnac25)) else None)
            out[f"{base}-C2-P"] = p_c2
            ra25 = cel25[eje_a][ka]["replicas"]
            rb25 = cel25[eje_b][kb]["replicas"]
            rnac25 = nac25["replicas"]
            ok_c2 = (np.isfinite(ra25) & np.isfinite(rb25) & np.isfinite(rnac25)
                     & (ra25 > 0) & (ra25 < 1) & (rb25 > 0) & (rb25 < 1)
                     & (rnac25 > 0) & (rnac25 < 1))
            with np.errstate(all="ignore"):
                lc2 = np.where(ok_c2, np.log(ra25 / (1 - ra25)) + np.log(rb25 / (1 - rb25))
                              - np.log(rnac25 / (1 - rnac25)), np.nan)
            c2r = 1.0 / (1.0 + np.exp(-lc2[ok_c2]))
            out[f"{base}-C2-IC-LO"] = _pct(c2r, 2.5)
            out[f"{base}-C2-IC-HI"] = _pct(c2r, 97.5)
            out[f"{base}-C2-REPLICAS-SIN-DEFINIR"] = int((~ok_c2).sum())

            # C7 · logit C2 + delta_barra (sin encoger) — se completa tras
            # conocer lambda_cruce, tres líneas abajo; aquí sólo delta_barra
            if i23 is not None and i24 is not None:
                dbar_c = (i23 + i24) / 2.0
                out[f"{base}-C7-P"] = _expit(_logit(p_c2) + dbar_c) if p_c2 is not None else None
            else:
                out[f"{base}-C7-P"] = None
            if reps_i23 is not None and reps_i24 is not None:
                ok7 = ok_c2 & np.isfinite(reps_i23) & np.isfinite(reps_i24)
                dbar_r = 0.5 * (reps_i23[ok7] + reps_i24[ok7])
                c7r = 1.0 / (1.0 + np.exp(-(lc2[ok7] + dbar_r)))
                out[f"{base}-C7-IC-LO"] = _pct(c7r, 2.5)
                out[f"{base}-C7-IC-HI"] = _pct(c7r, 97.5)
                out[f"{base}-C7-REPLICAS-SIN-DEFINIR"] = int((~ok7).sum())
            else:
                out[f"{base}-C7-IC-LO"] = out[f"{base}-C7-IC-HI"] = None
                out[f"{base}-C7-REPLICAS-SIN-DEFINIR"] = n_rep

        # ── λ del cruce, y C-ENCOGIDA por celda ───────────────────────────
        lam = _lambda_cruce(deltas23, ee23, deltas24, {c: out[f"{pre}-{c}-I24-EE"] for c in deltas24},
                            fuera_ex_ante)
        out[f"{pre}-G-LAMBDA"] = lam["lambda"]
        out[f"{pre}-G-LAMBDA-TAU2"] = lam["tau2"]
        out[f"{pre}-G-LAMBDA-SIGMA-BAR2"] = lam["sigma_bar2"]
        out[f"{pre}-G-LAMBDA-VAR-ENTRE"] = lam["var_entre"]
        out[f"{pre}-G-LAMBDA-K"] = lam["k"]
        out[f"{pre}-G-LAMBDA-ESTADO"] = lam["estado"]

        for ka, kb in celdas(cruce_id):
            c = celda_corta(cruce_id, ka, kb)
            base = f"{pre}-{c}"
            i23v, i24v = deltas23[c], deltas24[c]
            p_c2 = out[f"{base}-C2-P"]
            if i23v is not None and i24v is not None and p_c2 is not None:
                dbar_c = lam["lambda"] * (i23v + i24v) / 2.0
                out[f"{base}-C-ENCOGIDA-P"] = _expit(_logit(p_c2) + dbar_c)
            else:
                out[f"{base}-C-ENCOGIDA-P"] = None
            ra25 = cel25[eje_a][ka]["replicas"]
            rb25 = cel25[eje_b][kb]["replicas"]
            rnac25 = nac25["replicas"]
            ok_c2 = (np.isfinite(ra25) & np.isfinite(rb25) & np.isfinite(rnac25)
                     & (ra25 > 0) & (ra25 < 1) & (rb25 > 0) & (rb25 < 1)
                     & (rnac25 > 0) & (rnac25 < 1))
            with np.errstate(all="ignore"):
                lc2 = np.where(ok_c2, np.log(ra25 / (1 - ra25)) + np.log(rb25 / (1 - rb25))
                              - np.log(rnac25 / (1 - rnac25)), np.nan)
            cel_24 = x24["celdas"][(ka, kb)]
            cel_23 = x23["celdas"][(ka, kb)]
            reps_i24 = _interaccion_replicas(
                cel_24["replicas"], cel24[eje_a][ka]["replicas"],
                cel24[eje_b][kb]["replicas"], nac24["replicas"])[0] if cel_24["replicas"] is not None else None
            reps_i23 = _interaccion_replicas(
                cel_23["replicas"], cel23[eje_a][ka]["replicas"],
                cel23[eje_b][kb]["replicas"], nac23["replicas"])[0] if cel_23["replicas"] is not None else None
            if reps_i23 is not None and reps_i24 is not None:
                okE = ok_c2 & np.isfinite(reps_i23) & np.isfinite(reps_i24)
                dbar_r = lam["lambda"] * 0.5 * (reps_i23[okE] + reps_i24[okE])
                cEr = 1.0 / (1.0 + np.exp(-(lc2[okE] + dbar_r)))
                out[f"{base}-C-ENCOGIDA-IC-LO"] = _pct(cEr, 2.5)
                out[f"{base}-C-ENCOGIDA-IC-HI"] = _pct(cEr, 97.5)
            else:
                out[f"{base}-C-ENCOGIDA-IC-LO"] = out[f"{base}-C-ENCOGIDA-IC-HI"] = None

            # C-ASTRA · declarado NO-ENTRA salvo que el contrato lo traiga
            out[f"{base}-C-ASTRA-P"] = None
            out[f"{base}-C-ASTRA-ESTADO"] = "NO-ENTRA"

        out[f"{pre}-G-FORMA-C1"] = "p24(a,b) directo"
        out[f"{pre}-G-FORMA-C2"] = "expit(logit p25(a) + logit p25(b) - logit p25)"
        out[f"{pre}-G-FORMA-C7"] = "expit(logit C2 + (I23(a,b)+I24(a,b))/2)"
        out[f"{pre}-G-FORMA-C-ENCOGIDA"] = "expit(logit C2 + lambda_cruce*(I23(a,b)+I24(a,b))/2)"

    out[f"{P}-G-DESENLACE-ID"] = DESENLACE_ID
    out[f"{P}-G-INCERTIDUMBRE"] = (
        "IC95 percentil 2.5/97.5 de réplicas bootstrap de conglomerado "
        "estratificado, un remuestreo por ola compartido por todos sus "
        "grupos; C7/C-ENCOGIDA combinan la réplica k de cada ola (muestras "
        "independientes), sin covarianzas inventadas")
    out[f"{P}-G-L-ESTADO"] = "NO-ENTRA -- por firma de mesa (§2: sin L)"
    return out


_GLOBALES = (
    ("G-INPUT-ENVIPE2023-CSV-SHA256", "texto", "hash sha256"),
    ("G-INPUT-ENVIPE2024-CSV-SHA256", "texto", "hash sha256"),
    ("G-INPUT-ENVIPE2025-CSV-SHA256", "texto", "hash sha256"),
    ("G-INPUT-MARGINALES-2025-SELLADOS-SHA256", "texto", "hash sha256"),
    ("G-W24-N-UNIVERSO", "entero", "delitos"),
    ("G-W24-P-NACIONAL", "proporcion", "proporción [0,1]"),
    ("G-W23-N-UNIVERSO", "entero", "delitos"),
    ("G-W23-P-NACIONAL", "proporcion", "proporción [0,1]"),
    ("G-M25-N-UNIVERSO", "entero", "delitos"),
    ("G-RESERVA-CRUCE-2025-DERIVADO", "texto", "categoría (SI/NO)"),
    ("G-RESERVA-GUARDIA-PROBADA", "texto", "categoría"),
    ("G-CTRL-ARBITRO-DELTA-P-MAX", "flotante", "diferencia de proporción"),
    ("G-CTRL-ARBITRO-DELTA-IC-MAX", "flotante", "diferencia de proporción"),
    ("G-CTRL-ARBITRO-VEREDICTO", "texto", "categoría"),
    ("G-C-ASTRA-ESTADO", "texto", "categoría"),
    ("G-DESENLACE-ID", "texto", "identificador"),
    ("G-INCERTIDUMBRE", "texto", "descripción del método"),
    ("G-L-ESTADO", "texto", "categoría"),
)
_POR_CRUCE = (
    ("G-COBERTURA-CRUCE-2024", "proporcion", "proporción [0,1]"),
    ("G-COBERTURA-CRUCE-2023", "proporcion", "proporción [0,1]"),
    ("G-LAMBDA", "flotante", "adimensional [0,1]"),
    ("G-LAMBDA-TAU2", "flotante", "varianza en escala logit al cuadrado"),
    ("G-LAMBDA-SIGMA-BAR2", "flotante", "varianza en escala logit al cuadrado"),
    ("G-LAMBDA-VAR-ENTRE", "flotante", "varianza en escala logit al cuadrado"),
    ("G-LAMBDA-K", "entero", "celdas"),
    ("G-LAMBDA-ESTADO", "texto", "categoría"),
    ("G-FORMA-C1", "texto", "fórmula (texto)"),
    ("G-FORMA-C2", "texto", "fórmula (texto)"),
    ("G-FORMA-C7", "texto", "fórmula (texto)"),
    ("G-FORMA-C-ENCOGIDA", "texto", "fórmula (texto)"),
)
_POR_CELDA = (
    ("C1-N", "entero", "delitos"), ("C1-SOPORTE-2024", "texto", "categoría"),
    ("C1-P", "proporcion", "proporción [0,1]"),
    ("C1-IC-LO", "proporcion", "proporción [0,1]"), ("C1-IC-HI", "proporcion", "proporción [0,1]"),
    ("W23-N", "entero", "delitos"), ("W23-SOPORTE", "texto", "categoría"),
    ("I24", "flotante", "logit"), ("I23", "flotante", "logit"),
    ("I24-IC-LO", "flotante", "logit"), ("I24-IC-HI", "flotante", "logit"),
    ("I24-EE", "flotante", "error estándar en escala logit"),
    ("I23-IC-LO", "flotante", "logit"), ("I23-IC-HI", "flotante", "logit"),
    ("I23-EE", "flotante", "error estándar en escala logit"),
    ("C2-P", "proporcion", "proporción [0,1]"), ("C2-IC-LO", "proporcion", "proporción [0,1]"),
    ("C2-IC-HI", "proporcion", "proporción [0,1]"),
    ("C2-REPLICAS-SIN-DEFINIR", "entero", "réplicas"),
    ("C7-P", "proporcion", "proporción [0,1]"), ("C7-IC-LO", "proporcion", "proporción [0,1]"),
    ("C7-IC-HI", "proporcion", "proporción [0,1]"),
    ("C7-REPLICAS-SIN-DEFINIR", "entero", "réplicas"),
    ("C-ENCOGIDA-P", "proporcion", "proporción [0,1]"),
    ("C-ENCOGIDA-IC-LO", "proporcion", "proporción [0,1]"),
    ("C-ENCOGIDA-IC-HI", "proporcion", "proporción [0,1]"),
    ("C-ASTRA-P", "proporcion", "proporción [0,1]"), ("C-ASTRA-ESTADO", "texto", "categoría"),
)


def esquema_resultados(*_args):
    """Enumera, por estructura (CRUCES/ORDEN_EJE), exactamente los mismos ids
    que `medir()` emite -- sin correrlo y sin datos. `resultados:` del
    spec.yaml y el test D-22 (a) (`ids == set(out)`) se derivan de esta
    misma función, nunca se teclean por separado."""
    filas = []
    for suf, tipo, unidad in _GLOBALES:
        filas.append({"id": f"{P}-{suf}", "tipo": tipo, "unidad": unidad})
    for cruce_id in CRUCES:
        pre = prefijo(cruce_id)
        for suf, tipo, unidad in _POR_CRUCE:
            filas.append({"id": f"{pre}-{suf}", "tipo": tipo, "unidad": unidad})
        for ka, kb in celdas(cruce_id):
            base = f"{pre}-{celda_corta(cruce_id, ka, kb)}"
            for suf, tipo, unidad in _POR_CELDA:
                fila = {"id": f"{base}-{suf}", "tipo": tipo, "unidad": unidad}
                if tipo in ("proporcion", "flotante") and suf not in ("C1-N", "W23-N"):
                    fila["permite_no_estimable"] = True
                filas.append(fila)
    return filas
