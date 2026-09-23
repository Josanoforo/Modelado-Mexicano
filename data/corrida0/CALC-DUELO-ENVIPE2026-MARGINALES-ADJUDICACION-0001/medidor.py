#!/usr/bin/env python3
"""ADJUDICACION — COMMIT-3a/COMMIT-3, `GEN2-DUELO-ENVIPE2026-MARGINALES-2`.

Único código autorizado a abrir `envipe2026_csv` para este acto
(`FP-260922-GEN2-DUELO-ENVIPE2026-MARGINALES-2-b05c-01`, FIRMADA por mesa
22/sep/2026, verbatim en `spec.yaml::etiquetas.autorizacion_mesa`). R real
de `civico.denuncia.con_seguro × {asegurado, no_asegurado}` (BPCOD='01',
BP1_20∈{1,2}, BP2_1∈{1,2}, FAC_DEL, EST_DIS×UPM_DIS) contra el piso 2025
(COMMIT-2, sha citado en `spec.yaml::inputs`) y el retador TENDENCIA-SERIE
(COMMIT-2 también). No cruza nada, no toca ejes ausentes (nacional, sexo,
edad quedan NO-CONSTRUIBLE en EMISIONES-0001 y no se re-tocan aquí).

Adjudicación por `tools/duelo/cruces_familia.py::adjudica` -- genérica,
"no sabe qué es ENVIPE", no reimplementada -- mapeada al vocabulario del
`spec-v1_0.md` §3 (`VENCE-AL-PISO / PROPUESTA-CON-RESERVA / NO-VENCE /
C-PISO-ADOPTADO / INDECIDIBLE`). El bootstrap de UPM-en-estrato de R usa la
misma receta que `tools/calibracion_mordida_encig_serie.py::
wprop_ic_conglomerado` (verificado en `tests/test_duelo_envipe2026_
marginales_adjudicacion.py` contra esa función, misma semilla): se expone
el vector completo porque esa función sólo devuelve percentiles.

El primer resultado que produzca este procedimiento es el que se reporta.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def _raiz() -> Path:
    p = Path(__file__).resolve()
    for d in p.parents:
        if (d / "tools" / "corrida0.py").exists():
            return d
    raise RuntimeError("raíz del repo no encontrada desde " + str(p))


RAIZ = _raiz()


def _importa(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = mod
    spec.loader.exec_module(mod)
    return mod


MODULOS_SHA_CONGELADO = {
    RAIZ / "tools" / "celda_d" / "marginales_reproduccion.py":
        "4df2c630179c194345594d959d012b7dd18d94ac93fab3f48b8f6683753dafd6",
    RAIZ / "tools" / "duelo" / "cruces_familia.py":
        "a41bdb07d1d975fe84a0b5653232f8532d38c56952c1eafeffd29bae89f9ee3b",
}


def _verifica_dependencias_congeladas():
    for ruta, esperado in MODULOS_SHA_CONGELADO.items():
        real = hashlib.sha256(ruta.read_bytes()).hexdigest()
        if real != esperado:
            raise SystemExit(f"{ruta} cambió desde el sello de COMMIT-3a: "
                             f"esperado {esperado}, encontrado {real}")


_verifica_dependencias_congeladas()
mr = _importa("marginales_reproduccion", RAIZ / "tools" / "celda_d" / "marginales_reproduccion.py")
cf = _importa("cruces_familia", RAIZ / "tools" / "duelo" / "cruces_familia.py")

Z95 = 1.959964
SEED = 42
N_BOOT = 10000
CELDAS = ("ASEGURADO", "NO-ASEGURADO")
BP2_1_CODIGO = {"ASEGURADO": "1", "NO-ASEGURADO": "2"}
COLUMNAS = ("ID_DEL", "BPCOD", "BP1_20", "BP2_1", "FAC_DEL", "EST_DIS", "UPM_DIS")


def _logit(p: float) -> float:
    return float(np.log(p / (1.0 - p)))


def _expit(z):
    return 1.0 / (1.0 + np.exp(-z))


def carga_universo_con_seguro(zip_path, anio: int):
    """SÓLO este medidor llama esta función con datos reales (2026). El
    universo es EXACTAMENTE el de `ARBITRO-MARGINALES-ENVIPE2025-spec-v1_0.md`
    §1: BPCOD='01', BP1_20∈{1,2}, BP2_1∈{1,2}, FAC_DEL válido. Devuelve
    (df filtrado, meta A.13)."""
    df, nombre, enc = mr._lee_miembro(
        Path(zip_path), f"conjunto_de_datos_tmod_vic_envipe{anio}.csv", COLUMNAS)
    n_archivo = len(df)
    m1 = df["BPCOD"] == "01"
    m2 = df["BP1_20"].isin(["1", "2"])
    m3 = df["BP2_1"].isin(["1", "2"])
    w = pd.to_numeric(df["FAC_DEL"], errors="coerce")
    m4 = w.notna() & (w > 0)
    universo = df.loc[m1 & m2 & m3 & m4].copy()
    universo["_w"] = w.loc[universo.index].astype(float)
    meta = {
        "miembro": nombre, "encoding": enc, "filas_archivo": n_archivo,
        "filas_bpcod_01": int(m1.sum()),
        "filas_bpcod_01_bp1_20_valido": int((m1 & m2).sum()),
        "filas_universo": int(len(universo)),
        "filas_excluidas_bp2_1_invalido": int((m1 & m2 & ~m3).sum()),
        "filas_excluidas_fac_del_invalido": int((m1 & m2 & m3 & ~m4).sum()),
    }
    return universo, meta


def _bootstrap_replicas(d, w, estrato, upm, n_boot: int, seed: int):
    """Misma receta de resampleo que `wprop_ic_conglomerado` (UPM con
    reemplazo dentro de estrato, un generador `PCG64(seed)`); se expone el
    vector completo de réplicas porque esa función sólo devuelve
    percentiles. No es un método nuevo -- ver test de equivalencia."""
    d = np.asarray(d, dtype=float)
    w = np.asarray(w, dtype=float)
    llave = pd.Series([f"{e}\x1f{u}" for e, u in zip(estrato, upm)], dtype="object")
    cl_id, _ = pd.factorize(llave)
    n_cl = cl_id.max() + 1
    sw = np.bincount(cl_id, weights=w, minlength=n_cl)
    swd = np.bincount(cl_id, weights=w * d, minlength=n_cl)
    est_de_cl = pd.Series(list(estrato)).groupby(cl_id).first().to_numpy()
    orden = np.argsort(pd.factorize(pd.Series(est_de_cl))[0], kind="stable")
    sw, swd = sw[orden], swd[orden]
    est_ord = pd.factorize(pd.Series(est_de_cl[orden]))[0]
    tam_est = np.bincount(est_ord)
    inicio_est = np.concatenate([[0], np.cumsum(tam_est)[:-1]])
    inicio = inicio_est[est_ord].astype(np.int64)
    tam = tam_est[est_ord].astype(np.int64)
    rng = np.random.Generator(np.random.PCG64(seed))
    idx = inicio + (rng.random((n_boot, len(sw))) * tam).astype(np.int64)
    reps = swd[idx].sum(axis=1) / sw[idx].sum(axis=1)
    return reps, rng


VEREDICTO_MAPA = {
    "VENCE-RETADOR": "VENCE-AL-PISO",
    "PROPUESTA-CON-RESERVA": "PROPUESTA-CON-RESERVA",
    "NO-ADJUDICABLE": "INDECIDIBLE",
}


def _veredicto(delta_mae_pp, veredicto_cf):
    if veredicto_cf == "NADIE-VENCE":
        return "C-PISO-ADOPTADO" if (delta_mae_pp is not None and delta_mae_pp <= 0) else "NO-VENCE"
    return VEREDICTO_MAPA.get(veredicto_cf, "INDECIDIBLE")


def adjudica_celda(universo: pd.DataFrame, celda: str, piso: dict, retador: dict) -> dict:
    sub = universo.loc[universo["BP2_1"] == BP2_1_CODIGO[celda]]
    d = (sub["BP1_20"] == "1").to_numpy(dtype=float)
    w = sub["_w"].to_numpy()
    estrato, upm = sub["EST_DIS"].to_numpy(), sub["UPM_DIS"].to_numpy()
    n = len(sub)
    if n == 0 or w.sum() <= 0:
        return {"n": n, "indecidible": True}
    r_p = float((w * d).sum() / w.sum())
    r_reps, rng = _bootstrap_replicas(d, w, estrato, upm, N_BOOT, SEED)
    ok = np.isfinite(r_reps)
    r_lo, r_hi = float(np.percentile(r_reps[ok], 2.5)), float(np.percentile(r_reps[ok], 97.5))

    se_piso = (_logit(piso["ic_hi"]) - _logit(piso["ic_lo"])) / (2.0 * Z95)
    se_ret = (_logit(retador["ic_hi"]) - _logit(retador["ic_lo"])) / (2.0 * Z95)
    piso_reps = _expit(_logit(piso["p"]) + rng.standard_normal(N_BOOT) * se_piso)
    ret_reps = _expit(_logit(retador["p"]) + rng.standard_normal(N_BOOT) * se_ret)

    R = {"UNICA": cf.Celda(p=r_p, ic95=(r_lo, r_hi), replicas=r_reps, n=n)}
    candidatos = {
        "PISO": {"UNICA": cf.Celda(p=piso["p"], ic95=(piso["ic_lo"], piso["ic_hi"]),
                                    replicas=piso_reps, n=piso.get("n"))},
        "TENDENCIA-SERIE": {"UNICA": cf.Celda(p=retador["p"], ic95=(retador["ic_lo"], retador["ic_hi"]),
                                              replicas=ret_reps, n=None)},
    }
    puntuada = {"UNICA": True}
    out = cf.adjudica(R, candidatos, puntuada, piso="PISO", retador="TENDENCIA-SERIE",
                      umbral_vence_pp=0.5, umbral_reserva_pp=0.0)
    fila = out["candidatos"]["TENDENCIA-SERIE"]
    return {
        "n": n, "indecidible": False,
        "r_p": r_p, "r_ic_lo": r_lo, "r_ic_hi": r_hi,
        "error_piso_pp": 100.0 * (piso["p"] - r_p),
        "error_retador_pp": 100.0 * (retador["p"] - r_p),
        "piso_dentro_ic_r": bool(r_lo <= piso["p"] <= r_hi),
        "retador_dentro_ic_r": bool(r_lo <= retador["p"] <= r_hi),
        "r_dentro_ic_piso": bool(piso["ic_lo"] <= r_p <= piso["ic_hi"]),
        "r_dentro_ic_retador": bool(retador["ic_lo"] <= r_p <= retador["ic_hi"]),
        "delta_mae_pp": fila["delta_mae_pp"],
        "delta_ic_lo": None if fila["delta_ic95"] is None else fila["delta_ic95"][0],
        "delta_ic_hi": None if fila["delta_ic95"] is None else fila["delta_ic95"][1],
        "veredicto": _veredicto(fila["delta_mae_pp"], fila["veredicto"]),
    }


def medir(inputs: dict, contrato: dict) -> dict:
    emisiones = json.loads(inputs["CALC-DUELO-ENVIPE2026-MARGINALES-EMISIONES-0001"]["bytes"].decode("utf-8"))
    em = emisiones.get("resultados", emisiones)
    universo, meta_carga = carga_universo_con_seguro(inputs["envipe2026_csv"]["ruta_absoluta"], 2026)

    out = {}
    for celda in CELDAS:
        base_em = f"RESULT-DUELO-MARGINALES-{celda}"
        piso = {"p": em[base_em + "-PISO-P"], "ic_lo": em[base_em + "-PISO-IC-LO"],
                "ic_hi": em[base_em + "-PISO-IC-HI"], "n": em[base_em + "-PISO-N"]}
        retador = {"p": em[base_em + "-RETADOR-P"], "ic_lo": em[base_em + "-RETADOR-IC-LO"],
                   "ic_hi": em[base_em + "-RETADOR-IC-HI"]}
        r = adjudica_celda(universo, celda, piso, retador)
        base = f"RESULT-DUELO-MARGINALES-ADJ-{celda}"
        if r["indecidible"]:
            for suf in ("R-P", "R-IC-LO", "R-IC-HI", "ERROR-PISO-PP", "ERROR-RETADOR-PP",
                        "DELTA-MAE-PP", "DELTA-IC-LO", "DELTA-IC-HI"):
                out[f"{base}-{suf}"] = None
            for suf in ("PISO-DENTRO-IC-R", "RETADOR-DENTRO-IC-R", "R-DENTRO-IC-PISO", "R-DENTRO-IC-RETADOR"):
                out[f"{base}-{suf}"] = "NO-DEFINIDO"
            out[f"{base}-N"] = r["n"]
            out[f"{base}-VEREDICTO"] = "INDECIDIBLE"
            continue
        out[f"{base}-R-P"] = r["r_p"]
        out[f"{base}-R-IC-LO"] = r["r_ic_lo"]
        out[f"{base}-R-IC-HI"] = r["r_ic_hi"]
        out[f"{base}-N"] = r["n"]
        out[f"{base}-ERROR-PISO-PP"] = r["error_piso_pp"]
        out[f"{base}-ERROR-RETADOR-PP"] = r["error_retador_pp"]
        out[f"{base}-PISO-DENTRO-IC-R"] = "SI" if r["piso_dentro_ic_r"] else "NO"
        out[f"{base}-RETADOR-DENTRO-IC-R"] = "SI" if r["retador_dentro_ic_r"] else "NO"
        out[f"{base}-R-DENTRO-IC-PISO"] = "SI" if r["r_dentro_ic_piso"] else "NO"
        out[f"{base}-R-DENTRO-IC-RETADOR"] = "SI" if r["r_dentro_ic_retador"] else "NO"
        out[f"{base}-DELTA-MAE-PP"] = r["delta_mae_pp"]
        out[f"{base}-DELTA-IC-LO"] = r["delta_ic_lo"]
        out[f"{base}-DELTA-IC-HI"] = r["delta_ic_hi"]
        out[f"{base}-VEREDICTO"] = r["veredicto"]
    out["RESULT-DUELO-MARGINALES-ADJ-G-FILAS-ARCHIVO"] = meta_carga["filas_archivo"]
    out["RESULT-DUELO-MARGINALES-ADJ-G-FILAS-UNIVERSO"] = meta_carga["filas_universo"]
    out["RESULT-DUELO-MARGINALES-ADJ-G-MIEMBRO"] = meta_carga["miembro"]
    return out
