#!/usr/bin/env python3
"""Verifica congelaciones y pruebas portables del lote2 sin leer raw."""
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote2'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verificar():
    freeze=json.loads((BASE/'p1/congelacion-adaptador-v1.json').read_text())
    assert sha(ROOT/'tools/validacion/astra6_lote2/adaptador_comparador_v1.py') == freeze['adaptador_sha256']
    assert sha(BASE/'p1/contrato-adaptador-v1.json') == freeze['contrato_sha256']
    contract=json.loads((BASE/'p1/contrato-adaptador-v1.json').read_text())
    keys=[m['llave_sucesor'] for e in contract['entradas'] for m in e['correspondencia']]
    assert len(keys)==len(set(keys))==425
    spec=importlib.util.spec_from_file_location('proof',ROOT/'tools/validacion/astra6_lote1/prueba_commit.py')
    proof=importlib.util.module_from_spec(spec); spec.loader.exec_module(proof)
    entries=json.loads((BASE/'p3/lote2-entregas.json').read_text())
    assert len({e['paquete'] for e in entries})==len(entries)
    for e in entries:
        assert e['separacion_efectiva'] and e['session_id']
        assert e['entrada_registrada_utc'] < e['congelacion_recibida_utc'] <= e['revelacion_utc']
        archive=BASE/'p3'/e['reconstruccion']; assert sha(archive)==e['reconstruccion_sha256']
        files=proof.verificar(json.loads((BASE/'p3'/e['prueba_commit']).read_text()))
        assert hashlib.sha256(files[e['ruta_reconstruccion_commit']]).hexdigest()==e['reconstruccion_sha256']
        if e.get('comparacion'):
            assert sha(BASE/'p3'/e['comparacion'])==e['comparacion_sha256']
    result={'entradas_recibidas':len(entries),'identidades_contrato':len(keys),'congelaciones_portables_verificadas':len(entries),'adaptador_intacto':True}
    print(json.dumps(result,ensure_ascii=False)); return result
if __name__=='__main__': verificar()
