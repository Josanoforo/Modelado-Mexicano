"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026): guardia E.6 de apertura por mutación.

Defecto real que atrapa: NC-0328 (reserva quemada por un cruce de scratch). Sin microdato:
sintético con el esquema de cada ola (el del medidor sellado que la apertura reusa).

  · los medidores de apertura pasan la auditoría AST;
  · cada MUTACIÓN (groupby de dos llaves, crosstab, pivot_table, lectura fuera del lector
    autorizado, borrar la llamada a la auditoría) es detectada;
  · `proporcion_por_grupo` rechaza un cruce; la adjudicación cubre sus cuatro dictámenes;
  · sobre sintético, cada medidor produce R finito y un dictamen del vocabulario cerrado;
  · la vista `aperturas-pendientes-v1_0.tsv` cubre toda ola reservada del manifiesto y ningún
    payload reservado figura en la lista de archivos leídos de la nota.
"""
from __future__ import annotations

import ast
import csv
import importlib.util
import math
import os

import numpy as np
import pandas as pd
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AP = os.path.join(ROOT, "forense", "prereg-aperturas")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G = _load("forense/prereg-aperturas/guardia_apertura.py", "guardia_apertura_t")
ENS = _load("forense/prereg-aperturas/ENSANUT-2025/medidor_apertura_ensanut_2025.py", "ap_ensanut")
ENC = _load("forense/prereg-aperturas/ENCODAT-2025/medidor_apertura_encodat_2025.py", "ap_encodat")
MEDIDORES = ["forense/prereg-aperturas/ENSANUT-2025/medidor_apertura_ensanut_2025.py", "forense/prereg-aperturas/ENCODAT-2025/medidor_apertura_encodat_2025.py"]


def _src(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


@pytest.mark.parametrize("rel", MEDIDORES)
def test_auditoria_limpia(rel):
    assert G.auditoria_ast(_src(rel)) == []


MUTACIONES = [
    "def _m(df):\n    return df.groupby(['sexo', 'edad']).size()\n",
    "def _m(df):\n    return df.groupby(by=('sexo', 'estrato')).mean()\n",
    "def _m(df):\n    return df.value_counts(subset=['a', 'b'])\n",
    "import pandas as pd\ndef _m(df):\n    return pd.crosstab(df.a, df.b)\n",
    "def _m(df):\n    return df.pivot_table(index='a', columns='b')\n",
    "def _m(df):\n    return df.unstack()\n",
    "import pandas as pd\ndef _m(r):\n    return pd.read_stata(r)\n",
    "def _m(R, r):\n    return R.lee_dta(r, [])\n",
]


@pytest.mark.parametrize("rel", MEDIDORES)
@pytest.mark.parametrize("mut", MUTACIONES)
def test_mutacion_detectada(rel, mut):
    assert G.auditoria_ast(_src(rel) + "\n\n" + mut), mut


@pytest.mark.parametrize("rel", MEDIDORES)
def test_mutacion_sin_auditoria_detectada(rel):
    """Borrar la llamada a exige_auditoria de medir() es una mutación que este test mata."""
    arbol = ast.parse(_src(rel))
    medir = next(n for n in arbol.body if isinstance(n, ast.FunctionDef) and n.name == "medir")
    llama = [n for n in ast.walk(medir) if isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "exige_auditoria"]
    assert llama and medir.body[0].value is llama[0]  # primera sentencia, antes de leer nada


def test_proporcion_rechaza_cruce():
    y, w = np.array([1.0, 0.0, 1.0]), np.ones(3)
    with pytest.raises(G.ParoDeGuardia):
        G.proporcion_por_grupo(y, w, [np.array(["a", "b", "a"]), np.array(["x", "x", "y"])])
    with pytest.raises(G.ParoDeGuardia):
        G.proporcion_por_grupo(y, w, np.array([["a", "x"], ["b", "x"], ["a", "y"]]))
    r = G.proporcion_por_grupo(y, w, np.array(["a", "b", "a"], dtype=object))
    assert r["a"]["p"] == 1.0 and r["b"]["p"] == 0.0


def test_adjudicacion_cuatro_ramas():
    def cs(k, n):
        return [{"lo": 0.0, "hi": 1.0, "r": 0.5 if i < k else 2.0, "punto": 0.5} for i in range(n)]
    assert G.adjudica_cobertura([])["dictamen"] == "NO-ESTIMABLE"
    assert G.adjudica_cobertura([{"lo": None, "hi": 1, "r": 0.2}])["dictamen"] == "NO-ESTIMABLE"
    assert G.adjudica_cobertura(cs(95, 100))["dictamen"] == "CALIBRADO"
    assert G.adjudica_cobertura(cs(50, 100))["dictamen"] == "SUBCUBRE"
    assert G.adjudica_cobertura(cs(1000, 1000))["dictamen"] == "SOBRECUBRE"


# ── sintético con el esquema de cada ola ─────────────────────────────────────

def _fr_ensanut(M, rng, arch, n):
    d = {"folio_i": rng.integers(1, max(2, n // 3), n).astype(str), "folio_int": rng.integers(1, 4, n).astype(str),
         "ponde_f": rng.uniform(50, 500, n), "est_sel": rng.integers(1, 40, n).astype(str),
         "upm": rng.integers(1, 300, n).astype(str), "estrato": rng.integers(1, 4, n)}
    for c in M.COLS[arch]:
        if c not in d:
            d[c] = rng.integers(1, 5, n).astype(float)
    if "edad" in d:
        d["edad"] = rng.integers(10, 20, n) if arch == "ADOL" else rng.integers(20, 90, n)
    if "h0303" in d:
        d["h0303"] = rng.integers(0, 90, n)
    if "h0317a" in d:
        d["h0317a"] = rng.integers(1, 13, n).astype(float)
    if "u0201" in d:
        d["u0201"] = rng.integers(1, 27, n).astype(float)
    return pd.DataFrame(d)


def _dictamen_ok(out, P):
    assert out[f"{P}-DICTAMEN"] in G.VOCABULARIO
    assert out[f"{P}-MARCA"] == "PROSPECTIVA"
    for k, v in out.items():
        if isinstance(v, float):
            assert math.isfinite(v), k


def test_ensanut_sintetico():
    M, R, piso = ENS.sellados()
    rng = np.random.default_rng(28)
    frames = {a: _fr_ensanut(M, rng, a, 6000 if a == "INTE" else 2000) for a in ENS.PAYLOADS}
    out = ENS.salida(M, piso, ENS.mide_r(M, R, frames))
    _dictamen_ok(out, ENS.P)
    assert out[f"{ENS.P}-N"] > 0


def test_encodat_sintetico():
    M, R, piso = ENC.sellados()
    rng = np.random.default_rng(29)
    nh = 1200
    hog = pd.DataFrame({"id_hogar": [f"{i:020d}" for i in range(nh)], "estrato": rng.integers(1, 4, nh),
                        "est_var": rng.integers(1, 30, nh), "code_upm": rng.integers(1, 300, nh).astype(str)})
    n = 3000
    hid = rng.integers(0, nh, n)
    ind = pd.DataFrame({"id_pers": [f"{h:020d}{k:02d}" for h, k in zip(hid, rng.integers(1, 5, n))],
                        "ponde_ss": rng.uniform(1, 9, n), "ds2": rng.integers(1, 3, n), "ds3": rng.integers(10, 70, n),
                        "ds9": rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9], n)})
    for c in M.COLS_IND:
        if c not in ind:
            ind[c] = rng.choice([1, 2, 9], n).astype(float)
    out = ENC.salida(M, piso, ENC.mide_r(M, R, {"IND": ind, "HOG": hog}))
    _dictamen_ok(out, ENC.P)
    assert out[f"{ENC.P}-N"] > 0


@pytest.mark.parametrize("Mod", [ENS, ENC])
def test_medir_rechaza_input_ajeno(Mod):
    with pytest.raises(Mod.G.ParoDeGuardia):
        Mod.medir({"otro_payload": {"ruta_absoluta": "/nada"}}, {})


# ── vista y lista de leídos ─────────────────────────────────────────────────

VISTA = os.path.join(ROOT, "data", "corrida0", "aperturas-pendientes-v1_0.tsv")


def _vista():
    with open(VISTA, encoding="utf-8") as f:
        return list(csv.DictReader((x for x in f if not x.startswith("#")), delimiter="\t"))


def test_vista_cubre_toda_reservada():
    inv = _load("forense/prereg-aperturas/inventario_aperturas.py", "ap_inventario")
    reservados = set(inv.reservados_del_manifiesto())
    en_vista = {i for fila in _vista() for i in fila["ids"].split(";") if i}
    assert reservados and reservados - en_vista == set()


def test_vista_casa_con_la_derivacion():
    inv = _load("forense/prereg-aperturas/inventario_aperturas.py", "ap_inventario3")
    assert inv.main(["--verifica"]) == 0


def test_expediente_completo_donde_hay_contendiente():
    for fila in _vista():
        if fila["contendientes"] and fila["contendientes"] != "NINGUNO":
            d = os.path.join(ROOT, fila["expediente"])
            b = os.path.basename(d)
            for nombre in (f"APERTURA-{b}-spec-v1_0.md", f"APERTURA-{b}-spec.yaml", f"RECETA-APERTURA-{b}.md"):
                assert os.path.exists(os.path.join(d, nombre)), (fila["programa"], nombre)


def test_ningun_payload_reservado_leido():
    inv = _load("forense/prereg-aperturas/inventario_aperturas.py", "ap_inventario2")
    reservados = set(inv.reservados_del_manifiesto())
    archivos = set(inv.archivos_reservados_del_manifiesto())
    leidos = open(os.path.join(AP, "archivos-leidos-v1_0.txt"), encoding="utf-8").read().split()
    assert not (set(leidos) & (reservados | archivos))
