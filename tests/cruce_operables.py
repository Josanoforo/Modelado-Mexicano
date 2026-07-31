#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cruce completo catálogo (38 operables) × data/manifiesto.yaml.

No es un grep de acrónimo por prefijo (eso es lo que tests/dedup.py hace de
forma cruda y por lo que su cifra de "sin bajar" es solo una aproximación).
Aquí se declara explícitamente, por fuente operable, qué prefijos de `id`
en el manifiesto le pertenecen -- lista cerrada, mantenida a mano porque
los ids no siguen una convención mecánica única (encig2015_csv, ennvih1_...,
1_vfinal_..._ensanut_2024_..., etc.).

Uso: python3 tests/cruce_operables.py
"""
import json
import os
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import yaml

txt = open(os.path.join(RAIZ, 'data', 'manifiesto.yaml'), encoding='utf-8').read()
cuerpo = re.split(r'\n(?=- id:)', txt, maxsplit=1)[1]
entradas = yaml.safe_load(cuerpo)
con_payload = [e for e in entradas if 'sha256' in e]

# acronimo del catálogo -> lista de prefijos/substrings de `id` que le pertenecen
MAPA = {
    'ACS': [],
    'CNGF': [],
    'CNGMD': [],
    'CPS': [],
    'CPV': ['cpv2020'],
    'ECOVID-ML': [],
    'EDER': [],
    'EDR': [],
    'EIC': [],
    'ELCOS': [],
    'ENADID': ['enadid2023', 'enadid2018'],
    'ENAPROCE': [],
    'ENASEM': [],
    'ENCIG': ['encig'],
    'ENCUCI': ['encuci'],
    'ENCUESTA NACIONAL DE BIENESTAR': [],
    'ENCUESTA NACIONAL PARA EL SIST': [],
    'ENCUP': [],
    'ENDIREH': [],
    'ENDUTIH': [],
    'ENFIH': [],
    'ENIF': ['enif'],
    'ENIGH': ['enigh'],
    'ENNVIH': ['ennvih'],
    'ENOE': ['enoe_', 'enoen_', 'enoe_con_basedatos', 'encargoEG_ruptura_enoe'],
    'ENPOL': [],
    'ENSAFI': [],
    'ENSANUT': ['ensanut', 'vfinal_cuestionario', 'nse_hogar', 'nse_integrantes',
                'adolescentes_ensanut', 'adultos_ensanut', 'hogar_ensanut',
                'integrantes_ensanut', 'menores_ensanut', 'utilizadores_ensanut',
                'indice_de_bienestar'],
    'ENSU': [],
    'ENTI': [],
    'ENUT': ['enut'],
    'ENVIPE': ['envipe'],
    'ESTADÍSTICA EDUCATIVA': [],
    'ESTADÍSTICAS DE NATALIDAD / NA': [],
    'GLOBAL FINDEX DATABASE': [],
    'MOCIBA': [],
    'REGISTROS ADMINISTRATIVOS DE E': [],
    'SAEH': [],
}


def pertenece(id_, prefijos):
    return any(id_.startswith(p) or p in id_ for p in prefijos)


op = [r for r in json.load(open(os.path.join(RAIZ, 'data', 'catalogo_unico.json')))
      if r['micro'] == 'sí' and r['libre'] == 'sí']
op_acr = {r['acronimo'] for r in op}
faltan_mapa = op_acr - set(MAPA)
if faltan_mapa:
    raise SystemExit(f"MAPA incompleto, falta(n): {faltan_mapa}")

# ids que son solo instrumento (cuestionario) -- no microdato -- declarados a mano
# porque esta sesión los registró así (ver forense/notas/); si el con-payload de
# una fuente es subconjunto de este set, es PARCIAL, no EN MANIFIESTO.
SOLO_INSTRUMENTO = {
    'cpv2020_cuestionario_ampliado_pdf',
    'enadid2023_hogar_cuestionario_pdf',
    'enadid2023_mujer_modulo_cuestionario_pdf',
}

asignados = set()
print(f"{'ACRONIMO':32s} {'ESTADO':14s} PAYLOADS  (sin-payload)")
resumen = {'EN MANIFIESTO': 0, 'PARCIAL': 0, 'SIN PAYLOAD': 0}
detalle = []
for r in sorted(op, key=lambda r: r['acronimo']):
    prefijos = MAPA[r['acronimo']]
    con = [e for e in con_payload if pertenece(e['id'], prefijos)]
    sin = [e for e in entradas if e not in con_payload and pertenece(e['id'], prefijos)]
    asignados.update(e['id'] for e in con + sin)
    if not prefijos or (not con and not sin):
        estado = 'SIN PAYLOAD'
    elif con and {e['id'] for e in con} <= SOLO_INSTRUMENTO:
        estado = 'PARCIAL'
    elif con:
        estado = 'EN MANIFIESTO'
    else:
        estado = 'SIN PAYLOAD'
    resumen[estado] += 1
    detalle.append((r['acronimo'], estado, len(con), len(sin)))
    print(f"{r['acronimo']:32s} {estado:14s} {len(con):3d}       ({len(sin)})")

print()
print("RESUMEN:", resumen)
print(f"OPERABLES SIN PAYLOAD DE VERDAD: {resumen['SIN PAYLOAD']} de {len(op)}")

sin_atribuir = [e['id'] for e in entradas if e['id'] not in asignados]
print(f"\nEntradas del manifiesto NO atribuidas a ninguna de las 38 operables "
      f"(otras fuentes ya en manifiesto, o inventario sin fuente identificada "
      f"sin abrir el archivo): {len(sin_atribuir)}")
for i in sin_atribuir:
    print(' ', i)
