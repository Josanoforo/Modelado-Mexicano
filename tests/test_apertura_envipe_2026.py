"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENVIPE (tper_vic1 + tsdem) para el
expediente de apertura de la reserva restante de ENVIPE 2026.

El esquema es el del medidor sellado del contendiente (`COLS_PER`: ID_PER, AP4_3_3, AP4_4_A, AP4_10_02, SEXO,
EDAD, CVE_ENT, DOMINIO, FAC_ELE, EST_DIS, UPM_DIS; `COLS_SDEM`: ID_PER, NIV). Se fabrica un ZIP con la
estructura de datos abiertos (carpeta por tabla, más `tmod_vic`, que el medidor no lee) y se corre la
lectura real. Ramas: con soporte; conducta sin soporte (columna ausente → R None); categoría vacía;
estructura ausente → PARO. Toda salida pasa `corrida0._valida_outputs`, sin no finitos, dictamen del
vocabulario; auditoría AST limpia y cada mutación detectada.

Segundo contendiente (CALC-MC2-ENVIPE2025-0001): el ZIP trae además las columnas de su medidor sellado
(`COLS_PER24`/`COLS_PER25` en tper_vic1; `COLS_DEL` en tmod_vic). Ramas: con soporte (PROSPECTIVA puntúa,
RETROSPECTIVA y DUPLICADA emiten R sin puntuar), desenlace sin columna (R None), categoría vacía, estructura
ausente → PARO, fin de línea `\r` solo; R de MC2 contra un cálculo directo y la DUPLICADA contra su gemelo.
"""
from __future__ import annotations

import importlib.util
import io
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

REL = "forense/prereg-aperturas/ENVIPE-2026/medidor_apertura_envipe_2026.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AP = _load(REL, "ap_envipe_2026_t")
MC2 = _load("data/corrida0/CALC-MC2-ENVIPE2025-0001/medidor.py", "mc2_envipe2025_t")


def _ok(out):
    assert corrida0._valida_outputs({"resultados": AP.esquema_resultados()}, out) == []
    assert out[f"{AP.P}-DICTAMEN"] in AP.G.VOCABULARIO
    assert out[f"{AP.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _tablas(rng, n, quitar=(), dominio=None, quitar_del=()):
    ids = [f"{i:08d}01" for i in range(n)]
    per = pd.DataFrame({"ID_PER": ids, "AP4_3_3": rng.choice([1, 2, 9], n), "AP4_4_A": rng.choice([1, 2, 3, 4, 9], n),
                        "AP4_10_02": rng.choice([1, 2, 3], n), "SEXO": rng.integers(1, 3, n), "EDAD": rng.integers(18, 98, n),
                        "CVE_ENT": rng.integers(1, 33, n),
                        "DOMINIO": (np.full(n, dominio) if dominio else rng.choice(["U", "C", "R"], n)),
                        "FAC_ELE": rng.integers(100, 3000, n), "EST_DIS": rng.integers(1, 90, n),
                        "UPM_DIS": rng.integers(1, 900, n)})
    # columnas del medidor sellado de MC2 (AP4_2_*: 1 marcado / blanco; AP4_4_*: 1 seguro, 2 inseguro)
    for c in MC2.AP42:
        per[c] = rng.choice(["1", ""], n, p=[0.3, 0.7])
    for c in MC2.AP44.values():
        per[c] = rng.choice([1, 2, 3, 9], n)
    per["AP4_10_01"] = rng.choice([1, 2, 3], n)
    per = per.drop(columns=list(quitar))
    sdem = pd.DataFrame({"ID_PER": ids, "NIV": rng.integers(0, 10, n)})
    m = 2 * n
    dl = pd.DataFrame({"ID_PER": rng.choice(ids, m), "EST_DIS": rng.integers(1, 90, m), "UPM_DIS": rng.integers(1, 900, m),
                       "DOMINIO": (np.full(m, dominio) if dominio else rng.choice(["U", "C", "R"], m)),
                       "FAC_DEL": rng.integers(100, 3000, m), "SEXO": rng.integers(1, 3, m),
                       "BPCOD": rng.choice(["01", "05", "09", "10"], m), "BP1_20": rng.choice([1, 2, 9], m, p=[.1, .85, .05]),
                       "BP1_21": rng.choice([1, 2, 9], m), "BP1_24": rng.choice([1, 2, 9], m),
                       "BP1_5A_2": rng.choice([0, 1], m)}).drop(columns=list(quitar_del))
    return per, sdem, dl


def _zip(tmp_path, per, sdem, dl, fin="\n"):
    ruta = tmp_path / "conjunto_de_datos_ENVIPE_2026_csv.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        for tabla, df in (("tper_vic1", per), ("tsdem", sdem), ("tmod_vic", dl)):
            buf = io.StringIO()
            df.to_csv(buf, index=False, lineterminator=fin)
            z.writestr(f"{tabla}_envipe2026/conjunto_de_datos/conjunto_de_datos_{tabla}_envipe2026.csv", buf.getvalue())
    return str(ruta)


def _corre(tmp_path, fin="\n", **kw):
    S, R, M, piso = AP.sellados()
    S2, piso2 = AP.sellados_mc2()
    t = _tablas(np.random.default_rng(2026), 5000, **kw)
    L = AP.lee_payload_reservado(S, R, S2, _zip(tmp_path, *t, fin=fin))
    r = AP.mide_r(S, M, L["per"], L["sdem"])
    r2 = AP.mide_r_mc2(S2, piso2, L["mc2"], L["ausentes_mc2"])
    return AP.E.salida(AP.P, AP.filas(S, M, r, piso) + AP.filas_mc2(S2, r2, piso2)), t


def _n_puntuables():
    S, _R, _M, _p = AP.sellados()
    S2, piso2 = AP.sellados_mc2()
    return len(AP.celdas_de(S)) + sum(1 for _b, c in AP.celdas_mc2(S2, piso2) if c == "PROSPECTIVA")


def test_envipe_con_soporte(tmp_path):
    out, _t = _corre(tmp_path)
    _ok(out)
    assert 0 < out[f"{AP.P}-N"] <= _n_puntuables()
    assert out[f"{AP.P}-ESTADO-INSEGURO-ESCOLARIDAD-SUPERIOR-R"] is not None
    for cid in ("MC2-PREOC-AGUA-2024-DOM-R", "MC2-INSEGURO-CALLE-2024-EDAD-60-MAS", "MC2-DEJO-SALIR-NOCHE-2024-NAC",
                "MC2-RETROSPECTIVA-DEL-CIFRA-NEGRA-DOM-C", "MC2-RETROSPECTIVA-DEL-EXT-TELEFONICA-MUJER",
                "MC2-DUPLICADA-EDO-INSEGURO-2025-SINALOA"):
        assert out[f"{AP.P}-{cid}-R"] is not None, cid


def test_envipe_mc2_sin_soporte_y_categoria_vacia(tmp_path):
    out, _t = _corre(tmp_path, quitar=("AP4_10_02", "AP4_2_99"), dominio="U", quitar_del=("BP1_5A_2",))
    _ok(out)
    assert out[f"{AP.P}-DEJO-PERMITIR-MENORES-SALIR-SOLOS-TOTAL-TODOS-R"] is None
    assert out[f"{AP.P}-ESTADO-INSEGURO-DOMINIO-RURAL-R"] is None
    assert out[f"{AP.P}-ESTADO-INSEGURO-DOMINIO-URBANO-R"] is not None
    assert out[f"{AP.P}-MC2-PREOC-INSEGURIDAD-2024-NAC-R"] is None          # AP4_2_99 ausente -> NO-ESTIMABLE
    assert out[f"{AP.P}-MC2-RETROSPECTIVA-DEL-EXT-TELEFONICA-NAC-R"] is None
    assert out[f"{AP.P}-MC2-RETROSPECTIVA-DEL-DENUNCIA-NAC-R"] is not None
    assert out[f"{AP.P}-MC2-INSEGURO-BANCO-2024-DOM-R-R"] is None           # categoría vacía
    assert out[f"{AP.P}-MC2-INSEGURO-BANCO-2024-DOM-U-R"] is not None


def test_envipe_fin_de_linea_retorno(tmp_path):
    out, _t = _corre(tmp_path, fin="\r")
    _ok(out)
    assert out[f"{AP.P}-MC2-PREOC-AGUA-2024-NAC-R"] is not None
    assert out[f"{AP.P}-ESTADO-INSEGURO-TOTAL-TODOS-R"] is not None


def test_envipe_mc2_r_contra_calculo_directo(tmp_path):
    """R de MC2 recalculado a mano sobre el sintético (sin su código): la ranura 2026 no desplaza nada."""
    out, (per, _sdem, dl) = _corre(tmp_path)
    w = per["FAC_ELE"].astype(float)
    y = (per["AP4_2_07"] == "1").astype(float).where(per["AP4_2_99"] != "1")
    m = y.notna() & (per["DOMINIO"] == "R")
    assert out[f"{AP.P}-MC2-PREOC-AGUA-2024-DOM-R-R"] == pytest.approx(float((w[m] * y[m]).sum() / w[m].sum()), abs=1e-12)
    y = per[MC2.AP44["CALLE"]].map({2: 1.0, 1: 0.0})
    m = y.notna() & (per["EDAD"] >= 60) & (per["EDAD"] <= 97)
    assert out[f"{AP.P}-MC2-INSEGURO-CALLE-2024-EDAD-60-MAS-R"] == pytest.approx(
        float((w[m] * y[m]).sum() / w[m].sum()), abs=1e-12)
    wd = dl["FAC_DEL"].astype(float)
    val = dl["BP1_20"].isin([1, 2])
    den = (dl["BP1_20"] == 1) | (dl["BP1_21"] == 1)
    y = (~(den & (dl["BP1_24"] == 1))).astype(float).where(val)
    m = y.notna() & (dl["SEXO"] == 2)
    assert out[f"{AP.P}-MC2-RETROSPECTIVA-DEL-CIFRA-NEGRA-MUJER-R"] == pytest.approx(
        float((wd[m] * y[m]).sum() / wd[m].sum()), abs=1e-12)


def test_envipe_duplicada_igual_a_su_gemelo(tmp_path):
    """Con EDAD en 18-97 (el sintético), la DUPLICADA de MC2 y su gemelo de PERCEPCION dan el mismo R: por eso
    no se cuentan dos veces."""
    out, _t = _corre(tmp_path)
    S2, piso2 = AP.sellados_mc2()
    dups = [b for b, c in AP.celdas_mc2(S2, piso2) if c == "DUPLICADA"]
    assert dups
    for b in dups:
        assert out[f"{AP.P}-MC2-DUPLICADA-{b}-R"] == pytest.approx(out[f"{AP.P}-{AP.gemelo_percepcion(b)}-R"], abs=1e-12)


def test_envipe_rejilla_mc2_del_arbitro():
    """Toda celda de MC2 se clasifica; sólo PROSPECTIVA lleva lo/hi; DELITO sin punto; columnas declaradas ⊂
    columnas que su medidor lee."""
    S2, piso2 = AP.sellados_mc2()
    todas = AP.bases_mc2(S2, piso2)
    celdas = AP.celdas_mc2(S2, piso2)
    assert len(todas) - len(celdas) == len(AP.APARTA_MC2) + 1     # EDO-INSEGURO-2024 NAC/SINALOA + DIF
    cols = AP.cols_mc2(S2)
    for b, _c in celdas:
        tabla, cs = AP.columnas_mc2(S2, b)
        assert set(cs) <= set(cols[tabla]), b
    filas = {f["id"]: f for f in AP.filas_mc2(S2, {b: 0.5 for b in todas}, piso2)}
    for b, c in celdas:
        f = filas[AP._cid_mc2(b, c)]
        assert (f["lo"] is not None) == (c == "PROSPECTIVA"), b
        assert (f["punto"] is None) == b.startswith(AP.RETRO_MC2), b


def test_envipe_estructura_ausente_es_paro(tmp_path):
    S, R, _M, _p = AP.sellados()
    S2, _p2 = AP.sellados_mc2()
    per, sdem, dl = _tablas(np.random.default_rng(1), 50, quitar=("FAC_ELE",))
    with pytest.raises(AP.G.ParoDeGuardia):
        AP.lee_payload_reservado(S, R, S2, _zip(tmp_path, per, sdem, dl))
    per, sdem, dl = _tablas(np.random.default_rng(1), 50, quitar_del=("FAC_DEL",))
    with pytest.raises(AP.G.ParoDeGuardia):
        AP.lee_payload_reservado(S, R, S2, _zip(tmp_path, per, sdem, dl))


def test_envipe_medir_completo(tmp_path):
    """`medir()` de punta a punta: auditoría, chequeo exacto de inputs, lectura única y salida validada."""
    t = _tablas(np.random.default_rng(7), 800)
    inputs = {k: {} for k, _r, _n in AP.CONTRATO["repo"]}
    inputs[AP.PAYLOAD] = {"ruta_absoluta": _zip(tmp_path, *t)}
    _ok(AP.medir(inputs, {}))


def test_envipe_auditoria_y_mutaciones():
    src = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert AP.G.auditoria_ast(src) == []
    for mut in AP.E.MUTACIONES:
        assert AP.G.auditoria_ast(src + "\n\n" + mut), mut
