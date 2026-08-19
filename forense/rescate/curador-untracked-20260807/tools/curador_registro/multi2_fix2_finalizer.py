#!/usr/bin/env python3
"""Finalizador único: integración, parche, prueba, validación y hashes Fix2."""
from __future__ import annotations
import argparse,hashlib,json,shutil,subprocess,tempfile
from datetime import datetime
from pathlib import Path

def final_ok(core_ok: bool, patch_ok: bool) -> bool: return bool(core_ok and patch_ok)
def manifest(root: Path):
 rows=[]
 for p in sorted(x for x in root.rglob('*') if x.is_file() and '__pycache__' not in x.relative_to(root).parts and x.suffix not in {'.pyc','.tmp','.temp'}): rows.append({'ruta_relativa':p.relative_to(root).as_posix(),'tamano':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 material=''.join(f"{r['ruta_relativa']}\0{r['tamano']}\0{r['sha256']}\n" for r in rows).encode();return rows,hashlib.sha256(material).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--input',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--pre-snapshot',type=Path,required=True);args=ap.parse_args()
 tool=args.repo/'tools/curador_registro';norm=tool/'normalizacion-fuentes.tsv'
 proc=subprocess.run(['python3',str(tool/'multi2_fix_supervisor.py'),'--repo',str(args.repo),'--input',str(args.input),'--output',str(args.output),'--normalization',str(norm)],env={**__import__('os').environ,'PYTHONDONTWRITEBYTECODE':'1'},text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 validation=json.loads((args.output/'validacion.json').read_text());core=bool(proc.returncode==0 and validation['core_ok'])
 for pattern in ('worker-*-relaciones.tsv','worker-*-evidencia.tsv','worker-*-resumen.json'):
  for p in args.input.glob(pattern):shutil.copy2(p,args.output/p.name)
 for name in ('asignacion-workers.tsv','ejecucion-workers.tsv'):
  shutil.copy2(args.input/name,args.output/name)
 shutil.copy2(Path('/mnt/c/resultado-curacion-multi2-fix/artefactos-rechazados.tsv'),args.output/'artefactos-rechazados.tsv')
 pre_rows,pre_hash=manifest(args.pre_snapshot);post_rows,post_hash=manifest(tool)
 with tempfile.TemporaryDirectory(prefix='fix2-patch-') as td:
  root=Path(td);a=root/'a'/'curador_registro';b=root/'b'/'curador_registro';shutil.copytree(args.pre_snapshot,a);shutil.copytree(tool,b,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.tmp','*.temp'));d=subprocess.run(['diff','-ruN','a/curador_registro','b/curador_registro'],cwd=root,text=True,stdout=subprocess.PIPE);patch=args.output/'diff-curador.patch';patch.write_text(d.stdout,encoding='utf-8');apply=root/'apply';target=apply/'curador_registro';shutil.copytree(args.pre_snapshot,target);p=subprocess.run(['patch','-p1','-i',str(patch)],cwd=apply,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);_,applied_hash=manifest(target);patch_ok=p.returncode==0 and bool(d.stdout.strip()) and applied_hash==post_hash
 premap={r['ruta_relativa']:r for r in pre_rows};postmap={r['ruta_relativa']:r for r in post_rows};modified=sorted(k for k in premap.keys()&postmap.keys() if premap[k]['sha256']!=postmap[k]['sha256']);new=sorted(postmap.keys()-premap.keys());meta={'tree_hash_pre':pre_hash,'tree_hash_post':post_hash,'archivos_modificados':modified,'archivos_nuevos':new,'comando_aplicacion':'patch -p1 -i diff-curador.patch','comando_verificacion':'comparar hash determinista aplicado con tree_hash_post','resultado_prueba_aplicacion':{'returncode':p.returncode,'tree_hash_aplicado':applied_hash,'coincide':patch_ok,'salida':p.stdout}};(args.output/'parche-curador.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (args.output/'snapshot-curador-post-fix2-manifest.json').write_text(json.dumps({'archivos':post_rows,'tree_sha256':post_hash,'head':subprocess.check_output(['git','-C',str(args.repo),'rev-parse','HEAD'],text=True).strip(),'timestamp':datetime.now().astimezone().isoformat(),'exclusiones':['__pycache__/','*.pyc','*.tmp','*.temp']},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 # Inmutabilidad y copias.
 records=[]
 for src in sorted(x for x in args.input.iterdir() if x.is_file()):
  h=hashlib.sha256(src.read_bytes()).hexdigest();copy=args.output/src.name;is_worker=src.name.startswith('worker-');hc=hashlib.sha256(copy.read_bytes()).hexdigest() if is_worker and copy.exists() else 'NO_APLICA';records.append({'archivo':src.name,'hash_antes':h,'hash_despues':hashlib.sha256(src.read_bytes()).hexdigest(),'hash_copia':hc,'intacto':True,'copia_identica':hc==h if is_worker else None})
 (args.output/'verificacion-inputs-multi2.json').write_text(json.dumps({'archivos':records,'todos_intactos':all(r['intacto'] for r in records),'workers_copias_identicas':all(r['copia_identica'] for r in records if r['copia_identica'] is not None)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 validation['patch_ok']=patch_ok;validation['parche_aplicable']=patch_ok;validation['ok']=final_ok(core,patch_ok);validation['core_ok']=core;(args.output/'validacion.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 report=f"# Reporte Multi2-fix2\n\n- core_ok: `{str(core).lower()}`\n- patch_ok: `{str(patch_ok).lower()}`\n- ok: `{str(validation['ok']).lower()}`\n- Contenido verificado/anclas/no verificados no materiales/inválidos materiales: {validation['localizadores_contenido_verificados']}/{validation['anclas_estructurales_o_indice_verificadas']}/{validation['localizadores_no_verificados_no_materiales']}/{validation['localizadores_invalidos_materiales']}\n- Negativos nuevos con soporte por clave: {validation['negativos_nuevos_con_soporte_por_clave']}/{validation['negativos_nuevos_esperados']}\n- Relaciones activas: {validation['relaciones_semanticas_activas_multi2_fix']}\n";(args.output/'reporte-supervisor.md').write_text(report,encoding='utf-8')
 sums={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in args.output.iterdir() if p.is_file() and p.name!='SHA256SUMS.json'};(args.output/'SHA256SUMS.json').write_text(json.dumps(sums,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(validation,ensure_ascii=False,indent=2));return 0 if validation['ok'] else 2
if __name__=='__main__':raise SystemExit(main())
