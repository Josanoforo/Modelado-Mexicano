#!/usr/bin/env python3
"""Dictamen separado del comparador congelado, sobre números originales inmutables."""
import csv
from datetime import datetime,timezone
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'forense/validacion-independiente/catalogo-1-ejecucion-lote2'
ALIASES={'punto':('punto','valor'),'ic95_inf':('ic95_inf','ic_025'),'ic95_sup':('ic95_sup','ic_975')}
def rows(p):
    opener=gzip.open if str(p).endswith('.gz') else open
    with opener(p,'rt',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dictamina(package):
    contract=json.loads((BASE/'p1/contrato-adaptador-v1.json').read_text())
    freeze=json.loads((BASE/'p1/congelacion-adaptador-v1.json').read_text())
    assert sha(BASE/'p1/contrato-adaptador-v1.json')==freeze['contrato_sha256']
    assert sha(ROOT/'tools/validacion/astra6_lote2/adaptador_comparador_v1.py')==freeze['adaptador_sha256']
    entry=next(e for e in contract['entradas'] if e['paquete']==package)
    received=next(e for e in json.loads((BASE/'p3/lote2-entregas.json').read_text()) if e['paquete']==package)
    original=BASE/'p3'/received['reconstruccion']
    assert sha(original)==received['reconstruccion_sha256']
    spec=importlib.util.spec_from_file_location('proof',ROOT/'tools/validacion/astra6_lote1/prueba_commit.py');proof=importlib.util.module_from_spec(spec);spec.loader.exec_module(proof)
    files=proof.verificar(json.loads((BASE/'p3'/received['prueba_commit']).read_text()))
    assert hashlib.sha256(files[received['ruta_reconstruccion_commit']]).hexdigest()==received['reconstruccion_sha256']
    assert received['congelacion_recibida_utc']<=received['revelacion_utc']
    ownrows=rows(original);own={r['llave']:r for r in ownrows}
    assert len(own)==len(ownrows) and set(own)=={m['llave_sucesor'] for m in entry['correspondencia']}
    expectedpath=ROOT/contract['esperados_ruta']; assert sha(expectedpath)==contract['esperados_sha256']
    expected={r['llave']:r for r in rows(expectedpath) if r['calc']==entry['calc']}
    import tarfile
    with tarfile.open(ROOT/entry['ruta_tar']) as t:tb=t.extractfile('tolerancia.json').read()
    assert hashlib.sha256(tb).hexdigest()==entry['tolerancia_sha256']; tolerance=json.loads(tb)
    out=[]
    for mapping in entry['correspondencia']:
        key=mapping['llave_sucesor'];r=own[key];ref=expected[mapping['llave_original']]
        status=r['estado'];fields={};notes=[]
        if status in {'NO-EVALUADO','NO-RECALCULABLE-DESDE-SPEC','BLOQUEADO-POR-ACCESO'}:
            out.append(dict(llave=key,estado=status,campos={},publicabilidad='NO-DETERMINADA',spec='INSUFICIENTE' if status=='NO-RECALCULABLE-DESDE-SPEC' else 'NO-DICTAMINADA',motivo=r.get('motivo','')));continue
        assert status=='RECONSTRUIDO'
        for field,aliases in ALIASES.items():
            existing=[a for a in aliases if a in r]
            assert len(existing)<=1,'Alias ambiguos'
            actual=r.get(existing[0],'') if existing else '';target=ref.get(field,'')
            if not target:
                if actual:notes.append(field+': emitido independientemente sin referencia en catálogo')
                continue
            if not actual:
                notes.append(field+': ausente en salida independiente');continue
            try:a,b=float(actual),float(target)
            except ValueError:
                notes.append(field+': valor no numérico; requiere dictamen publicabilidad');continue
            assert math.isfinite(a) and math.isfinite(b)
            fields[field]={'delta':a-b,'dentro':math.isclose(a,b,abs_tol=tolerance['abs'],rel_tol=tolerance.get('rel',0)),'columna_original':existing[0]}
        expected_fields={f for f in ALIASES if ref.get(f,'')}
        complete=set(fields)==expected_fields
        state=('COINCIDE' if all(v['dentro'] for v in fields.values()) else 'DISCREPA') if complete and fields else 'NO-RECALCULABLE-DESDE-SPEC'
        publication='AMBOS-SIN-CIFRA' if not expected_fields and not any(r.get(a,'') for a in ALIASES['punto']) else 'CIFRA-EMITIDA' if 'punto' in fields else 'DIFERENCIA-DE-PUBLICABILIDAD'
        out.append(dict(llave=key,estado=state,campos=fields,publicabilidad=publication,spec='SUFICIENTE-PARA-RECONSTRUCCION' if complete and fields else 'REQUIERE-DICTAMEN',motivo=r.get('motivo',''),notas=notes))
    destination=BASE/'p3/dictamenes';destination.mkdir(exist_ok=True)
    with (destination/(package+'--dictamen.json')).open('x') as f:
        json.dump({'paquete':package,'dictamen_utc':datetime.now(timezone.utc).isoformat(),'estado_comparador':received['estado'], 'alcance':'Dictamen separado: alias de nombres sin modificación de valores, tolerancias originales; original congelado previo a revelación. No modifica adaptador ni salida ni adopta. IC sin referencia no acredita coincidencia.', 'alias_transporte':ALIASES, 'original_sha256':received['reconstruccion_sha256'],'commit_original':received['commit_reconstruccion'],'tolerancia':tolerance,'resultados':out},f,ensure_ascii=False,indent=2);f.write('\n')
    print(package,len(out),{s:sum(r['estado']==s for r in out) for s in {r['estado'] for r in out}})
if __name__=='__main__':
    import sys;dictamina(sys.argv[1])
