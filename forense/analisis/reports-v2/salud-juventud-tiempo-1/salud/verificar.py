#!/usr/bin/env python3
"""Control dirigido de cobertura y correspondencia de marcadores de salud."""
import csv
import json
import re
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[4]
report = (root / 'corpus/reports-v2/Health__Body__Food_and_Substance_Use_in_Mexico__The_Behavioral_Layer_of_Decisions__Environment_and_Structure.md').read_text()
with (here / 'afirmaciones.tsv').open() as f:
    claims = list(csv.DictReader(f, delimiter='\t'))
with (root / 'canon/mapa-dominios-v1_1.tsv').open() as f:
    canonical = {r['id_afirmacion']: r for r in csv.DictReader(f, delimiter='\t')}
with (root / 'forense/analisis/dominios/lotes/salud-cuerpo-filas-v1_0.tsv').open() as f:
    local = list(csv.DictReader(f, delimiter='\t'))
cifras = json.loads((here / 'cifras.json').read_text())
assert [x['id_afirmacion'] for x in claims[:39]] == [x['id_afirmacion'] for x in local]
assert [x['clave_editorial'] for x in claims[:39]] == [f'{n:03}' for n in range(1, 40)]
assert all(x['id_afirmacion'] in canonical and
           canonical[x['id_afirmacion']]['texto_vigente'] == local[i]['texto_vigente']
           for i, x in enumerate(claims[:39]))
assert all(x['id_afirmacion'].startswith('C3-SALUD-EX') for x in claims[39:])
assert len({x['id_afirmacion'] for x in claims}) == len(claims)
assert {x['dictamen'] for x in claims} <= {'CONFIRMA', 'MATIZA', 'ROMPE', 'SIN-CIFRA'}
for marker in set(re.findall(r'S-C\d{2}', report)):
    assert marker in cifras, marker
for marker, citation in cifras.items():
    assert citation['result_id_p'].startswith('RESULT-'), marker
    assert citation['resultados_sha256'] and citation['tabla_fila_fisica'] > 1, marker
    assert citation['eje'] and citation['categoria'] and citation['n'], marker
    assert citation['adopcion'].startswith('FP-'), marker
    assert marker in report or marker == 'S-C08' or marker == 'S-C09', marker
assert all(x['razon'] and x['evidencia_o_localizador'] for x in claims)
print(f'OK: {len(claims)} afirmaciones, {len(cifras)} cifras trazadas; dictámenes sometidos a revisión editorial')
