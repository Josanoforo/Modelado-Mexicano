"""Fallos materiales del transporte; pruebas sinteticas sin recalculo."""
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'herramientas/transporte_v1.py'
spec = importlib.util.spec_from_file_location('transporte', TOOL)
t = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = t
spec.loader.exec_module(t)


class Transporte(unittest.TestCase):
    def setUp(self):
        self.row = dict(zip(t.COLUMNAS, ['R#0', 'C', 'R', '0', 'ENDIREH', '2021',
                                        'comunitaria', 'nacional', 'MX', 'proporcion', 'IC95-DE-DISENO']))
        self.b = ('\t'.join(t.COLUMNAS) + '\r\n' + '\t'.join(self.row.values()) + '\r\n').encode()
        self.method = b'periodo octubre de 2020; edad 15-120; bootstrap 200'
        self.old = {'estimandos.tsv': self.b, 'metodo.md': self.method, 'tolerancia.json': b'{"abs":1e-10}'}

    def test_preserva_bytes_previos_e_identidad(self):
        out = t.transportar(self.b, {'R#0': 'desde_octubre_2020'}, self.method)
        rebuilt = b''.join(x.rsplit(b'\t', 1)[0] + b'\r\n' for x in out.splitlines())
        self.assertEqual(rebuilt, self.b)
        t.comprobar(self.old, {**self.old, 'estimandos.tsv': out})

    def test_ventana_ausente(self):
        with self.assertRaises(ValueError):
            t.transportar(self.b, {'R#0': ''}, self.method)

    def test_llave_duplicada(self):
        with self.assertRaises(ValueError):
            t.filas(self.b + self.b.splitlines(keepends=True)[1])

    def test_mapa_ventana_duplicada(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'mapa.tsv'
            path.write_text('llave\tpaquete\tventana\testado\n' +
                            'R#0\tP\tvida\tDEMOSTRADA-PUBLICADA\n' * 2)
            with self.assertRaises(ValueError):
                t.leer_mapa(path)

    def test_llave_inexistente(self):
        with self.assertRaises(ValueError):
            t.transportar(self.b, {'R#1': 'vida'}, self.method)

    def test_contradiccion_temporal(self):
        with self.assertRaises(ValueError):
            t.transportar(self.b, {'R#0': 'desde_octubre_2015'}, self.method)

    def test_metodo_modificado(self):
        out = t.transportar(self.b, {'R#0': 'vida'}, self.method)
        with self.assertRaises(ValueError):
            t.comprobar(self.old, {**self.old, 'metodo.md': b'edad 15-97', 'estimandos.tsv': out})

    def test_resultado_ic_codigo_infiltrado(self):
        for field in ['punto', 'ic95_inf', 'ic95_sup', 'codigo_productor']:
            bad = self.b.replace(b'naturaleza_ic\r\n', ('naturaleza_ic\t' + field + '\r\n').encode())
            with self.assertRaises(ValueError):
                t.filas(bad)

    def test_fuente_identidad_desajustada(self):
        out = t.transportar(self.b, {'R#0': 'vida'}, self.method).replace(b'nacional', b'entidad')
        with self.assertRaises(ValueError):
            t.comprobar(self.old, {**self.old, 'estimandos.tsv': out})

    def test_hash_cambiado(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'x.tar.gz'
            hashes = {k: t.sha(v) for k, v in self.old.items()}
            hashes['metodo.md'] = '0'*64
            data = {**self.old, 'manifiesto.json': t.json_bytes({'archivos': hashes})}
            t.escribir_tar(path, data)
            with self.assertRaisesRegex(ValueError, 'hash cambiado'):
                t.leer_tar(path)


if __name__ == '__main__':
    unittest.main()
