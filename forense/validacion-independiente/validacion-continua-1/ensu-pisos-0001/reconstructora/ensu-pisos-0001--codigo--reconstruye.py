"""Reconstruccion CALC-ENSU-PISOS-0001 desde paquete/ (spec humana v1.0 + lista cerrada P1).

Uso, desde el directorio de trabajo:  python3 salida/codigo/reconstruye.py
Escribe salida/resultado.json y salida/diagnostico.json.
"""
import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, 'paquete/lib')  # lectores de terceros; no se usan (todo es CSV)

SEMILLA = 20260925
R = 1000
IDENTIDAD = {"paquete": "ensu-pisos-0001", "version_entrada": "validacion-continua-1",
             "sha256_entrada": "327c54c1367a2f23803638b2f2e2d36e9bfa7656aabd08c37e65e088d4aa37e5"}

BASE = ['UPM', 'VIV_SEL', 'H_MUD', 'R_SEL', 'CD', 'EST_DIS', 'UPM_DIS', 'FAC_SEL',
        'BP1_1', 'BP1_2_03', 'BP1_2_08', 'BP1_2_09', 'BP1_3', 'BP1_4_3', 'BP1_4_4',
        'BP1_4_6', 'BP1_5_1', 'BP1_5_2', 'BP1_5_3', 'BP1_5_4', 'BP1_9_1', 'BP1_8_1',
        'SEXO', 'EDAD']
ARCHIVOS = {
    '2024T1': ('paquete/datos/ensu_2024t1_cb.csv', BASE),
    '2025T3': ('paquete/datos/ensu_2025t3_cb.csv', BASE),
    '2025T4': ('paquete/datos/ensu_2025t4_cb.csv', BASE + ['BP3_5', 'BP3_6']),
}

# Lista cerrada P1 s3: reactivo, codigos "si", universo
CONDUCTAS = {
    'c01-inseg-ciudad': ('BP1_1', {'2'}, {'1', '2', '9'}),
    'c02-inseg-calle': ('BP1_2_03', {'2'}, {'1', '2', '9'}),
    'c03-inseg-cajero': ('BP1_2_08', {'2'}, {'1', '2', '9'}),
    'c04-inseg-transporte': ('BP1_2_09', {'2'}, {'1', '2', '9'}),
    'c05-expect-empeora': ('BP1_3', {'4'}, {'1', '2', '3', '4', '9'}),
    'c06-testigo-robos': ('BP1_4_3', {'1'}, {'1', '2', '9'}),
    'c07-testigo-pandillas': ('BP1_4_4', {'1'}, {'1', '2', '9'}),
    'c08-testigo-disparos': ('BP1_4_6', {'1'}, {'1', '2', '9'}),
    'c09-habito-objetos-valor': ('BP1_5_1', {'1'}, {'1', '2', '3', '9'}),
    'c10-habito-caminar-noche': ('BP1_5_2', {'1'}, {'1', '2', '3', '9'}),
    'c11-habito-visitar': ('BP1_5_3', {'1'}, {'1', '2', '3', '9'}),
    'c12-habito-menores': ('BP1_5_4', {'1'}, {'1', '2', '3', '9'}),
    'c13-policia-mun-confianza': ('BP1_9_1', {'1', '2'}, {'1', '2', '3', '4', '9'}),
    'c14-policia-mun-efectiva': ('BP1_8_1', {'1', '2'}, {'1', '2', '3', '4', '9'}),
    'c15-corrupcion-policia': ('BP3_6', {'1'}, {'1', '2', '9'}),  # y BP3_5 == '1'
}


def segmento_edad(e):
    """18-29, 30-44, 45-59, 60-MAS (60-97; 97 = '97 o mas'); 98/99 y no numerico fuera."""
    out = pd.Series('', index=e.index, dtype=object)
    n = pd.to_numeric(e, errors='coerce')
    out[(n >= 18) & (n <= 29)] = '18-29'
    out[(n >= 30) & (n <= 44)] = '30-44'
    out[(n >= 45) & (n <= 59)] = '45-59'
    out[(n >= 60) & (n <= 97)] = '60-MAS'
    return out


def carga(ola):
    ruta, cols = ARCHIVOS[ola]
    d = pd.read_csv(ruta, usecols=cols, dtype=str, keep_default_na=False)
    for c in cols:
        d[c] = d[c].str.strip()
    diag = {'filas_archivo': int(len(d))}
    w = pd.to_numeric(d['FAC_SEL'], errors='coerce')
    ok_w = w > 0
    ok_st = (d['CD'] != '') & (d['EST_DIS'] != '')
    ok_u = d['UPM_DIS'] != ''
    diag['excl_factor_no_positivo'] = int((~ok_w).sum())
    diag['excl_estrato_vacio'] = int((ok_w & ~ok_st).sum())
    diag['excl_upm_vacia'] = int((ok_w & ok_st & ~ok_u).sum())
    d = d[ok_w & ok_st & ok_u].copy()
    d['w'] = w[d.index].astype(float)
    diag['filas_validas_marco'] = int(len(d))
    llave = d['UPM'] + '|' + d['VIV_SEL'] + '|' + d['H_MUD'] + '|' + d['R_SEL']
    diag['llave_cb_duplicada_filas_conservadas'] = int(llave.duplicated(keep=False).sum())
    d['estrato'] = d['CD'] + '|' + d['EST_DIS']
    d['conglom'] = d['estrato'] + '|' + d['UPM_DIS']
    d['ENT'] = d['UPM'].str.zfill(7).str[:2]
    d['SEXO_SEG'] = d['SEXO'].map({'1': 'HOMBRE', '2': 'MUJER'}).fillna('')
    d['EDAD_SEG'] = segmento_edad(d['EDAD'])
    d['CIUDAD'] = d['CD']
    diag['sexo_fuera_catalogo'] = int((d['SEXO_SEG'] == '').sum())
    diag['edad_fuera_eje'] = {k: int(v) for k, v in d.loc[d['EDAD_SEG'] == '', 'EDAD'].value_counts().sort_index().items()}
    diag['edad_97_en_60_MAS'] = int((d['EDAD'] == '97').sum())
    return d.reset_index(drop=True), diag


def multiplicidades(d):
    """Bootstrap de UPM dentro de estrato: matriz R x n_upm de multiplicidades."""
    rng = np.random.Generator(np.random.PCG64(SEMILLA))
    upms = d[['estrato', 'conglom']].drop_duplicates().sort_values(['estrato', 'conglom'])
    upm_idx = {u: i for i, u in enumerate(upms['conglom'])}
    M = np.zeros((R, len(upms)), dtype=np.float64)
    n_cert = 0
    pos = 0
    for est, g in upms.groupby('estrato', sort=True):
        nh = len(g)
        cols = np.arange(pos, pos + nh)
        if nh == 1:
            M[:, cols[0]] = 1.0  # UPM unica de certeza
            n_cert += 1
        else:
            draws = rng.integers(0, nh, size=(R, nh))
            for r in range(R):
                M[r, cols] = np.bincount(draws[r], minlength=nh)
        pos += nh
    return M, d['conglom'].map(upm_idx).to_numpy(), {'n_estratos': int(upms['estrato'].nunique()),
                                                     'n_upm': int(len(upms)),
                                                     'estratos_upm_unica_certeza': n_cert}


def main():
    esquema = pd.read_csv('paquete/esquema-identidades.tsv', sep='\t', dtype=str, keep_default_na=False)
    filas_out = {}
    diag_llaves = {}
    diag_olas = {}
    eje_col = {'TOTAL': None, 'SEXO': 'SEXO_SEG', 'EDAD': 'EDAD_SEG', 'ENT': 'ENT', 'CIUDAD': 'CIUDAD'}

    for ola in ['2024T1', '2025T3', '2025T4']:
        d, dg = carga(ola)
        M, uidx, dgb = multiplicidades(d)
        dg.update(dgb)
        diag_olas[ola] = dg
        nu = M.shape[1]
        sub = esquema[esquema['ola'] == ola]
        for cond, g in sub.groupby('conducta', sort=False):
            var, si, univ = CONDUCTAS[cond]
            v = d[var]
            en_univ = v.isin(univ)
            if cond == 'c15-corrupcion-policia':
                en_univ = en_univ & (d['BP3_5'] == '1')
            y = v.isin(si).astype(float).to_numpy()
            wv = d['w'].to_numpy()
            celdas = []
            for _, fila in g.iterrows():
                col = eje_col[fila['eje']]
                dom = pd.Series(True, index=d.index) if col is None else (d[col] == fila['segmento'])
                m = (dom & en_univ).to_numpy()
                ex = {}
                vd = v[dom]
                if cond == 'c15-corrupcion-policia':
                    b5 = d.loc[dom, 'BP3_5']
                    ex['BP3_5_distinto_de_1'] = {k: int(c) for k, c in b5[b5 != '1'].value_counts().sort_index().items()}
                    vd = vd[b5 == '1']
                ex['codigo_fuera_de_universo'] = {(k if k != '' else 'blanco'): int(c)
                                                  for k, c in vd[~vd.isin(univ)].value_counts().sort_index().items()}
                if fila['eje'] == 'EDAD':
                    ex['nota'] = 'edad 98/99 fuera del eje EDAD: ver diagnostico por ola'
                n = int(m.sum())
                diag_llaves[fila['llave']] = {'n_dominio': int(dom.sum()), 'n_valido': n, 'exclusiones': ex}
                celdas.append((fila['llave'], m, n))
            # agregados por UPM por celda
            idx = [i for i, (_, _, n) in enumerate(celdas) if n > 0]
            if idx:
                NUM = np.zeros((nu, len(idx)))
                DEN = np.zeros((nu, len(idx)))
                for j, i in enumerate(idx):
                    m = celdas[i][1]
                    np.add.at(NUM[:, j], uidx[m], (wv * y)[m])
                    np.add.at(DEN[:, j], uidx[m], wv[m])
                pnum = NUM.sum(0)
                pden = DEN.sum(0)
                RN = M @ NUM
                RD = M @ DEN
            for i, (llave, m, n) in enumerate(celdas):
                fila = {'llave': llave, 'unidad': sub.loc[sub['llave'] == llave, 'unidad'].iloc[0]}
                if n == 0:
                    fila['estado'] = 'DENOMINADOR-CERO'
                    fila['motivo'] = ('N=0: ninguna persona del marco valido en este dominio con codigo '
                                      'dentro del universo de la conducta (spec s3: celda sin personas emite N=0 y P/IC nulos)')
                    filas_out[llave] = fila
                    continue
                j = idx.index(i)
                p = pnum[j] / pden[j]
                fila['estado'] = 'RECONSTRUIDO'
                fila['punto'] = repr(float(p))
                deg = int((RD[:, j] <= 0).sum())
                diag_llaves[llave]['replicas_degeneradas'] = deg
                if deg > 0:
                    fila['estado_ic'] = 'NO-IDENTIFICADA'
                    fila['motivo_ic'] = (f'{deg} de {R} replicas bootstrap sin personas del dominio '
                                         '(denominador cero); contrato conservador de la spec s3: replica degenerada -> sin IC')
                else:
                    pr = RN[:, j] / RD[:, j]
                    lo, hi = np.percentile(pr, [2.5, 97.5])
                    fila['estado_ic'] = 'CALCULADO'
                    fila['ic95_inf'] = repr(float(lo))
                    fila['ic95_sup'] = repr(float(hi))
                filas_out[llave] = fila

    filas = [filas_out[k] for k in esquema['llave']]
    assert len(filas) == len(esquema) == len(set(esquema['llave']))
    with open('salida/resultado.json', 'w', encoding='utf-8') as f:
        json.dump({'version': 3, 'identidad': IDENTIDAD, 'filas': filas}, f, ensure_ascii=False, indent=1)

    decisiones = [
        {'decision': 'Bootstrap ingenuo: en cada estrato con n_h>=2 UPM se sortean n_h UPM con reemplazo; la multiplicidad multiplica FAC_SEL; sin reescalamiento tipo Rao-Wu.',
         'frase': '«Proporción ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato» (spec s3)'},
        {'decision': 'Un generador np.random.Generator(PCG64(20260925)) nuevo por ola; estratos en orden lexicografico de CD|EST_DIS, UPM en orden lexicografico dentro del estrato; por estrato se sortea integers(0,n_h,size=(1000,n_h)). Las mismas replicas por ola se usan para todas las conductas y ejes.',
         'frase': '«`PCG64(20260925)`, 1 000 réplicas» y «se calculan con el mismo marco, semilla y réplicas» (spec s3, s4)'},
        {'decision': 'Estrato = par (CD, EST_DIS); UPM = UPM_DIS anidada en ese estrato.',
         'frase': '«Estrato del bootstrap = `CD` + estrato de diseño (`EST_DIS`)... UPM = `UPM_DIS` dentro del estrato» (spec s1)'},
        {'decision': 'Estrato con una sola UPM: multiplicidad fija 1 en todas las replicas (no aporta varianza).',
         'frase': '«UPM única de certeza» (spec s3)'},
        {'decision': 'Replica degenerada = replica cuyo denominador ponderado del dominio×universo es 0; si hay al menos una, la celda queda sin IC (NO-IDENTIFICADA). Replicas con P en {0,1} no se consideran degeneradas.',
         'frase': '«contrato conservador (réplica degenerada → sin IC)» (spec s3)'},
        {'decision': 'Percentiles 2.5/97.5 con np.percentile (interpolacion lineal por defecto) sobre las 1000 proporciones replicadas.',
         'frase': '«percentiles 2.5/97.5» (spec s3)'},
        {'decision': 'EDAD 97 («97 o más años») se incluye en 60-MAS; solo 98/99 salen del eje.',
         'frase': '«`60-MAS` = 60–96; 98/99 «no especificada» fuera del eje» (lista s4) — 97 no se nombra; la etiqueta es «60 y más»'},
        {'decision': 'ENT = dos primeros digitos de UPM (UPM rellenada a 7 digitos).',
         'frase': '«E2/E3 los dos primeros dígitos de `UPM`» (lista s2)'},
        {'decision': 'SEXO 1=HOMBRE, 2=MUJER (FD 2025 CB); sin join CS en E3.',
         'frase': '«E3 | 2021T2–2025T4 | ... | `SEXO`, `EDAD` en CB» (lista s2)'},
        {'decision': 'Filas CB con llave UPM/VIV_SEL/H_MUD/R_SEL repetida se conservan (la regla G-CS-DUPLICADA es del join CS, inexistente en E3).',
         'frase': '«una llave CS duplicada sale del eje (`G-CS-DUPLICADA`)» (spec s1)'},
        {'decision': 'C13/C14: blanco fuera del universo; universo 1,2,3,4,9; si = 1,2.',
         'frase': '«1,2 | 1,2,3,4,9 (blanco = no la identifica, fuera)» (lista s3)'},
        {'decision': 'C15: universo BP3_5=1 y BP3_6 en {1,2,9}; si = BP3_6=1.',
         'frase': '«`BP3_5`=1 y `BP3_6` ∈ 1,2,9» (lista s3)'},
        {'decision': 'Celda con N=0 en universo -> estado DENOMINADOR-CERO sin campos numericos.',
         'frase': '«Una celda sin personas emite `N`=0 y `P`/IC nulos» (spec s3)'},
        {'decision': 'Valores leidos como texto con espacios recortados; codigos comparados como texto.',
         'frase': '«el resto de códigos (blanco, fuera de catálogo) sale del universo» (lista s3)'},
    ]
    with open('salida/diagnostico.json', 'w', encoding='utf-8') as f:
        json.dump({'olas': diag_olas, 'decisiones': decisiones, 'llaves': diag_llaves},
                  f, ensure_ascii=False, indent=1)
    est = pd.Series([r['estado'] + '/' + r.get('estado_ic', '') for r in filas]).value_counts()
    print(est.to_string())


if __name__ == '__main__':
    main()
