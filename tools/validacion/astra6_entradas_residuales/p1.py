"""Deriva únicamente las insuficiencias y discrepancias documentadas en #1202."""
import csv
import hashlib
import json
import tarfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'forense/validacion-independiente/catalogo-1-entradas-residuales-lote2/p1'
SOURCE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote2/lote2-tabla-estimadores.tsv'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_tsv(name, rows):
    with (OUT / name).open('w') as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    enriched = {}
    existing = OUT / 'tabla-llave-componente.tsv'
    if existing.exists():
        enriched = {(r['llave'], r['componente']): r for r in csv.DictReader(existing.open(), delimiter='\t')}
    rows = list(csv.DictReader(SOURCE.open(), delimiter='\t'))
    historical = {}
    dictamen_folder = SOURCE.parent / 'p3/dictamenes'
    for f in sorted(dictamen_folder.glob('*.json'), key=lambda p: ('-v2.' in p.name, p.name)):
        d = json.loads(f.read_text())
        for result in d.get('resultados', []):
            historical[result['llave']] = (f, d, result)
    residuals, discrepancies, inputs = [], [], {}
    for r in rows:
        for component in ['punto', 'ic']:
            state = r['estado_' + component]
            if state == 'DISCREPA':
                f, d, result = historical[r['llave']]
                discrepancies.append({**r, 'componente': component,
                                      'dictamen_ruta': str(f.relative_to(ROOT)),
                                      'dictamen_sha256': sha(f.read_bytes()),
                                      'campos_delta_json': json.dumps(result['campos'], sort_keys=True),
                                      'tolerancia_json': json.dumps(d.get('tolerancia'), sort_keys=True),
                                      'interpretacion_sucesora': 'PRESERVADO-SIN-RECLASIFICACION'})
            if state != 'NO-RECALCULABLE-DESDE-SPEC':
                continue
            package = r['paquete']
            if package not in inputs:
                folder = ROOT / 'forense/validacion-independiente/catalogo-1-preparacion-lote2/entradas' / package
                archives = list(folder.glob('*.tar.gz'))
                assert len(archives) == 1, archives
                archive = archives[0]
                with tarfile.open(archive) as t:
                    members = {m.name: sha(t.extractfile(m).read()) for m in t.getmembers() if m.isfile()}
                    manifest = json.loads(t.extractfile('manifiesto.json').read())
                inputs[package] = {'ruta': str(archive.relative_to(ROOT)), 'sha256': sha(archive.read_bytes()),
                                   'miembros_sha256': members, 'manifiesto': manifest}
            entry = inputs[package]
            clause = r['motivo'] if component == 'punto' else (
                'Receta completa de IC: población frente a dominio; orden de estratos/UPM/filas; '
                'algoritmo y consumo RNG; unidades y número de extracciones; multiplicidad/factor; '
                'estratos solitarios; réplicas inválidas; cuantiles. La receta abreviada entregada '
                'no determina identidad bit a bit bajo tolerancia histórica.')
            residuals.append({'llave': r['llave'], 'componente': component, 'instrumento': r['instrumento'],
                              'ola': r['ola'], 'calc': r['calc'], 'paquete_entregado': r['sucesor'],
                              'entrada_ruta': entry['ruta'], 'entrada_sha256': entry['sha256'],
                              'metodo_sha256': entry['miembros_sha256']['metodo.md'],
                              'estimandos_sha256': entry['miembros_sha256']['estimandos.tsv'],
                              'clausula_requerida': clause, 'fuente_humana_original_ruta': '',
                              'fuente_humana_original_sha256': '', 'localizador': '',
                              'disponibilidad': 'PENDIENTE-INTEGRACION-P2' if component == 'punto' else 'PENDIENTE-INTEGRACION-P3',
                              'decision': 'PENDIENTE-INTEGRACION-P2' if component == 'punto' else 'PENDIENTE-INTEGRACION-P3',
                              'estado_previo': state, 'evidencia_dictamen': r['notas_dictamen'],
                              'pieza_resolucion': 'p2' if component == 'punto' else 'p3'})
            old = enriched.get((r['llave'], component), {})
            for field in ['fuente_humana_original_ruta', 'fuente_humana_original_sha256', 'localizador',
                          'disponibilidad', 'decision']:
                if old.get(field):
                    residuals[-1][field] = old[field]
    counts = Counter(r['componente'] for r in residuals)
    unique = {r['llave'] for r in residuals}
    assert counts == {'punto': 56, 'ic': 312}, counts
    assert len(unique) == 312
    assert Counter(r['componente'] for r in discrepancies) == {'punto': 2, 'ic': 8}
    write_tsv('tabla-llave-componente.tsv', residuals)
    write_tsv('discrepancias-previas-preservadas.tsv', discrepancies)
    (OUT / 'entradas-entregadas-sha256.json').write_text(json.dumps(inputs, ensure_ascii=False, indent=2) + '\n')
    summary = {'fuente': str(SOURCE.relative_to(ROOT)), 'fuente_sha256': sha(SOURCE.read_bytes()),
               'llaves_corte': len(rows), 'filas_llave_componente': len(residuals), 'union_llaves': len(unique),
               'componentes': dict(counts), 'interseccion_punto_ic': 56,
               'por_instrumento_componente': dict(Counter(r['instrumento'] + '/' + r['componente'] for r in residuals)),
               'discrepancias_preservadas': dict(Counter(r['componente'] for r in discrepancies)),
               'microdatos_abiertos': False, 'productores_abiertos': False}
    (OUT / 'comprobacion-corte.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
