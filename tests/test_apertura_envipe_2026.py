"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1: sintético con el esquema de ENVIPE (tper_vic1 + tsdem) para el
expediente de apertura de la reserva restante de ENVIPE 2026.

El esquema es el del medidor sellado del contendiente (`COLS_PER`: ID_PER, AP4_3_3, AP4_4_A, AP4_10_02, SEXO,
EDAD, CVE_ENT, DOMINIO, FAC_ELE, EST_DIS, UPM_DIS; `COLS_SDEM`: ID_PER, NIV). Se fabrica un ZIP con la
estructura de datos abiertos (carpeta por tabla, más `tmod_vic`, que el medidor no lee) y se corre la
lectura real. Ramas: con soporte; conducta sin soporte (columna ausente → R None); categoría vacía;
estructura ausente → PARO. Toda salida pasa `corrida0._valida_outputs`, sin no finitos, dictamen del
vocabulario; auditoría AST limpia y cada mutación detectada.
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


def _ok(out):
    assert corrida0._valida_outputs({"resultados": AP.esquema_resultados()}, out) == []
    assert out[f"{AP.P}-DICTAMEN"] in AP.G.VOCABULARIO
    assert out[f"{AP.P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        assert not isinstance(v, float) or math.isfinite(v), k


def _tablas(rng, n, quitar=(), dominio=None):
    ids = [f"{i:08d}01" for i in range(n)]
    per = pd.DataFrame({"ID_PER": ids, "AP4_3_3": rng.choice([1, 2, 9], n), "AP4_4_A": rng.choice([1, 2, 3, 4, 9], n),
                        "AP4_10_02": rng.choice([1, 2, 3], n), "SEXO": rng.integers(1, 3, n), "EDAD": rng.integers(18, 98, n),
                        "CVE_ENT": rng.integers(1, 33, n),
                        "DOMINIO": (np.full(n, dominio) if dominio else rng.choice(["U", "C", "R"], n)),
                        "FAC_ELE": rng.integers(100, 3000, n), "EST_DIS": rng.integers(1, 90, n),
                        "UPM_DIS": rng.integers(1, 900, n)}).drop(columns=list(quitar))
    sdem = pd.DataFrame({"ID_PER": ids, "NIV": rng.integers(0, 10, n)})
    return per, sdem


def _zip(tmp_path, per, sdem):
    ruta = tmp_path / "conjunto_de_datos_ENVIPE_2026_csv.zip"
    with zipfile.ZipFile(ruta, "w") as z:
        for tabla, df in (("tper_vic1", per), ("tsdem", sdem)):
            buf = io.StringIO()
            df.to_csv(buf, index=False)
            z.writestr(f"{tabla}_envipe2026/conjunto_de_datos/conjunto_de_datos_{tabla}_envipe2026.csv", buf.getvalue())
        z.writestr("tmod_vic_envipe2026/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2026.csv", "ID_PER,BP1_20\n")
    return str(ruta)


def _corre(tmp_path, **kw):
    S, R, M, piso = AP.sellados()
    per, sdem = AP.lee_payload_reservado(S, R, _zip(tmp_path, *_tablas(np.random.default_rng(2026), 5000, **kw)))
    return AP.E.salida(AP.P, AP.filas(S, M, AP.mide_r(S, M, per, sdem), piso))


def test_envipe_con_soporte(tmp_path):
    out = _corre(tmp_path)
    _ok(out)
    assert out[f"{AP.P}-N"] > 0
    assert out[f"{AP.P}-ESTADO-INSEGURO-ESCOLARIDAD-SUPERIOR-R"] is not None


def test_envipe_sin_soporte_y_categoria_vacia(tmp_path):
    out = _corre(tmp_path, quitar=("AP4_10_02",), dominio="U")
    _ok(out)
    assert out[f"{AP.P}-DEJO-PERMITIR-MENORES-SALIR-SOLOS-TOTAL-TODOS-R"] is None
    assert out[f"{AP.P}-ESTADO-INSEGURO-DOMINIO-RURAL-R"] is None
    assert out[f"{AP.P}-ESTADO-INSEGURO-DOMINIO-URBANO-R"] is not None


def test_envipe_estructura_ausente_es_paro(tmp_path):
    S, R, _M, _p = AP.sellados()
    per, sdem = _tablas(np.random.default_rng(1), 50, quitar=("FAC_ELE",))
    with pytest.raises(AP.G.ParoDeGuardia):
        AP.lee_payload_reservado(S, R, _zip(tmp_path, per, sdem))


def test_envipe_auditoria_y_mutaciones():
    src = open(os.path.join(ROOT, REL), encoding="utf-8").read()
    assert AP.G.auditoria_ast(src) == []
    for mut in AP.E.MUTACIONES:
        assert AP.G.auditoria_ast(src + "\n\n" + mut), mut
