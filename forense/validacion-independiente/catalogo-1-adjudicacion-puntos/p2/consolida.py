"""Contrasta auxiliares con sellados y primer independiente, sin leer raw."""
import csv,json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;R=B.parents[3]
def read(p):return list(csv.DictReader(p.open(),delimiter='\t'))
def write(name,rows):
 with (B/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t');w.writeheader();w.writerows(rows)
def main():
 aux=read(B/'contrastes-raw2011-v3.tsv');by={(x['llave'],x['edad_corregida'],x['regla_corregida']):x for x in aux}
 sealed=json.loads(json.loads((R/'data/corrida0/CALC-ENDIREH-PISOS-2011-MODULOS-0001/resultados.json').read_text())['resultados']['RESULT-ENDIREH2011-MOD-TABLA'])
 independent=read(R/'forense/validacion-independiente/catalogo-1-ejecucion-lote1/reconstrucciones/endireh-pisos-2011-modulos-0001/endireh-pisos-2011-modulos-0001--reconstruccion.tsv')
 ind={x['llave']:x for x in independent};out=[]
 for k in sorted({x['llave'] for x in aux}):
  old=by[k,'0','0'];new=by[k,'1','1'];s=sealed[int(k.split('#')[1])]
  vals=[float(by[k,a,z]['punto']) if by[k,a,z]['punto'] else None for a,z in [('0','0'),('0','1'),('1','0'),('1','1')]]
  newp=float(new['punto']) if new['punto'] else None
  ip=ind[k].get('punto') or ind[k].get('estimacion') or ind[k].get('valor')
  delta=float(old['punto'])-s['p']
  out.append({'llave':k,'baseline_delta':delta,'baseline_n_coincide':int(old['n'])==s['n'],'baseline_p_coincide':abs(delta)<=1e-10,'n_propuesto':new['n'],'masa_propuesta':new['masa'],'punto_propuesto':new['punto'],'delta_nuevo_original':newp-s['p'] if newp is not None else '', 'interaccion_edad_regla':vals[3]-vals[2]-vals[1]+vals[0] if all(v is not None for v in vals) else '', 'punto_independiente_leido':ip or '', 'residual_independiente':newp-float(ip) if ip and newp is not None else '', 'limite':'denuncia regla combinada; factorial nacional separado' if old['conducta']=='externo_denuncia_ultima_visita' else 'interacción edad y regla; sin atribución causal'})
 write('cotejo-final2011.tsv',out)
 summary={'identidades2011':len(out),'baseline_discrepancias':sum(not x['baseline_p_coincide'] for x in out),'baseline_n_discrepancias':sum(not x['baseline_n_coincide'] for x in out),'interacciones_no_nulas':sum(x['interaccion_edad_regla']!='' and abs(x['interaccion_edad_regla'])>1e-10 for x in out),'residuales_independiente':sum(x['residual_independiente']!='' and abs(x['residual_independiente'])>1e-10 for x in out),'2021_agregados':len(read(B/'contrastes-raw2021-v4.tsv')),'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in B.iterdir() if p.is_file() and p.suffix in ['.py','.tsv','.md']}}
 (B/'c1-puntos-p2-final.json').write_text(json.dumps(summary,indent=2)+'\n');print({k:v for k,v in summary.items() if k!='hashes'})
if __name__=='__main__':main()
