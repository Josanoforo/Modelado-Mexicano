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
    if args.gold_se:
        gold_document = json.loads(args.gold_se.read_text())
        for label, group in gold_document['grupos'].items():
            if group['se_taylor'] is None:
                gold_blocks.append(dict(family='ENSU', group=label, reason='SE-TAYLOR-NULA-SINGLETON', singleton=group['singleton']))
                continue
            for temporal in (0., .01, .03):
                gold_rows.append(calculate('ENSU-SEXO-'+str(label), float(group['se_taylor']), 0., temporal))
    if args.enoe_gold_se:
        gold_document = json.loads(args.enoe_gold_se.read_text())
        for label, group in gold_document['grupos'].items():
            if group['se_taylor'] is None:
                gold_blocks.append(dict(family='ENOE', group=label, reason='SE-TAYLOR-NULA-SINGLETON', singleton=group['singleton']))
                continue
            for temporal in (0., .01, .03):
                gold_rows.append(calculate('ENOE-SEX-'+str(label), float(group['se_taylor']), 0., temporal))
    for row in rows:
        # Generic frontier assumes two hypothetical groups with equal precision.
        row['joint_lower_bound_stability'] = max(0., 1-TESTS*(1-row['probability_informative_stability']))
        row['joint_lower_bound_change'] = max(0., 1-TESTS*(1-row['probability_informative_change']))
    for row in gold_rows:
        peers = [r for r in gold_rows if r['group'].split('-')[0] == row['group'].split('-')[0]
                 and r['temporal_sd_assumed'] == row['temporal_sd_assumed']]
        for metric in ('stability', 'change'):
            row['joint_lower_bound_'+metric] = max(0., 1-sum(1-r['probability_informative_'+metric] for r in peers))
    output = Path(__file__).parent
    decisions = {}
    for family in ('ENSU', 'ENOE'):
        family_rows = [r for r in gold_rows if r['group'].startswith(family+'-')]
        decisions[family] = ('PREPARAR-LANZAMIENTO-CONDICIONAL' if family_rows and
                             all(r['meets_per_group_target'] for r in family_rows)
                             else 'NO-LANZAR-TODAVIA')
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
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter='\t')
        writer.writeheader()
        writer.writerows(rows + gold_rows)
    print(json.dumps(dict(z=Z, escenarios=len(rows), oro=len(gold_rows), bloqueos=len(gold_blocks), decision=decisions)))


if __name__ == '__main__':
    main()
