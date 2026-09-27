"""Deriva ejes históricos, sin nuevos contrastes ni ejecución del protocolo."""
import csv,json,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
BASE=ROOT/'forense/validacion-independiente/catalogo-1-ejecucion-lote1'

def read(n):
    with (BASE/n).open() as f:return list(csv.DictReader(f,delimiter='\t'))
rows=[r for r in read('tabla-estimadores.tsv') if r['estado_punto']=='COINCIDE' and r['estado_ic']=='DISCREPA']
assert len(rows)==1873 and len({r['llave'] for r in rows})==1873
fx={r['llave']:r for r in read('efectos-discrepancias.tsv')}
replays={r['paquete']:r for r in json.loads((BASE/'replay-reconstrucciones.json').read_text())}
output=[]
for r in rows:
    package=r['paquete']; f=fx[r['llave']]
    if '2011' in package:
        cls='MARCO-DIFERENTE-DOCUMENTADO';why='TViviend 16910 UPM frente a mujeres admitidas; 20 UPM sin mujeres de módulos'
    elif 'nofisica' in package:
        cls='MARCO-DIFERENTE-EN-REGLA';why='Reconstrucción XIV completo incluido C2; productor admite A1/A2/B1/B2/C1 y excluye C2; efecto efectivo requiere cotejo por UPM'
    else:
        cls='RNG-Y-ORDEN-DIFERENTES-MARCO-NO-COTEJADO';why='Ambos preservan ceros del dominio; marco módulo antes de filtros frente a filas admitidas; misma ley no acreditada por llave'
    output.append(dict(llave=r['llave'],paquete=package,estado_punto=r['estado_punto'],estado_ic_historico=r['estado_ic'],tolerancia_historica_abs='1e-10',dictamen_ic=cls,delta_ic95_inf=f['delta_ic95_inf'],delta_ic95_sup=f['delta_ic95_sup'],mecanismo=why,efecto='incertidumbre; cambio de conclusión no acreditado',equivalencia_inferencial='NO-ACREDITADA',protocolo_nuevo='PROPUESTO; NO-CORRIDO sobre históricos',replay_congelado_preexistente=str(replays[package]['identico']).lower(),fuente_productor='data/corrida0/'+r['calc']+'/medidor.py',fuente_reconstruccion='forense/validacion-independiente/catalogo-1-ejecucion-lote1/reconstrucciones/'+package,fuente_comparacion='forense/validacion-independiente/catalogo-1-ejecucion-lote1/comparaciones/'+package+'--comparacion.json'))
with (OUT/'evidencia-ic.tsv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(output[0]),delimiter='\t');w.writeheader();w.writerows(output)
summary={'alcance':'NO CIEGO; sin nuevos contrastes históricos','filas_ic':len(output),'por_paquete':dict(Counter(r['paquete'] for r in output)),'dictamen':dict(Counter(r['dictamen_ic'] for r in output)),'pruebas_sinteticas':14,'historico_modificado':False,'replays':'9/9 idénticos LEÍDO; no repetidos en este acto','evidencia_sha256':hashlib.sha256((OUT/'evidencia-ic.tsv').read_bytes()).hexdigest()}
(OUT/'astra6-c1-p1-ic-resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
# Fragments of source code are archived locally for review, with original line numbers.
inventory=[]
for package in replays:
    calc='CALC-'+package.upper();producer=ROOT/'data/corrida0'/calc/'medidor.py'
    reconstruction=list((BASE/'reconstrucciones'/package).rglob('*reconstruir.py'))
    reconstruction=[p for p in reconstruction if 'test_' not in p.name]
    record={'paquete':package,'productor':str(producer.relative_to(ROOT)),'reconstruccion':str(reconstruction[0].relative_to(ROOT)),'fuentes':[]}
    for p in [producer,reconstruction[0]]:
        lines=p.read_text().splitlines()
        relevant=[{'linea':i+1,'texto':l} for i,l in enumerate(lines) if any(t in l for t in ['clusters =','strata','rng','integers','choice','quantile','FAC_MUJ','FAC_PER','singleton','TViviend','psus =','pairs=','frame =','SEED',' B =','B =','REPLICAS','T_INSTRUM'])]
        record['fuentes'].append({'ruta':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'extractos':relevant})
    inventory.append(record)
(OUT/'algoritmos-fuentes.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False))
