#!/usr/bin/env python3
"""Enlaza propuesta de tablas con inventario custodial firmado; nunca lee ZIP."""
import argparse
import importlib.util
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location('custodia', ROOT / 'impedimentos-lote2-p3-proyecta.py')
custodia = importlib.util.module_from_spec(spec)
spec.loader.exec_module(custodia)


def compila(proposal, inventory, signature, public_key, trusted_key_sha256):
    raw = custodia.autentica(inventory, signature, public_key, trusted_key_sha256)
    i = json.loads(raw, object_pairs_hook=custodia.unico)
    c = json.loads(custodia.lee(proposal), object_pairs_hook=custodia.unico)
    custodia.exige(i['schema'] == 'custodia-inventario-v1' and i['records_read'] is False,
                   'no es inventario custodial')
    custodia.exige(i['source_sha256'] == c['source_sha256'], 'fuente inventario discordante')
    custodia.exige(i['code_sha256'] == c['code_sha256'], 'código inventario discordante')
    names = [m['member'] for m in i['members']]
    custodia.exige(len(names) == len(set(names)), 'inventario duplicado')
    for m in i['members']:
        p = PurePosixPath(m['member'])
        custodia.exige(not p.is_absolute() and '..' not in p.parts and '\\' not in m['member']
                       and not m['symlink'], 'miembro inseguro')
    c['members'] = {}
    for table in c['table_proposals']:
        # Exact basename equality; no regex/case folding/automatic adaptation.
        matches = [m for m in i['members'] if not m['directory']
                   and PurePosixPath(m['member']).name == table['documented_filename']]
        custodia.exige(len(matches) == 1, 'tabla ausente o ambigua')
        member = matches[0]['member']
        custodia.exige(member not in c['members'], 'tabla duplicada')
        c['members'][member] = {k: v for k, v in table.items()
                                if k not in ('documented_filename', 'logical_table', 'filename_evidence')}
    c['archive_inventory'] = names
    c['inventory_document_sha256'] = custodia.sha(raw)
    c['inventory_contract_sha256'] = i['inventory_contract_sha256']
    c['inventory_custodian_key_sha256'] = trusted_key_sha256
    c['operation'] = 'project'
    c['approved'] = False
    c['human_signature'] = {'reference': None, 'body_sha256': None, 'literal': None,
                             'scope': 'project', 'verified_by_custodian': False,
                             'reservation_scopes': []}
    c['status'] = 'PROPUESTO-POR-EJECUTOR; ENLAZADO; REQUIERE-FIRMA-ETAPA2'
    return c


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for n in ('proposal', 'inventory', 'signature', 'public-key', 'trusted-key-sha256'):
        p.add_argument('--' + n, required=True)
    try:
        print(json.dumps(compila(**vars(p.parse_args())), ensure_ascii=False, indent=2))
    except Exception:
        print('RECHAZADO: inventario, firma, fuente o enlace inválido')
        raise SystemExit(2)
