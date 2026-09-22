"""ARBITRO-MARGINALES-2, pieza LAPOP (6a pieza de P2, mesa 21/sep/2026).

Formaliza en GEN2 tres reglas de milpa/tramite-ola5-propuesta-v0.yaml (P1:
RE-MEDIDA nueva) sin CALC GEN2 previo: civico.clientelismo.
turnout_no_vote_choice_lapop2019, civico.protesta.agravio_urbano_lapop2019,
civico.voto.agencia_lapop2023. Universo, eje, desenlace, ponderador y metodo
de IC son los que GEN1 ya prerregistro (MAESTRA35-L9); ver
forense/prereg-caja/ARBITRO-MARGINALES-2-LAPOP-spec-v1_0.md.

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor}.
"""
from __future__ import annotations

import json

import numpy as np
import pyreadstat

PID_2019 = "mexico_lapop_americasbarometer_2019_v1_0_w"
PID_2023 = "mex_2023_lapop_americasbarometer_v1_0_w"
SEP = "␟"
GUARDIA_NUMERADOR = 10


def _code(v):
    if v is None:
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(f) or f != int(f):
        return None
    return int(f)


def _weight(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if np.isfinite(f) and f > 0 else None


def _pct(series):
    good = series[np.isfinite(series)]
    if not len(good):
        return None, None
    return (float(np.percentile(good, 2.5)), float(np.percentile(good, 97.5)))


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False)


class Survey:
    """Bootstrap de UPM dentro de estrato -- mismo metodo que las piezas
    ENCUCI2020 de este acto, aplicado a estratopri/upm/wt de LAPOP."""

    def __init__(self, est, upm, w, replicas, seed):
        self.w = np.asarray(w, dtype=float)
        self.n = len(self.w)
        self.replicas = int(replicas)
        self.est = np.asarray([str(x) for x in est])
        self.upm = np.asarray([str(x) for x in upm])
        keys = np.asarray([f"{a}{SEP}{b}" for a, b in zip(self.est, self.upm)])
        psus, self.psu_inverse = np.unique(keys, return_inverse=True)
        psu_strata = np.asarray([x.split(SEP, 1)[0] for x in psus])
        strata = np.unique(psu_strata)
        self.n_strata, self.n_psu = len(strata), len(psus)
        self.n_singleton = 0
        self.draws = np.zeros((self.replicas, self.n_psu), dtype=np.int16)
        rng = np.random.Generator(np.random.PCG64(int(seed)))
        for stratum in strata:
            pos = np.flatnonzero(psu_strata == stratum)
            k = len(pos)
            if k == 1:
                self.n_singleton += 1
                self.draws[:, pos[0]] = 1
            else:
                self.draws[:, pos] = rng.multinomial(
                    k, np.full(k, 1.0 / k), size=self.replicas)

    def ratio(self, numerator, denominator):
        numerator = np.asarray(numerator, dtype=bool)
        denominator = np.asarray(denominator, dtype=bool)
        den_w = self.w * denominator
        mass = float(den_w.sum())
        n_den = int(denominator.sum())
        n_num = int((numerator & denominator).sum())
        if n_num < GUARDIA_NUMERADOR:
            return {"n": n_den, "numerador": n_num, "masa": mass,
                    "p": "NO-ESTIMABLE", "ic95_lo": None, "ic95_hi": None,
                    "motivo": f"numerador {n_num} < {GUARDIA_NUMERADOR}"}
        point = None if mass <= 0 else float(
            (self.w * numerator * denominator).sum() / mass)
        den_psu = np.bincount(self.psu_inverse, weights=den_w,
                               minlength=self.n_psu)
        num_psu = np.bincount(self.psu_inverse,
                               weights=self.w * numerator * denominator,
                               minlength=self.n_psu)
        den_rep = self.draws @ den_psu
        num_rep = self.draws @ num_psu
        with np.errstate(divide="ignore", invalid="ignore"):
            series = np.where(den_rep > 0, num_rep / den_rep, np.nan)
        lo, hi = _pct(series)
        return {"n": n_den, "numerador": n_num, "masa": mass, "p": point,
                "ic95_lo": lo, "ic95_hi": hi}


def _regla_a(df, replicas, seed):
    clien1na = df["clien1na"].map(_code)
    vb2 = df["vb2"].map(_code)
    vb3n = df["vb3n"].map(_code)
    wt = df["wt"].map(_weight).fillna(0.0)

    u_asistencia = clien1na.isin([1, 2]) & vb2.isin([1, 2])
    survey_a = Survey(df.loc[u_asistencia, "estratopri"],
                       df.loc[u_asistencia, "upm"], wt[u_asistencia],
                       replicas, seed)
    oferta = (clien1na == 1)[u_asistencia]
    votado = (vb2 == 1)[u_asistencia]
    asistencia = {
        "con_oferta": survey_a.ratio(votado, oferta),
        "sin_oferta": survey_a.ratio(votado, ~oferta),
    }

    u_eleccion = u_asistencia & (vb2 == 1) & vb3n.notna()
    survey_b = Survey(df.loc[u_eleccion, "estratopri"],
                       df.loc[u_eleccion, "upm"], wt[u_eleccion],
                       replicas, seed)
    oferta_e = (clien1na == 1)[u_eleccion]
    pri = (vb3n == 103)[u_eleccion]
    eleccion_pri = {
        "con_oferta": survey_b.ratio(pri, oferta_e),
        "sin_oferta": survey_b.ratio(pri, ~oferta_e),
    }
    return {
        "n_universo_asistencia": int(u_asistencia.sum()),
        "n_universo_eleccion": int(u_eleccion.sum()),
        "asistencia": asistencia,
        "eleccion_pri": eleccion_pri,
    }


def _regla_b(df, replicas, seed):
    prot3 = df["prot3"].map(_code)
    ur = df["ur"].map(_code)
    vic1ext = df["vic1ext"].map(_code)
    wt = df["wt"].map(_weight).fillna(0.0)

    u = prot3.isin([1, 2]) & ur.isin([1, 2]) & vic1ext.isin([1, 2])
    survey = Survey(df.loc[u, "estratopri"], df.loc[u, "upm"], wt[u],
                     replicas, seed)
    part = (prot3 == 1)[u]
    urbano = (ur == 1)[u]
    victima = (vic1ext == 1)[u]
    celdas = {
        "urbano_victima": survey.ratio(part, urbano & victima),
        "urbano_no_victima": survey.ratio(part, urbano & (~victima)),
        "rural_victima": survey.ratio(part, (~urbano) & victima),
        "rural_no_victima": survey.ratio(part, (~urbano) & (~victima)),
    }
    return {"n_universo": int(u.sum()), "celdas": celdas}


def _regla_c(df, replicas, seed):
    mexwf = df["mexwf1_19"].map(_code)
    countfair = df["countfair3"].map(_code)
    vb20 = df["vb20"].map(_code)
    wt = df["wt"].map(_weight).fillna(0.0)

    u = mexwf.isin([1, 2]) & countfair.isin([1, 2, 3]) & vb20.isin([1, 2, 3, 4])
    survey = Survey(df.loc[u, "estratopri"], df.loc[u, "upm"], wt[u],
                     replicas, seed)
    ayuda = (mexwf == 1)[u]
    oficialismo = (vb20 == 2)[u]
    secreto = (countfair == 1)[u]
    observable = countfair.isin([2, 3])[u]
    ramas = {}
    for nombre, rama_mask in (("SECRETO", secreto), ("OBSERVABLE", observable)):
        ramas[nombre] = {
            "con_ayuda": survey.ratio(oficialismo, ayuda & rama_mask),
            "sin_ayuda": survey.ratio(oficialismo, (~ayuda) & rama_mask),
        }
    return {"n_universo": int(u.sum()), "ramas": ramas}


def medir(inputs, contrato):
    df19, _m19 = pyreadstat.read_dta(inputs[PID_2019]["ruta_absoluta"])
    df23, _m23 = pyreadstat.read_dta(inputs[PID_2023]["ruta_absoluta"])
    par = contrato["parametros"]
    seed = int(contrato["seed"]["valor"])
    replicas = int(par["bootstrap_replicas"])

    regla_a = _regla_a(df19, replicas, seed)
    regla_b = _regla_b(df19, replicas, seed)
    regla_c = _regla_c(df23, replicas, seed)

    return {
        "RESULT-ARB2-LAPOP-N-FILAS-2019": int(len(df19)),
        "RESULT-ARB2-LAPOP-N-FILAS-2023": int(len(df23)),
        "RESULT-ARB2-LAPOP-TURNOUT-NO-VOTE-CHOICE": _json(regla_a),
        "RESULT-ARB2-LAPOP-PROTESTA-AGRAVIO-URBANO": _json(regla_b),
        "RESULT-ARB2-LAPOP-AGENCIA-2023": _json(regla_c),
    }
