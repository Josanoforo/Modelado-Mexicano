"""Extrae exclusivamente semántica por llave exacta; nunca estima ni abre productor."""
from pathlib import Path
import csv, io, subprocess, hashlib, tarfile, collections, json, re

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
EVIDENCIA = 'df54ad05258ea36c77b9efda44a839e250174d1a'
CAT = 'canon/catalogo-del-mexicano-v1_2.tsv'
TAB = 'forense/validacion-independiente/catalogo-1-incertidumbre-spec/p3/identidades-799.tsv'
def git(path):
    return subprocess.check_output(['git', 'show', EVIDENCIA+':'+path], cwd=ROOT)
def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode()), delimiter='\t'))
def sha(data):
    return hashlib.sha256(data).hexdigest()

# El lector proyecta solamente columnas semánticas. Ningún valor pasa al mapa.
catbytes = (ROOT/CAT).read_bytes()
catcommit = subprocess.check_output(['git','log','-1','--format=%H','--',CAT],cwd=ROOT,text=True).strip()
fields = ['llave','conducta','eje','segmento','calc','reserva','firma_fp']
catalogo = [{k:r[k] for k in fields} for r in rows(catbytes)]
assert len(catalogo)==len({r['llave'] for r in catalogo})
catalogo = {r['llave']:r for r in catalogo}
tablebytes = git(TAB)
source = [r for r in rows(tablebytes) if r['clase_sucesor']=='RESTAURACION-DE-TRANSPORTE-DOCUMENTADA']
assert len(source)==767
packages = {r['paquete'] for r in source}
packages.add('endireh-pisos-2016-pareja-fisica-0002')
mapped=[]
excluded=[]
hashes=[]
for package in sorted(packages):
    base = ROOT/'forense/validacion-independiente'
    if '2016' in package:
        archive=base/'catalogo-1-preparacion-lote2'/'entradas'/package/(package+'-entradas-v2.tar.gz')
    else:
        archive=base/'catalogo-1'/'paquetes'/package/(package+'-entradas.tar.gz')
    with tarfile.open(archive) as t:
        original=rows(t.extractfile('estimandos.tsv').read())
    assert len(original)==len({r['llave'] for r in original})
    selected={r['llave']:r for r in source if r['paquete']==package}
    if '2016' in package:
        selected={r['llave']:{'ventana_demostrada':re.search(r'ventana=([^;]+)',catalogo[r['llave']]['reserva']).group(1)} for r in original}
    assert set(selected)<=set(r['llave'] for r in original)
    for old in original:
        key=old['llave']
        if key not in selected:
            excluded.append(dict(llave=key,paquete=package,estado='FUERA-DE-767-OMISIONES'))
            continue
        published=catalogo[key]
        assert all(old[k]==published[k] for k in ['conducta','eje','segmento','calc'])
        match=re.search(r'(?:^|;\s*)ventana=([^;]+)',published['reserva'])
        assert match
        window=match.group(1)
        assert window==selected[key]['ventana_demostrada']
        method='13.1/13.3' if '2016' in package else ('14.1/14.3' if 'nofisica' in package else {'comunitaria':'9.1/9.3','escolar':'7.6/7.8','laboral':'8.9/8.11'}[package.split('-2021-')[1].split('-0001')[0]])
        text = 'De octubre de 2015 a la fecha' if window=='desde_octubre_2015' else ('De octubre de 2020 a la fecha' if window=='desde_octubre_2020' else ('Desde que inició la relación' if window=='vida_relacion' or '2016' in package else ('Durante su vida de estudiante' if 'escolar' in package else ('Dígame si en alguno de sus trabajos' if 'laboral' in package else '¿Alguna vez…'))))
        mapped.append(dict(llave=key,paquete=package,ventana=window,estado='DEMOSTRADA-PUBLICADA',conducta=old['conducta'],eje=old['eje'],segmento=old['segmento'],columna='reserva',texto_literal=published['reserva'],fuente=CAT,fuente_commit=catcommit,fuente_sha256=sha(catbytes),firma_fp=published['firma_fp'],cuestionario_reactivos=method,cuestionario_texto_literal_fragmento=text,autoridad='significado publicado firmado; no spec independiente anterior al productor'))
    hashes.append(dict(paquete=package,ruta=str(archive.relative_to(ROOT)),sha256=sha(archive.read_bytes()),identidades_originales=len(original),identidades_mapeadas=len(selected)))
assert len(mapped)==859 and len({r['llave'] for r in mapped})==859
assert collections.Counter(r['ventana'] for r in mapped if '2016' in r['paquete'])=={'vida':46,'desde_octubre_2015':46}
paired = collections.defaultdict(set)
for r in mapped:
    if '2016' in r['paquete']:
        paired[(r['eje'],r['segmento'])].add(r['ventana'])
assert len(paired)==46 and all(v=={'vida','desde_octubre_2015'} for v in paired.values())
for name,data in [('mapa-ventanas.tsv',mapped),('excluidas-historico.tsv',excluded)]:
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(data[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(data)
metadata=dict(corte=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),evidencia_1194=EVIDENCIA,tabla_1194_sha256=sha(tablebytes),catalogo_sha256=sha(catbytes),catalogo_columna='reserva',paquetes=hashes,filas=len(mapped),llaves_distintas=len({r['llave'] for r in mapped}),excluidas=len(excluded),conteos={p:dict(collections.Counter(r['ventana'] for r in mapped if r['paquete']==p)) for p in sorted(packages)})
(OUT/'mapa-resumen.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(metadata['conteos'],ensure_ascii=False))
