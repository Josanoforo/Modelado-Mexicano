#!/usr/bin/env python3
"""Genera cobertura y citas de cifras desde decisiones editoriales explícitas y tabla sellada."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
rows = json.loads((HERE / 'decisiones-editoriales.json').read_text())['filas']
map_path = ROOT / 'canon/mapa-dominios-v1_1.tsv'
with map_path.open() as f:
    canonical = {r['id_afirmacion']: r for r in csv.DictReader(f, delimiter='\t')}
local_path = ROOT / 'forense/analisis/dominios/lotes/salud-cuerpo-filas-v1_0.tsv'
with local_path.open() as f:
    local = list(csv.DictReader(f, delimiter='\t'))
assert len(local) == 39
assert all(row['id_afirmacion'] in canonical for row in local)
assert [r[0] for r in rows[:39]] == [f'{n:03}' for n in range(1, 40)]
claim_rows = []
for key, verdict, reason, evidence in rows:
    if key.isdigit():
        source = local[int(key) - 1]
        assert source['fila_local'] == 'salud-cuerpo-' + key
        claim_id = source['id_afirmacion']
        assert canonical[claim_id]['texto_vigente'] == source['texto_vigente']
    else:
        claim_id = 'C3-SALUD-' + key
    claim_rows.append((claim_id, key, verdict, reason, evidence))
source = ROOT / 'forense/analisis/salud-bienestar/tabla-pisos-v1_0.tsv'
with source.open() as f:
    table = list(csv.DictReader(f, delimiter='\t'))

selection = {
    'S-C01': ('ATENCION-CONSULTORIO-FARMACIA', '2022', 'TOTAL', 'TODOS'),
    'S-C02': ('ATENCION-CONSULTORIO-FARMACIA', '2024', 'TOTAL', 'TODOS'),
    'S-C03': ('NECESIDAD-SALUD-3M', '2024', 'SEXO', 'HOMBRE'),
    'S-C04': ('NECESIDAD-SALUD-3M', '2024', 'SEXO', 'MUJER'),
    'S-C05': ('BUSCO-ATENCION', '2024', 'SEXO', 'HOMBRE'),
    'S-C06': ('BUSCO-ATENCION', '2024', 'SEXO', 'MUJER'),
    'S-C07': ('ALCOHOL-12M', '2016', 'SEXO', 'MUJER'),
    'S-C08': ('ATENCION-CURANDERO-HIERBERO', '2024', 'TOTAL', 'TODOS'),
    'S-C09': ('DROGA-ILEGAL-ALGUNA-VEZ', '2016', 'TOTAL', 'TODOS'),
}
cifras = {}
for key, query in selection.items():
    matches = [(i + 2, row) for i, row in enumerate(table)
               if tuple(row[k] for k in ('conducta', 'ola', 'eje', 'categoria')) == query]
    assert len(matches) == 1, (key, len(matches))
    line, row = matches[0]
    path = ROOT / 'data/corrida0' / row['calc'] / 'resultados.json'
    cifras[key] = dict(row, tabla_fila_fisica=line,
                      resultados_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                      resultados_ruta=str(path.relative_to(ROOT)),
                      adopcion=('FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01'
                                if 'ENSANUT' in row['calc'] else
                                'FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-02'))

with (HERE / 'afirmaciones.tsv').open('w') as f:
    writer = csv.writer(f, delimiter='\t', lineterminator='\n')
    writer.writerow(('id_afirmacion', 'clave_editorial', 'dictamen', 'razon', 'evidencia_o_localizador'))
    writer.writerows(claim_rows)
(HERE / 'cifras.json').write_text(json.dumps(cifras, ensure_ascii=False, indent=2) + '\n')
(HERE / 'cobertura.json').write_text(json.dumps({
    'total': len(rows), 'mapa': sum(r[0].isdigit() for r in rows),
    'adicionales': sum(not r[0].isdigit() for r in rows),
    'dictamenes': Counter(r[1] for r in rows),
    'base_original': 'corpus/reports/Health__Body__Food_and_Substance_Use_in_Mexico__The_Behavioral_Layer_of_Decisions__Environment_and_Structure.md',
    'fuente_mapa': 'forense/analisis/dominios/lotes/salud-cuerpo-filas-v1_0.tsv'
}, ensure_ascii=False, indent=2) + '\n')
