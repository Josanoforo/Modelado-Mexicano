#!/usr/bin/env python3
"""Deriva disposición documental de #1203; jamás concede acceso ni ejecuta paquetes."""
import argparse
import csv
import hashlib
import json
from pathlib import Path


def derive(source, evidence):
    proof = json.loads(evidence.read_text())
    with source.open(newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    output = []
    for row in rows:
        year = '2021' if '2021' in row['subcohorte'] else '2016'
        output.append({
            'paquete': row['paquete'], 'identidades': int(row['identidades']),
            'entrada': row['sucesor'], 'sha256_entrada': row['sha256_sucesor'],
            'apto_tecnicamente': 'NO-VERIFICADO-PARA-PAQUETE-REAL',
            'estado_entorno': proof.get('estado', 'NO-LANZAR-COMO-CIEGA'),
            'autorizado_para_abrir': False,
            'permiso': f'FP-260926-ASTRA6-C1-REEMPAQUETA-VENTANA-1-ee49-0{1 if year == "2021" else 2}',
            'estado_permiso_al_corte': 'ABIERTA',
            'ola': 'ENDIREH' + year,
            'alcance_permiso': 'módulos/campos/finalidad por paquete en hoja-de-firma-acceso-futuro.md de #1203',
            'intento': row['intento_futuro'],
            'requisitos': ['firma aplicable verificable al lanzamiento',
                          'sesión realmente nueva sin misión ni resultados',
                          'allowlist limpia con hashes, contrato v2 fijado',
                          'prueba material de lectura y red del mismo entorno',
                          'ordinal nuevo desde historial preservado, nunca reutilizar intento1',
                          'congelar código y números antes de revelar referencia'],
            'decision_recomendada': 'NO-LANZAR; recibir producto portable y resolver permiso/entorno por separado',
        })
    return {'version': 'disposicion-v2',
            'fuente_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'prueba_entorno_sha256': hashlib.sha256(evidence.read_bytes()).hexdigest(),
            'paquetes': output, 'total_identidades': sum(x['identidades'] for x in output),
            'historico_lote2': 'RESERVA-DE-SEPARACION-PRESERVADA; no se rehabilita retrospectivamente',
            'estado': 'PROPUESTO-POR-EJECUTOR; no concede firmas ni adopción'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fuente', type=Path, required=True)
    parser.add_argument('--prueba-entorno', type=Path, required=True)
    parser.add_argument('--salida', type=Path, required=True)
    args = parser.parse_args()
    args.salida.write_text(json.dumps(derive(args.fuente, args.prueba_entorno),
                                     ensure_ascii=False, indent=2) + '\n')
