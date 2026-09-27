"""Reconciliación por llave; evita sumar ejes como filas independientes (#1184)."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SRC = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1'

def read(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))

def write(path, rows, fields):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)

def assemble():
    base = read(SRC / 'tabla-estimadores.tsv')
    spec = {r['llave']: r for r in read(SRC / 'hallazgos-spec.tsv')}
    public = {r['llave']: r for r in read(SRC / 'dictamenes-publicabilidad.tsv')}
    adjudications = {}
    for axis, relative in [('IC', 'p1/evidencia-ic.tsv'), ('publicabilidad', 'p2/dictamenes.tsv'), ('spec', 'p3/identidades-799.tsv')]:
        evidence = read(OUT / relative)
        assert len(evidence) == len({r['llave'] for r in evidence}), relative
        adjudications[axis] = {r['llave']: r for r in evidence}
    assert len({r['llave'] for r in base}) == len(base)
    rows = []
    for r in base:
        key = r['llave']
        only_ic = r['estado_punto'] == 'COINCIDE' and r['estado_ic'] == 'DISCREPA'
        axes = [n for n, yes in [('IC', only_ic), ('publicabilidad', key in public), ('spec', key in spec)] if yes]
        rows.append(dict(llave=key, paquete=r['paquete'], calc=r['calc'], result_id=r['result_id'],
                         celda=r['celda'], eje=r['eje'], segmento=r['segmento'],
                         punto_historico=r['estado_punto'], ic_historico=r['estado_ic'],
                         estado_comparador=r['estado_comparador'], estado_lote=r['estado'],
                         solo_ic=str(only_ic).lower(), publicabilidad=public.get(key, {}).get('estado_dictamen', 'SIN-DICTAMEN-DE-SUPRESION'),
                         spec=spec.get(key, {}).get('estado', 'SIN-HALLAZGO-D15-EN-LOTE'),
                         ejes_encargo='|'.join(axes), evidencia_historica=str(SRC.relative_to(ROOT)),
                         motivo_spec=spec.get(key, {}).get('motivo', '')))
        for axis in ['IC', 'publicabilidad', 'spec']:
            evidence = adjudications[axis].get(key, {})
            rows[-1]['dictamen_' + axis] = evidence.get('dictamen_ic', evidence.get('dictamen', 'NO-APLICA-ENCARGO'))
        rows[-1]['dependencia_publicabilidad'] = adjudications['publicabilidad'].get(key, {}).get('condicion', '')
        rows[-1]['clase_sucesor_spec'] = adjudications['spec'].get(key, {}).get('clase_sucesor', '')
        rows[-1]['fuente_humana_spec'] = adjudications['spec'].get(key, {}).get('fuente_fechada', '')
        rows[-1]['evidencia_adjudicacion'] = '|'.join({'IC':'p1/evidencia-ic.tsv', 'publicabilidad':'p2/dictamenes.tsv', 'spec':'p3/identidades-799.tsv'}[axis] for axis in axes)
    fields = list(rows[0])
    write(OUT / 'tabla-unica.tsv', rows, fields)
    target = [r for r in rows if r['ejes_encargo']]
    patterns = Counter(r['ejes_encargo'] for r in target)
    summary = dict(denominador_lote=len(rows), cobertura_union=len(target),
                   ejes=dict(IC=sum(r['solo_ic']=='true' for r in rows), publicabilidad=len(public), spec=len(spec)),
                   intersecciones_exclusivas=dict(patterns), fuera_del_encargo=len(rows)-len(target),
                   primer_intento_preservado=True, validacion_ciega=False,
                   fuentes_sha256={f:hashlib.sha256((SRC/f).read_bytes()).hexdigest() for f in ['tabla-estimadores.tsv','hallazgos-spec.tsv','dictamenes-publicabilidad.tsv']})
    intersections = [dict(llave=r['llave'], ejes=r['ejes_encargo']) for r in target if '|' in r['ejes_encargo']]
    write(OUT/'intersecciones.tsv', intersections, ['llave','ejes'])
    assert summary['ejes'] == {'IC':1873, 'publicabilidad':11, 'spec':799}, summary
    for axis in adjudications:
        assert set(adjudications[axis]) == {r['llave'] for r in rows if axis in r['ejes_encargo'].split('|')}, axis
    assert len(target) == sum(patterns.values())
    for key in spec.keys() | public.keys():
        assert key in {r['llave'] for r in rows}
    (OUT/'cobertura.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False))

if __name__ == '__main__':
    assemble()
