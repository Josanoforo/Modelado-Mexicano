"""Verifica objetos propuestos cerrados; no abre microdato ni escribe al verificar."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INVENTARIO = ROOT / 'frontera-inventario.json'


def archivos():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts
                  and p != INVENTARIO and p.suffix != '.pyc'
                  and not p.name.startswith('frontera-gate-'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--crea-inventario', action='store_true')
    args = parser.parse_args()
    actuales = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in archivos()}
    if args.crea_inventario:
        INVENTARIO.write_text(json.dumps({'estado': 'PROPUESTO-POR-EJECUTOR',
                                         'sha256': actuales}, indent=2,
                                        ensure_ascii=False) + '\n')
        print(json.dumps({'inventario_creado': len(actuales)}))
        return
    esperado = json.loads(INVENTARIO.read_text())['sha256']
    fallos = [name for name in sorted(set(actuales) | set(esperado))
              if actuales.get(name) != esperado.get(name)]
    assert not fallos, f'IDENTIDAD: {fallos}'
    for nombre in ('ENSU-CAMPECHE-INSEGURIDAD', 'ENOE-INFORMALIDAD'):
        base = ROOT / 'paquetes' / nombre
        prefijo = 'enoe' if nombre.startswith('ENOE-') else 'ensu'
        assert (base / (prefijo + '-spec.yaml')).is_file() and (base / (prefijo + '-spec-humana.md')).is_file()
        prefijo += '-'
        evidencia = json.loads((base / (prefijo + 'sintetico-auditoria.json')).read_text())
        assert evidencia['estado'] == 'VERDE', nombre
        oro = json.loads((base / (prefijo + 'oro.json')).read_text())
        assert oro['estado'] == 'DIAGNOSTICO-HISTORICO-ABIERTO', nombre
        for grupo in oro['grupos'].values():
            assert 0 <= grupo['p0'] <= 1
            assert grupo['denominador_ponderado'] > 0
    print(json.dumps({'estado': 'VERDE', 'archivos': len(actuales),
                      'paquetes_diagnosticos': 2,
                      'adopciones': 0, 'aperturas_futuras': 0}))


if __name__ == '__main__':
    main()
