"""Protege la contaminación observada: specs con esperado y archivos productores.

No simula reconstrucciones COINCIDE ni valida ningún estimador del catálogo.
"""
import importlib.util
from pathlib import Path

import pytest


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).parents[1] / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P = module('astra6_paquetes', 'tools/validacion/astra6_paquetes.py')
C = module('astra6_compara', 'tools/validacion/astra6_catalogo/astra6_compara_catalogo.py')


@pytest.mark.parametrize('name,content', [
    ('metodo.md', 'p=0.642080'),
    ('metodo.md', 'Abrir resultados.json del productor'),
    ('medidor.py', 'pass'),
])
def test_rechaza_resultados_y_productores(tmp_path, name, content):
    file = tmp_path / name
    file.write_text(content)
    (tmp_path / 'manifiesto.json').write_text('{}')
    with pytest.raises(AssertionError):
        P.verify_files(tmp_path, {'archivos': {name: P.sha(file)}})


def test_rechaza_archivo_fuera_de_allowlist(tmp_path):
    (tmp_path / 'manifiesto.json').write_text('{}')
    (tmp_path / 'otro.md').write_text('Cifra ajena')
    with pytest.raises(AssertionError):
        P.verify_files(tmp_path, {'archivos': {}})


def test_rechaza_cambio_posterior_al_hash(tmp_path):
    file = tmp_path / 'metodo.md'
    file.write_text('Método recibido')
    digest = P.sha(file)
    (tmp_path / 'manifiesto.json').write_text('{}')
    file.write_text('Método alterado')
    with pytest.raises(AssertionError):
        P.verify_files(tmp_path, {'archivos': {'metodo.md': digest}})


def test_comparador_no_revela_esperado_sin_hash_congelado(tmp_path, monkeypatch):
    file = tmp_path / 'reconstruccion.tsv'
    file.write_text('sin reconstrucción real')
    monkeypatch.setattr(C, 'BASE', tmp_path / 'esperado-no-entregado')
    with pytest.raises(AssertionError):
        C.compare(file, tmp_path / 'recibo-inexistente.json', '0' * 64, tmp_path / 'salida.json')
    assert not (tmp_path / 'salida.json').exists()
