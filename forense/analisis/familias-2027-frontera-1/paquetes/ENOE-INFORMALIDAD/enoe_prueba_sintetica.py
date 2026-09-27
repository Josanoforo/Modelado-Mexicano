import ast,copy,json
from pathlib import Path
import enoe_lector as lector

def fixture():
    rows=[]
    for s in (1,2):
        for i,(b,w) in enumerate([('1','3'),('2','1'),('','2')]):
            rows.append(dict(R_DEF='00',C_RES='1',EDA='35',SEX=str(s),EMP_PPAL=b,CLASE2='1',FAC_TRI=w,EST_D_TRI='1',UPM=str(i),ENT='01',CON='1',V_SEL=str(i),N_HOG='1',H_MUD='0',N_REN=str(s),N_PRO_VIV=str(i)))
    r=rows[0].copy();r.update(UPM='9',CLASE2='3',EMP_PPAL='',V_SEL='9');rows.append(r)
    r=rows[0].copy();r.update(EDA='99',FAC_TRI='999',V_SEL='10');rows.append(r)
    return rows

def auditar(source):
    tree=ast.parse(source)
    fields={n.slice.value for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='r' and isinstance(n.slice,ast.Constant) and isinstance(n.slice.value,str)}
    if not fields.issubset(lector.CAMPOS):raise ValueError('CAMPO AJENO')
    indexes=[n.slice for n in ast.walk(tree) if isinstance(n,ast.Subscript) and isinstance(n.value,ast.Name) and n.value.id=='grupos']
    if any(not isinstance(n,ast.Name) or n.id!='sexo' for n in indexes):raise ValueError('SEGUNDO EJE')
    return True

def ejecutar():
    rows=fixture();result=lector.medir(rows,lector.CAMPOS)
    assert all(v['p0']==.75 and v['n']==2 and v['upm']==4 and v['excluidos_blanco']==1 for v in result.values())
    checks=['peso-desigual','blanco-excluido','no-ocupado-PSU-cero','edad99-fuera']
    for key,value in [('EMP_PPAL','9'),('FAC_TRI','nan'),('FAC_TRI','0'),('SEX','9'),('UPM',''),('CON',''),('CLASE2','9')]:
        rr=copy.deepcopy(rows);rr[0][key]=value
        try:lector.medir(rr,lector.CAMPOS)
        except ValueError:checks.append('rechaza-'+key+'-'+value)
        else:raise AssertionError(key)
    rr=copy.deepcopy(rows);rr.append(rr[0].copy())
    try:lector.medir(rr,lector.CAMPOS)
    except ValueError:checks.append('duplicado')
    else:raise AssertionError('duplicado')
    try:lector.medir(rows,lector.CAMPOS-{'FAC_TRI'})
    except ValueError:checks.append('esquema-faltante')
    else:raise AssertionError('esquema')
    src=Path(lector.__file__).read_text();assert auditar(src)
    for old,new in [('int(b)==1','int(b)==2'),("{'1','2'}","{'1'}"),("r['CLASE2']!='1'","r['CLASE2']=='1'"),("w=float(r['FAC_TRI'])","w=1.0")]:
        assert old in src;module={};exec(compile(src.replace(old,new),'<mutacion>','exec'),module)
        try:
            m=module['medir'](rows,lector.CAMPOS)
            assert any(v['p0']!=.75 for v in m.values())
        except ValueError:pass
        checks.append('mutacion-detectada-'+old)
    for mutant in [src.replace('grupos[sexo].append','grupos[(sexo,edad)].append'),src.replace("int(r['EDA'])","int(r['OTRO'])")]:
        try:auditar(mutant)
        except ValueError:checks.append('auditoria-eje-campo')
        else:raise AssertionError('auditoria')
    return {'estado':'VERDE','fixture':'SINTETICO-NO-MEDICION','pruebas':checks}
if __name__=='__main__':
    out=ejecutar();Path(__file__).with_name('enoe-sintetico-auditoria.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
