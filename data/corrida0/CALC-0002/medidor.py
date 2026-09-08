"""`CALC-0002` — marginal de INDICE_CONTEXTO por ola (S13, Camino B / ruta c).

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO EN `ACTO GEN2-E5-0` Y NO EJECUTADO EN EL. Lo corre `ACTO GEN2-E5`.
El `preflight` VERDE certifica la DECLARACION, no el numero.

NO mide `R10.3`: mide el ANTECEDENTE sin su desenlace. `aoj1` (denuncia) no
existe en 2019/2021/2023 -- verificado contra el codebook, spec.md §1.
"""
from __future__ import annotations

import numpy as np
import pyreadstat


def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como cadena."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _en(serie, codigos):
    """Indicador 1/0/NaN. Los missing extendidos de Stata (.a/.b/.c) llegan
    como NaN y se quedan NaN: no son un cero."""
    v = np.asarray(serie, dtype="float64")
    out = np.full(v.shape, np.nan)
    fin = np.isfinite(v)
    out[fin] = np.isin(v[fin], codigos).astype(float)
    return out


def _prop_ponderada(y, w):
    m = np.isfinite(y) & np.isfinite(w) & (w > 0)
    if not m.any():
        return None, 0
    return float(np.sum(y[m] * w[m]) / np.sum(w[m])), int(m.sum())


def _boot_ic(y, w, upm, estrato, b, semilla, n_min):
    ok = np.isfinite(y) & np.isfinite(w) & (w > 0)
    if int(ok.sum()) < n_min:
        return None, None
    rng = np.random.Generator(np.random.PCG64(semilla))
    idx, orden = {}, []
    for i in np.flatnonzero(ok):
        c = (estrato[i], upm[i])
        if c not in idx:
            idx[c] = []
            orden.append(c)
        idx[c].append(i)
    por_est = {}
    for e, u in orden:
        por_est.setdefault(e, []).append((e, u))
    reps = []
    for _ in range(b):
        tom = []
        for e, claves in por_est.items():
            for k in rng.integers(0, len(claves), len(claves)):
                tom.extend(idx[claves[k]])
        s = np.asarray(tom)
        p, _n = _prop_ponderada(y[s], w[s])
        if p is not None:
            reps.append(p)
    if len(reps) < b // 2:
        return None, None
    reps = np.asarray(reps)
    return float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))


def _lee(entrada):
    df, _ = pyreadstat.read_dta(entrada["ruta_absoluta"])
    return df


def medir(inputs, contrato):
    p = contrato["parametros"]
    n_min, b = int(p["n_minimo_celda"]), int(p["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    out: dict[str, object] = {}

    for ola, pid in p["olas"]:
        df = _lee(inputs[pid])
        pre = f"RESULT-CTX-{ola}"
        w = np.asarray(df[p["ponderador"]], dtype="float64")
        vict = _en(df[p["filtro_universo"]], p["codigos_victima"])
        sel = vict == 1.0
        out[f"{pre}-N-UNIVERSO"] = int(np.sum(sel & np.isfinite(w) & (w > 0)))

        # Indicadores presentes en ESTA ola -- no se supone ninguno.
        presentes, marginales = [], {}
        for var, codigos in p["indicadores"]:
            if var not in df.columns:
                marginales[var] = None
                continue
            ind = _en(df[var], codigos)
            presentes.append(ind)
            pm, _n = _prop_ponderada(ind[sel], w[sel])
            marginales[var] = _num(pm)
        for var, _c in p["indicadores"]:
            out[f"{pre}-MARGINAL-{var.upper()}"] = marginales[var]
        out[f"{pre}-N-INDICADORES"] = len(presentes)

        if len(presentes) < p["indicadores_exigidos"]:
            # El corte pre-registrado es "2 o 3 DE 3". Con menos, no existe.
            out[f"{pre}-P-ALTO"] = None
            out[f"{pre}-IC-LO"] = None
            out[f"{pre}-IC-HI"] = None
            out[f"{pre}-VEREDICTO"] = "NO-ESTIMABLE-INDICE-INCOMPLETO"
            continue

        pila = np.vstack(presentes)
        completo = np.all(np.isfinite(pila), axis=0)
        indice = np.where(completo, np.nansum(pila, axis=0), np.nan)
        alto = np.where(np.isfinite(indice),
                        (indice >= p["corte_alto"]).astype(float), np.nan)
        pa, na = _prop_ponderada(alto[sel], w[sel])
        lo, hi = _boot_ic(np.where(sel, alto, np.nan), w,
                          np.asarray(df[p["upm"]], dtype="float64"),
                          np.asarray(df[p["estrato"]], dtype="float64"),
                          b, semilla, n_min)
        out[f"{pre}-P-ALTO"] = _num(pa)
        out[f"{pre}-IC-LO"] = _num(lo)
        out[f"{pre}-IC-HI"] = _num(hi)
        out[f"{pre}-VEREDICTO"] = ("NO-ESTIMABLE" if (pa is None or na < n_min)
                                   else "MARGINAL-REPORTADO")

    # La cláusula que el encargo prohíbe convertir en veredicto: se emite como
    # output, para que quede en `resultados.json` y no sólo en la prosa.
    out["RESULT-VEREDICTO-D2H"] = p["veredicto_D2h"]
    out["RESULT-RUTA-ENCARGO"] = p["ruta_encargo"]
    return out
