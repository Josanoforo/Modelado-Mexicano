"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENADID (expediente ENADID-2023).

El esquema es el de los dos medidores sellados contendientes (`CALC-ENADID-FAMILIA-HOGARES-0001`:
`columnas_hog/columnas_per("2018")`; `CALC-ENADID-COLA-2018-0001`: `COLS_MUJ/COLS_HOG/COLS_MIG`), que el
medidor de apertura reusa por bytes; la situación conyugal de TSDEM llega como `p3_27` (renombre 2023
declarado). Ramas: con soporte; conducta sin soporte (R None); categoría vacía. Toda salida pasa
`corrida0._valida_outputs` contra `esquema_resultados()` sin no finitos, y el dictamen es del vocabulario.
Auditoría AST limpia y cada mutación de `expediente_apertura.MUTACIONES` detectada.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys
import zipfile

import numpy as np
import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402

REL = "forense/prereg-aperturas/ENADID-2023/medidor_apertura_enadid_2023.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ED = _load(REL, "ap_enadid_2023_t")
F, C, R, L, Mo, PISOS = ED.sellados()


def _ok(out):
    assert corrida0._valida_outputs({"resultados": ED.esquema_resultados()}, out) == []
    assert out[f"{ED.P}-DICTAMEN"] in ED.G.VOCABULARIO
    assert out[f"{ED.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _s(v):
    return [str(x) for x in v]


def _miembros(rng, nh=900):
    """CSV de texto con los nombres de miembro de 2023 (THOGAR, TSDEM, TMUJER2, TMIGRANTE)."""
    llave = [f"{i:08d}" for i in range(nh)]
    est, upm = _s(rng.integers(1, 20, nh)), _s(rng.integers(1, 300, nh))
    tloc = _s(rng.integers(1, 5, nh))
    thogar = pd.DataFrame({"llave_hog": llave, "fac_viv": _s(rng.integers(50, 900, nh)), "est_dis": est, "upm_dis": upm,
                           "tam_loc": tloc, "cls_hog": _s(rng.integers(1, 7, nh)), "sexo_jefe": _s(rng.integers(1, 3, nh)),
                           "edad_jefe": _s(rng.integers(18, 95, nh)), "niv_jefe": _s(rng.integers(0, 12, nh)),
                           "p2_5": _s(rng.integers(1, 8, nh)), "migra_ho": _s(rng.integers(1, 3, nh))})
    reps = rng.integers(1, 6, nh)
    idx = np.repeat(np.arange(nh), reps)
    npers = len(idx)
    paren = np.concatenate([np.r_[1, rng.integers(2, 9, k - 1)] for k in reps])
    tsdem = pd.DataFrame({"llave_hog": [llave[i] for i in idx], "paren": _s(paren), "sexo": _s(rng.integers(1, 3, npers)),
                          "edad": _s(rng.integers(0, 95, npers)), "niv": _s(rng.integers(0, 12, npers)),
                          "p3_21": _s(rng.integers(1, 3, npers)),       # en 2023 es OTRA pregunta: no debe usarse
                          "p3_27": _s(rng.integers(1, 8, npers)),
                          "ent": _s(rng.integers(1, 33, npers)), "tam_loc": [tloc[i] for i in idx],
                          "fac_viv": [thogar["fac_viv"][i] for i in idx], "est_dis": [est[i] for i in idx],
                          "upm_dis": [upm[i] for i in idx]})
    nm = 1200
    tmujer2 = pd.DataFrame({"p10_1": _s(rng.integers(1, 9, nm)), "edad_muj": _s(rng.integers(15, 55, nm)),
                            "tam_loc": _s(rng.integers(1, 5, nm)), "niv": _s(rng.integers(0, 12, nm)),
                            "fac_per": _s(rng.integers(50, 900, nm)), "est_dis": _s(rng.integers(1, 20, nm)),
                            "upm_dis": _s(rng.integers(1, 300, nm))})
    ng = 300
    tmig = pd.DataFrame({"llave_hog": [llave[i] for i in rng.integers(0, nh, ng)], "p4_6": _s(rng.integers(1, 3, ng)),
                         "p4_15": _s(rng.integers(1, 4, ng))})
    return {"THOGAR.csv": thogar, "TSDEM.csv": tsdem, "TMUJER2.csv": tmujer2, "TMIGRANTE.csv": tmig}


def _frames(m):
    """Lo que `medir` entrega a `mide_r` (sin pasar por el lector): columnas pedidas y renombre."""
    por = {"THogar.csv": "THOGAR.csv", "TSdem.csv": "TSDEM.csv", "TMujer2.csv": "TMUJER2.csv",
           "TMigrante.csv": "TMIGRANTE.csv"}
    out = {}
    for clave, miembro, cols, _e, ren in ED.lecturas(F, C):
        out[clave] = m[por[miembro]][cols].rename(columns=ren)
    return out


def _sale(frames, faltan=None):
    return ED.E.salida(ED.P, ED.filas(F, C, Mo, ED.mide_r(F, C, R, Mo, frames, faltan), PISOS))


def test_con_soporte():
    out = _sale(_frames(_miembros(np.random.default_rng(23))))
    _ok(out)
    assert out[f"{ED.P}-N"] > 0
    for k in ("FAM-HOGAR-NUCLEAR-TOTAL-TODOS", "FAM-UNIDO-15MAS-EN-UNION-LIBRE-TOTAL-TODOS",
              "COLA-SEPARADA-ENTRE-UNION-LIBRE-TOTAL-TODOS", "COLA-JEFATURA-FEMENINA-CON-MIGRANTE-VARON-TOTAL-TODOS"):
        assert out[f"{ED.P}-{k}-R"] is not None, k


def test_conyugal_sale_de_p3_27():
    m = _miembros(np.random.default_rng(24))
    m["TSDEM.csv"]["p3_27"] = "7"                        # todos solteros en la variable 2023
    out = _sale(_frames(m))
    _ok(out)
    assert out[f"{ED.P}-FAM-PERSONA-15MAS-UNIDA-TOTAL-TODOS-R"] == 0.0
    assert out[f"{ED.P}-FAM-UNIDO-15MAS-EN-UNION-LIBRE-TOTAL-TODOS-R"] is None


def test_sin_soporte_y_categoria_vacia():
    m = _miembros(np.random.default_rng(25))
    m["THOGAR.csv"]["cls_hog"] = ""                      # tipo de hogar sin soporte
    m["TMUJER2.csv"]["tam_loc"] = "1"                    # TAMLOC de mujeres: MENOS-2500 vacía
    fr = _frames(m)
    fr["COLA-MIG"]["p4_15"] = ""
    out = _sale(fr, {"COLA-MIG": ["p4_15"]})             # sin p4_15 no hay universo de jefatura con/sin migrante
    _ok(out)
    assert out[f"{ED.P}-FAM-HOGAR-NUCLEAR-TOTAL-TODOS-R"] is None
    assert out[f"{ED.P}-COLA-SEPARADA-ENTRE-UNION-LIBRE-TAMLOC-MENOS-2500-R"] is None
    assert out[f"{ED.P}-COLA-SEPARADA-ENTRE-UNION-LIBRE-TAMLOC-100MIL-MAS-R"] is not None
    assert out[f"{ED.P}-COLA-JEFATURA-FEMENINA-SIN-MIGRANTE-VARON-TOTAL-TODOS-R"] is None


def test_apartadas_no_se_puntuan():
    fl = ED.filas(F, C, Mo, {}, PISOS)
    ap = [f for f in fl if f["id"].startswith(("FAM-PERSONA-15MAS-UNIDA-SEXO", "FAM-UNIDO-15MAS-EN-UNION-LIBRE-TOTAL"))]
    assert ap and all(f["lo"] is None and f["hi"] is None for f in ap)
    assert {f["conglomerado"] for f in fl} == set(ED.CONTRATO["contendientes"])


# ── extremo a extremo: CSV en ZIP con los miembros de 2023 ──────────────────────────────────────
def _inputs(tmp_path, m, nombre="base_datos_enadid23_csv.zip"):
    z = tmp_path / nombre
    with zipfile.ZipFile(z, "w") as zf:
        for miembro, df in m.items():
            zf.writestr(miembro, df.to_csv(index=False, lineterminator="\r\n"))
    inp = {ED.PAYLOAD: {"ruta_absoluta": str(z)}}
    inp.update({k: {} for k, _r, _n in ED.CONTRATO["repo"]})
    return inp


def test_medir_extremo_a_extremo_columna_ausente(tmp_path):
    m = _miembros(np.random.default_rng(26), nh=400)
    m["TMIGRANTE.csv"] = m["TMIGRANTE.csv"].drop(columns=["p4_15"])
    m["THOGAR.csv"] = m["THOGAR.csv"].drop(columns=["migra_ho"])
    out = ED.medir(_inputs(tmp_path, m), {})
    _ok(out)
    assert out[f"{ED.P}-COLA-JEFATURA-FEMENINA-CON-MIGRANTE-VARON-TOTAL-TODOS-R"] is None
    assert out[f"{ED.P}-COLA-JEFATURA-FEMENINA-SIN-MIGRANTE-VARON-TOTAL-TODOS-R"] is None
    assert out[f"{ED.P}-FAM-HOGAR-CON-MIGRANTE-INTERNACIONAL-5A-TOTAL-TODOS-R"] is None
    assert out[f"{ED.P}-FAM-HOGAR-NUCLEAR-TOTAL-TODOS-R"] is not None


def test_medir_paro_por_diseno_ausente(tmp_path):
    m = _miembros(np.random.default_rng(27), nh=100)
    m["THOGAR.csv"] = m["THOGAR.csv"].drop(columns=["upm_dis"])
    with pytest.raises(ED.G.ParoDeGuardia):
        ED.medir(_inputs(tmp_path, m), {})


def test_medir_paro_si_no_es_2023(tmp_path):
    m = _miembros(np.random.default_rng(28), nh=100)
    with pytest.raises(ED.G.ParoDeGuardia):
        ED.medir(_inputs(tmp_path, m, nombre="base_datos_enadid18_csv.zip"), {})


# ── guardia E.6 ─────────────────────────────────────────────────────────────
def test_auditoria_limpia_y_mutaciones():
    fuente = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert ED.G.auditoria_ast(fuente) == []
    for mut in ED.E.MUTACIONES:
        assert ED.G.auditoria_ast(fuente + "\n\n" + mut), mut
