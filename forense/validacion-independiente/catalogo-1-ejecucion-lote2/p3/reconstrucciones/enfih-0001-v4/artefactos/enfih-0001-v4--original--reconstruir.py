#!/usr/bin/env python3
"""Reconstrucción independiente; sólo entradas declaradas, sin resultados externos."""
import csv, hashlib, io, json, platform, shutil, zipfile
from collections import Counter
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent
ENTRADA = Path('/entrada')
RAW = Path('/raw')
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def guardar(nombre, objeto):
    (BASE / nombre).write_text(json.dumps(objeto, ensure_ascii=False, indent=2) + '\n')

def main():
    manifiesto = json.loads((ENTRADA / 'manifiesto.json').read_text())
    inventario = []
    for nombre, esperado in manifiesto['archivos'].items():
        p = ENTRADA / nombre
        observado = sha(p)
        assert observado == esperado, f'Hash discrepante: {nombre}'
        inventario.append(dict(ruta=str(p), bytes=p.stat().st_size, sha256=observado))
        if p.suffix != '.pdf':
            shutil.copyfile(p, BASE / 'entrada' / nombre)
    shutil.copyfile(ENTRADA / 'manifiesto.json', BASE / 'entrada/manifiesto.json')
    insumos = json.loads((ENTRADA / 'insumos.json').read_text())
    rutas = {}
    for item in insumos:
        p = RAW / item['id'] / Path(item['archivo']).name
        observado = sha(p)
        assert observado == item['sha256'], f'Hash discrepante: {p}'
        inventario.append(dict(ruta=str(p), archivo_declarado=item['archivo'],
                               bytes=p.stat().st_size, sha256=observado, url=item['url']))
        rutas[item['id']] = p
    with zipfile.ZipFile(rutas['enfih2019_bd_csv_zip']) as z:
        # Inventario central del ZIP; no se abre THOGAR.csv ni otras tablas.
        miembros = [dict(nombre=i.filename, bytes=i.file_size, crc32=f'{i.CRC:08x}')
                    for i in z.infolist()]
        contenido = z.read('TCONCENTRADORA.csv')
    d = pd.read_csv(io.BytesIO(contenido), dtype=str, keep_default_na=False)
    llaves = ['FOLIO', 'VIV_SEL', 'HOGAR']
    assert not d.duplicated(llaves).any(), 'Llave de hogar duplicada'
    assert not (d[llaves] == '').any().any(), 'Llave vacía'
    soporte = sorted(d.C_AFORE.unique().tolist())
    assert set(soporte) <= {'0', '1'}, 'NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA'
    d = d.sort_values(llaves, kind='stable')
    pesos = pd.to_numeric(d.FAC_HOG, errors='coerce')
    elegible = np.isfinite(pesos) & (pesos > 0)
    n_original = len(d)
    d = d.loc[elegible].copy()
    d['w'] = pesos.loc[elegible].astype(float)
    assert len(d) > 0
    assert not (d[['EDIS', 'UPM_DIS']] == '').any().any()
    # Sumas secuenciales en orden lexicográfico de la llave cruda.
    w = d.w.to_numpy()
    si = (d.C_AFORE == '1').to_numpy()
    total = sum(w)
    numerador = sum(w * si)
    complemento_num = sum(w * (d.C_AFORE == '0').to_numpy())
    punto = numerador / total
    complemento = complemento_num / total
    tolerancia = json.loads((ENTRADA / 'tolerancia.json').read_text())['abs']
    assert abs(punto + complemento - 1) <= tolerancia
    # Convención congelada: réplicas por fuera; estratos y UPM lexicográficos.
    # Cada extracción replica todo el conglomerado, usando sus totales ponderados.
    estratos = []
    for _, estrato in d.groupby('EDIS', sort=True):
        agregados = []
        for _, upm in estrato.groupby('UPM_DIS', sort=True):
            uw = upm.w.to_numpy()
            agregados.append((sum(uw * (upm.C_AFORE == '1').to_numpy()), sum(uw)))
        estratos.append(np.asarray(agregados, dtype=float))
    rng = np.random.Generator(np.random.PCG64(20260915))
    replicas = []
    for _ in range(2000):
        num, den = 0.0, 0.0
        for grupo in estratos:
            seleccion = rng.integers(0, len(grupo), size=len(grupo))
            t = grupo[seleccion].sum(axis=0)
            num += t[0]
            den += t[1]
        replicas.append(num / den)
    limites = np.percentile(replicas, [2.5, 97.5], method='linear')
    unicas = sum(len(g) == 1 for g in estratos)
    metodo_ic = 'IC-CON-ESTRATOS-DE-UPM-UNICA' if unicas else 'BOOTSTRAP-UPM-DENTRO-EDIS'
    b = d.loc[d.H_PPAL == '1']
    bp = sum(b.w.to_numpy() * (b.C_AFORE == '1').to_numpy()) / sum(b.w.to_numpy())
    with (ENTRADA / 'estimandos.tsv').open(newline='') as f:
        lector = csv.DictReader(f, delimiter='\t')
        campos = lector.fieldnames
        solicitudes = list(lector)
    extras = ['estado', 'valor', 'ic95_inf', 'ic95_sup', 'unidad_calculo', 'metodo_ic', 'motivo']
    with (BASE / 'reconstruccion.tsv').open('w', newline='') as f:
        escritor = csv.DictWriter(f, fieldnames=campos + extras, delimiter='\t')
        escritor.writeheader()
        for fila in solicitudes:
            k = fila['llave']
            if k in ['RESULT-ENFIH-A-P', 'RESULT-ENFIH-A-P-COMPLEMENTO']:
                fila.update(estado='RECONSTRUIDO', valor=format(punto if k.endswith('A-P') else complemento, '.17g'), unidad_calculo='proporcion [0,1]', motivo='')
                if k.endswith('A-P'):
                    fila.update(ic95_inf=format(limites[0], '.17g'), ic95_sup=format(limites[1], '.17g'), metodo_ic=metodo_ic)
            else:
                fila.update(estado='NO-RECALCULABLE-DESDE-SPEC', motivo='Llave sin método identificado en la entrada.')
            escritor.writerow(fila)
    guardar('diagnosticos.json', dict(filas_originales=n_original, filas_elegibles=len(d),
        filas_excluidas=n_original-len(d), soporte_C_AFORE=soporte, suma_pesos=total,
        numerador_si=numerador, numerador_no=complemento_num,
        A_SUMA_UNO=punto+complemento, A_METODO_IC=metodo_ic,
        estratos=len(estratos), upm_por_estrato_total=sum(map(len, estratos)), estratos_upm_unica=unicas,
        perfiles_anchos={k:dict(Counter(d[k].str.len().map(str))) for k in ['EDIS','UPM_DIS']},
        B_P=bp, B_DELTA_VS_A=bp-punto, B_rotulo='Sensibilidad de universo: H_PPAL == 1; secundaria',
        B_filas=len(b), replicas=2000, semilla=20260915, generador='numpy.PCG64',
        percentiles=[2.5,97.5], interpolacion='linear'))
    with (BASE / 'bootstrap.tsv').open('w') as f:
        f.write('replica\tproporcion\n')
        for i, valor in enumerate(replicas, 1): f.write(f'{i}\t{valor:.17g}\n')
    guardar('recibo.json', dict(paquete=manifiesto['paquete'],
        manifiesto_sha256=sha(ENTRADA / 'manifiesto.json'), entradas_e_insumos=inventario,
        miembros_zip=miembros, tabla_abierta='TCONCENTRADORA.csv',
        tabla_sha256=hashlib.sha256(contenido).hexdigest(),
        acceso_resultados_esperados=False, revelacion_solicitada=False,
        identidad='Se conservan las llaves e identidades recibidas; celda vacía permanece vacía.',
        versiones=dict(python=platform.python_version(), numpy=np.__version__, pandas=pd.__version__)))

if __name__ == '__main__':
    main()
