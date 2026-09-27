"""Reconstrucción independiente; ejecutar con Python 3, numpy y pandas."""
from pathlib import Path
import csv, hashlib, json, platform, shutil, zipfile
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parent
ENT = Path('/entrada')
def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()
def dump(name, data):
    (OUT/name).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)+'\n')

def main():
    manifest = json.loads((ENT/'manifiesto.json').read_text())
    inputs = []
    (OUT/'entradas').mkdir(exist_ok=True)
    for p in sorted(ENT.iterdir()):
        actual = sha(p)
        if p.name in manifest['archivos']:
            assert actual == manifest['archivos'][p.name], p.name
        inputs.append(dict(ruta=str(p), bytes=p.stat().st_size, sha256=actual))
        if p.suffix != '.pdf': shutil.copyfile(p, OUT/'entradas'/p.name)
    archives = json.loads((ENT/'insumos.json').read_text())
    inventory = []
    for a in archives:
        p = Path('/raw')/a['id']/a['archivo']
        actual = sha(p)
        assert actual == a['sha256'], str(p)
        inputs.append(dict(ruta=str(p), bytes=p.stat().st_size, sha256=actual))
        with zipfile.ZipFile(p) as z:
            inventory.extend(dict(archivo=str(p), entrada=i.filename, bytes=i.file_size,
                                  crc32=f'{i.CRC:08x}') for i in z.infolist())
    dump('inventario_zip.json', inventory)
    archive = Path('/raw/enigh2020_nc_csv/enigh2020_nc_csv.zip')
    member = ('conjunto_de_datos_concentradohogar_enigh_2020_ns/conjunto_de_datos/'
              'conjunto_de_datos_concentradohogar_enigh_2020_ns.csv')
    with zipfile.ZipFile(archive) as z:
        blob = z.read(member)
        import io
        d = pd.read_csv(io.BytesIO(blob), dtype=str, keep_default_na=False)
    assert not d.duplicated(['folioviv','foliohog']).any(), 'Llave de hogar duplicada'
    assert (d[['folioviv','foliohog']] != '').all().all()
    w,r,y = [pd.to_numeric(d[c],errors='coerce').to_numpy(dtype=float)
             for c in ['factor','remesas','ing_cor']]
    fw = np.isfinite(w) & (w>0)
    vr = np.isfinite(r) & (r>=0)
    valid = fw & vr
    rec = valid & (r>0)
    dom = rec & np.isfinite(y) & (y>0)
    def counts(mask):
        return dict(n=int(mask.sum()), masa_factor_valido=float(w[mask & fw].sum()))
    stats = {
        'marco': counts(np.ones(len(d),dtype=bool)),
        'factor_invalido': counts(~fw), 'remesas_invalidas': counts(~vr),
        'universo_valido': counts(valid), 'receptores': counts(rec),
        'participacion': counts(dom),
        'exclusion_ing_cor_ausente_no_numerico_no_finito': counts(rec & ~np.isfinite(y)),
        'exclusion_ing_cor_cero': counts(rec & (y==0)),
        'exclusion_ing_cor_negativo': counts(rec & np.isfinite(y) & (y<0)),
        'remesas_mayor_ing_cor_mas_001': counts(dom & (r>y+0.01))}
    assert rec.any() and dom.any()
    rr,ww = r[rec],w[rec]
    order = np.argsort(rr,kind='stable')
    median = rr[order][np.searchsorted(np.cumsum(ww[order]),ww.sum()/2,side='left')]
    # Cinco contribuciones sobre TODAS las filas, cero fuera del dominio.
    c = np.zeros((len(d),5),dtype=float)
    c[dom] = np.column_stack([w[dom],w[dom]*r[dom]/y[dom],
                             w[dom]*r[dom],w[dom]*y[dom],
                             w[dom]*(r[dom]/y[dom]>=0.5)])
    def ratios(t): return np.array([t[1]/t[0],t[2]/t[3],t[4]/t[0]])
    point = ratios(c.sum(axis=0))
    points = dict(participacion_media_hogar_remesas=point[0],
                  participacion_agregada_remesas=point[1], participacion_ge50_remesas=point[2],
                  prevalencia_remesas=w[rec].sum()/w[valid].sum(),
                  remesas_media_remesas=np.sum(ww*rr)/ww.sum(), remesas_mediana_remesas=median)
    ci = {}
    operational = (d[['est_dis','upm']].apply(lambda s:s.str.strip())!='').all().all()
    stats['diseno_operativo'] = bool(operational)
    if operational:
        frame = pd.DataFrame(c,columns=['w','wr_y','wr','wy','wge50'])
        frame['est_dis'],frame['upm'] = d.est_dis,d.upm
        grouped = frame.groupby(['est_dis','upm'],sort=True,dropna=False).sum()
        strata = [g.to_numpy() for _,g in grouped.groupby(level=0,sort=True)]
        stats['estratos'] = len(strata)
        stats['upm_en_estrato'] = len(grouped)
        stats['estratos_upm_unica'] = sum(len(g)==1 for g in strata)
        rng = np.random.Generator(np.random.PCG64(20260916))
        boot = np.empty((2000,3))
        for b in range(2000):
            total = np.zeros(5)
            for g in strata:
                # Orden réplica -> estrato textual -> UPM textual.
                ix = rng.integers(0,len(g),size=len(g))
                total += g[ix].sum(axis=0)
            boot[b] = ratios(total)
        assert np.isfinite(boot).all(), 'Réplica con denominador inválido'
        np.savetxt(OUT/'replicas.tsv', boot, delimiter='\t',fmt='%.17g',
                   header='media_hogar\tagregada\tge50',comments='')
        limits = np.percentile(boot,[2.5,97.5],axis=0,method='linear')
        for j,k in enumerate(['participacion_media_hogar_remesas','participacion_agregada_remesas','participacion_ge50_remesas']):
            ci[k] = limits[:,j]
    rows = list(csv.DictReader((ENT/'estimandos.tsv').open(),delimiter='\t'))
    fields = list(rows[0])+['estado','valor','ic95_inf','ic95_sup','motivo','estado_diagnostico','motivo_ic']
    with (OUT/'reconstruccion.tsv').open('w') as f:
        writer = csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n')
        writer.writeheader()
        for row in rows:
            k = row['conducta']
            assert row['instrumento']=='ENIGH' and row['ola']=='2020'
            if k not in points:
                row.update(estado='NO-RECALCULABLE-DESDE-SPEC',motivo='Conducta sin definición en el método')
            else:
                row.update(estado='RECONSTRUIDO',valor=format(points[k],'.17g'),motivo='')
                if k in ci: row.update(ic95_inf=format(ci[k][0],'.17g'),ic95_sup=format(ci[k][1],'.17g'))
                elif row['naturaleza_ic']!='SIN-IC-IDENTIFICADO': row['motivo_ic']='Diseño no operativo'
                if k.startswith('participacion_') and stats['remesas_mayor_ing_cor_mas_001']['n']:
                    row['estado_diagnostico']='REPORTADO-CON-INCOMPATIBILIDAD-R-MAYOR-Y'
            writer.writerow(row)
    dump('diagnosticos.json',stats)
    dump('recibo.json',dict(manifiesto_sha256=sha(ENT/'manifiesto.json'),
         fase='CONGELACION-PRE-REVELACION',resultados_esperados_accedidos=False,
         solicitudes_al_preparador=0,entradas=inputs,
         miembro_utilizado=dict(archivo=str(archive),entrada=member,sha256=hashlib.sha256(blob).hexdigest()),
         entorno=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__),
         convenciones_bootstrap=dict(replicas=2000,semilla=20260916,generador='numpy.PCG64',
          orden='réplica, estrato lexicográfico, UPM lexicográfica; identidades conservadas como texto',
          muestreo='n_h índices uniformes con reemplazo con Generator.integers; sin reescalado',
          percentiles='numpy.percentile method=linear',
          limitacion='UPM única se remuestrea a sí misma, variación cero; no se afirma cota inferior',
          insuficiencia_para_igualdad_bit_a_bit='El método no fija orden de consumo RNG, algoritmo de extracción ni interpolación de percentiles; se registran las convenciones propias sin inferir las del preparador.'),
         archivos_congelados={n:sha(OUT/n) for n in ['reconstruir.py','reconstruccion.tsv','diagnosticos.json','replicas.tsv']}))

if __name__=='__main__': main()
