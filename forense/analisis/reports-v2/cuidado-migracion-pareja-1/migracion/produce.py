"""Deriva tablas desde juicios explícitos; valida errores materiales, sin dictaminar."""
import argparse
import copy
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
REPORT = ROOT / 'corpus/reports-v2/Psychology_of_Mexico-US_Migration__Identity__Family__Aspiration__and_Wellbeing_in_2025.md'
ORIGINAL = ROOT / 'corpus/reports' / REPORT.name
DEN = 'hogares receptores con remesas>0 e ingreso corriente válido>0; ponderador factor de hogar; ENIGH2020'

def read_tsv(path):
    with path.open() as stream:
        return list(csv.DictReader(stream, delimiter='\t'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate(decisions, figures):
    ids = [x['id'] for x in decisions]
    assert len(ids) == len(set(ids)), 'identidad duplicada'
    live_map = [x for x in read_tsv(ROOT / 'canon/mapa-dominios-v1_1.tsv') if x['report'].endswith(REPORT.name)]
    covered = [key for x in decisions for key in x['mapa_ids']]
    assert set(covered) == {x['id_afirmacion'] for x in live_map}, 'cobertura faltante o ajena'
    assert all(x['dictamen'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'} for x in decisions)
    assert all(x['juicio'] and x['revision_manual'] for x in decisions), 'juicio ausente'
    assert all(x['razon_sin_cifra'] for x in decisions if x['dictamen']=='SIN-CIFRA')
    assert all(x['evidencia'] for x in decisions if x['dictamen']=='ROMPE'), 'refutación sin evidencia'
    catalogue = {x['result_id']:x for x in read_tsv(ROOT / 'canon/catalogo-del-mexicano-v1_2.tsv')}
    adoption = read_tsv(ROOT / 'data/corrida0/decisiones.tsv')
    effects = read_tsv(ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1/efectos-discrepancias.tsv')
    for f in figures:
        assert f['result_id'] in catalogue, 'cifra sin catálogo'
        current = catalogue[f['result_id']]
        assert current['estado_adopcion']=='ADOPTADO', 'cifra no adoptada'
        assert f['denominador']==DEN, 'denominador incorrecto'
        assert any(x['objeto']==f['calc'] and 'cuenta_gen2=SI' in x['decision'] for x in adoption), 'sin acto de adopción'
        calc = ROOT / 'data/corrida0' / f['calc']
        seal = json.loads((calc/'sello.json').read_text())
        assert sha(calc/'resultados.json')==seal['resultados.json'], 'hash RESULT roto'
        obj = json.loads((calc/'resultados.json').read_text())['resultados']
        assert float(f['punto'])==obj[f['result_id']]==float(current['punto']), 'valor alterado'
        assert float(f['ic95_inf'])==obj[f['result_id']+'-IC-LO'], 'IC alterado'
        assert float(f['ic95_sup'])==obj[f['result_id']+'-IC-HI'], 'IC alterado'
        assert not any(f['result_id'] in str(x) or f['calc'] in str(x) for x in effects), 'C1 requiere adjudicación'
        assert not any(word in current['estado_adopcion'].upper() for word in ['VETADO','RETIRADO']), 'veto'
    text=REPORT.read_text()
    allowed={'Y1','U1','I1','K1','R1'}
    assert all(set(x['evidencia']) <= allowed for x in decisions), 'fuente sin registro'
    # Porciones cuantitativas explícitas: fuera de bloque solo tasa jurídica externa.
    import re
    without = text.split('<!-- CIFRAS:INICIO -->')[0]+text.split('<!-- CIFRAS:FIN -->')[1]
    assert not re.search(r'\d+(?:[.,]\d+)?\s*(?:%|millones|mdd|USD)', without), 'cantidad no contratada en narrativa'
    return live_map

def products(decisions, figures):
    table=['| ID | Dictamen | Cambio y evidencia |','|---|---|---|']
    for d in decisions:
        table.append('| '+d['id']+' | '+d['dictamen']+(' · '+d['razon_sin_cifra'] if d['razon_sin_cifra'] else '')+' | '+d['juicio'].replace('|','/')+' ['+', '.join(d['evidencia'])+'] |')
    f=figures[0]
    block='\n\n| RESULT y estado | Estimación histórica | Denominador y alcance |\n|---|---|---|\n'
    block+=f"| `{f['result_id']}` · ADOPTADO Firma M; validación independiente pendiente | {float(f['punto'])*100:.2f}% (IC95 {float(f['ic95_inf'])*100:.2f}–{float(f['ic95_sup'])*100:.2f}%) de hogares con remesas equivalentes al menos a la mitad del ingreso corriente | {DEN}; no todos los hogares mexicanos, personas migrantes ni gasto; bootstrap UPM dentro de estrato |\n\n"
    text=REPORT.read_text(); before=text.split('<!-- CIFRAS:INICIO -->')[0];after=text.split('<!-- CIFRAS:FIN -->')[1]
    report=before+'<!-- CIFRAS:INICIO -->'+block+'<!-- CIFRAS:FIN -->'+after
    rows=[]
    for d in decisions:
        rows.append({**d,'mapa_ids':';'.join(d['mapa_ids']),'evidencia':';'.join(d['evidencia'])})
    import io
    stream=io.StringIO(); writer=csv.DictWriter(stream,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');writer.writeheader();writer.writerows(rows)
    out={HERE/'afirmaciones.tsv':stream.getvalue(),HERE/'tabla-afirmaciones.md':'\n'.join(table)+'\n',REPORT:report}
    summary={'report':str(REPORT.relative_to(ROOT)),'registros':len(decisions),'mapa_filas':42,'dictamenes':dict(Counter(d['dictamen'] for d in decisions)),'cifras':len(figures),'fuentes_leidas':4,'comando_generar':['python3',str(Path(__file__).relative_to(ROOT))],'comando_verificar':['python3',str(Path(__file__).relative_to(ROOT)),'--check'],'self_test':['python3',str(Path(__file__).relative_to(ROOT)),'--self-test']}
    out[HERE/'resumen.json']=json.dumps(summary,ensure_ascii=False,indent=2)+'\n'
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    decisions=json.loads((HERE/'decisiones.json').read_text()); figures=json.loads((HERE/'cifras.json').read_text());validate(decisions,figures)
    if args.self_test:
        cases=[]
        first_map=decisions[0]['mapa_ids'][0]
        missing=[d for d in decisions if first_map not in d['mapa_ids']];cases.append((missing,figures))
        broken=copy.deepcopy(figures);broken[0]['punto']='0.99';cases.append((decisions,broken))
        wrong=copy.deepcopy(figures);wrong[0]['denominador']='todos los mexicanos';cases.append((decisions,wrong))
        fake=copy.deepcopy(figures);fake[0]['result_id']='RESULT-SIN-RESPALDO';cases.append((decisions,fake))
        for ds,fs in cases:
            try:validate(ds,fs)
            except AssertionError:continue
            raise AssertionError('mutación material aceptada')
        print('PASS: cuatro mutaciones materiales rechazadas');return
    for path,content in products(decisions,figures).items():
        if args.check:assert path.exists() and path.read_text()==content, f'derivado atrasado: {path}'
        else:path.write_text(content)
    print('PASS: cobertura, juicios, adopción, sello, denominador, C1 y tablas')

if __name__=='__main__':main()
