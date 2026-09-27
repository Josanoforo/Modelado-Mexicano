#!/usr/bin/env python3
"""Deriva presentación y conteos; nunca adjudica juicios editoriales."""
import argparse, collections, csv, hashlib, io, json, pathlib, re
B=pathlib.Path(__file__).resolve().parent
ROOT=B.parents[4]
REPORT=ROOT/'corpus/reports-v2/El_Clasemediero_Mexicano__Identidad__Ansiedad_de_Estatus_y_el_Miedo_Racional_a_Caer.md'
def read(n): return json.loads((B/n).read_text())
def validate(rows,evidence,text):
    actual=list(csv.DictReader((ROOT/'canon/mapa-dominios-v1_1.tsv').open(),delimiter='\t'))
    wanted={r['id_afirmacion'] for r in actual if r['report']=='corpus/reports/El_Clasemediero_Mexicano__Identidad__Ansiedad_de_Estatus_y_el_Miedo_Racional_a_Caer.md'}
    assert wanted=={r['id'] for r in rows if r['origen']=='mapa'}, 'cobertura mapa'
    assert len({r['id'] for r in rows})==len(rows)
    for r in rows:
        assert r['dictamen'] in {'CONFIRMA','MATIZA','ROMPE','SIN-CIFRA'}
        assert r['razon'] and r['evidencia'] and 'pendiente' in r['estatus_juicio']
        if r['dictamen']=='CONFIRMA': assert r['evidencia'] in {x['id'] for x in evidence}
    for e in evidence:
        p=ROOT/'data/corrida0'/e['calc']; seal=json.loads((p/'sello.json').read_text())
        assert hashlib.sha256((p/'resultados.json').read_bytes()).hexdigest()==e['hash']==seal['resultados.json'], 'sello'
        assert json.loads((p/'resultados.json').read_text())['resultados'][e['id']]==e['valor'],'valor'
        assert e['denominador']=='hogares ENIGH 2022 con NSE válido','denominador incompatible'
        assert e['ola']=='2022' and e['estado']=='ADOPTADO-CON-RESERVA-INSTRUMENTO','veto/estado'
        with (ROOT/'forense/firmas-pendientes.tsv').open() as f:
            fp=next(r for r in csv.DictReader(f,delimiter='\t') if r['id']==e['firma'])
        assert fp['estado']=='FIRMADA' and 'ENIGH 2022' in fp['firmada_en'],'firma'
    # Las cantidades externas declaradas son las únicas porcentuales del cuerpo editorial.
    q=re.findall(r'\*\*(\d+(?:\.\d+)?)%\*\*',text)
    assert collections.Counter(map(float,q))==collections.Counter(float(x['valor']) for x in read('cifras.json')),'cifra sin evidencia'
    assert not re.search(r'(?<!\*)\b\d+(?:\.\d+)?\s*%',text.replace('**50%**','').replace('**2%**','')), 'cifra porcentual no declarada'
    assert 'ENIGH2024_RR' not in text and '0.391' not in text, 'evidencia reservada'
def outputs():
    rows=read('editorial.json'); evidence=read('evidencia.json'); text=(B/'report.editorial.md').read_text()
    validate(rows,evidence,text)
    dist='| NSE | % hogares | RESULT / registro |\n|---|---:|---|\n'+''.join(f"| {e['id'].split('-DIST-')[1][:-2]} | {100*e['valor']:.1f} | `{e['id']}` |\n" for e in evidence)
    report=text.replace('<!-- DISTRIBUCION -->',dist)
    out=io.StringIO();w=csv.DictWriter(out,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
    counts=dict(collections.Counter(r['dictamen'] for r in rows if r['origen']!='clausula-hija'))
    summary=dict(pieza='clase',report=str(REPORT.relative_to(ROOT)),decisiones=str((B/'editorial.json').relative_to(ROOT)),cifras=str((B/'cifras.json').relative_to(ROOT)),reglas=str((B/'reglas.json').relative_to(ROOT)),comando_verificar=['python3',str((B/'productor.py').relative_to(ROOT)),'--verificar'],comando_producir=['python3',str((B/'productor.py').relative_to(ROOT))],conteos=counts,mapa=len([r for r in rows if r['origen']=='mapa']),fuera_mapa=len([r for r in rows if r['origen']=='fuera-del-mapa']),clausulas_hijas=len([r for r in rows if r['origen']=='clausula-hija']),revision_humana='SOLICITADA-NO-CONCEDIDA')
    return {REPORT:report,B/'afirmaciones.tsv':out.getvalue(),B/'resumen.json':json.dumps(summary,ensure_ascii=False,indent=2)+'\n'}
def selftest():
    rows=read('editorial.json'); es=read('evidencia.json');t=(B/'report.editorial.md').read_text()
    attacks=[(rows,es,t+'\n93% de hogares.\n'),(rows,[dict(es[0],denominador='personas')]+es[1:],t),(rows[1:],es,t),(rows,[dict(es[0],estado='VETADO')]+es[1:],t)]
    for r,e,x in attacks:
        try:validate(r,e,x)
        except AssertionError:continue
        raise AssertionError('mutación material no detectada')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--verificar',action='store_true');a.add_argument('--autoprueba',action='store_true');opts=a.parse_args()
    if opts.autoprueba:selftest()
    for p,content in outputs().items():
        if opts.verificar: assert p.read_text()==content,f'diferencia {p}'
        else:p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
    print('VERDE: cobertura, juicios explícitos, identidades selladas, firma, denominador, cifras y regeneración'+ ('; mutaciones detectadas' if opts.autoprueba else ''))
