"""Frontera normal analítica; escenarios explícitos, sin abrir microdatos."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import NormalDist

NORMAL = NormalDist()
ALPHA = .05
TARGET = .80
BAND = .05
TESTS = 2  # ENSU, dos sexos, una ola
Z = NORMAL.inv_cdf(1 - ALPHA / (2 * TESTS))
GROUP_PREFIX = {'ENSU': 'ENSU-SEXO-', 'ENOE': 'ENOE-SEX-'}
EXPECTED_GROUPS = ('1', '2')
TEMPORAL_SCENARIOS = (0., .01, .03)


def valid_se(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value > 0)


def gold_family(document, family):
    rows, blocks = [], []
    groups = document.get('grupos', {})
    for label in sorted(set(groups) - set(EXPECTED_GROUPS)):
        blocks.append(dict(family=family, group=label, reason='GRUPO-NO-PREVISTO'))
    for label in EXPECTED_GROUPS:
        if label not in groups:
            blocks.append(dict(family=family, group=label, reason='GRUPO-AUSENTE'))
            continue
        group = groups[label]
        se = group.get('se_taylor')
        if not valid_se(se):
            blocks.append(dict(family=family, group=label,
                               reason='SE-TAYLOR-NULA-SINGLETON' if se is None else 'SE-TAYLOR-INVALIDA',
                               singleton=group.get('singleton', [])))
            continue
        for temporal in TEMPORAL_SCENARIOS:
            rows.append(calculate(GROUP_PREFIX[family] + label, se, 0., temporal))
    return rows, blocks


def complete_family(rows, blocks, family):
    if any(block['family'] == family for block in blocks):
        return False
    expected = {(GROUP_PREFIX[family] + label, 0., temporal)
                for label in EXPECTED_GROUPS for temporal in TEMPORAL_SCENARIOS}
    actual = [(r['group'], r['rho_assumed'], r['temporal_sd_assumed']) for r in rows]
    return (len(actual) == len(expected) and set(actual) == expected
            and all(valid_se(r['se_gold']) and valid_se(r['se_future_assumed'])
                    for r in rows))


def family_decision(rows, blocks, family):
    family_rows = [r for r in rows if r['group'].startswith(GROUP_PREFIX[family])]
    return ('PREPARAR-LANZAMIENTO-CONDICIONAL'
            if complete_family(family_rows, blocks, family)
            and all(r['meets_per_group_target'] for r in family_rows)
            else 'NO-LANZAR-TODAVIA')


def probability_between(lo, hi, mean, sd):
    return max(0., NORMAL.cdf((hi - mean) / sd) - NORMAL.cdf((lo - mean) / sd))


def power(delta, se):
    h = Z * se
    return 1 - probability_between(-h, h, delta, se)


def mde(se):
    lo, hi = 0., 1.
    for _ in range(70):
        mid = (lo + hi) / 2
        if power(mid, se) < TARGET:
            lo = mid
        else:
            hi = mid
    return hi


def informative(delta, se, temporal_sd):
    h = Z * se
    total_sd = math.hypot(se, temporal_sd)
    outside = 1 - probability_between(-BAND - h, BAND + h, delta, total_sd)
    inside = probability_between(-BAND + h, BAND - h, delta, total_sd) if h < BAND else 0.
    return outside + inside


def calculate(label, se_gold, rho, temporal_sd, effective_n=None):
    # Equal future precision is an assumption, never a forecasted survey SE.
    se_future = se_gold
    variance = se_gold**2 + se_future**2 - 2 * rho * se_gold * se_future
    se_change = math.sqrt(variance)
    p_stable = informative(0., se_change, temporal_sd)
    p_change = informative(2 * BAND, se_change, temporal_sd)
    return dict(group=label, n_effective_assumed=effective_n,
                se_gold=se_gold, se_future_assumed=se_future,
                rho_assumed=rho, temporal_sd_assumed=temporal_sd,
                se_change=se_change, half_ci=Z * se_change, mde=mde(se_change),
                power_change=power(2 * BAND, se_change),
                probability_informative_stability=p_stable,
                probability_informative_change=p_change,
                conditional_fixed_p0_half_ci=Z*se_future,
                conditional_fixed_p0_mde=mde(se_future),
                conditional_fixed_p0_info_stability=informative(0., se_future, temporal_sd),
                conditional_fixed_p0_info_change=informative(2*BAND, se_future, temporal_sd),
                joint_lower_bound_stability=None,
                joint_lower_bound_change=None,
                meets_per_group_target=min(p_stable, p_change) >= TARGET)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gold-se', type=Path,
                        help='ensu-oro.json del paquete ENSU; consume grupos/se_taylor, no microdato')
    parser.add_argument('--enoe-gold-se', type=Path)
    args = parser.parse_args()
    rows = []
    for n in (500, 2000, 10000):
        for rho in (0., .5, .8):
            for temporal in (0., .01, .03):
                rows.append(calculate('ESCENARIO-NO-CALIBRADO', math.sqrt(.25/n), rho, temporal, n))
    gold_rows = []
    gold_blocks = []
    for family, source in (('ENSU', args.gold_se), ('ENOE', args.enoe_gold_se)):
        family_rows, family_blocks = gold_family(
            json.loads(source.read_text()) if source else {}, family)
        gold_rows.extend(family_rows)
        gold_blocks.extend(family_blocks)
    for row in rows:
        # Generic frontier assumes two hypothetical groups with equal precision.
        row['joint_lower_bound_stability'] = max(0., 1-TESTS*(1-row['probability_informative_stability']))
        row['joint_lower_bound_change'] = max(0., 1-TESTS*(1-row['probability_informative_change']))
    for row in gold_rows:
        family = row['group'].split('-')[0]
        family_rows = [r for r in gold_rows if r['group'].startswith(GROUP_PREFIX[family])]
        if not complete_family(family_rows, gold_blocks, family):
            continue  # No cota conjunta acreditada sobre una familia incompleta.
        peers = [r for r in gold_rows if r['group'].split('-')[0] == row['group'].split('-')[0]
                 and r['temporal_sd_assumed'] == row['temporal_sd_assumed']]
        for metric in ('stability', 'change'):
            row['joint_lower_bound_'+metric] = max(0., 1-sum(1-r['probability_informative_'+metric] for r in peers))
    output = Path(__file__).parent
    decisions = {family: family_decision(gold_rows, gold_blocks, family)
                 for family in GROUP_PREFIX}
    document = dict(status='PROPUESTO-POR-EJECUTOR', method='integracion-normal-analitica',
                    alpha_family=ALPHA, tests=TESTS, z=Z, target=TARGET, band=BAND,
                    criteria_sha256=hashlib.sha256((output/'criterios-previos.md').read_bytes()).hexdigest(),
                    gold_source=str(args.gold_se) if args.gold_se else None,
                    gold_sha256=hashlib.sha256(args.gold_se.read_bytes()).hexdigest() if args.gold_se else None,
                    enoe_gold_source=str(args.enoe_gold_se) if args.enoe_gold_se else None,
                    enoe_gold_sha256=hashlib.sha256(args.enoe_gold_se.read_bytes()).hexdigest() if args.enoe_gold_se else None,
                    gold_calibrated=bool(gold_rows), scenarios=rows, gold_scenarios=gold_rows,
                    gold_inference_blocks=gold_blocks,
                    decision_by_family=decisions,
                    decision='PROPUESTAS-CONDICIONALES-SIN-ADOPCION',
                    caveat='Escenarios no son emisiones ni aciertos futuros; requieren comparabilidad e inferencia de diseño.')
    (output/'frontera-potencia-resultados.json').write_text(json.dumps(document, ensure_ascii=False, indent=2)+'\n')
    with (output/'escenarios.tsv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows + gold_rows)
    print(json.dumps(dict(z=Z, escenarios=len(rows), oro=len(gold_rows), bloqueos=len(gold_blocks), decision=decisions)))


if __name__ == '__main__':
    main()
