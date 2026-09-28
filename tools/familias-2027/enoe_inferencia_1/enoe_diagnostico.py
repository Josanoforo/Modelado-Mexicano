"""Auditoría agregada del mismo oro; ninguna selección de método por potencia."""
import argparse, csv, hashlib, importlib.util, io, json, zipfile, math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HIST = ROOT/'forense/analisis/familias-2027-frontera-1/paquetes/ENOE-INFORMALIDAD'
spec = importlib.util.spec_from_file_location('enoe_original', HIST/'enoe_lector.py')
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)

def auditar(rows):
    marcos = {k: defaultdict(set) for k in ('todas','entrevistadas','edad','ocupados','SEX1','SEX2')}
    conteos = defaultdict(int)
    entidades = defaultdict(set); areas = defaultdict(set); upm_ent = defaultdict(set); upm_est=defaultdict(set)
    for r in rows:
        est, upm = r['EST_D_TRI'].strip(), r['UPM'].strip()
        entidades[est].add(r['ENT']); areas[est].add(r['CD_A']); upm_ent[upm].add(r['ENT'])
        upm_est[upm].add(est)
        marcos['todas'][est].add(upm); conteos['todas'] += 1
        if r['R_DEF'].strip() not in {'0','00'} or r['C_RES'] not in {'1','3'}: continue
        marcos['entrevistadas'][est].add(upm); conteos['entrevistadas'] += 1
        if not 15 <= int(r['EDA']) <= 98: continue
        marcos['edad'][est].add(upm); conteos['edad'] += 1
        if r['CLASE2'] != '1': continue
        marcos['ocupados'][est].add(upm); conteos['ocupados'] += 1
        if r['EMP_PPAL'].strip() not in {'1','2'}: continue
        g = 'SEX'+r['SEX']; marcos[g][est].add(upm); conteos[g] += 1
    marco = marcos['entrevistadas']
    detalle = []
    for est, upms in sorted(marco.items()):
        if len(upms) != 1: continue
        detalle.append({'estrato': est, 'entidades_distintas':len(entidades[est]), 'areas_distintas':len(areas[est]),
                        **{'upm_'+k:len(v.get(est,set())) for k,v in marcos.items()},
                        'singleton_creado_por_filtro_entrevista':len(marcos['todas'][est])>1})
    resumen = {}
    for k,v in marcos.items():
        resumen[k] = {'filas':conteos[k],'estratos':len(v),'upm':sum(map(len,v.values())),
                      'singleton':sum(len(s)==1 for s in v.values()),
                      'upm_cero_dominio':sum(len(s-marcos[k].get(e,set())) for e,s in marco.items())}
    return {'marcos':resumen,'singleton_union':len(detalle),'singleton_detalle':detalle,
            'colisiones':{'estratos_en_multiples_entidades':sum(len(s)>1 for s in entidades.values()),
                          'estratos_en_multiples_areas':sum(len(s)>1 for s in areas.values()),
                          'upm_en_multiples_entidades':sum(len(s)>1 for s in upm_ent.values()),
                          'upm_en_multiples_estratos':sum(len(s)>1 for s in upm_est.values())}}

def ejecutar(path):
    import yaml
    entradas=[e for e in yaml.safe_load((ROOT/'data/manifiesto.yaml').read_text()) if e['id']=='enoe_2024_4t_microdatos']
    if len(entradas)!=1 or entradas[0].get('estado_reserva') or entradas[0].get('retirada'): raise ValueError('ACCESO')
    if entradas[0]['sha256'] != original.SHA_ORO: raise ValueError('MANIFIESTO')
    payload=Path(path).read_bytes()
    if hashlib.sha256(payload).hexdigest()!=original.SHA_ORO: raise ValueError('IDENTIDAD ORO')
    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        reader=csv.DictReader(io.TextIOWrapper(z.open('ENOE_SDEMT424.csv'),encoding='latin1'))
        necesarios=original.CAMPOS|{'CD_A'}
        rows=[{k.upper():v for k,v in r.items() if k.upper() in necesarios} for r in reader]
        grupos=original.medir(iter(rows),set(rows[0]))
        auditoria=auditar(rows)
        marco=defaultdict(set)
        for r in rows:
            if r['R_DEF'].strip() in {'0','00'} and r['C_RES'] in {'1','3'}:
                marco[(r['ENT'],r['EST_D_TRI'])].add(r['UPM'])
        historico=json.loads((HIST/'enoe-oro.json').read_text())['grupos']
        for sexo,g in grupos.items():
            for campo in ('p0','numerador_ponderado','denominador_ponderado'):
                if g[campo]!=historico[sexo][campo]: raise ValueError('PUNTO HISTORICO CAMBIO: '+campo)
            clusters={est:dict.fromkeys(upms,0.) for est,upms in marco.items()}
            for r in rows:
                if r['R_DEF'].strip() not in {'0','00'} or r['C_RES'] not in {'1','3'}: continue
                if not 15<=int(r['EDA'])<=98 or r['CLASE2']!='1' or r['SEX']!=sexo: continue
                if r['EMP_PPAL'].strip() not in {'1','2'}: continue
                clusters[(r['ENT'],r['EST_D_TRI'])][r['UPM']]+=float(r['FAC_TRI'])*((r['EMP_PPAL'].strip()=='1')-g['p0'])/g['denominador_ponderado']
            parcial=0.;singleton_no_cero=0
            for pp in clusters.values():
                if len(pp)==1:
                    singleton_no_cero+=next(iter(pp.values()))!=0
                    continue
                media=sum(pp.values())/len(pp)
                parcial+=len(pp)/(len(pp)-1)*sum((v-media)**2 for v in pp.values())
            g['varianza_parcial_no_utilizable_como_total']=parcial
            g['singleton_residuo_no_cero']=singleton_no_cero
            g['clave_compuesta_equivalente_a_historica']=auditoria['colisiones']['estratos_en_multiples_entidades']==0
            n=auditoria['singleton_union']
            g['razon_bloqueo']=f'{n} estratos singleton presentes en todas las filas del oro; no son producto del filtro de dominio. La fórmula oficial m/(m-1) no identifica sus componentes.'
            g['insumo_faltante']=f'Instrucción oficial aplicable a ENOE2024T4 para los {n} estratos, con indicador de certeza y probabilidades de inclusión (si corresponde, incluidas etapas inferiores) o estructura oficial de colapso/réplicas que identifique sus componentes de varianza; además, crosswalk oficial para los códigos UPM que reaparecen en estratos distintos y definición de unidad primaria física; no basta FAC_TRI.'
            g['p0_historico_preservado']=True
    return {'estado':'DIAGNOSTICO-HISTORICO-ABIERTO','id':'enoe_2024_4t_microdatos','archivo_sha256':original.SHA_ORO,
            'grupos':grupos,**auditoria}

def varianza_clusters(clusters, certeza=()):
    """Sintético de una etapa: certeza explícita no resuelve etapas inferiores reales."""
    var=0.
    for est,pp in clusters.items():
        m=len(pp)
        if m==1:
            if est not in certeza: return None
            continue
        if m<1: raise ValueError('MARCO VACIO')
        media=sum(pp.values())/m
        var+=m/(m-1)*sum((v-media)**2 for v in pp.values())
    return var

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--oro',required=True); ap.add_argument('--salida',required=True); a=ap.parse_args()
    Path(a.salida).write_text(json.dumps(ejecutar(a.oro),indent=2,allow_nan=False)+'\n')
