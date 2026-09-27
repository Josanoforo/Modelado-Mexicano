#!/usr/bin/env python3
"""Reconciliación por identidad, sin extrapolar la selección al catálogo."""
from collections import Counter
import csv
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'forense/validacion-independiente/catalogo-1-ejecucion-lote2'
def load(p):
    with p.open(newline='') as f: return list(csv.DictReader(f,delimiter='\t'))
def write(p,rs):
    with p.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]),delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(rs)
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
    ic_contract_path=BASE/'p3/insuficiencia-ic-exacto.tsv'
    ic_contract={r['llave']:r for r in load(ic_contract_path)} if ic_contract_path.exists() else {}
    output=[]
    for identity in identities:
        identity={k:v for k,v in identity.items() if k not in {'estado','comparacion_punto','comparacion_ic','publicabilidad','spec'}}
        key=identity['llave']; package=identity['sucesor']; e=receipts.get(package,{})
        impediment=impediments.get(package,{})
        technical=compared.get(key,{})
        paths=sorted((BASE/'p3/dictamenes').glob(package+'--dictamen*.json'),key=lambda p:int(re.search(r'--dictamen-v(\d+)',p.name).group(1)) if re.search(r'--dictamen-v(\d+)',p.name) else 1)
        path=paths[-1] if paths else BASE/'p3/dictamenes'/(package+'--dictamen.json')
        adjudication={r['llave']:r for r in json.loads(path.read_text())['resultados']} if path.exists() else {}
        result=adjudication.get(key,technical); row=own.get(key,{})
        fields=result.get('campos',{})
        point=('COINCIDE' if fields['punto']['dentro'] else 'DISCREPA') if 'punto' in fields else (row.get('estado') if row.get('estado') in {'NO-RECALCULABLE-DESDE-SPEC','BLOQUEADO-POR-ACCESO','NO-EVALUADO'} else impediment.get('estado','NO-EVALUADO'))
        ic=[v['dentro'] for k,v in fields.items() if k.startswith('ic95_')]
        interval=('COINCIDE' if all(ic) else 'DISCREPA') if ic else (row.get('estado_ic') or (row.get('estado') if row.get('estado') in {'NO-RECALCULABLE-DESDE-SPEC','BLOQUEADO-POR-ACCESO'} else '') or ('SIN-IC-DE-REFERENCIA' if row.get('naturaleza_ic')=='SIN-IC-IDENTIFICADO' or any('sin referencia' in n for n in result.get('notas',[])) else 'NO-EVALUADO'))
        state=result.get('estado') or impediment.get('estado') or 'NO-EVALUADO'
        apartado=package=='endireh-pisos-2016-pareja-fisica-0002-v2'
        if apartado:
            state='NO-EVALUADO'
            point='NO-EVALUADO'
            interval='NO-EVALUADO'
        # Empty numerical fields never establish reconstructed numerical coverage.
        publication='APARTADA-POR-DEFECTO-DE-PAQUETE' if apartado else result.get('publicabilidad','PENDIENTE-DE-ADJUDICACION' if row else 'NO-EVALUADO')
        output.append(dict(identity,estado=state,estado_comparador=technical.get('estado',e.get('estado','NO-EVALUADO')),
            estado_punto=point,estado_ic=interval,estado_publicabilidad=publication,
            estado_spec=('PAQUETE-SIN-IDENTIDAD-DE-VENTANA' if apartado else 'INSUFICIENTE-PARA-PUNTO-E-IC' if row.get('estado')=='NO-RECALCULABLE-DESDE-SPEC' and row.get('estado_ic')=='NO-RECALCULABLE-DESDE-SPEC' else 'INSUFICIENTE-PARA-IC' if row.get('estado_ic')=='NO-RECALCULABLE-DESDE-SPEC' else result.get('spec','INSUFICIENTE' if state=='NO-RECALCULABLE-DESDE-SPEC' else 'NO-DICTAMINADA')),
            motivo=row.get('motivo') or row.get('motivo_ic') or row.get('explicacion') or impediment.get('motivo',''),
            separacion_efectiva=bool(e.get('separacion_efectiva')),commit_reconstruccion=e.get('commit_reconstruccion',''),
            reconstruccion_sha256=e.get('reconstruccion_sha256',''),estado_validador=row.get('estado',''),apartado_por_adenda=apartado,estado_ejecucion='INTENTO-DIAGNOSTICO-PRESERVADO' if apartado else 'EJECUTADO' if e else 'PENDIENTE',notas_dictamen='; '.join(result.get('notas',[]))))
    for r in output:
        if r['llave'] in ic_contract: r['estado_spec']=ic_contract[r['llave']]['estado_spec']
    assert len(output)==len({r['llave'] for r in output})==425
    assert set(own)<= {r['llave'] for r in output}
    write(BASE/'lote2-tabla-estimadores.tsv',output)
    numerical=sum(r['estado_punto'] in {'COINCIDE','DISCREPA'} for r in output)
    denominators=json.loads((BASE/'p4/cobertura-base.json').read_text())
    summary={'identidades':len(output),'entradas_recibidas':len(entries),'estados':dict(Counter(r['estado'] for r in output)),
        'punto':dict(Counter(r['estado_punto'] for r in output)), 'ic':dict(Counter(r['estado_ic'] for r in output)),
        'publicabilidad':dict(Counter(r['estado_publicabilidad'] for r in output)),
        'spec':dict(Counter(r['estado_spec'] for r in output)),
        'cobertura_numerica_ciega':numerical,'denominador_lote':len(output), 'ejecutables_por_adenda':sum(not r['apartado_por_adenda'] for r in output), 'apartadas_por_adenda':sum(r['apartado_por_adenda'] for r in output),
        'denominador_historico':denominators['historico_denominador'], 'denominador_overlay':denominators['overlay_denominador'], 'cobertura_lote':numerical/len(output), 'cobertura_historico':numerical/denominators['historico_denominador'], 'cobertura_overlay':numerical/denominators['overlay_denominador'], 'denominadores_fuente':denominators,'C1_cerrado':False,
        'alcance':'Selección por preparación, sin inferencia de tasa representativa global; dependencia por instrumento/ola.'}
    (BASE/'resumen-lote2.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='denominadores_fuente'},ensure_ascii=False))
if __name__=='__main__':resume()
