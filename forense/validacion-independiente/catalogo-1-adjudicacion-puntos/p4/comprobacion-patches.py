#!/usr/bin/env python3
"""Verifica propuestas en copias temporales; sin import/run productor ni microdatos."""
import ast
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SOURCES={2011:ROOT/'data/corrida0/CALC-ENDIREH-PISOS-2011-MODULOS-0001',2021:ROOT/'data/corrida0/CALC-ENDIREH-PISOS-2021-NOFISICA-BC-0001'}
PATCHES={2011:['edad-permisos-2011.patch','externos-reciente-2011.patch','denuncia-enlace-2011.patch','spec-sucesor-2011.patch'],2021:['edad-permisos-2021.patch','spec-sucesor-2021.patch']}

def functions(source,names):
    tree=ast.parse(source)
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert len(nodes)==len(names)
    namespace={'np':SimpleNamespace(isfinite=math.isfinite),'KEY':('CONTROL','VIV_SEL','HOGAR','R_SEL_M'),'ACTOR_DOMAINS':{'familiar_agresor':{'01','02','03','04','05','06'},'laboral_agresor':{'07','08'},'escolar_agresor':{'09','10','11'}},'PLACE_DOMAINS':{'comunitaria_lugar':{'01','06','07','08'},'escolar_lugar':{'02'},'laboral_lugar':{'03','04'}}}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'<funciones-propuestas-aisladas>','exec'),namespace)
    return namespace

def main():
    checks=[]; applied=[]; hashes={}
    def check(name,value):
        assert value,name
        checks.append({'caso':name,'estado':'PASS'})
    with tempfile.TemporaryDirectory(prefix='adjudicacion-p4-') as temp:
        directory=Path(temp)
        for year,path in SOURCES.items():
            target=directory/f'sucesor-{year}';target.mkdir()
            for name in ['medidor.py','spec.md']:
                data=(path/name).read_bytes();hashes[f'{year}/{name}']=hashlib.sha256(data).hexdigest();(target/name).write_bytes(data)
            for name in PATCHES[year]:
                proc=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(HERE/name)],cwd=directory,text=True,capture_output=True)
                assert proc.returncode==0,(name,proc.stdout,proc.stderr)
                applied.append({'patch':name,'sha256':hashlib.sha256((HERE/name).read_bytes()).hexdigest(),'resultado':proc.stdout.strip()})
            code=(target/'medidor.py').read_text();ast.parse(code)
            # Solo definición de funciones seleccionadas, jamás cuerpo de módulo/run.
            basic=functions(code,['_age_group','_eligible_age'])
            check(f'{year}: edad97 pertenece60+',basic['_age_group']('97')=='60+')
            check(f'{year}: edad98 elegible global sin corte',basic['_eligible_age']('98') and basic['_age_group']('98') is None)
            check(f'{year}: edad99 excluida opcion propuesta',not basic['_eligible_age']('99') and basic['_age_group']('99') is None)
        source=(directory/'sucesor-2011/medidor.py').read_text()
        ns=functions(source,['_age_group','_eligible_age','_key','_school_group','_base','_binary','_union_binary','_freq','_domain_act','_external','_partner_groups','_reason','_partner','_decisions'])
        fn=ns['_domain_act']; row={'AP2_6_1':'1','AP2_7_1_1':'07','AP2_7_1_2':'99'}
        check('externos:99 impide negativo',fn(row,'AP',1,{'01'},'2_7')==(None,None))
        row['AP2_7_1_2']='';check('externos: blanco opcional permite negativo',fn(row,'AP',1,{'01'},'2_7')==(0,0))
        row['AP2_7_1_1']='12';check('externos:12 es codigo valido',fn(row,'AP',1,{'01'},'2_7')==(0,0))
        row.update(AP2_7_1_1='01',AP2_7_1_2='99',AP2_9_1_1='1');check('externos: coincidencia positiva conservada',fn(row,'AP',1,{'01'},'2_7')==(1,1))
        row.update(AP2_7_1_1='07',AP2_7_1_2='99',AP2_9_1_1='2',AP2_9_1_2='1');check('externos: vida positiva reciente desconocida con99tiempo1',fn(row,'AP',1,{'07','08'},'2_7')==(1,None))
        row['AP2_9_1_2']='2';check('externos: vida positiva reciente desconocida con99tiempo2',fn(row,'AP',1,{'07','08'},'2_7')==(1,None))
        row['AP2_9_1_1']='1';check('externos: reciente positivo preservado pese99',fn(row,'AP',1,{'07','08'},'2_7')==(1,1))
        base={};ns['_decisions']({'CP4_1':'3'},{'CP7_1_1':'1'}, {},'C',base);check('permisos:nunca relacion excluida desde first',base=={})
        ns['_decisions']({'CP4_1':'2'},{'CP7_1_1':'1'}, {},'C',base);check('permisos:relacion anterior incluida',base['permiso_01']==1)
        calls=[n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='_decisions']
        check('permisos:caller pasa first',len(calls)==1 and len(calls[0].args)==5 and ast.unparse(calls[0].args[0])=='r')
        second={f'AP6_1_{i}':'9' for i in range(1,31)};second.update({f'AP6_3_{i}':'4' for i in range(1,31)});base={};ns['_partner']({},second,{},'A',base)
        check('reciente: ventana clasificable con vida desconocida',base['pareja_alguna_vida'] is None and base['pareja_alguna_desde_octubre_2010']==0)
        row={'AP2_6_1':'1','AP2_10_1_1':'01','AP2_10_1_2':'03','AP2_12_1_1':'2','AP2_12_1_4':'1'};base={};ns['_external'](row,'A',base);check('denuncia:columna4 segunda solicitud incluida',base['externo_denuncia_ultima_visita']==1)
        row['AP2_10_1_2']='10';base={};ns['_external'](row,'A',base);check('denuncia:respuesta familiar no cuenta',base['externo_denuncia_ultima_visita']==0)
        row.update(AP2_6_2='2',AP2_10_2_1='01',AP2_12_2_1='1');base={};ns['_external'](row,'A',base);check('denuncia:resultado fuera de hecho positivo excluido',base['externo_denuncia_ultima_visita']==0)
        row['AP2_12_1_5']='1';base={};ns['_external'](row,'A',base);check('denuncia:columna5 no consumida',base['externo_denuncia_ultima_visita']==0)
        # Alternativa institucional se aplica adicionalmente solo para probar compatibilidad.
        proc=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(HERE/'institucion-afectadas-alternativa.patch')],cwd=directory,text=True,capture_output=True)
        check('instituciones:alternativa aplica sobre composicion',proc.returncode==0)
        alternate=functions((directory/'sucesor-2011/medidor.py').read_text(),['_binary','_union_binary','_freq','_partner_groups','_reason','_partner'])
        second={f'AP6_1_{i}':'4' for i in range(1,31)};second['AP6_1_1']='1';second.update({f'AP6_5_{i}':'2' for i in range(1,7)})
        before={};after={};ns['_partner']({},second,{},'A',before);alternate['_partner']({},second,{},'A',after)
        check('instituciones:estimandos distintos afectados sin ayuda',before['pareja_institucion_01'] is None and after['pareja_institucion_01']==0)
        for year,path in SOURCES.items():
            for name in ['medidor.py','spec.md']:check(f'{year}/{name}: original intacto',hashlib.sha256((path/name).read_bytes()).hexdigest()==hashes[f'{year}/{name}'])
    result={'modo':'COPIAS-TEMPORALES-FUNCIONES-AST-SINTETICOS','raw_leido':False,'productor_importado_o_run':False,'originales_sha256':hashes,'patches':applied,'casos':checks,'total_pass':len(checks),'limite':'Sinteticos verifican reglas y composicion; no estiman magnitudes raw ni firman universo nacional99/estimando institucional.'}
    (HERE/'comprobacion-patches.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'total_pass':len(checks),'patches':len(applied),'estado':'PASS'},ensure_ascii=False))
if __name__=='__main__':main()
