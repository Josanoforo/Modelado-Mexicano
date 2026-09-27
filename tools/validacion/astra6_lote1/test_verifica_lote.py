"""Gates dirigidos: una comparación no elude congelación ni duplicados."""
import importlib.util
from pathlib import Path
import unittest
import tempfile
import json
from collections import Counter

spec = importlib.util.spec_from_file_location('verifica_lote', Path(__file__).with_name('verifica_lote.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Gates(unittest.TestCase):
    def test_comparacion_sin_congelacion_rechazada(self):
        with self.assertRaisesRegex(ValueError, 'Falta fecha'):
            module.comparacion({'entrada_registrada_utc': '2026-09-26T18:00:00Z'}, Path('/tmp'), {'a'})

    def test_publicabilidad_no_promueve_coincidencia(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / 'reconstruccion.tsv').write_text('llave\testado\tmotivo\tpunto\tic95_inf\tic95_sup\na\tNO-RECALCULABLE-DESDE-SPEC\tSUPRIMIDO-POR-SPEC: CV\t\t\t\n')
            (base / 'comparacion.json').write_text(json.dumps({'resultados': [{'llave': 'a', 'estado': 'NO-RECALCULABLE-DESDE-SPEC'}]}))
            (base / 'dictamenes-publicabilidad.tsv').write_text('llave\tpaquete\testado_comparador\testado_dictamen\tefecto\tmotivo\tevidencia\na\tp\tNO-RECALCULABLE-DESDE-SPEC\tCOINCIDE\talcance: publicabilidad\tsupresión\treconstruccion.tsv\n')
            entry = {'paquete': 'p', 'reconstruccion': 'reconstruccion.tsv', 'comparacion': 'comparacion.json'}
            with self.assertRaisesRegex(ValueError, 'solo discrepancia'):
                module.publicabilidad(base, [entry], Counter({'NO-RECALCULABLE-DESDE-SPEC': 1}))

    def test_blob_adulterado_rechazado(self):
        proof_module = module._prueba
        blob = b'llave\testado\na\tRECONSTRUIDO\n'
        blob_oid = proof_module.oid('blob', blob)
        tree = b'100644 reconstruccion.tsv\0' + bytes.fromhex(blob_oid)
        tree_oid = proof_module.oid('tree', tree)
        commit = ('tree ' + tree_oid + '\n\ncongelado\n').encode()
        proof = {'commit_oid': proof_module.oid('commit', commit),
                 'commit_content_base64': proof_module.encode(commit),
                 'archivos': [{'ruta': 'reconstruccion.tsv',
                    'trees': [{'oid': tree_oid, 'content_base64': proof_module.encode(tree)}],
                    'blob_oid': blob_oid, 'blob_content_base64': proof_module.encode(blob)}]}
        self.assertEqual(proof_module.verificar(proof)['reconstruccion.tsv'], blob)
        proof['archivos'][0]['blob_content_base64'] = proof_module.encode(blob + b'adulterado')
        with self.assertRaisesRegex(ValueError, 'Blob adulterado'):
            proof_module.verificar(proof)

    def test_llaves_duplicadas_rechazadas(self):
        with self.assertRaisesRegex(ValueError, 'duplicadas'):
            module.llaves([{'llave': 'a'}, {'llave': 'a'}])


if __name__ == '__main__':
    unittest.main()
