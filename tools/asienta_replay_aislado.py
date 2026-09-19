#!/usr/bin/env python3
"""Asienta, sin reejecutar, la evidencia aislada ya conservada por este acto."""
import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'forense/evidencia-replay-aislado-2026-09-19.json'
TSV=ROOT/'forense/replay-evidencia.tsv'
HEAD=['calc_id','corrida_id','resultado_replay','contexto_replay','razones','spec_yaml_sha256','script_blob_sha256','input_sha256_efectivos','codigo_commit','fecha_verificacion','entorno','procedencia','alcance','nota']

def main():
    with TSV.open(encoding='utf-8',newline='') as f: old=list(csv.DictReader(f,delimiter='\t'))
    if not old or list(old[0]) != HEAD: raise SystemExit('esquema replay-evidencia.tsv inesperado')
    seen={(r['calc_id'],r['spec_yaml_sha256'],r['script_blob_sha256'],r['fecha_verificacion']) for r in old}
    new=[]
    for x in json.loads(ART.read_text(encoding='utf-8')):
        calc=x['calc_id']; ej=ROOT/'data/corrida0'/calc/'ejecucion.json'
        if not ej.exists(): raise SystemExit(f'{calc}: ejecucion.json ausente')
        e=json.loads(ej.read_text(encoding='utf-8')); ident=x['identidad']
        for k in ('spec_yaml_sha256','script_blob_sha256'):
            if str(e.get(k,'')) != str(ident[k]): raise SystemExit(f'{calc}: identidad {k} no coincide')
        efectivo=','.join(f'{k}={v}' for k,v in sorted((e.get('input_sha256') or {}).items()))
        if efectivo != ident['input_sha256_efectivos']:
            raise SystemExit(f'{calc}: identidad input_sha256_efectivos no coincide')
        key=(calc,ident['spec_yaml_sha256'],ident['script_blob_sha256'],x['fecha_verificacion'])
        if key in seen: continue
        d=x.get('detalle_verify',{}); razones='; '.join(d.get('razones_contexto') or d.get('problemas_replay') or []) or 'verify aislado; ver salida cruda'
        alcance='NC-0313: discrepancia G-R-EXISTE-AL-CERRAR; C2 puntos/IC sin cambio' if calc=='CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001' else 'REPLAY-ASIENTOS; sin inferencia adicional'
        new.append({'calc_id':calc,'corrida_id':e.get('corrida_id',''),'resultado_replay':x['resultado_replay'],'contexto_replay':x['contexto_replay'],'razones':razones,'spec_yaml_sha256':ident['spec_yaml_sha256'],'script_blob_sha256':ident['script_blob_sha256'],'input_sha256_efectivos':ident['input_sha256_efectivos'],'codigo_commit':e.get('git_commit','DESCONOCIDO'),'fecha_verificacion':x['fecha_verificacion'],'entorno':'CAJA (Ubuntu/WSL2) con corpus montado','procedencia':'VERIFY-AISLADO · GEN2-REPLAY-Y-PISOS-CLI-1','alcance':alcance,'nota':'forense/evidencia-replay-aislado-2026-09-19.json; un veredicto de replay no se publica sin asiento en la fuente; verify que imprime y no asienta es media verificación.'})
    with TSV.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=HEAD,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(old+new)
    print(f'asientos_nuevos={len(new)}')
if __name__=='__main__': main()
