"""Pruebas con trampas y mutaciones que cambian la medición."""
import ast, copy, json
from pathlib import Path
import ensu_lector as lector

def fixture():
    return [dict(ID_PER=f'{s}-{i}',CD='01',SEXO=str(s),EDAD='38',BP1_1=b,FAC_SEL=w,EST_DIS='1',UPM_DIS=str(i)) for s in (1,2) for i,(b,w) in enumerate([('2','3'),('1','1'),('9','2'),('','4')])]+[dict(ID_PER='OTRA',CD='02',SEXO='1',EDAD='38',BP1_1='2',FAC_SEL='999',EST_DIS='1',UPM_DIS='9')]
def auditar(source):
    tree=ast.parse(source)
    fields={n.slice.value for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='r' and isinstance(n.slice,ast.Constant) and isinstance(n.slice.value,str)}
    if not fields.issubset(lector.CAMPOS): raise ValueError('CAMPO AJENO')
    indexes=[n.slice for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='grupos']
    if any(not isinstance(n,ast.Name) or n.id!='sexo' for n in indexes): raise ValueError('SEGUNDO EJE')
    return True

def ejecutar():
    rows=fixture();out=lector.medir(rows,lector.CAMPOS)
    assert all(abs(x['p0']-.5)<1e-12 for x in out.values())
    assert all(x['n']==3 and x['excluidos_blanco']==1 for x in out.values())
    pruebas=['ponderador','NSNR-en-denominador','blanco-fuera','ciudad-filtro']
    for campo,valor in [('BP1_1','3'),('FAC_SEL','nan'),('FAC_SEL','0'),('SEXO','9'),('EDAD','17'),('ID_PER',''),('UPM_DIS','')]:
        rr=copy.deepcopy(rows);rr[0][campo]=valor
        try: lector.medir(rr,lector.CAMPOS)
        except ValueError: pruebas.append('rechaza-'+campo+'-'+valor)
        else: raise AssertionError(campo)
    rr=copy.deepcopy(rows);rr[1]['ID_PER']=rr[0]['ID_PER']
    try: lector.medir(rr,lector.CAMPOS)
    except ValueError: pruebas.append('duplicado')
    else: raise AssertionError('duplicado')
    try: lector.medir(rows,lector.CAMPOS-{'FAC_SEL'})
    except ValueError: pruebas.append('falta-esquema')
    else: raise AssertionError('esquema')
    rr=copy.deepcopy(rows)
    for r in rr:r['UPM_DIS']='1'
    assert all(x['se_taylor'] is None for x in lector.medir(rr,lector.CAMPOS).values());pruebas.append('singleton-bloquea-inferencia')
    rr=fixture();rr[0]['UPM_DIS']='10'
    result=lector.medir(rr,lector.CAMPOS)
    assert result['1']['upm']==5 and result['2']['upm']==5
    pruebas.append('marco-UPM-ambos-sexos')
    source=Path(lector.__file__).read_text()
    assert auditar(source)
    for mutant in [source.replace('grupos[sexo].append','grupos[(sexo,edad)].append'),source.replace("int(r['EDAD'])","int(r['OTRO_CAMPO'])")]:
        try: auditar(mutant)
        except ValueError: pass
        else: raise AssertionError('auditoria fuga')
        pruebas.append('mutacion-auditoria-eje-campo')
    for antes,despues in [('int(b)==2','int(b)==1'),("{'1','2','9'}","{'1','2'}"),("r['CD'] != '01'","r['CD'] != '02'"),('w=float(r[\'FAC_SEL\'])','w=1.0')]:
        assert antes in source
        module={};exec(compile(source.replace(antes,despues),'<mutacion>','exec'),module)
        try:
            mutant=module['medir'](rows,lector.CAMPOS)
            assert any(abs(v['p0']-.5)>1e-12 for v in mutant.values())
        except ValueError: pass
        pruebas.append('mutacion-detectada-'+antes)
    tree=ast.parse(source)
    assert not any(isinstance(n,ast.Import) and any(a.name in {'subprocess','requests'} for a in n.names) for n in ast.walk(tree))
    assert lector.CAMPOS=={'ID_PER','CD','SEXO','EDAD','BP1_1','FAC_SEL','EST_DIS','UPM_DIS'}
    pruebas.append('auditoria-AST-esquema-sin-red')
    return {'estado':'VERDE','pruebas':pruebas,'fixture':'SINTETICO-NO-MEDICION'}
if __name__=='__main__':
    out=ejecutar();Path(__file__).with_name('ensu-sintetico-auditoria.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
