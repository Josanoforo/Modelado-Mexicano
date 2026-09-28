#!/usr/bin/env python3
"""Gate dirigido: cobertura, trazabilidad, fuentes, reserva y tabla/prosa."""
import csv
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
MAP=ROOT/'canon/mapa-dominios-v1_1.tsv'
REPORT=ROOT/'corpus/reports-v2/Autoridad_y_jerarquía_en_el_México_contemporáneo__anatomía_psicológica_de_un_sistema_dual.md'
ORIGINAL='corpus/reports/Autoridad_y_jerarquía_en_el_México_contemporáneo__anatomía_psicológica_de_un_sistema_dual.md'
with MAP.open(newline='') as f:
    ids={r['id_afirmacion'] for r in csv.DictReader(f,delimiter='\t') if r['report']==ORIGINAL}
with (HERE/'afirmaciones.tsv').open(newline='') as f:
    table=list(csv.DictReader(f,delimiter='\t'))
assert len(table)==len({r['id'] for r in table}), 'ID duplicado'
assert {r['id'] for r in table if r['id'].startswith('ASTRA5-')}==ids, 'Mapa incompleto'
assert all(r['dictamen'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'} and r['razon'] and r['evidencia'] for r in table), 'Decisión sin razón/fuente'
summary=json.loads((HERE/'resumen.json').read_text())
assert summary['registros']==len(table) and summary['mapa_filas']==len(ids)
assert summary['dictamenes']=={k:sum(r['dictamen']==k for r in table) for k in ('CONFIRMA','MATIZA','ROMPE','SIN-CIFRA')}
assert [r['id'] for r in table if r['dictamen']=='ROMPE']==['ASTRA5-U0-AUTOR-013']
assert next(r['dictamen'] for r in table if r['id']=='ASTRA5-U0-AUTOR-023')=='CONFIRMA'
prose=REPORT.read_text()
assert all(f'[{x}]' in prose for x in ('INEGI-ENCUCI','OCDE24','OCDE25','GLOBE04','HOF','WVS-Q'))
assert 'FP-293' in prose and 'no es nueva observación mexicana' in prose
assert 'RESULT-*' not in prose
assert '**27%**' in prose and 'figura 4' in prose and 'figura 5' in prose
assert '2026 Results: Mexico' not in prose
assert all(word in prose for word in ('Resumen ejecutivo','Evidencia por tier','Comparación internacional','Auditoría final','SI**'))
print(f'VERDE: mapa {len(ids)}/{len(ids)}, tabla {len(table)}, fuentes 6, reserva respetada, prosa y tabla presentes')
