"""Verificador de entrega: hashes, guardias, oro y emisiones por separado."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import yaml

from audita import auditar
from ejecuta import ANALISIS, CALCS, ROOT, SPEC, reproduce, verificar_congelado
from medidor import FAMILIAS, leer, medir, sha
from potencia import ejecutar as potencia


def verifica():
    verificar_congelado()
    for rel, expected in json.loads((ANALISIS/'commit1-extension-hashes.json').read_text()).items():
        assert sha(ROOT/rel) == expected, rel
    spec = yaml.safe_load(SPEC.read_text())
    assert np.__version__ == spec['dependencias']['numpy']
    assert yaml.__version__ == spec['dependencias']['yaml']
    auditar((ROOT/'tools/familias-2027/envipe/medidor.py').read_text())
    subprocess.run([sys.executable, str(ROOT/'tools/familias-2027/envipe/prueba_prospectiva.py'), '-q'], check=True)
    inv = json.loads((ANALISIS/'inventario-atestacion.json').read_text())
    assert inv['familias'] == 2 and inv['olas_futuras'] == 1
    assert inv['estado'] == 'SELLADO-INTERNAMENTE' and inv['atestaciones_verificadas'] == 0
    for rel, expected in inv['sellos'].items():
        assert sha(ROOT/rel) == expected, rel
        seal = json.loads((ROOT/rel).read_text())
        for path, expected_file in seal['archivos'].items():
            assert sha(ROOT/path) == expected_file, path
        # El código de COMMIT-1 antecede por historial a la emisión sellada.
        emission = str(Path(rel).with_name('emision.json'))
        commits = subprocess.check_output(['git','log','--reverse','--format=%H','--',emission], cwd=ROOT, text=True).splitlines()
        if commits:
            subprocess.run(['git','merge-base','--is-ancestor',seal['commit1'],commits[0]], cwd=ROOT, check=True)
            subprocess.run(['git','merge-base','--is-ancestor',seal['commit1_complemento'],commits[0]], cwd=ROOT, check=True)
    reproduce()
    # Oro: lectura histórica autorizada; nada se reescribe ni se resella.
    diag, reps = medir(leer(ROOT/'data/raw/envipe2025_csv.zip', spec), spec)
    saved = json.loads((ANALISIS/'replicas.json').read_text())
    original = json.loads((ANALISIS/'diagnostico.json').read_text())
    for name in FAMILIAS:
        assert np.array_equal(reps[name], saved[name], equal_nan=True), name
        assert diag['familias'][name]['punto'] == original['familias'][name]['punto']
        diag['familias'][name]['soporte'] = dict(diag['familias'][name])
        calc, rid, _ = CALCS[name]
        expected = json.loads((ROOT/'data/corrida0'/calc/'resultados.json').read_text())['resultados'][rid]
        assert abs(diag['familias'][name]['punto'] - expected) <= 1e-6
    assert diag == original
    assert json.loads(json.dumps(potencia(reps, diag))) == json.loads((ANALISIS/'potencia.json').read_text())
    cal = json.loads((ANALISIS/'calendario.json').read_text())
    assert cal['numero_olas'] == 1 and cal['estado_fecha'] == 'NO-CONFIRMADA'
    assert cal['fecha_confirmada'] is None and cal['fuentes']
    print('ORO-HISTORICO: REPRODUCE puntos, soporte y 2000 réplicas comunes; NO acredita acierto futuro')
    print('CIERRE: PASS · 2 familias · 1 ola · 0 R futuras · 0 retadores · 0 atestaciones externas')
    print('DEPENDENCIAS: autorización/metadatos/adaptador COMMIT-3; OTS y recibo técnico de Claude')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--verifica', action='store_true', required=True)
    p.parse_args()
    verifica()
