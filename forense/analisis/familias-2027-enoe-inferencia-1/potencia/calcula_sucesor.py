"""P5: consume diagnóstico agregado; importa contrato sin ejecutar su CLI histórico."""
import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = ROOT / 'forense/analisis/familias-2027-frontera-1'
SOURCE = BASE / 'potencia/calcula.py'
spec = importlib.util.spec_from_file_location('contrato_potencia_frontera', SOURCE)
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)
GOLD = BASE / 'paquetes/ENOE-INFORMALIDAD/enoe-oro.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(diagnostic, historical):
    rows, blocks = contract.gold_family(diagnostic, 'ENOE')
    # Un impedimento metodológico no se resuelve por publicar un SE numérico.
    for label, group in diagnostic.get('grupos', {}).items():
        if group.get('razon_bloqueo'):
            blocks.append(dict(family='ENOE', group=label, reason=group['razon_bloqueo']))
    complete = contract.complete_family(rows, blocks, 'ENOE')
    if complete:
        for row in rows:
            peers = [r for r in rows if r['temporal_sd_assumed'] == row['temporal_sd_assumed']]
            for metric in ('stability', 'change'):
                row['joint_lower_bound_' + metric] = max(
                    0., 1 - sum(1 - r['probability_informative_' + metric] for r in peers))
    decision = contract.family_decision(rows, blocks, 'ENOE')
    lookup = {(r['group'], r['temporal_sd_assumed']): r for r in rows}
    table = []
    for label in contract.EXPECTED_GROUPS:
        group = diagnostic.get('grupos', {}).get(label, {})
        reasons = [b['reason'] for b in blocks if b.get('group') in (None, label)]
        if blocks and not reasons:
            reasons = ['FAMILIA-INCOMPLETA: ' + '; '.join(b['reason'] for b in blocks)]
        for temporal in contract.TEMPORAL_SCENARIOS:
            row = lookup.get(('ENOE-SEX-' + label, temporal), {})
            # No cálculo prospectivo acreditado cuando falta identificación de la familia.
            if not complete:
                row = dict(group='ENOE-SEX-' + label, rho_assumed=0., temporal_sd_assumed=temporal,
                           **{key: None for key in contract.calculate('fixture', .01, 0., 0.)
                              if key not in ('group', 'rho_assumed', 'temporal_sd_assumed')})
            row = dict(row, p0_fijo=historical['grupos'][label]['p0'],
                       ola_oro='2024T4', ola_objetivo='2027T4', decision=decision,
                       razon_bloqueo='; '.join(reasons),
                       insumo_faltante=group.get('insumo_faltante', diagnostic.get('insumo_faltante', '')))
            table.append(row)
    return dict(status='PROPUESTO-POR-EJECUTOR', alpha_family=contract.ALPHA,
                tests=contract.TESTS, target=contract.TARGET, band=contract.BAND,
                scenario_count=len(table), inference_identifiable=complete,
                decision=decision, blocks=blocks, scenarios=table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--diagnostico', required=True, type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.diagnostico.read_text()), json.loads(GOLD.read_text()))
    result['sources'] = {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p): sha(p)
                         for p in (SOURCE, BASE / 'potencia/criterios-previos.md', GOLD, args.diagnostico.resolve())}
    (HERE / 'enoe-potencia-resultados.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    with (HERE / 'enoe-escenarios.tsv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result['scenarios'][0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(result['scenarios'])
    print(json.dumps({k: result[k] for k in ('scenario_count', 'inference_identifiable', 'decision')}))


if __name__ == '__main__':
    main()
