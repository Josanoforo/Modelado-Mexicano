"""Identidades de C1; ninguna cifra objetivo sale de los lectores CSV."""
import collections
import csv
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
csv.field_size_limit(10000000)


def read(rel):
    with (ROOT / rel).open() as source:
        return list(csv.DictReader((s for s in source if not s.startswith('#')), delimiter='\t'))


def write(name, fields, rows):
    with (OUT / name).open('w') as target:
        writer = csv.DictWriter(target, fieldnames=fields, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    source = ROOT / 'forense/validacion-independiente/catalogo-1/lotes.json'
    lotes = json.loads(source.read_text())
    old = {r['llave']: r for r in read('canon/catalogo-del-mexicano-v1_1.tsv')}
    current = {r['llave']: r for r in read('canon/catalogo-del-mexicano-v1_2.tsv')}
    incomplete = [r for r in lotes if r['estado_preparacion'] == 'INCOMPLETO']
    complete = [r for r in lotes if r['estado_preparacion'] == 'DISPONIBLE']
    assert len({r['calc'] for r in lotes}) == len(lotes)
    counts = collections.Counter(r['calc'] for r in old.values())
    now = collections.Counter(r['calc'] for r in current.values())
    assert set(counts) == {r['calc'] for r in lotes}
    assert all(counts[r['calc']] == r['estimadores'] for r in lotes)
    fields = ['paquete', 'calc', 'estimadores', 'filas_v1_1', 'filas_vigentes', 'estado_preparacion_original', 'sha256_original', 'sha256_contenedor_original', 'cohorte']
    rows = [dict(paquete=r['paquete'], calc=r['calc'], estimadores=r['estimadores'], filas_v1_1=counts[r['calc']], filas_vigentes=now[r['calc']], estado_preparacion_original=r['estado_preparacion'], sha256_original=r['sha256'], sha256_contenedor_original=r['sha256_contenedor'], cohorte='LOTE2' if r in incomplete else 'SESION01-FUERA') for r in lotes]
    write('correspondencia-59.tsv', fields, [r for r in rows if r['cohorte'] == 'LOTE2'])
    write('nueve-fuera.tsv', fields, [r for r in rows if r['cohorte'] != 'LOTE2'])
    delta = []
    for state, keys, data in [('NUEVO-FUERA-CORTE', current.keys()-old.keys(), current), ('RETIRADO', old.keys()-current.keys(), old)]:
        groups = collections.Counter(data[k]['calc'] for k in keys)
        delta += [dict(tipo=state, calc=c, filas=n, identidad='', campos='') for c,n in sorted(groups.items())]
    for k in sorted(old.keys() & current.keys()):
        changed = [f for f in old[k] if old[k][f] != current[k][f]]
        if changed:
            delta.append(dict(tipo='METADATO-MODIFICADO', calc=current[k]['calc'], filas=1, identidad=k, campos=';'.join(changed)))
    write('delta-catalogo.tsv', ['tipo', 'calc', 'filas', 'identidad', 'campos'], delta)
    groups = collections.Counter((r['calc'],r['causa'],r['firma'],r['nota']) for r in read('forense/analisis/catalogo/v1_2/excluidos-v1_2.tsv'))
    excluded = [dict(calc=c, causa=why, firma=fp, nota=note, filas=n, en_lote2=str(c in {r['calc'] for r in incomplete})) for (c,why,fp,note),n in sorted(groups.items())]
    write('vetados-sustituidos-excluidos.tsv', ['calc','causa','firma','nota','filas','en_lote2'], excluded)
    summary = dict(corte=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(), fuente_lotes_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), catalogo_original='v1.1', catalogo_vigente='v1.2', lote2_paquetes=len(incomplete), lote2_estimadores=sum(r['estimadores'] for r in incomplete), sesion01_paquetes=len(complete), sesion01_estimadores=sum(r['estimadores'] for r in complete), interseccion=0, nuevas_filas=len(current.keys()-old.keys()), retiradas=len(old.keys()-current.keys()), metadatos_modificados=sum(old[k]!=current[k] for k in old.keys()&current.keys()), exclusiones_en_lote2=sum(r['filas'] for r in excluded if r['en_lote2']=='True'), estado='PREPARACION-NO-CIEGA; progreso final se une al manifiesto sucesor por calc, sin reemplazar identidades originales')
    (OUT/'p4-cohorte-resumen.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == '__main__':
    main()
