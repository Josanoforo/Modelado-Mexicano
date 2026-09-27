#!/usr/bin/env python3
"""Lanza sesiones nuevas aisladas; no revela esperados ni compara."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'forense/validacion-independiente/catalogo-1-ejecucion-lote1'
LAUNCHER = ROOT / 'tools/validacion/astra6_lote1/lanza.sh'


def now():
    return datetime.now(timezone.utc).isoformat()


def launch(lot):
    package = lot['paquete']
    folder = Path('/home/pc0/astra6-c1-aislado') / ('tanda2-' + package)
    record_path = BASE / 'lanzamientos' / (package + '--lanzamiento.json')
    assert not record_path.exists(), 'No repite una entrega previa'
    assert hashlib.sha256((folder / 'entrada/manifiesto.json').read_bytes()).hexdigest() == lot['sha256']
    proof = subprocess.run(['bash', str(LAUNCHER), '--prueba', str(folder)], capture_output=True, text=True)
    assert proof.returncode == 0, proof.stderr
    record = {'paquete': package, 'paquete_sha256': lot['sha256'],
              'sha256_contenedor': lot['sha256_contenedor'],
              'entrada_registrada_utc': now(), 'separacion_efectiva': True,
              'prueba_separacion': proof.stdout, 'directorio_aislado': str(folder),
              'launcher_sha256': hashlib.sha256(LAUNCHER.read_bytes()).hexdigest(),
              'estado': 'LANZADO'}
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
    # La primera comparación es condición de secuencia, nunca se simula.
    first = BASE / 'comparaciones/endireh-pisos-2021-comunitaria-0001--comparacion.json'
    assert first.is_file()
    (BASE / 'lanzamientos').mkdir(exist_ok=True)
    lots = json.loads((ROOT / 'forense/validacion-independiente/catalogo-1/lotes.json').read_text())
    remaining = [lot for lot in lots if lot['estado_preparacion'] == 'DISPONIBLE' and 'comunitaria' not in lot['paquete']]
    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(launch, remaining))
