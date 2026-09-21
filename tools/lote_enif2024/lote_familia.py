#!/usr/bin/env python3
"""Lo que el lote ENIF 2024 necesita y `tools/duelo/cruces_familia.py` no trae.

ACTO `GEN2-DIN-LOTE-ENIF2024-COMMIT-1` (21/sep/2026). Módulo PROPIO del lote
(perímetro §9 del encargo): el del duelo no se edita; lo que falta se añade
aquí. Genérico sobre (par, celda): no abre archivos, no conoce columnas.

QUÉ TRAE
--------
  R3   ajuste proporcional iterativo (IPF / raking) sobre la tabla 2021.
       La PROPUESTA §4 lo deja como «tabla inicial p̂_21(a,b), escalada
       iterativamente hasta casar los marginales de 2024 en las dos
       direcciones; criterio de paro y tope en spec.yaml». Una tabla de
       PROPORCIONES no tiene marginales sin una composición; la forma bien
       definida es el raking de la tabla ponderada a TRES vías (a, b, D) de
       2021 contra los márgenes (a, D) y (b, D) de 2024 -- cada uno de ellos
       es UN marginal de un eje de 2024 (p̂(a) con su masa ponderada), que es
       exactamente lo que el árbitro selló y lo único que una lectura de un
       solo eje puede dar. Se conserva la estructura de interacción de 2021
       (razones de momios) y se casan los márgenes de 2024. Los márgenes se
       normalizan a participaciones (suman 1) para que las dos direcciones
       sean compatibles aunque sus universos válidos difieran por «fuera».
       Celda con masa cero en 2021: p SIN-DEFINIR (None / NaN), no se rellena.
  cobertura_par   fracción de celdas de un par con R dentro del IC95 del
       candidato, y al revés, más su recuento -- la lectura de §9 de la spec.
  conteo_tres_cuartos   descriptivo (enmienda v0.3): en cuántas celdas
       puntuadas el retador yerra menos que el piso.
  bbis_lectura   lectura MECÁNICA del pre-registro §10 (CORROBORADA · ACOTADA
       · FALSADOR DÉBIL); si caben dos, manda FALSADOR DÉBIL. No es el
       veredicto: lo lee mesa.
"""
from __future__ import annotations

import math

import numpy as np


class LoteError(ValueError):
    """Entrada mal formada: no se rellena, se levanta."""


# ══ R3 · ajuste proporcional iterativo ═════════════════════════════════════

def _normaliza(m: np.ndarray) -> np.ndarray:
    """Divide por la suma sobre los ejes distintos del primero (réplicas);
    NaN si la suma es 0."""
    ejes = tuple(range(1, m.ndim))
    s = m.sum(axis=ejes, keepdims=True)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(s > 0, m / s, np.nan)


def ipf_3vias(tabla: np.ndarray, margen_a: np.ndarray, margen_b: np.ndarray,
              tol: float, max_iter: int) -> dict:
    """Raking vectorizado sobre réplicas.

    `tabla`     (K, A, B, 2)  masa 2021 por (a, b, d)   -- d ∈ {0, 1}
    `margen_a`  (K, A, 2)     masa 2024 por (a, d)
    `margen_b`  (K, B, 2)     masa 2024 por (b, d)
    Devuelve {"p": (K, A, B) = T[..,1]/T[..,0]+T[..,1] (NaN si masa 0),
              "iteraciones": int, "convergio": (K,) bool, "delta_max": (K,)}.
    Las tres masas se normalizan a 1 por réplica antes de iterar."""
    T = _normaliza(np.asarray(tabla, dtype=float))
    MA = _normaliza(np.asarray(margen_a, dtype=float))
    MB = _normaliza(np.asarray(margen_b, dtype=float))
    if T.ndim != 4 or MA.ndim != 3 or MB.ndim != 3:
        raise LoteError("ipf_3vias: dimensiones (K,A,B,2), (K,A,2), (K,B,2)")
    K, A, B, D = T.shape
    if MA.shape != (K, A, D) or MB.shape != (K, B, D):
        raise LoteError(f"ipf_3vias: márgenes {MA.shape} {MB.shape} no casan con {T.shape}")
    convergio = np.zeros(K, dtype=bool)
    delta = np.full(K, np.nan)
    it = 0
    with np.errstate(invalid="ignore", divide="ignore"):
        for it in range(1, int(max_iter) + 1):
            prev = T
            sa = T.sum(axis=2, keepdims=True)                       # (K, A, 1, D)
            fa = np.where(sa > 0, MA[:, :, None, :] / sa, 0.0)
            T = T * fa
            sb = T.sum(axis=1, keepdims=True)                       # (K, 1, B, D)
            fb = np.where(sb > 0, MB[:, None, :, :] / sb, 0.0)
            T = T * fb
            d = np.nanmax(np.abs(T - prev).reshape(K, -1), axis=1)
            d = np.where(np.isfinite(d), d, np.inf)
            delta = d
            convergio = d <= tol
            if bool(convergio.all()):
                break
        masa = T.sum(axis=3)
        p = np.where(masa > 0, T[..., 1] / masa, np.nan)
    return {"p": p, "iteraciones": int(it), "convergio": convergio, "delta_max": delta}


def r3_por_par(tabla_punto: np.ndarray, tabla_reps: np.ndarray | None,
               ma_punto: np.ndarray, ma_reps: np.ndarray | None,
               mb_punto: np.ndarray, mb_reps: np.ndarray | None,
               tol: float, max_iter: int) -> dict:
    """R3 del par: punto (K=1) y réplicas (K=n_rep) con la misma rutina.
    Devuelve {"p": (A,B), "p_reps": (K,A,B) | None, "iteraciones_punto",
    "convergio_punto", "iteraciones_reps", "reps_no_convergen"}."""
    pt = ipf_3vias(tabla_punto[None], ma_punto[None], mb_punto[None], tol, max_iter)
    out = {"p": pt["p"][0], "iteraciones_punto": pt["iteraciones"],
           "convergio_punto": bool(pt["convergio"][0]),
           "p_reps": None, "iteraciones_reps": 0, "reps_no_convergen": 0}
    if tabla_reps is not None and ma_reps is not None and mb_reps is not None:
        rp = ipf_3vias(tabla_reps, ma_reps, mb_reps, tol, max_iter)
        p = rp["p"].copy()
        p[~rp["convergio"]] = np.nan          # una réplica que no converge queda SIN-DEFINIR
        out.update({"p_reps": p, "iteraciones_reps": rp["iteraciones"],
                    "reps_no_convergen": int((~rp["convergio"]).sum())})
    return out


# ══ cobertura, conteo descriptivo y B-bis ══════════════════════════════════

def _flag(v):
    return None if v is None else bool(v)


def cobertura_par(filas: dict) -> dict:
    """`filas` = {celda: {"dentro_ic_R": bool|None, "R_dentro_ic_cand": bool|None}}
    (la salida por celda de `cruces_familia.adjudica`). Devuelve recuentos y
    fracciones sobre las celdas donde la comparación está definida."""
    def _frac(clave):
        vals = [_flag(f.get(clave)) for f in filas.values()]
        vals = [v for v in vals if v is not None]
        n = len(vals)
        return {"n": n, "si": int(sum(vals)), "frac": (sum(vals) / n) if n else None}
    return {"R_en_ic_cand": _frac("R_dentro_ic_cand"),
            "cand_en_ic_R": _frac("dentro_ic_R")}


def conteo_tres_cuartos(adj: dict, piso: str, retador: str) -> dict:
    """Descriptivo v0.3: celdas puntuadas donde error(retador) < error(piso)."""
    cp = adj["candidatos"][piso]["celdas"]
    cr = adj["candidatos"][retador]["celdas"]
    gana, n = 0, 0
    for c, f in cp.items():
        if not f.get("puntuada"):
            continue
        e_p, e_r = f.get("error_pp"), cr[c].get("error_pp")
        if e_p is None or e_r is None:
            continue
        n += 1
        gana += e_r < e_p
    return {"n": n, "gana_retador": gana, "frac": (gana / n) if n else None,
            "tres_cuartos": (gana >= math.ceil(0.75 * n)) if n else None}


def bbis_lectura(veredicto_primario: str, sin_soporte_frac: float | None,
                 cobertura_c2_por_par: dict, veredictos_por_par: dict,
                 ejes_por_par: dict, umbral_cobertura: float = 0.8,
                 umbral_sin_soporte: float = 1.0 / 3.0) -> dict:
    """Lectura mecánica del §10 de la spec, antes de ver el dato, en este orden:
    FALSADOR DÉBIL si ≥ ⅓ de las celdas primarias quedan sin soporte (manda
    si cabe con otra) · CORROBORADA si nadie vence y la cobertura de C2 por
    par es ≥ 80 % en todos los pares primarios · ACOTADA si vence alguien
    sólo en pares que comparten UN eje (se nombra) · en otro caso NO-CAE-EN-
    NINGUNA-FILA, y se dice."""
    razones = []
    if sin_soporte_frac is not None and sin_soporte_frac >= umbral_sin_soporte:
        return {"fila": "FALSADOR-DEBIL",
                "razon": f"{sin_soporte_frac:.3f} de las celdas primarias sin soporte (≥ ⅓); manda sobre las demás"}
    fr = [v["frac"] for v in cobertura_c2_por_par.values() if v.get("frac") is not None]
    cob_ok = bool(fr) and all(f >= umbral_cobertura for f in fr)
    vencen = [p for p, v in veredictos_por_par.items() if v == "VENCE-RETADOR"]
    if veredicto_primario == "NADIE-VENCE" and not vencen and cob_ok:
        return {"fila": "CORROBORADA",
                "razon": "nadie vence (primaria) y cobertura de C2 ≥ 80 % en cada par primario"}
    if vencen:
        comunes = None
        for p in vencen:
            ejes = set(ejes_por_par[p])
            comunes = ejes if comunes is None else (comunes & ejes)
        if comunes and len(comunes) == 1 and veredicto_primario != "VENCE-RETADOR":
            eje = next(iter(comunes))
            return {"fila": "ACOTADA", "razon": f"vence sólo en el eje {eje!r} (pares {','.join(sorted(vencen))})"}
        razones.append(f"vence en {','.join(sorted(vencen))}")
    if veredicto_primario == "VENCE-RETADOR":
        razones.append("el retador vence en la comparación primaria")
    if not cob_ok:
        razones.append("cobertura de C2 < 80 % en algún par primario (refuta el argumento de producto)")
    return {"fila": "NO-CAE-EN-NINGUNA-FILA", "razon": "; ".join(razones) or "sin condición satisfecha"}
