#!/usr/bin/env python3
"""Lanza sesiones nuevas aisladas; no revela esperados ni compara."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote2/p2'
LAUNCHER = ROOT / 'tools/validacion/astra6_lote2/lote2_lanza.sh'


def now():
    return datetime.now(timezone.utc).isoformat()


def launch(lot):
    package = lot['paquete_sucesor']
    folder = Path(lot['directorio_aislado'])
    record_path = BASE / 'lanzamientos' / (package + '--lanzamiento.json')
    attempt = lot.get('intento', 1)
    if attempt > 1:
        previous = json.loads(record_path.read_text())
        assert previous['exit_code'] != 0 and previous['estado'] == 'REVISAR-SALIDA'
        archived = BASE / 'intentos' / (package + '--intento' + str(attempt - 1) + '.json')
        archived.parent.mkdir(exist_ok=True)
        assert not archived.exists(), 'No sobrescribe intento'
        archived.write_bytes(record_path.read_bytes())
        original = folder
        folder = folder.with_name(folder.name + '--intento' + str(attempt))
        assert not folder.exists()
        folder.mkdir()
        for name in ('entrada', 'raw'):
            shutil.copytree(original / name, folder / name)
        shutil.copyfile(original / 'recibo-entrada.json', folder / 'recibo-entrada.json')
    else:
        assert not record_path.exists(), 'No repite una entrega previa'
    assert hashlib.sha256((folder / 'entrada/manifiesto.json').read_bytes()).hexdigest() == lot['sha256_manifiesto']
    proof = subprocess.run(['bash', str(LAUNCHER), '--prueba', str(folder)], capture_output=True, text=True)
    assert proof.returncode == 0, proof.stderr
    record = {'paquete': package, 'intento': attempt, 'paquete_original': lot['paquete_original'],
              'version_entrada': lot['version_entrada'], 'sha256_manifiesto': lot['sha256_manifiesto'],
              'paquete_sha256': lot['sha256_manifiesto'],
              'sha256_contenedor': lot['sha256_contenedor'],
              'entrada_registrada_utc': now(), 'separacion_efectiva': True,
              'prueba_separacion': proof.stdout, 'directorio_aislado': str(folder),
              'launcher_sha256': hashlib.sha256(LAUNCHER.read_bytes()).hexdigest(),
              'estado': 'LANZADO'}
    if attempt > 1:
        record.update(intento_previo_preservado=str(archived.relative_to(BASE)),
                      motivo_reintento='Fallo infraestructura API/routing antes de ejecución; sin números ni exposición a esperados')
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print('LANZADO ' + package, flush=True)
    # Logs completos quedan fuera del repo porque pueden contener vistas de raw.
    log = folder / 'lanzamiento.log'
    with log.open('w') as stream:
        process = subprocess.run(['bash', str(LAUNCHER), '--ejecuta', str(folder)], stdout=stream, stderr=subprocess.STDOUT)
    transcript = log.read_text()
    ids = re.findall(r'session id: ([a-f0-9-]+)', transcript)
    record.update(exit_code=process.returncode, finalizacion_utc=now(),
                  session_id=ids[0] if len(ids) == 1 else '',
                  log_local=str(log), log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),
                  estado='TERMINADO' if process.returncode == 0 else 'REVISAR-SALIDA')
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
    print('TERMINADO ' + package + ' exit=' + str(process.returncode), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paquete', help='Paquete sucesor exacto o restantes')
    parser.add_argument('--congelacion-p1', required=True, type=Path)
    parser.add_argument('--intento', default=1, type=int)
    args = parser.parse_args()
    assert args.congelacion_p1.is_file(), 'Congelación P1 ausente'
    freeze = json.loads(args.congelacion_p1.read_text())
    for key, path in (
        ('adaptador_sha256', LAUNCHER.parent / 'adaptador_comparador_v1.py'),
        ('contrato_sha256', args.congelacion_p1.parent / 'contrato-adaptador-v1.json'),
        ('pruebas_sha256', args.congelacion_p1.parent / 'pruebas-sinteticas-v1.json')):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == freeze[key], 'Congelación P1 alterada'
    (BASE / 'lanzamientos').mkdir(exist_ok=True)
    lots = json.loads((BASE / 'materializaciones.json').read_text())
    if args.paquete == 'restantes':
        assert (BASE.parent / 'p3/dictamenes/eder-0003-v4--dictamen.json').is_file(), 'EDER2 extremo a extremo pendiente'
        chosen = [lot for lot in lots if lot['paquete_original'] != 'eder-0003']
        with ThreadPoolExecutor(max_workers=3) as pool:
            list(pool.map(launch, chosen))
    else:
        chosen = [lot for lot in lots if lot['paquete_sucesor'] == args.paquete]
        assert len(chosen) == 1
        chosen[0]['intento'] = args.intento
        launch(chosen[0])
