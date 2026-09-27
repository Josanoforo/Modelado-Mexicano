"""Protege fallos reales: cachés en inventario, enmienda no fijada, I/O Path
fuera de perímetro y serialización futura omitida por el cierre anterior.
"""
import importlib.util
import io
import json
from pathlib import Path
import shutil
import zipfile

import numpy as np
import pytest
import yaml

from auditoria_sucesora import RutasExactas, audita
from cierre import ROOT, AREA, AREA_REL, verifica, sha


def carga(nombre, path):
    s = importlib.util.spec_from_file_location(nombre, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


@pytest.fixture
def inventario():
    return json.loads((AREA/'inventario-portable.json').read_text())


@pytest.mark.parametrize('rel', [
    'forense/analisis/familias-2027/astra6-encig/enmienda-verificacion.json',
    'tools/familias-2027/encig/evaluar.py',
    'tools/familias-2027/encig/cierre.py',
    'forense/analisis/familias-2027/astra6-encig/pisos.json',
    'tools/familias-2027/enif/lector-futuro-serializacion-v2.py',
    'data/corrida0/CALC-FAMILIA-2027-ENIF-ORO-0002/medidor.py',
])
def test_mutacion_hash_ajeno_rechazado(tmp_path, inventario, rel):
    for name in inventario['archivos']:
        dest = tmp_path/name;dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, dest)
    target = tmp_path/AREA_REL/'inventario-portable.json'
    shutil.copyfile(AREA/'inventario-portable.json', target)
    (tmp_path/rel).write_bytes((tmp_path/rel).read_bytes()+b'\nMUTACION\n')
    with pytest.raises(ValueError, match='HASH-DISCORDANTE'):
        verifica(tmp_path, esperado=sha(target.read_bytes()))


def test_mutacion_inventario_y_ruta(tmp_path, inventario):
    p = tmp_path/AREA_REL/'inventario-portable.json';p.parent.mkdir(parents=True)
    original = (AREA/'inventario-portable.json').read_bytes()
    obj = json.loads(original)
    k = next(iter(obj['archivos']));obj['archivos']['../ajeno'] = obj['archivos'].pop(k)
    p.write_text(json.dumps(obj))
    with pytest.raises(ValueError, match='INVENTARIO-MUTADO'):
        verifica(tmp_path, esperado=sha(original))
    with pytest.raises(ValueError, match='RUTA-AJENA'):
        verifica(tmp_path, inv={'archivos':{'../ajeno': '0'}}, esperado=sha(p.read_bytes()))


def test_sin_caches_y_enmienda_cubierta(inventario):
    assert not any('__pycache__' in p or p.endswith('.pyc') for p in inventario['archivos'])
    assert 'forense/analisis/familias-2027/astra6-encig/enmienda-verificacion.json' in inventario['archivos']
    for rel in ('tools/familias-2027/enif/lector-futuro-serializacion-v2.py',
                'data/corrida0/CALC-FAMILIA-2027-ENIF-ORO-0002/medidor.py'):
        code = (ROOT/rel).read_text()
        assert audita(code, inventario['archivos'][rel])['estado'] == 'CODIGO-AUTENTICADO'
        # pathlib importado con alias no evade la identidad fijada.
        with pytest.raises(ValueError,match='CODIGO-EFECTIVO-DISCORDANTE'):
            audita(code+'\nfrom pathlib import Path as P\nP("/ajeno").read_bytes()\n',inventario['archivos'][rel])


@pytest.mark.parametrize('operacion', ['read_bytes','read_text','write_bytes','write_text','open','builtin'])
def test_path_y_open_ajenos_rechazados(tmp_path, operacion):
    permitido = tmp_path/'input';permitido.write_bytes(b'1')
    ajeno = tmp_path/'ajeno';ajeno.write_bytes(b'secreto-sintetico')
    g = RutasExactas([permitido])
    with pytest.raises(PermissionError), g.aplica():
        if operacion == 'builtin':
            open(str(ajeno), 'rb')
        elif operacion.startswith('write'):
            getattr(ajeno, operacion)(b'2' if operacion.endswith('bytes') else '2')
        else:
            getattr(ajeno, operacion)()
    assert ajeno.read_bytes() == b'secreto-sintetico'


def test_symlink_y_escape_de_tablas(tmp_path):
    outside = tmp_path/'outside';outside.mkdir()
    folder = tmp_path/'tablas';folder.mkdir()
    dest = folder/'replicas.json'
    g = RutasExactas([], [dest], [folder])
    with g.aplica():
        dest.write_bytes(b'[]');assert dest.read_bytes() == b'[]'
        with pytest.raises(PermissionError):
            (folder/'../outside/x').write_bytes(b'1')
    dest.unlink();dest.symlink_to(outside/'x')
    with pytest.raises(PermissionError), g.aplica():
        dest.write_bytes(b'1')
    assert not (outside/'x').exists()


def zip_sintetico(m, path, rama):
    # Muestra artificial; no es insumo futuro ni se escribe en data/raw.
    n = 10080 if rama == 'soporte' else 12
    out = io.StringIO();out.write(','.join(m.COLS)+'\n')
    for j in range(n):
        r = dict.fromkeys(m.COLS,'2')
        r.update(LLAVEMOD=str(j),FAC_PER='1',EDAD_V='98',
                 EST_DIS='' if rama == 'nulos' else str(j % 180),
                 UPM_DIS=str((j//180)%6))
        r['P5_6_1'] = '1' if j%2 else 'b'
        r['P5_1_1'] = '1' if j%3 else '2'
        out.write(','.join(r[c] for c in m.COLS)+'\n')
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('TMODULO.csv', out.getvalue())


@pytest.mark.parametrize('rama',['soporte','parcial','nulos'])
def test_futuro_v2_real_con_guardia_y_conducto(tmp_path, monkeypatch, inventario, rama):
    rel = 'tools/familias-2027/enif/lector-futuro-serializacion-v2.py'
    audita((ROOT/rel).read_text(),inventario['archivos'][rel])
    m = carga('futuro_guardado_'+rama, ROOT/rel)
    c = carga('conducto_guardado_'+rama, ROOT/'tools/corrida0.py')
    cid = 'CALC-FAMILIA-2027-ENIF-EVALUACION-0001'
    d = tmp_path/'data/corrida0'/cid;d.mkdir(parents=True)
    monkeypatch.setattr(m,'__file__',str(d/'medidor.py'))
    monkeypatch.setattr(c,'RAIZ',tmp_path)
    raw = tmp_path/'SINTETICO.zip';zip_sintetico(m,raw,rama)
    inputs = {k:{'bytes':(ROOT/'data/corrida0'/k/'resultados.json').read_bytes()} for k in m.PISOS_HASH}
    inputs['enif_2027'] = {'ruta_absoluta':str(raw)}
    meta = {'unidad':'persona18+','peso':'FAC_PER','formal':list(m.FORMAL),
            'informal':list(m.INFORMAL),'periodo':'ultimos12meses'}
    contrato = {'estado':'RESERVADA','autoridad_ola':'SINTETICO-SIN-R',
                'comparabilidad_cotejada':True,'metadatos':meta}
    # Pre-cargar RNG y módulos numpy antes del contexto acotado.
    np.random.default_rng(1).multinomial(2,[.5,.5],size=1)
    files = [d/'tablas'/('d-k-'+fam+'.json') for fam in ('ahorro-formal','horizonte-ahorro')]
    g = RutasExactas([raw],files,[d/'tablas'])
    with g.aplica():
        out = m.medir_futuro(inputs,contrato)
    schema = yaml.safe_load((ROOT/'tools/familias-2027/enif/contrato-futuro-serializacion-v2.yaml').read_text())
    assert c._fallas_run(schema,out,0,'',d) == []
    assert set(out) == {r['id'] for r in schema['resultados']}
    for fam in ('AHORRO-FORMAL','HORIZONTE-AHORRO'):
        ref = out['RESULT-FAMILIA-ENIF-FUTURO-'+fam+'-D-K']
        assert ref.startswith('REF:')
        data = json.loads(files[0 if fam=='AHORRO-FORMAL' else 1].read_bytes())
        assert all(np.isfinite(data))
        if rama == 'nulos':
            assert out['RESULT-FAMILIA-ENIF-FUTURO-'+fam+'-LO'] is None
            assert data == []
    # Mismo lector, sin parche: la guardia actúa antes de abrir un ZIP ajeno.
    inputs['enif_2027']['ruta_absoluta'] = str(tmp_path/'AJENO.zip')
    with pytest.raises(PermissionError), g.aplica():
        m.medir_futuro(inputs,contrato)
