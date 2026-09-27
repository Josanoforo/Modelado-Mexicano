#!/usr/bin/env python3
"""Reconciliación por identidad, sin extrapolar la selección al catálogo."""
from collections import Counter
import csv
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'forense/validacion-independiente/catalogo-1-ejecucion-lote2'
def load(p):
    with p.open(newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
def write(p,rs):
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]),delimiter='\t'); w.writeheader(); w.writerows(rs)
def resume():
    identities=load(BASE/'p4/identidades-base.tsv')
    received_path=BASE/'p3/lote2-entregas.json'
    entries=json.loads(received_path.read_text()) if received_path.exists() else []
    own={}; compared={}; receipts={}
    for e in entries:
        package=e['paquete']; receipts[package]=e
        for r in load(BASE/'p3'/e['reconstruccion']):
            assert r['llave'] not in own; own[r['llave']]=r
        if e.get('comparacion'):
            for r in json.loads((BASE/'p3'/e['comparacion']).read_text())['resultados']:
                assert r['llave'] not in compared; compared[r['llave']]=r
    impediments_path=BASE/'p3/impedimentos.json'
    impediments=json.loads(impediments_path.read_text()) if impediments_path.exists() else {}
    output=[]
    for identity in identities:
        key=identity['llave']; package=identity['sucesor']; e=receipts.get(package,{})
        impediment=impediments.get(package,{})
        technical=compared.get(key,{})
        path=BASE/'p3/dictamenes'/(package+'--dictamen.json')
        adjudication={r['llave']:r for r in json.loads(path.read_text())['resultados']} if path.exists() else {}
        result=adjudication.get(key,technical); row=own.get(key,{})
        fields=result.get('campos',{})
        point=('COINCIDE' if fields['punto']['dentro'] else 'DISCREPA') if 'punto' in fields else 'NO-EVALUADO'
        ic=[v['dentro'] for k,v in fields.items() if k.startswith('ic95_')]
        interval=('COINCIDE' if all(ic) else 'DISCREPA') if ic else 'NO-EVALUADO'
        state=result.get('estado') or impediment.get('estado') or 'NO-EVALUADO'
        # Empty numerical fields never establish reconstructed numerical coverage.
        publication=result.get('publicabilidad','PENDIENTE-DE-ADJUDICACION' if row else 'NO-EVALUADO')
        output.append(dict(identity,estado=state,estado_comparador=technical.get('estado',e.get('estado','NO-EVALUADO')),
            estado_punto=point,estado_ic=interval,estado_publicabilidad=publication,
            estado_spec=result.get('spec','INSUFICIENTE' if state=='NO-RECALCULABLE-DESDE-SPEC' else 'NO-DICTAMINADA'),
            motivo=row.get('motivo') or row.get('explicacion') or impediment.get('motivo',''),
            separacion_efectiva=bool(e.get('separacion_efectiva')),commit_reconstruccion=e.get('commit_reconstruccion',''),
            reconstruccion_sha256=e.get('reconstruccion_sha256',''),notas_dictamen='; '.join(result.get('notas',[]))))
    assert len(output)==len({r['llave'] for r in output})==425
    assert set(own)<= {r['llave'] for r in output}
    write(BASE/'lote2-tabla-estimadores.tsv',output)
    numerical=sum(r['estado_punto'] in {'COINCIDE','DISCREPA'} for r in output)
    denominators=json.loads((BASE/'p4/cobertura-base.json').read_text())
    summary={'identidades':len(output),'entradas_recibidas':len(entries),'estados':dict(Counter(r['estado'] for r in output)),
        'punto':dict(Counter(r['estado_punto'] for r in output)), 'ic':dict(Counter(r['estado_ic'] for r in output)),
        'publicabilidad':dict(Counter(r['estado_publicabilidad'] for r in output)),
        'spec':dict(Counter(r['estado_spec'] for r in output)),
        'cobertura_numerica_ciega':numerical,'denominador_lote':len(output),
        'denominador_historico':denominators['historico_denominador'], 'denominador_overlay':denominators['overlay_denominador'], 'cobertura_lote':numerical/len(output), 'cobertura_historico':numerical/denominators['historico_denominador'], 'cobertura_overlay':numerical/denominators['overlay_denominador'], 'denominadores_fuente':denominators,'C1_cerrado':False,
        'alcance':'Selección por preparación, sin inferencia de tasa representativa global; dependencia por instrumento/ola.'}
    (BASE/'resumen-lote2.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='denominadores_fuente'},ensure_ascii=False))
if __name__=='__main__':resume()
