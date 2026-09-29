"""Exploracion agregada (sin imprimir filas) de las columnas autorizadas."""
import pandas as pd

BASE = ['UPM', 'VIV_SEL', 'H_MUD', 'R_SEL', 'CD', 'EST_DIS', 'UPM_DIS', 'FAC_SEL',
        'BP1_1', 'BP1_2_03', 'BP1_2_08', 'BP1_2_09', 'BP1_3', 'BP1_4_3', 'BP1_4_4',
        'BP1_4_6', 'BP1_5_1', 'BP1_5_2', 'BP1_5_3', 'BP1_5_4', 'BP1_9_1', 'BP1_8_1',
        'SEXO', 'EDAD']
ARCHIVOS = [
    ('2024T1', 'paquete/datos/ensu_2024t1_cb.csv', BASE),
    ('2025T3', 'paquete/datos/ensu_2025t3_cb.csv', BASE),
    ('2025T4', 'paquete/datos/ensu_2025t4_cb.csv', BASE + ['BP3_5', 'BP3_6']),
]
for ola, ruta, cols in ARCHIVOS:
    d = pd.read_csv(ruta, usecols=cols, dtype=str, keep_default_na=False)
    print('=====', ola, len(d))
    for c in cols:
        s = d[c].str.strip()
        vc = s.value_counts().sort_index().to_dict() if s.nunique() <= 15 else ''
        print(c, 'len:', s.str.len().value_counts().to_dict(), 'blank:', (s == '').sum(),
              'nuniq:', s.nunique(), vc)
    fs = pd.to_numeric(d.FAC_SEL.str.strip(), errors='coerce')
    print('FAC_SEL<=0 o nan', (~(fs > 0)).sum())
    e = pd.to_numeric(d.EDAD, errors='coerce')
    print('EDAD min max', e.min(), e.max(), (e >= 97).sum(), (e < 18).sum())
    k = d.UPM.str.strip() + '|' + d.VIV_SEL.str.strip() + '|' + d.H_MUD.str.strip() + '|' + d.R_SEL.str.strip()
    print('llave dup', k.duplicated().sum())
    st = d.CD.str.strip() + '|' + d.EST_DIS.str.strip()
    u = st + '|' + d.UPM_DIS.str.strip()
    g = u.groupby(st).nunique()
    print('estratos', len(g), 'upms', u.nunique(), 'estratos 1-UPM', (g == 1).sum())
    print('UPM_DIS en >1 estrato', (d.assign(st=st).groupby(d.UPM_DIS.str.strip()).st.nunique() > 1).sum())
    print('ENT', sorted(d.UPM.str.strip().str.zfill(7).str[:2].unique()))
    print('CD', sorted(d.CD.str.strip().unique()))

# EDAD >= 96 por ola (conteos)
for ola, ruta, cols in ARCHIVOS:
    e = pd.read_csv(ruta, usecols=['EDAD'], dtype=str, keep_default_na=False).EDAD.str.strip()
    print(ola, 'EDAD>=96', e[e >= '96'].value_counts().sort_index().to_dict())
