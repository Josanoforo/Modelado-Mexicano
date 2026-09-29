"""ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026): guardia E.6 de apertura y contrato de TODO expediente.

Defecto real que atrapa: NC-0328 (reserva quemada por un cruce de scratch) y los actos perdidos del piloto 3
(D-22: un conducto que no acepta una rama terminal). Sin microdato. Recorre toda carpeta
`forense/prereg-aperturas/<X>/` con `medidor_apertura_*.py`:

  · el medidor pasa la auditoría AST y CADA mutación de `expediente_apertura.MUTACIONES` es detectada;
    borrar la llamada a la auditoría (primera sentencia de `medir`) también;
  · el contrato `APERTURA-<X>-spec.yaml` y la receta casan con su derivación, traen los campos
    obligatorios de `corrida0`, `resultados` == `esquema_resultados()`, y cada input tiene sha;
  · `corrida0._valida_outputs` acepta la salida de cada rama terminal de la adjudicación (todas con soporte,
    parcial, cero puntuadas, sin IC en el contendiente) sin None fuera de lo permitido ni no finitos;
  · `medir` rechaza un input fuera de su lista;
  · la vista cubre toda ola reservada y todo contendiente declarado, y ningún payload reservado figura en la
    lista de leídos.
Los sintéticos con el esquema de cada ola viven en `tests/test_apertura_*.py`.
"""
from __future__ import annotations

import ast
import csv
import glob
import importlib.util
import math
import os
import sys

import numpy as np
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AP = os.path.join(ROOT, "forense", "prereg-aperturas")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


E = _load("forense/prereg-aperturas/expediente_apertura.py", "expediente_apertura_t")
G = E.G
MEDIDORES = sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(AP, "*", "medidor_apertura_*.py")))
MODS = {rel: _load(rel, "t_" + os.path.basename(rel)[:-3]) for rel in MEDIDORES}


def _src(rel):
    return open(os.path.join(ROOT, rel), encoding="utf-8").read()


def test_hay_expedientes():
    assert len(MEDIDORES) >= 2


@pytest.mark.parametrize("rel", MEDIDORES)
def test_auditoria_limpia(rel):
    assert G.auditoria_ast(_src(rel)) == []


@pytest.mark.parametrize("rel", MEDIDORES)
@pytest.mark.parametrize("mut", E.MUTACIONES)
def test_mutacion_detectada(rel, mut):
    assert G.auditoria_ast(_src(rel) + "\n\n" + mut), mut


@pytest.mark.parametrize("rel", MEDIDORES)
def test_auditoria_es_la_primera_sentencia(rel):
    arbol = ast.parse(_src(rel))
    medir = next(n for n in arbol.body if isinstance(n, ast.FunctionDef) and n.name == "medir")
    primera = medir.body[0]
    assert isinstance(primera, ast.Expr) and isinstance(primera.value, ast.Call)
    assert getattr(primera.value.func, "attr", "") == "exige_auditoria"
    lectores = [n.name for n in arbol.body if isinstance(n, ast.FunctionDef) and n.name == G.LECTOR_AUTORIZADO]
    assert lectores == [G.LECTOR_AUTORIZADO]


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


def test_contratos_y_recetas_casan():
    esc = _load("forense/prereg-aperturas/escribe_expedientes.py", "escribe_expedientes_t")
    assert esc.main(["--verifica"]) == 0


@pytest.mark.parametrize("rel", MEDIDORES)
def test_contrato_corrida0(rel):
    M = MODS[rel]
    x = M.CONTRATO["x"]
    with open(os.path.join(ROOT, E.ruta_contrato(x)), encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    for campo in corrida0.CAMPOS_SPEC_OBLIGATORIOS:
        assert spec.get(campo) not in (None, "", [], {}), campo
    assert spec["resultados"] == M.esquema_resultados()
    assert spec["script"] == rel
    assert os.path.normpath(os.path.join(ROOT, "data", "corrida0", spec["calc_id"], spec["spec_md"])) == \
        os.path.join(AP, x, f"APERTURA-{x}-spec-v1_0.md")
    for e in spec["inputs"]:
        assert len(str(e["sha256"])) == 64, e["id"]
    assert M.CONTRATO["contendientes"] and all(
        os.path.isdir(os.path.join(ROOT, "data", "corrida0", c)) for c in M.CONTRATO["contendientes"])


def _ramas(celdas):
    rng = np.random.default_rng(5)
    base = [{"id": c, "conglomerado": c.split("-")[0], "lo": 0.1, "hi": 0.6, "punto": 0.3} for c in celdas]
    return {"todas": [dict(f, r=float(rng.uniform(0, 1))) for f in base],
            "parcial": [dict(f, r=(None if i % 2 else 0.35)) for i, f in enumerate(base)],
            "cero": [dict(f, r=None) for f in base],
            "sin_ic": [dict(f, lo=None, hi=None, r=0.4) for f in base]}


@pytest.mark.parametrize("rel", MEDIDORES)
def test_valida_outputs_todas_las_ramas(rel):
    M = MODS[rel]
    esq = M.esquema_resultados()
    celdas = [r["id"][len(M.P) + 1:-2] for r in esq if r["id"].endswith("-R")]
    assert celdas
    for nombre, filas in _ramas(celdas).items():
        out = E.salida(M.P, filas)
        assert corrida0._valida_outputs({"resultados": esq}, out) == [], nombre
        for k, v in out.items():
            assert v is None or not isinstance(v, float) or math.isfinite(v), (nombre, k)
        if nombre in ("cero", "sin_ic"):
            assert out[f"{M.P}-DICTAMEN"] == "NO-ESTIMABLE"


@pytest.mark.parametrize("rel", MEDIDORES)
def test_medir_rechaza_input_ajeno(rel):
    M = MODS[rel]
    with pytest.raises(M.G.ParoDeGuardia):
        M.medir({"otro_payload": {"ruta_absoluta": "/nada"}}, {})


# ── vista y lista de leídos ─────────────────────────────────────────────────

VISTA = os.path.join(ROOT, "data", "corrida0", "aperturas-pendientes-v1_0.tsv")
INV = _load("forense/prereg-aperturas/inventario_aperturas.py", "ap_inventario_t")


def _vista():
    with open(VISTA, encoding="utf-8") as f:
        return list(csv.DictReader((x for x in f if not x.startswith("#")), delimiter="\t"))


def test_vista_casa_con_la_derivacion():
    assert INV.main(["--verifica"]) == 0


def test_vista_cubre_toda_reservada():
    reservados = set(INV.reservados_del_manifiesto())
    en_vista = {i for fila in _vista() for i in fila["ids"].split(";") if i}
    assert reservados and reservados - en_vista == set()


def test_todo_contendiente_declarado_esta_en_la_vista():
    """Todo CALC sellado cuyo spec.yaml declara una ola RESERVADA (E.6) como no-input aparece como
    contendiente de una fila, o en YA_ADJUDICADOS con su cita."""
    declarados = set(INV.contendientes_declarados())
    en_vista = {c for fila in _vista() for c in fila["contendientes"].split(";") if c}
    assert declarados and sorted(declarados - en_vista - set(INV.YA_ADJUDICADOS)) == []


def test_expediente_completo_donde_hay_contendiente():
    for fila in _vista():
        if fila["contendientes"] and fila["contendientes"] != "NINGUNO":
            d = os.path.join(ROOT, fila["expediente"])
            b = os.path.basename(d)
            for nombre in (f"APERTURA-{b}-spec-v1_0.md", f"APERTURA-{b}-spec.yaml", f"RECETA-APERTURA-{b}.md"):
                assert os.path.exists(os.path.join(d, nombre)), (fila["programa"], nombre)
            assert glob.glob(os.path.join(d, "medidor_apertura_*.py")), fila["programa"]


def test_ningun_payload_reservado_leido():
    reservados = set(INV.reservados_del_manifiesto())
    archivos = set(INV.archivos_reservados_del_manifiesto())
    leidos = [ln.strip() for ln in open(os.path.join(AP, "archivos-leidos-v1_0.txt"), encoding="utf-8")
              if ln.strip() and not ln.startswith("#")]
    assert leidos and not (set(leidos) & (reservados | archivos))
