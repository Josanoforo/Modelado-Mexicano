"""Oro histórico y emisiones por referencia; nunca evalúa la ola futura."""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
import yaml

from medidor import FAMILIAS, leer, medir, sha
from potencia import ejecutar as potencia

ROOT = Path(__file__).resolve().parents[3]
ANALISIS = ROOT/'forense/analisis/familias-2027/astra6-envipe'
SPEC = ANALISIS/'auxiliares-spec.yaml'
CALCS = {
    'DENUNCIA_U4': ('CALC-ENVIPE-0001', 'RESULT-ENVIPE-DEN-P-C2-U4', 'DENUNCIA-U4'),
    'EVASION_NORMA': ('CALC-EVASION-NORMA-0001-v1_1', 'RESULT-EVASIONNORMA-A-P-EVADE', 'EVASION-NORMA'),
}


def escribir(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n')


def verificar_congelado():
    manifest = json.loads((ANALISIS/'commit1-hashes.json').read_text())
    for rel, expected in manifest.items():
        if sha(ROOT/rel) != expected:
            raise ValueError('COMMIT-1 alterado: '+rel)


def historico():
    verificar_congelado()
    contrato = yaml.safe_load(SPEC.read_text())
    commit1 = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    diag, reps = medir(leer(ROOT/'data/raw/envipe2025_csv.zip', contrato), contrato)
    evidencia = {'tipo': 'ORO-HISTORICO-NO-EVALUACION-FUTURA', 'commit1': commit1,
                 'insumo': contrato['insumo'], 'familias': {}}
    for name in FAMILIAS:
        calc, rid, slug = CALCS[name]
        folder = ROOT/'data/corrida0'/calc
        p0 = json.loads((folder/'resultados.json').read_text())['resultados'][rid]
        error = diag['familias'][name]['punto'] - p0
        if abs(error) > 1e-6:
            raise ValueError('oro DISCREPA: '+name)
        diag['familias'][name]['soporte'] = {k: v for k, v in diag['familias'][name].items()}
        evidencia['familias'][name] = {
            'result': rid, 'sello_sha256': sha(folder/'sello.json'),
            'resultados_sha256': sha(folder/'resultados.json'),
            'valor_result': p0, 'punto_recalculado': diag['familias'][name]['punto'],
            'error': error, 'tolerancia': 1e-6, 'estado': 'REPRODUCE-PUNTO',
            'ic': 'DIAGNOSTICO-NUEVO; no intenta reproducir extremos históricos',
        }
        out = ROOT/'data/corrida0'/('CALC-FAMILIA-2027-ENVIPE-'+slug)
        out.mkdir(exist_ok=True)
        escribir(out/'emision.json', {
            'familia': name, 'ola_objetivo': 'envipe_2027', 'R_futura': None,
            'p0': p0, 'fuente': evidencia['familias'][name], 'retadores': [],
            'estado': 'SELLADO-INTERNAMENTE', 'commit1': commit1,
            'resultado': 'EMISION-BASE-NO-ADOPCION-NO-EVALUACION',
        })
    escribir(ANALISIS/'oro.json', evidencia)
    escribir(ANALISIS/'diagnostico.json', diag)
    # JSON de vectores: bytes reproducibles, a diferencia de ZIP/NPZ con timestamps.
    escribir(ANALISIS/'replicas.json', {k: reps[k].tolist() for k in FAMILIAS})
    escribir(ANALISIS/'potencia.json', potencia(reps, diag))
    print(json.dumps({k: diag['familias'][k] for k in FAMILIAS}, ensure_ascii=False))


def reproduce():
    """Reproduce emisiones desde RESULT; no lee registros ni calcula oro."""
    verificar_congelado()
    for name, (calc, rid, slug) in CALCS.items():
        source = ROOT/'data/corrida0'/calc
        out = ROOT/'data/corrida0'/('CALC-FAMILIA-2027-ENVIPE-'+slug)/'emision.json'
        e = json.loads(out.read_text())
        assert e['R_futura'] is None and not e['retadores']
        assert e['p0'] == json.loads((source/'resultados.json').read_text())['resultados'][rid]
        assert e['fuente']['sello_sha256'] == sha(source/'sello.json')
        assert e['fuente']['resultados_sha256'] == sha(source/'resultados.json')
    print('REPRODUCE-EMISIONES: 2; R futura ausente; oro es comprobación separada')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--historico', action='store_true')
    p.add_argument('--reproduce-emisiones', action='store_true')
    args = p.parse_args()
    if args.historico == args.reproduce_emisiones:
        p.error('elige exactamente una acción')
    historico() if args.historico else reproduce()
