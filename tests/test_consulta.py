"""Tests de `tools/consulta.py` (ACTO GEN2-TUBERIA-RENDIMIENTO-1 · P2) y de la
equivalencia de loaders YAML que sostiene P3.

Defecto que atrapan: (1) un subcomando de consulta que imprime mas de una
linea, o que da un negativo sin declarar cuantas filas examino (A.13);
(2) que libyaml (`CSafeLoader`) y el loader Python (`SafeLoader`) lean
distinto un archivo que los derivadores de vistas parsean -- si divergieran,
la migracion de P3 cambiaria una vista publicada.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
import consulta  # noqa: E402


@pytest.fixture
def repo_falso(tmp_path, monkeypatch):
    tsv = tmp_path / "resultados.tsv"
    tsv.write_text("# DERIVADO\nresultado_id\tvalor\tunidad\tcuenta_gen2\n"
                   "RES-A\t0.5\tproporcion\tSI\nRES-B\t\"1\t2\"\tpp\tNO\n",
                   encoding="utf-8")
    monkeypatch.setattr(consulta, "RESULTADOS", tsv)
    monkeypatch.setattr(consulta, "RAIZ", tmp_path)
    celdas = tmp_path / "celdas"
    celdas.mkdir()
    (celdas / "X.a.b.yaml").write_text(
        "celda_d:\n  id: X.a.b\n  veredicto: CORROBORADA\n  champion_actual: C2\n"
        "  candidatos: [{id: C1}, {id: C2}]\n", encoding="utf-8")
    monkeypatch.setattr(consulta, "CELDAS_D", celdas)
    man = tmp_path / "manifiesto.yaml"
    man.write_text("- id: p1\n  sha256: abc\n  archivo: p1.zip\n", encoding="utf-8")
    monkeypatch.setattr(consulta, "MANIFIESTO", man)
    return tmp_path


def _una_linea(capsys) -> str:
    out = capsys.readouterr().out
    assert out.count("\n") == 1, out
    return out


def test_result_una_linea(repo_falso, capsys):
    assert consulta.main(["result", "RES-A"]) == 0
    out = _una_linea(capsys)
    assert out.startswith("RES-A · valor=0.5 · unidad=proporcion")
    assert "cuenta_gen2=SI" in out


def test_result_campo_citado_con_tab(repo_falso, capsys):
    # lector CSV, no split por linea fisica (§2)
    assert consulta.main(["result", "RES-B"]) == 0
    assert "valor=1 2" in _una_linea(capsys)


def test_negativo_declara_filas_examinadas(repo_falso, capsys):
    assert consulta.main(["result", "RES-Z"]) == 1
    out = _una_linea(capsys)
    assert "NO-ENCONTRADO" in out and "filas examinadas=2" in out


def test_celda_desde_yaml(repo_falso, capsys):
    assert consulta.main(["celda", "X.a.b"]) == 0
    out = _una_linea(capsys)
    assert "champion_actual=C2" in out and "n_candidatos=2" in out


def test_payload(repo_falso, capsys):
    assert consulta.main(["payload", "p1"]) == 0
    assert "sha256=abc" in _una_linea(capsys)
    assert consulta.main(["payload", "p9"]) == 1
    assert "filas examinadas=1" in _una_linea(capsys)


@pytest.mark.parametrize("tipo,ruta", [("fp", consulta.FIRMAS),
                                       ("nc", consulta.NO_CORRIDO),
                                       ("corrida", consulta.CORRIDAS)])
def test_tsv_reales_una_linea(tipo, ruta, capsys):
    col, _ = consulta.CAMPOS[tipo]
    fila, _n = consulta.busca_tsv(ruta, col, "__nunca__")
    assert fila is None
    import csv
    with ruta.open(encoding="utf-8", newline="") as fh:
        primera = next(csv.DictReader((l for l in fh if not l.startswith("#")),
                                      delimiter="\t"))
    assert consulta.main([tipo, primera[col]]) == 0
    _una_linea(capsys)


@pytest.mark.skipif(not hasattr(yaml, "CSafeLoader"), reason="sin libyaml")
@pytest.mark.parametrize("rel", ["milpa/tramite-ola5-propuesta-v0.yaml",
                                 "data/manifiesto.yaml"])
def test_libyaml_equivale_a_loader_python(rel):
    texto = (RAIZ / rel).read_text(encoding="utf-8")
    assert yaml.load(texto, Loader=yaml.CSafeLoader) == yaml.load(texto, Loader=yaml.SafeLoader)
