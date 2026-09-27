#!/usr/bin/env python3
"""Deriva la tabla sucesora por identidad; nunca modifica el universo original."""
from collections import Counter
import csv
import io
import json
from pathlib import Path
import tarfile

from verifica_lote import verificar

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1'
CATALOGO = ROOT / 'forense/validacion-independiente/catalogo-1'


def resume():
    verification = verificar()
    judgments = {}
    sidecar = BASE / 'dictamenes-publicabilidad.tsv'
    if sidecar.exists():
        with sidecar.open() as stream:
            judgments = {row['llave']: row for row in csv.DictReader(stream, delimiter='\t')}
    lots = {x['paquete']: x for x in json.loads((CATALOGO / 'lotes.json').read_text())}
    rows = []
    package_rows = []
    for entry in json.loads((BASE / 'entregas.json').read_text()):
        package = entry['paquete']
        lot = lots[package]
        with tarfile.open(CATALOGO / 'paquetes' / package / lot['archivo'], 'r:gz') as tar:
            identities = list(csv.DictReader(io.StringIO(tar.extractfile('estimandos.tsv').read().decode()), delimiter='\t'))
        own, compared = {}, {}
        if entry.get('comparacion'):
            compared = {x['llave']: x for x in json.loads((BASE / entry['comparacion']).read_text())['resultados']}
            with (BASE / entry['reconstruccion']).open() as stream:
                own = {x['llave']: x for x in csv.DictReader(stream, delimiter='\t')}
        states = Counter()
        for identity in identities:
            key = identity['llave']
            result = compared.get(key, {'estado': entry['estado'], 'efecto': 'NO-DETERMINADO'})
            judgment = judgments.get(key)
            state = judgment['estado_dictamen'] if judgment else result['estado']
            states[state] += 1
            fields = result.get('campos', {})
            point = ('COINCIDE' if fields['punto']['dentro'] else 'DISCREPA') if 'punto' in fields else 'NO-EVALUADO'
            intervals = [v['dentro'] for k, v in fields.items() if k.startswith('ic95_')]
            ic = ('COINCIDE' if all(intervals) else 'DISCREPA') if intervals else 'NO-EVALUADO'
            rows.append(dict(llave=key, paquete=package, calc=identity['calc'], result_id=identity['result_id'],
                             celda=identity['celda'], instrumento=identity['instrumento'], ola=identity['ola'],
                             eje=identity['eje'], segmento=identity['segmento'], estado=state,
                             estado_comparador=result['estado'], estado_punto=point, estado_ic=ic,
                             efecto=judgment['efecto'] if judgment else result['efecto'],
                             motivo=own.get(key, {}).get('motivo') or own.get(key, {}).get('explicacion') or entry.get('motivo', ''),
                             commit_reconstruccion=entry.get('commit_reconstruccion', ''),
                             reconstruccion_sha256=entry.get('reconstruccion_sha256', '')))
        package_rows.append({'paquete': package, 'estimadores': len(identities), 'estados': dict(states)})
    with (BASE / 'tabla-estimadores.tsv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter='\t')
        writer.writeheader()
        writer.writerows(rows)
    numerical = sum(row['estado_punto'] in {'COINCIDE', 'DISCREPA'} for row in rows)
    final_states = dict(Counter(row['estado'] for row in rows))
    if 'estados_dictamen' in verification:
        assert final_states == verification['estados_dictamen']
    summary = dict(verification, paquetes=package_rows, recalculados_por_llave=numerical,
                   estados_dictamen=final_states,
                   punto_coincide=sum(row['estado_punto'] == 'COINCIDE' for row in rows),
                   punto_discrepa=sum(row['estado_punto'] == 'DISCREPA' for row in rows),
                   solo_discrepa_ic=sum(row['estado_punto'] == 'COINCIDE' and row['estado_ic'] == 'DISCREPA' for row in rows),
                   cobertura_numerica_lote=numerical / verification['denominador_lote'],
                   cobertura_numerica_universo=numerical / verification['denominador_universo'])
    (BASE / 'resumen-lote1.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in {'causas', 'paquetes'}}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    resume()
