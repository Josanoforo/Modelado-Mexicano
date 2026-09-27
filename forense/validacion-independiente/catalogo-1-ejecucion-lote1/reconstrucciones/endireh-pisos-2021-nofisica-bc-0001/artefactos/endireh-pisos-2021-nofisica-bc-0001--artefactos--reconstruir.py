#!/usr/bin/env python3
"""Reconstrucción independiente; solo entradas locales, sin resultados de referencia."""
import csv
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
import zipfile
from collections import Counter
import numpy as np

ROOT = Path(__file__).resolve().parent
RAW = Path('/raw')
SEED = 20260923
B = 200
AB = {23, 24, 35, 36, 37, 38}
GROUPS = {'emocional_control': range(10,25), 'sexual': range(25,30),
          'digital': range(30,32), 'economica_patrimonial': range(32,39),
          'no_fisica_alguna': range(10,39)}

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''): h.update(block)
    return h.hexdigest()

def dump(name, obj):
    (ROOT/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')

def rows(z, filename):
    with z.open('bd_endireh_2021_csv/'+filename) as f:
        yield from csv.DictReader(io.TextIOWrapper(f, encoding='latin1'))

def act(row, i, window):
    suffix = str(i)+('AB' if i in AB else '')
    life = row.get('P14_1_'+suffix, '')
    if window == '14.1': return life
    if window != '14.3': raise ValueError(window)
    if life == '4': return '4'
    # 14.3 solo tiene significado cuando 14.1 registra un acto positivo.
    return row.get('P14_3_'+suffix, '') if life in ('1','2','3') else ''

def union(row, acts, window='14.1'):
    values = [act(row, i, window) for i in acts
              if not (row['T_INSTRUM'].startswith('C') and i in AB)]
    if any(v in ('1','2','3') for v in values): return 1
    if values and all(v == '4' for v in values): return 0
    return -1

def segment(row, dem, axis, value):
    if axis == 'nacional': return value == 'MX'
    if axis == 'pareja': return row['T_INSTRUM'] == value
    if axis == 'localidad': return row['DOMINIO'] == value
    if axis == 'entidad': return row['CVE_ENT'] == value
    if axis == 'edad':
        s = dem['EDAD']
        if not s.isdigit() or int(s) >= 98: return False
        age = int(s)
        return {'15-29':15<=age<=29, '30-44':30<=age<=44,
                '45-59':45<=age<=59, '60+':60<=age<98}[value]
    raise ValueError('Eje no identificado: '+axis)

def identity_problem(r):
    if r['conducta'] in GROUPS:
        return 'Falta ventana 14.1/14.3 en la identidad; celda y llave son identificadores opacos, sin correspondencia documentada.'
    if r['eje'] == 'escolaridad':
        return 'Falta recodificación NIV/GRA a ninguno/basica/media_superior/superior (preescolar, estudios técnicos y normal); no se infiere.'
    return ''

def selftest():
    r={'T_INSTRUM':'C1', **{'P14_1_'+str(i):'4' for i in range(1,39)}}
    assert union(r, range(10,39)) == 0
    r['P14_1_10']='9'
    assert union(r, range(10,39)) == -1
    r['P14_1_11']='1'
    assert union(r, range(10,39)) == 1
    assert act(r,12,'14.3') == '4'
    assert act(r,10,'14.3') == ''
    r['P14_3_11']='3'
    assert union(r, range(10,39),'14.3') == 1
    r['T_INSTRUM']='A1'
    assert union(r, [23]) == -1
    r['P14_1_23AB']='4'
    assert union(r, [23]) == 0


def main():
    selftest()
    if (ROOT/'reconstruccion.tsv').exists():
        raise RuntimeError('Se conserva el primer resultado. Use una copia limpia para reproducción.')
    specs=list(csv.DictReader((ROOT/'entrada/estimandos.tsv').open(), delimiter='\t'))
    assert len({r['llave'] for r in specs}) == len(specs)
    manifest=json.loads((ROOT/'entrada/manifiesto.json').read_text())
    entries={name:sha(ROOT/'entrada'/name) for name in manifest['archivos']}
    assert entries == manifest['archivos'], 'Entrada alterada'
    supplies=json.loads((ROOT/'entrada/insumos.json').read_text())
    inventory=[]
    for item in supplies:
        path=RAW/(item['id']+('.zip' if item['id'].endswith('_zip') else '.pdf'))
        digest=sha(path)
        assert digest == item['sha256'], 'Insumo alterado: '+str(path)
        inventory.append({**item, 'ruta_recibida':str(path), 'sha256_recalculado':digest,
                          'verificacion_sha256':True})
    dump('recibo.json', {'manifiesto_sha256':sha(ROOT/'entrada/manifiesto.json'),
        'manifiesto_recibido':manifest, 'entradas_verificadas':entries,
        'insumos':inventory, 'resultados_esperados_accedidos':False,
        'revelacion_solicitada':False, 'alcance':'Solo /entrada y /raw; no se buscaron reservas ni resultados.',
        'python':platform.python_version(), 'numpy':np.__version__,
        'semilla':SEED, 'replicas':B, 'rng':'numpy.random.Generator(PCG64)',
        'autopruebas':'Reglas de unión, desconocidos, salto 14.3 y actos AB: aprobadas'})
    with zipfile.ZipFile(RAW/'endireh2021_bd_csv_zip.zip') as z:
        zip_entries=[]
        for info in z.infolist():
            h=hashlib.sha256()
            with z.open(info) as f:
                for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
            zip_entries.append({'entrada':info.filename,'bytes':info.file_size,'sha256':h.hexdigest()})
        dump('entradas_zip.json',zip_entries)
        data=list(rows(z,'TB_SEC_XIV.csv'))
        ids=[r['ID_PER'] for r in data]
        assert len(set(ids))==len(ids)
        wanted=set(ids)
        dem={}
        for r in rows(z,'TSDem.csv'):
            if r['ID_PER'] in wanted:
                assert r['ID_PER'] not in dem
                dem[r['ID_PER']]={k:r[k] for k in ['EDAD','NIV','GRA']}
        reasons={}
        for r in rows(z,'TB_SEC_XIV_2.csv'):
            assert r['ID_PER'] not in reasons
            reasons[r['ID_PER']]={k:r[k] for k in r if k.startswith('P14_22_')}
    assert wanted <= dem.keys() and wanted <= reasons.keys()
    # Marco completo de XIV, incluido C2 y mujeres sin contribución a cada celda.
    pairs=sorted({(r['EST_DIS'],r['UPM_DIS']) for r in data})
    index={pair:i for i,pair in enumerate(pairs)}
    psu=np.array([index[r['EST_DIS'],r['UPM_DIS']] for r in data])
    weights=np.array([float(r['FAC_MUJ']) for r in data])
    assert np.all(np.isfinite(weights)) and np.all(weights>0)
    strata={s:np.array([i for i,p in enumerate(pairs) if p[0]==s]) for s in sorted({p[0] for p in pairs})}
    assert all(len(v)>1 for v in strata.values())
    rng=np.random.default_rng(SEED)
    counts=np.zeros((B,len(pairs)),dtype=np.int16)
    for indices in strata.values():
        n=len(indices)
        draws=rng.integers(0,n,size=(B,n))
        for b in range(B): counts[b,indices]=np.bincount(draws[b],minlength=n)
    eligible=np.array([r['T_INSTRUM'] in ('B1','B2','C1') and
                       dem[r['ID_PER']]['EDAD'].isdigit() and
                       15<=int(dem[r['ID_PER']]['EDAD'])<=98 and
                       union(r,range(1,39))==1 for r in data])
    output=[]; diagnostics=[]; replicas=[]
    for spec in specs:
        row={'llave':spec['llave'],'punto':'','ic95_inf':'','ic95_sup':'',
             'estado':'NO-RECALCULABLE-DESDE-SPEC','motivo':identity_problem(spec)}
        if row['motivo']:
            output.append(row); continue
        behavior=spec['conducta']
        denom=eligible.copy()
        if behavior in ('ayuda_bc','denuncia_bc'):
            key='P14_7_'+('1' if behavior=='ayuda_bc' else '2')
            vals=[r[key] for r in data]; valid=('1','2')
        elif behavior.startswith('institucion_bc_'):
            key='P14_8_'+str(int(behavior.rsplit('_',1)[1]))
            vals=[r[key] for r in data]; valid=('1','2')
            denom &= np.array([r['P14_7_1']=='1' for r in data])
        elif behavior.startswith('razon_bc_'):
            key='P14_22_'+str(int(behavior.rsplit('_',1)[1]))
            vals=[reasons[r['ID_PER']][key] for r in data]; valid=('0','1')
            denom &= np.array([r['P14_7_1']=='2' and r['P14_7_2']=='2' for r in data])
        else: raise ValueError('Conducta no identificada: '+behavior)
        denom &= np.array([v in valid for v in vals])
        denom &= np.array([segment(r,dem[r['ID_PER']],spec['eje'],spec['segmento']) for r in data])
        positive=denom & np.array([v=='1' for v in vals])
        n=int(denom.sum()); npsu=int(len(set(psu[positive])))
        diag={'llave':spec['llave'],'n_conocido':n,'upm_con_casos':npsu}
        if n<100 or npsu<5:
            row['motivo']='Sin cifras por regla de publicación: n conocido <100 o UPM con casos <5; no se difunden réplicas.'
        else:
            totals=np.bincount(psu,weights=weights*denom,minlength=len(pairs))
            cases=np.bincount(psu,weights=weights*positive,minlength=len(pairs))
            point=cases.sum()/totals.sum()
            rd=counts@totals
            if np.any(rd<=0):
                row['motivo']='Remuestreo con denominador cero; la spec no define tratamiento.'
            else:
                rp=(counts@cases)/rd
                lo,hi=np.quantile(rp,[.025,.975],method='linear')
                cv=float(np.std(rp,ddof=1)/point) if point>0 else 0.
                if hi-lo>.20 or (point>0 and cv>.30):
                    row['motivo']='Sin cifras por regla de publicación: ancho IC >0.20 o CV >0.30; no se difunden réplicas.'
                else:
                    row.update(punto=format(point,'.17g'),ic95_inf=format(lo,'.17g'),
                               ic95_sup=format(hi,'.17g'),estado='RECONSTRUIDO',motivo='')
                    replicas.extend({'llave':spec['llave'],'replica':b+1,'proporcion':format(p,'.17g')} for b,p in enumerate(rp))
        diag['estado']=row['estado'];diagnostics.append(diag);output.append(row)
    for filename, items, fields in [
        ('reconstruccion.tsv',output,['llave','punto','ic95_inf','ic95_sup','estado','motivo']),
        ('replicas.tsv',replicas,['llave','replica','proporcion']),
        ('diagnostico.tsv',diagnostics,['llave','n_conocido','upm_con_casos','estado'])]:
        with (ROOT/filename).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(items)
    summary={'filas':len(output),'estados':dict(Counter(r['estado'] for r in output)),
             'motivos':dict(Counter(r['motivo'] for r in output if r['motivo'])),
             'marco_upm':len(pairs),'estratos':len(strata),'filas_xiv':len(data),
             'primer_resultado':True}
    dump('resumen.json',summary)
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':
    if '--selftest' in sys.argv: selftest(); print('Autopruebas aprobadas')
    else: main()
