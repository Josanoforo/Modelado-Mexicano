"""P2 independiente: sintéticos exclusivamente; nunca abre microdatos/futuro."""
import ast
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import zipfile

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'tools/familias-2027/encig/lector.py'


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


@pytest.fixture
def lector():
    return module(SOURCE, 'encig_p2')


@pytest.fixture
def reglas():
    # Umbrales exclusivos del experimento sintético; no modifican norma real.
    return dict(seed=83, replicas=300, min_n=1, min_estratos=1, min_upm=1,
                min_replicas=1, fraccion_replicas=.1, banda=.125,
                residuo_max={'PAGO-DIGITAL': .1, 'SOLICITUD-MORDIDA': .1})


def tables():
    ps, ev = [], []
    for i in range(4):
        ps.append(dict(ID_PER=str(i), P8_3_1=str(1 if i % 2 == 0 else 2),
                       FAC_P18=str(10 if i % 2 == 0 else 30), EST_DIS=str(i//2), UPM_DIS=str(i)))
        ev.append(dict(ID_PER=str(i), ID_TRA=str(i), NT_TIPO='1', N_TRA='1',
                       P7_3=str(4 if i % 2 == 0 else 1), FAC_TRA=str(3 if i % 2 == 0 else 1),
                       FAC_P18=str(10 if i % 2 == 0 else 30), EST_DIS=str(i//2), UPM_DIS=str(i)))
    ev.append(dict(ev[1], ID_TRA='excluded', N_TRA='2', FAC_TRA='999', P7_3='4'))
    return dict(persona=ps, evento=ev)


def zipdata(tmp_path, lector, t=None):
    path = tmp_path / 'synthetic.zip'
    t = tables() if t is None else t
    with zipfile.ZipFile(path, 'w') as z:
        for rol, name in [('persona', lector.PERSONA), ('evento', lector.EVENTO)]:
            out = io.StringIO()
            writer = csv.DictWriter(out, fieldnames=list(lector.COLS[rol]))
            writer.writeheader()
            writer.writerows({k: row[k] for k in lector.COLS[rol]} for row in t[rol])
            z.writestr('base/'+name, out.getvalue())
        z.writestr('prohibida.csv', 'secret')
    return path


def test_pesos_universo_y_replicas(lector, reglas):
    f = lector.estima(tables(), reglas)['familias']
    assert f['PAGO-DIGITAL']['p'] == .75
    assert f['SOLICITUD-MORDIDA']['p'] == .25
    assert f['PAGO-DIGITAL']['soporte']['n'] == 4
    assert f['PAGO-DIGITAL']['soporte']['masa_denominador'] == 8
    # Both outcomes share draws: complementary binary numerator counts.
    for a, b in zip(f['PAGO-DIGITAL']['replicas'], f['SOLICITUD-MORDIDA']['replicas']):
        assert a / (3-2*a) == pytest.approx(3*b / (1+2*b))


def test_marco_cero_y_singleton_dominio(lector, reglas):
    t = tables()
    for row in t['persona'][1:]: row['P8_3_1'] = ''
    t['evento'] = t['evento'][:1]
    r = lector.estima(t, reglas)
    assert r['marco'] == dict(estratos=2, upm=4, estratos_upm_unica=0)
    f = r['familias']['PAGO-DIGITAL']
    assert f['soporte']['estratos_upm_unica_dominio'] == 1
    assert f['estado'] == 'ESTIMABLE'
    assert 0 < f['soporte']['replicas_validas'] < reglas['replicas']
    assert f['replicas'] == r['familias']['SOLICITUD-MORDIDA']['replicas']


@pytest.mark.parametrize('case', ['duplicate_person', 'duplicate_event', 'design', 'missing_design', 'missing_person', 'empty_event'])
def test_llaves_y_diseno(lector, reglas, case):
    t=tables()
    if case=='duplicate_person': t['persona'].append(t['persona'][0].copy())
    if case=='duplicate_event': t['evento'].append(t['evento'][0].copy())
    if case=='design': t['evento'][0]['UPM_DIS']='wrong'
    if case=='missing_design': t['persona'][0]['EST_DIS']=''
    if case=='missing_person': t['evento'][0]['ID_PER']='no'
    if case=='empty_event': t['evento'][0]['ID_TRA']=''
    with pytest.raises(ValueError): lector.estima(t, reglas)


@pytest.mark.parametrize('gate', ['min_n','min_estratos','min_upm','min_replicas','fraccion_replicas','residuo','weight','singleton','empty'])
def test_gates(lector, reglas, gate):
    t=tables()
    if gate.startswith('min_'): reglas[gate]=1000
    elif gate=='fraccion_replicas': reglas[gate]=1.1
    elif gate=='residuo': t['evento'][0]['P7_3']='9'
    elif gate=='weight': t['evento'][0]['FAC_TRA']='nan'
    elif gate=='singleton': t['persona']=t['persona'][:1]; t['evento']=t['evento'][:1]
    elif gate=='empty': t['evento']=[]
    f=lector.estima(t, reglas)['familias']['PAGO-DIGITAL']
    assert f['estado']=='NO-ESTIMABLE'
    if gate=='empty': assert f['p'] is None and f['ic']==[None,None]


@pytest.mark.parametrize('lo,hi,expected', [(-.125,.125,'COMPATIBLE-CON-TOLERANCIA'),(.126,.2,'DESVÍO-MATERIAL'),(-.3,-.126,'DESVÍO-MATERIAL'),(-.2,.1,'INDETERMINADO'),(None,None,'NO-ESTIMABLE'),(.2,.1,'NO-ESTIMABLE')])
def test_fronteras(lector, lo, hi, expected):
    assert lector.etiqueta(lo,hi,.125)==expected


def metadata(lector):
    return dict(instrumento='ENCIG',ola='2027',estado_reserva='RESERVADA',unidad_persona='PERSONA',unidad_evento='PAGO-LUZ',peso_persona='FAC_P18',peso_evento='FAC_TRA',solicitud_si=[1],solicitud_no=[2],digital=[4,5],no_digital=[1,2,6],universo='URBANO-100MIL-18PLUS',cuestionario_sha256='synthetic',descriptor_sha256='synthetic',autorizacion=dict(acto='ASTRA6-C2-ENCIG-1',ola='encig_2027',familias=list(lector.FAMILIAS),apertura='UNICA',asiento_firmado='synthetic',codigo_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest()))


def test_futuro_guardias_antes_io(lector, reglas, monkeypatch):
    def forbidden(*a, **k): raise AssertionError('IO before authorization')
    monkeypatch.setattr(lector.Path,'read_bytes',forbidden)
    assert lector.abrir_futuro('does-not-exist',{},reglas,{})=={'estado':'NO-COMPARABLE'}
    m=metadata_without_io(lector)
    m['miembros']={'persona':lector.PERSONA.replace('2025','2027'),'evento':lector.EVENTO.replace('2025','2027')}
    with pytest.raises(PermissionError,match='APERTURA'): lector.abrir_futuro('does-not-exist',m,reglas,{})


def metadata_without_io(lector):
    return dict(instrumento='ENCIG',ola='2027',estado_reserva='RESERVADA',unidad_persona='PERSONA',unidad_evento='PAGO-LUZ',peso_persona='FAC_P18',peso_evento='FAC_TRA',solicitud_si=[1],solicitud_no=[2],digital=[4,5],no_digital=[1,2,6],universo='URBANO-100MIL-18PLUS')


@pytest.mark.parametrize('p0,expected',[(.75,'COMPATIBLE-CON-TOLERANCIA'),(0,'DESVÍO-MATERIAL'),(.65,'INDETERMINADO'),(None,'NO-ESTIMABLE')])
def test_futuro_dictamen_sin_futuro(lector,reglas,tmp_path,monkeypatch,p0,expected):
    path=tmp_path/'identity-only';path.write_bytes(b'synthetic')
    m=metadata(lector);m['payload_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    asiento=tmp_path/'forense'/'encargos'/'synthetic-ONLY.txt'
    asiento.parent.mkdir(parents=True)
    asiento.write_text('SYNTHETIC ONLY\nAUTORIZO-APERTURA: encig_2027; ASTRA6-C2-ENCIG-1; UNICA; PAGO-DIGITAL,SOLICITUD-MORDIDA')
    m['autorizacion'].update(asiento_firmado=str(asiento),asiento_sha256=hashlib.sha256(asiento.read_bytes()).hexdigest())
    m['miembros']={'persona':'encig2027_01_sec1_A_3_4_5_8_9_10.csv','evento':'encig2027_04_sec_7.csv'}
    monkeypatch.setattr(lector,'lee_zip',lambda *a: tables())
    def synthetic(*a):
        return {'familias':{name:dict(estado='NO-ESTIMABLE' if p0 is None else 'ESTIMABLE',p=.75,replicas=[.625,.875]) for name in lector.FAMILIAS}}
    monkeypatch.setattr(lector,'estima',synthetic)
    floors={'familias':{name:{'p0':p0} for name in lector.FAMILIAS}}
    r=lector.abrir_futuro(path,m,reglas,floors)
    assert all(f['dictamen']==expected for f in r['familias'].values())


def test_zip_whitelist(lector,tmp_path,monkeypatch):
    path=zipdata(tmp_path,lector)
    original=zipfile.ZipFile.open;opened=[]
    def spy(z,name,*a,**k):
        opened.append(name)
        assert name.split('/')[-1] in {lector.PERSONA,lector.EVENTO}
        return original(z,name,*a,**k)
    monkeypatch.setattr(zipfile.ZipFile,'open',spy)
    lector.lee_zip(path,dict(persona=lector.PERSONA,evento=lector.EVENTO))
    assert len(opened)==2
    with pytest.raises(ValueError): lector.lee_zip(path,dict(persona='prohibida.csv',evento=lector.EVENTO))


def test_aux_outputs_y_nulos(lector,reglas,tmp_path,monkeypatch):
    corrida=module(ROOT/'tools/corrida0.py','corrida_p2')
    monkeypatch.setattr(lector,'__file__',str(tmp_path/'lector.py'))
    for empty in [False,True]:
        branch=tmp_path/str(empty);branch.mkdir()
        monkeypatch.setattr(lector,'__file__',str(branch/'lector.py'))
        t=tables()
        if empty: t['evento']=[]; [row.update(P8_3_1='') for row in t['persona']]
        path=zipdata(branch,lector,t);sha=hashlib.sha256(path.read_bytes()).hexdigest()
        par=dict(reglas,modo='HISTORICO-ABIERTO',payload_sha256=sha,calc_id='SYNTHETIC')
        result=lector.medir({'encig25_base_datos_csv':dict(sha256=sha,ruta_absoluta=str(path))},{'parametros':par})
        spec=yaml.safe_load((ROOT/'data/corrida0/CALC-ENCIG-AUX-FAMILIAS-2027-0001/spec.yaml').read_text())
        assert corrida._valida_outputs(spec,result)==[]
        assert (branch/'tablas/replicas.json').exists()
        if empty: assert result['RESULT-ENCIG-AUX-PAGO-DIGITAL-P'] is None
    with pytest.raises(PermissionError): lector.medir({'extra':{}},{'parametros':par})


def test_emision_guardias():
    emision=module(ROOT/'tools/familias-2027/encig/emision.py','emision_p2')
    data=json.dumps({'familias':{'PAGO-DIGITAL':dict(p0=.75,result_id='ORIGEN')}}).encode()
    source=dict(bytes=data,sha256=hashlib.sha256(data).hexdigest())
    contract={'parametros':dict(familia='PAGO-DIGITAL',result_origen='ORIGEN',result_emision='RESULT')}
    assert emision.medir({'IN-ENCIG-PISOS':source},contract)['RESULT']==.75
    for extra in ['extra','R-futura']:
        with pytest.raises(PermissionError): emision.medir({'IN-ENCIG-PISOS':source,extra:{}},contract)
    with pytest.raises(PermissionError): emision.medir({'IN-ENCIG-PISOS':dict(source,sha256='bad')},contract)


@pytest.mark.parametrize('mutation',["(\"evento\", 0, \"FAC_TRA\"",'if codigo(row["N_TRA"]) != 1:'])
def test_mutaciones_detectadas(lector,reglas,tmp_path,mutation):
    code=SOURCE.read_text()
    if mutation.startswith('('): changed=code.replace(mutation,'("evento", 0, "FAC_P18"')
    else: changed=code.replace(mutation,'if False:')
    assert changed!=code
    path=tmp_path/'mutante.py';path.write_text(changed)
    mutant=module(path,'mutante_p2')
    actual=mutant.estima(tables(),reglas)['familias']['PAGO-DIGITAL']
    assert actual['p']!=.75 or actual['soporte']['n']!=4


def test_ast_perimetro():
    tree=ast.parse(SOURCE.read_text())
    names=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Import): names.extend(x.name for x in node.names)
        if isinstance(node,ast.ImportFrom): names.append(node.module or '')
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name): assert node.func.id not in {'eval','exec','__import__'}
    assert not any(any(x in name for x in ['pandas','subprocess','productor','historico']) for name in names)
    opens=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='open' and isinstance(n.func.value,ast.Name) and n.func.value.id=='z']
    assert len(opens)==1


def test_mutacion_acceso_no_blanco(lector,tmp_path,monkeypatch):
    path=zipdata(tmp_path,lector)
    code=SOURCE.read_text()
    altered=code.replace('if miembros not in blancos:', 'if False:')
    assert altered != code
    target=tmp_path/'mutante_zip.py';target.write_text(altered)
    mutant=module(target,'mutante_zip_p2')
    original=zipfile.ZipFile.open
    def spy(z,name,*a,**k):
        assert name.split('/')[-1] in {lector.PERSONA,lector.EVENTO}, 'ACCESO-NO-BLANCO-DETECTADO'
        return original(z,name,*a,**k)
    monkeypatch.setattr(zipfile.ZipFile,'open',spy)
    with pytest.raises(AssertionError,match='ACCESO-NO-BLANCO'):
        mutant.lee_zip(path,dict(persona='prohibida.csv',evento=lector.EVENTO))


@pytest.mark.parametrize('mode',['ambiguo','columnas','traversal'])
def test_zip_malformado(lector,tmp_path,mode):
    path=zipdata(tmp_path,lector)
    if mode=='columnas':
        path=tmp_path/'bad.zip'
        with zipfile.ZipFile(path,'w') as z: z.writestr(lector.PERSONA,'ID_PER\n1\n')
    else:
        with zipfile.ZipFile(path,'a') as z:
            z.writestr(('extra/' if mode=='ambiguo' else '../')+lector.PERSONA,'ID_PER\n1\n')
    with pytest.raises(ValueError): lector.lee_zip(path,dict(persona=lector.PERSONA,evento=lector.EVENTO))


@pytest.mark.parametrize('case', ['code','asiento','payload','historico'])
def test_identidad_no_abre_zip(lector,reglas,tmp_path,monkeypatch,case):
    path=tmp_path/'identity-only';path.write_bytes(b'synthetic')
    m=metadata(lector)
    m['miembros']={'persona':lector.PERSONA.replace('2025','2027'),'evento':lector.EVENTO.replace('2025','2027')}
    m['payload_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    asiento=tmp_path/'forense'/'encargos'/'synthetic-ONLY.txt'
    asiento.parent.mkdir(parents=True)
    asiento.write_text('SYNTHETIC ONLY\nAUTORIZO-APERTURA: encig_2027; ASTRA6-C2-ENCIG-1; UNICA; PAGO-DIGITAL,SOLICITUD-MORDIDA')
    m['autorizacion'].update(asiento_firmado=str(asiento),asiento_sha256=hashlib.sha256(asiento.read_bytes()).hexdigest())
    def nozip(*a): raise AssertionError('ZIP abierto sin identidad')
    monkeypatch.setattr(lector,'lee_zip',nozip)
    if case=='code': m['autorizacion']['codigo_sha256']='bad'
    if case=='asiento': m['autorizacion']['asiento_sha256']='bad'
    if case=='payload': m['payload_sha256']='bad'
    if case=='historico':
        m['miembros']={'persona':lector.PERSONA,'evento':lector.EVENTO}
        assert lector.abrir_futuro(path,m,reglas,{})['estado']=='NO-COMPARABLE'
    else:
        with pytest.raises(PermissionError): lector.abrir_futuro(path,m,reglas,{})


def test_aux_malformado_terminal(lector,reglas,tmp_path,monkeypatch):
    monkeypatch.setattr(lector,'__file__',str(tmp_path/'lector.py'))
    t=tables();t['persona'].append(t['persona'][0].copy())
    path=zipdata(tmp_path,lector,t);sha=hashlib.sha256(path.read_bytes()).hexdigest()
    par=dict(reglas,modo='HISTORICO-ABIERTO',payload_sha256=sha,calc_id='SYNTHETIC')
    result=lector.medir({'encig25_base_datos_csv':dict(sha256=sha,ruta_absoluta=str(path))},{'parametros':par})
    assert result['RESULT-ENCIG-AUX-PAGO-DIGITAL-ESTADO']=='NO-COMPARABLE'
    assert result['RESULT-ENCIG-AUX-PAGO-DIGITAL-P'] is None
    corrida=module(ROOT/'tools/corrida0.py','corrida_terminal_p2')
    spec=yaml.safe_load((ROOT/'data/corrida0/CALC-ENCIG-AUX-FAMILIAS-2027-0001/spec.yaml').read_text())
    assert corrida._valida_outputs(spec,result)==[]


@pytest.mark.parametrize('case',['terminal','singleton','parcial','ambas','denominador_cero','marginal_vacio'])
def test_outputs_futuros_contrato_real(lector,reglas,case):
    corrida=module(ROOT/'tools/corrida0.py','corrida_future_p2')
    spec=yaml.safe_load((ROOT/'tools/familias-2027/encig/evaluacion-spec.yaml').read_text())
    if case=='terminal':
        payload={'estado':'NO-COMPARABLE'}
    else:
        t=tables()
        if case=='singleton': t['persona']=t['persona'][:1];t['evento']=t['evento'][:1]
        if case in ['parcial','marginal_vacio']: t['evento']=[]
        if case=='denominador_cero': t['evento']=t['evento'][:1]
        payload=lector.estima(t,reglas)
        for name,f in payload['familias'].items():
            if f['estado']=='ESTIMABLE':
                vals=[r-.5 for r in f['replicas'] if r is not None]
                f.update(d=f['p']-.5,ic_d=[min(vals),max(vals)],fraccion_en_banda=sum(abs(v)<=reglas['banda'] for v in vals)/len(vals),dictamen=lector.etiqueta(min(vals),max(vals),reglas['banda']))
            else: f.update(d=None,ic_d=[None,None],fraccion_en_banda=None,dictamen='NO-ESTIMABLE')
        if case=='denominador_cero': assert None in payload['familias']['PAGO-DIGITAL']['replicas']
        if case=='parcial': assert [f['estado'] for f in payload['familias'].values()]==['NO-ESTIMABLE','ESTIMABLE']
        if case=='ambas': assert all(f['estado']=='ESTIMABLE' for f in payload['familias'].values())
    outputs=lector.resultados_futuros(payload)
    assert corrida._valida_outputs(spec,outputs)==[]
    assert all(r['permite_no_estimable'] for r in spec['resultados'] if r['tipo']!='texto')
    if case=='terminal': assert all(v=='NO-COMPARABLE' if k.endswith('DICTAMEN') else v is None for k,v in outputs.items())


def test_aux_artefacto_no_reescrito(lector,reglas,tmp_path,monkeypatch):
    monkeypatch.setattr(lector,'__file__',str(tmp_path/'lector.py'))
    path=zipdata(tmp_path,lector);sha=hashlib.sha256(path.read_bytes()).hexdigest()
    contract={'parametros':dict(reglas,modo='HISTORICO-ABIERTO',payload_sha256=sha,calc_id='SYNTHETIC')}
    inputs={'encig25_base_datos_csv':dict(sha256=sha,ruta_absoluta=str(path))}
    first=lector.medir(inputs,contract)
    artifact=tmp_path/'tablas/replicas.json';before=artifact.read_bytes();mtime=artifact.stat().st_mtime_ns
    assert lector.medir(inputs,contract)==first
    assert artifact.read_bytes()==before and artifact.stat().st_mtime_ns==mtime
    t=tables();t['evento'][0]['P7_3']='1'
    path=zipdata(tmp_path,lector,t);sha=hashlib.sha256(path.read_bytes()).hexdigest()
    inputs['encig25_base_datos_csv']['sha256']=sha;contract['parametros']['payload_sha256']=sha
    with pytest.raises(RuntimeError,match='ARTEFACTO-SELLADO-DISCREPA'): lector.medir(inputs,contract)
    assert artifact.read_bytes()==before and artifact.stat().st_mtime_ns==mtime
