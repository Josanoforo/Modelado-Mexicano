"""Reconstrucción ciega; ninguna llave recibe una identidad por su nombre."""
import csv
import hashlib
import io
import json
import platform
from pathlib import Path
import zipfile

import numpy as np

ROOT = Path(__file__).resolve().parent
ENTRADA = Path('/entrada')
RAW = Path('/raw')
MEMBER = ('conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/'
          'conjunto_de_datos_concentradohogar_enigh2022_ns.csv')


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()


def calcular_familia_a(groups):
    """Proporción ponderada recibe remesas; NO asigna llaves del encargo.

    Convenciones operativas: orden lexicográfico de llaves de texto,
    bucle réplica/estrato, n_h extracciones uniformes con reemplazo,
    percentiles con interpolación lineal. No son una identidad de resultado.
    """
    strata = [np.array([groups[s][u] for u in sorted(groups[s])], dtype=float)
              for s in sorted(groups)]
    total = sum((a.sum(axis=0) for a in strata), np.zeros(2))
    rng = np.random.Generator(np.random.PCG64(20260915))
    reps = np.empty(2000)
    for b in range(2000):
        draw = np.zeros(2)
        for a in strata:
            draw += a[rng.integers(0, len(a), size=len(a))].sum(axis=0)
        reps[b] = draw[0] / draw[1]
    lo, hi = np.percentile(reps, [2.5, 97.5], method='linear')
    single = any(len(a) == 1 for a in strata)
    return dict(estimacion=float(total[0] / total[1]), ic_inferior=float(lo),
                ic_superior=float(hi), naturaleza_ic=(
                    'IC-CON-ESTRATOS-DE-UPM-UNICA' if single else 'BOOTSTRAP'),
                lectura_ic='límite inferior' if single else 'percentiles 2.5/97.5')


def main():
    inventory = []
    manifest = json.loads((ENTRADA / 'manifiesto.json').read_text())
    for name in ['manifiesto.json', *manifest['archivos']]:
        p = ENTRADA / name
        digest = sha(p)
        expected = manifest['archivos'].get(name)
        if expected and digest != expected:
            raise ValueError('Hash de entrada no coincide: ' + name)
        inventory.append(dict(ruta=str(p), bytes=p.stat().st_size,
                              sha256=digest, sha256_declarado=expected))
    for item in json.loads((ENTRADA / 'insumos.json').read_text()):
        p = RAW / item['id'] / item['archivo']
        digest = sha(p)
        if digest != item['sha256']:
            raise ValueError('Hash de insumo no coincide: ' + str(p))
        inventory.append(dict(ruta=str(p), bytes=p.stat().st_size,
                              sha256=digest, sha256_declarado=item['sha256']))
    groups, seen = {}, set()
    archive = RAW / 'enigh2022_nc_csv/enigh2022_nc_csv.zip'
    with zipfile.ZipFile(archive) as z:
        entries = [dict(nombre=i.filename, bytes=i.file_size, crc32=f'{i.CRC:08x}')
                   for i in z.infolist()]
        content = z.read(MEMBER)
        member_sha = hashlib.sha256(content).hexdigest()
        reader = csv.DictReader(io.StringIO(content.decode('utf-8-sig')))
        for r in reader:
            identity = (r['folioviv'], r['foliohog'])
            if identity in seen:
                raise ValueError('Hogar duplicado')
            seen.add(identity)
            s, u = r['est_dis'], r['upm']
            if not all((*identity, s, u)):
                raise ValueError('Llave vacía')
            w, outcome = float(r['factor']), float(r['remesas'])
            if not np.isfinite(w) or w <= 0 or not np.isfinite(outcome):
                raise ValueError('Valor ausente o inválido; no hay regla de imputación')
            aggregate = groups.setdefault(s, {}).setdefault(u, [0., 0.])
            aggregate[0] += w * (outcome > 0)
            aggregate[1] += w
    requested = list(csv.DictReader((ENTRADA / 'estimandos.tsv').open(), delimiter='\t'))
    # La única identidad documentada es A/recibe remesas/HOGAR.
    # No se autoriza mapear P-COMPLEMENTO/no_recibe_remesas a esa identidad.
    if len(requested) != 1 or requested[0]['llave'] != 'RESULT-ENIGH-A-P-COMPLEMENTO':
        raise ValueError('El conjunto de estimandos cambió; requiere nueva revisión humana')
    fields = list(requested[0]) + ['estado', 'estimacion', 'ic_inferior', 'ic_superior', 'motivo']
    with (ROOT / 'reconstruccion.tsv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fields, delimiter='\t')
        writer.writeheader()
        for row in requested:
            writer.writerow(dict(row, estado='NO-RECALCULABLE-DESDE-SPEC',
                estimacion='', ic_inferior='', ic_superior='',
                motivo='Identidad insuficiente: metodo.md define A recibe remesas (remesas > 0), '
                'pero la llave pide no_recibe_remesas, unidad VER-SPEC y celda vacía. '
                'No hay asignación explícita ni regla de complemento; no se infiere por el nombre.'))
    receipt = dict(manifiesto_sha256=sha(ENTRADA / 'manifiesto.json'),
        fase='CONGELACION-PRE-REVELACION', resultados_esperados_accedidos=False,
        solicitudes_al_preparador=0, entradas=inventory,
        miembro_usado=dict(archivo=str(archive), nombre=MEMBER, sha256=member_sha),
        validacion=dict(hogares=len(seen), estratos=len(groups),
            upm_por_estrato_total=sum(map(len, groups.values())),
            estratos_upm_unica=sum(len(g) == 1 for g in groups.values())),
        entorno=dict(python=platform.python_version(), numpy=np.__version__),
        tolerancia=json.loads((ENTRADA / 'tolerancia.json').read_text()),
        motor_familia_a='Implementado; no ejecutado sobre raw porque no tiene llave identificada',
        estimandos_con_cifras=0)
    for name, value in [('recibo.json', receipt), ('entradas_zip.json', entries)]:
        (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
