"""Cuenta identidades y resume integridad documental; no ejecuta estimadores ni valida contratos."""
from pathlib import Path
import csv, collections, hashlib, json
p=Path(__file__).resolve().parent
with (p/'identidades-799.tsv').open() as f: historic=list(csv.DictReader(f, delimiter='\t'))
with (p/'entradas/identidades-nuevas.tsv').open() as f: fresh=list(csv.DictReader(f, delimiter='\t'))
report={'llaves_historicas':len(historic), 'llaves_distintas':len({x['llave'] for x in historic}), 'clases':dict(collections.Counter(x['clase_sucesor'] for x in historic)), 'ventanas_transporte':dict(collections.Counter(x['ventana_demostrada'] for x in historic if x['clase_sucesor']=='RESTAURACION-DE-TRANSPORTE-DOCUMENTADA')), 'identidades_nuevas':len(fresh), 'identidades_nuevas_distintas':len({x['identidad_nueva'] for x in fresh}), 'fuentes_fechadas':sum(bool(x['fuente_fechada']) for x in historic), 'archivos_entrada':{str(f.relative_to(p)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((p/'entradas').rglob('*')) if f.is_file()}}
print(json.dumps(report, ensure_ascii=False, indent=2))
